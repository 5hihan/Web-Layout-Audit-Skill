#!/usr/bin/env python3
"""Runtime UI probe for device-sized browser evidence.

Requires Python Playwright and installed browsers. This script opens a URL or
local HTML file across device-sized viewports and reports layout facts, visual
risks, and proof gaps. It is an evidence helper, not a complete audit.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


DEFAULT_PRESETS: dict[str, tuple[int, int]] = {
    "small-phone": (320, 568),
    "iphone-se": (375, 667),
    "modern-phone": (390, 844),
    "android-phone": (412, 915),
    "tablet": (768, 1024),
    "desktop": (1440, 900),
}


@dataclass(frozen=True)
class RuntimeFinding:
    severity: str
    viewport: str
    rule: str
    message: str
    evidence: dict[str, Any]


@dataclass(frozen=True)
class ViewportResult:
    name: str
    width: int
    height: int
    url: str
    screenshot: str | None
    metrics: dict[str, Any]
    findings: list[RuntimeFinding]


AUDIT_SCRIPT = r"""
() => {
  const doc = document.documentElement;
  const body = document.body;
  const visual = window.visualViewport;
  const viewport = {
    width: Math.round((visual ? visual.width : doc.clientWidth || window.innerWidth) * 10) / 10,
    height: Math.round((visual ? visual.height : doc.clientHeight || window.innerHeight) * 10) / 10,
    layoutWidth: window.innerWidth,
    layoutHeight: window.innerHeight,
    clientWidth: doc.clientWidth,
    clientHeight: doc.clientHeight,
  };
  const findings = [];

  function add(severity, rule, message, evidence) {
    findings.push({ severity, rule, message, evidence });
  }

  function selectorFor(el) {
    if (!el || !el.tagName) return '';
    const tag = el.tagName.toLowerCase();
    const id = el.id ? `#${el.id}` : '';
    const classes = typeof el.className === 'string'
      ? el.className.trim().split(/\s+/).filter(Boolean).slice(0, 3).map((item) => `.${item}`).join('')
      : '';
    const role = el.getAttribute('role') ? `[role="${el.getAttribute('role')}"]` : '';
    return `${tag}${id}${classes}${role}`;
  }

  function rectFor(el) {
    const rect = el.getBoundingClientRect();
    return {
      x: Math.round(rect.x * 10) / 10,
      y: Math.round(rect.y * 10) / 10,
      width: Math.round(rect.width * 10) / 10,
      height: Math.round(rect.height * 10) / 10,
      left: Math.round(rect.left * 10) / 10,
      right: Math.round(rect.right * 10) / 10,
      top: Math.round(rect.top * 10) / 10,
      bottom: Math.round(rect.bottom * 10) / 10,
    };
  }

  function isVisible(el) {
    const style = getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return (
      style.display !== 'none' &&
      style.visibility !== 'hidden' &&
      Number(style.opacity || '1') > 0.01 &&
      rect.width > 0.5 &&
      rect.height > 0.5
    );
  }

  function textFor(el) {
    return (el.innerText || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 120);
  }

  const all = Array.from(document.querySelectorAll('body *')).filter((el) => {
    const tag = el.tagName.toLowerCase();
    return !['script', 'style', 'noscript', 'template', 'svg', 'path'].includes(tag) && isVisible(el);
  });

  const viewportMeta = document.querySelector('meta[name="viewport"]');
  if (!viewportMeta) {
    add('critical', 'viewport-meta-missing', 'No viewport meta tag was found at runtime.', {});
  } else {
    const content = viewportMeta.getAttribute('content') || '';
    if (/user-scalable\s*=\s*no|maximum-scale\s*=\s*1/i.test(content)) {
      add('critical', 'viewport-zoom-disabled', 'Viewport meta appears to restrict zoom.', { content });
    }
    if (!/viewport-fit\s*=\s*cover/i.test(content)) {
      add('warning', 'viewport-fit-cover-missing', 'Viewport meta does not include viewport-fit=cover.', { content });
    }
  }

  const horizontalOverflow = Math.max(doc.scrollWidth, body ? body.scrollWidth : 0) - viewport.width;
  if (horizontalOverflow > 1) {
    add('critical', 'horizontal-overflow', 'Document is wider than the viewport.', {
      viewportWidth: viewport.width,
      documentScrollWidth: Math.max(doc.scrollWidth, body ? body.scrollWidth : 0),
      overflowPixels: horizontalOverflow,
    });
  }

  const htmlStyle = getComputedStyle(doc);
  const bodyStyle = body ? getComputedStyle(body) : null;
  if (htmlStyle.overflowX === 'hidden' || (bodyStyle && bodyStyle.overflowX === 'hidden')) {
    add('warning', 'runtime-overflow-x-hidden', 'Root overflow-x:hidden can hide real layout defects.', {
      htmlOverflowX: htmlStyle.overflowX,
      bodyOverflowX: bodyStyle ? bodyStyle.overflowX : null,
    });
  }

  const outside = [];
  const clipped = [];
  const fixedBottom = [];
  const fixedBottomElements = [];
  const fixedOrSticky = [];
  const bottomOverlapRisks = [];
  const bottomClearanceRisks = [];
  const smallTargets = [];
  const unnamedControls = [];
  const inputZoomRisks = [];
  const imageRisks = [];

  const interactiveSelector = [
    'a[href]',
    'button',
    'input',
    'select',
    'textarea',
    '[role="button"]',
    '[role="link"]',
    '[role="menuitem"]',
    '[role="tab"]',
    '[tabindex]:not([tabindex="-1"])'
  ].join(',');

  const interactive = Array.from(document.querySelectorAll(interactiveSelector)).filter((el) => {
    return isVisible(el) && !el.disabled && el.getAttribute('aria-hidden') !== 'true';
  });

  for (const el of all) {
    const rect = rectFor(el);
    const style = getComputedStyle(el);
    if ((rect.left < -2 || rect.right > viewport.width + 2) && rect.width <= viewport.width * 3) {
      outside.push({ selector: selectorFor(el), rect, text: textFor(el) });
    }
    const overflowX = el.scrollWidth - el.clientWidth;
    const overflowY = el.scrollHeight - el.clientHeight;
    const clipsOverflow = ['hidden', 'clip', 'auto', 'scroll'].includes(style.overflowX) || ['hidden', 'clip', 'auto', 'scroll'].includes(style.overflowY);
    if ((overflowX > 2 || overflowY > 2) && clipsOverflow && textFor(el)) {
      clipped.push({
        selector: selectorFor(el),
        rect,
        scrollWidth: el.scrollWidth,
        clientWidth: el.clientWidth,
        scrollHeight: el.scrollHeight,
        clientHeight: el.clientHeight,
        overflowX: style.overflowX,
        overflowY: style.overflowY,
        text: textFor(el),
      });
    }
    if (style.position === 'fixed' || style.position === 'sticky') {
      fixedOrSticky.push({ selector: selectorFor(el), position: style.position, rect, zIndex: style.zIndex });
      if (style.position === 'fixed' && viewport.height - rect.bottom <= 4) {
        fixedBottom.push({ selector: selectorFor(el), rect, paddingBottom: style.paddingBottom, zIndex: style.zIndex });
        fixedBottomElements.push(el);
      }
    }
  }

  for (const el of interactive) {
    const rect = rectFor(el);
    const name = (
      el.getAttribute('aria-label') ||
      el.getAttribute('title') ||
      el.getAttribute('alt') ||
      textFor(el)
    ).trim();
    if (rect.width < 44 || rect.height < 44) {
      smallTargets.push({ selector: selectorFor(el), rect, text: textFor(el) });
    }
    if (!name) {
      unnamedControls.push({ selector: selectorFor(el), rect });
    }
    const style = getComputedStyle(el);
    const tag = el.tagName.toLowerCase();
    if ((tag === 'input' || tag === 'textarea' || tag === 'select') && parseFloat(style.fontSize) < 16) {
      inputZoomRisks.push({ selector: selectorFor(el), rect, fontSize: style.fontSize });
    }
  }

  for (const img of Array.from(document.querySelectorAll('img')).filter(isVisible)) {
    const rect = rectFor(img);
    const alt = img.getAttribute('alt');
    if (alt === null || (!img.getAttribute('width') || !img.getAttribute('height'))) {
      imageRisks.push({
        selector: selectorFor(img),
        rect,
        altMissing: alt === null,
        widthAttr: img.getAttribute('width'),
        heightAttr: img.getAttribute('height'),
        src: img.currentSrc || img.src,
      });
    }
  }

  function isInsideFixedBottom(el) {
    return fixedBottomElements.some((fixed) => fixed === el || fixed.contains(el));
  }

  function hasMeaningfulChild(el) {
    return Array.from(el.children || []).some((child) => {
      return isVisible(child) && !isInsideFixedBottom(child) && (textFor(child) || child.matches(interactiveSelector) || child.tagName.toLowerCase() === 'img');
    });
  }

  function isContentBlock(el) {
    const tag = el.tagName.toLowerCase();
    const className = typeof el.className === 'string' ? el.className : '';
    return (
      ['article', 'section', 'li', 'form', 'figure'].includes(tag) ||
      /(?:card|panel|item|row|tile|sheet|drawer|cta|restaurant|product|checkout)/i.test(className)
    );
  }

  if (fixedBottomElements.length) {
    const fixedRects = fixedBottomElements.map(rectFor);
    const fixedTop = Math.min(...fixedRects.map((rect) => rect.top));
    const fixedHeight = Math.max(...fixedRects.map((rect) => viewport.height - rect.top));
    const overlapped = all.filter((el) => {
      if (isInsideFixedBottom(el)) return false;
      const style = getComputedStyle(el);
      if (style.position === 'fixed' || style.position === 'sticky') return false;
      const rect = rectFor(el);
      if (rect.bottom <= fixedTop + 1 || rect.top >= viewport.height - 1) return false;
      if (hasMeaningfulChild(el) && !isContentBlock(el)) return false;
      return textFor(el) || el.matches(interactiveSelector) || el.tagName.toLowerCase() === 'img';
    });
    for (const el of overlapped.slice(0, 40)) {
      bottomOverlapRisks.push({ selector: selectorFor(el), rect: rectFor(el), text: textFor(el) });
    }

    const documentHeight = Math.max(doc.scrollHeight, body ? body.scrollHeight : 0);
    let bottomMostContent = 0;
    for (const el of all) {
      if (isInsideFixedBottom(el)) continue;
      const style = getComputedStyle(el);
      if (style.position === 'fixed' || style.position === 'sticky') continue;
      if (!(textFor(el) || el.matches(interactiveSelector) || el.tagName.toLowerCase() === 'img')) continue;
      if (hasMeaningfulChild(el) && !isContentBlock(el)) continue;
      const rect = rectFor(el);
      bottomMostContent = Math.max(bottomMostContent, rect.bottom + window.scrollY);
    }
    const bottomContentClearance = Math.round((documentHeight - bottomMostContent) * 10) / 10;
    const minimumNeeded = Math.round(Math.min(fixedHeight, 160) * 10) / 10;
    if (bottomMostContent > 0 && bottomContentClearance < minimumNeeded - 4) {
      bottomClearanceRisks.push({
        fixedBottomHeight: Math.round(fixedHeight * 10) / 10,
        fixedTop: Math.round(fixedTop * 10) / 10,
        documentHeight,
        bottomMostContent: Math.round(bottomMostContent * 10) / 10,
        bottomContentClearance,
        minimumNeeded,
      });
    }
  }

  function addLimited(severity, rule, message, list, limit = 20) {
    if (list.length) {
      add(severity, rule, message, { count: list.length, examples: list.slice(0, limit) });
    }
  }

  addLimited('critical', 'element-outside-viewport', 'Visible elements extend outside the viewport.', outside);
  addLimited('critical', 'clipped-visible-content', 'Visible text/content appears clipped or internally scrollable.', clipped);
  addLimited('warning', 'fixed-bottom-runtime', 'Fixed bottom elements need safe-area and scroll-end verification.', fixedBottom);
  addLimited('warning', 'bottom-fixed-overlap-runtime', 'Fixed bottom UI currently shares visible space with page content; inspect bottom nav, cards, and sticky actions.', bottomOverlapRisks);
  addLimited('warning', 'bottom-scroll-clearance-runtime', 'Document bottom clearance is smaller than the fixed bottom UI height; final scroll content may hide behind bottom chrome.', bottomClearanceRisks);
  addLimited('warning', 'small-touch-target-runtime', 'Interactive controls smaller than 44 by 44 CSS pixels were found.', smallTargets);
  addLimited('warning', 'unnamed-control-runtime', 'Interactive controls without obvious accessible names were found.', unnamedControls);
  addLimited('warning', 'ios-input-zoom-risk-runtime', 'Form controls below 16px font size can trigger iOS input zoom.', inputZoomRisks);
  addLimited('warning', 'image-runtime-risk', 'Images missing alt text or intrinsic dimensions were found.', imageRisks);

  const metrics = {
    viewport,
    document: {
      scrollWidth: Math.max(doc.scrollWidth, body ? body.scrollWidth : 0),
      scrollHeight: Math.max(doc.scrollHeight, body ? body.scrollHeight : 0),
      clientWidth: doc.clientWidth,
      clientHeight: doc.clientHeight,
    },
    counts: {
      visibleElements: all.length,
      interactive: interactive.length,
      fixedOrSticky: fixedOrSticky.length,
      fixedBottom: fixedBottom.length,
      bottomOverlapRisks: bottomOverlapRisks.length,
      bottomClearanceRisks: bottomClearanceRisks.length,
      outsideViewport: outside.length,
      clipped: clipped.length,
      smallTargets: smallTargets.length,
      unnamedControls: unnamedControls.length,
      inputZoomRisks: inputZoomRisks.length,
      imageRisks: imageRisks.length,
    },
    htmlClassList: Array.from(doc.classList),
    fixedOrSticky: fixedOrSticky.slice(0, 20),
  };

  return { metrics, findings };
}
"""


def normalize_target(target: str) -> str:
    if target.startswith(("http://", "https://", "file://")):
        return target
    path = Path(target).resolve()
    return path.as_uri()


def parse_viewport(value: str) -> tuple[str, int, int]:
    if "=" in value:
        name, size = value.split("=", 1)
    else:
        name, size = value, value
    width_text, height_text = size.lower().split("x", 1)
    return name, int(width_text), int(height_text)


def selected_viewports(values: list[str] | None) -> dict[str, tuple[int, int]]:
    if not values:
        return DEFAULT_PRESETS
    selected: dict[str, tuple[int, int]] = {}
    for value in values:
        if value == "all":
            selected.update(DEFAULT_PRESETS)
        elif value in DEFAULT_PRESETS:
            selected[value] = DEFAULT_PRESETS[value]
        else:
            name, width, height = parse_viewport(value)
            selected[name] = (width, height)
    return selected


def run_probe(args: argparse.Namespace) -> dict[str, Any]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as error:
        return {
            "ok": False,
            "error": "Python Playwright is not installed.",
            "detail": str(error),
            "install_hint": "Install with: python -m pip install playwright && python -m playwright install chromium",
        }

    target = normalize_target(args.target)
    audit_dir = Path(args.audit_dir).resolve() if args.audit_dir else None
    if audit_dir:
        (audit_dir / "screenshots").mkdir(parents=True, exist_ok=True)
        (audit_dir / "reports").mkdir(parents=True, exist_ok=True)
        (audit_dir / "logs").mkdir(parents=True, exist_ok=True)
    if audit_dir and args.screenshots_dir:
        screenshot_dir = (audit_dir / args.screenshots_dir).resolve()
    elif audit_dir:
        screenshot_dir = (audit_dir / "screenshots" / "runtime-probe").resolve()
    else:
        screenshot_dir = Path(args.screenshots_dir).resolve() if args.screenshots_dir else None
    if screenshot_dir:
        screenshot_dir.mkdir(parents=True, exist_ok=True)

    viewports = selected_viewports(args.viewport)
    results: list[ViewportResult] = []

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                for name, (width, height) in viewports.items():
                    context = browser.new_context(
                        viewport={"width": width, "height": height},
                        device_scale_factor=1,
                        is_mobile=width < 800,
                        has_touch=width < 800,
                        reduced_motion=args.reduced_motion,
                        color_scheme=args.color_scheme,
                    )
                    page = context.new_page()
                    page.goto(target, wait_until=args.wait_until, timeout=args.timeout)
                    if args.html_class:
                        page.evaluate("classes => document.documentElement.classList.add(...classes)", args.html_class)
                    if args.wait_ms:
                        page.wait_for_timeout(args.wait_ms)
                    audit = page.evaluate(AUDIT_SCRIPT)
                    screenshot_path = None
                    if screenshot_dir:
                        screenshot_path = str((screenshot_dir / f"{name}.png").resolve())
                        page.screenshot(path=screenshot_path, full_page=True)
                    findings = [
                        RuntimeFinding(
                            severity=item["severity"],
                            viewport=name,
                            rule=item["rule"],
                            message=item["message"],
                            evidence=item["evidence"],
                        )
                        for item in audit["findings"]
                    ]
                    results.append(
                        ViewportResult(
                            name=name,
                            width=width,
                            height=height,
                            url=page.url,
                            screenshot=screenshot_path,
                            metrics=audit["metrics"],
                            findings=findings,
                        )
                    )
                    context.close()
            finally:
                browser.close()
    except Exception as error:  # Playwright reports missing browser installs here.
        return {
            "ok": False,
            "error": "Runtime probe failed.",
            "detail": str(error),
            "install_hint": "If Chromium is missing, run: python -m playwright install chromium",
        }

    all_findings = [finding for result in results for finding in result.findings]
    summary = {
        "viewports": len(results),
        "findings": len(all_findings),
        "critical": sum(1 for item in all_findings if item.severity == "critical"),
        "warning": sum(1 for item in all_findings if item.severity == "warning"),
        "info": sum(1 for item in all_findings if item.severity == "info"),
    }
    return {
        "ok": True,
        "target": target,
        "artifactPaths": {
            "auditDir": str(audit_dir) if audit_dir else None,
            "screenshotsDir": str(screenshot_dir) if screenshot_dir else None,
        },
        "summary": summary,
        "results": [
            {
                **asdict(result),
                "findings": [asdict(item) for item in result.findings],
            }
            for result in results
        ],
    }


def print_text(report: dict[str, Any]) -> None:
    if not report.get("ok"):
        print(report.get("error", "Runtime probe failed."))
        print(report.get("detail", ""))
        if report.get("install_hint"):
            print(report["install_hint"])
        return

    summary = report["summary"]
    print("Runtime UI probe")
    print(f"Target: {report['target']}")
    artifacts = report.get("artifactPaths", {})
    if artifacts.get("auditDir"):
        print(f"Audit dir: {artifacts['auditDir']}")
    if artifacts.get("jsonReport"):
        print(f"JSON report: {artifacts['jsonReport']}")
    print(
        f"Viewports: {summary['viewports']} | Findings: {summary['findings']} "
        f"(critical {summary['critical']}, warning {summary['warning']}, info {summary['info']})"
    )
    for result in report["results"]:
        print()
        print(f"{result['name']} ({result['width']}x{result['height']})")
        print(f"URL: {result['url']}")
        if result["screenshot"]:
            print(f"Screenshot: {result['screenshot']}")
        counts = result["metrics"]["counts"]
        print(
            "Counts: "
            f"outside={counts['outsideViewport']}, clipped={counts['clipped']}, "
            f"fixedBottom={counts['fixedBottom']}, bottomOverlap={counts['bottomOverlapRisks']}, "
            f"bottomClearance={counts['bottomClearanceRisks']}, "
            f"smallTargets={counts['smallTargets']}, unnamedControls={counts['unnamedControls']}"
        )
        for finding in result["findings"]:
            print(f"- [{finding['severity'].upper()}] {finding['rule']}: {finding['message']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="URL or local HTML file to probe.")
    parser.add_argument(
        "--viewport",
        action="append",
        help="Preset name, all, or custom NAME=WIDTHxHEIGHT. May be repeated.",
    )
    parser.add_argument("--screenshots-dir", help="Directory for per-viewport full-page screenshots.")
    parser.add_argument(
        "--audit-dir",
        help="Single root folder for generated artifacts. Screenshots go under screenshots/ and JSON reports under reports/.",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--wait-until", default="networkidle", choices=("load", "domcontentloaded", "networkidle", "commit"))
    parser.add_argument("--wait-ms", type=int, default=0)
    parser.add_argument(
        "--html-class",
        action="append",
        default=[],
        help="Class to add to <html> before auditing, useful for class-based standalone/PWA CSS such as pwa-standalone. May be repeated.",
    )
    parser.add_argument("--timeout", type=int, default=30000)
    parser.add_argument("--reduced-motion", choices=("reduce", "no-preference"), default="no-preference")
    parser.add_argument("--color-scheme", choices=("light", "dark", "no-preference"), default="light")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on critical or warning findings.")
    args = parser.parse_args()
    if args.audit_dir is None and args.screenshots_dir:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        args.audit_dir = str(Path("web-layout-audit-runs") / f"runtime-probe-{timestamp}")

    report = run_probe(args)
    if args.audit_dir and report.get("ok"):
        report_path = Path(args.audit_dir).resolve() / "reports" / "runtime-probe.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report.setdefault("artifactPaths", {})["jsonReport"] = str(report_path)
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print_text(report)

    if not report.get("ok"):
        return 2
    summary = report["summary"]
    if args.strict and (summary["critical"] or summary["warning"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

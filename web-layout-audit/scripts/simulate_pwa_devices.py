#!/usr/bin/env python3
"""Playwright multi-device PWA display-mode simulator.

This is a high-fidelity simulator, not a real-device oracle. It uses Playwright
device descriptors, browser engines, touch/DPR/user-agent emulation, screenshots,
standalone JS signals, root classes, and a best-effort CSS media-rule clone for
`@media (display-mode: standalone)`. Real iOS Home Screen Web.app chrome,
platform safe-area env() values, and OS install state still require hardware.
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from probe_ui_runtime import AUDIT_SCRIPT, normalize_target


@dataclass(frozen=True)
class DeviceProfile:
    key: str
    label: str
    platform: str
    preferred_browser: str
    playwright_device: str | None
    viewport: dict[str, int]
    screen: dict[str, int]
    device_scale_factor: float
    is_mobile: bool
    has_touch: bool
    user_agent: str
    safe_area_top: int
    safe_area_bottom: int
    notes: str


@dataclass(frozen=True)
class SimulationFinding:
    severity: str
    device: str
    mode: str
    rule: str
    message: str
    evidence: dict[str, Any]


@dataclass(frozen=True)
class SimulationResult:
    device: str
    label: str
    platform: str
    mode: str
    launch_state: str
    browser: str
    target: str
    screenshot: str | None
    emulation: dict[str, Any]
    facts: dict[str, Any]
    metrics: dict[str, Any]
    findings: list[dict[str, Any]]


DEFAULT_MAIN_UI_FLAGS: dict[str, str] = {
    "onboardingComplete": "true",
    "hasSeenOnboarding": "true",
    "seenOnboarding": "true",
    "onboarding_completed": "true",
    "pwaOnboardingComplete": "true",
    "tutorialComplete": "true",
    "introComplete": "true",
    "welcomeSeen": "true",
    "firstRunComplete": "true",
    "tourComplete": "true",
    "hasCompletedOnboarding": "true",
}


IOS_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)
IPAD_UA = (
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)
ANDROID_UA = (
    "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
)


DEVICE_PROFILES: dict[str, DeviceProfile] = {
    "iphone-se": DeviceProfile(
        key="iphone-se",
        label="iPhone SE sized PWA",
        platform="ios",
        preferred_browser="webkit",
        playwright_device="iPhone SE",
        viewport={"width": 375, "height": 667},
        screen={"width": 375, "height": 667},
        device_scale_factor=2,
        is_mobile=True,
        has_touch=True,
        user_agent=IOS_UA,
        safe_area_top=20,
        safe_area_bottom=0,
        notes="Small iPhone viewport; no home indicator safe-area bottom on older SE shape.",
    ),
    "iphone-12": DeviceProfile(
        key="iphone-12",
        label="iPhone 12/13 sized PWA",
        platform="ios",
        preferred_browser="webkit",
        playwright_device="iPhone 12",
        viewport={"width": 390, "height": 844},
        screen={"width": 390, "height": 844},
        device_scale_factor=3,
        is_mobile=True,
        has_touch=True,
        user_agent=IOS_UA,
        safe_area_top=47,
        safe_area_bottom=34,
        notes="Modern notched iPhone viewport with home indicator.",
    ),
    "iphone-14-pro": DeviceProfile(
        key="iphone-14-pro",
        label="iPhone 14 Pro sized PWA",
        platform="ios",
        preferred_browser="webkit",
        playwright_device="iPhone 14 Pro",
        viewport={"width": 393, "height": 852},
        screen={"width": 393, "height": 852},
        device_scale_factor=3,
        is_mobile=True,
        has_touch=True,
        user_agent=IOS_UA,
        safe_area_top=59,
        safe_area_bottom=34,
        notes="Dynamic Island class viewport; real status-bar placement still needs device proof.",
    ),
    "iphone-15-pro-max": DeviceProfile(
        key="iphone-15-pro-max",
        label="iPhone 15 Pro Max sized PWA",
        platform="ios",
        preferred_browser="webkit",
        playwright_device=None,
        viewport={"width": 430, "height": 932},
        screen={"width": 430, "height": 932},
        device_scale_factor=3,
        is_mobile=True,
        has_touch=True,
        user_agent=IOS_UA,
        safe_area_top=59,
        safe_area_bottom=34,
        notes="Large modern iPhone fallback descriptor.",
    ),
    "ipad-11": DeviceProfile(
        key="ipad-11",
        label="iPad 11-inch portrait PWA",
        platform="ios",
        preferred_browser="webkit",
        playwright_device="iPad Pro 11",
        viewport={"width": 834, "height": 1194},
        screen={"width": 834, "height": 1194},
        device_scale_factor=2,
        is_mobile=True,
        has_touch=True,
        user_agent=IPAD_UA,
        safe_area_top=24,
        safe_area_bottom=20,
        notes="Tablet-class Home Screen app approximation.",
    ),
    "pixel-7": DeviceProfile(
        key="pixel-7",
        label="Pixel 7 installed PWA",
        platform="android",
        preferred_browser="chromium",
        playwright_device="Pixel 7",
        viewport={"width": 412, "height": 915},
        screen={"width": 412, "height": 915},
        device_scale_factor=2.625,
        is_mobile=True,
        has_touch=True,
        user_agent=ANDROID_UA,
        safe_area_top=24,
        safe_area_bottom=24,
        notes="Android gesture navigation class viewport.",
    ),
    "galaxy-s23": DeviceProfile(
        key="galaxy-s23",
        label="Galaxy S23 sized installed PWA",
        platform="android",
        preferred_browser="chromium",
        playwright_device=None,
        viewport={"width": 360, "height": 780},
        screen={"width": 360, "height": 780},
        device_scale_factor=3,
        is_mobile=True,
        has_touch=True,
        user_agent=ANDROID_UA,
        safe_area_top=24,
        safe_area_bottom=24,
        notes="Narrow Android fallback descriptor.",
    ),
}

DEVICE_GROUPS: dict[str, list[str]] = {
    "ios-core": ["iphone-se", "iphone-12", "iphone-14-pro", "iphone-15-pro-max", "ipad-11"],
    "android-core": ["pixel-7", "galaxy-s23"],
    "phones": ["iphone-se", "iphone-12", "iphone-14-pro", "iphone-15-pro-max", "pixel-7", "galaxy-s23"],
    "all": list(DEVICE_PROFILES.keys()),
}


STANDALONE_INIT_SCRIPT = r"""
mode => {
  const requestedMode = String(mode || 'browser');
  const displayModes = new Set(['browser', 'standalone', 'fullscreen', 'minimal-ui', 'window-controls-overlay']);
  try {
    Object.defineProperty(window.navigator, 'standalone', {
      configurable: true,
      get: () => requestedMode === 'standalone' || requestedMode === 'fullscreen',
    });
  } catch (error) {}

  const realMatchMedia = window.matchMedia ? window.matchMedia.bind(window) : null;
  window.matchMedia = query => {
    const media = String(query || '');
    const normalized = media.toLowerCase().replace(/\s+/g, '');
    const displayModeMatch = normalized.match(/display-mode:([a-z-]+)/);
    if (displayModeMatch && displayModes.has(displayModeMatch[1])) {
      const matches = displayModeMatch[1] === requestedMode;
      return {
        matches,
        media,
        onchange: null,
        addListener: () => {},
        removeListener: () => {},
        addEventListener: () => {},
        removeEventListener: () => {},
        dispatchEvent: () => false,
      };
    }
    return realMatchMedia
      ? realMatchMedia(media)
      : {
          matches: false,
          media,
          onchange: null,
          addListener: () => {},
          removeListener: () => {},
          addEventListener: () => {},
          removeEventListener: () => {},
          dispatchEvent: () => false,
        };
  };
}
"""

INJECT_SAFE_AREA_SCRIPT = r"""
safeArea => {
  const top = `${safeArea.top || 0}px`;
  const bottom = `${safeArea.bottom || 0}px`;
  const style = document.createElement('style');
  style.setAttribute('data-pwa-device-sim', 'safe-area-vars');
  style.textContent = `
    html.pwa-sim-safe-area {
      --pwa-sim-safe-area-top: ${top};
      --pwa-sim-safe-area-bottom: ${bottom};
      --safe-area-top: ${top} !important;
      --safe-area-bottom: ${bottom} !important;
      --safe-top: ${top} !important;
      --safe-bottom: ${bottom} !important;
      --sat: ${top} !important;
      --sab: ${bottom} !important;
      --app-safe-area-top: ${top} !important;
      --app-safe-area-bottom: ${bottom} !important;
      --shell-safe-area-top: ${top} !important;
      --shell-safe-area-bottom: ${bottom} !important;
    }
  `;
  document.documentElement.classList.add('pwa-sim-safe-area');
  document.head.appendChild(style);
  return { top, bottom };
}
"""

ACTIVATE_DISPLAY_MODE_CSS_SCRIPT = r"""
mode => {
  const requestedMode = String(mode || 'browser').toLowerCase();
  const style = document.createElement('style');
  style.setAttribute('data-pwa-device-sim', `display-mode-${requestedMode}`);
  const cloned = [];
  const inaccessible = [];

  function wanted(mediaText) {
    const media = String(mediaText || '').toLowerCase();
    if (!media.includes('display-mode')) return false;
    return media.includes(`display-mode: ${requestedMode}`) ||
      media.includes(`display-mode:${requestedMode}`);
  }

  function walk(ruleList) {
    for (const rule of Array.from(ruleList || [])) {
      if (rule.cssRules && rule.media && wanted(rule.media.mediaText)) {
        for (const inner of Array.from(rule.cssRules)) {
          cloned.push(inner.cssText);
        }
      } else if (rule.cssRules && !rule.media) {
        walk(rule.cssRules);
      }
    }
  }

  for (const sheet of Array.from(document.styleSheets)) {
    try {
      walk(sheet.cssRules);
    } catch (error) {
      inaccessible.push(sheet.href || 'inline stylesheet');
    }
  }

  if (cloned.length) {
    style.textContent = cloned.join('\n');
    document.head.appendChild(style);
  }
  return { clonedRules: cloned.length, inaccessibleSheets: inaccessible };
}
"""

FACTS_SCRIPT = r"""
async mode => {
  const doc = document.documentElement;
  const viewportMeta = document.querySelector('meta[name="viewport"]');
  const manifestLink = document.querySelector('link[rel~="manifest"]');
  const sentinel = document.createElement('div');
  sentinel.style.cssText = [
    'position: fixed',
    'inset: auto auto 0 0',
    'width: 1px',
    'height: 1px',
    'pointer-events: none',
    'visibility: hidden',
    'padding-top: env(safe-area-inset-top)',
    'padding-right: env(safe-area-inset-right)',
    'padding-bottom: env(safe-area-inset-bottom)',
    'padding-left: env(safe-area-inset-left)'
  ].join(';');
  document.body.appendChild(sentinel);
  const safeStyle = getComputedStyle(sentinel);
  const safeAreaEnv = {
    top: safeStyle.paddingTop,
    right: safeStyle.paddingRight,
    bottom: safeStyle.paddingBottom,
    left: safeStyle.paddingLeft,
  };
  sentinel.remove();

  let manifest = null;
  let manifestError = null;
  if (manifestLink && manifestLink.href) {
    try {
      const response = await fetch(manifestLink.href, { cache: 'no-store' });
      manifest = await response.json();
    } catch (error) {
      manifestError = String(error && error.message ? error.message : error);
    }
  }

  return {
    requestedMode: mode,
    url: location.href,
    title: document.title,
    htmlClassList: Array.from(doc.classList),
    viewportMeta: viewportMeta ? viewportMeta.getAttribute('content') : null,
    appleMobileWebAppCapable: document.querySelector('meta[name="apple-mobile-web-app-capable"]')?.getAttribute('content') || null,
    appleStatusBarStyle: document.querySelector('meta[name="apple-mobile-web-app-status-bar-style"]')?.getAttribute('content') || null,
    themeColor: document.querySelector('meta[name="theme-color"]')?.getAttribute('content') || null,
    navigatorStandalone: Boolean(window.navigator.standalone),
    displayModeMatches: {
      browser: matchMedia('(display-mode: browser)').matches,
      standalone: matchMedia('(display-mode: standalone)').matches,
      fullscreen: matchMedia('(display-mode: fullscreen)').matches,
      minimalUi: matchMedia('(display-mode: minimal-ui)').matches,
    },
    safeAreaEnv,
    manifestLink: manifestLink ? manifestLink.href : null,
    manifest,
    manifestError,
    visualViewport: window.visualViewport ? {
      width: window.visualViewport.width,
      height: window.visualViewport.height,
      offsetTop: window.visualViewport.offsetTop,
      offsetLeft: window.visualViewport.offsetLeft,
      scale: window.visualViewport.scale,
    } : null,
  };
}
"""

APP_SETTLE_FACTS_SCRIPT = r"""
selector => {
  const selectors = String(selector || 'main,[role="main"],#root,#__next,[data-app],[data-testid="app"]').split(',').map(item => item.trim()).filter(Boolean);
  const loadingSelectors = [
    '[aria-busy="true"]',
    '[role="progressbar"]',
    '[data-loading="true"]',
    '[class*="loading" i]',
    '[class*="spinner" i]',
    '[class*="skeleton" i]',
    '[class*="shimmer" i]'
  ].join(',');

  function visible(el) {
    if (!el || !el.getBoundingClientRect) return false;
    const style = getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return style.display !== 'none' && style.visibility !== 'hidden' && Number(style.opacity || '1') > 0.01 && rect.width > 1 && rect.height > 1;
  }

  const candidates = selectors.flatMap(item => Array.from(document.querySelectorAll(item))).filter(visible);
  const mainText = candidates.map(el => (el.innerText || el.textContent || '').trim()).join(' ').replace(/\s+/g, ' ');
  const bodyText = (document.body?.innerText || document.body?.textContent || '').trim().replace(/\s+/g, ' ');
  const loading = Array.from(document.querySelectorAll(loadingSelectors)).filter(visible);
  const blockingWords = /\b(loading|please wait|initializing|starting|fetching|synchronizing|syncing)\b/i;
  const loadingTextMatches = blockingWords.test(bodyText.slice(0, 800));

  return {
    readyState: document.readyState,
    url: location.href,
    title: document.title,
    mainSelector: selectors.join(','),
    mainCandidateCount: candidates.length,
    mainTextLength: mainText.length,
    bodyTextLength: bodyText.length,
    loadingCount: loading.length,
    loadingTextMatches,
    settled: document.readyState === 'complete' && bodyText.length > 0 && loading.length === 0 && !loadingTextMatches,
  };
}
"""

BLOCKER_FACTS_SCRIPT = r"""
() => {
  const viewport = {
    width: window.visualViewport ? window.visualViewport.width : document.documentElement.clientWidth || window.innerWidth,
    height: window.visualViewport ? window.visualViewport.height : document.documentElement.clientHeight || window.innerHeight,
  };
  const viewportArea = Math.max(1, viewport.width * viewport.height);
  const onboardingWords = /\b(onboard|welcome|intro|tutorial|tour|walkthrough|get started|getting started|setup|first run|new here|add to home screen)\b/i;
  const blockerWords = /\b(skip|not now|maybe later|continue|next|done|get started|close|dismiss|accept|agree)\b/i;

  function visible(el) {
    if (!el || !el.getBoundingClientRect) return false;
    const style = getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return style.display !== 'none' && style.visibility !== 'hidden' && Number(style.opacity || '1') > 0.01 && rect.width > 2 && rect.height > 2;
  }

  function textFor(el) {
    return (el.innerText || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 180);
  }

  const candidates = [];
  for (const el of Array.from(document.querySelectorAll('body *')).filter(visible)) {
    const rect = el.getBoundingClientRect();
    const style = getComputedStyle(el);
    const text = textFor(el);
    const attrs = [
      el.id || '',
      typeof el.className === 'string' ? el.className : '',
      el.getAttribute('role') || '',
      el.getAttribute('aria-label') || '',
      el.getAttribute('data-testid') || '',
      el.getAttribute('data-test') || '',
      el.getAttribute('data-onboarding') || '',
    ].join(' ');
    const attrLooksOnboarding = onboardingWords.test(attrs);
    const textLooksOnboarding = onboardingWords.test(text);
    const dialogLike = el.matches('dialog[open],[role="dialog"],[role="alertdialog"],[aria-modal="true"]');
    const fixedLike = ['fixed', 'sticky', 'absolute'].includes(style.position);
    const large = (rect.width * rect.height) / viewportArea > 0.28;
    const coversCenter = rect.left < viewport.width * 0.35 && rect.right > viewport.width * 0.65 && rect.top < viewport.height * 0.55 && rect.bottom > viewport.height * 0.45;
    const hasDismissAction = blockerWords.test(text);
    if (dialogLike || ((fixedLike || attrLooksOnboarding || textLooksOnboarding) && large && coversCenter)) {
      candidates.push({
        selector: `${el.tagName.toLowerCase()}${el.id ? '#' + el.id : ''}`,
        role: el.getAttribute('role'),
        ariaModal: el.getAttribute('aria-modal'),
        position: style.position,
        zIndex: style.zIndex,
        rect: {
          x: Math.round(rect.x),
          y: Math.round(rect.y),
          width: Math.round(rect.width),
          height: Math.round(rect.height),
          top: Math.round(rect.top),
          bottom: Math.round(rect.bottom),
        },
        text,
        attrLooksOnboarding,
        textLooksOnboarding,
        hasDismissAction,
      });
    }
  }

  return {
    blockingOverlayCount: candidates.length,
    onboardingLikely: candidates.some(item => item.attrLooksOnboarding || item.textLooksOnboarding || item.hasDismissAction),
    examples: candidates.slice(0, 10),
  };
}
"""

SEED_MAIN_UI_SCRIPT = r"""
flags => {
  const entries = Object.entries(flags || {});
  for (const [key, value] of entries) {
    try { window.localStorage.setItem(key, String(value)); } catch (error) {}
    try { window.sessionStorage.setItem(key, String(value)); } catch (error) {}
  }
}
"""

DISMISS_ONBOARDING_SCRIPT = r"""
extraSelectors => {
  const selectors = [
    '[data-testid*="skip" i]',
    '[data-testid*="dismiss" i]',
    '[data-testid*="close" i]',
    '[data-testid*="continue" i]',
    '[aria-label*="skip" i]',
    '[aria-label*="dismiss" i]',
    '[aria-label*="close" i]',
    '[aria-label*="continue" i]',
    'button',
    '[role="button"]',
    'a'
  ].concat(extraSelectors || []);
  const textPattern = /\b(skip|not now|maybe later|dismiss|close|got it|done|continue|get started|start|next|accept|agree)\b|^[x×]$/i;

  function visible(el) {
    if (!el || !el.getBoundingClientRect) return false;
    const style = getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return style.display !== 'none' && style.visibility !== 'hidden' && Number(style.opacity || '1') > 0.01 && rect.width > 2 && rect.height > 2;
  }

  function labelFor(el) {
    return [
      el.getAttribute('aria-label') || '',
      el.getAttribute('title') || '',
      el.getAttribute('data-testid') || '',
      el.innerText || el.textContent || ''
    ].join(' ').trim().replace(/\s+/g, ' ');
  }

  const seen = new Set();
  const elements = [];
  for (const selector of selectors) {
    try {
      for (const el of Array.from(document.querySelectorAll(selector))) {
        if (!seen.has(el) && visible(el)) {
          seen.add(el);
          elements.push(el);
        }
      }
    } catch (error) {}
  }
  for (const el of elements) {
    const label = labelFor(el);
    if (!textPattern.test(label)) continue;
    try {
      el.click();
      return { clicked: true, label: label.slice(0, 120), tag: el.tagName.toLowerCase() };
    } catch (error) {
      return { clicked: false, label: label.slice(0, 120), error: String(error) };
    }
  }
  return { clicked: false };
}
"""


def resolve_devices(value: str) -> list[DeviceProfile]:
    keys: list[str] = []
    for raw in value.split(","):
        item = raw.strip()
        if not item:
            continue
        if item in DEVICE_GROUPS:
            keys.extend(DEVICE_GROUPS[item])
        elif item in DEVICE_PROFILES:
            keys.append(item)
        else:
            known = ", ".join(sorted(list(DEVICE_GROUPS) + list(DEVICE_PROFILES)))
            raise SystemExit(f"Unknown device/group '{item}'. Known values: {known}")
    deduped: list[DeviceProfile] = []
    seen: set[str] = set()
    for key in keys:
        if key not in seen:
            deduped.append(DEVICE_PROFILES[key])
            seen.add(key)
    return deduped


def resolve_modes(value: str) -> list[str]:
    modes = [item.strip().lower() for item in value.split(",") if item.strip()]
    allowed = {"browser", "standalone", "fullscreen", "minimal-ui"}
    unknown = [item for item in modes if item not in allowed]
    if unknown:
        raise SystemExit(f"Unknown mode(s): {', '.join(unknown)}")
    return modes or ["browser", "standalone"]


def resolve_launch_states(value: str) -> list[str]:
    aliases = {
        "auto": "auto",
        "first": "first-launch",
        "first-launch": "first-launch",
        "main": "main-ui",
        "main-ui": "main-ui",
    }
    states = [aliases.get(item.strip().lower(), item.strip().lower()) for item in value.split(",") if item.strip()]
    allowed = {"auto", "first-launch", "main-ui"}
    unknown = [item for item in states if item not in allowed]
    if unknown:
        raise SystemExit(f"Unknown launch state(s): {', '.join(unknown)}")
    if "auto" in states and len(states) > 1:
        raise SystemExit("--launch-states auto cannot be combined with explicit states.")
    return states or ["auto"]


def parse_storage_flags(values: list[str] | None) -> dict[str, str]:
    flags = dict(DEFAULT_MAIN_UI_FLAGS)
    for value in values or []:
        if "=" in value:
            key, flag_value = value.split("=", 1)
        else:
            key, flag_value = value, "true"
        key = key.strip()
        if key:
            flags[key] = flag_value.strip()
    return flags


def wait_for_app_settled(page: Any, args: argparse.Namespace) -> dict[str, Any]:
    try:
        page.wait_for_load_state("domcontentloaded", timeout=min(args.settle_timeout, 5000))
    except Exception:
        pass
    try:
        page.wait_for_load_state("load", timeout=min(args.settle_timeout, 8000))
    except Exception:
        pass
    if args.wait_for_network_idle:
        try:
            page.wait_for_load_state("networkidle", timeout=min(args.settle_timeout, 10000))
        except Exception:
            pass

    deadline = time.monotonic() + max(args.settle_timeout, 0) / 1000
    last_facts: dict[str, Any] = {}
    stable_hits = 0
    while True:
        last_facts = page.evaluate(APP_SETTLE_FACTS_SCRIPT, args.main_selector)
        enough_text = last_facts.get("bodyTextLength", 0) >= args.min_body_text
        main_ready = (
            last_facts.get("mainCandidateCount", 0) > 0
            and last_facts.get("mainTextLength", 0) >= args.min_main_text
        )
        no_loader = last_facts.get("loadingCount", 0) == 0 and not last_facts.get("loadingTextMatches")
        ready = last_facts.get("readyState") == "complete" and enough_text and no_loader
        if args.require_main_selector:
            ready = ready and main_ready
        if ready:
            stable_hits += 1
            if stable_hits >= 2:
                last_facts["settled"] = True
                last_facts["settleReason"] = "ready-state-content-and-loader-clear"
                return last_facts
        else:
            stable_hits = 0
        if time.monotonic() >= deadline:
            last_facts["settled"] = False
            last_facts["settleReason"] = "timeout"
            return last_facts
        page.wait_for_timeout(250)


def dismiss_onboarding(page: Any, args: argparse.Namespace) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    selectors = args.dismiss_selector or []
    for _ in range(args.dismiss_attempts):
        result = page.evaluate(DISMISS_ONBOARDING_SCRIPT, selectors)
        attempts.append(result)
        if not result.get("clicked"):
            break
        page.wait_for_timeout(args.dismiss_wait_ms)
    return attempts


def device_context_options(playwright: Any, profile: DeviceProfile) -> tuple[dict[str, Any], str]:
    if profile.playwright_device and profile.playwright_device in playwright.devices:
        options = dict(playwright.devices[profile.playwright_device])
        return options, f"playwright.devices[{profile.playwright_device!r}]"
    return (
        {
            "viewport": profile.viewport,
            "screen": profile.screen,
            "device_scale_factor": profile.device_scale_factor,
            "is_mobile": profile.is_mobile,
            "has_touch": profile.has_touch,
            "user_agent": profile.user_agent,
        },
        "built-in fallback descriptor",
    )


def launch_browser(playwright: Any, browser_name: str, headless: bool) -> Any:
    if browser_name == "webkit":
        return playwright.webkit.launch(headless=headless)
    if browser_name == "firefox":
        return playwright.firefox.launch(headless=headless)
    return playwright.chromium.launch(headless=headless)


def add_simulation_findings(
    profile: DeviceProfile,
    mode: str,
    launch_state: str,
    facts: dict[str, Any],
    emulation: dict[str, Any],
    settle_facts: dict[str, Any],
    blocker_facts: dict[str, Any],
    main_ui_will_be_probed: bool,
) -> list[SimulationFinding]:
    findings: list[SimulationFinding] = []

    if not settle_facts.get("settled"):
        findings.append(
            SimulationFinding(
                severity="warning",
                device=profile.key,
                mode=mode,
                rule="app-not-fully-settled-before-probe",
                message="The page did not meet settle conditions before screenshot/audit; loader or late content may have been captured.",
                evidence=settle_facts,
            )
        )

    if blocker_facts.get("blockingOverlayCount", 0) > 0:
        severity = "warning" if launch_state == "main-ui" else "info"
        message = (
            "Main-UI pass is still blocked by onboarding/modal UI."
            if launch_state == "main-ui"
            else "First-launch pass is blocked by onboarding/modal UI; a main-UI pass is required for full UI coverage."
        )
        if launch_state == "first-launch" and main_ui_will_be_probed:
            message = "First-launch pass is blocked by onboarding/modal UI; simulator will also probe main UI."
        findings.append(
            SimulationFinding(
                severity=severity,
                device=profile.key,
                mode=mode,
                rule="launch-ui-blocker-detected",
                message=message,
                evidence=blocker_facts,
            )
        )

    if mode != "browser" and not facts.get("displayModeMatches", {}).get(mode.replace("-", ""), False):
        # minimal-ui is represented as minimalUi in facts.
        matched = facts.get("displayModeMatches", {}).get("minimalUi") if mode == "minimal-ui" else None
        if not matched:
            findings.append(
                SimulationFinding(
                    severity="warning",
                    device=profile.key,
                    mode=mode,
                    rule="display-mode-signal-not-active",
                    message="The requested display-mode did not appear active in JS matchMedia facts.",
                    evidence={"requestedMode": mode, "displayModeMatches": facts.get("displayModeMatches")},
                )
            )

    if profile.platform == "ios" and mode in {"standalone", "fullscreen"}:
        capable = (facts.get("appleMobileWebAppCapable") or "").lower()
        if capable != "yes":
            findings.append(
                SimulationFinding(
                    severity="warning",
                    device=profile.key,
                    mode=mode,
                    rule="ios-standalone-meta-missing-runtime",
                    message="iOS standalone simulation found no apple-mobile-web-app-capable=yes meta tag.",
                    evidence={"appleMobileWebAppCapable": facts.get("appleMobileWebAppCapable")},
                )
            )
        manifest = facts.get("manifest") if isinstance(facts.get("manifest"), dict) else None
        if manifest is None and facts.get("manifestLink"):
            findings.append(
                SimulationFinding(
                    severity="info",
                    device=profile.key,
                    mode=mode,
                    rule="manifest-runtime-fetch-unverified",
                    message="Manifest was linked but could not be read at runtime; static manifest inspection must cover display metadata.",
                    evidence={"manifestLink": facts.get("manifestLink"), "manifestError": facts.get("manifestError")},
                )
            )
        display = manifest.get("display") if manifest else None
        override = manifest.get("display_override") if manifest else None
        values = {display} if isinstance(display, str) else set()
        if isinstance(override, list):
            values.update(item for item in override if isinstance(item, str))
        if manifest is not None and not values.intersection({"standalone", "fullscreen"}):
            findings.append(
                SimulationFinding(
                    severity="warning",
                    device=profile.key,
                    mode=mode,
                    rule="manifest-display-not-standalone-runtime",
                    message="Manifest display metadata does not request standalone/fullscreen.",
                    evidence={"display": display, "display_override": override},
                )
            )
        findings.append(
            SimulationFinding(
                severity="info",
                device=profile.key,
                mode=mode,
                rule="ios-webapp-process-not-emulated",
                message="Playwright WebKit is not the real iOS Home Screen Web.app process; real device install remains required.",
                evidence={"profile": profile.key, "browser": emulation.get("browser")},
            )
        )

    expected_bottom = profile.safe_area_bottom
    actual_bottom = facts.get("safeAreaEnv", {}).get("bottom")
    if mode != "browser" and expected_bottom and actual_bottom in {"0px", "0"}:
        findings.append(
            SimulationFinding(
                severity="info",
                device=profile.key,
                mode=mode,
                rule="safe-area-env-not-emulated",
                message="Playwright did not expose a non-zero CSS env(safe-area-inset-bottom); injected common safe-area CSS variables are only an approximation.",
                evidence={"expectedBottomPx": expected_bottom, "computedEnvBottom": actual_bottom},
            )
        )

    css_clone = emulation.get("displayModeCssClone", {})
    if mode != "browser" and css_clone.get("inaccessibleSheets"):
        findings.append(
            SimulationFinding(
                severity="info",
                device=profile.key,
                mode=mode,
                rule="display-mode-css-clone-incomplete",
                message="Some stylesheets could not be inspected for display-mode media rules.",
                evidence={"inaccessibleSheets": css_clone.get("inaccessibleSheets")},
            )
        )

    return findings


def run_simulation(args: argparse.Namespace) -> dict[str, Any]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as error:
        return {
            "ok": False,
            "error": "Python Playwright is not installed.",
            "detail": str(error),
            "install_hint": "Install with: python -m pip install playwright && python -m playwright install chromium webkit",
        }

    target = normalize_target(args.target)
    devices = resolve_devices(args.devices)
    modes = resolve_modes(args.modes)
    launch_state_request = resolve_launch_states(args.launch_states)
    storage_flags = parse_storage_flags(args.storage_flag)
    audit_dir = Path(args.audit_dir).resolve() if args.audit_dir else None
    if audit_dir:
        (audit_dir / "screenshots").mkdir(parents=True, exist_ok=True)
        (audit_dir / "reports").mkdir(parents=True, exist_ok=True)
        (audit_dir / "logs").mkdir(parents=True, exist_ok=True)
    if audit_dir and args.screenshots_dir:
        screenshot_dir = (audit_dir / args.screenshots_dir).resolve()
    elif audit_dir:
        screenshot_dir = (audit_dir / "screenshots").resolve()
    else:
        screenshot_dir = Path(args.screenshots_dir).resolve() if args.screenshots_dir else None
    if screenshot_dir:
        screenshot_dir.mkdir(parents=True, exist_ok=True)

    results: list[SimulationResult] = []
    errors: list[dict[str, Any]] = []

    with sync_playwright() as playwright:
        for profile in devices:
            browser_name = profile.preferred_browser if args.browser == "auto" else args.browser
            if args.browser == "auto" and profile.platform == "ios":
                browser_name = "webkit"
            elif args.browser == "auto" and profile.platform == "android":
                browser_name = "chromium"
            try:
                browser = launch_browser(playwright, browser_name, headless=not args.headed)
            except Exception as error:
                errors.append(
                    {
                        "device": profile.key,
                        "browser": browser_name,
                        "error": str(error),
                        "install_hint": f"Run: python -m playwright install {browser_name}",
                    }
                )
                continue
            try:
                context_options, descriptor_source = device_context_options(playwright, profile)
                context_options.update(
                    {
                        "color_scheme": args.color_scheme,
                        "reduced_motion": args.reduced_motion,
                        "locale": args.locale,
                        "timezone_id": args.timezone,
                    }
                )
                if args.permissions:
                    context_options["permissions"] = [item.strip() for item in args.permissions.split(",") if item.strip()]
                for mode in modes:
                    states = ["first-launch"] if launch_state_request == ["auto"] else list(launch_state_request)
                    state_index = 0
                    while state_index < len(states):
                        launch_state = states[state_index]
                        context = browser.new_context(**context_options)
                        if mode != "browser" or args.force_display_mode_js:
                            context.add_init_script(f"({STANDALONE_INIT_SCRIPT})({json.dumps(mode)});")
                        if launch_state == "main-ui":
                            context.add_init_script(f"({SEED_MAIN_UI_SCRIPT})({json.dumps(storage_flags)});")
                        page = context.new_page()
                        try:
                            page.goto(target, wait_until=args.wait_until, timeout=args.timeout)
                            if args.wait_ms:
                                page.wait_for_timeout(args.wait_ms)
                            classes = ["pwa-sim", f"pwa-sim-{mode}", f"display-mode-{mode}", f"launch-state-{launch_state}"]
                            if mode in {"standalone", "fullscreen"}:
                                classes.extend(["pwa-standalone", "is-standalone", "standalone"])
                            if launch_state == "main-ui":
                                classes.extend(["pwa-main-ui", "onboarding-complete"])
                            page.evaluate("classes => document.documentElement.classList.add(...classes)", classes)
                            safe_area_result = None
                            if args.inject_safe_area_vars and mode != "browser":
                                safe_area_result = page.evaluate(
                                    INJECT_SAFE_AREA_SCRIPT,
                                    {"top": profile.safe_area_top, "bottom": profile.safe_area_bottom},
                                )
                            css_clone_result = {"clonedRules": 0, "inaccessibleSheets": []}
                            if args.activate_display_mode_css and mode != "browser":
                                css_clone_result = page.evaluate(ACTIVATE_DISPLAY_MODE_CSS_SCRIPT, mode)
                            if args.wait_ms_after_injection:
                                page.wait_for_timeout(args.wait_ms_after_injection)
                            settle_before_dismiss = wait_for_app_settled(page, args)
                            dismiss_attempts: list[dict[str, Any]] = []
                            if launch_state == "main-ui" and args.dismiss_onboarding:
                                dismiss_attempts = dismiss_onboarding(page, args)
                                if any(item.get("clicked") for item in dismiss_attempts):
                                    settle_before_dismiss = wait_for_app_settled(page, args)
                            blocker_facts = page.evaluate(BLOCKER_FACTS_SCRIPT)
                            first_launch_blocked = (
                                launch_state == "first-launch"
                                and blocker_facts.get("blockingOverlayCount", 0) > 0
                                and launch_state_request == ["auto"]
                            )
                            if first_launch_blocked and "main-ui" not in states:
                                states.append("main-ui")
                            facts = page.evaluate(FACTS_SCRIPT, mode)
                            audit = page.evaluate(AUDIT_SCRIPT)
                            screenshot_path = None
                            if screenshot_dir:
                                screenshot_path = str((screenshot_dir / f"{profile.key}-{mode}-{launch_state}.png").resolve())
                                page.screenshot(path=screenshot_path, full_page=True)
                            emulation = {
                                "descriptorSource": descriptor_source,
                                "browser": browser_name,
                                "playwrightDevice": profile.playwright_device,
                                "profile": asdict(profile),
                                "standaloneJsSignalsForced": mode != "browser" or args.force_display_mode_js,
                                "htmlClassesInjected": classes,
                                "safeAreaVarsInjected": safe_area_result,
                                "displayModeCssClone": css_clone_result,
                                "launchState": launch_state,
                                "launchStateRequest": args.launch_states,
                                "settleFacts": settle_before_dismiss,
                                "blockerFacts": blocker_facts,
                                "dismissAttempts": dismiss_attempts,
                                "mainUiStorageFlagsSeeded": storage_flags if launch_state == "main-ui" else {},
                                "limitations": [
                                    "CSS env(safe-area-inset-*) values are browser/platform controlled and may stay 0 in Playwright.",
                                    "Real iOS Home Screen Web.app process, status bar, install storage, and OS chrome are not fully emulated.",
                                    "Cloned display-mode CSS rules are best effort and cannot inspect cross-origin stylesheets blocked by CSSOM.",
                                    "Main-UI bypass uses common storage flags and visible dismiss buttons; app-specific onboarding gates may need --storage-flag or --dismiss-selector.",
                                ],
                            }
                            simulation_findings = [
                                asdict(item)
                                for item in add_simulation_findings(
                                    profile,
                                    mode,
                                    launch_state,
                                    facts,
                                    emulation,
                                    settle_before_dismiss,
                                    blocker_facts,
                                    first_launch_blocked,
                                )
                            ]
                            all_findings = audit["findings"] + simulation_findings
                            results.append(
                                SimulationResult(
                                    device=profile.key,
                                    label=profile.label,
                                    platform=profile.platform,
                                    mode=mode,
                                    launch_state=launch_state,
                                    browser=browser_name,
                                    target=page.url,
                                    screenshot=screenshot_path,
                                    emulation=emulation,
                                    facts=facts,
                                    metrics=audit["metrics"],
                                    findings=all_findings,
                                )
                            )
                        except Exception as error:
                            errors.append(
                                {
                                    "device": profile.key,
                                    "mode": mode,
                                    "launchState": launch_state,
                                    "browser": browser_name,
                                    "error": str(error),
                                }
                            )
                        finally:
                            context.close()
                        state_index += 1
            finally:
                browser.close()

    all_findings = [finding for result in results for finding in result.findings]
    summary = {
        "devices": len({result.device for result in results}),
        "runs": len(results),
        "errors": len(errors),
        "findings": len(all_findings),
        "critical": sum(1 for item in all_findings if item.get("severity") == "critical"),
        "warning": sum(1 for item in all_findings if item.get("severity") == "warning"),
        "info": sum(1 for item in all_findings if item.get("severity") == "info"),
    }
    return {
        "ok": not errors,
        "target": target,
        "artifactPaths": {
            "auditDir": str(audit_dir) if audit_dir else None,
            "screenshotsDir": str(screenshot_dir) if screenshot_dir else None,
        },
        "summary": summary,
        "results": [
            {
                **asdict(result),
            }
            for result in results
        ],
        "errors": errors,
    }


def print_text(report: dict[str, Any]) -> None:
    if not report.get("ok") and not report.get("results"):
        print(report.get("error", "PWA device simulation failed."))
        print(report.get("detail", ""))
        if report.get("install_hint"):
            print(report["install_hint"])
        for error in report.get("errors", []):
            print(f"- {error}")
        return

    summary = report["summary"]
    print("PWA device simulation")
    print(f"Target: {report['target']}")
    artifacts = report.get("artifactPaths", {})
    if artifacts.get("auditDir"):
        print(f"Audit dir: {artifacts['auditDir']}")
    if artifacts.get("jsonReport"):
        print(f"JSON report: {artifacts['jsonReport']}")
    print(
        f"Runs: {summary['runs']} | Devices: {summary['devices']} | Errors: {summary['errors']} | "
        f"Findings: {summary['findings']} "
        f"(critical {summary['critical']}, warning {summary['warning']}, info {summary['info']})"
    )
    for error in report.get("errors", []):
        print(f"ERROR {error.get('device')} {error.get('mode', '')} {error.get('browser')}: {error.get('error')}")
        if error.get("install_hint"):
            print(error["install_hint"])
    for result in report["results"]:
        counts = result["metrics"]["counts"]
        display = result["facts"]["displayModeMatches"]
        settle = result["emulation"].get("settleFacts", {})
        blocker = result["emulation"].get("blockerFacts", {})
        print()
        print(f"{result['device']} {result['mode']} {result['launch_state']} via {result['browser']}")
        if result["screenshot"]:
            print(f"Screenshot: {result['screenshot']}")
        print(
            f"displayMode={display} navigatorStandalone={result['facts']['navigatorStandalone']} "
            f"fixedBottom={counts['fixedBottom']} bottomOverlap={counts['bottomOverlapRisks']} "
            f"bottomClearance={counts['bottomClearanceRisks']} settled={settle.get('settled')} "
            f"loadingCount={settle.get('loadingCount')} blockers={blocker.get('blockingOverlayCount')}"
        )
        for finding in result["findings"][:20]:
            print(f"- [{finding['severity'].upper()}] {finding['rule']}: {finding['message']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="URL or local HTML file to simulate.")
    parser.add_argument("--devices", default="ios-core", help="Comma-separated device profiles/groups. Groups: ios-core, android-core, phones, all.")
    parser.add_argument("--modes", default="browser,standalone", help="Comma-separated modes: browser, standalone, fullscreen, minimal-ui.")
    parser.add_argument("--browser", choices=("auto", "chromium", "webkit", "firefox"), default="auto")
    parser.add_argument(
        "--audit-dir",
        help="Single root folder for all generated artifacts. Screenshots go under screenshots/ and JSON reports under reports/.",
    )
    parser.add_argument("--screenshots-dir", help="Directory for per-device/mode full-page screenshots.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--wait-until", default="networkidle", choices=("load", "domcontentloaded", "networkidle", "commit"))
    parser.add_argument("--wait-ms", type=int, default=0)
    parser.add_argument("--wait-ms-after-injection", type=int, default=100)
    parser.add_argument("--settle-timeout", type=int, default=15000, help="Milliseconds to wait for readyState, content, and loaders to settle before screenshots/audit.")
    parser.add_argument("--main-selector", default="main,[role=\"main\"],#root,#__next,[data-app],[data-testid=\"app\"]")
    parser.add_argument("--require-main-selector", action="store_true", help="Require visible main/root selector text before considering the page settled.")
    parser.add_argument("--min-main-text", type=int, default=20)
    parser.add_argument("--min-body-text", type=int, default=20)
    parser.add_argument("--no-wait-for-network-idle", dest="wait_for_network_idle", action="store_false")
    parser.add_argument("--launch-states", default="auto", help="auto, first, main, or comma-separated first,main. Auto runs main-ui when onboarding/modal blockers appear.")
    parser.add_argument("--storage-flag", action="append", help="Storage flag for main-ui state, KEY=VALUE. May be repeated.")
    parser.add_argument("--dismiss-selector", action="append", help="Extra selector to click while dismissing onboarding in main-ui state. May be repeated.")
    parser.add_argument("--dismiss-attempts", type=int, default=5)
    parser.add_argument("--dismiss-wait-ms", type=int, default=500)
    parser.add_argument("--no-dismiss-onboarding", dest="dismiss_onboarding", action="store_false")
    parser.add_argument("--timeout", type=int, default=30000)
    parser.add_argument("--headed", action="store_true", help="Run browsers headed for visual debugging.")
    parser.add_argument("--color-scheme", choices=("light", "dark", "no-preference"), default="light")
    parser.add_argument("--reduced-motion", choices=("reduce", "no-preference"), default="no-preference")
    parser.add_argument("--locale", default="en-GB")
    parser.add_argument("--timezone", default="Europe/London")
    parser.add_argument("--permissions", default="", help="Comma-separated Playwright permissions, e.g. notifications,geolocation.")
    parser.add_argument("--no-inject-safe-area-vars", dest="inject_safe_area_vars", action="store_false")
    parser.add_argument("--no-activate-display-mode-css", dest="activate_display_mode_css", action="store_false")
    parser.add_argument("--force-display-mode-js", action="store_true", help="Force matchMedia/navigator.standalone JS signals even in browser mode.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on critical, warning, or browser errors. Info-only output still exits zero.")
    parser.set_defaults(inject_safe_area_vars=True, activate_display_mode_css=True, wait_for_network_idle=True, dismiss_onboarding=True)
    args = parser.parse_args()
    if not args.audit_dir and not args.screenshots_dir:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        args.audit_dir = str(Path("web-layout-audit-runs") / f"pwa-device-simulation-{timestamp}")

    report = run_simulation(args)
    if args.audit_dir:
        report_path = Path(args.audit_dir).resolve() / "reports" / "pwa-device-simulation.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report.setdefault("artifactPaths", {})["jsonReport"] = str(report_path)
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print_text(report)
    if not report.get("ok") and args.strict:
        return 2
    summary = report.get("summary", {})
    if args.strict and (summary.get("critical") or summary.get("warning")):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

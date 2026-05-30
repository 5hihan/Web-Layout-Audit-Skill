#!/usr/bin/env python3
"""Suspicious static scanner for common responsive web and PWA defects.

This scanner reports two different classes of output:

- Findings: suspicious or broken code shapes found in the source.
- Evidence gaps: areas where the source did not prove that a required audit
  concern has been handled.

Evidence gaps are not automatic bugs, but they must stay open until a human or
agent verifies the behaviour through code inspection, browser tests, or devices.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse


TEXT_EXTENSIONS = {
    ".astro",
    ".css",
    ".html",
    ".htm",
    ".json",
    ".js",
    ".jsx",
    ".mjs",
    ".scss",
    ".svelte",
    ".ts",
    ".tsx",
    ".vue",
    ".webmanifest",
}

SKIP_DIRS = {
    ".git",
    ".hg",
    ".next",
    ".nuxt",
    ".svelte-kit",
    ".turbo",
    ".vercel",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "out",
}

BOTTOM_NAV_PATTERN = re.compile(
    r"(?:bottom[-_ ]?(?:nav|navigation|bar|tabs?|tab)|tab[-_ ]?bar|bottomnav|bottomtab|"
    r"bottomnavigation|bottomtabs|--tab-bar|--bottom-nav|--bottom-bar|home-indicator|"
    r"floatingcartbutton|cartdrawer|sticky[-_ ]?(?:cta|checkout))",
    re.I,
)

STANDALONE_PATTERN = re.compile(
    r"(?:display-mode|pwa-standalone|is-standalone|navigator\.standalone|"
    r"matchmedia\(\s*['\"]\(\s*display-mode\s*:\s*standalone\s*\))",
    re.I,
)

BOTTOM_CLEARANCE_PATTERN = re.compile(
    r"(?:safe-area-inset-bottom|--safe-area-bottom|--tab-bar|--bottom-nav|--bottom-bar|"
    r"--bottom-clearance|--app-bottom|--shell-bottom|scroll-padding-bottom|"
    r"padding-bottom\s*:\s*var\([^)]*(?:safe-area|tab-bar|bottom-nav|bottom-bar|clearance|reserved))",
    re.I,
)

BOTTOM_RESERVED_PATTERN = re.compile(
    r"(?:(?:--tab-bar|--bottom-nav|--bottom-bar|--app-bottom|--shell-bottom)[\w-]*"
    r"(?:reserved|clearance)|(?:reserved|clearance)[\w-]*(?:height|bottom)|"
    r"(?:scroll-padding-bottom|padding-bottom)\s*:\s*var\([^)]*(?:reserved|clearance|tab-bar|bottom-nav|bottom-bar))",
    re.I,
)

CSS_BLOCK_PATTERN = re.compile(r"(?P<selector>[^{}]{0,260})\{(?P<body>[^{}]{0,2600})\}", re.S)
VIEWPORT_FIT_COVER_PATTERN = re.compile(r"viewport-fit\s*=\s*cover", re.I)
APPLE_BLACK_TRANSLUCENT_PATTERN = re.compile(
    r"<meta\b(?=[^>]*apple-mobile-web-app-status-bar-style)(?=[^>]*black-translucent)[^>]*>",
    re.I | re.S,
)
ROOT_PERCENT_HEIGHT_PATTERN = re.compile(r"\b(?:height|min-height|block-size|min-block-size)\s*:\s*100%(?![\w-])", re.I)
ROOT_VH_HEIGHT_PATTERN = re.compile(r"\b(?:height|min-height|block-size|min-block-size)\s*:\s*100vh(?![\w-])", re.I)
AUTH_WEB_STORAGE_PATTERN = re.compile(
    r"(?:localStorage|sessionStorage)\s*(?:\.\s*(?:setItem|getItem|removeItem)\s*\(\s*['\"][^'\"]*"
    r"(?:auth|token|jwt|session|access|refresh)|\[\s*['\"][^'\"]*(?:auth|token|jwt|session|access|refresh))",
    re.I,
)
TARGET_BLANK_PATTERN = re.compile(r"<a\b(?=[^>]*\btarget\s*=\s*['\"]?_blank['\"]?)[^>]*>", re.I | re.S)
CAPTURE_INPUT_PATTERN = re.compile(r"<input\b(?=[^>]*\btype\s*=\s*['\"]?file['\"]?)(?=[^>]*\bcapture\b)[^>]*>", re.I | re.S)
EXTERNAL_LINK_PATTERN = re.compile(r"<a\b(?=[^>]*\bhref\s*=\s*['\"]https?://)[^>]*>", re.I | re.S)
NOTIFICATION_PERMISSION_PATTERN = re.compile(r"Notification\.requestPermission\s*\(", re.I)


@dataclass(frozen=True)
class Finding:
    severity: str
    rule: str
    path: str
    line: int
    message: str
    evidence: str
    reference: str


@dataclass(frozen=True)
class Summary:
    files_scanned: int
    findings: int
    critical: int
    warning: int
    info: int
    evidence_gap: int


@dataclass(frozen=True)
class ProjectEvidence:
    html_files: int
    style_files: int
    script_files: int
    component_files: int
    manifest_files: int
    service_worker_files: int
    service_worker_registrations: int
    media_query_usages: int
    container_query_usages: int
    safe_area_usages: int
    standalone_mode_usages: int
    manifest_link_usages: int
    theme_color_meta_usages: int
    apple_mobile_web_app_capable_usages: int
    apple_status_bar_meta_usages: int
    apple_black_translucent_usages: int
    viewport_fit_cover_usages: int
    root_percent_height_usages: int
    root_vh_height_usages: int
    auth_web_storage_usages: int
    apple_touch_icon_usages: int
    bottom_nav_usages: int
    bottom_nav_clearance_usages: int
    bottom_nav_reserved_height_usages: int
    fixed_bottom_block_usages: int
    service_worker_fetch_listeners: int
    service_worker_update_usages: int
    service_worker_cache_cleanup_usages: int
    skip_waiting_usages: int
    clients_claim_usages: int
    offline_fallback_usages: int
    beforeinstallprompt_usages: int
    appinstalled_usages: int
    ios_install_fallback_usages: int
    notification_permission_usages: int
    push_subscribe_usages: int
    push_event_usages: int
    notification_click_usages: int
    background_sync_usages: int
    online_fallback_usages: int
    storage_api_usages: int
    storage_persist_usages: int
    mutation_request_usages: int
    offline_queue_usages: int
    capture_input_usages: int
    media_capture_usages: int
    lifecycle_resume_usages: int
    history_api_usages: int
    popstate_usages: int
    external_link_usages: int
    target_blank_without_noopener_usages: int
    focus_visible_usages: int
    hover_usages: int
    reduced_motion_usages: int
    forced_colors_usages: int
    dark_mode_usages: int
    aria_usages: int
    semantic_landmark_usages: int
    image_tags: int
    responsive_image_usages: int
    ui_state_usages: int
    haptic_usages: int
    test_files: int


RULES: tuple[tuple[str, str, str, re.Pattern[str], str], ...] = (
    (
        "critical",
        "viewport-zoom-disabled",
        "Do not disable pinch zoom with user-scalable=no or maximum-scale restrictions.",
        re.compile(r"user-scalable\s*=\s*no|maximum-scale\s*=\s*1", re.I),
        "references/04-audit-checklist.md: Viewport meta",
    ),
    (
        "warning",
        "naked-100vh",
        "Avoid naked 100vh for app shells unless it is the documented iOS standalone black-translucent edge-to-edge fix; prove the viewport-unit intent.",
        re.compile(r"\b(?:height|min-height|max-height)\s*:\s*100vh\b", re.I),
        "references/04-audit-checklist.md: Viewport units",
    ),
    (
        "critical",
        "focus-outline-removed",
        "Do not remove focus outlines without a strong :focus-visible replacement.",
        re.compile(r"outline\s*:\s*(?:0|none)\b", re.I),
        "references/04-audit-checklist.md: Accessibility baseline",
    ),
    (
        "warning",
        "global-scroll-lock",
        "Global overflow hidden can break iOS scroll, modals, and keyboard paths; verify it is scoped.",
        re.compile(r"\b(?:html|body|#root|#__next)\b[^{]*{[^}]*overflow\s*:\s*hidden", re.I | re.S),
        "references/04-audit-checklist.md: Scroll root and pull-to-refresh",
    ),
    (
        "warning",
        "touch-action-none",
        "touch-action:none can block expected touch gestures; keep it narrowly scoped.",
        re.compile(r"touch-action\s*:\s*none\b", re.I),
        "references/04-audit-checklist.md: Touch targets and pointer media",
    ),
    (
        "warning",
        "selection-disabled",
        "Avoid broad text selection or callout disabling; scope it to controls that need it.",
        re.compile(r"(?:user-select|-webkit-user-select|-webkit-touch-callout)\s*:\s*none\b", re.I),
        "references/04-audit-checklist.md: Long-press, callout and selection",
    ),
    (
        "warning",
        "fixed-bottom-without-safe-area",
        "Fixed bottom UI must include safe-area inset handling and scroll end padding.",
        re.compile(r"(?:bottom|inset-block-end)\s*:\s*0\b", re.I),
        "references/04-audit-checklist.md: Fixed bottom UI",
    ),
    (
        "warning",
        "large-fixed-width",
        "Large fixed widths can overflow or look wrong on mobile devices; prove the responsive constraint.",
        re.compile(r"\b(?:width|min-width|max-width)\s*:\s*(?:[4-9]\d{2}|\d{4,})px\b", re.I),
        "references/04-audit-checklist.md: Form factors",
    ),
    (
        "warning",
        "horizontal-overflow-hidden",
        "overflow-x:hidden can hide layout defects instead of fixing them; inspect the overflowing owner.",
        re.compile(r"overflow-x\s*:\s*hidden\b", re.I),
        "references/06-failure-modes-matrices-references.md: Anti-patterns: remove on sight",
    ),
    (
        "warning",
        "nowrap-truncation",
        "white-space:nowrap can break narrow devices or hide text. Verify wrapping, truncation, and localisation.",
        re.compile(r"white-space\s*:\s*nowrap\b", re.I),
        "references/04-audit-checklist.md: Form factors",
    ),
    (
        "warning",
        "absolute-positioned-ui",
        "Absolute positioning in UI can detach elements from responsive flow. Verify overlap and stacking on target devices.",
        re.compile(r"position\s*:\s*absolute\b", re.I),
        "references/04-audit-checklist.md: Fixed, sticky and stacking contexts",
    ),
    (
        "info",
        "z-index-layering",
        "z-index usage found. Verify overlays, modals, fixed UI, and focus order do not fight on small screens.",
        re.compile(r"z-index\s*:\s*[-]?\d+", re.I),
        "references/04-audit-checklist.md: Fixed, sticky and stacking contexts",
    ),
    (
        "info",
        "reduced-motion-query",
        "Reduced motion branch found; verify animations and transitions respect it completely.",
        re.compile(r"prefers-reduced-motion", re.I),
        "references/03-native-app-conversion.md: Motion optimisation for all devices",
    ),
    (
        "warning",
        "service-worker-versioned-url-risk",
        "Avoid versioning the service worker script URL; stale cached HTML can keep registering the old worker.",
        re.compile(r"serviceWorker\.register\s*\(\s*['\"][^'\"]*(?:sw[-_.]?v?\d|service-worker[-_.]?v?\d|[a-f0-9]{8,}\.js)", re.I),
        "references/08-online-pwa-symptom-fix-catalog.md: Service worker update and stale shell",
    ),
)

EVIDENCE_RULES: tuple[tuple[str, str, str, str, str], ...] = (
    (
        "manifest_files",
        "manifest-evidence-missing",
        "No web app manifest file was found. PWA identity, scope, icons, and display mode are unverified.",
        "references/04-audit-checklist.md: PWA manifest",
        "warning",
    ),
    (
        "service_worker_files",
        "service-worker-file-evidence-missing",
        "No service worker file was found. Offline, update, cache, and force-refresh behaviour are unverified.",
        "references/04-audit-checklist.md: Service worker update flow",
        "warning",
    ),
    (
        "service_worker_registrations",
        "service-worker-registration-evidence-missing",
        "No service worker registration was found. Installed PWA update behaviour is unverified.",
        "references/05-code-patterns-library.md: Service worker template with versioning and update flow",
        "warning",
    ),
    (
        "safe_area_usages",
        "safe-area-evidence-missing",
        "No safe-area inset usage was found. Notch, home indicator, gesture area, and standalone layout are unverified.",
        "references/04-audit-checklist.md: Safe-area tokens",
        "warning",
    ),
    (
        "media_query_usages",
        "media-query-evidence-missing",
        "No media queries were found. Responsive layout adaptation across device widths is unverified.",
        "references/04-audit-checklist.md: Form factors",
        "warning",
    ),
    (
        "container_query_usages",
        "container-query-evidence-missing",
        "No container queries were found. Component-level adaptation is unverified; inspect whether breakpoints alone are enough.",
        "references/06-failure-modes-matrices-references.md: Media query vs container query",
        "info",
    ),
    (
        "focus_visible_usages",
        "focus-visible-evidence-missing",
        "No :focus-visible usage was found. Keyboard focus visibility is unverified.",
        "references/04-audit-checklist.md: Accessibility baseline",
        "warning",
    ),
    (
        "aria_usages",
        "accessibility-attribute-evidence-missing",
        "No ARIA usage was found. This may be fine for fully native semantic HTML, but custom component accessibility is unverified.",
        "references/04-audit-checklist.md: Accessibility baseline",
        "info",
    ),
    (
        "semantic_landmark_usages",
        "landmark-evidence-missing",
        "No obvious semantic landmarks were found. Page structure and navigation semantics are unverified.",
        "references/04-audit-checklist.md: Accessibility baseline",
        "info",
    ),
    (
        "ui_state_usages",
        "ui-state-evidence-missing",
        "No obvious loading, empty, error, disabled, or skeleton UI states were found. Real workflow state coverage is unverified.",
        "references/06-failure-modes-matrices-references.md: Common LLM anti-pattern catalogue",
        "info",
    ),
    (
        "reduced_motion_usages",
        "reduced-motion-evidence-missing",
        "No prefers-reduced-motion branch was found. Motion accessibility is unverified.",
        "references/03-native-app-conversion.md: Motion optimisation for all devices",
        "warning",
    ),
    (
        "forced_colors_usages",
        "forced-colors-evidence-missing",
        "No forced-colors branch was found. Windows high-contrast and forced-colour behaviour are unverified.",
        "references/04-audit-checklist.md: Theming and system integration",
        "info",
    ),
    (
        "haptic_usages",
        "haptic-evidence-missing",
        "No haptic or vibration usage was found. Mandatory button haptic coverage is unverified for native-feel/PWA work.",
        "references/03-native-app-conversion.md: Mandatory all-button haptic requirements",
        "info",
    ),
    (
        "test_files",
        "test-evidence-missing",
        "No obvious test files were found. Automated viewport, keyboard, PWA, or accessibility regression evidence is unverified.",
        "references/06-failure-modes-matrices-references.md: Device test matrix",
        "info",
    ),
)


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
            yield path


def looks_like_manifest(path: Path) -> bool:
    return path.name.lower() in {"manifest.json", "site.webmanifest", "manifest.webmanifest"} or path.suffix.lower() == ".webmanifest"


def looks_like_service_worker(path: Path) -> bool:
    name = path.name.lower()
    return (
        name in {"sw.js", "service-worker.js", "serviceworker.js"}
        or name.startswith("sw-")
        or "service-worker" in name
        or "serviceworker" in name
        or "workbox" in name
    )


def looks_like_test(path: Path) -> bool:
    folded = path.as_posix().casefold()
    return (
        ".test." in folded
        or ".spec." in folded
        or "/tests/" in folded
        or "/test/" in folded
        or "/e2e/" in folded
        or "playwright" in folded
        or "cypress" in folded
    )


def looks_like_component(path: Path) -> bool:
    return path.suffix.lower() in {".jsx", ".tsx", ".vue", ".svelte", ".astro"}


def line_number(content: str, index: int) -> int:
    return content.count("\n", 0, index) + 1


def evidence_line(content: str, index: int) -> str:
    start = content.rfind("\n", 0, index) + 1
    end = content.find("\n", index)
    if end == -1:
        end = len(content)
    return content[start:end].strip()[:220]


def has_nearby_safe_area(content: str, index: int) -> bool:
    window_start = max(0, index - 500)
    window_end = min(len(content), index + 500)
    window = content[window_start:window_end]
    return "env(safe-area-inset-bottom" in window or "constant(safe-area-inset-bottom" in window


def has_bottom_clearance_signal(content: str) -> bool:
    return bool(BOTTOM_CLEARANCE_PATTERN.search(content))


def has_standalone_signal(content: str) -> bool:
    return bool(STANDALONE_PATTERN.search(content))


def has_nearby_bottom_clearance(content: str, index: int) -> bool:
    window_start = max(0, index - 700)
    window_end = min(len(content), index + 700)
    return has_bottom_clearance_signal(content[window_start:window_end])


def has_nearby_standalone_signal(content: str, index: int) -> bool:
    window_start = max(0, index - 1200)
    window_end = min(len(content), index + 1200)
    return has_standalone_signal(content[window_start:window_end])


def css_block_has_fixed_bottom(body: str) -> bool:
    return bool(re.search(r"position\s*:\s*fixed\b", body, re.I)) and bool(
        re.search(r"(?:bottom|inset-block-end)\s*:", body, re.I)
    )


def css_block_is_root_or_shell(selector: str) -> bool:
    normalized = " ".join(selector.split()).casefold()
    return bool(re.search(r"(?:^|[,\s])(?:html|body|#root|#__next|#app|\.app|\.app-shell)(?:\b|[,\s])", normalized))


def css_block_has_root_percent_height(selector: str, body: str) -> bool:
    return css_block_is_root_or_shell(selector) and bool(ROOT_PERCENT_HEIGHT_PATTERN.search(body))


def css_block_has_root_vh_height(selector: str, body: str) -> bool:
    return css_block_is_root_or_shell(selector) and bool(ROOT_VH_HEIGHT_PATTERN.search(body))


def manifest_url_path(value: str) -> str:
    parsed = urlparse(value)
    path = parsed.path or "/"
    if not path.startswith("/"):
        path = "/" + path
    return path


def manifest_start_in_scope(start_url: str, scope: str) -> bool:
    start_path = manifest_url_path(start_url)
    scope_path = manifest_url_path(scope)
    if not scope_path.endswith("/"):
        scope_path += "/"
    return start_path == scope_path[:-1] or start_path.startswith(scope_path)


def manifest_icon_sizes(icon: dict[str, object]) -> set[str]:
    sizes = icon.get("sizes")
    if not isinstance(sizes, str):
        return set()
    return {item.strip().casefold() for item in sizes.split() if item.strip()}


def scan_manifest(path: Path, root: Path, content: str) -> list[Finding]:
    rel_path = path.relative_to(root).as_posix()
    findings: list[Finding] = []
    try:
        manifest = json.loads(content)
    except json.JSONDecodeError as error:
        return [
            Finding(
                severity="critical",
                rule="manifest-json-invalid",
                path=rel_path,
                line=error.lineno,
                message="Manifest JSON is invalid; installability and launch metadata are broken.",
                evidence=str(error),
                reference="references/08-online-pwa-symptom-fix-catalog.md: Manifest and install identity",
            )
        ]

    if not isinstance(manifest, dict):
        findings.append(
            Finding(
                severity="critical",
                rule="manifest-root-not-object",
                path=rel_path,
                line=1,
                message="Manifest root must be a JSON object.",
                evidence=type(manifest).__name__,
                reference="references/08-online-pwa-symptom-fix-catalog.md: Manifest and install identity",
            )
        )
        return findings

    if not (manifest.get("name") or manifest.get("short_name")):
        findings.append(
            Finding(
                severity="warning",
                rule="manifest-name-missing",
                path=rel_path,
                line=1,
                message="Manifest should include name or short_name for install identity.",
                evidence="name and short_name missing",
                reference="references/08-online-pwa-symptom-fix-catalog.md: Manifest and install identity",
            )
        )
    for key in ("id", "start_url", "scope"):
        if not manifest.get(key):
            findings.append(
                Finding(
                    severity="warning",
                    rule=f"manifest-{key.replace('_', '-')}-missing",
                    path=rel_path,
                    line=1,
                    message=f"Manifest should include {key} so install identity, launch URL, and navigation scope are explicit.",
                    evidence=f"{key} missing",
                    reference="references/08-online-pwa-symptom-fix-catalog.md: Manifest and install identity",
                )
            )
    if manifest.get("start_url") and manifest.get("scope") and not manifest_start_in_scope(
        str(manifest["start_url"]), str(manifest["scope"])
    ):
        findings.append(
            Finding(
                severity="critical",
                rule="manifest-start-url-out-of-scope",
                path=rel_path,
                line=1,
                message="Manifest start_url is not inside scope; launch and install checks can fail or leave app context.",
                evidence=f"start_url={manifest.get('start_url')!r}, scope={manifest.get('scope')!r}",
                reference="references/08-online-pwa-symptom-fix-catalog.md: Scope and external link handling",
            )
        )

    display = manifest.get("display")
    display_override = manifest.get("display_override")
    display_values = {display} if isinstance(display, str) else set()
    if isinstance(display_override, list):
        display_values.update(item for item in display_override if isinstance(item, str))
    if not display_values:
        findings.append(
            Finding(
                severity="warning",
                rule="manifest-display-missing",
                path=rel_path,
                line=1,
                message="Manifest should explicitly choose display/display_override so installed chrome is predictable.",
                evidence="display missing",
                reference="references/08-online-pwa-symptom-fix-catalog.md: Manifest and install identity",
            )
        )
    elif not any(item in {"standalone", "fullscreen", "minimal-ui", "window-controls-overlay"} for item in display_values):
        findings.append(
            Finding(
                severity="warning",
                rule="manifest-display-browser-only",
                path=rel_path,
                line=1,
                message="Manifest display values do not request an installed app-like mode.",
                evidence=f"display_values={sorted(display_values)}",
                reference="references/08-online-pwa-symptom-fix-catalog.md: Manifest and install identity",
            )
        )

    if not manifest.get("theme_color") or not manifest.get("background_color"):
        findings.append(
            Finding(
                severity="warning",
                rule="manifest-launch-colors-missing",
                path=rel_path,
                line=1,
                message="Manifest should include theme_color and background_color to reduce splash/status-bar flashes.",
                evidence=f"theme_color={manifest.get('theme_color')!r}, background_color={manifest.get('background_color')!r}",
                reference="references/08-online-pwa-symptom-fix-catalog.md: Splash, status bar, and launch flash",
            )
        )

    icons = manifest.get("icons")
    if not isinstance(icons, list) or not icons:
        findings.append(
            Finding(
                severity="warning",
                rule="manifest-icons-missing",
                path=rel_path,
                line=1,
                message="Manifest icons are missing; install prompt, launcher icon, splash icon, and maskable icon behaviour are unverified.",
                evidence="icons missing",
                reference="references/08-online-pwa-symptom-fix-catalog.md: Manifest and install identity",
            )
        )
    else:
        all_sizes: set[str] = set()
        has_maskable = False
        missing_src = 0
        for icon in icons:
            if not isinstance(icon, dict):
                continue
            if not icon.get("src"):
                missing_src += 1
            purpose = str(icon.get("purpose", "")).casefold()
            if "maskable" in purpose:
                has_maskable = True
            all_sizes.update(manifest_icon_sizes(icon))
        if missing_src:
            findings.append(
                Finding(
                    severity="critical",
                    rule="manifest-icon-src-missing",
                    path=rel_path,
                    line=1,
                    message="One or more manifest icons are missing src.",
                    evidence=f"missing_src_icons={missing_src}",
                    reference="references/08-online-pwa-symptom-fix-catalog.md: Manifest and install identity",
                )
            )
        if not has_maskable:
            findings.append(
                Finding(
                    severity="warning",
                    rule="manifest-maskable-icon-missing",
                    path=rel_path,
                    line=1,
                    message="No maskable icon was found; Android launcher icon cropping is unverified.",
                    evidence=f"sizes={sorted(all_sizes)}",
                    reference="references/08-online-pwa-symptom-fix-catalog.md: Manifest and install identity",
                )
            )
        if not ({"192x192", "512x512"} <= all_sizes):
            findings.append(
                Finding(
                    severity="warning",
                    rule="manifest-required-icon-sizes-unverified",
                    path=rel_path,
                    line=1,
                    message="Manifest does not show both 192x192 and 512x512 icon sizes.",
                    evidence=f"sizes={sorted(all_sizes)}",
                    reference="references/08-online-pwa-symptom-fix-catalog.md: Manifest and install identity",
                )
            )

    if manifest.get("prefer_related_applications") is True:
        findings.append(
            Finding(
                severity="warning",
                rule="manifest-prefer-related-applications-risk",
                path=rel_path,
                line=1,
                message="prefer_related_applications=true can steer users away from PWA install; verify this is intentional.",
                evidence="prefer_related_applications=true",
                reference="references/08-online-pwa-symptom-fix-catalog.md: Install prompt missing",
            )
        )

    if manifest.get("share_target") and not manifest.get("id"):
        findings.append(
            Finding(
                severity="warning",
                rule="manifest-share-target-without-id",
                path=rel_path,
                line=1,
                message="share_target exists but manifest id is missing; installed identity and share routing are unverified.",
                evidence="share_target present, id missing",
                reference="references/08-online-pwa-symptom-fix-catalog.md: Share target and file handling",
            )
        )

    return findings


def scan_file(path: Path, root: Path) -> list[Finding]:
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = path.read_text(encoding="utf-8", errors="replace")

    findings: list[Finding] = []
    rel_path = path.relative_to(root).as_posix()

    if looks_like_manifest(path):
        findings.extend(scan_manifest(path, root, content))

    for severity, rule, message, pattern, reference in RULES:
        for match in pattern.finditer(content):
            evidence = evidence_line(content, match.start())
            if rule == "large-fixed-width" and ("@media" in evidence or "@container" in evidence):
                continue
            if rule == "fixed-bottom-without-safe-area" and has_nearby_safe_area(content, match.start()):
                continue
            if rule == "fixed-bottom-without-safe-area" and has_nearby_bottom_clearance(content, match.start()):
                continue
            if rule == "focus-outline-removed":
                nearby = content[max(0, match.start() - 300) : min(len(content), match.start() + 300)]
                if ":focus-visible" in nearby:
                    continue
            findings.append(
                Finding(
                    severity=severity,
                    rule=rule,
                    path=rel_path,
                    line=line_number(content, match.start()),
                    message=message,
                    evidence=evidence,
                    reference=reference,
                )
            )

    for block_match in CSS_BLOCK_PATTERN.finditer(content):
        block_body = block_match.group("body")
        if not css_block_has_fixed_bottom(block_body):
            continue
        block = block_match.group(0)
        if has_bottom_clearance_signal(block) and has_standalone_signal(content):
            continue
        if has_bottom_clearance_signal(block) and has_nearby_standalone_signal(content, block_match.start()):
            continue
        selector = " ".join(block_match.group("selector").split())[-120:]
        findings.append(
            Finding(
                severity="warning",
                rule="fixed-bottom-display-mode-clearance-unverified",
                path=rel_path,
                line=line_number(content, block_match.start("body")),
                message="Fixed bottom UI block does not show both shared bottom clearance and standalone/display-mode handling nearby.",
                evidence=(selector + " { " + evidence_line(content, block_match.start("body"))).strip()[:220],
                reference="references/07-bottom-nav-pwa-safe-area.md: Static Scanner Leads",
            )
        )

    for permission_match in NOTIFICATION_PERMISSION_PATTERN.finditer(content):
        nearby = content[max(0, permission_match.start() - 500) : min(len(content), permission_match.start() + 250)]
        if not re.search(r"(?:click|pointerup|touchend|submit|gesture|userActivation|user activation)", nearby, re.I):
            findings.append(
                Finding(
                    severity="warning",
                    rule="notification-permission-without-user-gesture-evidence",
                    path=rel_path,
                    line=line_number(content, permission_match.start()),
                    message="Notification permission appears to be requested without nearby user-gesture evidence.",
                    evidence=evidence_line(content, permission_match.start()),
                    reference="references/08-online-pwa-symptom-fix-catalog.md: Push notifications",
                )
            )
    for input_match in CAPTURE_INPUT_PATTERN.finditer(content):
        findings.append(
            Finding(
                severity="warning",
                rule="ios-standalone-file-capture-risk",
                path=rel_path,
                line=line_number(content, input_match.start()),
                message="File input capture needs real iOS standalone background/foreground testing; public reports show camera preview regressions.",
                evidence=input_match.group(0)[:220],
                reference="references/08-online-pwa-symptom-fix-catalog.md: Camera, file capture, and media resume",
            )
        )

    if path.suffix.lower() in {".html", ".htm"}:
        viewport_count = len(re.findall(r"<meta[^>]+name=[\"']viewport[\"']", content, re.I))
        if viewport_count == 0:
            findings.append(
                Finding(
                    severity="critical",
                    rule="viewport-meta-missing",
                    path=rel_path,
                    line=1,
                    message="Missing viewport meta tag.",
                    evidence="No <meta name=\"viewport\"> found.",
                    reference="references/04-audit-checklist.md: Viewport meta",
                )
            )
        elif viewport_count > 1:
            findings.append(
                Finding(
                    severity="warning",
                    rule="viewport-meta-multiple",
                    path=rel_path,
                    line=1,
                    message="Multiple viewport meta tags found; browsers can apply unexpected precedence.",
                    evidence=f"{viewport_count} viewport meta tags found.",
                    reference="references/04-audit-checklist.md: Viewport meta",
                )
            )
        viewport_match = re.search(r"<meta[^>]+name=[\"']viewport[\"'][^>]*>", content, re.I)
        if viewport_match and "viewport-fit=cover" not in viewport_match.group(0):
            findings.append(
                Finding(
                    severity="warning",
                    rule="viewport-fit-cover-missing",
                    path=rel_path,
                    line=line_number(content, viewport_match.start()),
                    message="Viewport meta should make an explicit viewport-fit=cover decision for safe areas.",
                    evidence=viewport_match.group(0)[:220],
                    reference="references/04-audit-checklist.md: Viewport meta",
                )
            )
        if viewport_match and VIEWPORT_FIT_COVER_PATTERN.search(viewport_match.group(0)) and APPLE_BLACK_TRANSLUCENT_PATTERN.search(content):
            findings.append(
                Finding(
                    severity="warning",
                    rule="ios-black-translucent-edge-to-edge-audit-required",
                    path=rel_path,
                    line=line_number(content, viewport_match.start()),
                    message=(
                        "iOS viewport-fit=cover and black-translucent status bar are both present; "
                        "prove the root/full-screen shell uses 100vh, not 100%, and that installed iOS cold launch has no chin gap."
                    ),
                    evidence=viewport_match.group(0)[:220],
                    reference="references/08-online-pwa-symptom-fix-catalog.md: iOS standalone chrome and safe areas",
                )
            )
        for img_match in re.finditer(r"<img\b[^>]*>", content, re.I):
            tag = img_match.group(0)
            folded_tag = tag.casefold()
            if not re.search(r"\balt\s*=", tag, re.I):
                findings.append(
                    Finding(
                        severity="warning",
                        rule="img-alt-missing",
                        path=rel_path,
                        line=line_number(content, img_match.start()),
                        message="Image is missing alt text. Verify whether it is informative or intentionally decorative.",
                        evidence=tag[:220],
                        reference="references/04-audit-checklist.md: Accessibility baseline",
                    )
                )
            if "width=" not in folded_tag or "height=" not in folded_tag:
                findings.append(
                    Finding(
                        severity="warning",
                        rule="img-dimensions-missing",
                        path=rel_path,
                        line=line_number(content, img_match.start()),
                        message="Image is missing width or height attributes. CLS and device layout stability are unverified.",
                        evidence=tag[:220],
                        reference="references/04-audit-checklist.md: Images, fonts and Core Web Vitals",
                    )
                )
        if not re.search(r"<link\b[^>]*rel\s*=\s*['\"][^'\"]*\bmanifest\b", content, re.I):
            findings.append(
                Finding(
                    severity="warning",
                    rule="manifest-link-missing",
                    path=rel_path,
                    line=1,
                    message="HTML does not link a web app manifest; install metadata may never be discovered.",
                    evidence="No <link rel=\"manifest\"> found.",
                    reference="references/08-online-pwa-symptom-fix-catalog.md: Install prompt missing",
                )
            )
        if re.search(r"apple-mobile-web-app-status-bar-style", content, re.I) and not re.search(
            r"apple-mobile-web-app-capable[^>]+content\s*=\s*['\"]yes['\"]", content, re.I
        ):
            findings.append(
                Finding(
                    severity="warning",
                    rule="apple-status-bar-without-standalone-meta",
                    path=rel_path,
                    line=1,
                    message="iOS status-bar style meta has no effect unless apple-mobile-web-app-capable=yes is also present.",
                    evidence="apple-mobile-web-app-status-bar-style present without capable=yes",
                    reference="references/08-online-pwa-symptom-fix-catalog.md: Splash, status bar, and launch flash",
                )
            )
        for link_match in TARGET_BLANK_PATTERN.finditer(content):
            tag = link_match.group(0)
            if not re.search(r"\brel\s*=\s*['\"][^'\"]*\bnoopener\b", tag, re.I):
                findings.append(
                    Finding(
                        severity="warning",
                        rule="target-blank-without-noopener",
                        path=rel_path,
                        line=line_number(content, link_match.start()),
                        message="target=_blank link lacks rel=noopener; external navigation and opener security are unverified.",
                        evidence=tag[:220],
                        reference="references/08-online-pwa-symptom-fix-catalog.md: Scope and external link handling",
                    )
                )

    return findings


def collect_project_evidence(files: list[Path]) -> ProjectEvidence:
    html_files = style_files = script_files = component_files = 0
    manifest_files = service_worker_files = service_worker_registrations = 0
    media_query_usages = container_query_usages = 0
    safe_area_usages = standalone_mode_usages = bottom_nav_usages = 0
    manifest_link_usages = theme_color_meta_usages = apple_mobile_web_app_capable_usages = 0
    apple_status_bar_meta_usages = apple_black_translucent_usages = apple_touch_icon_usages = 0
    viewport_fit_cover_usages = root_percent_height_usages = root_vh_height_usages = auth_web_storage_usages = 0
    bottom_nav_clearance_usages = bottom_nav_reserved_height_usages = fixed_bottom_block_usages = 0
    service_worker_fetch_listeners = service_worker_update_usages = service_worker_cache_cleanup_usages = 0
    skip_waiting_usages = clients_claim_usages = offline_fallback_usages = 0
    beforeinstallprompt_usages = appinstalled_usages = ios_install_fallback_usages = 0
    notification_permission_usages = push_subscribe_usages = push_event_usages = notification_click_usages = 0
    background_sync_usages = online_fallback_usages = 0
    storage_api_usages = storage_persist_usages = mutation_request_usages = offline_queue_usages = 0
    capture_input_usages = media_capture_usages = lifecycle_resume_usages = 0
    history_api_usages = popstate_usages = external_link_usages = target_blank_without_noopener_usages = 0
    focus_visible_usages = reduced_motion_usages = 0
    hover_usages = 0
    forced_colors_usages = dark_mode_usages = haptic_usages = test_files = 0
    aria_usages = semantic_landmark_usages = image_tags = responsive_image_usages = ui_state_usages = 0

    for path in files:
        suffix = path.suffix.lower()
        if suffix in {".html", ".htm"}:
            html_files += 1
        if suffix in {".css", ".scss"}:
            style_files += 1
        if suffix in {".js", ".jsx", ".mjs", ".ts", ".tsx", ".vue", ".svelte", ".astro"}:
            script_files += 1
        if looks_like_component(path):
            component_files += 1
        if looks_like_manifest(path):
            manifest_files += 1
        if looks_like_service_worker(path):
            service_worker_files += 1
        if looks_like_test(path):
            test_files += 1

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = path.read_text(encoding="utf-8", errors="replace")
        folded = content.casefold()

        service_worker_registrations += len(re.findall(r"navigator\.serviceworker\.register", folded))
        media_query_usages += folded.count("@media")
        container_query_usages += folded.count("@container")
        safe_area_usages += folded.count("env(safe-area-inset") + folded.count("constant(safe-area-inset")
        standalone_mode_usages += len(STANDALONE_PATTERN.findall(content))
        manifest_link_usages += len(re.findall(r"<link\b[^>]*rel\s*=\s*['\"][^'\"]*\bmanifest\b", folded))
        theme_color_meta_usages += len(re.findall(r"<meta\b[^>]*name\s*=\s*['\"]theme-color['\"]", folded))
        apple_mobile_web_app_capable_usages += folded.count("apple-mobile-web-app-capable")
        apple_status_bar_meta_usages += folded.count("apple-mobile-web-app-status-bar-style")
        apple_black_translucent_usages += len(APPLE_BLACK_TRANSLUCENT_PATTERN.findall(content))
        viewport_fit_cover_usages += len(VIEWPORT_FIT_COVER_PATTERN.findall(content))
        apple_touch_icon_usages += folded.count("apple-touch-icon")
        bottom_nav_usages += len(BOTTOM_NAV_PATTERN.findall(content))
        bottom_nav_clearance_usages += len(BOTTOM_CLEARANCE_PATTERN.findall(content))
        bottom_nav_reserved_height_usages += len(BOTTOM_RESERVED_PATTERN.findall(content))
        root_percent_height_usages += sum(
            1
            for block_match in CSS_BLOCK_PATTERN.finditer(content)
            if css_block_has_root_percent_height(block_match.group("selector"), block_match.group("body"))
        )
        root_vh_height_usages += sum(
            1
            for block_match in CSS_BLOCK_PATTERN.finditer(content)
            if css_block_has_root_vh_height(block_match.group("selector"), block_match.group("body"))
        )
        fixed_bottom_block_usages += sum(
            1 for block_match in CSS_BLOCK_PATTERN.finditer(content) if css_block_has_fixed_bottom(block_match.group("body"))
        )
        service_worker_fetch_listeners += len(re.findall(r"addEventListener\s*\(\s*['\"]fetch['\"]", content, re.I))
        service_worker_update_usages += (
            folded.count("updatefound")
            + folded.count("controllerchange")
            + len(re.findall(r"\.update\s*\(", content))
        )
        service_worker_cache_cleanup_usages += folded.count("caches.delete") + folded.count("caches.keys") + folded.count("cleanupoutdatedcaches")
        skip_waiting_usages += folded.count("skipwaiting")
        clients_claim_usages += folded.count("clients.claim")
        offline_fallback_usages += sum(
            folded.count(term)
            for term in (
                "offline.html",
                "offline fallback",
                "offlinefallback",
                "navigatefallback",
                "navigationfallback",
                "request.mode === 'navigate'",
                'request.mode === "navigate"',
                "event.request.mode === 'navigate'",
                'event.request.mode === "navigate"',
            )
        )
        beforeinstallprompt_usages += folded.count("beforeinstallprompt")
        appinstalled_usages += folded.count("appinstalled")
        ios_install_fallback_usages += sum(
            folded.count(term)
            for term in ("add to home screen", "add-to-home-screen", "share menu", "ios install", "safari install")
        )
        notification_permission_usages += folded.count("notification.requestpermission")
        push_subscribe_usages += folded.count("pushmanager") + folded.count("pushsubscription") + folded.count("applicationserverkey")
        push_event_usages += len(re.findall(r"addEventListener\s*\(\s*['\"]push['\"]", content, re.I))
        notification_click_usages += len(re.findall(r"addEventListener\s*\(\s*['\"]notificationclick['\"]", content, re.I))
        background_sync_usages += folded.count("syncmanager") + len(re.findall(r"addEventListener\s*\(\s*['\"]sync['\"]", content, re.I))
        online_fallback_usages += folded.count("navigator.online") + folded.count("onlineManager") + folded.count("addEventListener('online") + folded.count('addEventListener("online')
        storage_api_usages += (
            folded.count("indexeddb")
            + folded.count("localstorage")
            + folded.count("sessionstorage")
            + folded.count("caches.open")
        )
        auth_web_storage_usages += len(AUTH_WEB_STORAGE_PATTERN.findall(content))
        storage_persist_usages += folded.count("navigator.storage.persist") + folded.count("navigator.storage.estimate")
        mutation_request_usages += len(
            re.findall(r"\bmethod\s*:\s*['\"](?:post|put|patch|delete)['\"]", content, re.I)
        )
        offline_queue_usages += sum(folded.count(term) for term in ("outbox", "offline queue", "offlinequeue", "background queue", "backgroundqueue", "queue.addrequest"))
        file_capture_count = len(CAPTURE_INPUT_PATTERN.findall(content))
        capture_input_usages += file_capture_count
        media_capture_usages += folded.count("getusermedia") + folded.count("mediadevices") + file_capture_count
        lifecycle_resume_usages += folded.count("visibilitychange") + folded.count("pagehide") + folded.count("pageshow") + folded.count("resume") + folded.count("focus")
        history_api_usages += folded.count("pushstate") + folded.count("replacestate")
        popstate_usages += folded.count("popstate")
        external_link_usages += len(EXTERNAL_LINK_PATTERN.findall(content))
        target_blank_without_noopener_usages += sum(
            1 for match in TARGET_BLANK_PATTERN.finditer(content) if not re.search(r"\brel\s*=\s*['\"][^'\"]*\bnoopener\b", match.group(0), re.I)
        )
        focus_visible_usages += folded.count(":focus-visible")
        hover_usages += folded.count(":hover")
        reduced_motion_usages += folded.count("prefers-reduced-motion")
        forced_colors_usages += folded.count("forced-colors")
        dark_mode_usages += folded.count("prefers-color-scheme") + folded.count("color-scheme")
        aria_usages += folded.count("aria-")
        semantic_landmark_usages += len(re.findall(r"<(?:main|nav|header|footer|aside|section)\b", folded))
        image_tags += len(re.findall(r"<img\b", folded))
        responsive_image_usages += folded.count("srcset") + folded.count("<picture") + folded.count("sizes=")
        ui_state_usages += sum(folded.count(term) for term in ("loading", "empty", "error", "disabled", "skeleton"))
        haptic_usages += folded.count("navigator.vibrate") + folded.count(".vibrate(") + folded.count("haptic")

    return ProjectEvidence(
        html_files=html_files,
        style_files=style_files,
        script_files=script_files,
        component_files=component_files,
        manifest_files=manifest_files,
        service_worker_files=service_worker_files,
        service_worker_registrations=service_worker_registrations,
        media_query_usages=media_query_usages,
        container_query_usages=container_query_usages,
        safe_area_usages=safe_area_usages,
        standalone_mode_usages=standalone_mode_usages,
        manifest_link_usages=manifest_link_usages,
        theme_color_meta_usages=theme_color_meta_usages,
        apple_mobile_web_app_capable_usages=apple_mobile_web_app_capable_usages,
        apple_status_bar_meta_usages=apple_status_bar_meta_usages,
        apple_black_translucent_usages=apple_black_translucent_usages,
        viewport_fit_cover_usages=viewport_fit_cover_usages,
        root_percent_height_usages=root_percent_height_usages,
        root_vh_height_usages=root_vh_height_usages,
        auth_web_storage_usages=auth_web_storage_usages,
        apple_touch_icon_usages=apple_touch_icon_usages,
        bottom_nav_usages=bottom_nav_usages,
        bottom_nav_clearance_usages=bottom_nav_clearance_usages,
        bottom_nav_reserved_height_usages=bottom_nav_reserved_height_usages,
        fixed_bottom_block_usages=fixed_bottom_block_usages,
        service_worker_fetch_listeners=service_worker_fetch_listeners,
        service_worker_update_usages=service_worker_update_usages,
        service_worker_cache_cleanup_usages=service_worker_cache_cleanup_usages,
        skip_waiting_usages=skip_waiting_usages,
        clients_claim_usages=clients_claim_usages,
        offline_fallback_usages=offline_fallback_usages,
        beforeinstallprompt_usages=beforeinstallprompt_usages,
        appinstalled_usages=appinstalled_usages,
        ios_install_fallback_usages=ios_install_fallback_usages,
        notification_permission_usages=notification_permission_usages,
        push_subscribe_usages=push_subscribe_usages,
        push_event_usages=push_event_usages,
        notification_click_usages=notification_click_usages,
        background_sync_usages=background_sync_usages,
        online_fallback_usages=online_fallback_usages,
        storage_api_usages=storage_api_usages,
        storage_persist_usages=storage_persist_usages,
        mutation_request_usages=mutation_request_usages,
        offline_queue_usages=offline_queue_usages,
        capture_input_usages=capture_input_usages,
        media_capture_usages=media_capture_usages,
        lifecycle_resume_usages=lifecycle_resume_usages,
        history_api_usages=history_api_usages,
        popstate_usages=popstate_usages,
        external_link_usages=external_link_usages,
        target_blank_without_noopener_usages=target_blank_without_noopener_usages,
        focus_visible_usages=focus_visible_usages,
        hover_usages=hover_usages,
        reduced_motion_usages=reduced_motion_usages,
        forced_colors_usages=forced_colors_usages,
        dark_mode_usages=dark_mode_usages,
        aria_usages=aria_usages,
        semantic_landmark_usages=semantic_landmark_usages,
        image_tags=image_tags,
        responsive_image_usages=responsive_image_usages,
        ui_state_usages=ui_state_usages,
        haptic_usages=haptic_usages,
        test_files=test_files,
    )


def build_evidence_gap_findings(evidence: ProjectEvidence) -> list[Finding]:
    findings: list[Finding] = []
    data = asdict(evidence)
    for field, rule, message, reference, severity in EVIDENCE_RULES:
        if data[field] == 0:
            findings.append(
                Finding(
                    severity="evidence-gap" if severity == "warning" else "info",
                    rule=rule,
                    path=".",
                    line=0,
                    message=message,
                    evidence=f"{field}=0",
                    reference=reference,
                )
            )
    pwa_like = evidence.manifest_files > 0 or evidence.service_worker_files > 0 or evidence.service_worker_registrations > 0
    has_service_worker_evidence = evidence.service_worker_files > 0 or evidence.service_worker_registrations > 0
    uses_ios_edge_to_edge_status = evidence.apple_black_translucent_usages > 0 and evidence.viewport_fit_cover_usages > 0
    if uses_ios_edge_to_edge_status and evidence.root_percent_height_usages > 0:
        findings.append(
            Finding(
                severity="critical",
                rule="ios-black-translucent-root-100-percent-chin-gap-risk",
                path=".",
                line=0,
                message=(
                    "iOS chin-gap risk found: viewport-fit=cover and black-translucent status-bar style are present, "
                    "and a root/app-shell selector uses 100% height. Use 100vh for the iOS edge-to-edge root or omit black-translucent."
                ),
                evidence=(
                    f"apple_black_translucent_usages={evidence.apple_black_translucent_usages}, "
                    f"viewport_fit_cover_usages={evidence.viewport_fit_cover_usages}, "
                    f"root_percent_height_usages={evidence.root_percent_height_usages}"
                ),
                reference="references/08-online-pwa-symptom-fix-catalog.md: iOS standalone chrome and safe areas",
            )
        )
    if uses_ios_edge_to_edge_status and evidence.root_vh_height_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="ios-black-translucent-height-evidence-missing",
                path=".",
                line=0,
                message=(
                    "iOS black-translucent edge-to-edge metadata exists but no root/full-screen shell 100vh evidence was found. "
                    "Cold-start installed iOS PWA chin-gap behaviour is unverified."
                ),
                evidence=(
                    f"apple_black_translucent_usages={evidence.apple_black_translucent_usages}, "
                    f"viewport_fit_cover_usages={evidence.viewport_fit_cover_usages}, root_vh_height_usages=0"
                ),
                reference="references/07-bottom-nav-pwa-safe-area.md: iOS Black-Translucent Chin Gap",
            )
        )
    if pwa_like and evidence.auth_web_storage_usages > 0:
        findings.append(
            Finding(
                severity="warning",
                rule="ios-installed-auth-storage-isolation-risk",
                path=".",
                line=0,
                message=(
                    "Auth-like localStorage/sessionStorage usage was found in a PWA-like project. "
                    "iOS installed PWAs use isolated storage from Safari; use cookies when login state must survive Add to Home Screen."
                ),
                evidence=f"auth_web_storage_usages={evidence.auth_web_storage_usages}",
                reference="references/08-online-pwa-symptom-fix-catalog.md: iOS standalone chrome and safe areas",
            )
        )
    if pwa_like and evidence.standalone_mode_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="standalone-mode-evidence-missing",
                path=".",
                line=0,
                message="PWA evidence exists but no standalone/display-mode branch was found. Browser versus installed-PWA layout is unverified.",
                evidence=(
                    f"manifest_files={evidence.manifest_files}, service_worker_files={evidence.service_worker_files}, "
                    f"service_worker_registrations={evidence.service_worker_registrations}, standalone_mode_usages=0"
                ),
                reference="references/07-bottom-nav-pwa-safe-area.md: Browser Versus PWA Comparison",
            )
        )
    if evidence.manifest_files > 0 and evidence.manifest_link_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="manifest-link-evidence-missing",
                path=".",
                line=0,
                message="Manifest file exists but no HTML <link rel=manifest> evidence was found.",
                evidence=f"manifest_files={evidence.manifest_files}, manifest_link_usages=0",
                reference="references/08-online-pwa-symptom-fix-catalog.md: Install prompt missing",
            )
        )
    if evidence.manifest_files > 0 and evidence.theme_color_meta_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="theme-color-meta-evidence-missing",
                path=".",
                line=0,
                message="PWA manifest exists but no theme-color meta evidence was found. Browser chrome/status-bar colour is unverified.",
                evidence=f"manifest_files={evidence.manifest_files}, theme_color_meta_usages=0",
                reference="references/08-online-pwa-symptom-fix-catalog.md: Splash, status bar, and launch flash",
            )
        )
    if evidence.manifest_files > 0 and evidence.apple_mobile_web_app_capable_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="ios-standalone-meta-evidence-missing",
                path=".",
                line=0,
                message="PWA manifest exists but no apple-mobile-web-app-capable meta evidence was found. iOS Home Screen standalone behaviour is unverified.",
                evidence=f"manifest_files={evidence.manifest_files}, apple_mobile_web_app_capable_usages=0",
                reference="references/08-online-pwa-symptom-fix-catalog.md: iOS standalone chrome and safe areas",
            )
        )
    if evidence.manifest_files > 0 and evidence.apple_touch_icon_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="apple-touch-icon-evidence-missing",
                path=".",
                line=0,
                message="PWA manifest exists but no apple-touch-icon evidence was found. iOS home-screen icon rendering is unverified.",
                evidence=f"manifest_files={evidence.manifest_files}, apple_touch_icon_usages=0",
                reference="references/08-online-pwa-symptom-fix-catalog.md: Manifest and install identity",
            )
        )
    if has_service_worker_evidence and evidence.service_worker_fetch_listeners == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="service-worker-fetch-handler-evidence-missing",
                path=".",
                line=0,
                message="Service worker file exists but no fetch event handler evidence was found. Installability, offline, and request handling are unverified.",
                evidence=(
                    f"service_worker_files={evidence.service_worker_files}, "
                    f"service_worker_registrations={evidence.service_worker_registrations}, service_worker_fetch_listeners=0"
                ),
                reference="references/08-online-pwa-symptom-fix-catalog.md: Service worker update and stale shell",
            )
        )
    if has_service_worker_evidence and evidence.offline_fallback_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="offline-navigation-fallback-evidence-missing",
                path=".",
                line=0,
                message="Service worker exists but no navigation/offline fallback evidence was found.",
                evidence=(
                    f"service_worker_files={evidence.service_worker_files}, "
                    f"service_worker_registrations={evidence.service_worker_registrations}, offline_fallback_usages=0"
                ),
                reference="references/08-online-pwa-symptom-fix-catalog.md: Offline reload and navigation fallback",
            )
        )
    if has_service_worker_evidence and evidence.service_worker_cache_cleanup_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="service-worker-cache-cleanup-evidence-missing",
                path=".",
                line=0,
                message="Service worker exists but no cache cleanup evidence was found. Stale assets after deploy are unverified.",
                evidence=(
                    f"service_worker_files={evidence.service_worker_files}, "
                    f"service_worker_registrations={evidence.service_worker_registrations}, service_worker_cache_cleanup_usages=0"
                ),
                reference="references/08-online-pwa-symptom-fix-catalog.md: Service worker update and stale shell",
            )
        )
    if has_service_worker_evidence and evidence.service_worker_update_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="service-worker-update-ui-evidence-missing",
                path=".",
                line=0,
                message="Service worker exists but no updatefound/controllerchange/manual update evidence was found.",
                evidence=(
                    f"service_worker_files={evidence.service_worker_files}, "
                    f"service_worker_registrations={evidence.service_worker_registrations}, service_worker_update_usages=0"
                ),
                reference="references/08-online-pwa-symptom-fix-catalog.md: Service worker update and stale shell",
            )
        )
    if evidence.skip_waiting_usages > 0 and evidence.clients_claim_usages > 0 and evidence.service_worker_update_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="force-update-without-ui-evidence",
                path=".",
                line=0,
                message="skipWaiting and clients.claim are present but no app-side update UI evidence was found; live update can blank or mismatch old clients.",
                evidence=(
                    f"skip_waiting_usages={evidence.skip_waiting_usages}, clients_claim_usages={evidence.clients_claim_usages}, "
                    "service_worker_update_usages=0"
                ),
                reference="references/08-online-pwa-symptom-fix-catalog.md: Service worker update and stale shell",
            )
        )
    if evidence.beforeinstallprompt_usages > 0 and evidence.ios_install_fallback_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="ios-install-fallback-evidence-missing",
                path=".",
                line=0,
                message="beforeinstallprompt is used but no iOS/Safari Add to Home Screen fallback copy or flow was found.",
                evidence=f"beforeinstallprompt_usages={evidence.beforeinstallprompt_usages}, ios_install_fallback_usages=0",
                reference="references/08-online-pwa-symptom-fix-catalog.md: Install prompt missing",
            )
        )
    if evidence.beforeinstallprompt_usages > 0 and evidence.appinstalled_usages == 0:
        findings.append(
            Finding(
                severity="info",
                rule="appinstalled-evidence-missing",
                path=".",
                line=0,
                message="beforeinstallprompt is used but no appinstalled tracking evidence was found.",
                evidence=f"beforeinstallprompt_usages={evidence.beforeinstallprompt_usages}, appinstalled_usages=0",
                reference="references/08-online-pwa-symptom-fix-catalog.md: Install prompt missing",
            )
        )
    if evidence.push_subscribe_usages > 0 and evidence.notification_permission_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="push-permission-flow-evidence-missing",
                path=".",
                line=0,
                message="Push subscription code exists but no notification permission request evidence was found.",
                evidence=f"push_subscribe_usages={evidence.push_subscribe_usages}, notification_permission_usages=0",
                reference="references/08-online-pwa-symptom-fix-catalog.md: Push notifications",
            )
        )
    if evidence.push_subscribe_usages > 0 and evidence.push_event_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="push-event-handler-evidence-missing",
                path=".",
                line=0,
                message="Push subscription code exists but no service-worker push event handler evidence was found.",
                evidence=f"push_subscribe_usages={evidence.push_subscribe_usages}, push_event_usages=0",
                reference="references/08-online-pwa-symptom-fix-catalog.md: Push notifications",
            )
        )
    if evidence.push_event_usages > 0 and evidence.notification_click_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="notification-click-handler-evidence-missing",
                path=".",
                line=0,
                message="Push event handler exists but no notificationclick handler evidence was found. Notification routing/open behaviour is unverified.",
                evidence=f"push_event_usages={evidence.push_event_usages}, notification_click_usages=0",
                reference="references/08-online-pwa-symptom-fix-catalog.md: Push notifications",
            )
        )
    if evidence.push_subscribe_usages > 0 and evidence.standalone_mode_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="push-ios-standalone-gate-evidence-missing",
                path=".",
                line=0,
                message="Push code exists but no standalone/display-mode gate was found. iOS Home Screen subscription flow is unverified.",
                evidence=f"push_subscribe_usages={evidence.push_subscribe_usages}, standalone_mode_usages=0",
                reference="references/08-online-pwa-symptom-fix-catalog.md: Push notifications",
            )
        )
    if evidence.background_sync_usages > 0 and evidence.online_fallback_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="background-sync-fallback-evidence-missing",
                path=".",
                line=0,
                message="Background Sync is used but no online/manual retry fallback evidence was found. iOS and unsupported browsers are unverified.",
                evidence=f"background_sync_usages={evidence.background_sync_usages}, online_fallback_usages=0",
                reference="references/08-online-pwa-symptom-fix-catalog.md: Offline mutations and background sync",
            )
        )
    if evidence.storage_api_usages > 0 and evidence.storage_persist_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="storage-persistence-evidence-missing",
                path=".",
                line=0,
                message="Browser storage is used but no storage persistence/quota estimate evidence was found.",
                evidence=f"storage_api_usages={evidence.storage_api_usages}, storage_persist_usages=0",
                reference="references/08-online-pwa-symptom-fix-catalog.md: Storage, quota, and data loss",
            )
        )
    if evidence.mutation_request_usages > 0 and pwa_like and evidence.offline_queue_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="offline-mutation-queue-evidence-missing",
                path=".",
                line=0,
                message="PWA-like project sends mutating requests but no offline outbox/queue evidence was found.",
                evidence=f"mutation_request_usages={evidence.mutation_request_usages}, offline_queue_usages=0",
                reference="references/08-online-pwa-symptom-fix-catalog.md: Offline mutations and background sync",
            )
        )
    if evidence.media_capture_usages > 0 and evidence.lifecycle_resume_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="media-capture-resume-evidence-missing",
                path=".",
                line=0,
                message="Camera/media capture is used but no visibility/pageshow/pagehide/focus lifecycle recovery evidence was found.",
                evidence=f"media_capture_usages={evidence.media_capture_usages}, lifecycle_resume_usages=0",
                reference="references/08-online-pwa-symptom-fix-catalog.md: Camera, file capture, and media resume",
            )
        )
    if evidence.history_api_usages > 0 and evidence.popstate_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="android-back-history-evidence-missing",
                path=".",
                line=0,
                message="History API is used but no popstate evidence was found. Android hardware back behaviour is unverified.",
                evidence=f"history_api_usages={evidence.history_api_usages}, popstate_usages=0",
                reference="references/08-online-pwa-symptom-fix-catalog.md: Android hardware back and SPA history",
            )
        )
    if evidence.bottom_nav_usages > 0 and evidence.standalone_mode_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="bottom-nav-standalone-evidence-missing",
                path=".",
                line=0,
                message="Bottom navigation evidence exists but no standalone/display-mode handling was found.",
                evidence=f"bottom_nav_usages={evidence.bottom_nav_usages}, standalone_mode_usages=0",
                reference="references/07-bottom-nav-pwa-safe-area.md: Files To Trace",
            )
        )
    if evidence.bottom_nav_usages > 0 and evidence.bottom_nav_clearance_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="bottom-nav-clearance-evidence-missing",
                path=".",
                line=0,
                message="Bottom navigation evidence exists but no shared safe-area/bottom clearance token was found.",
                evidence=f"bottom_nav_usages={evidence.bottom_nav_usages}, bottom_nav_clearance_usages=0",
                reference="references/07-bottom-nav-pwa-safe-area.md: Preferred Token Shape",
            )
        )
    if evidence.bottom_nav_usages > 0 and evidence.bottom_nav_reserved_height_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="bottom-nav-reserved-height-evidence-missing",
                path=".",
                line=0,
                message="Bottom navigation evidence exists but no route/content reserved-height signal was found.",
                evidence=f"bottom_nav_usages={evidence.bottom_nav_usages}, bottom_nav_reserved_height_usages=0",
                reference="references/07-bottom-nav-pwa-safe-area.md: Preferred Token Shape",
            )
        )
    if evidence.fixed_bottom_block_usages > 0 and evidence.bottom_nav_clearance_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="fixed-bottom-clearance-evidence-missing",
                path=".",
                line=0,
                message="Fixed bottom CSS exists but no shared bottom clearance evidence was found.",
                evidence=f"fixed_bottom_block_usages={evidence.fixed_bottom_block_usages}, bottom_nav_clearance_usages=0",
                reference="references/07-bottom-nav-pwa-safe-area.md: Static Scanner Leads",
            )
        )
    if evidence.fixed_bottom_block_usages > 0 and evidence.standalone_mode_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="fixed-bottom-standalone-evidence-missing",
                path=".",
                line=0,
                message="Fixed bottom CSS exists but no standalone/display-mode branch was found.",
                evidence=f"fixed_bottom_block_usages={evidence.fixed_bottom_block_usages}, standalone_mode_usages=0",
                reference="references/07-bottom-nav-pwa-safe-area.md: Browser Versus PWA Comparison",
            )
        )
    if evidence.bottom_nav_usages > 0 and evidence.fixed_bottom_block_usages == 0:
        findings.append(
            Finding(
                severity="info",
                rule="bottom-nav-position-evidence-missing",
                path=".",
                line=0,
                message="Bottom navigation terms exist but no CSS fixed-bottom block was detected. Inspect whether the nav is hidden, sticky, portal-rendered, or styled elsewhere.",
                evidence=f"bottom_nav_usages={evidence.bottom_nav_usages}, fixed_bottom_block_usages=0",
                reference="references/07-bottom-nav-pwa-safe-area.md: Files To Trace",
            )
        )
    if evidence.fixed_bottom_block_usages > 0 and evidence.safe_area_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="fixed-bottom-safe-area-evidence-missing",
                path=".",
                line=0,
                message="Fixed bottom CSS exists but no safe-area inset usage was found.",
                evidence=f"fixed_bottom_block_usages={evidence.fixed_bottom_block_usages}, safe_area_usages=0",
                reference="references/07-bottom-nav-pwa-safe-area.md: Failure Signs",
            )
        )
    if evidence.hover_usages > 0 and evidence.focus_visible_usages == 0:
        findings.append(
            Finding(
                severity="evidence-gap",
                rule="hover-without-focus-visible-evidence",
                path=".",
                line=0,
                message="Hover styles exist but no :focus-visible usage was found. Keyboard and touch parity are unverified.",
                evidence=f"hover_usages={evidence.hover_usages}, focus_visible_usages=0",
                reference="references/04-audit-checklist.md: Touch targets and pointer media",
            )
        )
    if evidence.image_tags > 0 and evidence.responsive_image_usages == 0:
        findings.append(
            Finding(
                severity="info",
                rule="responsive-image-evidence-missing",
                path=".",
                line=0,
                message="Images exist but no srcset, sizes, or picture usage was found. Responsive image behaviour is unverified.",
                evidence=f"image_tags={evidence.image_tags}, responsive_image_usages=0",
                reference="references/05-code-patterns-library.md: Image optimisation pattern",
            )
        )
    return findings


def build_summary(findings: list[Finding], files_scanned: int) -> Summary:
    return Summary(
        files_scanned=files_scanned,
        findings=len(findings),
        critical=sum(1 for item in findings if item.severity == "critical"),
        warning=sum(1 for item in findings if item.severity == "warning"),
        info=sum(1 for item in findings if item.severity == "info"),
        evidence_gap=sum(1 for item in findings if item.severity == "evidence-gap"),
    )


def print_text(summary: Summary, findings: list[Finding]) -> None:
    print("Static PWA scan")
    print(f"Files scanned: {summary.files_scanned}")
    print(
        "Findings: "
        f"{summary.findings} "
        f"(critical {summary.critical}, warning {summary.warning}, "
        f"evidence-gap {summary.evidence_gap}, info {summary.info})"
    )
    if not findings:
        print("No static findings. This does not replace device, PWA, keyboard, or accessibility verification.")
        return

    for item in findings:
        print()
        location = item.path if item.line == 0 else f"{item.path}:{item.line}"
        print(f"[{item.severity.upper()}] {item.rule} - {location}")
        print(item.message)
        print(f"Evidence: {item.evidence}")
        print(f"Reference: {item.reference}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=".", help="Project path to scan.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--audit-dir", help="Single root folder for generated artifacts. JSON report goes under reports/.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero on critical, warning, or evidence-gap output. Info-only output still exits zero.",
    )
    args = parser.parse_args()

    root = Path(args.path).resolve()
    files = list(iter_files(root))
    findings: list[Finding] = []
    for path in files:
        findings.extend(scan_file(path, root))
    evidence = collect_project_evidence(files)
    findings.extend(build_evidence_gap_findings(evidence))
    severity_order = {"critical": 0, "warning": 1, "evidence-gap": 2, "info": 3}
    findings.sort(key=lambda item: (severity_order.get(item.severity, 4), item.path, item.line, item.rule))
    summary = build_summary(findings, len(files))
    report = {
        "summary": asdict(summary),
        "project_evidence": asdict(evidence),
        "findings": [asdict(item) for item in findings],
        "artifactPaths": {"auditDir": str(Path(args.audit_dir).resolve()) if args.audit_dir else None},
    }
    if args.audit_dir:
        report_path = Path(args.audit_dir).resolve() / "reports" / "static-scan.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report["artifactPaths"]["jsonReport"] = str(report_path)
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print_text(summary, findings)

    if args.strict:
        return 1 if summary.critical or summary.warning or summary.evidence_gap else 0
    return 1 if summary.critical else 0


if __name__ == "__main__":
    raise SystemExit(main())

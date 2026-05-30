# Playwright PWA Device Simulation

Use this when the task needs repeatable browser evidence for how a PWA is likely to render across iPhone, iPad, and Android installed-app shapes.

Use it alongside code auditing, not instead of it. Before treating a simulation result as actionable, inspect the route/component/CSS/metadata/service-worker owner that can produce the observed behaviour.

## Honest Boundary

Playwright can emulate device descriptors such as viewport, screen size, DPR, user agent, touch support, colour scheme, reduced motion, permissions, WebKit/Chromium engines, network state, and screenshots. It can also run JavaScript before page load to force `navigator.standalone` and `matchMedia("(display-mode: standalone)")` for app code.

It cannot perfectly become the real iOS Home Screen Web.app process. Real iOS status bar placement, OS chrome, CSS `env(safe-area-inset-*)`, installed-app storage isolation, notification install state, and platform-specific launch behaviour still require real hardware. Treat simulated evidence as strong regression evidence, not final device proof.

## Tool

Run:

```bash
python scripts/simulate_pwa_devices.py TARGET --devices ios-core --modes browser,standalone --audit-dir ./web-layout-audit-runs/pwa-device-audit --format json
```

Useful variants:

```bash
python scripts/simulate_pwa_devices.py TARGET --devices phones --modes standalone --browser auto --strict
python scripts/simulate_pwa_devices.py TARGET --devices iphone-12,iphone-14-pro --modes browser,standalone --color-scheme dark --audit-dir ./web-layout-audit-runs/dark-pwa-sim
python scripts/simulate_pwa_devices.py TARGET --devices ios-core --modes standalone --permissions notifications --format json
python scripts/simulate_pwa_devices.py TARGET --devices iphone-12 --modes standalone --headed
```

## What The Simulator Forces

- Playwright device descriptor or fallback viewport/DPR/touch/user-agent.
- WebKit for iOS profiles when `--browser auto` is used.
- Chromium for Android profiles when `--browser auto` is used.
- HTML classes: `pwa-sim`, `pwa-sim-standalone`, `display-mode-standalone`, `pwa-standalone`, `is-standalone`, `standalone`.
- JavaScript signals: `navigator.standalone` and `matchMedia("(display-mode: standalone)")`.
- Best-effort CSS activation: clones accessible `@media (display-mode: standalone)` rule contents into active CSS for standalone runs.
- In non-browser modes, common safe-area CSS variables such as `--safe-area-bottom`, `--safe-bottom`, `--sab`, and shell equivalents.
- App-settle waiting before screenshots and probes: ready state, main/root content, network idle where possible, and disappearance of loaders/skeletons/spinners.
- Launch-state coverage: `first-launch` captures onboarding if present; `main-ui` seeds common onboarding-complete storage flags and tries visible skip/dismiss/continue controls so the main UI can also be audited.
- Runtime geometry audit from `probe_ui_runtime.py`: overflow, fixed-bottom overlap, scroll clearance, small touch targets, image risks, and accessibility-name risks.

## What It Does Not Prove

- Real iOS Home Screen Web.app chrome.
- Real CSS `env(safe-area-inset-bottom)` values when the browser reports zero.
- Cross-origin stylesheet display-mode rules that CSSOM blocks.
- Real installed storage isolation.
- OS-level install, launch, push, badging, app switcher, or notification click behaviour.
- Real keyboard-open geometry.
- App-specific onboarding gates unless the auditor supplies `--storage-flag` or `--dismiss-selector`.

If any of these matter, the report must say they remain unverified.

## Device Groups

- `ios-core`: iPhone SE, iPhone 12/13 size, iPhone 14 Pro size, iPhone 15 Pro Max fallback, iPad 11-inch.
- `android-core`: Pixel 7, Galaxy S23 fallback.
- `phones`: iOS and Android phone profiles.
- `all`: every bundled profile.

## Hard Audit Procedure

1. Use one artifact root with `--audit-dir`; do not scatter screenshots or JSON files across the repo.
2. Run browser and standalone modes for `ios-core`.
3. Let the simulator wait for app settle. If `app-not-fully-settled-before-probe` appears, increase `--settle-timeout`, provide `--main-selector`, or fix the loader/state that never resolves.
4. Trace the code owner for each finding: route/component, root CSS token, display-mode branch, viewport metadata, manifest, service worker, app shell, scroll root, bottom UI, or dependent floating surface.
5. Compare source and computed geometry first: `facts.displayModeMatches`, `facts.navigatorStandalone`, `facts.safeAreaEnv`, manifest display, iOS meta facts, DOM rects, scroll clearance, and CSS variables.
6. Compare screenshots after the code/runtime facts, not as the diagnosis.
7. Inspect `emulation.blockerFacts`. If first launch is blocked by onboarding, require a `main-ui` pass too. If main UI is still blocked, add `--storage-flag` or `--dismiss-selector` for the app's real gate.
8. Treat `bottom-fixed-overlap-runtime` and `bottom-scroll-clearance-runtime` as fix blockers for bottom chrome.
9. If `safe-area-env-not-emulated` appears, inspect whether the app uses shared safe-area variables that the simulator injected. If the app uses raw `env()` directly, keep real-device safe-area verification open.
10. If `display-mode-css-clone-incomplete` appears, inspect blocked stylesheets manually.
11. Fix shell-level owners first: root CSS tokens, display-mode branch, viewport metadata, manifest, app shell, scroll root, bottom UI, and dependent floating surfaces.

## Report Rules

Label evidence precisely:

- **Simulated iPhone WebKit standalone:** Playwright WebKit plus forced standalone signals and screenshots.
- **Class-emulated standalone:** root classes activated but CSS display-mode was not actually proven.
- **CSS-cloned display-mode:** accessible standalone media rules were copied into active CSS.
- **Real installed PWA:** only use this label after actual device Home Screen install.

Never call Playwright standalone simulation "exact iOS PWA proof". It is regression evidence and a bug finder.

Never call a screenshot mismatch the root cause until the relevant source owner and computed/runtime facts explain it.

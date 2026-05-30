# Bottom Nav, Tab Bar, and Installed-PWA Safe Area Workflow

Use this reference when the visible bug involves a bottom navbar, tab bar, floating cart button, sticky checkout CTA, drawer/sheet handle, home-indicator collision, bottom viewport gap, or a mismatch between mobile browser and installed iOS/Android PWA.

This file is an extra task-focused workflow. It does not replace `references/PWA.md`, which preserves the original source in full.

## Core Rule

Do not patch only the bottom-nav component unless the shell owner has already been proven correct. Bottom chrome is a shared app-shell problem because it affects scroll containers, safe-area insets, route padding, drawers, sheets, floating buttons, toasts, sticky CTAs, and installed-PWA display mode.

The correct fix usually lives in root layout tokens, not a one-off page padding value.

A screenshot can show the gap, overlap, or chin strip, but the diagnosis must come from source ownership. Trace the HTML head, root CSS, shell, scroll root, bottom component, dependent bottom UI, and display-mode detection before editing.

## Failure Signs

- Browser mode shows a floating nav, but installed PWA docks it differently.
- Installed PWA has a black or empty strip under the nav.
- The nav collides with the iOS home indicator or Android gesture area.
- The last card, CTA, drawer, or cart button sits under the nav.
- Scroll end padding differs by route.
- The nav uses `bottom: 0`, `bottom: 16px`, or a hard-coded height without a shared clearance variable.
- One component uses `env(safe-area-inset-bottom)` while another uses a separate magic number.
- iOS Home Screen mode uses `viewport-fit=cover` plus `apple-mobile-web-app-status-bar-style=black-translucent` and the root still has `height: 100%`.
- A screenshot comparison is treated as proof even though geometry was not measured.

## Files To Trace

Find the owner chain before editing:

- HTML head: viewport meta, `viewport-fit=cover`, `apple-mobile-web-app-status-bar-style`, app root classes, theme/status colour.
- Root CSS: safe-area variables, viewport units, body/root height, scroll root, bottom padding.
- App shell/layout: route container, main scroll area, standalone/browser display-mode branch.
- Bottom nav/tab bar component: position, height, bottom offset, z-index, blur/backdrop, hit targets.
- Dependent bottom UI: cart drawer, floating cart button, sticky checkout CTA, toasts, sheets, modals, account/order actions.
- PWA detection: `@media (display-mode: standalone)`, root class such as `html.pwa-standalone`, `navigator.standalone`, manifest `display`, and any launch-mode script.
- Tests/probes: viewport sweep, browser mode, standalone class emulation, installed device if available.

Keep the owner chain in the audit notes. For each owner, record the exact file, selector or component, the relevant token/state/meta field, and whether computed/runtime evidence confirms it. Do not accept a visual crop as proof of the root cause.

## iOS Black-Translucent Chin Gap

Treat this as a specific bug family, not a generic safe-area issue:

| Setup | Expected audit result |
| --- | --- |
| `display: standalone` without `black-translucent` | Usually safe. iOS reserves status/home-indicator areas and paints them from manifest/page background. |
| `display: standalone` plus `viewport-fit=cover`, default status bar style | Usually safe in portrait; useful for landscape edge-to-edge with manual `env(safe-area-inset-left/right)` control. |
| `display: standalone` plus `viewport-fit=cover` plus `black-translucent` plus root `height: 100%` | Broken risk. The view can shift up behind the status bar while the root height does not compensate, leaving a bottom chin gap around the status-bar height. |
| `display: standalone` plus `viewport-fit=cover` plus `black-translucent` plus root/full-screen shell `height: 100vh` | The current hard fix when true four-edge iOS rendering is required. |

Hard audit:

- Inspect the exact viewport meta and `apple-mobile-web-app-status-bar-style` meta.
- Search root CSS for `html`, `body`, `#root`, `#__next`, `.app`, or full-screen shell `height`, `min-height`, `block-size`, and `min-block-size`.
- If `black-translucent` is absent, do not cargo-cult it to fix a bottom nav gap. Prefer manifest `display: standalone`, manifest `background_color`, page background, and shared bottom-chrome tokens.
- If `black-translucent` is present, prove the final computed root/full-screen shell height is `100vh`, not `100%`, on a cold-start installed iOS PWA.
- Measure bottom gap in pixels and compare browser mode, standalone simulation, and real installed Home Screen mode when available.

Hard fix:

- Default path: omit `apple-mobile-web-app-status-bar-style` or leave it as `default`; keep `display: standalone`, `background_color`, `theme-color`, and root background aligned.
- Landscape edge-to-edge path: use `viewport-fit=cover` and safe-area tokens, without `black-translucent`, unless portrait content must render behind the status bar.
- True four-edge iOS path: keep `black-translucent`, but change root/full-screen shell height from `100%` to `100vh`, then retest cold launch, portrait, landscape, scroll end, and bottom fixed UI.
- Do not "fix" the chin gap by adding a bottom spacer under the nav. That hides the symptom and leaves the root viewport contract wrong.

Playwright simulation can catch CSS regressions and standalone-class branches, but it cannot prove the real iOS Home Screen status-bar offset. Mark real installed-device proof as unverified unless it was actually tested.

## Preferred Token Shape

Names can follow the app's conventions, but the behaviour needs these separate concepts:

```css
:root {
  --safe-area-bottom: env(safe-area-inset-bottom, 0px);
  --bottom-nav-height: 64px;
  --bottom-nav-bottom-offset: 16px;
  --bottom-nav-reserved-height:
    calc(var(--bottom-nav-height) + var(--bottom-nav-bottom-offset) + var(--safe-area-bottom));
}

@media (display-mode: standalone) {
  :root {
    --bottom-nav-bottom-offset: 0px;
  }
}

html.pwa-standalone {
  --bottom-nav-bottom-offset: 0px;
}

.app-scroll-root {
  padding-bottom: var(--bottom-nav-reserved-height);
}

.bottom-nav {
  position: fixed;
  left: 0;
  right: 0;
  bottom: var(--bottom-nav-bottom-offset);
  height: calc(var(--bottom-nav-height) + var(--safe-area-bottom));
  padding-bottom: var(--safe-area-bottom);
}
```

Use the same reserved-height token for drawers, FABs, cart buttons, sheets, and sticky CTAs. If a component needs extra spacing, add a derived token so the relationship stays auditable.

## Browser Versus PWA Comparison

Record this before and after the fix:

| Check | Browser Mode | Standalone/PWA Mode | Result |
| --- | --- | --- | --- |
| Source owner chain inspected | file/selector/component | file/selector/component | proven/unverified |
| Nav bottom gap | measured px | measured px | proven/unverified |
| Nav top overlap with content | measured px or none | measured px or none | proven/unverified |
| Last scroll item visible above nav | yes/no | yes/no | proven/unverified |
| Home indicator or gesture area cleared | yes/no/unverified | yes/no/unverified | proven/unverified |
| Route scroll root uses shared reserved token | file/line | file/line | proven/unverified |
| Drawers/FABs/sticky CTAs use same token | file/line | file/line | proven/unverified |

If only a class-emulated standalone pass was run, say so. It is useful evidence for CSS such as `html.pwa-standalone`, but it is not proof of real installed-PWA behaviour.

## Static Scanner Leads

Treat these scanner outputs as investigation leads:

- `bottom-nav-standalone-evidence-missing`: a bottom-nav surface exists but no standalone/display-mode handling was found.
- `bottom-nav-clearance-evidence-missing`: bottom-nav terms exist but no shared bottom clearance/safe-area token was found.
- `bottom-nav-reserved-height-evidence-missing`: a bottom-nav surface exists but no route/content reserved-height signal was found.
- `fixed-bottom-display-mode-clearance-unverified`: a fixed-bottom CSS block does not show nearby safe-area, reserved-height, or standalone handling.
- `standalone-mode-evidence-missing`: the project looks like a PWA but no installed display-mode branch was found.
- `ios-black-translucent-edge-to-edge-audit-required`: `viewport-fit=cover` and `black-translucent` are both present, so root height and installed iOS cold launch must be proven.
- `ios-black-translucent-root-100-percent-chin-gap-risk`: the exact high-risk chin-gap combination was found.
- `ios-black-translucent-height-evidence-missing`: `black-translucent` edge-to-edge metadata exists but no root/full-screen `100vh` evidence was found.

These are proof gaps unless the exact source inspection proves a different owner handles the behaviour.

## Runtime Probe Leads

Use `probe_ui_runtime.py` on phone-sized viewports. For class-based standalone CSS, compare:

```bash
python scripts/probe_ui_runtime.py TARGET --viewport modern-phone --format json --strict
python scripts/probe_ui_runtime.py TARGET --viewport modern-phone --html-class pwa-standalone --format json --strict
```

Important runtime rules:

- `bottom-fixed-overlap-runtime`: fixed bottom UI is occupying the same visible area as content.
- `bottom-scroll-clearance-runtime`: the document bottom clearance is smaller than the fixed bottom UI height, so final scroll content may hide under the nav.
- `fixed-bottom-runtime`: fixed bottom UI exists and still needs manual safe-area/display-mode verification.

## Completion Gate

Do not call a bottom-nav fix complete until all are proven or explicitly unverified:

- Browser mode nav position matches the intended design.
- Installed-PWA mode or standalone-class emulation matches the intended design.
- The source owner chain is inspected and explains the runtime geometry.
- Bottom gap is measured, not eyeballed.
- Nav top does not cover the current content at the tested scroll position.
- At final scroll position, the last meaningful content/action can sit above the nav.
- The home indicator or Android gesture area is cleared.
- All dependent bottom UI consumes the same shared token system.
- The fix works on every route that can show bottom chrome.

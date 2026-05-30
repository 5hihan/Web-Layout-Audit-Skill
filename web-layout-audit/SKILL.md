---
name: web-layout-audit
description: Audit, fix, and verify all UI-related behaviour in websites, web apps, mobile UI, app shells, and PWAs using fact-based device reasoning. Check intended design versus implemented code, responsive layout, visual hierarchy, spacing, typography, overflow, images, states, viewport, safe-area, keyboard, scroll, touch, haptics, motion, manifest, service worker updates, performance, accessibility, and device-specific defects. Use for targeted small UI fixes, full UI reviews, LLM-generated UI validation, installed PWA issues, bottom bars, iOS chin gaps, forms, modals, WebViews, native-app conversion, and will-this-look-wrong-on-a-device checks.
---

# Cross-Platform Web and PWA Layout Audit

Use this skill to make web UI behave correctly across desktop browsers, mobile browsers, WebViews, and installed PWAs. The complete original source is preserved at `references/PWA.md`; the split reference files exist only to make lookup cheaper and more precise.

## Suspicious Audit Posture

Assume nothing is correct until evidence proves it. Do not trust framework defaults, generated code, passing builds, existing abstractions, screenshots, "works on my machine" reports, desktop previews, or previous audit notes as proof. Treat every claim as unverified until it has direct evidence from code inspection, automated checks, browser/runtime behaviour, or real device/PWA testing.

Use this evidence standard:

- **Proven:** directly inspected or tested in the current task with concrete evidence.
- **Suspicious:** code shape suggests risk or the implementation relies on fragile platform assumptions.
- **Unverified:** no direct evidence has been collected yet.
- **Not applicable:** explicitly ruled out by the product surface, not merely skipped.

Keep an assumption ledger while auditing. For each area, record the claim, the evidence collected, the result, and the remaining proof gap. If evidence is missing, report it as unverified instead of saying it is fine.

For LLM-generated or LLM-modified UI, explicitly check whether the intended UI was fully implemented. Extract the intention from the user request, design artifact, issue, screenshot, or prior agent plan; map each intended outcome to files/components; then prove the rendered result matches. If the code only partially implements the intention, call it partial, not done.

Reason only from facts. Phrases like "should be fine", "probably works", "looks responsive", or "the framework handles it" are not evidence. Replace them with inspected source, measured geometry, computed styles, DOM state, accessibility tree output, browser trace, device result, or an explicit unverified status. Screenshots can prove what a user saw; they do not prove why it happened.

## Code-First Evidence Order

Use screenshots as symptom and regression artifacts, not as the primary diagnosis. For every visual defect, build this chain before editing:

1. **User-visible symptom:** screenshot, report, runtime finding, or reproduction steps.
2. **Source owner:** route, component, layout shell, CSS rule, root token, HTML head, manifest, service worker, or platform-detection code that can produce the symptom.
3. **Code evidence:** exact selectors, props, state, tokens, media queries, display-mode branches, viewport metadata, lifecycle handlers, or cache/update logic.
4. **Runtime confirmation when useful:** computed styles, DOM rects, CSS variables, scroll metrics, accessibility tree, logs, network/cache facts, or focused device probe.
5. **Screenshot comparison:** use only after the code owner and computed behaviour are understood, to confirm the final visual result and catch framing regressions.

Do not patch from pixels alone. If a screenshot shows a navbar gap, clipped CTA, keyboard overlap, blank install screen, stale shell, or bad spacing, first trace the files and platform contract that own it. If the owner cannot be found, report that as the blocker instead of guessing a visual spacer.

## Scope Modes

Default to the smallest scope that can honestly fix the user's request.

- **Targeted fix:** Use when the user names one concrete problem, component, screenshot defect, route, or state, such as "fix this navbar gap", "this modal clips", "input zooms on iOS", or "button text overflows". Do not run a full audit. Inspect the broken surface, its shared owner chain, and adjacent regressions only.
- **Focused surface audit:** Use when the symptom spans one family, such as bottom chrome, forms/keyboard, modals/sheets, service-worker updates, install flow, or PWA standalone mode. Check that family across relevant routes and modes, not every UI category.
- **Full audit:** Use only when the user asks for a broad review, pre-ship sweep, "cover everything", native-app conversion, broad PWA hardening, LLM UI acceptance, or an unknown multi-surface failure.

For targeted fixes, keep the work tight:

- Do not block on `scan_pwa_static.py`, `probe_ui_runtime.py`, device simulation, or a full checklist unless the issue needs that proof.
- Do inspect real files before editing and trace shared ownership far enough to avoid one-off padding or screenshot-only patches.
- If the issue reveals a shared shell/root cause, widen only to that owner chain and state why.
- If no screenshots, logs, or JSON are generated, no audit artifact folder is required. If any artifact is generated, keep it under one `--audit-dir` folder.
- Verify the affected path and the nearest likely regression paths. Mark unrelated audit areas as not inspected, not as correct.

## First Move

1. Choose `Targeted fix`, `Focused surface audit`, or `Full audit` from the user's wording and risk. If the user asks for a small fix, use Targeted fix.
2. Identify the surface being changed: app shell, viewport setup, bottom navigation/tab bar, safe-area layout, keyboard/form path, scroll root, modal/drawer/sheet, PWA manifest, service worker/update flow, install UX, haptics, motion, media, performance, or accessibility.
3. Build the source-owner chain before recommending a fix. In targeted mode, inspect only the affected component, its route/container, and any shared root owner that can plausibly cause the symptom.
4. Load the narrowest relevant reference file from `references/`. Use `references/PWA.md` only when you need the complete source or exact original wording.
5. Create one audit artifact root only when generating screenshots, JSON reports, logs, or probe output. Keep all generated artifacts inside it.
6. Run `scan_pwa_static.py`, `probe_ui_runtime.py`, or `simulate_pwa_devices.py` when their evidence is useful for the selected scope. In targeted mode, use the relevant viewport/mode only; use `--viewport all` and strict broad scans for full audits.
7. Fix the shared owner of the behaviour. Prefer root tokens, reusable helpers, app-shell primitives, manifest/service-worker flow, or component-system fixes over per-page padding and screenshot-specific patches.
8. Verify the actual affected behaviour and the nearest likely regressions. Untested relevant risk remains unverified; unrelated areas are out of scope unless the user asked for a broad audit.

## Reference Files

- `references/source-map.md`: source line ranges, file map, and script usage.
- `references/01-foundations-and-quickstart.md`: trigger scope, operating rules, and the top 22 shipping checks.
- `references/02-correction-playbook.md`: defect correction format, wrong-implementation matrix, geometry probes, viewport sweeps, and fix gates.
- `references/03-native-app-conversion.md`: native-app acceptance criteria, force-update PWA requirements, all-button haptics, app-like motion, and native-app verification report template.
- `references/04-audit-checklist.md`: runnable checks for viewport, safe areas, viewport units, fixed bottom UI, keyboard, scroll, modals, touch, manifest, service worker, install UX, performance, haptics, accessibility, form factors, theming, and storage.
- `references/05-code-patterns-library.md`: code templates for manifest, service worker, force update, safe-area shell, CSS reset, haptics, motion, standalone detection, keyboard adjustment, modal scroll lock, install prompts, network, share, images, forms, uploads, and media.
- `references/06-failure-modes-matrices-references.md`: failure catalogue, device matrix, decision trees, anti-patterns, performance budget, accessibility checklist, methodology, modern CSS reference, LLM anti-patterns, and cross-reference index.
- `references/07-bottom-nav-pwa-safe-area.md`: focused workflow for bottom navigation, tab bars, home-indicator clearance, browser versus installed-PWA drift, and shared shell spacing tokens.
- `references/08-online-pwa-symptom-fix-catalog.md`: public PWA symptom families and hard audit/fix paths for install prompts, manifests, service-worker updates, offline reloads, iOS standalone chrome, push, scope/link handling, Android back, camera capture, storage, sync, and share targets.
- `references/09-playwright-pwa-device-simulation.md`: Playwright multi-device PWA simulation workflow for iPhone/iPad/Android browser versus standalone runs, code-owner tracing, forced standalone signals, display-mode CSS cloning, safe-area approximation, screenshot confirmation, and real-device caveats.
- `references/PWA.md`: full original source kept intact.

## Scripts and Assets

- `scripts/pwa_section.py`: list, find, and extract exact sections from `references/PWA.md` with line provenance. Use `python scripts/pwa_section.py list`, `python scripts/pwa_section.py find "query"`, or `python scripts/pwa_section.py extract "heading"`.
- `scripts/scan_pwa_static.py`: suspiciously scan a project for common static UI/PWA hazards and missing evidence. It reports confirmed code-shape findings and `evidence-gap` items for missing proof around responsive CSS, manifest identity, service-worker fetch/update/offline paths, install prompt fallback, push, storage/queue, media capture, history/back handling, safe areas, standalone display-mode handling, shared bottom-nav clearance, focus-visible, reduced motion, forced colours, semantic structure, UI states, haptics, and tests. Use `--audit-dir AUDIT_DIR --format json` when another tool will consume the results and `--strict` when missing evidence should fail the scan.
- `scripts/probe_ui_runtime.py`: open a URL or local HTML file with Playwright across device-sized viewports and report rendered facts: horizontal overflow, outside-viewport elements, clipped content, fixed-bottom UI, bottom-nav overlap/scroll clearance, small touch targets, unnamed controls, input zoom risks, image risks, and screenshots when requested. Use after source ownership is understood, and use `--audit-dir AUDIT_DIR` to keep reports/screenshots in one removable folder.
- `scripts/simulate_pwa_devices.py`: run Playwright device profiles across browser and standalone modes. It uses WebKit for iOS profiles when available, waits for app content and loaders to settle, probes first-launch and main-UI states when onboarding blocks the view, injects standalone root classes and JS display-mode signals, best-effort activates standalone CSS media rules, injects common safe-area variables, captures screenshots, and reports simulation caveats. Use for PWA browser-versus-installed-mode regression evidence after auditing the relevant source owners.
- `scripts/validate_skill_package.py`: validate this skill folder and optional zip for required files, frontmatter, source preservation, split-reference coverage, script syntax, and package hygiene after editing the skill itself.
- `assets/audit-report-template.md`: use for broad audits or final reports.
- `assets/correction-record-template.md`: use when tracking a single defect through the correction protocol.
- `assets/verification-matrix-template.md`: use when the task needs explicit device, display-mode, keyboard, PWA, haptics, accessibility, or performance evidence.
- `assets/ui-intent-device-audit-template.md`: use when validating LLM-generated UI, a design implementation, or a user-facing visual change against intended outcomes and device appearance.
- `assets/runtime-probe-report-template.md`: use to summarise source-owner prechecks, runtime probe results, screenshot confirmation, viewport findings, and manual follow-up gaps.
- `assets/bottom-nav-pwa-audit-template.md`: use when auditing or fixing a bottom nav, tab bar, home-indicator collision, bottom viewport gap, floating cart button, drawer, sticky checkout CTA, or browser-versus-installed-PWA mismatch.
- `assets/pwa-symptom-fix-audit-template.md`: use for broad PWA symptom sweeps that cover installability, stale updates, offline, iOS standalone, push, scope/link handling, back button, capture/media, storage, and sync.
- `assets/pwa-device-simulation-report-template.md`: use when reporting Playwright device simulation runs, code-owner prechecks, standalone signals, CSS cloning, geometry findings, screenshot confirmation, and real-device gaps.

The static scanner is intentionally conservative and incomplete. A clean scan only means those text patterns were not found. It does not prove correctness. Always inspect matched code manually, close evidence gaps, load the relevant reference sections, and verify behaviour in browser/device/PWA contexts.

The runtime probe is also incomplete. It can prove some rendered geometry facts, but it does not replace keyboard-open testing, installed-PWA testing, real safe-area hardware, screen-reader review, or touch feel checks.

After editing this skill, run `python scripts/validate_skill_package.py . --zip ../web-layout-audit.zip --format json` from inside the skill folder, or the equivalent path from the parent workspace.

## Routing

- For a small, explicitly requested fix, use Targeted fix mode, read `02-correction-playbook.md` only if diagnosis is non-trivial, then load only the one relevant checklist/pattern/reference file. Use `assets/correction-record-template.md` only when a written defect record is useful.
- For any LLM-generated UI or design implementation, start with `assets/ui-intent-device-audit-template.md`, then inspect the relevant code and run the strict scanner.
- For a broad pre-ship UI review, read `01-foundations-and-quickstart.md`, `04-audit-checklist.md`, and `06-failure-modes-matrices-references.md`.
- For an existing bug or bad generated implementation, read `02-correction-playbook.md` first, then the relevant checklist or code pattern.
- For native-feel or web-to-app conversion, read `03-native-app-conversion.md`, then `05-code-patterns-library.md` for implementation patterns.
- For bottom navbar, tab bar, home-indicator collision, floating bottom chrome, bottom viewport gap, or browser-versus-iOS-PWA mismatch, read `07-bottom-nav-pwa-safe-area.md` and use `assets/bottom-nav-pwa-audit-template.md` before patching code.
- For iOS PWA chin gaps involving `viewport-fit=cover`, `apple-mobile-web-app-status-bar-style=black-translucent`, or root `height: 100%`, read `07-bottom-nav-pwa-safe-area.md` and `08-online-pwa-symptom-fix-catalog.md`; audit the metadata/root-height combination before adding bottom spacers.
- For viewport gaps, clipped bottom UI, home-indicator overlap, or `100vh` bugs, read `04-audit-checklist.md` sections 1-4 and the safe-area/app-shell patterns in `05-code-patterns-library.md`.
- For keyboard, forms, input zoom, focused controls, or virtual keyboard layout, read `04-audit-checklist.md` sections 5-6 and the keyboard/input patterns in `05-code-patterns-library.md`.
- For scroll locking, pull-to-refresh, custom scroll roots, drawers, modals, sheets, or stacking problems, read `04-audit-checklist.md` sections 7-11 plus the modal and pull-to-refresh patterns.
- For installability, manifest, service worker, stale shell, cache updates, or force refresh, read `04-audit-checklist.md` sections 12-14 and the PWA patterns in `05-code-patterns-library.md`.
- For broad PWA coverage or online-reported symptoms such as install prompt missing, stale update, offline reload failure, iOS push failure, scope/link weirdness, Android back button traps, camera capture bugs, or storage loss, read `08-online-pwa-symptom-fix-catalog.md` and use `assets/pwa-symptom-fix-audit-template.md`.
- For multi-device PWA simulation, iPhone standalone regression sweeps, browser-versus-installed drift, onboarding/main-UI coverage, loader timing, or Playwright device proof, read `09-playwright-pwa-device-simulation.md` and run `scripts/simulate_pwa_devices.py --audit-dir AUDIT_DIR`.
- For haptics, press states, touch targets, app-like transitions, route motion, FLIP lists, and animation performance, read `03-native-app-conversion.md` and the haptics/motion patterns in `05-code-patterns-library.md`.
- For final hardening, read the anti-patterns, device matrix, performance budget, and accessibility checklist in `06-failure-modes-matrices-references.md`.

## Correction Protocol

For every defect, preserve this reasoning structure in notes or in the user-facing report:

1. **Symptom:** what the user can see or do wrong.
2. **Broken assumption:** the false platform/layout belief behind the bug.
3. **Wrong implementation:** the exact code shape causing it.
4. **Correct implementation:** the shared token, semantic element, CSS primitive, JavaScript helper, manifest field, service-worker flow, or platform feature that should own it.
5. **Regression proof:** the device, viewport, display-mode, keyboard, scroll, motion, accessibility, and performance checks that prove the fix is not local-only.

Do not stop after naming an anti-pattern. Explain how to spot it, why it fails, what replaces it, and which devices or modes need re-testing.

## Bias Controls

- Start from evidence, not from confidence in the framework, author, library, or generated code.
- Start with source ownership. A screenshot can identify the symptom, but inspected code and runtime facts must explain the bug before a fix is accepted.
- Look for disconfirming evidence before accepting a claim as proven.
- If a helper, component library, CSS reset, service worker plugin, PWA plugin, or framework claims to handle an area, inspect the emitted code or runtime behaviour anyway.
- Treat "no scanner finding" as "not disproven by this scanner", not as "correct".
- Separate confirmed defects from unverified proof gaps in the report.
- Do not hide uncertainty. State "unverified" when device, installed-PWA, keyboard, accessibility, or performance checks were not run.
- Audit the final rendered result, not just the code change. If the intended UI cannot be observed or measured, the intention is unverified.

## Device Appearance Reasoning

The core question is: will it look wrong on a device? Answer that with observable evidence, not implementation intent.

For each relevant device class, ask what can visually go wrong and collect proof:

- Small phone: text wrapping, horizontal overflow, clipped CTAs, cramped spacing, target size, keyboard overlap, safe-area collision.
- Modern phone: bottom bars, home indicator, status bar, scroll end padding, modal/sheet height, gesture navigation.
- Android: keyboard resize mode, pull-to-refresh, gesture area, hardware/back behaviour where relevant, tap feedback.
- Tablet and foldable: awkward breakpoints, over-wide text, under-dense layouts, modal widths, split-screen behaviour.
- Desktop: max-width, empty space, hover/focus parity, pointer affordance, scrollbars, resizable windows.
- Installed PWA: standalone chrome, status/theme colour, home-screen launch, stale shell, update prompt, offline fallback.

Do not answer "will it look wrong?" from intent or screenshots alone. Answer from a source-owner map plus computed layout, DOM geometry, responsive sweep, accessibility tree, performance trace, screenshot confirmation, or explicit unverified status.

When runtime probing is available, run at least `small-phone`, `modern-phone`, `tablet`, and `desktop`. If the issue involves mobile install, bottom UI, keyboard, or safe area, include the closest available phone viewport and still mark real installed-PWA hardware as unverified unless it was actually tested.

In Targeted fix mode, shrink this matrix to the affected viewport/device state plus the nearest regression state. For example, a bottom nav PWA bug needs browser and standalone phone evidence, not a desktop typography audit; an input zoom bug needs focused iOS form evidence, not service-worker checks.

## Implementation Rules

- Keep pinch zoom, focus outlines, scrolling, text selection, and browser UI available unless there is a narrow, justified, component-level exception.
- Use one correct viewport meta tag with `width=device-width`, `initial-scale=1`, `viewport-fit=cover`, and an explicit `interactive-widget` decision.
- Treat `apple-mobile-web-app-status-bar-style=black-translucent` as high-risk. Omit it unless the app intentionally renders behind the iOS status bar. If it is used with `viewport-fit=cover`, prove the installed iOS PWA root or full-screen shell computes to `100vh`, not `100%`, on cold launch, or keep the bottom chin gap suspicious.
- Avoid naked `100vh` and route shell height through the guide's dynamic, small, and large viewport unit strategy. Exception: the deliberate iOS standalone `black-translucent` edge-to-edge fix is a documented root/full-screen shell `100vh` with installed-device evidence.
- Route headers, bottom navigation, drawers, sheets, floating buttons, and CTAs through shared safe-area-aware tokens. Bottom chrome needs a single shell-owned height, bottom offset, safe-area, and reserved scroll clearance abstraction; every dependent surface must consume the same tokens.
- Treat browser and installed-PWA bottom nav as different display modes. Prove whether the nav floats, docks flush to the bottom, clears the home indicator, and reserves content space correctly in each mode.
- Keep iOS input font size at 16px or above and keep focused fields and primary actions visible when the keyboard opens.
- Provide non-hover paths, visible press states, `:focus-visible`, target-size compliance, and haptic binding for enabled buttons where supported.
- Use shared motion tokens, trigger motion from user intent or state change, respect reduced motion, and verify animation performance on constrained devices.
- Require valid manifest identity, start URL, scope, display settings, icons including maskable icons, install UX, versioned service-worker caches, update prompt, and force-update repair path for PWA work.
- Keep accessibility intact: semantic controls, accessible names, keyboard paths, visible focus, contrast, forced colours, reduced motion, modal focus management, and target sizes.
- Re-check current primary browser documentation when behaviour is version-dependent or experimental.
- Ensure loading, empty, error, disabled, long-content, short-content, and slow-network states exist or are explicitly not applicable.
- Verify images and media have stable dimensions, appropriate cropping, responsive sources where needed, alt/decorative handling, and no layout shift.
- Verify copy can wrap without clipping in narrow widths and under likely localisation or longer real data.

## Verification Matrix

Match verification to the risk:

- Viewport and safe area: small iPhone, modern iPhone, Android phone, landscape where relevant, tablet or foldable where relevant, browser mode, and installed PWA display mode if touched.
- Keyboard and forms: focused field near the bottom, keyboard open and closed, iOS input zoom, Android resize behaviour, scroll restoration, and primary action visibility.
- Fixed bottom UI: home indicator, Android gesture area, tab bar height, drawers/sheets/FABs/cart buttons, scroll end padding, and standalone/browser differences.
- Bottom nav/browser-versus-PWA: normal mobile browser chrome, standalone class or display-mode branch, real installed PWA when available, final scroll position, last card/action visibility, nav bottom gap, nav top overlap, and every dependent floating surface.
- PWA update flow: first install, reload, waiting service worker, update prompt, skip waiting or controlled activation path, cache version bump, offline fallback, and hard-reset repair path.
- Haptics and motion: every enabled button or control path, reduced motion, high-refresh screens, low-end mobile, interaction latency, dropped frames, and non-blocking input.
- Accessibility and system settings: keyboard navigation, screen-reader names, contrast, forced colours, dark mode, reduced motion, reduced data, RTL where relevant, and target size.
- Visual implementation: intended outcomes mapped to actual components, source-owner proof plus screenshots or geometry for target devices, state coverage, image/media behaviour, text wrapping, overflow, and z-index/overlay checks.
- Runtime geometry: `probe_ui_runtime.py` output for relevant viewports, screenshots when useful as visual confirmation, and explicit manual follow-up for anything the probe cannot measure.

If real hardware or installed-PWA testing is unavailable, say exactly what was tested and what remains unverified.

## Output Contract

When reporting a targeted fix, keep the close-out concise:

- The defect addressed.
- The files/shared owners changed.
- The focused verification performed.
- Any relevant unverified risk.

When reporting a focused or full audit, include:

- The defect or objective addressed.
- The files and shared owners changed.
- The intended UI outcomes and whether each was fully implemented, partially implemented, not implemented, or unverified.
- The assumption ledger: proven, suspicious, unverified, and not-applicable areas.
- The key reference sections used.
- The verification performed, including devices, viewport sizes, display modes, and tools.
- Any remaining unverified risk.

Do not call the work complete because one screenshot, one desktop browser, one build, or one simulated viewport passes.

## Completion Gate

Before finalising any UI/PWA audit or fix, build a claim-to-evidence table at the selected scope.

For Targeted fix mode, the table may be brief and cover only:

- The user's concrete bug or intended outcome.
- The files/components that implement the fix.
- Source-owner evidence and runtime/build evidence that prove the bug path.
- The nearest relevant regression checks.
- Any unverified risk that is still relevant to that bug.

For focused and full audits, include:

- Each user requirement or intended UI outcome.
- The files/components that implement it.
- Static evidence from source inspection.
- Runtime evidence from browser/device probing when available.
- Manual evidence or explicit unverified status for keyboard, installed PWA, real safe-area hardware, accessibility tree, animation smoothness, touch feel, and performance.
- For bottom-nav work, measured browser and standalone/PWA evidence for nav bottom gap, nav top overlap, content scroll-end clearance, and all dependent floating UI.
- Result: fully implemented, partially implemented, not implemented, not applicable, or unverified.

Only report completion when every relevant row is fully implemented or not applicable with evidence. Anything else remains open.

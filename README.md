# web-layout-audit

A coding-agent skill for auditing, fixing, and **verifying** UI behaviour in websites, web apps, mobile UI, app shells, and PWAs — using fact-based, device-grounded reasoning instead of "looks fine on my desktop".

It targets the class of defects that desktop previews hide and real devices expose: iOS chin gaps, bottom-nav / home-indicator collisions, keyboard overlap, input zoom, `100vh` bugs, stale service-worker shells, broken install flows, missing safe-area handling, and the gap between *intended* UI and *implemented* UI in LLM-generated code.

> **Note:** The skill's own packaging validator (`scripts/validate_skill_package.py`) intentionally **fails if a README exists inside the skill folder**. This file is documentation only — delete it before running `validate_skill_package.py` or zipping the skill for distribution.

---

## Core idea

**Assume nothing is correct until evidence proves it.** Framework defaults, generated code, passing builds, screenshots, and "works on my machine" reports are *not* proof. Every claim is tracked as one of:

- **Proven** — directly inspected or tested this task, with concrete evidence.
- **Suspicious** — code shape suggests risk or relies on fragile platform assumptions.
- **Unverified** — no direct evidence collected yet (reported as-is, never silently "fine").
- **Not applicable** — explicitly ruled out by the product surface.

Diagnosis follows a **code-first evidence order**: user-visible symptom → source owner (route/component/CSS/token/manifest/SW) → code evidence → runtime confirmation → *then* screenshot comparison. Screenshots prove what a user saw; they don't prove *why*. Fixes go into the shared owner (root tokens, app-shell primitives, manifest/SW flow) rather than per-page padding or screenshot-specific patches.

## Scope modes

The skill picks the smallest honest scope for the request:

| Mode | When | Behaviour |
|------|------|-----------|
| **Targeted fix** | User names one concrete problem ("fix this navbar gap", "input zooms on iOS") | Inspect the broken surface + its shared owner chain + nearest regressions. No full sweep, no mandatory scripts. |
| **Focused surface audit** | Symptom spans one family (bottom chrome, forms/keyboard, modals, SW updates, install flow) | Check that family across relevant routes and display modes. |
| **Full audit** | User asks for a broad review, pre-ship sweep, native-app conversion, or LLM-UI acceptance | Full checklist, device matrix, and verification gate. |

## Layout

```
web-layout-audit/
├── SKILL.md          # entry point: posture, scope modes, routing, verification gate
├── references/       # knowledge base (split from the original PWA.md source)
├── scripts/          # Python tooling: section lookup, static scan, runtime probe, device sim, validator
└── assets/           # report / record templates (default everything to "Unverified")
```

### references/

`PWA.md` is the complete original source, preserved verbatim (lines 1–3992). The numbered files are mechanically split from it so an agent loads only what a task needs; `07`–`09` are extra workflows not part of the original split. If anything conflicts, `PWA.md` wins.

- `source-map.md` — file map, source line ranges, scripted-lookup commands, source-preservation hash.
- `01-foundations-and-quickstart.md` — triggers, operating rules, top-22 pre-ship checklist.
- `02-correction-playbook.md` — defect correction format, wrong-implementation matrix, geometry probes, fix gates.
- `03-native-app-conversion.md` — native-app acceptance criteria, force-update, all-button haptics, app-like motion.
- `04-audit-checklist.md` — runnable checks for viewport, safe areas, viewport units, fixed bottom UI, keyboard, scroll, modals, touch, manifest, SW, install, performance, haptics, a11y, theming, storage.
- `05-code-patterns-library.md` — copy-ready templates for manifest, service worker, force update, safe-area shell, CSS reset, haptics, motion, standalone detection, keyboard adjustment, modal scroll lock, install prompts, share, images, forms, uploads, media.
- `06-failure-modes-matrices-references.md` — failure catalogue, device matrix, decision trees, anti-patterns, perf budget, a11y checklist, LLM anti-patterns, cross-reference index.
- `07-bottom-nav-pwa-safe-area.md` — bottom nav / tab bar / home-indicator clearance, browser-vs-installed drift, shared shell spacing tokens.
- `08-online-pwa-symptom-fix-catalog.md` — public PWA symptom families: install prompts, manifest identity, SW updates, offline reload, iOS standalone chrome, push, scope/links, Android back, capture, storage, sync, share targets.
- `09-playwright-pwa-device-simulation.md` — multi-device Playwright simulation workflow (iPhone/iPad/Android, browser vs standalone), display-mode CSS cloning, safe-area approximation, real-device caveats.

### scripts/

All scripts are Python 3 with `argparse` CLIs. Run them from inside the skill folder.

| Script | Purpose | Needs |
|--------|---------|-------|
| `pwa_section.py` | List / find / extract exact sections from `PWA.md` with line provenance. | stdlib |
| `scan_pwa_static.py` | Suspicious static scan for common UI/PWA hazards and **evidence gaps**. | stdlib |
| `probe_ui_runtime.py` | Open a URL or local HTML across device viewports; report overflow, clipping, fixed-bottom overlap, small touch targets, unnamed controls, input-zoom/image risks; optional screenshots. | Playwright |
| `simulate_pwa_devices.py` | Run device profiles across browser **and** standalone modes (WebKit for iOS), settle loaders, inject standalone/display-mode/safe-area signals, capture screenshots. | Playwright |
| `validate_skill_package.py` | Validate the skill folder (and optional zip): required files, frontmatter, source-hash preservation, split recombination, script syntax, package hygiene. | PyYAML |

Example commands (from `references/source-map.md`):

```bash
python scripts/pwa_section.py list
python scripts/pwa_section.py find "safe-area"
python scripts/pwa_section.py extract "Fixed bottom UI"

python scripts/scan_pwa_static.py /path/to/project
python scripts/scan_pwa_static.py /path/to/project --audit-dir ./web-layout-audit-runs/static --format json --strict

python scripts/probe_ui_runtime.py http://localhost:5173 --audit-dir ./web-layout-audit-runs/runtime --viewport all --format json --strict
python scripts/probe_ui_runtime.py http://localhost:5173 --audit-dir ./web-layout-audit-runs/runtime-standalone --viewport modern-phone --html-class pwa-standalone

python scripts/simulate_pwa_devices.py http://localhost:5173 --devices ios-core --modes browser,standalone --audit-dir ./web-layout-audit-runs/pwa-device-sim --format json

python scripts/validate_skill_package.py . --zip ../web-layout-audit.zip --format json
```

> The static scanner and runtime probe are **deliberately conservative and incomplete**. A clean scan only means those patterns weren't found — it never proves correctness. Always inspect matched code manually and verify in real browser/device/PWA contexts. Neither tool replaces keyboard-open testing, installed-PWA testing, real safe-area hardware, screen-reader review, or touch-feel checks.

### assets/

Markdown templates that default unchecked areas to `Unverified`, so a report never implies correctness without evidence:

- `audit-report-template.md` — broad audits / final reports.
- `correction-record-template.md` — single defect through the symptom → broken-assumption → wrong-impl → correct-impl → regression-proof protocol.
- `verification-matrix-template.md` — explicit device / display-mode / keyboard / PWA / haptics / a11y / perf evidence.
- `ui-intent-device-audit-template.md` — intended-vs-implemented UI trace for LLM-generated or design-driven changes.
- `runtime-probe-report-template.md` — source-owner precheck, viewport-by-viewport probe summary, manual follow-up gaps.
- `bottom-nav-pwa-audit-template.md` — browser-vs-PWA bottom nav measurements, owner chain, fix record.
- `pwa-symptom-fix-audit-template.md` — broad PWA symptom matrix and fix record.
- `pwa-device-simulation-report-template.md` — Playwright simulation report with code-owner precheck and standalone evidence.

## Requirements

- **Python 3** (3.12 verified) for all scripts.
- **Playwright** (with browsers installed) for `probe_ui_runtime.py` and `simulate_pwa_devices.py`. WebKit is used for iOS profiles when available.
- **PyYAML** for `validate_skill_package.py`.

## Conventions

- British spelling throughout.
- Prefer semantic HTML and vanilla CSS/JavaScript over custom widgets.
- Never hide layout defects by globally disabling zoom, focus outlines, scrolling, text selection, or browser UI.
- Re-check current primary browser documentation when behaviour is version-dependent or experimental.

## Completion gate

Work is only "done" when a claim-to-evidence table at the chosen scope shows every relevant row as **fully implemented** or **not applicable**, each backed by source-owner evidence plus runtime/device proof (or an explicit `Unverified` for anything not testable, e.g. real installed-PWA hardware). One passing screenshot, one desktop browser, or one simulated viewport is never sufficient.

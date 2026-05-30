# Source Map

`PWA.md` is the complete original source preserved verbatim. The other reference files are mechanically split from that source to make Claude load only the sections needed for a task. If there is any conflict, use `PWA.md` as the source of truth.

## Reference Files

- `PWA.md`: complete original source, lines 1-3992.
- `01-foundations-and-quickstart.md`: frontmatter, primary references, triggers, operating rules, and top 22 shipping checks. Source lines 1-62.
- `02-correction-playbook.md`: wrong-implementation diagnosis, correction format, spotting workflow, and fix gates. Source lines 63-205.
- `03-native-app-conversion.md`: native-app conversion acceptance criteria, PWA force-update, mandatory haptics, app-like motion, and verification report template. Source lines 206-368.
- `04-audit-checklist.md`: runnable audit checks for viewport meta, safe areas, viewport units, fixed bottom UI, keyboard, scroll, modals, touch, PWA manifest, service worker, install UX, performance, haptics, accessibility, form factors, theming, and storage. Source lines 369-901.
- `05-code-patterns-library.md`: implementation patterns and code templates for viewport, iOS metadata, manifest, service worker, force update, safe-area shell, CSS reset, haptics, motion, standalone detection, keyboard adjustment, scroll lock, install prompts, network, wake lock, share, images, forms, uploads, and media. Source lines 902-3324.
- `06-failure-modes-matrices-references.md`: failure-mode catalogue, device matrix, decision trees, feedback matrix, anti-patterns, performance budget, accessibility checklist, reference notes, audit methodology, LLM anti-patterns, and cross-reference index. Source lines 3325-3992.
- `07-bottom-nav-pwa-safe-area.md`: extra workflow for bottom navigation, tab bars, home-indicator clearance, browser versus installed-PWA drift, and shared shell spacing tokens. This is not part of the original source split.
- `08-online-pwa-symptom-fix-catalog.md`: extra workflow built from public PWA reports and current docs. Covers install prompts, manifest identity, service-worker updates, offline reloads, iOS standalone chrome, iOS black-translucent chin gaps, scope/link handling, push, Android back, camera capture, storage, sync, and share targets. This is not part of the original source split.
- `09-playwright-pwa-device-simulation.md`: extra workflow for Playwright iPhone/iPad/Android browser-versus-standalone simulation, code-owner tracing, forced standalone JS signals, display-mode CSS cloning, safe-area approximation, screenshots as regression evidence, and caveat labelling. This is not part of the original source split.

## Scripted Lookup

In Claude Code or another environment where scripts are available, run:

```bash
python scripts/pwa_section.py list
python scripts/pwa_section.py find "safe-area"
python scripts/pwa_section.py extract "Fixed bottom UI"
python scripts/scan_pwa_static.py /path/to/project
python scripts/scan_pwa_static.py /path/to/project --audit-dir ./web-layout-audit-runs/static --format json --strict
python scripts/probe_ui_runtime.py http://localhost:5173 --audit-dir ./web-layout-audit-runs/runtime --viewport all --format json --strict
python scripts/probe_ui_runtime.py ./dist/index.html --audit-dir ./web-layout-audit-runs/runtime --viewport small-phone
python scripts/probe_ui_runtime.py http://localhost:5173 --audit-dir ./web-layout-audit-runs/runtime-standalone --viewport modern-phone --html-class pwa-standalone --format json --strict
python scripts/simulate_pwa_devices.py http://localhost:5173 --devices ios-core --modes browser,standalone --audit-dir ./web-layout-audit-runs/pwa-device-sim --format json
python scripts/validate_skill_package.py . --zip ../web-layout-audit.zip --format json
```

Use `find` when you know the topic but not the exact heading. Use `extract` when you need one source section with line provenance.

Use `scan_pwa_static.py` as a suspicious first-pass defect and evidence-gap finder. It can flag common static hazards and missing proof areas, but it does not prove that viewport, keyboard, safe-area, installed-PWA, motion, accessibility, or performance behaviour is correct.

Use `probe_ui_runtime.py` when a URL or local HTML file can be opened in Playwright after the relevant source owner has been inspected. It provides rendered viewport facts and optional screenshots, but it still cannot prove keyboard-open, installed-PWA, real-device safe-area, screen-reader, or touch-feel behaviour by itself.

## Assets

- `assets/audit-report-template.md`: broad audit and final report structure.
- `assets/correction-record-template.md`: single-defect correction record following the required symptom, broken-assumption, wrong-implementation, correct-implementation, regression-proof sequence.
- `assets/verification-matrix-template.md`: explicit verification matrix for viewport, keyboard, fixed bottom UI, PWA updates, haptics/motion, and accessibility/system settings.
- `assets/ui-intent-device-audit-template.md`: intended UI versus implemented UI trace, device appearance checklist, and visual fact ledger.
- `assets/runtime-probe-report-template.md`: source-owner precheck, viewport-by-viewport runtime probe summary, and manual follow-up gaps.
- `assets/bottom-nav-pwa-audit-template.md`: browser-versus-PWA bottom nav measurement table, owner chain, fix record, and verification slots.
- `assets/pwa-symptom-fix-audit-template.md`: broad PWA symptom matrix and fix record for installability, stale updates, offline, iOS standalone, push, scope/link handling, back button, media, storage, and sync.
- `assets/pwa-device-simulation-report-template.md`: Playwright device simulation report with code-owner precheck, browser/standalone screenshot confirmation, standalone evidence, geometry findings, and real-device gaps.

All templates default unchecked areas to `Unverified` so the auditor does not accidentally imply correctness without evidence.

## Source Preservation Check

The current source-preservation hash is:

```text
PWA.md SHA-256: F3BBE17E602D8F76097467EF4FD21DCC1C4B3AF7382BA9D6756CF1F14A531973
```

The skill is only source-preserving if `references/PWA.md` still has the same content as the workspace `PWA.md` that was used to create it.

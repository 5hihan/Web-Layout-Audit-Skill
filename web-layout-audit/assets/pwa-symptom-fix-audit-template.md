# PWA Symptom Fix Audit

## Symptom Family

- User-visible symptom:
- Platform/display mode:
- Online source family:
- Local files/components involved:

## Source-To-Code Trace

| Symptom | Hard audit check | Source owner/file | Source evidence | Runtime/device evidence | Result |
| --- | --- | --- | --- | --- | --- |
| Install prompt missing | Manifest, SW fetch handler, early listener, iOS fallback |  |  |  | Unverified |
| Stale update/blank screen | SW lifecycle, cache cleanup, update UI, chunk compatibility |  |  |  | Unverified |
| Offline reload/deep link failure | Navigation fallback, precache, offline route |  |  |  | Unverified |
| iOS standalone chrome/safe area/chin gap | Display-mode branch, shell tokens, status colours, black-translucent/root-height check |  |  |  | Unverified |
| Push failure | Installed-mode gate, permission click, push/click handlers |  |  |  | Unverified |
| Scope/link weirdness | Manifest scope/start_url, external-link policy |  |  |  | Unverified |
| Android back issue | History writes, popstate, modal route policy |  |  |  | Unverified |
| Camera/media resume | Capture inputs, media lifecycle recovery, iOS standalone test |  |  |  | Unverified |
| Storage/data loss | Quota/persist, outbox, repair path |  |  |  | Unverified |

## Fix Record

- Broken assumption:
- Wrong implementation:
- Correct shared owner:
- Source-owner proof:
- Files changed:
- Regression checks:

## Verification

- Static scan:
- Runtime probe:
- Browser installability:
- Installed PWA:
- Offline reload/deep link:
- Update path:
- Push path:
- Storage/offline mutation and iOS install isolation:
- Remaining unverified risks:

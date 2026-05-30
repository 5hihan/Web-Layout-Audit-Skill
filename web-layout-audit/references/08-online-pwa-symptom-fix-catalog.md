# Online PWA Symptom Fix Catalog

Use this catalog when the user asks for broad PWA coverage or reports a symptom that does not fit a single layout bug. It turns recurring public reports and current docs into hard audit/fix paths.

This file is an extra workflow. It does not replace `references/PWA.md`, which preserves the original source in full.

## How To Use

1. Identify the symptom family before editing.
2. Run `scripts/scan_pwa_static.py PROJECT_PATH --format json --strict`.
3. Inspect every reported file manually. Scanner findings are leads, not proof.
4. Apply the hard fix at the shared owner: manifest, HTML head, service worker lifecycle, app shell, route/navigation layer, install prompt controller, push controller, or offline data layer.
5. Verify in browser mode and installed display mode. If real installed testing is unavailable, say it is unverified.

## Install Prompt Missing

Common symptoms:

- The custom install button never appears.
- `beforeinstallprompt` never fires.
- Works on Android/desktop but not iOS.
- Lighthouse passes but production still has no install prompt.

Hard audit:

- Manifest is linked from HTML and fetched without 404.
- Manifest JSON is valid.
- `name` or `short_name`, `id`, `start_url`, `scope`, display mode, colours, and install icons are explicit.
- `start_url` is inside `scope`.
- Service worker is registered and has a `fetch` handler.
- `beforeinstallprompt` listener is attached early, prevents default, stores the event, and calls `prompt()` only from a user click.
- Install prompt has a fallback path for iOS/Safari where `beforeinstallprompt` cannot fire.
- `appinstalled` is tracked or explicitly not needed.

Hard fix:

- Add or repair `<link rel="manifest">`.
- Repair manifest fields and icon URLs.
- Add a service-worker fetch handler before expecting Chromium installability.
- Move `beforeinstallprompt` capture close to page load; store one deferred event and clear it after `prompt()`.
- Render iOS-specific Add to Home Screen instructions only in browser mode, never inside standalone.

Scanner rules:

- `manifest-link-missing`
- `manifest-json-invalid`
- `manifest-start-url-out-of-scope`
- `manifest-icons-missing`
- `manifest-maskable-icon-missing`
- `service-worker-fetch-handler-evidence-missing`
- `ios-install-fallback-evidence-missing`

## Manifest And Install Identity

Common symptoms:

- App installs as a generic browser shortcut.
- Icon is missing, cropped, or letterboxed.
- Splash screen flashes a wrong colour.
- Installed app opens the wrong page.
- App identity changes after deployment or route change.

Hard audit:

- Manifest has stable `id`, `name` or `short_name`, explicit `start_url`, explicit `scope`, and intended `display` or `display_override`.
- Icons include valid `src`, useful sizes such as 192x192 and 512x512, and at least one maskable icon.
- `theme_color` and `background_color` match the app's real launch background.
- iOS has `apple-touch-icon`, `apple-mobile-web-app-title` where needed, and status-bar metadata if the app targets Home Screen install.

Hard fix:

- Make the manifest identity boring and stable.
- Keep start URL and all app routes under one explicit scope.
- Add maskable and non-maskable icons with real files, then verify all icon URLs return 200.
- Align manifest colours, HTML theme-colour meta, and CSS initial background.

Scanner rules:

- `manifest-id-missing`
- `manifest-scope-missing`
- `manifest-display-missing`
- `manifest-launch-colors-missing`
- `manifest-required-icon-sizes-unverified`
- `apple-touch-icon-evidence-missing`

## Service Worker Update And Stale Shell

Common symptoms:

- Users still see the old UI after deployment.
- Installed PWA has a blank screen after an update.
- New JavaScript 404s while old HTML is cached.
- Clearing site data fixes the app.
- Update works on desktop but mobile stays stale for days.

Hard audit:

- Service worker URL is stable; do not version the service-worker filename as the update strategy.
- Every named cache has a version and an activate cleanup path.
- The app can detect `updatefound`, waiting workers, and `controllerchange`.
- If `skipWaiting()` and `clients.claim()` are used, there is an intentional user-facing update/reload path.
- HTML, JS, CSS, and lazy chunks cannot be mixed across incompatible versions.
- A manual repair path exists for corrupted caches.

Hard fix:

- Keep `/sw.js` or the framework equivalent stable.
- On `activate`, delete old caches.
- Use an update prompt when a worker is waiting; reload after user confirmation.
- Avoid unconditional live takeover when chunk compatibility can break.
- Add deployment smoke tests that install, update, reload, and cold launch the PWA.

Scanner rules:

- `service-worker-cache-cleanup-evidence-missing`
- `service-worker-update-ui-evidence-missing`
- `force-update-without-ui-evidence`
- `service-worker-versioned-url-risk`

## Offline Reload And Navigation Fallback

Common symptoms:

- First page works offline but refresh shows browser error.
- Deep links fail offline.
- Images/fonts disappear offline.
- POST or scan workflows lose data while offline.

Hard audit:

- Navigation requests have an app-shell or offline document fallback.
- Offline fallback file is precached.
- Static assets needed for the shell are precached or runtime cached.
- Mutating requests have an outbox/queue with replay and conflict handling.
- Offline mode is tested by launching a deep route, then refreshing while offline.

Hard fix:

- Handle `event.request.mode === "navigate"` and return the app shell or `/offline.html`.
- Cache the fallback during service-worker install.
- Add an outbox for POST/PUT/PATCH/DELETE instead of pretending fetch will work offline.
- Add visible sync state and retry controls.

Scanner rules:

- `offline-navigation-fallback-evidence-missing`
- `offline-mutation-queue-evidence-missing`

## iOS Standalone Chrome And Safe Areas

Common symptoms:

- Bottom chin gap.
- Status bar is white/black or flashes on launch.
- Content slides under the status bar.
- Browser mode looks right but Home Screen mode is wrong.
- Users must log in again after Add to Home Screen even though Safari was logged in.

Hard audit:

- Read `references/07-bottom-nav-pwa-safe-area.md` for bottom nav and shell spacing.
- HTML has standalone/iOS metadata where needed.
- CSS has safe-area-aware shell tokens for top, bottom, fixed chrome, and scroll clearance.
- Browser mode and standalone mode have explicit branches.
- Manifest/background/status colours match the initial body/root background.
- Inspect whether `viewport-fit=cover`, `apple-mobile-web-app-status-bar-style=black-translucent`, and root `html, body { height: 100% }` appear together. That combination is the known iOS chin-gap trap.
- If `black-translucent` is used, inspect the final computed height of `html`, `body`, and the app shell in cold-start installed mode. The fix path requires `100vh`, not `100%`, for that edge-to-edge root.
- Check auth/session persistence assumptions. iOS Home Screen PWAs have isolated localStorage, IndexedDB, Cache API, and service-worker storage from Safari; cookies are copied at install and then diverge.

Hard fix:

- Use root CSS variables for safe-area top/bottom, bottom chrome height, bottom chrome offset, and reserved scroll space.
- Add `@media (display-mode: standalone)` and iOS `navigator.standalone`/root-class detection where CSS needs it.
- Default to omitting `apple-mobile-web-app-status-bar-style` or leaving it as `default`. Use manifest `display: standalone`, `background_color`, page background, and shared shell tokens before reaching for `black-translucent`.
- If true portrait rendering behind the iOS status bar is required, keep `black-translucent` only with `viewport-fit=cover` and root/full-screen shell `height: 100vh`; do not use root `height: 100%`.
- Use cookies for auth tokens that must survive the Safari-to-installed-PWA transition; do not rely on localStorage/sessionStorage for install carryover.
- Do not add page-only spacers to hide a gap.
- Verify real Home Screen mode, not only mobile Safari.

Scanner rules:

- `ios-standalone-meta-evidence-missing`
- `theme-color-meta-evidence-missing`
- `apple-status-bar-without-standalone-meta`
- `ios-black-translucent-edge-to-edge-audit-required`
- `ios-black-translucent-root-100-percent-chin-gap-risk`
- `ios-black-translucent-height-evidence-missing`
- `ios-installed-auth-storage-isolation-risk`
- bottom-nav rules from `references/07-bottom-nav-pwa-safe-area.md`

## Scope And External Link Handling

Common symptoms:

- External links open inside the installed app.
- App suddenly shows a browser URL bar inside the PWA window.
- Auth redirects kick the user out of standalone mode.
- Deep links open in the browser instead of the installed app.

Hard audit:

- Manifest `scope` is explicit and includes every in-app route.
- `start_url` is inside scope.
- Auth callback and SSO routes are inside scope or have an intentional return path.
- External links use the app's chosen policy: stay in app, open a custom tab, or present a warning.
- `target="_blank"` links have `rel="noopener"`.

Hard fix:

- Fix `scope`, not just link attributes.
- Put redirect/callback routes under app scope when they must remain standalone.
- For true external links, use `target="_blank" rel="noopener"` and test Android/iOS behaviour because browsers differ.
- Add a visible interstitial when the app cannot control the external-link container.

Scanner rules:

- `manifest-start-url-out-of-scope`
- `target-blank-without-noopener`

## Push Notifications

Common symptoms:

- Push works on Android but not iOS.
- Permission dialog never appears.
- Notification arrives but tapping it opens the wrong route.
- Push subscription works in Safari tab but not Home Screen app.

Hard audit:

- iOS push is gated to Home Screen installed mode on supported iOS versions.
- `Notification.requestPermission()` happens from a user gesture.
- Service worker has `push` and `notificationclick` handlers.
- Subscription includes VAPID/application server key where required.
- Backend stores endpoint, keys, expiration, and platform details.
- Notification click uses `clients.matchAll`, `client.focus`, and `clients.openWindow` with in-scope URLs.

Hard fix:

- Gate push setup by capability, permission state, display mode, and install state.
- Ask permission only in a click/tap path.
- Add a `notificationclick` route handler and close the notification.
- Add a visible fallback channel when push is unavailable.

Scanner rules:

- `notification-permission-without-user-gesture-evidence`
- `push-permission-flow-evidence-missing`
- `push-event-handler-evidence-missing`
- `notification-click-handler-evidence-missing`
- `push-ios-standalone-gate-evidence-missing`

## Android Hardware Back And SPA History

Common symptoms:

- Android back button exits the app unexpectedly.
- Android back button never exits.
- A modal closes with in-app back but not hardware back.
- History loops or reopens the same route.

Hard audit:

- SPA history writes are paired with `popstate` handling.
- Modals/sheets/routes have a clear back-stack policy.
- The app does not keep re-pushing a sentinel state forever.
- Hardware back is tested on Android installed mode, not only desktop browser history.

Hard fix:

- Model route, modal, sheet, and selection state explicitly in history.
- On `popstate`, close the topmost UI layer first; then route back; then allow exit when history is empty.
- Avoid infinite `pushState` repair loops.

Scanner rules:

- `android-back-history-evidence-missing`

## Camera, File Capture, And Media Resume

Common symptoms:

- iOS camera preview is black after the PWA is backgrounded and reopened.
- File capture works in Safari but not standalone.
- Media stream fails after lock/unlock or app switch.

Hard audit:

- Any `input type=file capture`, `getUserMedia`, or media-device flow has real iOS standalone testing.
- Lifecycle handlers cover `visibilitychange`, `pagehide`, `pageshow`, and focus/resume paths.
- The app can destroy and recreate a stream/input after resume.
- Upload UI handles cancelled capture and zero-byte files.

Hard fix:

- Reinitialize capture state after resume.
- Do not assume a file input can be reused after backgrounding.
- Provide a retry button and safe cleanup of stale media tracks.
- Test browser mode, standalone mode, background/foreground, lock/unlock, and failed permission paths.

Scanner rules:

- `ios-standalone-file-capture-risk`
- `media-capture-resume-evidence-missing`

## Storage, Quota, And Data Loss

Common symptoms:

- Offline data disappears.
- IndexedDB writes fail only on mobile.
- Queue grows forever.
- Users lose drafts after reinstall, storage pressure, or private mode.

Hard audit:

- Storage usage is intentional: IndexedDB, Cache API, localStorage, or sessionStorage.
- Quota is estimated and storage persistence is requested where data matters.
- Offline queues have size limits, retry limits, conflict handling, and user-visible status.
- Auth/session data is separated from cache-repair cleanup.

Hard fix:

- Use IndexedDB for real offline data, not localStorage for critical workflows.
- Call `navigator.storage.estimate()` and request `navigator.storage.persist()` when supported.
- Add queue compaction and a repair/clear-cache path that does not wipe auth or user data accidentally.

Scanner rules:

- `storage-persistence-evidence-missing`
- `offline-mutation-queue-evidence-missing`

## Offline Mutations And Background Sync

Common symptoms:

- App says saved offline but server never receives the change.
- Background sync works on Chrome but not iOS.
- Duplicate orders or duplicate scans appear after reconnect.

Hard audit:

- Mutating requests have idempotency keys.
- Offline outbox stores request body, headers needed for replay, creation time, retry count, and user-visible state.
- Background Sync has a manual retry/online event fallback.
- Server accepts idempotency keys or client operation IDs.

Hard fix:

- Queue mutations explicitly.
- Replay on `online`, app open, and supported sync events.
- Keep server idempotency and client dedupe together.
- Show pending/failed/synced state in the UI.

Scanner rules:

- `background-sync-fallback-evidence-missing`
- `offline-mutation-queue-evidence-missing`

## Share Target And File Handling

Common symptoms:

- App appears in share sheet but opens blank.
- Shared file route works online but not from installed app.
- Shared POST body is ignored.

Hard audit:

- Manifest `share_target` action is inside scope.
- If `method` is POST, service worker and app route handle multipart/form data.
- Shared files have size/type validation and user feedback.
- Launch route works cold and while the app is already open.

Hard fix:

- Keep share target routes in scope.
- Parse shared data in the service worker or app route deliberately.
- Add cold-launch tests from OS share sheet.

Scanner rules:

- `manifest-share-target-without-id`

## Source Leads Used

- web.dev installation prompt: https://web.dev/learn/pwa/installation-prompt
- web.dev service worker update: https://web.dev/learn/pwa/update/
- web.dev service worker lifecycle: https://web.dev/articles/service-worker-lifecycle
- web.dev manifest scope: https://web.dev/articles/add-manifest
- MDN manifest reference: https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/index.html
- MDN scope reference: https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/scope
- MDN share_target reference: https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/share_target
- Apple standalone web app configuration: https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/SafariWebContent/ConfiguringWebApplications/ConfiguringWebApplications.html
- Apple supported meta tags: https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/SafariHTMLRef/Articles/MetaTags.html
- Reddit iOS chin-gap report and toggle test site: https://www.reddit.com/r/PWA/comments/1sdhsbu/pwa_on_ios_fighting_the_chin_gap/
- fozzedout iPhone PWA gotcha guide: https://gist.github.com/fozzedout/5e77925381991a9570151550992baf14
- Stack Overflow black-translucent bottom-gap report: https://stackoverflow.com/questions/59823681/webapp-on-iphone-with-black-translucent-statusbar-viewport-height-seems-to-be-w
- Stack Overflow iOS bottom gap report: https://stackoverflow.com/questions/79902310/ios-pwa-add-to-home-screen-white-gap-below-bottom-navigation-bar-100dvh-does
- Stack Overflow beforeinstallprompt report: https://stackoverflow.com/questions/50762626/pwa-beforeinstallprompt-not-called
- Stack Overflow iOS standalone capture report: https://stackoverflow.com/questions/59254979/ios-standalone-pwa-input-capture
- Stack Overflow Android back-button report: https://stackoverflow.com/questions/47849321/back-button-in-pwa-does-not-close-the-app
- Stack Overflow external-link-in-PWA report: https://stackoverflow.com/questions/77703509/how-do-i-make-an-android-pwa-open-external-links-in-the-actual-browser-not-a-we
- pwa.io iOS push checklist: https://pwa.io/articles/web-push-with-ios-safari-16-4-made-easy

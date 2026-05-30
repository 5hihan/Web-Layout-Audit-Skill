---
name: web-layout-audit
description: Audit, fix and verify cross-platform web, web app and PWA UI code for real-device viewport, safe-area, keyboard, scroll, touch, mandatory button haptics, native-feel, app-like fluid motion, forced PWA updates, performance and accessibility issues. Use this whenever building, reviewing or repairing any website, UI, app shell, mobile layout, PWA, install flow, form, modal, navigation, media, animation or device-specific interaction, especially when converting a web app to feel like a native app.
---

# Cross-Platform Web and PWA Layout Audit Skill

This skill is both auditor, fixer and verifier. It is designed for coding agents that generate or repair websites, web apps and PWAs. It focuses on issues hidden by desktop previews and exposed by real devices, then requires a full verification pass before the work is treated as complete.

Use British spelling. Prefer semantic HTML and vanilla CSS and JavaScript. Never hide layout defects by disabling zoom, focus outlines, scrolling, text selection or browser UI globally.

## Primary references used

Use current primary documentation when applying this skill. Key references include [MDN viewport meta](https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Viewport_meta_element), [MDN CSS env()](https://developer.mozilla.org/en-US/docs/Web/CSS/env), [WebKit iPhone X safe-area guidance](https://webkit.org/blog/7929/designing-websites-for-iphone-x/), [Chrome Android edge-to-edge guidance](https://developer.chrome.com/docs/css-ui/edge-to-edge), [Android WebView edge-to-edge guidance](https://developer.chrome.com/docs/webview/edge-to-edge), [MDN viewport units](https://developer.mozilla.org/en-US/docs/Web/CSS/length), [MDN overscroll-behavior](https://developer.mozilla.org/en-US/docs/Web/CSS/overscroll-behavior), [Chrome overscroll behaviour guidance](https://developer.chrome.com/blog/overscroll-behavior), [MDN manifest](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest), [W3C Web App Manifest](https://www.w3.org/TR/appmanifest/), [Apple web app configuration](https://developer.apple.com/documentation/safari-developer-tools/configuring-web-applications), [MDN Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API), [web.dev service worker lifecycle](https://web.dev/articles/service-worker-lifecycle), [web.dev PWA update guidance](https://web.dev/articles/handling-service-worker-updates), [MDN VirtualKeyboard API](https://developer.mozilla.org/en-US/docs/Web/API/VirtualKeyboard_API), [Chrome viewport resize behaviour from version 108](https://developer.chrome.com/blog/viewport-resize-behavior/), [MDN Vibration API](https://developer.mozilla.org/en-US/docs/Web/API/Vibration_API), [Safari 18.0 release notes](https://developer.apple.com/documentation/safari-release-notes/safari-18-release-notes), [web.dev Core Web Vitals](https://web.dev/articles/vitals), [WCAG 2.2 target size minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html), [Apple Human Interface Guidelines layout](https://developer.apple.com/design/human-interface-guidelines/layout), [Material Design accessibility](https://m2.material.io/design/usability/accessibility.html), [MDN Web Share API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Share_API), [MDN Wake Lock API](https://developer.mozilla.org/en-US/docs/Web/API/Screen_Wake_Lock_API), [MDN Page Visibility API](https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API), [WebKit web push for iOS and iPadOS web apps](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/), [MDN container queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries), [MDN Popover API](https://developer.mozilla.org/en-US/docs/Web/API/Popover_API), [MDN dialog element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog), [MDN CSS anchor positioning](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_anchor_positioning), [MDN img element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img), [MDN font-display](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display), [WebKit Tracking Prevention](https://webkit.org/tracking-prevention/), [MDN storage quotas](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria), [MDN color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme), [MDN forced-colors](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/forced-colors) and [MDN prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion).

## When to use

Use this skill for any of these triggers:

- Building, auditing or fixing a website, web app, mobile UI, responsive UI, app shell or PWA.
- Creating or reviewing headers, bottom navigation, floating action buttons, modals, drawers, sheets, forms, media, carousels or custom scroll containers.
- Using viewport units, safe-area insets, fixed or sticky positioning, keyboard handling, service workers, manifests or install prompts.
- Adding native-feel interaction, haptics, press states, transitions, page transitions, skeleton loaders or optimistic UI.
- Debugging behaviour visible only on iPhone, iPad, Android, foldables, tablets, landscape, split-screen, WebViews, in-app browsers or installed PWAs.
- Reviewing generated UI code before it is considered shippable.

## Operating rules for the auditing agent

1. Treat desktop preview as incomplete evidence.
2. Inspect the actual HTML head, CSS root rules, scroll root, fixed elements, form control sizes, manifest, service worker and install flow.
3. Use semantic HTML and native controls before custom widgets.
4. Prefer feature detection. Use user agent checks only when the platform behaviour has no feature probe.
5. Keep pinch zoom available.
6. Do not globally disable text selection, focus outlines, context menus or scrolling.
7. Test real devices for final verification.
8. Re-check current browser documentation when behaviour is version-dependent.

## Quick-start checklist: top 22 checks before shipping

1. The document has one viewport meta tag with `width=device-width`, `initial-scale=1`, `viewport-fit=cover` and an explicit `interactive-widget` decision.
2. No root app shell uses naked `height: 100vh` or `min-height: 100vh`.
3. Header, bottom navigation, drawers, sheets, FABs and CTAs include `env(safe-area-inset-*)`.
4. PWA standalone mode is tested after actual install.
5. Bottom controls do not overlap the iOS home indicator or Android gesture area.
6. Keyboard opening does not hide the focused input or primary action.
7. Form controls have at least 16px computed font size on iOS.
8. Every enabled button is haptic-bound, and buttons, links and controls have press states and `:focus-visible`.
9. Touch targets are at least 44 by 44 CSS pixels for app controls, with a 24 by 24 CSS pixel hard minimum for WCAG 2.2 AA target size checks.
10. Hover-only UI has a non-hover path.
11. Modal scroll lock preserves iOS scroll position.
12. Custom scroll containers handle anchors, restoration and reduced-motion smooth scrolling.
13. Images have width, height, loading, decoding and fetchpriority where appropriate.
14. Fonts use `font-display: swap`, critical preloads and subsets.
15. Core Web Vitals target LCP under 2.5 seconds, INP under 200 milliseconds and CLS under 0.1.
16. The service worker has versioned caches, offline fallback, an update prompt and a tested force-update path.
17. The manifest has valid `id`, `start_url`, `scope`, icons, maskable icons, shortcuts and display settings.
18. iOS Home Screen metadata, touch icons and startup images exist for targeted devices.
19. Reduced motion, forced colours, dark mode, RTL and reduced data are supported.
20. Tests include a small iPhone, modern iPhone, Android phone, tablet, desktop and installed PWA mode.
21. Motion uses shared app-like timing tokens and only triggers from user intent, navigation, state change or system feedback.
22. Animation performance is verified on low-end mobile, high-refresh devices, tablet, desktop and installed PWA mode without dropped-frame jank or interaction blocking.

# Correction playbook for wrong implementations

Use this section before changing code. The goal is not to make one screenshot look acceptable. The goal is to identify the broken assumption, move the fix to the shared owner, and prove the layout survives different viewport shapes, input modes, display modes and user settings.

## Required correction format

For every defect, write the fix in this order:

1. **Symptom:** what the user can see or do wrong, such as a bottom gap, clipped button, hidden input, double scroll, stale PWA shell or inaccessible menu.
2. **Broken assumption:** the false belief in the implementation, such as "the viewport is rectangular", "100vh is the visible height", "all users have hover", "standalone mode behaves like browser mode" or "a single breakpoint covers tablets".
3. **Wrong implementation:** the exact code shape that caused it.
4. **Correct implementation:** the shared token, semantic element, CSS primitive, JavaScript helper or platform feature that should own the behaviour.
5. **Regression proof:** the minimum device, viewport, display-mode and interaction checks that prove the fix is not only local.

Do not stop after naming an anti-pattern. Explain how to spot it, why it fails, what to replace it with and which devices must be re-tested.

## Wrong implementation breakdown matrix

| Area | Wrong implementation | How to spot it | Why it fails | Correct implementation | Regression proof |
| --- | --- | --- | --- | --- | --- |
| Viewport meta | Duplicate viewport tags, missing `viewport-fit=cover`, or `user-scalable=no`. | Inspect `document.head.querySelectorAll('meta[name="viewport"]')`. Search for `maximum-scale`, `minimum-scale` and `user-scalable`. | Browsers may choose the wrong viewport contract. Zoom restriction hides layout bugs and harms accessibility. | Keep one viewport tag with `width=device-width`, `initial-scale=1`, `viewport-fit=cover` and an explicit `interactive-widget` decision. | Check iPhone Safari, installed iOS PWA, Chrome Android, desktop zoom and 200 percent browser zoom. |
| Root height | App shell uses naked `height: 100vh`, `min-height: 100vh` or JavaScript `window.innerHeight` once on load. | Search for `100vh`, `innerHeight`, `.style.height` and full-screen wrappers. Scroll until mobile browser bars collapse or expand. | Legacy viewport height often tracks the large viewport, not the currently visible area. Static JavaScript values go stale after resize, rotation and keyboard changes. | Use `100svh` for stable shells, `100dvh` for live viewport-aware panels, and measured visual viewport tokens only when the keyboard or browser UI must be followed. | Test URL bar collapse, rotation, split-screen, keyboard open and installed standalone mode. |
| Width and overflow | Layout uses `width: 100vw`, fixed pixel grids, negative margins or off-canvas transforms without overflow discipline. | Run a 320px to 1920px viewport sweep. Check `document.documentElement.scrollWidth > document.documentElement.clientWidth`. | `100vw` can include the scrollbar gutter and fixed tracks cannot absorb narrow, zoomed or translated content. | Use `inline-size: 100%`, `max-inline-size: 100%`, fluid grids, `minmax(0, 1fr)`, wrapping and logical overflow boundaries. | No horizontal scroll at 320px, 360px, 390px, 744px, 1024px, 1366px and 1600px. Repeat at 200 percent zoom. |
| Safe areas | Header, nav, drawer or CTA has hard-coded `top`, `bottom`, padding or spacer values. | Search for `bottom: 16px`, `padding-bottom: 80px`, `margin-bottom`, notch-specific classes and one-off page spacers. Compare browser mode with installed PWA mode. | Device cutouts, home indicators and Android gesture areas vary by device, orientation and display mode. | Define root safe-area tokens with `env(safe-area-inset-*)` and consume them in all edge UI. | Test iPhone notch portrait, iPhone landscape, Android gesture nav, installed PWA and tablet split-screen. |
| Fixed bottom UI | Bottom nav, basket, FAB, cookie bar or checkout CTA is individually offset from the bottom. | Inspect every bottom-pinned component and compare its offset with the content reserved space. Look for page-level padding that only fixes one screen. | Fixed UI and scrollable content drift apart when each component invents its own clearance. | Create shared geometry tokens such as `--bottom-nav-offset`, `--bottom-nav-height`, `--bottom-nav-reserved-height` and `--safe-bottom`. All bottom UI and content padding must consume the same tokens. | Measure visual bottom gap, overlap and content padding in browser mode, standalone mode, keyboard open and landscape. |
| Standalone PWA layout | Browser spacing is reused unchanged in `display-mode: standalone`, or standalone mode gets a page-specific hack. | Force `display-mode: standalone`, inspect `navigator.standalone` on iOS and compare computed bottom offsets with browser mode. | Installed apps can be edge-to-edge and do not always need the same floating offset as browser tabs. Page hacks leave drawers, FABs and nav out of sync. | Add a root standalone class or media-query branch that changes the shared shell variables, then make all dependent components read those variables. | Confirm no bottom gap, no overlap and consistent drawer/FAB/nav clearance in installed iOS and Android PWA modes. |
| Breakpoints | UI is built around device names or a few global `@media (max-width)` rules. | Resize slowly and watch for jumps, empty side gutters, card overflow and text truncation. Search for device-specific widths like `375px`, `414px` and `768px` used as product logic. | Device width is not the same as component space. Tablets, foldables, split-screen and sidebars create widths between expected breakpoints. | Use intrinsic layout, container queries for component shape, media queries for device capabilities and content-driven breakpoints. | Test narrow phone, large phone, tablet portrait, tablet landscape, desktop sidebar, split-screen and ultra-wide. |
| Cards and grids | Grid columns are fixed, cards have fixed heights, and text is clamped to hide overflow. | Enable long names, prices, translated text, dynamic badges and empty states. Check if buttons move or text overlaps. | Real content is uneven. Fixed tracks and hidden overflow make successful data look broken. | Use `minmax()`, `auto-fit`, wrapping text, stable media aspect ratios and aligned action rows. Clamp only when loss of detail is acceptable and there is another path to the full text. | Test longest expected content, empty data, loading skeletons, error states, RTL and 200 percent zoom. |
| Typography | Font size scales with viewport width, headings are oversized inside compact panels, or inputs use 12px to 14px text. | Search for `vw` font sizing, tiny input classes and negative letter spacing. Focus inputs on iOS. | Viewport-scaled text can become unreadable or overflow. iOS zooms small form text. | Use readable rem-based type scales, `font-size: max(16px, 1rem)` for form controls, normal letter spacing and component-appropriate heading sizes. | Test iPhone SE, modern iPhone, desktop, 200 percent zoom, long labels and translated strings. |
| Keyboard handling | Fixed action rows ignore the visual viewport, or a hard-coded keyboard spacer is added. | Focus inputs near the bottom of forms, modals, sheets and checkout flows. Watch the primary action and focused field. | Keyboard geometry differs across iOS, Android, WebViews, display modes and browser versions. | Use `visualViewport` and `navigator.virtualKeyboard` as progressive enhancement, expose `--keyboard-inset-height`, and keep the focused control scrolled into view. | Test iOS Safari, iOS Home Screen, Chrome Android, Samsung Internet and Android WebView where relevant. |
| Scroll root | Body scroll, custom scroll containers and modals all compete. Pull-to-refresh, bounce or nested panels feel inconsistent. | Inspect which element scrolls. Try top and bottom overscroll, anchors, route changes and modal open/close. | Multiple unmanaged scroll roots break restoration, anchors, keyboard avoidance and iOS scroll lock. | Choose the scroll owner deliberately. Use body scroll for documents, one app scroll container for shells and `overscroll-behavior` on nested panels. | Verify route restoration, anchor links, pull-to-refresh, modal close position and reduced-motion smooth scroll. |
| Modal and sheet lock | Modal opens with `body { overflow: hidden; }` only, fixed backdrop is nested under a transformed app root, or focus stays behind the modal. | Scroll halfway, open a modal, close it and compare scroll position. Inspect fixed ancestors for `transform`, `filter`, `contain`, `will-change` and `opacity`. | iOS can keep scrolling the background. Transformed ancestors create fixed containing blocks. Keyboard and screen reader focus can escape. | Use an overlay root under `body`, iOS-safe scroll lock with position restoration, `inert` or focus trapping and semantic `<dialog>` where behaviour fits. | Test iOS scroll position, Android back button, keyboard navigation, VoiceOver, TalkBack and orientation changes. |
| Touch and hover | Controls are 32px, actions appear only on hover, or custom `div` buttons replace native buttons. | Use a coarse pointer, keyboard and screen reader. Inspect target boxes and whether every hover action has a visible non-hover path. | Touch users cannot hover. Small targets cause mistaps. Non-semantic controls lose keyboard and accessibility behaviour. | Use native controls, minimum 44px app targets, 48px on coarse pointers, visible labels where needed, `:focus-visible` and non-hover disclosure paths. | Test touch, mouse, keyboard, VoiceOver rotor or TalkBack local context menu and high zoom. |
| Disabled browser affordances | Global CSS disables selection, callouts, context menus, focus outlines, scrolling or zoom. | Search for `user-select: none`, `-webkit-touch-callout: none`, `outline: none`, `overflow: hidden`, `touch-action: none` and viewport zoom restrictions. | These rules hide symptoms while removing expected browser and accessibility behaviour. | Scope restrictions only to app controls and replace removed affordances with visible, keyboard-accessible alternatives. | Verify text can be copied, focus is visible, pinch zoom works, scroll works and custom gestures do not block browser navigation. |
| Images and media | Images have no intrinsic dimensions, hero is lazy-loaded, all images are high priority or videos omit `playsinline`. | Use Lighthouse, Performance panel and layout shift overlays. Inspect image attributes and network waterfall. | Late dimensions cause CLS. Wrong priority hurts LCP and bandwidth. Mobile video defaults can hijack full-screen playback. | Add `width`, `height`, responsive `srcset`, correct `sizes`, one LCP `fetchpriority="high"`, lazy loading for below-fold media and `playsinline muted` where autoplay is intended. | Check LCP, CLS, slow 4G, reduced data, orientation changes and image crop at all breakpoints. |
| Service worker | Caches are unversioned, update flow reloads immediately, offline fallback is missing or old shell survives deployment. | Deploy a change while the old app is open. Inspect Application panel caches and waiting service worker. | PWAs can keep serving stale shells indefinitely. Forced reload can destroy in-progress user work. | Version caches, clean old caches on activate, show an update prompt, support offline fallback and test update activation. | Verify first install, offline load, new deploy detection, update acceptance, update dismissal and old cache cleanup. |
| Manifest and install | Manifest has no stable `id`, scope mismatch, one non-maskable icon or missing iOS metadata. | Validate manifest in DevTools and check installed icon crop, launch URL and standalone detection. | Install identity, routing and icon rendering differ between Chromium and iOS. | Provide stable `id`, correct `start_url` and `scope`, multiple icons including maskable purpose, shortcuts if useful, theme colour and Apple touch metadata. | Install on Chrome Android, desktop Chromium and iOS Home Screen. Launch from icon, shortcut and deep link. |
| Accessibility and preferences | Reduced motion, forced colours, dark mode, RTL, labels and target sizes are treated as polish after layout is complete. | Toggle OS/browser preferences and run keyboard plus screen reader smoke tests. | These settings change dimensions, colours, motion and navigation paths. They expose real layout and interaction bugs. | Build preference branches into the base design. Use semantic HTML, labels, visible focus, `prefers-reduced-motion`, `forced-colors`, `color-scheme` and logical properties. | Test keyboard, screen reader, forced colours, dark/light, reduced motion, RTL and zoom before shipping. |

## How to spot incorrectly optimised multi-device UI

Incorrectly optimised UI usually passes a desktop preview and fails when the viewport, browser chrome, input method, display mode or content changes. Use these passes in order.

### 1. Static code scan

Search for these signals first:

- `100vh`, `100vw`, fixed `px` heights on shells, fixed card heights and one-off page spacers.
- `bottom:`, `top:`, `padding-bottom`, `padding-top` and `margin-bottom` values on edge UI that do not reference shared tokens or `env()`.
- `overflow: hidden` on `html`, `body` or app roots without a clear scroll owner.
- `user-scalable=no`, `maximum-scale=1`, `outline: none`, global `user-select: none` or global `touch-action: none`.
- Device-name breakpoints, width-only breakpoint logic and hard-coded keyboard spacers.
- Fixed overlays inside ancestors using `transform`, `filter`, `contain`, `perspective`, `will-change`, `opacity` or `isolation`.
- Inputs below 16px, icon-only controls below 44px, hover-only actions and non-semantic clickable elements.

### 2. Geometry probe

Run a small probe in the browser console for every suspect viewport:

```js
({
  innerWidth: window.innerWidth,
  innerHeight: window.innerHeight,
  visualWidth: window.visualViewport?.width,
  visualHeight: window.visualViewport?.height,
  scrollWidth: document.documentElement.scrollWidth,
  clientWidth: document.documentElement.clientWidth,
  hasHorizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
  displayModeStandalone: matchMedia('(display-mode: standalone)').matches,
  iosStandalone: Boolean(navigator.standalone),
  safeBottom: getComputedStyle(document.documentElement).getPropertyValue('--safe-bottom').trim()
}));
```

If the UI looks wrong, capture computed values from the root shell and the broken component. A real fix usually changes the shared contract that both values read from.

### 3. Viewport sweep

Do not jump from mobile to desktop. Sweep through the uncomfortable middle:

- 320px: small iPhone and worst-case narrow content.
- 360px to 412px: common Android and iPhone widths.
- 430px to 480px: large phones and dense forms.
- 600px to 900px: tablets, foldables, sidebars and split-screen.
- 1024px to 1366px: tablets landscape and ordinary laptops.
- 1600px and wider: ultra-wide containment and max-width discipline.

At each width, check for clipped text, horizontal scroll, orphaned actions, excessive empty space, overlapping fixed UI, unreachable controls and jumpy breakpoints.

### 4. Display-mode sweep

Browser mode, installed PWA mode and in-app browser mode are different enough to test separately.

- Browser mode: verify address-bar collapse, pull-to-refresh and scroll restoration.
- Installed PWA mode: verify edge-to-edge safe areas, standalone offsets, launch URL, stale shell handling and bottom controls.
- In-app browser mode: verify constrained height, third-party storage assumptions, share/open-in-browser fallback and blocked install prompts.

If a bottom gap or overlap appears only in standalone mode, treat it as an app-shell geometry defect first. Change the root display-mode variables, then verify every consumer such as nav, drawers, sheets, carts, FABs and page content.

### 5. Input and keyboard sweep

Focus every input that can appear below the fold:

- Search bars in headers.
- Checkout, address and payment fields.
- Inputs inside modals, drawers and bottom sheets.
- Chat boxes, comment boxes and sticky action forms.

The focused input must remain visible, the primary action must remain reachable, the page must not zoom unexpectedly on iOS and dismissing the keyboard must restore the layout.

### 6. Content stress sweep

Optimised layout must survive real data, not placeholder data:

- Long product names, long user names, long addresses and long currency values.
- Empty lists, one item, many items and loading skeletons.
- Error banners, validation messages, discounts, badges and optional metadata.
- Translated labels, RTL text and 200 percent zoom.
- Slow images, missing images and large uploaded media.

If the design depends on perfect copy length, it is not responsive. Fix the layout contract, not the sample data.

## Correction workflow

1. **Reproduce the exact failure state.** Include viewport size, browser, OS, display mode, orientation, zoom level, keyboard state and whether the PWA is installed.
2. **Find the shared owner.** Shell spacing belongs to shell tokens. Keyboard clearance belongs to visual viewport or keyboard tokens. Overlay layering belongs to an overlay root. Component width changes belong to container queries or intrinsic layout.
3. **Remove the local patch.** Page-only padding, device-name branches and hidden overflow usually mask the problem. Replace them with shared variables, semantic structure and platform-aware primitives.
4. **Make every dependent component consume the same contract.** Header, bottom nav, drawers, sheets, FABs, scroll containers and page content must agree on the same safe-area, keyboard and reserved-space values.
5. **Retest adjacent surfaces.** If bottom nav changes, retest drawers, carts, modals and checkout CTAs. If scroll root changes, retest anchors, route restoration, keyboard and modal lock.
6. **Record the regression handles.** Note computed CSS variables, viewport dimensions, scroll metrics, display mode and screenshots or test names that would catch the same class of bug.

## Fix quality gates

A correction is not complete until all applicable statements are true:

- The fix removes or reduces the wrong assumption instead of adding another exception.
- The behaviour is controlled at the lowest shared layer that owns it.
- Desktop, phone, tablet and installed PWA mode still work.
- The keyboard path, touch path, mouse path and keyboard-navigation path are all usable.
- Safe areas, zoom, reduced motion, forced colours and long content remain supported.
- No new global disabling of zoom, focus, scrolling, selection, callout or browser gestures was added.
- The regression check would fail against the old implementation and pass against the corrected implementation.

# Native-app conversion full audit and verification pass

Use this pass when the goal is to make a web app or PWA feel like a native app. It keeps the existing layout audit purpose, then adds install, update, tactile feedback, app-shell and real-device verification gates.

The standard is stricter than "responsive". A converted app must launch reliably, update reliably, keep controls clear of system UI, feel tactile on every button press, handle offline or slow network states, and avoid browser-looking failures such as stale service workers, address-bar jumps, dead hover states, tiny tap targets and form zoom.

## Native-app conversion acceptance criteria

1. **Installed launch works:** the app opens from the icon into the intended route, scope and display mode.
2. **Forced PWA update works:** a new deployed shell is detected, activated and reloaded without leaving the old service worker in control.
3. **Every single enabled button is haptic:** native `<button>`, `input[type="button"]`, `input[type="submit"]`, `input[type="reset"]`, `[role="button"]`, tabs, switches, menu items and app-action links all route through one haptic system.
4. **Every button has visible press feedback:** tactile feedback is paired with `:active`, pressed state, loading state and `:focus-visible`.
5. **Safe areas are correct:** headers, bottom nav, sheets, drawers, FABs, toasts and CTAs respect notches, Dynamic Island, home indicator and Android gesture navigation.
6. **Keyboard behaviour feels native:** focused inputs stay visible, primary actions remain reachable and the keyboard dismissal path restores layout.
7. **Navigation feels app-like:** route changes preserve expected scroll, use native-feeling transitions only when reduced motion allows them, and never expose blank white flashes.
8. **Offline and reconnection states are deliberate:** cached shell, offline fallback, queued actions and network banners are tested.
9. **Accessibility remains native-quality:** semantic controls, labels, target sizes, focus, screen readers, zoom, forced colours, reduced motion and RTL all pass.
10. **Motion feels native, not decorative:** animations are subtle, fluid, interruptible, tied to UX events and never used as page decoration.
11. **Performance meets interaction budgets:** LCP is 2.5 seconds or less, INP is 200 milliseconds or less, CLS is 0.1 or less, and heavy animation does not block taps.

## Full audit sequence

Run these phases in order and record evidence for each one.

| Phase | What to inspect | Required correction if broken | Verification evidence |
| --- | --- | --- | --- |
| 1. App identity | Manifest `id`, `name`, `short_name`, `start_url`, `scope`, icons, maskable icons, theme colours and iOS metadata. | Fix identity and install metadata before polishing UI. | DevTools manifest validation plus installed launch from iOS Home Screen and Chrome Android. |
| 2. Forced update | Service worker version, cache names, waiting worker, `skipWaiting`, `clients.claim`, update checks on launch and foreground. | Add a force-update controller that calls `registration.update()`, activates the waiting worker and reloads once on `controllerchange`. | Deploy a version change, open old PWA, prove the new version takes control after force update. |
| 3. Shell geometry | Root height, scroll owner, safe-area tokens, bottom reserved space, standalone mode class and viewport units. | Move geometry to shared shell variables; remove page-only spacers and guessed offsets. | Computed token values, no bottom gap, no overlap and no horizontal scroll across target devices. |
| 4. Button haptics | All button-like controls, delegated haptic binding, disabled controls, destructive/success patterns and user preference. | Bind all enabled buttons through one central `haptic()` utility and require explicit `data-haptic-off` only with a reason. | Haptic coverage verifier passes and manual taps produce tactile feedback on supported Android devices. |
| 5. Press and gesture feel | `:active`, `:focus-visible`, transitions, long press, swipe, pull-to-refresh, drag snap and loading states. | Add press-state CSS and gesture thresholds. Avoid hover-only interaction. | Touch, mouse, keyboard and screen-reader paths all work without duplicate or missing feedback. |
| 6. App-like motion | Motion tokens, route transitions, modal and sheet choreography, list updates, optimistic feedback, skeletons and reduced-motion branches. | Replace decorative scroll reveals and website-style effects with subtle UX-triggered transitions using transform and opacity. | Motion trigger matrix passes, reduced motion passes, and low-end mobile profiling shows no interaction-blocking animation. |
| 7. Forms and keyboard | iOS input font size, autocomplete, inputmode, visual viewport, bottom action rows and modal forms. | Use 16px form text, semantic input attributes and keyboard inset tokens. | Focus every field on iOS Safari, iOS PWA, Chrome Android and Samsung Internet. |
| 8. Native APIs | Share, clipboard, wake lock, file picker, notifications, page visibility and install prompts. | Use feature detection and secure-context checks; provide fallbacks for unsupported browsers. | Each native API path either works or shows a designed fallback. |
| 9. Offline and storage | Offline page, app shell cache, runtime cache, mutation queue, storage quota and cache cleanup. | Version caches, queue idempotent actions and clean stale caches. | Offline launch, offline route, failed submit, reconnect and storage eviction tests. |
| 10. Accessibility and settings | Keyboard, VoiceOver, TalkBack, target size, labels, zoom, reduced motion, forced colours, dark mode and RTL. | Fix semantics and settings branches before visual sign-off. | Manual assistive-tech smoke plus automated accessibility triage. |
| 11. Performance and release | Core Web Vitals, animation frame budget, network waterfall, cache headers, service worker update, build hash and production URL. | Prioritise LCP, split long tasks, reserve dimensions, avoid layout animation and verify deployed assets. | Lighthouse or WebPageTest plus production smoke with app installed and animation profiling. |

## Force-update PWA requirements

For a native-feel PWA, update handling must not rely on the user manually clearing site data. The app must provide a force-update path for new shell versions and critical fixes.

- Check for updates on first load, app foreground, network reconnection and an explicit "Update now" action.
- Call `registration.update()` before deciding no update exists.
- If `registration.waiting` exists, send `SKIP_WAITING` and reload once after `controllerchange`.
- If an installing worker becomes installed while an old controller exists, activate it through the same force-update path.
- Use versioned cache names and delete old caches during `activate`.
- For QA and broken-cache recovery, provide a hard reset path that unregisters service workers, deletes app caches and reloads. Keep this path out of ordinary user flows unless the app shell is known broken.
- Verify the update path against a real deployed version change, not only local dev.

## Mandatory all-button haptic requirements

Every single enabled button must be haptic-bound. Do not add one-off `onClick={() => haptic()}` calls across the app; use delegated binding or a shared button primitive so coverage cannot drift.

- Bind native `button`, `input[type="button"]`, `input[type="submit"]`, `input[type="reset"]`, `[role="button"]`, `[role="switch"]`, `[role="tab"]`, `[role="menuitem"]`, `summary` and app-action links.
- Trigger on committed user action such as `pointerup`, keyboard activation, successful long-press recognition, drag snap or form submit. Do not trigger on page load, hover, pointermove or every keypress.
- Disabled controls, passive links and decorative elements must not trigger haptics.
- Use named patterns: `light` for primary button taps, `selection` for tabs and secondary buttons, `toggleOn` and `toggleOff` for switches, `success`, `warning`, `error`, `longPress`, `swipe` and `dragSnap` for state changes.
- Respect a user haptic preference and reduced motion, but make the default enabled for app controls on platforms that support vibration.
- iOS Safari does not expose general Taptic Engine control through `navigator.vibrate`; still wire every button through the same haptic API so supported platforms vibrate and unsupported platforms get the paired visual press state or opt-in audio cue.
- Require `data-haptic-off` only for a documented exception, such as a disabled-looking passive element or a native control that already produces platform feedback.

## App-like motion requirements

App-like motion must feel useful, fast and restrained. It should explain state change, preserve spatial continuity and confirm user intent. It must not behave like a marketing website with scroll reveals, parallax decoration, oversized easing, long delays or animation that plays without user context.

Rules:

- Motion must trigger from UX: tap, press, route change, sheet open, modal close, tab switch, list insert, list remove, drag snap, refresh, successful save, warning, error, loading completion or offline/reconnect state.
- Motion must be subtle by default: small distance, short duration, no bounce unless the product has a clear native platform reason.
- Motion must be interruptible. A second tap, back gesture, route change, modal close or keyboard open must not wait for a long animation to finish.
- Use shared tokens for duration, easing, distance and opacity so the app feels consistent.
- Prefer `transform` and `opacity`. Avoid animating `height`, `width`, `top`, `left`, `right`, `bottom`, `margin`, `padding`, `box-shadow`, `filter`, `backdrop-filter` and large paint-heavy gradients.
- Keep `will-change` temporary and scoped. Remove it after the animation or use it only through a short-lived class.
- Disable meaningful motion under `prefers-reduced-motion: reduce`. Keep instant state changes, focus movement and non-motion feedback.
- Respect `prefers-reduced-data`, low-end devices and battery constraints by disabling non-essential animation, video backgrounds, parallax and large transitions.
- Keep loading motion calm: skeletons may pulse lightly, but shimmer must stop under reduced motion and must not animate large surfaces.
- Pair motion with haptics and press states, but avoid duplicate feedback. A button press should feel immediate before a route or modal transition starts.

## App-like motion trigger matrix

| UX event | Native-feel motion | Duration target | Performance rule | Reduced-motion fallback |
| --- | --- | --- | --- | --- |
| Button press | Scale to 0.96 to 0.98, slight colour state, haptic | 80 to 140 ms | Transform only | Colour or opacity state only |
| Tab switch | Selected indicator glides, content cross-fades or slides 8px | 140 to 220 ms | One moving indicator, no layout thrash | Instant selected state |
| Route push | New route enters from 8px to 16px forward direction or uses View Transition | 180 to 260 ms | Transform and opacity; no full-page blur | Instant navigation |
| Route back | Reverse route direction, preserve scroll where expected | 160 to 220 ms | Same layer count as push | Instant navigation |
| Modal open | Fade backdrop, surface scales from 0.98 or slides from anchor | 160 to 220 ms | Overlay root, transform opacity | Instant open with focus placement |
| Bottom sheet open | Sheet slides from bottom with safe-area-aware final position | 180 to 260 ms | Transform only, no `bottom` animation | Instant final position |
| Drawer open | Drawer translates from edge, content dim is light | 180 to 240 ms | Transform only; avoid broad blur | Instant open |
| List insert | New item fades and translates 6px, existing items use FLIP | 140 to 220 ms | Measure once, transform only | Instant insert |
| List remove | Item fades and collapses after transform or is removed after exit | 120 to 180 ms | Avoid animating height on long lists | Instant remove |
| Drag snap | Element settles to snap point, haptic at snap only | 100 to 180 ms | Use pointer capture and transform | Instant snap |
| Pull refresh | Indicator follows drag, snaps back or completes | 160 to 240 ms | Use transform tied to drag threshold | Static progress text |
| Save success | Button state changes, toast slides 8px and fades | 140 to 220 ms | No layout shift, reserved toast slot | Instant toast |
| Error | Field outline and summary appear without shaking the whole page | 120 to 180 ms | No repeated attention animation | Static error and focus |
| Offline or reconnect | Banner enters from top or bottom safe area | 160 to 220 ms | Reserved inset and transform | Instant banner |
| Skeleton loading | Reserved layout pulse only | 800 to 1400 ms loop | Opacity only, low contrast delta | Static placeholder |

## Motion optimisation for all devices

Test motion on the slowest supported device, not only a desktop simulator. Native-feel motion is allowed only when it stays responsive.

- **Small phones:** keep distances short, avoid vertical stacking shifts, keep bottom controls reachable and test keyboard-open transitions.
- **Large phones:** verify one-handed bottom sheets, gesture navigation, Dynamic Island or notch and route transitions from bottom navigation.
- **Android compact and WebView:** test gesture nav, low-memory mode, `navigator.vibrate`, reduced data and lower refresh devices.
- **iPad and tablets:** avoid phone-style full-screen slides for every route. Prefer split-pane continuity, sheet anchoring and pointer-friendly hover as enhancement only.
- **Foldables:** transition within the active pane or segment. Do not animate across a hinge unless the layout explicitly spans both segments.
- **Desktop:** keep transitions shorter and less spatial than mobile where pointer precision is high. Avoid mobile slide decks on wide layouts.
- **Ultra-wide:** constrain animated content width so route transitions do not sweep across the entire display.
- **Installed PWA:** retest motion after install because standalone mode changes safe areas, status bar, viewport height and browser chrome.
- **Low-end devices:** profile long lists, sheets, maps, media pages and dashboards. Disable non-essential motion if frames are missed.

## Motion performance verification

Every animation pass must produce evidence, not just visual approval.

- Record a Performance trace while tapping buttons, switching tabs, opening sheets, navigating routes and submitting forms.
- No animation should create repeated long tasks over 50 ms.
- Interaction handlers should finish quickly enough that INP stays under 200 ms.
- Animations should stay on compositor-friendly properties whenever possible.
- Layout shift during motion must not count as accidental CLS. Reserve space before loading, inserting or removing content.
- Layer count and memory must stay bounded. Persistent `will-change` on many elements is a failure.
- Animations must not delay route data fetch, service worker update, keyboard focus, form submit or back navigation.
- Test at 1x, 2x browser zoom and 200 percent text zoom where supported.
- Test with `prefers-reduced-motion`, `prefers-reduced-data`, forced colours, dark mode and RTL.
- Test slow 4G and offline/reconnect states so loading motion does not hide blocked network work.

## Motion anti-patterns to correct

| Wrong motion | How to spot it | Why it feels web-like | Correct native-feel motion |
| --- | --- | --- | --- |
| Scroll reveal on every section | Content fades up while reading or scrolling. | Marketing websites animate passive viewing. Apps should react to intent. | Load content in place with reserved skeletons; animate only state changes. |
| Large page slide for every click | Whole app moves 100 percent width for minor route changes. | It feels like a carousel and can disorient users. | Use small directional movement or View Transition only for navigation hierarchy. |
| Long easing over 400 ms | UI waits after tap before becoming usable. | Native controls respond immediately. | Keep ordinary interactions under 260 ms and make state immediate. |
| Bouncy overshoot everywhere | Buttons, sheets and cards all spring aggressively. | Over-styled motion feels playful, not operational. | Use restrained easing and reserve spring-like motion for drag release or snap. |
| Animating layout properties | DevTools shows layout and paint every frame. | Jank breaks the native illusion. | Animate transform and opacity; use FLIP for layout changes. |
| Persistent shimmer | Skeletons shimmer forever or under reduced motion. | It distracts and burns resources. | Use subtle opacity pulse, stop when loaded and disable under reduced motion. |
| Full-screen blur transitions | Large `backdrop-filter` animates during scroll or modal open. | Expensive blur drops frames on mobile. | Use light opacity overlay or static blur only on small surfaces. |
| Motion without haptics | Tap changes view silently. | Native taps usually give tactile or immediate visual response. | Trigger haptic and visual press state before transition. |
| Motion ignores keyboard | Sheet or route transition runs under keyboard. | The app loses spatial stability. | Recompute visual viewport and keyboard inset before moving surfaces. |
| Motion ignores direction | Back navigation uses the same animation as forward navigation. | Navigation hierarchy feels incoherent. | Use forward and backward direction tokens or no motion. |

## Native-app verification report template

Every audit should end with a concise report in this shape:

```md
## Native App Conversion Verification

- App identity and install: pass/fail, evidence.
- Forced PWA update: pass/fail, old version, new version, service worker state, reload behaviour.
- Shell geometry: pass/fail, tested viewports, safe-area token values, overflow result.
- Every-button haptics: pass/fail, selector coverage count, exceptions, manual supported-device result.
- App-like motion: pass/fail, trigger matrix coverage, reduced-motion result, device profiling result.
- Press and gesture feedback: pass/fail, touch, mouse, keyboard and screen reader result.
- Keyboard and forms: pass/fail, tested devices and failure cases.
- Offline and reconnection: pass/fail, cache and queue behaviour.
- Accessibility settings: pass/fail, zoom, reduced motion, forced colours, RTL, VoiceOver/TalkBack.
- Performance: pass/fail, LCP, INP, CLS, animation frame budget, blocking interaction notes.
- Remaining risks: only list real unverified items, not guesses.
```

# Audit checklist as runnable steps

## 1. Viewport meta

**Severity:** critical.

**What to check:** One correct viewport meta tag and no zoom restriction.

**How to check:** Run `document.head.querySelectorAll('meta[name="viewport"]')`. Compare against MDN viewport meta. Confirm no `user-scalable=no`, `maximum-scale=1` or duplicate viewport tags.

**Fix:**

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, interactive-widget=resizes-content">
```

**Why it matters:** `viewport-fit=cover` makes safe areas usable. `interactive-widget` defines keyboard resize intent where supported. Zoom restriction harms users and hides defects.

## 2. Safe-area tokens

**Severity:** critical.

**What to check:** `env(safe-area-inset-*)` appears in edge UI and root variables.

**How to check:** Search CSS. Test notch, Dynamic Island, iOS landscape, Home Screen and Android edge-to-edge. WebKit and MDN document safe-area env variables; Android WebView guidance documents recent M136, M139 and M144 inset changes.

**Fix:**

```css
:root {
  --safe-top: env(safe-area-inset-top, 0px);
  --safe-right: env(safe-area-inset-right, 0px);
  --safe-bottom: env(safe-area-inset-bottom, 0px);
  --safe-left: env(safe-area-inset-left, 0px);
}

.app-header {
  padding-block-start: max(12px, var(--safe-top));
  padding-inline-start: max(16px, var(--safe-left));
  padding-inline-end: max(16px, var(--safe-right));
}

.app-bottom-nav {
  padding-block-end: max(12px, var(--safe-bottom));
  padding-inline-start: max(16px, var(--safe-left));
  padding-inline-end: max(16px, var(--safe-right));
}
```

**Why it matters:** Device screens are not always rectangular and OS gesture areas are interactive.

## 3. Viewport units

**Severity:** critical.

**What to check:** `100vh`, `100vw`, full-screen roots and modals.

**How to check:** On iOS Safari and Chrome Android, scroll until the address bar changes. Watch for jumps, hidden controls and phantom space. MDN documents `svh`, `lvh` and `dvh`.

**Fix:**

```css
.fullscreen-stable {
  min-block-size: 100vh;
  min-block-size: 100svh;
}

.fullscreen-dynamic {
  min-block-size: 100vh;
  min-block-size: 100dvh;
}

.visual-splash {
  min-block-size: 100vh;
  min-block-size: 100lvh;
}

.no-horizontal-overflow {
  inline-size: 100%;
  max-inline-size: 100%;
}
```

**Why it matters:** Legacy `vh` often maps to the large viewport. `100vw` can include scrollbar gutter.

## 4. Fixed bottom UI

**Severity:** critical.

**What to check:** Bottom nav, cookie bars, checkout CTAs, FABs and input toolbars.

**How to check:** Install on iOS and tap controls near the home indicator. Repeat in landscape and on Android gesture navigation.

**Fix:**

```css
.fixed-bottom-surface {
  position: fixed;
  inset-inline: 0;
  inset-block-end: 0;
  z-index: 50;
  padding-block-start: 8px;
  padding-block-end: max(12px, env(safe-area-inset-bottom, 0px));
  padding-inline-start: max(16px, env(safe-area-inset-left, 0px));
  padding-inline-end: max(16px, env(safe-area-inset-right, 0px));
  background: Canvas;
}

.main-with-fixed-bottom {
  padding-block-end: calc(72px + env(safe-area-inset-bottom, 0px));
}
```

**Why it matters:** Bottom gesture areas compete with app controls.

## 5. Keyboard and focused controls

**Severity:** critical.

**What to check:** Inputs near screen bottom, modal forms and fixed action rows.

**How to check:** Focus every field on iOS Safari, iOS Home Screen, Chrome Android and Samsung Internet. Chrome 108 changed Android keyboard resize behaviour to align more closely with Safari by resizing the visual viewport.

**Fix:**

```js
(function initialiseKeyboardInsets() {
  const root = document.documentElement;

  function setKeyboardInsets() {
    const visualViewport = window.visualViewport;
    const viewportHeight = visualViewport ? visualViewport.height : window.innerHeight;
    const viewportTop = visualViewport ? visualViewport.offsetTop : 0;
    const keyboardHeight = Math.max(0, window.innerHeight - viewportHeight - viewportTop);

    root.style.setProperty('--visual-viewport-height', `${viewportHeight}px`);
    root.style.setProperty('--keyboard-inset-height', `${keyboardHeight}px`);
    root.classList.toggle('keyboard-open', keyboardHeight > 80);
  }

  if ('virtualKeyboard' in navigator) {
    navigator.virtualKeyboard.overlaysContent = false;
  }

  setKeyboardInsets();
  window.addEventListener('resize', setKeyboardInsets, { passive: true });

  if (window.visualViewport) {
    window.visualViewport.addEventListener('resize', setKeyboardInsets, { passive: true });
    window.visualViewport.addEventListener('scroll', setKeyboardInsets, { passive: true });
  }
}());
```

```css
.keyboard-aware-action-row {
  inset-block-end: max(env(safe-area-inset-bottom, 0px), var(--keyboard-inset-height, 0px));
}
```

**Why it matters:** Keyboard geometry is platform-specific. Fixed action rows often hide behind keyboards.

## 6. iOS input zoom

**Severity:** high.

**What to check:** Text, search, email, URL, password, number and textarea controls have computed font size of at least 16px on iOS.

**How to check:** Focus controls in iPhone Safari. If the page zooms, inspect computed font size.

**Fix:**

```css
input,
select,
textarea,
button {
  font: inherit;
}

input,
select,
textarea {
  font-size: max(16px, 1rem);
}
```

**Why it matters:** The correct fix is readable text. Do not disable zoom.

## 7. Scroll root and pull-to-refresh

**Severity:** high.

**What to check:** Body scroll, custom app scrollers and nested panels.

**How to check:** Overscroll top and bottom on iOS. Pull down at top on Chrome Android. Check `overscroll-behavior`.

**Fix:**

```css
html {
  min-block-size: 100%;
  overscroll-behavior-y: none;
}

body {
  min-block-size: 100%;
  margin: 0;
  overscroll-behavior-y: none;
}

.app-shell {
  min-block-size: 100svh;
  overflow: clip;
}

.app-main-scroll {
  overflow: auto;
  overscroll-behavior: contain;
  -webkit-overflow-scrolling: touch;
}
```

**Why it matters:** Uncontrolled bounce makes app shells feel loose and can trigger unintended refresh.

## 8. Modal scroll lock

**Severity:** high.

**What to check:** Opening a modal does not jump the page or allow background scroll.

**How to check:** Scroll halfway down on iOS, open modal, close it and verify exact scroll position.

**Fix:** Use the iOS-safe modal scroll lock pattern in the code library.

**Why it matters:** `body { overflow: hidden; }` alone is unreliable on iOS.

## 9. Touch targets and pointer media

**Severity:** high.

**What to check:** Buttons, icon buttons, checkboxes, chips and drag handles.

**How to check:** Physical tapping plus accessibility overlays. Compare Apple 44pt, Android 48dp and WCAG 2.2 24 CSS px target guidance.

**Fix:**

```css
:where(button, [role="button"], a[href], input, select, textarea, summary) {
  touch-action: manipulation;
}

.touch-target {
  min-inline-size: 44px;
  min-block-size: 44px;
}

@media (pointer: coarse) {
  .touch-target {
    min-inline-size: 48px;
    min-block-size: 48px;
  }
}

@media (hover: hover) and (pointer: fine) {
  .hover-only-enhancement:hover {
    text-decoration-thickness: 0.12em;
  }
}
```

**Why it matters:** Mistaps and hover-only controls are common mobile failures.

## 10. Long-press, callout and selection

**Severity:** medium.

**What to check:** Long-press buttons, icon links, images and draggable handles.

**How to check:** Long-press on iOS Safari. Ensure readable content remains selectable.

**Fix:**

```css
.app-control,
button,
[role="button"],
.draggable-handle {
  -webkit-user-select: none;
  user-select: none;
  -webkit-touch-callout: none;
}

.copyable,
.article-content,
textarea,
input {
  -webkit-user-select: text;
  user-select: text;
  -webkit-touch-callout: default;
}
```

**Why it matters:** Controls should feel app-like, but content must remain copyable.

## 11. Fixed, sticky and stacking contexts

**Severity:** high.

**What to check:** Fixed overlays inside ancestors with `transform`, `filter`, `perspective`, `contain`, `will-change`, `opacity` or `isolation`.

**How to check:** Inspect every ancestor of fixed UI. MDN documents stacking contexts and fixed containing blocks.

**Fix:**

```html
<body>
  <div id="app-root"></div>
  <div id="overlay-root"></div>
</body>
```

```css
#overlay-root {
  position: relative;
  z-index: 2147483647;
}

.modal-backdrop {
  position: fixed;
  inset: 0;
}
```

**Why it matters:** Transformed ancestors can make fixed positioning ancestor-relative.

## 12. PWA manifest

**Severity:** high.

**What to check:** `id`, `start_url`, `scope`, icons, maskable icons, display, display_override, shortcuts and advanced handlers.

**How to check:** Use DevTools Application panel and Lighthouse. Validate against MDN and W3C manifest docs.

**Fix:** Use the complete manifest pattern.

**Why it matters:** Scope and identity errors break install, routing and deep links.

## 13. Service worker update flow

**Severity:** high.

**What to check:** Cache versioning, offline fallback, waiting worker, update prompt and force-update path.

**How to check:** Deploy a new version while the old PWA remains open. Reopen the installed PWA, trigger an explicit update check, background and foreground the app, and verify the new worker activates.

**Fix:** Use the service worker, update prompt and force-update patterns. Version caches, call `registration.update()`, send `SKIP_WAITING` to a waiting worker, call `clients.claim()` during activate and reload once on `controllerchange`.

**Why it matters:** A stale service worker can serve an old shell indefinitely. Native apps do not require users to manually clear browser storage to receive critical shell fixes.

## 14. Install UX

**Severity:** medium.

**What to check:** Chrome install prompt, iOS manual install instructions and installed-state detection.

**How to check:** Test Chrome Android, desktop Chromium and iOS Safari. MDN marks `beforeinstallprompt` as non-baseline.

**Fix:** Use both install UI patterns.

**Why it matters:** iOS does not expose the same install prompt API as Chromium.

## 15. Images, fonts and Core Web Vitals

**Severity:** high.

**What to check:** Image dimensions, hero priority, lazy loading, font-display and reserved layout space.

**How to check:** DevTools, Lighthouse, WebPageTest and field data. web.dev defines good Core Web Vitals as LCP 2.5 seconds or less, INP 200 milliseconds or less and CLS 0.1 or less.

**Fix:**

```html
<link rel="preload" href="/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/images/hero-1280.avif" as="image" imagesrcset="/images/hero-768.avif 768w, /images/hero-1280.avif 1280w, /images/hero-1920.avif 1920w" imagesizes="100vw">

<img
  src="/images/hero-1280.avif"
  srcset="/images/hero-768.avif 768w, /images/hero-1280.avif 1280w, /images/hero-1920.avif 1920w"
  sizes="100vw"
  width="1280"
  height="720"
  alt="Product dashboard overview"
  fetchpriority="high"
  decoding="async">
```

```css
@font-face {
  font-family: "Inter Variable";
  src: url("/fonts/inter-var.woff2") format("woff2");
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}
```

**Why it matters:** Missing dimensions, late fonts and late hero resources harm LCP and CLS.

## 16. Haptics and native-feel feedback

**Severity:** medium.

**What to check:** Every enabled button and app action has haptic binding plus visible press feedback. Include native `button`, input buttons, `[role="button"]`, switches, tabs, menu items, summaries, app-action links, toggles, gestures, refresh, drag snap, success, warning and error feedback.

**How to check:** Run the haptic coverage verifier, then physically tap controls on Android where `navigator.vibrate()` is available. On iOS Safari, use fallback policy because general Vibration API support is absent, while Safari 18 adds system haptics for checkbox switches.

**Fix:** Use the haptic utility, every-button auto-binding, haptic coverage verifier, preference toggle, press state and audio fallback patterns.

**Why it matters:** Native-feel interaction needs coordinated visual, tactile and optional audio feedback. A single silent button makes the PWA feel like a web page again.

## 17. Accessibility baseline

**Severity:** critical.

**What to check:** Keyboard navigation, focus visibility, modal focus trap, reduced motion, forced colours, target size, labels and roles.

**How to check:** Test keyboard only, VoiceOver on iOS and TalkBack on Android. Use automated checks as triage.

**Fix:** Use skip link, focus trap, modern reset and the accessibility checklist.

**Why it matters:** A UI that excludes keyboard or assistive technology users is not shippable.

## 18. Form factors

**Severity:** high.

**What to check:** Small phones, large phones, tablets, foldables, landscape, split-screen, desktop, ultra-wide and TV.

**How to check:** Test real devices and foldable emulators. Use viewport segment variables where supported.

**Fix:**

```css
.card-grid {
  container-type: inline-size;
  display: grid;
  gap: 16px;
  grid-template-columns: 1fr;
}

@container (min-width: 560px) {
  .card-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@container (min-width: 920px) {
  .card-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (horizontal-viewport-segments: 2) {
  .foldable-master-detail {
    display: grid;
    grid-template-columns:
      env(viewport-segment-width 0 0)
      env(viewport-segment-width 1 0);
    column-gap: env(viewport-segment-right 0 0);
  }
}
```

**Why it matters:** Hard-coded breakpoints fail on resizable and hinged screens.

## 19. Theming and system integration

**Severity:** medium.

**What to check:** Dark mode, native controls, status bar, selection, caret, scrollbars, forced colours and reduced transparency.

**How to check:** Toggle system settings and inspect browser UI.

**Fix:**

```html
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0b0f19" media="(prefers-color-scheme: dark)">
<meta name="color-scheme" content="light dark">
```

```css
:root {
  color-scheme: light dark;
  accent-color: #2563eb;
  caret-color: #2563eb;
}

::selection {
  background: color-mix(in srgb, Highlight 70%, transparent);
  color: HighlightText;
}

@media (prefers-reduced-transparency: reduce) {
  .frosted {
    backdrop-filter: none;
    background: Canvas;
  }
}

@media (forced-colors: active) {
  .button {
    border: 1px solid ButtonText;
    forced-color-adjust: auto;
  }
}
```

**Why it matters:** Native UI should match system preferences.

## 20. Storage, privacy and offline resilience

**Severity:** medium.

**What to check:** App state, offline queues, storage quota, embedded contexts, in-app browsers and standalone analytics.

**How to check:** Disable network, clear storage and test Safari, Chrome, WebViews and in-app browsers.

**Fix:** Use first-party storage, IndexedDB for structured data, OPFS for large app-owned files where available, versioned migrations and network status UI.

**Why it matters:** Storage and cookies vary across standalone, embedded and browser contexts.

# Code patterns library

## Correct viewport meta tag

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, interactive-widget=resizes-content">
```

Use `interactive-widget=resizes-content` when layout should shrink as the keyboard appears. Use `resizes-visual` when the layout viewport should remain stable. Use `overlays-content` only with a deliberate keyboard avoidance strategy.

## Full iOS meta and link tags including startup images

Apple-specific tags are ignored by most other platforms. iOS startup images require exact media-query assets. This set covers common full-screen iPhone and iPad portrait and landscape sizes, including current Apple Human Interface Guidelines point sizes such as iPhone 17 Pro Max 440 by 956 pt, iPhone 17 Pro 402 by 874 pt, iPhone Air 420 by 912 pt and iPad Pro 11 inch M4 834 by 1210 pt. Regenerate it when Apple adds device dimensions or when the app supports Stage Manager and split-screen windows.

```html
<link rel="manifest" href="/manifest.webmanifest">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, interactive-widget=resizes-content">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0b0f19" media="(prefers-color-scheme: dark)">
<meta name="color-scheme" content="light dark">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="application-name" content="Example App">
<meta name="apple-mobile-web-app-title" content="Example App">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="apple-touch-icon" sizes="120x120" href="/ios/icons/apple-touch-icon-120.png">
<link rel="apple-touch-icon" sizes="152x152" href="/ios/icons/apple-touch-icon-152.png">
<link rel="apple-touch-icon" sizes="167x167" href="/ios/icons/apple-touch-icon-167.png">
<link rel="apple-touch-icon" sizes="180x180" href="/ios/icons/apple-touch-icon-180.png">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-se-portrait-640x1136.png" media="screen and (device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-se-landscape-1136x640.png" media="screen and (device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2) and (orientation: landscape)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-8-portrait-750x1334.png" media="screen and (device-width: 375px) and (device-height: 667px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-8-landscape-1334x750.png" media="screen and (device-width: 375px) and (device-height: 667px) and (-webkit-device-pixel-ratio: 2) and (orientation: landscape)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-8-plus-portrait-1242x2208.png" media="screen and (device-width: 414px) and (device-height: 736px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-8-plus-landscape-2208x1242.png" media="screen and (device-width: 414px) and (device-height: 736px) and (-webkit-device-pixel-ratio: 3) and (orientation: landscape)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-x-portrait-1125x2436.png" media="screen and (device-width: 375px) and (device-height: 812px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-x-landscape-2436x1125.png" media="screen and (device-width: 375px) and (device-height: 812px) and (-webkit-device-pixel-ratio: 3) and (orientation: landscape)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-xr-portrait-828x1792.png" media="screen and (device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-xr-landscape-1792x828.png" media="screen and (device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 2) and (orientation: landscape)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-xs-max-portrait-1242x2688.png" media="screen and (device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-xs-max-landscape-2688x1242.png" media="screen and (device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 3) and (orientation: landscape)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-12-mini-portrait-1080x2340.png" media="screen and (device-width: 360px) and (device-height: 780px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-12-mini-landscape-2340x1080.png" media="screen and (device-width: 360px) and (device-height: 780px) and (-webkit-device-pixel-ratio: 3) and (orientation: landscape)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-13-14-15-portrait-1170x2532.png" media="screen and (device-width: 390px) and (device-height: 844px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-13-14-15-landscape-2532x1170.png" media="screen and (device-width: 390px) and (device-height: 844px) and (-webkit-device-pixel-ratio: 3) and (orientation: landscape)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-14-pro-portrait-1179x2556.png" media="screen and (device-width: 393px) and (device-height: 852px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-14-pro-landscape-2556x1179.png" media="screen and (device-width: 393px) and (device-height: 852px) and (-webkit-device-pixel-ratio: 3) and (orientation: landscape)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-14-plus-portrait-1284x2778.png" media="screen and (device-width: 428px) and (device-height: 926px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-14-plus-landscape-2778x1284.png" media="screen and (device-width: 428px) and (device-height: 926px) and (-webkit-device-pixel-ratio: 3) and (orientation: landscape)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-15-pro-max-portrait-1290x2796.png" media="screen and (device-width: 430px) and (device-height: 932px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-15-pro-max-landscape-2796x1290.png" media="screen and (device-width: 430px) and (device-height: 932px) and (-webkit-device-pixel-ratio: 3) and (orientation: landscape)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-16-pro-portrait-1206x2622.png" media="screen and (device-width: 402px) and (device-height: 874px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-16-pro-landscape-2622x1206.png" media="screen and (device-width: 402px) and (device-height: 874px) and (-webkit-device-pixel-ratio: 3) and (orientation: landscape)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-16-pro-max-portrait-1320x2868.png" media="screen and (device-width: 440px) and (device-height: 956px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-16-pro-max-landscape-2868x1320.png" media="screen and (device-width: 440px) and (device-height: 956px) and (-webkit-device-pixel-ratio: 3) and (orientation: landscape)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-air-portrait-1260x2736.png" media="screen and (device-width: 420px) and (device-height: 912px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/iphone-air-landscape-2736x1260.png" media="screen and (device-width: 420px) and (device-height: 912px) and (-webkit-device-pixel-ratio: 3) and (orientation: landscape)">
<link rel="apple-touch-startup-image" href="/ios/splash/ipad-pro-11-m4-portrait-1668x2420.png" media="screen and (device-width: 834px) and (device-height: 1210px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/ipad-pro-11-m4-landscape-2420x1668.png" media="screen and (device-width: 834px) and (device-height: 1210px) and (-webkit-device-pixel-ratio: 2) and (orientation: landscape)">
<link rel="apple-touch-startup-image" href="/ios/splash/ipad-mini-portrait-1488x2266.png" media="screen and (device-width: 744px) and (device-height: 1133px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/ipad-mini-landscape-2266x1488.png" media="screen and (device-width: 744px) and (device-height: 1133px) and (-webkit-device-pixel-ratio: 2) and (orientation: landscape)">
<link rel="apple-touch-startup-image" href="/ios/splash/ipad-9-7-portrait-1536x2048.png" media="screen and (device-width: 768px) and (device-height: 1024px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/ipad-9-7-landscape-2048x1536.png" media="screen and (device-width: 768px) and (device-height: 1024px) and (-webkit-device-pixel-ratio: 2) and (orientation: landscape)">
<link rel="apple-touch-startup-image" href="/ios/splash/ipad-10-2-portrait-1620x2160.png" media="screen and (device-width: 810px) and (device-height: 1080px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/ipad-10-2-landscape-2160x1620.png" media="screen and (device-width: 810px) and (device-height: 1080px) and (-webkit-device-pixel-ratio: 2) and (orientation: landscape)">
<link rel="apple-touch-startup-image" href="/ios/splash/ipad-air-portrait-1640x2360.png" media="screen and (device-width: 820px) and (device-height: 1180px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/ipad-air-landscape-2360x1640.png" media="screen and (device-width: 820px) and (device-height: 1180px) and (-webkit-device-pixel-ratio: 2) and (orientation: landscape)">
<link rel="apple-touch-startup-image" href="/ios/splash/ipad-pro-10-5-portrait-1668x2224.png" media="screen and (device-width: 834px) and (device-height: 1112px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/ipad-pro-10-5-landscape-2224x1668.png" media="screen and (device-width: 834px) and (device-height: 1112px) and (-webkit-device-pixel-ratio: 2) and (orientation: landscape)">
<link rel="apple-touch-startup-image" href="/ios/splash/ipad-pro-11-portrait-1668x2388.png" media="screen and (device-width: 834px) and (device-height: 1194px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/ipad-pro-11-landscape-2388x1668.png" media="screen and (device-width: 834px) and (device-height: 1194px) and (-webkit-device-pixel-ratio: 2) and (orientation: landscape)">
<link rel="apple-touch-startup-image" href="/ios/splash/ipad-pro-12-9-portrait-2048x2732.png" media="screen and (device-width: 1024px) and (device-height: 1366px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/ipad-pro-12-9-landscape-2732x2048.png" media="screen and (device-width: 1024px) and (device-height: 1366px) and (-webkit-device-pixel-ratio: 2) and (orientation: landscape)">
<link rel="apple-touch-startup-image" href="/ios/splash/ipad-pro-13-portrait-2064x2752.png" media="screen and (device-width: 1032px) and (device-height: 1376px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="/ios/splash/ipad-pro-13-landscape-2752x2064.png" media="screen and (device-width: 1032px) and (device-height: 1376px) and (-webkit-device-pixel-ratio: 2) and (orientation: landscape)">
```

## Complete PWA manifest

`display_override`, `file_handlers`, `protocol_handlers`, `launch_handler` and `scope_extensions` have partial or experimental support. Browsers ignore unknown manifest members.

```json
{
  "id": "/?appId=example-app",
  "name": "Example App",
  "short_name": "Example",
  "description": "A cross-platform progressive web app with safe-area, install, share and offline support.",
  "lang": "en-GB",
  "dir": "ltr",
  "start_url": "/?source=pwa",
  "scope": "/",
  "scope_extensions": [
    {
      "origin": "https://assets.example.test"
    }
  ],
  "display": "standalone",
  "display_override": [
    "window-controls-overlay",
    "standalone",
    "minimal-ui",
    "browser"
  ],
  "orientation": "any",
  "background_color": "#0b0f19",
  "theme_color": "#0b0f19",
  "categories": [
    "productivity",
    "utilities"
  ],
  "icons": [
    {
      "src": "/icons/icon-48.png",
      "sizes": "48x48",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-72.png",
      "sizes": "72x72",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-96.png",
      "sizes": "96x96",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-128.png",
      "sizes": "128x128",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-144.png",
      "sizes": "144x144",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-152.png",
      "sizes": "152x152",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-180.png",
      "sizes": "180x180",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/icons/icon-384.png",
      "sizes": "384x384",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/icons/maskable-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "maskable"
    },
    {
      "src": "/icons/maskable-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable"
    }
  ],
  "screenshots": [
    {
      "src": "/screenshots/mobile-home.png",
      "sizes": "1080x1920",
      "type": "image/png",
      "form_factor": "narrow",
      "label": "Home screen on a phone"
    },
    {
      "src": "/screenshots/desktop-home.png",
      "sizes": "1920x1080",
      "type": "image/png",
      "form_factor": "wide",
      "label": "Home screen on desktop"
    }
  ],
  "shortcuts": [
    {
      "name": "New item",
      "short_name": "New",
      "description": "Create a new item",
      "url": "/new?source=shortcut",
      "icons": [
        {
          "src": "/icons/shortcut-new-96.png",
          "sizes": "96x96",
          "type": "image/png"
        }
      ]
    },
    {
      "name": "Search",
      "short_name": "Search",
      "description": "Open app search",
      "url": "/search?source=shortcut",
      "icons": [
        {
          "src": "/icons/shortcut-search-96.png",
          "sizes": "96x96",
          "type": "image/png"
        }
      ]
    }
  ],
  "share_target": {
    "action": "/share-target/",
    "method": "POST",
    "enctype": "multipart/form-data",
    "params": {
      "title": "title",
      "text": "text",
      "url": "url",
      "files": [
        {
          "name": "images",
          "accept": [
            "image/png",
            "image/jpeg",
            "image/webp",
            "image/avif"
          ]
        },
        {
          "name": "documents",
          "accept": [
            "application/pdf",
            "text/plain"
          ]
        }
      ]
    }
  },
  "file_handlers": [
    {
      "action": "/open-file/",
      "accept": {
        "image/png": [
          ".png"
        ],
        "image/jpeg": [
          ".jpg",
          ".jpeg"
        ],
        "text/plain": [
          ".txt"
        ],
        "application/pdf": [
          ".pdf"
        ]
      }
    }
  ],
  "protocol_handlers": [
    {
      "protocol": "web+example",
      "url": "/protocol?url=%s"
    }
  ],
  "launch_handler": {
    "client_mode": [
      "navigate-existing",
      "auto"
    ]
  },
  "prefer_related_applications": false,
  "related_applications": []
}
```

## Service worker template with versioning and update flow

Save as `/service-worker.js`.

```js
const APP_VERSION = '2026-05-06-v1';
const STATIC_CACHE = `static-${APP_VERSION}`;
const RUNTIME_CACHE = `runtime-${APP_VERSION}`;
const IMAGE_CACHE = `images-${APP_VERSION}`;

const PRECACHE_URLS = [
  '/',
  '/index.html',
  '/styles.css',
  '/app.js',
  '/manifest.webmanifest',
  '/offline.html',
  '/icons/icon-192.png',
  '/icons/icon-512.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  const expectedCaches = new Set([STATIC_CACHE, RUNTIME_CACHE, IMAGE_CACHE]);

  event.waitUntil(
    caches.keys()
      .then((cacheNames) => Promise.all(
        cacheNames
          .filter((cacheName) => !expectedCaches.has(cacheName))
          .map((cacheName) => caches.delete(cacheName))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

self.addEventListener('fetch', (event) => {
  const request = event.request;

  if (request.method !== 'GET') {
    return;
  }

  const requestUrl = new URL(request.url);

  if (request.mode === 'navigate') {
    event.respondWith(networkFirstNavigation(request));
    return;
  }

  if (requestUrl.origin === self.location.origin && request.destination === 'image') {
    event.respondWith(cacheFirst(request, IMAGE_CACHE));
    return;
  }

  if (requestUrl.origin === self.location.origin) {
    event.respondWith(staleWhileRevalidate(request, RUNTIME_CACHE));
    return;
  }

  event.respondWith(networkFirst(request, RUNTIME_CACHE));
});

async function networkFirstNavigation(request) {
  try {
    const response = await fetch(request);
    const cache = await caches.open(RUNTIME_CACHE);
    cache.put(request, response.clone());
    return response;
  } catch (error) {
    return await caches.match(request) || await caches.match('/offline.html') || new Response('Offline', {
      status: 503,
      headers: {
        'Content-Type': 'text/plain; charset=utf-8'
      }
    });
  }
}

async function cacheFirst(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);

  if (cached) {
    return cached;
  }

  const response = await fetch(request);
  cache.put(request, response.clone());
  return response;
}

async function staleWhileRevalidate(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  const network = fetch(request)
    .then((response) => {
      cache.put(request, response.clone());
      return response;
    })
    .catch(() => cached);

  return cached || network;
}

async function networkFirst(request, cacheName) {
  const cache = await caches.open(cacheName);

  try {
    const response = await fetch(request);
    cache.put(request, response.clone());
    return response;
  } catch (error) {
    return await cache.match(request) || new Response('Offline', {
      status: 503,
      headers: {
        'Content-Type': 'text/plain; charset=utf-8'
      }
    });
  }
}
```

## Update prompt UI for new service worker available

```html
<div class="sw-update" id="sw-update" hidden>
  <p class="sw-update__text">A new version is available.</p>
  <button class="sw-update__button" id="sw-update-apply" type="button">Update now</button>
  <button class="sw-update__dismiss" id="sw-update-dismiss" type="button" aria-label="Dismiss update notice">Dismiss</button>
</div>

<script>
(function initialiseServiceWorkerUpdatePrompt() {
  if (!('serviceWorker' in navigator)) {
    return;
  }

  const updateBanner = document.getElementById('sw-update');
  const applyButton = document.getElementById('sw-update-apply');
  const dismissButton = document.getElementById('sw-update-dismiss');
  let waitingWorker = null;
  let refreshing = false;

  function showUpdatePrompt(worker) {
    waitingWorker = worker;
    updateBanner.hidden = false;
  }

  navigator.serviceWorker.addEventListener('controllerchange', () => {
    if (refreshing) {
      return;
    }

    refreshing = true;
    window.location.reload();
  });

  navigator.serviceWorker.register('/service-worker.js')
    .then((registration) => {
      if (registration.waiting) {
        showUpdatePrompt(registration.waiting);
      }

      registration.addEventListener('updatefound', () => {
        const installingWorker = registration.installing;

        if (!installingWorker) {
          return;
        }

        installingWorker.addEventListener('statechange', () => {
          if (installingWorker.state === 'installed' && navigator.serviceWorker.controller) {
            showUpdatePrompt(installingWorker);
          }
        });
      });
    })
    .catch((error) => {
      console.error('Service worker registration failed', error);
    });

  applyButton.addEventListener('click', () => {
    if (waitingWorker) {
      waitingWorker.postMessage({ type: 'SKIP_WAITING' });
    }
  });

  dismissButton.addEventListener('click', () => {
    updateBanner.hidden = true;
  });
}());
</script>
```

```css
.sw-update {
  position: fixed;
  inset-inline: max(16px, env(safe-area-inset-left, 0px)) max(16px, env(safe-area-inset-right, 0px));
  inset-block-end: max(16px, env(safe-area-inset-bottom, 0px));
  z-index: 1000;
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 8px;
  align-items: center;
  padding: 12px;
  border: 1px solid CanvasText;
  border-radius: 16px;
  background: Canvas;
  color: CanvasText;
}

.sw-update[hidden] {
  display: none;
}
```

## Force-update PWA controller and hard reset repair path

Use this when the app shell must update like a native app. The controlled path checks for a new worker, activates it and reloads once. The hard reset path is for QA, support tools or a known broken cache state.

```js
(function initialiseForcePwaUpdate(global) {
  if (!('serviceWorker' in navigator)) {
    global.forcePwaUpdate = function forcePwaUpdateWithoutServiceWorker() {
      global.location.reload();
      return Promise.resolve(false);
    };
    return;
  }

  let reloadPending = false;

  function reloadOnce() {
    if (reloadPending) {
      return;
    }

    reloadPending = true;
    global.location.reload();
  }

  function waitForControllerChange(timeoutMs) {
    return new Promise((resolve) => {
      const timeout = global.setTimeout(() => {
        navigator.serviceWorker.removeEventListener('controllerchange', onControllerChange);
        resolve(false);
      }, timeoutMs);

      function onControllerChange() {
        global.clearTimeout(timeout);
        navigator.serviceWorker.removeEventListener('controllerchange', onControllerChange);
        reloadOnce();
        resolve(true);
      }

      navigator.serviceWorker.addEventListener('controllerchange', onControllerChange);
    });
  }

  async function activateWaitingWorker(registration) {
    const waitingWorker = registration.waiting;

    if (!waitingWorker) {
      return false;
    }

    const controllerChanged = waitForControllerChange(8000);
    waitingWorker.postMessage({ type: 'SKIP_WAITING' });
    return controllerChanged;
  }

  async function waitForInstallingWorker(registration) {
    const installingWorker = registration.installing;

    if (!installingWorker) {
      return false;
    }

    return new Promise((resolve) => {
      const timeout = global.setTimeout(() => {
        installingWorker.removeEventListener('statechange', onStateChange);
        resolve(false);
      }, 10000);

      async function onStateChange() {
        if (installingWorker.state === 'installed' && navigator.serviceWorker.controller) {
          global.clearTimeout(timeout);
          installingWorker.removeEventListener('statechange', onStateChange);
          resolve(await activateWaitingWorker(registration));
        }

        if (installingWorker.state === 'redundant' || installingWorker.state === 'activated') {
          global.clearTimeout(timeout);
          installingWorker.removeEventListener('statechange', onStateChange);
          resolve(false);
        }
      }

      installingWorker.addEventListener('statechange', onStateChange);
    });
  }

  async function forcePwaUpdate() {
    const registration = await navigator.serviceWorker.getRegistration();

    if (!registration) {
      reloadOnce();
      return false;
    }

    await registration.update();

    if (await activateWaitingWorker(registration)) {
      return true;
    }

    if (await waitForInstallingWorker(registration)) {
      return true;
    }

    return false;
  }

  async function hardResetPwa() {
    const registrations = await navigator.serviceWorker.getRegistrations();
    await Promise.all(registrations.map((registration) => registration.unregister()));

    if ('caches' in global) {
      const cacheNames = await caches.keys();
      await Promise.all(cacheNames.map((cacheName) => caches.delete(cacheName)));
    }

    global.location.replace(`${global.location.pathname}?pwa-reset=${Date.now()}`);
  }

  global.forcePwaUpdate = forcePwaUpdate;
  global.hardResetPwa = hardResetPwa;

  global.addEventListener('online', () => {
    forcePwaUpdate().catch((error) => {
      console.warn('PWA force update check failed', error);
    });
  }, { passive: true });

  global.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
      forcePwaUpdate().catch((error) => {
        console.warn('PWA foreground update check failed', error);
      });
    }
  });
}(window));
```

Force-update verification:

1. Install the PWA and open a route controlled by the old service worker.
2. Deploy a new version with a changed `APP_VERSION` and visible build marker.
3. Reopen or foreground the installed app.
4. Confirm `registration.update()` runs, the waiting worker receives `SKIP_WAITING`, `controllerchange` fires once and the app reloads into the new build.
5. Confirm old caches are removed and offline launch still works after the update.

## Safe-area-aware app shell

```html
<div class="app-shell">
  <header class="app-header">
    <a class="skip-link" href="#main-content">Skip to content</a>
    <h1 class="app-title">Example App</h1>
  </header>

  <main class="app-main" id="main-content" tabindex="-1">
    <section class="content-card">
      <h2>Home</h2>
      <p>This content scrolls inside the safe app shell.</p>
    </section>
  </main>

  <nav class="app-bottom-nav" aria-label="Primary">
    <a class="app-bottom-nav__item" href="/" aria-current="page">Home</a>
    <a class="app-bottom-nav__item" href="/search">Search</a>
    <a class="app-bottom-nav__item" href="/settings">Settings</a>
  </nav>
</div>
```

```css
:root {
  --safe-top: env(safe-area-inset-top, 0px);
  --safe-right: env(safe-area-inset-right, 0px);
  --safe-bottom: env(safe-area-inset-bottom, 0px);
  --safe-left: env(safe-area-inset-left, 0px);
  --header-size: 56px;
  --bottom-nav-size: 64px;
}

html,
body {
  block-size: 100%;
  margin: 0;
}

body {
  overscroll-behavior-y: none;
}

.app-shell {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr) auto;
  min-block-size: 100vh;
  min-block-size: 100svh;
  overflow: clip;
  background: Canvas;
  color: CanvasText;
}

.app-header {
  position: sticky;
  inset-block-start: 0;
  z-index: 20;
  min-block-size: var(--header-size);
  padding-block-start: max(8px, var(--safe-top));
  padding-block-end: 8px;
  padding-inline-start: max(16px, var(--safe-left));
  padding-inline-end: max(16px, var(--safe-right));
  background: Canvas;
}

.app-main {
  min-block-size: 0;
  overflow: auto;
  overscroll-behavior: contain;
  -webkit-overflow-scrolling: touch;
  scroll-padding-block-start: calc(var(--header-size) + var(--safe-top));
  padding-block: 16px;
  padding-inline-start: max(16px, var(--safe-left));
  padding-inline-end: max(16px, var(--safe-right));
}

.app-bottom-nav {
  position: sticky;
  inset-block-end: 0;
  z-index: 20;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 4px;
  min-block-size: var(--bottom-nav-size);
  padding-block-start: 8px;
  padding-block-end: max(8px, var(--safe-bottom));
  padding-inline-start: max(8px, var(--safe-left));
  padding-inline-end: max(8px, var(--safe-right));
  background: Canvas;
  border-block-start: 1px solid color-mix(in srgb, CanvasText 16%, transparent);
}

.app-bottom-nav__item {
  display: grid;
  place-items: center;
  min-block-size: 44px;
  border-radius: 12px;
  color: inherit;
  text-decoration: none;
  touch-action: manipulation;
}

.app-bottom-nav__item[aria-current="page"] {
  background: color-mix(in srgb, Highlight 16%, transparent);
}
```

## Modern CSS reset handling viewport units, safe areas, overscroll, font size, RTL, reduced motion and forced colours

```css
@layer reset, base, components, utilities;

@layer reset {
  *,
  *::before,
  *::after {
    box-sizing: border-box;
  }

  html {
    min-block-size: 100%;
    -webkit-text-size-adjust: 100%;
    text-size-adjust: 100%;
    color-scheme: light dark;
    scroll-behavior: smooth;
    overflow-wrap: anywhere;
  }

  body {
    min-block-size: 100%;
    margin: 0;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    line-height: 1.5;
    background: Canvas;
    color: CanvasText;
    overscroll-behavior-y: none;
  }

  img,
  picture,
  video,
  canvas,
  svg {
    display: block;
    max-inline-size: 100%;
    block-size: auto;
  }

  button,
  input,
  select,
  textarea {
    font: inherit;
    color: inherit;
  }

  input,
  select,
  textarea {
    font-size: max(16px, 1rem);
  }

  button,
  [role="button"],
  a[href],
  input,
  select,
  textarea,
  summary {
    touch-action: manipulation;
  }

  button {
    cursor: pointer;
  }

  :focus-visible {
    outline: 3px solid Highlight;
    outline-offset: 3px;
  }

  :target {
    scroll-margin-block-start: calc(64px + env(safe-area-inset-top, 0px));
  }

  @media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      scroll-behavior: auto !important;
      transition-duration: 0.01ms !important;
    }
  }

  @media (forced-colors: active) {
    * {
      box-shadow: none !important;
      text-shadow: none !important;
    }
  }
}

@layer base {
  :root {
    --safe-top: env(safe-area-inset-top, 0px);
    --safe-right: env(safe-area-inset-right, 0px);
    --safe-bottom: env(safe-area-inset-bottom, 0px);
    --safe-left: env(safe-area-inset-left, 0px);
    --keyboard-inset-height: env(keyboard-inset-height, 0px);
    accent-color: Highlight;
    caret-color: Highlight;
  }

  [dir="rtl"] {
    direction: rtl;
  }

  ::selection {
    background: Highlight;
    color: HighlightText;
  }
}
```

## Universal haptic utility with named patterns

The Vibration API accepts a duration or a pattern of vibration and pause durations in milliseconds. Unsupported browsers may no-op. iOS Safari does not expose general Taptic Engine control through `navigator.vibrate`; Safari 18 added haptic feedback for checkbox switches.

```js
(function initialiseHaptics(global) {
  const STORAGE_KEY = 'haptics-enabled';

  const patterns = Object.freeze({
    light: [10],
    medium: [20],
    heavy: [35],
    success: [10, 40, 20],
    warning: [20, 60, 20],
    error: [30, 40, 30, 40, 30],
    selection: [8],
    longPress: [45],
    swipe: [12],
    refresh: [15, 50, 15],
    dragSnap: [10, 20, 10],
    toggleOn: [12, 30, 12],
    toggleOff: [12],
    notification: [20, 80, 20],
    impactSoft: [12],
    impactRigid: [28]
  });

  let audioFallbackEnabled = false;
  let audioContext = null;

  function prefersReducedMotion() {
    return global.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function getStoredPreference() {
    try {
      return global.localStorage.getItem(STORAGE_KEY);
    } catch (error) {
      return null;
    }
  }

  function setStoredPreference(value) {
    try {
      global.localStorage.setItem(STORAGE_KEY, value ? 'true' : 'false');
      return true;
    } catch (error) {
      return false;
    }
  }

  function isEnabled() {
    const storedPreference = getStoredPreference();

    if (storedPreference === 'true') {
      return true;
    }

    if (storedPreference === 'false') {
      return false;
    }

    return !prefersReducedMotion();
  }

  function normalisePattern(nameOrPattern) {
    if (Array.isArray(nameOrPattern)) {
      return nameOrPattern.map((value) => Math.max(0, Number(value) || 0));
    }

    if (typeof nameOrPattern === 'number') {
      return [Math.max(0, nameOrPattern)];
    }

    return patterns[nameOrPattern] || patterns.light;
  }

  async function ensureAudioContext() {
    if (audioContext) {
      return audioContext;
    }

    const AudioContextConstructor = global.AudioContext || global.webkitAudioContext;

    if (!AudioContextConstructor) {
      return null;
    }

    audioContext = new AudioContextConstructor();

    if (audioContext.state === 'suspended') {
      await audioContext.resume();
    }

    return audioContext;
  }

  async function playAudioFallback(pattern) {
    if (!audioFallbackEnabled) {
      return false;
    }

    const context = await ensureAudioContext();

    if (!context) {
      return false;
    }

    let cursor = context.currentTime;

    pattern.forEach((duration, index) => {
      if (index % 2 === 1) {
        cursor += duration / 1000;
        return;
      }

      const oscillator = context.createOscillator();
      const gain = context.createGain();

      oscillator.type = 'sine';
      oscillator.frequency.setValueAtTime(88, cursor);
      gain.gain.setValueAtTime(0.0001, cursor);
      gain.gain.exponentialRampToValueAtTime(0.04, cursor + 0.005);
      gain.gain.exponentialRampToValueAtTime(0.0001, cursor + Math.max(0.01, duration / 1000));
      oscillator.connect(gain);
      gain.connect(context.destination);
      oscillator.start(cursor);
      oscillator.stop(cursor + Math.max(0.02, duration / 1000));
      cursor += duration / 1000;
    });

    return true;
  }

  async function haptic(nameOrPattern, options) {
    const settings = Object.assign({ audioFallback: false, force: false }, options || {});
    const pattern = normalisePattern(nameOrPattern);

    if (!settings.force && !isEnabled()) {
      return false;
    }

    if ('vibrate' in navigator && typeof navigator.vibrate === 'function') {
      return navigator.vibrate(pattern);
    }

    if (settings.audioFallback || audioFallbackEnabled) {
      return playAudioFallback(pattern);
    }

    return false;
  }

  function enable() {
    return setStoredPreference(true);
  }

  function disable() {
    if ('vibrate' in navigator && typeof navigator.vibrate === 'function') {
      navigator.vibrate(0);
    }

    return setStoredPreference(false);
  }

  function setAudioFallback(enabled) {
    audioFallbackEnabled = Boolean(enabled);
  }

  global.Haptics = Object.freeze({
    patterns,
    haptic,
    enable,
    disable,
    isEnabled,
    setAudioFallback
  });

  global.haptic = haptic;
}(window));
```

## Auto-binding script for haptics on every button and interactive element

This delegated binder is the preferred default for native-app conversion. It makes every enabled button haptic without scattering haptic calls through feature code. Keep the explicit `data-haptic-off` escape hatch rare and documented.

```js
(function bindHapticsToInteractiveElements() {
  const interactiveSelector = [
    'button',
    '[role="button"]',
    '[role="switch"]',
    '[role="tab"]',
    '[role="menuitem"]',
    'a[href]',
    'summary',
    'input[type="button"]',
    'input[type="submit"]',
    'input[type="reset"]',
    'input[type="checkbox"]',
    'input[type="radio"]',
    '[data-haptic]'
  ].join(',');

  let lastPointerHapticAt = 0;

  function inferHapticName(element) {
    const explicit = element.getAttribute('data-haptic');

    if (explicit) {
      return explicit;
    }

    if (element.matches('input[type="checkbox"], input[type="radio"], [role="switch"]')) {
      return element.matches(':checked, [aria-checked="true"]') ? 'toggleOn' : 'toggleOff';
    }

    if (element.matches('[data-destructive="true"], .is-destructive')) {
      return 'warning';
    }

    if (element.matches('[data-success="true"], .is-success')) {
      return 'success';
    }

    if (element.matches('[data-drag-snap="true"]')) {
      return 'dragSnap';
    }

    return 'selection';
  }

  function shouldSkipHaptic(interactive) {
    return interactive.hasAttribute('disabled') ||
      interactive.getAttribute('aria-disabled') === 'true' ||
      interactive.hasAttribute('data-haptic-off');
  }

  function triggerHaptic(interactive) {
    if (shouldSkipHaptic(interactive)) {
      return;
    }

    if (typeof window.haptic === 'function') {
      window.haptic(inferHapticName(interactive));
    }
  }

  document.addEventListener('pointerup', (event) => {
    const target = event.target instanceof Element ? event.target : null;
    const interactive = target ? target.closest(interactiveSelector) : null;

    if (!interactive) {
      return;
    }

    lastPointerHapticAt = performance.now();
    triggerHaptic(interactive);
  }, { passive: true });

  document.addEventListener('click', (event) => {
    if (performance.now() - lastPointerHapticAt < 250) {
      return;
    }

    const target = event.target instanceof Element ? event.target : null;
    const interactive = target ? target.closest(interactiveSelector) : null;

    if (!interactive) {
      return;
    }

    triggerHaptic(interactive);
  }, true);
}());
```

## Button haptic coverage verifier

Run this in development and QA after the app has rendered. It proves every enabled button-like control is covered by the delegated selector or has an explicit exception.

```js
(function verifyEveryButtonHasHaptics() {
  const hasHapticApi = typeof window.haptic === 'function' || Boolean(window.Haptics && window.Haptics.haptic);

  const requiredSelector = [
    'button:not([disabled])',
    'input[type="button"]:not([disabled])',
    'input[type="submit"]:not([disabled])',
    'input[type="reset"]:not([disabled])',
    '[role="button"]:not([aria-disabled="true"])',
    '[role="switch"]:not([aria-disabled="true"])',
    '[role="tab"]:not([aria-disabled="true"])',
    '[role="menuitem"]:not([aria-disabled="true"])',
    'summary'
  ].join(',');

  const delegatedSelector = [
    'button',
    '[role="button"]',
    '[role="switch"]',
    '[role="tab"]',
    '[role="menuitem"]',
    'a[href]',
    'summary',
    'input[type="button"]',
    'input[type="submit"]',
    'input[type="reset"]',
    'input[type="checkbox"]',
    'input[type="radio"]',
    '[data-haptic]'
  ].join(',');

  const controls = Array.from(document.querySelectorAll(requiredSelector));
  const failures = controls.filter((control) => {
    if (!hasHapticApi) {
      return true;
    }

    if (control.hasAttribute('data-haptic-off')) {
      return !control.hasAttribute('data-haptic-off-reason');
    }

    return !control.matches(delegatedSelector);
  });

  const result = {
    hasHapticApi,
    totalButtonLikeControls: controls.length,
    hapticExceptions: controls.filter((control) => control.hasAttribute('data-haptic-off')).length,
    failures: failures.map((control) => ({
      tag: control.tagName.toLowerCase(),
      id: control.id || null,
      role: control.getAttribute('role'),
      text: (control.textContent || control.value || '').trim().slice(0, 80),
      reason: control.getAttribute('data-haptic-off-reason')
    }))
  };

  console.table(result.failures);
  console.log('Every-button haptic coverage', result);

  if (result.failures.length > 0) {
    throw new Error('Some enabled button-like controls are missing haptic coverage or exception reasons.');
  }

  return result;
}());
```

## Press-state CSS that pairs with haptic

```css
.pressable {
  position: relative;
  min-inline-size: 44px;
  min-block-size: 44px;
  border: 0;
  border-radius: 14px;
  background: color-mix(in srgb, ButtonFace 92%, Highlight 8%);
  color: ButtonText;
  transform: translateZ(0) scale(1);
  transition:
    transform 140ms cubic-bezier(0.2, 0, 0, 1),
    background-color 140ms cubic-bezier(0.2, 0, 0, 1),
    box-shadow 140ms cubic-bezier(0.2, 0, 0, 1);
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
  -webkit-user-select: none;
  user-select: none;
}

.pressable:active {
  transform: translateZ(0) scale(0.96);
}

.pressable:focus-visible {
  outline: 3px solid Highlight;
  outline-offset: 3px;
}

@media (hover: hover) and (pointer: fine) {
  .pressable:hover {
    background: color-mix(in srgb, ButtonFace 84%, Highlight 16%);
  }
}

@media (prefers-reduced-motion: reduce) {
  .pressable {
    transition: background-color 80ms linear;
  }

  .pressable:active {
    transform: none;
  }
}
```

## App-like motion tokens and primitives

Use one motion language across the app. Tokens should feel quick, subtle and functional. Do not let each component invent its own easing, distance or duration.

```css
:root {
  --motion-duration-instant: 80ms;
  --motion-duration-fast: 140ms;
  --motion-duration-medium: 220ms;
  --motion-duration-slow: 320ms;
  --motion-distance-xs: 4px;
  --motion-distance-sm: 8px;
  --motion-distance-md: 16px;
  --motion-scale-press: 0.97;
  --motion-scale-surface: 0.98;
  --motion-ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --motion-ease-decelerate: cubic-bezier(0, 0, 0, 1);
  --motion-ease-accelerate: cubic-bezier(0.3, 0, 1, 1);
}

@media (prefers-reduced-motion: reduce), (prefers-reduced-data: reduce) {
  :root {
    --motion-duration-instant: 1ms;
    --motion-duration-fast: 1ms;
    --motion-duration-medium: 1ms;
    --motion-duration-slow: 1ms;
    --motion-distance-xs: 0px;
    --motion-distance-sm: 0px;
    --motion-distance-md: 0px;
    --motion-scale-press: 1;
    --motion-scale-surface: 1;
  }
}

.motion-fade-enter {
  opacity: 0;
  transform: translate3d(0, var(--motion-distance-sm), 0);
}

.motion-fade-enter.is-active {
  opacity: 1;
  transform: translate3d(0, 0, 0);
  transition:
    opacity var(--motion-duration-medium) var(--motion-ease-standard),
    transform var(--motion-duration-medium) var(--motion-ease-standard);
}

.motion-surface-open {
  opacity: 0;
  transform: translate3d(0, var(--motion-distance-md), 0) scale(var(--motion-scale-surface));
}

.motion-surface-open.is-active {
  opacity: 1;
  transform: translate3d(0, 0, 0) scale(1);
  transition:
    opacity var(--motion-duration-medium) var(--motion-ease-decelerate),
    transform var(--motion-duration-medium) var(--motion-ease-decelerate);
}

.motion-bottom-sheet {
  transform: translate3d(0, 100%, 0);
  transition: transform var(--motion-duration-medium) var(--motion-ease-decelerate);
  will-change: transform;
}

.motion-bottom-sheet.is-open {
  transform: translate3d(0, 0, 0);
}

@media (prefers-reduced-motion: reduce), (prefers-reduced-data: reduce) {
  .motion-fade-enter,
  .motion-fade-enter.is-active,
  .motion-surface-open,
  .motion-surface-open.is-active,
  .motion-bottom-sheet,
  .motion-bottom-sheet.is-open {
    opacity: 1;
    transform: none;
    transition: none;
    will-change: auto;
  }
}
```

## UX-triggered route and surface transitions

This pattern lets UX events start motion while keeping the state change immediate. Use it for route pushes, tab switches, modal opens, sheet opens and save confirmations.

```js
(function initialiseAppLikeMotion(global) {
  const reducedMotionQuery = global.matchMedia('(prefers-reduced-motion: reduce)');
  const reducedDataQuery = global.matchMedia('(prefers-reduced-data: reduce)');

  function shouldReduceMotion() {
    return reducedMotionQuery.matches || reducedDataQuery.matches;
  }

  function withTemporaryWillChange(element, properties, run) {
    if (!element) {
      return run();
    }

    element.style.willChange = properties;

    return Promise.resolve(run()).finally(() => {
      global.setTimeout(() => {
        element.style.willChange = '';
      }, 260);
    });
  }

  function activateMotionClass(element, className) {
    if (!element || shouldReduceMotion()) {
      return;
    }

    element.classList.add(className);
    requestAnimationFrame(() => {
      element.classList.add('is-active');
    });
  }

  async function transitionRoute(applyNavigation) {
    if (shouldReduceMotion() || typeof document.startViewTransition !== 'function') {
      applyNavigation();
      return;
    }

    await document.startViewTransition(applyNavigation).finished;
  }

  function openSurface(surface) {
    if (!surface) {
      return;
    }

    surface.hidden = false;
    withTemporaryWillChange(surface, 'transform, opacity', () => {
      activateMotionClass(surface, 'motion-surface-open');
    });
  }

  function closeSurface(surface, afterClose) {
    if (!surface) {
      return;
    }

    if (shouldReduceMotion()) {
      surface.hidden = true;
      if (afterClose) {
        afterClose();
      }
      return;
    }

    surface.classList.remove('is-active');
    surface.addEventListener('transitionend', () => {
      surface.hidden = true;
      surface.classList.remove('motion-surface-open');
      if (afterClose) {
        afterClose();
      }
    }, { once: true });
  }

  global.AppMotion = Object.freeze({
    shouldReduceMotion,
    withTemporaryWillChange,
    activateMotionClass,
    transitionRoute,
    openSurface,
    closeSurface
  });
}(window));
```

## FLIP list transition helper

Use FLIP for list insertions, removals and reordering. It preserves spatial continuity without animating expensive layout properties every frame.

```js
(function initialiseFlipListMotion(global) {
  function capturePositions(container) {
    const positions = new Map();

    Array.from(container.children).forEach((child) => {
      if (child instanceof HTMLElement) {
        positions.set(child, child.getBoundingClientRect());
      }
    });

    return positions;
  }

  function playFlip(container, previousPositions) {
    if (window.AppMotion && window.AppMotion.shouldReduceMotion()) {
      return;
    }

    Array.from(container.children).forEach((child) => {
      if (!(child instanceof HTMLElement)) {
        return;
      }

      const previous = previousPositions.get(child);

      if (!previous) {
        child.animate([
          { opacity: 0, transform: 'translate3d(0, 8px, 0)' },
          { opacity: 1, transform: 'translate3d(0, 0, 0)' }
        ], {
          duration: 160,
          easing: 'cubic-bezier(0.2, 0, 0, 1)'
        });
        return;
      }

      const next = child.getBoundingClientRect();
      const deltaX = previous.left - next.left;
      const deltaY = previous.top - next.top;

      if (deltaX === 0 && deltaY === 0) {
        return;
      }

      child.animate([
        { transform: `translate3d(${deltaX}px, ${deltaY}px, 0)` },
        { transform: 'translate3d(0, 0, 0)' }
      ], {
        duration: 180,
        easing: 'cubic-bezier(0.2, 0, 0, 1)'
      });
    });
  }

  global.FlipMotion = Object.freeze({
    capturePositions,
    playFlip
  });
}(window));
```

## Animation performance probe

Use this during QA to catch motion that blocks interactions or misses frames. Pair it with DevTools Performance traces on real devices.

```js
(function initialiseAnimationPerformanceProbe(global) {
  function measureAnimationBudget(label, durationMs) {
    const start = performance.now();
    const frames = [];
    let previous = start;

    return new Promise((resolve) => {
      function frame(now) {
        frames.push(now - previous);
        previous = now;

        if (now - start < durationMs) {
          requestAnimationFrame(frame);
          return;
        }

        const droppedFrames = frames.filter((frameDuration) => frameDuration > 34).length;
        const worstFrame = Math.max(...frames);
        const result = {
          label,
          durationMs,
          frameCount: frames.length,
          droppedFrames,
          worstFrame: Math.round(worstFrame)
        };

        console.log('Animation budget', result);

        if (droppedFrames > 0 || worstFrame > 50) {
          console.warn('Animation needs optimisation', result);
        }

        resolve(result);
      }

      requestAnimationFrame(frame);
    });
  }

  global.measureAnimationBudget = measureAnimationBudget;
}(window));
```

## User preference toggle for haptics

```html
<label class="setting-row" for="haptics-toggle">
  <span>Haptic feedback</span>
  <input id="haptics-toggle" type="checkbox" role="switch" autocomplete="off">
</label>

<script>
(function initialiseHapticsToggle() {
  const toggle = document.getElementById('haptics-toggle');

  if (!toggle || !window.Haptics) {
    return;
  }

  toggle.checked = window.Haptics.isEnabled();

  toggle.addEventListener('change', () => {
    if (toggle.checked) {
      window.Haptics.enable();
      window.Haptics.haptic('toggleOn', { force: true });
    } else {
      window.Haptics.disable();
    }
  });
}());
</script>
```

## Audio fallback for iOS using Web Audio API

```html
<button class="pressable" id="enable-audio-feedback" type="button">Enable subtle audio feedback</button>

<script>
(function initialiseAudioFeedback() {
  const button = document.getElementById('enable-audio-feedback');

  if (!button || !window.Haptics) {
    return;
  }

  button.addEventListener('click', async () => {
    window.Haptics.setAudioFallback(true);
    await window.Haptics.haptic('success', { audioFallback: true, force: true });
    button.textContent = 'Audio feedback enabled';
  });
}());
</script>
```

## Standalone-mode detection

```css
@media (display-mode: standalone), (display-mode: fullscreen), (display-mode: window-controls-overlay) {
  :root {
    --is-installed-app: 1;
  }

  .browser-only {
    display: none !important;
  }
}
```

```js
(function detectStandaloneMode() {
  const isStandaloneByMedia = window.matchMedia('(display-mode: standalone)').matches;
  const isFullscreenByMedia = window.matchMedia('(display-mode: fullscreen)').matches;
  const isWindowControlsOverlay = window.matchMedia('(display-mode: window-controls-overlay)').matches;
  const isIosStandalone = 'standalone' in navigator && navigator.standalone === true;
  const isStandalone = isStandaloneByMedia || isFullscreenByMedia || isWindowControlsOverlay || isIosStandalone;

  document.documentElement.classList.toggle('is-standalone', isStandalone);
  document.documentElement.classList.toggle('is-browser-tab', !isStandalone);

  window.AppDisplayMode = Object.freeze({
    isStandalone,
    isStandaloneByMedia,
    isFullscreenByMedia,
    isWindowControlsOverlay,
    isIosStandalone
  });
}());
```

## Keyboard detection helper and layout adjustment

```css
:root {
  --visual-viewport-height: 100svh;
  --keyboard-inset-height: env(keyboard-inset-height, 0px);
}

.keyboard-avoidant {
  padding-block-end: max(env(safe-area-inset-bottom, 0px), var(--keyboard-inset-height, 0px));
}

.full-height-keyboard-aware {
  min-block-size: var(--visual-viewport-height);
}
```

```js
(function initialiseKeyboardHelper() {
  const root = document.documentElement;

  function update() {
    const visualViewport = window.visualViewport;
    const visualHeight = visualViewport ? visualViewport.height : window.innerHeight;
    const visualOffsetTop = visualViewport ? visualViewport.offsetTop : 0;
    const keyboardHeight = Math.max(0, window.innerHeight - visualHeight - visualOffsetTop);

    root.style.setProperty('--visual-viewport-height', `${visualHeight}px`);
    root.style.setProperty('--keyboard-inset-height', `${keyboardHeight}px`);
    root.classList.toggle('keyboard-open', keyboardHeight > 80);
  }

  if ('virtualKeyboard' in navigator) {
    navigator.virtualKeyboard.overlaysContent = false;
  }

  update();
  window.addEventListener('resize', update, { passive: true });

  if (window.visualViewport) {
    window.visualViewport.addEventListener('resize', update, { passive: true });
    window.visualViewport.addEventListener('scroll', update, { passive: true });
  }
}());
```

## iOS-safe modal scroll lock

```js
window.ModalScrollLock = (function createModalScrollLock() {
  let lockCount = 0;
  let scrollY = 0;

  function lock() {
    lockCount += 1;

    if (lockCount > 1) {
      return;
    }

    scrollY = window.scrollY || document.documentElement.scrollTop || 0;
    document.body.style.position = 'fixed';
    document.body.style.insetInlineStart = '0';
    document.body.style.insetInlineEnd = '0';
    document.body.style.insetBlockStart = `-${scrollY}px`;
    document.body.style.inlineSize = '100%';
    document.body.style.overflow = 'hidden';
  }

  function unlock() {
    if (lockCount === 0) {
      return;
    }

    lockCount -= 1;

    if (lockCount > 0) {
      return;
    }

    document.body.style.position = '';
    document.body.style.insetInlineStart = '';
    document.body.style.insetInlineEnd = '';
    document.body.style.insetBlockStart = '';
    document.body.style.inlineSize = '';
    document.body.style.overflow = '';
    window.scrollTo(0, scrollY);
  }

  return Object.freeze({ lock, unlock });
}());
```

## iOS input zoom prevention without disabling zoom

```html
<form class="auth-form" autocomplete="on">
  <label for="email">Email</label>
  <input id="email" name="email" type="email" autocomplete="email" inputmode="email" enterkeyhint="next" required>

  <label for="password">Password</label>
  <input id="password" name="password" type="password" autocomplete="current-password" enterkeyhint="done" required>

  <button class="pressable" type="submit">Sign in</button>
</form>
```

```css
.auth-form input,
.auth-form select,
.auth-form textarea {
  font-size: max(16px, 1rem);
  line-height: 1.4;
}
```

## Pull-to-refresh disable and custom implementation

```html
<div class="refresh-shell" id="refresh-shell">
  <div class="refresh-indicator" id="refresh-indicator" aria-hidden="true">Pull to refresh</div>
  <main class="refresh-scroller" id="refresh-scroller" tabindex="-1">
    <article class="content-card">
      <h1>Feed</h1>
      <p>Pull from the top of this panel to refresh app content.</p>
    </article>
  </main>
</div>
```

```css
html,
body {
  overscroll-behavior-y: none;
}

.refresh-shell {
  min-block-size: 100svh;
  overflow: clip;
}

.refresh-indicator {
  position: fixed;
  inset-block-start: max(8px, env(safe-area-inset-top, 0px));
  inset-inline: 0;
  z-index: 10;
  text-align: center;
  transform: translateY(-120%);
  transition: transform 180ms cubic-bezier(0.2, 0, 0, 1);
  pointer-events: none;
}

.refresh-indicator.is-visible {
  transform: translateY(0);
}

.refresh-scroller {
  block-size: 100svh;
  overflow: auto;
  overscroll-behavior: contain;
  -webkit-overflow-scrolling: touch;
}
```

```js
(function initialiseCustomPullToRefresh() {
  const scroller = document.getElementById('refresh-scroller');
  const indicator = document.getElementById('refresh-indicator');

  if (!scroller || !indicator) {
    return;
  }

  let startY = 0;
  let pulling = false;
  let pullDistance = 0;
  const threshold = 72;

  async function refreshContent() {
    indicator.textContent = 'Refreshing';

    if (typeof window.haptic === 'function') {
      window.haptic('refresh');
    }

    await new Promise((resolve) => window.setTimeout(resolve, 600));
    indicator.textContent = 'Updated';
    window.setTimeout(() => {
      indicator.classList.remove('is-visible');
      indicator.textContent = 'Pull to refresh';
    }, 500);
  }

  scroller.addEventListener('touchstart', (event) => {
    if (scroller.scrollTop === 0) {
      startY = event.touches[0].clientY;
      pulling = true;
      pullDistance = 0;
    }
  }, { passive: true });

  scroller.addEventListener('touchmove', (event) => {
    if (!pulling) {
      return;
    }

    pullDistance = Math.max(0, event.touches[0].clientY - startY);

    if (pullDistance > 16) {
      indicator.classList.add('is-visible');
    }
  }, { passive: true });

  scroller.addEventListener('touchend', () => {
    if (!pulling) {
      return;
    }

    pulling = false;

    if (pullDistance >= threshold) {
      refreshContent();
    } else {
      indicator.classList.remove('is-visible');
    }
  }, { passive: true });
}());
```

## View Transitions API setup

Treat View Transitions as progressive enhancement and disable meaningful motion under reduced motion.

```css
@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(root),
  ::view-transition-new(root) {
    animation-duration: 0.01ms;
  }
}
```

```js
(function initialiseViewTransitions() {
  function navigateWithTransition(url) {
    const applyNavigation = () => {
      window.location.href = url;
    };

    if (!document.startViewTransition || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      applyNavigation();
      return;
    }

    document.startViewTransition(applyNavigation);
  }

  document.addEventListener('click', (event) => {
    const target = event.target instanceof Element ? event.target : null;
    const link = target ? target.closest('a[data-view-transition]') : null;

    if (!link) {
      return;
    }

    const url = new URL(link.href);

    if (url.origin !== window.location.origin) {
      return;
    }

    event.preventDefault();
    navigateWithTransition(url.href);
  });
}());
```

## Skip-to-content link

```html
<a class="skip-link" href="#main-content">Skip to content</a>
<main id="main-content" tabindex="-1">
  <h1>Page title</h1>
</main>
```

```css
.skip-link {
  position: fixed;
  inset-block-start: max(8px, env(safe-area-inset-top, 0px));
  inset-inline-start: max(8px, env(safe-area-inset-left, 0px));
  z-index: 10000;
  padding: 10px 14px;
  border-radius: 10px;
  background: Canvas;
  color: CanvasText;
  transform: translateY(calc(-100% - 24px));
  transition: transform 120ms ease-out;
}

.skip-link:focus-visible {
  transform: translateY(0);
}
```

## Focus trap implementation for modals

```html
<div class="modal-backdrop" id="settings-modal" role="dialog" aria-modal="true" aria-labelledby="settings-modal-title" hidden>
  <div class="modal-panel" role="document">
    <h2 id="settings-modal-title">Settings</h2>
    <button type="button">Example setting</button>
    <button type="button" data-modal-close>Close</button>
  </div>
</div>
```

```js
function createFocusTrap(modalElement) {
  const focusableSelector = [
    'a[href]',
    'button:not([disabled])',
    'input:not([disabled])',
    'select:not([disabled])',
    'textarea:not([disabled])',
    '[tabindex]:not([tabindex="-1"])'
  ].join(',');

  let previouslyFocused = null;

  function getFocusableElements() {
    return Array.from(modalElement.querySelectorAll(focusableSelector))
      .filter((element) => element.offsetParent !== null || element === document.activeElement);
  }

  function setBackgroundInert(value) {
    document.querySelectorAll('body > *').forEach((element) => {
      if (element !== modalElement) {
        element.inert = value;
      }
    });
  }

  function close() {
    modalElement.hidden = true;
    setBackgroundInert(false);
    modalElement.removeEventListener('keydown', handleKeydown);

    if (window.ModalScrollLock) {
      window.ModalScrollLock.unlock();
    }

    if (previouslyFocused && typeof previouslyFocused.focus === 'function') {
      previouslyFocused.focus();
    }
  }

  function handleKeydown(event) {
    if (event.key === 'Escape') {
      close();
      return;
    }

    if (event.key !== 'Tab') {
      return;
    }

    const focusableElements = getFocusableElements();
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    if (!firstElement || !lastElement) {
      event.preventDefault();
      modalElement.focus();
      return;
    }

    if (event.shiftKey && document.activeElement === firstElement) {
      event.preventDefault();
      lastElement.focus();
      return;
    }

    if (!event.shiftKey && document.activeElement === lastElement) {
      event.preventDefault();
      firstElement.focus();
    }
  }

  function open() {
    previouslyFocused = document.activeElement;
    modalElement.hidden = false;
    setBackgroundInert(true);

    if (window.ModalScrollLock) {
      window.ModalScrollLock.lock();
    }

    modalElement.addEventListener('keydown', handleKeydown);
    const focusableElements = getFocusableElements();
    (focusableElements[0] || modalElement).focus();
  }

  modalElement.querySelectorAll('[data-modal-close]').forEach((button) => {
    button.addEventListener('click', close);
  });

  return Object.freeze({ open, close });
}
```

## Install prompt UI for Chrome beforeinstallprompt

```html
<section class="install-card" id="install-card" hidden>
  <h2>Install Example App</h2>
  <p>Install the app for offline access, app shortcuts and a standalone window.</p>
  <button class="pressable" id="install-button" type="button">Install</button>
  <button class="pressable" id="install-dismiss" type="button">Not now</button>
</section>

<script>
(function initialiseInstallPrompt() {
  const installCard = document.getElementById('install-card');
  const installButton = document.getElementById('install-button');
  const dismissButton = document.getElementById('install-dismiss');
  let deferredPrompt = null;

  function isInstalled() {
    return window.matchMedia('(display-mode: standalone)').matches || ('standalone' in navigator && navigator.standalone === true);
  }

  window.addEventListener('beforeinstallprompt', (event) => {
    if (isInstalled()) {
      return;
    }

    event.preventDefault();
    deferredPrompt = event;
    installCard.hidden = false;
  });

  installButton.addEventListener('click', async () => {
    if (!deferredPrompt) {
      installCard.hidden = true;
      return;
    }

    deferredPrompt.prompt();
    const choiceResult = await deferredPrompt.userChoice;
    console.log('Install prompt outcome', choiceResult.outcome);
    deferredPrompt = null;
    installCard.hidden = true;
  });

  dismissButton.addEventListener('click', () => {
    installCard.hidden = true;
  });

  window.addEventListener('appinstalled', () => {
    deferredPrompt = null;
    installCard.hidden = true;
  });
}());
</script>
```

## Manual iOS install instructions component

```html
<section class="ios-install" id="ios-install" hidden>
  <h2>Install on iPhone or iPad</h2>
  <ol>
    <li>Open this page in Safari.</li>
    <li>Tap the Share button.</li>
    <li>Choose Add to Home Screen.</li>
    <li>Tap Add.</li>
  </ol>
  <button class="pressable" id="ios-install-dismiss" type="button">Got it</button>
</section>

<script>
(function initialiseIosInstallInstructions() {
  const panel = document.getElementById('ios-install');
  const dismiss = document.getElementById('ios-install-dismiss');
  const isIos = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  const isStandalone = window.matchMedia('(display-mode: standalone)').matches || ('standalone' in navigator && navigator.standalone === true);
  const dismissed = window.localStorage.getItem('ios-install-dismissed') === 'true';

  if (panel && isIos && !isStandalone && !dismissed) {
    panel.hidden = false;
  }

  if (dismiss) {
    dismiss.addEventListener('click', () => {
      window.localStorage.setItem('ios-install-dismissed', 'true');
      panel.hidden = true;
    });
  }
}());
</script>
```

## Network status UI

```html
<div class="network-status" id="network-status" role="status" aria-live="polite" hidden>
  You are offline. Changes will sync when the connection returns.
</div>
```

```js
(function initialiseNetworkStatus() {
  const status = document.getElementById('network-status');

  if (!status) {
    return;
  }

  function updateStatus() {
    status.hidden = navigator.onLine;
    document.documentElement.classList.toggle('is-offline', !navigator.onLine);
  }

  window.addEventListener('online', updateStatus);
  window.addEventListener('offline', updateStatus);
  updateStatus();
}());
```

```css
.network-status {
  position: fixed;
  inset-inline: max(16px, env(safe-area-inset-left, 0px)) max(16px, env(safe-area-inset-right, 0px));
  inset-block-start: max(16px, env(safe-area-inset-top, 0px));
  z-index: 1000;
  padding: 10px 12px;
  border-radius: 12px;
  background: CanvasText;
  color: Canvas;
}
```

## Wake Lock helper

```js
const WakeLockHelper = (function createWakeLockHelper() {
  let wakeLock = null;
  let requested = false;

  async function request() {
    requested = true;

    if (!('wakeLock' in navigator)) {
      return false;
    }

    try {
      wakeLock = await navigator.wakeLock.request('screen');
      wakeLock.addEventListener('release', () => {
        wakeLock = null;
      });
      return true;
    } catch (error) {
      console.warn('Wake lock request failed', error);
      return false;
    }
  }

  async function release() {
    requested = false;

    if (wakeLock) {
      await wakeLock.release();
      wakeLock = null;
    }
  }

  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible' && requested) {
      request();
    }
  });

  return Object.freeze({ request, release });
}());
```

## Web Share helper with clipboard fallback

```js
async function shareOrCopy(shareData) {
  const data = Object.assign({
    title: document.title,
    text: '',
    url: window.location.href
  }, shareData || {});

  if (navigator.share) {
    try {
      if (!navigator.canShare || navigator.canShare(data)) {
        await navigator.share(data);
        return { ok: true, method: 'share' };
      }
    } catch (error) {
      if (error && error.name === 'AbortError') {
        return { ok: false, method: 'share', reason: 'cancelled' };
      }
    }
  }

  const textToCopy = [data.title, data.text, data.url].filter(Boolean).join('\n');

  if (navigator.clipboard && navigator.clipboard.writeText) {
    await navigator.clipboard.writeText(textToCopy);
    return { ok: true, method: 'clipboard' };
  }

  const textarea = document.createElement('textarea');
  textarea.value = textToCopy;
  textarea.setAttribute('readonly', 'readonly');
  textarea.style.position = 'fixed';
  textarea.style.insetBlockStart = '-1000px';
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand('copy');
  textarea.remove();
  return { ok: true, method: 'legacy-clipboard' };
}
```

## Image optimisation pattern

```html
<picture>
  <source type="image/avif" srcset="/images/card-640.avif 640w, /images/card-1280.avif 1280w" sizes="(min-width: 768px) 50vw, 100vw">
  <source type="image/webp" srcset="/images/card-640.webp 640w, /images/card-1280.webp 1280w" sizes="(min-width: 768px) 50vw, 100vw">
  <img
    src="/images/card-640.jpg"
    srcset="/images/card-640.jpg 640w, /images/card-1280.jpg 1280w"
    sizes="(min-width: 768px) 50vw, 100vw"
    width="640"
    height="426"
    loading="lazy"
    decoding="async"
    alt="Dashboard card preview">
</picture>
```

## Forms and input attributes pattern

```html
<form class="profile-form" autocomplete="on">
  <label for="full-name">Full name</label>
  <input id="full-name" name="name" type="text" autocomplete="name" enterkeyhint="next" required>

  <label for="email-address">Email address</label>
  <input id="email-address" name="email" type="email" autocomplete="email" inputmode="email" enterkeyhint="next" required>

  <label for="phone-number">Phone number</label>
  <input id="phone-number" name="phone" type="tel" autocomplete="tel" inputmode="tel" enterkeyhint="next">

  <label for="one-time-code">Security code</label>
  <input id="one-time-code" name="one-time-code" type="text" autocomplete="one-time-code" inputmode="numeric" enterkeyhint="done" autocorrect="off" autocapitalize="off" spellcheck="false">

  <label for="code-snippet">Code</label>
  <textarea id="code-snippet" name="code" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" inputmode="text"></textarea>

  <button class="pressable" type="submit">Save</button>
</form>
```

## File upload, drag-and-drop and paste pattern

```html
<label class="upload-drop-zone" id="upload-drop-zone">
  <span>Upload images or paste files here</span>
  <input id="file-input" type="file" name="files" accept="image/png,image/jpeg,image/webp,image/avif,application/pdf" multiple>
</label>
<ul id="file-list" aria-live="polite"></ul>
```

```js
(function initialiseFileInput() {
  const dropZone = document.getElementById('upload-drop-zone');
  const fileInput = document.getElementById('file-input');
  const fileList = document.getElementById('file-list');

  function handleFiles(files) {
    fileList.innerHTML = '';
    Array.from(files).forEach((file) => {
      const item = document.createElement('li');
      item.textContent = `${file.name} (${Math.round(file.size / 1024)} KB)`;
      fileList.appendChild(item);
    });
  }

  fileInput.addEventListener('change', () => {
    handleFiles(fileInput.files);
  });

  dropZone.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropZone.classList.add('is-dragging');
  });

  dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('is-dragging');
  });

  dropZone.addEventListener('drop', (event) => {
    event.preventDefault();
    dropZone.classList.remove('is-dragging');
    handleFiles(event.dataTransfer.files);
  });

  document.addEventListener('paste', (event) => {
    if (event.clipboardData && event.clipboardData.files.length > 0) {
      handleFiles(event.clipboardData.files);
    }
  });
}());
```

## Media playback pattern

```html
<video
  class="hero-video"
  src="/media/hero.mp4"
  poster="/media/hero-poster.jpg"
  width="1280"
  height="720"
  autoplay
  muted
  loop
  playsinline
  webkit-playsinline
  controlslist="nodownload"
  disablepictureinpicture>
  <track kind="captions" src="/media/hero-captions.vtt" srclang="en" label="English">
</video>
```

```js
(function pauseMediaWhenHidden() {
  document.addEventListener('visibilitychange', () => {
    const videos = document.querySelectorAll('video[data-pause-when-hidden="true"]');

    videos.forEach((video) => {
      if (document.visibilityState === 'hidden') {
        video.pause();
      }
    });
  });
}());
```

# Failure-mode catalogue

| Failure mode | Reproduction case | Root cause | Fix |
| --- | --- | --- | --- |
| Dynamic Island or notch overlap | Open on iPhone with Dynamic Island in portrait and landscape. | Edge-to-edge viewport has no top safe-area padding. | Use viewport-fit=cover and padding-block-start: env(safe-area-inset-top). |
| Home indicator overlap | Tap bottom nav or CTA on iPhone gesture navigation. | Fixed bottom UI ignores safe-area-inset-bottom. | Put safe-area padding inside the bottom surface. |
| env(safe-area-inset-*) absent | Search CSS for safe-area-inset. | Generated UI assumes a rectangular viewport. | Create --safe-* tokens and use them in all edge UI. |
| Viewport meta missing viewport-fit | Inspect the head. | Safe-area variables are not activated for full edge-to-edge layout. | Use the viewport meta snippet. |
| interactive-widget not handled | Focus bottom inputs in Chrome Android and Safari. | Keyboard resize mode is unspecified. | Choose resizes-content, resizes-visual or overlays-content and keep visualViewport fallback. |
| PWA standalone layout breaks | Compare Safari tab with installed Home Screen app. | Standalone has different chrome and status bar behaviour. | Detect display-mode plus navigator.standalone and add standalone CSS. |
| Phantom scroll from 100vh | Scroll mobile Safari while address bar changes. | Legacy vh maps to the large viewport. | Use svh, dvh or lvh by intent. |
| Bottom nav visible gap | Scroll with home indicator visible. | A guessed bottom spacer is used instead of safe-area padding. | Pin to inset-block-end: 0 and pad inside. |
| Keyboard pushes layout incorrectly | Focus inputs at several vertical positions. | Visual viewport, layout viewport and keyboard insets are confused. | Use visualViewport and VirtualKeyboard progressive enhancement. |
| Foldables ignored | Test folded and unfolded Galaxy Fold or Surface Duo. | Single rectangular breakpoint model. | Use container queries and viewport segment variables. |
| Tablets and landscape ignored | Rotate iPad and use split-screen. | Breakpoints skip medium and resizable windows. | Use fluid grids, orientation tests and safe-area in landscape. |
| Hover and pointer ignored | Test mouse, touch and hybrid tablet. | Hover is the only reveal path or pointer type is assumed. | Use hover and pointer media queries and non-hover controls. |
| Android display cutouts ignored | Test Android edge-to-edge and WebView. | Android safe-area support and WebView versions are not considered. | Use env safe areas and WebView-specific test cases. |
| Some buttons are silent | Tap every button-like control on Android and run the haptic coverage verifier. | Haptics are added one component at a time or only to primary buttons. | Use delegated every-button haptic binding, named patterns and documented `data-haptic-off` exceptions only. |
| No micro-interactions | Tap controls repeatedly. | Only static or hover styling exists. | Add :active, :focus-visible, transitions and press states. |
| Website-style motion | Scroll a page without interacting and watch sections animate in. | Decorative reveal motion is used instead of UX-triggered state motion. | Remove passive scroll reveals and use app-like motion only for user intent, navigation and feedback. |
| Over-the-top animation | Tap through common flows and animations feel bouncy, long or theatrical. | Durations, distances and easing are designed for spectacle instead of fast task completion. | Use shared motion tokens, short distances and restrained easing. |
| Animation jank | Record route, sheet and list animations on low-end mobile. | Layout, paint, filters or long tasks run during animation. | Animate transform and opacity, use FLIP for layout changes and split long work. |
| iOS rubber-band scroll | Overscroll top and bottom of app shell. | Document body is the active scroller. | Use contained app scroller and overscroll-behavior where supported. |
| Pull-to-refresh hijacking | Pull near top inputs on Android Chrome. | Top overscroll reaches browser refresh. | Use overscroll-behavior-y and custom refresh if required. |
| Status bar tap-to-scroll-top broken | Tap iOS status bar while custom scroller is active. | Body is no longer the primary scroller. | Prefer body scroll for documents or add explicit scroll-to-top. |
| Long-press text selection on buttons | Long-press app controls on iOS. | Controls inherit selectable text behaviour. | Apply user-select: none only to controls. |
| iOS callout menu appears | Long-press links and images in controls. | Safari callout remains enabled. | Use -webkit-touch-callout: none only on app controls. |
| Double-tap zoom delay | Tap older mobile browsers rapidly. | Browser waits for double-tap zoom. | Use touch-action: manipulation and correct viewport width. |
| iOS input zoom | Focus a form control under 16px. | Safari zooms small text controls. | Set controls to at least 16px and keep zoom enabled. |
| Autofill yellow background | Autofill login forms. | Browser autofill pseudo-class paints default background. | Style :-webkit-autofill with inset box-shadow and text fill. |
| Date time select mismatch | Open pickers across iOS, Android and desktop. | Native pickers differ by platform. | Use semantic controls and avoid pixel-perfect assumptions. |
| 100vw horizontal scroll | Compare scrollWidth and innerWidth on desktop. | 100vw includes scrollbar gutter. | Use width: 100% or inline-size: 100%. |
| Sticky header jitter | Bounce-scroll at top on iOS. | Sticky geometry shifts with rubber-band and chrome movement. | Keep sticky in intended scroller and avoid heavy filters. |
| backdrop-filter frame drops | Profile lower-end Android scrolling. | Backdrop compositing repaints large areas. | Reduce blur, limit area and provide opaque fallback. |
| will-change memory bloat | Inspect layer count and memory. | Persistent layer promotion. | Apply will-change only shortly before animation. |
| Safari stacking context bugs | Open overlays under transformed ancestors. | transform, filter and opacity create stacking contexts. | Move overlays to a top-level root. |
| iOS fixed inside transform | Put fixed modal inside transformed root. | Transform creates fixed containing block. | Render fixed overlays under body. |
| 100dvh layout thrash | Use many 100dvh elements while address bar animates. | dvh changes cause repeated layout. | Use one root variable or svh where stable. |
| Images eager or unsized | Audit image attributes. | Images compete with critical resources and cause CLS. | Set width, height, loading, decoding and fetchpriority. |
| Font loading unmanaged | Throttle network and reload. | Fonts lack preload, swap or subsetting. | Use font-display: swap and preload critical fonts. |
| CLS from late components | Measure layout shifts in Performance panel. | Space not reserved. | Reserve slots with aspect-ratio, min-height and metrics. |
| LCP not prioritised | Inspect LCP request start and priority. | Hero resource starts late. | Preload and use fetchpriority high on true LCP image. |
| INP blocked | Record interactions. | Long tasks block event handling. | Split long work and reduce main-thread JS. |
| Stale service worker | Deploy update while app is open, then reopen the installed PWA. | Cache versioning, waiting flow or force-update controller is missing. | Use versioned caches, `registration.update()`, `SKIP_WAITING`, `clients.claim()` and reload once on `controllerchange`. |
| Offline UX absent | Disable network and submit forms. | No fallback or queue. | Add offline page, queue and network status. |
| Install prompts incomplete | Test Chrome and iOS install. | beforeinstallprompt is assumed universal. | Use Chrome prompt and manual iOS component. |
| Share APIs absent | Tap share action on mobile. | Custom link copy only. | Use navigator.share with clipboard fallback. |
| File flows weak | Upload from picker, drag and paste. | accept, paste and drop paths missing. | Add semantic accept plus drag and paste handlers. |
| Clipboard permission surprise | Copy outside user activation. | Clipboard API needs secure context and activation. | Call writeText from direct user action. |
| Wake lock absent | Use timer or navigation screen. | No screen wake lock request. | Request Wake Lock after user action and release on visibility change. |
| Orientation missing | Rotate media, maps or game. | Orientation lock and responsive fallback ignored. | Use Screen Orientation API where available. |
| Background work continues | Background tab and inspect polling. | Page Visibility API ignored. | Pause polling and media on visibilitychange. |
| Standalone detection wrong | Test iOS Home Screen and Android standalone. | Only one detection path used. | Use display-mode and navigator.standalone. |
| Address bar jank | Scroll mobile Chrome and Safari. | Layout tied to changing viewport. | Use svh or lvh by intent and restrict dvh. |
| Wrong viewport unit choice | Compare splash, forms and app shell. | One unit used everywhere. | Use the viewport unit decision tree. |
| Scroll restoration broken | Navigate back to a long route. | Router does not save position. | Use history.scrollRestoration with per-route storage. |
| Anchor hidden under fixed header | Open hash links. | Targets align under fixed UI. | Use scroll-margin-top or scroll-padding-top. |
| scroll-snap momentum issues | Swipe snap carousel on iOS. | Snap and momentum compete. | Use scroll-padding and test nested scroll carefully. |
| Modal focus escapes | Tab through open modal. | No focus trap or inert background. | Use dialog or focus trap plus inert. |
| Focus rings removed | Keyboard through page. | outline removed or :focus misused. | Use :focus-visible with visible outline. |
| Skip link missing | Press Tab from top. | Repeated navigation must be traversed. | Add visible-on-focus skip link. |
| Reduced data ignored | Enable save-data or reduced-data. | Heavy assets always load. | Use reduced-data and Network Information progressive enhancement. |
| Forced colours broken | Enable Windows High Contrast. | Custom colours hide UI. | Use forced-colors and system colours. |
| RTL broken | Set dir=rtl. | Physical left and right CSS. | Use logical properties. |
| text-size-adjust missing | Rotate iOS landscape. | Text autosizing changes layout. | Set text-size-adjust: 100%. |
| Smooth scroll ignores motion | Enable reduced motion and anchor navigate. | scroll-behavior remains smooth. | Disable smooth scroll under reduced motion. |
| Native APIs ignored | Audit custom menus and modals. | Popover and dialog not considered. | Use native APIs where fit and tested. |
| Native controls clash | Switch dark mode. | color-scheme and accent-color missing. | Set color-scheme and accent-color. |
| Custom scrollbar contrast | Test dark and forced colours. | Hard-coded low contrast. | Use scrollbar-color and forced-colors fallback. |
| WebView differences | Open same link in Safari and WebViews. | Host app changes behaviour. | Test WKWebView, Android WebView and in-app browsers. |
| Storage partitioning surprises | Test embedded flows and in-app browsers. | Third-party storage is constrained. | Use first-party sessions and IndexedDB. |
| Standalone analytics missing | Compare tab and installed app. | Analytics assumes browser tab signals. | Send privacy-respecting standalone events and offline queue. |
| Deep links fail | Open notification, share and external URLs. | scope, start_url or launch_handler misaligned. | Align manifest and router. |
| Manifest shortcuts missing | Long-press installed Android icon. | shortcuts absent. | Add shortcuts with icons and in-scope URLs. |
| File handlers absent | Open supported file from OS. | file_handlers missing. | Declare handlers and route. |
| Protocol handlers absent | Open web+example URL. | protocol_handlers missing. | Declare handlers and parse safely. |
| scope and start_url mismatch | Install and navigate routes. | App leaves scope. | Keep start_url inside scope and set id. |
| Maskable icon clipped | Inspect Android adaptive icon. | Artwork outside safe zone. | Keep essential art inside 80 percent safe zone. |
| Splash screens missing | Cold launch iOS Home Screen app. | Startup images absent or wrong size. | Provide exact apple-touch-startup-image assets. |
| Theme colour mismatch | Scroll sections and inspect browser UI. | theme-color static or absent. | Use media theme-color and optional dynamic updates. |
| Selection and caret colours clash | Select text and type. | Default colours clash with theme. | Define ::selection and caret-color. |
| Autocomplete weak | Test login, address and OTP. | Precise tokens absent. | Use email, current-password, new-password and one-time-code. |
| Wrong mobile keyboard | Focus numeric, email and search fields. | inputmode and enterkeyhint missing. | Use type, inputmode and enterkeyhint together. |
| iOS assistant bar overlap | Focus bottom field on iOS. | Keyboard accessory UI not considered. | Use visualViewport bottom padding. |
| Smart punctuation in code inputs | Type quotes in code field. | Autocorrect and spellcheck enabled. | Set autocorrect off, autocapitalize off and spellcheck false. |
| Memory pressure tab kill | Use media-heavy app on iOS. | Too many retained images, layers or canvases. | Release resources and cap retained DOM. |
| WebGL low power surprises | Enable iOS Low Power Mode. | Frame loops not adaptive. | Reduce resolution and pause offscreen rendering. |
| Reduced motion ignored | Enable reduced motion. | Animations ignore preference. | Wrap all motion and autoplay effects. |
| Reduced data ignored | Enable data saver or throttle network. | Non-essential motion, video or shimmer continues. | Disable decorative motion and heavy animated media under reduced data. |
| Autoplay video fails | Load hero video on mobile. | Autoplay policy requires muted inline. | Use muted autoplay playsinline and poster. |
| iOS video fullscreen takeover | Play inline video on iPhone. | playsinline missing. | Add playsinline and webkit-playsinline. |
| Picture-in-picture mismatch | Try PiP controls. | PiP support not checked. | Use disablePictureInPicture only when intended. |
| Audio context silent | Start audio on load. | User activation required. | Resume AudioContext from user gesture. |
| Battery and network adaptation absent | Throttle network. | Loading ignores connection constraints. | Use Network Information and optional Battery API as progressive enhancements. |

# Device test matrix

| Device or context | Browsers or modes | Required behaviours | Haptics | Install | Notifications | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| iPhone SE class | Safari tab, Home Screen, iOS Chrome | 100svh, input zoom, safe top and bottom, VoiceOver | No general Vibration API in Safari | Manual Add to Home Screen | Web Push requires installed web app on iOS 16.4 and later | Small height exposes keyboard and CTA failures |
| iPhone Pro or Pro Max with notch or Dynamic Island | Safari tab, Home Screen, in-app browsers | Dynamic Island, landscape safe areas, home indicator, startup image | Same iOS limitation | Manual Add to Home Screen | Installed web app support on iOS 16.4 and later | Test black-translucent status bar |
| iPad mini and iPad Pro | Safari tab, Home Screen, split-screen, Stage Manager | Resizable viewport, pointer hybrid, landscape, custom scroll containers | No general Vibration API in Safari | Manual Add to Home Screen | Installed web app support on iPadOS 16.4 and later | Startup images need exact window sizes |
| Android compact phone | Chrome, Firefox Android, Android WebView | safe-area, gesture navigation, keyboard, pull-to-refresh, install prompt | Vibration API often supported in Chromium | Chrome prompt and browser install UI | Push supported in Chromium PWAs with permission | Firefox support differs by API |
| Android large phone | Chrome, Samsung Internet | bottom nav, keyboard, landscape, coarse pointer, address bar jank | Common in Chromium-based browsers | Browser-dependent | Browser-dependent | Samsung Internet can differ in PWA behaviour |
| Galaxy Fold | Chrome, Samsung Internet | folded and unfolded widths, hinge, container queries, segment env variables | Common in Chromium-based browsers | Browser-dependent | Browser-dependent | Test both physical modes |
| Surface Duo or dual-screen emulator | Edge or Chromium | two horizontal segments, hinge gap, master-detail layout | Device-dependent | Browser-dependent | Browser-dependent | Use viewport segments as progressive enhancement |
| Android WebView | Host app WebView | safe-area insets, keyboard, storage, external links | Host-dependent | Not a PWA install context | Host-dependent | M136, M139 and M144 changed inset behaviour |
| Desktop narrow viewport | Chrome, Edge, Firefox, Safari | 100vw overflow, keyboard, resize, forced colours | Usually unavailable or limited | Desktop install varies | Browser-dependent | Include Windows High Contrast |
| Desktop ultra-wide | Chrome, Edge, Firefox, Safari | max-width, readable line length, layout density, hover | Usually unavailable | Browser-dependent | Browser-dependent | Avoid unbounded stretching |
| TV or kiosk | Chromium-based, WebView, smart TV browser | large viewport, focus navigation, remote control | Usually unavailable | Usually unavailable | Usually unavailable | Use visible focus |
| Instagram, Facebook and TikTok in-app browsers | Embedded WebViews | storage, cookies, external links, viewport, install unavailable | Host-dependent | Usually unavailable | Usually unavailable | Provide open-in-browser fallback |

# Decision trees

## dvh vs svh vs lvh

1. Splash, hero or visual background that may fill the largest possible viewport: use `100lvh` with `100vh` fallback.
2. App shell or screen that must never hide controls under browser chrome: use `100svh` with `100vh` fallback.
3. Panel that must track address bar or keyboard changes: use one `100dvh` or a `visualViewport` root variable.
4. Normal document flow: avoid viewport units and let content size the layout.
5. Desktop width: avoid `100vw`; use `width: 100%` or `inline-size: 100%`.

## Should this trigger haptics

1. Is the action user-initiated through tap, drag, switch, snap, save, warning or error? Continue.
2. Did the user disable haptics or does reduced motion apply with no opt-in? Do not trigger.
3. Is the control disabled, decorative or passive? Do not trigger.
4. Is the event high frequency, such as pointermove or typing? Trigger only on threshold, snap or completion.
5. Does `navigator.vibrate()` exist? Use the named pattern.
6. Is vibration unavailable and audio fallback enabled by the user? Play the subtle Web Audio cue.

## Media query vs container query

1. Component changes because its own width changes: use `@container`.
2. Behaviour changes because device or user capability changes: use media queries.
3. Component sits in a resizable sidebar, card or split pane: use container queries.
4. Whole app shell changes navigation mode: use media queries plus safe-area tests.
5. Foldables: combine viewport segment media features with container queries.

## position fixed vs position sticky

1. Global viewport-pinned UI: use `position: fixed` under a top-level overlay root.
2. Section-local UI that stops at section boundary: use `position: sticky`.
3. Any ancestor has transform, filter, perspective, contain, will-change or opacity: avoid fixed descendants.
4. Modal, toast, bottom sheet or global nav: prefer fixed.
5. Table header, section header or local toolbar: prefer sticky.

## Native dialog vs custom modal

1. Simple blocking modal: use `<dialog>` and `showModal()`.
2. Complex bottom sheet gestures or nested scroll physics: use custom modal with focus trap and inert.
3. Old browser support without polyfill: use tested custom modal.
4. Menu, tooltip or lightweight disclosure: consider Popover API.
5. Always test focus, Escape, scroll lock, VoiceOver and TalkBack.

# Interaction feedback matrix

| UI event | Visual feedback | Haptic pattern | Audio cue | Notes |
| --- | --- | --- | --- | --- |
| Primary button tap | Scale to 0.96, pressed background, focus-visible | light | None by default | Trigger on pointerup |
| Secondary button tap | Pressed background and opacity | selection | None | Keep contrast stable |
| Toggle on | Thumb movement and track colour | toggleOn | Optional soft click | Avoid double feedback if native switch already provides haptic |
| Toggle off | Thumb movement and track colour | toggleOff | Optional soft click | Same as toggle on |
| Checkbox or radio | Checkmark or dot transition | selection | None | Preserve native semantics |
| Successful save | Optimistic state and toast | success | Optional short success tone | Do not repeat on background sync |
| Warning action | Destructive highlight | warning | Optional low tone | Use before confirmation |
| Error after submit | Error message and invalid outline | error | Optional error tone | Move focus to error summary where appropriate |
| Long press recognised | Menu opens or handle grows | longPress | Optional tick | Avoid for ordinary links |
| Swipe accepted | Card exits with easing | swipe | None | Trigger on threshold or release |
| Drag snap | Item settles to snap point | dragSnap | None | Throttle to snap points |
| Pull-to-refresh threshold | Indicator locks | refresh | Optional tick | Do not fire every pixel |
| Navigation transition | View transition or fade | selection | None | Disable meaningful motion under reduced motion |
| Bottom sheet open | Translate from bottom to safe-area-aware final position | selection | None | Keep under 260 ms and interruptible |
| Modal close | Fade backdrop and scale or translate surface out | selection | None | Restore focus after close |
| List item inserted | Fade and translate 6px to 8px or FLIP existing items | None | None | Reserve space and avoid CLS |
| Offline banner | Slide from safe edge and hold | warning | None | Do not cover primary action |
| Copy to clipboard | Toast and icon change | success | None | Only after successful write |
| Install prompt opened | Card or sheet reveal | selection | None | Do not fire on page load |

# Anti-patterns: remove on sight

- `height: 100vh` on app roots, modals, heroes or panels without viewport-unit reasoning.
- `width: 100vw` on content wrappers.
- Fixed bottom navigation without `padding-bottom: env(safe-area-inset-bottom)`.
- Header or menu content under notch or Dynamic Island.
- `user-scalable=no`, `maximum-scale=1` or `minimum-scale=1` used as layout fix.
- `<input type="text">` with `font-size: 14px` on mobile.
- Body scroll lock implemented only as `overflow: hidden`.
- `position: fixed` inside transformed, filtered or `will-change` ancestor.
- Buttons built as `div` or `span` with click handlers.
- Hover-only menus or tooltips.
- Focus styles removed.
- Global `user-select: none`.
- Global `-webkit-touch-callout: none`.
- Motion, parallax, autoplay video or smooth scrolling without reduced-motion handling.
- Large scrolling surfaces with `backdrop-filter`.
- Persistent `will-change` on many elements.
- Images without width and height.
- Hero image lazy-loaded.
- Every image marked `fetchpriority="high"`.
- Fonts without `font-display`.
- Service worker caches without version names.
- Service worker updates that reload immediately with no user context.
- PWA updates that require users to clear site data before the new shell appears.
- Enabled buttons, tabs, switches or menu items that do not route through the haptic system.
- Manifest `start_url` outside `scope`.
- Missing 192 by 192 and 512 by 512 icons.
- Maskable icon artwork outside the safe zone.
- Missing `playsinline` on mobile video.
- Web Audio started before user activation.
- Clipboard writes outside user gestures.
- Hard-coded left and right CSS that breaks RTL.
- Custom scrollbars with insufficient contrast.

# Performance budget template

| Metric | Target | Hard fail | Measurement method | Priority |
| --- | --- | --- | --- | --- |
| Largest Contentful Paint | 2.5 seconds or less at p75 | More than 4.0 seconds | RUM, PageSpeed Insights, WebPageTest | Critical |
| Interaction to Next Paint | 200 milliseconds or less at p75 | More than 500 milliseconds | RUM, DevTools interaction traces | Critical |
| Cumulative Layout Shift | 0.1 or less at p75 | More than 0.25 | Lighthouse, web-vitals attribution | Critical |
| Initial JavaScript | 170 KB gzip for content sites, 250 KB gzip for app shells | More than 350 KB gzip | Network panel | High |
| Route-level JavaScript | 80 KB gzip per lazy route | More than 150 KB gzip | Network panel | High |
| Critical CSS | 20 KB gzip or less | More than 50 KB gzip | Coverage panel | Medium |
| Hero image | 200 KB or less on mobile where possible | More than 500 KB | Network panel | High |
| Above-fold images | 400 KB or less on mobile | More than 900 KB | Network panel | High |
| Long tasks | No interaction task over 50 ms | Repeated tasks over 100 ms | DevTools Performance | High |
| Critical font files | 100 KB gzip or less | More than 200 KB | Network panel | Medium |
| iOS memory | No retained media-heavy hidden routes | Reproducible tab kill | Real iPhone testing | High |
| Animation frames | No repeated frames over 34 ms during common motion | Worst frame over 50 ms or visible dropped frames | Performance trace and animation probe | High |
| Composited motion | Transform and opacity for primary motion | Layout or paint every frame | Rendering panel and Performance trace | High |
| Layer count | Temporary layers only for active motion | Persistent `will-change` across many elements | Layers panel | Medium |

Rules:

1. Reserve every media slot with width and height, aspect-ratio or min-block-size.
2. Add `fetchpriority="high"` only to the true LCP image.
3. Lazy-load below-fold images and iframes.
4. Split long work with timers, scheduler APIs where supported or idle callbacks.
5. Avoid broad `backdrop-filter` and persistent `will-change`.
6. Use `content-visibility: auto` carefully on below-fold sections.
7. Use reduced-data and Network Information as progressive enhancements.
8. Keep app-like motion under shared duration and distance tokens.
9. Profile route transitions, sheets, drawers, tabs and list changes on real mobile hardware.
10. Treat visible dropped frames, delayed taps or repeated layout during animation as release blockers.

# Accessibility checklist aligned to WCAG 2.2 AA

- Every interactive element is reachable by keyboard.
- Every interactive element has a visible `:focus-visible` indicator.
- Focus order matches visual and reading order.
- Modals trap focus, restore focus on close and make background inert.
- Escape closes dismissible modals and menus.
- Skip-to-content link appears on focus before repeated navigation.
- Touch targets meet at least 24 by 24 CSS pixels with spacing for WCAG 2.2 AA. App controls should usually be at least 44 by 44 CSS pixels and 48 by 48 on Android coarse pointer contexts.
- Text contrast meets 4.5:1 for normal text and 3:1 for large text and essential graphics.
- UI does not rely on colour alone.
- Motion respects `prefers-reduced-motion: reduce` for transitions, parallax, skeleton shimmer, smooth scrolling and autoplay media.
- Forced colours mode preserves visible boundaries, text and controls.
- Form errors are announced and associated with fields.
- Labels are programmatically associated with inputs.
- Custom controls use native elements first. If custom controls are necessary, roles, states and keyboard behaviour match the native pattern.
- Page language and direction use `lang` and `dir`.
- RTL layouts use logical properties.
- Zoom remains available.
- Text can be selected and copied in content areas.
- Screen reader testing includes VoiceOver on iOS and TalkBack on Android.
- Status messages use `role="status"` or `aria-live="polite"` where appropriate.

# Viewport and meta reference

`<meta name="viewport">` is parsed as comma-separated key-value tokens.

| Token | Values | Use | Audit warning |
| --- | --- | --- | --- |
| `width` | `device-width` or positive integer | Use `device-width` | Integer widths are usually legacy |
| `height` | `device-height` or positive integer | Rarely needed | Brittle on mobile |
| `initial-scale` | Number | Use `1` | Extreme values harm readability |
| `minimum-scale` | Number | Usually omit | Restricts zoom when combined poorly |
| `maximum-scale` | Number | Usually omit | Do not use to hide defects |
| `user-scalable` | `yes` or `no` | Omit or allow | `no` restricts zoom |
| `viewport-fit` | `auto`, `contain`, `cover` | Use `cover` for safe-area-aware edge-to-edge UI | Requires safe-area padding |
| `interactive-widget` | `resizes-visual`, `resizes-content`, `overlays-content` | Keyboard resize mode | Unsupported browsers ignore it |

Platform notes:

- iOS Safari and WKWebView share WebKit, but host apps can alter chrome, storage and permission UX.
- Chrome Android changed keyboard resize behaviour in Chrome 108.
- Android WebView safe-area insets changed in M136, M139 and M144.
- Samsung Internet and Firefox Android differ in some manifest, vibration, orientation and share support.
- Instagram, Facebook and TikTok in-app browsers should be tested as constrained embedded contexts.

# Safe area insets reference

Use modern `env()` variables. `constant()` is only for very old iOS 11.0 support. Variables include `safe-area-inset-*`, `safe-area-max-inset-*`, `keyboard-inset-*` and viewport segment variables.

```css
:root {
  --safe-top: env(safe-area-inset-top, 0px);
  --safe-right: env(safe-area-inset-right, 0px);
  --safe-bottom: env(safe-area-inset-bottom, 0px);
  --safe-left: env(safe-area-inset-left, 0px);
  --keyboard-bottom: env(keyboard-inset-height, 0px);
}

.safe-card {
  padding-block-start: calc(16px + var(--safe-top));
  padding-block-end: max(16px, var(--safe-bottom));
  padding-inline-start: max(16px, var(--safe-left));
  padding-inline-end: max(16px, var(--safe-right));
}

.old-ios-11-only-fallback {
  padding-top: constant(safe-area-inset-top);
  padding-top: env(safe-area-inset-top, 0px);
}
```

# PWA and standalone reference

Manifest `display` values are `fullscreen`, `standalone`, `minimal-ui` and `browser`. `display_override` lets browsers try advanced modes before fallback. iOS also needs Apple-specific metadata and manual install instructions. iOS and iPadOS web push notifications are available for installed web apps from Safari 16.4 and later.

Audit these manifest fields: `id`, `name`, `short_name`, `start_url`, `scope`, `display`, `display_override`, `icons`, `shortcuts`, `share_target`, `file_handlers`, `protocol_handlers`, `launch_handler`, `theme_color` and `background_color`.

# Keyboard and forms reference

- HTML input types to audit: `button`, `checkbox`, `color`, `date`, `datetime-local`, `email`, `file`, `hidden`, `image`, `month`, `number`, `password`, `radio`, `range`, `reset`, `search`, `submit`, `tel`, `text`, `time`, `url`, `week`.
- Mobile keyboard hints from `inputmode`: `none`, `text`, `decimal`, `numeric`, `tel`, `search`, `email`, `url`.
- Enter key hints from `enterkeyhint`: `enter`, `done`, `go`, `next`, `previous`, `search`, `send`.
- Autocomplete tokens to audit: `off`, `on`, `section-*`, `shipping`, `billing`, `name`, `honorific-prefix`, `given-name`, `additional-name`, `family-name`, `honorific-suffix`, `nickname`, `email`, `username`, `new-password`, `current-password`, `one-time-code`, `organization-title`, `organization`, `street-address`, `address-line1`, `address-line2`, `address-line3`, `address-level4`, `address-level3`, `address-level2`, `address-level1`, `country`, `country-name`, `postal-code`, `cc-name`, `cc-given-name`, `cc-additional-name`, `cc-family-name`, `cc-number`, `cc-exp`, `cc-exp-month`, `cc-exp-year`, `cc-csc`, `cc-type`, `transaction-currency`, `transaction-amount`, `language`, `bday`, `bday-day`, `bday-month`, `bday-year`, `sex`, `tel`, `tel-country-code`, `tel-national`, `tel-area-code`, `tel-local`, `tel-local-prefix`, `tel-local-suffix`, `tel-extension`, `impp`, `url`, `photo`, `webauthn`.
- Picker warning: `date`, `time`, `month`, `week`, `datetime-local`, `color` and `select` use platform-native UI that differs across iOS, Android and desktop. Keep semantics and avoid pixel-perfect assumptions.
- For code, tokens and identifiers use `autocorrect="off"`, `autocapitalize="off"` and `spellcheck="false"`.

```css
input:-webkit-autofill,
textarea:-webkit-autofill,
select:-webkit-autofill {
  -webkit-text-fill-color: CanvasText;
  box-shadow: 0 0 0 1000px Canvas inset;
  transition: background-color 9999s ease-out;
}
```

# Scroll and overflow reference

- Use `overscroll-behavior-y: none` to prevent browser-level pull-to-refresh where supported.
- Use `overscroll-behavior: contain` on nested scroll panels.
- Use `scroll-padding-top` on scroll containers with sticky headers.
- Use `scroll-margin-top` on anchor targets.
- Use `history.scrollRestoration = 'manual'` only when the router saves and restores positions.

```js
(function initialiseScrollRestoration() {
  if (!('scrollRestoration' in history)) {
    return;
  }

  const positions = new Map();
  history.scrollRestoration = 'manual';

  window.addEventListener('beforeunload', () => {
    positions.set(window.location.href, { x: window.scrollX, y: window.scrollY });
  });

  window.addEventListener('popstate', () => {
    const position = positions.get(window.location.href);

    if (position) {
      window.requestAnimationFrame(() => window.scrollTo(position.x, position.y));
    }
  });
}());
```

# Touch and pointer reference

- Use `(hover: hover)` and `(pointer: fine)` for hover enhancements.
- Use `(pointer: coarse)` for larger touch controls.
- Use `touch-action: manipulation` on controls.
- Use `-webkit-tap-highlight-color: transparent` only with a replacement press state.
- Use `-webkit-touch-callout: none` only on app controls.
- Use `user-select: none` only on controls and drag handles.

# Haptics and tactile feedback reference

| Name | Pattern | Intended use |
| --- | --- | --- |
| light | `[10]` | Ordinary tap |
| medium | `[20]` | More important tap |
| heavy | `[35]` | Strong impact |
| success | `[10, 40, 20]` | Successful commit |
| warning | `[20, 60, 20]` | Warning |
| error | `[30, 40, 30, 40, 30]` | Serious error |
| selection | `[8]` | Picker or tab selection |
| longPress | `[45]` | Long press recognised |
| swipe | `[12]` | Swipe accepted |
| refresh | `[15, 50, 15]` | Refresh threshold |
| dragSnap | `[10, 20, 10]` | Snap point |

Rules: never fire on page load, never fire every pointermove, respect preferences, keep audio fallback opt-in and always pair with visible feedback.

# Micro-interactions and native feel reference

Use `:active`, `:focus-visible`, small scale-down press states, native easing, skeletons that reserve dimensions, optimistic UI with rollback and View Transitions as progressive enhancement.

# Form factor coverage reference

| Context | Width or mode | Required behaviour |
| --- | --- | --- |
| iPhone SE | 320 CSS px | No clipped controls or input zoom |
| Modern iPhone | 390 to 440 CSS px | notch and home indicator safe areas |
| Android compact | 360 to 412 CSS px | keyboard and gesture nav |
| iPad mini | 744 CSS px portrait | tablet spacing |
| iPad Pro | 1024 CSS px and larger | split content and Stage Manager |
| Foldable folded | phone width | single column |
| Foldable unfolded | tablet or segments | master-detail and hinge awareness |
| Desktop | 1024 CSS px and larger | keyboard, hover and scrollbar correctness |
| Ultra-wide | 1600 CSS px and larger | max widths |
| TV or kiosk | large viewport | visible focus |

# Theming and system integration reference

```css
:root {
  color-scheme: light dark;
  accent-color: Highlight;
  scrollbar-color: color-mix(in srgb, CanvasText 50%, transparent) transparent;
  scrollbar-width: thin;
}

::-webkit-scrollbar {
  inline-size: 12px;
  block-size: 12px;
}

::-webkit-scrollbar-thumb {
  background: color-mix(in srgb, CanvasText 45%, transparent);
  border: 3px solid transparent;
  border-radius: 999px;
  background-clip: content-box;
}

@media (forced-colors: active) {
  :root {
    scrollbar-color: ButtonText Canvas;
  }
}
```

# Capabilities and APIs reference

| API | Native-feel use | Support warning |
| --- | --- | --- |
| Web Share API | Native share sheet | Secure context and activation rules |
| Share Target API | Receive shared content | Manifest feature, not universal |
| File System Access API | Local file workflows | Chromium-first |
| Clipboard API | Copy and paste | Secure context and permission rules |
| Wake Lock API | Timers and navigation | Release on visibility changes |
| Screen Orientation API | Games, maps and media | Locking may be restricted |
| Page Visibility API | Pause video and polling | Broad support |
| Geolocation API | Maps and local flows | Needs permission UX |
| Notifications API | Native notifications | iOS requires installed web app from 16.4 |
| Background Sync | Retry queued actions | Not universal |
| Periodic Background Sync | Periodic updates | Experimental and limited |
| Battery API | Adaptive loading | Deprecated or unavailable in many browsers |
| Network Information API | Adaptive loading | Limited support |

# Privacy and storage reference

Prefer first-party storage. Use IndexedDB for structured offline data and OPFS for large app-owned files where available. Use Storage API quota checks for large caches. Treat third-party cookies and embedded storage as unreliable. In in-app browsers, provide an open-in-browser path. Queue analytics and app actions offline with duplicate protection.

# Audit methodology

1. Inspect code statically for anti-patterns.
2. Use Chrome DevTools and Safari Responsive Design Mode for triage.
3. Use Xcode Simulator for iOS reproduction, then confirm on real iPhone.
4. Use Android Studio Emulator for foldables and Android versions, then confirm on real Android.
5. Use BrowserStack or Sauce Labs for breadth.
6. Use Lighthouse for performance and PWA triage.
7. Use PageSpeed Insights for field and lab Core Web Vitals.
8. Use WebPageTest for waterfall, LCP priority and filmstrip.
9. Install the PWA and test standalone mode.
10. Test Safari, Chrome Android, Samsung Internet, Firefox Android, Android WebView and in-app browsers.
11. Test VoiceOver on iOS and TalkBack on Android.
12. Test reduced motion, forced colours, dark mode, RTL and zoom.
13. Test offline, slow network, high latency and storage eviction.
14. Test deployment update flow with a waiting service worker.

# Modern CSS reference

Use logical properties, `:has()`, `@container`, `@layer`, CSS nesting where supported, `light-dark()`, `color-mix()`, CSS anchor positioning, Popover API and `<dialog>` when support and behaviour fit. Mark anchor positioning, some display override modes, file handlers, protocol handlers, launch handler, scope extensions and periodic background sync as experimental or partial.

```html
<button popovertarget="profile-menu" type="button">Open menu</button>
<div id="profile-menu" popover="auto">
  <button type="button">Profile</button>
  <button type="button">Sign out</button>
</div>
```

```html
<dialog id="confirm-dialog">
  <form method="dialog">
    <h2>Discard changes?</h2>
    <p>Unsaved edits will be lost.</p>
    <button value="cancel">Cancel</button>
    <button value="confirm">Discard</button>
  </form>
</dialog>

<script>
(function initialiseDialog() {
  const dialog = document.getElementById('confirm-dialog');

  window.openConfirmDialog = function openConfirmDialog() {
    if (dialog && typeof dialog.showModal === 'function') {
      dialog.showModal();
    }
  };
}());
</script>
```

# Common LLM anti-pattern catalogue

1. Full-screen root uses `height: 100vh` without intent.
2. Content wrapper uses `width: 100vw`.
3. Safe-area insets are absent.
4. Bottom nav uses hard-coded bottom spacing.
5. Header has no top safe-area padding.
6. PWA manifest exists but iOS tags are missing.
7. Manifest `start_url` is outside `scope`.
8. Only one manifest icon exists.
9. Maskable icon artwork fills the edges.
10. Service worker precaches without versioning.
11. Update handling reloads immediately.
12. Offline route does not exist.
13. Form inputs are 14px.
14. Viewport disables zoom.
15. Modal body lock uses only `overflow: hidden`.
16. Fixed modal is nested under transformed root.
17. Buttons are `div` or `span`.
18. Focus styles are removed.
19. Hover controls are required.
20. Long-press controls show selection handles.
21. Whole app disables `user-select`.
22. Whole app disables callouts.
23. Smooth scroll ignores reduced motion.
24. Skeletons shimmer under reduced motion.
25. Backdrop blur is used on large scrolling surfaces.
26. `will-change` is permanent.
27. Images omit dimensions.
28. Hero image is lazy-loaded.
29. Every image has `fetchpriority="high"`.
30. Fonts have no `font-display`.
31. Date inputs are replaced by inaccessible custom pickers.
32. Clipboard copy runs outside user gesture.
33. Web Audio starts on page load.
34. Video omits `playsinline`.
35. Autoplay video is not muted.
36. App assumes vibration works on iOS.
37. Haptics ignore preference and reduced motion.
38. Analytics assumes browser tab referrer.
39. Router does not restore scroll.
40. Anchors hide under sticky headers.
41. CSS uses physical left and right.
42. Scrollbars fail forced colours.
43. In-app browsers are not tested.
44. Foldables use a single desktop breakpoint.
45. Keyboard avoidance uses a hard-coded spacer.

# Cross-reference index

- **-webkit-overflow-scrolling**: iOS momentum scroll hint.. See the section in this skill that uses this term.
- **-webkit-tap-highlight-color**: iOS tap highlight colour.. See the section in this skill that uses this term.
- **-webkit-text-size-adjust**: Safari text inflation control.. See the section in this skill that uses this term.
- **-webkit-touch-callout**: iOS long-press callout control.. See the section in this skill that uses this term.
- **@container**: Component-local layout queries.. See the section in this skill that uses this term.
- **@font-face**: Downloadable font declaration and font-display.. See the section in this skill that uses this term.
- **accent-color**: Native checkbox, radio and range accent.. See the section in this skill that uses this term.
- **accept**: File picker media and document hints.. See the section in this skill that uses this term.
- **anchor-name**: CSS anchor positioning hook, experimental in some engines.. See the section in this skill that uses this term.
- **aria-***: Accessible names, roles and states when native HTML is insufficient.. See the section in this skill that uses this term.
- **autocapitalize**: Virtual keyboard capitalisation control.. See the section in this skill that uses this term.
- **autocomplete**: Precise autofill semantics.. See the section in this skill that uses this term.
- **autocorrect**: Platform correction control.. See the section in this skill that uses this term.
- **autoplay**: Media autoplay request subject to browser policy.. See the section in this skill that uses this term.
- **backdrop-filter**: Frosted effect that can be expensive.. See the section in this skill that uses this term.
- **Battery API**: Optional and limited battery information.. See the section in this skill that uses this term.
- **beforeinstallprompt**: Chromium install prompt event.. See the section in this skill that uses this term.
- **caret-color**: Text insertion caret colour.. See the section in this skill that uses this term.
- **clients.claim()**: Service worker immediate client control.. See the section in this skill that uses this term.
- **Clipboard API**: Secure context clipboard read and write.. See the section in this skill that uses this term.
- **color-mix()**: CSS colour interpolation.. See the section in this skill that uses this term.
- **color-scheme**: Native control colour scheme integration.. See the section in this skill that uses this term.
- **constant()**: Legacy early iOS safe-area fallback.. See the section in this skill that uses this term.
- **contain**: Layout, paint and size containment.. See the section in this skill that uses this term.
- **content-visibility**: Skip offscreen rendering.. See the section in this skill that uses this term.
- **decoding**: Image decode hint.. See the section in this skill that uses this term.
- **dialog**: Native dialog element.. See the section in this skill that uses this term.
- **display-mode**: Installed app display media query.. See the section in this skill that uses this term.
- **display_override**: Manifest display fallback list.. See the section in this skill that uses this term.
- **dvh**: Dynamic viewport height.. See the section in this skill that uses this term.
- **enterkeyhint**: Virtual keyboard enter key hint.. See the section in this skill that uses this term.
- **env()**: Environment variables including safe areas.. See the section in this skill that uses this term.
- **fetchpriority**: Fetch priority hint.. See the section in this skill that uses this term.
- **file_handlers**: Manifest file open handlers.. See the section in this skill that uses this term.
- **filter**: Visual filter and stacking context trigger.. See the section in this skill that uses this term.
- **forced-colors**: Forced colour mode media query.. See the section in this skill that uses this term.
- **history.scrollRestoration**: Browser scroll restoration control.. See the section in this skill that uses this term.
- **HTMLDialogElement.showModal()**: Native modal opening method.. See the section in this skill that uses this term.
- **inert**: Disable focus and accessibility for a subtree.. See the section in this skill that uses this term.
- **initial-scale**: Viewport initial zoom token.. See the section in this skill that uses this term.
- **inputmode**: Virtual keyboard type hint.. See the section in this skill that uses this term.
- **interactive-widget**: Viewport keyboard resize token.. See the section in this skill that uses this term.
- **launch_handler**: Manifest launch routing control.. See the section in this skill that uses this term.
- **light-dark()**: CSS colour choice by colour scheme.. See the section in this skill that uses this term.
- **loading**: Lazy or eager loading hint.. See the section in this skill that uses this term.
- **lvh**: Large viewport height.. See the section in this skill that uses this term.
- **maskable**: Adaptive icon purpose.. See the section in this skill that uses this term.
- **navigator.canShare()**: Validate Web Share payload.. See the section in this skill that uses this term.
- **navigator.serviceWorker**: Service worker registration.. See the section in this skill that uses this term.
- **navigator.share()**: Native share sheet.. See the section in this skill that uses this term.
- **navigator.standalone**: iOS Home Screen detection.. See the section in this skill that uses this term.
- **navigator.vibrate()**: Vibration API entry.. See the section in this skill that uses this term.
- **navigator.virtualKeyboard**: Virtual keyboard geometry and overlay control.. See the section in this skill that uses this term.
- **Network Information API**: Connection hints.. See the section in this skill that uses this term.
- **one-time-code**: SMS code autofill token.. See the section in this skill that uses this term.
- **overscroll-behavior**: Scroll chaining and pull-to-refresh control.. See the section in this skill that uses this term.
- **Page Visibility API**: Hidden and visible page state.. See the section in this skill that uses this term.
- **Periodic Background Sync**: Experimental periodic sync.. See the section in this skill that uses this term.
- **picture**: Responsive image art direction.. See the section in this skill that uses this term.
- **playsinline**: Inline mobile video.. See the section in this skill that uses this term.
- **popover**: Native lightweight overlay.. See the section in this skill that uses this term.
- **prefers-color-scheme**: Light or dark preference.. See the section in this skill that uses this term.
- **prefers-contrast**: Contrast preference.. See the section in this skill that uses this term.
- **prefers-reduced-data**: Reduced data preference.. See the section in this skill that uses this term.
- **prefers-reduced-motion**: Reduced motion preference.. See the section in this skill that uses this term.
- **prefers-reduced-transparency**: Reduced transparency preference.. See the section in this skill that uses this term.
- **protocol_handlers**: Manifest protocol handlers.. See the section in this skill that uses this term.
- **scope**: Manifest navigation boundary.. See the section in this skill that uses this term.
- **scope_extensions**: Experimental scope extension.. See the section in this skill that uses this term.
- **Screen Orientation API**: Screen orientation read and lock.. See the section in this skill that uses this term.
- **scroll-behavior**: Smooth scrolling control.. See the section in this skill that uses this term.
- **scroll-margin-top**: Anchor target offset.. See the section in this skill that uses this term.
- **scroll-padding-top**: Scroller top padding for anchors and snap.. See the section in this skill that uses this term.
- **scroll-snap-type**: Scroll snapping.. See the section in this skill that uses this term.
- **scrollbar-color**: Scrollbar colours.. See the section in this skill that uses this term.
- **scrollbar-width**: Scrollbar thickness.. See the section in this skill that uses this term.
- **service worker**: Programmable cache and network layer.. See the section in this skill that uses this term.
- **Share Target API**: Manifest receive-share registration.. See the section in this skill that uses this term.
- **shortcuts**: Manifest app icon actions.. See the section in this skill that uses this term.
- **skipWaiting()**: Activate a waiting service worker.. See the section in this skill that uses this term.
- **svh**: Small viewport height.. See the section in this skill that uses this term.
- **text-size-adjust**: Mobile text inflation control.. See the section in this skill that uses this term.
- **theme-color**: Browser UI and status colour.. See the section in this skill that uses this term.
- **touch-action**: Allowed touch gestures.. See the section in this skill that uses this term.
- **transform**: Transform and containing block trigger.. See the section in this skill that uses this term.
- **user-scalable**: Viewport zoom restriction token.. See the section in this skill that uses this term.
- **user-select**: Text selection control.. See the section in this skill that uses this term.
- **View Transitions API**: DOM state transition animation.. See the section in this skill that uses this term.
- **viewport-fit**: Viewport display cutout mode.. See the section in this skill that uses this term.
- **visualViewport**: Visual viewport geometry.. See the section in this skill that uses this term.
- **Wake Lock API**: Screen stay-awake request.. See the section in this skill that uses this term.
- **Web Audio API**: Generated audio feedback.. See the section in this skill that uses this term.
- **Web Share API**: Platform share sheet.. See the section in this skill that uses this term.
- **width**: Viewport token or image intrinsic size.. See the section in this skill that uses this term.
- **will-change**: Upcoming-change performance hint.. See the section in this skill that uses this term.

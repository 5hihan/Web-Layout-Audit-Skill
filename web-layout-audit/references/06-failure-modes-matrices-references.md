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

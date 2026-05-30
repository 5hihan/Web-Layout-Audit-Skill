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


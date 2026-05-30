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


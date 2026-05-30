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


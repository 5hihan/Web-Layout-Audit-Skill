# Suspicious Verification Matrix

| Risk Area | Required Checks | Evidence | Status |
| --- | --- | --- | --- |
| Intended UI implementation | User/design/issue intent mapped to actual files, components, rendered output, and state coverage |  | Unverified |
| Visual layout | Visual hierarchy, spacing, density, typography, wrapping, max widths, scrollbars, overflow, clipping, z-index, overlay placement |  | Unverified |
| Runtime geometry | Probe output for horizontal overflow, outside-viewport elements, clipped content, fixed-bottom UI, small touch targets, unnamed controls, input zoom risks, image risks |  | Unverified |
| Content states | Loading, empty, error, disabled, long content, short content, slow network, real data extremes |  | Unverified |
| Images and media | Intrinsic dimensions, aspect ratio, cropping, object-fit, responsive sources, alt/decorative handling, CLS |  | Unverified |
| Viewport and safe area | Small iPhone, modern iPhone, Android phone, landscape when relevant, tablet or foldable when relevant, browser mode, installed PWA mode if touched |  | Unverified |
| Keyboard and forms | Focused field near bottom, keyboard open and closed, iOS input zoom, Android resize behaviour, scroll restoration, primary action visibility |  | Unverified |
| Fixed bottom UI | Home indicator, Android gesture area, tab bar height, drawers/sheets/FABs/cart buttons, scroll end padding, standalone/browser differences |  | Unverified |
| PWA update flow | First install, reload, waiting service worker, update prompt, skip waiting or controlled activation, cache version bump, offline fallback, hard-reset repair path |  | Unverified |
| Haptics and motion | Enabled buttons/controls, reduced motion, high-refresh screens, low-end mobile, interaction latency, dropped frames, non-blocking input |  | Unverified |
| Accessibility and system settings | Keyboard navigation, screen-reader names, contrast, forced colours, dark mode, reduced motion, reduced data, RTL where relevant, target size |  | Unverified |
| Performance and loading | LCP, INP, CLS, image sizing, font loading, reduced data, low-end mobile interaction |  | Unverified |
| Storage and offline resilience | Quota behaviour, eviction assumptions, offline fallback, privacy-sensitive storage, clear recovery path |  | Unverified |

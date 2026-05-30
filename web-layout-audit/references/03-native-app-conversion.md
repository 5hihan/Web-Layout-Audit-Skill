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


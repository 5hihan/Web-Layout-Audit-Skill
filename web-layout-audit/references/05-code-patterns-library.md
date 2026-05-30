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


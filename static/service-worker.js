// Gem Slap — Service Worker
// Caches app shell on install; serves API levels from cache when offline

const SW_VERSION = 'gem-slap-v2';
const SHELL_CACHE = SW_VERSION + '-shell';
const LEVEL_CACHE = SW_VERSION + '-levels';

const SHELL_ASSETS = [
    '/',
    '/static/engine.js',
];

// ── Install: cache the app shell ──────────────────────────────────────────────
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(SHELL_CACHE)
            .then(cache => cache.addAll(SHELL_ASSETS))
            .then(() => self.skipWaiting())
    );
});

// ── Activate: clean up old caches ─────────────────────────────────────────────
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(
                keys
                    .filter(k => k !== SHELL_CACHE && k !== LEVEL_CACHE)
                    .map(k => caches.delete(k))
            )
        ).then(() => self.clients.claim())
    );
});

// ── Fetch: cache-first for levels, network-first for shell ────────────────────
self.addEventListener('fetch', event => {
    const url = new URL(event.request.url);

    // API level requests — cache first, then network
    if (url.pathname.startsWith('/api/level/')) {
        event.respondWith(
            caches.open(LEVEL_CACHE).then(async cache => {
                const cached = await cache.match(event.request);
                if (cached) return cached;
                try {
                    const res = await fetch(event.request);
                    if (res.ok) cache.put(event.request, res.clone());
                    return res;
                } catch {
                    // Offline and not cached — return a clear error response
                    return new Response(
                        JSON.stringify({ error: 'offline' }),
                        { status: 503, headers: { 'Content-Type': 'application/json' } }
                    );
                }
            })
        );
        return;
    }

    // Shell assets — network first, fall back to cache
    if (url.pathname === '/' || url.pathname.startsWith('/static/')) {
        event.respondWith(
            fetch(event.request)
                .then(res => {
                    // Update shell cache whenever online
                    if (res.ok) {
                        caches.open(SHELL_CACHE)
                            .then(cache => cache.put(event.request, res.clone()));
                    }
                    return res;
                })
                .catch(() => caches.match(event.request))
        );
        return;
    }
});

// ── Message: explicit cache-a-level command from the game ─────────────────────
self.addEventListener('message', event => {
    if (event.data && event.data.type === 'CACHE_LEVEL') {
        const { url } = event.data;
        caches.open(LEVEL_CACHE).then(async cache => {
            const existing = await cache.match(url);
            if (!existing) {
                try {
                    const res = await fetch(url);
                    if (res.ok) cache.put(url, res.clone());
                } catch { /* offline during prefetch — skip silently */ }
            }
        });
    }
});

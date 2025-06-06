const CACHE_NAME = "thed_ivu_bot_cache_v1";
const URLS_TO_CACHE = [
    "/",
    "/index.html",
    "/manifest.webmanifest",
    "/favicon.ico",
    "/icons/icon-192.png",
    "/icons/icon-512.png"
];

// 📦 INSTALLATION
self.addEventListener("install", event => {
    console.log("🧠 THED_IVU_BOT PWA installé.");
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            console.log("✅ Mise en cache des ressources");
            return cache.addAll(URLS_TO_CACHE);
        })
    );
    self.skipWaiting();
});

// 🧼 ACTIVATION
self.addEventListener("activate", event => {
    console.log("🧠 THED_IVU_BOT PWA activé.");
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.filter(name => name !== CACHE_NAME).map(name => caches.delete(name))
            );
        })
    );
    return self.clients.claim();
});

// 🌐 INTERCEPTION DES REQUÊTES
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        })
    );
});
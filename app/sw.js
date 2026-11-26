// Zikr: keeps the app on the phone so it opens offline. Serves the saved copy at once and
// fetches a fresh one in the background; the next launch uses the update.
const CACHE = "zikr-41d226429e";
const FILES = ["./", "index.html", "manifest.webmanifest", "icon-180.png", "icon-192.png", "icon-512.png", "icon-maskable-512.png", "fonts/scheherazade-new-arabic-400.woff2", "fonts/scheherazade-new-arabic-700.woff2", "qcf/qcf_v2.json"];
// The Quran.com page fonts (one per Mushaf page) are kept in their own store once fetched, across app updates.
const QCF_CACHE = "zikr-qcf-fonts";
const QCF_HOST = "static.qurancdn.com";
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES.map(f => new Request(f, { cache: "reload" })))).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith("zikr-") && k !== CACHE && k !== QCF_CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  if (e.request.method === "GET" && url.hostname === QCF_HOST && url.pathname.includes("/fonts/quran/")) {
    e.respondWith(caches.open(QCF_CACHE).then(async c => (await c.match(e.request)) || fetch(e.request).then(r => { if (r.ok) c.put(e.request, r.clone()); return r; })));
    return;
  }
  if (e.request.method !== "GET" || url.origin !== location.origin) return;   // fonts etc. go to the network as usual
  e.respondWith(caches.open(CACHE).then(async c => {
    const hit = await c.match(e.request, { ignoreSearch: true });
    const fresh = fetch(e.request).then(r => { if (r.ok) c.put(e.request, r.clone()); return r; }).catch(() => hit);
    return hit || fresh;
  }));
});

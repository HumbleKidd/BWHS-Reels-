self.addEventListener("install", (event) => {
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  const isPage = event.request.mode === "navigate" || url.pathname === "/" || url.pathname.endsWith("/index.html");
  if (isPage) {
    event.respondWith((async () => {
      const res = await fetch(event.request);
      const type = res.headers.get("content-type") || "";
      if (!type.includes("text/html")) return res;
      const html = await res.text();
      if (html.includes("reels-boot.js")) return new Response(html, { headers: { "Content-Type": "text/html" } });
      return new Response(html.replace("</body>", '<script src="/reels-boot.js"></script></body>'), { headers: { "Content-Type": "text/html" } });
    })());
    return;
  }
  event.respondWith(fetch(event.request).catch(() => caches.match(event.request)));
});

"""Builds the installable web app (PWA) into app/ for GitHub Pages.
Run after build.py:  python3 build_site.py
It wraps the built page (../index.html) in a full HTML document with the app icon, manifest and an
offline service worker, so it can be added to the home screen and opened like an app."""
import hashlib, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(REPO, "app")
page = open(os.path.join(HERE, "..", "index.html"), encoding="utf8").read()
version = hashlib.sha1(page.encode()).hexdigest()[:10]
head = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#fffdf9">
<script>window.ZIKR_BUILD = "__BUILD__";</script>
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Zikr">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="description" content="Zikr counter, Hisn al-Muslim, the Quran ayah by ayah, prayer times and the adhan.">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icon-180.png">
<style>html, body { margin: 0; padding: 0; } * { box-sizing: border-box; }</style>
<script>
// Updates: the app checks for a new version when it opens and when it comes back to the screen; once the new
// version is downloaded it switches to it straight away (instead of on the next opening).
if ("serviceWorker" in navigator) addEventListener("load", () => {
  const had = !!navigator.serviceWorker.controller;
  navigator.serviceWorker.register("sw.js").then(reg => {
    document.addEventListener("visibilitychange", () => { if (!document.hidden) reg.update().catch(() => {}); });
  }).catch(() => {});
  navigator.serviceWorker.addEventListener("controllerchange", () => { if (had && !window.__zikrReloading) { window.__zikrReloading = true; location.reload(); } });
});
</script>
</head><body>
"""
os.makedirs(OUT, exist_ok=True)
head = head.replace("__BUILD__", version)   # shown at the bottom of Home, to tell which version a phone has
open(os.path.join(OUT, "index.html"), "w", encoding="utf8").write(head + page + "\n</body></html>\n")
for f in ["manifest.webmanifest", "privacy.html", "icon.svg", "icon-180.png", "icon-192.png", "icon-512.png", "icon-maskable-512.png"]:
    shutil.copy(os.path.join(HERE, "site", f), os.path.join(OUT, f))
# The word codes for drawing the Quran with Quran.com's page fonts (see app.html).
os.makedirs(os.path.join(OUT, "qcf"), exist_ok=True)
shutil.copy(os.path.join(HERE, "qcf", "qcf_v2.json"), os.path.join(OUT, "qcf", "qcf_v2.json"))
# The Quran font ships with the app (see app.html), so it is there offline too.
os.makedirs(os.path.join(OUT, "fonts"), exist_ok=True)
for f in os.listdir(os.path.join(HERE, "fonts")): shutil.copy(os.path.join(HERE, "fonts", f), os.path.join(OUT, "fonts", f))
open(os.path.join(OUT, "sw.js"), "w", encoding="utf8").write(open(os.path.join(HERE, "site", "sw.js"), encoding="utf8").read().replace("__VERSION__", version))
print("built", OUT, "version", version, f"{os.path.getsize(os.path.join(OUT, 'index.html')) / 1e6:.2f} MB")

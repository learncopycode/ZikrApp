# Zikr · v1.1

A dhikr counter with Hisn al-Muslim, duas from hadith (HadeethEnc, Bukhari, Muslim), the Quran ayah by ayah (with tafsir, Bangla), after-prayer adhkar,
prayer times and the adhan. Every religious text in it is taken from a published source (see `web/src/README.md`).

Everything for Zikr lives in this repository:

| Folder | What it is |
|---|---|
| `app/` | The finished app as an installable web app (built; served by GitHub Pages). Open on iPhone in Safari → Share → Add to Home Screen. |
| `web/` | Sources: `web/src/app.html` and data, built by `web/src/build.py` into `web/index.html`, then `web/src/build_site.py` into `app/`. |
| `ios-app/` | The iPhone app for the App Store / TestFlight: `app/` in a native shell (Capacitor) with full-adhan alarms. Step-by-step guide in `ios-app/README.md`. |
| `legacy-swiftui/` | The first native SwiftUI version (not maintained; the app above replaced it). |

The iPhone build itself runs from `/.github/workflows/ios-testflight.yml` (GitHub only runs workflows from that place).

## Install it on an iPhone (free, no Mac)

1. Turn on GitHub Pages once: this repository → **Settings → Pages** → Source **Deploy from a branch**,
   branch **main**, folder **/ (root)** → **Save**. After a minute or two the site is live.
2. On the iPhone, open https://learncopycode.github.io/ZikrApp/app/ in **Safari**.
3. Tap **Share → Add to Home Screen → Add**.

Counts are kept on the phone. Stats → **Save backup** writes them to a file (Files / iCloud Drive);
**Restore from file** brings them back after reinstalling or on a new phone.

**Links** (once GitHub Pages is on)
- App: https://learncopycode.github.io/ZikrApp/app/
- Privacy policy: https://learncopycode.github.io/ZikrApp/app/privacy.html

**Version:** `appVersion` in `ios-app/package.json` and `APP_VERSION` in `web/src/app.html`.

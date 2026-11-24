"""Compare the app's Quran (web/src/quran.js) with QuranEnc's official text, ayah by ayah.
Usage: check_quran.py quran.js <dir with en_<sura>.json from quranenc api/v1/translation/sura/english_saheeh>"""
import json, re, sys, unicodedata
qjs, d = sys.argv[1:3]
src = open(qjs, encoding="utf8").read()
m = re.search(r"const QURAN_TEXT\s*=\s*(\[.*?\]);\s*\n", src, re.S)
T = json.loads(m.group(1))
nfc = lambda t: unicodedata.normalize("NFC", t or "").strip()
ar_diff, en_diff, total = [], [], 0
for s in range(1, 115):
    off = json.load(open(f"{d}/en_{s}.json", encoding="utf8"))["result"]
    if len(off) != len(T[s - 1]): print("AYAH COUNT DIFFERS in surah", s, len(off), len(T[s - 1]))
    for o in off:
        a = int(o["aya"]); total += 1
        app_ar, app_en = T[s - 1][a - 1][0], T[s - 1][a - 1][1]
        if nfc(app_ar) != nfc(o["arabic_text"]): ar_diff.append((s, a, app_ar, o["arabic_text"]))
        off_en = re.sub(r"\[\d+\]", "", o["translation"]).strip()
        if re.sub(r"\s+", " ", app_en).strip() != re.sub(r"\s+", " ", off_en): en_diff.append((s, a, app_en, off_en))
print("ayahs compared:", total)
print("Arabic identical:", total - len(ar_diff), "| different:", len(ar_diff))
print("English identical:", total - len(en_diff), "| different:", len(en_diff))
json.dump({"ar": ar_diff, "en": en_diff}, open(d + "/diffs.json", "w", encoding="utf8"), ensure_ascii=False)
for s, a, x, y in ar_diff[:5]:
    print(f"\nAR {s}:{a}\n app: {x[:120]}\n off: {y[:120]}")

# ---- what the differences are: the same signs encoded two ways (QuranEnc uses older stand-in marks for open
# tanween), the order marks are stored in, and spaces do not change a letter or a vowel. Anything else is real.
import unicodedata
EQ = {"ࣰ": "ٗ", "ࣱ": "ٞ", "ࣲ": "ٖ", "ـ": ""}
def clusters(t):
    t = "".join(EQ.get(c, c) for c in unicodedata.normalize("NFC", t)); out = []
    for c in t:
        if c.isspace(): continue
        if unicodedata.category(c) == "Mn":
            if out: out[-1][1].append(c)
        else: out.append([c, []])
    return [(b, tuple(sorted(m))) for b, m in out]
real = [(s, a) for s, a, x, y in ar_diff if clusters(x) != clusters(y)]
print("Arabic ayahs with a real difference in letters or marks:", len(real), real[:20])

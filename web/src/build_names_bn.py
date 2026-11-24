"""Bangla meanings of the Names of Allah from the Bangla edition of Jami` at-Tirmidhi 3507 (fawazahmed0/hadith-api,
ben-tirmidhi), the hadith the app's list of Names comes from. The hadith lists them in order as "আর-রহমান (মহান দয়ালু), …".
Only typing slips are corrected (listed in FIXES); the Assamese letter ৰ, used by mistake for র, is normalised.
Usage: build_names_bn.py ben-tirmidhi.json names.json out.json"""
import json, re, sys
src, names_path, out = sys.argv[1:4]
t = next(h["text"] for h in json.load(open(src, encoding="utf8"))["hadiths"] if h["hadithnumber"] == 3507)
body = t[t.index("তিনি আর-রহমান") + len("তিনি "): t.index("। নাম সমূহ")]
pairs = [(a.strip(" ,"), b.strip()) for a, b in re.findall(r"([^,()]+?)\s*\(([^)]+)\)", body)]
FIXES = {"পুখানুপুঙ্খ": "পুঙ্খানুপুঙ্খ", "চিরঞ্জাব": "চিরঞ্জীব", "সর্বদশী": "সর্বদর্শী"}
def fix(s):
    s = s.replace("ৰ", "র")
    for a, b in FIXES.items(): s = s.replace(a, b)
    return s
names = json.load(open(names_path, encoding="utf8"))["names"]
print("pairs", len(pairs), "| app names", len(names), "| first app name", names[0]["translit"], names[1]["translit"])
offset = len(names) - len(pairs)   # the app list starts with "Allah", which the hadith names without a meaning
res = {}
for i, (nm, mean) in enumerate(pairs):
    res[names[i + offset]["id"]] = {"bn_name": fix(nm), "bn": fix(mean)}
for k in list(res)[:3] + list(res)[45:48] + list(res)[-3:]: print(k, res[k], "|", next(n["translit"] + " · " + n["meaning"] for n in names if n["id"] == k))
# The first entry of the list, "Allahu la ilaha illa Huwa", is the hadith's own "তিনিই আল্লাহ যিনি ব্যতীত আর কোন ইলাহ নেই".
m = re.search(r"(তিনিই আল্লাহ যিনি ব্যতীত আর কোন ইলাহ নেই)", t)
if m and offset == 1: res[names[0]["id"]] = {"bn_name": "আল্লাহ", "bn": m.group(1)}
json.dump(res, open(out, "w", encoding="utf8"), ensure_ascii=False, separators=(",", ":"))

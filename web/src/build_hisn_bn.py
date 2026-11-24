"""Bangla Hisnul Muslim (IslamHouse, bn_Hisnul_Elmuslim.doc, converted with antiword -m UTF-8.txt) → per-dua Bangla.
The book numbers each dua as the Arabic edition does: "175-«Arabic»", then "(Bangla transliteration)", then
"১৭৫- “Bangla meaning”[footnote]". A dua with several parts is "176-(1) «…»" / "১৭৬-(১) “…”".
Usage: parse_hisn_bn.py doc.txt hisn.json out.json"""
import json, re, sys
src, hisn_path, out = sys.argv[1:4]
lines = [l.rstrip() for l in open(src, encoding="utf8")]
BN = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")
ar_re = re.compile(r"^\s*(\d+)\s*-\s*(?:\((\d+)\))?\s*(.*)$")
bn_re = re.compile(r"^\s*([০-৯]+)\s*-\s*(?:\(([০-৯]+)\))?\s*(.*)$")
head_re = re.compile(r"^\s*[০-৯]+\s*\.\s+\S")
entries = {}   # n -> {"parts": {part: {"ar":..., "tl":..., "bn":...}}}
cur = None
i = 0
while i < len(lines):
    l = lines[i]
    m = ar_re.match(l)
    if m and re.search(r"[؀-ۿ]", m.group(3) or ""):
        n, part = int(m.group(1)), int(m.group(2) or 0)
        e = entries.setdefault(n, {}); cur = e.setdefault(part, {"ar": "", "tl": "", "bn": ""})
        cur["ar"] = m.group(3).strip(); cur["owner"] = n
        i += 1; continue
    m = bn_re.match(l)
    if m and not head_re.match(l):
        n, part = int(m.group(1).translate(BN)), int((m.group(2) or "0").translate(BN))
        e = entries.setdefault(n, {}); p = e.setdefault(part, {"ar": "", "tl": "", "bn": ""})
        text = [m.group(3).strip()]
        j = i + 1   # a meaning can run over more paragraphs, up to the next numbered line or heading
        while j < len(lines):
            nl = lines[j]
            if ar_re.match(nl) or bn_re.match(nl) or head_re.match(nl): break
            if nl.strip() and not nl.strip().startswith("(") and not re.match(r"^\s*\[\d+\]", nl) and not nl.lstrip().startswith("|"): text.append(nl.strip())
            j += 1
        p["bn"] = re.sub(r"\[\d+\]", "", " ".join(t for t in text if t)).strip()
        i = j; continue
    # Some entries put a numbered label first ("৭৯-(৫) [সায়্যিদুল ইসতিগফার:]") and the meaning, unnumbered, after the Arabic.
    if cur is not None and l.strip().startswith("“"):
        cur.setdefault("loose", []).append(re.sub(r"\[\d+\]", "", l.strip()))
    i += 1
hisn = {int(e["n"]): e for e in json.load(open(hisn_path, encoding="utf8")) if str(e.get("n", "")).isdigit()}
norm = lambda t: re.sub(r"[^ء-ي]", "", re.sub(r"[ً-ٰٟـ]", "", t or "")).replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ى", "ي").replace("ة", "ه")
res, agree, checked = {}, 0, 0
for n, parts in sorted(entries.items()):
    for k in parts:
        p = parts[k]
        if p.get("loose") and "“" not in p["bn"]: p["bn"] = (p["bn"] + " " + " ".join(p["loose"])).strip()
    bn = " ".join(parts[k]["bn"] for k in sorted(parts) if parts[k]["bn"])
    ar = " ".join(parts[k]["ar"] for k in sorted(parts) if parts[k]["ar"])
    if not bn: continue
    res[n] = bn
    if n in hisn and ar:
        checked += 1; a, b = norm(ar), norm(hisn[n]["arabic"])
        if a[:20] == b[:20] or (len(b) > 15 and (b[:30] in a or a[:30] in b)): agree += 1
        elif checked - agree <= 12: print("mismatch?", n, a[:30], "|", b[:30])
json.dump({"source": "Hisnul Muslim (Bangla), IslamHouse: https://d1.islamhouse.com/data/bn/ih_books/single2/bn_Hisnul_Elmuslim.doc", "duas": res}, open(out, "w", encoding="utf8"), ensure_ascii=False, indent=0)
print("entries", len(entries), "with bangla", len(res), "| arabic checked", checked, "agree", agree, "| app hisn entries", len(hisn), "covered", sum(1 for n in hisn if n in res))

# ---- what the app shows: "h<n>" whole entries (the Arabic the book repeats inline is dropped, the app shows it
# above), "v<n>" the dhikr quoted inside a narration (the Bangla right after each «Arabic»), "t-…" single phrases
# taken out of longer duas (the matching sentence of the book's Bangla).
def no_ar(t): return re.sub(r"\s+", " ", re.sub(r"«[^»]*»\.?", " ", t)).strip()
def quotes(t): return [q.strip() for q in re.findall(r"[“‘]([^”’]+)[”’]", t)]
def after_ar(t):   # the Bangla meaning given right after each quoted Arabic dhikr
    out = []
    for m in re.finditer(r"«[^»]*»\.?\s*[“‘]([^”’]+)[”’]", t): q = m.group(1).strip(); out.append(q if q[-1:] in "।!?" else q + "।")
    return " ".join(out)
app = {f"h{n}": no_ar(t) for n, t in res.items()}
for n in (188, 250, 254, 255, 256, 259, 260, 261, 262, 263, 264):
    if after_ar(res[n]): app[f"v{n}"] = after_ar(res[n])
if "v261" in app: app["v257"] = app["v261"]   # the same four words; the book's narration for 257 gives them only transliterated
q69, q66 = quotes(res[69]), quotes(no_ar(res[66])) if False else quotes(res[66])
s69 = [x.strip() + "।" for x in q69[0].split("।") if x.strip()]
app.update({"t-subhanallah": s69[0], "t-alhamdulillah": s69[1], "t-allahuakbar": s69[2], "t-tahlil": q69[1],
            "t-astaghfirullah": q66[0], "t-antassalam": q66[1]})
json.dump({"source": "হিসনুল মুসলিম (বাংলা), IslamHouse", "url": "https://islamhouse.com/bn/books/2803/", "bn": app}, open(out.replace(".json", "_app.json"), "w", encoding="utf8"), ensure_ascii=False, separators=(",", ":"))
for k in ("t-subhanallah", "t-alhamdulillah", "t-allahuakbar", "t-tahlil", "t-astaghfirullah", "t-antassalam", "v256", "v257", "v264", "v188"): print(k, "|", app.get(k, "")[:120])

"""HadeethEnc.com explanations for the hadith in the app.

Input: the download made by tools/fetch_hadeethenc.py (Arabic, Malay, Indonesian, English).
Output:
  kutub/he/<k>.json      the HadeethEnc entries, k = id % 32, texts unchanged (HadeethEnc terms: credit, no changes)
  tools/hadeethenc_map.json   {"<book>:<number>": [HadeethEnc ids]}, read by build_kutub.py
Linking: HadeethEnc names the books (e.g. "متفق عليه", "رواه أبو داود"); its Arabic text is looked for in those books only.
 - up to 12 content words: the same words in the same order must appear in our hadith (at most 8 hits);
 - longer: at least 85% of its word triples must appear in our hadith.
 Formulas (ﷺ, radiyallahu 'anhu, "the Messenger of Allah", qala, 'an ...) are left out before comparing, so they can't
 make two different hadith look alike. Checked by hand on samples; anything not matched is simply not linked.
Usage: python3 build_hadeethenc.py <hadeethenc.json> <kutub dir>"""
import json, re, glob, os, sys, collections
RAW, KUT = sys.argv[1], sys.argv[2]
DIAC = re.compile('[ً-ٰٟۖ-ۭـ‏‎]')
FORM = re.compile(r'صلي الله عليه وسلم|رضي الله عن(?:ه|هما|ها|هم)|عز وجل|تبارك وتعالي|تعالي|رسول الله|النبي|نبي الله')
STOPW = {'قال', 'قالت', 'عن', 'ان', 'انه', 'يقول', 'فقال', 'سمعت', 'و', 'في', 'من'}
def nw(s):
    s = re.sub(r'[^ء-ي ]', ' ', DIAC.sub('', s or '')).replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا').replace('ى', 'ي').replace('ة', 'ه')
    s = FORM.sub(' ', ' '.join(s.split()).replace('رضى', 'رضي').replace('صلى', 'صلي'))
    return [w for w in s.split() if w not in STOPW]
BK = {'البخاري': 'bukhari', 'مسلم': 'muslim', 'أبو داود': 'abudawud', 'الترمذي': 'tirmidhi', 'النسائي': 'nasai', 'ابن ماجه': 'ibnmajah', 'مالك': 'malik'}
def books(attr):
    s = {'bukhari', 'muslim'} if 'متفق عليه' in attr else set()
    return s | {v for k, v in BK.items() if k in attr}
d = json.load(open(RAW))
idx, full, matn3 = {}, {}, {}
for f in glob.glob(os.path.join(KUT, '*', '*.json')):
    b = os.path.basename(os.path.dirname(f))
    if b == 'he' or f.endswith('books.json'): continue
    ix = idx.setdefault(b, collections.defaultdict(set))
    for h in json.load(open(f))['h']:
        w = nw(h[2]); full.setdefault(b, []).append((h[0], ' ' + ' '.join(w) + ' '))
        c = h[7] or {}
        if c.get('a'):
            wm = nw(h[2][c['a']:]); matn3.setdefault(b, []).append((h[0], {' '.join(wm[j:j + 3]) for j in range(len(wm) - 2)}))
        for j in range(len(w) - 2): ix[' '.join(w[j:j + 3])].add(h[0])
links, stat = collections.defaultdict(list), collections.Counter()
for i, v in sorted(d.items(), key=lambda x: int(x[0])):
    a = v.get('ar')
    if not a: continue
    bs = books(a.get('attribution', '')) & set(idx)
    if not bs: stat['in other books only'] += 1; continue
    for b in bs: matn3.setdefault(b, [])
    words = [w for s in (re.findall(r'«([^»]+)»', a['hadeeth']) or [a['hadeeth'].split(':', 1)[-1]]) for w in nw(s)]
    hits = []
    if len(words) < 2: stat['too short'] += 1; continue
    if len(words) <= 12:
        q = ' ' + ' '.join(words) + ' '
        hits = [(b, n) for b in bs for n, t in full[b] if q in t]
        if len(hits) > 8: hits = []
    else:
        tri = {' '.join(words[j:j + 3]) for j in range(len(words) - 2)}
        for b in bs:
            cnt = collections.Counter(n for t in tri for n in idx[b].get(t, ()))
            hits += [(b, n) for n, c in cnt.items() if c / len(tri) >= 0.85]
    # the other way round: a shorter narration of ours (text only, without the chain) inside HadeethEnc's text
    if len(words) > 12:
        tri_he = {' '.join(words[j:j + 3]) for j in range(len(words) - 2)}
        for b in bs:
            for n, t3 in matn3[b]:
                if len(t3) >= 8 and (b, n) not in hits and sum(x in tri_he for x in t3) / len(t3) >= 0.9: hits.append((b, n)); stat['by our shorter text'] += 1
    stat['linked' if hits else 'not found'] += 1
    for b, n in hits: links[f'{b}:{n}'].append(int(i))
print(dict(stat), 'links', sum(len(x) for x in links.values()), 'hadith with an explanation', len(links))
json.dump(dict(sorted(links.items())), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hadeethenc_map.json'), 'w'), separators=(',', ':'))
used = sorted({i for x in links.values() for i in x})
KEEP = ['title', 'hadeeth', 'attribution', 'grade', 'explanation', 'hints', 'words_meanings', 'hadeeth_intro', 'reference']
out = collections.defaultdict(dict)
for i in used:
    out[i % 32][str(i)] = {L: {k: e[k] for k in KEEP if e.get(k)} for L, e in d[str(i)].items()}
os.makedirs(os.path.join(KUT, 'he'), exist_ok=True)
for k, v in out.items():
    json.dump(v, open(os.path.join(KUT, 'he', f'{k}.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
langs = collections.Counter(L for i in used for L in d[str(i)])
print('entries', len(used), 'languages', dict(langs))

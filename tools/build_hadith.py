"""Hadith linked to ayat, only where the hadith books themselves make the link.

Sahih al-Bukhari, Book 65 (Kitab at-Tafsir): each chapter (bab) heading by al-Bukhari names the ayah.
  The ayah is taken from the chapter heading's reference on Sunnah.com (e.g. "(V.2:31)") and checked
  against the Qur'an words quoted in al-Bukhari's Arabic heading. Untitled chapters ("باب" alone) follow
  the chapter before them, as the commentators explain them. Chapters naming a whole surah go to the surah.
Sahih Muslim, Book 56 (Kitab at-Tafsir): the ayah is the one the hadith itself quotes (matched word for word).
  Narrations with no quoted ayah are left out, except "same chain" repeats of the hadith just before.

Sources: Arabic + English from Sunnah.com (Bukhari via the freococo/sunnah_dataset copy, CC BY-NC-SA 4.0;
Muslim via fawazahmed0/hadith-api). Indonesian from fawazahmed0/hadith-api (from tafsirq.com; translator not named).
Output: hadith/NNN.json per surah, hadith/review.txt listing every link that could not be confirmed both ways."""
import json, re, os, sys, glob, urllib.request
Q = json.load(open('tools/quran-plain.json')); NAMES = json.load(open('tools/surah-names.json'))
def norm(t):
    t = re.sub(r'[ً-ٰٟۖ-ۭـ]', '', t or '')
    t = re.sub('[إأآٱا]', 'ا', t).replace('ى', 'ي').replace('ة', 'ه').replace('ؤ', 'و').replace('ئ', 'ي')
    return re.sub(r'[^ء-ي ]', ' ', t).split()
AY = {}
for s, n, t in Q: AY.setdefault(s, {})[n] = norm(t)
def run(a, b):
    m = 0
    for i in range(len(a)):
        for j in range(len(b)):
            k = 0
            while i + k < len(a) and j + k < len(b) and a[i + k] == b[j + k]: k += 1
            m = max(m, k)
    return m
def match(toks, surahs):
    best = (0, None)
    for s in surahs:
        for n, at in AY[s].items():
            r = run(toks, at)
            if r > best[0]: best = (r, (s, n))
    return best
def jget(u):
    with urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'MyPersonalQuran/1.0'}), timeout=120) as r: return json.load(r)
FZ = 'https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/'
def edition(e): return {h['hadithnumber']: h for h in jget(FZ + e + '.min.json')['hadiths']}
out = {}; review = []
def add(s, a1, a2, item):
    d = out.setdefault(s, {'ayat': {}, 'surah': []})
    if a1 is None: d['surah'].append(item)
    else:
        item['range'] = [a1, a2]
        for a in range(a1, a2 + 1): d['ayat'].setdefault(str(a), []).append(item)

# ---------- Bukhari ----------
import pandas as pd
from huggingface_hub import snapshot_download
p = snapshot_download('freococo/sunnah_dataset', repo_type='dataset', local_dir='/tmp/ds')
df = pd.concat([pd.read_parquet(f) for f in glob.glob('/tmp/ds/**/*.parquet', recursive=True)])
df = df.astype(object).where(pd.notnull(df), None)
b = df[(df['collection'] == 'Sahih al-Bukhari') & (df['book_no'].astype(str).isin(['65', '65.0']))].to_dict('records')
if not b: raise SystemExit('no Bukhari book 65 rows')
num = lambda h: int(re.search(r'(\d+)', h['ref_raw']).group(1))
b.sort(key=lambda h: (num(h), h['freococo_id']))
ind_b = edition('ind-bukhari')
groups = []
for h in b:
    key = (h['chapter_en'] or '', h['chapter_ar'] or '')
    if groups and groups[-1]['key'] == key: groups[-1]['h'].append(h)
    else: groups.append({'key': key, 'h': [h]})
pat = re.compile(r'\(?(?:V\.?\s*)?(\d{1,3})\s*:\s*(\d{1,3})(?:\s*[-–]\s*(?:(\d{1,3})\s*:\s*)?(\d{1,3}))?\)?')
def surah_by_name(en, ar):
    m = re.match(r"\s*Surat\s+(.+?)\s*(\(|$)", en or '')
    if not m: return None
    key = re.sub(r"[^a-z]", '', m.group(1).lower().replace('al-', '').replace('ash-', '').replace('an-', ''))
    for i, nm in enumerate(NAMES):
        k2 = re.sub(r"[^a-z]", '', nm.lower().replace('al-', '').replace('ash-', '').replace('an-', '').replace('ā','a').replace('ī','i').replace('ū','u').replace('ḥ','h').replace('ṣ','s').replace('ḍ','d').replace('ṭ','t').replace('ẓ','z').replace('‘','').replace('’',''))
        if key == k2 or key.startswith(k2) or k2.startswith(key): return i + 1
    return None
cur = 1; prev = None; seen = set()
for g in groups:
    en, ar = g['key']; refs = [r for r in pat.findall(en) if 1 <= int(r[0]) <= 114]
    toks = [t for t in norm(ar) if t not in ('باب',)]
    target = None; how = ''
    sn = surah_by_name(en, ar) or (1 if 'فَاتِحَةِ الْكِتَابِ' in ar else None)
    if refs:
        s = int(refs[0][0]); a1 = int(refs[0][1]); last = refs[-1]
        a2 = int(last[3]) if last[3] and (not last[2] or int(last[2]) == s) else (int(last[1]) if int(last[0]) == s else a1)
        a2 = max(a1, min(a2, max(AY[s])))
        r, where = match(toks, [s]) if toks else (0, None)
        confirmed = where and where[0] == s and a1 - 1 <= where[1] <= a2 + 3 and r >= 2
        if not confirmed and toks and r >= 2 and run(toks, AY[s][a1]) >= 2: confirmed = True
        target = (s, a1, a2); how = 'bab'
        if not confirmed: review.append(f'BUKHARI {[num(h) for h in g["h"]]} heading ref {s}:{a1}-{a2} not confirmed by Arabic quote (best {where}, run {r}): {en[:90]} | {ar[:90]}')
    elif sn:
        target = (sn, None, None); how = 'surah'
    elif toks and len(toks) >= 1 and not (len(toks) == 0):
        r, where = match(toks, [cur, min(114, cur + 1)])
        if r >= 2: target = (where[0], where[1], where[1]); how = 'bab-arabic'; review.append(f'BUKHARI {[num(h) for h in g["h"]]} no English ref; Arabic heading matched {where} (run {r}): {ar[:90]}')
    if target is None and prev is not None and norm(ar) in ([], ['باب']):
        target = prev; how = 'untitled'
    if target is None:
        review.append(f'BUKHARI {[num(h) for h in g["h"]]} LEFT OUT, no ayah found: {en[:90]} | {ar[:90]}'); continue
    for h in g['h']:
        if h['freococo_id'] in seen: continue
        seen.add(h['freococo_id']); n = num(h)
        ind = ind_b.get(n, {}).get('text', '')
        add(target[0], target[1], target[2], {'c': 'bukhari', 'ref': h['ref_raw'].replace('Sahih al-Bukhari ', ''), 'inbook': h['in_book_ref_raw'],
            'url': h['url'], 'bab_en': en, 'bab_ar': ar, 'how': how, 'ar': h['arabic_full'], 'en': h['english_full'], 'id': ind, 'grade': 'Sahih'})
    prev = target; cur = target[0]

# ---------- Muslim ----------
ar_m, en_m, id_m = edition('ara-muslim'), edition('eng-muslim'), edition('ind-muslim')
last = None
for n in range(7523, 7564):
    h = ar_m[n]; an = h.get('arabicnumber') or en_m[n].get('arabicnumber') or ar_m.get(n - 1, {}).get('arabicnumber')
    an = str(an); base, _, sub = an.partition('.')
    ref = base + (chr(96 + int(sub)) if sub and int(sub) else '')
    quotes = re.findall(r'[{﴿]([^}﴾]+)[}﴾]', h['text'])
    best = (0, None)
    for q in quotes:
        r = match(norm(q), range(1, 115))
        if r[0] > best[0]: best = r
    tgt = None
    if best[0] < 4 and last:    # the quote may not be marked: look for the ayah's words in the text, in the surah of the hadith before
        r = match(norm(h['text']), [last[0]])
        if r[0] >= 5: best = r
    if best[0] >= 4: tgt = best[1]; last = tgt
    elif 'same chain' in en_m[n]['text'] or 'same chain' in en_m[n]['text'].lower() or 'another chain' in en_m[n]['text'].lower():
        tgt = last
    if not tgt:
        review.append(f'MUSLIM {ref} LEFT OUT, no quoted ayah: {en_m[n]["text"][:100]}'); continue
    add(tgt[0], tgt[1], tgt[1], {'c': 'muslim', 'ref': ref, 'inbook': f'Book 56', 'url': f'https://sunnah.com/muslim:{ref}',
        'bab_en': '', 'bab_ar': '', 'how': 'quote', 'ar': h['text'], 'en': en_m[n]['text'], 'id': id_m.get(n, {}).get('text', ''), 'grade': 'Sahih'})

os.makedirs('hadith', exist_ok=True)
for s, d in out.items():
    json.dump(d, open(f'hadith/{s:03d}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
json.dump({'surahs': sorted(out), 'counts': {s: sum(len(v) for v in d['ayat'].values()) + len(d['surah']) for s, d in out.items()}},
          open('hadith/index.json', 'w'), indent=0)
open('hadith/review.txt', 'w').write('\n'.join(review) + '\n')
print(len(out), 'surahs;', len(review), 'review lines')

"""Hadith linked to the Qur'an (Azli, 17 Oct 2026): for each ayah, the hadith in this app's books that quote it.
Found by matching the Arabic: a hadith is linked when its matn contains the ayah word for word (normalised spelling),
or at least 6 consecutive words of a longer ayah; ayat shorter than 4 words are left out (too common to be sure).
Also linked: the English of al-Bukhari's and Muslim's tafsir hadith that names the ayah, e.g. "(2.255)".
Writes quran/hadlinks.json: {"v":1, "a": {global ayah index: [[book, number, kitab, kind], ...]}} where kind is
"q" (quotes the ayah) or "r" (names it)."""
import json, os, re, collections
H = os.path.dirname(__file__); R = os.path.join(H, '..')
def N(t):
    t = re.sub('[ؐ-ًؚ-ٰٟۖ-ۭـ]', '', t or '')
    t = re.sub('[أإآٱ]', 'ا', t).replace('ى', 'ي').replace('ة', 'ه').replace('ؤ', 'و').replace('ئ', 'ي')
    return re.sub('[^ء-ي ]', ' ', t).split()
Q = json.load(open(os.path.join(H, 'quran-plain.json')))
AW = [N(x[2]) for x in Q]
gof = {(x[0], x[1]): i for i, x in enumerate(Q)}
K = 6
sh = collections.defaultdict(set)
for g, w in enumerate(AW):
    if len(w) < 4 or g == 0: continue   # the basmalah of al-Fatihah: quoted in letters and everywhere
    k = min(K, len(w))
    for i in range(len(w) - k + 1): sh[(k, ' '.join(w[i:i + k]))].add(g)
books = json.load(open(os.path.join(R, 'kutub', 'books2.json')))['books']
links = collections.defaultdict(list)
for b in books:
    for s in b['sections']:
        for h in json.load(open(os.path.join(R, 'kutub', b['id'], f"{s['n']}.json")))['h']:
            hw = N(h[2]); text = ' '.join(hw); found = set()
            for k in range(4, K + 1):
                for i in range(len(hw) - k + 1):
                    for g in sh.get((k, ' '.join(hw[i:i + k])), ()):
                        if g in found: continue
                        if len(AW[g]) == k or k == K: found.add(g)
            for g in found: links[g].append([b['id'], h[0], s['n'], 'q'])
            if b['id'] in ('bukhari', 'muslim'):
                for su, a in re.findall(r'\((\d{1,3})\.(\d{1,3})\)', h[3] or ''):
                    g = gof.get((int(su), int(a)))
                    if g is not None and g and g not in found: links[g].append([b['id'], h[0], s['n'], 'r']); found.add(g)
order = {b['id']: i for i, b in enumerate(books)}
out = {}
for g, L in links.items():
    L.sort(key=lambda x: (order[x[0]], x[1])); out[str(g)] = L[:40]
# ayat that also have hadith from the books' own tafsir chapters (hadith/NNN.json), for the mark in the reader
tl = []
for su in range(1, 115):
    try: d = json.load(open(os.path.join(R, 'hadith', f'{su:03d}.json')))
    except Exception: continue
    for a, L in (d.get('ayat') or {}).items():
        g = gof.get((su, int(a)))
        if g is not None and L: tl.append(g)
            # al-Bukhari's tafsir links use the same numbers as this app: do not list those twice
        for x in (L or []):
            if x.get('c') == 'bukhari' and g is not None and str(g) in out:
                out[str(g)] = [y for y in out[str(g)] if not (y[0] == 'bukhari' and str(y[1]) == str(x.get('ref')))]
out = {k: v for k, v in out.items() if v}
json.dump(dict(v=1, t=sorted(set(tl)), a=out), open(os.path.join(R, 'quran', 'hadlinks.json'), 'w'), separators=(',', ':'))
print(len(out), 'ayat linked;', sum(len(v) for v in out.values()), 'links')

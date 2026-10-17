"""Kamus Al-Quran (Azli, 17 Oct 2026): a dictionary of every word of the Qur'an by root and lemma.
Roots, lemmas and parts of speech: the Quranic Arabic Corpus morphology v0.4 (Kais Dukes, University of Leeds, GNU GPL),
as corrected in github.com/mustafa0x/quran-morphology (tools/qac/quran-morphology.txt).
Meanings: the word-by-word English and Indonesian of Quran.com (wbw/), gathered over each lemma's occurrences.
Writes kamus/kamus.json (roots -> lemmas, counts, meanings) and kamus/occ.json (where each lemma occurs)."""
import json, os, re, collections
H = os.path.dirname(__file__); R = os.path.join(H, '..')
M = os.path.join(H, 'qac', 'quran-morphology.txt')
# global ayah index, as the app counts them (A[g] = [surah, ayah, ...])
counts = [len(json.load(open(os.path.join(R, 'wbw', f'{s:03d}.json')))['en']) for s in range(1, 115)]
gstart = [0]
for c in counts: gstart.append(gstart[-1] + c)
WB = {s: json.load(open(os.path.join(R, 'wbw', f'{s:03d}.json'))) for s in range(1, 115)}
word = {}   # (s,a,w) -> dict(root, lem, pos)
for line in open(M, encoding='utf-8'):
    loc, form, tag, feats = line.rstrip('\n').split('\t')
    s, a, w, seg = map(int, loc.split(':'))
    f = feats.split('|')
    if 'PREF' in f or 'SUFF' in f: continue
    root = next((x[5:] for x in f if x.startswith('ROOT:')), '')
    lem = next((x[4:] for x in f if x.startswith('LEM:')), '')
    pos = 'PN' if 'PN' in f else ('ADJ' if 'ADJ' in f else tag)
    k = (s, a, w)
    if k in word and word[k]['root']: continue    # keep the first stem with a root
    word[k] = dict(root=root, lem=lem, pos=pos)
lemmas = collections.OrderedDict()
for (s, a, w), x in sorted(word.items()):
    key = (x['root'], x['lem'])
    L = lemmas.setdefault(key, dict(pos=collections.Counter(), en=collections.Counter(), id=collections.Counter(), occ=[], forms=collections.Counter()))
    L['pos'][x['pos']] += 1
    en = WB[s]['en'][a - 1][w - 1].strip(); idn = WB[s]['id'][a - 1][w - 1].strip(); ar = WB[s]['ar'][a - 1][w - 1]
    if en: L['en'][en.lower()] += 1
    if idn: L['id'][idn.lower()] += 1
    L['forms'][ar] += 1
    L['occ'].append((gstart[s - 1] + a - 1) * 1000 + w)
roots = collections.OrderedDict()
occ = {}
for i, ((root, lem), L) in enumerate(lemmas.items()):
    occ[i] = L['occ']
    roots.setdefault(root, []).append([lem, len(L['occ']), L['pos'].most_common(1)[0][0], [m for m, _ in L['en'].most_common(4)], [m for m, _ in L['id'].most_common(4)], [f for f, _ in L['forms'].most_common(3)], i])
out = [dict(r=r, n=sum(x[1] for x in ls), l=sorted(ls, key=lambda x: -x[1])) for r, ls in roots.items()]
ar_order = 'ءآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهوىي'
def sk(x): return [ar_order.find(c) if c in ar_order else 99 for c in (x['r'] or '~')]
out.sort(key=lambda x: (x['r'] == '', sk(x)))
os.makedirs(os.path.join(R, 'kamus'), exist_ok=True)
json.dump(dict(v=1, src='Quranic Arabic Corpus v0.4 (GPL), mustafa0x/quran-morphology; word meanings: Quran.com word-by-word', roots=out), open(os.path.join(R, 'kamus', 'kamus.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
json.dump([occ[i] for i in range(len(occ))], open(os.path.join(R, 'kamus', 'occ.json'), 'w'), separators=(',', ':'))
print(len(out), 'roots/particles,', len(lemmas), 'lemmas,', len(word), 'words')

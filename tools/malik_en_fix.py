"""Muwatta Malik, English: put each entry's text with the right Arabic entry.

In fawazahmed0's eng-malik many entries begin with Malik's own rulings that, in the Arabic, close the previous entry.
The hadith itself follows in the same English entry. This moves that leading part back to the previous entry, at the
point where the narration of the Arabic entry begins (checked by the narrator names of the Indonesian translation,
which follows the Arabic). Entries still not matched are left without English (the app says so).
Usage: python3 malik_en_fix.py <hadith-api repo> <out.json>
"""
import json, re, subprocess, sys, difflib
SRC, OUT = sys.argv[1], sys.argv[2]
g = lambda e: [(h['hadithnumber'], h['text'].strip()) for h in json.loads(subprocess.run(['git', '-C', SRC, 'show', f'HEAD:editions/{e}.min.json'], capture_output=True, text=True, check=True).stdout)['hadiths']]
A = dict(g('ara-malik')); E = [list(x) for x in g('eng-malik')]; I = dict(g('ind-malik'))
D = re.compile('[ً-ٰٟ]')
ar_ruling = lambda t: bool(re.match(r'\s*(و?قال مالك|و?سئل مالك|قال يحيى|و?سمعت مالك)', D.sub('', t[:60])))
STOP = {'bin', 'binti', 'ibnu', 'bapaknya', 'ibunya', 'pamannya', 'al', 'as', 'ad', 'an', 'ar', 'az', 'abu', 'umm', 'ummu', 'ummul',
        'mukminin', 'menjawab', 'dan', 'seorang', 'laki', 'dari', 'abi', 'yang', 'dia', 'beberapa', 'orang', 'keluarganya', 'lainnya', 'keduanya', 'seseorang'}
def toks(s): return [w for w in re.findall(r'[a-z]+', s.lower().replace("'", '').replace('`', '')) if w not in STOP and len(w) >= 3]
def cv(w):
    w = w.replace('sy', 'sh').replace('dz', 'dh').replace('dl', 'd').replace('ts', 'th').replace('kh', 'h').replace('q', 'k')
    return re.sub(r'(.)\1', r'\1', w)
def names(n): return [cv(w) for w in toks(' '.join(re.findall(r'\[([^\]]+)\]', I.get(n, ''))))]
def overlap(nt, text):
    et = [cv(w) for w in toks(text)]
    return sum(1 for w in nt if any(difflib.SequenceMatcher(None, w, x).ratio() >= 0.75 for x in et)) / len(nt)
RULING = re.compile(r'^\s*(Malik (said|spoke|was asked|added)|Yahya (said|related)( to me)?,? (that )?(he heard )?Malik|Yahya related to me from Malik(,)? (that he (had )?heard|that the best|"|, "))')
START = re.compile(r'(Yahya related to me|It was related to me|Malik related to me|Yahya related)')
moved, unmatched = [], []
for k in range(1, len(E)):
    n, t = E[k]
    if not t or ar_ruling(A.get(n, '')) or not A.get(n, '').strip(): continue
    nt = names(n)
    head_ok = overlap(nt, t[:400]) >= 0.5 if len(nt) >= 2 else not RULING.match(t)
    if head_ok: continue
    cut = None
    for m in START.finditer(t):
        if m.start() == 0: continue
        if (len(nt) >= 2 and overlap(nt, t[m.start():m.start() + 400]) >= 0.5) or (len(nt) < 2 and RULING.match(t)):
            cut = m.start(); break
    if cut:
        E[k - 1][1] = (E[k - 1][1] + ' ' + t[:cut].strip()).strip(); E[k][1] = t[cut:]; moved.append(n)
    elif len(nt) >= 2:
        unmatched.append(n)
out = {str(n): t for n, t in E}
for n in unmatched: out[str(n)] = ''
json.dump({'moved': moved, 'unmatched': unmatched, 'en': out}, open(OUT, 'w'), ensure_ascii=False)
print('moved', len(moved), 'unmatched', unmatched)

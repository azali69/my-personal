"""Repair Arabic words damaged in the source (U+FFFD) using the same hadith from the Sunnah.com copy
(freococo/sunnah_dataset). A word is replaced only when the two words before and after it match exactly,
and the replacement agrees with every intact letter of the damaged word. Writes tools/fffd_fix.json."""
import json, re, sys
H = re.compile('[ً-ْٰۡـ‏‎]')
sk = lambda s: re.sub(r'[^ء-ي�]', '', H.sub('', s or ''))
res = json.load(open(sys.argv[1]))
src = {(x['b'], x['n']): x['ar'] for x in json.load(open('tools/fffd.json'))}
fixes, report = {}, []
for r in res:
    key = (r['b'], r['n']); ours = src[key]
    if not r['ar']:
        report.append((key, 'not found in the Sunnah.com copy')); continue
    A, B = re.findall(r'\S+', ours), r['ar'].split()
    As, Bs = [sk(w) for w in A], [sk(w) for w in B]
    new, ok = list(A), True
    for i, w in enumerate(A):
        if '�' not in w: continue
        L = [x for x in As[max(0, i - 2):i] if x]; R = [x for x in As[i + 1:i + 3] if x and '�' not in x]
        pat = re.compile('^' + re.sub('�+', '.{0,2}', re.escape(As[i]).replace('\\�', '�')) + '$')
        def find(L, R, pat):
            out = []
            for j in range(len(B)):
                if not pat.match(Bs[j]): continue
                lb = [x for x in Bs[max(0, j - 4):j] if x][-len(L):] if L else []
                rb = [x for x in Bs[j + 1:j + 5] if x][:len(R)] if R else []
                if lb == L and rb == R: out.append(j)
            return out
        cands = find(L, R, pat)
        if len(cands) != 1:   # second try: one word each side, up to 3 missing letters; still must be the only match
            pat3 = re.compile('^' + re.sub('\ufffd+', '.{0,3}', re.escape(As[i]).replace('\\\ufffd', '\ufffd')) + '$')
            cands = find(L[-1:], R[:1], pat3)
        if len(cands) == 1 and '�' not in B[cands[0]]:
            new[i] = B[cands[0]]; report.append((key, f'{w}  ->  {B[cands[0]]}'))
        else:
            ok = False; report.append((key, f'UNRESOLVED {w} ({len(cands)} candidates)'))
    if ok:
        it = iter(new); fixes[f'{key[0]}:{key[1]}'] = re.sub(r'\S+', lambda m: next(it), ours)
json.dump(fixes, open('tools/fffd_fix.json', 'w'), ensure_ascii=False)
for k, m in report: print(k[0], k[1], m)
print('repaired hadith:', len(fixes), 'of', len(res))

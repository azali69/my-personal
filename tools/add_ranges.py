"""Adds "r" to every kitab in kutub/books2.json: the hadith numbers it really holds, as [first, last] runs, e.g. [[1,6],[8,9]].
Needed because the sources order a few kitab out of number order (at-Tirmidhi 2298 sits in kitab 32, Ibn Majah 2435 in kitab 10),
so "first..last" of a kitab is not a safe way to find the kitab of a number. The app looks a typed number up in these runs
(ktSecOf). Run after build_kutub.py and build_shamail.py; safe to run again."""
import json, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); K = os.path.join(R, 'kutub')
p = os.path.join(K, 'books2.json'); B = json.load(open(p))
for b in B['books']:
    for s in b['sections']:
        ns = sorted({int(h[0]) for h in json.load(open(os.path.join(K, b['id'], f"{s['n']}.json")))['h']})
        runs = []
        for n in ns:
            if runs and n == runs[-1][1] + 1: runs[-1][1] = n
            else: runs.append([n, n])
        s['r'] = runs
json.dump(B, open(p, 'w'), ensure_ascii=False, separators=(',', ':'))
print('ranges added;', sum(len(s['r']) for b in B['books'] for s in b['sections']), 'runs in', sum(len(b['sections']) for b in B['books']), 'kitab')

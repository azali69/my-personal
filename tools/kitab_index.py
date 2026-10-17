"""Where each hadith is: (book id, hadith number) -> the kitab (section) file it is in, over all eight books in kutub/books2.json.
Used by build_sirah.py, build_solat.py and build_jumuah.py to add the kitab number the app opens. Hadith numbers are unique per book."""
import json, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
K = os.path.join(R, 'kutub')

def where():
    w = {}
    for b in json.load(open(os.path.join(K, 'books2.json')))['books']:
        for s in b['sections']:
            for h in json.load(open(os.path.join(K, b['id'], f"{s['n']}.json")))['h']: w.setdefault((b['id'], h[0]), s['n'])
    return w

def with_kitab(hs, w):
    """[[book, n, note...]] -> [[book, n, kitab, note...]]"""
    return [[h[0], h[1], w[(h[0], h[1])]] + list(h[2:]) for h in hs]

def write(rel, obj):
    p = os.path.join(R, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(obj, open(p, 'w'), ensure_ascii=False, separators=(',', ':'))

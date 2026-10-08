"""Transliteration from Quran.com (Quran Foundation) API, kept unchanged:
 - translit/simple.json   : their ayah transliteration (translation resource 57)
 - translit/words.json    : their word-by-word transliteration, words joined with spaces
Each is a list of 114 lists (one string per ayah)."""
import json, os, sys, time, urllib.request, datetime, hashlib
UA = {'User-Agent': 'MyPersonalQuran/1.0 (+https://github.com/azali69/my-personal)'}
def get(u):
    for i in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30) as r: return json.load(r)
        except Exception as e: print('retry', u, e, file=sys.stderr); time.sleep(3 * (i + 1))
    raise RuntimeError(u)
simple, words = [], []
for s in range(1, 115):
    vs = get(f'https://api.quran.com/api/v4/verses/by_chapter/{s}?words=true&word_fields=text_uthmani&translations=57&per_page=300')['verses']
    simple.append([(v['translations'][0]['text'] if v.get('translations') else '') for v in vs])
    words.append([' '.join((w.get('transliteration') or {}).get('text') or '' for w in v['words'] if w.get('char_type_name') == 'word') for v in vs])
    time.sleep(0.2)
os.makedirs('translit', exist_ok=True)
json.dump(simple, open('translit/simple.json', 'w'), ensure_ascii=False, separators=(',', ':'))
json.dump(words, open('translit/words.json', 'w'), ensure_ascii=False, separators=(',', ':'))
meta = [t for t in get('https://api.quran.com/api/v4/resources/translations')['translations'] if t['id'] == 57]
info = {}
try: info = get('https://api.quran.com/api/v4/resources/translations/57/info')
except Exception: pass
h = lambda f: hashlib.sha256(open(f, 'rb').read()).hexdigest()[:16]
json.dump({'simple': {'resource': meta, 'info': info, 'hash': h('translit/simple.json')},
           'words': {'source': 'Quran.com API v4 word transliteration', 'hash': h('translit/words.json')},
           'counts': [len(x) for x in simple], 'retrieved': datetime.date.today().isoformat()},
          open('translit/index.json', 'w'), ensure_ascii=False, indent=1)
print(sum(map(len, simple)), sum(map(len, words)))

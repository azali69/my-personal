"""Download tafsir texts from QuranEnc.com (unchanged) into tafsir/<key>/NNN.json.
QuranEnc terms: no modification, cite QuranEnc.com and the publisher, give the version, keep it updated."""
import json, os, sys, time, urllib.request
KEYS = ['english_mokhtasar', 'indonesian_mokhtasar', 'indonesian_saadi', 'arabic_mokhtasar', 'arabic_saadi']
API = 'https://quranenc.com/api/v1'
def get(u, tries=5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'MyPersonalQuran/1.0 (+https://github.com/azali69/my-personal)'}), timeout=60) as r:
                return json.load(r)
        except Exception as e:
            print('retry', u, e, file=sys.stderr); time.sleep(3 * (i + 1))
    raise SystemExit('failed ' + u)
meta = {}
for lang in ['english', 'indonesian', 'arabic']:
    for t in get(f'{API}/translations/list/{lang}')['translations']:
        if t['key'] in KEYS: meta[t['key']] = t
index = {}
for k in KEYS:
    m = meta.get(k)
    if not m: print('no metadata for', k, file=sys.stderr); continue
    os.makedirs(f'tafsir/{k}', exist_ok=True); n = 0
    for s in range(1, 115):
        rows = get(f'{API}/translation/sura/{k}/{s}')['result']
        out = {'key': k, 'version': m.get('version'), 'sura': s,
               'ayat': [[int(r['aya']), r['translation'], r.get('footnotes')] for r in rows]}
        n += len(rows)
        json.dump(out, open(f'tafsir/{k}/{s:03d}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
        time.sleep(0.3)
    index[k] = {'title': m.get('title'), 'description': m.get('description'), 'version': m.get('version'),
                'last_update': m.get('last_update'), 'language': m.get('language_iso_code'), 'ayat': n,
                'source': f'https://quranenc.com/en/browse/{k}'}
    print(k, m.get('version'), n)
json.dump(index, open('tafsir/index.json', 'w'), ensure_ascii=False, indent=1)

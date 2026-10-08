"""Word-by-word meanings from Quran.com (Quran Foundation) API, unchanged: English and Indonesian.
wbw/NNN.json = {"en": [[word meanings of ayah 1], ...], "id": [...], "audio": [[...]]}"""
import json, os, sys, time, urllib.request
UA = {'User-Agent': 'MyPersonalQuran/1.0 (+https://github.com/azali69/my-personal)'}
def get(u):
    for i in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30) as r: return json.load(r)
        except Exception as e: print('retry', u, e, file=sys.stderr); time.sleep(3 * (i + 1))
    raise RuntimeError(u)
os.makedirs('wbw', exist_ok=True)
for s in range(1, 115):
    out = {}
    for lang in ['en', 'id']:
        vs = get(f'https://api.quran.com/api/v4/verses/by_chapter/{s}?words=true&language={lang}&word_fields=text_uthmani,audio_url&per_page=300')['verses']
        out[lang] = [[(w.get('translation') or {}).get('text') or '' for w in v['words'] if w.get('char_type_name') == 'word'] for v in vs]
        if lang == 'en':
            out['ar'] = [[w.get('text_uthmani') or '' for w in v['words'] if w.get('char_type_name') == 'word'] for v in vs]
            out['audio'] = [[w.get('audio_url') or '' for w in v['words'] if w.get('char_type_name') == 'word'] for v in vs]
        time.sleep(0.2)
    json.dump(out, open(f'wbw/{s:03d}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('done')

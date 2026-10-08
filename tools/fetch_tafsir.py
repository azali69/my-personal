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
# QuranEnc's translations list does not include its tafsir keys, so there is no version number to record:
# the retrieval date is recorded instead, and each file can be compared with the next monthly fetch.
TITLES = {'english_mokhtasar': ('Al-Mukhtasar in Interpreting the Noble Quran', 'en', 'Tafsir Center for Quranic Studies'),
          'indonesian_mokhtasar': ('Al-Mukhtasar fi Tafsir al-Quran (Indonesian)', 'id', 'Tafsir Center for Quranic Studies'),
          'indonesian_saadi': ('Tafsir As-Sa\'di (Indonesian)', 'id', 'Shaykh Abdurrahman as-Sa\'di'),
          'arabic_mokhtasar': ('المختصر في تفسير القرآن الكريم', 'ar', 'مركز تفسير للدراسات القرآنية'),
          'arabic_saadi': ('تيسير الكريم الرحمن (تفسير السعدي)', 'ar', 'عبد الرحمن بن ناصر السعدي')}
import hashlib, datetime
index = {}
for k in KEYS:
    os.makedirs(f'tafsir/{k}', exist_ok=True); n = 0
    for s in range(1, 115):
        rows = get(f'{API}/translation/sura/{k}/{s}')['result']
        out = {'key': k, 'sura': s,
               'ayat': [[int(r['aya']), r['translation'], r.get('footnotes')] for r in rows]}
        n += len(rows)
        json.dump(out, open(f'tafsir/{k}/{s:03d}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
        time.sleep(0.3)
    h = hashlib.sha256(b''.join(open(f'tafsir/{k}/{s:03d}.json', 'rb').read() for s in range(1, 115))).hexdigest()[:16]
    old = {}
    try: old = json.load(open('tafsir/index.json')).get(k, {})
    except Exception: pass
    t, lang, by = TITLES[k]
    index[k] = {'title': t, 'by': by, 'language': lang, 'ayat': n, 'hash': h,
                'retrieved': old.get('retrieved') if old.get('hash') == h else datetime.date.today().isoformat(),
                'source': f'https://quranenc.com/en/browse/{k}'}
    print(k, n, h)
json.dump(index, open('tafsir/index.json', 'w'), ensure_ascii=False, indent=1)

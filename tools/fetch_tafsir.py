"""Download tafsir texts from QuranEnc.com (unchanged) into tafsir/<key>/NNN.json.
QuranEnc terms: no modification, cite QuranEnc.com and the publisher, give the version, keep it updated."""
import json, os, re, sys, time, html as H, urllib.request, urllib.error
KEYS = ['english_mokhtasar', 'indonesian_mokhtasar', 'indonesian_saadi', 'arabic_mokhtasar', 'arabic_saadi']
API = 'https://quranenc.com/api/v1'
def get(u, tries=5, raw=False):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'MyPersonalQuran/1.0 (+https://github.com/azali69/my-personal)'}), timeout=60) as r:
                return r.read().decode('utf-8') if raw else json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404: raise
            print('retry', u, e, file=sys.stderr); time.sleep(3 * (i + 1))
        except Exception as e:
            print('retry', u, e, file=sys.stderr); time.sleep(3 * (i + 1))
    raise RuntimeError('failed ' + u)
# QuranEnc's translations list does not include its tafsir keys, so there is no version number to record:
# the retrieval date is recorded instead, and each file can be compared with the next monthly fetch.
TITLES = {'english_mokhtasar': ('Al-Mukhtasar in Interpreting the Noble Quran', 'en', 'Tafsir Center for Quranic Studies'),
          'indonesian_mokhtasar': ('Al-Mukhtasar fi Tafsir al-Quran (Indonesian)', 'id', 'Tafsir Center for Quranic Studies'),
          'indonesian_saadi': ('Tafsir As-Sa\'di (Indonesian)', 'id', 'Shaykh Abdurrahman as-Sa\'di'),
          'arabic_mokhtasar': ('المختصر في تفسير القرآن الكريم', 'ar', 'مركز تفسير للدراسات القرآنية'),
          'arabic_saadi': ('تيسير الكريم الرحمن (تفسير السعدي)', 'ar', 'عبد الرحمن بن ناصر السعدي')}
import hashlib, datetime
def clean(t):
    t = re.sub(r'<br\s*/?>', '\n', t); t = re.sub(r'</p>', '\n', t)
    t = H.unescape(re.sub('<[^>]+>', '', t))
    t = '\n'.join(re.sub(r'[ \t]+', ' ', l).strip() for l in t.split('\n')).strip()
    return re.sub(r'\n{3,}', '\n\n', t)
def page_blocks(src):
    """As-Sa'di on QuranEnc is not in its API; its browse page has the same text in blocks:
    passages (the ayat being explained), explanations labelled 'Verse N' or 'Verse N - M', and unlabelled lead-in notes.
    Only the HTML markup is removed; the words are kept as they are."""
    intro, blocks, lead = [], [], []
    for m in re.finditer(r'<article\b([^>]*)>(.*?)</article>', src, re.S):
        attrs, body = m.group(1), m.group(2)
        lab = re.search(r'saadi-(?:block|aya)-label">(.*?)</span>', body, re.S)
        lab = re.sub(r'\s+', ' ', H.unescape(re.sub('<[^>]+>', '', lab.group(1)))).strip() if lab else ''
        t = re.search(r'<div class="saadi-text">(.*)', body, re.S); t = clean(t.group(1)) if t else ''
        if 'saadi-passage' in attrs: continue          # the ayat themselves (a translation), not the explanation
        nums = [int(x) for x in re.findall(r'\d+', lab)]
        if not nums:
            (intro if not blocks else lead).append(t); continue
        blocks.append([nums[0], nums[-1], '\n\n'.join(lead), t]); lead = []
    if lead and blocks: blocks[-1][3] += '\n\n' + '\n\n'.join(lead)
    return intro, blocks
LOG = []; os.makedirs('tafsir', exist_ok=True)
def fetch_key(k):
    os.makedirs(f'tafsir/{k}', exist_ok=True); n = 0
    for s in range(1, 115):
        rows = []
        try: rows = get(f'{API}/translation/sura/{k}/{s}', tries=2)['result']
        except Exception: pass
        if rows:
            out = {'key': k, 'sura': s, 'ayat': [[int(r['aya']), r['translation'], r.get('footnotes')] for r in rows]}
            n += len(rows)
        else:
            intro, blocks = page_blocks(get(f'https://quranenc.com/en/browse/{k}/{s}', raw=True))
            if not blocks: raise RuntimeError(f'no text for surah {s}')
            out = {'key': k, 'sura': s, 'intro': intro, 'blocks': blocks}
            n += sum(b[1] - b[0] + 1 for b in blocks)
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
    print(k, n, h); LOG.append(f'{k}: ok, {n} ayat, {h}')
try: index = json.load(open('tafsir/index.json'))
except Exception: index = {}
for k in KEYS:
    try: fetch_key(k)
    except Exception as e: LOG.append(f'{k}: FAILED {e!r}'); print(k, 'FAILED', e, file=sys.stderr)
json.dump(index, open('tafsir/index.json', 'w'), ensure_ascii=False, indent=1)
open('tafsir/fetch-log.txt', 'w').write('\n'.join(LOG) + '\n')

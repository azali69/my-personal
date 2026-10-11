"""Download HadeethEnc.com (hadith with explanation): Arabic plus the Malay, Indonesian and English translations.
HadeethEnc terms: credit HadeethEnc.com and do not change the content. Used as-is in the app.
Usage: python3 fetch_hadeethenc.py <out-dir>"""
import json, os, sys, time, urllib.request, concurrent.futures as cf
H = 'https://hadeethenc.com/api/v1'
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
def get(path, tries=4):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(H + path, headers={'User-Agent': 'MyPersonalQuran/1.0 (personal app; credits HadeethEnc.com)'}), timeout=60) as r:
                return json.loads(r.read().decode('utf8') or 'null')
        except Exception as e:
            time.sleep(2 + 3 * k)
    return None
langs = ['ar', 'ms', 'id', 'en']
ids = {}
for L in langs:
    cats = get(f'/categories/list/?language={L}') or []
    json.dump(cats, open(f'{OUT}/cats-{L}.json', 'w'), ensure_ascii=False)
    for c in cats:
        page = 1
        while True:
            d = get(f'/hadeeths/list/?language={L}&category_id={c["id"]}&page={page}&per_page=500')
            if not d or not d.get('data'): break
            for h in d['data']: ids.setdefault(h['id'], set()).add(L)
            meta = d.get('meta') or {}
            if int(meta.get('current_page', page)) >= int(meta.get('last_page', page)): break
            page += 1
print('ids', len(ids), {L: sum(L in v for v in ids.values()) for L in langs})
def one(i):
    res = {}
    for L in langs:
        if L in ids[i] or L == 'ar':
            d = get(f'/hadeeths/one/?language={L}&id={i}')
            if d: res[L] = d
        time.sleep(0.1)
    return i, res
allh = {}
with cf.ThreadPoolExecutor(6) as ex:
    for i, res in ex.map(one, sorted(ids, key=int)):
        allh[i] = res
json.dump(allh, open(f'{OUT}/hadeethenc.json', 'w'), ensure_ascii=False)
print('saved', len(allh))

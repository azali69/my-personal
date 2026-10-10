# Temporary: find each damaged hadith (U+FFFD in the Arabic) in the freococo/sunnah_dataset copy of Sunnah.com.
import json, re, glob
import pandas as pd
from huggingface_hub import snapshot_download
H = re.compile('[ً-ْٰۡـ‏‎ ]')
sk = lambda s: re.sub(r'[^ء-ي]', '', H.sub('', s or ''))
p = snapshot_download('freococo/sunnah_dataset', repo_type='dataset', local_dir='/tmp/ds')
df = pd.concat([pd.read_parquet(f) for f in glob.glob('/tmp/ds/**/*.parquet', recursive=True)])
print(df['collection'].value_counts().to_string())
items = json.load(open('tools/fffd.json'))
WANT = {'bukhari': 'bukhari', 'muslim': 'muslim', 'abudawud': 'dawud', 'tirmidhi': 'tirmidhi', 'nasai': 'nasa', 'ibnmajah': 'majah'}
res = []
for it in items:
    sub = df[df['collection'].str.lower().str.contains(WANT[it['b']])]
    parts = [sk(x) for x in it['ar'].split('�') if len(sk(x)) >= 12]
    best = None
    for _, r in sub.iterrows():
        s = sk(r['arabic_full'])
        hits = sum(1 for q in parts if q[-25:] in s or q[:25] in s)
        if hits and (best is None or hits > best[0]): best = (hits, r['ref_raw'], r['arabic_full'])
    res.append({'b': it['b'], 'n': it['n'], 'parts': len(parts), 'hits': best[0] if best else 0, 'ref': best[1] if best else None, 'ar': best[2] if best else None})
json.dump(res, open('out/fffd_res.json', 'w'), ensure_ascii=False)
print('found', sum(1 for r in res if r['ar']), 'of', len(res))

"""Build the Kutub as-Sittah data for the app from fawazahmed0/hadith-api (public domain).

Usage: python3 build_kutub.py <path to a clone of fawazahmed0/hadith-api> <output dir>

Per book: Arabic with harakat (ara-*), English (eng-*), Indonesian (ind-*), split by kitab.
Gradings kept (decided 10 Oct 2026 after checking the data):
  al-Albani, Shu'ayb al-Arna'ut, Zubair 'Ali Za'i, and at-Tirmidhi's own verdict taken from his text.
Left out: the columns named Abu Ghuddah, Fuad Abd al-Baqi, Muhyi al-Din Abdul Hamid and Ahmad Shakir
(95-97% identical to al-Albani: his rulings as printed in those editions), and "Bashar Awad Maarouf"
(91% identical to at-Tirmidhi's own wording).
"""
import json, os, re, subprocess, sys

SRC, OUT = sys.argv[1], sys.argv[2]
BOOKS = [
    ('bukhari', 'صحيح البخاري', 'Sahih al-Bukhari'),
    ('muslim', 'صحيح مسلم', 'Sahih Muslim'),
    ('abudawud', 'سنن أبي داود', 'Sunan Abi Dawud'),
    ('tirmidhi', 'جامع الترمذي', "Jami' at-Tirmidhi"),
    ('nasai', 'سنن النسائي', "Sunan an-Nasa'i"),
    ('ibnmajah', 'سنن ابن ماجه', 'Sunan Ibn Majah'),
]
KEEP = {'Al-Albani': 'alb', 'Shuaib Al Arnaut': 'arn', 'Zubair Ali Zai': 'zub'}
# Unreferenced hadith on a kitab boundary that open the next kitab (checked by content):
# Bukhari 521 Mawaqit as-Salat, 2711 ash-Shurut, 3156 al-Jizyah, 4978 Fada'il al-Qur'an; Muslim 5885-5886 ash-Shi'r.
OPENS_NEXT = {('bukhari', 521), ('bukhari', 2711), ('bukhari', 3156), ('bukhari', 4978), ('muslim', 5885), ('muslim', 5886)}
HARAKAT = re.compile('[ً-ْٰۡـ]')
TIR = re.compile(r'هذا حديث ((?:(?:حسن|صحيح|غريب|ضعيف|مرسل|منكر|مضطرب|مفسر|موقوف)\s*)+)')


def edition(name):
    raw = subprocess.run(['git', '-C', SRC, 'show', f'HEAD:editions/{name}.min.json'], capture_output=True, text=True, check=True).stdout
    return json.loads(raw)


def tirmidhi_verdict(ar):
    t = HARAKAT.sub('', ar)
    i = t.find('قال أبو عيسى')
    m = TIR.search(t, i if i >= 0 else 0)
    return m.group(1).strip() if m else None


info = json.load(open(os.path.join(SRC, 'info.json')))
index = []
for bid, ar_name, en_name in BOOKS:
    A, E, I = edition('ara-' + bid), edition('eng-' + bid), edition('ind-' + bid)
    grades = {h['hadithnumber']: h['grades'] for h in info[bid]['hadiths']}
    ah, eh, ih = A['hadiths'], E['hadiths'], I['hadiths']
    assert len(ah) == len(eh) == len(ih), bid
    # kitab of each hadith: its own reference; 306 in Bukhari, 148 in Muslim and 266 in Ibn Majah have none (book 0)
    # hadith without a kitab reference: the kitab of the referenced hadith on both sides (they agree for all but 17)
    refbook = [((a.get('reference') or {}).get('book') or 0) for a in ah]
    prev_k, next_k, last = [0] * len(ah), [0] * len(ah), 0
    for k, rb in enumerate(refbook):
        if rb: last = rb
        prev_k[k] = last
    last = 0
    for k in range(len(ah) - 1, -1, -1):
        if refbook[k]: last = refbook[k]
        next_k[k] = last
    def kitab(k, n):
        if refbook[k]:
            return str(refbook[k])
        if prev_k[k] == next_k[k]:
            return str(prev_k[k])
        if (bid, n) in OPENS_NEXT:   # on a kitab boundary: the first hadith of the next kitab
            return str(next_k[k])
        return str(prev_k[k])        # otherwise it continues the previous one (e.g. "another chain" narrations)
    secs = {}
    for k, (a, e, i) in enumerate(zip(ah, eh, ih)):
        n = a['hadithnumber']
        assert e['hadithnumber'] == n and i['hadithnumber'] == n, (bid, n)
        if not (a['text'].strip() or e['text'].strip()):
            continue
        g = [[KEEP[x['name']], x['grade']] for x in grades.get(n, []) if x['name'] in KEEP]
        if bid == 'tirmidhi':
            v = tirmidhi_verdict(a['text'])
            if v:
                g.insert(0, ['tir', v])
        ref = a.get('reference') or e.get('reference') or {}
        sec = kitab(k, n)
        secs.setdefault(sec, []).append([n, ref.get('hadith') if ref.get('book') else None, a['text'].strip(), e['text'].strip(), i['text'].strip(), g])
    names = E['metadata']['sections']
    os.makedirs(os.path.join(OUT, bid), exist_ok=True)
    sl = []
    for sec in sorted(secs, key=int):
        hs = secs[sec]
        with open(os.path.join(OUT, bid, f'{sec}.json'), 'w', encoding='utf8') as f:
            json.dump({'h': hs}, f, ensure_ascii=False, separators=(',', ':'))
        nm = (names.get(sec) or ('Introduction' if sec == '0' else f'Book {sec}')).strip()
        if nm.count('(') > nm.count(')'): nm += ')'
        sl.append({'n': int(sec), 'en': nm,
                   'first': hs[0][0], 'last': hs[-1][0], 'count': len(hs)})
    total = sum(s['count'] for s in sl)
    index.append({'id': bid, 'ar': ar_name, 'en': en_name, 'count': total, 'sections': sl})
    print(bid, total, 'hadith in', len(sl), 'kitab')
with open(os.path.join(OUT, 'books.json'), 'w', encoding='utf8') as f:
    json.dump({'source': 'fawazahmed0/hadith-api (public domain)', 'books': index}, f, ensure_ascii=False, separators=(',', ':'))

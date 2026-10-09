"""Hisn al-Muslim (hisnmuslim.com API: Arabic, English, transliteration, repeat counts, Arabic audio) and the
MUIS prayer timetable (data.gov.sg, Open Data Licence), kept unchanged apart from the time format (12-hour -> 24-hour)."""
import json, os, sys, time, urllib.request, datetime
UA = {'User-Agent': 'Mozilla/5.0 MyPersonalQuran/1.0 (+https://github.com/azali69/my-personal)'}
def get(u, raw=False):
    for i in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60) as r:
                b = r.read().decode('utf-8-sig'); return b if raw else json.loads(b)
        except Exception as e: print('retry', u, e, file=sys.stderr); time.sleep(3 * (i + 1))
    raise RuntimeError(u)
log = []
# ---------- Hisn al-Muslim ----------
try:
    idx_en = get('http://www.hisnmuslim.com/api/en/husn_en.json')['English']
    idx_ar = {c['ID']: c for c in get('http://www.hisnmuslim.com/api/ar/husn_ar.json')['العربية']}
    chapters = []
    for c in sorted(idx_en, key=lambda c: c['ID']):
        en = get(f"http://www.hisnmuslim.com/api/en/{c['ID']}.json"); en = en[list(en)[0]]
        ar = get(f"http://www.hisnmuslim.com/api/ar/{c['ID']}.json"); ar_title = list(ar)[0]; ar = {x['ID']: x for x in ar[ar_title]}
        items = []
        for x in en:
            a = ar.get(x['ID'], {})
            items.append({'id': int(x['ID']), 'ar': (a.get('ARABIC_TEXT') or x.get('ARABIC_TEXT') or '').strip(), 'tl': (x.get('LANGUAGE_ARABIC_TRANSLATED_TEXT') or '').strip(),
                          'en': (x.get('TRANSLATED_TEXT') or '').strip(), 'rep': int(x.get('REPEAT') or 1), 'audio': (x.get('AUDIO') or '').replace('http://', 'https://')})
        chapters.append({'id': c['ID'], 'en': c['TITLE'].strip(), 'ar': ar_title.strip(), 'audio': (c.get('AUDIO_URL') or '').replace('http://', 'https://'), 'items': items})
        time.sleep(0.2)
    os.makedirs('dua', exist_ok=True)
    json.dump({'source': 'https://www.hisnmuslim.com', 'retrieved': datetime.date.today().isoformat(), 'chapters': chapters},
              open('dua/hisn.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    log.append(f'hisn: {len(chapters)} chapters, {sum(len(c["items"]) for c in chapters)} items')
except Exception as e: log.append(f'hisn FAILED {e!r}')
# ---------- MUIS prayer timetable ----------
try:
    coll = get('https://api-production.data.gov.sg/v2/public/api/collections/2312/metadata')['data']['collectionMetadata']['childDatasets']
    days = {}
    for ds in coll:
        off = 0
        while True:
            r = get(f'https://data.gov.sg/api/action/datastore_search?resource_id={ds}&limit=1000&offset={off}')['result']
            for x in r['records']:
                if 'Subuh' not in x: break
                def t24(v, pm):
                    h, m = map(int, v.strip()[:5].split(':'))
                    if pm and h < 12 and not (h == 12): h += 12
                    if pm and h == 12: pass
                    return f'{h:02d}:{m:02d}'
                z = x['Zohor']; zh = int(z[:2]); zpm = zh < 11   # Zohor is around 12:xx-13:xx; "01:10" means 13:10
                days[x['Date'][:10]] = [t24(x['Subuh'], False), t24(x['Syuruk'], False), t24(z, zpm), t24(x['Asar'], True), t24(x['Maghrib'], True), t24(x['Isyak'], True)]
            off += len(r['records'])
            if not r['records'] or off >= r.get('total', 0): break
    os.makedirs('prayer', exist_ok=True)
    json.dump({'source': 'MUIS, Muslim Prayer Timetable, data.gov.sg (Open Data Licence)', 'datasets': coll, 'retrieved': datetime.date.today().isoformat(),
               'cols': ['Subuh', 'Syuruk', 'Zohor', 'Asar', 'Maghrib', 'Isyak'], 'days': dict(sorted(days.items()))},
              open('prayer/muis.json', 'w'), separators=(',', ':'))
    log.append(f'muis: {len(days)} days, {min(days)} to {max(days)}')
except Exception as e: log.append(f'muis FAILED {e!r}')
os.makedirs('dua', exist_ok=True); open('dua/fetch-log.txt', 'w').write('\n'.join(log) + '\n'); print('\n'.join(log))

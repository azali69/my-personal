"""Builds mosque/places.json for the "Masjid & musollah" page.
Sources (saved in mosque/src/, fetched 15 Oct 2026):
 - MUIS Mosque Directory, https://www.muis.gov.sg/mosque/Our-Mosques/Mosque-Directory (page dated 21 Sep 2026): name, address, phone.
 - OneMap search API (Singapore Land Authority): latitude/longitude of each postal code.
 - OpenStreetMap (Overpass, amenity=place_of_worship + religion=muslim), (c) OpenStreetMap contributors, ODbL: cross-check and suraus.
 - Wikipedia "List of mosques in Singapore" + article coordinates: mosques not under MUIS, and suraus with an article."""
import json, re, math, os
D = os.path.join(os.path.dirname(__file__), '..', 'mosque')
S = lambda f: json.load(open(os.path.join(D, 'src', f)))
rows = S('muis_directory_rows.json')[1:]
om = S('onemap_postal.json'); osm = S('osm_muslim_pow.json')['elements']; wc = S('wikipedia_coords.json')['query']['pages']

def km(a, b, c, d):
    r = math.radians; h = math.sin(r(c-a)/2)**2 + math.cos(r(a))*math.cos(r(c))*math.sin(r(d-b)/2)**2
    return 2*6371*math.asin(math.sqrt(h))
def title(s): return ' '.join(w if re.match(r'^[A-Z0-9]{1,3}$', w) and w not in ('RD','ST','AVE','DR') else w.capitalize() for w in s.split())

out, report = [], []
osm_m = [(e.get('tags', {}).get('name', ''), e.get('lat') or e['center']['lat'], e.get('lon') or e['center']['lon']) for e in osm]
for name, addr, contact in rows:
    pc = re.search(r'(\d{6})', addr).group(1)
    res = [r for r in om.get(pc, []) if r['POSTAL'] == pc]
    lat = lng = None
    if res: lat, lng = round(float(res[0]['LATITUDE']), 6), round(float(res[0]['LONGITUDE']), 6)
    else:   # no postal-code result (Pulau Bukom): the Wikipedia article's coordinates
        w = [p['coordinates'][0] for p in wc.values() if p['title'].lower() == ('masjid ' + name).lower() and 'coordinates' in p]
        if w: lat, lng = round(w[0]['lat'], 6), round(w[0]['lon'], 6)
    tel = (re.search(r'\b(6\d{7})\b', contact) or [None, None])[1]
    n = 'Masjid ' + name if not name.lower().startswith('masjid') else name
    a = re.sub(r'\s*\|\s*', ', ', addr)
    near = min(((km(lat, lng, la, lo), nm) for nm, la, lo in osm_m), default=(99, '')) if lat else (99, '')
    report.append(f"{n:45s} {pc} {'%.6f,%.6f' % (lat, lng) if lat else 'NO LOCATION':24s} OSM nearest {near[0]*1000:6.0f} m {near[1]}")
    note = 'On Pulau Bukom, an industrial island with restricted access' if pc == '921095' else ''
    out.append(dict(id='muis-'+pc, n=n, t='m', a=a, pc=pc, tel=tel, lat=lat, lng=lng, note=note, src='muis'))
# not under MUIS (Wikipedia), and suraus with a Wikipedia article
extra = {'Masjid Temenggong Daeng Ibrahim': ('m', 'Not administered by MUIS (Johor government)'),
         'Masjid Taha': ('m', 'Not administered by MUIS'),
         'Islamic Centre Jamiyah': ('m', 'Not administered by MUIS'),
         'Surau Al-Firdaus': ('s', ''), 'Surau Ghim Moh': ('s', '')}
have = {o['n'].lower() for o in out}
for p in wc.values():
    t = p['title']
    if t not in extra or 'coordinates' not in p or t.lower() in have: continue
    c = p['coordinates'][0]; ty, note = extra[t]
    out.append(dict(id='wiki-'+re.sub(r'\W+', '-', t.lower()), n=t, t=ty, a='', lat=round(c['lat'], 6), lng=round(c['lon'], 6), note=note, src='wiki'))
# suraus / musollahs in OpenStreetMap not already listed
for e in osm:
    t = e.get('tags', {}); nm = t.get('name', '')
    if not re.search(r'surau|mus[h]?[oa]ll?ah|musolla|prayer room', nm, re.I): continue
    if nm.lower() in {o['n'].lower() for o in out}: continue
    la = e.get('lat') or e['center']['lat']; lo = e.get('lon') or e['center']['lon']
    out.append(dict(id=f"osm-{e['type']}-{e['id']}", n=nm, t='s', a=' '.join(x for x in [t.get('addr:housenumber', ''), t.get('addr:street', '')] if x), lat=round(la, 6), lng=round(lo, 6), src='osm'))
for o in out:
    for k in [k for k, v in o.items() if v in (None, '')]: del o[k]
json.dump({'ver': 1, 'updated': '2026-10-15', 'muis': '2026-09-21', 'p': out}, open(os.path.join(D, 'places.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
open(os.path.join(D, 'src', 'check_report.txt'), 'w').write('\n'.join(report) + '\n')
print(len(out), 'places;', sum(o['t'] == 'm' for o in out), 'masjid,', sum(o['t'] == 's' for o in out), 'musollah')

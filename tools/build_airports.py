"""Builds src/airports.json: the airports with scheduled passenger service, for the app's Flight Prayer page (Azli, 26 Nov 2026).
Rows: [IATA, name, city, country, latitude, longitude, IANA time zone]. Works offline inside the app.
Sources (download first):  OurAirports airports.csv (public domain, davidmegginson/ourairports-data)  and
mwgg/Airports airports.json (MIT, for the time zones).
Usage: python3 tools/build_airports.py /path/to/airports.csv /path/to/airports.json"""
import csv, json, sys, os
csvp, jsp = sys.argv[1], sys.argv[2]
mw = {v['iata']: v for v in json.load(open(jsp, encoding='utf8')).values() if v.get('iata')}
rows = []
for r in csv.DictReader(open(csvp, encoding='utf8')):
    if not (r['iata_code'] and r['type'] in ('large_airport', 'medium_airport') and r['scheduled_service'] == 'yes'): continue
    m = mw.get(r['iata_code'])
    if not m or not m.get('tz'): continue
    try: lat, lng = round(float(r['latitude_deg']), 4), round(float(r['longitude_deg']), 4)
    except ValueError: continue
    if abs(lat - m['lat']) > 0.3 or abs(lng - m['lon']) > 0.3: continue      # the two sources must agree on where it is
    rows.append([r['iata_code'], r['name'].replace(' International Airport', ' Intl').replace(' Airport', '').strip(), m.get('city') or r['municipality'], r['iso_country'], lat, lng, m['tz']])
rows.sort(key=lambda x: x[0])
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'airports.json')
json.dump(rows, open(out, 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
print(len(rows), 'airports', os.path.getsize(out) // 1024, 'KB')

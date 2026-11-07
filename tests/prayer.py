"""Prayer times: Batam by city and by My location, Singapore still MUIS (Azli, 7 Nov 2026). Usage: python3 tests/prayer.py"""
import os, re, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smoke import R, FAKE, route
fails = []
def chk(name, ok, extra=''):
    print(f'{name:55} {"ok" if ok else "FAIL"} {extra}'); (not ok) and fails.append(name)
with sync_playwright() as p:
    exe = os.environ.get('CHROME') or ('/opt/google/chrome/chrome' if os.path.exists('/opt/google/chrome/chrome') else None)
    b = p.chromium.launch(executable_path=exe, args=['--no-sandbox'])
    ctx = b.new_context(viewport={'width': 393, 'height': 873}, timezone_id='Asia/Jakarta')
    ctx.route(re.compile(r'.*(github\.io|jsdelivr).*'), route)
    pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); pg.add_init_script(FAKE)
    pg.goto('file://' + os.path.join(R, 'index.html')); pg.wait_for_timeout(3500)
    T = lambda loc: pg.evaluate("l=>{store.set('prLoc',l);return prayerTimesFor(new Date(2026,10,7))}", loc)
    # official Bimas Islam (SIHAT, Kemenag RI) tables, every time within 1 minute
    tm = lambda x: int(x[:2]) * 60 + int(x[3:])
    OFF = {('Batam', 7, 11): '04:28 05:42 11:51 15:12 17:53 19:04', ('Batam', 22, 11): '04:29 05:45 11:53 15:16 17:55 19:08',
           ('Batam', 15, 12): '04:36 05:54 12:02 15:26 18:04 19:18', ('Jakarta', 7, 11): '04:07 05:22 11:40 14:58 17:50 19:02',
           ('Jakarta', 30, 11): '04:06 05:24 11:45 15:09 17:58 19:13'}
    for (c, d, mo), e in OFF.items():
        r = pg.evaluate("a=>{const c=PR_CITIES.find(x=>x[0]===a[0]);store.set('prLoc',{mode:'city',name:c[0],lat:c[1],lng:c[2]});return prayerTimesFor(new Date(2026,a[2]-1,a[1])).times}", [c, d, mo])
        diff = [abs(tm(x) - tm(y)) for x, y in zip(r, e.split())]
        chk(f'{c} {d}/{mo} within 1 min of Bimas Islam', max(diff) <= 1, f'{r} vs {e}')
    for n, la, ln in [('Harbour Bay', 1.16, 104.02), ('Nongsa', 1.19, 104.09), ('Batam centre', 1.05, 104.03)]:
        r = T({'mode': 'gps', 'lat': la, 'lng': ln})
        chk(f'My location {n}: calculated, not MUIS', r['label'] != 'MUIS' and r['method'] and r['method']['n'] == 'Kemenag' and r['tz'] == 'Asia/Jakarta', f"{r['label'][:30]} {r['times'][0]}")
    for n, la, ln in [('Orchard', 1.3048, 103.8318), ('Changi', 1.36, 103.99), ('Tuas', 1.30, 103.63), ('Pulau Ubin', 1.41, 103.96)]:
        r = T({'mode': 'gps', 'lat': la, 'lng': ln}); chk(f'My location {n}: MUIS', r['label'] == 'MUIS')
    r = T({'mode': 'gps', 'lat': 1.4927, 'lng': 103.7414}); chk('Johor Bahru: JAKIM, not MUIS', r['label'] != 'MUIS' and r['method']['n'] == 'JAKIM')
    r = T({'mode': 'sg'}); chk('Singapore mode: MUIS', r['label'] == 'MUIS')
    chk('no page errors', not errs, str(errs))
    b.close()
print('FAILED:', fails) if fails else print('all ok'); sys.exit(1 if fails else 0)

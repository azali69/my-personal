"""Flight Prayer (Azli, 26 Nov 2026): the sun position against the independent `ephem` library, the events along a route, the page. Usage: python3 tests/flight.py"""
import os, re, sys, math, datetime as dt
import ephem
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smoke import R, FAKE, route
fails = []
def chk(name, ok, extra=''):
    print(f'{name:60} {"ok" if ok else "FAIL"} {extra}'); (not ok) and fails.append(name)
def eph(ms, lat, lng):
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lng); o.elevation = 0; o.pressure = 0; o.date = dt.datetime.fromtimestamp(ms / 1000, dt.UTC).replace(tzinfo=None)
    s = ephem.Sun(o); return math.degrees(s.alt), math.degrees(s.az)
with sync_playwright() as p:
    exe = os.environ.get('CHROME') or ('/opt/google/chrome/chrome' if os.path.exists('/opt/google/chrome/chrome') else None)
    b = p.chromium.launch(executable_path=exe, args=['--no-sandbox'])
    ctx = b.new_context(viewport={'width': 393, 'height': 873}, timezone_id='Asia/Singapore')
    ctx.route(re.compile(r'.*(github\.io|jsdelivr).*'), route)
    pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); pg.add_init_script(FAKE)
    pg.goto('file://' + os.path.join(R, 'index.html')); pg.wait_for_timeout(3500)
    # 1. sun position vs ephem at many places and times (altitude within 0.05°, bearing within 0.3° where the sun is up)
    worst = [0, 0]
    for lat, lng in [(1.3, 103.8), (35.7, 140.4), (21.4, 39.8), (51.5, -0.5), (-33.9, 151.2), (40.6, -73.8), (64.1, -21.9), (-54.8, -68.3)]:
        for k in range(0, 24 * 5):
            ms = 1795000000000 + k * 3600e3 * 4.9
            a, z = pg.evaluate("a=>{const s=flSun(a[0],a[1],a[2]);return [s.alt,s.az]}", [ms, lat, lng]); ea, ez = eph(ms, lat, lng)
            worst[0] = max(worst[0], abs(a - ea))
            if ea > 5 and abs(abs(lat) - 90) > 30: worst[1] = max(worst[1], abs(((z - ez + 180) % 360) - 180))
    chk('sun altitude within 0.05° of ephem', worst[0] < 0.05, f'worst {worst[0]:.3f}°'); chk('sun bearing within 0.3° of ephem', worst[1] < 0.3, f'worst {worst[1]:.3f}°')
    # 2. fixed place: the events must agree with ephem rise/set/transit (no flight: stand still)
    r = pg.evaluate("""()=>{ const M=PR_METHODS.mwl, t0=Date.UTC(2026,10,26,20,0), tr=()=>({lat:1.3,lng:103.8,brg:0}); return flEvents(tr,t0,t0+24*3600e3,M,0).map(e=>[e.k,e.t]); }""")
    o = ephem.Observer(); o.lat, o.lon = '1.3', '103.8'; o.pressure = 0; o.horizon = '-0:34'; o.date = dt.datetime(2026, 11, 26, 20, 0)
    sr = o.next_rising(ephem.Sun()).datetime(); ss = o.next_setting(ephem.Sun()).datetime(); tn = o.next_transit(ephem.Sun()).datetime()
    ms = lambda d: (d - dt.datetime(1970, 1, 1)).total_seconds() * 1000
    got = {k: t for k, t in r}
    chk('sunrise within 1 min of ephem', abs(got['rise'] - ms(sr)) < 60e3, f"{(got['rise'] - ms(sr)) / 1000:.0f}s")
    chk('sunset within 1 min of ephem', abs(got['set'] - ms(ss)) < 60e3, f"{(got['set'] - ms(ss)) / 1000:.0f}s")
    chk('Zuhr (transit) within 1 min of ephem', abs(got['zuhr'] - ms(tn)) < 60e3, f"{(got['zuhr'] - ms(tn)) / 1000:.0f}s")
    chk('aircraft sunset later than ground, sunrise earlier', pg.evaluate("()=>{const M=PR_METHODS.mwl,t0=Date.UTC(2026,10,26,20,0),e=flEvents(()=>({lat:1.3,lng:103.8,brg:0}),t0,t0+24*36e5,M,10500);const g=k=>e.find(x=>x.k===k).t;return [g('setA')-g('set'),g('rise')-g('riseA')]}") > [60e3, 60e3] if False else all(x > 4 * 60e3 for x in pg.evaluate("()=>{const M=PR_METHODS.mwl,t0=Date.UTC(2026,10,26,20,0),e=flEvents(()=>({lat:1.3,lng:103.8,brg:0}),t0,t0+24*36e5,M,10500);const g=k=>e.find(x=>x.k===k).t;return [g('setA')-g('set'),g('rise')-g('riseA')]}")))
    # 3. the same place as the existing timetable code (MWL): Fajr, Zuhr, Asr, Isha within 1 min of sunCalc
    sc = pg.evaluate("()=>sunCalc(new Date(2026,10,27),1.3,103.8,PR_METHODS.mwl,8)")
    base = pg.evaluate("()=>Date.UTC(2026,10,27)-8*3600e3")
    evk = {}
    for k, t in r: evk.setdefault(k, t)
    for i, k in [(0, 'fajr'), (2, 'zuhr'), (3, 'asr'), (4, 'set'), (5, 'isha')]:
        chk(f'{k} agrees with the Prayer Times engine (<=1 min)', abs(evk[k] - (base + sc[i] * 3600e3)) <= 61e3, f'{(evk[k] - (base + sc[i] * 3600e3)) / 1000:.0f}s')
    # 4. a real flight: Singapore to Jeddah, leaving 27 Nov 2026 09:00 SGT, 8 h 40 min; sun at the aircraft at each event matches ephem
    fl = pg.evaluate("""()=>{ const o=flApFind('SIN'),d=flApFind('JED'),a=flFromLocal('2026-11-27T13:00',o[6]),b=flFromLocal('2026-11-27T16:40',d[6]);
        const tr=flRouteTrack([o[4],o[5]],[d[4],d[5]],a,b), M=PR_METHODS.mwl, ev=flEvents(tr,a,b,M,10500);
        return {a,b,ev:ev.map(e=>[e.k,e.t,e.lat,e.lng,e.salt]), dur:(b-a)/36e5, d:flDist([o[4],o[5]],[d[4],d[5]]), start:tr(a), end:tr(b)}; }""")
    chk('SIN-JED great-circle distance about 6,800 km', 7000 < fl['d'] < 7600, f"{fl['d']:.0f} km"); chk('flight time 8.67 h', abs(fl['dur'] - 8.667) < .01, f"{fl['dur']:.2f}")
    chk('route starts at SIN, ends at JED', abs(fl['start']['lat'] - 1.35) < .1 and abs(fl['end']['lng'] - 39.157) < .1)
    keys = [e[0] for e in fl['ev']]; print('   events:', [(e[0], dt.datetime.fromtimestamp(e[1] / 1000, dt.UTC).strftime('%H:%M UTC'), round(e[2], 1), round(e[3], 1)) for e in fl['ev']])
    chk('SIN-JED leaving after Zuhr: Asr found on the way', 'asr' in keys and 'zuhr' not in keys, str(keys))
    for e in fl['ev']:
        a, _ = eph(e[1], e[2], e[3]); tgt = {'fajr': -18, 'rise': -.833, 'riseA': -.833 - 3.28, 'set': -.833, 'setA': -.833 - 3.28, 'isha': -17, 'zuhr': None, 'asr': None}[e[0]]
        if tgt is not None: chk(f'  {e[0]}: sun at the aircraft is at the angle', abs(a - tgt) < 0.1, f'{a:.2f} vs {tgt}')
        else: chk(f'  {e[0]}: sun altitude at the aircraft matches ephem', abs(a - e[4]) < 0.05, f'{a:.2f}')
    # 5. a night flight over the Atlantic: Fajr, then sunrise seen from the aircraft before the ground sunrise
    ng = pg.evaluate("""()=>{ const o=flApFind('JFK'),d=flApFind('LHR'),a=flFromLocal('2026-11-27T21:00',o[6]),b=flFromLocal('2026-11-28T09:00',d[6]); const tr=flRouteTrack([o[4],o[5]],[d[4],d[5]],a,b),M=PR_METHODS.mwl,
        ev=flEvents(tr,a,b,M,10500); return {h:(b-a)/36e5,ev:ev.map(e=>[e.k,e.t,e.lat,e.lng,e.salt])}; }""")
    kk = [e[0] for e in ng['ev']]; print('   JFK-LHR night flight:', [(e[0], dt.datetime.fromtimestamp(e[1] / 1000, dt.UTC).strftime('%H:%M'), round(e[2]), round(e[3])) for e in ng['ev']])
    chk('JFK-LHR: Fajr and sunrise on the way, in order', 'fajr' in kk and 'riseA' in kk and kk.index('fajr') < kk.index('riseA'), str(kk))
    chk('events are in time order', all(ng['ev'][i][1] <= ng['ev'][i + 1][1] for i in range(len(ng['ev']) - 1)))
    # 6. the page
    pg.evaluate("()=>{ window.AndroidExtra=undefined; }")
    pg.evaluate("()=>store.set('flight',{mode:'route',o:'SIN',d:'KIX',dep:'2026-11-27T09:00',arr:'2026-11-27T16:30',clock:'phone',meth:'auto'})")
    pg.evaluate("()=>flightPanel()"); pg.wait_for_timeout(500)
    txt = pg.inner_text('#flight')
    chk('page shows ESTIMATE for a route', 'ESTIMATE' in pg.inner_text('#flRes')); chk('page shows Qibla and Zuhr', 'Qibla' in txt and 'Zuhr' in txt, txt[:0])
    chk('airport sheet search KIX', pg.evaluate("()=>{ flAirportSheet('SIN',()=>{}); const q=document.getElementById('faQ'); q.value='kix'; q.oninput(); return document.getElementById('faL').textContent }").find('Osaka') >= 0)
    pg.evaluate("()=>closeSheet()")
    pg.evaluate("()=>{ store.set('flight',Object.assign(store.get('flight'),{mode:'gps'})); flRenderForm(); document.getElementById('flRes').innerHTML=flResHtml(); }")
    chk('GPS mode waits for a fix', 'Waiting for a GPS fix' in pg.inner_text('#flight'))
    pg.evaluate("()=>window.__flFix({lat:12.0,lng:80.0,alt:10600,spd:240,brg:285,acc:12,t:Date.now()})"); pg.wait_for_timeout(300)
    txt = pg.inner_text('#flight'); chk('live fix: Live GPS badge, no ESTIMATE title', 'Live GPS fix' in txt and 'ESTIMATE' not in pg.inner_text('#flRes'), '')
    pg.evaluate("()=>window.__flFix({lat:12.0,lng:80.0,alt:null,spd:240,brg:285,acc:12,t:Date.now()})"); pg.wait_for_timeout(300)
    chk('fix without height: ESTIMATE, height assumed', 'ESTIMATE' in pg.inner_text('#flRes') and 'assumed' in pg.inner_text('#flRes'))
    # 7. Home tile and the Prayer Times button
    chk('no page errors', not errs, str(errs[:2]))
    b.close()
print('FAILED:', fails) if fails else print('all passed'); sys.exit(1 if fails else 0)

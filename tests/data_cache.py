"""Data loader test: every data file loads online, loads again offline from the phone's cache, and a changed file on
the server reaches the cache in the background (revalidate). Serves the repo over http://localhost so CacheStorage works.
Usage: python3 tests/data_cache.py"""
import os, re, sys, json, threading, functools, http.server
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
H = functools.partial(Q, directory=R)
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H); port = srv.server_port
threading.Thread(target=srv.serve_forever, daemon=True).start()
state = {'offline': False, 'patch': None}

def route(r):
    if state['offline']: return r.abort()
    u = r.request.url.split('?')[0]
    m = re.search(r'my-personal(?:@main)?/(.*)$', u)
    f = os.path.join(R, m.group(1)) if m else None
    if not (f and os.path.isfile(f)): return r.fulfill(status=404, body='')
    if state['patch'] and u.endswith(state['patch'][0]):
        return r.fulfill(body=json.dumps(state['patch'][1]), content_type='application/json')
    r.fulfill(path=f, content_type='application/json')

LOADS = {  # name: JS returning something checkable
    'translit': "(async()=>{ await tlLoad('simple'); return TL.simple?.length })()",
    'wbw': "wbwLoad(1).then(j=>j.en.length)",
    'hadith': "hdGet('002.json').then(j=>j===null?'null':Object.keys(j).length)",
    'hadith404': "hdGet('999.json').then(j=>String(j))",
    'tafsir': "tafLoad('english_mokhtasar',1).then(j=>(j.ayat||j.blocks).length)",
    'tafIndex': "tafIndex().then(j=>Object.keys(j).length)",
    'hisn': "hisnLoad().then(j=>j.chapters.length)",
    'kutub': "ktGet('books2.json').then(j=>j.length)",
    'kitab': "ktGet('bukhari/1.json').then(j=>Object.keys(j).length)",
    'sirah': "ktGet('../sirah/sirah.json').then(j=>Object.keys(j).length)",
}
fails = []
with sync_playwright() as p:
    exe = os.environ.get('CHROME') or ('/opt/google/chrome/chrome' if os.path.exists('/opt/google/chrome/chrome') else None)
    b = p.chromium.launch(executable_path=exe, args=['--no-sandbox'])
    ctx = b.new_context(viewport={'width': 393, 'height': 873})
    ctx.route(re.compile(r'.*(github\.io|jsdelivr).*'), route)
    pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    url = f'http://127.0.0.1:{port}/index.html'
    def run(tag):
        out = {}
        for k, js in LOADS.items():
            try: out[k] = pg.evaluate(f"(async()=>{{ try{{ return await {js}; }}catch(e){{ return 'ERR '+e.message }} }})()")
            except Exception as e: out[k] = 'EXC ' + str(e)[:80]
        print(tag, out); return out
    pg.goto(url); pg.wait_for_timeout(2500)
    on = run('online ')
    for k, v in on.items():
        if isinstance(v, str) and v.startswith(('ERR', 'EXC')): fails.append(f'online {k}: {v}')
    if on['hadith404'] != 'null': fails.append('missing hadith file should give null')
    state['offline'] = True; pg.reload(); pg.wait_for_timeout(2500)
    off = run('offline')
    for k in LOADS:
        if k in ('hadith404', 'tafIndex'): continue
        if off[k] != on[k]: fails.append(f'offline {k}: {off[k]} != {on[k]}')
    # background refresh: server now has a changed translit file; first open uses the kept copy, the next open the new one
    state['offline'] = False; state['patch'] = ('translit/simple.json', [['NEW']] * 114)
    pg.reload(); pg.wait_for_timeout(2000)
    a = pg.evaluate("(async()=>{ await tlLoad('simple'); return TL.simple[0][0] })()"); pg.wait_for_timeout(1500)
    pg.reload(); pg.wait_for_timeout(2000)
    c = pg.evaluate("(async()=>{ await tlLoad('simple'); return TL.simple[0][0] })()")
    print('revalidate:', repr(a)[:30], '->', repr(c)[:30])
    if a == 'NEW' or c != 'NEW': fails.append(f'revalidate: first {a!r} then {c!r}')
    fails += [f'page error: {e}' for e in errs]
    b.close()
srv.shutdown()
print('\n'.join(fails) or 'OK')
sys.exit(1 if fails else 0)

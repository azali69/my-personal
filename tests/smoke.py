"""Smoke test: opens index.html in a phone-sized Chromium with a stand-in for the Android bridge,
serves the data folders from this repository instead of GitHub Pages, opens every home tile and the
main reader views, and fails on any page error.

Usage: python3 tests/smoke.py [--shots DIR]      (needs: pip install playwright; a Chromium)
Set CHROME=/path/to/chrome if Playwright's own browser is not installed."""
import os, re, sys
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = sys.argv[sys.argv.index('--shots') + 1] if '--shots' in sys.argv else None
FAKE = """
window.AndroidSpeech={getInsets:()=>'',setImmersive(){},setBarColor(){},keepScreenOn(){},isAvailable:()=>true,copyText(){},
 setMicPrefs(){}, micInfo:()=>'phone,boost',
 start(){ setTimeout(()=>window.__androidSpeech.onstart(),50); },
 stop(){ setTimeout(()=>{ window.__androidSpeech.onresult({text:'',final:true}); window.__androidSpeech.onend(); },100); } };
"""

def route(r):
    u = r.request.url.split('?')[0]
    m = re.search(r'my-personal(?:@main)?/(.*)$', u)
    f = os.path.join(R, m.group(1)) if m else None
    if f and os.path.isfile(f):
        r.fulfill(path=f, content_type='application/json')
    else:
        r.abort()

if __name__ == '__main__':
    fails = []
    with sync_playwright() as p:
        exe = os.environ.get('CHROME') or ('/opt/google/chrome/chrome' if os.path.exists('/opt/google/chrome/chrome') else None)
        b = p.chromium.launch(executable_path=exe, args=['--no-sandbox'])
        ctx = b.new_context(viewport={'width': 393, 'height': 873}, is_mobile=True, has_touch=True)
        ctx.route(re.compile(r'.*(github\.io|jsdelivr).*'), route)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.add_init_script(FAKE)
        pg.goto('file://' + os.path.join(R, 'index.html')); pg.wait_for_timeout(3000)
        pg.evaluate("document.getElementById('cover')&&(document.getElementById('cover').hidden=true)")
        tiles = pg.evaluate("[...document.querySelectorAll('[data-t]')].map(x=>x.dataset.t)")
        if len(tiles) < 15: fails.append(f'only {len(tiles)} home tiles')
        for t in tiles:
            r = pg.evaluate(f"(()=>{{ const x=document.querySelector('[data-t={t}]'); if(!x) return 'missing'; x.click(); return 'ok'; }})()")
            pg.wait_for_timeout(1500)
            pid = pg.evaluate("topPanel()?.id||'-'")
            if r != 'ok': fails.append(f'tile {t}: {r}')
            if SHOTS: pg.screenshot(path=os.path.join(SHOTS, f'tile_{t}.png'))
            print(f'{t:8} {r:7} {pid}')
            pg.evaluate("closeSheet(); document.querySelectorAll('.panel').forEach(p=>p.hidden=true); showHome()"); pg.wait_for_timeout(300)
        # reader: page, ayah sheet, hadith sheet, a hadith book, a hadith with links
        pg.evaluate("hideHome(); st.tr=true; renderReader()"); pg.wait_for_timeout(800)
        g = pg.evaluate("A.findIndex(x=>x[0]===2&&x[1]===255)")
        pg.evaluate(f"goAyah({g}); similarSheet({g})"); pg.wait_for_timeout(1500)
        if pg.evaluate("sheetB.querySelectorAll('.sim').length") < 1: fails.append('similar ayat: none')
        pg.evaluate(f"closeSheet(); hadithSheet({g})"); pg.wait_for_timeout(1500)
        pg.evaluate("closeSheet(); ktOpenHadith('bukhari',8)"); pg.wait_for_timeout(3000)
        if pg.evaluate("document.querySelectorAll('#kt-8').length") != 1: fails.append('bukhari 8 not shown')
        if SHOTS: pg.screenshot(path=os.path.join(SHOTS, 'hadith.png'))
        fails += [f'page error: {e}' for e in errs]
        b.close()

    print('\n'.join(fails) or 'OK: no page errors')
    sys.exit(1 if fails else 0)

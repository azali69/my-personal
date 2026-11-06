"""Tap scheme of the Qur'an reader (Azli, 6 Nov 2026): middle tap = bars, side tap = turn page / scroll,
double tap on the book mark or a bookmark = open it. Usage: python3 tests/taps.py"""
import os, re, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smoke import R, FAKE, route

def main():
    fails = []
    def chk(name, ok, extra=''):
        print(f'{name:44} {"ok" if ok else "FAIL"} {extra}'); (not ok) and fails.append(name)
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
        pg.evaluate("hideHome(); st.scroll=false; st.mushaf='text'; st.tr=true; renderReader(); goPage(2)"); pg.wait_for_timeout(1200)
        imm = lambda: pg.evaluate("document.body.classList.contains('immersive')")
        page = lambda: pg.evaluate("st.page")
        tap = lambda x, y: (pg.touchscreen.tap(x, y), pg.wait_for_timeout(700))
        # 1. middle tap toggles the bars
        a = imm(); tap(196, 400); chk('middle tap toggles the bars', imm() != a); tap(196, 400); chk('middle tap toggles back', imm() == a)
        # 2. side taps turn the page (left = next, right = previous)
        p0 = page(); tap(20, 400); pg.wait_for_timeout(900); chk('left edge tap = next page', page() == p0 + 1, f'{p0}->{page()}')
        tap(375, 400); pg.wait_for_timeout(900); chk('right edge tap = previous page', page() == p0, f'->{page()}')
        # 3. switch off: side tap only toggles the bars
        pg.evaluate("store.set('sideTap',false)"); a = imm(); p1 = page(); tap(20, 400)
        chk('side tap off: bars toggle, page stays', imm() != a and page() == p1); tap(20, 400); pg.evaluate("store.set('sideTap',true)")
        # 4. double tap on the 📖 mark opens the hadith sheet
        pg.evaluate("goPage(+A[A.findIndex(x=>x[0]===2&&x[1]===255)][4])"); pg.wait_for_timeout(1200)
        pos = pg.evaluate("""()=>{ const g=A.findIndex(x=>x[0]===2&&x[1]===255); const n=[...document.querySelectorAll('#main .num.hl')].find(n=>n.closest('[data-g]').dataset.g==g); if(!n) return null; n.scrollIntoView({block:'center'}); const r=n.getBoundingClientRect(); return [r.left+r.width/2, r.top-r.height*.5]; }""")
        chk('2:255 shows the 📖 mark', pos is not None)
        if pos:
            pg.wait_for_timeout(300); pos = pg.evaluate("""()=>{ const g=A.findIndex(x=>x[0]===2&&x[1]===255); const n=[...document.querySelectorAll('#main .num.hl')].find(n=>n.closest('[data-g]').dataset.g==g); const r=n.getBoundingClientRect(); return [r.left+r.width/2, r.top-r.height*.5]; }""")
            x = min(max(pos[0], 90), 300); a = imm()
            pg.touchscreen.tap(x, pos[1]); pg.wait_for_timeout(120); pg.touchscreen.tap(x, pos[1]); pg.wait_for_timeout(900)
            chk('double tap on 📖 opens hadith sheet', pg.evaluate("document.getElementById('sheet')?document.getElementById('sheet').classList.contains('open'):!!document.querySelector('.sheet.open')"))
            chk('...and leaves the bars as they were', imm() == a)
            pg.evaluate("closeSheet()"); pg.wait_for_timeout(400)
            a = imm(); pg.touchscreen.tap(x, pos[1]); pg.wait_for_timeout(900)
            chk('single tap on 📖 still acts as a normal tap', imm() != a)
        # 4b. double tap on a bookmarked ayah number opens its menu
        pg.evaluate("st.scroll=false; const g=A.findIndex(x=>x[0]===1&&x[1]===3); st.bm[g]={c:1}; goPage(1)"); pg.wait_for_timeout(1200)
        bp = pg.evaluate("()=>{ const n=document.querySelector('#main .num.bm'); if(!n) return null; const r=n.getBoundingClientRect(); return [Math.min(Math.max(r.left+r.width/2,90),300), r.top+r.height/2]; }")
        chk('bookmarked ayah number is drawn', bp is not None)
        if bp:
            pg.touchscreen.tap(*bp); pg.wait_for_timeout(120); pg.touchscreen.tap(*bp); pg.wait_for_timeout(900)
            chk('double tap on bookmark opens its menu', pg.evaluate("!!document.querySelector('#aBm')"))
            pg.evaluate("st.bm={}; closeSheet()")
        # 5. continuous mode: side tap scrolls
        pg.evaluate("st.scroll=true; goPage(300)"); pg.wait_for_timeout(1500); y0 = pg.evaluate("scrollY"); tap(20, 400); pg.wait_for_timeout(900)
        y1 = pg.evaluate("scrollY"); chk('continuous: left tap scrolls down', y1 > y0 + 300, f'{y0}->{y1}')
        tap(375, 400); pg.wait_for_timeout(900); chk('continuous: right tap scrolls up', pg.evaluate("scrollY") < y1 - 300)
        a = imm(); tap(196, 400); chk('continuous: middle tap toggles bars', imm() != a)
        chk('no page errors', not errs, str(errs[:2]))
        b.close()
    print('FAILED: ' + ', '.join(fails) if fails else 'OK'); sys.exit(1 if fails else 0)
main()

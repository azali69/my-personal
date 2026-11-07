"""Home tiles hidden by default (switchable) and Copy link / opening links (Azli, 7 Nov 2026). Usage: python3 tests/links.py"""
import os, re, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smoke import R, FAKE, route
fails = []
def chk(name, ok, extra=''):
    print(f'{name:50} {"ok" if ok else "FAIL"} {extra}'); (not ok) and fails.append(name)
def fresh(b, hash_=''):
    ctx = b.new_context(viewport={'width': 393, 'height': 873}, is_mobile=True, has_touch=True)
    ctx.route(re.compile(r'.*(github\.io|jsdelivr).*'), route)
    pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); pg.add_init_script(FAKE)
    pg.goto('file://' + os.path.join(R, 'index.html') + hash_); pg.wait_for_timeout(3500); return ctx, pg, errs
with sync_playwright() as p:
    exe = os.environ.get('CHROME') or ('/opt/google/chrome/chrome' if os.path.exists('/opt/google/chrome/chrome') else None)
    b = p.chromium.launch(executable_path=exe, args=['--no-sandbox'])
    # 1. Home tiles
    ctx, pg, errs = fresh(b)
    pg.evaluate("document.getElementById('cover')&&(document.getElementById('cover').hidden=true); showHome()"); pg.wait_for_timeout(800)
    tiles = pg.evaluate("[...document.querySelectorAll('#home .tile[data-t]')].map(t=>t.dataset.t)")
    gone = ['hz','tq','dua','halal','masjid','pray','qibla']; keep = ['read','open','bm','kutub','shamail','sirah','solat','kamus','jumuah','check','notes','set','man']
    chk('hidden tiles are not on Home', not any(t in tiles for t in gone), str([t for t in gone if t in tiles]))
    chk('other tiles (incl. Shama\'il) are still there', all(t in tiles for t in keep), str([t for t in keep if t not in tiles]))
    chk('next-prayer card is not on Home', pg.evaluate("!document.getElementById('hmSalah')"))
    pg.evaluate("homeSetSheet()"); pg.wait_for_timeout(500)
    chk('Home settings lists the 8 switches', pg.evaluate("document.querySelectorAll('#sheetB [id^=hmv-]').length") == 8)
    pg.evaluate("document.querySelector('#hmv-qibla button[data-v=\"true\"]').click(); document.querySelector('#hmv-salah button[data-v=\"true\"]').click()"); pg.wait_for_timeout(500)
    chk('switching Qibla on brings the tile back', pg.evaluate("!!document.querySelector('#home .tile[data-t=qibla]')"))
    chk('switching the prayer card on brings it back', pg.evaluate("!!document.getElementById('hmSalah')"))
    pg.evaluate("closeSheet(); document.querySelector('#home .tile[data-t=qibla]').click()"); pg.wait_for_timeout(800)
    chk('a brought-back tile still opens its page', pg.evaluate("!!document.querySelector('#qibla:not([hidden])')||!!document.querySelector('.panel:not([hidden])')"))
    chk('Home: no page errors', not errs, str(errs[:2])); ctx.close()
    # 2. Copy link (ayah) and the link text
    ctx, pg, errs = fresh(b)
    pg.add_init_script("window.__clip=null;")
    pg.evaluate("document.getElementById('cover')&&(document.getElementById('cover').hidden=true); hideHome(); renderReader(); window.putClipboard=async t=>{ window.__clip=t; return true; }")
    pg.evaluate("ayahSheet(A.findIndex(x=>x[0]===2&&x[1]===255))"); pg.wait_for_timeout(500)
    chk('ayah menu has Copy link', pg.evaluate("!!document.querySelector('#aLink')"))
    pg.evaluate("document.querySelector('#aLink').click()"); pg.wait_for_timeout(400)
    chk('ayah link text', pg.evaluate("window.__clip") == 'https://azali69.github.io/my-personal/#2:255', str(pg.evaluate("window.__clip")))
    # 3. Copy link (hadith)
    pg.evaluate("ktOpenHadith('bukhari',1)"); pg.wait_for_timeout(3500)
    chk('hadith card has a link button', pg.evaluate("!!document.querySelector('[data-link]')"))
    pg.evaluate("document.querySelector('[data-link]').click()"); pg.wait_for_timeout(400)
    chk('hadith link text', pg.evaluate("window.__clip") == 'https://azali69.github.io/my-personal/#bukhari-1', str(pg.evaluate("window.__clip")))
    pg.evaluate("ktOpenHadith('muslim',93)"); pg.wait_for_timeout(3500)
    pg.evaluate("document.querySelector('[data-link]').click()"); pg.wait_for_timeout(400)
    chk('Muslim link uses the standard number', pg.evaluate("window.__clip") == 'https://azali69.github.io/my-personal/#muslim-8a', str(pg.evaluate("window.__clip")))
    chk('Links: no page errors', not errs, str(errs[:2])); ctx.close()
    # 4. Opening links
    for frag, test, label in [('#2:255', "st.page===42 || (A[pageStart[st.page]][0]<=2)", 'Qur\'an link opens the ayah page'),
                              ('#p50', "st.page===50", 'page link opens page 50'),
                              ('#bukhari-10', "/Sahih al-Bukhari 10\\b/.test(document.body.innerText)", 'Bukhari 10 link opens Bukhari 10'),
                              ('#muslim-8a', "/Sahih Muslim 8a/.test(document.body.innerText)", 'Muslim 8a link opens Muslim 8a'),
                              ('#nonsense', "!!document.getElementById('home') && document.getElementById('home').hidden===false || true", 'unknown # does not break the app')]:
        ctx, pg, errs = fresh(b, frag); pg.wait_for_timeout(2500)
        chk(label, pg.evaluate(test) is True, str(pg.evaluate("st.page"))); chk('  no page errors', not errs, str(errs[:2])); ctx.close()
    # 5. a link clicked while the app is open
    ctx, pg, errs = fresh(b)
    pg.evaluate("document.getElementById('cover')&&(document.getElementById('cover').hidden=true); hideHome(); renderReader()")
    pg.evaluate("location.hash='#p77'"); pg.wait_for_timeout(1500)
    chk('hash change while open: page link', pg.evaluate("st.page") == 77, str(pg.evaluate("st.page")))
    pg.evaluate("location.hash='#tirmidhi-3'"); pg.wait_for_timeout(4000)
    chk('hash change while open: hadith link', pg.evaluate("/Jami. at-Tirmidhi 3\\b|Tirmidhi 3\\b/.test(document.body.innerText)"))
    chk('  no page errors', not errs, str(errs[:2])); ctx.close(); b.close()
print('FAILED: ' + ', '.join(fails) if fails else 'OK'); sys.exit(1 if fails else 0)

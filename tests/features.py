"""Feature walk-through: drives the main flows of every part of the app and fails on any page error or a step that
throws. Data folders are served from this repository (as in tests/smoke.py); the printed-page fonts are not reachable.
Usage: python3 tests/features.py [--shots DIR]"""
import os, re, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smoke import R, FAKE, route 

SHOTS = sys.argv[sys.argv.index('--shots') + 1] if '--shots' in sys.argv else None
STEPS = [  # (name, JS run in the page, wait ms)
    ('reader text', "hideHome(); st.mushaf='text'; st.tr=true; renderReader(); goPage(296)", 800),
    ('reader v4', "st.mushaf='v4'; renderReader(); goPage(2)", 800),
    ('reader v4t', "st.mushaf='v4t'; renderReader(); goPage(3)", 800),
    ('back to text', "st.mushaf='text'; renderReader()", 500),
    ('scroll mode', "st.scroll=true; goPage(300); window.scrollBy(0,4000)", 800),
    ('scroll mode follows', "if(st.page<=300) throw new Error('page did not follow the scroll: '+st.page)", 100),
    ('scroll mode printed', "st.mushaf='v4'; goPage(5)", 800),
    ('book mode again', "st.scroll=false; st.mushaf='text'; goPage(296)", 500),
    ('nav sheet', "navSheet()", 500),
    ('search sheet', "closeSheet(); searchSheet()", 500),
    ('ayah sheet', "closeSheet(); ayahSheet(A.findIndex(x=>x[0]===18&&x[1]===10))", 800),
    ('tafsir', "closeSheet(); tafsirSheet(A.findIndex(x=>x[0]===1&&x[1]===1))", 1500),
    ('hadith on ayah', "closeSheet(); hadithSheet(A.findIndex(x=>x[0]===2&&x[1]===255))", 1500),
    ('bookmarks', "closeSheet(); bmSheet()", 500),
    ('hafazan start', "closeSheet(); { const g=A.findIndex(x=>x[0]===112&&x[1]===1); startHz(g,g+3); }", 1000),
    ('hafazan recite', "window.__partial && window.__partial('قل هو الله احد')", 800),
    ('hafazan back', "window.__back && window.__back()", 600),
    ('hadith books', "ktPanel()", 1500),
    ('bukhari book', "ktBook('bukhari')", 1500),
    ('hadith search', "ktSearch('bukhari','النية')", 2500),
    ('open hadith', "ktOpenHadith('muslim',1)", 2500),
    ('same hadith elsewhere', "ktRelSheet('bukhari',1)", 1500),
    ('syamail', "closeSheet(); ktBook('shamail')", 1500),
    ('sirah', "closeSheet(); sirahPanel()", 1500),
    ('sirah event', "sirahEvent(document.querySelector('[data-e]')?.dataset.e||1)", 1500),
    ('sifat solat', "solatPanel('solat')", 1500),
    ('solat step', "solatStep(document.querySelector('[data-s]')?.dataset.s||1,'solat')", 1200),
    ('jumaat', "solatPanel('jumuah')", 1500),
    ('jumaat step', "solatStep(document.querySelector('[data-s]')?.dataset.s||1,'jumuah')", 1200),
    ('doa', "duaPanel()", 2000),
    ('doa chapter', "duaOpen(27)", 1500),
    ('kamus', "kamusPanel('علم')", 2500),
    ('kamus root', "kamusRoot(0)", 1500),
    ('meaning ar', "window.__meaning('رحمة')", 1500),
    ('meaning ms', "closeSheet(); window.__meaning('sabar')", 1500),
    ('check ayah', "closeSheet(); checkPanel({text:'قل هو الله أحد الله الصمد لم يلد ولم يولد ولم يكن له كفوا أحد'}); document.querySelector('#ckGo').click()", 3500),
    ('check hadith', "checkPanel({text:'إنما الأعمال بالنيات وإنما لكل امرئ ما نوى'}); document.querySelector('#ckGo').click()", 4000),
    ('check unknown', "checkPanel({text:'zzzz qqqq xxxx yyyy wwww'}); document.querySelector('#ckGo').click()", 2500),
    ('masjid', "mqPanel()", 2000),
    ('halal', "halalPanel()", 800),
    ('bookmarks over home', "document.querySelectorAll('.panel').forEach(p=>p.hidden=true); showHome(); bmSheet(null,'q'); if(document.getElementById('home').hidden) throw new Error('home hidden')", 500),
    ('bookmarks doa tab', "bmSheet(null,'d')", 1500),
    ('sirah family', "closeSheet(); sirahPanel().then(()=>{ if(!document.querySelector('[data-era=fam]')) throw new Error('no family'); })", 1500),
    ('tajweed key', "tajweedKey()", 500),
    ('about', "closeSheet(); aboutSheet()", 500),
    ('prayer', "prayerPanel()", 1200),
    ('qibla', "qiblaPanel()", 800),
    ('notes', "notesPanel()", 800),
    ('backup', "backupSheet()", 800),
    ('sync', "closeSheet(); syncSheet()", 800),
    ('manual', "closeSheet(); manualPanel()", 1000),
    ('cover', "document.querySelectorAll('.panel').forEach(p=>p.hidden=true); showCover()", 800),
]

if __name__ == '__main__':
    fails = []
    with sync_playwright() as p:
        exe = os.environ.get('CHROME') or ('/opt/google/chrome/chrome' if os.path.exists('/opt/google/chrome/chrome') else None)
        b = p.chromium.launch(executable_path=exe, args=['--no-sandbox'])
        ctx = b.new_context(viewport={'width': 393, 'height': 873}, is_mobile=True, has_touch=True)
        ctx.route(re.compile(r'.*(github\.io|jsdelivr).*'), route)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.add_init_script(FAKE + "window.__partial=t=>window.__androidSpeech&&window.__androidSpeech.onresult({text:t,final:false});")
        pg.goto('file://' + os.path.join(R, 'index.html')); pg.wait_for_timeout(3000)
        pg.evaluate("document.getElementById('cover')&&(document.getElementById('cover').hidden=true)")
        for name, js, ms in STEPS:
            n0 = len(errs)
            r = pg.evaluate("async js=>{ try{ await (0,eval)(js); return 'ok'; }catch(e){ return 'THROW '+e.message; } }", js)
            pg.wait_for_timeout(ms)
            new = errs[n0:]
            print(f'{name:22} {r}' + (f'  page error: {new}' if new else ''))
            if r != 'ok': fails.append(f'{name}: {r}')
            if SHOTS: pg.screenshot(path=os.path.join(SHOTS, 'f_' + re.sub(r'\W+', '_', name) + '.png'))
        fails += [f'page error: {e}' for e in errs]
        b.close()
    print('\n'.join(fails) or 'OK: no errors')
    sys.exit(1 if fails else 0)

"""Scan & Check: the ranked search by a few words, and the exact check for long text (Azli, 9 Nov 2026). Usage: python3 tests/search.py"""
import os, re, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smoke import R, FAKE, route
fails = []
def chk(name, ok, extra=''):
    print(f'{name:62} {"ok" if ok else "FAIL"} {extra}'); (not ok) and fails.append(name)
with sync_playwright() as p:
    exe = os.environ.get('CHROME') or ('/opt/google/chrome/chrome' if os.path.exists('/opt/google/chrome/chrome') else None)
    b = p.chromium.launch(executable_path=exe, args=['--no-sandbox'])
    ctx = b.new_context(viewport={'width': 393, 'height': 873}); ctx.route(re.compile(r'.*(github\.io|jsdelivr).*'), route)
    pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); pg.add_init_script(FAKE)
    pg.goto('file://' + os.path.join(R, 'index.html')); pg.wait_for_timeout(3000)
    pg.evaluate("document.getElementById('cover')&&(document.getElementById('cover').hidden=true)")
    pg.evaluate("checkPanel()"); pg.wait_for_timeout(400)
    def run(q):
        pg.evaluate("q=>{document.getElementById('ckT').value=q;checkRun(q)}", q)
        pg.wait_for_function("()=>{const r=ckSt.res;return !!(r&&r.hDone)}", timeout=170000)
        return pg.evaluate("()=>ckSt.res?{q:ckSt.res.q.map(w=>A[w.g][0]+':'+A[w.g][1]),h:ckSt.res.h.map(r=>r.k+' '+r.h[0]),hAll:ckSt.res.hAll,search:ckSt.res.search,full:ckSt.res.h[0]?!!ckSt.res.h[0].sc.full:null}:null")
    # Azli's example: a popular hadith typed in a few words, with a stray "و" and a space
    r = run("إنما الأعمال بالنيات و إنما"); chk('few Arabic words + stray و: Sahih al-Bukhari 1 is first', r['h'][:1] == ['bukhari 1'] and r['search'], str(r['h'][:3]))
    r = run("إنما الأعمال بالنيات،"); chk('Arabic comma stuck to a word does not matter', 'bukhari 1' in r['h'][:3], str(r['h'][:3]))
    r = run("إنما الأعمال"); chk('two Arabic words: Bukhari 1 among the first 10', 'bukhari 1' in r['h'][:10], str(r['h'][:6]))
    r = run("النيات"); chk('one Arabic word (with the ال and prefix ignored): many hits', r['hAll'] >= 10 and r['h'], str(r['hAll']))
    r = run("niat"); chk('one Malay word: Bukhari 1 among the first 10', 'bukhari 1' in r['h'][:10], str(r['h'][:6]))
    r = run("Sesungguhnya setiap perbuatan tergantung niatnya"); chk('a Malay sentence from the hadith: Bukhari 1 found', 'bukhari 1' in r['h'][:3], str(r['h'][:3]))
    r = run("puasa ramadan"); chk('two Malay words: results, all with both words first', r['hAll'] >= 5 and r['h'], str(r['hAll']))
    r = run("الله لا إله إلا هو الحي القيوم"); chk("Ayat al-Kursi's opening words: 2:255 among the Qur'an results", '2:255' in r['q'][:3], str(r['q'][:3]))
    r = run("sabar"); chk('one Malay word in the Qur\'an: 2:153 found', '2:153' in r['q'], str(r['q'][:4]))
    long = "إنما الأعمال بالنيات، وإنما لكل امرئ ما نوى، فمن كانت هجرته إلى دنيا يصيبها أو إلى امرأة ينكحها، فهجرته إلى ما هاجر إليه"
    r = run(long); chk('long text: the exact check still ranks Bukhari 1 first', r['h'][:1] == ['bukhari 1'] and not r['search'], str(r['h'][:3]))
    r = run("xyzqwv"); chk('a word that is nowhere: no hadith, no crash', r['h'] == [] and r['q'] == [])
    pg.evaluate("document.getElementById('ckT').value='ا';checkRun('ا')"); pg.wait_for_timeout(300)
    chk('one letter: asks for a word', pg.evaluate("document.getElementById('ckMsg').textContent") != '')
    pg.evaluate("document.getElementById('ckT').value='niat';"); pg.press('#ckT', 'Enter'); pg.wait_for_function("()=>ckSt.res&&ckSt.res.hDone&&ckSt.text==='niat'", timeout=60000)
    chk('Enter key runs the search', True)
    chk('hadith cards are shown', pg.evaluate("document.querySelectorAll('#ckH .ck-hd').length") >= 5)
    chk('no page errors', not errs, str(errs))
    b.close()
print('FAILED:', fails) if fails else print('all ok'); sys.exit(1 if fails else 0)

"""Finds MUIS's latest Friday khutbah (Azli, 17 Oct 2026) from
https://www.muis.gov.sg/resources/khutbah-and-religious-advice/khutbah/ and writes khutbah/latest.json:
{"updated": ISO time, "items": [{"title", "date", "url", "pdf"}]}, newest first (up to 6).
Run by .github/workflows/khutbah.yml on Thursday evening and Friday morning (Singapore time)."""
import json, re, sys, os, html, datetime, urllib.request
BASE = 'https://www.muis.gov.sg'
LIST = BASE + '/resources/khutbah-and-religious-advice/khutbah/'
UA = {'User-Agent': 'Mozilla/5.0 (My Personal Qur'an; github.com/azali69/my-personal)'}
def get(u):
    with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40) as r:
        return r.read().decode('utf-8', 'replace')
MONTHS = 'January|February|March|April|May|June|July|August|September|October|November|December'
def main():
    page = get(LIST)
    links = []
    for m in re.finditer(r'href="([^"]*?/resources/khutbah-and-religious-advice/khutbah/[^"#?]+/)"', page):
        u = m.group(1); u = u if u.startswith('http') else BASE + u
        if u.rstrip('/') != LIST.rstrip('/') and u not in links and '/page/' not in u: links.append(u)
    items = []
    for u in links[:10]:
        try: p = get(u)
        except Exception as e: print('skip', u, e); continue
        t = re.search(r'<h1[^>]*>(.*?)</h1>', p, re.S) or re.search(r'<title>(.*?)</title>', p, re.S)
        title = html.unescape(re.sub(r'<[^>]+>', '', t.group(1))).strip() if t else u.rstrip('/').split('/')[-1]
        title = re.sub(r'\s*\|.*$', '', title)
        d = re.search(r'(\d{1,2} (?:%s) 20\d\d)' % MONTHS, p)
        pdfs = re.findall(r'href="([^"]+\.pdf)"', p, re.I)
        pdf = html.unescape(pdfs[0]) if pdfs else ''
        f = pdf.rsplit('/', 1)[-1][:1].upper()   # MUIS names the PDF E…, R… (Rumi Malay) or T… (Tamil)
        lang = {'E': 'en', 'R': 'ms', 'T': 'ta'}.get(f, 'ta' if u.rstrip('/').endswith('tamil') else '')
        items.append(dict(title=title, date=d.group(1) if d else '', url=u, pdf=pdf, lang=lang))
    def key(x):
        try: return datetime.datetime.strptime(x['date'], '%d %B %Y')
        except Exception: return datetime.datetime(1900, 1, 1)
    items.sort(key=key, reverse=True)
    if not items:
        print('::error::nothing found; page length %d; links %d; sample %s' % (len(page), len(links), re.sub(r'\s+',' ',page[:600]).replace('%','%%')))
        sys.exit(1)
    out = os.path.join(os.path.dirname(__file__), '..', 'khutbah', 'latest.json')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    old = None
    try: old = json.load(open(out))
    except Exception: pass
    if old and old.get('items') == items[:9]: print('unchanged'); return
    json.dump(dict(updated=datetime.datetime.utcnow().isoformat(timespec='seconds') + 'Z', items=items[:9]), open(out, 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(items[:9], ensure_ascii=False, indent=1))
    print('::notice::%d khutbah; newest: %s (%s) pdf=%s' % (len(items), items[0]['title'], items[0]['date'], bool(items[0]['pdf'])))
try: main()
except SystemExit: raise
except Exception as e:
    print('::error::%s: %s' % (type(e).__name__, str(e)[:500])); sys.exit(1)

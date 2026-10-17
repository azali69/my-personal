"""Hisn al-Muslim references from Sunnah.com: reads a saved copy of https://sunnah.com/hisn (argv[1]), writes sunnah_hisn.json
({number: {ref, ar}}) and lists entries of dua/hisn.json whose Arabic differs from Sunnah.com's (a check that the numbering matches).
Usage, from the repository root: python3 tools/hisn_refs_parse.py hisn.html"""
import re,html,json,sys,difflib,os
s=open(sys.argv[1]).read()
blocks=re.split(r'<div class="actualHadithContainer',s)[1:]
out={}
strip=lambda t: re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',t))).strip()
for b in blocks:
    n=re.search(r'hadith_reference_sticky">Hisn al-Muslim (\d+)',b)
    if not n: continue
    n=int(n.group(1))
    r=re.search(r'class="hisn_english_reference">(.*?)</span>',b,re.S)
    a=re.search(r'arabic_text_details arabic">(.*?)</span>',b,re.S)
    out[n]={'ref':strip(r.group(1)) if r else '', 'ar':strip(a.group(1)) if a else ''}
json.dump(out,open('sunnah_hisn.json','w'),ensure_ascii=False,indent=0)
print(len(out),min(out),max(out),[k for k in range(1,max(out)+1) if k not in out])
H=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','dua','hisn.json')))
import unicodedata
def norm(t): return re.sub(r'[^ء-ي ]','',re.sub(r'[ً-ْـ]','',t))
bad=0
for c in H['chapters']:
    for it in c['items']:
        o=out.get(it['id'])
        if not o: print('missing',it['id']); continue
        r=difflib.SequenceMatcher(None,norm(it['ar'])[:200],norm(o['ar'])[:200]).ratio()
        if r<.6: bad+=1; print(it['id'],round(r,2),norm(it['ar'])[:60],'||',norm(o['ar'])[:60])
print('bad',bad)

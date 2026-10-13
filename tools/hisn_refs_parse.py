import re,html,json,sys,difflib
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
H=json.load(open('/home/claude/my-personal/dua/hisn.json'))
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

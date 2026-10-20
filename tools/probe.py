import urllib.request, urllib.parse, json, re
UA={'User-Agent':'MyPersonalQuran-probe/1.0 (azali69)'}
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read().decode('utf-8','replace')
out=[]
api='https://ar.wikisource.org/w/api.php?action=query&list=allpages&format=json&aplimit=500&apprefix='+urllib.parse.quote('البداية والنهاية/الجزء الخامس/')
pages=[p['title'] for p in json.loads(get(api))['query']['allpages']]
sel=[t for t in pages if re.search('أزواج|أولاد|زوجات|سراري|أمهات المؤمنين',t)]
out.append('SEL: '+' || '.join(sel))
for t in sel[:6]:
    raw=get('https://ar.wikisource.org/w/index.php?action=raw&title='+urllib.parse.quote(t))
    raw=re.sub(r'\{\{[^{}]*\}\}','',raw); raw=re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]',r'\1',raw)
    out.append(f'#### {t} ({len(raw)})\n'+raw[:9000])
txt='\n'.join(out)
for i in range(0,min(len(txt),60000),3800): print('::notice title=p%d::'%(i//3800)+txt[i:i+3800].replace('%','%25').replace('\n','%0A').replace('\r',''))

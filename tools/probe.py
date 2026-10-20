import urllib.request, urllib.parse, json, re, os
UA={'User-Agent':'MyPersonalQuran-probe/1.0 (azali69)'}
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read().decode('utf-8','replace')
def search(q):
    r=json.loads(get('https://ar.wikisource.org/w/api.php?action=query&list=search&format=json&srlimit=20&srsearch='+urllib.parse.quote(q)))
    return [x['title'] for x in r['query']['search']]
out=[]
for q in ['intitle:أزواجه','intitle:"زاد المعاد" أزواجه','"فصل في أزواجه"','intitle:"تلقيح فهوم"']:
    out.append(q+' => '+' || '.join(search(q)))
print('::notice title=s::'+'%0A'.join(out).replace('%','%25'))
os.makedirs('src_out',exist_ok=True)

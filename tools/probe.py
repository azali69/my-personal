import urllib.request, re, json, sys
UA={'User-Agent':'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/126 Mobile Safari/537.36','Accept':'*/*'}
def get(u):
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30); return r.status, r.read().decode('utf-8','replace'), r.geturl()
    except Exception as e: return 0, str(e), u
out=[]
s,h,u=get('https://halal.muis.gov.sg/halal/establishments'); out.append(f'page {s} {u} len={len(h)}')
scripts=re.findall(r'<script[^>]+src="([^"]+)"',h); out.append('scripts: '+' '.join(scripts[:15]))
out.append('apis in html: '+' '.join(sorted(set(re.findall(r'["\'](/?api/[^"\']{0,80}|https?://[^"\']*api[^"\']{0,80})["\']',h)))[:20]))
for sc in scripts[:12]:
    url=sc if sc.startswith('http') else 'https://halal.muis.gov.sg'+('' if sc.startswith('/') else '/')+sc
    s2,j,_=get(url)
    hits=sorted(set(re.findall(r'["\'`]([^"\'`]{0,60}(?:api|establish|Establish|search)[^"\'`]{0,60})["\'`]',j)))
    if hits: out.append(f'{sc} -> '+' | '.join(hits[:25]))
txt='\n'.join(out)
for i in range(0,min(len(txt),36000),3500): print('::notice title=probe%d::'%(i//3500)+txt[i:i+3500].replace('%','%25').replace('\n','%0A'))

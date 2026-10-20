import urllib.request, json
out=[]
for origin in [None,'https://azali69.github.io']:
    h={'User-Agent':'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/126 Mobile Safari/537.36','Content-Type':'application/json','Accept':'application/json'}
    if origin: h['Origin']=origin
    try:
        r=urllib.request.urlopen(urllib.request.Request('https://halal.muis.gov.sg/api/halal/establishments',data=json.dumps({'text':'tampines'}).encode(),headers=h),timeout=40)
        b=r.read().decode('utf-8','replace'); out.append(f'origin={origin} {r.status} headers={dict(r.headers)}'); out.append(b[:2500])
    except urllib.error.HTTPError as e: out.append(f'origin={origin} HTTP {e.code} {dict(e.headers)} {e.read()[:300]}')
    except Exception as e: out.append(f'origin={origin} ERR {e}')
txt='\n'.join(out)
for i in range(0,min(len(txt),30000),3500): print('::notice title=probe%d::'%(i//3500)+txt[i:i+3500].replace('%','%25').replace('\n','%0A'))

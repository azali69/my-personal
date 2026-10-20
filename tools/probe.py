import urllib.request, json, re, http.cookiejar
cj=http.cookiejar.CookieJar(); op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
UA='Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/126 Mobile Safari/537.36'
out=[]
h=op.open(urllib.request.Request('https://halal.muis.gov.sg/halal/establishments',headers={'User-Agent':UA}),timeout=40).read().decode()
tok=re.search(r'name="__RequestVerificationToken" type="hidden" value="([^"]+)"',h).group(1)
for q in ['tampines','prata']:
    r=op.open(urllib.request.Request('https://halal.muis.gov.sg/api/halal/establishments',data=json.dumps({'text':q}).encode(),headers={'User-Agent':UA,'Content-Type':'application/json','Accept':'application/json','X-CSRF-TOKEN':tok,'Referer':'https://halal.muis.gov.sg/halal/establishments'}),timeout=40)
    b=json.loads(r.read().decode()); d=b.get('data',[]); out.append(f'{q}: keys={list(b)} n={len(d)} total={b.get("totalRecords") or b.get("total")}'); out.append(json.dumps(d[:2],ensure_ascii=False)[:1500])
txt='\n'.join(out)
for i in range(0,min(len(txt),30000),3500): print('::notice title=probe%d::'%(i//3500)+txt[i:i+3500].replace('%','%25').replace('\n','%0A'))

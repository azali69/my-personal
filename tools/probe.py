import urllib.request, json, re, http.cookiejar
cj=http.cookiejar.CookieJar(); op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
UA='Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/126 Mobile Safari/537.36'
out=[]
h=op.open(urllib.request.Request('https://halal.muis.gov.sg/halal/establishments',headers={'User-Agent':UA}),timeout=40).read().decode()
out.append('tokens in html: '+' | '.join(re.findall(r'.{0,80}(?:[Tt]oken|csrf|XSRF|antiforgery).{0,120}',h)[:8]))
c=op.open(urllib.request.Request('https://halal.muis.gov.sg/js/core.min.js',headers={'User-Agent':UA}),timeout=40).read().decode()
i=c.find('postAsync'); out.append('core postAsync: '+c[max(0,i-200):i+900])
for m in re.finditer(r'.{0,100}(?:RequestVerification|X-CSRF|XSRF|antiforgery|__RequestVerificationToken).{0,150}',c): out.append('core tok: '+m.group(0)); 
out.append('cookies: '+str([x.name for x in cj]))
txt='\n'.join(out)
for i in range(0,min(len(txt),30000),3500): print('::notice title=probe%d::'%(i//3500)+txt[i:i+3500].replace('%','%25').replace('\n','%0A'))

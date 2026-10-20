import urllib.request, re, json
UA={'User-Agent':'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/126 Mobile Safari/537.36','Accept':'*/*','Referer':'https://halal.muis.gov.sg/halal/establishments'}
def get(u,data=None,ct=None):
    h=dict(UA); 
    if ct: h['Content-Type']=ct
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,data=data,headers=h),timeout=40); return r.status, r.read().decode('utf-8','replace')
    except urllib.error.HTTPError as e: return e.code, e.read().decode('utf-8','replace')[:300]
    except Exception as e: return 0, str(e)
out=[]
s,j=get('https://halal.muis.gov.sg/js/views/halal/establishments/_panel.js')
i=j.find('/api/halal/establishments'); out.append('PANEL: '+j[max(0,i-1500):i+700])
for u in ['https://halal.muis.gov.sg/api/halal/establishments','https://halal.muis.gov.sg/api/halal/establishments?text=&page=1']:
    s,b=get(u); out.append(f'GET {u} -> {s} {b[:600]}')
txt='\n'.join(out)
for i in range(0,min(len(txt),30000),3500): print('::notice title=probe%d::'%(i//3500)+txt[i:i+3500].replace('%','%25').replace('\n','%0A'))

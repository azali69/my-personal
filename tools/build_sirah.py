"""Builds sirah/sirah.json from tools/sirah_events.py, adding the kitab number of each hadith (from kutub/)."""
import json,sys,os
sys.path.insert(0,os.path.dirname(__file__)); import sirah_events as S
R=os.path.join(os.path.dirname(__file__),'..','kutub')
B=json.load(open(os.path.join(R,'books.json')))['books']
where={}
for b in B:
    for s in b['sections']:
        for h in json.load(open(os.path.join(R,b['id'],f"{s['n']}.json")))['h']: where[(b['id'],h[0])]=s['n']
out=[]
for e in S.E:
    e=dict(e)
    e['h']=[[h[0],h[1],where[(h[0],h[1])]]+list(h[2:]) for h in e.get('h',[])]
    out.append(e)
json.dump({'v':1,'built':'2026-10-15','events':out},open(os.path.join(os.path.dirname(__file__),'..','sirah','sirah.json'),'w'),ensure_ascii=False,separators=(',',':'))
print(len(out),'events')

"""Builds solat/jumuah.json (Solat Jumaat) from tools/jumuah.py, adding the kitab number of each hadith (from kutub/)."""
import json,sys,os
sys.path.insert(0,os.path.dirname(__file__)); import jumuah as S
R=os.path.join(os.path.dirname(__file__),'..','kutub')
B=json.load(open(os.path.join(R,'books.json')))['books']
where={}
for b in B:
    for s in b['sections']:
        for h in json.load(open(os.path.join(R,b['id'],f"{s['n']}.json")))['h']: where.setdefault((b['id'],h[0]),s['n'])
fix=lambda hs:[[h[0],h[1],where[(h[0],h[1])],h[2]] for h in hs]
out=[]
for e in S.E:
    e=dict(e); e['h']=fix(e.get('h',[]))
    e['d']=[dict(x,h=fix(x.get('h',[]))) for x in e.get('d',[])]
    out.append(e)
json.dump({'v':1,'built':'2026-10-17','who':S.WHO,'com':S.COMMENTATORS,'steps':out},open(os.path.join(os.path.dirname(__file__),'..','solat','jumuah.json'),'w'),ensure_ascii=False,separators=(',',':'))
print(len(out),'steps')

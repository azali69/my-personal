"""Same hadith in the other books: links between the hadith of the eight books (kutub/, with the Shama'il) whose matn (the text after the
chain, where the app knows where the chain ends) shares most of its wording. Arabic is compared without harakat, with
alif/ya/ta marbuta forms unified, in 5-word pieces. Pieces found in more than 40 hadith (set phrases such as
"قال رسول الله صلى الله عليه وسلم") are ignored. Two hadith are linked when they share at least 3 of the remaining pieces
and those cover at least half of the shorter matn's pieces. This finds the same report (or most of it) in another
book; it is an aid for finding, not a takhrij: a link does not say the two chains or gradings are the same.
Output kutub/rel2/<book>.json: {"n": [[book index in books2.json, n, percent, kitab], ...]}, other books only, up to 8, closest first."""
import json,re,os,collections
import sys
K,DF,MINS,TH=3,60,4,0.45
BF=sys.argv[1] if len(sys.argv)>1 else 'kutub/books2.json'; OUT=sys.argv[2] if len(sys.argv)>2 else 'kutub/rel2'
B=json.load(open(BF))['books']; ids=[b['id'] for b in B]
def norm(t):
    t=re.sub(r'[ً-ْٰـ]','',t); t=re.sub('[إأآٱ]','ا',t).replace('ى','ي').replace('ة','ه')
    t=re.sub(r'[^ء-ي ]',' ',t); return t.split()
docs={}; secOf={}
for b in B:
    d=f"kutub/{b['id']}"
    for s in b['sections']:
        f=f"{d}/{s['n']}.json"
        if not os.path.exists(f): continue
        for h in json.load(open(f))['h']:
            cut=h[7] if len(h)>7 and isinstance(h[7],dict) else {}
            ar=h[2] or ''; ar=ar[cut['a']:] if cut.get('a') else ar
            w=norm(ar)
            secOf[(b['id'],h[0])]=s['n']
            docs[(b['id'],h[0])]=set(tuple(w[i:i+K]) for i in range(len(w)-K+1))
print(len(docs),'hadith')
df=collections.Counter(g for v in docs.values() for g in v)
rare={k:{g for g in v if df[g]<=DF} for k,v in docs.items()}
inv=collections.defaultdict(list)
for k,v in rare.items():
    for g in v: inv[g].append(k)
out={i:{} for i in ids}
for k,v in rare.items():
    if len(v)<3: continue
    c=collections.Counter()
    for g in v:
        for o in inv[g]:
            if o[0]!=k[0]: c[o]+=1
    res=[]
    for o,n in c.items():
        if n<MINS: continue
        m=min(len(v),len(rare[o]))
        if m and n/m>=TH: res.append((o,round(100*n/m)))
    res.sort(key=lambda x:(-x[1],ids.index(x[0][0]),x[0][1]))
    if res: out[k[0]][str(k[1])]=[[ids.index(o[0]),o[1],p,secOf[o]] for o,p in res[:8]]
os.makedirs(OUT,exist_ok=True)
for i in ids:
    json.dump(out[i],open(f'{OUT}/{i}.json','w'),separators=(',',':'))
    print(i,len(out[i]),'linked', os.path.getsize(f'{OUT}/{i}.json'))
json.dump({'books':ids},open(f'{OUT}/index.json','w'))

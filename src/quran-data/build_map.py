import json,re,unicodedata
K=json.load(open('kfgqpc_hafs_v2.json')); C=json.load(open('kfgqpc_clean.json'))
UNI={'آ':'ا','أ':'ا','إ':'ا','ٱ':'ا','ؤ':'و','ئ':'ي','ى':'ي','ة':'ه','ـ':''}
def norm(w):
    o=''
    for ch in w:
        c=ord(ch)
        if 0x610<=c<=0x61A or 0x64B<=c<=0x65F or c==0x670 or 0x6D6<=c<=0x6ED: continue
        ch=UNI.get(ch,ch)
        if ch and 0x600<=ord(ch[0])<=0x6FF: o+=ch
    return o
def sk(w): return re.sub('[اويء]','',norm(w))
MARK={'۞','۩'}
def mapayah(u,e):
    words=[i for i,t in enumerate(u) if t not in MARK]
    if len(words)==len(e):
        res=[[] for _ in u]
        for n,i in enumerate(words): res[i]=[n]
        return res
    # returns list per uthmani token: list of emlaey indices ([] for markers)
    res=[];j=0;i=0
    while i<len(u):
        if u[i] in MARK: res.append([]); i+=1; continue
        a=sk(u[i])
        if j<len(e) and a==sk(e[j]): res.append([j]); i+=1; j+=1; continue
        if j+1<len(e) and a==sk(e[j]+e[j+1]): res.append([j,j+1]); i+=1; j+=2; continue
        if j+2<len(e) and a==sk(e[j]+e[j+1]+e[j+2]): res.append([j,j+1,j+2]); i+=1; j+=3; continue
        nxt=i+1
        while nxt<len(u) and u[nxt] in MARK: nxt+=1
        if nxt<len(u) and j<len(e) and sk(u[i]+u[nxt])==sk(e[j]): res.append([j]); res.append([]) ; i+=2; j+=1; continue  # NOTE simplistic
        if j<len(e): res.append([j]); i+=1; j+=1; continue   # fallback 1:1 (spelling differs)
        return None
    return res if j==len(e) else None
out={};fails=[];fallback=0
for r in K:
    k=f"{r['sura_no']}:{r['aya_no']}"; u=C[k].split(); e=r['aya_text_emlaey'].split()
    m=mapayah(u,e)
    if m is None: fails.append(k); continue
    out[k]=m
print('mapped',len(out),'fails',len(fails),fails[:20])
json.dump(out,open('wordmap.json','w'))

import difflib
def r(a,b): return difflib.SequenceMatcher(None,a,b).ratio()
weak=[]
for x in K:
    k=f"{x['sura_no']}:{x['aya_no']}"
    if k not in out: continue
    u=C[k].split(); e=x['aya_text_emlaey'].split()
    for i,g in enumerate(out[k]):
        if not g: continue
        a=sk(u[i]); b=sk(''.join(e[j] for j in g))
        if a!=b: weak.append((k,u[i],' '.join(e[j] for j in g),round(r(norm(u[i]),norm(''.join(e[j] for j in g))),2)))
print('non-exact groups',len(weak))
import collections
print('lowest:',sorted(weak,key=lambda t:t[3])[:25])
for k in fails:
    x=[y for y in K if f"{y['sura_no']}:{y['aya_no']}"==k][0]
    print(k,' U:',' | '.join(C[k].split()),'\n  E:',' | '.join(x['aya_text_emlaey'].split()))

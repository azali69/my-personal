import json,sqlite3,collections,re
Q='/tmp/claude-0/qul/'
W=json.load(open(Q+'qpc-v4.json')); byid={v['id']:v for v in W.values()}
c=sqlite3.connect(Q+'qpc-v4-tajweed-15-lines.db')
rows=c.execute("select page_number,line_number,line_type,is_centered,first_word_id,last_word_id,surah_number from pages order by page_number,line_number").fetchall()
K=json.load(open('kfgqpc_hafs_v2.json')); C=json.load(open('kfgqpc_clean.json'))
gidx={(r['sura_no'],r['aya_no']):i for i,r in enumerate(K)}
MARK=('۞','۩')
lastpos=collections.defaultdict(int)
for v in W.values(): k=(int(v['surah']),int(v['ayah'])); lastpos[k]=max(lastpos[k],int(v['word']))
# my non-marker word counts
nW={k:len([t for t in C[f"{k[0]}:{k[1]}"].split(' ') if t not in MARK]) for k in gidx}
P=[[] for _ in range(604)]; adj=collections.Counter()
for p,ln,t,cen,a,b,sn in rows:
    if t=='surah_name': P[p-1].append(['h',sn]); continue
    if t=='basmallah': P[p-1].append(['b']); continue
    words=[];gs=[];ps=[]
    for i in range(a,b+1):
        w=byid[i]; k=(int(w['surah']),int(w['ayah'])); g=gidx[k]
        end=int(w['word'])==lastpos[k]
        words.append(w['text']); gs.append(-(g+1) if end else g)
        if end: ps.append(nW[k]-1)
        else:
            q=lastpos[k]-1; o=int(w['word'])-1
            if q!=nW[k]: adj[k]+=1; o=round(o*(nW[k]-1)/max(1,q-1)) if q>1 else 0   # 4 ayat split words differently; scale
            ps.append(min(o,nW[k]-1))
    P[p-1].append([1 if cen else 0, words, gs, ps])
bas=[W[f'1:1:{i}']['text'] for i in range(1,5)]
json.dump({'P':P,'bas':bas},open('/home/claude/app/glyph.json','w'),ensure_ascii=False,separators=(',',':'))
print('adjusted ayat',sorted(adj))

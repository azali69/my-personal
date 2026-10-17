import json,os,re,collections
P='qm/node_modules/quran-qcf4/pages/'
C=json.load(open('kfgqpc_clean.json')); K=json.load(open('kfgqpc_hafs_v2.json'))
gidx={f"{r['sura_no']}:{r['aya_no']}":i for i,r in enumerate(K)}
MARK=('۞','۩')
UNI={'آ':'ا','أ':'ا','إ':'ا','ٱ':'ا','ؤ':'و','ئ':'ي','ى':'ي','ة':'ه','ـ':''}
def sk(w):
    o=''
    for ch in w:
        c=ord(ch)
        if 0x610<=c<=0x61A or 0x64B<=c<=0x65F or c==0x670 or 0x6D6<=c<=0x6ED: continue
        ch=UNI.get(ch,ch)
        if ch and 0x600<=ord(ch[0])<=0x6FF: o+=ch
    return re.sub('[اويء]','',o)
# collect qcf word order per verse
qwords=collections.defaultdict(list)
pages=[]
for f in sorted(os.listdir(P)):
    d=json.load(open(P+f)); pages.append(d)
    for l in d['lines']:
        for w in l['words']:
            if w['type']=='word' and not w['text'].startswith('#'): qwords[w['verse_key']].append(w['text'])
# map qcf word ordinal -> my token index, per verse
qmap={}
for k,t in C.items():
    toks=t.split(' '); wi=[i for i,x in enumerate(toks) if x not in MARK]; q=qwords[k]
    if len(wi)==len(q): qmap[k]=wi; continue
    m=[];i=0;j=0
    while j<len(q):
        if i<len(wi) and sk(toks[wi[i]])==sk(q[j]): m.append(wi[i]); i+=1; j+=1
        elif i<len(wi) and j+1<len(q) and sk(toks[wi[i]])==sk(q[j]+q[j+1]): m+= [wi[i],wi[i]]; i+=1; j+=2
        else: raise SystemExit(f'cannot map {k}')
    assert i==len(wi); qmap[k]=m
L=[];seen=collections.defaultdict(set);issues=[]
for d in pages:
    pl=[]
    for l in d['lines']:
        items=[];ord_=collections.Counter()
        for w in l['words']:
            ty=w['type']
            if ty=='surah_header': items.append(['h',w['sura']])
            elif ty=='bismillah': items.append(['b'])
            elif ty=='quarter':
                k=w['verse_key']; toks=C[k].split(' ')
                if '۞' in toks: items.append(gidx[k]*256+toks.index('۞')); seen[k].add(toks.index('۞'))
                else: issues.append(('noquarter',k))
            elif ty=='end': items.append(-(gidx[w['verse_key']]+1))
            elif ty=='word':
                if w['text'].startswith('#'): continue
                k=w['verse_key']
                # ordinal of this word within verse = count of qcf words seen so far
                n=qwords_pos[k] if (qwords_pos:=globals().setdefault('QP',collections.Counter())) is None else globals()['QP'][k]
                ti=qmap[k][globals()['QP'][k]]; globals()['QP'][k]+=1
                v=gidx[k]*256+ti
                if items and items[-1]==v: continue   # split word already placed
                items.append(v); seen[k].add(ti)
        pl.append(items)
    L.append(pl)
# completeness: every token of every verse appears exactly in order
miss=0
for k,t in C.items():
    toks=t.split(' ')
    if set(range(len(toks)))!=seen[k]: miss+=1; issues.append(('missing',k,sorted(set(range(len(toks)))-seen[k])))
print('pages',len(L),'lines',sum(len(p) for p in L),'verses with missing tokens',miss, issues[:10])
# order check: flatten all word refs, must be strictly increasing
flat=[x for p in L for l in p for x in l if isinstance(x,int) and x>=0]
print('monotonic', all(a<b for a,b in zip(flat,flat[1:])), 'tokens',len(flat))
json.dump(L,open('/home/claude/app/layout.json','w'),separators=(',',':'))
print(os.path.getsize('/home/claude/app/layout.json')/1e6,'MB')

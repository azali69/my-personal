import json,unicodedata,re,collections
T=json.load(open('uthmani.json')); Q=json.load(open('qpc-hafs.json'))
def skel(s):
    out=[]
    for ch in s:
        c=ord(ch)
        cat=unicodedata.category(ch)
        if cat in('Mn','Me','Cf') : continue          # all harakat, small marks, waqf signs
        if 0x06D6<=c<=0x06ED: continue                # Quranic annotation signs
        if ch in 'ـ': continue                   # tatweel
        if ch in '۞۩': continue                       # rub' / sajdah symbols
        m={'ٱ':'ا','أ':'ا','إ':'ا','آ':'ا','ى':'ي','ی':'ي','ۦ':'','ۥ':'','ـ':'','ک':'ك','ہ':'ه'}
        ch=m.get(ch,ch)
        out.append(ch)
    return re.sub(r'\s+',' ',''.join(out)).strip()
n=0;diff=[]
for s in range(1,115):
    a,b=T[str(s)],Q[str(s)]
    assert len(a)==len(b),(s,len(a),len(b))
    for x,y in zip(a,b):
        n+=1
        if skel(x['text'])!=skel(y['text']): diff.append((s,x['verse'],skel(x['text']),skel(y['text'])))
print('verses',n,'differ',len(diff))
for d in diff[:15]: print(d[0],d[1],'\n T:',d[2][:150],'\n Q:',d[3][:150])
json.dump(diff,open('diff.json','w'),ensure_ascii=False)

BAS=T['1'][0]['text']
print('basmala:',BAS)
def tbody(s,v,t):
    if v==1 and s not in(1,9):
        w=t.split(' ')
        assert ' '.join(w[1:4])==' '.join(BAS.split(' ')[1:4]) and w[0] in ('\u0628\u0650\u0633\u0652\u0645\u0650','\u0628\u0651\u0650\u0633\u0652\u0645\u0650'),(s,t[:60])
        return ' '.join(w[4:])
    return t
def skel2(s):
    s=s.replace('ٔ','ء').replace('ٕ','ء')  # hamza above/below as combining -> letter
    return skel(s).replace('ـ','')
diff2=[]
for s in range(1,115):
    for x,y in zip(T[str(s)],Q[str(s)]):
        a=skel2(tbody(s,x['verse'],x['text'])); b=skel2(y['text'])
        if a!=b:
            wa,wb=a.split(),b.split()
            import difflib
            ops=[(t,' '.join(wa[i1:i2]),' '.join(wb[j1:j2])) for t,i1,i2,j1,j2 in difflib.SequenceMatcher(None,wa,wb).get_opcodes() if t!='equal']
            diff2.append((s,x['verse'],ops))
print('after basmala + hamza encoding:',len(diff2))
cnt=collections.Counter((o[1],o[2]) for d in diff2 for o in d[2])
for k,v in cnt.most_common(60): print(v,k)

def skel3(s): return skel2(s).replace('ء','').replace('ئ','ي').replace('ؤ','و')
res=[];spacing=[]
for s in range(1,115):
    for x,y in zip(T[str(s)],Q[str(s)]):
        a=skel3(tbody(s,x['verse'],x['text'])); b=skel3(y['text'])
        if a!=b:
            if a.replace(' ','')==b.replace(' ',''): spacing.append((s,x['verse']))
            else: res.append((s,x['verse'],a,b))
print('residual letter differences:',len(res)); 
for r in res: print(r)
print('spacing-only verses:',spacing)

"""Ayat with similar wording (mutashabihat in wording), computed from the plain Arabic text (tools/quran-plain.json).
Two ayat are linked when they share a run of at least 5 consecutive words (after removing harakat and unifying
alif/ya/ta marbuta forms), or are the same ayah word for word (3+ words). Runs made only of very common phrases
(a 4-word piece found in more than 15 ayat, e.g. "إن الله على كل شيء قدير") do not count: the two ayat must share at
least two 4-word pieces that are each found in 15 ayat or fewer.
Output quran/similar.json: {"s:a": [[s, a, words_shared], ...]} up to 8 per ayah, longest shared run first."""
import json,re,collections
Q=json.load(open('tools/quran-plain.json'))
def norm(t):
    t=re.sub(r'[ً-ْٰـۖ-ۭ]','',t)
    t=re.sub('[إأآٱ]','ا',t).replace('ى','ي').replace('ة','ه').replace('ؤ','و').replace('ئ','ي')
    return t.split()
W={(s,a):norm(t) for s,a,t in Q}
keys=list(W); N=4
sh=collections.defaultdict(set)
for k,w in W.items():
    for i in range(len(w)-N+1): sh[tuple(w[i:i+N])].add(k)
df={g:len(v) for g,v in sh.items()}
def run(a,b):
    # longest common run of words between two ayat (dynamic programming, ayat are short)
    A,B=W[a],W[b]; best=0; prev=[0]*(len(B)+1)
    for i in range(1,len(A)+1):
        cur=[0]*(len(B)+1)
        for j in range(1,len(B)+1):
            if A[i-1]==B[j-1]:
                cur[j]=prev[j-1]+1
                if cur[j]>best: best=cur[j]
        prev=cur
    return best
out={}
byText=collections.defaultdict(list)
for k,w in W.items():
    if len(w)>=3: byText[' '.join(w)].append(k)
for k,w in W.items():
    cand=collections.Counter()
    for i in range(len(w)-N+1):
        g=tuple(w[i:i+N])
        if df[g]<=15:
            for o in sh[g]:
                if o!=k: cand[o]+=1
    res=[]
    for o,c in cand.items():
        if c<2: continue          # at least two distinctive 4-word pieces in common
        r=run(k,o)
        if r>=5: res.append((o,r))
    for o in byText.get(' '.join(w),[]):
        if o!=k and all(o!=x for x,_ in res): res.append((o,len(w)))
    res.sort(key=lambda x:(-x[1],x[0]))
    if res: out[f'{k[0]}:{k[1]}']=[[o[0],o[1],r] for o,r in res[:8]]
json.dump(out,open('quran/similar.json','w'),separators=(',',':'))
print(len(out),'ayat linked; sample 2:255',out.get('2:255'),'2:2',out.get('2:2'),'55:13',out.get('55:13'))

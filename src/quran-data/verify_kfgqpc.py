import json
K=json.load(open('kfgqpc_hafs_v2.json')); Q=json.load(open('qpc-hafs.json'))
def clean(t):
    w=t.replace('\xa0',' ').rstrip().split(' ')
    if all(0xFB50<=ord(c)<=0xFEFF or 0xE000<=ord(c)<=0xF8FF for c in w[-1]): w=w[:-1]
    return ' '.join(w)
same=diff=0
for r in K:
    q=Q[str(r['sura_no'])][r['aya_no']-1]['text']
    if clean(r['aya_text'])==q: same+=1
    else:
        diff+=1
        if diff<4: print(r['sura_no'],r['aya_no'],repr(clean(r['aya_text'])[-25:]),repr(q[-25:]))
print('identical',same,'different',diff)

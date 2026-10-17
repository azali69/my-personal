import json,hashlib
K=json.load(open('kfgqpc_hafs_v2.json')); C=json.load(open('kfgqpc_clean.json')); M=json.load(open('wordmap.json'))
ch=json.load(open('chapters.json'))['chapters']; N=json.load(open('names.json'))
MS=json.load(open('malay_basumayyah.json')); EN=json.load(open('english_saheeh.json'))
import subprocess
rk=json.load(open('info.json'))['rukus']['references']
S=[];A=[]
names={r['sura_no']:(r['sura_name_ar'],r['sura_name_en']) for r in K}
for c in ch:
    s=c['id']; S.append([names[s][0],names[s][1],N[s-1][0],N[s-1][1],'M' if c['type']=='meccan' else 'D',c['total_verses']])
for r in K:
    k=f"{r['sura_no']}:{r['aya_no']}"; u=C[k].split(' ')
    m=M[k]; one=[[i] for i in range(len(u))]
    a=[r['sura_no'],r['aya_no'],C[k],r['aya_text_emlaey'],r['page'],r['jozz'],
       MS[str(r['sura_no'])][r['aya_no']-1]['text'],
       EN[str(r['sura_no'])][r['aya_no']-1]['text'],
       EN[str(r['sura_no'])][r['aya_no']-1].get('footnotes') or '']
    # wordmap: only store when not trivial identity
    ident = len(m)==len(r['aya_text_emlaey'].split()) and all(g==[i] for i,g in enumerate(m))
    a.append(0 if ident else m)
    A.append(a)
R=[[x['start']['chapter'],x['start']['verse']] for x in rk]
def h(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()
quran_text='\n'.join(a[2] for a in A)
D={'S':S,'A':A,'R':R,'L':json.load(open('/home/claude/app/layout.json')),'G':json.load(open('/home/claude/app/glyph.json')),'hash':{'uthmani':h(quran_text),'imlaei':h('\n'.join(a[3] for a in A)),'ms':h('\n'.join(a[6] for a in A)),'en':h('\n'.join(a[7] for a in A))}}
s=json.dumps(D,ensure_ascii=False,separators=(',',':'))
open('/home/claude/app/data.json','w').write(s)
print(len(A),len(s)/1e6,'MB',D['hash'])
# self-check: every displayed ayah text identical to official KFGQPC source after stripping ayah-number glyph
exec(open('verify_kfgqpc.py').read().split('same=diff=0')[0])
ok=all(A[i][2]==clean(K[i]['aya_text']).strip() for i in range(6236)); print('display text == official KFGQPC:',ok)

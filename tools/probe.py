import urllib.request, urllib.parse, re, os
UA={'User-Agent':'MyPersonalQuran/1.0 (github.com/azali69/my-personal)'}
def raw(t): return urllib.request.urlopen(urllib.request.Request('https://ar.wikisource.org/w/index.php?action=raw&title='+urllib.parse.quote(t),headers=UA),timeout=60).read().decode('utf-8','replace')
os.makedirs('tools/sources',exist_ok=True)
def clean(s): s=re.sub(r'\{\{[^{}]*\}\}','',s); return re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]',r'\1',s)
z=clean(raw('زاد المعاد/المجلد الأول'))
parts=[]
for key in ['فصل في أولاده','فصل في أزواجه','فصل في سراريه','فصل في أعمامه']:
    i=z.find(key)
    if i>=0: parts.append(z[i:i+9000] if key!='فصل في أعمامه' else '')
open('tools/sources/zad_al_maad_v1_family.txt','w').write('Source: Ibn al-Qayyim, Zad al-Ma\'ad, vol. 1, from ar.wikisource.org "زاد المعاد/المجلد الأول" (retrieved by tools/probe.py)\n\n'+'\n\n=====\n\n'.join(p for p in parts if p))
for t,f in [('البداية والنهاية/الجزء الخامس/باب زوجاته وأولاده صلى الله عليه وسلم','bidayah_v5_wives.txt'),('البداية والنهاية/الجزء الخامس/فصل في ذكر أولاده عليه الصلاة والسلام','bidayah_v5_children.txt'),('البداية والنهاية/الجزء الخامس/فصل في ذكر سراريه عليه السلام','bidayah_v5_concubines.txt')]:
    open('tools/sources/'+f,'w').write('Source: Ibn Kathir, al-Bidayah wa al-Nihayah, ar.wikisource.org "'+t+'"\n\n'+clean(raw(t)))
print(os.listdir('tools/sources'), len(z))

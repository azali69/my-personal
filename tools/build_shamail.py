"""Builds the Shama'il of at-Tirmidhi as an eighth book in kutub/ (kutub/shamail/<chapter>.json, same record format).
Sources (fetched 15 Oct 2026, saved in shamail_src/):
 - Sunnah.com, Ash-Shama'il al-Muhammadiyah: Arabic, English translation, and the gradings of Zubair 'Ali Za'i (400 hadith,
   numbered 1-417 as on Sunnah.com; 17 numbers are not on Sunnah.com).
 - al-Albani, Mukhtasar ash-Shama'il al-Muhammadiyyah (al-Maktabah al-Islamiyyah, Amman), text from usul.ai: his grading
   of each hadith he kept. Linked to the Shama'il hadith by comparing the Arabic (4-word pieces); his number is shown.
No Malay or Indonesian translation is open for this book, so those are left empty (see "Also in" for the same hadith in
the six books, which have the Indonesian)."""
import json,re,collections,hashlib,os
R=os.path.join(os.path.dirname(__file__),'..'); src=lambda f:json.load(open(os.path.join(R,'shamail_src',f)))
C=src('sunnah_shamail.json'); M=src('albani_mukhtasar_shamail.json')
def norm(t):
    t=re.sub(r'[ً-ْٰـ]','',t); t=re.sub('[إأآٱ]','ا',t).replace('ى','ي').replace('ة','ه')
    t=re.sub(r'صلي الله عليه وسلم|ﷺ','',t); t=re.sub(r'[^ء-ي ]',' ',t); return t.split()
K=4; gram=lambda w:set(tuple(w[i:i+K]) for i in range(len(w)-K+1))
H=[h for c in C for h in c['h']]; HS=[gram(norm(h['ar'])) for h in H]
df=collections.Counter(g for s in HS for g in s); inv=collections.defaultdict(list)
for i,s in enumerate(HS):
    for g in s: inv[g].append(i)
alb={}
for m in M:
    if not m['gr']: continue
    mg=gram(norm(m['ar'])); c=collections.Counter()
    for g in mg:
        if df[g]<=6:
            for i in inv[g]: c[i]+=1
    if not c: continue
    i,k=c.most_common(1)[0]; sc=k/max(1,len(mg))
    if sc>=0.35 and (i not in alb or sc>alb[i][2]): alb[i]=(m['n'],m['gr'],sc)
AG={'صحيح':'Sahih','حسن':'Hasan','ضعيف':"Da'if",'ضعيف جدا':"Very Da'if"}
def zub(g):
    g=re.sub(r"\s*\(Zubair `Aliza'i\)",'',g).replace('Isnād','Isnad').replace('Hadīth','hadith')
    m=re.match(r"(Sahih|Hasan|Da'if) Isnad$",g)
    if m: return 'Isnad '+m.group(1)
    return {"Sanad Da'if Jiddan":"Isnad Very Da'if","Sanad Da'if wal-hadith Hasan":"Isnad Da'if, the hadith Hasan","Sanad Da'if wal-hadith Sahih":"Isnad Da'if, the hadith Sahih","Sahih Muttafaq 'alay":"Sahih - Agreed Upon"}.get(g,g)
# "Sayyidina Rasoolullah" in Sunnah.com's chapter titles -> "Sayyidina Rasulullah ﷺ" (Azli, 20 Oct 2026); elsewhere "Allah's Messenger ﷺ"
TITLE=lambda s:re.sub(r"\bRasoolullah\b","Allah's Messenger ﷺ",re.sub(r"\bSayyidina Rasoolullah\b","Sayyidina Rasulullah ﷺ",s)).replace("Of Allah's Messenger ﷺ","of Allah's Messenger ﷺ")
os.makedirs(os.path.join(R,'kutub','shamail'),exist_ok=True); sections=[]; idx=0
for c in C:
    recs=[]
    for k,h in enumerate(c['h'],1):
        i=H.index(h); gr=[['zub',zub(g)] for g in h['gr']]
        if i in alb: gr.append(['alb', AG.get(alb[i][1], alb[i][1].replace('صحيح دون قوله:','Sahih, except the words:')) + f" (Mukhtasar {alb[i][0]})"])
        en=(h['nar']+' '+h['en']).strip()
        recs.append([h['n'],k,h['ar'],en,'',gr,0,0])
    data={'h':recs}; s=json.dumps(data,ensure_ascii=False,separators=(',',':'))
    open(os.path.join(R,'kutub','shamail',f"{c['n']}.json"),'w').write(s)
    ns=[r[0] for r in recs]
    sections.append({'n':c['n'],'en':TITLE(c['en']),'ar':c['ar'],'first':min(ns),'last':max(ns),'count':len(recs),'v':hashlib.md5(s.encode()).hexdigest()[:8]})
B=json.load(open(os.path.join(R,'kutub','books.json')))   # written to books2.json (books.json + this book); the released app keeps reading books.json
B['books']=[b for b in B['books'] if b['id']!='shamail']+[{'id':'shamail','ar':'الشمائل المحمدية','en':"Asy-Syama'il al-Muhammadiyyah",'count':sum(s['count'] for s in sections),'sections':sections}]
json.dump(B,open(os.path.join(R,'kutub','books2.json'),'w'),ensure_ascii=False,separators=(',',':'))
print(len(sections),'chapters',sum(s['count'] for s in sections),'hadith;',len(alb),"with al-Albani's grading")

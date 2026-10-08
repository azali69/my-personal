# For one reciter edition and surah: download timings + audio, measure how well verse starts sit on pauses,
# and compute a per-verse shift that moves each verse start onto the speech onset after the nearest pause.
import json, sys, subprocess, urllib.request, numpy as np, os
rid, s = sys.argv[1], int(sys.argv[2])
UA={'User-Agent':'Mozilla/5.0'}
d=json.load(urllib.request.urlopen(urllib.request.Request(f"https://api.qurancdn.com/api/qdc/audio/reciters/{rid}/audio_files?chapter={s}&segments=true",headers=UA),timeout=60))['audio_files'][0]
v=d['verse_timings']; url=d['audio_url']
raw=subprocess.run(['ffmpeg','-v','error','-user_agent','Mozilla/5.0','-i',url,'-ac','1','-ar','8000','-f','s16le','-'],capture_output=True,timeout=900).stdout
x=np.frombuffer(raw,dtype=np.int16).astype(np.float32)
hop=80; n=len(x)//hop; env=np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1)); med=float(np.median(env)) or 1.0; e=env/med
def at(ms): i=int(ms/10); return float(e[min(max(i,0),n-1)])
def onset(ms, win=700):
    c=int(ms/10); lo=max(0,c-win//10); hi=min(n-1,c+win//10)
    q=np.where(e[lo:hi]<0.12)[0]
    if len(q)==0: return None
    # quiet frames grouped into runs; pick the run nearest the timestamp, then the first loud frame after it
    runs=np.split(q, np.where(np.diff(q)!=1)[0]+1); best=min(runs,key=lambda r: abs(lo+r[-1]+1-c)); k=lo+best[-1]+1
    while k<min(n-1,hi+50) and e[k]<0.3: k+=1
    return k*10
deltas=[]; before=[]; after=[]
for i,t in enumerate(v):
    f=t['timestamp_from']; before.append(at(f+30))
    if i==0: deltas.append(0); after.append(before[-1]); continue
    o=onset(f)
    dl=0 if o is None else int(o-60-f)       # start the highlight 60 ms before the voice
    if abs(dl)>650: dl=0
    deltas.append(dl); after.append(at(f+dl+30))
res={'rid':rid,'s':s,'url':url,'file_s':round(len(x)/8000,1),'end_s':round(v[-1]['timestamp_to']/1000,1),
     'before':round(float(np.median(before)),2),'after':round(float(np.median(after)),2),
     'good_before':round(float(np.mean(np.array(before)<0.3)),2),'good_after':round(float(np.mean(np.array(after)<0.3)),2),'d':deltas}
os.makedirs('o/al',exist_ok=True); json.dump(res,open(f'o/al/{rid}_{s}.json','w'))
print(rid,s,res['before'],'->',res['after'],res['good_before'],'->',res['good_after'])

# Is a reciter's word timing offset from (or drifting against) its audio? For 30-second windows, find the time shift
# that best matches "speech according to the timings" with "loudness of the recording". Positive = text is early.
import json, sys, subprocess, urllib.request, numpy as np
rid, s = sys.argv[1], int(sys.argv[2])
d=json.load(urllib.request.urlopen(urllib.request.Request(f"https://api.qurancdn.com/api/qdc/audio/reciters/{rid}/audio_files?chapter={s}&segments=true",headers={'User-Agent':'Mozilla/5.0'}),timeout=60))['audio_files'][0]
raw=subprocess.run(['ffmpeg','-v','error','-user_agent','Mozilla/5.0','-i',d['audio_url'],'-ac','1','-ar','8000','-f','s16le','-'],capture_output=True,timeout=900).stdout
x=np.frombuffer(raw,dtype=np.int16).astype(np.float32); hop=80; n=len(x)//hop
env=np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1)); env=np.log1p(env); env=(env-env.mean())/(env.std()+1e-9)
sp=np.zeros(n)
for t in d['verse_timings']:
    for g in (t.get('segments') or []):
        if len(g)>=3: a,b=int(g[1]/10),int(g[2]/10); sp[max(0,a):min(n,b)]=1
sp=(sp-sp.mean())/(sp.std()+1e-9)
out=[]
W=3000 if n>4500 else max(600,n-200)
for w0 in range(0,max(1,n-W),W):
    best=max(range(-300,301,5),key=lambda k: float(np.dot(sp[w0:w0+W], env[w0+k:w0+W+k])) if 0<=w0+k and w0+W+k<=n else -1e18)
    out.append(best*10)
import os; os.makedirs('o/dr',exist_ok=True); json.dump({'rid':rid,'s':s,'w':out},open(f'o/dr/{rid}_{s}.json','w')); print(rid,s,out)

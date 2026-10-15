import easyocr, glob, time
r=easyocr.Reader(['ar','en'], gpu=False)
for f in sorted(glob.glob('img/*.jpg')):
    t=time.time(); res=r.readtext(f, detail=0, paragraph=True)
    print(f, round(time.time()-t,1), res, flush=True)

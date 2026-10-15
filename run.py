import glob, json, sys, time
from paddleocr import PaddleOCR
out={}
for lang in ['ar']:
    ocr=PaddleOCR(lang=lang, use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=False)
    for f in sorted(glob.glob('img/*.jpg')):
        t=time.time(); r=ocr.predict(f)
        txt=[]
        for page in r:
            txt += list(page['rec_texts'])
        out[f+'|'+lang]={'t':round(time.time()-t,1),'lines':txt}
        print(f, lang, txt, flush=True)
json.dump(out,open('out/result.json','w'),ensure_ascii=False,indent=1)

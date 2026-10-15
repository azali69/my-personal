# The same steps the Android app will run: Paddle text-line detection (DB) + EasyOCR Arabic recognition, both ONNX.
import onnxruntime as ort, numpy as np, json, glob, sys, time, os
from PIL import Image
from scipy import ndimage
import rapidocr_onnxruntime as R
DET = glob.glob(os.path.join(os.path.dirname(R.__file__), 'models', '*det*.onnx'))[0]
print('det model', DET, os.path.getsize(DET))
det = ort.InferenceSession(DET); REC = sys.argv[1]
rec = ort.InferenceSession(REC); meta = json.load(open('out/ar_rec.json'))
chars = ['[blank]'] + list(meta['chars']); ign = [chars.index(c) for c in meta['ignore'] if c in chars]
def detect(img):
    W, H = img.size; s = min(1.0, 960 / max(W, H)); w2 = max(32, int(round(W * s / 32)) * 32); h2 = max(32, int(round(H * s / 32)) * 32)
    a = np.asarray(img.convert('RGB').resize((w2, h2), Image.BILINEAR), dtype=np.float32) / 255.0
    a = (a - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    p = det.run(None, {det.get_inputs()[0].name: a.transpose(2, 0, 1)[None].astype(np.float32)})[0][0, 0]
    lab, n = ndimage.label(p > 0.3); boxes = []
    for i, sl in enumerate(ndimage.find_objects(lab)):
        if sl is None: continue
        y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
        if (y1 - y0) < 3 or (x1 - x0) < 3: continue
        if p[sl][lab[sl] == i + 1].mean() < 0.6: continue
        bw, bh = x1 - x0, y1 - y0; d = bw * bh * 1.5 / (2 * (bw + bh))   # DB "unclip" for a rectangle
        boxes.append([max(0, (x0 - d) * W / w2), max(0, (y0 - d) * H / h2), min(W, (x1 + d) * W / w2), min(H, (y1 + d) * H / h2)])
    return boxes
def order(boxes):
    boxes = sorted(boxes, key=lambda b: (b[1] + b[3]) / 2); rows = []
    for b in boxes:
        c = (b[1] + b[3]) / 2
        if rows and abs(c - rows[-1][0]) < 0.5 * (b[3] - b[1]): rows[-1][1].append(b)
        else: rows.append([c, [b]])
    return [sorted(r[1], key=lambda b: -b[2]) for r in rows]
def logical(s):
    # the model reads left to right; Arabic is stored right to left: reverse, then put Latin/digit runs back in order
    out = s[::-1]; res = []; run = ''
    for ch in out:
        if ch.isascii() and (ch.isalnum()): run += ch
        else:
            if run: res.append(run[::-1]); run = ''
            res.append(ch)
    if run: res.append(run[::-1])
    return ''.join(res)
def recognize(gray, b):
    x0, y0, x1, y1 = [int(round(v)) for v in b]; crop = gray.crop((x0, y0, x1, y1))
    w = max(8, int(np.ceil(64 * crop.width / max(1, crop.height)))); crop = crop.resize((w, 64), Image.LANCZOS)
    a = (np.asarray(crop, dtype=np.float32) / 255.0 - 0.5) / 0.5
    y = rec.run(None, {'x': a[None, None]})[0][0]
    y[:, ign] = -1e9; idx = y.argmax(1); s = ''; prev = 0
    for k in idx:
        if k != prev and k != 0: s += chars[k]
        prev = k
    return logical(s)
for f in sorted(glob.glob('img/*.jpg')):
    t = time.time(); img = Image.open(f); gray = img.convert('L')
    lines = [' '.join(recognize(gray, b) for b in row) for row in order(detect(img))]
    print(f, round(time.time() - t, 1), lines, flush=True)

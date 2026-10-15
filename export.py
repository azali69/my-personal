import easyocr, torch, json, os
r = easyocr.Reader(['ar','en'], gpu=False, quantize=False, verbose=False)
m = r.recognizer; m.eval()
class MeanH(torch.nn.Module):
    def forward(s, x): return x.mean(dim=3, keepdim=True)   # same as AdaptiveAvgPool2d((None,1)) here, but exportable
m.AdaptiveAvgPool = MeanH()
class W(torch.nn.Module):
    def __init__(s, m): super().__init__(); s.m = m
    def forward(s, x): return s.m(x, None)
w = W(m)
x = torch.randn(1, 1, 64, 320)
os.makedirs('out', exist_ok=True)
torch.onnx.export(w, x, 'out/ar_rec.onnx', input_names=['x'], output_names=['y'], dynamic_axes={'x': {3: 'w'}, 'y': {1: 't'}}, opset_version=17, dynamo=False)
ignore = ''.join(sorted(set(r.character) - set(r.lang_char)))
json.dump({'chars': r.character, 'ignore': ignore}, open('out/ar_rec.json', 'w'), ensure_ascii=False)
from onnxruntime.quantization import quantize_dynamic, QuantType
quantize_dynamic('out/ar_rec.onnx', 'out/ar_rec_q.onnx', weight_type=QuantType.QUInt8)
for f in os.listdir('out'): print(f, os.path.getsize('out/'+f))

import sys, numpy as np, librosa, torch
from transformers import ASTFeatureExtractor, ASTForAudioClassification
d = sys.argv[1]
sr = 16000
stems = {n: librosa.load(f"{d}/{n}.wav", sr=sr, mono=True)[0] for n in ("vocals","drums","bass","other")}
for n,y in stems.items():
    rms = librosa.feature.rms(y=y, frame_length=8000, hop_length=8000)[0]
    print(n, "mean dB", round(float(20*np.log10(np.mean(rms)+1e-9)),1), "max dB", round(float(20*np.log10(np.max(rms)+1e-9)),1))
# spectral centroid of music
music = stems["drums"]+stems["bass"]+stems["other"]
cent = librosa.feature.spectral_centroid(y=music, sr=sr)[0]
print("music spectral centroid median Hz", round(float(np.median(cent))))
fe = ASTFeatureExtractor.from_pretrained("MIT/ast-finetuned-audioset-10-10-0.4593")
model = ASTForAudioClassification.from_pretrained("MIT/ast-finetuned-audioset-10-10-0.4593").eval()
def top(y, k=8):
    inp = fe(y, sampling_rate=sr, return_tensors="pt")
    with torch.no_grad(): p = torch.sigmoid(model(**inp).logits)[0]
    t = torch.topk(p, k); return [(model.config.id2label[int(i)], round(float(s),2)) for s,i in zip(t.values,t.indices)]
print("drums whole:", top(stems["drums"][:sr*10]))
print("other 0-10:", top(stems["other"][:sr*10]))
print("other 62-70:", top(stems["other"][sr*62:sr*70]))
print("music 62-70:", top(music[sr*62:sr*70]))
for a,b in [(19.0,21.0),(10.2,11.2),(28.8,29.8),(47.0,48.0),(51.0,52.0),(61.3,62.8),(33.3,34.3),(55.3,56.3)]:
    seg_v = stems["vocals"][int(a*sr):int(b*sr)]; seg_m = music[int(a*sr):int(b*sr)]
    print(f"{a}-{b} vocals:", top(seg_v,6)); print(f"{a}-{b} music :", top(seg_m,6))

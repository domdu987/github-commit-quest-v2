import sys, numpy as np, librosa, torch
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification
name = "alefiury/wav2vec2-large-xlsr-53-gender-recognition-librispeech"
fe = AutoFeatureExtractor.from_pretrained(name); m = AutoModelForAudioClassification.from_pretrained(name).eval()
y, sr = librosa.load(sys.argv[1], sr=16000, mono=True)
votes = []
for st in range(0, 60, 4):
    seg = y[st*sr:(st+4)*sr]
    inp = fe(seg, sampling_rate=sr, return_tensors="pt", padding=True)
    with torch.no_grad(): p = torch.softmax(m(**inp).logits, -1)[0]
    lab = {m.config.id2label[i]: round(float(p[i]),2) for i in range(len(p))}
    votes.append(lab); print(st, lab)

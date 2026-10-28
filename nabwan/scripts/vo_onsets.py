import sys, numpy as np, librosa
y, sr = librosa.load(sys.argv[1], sr=16000)
hop = 160  # 10 ms
rms = librosa.feature.rms(y=y, frame_length=640, hop_length=hop)[0]
db = 20*np.log10(rms+1e-9); thr = np.percentile(db, 95) - 28
voiced = db > thr
# phrase onsets: voiced after >=180 ms unvoiced
onsets = []; gap = 0
for i, v in enumerate(voiced):
    if v:
        if gap >= 18: onsets.append(round(i*hop/sr, 2))
        gap = 0
    else: gap += 1
print("VO phrase onsets (after >=180ms gaps):", onsets)

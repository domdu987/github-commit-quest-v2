# Split a narration take into N phrases at its N-1 longest silences. Usage: split_phrases.py <wav44> <N>
import sys, json
import numpy as np, soundfile as sf
y, sr = sf.read(sys.argv[1]); N = int(sys.argv[2])
hop = int(0.01 * sr)
rms = np.array([np.sqrt(np.mean(y[i:i + hop] ** 2)) for i in range(0, len(y) - hop, hop)])
db = 20 * np.log10(rms + 1e-9)
on = db > db.max() - 40
segs, i = [], 0
while i < len(on):
    if on[i]:
        j = i
        while j < len(on) and on[j]: j += 1
        segs.append([i, j]); i = j
    else: i += 1
merged = []
for s in segs:
    if merged and s[0] - merged[-1][1] < 18: merged[-1][1] = s[1]
    else: merged.append(s)
merged = [m for m in merged if m[1] - m[0] >= 6]
gaps = sorted(range(len(merged) - 1), key=lambda k: merged[k + 1][0] - merged[k][1], reverse=True)[:N - 1]
cuts = sorted(gaps)
phr, start = [], 0
for c in cuts + [len(merged) - 1]:
    phr.append([merged[start][0] * hop / sr, merged[c][1] * hop / sr]); start = c + 1
allg = [round((merged[k + 1][0] - merged[k][1]) * hop / sr, 2) for k in range(len(merged) - 1)]
print(json.dumps({'dur': round(len(y) / sr, 2), 'phrases': [[round(a, 2), round(b, 2)] for a, b in phr], 'gaps': allg}))

# Evaluate a fal eleven-v3 take: download, Whisper transcript, pitch range, pauses, char timeline.
# Usage: python -I vo_eval.py <res.json> <outprefix>
import sys, json, subprocess, os
import numpy as np, soundfile as sf, librosa
res = json.load(open(sys.argv[1])); pre = sys.argv[2]
mp3 = pre + '.mp3'
if not os.path.exists(mp3):
    subprocess.run(['curl', '-sS', '-o', mp3, res['audio']['url']], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp3, '-ac', '1', '-ar', '44100', pre + '44.wav'], check=True)
y, sr = sf.read(pre + '44.wav')
print(f'duration {len(y)/sr:.2f}s')
# char timeline -> words with times
chars = []
for blk in res.get('timestamps') or []:
    for c, a, b in zip(blk['characters'], blk['character_start_times_seconds'], blk['character_end_times_seconds']):
        chars.append((c, a, b))
line, t0 = '', None
for c, a, b in chars:
    if t0 is None: t0 = a
    line += c
    if c in ' .]':
        if line.strip(): print(f'  {t0:6.2f}-{b:6.2f} {line.strip()}')
        line, t0 = '', None
if line.strip(): print(f'  {t0:6.2f}-{chars[-1][2]:6.2f} {line.strip()}')
# speech/pause segments from RMS
hop = 441
rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=hop)[0]
db = 20 * np.log10(rms + 1e-9)
thr = np.max(db) - 35
on = db > thr
segs, i = [], 0
while i < len(on):
    if on[i]:
        j = i
        while j < len(on) and on[j]: j += 1
        segs.append([i * hop / sr, j * hop / sr]); i = j
    else: i += 1
merged = []
for s in segs:
    if merged and s[0] - merged[-1][1] < 0.12: merged[-1][1] = s[1]
    else: merged.append(s)
print('voiced blocks:', ' '.join(f'{a:.2f}-{b:.2f}' for a, b in merged))
print('pauses:', ' '.join(f'{merged[k+1][0]-merged[k][1]:.2f}' for k in range(len(merged) - 1)))
# pitch
y16 = librosa.resample(y, orig_sr=sr, target_sr=16000)
f0, vf, _ = librosa.pyin(y16, fmin=110, fmax=600, sr=16000, frame_length=1024)
f0 = f0[~np.isnan(f0)]
st = 12 * np.log2(f0 / np.median(f0))
print(f'F0 median {np.median(f0):.0f} Hz, range p5-p95 {np.percentile(st,5):.1f}..{np.percentile(st,95):.1f} st, std {np.std(st):.2f} st')
# loudness dynamics per voiced block
print('block loudness dB:', ' '.join(f'{np.max(db[int(a*sr/hop):int(b*sr/hop)]):.1f}' for a, b in merged))
sf.write(pre + '16.wav', y16, 16000, subtype='PCM_16')

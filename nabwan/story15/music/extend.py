# lengthen the score by ~1.2 s inside อาม่า's line (the take grew): jump back from a spot near 43 s to an earlier
# spot that sounds the same, so every later section moves with the narration
import subprocess, numpy as np, soundfile as sf
SR = 44100
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'story15/music/music.mp3', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
m = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).astype(np.float64)
mono = m.mean(1)
def spec(t, w=1.0):
    i = int(t * SR); seg = mono[i - int(w * SR): i]
    S = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
    f = np.fft.rfftfreq(len(seg), 1 / SR)
    bands = np.geomspace(80, 5000, 40)
    v = np.array([S[(f >= a) & (f < b)].mean() for a, b in zip(bands[:-1], bands[1:])])
    v = np.log(v + 1e-6); return (v - v.mean()) / (v.std() + 1e-9)
best = max(((float(spec(c) @ spec(s)) / 39, c, s) for c in np.arange(42.4, 44.6, 0.05) for s in np.arange(c - 1.45, c - 1.15, 0.02)), key=lambda x: x[0])
print('best match', [round(x, 3) for x in best])
_, cut, s = best
xf = int(0.35 * SR)
head = m[: int(cut * SR)]; tail = m[int(s * SR) - xf:]
out = np.zeros((len(head) + len(tail) - xf, 2)); out[: len(head)] = head
k = np.linspace(0, 1, xf)[:, None]
out[len(head) - xf: len(head)] = head[-xf:] * np.cos(k * np.pi / 2) + tail[:xf] * np.sin(k * np.pi / 2)
out[len(head):] = tail[xf:]
sf.write('story15/music/music_v2.wav', out.astype(np.float32), SR)
print('len', round(len(out) / SR, 2))

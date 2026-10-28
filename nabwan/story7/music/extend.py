# extend the score's tail: find an earlier spot that sounds like the music at 40.6 s and crossfade into it
import subprocess, numpy as np, soundfile as sf
SR = 44100
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'story7/music/music.mp3', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
m = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).astype(np.float64)
mono = m.mean(1)
def spec(t, w=1.0):
    i = int(t * SR); seg = mono[i - int(w * SR): i]
    S = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
    f = np.fft.rfftfreq(len(seg), 1 / SR)
    bands = np.geomspace(80, 5000, 40)
    v = np.array([S[(f >= a) & (f < b)].mean() for a, b in zip(bands[:-1], bands[1:])])
    v = np.log(v + 1e-6); return (v - v.mean()) / (v.std() + 1e-9)
cut = 40.6
ref = spec(cut)
best = max(((float(ref @ spec(s)) / len(ref), s) for s in np.arange(18.0, 36.0, 0.02)), key=lambda x: x[0])
print('best match', best)
s = best[1]
need = 44.6 - cut
xf = int(0.5 * SR)
head = m[: int(cut * SR)].copy()
tail = m[int(s * SR) - xf: int((s + need) * SR)].copy()
out = np.zeros((len(head) + len(tail) - xf, 2))
out[: len(head)] = head
k = np.linspace(0, 1, xf)[:, None]
out[len(head) - xf: len(head)] = head[-xf:] * np.cos(k * np.pi / 2) + tail[:xf] * np.sin(k * np.pi / 2)
out[len(head):] = tail[xf:]
fo = int(2.2 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
sf.write('story7/music/music_v2.wav', out.astype(np.float32), SR)
print('len', len(out) / SR)

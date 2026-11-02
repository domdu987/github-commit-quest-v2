import json, subprocess, sys, numpy as np
SR = 48000
def load(p):
    return np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"]), np.float32)
sc = json.load(open("schedule.json"))
speech = []
for s in sc["shots"]:
    for v in s["vo"]:
        speech.append((s["start"] + v["t"] - 0.1, s["start"] + v["t"] + v["dur"] + 0.1))
def report(path):
    x = load(path); W = 2048; H = 1024; n = (len(x) - W) // H
    win = np.hanning(W); fq = np.fft.rfftfreq(W, 1 / SR); band = (fq >= 5000) & (fq <= 14000); fb = (fq >= 2000) & (fq <= 14000)
    hf, flat, tt = [], [], []
    for i in range(n):
        seg = x[i * H:i * H + W] * win; P = np.abs(np.fft.rfft(seg)) ** 2 + 1e-20
        hf.append(10 * np.log10(P[band].mean())); b = P[fb]; flat.append(np.exp(np.log(b).mean()) / b.mean()); tt.append((i * H + W / 2) / SR)
    hf, flat, tt = map(np.array, (hf, flat, tt))
    ns = np.array([not any(a <= t <= b for a, b in speech) for t in tt])
    loud = hf > (np.max(hf) - 60)   # ignore digital silence
    m = ns & loud
    hf_ns = 10 * np.log10(np.mean(10 ** (hf[ns] / 10)))
    # flat noise runs: flatness > 0.35 with real HF energy, in non-speech frames, lasting > 0.5 s
    f = (flat > 0.35) & m
    runs, cur, st = [], 0, 0
    for i, v in enumerate(f):
        if v: cur += 1; st = st if cur > 1 else tt[i]
        else:
            if cur * H / SR > 0.5: runs.append((round(st, 2), round(cur * H / SR, 2)))
            cur = 0
    if cur * H / SR > 0.5: runs.append((round(st, 2), round(cur * H / SR, 2)))
    return hf_ns, runs
a = report(sys.argv[1]); b = report(sys.argv[2])
print(f"HF 5-14 kHz (non-speech, mean power): before {a[0]:.1f} dB  after {b[0]:.1f} dB  drop {a[0]-b[0]:.1f} dB")
print("flat-noise runs >0.5 s before:", len(a[1]), a[1][:8]); print("flat-noise runs >0.5 s after:", len(b[1]), b[1][:8])

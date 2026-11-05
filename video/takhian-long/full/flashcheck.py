"""V1b flash count from the real file: mean luma per frame (64x36), a flash = luma jumps >= 18 over the median of the previous 0.3 s
and stays >= 10 over it for <= 0.4 s. Reports every flash and the worst 10 s window. usage: flashcheck.py <video>"""
import subprocess, sys, numpy as np
v = sys.argv[1]
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", v, "-vf", "scale=64:36,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
y = np.frombuffer(raw, np.uint8).reshape(-1, 36 * 64).mean(1); fps = 60; n = len(y)
ev = []; i = 18
while i < n:
    base = np.median(y[max(0, i - 18):i])
    if y[i] - base >= 18:
        j = i
        while j < n and y[j] - base >= 10 and j - i < 60: j += 1
        if j - i <= 24: ev.append((i / fps, float(y[i] - base)))
        i = j + 6
    else: i += 1
ts = np.array([e[0] for e in ev]); worst = max((int(((ts >= t) & (ts < t + 10)).sum()), t) for t in np.arange(0, n / fps, 0.5)) if len(ts) else (0, 0)
print(f"{len(ev)} flashes · worst 10 s window {worst[0]} (from {worst[1]:.1f} s)")
for t, d in ev: print(f"  {t:7.2f}s +{d:.0f}")

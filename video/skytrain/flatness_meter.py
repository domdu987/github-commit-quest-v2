"""Coordinator's no-hiss meter: 0.5 s windows, per-frame (2048) magnitude spectral flatness over 5–14 kHz, median per window.
Reports the median, % noise windows (> TH), the quiet-window hi/lo ratio and noise runs > 1.5 s."""
import sys, subprocess, numpy as np
SR = 48000; TH = float(sys.argv[2]) if len(sys.argv) > 2 else 0.55; NF = 2048
x = np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"]), np.float32)
W = SR // 2; n = len(x) // W; f = np.fft.rfftfreq(NF, 1 / SR); b = (f >= 5000) & (f <= 14000); lo = (f >= 100) & (f < 2000)
fl = np.zeros(n); hl = np.zeros(n); lvl = np.zeros(n)
for i in range(n):
    s = x[i * W:(i + 1) * W]; lvl[i] = 10 * np.log10(np.mean(s ** 2) + 1e-20)
    fr = np.lib.stride_tricks.sliding_window_view(s, NF)[::NF // 2] * np.hanning(NF); X = np.abs(np.fft.rfft(fr, axis=1)) + 1e-12
    Xb = X[:, b]; fl[i] = np.median(np.exp(np.log(Xb).mean(1)) / Xb.mean(1)); hl[i] = 10 * np.log10((Xb ** 2).sum() / ((X[:, lo] ** 2).sum() + 1e-20))
act = lvl > -70; noisy = (fl > TH) & act
runs = []; i = 0
while i < n:
    if noisy[i]:
        j = i
        while j < n and noisy[j]: j += 1
        if (j - i) * 0.5 > 1.5: runs.append((i * 0.5, j * 0.5))
        i = j
    else: i += 1
q = act & (lvl < np.percentile(lvl[act], 25))
print(f"{sys.argv[1].split('/')[-1]}: flatness median {np.median(fl[act]):.2f} · noise windows {100 * noisy.sum() / max(1, act.sum()):.0f}% · quiet hi/lo {np.median(hl[q]):.1f} dB · runs>1.5s {runs}")

"""p03 "โอ๊ย! ขาผม!" has no usable TTS take (lane B BUDGET: CER 0.60–0.75), so ภูมิ's cry is a synthesized 11-year-old's pain scream:
a sharp "โอ๊ย!" (o→i glide, pitch jumping up then breaking) and a long wailing "อ๊าา…" with a sob in it, source-filter (harmonics shaped by
vowel formants), soft breath on top. Writes kidscream.wav (48 kHz mono) — length matches the p03 slot (2.175 s)."""
import numpy as np, subprocess, sys
SR = 48000
rng = np.random.default_rng(11)
def burst(d, f0f, F1f, F2f, amp):
    t = np.arange(int(d * SR)) / SR
    f0 = f0f(t); ph = 2 * np.pi * np.cumsum(f0) / SR
    F1, F2 = F1f(t), F2f(t)
    x = np.zeros_like(t)
    for k in range(1, 26):
        fk = k * f0
        a = np.exp(-((fk - F1) ** 2) / (2 * 140 ** 2)) + 0.6 * np.exp(-((fk - F2) ** 2) / (2 * 220 ** 2)) + 0.12 * np.exp(-((fk - 3000) ** 2) / (2 * 400 ** 2))
        x += a * np.sin(k * ph + rng.uniform(0, 6.28)) * (fk < 9000)
    br = rng.standard_normal(len(t)); br = np.convolve(br, np.ones(6) / 6, "same") * 0.05
    return (x / 6 + br) * amp(t)
o = lambda d: (lambda t: np.clip(t / 0.03, 0, 1) * np.clip((d - t) / 0.08, 0, 1))
d1 = 0.62   # "โอ๊ย!": jumps 520 → 880 Hz, cracks, falls; vowel o → i
b1 = burst(d1, lambda t: 520 + 360 * np.clip(t / 0.12, 0, 1) - 260 * np.clip((t - 0.3) / 0.3, 0, 1) + 25 * np.sin(2 * np.pi * 9 * t) + 60 * (np.abs(np.sin(2 * np.pi * 3 * t)) > 0.97),
           lambda t: 520 - 200 * np.clip((t - 0.25) / 0.3, 0, 1), lambda t: 900 + 1400 * np.clip((t - 0.25) / 0.3, 0, 1), o(d1))
d2 = 1.45   # the wail: "อ๊าาา…" 820 Hz with vibrato, a sob dip at 0.55 s, trailing off
sob = lambda t: 1 - 0.75 * np.exp(-((t - 0.55) ** 2) / (2 * 0.04 ** 2))
b2 = burst(d2, lambda t: 760 + 120 * np.exp(-t * 3) - 140 * np.clip((t - 0.9) / 0.55, 0, 1) + 30 * np.sin(2 * np.pi * 7 * t),
           lambda t: 880 + 0 * t, lambda t: 1350 + 0 * t, lambda t: o(d2)(t) * sob(t) * np.exp(-np.clip(t - 0.8, 0, None) * 1.6))
x = np.zeros(int(2.175 * SR)); x[:len(b1)] += b1; i = int(0.78 * SR); x[i:i + len(b2)] += b2[: len(x) - i]
x = x / np.max(np.abs(x)) * 0.8
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f64le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", "highpass=f=180,lowpass=f=7000", sys.argv[1]], input=x.tobytes(), check=True)

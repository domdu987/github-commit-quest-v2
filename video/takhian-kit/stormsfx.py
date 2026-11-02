"""StormFX sounds (lane C): event sounds only, every one with a clear pitch — no rain-noise bed (SKILL A4, owner: no hiss).
usage: python3 stormsfx.py out.wav total_s  far:0.63  strike:2.15  ground:2.18  chips:2.16  thud:3.19  [plinks=1]
  far:t     distant thunder: a low rolling rumble that starts ~0.8 s after the flash at t
  strike:t  the return stroke at t: a sharp descending crack, a deep boom, then ~4 s of rolling thunder
  ground:t  the current over the wet field: a short 100 Hz buzz with harmonics that crackles off
  thud:t    a branch hitting the mud · chips:t a few dry wooden ticks after the hit
  plinks=1  sparse tonal raindrops (under 3 kHz) over the whole clip
Times are the StormFX return-stroke times (StormFX.bolt(...).tR). Output is normalised to −16 LUFS, peaks ≤ −2 dBTP,
ready to sit under a voice mix (duck it there).
"""
import subprocess
import sys

import numpy as np

SR = 48000


def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)


def tone(f0, f1, dur, d, a=0.002):
    n = int(dur * SR)
    f = f0 * (f1 / f0) ** (np.arange(n) / SR / dur)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, a, d)


def rumble(dur, seed, lo=34, hi=130, k=14):
    """rolling thunder as a cluster of low sines, each swelling and fading on its own — pitched, not noise"""
    r = np.random.default_rng(seed)
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for _ in range(k):
        am = 0.5 + 0.5 * np.sin(2 * np.pi * r.uniform(1.5, 6) * t + r.uniform(0, 6.28))
        out += np.sin(2 * np.pi * r.uniform(lo, hi) * t + r.uniform(0, 6.28)) * am ** 2 * r.uniform(0.4, 1)
    return out / k * np.minimum(1, t / 0.35) * np.exp(-t / (dur * 0.45))


def crack():
    """the strike: six fast descending chirps on top of each other, then a deep boom"""
    out = np.zeros(int(0.5 * SR))
    for i, (f0, f1) in enumerate([(2800, 420), (2300, 360), (1900, 300), (1500, 240), (3200, 520), (1200, 200)]):
        x = tone(f0, f1, 0.09, 0.03) * (1 - i * 0.1)
        j = int(i * 0.006 * SR)
        out[j:j + len(x)] += x
    boom = tone(70, 42, 0.5, 0.22, 0.004) * 1.6
    out[: len(boom)] += boom
    hi = tone(110, 60, 0.4, 0.12, 0.003) * 0.8
    out[: len(hi)] += hi
    return out


def place(buf, x, t, g):
    i = int(t * SR)
    j = min(len(buf), i + len(x))
    if 0 <= i < len(buf):
        buf[i:j] += x[: j - i] * g


def main():
    out, total = sys.argv[1], float(sys.argv[2])
    buf = np.zeros(int(total * SR))
    plinks = False
    for a in sys.argv[3:]:
        if a.startswith("plinks"):
            plinks = True
            continue
        k, t = a.split(":")
        t = float(t)
        if k == "far":
            place(buf, rumble(3.0, 3, 30, 90, 10), t + 0.8, 0.5)
        elif k == "strike":
            place(buf, crack(), t, 0.9)
            place(buf, rumble(4.5, 7), t + 0.15, 1.1)
        elif k == "ground":
            n = int(0.35 * SR)
            tt = np.arange(n) / SR
            bz = sum(np.sin(2 * np.pi * 100 * h * tt) / h for h in (1, 2, 3, 5, 7)) * env(n, 0.003, 0.09)
            place(buf, bz * (0.6 + 0.4 * (np.sin(2 * np.pi * 37 * tt) > 0)), t, 0.35)
        elif k == "thud":
            place(buf, tone(95, 50, 0.35, 0.09), t, 0.7)
            place(buf, tone(220, 140, 0.12, 0.04), t + 0.01, 0.25)
        elif k == "chips":
            r = np.random.default_rng(11)
            for i in range(7):
                place(buf, tone(r.uniform(900, 1700), r.uniform(600, 900), 0.03, 0.008), t + 0.1 + i * r.uniform(0.06, 0.14), 0.12)
    if plinks:
        r = np.random.default_rng(5)
        for _ in range(int(total * 7)):
            place(buf, tone(r.uniform(1300, 2800), r.uniform(900, 1600), 0.04, 0.012), r.uniform(0, total), r.uniform(0.02, 0.05))
    raw = out.replace(".wav", "_raw.wav")
    pk = np.max(np.abs(buf)) + 1e-9
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", raw],
                   input=(buf / pk * 0.9).astype(np.float32).tobytes(), check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", "loudnorm=I=-16:TP=-2:LRA=11", "-ar", "48000", out], check=True)
    print("wrote", out)


if __name__ == "__main__":
    main()

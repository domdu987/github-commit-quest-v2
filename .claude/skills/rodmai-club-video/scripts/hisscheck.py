#!/usr/bin/env python3
"""Hiss / noise-bed check for rule A4 ("ไม่มีเสียงซ่า"). Run on the final HQ file or on mix.wav before delivery.

    python3 -I hisscheck.py <file> [<file> ...] [--vo vo_stem.wav]

With --vo (one file only) the pauses are taken from the voice stem, so a mix with continuous audible
music (rule A5) still has pauses to measure. Without it the pauses are frames where the mix's voice
band is quiet; if there are too few, test 2 reports n/a instead of failing (never add silence to pass).

Two tests, both must pass:
  1. Flatness: split the file into 0.5 s windows and keep the ones whose 5-14 kHz band is audible
     (> -80 dBFS; digital silence reads as "flat" but is not hiss). The median spectral flatness of
     that band must be <= 0.40. Noise beds (surf, rain, wind, fire loop, crowd, room tone, noise-made
     rotor) push it to 0.6-0.7; clean mixes sit at 0.28-0.39.
  2. Pause floor: in 50 ms frames with no voice (from --vo, else the mix's 300-3400 Hz band < -40 dBFS)
     the noise-like 5-14 kHz level (frames with flatness <= 0.5 are tonal music and count as silence)
     must have a median <= -65 dBFS. A bed keeps sounding between words; music and speech do not count.
Do not add music or tones to pass test 1: fix the mix (cut the beds, low-pass the FX bus ~4.5 kHz).

Calibrated 2 Nov 2569:
  pass  plane EP.1 v6 (0.32, -80), plane EP.2 v6b (0.39, -77), war v2 (0.32/0.30, -84/-82), skytrain v3 (0.29/0.30, -68/-70)
  fail  old war EP.1 (0.64, -48), old skytrain EP.1 (0.68, -58), old exam EP.1 (0.70, -74)
"""
import subprocess
import sys

import numpy as np

SR = 48000


def load(path):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, np.float32)


def band(x, lo, hi):
    spec = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    spec[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(spec, len(x))


def db(x):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)


def flatness(seg):
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) + 1e-12
    f = np.fft.rfftfreq(len(seg), 1 / SR)
    b = (f > 5000) & (f < 14000)
    return np.exp(np.mean(np.log(spec[b]))) / np.mean(spec[b])


def check(path, vo_path=None):
    x = load(path)
    hf = band(x, 5000, 14000)
    voice = load(vo_path) if vo_path else band(x, 300, 3400)
    if len(voice) < len(x):
        voice = np.pad(voice, (0, len(x) - len(voice)))
    gate = -50 if vo_path else -40
    n = int(0.5 * SR)
    flats = [flatness(x[i:i + n]) for i in range(0, len(x) - n, n) if db(hf[i:i + n]) > -80]
    flat = float(np.median(flats)) if flats else 0.0
    n = int(0.05 * SR)
    # noise-like frames keep their 5-14 kHz level; tonal ones (music sparkle under rule A5) count as silence
    pause_hf = [db(hf[i:i + n]) if flatness(x[i:i + n]) > 0.5 else -120.0
                for i in range(0, len(x) - n, n) if db(voice[i:i + n]) < gate]
    ok1 = flat <= 0.40
    if len(pause_hf) < 10:
        return (f"{path}: flatness {flat:.2f} ({'ok' if ok1 else 'HISS'}) · pause HF n/a (too few pauses; "
                f"pass --vo vo_stem.wav) → {'PASS' if ok1 else 'FAIL'}"), ok1
    floor = float(np.median(pause_hf))
    ok2 = floor <= -65
    ok = ok1 and ok2
    return (f"{path}: flatness {flat:.2f} ({'ok' if ok1 else 'HISS'}) · pause HF median {floor:.1f} dBFS "
            f"({'ok' if ok2 else 'BED'}) → {'PASS' if ok else 'FAIL'}"), ok


if __name__ == "__main__":
    args, vo = sys.argv[1:], None
    if "--vo" in args:
        i = args.index("--vo")
        vo = args[i + 1]
        args = args[:i] + args[i + 2:]
    all_ok = True
    for p in args:
        line, ok = check(p, vo)
        all_ok &= ok
        print(line)
    sys.exit(0 if all_ok else 1)

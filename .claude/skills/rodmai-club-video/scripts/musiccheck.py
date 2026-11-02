#!/usr/bin/env python3
"""Is the theme music actually audible? (rule A5; owner 2 Nov 2569: "เพลงเบาไม่ได้ยินเหมือนไม่ได้ใส่")

    python3 -I musiccheck.py <vo_stem.wav> <music_stem.wav>

Both stems must be exactly what is summed into the final mix: after every gain, dip, duck and low-pass,
and after the final loudness-normalisation gain (the delivered file is -14 LUFS integrated).
Loudness is EBU R128 momentary (400 ms) from ffmpeg's ebur128 filter, on a 100 ms grid.

Targets (all must pass):
  1. music under the voice (voice momentary > -35 LUFS): median -27 .. -22 LUFS
  2. music between lines (voice < -50 LUFS for >= 1 s, else >= 0.5 s; n/a if the narration never pauses): median -22 .. -17 LUFS
  3. voice stays clear: median (voice - music) while speaking >= 8 LU
  4. music not missing: in voice-free time, music below -40 LUFS for <= 15 % (planned hush beats only)
Old mixes (theme at -30/-33 with an 0.65-0.8 duck and a gate) sit around -45 under the voice and -30 between
lines, which the owner heard as no music at all.

Every target is checked twice: on the full band, and again on the "phone speaker" band (both stems high-passed
at 300 Hz, 24 dB/oct). Both passes must hold. Owner 2 Nov 2569 ~19:15: "เพลงหาย ไม่ได้ยินเลย". Every theme
then had 78-97 % of its energy below 300 Hz, because the music prompt asked to "keep the midrange sparse".
Full band passed, but on a phone the music sat 22-24 dB under the voice.
"""
import re
import subprocess
import sys

import numpy as np


PHONE = "highpass=f=300,highpass=f=300,"   # small phone speakers reproduce almost nothing below ~300 Hz


def momentary(path, pre=""):
    cmd = ["ffmpeg", "-nostats", "-i", path, "-af",
           pre + "ebur128=metadata=1,ametadata=mode=print:key=lavfi.r128.M:file=-", "-f", "null", "-"]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    t, m, cur = [], [], None
    for line in out.splitlines():
        a = re.search(r"pts_time:([0-9.]+)", line)
        if a:
            cur = float(a.group(1))
            continue
        b = re.search(r"lavfi\.r128\.M=(-?inf|-?nan|-?[0-9.]+)", line)
        if b and cur is not None:   # digital silence reads as -inf or nan: count it as -120
            v = b.group(1)
            t.append(cur)
            m.append(-120.0 if ("inf" in v or "nan" in v) else float(v))
    t, m = np.array(t), np.array(m)
    grid = np.arange(0, t.max() if len(t) else 0, 0.1)
    return grid, np.interp(grid, t, m) if len(t) else np.array([])


def runs(mask, min_len):
    out, start = np.zeros_like(mask), None
    for i, v in enumerate(list(mask) + [False]):
        if v and start is None:
            start = i
        if not v and start is not None:
            if i - start >= min_len:
                out[start:i] = True
            start = None
    return out


def check(vo_path, mus_path, pre=""):
    g1, vo = momentary(vo_path, pre)
    g2, mu = momentary(mus_path, pre)
    n = min(len(vo), len(mu))
    vo, mu = vo[:n], mu[:n]
    speaking = vo > -35
    free = runs(vo < -50, 10)          # gaps between lines of >= 1 s
    if not free.any():
        free = runs(vo < -50, 5)       # narration with no 1 s gaps: fall back to >= 0.5 s
    under = float(np.median(mu[speaking])) if speaking.any() else float("nan")
    between = float(np.median(mu[free])) if free.any() else float("nan")
    margin = float(np.median((vo - mu)[speaking])) if speaking.any() else float("nan")
    missing = float(np.mean(mu[free] < -40) * 100) if free.any() else 0.0
    gap_line = (f"music between lines {between:.1f} LUFS (target -22..-17)", -22 <= between <= -17) if free.any() else \
        ("music between lines: n/a (no voice gap of 0.5 s or more; the narration runs end to end)", True)
    checks = [
        (f"music under the voice {under:.1f} LUFS (target -27..-22)", -27 <= under <= -22),
        gap_line,
        (f"voice over music {margin:.1f} LU (target >= 8)", margin >= 8),
        (f"music missing in voice-free time {missing:.0f}% (target <= 15%)", missing <= 15),
    ]
    ok = all(c[1] for c in checks)
    for text, good in checks:
        print(("ok   " if good else "FAIL ") + text)
    return ok


def main(vo_path, mus_path):
    print("[full band]")
    a = check(vo_path, mus_path)
    print("[phone speaker band: both stems high-passed at 300 Hz]")
    b = check(vo_path, mus_path, PHONE)
    if not b:
        print("  -> the theme lives below 300 Hz: regenerate it with a mid-register lead melody (scripts/gen_theme.py)")
    ok = a and b
    print("PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(0 if main(sys.argv[1], sys.argv[2]) else 1)

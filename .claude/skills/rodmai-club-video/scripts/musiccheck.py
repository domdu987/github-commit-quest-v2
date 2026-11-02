#!/usr/bin/env python3
"""Does the music sit like ทะเลลด? (rule A5; owner 2 Nov 2569 ~21:00: "เอาซาวเพลงแบบทะเลลด ใช้ทุกคลิปเลย")

    python3 -I musiccheck.py <vo_stem.wav> <music_stem.wav>

Every story now uses video/music/suno1.mp3 with the ทะเลลด mix recipe (video/tide-ep1/production/mix.py):
  suno1 from 0 s, no EQ / low-pass / high-pass / compressor on it · horror dips (x0.4-0.55) on the scary beats
  level -30 dB RMS (samples above 1e-4, after the dips) · voice lines -18 dB RMS each · SFX -27
  duck 0.65: 50 ms envelope of |voice| / its median, clipped 0..1, smoothed 0.25 s · final -14 LUFS integrated
  cliffhanger: hard cut to silence on the choice · finale: fade over the end card

Both stems must be exactly what is summed into the final mix (after every gain, dip and duck, and after the final
loudness gain). Loudness is EBU R128 momentary (400 ms) from ffmpeg's ebur128 filter, on a 100 ms grid.

Targets = ทะเลลด EP.1 as delivered (stems rebuilt from its mix.py, measured 2 Nov) +- 3 LU:
  1. music under the voice (voice momentary > -35 LUFS): median -36.6 .. -30.6 LUFS   (ทะเลลด -33.6)
  2. music between lines (voice < -50 LUFS for >= 1 s, else >= 0.5 s; n/a if none): median -34.5 .. -28 LUFS (ทะเลลด -31.3)
  3. voice stays clear: median (voice - music) while speaking >= 8 LU                  (ทะเลลด 18.9)
  4. music not missing: in voice-free time, music below -40 LUFS for <= 15 %           (ทะเลลด 12 %)
The phone-speaker band (both stems high-passed at 300 Hz) is printed for information only: ทะเลลด itself reads
-39.0 under the voice and -35.4 between lines there, and the owner chose ทะเลลด as the sound for every clip.
History: 2 Nov ~19:15 the owner said "เพลงหาย ไม่ได้ยินเลย" about bass-heavy per-story themes; louder targets and new
themes followed (gen_theme.py); at ~20:45 and ~21:00 the owner overrode that: suno1 and the ทะเลลด sound everywhere.
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
    gap_line = (f"music between lines {between:.1f} LUFS (ทะเลลด -31.3; target -34.5..-28)", -34.5 <= between <= -28) if free.any() else \
        ("music between lines: n/a (no voice gap of 0.5 s or more; the narration runs end to end)", True)
    checks = [
        (f"music under the voice {under:.1f} LUFS (ทะเลลด -33.6; target -36.6..-30.6)", -36.6 <= under <= -30.6),
        gap_line,
        (f"voice over music {margin:.1f} LU (ทะเลลด 18.9; target >= 8)", margin >= 8),
        (f"music missing in voice-free time {missing:.0f}% (ทะเลลด 12%; target <= 15%)", missing <= 15),
    ]
    if pre:   # phone band: information only
        for text, _ in checks:
            print("info " + text.split(" (")[0])
        return True
    ok = all(c[1] for c in checks)
    for text, good in checks:
        print(("ok   " if good else "FAIL ") + text)
    return ok


def main(vo_path, mus_path):
    print("[full band]")
    ok = check(vo_path, mus_path)
    print("[phone speaker band, info only: both stems high-passed at 300 Hz; ทะเลลด reads -39.0 under the voice, -35.4 between lines]")
    check(vo_path, mus_path, PHONE)
    print("PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(0 if main(sys.argv[1], sys.argv[2]) else 1)

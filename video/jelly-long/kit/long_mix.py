"""หนวดใส คลิปยาว: the long soundtrack = the five part mixes cut at the same frame boundaries as the picture (60 fps), joined with
40 ms equal-power crossfades at each join, then one static gain to -14 LUFS (soft knee as the episode mixes). Prints the part table
(frames, start, end) that concat_long.sh trims the picture with, and writes long-parts.json.
usage: python3 long_mix.py <out dir>"""
import json
import os
import re
import subprocess
import sys

import numpy as np

J = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(J, "long")
os.makedirs(OUT, exist_ok=True)
SR, FPS = 48000, 60
# (name, mix, picture project, first frame, frame count) — frames of each part's own 60 fps render
PARTS = [
    ("cold", "brc/mix.wav", "Lbr", 964, 2045 - 964),      # bridges 16.067 … 34.083 (C1–C4: thirty years ago) → black
    ("title", "endc/mix.wav", "Lend", 0, 180),            # "หนวดใส ฉบับเต็ม" 3 s
    ("ep1", "ep1c/mix.wav", "L1", 0, 6174),               # 0 … 102.900 (cut 29, the vote, starts at 102.90)
    ("bridgeA", "brc/mix.wav", "Lbr", 0, 497),            # 0 … 8.283 (B1 starts at 8.284)
    ("ep2", "ep2c/mix.wav", "L2", 476, 4803 - 476),       # 7.933 … 80.050 (stay … the vote at 80.06)
    ("bridgeB", "brc/mix.wav", "Lbr", 497, 964 - 497),    # 8.283 … 16.067 ("นั่นมัน… พ่อผม")
    ("ep3a", "ep3c/mix.wav", "L3", 0, 2963),              # EP.3 0 … 49.383 (to y05 "แล้วเขาก็ไม่ได้กลับบ้านอีกเลย")
    ("secret", "fbc/mix.wav", "Lfb", 0, 2534),            # the full secret (lane B fb_* + hush), 42.233 s
    ("ep3b", "ep3c/mix.wav", "L3", 2963, 5357 - 2963),    # EP.3 49.383 … 89.283 (the twist … dawn; EP.3's own end board dropped)
    ("epi", "brc/mix.wav", "Lbr", 2045, 3267 - 2045),     # bridges 34.083 … 54.450 (E1–E3: a year later)
    ("credits", "endc/mix.wav", "Lend", 180, 300),        # 3 … 8: the sea held 5 s, then silence
    ("card", "endc/mix.wav", "Lend", 480, 480),           # 8 … 16: เรื่องต่อไป · ติดตาม · นาทีก่อนจม ฉบับเต็ม
]
XF = int(0.04 * SR)


def load(path):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, dtype=np.float32).copy()


def wr(path, x):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", "-c:a", "pcm_s16le", path], input=x.astype(np.float32).tobytes(), check=True)


def integrated(path):
    out = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", out)[-1])


segs, table, t = [], [], 0.0
for name, mix, proj, f0, nf in PARTS:
    x = load(os.path.join(J, mix)); a = f0 * SR // FPS; n = nf * SR // FPS
    seg = x[a:a + n]; seg = np.pad(seg, (0, n - len(seg)))
    segs.append(seg); table.append({"part": name, "proj": proj, "frame0": f0, "frames": nf, "start": round(t, 4), "end": round(t + nf / FPS, 4)}); t += nf / FPS
out = segs[0].copy()
r = np.sin(np.linspace(0, np.pi / 2, XF, dtype=np.float32))
for s in segs[1:]:
    # equal-power join: the last 40 ms of the outgoing part fades under the first 40 ms of the next (the total stays frame-exact
    # because the overlap is given back by padding the end)
    out[-XF:] = out[-XF:] * r[::-1] + s[:XF] * r
    out = np.concatenate([out, s[XF:]])
total = sum(p["frames"] for p in table) / FPS
out = np.pad(out, (0, max(0, int(round(total * SR)) - len(out))))[: int(round(total * SR))]
knee = lambda y: np.where(np.abs(y) > 0.6, np.sign(y) * (0.6 + 0.19 * np.tanh((np.abs(y) - 0.6) / 0.19)), y).astype(np.float32)
tmp = os.path.join(OUT, "long_raw.wav"); g = 1.0
for _ in range(3):
    wr(tmp, knee(out * g)); g *= 10 ** ((-14.0 - integrated(tmp)) / 20)
os.remove(tmp)
wr(os.path.join(OUT, "long-mix.wav"), knee(out * g))
json.dump({"fps": FPS, "total": round(total, 4), "parts": table}, open(os.path.join(OUT, "long-parts.json"), "w"), indent=1)
for p in table: print(p)
print("total", round(total, 3), "gain", round(20 * np.log10(g), 2))

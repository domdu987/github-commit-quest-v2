"""Rebuild brand/signature.wav with a clearer "ถูกทาง".

In the first take the narrator swallows the final ง, so "ถูกทาง" is heard as "ถูกทาก" (leech).
This keeps that take (signature-v1.wav, the trimmed s01 at tempo 1.05) and swaps only its second
phrase for s01-tang.mp3, a take of "ถูกทาง…" that holds the ง (a nasal can be held, a final ก cannot).
The new phrase starts where the old one did, so the caption fragments and the checklist ticks timed
from schedule.json still line up and no episode has to be re-rendered.
Usage: python3 splice_signature.py   (then copy signature.wav to each episode's production/vo/s01.wav)
"""
import os
import subprocess

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 44100


def load(path, af=None):
    cmd = ["ffmpeg", "-v", "error", "-i", path] + (["-af", af] if af else []) + ["-f", "f32le", "-ac", "2", "-ar", str(SR), "-"]
    return np.frombuffer(subprocess.check_output(cmd), np.float32).reshape(-1, 2).copy()


def phrases(x, gap=0.25):
    """Voiced stretches (20 ms frames above -35 dB of the loudest) separated by pauses longer than gap
    (0.25 s keeps the short stop inside "ถูกทาง" in one phrase)."""
    hop = int(0.02 * SR)
    e = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)])
    on = 20 * np.log10(e + 1e-9) > 20 * np.log10(e.max()) - 35
    idx = np.where(on)[0]
    groups = np.split(idx, np.where(np.diff(idx) > gap / 0.02)[0] + 1)
    return [(g[0] * hop, (g[-1] + 1) * hop) for g in groups if len(g) > 2]


old = load(os.path.join(HERE, "signature-v1.wav"))
ph = phrases(old)
assert len(ph) == 4, ph  # ทุกอย่าง / ถูกทาง / พลาดแค่ / เรื่องเดียว
trim = ("silenceremove=start_periods=1:start_threshold=-40dB,areverse,"
        "silenceremove=start_periods=1:start_threshold=-40dB,areverse,atempo=1.08")  # about the tempo of the rest of the line
new = load(os.path.join(HERE, "s01-tang.mp3"), trim)
a, b = ph[1]
start = a - int(0.10 * SR)  # 100 ms early, so the held ง still leaves a pause before "พลาดแค่"
slot = ph[2][0] - start - int(0.22 * SR)
assert len(new) <= slot, (len(new) / SR, slot / SR)
rms = lambda v: np.sqrt(np.mean(v[np.abs(v) > 1e-3] ** 2))
new *= rms(old[a:b]) / rms(new)
fade = int(0.008 * SR)
new[:fade] *= np.linspace(0, 1, fade)[:, None]
new[-fade:] *= np.linspace(1, 0, fade)[:, None]
out = old.copy()
out[start:ph[2][0]] = 0
out[start:start + len(new)] = new
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s16le",
                os.path.join(HERE, "signature.wav")], input=out.astype(np.float32).tobytes(), check=True)
print("phrases (s):", [(round(p / SR, 2), round(q / SR, 2)) for p, q in ph], "new phrase:", round(start / SR, 2), "+", round(len(new) / SR, 2), "s")

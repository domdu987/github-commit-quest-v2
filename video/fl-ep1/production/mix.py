"""ช่างเชื่อมสายฟ้า EP.1: the soundtrack from schedule.json: levelled narrator, synthesized SFX and the owner's Suno bed
(quest through the alley, tension from the storm to the strike and under the blackout, quest again for the comedy and the end card). Output about -14 LUFS."""
import json
import os
import subprocess

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
SC = json.load(open(os.path.join(HERE, "schedule.json")))
SH = {s["key"]: s for s in SC["shots"]}
TOTAL = SC["total"]
N = int(TOTAL * SR)


def load(path):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, dtype=np.float32).copy()


def place(buf, x, t, g=1.0):
    i = int(t * SR)
    j = min(len(buf), i + len(x))
    if i < len(buf):
        buf[i:j] += x[: j - i] * g


def rms_db(x):
    x = x[np.abs(x) > 1e-4]
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)


def level(x, target):
    return x * 10 ** ((target - rms_db(x)) / 20)


def box(x, n):
    c = np.concatenate([[0.0], np.cumsum(x, dtype=np.float64)])
    i = np.arange(len(x))
    lo, hi = np.clip(i - n // 2, 0, len(x)), np.clip(i - n // 2 + n, 0, len(x))
    return ((c[hi] - c[lo]) / n).astype(np.float32)


def T(k, t):
    s = SH[k]
    return s["start"] + (t if t >= 0 else s["dur"] + t)


def vo_t(k, i=0):
    return SH[k]["vo"][i]["t"]


def vo_end(k, i=0):
    return SH[k]["vo"][i]["t"] + SH[k]["vo"][i]["dur"]


def F(k, i=0, j=0):
    v = SH[k]["vo"][i]
    return v["t"] + v["frags"][min(j, len(v["frags"]) - 1)]


D = {k: SH[k]['dur'] for k in SH}
# ---- voice ----
vo = np.zeros(N, np.float32)
for s in SC["shots"]:
    for v in s["vo"]:
        x = load(os.path.join(HERE, "vo", f"{v['id']}.wav"))
        place(vo, level(x, -18), s["start"] + v["t"])

# ---- SFX cues (times follow the picture in body.part) ----
CUES = [
    ("f01", 0.3, "whoosh", 0.1), ("f01", 1.2, "whoosh", 0.09), ("f01", 2.0, "whoosh", 0.08), ("f01", F("f01", 0, 1), "swell", 0.07),
    ("f02", F("f02", 0, 1), "ding", 0.07), ("f02", 1.0, "whoosh", 0.1), ("f02", 1.5, "whoosh", 0.1), ("f02", 2.1, "whoosh", 0.1), ("f02", F("f02", 0, 1) + 0.1, "pop", 0.1),
    ("f03", F("f03", 0, 1), "pop", 0.1), ("f03", F("f03", 0, 1) + 0.4, "thud", 0.08), ("f03", F("f03", 0, 2), "whoosh", 0.16), ("f03", F("f03", 0, 2), "swell", 0.08),
    ("f04", F("f04", 0, 1), "whoosh", 0.12), ("f04", F("f04", 0, 1) + 0.6, "thud", 0.22), ("f04", F("f04", 0, 1) + 0.9, "pop", 0.1),
    ("f05", 0.1, "pop", 0.1), ("f05", F("f05", 0, 1) - 0.1, "beep", 0.06), ("f05", F("f05", 0, 1), "buzz", 0.08),
    ("f06", F("f06", 0, 1) - 0.05, "crackle", 0.14), ("f06", F("f06", 0, 1) + 0.5, "clang", 0.1), ("f06", F("f06", 0, 1) + 1.3, "clang", 0.1), ("f06", F("f06", 0, 1) + 2.1, "clang", 0.1), ("f06", F("f06", 0, 2), "pop", 0.1),
    ("f07", F("f07", 0, 1) - 0.2, "hiss", 0.12), ("f07", F("f07", 0, 1) + 1.2, "steps", 0.08),
    ("f08", 0.2, "steps", 0.06), ("f08", 0.2, "whoosh", 0.1), ("f08", 1.4, "whoosh", 0.1), ("f08", F("f08", 0, 1) - 0.3, "pop", 0.1), ("f08", F("f08", 0, 0) + 1.2, "tick", 0.07), ("f08", F("f08", 0, 0) + 2.0, "tick", 0.07),
    ("f09", F("f09", 0, 1) + 0.1, "pop", 0.1), ("f09", F("f09", 0, 1) + 0.5, "tick", 0.06), ("f09", F("f09", 0, 1) + 1.0, "tick", 0.06), ("f09", F("f09", 0, 1) + 1.5, "tick", 0.06), ("f09", F("f09", 0, 2) + 0.1, "snap", 0.12),
    ("f10", 0.05, "pop", 0.1), ("f10", F("f10", 0, 1), "tap", 0.1), ("f10", F("f10", 0, 1) + 0.2, "pop", 0.1),
    ("f11", F("f11", 0, 0) + 0.2, "ding", 0.07), ("f11", F("f11", 0, 1), "powerdown", 0.12), ("f11", F("f11", 0, 2) - 0.2, "pop", 0.1), ("f11", F("f11", 0, 2), "whoosh", 0.1), ("f11", F("f11", 0, 2) + 0.2, "whoosh", 0.1), ("f11", F("f11", 0, 2) + 0.4, "whoosh", 0.1),
    ("f12", F("f12", 0, 1), "zap", 0.16), ("f12", F("f12", 0, 1) + 0.1, "crackle", 0.1), ("f12", F("f12", 0, 1) + 0.3, "hiss", 0.1), ("f12", F("f12", 0, 2) + 0.2, "pop", 0.1),
    ("f13", 0.0, "static", 0.04), ("f13", F("f13", 0, 2), "swell", 0.08), ("f13", F("f13", 0, 2), "pop", 0.1), ("f13", F("f13", 0, 3) + 0.3, "pop", 0.14), ("f13", F("f13", 0, 3) + 0.75, "pop", 0.14), ("f13", F("f13", 0, 3) + 1.2, "pop", 0.14), ("f13", F("f13", 0, 3) + 1.9, "pop", 0.14),
    ("f14", 0.2, "hum", 0.06), ("f14", F("f14", 0, 2), "ding", 0.08), ("f14", F("f14", 0, 2) + 0.2, "pop", 0.1),
    ("f15", 0.0, "crickets", 0.05), ("f15", F("f15", 0, 2) - 0.6, "tick", 0.08), ("f15", F("f15", 0, 2) - 0.3, "tick", 0.08), ("f15", F("f15", 0, 2), "ding", 0.09),
    ("f16", 0.0, "whoosh", 0.12)
]
SECTIONS = [(0, T("f02", 0), "tension"), (T("f02", 0), T("f09", 0), "hope"), (T("f09", 0), T("f12", 0), "tension"), (T("f12", 0), T("f16", 0), "twist"),
            (T("f16", 0), T("f17", 0), "cta"), (T("f17", 0), TOTAL, "silence")]
cues = {"duration": TOTAL, "bpm": 108, "sections": [{"start": round(a, 3), "end": round(b, 3), "mood": m} for a, b, m in SECTIONS],
        "sfx": [{"t": round(T(k, t), 3), "type": typ, "gain": g} for k, t, typ, g in CUES]}
json.dump(cues, open(os.path.join(HERE, "sfx_cues.json"), "w"))
subprocess.run(["python3", os.path.join(HERE, "..", "..", "synth.py"), os.path.join(HERE, "sfx_cues.json"), os.path.join(HERE, "sfx.wav")],
               check=True, env={**os.environ, "STEMS": "1"})
sfx = load(os.path.join(HERE, "sfx_sfx.wav"))[:N]
sfx = np.pad(sfx, (0, N - len(sfx)))
import sys
sys.path.insert(0, os.path.join(HERE, ".."))
from musicbed import bed
mus = bed(N, SR, [(0, T("f09", 0), "quest"), (T("f09", 0), T("f16", 0), "tension"), (T("f16", 0), T("f17", 0), "quest")], load)   # the owner's Suno tracks

# ---- levels + ducking (the bed sits well under the voice) ----
mus = level(mus, -31)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.6 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mix = vo + mus * duck + sfx
peak = np.max(np.abs(mix))
if peak > 0.98:
    mix = np.tanh(mix / peak * 1.2) * 0.95
out = os.path.join(HERE, "mix_raw.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", out],
               input=mix.astype(np.float32).tobytes(), check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", "loudnorm=I=-13.3:TP=-2.2:LRA=11", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)
print("mix written", TOTAL)

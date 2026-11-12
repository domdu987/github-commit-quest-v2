"""สกิลจอมโกหก ภาค 2 ครึ่งหลัง: the soundtrack from schedule.json: levelled narrator, synthesized SFX and a light bed
(tension hook → calm Earth → hope in heaven → twist in town → cta → silence on the logo). Output about -14 LUFS."""
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
    return SH[k]["vo"][i]["t"] + SH[k]["vo"][i]["frags"][j]


D = {k: SH[k]['dur'] for k in SH}
# ---- voice ----
vo = np.zeros(N, np.float32)
for s in SC["shots"]:
    for v in s["vo"]:
        x = load(os.path.join(HERE, "vo", f"{v['id']}.wav"))
        place(vo, level(x, -18), s["start"] + v["t"])

# ---- SFX cues (times follow the picture in shotsB.part) · no hum/swell at the top, no wind, rain or sting ----
CUES = [
    ("b01", F("b01", 0, 2), "roar", 0.22), ("b01", F("b01", 0, 2), "quake", 0.08),
    ("b02", F("b02", 0, 0) + 1.0, "clang", 0.12), ("b02", F("b02", 0, 0) + 1.05, "ching", 0.08), ("b02", F("b02", 0, 2), "whoosh", 0.1),
    ("b04", F("b04", 0, 1), "rustle", 0.08), ("b04", F("b04", 0, 2) - 0.1, "whoosh", 0.1), ("b04", F("b04", 0, 3), "ding", 0.07),
    ("b05", 0.1, "whoosh", 0.12), ("b05", F("b05", 0, 1) - 0.05, "clang", 0.2), ("b05", F("b05", 0, 2), "ding", 0.07),
    ("b06", F("b06", 0, 2), "blinker", 0.14), ("b07", F("b07", 0, 3), "thud", 0.12), ("b07", F("b07", 0, 3) + 0.3, "splash", 0.08),
    ("b08", F("b08", 0, 2) + 0.3, "squish", 0.1), ("b09", F("b09", 0, 2), "ding", 0.08),
    ("b10", 0.0, "steps", 0.1), ("b10", F("b10", 0, 2), "ching", 0.08),
    ("b11", F("b11", 0, 1), "drum", 0.08), ("b12", 0.1, "riser", 0.08), ("b12", F("b12", 0, 2) - 0.1, "ching", 0.14),
    ("b13", F("b13", 0, 0) + 0.6, "roar", 0.18), ("b13", F("b13", 0, 0) + 0.6, "crackle", 0.2), ("b13", F("b13", 0, 2), "shatter", 0.06),
    ("b14", F("b14", 0, 1), "growl", 0.08), ("b15", F("b15", 0, 1), "pop", 0.08), ("b15", F("b15", 0, 2), "ching", 0.08),
    ("b16", 0.2, "marker", 0.12), ("b16", F("b16", 0, 1), "slam", 0.16), ("b17", F("b17", 0, 1), "ching", 0.12), ("b17", F("b17", 0, 1) + 0.1, "drum", 0.08),
    ("b18", F("b18", 0, 1), "ching", 0.1), ("b19", 0.0, "crickets", 0.06), ("b19", F("b19", 0, 1) + 0.2, "knock", 0.2), ("b19", F("b19", 0, 1) + 0.45, "knock", 0.2),
    ("b20", F("b20", 0, 0) + 0.5, "whoosh", 0.08), ("b20", F("b20", 0, 1), "ding", 0.06),
    ("b21", F("b21", 0, 1) - 0.3, "flap", 0.14), ("b21", F("b21", 0, 2), "roar", 0.1), ("b22", 0.0, "flap", 0.1), ("b22", F("b22", 0, 2), "drum", 0.1),
    ("b23", 0.0, "whoosh", 0.1),
]
BED = [(0, T("b11", 0), "tension"), (T("b11", 0), T("b19", 0), "quest"), (T("b19", 0), T("b21", 0), "musicbox"), (T("b21", 0), T("b24", 0), "tension")]
SECTIONS = [(0, T("b11", 0), "tension"), (T("b11", 0), T("b19", 0), "hope"), (T("b19", 0), T("b21", 0), "calm"), (T("b21", 0), T("b23", 0), "tension"), (T("b23", 0), T("b24", 0), "cta"), (T("b24", 0), TOTAL, "silence")]
cues = {"duration": TOTAL, "bpm": 104, "sections": [{"start": round(a, 3), "end": round(b, 3), "mood": m} for a, b, m in SECTIONS],
        "sfx": [{"t": round(T(k, t), 3), "type": typ, "gain": g} for k, t, typ, g in CUES]}
json.dump(cues, open(os.path.join(HERE, "sfx_cues.json"), "w"))
subprocess.run(["python3", os.path.join(HERE, "..", "..", "synth.py"), os.path.join(HERE, "sfx_cues.json"), os.path.join(HERE, "sfx.wav")],
               check=True, env={**os.environ, "STEMS": "1"})
sfx = load(os.path.join(HERE, "sfx_sfx.wav"))[:N]
sfx = np.pad(sfx, (0, N - len(sfx)))
import sys
sys.path.insert(0, os.path.join(HERE, ".."))
from musicbed import bed
mus = bed(N, SR, BED, load)

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

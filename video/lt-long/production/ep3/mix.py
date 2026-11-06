"""ช่างเชื่อมสายฟ้า EP.3: the soundtrack from schedule.json: levelled narrator, synthesized SFX and the owner's Suno bed
(tension from the storm to the overload, musicbox under the incubators, tension again as he rises). Output about -14 LUFS."""
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
    ("t01", 0.0, "rain", 0.08), ("t01", 0.4, "thunder", 0.12), ("t01", 0.0, "beep", 0.03), ("t01", 1.0, "beep", 0.03), ("t01", 2.0, "beep", 0.03), ("t01", F("t01", 0, 1) + 0.3, "pop", 0.1),
    ("t02", 0.0, "wind", 0.18), ("t02", 0.0, "rain", 0.12), ("t02", 0.8, "thunder", 0.2), ("t02", F("t02", 0, 0) + 1.6, "pop", 0.1),
    ("t03", 0.0, "rain", 0.1), ("t03", F("t03", 0, 1) - 1.1, "buzz", 0.12), ("t03", F("t03", 0, 1) - 0.3, "boom", 0.3), ("t03", F("t03", 0, 1) - 0.3, "shatter", 0.14), ("t03", F("t03", 0, 1) - 0.05, "powerdown", 0.22),
    ("t04", 0.0, "rain", 0.06), ("t04", F("t04", 0, 1) + 0.2, "thud", 0.16), ("t04", F("t04", 0, 1) + 0.3, "pop", 0.1),
    ("t05", 0.0, "beep", 0.03), ("t05", 0.9, "beep", 0.03), ("t05", 1.8, "beep", 0.03), ("t05", F("t05", 0, 1) + 0.2, "pop", 0.08), ("t05", F("t05", 0, 1) + 0.6, "pop", 0.08), ("t05", F("t05", 0, 1) + 1.0, "pop", 0.08),
    ("t06", 0.0, "rain", 0.12), ("t06", 0.1, "steps", 0.12), ("t06", F("t06", 0, 1) + 0.3, "snap", 0.1), ("t06", F("t06", 0, 3) - 0.3, "riser", 0.12), ("t06", F("t06", 0, 3), "zap", 0.24), ("t06", F("t06", 0, 3), "boom", 0.14), ("t06", F("t06", 0, 3) + 0.2, "crackle", 0.16),
    ("t07", 0.4, "notif", 0.1), ("t07", 1.1, "notif", 0.1), ("t07", 1.8, "notif", 0.1), ("t07", 0.4, "hum", 0.05),
    ("t08", 0.0, "crackle", 0.14), ("t08", 0.1, "riser", 0.1), ("t08", F("t08", 0, 1), "zap", 0.18), ("t08", F("t08", 0, 1) + 0.9, "ding", 0.08),
    ("t09", 0.0, "crackle", 0.12), ("t09", F("t09", 0, 1) - 0.2, "riser", 0.1), ("t09", F("t09", 0, 1), "boom", 0.2), ("t09", F("t09", 0, 1), "zap", 0.2), ("t09", F("t09", 0, 1) + 0.1, "swell", 0.1),
    ("t10", 0.3, "pop", 0.12), ("t10", 0.3, "ding", 0.08), ("t10", F("t10", 0, 1) + 0.2, "pop", 0.12), ("t10", F("t10", 0, 1) + 0.2, "gong", 0.08), ("t10", F("t10", 0, 2) + 0.2, "pop", 0.14), ("t10", F("t10", 0, 2) + 0.2, "swell", 0.1),
    ("t11", 0.0, "hum", 0.08), ("t11", F("t11", 0, 1), "riser", 0.1), ("t11", F("t11", 0, 1) + 0.5, "swell", 0.08),
    ("t12", 0.0, "hum", 0.08), ("t12", F("t12", 0, 1) + 0.2, "pop", 0.1), ("t12", F("t12", 0, 1) + 0.2, "alarm", 0.06),
    ("t13", 0.0, "whoosh", 0.12),
]
SECTIONS = [(0, T("t02", 0), "tension"), (T("t02", 0), T("t07", 0), "tension"), (T("t07", 0), T("t08", 0), "hope"), (T("t08", 0), T("t13", 0), "twist"),
            (T("t13", 0), T("t14", 0), "cta"), (T("t14", 0), TOTAL, "silence")]
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
mus = bed(N, SR, [(0, T("t07", 0), "tension"), (T("t07", 0), T("t08", 0), "musicbox"), (T("t08", 0), T("t13", 0), "tension"), (T("t13", 0), T("t14", 0), "quest")], load)   # the owner's Suno tracks (4 Nov)

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

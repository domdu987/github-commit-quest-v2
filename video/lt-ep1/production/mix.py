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
    ("w01", 0.0, "crackle", 0.16), ("w01", 0.0, "rain", 0.1), ("w01", F("w01", 0, 1) - 0.05, "strike", 0.3), ("w01", F("w01", 0, 1), "thunder", 0.22), ("w01", F("w01", 0, 1) + 0.1, "zap", 0.16),
    ("w02", 0.0, "rain", 0.08), ("w02", 0.2, "hum", 0.08), ("w02", F("w02", 0, 1) + 0.1, "ding", 0.07), ("w02", F("w02", 0, 1) + 0.1, "sting", 0.08),
    ("w03", 0.0, "crackle", 0.12), ("w03", F("w03", 0, 1) + 0.3, "pop", 0.1), ("w03", F("w03", 0, 2) + 0.3, "pop", 0.1),
    ("w04", 0.0, "crackle", 0.12), ("w04", 0.5, "pop", 0.1), ("w04", F("w04", 0, 1) * 0.55 + 0.3, "pop", 0.1), ("w04", F("w04", 0, 1) + 0.2, "pop", 0.1), ("w04", F("w04", 0, 2) + 0.2, "ching", 0.1),
    ("w05", 0.0, "motor", 0.05), ("w05", F("w05", 0, 1) + 0.2, "ding", 0.06), ("w05", F("w05", 0, 1) + 0.3, "pop", 0.1),
    ("w06", 0.2, "wind", 0.16), ("w06", F("w06", 0, 1) + 0.2, "thunder", 0.16),
    ("w07", 0.0, "wind", 0.12), ("w07", 0.9, "thunder", 0.1), ("w07", F("w07", 0, 1) + 0.3, "pop", 0.1), ("w07", F("w07", 0, 2) + 0.2, "ding", 0.06),
    ("w08", 0.0, "rain", 0.14), ("w08", 0.3, "thunder", 0.12),
    ("w09", 0.0, "rain", 0.12), ("w09", 0.0, "crackle", 0.16), ("w09", F("w09", 0, 1) - 0.3, "riser", 0.1), ("w09", F("w09", 0, 1) - 0.03, "strike", 0.34), ("w09", F("w09", 0, 1), "thunder", 0.26), ("w09", F("w09", 0, 1) + 0.1, "zap", 0.2), ("w09", F("w09", 0, 2), "crackle", 0.14),
    ("w10", 0.0, "beep", 0.04), ("w10", 0.3, "pop", 0.1), ("w10", F("w10", 0, 1) + 1.0, "snap", 0.14), ("w10", F("w10", 0, 1) + 1.2, "pop", 0.1),
    ("w11", 0.95, "notif", 0.1), ("w11", 1.95, "notif", 0.1), ("w11", 2.95, "notif", 0.1),
    ("w12", F("w12", 0, 1), "zap", 0.1), ("w12", F("w12", 0, 1) + 0.3, "snap", 0.14),
    ("w13", 0.3, "beep", 0.05), ("w13", 1.1, "beep", 0.05), ("w13", F("w13", 0, 1), "beep", 0.08), ("w13", F("w13", 0, 1) + 0.3, "zap", 0.08), ("w13", F("w13", 0, 1) + 0.6, "beep", 0.08), ("w13", F("w13", 0, 1) + 0.9, "beep", 0.08),
    ("w14", 0.0, "crickets", 0.06), ("w14", F("w14", 0, 1) - 0.9, "riser", 0.06), ("w14", F("w14", 0, 1) - 0.05, "zap", 0.16), ("w14", F("w14", 0, 1), "powerdown", 0.22),
    ("w15", 0.4, "whoosh", 0.08), ("w15", F("w15", 0, 1), "zap", 0.2), ("w15", F("w15", 0, 1) + 0.1, "crackle", 0.16),
    ("w16", 0.0, "crackle", 0.14), ("w16", F("w16", 0, 1) - 0.2, "pop", 0.1), ("w16", F("w16", 0, 1), "tick", 0.08), ("w16", F("w16", 0, 1) + 0.3, "tick", 0.08), ("w16", F("w16", 0, 1) + 0.6, "tick", 0.08), ("w16", F("w16", 0, 1) + 0.9, "ding", 0.08), ("w16", F("w16", 0, 1) + 0.9, "hiss", 0.08),
    ("w17", 0.1, "ching", 0.08), ("w17", F("w17", 0, 1), "pop", 0.1), ("w17", F("w17", 0, 1) + 0.2, "ratchet", 0.08), ("w17", F("w17", 0, 1) + 1.0, "ching", 0.1), ("w17", F("w17", 0, 2) + 0.2, "swell", 0.06), ("w17", F("w17", 0, 3) + 0.1, "pop", 0.1), ("w17", F("w17", 0, 3) + 0.6, "trumpet", 0.08),
    ("w18", 0.0, "whoosh", 0.12),
]
SECTIONS = [(0, T("w02", 0), "tension"), (T("w02", 0), T("w06", 0), "hope"), (T("w06", 0), T("w10", 0), "tension"), (T("w10", 0), T("w14", 0), "hope"), (T("w14", 0), T("w18", 0), "twist"),
            (T("w18", 0), T("w19", 0), "cta"), (T("w19", 0), TOTAL, "silence")]
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
mus = bed(N, SR, [(0, T("w06", 0), "quest"), (T("w06", 0), T("w10", 0), "tension"), (T("w10", 0), T("w14", 0), "quest"), (T("w14", 0), T("w16", 0), "tension"), (T("w16", 0), T("w19", 0), "quest")], load)   # the owner's Suno tracks (4 Nov)

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

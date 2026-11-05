"""บางระจัน แบต 3% EP.3: the soundtrack from schedule.json: levelled narrator, synthesized SFX and the owner's Suno bed
(quest through the comedy, tension once the battery becomes the way home, quest again under the end card). Output about -14 LUFS."""
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
    ("d01", 0.0, "whoosh", 0.14), ("d01", F("d01", 0, 0) + 0.6, "ding", 0.06), ("d01", F("d01", 0, 2), "pop", 0.14),
    ("d02", 0.1, "pop", 0.14), ("d02", 0.6, "ding", 0.05),
    ("d03", 0.05, "creak", 0.12), ("d03", F("d03", 0, 0) + 0.5, "stomp", 0.22),
    ("d04", 0.0, "whoosh", 0.1), ("d04", F("d04", 0, 1) - 0.4, "riser", 0.1),
    ("d05", 0.1, "pop", 0.12), ("d05", F("d05", 0, 0) + 0.3, "crank", 0.1), ("d05", F("d05", 0, 1) + 0.3, "ding", 0.08), ("d05", F("d05", 0, 1) + 0.3, "swell", 0.1),
    ("d06", (vo_t("d06") + 0.9) - 0.1, "stomp", 0.16), ("d06", (vo_t("d06") + 0.9) + 0.3, "stomp", 0.16), ("d06", (vo_t("d06") + 0.9) + 0.7, "stomp", 0.16), ("d06", (vo_t("d06") + 0.9) + 0.2, "pop", 0.1),
    ("d07", F("d07", 0, 1) + 0.1, "pop", 0.1),
    ("d08", F("d08", 0, 1) + 0.25, "stomp", 0.2), ("d08", F("d08", 0, 1) + 0.25, "pop", 0.12),
    ("d09", 0.0, "whoosh", 0.12), ("d09", 0.3, "hum", 0.06),
    ("d10", 0.1, "hum", 0.05), ("d10", F("d10", 0, 1), "swell", 0.08),
    ("d11", F("d11", 0, 1), "ding", 0.07), ("d11", F("d11", 0, 1) + 0.5, "pop", 0.12),
    ("d12", F("d12", 0, 0) + 0.4, "ding", 0.08), ("d12", F("d12", 0, 1) - 0.1, "whoosh", 0.12),
    ("d13", 0.0, "whoosh", 0.12), ("d13", vo_t("d13") + 0.4, "boom", 0.16), ("d13", F("d13", 0, 1), "stomp", 0.22), ("d13", F("d13", 0, 1) + 0.4, "stomp", 0.2), ("d13", F("d13", 0, 1) + 0.8, "stomp", 0.2),
    ("d14", F("d14", 0, 0) + 0.3, "swell", 0.12), ("d14", F("d14", 0, 1), "riser", 0.14), ("d14", F("d14", 0, 1) + 1.0, "stomp", 0.18), ("d14", F("d14", 0, 1) + 1.5, "stomp", 0.2), ("d14", F("d14", 0, 1) + 2.0, "stomp", 0.22),
    ("d15", (vo_t("d15") + 0.55), "whoosh", 0.16),
    ("d16", F("d16", 0, 0) + 0.45, "ding", 0.08), ("d16", F("d16", 0, 1) + 0.3, "boom", 0.2),
    ("d17", 0.35, "stomp", 0.18), ("d17", F("d17", 0, 1), "hum", 0.04),
    ("d18", 0.2, "hum", 0.05), ("d18", F("d18", 0, 1), "riser", 0.08),
    ("d19", F("d19", 0, 1), "creak", 0.14), ("d19", F("d19", 0, 1) + 0.4, "creak", 0.12),
    ("d20", 0.0, "swell", 0.12), ("d20", F("d20", 0, 1), "boom", 0.16),
    ("d21", F("d21", 0, 0) + 0.15, "whoosh", 0.2), ("d21", F("d21", 0, 0) + 0.5, "stomp", 0.14),
    ("d22", F("d22", 0, 1) + 0.2, "pop", 0.12),
    ("d23", 0.0, "whoosh", 0.12),
]
SECTIONS = [(0, T("d02", 0), "tension"), (T("d02", 0), T("d09", 0), "hope"), (T("d09", 0), T("d20", 0), "panic"), (T("d20", 0), T("d23", 0), "twist"),
            (T("d23", 0), T("d24", 0), "cta"), (T("d24", 0), TOTAL, "silence")]
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
mus = bed(N, SR, [(0, T("d09", 0), "quest"), (T("d09", 0), T("d20", 0), "tension"), (T("d20", 0), T("d24", 0), "quest")], load)   # the owner's Suno tracks (4 Nov)

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

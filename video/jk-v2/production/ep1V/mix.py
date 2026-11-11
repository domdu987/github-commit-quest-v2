"""สกิลจอมโกหก v2 EP.1: the soundtrack from schedule.json: levelled narrator, synthesized SFX and a light bed
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

# ---- SFX cues (times follow the picture in body.part) ----
CUES = [
    ("k01", F("k01", 0, 1), "whoosh", 0.1),   # no hum/swell tone at the very start (owner 11 Nov: "เสียงที่ดังตื้ดตอนแรก เอาออก")
    ("k02", F("k02", 0, 2) - 0.1, "whoosh", 0.14), ("k02", F("k02", 0, 3), "blinker", 0.16), ("k02", D["k02"] - 0.8, "rewind", 0.18), ("k02", D["k02"] - 0.18, "whoosh", 0.14),
    ("k03", 0.0, "whoosh", 0.1), ("k03", F("k03", 0, 1), "ding", 0.07), ("k03", F("k03", 0, 2), "pop", 0.08),
    ("k04", F("k04", 0, 0) + 0.6, "blinker", 0.12), ("k04", F("k04", 0, 1), "pop", 0.1), ("k04", F("k04", 0, 2), "steps", 0.12), ("k04", F("k04", 0, 2), "whoosh", 0.08),
    ("k05", 0.1, "steps", 0.08), ("k05", F("k05", 0, 2) - 0.05, "pop", 0.12), ("k05", F("k05", 0, 3) + 0.3, "whoosh", 0.14), ("k05", F("k05", 0, 4), "thud", 0.3), ("k05", F("k05", 0, 4), "boom", 0.18),
    ("k06", 0.1, "swell", 0.14), ("k06", 0.5, "ding", 0.05), ("k06", F("k06", 0, 2), "ding", 0.06), ("k06", F("k06", 0, 3) + 1.6, "pop", 0.16),
    ("k07", 0.15, "crank", 0.14), ("k07", F("k07", 0, 1) - 0.1, "riser", 0.14), ("k07", F("k07", 0, 1), "ching", 0.14), ("k07", F("k07", 0, 2), "ding", 0.08),
    ("k08", 0.2, "rattle", 0.1), ("k08", F("k08", 0, 3) - 0.05, "plop", 0.12), ("k08", F("k08", 0, 3) + 0.6, "slam", 0.2), ("k08", F("k08", 0, 4), "pop", 0.1),
    ("k09", F("k09", 0, 0) + 0.3, "pop", 0.1), ("k09", F("k09", 0, 1) + 0.3, "whoosh", 0.1), ("k09", F("k09", 0, 2) + 0.05, "ding", 0.06), ("k09", F("k09", 0, 4), "ding", 0.06),
    ("k10", F("k10", 0, 0) + 0.05, "ding", 0.06), ("k10", F("k10", 0, 2) + 0.1, "tick", 0.08), ("k10", F("k10", 0, 3) + 0.1, "whoosh", 0.1),
    ("k11", F("k11", 0, 0) + 0.2, "creak", 0.16), ("k11", F("k11", 0, 0) + 0.45, "whoosh", 0.2), ("k11", F("k11", 0, 1) + 0.3, "whoosh", 0.16), ("k11", F("k11", 0, 1) + 1.25, "boom", 0.3), ("k11", F("k11", 0, 1) + 1.25, "stomp", 0.2),
    ("k12", 0.0, "whoosh", 0.12),
]
SECTIONS = [(0, T("k03", 0), "tension"), (T("k03", 0), T("k06", 0), "calm"), (T("k06", 0), T("k11", 0), "hope"), (T("k11", 0), T("k12", 0), "twist"),
            (T("k12", 0), T("k13", 0), "cta"), (T("k13", 0), TOTAL, "silence")]
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
mus = bed(N, SR, [(0, T("k03", 0), "tension"), (T("k03", 0), T("k06", 0), "musicbox"), (T("k06", 0), T("k11", 0), "quest"), (T("k11", 0), T("k12", 0), "tension"), (T("k12", 0), T("k13", 0), "quest")], load)   # the owner's Suno tracks (4 Nov) instead of the synth bed

# ---- levels + ducking (the bed sits well under the voice) ----
mus = level(mus, -31)
# the hook (sword at the throat, 0 → the rewind) wants the tension track up front: +6 dB until k03, eased down over 0.6 s (owner 11 Nov asked about the opening music)
_hb = np.ones(N, np.float32); _n3 = int(T("k03", 0) * SR); _r = int(0.6 * SR)
_hb[:_n3 - _r] = 10 ** (6 / 20); _hb[_n3 - _r:_n3] = np.linspace(10 ** (6 / 20), 1, _r, dtype=np.float32)
mus = mus * _hb
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

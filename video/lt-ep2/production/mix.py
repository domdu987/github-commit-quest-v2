"""ช่างเชื่อมสายฟ้า EP.2: the soundtrack from schedule.json: levelled narrator, synthesized SFX and the owner's Suno bed
(musicbox for เฮียกิม's night, tension for the forty-years-ago blackout, quest for the queue and the banana tree). Output about -14 LUFS."""
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
    ("r01", 0.0, "crickets", 0.05), ("r01", 0.3, "crackle", 0.12), ("r01", 0.8, "notif", 0.1), ("r01", F("r01", 0, 1) + 0.3, "notif", 0.1), ("r01", F("r01", 0, 1) + 0.9, "notif", 0.1),
    ("r02", 0.0, "crickets", 0.05), ("r02", F("r02", 0, 1) + 0.1, "knock", 0.2), ("r02", F("r02", 0, 1) + 0.4, "knock", 0.2),
    ("r03", 0.3, "creak", 0.14), ("r03", 0.7, "pop", 0.1), ("r03", F("r03", 0, 1) + 0.3, "ding", 0.06), ("r03", F("r03", 0, 1) + 0.3, "pop", 0.1),
    ("r04", F("r04", 0, 1) + 0.3, "pop", 0.1), ("r04", F("r04", 0, 1) + 0.3, "thunder", 0.08),
    ("r05", F("r05", 0, 1), "hum", 0.05),
    ("r06", F("r06", 0, 1) - 0.2, "creak", 0.18), ("r06", F("r06", 0, 1) + 0.3, "latch", 0.12),
    ("r07", 0.05, "whoosh", 0.1), ("r07", F("r07", 0, 1) - 0.3, "ding", 0.06), ("r07", F("r07", 1, 1) - 0.3, "ding", 0.06), ("r07", vo_t("r07", 2) + 0.6, "ding", 0.06),
    ("r08", 0.3, "zap", 0.16), ("r08", 0.3, "hum", 0.08), ("r08", F("r08", 0, 1) + 0.1, "powerdown", 0.22), ("r08", F("r08", 0, 1) + 0.5, "pop", 0.1),
    ("r09", 0.3, "pop", 0.1), ("r09", F("r09", 0, 1) - 0.2, "steps", 0.1), ("r09", F("r09", 0, 2) + 0.1, "zap", 0.14), ("r09", F("r09", 0, 3) - 0.4, "tick", 0.06), ("r09", F("r09", 0, 3) - 0.1, "tick", 0.06), ("r09", F("r09", 0, 3) + 0.2, "tick", 0.06), ("r09", F("r09", 0, 3) + 0.4, "notif", 0.12),
    ("r10", F("r10", 0, 1), "ching", 0.12), ("r10", F("r10", 0, 1) + 0.4, "ching", 0.1), ("r10", F("r10", 0, 2) + 0.2, "pop", 0.1), ("r10", F("r10", 0, 2) + 0.6, "trumpet", 0.08),
    ("r11", 0.5, "riser", 0.1), ("r11", 0.6, "crackle", 0.16), ("r11", F("r11", 0, 1) + 0.1, "whoosh", 0.12), ("r11", F("r11", 0, 1) + 0.2, "steps", 0.12), ("r11", F("r11", 0, 1) + 1.1, "thud", 0.14), ("r11", F("r11", 0, 1) + 1.2, "zap", 0.1), ("r11", F("r11", 0, 2) + 0.2, "pop", 0.1),
    ("r12", 0.0, "crackle", 0.1), ("r12", F("r12", 0, 2) + 0.1, "ding", 0.12), ("r12", F("r12", 0, 2) + 0.1, "pop", 0.12), ("r12", F("r12", 0, 2) + 0.4, "pop", 0.1),
    ("r13", 0.0, "whoosh", 0.12),
]
SECTIONS = [(0, T("r02", 0), "tension"), (T("r02", 0), T("r08", 0), "calm"), (T("r08", 0), T("r09", 0), "tension"), (T("r09", 0), T("r13", 0), "twist"),
            (T("r13", 0), T("r14", 0), "cta"), (T("r14", 0), TOTAL, "silence")]
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
mus = bed(N, SR, [(0, T("r02", 0), "quest"), (T("r02", 0), T("r08", 0), "musicbox"), (T("r08", 0), T("r09", 0), "tension"), (T("r09", 0), T("r14", 0), "quest")], load)   # the owner's Suno tracks (4 Nov)

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

"""Build the EP.3 (finale) soundtrack from schedule.json: per-line levelled voice, synthesized SFX (wind in the fog, the embers of
the doused stove, the door slamming, the pickup's engine, a phone beep, a creaking door in the 2529 flashback) and the Suno music bed with dips before the scares and sidechain ducking under the voice.
Output -14 LUFS, hard cut to silence at the end."""
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
    """Centered moving average via cumulative sums (np.convolve with a long kernel is far too slow here)."""
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


def frag(k, i=0, j=0):
    return SH[k]["vo"][i]["t"] + SH[k]["vo"][i]["frags"][j]


# ---- voice: every line levelled on its own so whispers and shouts sit at a readable loudness ----
LINE_GAIN = {}
vo = np.zeros(N, np.float32)
for s in SC["shots"]:
    for v in s["vo"]:
        x = load(os.path.join(HERE, "vo", f"{v['id']}.wav"))
        place(vo, level(x, -18 + LINE_GAIN.get(v["id"], 0)), s["start"] + v["t"])

# ---- sfx cues: (shot, t from shot start (negative = from its end), type, gain) ----
D = {k: SH[k]["dur"] for k in SH}


def beats(k, t0, dur, period, g=0.9):  # heartbeat sfx in step with Fx.heart
    return [(k, t0 + i * period, "heartbeat", g) for i in range(int((dur - 0.1) / period) + 1)]


def bed(kind, a, b, g, step=4.6):  # overlapping copies of an ambience between absolute times a and b
    out, t = [], a - 0.6
    while t < b - 1.0:
        out.append((None, t, kind, g))
        t += step
    return out


CUES = [
    # cold open: the door glowing, a voice from inside
    *bed("wind", T("hook", 0), T("hook", -0.1), 0.7, 2.6), ("hook", 0.3, "crackle", 0.4), ("hook", 1.5, "creak", 0.6), *beats("hook", frag("hook", 0, 3), D["hook"] - frag("hook", 0, 3), 0.55, 0.55),
    ("hook", vo_t("hook", 1), "sting", 1.0), ("hook", vo_t("hook", 1), "boom", 0.7), ("hook", vo_t("hook", 1), "glitch", 0.6), ("hook", -0.25, "whoosh", 0.8),
    ("chapter", 0.05, "whoosh", 0.6), ("chapter", 0.3, "wind", 0.5), ("chapter", 0.55, "sting", 0.5),
    # back inside: embers, the gas, the thing in มิ้นท์'s jacket
    *bed("crackle", T("inside", 0), T("turn", -0.1), 0.5, 4.0), ("inside", 0.1, "creak", 0.7), ("inside", 1.4, "buzz", 0.5),
    *beats("inside", frag("inside", 0, 2), D["inside"] - frag("inside", 0, 2), 0.5, 0.5),
    ("call", 0.1, "buzz", 0.45), *beats("call", 0.3, D["call"] - 0.3, 0.55, 0.6),
    ("turn", frag("turn", 0, 1), "sting", 1.2), ("turn", frag("turn", 0, 1), "boom", 0.8), ("turn", frag("turn", 0, 1), "glitch", 0.7), *beats("turn", frag("turn", 0, 1), D["turn"] - frag("turn", 0, 1), 0.4, 0.75),
    # outside: the real มิ้นท์; เจ out, the door slams
    *bed("wind", T("wan", 0), T("nosig", -0.1), 0.6, 2.6), ("wan", 0.1, "sting", 0.6), ("wan", 0.2, "rustle", 0.7),
    ("out", 1.25, "slam", 1.3), ("out", 1.3, "boom", 0.4), ("out", 1.6, "thud", 0.5), *[("out", frag("out", 0, j) - 0.05, "pop", 0.45) for j in (0, 1, 2)],
    *beats("breath", 0.3, D["breath"] - 0.3, 0.6, 0.45),
    *[("ems", frag("ems", 0, j) - 0.05, "pop", 0.45) for j in (0, 1, 2)], ("ems", frag("ems", 0, 3), "ding", 0.6),
    ("nosig", 0.15, "beep", 0.6), ("nosig", 0.55, "beep", 0.6), ("nosig", 0.95, "beep", 0.6),
    # the pickup in the fog
    *bed("wind", T("lights", 0), T("nodrive", -0.1), 0.5, 2.6), ("lights", 0.3, "engine", 0.5), ("lights", 1.6, "engine", 0.7), ("lights", frag("lights", 0, 1), "swell", 0.5),
    *bed("engine", T("drive", 0), T("nodrive", 2.0), 0.55, 3.6), *[("drive", frag("drive", 0, j) - 0.05, "pop", 0.45) for j in (0, 1, 2)], ("drive", frag("drive", 0, 3), "ding", 0.5),
    ("driver", 0.2, "sting", 0.5), *beats("driver", 0.2, D["driver"] - 0.2, 0.55, 0.4),
    *[("nodrive", frag("nodrive", 0, j) - 0.05, "pop", 0.45) for j in (1, 2, 3)], ("nodrive", 1.0, "engine", 0.6), ("nodrive", 2.6, "engine", 0.35),
    # morning at the pump: "I never left"
    ("morning", 0.1, "whoosh", 0.4), ("morning", 0.2, "wind", 0.3),
    ("never", frag("never", 0, 1), "sting", 0.8), *beats("never", frag("never", 0, 1), D["never"] - frag("never", 0, 1), 0.48, 0.6),
    ("mimic", frag("mimic", 0, 2) - 0.05, "sting", 0.9), ("mimic", frag("mimic", 0, 2) - 0.05, "glitch", 0.6),
    *beats("mimic", frag("mimic", 0, 2), D["mimic"] - frag("mimic", 0, 2), 0.45, 0.6),
    # 2529
    ("mother", 0.05, "rewind", 0.5), ("mother", 0.3, "wind", 0.5), ("mother", 0.4, "crackle", 0.35),
    ("mother", frag("mother", 0, 3) - 0.6, "creak", 0.9), ("mother", frag("mother", 0, 3) - 0.2, "slam", 0.9), ("mother", frag("mother", 0, 3), "sting", 0.8),
    *beats("mother", frag("mother", 0, 3), D["mother"] - frag("mother", 0, 3), 0.55, 0.5),
    # the old pickup, fresh mud, the photo
    ("truck", 0.1, "wind", 0.4), ("truck", frag("truck", 0, 3) - 0.3, "creak", 0.4), ("truck", frag("truck", 0, 3), "swell", 0.5),
    ("mud", frag("mud", 0, 1), "sting", 1.1), ("mud", frag("mud", 0, 1), "boom", 0.7), ("mud", frag("mud", 0, 1), "glitch", 0.5), *beats("mud", frag("mud", 0, 1), D["mud"] - frag("mud", 0, 1), 0.42, 0.75),
    ("photo", 0.1, "beep", 0.5), ("photo", frag("photo", 0, 1), "sting", 0.7), ("photo", frag("photo", 0, 3), "sting", 1.1), ("photo", frag("photo", 0, 3), "boom", 0.8), ("photo", frag("photo", 0, 3), "glitch", 0.7),
    *beats("photo", frag("photo", 0, 1), D["photo"] - frag("photo", 0, 1), 0.42, 0.7),
    *beats("choice", 0.0, D["choice"] - 0.3, 0.38, 1.0), *[("choice", 0.05 + k * 1.0, "tick", 1.0) for k in range(3)], ("choice", 1.0, "glitch", 0.6),
    ("choice", 0.3, "wind", 0.6), ("choice", D["choice"] - 2.2, "riser", 1.0), ("choice", D["choice"] - 0.62, "sting", 1.0), ("choice", D["choice"] - 0.6, "glitch", 0.8), ("choice", D["choice"] - 0.6, "boom", 0.7),
    ("next", 0.3, "whoosh", 0.5), ("next", 0.45, "pop", 0.5), ("next", 0.8, "sting", 0.7), *beats("next", 0.9, D["next"] - 0.9, 0.7, 0.5),
]
# no hiss: the noise-based wind bed reads as static under the voice (user: "ลบเสียงซ่าออก"), and the fire keeps only a faint crackle
CUES = [(k, t, typ, g * (0.3 if typ == "crackle" else 1)) for k, t, typ, g in CUES if typ not in ("wind",)]
CUES = [c for c in CUES if c[3] > 0]
cues = {"duration": TOTAL, "sections": [{"start": 0, "end": TOTAL, "mood": "silence"}],
        "sfx": [{"t": round(t if k is None else T(k, t), 3), "type": typ, "gain": g} for k, t, typ, g in CUES]}
json.dump(cues, open(os.path.join(HERE, "sfx_cues.json"), "w"))
subprocess.run(["python3", os.path.join(HERE, "..", "synth.py"), os.path.join(HERE, "sfx_cues.json"), os.path.join(HERE, "sfx.wav")],
               check=True, env={**os.environ, "STEMS": "1"})
sfx = load(os.path.join(HERE, "sfx_sfx.wav"))[:N]
sfx = np.pad(sfx, (0, N - len(sfx)))



# ---- music with horror dips ----
mus = load(os.path.join(HERE, "..", "music", "suno1.mp3"))
while len(mus) < N:
    mus = np.concatenate([mus, mus])
mus = mus[:N]
t = np.arange(N) / SR
gain = np.ones(N, np.float32)


def dip(t0, t1, lvl, ramp=0.25):
    a = np.clip((t - (t0 - ramp)) / ramp, 0, 1) * np.clip(((t1 + ramp) - t) / ramp, 0, 1)
    np.minimum(gain, 1 - (1 - lvl) * a, out=gain)


dip(0.0, T("hook", -0.1), 0.25, 0.05)                    # the cold open: wind and the glowing door
dip(T("call", 0), T("turn", -0.05), 0.3)
dip(T("never", frag("never", 0, 1)), T("mimic", -0.05), 0.35)
dip(T("mother", 0), T("mother", -0.05), 0.5)
dip(T("mud", 0), T("photo", -0.05), 0.3)
dip(T("choice", 0), T("choice", -0.3), 0.5)
boost = np.ones(N, np.float32)
mus = mus * gain * boost
end = int(T("choice", -0.2) * SR)
mus[end:] = 0  # hard cut to black and silence

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mix = vo + mus * duck + sfx
cut, card = int(T("choice", -0.2) * SR), int(T("next", 0.3) * SR)
mix[cut - 240:cut] *= np.linspace(1, 0, 240)
mix[cut:card] = 0  # a beat of black and silence after the cliffhanger, then only the end card's own sounds
peak = np.max(np.abs(mix))
if peak > 0.98:
    mix = np.tanh(mix / peak * 1.2) * 0.95
out = os.path.join(HERE, "mix_raw.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", out],
               input=mix.astype(np.float32).tobytes(), check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)
print("mix written", TOTAL)

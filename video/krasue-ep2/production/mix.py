"""แสงกระสือ EP.2 (สูตรเสียงกอย re-cut): build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX for a flooded village
at night with live wires (the mains hum, a broken line arcing in the water, the main switch thrown, the power dying, wading steps, the
old comic's pages) and the Suno music bed with dips before the scares and sidechain ducking under the voice. Output -14 LUFS, hard cut
to silence after the choice. No noise beds and no high hiss (user: "เสียงซ่าๆเอาออก")."""
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


F = frag
SHOCK = max(2.4, frag("walk", 0, 1) + 0.4)  # the walk shot: his hand on the fridge
B2 = frag("broom", 0, 2) - 0.12             # the broom shot cuts to the switch close up
HIT = B2 + 0.55                             # the broom handle knocks the lever down
UP = frag("lever", 0, 1) + 0.2              # the lever starts going up on its own
CUT1 = vo_t("know1", 1) + 0.2               # the diagram's lever goes down
FALL = frag("dark", 0, 1)                   # เต้ย drops into the water
PRESS = vo_t("breathe", 1) - 0.2            # she stops pressing: he breathes


def zaps(k, ts, g=0.5):
    return [(k, t, "zap", g) for t in ts]


def buzzing(k, t0, dur, g=0.6, step=0.35):  # a body stuck on a live appliance: a stuttering zap train
    return [(k, t0 + i * step, "zap", g) for i in range(int(dur / step) + 1)]


CUES = [
    ("recap", 0.0, "hum", 0.6), ("recap", 0.0, "glitch", 0.5), *zaps("recap", (0.3, 1.2), 0.5), *beats("recap", 0.0, D["recap"], 0.4, 0.6),
    *buzzing("hook", 0.3, D["hook"] - 0.6, 0.55), ("hook", 0.3, "buzz", 0.4), *beats("hook", 0.3, D["hook"] - 0.3, 0.4, 0.5),
    ("hook", D["hook"] - 0.5, "sting", 1.0), ("hook", D["hook"] - 0.5, "glitch", 0.7), ("hook", D["hook"] - 0.45, "boom", 0.6),
    ("stop", 0.05, "whoosh", 0.5), ("stop", 0.1, "slam", 0.3), ("stop", 0.6, "plop", 0.3),
    ("off", 0.0, "hum", 0.5), ("off", 0.3, "beep", 0.3), *zaps("off", (0.4, 1.3, 2.1), 0.5), ("off", F("off", 0, 1), "powerdown", 0.8), ("off", F("off", 0, 1), "glitch", 0.4),
    ("dazed", 0.3, "drip", 0.4), ("dazed", 1.4, "drip", 0.3), ("dazed", F("dazed", 0, 1), "swell", 0.4), *beats("dazed", F("dazed", 0, 1), D["dazed"] - F("dazed", 0, 1), 0.45, 0.45),
    ("scold", 0.05, "plop", 0.35), ("scold", 0.9, "creak", 0.25),
    ("one", F("one", 0, 1), "click", 0.4), ("one", F("one", 0, 1) + 0.05, "hum", 0.5),
    ("down", 0.1, "click", 0.3),
    ("two", F("two", 0, 1) - 0.1, "zap", 0.5), ("two", F("two", 0, 1), "hum", 0.6), ("two", F("two", 0, 1) + 0.2, "buzz", 0.4), *beats("two", F("two", 0, 1), D["two"] - F("two", 0, 1), 0.45, 0.45),
    ("lever", UP, "creak", 0.4), ("lever", UP + 0.5, "clang", 0.7), ("lever", UP + 0.5, "zap", 0.8), ("lever", UP + 0.55, "hum", 0.6),
    ("call", 0.0, "hum", 0.4), ("call", 0.2, "swell", 0.5), *beats("call", 0.0, D["call"], 0.5, 0.55),
    ("walk", 0.0, "hum", 0.4), *[("walk", 0.25 * k, "steps", 0.3) for k in range(7)], *[("walk", t, "plop", 0.35) for t in (1.85, 2.1)],
    ("walk", SHOCK, "sting", 1.0), ("walk", SHOCK, "glitch", 0.7), *buzzing("walk", SHOCK, D["walk"] - SHOCK, 0.8),
    *buzzing("scream", 0.0, D["scream"], 0.5), ("scream", 0.05, "whoosh", 0.4),
    *[("rush", 0.3 * k, "steps", 0.45) for k in range(5)], *buzzing("rush", 0.0, D["rush"], 0.5), *beats("rush", 0.0, D["rush"], 0.36, 0.55),
    ("rule", 0.0, "glitch", 0.5), ("rule", 0.05, "sting", 0.6), *buzzing("rule", 0.2, D["rule"] - 0.2, 0.25, 0.5),
    *buzzing("know1", 0.0, CUT1, 0.3, 0.5), ("know1", CUT1 + 0.1, "clang", 0.5), ("know1", CUT1 + 0.15, "powerdown", 0.5), ("know1", CUT1 + 0.4, "ding", 0.5),
    # koi-style: the eyes by the switch fade in on a held breath, a heartbeat, no sting
    ("guard", 0.0, "hum", 0.5), ("guard", F("guard", 0, 1) - 0.3, "swell", 0.5), *beats("guard", F("guard", 0, 1), D["guard"] - F("guard", 0, 1), 0.5, 0.55),
    ("broom", 0.2, "rustle", 0.4), ("broom", 0.8, "whoosh", 0.3), *beats("broom", 0.0, B2, 0.4, 0.5),
    ("broom", B2 + 0.1, "whoosh", 0.7), ("broom", HIT, "clang", 0.9), ("broom", HIT + 0.05, "zap", 0.9), ("broom", HIT + 0.4, "thud", 0.6), ("broom", HIT + 0.45, "powerdown", 0.9),
    ("know2", 0.1, "hum", 0.35), ("know2", 0.2, "whoosh", 0.35), ("know2", vo_t("know2", 1), "ding", 0.5),
    ("dark", 0.05, "drip", 0.3), ("dark", FALL, "splash", 1.0), ("dark", FALL + 0.1, "thud", 0.4), *beats("dark", F("dark", 0, 2), D["dark"] - F("dark", 0, 2), 0.5, 0.55),
    ("know3", 0.3, "beep", 0.35), ("know3", 0.8, "ring", 0.3), *[("know3", vo_t("know3", 1) + 0.2 + 0.5 * k, "thud", 0.25) for k in range(int((D["know3"] - vo_t("know3", 1) - 0.2) / 0.5) + 1)],
    *[("breathe", 0.5 * k, "thud", 0.25) for k in range(int(PRESS / 0.5) + 1)], ("breathe", PRESS + 0.1, "swell", 0.5),
    *[("knock", F("knock", 0, 1) + k * 0.32, "knock", 0.9) for k in range(3)], *beats("knock", F("knock", 0, 1), D["knock"] - F("knock", 0, 1), 0.45, 0.45),
    *[("voice", 0.05 + k * 0.3, "knock", 0.6) for k in range(2)],
    ("under", F("under", 0, 1) - 0.2, "swell", 0.6), ("under", F("under", 0, 1), "glitch", 0.4), *beats("under", F("under", 0, 1), D["under"] - F("under", 0, 1), 0.42, 0.55),
    ("inside", 0.0, "hum", 0.4), ("inside", D["inside"] - 1.4, "creak", 0.6), *beats("inside", 0.0, D["inside"], 0.4, 0.6),
    *beats("choice", 0.0, D["choice"] - 0.3, 0.38, 1.0), *[("choice", 0.05 + k * 1.0, "tick", 1.0) for k in range(3)], ("choice", 1.0, "glitch", 0.6), *[("choice", 0.4 + k * 0.9, "knock", 0.5) for k in range(2)],
    ("choice", D["choice"] - 2.2, "riser", 1.0), ("choice", D["choice"] - 0.62, "sting", 1.0), ("choice", D["choice"] - 0.6, "glitch", 0.8), ("choice", D["choice"] - 0.6, "boom", 0.7),
    ("next", 0.3, "whoosh", 0.5), ("next", 0.45, "drip", 0.6), ("next", 0.6, "zap", 0.35), ("next", 0.8, "sting", 0.7), *beats("next", 0.9, D["next"] - 0.9, 0.7, 0.5),
]
# no hiss: the noise-based wind bed reads as static under the voice (user: "ลบเสียงซ่าออก")
CUES = [c for c in CUES if c[2] not in ("wind", "lap") and c[3] > 0]  # no noise beds (user: "เสียงซ่าๆเอาออก")
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


dip(0.0, T("recap", -0.05), 0.3, 0.05)
dip(T("hook", 0), T("hook", -0.05), 0.35)
dip(T("walk", SHOCK), T("rule", -0.05), 0.25)
dip(T("guard", 0), T("broom", B2), 0.35)  # the eyes by the switch: the music holds its breath
dip(T("dark", 0), T("dark", -0.05), 0.3)
dip(T("knock", 0), T("inside", -0.05), 0.3)
dip(T("choice", 0), T("choice", -0.3), 0.5)
mus = mus * gain
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

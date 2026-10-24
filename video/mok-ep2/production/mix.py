"""Build the EP.2 soundtrack from schedule.json: per-line levelled voice, synthesized SFX (the power window, a dying hazard
relay, a starter that won't catch, wind in the fog, a charcoal fire crackling, the shutters banging, a camera shutter, steam
off the doused stove) and the Suno music bed with dips before the scares and sidechain ducking under the voice.
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
    # cold open: the fire, the sleepers, the dead round the stove
    *bed("crackle", T("hook", 0), T("hook", -0.1), 0.9, 4.0), ("hook", 0.2, "wind", 0.3), *beats("hook", 0.4, D["hook"] - 0.4, 0.6, 0.5),
    ("hook", vo_t("hook", 1), "sting", 1.0), ("hook", vo_t("hook", 1), "boom", 0.7), ("hook", vo_t("hook", 1), "glitch", 0.6), ("hook", -0.25, "whoosh", 0.8),
    ("chapter", 0.05, "whoosh", 0.6), ("chapter", 0.3, "wind", 0.5), ("chapter", 0.55, "sting", 0.5),
    # the window comes down: nobody; then 06:00 and the car won't start
    ("window", 0.1, "motor", 1.3), ("window", frag("window", 0, 1) + 0.5, "sting", 0.9), ("window", frag("window", 0, 1) + 0.5, "glitch", 0.5),
    ("window", frag("window", 0, 2), "whoosh", 0.6), ("window", frag("window", 0, 2) + 0.1, "wind", 0.8), *beats("window", frag("window", 0, 1), D["window"] - frag("window", 0, 1), 0.5, 0.55),
    ("dawn", frag("dawn", 0, 2) - 0.05, "swell", 0.5), ("dawn", frag("dawn", 0, 3), "sting", 0.7),
    *bed("blinker", T("dawn", 0), T("start", 0.6), 0.35, 0.8), ("dawn", 0.1, "wind", 0.5), ("dawn", frag("dawn", 0, 1), "swell", 0.4),
    ("start", 0.05, "crank", 1.4), ("start", 0.75, "crank", 1.0), ("start", vo_t("start", 1), "thud", 0.25),
    # into the fog, the village
    *bed("wind", T("walk", 0), T("village", -0.1), 0.8, 2.6), ("walk", 0.3, "crickets", 0.25),
    ("village", 0.3, "creak", 0.6), ("village", vo_t("village", 1), "sting", 0.7), *beats("village", vo_t("village", 1), D["village"] - vo_t("village", 1), 0.5, 0.55),
    ("stove", 0.15, "creak", 0.8), ("stove", 0.3, "wind", 0.4), ("stove", frag("stove", 0, 2), "swell", 0.5), ("stove", frag("stove", 0, 2), "sting", 0.6),
    *beats("stove", frag("stove", 0, 2), D["stove"] - frag("stove", 0, 2), 0.5, 0.5),
    # the fire, the shutters, the photo
    ("light", 0.3, "snap", 0.6), ("light", 0.45, "whoosh", 0.4), ("light", 1.42, "slam", 1.1),
    *bed("crackle", T("light", 0.4), T("shout", 0), 0.75, 4.0),
    ("photo", vo_end("photo") - 0.05, "shutter", 1.4), ("photo", vo_end("photo") - 0.05, "pop", 0.4),
    ("pic", 0.1, "beep", 0.5), ("pic", frag("pic", 0, 1), "sting", 0.8), ("pic", frag("pic", 0, 2), "boom", 0.8), ("pic", frag("pic", 0, 2), "glitch", 0.6),
    *beats("pic", frag("pic", 0, 1), D["pic"] - frag("pic", 0, 1), 0.45, 0.65),
    # symptoms, sleep, the rule
    ("sick", 0.2, "buzz", 0.5), *[("sick", frag("sick", 0, j) + 0.1, "pop", 0.4) for j in (0, 1, 2)], *beats("sick", 0.3, D["sick"] - 0.3, 0.7, 0.45),
    ("sleep", vo_t("sleep", 1) - 0.1, "swell", 0.6), ("sleep", vo_t("sleep", 1) + 0.05, "ding", 0.45), ("sleep", frag("sleep", 1, 1), "sting", 0.8),
    *beats("sleep", vo_t("sleep", 1), D["sleep"] - vo_t("sleep", 1), 0.55, 0.6),
    # outside: better; what it is
    *bed("wind", T("out", 0), T("know", -0.1), 0.7, 2.6), ("out", frag("out", 0, 1), "swell", 0.4),
    *[("know", frag("know", 0, j) - 0.05, "pop", 0.45) for j in (0, 1, 3)], ("know", frag("know", 0, 3), "ding", 0.5),
    *[("gas", frag("gas", 0, j) - 0.05, "pop", 0.45) for j in (0, 1, 2)], ("gas", frag("gas", 0, 3) - 1.0, "riser", 0.6), ("gas", frag("gas", 0, 3), "sting", 0.9), ("gas", frag("gas", 0, 3), "boom", 0.5),
    *beats("gas", frag("gas", 0, 3), D["gas"] - frag("gas", 0, 3), 0.5, 0.6),
    ("shout", 0.05, "wind", 0.6), ("shout", 0.1, "sting", 0.6),
    ("act", 0.3, "hiss", 1.4), ("act", 0.35, "hiss", 1.0), ("act", 0.5, "whoosh", 0.4), ("act", 1.0, "thud", 0.5), ("act", 2.2, "thud", 0.4),
    *[("act", frag("act", 0, j) - 0.05, "pop", 0.45) for j in (1, 2)],
    ("sig", 0.05, "glitch", 0.35), ("sig", 0.05, "beep", 0.35),
    ("sig", frag("sig", 0, 0) + 0.3, "ding", 0.6), ("sig", frag("sig", 0, 0) + 0.62, "ding", 0.6), ("sig", frag("sig", 0, 1) + 0.15, "ding", 0.6),
    ("sig", frag("sig", 0, 2), "glitch", 0.45), *beats("sig", frag("sig", 0, 2), frag("sig", 0, 3) - frag("sig", 0, 2), 0.38, 0.8),
    *[("sig", frag("sig", 0, 2) + o, "tick", 0.55 + 0.1 * k) for k, o in enumerate((0.1, 0.42, 0.68, 0.88, 1.02, 1.12))],
    ("sig", frag("sig", 0, 3) - 1.1, "riser", 0.6),
    ("sig", frag("sig", 0, 3), "sting", 1.1), ("sig", frag("sig", 0, 3), "boom", 0.8), ("sig", frag("sig", 0, 3), "glitch", 0.7), ("sig", frag("sig", 0, 3) + 0.12, "slam", 0.7),
    *beats("sig", frag("sig", 0, 3), D["sig"] - frag("sig", 0, 3), 0.5, 0.7),
    # the ring of the dead, มิ้นท์ inside, the bundle
    *bed("wind", T("ring", 0), T("choice", -0.3), 0.7, 2.6), ("ring", frag("ring", 0, 1), "sting", 0.7), *beats("ring", frag("ring", 0, 1), D["ring"] - frag("ring", 0, 1), 0.5, 0.6),
    ("inside", 0.1, "crackle", 0.5), ("inside", frag("inside", 0, 1), "sting", 1.0), ("inside", frag("inside", 0, 1), "glitch", 0.5),
    ("who", frag("who", 0, 2), "sting", 0.8), *beats("who", 0.3, D["who"] - 0.3, 0.48, 0.65),
    ("bundle", 0.3, "rustle", 0.8), ("bundle", vo_t("bundle"), "buzz", 0.4), ("bundle", frag("bundle", 0, 1), "sting", 1.1), ("bundle", frag("bundle", 0, 1), "boom", 0.7), ("bundle", frag("bundle", 0, 1), "glitch", 0.7),
    *beats("bundle", vo_t("bundle"), D["bundle"] - vo_t("bundle"), 0.42, 0.75),
    *beats("choice", 0.0, D["choice"] - 0.3, 0.38, 1.0), *[("choice", 0.05 + k * 1.0, "tick", 1.0) for k in range(3)], ("choice", 1.0, "glitch", 0.6),
    ("choice", 1.9, "creak", 1.2), ("choice", D["choice"] - 2.2, "riser", 1.0), ("choice", D["choice"] - 0.62, "sting", 1.0), ("choice", D["choice"] - 0.6, "glitch", 0.8), ("choice", D["choice"] - 0.6, "boom", 0.7),
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


dip(0.0, T("hook", -0.1), 0.2, 0.05)                     # the cold open: only the fire
dip(T("window", 0), T("start", -0.05), 0.35)
dip(T("pic", 0), T("pic", -0.05), 0.3)
dip(T("sleep", vo_t("sleep", 1) - 0.1), T("sleep", -0.05), 0.35)
dip(T("sig", frag("sig", 0, 2)), T("sig", frag("sig", 0, 3) + 0.05), 0.05, 0.12)  # silence before "ข้อเดียว"
dip(T("inside", 0), T("bundle", -0.05), 0.3)
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

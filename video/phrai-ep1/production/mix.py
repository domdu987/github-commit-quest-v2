"""Build the episode soundtrack from schedule.json: per-line levelled voice, synthesized rainforest SFX
(tap water, knocks, a muffled scream, the infected growling, stairwell footsteps) and the Suno music bed with dips before the scares and
sidechain ducking under the voice. Output -14 LUFS, hard cut to silence at the end."""
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


CODE = (0.0, 0.42, 0.6)   # บอส's knock: one, a beat, two quick (same as CODE in shots.part)


def code(k, t, g=1.0):
    return [(k, t + d, "knock", g) for d in CODE]


CUES = [
    # cold open: the knock code through the door, smoke hissing under it, a hand on the handle — stop
    *code("hook", 0.15, 1.0), *code("hook", 2.2, 1.0), ("hook", 0.3, "hiss", 0.4), ("hook", 0.0, "crackle", 0.4), *beats("hook", 0.3, D["hook"] - 0.3, 0.55, 0.6),
    ("hook", vo_t("hook", 1), "sting", 0.9), ("hook", vo_t("hook", 1), "boom", 0.6), ("hook", vo_t("hook", 1), "glitch", 0.5), ("hook", -0.25, "whoosh", 0.8),
    ("chapter", 0.05, "whoosh", 0.5), ("chapter", 0.3, "glitch", 0.35), *code("chapter", 1.2, 0.8), ("chapter", 0.67, "sting", 0.5),
    ("hush", 0.0, "rustle", 0.8), ("hush", 0.05, "sting", 0.6),
    *code("peep", 0.3, 0.9), ("peep", 0.2, "growl", 0.8), *beats("peep", 0.0, D["peep"], 0.45, 0.7),
    *code("mimic", 0.14, 1.3), ("mimic", frag("mimic", 0, 1), "sting", 1.0), ("mimic", frag("mimic", 0, 1), "glitch", 0.6), ("mimic", frag("mimic", 0, 1), "growl", 1.0),
    ("smoke", 0.0, "roar", 0.35), ("smoke", 0.1, "crackle", 0.5), ("smoke", frag("smoke", 0, 1), "sting", 0.7),
    ("map", 0.0, "crackle", 0.6), ("map", 0.2, "riser", 0.4), ("map", frag("map", 0, 1), "boom", 0.4),
    *[("alarm", 0.0 + k * 0.5, "beep", 0.75) for k in range(int(D["alarm"] / 0.5))], ("alarm", frag("alarm", 0, 2), "sting", 0.8), *beats("alarm", 0.0, D["alarm"], 0.35, 0.7),
    ("boss", 0.0, "steps", 0.8), ("boss", 0.1, "crackle", 0.4),
    ("touch", 0.2, "tap", 0.15), ("touch", frag("touch", 0, 1) - 0.05, "latch", 0.4), *beats("touch", 0.0, D["touch"], 0.45, 0.6),
    ("open", 0.2, "creak", 0.9), ("open", frag("open", 0, 1) - 0.1, "creak", 0.7), ("open", 0.3, "hiss", 0.4), ("open", 0.2, "roar", 0.3),
    ("crawl", 0.0, "crackle", 0.4), ("crawl", 0.0, "rustle", 0.6), ("crawl", 1.2, "rustle", 0.6), ("crawl", 2.4, "rustle", 0.6), *beats("crawl", 0.0, D["crawl"], 0.45, 0.6),
    # action: the uncle, the sniff, the extinguisher, the dash
    ("uncle", 0.45, "growl", 1.0), ("uncle", 0.5, "sting", 0.9), ("uncle", 0.5, "glitch", 0.4), *beats("uncle", 0.0, D["uncle"], 0.38, 0.7),
    ("sniff", 0.2, "hiss", 0.4), ("sniff", 0.4, "growl", 0.6), ("sniff", 0.9, "shriek", 1.0), ("sniff", 0.95, "sting", 0.9), *beats("sniff", 0.0, D["sniff"], 0.35, 0.8),
    ("spray", 0.05, "rustle", 0.7), ("spray", 0.25, "static", 1.0), ("spray", 0.25, "whoosh", 0.9), ("spray", 0.5, "shriek", 0.8), ("spray", 0.9, "thud", 0.7),
    ("dash", 0.0, "steps", 1.0), ("dash", 0.5, "steps", 0.9), ("dash", 0.1, "riser", 0.6),
    ("hotdoor", 0.0, "roar", 0.5), ("hotdoor", frag("hotdoor", 0, 1) + 0.15, "hiss", 0.6), ("hotdoor", frag("hotdoor", 0, 1) + 0.15, "sting", 0.9), *beats("hotdoor", 0.0, D["hotdoor"], 0.4, 0.7),
    ("second", frag("second", 0, 1), "ding", 0.6), ("second", frag("second", 0, 1) + 0.2, "whoosh", 0.5),
    *[("down", 0.2 + k * 0.4, "stomp", 0.35) for k in range(6)], ("down", frag("down", 0, 1), "swell", 0.4),
    ("real", frag("real", 0, 1) - 0.1, "pop", 0.5), ("real", frag("real", 0, 2) - 0.1, "ding", 0.5),
    ("pass", 0.3, "growl", 0.7), ("pass", 0.6, "hiss", 0.4), ("pass", 1.2, "shriek", 0.9), ("pass", 1.5, "sting", 0.9), *beats("pass", 0.0, D["pass"], 0.38, 0.75),
    ("confess", 0.1, "swell", 0.4),
    ("sleeve", 0.3, "rustle", 0.8), ("sleeve", frag("sleeve", 0, 1), "sting", 0.7), *beats("sleeve", 0.0, D["sleeve"], 0.5, 0.6),
    ("healed", frag("healed", 0, 1) - 0.05, "sting", 1.0), ("healed", frag("healed", 0, 1) - 0.05, "glitch", 0.6),
    ("sig", 0.05, "glitch", 0.35), ("sig", 0.05, "beep", 0.35),
    ("sig", frag("sig", 0, 0) + 0.3, "ding", 0.6), ("sig", frag("sig", 0, 0) + 0.62, "ding", 0.6), ("sig", frag("sig", 0, 1) + 0.15, "ding", 0.6),
    ("sig", frag("sig", 0, 2), "glitch", 0.45), *beats("sig", frag("sig", 0, 2), frag("sig", 0, 3) - frag("sig", 0, 2), 0.38, 0.8),
    *[("sig", frag("sig", 0, 2) + o, "tick", 0.55 + 0.1 * k) for k, o in enumerate((0.1, 0.42, 0.68, 0.88, 1.02, 1.12))],  # ticking that speeds up into the cross
    ("sig", frag("sig", 0, 3) - 1.1, "riser", 0.6),
    ("sig", frag("sig", 0, 3), "sting", 1.1), ("sig", frag("sig", 0, 3), "boom", 0.8), ("sig", frag("sig", 0, 3), "glitch", 0.7), ("sig", frag("sig", 0, 3) + 0.12, "slam", 0.7),
    *beats("sig", frag("sig", 0, 3), D["sig"] - frag("sig", 0, 3), 0.5, 0.7),
    *bed("siren", T("street", 0), T("box", -0.2), 0.12, 2.9), ("street", 0.0, "wind", 0.3), ("street", 0.2, "crank", 0.3),
    ("order", vo_t("order") - 0.1, "static", 0.4), ("order", frag("order", 0, 2), "sting", 0.6),
    *[("jit", 0.2 + k * 0.5, "stomp", 0.3) for k in range(4)], ("jit", 0.1, "swell", 0.4),
    ("bye", 0.1, "swell", 0.5),
    ("box", 0.2, "slam", 1.4), ("box", 0.25, "latch", 1.0), ("box", 0.3, "boom", 0.6), *code("box", frag("box", 0, 1) + 0.1, 1.3), *code("box", frag("box", 0, 2) + 0.05, 1.4),
    ("box", frag("box", 0, 2), "sting", 1.0), ("box", frag("box", 0, 2), "glitch", 0.5), *beats("box", 0.0, D["box"], 0.4, 0.8),
    *code("choice", 0.2, 1.0), *code("choice", 1.4, 1.2), *code("choice", 1.45, 0.8), *code("choice", 2.3, 1.3), *code("choice", 2.35, 0.9),
    *beats("choice", 0.0, D["choice"] - 0.3, 0.38, 1.0), *[("choice", 0.05 + k * 1.0, "tick", 1.0) for k in range(3)], ("choice", 1.0, "glitch", 0.6),
    ("next", 0.3, "buzz", 0.5), ("next", 0.42, "slam", 0.6), ("next", 0.42, "glitch", 0.35), ("next", 0.85, "sting", 0.7), *beats("next", 0.9, D["next"] - 0.9, 0.7, 0.5),
    ("choice", D["choice"] - 2.2, "riser", 1.0), ("choice", D["choice"] - 0.62, "sting", 1.0), ("choice", D["choice"] - 0.6, "glitch", 0.8), ("choice", D["choice"] - 0.6, "boom", 0.7),
]
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


dip(0.0, T("hook", -0.1), 0.15, 0.05)                    # the cold open: the knocks, the smoke
dip(T("peep", 0), T("mimic", -0.05), 0.25)
dip(T("touch", 0), T("crawl", -0.05), 0.35)
dip(T("hotdoor", 0), T("hotdoor", -0.1), 0.35)
dip(T("confess", 0), T("healed", -0.05), 0.4)
dip(T("sig", frag("sig", 0, 2)), T("sig", frag("sig", 0, 3) + 0.05), 0.05, 0.12)  # silence before "ข้อเดียว"
dip(T("bye", 0), T("box", -0.05), 0.3)
dip(T("choice", 0), T("choice", -0.3), 0.5)
boost = np.ones(N, np.float32)  # the action plays with the music up
a0, a1 = T("uncle", 0.4), T("dash", -0.05)
boost += 0.4 * (np.clip((t - a0) / 0.3, 0, 1) * np.clip((a1 - t) / 0.2, 0, 1)).astype(np.float32)
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

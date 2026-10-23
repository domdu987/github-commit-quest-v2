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
HIT2 = 0.5


def code(k, t, g=1.0):
    return [(k, t + d, "knock", g) for d in CODE]


CUES = [
    # cold open: the torch clicks on, the fridge seal pops, cold air hisses — the door slammed shut
    ("hook", 0.05, "click", 0.8), *beats("hook", 0.3, D["hook"] - 0.3, 0.6, 0.6), ("hook", frag("hook", 0, 2), "creak", 0.6), ("hook", frag("hook", 0, 2) + 0.05, "pop", 0.4),
    ("hook", frag("hook", 0, 2) + 0.15, "hiss", 0.35), ("hook", vo_t("hook", 1) - 0.05, "slam", 1.3), ("hook", vo_t("hook", 1), "sting", 0.9), ("hook", vo_t("hook", 1), "boom", 0.6),
    ("hook", vo_t("hook", 1), "glitch", 0.5), ("hook", -0.25, "whoosh", 0.8),
    ("chapter", 0.0, "click", 0.6), ("chapter", 0.05, "whoosh", 0.5), ("chapter", 0.3, "glitch", 0.35), ("chapter", 0.67, "sting", 0.5),
    ("hungry", 0.2, "rustle", 0.5),
    ("slam", 0.0, "slam", 1.0), ("slam", 0.05, "pop", 0.3),
    *[("note", t, "marker", 0.7) for t in (0.1, 0.4, frag("note", 0, 1) - 0.1, frag("note", 0, 1) + 0.25, frag("note", 1, 1) - 0.05, frag("note", 1, 1) + 0.3)],
    *beats("sleeve", frag("sleeve", 0, 1), D["sleeve"] - frag("sleeve", 0, 1), 0.5, 0.5), ("sleeve", frag("sleeve", 0, 1), "sting", 0.5),
    ("veins", 0.1, "riser", 0.5), *beats("veins", 0.0, D["veins"], 0.45, 0.7), ("veins", frag("veins", 0, 1), "sting", 0.9), ("veins", frag("veins", 0, 1), "glitch", 0.5), ("veins", 0.4, "squish", 0.3),
    ("caught", 0.05, "rustle", 0.7), ("caught", frag("caught", 0, 1), "sting", 0.8), ("caught", frag("caught", 0, 1), "boom", 0.4),
    *[("decide", frag("decide", 0, 2) + k * 0.45, "stomp", 0.35) for k in range(3)],
    ("plead", vo_t("plead", 1) - 0.05, "sting", 0.7), ("plead", vo_t("plead", 1) + 0.1, "pop", 0.5), ("plead", vo_t("plead", 1) + 0.1, "glitch", 0.3),
    ("hear", 0.0, "wind", 0.25), ("hear", vo_t("hear", 1), "knock", 0.4), ("hear", frag("hear", 1, 1) - 0.1, "growl", 0.9), ("hear", frag("hear", 1, 1), "growl", 0.6),
    ("hear", frag("hear", 1, 1) - 0.1, "sting", 0.9), ("hear", frag("hear", 1, 1) - 0.1, "glitch", 0.5), *beats("hear", 0.0, D["hear"], 0.5, 0.6),
    *code("code", vo_end("code") + 0.05, 1.0),
    ("floor20", 0.0, "click", 0.5), *[("floor20", 0.15 + k * 0.4, "stomp", 0.3) for k in range(3)], *beats("floor20", 0.0, D["floor20"], 0.55, 0.45),
    # action: the mirror, the swing, the glass, the box, the stairs, the code on the door
    *beats("mirror", 0.0, D["mirror"], 0.4, 0.7), ("mirror", 0.7, "growl", 0.7), ("mirror", 1.2, "creak", 0.4), ("mirror", 1.5, "riser", 0.6),
    ("turn", 0.45, "shriek", 1.0), ("turn", 0.5, "sting", 1.0), ("turn", 0.5, "glitch", 0.5), ("turn", 0.3, "steps", 0.8),
    ("hit", 0.25, "whoosh", 0.9), ("hit", HIT2, "clang", 1.3), ("hit", HIT2, "boom", 0.8), ("hit", HIT2, "glitch", 0.5), ("hit", HIT2 + 0.3, "growl", 0.6),
    ("glass", 0.0, "shatter", 1.4), ("glass", 0.0, "boom", 0.7), ("glass", 0.32, "scream", 0.6), ("glass", 0.32, "squish", 0.6), ("glass", 0.32, "sting", 0.8),
    ("kit", 0.35, "rustle", 0.8), ("kit", 0.45, "steps", 1.0), ("kit", 0.6, "shriek", 0.6),
    ("runup", 0.0, "steps", 1.0), ("runup", 0.65, "steps", 0.9), ("runup", 0.3, "growl", 0.9), ("runup", 0.9, "shriek", 0.7), ("runup", 0.2, "riser", 0.8), *beats("runup", 0.0, D["runup"], 0.3, 0.6),
    *code("back", 0.1, 1.1), ("back", 1.15, "rustle", 0.6), ("back", 1.35, "latch", 0.9), ("back", D["back"] - 0.08, "boom", 0.7), *beats("back", 0.0, D["back"], 0.3, 0.6),
    ("bleed", 0.0, "thud", 0.8), *[("bleed", 0.6 + k * 0.7, "drip", 0.7) for k in range(3)], *beats("bleed", 0.0, D["bleed"], 0.4, 0.6),
    ("five", frag("five", 0, 1) - 0.05, "sting", 0.8), ("five", frag("five", 0, 1) - 0.05, "beep", 0.6), *[("five", frag("five", 0, 1) + 0.95 + k, "tick", 0.5) for k in range(2)], *beats("five", 0.0, D["five"], 0.32, 0.8),
    ("press", frag("press", 0, 1) - 0.1, "squish", 0.7), ("press", frag("press", 0, 1) - 0.1, "thud", 0.5), *[("press", 0.3 + k, "tick", 0.45) for k in range(3)], *beats("press", 0.0, D["press"], 0.36, 0.6),
    ("real", frag("real", 0, 1) - 0.1, "pop", 0.5), ("real", frag("real", 0, 2) - 0.05, "pop", 0.5), *[("real", 0.3 + k, "tick", 0.35) for k in range(4)],
    ("stops", frag("stops", 0, 1), "ding", 0.6), ("stops", frag("stops", 0, 1), "swell", 0.4),
    ("gone", 0.3, "crickets", 0.25), ("gone", frag("gone", 0, 1), "creak", 0.7), ("gone", frag("gone", 0, 1), "sting", 0.8), *beats("gone", 0.0, D["gone"], 0.5, 0.6),
    ("peep", 0.2, "growl", 0.5), ("peep", 1.3, "growl", 0.4), *beats("peep", 0.0, D["peep"], 0.45, 0.6),
    ("ignore", 0.5, "growl", 0.7), ("ignore", 0.8, "hiss", 0.3), ("ignore", 1.45, "sting", 1.0), ("ignore", 1.45, "glitch", 0.6), ("ignore", 1.45, "boom", 0.5), *beats("ignore", 0.0, D["ignore"], 0.4, 0.8),
    ("sig", 0.05, "glitch", 0.35), ("sig", 0.05, "beep", 0.35),
    ("sig", frag("sig", 0, 0) + 0.3, "ding", 0.6), ("sig", frag("sig", 0, 0) + 0.62, "ding", 0.6), ("sig", frag("sig", 0, 1) + 0.15, "ding", 0.6),
    ("sig", frag("sig", 0, 2), "glitch", 0.45), *beats("sig", frag("sig", 0, 2), frag("sig", 0, 3) - frag("sig", 0, 2), 0.38, 0.8),
    *[("sig", frag("sig", 0, 2) + o, "tick", 0.55 + 0.1 * k) for k, o in enumerate((0.1, 0.42, 0.68, 0.88, 1.02, 1.12))],  # ticking that speeds up into the cross
    ("sig", frag("sig", 0, 3) - 1.1, "riser", 0.6),
    ("sig", frag("sig", 0, 3), "sting", 1.1), ("sig", frag("sig", 0, 3), "boom", 0.8), ("sig", frag("sig", 0, 3), "glitch", 0.7), ("sig", frag("sig", 0, 3) + 0.12, "slam", 0.7),
    *beats("sig", frag("sig", 0, 3), D["sig"] - frag("sig", 0, 3), 0.5, 0.7),
    *bed("crickets", T("three", 0), T("knock", 0.2), 0.25, 5.0), *[("three", 0.3 + k, "tick", 0.3) for k in range(2)], ("three", frag("three", 0, 1), "swell", 0.3),
    *code("knock", 0.05, 1.1), *code("knock", frag("knock", 0, 1) + 0.1, 1.2), ("knock", frag("knock", 0, 1), "sting", 1.0), ("knock", frag("knock", 0, 1), "boom", 0.6), ("knock", frag("knock", 0, 1), "glitch", 0.5),
    *beats("knock", 0.0, D["knock"], 0.4, 0.8),
    *code("choice", 0.2, 1.0), *beats("choice", 0.0, D["choice"] - 0.3, 0.38, 1.0), *[("choice", 0.05 + k * 1.0, "tick", 1.0) for k in range(3)], ("choice", 1.0, "glitch", 0.6),
    ("choice", D["choice"] - 0.62, "creak", 0.9),
    ("next", 0.3, "buzz", 0.5), ("next", 0.42, "slam", 0.6), ("next", 0.42, "glitch", 0.35), ("next", 0.85, "sting", 0.7), ("next", 0.9, "squish", 0.4), *beats("next", 0.9, D["next"] - 0.9, 0.7, 0.5),
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


dip(0.0, T("hook", -0.1), 0.15, 0.05)                    # the cold open: the fridge, a heartbeat
dip(T("veins", 0), T("caught", -0.1), 0.35)
dip(T("hear", 0), T("hear", -0.1), 0.2)                    # the dark corridor: near silence
dip(T("code", 0), T("code", -0.05), 0.3)
dip(T("floor20", 0), T("mirror", 1.5), 0.25)               # the gym: quiet until it moves
dip(T("gone", 0), T("ignore", -0.05), 0.3)
dip(T("sig", frag("sig", 0, 2)), T("sig", frag("sig", 0, 3) + 0.05), 0.05, 0.12)  # silence before "ข้อเดียว"
dip(T("three", 0), T("knock", -0.05), 0.2)
dip(T("choice", 0), T("choice", -0.3), 0.5)
boost = np.ones(N, np.float32)  # the action plays with the music up
a0, a1 = T("mirror", 1.5), T("back", -0.05)
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

"""Build the episode soundtrack from schedule.json (เอาชีวิตรอด 99 วัน EP.5): per-line levelled voice, synthesized SFX
(cicadas in the noon heat, the pickup and its last cough, footsteps on hot asphalt, the fall, water poured on cloth and the cardboard fan,
the lunge under the bridge, the station at dusk, the rifle, the radio) and the Suno music bed with dips and sidechain ducking under the voice.
Output -14 LUFS, hard cut to silence at the cliffhanger, only the end card's own sounds after it."""
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


# ---- voice: every line levelled on its own so shouts and the child's line sit at a readable loudness ----
LINE_GAIN = {"r01": -2, "g01": -1, "d10": -1, "d13": -1, "s01": 0}
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


def growls(k, a, b, g=0.7, step=0.7):
    return [(k, a + i * step, "growl", g * (0.7 + 0.3 * (i % 2))) for i in range(int((b - a) / step))]


CUES = [
    # cold open: the white-hot road, cicadas, the bottle sloshing; "อย่ารอให้หิวน้ำ"
    *bed("cicada", T("hook", 0), T("hook", -0.1), 0.45, 5.0), *bed("wind", T("hook", 0), T("hook", -0.1), 0.2, 3.2), *[("hook", 0.3 + k * 0.55, "steps", 0.35) for k in range(10)],
    ("hook", vo_t("hook", 1) - 0.2, "whoosh", 0.4), *[("hook", vo_t("hook", 1) + 0.6 + k * 0.32, "drip", 0.35) for k in range(4)],
    ("hook", vo_t("hook", 2), "sting", 1.0), ("hook", vo_t("hook", 2), "boom", 0.6), ("hook", vo_t("hook", 2), "glitch", 0.5), ("hook", frag("hook", 2, 1), "slam", 0.4), *beats("hook", vo_t("hook", 1), D["hook"] - vo_t("hook", 1), 0.5, 0.55), ("hook", -0.25, "whoosh", 0.8),
    # the board; the pickup
    ("chapter", 0.05, "page", 0.9), ("chapter", 0.4, "rustle", 0.5), ("chapter", 0.5, "slam", 0.5), *[("chapter", 0.9 + k * 0.16, "pop", 0.4) for k in range(2)], ("chapter", frag("chapter", 0, 1) + 0.3, "buzz", 0.5), ("chapter", frag("chapter", 0, 1) + 0.3, "sting", 0.6),
    *bed("wind", T("pack", 0), T("wave", -0.1), 0.25, 3.2), ("pack", 0.3, "rustle", 0.5), ("pack", 1.2, "thud", 0.4), ("pack", 2.2, "thud", 0.4), ("pack", frag("pack", 0, 1) - 0.1, "pop", 0.5), ("pack", frag("pack", 0, 1), "marker", 0.4), ("pack", frag("pack", 0, 2) - 0.1, "pop", 0.5), ("pack", frag("pack", 0, 2), "marker", 0.4), ("pack", vo_t("pack", 1) + 0.6, "engine", 0.35),
    # seen from the fence: the pickup going away; "ลุงหมานค่ะ" — the gap
    *bed("engine", T("wave", 0), T("wave", vo_t("wave", 2) - 0.6), 0.3, 4.0), *bed("cicada", T("wave", 0), T("wave", -0.1), 0.25, 5.0), ("wave", vo_t("wave", 2) - 0.1, "whoosh", 0.5), ("wave", vo_t("wave", 2) + 0.2, "glitch", 0.6), ("wave", vo_t("wave", 2) + 0.25, "sting", 0.9), ("wave", vo_t("wave", 2) + 0.3, "boom", 0.4), *beats("wave", vo_t("wave", 2), D["wave"] - vo_t("wave", 2), 0.6, 0.5), ("wave", -0.9, "wind", 0.4),
    # the highway from above, from the side: the engine, the slow dead
    *bed("engine", T("highway", 0), T("empty", vo_t("empty", 0) + 1.3), 0.4, 4.0), *bed("cicada", T("highway", 0), T("signs", -0.1), 0.35, 5.0), ("highway", 0.2, "whoosh", 0.5), ("highway", frag("highway", 1, 1), "page", 0.5), ("highway", frag("highway", 1, 1) + 0.3, "slam", 0.4), *growls("highway", vo_t("highway", 1), D["highway"], 0.35, 1.0),
    # the needle at E; the cough; the bridge; the sign
    *[("empty", 0.2 + k * 0.4, "beep", 0.3) for k in range(int(vo_t("empty", 1) / 0.4))], ("empty", frag("empty", 0, 1) - 0.1, "sputter", 0.9), ("empty", frag("empty", 0, 1) + 0.4, "powerdown", 0.8), ("empty", frag("empty", 0, 1), "sting", 0.8), ("empty", frag("empty", 0, 1), "boom", 0.4), ("empty", vo_t("empty", 1) - 0.1, "slam", 0.4), ("empty", vo_t("empty", 1) + 0.3, "creak", 0.4),
    # the walk: steps, the heat, the thermometer
    *[("walk", 0.2 + k * 0.62, "steps", 0.45) for k in range(14)], ("walk", frag("walk", 0, 1) - 0.1, "pop", 0.5), ("walk", frag("walk", 0, 1) + 0.8, "buzz", 0.5), ("walk", frag("walk", 1, 2), "sting", 0.5), ("walk", vo_t("walk", 2), "rustle", 0.4), *beats("walk", 0.0, D["walk"], 0.65, 0.35),
    ("rule", vo_t("rule", 0) - 0.1, "page", 0.6), ("rule", vo_t("rule", 0) + 0.2, "slam", 0.45), ("rule", frag("rule", 0, 1), "sting", 0.6), ("rule", frag("rule", 1, 1), "ding", 0.5), ("rule", 0.5, "drip", 0.3), ("rule", 1.2, "drip", 0.3),
    # the sway; the fall; the signs
    *bed("hum", T("confuse", 0), T("confuse", frag("confuse", 1, 1)), 0.35, 3.0), ("confuse", 0.3, "riser", 0.5), *[("confuse", 0.3 + k * 0.7, "steps", 0.4) for k in range(5)], ("confuse", frag("confuse", 1, 1) + 0.45, "thud", 1.0), ("confuse", frag("confuse", 1, 1) + 0.45, "boom", 0.6), ("confuse", frag("confuse", 1, 1) + 0.45, "sting", 0.9), ("confuse", frag("confuse", 1, 1) + 0.5, "scream", 0.35), *beats("confuse", 0.0, D["confuse"], 0.6, 0.55),
    *[("signs", t, "pop", 0.5) for t in (vo_t("signs", 0) + 0.1, frag("signs", 0, 1), frag("signs", 0, 2), frag("signs", 0, 2) + 0.6)], *[("signs", t + 0.2, "marker", 0.35) for t in (vo_t("signs", 0) + 0.1, frag("signs", 0, 1), frag("signs", 0, 2), frag("signs", 0, 2) + 0.6)],
    ("signs", vo_t("signs", 0) + 0.3, "slam", 0.4), ("signs", vo_t("signs", 1) - 0.05, "page", 0.6), ("signs", frag("signs", 1, 1), "sting", 0.9), ("signs", frag("signs", 1, 1), "boom", 0.5), ("signs", frag("signs", 2, 1), "glitch", 0.5), ("signs", frag("signs", 2, 1), "buzz", 0.5), *growls("signs", 1.0, D["signs"], 0.3, 1.3), *beats("signs", 0.0, D["signs"], 0.45, 0.65),
    # into the shade; the bottle; "อย่า"
    *bed("wind", T("shade", 0), T("real", -0.1), 0.18, 3.2), *bed("cicada", T("shade", 0), T("real", -0.1), 0.15, 5.0), *[("shade", 0.1 + k * 0.35, "rustle", 0.5) for k in range(6)], *beats("shade", 0.0, D["shade"], 0.55, 0.5),
    *[("nodrink", 0.1 + k * 0.28, "steps", 0.5) for k in range(5)], ("nodrink", vo_t("nodrink", 1), "slam", 0.4), ("nodrink", vo_t("nodrink", 2) - 0.1, "page", 0.6), ("nodrink", vo_t("nodrink", 2) + 0.2, "slam", 0.45), ("nodrink", frag("nodrink", 2, 1), "sting", 0.8), ("nodrink", frag("nodrink", 2, 1), "boom", 0.4), *beats("nodrink", 0.0, D["nodrink"], 0.55, 0.5),
    # the cooling cloths: the decision, the pour, the cloths, the fan, the recipe
    ("craft", vo_t("craft", 0), "pop", 0.4), ("craft", vo_t("craft", 1) + 0.1, "pop", 0.5), ("craft", vo_t("craft", 1) + 0.3, "marker", 0.4), ("craft", vo_t("craft", 1) + 0.5, "slam", 0.45),
    ("craft", vo_t("craft", 2) + 0.1, "page", 0.8), ("craft", vo_t("craft", 2) + 0.5, "slam", 0.5), ("craft", frag("craft", 2, 0) - 0.1, "stream", 0.6), *[("craft", frag("craft", 2, 0) + 0.2 + k * 0.3, "drip", 0.4) for k in range(4)],
    *[("craft", frag("craft", 2, 1) + o, "squish", 0.35) for o in (0.0, 0.45, 0.9, 1.3)], *[("craft", frag("craft", 2, 1) + o, "pop", 0.4) for o in (0.05, 0.5)],
    *[("craft", vo_t("craft", 3) + k * 0.32, "whoosh", 0.3) for k in range(int((D["craft"] - vo_t("craft", 3)) / 0.32))], ("craft", vo_t("craft", 3), "pop", 0.45),
    ("craft", vo_t("craft", 4) - 0.5, "riser", 0.6), ("craft", vo_t("craft", 4), "slam", 0.9), ("craft", vo_t("craft", 4), "sting", 0.7), ("craft", vo_t("craft", 4) + 0.3, "ding", 0.5), ("craft", vo_t("craft", 4) + 0.5, "page", 0.4), *beats("craft", 0.0, D["craft"], 0.6, 0.35),
    # under the bridge: something under the car; the lunge; the spear
    ("lunge", frag("lunge", 0, 1) - 0.2, "zbreath", 0.7), ("lunge", frag("lunge", 0, 1) - 0.1, "riser", 0.8), *growls("lunge", frag("lunge", 0, 1), vo_t("lunge", 0) + 2.2, 0.6, 0.5), ("lunge", frag("lunge", 0, 1) + 0.4, "sting", 0.7),
    ("lunge", vo_t("lunge", 0) + 2.2, "shriek", 1.0), ("lunge", vo_t("lunge", 0) + 2.25, "riser", 0.8), ("lunge", vo_t("lunge", 1) - 0.15, "boom", 0.7),
    ("lunge", vo_t("lunge", 1) + 0.2, "squelch", 0.8), ("lunge", vo_t("lunge", 1) + 0.2, "clang", 0.6), ("lunge", vo_t("lunge", 1) + 0.2, "sting", 1.0), ("lunge", vo_t("lunge", 1) + 0.25, "thud", 0.8), ("lunge", frag("lunge", 1, 1), "slam", 0.4), *beats("lunge", 0.0, D["lunge"], 0.38, 0.8),
    # waking; real life
    ("wake", frag("wake", 0, 1), "ding", 0.5), ("wake", frag("wake", 0, 1), "swell", 0.5), ("wake", vo_t("wake", 1) + 0.2, "drip", 0.4), ("wake", vo_t("wake", 1) + 0.6, "drip", 0.3),
    ("real", frag("real", 0, 1) - 0.1, "page", 0.6), ("real", frag("real", 0, 1) + 0.2, "slam", 0.5), ("real", frag("real", 1, 2), "ding", 0.5), ("real", frag("real", 1, 2), "pop", 0.5),
    # dusk at the station; the chain; the glint
    *bed("crickets", T("station", 0), T("radio", -0.1), 0.25, 4.0), *bed("wind", T("station", 0), T("sig", -0.1), 0.2, 3.2), *[("station", 0.2 + k * 0.6, "steps", 0.4) for k in range(7)], ("station", vo_t("station", 1), "hum", 0.3), ("station", frag("station", 2, 1), "clang", 0.6), ("station", frag("station", 2, 1), "sting", 0.8), ("station", frag("station", 2, 1), "boom", 0.4), *beats("station", 0.0, D["station"], 0.55, 0.45),
    ("roof", 0.4, "ching", 0.7), ("roof", 0.2, "pop", 0.5), ("roof", 0.4, "slam", 0.45), ("roof", frag("roof", 0, 1), "sting", 0.8), ("roof", frag("roof", 0, 1), "boom", 0.4), *beats("roof", 0.0, D["roof"], 0.45, 0.65),
    # the rifle; hands up; nothing is free
    ("gun", 0.1, "click", 0.9), ("gun", 0.3, "latch", 0.8), ("gun", frag("gun", 0, 1), "sting", 1.0), ("gun", frag("gun", 0, 1), "boom", 0.6), ("gun", frag("gun", 0, 1), "glitch", 0.5), ("gun", vo_t("gun", 1) - 0.1, "rustle", 0.5), ("gun", vo_t("gun", 2) - 0.1, "click", 0.5), ("gun", frag("gun", 2, 1), "sting", 0.8), ("gun", frag("gun", 2, 1), "slam", 0.4), *beats("gun", 0.0, D["gun"], 0.4, 0.75),
    # the signature
    ("sig", 0.05, "glitch", 0.35), ("sig", 0.05, "beep", 0.35),
    ("sig", frag("sig", 0, 0) + 0.3, "ding", 0.6), ("sig", frag("sig", 0, 0) + 0.62, "buzz", 0.6), ("sig", frag("sig", 0, 1) + 0.15, "ding", 0.6),
    ("sig", frag("sig", 0, 2), "glitch", 0.45), *beats("sig", frag("sig", 0, 2), frag("sig", 0, 3) - frag("sig", 0, 2), 0.38, 0.8),
    *[("sig", frag("sig", 0, 2) + o, "tick", 0.55 + 0.1 * k) for k, o in enumerate((0.1, 0.42, 0.68, 0.88, 1.02, 1.12))],
    ("sig", frag("sig", 0, 3) - 1.1, "riser", 0.6),
    ("sig", frag("sig", 0, 3), "sting", 1.1), ("sig", frag("sig", 0, 3), "boom", 0.8), ("sig", frag("sig", 0, 3), "glitch", 0.7), ("sig", frag("sig", 0, 3) + 0.12, "slam", 0.7),
    *beats("sig", frag("sig", 0, 3), D["sig"] - frag("sig", 0, 3), 0.5, 0.7),
    # the radio: 94… five; the guard hears it too; the torch; the name
    *bed("crickets", T("radio", 0), T("choice", -0.3), 0.25, 4.0), ("radio", vo_t("radio", 0) - 0.4, "radio", 1.0), *bed("radiobed", T("radio", vo_t("radio", 0) - 0.1), T("radio", vo_end("radio", 0) + 0.3), 0.5, 3.0),
    ("radio", frag("radio", 0, 1), "tick", 0.5), ("radio", frag("radio", 0, 1), "rustle", 0.6), ("radio", vo_end("radio", 0) + 0.3, "static", 0.5), ("radio", frag("radio", 0, 2), "sting", 0.9), ("radio", frag("radio", 0, 2), "slam", 0.6), ("radio", frag("radio", 0, 2), "glitch", 0.4),
    ("radio", frag("radio", 2, 1), "sting", 0.7), ("radio", frag("radio", 2, 1), "buzz", 0.4), *beats("radio", vo_t("radio", 0), D["radio"] - vo_t("radio", 0), 0.5, 0.5),
    ("name", 0.2, "click", 0.6), ("name", 0.25, "whoosh", 0.4), ("name", frag("name", 0, 1), "sting", 0.8), ("name", frag("name", 1, 1), "sting", 1.0), ("name", frag("name", 1, 1), "boom", 0.6), ("name", frag("name", 1, 1), "glitch", 0.6), *beats("name", 0.0, D["name"], 0.42, 0.75),
    ("drawing", 0.1, "crayon", 0.6), ("drawing", 0.9, "crayon", 0.5), ("drawing", frag("drawing", 0, 1), "riser", 0.4), ("drawing", frag("drawing", 1, 1), "sting", 0.9), ("drawing", frag("drawing", 1, 1), "boom", 0.5), ("drawing", frag("drawing", 1, 1), "glitch", 0.5), *beats("drawing", frag("drawing", 0, 1), D["drawing"] - frag("drawing", 0, 1), 0.55, 0.5),
    *beats("choice", 0.0, D["choice"] - 0.3, 0.38, 1.0), *[("choice", 0.05 + k * 1.0, "tick", 1.0) for k in range(3)], ("choice", 1.0, "glitch", 0.6), ("choice", 1.0, "radio", 0.5),
    ("choice", D["choice"] - 2.2, "riser", 1.0), ("choice", D["choice"] - 0.62, "sting", 1.0), ("choice", D["choice"] - 0.6, "glitch", 0.8), ("choice", D["choice"] - 0.6, "boom", 0.7),
    ("next", 0.3, "page", 0.9), ("next", 0.6, "marker", 0.35), ("next", 1.0, "marker", 0.35), ("next", 1.45, "sting", 0.6), ("next", 1.9, "glitch", 0.3), *beats("next", 1.2, D["next"] - 1.2, 0.7, 0.5),
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


dip(0.0, T("hook", -0.1), 0.25, 0.05)
dip(T("wave", vo_t("wave", 2) - 0.2), T("wave", -0.05), 0.25)
dip(T("confuse", frag("confuse", 1, 1)), T("signs", 0.5), 0.35)
dip(T("lunge", frag("lunge", 0, 1) - 0.2), T("lunge", vo_t("lunge", 0) + 2.2), 0.25)
dip(T("gun", 0), T("gun", -0.05), 0.4)
dip(T("sig", frag("sig", 0, 2)), T("sig", frag("sig", 0, 3) + 0.05), 0.05, 0.12)
dip(T("radio", vo_t("radio", 0) - 0.4), T("radio", vo_end("radio", 0) + 0.3), 0.15)
dip(T("name", 0), T("name", -0.05), 0.35)
dip(T("drawing", frag("drawing", 0, 1)), T("drawing", -0.05), 0.35)
dip(T("choice", 0), T("choice", -0.3), 0.5)
boost = np.ones(N, np.float32)  # the action plays with the music up
for a0, a1 in ((T("lunge", vo_t("lunge", 0) + 2.2), T("lunge", -0.05)), (T("craft", vo_t("craft", 4) - 0.5), T("craft", vo_t("craft", 4) + 1.5))):
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

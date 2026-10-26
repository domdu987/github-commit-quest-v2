"""Build the episode soundtrack from schedule.json (เอาชีวิตรอด 99 วัน EP.2): per-line levelled voice, synthesized SFX
(chalk on the board, cicadas at noon, the can dropping, the horde, the gate on its rail, the sickle, the radio waking,
the ledger page) and the Suno music bed with dips before the scares and sidechain ducking under the voice.
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
LINE_GAIN = {"r01": -2, "d05": -1, "d07": -1, "d08": -1}
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
    # cold open: the cord, the engine coughs and catches, the bulb, the fan; "อย่าเปิดในห้อง" hits
    ("hook", 0.35, "cord", 0.9), *bed("engine", T("hook", 0.9), T("hook", -0.1), 0.5, 4.3), ("hook", frag("hook", 1, 1) - 0.3, "bulb", 0.9), *bed("fan", T("hook", frag("hook", 1, 1)), T("hook", -0.1), 0.35, 2.8),
    ("hook", vo_t("hook", 2), "sting", 1.0), ("hook", vo_t("hook", 2), "boom", 0.6), ("hook", vo_t("hook", 2), "glitch", 0.5), ("hook", frag("hook", 2, 1), "slam", 0.5), *beats("hook", 0.3, D["hook"] - 0.3, 0.55, 0.6), ("hook", -0.25, "whoosh", 0.8),
    # the page, the tank; the register
    ("chapter", 0.05, "page", 0.9), ("chapter", 0.4, "rustle", 0.5), ("chapter", 0.5, "slam", 0.5), *[("chapter", 0.9 + k * 0.16, "pop", 0.4) for k in range(2)], ("chapter", frag("chapter", 0, 1) + 0.4, "buzz", 0.5), ("chapter", frag("chapter", 0, 1) + 0.4, "sting", 0.5),
    *bed("wind", T("roster", 0), T("gate", -0.1), 0.25, 3.2), ("roster", 0.2, "page", 0.8), ("roster", 0.55, "slam", 0.5),
    *[c for k, at in enumerate((frag("roster", 1, 0), frag("roster", 1, 1), frag("roster", 2, 0), frag("roster", 2, 1), vo_end("roster", 2) + 0.1)) for c in (("roster", at, "pop", 0.5), ("roster", at + 0.15, "marker", 0.35), ("roster", at + 0.35, "slam", 0.45))],
    # the map, the gate
    ("map", 0.15, "whoosh", 0.5), *[("map", 0.15 + 0.2 * k, "pop", 0.5) for k in range(2)], ("map", frag("map", 0, 1) + 0.3, "pop", 0.6), ("map", frag("map", 0, 1) + 0.4, "marker", 0.5), ("map", frag("map", 0, 2), "ding", 0.4),
    ("gate", 0.2, "page", 0.5), ("gate", 0.3, "gate", 0.5), ("gate", 0.4, "steps", 0.3), ("gate", 0.35, "tick", 0.4),
    # the fair: cicadas, the cart's wheels, the one under the wheel
    *bed("cicada", T("fair", 0), T("fairRun", -0.1), 0.9, 4.6), ("fair", 0.3, "creak", 0.4), ("fair", 1.6, "creak", 0.35), ("fair", 3.0, "creak", 0.35), ("fair", frag("fair", 0, 1) - 0.1, "zbreath", 0.6), ("fair", frag("fair", 0, 1), "sting", 0.8), ("fair", frag("fair", 0, 1) + 0.1, "growl", 0.7),
    ("fairRun", 0.05, "shriek", 1.0), ("fairRun", 0.1, "steps", 0.8), ("fairRun", 0.55, "clang", 1.0), ("fairRun", 0.58, "cans", 0.6), ("fairRun", 0.58, "boom", 0.5), ("fairRun", 0.6, "thud", 0.8), ("fairRun", 0.9, "steps", 0.9), ("fairRun", 1.4, "steps", 0.9), ("fairRun", 1.9, "steps", 0.8), ("fairRun", 0.7, "riser", 0.6), *beats("fairRun", 0.0, D["fairRun"], 0.35, 0.8),
    # back at the gate: wheels, the gate, the jerrycan; inside: the generator set down
    *bed("wind", T("back", 0), T("back", -0.1), 0.3, 3.2), ("back", 0.2, "gate", 0.6), ("back", 0.5, "creak", 0.4), ("back", 1.6, "creak", 0.4), ("back", frag("back", 0, 1), "pop", 0.5), *[("back", frag("back", 0, 1) + 0.12 * k, "tick", 0.3) for k in range(5)], ("back", frag("back", 1, 1), "ding", 0.5),
    *bed("crickets", T("inside", 0), T("drag", -0.1), 0.45, 4.6), ("inside", 0.3, "thud", 0.6), ("inside", 0.35, "clang", 0.4), ("inside", vo_t("inside", 1), "creak", 0.3),
    # the start: the cord, the engine, the bulb, the fan; the room with the engine running under everything
    ("start", 0.2, "cord", 1.0), *bed("engine", T("start", 0.8), T("drag", 0.35), 0.45, 4.3), ("start", frag("start", 0, 0) + 0.2, "bulb", 1.0), ("start", frag("start", 0, 0) + 0.45, "sting", 0.5), *bed("fan", T("start", frag("start", 0, 0) + 0.6), T("drag", 0.35), 0.3, 2.8),
    ("fan", 0.2, "page", 0.5), *[("fan", 0.4 + k * 0.17, "tick", 0.25) for k in range(16)],
    ("smoke", 0.3, "hiss", 0.35), ("smoke", 1.8, "hiss", 0.3), ("smoke", frag("smoke", 0, 1), "sting", 0.6), ("smoke", vo_t("smoke", 1) + 0.2, "cough", 0.7), *beats("smoke", frag("smoke", 0, 1), D["smoke"] - frag("smoke", 0, 1), 0.6, 0.45),
    ("dizzy", frag("dizzy", 0, 1), "sting", 0.5), ("dizzy", frag("dizzy", 0, 1), "buzz", 0.4), *beats("dizzy", 0.0, D["dizzy"], 0.55, 0.5),
    ("co", frag("co", 0, 0) + 0.2, "page", 0.6), ("co", frag("co", 0, 0) + 0.5, "slam", 0.5), ("co", frag("co", 0, 1), "pop", 0.5), ("co", frag("co", 0, 2), "sting", 1.0), ("co", frag("co", 0, 2), "boom", 0.6), ("co", frag("co", 0, 2), "glitch", 0.5), *beats("co", 0.0, D["co"], 0.45, 0.6),
    ("collapse", frag("collapse", 0, 1), "thud", 1.0), ("collapse", frag("collapse", 0, 1), "sting", 0.9), ("collapse", frag("collapse", 0, 1), "boom", 0.5), ("collapse", vo_t("collapse", 1), "slam", 0.4), *beats("collapse", frag("collapse", 0, 1), D["collapse"] - frag("collapse", 0, 1), 0.35, 0.85),
    ("drag", 0.35, "powerdown", 0.9), ("drag", 0.35, "slam", 0.5), ("drag", 0.5, "creak", 0.7), ("drag", 0.6, "gate", 0.5), ("drag", 0.4, "steps", 0.9), ("drag", 0.9, "steps", 0.9), ("drag", 1.4, "steps", 0.8), ("drag", 0.3, "riser", 0.6), *beats("drag", 0.0, D["drag"], 0.33, 0.85),
    # outside at night: in real life; she wakes
    *bed("crickets", T("real", 0), T("wake", -0.1), 0.5, 4.6), ("real", frag("real", 0, 1), "page", 0.6), ("real", frag("real", 0, 1) + 0.3, "slam", 0.5), ("real", frag("real", 1, 1), "ding", 0.5), ("real", frag("real", 1, 1), "pop", 0.5),
    ("wake", frag("wake", 0, 1), "ding", 0.4), ("wake", frag("wake", 0, 1) + 0.1, "cough", 0.5), *beats("wake", 0.0, frag("wake", 0, 1), 0.5, 0.5),
    # the yard: the engine out in the open, the bulb; the map of sound
    *bed("crickets", T("yard", 0), T("count2", 2.5), 0.4, 4.6), ("yard", 0.3, "cord", 0.8), *bed("engine", T("yard", 0.9), T("count", 2.4), 0.55, 4.3), ("yard", frag("yard", 0, 1) + 0.2, "bulb", 0.8),
    ("yard", vo_t("yard", 1), "whoosh", 0.5), *[("yard", frag("yard", 1, 1) + k * 0.35, "buzz", 0.5) for k in range(3)], ("yard", frag("yard", 1, 1), "sting", 0.7), ("yard", frag("yard", 1, 1), "glitch", 0.3),
    # they come; "ยี่สิบวิ"
    *bed("horde", T("horde", 0.3), T("count2", 2.5), 0.6, 4.6), *growls("horde", 0.3, D["horde"], 0.6, 0.7), ("horde", frag("horde", 0, 1), "sting", 0.9), ("horde", frag("horde", 0, 1), "boom", 0.5), ("horde", vo_t("horde", 1) + 1.6, "slam", 0.4), *beats("horde", 0.0, D["horde"], 0.45, 0.7),
    # the countdown: a tick every second, the switch, the sickle, the run, the door
    ("count", 0.2, "page", 0.7), ("count", 0.45, "slam", 0.5), *[("count", 0.2 + 0.53 * (k + 1), "tick", 0.75) for k in range(14)], *beats("count", 0.2, D["count"] - 0.2, 0.6, 0.6), *growls("count", 0.5, D["count"], 0.5, 0.9),
    ("count", 0.2, "steps", 0.6), ("count", 0.8, "steps", 0.6), ("count", 1.9, "pop", 0.5), ("count", 2.1, "slam", 0.45), ("count", 2.4, "latch", 0.9), ("count", 2.4, "powerdown", 0.8),
    ("count", 3.0, "steps", 0.6), ("count", 3.6, "steps", 0.6), ("count", 4.5, "rustle", 0.8), ("count", 4.6, "shriek", 0.9), ("count", 5.2, "sparks", 1.0), ("count", 5.2, "clang", 0.8), ("count", 5.25, "sting", 0.8), ("count", 5.6, "thud", 0.5),
    *[("count", 6.0 + k * 0.33, "steps", 0.6) for k in range(6)], ("count", -0.3, "riser", 0.8),
    *growls("count2", 0.0, D["count2"] - 1.5, 0.7, 0.5), *[("count2", 0.5 * (k + 1), "tick", 1.0) for k in range(5)], *beats("count2", 0.0, 2.5, 0.3, 0.9), *[("count2", 0.5 * (k + 1), "sting", 0.35) for k in range(4)],
    *[("count2", 0.15 + k * 0.3, "steps", 0.8) for k in range(7)], ("count2", 2.15, "shriek", 0.8), ("count2", 2.5, "slam", 1.3), ("count2", 2.5, "boom", 0.9), ("count2", 2.55, "gate", 0.8), ("count2", 2.75, "latch", 1.0), ("count2", 3.0, "thud", 0.6),
    # dark: twenty minutes; the hill
    *bed("crickets", T("dark", 0), T("sig", -0.1), 0.45, 4.6), *bed("horde", T("dark", 0), T("dark", -0.1), 0.35, 4.6), ("dark", 0.5, "page", 0.5), *[("dark", 0.6 + k * 0.1, "tick", 0.3) for k in range(10)], ("dark", frag("dark", 0, 1), "buzz", 0.5),
    ("hill", frag("hill", 0, 1), "riser", 0.5), *[("hill", frag("hill", 0, 1) + 0.2 + o, "beep", 0.35) for o in (0, 0.45, 0.9)], ("hill", frag("hill", 0, 2), "sting", 0.8), ("hill", frag("hill", 1, 1), "sting", 0.7), ("hill", frag("hill", 1, 1), "glitch", 0.4), *beats("hill", frag("hill", 0, 1), D["hill"] - frag("hill", 0, 1), 0.5, 0.55),
    # the signature
    ("sig", 0.05, "glitch", 0.35), ("sig", 0.05, "beep", 0.35),
    ("sig", frag("sig", 0, 0) + 0.3, "ding", 0.6), ("sig", frag("sig", 0, 0) + 0.62, "ding", 0.6), ("sig", frag("sig", 0, 1) + 0.15, "ding", 0.6),
    ("sig", frag("sig", 0, 2), "glitch", 0.45), *beats("sig", frag("sig", 0, 2), frag("sig", 0, 3) - frag("sig", 0, 2), 0.38, 0.8),
    *[("sig", frag("sig", 0, 2) + o, "tick", 0.55 + 0.1 * k) for k, o in enumerate((0.1, 0.42, 0.68, 0.88, 1.02, 1.12))],
    ("sig", frag("sig", 0, 3) - 1.1, "riser", 0.6),
    ("sig", frag("sig", 0, 3), "sting", 1.1), ("sig", frag("sig", 0, 3), "boom", 0.8), ("sig", frag("sig", 0, 3), "glitch", 0.7), ("sig", frag("sig", 0, 3) + 0.12, "slam", 0.7),
    *beats("sig", frag("sig", 0, 3), D["sig"] - frag("sig", 0, 3), 0.5, 0.7),
    # the radio: 97… six; switched off, still counting
    *bed("crickets", T("radio", 0), T("drawing", -0.1), 0.45, 4.6), ("radio", vo_t("radio", 1) - 0.35, "radio", 1.0), *bed("radiobed", T("radio", vo_t("radio", 1) - 0.1), T("radio", vo_end("radio", 1) + 0.3), 0.5, 3.0),
    ("radio", frag("radio", 1, 1), "tick", 0.5), ("radio", frag("radio", 1, 1), "rustle", 0.6), ("radio", vo_end("radio", 1) + 0.3, "static", 0.5), *beats("radio", vo_t("radio", 1), D["radio"] - vo_t("radio", 1), 0.5, 0.5),
    ("radio", frag("radio", 1, 2), "sting", 0.7), ("radio", frag("radio", 1, 2), "slam", 0.6), ("radio", vo_t("radio", 2) + 0.5, "click", 0.9), ("radio", frag("radio", 3, 1), "static", 0.6), ("radio", frag("radio", 3, 1), "sting", 0.9), ("radio", frag("radio", 3, 1), "glitch", 0.6), ("radio", frag("radio", 3, 1), "buzz", 0.5),
    ("drawing", 0.1, "crayon", 0.6), ("drawing", 0.9, "crayon", 0.5), ("drawing", frag("drawing", 0, 1), "sting", 0.6), ("drawing", frag("drawing", 0, 1) + 0.2, "riser", 0.4), ("drawing", frag("drawing", 1, 1), "sting", 0.9), ("drawing", frag("drawing", 1, 1), "boom", 0.5), ("drawing", frag("drawing", 1, 1), "glitch", 0.5), *beats("drawing", frag("drawing", 0, 1), D["drawing"] - frag("drawing", 0, 1), 0.55, 0.5),
    # morning: the man at the gate; the choice
    *bed("wind", T("morning", 0), T("choice", -0.3), 0.3, 3.2), ("morning", 0.2, "steps", 0.4), ("morning", 0.9, "steps", 0.4), ("morning", frag("morning", 0, 1), "sting", 0.8), ("morning", frag("morning", 0, 1), "boom", 0.5), ("morning", frag("morning", 1, 1), "sting", 1.0), ("morning", frag("morning", 1, 1), "glitch", 0.6), ("morning", frag("morning", 1, 1), "boom", 0.6), *beats("morning", frag("morning", 0, 1), D["morning"] - frag("morning", 0, 1), 0.45, 0.6),
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


dip(0.0, T("hook", -0.1), 0.2, 0.05)
dip(T("start", 0), T("fan", -0.05), 0.5)
dip(T("smoke", 0), T("co", frag("co", 0, 2)), 0.35)
dip(T("real", 0), T("wake", -0.05), 0.4)
dip(T("count", 0), T("count2", 2.5), 0.5)
dip(T("sig", frag("sig", 0, 2)), T("sig", frag("sig", 0, 3) + 0.05), 0.05, 0.12)
dip(T("radio", vo_t("radio", 1) - 0.4), T("radio", vo_end("radio", 1) + 0.3), 0.15)
dip(T("drawing", frag("drawing", 1, 0)), T("drawing", -0.05), 0.35)
dip(T("choice", 0), T("choice", -0.3), 0.5)
boost = np.ones(N, np.float32)  # the action plays with the music up
for a0, a1 in ((T("fairRun", 0), T("fairRun", -0.05)), (T("drag", 0), T("drag", -0.05)), (T("horde", 0), T("count2", 2.5))):
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

"""Build the episode soundtrack from schedule.json (เอาชีวิตรอด 99 วัน EP.4): per-line levelled voice, synthesized SFX
(rain and thunder, the crying from the dark, the craft bench, the fence going over, the horde in the mud, the bar on the door, the radio,
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
LINE_GAIN = {"r01": -2, "l01": -4, "w01": -3, "d07": -1, "d09": -1, "d10": -1, "d11": -1, "d13": -1}
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
    # cold open: rain, thunder, the crying out there, the pulse; "อย่าเพิ่งออกไป"
    *bed("rain", T("hook", 0), T("hook", -0.1), 0.55, 4.0), ("hook", 0.6, "thunder", 0.6), ("hook", vo_t("hook", 1) + 1.2, "thunder", 0.7), ("hook", vo_t("hook", 1) - 0.2, "static", 0.25),
    ("hook", vo_t("hook", 2), "sting", 1.0), ("hook", vo_t("hook", 2), "boom", 0.6), ("hook", vo_t("hook", 2), "glitch", 0.5), ("hook", frag("hook", 2, 1), "slam", 0.5), *beats("hook", vo_t("hook", 1), D["hook"] - vo_t("hook", 1), 0.5, 0.6), ("hook", -0.25, "whoosh", 0.8),
    # the page; the yard: the stock-keeper, the knife, the runner
    ("chapter", 0.05, "page", 0.9), ("chapter", 0.4, "rustle", 0.5), ("chapter", 0.5, "slam", 0.5), *[("chapter", 0.9 + k * 0.16, "pop", 0.4) for k in range(2)], ("chapter", frag("chapter", 0, 1) + 0.3, "buzz", 0.5), ("chapter", frag("chapter", 0, 1) + 0.3, "sting", 0.6),
    *bed("wind", T("ask", 0), T("run", -0.1), 0.25, 3.2), ("ask", vo_t("ask", 1) + 0.2, "pop", 0.5), ("ask", vo_t("ask", 1) + 0.35, "marker", 0.4), ("ask", vo_t("ask", 1) + 0.55, "slam", 0.45), ("ask", frag("ask", 1, 2), "sting", 0.5), ("ask", frag("ask", 1, 2), "buzz", 0.3),
    ("phuKnife", 0.5, "ching", 0.8), ("phuKnife", 0.55, "sting", 0.6), ("phuKnife", frag("phuKnife", 1, 1), "sting", 0.6), ("phuKnife", frag("phuKnife", 1, 1), "slam", 0.4), *beats("phuKnife", 0.5, D["phuKnife"] - 0.5, 0.55, 0.45),
    ("run", 0.3, "pop", 0.5), ("run", 0.45, "marker", 0.4), ("run", 0.65, "slam", 0.45), *[("run", 0.2 + k * 0.32, "steps", 0.6) for k in range(9)], ("run", 0.2, "riser", 0.4),
    # the bench: three parts, the slam, the steel, the sparks
    ("craft", 0.3, "page", 0.9), ("craft", 0.7, "slam", 0.5), *[c for at in (frag("craft", 0, 0) + 0.1, frag("craft", 0, 1) + 0.1, frag("craft", 0, 2) + 0.1) for c in (("craft", at, "pop", 0.55), ("craft", at + 0.15, "marker", 0.4), ("craft", at + 0.35, "slam", 0.45))],
    ("craft", frag("craft", 0, 0), "thud", 0.5), ("craft", frag("craft", 0, 1) + 0.7, "ching", 0.7), ("craft", frag("craft", 0, 1) + 0.7, "clang", 0.35), *[("craft", frag("craft", 0, 2) + 0.25 + k * 0.3, "rustle", 0.55) for k in range(3)],
    ("craft", frag("craft", 1, 0) - 0.5, "riser", 0.8), ("craft", frag("craft", 1, 0), "slam", 1.0), ("craft", frag("craft", 1, 0), "boom", 0.6), ("craft", frag("craft", 1, 0), "sting", 0.9), ("craft", frag("craft", 1, 0) + 0.15, "whoosh", 0.6), ("craft", frag("craft", 1, 0) + 0.3, "ding", 0.5),
    ("craft", frag("craft", 2, 1), "pop", 0.5), ("craft", frag("craft", 2, 1) + 0.2, "marker", 0.4), ("craft", frag("craft", 2, 0) + 0.2, "pop", 0.5), ("craft", frag("craft", 2, 0) + 0.55, "slam", 0.45),
    ("craft", frag("craft", 3, 0) - 0.5, "riser", 0.7), ("craft", frag("craft", 3, 0) - 0.3, "sparks", 0.9), ("craft", frag("craft", 3, 0), "clang", 1.0), ("craft", frag("craft", 3, 0), "sparks", 1.0), ("craft", frag("craft", 3, 0), "sting", 0.9), ("craft", frag("craft", 3, 0), "glitch", 0.4), ("craft", frag("craft", 3, 0) + 0.3, "ding", 0.5), ("craft", frag("craft", 3, 0) + 0.1, "slam", 0.6),
    ("loud", frag("loud", 0, 1), "clang", 0.5), ("loud", frag("loud", 0, 1), "page", 0.5), ("loud", frag("loud", 0, 1) + 0.3, "slam", 0.4), ("loud", frag("loud", 0, 1), "sting", 0.5),
    # the rain comes; they run in it
    *bed("rain", T("rain", 0.4), T("count2", 2.5), 0.5, 4.0), ("rain", frag("rain", 0, 1), "thunder", 0.8), ("rain", frag("rain", 1, 0) - 0.1, "page", 0.6), ("rain", frag("rain", 1, 0) + 0.2, "slam", 0.5), ("rain", frag("rain", 1, 1), "thunder", 0.9), ("rain", frag("rain", 1, 1), "sting", 0.8), ("rain", frag("rain", 1, 1) + 0.1, "growl", 0.5), *beats("rain", vo_t("rain", 1), D["rain"] - vo_t("rain", 1), 0.5, 0.5),
    # the crying in the night; the gate; the trap card
    ("cry", 0.3, "thunder", 0.5), ("cry", vo_t("cry", 0) - 0.2, "static", 0.3), ("cry", vo_t("cry", 1), "rustle", 0.4), ("cry", vo_t("cry", 2) + 0.2, "clang", 0.4), ("cry", vo_t("cry", 3) - 0.1, "gate", 0.3), ("cry", frag("cry", 4, 1), "sting", 0.7), ("cry", frag("cry", 4, 1), "slam", 0.5), ("cry", frag("cry", 5, 1), "sting", 0.5), ("cry", frag("cry", 5, 1), "glitch", 0.3), *beats("cry", 0.0, D["cry"], 0.55, 0.5),
    ("peek", 0.2, "gate", 0.7), ("peek", 0.5, "creak", 0.5), ("peek", frag("peek", 0, 1), "static", 0.4), ("peek", frag("peek", 0, 1) + 0.1, "click", 0.6), ("peek", frag("peek", 1, 0) + 0.1, "thunder", 1.0), ("peek", frag("peek", 1, 0), "riser", 0.8), *growls("peek", vo_t("peek", 1), D["peek"], 0.7, 0.4), ("peek", frag("peek", 1, 1), "shriek", 1.0), ("peek", frag("peek", 1, 1), "sting", 0.9), ("peek", frag("peek", 1, 1), "boom", 0.6), *beats("peek", frag("peek", 0, 1), D["peek"] - frag("peek", 0, 1), 0.4, 0.7),
    *bed("horde", T("trap", 0), T("count2", 2.5), 0.55, 4.6), ("trap", 0.2, "page", 0.7), ("trap", 0.5, "slam", 0.5), ("trap", frag("trap", 0, 1), "sting", 0.9), ("trap", frag("trap", 0, 1), "glitch", 0.5), ("trap", frag("trap", 0, 1), "boom", 0.5), *[("trap", 0.2 + k * 0.9, "beep", 0.25) for k in range(3)], *beats("trap", 0.0, D["trap"], 0.45, 0.6),
    # the fence goes over; the lunge; the run; the rebar
    *growls("fenceFall", 0.0, D["fenceFall"], 0.7, 0.5), *[("fenceFall", frag("fenceFall", 1, 0) - 1.6 + k * 0.16, "clang", 0.45) for k in range(9)], ("fenceFall", frag("fenceFall", 1, 0), "creak", 1.0), ("fenceFall", frag("fenceFall", 1, 0) + 0.2, "riser", 0.8),
    ("fenceFall", frag("fenceFall", 1, 0) + 0.55, "boom", 1.0), ("fenceFall", frag("fenceFall", 1, 0) + 0.55, "clang", 1.0), ("fenceFall", frag("fenceFall", 1, 0) + 0.55, "thud", 0.9), ("fenceFall", frag("fenceFall", 1, 0) + 0.6, "thunder", 0.8), ("fenceFall", frag("fenceFall", 1, 0) + 0.6, "sting", 1.0), ("fenceFall", frag("fenceFall", 1, 0) + 0.6, "glitch", 0.6),
    ("fenceFall", D["fenceFall"] - 1.0, "zbreath", 0.7), ("fenceFall", D["fenceFall"] - 0.95, "riser", 0.8), ("fenceFall", D["fenceFall"] - 0.1, "shriek", 1.0), ("fenceFall", D["fenceFall"] - 0.1, "boom", 0.6), *beats("fenceFall", 0.0, D["fenceFall"], 0.36, 0.8),
    ("flee", 0.05, "slam", 0.4), *[("flee", 0.1 + k * 0.28, "steps", 0.8) for k in range(14)], *growls("flee", 0.0, D["flee"], 0.6, 0.6), ("flee", vo_t("flee", 1), "thud", 1.0), ("flee", vo_t("flee", 1), "sparks", 0.6), ("flee", vo_t("flee", 1), "sting", 0.9), ("flee", vo_t("flee", 1), "boom", 0.5), ("flee", vo_t("flee", 1) + 0.1, "scream", 0.5), ("flee", 0.0, "riser", 0.6), *beats("flee", 0.0, D["flee"], 0.33, 0.85),
    ("cover", 0.8, "clang", 0.7), ("cover", 1.5, "clang", 0.6), ("cover", 2.3, "squelch", 0.5), *growls("cover", 0.0, D["cover"], 0.6, 0.6), *[("cover", 1.0 + k * 0.5, "steps", 0.6) for k in range(5)], ("cover", 2.35, "slam", 0.4), ("cover", 2.65, "sting", 0.6), *beats("cover", 0.0, D["cover"], 0.4, 0.7),
    # the countdown: a tick a second; the thrusts; the thunder; the door and the bar
    ("count", 0.2, "page", 0.7), ("count", 0.45, "slam", 0.5), *[("count", 0.2 + 0.55 * (k + 1), "tick", 0.75) for k in range(14)], *beats("count", 0.2, D["count"] - 0.2, 0.55, 0.6), *growls("count", 0.3, D["count"], 0.55, 0.7),
    *[c for t in (1.0, 2.2, 3.4, 4.6) for c in (("count", t, "clang", 0.8), ("count", t, "squelch", 0.4), ("count", t + 0.05, "shriek", 0.4))], ("count", 5.2, "thunder", 0.7), ("count", 7.4, "thunder", 0.8), ("count", 5.0, "creak", 0.7), ("count", frag("count", 1, 2), "sting", 0.9), ("count", frag("count", 1, 2), "glitch", 0.5), ("count", frag("count", 1, 2), "boom", 0.5), ("count", -0.3, "riser", 0.8),
    *growls("count2", 0.0, D["count2"] - 1.5, 0.6, 0.5), *[("count2", 0.5 * (k + 1), "tick", 1.0) for k in range(5)], *beats("count2", 0.0, 2.5, 0.3, 0.9), *[("count2", 0.5 * (k + 1), "sting", 0.35) for k in range(4)], ("count2", vo_t("count2", 0), "static", 0.3),
    ("count2", 2.05, "creak", 0.9), ("count2", 2.5, "slam", 1.3), ("count2", 2.5, "boom", 0.9), ("count2", 2.5, "thud", 0.8), ("count2", 2.65, "latch", 1.0), ("count2", 2.7, "clang", 0.6),
    # black: the knocks, then nothing; the tourniquet
    ("after", 0.15, "thud", 0.9), ("after", 0.4, "thud", 0.8), ("after", 0.9, "thud", 0.7), ("after", 1.3, "growl", 0.4), *bed("rain", T("after", 0), T("real", -0.1), 0.25, 4.0), ("after", frag("after", 0, 1), "sting", 0.7), ("after", frag("after", 0, 1), "slam", 0.4), *beats("after", 0.0, D["after"], 0.6, 0.4),
    ("tq", 0.3, "drip", 0.4), ("tq", 1.2, "drip", 0.4), ("tq", frag("tq", 0, 2), "sting", 0.6), ("tq", vo_t("tq", 1) + 0.2, "rustle", 0.6), ("tq", vo_t("tq", 1) + 0.6, "snap", 0.5), *[("tq", vo_t("tq", 1) + 0.8 + k * 0.28, "creak", 0.35) for k in range(6)], ("tq", vo_t("tq", 2) - 0.1, "page", 0.6), ("tq", vo_t("tq", 2) + 0.2, "slam", 0.45), ("tq", frag("tq", 2, 1), "pop", 0.4), ("tq", frag("tq", 2, 2) + 0.1, "marker", 0.6), ("tq", frag("tq", 2, 2) + 0.1, "ding", 0.4), ("tq", frag("tq", 3, 1), "ding", 0.4), *beats("tq", 0.0, D["tq"], 0.55, 0.45),
    ("real", frag("real", 0, 1), "page", 0.6), ("real", frag("real", 0, 1) + 0.3, "slam", 0.5), ("real", frag("real", 0, 2), "ding", 0.5), ("real", frag("real", 0, 2), "pop", 0.5),
    # the signature
    ("sig", 0.05, "glitch", 0.35), ("sig", 0.05, "beep", 0.35),
    ("sig", frag("sig", 0, 0) + 0.3, "ding", 0.6), ("sig", frag("sig", 0, 0) + 0.62, "buzz", 0.6), ("sig", frag("sig", 0, 1) + 0.15, "ding", 0.6),
    ("sig", frag("sig", 0, 2), "glitch", 0.45), *beats("sig", frag("sig", 0, 2), frag("sig", 0, 3) - frag("sig", 0, 2), 0.38, 0.8),
    *[("sig", frag("sig", 0, 2) + o, "tick", 0.55 + 0.1 * k) for k, o in enumerate((0.1, 0.42, 0.68, 0.88, 1.02, 1.12))],
    ("sig", frag("sig", 0, 3) - 1.1, "riser", 0.6),
    ("sig", frag("sig", 0, 3), "sting", 1.1), ("sig", frag("sig", 0, 3), "boom", 0.8), ("sig", frag("sig", 0, 3), "glitch", 0.7), ("sig", frag("sig", 0, 3) + 0.12, "slam", 0.7),
    *beats("sig", frag("sig", 0, 3), D["sig"] - frag("sig", 0, 3), 0.5, 0.7),
    # the radio: 95… five; the ledger
    *bed("rain", T("radio", 0), T("ledger", -0.1), 0.2, 4.0), ("radio", vo_t("radio", 0) - 0.4, "radio", 1.0), *bed("radiobed", T("radio", vo_t("radio", 0) - 0.1), T("radio", vo_end("radio", 0) + 0.3), 0.5, 3.0),
    ("radio", frag("radio", 0, 1), "tick", 0.5), ("radio", frag("radio", 0, 1), "rustle", 0.6), ("radio", vo_end("radio", 0) + 0.3, "static", 0.5), ("radio", frag("radio", 0, 2), "sting", 0.9), ("radio", frag("radio", 0, 2), "slam", 0.6), ("radio", frag("radio", 0, 2), "glitch", 0.4), ("radio", frag("radio", 1, 1), "buzz", 0.5), ("radio", frag("radio", 1, 1), "sting", 0.7), *beats("radio", vo_t("radio", 0), D["radio"] - vo_t("radio", 0), 0.5, 0.5),
    ("ledger", 0.2, "page", 0.6), ("ledger", 0.4, "marker", 0.4), ("ledger", 1.0, "clang", 0.3),
    # dawn: the box; the second radio; the drawing; the choice
    *bed("wind", T("dawn", 0), T("walkie", -0.1), 0.3, 3.2), ("dawn", 0.3, "steps", 0.4), ("dawn", 1.0, "steps", 0.4), ("dawn", 1.7, "steps", 0.4), ("dawn", vo_t("dawn", 1) + 0.6, "snap", 0.5), ("dawn", vo_t("dawn", 1) + 0.9, "rustle", 0.5), ("dawn", frag("dawn", 1, 1), "sting", 0.6), *beats("dawn", vo_t("dawn", 1), D["dawn"] - vo_t("dawn", 1), 0.5, 0.5),
    ("walkie", 0.1, "static", 0.6), ("walkie", 0.2, "beep", 0.4), *[("walkie", 0.2 + k * 0.5, "beep", 0.2) for k in range(1, 5)], ("walkie", vo_end("walkie", 0) + 0.1, "static", 0.4), ("walkie", frag("walkie", 1, 1), "sting", 1.0), ("walkie", frag("walkie", 1, 1), "boom", 0.6), ("walkie", frag("walkie", 1, 1), "glitch", 0.6), ("walkie", frag("walkie", 1, 1) + 0.05, "buzz", 0.5), *beats("walkie", 0.0, D["walkie"], 0.45, 0.6),
    ("drawing", 0.1, "crayon", 0.6), ("drawing", 0.9, "crayon", 0.5), ("drawing", frag("drawing", 0, 1), "riser", 0.4), ("drawing", frag("drawing", 0, 2), "sting", 0.9), ("drawing", frag("drawing", 0, 2), "boom", 0.5), ("drawing", frag("drawing", 0, 2), "glitch", 0.5), *beats("drawing", frag("drawing", 0, 1), D["drawing"] - frag("drawing", 0, 1), 0.55, 0.5),
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
dip(T("craft", frag("craft", 1, 0) - 0.5), T("craft", frag("craft", 1, 0) + 0.6), 0.3, 0.1)
dip(T("craft", frag("craft", 3, 0) - 0.5), T("craft", frag("craft", 3, 0) + 0.6), 0.3, 0.1)
dip(T("cry", 0), T("cry", vo_t("cry", 1)), 0.25)
dip(T("peek", 0), T("peek", vo_t("peek", 1)), 0.3)
dip(T("count", 0), T("count2", 2.5), 0.5)
dip(T("after", 0), T("after", -0.05), 0.15)
dip(T("sig", frag("sig", 0, 2)), T("sig", frag("sig", 0, 3) + 0.05), 0.05, 0.12)
dip(T("radio", vo_t("radio", 0) - 0.4), T("radio", vo_end("radio", 0) + 0.3), 0.15)
dip(T("walkie", 0), T("walkie", vo_end("walkie", 0)), 0.25)
dip(T("drawing", frag("drawing", 0, 1)), T("drawing", -0.05), 0.35)
dip(T("choice", 0), T("choice", -0.3), 0.5)
boost = np.ones(N, np.float32)  # the action plays with the music up
for a0, a1 in ((T("run", 0), T("run", -0.05)), (T("peek", vo_t("peek", 1)), T("count", 0)), (T("craft", frag("craft", 1, 0) - 0.5), T("craft", frag("craft", 1, 0) + 1.5))):
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

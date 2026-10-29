"""Build the episode soundtrack from schedule.json (เอาชีวิตรอด 99 วัน EP.3): per-line levelled voice, synthesized SFX
(the gate on its rail, water poured on a wound, cloth torn, the rusted blade, the lunge at the bars, the radio waking,
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
LINE_GAIN = {"r01": -2, "d03": -1, "d09": -1, "d10": -1}
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
    # cold open: wind, his hand on the bar, the knock of a bar; "อย่าเพิ่งเปิดประตู" hits
    *bed("wind", T("hook", 0), T("hook", -0.1), 0.35, 3.2), ("hook", vo_t("hook", 1) - 0.3, "rustle", 0.6), ("hook", vo_t("hook", 1) + 0.5, "clang", 0.35), ("hook", vo_t("hook", 1) + 0.9, "clang", 0.3),
    ("hook", vo_t("hook", 2), "sting", 1.0), ("hook", vo_t("hook", 2), "boom", 0.6), ("hook", vo_t("hook", 2), "glitch", 0.5), ("hook", frag("hook", 2, 1), "slam", 0.5), *beats("hook", 0.3, D["hook"] - 0.3, 0.55, 0.6), ("hook", -0.25, "whoosh", 0.8),
    # the page; six
    ("chapter", 0.05, "page", 0.9), ("chapter", 0.4, "rustle", 0.5), ("chapter", 0.5, "slam", 0.5), *[("chapter", 0.9 + k * 0.16, "pop", 0.4) for k in range(2)], ("chapter", frag("chapter", 0, 1), "pop", 0.4), ("chapter", frag("chapter", 0, 2) + 0.3, "buzz", 0.5), ("chapter", frag("chapter", 0, 2) + 0.3, "sting", 0.6),
    # the rule, the gate, the plea
    *bed("wind", T("rule", 0), T("plea", -0.1), 0.25, 3.2), ("rule", vo_t("rule", 1) - 0.3, "page", 0.8), ("rule", vo_t("rule", 1) + 0.05, "slam", 0.5), ("rule", frag("rule", 1, 1), "sting", 0.5), ("rule", frag("rule", 1, 1), "marker", 0.4),
    ("gate", 0.1, "steps", 0.7), ("gate", 0.5, "steps", 0.7), ("gate", 0.9, "clang", 0.5), ("gate", vo_t("gate", 1), "slam", 0.3), *beats("gate", 0.0, D["gate"], 0.5, 0.5),
    ("plea", 0.4, "rustle", 0.5), ("plea", 0.5, "cough", 0.4), ("plea", frag("plea", 1, 1), "page", 0.5), ("plea", frag("plea", 1, 1) + 0.3, "slam", 0.4), ("plea", frag("plea", 1, 1), "sting", 0.5),
    # the search: the checklist ticks; the leg
    *bed("wind", T("search", 0), T("knife", -0.1), 0.25, 3.2), ("search", frag("search", 0, 0) + 0.3, "rustle", 0.6), *[c for at in (frag("search", 0, 0) + 0.5, frag("search", 0, 0) + 1.3, frag("search", 0, 1) + 0.3) for c in (("search", at, "pop", 0.5), ("search", at + 0.3, "marker", 0.4), ("search", at + 0.5, "ding", 0.35))],
    ("search", frag("search", 0, 1) + 0.15, "rustle", 0.5), ("search", frag("search", 1, 2), "pop", 0.5), ("search", frag("search", 1, 2) + 0.3, "slam", 0.6), ("search", frag("search", 1, 2), "sting", 0.7), *beats("search", 0.0, D["search"], 0.6, 0.4),
    ("wound", 0.2, "whoosh", 0.3), ("wound", frag("wound", 0, 2), "marker", 0.6), ("wound", frag("wound", 0, 2), "sting", 0.7), ("wound", frag("wound", 0, 2), "buzz", 0.3), *beats("wound", 0.0, D["wound"], 0.6, 0.4),
    # the knife through the bars
    ("knife", 0.3, "rustle", 0.4), ("knife", frag("knife", 0, 1), "page", 0.5), ("knife", frag("knife", 0, 1) + 0.3, "slam", 0.4), ("knife", 1.2, "ching", 0.5), ("knife", frag("knife", 1, 1), "ching", 0.8), ("knife", frag("knife", 1, 1), "sting", 0.9), ("knife", frag("knife", 1, 1), "glitch", 0.4), ("knife", frag("knife", 1, 1) + 0.1, "buzz", 0.5), *beats("knife", 0.0, D["knife"], 0.5, 0.5),
    # he cuts the cloth; the gate rolls
    *[("open", 0.2 + k * 0.28, "saw", 0.35) for k in range(4)], ("open", vo_end("open", 0) + 0.3, "gate", 1.0), ("open", vo_end("open", 0) + 0.35, "creak", 0.5), ("open", vo_end("open", 0) + 1.0, "steps", 0.4), ("open", vo_end("open", 0) + 1.6, "steps", 0.4), ("open", vo_end("open", 0) + 2.2, "steps", 0.35), ("open", vo_end("open", 0) + 2.6, "latch", 0.6), *beats("open", 0.0, D["open"], 0.55, 0.45),
    # the wash: water, the cloth, the wrap
    *bed("cicada", T("wash", 0), T("real", -0.1), 0.5, 4.6), ("wash", 0.3, "stream", 0.8), ("wash", 1.6, "stream", 0.6), ("wash", frag("wash", 1, 1), "rustle", 0.5), ("wash", frag("wash", 1, 1) + 0.6, "squelch", 0.3), ("wash", frag("wash", 1, 2) + 0.2, "rustle", 0.6), ("wash", frag("wash", 1, 2) + 0.4, "snap", 0.4), ("wash", vo_t("wash", 1), "page", 0.5), ("wash", vo_t("wash", 1) + 0.3, "slam", 0.4), ("wash", frag("wash", 1, 2), "ding", 0.4),
    ("ledger", 0.2, "page", 0.6), ("ledger", 0.4, "marker", 0.4), ("ledger", vo_t("ledger", 0) + 0.3, "buzz", 0.5), ("ledger", vo_t("ledger", 0) + 0.3, "sting", 0.4),
    # the blade: the rust, the one on the road, the lunge, the cut
    ("blade", 0.1, "steps", 0.4), ("blade", 0.6, "steps", 0.4), ("blade", 1.2, "rustle", 0.4), ("blade", frag("blade", 0, 2), "page", 0.5), ("blade", frag("blade", 0, 2) + 0.3, "slam", 0.4), ("blade", frag("blade", 0, 2), "sting", 0.5), *growls("blade", 0.5, D["blade"] - 1.0, 0.35, 0.9),
    ("blade", D["blade"] - 1.0, "zbreath", 0.7), ("blade", D["blade"] - 0.95, "riser", 0.8), ("blade", D["blade"] - 0.1, "shriek", 1.0), ("blade", D["blade"] - 0.1, "clang", 0.9), ("blade", D["blade"] - 0.1, "boom", 0.6), *beats("blade", D["blade"] - 1.0, 1.0, 0.3, 0.9),
    ("cut", 0.05, "sparks", 0.7), ("cut", 0.05, "sting", 1.0), ("cut", 0.05, "boom", 0.5), ("cut", 0.05, "glitch", 0.4), ("cut", 0.1, "thud", 0.6), ("cut", 0.4, "growl", 0.6), ("cut", 1.0, "growl", 0.4), ("cut", frag("cut", 1, 1), "sting", 0.7), ("cut", frag("cut", 1, 1), "slam", 0.4), *beats("cut", 0.0, D["cut"], 0.36, 0.85),
    ("press", 0.0, "steps", 0.8), ("press", 0.3, "steps", 0.8), ("press", 0.6, "rustle", 0.5), ("press", 0.9, "pop", 0.6), ("press", 1.05, "marker", 0.4), ("press", 1.25, "slam", 0.5), ("press", vo_t("press", 1) + 0.3, "page", 0.5), ("press", vo_t("press", 1) + 0.6, "slam", 0.4), ("press", frag("press", 1, 1), "ding", 0.4), *beats("press", 0.0, D["press"], 0.45, 0.6),
    # tetanus: the card, the lockjaw hit, one in ten
    ("tetanus", frag("tetanus", 0, 1), "page", 0.6), ("tetanus", frag("tetanus", 0, 1) + 0.3, "slam", 0.5), ("tetanus", frag("tetanus", 1, 0), "pop", 0.4), ("tetanus", frag("tetanus", 1, 2), "sting", 1.0), ("tetanus", frag("tetanus", 1, 2), "boom", 0.6), ("tetanus", frag("tetanus", 1, 2), "glitch", 0.5), ("tetanus", vo_t("tetanus", 2), "marker", 0.4), ("tetanus", frag("tetanus", 2, 1), "sting", 0.8), ("tetanus", frag("tetanus", 2, 1), "slam", 0.6), *beats("tetanus", 0.0, D["tetanus"], 0.5, 0.55),
    ("needle", frag("needle", 1, 1), "sting", 0.8), ("needle", frag("needle", 1, 1), "glitch", 0.4), ("needle", frag("needle", 1, 1), "buzz", 0.4), *beats("needle", 0.0, D["needle"], 0.5, 0.5),
    *[c for at in (frag("signs", 0, 1), frag("signs", 0, 1) + 0.55, frag("signs", 0, 2), frag("signs", 1, 0)) for c in (("signs", at, "pop", 0.5), ("signs", at + 0.2, "marker", 0.4), ("signs", at + 0.4, "slam", 0.45))], ("signs", frag("signs", 1, 2), "sting", 0.6), ("signs", frag("signs", 1, 2), "ding", 0.4), *beats("signs", 0.0, D["signs"], 0.6, 0.4),
    ("real", frag("real", 0, 1), "page", 0.6), ("real", frag("real", 0, 1) + 0.3, "slam", 0.5), ("real", frag("real", 0, 2), "ding", 0.5), ("real", frag("real", 0, 2), "pop", 0.5),
    # dusk: the sixth name; the name
    *bed("crickets", T("trust", 0), T("sig", -0.1), 0.4, 4.6), ("trust", 0.3, "page", 0.8), ("trust", 0.7, "slam", 0.5), ("trust", frag("trust", 0, 1), "pop", 0.5), ("trust", frag("trust", 0, 1) + 0.15, "marker", 0.4), ("trust", frag("trust", 0, 1) + 0.35, "slam", 0.45), ("trust", frag("trust", 0, 2), "sting", 0.6), ("trust", frag("trust", 0, 2), "whoosh", 0.4), *beats("trust", frag("trust", 0, 2), D["trust"] - frag("trust", 0, 2), 0.5, 0.5),
    ("name", 0.2, "crayon", 0.4), ("name", 0.9, "crayon", 0.4), ("name", frag("name", 0, 1), "sting", 0.8), ("name", frag("name", 0, 1), "glitch", 0.4), ("name", frag("name", 1, 1), "sting", 0.7), ("name", frag("name", 1, 1), "slam", 0.5), ("name", vo_t("name", 2), "riser", 0.4), ("name", frag("name", 4, 1), "sting", 1.1), ("name", frag("name", 4, 1), "boom", 0.7), ("name", frag("name", 4, 1), "glitch", 0.7), ("name", frag("name", 4, 1) + 0.1, "slam", 0.6), *beats("name", vo_t("name", 1), D["name"] - vo_t("name", 1), 0.42, 0.7),
    # the signature
    # the sheet slaps on and is taped; a red pen ticks each line (with a soft ding); a marker circles the ???
    ("sig", 0.05, "page", 0.8), ("sig", 0.36, "thud", 0.25),
    *[x for o in (frag("sig", 0, 0) + 0.3, frag("sig", 0, 0) + 0.62, frag("sig", 0, 1) + 0.15) for x in (("sig", o, "pen", 0.9), ("sig", o + 0.05, "ding", 0.3))],
    ("sig", frag("sig", 0, 2) + 0.45, "marker", 0.45), *beats("sig", frag("sig", 0, 2), frag("sig", 0, 3) - frag("sig", 0, 2), 0.38, 0.8),
    *[("sig", frag("sig", 0, 2) + o, "tick", 0.55 + 0.1 * k) for k, o in enumerate((0.1, 0.42, 0.68, 0.88, 1.02, 1.12))],
    ("sig", frag("sig", 0, 3) - 1.1, "riser", 0.6),
    # "ข้อเดียว": two red slashes, the page tears across, the strip drops, a stamp hits what is left
    ("sig", frag("sig", 0, 3), "sting", 1.1), ("sig", frag("sig", 0, 3), "boom", 0.7), ("sig", frag("sig", 0, 3), "pen", 1.0), ("sig", frag("sig", 0, 3) + 0.1, "pen", 1.0),
    ("sig", frag("sig", 0, 3) + 0.24, "rip", 1.1), ("sig", frag("sig", 0, 3) + 0.86, "thud", 0.8), ("sig", frag("sig", 0, 3) + 0.86, "slam", 0.35),
    *beats("sig", frag("sig", 0, 3), D["sig"] - frag("sig", 0, 3), 0.5, 0.7),
    # the radio: 96… six; "เราหกคนพอดี"
    *bed("crickets", T("radio", 0), T("drawing", -0.1), 0.45, 4.6), ("radio", vo_t("radio", 1) - 0.35, "radio", 1.0), *bed("radiobed", T("radio", vo_t("radio", 1) - 0.1), T("radio", vo_end("radio", 1) + 0.3), 0.5, 3.0),
    ("radio", frag("radio", 1, 1), "tick", 0.5), ("radio", frag("radio", 1, 1), "rustle", 0.6), ("radio", vo_end("radio", 1) + 0.3, "static", 0.5), *beats("radio", vo_t("radio", 1), D["radio"] - vo_t("radio", 1), 0.5, 0.5),
    ("radio", frag("radio", 1, 2), "sting", 0.7), ("radio", frag("radio", 1, 2), "slam", 0.6), ("radio", vo_t("radio", 2) + 0.5, "click", 0.6), ("radio", frag("radio", 2, 1), "buzz", 0.5), ("radio", frag("radio", 2, 1), "sting", 0.9), ("radio", frag("radio", 2, 1), "glitch", 0.6),
    ("drawing", 0.1, "crayon", 0.6), ("drawing", 0.9, "crayon", 0.5), ("drawing", frag("drawing", 0, 1), "sting", 0.5), ("drawing", frag("drawing", 1, 0), "riser", 0.4), ("drawing", frag("drawing", 1, 2), "sting", 0.9), ("drawing", frag("drawing", 1, 2), "boom", 0.5), ("drawing", frag("drawing", 1, 2), "glitch", 0.5), *beats("drawing", frag("drawing", 0, 1), D["drawing"] - frag("drawing", 0, 1), 0.55, 0.5),
    # 2 a.m.; the knife gone; the choice
    *bed("crickets", T("night", 0), T("choice", -0.3), 0.35, 4.6), *bed("wind", T("night", 0), T("knife2", -0.1), 0.3, 3.2), ("night", 0.8, "zbreath", 0.25), ("night", 2.4, "zbreath", 0.25), ("night", frag("night", 0, 2), "sting", 0.7), ("night", frag("night", 0, 2), "static", 0.3), *beats("night", 0.0, D["night"], 0.5, 0.5),
    ("knife2", 0.2, "whoosh", 0.3), ("knife2", frag("knife2", 0, 1), "sting", 1.0), ("knife2", frag("knife2", 0, 1), "boom", 0.6), ("knife2", frag("knife2", 0, 1), "glitch", 0.6), ("knife2", frag("knife2", 0, 1) + 0.3, "page", 0.5), ("knife2", frag("knife2", 0, 1) + 0.6, "marker", 0.4), *beats("knife2", 0.0, D["knife2"], 0.42, 0.7),
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
dip(T("search", 0), T("wound", -0.05), 0.5)
dip(T("wash", 0), T("wash", -0.05), 0.45)
dip(T("blade", D["blade"] - 1.0), T("cut", -0.05), 0.4)
dip(T("tetanus", frag("tetanus", 1, 2) - 0.1), T("tetanus", frag("tetanus", 1, 2) + 0.5), 0.3, 0.1)
dip(T("name", vo_t("name", 1) - 0.2), T("name", -0.05), 0.35)
dip(T("sig", frag("sig", 0, 2)), T("sig", frag("sig", 0, 3) + 0.05), 0.05, 0.12)
dip(T("radio", vo_t("radio", 1) - 0.4), T("radio", vo_end("radio", 1) + 0.3), 0.15)
dip(T("drawing", frag("drawing", 1, 0)), T("drawing", -0.05), 0.35)
dip(T("night", 0), T("knife2", -0.05), 0.4)
dip(T("choice", 0), T("choice", -0.3), 0.5)
boost = np.ones(N, np.float32)  # the action plays with the music up
for a0, a1 in ((T("gate", 0), T("gate", -0.05)), (T("blade", D["blade"] - 1.0), T("press", 0.9))):
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

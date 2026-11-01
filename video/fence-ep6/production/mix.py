"""Build the episode soundtrack from schedule.json (เอาชีวิตรอด 99 วัน EP.6 "นิคม"): per-line levelled voice, synthesized SFX
(the washroom's drips and hum, the pour and the gas hiss, the coughing, the estate's sliding gate, the register's pen and stamp, the
workshop's collar, rubber and grinder, the canteen, the radio, the gate at midnight) and the Suno music bed with dips and ducking.
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


WP1 = frag("workshop", 0, 1); WP2 = WP1 + 0.75; WB = WP2 + 1.1   # the recipe's collar, rubber and build (shots.part uses the same three)


# ---- voice: every line levelled on its own so shouts and the child's line sit at a readable loudness ----
LINE_GAIN = {"r01": -2, "g01": -1, "d07": -1, "s01": 0}
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


def gasbed(a, b, g, step=2.0, d=3.0):  # overlapping "gas" breaths (3 s each) between absolute times a and b, all faded by b + 0.6
    out, t = [], a - 0.6
    while t + d <= b + 0.6:
        out.append((None, t, "gas", g))
        t += step
    return out


def growls(k, a, b, g=0.7, step=0.7):
    return [(k, a + i * step, "growl", g * (0.7 + 0.3 * (i % 2))) for i in range(int((b - a) / step))]


CUES = [
    # cold open: the filthy washroom — drips, the tube light's hum, the bottles; the pour (as long as the drawn streams: P + 0.4 → "อย่าผสม"); "อย่าผสม" — the cloud
    *bed("hum", T("hook", 0), T("hook", -0.1), 0.25, 3.0), *[("hook", 0.4 + k * 0.9, "drip", 0.35) for k in range(11)], ("hook", 0.25, "rustle", 0.45), ("hook", 0.4, "rustle", 0.4),
    ("hook", frag("hook", 1, 1) - 0.1, "whoosh", 0.4), *[("hook", frag("hook", 1, 1) + o, f"pour@{vo_t('hook', 2) - 0.05 - frag('hook', 1, 1) - o:.2f}", g) for o, g in ((0.25, 0.5), (0.33, 0.37))],
    ("hook", vo_t("hook", 2), "sting", 1.0), ("hook", vo_t("hook", 2), "boom", 0.6), ("hook", vo_t("hook", 2), "glitch", 0.5), ("hook", vo_t("hook", 2) - 0.05, "gasburst", 1.35), ("hook", frag("hook", 2, 1), "slam", 0.4),
    *beats("hook", vo_t("hook", 1), D["hook"] - vo_t("hook", 1), 0.5, 0.55), ("hook", -0.25, "whoosh", 0.8),
    # the board at dawn
    ("chapter", 0.05, "page", 0.9), ("chapter", 0.4, "chalk", 0.5), ("chapter", 0.5, "slam", 0.5), *[("chapter", 0.9 + k * 0.16, "pop", 0.4) for k in range(2)], ("chapter", frag("chapter", 0, 2) + 0.2, "sting", 0.6),
    *bed("wind", T("chapter", 0), T("chapter", -0.1), 0.22, 3.2), *bed("crickets", T("chapter", 0), T("chapter", -0.1), 0.12, 4.0),
    # the six on the verge; the hum of power as the camera reaches the lit fence
    *[("chapter", 0.3 + k * 0.6, "steps", 0.25) for k in range(8)], ("chapter", frag("chapter", 0, 2) - 0.35, "riser", 0.4), *bed("hum", T("chapter", frag("chapter", 0, 2)), T("chapter", -0.1), 0.35, 3.0), ("chapter", frag("chapter", 0, 2) + 0.25, "buzz", 0.3),
    # the gate: the shout, the tower, the gate rolls; the whole yard stares
    *bed("wind", T("gate", 0), T("register", -0.1), 0.18, 3.2), ("gate", 0.35, "latch", 0.5), ("gate", 1.5, "gate", 1.0), ("gate", 2.9, "clang", 0.5),
    ("gate", vo_t("gate", 1) + 0.1, "whoosh", 0.4), ("gate", frag("gate", 1, 1) - 0.1, "sting", 0.8), ("gate", frag("gate", 1, 1), "boom", 0.4), *beats("gate", vo_t("gate", 1), D["gate"] - vo_t("gate", 1), 0.6, 0.55),
    # คุณวิน: his steps, the welcome, the skill card; ปั้น's polaroid
    *[("win", 0.1 + k * 0.45, "steps", 0.35) for k in range(4)], ("win", 1.0, "page", 0.5), ("win", 1.25, "slam", 0.5), ("win", 1.35, "pop", 0.4),
    ("win", vo_t("win", 1) + 0.15, "whoosh", 0.4), ("win", vo_t("win", 1) + 0.45, "page", 0.6), ("win", vo_t("win", 1) + 0.45, "sting", 0.7), *beats("win", vo_t("win", 1), D["win"] - vo_t("win", 1), 0.6, 0.45),
    # the offer: four ticks; then "ทุกคนต้องมีประโยชน์"
    *[x for o in (vo_t("offer", 0), frag("offer", 0, 1), frag("offer", 0, 2), frag("offer", 0, 2) + 0.55) for x in (("offer", o, "pop", 0.45), ("offer", o + 0.35, "pen", 0.45))],
    ("offer", frag("offer", 1, 1) - 0.05, "page", 0.6), ("offer", frag("offer", 1, 1) + 0.25, "slam", 0.6), ("offer", frag("offer", 1, 1), "sting", 0.8), ("offer", frag("offer", 1, 1), "boom", 0.4), *beats("offer", vo_t("offer", 1), D["offer"] - vo_t("offer", 1), 0.6, 0.45),
    # the register: the card flips, a pen for each name; ปั้น — the stamp "รอดู"
    ("register", 0.15, "page", 0.8), ("register", 0.5, "slam", 0.45), *[("register", at + 0.12, "pen", 0.5) for at in (0.6, 1.1, 1.6, 2.1)], *[("register", at + 0.35, "thud", 0.3) for at in (0.6, 1.1, 1.6, 2.1)],
    ("register", vo_end("register", 1) + 0.2, "pen", 0.6), ("register", vo_end("register", 1) + 0.55, "slam", 0.8), ("register", vo_end("register", 1) + 0.55, "sting", 0.7), *beats("register", vo_t("register", 0), D["register"] - vo_t("register", 0), 0.6, 0.45),
    # he knows the school: the pen keeps writing; ครูพิม's look; the rules on the board — "บอกไปแล้ว"
    *[("knows", 0.3 + k * 0.5, "pen", 0.35) for k in range(6)], ("knows", frag("knows", 0, 1), "sting", 0.7), ("knows", vo_t("knows", 1) - 0.1, "whoosh", 0.4), *beats("knows", vo_t("knows", 1), D["knows"] - vo_t("knows", 1), 0.5, 0.6),
    ("knows", vo_t("knows", 2) - 0.05, "page", 0.5), *[("knows", vo_t("knows", 2) + o, "chalk", 0.45) for o in (0.05, 0.3, 0.9)], 
    ("knows", frag("knows", 2, 1), "sting", 1.0), ("knows", frag("knows", 2, 1), "boom", 0.6), ("knows", frag("knows", 2, 1), "glitch", 0.5),
    # the workshop: the recipe, the collar, the rubber, the grinder, the lift; ก้องขออยู่
    ("workshop", 0.2, "page", 0.8), ("workshop", 0.5, "slam", 0.45), *[("workshop", o, "pop", 0.5) for o in (frag("workshop", 0, 0) + 0.25, WP1, WP2)],
    ("workshop", WP1 + 0.1, "clang", 0.7), ("workshop", WP1 + 0.3, "latch", 0.5), *[("workshop", WP2 + 0.1 + k * 0.15, "squish", 0.35) for k in range(6)],
    ("workshop", WB - 0.05, "saw", 0.7), ("workshop", WB + 0.05, "sparks", 0.8), ("workshop", WB + 0.5, "riser", 0.5), ("workshop", WB + 0.55, "slam", 0.9),
    ("workshop", WB + 0.55, "sting", 0.7), ("workshop", WB + 0.85, "ding", 0.5), ("workshop", WB + 0.95, "ching", 0.5), *beats("workshop", 0.0, vo_t("workshop", 1), 0.6, 0.35),
    *bed("hum", T("workshop", vo_t("workshop", 1) - 0.3), T("calm", -0.1), 0.2, 3.0), ("workshop", vo_end("workshop", 1) + 0.15, "sting", 0.4),
    # too quiet: the line of workers, their steps; one old woman (the counter)
    *bed("wind", T("calm", 0), T("calm", -0.1), 0.25, 3.2), *[("calm", 0.2 + k * 0.5, "steps", 0.28) for k in range(13)], ("calm", 1.0, "creak", 0.2), ("calm", frag("calm", 0, 1), "sting", 0.4),
    ("calm", frag("calm", 1, 1) - 0.1, "pop", 0.5), ("calm", frag("calm", 1, 1) + 0.2, "buzz", 0.45), ("calm", frag("calm", 1, 1), "sting", 0.7),
    # the washroom: the brush, the drips; เจ๊หงส์ comes in
    *bed("hum", T("yai", 0), T("out", vo_t("out", 1) - 0.2), 0.22, 3.0), *[("yai", 0.3 + k * 0.85, "drip", 0.3) for k in range(10)], *[("yai", 0.1 + k * 0.55, "squish", 0.3) for k in range(16)], *[("yai", 0.1 + k * 0.4, "steps", 0.3) for k in range(4)],
    # the mix: the pour (one flow, as long as the drawn stream: 0.4 → vo 2 − 0.35), the card (two ✗), the gas starts
    ("mix", 0.4, f"pour@{vo_t('mix', 2) - 0.75:.2f}", 0.55), *[("mix", 0.5 + k * 0.4, "drip", 0.35) for k in range(9)],
    ("mix", vo_t("mix", 1), "page", 0.6), ("mix", vo_t("mix", 1) + 0.35, "pen", 0.7), ("mix", vo_t("mix", 2) + 0.4, "page", 0.4), ("mix", vo_t("mix", 2) + 0.75, "pen", 0.7),
    ("mix", vo_t("mix", 2) - 0.3, "gasburst", 0.9), ("mix", frag("mix", 2, 1), "sting", 0.8), ("mix", frag("mix", 2, 1), "boom", 0.4), *beats("mix", vo_t("mix", 1), D["mix"] - vo_t("mix", 1), 0.55, 0.5),
    # it sinks: the gas spreads along the floor (soft low breaths — the old high-passed "hiss" bed read as static, "เสียงซ่า")
    *gasbed(T("sink", 0), T("out", vo_t("out", 1) - 0.1), 0.45), ("sink", 0.2, "riser", 0.4), ("sink", frag("sink", 0, 1), "page", 0.5), ("sink", frag("sink", 1, 1), "sting", 0.8), ("sink", frag("sink", 1, 1), "boom", 0.4), *beats("sink", 0.0, D["sink"], 0.5, 0.55),
    # the signs: coughing, the checklist, "ถึงตายได้"
    *[("signs", 0.2 + k * 0.62, "cough", 0.55 - 0.1 * (k % 2)) for k in range(12)], *[x for o in (vo_t("signs", 0), frag("signs", 0, 1), frag("signs", 0, 2), frag("signs", 1, 1)) for x in (("signs", o, "pop", 0.45), ("signs", o + 0.35, "marker", 0.35))],
    ("signs", frag("signs", 0, 1) - 0.05, "whoosh", 0.3), ("signs", frag("signs", 0, 2) - 0.05, "whoosh", 0.3),
    ("signs", frag("signs", 1, 3), "sting", 1.0), ("signs", frag("signs", 1, 3), "boom", 0.6), ("signs", frag("signs", 1, 3), "glitch", 0.5), *beats("signs", 0.0, D["signs"], 0.42, 0.75),
    # out: ครูพิม runs in, the door, outside the air; the window shoved open
    *[("out", 0.05 + k * 0.28, "steps", 0.55) for k in range(4)], ("out", 0.15, "scream", 0.15), *[("out", 0.6 + k * 0.45, "cough", 0.5) for k in range(3)], ("out", vo_t("out", 1) - 0.25, "creak", 0.6), ("out", vo_t("out", 1) - 0.15, "slam", 0.5),
    *bed("wind", T("out", vo_t("out", 1) - 0.1), T("watch", vo_t("watch", 1) - 0.2), 0.25, 3.2), ("out", vo_t("out", 1) + 0.4, "creak", 0.5), ("out", vo_t("out", 1) + 0.6, "knock", 0.4), ("out", vo_t("out", 1) + 0.4, "page", 0.5), ("out", vo_t("out", 1) + 0.6, "slam", 0.45),
    *[("out", vo_t("out", 1) + 1.2 + k * 1.3, "cough", 0.25) for k in range(3)], ("out", frag("out", 1, 1), "page", 0.5), ("out", frag("out", 1, 1) + 0.3, "slam", 0.45), *beats("out", 0.0, vo_t("out", 1), 0.36, 0.8),
    # in real life
    ("real", frag("real", 0, 1) - 0.1, "page", 0.6), ("real", frag("real", 0, 1) + 0.2, "slam", 0.5), ("real", frag("real", 0, 2), "page", 0.6), ("real", frag("real", 0, 2) + 0.3, "slam", 0.5), ("real", frag("real", 0, 3), "ding", 0.5), ("real", frag("real", 0, 3), "pop", 0.5),
    # the first-floor window; the pen: "ทำงานไม่ได้"
    ("watch", 2.3, "riser", 0.4), ("watch", 3.1, "sting", 0.5), ("watch", vo_t("watch", 1) + 0.15, "pen", 0.7), ("watch", frag("watch", 1, 1) - 0.1, "marker", 0.6), ("watch", frag("watch", 1, 1) + 0.25, "pen", 0.8),
    ("watch", frag("watch", 1, 1) + 0.4, "sting", 0.8), ("watch", frag("watch", 1, 1) + 0.4, "boom", 0.4), *beats("watch", vo_t("watch", 1), D["watch"] - vo_t("watch", 1), 0.55, 0.5),
    # dinner under the tubes: the hum, spoons, the whisper
    *bed("hum", T("dinner", 0), T("sig", -0.1), 0.3, 3.0), *bed("fan", T("dinner", 0), T("dinner", -0.1), 0.15, 4.0), *[("dinner", 0.2 + k * 0.8, "ching", 0.12) for k in range(5)],
    ("dinner", vo_t("dinner", 0) - 0.1, "whoosh", 0.3), ("dinner", frag("dinner", 0, 1), "sting", 0.8), ("dinner", frag("dinner", 0, 1), "boom", 0.4), *beats("dinner", vo_t("dinner", 0), D["dinner"] - vo_t("dinner", 0), 0.55, 0.55),
    # the signature
    ("sig", 0.05, "page", 0.8), ("sig", 0.36, "thud", 0.25),
    *[x for o in (frag("sig", 0, 0) + 0.3, frag("sig", 0, 0) + 0.62, frag("sig", 0, 1) + 0.15) for x in (("sig", o, "pen", 0.9), ("sig", o + 0.05, "ding", 0.3))],
    ("sig", frag("sig", 0, 2) + 0.45, "marker", 0.45), *beats("sig", frag("sig", 0, 2), frag("sig", 0, 3) - frag("sig", 0, 2), 0.38, 0.8),
    *[("sig", frag("sig", 0, 2) + o, "tick", 0.55 + 0.1 * k) for k, o in enumerate((0.1, 0.42, 0.68, 0.88, 1.02, 1.12))],
    ("sig", frag("sig", 0, 3) - 1.1, "riser", 0.6),
    ("sig", frag("sig", 0, 3), "sting", 1.1), ("sig", frag("sig", 0, 3), "boom", 0.7), ("sig", frag("sig", 0, 3), "pen", 1.0), ("sig", frag("sig", 0, 3) + 0.1, "pen", 1.0),
    ("sig", frag("sig", 0, 3) + 0.24, "rip", 1.1), ("sig", frag("sig", 0, 3) + 0.86, "thud", 0.8), ("sig", frag("sig", 0, 3) + 0.86, "slam", 0.35),
    *beats("sig", frag("sig", 0, 3), D["sig"] - frag("sig", 0, 3), 0.5, 0.7),
    # the radio: 93… five; in คุณวิน's room the other radio, his pen writing 93
    *bed("crickets", T("radio", 0), T("choice", -0.3), 0.25, 4.0), ("radio", vo_t("radio", 0) - 0.4, "radio", 1.0), *bed("radiobed", T("radio", vo_t("radio", 0) - 0.1), T("radio", -0.2), 0.5, 3.0),
    ("radio", frag("radio", 0, 1), "tick", 0.5), ("radio", frag("radio", 0, 1), "rustle", 0.6), ("radio", frag("radio", 0, 2), "sting", 0.9), ("radio", frag("radio", 0, 2), "slam", 0.6), ("radio", frag("radio", 0, 2), "glitch", 0.4),
    ("radio", vo_t("radio", 1) - 0.1, "static", 0.5), ("radio", vo_t("radio", 1) + 0.4, "pen", 0.7), ("radio", frag("radio", 1, 1), "sting", 0.9), ("radio", frag("radio", 1, 1), "boom", 0.5), ("radio", frag("radio", 1, 1), "glitch", 0.5), *beats("radio", vo_t("radio", 0), D["radio"] - vo_t("radio", 0), 0.5, 0.5),
    # midnight: the floodlights, the gate rolls open, the shuffle, the dead out there, the gate shuts; ครูพิม
    ("night", 0.3, "click", 0.6), ("night", frag("night", 0, 1), "sting", 0.7), ("night", frag("night", 0, 1) + 0.1, "gate", 0.6), *beats("night", 0.0, D["night"], 0.45, 0.7),
    ("night", vo_t("night", 1) + 0.1, "gate", 1.0), *[("night", vo_t("night", 1) + 0.2 + k * 0.6, "steps", 0.35) for k in range(4)], *growls("night", vo_t("night", 1) + 0.3, frag("night", 1, 2) + 0.6, 0.35, 0.8),
    ("night", frag("night", 1, 2) - 0.35, "whoosh", 0.35), ("night", frag("night", 1, 2) - 0.2, "gate", 0.9), ("night", frag("night", 1, 2) + 0.35, "clang", 0.9), ("night", frag("night", 1, 2) + 0.35, "sting", 1.0), ("night", frag("night", 1, 2) + 0.35, "boom", 0.6), ("night", frag("night", 1, 2) + 0.9, "glitch", 0.5),
    ("drawing", 0.1, "crayon", 0.6), ("drawing", 0.9, "crayon", 0.5), ("drawing", frag("drawing", 0, 1), "riser", 0.4), *growls("drawing", vo_t("drawing", 1) - 0.3, D["drawing"], 0.3, 0.7), ("drawing", frag("drawing", 1, 1), "sting", 0.9), ("drawing", frag("drawing", 1, 1), "boom", 0.5), ("drawing", frag("drawing", 1, 1), "glitch", 0.5), *beats("drawing", frag("drawing", 0, 1), D["drawing"] - frag("drawing", 0, 1), 0.55, 0.5),
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
dip(T("gate", frag("gate", 1, 1) - 0.2), T("gate", -0.05), 0.35)
dip(T("knows", vo_t("knows", 1) - 0.1), T("knows", -0.05), 0.35)
dip(T("mix", vo_t("mix", 2) - 0.3), T("signs", -0.05), 0.3)
dip(T("watch", frag("watch", 1, 1)), T("watch", -0.05), 0.35)
dip(T("sig", frag("sig", 0, 2)), T("sig", frag("sig", 0, 3) + 0.05), 0.05, 0.12)
dip(T("radio", vo_t("radio", 0) - 0.4), T("radio", vo_end("radio", 0) + 0.3), 0.15)
dip(T("night", 0), T("night", -0.05), 0.3)
dip(T("drawing", frag("drawing", 0, 1)), T("drawing", -0.05), 0.35)
dip(T("choice", 0), T("choice", -0.3), 0.5)
boost = np.ones(N, np.float32)  # the action plays with the music up
for a0, a1 in ((T("out", 0), T("out", vo_t("out", 1))), (T("workshop", WB + 0.05), T("workshop", WB + 1.65))):
    boost += 0.4 * (np.clip((t - a0) / 0.3, 0, 1) * np.clip((a1 - t) / 0.2, 0, 1)).astype(np.float32)
mus = mus * gain * boost
end = int(T("choice", -0.2) * SR)
mus[end:] = 0  # hard cut to black and silence

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
SFX_REF_DB = -25.352   # rms_db of the v2 SFX stem (sfx_sfx.v2.wav)
mus = level(mus, -30)
sfx = sfx * 10 ** ((-27 - SFX_REF_DB) / 20)   # the gain level(sfx, -27) gave the stem before the de-hiss: quieter beds must not push every other effect up
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

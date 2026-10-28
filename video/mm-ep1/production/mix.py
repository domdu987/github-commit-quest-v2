"""ผีแม่ม่าย EP.1: build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX for an Isan village
under the red shirts (the bus on the map, the PA tower, the shadow-puppet legend, the flipchart's heart and its short circuit, the
clock striking three, the bulb dying before the face) and the Suno music bed with dips before the scares and sidechain ducking under
the voice. Output -14 LUFS, hard cut to silence after the choice. No noise beds and no high hiss (user: "เสียงซ่าๆเอาออก")."""
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


def monitor(k, a, b, g=0.18, step=1.0):  # a bedside-monitor style beep
    return [(k, a + i * step, "beep", g) for i in range(int((b - a) / step) + 1)]


def ticks(k, a, b, g=0.2, step=1.0):  # the wall clock / the stopwatch
    return [(k, a + i * step, "tick", g) for i in range(int((b - a) / step) + 1)]


# flipchart row A: the beats land where the trace's R waves are (mmui.flipAnim: sweep 2.6 s from 0.5 s, R at x 70/205/340 of 410)
RA = [0.5 + bx / 410 * 2.6 for bx in (70, 205, 340)]
KB = vo_t("know1", 1) - 0.15                               # row B (the short circuit) pops in
STAMP = F("know1", 2, 1) - 0.05 + 0.2                      # the stamp lands (power4.in, 0.2 s)
K2B = vo_t("know2", 1) - 0.1                               # page 2, row B: the family tree
FING = F("close", 0, 1)                                    # the black fingers curl round the door frame
DEMO_TAP = F("demo", 0, 1) + 0.1                           # Bua's pats (tapBack: sin(u*16) peaks every 0.39 s)

CUES = [
    # 1. the shirt in the dark; the title paints itself; drips run
    ("open", 0.0, "swell", 0.3), ("open", 0.0, "crickets", 0.22), ("open", 0.35, "whoosh", 0.22),
    ("open", 2.4, "drip", 0.32), ("open", 2.85, "drip", 0.26),
    # 2. flash-forward: Fon shaking him in the dark
    ("hook", 0.0, "glitch", 0.45), *beats("hook", 0.05, D["hook"] - 0.4, 0.42, 0.55), ("hook", 0.1, "rustle", 0.3), ("hook", 0.9, "rustle", 0.3),
    ("hook", D["hook"] - 0.35, "glitch", 0.6), ("hook", D["hook"] - 0.32, "sting", 0.85), ("hook", D["hook"] - 0.3, "boom", 0.5),
    # 3. the map: pin, the bus drives, the end pin, the drop to the village
    ("map", 0.4, "pop", 0.3), ("map", 0.55, "engine", 0.22), ("map", 2.95, "pop", 0.32), ("map", 3.0, "ding", 0.3), ("map", D["map"] - 1.35, "whoosh", 0.35),
    # 4. the songthaew pulls away; dusk
    ("arrive", 0.0, "engine", 0.2), ("arrive", 0.3, "crickets", 0.14),
    # 5./6. the PA tower: chime, hum under the announcement; "ตัวละห้าสิบ"; Keng, deadpan
    ("horns", 0.0, "ding", 0.32), ("horns", 0.22, "ding", 0.26), ("horns", 0.25, "hum", 0.12), ("horns", 3.6, "hum", 0.12),
    ("sell", 0.0, "hum", 0.12), ("sell", F("sell", 0, 2) + 0.75, "ching", 0.32), ("sell", vo_t("sell", 1) - 0.15, "pop", 0.3),
    # 7. Fon runs up the street
    ("fon", 0.0, "steps", 0.28),
    # 8. the shadow-puppet legend: gong and cymbals, the red shirt drops, the widow turns away
    ("legend", 0.0, "gong", 0.45), ("legend", 0.2, "ching", 0.25),
    ("legend", vo_t("legend", 1) + 0.05, "whoosh", 0.25), ("legend", vo_t("legend", 1) + 0.45, "ching", 0.3),
    ("legend", F("legend", 1, 2) - 0.1, "whoosh", 0.25), ("legend", F("legend", 1, 2), "gong", 0.3),
    ("legend2", 0.9, "swell", 0.35), ("legend2", 2.0, "gong", 0.3),
    # 9. morning: ลุงเปี๊ยก's nails; "สมศรี"
    ("nails", 0.05, "rooster", 0.22),
    ("somsri", vo_t("somsri", 1) - 0.15, "pop", 0.28), ("somsri", vo_end("somsri", 1) + 0.05, "ching", 0.3),
    # 10. supper; the clock; the father's portrait
    *ticks("photo", 0.2, D["photo"] + D["mom"] - 0.3, 0.18), ("photo", D["photo"] - 1.5, "swell", 0.35),
    # 11. the class: the flipchart (heart beats, the short circuit, the stamp), page 2 (the age band, the family tree)
    ("bua", 0.0, "whoosh", 0.18),
    ("know1", 0.0, "whoosh", 0.28), ("know1", 0.05, "rustle", 0.3), ("know1", 0.3, "pop", 0.28),
    *[("know1", t, "heartbeat", 0.45) for t in RA], *[("know1", t, "beep", 0.14) for t in RA],
    ("know1", KB, "pop", 0.3), ("know1", KB + 0.4, "zap", 0.22), ("know1", KB + 1.5, "zap", 0.2), ("know1", KB + 1.1, "buzz", 0.22),
    ("know1", F("know1", 2, 0) + 0.15, "marker", 0.25), ("know1", STAMP, "stomp", 0.5),
    ("know2", 0.05, "whoosh", 0.28), ("know2", 0.05, "rustle", 0.3), ("know2", 0.5, "pop", 0.28), ("know2", 0.95, "marker", 0.25),
    ("know2", K2B, "pop", 0.28), ("know2", K2B + 0.2, "marker", 0.25), ("know2", K2B + 0.8, "ding", 0.32),
    # Keng hears it: heartbeat, the portrait flashes
    *beats("kface", 0.0, D["kface"], 0.5, 0.6), ("kface", 0.72, "sting", 0.8), ("kface", 0.72, "boom", 0.4),
    # the rule card; the demo on ลุงเปี๊ยก
    ("rule", 0.6, "whoosh", 0.35), ("rule", 1.15, "ding", 0.38), ("rule", 1.35, "pop", 0.25), ("rule", 1.6, "marker", 0.22),
    *[("demo", DEMO_TAP + i * 0.39, "knock", 0.2) for i in range(5)],
    ("demo", vo_t("demo", 1) - 0.1, "whoosh", 0.3), ("demo", vo_t("demo", 1), "ching", 0.35),
    # 12. 3 a.m.: the clock strikes three, the shirt at the door swings with no wind
    ("night", 0.0, "crickets", 0.18), *ticks("night", 0.1, 1.7, 0.2, 0.5), ("night", 0.7, "creak", 0.22),
    ("night", 1.9, "gong", 0.3), ("night", 2.45, "gong", 0.28), ("night", 3.0, "gong", 0.26),
    ("window", 0.2, "creak", 0.28), ("window", 0.4, "swell", 0.38),
    # he jerks rigid; she shakes him; he goes still
    *beats("jerk", 0.1, D["jerk"] - 0.1, 0.5, 0.5), *[("jerk", t, "rustle", 0.28) for t in (0.1, 0.8, 1.5, 2.2)],
    *beats("shake", 0.0, 1.2, 0.42, 0.55), ("shake", 0.1, "rustle", 0.33), ("shake", 0.6, "rustle", 0.33),
    # lights out: the bulb flickers and dies; the eyes; stillness; the face; black
    ("foot", 0.12, "buzz", 0.2), ("foot", 0.45, "powerdown", 0.35), *beats("foot", 0.9, 2.1, 0.8, 0.38), ("foot", 1.0, "swell", 0.16),
    ("foot", 3.4, "sting", 1.25), ("foot", 3.4, "slam", 0.7), ("foot", 3.42, "shriek", 0.5), ("foot", 3.4, "glitch", 0.5),
    # 13. what it was: the badges, the stopwatch running
    *beats("know3", 0.0, D["know3"], 0.85, 0.35), ("know3", vo_t("know3", 0) - 0.05, "pop", 0.28), ("know3", F("know3", 0, 1) - 0.05, "pop", 0.28),
    ("know3", vo_t("know3", 1) - 0.05, "pop", 0.3), *ticks("know3", vo_t("know3", 1) + 0.1, D["know3"] - 0.4, 0.2, 0.25),
    ("scream", 0.1, "sting", 0.6), ("scream", 0.1, "boom", 0.4), ("scream", 0.15, "glitch", 0.4),
    # 14. the shirt still hangs at the door… and the fingers
    ("close", 0.0, "creak", 0.22), ("close", FING - 0.3, "swell", 0.38), ("close", FING - 0.15, "creak", 0.28),
    *beats("close", FING, D["close"] - FING, 0.7, 0.55),
    # 15. the choice, dragged to the ghost doctor
    *beats("choice", 0.0, D["choice"] - 0.15, 0.42, 0.55), ("choice", 0.3, "pop", 0.28), ("choice", 0.42, "pop", 0.28), ("choice", 0.75, "click", 0.3),
    ("choice", 1.3, "swell", 0.3), ("choice", 1.6, "glitch", 0.5), ("choice", 1.65, "whoosh", 0.35), ("choice", D["choice"] - 0.5, "glitch", 0.6),
    # 16. the end card: the tag swings onto its hook
    ("next", 0.3, "whoosh", 0.45), ("next", 0.35, "creak", 0.3), ("next", 0.7, "gong", 0.45),
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


dip(0.0, T("open", -0.05), 0.4, 0.05)
dip(T("hook", 0), T("hook", -0.05), 0.3)
dip(T("photo", 0), T("mom", -0.05), 0.5)
dip(T("kface", 0), T("kface", -0.05), 0.3, 0.1)
dip(T("night", 0), T("shake", -0.05), 0.3)
dip(T("foot", 0), T("foot", -0.05), 0.04, 0.1)
dip(T("know3", 0), T("close", -0.05), 0.42)
dip(T("choice", 0), T("choice", -0.05), 0.5)
mus = mus * gain
end = int(T("choice", -0.15) * SR)
mus[end:] = 0  # hard cut to black and silence

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mix = vo + mus * duck + sfx
cut, card = int(T("choice", -0.15) * SR), int(T("next", 0.3) * SR)
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

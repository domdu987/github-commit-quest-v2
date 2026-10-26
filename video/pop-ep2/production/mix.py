"""เห็ดปอบ EP.2: build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX for a flooded village
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
RS = vo_t("road", 1) - 0.25                               # the road shot cuts to ลุงทองดี close
WB, WC, WD = F("print", 1, 1) + 0.3, D["print"] - 1.0, D["print"] - 0.6  # the window: eyes in, eyes out, the hit


def chew(k, t0, n, gap=0.55, g=0.35):
    return [(k, t0 + i * gap, "squelch", g) for i in range(n)]


def engine(k, a, b, g=0.35, step=0.9):  # the old pickup's motor
    return [(k, a + i * step, "engine", g) for i in range(int((b - a) / step) + 1)]


CUES = [
    ("recap", 0.0, "glitch", 0.5), ("recap", 0.2, "pant", 0.3), *beats("recap", 0.0, D["recap"], 0.4, 0.6),
    *engine("hook", 0.0, D["hook"] - 0.6, 0.4), *beats("hook", 0.4, D["hook"] - 0.4, 0.4, 0.5),
    ("hook", D["hook"] - 0.5, "sting", 1.0), ("hook", D["hook"] - 0.5, "glitch", 0.7), ("hook", D["hook"] - 0.45, "boom", 0.6),
    ("wait", 0.1, "swell", 0.3), *beats("wait", 0.0, D["wait"], 0.5, 0.45),
    ("no", 0.05, "slam", 0.3), ("no", 0.05, "whoosh", 0.35),
    ("vomit", 0.4, "splash", 0.35), ("vomit", 1.4, "splash", 0.25), *beats("vomit", 0.0, D["vomit"], 0.42, 0.5),
    ("crowd", 0.0, "steps", 0.4), ("crowd", 0.3, "steps", 0.35), ("crowd", 0.05, "whoosh", 0.3),
    ("salt", 0.1, "ching", 0.3),
    ("know1", F("know1", 0, 1), "click", 0.5), ("know1", F("know1", 0, 2), "click", 0.5), ("know1", F("know1", 0, 2) + 0.4, "click", 0.5), ("know1", vo_t("know1", 1), "pant", 0.35),
    ("grab", vo_end("grab") - 0.4, "rustle", 0.45),
    ("know2", 0.1, "pop", 0.35), ("know2", F("know2", 0, 1) - 0.2, "whoosh", 0.3), ("know2", F("know2", 0, 1) + 0.6, "ding", 0.45),
    ("photo", 0.2, "shutter", 0.7),
    ("fine", 0.1, "swell", 0.25),
    ("both", 0.05, "whoosh", 0.3), *[("both", 0.4 + k * 0.3, "steps", 0.35) for k in range(5)],
    ("know3", F("know3", 0, 1), "ding", 0.5),
    ("nocar", 0.0, "crickets", 0.35),
    ("truck", 0.0, "engine", 0.6), ("truck", 0.05, "slam", 0.35), ("truck", 0.05, "swell", 0.3),
    *engine("joke", 0.0, D["joke"], 0.3),
    *engine("road", 0.0, D["road"], 0.35), ("road", RS + 0.1, "swell", 0.3),
    ("er", 0.0, "engine", 0.4), ("er", 1.4, "thud", 0.3), ("er", 1.8, "steps", 0.4), ("er", 2.1, "steps", 0.4),
    ("ask", 0.05, "beep", 0.25),
    ("answer", F("answer", 0, 1) - 0.2, "whoosh", 0.3),
    *[("know4", 0.3 + k * (D["know4"] - 1.0) / 4, "click", 0.4) for k in range(4)],
    ("diag", F("diag", 0, 1), "swell", 0.35), *beats("diag", F("diag", 0, 1), D["diag"] - F("diag", 0, 1), 0.48, 0.45),
    ("dawn", 0.1, "beep", 0.2), ("dawn", 1.1, "beep", 0.2),
    ("better", 0.1, "beep", 0.2), ("better", 0.3, "pop", 0.3),
    # koi-style: a handprint on the glass, two eyes outside, the heartbeat; one hit and cut
    ("print", 0.1, "beep", 0.18), ("print", F("print", 0, 1), "swell", 0.35), *beats("print", F("print", 0, 1), WC - F("print", 0, 1), 0.55, 0.6),
    ("print", WD, "sting", 1.1), ("print", WD, "slam", 0.7), ("print", WD + 0.02, "shriek", 0.5),
    *beats("choice", 0.0, D["choice"] - 0.3, 0.38, 1.0), *[("choice", 0.05 + k * 1.0, "tick", 1.0) for k in range(3)],
    ("choice", D["choice"] - 2.2, "riser", 1.0), ("choice", D["choice"] - 0.62, "sting", 1.0), ("choice", D["choice"] - 0.6, "glitch", 0.8), ("choice", D["choice"] - 0.6, "boom", 0.7),
    ("next", 0.3, "whoosh", 0.5), ("next", 0.45, "drip", 0.6), ("next", 0.8, "sting", 0.6),
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
dip(T("know1", 0), T("know1", -0.05), 0.6)
dip(T("road", RS), T("road", -0.05), 0.35)
dip(T("print", 0), T("print", -0.05), 0.08, 0.1)
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

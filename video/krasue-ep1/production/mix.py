"""แสงกระสือ EP.1: build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX for a flooded village
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


AT, LAND, FACE = 2.2, 4.0, 1.45  # the opener (OpenerLight: at, at + glide, face) as in the composition
K2 = frag("cut", 0, 2) - 0.12    # the cut shot cuts to the switch close up
LV = K2 + 0.5                    # the lever comes down
F = frag
KNOW_CUT = vo_t("know", 1) + 0.5  # the diagram's lever


def zaps(k, ts, g=0.5):
    return [(k, t, "zap", g) for t in ts]


CUES = [
    # story opener, its own (OpenerLight.cues)
    ("open", 0.0, "hum", 0.7), ("open", 0.25, "buzz", 0.5), ("open", 0.6, "zap", 0.5), ("open", 0.95, "boom", 0.35), ("open", FACE - 0.1, "zap", 0.7),
    ("open", FACE + 0.28, "sting", 1.0), ("open", FACE + 0.3, "shriek", 0.6), ("open", FACE + 0.3, "glitch", 0.6), *beats("open", 0.3, FACE, 0.55, 0.4),
    ("open", AT - 0.2, "zap", 0.9), ("open", AT, "powerdown", 0.4), ("open", AT + 0.5, "buzz", 0.4), ("open", LAND - 0.02, "boom", 0.8), ("open", LAND, "glitch", 0.4),
    ("hook", 0.0, "hum", 0.6), *[("hook", t, "plop", 0.35) for t in (0.3, 1.1, 1.9)], *zaps("hook", (0.5, 1.4), 0.6),
    ("hook", D["hook"] - 0.5, "sting", 1.0), ("hook", D["hook"] - 0.45, "boom", 0.6),
    ("back", 0.0, "rewind", 0.8), *[("back", 0.05 + k * 0.2, "tick", 0.3) for k in range(6)],
    ("dusk", 0.2, "swell", 0.3),
    ("live", 0.1, "notif", 0.45), ("live", 0.15, "pop", 0.3),
    ("toey", 0.1, "plop", 0.4), ("toey", 0.6, "pop", 0.3),
    ("boat", 0.3, "plop", 0.35), ("boat", 0.9, "creak", 0.35), ("boat", 1.8, "thud", 0.25),
    ("rule", 0.0, "swell", 0.4), *[("rule", F("rule", 0, j), "ding", 0.45) for j in (0, 1)],
    ("legend", 0.0, "rustle", 0.5), ("legend", F("legend", 0, 1) - 0.05, "sting", 0.7),
    *[("traits", F("traits", i, j) - 0.12, "rustle", 0.45) for i, j in ((1, 0), (2, 0))], ("traits", F("traits", 1, 1), "squelch", 0.5),
    ("chaem", 0.1, "steps", 0.35), ("chaem", 0.8, "steps", 0.3), ("chaem", 1.75, "clang", 0.3),
    ("cold", 0.1, "whoosh", 0.3), ("cold", 0.5, "swell", 0.45), *beats("cold", 0.5, D["cold"] - 0.5, 0.45, 0.4),
    *[("nine", 0.05 + k * 0.4, "tick", 0.35) for k in range(2)], ("nine", vo_t("nine", 1), "plop", 0.35),
    ("know", 0.2, "drip", 0.3), *zaps("know", (1.2, 1.9), 0.45), ("know", KNOW_CUT, "clang", 0.5), ("know", KNOW_CUT + 0.35, "ding", 0.5), ("know", vo_t("know", 2) + 0.1, "buzz", 0.35),
    ("cut", 0.2, "rustle", 0.3), ("cut", K2 + 0.05, "click", 0.4), ("cut", LV + 0.05, "zap", 0.8), ("cut", LV + 0.4, "clang", 0.6), ("cut", LV + 0.5, "powerdown", 0.9),
    ("dark", 0.2, "swell", 0.35),
    ("cam", 0.05, "beep", 0.25), *beats("cam", 0.3, D["cam"] - 0.3, 0.55, 0.4),
    ("bomb", 0.0, "hum", 0.45), *zaps("bomb", (F("bomb", 0, 1), F("bomb", 0, 1) + 0.6), 0.6),
    *[("two", 0.05 + k * 0.45, "tick", 0.3) for k in range(3)],
    *beats("call", 0.0, D["call"], 0.55, 0.5),
    ("answer", 0.0, "hum", 0.3),
    *[("wade", t, "plop", 0.4) for t in (1.0, 1.4, 1.8, 2.3, 2.8)],
    ("shout", 0.05, "whoosh", 0.4),
    ("know2", 0.0, "hum", 0.4), *zaps("know2", (0.6, 2.4, 4.2), 0.4),
    ("know3", 0.0, "hum", 0.35), ("know3", 0.25, "whoosh", 0.3),
    ("clue", 0.2, "creak", 0.4), *beats("clue", vo_t("clue", 1), D["clue"] - vo_t("clue", 1), 0.5, 0.5), ("clue", vo_t("clue", 1), "swell", 0.4),
    # koi-style: only her eyes in the dark, a slow heartbeat, the whisper; no stings
    *beats("whisper", 0.0, D["whisper"], 0.55, 0.6), *zaps("whisper", (1.2,), 0.3),
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


dip(0.0, T("open", -0.05), 0.25, 0.05)
dip(T("hook", 0), T("hook", -0.05), 0.35)
dip(T("legend", 0), T("traits", -0.2), 0.5)
dip(T("cold", 0), T("cold", -0.05), 0.4)
dip(T("cut", LV + 0.4), T("bomb", -0.05), 0.3)  # the power goes: the music thins with it
dip(T("two", 0), T("answer", -0.05), 0.15)
dip(T("clue", 0), T("whisper", -0.05), 0.35)
dip(T("whisper", 0), T("whisper", -0.05), 0.1)
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

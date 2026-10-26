"""เต็นท์ผีอำ EP.1: build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX for a campsite on a
cold doi (crickets at dusk, thunder and drips in the rain, coals crackling, the stove set down, the heartbeat under the ผีอำ) and the Suno music bed with dips before the scares and sidechain ducking under the voice. Output -14 LUFS, hard cut
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
GB, GHT, GD = vo_t("ghost") + 0.2, D["ghost"] - 0.9, D["ghost"] - 0.45  # the ghost on the chest: eyes open, the dark comes down, the hit (as in the composition)


def steps(k, t0, dur, gap=0.45, g=0.25):
    return [(k, t0 + i * gap, "steps", g) for i in range(int(dur / gap))]


CUES = [
    # story opener, its own: coals crackling, the title in the smoke, the eyes
    ("open", 0.0, "crackle", 0.4), ("open", 0.3, "swell", 0.4), *beats("open", 2.0, 1.8, 0.45, 0.5),
    ("open", 3.0, "swell", 0.35), ("open", D["open"] - 0.45, "sting", 0.9), ("open", D["open"] - 0.45, "glitch", 0.6), ("open", D["open"] - 0.42, "boom", 0.6),
    ("hook", 0.1, "thunder", 0.45), ("hook", 0.6, "drip", 0.3), ("hook", 1.6, "drip", 0.25), ("hook", F("hook", 1, 0) + 0.2, "swell", 0.4),
    *beats("hook", F("hook", 1, 0), D["hook"] - F("hook", 1, 0) - 0.4, 0.5, 0.5),
    ("hook", D["hook"] - 0.4, "sting", 1.0), ("hook", D["hook"] - 0.4, "glitch", 0.7), ("hook", D["hook"] - 0.35, "boom", 0.6),
    ("arrive", 0.0, "crickets", 0.25), *steps("arrive", 0.3, D["arrive"] - 0.3),
    ("vlog", 0.05, "beep", 0.3), ("vlog", vo_t("vlog") + 0.1, "pop", 0.25),
    ("pork", vo_t("pork") + 0.1, "pop", 0.3), ("pork", F("pork", 0, 1), "clang", 0.3),
    ("booze", vo_t("booze") + 0.2, "ding", 0.25),
    ("cold", 0.0, "crickets", 0.2),
    ("plot", 0.0, "crickets", 0.2), ("plot", F("plot", 0, 1), "swell", 0.3),
    ("why", 0.05, "pop", 0.25),
    ("am", vo_t("am"), "swell", 0.4), ("am", vo_t("am") + 0.2, "creak", 0.3), *beats("am", vo_t("am"), D["am"] - vo_t("am"), 0.55, 0.5),
    ("legend1", 0.0, "rustle", 0.4), ("legend1", F("legend1", 0, 2), "gong", 0.45),
    ("legend2", F("legend2", 0, 1), "swell", 0.4), *beats("legend2", F("legend2", 0, 1), D["legend2"] - F("legend2", 0, 1), 0.5, 0.5),
    ("joke", vo_t("joke") + 0.3, "pop", 0.3),
    ("rule", vo_t("rule") + 0.2, "ding", 0.45), ("rule", vo_t("rule") + 0.2, "swell", 0.3),
    ("rain", 0.1, "thunder", 0.6), *[("rain", 0.3 + k * 0.6, "drip", 0.25) for k in range(int(D["rain"] / 0.6))], ("rain", 0.4, "rustle", 0.35),
    ("bring", 0.2, "rustle", 0.3), ("bring", 0.5, "clang", 0.35), ("bring", 0.6, "crackle", 0.3),
    ("know1", 0.1, "ding", 0.4), *[("know1", 0.4 + k * 0.32, "pop", 0.22) for k in range(6)], ("know1", F("know1", 0, 1), "click", 0.4),
    ("know2", vo_t("know2") + 0.3, "click", 0.45), ("know2", F("know2", 0, 1) + 0.2, "click", 0.45),
    ("know3", 0.3, "swell", 0.35), *[("know3", 0.4 + k * 0.22, "pop", 0.18) for k in range(10)], ("know3", F("know3", 0, 1), "clang", 0.35),
    ("know4", 0.3, "whoosh", 0.25), ("know4", F("know4", 0, 1), "click", 0.45), ("know4", F("know4", 0, 1) + 0.05, "clang", 0.4),
    ("order", 0.0, "crackle", 0.2),
    ("more", 0.0, "crackle", 0.35), ("more", 0.5, "squish", 0.35), ("more", 0.9, "squish", 0.3),
    ("cheers", vo_t("cheers") + 0.15, "ding", 0.5), ("cheers", 0.0, "crackle", 0.2),
    ("out", 0.0, "thunder", 0.3), *steps("out", 0.2, 1.4, 0.4, 0.3), ("out", 1.6, "clang", 0.3), ("out", F("out", 0, 1) + 0.1, "whoosh", 0.35), ("out", 0.8, "drip", 0.25),
    ("two", 0.2, "swell", 0.25), *beats("two", F("two", 0, 1), D["two"] - F("two", 0, 1), 0.5, 0.5),
    ("back", 0.0, "crackle", 0.35), ("back", F("back", 0, 1), "swell", 0.45), *beats("back", F("back", 0, 1), D["back"] - F("back", 0, 1), 0.5, 0.55),
    ("chest", 0.2, "pant", 0.3), ("chest", F("chest", 0, 1), "swell", 0.35), *beats("chest", 0.0, D["chest"], 0.55, 0.6),
    # koi-style: only the eyes in the dark, a slow heartbeat; one hit and cut
    *beats("ghost", 0.0, GHT, 0.6, 0.65), ("ghost", GB, "swell", 0.3),
    ("ghost", GD, "sting", 1.1), ("ghost", GD, "slam", 0.7), ("ghost", GD + 0.02, "shriek", 0.5),
    *beats("choice", 0.0, D["choice"] - 0.3, 0.38, 1.0), *[("choice", 0.05 + k * 1.0, "tick", 1.0) for k in range(3)],
    ("choice", D["choice"] - 2.2, "riser", 1.0), ("choice", D["choice"] - 0.62, "sting", 1.0), ("choice", D["choice"] - 0.6, "glitch", 0.8), ("choice", D["choice"] - 0.6, "boom", 0.7),
    ("next", 0.3, "whoosh", 0.5), ("next", 0.45, "crickets", 0.4), ("next", 0.8, "sting", 0.6),
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


dip(0.0, T("open", -0.05), 0.3, 0.05)
dip(T("hook", 0), T("hook", -0.05), 0.35)
dip(T("am", 0), T("legend2", -0.05), 0.45)
dip(T("two", 0), T("ghost", 0), 0.2)
dip(T("ghost", 0), T("ghost", -0.05), 0.05, 0.1)
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

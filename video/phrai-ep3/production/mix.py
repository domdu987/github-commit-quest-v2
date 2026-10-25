"""มือพราย EP.3 (ตอนจบ): build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX for a river on Loy
Krathong night (water lapping at the pier, the splash, bubbles under the water, the gallon landing, the shadow-puppet gong) and the
Suno music bed with dips before the scares and sidechain ducking under the voice. Output -14 LUFS, hard cut to silence before the end card."""
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


H2 = frag("hook", 1, 0)
GR = lambda j: frag("grab", 0, j)
strokes = lambda k, a, b, p: [(k, a + i * p, "splash", 0.12) for i in range(int((b - a) / p))]

CUES = [
    *beats("recap", 0.0, D["recap"], 0.38, 0.8), ("recap", D["recap"] - 0.35, "glitch", 0.7),
    ("hook", 0.0, "swell", 0.4), ("hook", 0.3, "sting", 0.6), *strokes("hook", 0.2, D["hook"], 0.6), *beats("hook", 0.5, D["hook"] - 0.5, 0.5, 0.4),
    ("hook", H2 - 0.7, "whoosh", 0.5), ("hook", H2 + 0.18, "slam", 0.8), ("hook", H2 + 0.18, "glitch", 0.6),
    *strokes("swim", 0.0, D["swim"], 0.52),
    ("tired", 0.8, "splash", 0.35), ("tired", 1.9, "splash", 0.3), ("tired", 3.0, "splash", 0.35), ("tired", 4.1, "splash", 0.3),
    *beats("tired", frag("tired", 0, 1), D["tired"] - frag("tired", 0, 1), 0.42, 0.55),
    ("call", 0.0, "bubbles", 0.9), ("call", 1.8, "bubbles", 0.7), ("call", vo_t("call") - 0.2, "swell", 0.6), *beats("call", vo_t("call"), D["call"] - vo_t("call"), 0.42, 0.6),
    ("call", frag("call", 0, 1), "glitch", 0.4),
    ("grab", 0.0, "bubbles", 0.7), ("grab", GR(1), "sting", 1.0), ("grab", GR(1), "squish", 0.5), ("grab", GR(1), "glitch", 0.5),
    ("grab", GR(2), "boom", 0.8), ("grab", GR(2), "bubbles", 1.0), *beats("grab", GR(1), D["grab"] - GR(1), 0.36, 0.7),
    ("sink", 0.0, "splash", 0.6), ("sink", 1.2, "bubbles", 1.0), *beats("sink", 0.0, D["sink"], 0.36, 0.7),
    ("memory", 0.0, "whoosh", 0.5), ("memory", 0.05, "glitch", 0.3), ("memory", frag("memory", 0, 1), "ding", 0.6),
    ("mouth", 0.2, "splash", 0.25), ("mouth", frag("mouth", 0, 1), "swell", 0.4),
    ("float", 0.0, "splash", 0.3), ("float", 0.3, "plop", 0.3),
    ("then", frag("then", 0, 1), "whoosh", 0.35), ("then", frag("then", 0, 2), "whoosh", 0.35),
    ("moon", 0.0, "swell", 0.4),
    ("loose", frag("loose", 0, 1), "bubbles", 0.6), ("loose", frag("loose", 0, 1) + 0.4, "swell", 0.4),
    ("gallon", 0.4, "plop", 0.4), ("gallon", frag("gallon", 0, 2) + 0.6, "thud", 0.25),
    ("help", vo_t("help"), "whoosh", 0.3), ("help", 0.3, "splash", 0.2),
    ("oar", 0.0, "creak", 0.5), ("oar", frag("oar", 0, 1), "whoosh", 0.45), ("oar", frag("oar", 0, 1) + 0.4, "creak", 0.4),
    ("hold", vo_t("hold") - 0.2, "swell", 0.4),
    ("land", 0.3, "splash", 0.25), ("land", 1.1, "steps", 0.5),
    ("dawn", frag("dawn", 0, 1) - 0.4, "steps", 0.5), ("dawn", 0.2, "beep", 0.2), ("dawn", 1.4, "beep", 0.2), ("dawn", 2.6, "beep", 0.2),
    ("tell", 0.0, "beep", 0.2),
    ("dead", frag("dead", 0, 1), "sting", 0.9), ("dead", frag("dead", 0, 1), "glitch", 0.5), *beats("dead", frag("dead", 0, 1), D["dead"] - frag("dead", 0, 1), 0.45, 0.6),
    ("legend", 0.0, "gong", 0.6), ("legend", frag("legend", 0, 1) + 0.75, "splash", 0.5), ("legend", frag("legend", 0, 2), "gong", 0.45), ("legend", frag("legend", 0, 2) + 0.3, "bubbles", 0.7),
    ("every", 0.0, "creak", 0.35), ("every", D["every"] - 1.6, "swell", 0.5),
    ("know", frag("know", 0, 2), "ding", 0.5), ("know", frag("know", 0, 2) + 0.45, "ding", 0.5), ("know", frag("know", 0, 2) + 0.9, "ding", 0.5),
    ("wake", 0.6, "swell", 0.4), ("wake", 0.2, "beep", 0.2),
    *beats("whisper", frag("whisper", 0, 1), D["whisper"] - frag("whisper", 0, 1), 0.5, 0.55), ("whisper", frag("whisper", 0, 2), "riser", 0.6),
    ("whisper", frag("whisper", 0, 3), "sting", 1.0), ("whisper", frag("whisper", 0, 3), "glitch", 0.6), ("whisper", frag("whisper", 0, 3), "boom", 0.5),
    ("marks", frag("marks", 0, 1), "sting", 0.9), ("marks", frag("marks", 0, 1), "thud", 0.5), ("marks", frag("marks", 0, 2), "glitch", 0.5),
    *beats("marks", frag("marks", 0, 1), D["marks"] - frag("marks", 0, 1), 0.42, 0.6),
    ("last", 0.0, "plop", 0.3), ("last", vo_t("last"), "bubbles", 0.7), *beats("last", 0.0, D["last"], 0.4, 0.6),
    ("last", D["last"] - 2.2, "riser", 1.0), ("last", D["last"] - 0.52, "sting", 1.0), ("last", D["last"] - 0.5, "glitch", 0.8), ("last", D["last"] - 0.5, "boom", 0.7),
    ("end", 0.3, "whoosh", 0.5), ("end", 0.45, "drip", 0.6), ("end", 0.8, "gong", 0.5), *beats("end", 0.9, D["end"] - 0.9, 0.7, 0.5),
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
dip(T("call", 0), T("sink", -0.05), 0.3)
dip(T("memory", 0), T("memory", -0.05), 0.5)
dip(T("moon", 0), T("loose", -0.05), 0.55)
dip(T("dead", frag("dead", 0, 1)), T("dead", -0.05), 0.3)
dip(T("whisper", frag("whisper", 0, 2)), T("last", -0.2), 0.3)
mus = mus * gain
end = int(T("last", -0.15) * SR)
mus[end:] = 0  # hard cut to black and silence
# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mix = vo + mus * duck + sfx
cut, card = int(T("last", -0.15) * SR), int(T("end", 0.3) * SR)
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

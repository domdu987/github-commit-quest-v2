"""มือพราย EP.2: build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX for a river on Loy
Krathong night (water lapping at the pier, the splash, bubbles under the water, the gallon landing, the shadow-puppet gong) and the
Suno music bed with dips before the scares and sidechain ducking under the voice. Output -14 LUFS, hard cut to silence after the choice."""
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
SRT = lambda j: frag("srt", 0, j)
JOLT = frag("fall", 0, 0) + 0.3
SF = lambda j: frag("sig", 0, j)
CPR_A, CPR_B = 0.1, frag("cpr", 0, 1) - 0.1

CUES = [
    ("recap", 0.0, "lap", 0.8), *beats("recap", 0.0, D["recap"], 0.38, 0.8), ("recap", D["recap"] - 0.35, "glitch", 0.7),
    ("hook", 0.0, "swell", 0.4), ("hook", 0.3, "sting", 0.6), ("hook", 0.4, "drip", 0.5), ("hook", 1.2, "drip", 0.4), *beats("hook", 0.5, D["hook"] - 0.5, 0.5, 0.4),
    ("hook", H2 - 0.7, "whoosh", 0.5), ("hook", H2 + 0.18, "slam", 0.8), ("hook", H2 + 0.18, "glitch", 0.6),
    ("follow", 0.0, "lap", 0.8), ("follow", 0.3, "creak", 0.4),
    ("lure", 0.0, "bubbles", 0.9), ("lure", 1.5, "bubbles", 0.7), *beats("lure", vo_t("lure"), D["lure"] - vo_t("lure"), 0.45, 0.5),
    ("sleep", 0.0, "lap", 0.9), ("sleep", 0.6, "plop", 0.3), ("sleep", 1.8, "plop", 0.3), *beats("sleep", 0.0, D["sleep"], 0.45, 0.45),
    ("stop", 0.0, "whoosh", 0.5),
    ("almost", 0.0, "steps", 0.6), ("almost", frag("almost", 0, 1), "sting", 0.6), ("almost", frag("almost", 0, 1), "thud", 0.4),
    ("srt", SRT(1), "whoosh", 0.7), ("srt", SRT(1) + 0.8, "plop", 0.8), ("srt", SRT(2), "creak", 0.5), ("srt", 0.0, "lap", 0.6),
    ("help", vo_t("help"), "whoosh", 0.3),
    ("out", 0.2, "splash", 0.35), ("out", 1.4, "thud", 0.5), ("out", frag("out", 0, 1), "swell", 0.5), *beats("out", frag("out", 0, 1), D["out"] - frag("out", 0, 1), 0.45, 0.55),
    ("yai", 0.0, "steps", 0.6), ("no", 0.05, "thud", 0.5), ("no", 0.05, "sting", 0.5),
    ("dont", frag("dont", 0, 1), "whoosh", 0.4),
    ("call", 0.2, "beep", 0.4), ("call", 0.6, "ring", 0.4),
    *[("check", 0.2 + i * 0.12, "rustle", 0.3) for i in range(0, 8, 2)], *beats("check", frag("check", 0, 2), D["check"] - frag("check", 0, 2), 0.42, 0.5),
    ("air", frag("air", 0, 2) + 0.3, "whoosh", 0.35), ("air", frag("air", 0, 2) + 1.1, "whoosh", 0.35),
    *[("cpr", CPR_A + i * (CPR_B - CPR_A) / 30, "tick", 0.45) for i in range(30)], ("cpr", CPR_B + 0.3, "whoosh", 0.35), ("cpr", CPR_B + 1.0, "whoosh", 0.35),
    ("breathe", 0.35, "splash", 0.15), ("breathe", 0.8, "swell", 0.5), ("breathe", 1.0, "ding", 0.3),
    ("recover", 0.3, "rustle", 0.5), ("recover", frag("recover", 0, 1), "rustle", 0.5),
    ("flood", 0.0, "lap", 0.9), ("flood", 0.0, "siren", 0.25), ("flood", 1.6, "siren", 0.2),
    ("ferry", 0.0, "lap", 0.8), ("ferry", 0.3, "creak", 0.5),
    # channel signature
    ("sig", 0.05, "glitch", 0.35), ("sig", 0.05, "beep", 0.35),
    ("sig", SF(0) + 0.3, "ding", 0.6), ("sig", SF(0) + 0.62, "ding", 0.6), ("sig", SF(1) + 0.15, "ding", 0.6),
    ("sig", SF(2), "glitch", 0.45), *beats("sig", SF(2), SF(3) - SF(2), 0.38, 0.8),
    *[("sig", SF(2) + o, "tick", 0.55 + 0.1 * k) for k, o in enumerate((0.1, 0.42, 0.68, 0.88, 1.02, 1.12))],
    ("sig", SF(3) - 1.1, "riser", 0.6),
    ("sig", SF(3), "sting", 1.1), ("sig", SF(3), "boom", 0.8), ("sig", SF(3), "glitch", 0.7), ("sig", SF(3) + 0.12, "slam", 0.7),
    *beats("sig", SF(3), D["sig"] - SF(3), 0.5, 0.7),
    ("mid", 0.0, "lap", 0.7), ("mid", frag("mid", 0, 3), "sting", 0.7), ("mid", frag("mid", 0, 3), "glitch", 0.5), *beats("mid", frag("mid", 0, 3), D["mid"] - frag("mid", 0, 3), 0.45, 0.5),
    ("hands", 0.0, "bubbles", 1.0), ("hands", frag("hands", 0, 1), "sting", 1.0), ("hands", frag("hands", 0, 1), "boom", 0.7), ("hands", frag("hands", 0, 1), "glitch", 0.6), ("hands", 2.0, "bubbles", 0.8),
    *beats("hands", frag("hands", 0, 1), D["hands"] - frag("hands", 0, 1), 0.4, 0.6),
    ("look", 0.0, "lap", 0.6), ("look", vo_t("look") - 0.2, "swell", 0.5),
    ("fall", JOLT, "thud", 0.9), ("fall", JOLT, "glitch", 0.6), ("fall", JOLT + 0.45, "splash", 1.3), ("fall", JOLT + 0.5, "boom", 0.5),
    ("swim", 0.0, "bubbles", 0.8), ("swim", 0.2, "splash", 0.25), ("swim", vo_t("swim") - 0.2, "swell", 0.5), *beats("swim", 0.0, D["swim"], 0.42, 0.55),
    *beats("choice", 0.0, D["choice"] - 0.3, 0.38, 1.0), *[("choice", 0.05 + k * 1.0, "tick", 1.0) for k in range(3)], ("choice", 1.0, "glitch", 0.6),
    ("choice", D["choice"] - 2.2, "riser", 1.0), ("choice", D["choice"] - 0.62, "sting", 1.0), ("choice", D["choice"] - 0.6, "glitch", 0.8), ("choice", D["choice"] - 0.6, "boom", 0.7),
    ("next", 0.3, "whoosh", 0.5), ("next", 0.45, "drip", 0.6), ("next", 0.8, "sting", 0.7), *beats("next", 0.9, D["next"] - 0.9, 0.7, 0.5),
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
dip(T("lure", 0), T("sleep", -0.05), 0.3)
dip(T("out", frag("out", 0, 1)), T("yai", -0.05), 0.35)
dip(T("sig", SF(2)), T("sig", SF(3) + 0.05), 0.05, 0.12)  # silence before "ข้อเดียว"
dip(T("mid", frag("mid", 0, 3)), T("look", -0.05), 0.2)
dip(T("swim", 0), T("choice", -0.3), 0.4)
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

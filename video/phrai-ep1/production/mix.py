"""มือพราย EP.1: build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX for a river on Loy
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


GRAB, YANK = 0.55, 0.95  # the bend shot (same as the composition)
T2 = frag("throw", 0, 2) - 0.15
T3 = frag("throw", 0, 3)
SF = lambda j: frag("sig", 0, j)

CUES = [
    # story opener, its own (OpenerWater.cues, at 1.9 / glide 1.8): the title surfacing, the hands, the drag under, the tilt up, the hit
    ("open", 0.0, "swell", 0.5), ("open", 0.1, "bubbles", 0.8), ("open", 0.95, "boom", 0.35), *[("open", 1.15 + i * 0.12, "plop", 0.55) for i in range(5)], ("open", 1.15, "sting", 0.8),
    ("open", 1.0, "riser", 0.5), ("open", 1.7, "splash", 0.9), ("open", 1.7, "glitch", 0.5), ("open", 1.9, "whoosh", 0.6), ("open", 3.68, "boom", 0.8), ("open", 3.7, "glitch", 0.4),
    ("hook", 0.0, "lap", 0.7), ("hook", 0.7, "bubbles", 0.6), *beats("hook", 0.4, D["hook"] - 0.4, 0.42, 0.5), ("hook", D["hook"] - 0.45, "sting", 1.0), ("hook", D["hook"] - 0.45, "glitch", 0.7), ("hook", D["hook"] - 0.4, "boom", 0.6),
    ("back", 0.0, "rewind", 0.8), ("back", 0.05, "glitch", 0.4), ("back", 0.5, "ching", 0.4),
    ("dusk", 0.0, "lap", 0.6), ("dusk", 0.3, "swell", 0.3),
    ("arrive", 0.1, "steps", 0.4), ("arrive", 0.7, "steps", 0.35),
    ("coins", 0.4, "ching", 0.3), ("coins", 0.8, "ching", 0.25),
    ("warn", frag("warn", 0, 1), "swell", 0.4), *beats("warn", frag("warn", 0, 1), 1.6, 0.6, 0.3),
    ("rule", 0.0, "swell", 0.45), *[("rule", frag("rule", 0, j), "sting", 0.35) for j in (0, 2, 4)], ("rule", 3.0, "lap", 0.5), ("rule", 7.0, "lap", 0.5),
    ("legend", 0.05, "gong", 0.7), ("legend", 0.3, "bubbles", 0.5), ("legend", frag("legend", 0, 2) - 0.1, "whoosh", 0.4), ("legend", frag("legend", 1) - 0.1, "whoosh", 0.4),
    ("legend", frag("legend", 1, 1) - 0.1, "sting", 0.7), ("legend", frag("legend", 1, 1), "glitch", 0.5), ("legend", D["legend"] - 1.0, "gong", 0.45),
    ("traits", 0.35, "glitch", 0.5), ("traits", 0.35, "swell", 0.5), ("traits", frag("traits", 1, 1), "whoosh", 0.3),
    ("traits", frag("traits", 2, 1), "sting", 0.8), ("traits", frag("traits", 2, 1), "splash", 0.4), ("traits", frag("traits", 2, 1) + 0.1, "bubbles", 0.6),
    ("cant", 0.0, "lap", 0.8), *beats("cant", frag("cant", 0, 1), D["cant"] - frag("cant", 0, 1), 0.45, 0.4), ("cant", frag("cant", 0, 1), "swell", 0.4),
    ("crowd", 0.0, "lap", 0.6), ("crowd", 0.0, "rustle", 0.3),
    ("mhem", 0.0, "lap", 0.7), ("mhem", 1.4, "creak", 0.35),
    ("kids", 0.0, "lap", 0.6), ("kids", 0.8, "plop", 0.4), ("kids", 1.9, "plop", 0.35),
    ("know", 0.0, "lap", 0.5),
    ("under", frag("under", 0, 1) - 0.1, "whoosh", 0.6), ("under", frag("under", 0, 1), "bubbles", 0.9), *beats("under", frag("under", 0, 1), D["under"] - frag("under", 0, 1), 0.45, 0.5), ("under", D["under"] - 0.6, "glitch", 0.4),
    ("gone", 0.0, "rustle", 0.3), *beats("gone", 1.0, D["gone"] - 1.0, 0.42, 0.45), ("gone", 1.0, "sting", 0.5),
    ("whisper", 0.0, "lap", 0.9), ("whisper", vo_t("whisper") - 0.2, "swell", 0.5), *beats("whisper", vo_t("whisper"), D["whisper"] - vo_t("whisper"), 0.45, 0.5), ("whisper", frag("whisper", 0, 1), "glitch", 0.4),
    ("five", 0.0, "lap", 0.7), ("five", 0.3, "ching", 0.35), ("five", 1.3, "ching", 0.3), ("five", 2.3, "ching", 0.3),
    ("bend", GRAB, "sting", 1.0), ("bend", GRAB, "glitch", 0.7), ("bend", YANK + 0.25, "splash", 1.3), ("bend", YANK + 0.3, "boom", 0.7),
    ("scream", 0.0, "whoosh", 0.6), ("stop", 0.0, "steps", 0.6), ("stop", 0.35, "thud", 0.5),
    ("hug", 0.0, "bubbles", 1.0), ("hug", 1.5, "bubbles", 0.8), *beats("hug", frag("hug", 0, 2), D["hug"] - frag("hug", 0, 2), 0.45, 0.5),
    ("how", 0.0, "lap", 0.8), ("how", 0.4, "plop", 0.4), ("how", 1.6, "plop", 0.4), ("how", 2.8, "plop", 0.4),
    ("shout", 0.0, "lap", 0.6), ("shout", vo_t("shout"), "whoosh", 0.3),
    ("throw", 0.2, "rustle", 0.4), ("throw", T2 + 0.4, "plop", 0.5), ("throw", T3 - 0.05, "whoosh", 0.8), ("throw", T3 + 0.9, "plop", 0.9), ("throw", T3 + 0.9, "splash", 0.35),
    ("reach", 0.0, "lap", 0.7), ("reach", 0.4, "creak", 0.5), ("reach", frag("reach", 0, 3) - 0.1, "sting", 0.9), ("reach", frag("reach", 0, 3) - 0.1, "glitch", 0.6), ("reach", frag("reach", 0, 3), "splash", 0.4),
    *beats("reach", frag("reach", 0, 2), D["reach"] - frag("reach", 0, 2), 0.42, 0.5),
    ("leg", 0.1, "drip", 0.5), ("leg", 0.6, "drip", 0.4), ("leg", 1.3, "drip", 0.4), *beats("leg", frag("leg", 0, 1), D["leg"] - frag("leg", 0, 1), 0.45, 0.5),
    # channel signature
    ("sig", 0.05, "glitch", 0.35), ("sig", 0.05, "beep", 0.35),
    ("sig", SF(0) + 0.3, "ding", 0.6), ("sig", SF(0) + 0.62, "ding", 0.6), ("sig", SF(1) + 0.15, "ding", 0.6),
    ("sig", SF(2), "glitch", 0.45), *beats("sig", SF(2), SF(3) - SF(2), 0.38, 0.8),
    *[("sig", SF(2) + o, "tick", 0.55 + 0.1 * k) for k, o in enumerate((0.1, 0.42, 0.68, 0.88, 1.02, 1.12))],
    ("sig", SF(3) - 1.1, "riser", 0.6),
    ("sig", SF(3), "sting", 1.1), ("sig", SF(3), "boom", 0.8), ("sig", SF(3), "glitch", 0.7), ("sig", SF(3) + 0.12, "slam", 0.7),
    *beats("sig", SF(3), D["sig"] - SF(3), 0.5, 0.7),
    ("marks", frag("marks", 0, 1), "swell", 0.5), ("marks", frag("marks", 0, 2), "sting", 0.9), ("marks", frag("marks", 0, 2), "glitch", 0.5), *beats("marks", frag("marks", 0, 1), D["marks"] - frag("marks", 0, 1), 0.42, 0.55),
    ("shadow", 0.0, "lap", 0.7), ("shadow", frag("shadow", 0, 2), "sting", 1.0), ("shadow", frag("shadow", 0, 2), "glitch", 0.6), ("shadow", frag("shadow", 0, 2), "boom", 0.5),
    *[("night", frag("night", 0, 1) + k * 0.28, "drip", 0.6) for k in range(7)], *beats("night", frag("night", 0, 1), D["night"] - frag("night", 0, 1), 0.45, 0.5),
    ("call", 0.0, "lap", 0.9), ("call", 0.3, "steps", 0.25), ("call", vo_t("call") - 0.2, "swell", 0.5), *beats("call", 0.0, D["call"], 0.45, 0.5),
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


dip(0.0, T("open", -0.05), 0.25, 0.05)
dip(T("hook", 0), T("hook", -0.05), 0.35)
dip(T("legend", 0), T("traits", -0.2), 0.5)
dip(T("under", frag("under", 0, 1)), T("under", -0.05), 0.3)
dip(T("whisper", 0), T("bend", YANK + 0.2), 0.2)
dip(T("sig", SF(2)), T("sig", SF(3) + 0.05), 0.05, 0.12)  # silence before "ข้อเดียว"
dip(T("marks", 0), T("shadow", -0.05), 0.35)
dip(T("night", 0), T("call", -0.05), 0.3)
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

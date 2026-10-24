"""ควันหลง EP.3: build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX for a night drive in fog
(engine, tyre screech, the hazard relay, the handbrake, a knock on the glass, the power window) and the Suno music bed with dips
before the scares and sidechain ducking under the voice. Output -14 LUFS, hard cut to silence at the end."""
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


CUES = [
    ("recap", 0.0, "swell", 0.6), *beats("recap", 0.0, D["recap"], 0.38, 0.8), ("recap", D["recap"] - 0.35, "glitch", 0.7), ("recap", D["recap"] - 0.3, "boom", 0.5),
    ("hook", 0.3, "sting", 0.6), ("hook", 0.35, "slam", 0.4), ("hook", 0.5, "steps", 0.3), ("hook", 1.8, "steps", 0.3), *beats("hook", 1.0, D["hook"] - 1.0, 0.5, 0.35),
    ("foot", 0.2, "rustle", 0.4), ("foot", 1.0, "swell", 0.5), *beats("foot", 1.0, D["foot"] - 1.0, 0.42, 0.45),
    ("pull", 0.1, "whoosh", 0.9), ("pull", 0.15, "thud", 0.7), ("pull", 0.12, "glitch", 0.5),
    ("shut", 0.6, "motor", 0.7), ("shut", 2.75, "thud", 0.6), ("shut", 2.8, "sting", 0.6), *beats("shut", 0.6, D["shut"] - 0.6, 0.45, 0.5),
    *[("count", 0.2 + k * (frag("count", 0, 1) - 0.9) / 7, "tick", 0.5) for k in range(7)], ("count", frag("count", 0, 2), "ding", 0.8), ("count", frag("count", 0, 2), "glitch", 0.4),
    *[("count", frag("count", 0, 2) + 0.1 + k * 0.6, "tick", 0.6) for k in range(4)], *beats("count", frag("count", 0, 2), D["count"] - frag("count", 0, 2), 0.5, 0.5),
    ("rule", 0.0, "crackle", 0.8),
    ("this", 0.0, "creak", 0.8), ("this", 0.3, "steps", 0.5),
    ("stairs", 0.0, "steps", 0.7), ("stairs", 1.3, "steps", 0.7), ("stairs", 2.6, "steps", 0.6), ("stairs", frag("stairs", 0, 2) - 0.3, "crackle", 1.0), ("stairs", frag("stairs", 0, 2) + 0.15, "slam", 0.8), ("stairs", frag("stairs", 0, 2) + 0.15, "thud", 0.6),
    ("onfire", 0.05, "sting", 0.9), ("onfire", 0.05, "glitch", 0.6), ("onfire", 0.0, "crackle", 1.0), *beats("onfire", 0.2, D["onfire"] - 0.2, 0.36, 0.6),
    ("sdr", 0.0, "crackle", 0.8), ("sdr", vo_t("sdr") + SH["sdr"]["vo"][0]["frags"][1], "thud", 0.6), *[("sdr", vo_t("sdr", 1) + k * 0.42, "rustle", 0.5) for k in range(6)],
    ("out", 0.2, "swell", 0.35),
    ("up", 0.2, "swell", 0.5), *beats("up", 1.5, D["up"] - 1.5, 0.42, 0.5), ("up", D["up"] - 1.0, "riser", 0.7),
    ("drop", 0.3, "growl", 0.6), ("drop", 0.9, "shriek", 1.0), ("drop", 0.95, "boom", 1.0), ("drop", 0.95, "glitch", 0.8), ("drop", 1.15, "slam", 0.8),
    # channel signature
    ("sig", 0.05, "glitch", 0.35), ("sig", 0.05, "beep", 0.35),
    ("sig", frag("sig", 0, 0) + 0.3, "ding", 0.6), ("sig", frag("sig", 0, 0) + 0.62, "ding", 0.6), ("sig", frag("sig", 0, 1) + 0.15, "ding", 0.6),
    ("sig", frag("sig", 0, 2), "glitch", 0.45), *beats("sig", frag("sig", 0, 2), frag("sig", 0, 3) - frag("sig", 0, 2), 0.38, 0.8),
    *[("sig", frag("sig", 0, 2) + o, "tick", 0.55 + 0.1 * k) for k, o in enumerate((0.1, 0.42, 0.68, 0.88, 1.02, 1.12))],
    ("sig", frag("sig", 0, 3) - 1.1, "riser", 0.6),
    ("sig", frag("sig", 0, 3), "sting", 1.1), ("sig", frag("sig", 0, 3), "boom", 0.8), ("sig", frag("sig", 0, 3), "glitch", 0.7), ("sig", frag("sig", 0, 3) + 0.12, "slam", 0.7),
    *beats("sig", frag("sig", 0, 3), D["sig"] - frag("sig", 0, 3), 0.5, 0.7),
    ("signs", 0.0, "steps", 0.5), ("signs", 1.4, "steps", 0.5), *[("signs", vo_t("signs") + SH["signs"]["vo"][0]["frags"][1] + k * 0.9, "tick", 0.6) for k in range(3)],
    ("seven", frag("seven", 0, 2), "sting", 1.1), ("seven", frag("seven", 0, 2), "boom", 0.8), ("seven", frag("seven", 0, 2), "glitch", 0.7), *beats("seven", frag("seven", 0, 2) + 0.3, D["seven"] - frag("seven", 0, 2) - 0.3, 0.42, 0.6),
    ("key", 0.3, "ching", 0.4), ("key", vo_t("key", 1) - 0.2, "knock", 0.9), ("key", vo_t("key", 1) - 0.0, "knock", 0.9), ("key", vo_t("key", 1) + 0.3, "glitch", 0.5), ("key", vo_t("key", 1), "crackle", 0.8),
    *beats("key", vo_t("key", 1), D["key"] - vo_t("key", 1), 0.42, 0.6),
    *beats("choice", 0.0, D["choice"] - 0.3, 0.38, 1.0), *[("choice", 0.05 + k * 1.0, "tick", 1.0) for k in range(3)], ("choice", 1.0, "glitch", 0.6),
    ("choice", D["choice"] - 2.2, "riser", 1.0), ("choice", D["choice"] - 0.62, "sting", 1.0), ("choice", D["choice"] - 0.6, "glitch", 0.8), ("choice", D["choice"] - 0.6, "boom", 0.7),
    ("next", 0.3, "whoosh", 0.5), ("next", 0.45, "ching", 0.5), ("next", 0.8, "sting", 0.7), *beats("next", 0.9, D["next"] - 0.9, 0.7, 0.5),
]
# no hiss: the noise-based wind bed reads as static under the voice (user: "ลบเสียงซ่าออก"), and the fire keeps only a faint crackle
CUES = [(k, t, typ, g * (0.3 if typ == "crackle" else 1)) for k, t, typ, g in CUES if typ not in ("wind",)]
CUES = [c for c in CUES if c[3] > 0]
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
dip(T("foot", 0), T("foot", -0.05), 0.4)
dip(T("up", 0), T("drop", 1.2), 0.25)
dip(T("drop", 1.25), T("drop", -0.02), 0.0, 0.05)
dip(T("sig", frag("sig", 0, 2)), T("sig", frag("sig", 0, 3) + 0.05), 0.05, 0.12)  # silence before "ข้อเดียว"
dip(T("key", vo_t("key", 1) - 0.3), T("key", -0.05), 0.3)
dip(T("choice", 0), T("choice", -0.3), 0.5)
boost = np.ones(N, np.float32)
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

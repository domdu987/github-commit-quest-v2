"""เต็นท์ผีอำ EP.3 (ตอนจบ): build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX for a campsite on a
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
QB, QHT, QD = vo_t("ghost") - 0.2, D["ghost"] - 0.9, D["ghost"] - 0.45  # the shape at the foot of the bed: eyes, the dark, the hit


CUES = [
    ("recap", 0.0, "hum", 0.3), *beats("recap", 0.0, D["recap"], 0.6, 0.6), ("recap", D["recap"] - 0.3, "glitch", 0.5),
    ("hook", 0.0, "crackle", 0.25), ("hook", F("hook", 1, 0), "swell", 0.4), *beats("hook", F("hook", 1, 0), D["hook"] - F("hook", 1, 0) - 0.3, 0.5, 0.5),
    ("hook", D["hook"] - 0.3, "sting", 0.8), ("hook", D["hook"] - 0.3, "glitch", 0.6),
    ("wakeup", 0.2, "beep", 0.25), ("wakeup", 1.2, "beep", 0.25), ("wakeup", 2.2, "beep", 0.25),
    ("almost", vo_t("almost"), "thud", 0.3),
    ("know1", 0.3, "riser", 0.3), ("know1", F("know1", 0, 2) - 0.2, "clang", 0.4), ("know1", F("know1", 0, 2), "ding", 0.35),
    *[("know2", 0.4 + k * 0.35, "pop", 0.2) for k in range(6)], ("know2", F("know2", 0, 1), "swell", 0.3),
    ("know3", vo_t("know3") + 0.5, "click", 0.45), ("know3", F("know3", 0, 1), "whoosh", 0.3), ("know3", F("know3", 0, 1) + 0.3, "ding", 0.3),
    ("quit", vo_t("quit") + 0.1, "gong", 0.3), ("week", vo_end("week") - 0.1, "pop", 0.3),
    ("know4", 0.2, "ding", 0.3), ("know5", F("know5", 0, 1), "sting", 0.35), ("know5", F("know5", 0, 1) + 0.2, "ring", 0.25),
    ("visit", 0.1, "steps", 0.3), ("visit", 0.5, "steps", 0.3), ("visit", 0.9, "creak", 0.3),
    ("mem1", 0.0, "rewind", 0.5), ("mem1", 0.6, "crackle", 0.3),
    ("mem2", 0.2, "squelch", 0.35), ("mem2", F("mem2", 0, 1), "swell", 0.4), *beats("mem2", F("mem2", 0, 1), D["mem2"] - F("mem2", 0, 1), 0.6, 0.5),
    *beats("realize", 0.0, D["realize"], 0.55, 0.5), ("realize", 0.2, "swell", 0.3),
    ("father", F("father", 0, 1), "swell", 0.35), *beats("father", F("father", 0, 1), D["father"] - F("father", 0, 1), 0.6, 0.45),
    ("rule", 0.1, "ding", 0.35), ("rule", 0.25, "ding", 0.35), ("rule", vo_t("rule") + 0.2, "ding", 0.45), ("rule", vo_t("rule") + 0.2, "swell", 0.3),
    ("home", 0.0, "crickets", 0.2), ("home", 0.4, "tick", 0.25), ("home", 1.4, "tick", 0.25), ("home", 2.4, "tick", 0.25),
    ("talk", F("talk", 0, 2), "swell", 0.35), *beats("talk", F("talk", 0, 2), D["talk"] - F("talk", 0, 2), 0.55, 0.45),
    ("coal", 0.0, "crackle", 0.35), ("coal", F("coal", 0, 1), "swell", 0.45), *beats("coal", 0.0, D["coal"], 0.55, 0.55),
    # koi-style: the shape, the eyes, the whisper, a slow heartbeat; one hit and cut
    ("ghost", 0.0, "crackle", 0.3), *beats("ghost", 0.0, QHT, 0.6, 0.65), ("ghost", QB, "swell", 0.3),
    ("ghost", QD, "sting", 1.1), ("ghost", QD, "slam", 0.7), ("ghost", QD + 0.02, "shriek", 0.5),
    ("end", 0.4, "whoosh", 0.5), ("end", 0.55, "crickets", 0.4), ("end", 0.9, "gong", 0.5),
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


dip(0.0, T("hook", -0.05), 0.3, 0.1)
dip(T("mem1", 0), T("father", -0.05), 0.45)
dip(T("talk", 0), T("ghost", 0), 0.2)
dip(T("ghost", 0), T("ghost", -0.05), 0.05, 0.1)
mus = mus * gain
end = int(T("ghost", -0.2) * SR)
mus[end:] = 0  # hard cut to black and silence

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mix = vo + mus * duck + sfx
cut, card = int(T("ghost", -0.2) * SR), int(T("end", 0.4) * SR)
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

"""ห้องสอบ EP.1 soundtrack: levelled voices, ElevenLabs effects (video/exam/sfxlib) + a few synth accents, the bed with dips. -14 LUFS, no noise beds."""
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


# ---- voice ----
LINE_GAIN = {"k03": 2, "k04": 2}
vo = np.zeros(N, np.float32)
for s in SC["shots"]:
    for v in s["vo"]:
        x = load(os.path.join(HERE, "vo", f"{v['id']}.wav"))
        place(vo, level(x, -18 + LINE_GAIN.get(v["id"], 0)), s["start"] + v["t"])
D = {k: SH[k]["dur"] for k in SH}
F = frag
def beats(k, t0, dur, period, g=0.3):
    return [(k, t0 + i * period, "heartbeat", g) for i in range(int((dur - 0.1) / period) + 1)]
def ticks(k, a, b, g=0.2, step=1.0):
    return [(k, a + i * step, "tick", g) for i in range(int((b - a) / step) + 1)]
dd = D["drag"] - 0.9
CUES = [
    ("hook", 0.0, "sting", 0.3), ("dont", 0.35, "thud", 0.3),
    *ticks("clock", 0.05, 1.25, 0.3),
    ("viral", 0.1, "whoosh", 0.2),
    *[("rule", 0.25 + a, "pop", 0.18) for a in (0.2, 0.55, 0.9, 1.3)],
    ("desk", F("desk", 0, 1), "sting", 0.22),
    *beats("hide", 0.3, D["hide"] - 0.3, 0.75, 0.26),
    *[("rooms", F("rooms", 0, k), "thud", 0.2) for k in range(3)],
    *beats("stop", 1.5, D["stop"] - 1.5, 0.5, 0.32), *beats("breath", 0.0, D["breath"] - 0.4, 0.42, 0.34),
    ("buzz", D["buzz"] - 0.25, "sting", 0.35),
    ("next", 0.1, "whoosh", 0.3), ("next", 0.6, "ding", 0.22),
]
exec(open(os.path.join(HERE, "..", "samples_inc.py")).read())
SAMPLES = [
    ("hook", 0.0, "glassslam", 1.0), ("hook", 0.02, "glasscrack", 0.6), ("hook", 0.3, "groan", 0.18), ("hook", 1.2, "handslap", 0.55), ("hook", 1.25, "glasscrack", 0.25),
    ("dont", 0.0, "groan", 0.35, 1.6),
    ("calm", 0.0, "classroom", 0.55, 4.84), ("clock", 0.0, "classroom", 0.45, 3.85), ("clock", 1.6, "doorbang", 0.85), ("joke", 0.0, "classroom", 0.4, 3.1),
    ("scream", 0.05, "scream", 0.95), ("scream", 0.4, "flicker", 0.35, 2.8), ("scream", 1.4, "groan", 0.45),
    ("slam", 0.1, "glassslam", 1.0), ("slam", 0.2, "bodyfall", 0.8),
    ("lock", 0.3, "lockturn", 0.9), ("lock", F("lock", 0, 1) - 0.12, "lightsoff", 0.8),
    ("latch", 0.3, "cabinet", 0.45, 1.6),
    ("drag", 0.0, "deskdrag", 0.95, dd + 0.05), ("drag", dd, "deskthud", 1.0),
    ("steps", 0.0, "shuffle", 0.85, D["steps"]), ("steps", 0.2, "flicker", 0.35, 2.5), ("steps", 1.1, "groan", 0.4),
    ("rooms", 0.0, "shuffle", 0.7, D["rooms"]), ("stop", 0.0, "shuffle", 0.7, 1.4),
    ("breath", 0.2, "breath", 0.7),
    ("buzz", 0.4, "phonebuzz", 0.9, D["buzz"] - 0.6), ("buzz", 1.95, "groan", 0.55),
]
cues = {"duration": TOTAL, "sections": [{"start": 0, "end": TOTAL, "mood": "silence"}],
        "sfx": [{"t": round(t if k is None else T(k, t), 3), "type": typ, "gain": g} for k, t, typ, g in CUES]}
json.dump(cues, open(os.path.join(HERE, "sfx_cues.json"), "w"))
subprocess.run(["python3", os.path.join(HERE, "..", "synth.py"), os.path.join(HERE, "sfx_cues.json"), os.path.join(HERE, "sfx.wav")],
               check=True, env={**os.environ, "STEMS": "1"})
sfx = load(os.path.join(HERE, "sfx_sfx.wav"))[:N]
sfx = np.pad(sfx, (0, N - len(sfx)))
for k, t0, name, g, *mx in SAMPLES:
    place(sfx, smp(name, mx[0] if mx else None), T(k, t0), g)

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


dip(T("calm", 0), T("joke", -0.01), 0.45)        # the quiet exam room
dip(T("hide", 0), T("desk", -0.01), 0.4)
dip(T("stop", 0), T("buzz", -0.3), 0.12)         # the held breath: near silence before the buzz
mus = mus * gain
a, b = int(T("next", 0) * SR), int(T("next", -0.01) * SR)
mus[a:b] *= np.linspace(1, 0, b - a)
mus[b:] = 0

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mix = vo + mus * duck + sfx
peak = np.max(np.abs(mix))
if peak > 0.98:
    mix = np.tanh(mix / peak * 1.2) * 0.95
out = os.path.join(HERE, "mix_raw.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", out],
               input=mix.astype(np.float32).tobytes(), check=True)
# single-pass loudnorm lands ~0.8 dB under its target on this mix: aim at -13.2 to measure -14
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", "loudnorm=I=-13.2:TP=-1.5:LRA=11", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)
print("mix written", TOTAL)

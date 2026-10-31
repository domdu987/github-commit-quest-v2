"""หมาดำตาสี่ EP.N: the soundtrack from schedule.json: levelled voice, synthesized SFX (crickets, engine, the lock click, the countdown
ticks, the screech, the splash, water pouring in, bubbles, the window motor, the rewind, the child's switch, the flicker) and the Suno bed
with dips and ducking; the bed fades out over the next-episode card. Output -14 LUFS, no noise beds."""
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
LINE_GAIN = {}
vo = np.zeros(N, np.float32)
for s in SC["shots"]:
    for v in s["vo"]:
        x = load(os.path.join(HERE, "vo", f"{v['id']}.wav"))
        place(vo, level(x, -18 + LINE_GAIN.get(v["id"], 0)), s["start"] + v["t"])
D = {k: SH[k]["dur"] for k in SH}
F = frag


def beats(k, t0, dur, period, g=0.9):
    return [(k, t0 + i * period, "heartbeat", g) for i in range(int((dur - 0.1) / period) + 1)]


exec(open(os.path.join(HERE, "..", "samples_inc.py")).read())
REPLACED = set()
CUES = [
    ("hook", 0.0, "swell", 0.24), ("cmd", 0.05, "sting", 0.42), ("warn", 0.05, "rewind", 0.3),
    *beats("hide", 0.3, D["hide"] - 0.3, 0.7, 0.28), ("snap", 2.4, "thud", 0.45), ("snap", 2.42, "sting", 0.45),
    ("home", 0.1, "whoosh", 0.25), ("home", F("home", 0, 2) + 0.1, "thud", 0.3),
    ("khiao", 0.0, "sting", 0.2), ("pen", 0.2, "whoosh", 0.18), ("map", 0.2, "whoosh", 0.22), ("map", 2.6, "ding", 0.22),
    ("race", 0.1, "whoosh", 0.25), *beats("race", 0.4, 1.8, 0.4, 0.28), ("race", F("race", 0, 3), "sting", 0.35),
    ("rule", vo_end("rule") + 0.3, "whoosh", 0.25), ("rule", vo_end("rule") + 0.9, "ding", 0.2), ("confess", vo_end("confess") - 0.6, "sting", 0.35),
    ("rw", vo_t("rw", 1) - 0.8, "sting", 0.32), ("ear", 0.5, "sting", 0.4),
    ("day6", 0.0, "swell", 0.22), ("final", 0.1, "whoosh", 0.28), ("final", 0.9, "ding", 0.26),
]
SAMPLES = [
    ("hook", 0.0, "daybed", 0.3, 3.4), ("hook", 0.3, "dogpant", 0.55), ("cmd", 0.0, "daybed", 0.25, 1.8),
    ("warn", 0.8, "nightvil", 0.35, 3.3), ("hide", 0.0, "nightvil", 0.35, 6.4), ("hide", 1.6, "growl", 0.45),
    ("snap", 0.0, "nightvil", 0.3, 4.6), ("snap", 0.6, "growl", 0.7), ("snap", 2.3, "snap", 1.0),
    ("herb", 0.0, "mortar", 0.5), ("herb", 2.4, "mortar", 0.4), ("home", 0.9, "dogfight", 0.5),
    ("khiao", 0.0, "daybed", 0.3, 3.0), ("pen", 0.0, "daybed", 0.25, 5.4), ("pen", 0.5, "chain", 0.75),
    ("map", 0.2, "moto", 0.5), ("race", 0.0, "clinic", 0.25, 5.5), ("rule", 0.0, "clinic", 0.3, 5.1), ("rule", vo_end("rule") + 0.35, "zinc", 0.5), ("rule", vo_end("rule") + 0.8, "chalk", 0.55),
    ("confess", 0.0, "clinic", 0.3, 4.3), ("rw", 0.0, "clinic", 0.25, 2.5), ("rw", vo_t("rw", 1) - 0.8, "rewind", 0.8),
    ("ear", 0.0, "daybed", 0.22, 3.9), ("day6", 0.0, "nightvil", 0.25, 5.0), ("end", 0.0, "nightvil", 0.22, 4.4), ("final", 0.6, "chalk", 0.5),
]


def music_dips(dip):
    dip(T("hide", 0), T("snap", -0.01), 0.45)
    dip(T("day6", 0), T("end", -0.01), 0.5)
# no hiss: the noise-based wind bed reads as static under the voice (user: "ลบเสียงซ่าออก")
CUES = [c for c in CUES if c[2] not in ("wind", "lap", "pop", "tick") and c[3] > 0]   # no HUD: no chip pops, no countdown ticks (user 31 ต.ค.)  # no noise beds (user: "เสียงซ่าๆเอาออก")
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


music_dips(dip)
mus = mus * gain
a, b = int(T("final", 0) * SR), int(T("final", -0.01) * SR)
mus[a:b] *= np.linspace(1, 0, b - a)   # no cliffhanger: the bed fades out over the end card
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

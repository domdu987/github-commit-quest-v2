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
    ("hook", 0.0, "swell", 0.24), ("cmd", 0.05, "sting", 0.42), ("knee", 0.1, "whoosh", 0.2),
    ("clock", 0.1, "rewind", 0.3), ("legend", 0.0, "swell", 0.2), ("legend", 3.6, "sting", 0.25), ("rule", vo_end("rule") + 0.4, "whoosh", 0.25), ("rule", vo_end("rule") + 1.0, "ding", 0.2),
    ("age", 0.1, "whoosh", 0.25), ("age", 1.3, "ding", 0.2), ("saliva", 0.1, "whoosh", 0.25), ("saliva", 1.0, "ding", 0.2),
    ("sick", 0.1, "swell", 0.2), *beats("sick", 0.3, D["sick"] - 0.3, 0.6, 0.3), ("pull", 0.0, "sting", 0.28),
    ("rw", vo_t("rw", 1) - 0.8, "sting", 0.32), ("lick", vo_end("lick") - 0.4, "sting", 0.4),
    *beats("night", 0.2, D["night"] - 0.2, 0.45, 0.32), ("ear", 0.2, "swell", 0.24), ("ear", vo_t("ear") + 1.2, "sting", 0.4),
    *beats("choice", 0.2, D["choice"] - 0.2, 0.5, 0.3), ("choice", D["choice"] - 1.3, "thud", 0.4),
    ("next", 0.1, "whoosh", 0.3), ("next", 0.6, "ding", 0.24),
]
SAMPLES = [
    ("hook", 0.0, "daybed", 0.3, 4.4), ("hook", 0.05, "pupwhine", 0.7), ("hook", 1.2, "puplick", 0.7),
    ("cmd", 0.0, "daybed", 0.25, 1.5), ("knee", 0.2, "puplick", 0.9),
    ("arrive", 0.0, "van", 0.5), ("arrive", 0.0, "daybed", 0.3, 3.8), ("arrive", 1.2, "bark", 0.25),
    ("yai", 0.0, "daybed", 0.3, 3.8), ("yai", 0.5, "dogpant", 0.6),
    ("rule", 0.0, "daybed", 0.22, 5.4), ("rule", vo_end("rule") + 0.5, "zinc", 0.6), ("rule", vo_end("rule") + 0.9, "chalk", 0.6),
    ("hug", 0.0, "daybed", 0.25, 4.7), ("hug", 0.4, "puplick", 0.6), ("hug", 1.6, "pupwhine", 0.45),
    ("sick", 0.0, "pupwhine", 0.4), ("pull", 0.0, "nightvil", 0.25, 4.6),
    ("lick", 0.1, "puplick", 0.8), ("rw", vo_t("rw", 1) - 0.8, "rewind", 0.8),
    ("night", 0.0, "nightvil", 0.4, 3.6), ("night", 0.0, "growl", 0.9), ("night", 1.25, "dogfight", 0.95), ("night", 2.4, "yelp", 0.7),
    ("ear", 0.0, "daybed", 0.25, 3.3), ("ear", 0.4, "dogpant", 0.4),
    ("choice", 0.0, "nightvil", 0.25, 3.2), ("legend", 0.0, "nightvil", 0.3, 7.2), ("legend", 4.2, "growl", 0.35), ("choice", D["choice"] - 1.4, "growl", 0.7),
]


def music_dips(dip):
    dip(T("knee", 0), T("knee", -0.01), 0.5)
    dip(T("night", 0), T("ear", -0.01), 0.4)
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
a, b = int(T("next", 0) * SR), int(T("next", -0.01) * SR)
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

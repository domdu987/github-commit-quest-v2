"""ห้องสอบ EP.2 soundtrack: levelled voices, ElevenLabs effects (video/exam/sfxlib) + a few synth accents, the bed with dips. -14 LUFS, no noise beds."""
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
LINE_GAIN = {"k01": 2, "k02": 1}
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
CUES = [
    ("hook", 0.0, "sting", 0.3), ("dont", 0.35, "thud", 0.3),
    *beats("quiet", 0.2, D["quiet"] - 0.2, 0.7, 0.26),
    ("mute", 0.5, "click", 0.35), *[("mute", a, "pop", 0.18) for a in (0.75, F("mute", 0, 1) + 0.3)],
    *beats("pass", 0.0, F("pass", 0, 2), 0.5, 0.32),
    *ticks("knock", 0.05, 1.2, 0.25, 0.25),
    ("up", 0.3, "whoosh", 0.15),
    ("rule", F("rule", 0, 1) + 0.2, "pop", 0.18), ("rule", vo_t("rule", 1) + 0.6, "pop", 0.18),
    ("key", 1.5, "swell", 0.3),
    ("call", F("call", 0, 1) + 0.4, "pop", 0.18), ("call", vo_t("call", 1) + 0.5, "ding", 0.18),
    ("thirty", F("thirty", 0, 1) + 0.4, "sting", 0.35),
    ("cab", 0.1, "swell", 0.2),
    ("where", D["where"] - 1.0, "sting", 0.3),
    ("end", 0.1, "whoosh", 0.3), ("end", 0.6, "ding", 0.22),
]
exec(open(os.path.join(HERE, "..", "samples_inc.py")).read())
SAMPLES = [
    ("hook", 0.0, "phonebuzz", 1.0, 1.6), ("hook", 1.65, "groan", 0.6),
    ("dont", 0.0, "phonebuzz", 0.6, 1.0),
    ("quiet", 0.3, "breath", 0.45), ("pass", 0.0, "groan", 0.3, 1.6), ("pass", F("pass", 0, 2), "shuffle", 0.7, 2.2),
    ("knock", 1.3 + 0.12, "knock", 1.0), ("cop", 0.0, "knock", 0.6, 1.2),
    ("up", 0.2, "crowdwalk", 0.3, 1.6),
    ("key", 0.05, "knob", 0.9), ("key", 0.7, "keys", 0.9), ("key", 1.4, "dooropen", 0.9),
    ("safe", 0.0, "crowdwalk", 0.5, 2.0), ("call", 0.0, "crowdwalk", 0.4, D["call"]),
    ("cab", 0.0, "cabinet", 0.75),
    ("where", 0.0, "crowdwalk", 0.25, 1.5), ("where", 1.4, "shuffle", 0.4, 1.8),
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


dip(T("hook", 0), T("knock", -0.01), 0.3)       # hiding: near silence
dip(T("key", 0), T("key", -0.01), 0.2)
dip(T("thirty", 0), T("where", -0.01), 0.35)
mus = mus * gain
a, b = int(T("end", 0) * SR), int(T("end", -0.01) * SR)
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

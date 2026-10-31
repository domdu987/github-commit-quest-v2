"""ต่อหัวเสือ EP.1 (from the นาทีก่อนจม mixer): the soundtrack from schedule.json: levelled voice, synthesized SFX (crickets, engine, the lock click, the countdown
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


# ---- voice: every line levelled on its own so whispers and shouts sit at a readable loudness ----
LINE_GAIN = {"t02": 2, "y01": 2, "s01": 1}   # ขิม shouts over the water: lift her line over the bed and effects
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


def monitor(k, a, b, g=0.18, step=1.0):  # a bedside-monitor style beep
    return [(k, a + i * step, "beep", g) for i in range(int((b - a) / step) + 1)]


def ticks(k, a, b, g=0.2, step=1.0):  # the wall clock / the stopwatch
    return [(k, a + i * step, "tick", g) for i in range(int((b - a) / step) + 1)]


def pushes(k, a, b, g=0.12, period=60 / 110):  # the compressions, on the same beat as the rig (Rig.MODES.cpr / MmUI.cpr)
    return [(k, a + i * period, "knock", g) for i in range(int((b - a) / period) + 1)]


def quake(k, a, b, g=0.5, step=2.4):  # the building's rumble, overlapping copies between a and b (seconds into shot k)
    return [(k, a + i * step, "quake", g) for i in range(int(max(0, b - a - 0.5) / step) + 1)]


def tick3(k, a, g=0.3):  # the choice ring: three ticks
    return [(k, a + i * 1.0, "tick", g) for i in range(3)]


CUES = [
    ("hook", 0.0, "swell", 0.24), ("cmd", vo_t("cmd") - 0.02, "sting", 0.32), ("why", 0.1, "whoosh", 0.2),
    ("back", 0.0, "rewind", 0.3), ("legend", 0.0, "swell", 0.2), ("wake", 0.0, "boom", 0.3), ("wake", 0.1, "sting", 0.26),
    ("still", 0.1, "whoosh", 0.18), ("know", 0.1, "whoosh", 0.18), ("rule", 1.0, "whoosh", 0.2),
    ("rw", 0.0, "rewind", 0.42), ("rw", 3.0, "sting", 0.28), ("fine", 0.2, "swell", 0.2), *beats("fine", 0.3, D["fine"] - 0.2, 0.6, 0.3),
    ("next", 0.1, "whoosh", 0.3), ("next", 0.6, "ding", 0.24),
]

exec(open(os.path.join(HERE, "..", "samples_inc.py")).read())
SAMPLES = [
    ("hook", 0.0, "swarm", 0.9, 2.9), ("hook", 0.0, "run", 0.6, 2.9), ("cmd", 0.0, "swarm", 0.85, 1.9),
    ("why", 0.0, "swarmfar", 0.35, 4.6),
    ("back", 0.3, "village", 0.5, 3.6), ("palm", 0.0, "village", 0.45, 3.3), ("palm", 0.0, "swarmfar", 0.25, 3.3),
    ("reveal", 0.0, "village", 0.35, 6.2), ("reveal", 1.6, "swarmfar", 0.55, 4.5),
    ("legend", 0.1, "puppet", 0.7), ("legend", F("legend", 0, 2), "swarmfar", 0.4, 3.5),
    ("sing", 0.0, "village", 0.45, 4.4), ("crazy", 0.0, "village", 0.4, 2.0),
    ("first", 0.0, "hornet1", 0.8, 3.0), ("first", F("first", 0, 2) - 0.05, "swat", 0.9),
    ("still", 0.0, "hornet1", 0.3, 3.0),
    ("wake", 0.0, "swarm", 0.95, 3.0), ("toey", 0.0, "swarm", 0.8, 2.2), ("toey", 0.0, "run", 0.5, 2.2),
    ("rule", 0.0, "swarm", 0.6, 1.2), ("know", 0.0, "swarmfar", 0.3, 5.9),
    ("grab", 0.0, "swarm", 0.8, 3.0), ("grab", 0.5, "run", 0.6, 2.5),
    ("shed", 0.55, "doorslam", 1.0), ("shed", 0.7, "screen", 0.7, 2.2),
    ("rw", 0.0, "swarm", 0.35, 3.0), ("where", 0.0, "swarmfar", 0.25, 2.4),
    ("shrine", 0.0, "swarmfar", 0.55, 2.8), ("fine", 0.0, "swarmfar", 0.3, 2.5),
]
CUES = [c for c in CUES if c[2] not in REPLACED]

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


dip(T("wake", 0), T("grab", -0.01), 0.55)      # the swarm: the bed sits under the buzzing
dip(T("rw", 0), T("fine", -0.01), 0.5)         # the rewind and the reveal
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

"""นาทีก่อนจม EP.1: the soundtrack from schedule.json: levelled voice, synthesized SFX (crickets, engine, the lock click, the countdown
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
LINE_GAIN = {"x01": 2, "q03": 2, "r01": 2, "r02": 2}   # ขิม shouts over the water: lift her line over the bed and effects
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
    # the hook: night wind across the rocks, surf, the far lights (a thin swell), the title thud
    ("hook", 0.0, "swell", 0.28), ("hook", 0.0, "stream", 0.16), ("hook", 0.1, "thunder", 0.22), ("hook", 0.3, "thud", 0.2),
    ("cmd", 0.2, "steps", 0.2), ("cmd", F("cmd", 0, 0), "sting", 0.42),
    ("night", 0.0, "creak", 0.2), ("night", 1.2, "thunder", 0.16), ("night", 3.0, "creak", 0.16), ("night", 4.5, "rattle", 0.14),
    ("lights", 0.0, "swell", 0.2), ("lights", 0.5, "stream", 0.14),
    ("village", 0.1, "rustle", 0.3), ("village", 0.4, "click", 0.2),
    ("spot", 0.15, "whoosh", 0.26), ("spot", D["spot"] * 0.62 + 0.28, "sting", 0.3), ("spot", D["spot"] * 0.62 + 0.3, "thud", 0.24),
    ("wreck", 0.15, "whoosh", 0.22), ("wreck", D["wreck"] * 0.45 + 0.15, "ding", 0.3),
    ("route", 0.2, "whoosh", 0.24), ("route", 0.8, "engine", 0.1), ("route", D["route"] * 0.5, "pop", 0.0), ("route", D["route"] * 0.5, "click", 0.2),
    ("wait", 0.6, "thud", 0.2),
    # dawn: rotor thuds approach; his shout; it leaves
    *[("heli", 0.05 + j * 0.42, "drum", 0.22) for j in range(int(D["heli"] / 0.42))],
    *[("pass", 0.05 + j * 0.45, "drum", 0.22 - j * 0.02) for j in range(int(D["pass"] / 0.45))], ("pass", 1.0, "powerdown", 0.14),
    ("rw", 0.0, "rewind", 0.45), ("rw", F("rw", 0, 1), "sting", 0.34),
    ("vest", 0.3, "rustle", 0.3), ("vest", 1.1, "pop", 0.0), ("vest", 1.1, "ching", 0.28),
    ("lay", 0.3, "rustle", 0.24), ("lay", 1.0, "clang", 0.2), ("lay", 1.2, "whoosh", 0.2), ("lay", vo_t("lay", 1), "ching", 0.4),
    *[("found", 0.05 + j * 0.4, "drum", 0.24) for j in range(int(D["found"] / 0.4))], ("found", 0.1, "radiosq", 0.3), ("found", 0.3, "swell", 0.22),
    # the turn: silence, the radio, a low sting
    ("empty", 0.0, "radiosq", 0.34), ("empty", F("empty", 0, 1), "sting", 0.45), ("empty", F("empty", 0, 1) + 0.1, "boom", 0.3),
    ("truth", 0.0, "rewind", 0.4), ("truth", 0.5, "thunder", 0.18), *beats("truth", 0.6, D["truth"] - 0.6, 0.6, 0.28),
    ("walkoff", 0.0, "steps", 0.14), ("walkoff", 1.0, "steps", 0.12), ("walkoff", 2.2, "thunder", 0.2), *beats("walkoff", 0.1, D["walkoff"] - 0.1, 0.55, 0.32),
    ("end", 0.0, "drum", 0.2), ("end", 0.5, "drum", 0.18), ("end", 1.0, "ding", 0.24), ("end", vo_t("end", 1), "sting", 0.3), ("end", vo_t("end", 1) + 0.1, "swell", 0.2),
    ("fin", 0.1, "whoosh", 0.3), ("fin", 1.1, "thud", 0.4), ("fin", 1.15, "gong", 0.26),
]
SAMPLES = []
REPLACED = set()
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


dip(T("cmd", 0), T("night", 1.0), 0.6)
dip(T("empty", 0), T("walkoff", -0.01), 0.3)
mus = mus * gain
a, b = int(T("fin", 0) * SR), int(T("fin", -0.01) * SR)
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

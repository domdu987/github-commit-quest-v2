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
    # the hook: frame 0 the engine bursts (boom + roar), inside the alarm, masks drop, he screams
    ("hook", 0.0, "boom", 0.5), ("hook", 0.02, "roar", 0.42), ("hook", 0.05, "crackle", 0.3), ("hook", 0.8, "alarm", 0.18), ("hook", 0.85, "rattle", 0.3), ("hook", 1.0, "debris", 0.22),
    ("cmd", 0.0, "rattle", 0.24), ("cmd", F("cmd", 0, 0), "sting", 0.42), ("cmd", 0.1, "crackle", 0.2),
    # 40 minutes before: the calm cabin, a ding, steps, the seat
    ("seat", 0.0, "hum", 0.12), ("seat", 0.1, "steps", 0.2), ("seat", 0.6, "thud", 0.16), ("seat", 1.0, "liftding", 0.16),
    ("nap", 0.0, "hum", 0.12), ("nap", 0.3, "click", 0.2),
    ("map", 0.2, "whoosh", 0.26), ("map", 0.5, "ding", 0.14), ("map", 1.2, "engine", 0.12),
    # the engine bursts
    ("engine", 0.0, "engine", 0.18), ("engine", F("engine", 0, 1) + 0.1, "boom", 0.6), ("engine", F("engine", 0, 1) + 0.12, "roar", 0.4), ("engine", F("engine", 0, 1) + 0.2, "debris", 0.3), ("engine", F("engine", 0, 1) + 0.3, "crackle", 0.3),
    ("brace", 0.0, "alarm", 0.2), ("brace", 0.05, "rattle", 0.32), ("brace", 0.1, "clang", 0.2), *beats("brace", 0.3, D["brace"] - 0.3, 0.42, 0.32),
    ("dive", 0.0, "riser", 0.4), ("dive", 0.0, "roar", 0.32), ("dive", 0.1, "whoosh", 0.34),
    # impact on the island rocks
    ("impact", 0.33, "boom", 0.8), ("impact", 0.35, "debris", 0.6), ("impact", 0.38, "scrape", 0.5), ("impact", 0.42, "splash", 0.5), ("impact", 0.5, "shatter", 0.3), ("impact", 0.6, "crackle", 0.3),
    ("smoke", 0.0, "tinnitus", 0.2), ("smoke", 0.4, "crackle", 0.26), ("smoke", 1.2, "creak", 0.2), ("smoke", 1.6, "hiss", 0.0),
    ("grab", 0.1, "crackle", 0.22), ("grab", 0.4, "rustle", 0.26), *beats("grab", 0.2, D["grab"] - 0.2, 0.45, 0.26),
    # the cards: an entry whoosh, ticking stopwatch for 90 s, pops of bags, the jam (thud + sting)
    ("ninety", 0.15, "whoosh", 0.26), *ticks("ninety", 0.6, D["ninety"] - 0.3, 0.16, 0.5), ("ninety", D["ninety"] - 0.7, "ding", 0.24),
    ("half", 0.15, "whoosh", 0.24), *[("half", 1.0 + j * 0.22, "pop", 0.0) for j in range(5)], *[("half", 1.0 + j * 0.22, "click", 0.22) for j in range(5)], ("half", 2.2, "sting", 0.2),
    ("block", 0.15, "whoosh", 0.24), ("block", 0.4, "steps", 0.2), ("block", 1.35, "thud", 0.4), ("block", 1.36, "sting", 0.3),
    # he drops it, runs the wrong way into the heat
    ("run", 0.2, "thud", 0.26), ("run", 0.9, "steps", 0.3), ("run", 1.6, "steps", 0.3), ("run", 0.5, "crackle", 0.3), ("run", D["run"] - 0.8, "roar", 0.4), *beats("run", 0.2, D["run"] - 0.2, 0.38, 0.32),
    ("behind", 0.2, "steps", 0.28), ("behind", 1.0, "steps", 0.28), ("behind", 0.1, "crackle", 0.2), *beats("behind", 0.2, D["behind"] - 0.2, 0.38, 0.3),
    ("rows", 0.15, "whoosh", 0.24), *[("rows", 0.6 + j * 0.22, "click", 0.16) for j in range(8)], ("rows", 2.8, "ding", 0.3),
    # out: the door, down the slide, the surf; the card ticks
    ("jump", 0.75, "whoosh", 0.3), ("jump", 0.75, "thud", 0.3), ("jump", 0.9, "roar", 0.2), ("jump", 0.8, "crackle", 0.14),
    # alone: the surf, the gulls, then the smoke across the bay (sting)
    ("alone", 0.0, "stream", 0.16), ("alone", 1.0, "flap", 0.18), ("alone", 3.0, "flap", 0.14), ("alone", vo_t("alone", 2), "sting", 0.34), ("alone", vo_t("alone", 2) + 0.2, "swell", 0.2),
    ("next", 0.1, "whoosh", 0.3), ("next", 0.8, "ding", 0.24),
]
import sys; sys.path.insert(0, "/home/user/github-commit-quest-v2/video/lib-shared/sfx"); import iconfx_mix
_ic, SAMP = iconfx_mix.split(json.load(open(os.path.join(HERE, "iconfx_cues.json"))) if os.path.exists(os.path.join(HERE, "iconfx_cues.json")) else [], N, SR)
CUES += [(None, c["t"], c["type"], c["gain"]) for c in _ic]
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
mus = load(os.path.join(HERE, "..", "music", "plane-theme.mp3"))   # theme score (owner 1 Nov: "ซาวเพลงทำให้เข้าธีมด้วย")
mus = mus[int(max(0.0, len(mus) / SR - TOTAL - 1.0) * SR):]   # start so the track's peak (its last ~20 s) lands on the cliffhanger
while len(mus) < N:
    mus = np.concatenate([mus, mus])
mus = mus[:N]
t = np.arange(N) / SR
gain = np.ones(N, np.float32)


def dip(t0, t1, lvl, ramp=0.25):
    a = np.clip((t - (t0 - ramp)) / ramp, 0, 1) * np.clip(((t1 + ramp) - t) / ramp, 0, 1)
    np.minimum(gain, 1 - (1 - lvl) * a, out=gain)


dip(T("impact", 0), T("smoke", 1.0), 0.35)
dip(T("alone", vo_t("alone", 2) - 0.3), T("next", 0), 0.4)
mus = mus * gain
a, b = int(T("next", 0) * SR), int(T("next", -0.01) * SR)
mus[a:b] *= np.linspace(1, 0, b - a)   # no cliffhanger: the bed fades out over the end card
mus[b:] = 0

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -33)
sfx = level(sfx, -27) + SAMP
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.8 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
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

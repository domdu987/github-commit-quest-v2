"""ซอมบี้รถไฟฟ้า: the soundtrack from schedule.json: levelled voice, synthesized SFX (rail clacks, slams, the alarm, the bell, radio,
heartbeat speeding up, silences before the big moments) and the Suno bed with dips and ducking. Output -14 LUFS."""
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
LINE_GAIN = {"c01": 2}   # ขิม shouts over the water: lift her line over the bed and effects
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



def rails(k, a, b, g=0.14, period=0.62):  # wheel clacks over the rail joints (clack-clack), the tempo of the ride
    out, t = [], a
    while t < b:
        out += [(k, t, "knock", g), (k, t + 0.11, "knock", g * 0.8)]
        t += period
    return out


def accel(k, a, b, p0=0.62, p1=0.34, g=0.32):  # a heartbeat that speeds up toward the crisis
    out, t = [], a
    while t < b:
        out.append((k, t, "heartbeat", g)); f = (t - a) / max(0.01, b - a); t += p0 + (p1 - p0) * f
    return out


CUES = [
    # hook: palms slam the glass (slams, the crack), alarm, the car rattling
    ("hook", 0.0, "slam", 0.42), ("hook", 0.36, "slam", 0.4), ("hook", 0.38, "shatter", 0.3), ("hook", 0.0, "growl", 0.3), ("hook", 0.8, "alarm", 0.2), ("hook", 0.82, "rattle", 0.3), *rails("hook", 0.8, D["hook"], 0.16, 0.4),
    ("cmd", 0.0, "rattle", 0.24), ("cmd", 0.15, "ratchet", 0.3), ("cmd", F("cmd", 0, 0), "sting", 0.42),
    # ten minutes before: the train passes on the viaduct (roar + clacks), the calm car
    ("before", 0.0, "whoosh", 0.3), ("before", 0.0, "engine", 0.22), *rails("before", 0.0, D["before"], 0.16, 0.62), ("before", 1.5, "hum", 0.1),
    ("live", 0.0, "hum", 0.1), *rails("live", 0.0, D["live"], 0.12, 0.62), ("live", 0.2, "notif", 0.14),
    ("rhyme", 0.0, "hum", 0.1), *rails("rhyme", 0.0, D["rhyme"], 0.12, 0.62),
    ("lcd", 0.0, "ding", 0.2), *rails("lcd", 0.0, D["lcd"], 0.1, 0.62),
    # the screams from the end car
    ("scream", 0.0, "scream", 0.2), ("scream", 0.1, "alarm", 0.12), ("scream", D["scream"] - 0.6, "growl", 0.24), ("scream", 0.5, "steps", 0.18), *rails("scream", 0.0, D["scream"], 0.14, 0.5),
    ("shut", 0.4, "slam", 0.6), ("shut", 0.45, "latch", 0.3), *rails("shut", 0.0, D["shut"], 0.14, 0.5),
    ("glass", 0.0, "slam", 0.4), ("glass", 0.5, "slam", 0.4), ("glass", 1.0, "slam", 0.4), ("glass", F("glass", 0, 1) + 0.1, "shatter", 0.36), ("glass", 0.2, "growl", 0.3), *accel("glass", 0.2, D["glass"], 0.62, 0.5),
    ("suit", 0.2, "ratchet", 0.34), ("suit", 0.6, "rattle", 0.3), *accel("suit", 0.0, D["suit"], 0.5, 0.46),
    ("lever", 0.0, "rattle", 0.2), *accel("lever", 0.0, D["lever"], 0.5, 0.46, 0.28), ("lever", F("lever", 0, 2), "ding", 0.2),
    ("drop", 0.0, "whoosh", 0.3), ("drop", 0.0, "engine", 0.18), ("drop", 0.45, "pop", 0.0), ("drop", 0.6, "zap", 0.0), *rails("drop", 0.0, D["drop"], 0.14, 0.4),
    ("rule", 0.0, "thud", 0.3), *accel("rule", 0.0, D["rule"], 0.46, 0.44),
    # the bell, control answers (a radio squelch)
    ("bell", 0.75, "click", 0.3), ("bell", 0.8, "ring", 0.24), *accel("bell", 0.0, D["bell"], 0.46, 0.44, 0.26),
    ("occ", 0.0, "radiosq", 0.3), ("occ", D["occ"] - 0.3, "radiosq", 0.24), *rails("occ", 0.0, D["occ"], 0.12, 0.45),
    # the hinge bends; backs to the door; the heartbeat races
    ("bend", 0.0, "creak", 0.5), ("bend", F("bend", 0, 1), "clang", 0.4), ("bend", 0.2, "growl", 0.34), *accel("bend", 0.0, D["bend"], 0.42, 0.36, 0.34),
    ("push", 0.0, "slam", 0.4), ("push", 0.6, "slam", 0.4), ("push", 1.2, "slam", 0.4), ("push", 0.3, "growl", 0.3), *accel("push", 0.0, D["push"] - 0.45, 0.36, 0.3, 0.38),
    # silence 0.45 s, then the train slows (screech) into the dark station
    ("arrive", 0.0, "screech", 0.3), ("arrive", 0.6, "powerdown", 0.26),
    ("out", 0.2, "hiss", 0.0), ("out", 0.25, "latch", 0.34), ("out", 0.35, "steps", 0.4), ("out", 0.9, "steps", 0.3), ("out", 0.2, "pant", 0.26),
    ("quiet", 0.3, "drip", 0.14),
    ("sign", 0.05, "creak", 0.12),
    ("turn", F("turn", 0, 1), "sting", 0.5), ("turn", F("turn", 0, 1) + 0.05, "growl", 0.4), ("turn", F("turn", 0, 1) + 0.1, "swell", 0.3),
    ("next", 0.1, "whoosh", 0.3), ("next", 0.8, "ding", 0.24),
]
import sys; sys.path.insert(0, "/home/user/github-commit-quest-v2/video/lib-shared/sfx"); import iconfx_mix
_ic, SAMP = iconfx_mix.split(json.load(open(os.path.join(HERE, "iconfx_cues.json"))) if os.path.exists(os.path.join(HERE, "iconfx_cues.json")) else [], N, SR)
CUES += [(None, c["t"], c["type"], c["gain"]) for c in _ic]   # IconFX hits (icons, the clipboard), frame-exact
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
mus = load(os.path.join(HERE, "..", "music", "skytrain-theme.mp3"))   # theme score (owner 1 Nov: "ซาวเพลงทำให้เข้าธีมด้วย")
mus = mus[int(max(0.0, len(mus) / SR - TOTAL - 1.0) * SR):]   # start so the track's peak (its last ~20 s) lands on the cliffhanger
while len(mus) < N:
    mus = np.concatenate([mus, mus])
mus = mus[:N]
t = np.arange(N) / SR
gain = np.ones(N, np.float32)


def dip(t0, t1, lvl, ramp=0.25):
    a = np.clip((t - (t0 - ramp)) / ramp, 0, 1) * np.clip(((t1 + ramp) - t) / ramp, 0, 1)
    np.minimum(gain, 1 - (1 - lvl) * a, out=gain)


dip(T("push", -0.45), T("arrive", 0.05), 0.0, ramp=0.08)                 # 0.45 s of silence before the station
dip(T("turn", F("turn", 0, 1) - 0.4), T("turn", F("turn", 0, 1) - 0.02), 0.15, ramp=0.08)
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

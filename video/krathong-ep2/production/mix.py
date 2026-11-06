"""เรือล่มคืนลอยกระทง EP.2 (Shorts): the soundtrack from schedule.json and soundplan.json (CINEMA BIBLE): levelled voice, synthesized SFX in four
layers (place, action, music, a 48 Hz drone from the recap to the roll), one sting at the roll, silences before the two commands and
the sting, heartbeat 90→130 bpm. No noise beds. Output -14 LUFS."""
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


PLAN = json.load(open(os.path.join(HERE, "soundplan.json")))
STING = PLAN["sting"]


def bedabs(kind, a, b, g, step):  # overlapping copies of a bed between absolute times a and b (None as the shot key)
    return [(None, a + i * step, kind, g) for i in range(max(1, int((b - a) / step)))]


def hbeat(a, b, bpm, g):  # heartbeat at bpm between absolute times a and b
    p = 60 / bpm
    return [(None, a + i * p, "heartbeat", g) for i in range(int((b - a) / p))]


CUES = [
    # open mid-capsize: the hull groans, water pours over the low gunwale, people shout (no sting: the one sting is the roll)
    ("open", 0.0, "creak", 0.34), ("open", 0.1, "splash", 0.18), ("open", 1.6, "creak", 0.24),
    ("hook", 1.2, "creak", 0.3),
    # recap: the counter clicks on 0019, the sign
    ("recap", 0.6, "click", 0.36), ("recap", 1.0, "click", 0.36), ("recap", 2.4, "engine", 0.16),
    # the climb: feet on the boards, the boat whips back
    ("climb", 0.1, "creak", 0.36), ("climb", 0.5, "knock", 0.3), ("climb", 2.55, "thud", 0.42), ("climb", 2.6, "splash", 0.16),
    # the rule: the paddle bell, the brush stroke
    ("rule", 2.4, "ding", 0.3), ("rule", 2.7, "marker", 0.22), ("rule", 4.5, "creak", 0.2),
    # the roll: sting once, the roof comes down
    (None, STING, "sting", 0.42), (None, STING + 0.05, "creak", 0.36), (None, STING + 0.25, "roar", 0.3), (None, STING + 0.5, "splash", 0.24),
    # under the hull: muffled thuds and bubbles only
    ("under", 0.3, "plop", 0.2), ("under", 1.0, "plop", 0.16), ("under", 1.8, "thud", 0.2), ("under", 3.2, "plop", 0.18),
    # the surface: gasp, the far fireworks, the gallon hits the water
    ("surf", 0.05, "splash", 0.2), ("surf", 1.5, "boom", 0.14), ("jug", 0.0, "splash", 0.26), ("jug", 0.4, "plop", 0.24),
    ("stairs", 0.4, "creak", 0.16), ("stairs", 3.0, "plop", 0.2), ("stairs", 5.6, "plop", 0.2),
    ("vest", 0.3, "plop", 0.16), ("vest", 2.5, "drip", 0.16),
    *[("choice", 0.4 + i * 1.0, "tick", 0.2) for i in range(3)],
    ("endb", 0.25, "knock", 0.22), ("endb", vo_t("endb") + 0.2, "ding", 0.18),
    *bedabs("crickets", T("stairs", 0), T("vest", 0), 0.12, 5.4),
]
# the heart: 90 → 110 → 130 bpm as the pontoon nears (PLAN bpm), hushed in the command's silence and before the sting
for (a, bpm), nxt in zip(PLAN["bpm"], PLAN["bpm"][1:] + [[STING, 0]]):
    CUES += hbeat(a, nxt[0], bpm, 0.36)
# the drone (48 Hz hum, barely heard) from the first uneasy cut, growing to the sting
DR0 = PLAN["drone_start"]
CUES += [(None, DR0 + i * 3.0, "hum", 0.08 + 0.22 * (i * 3.0) / (STING - DR0)) for i in range(int((STING - 1.0 - DR0) / 3.0))]
# the silences: nothing but the voice from 1 s before each command and 0.8 s before the sting
CUT = [(a - 0.25, b) for a, b in PLAN["silences"]]
CUES = [c for c in CUES if not any(a <= (c[1] if c[0] is None else T(c[0], c[1])) < b for a, b in CUT)]
# no hiss: the noise-based wind bed reads as static under the voice (user: "ลบเสียงซ่าออก")
CUES = [c for c in CUES if c[2] not in ("wind", "lap") and c[3] > 0]
cues = {"duration": TOTAL, "sections": [{"start": 0, "end": TOTAL, "mood": "silence"}],
        "sfx": [{"t": round(t if k is None else T(k, t), 3), "type": typ, "gain": g} for k, t, typ, g in CUES]}
json.dump(cues, open(os.path.join(HERE, "sfx_cues.json"), "w"))
subprocess.run(["python3", os.path.join(HERE, "..", "synth.py"), os.path.join(HERE, "sfx_cues.json"), os.path.join(HERE, "sfx.wav")],
               check=True, env={**os.environ, "STEMS": "1"})
sfx = load(os.path.join(HERE, "sfx_sfx.wav"))[:N]
sfx = np.pad(sfx, (0, N - len(sfx)))

# ---- music with horror dips ----
# the track's bright, noise-like top (cymbal wash, 5-14 kHz) reads as hiss in the voice pauses of this short episode
# (hisscheck flatness 0.46 with every effect removed): low-passed at 4.5 kHz (two 2nd-order passes)
LP = os.path.join(HERE, "music_lp.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(HERE, "..", "music", "suno1.mp3"), "-af", "lowpass=f=4500,lowpass=f=4500", LP], check=True)
mus = load(LP)
# loop the body of the track (3 s … 125 s) with a 1 s crossfade: the file fades out at its end (~128 s), which used to land on the capsize
body, xf = mus[int(3 * SR):int(125 * SR)], int(1.0 * SR)
mus = mus[:int(125 * SR)].copy()
while len(mus) < N:
    r = np.linspace(0, 1, xf, dtype=np.float32)
    mus[-xf:] = mus[-xf:] * (1 - r) + body[:xf] * r
    mus = np.concatenate([mus, body[xf:]])
mus = mus[:N]
t = np.arange(N) / SR
gain = np.ones(N, np.float32)


def dip(t0, t1, lvl, ramp=0.25):
    a = np.clip((t - (t0 - ramp)) / ramp, 0, 1) * np.clip(((t1 + ramp) - t) / ramp, 0, 1)
    np.minimum(gain, 1 - (1 - lvl) * a, out=gain)


for a, b in PLAN["silences"]:
    dip(a, b, 0.0, ramp=0.2)          # music out under the commands and before the sting (only breath and voice remain)
dip(T("under", 0), T("surf", 0), 0.35)  # under the hull: the music sinks with her
dip(T("vest", 0), T("choice", 0), 0.7)
mus = mus * gain
# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -31.6)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
# the silences of the plan: every layer but the voice goes to zero (50 ms ramps), so effect tails cannot ring into them
hush = np.ones(N, np.float32)
for a, b in PLAN["silences"]:
    np.minimum(hush, np.clip(np.maximum((a - t) / 0.05, (t - b) / 0.05), 0, 1).astype(np.float32), out=hush)
mus, sfx = mus * hush, sfx * hush
import sys
sys.path.insert(0, HERE)
# the screamed lines peak far above the rest: finalize's soft clip would distort them (hisscheck read the distortion as hiss,
# flatness 0.46). Instead the voice goes through a clean look-ahead limiter first, at the level the -14 LUFS gain will need,
# so the mix reaches its true-peak target without clipping (the voice stem is this limited voice: what is summed)
from finalmix import _lufs
_I, _ = _lufs(vo + mus * duck + sfx)
_g = 10 ** ((-14.0 - _I) / 20)
_lim = 10 ** (-3.4 / 20) / _g
_raw = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af",
                       f"alimiter=limit={min(1.0, _lim):.5f}:attack=4:release=60:level=disabled:asc=0", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                      input=vo.astype(np.float32).tobytes(), capture_output=True, check=True).stdout
vo = np.frombuffer(_raw, np.float32)[:N].copy()
vo = np.pad(vo, (0, N - len(vo)))
mix = vo + mus * duck + sfx
# a short hard silence between the choice and the end card
cut, card = int(T("choice", -0.12) * SR), int(T("endb", 0.05) * SR)
mix[cut - 240:cut] *= np.linspace(1, 0, 240)
mix[cut:card] = 0
# one linear gain to -14 LUFS for the mix and both stems (finalmix.finalize: no loudnorm, so the stems are exactly what is summed)
from finalmix import finalize
mus_part = mus * duck
mus_part[cut:card] = 0
finalize(HERE, mix, vo, mus_part, tp=-1.1)
print("mix written", TOTAL)

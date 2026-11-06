"""เรือล่มคืนลอยกระทง EP.1 (Shorts): the soundtrack from schedule.json and soundplan.json (CINEMA BIBLE): levelled voice, synthesized SFX in four
layers (place, action, music, a 48 Hz drone from the red stripe to the capsize), one sting at the capsize, silences before the two commands and
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


GA = T("grab", 0) + 1.47          # cut 24 (the choice) · the command "อย่า" sits at PLAN silences[1][1]
CMD_T = PLAN["silences"][1][1] - 0.05
CUES = [
    # hook: the boat rocking at the pontoon, fireworks, no sting (CINEMA BIBLE: the one sting is the capsize)
    ("open", 0.0, "creak", 0.22), ("open", 0.9, "boom", 0.3), ("open", 1.2, "splash", 0.12), ("hook", 1.05, "creak", 0.26),
    # card: the counter's reset knob ("แกร๊ก") and the wheels rolling back
    ("card", 0.2, "rewind", 0.2), ("card", 0.55, "click", 0.4), ("card", 0.83, "click", 0.4),
    # the pier: crickets, the far fair (booms), the whistle (the clue)
    *bedabs("crickets", T("kids", 0), T("line", 0), 0.16, 5.4),
    ("kids", 1.5, "boom", 0.12), ("kids", 6.5, "boom", 0.1), ("kids", 3.88, "knock", 0.22),
    ("whistle", 0.1, "whistle", 0.45), ("whistle", 0.6, "whistle", 0.3),
    ("code", 4.8, "ching", 0.14), ("vest", 2.0, "click", 0.3), ("vest", 2.3, "click", 0.3), ("vest", 2.6, "click", 0.3),
    ("rap", 2.91, "ding", 0.3), ("rap", 2.98, "knock", 0.2), ("rap", 5.84, "knock", 0.3), ("rap", 6.0, "ding", 0.24), ("rap", 6.2, "marker", 0.22),
    # uneasy from the red stripe: the drone starts low and grows to the capsize
    ("line", 0.4, "plop", 0.12), ("line", 3.0, "plop", 0.12), ("line", 6.0, "plop", 0.14),
    ("coin", 0.5, "marker", 0.26), ("coin", 1.0, "marker", 0.2), ("coin", vo_t("coin", 1) + 0.3, "creak", 0.24),
    ("board", 0.4, "click", 0.4), ("board", 1.4, "click", 0.4),
    *[("load", 0.5 + c * 0.95, "click", 0.42) for c in range(7)], ("load", 0.3, "creak", 0.16),
    ("sign", 4.8, "engine", 0.2), ("sign", 7.8, "engine", 0.2),
    # mid-river: fireworks, the crowd at one side, water slopping in
    ("fire", 0.05, "boom", 0.42), ("fire", 2.6, "boom", 0.36), ("fire", 5.4, "boom", 0.38), ("fire", 1.0, "splash", 0.18), ("fire", 1.6, "creak", 0.28),
    ("sit", 0.1, "whistle", 0.45), ("sit", 0.55, "whistle", 0.45), ("sit", 1.3, "creak", 0.2),
    ("float", 0.6, "plop", 0.24),
    # sound before picture: the party raft's bass from 1.5 s before we see it
    *[(None, T("back", 0) - 1.5 + i * 0.5, "drum", 0.14 + 0.012 * i) for i in range(int((D["back"] + 1.5) / 0.5))],
    ("back", 1.0, "swell", 0.24),
    # the crash: the wake slaps, people jump up, the bump, three blasts behind ลุง
    ("hit", 0.2, "splash", 0.36), ("hit", 0.45, "creak", 0.3), ("hit", 3.2, "thud", 0.5), ("hit", 3.25, "knock", 0.3),
    ("hit", D["hit"] - 1.2, "whistle", 0.5), ("hit", D["hit"] - 0.8, "whistle", 0.5), ("hit", D["hit"] - 0.4, "whistle", 0.5),
    # the capsize: the sting (once), the wood cracks, the river comes in
    (None, STING, "sting", 0.42), (None, STING + 0.05, "creak", 0.36), (None, STING + 0.25, "roar", 0.42), (None, STING + 0.5, "splash", 0.4),
    ("evid", 0.4, "drip", 0.2), ("evid", 2.0, "drip", 0.16),
    *[("choice", 0.4 + i * 1.0, "tick", 0.2) for i in range(3)],
    ("endb", 0.25, "knock", 0.22), ("endb", vo_t("endb") + 0.2, "ding", 0.18),
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
dip(T("line", 0), T("fire", 0), 0.85)  # uneasy: the bed thins out a little
dip(T("evid", 0), T("choice", 0), 0.7)
mus = mus * gain
# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -29.2)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
# the silences of the plan: every layer but the voice goes to zero (50 ms ramps), so effect tails cannot ring into them
hush = np.ones(N, np.float32)
for a, b in PLAN["silences"]:
    np.minimum(hush, np.clip(np.maximum((a - t) / 0.05, (t - b) / 0.05), 0, 1).astype(np.float32), out=hush)
mus, sfx = mus * hush, sfx * hush
mix = vo + mus * duck + sfx
# a short hard silence between the choice and the end card
cut, card = int(T("choice", -0.12) * SR), int(T("endb", 0.05) * SR)
mix[cut - 240:cut] *= np.linspace(1, 0, 240)
mix[cut:card] = 0
# one linear gain to -14 LUFS for the mix and both stems (finalmix.finalize: no loudnorm, so the stems are exactly what is summed)
import sys
sys.path.insert(0, HERE)
from finalmix import finalize
mus_part = mus * duck
mus_part[cut:card] = 0
finalize(HERE, mix, vo, mus_part, tp=-1.5)
print("mix written", TOTAL)

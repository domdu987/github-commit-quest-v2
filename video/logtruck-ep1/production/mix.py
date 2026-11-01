"""ท่อนซุงลงเขา EP.1 (from the นาทีก่อนจม mixer): the soundtrack from schedule.json: levelled voice, synthesized SFX (crickets, engine, the lock click, the countdown
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
LINE_GAIN = {"j01": 1, "j02": 1}
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
    ("hook", 0.0, "swell", 0.2), ("cmd", vo_t("cmd") - 0.02, "sting", 0.3), ("law", 0.1, "whoosh", 0.16),
    ("squeeze", 0.0, "swell", 0.18), ("pop", 0.3, "boom", 0.3), ("next", 0.1, "whoosh", 0.3), ("next", 0.6, "ding", 0.24),
]

exec(open(os.path.join(HERE, "..", "samples_inc.py")).read())
SAMPLES = [
    ("hook", 0.0, "chainsnap", 1.0), ("hook", 0.95, "ltscreech", 0.8), ("hook", 1.2, "logthud", 1.0), ("hook", 1.7, "logroll", 0.7),
    ("cmd", 0.0, "airbrake", 0.45), ("rest", 0.0, "logroll", 0.35, 2.0),
    ("horn", 0.0, "airhorn", 1.0), ("horn", 1.0, "airhorn", 0.75),
    ("squeeze", 0.3, "airhorn", 0.7), ("squeeze", 1.2, "chainrattle", 0.5),
    ("five", 0.2, "airbrake", 0.7), ("five", 1.9, "chainrattle", 0.75),
    ("wave", 0.3, "truckahead", 0.5), ("gear", 0.0, "airbrake", 0.8), ("gear", F("gear", 0, 1) - 0.2, "gearshift", 0.8),
    ("last", 0.4, "chainrattle", 0.8), ("last", 2.4, "airbrake", 0.6),
    ("pop", 0.0, "binder", 1.0), ("pop", 0.1, "chainsnap", 0.55), ("pop", 0.3, "logslide", 1.0), ("pop", 1.3, "airhorn", 0.8),
]
_t = 0.0
while _t < SH["next"]["start"] - 1.0:      # the cabin hum and the truck ahead under everything until the end card
    SAMPLES.append((None, _t, "cabin", 0.38, 7.6)); _t += 7.0
_t = 0.0
while _t < SH["next"]["start"] - 1.0:
    SAMPLES.append((None, _t, "truckahead", 0.3, 5.8)); _t += 5.4
# ---- the in-world cards (1 Nov): steel sounds in step with Lt.board / Lt.plateIn / Lt.numPost (times mirror body.part) ----
def board_sfx(tb, active_row, done_rows, dur):   # tb = the board's drop start (absolute); rows indexed on the board
    out = [(None, tb + 0.05, "boarddrop", 0.9), (None, tb + 1.4, "chainclink", 0.35)]
    if dur > 3.6: out.append((None, tb + 3.2, "chainclink", 0.3))
    if active_row >= 0: ta = tb + 0.75 + active_row * 0.12; out.append((None, ta, "spray", 0.55))
    out += [(None, tb + 0.9 + k * 0.12, "spraytick", 0.4) for k in done_rows]
    return out
def plate_sfx(t): return [(None, t, "signboing", 0.65)]
_at = max(0.2, F("wave", 0, 2) - 2.4)
SAMPLES += plate_sfx(T("law", F("law", 0, 1) - 0.1))
SAMPLES += [(None, T("count", F("count", 0, j) + 0.1), "stake", 0.7) for j in (0, 1)]
SAMPLES += board_sfx(T("twosec", 0.05), 0, [], D["twosec"])
SAMPLES += board_sfx(T("wave", 2.4 + _at + 1.0), 1, [0], D["wave"] - 2.4 - _at - 1.0)
SAMPLES += board_sfx(T("gear", 0.1), 2, [0, 1], D["gear"])

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
    place(sfx, smp(name, mx[0] if mx else None), t0 if k is None else T(k, t0), g)

# ---- music with horror dips ----
mus = load(os.path.join(HERE, "..", "music", "logtruck-theme.mp3"))[int(6.0 * SR):]   # ท่อนซุงลงเขา theme (owner 1 Nov: no suno1); offset puts the peak on the cliffhanger
while len(mus) < N:
    mus = np.concatenate([mus, mus])
mus = mus[:N]
t = np.arange(N) / SR
gain = np.ones(N, np.float32)


def dip(t0, t1, lvl, ramp=0.25):
    a = np.clip((t - (t0 - ramp)) / ramp, 0, 1) * np.clip(((t1 + ramp) - t) / ramp, 0, 1)
    np.minimum(gain, 1 - (1 - lvl) * a, out=gain)

def boost(t0, t1, lvl, ramp=0.25):   # lift the bed under the action (the logs coming loose)
    global gain
    a = np.clip((t - (t0 - ramp)) / ramp, 0, 1) * np.clip(((t1 + ramp) - t) / ramp, 0, 1)
    gain = gain * (1 + (lvl - 1) * a)





boost(T("hook", 0), T("cmd", 0.3), 1.7)       # the snap and the log: the bed drives it
dip(T("horn", 0) - 0.25, T("horn", 0.5), 0.3)   # a breath before the air horn
boost(T("squeeze", 0), T("squeeze", -0.01), 1.3)
dip(T("pop", 0) - 0.3, T("pop", 0.35), 0.2)     # silence before the binder springs
boost(T("pop", 0.35), T("pop", -0.01), 1.8)     # the peak on the cliffhanger
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

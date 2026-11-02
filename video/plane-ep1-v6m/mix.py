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
LINE_GAIN = {"q02": 1}   # ขิม shouts over the water: lift her line over the bed and effects
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


def C(k, i=0, j=0):  # the cut before card j of line i (same as body.part)
    return max(0.0, F(k, i, j) - 0.1)


def fire(k, a, b, g=0.24, step=2.2):  # the fire's crackle and roar, overlapping copies inside shot k
    return [(k, a + i * step, "crackle", g) for i in range(int(max(0, b - a - 0.4) / step) + 1)]


# diegetic sound only (S17 trial): no stings or whooshes on the cards; the cabin itself makes the hits
CUES = [
    # B0 the face in the dark: alarm + rumble; cut to the engine: the burst
    ("hook", 0.0, "alarm", 0.2), ("hook", 0.0, "rattle", 0.26), ("hook", 0.0, "roar", 0.2),
    ("hook", C("hook", 0, 1), "boom", 0.6), ("hook", C("hook", 0, 1) + 0.02, "roar", 0.42), ("hook", C("hook", 0, 1) + 0.1, "debris", 0.24),
    ("cmd", 0.0, "rattle", 0.24), ("cmd", 0.05, "clang", 0.22), *fire("cmd", 0.1, D["cmd"]),
    ("why", 0.0, "alarm", 0.16), *fire("why", 0.0, D["why"], 0.2), ("why", C("why", 0, 1), "scream", 0.07), ("why", C("why", 0, 1) + 0.5, "scream", 0.05),
    ("why", C("why", 0, 2), "roar", 0.42), ("why", C("why", 0, 3), "tinnitus", 0.14), ("why", C("why", 0, 3) + 0.2, "hiss", 0.0),
    # B1 the bag: rustle, the strap snag, the yank, the fire spreading
    *fire("grab", 0.0, D["grab"], 0.22), ("grab", C("grab", 0, 1), "rustle", 0.3),
    *fire("q", 0.0, D["q"], 0.2), ("q", 0.3, "rattle", 0.18),
    ("snag", 0.02, "clang", 0.3), *fire("snag", 0.2, D["snag"], 0.18), ("snag", C("snag", 0, 1), "rustle", 0.28), ("snag", C("snag", 0, 2), "creak", 0.3), ("snag", C("snag", 0, 2) + 0.15, "chain", 0.16),
    *[("pull", 0.1 + i * 0.36, "creak", 0.22) for i in range(4)], ("pull", C("pull", 0, 1), "roar", 0.5), *fire("pull", C("pull", 0, 1), D["pull"], 0.32),
    # B2 the card from the seat pocket (IconFX seat_card sounds), the crowd, the bags hitting the floor
    *fire("ninety", 0.0, D["ninety"], 0.16), ("ninety", 0.2, "rustle", 0.26),
    *fire("half", 0.0, D["half"], 0.16), ("half", 0.2, "scream", 0.05), ("half", C("half", 0, 1), "steps", 0.22), ("half", C("half", 0, 2) + 0.1, "latch", 0.24), ("half", C("half", 0, 2) + 0.3, "latch", 0.2), ("half", C("half", 0, 3), "rustle", 0.28),
    ("block", 0.15, "thud", 0.32), ("block", 0.5, "thud", 0.26), ("block", 0.85, "thud", 0.28), ("block", C("block", 0, 1), "steps", 0.3), ("block", C("block", 0, 1) + 0.1, "scream", 0.07), *fire("block", 0.0, D["block"], 0.18),
    # B3 he drops it and runs forward into the smoke, the fire bursts ahead
    ("run", 0.3, "thud", 0.34), ("run", C("run", 0, 1), "steps", 0.34), ("run", C("run", 0, 1) + 0.7, "steps", 0.34), ("run", C("run", 0, 2), "steps", 0.3), ("run", C("run", 0, 2) + 0.7, "steps", 0.3), *fire("run", 0.0, D["run"], 0.2),
    ("blind", 0.1, "pant", 0.24), *fire("blind", 0.0, D["blind"], 0.16), ("blind", C("blind", 0, 1), "tinnitus", 0.12),
    ("front", 0.0, "pant", 0.18), ("front", C("front", 0, 1), "boom", 0.55), ("front", C("front", 0, 1) + 0.02, "roar", 0.5), ("front", C("front", 0, 1) + 0.05, "debris", 0.26),
    # B4 behind him: the exit; the rule (calm cabin, the card), the sign sinking
    *fire("behind", 0.0, D["behind"], 0.18), ("behind", 0.2, "pant", 0.18), *beats("behind", 0.2, D["behind"] - 0.2, 0.46, 0.24),
    ("rule", 0.0, "hum", 0.14), ("rule", 0.4, "liftding", 0.14),
    *fire("sign", 0.0, D["sign"], 0.18), ("sign", C("sign", 0, 1), "hiss", 0.0), ("sign", C("sign", 0, 1) + 0.2, "tinnitus", 0.12),
    # B5 counting the seatbacks by touch, the door, the slide, the fire at his back
    *[("count", 0.2 + i * 0.6, "knock", 0.22) for i in range(4)], ("count", C("count", 0, 1), "knock", 0.36), *fire("count", 0.0, D["count"], 0.14), *beats("count", 0.1, D["count"] - 0.1, 0.4, 0.28),
    ("out", 0.25, "latch", 0.4), ("out", 0.4, "whoosh", 0.3), ("out", 0.45, "stream", 0.14), ("out", C("out", 0, 1) + 0.6, "scrape", 0.32), ("out", C("out", 0, 1) + 0.7, "whoosh", 0.26),
    ("out", C("out", 0, 2) + 0.1, "boom", 0.5), ("out", C("out", 0, 2) + 0.12, "roar", 0.42), *fire("out", C("out", 0, 2), D["out"], 0.24),
    ("safe", 0.0, "pant", 0.26), ("safe", 0.0, "stream", 0.14), *fire("safe", 0.0, D["safe"], 0.14),
    # hush: nothing at all (0.45 s) — then the surf, the gulls, the far smoke
    ("twist", 0.0, "stream", 0.14), ("twist", 1.6, "flap", 0.14), *fire("twist", 0.3, D["twist"], 0.1),
    ("alone", 0.0, "stream", 0.14), ("alone", 1.4, "flap", 0.12),
    ("smoke2", 0.0, "stream", 0.12), ("smoke2", C("smoke2", 0, 1), "swell", 0.2),
    ("next", 0.1, "stream", 0.1),
]
import sys; sys.path.insert(0, "/home/user/github-commit-quest-v2/video/lib-shared/sfx"); import iconfx_mix
_ic, SAMP = iconfx_mix.split(json.load(open(os.path.join(HERE, "iconfx_cues.json"))) if os.path.exists(os.path.join(HERE, "iconfx_cues.json")) else [], N, SR)
CUES += [(None, c["t"], c["type"], c["gain"]) for c in _ic]
SAMPLES = []
REPLACED = set()
CUES = [c for c in CUES if c[2] not in REPLACED]

# no hiss: the noise-based wind bed reads as static under the voice (user: "ลบเสียงซ่าออก")
CUES = [c for c in CUES if c[2] not in ("wind", "lap", "pop", "tick") and c[3] > 0]
# no hiss (owner, again: "ลบเสียงซ่าออกด้วย", SKILL A4): drop every continuous noise bed and long noise burst — the fire loop (crackle),
# roar, surf (stream), hiss, breathing (pant), debris, whooshes, hum and the tinnitus whine. Fire is heard only as short hits (boom, clang).
NOISY = {"crackle", "roar", "stream", "hiss", "pant", "debris", "whoosh", "hum", "tinnitus", "wind", "rain", "static", "swell"}
CUES = [c for c in CUES if c[2] not in NOISY]   # no HUD: no chip pops, no countdown ticks (user 31 ต.ค.)  # no noise beds (user: "เสียงซ่าๆเอาออก")
cues = {"duration": TOTAL, "sections": [{"start": 0, "end": TOTAL, "mood": "silence"}],
        "sfx": [{"t": round(t if k is None else T(k, t), 3), "type": typ, "gain": g} for k, t, typ, g in CUES]}
json.dump(cues, open(os.path.join(HERE, "sfx_cues.json"), "w"))
subprocess.run(["python3", os.path.join(HERE, "..", "synth.py"), os.path.join(HERE, "sfx_cues.json"), os.path.join(HERE, "sfx.wav")],
               check=True, env={**os.environ, "STEMS": "1"})
sfx = load(os.path.join(HERE, "sfx_sfx.wav"))[:N]
sfx = np.pad(sfx, (0, N - len(sfx)))


# ---- music with horror dips ----
mus = load(os.path.join(HERE, "..", "music", "plane-theme.mp3"))   # theme score (owner 1 Nov: "ซาวเพลงทำให้เข้าธีมด้วย")
mus = mus[int(max(0.0, len(mus) / SR - TOTAL - 10.0) * SR):]   # A5: the track fades out over its last ~9 s, keep that past the end card · start so the track's peak (its last ~20 s) lands on the cliffhanger
while len(mus) < N:
    mus = np.concatenate([mus, mus])
mus = mus[:N]
t = np.arange(N) / SR
gain = np.ones(N, np.float32)


def dip(t0, t1, lvl, ramp=0.25):
    a = np.clip((t - (t0 - ramp)) / ramp, 0, 1) * np.clip(((t1 + ramp) - t) / ramp, 0, 1)
    np.minimum(gain, 1 - (1 - lvl) * a, out=gain)


dip(T("hush", 0), T("hush", -0.01), 0.0, ramp=0.06)   # the twist pulls out: 0.45 s of silence
dip(T("smoke2", C("smoke2", 0, 1) - 0.2), T("next", 0), 0.55)
mus = mus * gain
# cut the bass under the twist (from the hush to the end card): a 1-pole high-pass at ~400 Hz, crossfaded in
mus_full = mus.copy()
a0 = int(T("hush", 0) * SR)
seg_ = mus[a0:].astype(np.float64); Fq = np.fft.rfft(seg_); fq = np.fft.rfftfreq(len(seg_), 1 / SR)
Fq *= np.clip((fq - 150) / 250, 0, 1)   # nothing under 150 Hz, full from 400 Hz
mus[a0:] = np.fft.irfft(Fq, len(seg_)).astype(np.float32)
a, b = int(T("next", 0) * SR), int(T("next", -0.01) * SR)
_w = np.clip((t - T("next", 0)) / 0.3, 0, 1).astype(np.float32); mus = mus * (1 - _w) + mus_full * _w   # A5: the full score (bass back) under the end card
mus[a:b] *= np.linspace(0.38, 0.3, b - a)   # A5: the score stays audible over the end card (eases down, never gone)
mus[b:] = 0

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
MUS_DB = float(os.environ.get("MUS_DB", "-18.8"))   # A5 (owner 2 Nov "เพลงเบาไม่ได้ยิน"): the score up where you hear it
mus = level(mus, MUS_DB)
_X = np.fft.rfft(mus.astype(np.float64)); _f = np.fft.rfftfreq(len(mus), 1 / SR)
_X *= np.clip((6600 - _f) / 1200, 0, 1); mus = np.fft.irfft(_X, len(mus)).astype(np.float32)   # the score's top shimmer read as hiss once its bass is cut: soft low-pass at 6 kHz
sfx = level(sfx, -27) + SAMP
def lowpass(x, fc, w=600.0):   # zero-phase FFT low-pass with a soft knee: no sharp tails on the effects bus
    X = np.fft.rfft(x.astype(np.float64)); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= np.clip((fc + w - f) / (2 * w), 0, 1); return np.fft.irfft(X, len(x)).astype(np.float32)
sfx = lowpass(sfx, 4500)
import sys; sys.path.insert(0, os.path.join(HERE, ".."))
from finalmix import duck_curve, finalize
duck = duck_curve(vo, amount=float(os.environ.get("DUCK", "0.5")))   # ~6 dB under the voice, 80 ms in / 400 ms out, no gate
mus_d = mus * duck
h0, h1 = T("hush", 0), T("hush", -0.01)   # the hush is silent for everything (voice, effects, music tails)
hush = (1 - np.clip((t - (h0 - 0.12)) / 0.12, 0, 1) * np.clip(((h1 + 0.02) - t) / 0.02, 0, 1)).astype(np.float32)
vo_h, mus_h, sfx_h = vo * hush, mus_d * hush, sfx * hush
finalize(HERE, vo_h + mus_h + sfx_h, vo_h, mus_h)
print("mix written", TOTAL)

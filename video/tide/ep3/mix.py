"""ทะเลลด EP.3 (ตอนจบ): build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX (the tower's siren,
the hazards ticking and the horns on the jammed beach road, the bump, ยาย's feet on the stair, the boards landing and the rows painted
on, the calm after, the phone zooming on the roof and the sparkle when ยาย waves, the kids running, the paper of the clipping, the
memory of the wave, the carved name, the shadow screen's gong, the Wednesday test tone, the duck ring) and the Suno music bed with dips
and sidechain ducking under the voice; no cliffhanger: the music fades out over the end card.
Output -14 LUFS. No noise beds and no high hiss (user: "เสียงซ่าๆเอาออก")."""
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
LINE_GAIN = {"y02": 3}  # ยาย says her own rule softly while climbing: lift it over the bed
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
    # the hook: a sound on frame 0, the tower's siren, people running for the cars, an engine
    ("hook", 0.0, "swell", 0.3), ("hook", 0.05, "siren", 0.16), *[("hook", 0.3 + i * 0.28, "steps", 0.08) for i in range(7)], ("hook", 1.4, "engine", 0.12),
    # the jam: the hazards ticking, a horn
    *[("cars", 0.05 + i * 0.42, "blinker", 0.16) for i in range(4)], ("cars", 0.15, "beep", 0.22), ("cars", 0.5, "beep", 0.18),
    # the man on the horn; the bump
    *[("jam", 0.05 + i * 0.42, "blinker", 0.12) for i in range(16)], ("jam", 0.2, "beep", 0.2), ("jam", 0.55, "beep", 0.18), ("jam", 1.2, "engine", 0.14),
    ("jam", vo_t("jam", 1) - 0.17, "thud", 0.34), ("jam", vo_t("jam", 1) - 0.15, "clang", 0.2),
    # ยาย turns to the hotel
    ("yai", 0.05, "siren", 0.1), ("yai", 0.6, "swell", 0.2),
    # up the stair; the board, rule 3 painted on
    *[("stair", 0.1 + i * 0.32, "steps", 0.06 if vo_t("stair") - 0.1 < 0.1 + i * 0.32 < vo_end("stair") else 0.12) for i in range(11)], ("stair", 0.02, "pant", 0.14),
    ("stair", 0.35, "whoosh", 0.22), ("stair", 0.7, "thud", 0.16), ("stair", vo_end("stair") + 0.05, "ding", 0.3),  # ยาย's own rule stays clear
    # the board of refuges: each row lands as it is said; the last one, the car crossed out
    ("know", 0.05, "whoosh", 0.3), ("know", 0.3, "thud", 0.2),
    *[x for t in (F("know", 0, 1) - 0.1, vo_t("know", 1), vo_t("know", 2), vo_t("know", 3)) for x in (("know", t, "pop", 0.24), ("know", t + 0.15, "marker", 0.2))],
    ("know", F("know", 3, 1), "sting", 0.24),
    # hours later: the calm, a bird, the chip
    ("hours", 0.1, "swell", 0.18), ("hours", 0.6, "ding", 0.2), ("hours", 1.4, "flap", 0.12),
    # the phone zooms on the roof: ยาย waves
    ("roof", 0.15, "whoosh", 0.16), ("roof", 1.3, "ching", 0.32), ("roof", 1.45, "pop", 0.18),
    # the kids run to her
    *[("hug", 0.05 + i * 0.25, "steps", 0.12) for i in range(4)], ("hug", 1.0, "rustle", 0.14),
    # ตาจุ่น comes
    *[("ask", 0.05 + i * 0.36, "steps", 0.08) for i in range(3)], ("ask", 0.2, "swell", 0.14),
    # the old photo; the clipping, the memory of the wave
    ("photo", 0.1, "swell", 0.24), ("photo", 0.4, "ching", 0.12), ("clip", 0.1, "rustle", 0.22), ("clip", 1.6, "roar", 0.16), *beats("clip", 2.6, D["clip"] - 2.6, 0.8, 0.24),
    # it was their mother
    ("mom", 0.15, "sting", 0.26), *beats("mom", 0.4, D["mom"] - 0.4, 0.75, 0.3),
    # ยาย and ตาจุ่น; by the calm sea
    ("why", 0.2, "swell", 0.14), ("hands", 0.2, "swell", 0.18), ("hands", 1.4, "bubbles", 0.1),
    # the board's back: the carved name
    ("board", 0.0, "whoosh", 0.26), ("board", 0.35, "thud", 0.22), ("board", vo_t("board") + 0.3, "ching", 0.24),
    # the Moken screen
    ("moken", 0.1, "gong", 0.34), ("moken", 0.6, "swell", 0.22), *[("moken", 2.8 + i * 0.5, "drum", 0.14) for i in range(5)], ("moken", 4.8, "roar", 0.26),
    # the next Wednesday, 08:00: the test tone, everybody stops
    ("wed", 0.2, "pop", 0.22), ("wed", 0.3, "siren", 0.26),
    # the duck ring
    ("duck", 0.3, "squish", 0.14), ("duck", 1.2, "pop", 0.14),
    # the last line by the sea
    ("final", 0.2, "swell", 0.2), ("final", D["final"] - 1.0, "ching", 0.2),
    # the end card
    ("end", 0.15, "whoosh", 0.32), ("end", 0.5, "flap", 0.2), ("end", 1.0, "ding", 0.26), ("end", 1.6, "flap", 0.16),
]

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
while len(mus) < N:
    mus = np.concatenate([mus, mus])
mus = mus[:N]
t = np.arange(N) / SR
gain = np.ones(N, np.float32)


def dip(t0, t1, lvl, ramp=0.25):
    a = np.clip((t - (t0 - ramp)) / ramp, 0, 1) * np.clip(((t1 + ramp) - t) / ramp, 0, 1)
    np.minimum(gain, 1 - (1 - lvl) * a, out=gain)


dip(T("photo", 0), T("hands", -0.01), 0.45)   # under ตาจุ่น's story and the reveal
mus = mus * gain
a, b = int(T("end", 0) * SR), int(T("end", -0.01) * SR)
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

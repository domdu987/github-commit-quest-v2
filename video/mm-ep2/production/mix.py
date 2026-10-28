"""ผีแม่ม่าย EP.2: build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX (the 1669 call and its
checklist, the ambulance countdown, the motorbike on the map, the compressions on the beat, the widow's arm in the flicker, the AED's
lid, power, pads, analysis, charge and shock, the siren, the ward monitor) and the Suno music bed with dips before the scares and
sidechain ducking under the voice. Output -14 LUFS, hard cut to silence after the choice. No noise beds and no high hiss
(user: "เสียงซ่าๆเอาออก")."""
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


RW = [vo_t("know1") + 1.3, frag("know1", 0, 1) + 0.25, frag("know1", 0, 1) + 1.0, frag("know1", 0, 2) + 0.15]  # the checklist ticks
SHOT_AT = vo_end("shock") + 0.15                          # the shock button is pressed
EYES = frag("silent", 0, 1)                               # the eyes in the ward window

CUES = [
    # 3 a.m. again: the shake, the heart, the eyes at the foot of the mattress; the torch at the door
    ("hook", 0.0, "glitch", 0.45), *beats("hook", 0.05, D["hook"] - 0.1, 0.45, 0.5), ("hook", 0.1, "rustle", 0.3), ("hook", 0.95, "rustle", 0.28),
    ("hook", 1.2, "swell", 0.3), ("hook", 0.0, "crickets", 0.14),
    ("hook2", 0.05, "click", 0.32), ("hook2", 0.3, "creak", 0.22),
    ("fon", F("fon", 0, 1), "stomp", 0.35),
    # the memory: the card drops in
    ("rule", 0.0, "whoosh", 0.32), ("rule", 0.0, "swell", 0.22), ("rule", 0.6, "whoosh", 0.32), ("rule", 1.15, "ding", 0.36), ("rule", 1.35, "pop", 0.24), ("rule", 1.6, "marker", 0.2),
    # the check: two crosses
    ("check", 0.1, "swell", 0.2), ("check", vo_t("check") + 0.6, "buzz", 0.18), ("check", F("check", 0, 1) + 0.1, "buzz", 0.2),
    # the call: dialling, the phone and its checklist, the countdown chip
    ("call", 0.15, "beep", 0.14), ("call", 0.4, "beep", 0.14), ("call", 0.65, "beep", 0.14),
    ("know1", 0.0, "whoosh", 0.28), ("know1", 0.05, "ring", 0.2), ("know1", 0.35, "whoosh", 0.22), *[("know1", t, "pop", 0.26) for t in RW], *[("know1", t + 0.1, "ding", 0.18) for t in RW],
    ("eta", F("eta", 0, 1) - 0.1, "notif", 0.36), ("eta", F("eta", 0, 1) + 1.3, "whoosh", 0.25),
    # next door
    ("window", 0.0, "creak", 0.3), ("window", 0.0, "crickets", 0.2), ("piak", 0.0, "crickets", 0.16), ("piak", 0.3, "rustle", 0.25),
    # the map: the motorbike to the sala and back
    ("map", 0.3, "sputter", 0.2), ("map", 0.4, "pop", 0.28), ("map", 0.45, "engine", 0.16), ("map", 1.8, "ding", 0.3), ("map", 4.1, "pop", 0.3),
    # onto the floor; the hands; the compressions
    ("floor", 1.1, "thud", 0.3), ("floor", vo_t("floor") + 0.5, "buzz", 0.2), ("floor", F("floor", 0, 1) + 0.3, "ding", 0.28),
    ("hands", 0.1, "whoosh", 0.24), ("hands", 0.3, "swell", 0.18), ("hands", vo_t("hands") + 0.15, "whoosh", 0.24), ("hands", F("hands", 0, 2) - 0.05, "knock", 0.22),
    *pushes("hands", F("hands", 0, 2) + 0.55, D["hands"] - 0.1, 0.1),
    *pushes("pump", 0.0, D["pump"] - 0.1, 0.13), *[("pump", 0.2 + i * 60 / 110, "tick", 0.12) for i in range(int((D["pump"] - 0.4) / (60 / 110)))],
    *pushes("mouth", 0.0, D["mouth"] - 0.1, 0.1),
    # the widow's arm: the bulb stutters, the eyes, the grab, the drag; Fon hauls him back
    ("tug", 0.1, "buzz", 0.24), ("tug", 0.46, "click", 0.14), ("tug", 0.6, "swell", 0.3), ("tug", 0.7, "sting", 0.45), ("tug", 0.6, "growl", 0.22), ("tug", 0.62, "rustle", 0.3),
    ("tug", 1.05, "snap", 0.4), ("tug", 1.05, "sting", 0.85), ("tug", 1.05, "glitch", 0.45), ("tug", 1.15, "rustle", 0.4), ("tug", 1.2, "creak", 0.3), *beats("tug", 0.6, D["tug"] - 0.6, 0.42, 0.5),
    ("nogive", 0.1, "whoosh", 0.35), ("nogive", 0.3, "thud", 0.3), ("nogive", 0.4, "shriek", 0.22),
    *pushes("keep", 0.0, D["keep"] - 0.1, 0.12), *[("keep", t, "buzz", 0.12) for t in (0.2, 1.1, 2.0)],
    # the AED: Piak bursts in, the lid, the power, the pads, the analysis
    ("aed", 0.0, "steps", 0.32), ("aed", 0.05, "slam", 0.26), ("aed", 0.85, "thud", 0.24), *pushes("aed", 0.9, D["aed"] - 0.1, 0.1),
    ("on", 0.1, "latch", 0.34), ("on", 0.75, "click", 0.34), ("on", 0.95, "beep", 0.3), ("on", 1.0, "ding", 0.22),
    ("pads", 0.0, "rustle", 0.28), ("pads", vo_t("pads") + 0.25, "squish", 0.3), ("pads", F("pads", 0, 1) + 0.15, "squish", 0.3), ("pads", vo_t("pads") + 0.55, "pop", 0.2), ("pads", F("pads", 0, 1) + 0.45, "pop", 0.2),
    ("analyze", 0.0, "beep", 0.24), ("analyze", 0.3, "hum", 0.1), *[("analyze", t, "beep", 0.14) for t in (0.6, 1.1, 1.6, 2.1, 2.6)], ("analyze", vo_t("analyze", 1) - 0.15, "whoosh", 0.25),
    # the shock: it charges, the press, the jolt; the widow shrieks and comes apart
    ("shock", 0.2, "riser", 0.34), ("shock", SHOT_AT, "zap", 0.6), ("shock", SHOT_AT, "boom", 0.5), ("shock", SHOT_AT + 0.02, "slam", 0.35),
    ("shock", SHOT_AT + 0.17, "shriek", 0.55), ("shock", SHOT_AT + 0.17, "glitch", 0.4), ("shock", SHOT_AT + 0.6, "whoosh", 0.3),
    *pushes("resume", 0.0, D["resume"] - 0.1, 0.12), ("resume", D["resume"] - 1.0, "siren", 0.32),
    # the ambulance: the map, the ER door
    ("route", 0.0, "siren", 0.26), ("route", 0.3, "engine", 0.16), ("route", 2.8, "pop", 0.3),
    ("arrive", 0.0, "siren", 0.22), ("arrive", 0.0, "engine", 0.18), ("arrive", 1.5, "latch", 0.24),
    # the ward: the monitor; the question; the eyes
    *monitor("er", 0.1, D["er"] + D["wake"] + D["ask"] - 0.3, 0.13),
    ("ask", vo_end("ask") + 0.05, "swell", 0.22),
    ("silent", EYES, "sting", 0.6), ("silent", EYES, "swell", 0.3), *beats("silent", EYES, D["silent"] - EYES, 0.6, 0.5),
    # the choice, dragged to ปิดไว้
    *beats("choice", 0.0, D["choice"] - 0.15, 0.42, 0.55), ("choice", 0.3, "pop", 0.28), ("choice", 0.42, "pop", 0.28), ("choice", 0.75, "click", 0.3),
    ("choice", 1.3, "swell", 0.3), ("choice", 1.6, "glitch", 0.5), ("choice", 1.65, "whoosh", 0.35), ("choice", D["choice"] - 0.5, "glitch", 0.6),
    # the end card
    ("next", 0.3, "whoosh", 0.45), ("next", 0.35, "creak", 0.3), ("next", 0.7, "gong", 0.45),
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


dip(0.0, T("hook", -0.05), 0.35, 0.05)
dip(T("check", 0), T("check", -0.05), 0.4)
dip(T("tug", 0), T("nogive", -0.05), 0.15, 0.1)
dip(T("shock", 0), T("shock", -0.05), 0.35)
dip(T("silent", 0), T("silent", -0.05), 0.3)
dip(T("choice", 0), T("choice", -0.05), 0.5)
mus = mus * gain
end = int(T("choice", -0.15) * SR)
mus[end:] = 0  # hard cut to black and silence

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mix = vo + mus * duck + sfx
cut, card = int(T("choice", -0.15) * SR), int(T("next", 0.3) * SR)
mix[cut - 240:cut] *= np.linspace(1, 0, 240)
mix[cut:card] = 0  # a beat of black and silence after the cliffhanger, then only the end card's own sounds
peak = np.max(np.abs(mix))
if peak > 0.98:
    mix = np.tanh(mix / peak * 1.2) * 0.95
out = os.path.join(HERE, "mix_raw.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", out],
               input=mix.astype(np.float32).tobytes(), check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)
print("mix written", TOTAL)

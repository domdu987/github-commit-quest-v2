"""ผีแม่ม่าย EP.3 (ตอนจบ): build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX (the ward's
monitor at dawn, the widow's eyes, the family tree's gene, the shadow screen's gong, the ECG paper, the defibrillator's shock and the
rhythm coming back, the stamps on the medicine cards, the compressions at the sala, Boss's night, the last heartbeat on black) and
the Suno music bed with dips and sidechain ducking under the voice. The music stops when the screen goes black for the last line.
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


CONF = frag("confess", 0, 1) - 0.05                      # the portrait flashes
FIRE = D["icd"] - 1.2                                     # the implanted device fires
YOU_R = [0.2 + 1.6 * 380 / 1080, 0.2 + 1.6 * 640 / 1080]  # the R waves as the last trace draws

CUES = [
    # dawn on the ward: a rooster far off, the monitor, the eyes at the foot of the bed; they turn to us
    ("hook", 0.2, "rooster", 0.16), *monitor("hook", 0.1, D["hook"] + D["hook2"] - 0.4, 0.1),
    ("hook", 0.9, "swell", 0.3), *beats("hook", 0.9, D["hook"] - 0.9, 0.6, 0.4),
    ("hook2", 0.4, "whoosh", 0.18), ("hook2", 0.9, "sting", 0.55), *beats("hook2", 0.0, D["hook2"] - 0.4, 0.5, 0.45),
    ("hook2", D["hook2"] - 0.35, "glitch", 0.5), ("hook2", D["hook2"] - 0.3, "boom", 0.4),
    # the confession: the monitor under it, the portrait
    *monitor("plea", 0.2, D["plea"] + D["confess"] + D["fear"] + D["doc"] - 0.3, 0.09), ("confess", CONF, "sting", 0.32), ("confess", CONF, "swell", 0.2),
    # the family tree: the people pop, the gene runs, the count, the rings
    ("tree", 0.0, "whoosh", 0.25), *[("tree", 0.15 + k * 0.12, "pop", 0.18) for k in range(7)], ("tree", vo_t("tree") + 0.6, "riser", 0.22),
    ("tree", vo_t("tree", 1) + 0.2, "pop", 0.28), ("tree", vo_t("tree", 1) + 1.0, "ding", 0.3), *[("tree", vo_t("tree", 1) + 1.6 + k * 0.18, "ding", 0.18) for k in range(3)],
    # the shadow screen
    ("house", 0.0, "gong", 0.4), ("house", 0.2, "ching", 0.2), ("house", F("house", 0, 1) - 0.1, "sting", 0.3), ("house", F("house", 0, 1), "ding", 0.25),
    # the ECG paper; the ages
    ("screen", 0.1, "beep", 0.22), ("screen", 0.3, "motor", 0.16), *[("screen", vo_t("screen", 1) + 0.6 + k * 0.25, "pop", 0.24) for k in range(3)],
    ("result", F("result", 0, 1) - 0.1, "pop", 0.3),
    # the defibrillator: in under the skin, the lead, the quiver, the shock, the rhythm back
    ("icd", 0.1, "whoosh", 0.22), ("icd", vo_t("icd") + 0.4, "click", 0.3), ("icd", vo_t("icd") + 0.8, "whoosh", 0.18),
    ("icd", FIRE, "zap", 0.38), ("icd", FIRE + 0.35, "beep", 0.22), ("icd", FIRE + 0.85, "beep", 0.22),
    *monitor("robot", 0.2, D["robot"] - 0.3, 0.09),
    # the medicine cards: pop, stamp; the banner
    ("pills", vo_t("pills") + 0.05, "pop", 0.26), ("pills", vo_t("pills") + 0.65, "stomp", 0.32), ("pills", vo_t("pills") + 0.6, "pop", 0.26), ("pills", vo_t("pills") + 1.2, "stomp", 0.32),
    ("pills", vo_t("pills", 1) + 0.3, "ding", 0.3),
    # a month on: the class on the beat
    *pushes("sala", 0.0, D["sala"] - 0.1, 0.08),
    ("rule", 0.6, "whoosh", 0.32), ("rule", 1.15, "ding", 0.36), ("rule", 1.35, "pop", 0.24), ("rule", 1.6, "marker", 0.2),
    *pushes("teach", 0.0, D["teach"] - 0.1, 0.1), *pushes("piak", 0.0, D["piak"] - 0.1, 0.1),
    ("shirt", 0.2, "rustle", 0.25), ("shirt", vo_end("shirt") + 0.1, "ching", 0.3),
    # that night, Boss's house: the eyes; then black and the last heartbeat
    ("night", 0.0, "crickets", 0.18), ("night", 0.6, "creak", 0.18),
    ("wait", 0.5, "swell", 0.3), *beats("wait", 0.5, D["wait"] - 0.5, 0.75, 0.42),
    *[("you", t, "beep", 0.32) for t in YOU_R], *[("you", t, "heartbeat", 0.4) for t in YOU_R],
    # the end card
    ("end", 0.2, "whoosh", 0.4), ("end", 0.25, "creak", 0.26), ("end", 0.7, "gong", 0.45),
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


dip(0.0, T("hook2", -0.05), 0.35, 0.05)
dip(T("confess", 0), T("fear", -0.05), 0.55)
dip(T("night", 0), T("wait", -0.05), 0.3)
mus = mus * gain
end = int(T("you", 0.0) * SR)
mus[end:] = 0  # hard cut to black and silence

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mix = vo + mus * duck + sfx
cut, card = int(T("you", -0.15) * SR), int(T("end", 0.15) * SR)
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

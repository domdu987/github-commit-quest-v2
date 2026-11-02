"""รูพญานาค EP.3 (final): build the episode soundtrack from schedule.json: per-line levelled voice (the headman's megaphone
band-passed), synthesized SFX (cracks round the hole, the stuck barn door and the iron bar, the run to 100 m, the cave roof giving way,
thunder over the first rain, the barn's creak, collapse and splash, heartbeats under the warning, the shrine gong) and the theme with
dips and sidechain ducking under the voice. Rain is shown, never a noise bed. No choice in the final episode: the theme fades out
over the end card. Output -14 LUFS. No noise beds and no high hiss (user: "เสียงซ่าๆเอาออก")."""
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
LINES_FX = {l["id"]: l.get("fx") for l in json.load(open(os.path.join(HERE, "lines.json")))}


def bandpass(x, lo, hi):
    out = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"highpass=f={lo}:poles=2,highpass=f={lo}:poles=2,lowpass=f={hi}:poles=2,lowpass=f={hi}:poles=2", "-f", "f32le", "-"],
                         input=x.astype(np.float32).tobytes(), capture_output=True, check=True).stdout
    return np.frombuffer(out, np.float32)[:len(x)]
vo = np.zeros(N, np.float32)
for s in SC["shots"]:
    for v in s["vo"]:
        x = load(os.path.join(HERE, "vo", f"{v['id']}.wav"))
        if LINES_FX.get(v["id"]) == "megaphone":  # the headman on his loudspeaker: narrow band, a little crunch
            x = np.tanh(3 * bandpass(x, 600, 3200)) / 2
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
    ("open", 0.0, "drip", 0.2), ("open", 0.6, "crackby", 0.24), ("open", 1.8, "debris", 0.2), ("open", 2.6, "crackby", 0.2),
    ("hook", vo_t("hook") - 0.02, "sting", 0.36), ("hook", 0.3, "creak", 0.26), ("hook", 1.2, "knock", 0.2),
    ("barn", 0.1, "steps", 0.24), ("barn", 1.2, "knock", 0.26), ("barn", 1.6, "knock", 0.24), ("barn", 2.0, "latch", 0.22), ("barn", 3.2, "knock", 0.28), ("barn", 3.5, "creak", 0.22),
    *beats("barn", 2.4, D["barn"] - 2.4, 0.6, 0.24),
    ("pry", 0.4, "clang", 0.26), ("pry", 1.4, "creak", 0.3), ("pry", 2.6, "ratchet", 0.2), ("pry", 3.6, "clang", 0.3), ("pry", 4.4, "snap", 0.3), ("pry", 4.6, "creak", 0.22), ("pry", 5.6, "steps", 0.26), ("pry", 6.6, "steps", 0.24),
    ("rule", 0.1, "flap", 0.22), ("rule", 1.4, "steps", 0.26), ("rule", 2.6, "steps", 0.24), ("rule", vo_t("rule") + 1.4, "ding", 0.18),
    ("far", 0.1, "steps", 0.24), ("far", 1.5, "steps", 0.22), ("far", 2.6, "marker", 0.18),
    ("count", 0.1, "steps", 0.26), ("count", 1.3, "steps", 0.26), ("count", 2.5, "steps", 0.24), ("count", 3.7, "pant", 0.18), ("count", 4.4, "steps", 0.26),
    ("grow1", 0.2, "crackby", 0.3), ("grow1", 1.2, "debris", 0.26), ("grow1", 2.0, "crackby", 0.24),
    ("grow2", 0.2, "crackby", 0.3), ("grow2", 1.6, "boom", 0.3), ("grow2", 1.65, "debris", 0.28),
    ("myth", 0.0, "radiosq", 0.2), ("myth", 0.4, "crackle", 0.1), ("myth", 2.6, "crackby", 0.18),
    ("know1", 0.3, "drip", 0.16), ("know1", 1.8, "drip", 0.16), ("know1", 2.9, "drip", 0.14),
    ("know2", 0.3, "debris", 0.22), ("know2", 2.0, "boom", 0.42), ("know2", 2.05, "debris", 0.34),
    ("rain", 0.33, "thunder", 0.4), ("rain", 0.9, "drip", 0.14), ("rain", 1.6, "creak", 0.3), ("rain", 2.2, "creak", 0.26), ("rain", 2.53, "thunder", 0.46),
    ("sink", 0.06, "thunder", 0.5), ("sink", 0.15, "crackby", 0.4), ("sink", 0.2, "creak", 0.34), ("sink", 0.6, "quake", 0.5), ("sink", 0.62, "boom", 0.5), ("sink", 0.7, "debris", 0.4),
    ("sink", 1.4, "debris", 0.3), ("sink", 2.6, "thud", 0.36), ("sink", 2.85, "splash", 0.3), ("sink", 3.2, "plop", 0.2),
    ("loss", 0.0, "drip", 0.14), *beats("loss", 0.2, D["loss"] - 0.4, 0.9, 0.18),
    ("leaf", 0.1, "rustle", 0.2), ("leaf", 1.2, "rustle", 0.16),
    ("hand", 0.3, "swell", 0.22), ("hand", 3.5, "rustle", 0.14),
    ("ess", 0.2, "whoosh", 0.2), ("ess", vo_t("ess") + 1.7, "ding", 0.24),
    ("num", 0.2, "flap", 0.16), ("num", 1.9, "whoosh", 0.18),
    ("low", 0.2, "drip", 0.2), ("low", 1.5, "drip", 0.18), ("low", 2.6, "swell", 0.24),
    *beats("warn", 0.2, D["warn"] - 0.4, 0.75, 0.26), ("warn", vo_t("warn") + 1.9, "sting", 0.26),
    ("week", 0.2, "rooster", 0.14), ("week", 2.0, "rattle", 0.0), ("week", 2.2, "steps", 0.18),
    ("shrine", 0.3, "gong", 0.24), ("shrine", 2.8, "gong", 0.14),
    ("sell", 0.0, "radiosq", 0.18), ("sell", 0.4, "crackle", 0.1), ("sell", 2.6, "engine", 0.12),
    ("close", 0.2, "swell", 0.24), ("close", 2.0, "gong", 0.12),
    ("end", 0.15, "whoosh", 0.3), ("end", 0.5, "flap", 0.2), ("end", 1.0, "ding", 0.24),
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

# ---- music: the ทะเลลด recipe (owner 2 Nov 2569 ~21:00: "เอาซาวเพลงแบบทะเลลด ใช้ทุกคลิปเลย") ----
# the channel song suno1 from 0 s, unfiltered (no EQ, no dynaudnorm), dipped x0.4-0.55 on the scary beats, -30 dB RMS, duck 0.65
mus = load(next(p for p in (os.path.join(HERE, "..", "music", "suno1.mp3"), os.path.join(HERE, "..", "..", "music", "suno1.mp3")) if os.path.exists(p)))
while len(mus) < N:
    mus = np.concatenate([mus, mus])
mus = mus[:N]
t = np.arange(N) / SR
gain = np.ones(N, np.float32)


def dip(t0, t1, lvl, ramp=0.25):
    a = np.clip((t - (t0 - ramp)) / ramp, 0, 1) * np.clip(((t1 + ramp) - t) / ramp, 0, 1)
    np.minimum(gain, 1 - (1 - lvl) * a, out=gain)


dip(T("rain", -0.25), T("sink", 0.08), 0.4, 0.1)  # breath held before the barn goes
dip(T("warn", 0.0), T("warn", -0.2), 0.55, 0.3)  # "it's a warning"
mus = mus * gain
f0 = int(T("end", 0.0) * SR); mus[f0:] *= np.linspace(1, 0, N - f0)  # final episode: the theme fades out under the end card

# ---- levels + ducking (music sits well under the voice while it speaks; no gate), sfx low-passed (no hiss, A4) ----
from finalmix import finalize


def lowpass(x, fc):
    out = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"lowpass=f={fc}:poles=2", "-f", "f32le", "-"],
                         input=x.astype(np.float32).tobytes(), capture_output=True, check=True).stdout
    return np.frombuffer(out, np.float32)[:len(x)]


mus = level(mus, -30)
sfx = level(lowpass(lowpass(sfx, 3500), 3500), -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mus_part = (mus * duck).astype(np.float32)
mix = vo + mus_part + sfx
finalize(HERE, mix.astype(np.float32), vo.copy(), mus_part, tp=-2.4)  # one linear gain to -14 LUFS (stems at the same gain)

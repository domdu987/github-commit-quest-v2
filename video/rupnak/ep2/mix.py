"""รูพญานาค EP.2: build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX (the wash pulling
back off the title, the flopping fish, the clock spinning back, the van on the map, the shallows under running feet, the live's pings,
the tower's 08:00 test tone, the shadow screen's gong, the deep boom of the quake, the glass's faint ring, the seabed's mud and the
shutter clicks, the conch, the run, the surge round the shop, heartbeats once ยาย is missing, the choice's ticks) and the Suno
music bed with dips and sidechain ducking under the voice. The music stops when the screen goes black after the choice.
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
    ("open", 0.0, "drip", 0.2), ("open", 0.8, "crackby", 0.22), ("open", 1.8, "boom", 0.2),
    ("hook", vo_t("hook") - 0.02, "sting", 0.36), ("hook", 0.1, "crackby", 0.3), ("hook", 0.7, "crackby", 0.26), ("hook", 1.1, "creak", 0.24),
    ("out", 0.1, "steps", 0.24), ("out", 1.4, "creak", 0.16), ("out", 3.0, "steps", 0.2),
    ("rice", 0.1, "steps", 0.2),
    ("rule", 0.1, "flap", 0.22), ("rule", 2.0, "steps", 0.26), ("rule", 3.0, "steps", 0.24),
    ("tell", 0.0, "steps", 0.26), ("tell", 1.0, "steps", 0.22), ("tell", 2.2, "crackle", 0.12),
    ("nope", 0.0, "radiosq", 0.2), ("nope", 0.4, "crackle", 0.1),
    ("call", 0.3, "notif", 0.14), *[("call", vo_t("call", 1) + 0.4 + i * 0.32, "tap", 0.2) for i in range(4)], ("call", vo_t("call", 1) + 1.9, "ring", 0.18),
    ("water", 0.0, "radiosq", 0.18), ("water", 1.0, "splash", 0.14), ("water", 2.4, "splash", 0.12),
    ("stop", vo_t("stop") - 0.02, "sting", 0.28),
    ("why", 0.2, "splash", 0.2), ("why", 1.4, "debris", 0.24), ("why", 2.6, "debris", 0.2),
    ("wai", 0.3, "pop", 0.14),
    *[("pump", 0.05 + i * 0.25, "thud", 0.34 if i % 2 == 0 else 0.22) for i in range(4)], ("pump", 0.0, "heartbeat", 0.3),
    ("found", 0.0, "engine", 0.24), *[("found", 0.1 + i * 0.5, "thud", 0.16) for i in range(4)],
    ("hose", 0.0, "stream", 0.0), ("hose", 0.0, "engine", 0.24),
    ("know1", 0.3, "drip", 0.16), ("know1", 1.6, "drip", 0.14),
    ("know2", 0.3, "debris", 0.2), ("know2", 2.3, "boom", 0.42), ("know2", 2.35, "debris", 0.34),
    ("mural", 0.2, "gong", 0.24), ("mural", 1.6, "swell", 0.26), ("mural", 1.6, "heartbeat", 0.3),
    ("valve", 0.0, "engine", 0.22), ("valve", 1.0, "clang", 0.3), ("valve", 1.3, "powerdown", 0.3),
    ("sin2", 0.3, "gong", 0.16),
    ("sin3", 0.4, "scrape", 0.2),
    ("cordon", 0.2, "rooster", 0.14), ("cordon", 0.8, "rattle", 0.16),
    ("sneak", 0.2, "steps", 0.14), ("sneak", 1.4, "steps", 0.12),
    ("rumble", 0.25, "quake", 0.5), ("rumble", 0.3, "boom", 0.34), ("rumble", 0.8, "debris", 0.22),
    ("ring", 0.1, "crackby", 0.3), ("ring", 0.8, "crackby", 0.24),
    ("close", 0.2, "riser", 0.26), ("close", 2.9, "quake", 0.3), *beats("close", 0.4, D["close"] - 0.4, 0.7, 0.28),
    *tick3("choice", 0.0, 0.3), *beats("choice", 0.2, D["choice"] - 0.6, 0.55, 0.36), ("choice", 1.1, "scrape", 0.18), ("choice", D["choice"] - 1.3, "whoosh", 0.32),
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

# ---- music with horror dips ----
mus = load(os.path.join(HERE, "..", "music", "rupnak-theme-v2-loop.mp3"))
while len(mus) < N:
    mus = np.concatenate([mus, mus])
mus = mus[:N]
t = np.arange(N) / SR
gain = np.ones(N, np.float32)


def dip(t0, t1, lvl, ramp=0.25):
    a = np.clip((t - (t0 - ramp)) / ramp, 0, 1) * np.clip(((t1 + ramp) - t) / ramp, 0, 1)
    np.minimum(gain, 1 - (1 - lvl) * a, out=gain)


dip(T("pump", 0.0), T("pump", 1.0), 0.35, 0.08)

mus = mus * gain
end = int(T("choice", -0.12) * SR)
card0 = int(T("end", 0.1) * SR)
mus[end:card0] = 0  # hard cut to black, then the theme returns softly under the end card
fi = int(0.4 * SR); mus[card0:card0 + fi] *= np.linspace(0, 1, fi)

# ---- levels: music audible under a gentle duck (A5), sfx low-passed (no hiss, A4), one linear gain to -14 LUFS ----
from finalmix import duck_curve, finalize
def dyn(x):  # even out the plucked theme's peaks and gaps so it reads as a continuous score
    out = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", "dynaudnorm=f=400:g=21:m=12", "-f", "f32le", "-"],
                         input=x.astype(np.float32).tobytes(), capture_output=True, check=True).stdout
    return np.frombuffer(out, np.float32)[:len(x)]
def highpass(x, fc):  # thin the theme's low end so the phone-band melody carries the level, not the bass
    out = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"highpass=f={fc}:poles=2", "-f", "f32le", "-"],
                         input=x.astype(np.float32).tobytes(), capture_output=True, check=True).stdout
    return np.frombuffer(out, np.float32)[:len(x)]
def lowpass(x, fc):
    out = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"lowpass=f={fc}:poles=2", "-f", "f32le", "-"],
                         input=x.astype(np.float32).tobytes(), capture_output=True, check=True).stdout
    return np.frombuffer(out, np.float32)[:len(x)]
mus = level(highpass(highpass(lowpass(dyn(mus), 6000), 380), 380), -19.1)
sfx = level(lowpass(lowpass(sfx, 3500), 3500), -27)
mus_part = mus * duck_curve(vo, 0.635)
mix = vo + mus_part + sfx
cut, card = int(T("choice", -0.12) * SR), int(T("end", 0.1) * SR)
for x in (mix, mus_part):
    x[cut - 240:cut] *= np.linspace(1, 0, 240)
mix[cut:card] = 0
finalize(HERE, mix.astype(np.float32), vo.copy(), mus_part.astype(np.float32), tp=-2.4)

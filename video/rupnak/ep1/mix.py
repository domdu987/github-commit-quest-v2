"""ทะเลลด EP.1: build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX (the wash pulling
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
    # hook: incense crackle, a far rumble under the field, the bike idling, a clod drops; sting on "อย่า"
    ("open", 0.0, "crackle", 0.16), ("open", 0.0, "boom", 0.22), ("open", 0.6, "motor", 0.12), ("open", 1.6, "debris", 0.2),
    ("hook", vo_t("hook") - 0.02, "sting", 0.36), ("hook", 0.3, "crackby", 0.22), ("hook", 0.9, "debris", 0.24),
    ("crowd", 0.2, "ching", 0.14), ("crowd", 1.4, "crackle", 0.12),
    # the board rolls back: rewind + wooden ticks + chalk scrape
    ("lotto", 0.05, "rewind", 0.34), ("lotto", 0.2, "rattle", 0.22), ("lotto", 1.3, "clack", 0.0), ("lotto", 1.5, "scrape", 0.2),
    ("map", 0.2, "whoosh", 0.26), ("map", 0.6, "engine", 0.12), ("map", D["map"] - 0.8, "pop", 0.24),
    ("arrive", 0.2, "rustle", 0.12), ("arrive", 1.0, "notif", 0.12),
    ("ton", 0.0, "steps", 0.22), ("ton", 1.2, "rustle", 0.16),
    ("door", 0.2, "creak", 0.28), ("door", 1.2, "latch", 0.22), ("door", 1.6, "creak", 0.2),
    # night: the far pump thumps (a clue)
    *[("night", 0.3 + i * 0.5, "thud", 0.12) for i in range(6)], *[("notch", 0.2 + i * 0.6, "thud", 0.07) for i in range(5)],
    ("notch", 1.4, "scrape", 0.24), ("notch", 1.9, "scrape", 0.2),
    ("rumor", 0.3, "creak", 0.12),
    ("rule", 0.1, "flap", 0.24), ("rule", 0.8, "scrape", 0.12), ("rule", 1.4, "ding", 0.14),
    ("morning", 0.0, "rooster", 0.2), ("morning", 0.6, "steps", 0.2),
    ("sell", 0.2, "ching", 0.18), ("sell", 0.9, "crackle", 0.12),
    ("legend", 0.2, "gong", 0.26), ("legend", 3.4, "boom", 0.22),
    ("know0", 0.3, "drip", 0.18), ("know0", 1.6, "drip", 0.16), ("know0", 3.0, "drip", 0.14),
    ("cave", 0.4, "boom", 0.18), ("cave", 1.5, "swell", 0.2),
    ("pray", 0.1, "crackle", 0.16), ("ask", 0.1, "crackle", 0.12),
    ("lean", 0.2, "debris", 0.2), ("lean", vo_t("lean") - 0.02, "sting", 0.32), ("lean", 1.4, "crackby", 0.2),
    ("crack", 0.1, "crackby", 0.3), ("crack", 1.0, "crackby", 0.26), ("crack", 1.6, "steps", 0.2),
    # 0.4 s silence, then the collapse
    ("collapse", 0.55, "quake", 0.5), ("collapse", 0.6, "debris", 0.46), ("collapse", 0.6, "boom", 0.5), ("collapse", 1.0, "debris", 0.3),
    ("know1", 0.2, "crackby", 0.2), ("know1", 1.4, "crackby", 0.16),
    ("know2", 0.2, "pop", 0.2), ("know2", 0.7, "pop", 0.2), ("know2", 1.2, "pop", 0.2), ("know2", 0.0, "steps", 0.2),
    ("thong2", 0.1, "debris", 0.14),
    ("home", 0.3, "drip", 0.2), ("home", 1.0, "crackby", 0.26), ("home", 2.4, "crackby", 0.2),
    ("fear", 0.2, "heartbeat", 0.3), ("fear", 1.0, "heartbeat", 0.3), ("fear", 1.8, "heartbeat", 0.3),
    ("close", 0.2, "riser", 0.26), ("close", 1.2, "quake", 0.34), *beats("close", 0.4, D["close"] - 0.4, 0.75, 0.3),
    *tick3("choice", 0.0, 0.3), *beats("choice", 0.2, D["choice"] - 0.6, 0.55, 0.36), ("choice", 1.1, "scrape", 0.18), ("choice", D["choice"] - 1.3, "whoosh", 0.32),
    ("end", 0.15, "whoosh", 0.3), ("end", 0.5, "flap", 0.2), ("end", 1.2, "flap", 0.16), ("end", 0.8, "ding", 0.24),
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


dip(T("collapse", 0.0), T("collapse", 0.55), 0.05, 0.08)

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
mus = level(highpass(highpass(lowpass(dyn(mus), 6000), 380), 380), -20)
sfx = level(lowpass(lowpass(sfx, 3500), 3500), -27)
mus_part = mus * duck_curve(vo, 0.6)
mix = vo + mus_part + sfx
cut, card = int(T("choice", -0.12) * SR), int(T("end", 0.1) * SR)
for x in (mix, mus_part):
    x[cut - 240:cut] *= np.linspace(1, 0, 240)
mix[cut:card] = 0
finalize(HERE, mix.astype(np.float32), vo.copy(), mus_part.astype(np.float32))

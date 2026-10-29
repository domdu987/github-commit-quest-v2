"""ตึกโยก EP.1: build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX (the ward's
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


def quake(k, a, b, g=0.5, step=2.4):  # the building's rumble, overlapping copies between a and b (seconds into shot k)
    return [(k, a + i * step, "quake", g) for i in range(int(max(0, b - a - 0.5) / step) + 1)]


def tick3(k, a, g=0.3):  # the choice ring: three ticks
    return [(k, a + i * 1.0, "tick", g) for i in range(3)]


TS = D["tower"]
CUES = [
    # the opener: the tower sways, the pool slops over, the birds go; the title lands
    *quake("open", 0.0, D["open"], 0.45), ("open", 0.1, "creak", 0.3), ("open", 0.15, "sting", 0.3), ("open", 0.55, "flap", 0.12), ("open", 1.2, "splash", 0.18),
    ("open", 0.8, "pop", 0.25), ("open", 2.6, "creak", 0.24),
    # first person in the corridor: rumble, rattles, the swinging sign, a flickering tube
    *quake("hook", 0.0, D["hook"], 0.55), ("hook", 0.2, "rattle", 0.3), ("hook", 0.5, "buzz", 0.18), ("hook", 1.4, "buzz", 0.16), ("hook", 1.0, "creak", 0.3),
    # two minutes back: the tape, the app pings
    ("back", 0.0, "rewind", 0.3), ("back", 0.7, "whoosh", 0.25), ("back", 1.1, "notif", 0.3), ("back", 1.5, "pop", 0.22),
    # the lobby: footsteps on stone, the guard's fan, a lift chimes
    *[("lobby", 0.1 + i * 0.48, "tap", 0.0) for i in range(0)], ("lobby", 0.1, "steps", 0.12), ("lobby", 1.2, "steps", 0.1), ("lobby", D["lobby"] - 0.8, "liftding", 0.26),
    # the lift: the button, the hum of the ride, the arrival
    ("lift", 0.42, "click", 0.4), ("lift", 0.5, "hum", 0.16), ("lift", D["lift"] - 0.2, "liftding", 0.3),
    # 2714: the whistle, the door
    ("door", 0.05, "latch", 0.3), ("door", 0.15, "whistle", 0.36), ("bag", 0.15, "rustle", 0.3), ("whistle", 0.1, "rustle", 0.18),
    # 13:20: the phone's minute flips, the rings in the glass, the first rumble
    ("ripple", vo_t("ripple") - 0.05, "tick", 0.3), ("ripple", 0.3, "drip", 0.25), ("ripple", 0.6, "rattle", 0.2), ("ripple", 1.0, "swell", 0.3),
    *quake("ripple", 1.2, D["ripple"], 0.55), ("ripple", 1.6, "creak", 0.35),
    # outside: the tower, the spilling pool, the birds
    *quake("tower", 0.0, TS, 0.65), ("tower", 0.2, "flap", 0.16), ("tower", 0.5, "splash", 0.25), ("tower", 1.4, "splash", 0.2), ("tower", 0.9, "creak", 0.35),
    # มิว pulls you
    *quake("panic", 0.0, D["panic"], 0.6), ("panic", 0.3, "rattle", 0.3),
    # the choice: the ring ticks, the pick
    *quake("choice1", 0.0, D["choice1"], 0.35), ("choice1", 0.05, "whoosh", 0.28), *tick3("choice1", 0.0, 0.32), ("choice1", 2.7, "click", 0.4),
    # the wrong way: run, the doors, the ride down, the power dies, a jolt; the red lamp hums
    ("wrong", 0.0, "steps", 0.3), ("wrong", 0.5, "latch", 0.3), ("wrong", 0.6, "hum", 0.22), *quake("wrong", 0.6, D["wrong"], 0.5), ("wrong", 0.9, "buzz", 0.2),
    ("stuck", 0.0, "powerdown", 0.55), ("stuck", 0.05, "thud", 0.5), ("stuck", 0.1, "clang", 0.32), ("stuck", 0.9, "buzz", 0.14), *beats("stuck", 1.0, D["stuck"] - 1.0, 0.75, 0.42),
    # rewind to the choice: ✗ ✓
    ("rewind", 0.0, "rewind", 0.35), ("rewind", 0.7, "glitch", 0.25), ("rewind", 0.85, "buzz", 0.25), ("rewind", 1.1, "ding", 0.35),
    # under the table: you drop, the lamp swings and crashes onto the tabletop, the table walks
    *quake("drop", 0.0, D["drop"], 0.6), ("drop", 0.75, "thud", 0.4), ("drop", 0.4, "rattle", 0.3),
    *quake("cover", 0.0, D["cover"], 0.55), ("cover", 1.12, "clang", 0.42), ("cover", 1.15, "shatter", 0.22), *[("cover", F("cover", 0, 0) - 0.1 + i * 0.55, "pop", 0.26) for i in range(2)], ("cover", F("cover", 0, 1), "pop", 0.26),
    *quake("slide", 0.0, D["slide"], 0.6), *[("slide", t, "scrape", 0.45) for t in (0.4, 1.3, 2.3, 3.2)], ("slide", 0.8, "rattle", 0.25),
    # the window bursts; the power cuts
    *quake("glass", 0.0, D["glass"], 0.6), ("glass", 0.2, "crackle", 0.3), ("glass", 0.5, "crackle", 0.3), ("glass", 0.95, "shatter", 0.75), ("glass", 1.0, "powerdown", 0.35), ("glass", 1.3, "debris", 0.25),
    # แม่'s plan: the marker, the zones pop
    *quake("danger", 0.0, D["danger"], 0.25), ("danger", 0.1, "rustle", 0.25), *[("danger", F("danger", 0, j) + d, "pop", 0.25) for j, d in ((0, 0), (1, 0), (1, 0.25), (1, 0.5))], ("danger", D["danger"] - 1.0, "ding", 0.3),
    # มิว tries to run; the corridor ceiling crashes where you would have been
    *quake("run", 0.0, D["run"], 0.55), ("run", 0.6, "rustle", 0.3),
    *quake("fall", 0.0, D["fall"], 0.55), ("fall", 0.9, "debris", 0.4), ("fall", 1.0, "slam", 0.42), ("fall", 1.4, "slam", 0.36), ("fall", 1.8, "thud", 0.4), ("fall", 1.45, "glitch", 0.3),
    # the note on the fridge (the rule): the paper, the highlighter
    *quake("rule", 0.0, 1.7, 0.4), ("rule", 1.7, "whoosh", 0.32), ("rule", 1.75, "rustle", 0.3), ("rule", 2.1, "marker", 0.26), ("rule", 2.6, "ding", 0.34), ("rule", 2.2, "rattle", 0.15),
    # it stops: silence, dust; then the fire alarm
    ("stop", 0.0, "creak", 0.3), *[("stop", 1.2 + i * 1.9, "alarm", 0.32) for i in range(2)],
    # the seismogram: the pen ticks, a thump for each aftershock
    *[("after", 0.3 + i * 0.12, "tick", 0.12) for i in range(18)], *[("after", 0.25 + (D["after"] - 0.9) * f, "boom", 0.2) for f in (0.58, 0.72, 0.86)], ("after", 0.25 + (D["after"] - 0.9) * 0.75, "pop", 0.3),
    *[("after", 0.6 + i * 1.9, "alarm", 0.12) for i in range(2)],
    # the real quake: a deep boom at the epicentre, the rings, the pins, the counter
    ("real", 0.1, "boom", 0.45), ("real", 0.3, "whoosh", 0.3), ("real", 0.35, "pop", 0.3), ("real", vo_t("real", 1) + 1.4, "pop", 0.32), ("real", vo_t("real", 2), "ding", 0.3),
    *[("real", vo_t("real", 2) + 0.3 + i * 0.12, "tick", 0.12) for i in range(18)],
    # แม่ doesn't answer
    *[("mom", 0.3 + i * 0.9, "ring", 0.2) for i in range(2)], ("mom", D["mom"] - 0.9, "beep", 0.3),
    # the dark corridor: the emergency lamp dies
    ("dark", 0.2, "buzz", 0.2), ("dark", 1.4, "powerdown", 0.3), *beats("dark", 0.5, D["dark"] - 0.5, 0.8, 0.35),
    # the candle: the drawer, the box of matches; the canister (no hiss: the picture and the word carry it)
    ("candle", 0.2, "latch", 0.25), ("candle", 1.0, "rustle", 0.25), ("candle", vo_t("candle", 1) - 0.2, "swell", 0.32), *beats("candle", vo_t("candle", 1), D["candle"] - vo_t("candle", 1), 0.7, 0.4),
    # your call: ticks, the heartbeat quickens, the match strikes → black
    *tick3("choice2", 0.0, 0.32), *beats("choice2", 0.2, D["choice2"] - 0.6, 0.55, 0.42), ("choice2", D["choice2"] - 0.45, "strike", 0.6),
    # the end card
    ("end", 0.15, "whoosh", 0.35), ("end", 0.3, "whistle", 0.22), ("end", 0.7, "ding", 0.3),
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


dip(T("back", 0), T("ripple", 1.0), 0.55)
dip(T("stuck", 0.0), T("stuck", -0.05), 0.3, 0.05)
dip(T("stop", 0), T("real", 0), 0.35)
dip(T("mom", 0), T("choice2", 0), 0.4)
mus = mus * gain
end = int(T("choice2", -0.24) * SR)
mus[end:] = 0  # hard cut to black and silence

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mix = vo + mus * duck + sfx
cut, card = int(T("choice2", -0.24) * SR), int(T("end", 0.1) * SR)
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

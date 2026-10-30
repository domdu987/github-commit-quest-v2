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
    # the opener: the wash pulls back off the title (a sound on frame 0), fish flop on the wet sand
    ("open", 0.0, "splash", 0.32), ("open", 0.35, "bubbles", 0.18), ("open", 1.3, "squish", 0.2), ("open", 2.2, "squish", 0.16),
    # the hook: the fish flops, the child's hand reaches; a sting on "อย่า"
    ("hook", 0.0, "squish", 0.3), ("hook", 0.5, "plop", 0.2), ("hook", vo_t("hook") - 0.02, "sting", 0.34), ("hook", 1.2, "rustle", 0.16),
    # two hours back: the clock's hands spin back, then tick on
    ("clock", 0.1, "rewind", 0.34), ("clock", 0.2, "whoosh", 0.2), *ticks("clock", D["clock"] - 1.0, D["clock"] - 0.1, 0.22, 0.5),
    # the map: the route draws, the van, the pin drops
    ("map", 0.2, "whoosh", 0.26), ("map", 0.6, "engine", 0.14), ("map", D["map"] - 1.4, "pop", 0.3), ("map", D["map"] - 1.1, "ding", 0.26),
    # arrival: จูน goes live, ตังค์ cheers
    ("arrive", 0.15, "notif", 0.3), ("arrive", 0.5, "pop", 0.2), ("arrive", 1.2, "rustle", 0.12),
    # ตังค์ runs through the shallows
    *[("tang", 0.25 + i * 0.42, "splash", 0.12) for i in range(int(D["tang"] / 0.42))],
    # the account: taps on the phone, the account is made
    *[("acct", 0.3 + i * 0.22, "tap", 0.16) for i in range(4)], ("acct", vo_end("acct", 0) - 0.4, "notif", 0.28),
    # the photo: the cloth rubs the glass, a glint
    ("photo", 0.3, "rustle", 0.24), ("photo", 1.0, "rustle", 0.22), ("photo", 1.7, "rustle", 0.2), ("photo", D["photo"] - 0.9, "ching", 0.3),
    # 08:00 Wednesday: the tower's test tone over the beach
    ("test", 0.3, "siren", 0.26), ("test", 0.25, "pop", 0.22),
    # the whisper about ตาจุ่น
    ("rumor", 0.2, "swell", 0.2),
    # ยาย's board: it lands, the rule is painted, the coin pops
    ("rule", 0.1, "whoosh", 0.3), ("rule", 0.35, "thud", 0.22), ("rule", 0.8, "marker", 0.26), ("rule", 1.6, "ding", 0.32),
    # the shadow screen: a gong, the sea drawing back, the elders lead the children up, the seven-layer wave
    ("legend", 0.1, "gong", 0.36), ("legend", 0.6, "swell", 0.24), *[("legend", 3.9 + i * 0.5, "drum", 0.16) for i in range(6)], ("legend", 6.4, "roar", 0.32),
    # the quake far out: a deep boom, the rings, the pin at the coast
    ("quake", 0.3, "boom", 0.5), ("quake", 0.6, "whoosh", 0.28), ("quake", D["quake"] - 1.2, "pop", 0.3), ("quake", D["quake"] - 1.0, "ding", 0.24),
    # the glass barely trembles: almost nothing
    ("cup", 0.3, "ching", 0.16), ("cup", 1.4, "ching", 0.12),
    # the sea draws back: water running off, the mud, birds lift
    ("recede", 0.1, "bubbles", 0.26), ("recede", 0.7, "swell", 0.24), ("recede", 1.6, "squelch", 0.2), ("recede", 2.0, "flap", 0.16),
    # the live: comments ping in, ตังค์'s feet on the mud, the fish
    *[("fish", t, "notif", 0.16) for t in (0.3, 1.0, 1.8, 2.6, 3.3)], ("fish", 0.6, "squish", 0.2), ("fish", 1.5, "squelch", 0.18), ("fish", 2.4, "squelch", 0.16),
    # people walk out on the seabed taking pictures; the birds flee
    ("walk", 0.3, "flap", 0.24), ("walk", 1.1, "shutter", 0.3), ("walk", 1.9, "shutter", 0.26), ("walk", 0.8, "squelch", 0.14),
    # the cross-sections
    ("know1", 0.1, "whoosh", 0.28), ("know1", 0.6, "swell", 0.24), ("know1", D["know1"] - 1.4, "pop", 0.24),
    ("know2", 0.1, "whoosh", 0.28), ("know2", 0.5, "pop", 0.26), ("know2", vo_t("know2", 1), "pop", 0.26), ("know2", vo_t("know2", 1) + 0.3, "whoosh", 0.22),
    # go up now: the time-left bar drains, the riser
    ("know3", 0.3, "pop", 0.26), *ticks("know3", 0.6, D["know3"] - 0.2, 0.16, 0.5), ("know3", D["know3"] - 1.4, "riser", 0.28),
    # the conch, then the shout
    ("conch", 0.05, "trumpet", 0.5), ("conch", 0.1, "whistlefar", 0.2),
    # the run: feet, breath, the duck ring bounces on the sand
    *[("run", 0.1 + i * 0.32, "steps", 0.16) for i in range(int(D["run"] / 0.32))], ("run", 0.4, "pant", 0.2), ("run", vo_t("run", 1) - 0.2, "plop", 0.32), ("run", vo_t("run", 1) + 0.05, "plop", 0.18),
    # up the steps, the tower's alarm
    *[("hill", 0.1 + i * 0.34, "steps", 0.14) for i in range(int(D["hill"] / 0.34))], ("hill", 0.2, "pant", 0.2), ("hill", 0.3, "siren", 0.18),
    # the first wave: the surge roars in round the shop, things knock about, it drains; then quiet feet going back down
    ("wave1", 0.2, "roar", 0.55), ("wave1", 0.9, "splash", 0.32), ("wave1", 1.3, "debris", 0.3), ("wave1", 1.7, "crackle", 0.18), ("wave1", 2.3, "bubbles", 0.2),
    *[("wave1", vo_t("wave1", 1) + 0.3 + i * 0.4, "steps", 0.1) for i in range(4)],
    # the sea goes out again: the long breath before the heartbeat
    ("again", 0.2, "swell", 0.3), ("again", 0.9, "bubbles", 0.16), *beats("again", 1.2, D["again"] - 1.2, 0.8, 0.36),
    # ยาย is missing
    *beats("yai", 0.1, D["yai"] - 0.1, 0.7, 0.42), ("yai", vo_t("yai") - 0.05, "sting", 0.26),
    # the empty shop: the loose door creaks, the shell chime, the far alarm
    ("clue", 0.2, "creak", 0.3), ("clue", 0.6, "ching", 0.12), ("clue", 1.3, "ching", 0.1), ("clue", 0.9, "rustle", 0.14), ("clue", 0.4, "siren", 0.1),
    # the white line
    ("close", 0.2, "riser", 0.3), *beats("close", 0.4, D["close"] - 0.4, 0.75, 0.34),
    # the choice: ticks, the heartbeat quickens, the pull → black
    *tick3("choice", 0.0, 0.32), *beats("choice", 0.2, D["choice"] - 0.6, 0.55, 0.4), ("choice", D["choice"] - 1.3, "whoosh", 0.36), ("choice", D["choice"] - 1.2, "splash", 0.4),
    # the end card: the paper note flaps
    ("end", 0.15, "whoosh", 0.32), ("end", 0.5, "flap", 0.2), ("end", 1.2, "flap", 0.16), ("end", 0.8, "ding", 0.26),
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


dip(T("recede", 0), T("know1", 0), 0.55)
dip(T("again", 0), T("choice", 0), 0.4)
mus = mus * gain
end = int(T("choice", -0.12) * SR)
mus[end:] = 0  # hard cut to black and silence

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mix = vo + mus * duck + sfx
cut, card = int(T("choice", -0.12) * SR), int(T("end", 0.1) * SR)
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

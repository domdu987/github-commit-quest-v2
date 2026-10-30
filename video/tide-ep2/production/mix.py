"""ทะเลลด EP.2: build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX (จูน's feet on the
steps, the sting and the grip on "อย่า", the struggle, ยาย's board, the riser as the line thickens, the series of crests and the
height tags, the tower's siren under the announcement, the people running back up, the shell chime at the shop, the roar of the
second wave, the shop breaking up, the duck ring on the flood, a silence, the typing and the pinned comment, the tourist on the
cooler, the third wave and the windows going, the last comment, the live cutting out, the choice's ticks) and the Suno music bed
with dips and sidechain ducking under the voice. The music stops when the screen goes black after the choice.
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
    # the hook: a sound on frame 0 (the long breath of the sea still out), จูน's feet on the steps, her breath
    ("open", 0.0, "swell", 0.3), *[("open", 0.35 + i * 0.3, "steps", 0.09) for i in range(8)], ("open", 0.2, "pant", 0.14), *beats("open", 0.2, D["open"] - 0.2, 0.7, 0.2),
    # the old hand clamps her wrist on "อย่า": the sting, the grip, the sandal skids
    ("grab", vo_t("grab") - 0.02, "sting", 0.38), ("grab", vo_t("grab"), "snap", 0.3), ("grab", 0.3, "scrape", 0.2),
    # the struggle against the grip
    ("pull", 0.1, "rustle", 0.24), ("pull", 0.9, "rustle", 0.2), ("pull", 1.5, "scrape", 0.14), *beats("pull", 0.2, D["pull"] - 0.2, 0.6, 0.26),
    # ตาจุ่น: "ครั้งนี้… ตาไม่ปล่อย"
    ("face", 0.1, "swell", 0.22),
    # ยาย's board: it lands, rule 1 ticked, rule 2 brushed on, its coin pops
    ("rule", 0.1, "whoosh", 0.3), ("rule", 0.35, "thud", 0.22), ("rule", 0.8, "marker", 0.26), ("rule", 1.6, "ding", 0.32),
    # จูน: "ตารู้ได้ไง…"
    ("how", 0.1, "swell", 0.14),
    # from the hill: the people back down on the beach, a bird lifts, the line thickens
    ("below", 0.3, "flap", 0.14), ("below", 1.0, "riser", 0.26),
    # the series: the board lands, three crests roll in, the gaps open with the clocks
    ("series", 0.1, "whoosh", 0.28), ("series", 0.15, "thud", 0.18),
    *[("series", t, "swell", 0.2) for t in (vo_t("series", 0) + 0.1, vo_t("series", 0) + 0.7, F("series", 0, 1))],
    ("series", vo_t("series", 1) + 0.2, "pop", 0.26), *ticks("series", vo_t("series", 1) + 0.4, D["series"] - 0.3, 0.14, 0.5),
    # the heights: each crest comes in, its tag lands on the number; the third is red
    ("heights", 0.1, "whoosh", 0.26), *[x for i in (1, 2, 3) for x in (("heights", F("heights", i, 1) - 0.6, "swell", 0.2), ("heights", F("heights", i, 1), "pop", 0.28))],
    ("heights", F("heights", 3, 1) + 0.05, "sting", 0.24),
    # back on the hill
    ("stay", 0.2, "rustle", 0.12), ("stay", 1.2, "flap", 0.1),
    # the tower for real: the siren under the announcement, the panel lands, the second line slams in
    ("siren", 0.0, "siren", 0.3), ("siren", 2.0, "siren", 0.24), ("siren", 0.05, "whoosh", 0.22), ("siren", F("siren", 0, 1), "thud", 0.22),
    # the people below turn and run back up the steps
    ("turn", vo_end("turn") + 0.05, "siren", 0.14), *[("turn", 0.2 + i * 0.24, "steps", 0.08 if 0.2 + i * 0.24 < vo_end("turn") else 0.15) for i in range(13)], ("turn", vo_end("turn") + 0.05, "pant", 0.2),
    # down at the shop: the shell chime, the far siren, the loose door
    ("shop", 0.2, "ching", 0.14), ("shop", 0.5, "siren", 0.08), ("shop", 1.4, "creak", 0.16),
    # she looks up at the hotel; the riser into the wall of water
    ("hotel", 0.9, "swell", 0.22), ("hotel", D["hotel"] - 1.2, "riser", 0.28),
    # the second wave at beach level
    ("wall", 0.0, "roar", 0.5), ("wall", 1.6, "roar", 0.42), ("wall", 0.5, "debris", 0.26), ("wall", 2.2, "crackle", 0.18), ("wall", 3.0, "splash", 0.3),
    # from the hill: the village floods, ยาย's shop breaks up and goes under
    ("smash", 0.0, "roar", 0.46), ("smash", 1.2, "debris", 0.32), ("smash", D["smash"] * 0.45, "crackle", 0.3), ("smash", D["smash"] * 0.5, "shatter", 0.18),
    ("smash", 3.4, "splash", 0.28), ("smash", 3.9, "bubbles", 0.2),
    # the duck ring floats past the hotel on the flood
    ("duck", 0.1, "bubbles", 0.2), ("duck", 0.9, "plop", 0.14), ("duck", 1.6, "debris", 0.12),
    # silence: only the heart
    *beats("hush", 0.4, D["hush"] - 0.4, 0.9, 0.3),
    # the live: a comment, ยายพร❤️ typing, her comment pops in pinned (the twist), the phone zooms in on the hotel
    ("live", 0.15, "notif", 0.14), *[("live", 0.35 + i * 0.16, "tap", 0.08) for i in range(4)], ("live", vo_t("live") - 0.35, "notif", 0.34),
    ("live", vo_t("live") - 0.33, "sting", 0.3), ("live", vo_t("live", 1) - 0.15, "whoosh", 0.12),
    # a tourist clings to a cooler
    ("raft", 0.1, "splash", 0.26), ("raft", 0.8, "bubbles", 0.18), ("raft", 1.6, "splash", 0.2), ("raft", 2.4, "debris", 0.14),
    # ตาจุ่น: "มันยังไม่จบ…"
    ("notyet", 0.1, "swell", 0.26), *beats("notyet", 0.3, vo_end("notyet") + 0.1, 0.75, 0.3), ("notyet", vo_end("notyet") + 0.15, "riser", 0.26),  # then the bay drawing back again
    # the third wave climbs the hotel: the roar, the windows going
    ("wave3", 0.0, "roar", 0.5), ("wave3", 1.3, "roar", 0.4), ("wave3", 0.8, "debris", 0.28), ("wave3", 2.0, "shatter", 0.2), ("wave3", 2.8, "splash", 0.28),
    # her last comment; she types… and stops
    ("comment", 0.3, "notif", 0.3), *[("comment", 1.2 + i * 0.25, "tap", 0.07) for i in range(6)],
    # ตังค์: "ยาย… ไม่พิมพ์แล้ว…"
    *beats("tang", 0.2, D["tang"] - 0.2, 0.8, 0.3),
    # the live cuts out on "ดับ", then nothing
    ("close", 0.2, "swell", 0.2), ("close", vo_end("close", 1) - 0.22, "glitch", 0.4), ("close", vo_end("close", 1) - 0.18, "powerdown", 0.3),
    # the choice: ticks, the heartbeat quickens, the pull → black
    *tick3("choice", 0.0, 0.32), *beats("choice", 0.2, D["choice"] - 0.6, 0.55, 0.4), ("choice", D["choice"] - 1.3, "whoosh", 0.36), ("choice", D["choice"] - 1.2, "splash", 0.4),
    # the end card: the paper note flaps, the "ตอนจบ" sticker is stamped on
    ("end", 0.15, "whoosh", 0.32), ("end", 0.5, "flap", 0.2), ("end", 1.0, "thud", 0.26), ("end", 1.05, "ding", 0.24), ("end", 1.6, "flap", 0.16),
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


dip(T("wall", 0), T("duck", 0), 0.5)             # under the roar of the second wave
dip(T("hush", 0), T("live", vo_t("live")), 0.12)  # the silence before the pinned comment
dip(T("wave3", 0), T("choice", 0), 0.4)
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
# single-pass loudnorm lands ~0.8 dB under its target on this mix: aim at -13.2 to measure -14
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", "loudnorm=I=-13.2:TP=-1.5:LRA=11", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)
print("mix written", TOTAL)

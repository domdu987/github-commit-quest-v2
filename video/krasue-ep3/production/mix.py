"""แสงกระสือ EP.3 (สูตรเสียงกอย re-cut) (the finale): build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX for a flooded village
at night with live wires (the mains hum, a broken line arcing in the water, the main switch thrown, the power dying, wading steps, the
old comic's pages) and the Suno music bed with dips before the scares and sidechain ducking under the voice. Output -14 LUFS, hard cut
to silence after the choice. No noise beds and no high hiss (user: "เสียงซ่าๆเอาออก")."""
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
FC = frag("face", 0, 1) - 0.2     # the face at the window
WK = vo_t("wake", 0) - 0.4        # ป้าแช่ม opens her eyes
GO = frag("morning", 1, 1)        # ฝน heads for the stairs
SHOO = frag("joke", 1, 1)         # "หลบไป!": เต้ย runs
WS = vo_t("who", 1) - 0.15        # cut to the lever close up
SL = frag("who", 1, 1) - 0.2      # the slime drips
CUT3 = frag("know3", 0, 2) + 0.4  # the diagram's lever goes down
GL = frag("glint", 0, 1)          # her eyes flash green


def zaps(k, ts, g=0.5):
    return [(k, t, "zap", g) for t in ts]


def knocks(k, t0, n, gap=0.32, g=0.8):
    return [(k, t0 + i * gap, "knock", g) for i in range(n)]


CUES = [
    ("recap", 0.0, "glitch", 0.5), *beats("recap", 0.0, D["recap"], 0.4, 0.6),
    ("hook", 0.2, "click", 0.3), ("hook", D["hook"] - 1.4, "creak", 0.5), ("hook", D["hook"] - 0.55, "clang", 0.6), *beats("hook", D["hook"] - 1.4, 1.4, 0.42, 0.5),
    ("hook", D["hook"] - 0.5, "sting", 1.0), ("hook", D["hook"] - 0.5, "glitch", 0.7), ("hook", D["hook"] - 0.45, "boom", 0.6),
    ("latch", 0.3, "latch", 0.5), *beats("latch", 0.0, D["latch"], 0.42, 0.5),
    *knocks("open", 0.05, 2, 0.3, 0.6), *beats("open", 0.0, D["open"], 0.42, 0.55),
    ("toey", F("toey", 0, 1) - 0.2, "swell", 0.45), *beats("toey", 0.0, D["toey"], 0.42, 0.55),
    *beats("shush", 0.0, D["shush"], 0.38, 0.6), ("shush", F("shush", 0, 2), "swell", 0.3),
    *knocks("why", 0.05, 4, 0.26, 0.9), *beats("why", 0.0, D["why"], 0.38, 0.6),
    # koi-style: the face comes in slowly with only a heartbeat; one hit (it presses to the glass), then silence
    ("face", FC - 0.2, "swell", 0.25), *beats("face", FC, D["face"] - FC - 0.6, 0.45, 0.6),
    ("face", D["face"] - 0.55, "slam", 0.9), ("face", D["face"] - 0.55, "sting", 1.1), ("face", D["face"] - 0.5, "shriek", 0.45),
    ("dawn", F("dawn", 0, 0) + 0.1, "rooster", 0.8), ("dawn", 0.2, "swell", 0.3),
    ("morning", 0.15, "notif", 0.45), ("morning", F("morning", 0, 2), "pop", 0.35), ("morning", 1.6, "drip", 0.3),
    *[("morning", GO + 0.25 * k, "steps", 0.3) for k in range(4)], ("morning", GO + 0.2, "squelch", 0.35),
    ("reach", 0.3, "rustle", 0.3),
    ("stop", 0.05, "whoosh", 0.5), ("stop", 0.1, "slam", 0.4),
    ("know1", F("know1", 0, 1) + 0.1, "click", 0.4), ("know1", F("know1", 0, 2) + 0.1, "whoosh", 0.3), ("know1", F("know1", 0, 2) + 0.8, "ding", 0.5),
    ("joke", vo_t("joke", 1), "slam", 0.25), ("joke", SHOO + 0.2, "whoosh", 0.5), *[("joke", SHOO + 0.25 + 0.15 * k, "steps", 0.35) for k in range(4)],
    ("know2", 0.2, "drip", 0.35), ("know2", 0.9, "drip", 0.3), ("know2", F("know2", 0, 1), "swell", 0.3),
    ("know2", F("know2", 0, 2), "whoosh", 0.3), ("know2", F("know2", 0, 2) + 0.7, "ding", 0.5),
    *zaps("know3", (0.5, 0.65, 0.85, 1.05), 0.45), ("know3", F("know3", 0, 1), "swell", 0.3),
    ("know3", CUT3, "clang", 0.6), ("know3", CUT3 + 0.05, "powerdown", 0.5), ("know3", CUT3 + 0.6, "ding", 0.5),
    ("outlet", 0.3, "rustle", 0.3), ("outlet", F("outlet", 0, 1), "sting", 0.4),
    ("who", WS + 0.3, "squelch", 0.5), ("who", SL, "drip", 0.5), ("who", SL, "swell", 0.4), *beats("who", SL, D["who"] - SL, 0.42, 0.5), ("who", SL + 0.6, "glitch", 0.4),
    *[("pot", 0.2 + 0.45 * k, "steps", 0.3) for k in range(int(D["pot"] / 0.45))],
    ("mat", 0.3, "creak", 0.4), ("mat", 1.5, "swell", 0.3),
    ("rag", F("rag", 0, 1), "squelch", 0.5), ("rag", F("rag", 0, 1), "sting", 0.5), *beats("rag", F("rag", 0, 1), D["rag"] - F("rag", 0, 1), 0.42, 0.5),
    ("wake", WK, "sting", 0.4), *beats("wake", 0.0, D["wake"], 0.45, 0.45),
    ("glint", GL + 0.35, "sting", 0.45), *beats("glint", GL + 0.35, D["glint"] - GL - 0.35, 0.45, 0.5),
    ("night", 0.2, "hum", 0.4), ("night", 0.8, "swell", 0.3),
    # it calls from far off and holds still; the eyes go out; silence; then at the lens; cut
    ("call", 0.2, "swell", 0.35), *beats("call", 0.0, vo_end("call"), 0.5, 0.55),
    ("call", D["call"] - 0.5, "sting", 1.2), ("call", D["call"] - 0.48, "shriek", 0.6), ("call", D["call"] - 0.5, "slam", 0.7),
    ("last", 0.3, "hum", 0.3), *beats("last", 0.0, D["last"] - 0.6, 0.6, 0.4), ("last", D["last"] - 0.25, "boom", 0.6),
    ("end", 0.3, "whoosh", 0.5), ("end", 0.45, "drip", 0.6), ("end", 0.8, "gong", 0.5),
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


dip(0.0, T("recap", -0.05), 0.3, 0.05)
dip(T("hook", 0), T("hook", -0.05), 0.35)
dip(T("open", 0), T("face", FC - 0.3), 0.3)
dip(T("rag", 0), T("glint", -0.05), 0.35)
dip(T("face", FC - 0.3), T("face", -0.05), 0.15)
dip(T("call", 0), T("call", vo_end("call")), 0.25)
dip(T("call", vo_end("call")), T("last", 0.4), 0.0, 0.1)  # dead silence before the hit
mus = mus * gain
end = int(T("last", -0.2) * SR)
mus[end:] = 0  # hard cut to black and silence

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mix = vo + mus * duck + sfx
cut, card = int(T("last", -0.2) * SR), int(T("end", 0.3) * SR)
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

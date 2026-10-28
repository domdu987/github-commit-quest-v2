"""เห็ดปอบ EP.3: build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX for a flooded village
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
HB = F("hungry", 0, 1) - 0.05                             # ยาย's eyes turn green on "ยายหิวข้าว"
HC, HD = D["hungry"] - 0.9, D["hungry"] - 0.5             # the dark comes down; the hit


def monitor(k, a, b, g=0.18, step=1.0):  # the bedside monitor
    return [(k, a + i * step, "beep", g) for i in range(int((b - a) / step) + 1)]


CUES = [
    ("recap", 0.0, "glitch", 0.5), *beats("recap", 0.0, D["recap"], 0.42, 0.6),
    *monitor("hook", 0.1, D["hook"] - 0.6), ("hook", 0.4, "creak", 0.3), *beats("hook", 0.3, D["hook"] - 0.3, 0.42, 0.5),
    ("hook", D["hook"] - 0.5, "sting", 1.0), ("hook", D["hook"] - 0.5, "glitch", 0.7), ("hook", D["hook"] - 0.45, "boom", 0.6),
    ("home", 0.1, "swell", 0.3), *beats("home", 0.0, D["home"], 0.5, 0.45),
    ("no", 0.05, "slam", 0.25),
    *monitor("doc", 0.1, D["doc"]),
    ("know1", 0.2, "whoosh", 0.25), ("know1", F("know1", 0, 1), "ding", 0.45), ("know1", vo_t("know1", 1) - 0.2, "riser", 0.4), ("know1", vo_t("know1", 1) + 0.6, "clang", 0.4),
    ("know2", 0.2, "whoosh", 0.3), ("know2", F("know2", 0, 1), "click", 0.45),
    ("two", 0.1, "pop", 0.3),
    ("scold", 0.05, "whoosh", 0.25),
    *monitor("night2", 0.1, D["night2"], 0.22), ("night2", F("night2", 0, 1), "swell", 0.3),
    ("relief", 0.1, "ding", 0.3),
    ("know3", 0.2, "ding", 0.4), ("know3", 0.5, "ding", 0.4), ("know3", F("know3", 0, 1), "ding", 0.5),
    ("sorry", 0.1, "steps", 0.35), ("sorry", 0.5, "steps", 0.35), ("sorry", vo_t("sorry") + 0.1, "rustle", 0.3),
    ("feet", F("feet", 0, 1), "swell", 0.35), *beats("feet", F("feet", 0, 1), D["feet"] - F("feet", 0, 1), 0.5, 0.45),
    ("odd", 0.1, "rustle", 0.3), ("odd", F("odd", 0, 2), "swell", 0.4), *beats("odd", F("odd", 0, 2), D["odd"] - F("odd", 0, 2), 0.48, 0.5),
    *monitor("wake", 0.1, D["wake"], 0.15), *beats("wake", F("wake", 0, 1), D["wake"] - F("wake", 0, 1), 0.45, 0.55),
    *monitor("sit", 0.1, D["sit"], 0.15), *beats("sit", 0.0, D["sit"], 0.5, 0.6), ("sit", 0.8, "squelch", 0.3), ("sit", 1.6, "squelch", 0.3),
    *beats("toes", 0.0, D["toes"], 0.48, 0.6), ("toes", F("toes", 0, 1), "swell", 0.35),
    # koi-style: she speaks, turns; only the eyes; hold; one hit and cut
    *beats("hungry", 0.0, HC, 0.6, 0.65), ("hungry", HB, "swell", 0.3),
    ("hungry", HD, "sting", 1.1), ("hungry", HD, "slam", 0.7), ("hungry", HD + 0.02, "shriek", 0.5),
    ("last", 0.3, "crickets", 0.3), ("last", vo_t("last", 1) + 0.6, "swell", 0.35), *beats("last", vo_t("last", 1), D["last"] - vo_t("last", 1), 0.6, 0.45),
    ("rule", 0.15, "ding", 0.35), ("rule", 0.35, "ding", 0.35), ("rule", vo_t("rule") + 0.2, "ding", 0.45), ("rule", D["rule"] - 0.25, "boom", 0.6),
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
dip(T("wake", 0), T("toes", -0.05), 0.3)
dip(T("hungry", 0), T("hungry", -0.05), 0.08, 0.1)
dip(T("last", 0), T("rule", -0.05), 0.4)
mus = mus * gain
end = int(T("rule", -0.2) * SR)
mus[end:] = 0  # hard cut to black and silence

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mix = vo + mus * duck + sfx
cut, card = int(T("rule", -0.2) * SR), int(T("end", 0.3) * SR)
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

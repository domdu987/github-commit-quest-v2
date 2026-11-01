"""รอดคนเดียว EP.2 v5: the soundtrack from schedule.json. Levelled voice, diegetic SFX from the materials on screen (the bottle, water,
the coconut, the plastic sheet in the rain, limpets, the lighter, the fire, the rotor), the plane theme (same as EP.1) ducked under the
voice, 0.5 s of total silence at the hush and the bass cut after it. Output −14 LUFS, peaks ≤ −1 dBTP. No noise beds, no HUD stings."""
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
t = np.arange(N) / SR


def load(path):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, dtype=np.float32).copy()


def place(buf, x, at, g=1.0):
    i = int(at * SR)
    j = min(len(buf), i + len(x))
    if 0 <= i < len(buf):
        buf[i:j] += x[: j - i] * g


def rms_db(x):
    x = x[np.abs(x) > 1e-4]
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)


def level(x, target):
    return x * 10 ** ((target - rms_db(x)) / 20)


def box(x, n):
    c = np.concatenate([[0.0], np.cumsum(x, dtype=np.float64)])
    i = np.arange(len(x))
    lo, hi = np.clip(i - n // 2, 0, len(x)), np.clip(i - n // 2 + n, 0, len(x))
    return ((c[hi] - c[lo]) / n).astype(np.float32)


def T(k, x):
    s = SH[k]
    return s["start"] + (x if x >= 0 else s["dur"] + x)


def F(k, i=0, j=0):
    return SH[k]["vo"][i]["t"] + SH[k]["vo"][i]["frags"][j]


def C(k, i=0, j=0):
    return max(0.0, F(k, i, j) - 0.1)


D = {k: SH[k]["dur"] for k in SH}

# ---- voice ----
vo = np.zeros(N, np.float32)
for s in SC["shots"]:
    for v in s["vo"]:
        x = load(os.path.join(HERE, "vo", f"{v['id']}.wav"))
        place(vo, level(x, -18 + (1.5 if v["id"].startswith(("q", "r")) else 0)), s["start"] + v["t"])


# ---- effects from the shared synth (cues: shot, seconds into it, kind, gain) ----
def fire(k, a, b, g=0.22, step=2.2):
    return [(k, a + i * step, "crackle", g) for i in range(int(max(0, b - a - 0.4) / step) + 1)]


def beats(k, a, b, g=0.24, period=0.5):
    return [(k, a + i * period, "heartbeat", g) for i in range(int(max(0, b - a - 0.1) / period) + 1)]


def surf(k, g=0.12):
    return [(k, 0.0, "stream", g)] + ([(k, 4.5, "stream", g)] if D[k] > 5 else [])


CUES = [
    *surf("hook", 0.14), *fire("hook", 0.0, D["hook"], 0.06), *surf("cmd", 0.12),
    ("why", 0.0, "flap", 0.1), ("why", C("why", 0, 2), "engine", 0.12), ("wreck", 0.0, "engine", 0.1), ("wreck", C("wreck", 0, 1), "rustle", 0.26),
    ("bottle", 0.1, "plop", 0.16), ("bottle", 0.6, "plop", 0.12), *surf("bottle", 0.08),
    ("sun", 0.0, "tinnitus", 0.08), *surf("sun", 0.08),
    ("empty1", 0.85, "drip", 0.34), *surf("empty1", 0.06),
    ("thirst", 0.05, "pant", 0.2), ("thirst", C("thirst", 0, 1) + 0.4, "splash", 0.16), *surf("thirst", 0.12),
    ("nosea", 0.0, "splash", 0.1), *beats("nosea", 0.05, D["nosea"], 0.3, 0.42),
    ("salt", 0.15, "stream", 0.14), ("salt", C("salt", 0, 1) + 0.2, "stream", 0.18), ("salt", C("salt", 0, 1) + 0.4, "stream", 0.18),
    ("salt", C("salt", 0, 1) + 0.8, "drip", 0.24), ("salt", C("salt", 0, 1) + 1.1, "drip", 0.2), ("salt", C("salt", 0, 2) + 0.1, "ching", 0.1),
    ("look", 0.1, "rustle", 0.2), ("look", 0.6, "flap", 0.1), *surf("look", 0.08),
    ("coco", 0.1, "thud", 0.36), ("coco", 0.5, "clang", 0.26), ("coco", 0.75, "plop", 0.18), ("coco", C("coco", 0, 2) + 0.3, "thud", 0.24),
    *surf("onetree", 0.12), ("onetree", 0.3, "flap", 0.1),
    ("rain", 0.0, "rain", 0.3), ("rain", 4.0, "rain", 0.3), *[("rain", 0.4 + i * 0.55, "drip", 0.2) for i in range(int(D["rain"] / 0.55))],
    ("vest", 0.1, "rustle", 0.24), ("vest", C("vest", 0, 2), "click", 0.24), ("vest", 0.0, "rain", 0.16),
    *fire("glow", 0.0, D["glow"], 0.06), *beats("glow", 0.2, D["glow"], 0.22, 0.6),
    ("q1", 0.1, "rustle", 0.16),
    *[("lure", 0.3 + i * 0.5, "steps", 0.18) for i in range(int(D["lure"] / 0.5))], *surf("lure", 0.12),
    ("dont", 0.04, "scrape", 0.36), ("dont", 0.1, "debris", 0.26), *beats("dont", 0.0, D["dont"], 0.32, 0.4),
    ("q2", 0.2, "rustle", 0.14),
    *surf("tide", 0.1), ("tide", 0.5, "squelch", 0.14), ("tide", C("tide", 0, 2), "rustle", 0.24),
    ("nofruit", 0.0, "rustle", 0.2), *beats("nofruit", 0.05, D["nofruit"], 0.28, 0.42),
    ("shell", 0.3, "scrape", 0.3), ("shell", 0.7, "click", 0.24), *surf("shell", 0.08),
    *fire("cook", 0.0, D["cook"], 0.3), ("cook", 0.2, "hiss", 0.12),
    ("fire", 0.35, "click", 0.32), ("fire", 0.45, "strike", 0.2), ("fire", C("fire", 0, 1), "whoosh", 0.16), *fire("fire", C("fire", 0, 1), D["fire"], 0.26),
    *fire("rotor", 0.0, D["rotor"], 0.2),
    *fire("leaves", 0.0, D["leaves"], 0.26), ("leaves", 0.3, "rustle", 0.3), ("leaves", 0.7, "hiss", 0.2),
    ("bright", 0.1, "rustle", 0.26), ("flash", 0.3, "ching", 0.14), ("flash", 0.7, "ching", 0.1),
    ("found", 0.0, "pant", 0.14), ("saved", 0.0, "pant", 0.2),
    ("empty", 0.0, "steps", 0.2), ("empty", C("empty", 0, 1), "tinnitus", 0.08),
    *surf("twist", 0.1), *fire("twist", C("twist", 0, 2), D["twist"], 0.08),
    *[("walk", 0.2 + i * 0.55, "steps", 0.12) for i in range(int(D["walk"] / 0.55))],
    *surf("lost", 0.1), ("lost", 0.4, "flap", 0.08), ("end", 0.1, "rustle", 0.2),
]
CUES = [c for c in CUES if c[3] > 0 and c[2] not in ("wind", "lap", "pop", "tick")]
cues = {"duration": TOTAL, "sections": [{"start": 0, "end": TOTAL, "mood": "silence"}],
        "sfx": [{"t": round(T(k, x), 3), "type": typ, "gain": g} for k, x, typ, g in CUES]}
json.dump(cues, open(os.path.join(HERE, "sfx_cues.json"), "w"))
subprocess.run(["python3", os.path.join(HERE, "..", "prod1", "synth.py"), os.path.join(HERE, "sfx_cues.json"), os.path.join(HERE, "sfx.wav")],
               check=True, env={**os.environ, "STEMS": "1"})
sfx = load(os.path.join(HERE, "sfx_sfx.wav"))[:N]
sfx = np.pad(sfx, (0, N - len(sfx)))

# ---- the helicopter: blade slap (~11 Hz thumps of low noise) + turbine whine, with a distance envelope per pass ----
rng = np.random.default_rng(7)


def rotor(dur, near):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    noise = rng.standard_normal(n).astype(np.float32)
    low = box(box(noise, 40), 40) * 6
    slap = (0.5 + 0.5 * np.cos(2 * np.pi * 11 * tt)) ** 6
    whine = 0.08 * np.sin(2 * np.pi * (520 + 30 * np.sin(tt * 0.7)) * tt)
    return (low * slap + whine * near).astype(np.float32)


heli = np.zeros(N, np.float32)
for k, a, b, shape in [("rotor", 0.0, -0.01, "in"), ("q3", 0.0, -0.01, "near"), ("pass", 0.0, -0.01, "pass"), ("under", 0.0, 1.2, "out"),
                       ("back", 0.0, -0.01, "in"), ("found", 0.0, -0.01, "near"), ("saved", 0.0, -0.01, "near")]:
    t0, t1 = T(k, a), T(k, b)
    x = rotor(t1 - t0, 1.0)
    u = np.linspace(0, 1, len(x))
    env = {"in": 0.2 + 0.8 * u, "near": np.ones_like(u), "pass": np.clip(1.4 - 1.3 * u, 0.1, 1), "out": 0.3 * (1 - u)}[shape]
    place(heli, x * env.astype(np.float32), t0)

# ---- music: the plane theme (as EP.1), its peak on the twist; silent at the hush, bass cut after, fades over the end card ----
mus = load(os.path.join(HERE, "..", "plane-theme.mp3"))
mus = mus[int(max(0.0, len(mus) / SR - TOTAL - 1.0) * SR):]
while len(mus) < N:
    mus = np.concatenate([mus, mus])
mus = mus[:N]
gain = np.ones(N, np.float32)


def dip(t0, t1, lvl, ramp=0.25):
    a = np.clip((t - (t0 - ramp)) / ramp, 0, 1) * np.clip(((t1 + ramp) - t) / ramp, 0, 1)
    np.minimum(gain, 1 - (1 - lvl) * a, out=gain)


for k in ("nosea", "nofruit", "dont"):   # the red cards: the bed drops away so the command lands
    dip(T(k, 0), T(k, -0.01), 0.35, ramp=0.1)
mus = mus * gain
a0 = int(T("hush", 0) * SR)
seg = mus[a0:].astype(np.float64)
Fq = np.fft.rfft(seg)
fq = np.fft.rfftfreq(len(seg), 1 / SR)
Fq *= np.clip((fq - 150) / 250, 0, 1)
mus[a0:] = np.fft.irfft(Fq, len(seg)).astype(np.float32)
a, b = int(T("end", 0) * SR), int(T("end", -0.01) * SR)
mus[a:b] *= np.linspace(1, 0, b - a)
mus[b:] = 0

# ---- levels, ducking, the hush ----
mus = level(mus, -33)
sfx = level(sfx, -27)
heli = level(heli, -26)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.8 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mix = vo + mus * duck + sfx * (0.6 + 0.4 * duck) + heli * (0.5 + 0.5 * duck)
h0, h1 = T("hush", 0), T("hush", -0.01)
mix *= 1 - np.clip((t - (h0 - 0.12)) / 0.12, 0, 1) * np.clip(((h1 + 0.02) - t) / 0.02, 0, 1)
peak = np.max(np.abs(mix))
if peak > 0.98:
    mix = np.tanh(mix / peak * 1.2) * 0.95
out = os.path.join(HERE, "mix_raw.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", out],
               input=mix.astype(np.float32).tobytes(), check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", "loudnorm=I=-13.7:TP=-1.5:LRA=11", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)
print("mix written", TOTAL)

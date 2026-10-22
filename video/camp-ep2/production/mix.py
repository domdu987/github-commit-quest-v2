"""Build the episode soundtrack from schedule.json: per-line levelled voice, synthesized forest/camp SFX
and the Suno music bed with dips before the scares and sidechain ducking under the voice. Output -14 LUFS."""
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


# ---- voice: every line levelled on its own so whispers and screams sit at a readable loudness ----
LINE_GAIN = {"d00": -3, "d03": -3, "d11": -2, "d06": -1}  # the thing in the forest stays a little distant
vo = np.zeros(N, np.float32)
for s in SC["shots"]:
    for v in s["vo"]:
        x = load(os.path.join(HERE, "vo", f"{v['id']}.wav"))
        place(vo, level(x, -18 + LINE_GAIN.get(v["id"], 0)), s["start"] + v["t"])

# ---- sfx cues: (shot, t from shot start (negative = from its end), type, gain) ----
D = {k: SH[k]["dur"] for k in SH}


def beats(k, t0, dur, period, g=0.9):  # heartbeat sfx in step with Fx.heart
    return [(k, t0 + i * period, "heartbeat", g) for i in range(int((dur - 0.1) / period) + 1)]


def ticks(k, t0, t1, step, g=0.5):
    n = int((t1 - t0) / step)
    return [(k, t0 + i * step, "tick", g) for i in range(n)]


pick = vo_t("open") + SH["open"]["vo"][0]["dur"] + 0.15
V = lambda i: vo_t("voices", i)
VE = lambda i: V(i) + SH["voices"]["vo"][i]["dur"]
H = lambda i: vo_t("herd", i)
DV = lambda i: vo_t("door", i)
pick4 = VE(4) + 0.5
strike = 0.95
CUES = [
    ("open", 0.0, "wind", 0.5), ("open", 0.2, "glitch", 0.7), *beats("open", 0.0, D["open"], 0.36, 0.9), ("open", pick - 0.25, "glitch", 0.8),
    ("open", pick, "sting", 1.2), ("open", pick, "boom", 0.6), ("open", pick + 0.4, "whoosh", 1.0), ("open", pick + 0.5, "rustle", 0.9), *ticks("open", 0.15, pick, 0.5, 1.0),
    ("chase", 0.0, "rustle", 1.0), ("chase", 1.2, "rustle", 1.0), ("chase", 2.4, "rustle", 1.0), ("chase", 3.6, "rustle", 0.9), *beats("chase", 0.0, D["chase"], 0.36, 0.9),
    ("chase", vo_t("chase"), "glitch", 0.5), *[("chase", 0.3 + k * 0.28, "snap", 0.35) for k in range(14)],
    ("fall", 0.4, "whoosh", 1.0), ("fall", 0.7, "boom", 0.7), ("fall", 0.75, "snap", 1.0), ("fall", 0.8, "rustle", 1.0), ("fall", 1.3, "crickets", 0.5), ("fall", 1.5, "swell", 0.45),
    *[("fall", 1.6 + k * 0.6, "buzz", 0.3) for k in range(4)],
    ("voices", 0.0, "crickets", 0.5), *beats("voices", 0.0, D["voices"], 0.55, 0.8), ("voices", V(1), "glitch", 0.5), ("voices", V(4), "glitch", 0.8), ("voices", V(4), "sting", 1.0),
    *[("voices", VE(1) + 0.3 + k, "tick", 0.9) for k in range(int(pick4 - VE(1) - 0.3))], ("voices", pick4, "ding", 0.7), ("voices", pick4 + 0.4, "notif", 0.45),
    ("reunite", 0.0, "rustle", 0.7), ("reunite", 1.1, "swell", 0.5), ("reunite", 1.1, "notif", 0.4),
    ("map", 0.0, "whoosh", 1.0), ("map", 0.05, "riser", 0.5), ("map", 2.4, "ding", 0.5), *ticks("map", 2.4, 4.2, 0.12, 0.35), ("map", 4.2, "pop", 0.6),
    *[("herd", 0.3 + k * 0.8, "stomp", 0.9 - min(k, 8) * 0.05) for k in range(19)], ("herd", 0.6, "trumpet", 0.7), *beats("herd", 2.9, H(1) - 3.0, 0.5, 0.9),
    ("herd", H(1) - 0.7, "ding", 0.5), ("herd", H(1) + 0.1, "notif", 0.35), ("herd", H(2) - 0.1, "trumpet", 1.4), ("herd", H(2), "boom", 0.6), ("herd", H(2) + 0.5, "whoosh", 0.8),
    ("bite", 0.0, "rustle", 0.7), ("bite", 0.3, "hiss", 0.9), ("bite", strike, "boom", 0.55), ("bite", strike, "sting", 1.0), *beats("bite", strike, D["bite"] - strike, 0.45, 0.9),
    ("aid", 0.0, "crickets", 0.5), ("aid", 0.35, "notif", 0.35), ("aid", 2.6, "rustle", 0.6), ("aid", vo_t("aid", 1), "notif", 0.35), ("aid", vo_t("aid", 2) + 0.2, "notif", 0.4),
    ("hut", 0.0, "crickets", 0.5), ("hut", 0.0, "rustle", 0.5), ("hut", 1.0, "ding", 0.6), ("hut", 1.0, "swell", 0.5),
    ("door", 0.0, "crickets", 0.3), ("door", 0.3, "knock", 1.3), ("door", DV(0) - 0.3, "static", 1.0), ("door", DV(0) + 1.4, "static", 0.6), ("door", DV(0), "glitch", 0.6),
    ("door", DV(1), "sting", 1.2), ("door", DV(1), "boom", 0.6), *beats("door", DV(0), D["door"] - DV(0) - 0.3, 0.42, 1.0),
    *[("door", DV(1) + 1.3 + k * 0.5, "tick", 1.1) for k in range(int((D["door"] - DV(1) - 1.6) / 0.5))], ("door", D["door"] - 2.3, "riser", 1.0),
]
cues = {"duration": TOTAL, "sections": [{"start": 0, "end": TOTAL, "mood": "silence"}],
        "sfx": [{"t": round(T(k, t), 3), "type": typ, "gain": g} for k, t, typ, g in CUES]}
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


dip(0.0, pick - 0.05, 0.3)                                         # the pull of the choice
dip(T("voices", 0.0), T("voices", -0.2), 0.2)                      # two voices in the dark
dip(T("herd", 2.6), T("herd", H(1)), 0.05)                         # silence while the herd passes
dip(T("bite", 0.3), T("bite", strike + 0.1), 0.05)
dip(T("door", 0.0), T("door", -0.3), 0.3)
mus = mus * gain
fade = int(1.2 * SR)
end = int(T("door", -0.22) * SR)
mus[end - fade:end] *= np.linspace(1, 0.25, fade)
mus[end:] = 0  # hard cut to black and silence

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
k = int(0.25 * SR)
duck = box(duck, k)
mix = vo + mus * duck + sfx
cut = int(T("door", -0.22) * SR)  # the episode ends on a hard cut to black and silence
mix[cut - 240:cut] *= np.linspace(1, 0, 240)
mix[cut:] = 0
peak = np.max(np.abs(mix))
if peak > 0.98:
    mix = np.tanh(mix / peak * 1.2) * 0.95
out = os.path.join(HERE, "mix_raw.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", out],
               input=mix.astype(np.float32).tobytes(), check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)
print("mix written", TOTAL)

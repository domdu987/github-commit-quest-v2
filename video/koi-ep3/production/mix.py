"""Build the episode soundtrack from schedule.json: per-line levelled voice, synthesized rainforest SFX
(stream, stick taps, fire, a synthesized helicopter, the ward monitor) and the Suno music bed with dips before the scares and
sidechain ducking under the voice. Output -14 LUFS, hard cut to silence at the end."""
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
LINE_GAIN = {"k01": -2, "d03": -1, "d02": 0}
vo = np.zeros(N, np.float32)
for s in SC["shots"]:
    for v in s["vo"]:
        x = load(os.path.join(HERE, "vo", f"{v['id']}.wav"))
        place(vo, level(x, -18 + LINE_GAIN.get(v["id"], 0)), s["start"] + v["t"])

# ---- sfx cues: (shot, t from shot start (negative = from its end), type, gain) ----
D = {k: SH[k]["dur"] for k in SH}


def beats(k, t0, dur, period, g=0.9):  # heartbeat sfx in step with Fx.heart
    return [(k, t0 + i * period, "heartbeat", g) for i in range(int((dur - 0.1) / period) + 1)]


def bed(kind, a, b, g, step=4.6):  # overlapping 6 s copies of an ambience between absolute times a and b
    out, t = [], a - 0.6
    while t < b - 1.0:
        out.append((None, t, kind, g))
        t += step
    return out


HK = frag("hook", 0, 2) - 0.05
walk_taps = [t for t in np.arange(0.1, D["walk"] - 0.2, 0.48)]
w0 = vo_t("lure", 1)
lure_taps = [t for t in np.arange(w0 + 0.3, D["lure"] - 0.8, 0.8)]
_a, _b = frag("sig", 0, 0), frag("sig", 0, 1) + 0.15  # ticks on the checklist, as spread by Sig.ui in sig.js
SIG_TICKS = [_a + 0.3 + (_b - _a - 0.3) * i / (3 - 1) for i in range(3)] if 3 > 1 else [_b]
CUES = [
    *bed("stream", 0.0, T("hook", -0.1), 0.7, 3.0), *beats("hook", 0.6, D["hook"] - 0.6, 0.6, 0.6), ("hook", frag("hook", 0, 1), "rustle", 0.4),
    ("hook", HK, "whoosh", 0.6), ("hook", vo_t("hook", 1), "sting", 0.9), ("hook", vo_t("hook", 1), "boom", 0.6), ("hook", vo_t("hook", 1), "glitch", 0.6), ("hook", -0.25, "whoosh", 0.8),
    ("rewind", 0.0, "rewind", 1.0), ("rewind", 0.05, "glitch", 0.5), ("rewind", 1.2, "pop", 0.5),
    *bed("wind", T("up", 0), T("mad", -0.1), 0.35, 5.0), ("up", frag("up", 0, 1), "sting", 0.5), *beats("up", frag("up", 0, 1), D["up"] - frag("up", 0, 1), 0.55, 0.5),
    ("up", frag("up", 1, 1) + 0.75, "drip", 1.0),
    ("mad", 0.1, "rustle", 0.4), ("mad", frag("mad", 0, 1), "sting", 0.6), ("mad", vo_t("mad") + 0.05, "knock", 0.5),
    *[("walk", t, "knock", 0.55) for t in walk_taps], *[("walk", 0.05 + k * 0.48, "rustle", 0.25) for k in range(8)], ("walk", frag("walk", 0, 1), "swell", 0.4),
    *bed("stream", T("cross", 0), T("depth", -0.1), 0.8, 3.0), ("cross", vo_t("cross", 1) - 0.1, "whoosh", 0.6), ("cross", vo_t("cross", 1), "boom", 0.6), ("cross", vo_t("cross", 1), "sting", 0.6),
    ("depth", frag("depth", 0, 1) + 0.15, "beep", 0.7), ("depth", frag("depth", 1, 1) - 0.1, "whoosh", 0.9), ("depth", frag("depth", 1, 1) + 0.1, "roar", 0.7),
    ("depth", frag("depth", 1, 1) + 0.2, "boom", 0.6), ("depth", frag("depth", 1, 1) + 0.2, "sting", 0.8), ("depth", vo_t("depth", 1) + 0.1, "pop", 0.5),
    ("detour", frag("detour", 0, 0) + 0.3, "pop", 0.6), *[("detour", frag("detour", 0, 1) + i * 0.09, "tick", 0.35) for i in range(14)], ("detour", frag("detour", 0, 2), "ding", 0.6),
    ("thirst", 0.1, "rustle", 0.6), ("thirst", 0.6, "rustle", 0.5), ("thirst", 1.1, "drip", 0.6), *bed("stream", T("thirst", frag("thirst", 0, 1)), T("thirst", -0.1), 0.5, 3.0),
    ("thirst", frag("thirst", 0, 1) + 0.1, "squelch", 0.6),
    *bed("crackle", T("boil", 0), T("boil", -0.1), 0.9, 2.5), ("boil", 0.0, "hiss", 0.5), ("boil", frag("boil", 0, 1), "hiss", 0.7),
    *[("boil", frag("boil", 0, 1) + 0.1 + k * 0.11, "tick", 0.3) for k in range(12)], ("boil", frag("boil", 0, 1) + 1.45, "ding", 0.7),
    ("heli", frag("heli", 0, 1), "swell", 0.5), ("heli", vo_t("heli", 1), "whoosh", 0.4), ("heli", vo_t("heli", 1) + 0.1, "beep", 0.6), ("heli", frag("heli", 1, 1), "sting", 0.7),
    *bed("wind", T("clearing", 0), T("vx", -0.1), 0.35, 5.0), *[("clearing", 0.05 + k * 0.2, "stomp", 0.25) for k in range(5)], ("clearing", frag("clearing", 0, 1), "swell", 0.5),
    ("vx", frag("vx", 0, 0) + 0.3, "swell", 0.5), ("vx", frag("vx", 0, 0) + 0.5, "pop", 0.6), ("vx", frag("vx", 0, 1), "pop", 0.6), ("vx", vo_t("vx", 1) + 0.1, "whoosh", 0.5), ("vx", frag("vx", 1, 1), "ding", 0.6),
    *[("prints", frag("prints", 0, 1) - 0.1 + i * 0.035 * 3, "tick", 0.3) for i in range(10)], ("prints", frag("prints", 0, 1), "sting", 1.0), ("prints", frag("prints", 0, 1), "boom", 0.6),
    ("prints", frag("prints", 0, 1), "glitch", 0.6), *beats("prints", frag("prints", 0, 1), D["prints"] - frag("prints", 0, 1), 0.45, 0.7),
    *bed("wind", T("lure", 0), T("lure", -0.1), 0.3, 5.0), *[("lure", t, "knock", 0.5 * (1 - (t - w0) / (D["lure"] - w0)) + 0.1) for t in lure_taps],
    *beats("tracks", 0.0, D["tracks"], 0.5, 0.7), ("tracks", frag("tracks", 0, 1), "sting", 1.0), ("tracks", frag("tracks", 0, 1), "glitch", 0.6),
    ("rescue", frag("rescue", 0, 1) - 0.1, "beep", 1.0), ("rescue", frag("rescue", 0, 1), "riser", 0.5),
    ("sig", 0.05, "glitch", 0.35), ("sig", 0.05, "beep", 0.35), *[("sig", t, "ding", 0.6) for t in SIG_TICKS],
    ("sig", frag("sig", 0, 2), "glitch", 0.45), *beats("sig", frag("sig", 0, 2), frag("sig", 0, 3) - frag("sig", 0, 2), 0.38, 0.8),
    *[("sig", frag("sig", 0, 2) + o, "tick", 0.55 + 0.1 * k) for k, o in enumerate((0.1, 0.42, 0.68, 0.88, 1.02, 1.12))],  # ticking that speeds up into the cross
    ("sig", frag("sig", 0, 3) - 1.1, "riser", 0.6),
    ("sig", frag("sig", 0, 3), "sting", 1.1), ("sig", frag("sig", 0, 3), "boom", 0.8), ("sig", frag("sig", 0, 3), "glitch", 0.7), ("sig", frag("sig", 0, 3) + 0.12, "slam", 0.7),
    *beats("sig", frag("sig", 0, 3), D["sig"] - frag("sig", 0, 3), 0.5, 0.7),
    *[(None, t, "beep", 0.22) for t in np.arange(T("hosp", 0.4), T("mud", -0.1), 1.05)], ("hosp", 0.2, "swell", 0.4),
    ("gone", frag("gone", 0, 1) + 0.55, "boom", 0.9), ("gone", frag("gone", 0, 1) + 0.55, "knock", 0.8), *beats("gone", frag("gone", 0, 1), D["gone"] - frag("gone", 0, 1), 0.55, 0.5),
    ("stick", frag("stick", 0, 1), "sting", 0.8), *beats("stick", 0.0, D["stick"], 0.55, 0.6),
    *beats("mud", 0.0, D["mud"], 0.45, 0.8), ("mud", frag("mud", 0, 1), "sting", 1.0), ("mud", frag("mud", 0, 1), "glitch", 0.6),
    *beats("bed", 0.0, D["bed"], 0.38, 0.9), ("bed", vo_t("bed") - 0.15, "creak", 0.5),
    *beats("choice", 0.0, D["choice"] - 0.3, 0.38, 1.0), *[("choice", 0.05 + k * 1.0, "tick", 1.0) for k in range(3)], ("choice", 1.0, "glitch", 0.6),
    ("choice", D["choice"] - 2.2, "riser", 1.0), ("choice", D["choice"] - 0.62, "creak", 1.0), ("choice", D["choice"] - 0.6, "glitch", 0.8), ("choice", D["choice"] - 0.6, "boom", 0.7),
]
cues = {"duration": TOTAL, "sections": [{"start": 0, "end": TOTAL, "mood": "silence"}],
        "sfx": [{"t": round(t if k is None else T(k, t), 3), "type": typ, "gain": g} for k, t, typ, g in CUES]}
json.dump(cues, open(os.path.join(HERE, "sfx_cues.json"), "w"))
subprocess.run(["python3", os.path.join(HERE, "..", "synth.py"), os.path.join(HERE, "sfx_cues.json"), os.path.join(HERE, "sfx.wav")],
               check=True, env={**os.environ, "STEMS": "1"})
sfx = load(os.path.join(HERE, "sfx_sfx.wav"))[:N]
sfx = np.pad(sfx, (0, N - len(sfx)))


def heli(dur, g):  # chopped low noise + rotor thump at ~11 Hz
    n = int(dur * SR)
    tt = np.arange(n) / SR
    noise = np.random.default_rng(3).standard_normal(n).astype(np.float32)
    lp = box(box(noise, int(SR / 300)), int(SR / 600))
    ph = np.clip(np.sin(2 * np.pi * 11 * tt), 0, 1)
    x = lp * (0.35 + 0.65 * ph ** 3) * 6 + 0.6 * np.sin(2 * np.pi * 58 * tt) * ph ** 8
    env = np.minimum(1, tt / 0.8) * np.minimum(1, (dur - tt) / 0.4)
    return (x * env * g).astype(np.float32)


HEL = vo_t("heli", 1) - 0.05
place(sfx, heli(HEL, 0.5) * np.linspace(0.4, 1.0, int(HEL * SR)).astype(np.float32), T("heli", 0))
place(sfx, heli(D["heli"] - HEL, 0.35), T("heli", HEL))
place(sfx, heli(D["rescue"], 0.7), T("rescue", 0))

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


dip(0.0, T("hook", -0.1), 0.15, 0.05)                    # the cold open sits on the stream and a heartbeat
dip(T("up", 0), T("mad", -0.1), 0.4)
dip(T("depth", frag("depth", 1, 1) - 0.1), T("depth", -0.1), 0.3)
dip(T("heli", 0), T("heli", -0.1), 0.45)
dip(T("prints", frag("prints", 0, 1)), T("prints", -0.1), 0.3)
dip(T("lure", 0), T("lure", -0.1), 0.3)
dip(T("tracks", 0), T("tracks", -0.05), 0.0, 0.1)          # silence: one foot
dip(T("rescue", 0), T("rescue", -0.1), 0.5)
dip(T("sig", frag("sig", 0, 2)), T("sig", frag("sig", 0, 3) + 0.05), 0.05, 0.12)  # silence before "ข้อเดียว"
dip(T("gone", 0), T("gone", -0.1), 0.4)
dip(T("stick", 0), T("mud", -0.1), 0.25)
dip(T("bed", 0), T("bed", -0.05), 0.0, 0.1)               # silence, then the whisper
dip(T("choice", 0), T("choice", -0.3), 0.5)
mus = mus * gain
end = int(T("choice", -0.2) * SR)
mus[end:] = 0  # hard cut to black and silence

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mix = vo + mus * duck + sfx
cut = int(T("choice", -0.2) * SR)
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

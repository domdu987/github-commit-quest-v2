"""Build the episode soundtrack from schedule.json: per-line levelled voice, synthesized rainforest SFX
(tap water, knocks, a muffled scream, the infected growling, stairwell footsteps) and the Suno music bed with dips before the scares and
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
LINE_GAIN = {"d02": -1, "d04": 1, "d07": 0, "d08": -1}
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


CUES = [
    *bed("tap", 0.0, T("hook", -0.1), 0.8, 2.4), *beats("hook", 0.3, D["hook"] - 0.3, 0.6, 0.6), ("hook", frag("hook", 0, 1), "sting", 0.5),
    ("hook", vo_t("hook", 1) - 0.4, "whoosh", 0.5), ("hook", vo_t("hook", 1), "sting", 0.9), ("hook", vo_t("hook", 1), "boom", 0.6), ("hook", vo_t("hook", 1), "glitch", 0.6), ("hook", -0.25, "whoosh", 0.8),
    ("rewind", 0.0, "rewind", 1.0), ("rewind", 0.05, "glitch", 0.5), ("rewind", 1.2, "pop", 0.5),
    *[("news", frag("news", 0, j) + (0.1 if j == 0 else 0), "notif", 0.7) for j in range(3)], ("news", frag("news", 0, 1), "sting", 0.4),
    ("fake", vo_t("fake") - 0.05, "pop", 0.3),
    ("scream", frag("scream", 0, 1) - 0.15, "scream", 1.0), ("scream", frag("scream", 0, 1), "sting", 0.7), *[("scream", frag("scream", 0, 2) + k * 0.15, "knock", 0.9) for k in range(4)],
    *beats("scream", frag("scream", 0, 1), D["scream"] - frag("scream", 0, 1), 0.45, 0.6),
    *beats("peep", 0.0, D["peep"], 0.6, 0.6), ("peep", 0.4, "growl", 0.5), ("peep", frag("peep", 0, 1), "sting", 0.6),
    ("turn", 0.3, "growl", 0.6), ("turn", frag("turn", 0, 1) - 0.05, "growl", 1.2), ("turn", frag("turn", 0, 1) - 0.05, "boom", 0.8), ("turn", frag("turn", 0, 1) - 0.05, "sting", 1.0), ("turn", frag("turn", 0, 1) - 0.05, "glitch", 0.8),
    *[("knock", 0.05 + k * 0.2, "knock", 1.0) for k in range(3)], *[("knock", vo_t("knock") + 0.4 + k * 0.18, "knock", 0.9) for k in range(3)], *beats("knock", 0.0, D["knock"], 0.42, 0.7),
    ("jit", 0.0, "rustle", 0.6), ("jit", 0.82, "slam", 1.0), ("jit", frag("jit", 0, 0) + 0.15, "pop", 0.4),
    ("rule", 0.1, "swell", 0.4), *[("rule", t, "pop", 0.5) for t in (vo_t("rule", 1), frag("rule", 1, 1) - 0.05, frag("rule", 1, 2) - 0.05)], ("rule", frag("rule", 1, 2) + 0.15, "knock", 0.5),
    ("water", 0.2, "hum", 0.4), ("water", frag("water", 1, 1), "buzz", 0.5), ("water", frag("water", 1, 1), "boom", 0.5), ("water", frag("water", 1, 1), "sting", 0.6),
    *[("litres", t, "pop", 0.45) for t in (frag("litres", 0, 0), vo_t("litres", 1))], *[("litres", frag("litres", 0, 2) + i * 0.12, "tick", 0.4) for i in range(4)],
    *bed("tap", T("fill", 0), T("stop", frag("stop", 0, 1)), 0.9, 2.4), *[("fill", 0.2 + k * 0.5, "tick", 0.2) for k in range(6)],
    ("stop", frag("stop", 0, 1) - 0.5, "sputter", 1.0), ("stop", frag("stop", 0, 1) + 0.3, "drip", 0.8), ("stop", frag("stop", 0, 2), "sting", 0.7), ("stop", frag("stop", 0, 2), "beep", 0.6),
    ("boss", 0.2, "rustle", 0.5),
    *[("stairs", 0.2 + k * 0.45, "stomp", 0.35) for k in range(7)], ("stairs", frag("stairs", 0, 2), "swell", 0.4),
    *[("floor19", 0.1 + k * 0.45, "stomp", 0.3) for k in range(2)], ("floor19", frag("floor19", 0, 1) - 0.05, "growl", 1.0), ("floor19", frag("floor19", 0, 1), "sting", 0.9), ("floor19", frag("floor19", 0, 1), "boom", 0.5),
    ("bite", 0.0, "growl", 1.3), ("bite", 0.3, "scream", 0.8), ("bite", 0.35, "boom", 0.8), ("bite", 0.35, "glitch", 0.8), ("bite", 0.35, "squish", 0.8),
    *bed("tap", T("wash", 0), T("real", -0.1), 0.6, 2.4), ("wash", frag("wash", 0, 2) - 0.1, "pop", 0.5), *[("wash", frag("wash", 0, 2) + 0.2 + k * 0.1, "tick", 0.3) for k in range(12)], ("wash", frag("wash", 0, 2) + 1.55, "ding", 0.6),
    ("real", frag("real", 0, 1) - 0.1, "pop", 0.5), ("real", frag("real", 1, 1) - 0.1, "ding", 0.6),
    ("hosp", 0.1, "siren", 0.25), ("hosp", frag("hosp", 0, 2) - 0.05, "notif", 0.7), ("hosp", frag("hosp", 0, 2), "sting", 0.6),
    ("door", 0.1, "knock", 0.5), *beats("door", 0.0, D["door"], 0.5, 0.5),
    ("sleeve", frag("sleeve", 0, 1), "rustle", 0.8), *beats("sleeve", 0.0, D["sleeve"], 0.55, 0.5),
    ("sig", frag("sig", 0, 0) + 0.35, "ding", 0.6), ("sig", frag("sig", 0, 0) + 0.85, "ding", 0.6), ("sig", frag("sig", 0, 1) + 0.25, "ding", 0.6),
    ("sig", frag("sig", 0, 3), "sting", 1.1), ("sig", frag("sig", 0, 3), "boom", 0.7), ("sig", frag("sig", 0, 3), "glitch", 0.6),
    *beats("sig", frag("sig", 0, 3), D["sig"] - frag("sig", 0, 3), 0.5, 0.7),
    *bed("crickets", T("night", 0), T("choice", -0.3), 0.25, 5.0), ("night", frag("night", 0, 1), "swell", 0.4),
    ("scar", frag("scar", 0, 1), "sting", 1.0), ("scar", frag("scar", 0, 1), "glitch", 0.6), *beats("scar", 0.0, D["scar"], 0.5, 0.7),
    *beats("choice", 0.0, D["choice"] - 0.3, 0.38, 1.0), *[("choice", 0.05 + k * 1.0, "tick", 1.0) for k in range(3)], ("choice", 1.0, "glitch", 0.6),
    ("choice", D["choice"] - 2.2, "riser", 1.0), ("choice", D["choice"] - 0.62, "sting", 1.0), ("choice", D["choice"] - 0.6, "glitch", 0.8), ("choice", D["choice"] - 0.6, "boom", 0.7),
]
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


dip(0.0, T("hook", -0.1), 0.15, 0.05)                    # the cold open sits on the tap and a heartbeat
dip(T("scream", 0), T("knock", -0.1), 0.3)
dip(T("turn", frag("turn", 0, 1) - 0.1), T("knock", -0.1), 0.0, 0.05)  # silence after the jump scare, through the knocks
dip(T("rule", 0), T("rule", -0.1), 0.35)
dip(T("floor19", 0), T("bite", -0.1), 0.3)
dip(T("door", 0), T("sleeve", -0.1), 0.35)
dip(T("sig", frag("sig", 0, 2)), T("sig", frag("sig", 0, 3) + 0.05), 0.05, 0.12)  # silence before "เรื่องเดียว"
dip(T("night", 0), T("scar", -0.05), 0.25)
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

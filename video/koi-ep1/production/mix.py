"""Build the episode soundtrack from schedule.json: per-line levelled voice, synthesized rainforest SFX
(rain, stream, flood, crickets, puppet gong) and the Suno music bed with dips before the scares and
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
LINE_GAIN = {"k01": -2, "k02": -3, "d10": -1, "d08": -1}
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


hops = [0.2 + j * (D["sleep"] - 0.2) / 6 for j in range(1, 7)]
CUES = [
    *bed("rain", 0.0, T("hook", -0.1), 0.25), *beats("hook", 0.6, D["hook"] - 0.6, 0.6, 0.8), ("hook", frag("hook", 0, 2), "sting", 0.7),
    ("hook", vo_t("hook", 1) - 0.2, "rustle", 0.6), ("hook", vo_t("hook", 1) + 0.7, "glitch", 0.6), ("hook", -0.25, "whoosh", 0.8),
    ("rewind", 0.0, "rewind", 1.0), ("rewind", 0.05, "glitch", 0.5), ("rewind", 1.2, "pop", 0.5),
    *bed("rain", T("canopy", 0), T("rule", -0.2), 0.55), ("canopy", 0.4, "thunder", 0.45), ("canopy", 0.0, "wind", 0.4),
    ("vlog", 0.0, "beep", 1.0), ("vlog", 0.3, "rustle", 0.4),
    ("leg", 0.15, "squish", 0.9), ("leg", 0.55, "squish", 0.7), ("leg", frag("leg", 0, 1), "pop", 0.6),
    ("guide", 0.2, "squelch", 0.5), ("guide", 0.8, "squelch", 0.45), ("guide", frag("guide", 0, 1) - 0.05, "whoosh", 0.4),
    ("rule", 0.1, "swell", 0.5), *[("rule", frag("rule", 0, j), "pop", 0.35) for j in range(3)], ("rule", -0.4, "sting", 0.35),
    ("legend", 0.0, "gong", 1.0), ("legend", frag("legend", 0, 1), "ching", 1.0), ("legend", frag("legend", 0, 1), "glitch", 0.5),
    ("legend", vo_t("legend", 1), "gong", 0.8), ("legend", frag("legend", 1, 1), "ching", 0.8), ("legend", vo_t("legend", 2), "gong", 0.9),
    *beats("legend", frag("legend", 2, 0), D["legend"] - frag("legend", 2, 0), 0.55, 0.7),
    *bed("rain", T("laugh", 0), T("laugh", -0.1), 0.35),
    *bed("stream", T("stream", 0), T("stream", -0.1), 0.8), ("stream", vo_t("stream", 2), "boom", 0.35),
    *bed("rain", T("xsec", 0), T("xsec", -0.1), 0.3), ("xsec", frag("xsec", 1, 0), "whoosh", 0.8), ("xsec", frag("xsec", 1, 0) + 0.9, "roar", 0.8),
    *bed("stream", T("signs", 0), T("signs", -0.1), 0.8), ("signs", frag("signs", 0, 0) + 0.5, "swell", 0.5),
    ("signs", frag("signs", 0, 1), "riser", 0.6), ("signs", frag("signs", 0, 2) - 0.2, "roar", 1.2), ("signs", frag("signs", 0, 2), "thunder", 0.6),
    *bed("rain", T("climb", 0), T("climb", -0.1), 0.6), *[("climb", 0.2 + k * 0.48, "squelch", 0.45) for k in range(5)],
    *bed("crickets", T("night", 0), T("choice", 0), 0.6, 5.0), ("night", 0.4, "drip", 0.6), *[("night", 0.5 + k * 0.1, "tick", 0.35) for k in range(9)],
    ("cry", vo_t("cry") - 0.1, "sting", 0.7), *beats("cry", vo_t("cry"), D["cry"] - vo_t("cry"), 0.75, 0.6), ("cry", 0.0, "wind", 0.5),
    ("listen", 0.05, "rustle", 0.6), *beats("listen", 0.0, D["listen"], 0.7, 0.4),
    ("phonecam", 0.0, "beep", 1.0), ("phonecam", 0.0, "nv", 1.0), ("phonecam", vo_end("phonecam") + 0.1, "sting", 1.0), ("phonecam", vo_end("phonecam") + 0.1, "beep", 0.8),
    *[("sleep", t, "stomp", 0.35) for t in hops], ("sleep", 0.2, "swell", 0.4),
    *beats("feet", 0.0, D["feet"], 0.5, 1.0), ("feet", 0.6, "creak", 0.5), ("feet", 1.4, "drip", 0.6), ("feet", -0.15, "boom", 0.5),
    *bed("rain", T("twoam", 0), T("twoam", -0.1), 0.2), *beats("twoam", 0.0, D["twoam"], 0.42, 0.95), *[("twoam", 0.1 + k * 0.08, "tick", 0.4) for k in range(7)],
    ("twoam", vo_t("twoam", 2), "sting", 0.8), ("twoam", vo_t("twoam", 2), "boom", 0.4),
    ("leech", 0.1, "squish", 0.9), ("leech", frag("leech", 0, 1), "sting", 0.5),
    *[("howto", frag("howto", i, j) - 0.05, "pop", 0.5) for i in range(3) for j in range(2)], ("howto", frag("howto", 0, 0) + 0.2, "squish", 0.8),
    ("howto", frag("howto", 1, 1), "whoosh", 0.4),
    *[("bleed", 0.25 + k * 1.1, "drip", 0.8) for k in range(3)],
    ("relief", 0.0, "rustle", 0.4),
    *beats("print", 0.0, D["print"], 0.5, 0.8), ("print", 0.1, "squelch", 0.6), ("print", frag("print", 0, 1), "sting", 0.9), ("print", frag("print", 0, 1), "glitch", 0.5),
    *[("ring", 0.1 + k * 0.06, "tick", 0.3) for k in range(15)], *beats("ring", 0.0, D["ring"], 0.45, 0.85), ("ring", frag("ring", 0, 1), "boom", 0.6),
    *[("hammock", 0.2 + k * 1.6, "creak", 0.6) for k in range(2)], *beats("hammock", 0.0, D["hammock"], 0.42, 0.9), ("hammock", frag("hammock", 0, 1), "sting", 0.8),
    *beats("close", 0.0, vo_t("close"), 0.36, 0.6), ("close", vo_t("close") + 0.25, "glitch", 0.8), ("close", vo_t("close") + 0.25, "boom", 0.6),
    *beats("choice", 0.0, D["choice"] - 0.3, 0.38, 1.0), *[("choice", 0.05 + k * 1.0, "tick", 1.0) for k in range(3)], ("choice", 1.0, "glitch", 0.6),
    ("choice", D["choice"] - 2.2, "riser", 1.0), ("choice", D["choice"] - 1.0, "glitch", 0.8),
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


dip(0.0, T("hook", -0.1), 0.15, 0.05)                    # the cold open sits on rain and a heartbeat
dip(T("legend", 0), T("legend", -0.1), 0.35)              # let the gong ring
dip(T("cry", 0), T("cry", -0.1), 0.2)
dip(T("phonecam", 0), T("phonecam", -0.1), 0.35)
dip(T("feet", 0), T("feet", -0.05), 0.0, 0.1)              # silence: it is standing at her feet
dip(T("twoam", 0), T("twoam", -0.1), 0.3)
dip(T("print", 0), T("hammock", -0.1), 0.45)
dip(T("close", 0), T("close", -0.05), 0.0, 0.1)            # silence, then the whisper
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

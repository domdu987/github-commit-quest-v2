"""Build the episode soundtrack from schedule.json: per-line levelled voice, synthesized rainforest SFX
(rain, wind, flood roar, thunder, crickets, night-vision hiss) and the Suno music bed with dips before the scares and
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
LINE_GAIN = {"d01": -1, "d03": -1, "d02": 1}
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


hops = [0.1 + j * frag("arrive", 0, 1) / 4 for j in range(1, 5)]
_a, _b = frag("sig", 0, 0), frag("sig", 0, 1) + 0.15  # ticks on the checklist, as spread by Sig.ui in sig.js
SIG_TICKS = [_a + 0.3 + (_b - _a - 0.3) * i / (3 - 1) for i in range(3)] if 3 > 1 else [_b]
CUES = [
    *bed("rain", 0.0, T("hook", -0.1), 0.5), *bed("wind", 0.0, T("hook", -0.1), 0.35, 5.0), ("hook", 0.3, "thunder", 0.5),
    ("hook", frag("hook", 0, 2), "sting", 0.7), *beats("hook", frag("hook", 1, 2), D["hook"] - frag("hook", 1, 2), 0.5, 0.8),
    ("hook", frag("hook", 1, 1), "wind", 0.6), ("hook", -0.25, "whoosh", 0.8),
    ("rewind", 0.0, "rewind", 1.0), ("rewind", 0.05, "glitch", 0.5), ("rewind", 1.2, "pop", 0.5),
    *bed("rain", T("grab", 0), T("rule", -0.2), 0.45), ("grab", vo_t("grab") - 0.05, "whoosh", 0.7), *beats("grab", 0.0, D["grab"], 0.38, 0.7),
    *[("grab", 0.1 + k * 0.25, "squelch", 0.4) for k in range(3)],
    *[("climb", 0.2 + k * 0.6, "rustle", 0.55) for k in range(6)], ("climb", 0.9, "creak", 0.4), ("climb", 2.3, "snap", 0.35), *beats("climb", 0.0, D["climb"], 0.42, 0.5),
    *[("arrive", t, "stomp", 0.45) for t in hops], ("arrive", frag("arrive", 0, 1), "boom", 0.6), ("arrive", frag("arrive", 0, 1), "sting", 0.6),
    *beats("arrive", 0.0, D["arrive"], 0.45, 0.6),
    *[("cant", 0.1 + k * 0.5, "rustle", 0.8) for k in range(4)], ("cant", 0.6, "creak", 0.7), ("cant", frag("cant", 0, 1), "pop", 0.4),
    ("rain", 0.0, "thunder", 0.5), *bed("wind", T("rain", 0), T("signs", -0.1), 0.45, 5.0),
    *[("cold", t, "tick", 0.35) for t in [0.3, 1.2, 2.2, 3.2, 4.2]], ("cold", frag("cold", 1, 1), "beep", 0.9), ("cold", frag("cold", 1, 1), "sting", 0.7),
    ("slur", 0.3, "swell", 0.5), *beats("slur", 0.4, D["slur"] - 0.4, 0.8, 0.6),
    *[("signs", frag("signs", 0, j) + 0.05, "pop", 0.5) for j in range(3)], ("signs", frag("signs", 0, 2), "sting", 0.4),
    ("huddle", frag("huddle", 0, 1), "rustle", 0.9), ("huddle", frag("huddle", 0, 1) + 0.3, "rustle", 0.6), ("huddle", frag("huddle", 1, 1), "ding", 0.5),
    ("roar", 0.0, "rustle", 0.4), ("roar", frag("roar", 0, 1) - 0.2, "roar", 1.3), ("roar", frag("roar", 0, 1), "boom", 0.6), ("roar", frag("roar", 0, 1) + 0.3, "riser", 0.6),
    *bed("stream", T("roar", frag("roar", 0, 1)), T("flood", -0.1), 1.0, 3.0), *bed("rain", T("roar", 0), T("flood", -0.1), 0.4),
    ("flood", 0.0, "roar", 1.1), ("flood", frag("flood", 0, 1) - 0.05, "whoosh", 0.8), ("flood", vo_t("flood", 1) - 0.05, "boom", 0.6), ("flood", 2.6, "roar", 0.9),
    *bed("stream", T("rule", 0), T("rule", -0.1), 0.5), ("rule", 0.05, "swell", 0.5), *[("rule", t, "pop", 0.5) for t in (0.2, 0.75, 1.3)], ("rule", 0.95, "ching", 0.5), ("rule", frag("rule", 0, 1), "gong", 0.45),
    *bed("rain", T("flash", 0), T("feet", -0.1), 0.5),
    *[("flash", frag("flash", 0, 1) + k - 0.15, "snap", 0.6 - i * 0.15) for i, k in enumerate([0.15, 0.32, 0.55])], ("flash", frag("flash", 0, 1) + 0.25, "thunder", 1.0),
    ("flash", vo_t("flash", 1) - 0.05, "whoosh", 0.4),
    *beats("feet", 0.0, D["feet"], 0.5, 0.6), *[("feet", 0.4 + k * 0.9, "drip", 0.7) for k in range(3)], ("feet", frag("feet", 0, 1), "sting", 0.7),
    ("feet", vo_t("feet", 1) + 0.2, "creak", 0.5),
    *bed("stream", T("waits", 0), T("waits", -0.1), 0.6), *beats("waits", 0.0, D["waits"], 0.55, 0.6), ("waits", 0.8, "creak", 0.4),
    ("waits", frag("waits", 0, 1), "sting", 0.9), ("waits", frag("waits", 0, 1), "boom", 0.5),
    *bed("rain", T("night", 0), T("night", 1.8), 0.25), *bed("crickets", T("night", 0.8), T("dawn", vo_t("dawn", 1)), 0.45, 5.0),
    *[("night", 0.15 + k * 0.12, "tick", 0.3) for k in range(18)],
    *bed("stream", T("dawn", 0), T("dawn", vo_t("dawn", 1)), 0.35), ("dawn", frag("dawn", 0, 2), "swell", 0.4),
    ("dawn", vo_t("dawn", 1) - 0.1, "whoosh", 0.4), ("dawn", vo_t("dawn", 1) + 0.4, "creak", 0.6), ("dawn", vo_t("dawn", 1) + 1.6, "creak", 0.5),
    ("dawn", frag("dawn", 1, 1), "sting", 0.8), *beats("dawn", vo_t("dawn", 1), 3.0, 0.5, 0.5),
    # channel signature: three soft ticks, a held breath, then the cross
    ("sig", 0.05, "glitch", 0.35), ("sig", 0.05, "beep", 0.35), *[("sig", t, "ding", 0.6) for t in SIG_TICKS],
    ("sig", frag("sig", 0, 2), "glitch", 0.45), *beats("sig", frag("sig", 0, 2), frag("sig", 0, 3) - frag("sig", 0, 2), 0.38, 0.8),
    *[("sig", frag("sig", 0, 2) + o, "tick", 0.55 + 0.1 * k) for k, o in enumerate((0.1, 0.42, 0.68, 0.88, 1.02, 1.12))],  # ticking that speeds up into the cross
    ("sig", frag("sig", 0, 3) - 1.1, "riser", 0.6),
    ("sig", frag("sig", 0, 3), "sting", 1.1), ("sig", frag("sig", 0, 3), "boom", 0.8), ("sig", frag("sig", 0, 3), "glitch", 0.7), ("sig", frag("sig", 0, 3) + 0.12, "slam", 0.7),
    *beats("sig", frag("sig", 0, 3), D["sig"] - frag("sig", 0, 3), 0.5, 0.7),
    ("play", 0.2, "beep", 0.9), ("play", frag("play", 0, 1), "notif", 0.4),
    ("three", 0.0, "nv", 1.0), ("three", 0.0, "static", 0.25), *beats("three", 0.4, D["three"] - 0.4, 0.55, 0.6),
    ("three", frag("three", 0, 2) - 0.1, "beep", 0.9), ("three", frag("three", 0, 2), "sting", 1.0), ("three", frag("three", 0, 2), "boom", 0.5),
    ("three", vo_t("three", 1), "glitch", 0.7), ("three", frag("three", 1, 1), "riser", 0.6),
    ("drip", 0.0, "beep", 0.7), ("drip", 0.0, "static", 0.2), ("drip", frag("drip", 0, 1) + 0.5, "drip", 1.2), ("drip", frag("drip", 0, 1) + 0.5, "squish", 0.8),
    ("drip", frag("drip", 0, 1) + 0.5, "boom", 0.5), *beats("drip", frag("drip", 0, 1) + 0.5, D["drip"] - frag("drip", 0, 1) - 0.5, 0.42, 0.8),
    ("drip", frag("drip", 0, 1) + 1.5, "drip", 0.8),
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
dip(T("arrive", 0), T("cant", -0.1), 0.35)
dip(T("roar", frag("roar", 0, 1)), T("flood", -0.1), 0.4)  # the flood owns the soundtrack
dip(T("flash", 0), T("flash", -0.1), 0.4)
dip(T("feet", 0), T("feet", -0.1), 0.25)
dip(T("waits", frag("waits", 0, 1)), T("waits", -0.05), 0.0, 0.1)   # silence: it waits too
dip(T("dawn", vo_t("dawn", 1)), T("dawn", -0.1), 0.3)
dip(T("sig", frag("sig", 0, 2)), T("sig", frag("sig", 0, 3) + 0.05), 0.05, 0.12)  # silence before "ข้อเดียว"
dip(T("three", 0), T("three", -0.1), 0.25)
dip(T("drip", 0), T("drip", -0.05), 0.0, 0.1)              # silence, then the drop
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

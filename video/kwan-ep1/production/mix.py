"""Build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX for a night drive in fog
(engine, tyre screech, the hazard relay, the handbrake, a knock on the glass, the power window) and the Suno music bed with dips
before the scares and sidechain ducking under the voice. Output -14 LUFS, hard cut to silence at the end."""
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


CUES = [
    # story opener (Opener.cues, at 1.9 / glide 1.8): drone, glitches, the EP stamp, the eyes, riser, the fall, the hit
    ("open", 0.0, "swell", 0.6), ("open", 0.55, "glitch", 0.35), ("open", 0.82, "boom", 0.45), ("open", 1.15, "sting", 0.5), ("open", 1.18, "glitch", 0.45),
    *beats("open", 1.15, 0.75, 0.5, 0.6), ("open", 1.0, "riser", 0.7), ("open", 1.78, "glitch", 0.5), ("open", 1.9, "whoosh", 0.9), ("open", 2.71, "whoosh", 0.8),
    ("open", 3.68, "boom", 0.9), ("open", 3.7, "glitch", 0.5), ("open", 3.75, "crackle", 0.8),
    # you wake: the smoke alarm, the knocking
    *[("wake", 0.4 + k * 0.5, "beep", 0.22) for k in range(13)], ("wake", 1.0, "knock", 1.1), ("wake", 1.22, "knock", 1.0), ("wake", 1.44, "knock", 1.1),
    *[("wake", vo_t("wake", 1) - 0.25 + k * 0.18, "knock", 1.2) for k in range(4)], *beats("wake", vo_t("wake", 1), D["wake"] - vo_t("wake", 1), 0.45, 0.5),
    ("stop", 0.08, "sting", 0.8), ("stop", 0.1, "thud", 0.5), *beats("stop", 0.3, D["stop"] - 0.3, 0.45, 0.55),
    ("phone", 0.1, "vibe", 0.7), ("phone", frag("phone", 0, 1), "tick", 0.4),
    ("timer", 0.05, "click", 0.8), ("timer", 0.3, "ding", 0.35), *[("timer", 0.5 + k * 1.0, "tick", 0.45) for k in range(3)],
    ("gap", 0.2, "crackle", 1.0), ("gap", frag("gap", 0, 1), "creak", 0.5), *beats("gap", frag("gap", 0, 2), D["gap"] - frag("gap", 0, 2), 0.42, 0.5),
    *[("bang", t0 + k * 0.16, "knock", 1.3) for t0, n in ((0.1, 5), (0.9, 4), (1.6, 5)) for k in range(n)], ("bang", 0.1, "glitch", 0.4),
    ("sign", 1.4, "rustle", 0.6), *[("sign", 0.5 + k * 1.0, "tick", 0.35) for k in range(6)],
    ("rule", 0.0, "swell", 0.5), *[("rule", frag("rule", 0, j), "sting", 0.35) for j in range(3)], ("rule", frag("rule", 0, 2) + 0.45, "glitch", 0.6),
    *beats("rule", frag("rule", 0, 2), D["rule"] - frag("rule", 0, 2), 0.5, 0.5),
    ("dao", frag("dao", 0, 2), "sting", 1.0), ("dao", frag("dao", 0, 2), "boom", 0.7), ("dao", frag("dao", 0, 2), "glitch", 0.7),
    ("touch", frag("touch", 0, 1) + 0.15, "sting", 0.9), ("touch", frag("touch", 0, 1) + 0.15, "thud", 0.6), ("touch", 0.0, "crackle", 0.9),
    ("hot", 0.0, "crackle", 1.0), *beats("hot", 0.5, D["hot"] - 0.5, 0.45, 0.45),
    ("noexit", 0.1, "whoosh", 0.9), ("noexit", frag("noexit", 0, 1) - 0.12, "boom", 0.6), ("noexit", frag("noexit", 0, 1) - 0.1, "siren", 0.25),
    ("smoke", 0.0, "swell", 0.4), ("smoke", 1.6, "thud", 0.4), *[("smoke", 0.5 + k * 1.0, "tick", 0.4) for k in range(3)],
    ("crawl", frag("crawl", 0, 1), "thud", 0.6), ("crawl", frag("crawl", 0, 1) + 0.1, "rustle", 0.6), ("crawl", 2.2, "sting", 0.45), *beats("crawl", 2.2, D["crawl"] - 2.2, 0.42, 0.5),
    ("seal", frag("seal", 0, 1) - 0.2, "rustle", 0.9), ("seal", frag("seal", 0, 1) + 0.8, "rustle", 0.6),
    *[("call", 0.25 + k * 0.32, "beep", 0.6) for k in range(3)], ("call", 1.4, "ring", 0.5), ("call", vo_t("call", 1) - 0.3, "click", 0.7),
    ("window", 0.0, "siren", 0.55), ("window", 2.4, "siren", 0.6), ("window", 2.6, "sting", 0.5), *beats("window", 2.6, D["window"] - 2.6, 0.42, 0.5),
    # channel signature
    ("sig", 0.05, "glitch", 0.35), ("sig", 0.05, "beep", 0.35),
    ("sig", frag("sig", 0, 0) + 0.3, "ding", 0.6), ("sig", frag("sig", 0, 0) + 0.62, "ding", 0.6), ("sig", frag("sig", 0, 1) + 0.15, "ding", 0.6),
    ("sig", frag("sig", 0, 2), "glitch", 0.45), *beats("sig", frag("sig", 0, 2), frag("sig", 0, 3) - frag("sig", 0, 2), 0.38, 0.8),
    *[("sig", frag("sig", 0, 2) + o, "tick", 0.55 + 0.1 * k) for k, o in enumerate((0.1, 0.42, 0.68, 0.88, 1.02, 1.12))],
    ("sig", frag("sig", 0, 3) - 1.1, "riser", 0.6),
    ("sig", frag("sig", 0, 3), "sting", 1.1), ("sig", frag("sig", 0, 3), "boom", 0.8), ("sig", frag("sig", 0, 3), "glitch", 0.7), ("sig", frag("sig", 0, 3) + 0.12, "slam", 0.7),
    *beats("sig", frag("sig", 0, 3), D["sig"] - frag("sig", 0, 3), 0.5, 0.7),
    # the peephole: แพร, alive, outside; then the bed
    ("reveal", 0.05, "whoosh", 0.6), *beats("reveal", 0.6, D["reveal"] - 0.6, 0.6, 0.4),
    *[("prae", 0.1 + k * 0.28, "knock", 1.2) for k in range(6)], ("prae", frag("prae", 0, 2), "sting", 1.0), ("prae", frag("prae", 0, 2), "glitch", 0.6),
    ("turn", 0.2, "whoosh", 0.8), *beats("turn", 0.0, D["turn"], 0.36, 0.6),
    ("ghost", 0.3, "creak", 0.9), ("ghost", 0.35, "swell", 0.7), ("ghost", 1.7, "sting", 0.8), ("ghost", 1.7, "glitch", 0.5), ("ghost", 1.9, "beep", 0.9),
    *beats("ghost", 0.4, D["ghost"] - 1.0, 0.4, 0.6), ("ghost", D["ghost"] - 1.4, "riser", 0.8),
    ("ghost", D["ghost"] - 0.6, "shriek", 0.7), ("ghost", D["ghost"] - 0.6, "boom", 0.9), ("ghost", D["ghost"] - 0.6, "glitch", 0.7),
    # the choice, then the key tag
    *beats("choice", 0.0, D["choice"] - 0.3, 0.38, 1.0), *[("choice", 0.05 + k * 1.0, "tick", 1.0) for k in range(3)], ("choice", 1.0, "glitch", 0.6),
    ("choice", D["choice"] - 2.2, "riser", 1.0), ("choice", D["choice"] - 0.62, "sting", 1.0), ("choice", D["choice"] - 0.6, "glitch", 0.8), ("choice", D["choice"] - 0.6, "boom", 0.7),
    ("next", 0.3, "whoosh", 0.5), ("next", 0.45, "ching", 0.5), ("next", 0.8, "sting", 0.7), *beats("next", 0.9, D["next"] - 0.9, 0.7, 0.5),
]
# no hiss: the noise-based wind bed reads as static under the voice (user: "ลบเสียงซ่าออก"), and the fire keeps only a faint crackle
CUES = [(k, t, typ, g * (0.3 if typ == "crackle" else 1)) for k, t, typ, g in CUES if typ not in ("wind",)]
CUES = [c for c in CUES if c[3] > 0]
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


dip(0.0, T("open", -0.05), 0.25, 0.05)                    # the opener: drone and hits over a quiet bed
dip(T("wake", 0), T("stop", -0.05), 0.35)
dip(T("rule", 0), T("dao", -0.05), 0.3)                    # her voice reading the rule
dip(T("sig", frag("sig", 0, 2)), T("sig", frag("sig", 0, 3) + 0.05), 0.05, 0.12)  # silence before "ข้อเดียว"
dip(T("turn", 0), T("ghost", -0.05), 0.25)
dip(T("choice", 0), T("choice", -0.3), 0.5)
boost = np.ones(N, np.float32)
mus = mus * gain * boost
end = int(T("choice", -0.2) * SR)
mus[end:] = 0  # hard cut to black and silence

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mix = vo + mus * duck + sfx
cut, card = int(T("choice", -0.2) * SR), int(T("next", 0.3) * SR)
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

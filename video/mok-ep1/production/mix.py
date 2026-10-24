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
    # cold open: the engine, the fog, a hand going for the high beams — stop
    *bed("engine", T("hook", 0), T("hook", -0.1), 0.8, 3.6), ("hook", 0.2, "wind", 0.4), *beats("hook", 0.4, D["hook"] - 0.4, 0.55, 0.55),
    ("hook", vo_t("hook", 1), "sting", 0.9), ("hook", vo_t("hook", 1), "boom", 0.6), ("hook", vo_t("hook", 1), "glitch", 0.5), ("hook", -0.25, "whoosh", 0.8),
    ("chapter", 0.05, "whoosh", 0.6), ("chapter", 0.3, "engine", 0.5), ("chapter", 0.55, "sting", 0.5),
    ("road", 0.0, "wind", 0.6), ("road", 0.2, "crickets", 0.4),
    # the petrol station: the tubes hum, crickets
    *bed("hum", T("mint", 0), T("gps", D["gps"] * 0.55), 0.5, 3.6), *bed("crickets", T("mint", 0), T("gps", D["gps"] * 0.55), 0.4, 3.6),
    ("saeng", 0.1, "swell", 0.4),
    ("rule", frag("rule", 0, 0), "ding", 0.45), ("rule", frag("rule", 0, 2), "ding", 0.45), ("rule", frag("rule", 0, 4), "ding", 0.45), ("rule", frag("rule", 0, 5), "sting", 0.6),
    ("gps", D["gps"] * 0.55, "engine", 0.6), ("gps", D["gps"] * 0.55, "whoosh", 0.4),
    ("mirror", 0.1, "hum", 0.5), ("mirror", frag("mirror", 0, 1), "glitch", 0.35), ("mirror", frag("mirror", 0, 2), "sting", 1.0), ("mirror", frag("mirror", 0, 2), "boom", 0.5),
    *beats("mirror", frag("mirror", 0, 2), D["mirror"] - frag("mirror", 0, 2), 0.45, 0.7),
    # 3 a.m. on the road
    *bed("engine", T("three", 0), T("stop", -0.05), 0.75, 3.6), ("three", 0.0, "wind", 0.6), ("three", 0.4, "tick", 0.5),
    ("high", vo_end("high") - 0.3, "stalk", 1.0),
    ("glare", 0.0, "whoosh", 0.8), ("glare", 0.05, "buzz", 0.4), ("glare", frag("glare", 0, 2), "sting", 1.1), ("glare", frag("glare", 0, 2), "boom", 0.8), ("glare", frag("glare", 0, 2), "glitch", 0.7),
    *beats("glare", frag("glare", 0, 2), D["glare"] - frag("glare", 0, 2), 0.38, 0.8),
    ("swerve", 0.4, "screech", 1.2), ("swerve", 0.45, "whoosh", 0.7), ("swerve", 1.2, "thud", 0.5), *beats("swerve", 0.0, D["swerve"], 0.35, 0.8),
    *[("low", frag("low", 0, j) - 0.05, "pop", 0.45) for j in (1, 2, 3)],
    ("wave", 0.2, "wind", 0.5), ("wave", frag("wave", 0, 1), "sting", 0.6), *beats("wave", frag("wave", 0, 1), D["wave"] - frag("wave", 0, 1), 0.45, 0.6),
    ("stop", vo_t("stop", 1), "sting", 0.9), ("stop", vo_t("stop", 1), "glitch", 0.4),
    ("pass", 0.1, "whoosh", 0.9), ("pass", 0.2, "engine", 0.8), ("pass", 1.0, "sting", 0.6), *beats("pass", 0.0, D["pass"], 0.4, 0.7),
    # white out, hazards, pull over, lights off, handbrake, foot off the brake
    *bed("engine", T("white", 0), T("haz", 1.5), 0.6, 3.6), ("white", 0.0, "wind", 0.8), ("white", 0.1, "swell", 0.4),
    ("haz", 0.58, "click", 0.9),
    *bed("blinker", T("haz", 0.62), T("why", 0), 0.6, 0.8),
    ("off", frag("off", 0, 0) + 0.3, "click", 0.7), ("off", frag("off", 0, 2) + 0.1, "ratchet", 1.0), ("off", frag("off", 0, 3) + 0.5, "click", 0.5),
    ("why", 0.1, "engine", 0.8), ("why", 0.2, "riser", 0.6), ("why", frag("why", 0, 2) + 0.35, "screech", 0.8), ("why", frag("why", 0, 2) + 0.4, "slam", 1.2), ("why", frag("why", 0, 2) + 0.4, "boom", 0.8), ("why", frag("why", 0, 2) + 0.4, "glitch", 0.6),
    ("sig", 0.05, "glitch", 0.35), ("sig", 0.05, "beep", 0.35),
    ("sig", frag("sig", 0, 0) + 0.3, "ding", 0.6), ("sig", frag("sig", 0, 0) + 0.62, "ding", 0.6), ("sig", frag("sig", 0, 1) + 0.15, "ding", 0.6),
    ("sig", frag("sig", 0, 2), "glitch", 0.45), *beats("sig", frag("sig", 0, 2), frag("sig", 0, 3) - frag("sig", 0, 2), 0.38, 0.8),
    *[("sig", frag("sig", 0, 2) + o, "tick", 0.55 + 0.1 * k) for k, o in enumerate((0.1, 0.42, 0.68, 0.88, 1.02, 1.12))],
    ("sig", frag("sig", 0, 3) - 1.1, "riser", 0.6),
    ("sig", frag("sig", 0, 3), "sting", 1.1), ("sig", frag("sig", 0, 3), "boom", 0.8), ("sig", frag("sig", 0, 3), "glitch", 0.7), ("sig", frag("sig", 0, 3) + 0.12, "slam", 0.7),
    *beats("sig", frag("sig", 0, 3), D["sig"] - frag("sig", 0, 3), 0.5, 0.7),
    # a car comes up behind and stops; nobody gets out; the plate
    *bed("blinker", T("behind", 0), T("choice", -0.3), 0.55, 0.8),
    ("behind", 0.1, "engine", 0.7), ("behind", 1.2, "engine", 0.5), ("behind", D["behind"] - 0.8, "thud", 0.3), *beats("behind", 0.6, D["behind"] - 0.6, 0.45, 0.6),
    ("nobody", 0.0, "engine", 0.35), ("nobody", 0.1, "wind", 0.6), ("nobody", frag("nobody", 0, 0) + 0.6, "sting", 0.6),
    ("plate", 0.1, "swell", 0.4), ("plate", frag("plate", 0, 2) - 0.05, "sting", 1.1), ("plate", frag("plate", 0, 2) - 0.05, "boom", 0.7), ("plate", frag("plate", 0, 2) - 0.05, "glitch", 0.7),
    *beats("plate", frag("plate", 0, 2), D["plate"] - frag("plate", 0, 2), 0.42, 0.75),
    # the knock, the window
    *[("knock", k, "knock", 1.2) for k in (0.15, 0.4, 0.65)], ("knock", 0.15, "sting", 0.8), *beats("knock", 0.0, D["knock"], 0.42, 0.7),
    *beats("choice", 0.0, D["choice"] - 0.3, 0.38, 1.0), *[("choice", 0.05 + k * 1.0, "tick", 1.0) for k in range(3)], ("choice", 1.0, "glitch", 0.6),
    ("choice", 2.0, "motor", 1.4), ("choice", D["choice"] - 2.2, "riser", 1.0), ("choice", D["choice"] - 0.62, "sting", 1.0), ("choice", D["choice"] - 0.6, "glitch", 0.8), ("choice", D["choice"] - 0.6, "boom", 0.7),
    ("next", 0.3, "whoosh", 0.5), ("next", 0.45, "pop", 0.5), ("next", 0.8, "sting", 0.7), *beats("next", 0.9, D["next"] - 0.9, 0.7, 0.5),
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


dip(0.0, T("hook", -0.1), 0.2, 0.05)                     # the cold open: engine and fog
dip(T("mirror", 0), T("mirror", -0.05), 0.3)
dip(T("glare", 0), T("swerve", -0.05), 0.3)
dip(T("white", 0), T("off", -0.05), 0.4)
dip(T("sig", frag("sig", 0, 2)), T("sig", frag("sig", 0, 3) + 0.05), 0.05, 0.12)  # silence before "ข้อเดียว"
dip(T("behind", 0), T("knock", -0.05), 0.3)
dip(T("choice", 0), T("choice", -0.3), 0.5)
boost = np.ones(N, np.float32)  # the swerve plays with the music up
a0, a1 = T("swerve", 0.3), T("swerve", -0.05)
boost += 0.4 * (np.clip((t - a0) / 0.2, 0, 1) * np.clip((a1 - t) / 0.2, 0, 1)).astype(np.float32)
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

"""Build the episode soundtrack from schedule.json (เอาชีวิตรอด 99 วัน EP.8 "ยาตู้เย็น"): per-line levelled voice, synthesized SFX
(the canteen's tubes and spoons, the slaps that do nothing, the silence of a child who can't breathe, ภู's five back blows and the
thrusts, the score board, คุณวิน's pen, the yard at midnight, the radio in the office) and the Suno music bed with dips and ducking.
Every noise sound comes from the de-hissed synth.py (fband on every bed). Output -14 LUFS, hard cut to silence at the cliffhanger."""
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


D = {k: SH[k]["dur"] for k in SH}
# the same beats as shots.part
BF = 1.9                                                                                    # the bar fridge opens here (steal)

# ---- voice: every line levelled on its own so shouts and the child's line sit at a readable loudness ----
LINE_GAIN = {"r01": -2, "w02": -1, "p02": -1, "h02": -1, "p03": -1, "pn02": 1, "s01": 0}
vo = np.zeros(N, np.float32)
for s in SC["shots"]:
    for v in s["vo"]:
        x = load(os.path.join(HERE, "vo", f"{v['id']}.wav"))
        place(vo, level(x, -18 + LINE_GAIN.get(v["id"], 0)), s["start"] + v["t"])


def beats(k, t0, dur, period, g=0.9):  # heartbeat sfx in step with Fx.heart
    return [(k, t0 + i * period, "heartbeat", g) for i in range(int((dur - 0.1) / period) + 1)]


def bed(kind, a, b, g, step=4.6):  # overlapping copies of an ambience between absolute times a and b
    out, t = [], a - 0.6
    while t < b - 1.0:
        out.append((None, t, kind, g))
        t += step
    return out


CUES = [
    # cold open: the fridge dead (no hum), water dripping off the shelves, her tremor; "อย่าหยุดยาเอง" — the jolt
    ("hook", -0.2, "whoosh", 0.6), *[("hook", 0.5 + k * 0.9, "drip", 0.35) for k in range(7)], ("hook", 0.3, "creak", 0.5), ("hook", 1.4, "click", 0.3),
    *[("hook", vo_t("hook", 0) + 0.4 + k * 0.55, "tick", 0.3) for k in range(10)],
    ("hook", frag("hook", 2, 1), "sting", 1.0), ("hook", frag("hook", 2, 1), "boom", 0.6), ("hook", frag("hook", 2, 1), "glitch", 0.5), *beats("hook", 0.3, D["hook"] - 0.3, 0.55, 0.6),
    # the yard after the storm: the board; wind, water off the panels, a broom
    ("chapter", 0.05, "page", 0.9), ("chapter", 0.4, "chalk", 0.5), ("chapter", 0.5, "slam", 0.5), *[("chapter", 0.9 + k * 0.16, "pop", 0.4) for k in range(2)],
    *bed("wind", T("chapter", 0), T("chapter", -0.1), 0.25, 3.2), *[("chapter", 0.8 + k * 0.7, "drip", 0.3) for k in range(5)], *[("chapter", 1.2 + k * 0.5, "rustle", 0.25) for k in range(6)],
    ("chapter", frag("chapter", 0, 2), "sting", 0.5),
    # the canteen: the dead fridge with its door open; คุณวิน keeps the power
    *bed("crickets", T("dark", 0), T("hong", -0.1), 0.08, 4.0), ("dark", 0.3, "creak", 0.5), ("dark", frag("dark", 0, 1), "sting", 0.5), ("dark", vo_t("dark", 1) - 0.1, "whoosh", 0.3), ("dark", frag("dark", 1, 1), "sting", 0.6), ("dark", frag("dark", 1, 1), "boom", 0.3), *beats("dark", 0.0, D["dark"], 0.8, 0.35),
    # เจ๊หงส์ and the warm vial; the box shoved away
    ("hong", 0.3, "click", 0.3), ("hong", frag("hong", 1, 1), "sting", 0.6), ("hong", vo_t("hong", 1) + 1.0, "slam", 0.35), ("hong", vo_t("hong", 1) + 1.05, "rustle", 0.4), *beats("hong", 0.0, D["hong"], 0.7, 0.4),
    # the dorm at dusk: the fan, her breathing
    *bed("crickets", T("skip", 0), T("kong", -0.1), 0.12, 4.0), *[("skip", 0.2 + k * 1.2, "fan", 0.18) for k in range(4)], ("skip", frag("skip", 1, 1), "sting", 0.6), ("skip", frag("skip", 1, 1), "breath", 0.5), *beats("skip", 0.0, D["skip"], 0.7, 0.4),
    # ก้อง at the window, then out of the door
    ("kong", vo_t("kong", 0) + 1.7, "steps", 0.35), ("kong", vo_t("kong", 0) + 2.1, "steps", 0.35), ("kong", vo_t("kong", 0) + 2.5, "creak", 0.4), ("kong", vo_t("kong", 1), "sting", 0.6), ("kong", vo_t("kong", 1), "boom", 0.3), *beats("kong", 0.0, D["kong"], 0.6, 0.5),
    # the office: the sneak, the bar fridge opening (its hum), the torch behind the glass
    *bed("hum", T("steal", BF), T("steal", -0.1), 0.2, 3.0), *[("steal", 0.1 + k * 0.4, "steps", 0.2) for k in range(3)], ("steal", BF, "latch", 0.5), ("steal", BF + 0.05, "creak", 0.4), ("steal", BF + 0.4, "click", 0.3), ("steal", frag("steal", 0, 1), "sting", 0.5), *beats("steal", 0.0, D["steal"], 0.5, 0.6),
    # the label: the box handed over, the card, her eyes
    ("label", vo_t("label", 1) + 0.2, "page", 0.5), ("label", vo_t("label", 1) + 0.5, "pen", 0.5), ("label", frag("label", 1, 1), "sting", 0.6), ("label", frag("label", 1, 1) + 0.05, "ding", 0.3), ("label", vo_t("label", 2) + 0.1, "sting", 0.5), ("label", vo_t("label", 2) + 0.5, "gasp", 0.35), *beats("label", 0.0, D["label"], 0.75, 0.35),
    # the card
    *[x for o in (vo_t("card", 0), vo_t("card", 1), frag("card", 1, 2), frag("card", 1, 3) + 0.6) for x in (("card", o, "page", 0.4), ("card", o + 0.3, "pen", 0.5), ("card", o + 0.35, "ding", 0.25))],
    # in real life
    ("real", 0.1, "page", 0.4), ("real", 0.4, "pen", 0.4), ("real", frag("real", 0, 1), "ding", 0.3),
    # the torch on his face, the box on the floor, the guards, the bell
    ("alarm", 0.3, "click", 0.7), ("alarm", 0.3, "sting", 1.0), ("alarm", 0.3, "boom", 0.6), ("alarm", 0.3, "glitch", 0.5), ("alarm", 0.8, "thud", 0.5), ("alarm", 0.82, "rustle", 0.3), *[("alarm", 0.2 + k * 0.3, "steps", 0.4) for k in range(4)], *[("alarm", 1.0 + k * 0.48, "bell", 0.6) for k in range(8)],
    ("alarm", frag("alarm", 0, 2), "sting", 0.7), ("alarm", frag("alarm", 0, 2), "boom", 0.4), *beats("alarm", 0.0, D["alarm"], 0.36, 0.9),
    # across the yard: the bell, running feet, ภู's shove, the gate
    *[("run", 0.1 + k * 0.6, "bell", 0.45) for k in range(8)], *[("run", 0.05 + k * 0.22, "steps", 0.4) for k in range(20)], ("run", vo_t("run", 0), "sting", 0.5), ("run", 1.1, "thud", 0.7), ("run", 1.12, "boom", 0.3), *bed("wind", T("run", 0), T("gate", -0.1), 0.15, 3.2), *beats("run", 0.0, D["run"], 0.36, 0.9),
    ("gate", 0.3, "gate", 0.8), ("gate", 1.2, "gate", 0.6), *[("gate", 0.05 + k * 0.24, "steps", 0.35) for k in range(10)], ("gate", vo_t("gate", 0), "sting", 0.5), ("gate", vo_t("gate", 1) - 0.1, "slam", 1.0), ("gate", vo_t("gate", 1) - 0.1, "boom", 0.7), ("gate", vo_t("gate", 1) - 0.1, "glitch", 0.4), ("gate", vo_t("gate", 1) - 0.05, "clang", 0.6), *beats("gate", 0.0, D["gate"], 0.36, 0.95),
    # the field: crickets, wind; the walkie's LED, its crackle, the voice
    *bed("crickets", T("outside", 0), T("sig", -0.1), 0.16, 4.0), *bed("wind", T("outside", 0), T("sig", -0.1), 0.12, 3.2), ("outside", 0.6, "breath", 0.4), *beats("outside", 0.0, D["outside"], 0.6, 0.5),
    *[("walkie", 0.2 + k * 0.45, "beep", 0.15) for k in range(int((vo_t("walkie", 0) - 0.5) / 0.45))], ("walkie", vo_t("walkie", 0) - 0.35, "static", 0.6), ("walkie", vo_t("walkie", 0) - 0.3, "rustle", 0.4), *bed("radiobed", T("walkie", vo_t("walkie", 0) - 0.3), T("walkie", vo_end("walkie", 1) + 0.2), 0.25, 3.0),
    ("walkie", frag("walkie", 0, 1), "sting", 0.5), ("walkie", frag("walkie", 1, 2), "sting", 1.0), ("walkie", frag("walkie", 1, 2), "boom", 0.6), ("walkie", frag("walkie", 1, 2), "glitch", 0.5), ("walkie", vo_t("walkie", 2), "sting", 0.5), *beats("walkie", 0.0, D["walkie"], 0.5, 0.6),
    # the signature
    ("sig", 0.05, "page", 0.8), ("sig", 0.36, "thud", 0.25),
    *[x for o in (frag("sig", 0, 0) + 0.3, frag("sig", 0, 0) + 0.62, frag("sig", 0, 1) + 0.15) for x in (("sig", o, "pen", 0.9), ("sig", o + 0.05, "ding", 0.3))],
    ("sig", frag("sig", 0, 2) + 0.45, "marker", 0.45), *beats("sig", frag("sig", 0, 2), frag("sig", 0, 3) - frag("sig", 0, 2), 0.38, 0.8),
    *[("sig", frag("sig", 0, 2) + o, "tick", 0.55 + 0.1 * k) for k, o in enumerate((0.1, 0.42, 0.68, 0.88, 1.02, 1.12))],
    ("sig", frag("sig", 0, 3) - 1.1, "riser", 0.6),
    ("sig", frag("sig", 0, 3), "sting", 1.1), ("sig", frag("sig", 0, 3), "boom", 0.7), ("sig", frag("sig", 0, 3), "pen", 1.0), ("sig", frag("sig", 0, 3) + 0.1, "pen", 1.0),
    ("sig", frag("sig", 0, 3) + 0.24, "rip", 1.1), ("sig", frag("sig", 0, 3) + 0.86, "thud", 0.8), ("sig", frag("sig", 0, 3) + 0.86, "slam", 0.35),
    *beats("sig", frag("sig", 0, 3), D["sig"] - frag("sig", 0, 3), 0.5, 0.7),
    # the radio: static, the dial, the day torn off, the number
    ("count", vo_t("count", 0) - 0.4, "static", 0.7), ("count", vo_t("count", 0) - 0.3, "radio", 0.5), *bed("radiobed", T("count", vo_t("count", 0) - 0.4), T("count", -0.1), 0.3, 3.0), ("count", frag("count", 0, 1), "rip", 0.8), ("count", frag("count", 0, 1) + 0.1, "page", 0.4), ("count", frag("count", 0, 2), "sting", 1.0), ("count", frag("count", 0, 2), "boom", 0.6), ("count", frag("count", 0, 2), "glitch", 0.4), *beats("count", 0.0, D["count"], 0.5, 0.6),
    # the drawing under the lightning
    ("drawing", 0.1, "crayon", 0.6), ("drawing", 0.9, "crayon", 0.5), ("drawing", frag("drawing", 0, 1) - 0.3, "thunder", 0.8), ("drawing", frag("drawing", 0, 1), "sting", 0.6), *bed("rain", T("drawing", 0), T("drawing", -0.1), 0.2, 3.0), *beats("drawing", 0.0, D["drawing"], 0.55, 0.5),
    # the choice, then black; the end card
    *beats("choice", 0.0, D["choice"] - 0.3, 0.38, 1.0), *[("choice", 0.05 + k * 1.0, "tick", 1.0) for k in range(3)], ("choice", 1.0, "glitch", 0.6), ("choice", D["choice"] - 0.6, "riser", 0.8), ("choice", D["choice"] - 0.2, "sting", 1.0), ("choice", D["choice"] - 0.2, "boom", 0.7),
    ("next", 0.3, "page", 0.7), ("next", 0.6, "page", 0.5), *[("next", 0.9 + k * 0.22, "pen", 0.5) for k in range(5)], ("next", 1.9, "glitch", 0.4),
]
cues = {"duration": TOTAL, "sections": [{"start": 0, "end": TOTAL, "mood": "silence"}],
        "sfx": [{"t": round(float(t) if k is None else T(k, float(t)), 3), "type": typ, "gain": g} for k, t, typ, g in CUES]}
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


dip(0.0, T("hook", -0.1), 0.3, 0.05)
dip(T("hong", frag("hong", 1, 1) - 0.2), T("hong", -0.05), 0.4)
dip(T("steal", 0), T("steal", -0.05), 0.3)
dip(T("alarm", 0.2), T("alarm", 1.0), 0.15)
dip(T("gate", vo_t("gate", 1) - 0.2), T("gate", -0.05), 0.3)
dip(T("walkie", vo_t("walkie", 0) - 0.4), T("walkie", -0.05), 0.2)
dip(T("sig", frag("sig", 0, 2)), T("sig", frag("sig", 0, 3) + 0.05), 0.05, 0.12)
dip(T("count", vo_t("count", 0) - 0.4), T("count", -0.05), 0.2)
dip(T("drawing", frag("drawing", 0, 1)), T("drawing", -0.05), 0.35)
dip(T("choice", 0), T("choice", -0.3), 0.5)
boost = np.ones(N, np.float32)  # the action plays with the music up
for a0, a1 in ((T("alarm", 1.0), T("alarm", -0.05)), (T("run", 0), T("run", -0.05)), (T("gate", 0), T("gate", vo_t("gate", 1) - 0.3))):
    boost += 0.4 * (np.clip((t - a0) / 0.3, 0, 1) * np.clip((a1 - t) / 0.2, 0, 1)).astype(np.float32)
mus = mus * gain * boost
end = int(T("choice", -0.2) * SR)
mus[end:] = 0  # hard cut to black and silence

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
SFX_GAIN_DB = -1.648   # the same absolute effects level as EP.6 (its de-hissed stem kept level(sfx, -27) of the v2 stem); not re-normalised per episode
mus = level(mus, -30)
sfx = sfx * 10 ** (SFX_GAIN_DB / 20)
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

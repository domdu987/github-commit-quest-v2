"""Build the episode soundtrack from schedule.json (ติดเกาะร้าง EP.1 "ผีอำ"): per-line levelled voice, synthesized SFX (the sea on every
shore, gulls, the longtail, the squall, the lighter and the fire, the pool and the fish's grunt, fat on the grill, the clock, the
lamp's wire, the breaths she gives, the compressions, the first breath at dawn) and the Suno music bed with dips and ducking.
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
HK2 = vo_t("hook", 1) - 0.08                       # the cut to the sand
BT2 = 2.6                                          # the cut into the boat
FSH = vo_t("fish", 2) - 0.15; FS3 = vo_t("fish", 3) - 0.15
PA2 = vo_t("phiam", 1) - 0.25
LP2 = vo_t("lamp", 1) - 0.4
DW2 = vo_t("dawn", 1) - 0.4; DW3 = vo_t("dawn", 2) - 0.25

# ---- voice: every line levelled on its own; the inner voice and the weak lines sit a touch lower, the shouts a touch lower too ----
LINE_GAIN = {"i01": -2, "i02": -2, "t10": 1, "t11": 1, "t12": 0, "p07": -1.5, "p09": -1.5, "m01": -1, "m02": -1, "m03": -1, "s01": 0}
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
    # cold open: the fish in his hands (water dripping, its grunt), then the hard cut to the sand: muffled, the heart
    ("hook", 0.05, "splash", 0.35), ("hook", 0.5, "squeak", 0.6), ("hook", 1.9, "squeak", 0.45), *[("hook", 0.3 + k * 0.33, "drip", 0.3) for k in range(6)],
    *bed("waves", T("hook", 0), T("hook", HK2), 0.2, 4.6),
    ("hook", HK2, "boom", 0.6), ("hook", HK2, "whoosh", 0.5), ("hook", frag("hook", 1, 2), "sting", 1.0), ("hook", frag("hook", 1, 2), "boom", 0.6), ("hook", frag("hook", 1, 2), "glitch", 0.5),
    *beats("hook", HK2, D["hook"] - HK2, 0.5, 0.8),
    # ยาย's porch: the sea, gulls, the cleaver on the coconut, the rule card
    *bed("waves", T("yai", 0), T("yai", -0.1), 0.22, 4.6), ("yai", 0.6, "gull", 0.3), ("yai", 5.2, "gull", 0.25), ("yai", 10.5, "gull", 0.2),
    *[("yai", 0.2 + k * 1.1, "thud", 0.3) for k in range(3)],
    *[x for o in (vo_t("yai", 0) + 0.2, frag("yai", 1, 2) + 0.1, vo_t("yai", 2) + 0.1) for x in (("yai", o, "page", 0.45), ("yai", o + 0.3, "pen", 0.5), ("yai", o + 0.35, "ding", 0.25))],
    ("yai", frag("yai", 1, 1), "sting", 0.5), ("yai", frag("yai", 1, 4), "sting", 0.7), ("yai", frag("yai", 1, 4), "boom", 0.35), ("yai", frag("yai", 2, 1), "sting", 0.5),
    *beats("yai", vo_t("yai", 1), D["yai"] - vo_t("yai", 1), 0.8, 0.3),
    # the boat: the longtail across the bay, the sign, then inside: the engine behind ลุงนวล, the slap of water
    *bed("longtail", T("boat", 0), T("boat", -0.1), 0.5, 4.2), *bed("waves", T("boat", 0), T("boat", -0.1), 0.16, 4.6), ("boat", 0.9, "page", 0.5), ("boat", 1.0, "slam", 0.35),
    ("boat", BT2, "whoosh", 0.4), ("boat", frag("boat", 1, 3), "sting", 0.6), ("boat", frag("boat", 1, 3), "boom", 0.3), *beats("boat", vo_t("boat", 1), D["boat"] - vo_t("boat", 1), 0.9, 0.25),
    # stranded: the squall — wind, thunder on the flashes, the sea getting up; the dead phone; his cheer
    *bed("wind", T("stranded", 0), T("stranded", -0.1), 0.4, 3.2), *bed("waves", T("stranded", 0), T("survive", -0.1), 0.3, 4.6),
    ("stranded", 0.5, "thunder", 0.7), ("stranded", 1.9, "thunder", 0.5), ("stranded", vo_t("stranded", 1) - 0.3 + 2.6, "thunder", 0.6),
    ("stranded", vo_t("stranded", 1) + 0.1, "beep", 0.3), ("stranded", vo_t("stranded", 1) + 0.6, "beep", 0.3), ("stranded", frag("stranded", 1, 2), "powerdown", 0.4),
    ("stranded", frag("stranded", 2, 1), "sting", 0.5), *beats("stranded", 0.0, D["stranded"], 0.75, 0.35),
    # survival: the lighter, the fire catching, the crackle; the coconut; the fronds; the checklist ticks
    ("survive", 0.1, "click", 0.7), ("survive", 0.35, "click", 0.7), ("survive", 0.6, "whoosh", 0.5), *bed("crackle", T("survive", 0.6), T("wait", -0.1), 0.3, 5.0),
    ("survive", 1.15, "whoosh", 0.3), ("survive", 1.4, "squelch", 0.4), ("survive", 2.3, "whoosh", 0.3), ("survive", 2.5, "rustle", 0.6), ("survive", 3.0, "rustle", 0.5),
    *[x for o in (2.4, 2.7, 3.2) for x in (("survive", o, "page", 0.4), ("survive", o + 0.25, "pen", 0.5), ("survive", o + 0.3, "ding", 0.3))], ("survive", vo_t("survive", 0) + 1.0, "page", 0.5), ("survive", frag("survive", 0, 1), "sting", 0.5),
    # the pool: it swims to him, the hands go in, the grunt as it blows up; the photo; the argument
    *bed("waves", T("fish", 0), T("fish", -0.1), 0.24, 4.6), ("fish", 1.6, "splash", 0.7), ("fish", 2.0, "squelch", 0.3), ("fish", vo_t("fish", 1) + 0.05, "squeak", 0.8), ("fish", vo_t("fish", 1) + 0.1, "pop", 0.5), ("fish", vo_t("fish", 1) + 0.15, "sting", 0.5),
    ("fish", FSH + vo_t("fish", 2) - FSH + 0.9, "shutter", 0.9), ("fish", FS3 + 0.1, "whoosh", 0.3), ("fish", vo_t("fish", 4), "sting", 0.4), *beats("fish", vo_t("fish", 3), D["fish"] - vo_t("fish", 3), 0.7, 0.4),
    # the grill: fat on the fire, the sign, the bite
    *bed("sizzle", T("grill", 0), T("grill", -0.1), 0.35, 2.6), *bed("waves", T("grill", 0), T("sig", -0.1), 0.14, 4.6), *bed("crickets", T("grill", 0), T("night", -0.1), 0.1, 4.0),
    ("grill", frag("grill", 0, 1), "page", 0.5), ("grill", frag("grill", 0, 1) + 0.3, "marker", 0.6), ("grill", frag("grill", 0, 1) + 0.35, "sting", 0.7), ("grill", frag("grill", 0, 1) + 0.35, "boom", 0.3),
    ("grill", vo_t("grill", 1) - 0.3, "squish", 0.5), *beats("grill", 0.0, D["grill"], 0.7, 0.45),
    # the wait: the clock, the lip, the stick on the sand; the poison climbs
    *[("wait", vo_t("wait", 0) + 0.1 + k * 0.19, "tick", 0.35) for k in range(10)], ("wait", vo_t("wait", 0) + 2.0, "ding", 0.3),
    ("wait", vo_t("wait", 1) - 0.2, "sting", 0.35), ("wait", vo_t("wait", 3) + 0.6, "thud", 0.6), ("wait", vo_t("wait", 3) + 0.62, "rustle", 0.3),
    ("wait", vo_t("wait", 4), "riser", 0.5), ("wait", frag("wait", 4, 4), "sting", 0.9), ("wait", frag("wait", 4, 4), "boom", 0.5),
    *beats("wait", 0.0, vo_t("wait", 1), 0.9, 0.3), *beats("wait", vo_t("wait", 1), D["wait"] - vo_t("wait", 1), 0.55, 0.7),
    # ผีอำ: he goes down; the cut inside his head — the world muffled; her tears
    ("phiam", 0.1, "thud", 0.8), ("phiam", 0.12, "rustle", 0.5), ("phiam", 0.1, "boom", 0.4), ("phiam", PA2, "whoosh", 0.4), ("phiam", PA2 + 0.05, "boom", 0.5),
    ("phiam", frag("phiam", 2, 3), "sting", 1.0), ("phiam", frag("phiam", 2, 3), "boom", 0.6), ("phiam", frag("phiam", 2, 3), "glitch", 0.4),
    *[("phiam", vo_t("phiam", 3) + o + 0.5, "drip", 0.6) for o in (0.2, 1.1, 2.0)], *beats("phiam", 0.0, D["phiam"], 0.5, 0.85),
    # the lamp: the creak of its wire out of the dark, steps on sand; her scream; ตาเมฆ
    *[("lamp", 0.2 + k * 0.5, "lamp", 0.5) for k in range(4)], *[("lamp", 0.35 + k * 0.52, "steps", 0.22) for k in range(4)],
    ("lamp", vo_t("lamp", 0) - 0.1, "sting", 0.9), ("lamp", vo_t("lamp", 0) - 0.1, "boom", 0.6), ("lamp", vo_t("lamp", 0) - 0.1, "glitch", 0.4),
    ("lamp", LP2, "whoosh", 0.3), ("lamp", frag("lamp", 1, 1), "sting", 0.6), ("lamp", frag("lamp", 2, 2), "sting", 0.7), ("lamp", frag("lamp", 3, 1), "sting", 0.7), ("lamp", frag("lamp", 3, 1), "boom", 0.35),
    ("lamp", vo_t("lamp", 3) + 1.3, "breath", 0.7), *beats("lamp", 0.0, D["lamp"], 0.6, 0.55),
    # the safety card
    *[x for o in (0.1, vo_t("card", 0) + 0.1, frag("card", 0, 1), frag("card", 0, 3)) for x in (("card", o, "page", 0.4), ("card", o + 0.3, "pen", 0.5), ("card", o + 0.35, "ding", 0.25))], ("card", frag("card", 0, 2), "ring", 0.35),
    # the night: her count, the breaths she gives, the compressions, the dying fire, the lamp; the moon
    *bed("waves", T("night", 0), T("night", -0.1), 0.2, 4.6),
    ("night", 2.1, "sting", 0.7), ("night", 2.1, "boom", 0.4), ("night", 2.3, "breath", 0.9), ("night", 3.8, "breath", 0.9), *[("night", 4.3 + k * 0.5, "thud", 0.5) for k in range(6)],
    ("night", 7.2, "sting", 0.6), ("night", 7.5, "breath", 0.9), ("night", 8.5, "gasp", 0.5), *beats("night", 0.0, D["night"], 0.52, 0.7),
    # the signature
    ("sig", 0.05, "page", 0.8), ("sig", 0.36, "thud", 0.25),
    *[x for o in (frag("sig", 0, 0) + 0.3, frag("sig", 0, 0) + 0.62, frag("sig", 0, 1) + 0.15) for x in (("sig", o, "pen", 0.9), ("sig", o + 0.05, "ding", 0.3))],
    ("sig", frag("sig", 0, 2) + 0.45, "marker", 0.45), *beats("sig", frag("sig", 0, 2), frag("sig", 0, 3) - frag("sig", 0, 2), 0.38, 0.8),
    *[("sig", frag("sig", 0, 2) + o, "tick", 0.55 + 0.1 * k) for k, o in enumerate((0.1, 0.42, 0.68, 0.88, 1.02, 1.12))],
    ("sig", frag("sig", 0, 3) - 1.1, "riser", 0.6),
    ("sig", frag("sig", 0, 3), "sting", 1.1), ("sig", frag("sig", 0, 3), "boom", 0.7), ("sig", frag("sig", 0, 3), "pen", 1.0), ("sig", frag("sig", 0, 3) + 0.1, "pen", 1.0),
    ("sig", frag("sig", 0, 3) + 0.24, "rip", 1.1), ("sig", frag("sig", 0, 3) + 0.86, "thud", 0.8), ("sig", frag("sig", 0, 3) + 0.86, "slam", 0.35),
    *beats("sig", frag("sig", 0, 3), D["sig"] - frag("sig", 0, 3), 0.5, 0.7),
    # dawn: gulls, the first breath, the longtail coming in, feet on sand; the empty beach; the lamp smoking on the shrine
    *bed("waves", T("dawn", 0), T("dawn", -0.1), 0.26, 4.6), ("dawn", 0.3, "gull", 0.35), ("dawn", 2.2, "gull", 0.3), ("dawn", 0.9, "gasp", 0.7), ("dawn", 1.3, "cough", 0.4), ("dawn", vo_t("dawn", 0) - 0.1, "sting", 0.4),
    *bed("longtail", T("dawn", DW2 - 0.6), T("dawn", DW3), 0.35, 4.2), *[("dawn", DW2 + 0.2 + k * 0.3, "steps", 0.4) for k in range(5)],
    ("dawn", frag("dawn", 1, 1), "sting", 0.8), ("dawn", frag("dawn", 1, 1), "boom", 0.4), ("dawn", DW2 + 1.9, "wash", 0.5),
    ("dawn", DW3, "whoosh", 0.35), ("dawn", frag("dawn", 2, 2), "sting", 0.9), ("dawn", frag("dawn", 2, 2), "boom", 0.5), ("dawn", frag("dawn", 2, 2) + 0.1, "glitch", 0.3),
    *beats("dawn", DW2, D["dawn"] - DW2, 0.55, 0.55),
    # the boat home: the engine, the sea; the one thing he says; black
    *bed("longtail", T("line", 0), T("line", -0.05), 0.4, 4.2), *bed("waves", T("line", 0), T("line", -0.05), 0.14, 4.6),
    ("line", frag("line", 0, 3), "sting", 1.0), ("line", frag("line", 0, 3), "boom", 0.6), ("line", frag("line", 0, 3) + 0.1, "glitch", 0.5), ("line", D["line"] - 1.25, "whoosh", 0.4), ("line", D["line"] - 1.2, "radio", 0.25),
    ("line", D["line"] - 0.08, "slam", 0.5), *beats("line", frag("line", 0, 1), D["line"] - frag("line", 0, 1), 0.5, 0.65),
    # the choice, then black
    *beats("choice", 0.0, D["choice"] - 0.3, 0.38, 1.0), *[("choice", 0.05 + k * 1.0, "tick", 1.0) for k in range(3)],
    ("choice", D["choice"] - 1.6, "riser", 0.8), ("choice", D["choice"] - 0.2, "sting", 1.0), ("choice", D["choice"] - 0.2, "boom", 0.7),
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
dip(T("yai", frag("yai", 1, 1)), T("yai", frag("yai", 1, 4) + 0.6), 0.4)
dip(T("wait", vo_t("wait", 3) - 0.2), T("wait", -0.05), 0.25)
dip(T("phiam", 0), T("phiam", -0.05), 0.12)                          # the world drops away while he cannot move
dip(T("lamp", 0), T("lamp", vo_t("lamp", 0) + 0.4), 0.2)
dip(T("lamp", vo_t("lamp", 1) - 0.2), T("lamp", -0.05), 0.3)
dip(T("night", 1.8), T("night", -0.05), 0.2)
dip(T("sig", frag("sig", 0, 2)), T("sig", frag("sig", 0, 3) + 0.05), 0.05, 0.12)
dip(T("dawn", 0), T("dawn", 1.8), 0.3)
dip(T("dawn", frag("dawn", 1, 1)), T("dawn", -0.05), 0.3)
dip(T("line", frag("line", 0, 1)), T("line", -0.05), 0.25)
dip(T("choice", 0), T("choice", -0.3), 0.5)
boost = np.ones(N, np.float32)  # the storm and the first scramble play with the music up
for a0, a1 in ((T("stranded", 0), T("stranded", -0.05)), (T("survive", 0), T("survive", -0.05))):
    boost += 0.3 * (np.clip((t - a0) / 0.3, 0, 1) * np.clip((a1 - t) / 0.2, 0, 1)).astype(np.float32)
mus = mus * gain * boost
end = int(T("line", -0.07) * SR)
mus[end:int(T("choice", 0.05) * SR)] = 0   # black and silence between the line and the choice
mus[int(T("choice", -0.2) * SR):] = 0       # hard cut to black and silence

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
SFX_GAIN_DB = -1.648   # the same absolute effects level as EP.6 (its de-hissed stem kept level(sfx, -27) of the v2 stem); not re-normalised per episode
mus = level(mus, -30)
sfx = sfx * 10 ** (SFX_GAIN_DB / 20)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mix = vo + mus * duck + sfx
gap0, gap1 = int(T("line", -0.07) * SR), int(T("choice", 0.05) * SR)   # black and silence between his line and the choice
mix[gap0 - 240:gap0] *= np.linspace(1, 0, 240)
mix[gap0:gap1] = 0
cut = int(T("choice", -0.2) * SR)
mix[cut - 240:cut] *= np.linspace(1, 0, 240)
mix[cut:] = 0  # black and silence after the choice: no end card, no goodbye
peak = np.max(np.abs(mix))
if peak > 0.98:
    mix = np.tanh(mix / peak * 1.2) * 0.95
out = os.path.join(HERE, "mix_raw.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", out],
               input=mix.astype(np.float32).tobytes(), check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)
print("mix written", TOTAL)

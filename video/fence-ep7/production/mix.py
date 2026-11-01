"""Build the episode soundtrack from schedule.json (เอาชีวิตรอด 99 วัน EP.7 เสียงเรียกฝูง): per-line levelled voice, synthesized SFX
(cicadas in the noon heat, the pickup and its last cough, footsteps on hot asphalt, the fall, water poured on cloth and the cardboard fan,
the lunge under the bridge, the station at dusk, the rifle, the radio) and the Suno music bed with dips and sidechain ducking under the voice.
Output -14 LUFS, hard cut to silence at the cliffhanger, only the end card's own sounds after it."""
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


# ---- voice: every line levelled on its own ----
LINE_GAIN = {"r01": -2, "g02": -1, "g03": -1, "w01": -2, "ph01": 0.5, "ph02": 0.5, "p02": 1.5, "pn01": 0.5, "s01": 0}
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


def growls(k, a, b, g=0.7, step=0.7):
    return [(k, a + i * step, "growl", g * (0.7 + 0.3 * (i % 2))) for i in range(int((b - a) / step))]


HK2 = vo_t("hook", 1) - 0.1          # the swarm flash on the headlights
CT2 = vo_t("count", 1) - 0.2         # the roof: ภู's rule, the lamp goes out
LT2 = vo_t("lights", 1) - 0.2        # the roof: the whispered rule
LA2 = vo_t("ladder", 1) - 0.2        # the guard lands on the roof
LR2 = vo_t("later", 1) - 0.4         # the radio close-up
CX = D["cliff"] - 1.4                # the cliff's punch; black at D - 0.08
T1 = frag("trucks", 0, 1) + 0.6      # the lights go out one by one

CUES = [
    # BEAT 0: the trucks' lights from the roof (engines up the road, crickets), the sting on "อย่าลงไป", the swarm flash, the growls
    *bed("crickets", T("hook", 0), T("count", CT2 + 0.5), 0.26, 5.0), *bed("engine", T("hook", 0), T("count", -0.1), 0.42, 4.0),
    ("hook", frag("hook", 1, 0), "sting", 0.9), ("hook", frag("hook", 1, 0), "boom", 0.4), ("hook", HK2, "whoosh", 0.45), ("hook", HK2 + 0.05, "glitch", 0.4),
    *growls("hook", frag("hook", 1, 2) - 0.2, D["hook"], 0.55, 0.6), *beats("hook", frag("hook", 1, 0), D["hook"] - frag("hook", 1, 0), 0.5, 0.6),
    # BEAT 1: the loudspeaker counts; rule two is for the dead (red); lights off, be still; the lamp goes out
    ("count", vo_t("count", 0) - 0.3, "static", 0.5), ("count", vo_t("count", 0) - 0.25, "trumpet", 0.5), ("count", vo_t("count", 0) - 0.2, "radio", 0.45),
    ("count", frag("count", 0, 2), "sting", 0.5), ("count", vo_t("count", 1) - 0.1, "page", 0.5), ("count", frag("count", 1, 2), "sting", 0.85), ("count", frag("count", 1, 2), "slam", 0.6), ("count", frag("count", 1, 2), "boom", 0.45),
    *[x for o in (frag("count", 1, 2) + 0.9, frag("count", 1, 2) + 1.3) for x in (("count", o, "pop", 0.45), ("count", o + 0.2, "pen", 0.5))], ("count", frag("count", 1, 2) + 1.3, "click", 0.6), ("count", frag("count", 1, 2) + 1.35, "powerdown", 0.35),
    *beats("count", 0.0, D["count"], 0.6, 0.45),
    # BEAT 2: the dark (the engines idle below, the wind), the adapted eye
    *bed("engine", T("dark", 0), T("dark", -0.1), 0.3, 4.0), *bed("wind", T("dark", 0), T("dark", -0.1), 0.15, 3.2), ("dark", 0.2, "swell", 0.45), ("dark", frag("dark", 0, 1), "sting", 0.5), *beats("dark", 0.0, D["dark"], 0.75, 0.4),
    # BEAT 3: what followed the engines arrives before ten (red): the roar, the beam swings, the men's shriek
    *bed("engine", T("arrive", 0), T("trucks", T1 + 1.1), 0.45, 4.0), *growls("arrive", 0.0, D["arrive"], 0.8, 0.5),
    ("arrive", frag("arrive", 0, 1), "roar", 1.0), ("arrive", frag("arrive", 0, 1), "boom", 0.6), ("arrive", frag("arrive", 0, 1) + 0.05, "glitch", 0.5), ("arrive", frag("arrive", 0, 1) + 0.25, "whoosh", 0.5), ("arrive", frag("arrive", 0, 1) + 0.5, "shriek", 0.35), ("arrive", frag("arrive", 0, 1) + 0.6, "scream", 0.3),
    *beats("arrive", 0.0, D["arrive"], 0.42, 0.85),
    # BEAT 4: every torch turns to them, they turn to every torch (the lunge); on the roof, the whispered rule
    *growls("lights", 0.0, LT2, 0.85, 0.45), ("lights", 0.6, "whoosh", 0.45), ("lights", 1.4, "whoosh", 0.45), ("lights", 2.0, "steps", 0.4), ("lights", frag("lights", 0, 1), "sting", 0.9), ("lights", frag("lights", 0, 1), "boom", 0.5), ("lights", frag("lights", 0, 1) + 1.5, "roar", 0.8), ("lights", frag("lights", 0, 1) + 1.5, "slam", 0.5),
    *bed("crickets", T("lights", LT2), T("ladder", LA2), 0.2, 5.0), *growls("lights", LT2, D["lights"], 0.4, 0.7), ("lights", frag("lights", 1, 1), "sting", 0.5), ("lights", frag("lights", 1, 1), "ding", 0.3),
    *beats("lights", 0.0, LT2, 0.42, 0.85), *beats("lights", LT2, D["lights"] - LT2, 0.45, 0.7),
    # BEAT 5: the ladder: the rungs, the claws, the pull over the edge; "เพราะเรานับได้หก"
    *[("ladder", o, "clang", 0.45) for o in (0.6, 1.1, 1.6, 2.1)], *growls("ladder", 0.0, LA2, 0.8, 0.5), ("ladder", frag("ladder", 0, 1), "sting", 0.6), ("ladder", 2.3, "rustle", 0.45), ("ladder", 2.5, "roar", 0.85), ("ladder", 2.5, "boom", 0.4),
    ("ladder", LA2 + 0.1, "thud", 0.6), ("ladder", LA2 + 0.3, "gasp", 0.5), ("ladder", LA2 + 0.9, "breath", 0.5), *growls("ladder", LA2, D["ladder"], 0.4, 0.7), ("ladder", vo_t("ladder", 2) - 0.1, "page", 0.4), ("ladder", vo_t("ladder", 2), "sting", 0.7), ("ladder", vo_t("ladder", 2) + 0.4, "ding", 0.4),
    *beats("ladder", 0.0, LA2, 0.42, 0.85), *beats("ladder", LA2, D["ladder"] - LA2, 0.5, 0.6),
    # BEAT 6: the swarm takes the trucks (red): everything a horde wants; the lights die one by one; the engines die
    *growls("trucks", 0.0, T1 + 1.5, 0.9, 0.4), ("trucks", 0.25, "roar", 1.0), ("trucks", 0.25, "boom", 0.8), ("trucks", 0.3, "glitch", 0.6), ("trucks", 0.3, "slam", 0.6), ("trucks", 0.8, "scream", 0.35), ("trucks", 1.0, "shatter", 0.6), ("trucks", 1.6, "scream", 0.3),
    ("trucks", frag("trucks", 0, 1), "sting", 0.9), ("trucks", frag("trucks", 0, 1), "boom", 0.5), ("trucks", T1, "click", 0.6), ("trucks", T1 + 1.1, "click", 0.6), ("trucks", T1 + 1.1, "powerdown", 0.7),
    *growls("trucks", T1 + 1.5, D["trucks"], 0.5, 0.6), *beats("trucks", 0.0, D["trucks"], 0.42, 0.85),
    # BEAT 7: dawn: no trucks, no lights, no sound; the guard's lie; เจ๊หงส์'s message
    *bed("cicada", T("dawn", 0), T("rule6", -0.1), 0.35, 5.0), *bed("wind", T("dawn", 0), T("rule6", -0.1), 0.15, 3.2), ("dawn", 0.5, "gull", 0.25), ("dawn", frag("dawn", 0, 2), "sting", 0.45),
    ("dawn", vo_t("dawn", 1) - 0.4, "steps", 0.35), ("dawn", frag("dawn", 1, 1), "sting", 0.6), ("dawn", frag("dawn", 2, 1), "pop", 0.35), ("dawn", frag("dawn", 2, 1) + 0.05, "ding", 0.35), *beats("dawn", 0.0, D["dawn"], 0.8, 0.3),
    # BEAT 8: rule six on the wall (red)
    ("rule6", frag("rule6", 0, 1) - 0.1, "page", 0.6), ("rule6", frag("rule6", 0, 1), "marker", 0.5), ("rule6", frag("rule6", 0, 2), "slam", 0.6), ("rule6", frag("rule6", 0, 2), "sting", 0.8), ("rule6", frag("rule6", 0, 2), "boom", 0.4), *beats("rule6", 0.0, D["rule6"], 0.7, 0.35),
    # BEAT 9: twenty days later (rain), the radio counts them as nought (red); "ดี" (the false safety)
    *bed("rain", T("later", 0), T("cliff", -0.1), 0.4, 4.0), ("later", 0.6, "thunder", 0.3), ("later", frag("later", 0, 1), "page", 0.5), ("later", frag("later", 0, 1) + 0.25, "pen", 0.5), ("later", frag("later", 0, 1) + 0.5, "ding", 0.3),
    ("later", vo_t("later", 1) - 0.2, "static", 0.5), ("later", vo_t("later", 1) - 0.15, "radio", 0.6), *bed("radiobed", T("later", vo_t("later", 1) - 0.15), T("later", vo_end("later", 1) + 0.2), 0.3, 3.0),
    ("later", frag("later", 1, 1), "page", 0.5), ("later", frag("later", 1, 1), "rip", 0.4), ("later", frag("later", 1, 2), "sting", 0.85), ("later", frag("later", 1, 2), "glitch", 0.5), ("later", frag("later", 1, 2), "boom", 0.4),
    ("later", frag("later", 2, 1), "ding", 0.4), *beats("later", vo_t("later", 1), D["later"] - vo_t("later", 1), 0.6, 0.45),
    # BEAT 10: the cliff: the storm, more of them than ever below the roof; the question; black
    ("cliff", 0.3, "thunder", 0.5), ("cliff", 4.0, "thunder", 0.45), *growls("cliff", 0.0, CX, 0.5, 0.7), ("cliff", frag("cliff", 0, 2), "sting", 0.7), ("cliff", CX, "roar", 0.9), ("cliff", CX, "boom", 0.8), ("cliff", CX, "slam", 0.6), ("cliff", CX + 0.05, "glitch", 0.5),
    *beats("cliff", 0.0, CX, 0.45, 0.8),
    ("sig", 0.05, "page", 0.8), ("sig", 0.36, "thud", 0.25),
    *[x for o in (frag("sig", 0, 0) + 0.3, frag("sig", 0, 0) + 0.62, frag("sig", 0, 1) + 0.15) for x in (("sig", o, "pen", 0.9), ("sig", o + 0.05, "ding", 0.3))],
    ("sig", frag("sig", 0, 2) + 0.45, "marker", 0.45), *beats("sig", frag("sig", 0, 2), frag("sig", 0, 3) - frag("sig", 0, 2), 0.38, 0.8),
    *[("sig", frag("sig", 0, 2) + o, "tick", 0.55 + 0.1 * k) for k, o in enumerate((0.1, 0.42, 0.68, 0.88, 1.02, 1.12))],
    ("sig", frag("sig", 0, 3) - 1.1, "riser", 0.6),
    ("sig", frag("sig", 0, 3), "sting", 1.1), ("sig", frag("sig", 0, 3), "boom", 0.7), ("sig", frag("sig", 0, 3), "pen", 1.0), ("sig", frag("sig", 0, 3) + 0.1, "pen", 1.0),
    ("sig", frag("sig", 0, 3) + 0.24, "rip", 1.1), ("sig", frag("sig", 0, 3) + 0.86, "thud", 0.8), ("sig", frag("sig", 0, 3) + 0.86, "slam", 0.35),
    *beats("sig", frag("sig", 0, 3), D["sig"] - frag("sig", 0, 3), 0.5, 0.7),
    # ตอนที่ 8: the card slaps on, the tease, the CTA
    ("next", 0.1, "page", 0.8), ("next", 0.45, "slam", 0.5), ("next", 0.6, "sting", 0.6), ("next", 1.5, "pop", 0.4), ("next", 2.4, "pop", 0.4), ("next", 2.45, "ding", 0.3),
]
cues = {"duration": TOTAL, "sections": [{"start": 0, "end": TOTAL, "mood": "silence"}],
        "sfx": [{"t": round(t if k is None else T(k, t), 3), "type": typ, "gain": g} for k, t, typ, g in CUES]}
json.dump(cues, open(os.path.join(HERE, "sfx_cues.json"), "w"))
subprocess.run(["python3", os.path.join(HERE, "..", "synth.py"), os.path.join(HERE, "sfx_cues.json"), os.path.join(HERE, "sfx.wav")],
               check=True, env={**os.environ, "STEMS": "1"})
sfx = load(os.path.join(HERE, "sfx_sfx.wav"))[:N]
sfx = np.pad(sfx, (0, N - len(sfx)))

# ---- music with horror dips: the reference drops ~10 dB before the twist ----
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
dip(T("count", CT2), T("dark", -0.05), 0.4)              # the roof whispers and the dark
dip(T("lights", LT2), T("lights", -0.05), 0.4)           # the whispered rule
dip(T("later", vo_t("later", 1) - 0.2), T("later", vo_end("later", 1) + 0.2), 0.2)
dip(T("cliff", 0), T("cliff", vo_t("cliff", 0) + 0.4), 0.3, 0.6)   # the drop before the question
dip(T("sig", frag("sig", 0, 2)), T("sig", frag("sig", 0, 3) + 0.05), 0.05, 0.12)
boost = np.ones(N, np.float32)  # the action plays with the music up
for a0, a1 in ((T("arrive", 0), T("lights", LT2 - 0.1)), (T("trucks", 0), T("trucks", T1 + 1.1)), (T("cliff", CX - 0.2), T("cliff", -0.1))):
    boost += 0.4 * (np.clip((t - a0) / 0.3, 0, 1) * np.clip((a1 - t) / 0.2, 0, 1)).astype(np.float32)
mus = mus * gain * boost
end = int(T("cliff", -0.08) * SR)
mus[end:int(T("sig", 0) * SR)] = 0  # the cliffhanger cuts to black and silence until the signature

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mix = vo + mus * duck + sfx
cut, back = int(T("cliff", -0.08) * SR), int(T("sig", 0.0) * SR)
mix[cut - 240:cut] *= np.linspace(1, 0, 240)
mix[cut:back] = 0  # a beat of black and silence after the cliffhanger
mix[int(T("end", 0.0) * SR):] = 0
peak = np.max(np.abs(mix))
if peak > 0.98:
    mix = np.tanh(mix / peak * 1.2) * 0.95
out = os.path.join(HERE, "mix_raw.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", out],
               input=mix.astype(np.float32).tobytes(), check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)
print("mix written", TOTAL)

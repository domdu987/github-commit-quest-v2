"""Build the episode soundtrack from schedule.json (เอาชีวิตรอด 99 วัน EP.5): per-line levelled voice, synthesized SFX
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
LINE_GAIN = {"r01": -2, "g01": -1, "g02": -1, "g03": -1, "w01": -2, "ph03": 0.5, "ph04": 0.5, "s01": 0}
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


HK2 = vo_t("hook", 2) - 0.1          # the cut to the torch on ภู
DY2 = vo_t("days", 1) - 0.15         # the second roof framing
TW2 = vo_t("twist", 0) - 0.1; TW3 = vo_t("twist", 2) + 1.2   # the twist's three framings

CUES = [
    # BEAT 0: the lamp-lit nest (crickets, the lamp), the sting on "คนของอีกฝ่าย", the torch on ภู
    *bed("crickets", T("hook", 0), T("refuse", -0.1), 0.32, 5.0), *bed("hum", T("hook", 0), T("refuse", -0.1), 0.1, 3.0),
    ("hook", vo_t("hook", 1), "sting", 0.9), ("hook", vo_t("hook", 1), "boom", 0.4), ("hook", HK2, "whoosh", 0.4), ("hook", HK2 + 0.05, "click", 0.5), *beats("hook", vo_t("hook", 1), D["hook"] - vo_t("hook", 1), 0.5, 0.6),
    # BEAT 1: the offer; the one rule slams in red; the name
    ("deal", 0.2, "creak", 0.4), ("deal", frag("deal", 1, 1) - 0.05, "page", 0.5), ("deal", frag("deal", 1, 1), "slam", 0.6), ("deal", frag("deal", 1, 1), "sting", 0.8), *beats("deal", vo_t("deal", 1), D["deal"] - vo_t("deal", 1), 0.75, 0.35),
    # BEAT 2: the confession; the second number counts up on the HUD
    ("who", frag("who", 0, 1), "sting", 0.8), ("who", frag("who", 0, 1), "glitch", 0.4), ("who", frag("who", 0, 2), "page", 0.5), ("who", frag("who", 0, 2) + 0.25, "pen", 0.5), ("who", frag("who", 0, 2) + 0.3, "ding", 0.3), *beats("who", frag("who", 0, 1), D["who"] - frag("who", 0, 1), 0.65, 0.4),
    ("count", frag("count", 0, 1), "page", 0.5), ("count", frag("count", 0, 1) + 0.2, "rip", 0.45), ("count", frag("count", 0, 2), "sting", 0.6), ("count", 1.5, "thunder", 0.3), ("count", frag("count", 1, 1) - 0.05, "page", 0.5), ("count", frag("count", 1, 1), "slam", 0.6), ("count", frag("count", 1, 1), "sting", 0.8), ("count", frag("count", 1, 1), "boom", 0.4),
    *beats("count", 0.0, D["count"], 0.6, 0.45),
    ("refuse", frag("refuse", 0, 1), "sting", 0.5), ("refuse", vo_t("refuse", 1) - 0.3, "steps", 0.4), ("refuse", vo_t("refuse", 1) - 0.1, "clang", 0.35), ("refuse", frag("refuse", 1, 1), "sting", 0.8), ("refuse", frag("refuse", 1, 1), "boom", 0.4), *beats("refuse", 0.0, D["refuse"], 0.6, 0.45),
    # BEAT 3: morning, the five rules tick in; the movies' verdict (three slams)
    *bed("cicada", T("rules", 0), T("rules", -0.1), 0.35, 5.0), *bed("wind", T("rules", 0), T("rules", -0.1), 0.15, 3.2), ("rules", 0.4, "gull", 0.25),
    ("rules", vo_t("rules", 1) - 0.1, "page", 0.6), *[x for o in (frag("rules", 1, 0) + 0.1, frag("rules", 1, 1) + 0.1, frag("rules", 1, 1) + 0.9, frag("rules", 1, 1) + 1.5, frag("rules", 1, 2) + 0.1) for x in (("rules", o, "pop", 0.45), ("rules", o + 0.25, "pen", 0.5), ("rules", o + 0.3, "ding", 0.3))],
    *bed("crickets", T("movie", 0), T("movie", -0.1), 0.25, 5.0), ("movie", frag("movie", 0, 2) - 0.15, "page", 0.6), *[("movie", o, "slam", 0.5) for o in (frag("movie", 0, 2) - 0.1, frag("movie", 0, 2) + 0.35, (frag("movie", 0, 2) + 0.8) + 0.1)], *[("movie", o + 0.1, "marker", 0.4) for o in (frag("movie", 0, 2) - 0.1, frag("movie", 0, 2) + 0.35, (frag("movie", 0, 2) + 0.8) + 0.1)],
    ("movie", (frag("movie", 0, 2) + 0.8), "sting", 0.7), *beats("movie", 0.0, D["movie"], 0.7, 0.35),
    # BEAT 4: ten days later (cicadas, the can, the counters), the radio, "เป็นเดือน"
    *bed("cicada", T("days", 0), T("days", -0.1), 0.35, 5.0), *bed("wind", T("days", 0), T("days", -0.1), 0.15, 3.2), *[("days", 0.4 + k * 1.2, "cans", 0.4) for k in range(3)], ("days", frag("days", 0, 1), "page", 0.5), ("days", frag("days", 0, 1) + 0.25, "pen", 0.5), ("days", frag("days", 0, 2) + 0.1, "ding", 0.3),
    ("days", vo_t("days", 1) + 0.2, "canfall", 0.45), ("days", vo_t("days", 1) + 0.3, "page", 0.5), ("days", vo_t("days", 1) + 0.6, "pen", 0.5),
    ("radio", vo_t("radio", 0) - 0.2, "static", 0.5), ("radio", vo_t("radio", 0) - 0.15, "radio", 0.6), *bed("radiobed", T("radio", vo_t("radio", 0) - 0.15), T("radio", vo_end("radio", 0) + 0.2), 0.3, 3.0), ("radio", frag("radio", 0, 1), "page", 0.5), ("radio", frag("radio", 0, 1), "rip", 0.4), ("radio", frag("radio", 0, 2), "sting", 0.7),
    ("radio", frag("radio", 1, 1), "ding", 0.4), *beats("radio", vo_t("radio", 0), D["radio"] - vo_t("radio", 0), 0.6, 0.45),
    # BEAT 5: the drop; the engines up the road, the horn, the loudspeaker crackle; the fields growl; the lunge; black
    *bed("crickets", T("twist", 0), T("twist", TW2 + 1.0), 0.28, 5.0), ("twist", 0.2, "swell", 0.5),
    ("twist", TW2 + 0.2, "riser", 0.5), *bed("engine", T("twist", TW2 + 0.2), T("twist", -0.1), 0.5, 4.0), ("twist", vo_t("twist", 0) + 0.6, "trumpet", 0.55), ("twist", vo_t("twist", 1) - 0.3, "static", 0.5), ("twist", vo_t("twist", 1) - 0.25, "radio", 0.4),
    ("twist", frag("twist", 1, 1), "sting", 0.9), ("twist", frag("twist", 1, 1), "boom", 0.5), ("twist", frag("twist", 1, 1), "glitch", 0.5), ("twist", frag("twist", 2, 1), "sting", 0.5),
    *growls("twist", TW3 + 0.2, D["twist"] - 0.9, 0.75, 0.42), ("twist", frag("twist", 2, 2), "sting", 0.8), ("twist", D["twist"] - 0.8, "roar", 1.0), ("twist", D["twist"] - 0.8, "boom", 0.8), ("twist", D["twist"] - 0.8, "glitch", 0.6), ("twist", D["twist"] - 0.75, "slam", 0.6),
    *beats("twist", 0.0, D["twist"] - 0.8, 0.42, 0.85),
    ("sig", 0.05, "page", 0.8), ("sig", 0.36, "thud", 0.25),
    *[x for o in (frag("sig", 0, 0) + 0.3, frag("sig", 0, 0) + 0.62, frag("sig", 0, 1) + 0.15) for x in (("sig", o, "pen", 0.9), ("sig", o + 0.05, "ding", 0.3))],
    ("sig", frag("sig", 0, 2) + 0.45, "marker", 0.45), *beats("sig", frag("sig", 0, 2), frag("sig", 0, 3) - frag("sig", 0, 2), 0.38, 0.8),
    *[("sig", frag("sig", 0, 2) + o, "tick", 0.55 + 0.1 * k) for k, o in enumerate((0.1, 0.42, 0.68, 0.88, 1.02, 1.12))],
    ("sig", frag("sig", 0, 3) - 1.1, "riser", 0.6),
    ("sig", frag("sig", 0, 3), "sting", 1.1), ("sig", frag("sig", 0, 3), "boom", 0.7), ("sig", frag("sig", 0, 3), "pen", 1.0), ("sig", frag("sig", 0, 3) + 0.1, "pen", 1.0),
    ("sig", frag("sig", 0, 3) + 0.24, "rip", 1.1), ("sig", frag("sig", 0, 3) + 0.86, "thud", 0.8), ("sig", frag("sig", 0, 3) + 0.86, "slam", 0.35),
    *beats("sig", frag("sig", 0, 3), D["sig"] - frag("sig", 0, 3), 0.5, 0.7),
    # ตอนที่ 7: the card slaps on, the tease, the CTA
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
dip(T("who", frag("who", 0, 1) - 0.3), T("count", -0.05), 0.4)
dip(T("refuse", vo_t("refuse", 1) - 0.3), T("refuse", -0.05), 0.4)
dip(T("radio", vo_t("radio", 0) - 0.2), T("radio", vo_end("radio", 0) + 0.2), 0.2)
dip(T("twist", 0), T("twist", TW2 + 0.3), 0.3, 0.6)   # the drop before the twist
dip(T("sig", frag("sig", 0, 2)), T("sig", frag("sig", 0, 3) + 0.05), 0.05, 0.12)
boost = np.ones(N, np.float32)  # the action plays with the music up
for a0, a1 in ((T("twist", TW2 + 0.5), T("twist", -0.1)),):
    boost += 0.4 * (np.clip((t - a0) / 0.3, 0, 1) * np.clip((a1 - t) / 0.2, 0, 1)).astype(np.float32)
mus = mus * gain * boost
end = int(T("twist", -0.08) * SR)
mus[end:int(T("sig", 0) * SR)] = 0  # the cliffhanger cuts to black and silence until the signature

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mix = vo + mus * duck + sfx
cut, back = int(T("twist", -0.08) * SR), int(T("sig", 0.0) * SR)
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

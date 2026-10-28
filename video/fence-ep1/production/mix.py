"""Build the episode soundtrack from schedule.json (วันที่ 100 EP.1): per-line levelled voice, synthesized SFX
(chalk on the board, cicadas at noon, the can dropping, the horde, the gate on its rail, the sickle, the radio waking,
the ledger page) and the Suno music bed with dips before the scares and sidechain ducking under the voice.
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


# ---- voice: every line levelled on its own so shouts and the child's line sit at a readable loudness ----
LINE_GAIN = {"r01": -2, "d05": -1, "d06": -1, "d08": -1}
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


CUES = [
    # cold open: the lid creaks, the child's hand, the "no" — heartbeat under it all
    *bed("wind", T("open", 0), T("open", -0.1), 0.45, 3.2), ("open", 0.9, "slam", 0.45), ("open", 1.3, "riser", 0.7), ("open", -0.25, "whoosh", 0.9),
    ("hook", 0.2, "creak", 0.35), ("hook", frag("hook", 1, 1), "sting", 0.7), ("hook", frag("hook", 1, 1), "creak", 0.5),
    ("hook", vo_t("hook", 2), "sting", 1.0), ("hook", vo_t("hook", 2), "boom", 0.6), ("hook", vo_t("hook", 2), "glitch", 0.5), ("hook", frag("hook", 2, 1), "slam", 0.5),
    *beats("hook", 0.3, D["hook"] - 0.3, 0.55, 0.6), ("hook", -0.25, "whoosh", 0.8),
    # the board: chalk, then the yard
    ("chapter", 0.05, "chalk", 0.9), ("chapter", 0.4, "rustle", 0.5), ("chapter", 0.5, "chalk", 0.8), ("chapter", 1.1, "tick", 0.3), ("chapter", 1.2, "tick", 0.3), ("chapter", 1.3, "tick", 0.3), ("chapter", 1.4, "tick", 0.3), ("chapter", 1.5, "tick", 0.3), ("chapter", 1.6, "chalk", 0.7),
    *bed("wind", T("yard", 0), T("rules", 0), 0.25, 3.2), ("yard", 0.1, "crayon", 0.5), *[("yard", frag("yard", 0, 1) + 0.2 * k, "ding", 0.35) for k in range(5)],
    ("yard", frag("yard", 0, 2), "whoosh", 0.5), *[("yard", frag("yard", 0, 2) + 0.15 + 0.22 * k, "pop", 0.5) for k in range(4)],
    ("rules", 0.1, "chalk", 0.6), ("rules", frag("rules", 0, 1) - 0.05, "chalk", 0.6), ("rules", frag("rules", 0, 2) - 0.05, "chalk", 0.6), *[("rules", frag("rules", 0, k), "ding", 0.4) for k in range(3)],
    # noon and dusk on the road
    *bed("cicada", T("noon", 0), T("noon", -0.1), 0.9, 4.6), ("noon", 0.3, "growl", 0.35), ("noon", 1.8, "growl", 0.3),
    *bed("wind", T("dusk", 0), T("dusk", -0.1), 0.3, 3.2), ("dusk", frag("dusk", 0, 1) - 0.1, "shriek", 0.8), ("dusk", frag("dusk", 0, 1), "sting", 0.8), ("dusk", frag("dusk", 0, 1), "steps", 0.7), ("dusk", frag("dusk", 0, 1) + 0.6, "steps", 0.6), *beats("dusk", frag("dusk", 0, 1), D["dusk"] - frag("dusk", 0, 1), 0.4, 0.6),
    # the ledger, the gate
    ("ledger", 0.1, "page", 0.5), ("ledger", vo_t("ledger", 1), "marker", 0.3), ("ledger", frag("ledger", 1, 1) + 0.6, "buzz", 0.5), ("ledger", frag("ledger", 1, 1) + 0.6, "sting", 0.5),
    *bed("wind", T("gate", 0), T("gate", -0.1), 0.25, 3.2), ("gate", 0.3, "gate", 0.5), ("gate", 0.4, "steps", 0.3), ("gate", D["gate"] - 0.6, "steps", 0.35), ("gate", 0.35, "tick", 0.4),
    # the market: dust and drips, the vendor breathing, cans into the bag, then the one that falls
    *bed("wind", T("market", 0), T("clatter", -0.1), 0.18, 3.2), ("market", 0.4, "drip", 0.4), ("market", 2.2, "drip", 0.35), ("market", 0.6, "zbreath", 0.35), ("market", 2.6, "zbreath", 0.3), *[("market", vo_t("market", 1) + 0.2 * k, "tick", 0.3) for k in range(11)],
    *beats("market", 0.0, vo_t("market", 1), 0.8, 0.3),
    ("clatter", 0.05, "canfall", 1.2), ("clatter", 0.33, "cans", 0.6), ("clatter", 0.5, "sniff", 0.8), ("clatter", 1.1, "growl", 0.8), ("clatter", frag("clatter", 0, 1), "sting", 0.9), ("clatter", frag("clatter", 0, 1), "glitch", 0.5), ("clatter", frag("clatter", 0, 1), "boom", 0.4), *beats("clatter", 0.4, D["clatter"] - 0.4, 0.45, 0.7),
    # action: the lunge, the shelf, the run
    ("lunge", 0.05, "shriek", 1.0), ("lunge", 0.35, "sting", 0.9), ("lunge", 0.35, "glitch", 0.4), ("lunge", 0.5, "steps", 0.8), ("lunge", 0.9, "steps", 0.9), *beats("lunge", 0.0, D["lunge"], 0.35, 0.7),
    ("shelf", 0.32, "clang", 0.9), ("shelf", 0.32, "cans", 1.3), ("shelf", 0.6, "cans", 0.8), ("shelf", 0.5, "shriek", 0.8), ("shelf", 0.95, "steps", 0.9), *beats("shelf", 0.0, D["shelf"], 0.35, 0.8),
    ("run", 0.0, "steps", 1.0), ("run", 0.55, "steps", 1.0), ("run", 1.1, "steps", 0.9), ("run", 0.1, "riser", 0.6), ("run", -0.3, "buzz", 0.4), *beats("run", 0.0, D["run"], 0.3, 0.7),
    ("road", 0.0, "steps", 0.8), ("road", 0.7, "steps", 0.8), ("road", 1.4, "steps", 0.8), ("road", 2.1, "steps", 0.8), ("road", 2.8, "steps", 0.8), *growls("road", 0.3, D["road"], 0.6, 0.6), ("road", frag("road", 1, 1), "shriek", 0.9), ("road", frag("road", 1, 1), "sting", 0.9), ("road", frag("road", 1, 1), "boom", 0.5), *beats("road", 0.0, D["road"], 0.38, 0.75),
    # the gate action
    ("bolt", 0.5, "latch", 0.9), ("bolt", 0.55, "creak", 0.6), ("bolt", D["bolt"] - 0.45, "gate", 0.9), *bed("horde", T("bolt", 0), T("slam", -0.1), 0.6, 4.6), *growls("bolt", 0.0, D["bolt"], 0.5, 0.6), *beats("bolt", 0.0, D["bolt"], 0.35, 0.8),
    ("snag", 0.3, "thud", 0.8), ("snag", 0.9, "sting", 0.9), ("snag", 0.9, "rustle", 0.9), ("snag", 0.95, "shriek", 0.9), *growls("snag", 0.0, D["snag"], 0.7, 0.45), *beats("snag", 0.0, D["snag"], 0.33, 0.85),
    ("cut", 0.4, "whoosh", 0.6), ("cut", 0.55, "sickle", 1.2), ("cut", 0.55, "clang", 0.7), ("cut", 0.6, "cans", 1.0), ("cut", 0.7, "shriek", 0.8), *beats("cut", 0.0, D["cut"], 0.33, 0.85),
    *growls("gateTop", 0.0, D["gateTop"], 0.8, 0.3), ("gateTop", 0.2, "gate", 0.8), ("gateTop", 0.0, "rustle", 0.6), *beats("gateTop", 0.0, D["gateTop"], 0.33, 0.85),
    ("slam", 0.2, "gate", 1.0), ("slam", 0.5, "slam", 1.3), ("slam", 0.5, "boom", 0.6), ("slam", 0.75, "latch", 1.0), *growls("slam", 0.0, D["slam"], 0.7, 0.4), ("slam", 1.2, "shriek", 0.6), *beats("slam", 0.0, D["slam"], 0.4, 0.8),
    # the desk at night: crickets outside, the count, the small hand, the "no"
    *bed("crickets", T("cans", 0), T("real", -0.1), 0.6, 4.6), ("cans", frag("cans", 0, 1) + 0.5, "buzz", 0.5), ("cans", frag("cans", 0, 1) + 0.5, "sting", 0.5), ("cans", frag("cans", 1, 1), "sting", 0.7), ("cans", frag("cans", 1, 1), "creak", 0.5), *beats("cans", vo_t("cans", 1), D["cans"] - vo_t("cans", 1), 0.6, 0.45),
    ("reach", 0.4, "rustle", 0.5), *beats("reach", vo_t("reach", 1), D["reach"] - vo_t("reach", 1), 0.4, 0.7), ("reach", -0.3, "riser", 0.5),
    ("stop", 0.06, "slam", 0.6), ("stop", 0.06, "sting", 0.9), ("stop", 0.1, "canfall", 1.0), *beats("stop", 0.0, D["stop"], 0.45, 0.6),
    ("signs", frag("signs", 0, 0) + 0.45, "buzz", 0.5), ("signs", frag("signs", 0, 0) + 1.25, "buzz", 0.5), ("signs", frag("signs", 0, 1) + 0.45, "buzz", 0.5), ("signs", frag("signs", 0, 2), "sting", 0.6),
    ("toxin", frag("toxin", 0, 1), "pop", 0.5), ("toxin", frag("toxin", 1, 1), "sting", 1.0), ("toxin", frag("toxin", 1, 1), "boom", 0.6), ("toxin", frag("toxin", 1, 1), "glitch", 0.5), *beats("toxin", vo_t("toxin", 1), D["toxin"] - vo_t("toxin", 1), 0.45, 0.6),
    ("real", frag("real", 0, 1), "ding", 0.5), ("real", frag("real", 0, 1) + 0.6, "thud", 0.5), ("real", frag("real", 0, 2) + 0.3, "buzz", 0.4),
    *bed("crickets", T("three", 0), T("sig", -0.1), 0.5, 4.6), *bed("horde", T("three", 0), T("three", -0.1), 0.7, 4.6), *growls("three", 0.4, D["three"], 0.35, 0.9), ("three", frag("three", 0, 1), "sting", 0.7), ("three", frag("three", 0, 1), "boom", 0.4), *beats("three", frag("three", 0, 1), D["three"] - frag("three", 0, 1), 0.5, 0.6),
    # the signature
    # the sheet slaps on and is taped; a red pen ticks each line (with a soft ding); a marker circles the ???
    ("sig", 0.05, "page", 0.8), ("sig", 0.36, "thud", 0.25),
    *[x for o in (frag("sig", 0, 0) + 0.3, frag("sig", 0, 0) + 0.62, frag("sig", 0, 1) + 0.15) for x in (("sig", o, "pen", 0.9), ("sig", o + 0.05, "ding", 0.3))],
    ("sig", frag("sig", 0, 2) + 0.45, "marker", 0.45), *beats("sig", frag("sig", 0, 2), frag("sig", 0, 3) - frag("sig", 0, 2), 0.38, 0.8),
    *[("sig", frag("sig", 0, 2) + o, "tick", 0.55 + 0.1 * k) for k, o in enumerate((0.1, 0.42, 0.68, 0.88, 1.02, 1.12))],
    ("sig", frag("sig", 0, 3) - 1.1, "riser", 0.6),
    # "ข้อเดียว": two red slashes, the page tears across, the strip drops, a stamp hits what is left
    ("sig", frag("sig", 0, 3), "sting", 1.1), ("sig", frag("sig", 0, 3), "boom", 0.7), ("sig", frag("sig", 0, 3), "pen", 1.0), ("sig", frag("sig", 0, 3) + 0.1, "pen", 1.0),
    ("sig", frag("sig", 0, 3) + 0.24, "rip", 1.1), ("sig", frag("sig", 0, 3) + 0.86, "thud", 0.8), ("sig", frag("sig", 0, 3) + 0.86, "slam", 0.35),
    *beats("sig", frag("sig", 0, 3), D["sig"] - frag("sig", 0, 3), 0.5, 0.7),
    # the radio wakes, the number, the count
    *bed("crickets", T("radio", 0), T("drawing", -0.1), 0.45, 4.6), ("radio", vo_t("radio", 1) - 0.35, "radio", 1.0), *bed("radiobed", T("radio", vo_t("radio", 1) - 0.1), T("radio", vo_end("radio", 1) + 0.4), 0.8, 3.0),
    ("radio", frag("radio", 1, 1), "tick", 0.5), ("radio", vo_end("radio", 1) + 0.3, "static", 0.5), *beats("radio", vo_t("radio", 1), D["radio"] - vo_t("radio", 1), 0.5, 0.5),
    ("radio", frag("radio", 1, 2), "sting", 0.7), ("radio", frag("radio", 2, 2), "sting", 0.6), ("radio", frag("radio", 2, 2), "glitch", 0.4),
    ("radio", frag("radio", 3, 2), "sting", 1.0), ("radio", frag("radio", 3, 2), "boom", 0.6), ("radio", frag("radio", 3, 2), "glitch", 0.6), ("radio", frag("radio", 3, 2), "buzz", 0.5),
    ("drawing", 0.1, "crayon", 0.6), ("drawing", 0.9, "crayon", 0.5), ("drawing", frag("drawing", 0, 1), "sting", 0.6), ("drawing", frag("drawing", 0, 1) + 0.2, "riser", 0.4), *beats("drawing", frag("drawing", 0, 1), D["drawing"] - frag("drawing", 0, 1), 0.6, 0.4),
    # morning at the tank
    ("tank", 0.2, "drip", 0.5), ("tank", 1.1, "drip", 0.4), ("tank", frag("tank", 0, 1), "drip", 0.8), ("tank", frag("tank", 0, 1), "sting", 0.8), ("tank", frag("tank", 0, 1) + 0.1, "thud", 0.4),
    ("tank", frag("tank", 1, 1), "sting", 1.0), ("tank", frag("tank", 1, 1), "boom", 0.6), ("tank", frag("tank", 1, 1), "glitch", 0.5), *beats("tank", frag("tank", 0, 1), D["tank"] - frag("tank", 0, 1), 0.45, 0.6),
    *beats("choice", 0.0, D["choice"] - 0.3, 0.38, 1.0), *[("choice", 0.05 + k * 1.0, "tick", 1.0) for k in range(3)], ("choice", 1.0, "glitch", 0.6), ("choice", 1.0, "radio", 0.5),
    ("choice", D["choice"] - 2.2, "riser", 1.0), ("choice", D["choice"] - 0.62, "sting", 1.0), ("choice", D["choice"] - 0.6, "glitch", 0.8), ("choice", D["choice"] - 0.6, "boom", 0.7),
    # the end card: the page, the pen, the tick
    ("next", 0.3, "page", 0.9), ("next", 0.6, "marker", 0.35), ("next", 1.0, "marker", 0.35), ("next", 1.45, "sting", 0.6), ("next", 1.9, "glitch", 0.3), *beats("next", 1.2, D["next"] - 1.2, 0.7, 0.5),
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


dip(0.0, T("hook", -0.1), 0.2, 0.05)                      # the cold open: the lid, the hand
dip(T("market", 0), T("clatter", frag("clatter", 0, 1)), 0.3)
dip(T("gateTop", 0), T("gateTop", -0.05), 0.6)   # the market is quiet until the can drops
dip(T("reach", 0), T("stop", -0.05), 0.3)
dip(T("sig", frag("sig", 0, 2)), T("sig", frag("sig", 0, 3) + 0.05), 0.05, 0.12)  # silence before "ข้อเดียว"
dip(T("radio", vo_t("radio", 1) - 0.4), T("radio", vo_end("radio", 1) + 0.3), 0.15)  # only the radio speaks
dip(T("tank", frag("tank", 0, 1)), T("tank", -0.05), 0.35)
dip(T("choice", 0), T("choice", -0.3), 0.5)
boost = np.ones(N, np.float32)  # the action plays with the music up
for a0, a1 in ((T("lunge", 0.3), T("run", -0.05)), (T("road", 0), T("slam", 0.6))):
    boost += 0.4 * (np.clip((t - a0) / 0.3, 0, 1) * np.clip((a1 - t) / 0.2, 0, 1)).astype(np.float32)
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

"""Build the episode soundtrack from schedule.json (เอาชีวิตรอด 99 วัน EP.7 "คนไร้ประโยชน์"): per-line levelled voice, synthesized SFX
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
HS = vo_t("hook", 1) - 0.1; HN = int((vo_t("hook", 2) - HS) / 0.3)                         # the hook's slaps: every 0.3 s until "อย่ามัวแต่ตบหลัง"
BL, TH = 0.36, 0.42
B0 = frag("phu", 0, 2) + 0.35; T0 = vo_end("phu", 1) + 0.05; POP = T0 + 2 * TH + 0.12      # first back blow; first thrust; out on the third
BA = vo_t("board", 1) - 0.25                                                               # the score card's shot starts here

# ---- voice: every line levelled on its own so shouts and the child's line sit at a readable loudness ----
LINE_GAIN = {"r01": -2, "d03": -1, "d04": 1, "s01": 0}
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
    # cold open: the canteen under the tubes; our hand slapping her back, again and again; "อย่ามัวแต่ตบหลัง" — the jolt
    *bed("hum", T("hook", 0), T("hook", -0.1), 0.25, 3.0), ("hook", -0.25, "whoosh", 0.7), *[("hook", HS + i * 0.3 + 0.09, "slap", 0.55 + 0.05 * (i % 2)) for i in range(HN)],
    ("hook", vo_t("hook", 2), "sting", 1.0), ("hook", vo_t("hook", 2), "boom", 0.6), ("hook", vo_t("hook", 2), "glitch", 0.5), *beats("hook", 0.4, D["hook"] - 0.4, 0.45, 0.6),
    # dawn, the board: "เหลือ 93 วัน"; ยายจันทร์'s brush by the door
    ("chapter", 0.05, "page", 0.9), ("chapter", 0.4, "chalk", 0.5), ("chapter", 0.5, "slam", 0.5), *[("chapter", 0.9 + k * 0.16, "pop", 0.4) for k in range(2)], ("chapter", frag("chapter", 0, 1), "sting", 0.6),
    *bed("wind", T("chapter", 0), T("board", -0.1), 0.2, 3.2), *bed("crickets", T("chapter", 0), T("chapter", -0.1), 0.1, 4.0),
    # the line-up: คุณวิน's rule; the score card — ปั้น at the bottom, the red ring, the stamp
    *[("board", 0.2 + k * 0.5, "steps", 0.2) for k in range(3)], ("board", frag("board", 0, 2), "sting", 0.7), ("board", frag("board", 0, 2), "boom", 0.35),
    ("board", BA + 0.05, "page", 0.8), ("board", BA + 0.4, "slam", 0.45), *[("board", BA + 0.55 + i * 0.32, "pen", 0.45) for i in range(5)],
    ("board", frag("board", 1, 1) - 0.05, "marker", 0.6), ("board", frag("board", 1, 1), "sting", 0.8), ("board", frag("board", 1, 1), "boom", 0.4), ("board", frag("board", 1, 1) + 0.5, "slam", 0.7), ("board", frag("board", 1, 1) + 0.5, "thud", 0.5),
    *beats("board", vo_t("board", 0), D["board"] - vo_t("board", 0), 0.6, 0.4),
    # dinner under the tubes: spoons, ปั้น's quick spoon; "เดี๋ยวติดคอ"
    *bed("hum", T("dinner", 0), T("sig", -0.1), 0.28, 3.0), *bed("fan", T("dinner", 0), T("breathe", -0.1), 0.14, 4.0), *[("dinner", 0.2 + k * 0.8, "ching", 0.1) for k in range(8)], *[("dinner", 0.3 + k * 0.36, "ching", 0.07) for k in range(10)],
    ("dinner", frag("dinner", 1, 1), "sting", 0.4),
    # she chokes: the room drops away — only the heartbeat and the tubes; the three ✗
    ("choke", 0.05, "riser", 0.5), *[x for o in (vo_t("choke", 1), frag("choke", 1, 1), frag("choke", 1, 2)) for x in (("choke", o, "pop", 0.45), ("choke", o + 0.3, "marker", 0.35))],
    ("choke", frag("choke", 1, 2), "sting", 0.9), ("choke", frag("choke", 1, 2), "boom", 0.45), *beats("choke", 0.0, D["choke"], 0.42, 0.85),
    # panic: slap after slap, a cup set down, the count climbing; คุณวิน doesn't move
    *[("panic", t, "slap", 0.5) for t in np.arange(0.12, D["panic"] - 0.05, 0.3)], ("panic", 0.4, "ching", 0.35), ("panic", D["panic"] - 1.0, "sting", 0.5), *beats("panic", 0.0, D["panic"], 0.36, 0.95),
    # ภู: steps, the skill card; five back blows (the tally ticks), "ยังไม่หลุด"; the thrusts — out on the third
    *[("phu", k * 0.16, "steps", 0.45) for k in range(3)], ("phu", 0.15, "page", 0.6), ("phu", 0.45, "slam", 0.5), ("phu", 0.55, "sting", 0.6),
    *[x for i in range(5) for x in (("phu", B0 + i * BL + 0.1, "blow", 0.85), ("phu", B0 + i * BL + 0.12, "pop", 0.3))],
    ("phu", B0 + 5 * BL + 0.05, "slam", 0.6), ("phu", B0 + 5 * BL + 0.05, "buzz", 0.35),
    *[x for i in range(3) for x in (("phu", T0 + i * TH + 0.1, "thud", 0.45), ("phu", T0 + i * TH + 0.12, "pop", 0.3))],
    ("phu", POP, "pop", 0.8), ("phu", POP, "sting", 1.0), ("phu", POP, "boom", 0.5), ("phu", POP + 0.1, "ding", 0.6), ("phu", POP + 0.85, "tap", 0.5), ("phu", POP + 0.2, "cough", 0.45),
    *beats("phu", 0.0, POP, 0.4, 0.8),
    # she breathes: coughing, then quiet; "หนูขอโทษ…"
    *[("breathe", 0.1 + k * 0.35, "cough", 0.4 - 0.08 * k) for k in range(3)], ("breathe", frag("breathe", 0, 1), "sting", 0.35),
    # the steps card and the real-life tips
    *[x for o in (vo_t("card", 0), frag("card", 0, 1), frag("card", 0, 2), frag("card", 0, 3)) for x in (("card", o, "page", 0.4), ("card", o + 0.3, "pen", 0.5), ("card", o + 0.35, "ding", 0.25))],
    ("real", frag("real", 0, 1) - 0.1, "page", 0.6), ("real", frag("real", 0, 1) + 0.2, "slam", 0.5), ("real", frag("real", 0, 2), "page", 0.6), ("real", frag("real", 0, 2) + 0.3, "slam", 0.5), ("real", frag("real", 0, 3), "ding", 0.4),
    # คุณวิน crosses to ภู: "เหมือนเดิม…"; his pen: ปั้น → ภาระ
    *[("win", 0.1 + k * 0.45, "steps", 0.3) for k in range(2)], ("win", frag("win", 1, 0) + 0.05, "sting", 0.7), ("win", frag("win", 1, 0) + 0.05, "boom", 0.35),
    ("win", frag("win", 2, 1) - 0.45, "marker", 0.5), ("win", frag("win", 2, 1) - 0.15, "pen", 0.8), ("win", frag("win", 2, 1) + 0.45, "pen", 0.8), ("win", frag("win", 2, 1) + 0.6, "sting", 0.8), ("win", frag("win", 2, 1) + 0.6, "boom", 0.4),
    *beats("win", vo_t("win", 1), D["win"] - vo_t("win", 1), 0.55, 0.5),
    # the signature
    ("sig", 0.05, "page", 0.8), ("sig", 0.36, "thud", 0.25),
    *[x for o in (frag("sig", 0, 0) + 0.3, frag("sig", 0, 0) + 0.62, frag("sig", 0, 1) + 0.15) for x in (("sig", o, "pen", 0.9), ("sig", o + 0.05, "ding", 0.3))],
    ("sig", frag("sig", 0, 2) + 0.45, "marker", 0.45), *beats("sig", frag("sig", 0, 2), frag("sig", 0, 3) - frag("sig", 0, 2), 0.38, 0.8),
    *[("sig", frag("sig", 0, 2) + o, "tick", 0.55 + 0.1 * k) for k, o in enumerate((0.1, 0.42, 0.68, 0.88, 1.02, 1.12))],
    ("sig", frag("sig", 0, 3) - 1.1, "riser", 0.6),
    ("sig", frag("sig", 0, 3), "sting", 1.1), ("sig", frag("sig", 0, 3), "boom", 0.7), ("sig", frag("sig", 0, 3), "pen", 1.0), ("sig", frag("sig", 0, 3) + 0.1, "pen", 1.0),
    ("sig", frag("sig", 0, 3) + 0.24, "rip", 1.1), ("sig", frag("sig", 0, 3) + 0.86, "thud", 0.8), ("sig", frag("sig", 0, 3) + 0.86, "slam", 0.35),
    *beats("sig", frag("sig", 0, 3), D["sig"] - frag("sig", 0, 3), 0.5, 0.7),
    # midnight: the dorm, then through the bars — ภู under the lamp, the knot, his steps to the office
    *bed("crickets", T("scarf", 0), T("choice", -0.3), 0.22, 4.0), *bed("wind", T("scarf", 0), T("office", -0.1), 0.12, 3.2),
    ("scarf", vo_t("scarf", 0) + 0.3, "rustle", 0.6), ("scarf", vo_t("scarf", 0) + 1.0, "rustle", 0.5), ("scarf", frag("scarf", 0, 1), "sting", 0.7), ("scarf", frag("scarf", 1, 1), "sting", 0.8), ("scarf", frag("scarf", 1, 1), "boom", 0.4),
    *[("scarf", D["scarf"] - 1.0 + k * 0.48, "steps", 0.2) for k in range(2)], *beats("scarf", 0.0, D["scarf"], 0.55, 0.5),
    # the office window: the radio — 92… five — then คุณวิน: "ฉันเก็บไว้ให้นายตลอด"
    ("office", vo_t("office", 0) - 0.4, "radio", 1.0), *bed("radiobed", T("office", vo_t("office", 0) - 0.1), T("office", vo_end("office", 0) + 0.3), 0.5, 3.0),
    ("office", frag("office", 0, 2), "tick", 0.5), ("office", frag("office", 0, 2), "sting", 0.8), ("office", frag("office", 0, 2), "glitch", 0.35),
    ("office", vo_t("office", 1) - 0.1, "static", 0.25), ("office", frag("office", 1, 1), "sting", 1.0), ("office", frag("office", 1, 1), "boom", 0.6), ("office", frag("office", 1, 1), "glitch", 0.5),
    *beats("office", vo_t("office", 0), D["office"] - vo_t("office", 0), 0.5, 0.55),
    # ปั้น's drawing
    ("drawing", 0.1, "crayon", 0.6), ("drawing", 0.9, "crayon", 0.5), ("drawing", frag("drawing", 0, 1) - 0.4, "riser", 0.4), ("drawing", frag("drawing", 0, 1), "sting", 0.9), ("drawing", frag("drawing", 0, 1), "boom", 0.5), ("drawing", frag("drawing", 0, 1) + 0.2, "glitch", 0.45),
    *beats("drawing", 0.3, D["drawing"] - 0.3, 0.55, 0.5),
    # the choice, then black; the end card
    *beats("choice", 0.0, D["choice"] - 0.3, 0.38, 1.0), *[("choice", 0.05 + k * 1.0, "tick", 1.0) for k in range(3)], ("choice", 1.0, "glitch", 0.6), ("choice", 1.0, "radio", 0.5),
    ("choice", D["choice"] - 2.2, "riser", 1.0), ("choice", D["choice"] - 0.62, "sting", 1.0), ("choice", D["choice"] - 0.6, "glitch", 0.8), ("choice", D["choice"] - 0.6, "boom", 0.7),
    ("next", 0.3, "page", 0.9), ("next", 0.6, "marker", 0.35), ("next", 1.0, "marker", 0.35), ("next", 1.45, "sting", 0.6), ("next", 1.9, "glitch", 0.3), *beats("next", 1.2, D["next"] - 1.2, 0.7, 0.5),
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
dip(T("board", frag("board", 1, 1) - 0.2), T("board", -0.05), 0.35)
dip(T("choke", 0.1), T("choke", -0.05), 0.12)                      # the room drops away while she can't breathe
dip(T("phu", POP - 0.1), T("phu", POP + 0.6), 0.25)
dip(T("win", frag("win", 1, 0)), T("win", -0.05), 0.35)
dip(T("sig", frag("sig", 0, 2)), T("sig", frag("sig", 0, 3) + 0.05), 0.05, 0.12)
dip(T("office", vo_t("office", 0) - 0.4), T("office", vo_end("office", 0) + 0.3), 0.15)
dip(T("office", frag("office", 1, 1)), T("office", -0.05), 0.3)
dip(T("drawing", frag("drawing", 0, 1)), T("drawing", -0.05), 0.35)
dip(T("choice", 0), T("choice", -0.3), 0.5)
boost = np.ones(N, np.float32)  # the action plays with the music up
for a0, a1 in ((T("panic", 0), T("panic", -0.05)), (T("phu", 0.2), T("phu", POP - 0.1))):
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

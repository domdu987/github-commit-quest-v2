"""Build the episode soundtrack from schedule.json: per-line levelled voice, synthesized rainforest SFX
(tap water, knocks, a muffled scream, the infected growling, stairwell footsteps) and the Suno music bed with dips before the scares and
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
LINE_GAIN = {"d02": -1, "d04": 0, "d07": 0, "d08": -1}
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
    *bed("tap", 0.0, T("hook", -0.1), 0.8, 2.4), *beats("hook", 0.3, D["hook"] - 0.3, 0.6, 0.6), ("hook", frag("hook", 0, 1), "sting", 0.5),
    ("hook", vo_t("hook", 1) - 0.4, "whoosh", 0.5), ("hook", vo_t("hook", 1), "sting", 0.9), ("hook", vo_t("hook", 1), "boom", 0.6), ("hook", vo_t("hook", 1), "glitch", 0.6), *[("hook", vo_t("hook", 1) + k * 0.4, "beep", 0.35) for k in range(3)], ("hook", -0.25, "whoosh", 0.8),
    ("rewind", 0.0, "rewind", 1.0), ("rewind", 0.05, "glitch", 0.5), ("rewind", 0.1, "boom", 0.45), ("rewind", 0.55, "pop", 0.5),
    *[("news", frag("news", 0, j) + (0.1 if j == 0 else 0), "notif", 0.7) for j in range(3)], ("news", frag("news", 0, 1), "sting", 0.4),
    ("fake", vo_t("fake") - 0.05, "pop", 0.3),
    ("scream", frag("scream", 0, 1) - 0.15, "scream", 1.0), ("scream", frag("scream", 0, 1), "sting", 0.7), *[("scream", frag("scream", 0, 2) + k * 0.15, "knock", 0.9) for k in range(4)],
    *beats("scream", frag("scream", 0, 1), D["scream"] - frag("scream", 0, 1), 0.45, 0.6),
    *beats("peep", 0.0, D["peep"], 0.6, 0.6), ("peep", 0.4, "growl", 0.5), ("peep", frag("peep", 0, 1), "sting", 0.6),
    ("turn", 0.3, "growl", 0.6), ("turn", frag("turn", 0, 1) - 0.05, "growl", 1.2), ("turn", frag("turn", 0, 1) - 0.05, "boom", 0.8), ("turn", frag("turn", 0, 1) - 0.05, "sting", 1.0), ("turn", frag("turn", 0, 1) - 0.05, "glitch", 0.8),
    *[("knock", 0.05 + k * 0.2, "knock", 1.0) for k in range(3)], *[("knock", vo_t("knock") + 0.4 + k * 0.18, "knock", 0.9) for k in range(3)], *beats("knock", 0.0, D["knock"], 0.42, 0.7),
    ("jit", 0.0, "rustle", 0.6), ("jit", 0.82, "slam", 1.0), ("jit", frag("jit", 0, 0) + 0.15, "pop", 0.4),
    ("rule", 0.1, "swell", 0.4), *[("rule", t, "pop", 0.5) for t in (vo_t("rule", 1), frag("rule", 1, 1) - 0.05, frag("rule", 1, 2) - 0.05)], ("rule", frag("rule", 1, 2) + 0.15, "knock", 0.5),
    ("water", 0.2, "hum", 0.4), ("water", frag("water", 1, 1), "buzz", 0.5), ("water", frag("water", 1, 1), "boom", 0.5), ("water", frag("water", 1, 1), "sting", 0.6),
    *[("litres", t, "marker", 0.7) for t in (frag("litres", 0, 0), frag("litres", 0, 0) + 0.45, frag("litres", 0, 2) + 0.1, vo_t("litres", 1), vo_t("litres", 1) + 0.5, frag("litres", 1, 1), frag("litres", 1, 1) + 0.5)],
    *bed("tap", T("fill", 0), T("stop", frag("stop", 0, 1)), 0.9, 2.4), *[("fill", 0.2 + k * 0.5, "tick", 0.2) for k in range(6)],
    ("stop", frag("stop", 0, 1) - 0.5, "sputter", 1.0), ("stop", frag("stop", 0, 1), "powerdown", 1.0), ("stop", frag("stop", 0, 1) + 0.3, "drip", 0.8), ("stop", frag("stop", 0, 2), "sting", 0.7), ("stop", frag("stop", 0, 2), "beep", 0.6),
    ("boss", 0.2, "rustle", 0.5),
    *[("lift", t, "click", 0.9) for t in (0.24, 0.56, 0.76)], *beats("lift", 0.0, D["lift"], 0.5, 0.5), ("lift", 0.98, "whoosh", 0.45),  # LIFT_PRESS in shots.part
    *[("stairs", 0.2 + k * 0.45, "stomp", 0.35) for k in range(7)], ("stairs", frag("stairs", 0, 2), "swell", 0.4),
    *[("floor19", 0.1 + k * 0.45, "stomp", 0.3) for k in range(2)], ("floor19", frag("floor19", 0, 1) - 0.05, "growl", 1.0), ("floor19", frag("floor19", 0, 1), "sting", 0.9), ("floor19", frag("floor19", 0, 1), "boom", 0.5),
    # ---- action: ambush, bite, the extinguisher, the chase, the fire door, the corridor, home ----
    ("ambush", 0.3, "growl", 0.7), ("ambush", 0.5, "shriek", 0.9), ("ambush", 0.5, "steps", 1.0), ("ambush", 0.95, "whoosh", 0.9), ("ambush", 1.0, "scream", 0.7),
    ("ambush", 1.02, "sting", 0.9), ("ambush", 1.02, "glitch", 0.5), *beats("ambush", 0.5, D["ambush"] - 0.5, 0.34, 0.6),
    ("bite", 0.0, "growl", 1.3), ("bite", 0.2, "scream", 0.8), ("bite", 0.25, "boom", 0.8), ("bite", 0.2, "glitch", 0.8), ("bite", 0.25, "squish", 0.8),
    ("swing", 0.0, "steps", 0.7), ("swing", 0.22, "whoosh", 0.9), ("swing", 0.42, "clang", 1.3), ("swing", 0.42, "boom", 0.8), ("swing", 0.42, "glitch", 0.5), ("swing", 0.92, "thud", 1.0),
    ("swing", 1.45, "shriek", 0.8), ("swing", 1.55, "growl", 0.9), ("swing", 1.6, "steps", 0.8), *beats("swing", 1.55, D["swing"] - 1.55, 0.36, 0.6),
    ("noise", 0.0, "clang", 0.55), ("noise", 0.25, "clang", 0.3), ("noise", 0.5, "clang", 0.15), ("noise", 0.35, "growl", 0.8), ("noise", 0.6, "growl", 0.7), ("noise", 0.75, "shriek", 0.6),
    ("noise", 0.2, "pop", 0.4), *beats("noise", 0.0, D["noise"], 0.34, 0.6),
    ("chase", 0.0, "steps", 1.0), ("chase", 0.65, "steps", 0.9), ("chase", 0.3, "growl", 0.9), ("chase", 0.9, "shriek", 0.7), ("chase", 0.53, "riser", 0.8), *beats("chase", 0.0, D["chase"], 0.32, 0.6),
    ("jam", 0.0, "growl", 1.1), ("jam", 0.0, "knock", 0.7), ("jam", 0.62, "shriek", 0.8), ("jam", 0.83, "slam", 1.4), ("jam", 0.83, "boom", 0.9), ("jam", 0.9, "latch", 0.9),
    ("jam", 0.95, "thud", 0.7), ("jam", 1.0, "growl", 0.6),
    ("corridor", 0.0, "steps", 0.9), ("corridor", 0.65, "steps", 0.9), ("corridor", 1.3, "steps", 0.9), ("corridor", 0.7, "slam", 1.1), ("corridor", 0.7, "sting", 1.0),
    ("corridor", 0.75, "shriek", 1.1), ("corridor", 1.15, "whoosh", 1.0), ("corridor", 1.16, "glitch", 0.6), *beats("corridor", 0.0, D["corridor"], 0.3, 0.6),
    ("inside", 0.06, "slam", 1.4), ("inside", 0.08, "boom", 0.6), ("inside", 0.1, "latch", 0.8), ("inside", 0.5, "knock", 1.0),
    *bed("tap", T("wash", 0), T("real", -0.1), 0.6, 2.4), ("wash", frag("wash", 0, 2), "beep", 0.45), ("wash", frag("wash", 0, 2) + 0.5, "beep", 0.6), *[("wash", frag("wash", 0, 2) + 1.5 + k, "tick", 0.35) for k in range(3)],
    ("real", frag("real", 0, 1) - 0.1, "pop", 0.5), ("real", frag("real", 1, 1) - 0.1, "ding", 0.6),
    ("hosp", 0.1, "siren", 0.25), ("hosp", frag("hosp", 0, 2) - 0.05, "notif", 0.7), ("hosp", frag("hosp", 0, 2), "sting", 0.6),
    ("door", 0.1, "knock", 0.5), *beats("door", 0.0, D["door"], 0.5, 0.5),
    ("sleeve", frag("sleeve", 0, 1), "rustle", 0.8), *beats("sleeve", 0.0, D["sleeve"], 0.55, 0.5),
    ("sig", 0.05, "glitch", 0.35), ("sig", 0.05, "beep", 0.35),
    ("sig", frag("sig", 0, 0) + 0.3, "ding", 0.6), ("sig", frag("sig", 0, 0) + 0.62, "ding", 0.6), ("sig", frag("sig", 0, 1) + 0.15, "ding", 0.6),
    ("sig", frag("sig", 0, 2), "glitch", 0.45), *beats("sig", frag("sig", 0, 2), frag("sig", 0, 3) - frag("sig", 0, 2), 0.38, 0.8),
    *[("sig", frag("sig", 0, 2) + o, "tick", 0.55 + 0.1 * k) for k, o in enumerate((0.1, 0.42, 0.68, 0.88, 1.02, 1.12))],  # ticking that speeds up into the cross
    ("sig", frag("sig", 0, 3) - 1.1, "riser", 0.6),
    ("sig", frag("sig", 0, 3), "sting", 1.1), ("sig", frag("sig", 0, 3), "boom", 0.8), ("sig", frag("sig", 0, 3), "glitch", 0.7), ("sig", frag("sig", 0, 3) + 0.12, "slam", 0.7),
    *beats("sig", frag("sig", 0, 3), D["sig"] - frag("sig", 0, 3), 0.5, 0.7),
    *bed("crickets", T("night", 0), T("choice", -0.3), 0.25, 5.0), ("night", frag("night", 0, 1), "swell", 0.4),
    ("scar", frag("scar", 0, 1), "sting", 1.0), ("scar", frag("scar", 0, 1), "glitch", 0.6), *beats("scar", 0.0, D["scar"], 0.5, 0.7),
    *beats("choice", 0.0, D["choice"] - 0.3, 0.38, 1.0), *[("choice", 0.05 + k * 1.0, "tick", 1.0) for k in range(3)], ("choice", 1.0, "glitch", 0.6),
    ("next", 0.3, "buzz", 0.5), ("next", 0.42, "slam", 0.6), ("next", 0.42, "glitch", 0.35), ("next", 0.85, "sting", 0.7), ("next", 0.9, "squish", 0.4), *beats("next", 0.9, D["next"] - 0.9, 0.7, 0.5),
    ("choice", D["choice"] - 2.2, "riser", 1.0), ("choice", D["choice"] - 0.62, "sting", 1.0), ("choice", D["choice"] - 0.6, "glitch", 0.8), ("choice", D["choice"] - 0.6, "boom", 0.7),
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


dip(0.0, T("hook", -0.1), 0.15, 0.05)                    # the cold open sits on the tap and a heartbeat
dip(T("scream", 0), T("knock", -0.1), 0.3)
dip(T("turn", frag("turn", 0, 1) - 0.1), T("knock", -0.1), 0.0, 0.05)  # silence after the jump scare, through the knocks
dip(T("rule", 0), T("rule", -0.1), 0.35)
dip(T("lift", 0.1), T("lift", -0.05), 0.25, 0.1)                     # the dead lift: near silence, three dry clicks
dip(T("floor19", 0), T("ambush", 0.45), 0.3)
dip(T("inside", 0.1), T("inside", -0.05), 0.12, 0.08)                 # the door shut: near silence, the pounding
dip(T("door", 0), T("sleeve", -0.1), 0.35)
dip(T("sig", frag("sig", 0, 2)), T("sig", frag("sig", 0, 3) + 0.05), 0.05, 0.12)  # silence before "ข้อเดียว"
dip(T("night", 0), T("scar", -0.05), 0.25)
dip(T("choice", 0), T("choice", -0.3), 0.5)
boost = np.ones(N, np.float32)  # the action plays with the music up
a0, a1 = T("ambush", 0.45), T("corridor", -0.05)
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

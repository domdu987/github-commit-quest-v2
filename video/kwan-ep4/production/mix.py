"""ควันหลง EP.4 (finale): build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX (the fire door,
sirens and the firefighters' radio outside, the far voice from the seventh floor, a shadow-puppet gong for 2539, the blanket) and the
Suno music bed with dips before the scares and sidechain ducking under the voice. No signature, no choice: the music fades out under
the end card. Output -14 LUFS."""
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


OPEN = frag("hook", 0, 1) - 0.25  # the fire door swings open (same as the composition)
RULE = frag("rule", 0, 1) - 0.12
BYE = frag("wave", 0, 2)
LG = lambda j: vo_t("legend", j)

CUES = [
    ("recap", 0.0, "swell", 0.6), *beats("recap", 0.0, D["recap"], 0.38, 0.8), ("recap", D["recap"] - 0.35, "glitch", 0.7),
    ("hook", 0.3, "sting", 0.6), *beats("hook", 0.0, OPEN, 0.4, 0.45), ("hook", OPEN - 0.1, "latch", 0.9), ("hook", OPEN, "creak", 0.7), ("hook", OPEN + 0.05, "whoosh", 0.7),
    ("hook", OPEN + 0.1, "siren", 0.6), ("hook", OPEN + 2.6, "siren", 0.6), ("hook", frag("hook", 0, 3), "glitch", 0.5), ("hook", D["hook"] - 0.3, "whoosh", 0.6),
    ("out", 0.0, "siren", 0.5), ("out", 0.2, "steps", 0.35), ("out", 0.6, "pant", 0.5), ("out", 2.8, "pant", 0.4), ("out", 0.0, "crackle", 0.6),
    ("meet", 0.0, "siren", 0.35), ("meet", 2.9, "siren", 0.35), ("meet", 0.2, "steps", 0.3), ("meet", 1.5, "radiosq", 0.35),
    ("ask", 0.0, "siren", 0.45), ("ask", vo_t("ask") - 0.25, "radiosq", 0.5),
    ("tell", 0.0, "siren", 0.35), ("tell", frag("tell", 0, 1) + 0.6, "radiosq", 0.7), ("tell", frag("tell", 0, 1) + 1.6, "radiosq", 0.5),
    ("call", 0.0, "siren", 0.3), ("call", vo_t("call") - 0.2, "swell", 0.6), ("call", vo_t("call") + 0.3, "sting", 0.5), ("call", frag("call", 0, 1), "glitch", 0.6),
    *beats("call", vo_t("call"), D["call"] - vo_t("call"), 0.42, 0.5),
    *beats("beside", frag("beside", 0, 1), D["beside"] - frag("beside", 0, 1), 0.42, 0.55), ("beside", frag("beside", 0, 1) - 0.1, "swell", 0.4),
    *beats("notme", 0.0, D["notme"], 0.4, 0.6), ("notme", vo_t("notme") + 0.5, "glitch", 0.5), ("notme", vo_t("notme") + 0.5, "sting", 0.8), ("notme", D["notme"] - 1.0, "riser", 0.5),
    # 2539, as a shadow-puppet play
    ("legend", 0.05, "gong", 0.7), ("legend", 0.1, "swell", 0.45), ("legend", 0.4, "crackle", 0.8), ("legend", LG(1) - 0.1, "whoosh", 0.35), ("legend", LG(1) - 0.05, "ching", 0.4),
    ("legend", LG(1) + 2.4, "scream", 0.25), ("legend", LG(2) - 0.1, "whoosh", 0.35), ("legend", LG(2) - 0.05, "gong", 0.5), ("legend", LG(2) + 0.2, "steps", 0.4),
    *beats("legend", LG(2) + 0.4, 1.8, 0.6, 0.35), ("legend", LG(3) - 0.15, "glitch", 0.4), ("legend", LG(3) - 0.1, "whoosh", 0.35), ("legend", LG(3), "ching", 0.4),
    ("legend", D["legend"] - 1.0, "gong", 0.45),
    ("sri", 0.35, "rustle", 0.6), ("sri", 0.5, "flap", 0.25), ("sri", 0.0, "siren", 0.15),
    ("reveal", frag("reveal", 0, 1) - 0.15, "whoosh", 0.4), ("reveal", frag("reveal", 0, 1) - 0.1, "swell", 0.5), ("reveal", D["reveal"] - 0.7, "glitch", 0.35),
    ("rule", RULE, "ching", 0.5), ("rule", RULE + 0.15, "swell", 0.5), *beats("rule", RULE + 0.1, D["rule"] - RULE - 0.1, 0.5, 0.4),
    ("wave", 0.2, "swell", 0.4), ("wave", BYE - 0.2, "ching", 0.35), ("wave", vo_end("wave") + 0.5, "swell", 0.5), ("wave", vo_end("wave") + 0.6, "ching", 0.4),
    ("end", 0.3, "whoosh", 0.4), ("end", 0.45, "ching", 0.5), ("end", 0.6, "gong", 0.5),
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


dip(0.0, T("hook", OPEN), 0.3, 0.05)
dip(T("call", 0), T("notme", -0.05), 0.35)
dip(T("legend", 0), T("legend", -0.2), 0.55)
dip(T("rule", RULE), T("rule", -0.05), 0.4)
mus = mus * gain
fade0, fade1 = T("end", 0.0), TOTAL - 0.1  # the finale: the music winds down under the end card instead of a hard cut
mus *= np.clip((fade1 - t) / (fade1 - fade0), 0, 1) ** 1.5

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mix = vo + mus * duck + sfx
tail = int(0.6 * SR)
mix[-tail:] *= np.linspace(1, 0, tail)  # in step with the end card fading to black
peak = np.max(np.abs(mix))
if peak > 0.98:
    mix = np.tanh(mix / peak * 1.2) * 0.95
out = os.path.join(HERE, "mix_raw.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", out],
               input=mix.astype(np.float32).tobytes(), check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)
print("mix written", TOTAL)

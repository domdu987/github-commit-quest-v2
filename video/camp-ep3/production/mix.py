"""Build the episode soundtrack from schedule.json: per-line levelled voice, synthesized forest/camp SFX
and the Suno music bed with dips before the scares and sidechain ducking under the voice. Output -14 LUFS."""
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


# ---- voice: every line levelled on its own so whispers and screams sit at a readable loudness ----
LINE_GAIN = {"d00": -3, "d03": -3, "d11": -2, "d06": -1}  # the thing in the forest stays a little distant
vo = np.zeros(N, np.float32)
for s in SC["shots"]:
    for v in s["vo"]:
        x = load(os.path.join(HERE, "vo", f"{v['id']}.wav"))
        place(vo, level(x, -18 + LINE_GAIN.get(v["id"], 0)), s["start"] + v["t"])

# ---- sfx cues: (shot, t from shot start (negative = from its end), type, gain) ----
D = {k: SH[k]["dur"] for k in SH}


def beats(k, t0, dur, period, g=0.9):  # heartbeat sfx in step with Fx.heart
    return [(k, t0 + i * period, "heartbeat", g) for i in range(int((dur - 0.1) / period) + 1)]


def ticks(k, t0, t1, step, g=0.5):
    n = int((t1 - t0) / step)
    return [(k, t0 + i * step, "tick", g) for i in range(n)]


pick = vo_t("open") + SH["open"]["vo"][0]["dur"] + 0.15
SV = lambda i: vo_t("siege", i)
SE = lambda i: SV(i) + SH["siege"]["vo"][i]["dur"]
msg = vo_t("signal", 1) - 2.2
KN = [0.2, 0.55, 0.9, 1.25]
s0 = vo_t("sneak", 1) - 0.2
creak, face = s0 + 3.0, s0 + 4.2
slam = vo_t("sneak", 2) + SH["sneak"]["vo"][2]["dur"] + 0.15
sneak_steps = [s0 + k for k in (0.4, 1.2, 2.0)]
CUES = [
    ("open", 0.0, "static", 0.8), ("open", 1.0, "static", 0.5), ("open", 0.2, "glitch", 0.6), *beats("open", 0.0, D["open"], 0.4, 0.9),
    *[("open", 0.15 + k * (pick - 0.15) / 3, "tick", 1.0) for k in range(3)], ("open", pick, "ding", 0.7), ("open", pick, "whoosh", 1.0),
    ("chai", 0.0, "rustle", 1.0), ("chai", 0.5, "rustle", 0.9), ("chai", 1.0, "boom", 0.4), ("chai", -0.8, "notif", 0.4),
    ("inside", 0.0, "static", 0.7), ("inside", 0.5, "notif", 0.35), ("inside", 1.2, "static", 0.4),
    ("map", 0.0, "whoosh", 1.0), ("map", 0.05, "riser", 0.4), ("map", 2.4, "sting", 0.5), *ticks("map", 3.5, 5.6, 0.07, 0.4), ("map", 5.6, "ding", 0.5),
    *ticks("signal", 0.5, 1.7, 0.08, 0.35), ("signal", 1.6, "notif", 0.6), ("signal", msg, "notif", 1.0), ("signal", msg + 1.0, "ding", 0.6), ("signal", msg + 1.1, "sting", 0.7),
    *beats("signal", msg + 1.1, D["signal"] - msg - 1.1, 0.5, 0.8),
    ("who", 0.0, "hum", 0.6), ("who", vo_t("who", 1), "hum", 0.7), ("who", vo_t("who", 1) + 0.3, "glitch", 0.5), ("who", vo_t("who", 1) + 1.5, "glitch", 0.4),
    ("aspirin", 0.2, "rustle", 0.4), ("aspirin", vo_t("aspirin", 1), "sting", 0.5), ("aspirin", vo_t("aspirin", 2), "notif", 0.4),
    *[("siege", k, "knock", 1.2) for k in KN], ("siege", SV(0) - 0.2, "glitch", 0.7), ("siege", SV(0), "sting", 0.8), *beats("siege", 0.0, D["siege"], 0.45, 0.9),
    ("siege", SE(0) + 0.5, "knock", 0.9), ("siege", SE(1) + 1.5, "creak", 0.9), ("siege", SE(1) + 3.0, "knock", 1.0), ("siege", D["siege"] - 0.6, "pop", 0.4),
    ("sneak", 0.0, "crickets", 0.3), *[("sneak", k, "rustle", 0.25) for k in sneak_steps], *[("sneak", k, "tick", 0.5) for k in sneak_steps],
    ("sneak", creak, "creak", 2.2), ("sneak", creak, "sting", 0.7), ("sneak", creak + 0.55, "glitch", 0.6), ("sneak", creak + 0.55, "notif", 0.5),
    ("sneak", face, "knock", 1.8), ("sneak", face, "boom", 0.9), ("sneak", face, "sting", 1.3), ("sneak", face + 0.3, "knock", 1.4), ("sneak", slam, "knock", 1.6), ("sneak", slam, "boom", 0.7),
    *beats("sneak", s0, D["sneak"] - s0, 0.5, 0.85),
    ("window", 0.0, "wind", 0.6), *[("window", k, "glitch", 0.5) for k in (1.6, 3.1, 4.6, 6.6)], *[("window", k, "boom", 0.3) for k in (3.1, 6.6)], *beats("window", 0.0, D["window"], 0.42, 0.9),
    ("dawn", 0.0, "riser", 0.5), *ticks("dawn", 0.45, 2.45, 0.05, 0.35), ("dawn", 2.4, "swell", 0.6), ("dawn", vo_t("dawn") + 0.2, "siren", 0.9), ("dawn", vo_t("dawn") + 2.8, "siren", 0.7),
    ("dawn", vo_t("dawn", 1) + 0.6, "ding", 0.5),
    ("after", 0.0, "swell", 0.5), ("after", 0.6, "notif", 0.4),
    *[("call", 0.2 + k * 1.2, "vibe", 1.0) for k in range(5)], *[("call", 0.3 + k * 1.2, "ring", 0.8) for k in range(5)], ("call", vo_t("call", 1), "sting", 1.0), ("call", vo_t("call", 1) + 0.4, "glitch", 0.6),
    *[("phone", 0.1 + k * 1.2, "vibe", 1.1) for k in range(6)], *[("phone", 0.2 + k * 1.2, "ring", 0.9) for k in range(6)], ("phone", 2.6, "glitch", 0.7),
    *beats("phone", 0.0, D["phone"] - 0.3, 0.42, 1.0), ("phone", D["phone"] - 1.2, "glitch", 0.9), ("phone", D["phone"] - 2.2, "riser", 1.0),
]
cues = {"duration": TOTAL, "sections": [{"start": 0, "end": TOTAL, "mood": "silence"}],
        "sfx": [{"t": round(T(k, t), 3), "type": typ, "gain": g} for k, t, typ, g in CUES]}
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


dip(0.0, pick - 0.05, 0.3)                                         # which voice is real
dip(T("siege", 0.0), T("window", -0.2), 0.12)                      # the siege and the sneak: knocks and creaks on near-silence
dip(T("call", vo_t("call", 1) - 0.1), T("phone", -0.3), 0.0, 0.05)  # the call: the music drops out
mus = mus * gain
fade = int(1.2 * SR)
end = int(T("phone", -0.22) * SR)
mus[end - fade:end] *= np.linspace(1, 0.25, fade)
mus[end:] = 0  # hard cut to black and silence

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
k = int(0.25 * SR)
duck = box(duck, k)
mix = vo + mus * duck + sfx
cut = int(T("phone", -0.22) * SR)  # the episode ends on a hard cut to black and silence
mix[cut - 240:cut] *= np.linspace(1, 0, 240)
mix[cut:] = 0
peak = np.max(np.abs(mix))
if peak > 0.98:
    mix = np.tanh(mix / peak * 1.2) * 0.95
out = os.path.join(HERE, "mix_raw.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", out],
               input=mix.astype(np.float32).tobytes(), check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)
print("mix written", TOTAL)

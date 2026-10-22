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
open_choice = vo_t("open", 1) + 2.6
turn = vo_t("whistle", 1) - 1.75
strike = 0.95
scare = SH["window"]["dur"] - 0.95
CUES = [
    ("open", 0.0, "crickets", 0.7), ("open", 0.0, "wind", 0.5), ("open", 1.15, "pop", 0.8),
    *[("open", open_choice + k, "tick", 1.0) for k in range(4)], ("open", -0.2, "whoosh", 0.8),
    ("arrive", 0.35, "swell", 0.5), *[("arrive", vo_t("arrive", 1) + k * 0.55, "pop", 0.6) for k in range(3)],
    ("ranger", 0.0, "rustle", 0.6), ("ranger", 2.0, "notif", 0.5),
    ("van", 0.5, "crank", 1.0), ("van", 0.9, "glitch", 0.35), ("van", -1.6, "rustle", 0.6),
    ("fire", 0.0, "crackle", 1.0), ("fire", 0.0, "crickets", 0.6), ("fire", vo_t("fire", 1) + 0.45, "shutter", 1.0), ("fire", vo_t("fire", 1) + 0.5, "sting", 0.6),
    ("call", 0.0, "crackle", 0.6), ("call", 0.0, "crickets", 0.5), ("call", 1.0, "rustle", 0.7),
    *[("call", 1.5 + k * 0.8, "heartbeat", 0.9) for k in range(4)],
    ("choice", 0.0, "crackle", 0.5), *[("choice", 0.1 + k * 0.75, "tick", 1.1) for k in range(4)], ("choice", 2.35, "ding", 0.7),
    ("choice", vo_t("choice") + 2.1, "whoosh", 0.9), ("choice", vo_t("choice") + 2.2, "rustle", 0.9),
    ("lost", 0.0, "crickets", 0.6), ("lost", 0.1, "rustle", 0.6), ("lost", 0.3, "notif", 0.4),
    ("stop", 0.0, "crickets", 0.6), *[("stop", 0.25 + k * 0.32, "pop", 0.45) for k in range(4)],
    ("whistle", 0.0, "crickets", 0.5), *[("whistle", t, "whistle", 1.0) for t in (0.15, 0.6, 1.05)], ("whistle", 1.5, "notif", 0.35),
    *[("whistle", turn - d, "whistlefar", 1.4) for d in (1.3, 0.85, 0.4)], ("whistle", turn, "sting", 0.9),
    ("whistle", turn + 0.2, "heartbeat", 1.0), ("whistle", turn + 0.9, "heartbeat", 1.0),
    ("hide", 0.15, "snap", 0.8), ("hide", 0.6, "trumpet", 1.0), *[("hide", 0.3 + k * 0.8, "stomp", 0.7 - k * 0.05) for k in range(11)],
    *[("hide", 1.0 + k * 0.7, "heartbeat", 0.9) for k in range(3)], ("hide", vo_t("hide", 1) - 0.8, "ding", 0.6), ("hide", vo_t("hide", 1) + 0.1, "notif", 0.35),
    ("snake", 0.0, "rustle", 0.7), ("snake", 0.3, "hiss", 0.9), ("snake", strike, "boom", 0.55), ("snake", strike, "sting", 1.0), ("snake", strike + 0.5, "glitch", 0.4),
    ("firstaid", 0.0, "crickets", 0.5), ("firstaid", 2.6, "rustle", 0.6), ("firstaid", 0.35, "notif", 0.35),
    ("firstaid", vo_t("firstaid", 1) + 0.2, "notif", 0.4), ("firstaid", -1.6, "ding", 0.5),
    ("radio", 0.15, "static", 0.8), ("radio", 0.6, "notif", 0.35), ("radio", vo_t("radio", 1) - 0.1, "static", 0.5),
    ("radio", vo_t("radio", 1) + 0.3, "siren", 0.45), ("radio", vo_t("radio", 1), "swell", 0.45),
    ("message", 0.15, "notif", 1.0), ("message", 1.15, "ding", 0.6), *[("message", 1.6 + k * 0.75, "heartbeat", 1.0) for k in range(6)], ("message", vo_t("message"), "sting", 0.7),
    ("who", 0.0, "hum", 0.7), ("who", 1.0, "glitch", 0.6), *[("who", 0.3 + k * 0.7, "heartbeat", 1.0) for k in range(6)],
    ("window", 0.0, "wind", 0.5), ("window", 0.0, "crickets", 0.4), *[("window", 0.6 + k * 0.7, "heartbeat", 0.8 + k * 0.05) for k in range(6)],
    ("window", scare, "sting", 1.5), ("window", scare, "boom", 1.0), ("window", scare, "glitch", 1.0),
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


dip(0.0, 1.1, 0.0, 0.05)                                           # cold open: the whisper on silence
dip(T("call", 0.0), T("call", 4.0), 0.3)                           # the voice from the trees
dip(T("whistle", turn - 1.6), T("whistle", turn + 0.4), 0.05)      # listening for the answer
dip(T("hide", 0.0), T("hide", 1.6), 0.1)                           # the elephant arrives
dip(T("snake", 0.4), T("snake", strike + 0.1), 0.05)               # silence before the strike
dip(T("message", 0.8), T("message", -0.2), 0.25)                   # the twist lands
dip(T("window", scare - 1.2), T("window", scare - 0.02), 0.03)     # nothing… then the face
mus = mus * gain
fade = int(1.2 * SR)
end = int(T("window", -0.4) * SR)
mus[end - fade:end] *= np.linspace(1, 0.25, fade)
mus[end:] *= np.linspace(0.25, 0, N - end)

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
k = int(0.25 * SR)
duck = box(duck, k)
mix = vo + mus * duck + sfx
peak = np.max(np.abs(mix))
if peak > 0.98:
    mix = np.tanh(mix / peak * 1.2) * 0.95
out = os.path.join(HERE, "mix_raw.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", out],
               input=mix.astype(np.float32).tobytes(), check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)
print("mix written", TOTAL)

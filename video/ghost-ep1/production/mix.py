"""Build the episode soundtrack from schedule.json: narration + dialogue, synthesized SFX and the Suno
music bed with horror dips before the scares and sidechain ducking under the voice. Output -14 LUFS."""
import json
import os
import subprocess
import sys

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


def lufs_norm(x, target):
    rms = np.sqrt(np.mean(x[np.abs(x) > 1e-4] ** 2)) + 1e-9
    return x * (10 ** ((target + 3.0) / 20) / rms)  # rough RMS-based level match, final loudnorm fixes it


# ---- voice ----
vo = np.zeros(N, np.float32)
for s in SC["shots"]:
    for v in s["vo"]:
        place(vo, load(os.path.join(HERE, "vo", f"{v['id']}.wav")), s["start"] + v["t"])

# ---- sfx (relative to shot start; negative = from shot end) ----
def T(k, t):
    s = SH[k]
    return s["start"] + (t if t >= 0 else s["dur"] + t)

CUES = [
    ("open", 0.1, "knock", 1.2), ("open", 0.0, "wind", 0.8), ("open", 0.95, "thunder", 1.0),
    ("flash", 0.0, "whoosh", 1.0), ("flash", 1.0, "sting", 1.0), ("flash", 2.0, "heartbeat", 1.2), ("flash", 2.0, "whoosh", 0.8),
    ("arrive", 1.8, "meow", 0.8),
    ("storm", 0.0, "wind", 1.0), ("storm", 0.5, "pop", 1.2), ("storm", 0.55, "buzz", 0.8), ("storm", 1.6, "thunder", 0.9),
    ("mistake1", 0.3, "hum", 1.0), ("mistake1", -0.9, "boom", 0.45), ("mistake1", -0.9, "heartbeat", 1.0),
    ("exhaust", 0.0, "hum", 1.0), ("exhaust", 1.2, "tick", 1.0), ("exhaust", 2.2, "tick", 1.0), ("exhaust", -0.75, "knock", 1.3),
    ("cat", 0.0, "hum", 0.7), ("cat", 1.1, "meow", 0.6), ("cat", 2.8, "creak", 1.0),
    ("knock", 0.1, "knock", 1.3), ("knock", -1.45, "sting", 1.2), ("knock", -1.45, "boom", 0.6),
    ("headache", 0.2, "heartbeat", 1.2), ("headache", 1.0, "heartbeat", 1.2), ("headache", 1.8, "heartbeat", 1.2), ("headache", 2.6, "heartbeat", 1.2),
    ("mistake2", 0.0, "hum", 0.6), ("mistake2", 1.4, "heartbeat", 0.9),
    ("losttime", 0.6, "tick", 1.0), ("losttime", 1.4, "tick", 1.0), ("losttime", 2.2, "creak", 1.0),
    ("ghost", 0.3, "heartbeat", 1.0), ("ghost", 1.2, "heartbeat", 1.1), ("ghost", -1.0, "sting", 1.4), ("ghost", -1.0, "boom", 0.9), ("ghost", -0.98, "glitch", 1.0),
    ("wake", 0.0, "whoosh", 0.8), ("wake", 0.6, "creak", 1.0),
    ("symptoms", 0.1, "heartbeat", 1.0), ("symptoms", 0.8, "heartbeat", 1.0), ("symptoms", 1.5, "heartbeat", 1.0),
    ("catfirst", 0.6, "meow", 0.5),
    ("xray", 0.0, "whoosh", 1.0), ("xray", 0.2, "hum", 1.3), ("xray", 1.0, "riser", 0.7),
    ("escape", 0.0, "whoosh", 1.0), ("escape", 0.3, "heartbeat", 1.0), ("escape", -1.1, "pop", 1.2),
    ("block", 0.5, "sting", 0.8),
    ("call", 0.5, "tick", 1.0), ("call", 1.2, "tick", 1.0), ("call", 1.9, "tick", 1.0), ("call", -1.4, "ding", 1.0),
    ("rescue", 0.0, "siren", 1.0), ("rescue", 2.4, "siren", 0.8),
    ("who", -1.0, "sting", 0.7),
    ("stillhere", 0.2, "hiss", 1.0), ("stillhere", 0.0, "wind", 0.6), ("stillhere", -1.4, "knock", 1.4), ("stillhere", -0.25, "boom", 0.7),
    ("end", 0.3, "sting", 0.8), ("end", -1.2, "meow", 0.7),
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
if len(mus) < N:
    mus = np.concatenate([mus, mus])
mus = mus[:N]
t = np.arange(N) / SR
gain = np.ones(N, np.float32)
def dip(t0, t1, level, ramp=0.25):
    a = np.clip((t - (t0 - ramp)) / ramp, 0, 1) * np.clip(((t1 + ramp) - t) / ramp, 0, 1)
    np.minimum(gain, 1 - (1 - level) * a, out=gain)
dip(0.0, 1.2, 0.0, 0.05)                                   # cold open: knocks on silence
for k, before in (("knock", 1.45), ("ghost", 1.0), ("stillhere", 1.4)):
    dip(T(k, -before) - 0.8, T(k, -before) + 0.6, 0.08)   # suck the music out just before each scare
dip(T("end", 0), TOTAL, 0.6)
gain[: int(0.05 * SR)] = 0
mus = mus * gain
fade = int(1.5 * SR)
mus[-fade:] *= np.linspace(1, 0, fade)

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
vo = lufs_norm(vo, -15)
mus = lufs_norm(mus, -25)
sfx = lufs_norm(sfx, -24)
env = np.convolve(np.abs(vo), np.ones(int(0.05 * SR)) / int(0.05 * SR), mode="same")
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
k = int(0.25 * SR)
duck = np.convolve(duck, np.ones(k) / k, mode="same")
mix = vo + mus * duck + sfx
peak = np.max(np.abs(mix))
if peak > 0.98:
    mix = np.tanh(mix / peak * 1.2) * 0.95
out = os.path.join(HERE, "mix_raw.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", out],
               input=mix.astype(np.float32).tobytes(), check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)
print("mix written", TOTAL)

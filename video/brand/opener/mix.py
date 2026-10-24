"""Sound for the opener demo: the EP.1 hook voices, music, and the dive (whoosh through the cloud, boom on landing)."""
import json
import os
import subprocess

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
SC = json.load(open(os.path.join(HERE, "schedule.json")))
TOTAL = SC["total"]
N = int(TOTAL * SR)
AT, GLIDE = 1.9, 1.9  # same as OP in shots.part


def load(path):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, dtype=np.float32).copy()


def place(buf, x, t, g=1.0):
    i = int(t * SR)
    j = min(len(buf), i + len(x))
    if i < len(buf):
        buf[i:j] += x[: j - i] * g


def level(x, target):
    r = 20 * np.log10(np.sqrt(np.mean(x[np.abs(x) > 1e-4] ** 2)) + 1e-9)
    return x * 10 ** ((target - r) / 20)


vo = np.zeros(N, np.float32)
for v in SC["shots"][0]["vo"]:
    place(vo, load(os.path.join(HERE, "..", "mok1", "vo", f"{v['id']}.wav")), v["t"])
cues = {"duration": TOTAL, "sections": [{"start": 0, "end": TOTAL, "mood": "silence"}],
        "sfx": [{"t": 0.05, "type": "swell", "gain": 0.5}, {"t": AT - 0.05, "type": "whoosh", "gain": 0.9}, {"t": AT + GLIDE * 0.45, "type": "whoosh", "gain": 0.7},
                {"t": AT + GLIDE - 0.05, "type": "boom", "gain": 0.6}, {"t": 3.98, "type": "sting", "gain": 0.8}]}
json.dump(cues, open(os.path.join(HERE, "sfx_cues.json"), "w"))
subprocess.run(["python3", os.path.join(HERE, "..", "synth.py"), os.path.join(HERE, "sfx_cues.json"), os.path.join(HERE, "sfx.wav")],
               check=True, env={**os.environ, "STEMS": "1"})
sfx = load(os.path.join(HERE, "sfx_sfx.wav"))[:N]
sfx = np.pad(sfx, (0, N - len(sfx)))
mus = load(os.path.join(HERE, "..", "music", "suno1.mp3"))[:N]
mus = np.pad(mus, (0, N - len(mus)))
t = np.arange(N) / SR
mus *= np.clip(t / 0.6, 0, 1) * np.clip((TOTAL - t) / 0.5, 0, 1)
vo, mus, sfx = vo, level(mus, -28), level(sfx, -27)
mix = vo + mus * 0.6 + sfx
peak = np.max(np.abs(mix))
if peak > 0.98:
    mix = np.tanh(mix / peak * 1.2) * 0.95
out = os.path.join(HERE, "mix_raw.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", out], input=mix.astype(np.float32).tobytes(), check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)
print("mix written", TOTAL)

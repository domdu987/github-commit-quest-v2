"""Soundtrack for the systems demo: synthesized SFX (page, pen, stickers, the assembly clang, the countdown ticks and
heartbeat, the horde, the door) over the Suno bed, -14 LUFS."""
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
D = {k: SH[k]["dur"] for k in SH}


def load(path):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, dtype=np.float32).copy()


def rms_db(x):
    x = x[np.abs(x) > 1e-4]
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)


def level(x, target):
    return x * 10 ** ((target - rms_db(x)) / 20)


def T(k, t):
    s = SH[k]
    return s["start"] + (t if t >= 0 else s["dur"] + t)


def beats(k, t0, dur, period, g=0.9):
    return [(k, t0 + i * period, "heartbeat", g) for i in range(int((dur - 0.1) / period) + 1)]


def bed(kind, a, b, g, step=4.6):
    out, t = [], a - 0.6
    while t < b - 1.0:
        out.append((None, t, kind, g))
        t += step
    return out


def growls(k, a, b, g=0.7, step=0.7):
    return [(k, a + i * step, "growl", g * (0.7 + 0.3 * (i % 2))) for i in range(int((b - a) / step))]


CUES = [
    *bed("wind", T("title", 0), T("roster", -0.1), 0.35, 3.2), ("title", 0.3, "page", 0.7), ("title", 0.5, "slam", 0.6), ("title", 0.9, "riser", 0.5), ("title", -0.2, "whoosh", 0.8),
    # the register: page, tape, one row at a time (sticker pop, pen, stamp)
    ("roster", 0.3, "page", 0.8), ("roster", 0.7, "rustle", 0.4), ("roster", 0.65, "slam", 0.5),
    *[c for k in range(5) for c in (("roster", 0.9 + k * 1.2, "pop", 0.5), ("roster", 1.05 + k * 1.2, "marker", 0.35), ("roster", 1.25 + k * 1.2, "slam", 0.45), ("roster", 1.45 + k * 1.2, "ding", 0.3))],
    ("roster", -0.3, "whoosh", 0.5),
    # the recipe: pen boxes, three finds (rustle + pop + tick), the assembly (whoosh, clang, boom), stats, the upgrade
    *bed("crickets", T("craft", 0), T("craft", -0.1), 0.4, 4.6), ("craft", 0.4, "page", 0.8), ("craft", 0.7, "slam", 0.5), ("craft", 0.8, "marker", 0.4), ("craft", 1.0, "marker", 0.3),
    *[c for k, at in enumerate((1.2, 2.3, 3.4)) for c in (("craft", at - 0.15, "rustle", 0.5), ("craft", at + 0.28, "pop", 0.6), ("craft", at + 0.3, "thud", 0.3), ("craft", at + 0.5, "marker", 0.3), ("craft", at + 0.85, "ding", 0.4))],
    ("craft", 4.6, "whoosh", 0.8), ("craft", 4.75, "whoosh", 0.6), ("craft", 5.15, "clang", 1.1), ("craft", 5.15, "boom", 0.6), ("craft", 5.2, "sting", 0.5), ("craft", 5.55, "slam", 0.7), ("craft", 5.6, "pop", 0.5),
    *[("craft", 5.7 + k * 0.09, "tick", 0.25) for k in range(7)],
    ("craft", 8.0, "rustle", 0.5), ("craft", 8.05, "pop", 0.5), ("craft", 8.5, "slam", 0.6), ("craft", 8.85, "clang", 0.9), ("craft", 8.85, "glitch", 0.3), ("craft", 8.9, "sting", 0.6), *[("craft", 9.1 + k * 0.08, "tick", 0.3) for k in range(5)],
    ("craft", 7.4, "pop", 0.5), ("craft", 7.6, "slam", 0.45),   # ลุงหมาน's skill card
    ("craft", 1.3, "rustle", 0.6), ("craft", 1.9, "thud", 0.4), ("craft", 2.4, "rustle", 0.5), ("craft", 2.98, "clang", 0.45), ("craft", 3.45, "rustle", 0.5), ("craft", 3.75, "rustle", 0.45), ("craft", 4.05, "rustle", 0.45), ("craft", 4.5, "thud", 0.3),   # the hands: pick up, set the knife, wind the tape
    ("craft", 8.3, "rustle", 0.5), ("craft", 8.6, "whoosh", 0.5),
    ("craft", -0.3, "whoosh", 0.5),
    # the countdown: the generator, the horde at the fence, a tick every second, the heart speeding up, the card
    *bed("horde", T("count", 0), T("count2", -0.4), 0.55, 4.6), *bed("crickets", T("count", 0), T("count2", -0.4), 0.3, 4.6), *growls("count", 0.4, D["count"], 0.5, 0.8),
    ("count", 0.2, "page", 0.7), ("count", 0.45, "slam", 0.5), *[("count", 1.2 + k, "tick", 0.75) for k in range(12)], *beats("count", 0.2, D["count"] - 0.2, 0.6, 0.6),
    ("count", 3.2, "pop", 0.5), ("count", 3.4, "slam", 0.45), ("count", 4.4, "latch", 0.8), ("count", 4.6, "buzz", 0.5), ("count", 5.3, "clang", 0.6),
    ("count", 6.5, "steps", 0.6), ("count", 7.2, "steps", 0.6), ("count", 7.9, "steps", 0.6), ("count", 8.6, "steps", 0.6), ("count", 9.3, "steps", 0.6), ("count", 10.0, "steps", 0.6), ("count", 10.7, "steps", 0.6), ("count", 11.4, "steps", 0.6),
    ("count", -0.3, "riser", 0.8),
    *growls("count2", 0.0, D["count2"] - 1.5, 0.7, 0.5), *[("count2", 1.0 + k, "tick", 1.0) for k in range(5)], *beats("count2", 0.0, 5.0, 0.36, 0.9), *[("count2", 1.0 + k, "sting", 0.35) for k in range(4)],
    ("count2", 0.3, "steps", 0.8), ("count2", 0.9, "steps", 0.8), ("count2", 1.5, "steps", 0.8), ("count2", 2.1, "steps", 0.8), ("count2", 2.7, "steps", 0.8), ("count2", 3.3, "steps", 0.8), ("count2", 3.9, "steps", 0.9),
    ("count2", 4.3, "shriek", 0.8), ("count2", 5.0, "slam", 1.3), ("count2", 5.0, "boom", 0.9), ("count2", 5.05, "gate", 0.8), ("count2", 5.25, "latch", 1.0), ("count2", 5.5, "thud", 0.6),
]
cues = {"duration": TOTAL, "sections": [{"start": 0, "end": TOTAL, "mood": "silence"}],
        "sfx": [{"t": round(t if k is None else T(k, t), 3), "type": typ, "gain": g} for k, t, typ, g in CUES]}
json.dump(cues, open(os.path.join(HERE, "sfx_cues.json"), "w"))
subprocess.run(["python3", os.path.join(HERE, "..", "synth.py"), os.path.join(HERE, "sfx_cues.json"), os.path.join(HERE, "sfx.wav")], check=True, env={**os.environ, "STEMS": "1"})
sfx = load(os.path.join(HERE, "sfx_sfx.wav"))[:N]
sfx = np.pad(sfx, (0, N - len(sfx)))

mus = load(os.path.join(HERE, "..", "music", "suno1.mp3"))
while len(mus) < N:
    mus = np.concatenate([mus, mus])
mus = mus[:N]
t = np.arange(N) / SR
gain = np.ones(N, np.float32)


def dip(t0, t1, lvl, ramp=0.25):
    a = np.clip((t - (t0 - ramp)) / ramp, 0, 1) * np.clip(((t1 + ramp) - t) / ramp, 0, 1)
    np.minimum(gain, 1 - (1 - lvl) * a, out=gain)


dip(T("count", 0), T("count2", 5.0), 0.55)
mus = mus * gain
end = int(T("count2", 5.0) * SR)
mus[end:] = 0
mus = level(mus, -28)
sfx = level(sfx, -24)
mix = mus + sfx
mix[end - 240:end] *= np.linspace(1, 0.3, 240)
mix[end:] *= 0.3
mix = np.clip(mix, -1, 1)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", str(SR), os.path.join(HERE, "mix.wav")], input=mix.astype(np.float32).tobytes(), check=True)
print("mix", TOTAL)

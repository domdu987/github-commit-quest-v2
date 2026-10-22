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


oc = vo_t("open", 1) + 2.6
run_f = vo_t("choice") + SH["choice"]["vo"][0]["dur"] + 0.1
ans = [vo_t("whistle", 1) - d for d in (2.1, 1.65, 1.2)]
find = 2.3
lurch = [1.3, 2.1, 2.9, 3.6]
fin_c = vo_t("final") + SH["final"]["vo"][0]["dur"] + 0.1
CUES = [
    ("open", 0.0, "crickets", 0.7), ("open", 0.0, "wind", 0.5), ("open", 1.15, "pop", 0.9), ("open", 0.35, "glitch", 0.5), ("open", 1.85, "glitch", 0.4),
    *beats("open", 1.3, D["open"] - 1.4, 0.72, 0.8), *[("open", oc + k, "tick", 1.0) for k in range(4)], ("open", -0.2, "whoosh", 0.8),
    ("arrive", 0.2, "glitch", 0.4), ("arrive", 0.4, "whoosh", 0.7), *ticks("arrive", 0.55, 2.1, 0.07, 0.45), ("arrive", 2.1, "swell", 0.5),
    *[("arrive", vo_t("arrive", 1) + k * 0.55, "pop", 0.6) for k in range(3)],
    ("ranger", 0.0, "rustle", 0.6), ("ranger", 1.2, "notif", 0.45), ("ranger", vo_t("ranger") + 3.2, "sting", 0.45), ("ranger", vo_t("ranger") + 5.4, "boom", 0.35),
    ("van", 0.25, "notif", 0.35), ("van", 0.5, "crank", 1.0), ("van", 1.95, "buzz", 0.5), ("van", vo_t("van", 1) + 0.05, "glitch", 0.35),
    ("van", vo_t("van", 2) + 0.1, "notif", 0.35), ("van", vo_t("van", 2) + 2.0, "rustle", 0.6),
    ("fire", 0.0, "crackle", 1.0), ("fire", 0.0, "crickets", 0.6), *ticks("fire", 0.5, 2.4, 0.08, 0.4), ("fire", 2.45, "ding", 0.5),
    ("call", 0.0, "crackle", 0.6), ("call", 0.0, "crickets", 0.4), *[("call", 0.7 + i * 0.28, "pop", 0.35) for i in range(9)],
    *[("call", k, "glitch", 0.45) for k in (0.6, 2.0, 3.4)], *beats("call", 1.2, D["call"] - 1.2, 0.7, 0.85),
    *beats("callpov", 0.0, D["callpov"], 0.6, 0.9), ("callpov", 0.75, "sting", 0.8), ("callpov", vo_t("callpov") - 0.15, "whoosh", 0.8),
    ("choice", 0.0, "crackle", 0.5), *[("choice", 0.1 + k * 0.75, "tick", 1.1) for k in range(4)], *beats("choice", 0.2, 2.2, 0.55, 0.8), ("choice", 2.25, "ding", 0.7),
    ("choice", 2.85, "notif", 0.4), ("choice", run_f, "whoosh", 0.9), ("choice", run_f + 0.1, "rustle", 0.9), ("choice", run_f + 0.6, "rustle", 0.8),
    ("lost", 0.0, "crickets", 0.6), ("lost", 0.1, "rustle", 0.6), *ticks("lost", 0.5, 1.4, 0.08, 0.35), ("lost", 0.4, "notif", 0.35), ("lost", 1.8, "sting", 0.35),
    ("stop", 0.0, "crickets", 0.6), *[("stop", 0.25 + k * 0.32, "pop", 0.45) for k in range(4)],
    ("whistle", 0.0, "crickets", 0.5), *[("whistle", t, "whistle", 1.0) for t in (0.15, 0.6, 1.05)], ("whistle", 1.4, "notif", 0.35),
    *[("whistle", t, "whistlefar", 1.4) for t in ans], ("whistle", ans[0], "sting", 0.9), *beats("whistle", ans[0], D["whistle"] - ans[0], 0.6, 0.9),
    *beats("hush", 0.0, D["hush"], 0.5, 1.0), ("hush", 1.2, "rustle", 0.7), ("hush", 1.4, "snap", 0.7), ("hush", 2.6, "snap", 0.9), ("hush", 3.4, "pop", 0.4),
    ("reveal", 0.5, "pop", 0.9), ("reveal", 0.6, "rustle", 0.5), ("reveal", find, "sting", 1.3), ("reveal", find, "boom", 0.6),
    ("reveal", vo_t("reveal"), "glitch", 0.6), ("reveal", vo_t("reveal") + 2.0, "glitch", 0.5), ("reveal", 3.6, "buzz", 0.5), *beats("reveal", find, D["reveal"] - find, 0.5, 0.9),
    *beats("twoshot", vo_t("twoshot", 1), D["twoshot"] - vo_t("twoshot", 1), 0.5, 0.9), ("twoshot", vo_t("twoshot", 1), "sting", 0.6), ("twoshot", 0.1, "rustle", 0.6),
    ("eyes", 0.05, "boom", 0.55), ("eyes", 0.05, "sting", 1.0), ("eyes", 0.05, "glitch", 0.6), ("eyes", 0.5, "notif", 0.3), *beats("eyes", 0.0, D["eyes"], 0.48, 0.9),
    *beats("final", 0.0, D["final"] - 0.3, 0.4, 1.0), ("final", vo_t("final"), "glitch", 0.7), *[("final", t, "stomp", 0.7) for t in lurch], *[("final", t, "snap", 0.6) for t in lurch],
    ("final", lurch[3], "glitch", 0.8), *[("final", t, "buzz", 0.45) for t in (1.2, 3.2, 5.2)], *[("final", fin_c + k * 0.5, "tick", 1.1) for k in range(int((D["final"] - 0.3 - fin_c) / 0.5))],
    ("final", D["final"] - 2.3, "riser", 1.0),
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


dip(0.0, 1.15, 0.0, 0.05)                                          # cold open: the whisper on silence
dip(T("call", 0.0), T("callpov", -0.1), 0.25)                      # the voice from the trees
dip(T("whistle", ans[0] - 0.6), T("whistle", -0.1), 0.15)          # listening for the answer
dip(T("hush", 0.0), T("reveal", find - 0.05), 0.0, 0.1)            # silence: hold your breath
dip(T("final", 0.0), T("final", -0.3), 0.45)
mus = mus * gain
fade = int(1.2 * SR)
end = int(T("final", -0.22) * SR)
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
cut = int(T("final", -0.22) * SR)  # the episode ends on a hard cut to black and silence
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

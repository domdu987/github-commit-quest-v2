"""ทางกลับบ้าน EP.N: the soundtrack from schedule.json: levelled voice, synthesized SFX (crickets, engine, the lock click, the countdown
ticks, the screech, the splash, water pouring in, bubbles, the window motor, the rewind, the child's switch, the flicker) and the Suno bed
with dips and ducking; the bed fades out over the next-episode card. Output -14 LUFS, no noise beds."""
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


# ---- voice ----
LINE_GAIN = {}
vo = np.zeros(N, np.float32)
for s in SC["shots"]:
    for v in s["vo"]:
        x = load(os.path.join(HERE, "vo", f"{v['id']}.wav"))
        place(vo, level(x, -18 + LINE_GAIN.get(v["id"], 0)), s["start"] + v["t"])
D = {k: SH[k]["dur"] for k in SH}
F = frag


def beats(k, t0, dur, period, g=0.9):
    return [(k, t0 + i * period, "heartbeat", g) for i in range(int((dur - 0.1) / period) + 1)]


exec(open(os.path.join(HERE, "..", "samples_inc.py")).read())
REPLACED = set()
SFXLIB = "/home/user/github-commit-quest-v2/video/war/sfxlib"
CUES = [
    ("cmd", 0.05, "sting", 0.4), ("rule", vo_end("rule") - 1.0, "whoosh", 0.25), ("hide", 0.1, "whoosh", 0.25),
    ("cover", vo_t("cover") + 3.0, "ding", 0.2), ("cover", vo_t("cover") + 3.9, "ding", 0.2), ("cover", vo_t("cover") + 4.8, "ding", 0.2), ("cover", vo_t("cover") + 4.1, "ding", 0.2),
    ("down", 0.2, "ding", 0.16), ("ditch", 0.1, "swell", 0.2), ("law", 0.9, "ding", 0.18), ("law", vo_t("law") + 3.2, "ding", 0.18),
    ("bandage", vo_t("bandage") + 2.8, "ding", 0.2), ("rule2", vo_end("rule2") + 0.3, "ding", 0.25),
    ("home", 0.1, "swell", 0.2), ("parcel", 0.3, "sting", 0.25), ("open", vo_t("open") + 3.3, "swell", 0.24), ("open", D["open"] - 1.1, "sting", 0.45),
    *beats("choice", 0.2, D["choice"] - 0.2, 0.5, 0.3), ("choice", D["choice"] - 0.8, "ding", 0.3),
    ("end", 0.1, "whoosh", 0.3), ("end", 0.8, "ding", 0.24),
]
CARDS = [  # the in-world cards make the sound of their material (owner 1 Nov)
    ("hide", 0.1, "canvas", 0.7), ("hide", 0.7, "pencil", 0.25), ("hide", 2.2, "pencil", 0.2),
    *[x for t in (frag("cover", 0, 1), frag("cover", 0, 1) + 0.9, frag("cover", 0, 1) + 1.8, frag("cover", 0, 2) + 0.2) for x in (("cover", t, "spray", 0.45), ("cover", t + 0.25, "stake", 0.5))],
    ("down", vo_t("down") - 0.05, "buckle", 0.6), ("down", vo_t("down") + 0.1, "spray", 0.4), ("down", frag("down", 0, 1), "spray", 0.4), ("down", frag("down", 0, 2), "spray", 0.4),
    ("law", vo_t("law") + 0.65, "buckle", 0.55), ("law", vo_t("law") + 0.8, "spray", 0.4), ("law", frag("law", 0, 1), "spray", 0.4),
    ("bandage", frag("bandage", 0, 2), "spray", 0.4), ("bandage", frag("bandage", 0, 2) + 0.25, "stake", 0.5),
    ("choice", 0.0, "canvas", 0.7), ("choice", 0.6, "pencil", 0.45), ("choice", D["choice"] - 1.4, "pencil", 0.55), ("choice", D["choice"] - 1.0, "pencil", 0.55),
]
SAMPLES = [
    ("hook", 0.0, "whiz", 0.4), ("hook", 0.0, "leaves", 0.3), ("hook", 0.5, "leaves", 0.25), ("hook", 2.2, "whiz", 0.6), ("hook", 0.0, "field", 0.12, 2.6),
    ("cmd", 1.5, "whiz", 0.5), ("cmd", 1.5, "leaves", 0.4), ("rule", 0.0, "whiz", 0.35), ("rule", 0.0, "field", 0.25, 3.4), ("rule", vo_end("rule") - 0.9, "dogtag", 0.8),
    ("hide", 0.0, "field", 0.2, 5.7), ("cover", 0.0, "field", 0.3, 6.6), ("cover", 0.0, "distshots", 0.25),
    ("down", 0.0, "whiz", 0.35), ("down", 1.1, "whiz", 0.3), ("down", 2.0, "distshots", 0.25), ("down", 2.9, "whiz", 0.3),
    ("ditch", 0.0, "field", 0.15, 5.5), ("joe", 0.0, "field", 0.25, 3.0), ("law", 0.0, "field", 0.25, 6.0),
    ("bandage", 0.0, "field", 0.25, 4.7), ("bandage", 2.0, "truck", 0.3), ("rule2", 0.0, "dogtag", 0.8),
    
    ("home", 0.0, "songkran", 0.22, 3.3), ("hug", 0.0, "songkran", 0.3, 3.0), ("parcel", 0.0, "songkran", 0.25, 3.7), ("open", 0.1, "parcel", 0.7),
]


def music_dips(dip):
    dip(T("ditch", 0), T("joe", -0.01), 0.45)                 # the guns stop: quiet
    dip(T("open", 0), T("open", frag("open", 0, 2)), 0.35)    # the hush before the note, then the theme's peak lands on it
BOOST = [("hook", 1.9, 0.7, 1.5), ("down", 0.0, 0.3, 1.3)]   # push only in the gaps between lines
# no hiss: the noise-based wind bed reads as static under the voice (user: "ลบเสียงซ่าออก")
CUES = [c for c in CUES if c[2] not in ("wind", "lap", "pop", "tick") and c[3] > 0]   # no HUD: no chip pops, no countdown ticks (user 31 ต.ค.)  # no noise beds (user: "เสียงซ่าๆเอาออก")
cues = {"duration": TOTAL, "sections": [{"start": 0, "end": TOTAL, "mood": "silence"}],
        "sfx": [{"t": round(t if k is None else T(k, t), 3), "type": typ, "gain": g} for k, t, typ, g in CUES]}
json.dump(cues, open(os.path.join(HERE, "sfx_cues.json"), "w"))
subprocess.run(["python3", os.path.join(HERE, "..", "synth.py"), os.path.join(HERE, "sfx_cues.json"), os.path.join(HERE, "sfx.wav")],
               check=True, env={**os.environ, "STEMS": "1"})
sfx = load(os.path.join(HERE, "sfx_sfx.wav"))[:N]
sfx = np.pad(sfx, (0, N - len(sfx)))
for k, t0, name, g, *mx in SAMPLES + CARDS:
    place(sfx, smp(name, mx[0] if mx else None), T(k, t0), g)

# ---- music with horror dips ----
mus = load(os.path.join(HERE, "..", "music", "war-theme.mp3"))[int(14.1 * SR):]   # war theme (owner 1 Nov), offset so its peak lands on the cliffhanger
while len(mus) < N:
    mus = np.concatenate([mus, mus])
mus = mus[:N]
t = np.arange(N) / SR
gain = np.ones(N, np.float32)


def dip(t0, t1, lvl, ramp=0.25):
    a = np.clip((t - (t0 - ramp)) / ramp, 0, 1) * np.clip(((t1 + ramp) - t) / ramp, 0, 1)
    np.minimum(gain, 1 - (1 - lvl) * a, out=gain)


music_dips(dip)
for k, a0, d0, g0 in BOOST:
    gain[int(T(k, a0) * SR):int(T(k, a0 + d0) * SR)] *= g0
mus = mus * gain
a, b = int(T("end", 0) * SR), int(T("end", -0.01) * SR)
mus[a:b] *= np.linspace(1, 0, b - a)   # no cliffhanger: the bed fades out over the end card
mus[b:] = 0

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30)
sfx = level(sfx, -27)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mix = vo + mus * duck + sfx
peak = np.max(np.abs(mix))
if peak > 0.98:
    mix = np.tanh(mix / peak * 1.2) * 0.95
out = os.path.join(HERE, "mix_raw.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", out],
               input=mix.astype(np.float32).tobytes(), check=True)
# single-pass loudnorm lands ~0.8 dB under its target on this mix: aim at -13.2 to measure -14
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", "loudnorm=I=-13.2:TP=-1.5:LRA=11", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)
print("mix written", TOTAL)

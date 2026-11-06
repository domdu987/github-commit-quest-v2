"""หนวดใส EP.1 (from the ทะเลลด EP.1 mix): build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX (the wash pulling
back off the title, the flopping fish, the clock spinning back, the van on the map, the shallows under running feet, the live's pings,
the tower's 08:00 test tone, the shadow screen's gong, the deep boom of the quake, the glass's faint ring, the seabed's mud and the
shutter clicks, the conch, the run, the surge round the shop, heartbeats once ยาย is missing, the choice's ticks) and the Suno
music bed with dips and sidechain ducking under the voice. The music stops when the screen goes black after the choice.
Output -14 LUFS. No noise beds and no high hiss (user: "เสียงซ่าๆเอาออก")."""
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


# ---- voice: lane B's takes (vo/<id>.wav rebuilt from its cached mp3s, durations identical), each line levelled on its own;
# p03 "โอ๊ย! ขาผม!" is the synthesized kid's scream (kidscream.py) instead of a TTS take ----
LINE_GAIN = {"p03": 1.5}
vo = np.zeros(N, np.float32)
for s in SC["shots"]:
    for v in s["vo"]:
        f = os.path.join(HERE, "kidscream.wav") if v["id"] == "p03" else os.path.join(HERE, "lb", "vo", f"{v['id']}.wav")
        place(vo, level(load(f), -18 + LINE_GAIN.get(v["id"], 0)), s["start"] + v["t"])

D = {k: SH[k]["dur"] for k in SH}
F = frag
def beats(k, t0, dur, period, g=0.9):
    return [(k, t0 + i * period, "heartbeat", g) for i in range(int((dur - 0.1) / period) + 1)]
def ticks(k, a, b, g=0.2, step=1.0):
    return [(k, a + i * step, "tick", g) for i in range(int((b - a) / step) + 1)]
def tick3(k, a, g=0.3):
    return [(k, a + i * 1.0, "tick", g) for i in range(3)]

CUES = [
    # frame 0: the swash runs in over the sand carrying the title; the cap drops; the boy sobs (his scream is in the voice track later)
    ("open", 0.0, "splash", 0.3), ("open", 0.3, "bubbles", 0.16), ("open", 0.05, "plop", 0.18), ("open", 1.4, "squish", 0.14),
    # the hook: the sting on "อย่า", the drop trembling on the lip
    ("hook", vo_t("hook") - 0.02, "sting", 0.36), ("hook", 0.4, "drip", 0.2),
    # สามชั่วโมงก่อน: the sun's shadow swings back
    ("card", 0.15, "rewind", 0.34), ("card", 0.2, "whoosh", 0.2), ("card", D["card"] - 0.35, "thud", 0.18),
    # dawn at ยาย's door: bottles clink in the basket, the floorboards
    ("door", 0.2, "ching", 0.16), ("door", 0.8, "creak", 0.14), ("door", vo_t("door", 2) - 0.1, "rustle", 0.12),
    # the rhyme: the board's lines brushed bright, the HG7 card's bell, น้ำหวาน's song
    ("rhyme", F("rhyme", 0, 1), "marker", 0.22), ("rhyme", F("rhyme", 0, 2), "ding", 0.28), ("rhyme", F("rhyme", 0, 2) + 0.05, "marker", 0.2),
    ("rhyme", F("rhyme", 0, 3), "marker", 0.22), ("rhyme", vo_t("rhyme", 1), "pop", 0.16),
    # ต้น laughs; the photo face down: a held breath
    ("mock", vo_t("mock", 1) + 1.02, "swell", 0.2), ("mock", vo_t("mock", 1) + 1.1, "ching", 0.1),
    # they go; ยาย sets the basket down
    *[("basket", 0.2 + i * 0.4, "steps", 0.1) for i in range(5)], ("basket", F("basket", 0, 2) + 0.4, "thud", 0.22), ("basket", F("basket", 0, 2) + 0.45, "ching", 0.16),
    # the map: the route draws, the pins
    ("map", 0.05, "pop", 0.26), ("map", 0.2, "whoosh", 0.24), ("map", D["map"] - 0.7, "pop", 0.3), ("map", D["map"] - 0.6, "ding", 0.24),
    # the beach: the ring drops, a phone tap, the empty post
    ("beach", 0.3, "plop", 0.26), ("beach", vo_t("beach", 1) + 0.2, "tap", 0.0), ("beach", vo_t("beach", 3), "whoosh", 0.18), ("beach", vo_t("beach", 3) + 0.3, "ching", 0.12),
    # the rock: the REC beep, ภูมิ splashes in
    ("rock", vo_t("rock", 1), "beep", 0.2), *[("rock", vo_t("rock", 1) + 0.4 + i * 0.36, "splash", 0.12) for i in range(5)],
    # the sting: the jolt (the scream is the p03 voice line)
    ("sting", 0.05, "zap", 0.26), ("sting", 0.1, "splash", 0.32), ("sting", 0.2, "bubbles", 0.2),
    # ต้น splashes in shouting
    *[("stingB", 0.1 + i * 0.32, "splash", 0.16) for i in range(int(D["stingB"] / 0.32))],
    # the crowd: bottles cracked open
    ("crowd", 0.2, "click", 0.2), ("crowd", vo_t("crowd", 1) - 0.1, "click", 0.18), ("crowd", vo_t("crowd", 2) - 0.1, "swell", 0.16),
    # the cross-section: water drops, the rubbing, the stingers fire, the venom spreads
    *[("know", 0.15 + i * 0.25, "drip", 0.14) for i in range(7)], ("know", 0.4, "rustle", 0.16),
    *[("know", F("know", 0, 1) + 0.25 + i * 0.12, "snap", 0.12) for i in range(8)], ("know", F("know", 0, 2), "swell", 0.24),
    # the bottle over the leg: the heart
    *beats("choice", 0.1, D["choice"] - 0.1, 0.62, 0.36),
    # he sets it down; the board's rule 1 lights and the tick lands
    ("choiceB", 0.85, "thud", 0.22), ("choiceB", F("choiceB", 0, 1), "marker", 0.22), ("choiceB", F("choiceB", 0, 1) + 0.5, "ding", 0.3),
    # ภูมิ sobs; quiet
    ("choiceC", 0.1, "swell", 0.14),
    # he turns: the heartbeat comes back; the peak: the swarm under the empty ring; "น้ำหวาน…?"
    *beats("gone", 0.3, D["gone"] - 0.3, 0.7, 0.34), ("goneB", 0.05, "riser", 0.26), ("goneB", 0.2, "bubbles", 0.18), *beats("goneB", 0.4, D["goneB"] - 0.4, 0.62, 0.4),
    ("goneC", 0.0, "sting", 0.24), *beats("goneC", 0.3, D["goneC"] - 0.3, 0.55, 0.42),
    # the choice: ticks, the heartbeat, the wave pull → black
    *tick3("vote", 0.3, 0.3), *beats("vote", 0.2, D["vote"] - 0.6, 0.55, 0.38), ("vote", D["vote"] - 1.3, "whoosh", 0.36), ("vote", D["vote"] - 1.2, "splash", 0.4),
    # the end board drops in on its ropes, the buttons pop
    ("endb", 0.1, "whoosh", 0.3), ("endb", 0.6, "thud", 0.2), ("endb", F("endb", 0, 1), "pop", 0.26), ("endb", F("endb", 0, 2), "pop", 0.26),
]

# no hiss: the noise-based wind bed reads as static under the voice (user: "ลบเสียงซ่าออก")
CUES = [c for c in CUES if c[2] not in ("wind", "lap") and c[3] > 0]  # no noise beds (user: "เสียงซ่าๆเอาออก")
cues = {"duration": TOTAL, "sections": [{"start": 0, "end": TOTAL, "mood": "silence"}],
        "sfx": [{"t": round(t if k is None else T(k, t), 3), "type": typ, "gain": g} for k, t, typ, g in CUES]}
json.dump(cues, open(os.path.join(HERE, "sfx_cues.json"), "w"))
subprocess.run(["python3", os.path.join(HERE, "..", "synth.py"), os.path.join(HERE, "sfx_cues.json"), os.path.join(HERE, "sfx.wav")],
               check=True, env={**os.environ, "STEMS": "1"})
sfx = load(os.path.join(HERE, "sfx_sfx.wav"))[:N]
sfx = np.pad(sfx, (0, N - len(sfx)))

def load_filt(x, af):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", af, "-f", "f32le", "-"], input=x.astype(np.float32).tobytes(), capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)[:N].copy()


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


dip(T("sting", 0), T("know", 0), 0.55)      # the sting and the crowd: the bed pulls back under the screams
dip(T("choice", 0), T("vote", 0), 0.4)      # the hard choice and the peak
dip(T("mock", 0) + 4.8, T("basket", 0), 0.5)   # "พ่อแกก็พูดอย่างนี้" and the photo
mus = mus * gain
end = int(T("vote", -0.12) * SR)
mus[end:] = 0  # hard cut to black and silence

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30)
sfx = level(sfx, -27)
sfx = load_filt(sfx, "lowpass=f=4500,lowpass=f=4500,highpass=f=40")
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mix = vo + mus * duck + sfx
cut, card = int(T("vote", -0.12) * SR), int(T("endb", 0.1) * SR)
mix[cut - 240:cut] *= np.linspace(1, 0, 240)
mix[cut:card] = 0  # a beat of black and silence after the cliffhanger, then only the end card's own sounds
# one static gain to -14 LUFS integrated (no dynamic loudnorm, so the stems are exactly what is in the mix); soft knee above -3 dBFS
def wr(path, x):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", "-c:a", "pcm_s16le", path], input=x.astype(np.float32).tobytes(), check=True)
def integrated(path):
    import re
    out = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", out)[-1])
mstem = mus * duck
mstem[cut:card] = 0
tmp = os.path.join(HERE, "mix_raw.wav")
wr(tmp, mix); I = integrated(tmp); wr(tmp, mix * 10 ** ((-14.0 - I) / 20)); I2 = integrated(tmp); os.remove(tmp)
g = 10 ** ((-14.0 - I) / 20) * 10 ** ((-14.0 - I2) / 20); mix, vos, mstem = mix * g, vo * g, mstem * g
dz = (np.random.default_rng(7).standard_normal(N) * 1e-5).astype(np.float32); vos = vos + dz; mix = mix + dz
ax = np.abs(mix); mix = np.where(ax > 0.7, np.sign(mix) * (0.7 + 0.19 * np.tanh((ax - 0.7) / 0.19)), mix).astype(np.float32)
wr(os.path.join(HERE, "mix.wav"), mix); wr(os.path.join(HERE, "vo_stem.wav"), vos); wr(os.path.join(HERE, "music_stem.wav"), mstem)
print("mix written", TOTAL, "gain", round(20 * np.log10(g), 2))

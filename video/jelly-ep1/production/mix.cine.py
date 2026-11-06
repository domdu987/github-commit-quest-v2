"""หนวดใส EP.1 · CINEMA BIBLE mix (from the first-cut mix): the sound plan in production/soundplan.json —
real ambience (low-passed so it carries no hiss), a 40–60 Hz drone from the first uneasy cut, full silence before the two real
commands and before the sting, short dips in the rhyme, one sting, heartbeats from 90 to 130 bpm. Earlier text of the first cut:
: build the episode soundtrack from schedule.json: per-line levelled voice, synthesized SFX (the wash pulling
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
SC = json.load(open(os.path.join(HERE, "ghost.json")))   # lane B 7970a9d4 timing, lines split per place (each line once)
PROD = "/home/user/github-commit-quest-v2/video/jelly-ep1/production"
PLAN = json.load(open(os.path.join(PROD, "soundplan.json")))
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
# p03 "โอ๊ย! ขาผม!" is a real kid's pain scream (ElevenLabs SFX v2 take1, production/scream/) instead of a TTS take ----
LINE_GAIN = {"p03": 1.5}
vo = np.zeros(N, np.float32)
for s in SC["shots"]:
    for v in s["vo"]:
        f = os.path.join(HERE, "scream_take1.mp3") if v["id"] == "p03" else os.path.join(HERE, "..", "ep1", "lb2", "video", "jelly", "ep1", "vo", f"{v['id']}.wav")
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
    ("hook", 0.4, "drip", 0.2),
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
    ("sting", 0.0, "sting", 0.42), ("sting", 0.05, "zap", 0.2), ("sting", 0.1, "splash", 0.32), ("sting", 0.2, "bubbles", 0.2),
    # ต้น splashes in shouting
    *[("stingB", 0.1 + i * 0.32, "splash", 0.16) for i in range(int(D["stingB"] / 0.32))],
    # the crowd: bottles cracked open
    ("crowd", 0.2, "click", 0.2), ("crowd", vo_t("crowd", 1) - 0.1, "click", 0.18), ("crowd", vo_t("crowd", 2) - 0.1, "swell", 0.16),
    # the cross-section: water drops, the rubbing, the stingers fire, the venom spreads
    *[("know", 0.15 + i * 0.25, "drip", 0.14) for i in range(7)], ("know", 0.4, "rustle", 0.16),
    *[("know", F("know", 0, 1) + 0.25 + i * 0.12, "snap", 0.12) for i in range(8)], ("know", F("know", 0, 2), "swell", 0.24),
    # the bottle over the leg: the heart
    
    # he sets it down; the board's rule 1 lights and the tick lands
    ("choiceB", 0.85, "thud", 0.22), ("choiceB", F("choiceB", 0, 1), "marker", 0.22), ("choiceB", F("choiceB", 0, 1) + 0.5, "ding", 0.3),
    # ภูมิ sobs; quiet
    ("choiceC", 0.1, "swell", 0.14),
    # he turns: the heartbeat comes back; the peak: the swarm under the empty ring; "น้ำหวาน…?"
    ("goneB", 0.05, "riser", 0.26), ("goneB", 0.2, "bubbles", 0.18),
    
    # the choice: ticks, the heartbeat, the wave pull → black
    *tick3("vote", 0.3, 0.3), ("vote", D["vote"] - 1.3, "whoosh", 0.36), ("vote", D["vote"] - 1.2, "splash", 0.4),
    # the end board drops in on its ropes, the buttons pop
    ("endb", 0.1, "whoosh", 0.3), ("endb", 0.6, "thud", 0.2), ("endb", F("endb", 0, 1), "pop", 0.26), ("endb", F("endb", 0, 2), "pop", 0.26),
]

# no hiss: the noise-based wind bed reads as static under the voice (user: "ลบเสียงซ่าออก")
# the heart (bible §3): 90 → 130 bpm with the danger, from the sting to the black after the choice; none inside the silences
def bpm_at(t):
    pts = PLAN["bpm"]
    if t <= pts[0][0]: return pts[0][1]
    for (a, x), (b, y) in zip(pts, pts[1:]):
        if t < b: return x + (y - x) * (t - a) / (b - a)
    return pts[-1][1]
_t, BLACK = PLAN["bpm"][0][0] + 0.7, PLAN["black"][0]
while _t < BLACK - 0.3:
    if not any(a - 0.05 <= _t <= b for a, b in PLAN["silences"]):
        CUES.append((None, _t, "heartbeat", 0.36 + 0.1 * (bpm_at(_t) - 90) / 40))
    _t += 60.0 / bpm_at(_t)
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
dip(T("mock", vo_t("mock", 1)), T("basket", 0) + 3.6, 0.5)   # "พ่อแกก็พูดอย่างนี้" and the photo
mus = mus * gain
end = int(T("vote", -0.12) * SR)
mus[end:] = 0  # hard cut to black and silence

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30)
sfx = level(sfx, -27)
sfx = load_filt(sfx, "lowpass=f=4500,lowpass=f=4500,highpass=f=40")
# ---- real ambience (production/ambience, ElevenLabs SFX, low-passed 2.4 kHz: structure, no hiss) ----
AMB = os.path.join(PROD, "ambience")
def amb_file(name):
    return load_filt(load(os.path.join(AMB, name + ".mp3")), "lowpass=f=2400,lowpass=f=2400,lowpass=f=2400,highpass=f=60")
def loop(x, a, b, xf=0.6):
    out = np.zeros(N, np.float32); n, step, i = len(x), len(x) - int(xf * SR), int(a * SR)
    ramp = np.linspace(0, 1, int(xf * SR), dtype=np.float32)
    while i < int(b * SR):
        seg = x.copy(); seg[: len(ramp)] *= ramp; seg[-len(ramp):] *= ramp[::-1]
        j = min(N, i + n); out[i:j] += seg[: j - i]; i += step
    e = int(b * SR); out[e:] = 0; fade = int(0.3 * SR); out[max(0, e - fade):e] *= np.linspace(1, 0, min(fade, e))
    return out
def load_filt(x, af):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", af, "-f", "f32le", "-"], input=x.astype(np.float32).tobytes(), capture_output=True, check=True).stdout
    y = np.frombuffer(raw, np.float32).copy(); return y
waves, gulls, rooster, under = amb_file("waves"), amb_file("gulls"), amb_file("rooster"), amb_file("under")
BEACH_SPANS = [(0.0, T("card", 0)), (T("map", 0), T("sting", 0)), (T("stingB", 0), T("goneB", 0)), (T("endb", 0), TOTAL)]
UNDER_SPANS = [(T("rock", -1.5), T("stingB", 0)), (T("goneB", 0), T("vote", -0.12))]
amb = np.zeros(N, np.float32)
for a, b in BEACH_SPANS: amb += level(loop(waves, a, b), -36) if b - a > 1 else 0
for t in (T("beach", 0.4), T("beach", 6.5), T("crowd", 1.0), T("endb", 1.0)): place(amb, level(gulls, -40), t)
place(amb, level(rooster, -38), T("card", 0.3))
und = np.zeros(N, np.float32)
for a, b in UNDER_SPANS: und += level(loop(under, a, b, 0.4), -34)
amb += und
# ---- the drone: 40–60 Hz (a 47 Hz sine + a 51 Hz beat + a quiet 94 Hz so a phone hints at it), rising from the first uneasy cut to the
# danger, held through it, cut dead 0.6 s before the sting, gone at the black ----
tt = np.arange(N) / SR
dr = (np.sin(2 * np.pi * 47 * tt) + 0.6 * np.sin(2 * np.pi * 51 * tt) + 0.18 * np.sin(2 * np.pi * 94 * tt)).astype(np.float32)
ds, th = PLAN["drone_start"], PLAN["sting"]
denv = np.clip((tt - ds) / (th - ds), 0, 1) ** 1.6 * 0.7 + np.where(tt >= th, 0.3, 0)
denv[(tt >= PLAN["black"][0])] = 0
dr = dr * denv.astype(np.float32)
dr = dr / (np.sqrt(np.mean(dr[tt > th] ** 2)) + 1e-9) * 10 ** (-38 / 20)
# ---- the plan's silences (everything but the voice ≤ −45 dBFS, 80 ms ramps) and dips (−12 dB) ----
gate = np.ones(N, np.float32)
def hole(a, b, lvl, ramp=0.08):
    k = np.clip((tt - (a - ramp)) / ramp, 0, 1) * np.clip(((b + ramp) - tt) / ramp, 0, 1)
    np.minimum(gate, (1 - (1 - lvl) * k).astype(np.float32), out=gate)
for a, b in PLAN["silences"]: hole(a, b, 0.002)
for a, b in PLAN.get("dips", []): hole(a, b, 0.25)
env = box(np.abs(vo), int(0.05 * SR))
duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
duck = box(duck, int(0.25 * SR))
mus, sfx, amb, dr = mus * gate, sfx * gate, amb * gate, dr * gate
mix = vo + mus * duck + sfx + amb + dr
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

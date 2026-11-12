"""หนวดใส EP.2 · CINEMA BIBLE mix (EP.1's cine mix, EP.2 cues): the sound plan in production/soundplan.json —
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
SC = json.load(open("/home/user/github-commit-quest-v2/video/jelly-ep2/production/lane-b-schedule.json"))   # lane B e8697550 timing (each line once)
PROD = "/home/user/github-commit-quest-v2/video/jelly-ep2/production"
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


# ---- voice: lane B's takes (vo/<id>.wav rebuilt from its cached mp3s with voice.py, durations identical to lane B's), each line levelled ----
VO = "/tmp/claude-0/-home-user-github-commit-quest-v2/2379a335-2a12-59c5-bdf9-6c760b7486b5/scratchpad/jw/lb3/video/jelly/ep2/vo"
LINE_GAIN = {}
vo = np.zeros(N, np.float32)
for s in SC["shots"]:
    for v in s["vo"]:
        place(vo, level(load(os.path.join(VO, f"{v['id']}.wav")), -18 + LINE_GAIN.get(v["id"], 0)), s["start"] + v["t"])
SL = json.load(open(os.path.join(PROD, "shotlist.json")))["cuts"]
C = lambda n: SL[n - 1]["t"]          # shot-list cut n start (global)
CE = lambda n: SL[n - 1]["t"] + SL[n - 1]["dur"]
V = lambda k, i=0: SH[k]["start"] + SH[k]["vo"][i]["t"]
VF = lambda k, i=0, j=0: SH[k]["start"] + SH[k]["vo"][i]["t"] + SH[k]["vo"][i]["frags"][j]
G = None   # cue times below are global
CUES = [
    # 1 the empty ring over the swarm · 2 the fingers dig into the sand
    (G, 0.02, "bubbles", 0.18), (G, 0.1, "plop", 0.12), (G, C(2) + 0.05, "rustle", 0.22), (G, C(2) + 0.15, "squish", 0.16),
    # 5–7 he grabs the shirt · the hands press him down
    (G, C(5) + 0.1, "rustle", 0.18), (G, C(7) + 0.02, "thud", 0.2),
    # 8–9 the leg cut open: the vein pumps, the venom climbs, the stamp
    (G, C(8) + 0.9, "swell", 0.16), (G, C(9) + 0.1, "whoosh", 0.2), (G, C(9) + 1.6, "thud", 0.26),
    # 10 the hand-over; he runs off (before the silence)
    *[(G, VF("leave", 0) + 0.85 + i * 0.28, "steps", 0.12) for i in range(4)],
    # 12 the sting (the swarm in the shallows) · 13 held back in the wash
    (G, C(12), "sting", 0.42), (G, C(12) + 0.08, "bubbles", 0.2), *[(G, C(13) + 0.1 + i * 0.4, "splash", 0.12) for i in range(4)],
    # 14 this morning: the rewind, the ring drops at her feet
    (G, C(14), "rewind", 0.3), (G, C(14) + 0.05, "whoosh", 0.18), (G, C(14) + 1.55, "plop", 0.24), (G, C(14) + 2.0, "tap", 0.08),
    # 15–16 "พ่อ!" he turns; her steps; the hug
    (G, V("back", 0) + 0.25, "whoosh", 0.2), *[(G, C(15) + 1.0 + i * 0.45, "steps", 0.08) for i in range(4)], (G, C(16) + 0.05, "swell", 0.2),
    # 17–18 the bottle; HG7's bell
    (G, C(17) + 0.2, "ching", 0.14),   # the long: no HG7 bell (the HG7 card is hidden in the 16:9 build, review 12 Nov)
    # 19 the board: rule 2 lit
    (G, C(19) + 0.15, "marker", 0.22), (G, C(19) + 0.6, "ding", 0.26),
    # 20 the kitchen shelf, 4–6 %, the pour, the stopwatch
    (G, C(20) + 0.1, "ching", 0.16), (G, VF("vinegar", 0, 1) + 0.1, "pop", 0.26), (G, VF("vinegar", 0, 2), "splash", 0.12),
    *[(G, VF("vinegar", 0, 2) + 0.3 + i * 0.25, "tick", 0.12) for i in range(int((C(21) - VF("vinegar", 0, 2) - 0.4) / 0.25))],
    # 21 the pour over the leg
    *[(G, C(21) + 0.2 + i * 0.35, "drip", 0.1) for i in range(14)],
    # 23 the reveal of ภูมิ arching
    (G, C(23) + 0.9, "riser", 0.2),
    # 25 the empty road (high wide) · 26 the call on speaker
    (G, C(25) + 0.05, "whoosh", 0.16), (G, C(26) + 0.1, "beep", 0.12),
    # 27 vinegar drops on the skin, the stingers fall off
    *[(G, C(27) + 0.1 + i * 0.12, "drip", 0.12) for i in range(6)], *[(G, C(27) + 1.0 + i * 0.07, "snap", 0.08) for i in range(6)],
    # 28 the map: the pins, the route
    (G, C(28) + 0.05, "pop", 0.24), (G, C(28) + 0.3, "pop", 0.24), (G, C(28) + 0.25, "whoosh", 0.2),
    # 29 the choice: ticks, the pull → black · 30 the end board
    *[(G, C(29) + 0.3 + i, "tick", 0.3) for i in range(3)], (G, CE(29) - 1.3, "whoosh", 0.36), (G, CE(29) - 1.2, "thud", 0.3),
    (G, C(30) + 0.1, "whoosh", 0.3), (G, C(30) + 0.6, "thud", 0.2), (G, VF("endb", 0, 1), "pop", 0.26), (G, VF("endb", 0, 2), "pop", 0.26),
]
def T(k, t):
    s = SH[k]
    return s["start"] + (t if t >= 0 else s["dur"] + t)

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
    if not any(a - 0.05 <= _t <= b for a, b in PLAN["silences"] + PLAN.get("heart_off", [])):
        CUES.append((None, _t, "heartbeat", 0.36 + 0.1 * (bpm_at(_t) - 90) / 40))
    _t += 60.0 / bpm_at(_t)
CUES = [c for c in CUES if c[2] not in ("wind", "lap") and c[3] > 0]  # no noise beds (user: "เสียงซ่าๆเอาออก")
cues = {"duration": TOTAL, "sections": [{"start": 0, "end": TOTAL, "mood": "silence"}],
        "sfx": [{"t": round(t, 3), "type": typ, "gain": g} for k, t, typ, g in CUES]}
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


dip(C(12), C(14), 0.55)      # the swarm and the shout: the bed pulls back under the screams
dip(C(5), C(8), 0.55)        # "พ่ออย่าทิ้งผม" / the choice
dip(C(22), C(24), 0.6)       # the shame
dip(C(24), C(29), 0.4)       # can't breathe, the wait
mus = mus * gain
end = int((CE(29) - 0.12) * SR)
mus[end:] = 0  # hard cut to black and silence

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30.8)   # EP.2: the knee lifts the static gain, so the bed sits 0.8 dB lower than EP.1
sfx = level(sfx, -27)
sfx = load_filt(sfx, "lowpass=f=3000,lowpass=f=3000,highpass=f=40")
# ---- real ambience (production/ambience, ElevenLabs SFX, low-passed 2.4 kHz: structure, no hiss) ----
AMB = "/home/user/github-commit-quest-v2/video/jelly-ep1/production/ambience"   # the same four recordings as EP.1
def amb_file(name):
    return load_filt(load(os.path.join(AMB, name + ".mp3")), "lowpass=f=2000,lowpass=f=2000,lowpass=f=2000,highpass=f=60")
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
BEACH_SPANS = [(C(2), C(8)), (C(10), C(12)), (C(13), C(20)), (C(21), C(27)), (C(29), CE(29) - 0.12), (C(30), TOTAL)]
UNDER_SPANS = [(0.0, C(2)), (PLAN["lead_sounds"][0]["t"], C(13))]
amb = np.zeros(N, np.float32)
for a, b in BEACH_SPANS: amb += level(loop(waves, a, b), -36) if b - a > 1 else 0
for t in (C(4) + 1.0, C(15) + 0.5, C(21) + 1.0, C(25) + 0.1, C(30) + 1.0): place(amb, level(gulls, -40), t)
und = np.zeros(N, np.float32)
for a, b in UNDER_SPANS: und += level(loop(under, a, b, 0.4), -34)
amb += und
# ---- the drone: 40–60 Hz (a 47 Hz sine + a 51 Hz beat + a quiet 94 Hz so a phone hints at it), rising from the first uneasy cut to the
# danger, held through it, cut dead 0.6 s before the sting, gone at the black ----
tt = np.arange(N) / SR
dr = (np.sin(2 * np.pi * 47 * tt) + 0.6 * np.sin(2 * np.pi * 51 * tt) + 0.18 * np.sin(2 * np.pi * 94 * tt)).astype(np.float32)
ds, th = PLAN["drone_start"], PLAN["sting"]
denv = np.clip((tt - ds) / (th - ds), 0, 1) ** 1.6 * 0.7 + np.where(tt >= th, 0.3, 0)
lo0, lo1 = PLAN.get("drone_low", [0, 0]); denv[(tt >= lo0) & (tt < lo1)] *= 0.25   # the relief: almost gone
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
cut, card = int((CE(29) - 0.12) * SR), int((C(30) + 0.1) * SR)
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
wr(tmp, mix); I = integrated(tmp); wr(tmp, mix * 10 ** ((-14.0 - I) / 20)); I2 = integrated(tmp)
g = 10 ** ((-14.0 - I) / 20) * 10 ** ((-14.0 - I2) / 20); mix, vos, mstem = mix * g, vo * g, mstem * g
dz = (np.random.default_rng(7).standard_normal(N) * 1e-5).astype(np.float32); vos = vos + dz; mix = mix + dz
# soft knee from −4.4 dBFS to a −2.0 dBFS ceiling (EP.2's narrator takes peak higher than EP.1's), then the static gain is trimmed
# so the kneed mix sits at −14 LUFS (two passes)
knee = lambda y: np.where(np.abs(y) > 0.6, np.sign(y) * (0.6 + 0.19 * np.tanh((np.abs(y) - 0.6) / 0.19)), y).astype(np.float32)
pre = mix.copy()
for _ in range(2):
    wr(tmp, knee(pre)); g2 = 10 ** ((-14.0 - integrated(tmp)) / 20); pre = pre * g2; vos = vos * g2; mstem = mstem * g2
os.remove(tmp); mix = knee(pre)
wr(os.path.join(HERE, "mix.wav"), mix); wr(os.path.join(HERE, "vo_stem.wav"), vos); wr(os.path.join(HERE, "music_stem.wav"), mstem)
print("mix written", TOTAL, "gain", round(20 * np.log10(g), 2))

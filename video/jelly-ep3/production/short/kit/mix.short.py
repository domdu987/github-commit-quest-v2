"""หนวดใส EP.3 Short 9:16 (lane B e24aeda, 104.75 s; plan in production/short) · CINEMA BIBLE mix (EP.2's cine mix, EP.3 cues): no choice and no black; the end board closes it: the sound plan in production/soundplan.json —
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
SC = json.load(open("/home/user/github-commit-quest-v2/video/jelly-ep3/production/short/lane-b-schedule.e24aeda.json"))   # lane B e24aeda timing (each line once)
PROD = "/home/user/github-commit-quest-v2/video/jelly-ep3/production/short"
OUTD = os.path.join(HERE, "short_mix"); os.makedirs(OUTD, exist_ok=True)
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
VO = "/tmp/claude-0/-home-user-github-commit-quest-v2/2379a335-2a12-59c5-bdf9-6c760b7486b5/scratchpad/jw/lb3/video/jelly/ep3/vo"
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
    # 1–2 the towel comes at the calf · the wet tentacle glints
    (G, 0.05, "rustle", 0.2), (G, C(2) + 0.1, "ching", 0.1), (G, C(2) + 0.5, "swell", 0.14),
    # 3 the command (after the silence) · 4–5 the towel inches closer · 6 ต้น catches her wrist
    (G, C(3) + 0.12, "thud", 0.2), (G, C(4) + 0.1, "rustle", 0.18), (G, C(5) + 0.1, "swell", 0.16), (G, C(6) + 1.0, "thud", 0.24),
    # 7–9 the skin: rubbing, the stingers fire, the venom, the stamp
    *[(G, C(7) + 0.25 + i * 0.22, "rustle", 0.1) for i in range(10)], *[(G, C(8) + 0.15 + i * 0.14, "snap", 0.1) for i in range(8)],
    (G, C(9) + 0.2, "swell", 0.18), (G, C(9) + 1.05, "thud", 0.3),
    # 10–11 ยาย runs in · the pour · the tweezers
    *[(G, C(10) + 0.1 + i * 0.3, "steps", 0.12) for i in range(7)], (G, C(11) + 0.2, "pop", 0.22), *[(G, C(11) + 0.4 + i * 0.3, "drip", 0.1) for i in range(6)], (G, C(11) + 1.9, "ching", 0.12),
    # 12 the rule board: rule 3 lit · 13 the ambulance
    (G, C(12) + 0.15, "marker", 0.22), (G, C(12) + 0.6, "ding", 0.26), (G, C(13) + 0.05, "whoosh", 0.2), (G, C(13) + 0.9, "thud", 0.12),
    # 14–15 the ER corridor: a door, a trolley far off
    (G, C(14) + 0.6, "thud", 0.08), (G, C(15) + 2.0, "rustle", 0.08),
    # 16 the shadow screen: the gong · 17 the sting · 18 plain water · 19 the empty boat
    (G, C(16) + 0.1, "gong", 0.26), (G, C(17), "sting", 0.42), (G, C(17) + 0.08, "bubbles", 0.2), *[(G, C(18) + 0.6 + i * 0.16, "drip", 0.12) for i in range(8)],
    (G, C(19) + 0.2, "plop", 0.1),
    # 20 the twist (no hit: the voice carries it) · 22 the post filled at dawn
    (G, C(22) + 0.2, "ching", 0.14), (G, C(22) + 1.0, "ching", 0.12),
    # 24 ภูมิ wakes: a monitor beep · 26–27 the four steps pop on
    *[(G, C(24) + 0.2 + i * 0.8, "beep", 0.06) for i in range(4)],
    *[(G, VF("rules", 0, j), "pop", 0.24) for j in range(1, 6)], (G, C(26) + 0.1, "whoosh", 0.18),
    # 28 dawn: bottles into the rack · 29 the end board
    *[(G, C(27) + 1.0 + i * 0.9, "ching", 0.12) for i in range(5)], (G, C(28) + 0.1, "whoosh", 0.26), (G, C(28) + 0.5, "thud", 0.18),
    # 30 the night corridor thirty years ago: the tube flickers · 31 the sign drops in, the follow card on "กดติดตาม", the YouTube badge
    *[(G, C(29) + 0.7 + i * 0.09, "click", 0.06) for i in range(4)], (G, C(30) + 0.05, "whoosh", 0.22), (G, C(30) + 0.6, "thud", 0.16),
    (G, VF("endb", 0, 1) - 0.1, "ding", 0.22), (G, VF("endb", 0, 2) - 0.1, "pop", 0.2),
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
_t, BLACK = PLAN["bpm"][0][0] + 0.7, PLAN["heart_off"][0][0]
while _t < BLACK - 0.3:
    if not any(a - 0.05 <= _t <= b for a, b in PLAN["silences"] + PLAN.get("heart_off", [])):
        CUES.append((None, _t, "heartbeat", 0.36 + 0.1 * (bpm_at(_t) - 90) / 40))
    _t += 60.0 / bpm_at(_t)
CUES = [c for c in CUES if c[2] not in ("wind", "lap") and c[3] > 0]  # no noise beds (user: "เสียงซ่าๆเอาออก")
cues = {"duration": TOTAL, "sections": [{"start": 0, "end": TOTAL, "mood": "silence"}],
        "sfx": [{"t": round(t, 3), "type": typ, "gain": g} for k, t, typ, g in CUES]}
json.dump(cues, open(os.path.join(OUTD, "sfx_cues.json"), "w"))
subprocess.run(["python3", os.path.join(HERE, "..", "synth.py"), os.path.join(OUTD, "sfx_cues.json"), os.path.join(OUTD, "sfx.wav")],
               check=True, env={**os.environ, "STEMS": "1"})
sfx = load(os.path.join(OUTD, "sfx_sfx.wav"))[:N]
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


dip(C(3), C(10), 0.5)        # the towel, the wrist, the skin
dip(C(14), C(20), 0.6)      # the corridor and the shadow screen: the drone carries it
dip(C(20), C(24), 0.6)      # the twist, the why, the guilt
dip(C(29), C(30), 0.6)      # the night ยาย lied to her son
fade = np.clip((TOTAL - 0.4 - t) / 1.6, 0, 1).astype(np.float32)   # the end board: the bed fades out
mus = mus * gain * fade

# ---- levels + ducking (music sits ~16-20 dB under the voice while it speaks) ----
mus = level(mus, -30.8)
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
BEACH_SPANS = [(0.0, C(14)), (C(22), C(23)), (C(27), C(29)), (C(30), TOTAL)]
UNDER_SPANS = [(PLAN["lead_sounds"][0]["t"], C(18))]
amb = np.zeros(N, np.float32)
for a, b in BEACH_SPANS: amb += level(loop(waves, a, b), -36) if b - a > 1 else 0
for t in (C(10) + 0.5, C(22) + 0.3, C(27) + 1.5): place(amb, level(gulls, -40), t)
und = np.zeros(N, np.float32)
for a, b in UNDER_SPANS: und += level(loop(under, a, b, 0.4), -34)
amb += und
# ---- the drone: 40–60 Hz (a 47 Hz sine + a 51 Hz beat + a quiet 94 Hz so a phone hints at it), rising from the first uneasy cut to the
# danger, held through it, cut dead 0.6 s before the sting, gone at the black ----
tt = np.arange(N) / SR
dr = (np.sin(2 * np.pi * 47 * tt) + 0.6 * np.sin(2 * np.pi * 51 * tt) + 0.18 * np.sin(2 * np.pi * 94 * tt)).astype(np.float32)
ds, th = PLAN["drone_start"], PLAN["sting"]
denv = np.clip((tt - ds) / (th - ds), 0, 1) ** 1.6 * 0.7 + np.where(tt >= th, 0.3, 0)
denv *= np.clip((PLAN["drone_end"] - tt) / 1.5, 0, 1)   # ภูมิ wakes: the drone fades out over 1.5 s
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
# one static gain to -14 LUFS integrated (no dynamic loudnorm, so the stems are exactly what is in the mix); soft knee above -3 dBFS
def wr(path, x):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", "-c:a", "pcm_s16le", path], input=x.astype(np.float32).tobytes(), check=True)
def integrated(path):
    import re
    out = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", out)[-1])
mstem = mus * duck
tmp = os.path.join(OUTD, "mix_raw.wav")
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
wr(os.path.join(OUTD, "mix.wav"), mix); wr(os.path.join(OUTD, "vo_stem.wav"), vos); wr(os.path.join(OUTD, "music_stem.wav"), mstem)
print("mix written", TOTAL, "gain", round(20 * np.log10(g), 2))

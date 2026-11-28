"""common.py -- paths, timing, the narration envelope and small maths shared by the shot scripts (no bpy)."""
import os, sys, math, json, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
AUDIO = os.path.join(PROJ, "audio", "narr_ohm")           # v3: the Ohm take (narration, captions, mix)
AUDIO_V1 = os.path.join(PROJ, "audio", "narr_v1")
FONTS = os.path.join(PROJ, "fonts")
KANIT = os.path.join(FONTS, "Kanit_900Black.ttf")
WORKS = os.path.join(FONTS, "WorkSans-Black.ttf")
import importlib.util as _iu
_sp = _iu.spec_from_file_location("dz_timing", os.path.join(PROJ, "v4", "animatic", "timing.py"))
TM = _iu.module_from_spec(_sp); _sp.loader.exec_module(TM)                                      # the approved cut (shot id -> t0, t1, caption)

FPS = 24
NARR0 = TM.NARR0                                        # film time = narration time + 0.30
DUR = TM.DUR
NF = TM.NF                                              # 1280
TITLE_T = TM.TITLE
SHOT_IDS = list(TM.NEW.keys())                          # S01 .. S24
# sound-effect / picture cues (film seconds).  Same values as narr_v1/cue_times_v2.json; mix_ohm_v2.py places every
# effect at the same times (cutter 15.05, phone 17.65, lunge 43.45, scream 43.80, hit 50.72), so they did not move with the voice.
CUES = {"static2": 3.243, "rain": 5.489, "sirens": 6.139, "alarm": 11.103, "cutter": 15.052, "phone": 17.648, "mus_in": 17.248,
        "hood": 30.347, "pry": 34.508, "hb1": 38.681, "hb2": 40.681, "drop0": 40.081, "lunge": 43.445, "mus2": 45.103,
        "hit": 50.72, "scream": 43.795, "dur": 53.32}
CAPS = json.load(open(os.path.join(AUDIO, "captions_timing.json"), encoding="utf-8"))     # [{id, text, t0, t1}] narration time


def word(text, end=False):
    """film time at which a caption phrase starts (or ends) in the Ohm narration (caption time + NARR0)."""
    for c in CAPS:
        if c["text"] == text:
            return (c["t1"] if end else c["t0"]) + TM.NARR0
    raise KeyError(text)


def fr(t):
    return int(round(t * FPS))


def shot_range(sid):
    """global frame range [g0, g1) of a shot; consecutive shots tile 0..NF exactly."""
    t0, t1, _ = TM.NEW[sid]
    return fr(t0), (NF if sid == SHOT_IDS[-1] else fr(t1))


def shot_of(g):
    for sid in SHOT_IDS:
        a, b = shot_range(sid)
        if a <= g < b:
            return sid
    return SHOT_IDS[-1]


# ------------------------------------------------------------------------------------------------ easing
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_out(x, p=2.2):
    return 1 - (1 - clamp(x)) ** p


def ease_in(x, p=2.2):
    return clamp(x) ** p


def ramp(t, a, b):
    """0 before a, 1 after b, linear between."""
    return clamp((t - a) / max(b - a, 1e-6))


def lerp(a, b, u):
    if isinstance(a, (tuple, list)):
        return tuple(x + (y - x) * u for x, y in zip(a, b))
    return a + (b - a) * u


def on_twos(t):
    """pose clock: drawings change every second frame (12 per second), the camera moves on ones."""
    return math.floor(t * FPS / 2.0) * 2.0 / FPS


# ------------------------------------------------------------------------------------------------ voice envelope
_ENV = None


def envelope():
    """RMS of narr_ohm/narr_final.wav per film frame (0..1, 95th percentile = 1), shifted by NARR0."""
    global _ENV
    if _ENV is None:
        w = wave.open(os.path.join(AUDIO, "narr_final.wav"))
        sr, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
        a = np.frombuffer(w.readframes(n), dtype={1: np.int8, 2: np.int16, 4: np.int32}[sw]).astype(np.float32)
        a = a.reshape(-1, ch).mean(1) / float(2 ** (8 * sw - 1))
        hop = sr / float(FPS)
        env = np.zeros(NF, np.float32)
        for g in range(NF):
            tn = g / float(FPS) - NARR0
            i0 = int(round(tn * sr)); i1 = int(round(i0 + hop))
            if i1 <= 0 or i0 >= len(a):
                continue
            seg = a[max(i0, 0):i1]
            env[g] = float(np.sqrt((seg * seg).mean())) if len(seg) else 0.0
        p = np.percentile(env[env > 0], 95) if (env > 0).any() else 1.0
        _ENV = np.clip(env / max(p, 1e-6), 0, 1)
    return _ENV


def mouth(g, floor=0.10):
    """lip-sync mouth level for film frame g, quantised to 5 drawings (0, .25, .5, .75, 1)."""
    e = envelope()
    v = float(e[min(max(g, 0), NF - 1)])
    if v < floor:
        return 0.0
    v = (v - floor) / (1 - floor)
    # a little syllable chatter so held vowels still move
    return round(clamp(0.25 + 0.75 * v ** 0.7) * 4) / 4.0


def blink(name, t):
    """0 open, 1 half, 2 closed; one blink every 2.3-3.9 s per actor, deterministic."""
    seed = sum(ord(c) for c in name) * 0.37
    per = 2.3 + (seed % 1.6)
    ph = (t + seed) % per
    k = int(ph * FPS)
    return {0: 1, 1: 2, 2: 2, 3: 1}.get(k, 0)


def shake(t, amp, hz, seed=0.0):
    """handheld: (yaw, pitch, roll) degrees, sum of sines (same family as the animatic)."""
    w = 2 * math.pi * hz
    t = t + seed
    yaw = amp * (0.6 * math.sin(w * t + 1.1) + 0.4 * math.sin(2.3 * w * t + 0.3))
    pit = amp * (0.6 * math.sin(1.3 * w * t + 2.0) + 0.4 * math.sin(2.9 * w * t + 0.7))
    rol = 0.5 * amp * math.sin(0.7 * w * t + 0.4)
    return yaw, pit, rol


def hash01(*k):
    x = math.sin(sum((i + 1) * 12.9898 * float(v) for i, v in enumerate(k))) * 43758.5453
    return x - math.floor(x)

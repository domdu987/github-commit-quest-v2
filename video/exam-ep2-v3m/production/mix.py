"""ห้องสอบ EP.2 soundtrack: levelled voices, ElevenLabs effects (video/exam/sfxlib) + a few synth accents, the bed with dips. -14 LUFS, no noise beds."""
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
LINE_GAIN = {"k01": 2, "k02": 1}
vo = np.zeros(N, np.float32)
for s in SC["shots"]:
    for v in s["vo"]:
        x = load(os.path.join(HERE, "vo", f"{v['id']}.wav"))
        place(vo, level(x, -18 + LINE_GAIN.get(v["id"], 0)), s["start"] + v["t"])
D = {k: SH[k]["dur"] for k in SH}
F = frag
def beats(k, t0, dur, period, g=0.3):
    return [(k, t0 + i * period, "heartbeat", g) for i in range(int((dur - 0.1) / period) + 1)]
def ticks(k, a, b, g=0.2, step=1.0):
    return [(k, a + i * step, "tick", g) for i in range(int((b - a) / step) + 1)]
CUES = [
    ("hook", 0.0, "sting", 0.3), 
    *beats("quiet", 0.2, D["quiet"] - 0.2, 0.7, 0.26),
    ("mute", 0.5, "click", 0.35),
    *beats("pass", 0.0, F("pass", 0, 2), 0.5, 0.32),
    *ticks("knock", 0.05, 1.2, 0.25, 0.25),
    ("key", 1.5, "swell", 0.3),
    ("call", vo_t("call", 1) + 0.5, "ding", 0.18),
    ("thirty", F("thirty", 0, 1) + 0.4, "sting", 0.35),
    ("cab", 0.1, "swell", 0.2),
    ("where", D["where"] - 1.0, "sting", 0.3),
    ("end", 0.6, "ding", 0.22),
]
exec(open(os.path.join(HERE, "..", "samples_inc.py")).read())
exec(open(os.path.join(HERE, "..", "nohiss_inc.py")).read())
SAMPLES = [
    ("hook", 0.0, "phonebuzz", 0.7, 1.6), ("hook", 1.65, "groan", 0.3),
    ("dont", 0.0, "phonebuzz", 0.6, 1.0),
    ("quiet", 0.3, "breath", 0.45), ("pass", 0.0, "groan", 0.3, 1.6), ("pass", F("pass", 0, 2), "shuffle", 0.7, 2.2),
    ("knock", 1.3 + 0.12, "knock", 1.0), ("cop", 0.0, "knock", 0.6, 1.2),
    ("up", 0.2, "crowdwalk", 0.3, 1.6),
    ("key", 0.05, "knob", 0.9), ("key", 0.7, "keys", 0.9), ("key", 1.4, "dooropen", 0.9),
    ("safe", 0.0, "crowdwalk", 0.5, 2.0), ("call", 0.0, "crowdwalk", 0.4, D["call"]),
    ("cab", 0.0, "cabinet", 0.75),
    ("where", 0.0, "crowdwalk", 0.25, 1.5), ("where", 1.4, "shuffle", 0.4, 1.8),
]

# ---- the classroom cards: the chalkboard (drop + swing on its nail, chalk writing each rule, quick chalk ticks) and the red-pen answer sheet ----
def board(k, t0, ats, texts):
    out = [(k, t0 + 0.3, "boarddrop", 0.8)]
    for a, tx in zip(ats, texts):
        wr = min(0.75, 0.25 + len(tx) * 0.03)
        out += [(k, t0 + a + 0.1, "chalkwrite", 0.75, wr + 0.05), (k, t0 + a + 0.15 + wr, "chalkswipe", 0.6), (k, t0 + a + 0.4 + wr, "chalkswipe", 0.55)]
    return out + [(k, t0 + 0.2, "eraser", 0.25)]
def sheet(k, st=0.35):
    return [(k, 0.0, "paperflutter", 0.4), (k, st, "redpen", 0.45), (k, st + 0.8, "redpen", 0.35, 0.35)]
SAMPLES += sheet("dont") + board("mute", 0.05, [0.35, F("mute", 0, 1) - 0.1], ["ปิดเสียงมือถือ", "ปิดทุกอย่างที่ดังได้"]) + board("rule", 0.05, [F("rule", 0, 1) - 0.2, vo_t("rule", 1) + 0.2], ["ห้ามเปิดให้ใคร", "รอเจ้าหน้าที่ไขเอง"]) + board("call", vo_t("call", 0), [F("call", 0, 1) - vo_t("call", 0)], ["เช็กชื่อให้ครบ"])
cues = {"duration": TOTAL, "sections": [{"start": 0, "end": TOTAL, "mood": "silence"}],
        "sfx": [{"t": round(t if k is None else T(k, t), 3), "type": typ, "gain": g} for k, t, typ, g in CUES]}
json.dump(cues, open(os.path.join(HERE, "sfx_cues.json"), "w"))
subprocess.run(["python3", os.path.join(HERE, "..", "synth.py"), os.path.join(HERE, "sfx_cues.json"), os.path.join(HERE, "sfx.wav")],
               check=True, env={**os.environ, "STEMS": "1"})
sfx = load(os.path.join(HERE, "sfx_sfx.wav"))[:N]
sfx = np.pad(sfx, (0, N - len(sfx)))
sfx = lp45(sfx)   # the synth stem too: a saw-chord sting has dense harmonics up high that read as hiss
place_samples(sfx, SAMPLES)

# ---- music with horror dips ----
_th = load(os.path.join(HERE, "..", "music", "exam-theme.mp3"))
# A5: the theme from 33.4 s up to 81 s (before its own fade-out), then its continuous body (41–81 s) looped with 1 s crossfades
mus, _body, _xf = _th[int(33.4 * SR):int(81 * SR)].copy(), _th[int(41 * SR):int(81 * SR)].copy(), int(1.0 * SR)
while len(mus) < N:
    _r = np.linspace(0, 1, _xf, dtype=np.float32)
    mus = np.concatenate([mus[:-_xf], mus[-_xf:] * (1 - _r) + _body[:_xf] * _r, _body[_xf:]])   # the theme: its abrupt cut (~85 s) lands on the cliffhanger
mus = np.pad(mus, (0, max(0, N - len(mus))))[:N]
t = np.arange(N) / SR
gain = np.ones(N, np.float32)


def dip(t0, t1, lvl, ramp=0.25):
    a = np.clip((t - (t0 - ramp)) / ramp, 0, 1) * np.clip(((t1 + ramp) - t) / ramp, 0, 1)
    np.minimum(gain, 1 - (1 - lvl) * a, out=gain)


dip(T("hook", 0), T("knock", -0.01), 0.7)      # hiding: near silence
# (v3m: no dip on the key — the bed carries the pause)
gain[int(T("thirty", 0) * SR):int(T("where", -0.01) * SR)] *= 1.25   # the twist: the bed rises to its peak
mus = lp45(mus * gain, 6000.0, 48)   # A5: the theme keeps its air (6 kHz); the effects bus stays at 4.5 kHz
a, b = int(T("end", 0) * SR), int(T("end", -0.01) * SR)
c = max(a, b - int(0.8 * SR)); mus[c:b] *= np.linspace(1, 0, b - c)   # A5: the theme stays over the end card, out in the last 0.8 s
mus[b:] = 0

# ---- levels, duck, -14 LUFS, stems (A5) ----
exec(open(os.path.join(HERE, "..", "musicmix_inc.py")).read())
# a planned hush right after "ต้องไม่มีเสียงเลย": 0.55 s of true silence before the next line (the room obeys the rule)
_h0, _h1 = vo_end("quiet") + 0.05 + SH["quiet"]["start"], SH["mute"]["start"] + vo_t("mute") - 0.03
_hush = (1 - np.clip((t - (_h0 - 0.03)) / 0.03, 0, 1) * np.clip(((_h1 + 0.03) - t) / 0.03, 0, 1)).astype(np.float32)
music_mix(vo, ride(mus), sfx, hush=_hush, mus_db=float(os.environ.get("MUS_DB", -22)))
print("mix written", TOTAL)

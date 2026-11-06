"""รูพญานาค ฉบับเต็ม (cold open: EP.2 open+hook with c01 = n01 trimmed, then 0.4 s black) (YouTube 16:9) soundtrack, from long/schedule.json (combine.py).
Voice: every line levelled on its own (-18), the headman's megaphone band-passed, as in the episode mixes; the bridge lines (b01–b07).
SFX: each episode's own cue list (its mix.py, evaluated against that episode's shots in the full schedule; cues of the cut shots
— EP.1/2 choice+end, EP.2/3 hook — fall away) plus cues for the bridges. Music: the channel song suno1 with the ทะเลลด recipe
(unfiltered, -30 dB RMS, duck 0.65), restarted from 0 at each chapter, dipped on the scary beats, faded under the final card."""
import json, os, re, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
WS = os.environ.get("WS", "/tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/mw2")
EPDIR = os.environ.get("EPDIR", "/home/user/github-commit-quest-v2/video/rupnak")
SR = 48000
SC = json.load(open(os.path.join(HERE, "schedule.json"))); SH = {s["key"]: s for s in SC["shots"]}; TOTAL = SC["total"]; N = int(TOTAL * SR)

def load(path):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"]); return np.frombuffer(raw, dtype=np.float32).copy()
def place(buf, x, t, g=1.0):
    i = int(t * SR); j = min(len(buf), i + len(x))
    if 0 <= i < len(buf): buf[i:j] += x[: j - i] * g
def rms_db(x):
    x = x[np.abs(x) > 1e-4]; return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
def level(x, target): return x * 10 ** ((target - rms_db(x)) / 20)
def box(x, n):
    c = np.concatenate([[0.0], np.cumsum(x, dtype=np.float64)]); i = np.arange(len(x))
    lo, hi = np.clip(i - n // 2, 0, len(x)), np.clip(i - n // 2 + n, 0, len(x)); return ((c[hi] - c[lo]) / n).astype(np.float32)
def ff(x, af):
    out = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", af, "-f", "f32le", "-"], input=x.astype(np.float32).tobytes(), capture_output=True, check=True).stdout
    return np.frombuffer(out, np.float32)[:len(x)]
def T(k, t=0.0):
    s = SH[k]; return s["start"] + (t if t >= 0 else s["dur"] + t)

# ---- voice ----
FX = {}
for n in (1, 2, 3):
    for l in json.load(open(os.path.join(EPDIR, f"ep{n}", "lines.json"))): FX[f"e{n}/{l['id']}"] = l.get("fx")
vo = np.zeros(N, np.float32)
for s in SC["shots"]:
    for v in s["vo"]:
        ep, lid = v["id"].split("/")
        path = os.path.join(HERE, "..", "bridge", "vo", f"{lid}.wav") if ep == "b" else os.path.join(WS, f"rup{ep[1]}", "vo", f"{lid}.wav")
        x = load(path)
        if FX.get(v["id"]) == "megaphone": x = np.tanh(3 * ff(x, "highpass=f=600:poles=2,highpass=f=600:poles=2,lowpass=f=3200:poles=2,lowpass=f=3200:poles=2")) / 2
        place(vo, level(x, -18), s["start"] + v["t"])

# ---- sfx: each episode's own cue list against its shots in the full schedule ----
CUES = []
for n in (1, 2, 3):
    src = open(os.path.join(WS, f"rup{n}", "mix.py")).read()
    a = src.index("def T(k, t):"); b = src.index("LINE_GAIN = {}"); c = src.index("D = {k: SH[k]"); d = src.index("\n", src.index("CUES = [c for c in CUES")) + 1
    code = src[a:b] + src[c:d]
    class EpSH(dict):
        def __missing__(self, k): return {"start": -1000.0, "dur": 1.0, "vo": [{"t": 0, "dur": 1, "frags": [0, 0.3, 0.6]}] * 4}
    sh = EpSH({k[3:]: v for k, v in SH.items() if k.startswith(f"e{n}_")})
    for k in ("open", "hook", "choice", "end", "lotto", "map"):   # keys the episode's cue code may name though they are not all in the film
        pass
    ns = {"SH": sh, "np": np, "TOTAL": TOTAL}
    exec(code.replace("D = {k: SH[k][\"dur\"] for k in SH}", "D = __import__('collections').defaultdict(lambda: 1.0, {k: SH[k]['dur'] for k in SH})"), ns)
    for k, t, typ, g in ns["CUES"]:
        at = t if k is None else (sh[k]["start"] + (t if t >= 0 else sh[k]["dur"] + t))
        if 0 <= at < TOTAL - 0.05: CUES.append((None, at, typ, g))
# the bridges
CUES += [(None, T("b1win", 0.3), "crickets", 0.0), (None, T("b1dust", 0.2), "crackle", 0.12), (None, T("b1dust", 1.2), "creak", 0.24), (None, T("b1dust", 1.6), "quake", 0.4),
         (None, T("b1shake", 0.05), "boom", 0.3), (None, T("b1shake", 0.1), "quake", 0.45), (None, T("b1shake", 0.4), "rattle", 0.22),
         (None, T("b2call", 0.4), "steps", 0.24), (None, T("b2call", 1.4), "steps", 0.22), (None, T("b2call", 2.4), "tap", 0.16), (None, T("b2call", 2.8), "ring", 0.14),
         (None, T("b2dawn", 0.2), "rooster", 0.14), (None, T("b2dawn", 2.0), "crackby", 0.26), (None, T("b2dawn", 2.1), "debris", 0.2),
         (None, T("b2barn", 0.3), "creak", 0.22), (None, T("b2barn", 1.4), "drip", 0.16)]
CUES = [c for c in CUES if c[3] > 0]
json.dump({"duration": TOTAL, "sections": [{"start": 0, "end": TOTAL, "mood": "silence"}], "sfx": [{"t": round(t, 3), "type": typ, "gain": g} for _, t, typ, g in CUES]}, open(os.path.join(HERE, "sfx_cues.json"), "w"))
subprocess.run(["python3", os.path.join(WS, "synth.py"), os.path.join(HERE, "sfx_cues.json"), os.path.join(HERE, "sfx.wav")], check=True, env={**os.environ, "STEMS": "1"})
sfx = load(os.path.join(HERE, "sfx_sfx.wav"))[:N]; sfx = np.pad(sfx, (0, N - len(sfx)))

# ---- music: suno1 from 0 at each chapter, the ทะเลลด recipe ----
song = load(os.path.join(WS, "music", "suno1.mp3"))
mus = np.zeros(N, np.float32); t = np.arange(N) / SR
ch = [0.0, T("b1win", 0), T("b2call", 0), TOTAL]   # restart on the three rule chapters only (the other chapter marks run through)
for a, b in zip(ch, ch[1:]):
    i, j = int(a * SR), int(b * SR); seg = song[: j - i].copy()
    if len(seg) < j - i: seg = np.pad(seg, (0, j - i - len(seg)))
    fi, fo = int(0.6 * SR), int(1.2 * SR); seg[:fi] *= np.linspace(0, 1, fi); seg[-fo:] *= np.linspace(1, 0, fo)
    mus[i:j] = seg
gain = np.ones(N, np.float32)
def dip(t0, t1, lvl, ramp=0.25):
    a = np.clip((t - (t0 - ramp)) / ramp, 0, 1) * np.clip(((t1 + ramp) - t) / ramp, 0, 1); np.minimum(gain, 1 - (1 - lvl) * a, out=gain)
dip(T("e2_hook", 0.0), T("cogap", -0.01), 0.55)                   # cold open: the command, then the black
dip(T("e1_collapse", 0.0), T("e1_collapse", 0.55), 0.4, 0.08)      # breath held on the collapse
dip(T("b1shake", 0.0), T("b1shake", -0.1), 0.55)                    # the floor shakes
dip(T("e2_pump", 0.0), T("e2_pump", 1.0), 0.4, 0.08)               # the far pump in the dark
dip(T("e2_rumble", 0), T("e2_ring", -0.01), 0.55)                  # the ground rumbles again
dip(T("e3_rain", -0.25), T("e3_sink", 0.08), 0.4, 0.1)             # before the barn goes
dip(T("e3_warn", 0.0), T("e3_warn", -0.2), 0.55, 0.3)              # "it's a warning"
mus = mus * gain
f0 = int(T("e3_end", 0.0) * SR); mus[f0:] *= np.linspace(1, 0, N - f0)   # the theme fades out under the final card

from finalmix import finalize
mus = level(mus, -30)
sfx = level(ff(ff(sfx, "lowpass=f=3500:poles=2"), "lowpass=f=3500:poles=2"), -27)
env = box(np.abs(vo), int(0.05 * SR)); duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1); duck = box(duck, int(0.25 * SR))
mus_part = (mus * duck).astype(np.float32)
finalize(HERE, (vo + mus_part + sfx).astype(np.float32), vo.copy(), mus_part, tp=-2.8)   # tp -1.5 keeps the soft limiter out (its tanh knee reads as hiss, M8)
print("cues", len(CUES), "total", TOTAL)

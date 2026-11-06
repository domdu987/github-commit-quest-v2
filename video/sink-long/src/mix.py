"""นาทีก่อนจม ฉบับเต็ม (YouTube 16:9) soundtrack, from long/schedule.json (combine.py).
Voice: every line levelled on its own (-18, ขิม's shouts and the rider's sorry lifted as in the episode mixes) + the bridge lines.
SFX (3.5 kHz low-pass, -27): each episode's own cue list and recorded samples (its mix.py, evaluated against that episode's shots in the full schedule, and
again against its xN_ copies used in the bridges; cues of cut shots fall away). Music: suno1 as one continuous bed from the first
frame (looped with a crossfade if the film outruns it), -30 dB RMS, duck 0.65, the episodes' dips, faded out under the series card."""
import json, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
K = os.path.dirname(HERE)
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
EPV = lambda n: os.path.join(K, "video", f"sink-ep{n}", "production")

# ---- voice ----
GAIN = {1: {"k01": 3}, 2: {"y02": 3}, 3: {"k01": 4, "r01": 2}}
BRV = os.path.join(HERE, "bridges", "vo")
BRGAIN = {"a1": 3, "b2": 4}
vo = np.zeros(N, np.float32)
for s in SC["shots"]:
    for v in s["vo"]:
        k = s["key"]
        if v["id"].startswith("l"):   # long-only re-recorded narrator lines (M6)
            x = load(os.path.join(BRV, f"{v['id']}.wav")); g = 0
        elif k.startswith("e"):
            n = int(k[1]); x = load(os.path.join(EPV(n), "vo", f"{v['id']}.wav")); g = GAIN[n].get(v["id"], 0)
        elif v["id"] == "x02":   # bridge B repeats EP.3's own rule line
            x = load(os.path.join(EPV(3), "vo", "n02.wav")); g = 0
        else:
            x = load(os.path.join(BRV, f"{v['id']}.wav")); g = BRGAIN.get(v["id"], 0)
        place(vo, level(x, -18 + g), s["start"] + v["t"])

# ---- sfx: each episode's cue list and samples, against its e-shots and again against its x-copies ----
CUES, SAMPLES = [], []
smp_ns = None
for n in (1, 2, 3):
    src = open(os.path.join(EPV(n), "mix.py")).read()
    a = src.index("def T(k, t):"); b = src.index("# ---- voice"); c = src.index("D = {k: SH[k]"); d = src.index("\n", src.index('CUES = [c for c in CUES if c[2] not in ("wind"')) + 1
    code = src[a:b] + src[c:d]
    code = code.replace('exec(open(os.path.join(HERE, "..", "samples_inc.py")).read())', "")
    for pre in ("e", "x"):
        class EpSH(dict):
            def __missing__(self, k): return {"start": -1000.0, "dur": 1.0, "vo": [{"t": 0, "dur": 1, "frags": [0, 0.3, 0.6, 0.9]}] * 4}
        pad = lambda v: {**v, "vo": [{**x, "frags": (x.get("frags") or [0]) + [x["dur"]] * 4} for x in v["vo"]] + [{"t": v["dur"] - 0.2, "dur": 0.1, "frags": [0, 0.03, 0.06, 0.09]}] * 4}
        sh = EpSH({k[3:]: pad(v) for k, v in SH.items() if k.startswith(f"{pre}{n}_")})
        if not sh:
            continue
        ns = {"SH": sh, "np": np, "TOTAL": TOTAL, "os": os, "load": load, "SR": SR}
        exec(open(os.path.join(K, "video", "sink", "samples_inc.py")).read().replace('os.path.join(HERE, "..", "..", "sfxlib")', repr(os.path.join(K, "sfxlib"))), ns)
        smp_ns = smp_ns or ns
        exec(code.replace('D = {k: SH[k]["dur"] for k in SH}', "D = __import__('collections').defaultdict(lambda: 1.0, {k: SH[k]['dur'] for k in SH})"), ns)
        for k, t, typ, g in ns["CUES"]:
            at = t if k is None else (sh[k]["start"] + (t if t >= 0 else sh[k]["dur"] + t))
            if 0 <= at < TOTAL - 0.05: CUES.append((None, at, typ, g))
        for k, t0, name, g, *mx in ns.get("SAMPLES", []):
            if k not in sh: continue
            at = sh[k]["start"] + (t0 if t0 >= 0 else sh[k]["dur"] + t0)
            if 0 <= at < TOTAL - 0.05: SAMPLES.append((at, name, g, mx[0] if mx else None, ns))
CUES = [c for c in CUES if c[3] > 0]
# review 6 Nov (M6): the two re-cut beats get their own sounds: the headrest card (two taps into the groove, the pane goes) and the
# shoe beat (the tug under water, then the shoe lands in the canal)
_ns = next(x[4] for x in SAMPLES if x[1] == "prongtap")
def _win(k): s = SH[k]; return s["start"], s["start"] + s["dur"]
_hr, _sh = _win("e2_headrest"), _win("e3_shoe")
_out = lambda at: _hr[0] - 0.01 <= at < _hr[1] or _sh[0] - 0.01 <= at < _sh[1]
CUES = [c for c in CUES if not _out(c[1])]; SAMPLES = [x for x in SAMPLES if not _out(x[0])]
_v = SH["e2_headrest"]["vo"][0]; _at = _hr[0] + _v["t"] + _v["frags"][1] + 0.35
SAMPLES += [(_at - 0.4, "prongtap", 1.0, 0.6, _ns), (_at - 0.15, "prongtap", 1.0, 0.6, _ns), (_at + 0.5, "glasscrack", 0.85, None, _ns)]
_v = SH["e3_shoe"]["vo"][0]; _ss = _v["t"] + _v["frags"][1] - 0.05
SAMPLES += [(_sh[0], "underwater", 0.3, _ss, _ns), (_sh[0] + 0.15, "shoetug", 0.9, None, _ns)]
CUES.append((None, _sh[0] + _ss + 1.6, "splash", 0.5))
json.dump({"duration": TOTAL, "sections": [{"start": 0, "end": TOTAL, "mood": "silence"}], "sfx": [{"t": round(t, 3), "type": typ, "gain": g} for _, t, typ, g in CUES]}, open(os.path.join(HERE, "sfx_cues.json"), "w"))
subprocess.run(["python3", os.path.join(K, "synth.py"), os.path.join(HERE, "sfx_cues.json"), os.path.join(HERE, "sfx.wav")], check=True, env={**os.environ, "STEMS": "1"})
sfx = load(os.path.join(HERE, "sfx_sfx.wav"))[:N]; sfx = np.pad(sfx, (0, N - len(sfx)))
for at, name, g, mx, ns in SAMPLES:
    place(sfx, ns["smp"](name, mx), at, g)

# ---- music: one continuous suno1 bed ----
song = load(os.path.join(K, "music", "suno1.mp3"))
XF = int(2.0 * SR)
while len(song) < N:   # loop with a 2 s crossfade
    a, b = song[:-XF], song[-XF:]; w = np.linspace(1, 0, XF)
    song = np.concatenate([a, b * w + song[:XF] * (1 - w), song[XF:]])
mus = song[:N].copy(); t = np.arange(N) / SR
fi = int(0.6 * SR); mus[:fi] *= np.linspace(0, 1, fi)
gain = np.ones(N, np.float32)
def dip(t0, t1, lvl, ramp=0.25):
    a = np.clip((t - (t0 - ramp)) / ramp, 0, 1) * np.clip(((t1 + ramp) - t) / ramp, 0, 1); np.minimum(gain, 1 - (1 - lvl) * a, out=gain)
dip(T("e3_hook", 0), T("cogap", -0.01), 0.6)                # cold open: the shout over the water
dip(T("e1_plunge", 0), T("e1_inrush", -0.01), 0.35)         # the splash and the water pouring in
dip(T("e1_kim", 0), T("e1_flicker", -0.01), 0.55)           # EP.1's twist
dip(T("e2_open", 0), T("e2_open", -0.01), 0.55)             # EP.2's twist
dip(T("e2_surface", 0), T("e2_surface", -0.01), 0.6)        # her first breath above the water
dip(T("x3_kim", 0), T("x3_kim", -0.01), 0.4)                # bridge B: "หนูจะลงไปหาพี่"
dip(T("e3_grab", 0), T("e3_grab", -0.01), 0.6)              # what would happen under the water
dip(T("e3_kim", 0), T("e3_kim", -0.01), 0.35)               # her shout over the water
dip(T("e3_rw", 0), T("e3_same", -0.01), 0.55)               # the push-in and the twist
mus = mus * gain
f0 = int(T("e3_end", 0.0) * SR); mus[f0:] *= np.linspace(1, 0, N - f0)   # the bed fades out under the series card

from finalmix import finalize
mus = level(mus, -30)   # suno1's faint top end reads as hiss under this film's long pauses (hisscheck)
def brick(x, hz):   # a hard low-pass in the spectrum (with a 600 Hz taper): the water/struggle samples are noise up to 14 kHz
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X *= np.clip((hz + 300 - f) / 600, 0, 1); return np.fft.irfft(X, len(x)).astype(np.float32)
sfx = level(ff(ff(sfx, "lowpass=f=3500:poles=2"), "lowpass=f=3500:poles=2"), -27)   # the ทะเลลด recipe: no hiss from the water/cricket samples
env = box(np.abs(vo), int(0.05 * SR)); duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1); duck = box(duck, int(0.25 * SR))
mus_part = (mus * duck).astype(np.float32)
finalize(HERE, (vo + mus_part + sfx).astype(np.float32), vo.copy(), mus_part, tp=-1.5)   # tp -1.5 keeps the soft limiter out (its tanh knee reads as hiss); the rule is peak <= -1
print("cues", len(CUES), "samples", len(SAMPLES), "total", TOTAL)

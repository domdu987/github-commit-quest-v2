"""หนวดใส คลิปยาว · ฉากเชื่อม A/B mix: lane B's bridge lines (a01 a02 b01 b02, each -18 dB RMS), a01 through a phone band once we cut
to ยาย listening, the ring before it, real beach / dawn-porch ambience (low-passed, no hiss), suno1 at the ทะเลลด level with the same
duck, short SFX on the actions (the basket lifted, her steps out, the knock on the empty rack, the push onto the photo). -14 LUFS."""
import json
import os
import subprocess

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
SC = json.load(open(os.path.join(HERE, "plan", "lane-b-schedule.json")))
SL = json.load(open(os.path.join(HERE, "plan", "shotlist.json")))["cuts"]
SH = {s["key"]: s for s in SC["shots"]}
TOTAL = SC["total"]; N = int(TOTAL * SR)
VO = os.path.join(HERE, "..", "lb3", "video", "jelly", "bridges", "vo")
C = lambda n: SL[n - 1]["t"]
V = lambda k, i=0: SH[k]["start"] + SH[k]["vo"][i]["t"]
VF = lambda k, i=0, j=0: V(k, i) + SH[k]["vo"][i]["frags"][j]


def load(path):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, dtype=np.float32).copy()


def filt(x, af):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", af, "-f", "f32le", "-"],
                         input=x.astype(np.float32).tobytes(), capture_output=True, check=True).stdout
    y = np.frombuffer(raw, np.float32).copy(); return np.pad(y, (0, max(0, len(x) - len(y))))[: len(x)]


def place(buf, x, t, g=1.0):
    i = int(t * SR); j = min(len(buf), i + len(x))
    if 0 <= i < len(buf): buf[i:j] += x[: j - i] * g


def rms_db(x):
    x = x[np.abs(x) > 1e-4]; return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)


def level(x, target): return x * 10 ** ((target - rms_db(x)) / 20)


def box(x, n):
    c = np.concatenate([[0.0], np.cumsum(x, dtype=np.float64)]); i = np.arange(len(x))
    lo, hi = np.clip(i - n // 2, 0, len(x)), np.clip(i - n // 2 + n, 0, len(x)); return ((c[hi] - c[lo]) / n).astype(np.float32)


# ---- voice: a01 is the lifeguard on the phone: clean while we see him, through a phone band once we are with ยาย (cut 2) ----
vo = np.zeros(N, np.float32)
for s in SC["shots"]:
    for v in s["vo"]:
        x = level(load(os.path.join(VO, f"{v['id']}.wav")), -18); t0 = s["start"] + v["t"]
        if v["id"] == "a01":
            k = int((C(2) - t0) * SR); ph = level(filt(x, "highpass=f=320,lowpass=f=3200,acompressor=threshold=0.1:ratio=3"), -19)
            xf = int(0.03 * SR); r = np.linspace(0, 1, xf, dtype=np.float32)
            x = np.concatenate([x[:k], x[k:k + xf] * (1 - r) + ph[k:k + xf] * r, ph[k + xf:]])
        place(vo, x, t0)
# ---- SFX ----
CUES = [(0.0, "ring", 0.18), (C(4) + 0.3, "rustle", 0.2), (C(4) + 0.75, "ching", 0.14), *[(C(4) + 0.9 + i * 0.22, "steps", 0.1) for i in range(2)],
        *[(C(5) + 0.35 + i * 0.32, "knock", 0.12) for i in range(3)], (C(7) + 0.05, "swell", 0.16), (C(8) + 0.02, "thud", 0.18)]
cues = {"duration": TOTAL, "sections": [{"start": 0, "end": TOTAL, "mood": "silence"}], "sfx": [{"t": round(t, 3), "type": k, "gain": g} for t, k, g in CUES]}
json.dump(cues, open(os.path.join(HERE, "sfx_cues.json"), "w"))
subprocess.run(["python3", os.path.join(HERE, "..", "synth.py"), os.path.join(HERE, "sfx_cues.json"), os.path.join(HERE, "sfx.wav")], check=True, env={**os.environ, "STEMS": "1"})
sfx = load(os.path.join(HERE, "sfx_sfx.wav"))[:N]; sfx = np.pad(sfx, (0, N - len(sfx)))
sfx = filt(level(sfx, -27), "lowpass=f=3000,lowpass=f=3000,highpass=f=40")
# ---- ambience: the beach (A1, B1, B2) and the dawn porch (A1b, A2: a rooster far off, the sea through the window, low) ----
AMB = "/home/user/github-commit-quest-v2/video/jelly-ep1/production/ambience"
af = "lowpass=f=2000,lowpass=f=2000,lowpass=f=2000,highpass=f=60"
waves, gulls, rooster = (filt(load(os.path.join(AMB, n + ".mp3")), af) for n in ("waves", "gulls", "rooster"))
def span(x, a, b, lvl, fade=0.08):
    out = np.zeros(N, np.float32); x = level(x, lvl); n = int((b - a) * SR)
    while len(x) < n: x = np.concatenate([x, x])
    seg = x[:n].copy(); f = int(fade * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f); place(out, seg, a); return out
amb = span(waves, 0, C(2), -36) + span(waves, C(2), C(5), -46) + span(waves, C(5), TOTAL, -36)
place(amb, level(rooster, -44), C(2) + 0.4); place(amb, level(gulls, -40), C(5) + 0.6)
# ---- music: suno1 at the ทะเลลด level, a small dip on the photo, the same duck ----
mus = load(os.path.join(HERE, "..", "music", "suno1.mp3"))[int(20 * SR):][:N]
t = np.arange(N) / SR
g = 1 - 0.5 * np.clip((t - (C(7) - 0.25)) / 0.25, 0, 1)
mus = level(mus * g.astype(np.float32), -30)
env = box(np.abs(vo), int(0.05 * SR))
duck = box(1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1), int(0.25 * SR))
mstem = mus * duck
mix = vo + mstem + sfx + amb


def wr(path, x):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", "-c:a", "pcm_s16le", path], input=x.astype(np.float32).tobytes(), check=True)


def integrated(path):
    import re
    out = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", out)[-1])


tmp = os.path.join(HERE, "mix_raw.wav")
knee = lambda y: np.where(np.abs(y) > 0.6, np.sign(y) * (0.6 + 0.19 * np.tanh((np.abs(y) - 0.6) / 0.19)), y).astype(np.float32)
gain = 1.0
for _ in range(3):
    wr(tmp, knee(mix * gain)); gain *= 10 ** ((-14.0 - integrated(tmp)) / 20)
os.remove(tmp)
wr(os.path.join(HERE, "mix.wav"), knee(mix * gain)); wr(os.path.join(HERE, "vo_stem.wav"), vo * gain); wr(os.path.join(HERE, "music_stem.wav"), mstem * gain)
print("bridges mix", TOTAL, "gain", round(20 * np.log10(gain), 2))

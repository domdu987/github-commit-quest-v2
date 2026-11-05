"""เสียงรถไฟ mixer core (from video/release/audio/takhian-tide-mix/lib/mixcore.py).
- voice: every line levelled on its own to -18 dB RMS (A3)
- sfx: short events from ../sfxlib, the bus low-passed at 4.5 kHz and levelled to -27 dB RMS (A3, A4)
- the storm's roar: its own bus, low-passed at 900 Hz so it reads as a freight-train rumble and never as hiss (A4),
  ducked a little under the voice
- music: video/music/suno1.mp3 from 0 s, unfiltered, dips and boosts, -30 dB RMS after the dips, duck 0.65 (A5)
- one static gain to -14 LUFS integrated, so vo_stem.wav and music_stem.wav are exactly what is in mix.wav (musiccheck)."""
import json, os, re, subprocess
import numpy as np
SR = 48000
VIDEO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SFXLIB = os.path.join(VIDEO, "tornado", "sfxlib")


class Mix:
    def __init__(self, here, out=None, vo_dirs=None):
        self.here, self.out = here, out or here
        self.vo_dirs = vo_dirs or [os.path.join(here, "vo")]   # the full story reads ep1/vo and ep2/vo
        self.SC = json.load(open(os.path.join(here, "schedule.json")))
        self.SH = {s["key"]: s for s in self.SC["shots"]}
        self.TOTAL = self.SC["total"]; self.N = int(self.TOTAL * SR)
        self.t = np.arange(self.N) / SR
        self.vo = np.zeros(self.N, np.float32); self.sfx = np.zeros(self.N, np.float32); self.amb = np.zeros(self.N, np.float32)
        self.gain = np.ones(self.N, np.float32); self.ambg = np.ones(self.N, np.float32)
        self.cache = {}

    def load(self, path):
        raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
        return np.frombuffer(raw, dtype=np.float32).copy()

    def place(self, buf, x, t, g=1.0):
        i = int(max(0, t) * SR); j = min(len(buf), i + len(x))
        if i < len(buf): buf[i:j] += x[: j - i] * g

    @staticmethod
    def rms_db(x):
        x = x[np.abs(x) > 1e-4]
        return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)

    def level(self, x, target):
        return x * 10 ** ((target - self.rms_db(x)) / 20)

    def T(self, k, t=0.0):
        s = self.SH[k]; return s["start"] + (t if t >= 0 else s["dur"] + t)

    def vo_t(self, k, i=0): return self.SH[k]["vo"][i]["t"]
    def vo_end(self, k, i=0): return self.SH[k]["vo"][i]["t"] + self.SH[k]["vo"][i]["dur"]
    def frag(self, k, i=0, j=0): return self.SH[k]["vo"][i]["t"] + self.SH[k]["vo"][i]["frags"][j]

    def voices(self, line_gain={}):
        for s in self.SC["shots"]:
            for v in s["vo"]:
                x = self.load(next(p for p in (os.path.join(d, f"{v['id']}.wav") for d in self.vo_dirs) if os.path.exists(p)))
                self.place(self.vo, self.level(x, -18 + line_gain.get(v["id"], 0)), s["start"] + v["t"])

    def filt(self, x, af):
        out = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", af, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                             input=x.astype(np.float32).tobytes(), capture_output=True, check=True).stdout
        y = np.frombuffer(out, np.float32).copy(); return np.pad(y, (0, max(0, len(x) - len(y))))[: len(x)]

    def heart(self):
        """One lub-dub, synthesized: low thumps with two harmonics so a phone speaker still carries it."""
        n = int(0.8 * SR); t = np.arange(n) / SR; x = np.zeros(n)
        for t0, a in ((0.0, 1.0), (0.26, 0.7)):
            tt = t - t0; env = np.where(tt >= 0, np.exp(-np.clip(tt, 0, None) / 0.07) * (1 - np.exp(-np.clip(tt, 0, None) / 0.004)), 0)
            x += a * env * (np.sin(2 * np.pi * 55 * tt) + 0.45 * np.sin(2 * np.pi * 110 * tt) + 0.2 * np.sin(2 * np.pi * 165 * tt))
        return self.level(x.astype(np.float32), -20)

    def smp(self, name):
        if name in self.cache: return self.cache[name]
        L = lambda f: self.load(os.path.join(SFXLIB, f + ".mp3"))
        if name in ("crack", "crack2"):   # lightning: the crack only (≤ 0.45 s), then thunder low-passed under 300 Hz
            x = L("strike" if name == "crack" else "strike2")[: int(0.45 * SR)]; x[-int(0.12 * SR):] *= np.linspace(1, 0, int(0.12 * SR))
            rum = self.filt(L("thundermid"), "lowpass=f=300,lowpass=f=300")
            y = np.zeros(int(0.2 * SR) + len(rum), np.float32); y[: len(x)] += self.level(x, -20); y[int(0.2 * SR):] += self.level(rum, -18)
            self.cache[name] = y
        elif name == "zap":   # a transformer blowing: the first 0.3 s of a crack
            x = L("strike2")[: int(0.3 * SR)]; x[-int(0.1 * SR):] *= np.linspace(1, 0, int(0.1 * SR)); self.cache[name] = self.level(x, -20)
        elif name == "rumble":   # far thunder, low-passed
            self.cache[name] = self.level(self.filt(L("thunderfar"), "lowpass=f=260,lowpass=f=260"), -20)
        elif name == "heart":
            self.cache[name] = self.heart()
        else:
            x = L(name); n = int(0.02 * SR); x[:n] *= np.linspace(0, 1, n); x[-n * 4:] *= np.linspace(1, 0, n * 4)
            self.cache[name] = self.level(x, -20)
        return self.cache[name]

    def fx(self, k, t, name, g=1.0):
        self.place(self.sfx, self.smp(name), self.T(k, t) if k else t, g)

    def roar(self, a, b, g=1.0, lp=900, fade=0.8, step=1.4):
        """The freight-train roar from absolute time a to b. The 6 s take swells and dies away, so the bed is built from copies
        overlapping every ~1.4 s (already full at a) and then evened out over 0.6 s windows: the roar never stops, as the story says."""
        key = f"roar{lp}"
        if key not in self.cache: self.cache[key] = self.level(self.filt(self.load(os.path.join(SFXLIB, "trainroar.mp3")), f"lowpass=f={lp},lowpass=f={lp},highpass=f=30"), -20)
        x = self.cache[key]; n = int((b - a) * SR); rng = np.random.default_rng(int(a * 100))
        y = np.zeros(n + len(x), np.float32); pos = -int(4.5 * SR)
        while pos < n:
            i0 = max(0, -pos); y[max(0, pos): pos + len(x)] += x[i0:] * (0.85 + 0.3 * rng.random())
            pos += int(step * SR * (0.8 + 0.4 * rng.random()))
        y = y[:n]; e = np.sqrt(self.box(y * y, int(0.6 * SR))) + 1e-6
        y = y / e ** 0.85; y = self.level(y, -20)
        f = min(int(fade * SR), n // 2); y[:f] *= np.linspace(0, 1, f); y[n - f:] *= np.linspace(1, 0, f)
        self.place(self.amb, y, a, g)

    def env(self, arr, t0, t1, lvl, ramp=0.25):
        # NB a dip (lvl <= 1) is np.minimum against 1 outside its window too, so it also cancels every boost made before it,
        # anywhere in the story; boosts made after it survive. The delivered mixes were made with this (full/mix.py's EP.1 lifts
        # at the touchdown and the roof, and its xpass swell, are cancelled by the dips that follow them): kept for their re-runs.
        # New mixes: make the dips first, then the boosts.
        a = np.clip((self.t - (t0 - ramp)) / ramp, 0, 1) * np.clip(((t1 + ramp) - self.t) / ramp, 0, 1)
        if lvl <= 1: np.minimum(arr, 1 - (1 - lvl) * a, out=arr)
        else: arr *= 1 + (lvl - 1) * a

    def dip(self, t0, t1, lvl, ramp=0.25): self.env(self.gain, t0, t1, lvl, ramp)
    def boost(self, t0, t1, lvl, ramp=0.25): self.env(self.gain, t0, t1, lvl, ramp)
    def roar_level(self, t0, t1, lvl, ramp=0.4): self.env(self.ambg, t0, t1, lvl, ramp)

    @staticmethod
    def box(x, n):
        c = np.concatenate([[0.0], np.cumsum(x, dtype=np.float64)]); i = np.arange(len(x))
        lo, hi = np.clip(i - n // 2, 0, len(x)), np.clip(i - n // 2 + n, 0, len(x))
        return ((c[hi] - c[lo]) / n).astype(np.float32)

    def finish(self, cut=None, card=None, holes=(), amb_db=-31.0, segments=None, fade=None):
        src = self.load(os.path.join(VIDEO, "music", "suno1.mp3"))
        if segments is None:   # ทะเลลด recipe: suno1 from 0 s, no filter
            mus = np.pad(src, (0, max(0, self.N - len(src))))[: self.N]
        else:   # the full story: suno1 restarts at the chapter break; each segment (a, b, offset) gets 40 ms edges
            mus = np.zeros(self.N, np.float32)
            for a, b, off in segments:
                i, j, o = int(a * SR), min(self.N, int(b * SR)), int(off * SR); seg = src[o: o + j - i].copy(); e = int(0.04 * SR)
                seg[:e] *= np.linspace(0, 1, e); seg[-e:] *= np.linspace(1, 0, e); mus[i: i + len(seg)] += seg
        if fade is not None:   # the final card: the theme fades out under it
            a, b = int(fade[0] * SR), int(fade[1] * SR); mus[a:b] *= np.linspace(1, 0, b - a); mus[b:] = 0
        mus = mus * self.gain
        if cut is not None: mus[int(cut * SR):] = 0   # cliffhanger: the music stops with the black after the choice
        mus = self.level(mus, -30)
        sfx = self.level(self.filt(self.sfx, "lowpass=f=4500,lowpass=f=4500,highpass=f=40"), -27)
        amb = self.level(self.filt(self.amb * self.ambg, "lowpass=f=900,lowpass=f=900,highpass=f=30"), amb_db) if np.any(self.amb) else self.amb
        env = self.box(np.abs(self.vo), int(0.05 * SR)); v = np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
        duck = self.box(1 - 0.65 * v, int(0.25 * SR)); aduck = self.box(1 - 0.4 * v, int(0.25 * SR))
        mstem = mus * duck
        mix = self.vo + mstem + sfx + amb * aduck
        for h0, h1 in holes:   # a held breath: everything but the voice drops out (there is no voice inside a hole)
            a, b, r = int(h0 * SR), int(h1 * SR), int(0.06 * SR)
            mix[a - r:a] *= np.linspace(1, 0, r); mix[a:b] = self.vo[a:b]; mstem[a - r:a] *= np.linspace(1, 0, r); mstem[a:b] = 0
        if cut is not None and card is not None:
            a, b, r = int(cut * SR), int(card * SR), 240
            mix[a - r:a] *= np.linspace(1, 0, r); mix[a:b] = 0
        tmp = os.path.join(self.out, "mix_raw.wav")
        wr = lambda path, x: subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", "-c:a", "pcm_s16le", path], input=x.astype(np.float32).tobytes(), check=True)
        wr(tmp, mix); I = integrated(tmp); wr(tmp, mix * 10 ** ((-14.0 - I) / 20)); I2 = integrated(tmp); os.remove(tmp)
        g = 10 ** ((-14.0 - I) / 20) * 10 ** ((-14.0 - I2) / 20); mix, vo, mstem = mix * g, self.vo * g, mstem * g
        dz = (np.random.default_rng(7).standard_normal(self.N) * 1e-5).astype(np.float32); vo = vo + dz; mix = mix + dz   # ~-100 dBFS: R128 needs non-zero samples
        if np.max(np.abs(mix)) > 0.7: ax = np.abs(mix); mix = np.where(ax > 0.7, np.sign(mix) * (0.7 + 0.19 * np.tanh((ax - 0.7) / 0.19)), mix).astype(np.float32)
        wr(os.path.join(self.out, "mix.wav"), mix); wr(os.path.join(self.out, "vo_stem.wav"), vo); wr(os.path.join(self.out, "music_stem.wav"), mstem)
        print("mix written", self.TOTAL, "integrated after gain", integrated(os.path.join(self.out, "mix.wav")))


def integrated(path):
    out = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", out)[-1])

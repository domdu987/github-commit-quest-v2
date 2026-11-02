"""ต้นตะเคียนกลางนา mixer core: levelled voice + short event SFX from ../sfxlib + the story theme with dips/boosts and voice ducking.
No noise beds (A4): rain and thunder are short events only. Loudness target -14 LUFS (loudnorm aims -13.2)."""
import json, os, subprocess
import numpy as np
SR = 48000


class Mix:
    def __init__(self, here):
        self.here = here
        self.SC = json.load(open(os.path.join(here, "schedule.json")))
        self.SH = {s["key"]: s for s in self.SC["shots"]}
        self.TOTAL = self.SC["total"]; self.N = int(self.TOTAL * SR)
        self.t = np.arange(self.N) / SR
        self.vo = np.zeros(self.N, np.float32); self.sfx = np.zeros(self.N, np.float32)
        self.gain = np.ones(self.N, np.float32)
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

    def voices(self, line_gain={}):
        for s in self.SC["shots"]:
            for v in s["vo"]:
                x = self.load(os.path.join(self.here, "vo", f"{v['id']}.wav"))
                self.place(self.vo, self.level(x, -18 + line_gain.get(v["id"], 0)), s["start"] + v["t"])

    def smp(self, name):
        if name not in self.cache:
            x = self.load(os.path.join(self.here, "..", "sfxlib", f"{name}.mp3"))
            n = int(0.02 * SR); x[:n] *= np.linspace(0, 1, n); x[-n * 4:] *= np.linspace(1, 0, n * 4)
            self.cache[name] = self.level(x, -20)
        return self.cache[name]

    def fx(self, k, t, name, g=1.0):
        self.place(self.sfx, self.smp(name), self.T(k, t) if k else t, g)

    def dip(self, t0, t1, lvl, ramp=0.25):
        a = np.clip((self.t - (t0 - ramp)) / ramp, 0, 1) * np.clip(((t1 + ramp) - self.t) / ramp, 0, 1)
        np.minimum(self.gain, 1 - (1 - lvl) * a, out=self.gain)

    def boost(self, t0, t1, lvl, ramp=0.25):
        a = np.clip((self.t - (t0 - ramp)) / ramp, 0, 1) * np.clip(((t1 + ramp) - self.t) / ramp, 0, 1)
        self.gain = self.gain * (1 + (lvl - 1) * a)

    @staticmethod
    def box(x, n):
        c = np.concatenate([[0.0], np.cumsum(x, dtype=np.float64)]); i = np.arange(len(x))
        lo, hi = np.clip(i - n // 2, 0, len(x)), np.clip(i - n // 2 + n, 0, len(x))
        return ((c[hi] - c[lo]) / n).astype(np.float32)

    def finish(self, music_offset=0.0, fade_from=None):
        mus = self.load(os.path.join(self.here, "..", "music", "takhian-theme.mp3"))[int(music_offset * SR):]
        while len(mus) < self.N: mus = np.concatenate([mus, mus])
        mus = mus[: self.N] * self.gain
        if fade_from is not None:
            a = int(fade_from * SR); mus[a:] *= np.linspace(1, 0, self.N - a)
        mus = self.level(mus, -30); sfx = self.level(self.sfx, -25)
        env = self.box(np.abs(self.vo), int(0.05 * SR))
        duck = 1 - 0.65 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
        duck = self.box(duck, int(0.25 * SR))
        mix = self.vo + mus * duck + sfx
        peak = np.max(np.abs(mix))
        if peak > 0.98: mix = np.tanh(mix / peak * 1.2) * 0.95
        raw = os.path.join(self.here, "mix_raw.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", raw], input=mix.astype(np.float32).tobytes(), check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", "loudnorm=I=-13.2:TP=-1.5:LRA=11", "-ar", "48000", os.path.join(self.here, "mix.wav")], check=True)
        os.remove(raw)
        print("mix written", self.TOTAL)

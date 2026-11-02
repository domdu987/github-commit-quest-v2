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

    def filt(self, x, af):
        """Run a mono float array through an ffmpeg audio filter (lowpass, etc.)."""
        out = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", af, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                             input=x.astype(np.float32).tobytes(), capture_output=True, check=True).stdout
        y = np.frombuffer(out, np.float32).copy(); return np.pad(y, (0, max(0, len(x) - len(y))))[: len(x)]

    def smp(self, name):
        if name not in self.cache and name in ("crack", "crack2"):
            # the lightning: only the crack (≤ 0.45 s) of the strike, then a low rumble (thunder low-passed under 300 Hz)
            x = self.load(os.path.join(self.here, "..", "sfxlib", ("strike" if name == "crack" else "strike2") + ".mp3"))[: int(0.45 * SR)]
            x[-int(0.12 * SR):] *= np.linspace(1, 0, int(0.12 * SR))
            rum = self.filt(self.load(os.path.join(self.here, "..", "sfxlib", "thundermid.mp3")), "lowpass=f=300,lowpass=f=300")
            y = np.zeros(int(0.2 * SR) + len(rum), np.float32); y[: len(x)] += self.level(x, -20); y[int(0.2 * SR):] += self.level(rum, -18)
            self.cache[name] = y
        if name not in self.cache and name == "rumble":
            self.cache[name] = self.level(self.filt(self.load(os.path.join(self.here, "..", "sfxlib", "thunderfar.mp3")), "lowpass=f=260,lowpass=f=260"), -20)
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
        mus = self.filt(mus[: self.N], "lowpass=f=6000,lowpass=f=6000") * self.gain
        if fade_from is not None:
            a = int(fade_from * SR); mus[a:] *= np.linspace(1, 0, self.N - a)
        mus = self.level(mus, -30); sfx = self.level(self.filt(self.sfx, "lowpass=f=4500,lowpass=f=4500,highpass=f=40"), -25)
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
        print(measure(os.path.join(self.here, "mix.wav")))


def measure(path, a=0, b=None):
    """Noise metrics: median spectral flatness inside 5–14 kHz ( 50 ms frames, voiced/loud frames only), % of 'noise windows'
    (flatness > 0.5 and above -50 dBFS), the longest run of noise windows, and the 5–14 kHz band level vs 200 Hz–5 kHz (median dB)."""
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"]); x = np.frombuffer(raw, np.float32)
    x = x[int(a * SR): int(b * SR) if b else None]
    n = int(0.05 * SR); fr = x[: len(x) // n * n].reshape(-1, n)
    P = np.abs(np.fft.rfft(fr * np.hanning(n), axis=1)) ** 2 + 1e-12; f = np.fft.rfftfreq(n, 1 / SR)
    band = (f >= 5000) & (f <= 14000); Pb = P[:, band]
    flat = np.exp(np.mean(np.log(Pb), 1)) / np.mean(Pb, 1)
    rms = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9); hidb = 10 * np.log10(Pb.sum(1) / (n * n / 4) + 1e-12); live = (rms > -50) & (hidb > -75)
    noise = (flat > 0.5) & live
    run = best = 0
    for v in noise: run = run + 1 if v else 0; best = max(best, run)
    hi = P[:, (f >= 5000) & (f <= 14000)].sum(1); lo = P[:, (f >= 200) & (f < 5000)].sum(1)
    rel = 10 * np.log10(hi / lo)
    if not live.any(): live = rms > -50
    return {"hf_band_dBFS_median": round(float(np.median(hidb[rms > -50])), 1), "flatness_5_14k_median": round(float(np.median(flat[live])), 3), "noise_windows_pct": round(100 * float(noise.sum()) / max(1, live.sum()), 1),
            "longest_noise_s": round(best * 0.05, 2), "hi_vs_mid_dB_median": round(float(np.median(rel[live])), 1)}

"""sfx_synth.py -- the scene-02 effects, synthesised by code (numpy + ffmpeg filters).  No network, no generated audio.
Every function returns a float64 array (n, 2) at 48 kHz, peak about 1 (levels are set in mix_sc02.py).  Deterministic
(a fixed seed per call).  The only recorded material the mix uses is the hook's own rain / siren beds and its scream,
for continuity across the join (see mix_sc02.py); nothing here reads a file.
"""
import numpy as np, subprocess

SR = 48000


def rng(seed):
    return np.random.default_rng(seed)


def ff(x, af):
    """run a mono or stereo float signal through an ffmpeg audio filter chain (biquads, echo, ...)."""
    x = np.asarray(x, np.float64)
    ch = 1 if x.ndim == 1 else x.shape[1]
    r = subprocess.run(["ffmpeg", "-v", "error", "-f", "f64le", "-ar", str(SR), "-ac", str(ch), "-i", "-", "-af", af, "-f", "f64le", "-ar", str(SR), "-ac", str(ch), "-"],
                       input=x.astype(np.float64).tobytes(), capture_output=True)
    if r.returncode: raise RuntimeError(r.stderr.decode()[-800:])
    y = np.frombuffer(r.stdout, np.float64)
    y = y.reshape(-1, ch) if ch > 1 else y
    n = len(x)
    if len(y) < n: y = np.concatenate([y, np.zeros((n - len(y),) + y.shape[1:])])
    return y[:n].copy()


def st(m, pan=0.0, width=0.0, seed=0):
    """mono -> stereo with a constant-power pan (-1 left .. 1 right); width > 0 decorrelates a little (2-8 ms delay)."""
    m = np.asarray(m, np.float64)
    a = (pan + 1) * np.pi / 4
    L = m * np.cos(a) * np.sqrt(2); R = m * np.sin(a) * np.sqrt(2)
    if width > 0:
        d = int(SR * (0.002 + 0.006 * width))
        R = np.concatenate([np.zeros(d), R[:-d]]) * (1 - 0.3 * width) + R * 0.3 * width
    return np.stack([L, R], 1)


def norm(x, peak=1.0):
    p = np.abs(x).max()
    return x * (peak / p) if p > 0 else x


def env_ad(n, a, d, curve=4.0):
    """attack a s (linear), exponential decay over d s."""
    t = np.arange(n) / SR
    e = np.where(t < a, t / max(a, 1e-6), np.exp(-curve * (t - a) / max(d, 1e-6)))
    return e


def modes(dur, freqs, decays, amps, seed=0, jitter=0.0):
    """damped sines (struck metal / panel / glass)."""
    n = int(dur * SR); t = np.arange(n) / SR; r = rng(seed); y = np.zeros(n)
    for f, d, a in zip(freqs, decays, amps):
        f = f * (1 + jitter * (r.random() - 0.5)); ph = r.random() * 2 * np.pi
        y += a * np.sin(2 * np.pi * f * t + ph) * np.exp(-t / d)
    return y


def noise(n, seed=0):
    return rng(seed).standard_normal(n)


def burst(dur, lo, hi, a=0.002, d=0.08, seed=0, curve=4.0):
    n = int(dur * SR)
    x = noise(n, seed) * env_ad(n, a, d, curve)
    af = []
    if lo: af.append("highpass=f=%d:poles=2" % lo)
    if hi: af.append("lowpass=f=%d:poles=2" % hi)
    return ff(x, ",".join(af)) if af else x


def pad(x, dur):
    n = int(dur * SR)
    return np.concatenate([x, np.zeros(max(0, n - len(x)))])[:n] if x.ndim == 1 else np.concatenate([x, np.zeros((max(0, n - len(x)), x.shape[1]))])[:n]


# ------------------------------------------------------------------------------------------------ the countdown
def tick(seed=0):
    """a dry quartz-watch tick, close: a 3 ms click with a small high ping."""
    n = int(0.06 * SR); t = np.arange(n) / SR
    c = burst(0.06, 2500, 9000, a=0.0003, d=0.004, seed=seed, curve=5)
    p = 0.35 * np.sin(2 * np.pi * 4200 * t) * np.exp(-t / 0.006) + 0.15 * np.sin(2 * np.pi * 7300 * t) * np.exp(-t / 0.004)
    return norm(c + p)


def heartbeat(seed=0, strength=1.0):
    """one lub-dub: two low thumps with a falling pitch, the second weaker (0.27 s later)."""
    n = int(0.75 * SR); t = np.arange(n) / SR; y = np.zeros(n)
    for t0, a, f0 in ((0.0, 1.0, 62.0), (0.27, 0.62, 74.0)):
        tt = t - t0; m = tt >= 0
        f = f0 * (1 + 0.5 * np.exp(-tt[m] / 0.02))
        ph = 2 * np.pi * np.cumsum(f) / SR
        y[m] += a * np.sin(ph) * (1 - np.exp(-tt[m] / 0.004)) * np.exp(-tt[m] / 0.075)
    y += 0.05 * burst(0.75, 0, 300, a=0.002, d=0.05, seed=seed)
    return norm(ff(y, "lowpass=f=180"))


def sub_swell(dur):
    """sub-bass swell (S048): 34 -> 46 Hz with a slow rumble, growing to the eye-open, then cut."""
    n = int(dur * SR); t = np.arange(n) / SR; u = t / dur
    f = 34 + 12 * u ** 2
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * (u ** 2.2) + 0.25 * np.sin(2 * np.pi * np.cumsum(2 * f) / SR) * u ** 3
    y += 0.2 * ff(noise(n, 7), "lowpass=f=90,lowpass=f=90") * u ** 2 * 6
    y[-int(0.004 * SR):] *= np.linspace(1, 0, int(0.004 * SR))
    return norm(y)


def open_hit():
    """the eye-open: a short low thump and a dry high snap (the lids)."""
    n = int(0.9 * SR); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * (48 + 30 * np.exp(-t / 0.03)) * t) * np.exp(-t / 0.22)
    y += 0.3 * burst(0.9, 1800, 7000, a=0.0005, d=0.02, seed=11)
    return norm(y)


# ------------------------------------------------------------------------------------------------ the set
def car_alarm(dur, t_film0, period=10 / 24.0, duty=0.5, seed=0):
    """two-tone car horn alarm locked to the X1 alarm lamps (10-frame cycle, lamps on for the first half of it).
    t_film0 = the film time of sample 0; the cycle's phase is taken on the scene's frame clock (frame % 10 == 0 -> on)."""
    n = int(dur * SR); t = np.arange(n) / SR + t_film0
    loc = t * 24.0 - 1280.0                                  # scene-02 frame (the lamps key on the stage frame g, g % 10)
    ph = (loc % 10.0) / 10.0
    cyc = np.floor(loc / 10.0)
    on = (ph < duty).astype(float)
    hi = (cyc % 2 == 0)                                      # the two tones alternate cycle by cycle
    f = np.where(hi, 470.0, 380.0)
    p = 2 * np.pi * np.cumsum(f) / SR
    sq = np.sign(np.sin(p)) * 0.6 + np.sign(np.sin(p * 1.26 + 0.3)) * 0.4          # two detuned square horns
    g = ff(on, "lowpass=f=120")                              # soft key edges
    y = ff(sq * g, "highpass=f=250,lowpass=f=2600,equalizer=f=900:t=q:w=1.2:g=5")
    return norm(y)


def beacon_hum(dur, t_film0):
    """the light bar on the rescue truck: a low motor / relay hum swelling with the rotation (20-frame cycle), very quiet in the mix."""
    n = int(dur * SR); t = np.arange(n) / SR + t_film0
    ph = ((t * 24.0) % 20.0) / 20.0
    am = 0.55 + 0.45 * np.cos(2 * np.pi * ph)
    y = (np.sin(2 * np.pi * 100 * t) + 0.5 * np.sin(2 * np.pi * 200 * t + 0.4) + 0.25 * np.sin(2 * np.pi * 300 * t + 1.1)) * am
    y += 0.4 * ff(noise(n, 3), "bandpass=f=1800:width_type=q:w=2") * am
    clicks = np.zeros(n); k = ((t * 24.0) % 20.0) < (24.0 / SR * 1.5)
    clicks[k] = 1.0
    y += 0.6 * ff(clicks, "highpass=f=1500,lowpass=f=6000")
    return norm(y)


def rain_metal(dur, density=60.0, seed=0, lo=1800, hi=7500):
    """rain on truck / car metal: Poisson drops, each a click plus a tiny ping."""
    n = int(dur * SR); r = rng(seed); y = np.zeros(n)
    k = int(density * dur)
    pos = r.integers(0, n, k)
    L = int(0.03 * SR); tt = np.arange(L) / SR
    for i, p in enumerate(pos):
        f = r.uniform(2200, 6500); a = r.uniform(0.2, 1.0)
        g = a * (np.sin(2 * np.pi * f * tt) * np.exp(-tt / r.uniform(0.002, 0.008)) + 0.6 * r.standard_normal(L) * np.exp(-tt / 0.0015))
        e = min(n, p + L); y[p:e] += g[:e - p]
    return norm(ff(y, "highpass=f=%d,lowpass=f=%d" % (lo, hi)))


# ------------------------------------------------------------------------------------------------ impacts
def thud_ram(seed=1):
    """S027: the cutter body driven into the driver's back: a dull heavy thud, a short steel ring, cloth tearing."""
    n = int(1.2 * SR); t = np.arange(n) / SR
    body = np.sin(2 * np.pi * (70 + 60 * np.exp(-t / 0.02)) * t) * np.exp(-t / 0.10)
    ring = 0.25 * modes(1.2, [612, 1477, 2290, 3410], [0.25, 0.16, 0.10, 0.06], [1, 0.7, 0.5, 0.3], seed)
    hit = 0.6 * burst(1.2, 200, 3000, a=0.0008, d=0.03, seed=seed)
    tear = cloth_tear(0.35, seed + 4)
    y = body + ring + hit
    y[int(0.04 * SR):int(0.04 * SR) + len(tear)] += 0.45 * tear
    return norm(y)


def body_panel(seed=2, big=1.0):
    """a body slammed against a car / truck panel: a boom and the panel's modes."""
    n = int(1.6 * SR); t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (58 + 40 * np.exp(-t / 0.03)) * t) * np.exp(-t / 0.16)
    pan = modes(1.6, [143, 211, 327, 468, 703, 1012], [0.45, 0.38, 0.30, 0.22, 0.14, 0.09], [1, 0.8, 0.7, 0.5, 0.35, 0.2], seed, 0.1)
    hit = burst(1.6, 120, 2400, a=0.001, d=0.05, seed=seed)
    y = big * boom + 0.45 * pan + 0.5 * hit
    return norm(y)


def roof_bang(seed=3):
    """a boot landing on a car roof: hollow, short."""
    n = int(0.8 * SR); t = np.arange(n) / SR
    y = 0.7 * modes(0.8, [96, 151, 233, 389, 590], [0.18, 0.14, 0.10, 0.07, 0.05], [1, 0.8, 0.6, 0.4, 0.25], seed, 0.2)
    y += np.sin(2 * np.pi * (80 + 50 * np.exp(-t / 0.02)) * t) * np.exp(-t / 0.06)
    y += 0.4 * burst(0.8, 300, 3500, a=0.0008, d=0.025, seed=seed)
    return norm(y)


def hand_slap(seed=4):
    """flat hands slapping a wet bonnet."""
    y = burst(0.5, 400, 6000, a=0.0005, d=0.03, seed=seed) + 0.5 * modes(0.5, [180, 260, 420], [0.12, 0.09, 0.06], [1, 0.7, 0.5], seed)
    y += 0.25 * burst(0.5, 2500, 9000, a=0.003, d=0.12, seed=seed + 1)                   # water spray
    return norm(y)


def clank(seed=5):
    """teeth / claws on the cutter's steel arm."""
    y = modes(0.6, [1180, 1903, 2730, 3920, 5270], [0.09, 0.07, 0.05, 0.035, 0.025], [1, 0.8, 0.6, 0.4, 0.3], seed, 0.15)
    y += 0.5 * burst(0.6, 1500, 8000, a=0.0003, d=0.01, seed=seed)
    return norm(y)


def scrape(dur=0.6, seed=6):
    """teeth grinding along steel: band noise with a stick-slip stutter."""
    n = int(dur * SR); t = np.arange(n) / SR; r = rng(seed)
    am = (np.sin(2 * np.pi * (28 + 8 * np.sin(2 * np.pi * 3 * t)) * t) > 0.2).astype(float)
    am = ff(am, "lowpass=f=300")
    y = ff(noise(n, seed), "bandpass=f=2600:width_type=q:w=3") * am + 0.3 * modes(dur, [1903, 2730], [0.3, 0.2], [1, 0.6], seed) * am
    y *= np.minimum(1, t / 0.03) * np.minimum(1, (dur - t) / 0.08)
    return norm(y)


def windscreen_crack(seed=7):
    """a boot landing on a windscreen: a hollow knock and a fast crackle of the laminate."""
    n = int(0.7 * SR); r = rng(seed); y = np.zeros(n)
    y += 0.7 * modes(0.7, [210, 340, 520], [0.08, 0.06, 0.05], [1, 0.7, 0.5], seed)
    for i in range(55):
        p = int(SR * 0.25 * (r.random() ** 1.6)); L = int(0.004 * SR)
        e = min(n, p + L); y[p:e] += r.uniform(0.2, 1.0) * r.standard_normal(e - p) * np.exp(-np.arange(e - p) / (0.0008 * SR))
    return norm(ff(y, "highpass=f=150"))


def claws_metal(dur=1.0, seed=8):
    """claws scrabbling on a car roof: short screeches and taps."""
    n = int(dur * SR); r = rng(seed); y = np.zeros(n)
    for i in range(7):
        p = int(r.uniform(0, dur - 0.2) * SR); L = int(r.uniform(0.05, 0.16) * SR); tt = np.arange(L) / SR
        f = r.uniform(2400, 4200) * (1 + 0.3 * tt / tt[-1])
        g = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / tt[-1]) ** 2 * (0.5 + 0.5 * r.standard_normal(L) * 0.3)
        e = min(n, p + L); y[p:e] += r.uniform(0.4, 1.0) * g[:e - p]
        q = int(r.uniform(0, dur - 0.1) * SR); tp = burst(0.08, 800, 6000, a=0.0005, d=0.01, seed=seed + i)
        e = min(n, q + len(tp)); y[q:e] += 0.6 * tp[:e - q]
    return norm(y)


def glass_burst(seed=9):
    """a car window bursting: a crack, a spray of shards, tinkles falling on the road for half a second."""
    n = int(1.4 * SR); r = rng(seed); y = np.zeros(n)
    y += burst(1.4, 1800, 12000, a=0.0005, d=0.06, seed=seed)
    for i in range(70):
        p = int(SR * (0.01 + 0.8 * r.random() ** 1.8)); L = int(0.25 * SR); tt = np.arange(L) / SR
        g = r.uniform(0.1, 0.6) * np.sin(2 * np.pi * r.uniform(3000, 10500) * tt) * np.exp(-tt / r.uniform(0.01, 0.06))
        e = min(n, p + L); y[p:e] += g[:e - p]
    return norm(ff(y, "highpass=f=1200"))


def car_rock(seed=10):
    """the taxi on its springs after the impact: two soft creaks."""
    n = int(1.2 * SR); t = np.arange(n) / SR
    y = np.zeros(n)
    for t0 in (0.05, 0.45):
        tt = t - t0; m = (tt >= 0) & (tt < 0.3)
        y[m] += np.sin(2 * np.pi * (140 + 40 * tt[m]) * tt[m]) * (np.sin(2 * np.pi * 37 * tt[m]) > 0) * np.sin(np.pi * tt[m] / 0.3)
    return norm(ff(y, "bandpass=f=420:width_type=q:w=1.5"))


# ------------------------------------------------------------------------------------------------ bodies
def footstep(seed=0, wet=1.0, heavy=1.0):
    """a boot on wet concrete: a low knock, the sole, a small splash."""
    n = int(0.35 * SR); t = np.arange(n) / SR
    y = heavy * np.sin(2 * np.pi * (85 + 40 * np.exp(-t / 0.01)) * t) * np.exp(-t / 0.035)
    y += 0.5 * burst(0.35, 200, 1800, a=0.001, d=0.03, seed=seed)
    y += 0.35 * wet * burst(0.35, 2500, 9000, a=0.004, d=0.09, seed=seed + 100)
    return norm(y)


def drag(dur=0.32, seed=0):
    """a boot dragged on wet concrete."""
    n = int(dur * SR); t = np.arange(n) / SR
    y = ff(noise(n, seed), "bandpass=f=900:width_type=q:w=0.8") * np.sin(np.pi * t / dur) ** 1.5
    y += 0.3 * ff(noise(n, seed + 1), "highpass=f=3000") * np.sin(np.pi * t / dur)
    return norm(y)


def breath(dur, kind="out", seed=0, f=1200):
    """breath noise: 'in' rises, 'out' falls, 'pant' is short and hard."""
    n = int(dur * SR); t = np.arange(n) / SR; u = t / dur
    e = {"in": np.sin(np.pi * u) * (0.4 + 0.6 * u), "out": np.sin(np.pi * u) * (1.0 - 0.5 * u), "pant": np.sin(np.pi * u) ** 0.6}[kind]
    y = ff(noise(n, seed), "bandpass=f=%d:width_type=q:w=0.9,highpass=f=300" % f) * e
    return norm(y)


def shiver_cloth(dur, seed=0):
    """wet jacket fabric shivering: rapid soft rustles."""
    n = int(dur * SR); t = np.arange(n) / SR
    am = 0.5 + 0.5 * np.sin(2 * np.pi * 9 * t + np.sin(2 * np.pi * 1.3 * t))
    y = ff(noise(n, seed), "bandpass=f=2200:width_type=q:w=1.2") * am ** 2
    return norm(y)


def cloth_press(dur, seed=0):
    """a wet pad pressed on a wound: a squelch, then the soft rub of the gloves."""
    n = int(dur * SR); t = np.arange(n) / SR
    y = ff(noise(n, seed), "lowpass=f=900") * np.exp(-t / 0.12)
    y += 0.4 * ff(noise(n, seed + 1), "bandpass=f=1600:width_type=q:w=1") * (0.5 + 0.5 * np.sin(2 * np.pi * 2.2 * t)) * np.minimum(1, t / 0.1)
    return norm(y)


def cloth_tear(dur, seed=0):
    n = int(dur * SR); t = np.arange(n) / SR; r = rng(seed)
    am = (r.random(n // 120 + 1) > 0.45).repeat(120)[:n].astype(float)
    y = ff(noise(n, seed), "bandpass=f=3000:width_type=q:w=0.8") * am * np.exp(-t / (0.6 * dur))
    return norm(y)


def growl(dur, f0=82.0, seed=0, hard=1.0, rise=0.0):
    """an infected snarl: a jittery low voice with vocal fry and a hiss, through two formants."""
    n = int(dur * SR); t = np.arange(n) / SR; r = rng(seed); u = t / dur
    jit = ff(r.standard_normal(n), "lowpass=f=12") * 40
    f = f0 * (1 + rise * u) * (1 + 0.06 * jit)
    ph = 2 * np.pi * np.cumsum(f) / SR
    saw = 2 * ((ph / (2 * np.pi)) % 1.0) - 1
    fry = 0.55 + 0.45 * np.sign(np.sin(2 * np.pi * 31 * t + 3 * np.sin(2 * np.pi * 2.1 * t)))
    v = saw * fry
    y = ff(v, "bandpass=f=520:width_type=q:w=1.6") + 0.7 * ff(v, "bandpass=f=1250:width_type=q:w=2.2") + 0.25 * ff(v, "lowpass=f=300")
    y += 0.35 * hard * ff(noise(n, seed + 1), "bandpass=f=3200:width_type=q:w=1.0")
    e = np.minimum(1, t / 0.04) * np.minimum(1, (dur - t) / 0.12)
    return norm(y * e)


def inhale_infected(dur=1.1, seed=12):
    """S049: a long rasping inhale that ends in a click of the throat."""
    b = breath(dur, "in", seed, f=900)
    g = growl(dur, 70, seed, hard=0.5, rise=0.25) * np.linspace(0.2, 0.7, int(dur * SR))
    return norm(b + 0.6 * g)


def sniff(seed=0):
    """short searching breaths through the nose (S054)."""
    y = np.concatenate([breath(0.09, "pant", seed + i, f=2400) * (0.7 + 0.3 * (i % 2)) for i in range(3)] + [np.zeros(int(0.05 * SR))])
    return norm(y)


def horn(dur=0.7, f=(352.0, 440.0), seed=0):
    n = int(dur * SR); t = np.arange(n) / SR
    y = sum(np.sign(np.sin(2 * np.pi * ff_ * t + i)) for i, ff_ in enumerate(f))
    e = np.minimum(1, t / 0.01) * np.minimum(1, (dur - t) / 0.03)
    return norm(ff(y * e, "lowpass=f=2400,highpass=f=200"))


def crowd_roar(dur, seed=0):
    """far crowd panic: many voices as formant-filtered noise with irregular swells (screams are layered in the mix)."""
    n = int(dur * SR); t = np.arange(n) / SR; r = rng(seed); y = np.zeros(n)
    for i in range(10):
        f = r.uniform(500, 1400)
        am = ff(r.standard_normal(n), "lowpass=f=4") * 8
        am = np.clip(am, 0, None)
        y += ff(noise(n, seed + i), "bandpass=f=%d:width_type=q:w=4" % f) * am
    y *= np.minimum(1, t / 0.25) * np.minimum(1, (dur - t) / 0.4)
    return norm(y)


def far(x, amount=0.5):
    """push a sound away: low-pass, thinner, with an outdoor slap-back."""
    y = ff(x, "lowpass=f=%d,highpass=f=180,aecho=0.8:0.6:90|170:0.35|0.2" % int(5000 - 3200 * amount))
    return y

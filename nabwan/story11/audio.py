# "12 ฤดูฝน ที่ไหล่ของพ่อเปียก" soundtrack: Puck narration (1.2x) placed take by take, the ElevenLabs score (levelled, ducked
# under the voice, lifted for the title and end card), rain beds per location (street, school, porch, muffled indoors, glass),
# umbrella patter, wet footsteps and action sounds synced to story11/scenes.js.
# Usage (from the scratchpad root): python story11/audio.py story11/segments.json story11/music/music.mp3 <out>
import sys, json, subprocess
import numpy as np
import soundfile as sf

SR = 44100
seg_path, music_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
js = open('story11/vo.js').read()
P = json.loads(js[js.index('{'):js.rindex('}') + 1])['P']
DUR = P['DUR']
N = int(SR * DUR)
rng = np.random.default_rng(41)


def tt(d):
    return np.arange(int(SR * d)) / SR


def place(buf, sig, at, gain=1.0, pan=0.0):
    """Add mono or stereo sig into the stereo buf at time `at` (pan -1..1 for mono)."""
    i = int(at * SR)
    if sig.ndim == 1:
        sig = np.stack([sig * np.sqrt(0.5 * (1 - pan)), sig * np.sqrt(0.5 * (1 + pan))], axis=1) * np.sqrt(2)
    j = min(len(buf), i + len(sig))
    if j > i:
        buf[i:j] += gain * sig[: j - i]


def band(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))


def norm(x):
    return x / (np.max(np.abs(x)) + 1e-9)


def env_ad(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(t / a, 1) * np.exp(-t / d)


# ---------------- sound primitives ----------------
def blip(f0, f1, dur, vol):
    t = tt(dur); f = np.linspace(f0, f1, len(t))
    return vol * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (dur / 3)) * np.minimum(t / 0.003, 1)


def bell(f, dur, vol):
    t = tt(dur)
    return vol * sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t / (dur / (1 + m))) for m, a in [(1, 1), (2.76, 0.4), (5.4, 0.15)])


def noise_burst(dur, vol, lo, hi, shape=1.5):
    n = int(SR * dur)
    x = norm(band(rng.standard_normal(n), lo, hi))
    return vol * x * np.sin(np.linspace(0, np.pi, n)) ** shape


def whoosh(dur, vol, f0, f1):
    n = int(SR * dur)
    lo = norm(band(rng.standard_normal(n), f0, f0 * 3)); hi = norm(band(rng.standard_normal(n), f1 / 3, f1))
    k = np.linspace(0, 1, n)
    return vol * ((1 - k) * lo + k * hi) * np.sin(np.linspace(0, np.pi, n)) ** 2


def thump(f, dur, vol):
    t = tt(dur)
    return vol * np.sin(2 * np.pi * f * t * (1 - 0.3 * t / dur)) * np.exp(-t / (dur / 4))


def tick(vol, f=3200):
    t = tt(0.025)
    return vol * np.sin(2 * np.pi * f * t) * np.exp(-t / 0.004)


def sparkle(vol, base=2093, n=5, step=0.045):
    out = np.zeros(int(SR * (n * step + 0.8)))
    for i in range(n):
        s = bell(base * 2 ** (rng.integers(0, 8) / 12), 0.6, vol)
        out[int(i * step * SR): int(i * step * SR) + len(s)] += s
    return out


def chirp_bird(vol):
    out = np.zeros(int(SR * 0.6)); p = 0
    for _ in range(rng.integers(2, 5)):
        d = rng.uniform(0.05, 0.11); t = tt(d)
        f = np.linspace(rng.uniform(2600, 3600), rng.uniform(4200, 5600), len(t))
        s = vol * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** 2
        out[p:p + len(s)] += s; p += len(s) + int(SR * rng.uniform(0.02, 0.06))
        if p > len(out) - SR * 0.12: break
    return out


def bed(dur, lo, hi, vol, mod=0.15, rate=0.3):
    n = int(SR * dur)
    x = norm(band(rng.standard_normal(n), lo, hi))
    t = np.arange(n) / SR
    return vol * x * (1 + mod * np.sin(2 * np.pi * rate * t + rng.uniform(0, 6)))


def movavg(x, w):
    # O(N) centred moving average (np.convolve is O(N*w) and far too slow for second-long windows)
    c = np.cumsum(np.r_[np.zeros(w // 2 + 1), x, np.zeros(w - w // 2)])
    return (c[w:w + len(x)] - c[:len(x)]) / w


def fade(x, a=0.4, b=0.6):
    n = len(x); e = np.ones(n)
    ia, ib = int(a * SR), int(b * SR)
    e[:ia] = np.linspace(0, 1, ia); e[n - ib:] = np.linspace(1, 0, ib)
    return x * e



def drop_plip(vol):
    t = tt(0.12); f = 700 + 1100 * (1 - np.exp(-t / 0.02))
    return vol * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.035) * np.minimum(t / 0.002, 1)


def glide(f0, f1, dur, vol):
    t = tt(dur); f = np.geomspace(f0, f1, len(t))
    return vol * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / dur) ** 1.5


def softsq(f, dur, vol, harm=5):
    t = tt(dur)
    return vol * sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, harm + 1, 2)) * np.minimum(t / 0.004, 1) * np.minimum((dur - t) / 0.01, 1)


def old_ring(dur, vol):
    """keypad-phone ring: a fast two-note trill in bursts"""
    out = np.zeros(int(SR * dur)); p = 0.0
    while p < dur - 0.2:
        for k in range(int(0.7 / 0.06)):
            s = softsq(1319 if k % 2 == 0 else 1047, 0.055, vol)
            i = int((p + k * 0.06) * SR); out[i:i + len(s)] += s[: max(0, len(out) - i)]
        p += 1.05
    return out


def buzz(dur, vol):
    t = tt(dur)
    return vol * np.tanh(3 * np.sin(2 * np.pi * 155 * t)) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t)) * np.sin(np.pi * t / dur) ** 0.3


def dtmf(lo, hi, vol, dur=0.09):
    t = tt(dur)
    return vol * (np.sin(2 * np.pi * lo * t) + np.sin(2 * np.pi * hi * t)) * 0.5 * np.minimum(t / 0.003, 1) * np.minimum((dur - t) / 0.006, 1)


def step(vol):
    return noise_burst(0.09, vol, 300, 4000, 0.8) + thump(90, 0.09, vol * 0.8)


def clank(vol, f=1850):
    t = tt(0.5)
    return vol * sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t / (0.12 / m ** 0.5)) for m, a in [(1, 1), (1.47, 0.6), (2.31, 0.4), (3.9, 0.2)])


def cicada(dur, vol):
    n = int(SR * dur); t = np.arange(n) / SR
    x = norm(band(rng.standard_normal(n), 4200, 7200))
    return vol * x * (0.55 + 0.45 * np.sin(2 * np.pi * 38 * t)) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.23 * t))


def crickets(dur, vol):
    out = np.zeros(int(SR * dur))
    for c in range(2):
        t0 = rng.uniform(0, 0.4)
        while t0 < dur - 0.2:
            for k in range(3):
                s = tt(0.02); ch = vol * np.sin(2 * np.pi * (4300 + 400 * c) * s) * np.sin(np.pi * s / 0.02)
                i = int((t0 + k * 0.034) * SR); out[i:i + len(ch)] += ch[: max(0, len(out) - i)]
            t0 += rng.uniform(0.6, 1.0)
    return out


def fan(dur, vol):
    n = int(SR * dur); t = np.arange(n) / SR
    x = norm(band(rng.standard_normal(n), 250, 1500))
    return vol * (x * (0.75 + 0.25 * np.sin(2 * np.pi * 15 * t)) + 0.5 * np.sin(2 * np.pi * 50 * t))


def ticks_roll(t0, t1, n, vol, f=3200):
    for k in range(n):
        place(sfx, tick(vol, f), t0 + (t1 - t0) * (1 - (1 - k / n) ** 0.5))


sfx = np.zeros((N, 2))
amb = np.zeros((N, 2))
SC = {'s0': 0, 's1a': P['A0'] - 0.3, 's1b': P['A2'] - 0.3, 's1c': P['A4'] - 0.3, 's1d': P['A5'] - 0.3, 's2': P['B0'] - 0.3, 's2i': P['B4'] - 0.1,
      's3a': P['C0'] - 0.3, 's3b': P['C2'] - 0.3, 's3f': P['Cend'] - 0.15, 's4': P['title'], 's5a': P['D0'] - 0.1, 's5b': P['D3'] - 0.3, 's6': P['end']}


def birds(t0, dur, vol, density=1.0):
    t = t0 + rng.uniform(0.1, 0.5)
    while t < t0 + dur - 0.6:
        place(amb, chirp_bird(vol * rng.uniform(0.6, 1.0)), t, pan=rng.uniform(-0.8, 0.8))
        t += rng.uniform(0.5, 1.4) / density


def chime(t, vol=0.06, notes=(1568, 2093)):
    for i, f in enumerate(notes):
        place(sfx, bell(f, 0.9, vol), t + i * 0.09)


def ding(vol=0.08):
    return bell(1760, 1.2, vol) + bell(2637, 1.2, vol * 0.4)


def typing_clicks(t0, t1, rate, vol):
    t = t0
    while t < t1:
        place(sfx, tick(vol * rng.uniform(0.6, 1.0), rng.uniform(2200, 3400)), t, pan=rng.uniform(-0.2, 0.2))
        t += rng.uniform(0.5, 1.5) / rate


def key_clicks(t0, t1, vol=0.05, rate=11, pan=0.0):
    t = t0
    while t < t1:
        place(sfx, tick(vol * rng.uniform(0.7, 1.0), rng.uniform(2600, 3600)), t, pan=pan)
        t += rng.uniform(0.6, 1.4) / rate


def backspace(t0, t1, vol=0.045, pan=0.0):
    n = max(2, int((t1 - t0) / 0.05))
    for k in range(n):
        place(sfx, tick(vol, 1800 - 40 * k), t0 + k * (t1 - t0) / n, pan=pan)


def crumple_toss(t, vol=0.065):
    place(sfx, noise_burst(0.12, vol, 1500, 7000, 0.8), t)                       # paper crumple
    place(sfx, whoosh(0.35, vol * 0.8, 800, 4000), t + 0.05)
    place(sfx, thump(160, 0.08, vol * 1.6), t + 0.45); place(sfx, noise_burst(0.06, vol * 0.8, 800, 3000), t + 0.45)   # into the bin


def ping(t, vol=0.06, f=2093):
    place(sfx, bell(f, 0.7, vol), t); place(sfx, bell(f * 1.5, 0.5, vol * 0.5), t + 0.06)



def ringtone(dur, vol):
    """smartphone ring: a bright three-note marimba-ish figure, repeated"""
    out = np.zeros(int(SR * dur)); p = 0.0
    while p < dur - 0.3:
        for k, f in enumerate((1319, 1760, 2093, 1760)):
            s = bell(f, 0.35, vol)
            i = int((p + k * 0.12) * SR); out[i:i + len(s)] += s[: max(0, len(out) - i)]
        p += 1.0
    return out


def rumble(dur, vol, rate=1.6):
    n = int(SR * dur); t = np.arange(n) / SR
    x = norm(band(rng.standard_normal(n), 35, 260))
    return vol * x * (0.75 + 0.25 * np.sin(2 * np.pi * rate * t))


def rail_clacks(t0, t1, vol):
    t = t0 + 0.2
    while t < t1:
        place(amb, thump(70, 0.08, vol), t); place(amb, noise_burst(0.05, vol * 0.5, 600, 3000), t); place(amb, thump(66, 0.08, vol * 0.8), t + 0.13)
        t += 0.62


def heartbeat(t0, t1, vol, period=0.75):
    t = t0
    while t < t1:
        place(sfx, thump(52, 0.16, vol), t); place(sfx, thump(48, 0.18, vol * 0.75), t + 0.17)
        t += period


def coins(t, vol=0.05):
    for k in range(5):
        place(sfx, bell(3136 + 300 * (k % 3), 0.3, vol * (1 - k * 0.12)), t + k * 0.05)


def bloop(t, vol=0.06):
    place(sfx, blip(900, 520, 0.09, vol), t)



def jingle(t, vol=0.04):
    for k in range(6):
        place(sfx, bell(rng.uniform(2600, 4200), 0.25, vol * rng.uniform(0.6, 1.0)), t + k * rng.uniform(0.03, 0.06), pan=rng.uniform(-0.3, 0.3))


def paws(t0, t1, vol=0.05, rate=9):
    t = t0
    while t < t1:
        place(sfx, tick(vol, rng.uniform(900, 1400)), t); place(sfx, thump(180, 0.04, vol * 0.8), t)
        t += 1 / rate * rng.uniform(0.8, 1.2)


def wag_thumps(t0, t1, vol=0.05, period=0.32):
    t = t0
    while t < t1:
        place(sfx, thump(120, 0.08, vol), t); t += period


# ---------------- story7 sounds ----------------
def chatter(dur, vol):
    """canteen / restaurant walla: band-limited noise with syllable-rate wobble"""
    n = int(SR * dur); t = np.arange(n) / SR
    x = norm(band(rng.standard_normal(n), 250, 2600))
    wob = sum(0.25 * np.sin(2 * np.pi * r * t + rng.uniform(0, 6)) for r in (3.1, 4.7, 6.3))
    return vol * x * (0.6 + wob)


def sizzle(dur, vol):
    n = int(SR * dur); t = np.arange(n) / SR
    x = norm(band(rng.standard_normal(n), 2500, 9000)) * (0.75 + 0.25 * np.sin(2 * np.pi * 0.4 * t))
    pops = np.zeros(n)
    for _ in range(int(dur * 14)):
        i = rng.integers(0, n - 400); pops[i:i + 400] += rng.uniform(0.5, 1.5) * np.exp(-np.arange(400) / 60) * rng.choice([-1, 1])
    return vol * (x + 0.6 * band(pops, 1500, 9000))


def notif_pop(t, vol=0.06, f=1568):
    place(sfx, blip(f * 0.6, f, 0.06, vol * 1.2), t); place(sfx, bell(f, 0.6, vol), t + 0.03); place(sfx, bell(f * 1.5, 0.5, vol * 0.5), t + 0.09)


def clink(t, vol=0.08):
    place(sfx, clank(vol, 2600), t); place(sfx, clank(vol * 0.6, 3900), t + 0.012)


def tick_tock(t0, t1, vol=0.03):
    t, k = t0, 0
    while t < t1:
        place(amb, tick(vol, 1500 if k % 2 == 0 else 1150), t); t += 0.5; k += 1




def cash(t, vol=0.05):
    place(sfx, bell(2637, 0.5, vol), t); place(sfx, bell(3520, 0.6, vol * 0.8), t + 0.07); place(sfx, noise_burst(0.15, vol * 0.5, 3000, 9000), t)




def water_lap(dur, vol):
    n = int(SR * dur); t = np.arange(n) / SR
    x = norm(band(rng.standard_normal(n), 120, 1100))
    return vol * x * (0.55 + 0.45 * np.sin(2 * np.pi * 0.35 * t) * np.sin(2 * np.pi * 0.13 * t + 1))


def plop(vol):
    t = tt(0.25); f = 380 + 600 * np.exp(-t / 0.03)
    out = vol * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.06)
    nb = noise_burst(0.2, vol * 0.5, 300, 2500, 1.2); out[:len(nb)] += nb
    return out


def gecko(t0, vol):
    """ตุ๊กแก call: a rattle then a few two-syllable barks"""
    place(amb, noise_burst(0.5, vol * 0.5, 600, 2500, 0.6), t0)
    for k in range(4):
        for j, f in enumerate((520, 360)):
            place(amb, glide(f * 1.2, f, 0.14, vol), t0 + 0.6 + k * 0.62 + j * 0.2)


def rustle(t0, t1, vol, rate=6):
    t = t0
    while t < t1:
        place(sfx, noise_burst(rng.uniform(0.06, 0.16), vol * rng.uniform(0.6, 1.0), 1500, 8000, 0.8), t, pan=rng.uniform(-0.3, 0.1))
        t += rng.uniform(0.6, 1.4) / rate


def flick(t, vol=0.06):
    place(sfx, tick(vol * 1.4, 2400), t); place(sfx, noise_burst(0.05, vol, 2000, 9000), t)
    place(sfx, fade(noise_burst(0.5, vol * 0.7, 300, 2500, 0.7), 0.05, 0.3), t + 0.04)   # flame catching


def projector(t0, t1, vol):
    t = t0
    while t < t1:
        place(amb, tick(vol, rng.uniform(900, 1300)), t); t += 1 / 24 * rng.uniform(0.9, 1.1)


def far_firework(t, vol):
    place(amb, thump(55, 0.5, vol), t); place(amb, fade(noise_burst(0.9, vol * 0.4, 1500, 7000, 1.0), 0.1, 0.6), t + 0.12)



# ---------------- rain ----------------
def fftconv(a, k):
    n = len(a) + len(k) - 1; m = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(a, m) * np.fft.rfft(k, m), m)[:len(a)]


def rain_bed(dur, vol, lo=350, hi=8000, crackle=900):
    n = int(SR * dur)
    x = norm(band(rng.standard_normal(n), lo, hi))
    imp = np.zeros(n); k = int(dur * crackle); imp[rng.integers(0, n, k)] = rng.uniform(-1, 1, k)
    cr = norm(band(imp, max(lo, 1800), hi))
    return vol * (0.75 * x + 0.5 * cr)


def patter(dur, vol, rate=45):
    """rain drumming on umbrella cloth: dense soft taps with a little drum body"""
    n = int(SR * dur); imp = np.zeros(n); k = int(dur * rate)
    imp[rng.integers(0, n, k)] = rng.uniform(0.3, 1.0, k)
    kt = tt(0.03); ker = np.sin(2 * np.pi * 1500 * kt) * np.exp(-kt / 0.004) + 0.7 * np.sin(2 * np.pi * 380 * kt) * np.exp(-kt / 0.01)
    return vol * norm(fftconv(imp, ker))


def wet_step(vol):
    o = np.zeros(int(0.2 * SR))
    for x, d in [(noise_burst(0.08, vol, 700, 6000, 0.8), 0), (thump(85, 0.09, vol * 0.6), 0), (noise_burst(0.14, vol * 0.6, 1500, 7000, 1.4), int(0.02 * SR))]:
        o[d:d + len(x)] += x
    return o


def steps(t0, t1, period, vol, wet=True, pan=0.0, jitter=0.04):
    t = t0
    while t < t1:
        place(sfx, wet_step(vol * rng.uniform(0.75, 1.0)) if wet else step(vol * rng.uniform(0.75, 1.0)), t, pan=pan)
        t += period * rng.uniform(1 - jitter, 1 + jitter)


def umb_open(t, vol=0.08):
    place(sfx, whoosh(0.28, vol, 300, 2500), t)
    place(sfx, noise_burst(0.1, vol * 0.9, 600, 4000, 0.6), t + 0.22)          # the cloth snapping taut
    place(sfx, thump(140, 0.08, vol * 1.2), t + 0.24); place(sfx, tick(vol * 0.9, 2200), t + 0.25)   # runner clicks home


def umb_close(t, vol=0.07):
    place(sfx, tick(vol, 1900), t)
    place(sfx, whoosh(0.35, vol * 0.8, 400, 3000), t + 0.03)
    place(sfx, noise_burst(0.12, vol * 0.6, 500, 3000, 0.8), t + 0.32)


def shake(t, n, vol=0.05):
    for k in range(n):
        place(sfx, noise_burst(0.09, vol, 800, 5000, 0.7), t + k * 0.14)
        place(sfx, noise_burst(0.2, vol * 0.5, 2000, 8000, 1.5), t + k * 0.14 + 0.03)   # spray


def plips(t0, t1, rate, vol, pan=0.0):
    t = t0
    while t < t1:
        place(sfx, drop_plip(vol * rng.uniform(0.6, 1.0)), t, pan=pan + rng.uniform(-0.2, 0.2)); t += rng.uniform(0.6, 1.4) / rate


def thunder(t, vol, dist=1.0):
    place(amb, fade(rumble(3.2, vol, 0.7), 0.05 + 0.3 * dist, 1.8), t)
    place(amb, fade(noise_burst(0.5, vol * 0.5 * (1.4 - dist), 120, 2500, 0.6), 0.02, 0.3), t)


def pour(dur, vol):
    n = int(SR * dur); t = np.arange(n) / SR
    x = norm(band(rng.standard_normal(n), 300, 2400))
    return vol * x * (0.7 + 0.3 * np.sin(2 * np.pi * 7 * t) * np.sin(2 * np.pi * 1.3 * t))


def traffic(dur, vol):
    n = int(SR * dur); t = np.arange(n) / SR
    x = norm(band(rng.standard_normal(n), 60, 900))
    return vol * x * (0.7 + 0.3 * np.sin(2 * np.pi * 0.11 * t + 1))


def moto_pass(t, vol, pan0=-0.8, pan1=0.8, dur=2.4):
    tt_ = tt(dur); f = 95 + 25 * np.tanh((tt_ - dur / 2) * 2)
    s_ = vol * np.tanh(2.5 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.sin(np.pi * tt_ / dur) ** 2
    s_ = band(s_, 60, 3000)
    i = int(t * SR); L_ = len(s_); pan = np.linspace(pan0, pan1, L_)
    st = np.stack([s_ * np.sqrt(0.5 * (1 - pan)), s_ * np.sqrt(0.5 * (1 + pan))], axis=1) * np.sqrt(2)
    j = min(N, i + L_)
    if j > i: amb[i:j] += st[:j - i]


s = SC
T = lambda k: s[k]
rain_spans = [  # (start, end, vol, lo, hi) — street / school / soi rain
    (0, T('s1d'), 0.020, 350, 8000), (T('s1d'), T('s2'), 0.016, 300, 7000),
    (T('s3f'), T('s4'), 0.018, 350, 8000), (T('s5a'), T('s5b'), 0.012, 350, 5500)]
for a, b, v, lo, hi in rain_spans:
    place(amb, fade(rain_bed(b - a + 0.4, v, lo, hi), 0.3, 0.4), a)
# indoors: the rain is muffled behind the window; a fan, a clock
place(amb, fade(rain_bed(T('s3a') - T('s2') + 0.3, 0.012, 150, 1800, 200), 0.3, 0.3), T('s2'))
place(amb, fade(fan(T('s2i') - T('s2'), 0.004), 0.3, 0.3), T('s2'))
tick_tock(T('s2') + 0.2, T('s2i'), 0.012)
thunder(T('s2') + 2.3, 0.05, 0.6)
# present street: traffic, walla, motorbikes; the rain arrives at C2
place(amb, fade(traffic(T('s4') - T('s3a') + 0.3, 0.012), 0.4, 0.3), T('s3a'))
place(amb, fade(chatter(T('s3b') + 1.2 - T('s3a'), 0.006), 0.3, 0.6), T('s3a'))
moto_pass(T('s3a') + 0.6, 0.010, 0.8, -0.8); moto_pass(T('s3b') + 4.5, 0.008, -0.8, 0.8)
tRain = P['C2'] - 0.05
rb = rain_bed(T('s3f') - tRain + 0.3, 0.020); rb *= np.clip(np.arange(len(rb)) / (1.4 * SR), 0, 1)[:] ** 1.5
place(amb, fade(rb, 0.01, 0.2), tRain)
for k in range(9):
    place(sfx, drop_plip(0.03 * rng.uniform(0.6, 1.0)), tRain + k * 0.12 + rng.uniform(0, 0.08), pan=rng.uniform(-0.6, 0.6))   # the first fat drops
thunder(tRain + 0.35, 0.045, 0.8)
place(amb, fade(traffic(DUR - T('s5b'), 0.009), 0.5, 0.6), T('s5b'))
rb2 = rain_bed(DUR - T('s5b'), 0.020); rb2 *= np.clip(1 - 0.55 * (np.arange(len(rb2)) / SR - (P['D5'] - T('s5b'))) / (P['end'] - P['D5']), 0.45, 1)
place(amb, fade(rb2, 0.6, 0.6), T('s5b'))
place(amb, fade(rain_bed(P['D0'] - T('s4'), 0.010, 600, 9000, 300), 0.3, 0.3), T('s4'))   # rain on the glass (title)
place(amb, fade(rain_bed(DUR - P['end'], 0.006, 400, 6000), 0.3, 0.4), P['end'])

# ---------------- S0: hook ----------------
place(sfx, fade(bell(784, 2.5, 0.022), 0.2, 1.5), 0.3)
place(sfx, fade(patter(T('s1a') - 0.2, 0.012), 0.2, 0.3), 0.1)
steps(0.2, T('s1a'), 0.42, 0.03); steps(0.35, T('s1a'), 0.34, 0.022, pan=0.3)
plips(P['H2'] + 0.1, P['H4'] - 0.2, 6, 0.03, pan=-0.2)                                        # drops landing on his shoulder
place(sfx, sparkle(0.035, 1760, 7), P['H4'] + 0.15)

# ---------------- S1a / S1b: the school gate ----------------
place(sfx, whoosh(0.6, 0.045, 300, 2500), T('s1a') - 0.3)
for k, tf in enumerate([P['A0'] + 0.45, P['A0'] + 0.95, P['A0'] + 1.45]):
    place(sfx, whoosh(0.25, 0.035, 600, 4000), tf - 0.1); place(sfx, bell(1568 + 196 * k, 0.6, 0.025), tf)   # a grade flies by
k0, k1 = P['A0'] + 0.15, P['A1'] - 0.15
for k in range(12):
    tp = k0 + (k1 - k0) * k / 12 + 0.02
    place(sfx, drop_plip(0.035), tp); place(sfx, tick(0.012, 2600), tp)                     # a raindrop pip per rainy season
place(sfx, fade(patter(T('s1c') - T('s1b'), 0.012), 0.2, 0.2), T('s1b'))
tr0, tr1 = T('s1b') + (P['A2'] + 0.45 - T('s1b')) - 0.3 + 0.3, P['A3'] - 0.3
steps(tr0, tr1, 0.17, 0.03, pan=0.2)                                                          # the kid runs out
place(sfx, whoosh(0.3, 0.035, 500, 3000), tr1 - 0.05)
place(sfx, bell(1319, 0.9, 0.035), P['A3'] + 0.05); place(sfx, bell(1760, 0.8, 0.025), P['A3'] + 0.18)

# ---------------- S1c / S1d: home ----------------
place(sfx, fade(patter(T('s1d') + 0.8 - T('s1c'), 0.012), 0.1, 0.3), T('s1c'))
steps(T('s1c'), T('s1d') + 1.0, 0.42, 0.03); steps(T('s1c') + 0.15, T('s1d') + 1.1, 0.34, 0.022, pan=0.3)
place(amb, fade(pour(T('s2') - T('s1d'), 0.010), 0.2, 0.3), T('s1d'))                       # downspout into the dragon jar
plips(T('s1d'), T('s2'), 5, 0.02, pan=0.3)                                                    # the eave dripping
umb_close(T('s1d') + 0.72)
shake(T('s1d') + 1.55, 3, 0.04)
place(sfx, sparkle(0.04, 2093, 7), P['A6'] + 0.05)
for k in range(3):
    place(sfx, thump(150, 0.06, 0.03), P['A6'] + 0.1 + k * 0.45)                              # little hops
plips(P['Aend'] - 0.35, T('s2'), 6, 0.04, pan=-0.2)                                            # his back dripping onto the tiles

# ---------------- S2: the living room ----------------
place(sfx, whoosh(0.5, 0.035, 300, 2200), T('s2') - 0.25)
rustle(T('s2') + 0.2, P['B1'] - 0.2, 0.012, 3)                                                 # pencil and pages
place(sfx, blip(520, 800, 0.08, 0.05), P['B1'] + 0.05)                                           # the kid's bubble
rustle(P['B2'] - 0.15, P['B2'] + 0.25, 0.04, 14)                                                 # newspaper lowered
place(sfx, blip(420, 650, 0.09, 0.05), P['B2'] + 0.3)                                            # dad's bubble
place(sfx, thump(70, 0.25, 0.03), P['B4'] - 0.02)                                                # "หนัก" lands
# the shirt on the grille: drips into the bowl
plips(T('s2i') + 0.05, T('s3a') - 0.05, 5, 0.045)
place(sfx, fade(bell(659, 2.0, 0.02), 0.2, 1.4), T('s2i'))

# ---------------- S3a: present ----------------
place(sfx, ding(0.04), T('s3a') + 0.35)                                                          # the clinic's door chime
ticks_roll(T('s3a') + 0.25, T('s3a') + 1.3, 27, 0.018, 2600)                                   # 40 → 67
place(sfx, bell(1047, 1.2, 0.04), T('s3a') + 1.35)
steps(T('s3a') + 0.1, T('s3b') + (tRain - T('s3b')), 0.62, 0.022, wet=False)
t = T('s3a') + 0.3
while t < tRain:
    place(sfx, tick(0.03, 1300), t); place(sfx, thump(240, 0.04, 0.02), t); t += 0.62         # the umbrella-cane tapping
place(sfx, fade(whoosh(1.4, 0.03, 300, 1500), 0.3, 0.6), P['C1'] + 0.05)                        # the ghost strides past

# ---------------- S3b: the rain, the hand-off, the tilt ----------------
tLift, tTake, tOpen, tGo = P['C3'] - 0.7, P['C3'] + 0.4, P['C3'] + 0.95, P['C3'] + 1.6
place(sfx, noise_burst(0.25, 0.025, 600, 3000, 0.6), tLift + 0.1)
place(sfx, noise_burst(0.2, 0.03, 800, 4000, 0.7), tTake)                                        # the handle changes hands
umb_open(tOpen)
place(sfx, fade(patter(T('s3f') - tOpen, 0.016), 0.2, 0.2), tOpen + 0.25)
steps(tGo, T('s3f'), 0.6, 0.025); steps(tGo + 0.2, T('s3f'), 0.62, 0.02, pan=0.3)
place(sfx, glide(500, 760, 0.6, 0.02), P['C4'] + 0.1); place(sfx, blip(800, 1200, 0.07, 0.04), P['C4'] + 0.35)   # the tilt, "นิดเดียว"
plips(P['C5'], P['Cend'] - 0.6, 7, 0.035, pan=-0.3)                                            # rain on his own shoulder now
place(sfx, fade(bell(523, 2.6, 0.03), 0.3, 1.8), P['Cend'] - 0.3)                                 # he understands
place(sfx, fade(glide(1600, 800, 0.8, 0.012), 0.1, 0.5), T('s3f') - 0.1)                         # memory flash

# ---------------- S4: title ----------------
place(sfx, whoosh(0.8, 0.055, 300, 2000), T('s4') - 0.6)
for i in range(2):
    place(sfx, thump(110 - i * 8, 0.22, 0.07), T('s4') + 0.15 + i * 0.08)
place(sfx, bell(1319, 1.4, 0.05), T('s4') + 0.9)

# ---------------- S5a: the twelve rainy seasons (memory) ----------------
place(sfx, whoosh(0.6, 0.045, 300, 2500), T('s5a') - 0.3)
projector(T('s5a') + 0.1, T('s5b'), 0.008)
place(sfx, fade(patter(T('s5b') - T('s5a'), 0.009), 0.3, 0.4), T('s5a'))
tc3 = P['D2'] - 0.05 - T('s5a')
k0, k1 = T('s5a') + 0.3, T('s5a') + tc3 + 0.6
for k in range(12):
    place(sfx, drop_plip(0.03), k0 + (k1 - k0) * (k + 0.5) / 12)
for tcut in [P['D1'] - 0.05, P['D1'] + 1.25, P['D2'] - 0.05]:
    place(sfx, whoosh(0.3, 0.03, 500, 3000), tcut - 0.1)

# ---------------- S5b: walking him home ----------------
place(sfx, fade(patter(DUR - T('s5b') - 0.5, 0.013), 0.6, 1.0), T('s5b'))
tPush = P['D4'] - 0.2
steps(T('s5b') + 0.3, tPush - 0.3, 0.6, 0.022); steps(tPush + 1.3, P['end'], 0.6, 0.02)
rustle(tPush + 0.1, tPush + 0.6, 0.03, 10)
place(sfx, fade(bell(784, 1.6, 0.03), 0.1, 1.0), tPush + 1.0)                                    # the smile
place(sfx, sparkle(0.03, 2093, 6), P['D5'] + 0.4)

# ---------------- S6: end card ----------------
E = P['end']
ping(E + 0.15, 0.05, 2093)
place(sfx, sparkle(0.04, 2093, 6), E + 0.3)
for i in range(3):
    place(sfx, thump(120 - i * 10, 0.22, 0.07), E + 0.4 + i * 0.08)
place(sfx, blip(600, 1000, 0.09, 0.12), E + 1.4); place(sfx, bell(1568, 0.9, 0.05), E + 1.42)
place(sfx, whoosh(0.8, 0.05, 500, 4000), E + 1.7)

# ---------------- narration ----------------
voice = np.zeros((N, 2))
segs = json.load(open(seg_path))
takes = {}
for sgm in segs:
    f = sgm['file']
    if f not in takes:
        v, sr = sf.read(f)
        if v.ndim > 1: v = v.mean(axis=1)
        assert sr == SR
        v = band(v, 70, 16000)
        act = v[np.abs(v) > 0.01]
        takes[f] = v / (np.sqrt(np.mean(act ** 2)) + 1e-9) * 0.16
for j, sgm in enumerate(segs):
    v = takes[sgm['file']]
    a, b = sgm['src']
    nxt = segs[j + 1]['src'][0] if j + 1 < len(segs) and segs[j + 1]['file'] == sgm['file'] else len(v) / SR
    i0, i1 = int(max(0, a - 0.08) * SR), int(min(b + 0.22, nxt - 0.06) * SR)
    piece = v[i0:i1].copy()
    nf, nfo = int(0.01 * SR), int(0.06 * SR)
    piece[:nf] *= np.linspace(0, 1, nf); piece[-nfo:] *= np.linspace(1, 0, nfo)
    place(voice, piece, sgm['on'] - (a - i0 / SR))

voice = 0.7 * np.tanh(voice / 0.7)   # soft-limit the odd plosive peak before mixing

# ---------------- music: level toward a target curve, duck under the voice ----------------
m = subprocess.run(['ffmpeg', '-v', 'error', '-i', music_path, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
mus = np.frombuffer(m, dtype=np.float32).reshape(-1, 2).astype(np.float64)
music = np.zeros((N, 2)); music[: min(N, len(mus))] = mus[:N]
mono = music.mean(axis=1)
lvl = 10 * np.log10(np.maximum(movavg(mono ** 2, int(1.2 * SR)), 0) + 1e-10)
t = np.arange(N) / SR
target = np.full(N, -24.0)


def ramp(a, b, val, edge=0.5):
    k = np.clip(np.minimum((t - a) / edge, (b - t) / edge), 0, 1)
    k = 0.5 - 0.5 * np.cos(np.pi * k)
    return k * (val - target)


target = target + ramp(P['title'] - 0.2, P['D0'] + 0.1, -17.0, 0.4) + ramp(P['end'] - 0.2, DUR + 1, -17.0, 0.5)
gain_db = np.clip(0.6 * (target - lvl), -14, 9)
gain_db = movavg(gain_db, int(0.3 * SR))
music *= (10 ** (gain_db / 20))[:, None]
vm = np.abs(voice.mean(axis=1))
envv = np.zeros(N); a_att, a_rel = np.exp(-1 / (0.06 * SR)), np.exp(-1 / (0.45 * SR)); e = 0.0
for i in range(0, N, 32):
    x = vm[i:i + 32].max()
    e = a_att * e + (1 - a_att) * x if x > e else a_rel ** 32 * e + (1 - a_rel ** 32) * x
    envv[i:i + 32] = e
# hold the duck for 0.4 s after each peak so soft word endings (e.g. the final "ตอบ") stay above the music
blk = envv[::32]; held = blk.copy()
for k in range(1, int(0.4 * SR / 32)):
    held[k:] = np.maximum(held[k:], blk[:-k])
envv = np.repeat(held, 32)[:N]
music *= (10 ** (-6.5 * np.clip(envv / 0.04, 0, 1) / 20))[:, None]

amb *= (10 ** (-4.0 * np.clip(envv / 0.04, 0, 1) / 20))[:, None]
mix = voice + music + 0.9 * sfx + amb
fadeo = np.ones(N); fo = int(0.45 * SR); fadeo[-fo:] = np.linspace(1, 0, fo)
mix *= fadeo[:, None]
np.save(out_path + '.stems.npy', np.stack([voice.mean(1), music.mean(1), sfx.mean(1), amb.mean(1)]).astype(np.float32))
sf.write(out_path + '.pre.wav', mix.astype(np.float32), SR, subtype='FLOAT')
print('pre-master peak', round(float(np.max(np.abs(mix))), 3))

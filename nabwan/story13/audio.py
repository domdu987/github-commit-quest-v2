# "15 ปีใหม่ ที่แม่อยู่บนรถทัวร์" soundtrack: Puck narration (1.2x) placed take by take, แม่'s midnight announcement in her
# own voice through a bus-PA filter (band-limited, a little drive, a short cabin echo), the ElevenLabs score (levelled, ducked
# under the voices, lifted for the title, the cheer and the end card), recorded sound effects from story13/sfx (bus cabin hum,
# passing bus, terminal, village night, fireworks near and far — muffled inside the bus —, the cheer, the mic, the PA chime,
# the LINE pop, the bottle, the horn) plus a few synthesised accents, all synced to story13/scenes.js.
# Usage (from the scratchpad root): python story13/audio.py story13/segments.json story13/music/music.mp3 <out>
import sys, json, subprocess
import numpy as np
import soundfile as sf

SR = 44100
seg_path, music_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
js = open('story13/vo.js').read()
P = json.loads(js[js.index('{'):js.rindex('}') + 1])['P']
DUR = P['DUR']
N = int(SR * DUR)
rng = np.random.default_rng(43)


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
SC = {'s0a': 0, 's0b': P['H2'] - 0.05, 's1': P['A0'] - 0.3, 's1b': P['A3'] - 0.1, 's2': P['B0'] - 0.3, 's3a': P['C0'] - 0.3, 's3b': P['C3'] - 0.1,
      's4': P['title'], 's5': P['D0'] - 0.1, 's5i': P['F2'] - 0.1, 's6': P['E0'] - 0.1, 's7': P['end']}
T = lambda k: SC[k]
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




def traffic(dur, vol):
    n = int(SR * dur); t = np.arange(n) / SR
    x = norm(band(rng.standard_normal(n), 60, 900))
    return vol * x * (0.7 + 0.3 * np.sin(2 * np.pi * 0.11 * t + 1))



def walk_steps(t0, t1, period, vol, pan=0.0):
    t = t0
    while t < t1:
        place(sfx, step(vol * rng.uniform(0.75, 1.0)), t, pan=pan)
        t += period * rng.uniform(0.94, 1.06)


# ---------------- recorded effects ----------------
FX = {}
def fx(name):
    if name not in FX:
        x, sr = sf.read(f'story13/sfx/{name}.wav')
        if x.ndim == 1: x = np.stack([x, x], 1)
        assert sr == SR
        FX[name] = x / (np.max(np.abs(x)) + 1e-9)
    return FX[name]


def muffle(x, hi=1400, lo=30):
    return np.stack([band(x[:, 0], lo, hi), band(x[:, 1], lo, hi)], 1)


def put(buf, name, at, gain, muff=None, start=0.0, dur=None):
    x = fx(name)
    i0 = int(start * SR); x = x[i0:] if dur is None else x[i0:i0 + int(dur * SR)]
    if muff: x = muffle(x, muff)
    x = x.copy(); nf = min(len(x) // 4, int(0.04 * SR)); x[:nf] *= np.linspace(0, 1, nf)[:, None]; x[-nf:] *= np.linspace(1, 0, nf)[:, None]
    place(buf, x, at, gain)


def loop_bed(buf, name, a, b, gain, muff=None, xf=0.6):
    """fill [a, b) by looping a recording with crossfades"""
    x = fx(name)
    if muff: x = muffle(x, muff)
    L_, k, t = len(x), int(xf * SR), a
    while t < b:
        seg = x[: min(L_, int((b - t + xf) * SR))].copy()
        ramp_in = np.linspace(0, 1, min(k, len(seg)))[:, None]; seg[:len(ramp_in)] *= ramp_in
        ramp_out = np.linspace(1, 0, min(k, len(seg)))[:, None]; seg[-len(ramp_out):] *= ramp_out
        place(buf, seg, t, gain)
        t += L_ / SR - xf


def pop_party(t, vol):
    place(sfx, thump(180, 0.06, vol), t); place(sfx, noise_burst(0.12, vol * 0.7, 1500, 8000, 0.6), t)
    place(sfx, sparkle(vol * 0.4, 2349, 4), t + 0.05)


# ---------------- beds ----------------
loop_bed(amb, 'night_village', 0, T('s0b') + 0.3, 0.05)                         # outside: the road at night
put(amb, 'bus_pass', 0.1, 0.32)
for a, b in [(T('s0b'), T('s1')), (T('s3b'), T('s4')), (T('s5'), T('s6'))]:        # inside the cabin
    loop_bed(amb, 'bus_hum', a - 0.1, b + 0.2, 0.18)
loop_bed(amb, 'bus_hum', T('s4'), T('s5'), 0.07)
loop_bed(amb, 'terminal', T('s1') - 0.1, T('s1b') + 0.15, 0.16)
loop_bed(amb, 'terminal', T('s3a') - 0.2, T('s3b') + 0.15, 0.15)
put(amb, 'bus_pass', T('s1b') - 0.2, 0.34); put(sfx, 'horn', T('s1b') + 0.35, 0.18)
loop_bed(amb, 'night_village', T('s2') - 0.2, T('s3a') + 0.3, 0.07)
loop_bed(amb, 'bus_hum', T('s5i'), T('s6'), 0.10, muff=900)
loop_bed(amb, 'night_village', T('s6') - 0.1, DUR - 2.4, 0.04)
put(amb, 'bus_pass', T('s6') + 0.2, 0.26)

# ---------------- S0: hook ----------------
for k, tf in enumerate([0.15, 0.55, 1.4, 2.0]):
    put(sfx, 'fw_far', tf, 0.10 + 0.03 * (k % 2), start=0.2 + 0.5 * k, dur=1.6)
put(sfx, 'bottle', T('s0b') + 0.5, 0.22); put(sfx, 'snackbox', T('s0b') + 0.9, 0.12)
for k in range(3): put(sfx, 'fw_far', P['H3'] - 0.2 + k * 0.6, 0.06, muff=1600, start=1.0 + k * 0.6, dur=1.2)   # clear of "สังเกต"
place(sfx, sparkle(0.03, 1760, 7), P['Hend'] + 0.05)

# ---------------- S1: the terminal, fifteen New Year's Eves ----------------
place(sfx, whoosh(0.5, 0.04, 300, 2200), T('s1') - 0.25)
walk_steps(T('s1') + 0.1, P['A1'] + 0.25, 0.42, 0.022)
place(sfx, whoosh(0.5, 0.045, 400, 3000), P['A1'] - 0.05)
ticks_roll(P['A1'] + 0.35, P['A3'] - 0.2, 14, 0.018, 2600)                     # 2555 → 2569
place(sfx, ding(0.04), P['A3'] - 0.2)

# ---------------- S2: home, the countdown, the LINE from แม่ ----------------
tMid2 = P['B2'] + 0.05
place(sfx, whoosh(0.7, 0.05, 200, 1800), T('s2') - 0.3)
put(amb, 'tv_count', T('s2') + 0.1, 0.06, muff=3000, dur=tMid2 - T('s2'))
for k in range(int(tMid2 - T('s2') - 0.4)): place(sfx, tick(0.02, 1800), tMid2 - 1 - k)
put(sfx, 'fw_far', tMid2, 0.16, dur=3.5); put(sfx, 'tv_count', tMid2, 0.10, muff=3500, start=3.0, dur=3.0)
place(sfx, bell(1047, 1.2, 0.03), tMid2)
put(sfx, 'phone_buzz', P['B3'] + 0.08, 0.28); put(sfx, 'msg_pop', P['B3'] + 0.15, 0.22)
place(sfx, sparkle(0.02, 2093, 4), P['B5'] + 0.6)

# ---------------- S3a: the secret seat ----------------
place(sfx, fade(bell(784, 1.6, 0.02), 0.3, 1.0), T('s3a'))
place(sfx, whoosh(0.5, 0.035, 400, 3000), P['C1'] - 0.35); put(sfx, 'ticket', P['C1'] - 0.3, 0.1)
t = P['C1'] + 0.35
while t < P['C1'] + 0.75: place(sfx, fade(noise_burst(0.06, 0.005, 2500, 9000, 0.9), 0.01, 0.03), t); t += 0.07   # red marker
place(sfx, thump(90, 0.12, 0.04), P['C1'] + 0.75); place(sfx, noise_burst(0.06, 0.01, 1000, 5000), P['C1'] + 0.75)   # stamp
walk_steps(P['C2'] - 0.05, T('s3b') - 0.1, 0.42, 0.02, pan=0.4)

# ---------------- S3b: the aisle, the reveal, the freeze ----------------
tTwo, tOff, tFreeze = P['C4'] - 0.1, P['C4'] + 0.25, P['C5'] - 0.1
put(sfx, 'steps_carpet', T('s3b'), 0.22, dur=tTwo - T('s3b') + 0.1)
put(sfx, 'bottle', T('s3b') + 0.35, 0.18)
put(sfx, 'whoosh', tOff, 0.3); place(sfx, sparkle(0.03, 2093, 5), tOff + 0.3)
put(sfx, 'heartbeat', tFreeze, 0.5)
place(sfx, whoosh(0.25, 0.05, 600, 4000), tFreeze)                                # crash zoom
put(sfx, 'bottle', tFreeze + 0.45, 0.2); place(sfx, thump(150, 0.08, 0.05), tFreeze + 0.46); place(sfx, thump(170, 0.06, 0.03), tFreeze + 0.62)

# ---------------- S4: title ----------------
place(sfx, whoosh(0.8, 0.055, 300, 2000), T('s4') - 0.6)
put(sfx, 'sparkle', T('s4') + 0.1, 0.25)
for i in range(15): place(sfx, blip(800 + 30 * i, 1200 + 30 * i, 0.04, 0.012), T('s4') + 0.05 + (14 - i) * 0.055)
for i in range(2): place(sfx, thump(110 - i * 8, 0.22, 0.07), T('s4') + 0.3 + i * 0.07)
place(sfx, bell(1319, 1.4, 0.045), T('s4') + 1.0)

# ---------------- S5: midnight on the bus ----------------
tMid = P['D0'] + 0.25
for k in range(3): place(sfx, tick(0.03, 2400), tMid - 0.2 - (2 - k) * 0.3)
put(sfx, 'fw_near', tMid, 0.24, muff=1500, dur=2.2)
for k in range(9): put(sfx, 'fw_far', tMid + 1.2 + k * 1.3, 0.07, muff=1500, start=(k * 0.9) % 4, dur=1.8)
put(sfx, 'cheer', tMid + 0.1, 0.05, dur=1.0)
put(sfx, 'mic_on', P['Dend'] + 0.03, 0.2)                                      # after "ไมค์ ... เหมือนทุกปี"
put(sfx, 'pa_chime', P['Dend'] + 0.12, 0.18)
tCheer = P['Mend'] + 0.15
put(sfx, 'cheer', tCheer, 0.42); put(sfx, 'clap', tCheer + 0.4, 0.3)
for k in range(5): pop_party(tCheer + 0.05 + k * 0.13, 0.05)
put(sfx, 'fw_near', tCheer + 0.4, 0.18, muff=1800)
place(sfx, fade(bell(659, 2.4, 0.025), 0.2, 1.6), P['F0'] - 0.1)

# ---------------- S5i, S6: the window, the road ----------------
for k in range(3): put(sfx, 'fw_far', T('s5i') + k * 0.8, 0.12, muff=1200, start=k * 1.1, dur=1.6)
put(sfx, 'fw_near', T('s6') + 0.3, 0.2, dur=5.5)
put(sfx, 'fw_far', T('s6') + 2.4, 0.16, dur=4.0)
place(sfx, fade(glide(1200, 2400, 0.9, 0.01), 0.1, 0.5), P['E1'])
put(sfx, 'horn', P['Eend'] + 0.15, 0.2)

# ---------------- S7: end card ----------------
E = P['end']
ping(E + 0.15, 0.05, 2093)
place(sfx, sparkle(0.04, 2093, 6), E + 0.3)
for i in range(3): place(sfx, thump(120 - i * 10, 0.22, 0.07), E + 0.4 + i * 0.08)
place(sfx, blip(600, 1000, 0.09, 0.12), E + 1.4); place(sfx, bell(1568, 0.9, 0.05), E + 1.42)
place(sfx, whoosh(0.8, 0.05, 500, 4000), E + 1.7)
put(sfx, 'fw_far', E + 0.2, 0.08, dur=2.6)

# ---------------- voices ----------------
def pa(v):
    """the bus PA: band-limited, a touch of drive, a short metallic cabin echo"""
    x = band(v, 170, 6500)
    x = np.tanh(x * 1.3) / 1.3
    ir = np.zeros(int(0.3 * SR)); ir[0] = 1.0
    for d, g in [(0.029, 0.16), (0.053, 0.11), (0.09, 0.07), (0.15, 0.04)]: ir[int(d * SR)] += g
    y = np.convolve(x, ir)[:len(x)]
    return band(y, 160, 7000)   # gentle: Whisper must still read every word


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
        if sgm['name'] == 'M': v = pa(v)
        act = v[np.abs(v) > 0.01]
        takes[f] = v / (np.sqrt(np.mean(act ** 2)) + 1e-9) * (0.15 if sgm['name'] == 'M' else 0.16)
for j, sgm in enumerate(segs):
    v = takes[sgm['file']]
    a, b = sgm['src']
    nxt = segs[j + 1]['src'][0] if j + 1 < len(segs) and segs[j + 1]['file'] == sgm['file'] else len(v) / SR
    i0, i1 = int(max(0, a - 0.08) * SR), int(min(b + (0.4 if sgm['name'] == 'M' else 0.22), nxt - 0.06) * SR)
    piece = v[i0:i1].copy()
    nf, nfo = int(0.01 * SR), int(0.06 * SR)
    piece[:nf] *= np.linspace(0, 1, nf); piece[-nfo:] *= np.linspace(1, 0, nfo)
    place(voice, piece, sgm['on'] - (a - i0 / SR), pan=0.0)

voice = 0.7 * np.tanh(voice / 0.7)

# ---------------- music: level toward a target curve, duck under the voices ----------------
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


target = target + ramp(P['title'] - 0.2, P['D0'] + 0.1, -17.0, 0.4) + ramp(P['Mend'] + 0.2, P['F0'] - 0.1, -18.0, 0.35) + ramp(P['end'] - 0.2, DUR + 1, -17.0, 0.5)
target = target + ramp(P['H5'] - 0.15, P['Hend'] + 0.1, -29.0, 0.2) + ramp(P['C1'] - 0.15, P['C2'] + 0.4, -29.0, 0.2) + ramp(P['M0'] - 0.15, P['Mend'] + 0.1, -28.0, 0.3) + ramp(P['D1'] - 0.15, P['D2'] + 0.3, -29.0, 0.2)   # words Whisper lost under the music
gain_db = np.clip(0.6 * (target - lvl), -14, 9)
gain_db = movavg(gain_db, int(0.3 * SR))
music *= (10 ** (gain_db / 20))[:, None]
vm = np.abs(voice.mean(axis=1))
envv = np.zeros(N); a_att, a_rel = np.exp(-1 / (0.06 * SR)), np.exp(-1 / (0.45 * SR)); e = 0.0
for i in range(0, N, 32):
    x = vm[i:i + 32].max()
    e = a_att * e + (1 - a_att) * x if x > e else a_rel ** 32 * e + (1 - a_rel ** 32) * x
    envv[i:i + 32] = e
blk = envv[::32]; held = blk.copy()
for k in range(1, int(0.4 * SR / 32)):
    held[k:] = np.maximum(held[k:], blk[:-k])
envv = np.repeat(held, 32)[:N]
duck = np.clip(envv / 0.04, 0, 1)
music *= (10 ** (-6.5 * duck / 20))[:, None]
amb *= (10 ** (-4.0 * duck / 20))[:, None]
sfx *= (10 ** (-3.0 * duck / 20))[:, None]
mix = voice + music + 0.9 * sfx + amb
fadeo = np.ones(N); fo = int(0.45 * SR); fadeo[-fo:] = np.linspace(1, 0, fo)
mix *= fadeo[:, None]
np.save(out_path + '.stems.npy', np.stack([voice.mean(1), music.mean(1), sfx.mean(1), amb.mean(1)]).astype(np.float32))
sf.write(out_path + '.pre.wav', mix.astype(np.float32), SR, subtype='FLOAT')
print('pre-master peak', round(float(np.max(np.abs(mix))), 3))

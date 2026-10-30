# "720 มื้อ ที่ครูซื้อเกิน" soundtrack: Puck narration (1.2x) placed take by take, ครูสมศรี's own line (a female voice, a
# light classroom room tone), the ElevenLabs score (levelled, ducked under the voices, lifted for the title and the end card,
# dipped under the narrator's own "ครูซื้อมาเกิน"), recorded effects from story14/sfx (the quiet classroom with its fan, the
# schoolyard, cicadas, the canteen, the bell, footsteps on wood and tile, plastic food bags, the chair, the spoon, chalk,
# the sip, a small stomach growl) — the past a little band-limited like a memory — all synced to story14/scenes.js.
# Usage (from the scratchpad root): python story14/audio.py story14/segments.json story14/music/music.mp3 <out>
import sys, json, subprocess
import numpy as np
import soundfile as sf

SR = 44100
seg_path, music_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
js = open('story14/vo.js').read()
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
SC = {'s0': 0, 's1': P['A0'] - 0.3, 's2': P['B0'] - 0.3, 's3': P['C0'] - 0.3, 's4': P['title'], 's5': P['D0'] - 0.1, 's6': P['E0'] - 0.1,
      's7': P['F0'] - 0.3, 's8': P['end']}
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
        x, sr = sf.read(f'story14/sfx/{name}.wav')
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
loop_bed(amb, 'classroom_quiet', 0, T('s1') + 0.2, 0.10)                         # today: fan, kids far off
loop_bed(amb, 'kids_lunch', 0, T('s1') + 0.2, 0.05, muff=3000)
for a, b in [(T('s1'), T('s4'))]:                                                  # the past, like a memory
    loop_bed(amb, 'classroom_quiet', a - 0.1, b + 0.2, 0.10, muff=5000)
    loop_bed(amb, 'cicadas', a - 0.1, b + 0.2, 0.05, muff=6000)
    loop_bed(amb, 'schoolyard', a - 0.1, b + 0.2, 0.05, muff=4000)
loop_bed(amb, 'classroom_quiet', T('s4'), T('s5'), 0.05)
loop_bed(amb, 'classroom_quiet', T('s5') - 0.1, T('s8') + 0.3, 0.09)
loop_bed(amb, 'birds_morning', T('s5'), T('s6'), 0.05)
loop_bed(amb, 'kids_lunch', P['D1'] + 0.2, T('s7'), 0.06, muff=2500)
loop_bed(amb, 'schoolyard', T('s7'), T('s8') + 0.2, 0.04, muff=3500)

# ---------------- S0: today, the hook ----------------
tPut0, tSit0 = P['H2'] + 0.2, P['H3'] + 0.3
put(sfx, 'steps_tile', 0.25, 0.18, dur=tPut0 - 0.4)
put(sfx, 'bag_rustle', tPut0 - 0.05, 0.22)
put(sfx, 'chair', P['Hend'] + 0.05, 0.12)
place(sfx, sparkle(0.03, 1760, 7), P['Hend'] + 0.15)

# ---------------- S1: the boy alone ----------------
place(sfx, whoosh(0.7, 0.05, 200, 1800), T('s1') - 0.3)
put(sfx, 'sip', P['A3'] - 0.1 + 0.15, 0.16, muff=5000)
put(sfx, 'tummy', P['Aend'] + 0.05, 0.22)

# ---------------- S2: ครูสมศรี walks in ----------------
tPut2, tSit2 = P['T0'] - 0.05, P['T1'] - 0.1
put(sfx, 'steps_wood', T('s2') + 0.2, 0.2, dur=P['B2'] - T('s2'), muff=6000)
put(sfx, 'bag_rustle', P['Bend'] + 0.02, 0.22, muff=6000)                          # set down after "ถุง"
put(sfx, 'chair', P['Tend'] + 0.05, 0.12, muff=6000)

# ---------------- S3: three years of lunches ----------------
for k in range(int((P['C3'] - T('s3')) * 4)):
    tk = T('s3') + 0.3 + k * 0.25
    if tk > P['C3'] - 0.2: break
    put(sfx, 'spoon', tk, 0.05, muff=5000, dur=0.4)
ticks_roll(T('s3') + 0.4, P['C3'] - 0.4, 24, 0.012, 2600)                         # 1 → 720
for k in range(2): put(sfx, 'page_flip', P['C2'] - 0.1 + k * 0.7, 0.12)            # ป.4 → ป.5 → ป.6
put(sfx, 'chalk', P['C2'] + 0.1, 0.08, muff=6000, dur=1.4)
place(sfx, ding(0.035), P['C3'] - 0.25)

# ---------------- S4: title ----------------
place(sfx, whoosh(0.8, 0.055, 300, 2000), T('s4') - 0.6)
put(sfx, 'sparkle', T('s4') + 0.1, 0.25)
for i in range(3): place(sfx, thump(110 - i * 8, 0.22, 0.07), T('s4') + 0.3 + i * 0.07)
place(sfx, bell(1319, 1.4, 0.045), T('s4') + 1.05)

# ---------------- S5: today, the bell, the girl ----------------
put(sfx, 'school_bell', P['D1'] - 0.15, 0.06, muff=2500, dur=1.6)
put(sfx, 'steps_tile', P['D1'] + 0.3, 0.07, dur=1.6)
put(sfx, 'sip', P['D3'] - 0.1 + 0.4, 0.14)
place(sfx, fade(bell(659, 2.2, 0.018), 0.2, 1.6), P['D3'])                          # memory
put(sfx, 'heartbeat', P['Dend'] + 0.05, 0.25)

# ---------------- S6: two bags, the same words ----------------
tPut6, tSit6 = P['E1'] - 0.05, P['G1'] - 0.1
put(sfx, 'steps_tile', T('s6') + 0.2, 0.18, dur=tPut6 - T('s6') - 0.3)
put(sfx, 'bag_rustle', P['Eend'] + 0.02, 0.2)
put(sfx, 'chair', P['Gend'] + 0.05, 0.1)
put(sfx, 'rubber_band', P['Gend'] + 0.5, 0.18)
place(sfx, sparkle(0.03, 2093, 6), P['Gend'] + 0.3)

# ---------------- S7: the split screen ----------------
for k in range(5): put(sfx, 'spoon', T('s7') + 0.5 + k * 0.8, 0.04, dur=0.4)
place(sfx, whoosh(0.6, 0.04, 400, 3000), P['F2'] - 0.4)
place(sfx, fade(bell(784, 2.4, 0.025), 0.2, 1.6), P['Fend'] + 0.1)

# ---------------- S8: end card ----------------
E = P['end']
ping(E + 0.15, 0.05, 2093)
place(sfx, sparkle(0.04, 2093, 6), E + 0.3)
for i in range(3): place(sfx, thump(120 - i * 10, 0.22, 0.07), E + 0.4 + i * 0.08)
place(sfx, blip(600, 1000, 0.09, 0.12), E + 1.4); place(sfx, bell(1568, 0.9, 0.05), E + 1.42)
place(sfx, whoosh(0.8, 0.05, 500, 4000), E + 1.7)

# ---------------- voices ----------------
def room(v):
    """ครูสมศรี in the old classroom: a soft early reflection, nothing that blurs the words"""
    ir = np.zeros(int(0.2 * SR)); ir[0] = 1.0
    for d, g in [(0.019, 0.12), (0.037, 0.08), (0.061, 0.05)]: ir[int(d * SR)] += g
    return np.convolve(v, ir)[:len(v)]


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
        if sgm['name'] == 'T': v = room(v)
        act = v[np.abs(v) > 0.01]
        takes[f] = v / (np.sqrt(np.mean(act ** 2)) + 1e-9) * (0.15 if sgm['name'] == 'T' else 0.16)
for j, sgm in enumerate(segs):
    v = takes[sgm['file']]
    a, b = sgm['src']
    nxt = segs[j + 1]['src'][0] if j + 1 < len(segs) and segs[j + 1]['file'] == sgm['file'] else len(v) / SR
    i0, i1 = int(max(0, a - 0.08) * SR), int(min(b + 0.22, nxt - 0.06) * SR)
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


target = target + ramp(P['title'] - 0.2, P['D0'] + 0.1, -17.0, 0.4) + ramp(P['end'] - 0.2, DUR + 1, -17.0, 0.5)
target = target + ramp(P['G0'] - 0.15, P['Gend'] + 0.15, -28.0, 0.25) + ramp(P['T0'] - 0.15, P['Tend'] + 0.15, -27.0, 0.25)   # the two "ครูซื้อมาเกิน" lines
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

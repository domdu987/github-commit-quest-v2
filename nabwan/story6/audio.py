# "4,380 วันที่รอ" soundtrack: Puck narration (1.2x) placed take by take, the ElevenLabs score (levelled, ducked under the
# voice, lifted for the title and end card), ambience beds and UI/action sounds synced to story6/scenes.js.
# Usage (from the scratchpad root): python story6/audio.py story6/segments.json story6/music/music.mp3 <out>
import sys, json, subprocess
import numpy as np
import soundfile as sf

SR = 44100
seg_path, music_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
js = open('story6/vo.js').read()
P = json.loads(js[js.index('{'):js.rindex('}') + 1])['P']
DUR = P['DUR']
N = int(SR * DUR)
rng = np.random.default_rng(23)


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
SC = {'s0a': 0, 's0b': P['H2'] - 0.15, 's1': P['A0'] - 0.3, 's2': P['B0'] - 0.3, 's3': P['Cst'] - 0.3, 's4': P['C5'] - 0.15, 's5': P['title'],
      's6': P['D0'] - 0.1, 's7': P['D5'] - 0.15, 's8': P['D7'] - 0.15, 's9': P['end']}


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


# ---------------- ambience beds ----------------
s = SC
place(amb, fade(bed(s['s0b'] + 0.1, 60, 400, 0.012, 0.15, 0.3), 0.3, 0.1), 0.0)                    # office: AC + computer hum
typing_clicks(0.2, s['s0b'] - 0.1, 9, 0.03)
place(amb, fade(bed(s['s1'] - s['s0b'] + 0.1, 120, 900, 0.006), 0.2, 0.2), s['s0b'])                # quiet night at the door
place(amb, fade(crickets(s['s1'] - s['s0b'] + 0.1, 0.006), 0.2, 0.2), s['s0b'])
place(amb, fade(bed(s['s2'] - s['s1'] + 0.1, 120, 900, 0.007), 0.2, 0.3), s['s1'])                 # the entrance, evening into night
birds(s['s1'], (P['A6'] - s['s1']), 0.012, 1.2)
place(amb, fade(crickets(s['s2'] - P['A6'], 0.008), 0.6, 0.3), P['A6'])
for k in range(int((s['s2'] - s['s1']) / 1.0)):
    place(amb, tick(0.018, 1400), s['s1'] + 0.4 + k)                                                 # wall clock
place(amb, fade(bed(s['s3'] - s['s2'] + 0.1, 150, 1200, 0.008, 0.3, 0.6), 0.3, 0.3), s['s2'])       # living room: TV murmur
place(amb, fade(crickets(s['s3'] - s['s2'], 0.005), 0.3, 0.3), s['s2'])
place(amb, fade(bed(s['s4'] - s['s3'] + 0.1, 60, 400, 0.012, 0.1, 0.3), 0.3, 0.3), s['s3'])        # clinic: AC hum
place(amb, fade(bed(s['s5'] - s['s4'], 120, 900, 0.006), 0.3, 0.4), s['s4'])
place(amb, fade(crickets(s['s5'] - s['s4'], 0.005), 0.3, 0.4), s['s4'])
place(amb, fade(bed(s['s7'] - s['s6'] + 0.1, 120, 900, 0.007), 0.3, 0.3), s['s6'])                 # six o'clock, sunset
birds(s['s6'], s['s7'] - s['s6'], 0.014, 1.4)
place(amb, fade(bed(s['s9'] - s['s7'], 120, 900, 0.006), 0.3, 0.5), s['s7'])

# ---------------- S0: the hook ----------------
place(sfx, whoosh(0.3, 0.06, 500, 3500), 0.1)                                                      # clock card
place(sfx, whoosh(0.5, 0.07, 300, 3000), s['s0b'] - 0.25)
place(sfx, fade(noise_burst(0.7, 0.03, 2000, 9000, 1.2), 0.3, 0.3), s['s0b'] + 0.05)                # spotlight
place(sfx, thump(60, 0.4, 0.10), s['s0b'] + 0.15)
jingle(P['H3'] + 0.1, 0.025)                                                                       # his tag jingles
place(sfx, blip(500, 1000, 0.12, 0.08), P['H5'] - 0.05); place(sfx, bell(988, 1.0, 0.05), P['H5'])

# ---------------- S1: six o'clock, waiting ----------------
place(sfx, whoosh(0.3, 0.06, 500, 3500), P['A0'] - 0.1); chime(P['A1'], 0.05, (1047, 1568))        # 18:00
place(sfx, glide(500, 1300, 0.18, 0.06), P['A4'] - 0.05)                                          # ears pop up
for k in range(3):
    place(sfx, thump(140, 0.06, 0.05), P['A4'] + k * 0.12)                                         # little hops
wag_thumps(P['A5'] - 0.1, P['A6'] + 0.6, 0.045)
place(sfx, blip(600, 900, 0.07, 0.10), P['A6'] - 0.1)                                            # wait chip
ticks_roll(P['A6'], P['A9'], 26, 0.025, 2400)                                                      # the hours go by
for tb in (P['A7'], P['A8']):
    place(sfx, bell(880, 0.9, 0.04), tb + 0.05)
place(sfx, noise_burst(0.6, 0.04, 200, 1400, 1.0), P['A9'] + 0.1); place(sfx, thump(90, 0.15, 0.06), P['A9'] + 0.3)   # lies down with a sigh

# ---------------- S2: one pat, then the phone ----------------
jingle(s['s2'] + 0.05, 0.04)                                                                       # keys
place(sfx, noise_burst(0.25, 0.04, 800, 4000, 1.0), P['B2'] - 0.05)                               # the pat
place(sfx, blip(600, 1000, 0.08, 0.08), P['B2'] + 0.35); place(sfx, blip(520, 860, 0.08, 0.08), P['B3'] + 0.3)   # chips
typing_clicks(P['B3'] + 0.3, s['s3'] - 0.3, 5, 0.018)                                               # scrolling
place(sfx, thump(90, 0.15, 0.06), P['B4'])                                                         # he lies down at her feet
place(sfx, fade(glide(900, 720, 0.6, 0.012), 0.1, 0.3), P['B6'] + 0.3)                              # a tiny whine

# ---------------- S3: the vet ----------------
place(sfx, whoosh(0.35, 0.07, 400, 3000), P['C1'] - 0.25)
place(sfx, noise_burst(0.3, 0.035, 2000, 7000, 0.7), P['C3'] - 0.05)
place(sfx, noise_burst(0.4, 0.035, 2000, 7000, 0.7), P['C4'])
heartbeat(P['C4'] + 0.3, s['s4'] - 0.1, 0.06, 0.9)

# ---------------- S4: 4,380 days ----------------
place(sfx, whoosh(0.4, 0.07, 300, 3000), s['s4'] + 0.0)
for i in range(5):
    place(sfx, blip(600 + 80 * i, 900 + 80 * i, 0.06, 0.07), P['C6'] - 0.1 + i * 0.12)
ticks_roll(P['C7'] - 0.15, P['C7'] + 0.95, 20, 0.03)
place(sfx, thump(90, 0.3, 0.12), P['C7'] + 0.97); place(sfx, bell(1047, 1.2, 0.06), P['C7'] + 0.99)
for k in range(14):
    place(sfx, tick(0.02, 2400 + 60 * k), P['C8'] - 0.05 + k * 0.08)                               # the waffle fills
place(sfx, whoosh(0.5, 0.05, 300, 2500), P['C9'] - 0.35); jingle(P['C9'] + 0.3, 0.03)

# ---------------- S5: title ----------------
place(sfx, whoosh(0.8, 0.06, 300, 2000), s['s5'] - 0.6)
place(sfx, fade(noise_burst(0.8, 0.04, 2000, 9000, 1.2), 0.4, 0.3), s['s5'] - 0.3)
for i in range(5):
    place(sfx, thump(120 - i * 6, 0.22, 0.08), s['s5'] + 0.15 + i * 0.07)
place(sfx, noise_burst(0.5, 0.025, 3000, 8000), s['s5'] + 0.65); place(sfx, bell(1319, 1.2, 0.05), s['s5'] + 0.9)

# ---------------- S6: home at six ----------------
place(sfx, whoosh(0.3, 0.06, 500, 3500), s['s6'] + 0.05)
place(sfx, tick(0.08, 1600), P['D1'] - 0.35); place(sfx, tick(0.06, 1200), P['D1'] - 0.3)          # key in the lock
place(sfx, fade(glide(180, 140, 0.6, 0.03), 0.05, 0.3), P['D1'] - 0.25)                            # door swings
chime(P['D1'] + 0.1, 0.05, (1319, 1760))                                                           # "ตรงเวลา"
paws(P['D2'] - 0.2, P['D3'], 0.05, 10)
place(sfx, whoosh(0.4, 0.09, 400, 4000), P['D3'])                                                  # the leap
place(sfx, thump(70, 0.35, 0.16), P['D4'] + 0.05); place(sfx, noise_burst(0.15, 0.08, 300, 3000), P['D4'] + 0.05)   # both go down
place(sfx, noise_burst(0.12, 0.10, 1500, 9000, 0.5), P['D4'] + 0.05); place(sfx, sparkle(0.05, 2093, 9), P['D4'] + 0.1)
jingle(P['D4'] + 0.2, 0.04); wag_thumps(P['D4'] + 0.3, s['s7'] - 0.1, 0.04, 0.25)

# ---------------- S7: our life vs his ----------------
for i in range(6):
    place(sfx, blip(700 + 60 * i, 1100 + 60 * i, 0.06, 0.06), s['s7'] + 0.1 + i * 0.1)
place(sfx, thump(150, 0.15, 0.08), P['D6'] + 0.1); place(sfx, sparkle(0.04, 1760, 6), P['D6'] + 0.15)
for k in range(3):
    place(sfx, thump(55, 0.16, 0.06), P['D6'] + 0.5 + k * 0.6); place(sfx, thump(50, 0.18, 0.045), P['D6'] + 0.68 + k * 0.6)

# ---------------- S8: the hug ----------------
place(sfx, whoosh(0.5, 0.06, 300, 2500), s['s8'] - 0.2)
for k in range(5):
    place(sfx, bell(2349 + 200 * (k % 3), 0.4, 0.025), s['s8'] + 0.3 + k * 0.3)
place(sfx, fade(noise_burst(1.0, 0.04, 2000, 9000, 1.2), 0.5, 0.4), P['end'] - 0.5)

# ---------------- S9: end card ----------------
E = P['end']
ping(E + 0.15, 0.05, 2093)
place(sfx, sparkle(0.04, 2093, 6), E + 0.3)
for i in range(3):
    place(sfx, thump(120 - i * 10, 0.22, 0.08), E + 0.4 + i * 0.08)
place(sfx, noise_burst(0.5, 0.02, 3000, 8000), E + 0.85)
place(sfx, blip(560, 840, 0.07, 0.08), E + 1.1)
place(sfx, blip(600, 1000, 0.09, 0.14), E + 1.4); place(sfx, bell(1568, 0.9, 0.05), E + 1.42)
place(sfx, whoosh(0.8, 0.06, 500, 4000), E + 1.7)

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


target = target + ramp(P['title'] - 0.2, P['D0'] + 0.1, -17.0, 0.4) + ramp(P['D3'], P['D5'] - 0.2, -21.0, 0.3) + ramp(P['end'] - 0.2, DUR + 1, -17.0, 0.5)
gain_db = np.clip(0.6 * (target - lvl), -14, 9)
gain_db = movavg(gain_db, int(0.3 * SR))
music *= (10 ** (gain_db / 20))[:, None]
vm = np.abs(voice.mean(axis=1))
envv = np.zeros(N); a_att, a_rel = np.exp(-1 / (0.06 * SR)), np.exp(-1 / (0.45 * SR)); e = 0.0
for i in range(0, N, 32):
    x = vm[i:i + 32].max()
    e = a_att * e + (1 - a_att) * x if x > e else a_rel ** 32 * e + (1 - a_rel ** 32) * x
    envv[i:i + 32] = e
music *= (10 ** (-6.5 * np.clip(envv / 0.04, 0, 1) / 20))[:, None]

mix = voice + music + 0.9 * sfx + amb
fadeo = np.ones(N); fo = int(0.45 * SR); fadeo[-fo:] = np.linspace(1, 0, fo)
mix *= fadeo[:, None]
np.save(out_path + '.stems.npy', np.stack([voice.mean(1), music.mean(1), sfx.mean(1), amb.mean(1)]).astype(np.float32))
sf.write(out_path + '.pre.wav', mix.astype(np.float32), SR, subtype='FLOAT')
print('pre-master peak', round(float(np.max(np.abs(mix))), 3))

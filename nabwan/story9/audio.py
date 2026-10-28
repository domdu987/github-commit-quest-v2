# "39 บาทที่แม่ไม่กล้ากด" soundtrack: Puck narration (1.2x) placed take by take, the ElevenLabs score (levelled, ducked under the
# voice, lifted for the title and end card), ambience beds and UI/action sounds synced to story9/scenes.js.
# Usage (from the scratchpad root): python story9/audio.py story9/segments.json story9/music/music.mp3 <out>
import sys, json, subprocess
import numpy as np
import soundfile as sf

SR = 44100
seg_path, music_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
js = open('story9/vo.js').read()
P = json.loads(js[js.index('{'):js.rindex('}') + 1])['P']
DUR = P['DUR']
N = int(SR * DUR)
rng = np.random.default_rng(37)


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
SC = {'s0': 0, 's1': P['A0'] - 0.3, 's2': P['B0'] - 0.3, 's3': P['C0'] - 0.3, 's4': P['title'], 's5': P['D0'] - 0.1, 's6': P['D3'] - 0.05, 's7': P['end']}


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


s = SC
# ---------------- ambience beds ----------------
place(amb, fade(bed(s['s2'] + 0.1, 80, 600, 0.008, 0.1, 0.2), 0.3, 0.2), 0.0)                      # her room at night
place(amb, fade(crickets(s['s2'] + 0.1, 0.005), 0.3, 0.2), 0.0)
place(amb, fade(bed(s['s7'] - s['s2'] + 0.2, 60, 400, 0.010, 0.1, 0.3), 0.3, 0.4), s['s2'])        # mom's room: tube-light hum
place(amb, fade(crickets(s['s6'] - s['s2'], 0.006), 0.3, 0.3), s['s2'])
for k in range(int((s['s6'] - s['s2']) / 1.0)):
    place(amb, tick(0.016, 1400), s['s2'] + 0.4 + k)                                                 # wall clock
birds(s['s6'], s['s7'] - s['s6'], 0.012, 1.2)                                                     # three days later, daytime

# ---------------- S0: the hook ----------------
place(sfx, whoosh(0.3, 0.06, 500, 3500), 0.05)
for k in range(12):
    place(sfx, blip(800 + 40 * k, 1200 + 40 * k, 0.05, 0.045), P['H0'] + 0.15 + k * 0.13)        # add-to-cart pops
place(sfx, whoosh(0.35, 0.06, 400, 3000), P['H2'] - 0.1)
place(sfx, blip(520, 860, 0.08, 0.07), P['H2'] + 0.3)
place(sfx, blip(600, 950, 0.08, 0.08), P['H4'] + 0.05)
for k in range(5):
    place(sfx, tick(0.025, 2200 + 80 * k), P['H4'] + 0.1 + k * 0.09)

# ---------------- S1: 11.11 at midnight ----------------
place(sfx, sparkle(0.05, 2093, 9), P['A0']); place(sfx, thump(90, 0.25, 0.10), P['A0'] + 0.02)     # 11.11 badge
place(sfx, whoosh(0.35, 0.06, 500, 3500), P['A1'] - 0.2)
for tt_ in [P['A3'], P['A3'] + 0.45, P['A3'] + 0.9, P['A2'] - 0.25, P['A2'] + 0.15, P['A2'] + 0.55]:
    place(sfx, blip(900, 1400, 0.06, 0.06), tt_); place(sfx, tick(0.03, 2600), tt_ + 0.04)
ticks_roll(P['A2'] - 0.3, P['A2'] + 0.7, 12, 0.025, 2600)
cash(P['A2'] + 0.72, 0.05)
place(sfx, whoosh(0.3, 0.05, 400, 2500), P['A5'] - 0.3)
notif_pop(P['A5'], 0.07, 1319); place(sfx, buzz(0.3, 0.02), P['A5'] - 0.02)                        # LINE from mom

# ---------------- S2: mom's cart ----------------
place(sfx, whoosh(0.5, 0.06, 300, 2500), s['s2'] - 0.2)
place(sfx, blip(560, 900, 0.08, 0.07), P['B0'] + 0.05)
place(sfx, bell(1760, 0.8, 0.045), P['B1'] + 0.2)
place(sfx, fade(noise_burst(0.45, 0.03, 2000, 8000, 1.0), 0.05, 0.2), P['B3'] + 0.3)               # marker circling the date
for k in range(4):
    place(sfx, step(0.035), s['s2'] + 0.12 + k * 0.33, pan=-0.5 + k * 0.12)                      # ฝ้าย walks in
place(sfx, thump(110, 0.12, 0.05), s['s2'] + 1.6); place(sfx, noise_burst(0.12, 0.02, 400, 3000), s['s2'] + 1.6)   # sits on the mat
place(sfx, tick(0.04, 2000), s['s2'] + 1.65)                                                     # takes mom's phone
place(sfx, thump(70, 0.3, 0.14), P['B5'] + 0.05); place(sfx, noise_burst(0.12, 0.08, 400, 4000), P['B5'] + 0.05)   # "1 ปี" stamp

# ---------------- S3: too shy to order ----------------
place(sfx, glide(500, 380, 0.4, 0.035), P['C1'] + 0.1)                                            # mom's shy laugh-ish
place(sfx, whoosh(0.35, 0.06, 400, 3000), P['C3'] - 0.2)
place(sfx, blip(700, 1000, 0.07, 0.07), P['C3'] + 0.1)
place(sfx, whoosh(0.28, 0.04, 600, 3000), P['C4'] - 0.1)                                          # the box drops onto the pan
place(sfx, thump(75, 0.3, 0.13), P['C4'] + 0.18); place(sfx, clank(0.03, 1400), P['C4'] + 0.18)
place(sfx, fade(glide(300, 240, 0.7, 0.02), 0.05, 0.4), P['C4'] + 0.25)                            # beam creaks over
place(sfx, thump(80, 0.25, 0.10), P['C5'] + 0.05)
place(sfx, whoosh(0.4, 0.06, 300, 2500), P['C6'] - 0.1)
for k in range(4):
    place(sfx, clank(0.018, 2400 + 300 * k), P['C8'] + 0.05 + k * 0.12)                          # the wire
place(sfx, fade(glide(600, 300, 0.8, 0.02), 0.1, 0.4), P['C8'] + 0.5)

# ---------------- S4: title ----------------
place(sfx, whoosh(0.8, 0.06, 300, 2000), s['s4'] - 0.6)
place(sfx, fade(noise_burst(0.8, 0.04, 2000, 9000, 1.2), 0.4, 0.3), s['s4'] - 0.3)
for i in range(2):
    place(sfx, thump(120 - i * 8, 0.22, 0.08), s['s4'] + 0.15 + i * 0.08)
place(sfx, noise_burst(0.5, 0.025, 3000, 8000), s['s4'] + 0.6); place(sfx, bell(1319, 1.2, 0.05), s['s4'] + 0.9)

# ---------------- S5: two pairs, shipping paid ----------------
place(sfx, whoosh(0.4, 0.06, 400, 3000), s['s5'] + 0.05)
place(sfx, tick(0.05, 1800), P['D1']); place(sfx, blip(700, 1100, 0.07, 0.07), P['D1'] + 0.02)     # qty +1
place(sfx, blip(800, 1200, 0.07, 0.07), P['D2'] + 0.02)
place(sfx, tick(0.06, 1500), P['D2'] + 0.5)                                                        # tap order
cash(P['D2'] + 0.7, 0.06); place(sfx, sparkle(0.05, 2093, 9), P['D2'] + 0.75)

# ---------------- S6: new slippers ----------------
place(sfx, whoosh(0.5, 0.05, 300, 2500), s['s6'] - 0.2)
place(sfx, blip(600, 1000, 0.08, 0.07), s['s6'] + 0.15); place(sfx, blip(700, 1100, 0.08, 0.07), s['s6'] + 0.55)
for k in range(6):
    place(sfx, thump(150, 0.05, 0.035), s['s6'] + 0.7 + k * 0.45)                                 # slipper taps
place(sfx, sparkle(0.04, 1760, 8), P['D4'] + 0.3)
place(sfx, fade(noise_burst(1.0, 0.04, 2000, 9000, 1.2), 0.5, 0.4), P['end'] - 0.5)

# ---------------- S7: end card ----------------
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


target = target + ramp(P['title'] - 0.2, P['D0'] + 0.1, -17.0, 0.4) + ramp(P['B1'], P['B5'] + 0.6, -26.0, 0.4) + ramp(P['end'] - 0.2, DUR + 1, -17.0, 0.5)
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

mix = voice + music + 0.9 * sfx + amb
fadeo = np.ones(N); fo = int(0.45 * SR); fadeo[-fo:] = np.linspace(1, 0, fo)
mix *= fadeo[:, None]
np.save(out_path + '.stems.npy', np.stack([voice.mean(1), music.mean(1), sfx.mean(1), amb.mean(1)]).astype(np.float32))
sf.write(out_path + '.pre.wav', mix.astype(np.float32), SR, subtype='FLOAT')
print('pre-master peak', round(float(np.max(np.abs(mix))), 3))

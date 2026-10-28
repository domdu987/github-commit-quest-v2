# "75 วันของพ่อ" soundtrack: phrase-placed Charon narration, the ElevenLabs score (levelled, ducked under the
# voice, lifted for the title and end card), ambience beds and UI/action sounds synced to story2/scenes.js.
# Usage (from the scratchpad root): python story2/audio.py story2/segments.json story2/music/music.mp3 <out>
import sys, json, subprocess
import numpy as np
import soundfile as sf

SR = 44100
seg_path, music_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
js = open('story2/vo.js').read()
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
SC = {'s1': 0, 's2': 7.62, 's3': 13.40, 's4': 22.25, 's5': 28.45, 's6': 34.35, 's7': 38.06, 's8a': 40.25, 's8b': 43.85, 's8c': 47.62, 's8d': 51.75, 's9': P['end']}

# ---------------- ambience beds ----------------
place(amb, fade(bed(7.7, 80, 500, 0.016), 0.3, 0.1), 0.0)                                      # S1 night room + far city
site = bed(14.8, 35, 160, 0.045, 0.25, 0.6) + bed(14.8, 400, 2500, 0.010, 0.4, 0.4)
place(amb, fade(site, 0.05, 0.3), SC['s2'])                                                     # S2–S3 machinery + wind
place(amb, fade(cicada(20.9, 0.006), 0.6, 0.6), SC['s2'])                                       # midday cicadas
place(amb, fade(0.55 * bed(6.3, 35, 160, 0.045, 0.25, 0.6), 0.1, 0.3), SC['s4'])                # S4 quieter site
for at in np.arange(SC['s2'] + 0.4, SC['s5'] - 0.4, 1.0):                                       # distant hammers
    if rng.random() < 0.7:
        place(amb, clank(0.012, rng.uniform(1500, 2300)), at + rng.uniform(0, 0.5), pan=rng.uniform(-0.7, 0.7))
for at in (9.6, 16.8, 25.0):                                                                     # crane reversing beeper
    for k in range(3):
        place(amb, softsq(1050, 0.22, 0.010), at + k * 0.45, pan=0.6)
place(amb, fade(bed(6.0, 100, 1000, 0.012, 0.2, 0.2), 0.2, 0.2), SC['s5'])                      # S5 condo day: traffic hush
for at, pn in ((28.9, -0.5), (30.9, 0.4), (33.0, -0.2)):
    place(amb, chirp_bird(0.018), at, pan=pn)
place(amb, fade(crickets(3.9, 0.010), 0.3, 0.3), SC['s6'])                                      # S6 Dad's night
place(amb, fade(fan(3.9, 0.006), 0.3, 0.3), SC['s6'], pan=0.5)
for k in range(4):
    place(amb, tick(0.018, 1400), SC['s6'] + 0.3 + k * 1.0)                                      # wall clock
place(amb, fade(crickets(2.3, 0.006), 0.2, 0.6), SC['s7'])                                      # under the title
place(amb, fade(bed(3.7, 80, 500, 0.014), 0.2, 0.2), SC['s8a'])                                 # son's room
place(amb, fade(crickets(12.3, 0.008), 0.3, 0.6), SC['s8b'])                                    # Dad's house to the end
place(amb, fade(fan(12.3, 0.005), 0.3, 0.6), SC['s8b'], pan=0.5)

# ---------------- S1: midnight order ----------------
place(sfx, whoosh(0.3, 0.06, 500, 3500), 0.02)                                                  # clock card
place(sfx, whoosh(0.3, 0.08, 400, 3000), P['A0'] - 0.25); place(sfx, blip(560, 900, 0.08, 0.12), P['A0'] - 0.1)  # shop card
ticks_roll(P['A1'] + 0.2, P['A1'] + 1.0, 14, 0.03)                                               # price rolls 0 → 30,000
place(sfx, bell(1568, 0.9, 0.07), P['A1'] + 1.05); place(sfx, thump(140, 0.15, 0.08), P['A1'] + 1.03)
for k in range(5):
    place(sfx, tick(0.04, 1800), P['A2'] - 0.9 + k * 0.2)                                        # seconds to midnight
place(sfx, tick(0.07, 1200), P['A2'] + 0.1); place(sfx, bell(880, 1.4, 0.07), P['A2'] + 0.12)   # 00:00 flip
t_tap = P['A2'] + 0.3
place(sfx, tick(0.09, 2400), t_tap); place(sfx, thump(260, 0.06, 0.06), t_tap)                  # tap
place(sfx, blip(880, 1320, 0.08, 0.12), t_tap + 0.06); place(sfx, bell(1760, 0.8, 0.06), t_tap + 0.14)   # ordered ✓
place(sfx, sparkle(0.04, 2093, 7), t_tap + 0.08)                                                 # confetti
place(sfx, blip(600, 900, 0.07, 0.12), P['A3'] + 0.05)                                           # stopwatch chip
for k in range(8):
    place(sfx, tick(0.03, 4200), P['A3'] + 0.2 + k * 0.17)
place(sfx, whoosh(0.5, 0.12, 300, 6000), SC['s2'] - 0.45)                                       # into the sun flash
place(sfx, fade(noise_burst(0.9, 0.05, 2000, 9000, 1.2), 0.05, 0.6), SC['s2'] - 0.05)

# ---------------- S2: noon on the site ----------------
for k in range(6):
    place(sfx, step(0.035), SC['s2'] + 0.35 + k * 1.07, pan=-0.2)                                  # gravel steps
place(sfx, blip(520, 860, 0.08, 0.12), P['A4'] + 0.1); place(sfx, glide(500, 1500, 0.7, 0.04), P['A4'] + 0.2)   # sun/thermo
place(sfx, whoosh(0.3, 0.09, 400, 3000), P['A5'] - 0.15)                                       # money card swings
for k in range(3):
    place(sfx, noise_burst(0.06, 0.05, 2000, 7000), P['A5'] + k * 0.08)                          # banknotes riffle
place(sfx, bell(2093, 0.6, 0.04), P['A5'] + 0.3)
place(sfx, drop_plip(0.16), P['A6']); place(sfx, drop_plip(0.08), P['A6'] + 0.42)              # sweat drop
place(sfx, whoosh(0.3, 0.09, 400, 3000), P['A7'] - 0.25)                                       # 75 days card
ticks_roll(P['A7'] - 0.05, P['A7'] + 0.8, 16, 0.03)
place(sfx, thump(80, 0.4, 0.18), P['A7'] + 0.85); place(sfx, bell(1047, 1.6, 0.09), P['A7'] + 0.86); place(sfx, sparkle(0.03), P['A7'] + 0.88)

# ---------------- S3: the work ----------------
place(sfx, whoosh(0.25, 0.08, 300, 4000), SC['s3'] - 0.1)
place(sfx, blip(600, 900, 0.07, 0.12), P['B0'] - 0.05)                                          # name tag
for k in range(7):
    place(sfx, noise_burst(0.32, 0.03 + 0.01 * (k % 2), 500, 3200, 1.2), SC['s3'] + 0.2 + k * 0.63)  # hoe scrapes the mortar
place(sfx, whoosh(0.3, 0.09, 400, 3000), P['B1'] - 0.25)                                       # wage card
ticks_roll(P['B1'], P['B1'] + 0.9, 14, 0.03)
for k in range(4):
    place(sfx, bell(2637 + 200 * k, 0.35, 0.03), P['B1'] + 0.05 + k * 0.12)                       # coins stack
place(sfx, whoosh(0.3, 0.08, 400, 3000), P['B1'] + 1.45)                                       # equation card
ticks_roll(P['B1'] + 1.7, P['B1'] + 2.3, 10, 0.025)
place(sfx, bell(1319, 1.0, 0.06), P['B1'] + 2.35)
t_lift = P['B2'] - 0.1
place(sfx, noise_burst(0.45, 0.06, 300, 3000), t_lift + 0.05)                                  # bag rustle
place(sfx, thump(95, 0.25, 0.14), t_lift + 0.7)                                                 # bag onto the shoulder
place(sfx, glide(500, 1600, 0.8, 0.035), P['B2'] + 0.25)                                        # thermometer climbs
for at in (P['B2'] + 1.0, P['B2'] + 2.05):
    place(sfx, step(0.05), at, pan=0.1)                                                          # heavy steps
t_hurt = P['B3'] + 0.05
place(sfx, thump(60, 0.45, 0.26), t_hurt); place(sfx, noise_burst(0.12, 0.10, 1500, 6000), t_hurt)   # back gives
place(sfx, bell(740, 0.9, 0.05), t_hurt + 0.02); place(sfx, bell(784, 0.9, 0.05), t_hurt + 0.02)
place(sfx, whoosh(0.3, 0.16, 300, 5000), SC['s4'] - 0.2)                                       # whip to the break

# ---------------- S4: the old phone ----------------
place(sfx, whoosh(0.3, 0.09, 400, 3000), P['B4'])                                               # phone card
place(sfx, softsq(1760, 0.08, 0.03), P['B4'] + 0.3); place(sfx, softsq(1760, 0.08, 0.03), P['B4'] + 0.42)   # old-phone double beep
place(sfx, blip(560, 840, 0.07, 0.10), P['B4'] + 0.3)                                           # ฿30,000 chip
place(sfx, blip(520, 780, 0.07, 0.10), P['B5'] - 0.05)                                          # keypad chip
for k, (lo, hi) in enumerate(((697, 1209), (770, 1336), (852, 1477), (941, 1336))):
    place(sfx, dtmf(lo, hi, 0.035), P['B5'] + 0.15 + k * 0.17)                                  # keys
place(sfx, blip(620, 930, 0.08, 0.12), P['B6']); place(sfx, bell(1175, 0.7, 0.04), P['B6'] + 0.02)  # "10 ปี"
t_crack = P['B7'] + 0.25
for k in range(6):
    place(sfx, noise_burst(0.025, 0.10 - 0.012 * k, 3000, 11000, 0.5), t_crack + k * 0.035)       # screen cracks
place(sfx, glide(2600, 900, 0.25, 0.03), t_crack); place(sfx, thump(180, 0.1, 0.06), t_crack)
place(sfx, whoosh(0.3, 0.16, 300, 5000), SC['s5'] - 0.2)                                       # whip to the son

# ---------------- S5: the son's 30,000-baht phone ----------------
for k in range(8):
    place(sfx, blip(900 + 90 * (k % 4), 1400 + 90 * (k % 4), 0.05, 0.06), P['C1'] + 0.15 + k * 0.32, pan=(k % 3 - 1) * 0.4)   # app pings
place(sfx, thump(150, 0.12, 0.10), P['C1'] + 0.5); place(sfx, bell(2093, 0.5, 0.06), P['C1'] + 0.55); place(sfx, bell(2637, 0.6, 0.05), P['C1'] + 0.63)  # ka-ching
place(sfx, blip(600, 900, 0.07, 0.12), P['C2'] + 0.1)                                          # "ถือทุกวัน"
for k in range(8):
    place(sfx, noise_burst(0.04, 0.025, 1500, 5000), P['C2'] + 0.15 + k * 0.17)                 # calendar pages
place(sfx, fade(noise_burst(0.6, 0.03, 1500, 7000, 1.0), 0.3, 0.2), SC['s6'] - 0.3)              # soft cross-fade

# ---------------- S6: Dad's call log: 0 ----------------
place(sfx, whoosh(0.3, 0.07, 400, 2500), P['C3'] - 0.25)
place(sfx, softsq(523, 0.12, 0.025), P['C4'] + 0.05); place(sfx, softsq(392, 0.22, 0.025), P['C4'] + 0.2)   # empty-log "bop-bop"
place(sfx, thump(55, 0.6, 0.12), P['C4'] + 0.05)

# ---------------- S7: title ----------------
place(sfx, whoosh(0.8, 0.06, 300, 2000), SC['s7'] - 0.6)
for i in range(2):
    place(sfx, thump(120 - i * 10, 0.25, 0.10), SC['s7'] + 0.2 + i * 0.1)                        # digits land
place(sfx, thump(100, 0.25, 0.08), SC['s7'] + 0.45)
place(sfx, noise_burst(0.5, 0.025, 3000, 8000), SC['s7'] + 0.6)
place(sfx, bell(1047, 1.4, 0.05), SC['s7'] + 0.8)
for at in (SC['s7'] + 1.0, SC['s7'] + 1.85):
    place(sfx, thump(55, 0.18, 0.07), at); place(sfx, thump(50, 0.2, 0.05), at + 0.2)              # heartbeat
place(sfx, noise_burst(0.7, 0.02, 4000, 9000), SC['s7'] + 1.15)                                 # glint
place(sfx, fade(noise_burst(0.9, 0.05, 2000, 9000, 1.2), 0.5, 0.3), SC['s8a'] - 0.4)             # bloom to warm white

# ---------------- S8a: the son calls ----------------
place(sfx, whoosh(0.3, 0.08, 400, 3000), P['D0'] - 0.3)                                        # call screen
t_dial = P['D1'] + 0.35
place(sfx, tick(0.09, 2400), t_dial); place(sfx, blip(700, 1000, 0.06, 0.08), t_dial + 0.02)
place(sfx, fade(np.sin(2 * np.pi * 425 * tt(1.0)) * 0.03, 0.02, 0.05), t_dial + 0.25)          # ring-back tone

# ---------------- S8b: Dad's phone rings ----------------
place(sfx, old_ring(P['D2'] + 0.9 - SC['s8b'], 0.035), SC['s8b'], pan=0.25)
place(sfx, buzz(P['D2'] + 0.9 - SC['s8b'], 0.035), SC['s8b'], pan=0.25)
place(sfx, blip(620, 980, 0.08, 0.10), SC['s8b'] + 0.15)                                         # incoming card
t_grab = P['D2'] + 0.9
place(sfx, noise_burst(0.12, 0.05, 800, 4000), t_grab - 0.1); place(sfx, tick(0.08, 1900), t_grab + 0.02)   # picks up
place(sfx, sparkle(0.04, 1760, 7), P['D3'] + 0.2); place(sfx, bell(1047, 1.4, 0.05), P['D3'] + 0.25)   # hearts

# ---------------- S8c: split screen ----------------
place(sfx, fade(noise_burst(4.0, 0.012, 2500, 8000, 1.0), 0.6, 0.8), SC['s8c'])                 # voice-wave shimmer
place(sfx, blip(600, 960, 0.08, 0.12), P['D4'] + 0.05); place(sfx, sparkle(0.03, 2093, 4), P['D4'] + 0.08)   # gift
place(sfx, noise_burst(0.16, 0.07, 1200, 6000), P['D5'] + 0.35); place(sfx, thump(150, 0.15, 0.10), P['D5'] + 0.5)  # money struck out

# ---------------- S8d: "พ่อเหนื่อยไหม" ----------------
place(sfx, blip(560, 820, 0.07, 0.08), P['D6'] - 0.05)                                          # bubble
for k in range(5):
    place(sfx, blip(1100, 1250, 0.04, 0.025), P['D6'] + 0.3 + k * 0.45)                          # typing dots
place(sfx, bell(1568, 1.2, 0.035), P['D7'] - 0.1)                                               # glint
place(sfx, bell(3136, 1.2, 0.02), P['D7'] + 0.4)                                                # tear
place(sfx, sparkle(0.035, 1760, 6), P['D7'] + 0.35)
place(sfx, fade(noise_burst(1.0, 0.04, 2000, 9000, 1.2), 0.5, 0.4), P['end'] - 0.5)              # bloom to the end card

# ---------------- S9: end card ----------------
E = P['end']
place(sfx, old_ring(1.5, 0.022), E + 0.15, pan=0.0)
place(sfx, sparkle(0.04, 2093, 6), E + 0.3)
for i in range(2):
    place(sfx, thump(120 - i * 10, 0.25, 0.09), E + 0.45 + i * 0.1)
place(sfx, noise_burst(0.5, 0.02, 3000, 8000), E + 0.8)
place(sfx, blip(560, 840, 0.07, 0.08), E + 1.1)
place(sfx, blip(600, 1000, 0.09, 0.14), E + 1.4); place(sfx, bell(1568, 0.9, 0.05), E + 1.42)   # CTA
place(sfx, whoosh(0.8, 0.06, 500, 4000), E + 1.7)                                               # paper plane

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


target = target + ramp(36.3, 38.0, -28.0, 0.6)                 # hold back before the title so "สักวัน" lands bare
target = target + ramp(37.9, 40.5, -17.0, 0.4) + ramp(55.7, DUR + 1, -17.0, 0.5)
gain_db = np.clip(0.6 * (target - lvl), -12, 9)
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

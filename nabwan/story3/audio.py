# "1,095 ข้อความของแม่" soundtrack: phrase-placed Charon narration, the ElevenLabs score (levelled, ducked under the
# voice, lifted for the title and end card), ambience beds and UI/action sounds synced to story3/scenes.js.
# Usage (from the scratchpad root): python story3/audio.py story3/segments.json story3/music/music.mp3 <out>
import sys, json, subprocess
import numpy as np
import soundfile as sf

SR = 44100
seg_path, music_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
js = open('story3/vo.js').read()
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
SC = {'s0': 0, 's1': P['A0'] - 0.3, 's1b': P['A7'] - 0.11, 's2': P['B0'] - 0.08, 's3': P['B4'] - 0.07, 's4': P['C0'] - 0.08, 's6': P['C8'] - 0.05, 's7': P['title'],
      's8': P['D0'] - 0.07, 's9': P['D3'] - 0.06, 's10': P['end']}


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


# ---------------- ambience beds ----------------
place(amb, fade(bed(SC['s1b'] + 0.05, 300, 2500, 0.007, 0.4, 0.2), 0.6, 0.2), 0.0)                # dawn breeze (hook + porch)
birds(0.0, SC['s1b'] - 0.05, 0.02, 1.2)
place(sfx, bell(220, 3.5, 0.03), SC['s1'] + 0.3); place(sfx, bell(330, 3.0, 0.012), SC['s1'] + 0.3)                                    # far temple bell at dawn
place(amb, fade(bed(SC['s3'] - SC['s2'] + 0.1, 60, 400, 0.02, 0.15, 0.3), 0.1, 0.1), SC['s2'])                        # office: AC + computer hum
place(amb, fade(0.4 * np.sin(2 * np.pi * 120 * tt(SC['s3'] - SC['s2'] + 0.1)) * 0.012, 0.2, 0.2), SC['s2'])
place(amb, fade(bed(SC['s4'] - SC['s3'], 300, 2500, 0.006, 0.4, 0.2), 0.3, 0.3), SC['s3'])                      # porch again
birds(SC['s3'], SC['s4'] - SC['s3'], 0.014, 0.9)
place(amb, fade(bed(SC['s6'] - SC['s4'] + 0.1, 120, 900, 0.008), 0.3, 0.3), SC['s4'])                                # bedroom morning
birds(SC['s4'], P['C5'] - 0.35 - SC['s4'], 0.012, 0.8)
for k in range(int(SC['s6'] - SC['s4'])):
    place(amb, tick(0.02 if SC['s4'] + 0.3 + k < P['C5'] else 0.035, 1500), SC['s4'] + 0.3 + k)   # clock ticks, louder in the silence
for k in range(5):
    tb = SC['s4'] + 0.209 + 0.838 * k + (P['C5'] - SC['s4']) - ((P['C5'] - SC['s4']) % 0.838)
    if tb < P['C6'] + 0.6:
        place(sfx, thump(55, 0.18, 0.10), tb); place(sfx, thump(50, 0.2, 0.07), tb + 0.18)       # heartbeat
place(amb, fade(bed(SC['s7'] - SC['s6'] - 0.1, 120, 900, 0.007), 0.2, 0.3), SC['s6'])                                 # Mom's room
birds(SC['s6'], SC['s7'] - SC['s6'] - 0.2, 0.008, 0.6)
place(amb, fade(bed(SC['s9'] - SC['s8'] + 0.1, 120, 900, 0.007), 0.3, 0.3), SC['s8'])
birds(SC['s8'], SC['s9'] - SC['s8'], 0.01, 0.7)
place(amb, fade(bed(P['end'] - SC['s9'] + 0.2, 120, 900, 0.006), 0.3, 0.3), SC['s9'])

# ---------------- S0: the "ถ้า..." hook ----------------
for tin, tsw in ((P['H1'] - 0.05, P['H4'] - 0.15), (P['H1'] + 0.35, P['H4'] + 0.05), (P['H2'] + 0.2, P['H4'] + 0.25)):
    place(sfx, whoosh(0.25, 0.05, 500, 3500), tin - 0.05); chime(tin + 0.02, 0.04, (1319, 1760))      # Mom's sticker banners
    place(sfx, whoosh(0.3, 0.08, 300, 5000), tsw + 0.05)                                            # swiped away
place(sfx, whoosh(0.5, 0.06, 300, 2500), P['H5'] - 0.3)
place(sfx, fade(noise_burst(0.7, 0.03, 2000, 9000, 1.2), 0.3, 0.3), P['H5'] - 0.1)                  # spotlight
place(sfx, thump(60, 0.4, 0.12), P['H5'] + 0.05)
place(sfx, fade(np.sin(2 * np.pi * 330 * tt(1.0)) * 0.018 + np.sin(2 * np.pi * 247 * tt(1.0)) * 0.012, 0.1, 0.7), P['H6'] - 0.05)   # empty slot: hollow tone
place(sfx, blip(500, 1000, 0.12, 0.08), P['H7'] - 0.05); place(sfx, bell(988, 1.0, 0.05), P['H7'])  # question mark

# ---------------- S1: dawn, the Monday sticker ----------------
place(sfx, whoosh(0.3, 0.06, 500, 3500), SC['s1'] + 0.05)                                         # clock card
place(sfx, tick(0.07, 1200), P['A1'] + 0.1); chime(P['A1'] + 0.12, 0.05, (1047, 1568))           # 05:59 -> 06:00
place(sfx, whoosh(0.3, 0.08, 400, 3000), P['A2'] - 0.25); place(sfx, blip(560, 900, 0.08, 0.10), P['A2'] - 0.12)   # chat phone
place(sfx, tick(0.08, 2400), P['A2'] + 0.42)                                                     # Mom taps send
place(sfx, blip(700, 1150, 0.08, 0.12), P['A2'] + 0.6); place(sfx, sparkle(0.03, 2093, 5), P['A2'] + 0.65)   # sticker lands
place(sfx, bell(1047, 1.4, 0.06), P['A4'] + 0.05); place(sfx, bell(1319, 1.2, 0.05), P['A4'] + 0.1); place(sfx, bell(1568, 1.2, 0.05), P['A4'] + 0.15)
place(sfx, sparkle(0.04, 2093, 7), P['A4'] + 0.08)                                               # "สวัสดีวันจันทร์" sparkle
place(sfx, blip(640, 960, 0.07, 0.10), P['A5'] + 0.05)                                           # text bubble
place(sfx, blip(600, 900, 0.07, 0.12), P['A6'] + 0.05); place(sfx, fade(noise_burst(0.5, 0.03, 600, 3000, 1.0), 0.1, 0.3), P['A6'] + 0.1)   # flame chip
for k in range(3):
    place(sfx, tick(0.04, 2600 + 300 * k), P['A6'] + 0.25 + k * 0.35)                              # 1, 2, 3 ปี
place(sfx, tick(0.03, 3600), P['A6'] + 0.4)                                                      # read receipt
place(sfx, fade(noise_burst(0.7, 0.04, 2000, 9000, 1.2), 0.3, 0.3), SC['s1b'] - 0.3)              # warm flash

# ---------------- S1b: three years scroll by ----------------
scale = [1047, 1175, 1319, 1568, 1760, 2093, 2349]
for i in range(26):
    if SC['s1b'] + 0.05 + i * 0.13 < SC['s2'] - 0.15:
        place(sfx, blip(scale[i % 7] * 0.6, scale[i % 7], 0.05, 0.035), SC['s1b'] + 0.05 + i * 0.13, pan=0.2)   # sticker pops
ticks_roll(P['A7'] + 0.1, P['A8'] + 1.45, 22, 0.03)
place(sfx, thump(80, 0.4, 0.16), P['A8'] + 1.5); place(sfx, bell(1047, 1.8, 0.08), P['A8'] + 1.52); place(sfx, sparkle(0.04), P['A8'] + 1.55)

# ---------------- S2: the office ----------------
typing_clicks(SC['s2'] + 0.1, P['B0'] - 0.4, 9, 0.03)
place(sfx, buzz(0.45, 0.04), P['B0'] - 0.5)                                                      # phone buzzes on the desk
place(sfx, whoosh(0.3, 0.07, 500, 3500), P['B0'] - 0.45); chime(P['B0'] - 0.35, 0.05, (1319, 1760))   # banner
place(sfx, blip(700, 1050, 0.07, 0.10), P['B0'] + 0.85)                                          # "อ่านแล้ว"
place(sfx, whoosh(0.35, 0.12, 300, 5000), P['B1'] + 0.3)                                         # swiped away
place(sfx, whoosh(0.3, 0.08, 400, 3000), P['B2'] - 0.1)                                          # mute card
for k in range(5):
    place(sfx, bell(1760, 0.25, 0.03), P['B2'] + 0.05 + k * 0.1)                                   # bell jingles
place(sfx, tick(0.09, 1600), P['B2'] + 0.85); place(sfx, blip(900, 500, 0.12, 0.08), P['B2'] + 0.88)   # switch off
place(sfx, noise_burst(0.45, 0.06, 200, 1500, 1.0), P['B3'] + 0.25)                              # sigh
place(sfx, blip(300, 220, 0.12, 0.06), P['B3'] + 0.05); place(sfx, blip(300, 220, 0.12, 0.06), P['B3'] + 0.2)   # annoyed sting
typing_clicks(P['B3'] + 0.8, SC['s3'] - 0.1, 10, 0.03)
place(sfx, whoosh(0.3, 0.16, 300, 5000), SC['s3'] - 0.2)                                        # whip back to Mom

# ---------------- S3: one finger at a time ----------------
place(sfx, blip(560, 840, 0.08, 0.10), P['B4'] - 0.02)                                           # typing card
t0, t1, n = P['B5'] + 0.25, P['B7'] - 0.05, 8
for i in range(n):
    tp = t0 + (t1 - t0) / n * (i + 0.47)
    place(sfx, tick(0.07, 2000), tp); place(sfx, thump(300, 0.05, 0.03), tp)                       # slow, deliberate taps
t_send = P['B7'] + 0.55
place(sfx, tick(0.09, 2200), t_send); place(sfx, whoosh(0.4, 0.07, 800, 5000), t_send + 0.2); chime(t_send + 0.3, 0.05, (1568, 2093))

# ---------------- S4: the silent morning ----------------
for tf, low in ((P['C1'], 0), (P['C2'], 0), (P['C3'], 1)):
    place(sfx, tick(0.07, 1200), tf); place(sfx, bell(880 if not low else 587, 1.0, 0.04), tf + 0.02)
    if low: place(sfx, thump(60, 0.5, 0.12), tf)
place(sfx, whoosh(0.3, 0.06, 400, 2500), SC['s4'] + 0.7)                                         # chat pops up
place(sfx, fade(np.sin(2 * np.pi * 330 * tt(1.2)) * 0.02 + np.sin(2 * np.pi * 247 * tt(1.2)) * 0.015, 0.1, 0.9), P['C4'] - 0.05)   # empty slot: hollow tone
place(sfx, whoosh(0.3, 0.08, 400, 3000), P['C6'] - 0.25)                                         # call screen
place(sfx, tick(0.09, 2400), P['C6'] + 0.25); place(sfx, blip(700, 1000, 0.06, 0.08), P['C6'] + 0.27)
place(sfx, fade(np.sin(2 * np.pi * 425 * tt(1.0)) * 0.03, 0.02, 0.05), P['C6'] + 0.45)             # ring-back
place(sfx, tick(0.06, 1900), SC['s6'] + 0.05)                                                    # Mom picks up

# ---------------- S7: title ----------------
place(sfx, whoosh(0.8, 0.06, 300, 2000), SC['s7'] - 0.6)
place(sfx, fade(noise_burst(0.8, 0.04, 2000, 9000, 1.2), 0.4, 0.3), SC['s7'] - 0.3)
for i in range(5):
    place(sfx, thump(120 - i * 6, 0.22, 0.08), SC['s7'] + 0.15 + i * 0.07)                       # digits land
place(sfx, thump(100, 0.25, 0.07), SC['s7'] + 0.5)
place(sfx, sparkle(0.03, 2093, 5), SC['s7'] + 0.1)
place(sfx, noise_burst(0.5, 0.025, 3000, 8000), SC['s7'] + 0.7); place(sfx, bell(1047, 1.4, 0.05), SC['s7'] + 0.9)
for at in (SC['s7'] + 1.1, SC['s7'] + 1.9):
    place(sfx, thump(55, 0.18, 0.06), at); place(sfx, thump(50, 0.2, 0.045), at + 0.2)
place(sfx, fade(noise_burst(0.8, 0.04, 2000, 9000, 1.2), 0.4, 0.3), SC['s8'] - 0.3)

# ---------------- S8: the proof someone misses you ----------------
place(sfx, whoosh(0.3, 0.07, 400, 3000), P['D0'] - 0.1); place(sfx, ding(0.05), P['D0'] + 0.1)   # bell card
for k in range(4):
    place(sfx, noise_burst(0.25, 0.012, 1500, 5000), SC['s8'] + 0.3 + k * 1.2)                    # scrolling back
place(sfx, blip(500, 760, 0.1, 0.12), P['D2'] - 0.15)                                            # "="
place(sfx, thump(150, 0.15, 0.08), P['D2'] + 0.05); place(sfx, sparkle(0.04, 1760, 6), P['D2'] + 0.08)   # heart
place(sfx, tick(0.09, 1600), P['D2'] + 0.6); place(sfx, blip(500, 900, 0.12, 0.08), P['D2'] + 0.62); place(sfx, ding(0.06), P['D2'] + 0.75)   # notifications back on

# ---------------- S9: she answers ----------------
t_send = P['D4'] + 0.25; t_arr = t_send + 0.55
for k in range(6):
    place(sfx, tick(0.04, 2800), P['D3'] + 0.12 + k * 0.14)                                       # typing the reply
place(sfx, blip(640, 960, 0.07, 0.10), P['D3'] + 0.1)
place(sfx, tick(0.09, 2200), t_send); place(sfx, whoosh(0.6, 0.08, 600, 6000), t_send + 0.05)     # sticker flies down
place(sfx, glide(2400, 900, 0.55, 0.03), t_send + 0.05)
place(sfx, buzz(0.5, 0.035), t_arr); chime(t_arr + 0.05, 0.06, (1319, 1760, 2093))                # Mom's phone lights up
place(sfx, sparkle(0.045, 1760, 7), t_arr + 0.9); place(sfx, bell(1047, 1.6, 0.05), t_arr + 0.95)   # hearts
place(sfx, fade(noise_burst(1.0, 0.04, 2000, 9000, 1.2), 0.5, 0.4), P['end'] - 0.5)              # bloom to the end card

# ---------------- S10: end card ----------------
E = P['end']
chime(E + 0.15, 0.05, (1568, 2093))
place(sfx, sparkle(0.04, 2093, 6), E + 0.3)
for i in range(5):
    place(sfx, thump(120 - i * 6, 0.22, 0.07), E + 0.4 + i * 0.07)
place(sfx, noise_burst(0.5, 0.02, 3000, 8000), E + 0.9)
place(sfx, blip(560, 840, 0.07, 0.08), E + 1.15)
place(sfx, blip(600, 1000, 0.09, 0.14), E + 1.45); place(sfx, bell(1568, 0.9, 0.05), E + 1.47)   # CTA
place(sfx, whoosh(0.8, 0.06, 500, 4000), E + 1.75)                                               # paper plane

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


target = target + ramp(P['C5'] - 0.2, P['C6'] - 0.05, -33.0, 0.5)   # the silent screen: the score nearly drops out
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
music *= (10 ** (-6.5 * np.clip(envv / 0.04, 0, 1) / 20))[:, None]

mix = voice + music + 0.9 * sfx + amb
fadeo = np.ones(N); fo = int(0.45 * SR); fadeo[-fo:] = np.linspace(1, 0, fo)
mix *= fadeo[:, None]
np.save(out_path + '.stems.npy', np.stack([voice.mean(1), music.mean(1), sfx.mean(1), amb.mean(1)]).astype(np.float32))
sf.write(out_path + '.pre.wav', mix.astype(np.float32), SR, subtype='FLOAT')
print('pre-master peak', round(float(np.max(np.abs(mix))), 3))

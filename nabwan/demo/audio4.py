# v4 soundtrack: three narration takes, the ElevenLabs score (levelled, ducked under the voice, lifted for
# the title and end card), ambience beds and UI sounds synced to scenes4.js.
# Usage: python audio4.py <vo_dir> <music.mp3> <out.wav>
import sys, subprocess
import numpy as np
import soundfile as sf

SR = 44100
DUR = 46.0
N = int(SR * DUR)
rng = np.random.default_rng(11)
vo_dir, music_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
seg_path = sys.argv[4] if len(sys.argv) > 4 else None
import os
V6 = os.environ.get('V6') == '1'   # v6 icon set adds a few UI sounds   # v5: phrase-placed narration (vo5_segments.json)
# narration landmarks: v4 values, replaced by vo5.js when phrase placement is used
P = {'song': 7.14, 'wa': 10.46, 'ja': 11.97, 'eek': 13.42, 'sip': 19.71, 'nap': 22.95, 'sam': 24.07, 'hawan': 25.31,
     'doi': 26.72, 'mai1': 30.42, 'mai2': 31.90, 'pimai': 32.55, 'wang': 33.91, 'luk': 40.83, 'tuk': 41.51}
if seg_path:
    import json, os
    js = open(os.path.join(os.path.dirname(seg_path), 'vo5.js')).read()
    P.update(json.loads(js[js.index('{'):js.rindex('}') + 1])['P'])


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


sfx = np.zeros((N, 2))
amb = np.zeros((N, 2))

# ---------------- ambience beds ----------------
place(amb, fade(bed(5.3, 80, 500, 0.018), 0.3, 0.2), 0.0)                                   # S1 city night hum
place(amb, fade(bed(3.7, 60, 300, 0.03), 0.1, 0.1), 5.30)                                   # S2 terminal rumble
eng = fade(bed(13.0, 35, 160, 0.05, 0.25, 0.8) + 0.02 * np.sin(2 * np.pi * 52 * tt(13.0)), 0.1, 0.5)
place(amb, eng[: int(SR * 5.67)], 8.98)                                                    # S3 engine + road
place(amb, fade(bed(5.67, 400, 2500, 0.012, 0.4, 0.5), 0.2, 0.2), 8.98)                    # wind
place(amb, 0.55 * eng[int(SR * 5.67):], 14.65)                                             # S4 cabin hum
crick = np.zeros(int(SR * 6.4))
for c in range(2):
    t0 = rng.uniform(0, 0.4)
    while t0 < 6.2:
        for k in range(3):
            s = tt(0.02); ch = 0.011 * np.sin(2 * np.pi * (4300 + 400 * c) * s) * np.sin(np.pi * s / 0.02)
            i = int((t0 + k * 0.034) * SR); crick[i:i + len(ch)] += ch[: len(crick) - i]
        t0 += rng.uniform(0.6, 1.0)
place(amb, fade(crick, 0.4, 0.4), 21.70, pan=0.0)                                           # S5 crickets
place(amb, fade(crick[: int(SR * 2.3)], 0.2, 0.6), 28.05, gain=0.6)                        # under the title
place(amb, fade(bed(4.45, 150, 900, 0.008), 0.4, 0.2), 30.30)                               # S7 room tone
for at in (30.6, 31.7, 33.2):
    place(amb, chirp_bird(0.02), at, pan=-0.5)
place(amb, fade(bed(7.95, 300, 1400, 0.012, 0.5, 0.2), 0.3, 0.8), 34.75)                    # S8 breeze
for at, pn in ((34.9, -0.6), (35.8, 0.5), (36.9, -0.3), (38.6, 0.6), (40.2, -0.5), (41.6, 0.3)):
    place(amb, chirp_bird(0.028), at, pan=pn)

# ---------------- UI / action sounds ----------------
bz = tt(0.28)
place(sfx, 0.08 * np.sign(np.sin(2 * np.pi * 150 * bz)) * np.sin(np.pi * bz / 0.28), 0.22)  # phone buzz
place(sfx, blip(620, 980, 0.09, 0.28), 0.30)                                                 # notification
place(sfx, bell(1760, 0.9, 0.06), 0.66)
for i in range(13):
    place(sfx, tick(0.03, 2600 + 200 * (i % 3)), 0.52 + i * 0.045)                           # typing
place(sfx, whoosh(0.30, 0.10, 400, 3500), 1.70)                                              # route card flips
if V6:   # v6 icons: typing bubbles, pins drop and squash, hearts when the bus arrives
    for i in range(3): place(sfx, blip(900 + 120 * i, 1300 + 120 * i, 0.05, 0.05), 0.36 + i * 0.08)
    for at in (2.14, 2.42):
        place(sfx, whoosh(0.2, 0.04, 800, 4000), at - 0.22); place(sfx, thump(180, 0.12, 0.10), at); place(sfx, blip(500, 900, 0.06, 0.10), at + 0.01)
    place(sfx, sparkle(0.04, 1760, 6), 3.03)
else:
    place(sfx, blip(700, 1050, 0.07, 0.15), 1.93); place(sfx, blip(760, 1150, 0.07, 0.15), 2.73) # pins
place(sfx, whoosh(0.8, 0.05, 600, 2500), 2.05)                                               # bus travels the route
place(sfx, sparkle(0.04), 2.95)
place(sfx, blip(560, 900, 0.09, 0.18), 3.68)                                                 # days chip
for k in range(12):
    place(sfx, tick(0.035), 3.80 + 0.8 * (1 - (1 - k / 12) ** 0.5) * 0.95)                  # odometer ticks
place(sfx, whoosh(0.28, 0.18, 300, 5000), 5.10)                                              # whip
place(sfx, fade(bed(1.2, 40, 200, 0.06), 0.05, 0.6), 5.30)                                   # bus pulls in
place(sfx, noise_burst(0.55, 0.05, 3000, 9000, 0.6) * np.exp(-tt(0.55) / 0.2), 6.35)         # air brakes
place(sfx, blip(560, 820, 0.07, 0.12), 5.44); place(sfx, blip(600, 900, 0.07, 0.10), 5.52)
place(sfx, whoosh(0.25, 0.08, 500, 3000), 6.34)                                              # card swings in
place(sfx, bell(1568, 0.9, 0.08), P['song'] + 0.06); place(sfx, sparkle(0.035), P['song'] + 0.08)                    # lands on 2
for at, f in ((7.66, 1568), (7.91, 1976)):
    place(sfx, blip(700, 1050, 0.07, 0.14), at); place(sfx, bell(f, 0.8, 0.06), at + 0.02)
place(sfx, thump(90, 0.35, 0.22), 8.98)                                                      # cut to the highway
place(sfx, blip(520, 900, 0.10, 0.20), 9.15); place(sfx, bell(880, 1.4, 0.12), 9.18)         # "?"
place(sfx, whoosh(0.35, 0.09, 300, 2500), P['wa'] - 0.16)                                             # "?" slides, hourglass flips
place(sfx, thump(200, 0.12, 0.08), P['wa'] + 0.49); place(sfx, bell(1320, 0.7, 0.05), P['wa'] + 0.51)
for i in range(10):
    place(sfx, tick(0.02, 5200), P['wa'] + 0.54 + i * 0.25)                                            # sand trickle
place(sfx, blip(660, 990, 0.08, 0.14), P['ja']); place(sfx, blip(740, 1110, 0.08, 0.14), P['ja'] + 0.14)
place(sfx, thump(70, 0.45, 0.24), P['eek']); place(sfx, blip(300, 260, 0.18, 0.09), P['eek'] + 0.01)     # red alert
for i in range(6):
    place(sfx, tick(0.05, 1800), P['eek'] + 0.08 + i * 0.13)                                           # urgent clock ticks
place(sfx, whoosh(0.42, 0.20, 200, 6000), 14.25)                                             # zoom-through
place(sfx, whoosh(0.28, 0.08, 400, 2500), 15.62)                                             # waffle card
place(sfx, noise_burst(0.7, 0.02, 4000, 9000), 15.85)                                        # cells cascade shimmer
for k in range(10):
    place(sfx, bell(1568 * 2 ** (k / 12), 0.5, 0.04), 17.20 + k * 0.15)                     # gold days
place(sfx, bell(1047, 1.4, 0.10), P['sip'] + 0.02); place(sfx, bell(1568, 1.2, 0.06), P['sip'] + 0.04); place(sfx, sparkle(0.04), P['sip'] + 0.04)
place(sfx, whoosh(0.4, 0.07, 400, 3000), 20.42)                                              # card exits
place(sfx, fade(noise_burst(1.4, 0.05, 1500, 7000, 1.0), 0.6, 0.2), 20.60)                  # push into the moon
place(sfx, bell(2637, 1.6, 0.03), 21.70)
place(sfx, noise_burst(0.30, 0.06, 2500, 6000), P['nap'] + 0.35); place(sfx, noise_burst(0.30, 0.06, 2500, 6000), P['nap'] + 0.77)  # marker
place(sfx, bell(1320, 0.8, 0.06), P['nap'] + 1.07); place(sfx, sparkle(0.03), P['nap'] + 1.10)
for i in range(4):
    place(sfx, noise_burst(0.05, 0.03, 1500, 5000), P['nap'] + 1.12 + i * 0.07)                        # page flutter
place(sfx, blip(560, 840, 0.09, 0.16), P['sam'] - 0.25)                                                 # counter card flips
for k in range(26):
    x = k / 26
    place(sfx, tick(0.028, 2800), P['sam'] - 0.05 + (P['hawan'] + 0.47 - P['sam']) * (1 - (1 - x) ** 0.33))                     # counter ticks
place(sfx, bell(1047, 1.8, 0.11), P['hawan'] + 0.42); place(sfx, bell(1568, 1.4, 0.07), P['hawan'] + 0.45); place(sfx, sparkle(0.04), P['hawan'] + 0.45)
place(sfx, blip(600, 900, 0.08, 0.10), P['doi'] + 0.12); place(sfx, bell(1760, 1.0, 0.05), P['doi'] + 0.14)     # heart
place(sfx, bell(3136, 1.2, 0.025), P['doi'] + 0.48)                                                     # tear glint
place(sfx, whoosh(0.8, 0.06, 300, 2000), 27.90)                                               # into the title
for i in range(3):
    place(sfx, thump(120 - i * 10, 0.25, 0.10), 28.20 + i * 0.09)                             # digits land
place(sfx, noise_burst(0.5, 0.025, 3000, 8000), 28.62)
place(sfx, fade(noise_burst(0.9, 0.05, 2000, 9000, 1.2), 0.5, 0.3), 29.80)                    # bloom to white
place(sfx, whoosh(0.28, 0.08, 400, 3000), max(30.22, P['mai1'] - 0.17)); place(sfx, bell(1568, 0.7, 0.04), max(30.47, P['mai1'] + 0.08))  # Songkran card
place(sfx, noise_burst(0.18, 0.08, 1200, 6000), P['mai1'] + 1.02); place(sfx, thump(150, 0.16, 0.12), P['mai1'] + 1.20)   # strike + stamp
place(sfx, whoosh(0.28, 0.08, 400, 3000), P['mai2'] - 0.17); place(sfx, bell(1976, 0.7, 0.04), P['mai2'] + 0.08)  # New Year card
place(sfx, noise_burst(0.18, 0.08, 1200, 6000), P['pimai'] + 0.25); place(sfx, thump(150, 0.16, 0.12), P['pimai'] + 0.43)
place(sfx, whoosh(0.45, 0.10, 250, 2500), P['wang'] - 0.55)                                              # cards fall away
place(sfx, whoosh(0.3, 0.09, 400, 3500), P['wang'] - 0.31)                                               # ticket
place(sfx, thump(110, 0.2, 0.16), P['wang'] + 0.42); place(sfx, bell(1319, 1.0, 0.08), P['wang'] + 0.43); place(sfx, sparkle(0.05), P['wang'] + 0.45)
place(sfx, whoosh(0.28, 0.18, 300, 5000), 34.60)                                              # whip to home
for i in range(8):
    place(sfx, thump(180, 0.07, 0.035), 34.85 + i * 0.5)                                      # soft footsteps
place(sfx, noise_burst(0.12, 0.07, 800, 4000) + thump(160, 0.15, 0.10)[: int(SR * 0.12)], 37.05)  # broom drops
place(sfx, noise_burst(0.10, 0.04, 800, 4000), 37.22)
for i in range(14):
    place(sfx, thump(240, 0.05, 0.02), 35.95 + i * 0.075)                                     # dog paws
place(sfx, fade(noise_burst(1.4, 0.03, 2000, 9000, 1.0), 0.6, 0.6), 38.10)                   # embrace shimmer
place(sfx, sparkle(0.05, 1760, 7), P['luk']); place(sfx, bell(1047, 1.6, 0.06), P['luk'] + 0.02)          # heart burst
place(sfx, fade(noise_burst(1.6, 0.04, 2500, 9000, 1.0), 0.7, 0.5), P['tuk'] - 0.21)                   # light bloom
place(sfx, blip(520, 880, 0.10, 0.16), 42.90); place(sfx, bell(1047, 1.4, 0.08), 42.92); place(sfx, sparkle(0.04), 43.0)
for i in range(3):
    place(sfx, thump(120 - i * 10, 0.25, 0.09), 43.15 + i * 0.09)
place(sfx, noise_burst(0.5, 0.02, 3000, 8000), 43.55)
place(sfx, blip(600, 1000, 0.09, 0.16), 44.25); place(sfx, bell(1568, 0.9, 0.05), 44.27)    # CTA
place(sfx, whoosh(0.8, 0.07, 500, 4000), 44.80)                                              # paper plane

# ---------------- narration ----------------
voice = np.zeros((N, 2))
if seg_path:
    import json
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
for name, at in (() if seg_path else (('A1', 0.50), ('B1', 14.75), ('C1', 30.35))):
    v, sr = sf.read(f'{vo_dir}/{name}44.wav')
    if v.ndim > 1: v = v.mean(axis=1)
    assert sr == SR
    v = band(v, 70, 16000)
    act = v[np.abs(v) > 0.01]
    v = v / (np.sqrt(np.mean(act ** 2)) + 1e-9) * 0.16
    place(voice, v, at)

# ---------------- music: shift 0.5 s earlier, level, duck ----------------
m = subprocess.run(['ffmpeg', '-v', 'error', '-i', music_path, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
mus = np.frombuffer(m, dtype=np.float32).reshape(-1, 2).astype(np.float64)
mus = mus[int(0.5 * SR):]
music = np.zeros((N, 2)); music[: min(N, len(mus))] = mus[:N]
# the score's final chord dies by ~44 s; extend it with a soft reverb tail so the end card isn't silent
tail_src = music[int(42.4 * SR):int(43.6 * SR)].copy()
tail_src *= np.hanning(len(tail_src))[:, None]
irn = int(3.2 * SR)
ir = rng.standard_normal((irn, 2)) * np.exp(-np.arange(irn) / SR / 0.9)[:, None]
wet = np.stack([np.fft.irfft(np.fft.rfft(tail_src[:, c], len(tail_src) + irn) * np.fft.rfft(ir[:, c], len(tail_src) + irn)) for c in range(2)], axis=1)
wet = wet / (np.max(np.abs(wet)) + 1e-9) * np.max(np.abs(tail_src)) * 0.55
place(music, wet, 42.9)
# smoothed music level (dB) and a 60 % leveller toward a target curve
mono = music.mean(axis=1)
win = int(1.2 * SR)
lvl = 10 * np.log10(np.maximum(movavg(mono ** 2, win), 0) + 1e-10)
t = np.arange(N) / SR
target = np.full(N, -24.0)


def ramp(a, b, val, edge=0.5):
    k = np.clip(np.minimum((t - a) / edge, (b - t) / edge), 0, 1)
    k = 0.5 - 0.5 * np.cos(np.pi * k)
    return k * (val - target)


target = target + ramp(27.9, 30.6, -16.0) + ramp(42.2, 46.5, -16.5)
gain_db = np.clip(0.6 * (target - lvl), -12, 9)
gain_db = movavg(gain_db, int(0.3 * SR))
music *= (10 ** (gain_db / 20))[:, None]
# duck under speech: fast-ish attack, slow release envelope follower
vm = np.abs(voice.mean(axis=1))
envv = np.zeros(N); a_att, a_rel = np.exp(-1 / (0.06 * SR)), np.exp(-1 / (0.45 * SR)); e = 0.0
for i in range(0, N, 32):  # block-wise follower for speed
    x = vm[i:i + 32].max()
    e = a_att * e + (1 - a_att) * x if x > e else a_rel ** 32 * e + (1 - a_rel ** 32) * x
    envv[i:i + 32] = e
duck_db = -6.5 * np.clip(envv / 0.04, 0, 1)
music *= (10 ** (duck_db / 20))[:, None]

mix = voice + music + 0.9 * sfx + amb
fadeo = np.ones(N); fo = int(0.45 * SR); fadeo[-fo:] = np.linspace(1, 0, fo)
mix *= fadeo[:, None]
np.save(out_path + '.stems.npy', np.stack([voice.mean(1), music.mean(1), sfx.mean(1), amb.mean(1)]).astype(np.float32))
sf.write(out_path + '.pre.wav', mix.astype(np.float32), SR, subtype='FLOAT')
print('pre-master peak', round(float(np.max(np.abs(mix))), 3))

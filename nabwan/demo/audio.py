# Free placeholder soundtrack for the demo: synthesized soft piano + pad, small UI sounds, and the
# already-generated narration. Usage: python audio.py <vo.wav> <out.wav>
import sys
import numpy as np
import soundfile as sf

SR = 44100
DUR = 17.0
VO_AT = 0.40
N = int(SR * DUR)
rng = np.random.default_rng(7)


def note_hz(name):
    names = {'C': -9, 'C#': -8, 'D': -7, 'D#': -6, 'E': -5, 'F': -4, 'F#': -3, 'G': -2, 'G#': -1, 'A': 0, 'A#': 1, 'B': 2}
    n, octave = name[:-1], int(name[-1])
    return 440.0 * 2 ** ((names[n] + 12 * (octave - 4)) / 12)


def piano(f, dur, vel=1.0):
    t = np.arange(int(SR * dur)) / SR
    env = np.minimum(t / 0.008, 1) * np.exp(-t / (0.9 + 120 / f))
    sig = sum(a * np.sin(2 * np.pi * f * k * t * (1 + 0.0004 * k)) for k, a in [(1, 1), (2, 0.42), (3, 0.16), (4, 0.06)])
    return vel * env * sig


def pad(fs, dur):
    t = np.arange(int(SR * dur)) / SR
    env = np.minimum(t / 0.9, 1) * np.minimum((dur - t) / 0.9, 1)
    sig = 0
    for f in fs:
        for d in (-0.15, 0.15):
            sig = sig + np.sin(2 * np.pi * (f + d) * t + 0.3 * np.sin(2 * np.pi * 0.2 * t))
    return env * sig / (2 * len(fs))


def place(buf, sig, at, gain=1.0):
    i = int(at * SR)
    j = min(len(buf), i + len(sig))
    if j > i:
        buf[i:j] += gain * sig[: j - i]


def reverb(x, secs=1.9, mix=0.28):
    n = int(SR * secs)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR / (secs / 5))
    ir[0] = 0
    wet = np.fft.irfft(np.fft.rfft(x, len(x) + n) * np.fft.rfft(ir, len(x) + n))[: len(x)]
    wet /= np.max(np.abs(wet)) + 1e-9
    return (1 - mix) * x / (np.max(np.abs(x)) + 1e-9) + mix * wet


# --- music: G – Em – C – D at 76 BPM, gentle eighth-note arpeggios ---
beat = 60 / 76
bar = 4 * beat
chords = [
    (['G2', 'D3'], ['G3', 'B3', 'D4', 'B3', 'G4', 'D4', 'B3', 'D4']),
    (['E2', 'B2'], ['E3', 'G3', 'B3', 'G3', 'E4', 'B3', 'G3', 'B3']),
    (['C2', 'G2'], ['C3', 'G3', 'C4', 'E4', 'G4', 'E4', 'C4', 'G3']),
    (['D2', 'A2'], ['D3', 'A3', 'D4', 'F#4', 'A4', 'F#4', 'D4', 'A3']),
]
music = np.zeros(N)
t = 0.0
k = 0
while t < DUR:
    bass, arp = chords[k % 4]
    for b in bass:
        place(music, piano(note_hz(b), 3.0, 0.55), t)
    place(music, pad([note_hz(n) for n in arp[:3]], bar + 0.6), t, 0.35)
    for i, n in enumerate(arp):
        place(music, piano(note_hz(n), 1.6, 0.42 if i % 2 else 0.5), t + i * beat / 2 + rng.uniform(0, 0.012))
    if k % 2 == 1:  # a soft melody note on the 2nd bar of each pair
        place(music, piano(note_hz(arp[4]) * 2, 2.2, 0.22), t + 2 * beat)
    t += bar
    k += 1
music = reverb(music)
fade = np.ones(N)
fade[: int(0.6 * SR)] = np.linspace(0, 1, int(0.6 * SR))
fade[-int(2.2 * SR):] = np.linspace(1, 0, int(2.2 * SR))
music *= fade

# --- UI sounds ---
def blip(f0, f1, dur, vol):
    tt = np.arange(int(SR * dur)) / SR
    f = np.linspace(f0, f1, len(tt))
    return vol * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / (dur / 3)) * np.minimum(tt / 0.003, 1)


def bell(f, dur, vol):
    tt = np.arange(int(SR * dur)) / SR
    return vol * sum(a * np.sin(2 * np.pi * f * m * tt) * np.exp(-tt / (dur / (1 + m))) for m, a in [(1, 1), (2.76, 0.4), (5.4, 0.15)])


def noise_burst(dur, vol, lo, hi):
    n = int(SR * dur)
    x = rng.standard_normal(n)
    X = np.fft.rfft(x)
    fr = np.fft.rfftfreq(n, 1 / SR)
    X[(fr < lo) | (fr > hi)] = 0
    x = np.fft.irfft(X, n)
    x /= np.max(np.abs(x)) + 1e-9
    env = np.sin(np.linspace(0, np.pi, n)) ** 1.5
    return vol * x * env


sfx = np.zeros(N)


def whoosh(dur, vol, f0, f1):
    n = int(SR * dur)
    x = rng.standard_normal(n)
    out = np.zeros(n)
    # sweep a band-pass by mixing two filtered copies over time
    lo = noise_burst(dur, 1.0, f0, f0 * 3)
    hi = noise_burst(dur, 1.0, f1 / 3, f1)
    k = np.linspace(0, 1, n)
    out = (1 - k) * lo + k * hi
    env = np.sin(np.linspace(0, np.pi, n)) ** 2
    return vol * out * env


def thump(f, dur, vol):
    tt = np.arange(int(SR * dur)) / SR
    return vol * np.sin(2 * np.pi * f * tt * (1 - 0.3 * tt / dur)) * np.exp(-tt / (dur / 4))


buzz_t = np.arange(int(SR * 0.28)) / SR
place(sfx, 0.10 * np.sign(np.sin(2 * np.pi * 150 * buzz_t)) * np.sin(np.pi * buzz_t / 0.28), 0.22)  # phone buzz
place(sfx, blip(620, 980, 0.09, 0.30), 0.30)       # notification drops in
place(sfx, bell(1760, 0.9, 0.07), 0.66)            # sparkle on the avatar
place(sfx, whoosh(0.28, 0.20, 300, 5000), 2.13)    # whip pan
place(sfx, blip(560, 820, 0.07, 0.14), 2.41)       # clock card
place(sfx, blip(600, 900, 0.07, 0.12), 2.47)       # departure board
place(sfx, whoosh(0.22, 0.08, 500, 3000), 2.55)    # counter card swings in
for at, f in ((2.99, 1568), (3.29, 1976)):
    place(sfx, blip(700, 1050, 0.07, 0.16), at)    # chips pop
    place(sfx, bell(f, 0.8, 0.07), at + 0.02)
place(sfx, thump(90, 0.35, 0.22), 4.12)            # cut to the highway
place(sfx, blip(520, 900, 0.10, 0.22), 4.27)       # question mark pops
place(sfx, bell(880, 1.4, 0.14), 4.30)
place(sfx, thump(70, 0.45, 0.26), 6.32)            # red alert on "อีกกี่วัน"
place(sfx, blip(300, 260, 0.18, 0.10), 6.33)
place(sfx, whoosh(0.42, 0.22, 200, 6000), 7.68)    # zoom through the window
place(sfx, whoosh(0.25, 0.08, 400, 2500), 8.17)    # waffle card swings in
for i in range(10):
    place(sfx, bell(2093 + 60 * i, 0.5, 0.045), 8.69 + i * 0.085)  # golden days light up
place(sfx, blip(560, 840, 0.09, 0.20), 10.45)      # counter card flips
place(sfx, noise_burst(0.30, 0.06, 2500, 6000), 10.88)  # marker stroke 1
place(sfx, noise_burst(0.30, 0.06, 2500, 6000), 11.33)  # marker stroke 2
place(sfx, bell(1320, 0.8, 0.07), 11.65)           # X complete
place(sfx, bell(1047, 1.6, 0.12), 13.05)           # counter lands on 355
place(sfx, bell(1568, 1.2, 0.07), 13.12)
place(sfx, whoosh(0.9, 0.10, 300, 2500), 14.30)    # soft whoosh into the title
for i in range(3):
    place(sfx, thump(120 - i * 10, 0.25, 0.12), 14.83 + i * 0.09)  # digits land

# --- narration ---
vo, sr = sf.read(sys.argv[1])
if vo.ndim > 1:
    vo = vo.mean(axis=1)
assert sr == SR, sr
vo = vo / (np.sqrt(np.mean(vo[np.abs(vo) > 0.01] ** 2)) + 1e-9) * 0.16  # speech RMS ~ -16 dBFS
voice = np.zeros(N)
place(voice, vo, VO_AT)

# duck music under speech (smoothed envelope)
env = np.abs(voice)
win = int(0.25 * SR)
env = np.convolve(env, np.ones(win) / win, mode='same')
duck = 1 - 0.45 * np.clip(env / 0.05, 0, 1)
music = music * 0.10 * duck

mix = voice + music + sfx
mix = np.tanh(mix * 1.15) / 1.15  # gentle safety limiter
peak = np.max(np.abs(mix))
mix = mix / peak * 0.89 if peak > 0.89 else mix
stereo = np.stack([mix, mix], axis=1)
sf.write(sys.argv[2], stereo, SR, subtype='PCM_16')
print('wrote', sys.argv[2], 'peak', round(float(np.max(np.abs(mix))), 3))

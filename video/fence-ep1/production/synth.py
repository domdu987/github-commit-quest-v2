"""Deterministic music bed + SFX synthesizer.

Usage: python3 synth.py cues.json out.wav
cues.json: {"duration": 62, "bpm": 100,
            "sections": [{"start":0,"end":8,"mood":"calm"}, ...],
            "sfx": [{"t":1.2,"type":"whoosh"}, ...]}
moods: calm, tension, panic, hope, twist, cta, silence
sfx: whoosh, pop, ding, boom, riser, heartbeat, tick, glitch, notif, buzz, sting, swell
"""
import json
import sys
import wave

import numpy as np

SR = 44100
rng = np.random.default_rng(7)


def t_arr(dur):
    return np.arange(int(dur * SR)) / SR


def env(n, a=0.005, r=0.2):
    e = np.ones(n)
    na, nr = max(1, int(a * SR)), max(1, int(r * SR))
    na, nr = min(na, n), min(nr, n)
    e[:na] = np.linspace(0, 1, na)
    e[-nr:] *= np.linspace(1, 0, nr)
    return e


def osc(freq, dur, kind="sine"):
    t = t_arr(dur)
    ph = 2 * np.pi * np.cumsum(np.broadcast_to(freq, t.shape)) / SR
    if kind == "sine":
        return np.sin(ph)
    if kind == "saw":
        return 2 * ((ph / (2 * np.pi)) % 1) - 1
    if kind == "square":
        return np.sign(np.sin(ph))
    if kind == "tri":
        return 2 * np.abs(2 * ((ph / (2 * np.pi)) % 1) - 1) - 1
    raise ValueError(kind)


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y


def lp_fast(x, cutoff):
    # one-pole lowpass via scipy-free IIR using cumulative trick on blocks
    from numpy.lib.stride_tricks import sliding_window_view  # noqa: F401
    a = np.exp(-2 * np.pi * cutoff / SR)
    # approximate with FIR exponential kernel (fast, deterministic)
    k = int(min(SR * 0.02, 5 / (1 - a)))
    kern = (1 - a) * a ** np.arange(max(k, 1))
    return np.convolve(x, kern)[: len(x)]


def note(m):
    return 440.0 * 2 ** ((m - 69) / 12)


# ---------------- drums ----------------
def kick():
    d = 0.35
    t = t_arr(d)
    f = 50 + 120 * np.exp(-t * 30)
    return osc(f, d) * np.exp(-t * 9) * 0.9


def snare():
    d = 0.22
    t = t_arr(d)
    n = rng.standard_normal(len(t))
    return (n * 0.6 + osc(190, d) * 0.4) * np.exp(-t * 18) * 0.45


def hat():
    d = 0.05
    t = t_arr(d)
    n = rng.standard_normal(len(t))
    n = n - lp_fast(n, 6000)
    return n * np.exp(-t * 80) * 0.18


def clap():
    d = 0.2
    t = t_arr(d)
    n = rng.standard_normal(len(t))
    e = np.exp(-t * 25) + 0.6 * np.exp(-np.maximum(t - 0.012, 0) * 40) * (t > 0.012)
    return n * e * 0.3


# ---------------- tonal layers ----------------
CHORDS = {
    "calm": [[60, 64, 67, 71], [57, 60, 64, 67], [53, 57, 60, 64], [55, 59, 62, 65]],  # Cmaj7 Am7 Fmaj7 G7
    "hope": [[53, 57, 60, 64], [55, 59, 62, 67], [57, 60, 64, 67], [60, 64, 67, 72]],
    "tension": [[57, 60, 64], [57, 60, 64], [53, 57, 60], [52, 56, 59]],  # Am Am F E
    "panic": [[57, 60, 63], [57, 60, 63], [56, 59, 62], [56, 59, 62]],  # dim-ish
    "cta": [[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]],
    "twist": [[45, 48, 51], [45, 48, 51]],
}


def pad(chord, dur, bright=1500, vol=0.08):
    x = sum(osc(note(m), dur, "saw") + osc(note(m) * 1.005, dur, "saw") for m in chord)
    x = lp_fast(x, bright)
    return x * env(len(x), 0.3, 0.4) * vol / len(chord)


def pluck(m, dur=0.25, vol=0.12, kind="square"):
    t = t_arr(dur)
    x = osc(note(m), dur, kind) * np.exp(-t * 14)
    return lp_fast(x, 3500) * vol


def bass(m, dur, vol=0.22):
    x = osc(note(m - 12), dur, "saw")
    x = lp_fast(x, 400)
    return x * env(len(x), 0.005, 0.05) * vol


def add(buf, x, t0, gain=1.0):
    i = int(t0 * SR)
    if i >= len(buf) or i + len(x) <= 0:
        return
    if i < 0:
        x = x[-i:]
        i = 0
    j = min(len(buf), i + len(x))
    buf[i:j] += x[: j - i] * gain


def render_section(buf, s, bpm):
    mood = s["mood"]
    start, end = s["start"], s["end"]
    if mood == "silence":
        return
    beat = 60 / bpm
    bar = beat * 4
    if mood == "ambient":
        beat = 60 / bpm
        prog = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 65]]  # Am7 Fmaj7 Cmaj7 G7
        bar = beat * 4
        nb = int(np.ceil((end - start) / bar))
        for b in range(nb):
            t0 = start + b * bar
            seg = min(bar, end - t0)
            if seg <= 0.05:
                break
            ch = prog[b % 4]
            add(buf, pad(ch, seg + 0.3, 900, 0.07), t0)
            sub = osc(note(ch[0] - 12), seg) * env(int(seg * SR), 0.4, 0.5) * 0.10
            add(buf, sub, t0)
            for q in range(8):
                tb = t0 + q * beat / 2
                if tb >= end:
                    break
                m = (ch + [ch[1] + 12])[[0, 2, 1, 3, 4, 3, 2, 1][q]] + 12
                d = 0.9
                tt = t_arr(d)
                ep = (osc(note(m), d) + 0.25 * osc(note(m) * 2, d) + 0.08 * osc(note(m) * 3, d)) * np.exp(-tt * 3.2)
                add(buf, lp_fast(ep, 2500) * 0.075, tb)
            add(buf, kick() * 0.25, t0)
            add(buf, kick() * 0.18, t0 + 2 * beat)
        return
    if mood == "twist":
        # low drone + detuned bell, sparse
        d = end - start
        x = pad([33, 45, 46], d, 600, 0.22)
        add(buf, x, start)
        for k, m in enumerate([75, 74, 70, 69]):
            add(buf, pluck(m, 1.2, 0.08, "sine"), start + 0.4 + k * beat * 2)
        return
    chords = CHORDS[mood]
    nb = int(np.ceil((end - start) / bar))
    for b in range(nb):
        t0 = start + b * bar
        ch = chords[b % len(chords)]
        seg = min(bar, end - t0)
        if seg <= 0.05:
            break
        bright = {"calm": 1400, "hope": 2600, "tension": 900, "panic": 1800, "cta": 3200}[mood]
        add(buf, pad(ch, seg, bright, 0.09 if mood != "panic" else 0.07), t0)
        for q in range(4):
            tb = t0 + q * beat
            if tb >= end:
                break
            if mood in ("calm", "hope", "cta"):
                if q in (0, 2) or mood == "cta":
                    add(buf, kick(), tb, 0.8 if mood != "calm" else 0.5)
                if q in (1, 3):
                    add(buf, clap() if mood == "cta" else snare(), tb, 0.6 if mood == "calm" else 0.8)
                for h in range(2):
                    add(buf, hat(), tb + h * beat / 2, 0.7)
                add(buf, bass(ch[0], beat * 0.9), tb, 0.8)
                arp = ch + [ch[0] + 12]
                for h in range(2):
                    add(buf, pluck(arp[(q * 2 + h) % len(arp)] + 12, 0.22, 0.07, "tri"), tb + h * beat / 2)
            elif mood == "tension":
                # pulsing bass eighths, kick on 1, rising hats
                for h in range(2):
                    add(buf, bass(ch[0], beat / 2 * 0.8, 0.25), tb + h * beat / 2)
                if q == 0:
                    add(buf, kick(), tb, 0.9)
                add(buf, hat(), tb + beat / 2, 0.9)
            elif mood == "panic":
                for h in range(4):
                    add(buf, bass(ch[0], beat / 4 * 0.8, 0.22), tb + h * beat / 4)
                    add(buf, hat(), tb + h * beat / 4, 0.8)
                add(buf, kick(), tb, 1.0)
                if q in (1, 3):
                    add(buf, snare(), tb, 0.9)
    # soften section edges
    a, b = int(start * SR), min(len(buf), int(end * SR))


# ---------------- sfx ----------------
def sfx(kind):
    if kind == "whoosh":
        d = 0.45
        t = t_arr(d)
        n = rng.standard_normal(len(t))
        cut = 300 + 5000 * np.sin(np.pi * t / d)
        out = np.zeros_like(n)
        # crude sweep: blend of two filters by progress
        lo, hi = lp_fast(n, 600), lp_fast(n, 5000)
        w = np.sin(np.pi * t / d)
        out = lo * (1 - w) + hi * w
        return out * np.sin(np.pi * t / d) ** 2 * 0.35 + 0 * cut
    if kind == "pop":
        d = 0.12
        t = t_arr(d)
        return osc(900 * np.exp(-t * 20) + 300, d) * np.exp(-t * 40) * 0.35
    if kind == "ding":
        d = 0.9
        t = t_arr(d)
        return (osc(1318, d) + 0.5 * osc(1975, d) + 0.25 * osc(2637, d)) * np.exp(-t * 5) * 0.15
    if kind == "notif":
        a = sfx("ding")[: int(0.18 * SR)]
        d = 0.6
        t = t_arr(d)
        b = (osc(1760, d) + 0.4 * osc(2637, d)) * np.exp(-t * 6) * 0.15
        out = np.zeros(int(0.8 * SR))
        out[: len(a)] += a
        out[int(0.14 * SR): int(0.14 * SR) + len(b)] += b
        return out
    if kind == "boom":
        d = 2.2
        t = t_arr(d)
        f = 30 + 80 * np.exp(-t * 6)
        n = lp_fast(rng.standard_normal(len(t)), 300)
        return (osc(f, d) * 0.9 + n * 0.5) * np.exp(-t * 1.8) * 0.9
    if kind == "riser":
        d = 2.0
        t = t_arr(d)
        f = 200 * (2 ** (3 * t / d))
        n = rng.standard_normal(len(t))
        x = osc(f, d, "saw") * 0.15 + (n - lp_fast(n, 2000)) * 0.15 * (t / d)
        return lp_fast(x, 6000) * (t / d) ** 1.5 * 0.7
    if kind == "heartbeat":
        out = np.zeros(int(0.7 * SR))
        for off, g in ((0, 1.0), (0.18, 0.7)):
            d = 0.18
            t = t_arr(d)
            x = osc(55 + 20 * np.exp(-t * 30), d) * np.exp(-t * 18) * g * 0.8
            add(out, x, off)
        return out
    if kind == "tick":
        d = 0.04
        t = t_arr(d)
        return osc(2500, d, "square") * np.exp(-t * 150) * 0.12
    if kind == "glitch":
        d = 0.35
        out = np.zeros(int(d * SR))
        for k in range(7):
            seg = osc(200 + 400 * ((k * 37) % 7), 0.04, "square") * 0.15
            add(out, seg, k * 0.045)
        return out
    if kind == "buzz":
        d = 0.9
        t = t_arr(d)
        on = (np.floor(t / 0.15) % 2 == 0)
        return osc(150, d, "square") * on * 0.08 * lp_fast(np.ones(len(t)), 50)
    if kind == "sting":
        d = 1.6
        t = t_arr(d)
        x = sum(osc(note(m), d, "saw") for m in (57, 60, 63, 66))
        return lp_fast(x, 2500) * np.exp(-t * 2.2) * 0.12
    if kind == "swell":
        d = 1.5
        t = t_arr(d)
        x = sum(osc(note(m), d, "saw") for m in (60, 64, 67, 72))
        return lp_fast(x, 2000) * (t / d) ** 2 * 0.1
    if kind == "knock":
        out = np.zeros(int(0.9 * SR))
        for k in range(3):
            d = 0.12
            t = t_arr(d)
            x = (osc(140 + 30 * np.exp(-t * 40), d) * 0.8 + lp_fast(rng.standard_normal(len(t)), 900) * 0.6) * np.exp(-t * 38)
            add(out, x * 0.9, k * 0.26)
        return out
    if kind == "creak":
        d = 1.1
        t = t_arr(d)
        f = 90 + 40 * np.sin(2 * np.pi * 1.3 * t) + 25 * np.sin(2 * np.pi * 7 * t)
        x = osc(f, d, "saw") * (0.5 + 0.5 * np.sin(2 * np.pi * 23 * t) ** 2)
        return lp_fast(x, 1800) * np.sin(np.pi * t / d) * 0.18
    if kind == "wind":
        d = 6.0
        t = t_arr(d)
        n = rng.standard_normal(len(t))
        lo, hi = lp_fast(n, 300), lp_fast(n, 1200)
        w = 0.5 + 0.5 * np.sin(2 * np.pi * 0.23 * t + 1.0)
        return (lo * (1 - w) + hi * w) * np.sin(np.pi * t / d) * 0.5
    if kind == "thunder":
        d = 3.0
        t = t_arr(d)
        n = lp_fast(rng.standard_normal(len(t)), 220)
        env_ = np.exp(-t * 1.4) * (1 + 0.6 * np.sin(2 * np.pi * 3.1 * t))
        return (n * 1.4 + osc(38 + 20 * np.exp(-t * 3), d) * 0.5) * env_ * 0.9
    if kind == "hum":
        d = 4.0
        t = t_arr(d)
        x = osc(48, d, "saw") * 0.6 + osc(96, d) * 0.3 + rng.standard_normal(len(t)) * 0.05
        return lp_fast(x, 500) * env(len(t), 0.5, 0.8) * 0.12
    if kind == "siren":
        d = 3.0
        t = t_arr(d)
        f = np.where((t % 1.0) < 0.5, 960, 770)
        return lp_fast(osc(f, d, "tri"), 3000) * env(len(t), 0.6, 0.8) * 0.12
    if kind == "meow":
        d = 0.7
        t = t_arr(d)
        f = 520 + 260 * np.sin(np.pi * t / d)
        return lp_fast(osc(f, d, "saw"), 2200) * np.sin(np.pi * t / d) ** 1.5 * 0.12
    if kind == "hiss":
        d = 0.8
        t = t_arr(d)
        n = rng.standard_normal(len(t))
        return (n - lp_fast(n, 2500)) * np.exp(-t * 2.5) * env(len(t), 0.02, 0.2) * 0.35
    if kind == "whistle":  # pea whistle: bright tone with a fast trill
        d = 0.42
        t = t_arr(d)
        f = 2850 + 140 * np.sin(2 * np.pi * 38 * t)
        x = osc(f, d) * (0.75 + 0.25 * np.sin(2 * np.pi * 38 * t)) + 0.15 * osc(2 * f, d)
        return x * env(len(t), 0.015, 0.06) * 0.22
    if kind == "whistlefar":
        return lp_fast(sfx("whistle"), 1600) * 0.6
    if kind == "trumpet":  # elephant trumpet: buzzy rising-falling blare
        d = 1.5
        t = t_arr(d)
        f = 380 + 360 * np.sin(np.pi * np.clip(t / 1.2, 0, 1)) + 25 * np.sin(2 * np.pi * 9 * t)
        x = osc(f, d, "saw") + 0.5 * osc(f * 1.5, d, "square") + 0.4 * rng.standard_normal(len(t))
        return lp_fast(x, 2600) * env(len(t), 0.08, 0.5) * 0.22
    if kind == "stomp":
        d = 0.6
        t = t_arr(d)
        return (osc(32 + 30 * np.exp(-t * 12), d) + 0.4 * lp_fast(rng.standard_normal(len(t)), 150)) * np.exp(-t * 7) * 0.8
    if kind == "snap":  # twig crack
        out = np.zeros(int(0.25 * SR))
        for off, g in ((0, 1.0), (0.05, 0.6)):
            n = rng.standard_normal(int(0.03 * SR))
            add(out, (n - lp_fast(n, 1500)) * np.exp(-np.arange(len(n)) / SR * 120) * g * 0.7, off)
        return out
    if kind == "rustle":
        d = 1.2
        t = t_arr(d)
        n = rng.standard_normal(len(t))
        am = 0.5 + 0.5 * np.sin(2 * np.pi * 6 * t + 3 * np.sin(2 * np.pi * 1.3 * t))
        return (n - lp_fast(n, 1200)) * am * np.sin(np.pi * t / d) * 0.12
    if kind == "crickets":
        d = 6.0
        t = t_arr(d)
        chirp = ((t * 3.1) % 1.0 < 0.18) * (np.sin(2 * np.pi * 45 * t) > 0)
        chirp2 = (((t + 0.37) * 2.6) % 1.0 < 0.15) * (np.sin(2 * np.pi * 50 * t) > 0)
        x = osc(4300, d) * chirp + 0.7 * osc(3900, d) * chirp2
        return lp_fast(x, 6000) * np.sin(np.pi * t / d) ** 0.3 * 0.025
    if kind == "crackle":
        d = 6.0
        n = int(d * SR)
        out = lp_fast(rng.standard_normal(n), 180) * 0.12
        pops = rng.random(n) < 7 / SR
        out += np.convolve(pops * rng.standard_normal(n), np.exp(-np.arange(200) / 25))[:n] * 0.5
        return out * env(n, 0.5, 0.8) * 0.4
    if kind == "crank":  # starter clicks + a weak motor that dies
        out = np.zeros(int(1.6 * SR))
        for k in range(3):
            add(out, sfx("tick") * 3, k * 0.35)
        d = 0.8
        t = t_arr(d)
        x = osc(22 + 8 * np.sin(2 * np.pi * 3 * t), d, "square") * np.exp(-t * 3)
        add(out, lp_fast(x, 400) * 0.25, 0.9)
        return out
    if kind == "static":
        d = 0.7
        t = t_arr(d)
        n = rng.standard_normal(len(t))
        return (lp_fast(n, 4000) - lp_fast(n, 800)) * env(len(t), 0.01, 0.15) * 0.25
    if kind == "shutter":
        out = np.zeros(int(0.2 * SR))
        for off in (0, 0.07):
            n = rng.standard_normal(int(0.02 * SR))
            add(out, (n - lp_fast(n, 2500)) * 0.5, off)
        return out
    if kind == "ring":  # phone ringtone: two quick tone pairs
        out = np.zeros(int(1.2 * SR))
        for k, f in enumerate((1318, 1568, 1318, 1568)):
            d = 0.13
            add(out, (osc(f, d) + 0.3 * osc(f * 2, d)) * env(int(d * SR), 0.005, 0.04) * 0.16, k * 0.16 + (0.25 if k > 1 else 0))
        return out
    if kind == "vibe":  # phone vibrating on a bench
        d = 0.45
        t = t_arr(d)
        return lp_fast(osc(165, d, "square"), 900) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t)) * env(len(t), 0.02, 0.05) * 0.2
    if kind == "rain":  # steady rain on leaves: hiss bed + scattered drops (6 s, overlap copies to extend)
        d = 6.0
        n = int(d * SR)
        t = t_arr(d)
        bed = lp_fast(rng.standard_normal(n), 5200) - lp_fast(rng.standard_normal(n), 400) * 0.3
        drops = (rng.random(n) < 90 / SR) * rng.standard_normal(n)
        drops = np.convolve(drops, np.exp(-np.arange(160) / 18) * np.sin(np.arange(160) * 0.9))[:n]
        return (bed * 0.18 + drops * 0.35) * np.sin(np.pi * t / d) ** 0.25
    if kind == "stream":  # brook: band-limited noise with a bubbling wobble and small plinks
        d = 6.0
        n = int(d * SR)
        t = t_arr(d)
        x = rng.standard_normal(n)
        band = lp_fast(x, 2400) - lp_fast(x, 300)
        am = 0.55 + 0.45 * np.sin(2 * np.pi * (3.1 + 1.3 * np.sin(2 * np.pi * 0.4 * t)) * t)
        plink = (rng.random(n) < 14 / SR) * 1.0
        plink = np.convolve(plink, np.exp(-np.arange(900) / 120) * np.sin(2 * np.pi * 900 * np.arange(900) / SR))[:n]
        return (band * am * 0.25 + plink * 0.3) * np.sin(np.pi * t / d) ** 0.25
    if kind == "roar":  # flash-flood surge: rising low rumble with churning noise
        d = 2.8
        t = t_arr(d)
        x = rng.standard_normal(len(t))
        rum = lp_fast(x, 160) * 2.2 + (lp_fast(x, 1400) - lp_fast(x, 400)) * 0.6
        rise = np.clip(t / 1.4, 0, 1) ** 1.5 * np.exp(-np.clip(t - 1.8, 0, None) * 2.0)
        return rum * rise * 0.8 + osc(42, d) * rise * 0.25
    if kind == "chalk":  # chalk on a blackboard: dry scratchy strokes, a few short taps between letters (1.4 s)
        d = 1.4
        t = t_arr(d)
        n = rng.standard_normal(len(t))
        strokes = np.clip(np.sin(2 * np.pi * 7 * t + 2 * np.sin(2 * np.pi * 1.7 * t)), 0, None) ** 0.6
        x = (lp_fast(n, 5000) - lp_fast(n, 1800)) * strokes * 0.5
        taps = rng.random(len(t)) < 9 / SR
        x += np.convolve(taps * rng.standard_normal(len(t)), np.exp(-np.arange(120) / 18))[: len(t)] * 0.8
        return x * env(len(t), 0.02, 0.2) * 0.3
    if kind == "cans":  # tin cans clattering onto concrete: a burst of short metallic hits with ringing partials (1.1 s)
        out = np.zeros(int(1.1 * SR))
        for k in range(9):
            d = 0.22
            t = t_arr(d)
            f = 1900 + (k * 419) % 1300
            x = (np.sin(2 * np.pi * f * t) * 0.5 + np.sin(2 * np.pi * f * 2.76 * t) * 0.3 + lp_fast(rng.standard_normal(len(t)), 3000) * 0.5) * np.exp(-t * 26)
            add(out, x * (0.5 + 0.5 * ((k * 7) % 3) / 2), k * 0.09 + ((k * 13) % 5) * 0.01)
        return out * 0.5
    if kind == "canfall":  # one can dropping and rolling: a hit, two bounces, a short roll
        out = np.zeros(int(0.9 * SR))
        for k, (off, g) in enumerate(((0.0, 1.0), (0.17, 0.6), (0.29, 0.35))):
            d = 0.2
            t = t_arr(d)
            x = (np.sin(2 * np.pi * 2300 * t) * 0.5 + np.sin(2 * np.pi * 6100 * t) * 0.25 + lp_fast(rng.standard_normal(len(t)), 3500) * 0.5) * np.exp(-t * 30)
            add(out, x * g, off)
        tr = t_arr(0.45)
        roll = lp_fast(rng.standard_normal(len(tr)), 2500) * (0.5 + 0.5 * np.sin(2 * np.pi * 11 * tr)) * np.exp(-tr * 5)
        add(out, roll * 0.25, 0.38)
        return out * 0.6
    if kind == "radio":  # an old AM radio waking up: hiss, a swept whistle as it tunes, then settled static (2.4 s)
        d = 2.4
        t = t_arr(d)
        n = rng.standard_normal(len(t))
        hiss = (lp_fast(n, 3200) - lp_fast(n, 400)) * (0.35 + 0.65 * np.clip(t / 0.4, 0, 1))
        f = 2600 * np.exp(-t * 2.2) + 140
        whistle = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.6) * 0.6
        crackle = np.convolve((rng.random(len(t)) < 25 / SR) * rng.standard_normal(len(t)), np.exp(-np.arange(80) / 14))[: len(t)] * 0.6
        hum = np.sin(2 * np.pi * 50 * t) * 0.05
        return (hiss * 0.4 + whistle + crackle + hum) * env(len(t), 0.05, 0.3) * 0.3
    if kind == "radiobed":  # the station's carrier under the voice: soft static with a slow wow (4 s, overlap copies)
        d = 4.0
        t = t_arr(d)
        n = rng.standard_normal(len(t))
        return (lp_fast(n, 2800) - lp_fast(n, 500)) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.6 * t)) * np.sin(np.pi * t / d) ** 0.3 * 0.07
    if kind == "gate":  # an iron gate sliding on its rail: a low rumble with a chattering wheel, ending in a clang (1.0 s)
        d = 1.0
        t = t_arr(d)
        n = rng.standard_normal(len(t))
        rumble = lp_fast(n, 260) * (0.6 + 0.4 * np.sin(2 * np.pi * 27 * t)) * np.clip(t / 0.1, 0, 1) * np.clip((d - 0.2 - t) / 0.3, 0, 1)
        out = rumble * 0.9
        tc = t_arr(0.4)
        clang = (np.sin(2 * np.pi * 820 * tc) * 0.5 + np.sin(2 * np.pi * 2140 * tc) * 0.3 + np.sin(2 * np.pi * 3330 * tc) * 0.2 + lp_fast(rng.standard_normal(len(tc)), 3000) * 0.6) * np.exp(-tc * 12)
        add(out, clang * 0.8, d - 0.42)
        return out * 0.5
    if kind == "cicada":  # the midday heat: a dense, rising-falling buzz of cicadas (6 s, overlap copies to extend)
        d = 6.0
        t = t_arr(d)
        buzz = osc(4200 + 120 * np.sin(2 * np.pi * 0.35 * t), d, "square") * (np.sin(2 * np.pi * 110 * t) > 0)
        swell = 0.55 + 0.45 * np.sin(2 * np.pi * 0.22 * t) ** 2
        return lp_fast(buzz, 6500) * swell * np.sin(np.pi * t / d) ** 0.3 * 0.02
    if kind == "page":  # a notebook page turning: a soft brushed sweep with a flap at the end
        d = 0.5
        t = t_arr(d)
        n = rng.standard_normal(len(t))
        sweep = (lp_fast(n, 5000) - lp_fast(n, 1500)) * np.sin(np.pi * np.clip(t / 0.35, 0, 1)) ** 2
        tf = t_arr(0.08)
        out = sweep * 0.3
        add(out, lp_fast(rng.standard_normal(len(tf)), 900) * np.exp(-tf * 50) * 0.5, 0.36)
        return out * 0.5
    if kind == "crayon":  # a wax crayon colouring: short waxy scrubs (0.9 s)
        d = 0.9
        t = t_arr(d)
        n = rng.standard_normal(len(t))
        scrub = np.clip(np.sin(2 * np.pi * 5.5 * t), 0, None) ** 0.8
        return lp_fast(n, 1600) * scrub * env(len(t), 0.02, 0.15) * 0.18
    if kind == "sickle":  # a sickle through a strap: a short whoosh and a snap
        out = np.zeros(int(0.5 * SR))
        tw = t_arr(0.25)
        n = rng.standard_normal(len(tw))
        add(out, (lp_fast(n, 4000) - lp_fast(n, 900)) * np.sin(np.pi * tw / 0.25) ** 2 * 0.5, 0.0)
        ts = t_arr(0.12)
        add(out, (lp_fast(rng.standard_normal(len(ts)), 2500) + osc(160, 0.12) * 0.5) * np.exp(-ts * 55) * 0.9, 0.2)
        return out * 0.6
    if kind == "drip":
        d = 0.18
        t = t_arr(d)
        return np.sin(2 * np.pi * np.cumsum(1400 - 2400 * t) / SR) * np.exp(-t * 40) * 0.3
    if kind == "squelch":  # a foot in mud
        d = 0.35
        t = t_arr(d)
        x = lp_fast(rng.standard_normal(len(t)), 900)
        return (x * 0.8 + np.sin(2 * np.pi * np.cumsum(180 - 120 * t) / SR) * 0.4) * np.exp(-t * 11) * 0.5
    if kind == "rewind":  # tape rewinding: whirring rising pitch + hiss
        d = 1.0
        t = t_arr(d)
        ph = 2 * np.pi * np.cumsum(300 + 2400 * t ** 1.5) / SR
        hiss = rng.standard_normal(len(t))
        return (np.sin(ph) * 0.12 + np.sign(np.sin(ph * 0.5)) * 0.04 + (hiss - lp_fast(hiss, 2000)) * 0.08) * np.sin(np.pi * t / d) ** 0.5
    if kind == "gong":  # โหม่ง of a shadow-puppet band: low gong with a hum and slow decay
        d = 3.2
        t = t_arr(d)
        x = sum(a * np.sin(2 * np.pi * f * t + p) for f, a, p in ((98, 1, 0), (196.8, 0.45, 1), (263, 0.22, 2), (391, 0.12, 0.5)))
        return x * (1 - np.exp(-t * 60)) * np.exp(-t * 1.1) * (1 + 0.15 * np.sin(2 * np.pi * 4 * t)) * 0.35
    if kind == "ching":  # small cymbals
        d = 0.9
        t = t_arr(d)
        hiss = rng.standard_normal(len(t))
        x = osc(3150, d) + 0.7 * osc(4710, d) + 0.5 * osc(6230, d) + (hiss - lp_fast(hiss, 5000)) * 0.4
        return x * np.exp(-t * 6) * 0.12
    if kind == "beep":  # camera record beep
        d = 0.16
        return osc(2600, d) * env(int(d * SR), 0.004, 0.04) * 0.14
    if kind == "squish":  # wet leech
        d = 0.5
        t = t_arr(d)
        x = lp_fast(rng.standard_normal(len(t)), 700)
        return x * (0.5 + 0.5 * np.sin(2 * np.pi * 7 * t)) * np.sin(np.pi * t / d) * 0.45
    if kind == "nv":  # night-vision electronics whine
        d = 3.0
        t = t_arr(d)
        return (osc(7800, d) * 0.02 + osc(120, d, "square") * 0.01) * np.sin(np.pi * t / d) ** 0.3
    if kind == "scream":  # a human scream through a door: gliding buzzy voice with vibrato, muffled
        d = 1.5
        t = t_arr(d)
        f0 = 620 + 380 * np.sin(np.pi * np.clip(t / 1.1, 0, 1)) + 18 * np.sin(2 * np.pi * 6.5 * t)
        ph = 2 * np.pi * np.cumsum(f0) / SR
        v = sum(np.sin(k * ph) / k for k in range(1, 9))
        x = (lp_fast(v, 2600) - lp_fast(v, 450)) * 0.9 + (lp_fast(rng.standard_normal(len(t)), 3000) - lp_fast(rng.standard_normal(len(t)), 800)) * 0.25
        e = np.clip(t / 0.06, 0, 1) * np.exp(-np.clip(t - 0.9, 0, None) * 4)
        return lp_fast(x * e, 1800) * 0.9
    if kind == "growl":  # the infected: low ragged throat noise, pulsing
        d = 1.3
        t = t_arr(d)
        n = rng.standard_normal(len(t))
        am = 0.55 + 0.45 * np.sign(np.sin(2 * np.pi * (28 + 6 * np.sin(2 * np.pi * 1.3 * t)) * t))
        f = 78 + 14 * np.sin(2 * np.pi * 2.1 * t)
        saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
        x = (lp_fast(n, 900) * 1.2 + lp_fast(saw, 700) * 0.8) * am
        e = np.clip(t / 0.15, 0, 1) * np.clip((d - t) / 0.3, 0, 1)
        return x * e * 0.55
    if kind == "tap":  # water running from a tap into a basin
        d = 3.0
        t = t_arr(d)
        n = rng.standard_normal(len(t))
        x = (lp_fast(n, 7000) - lp_fast(n, 1200)) * (0.8 + 0.2 * np.sin(2 * np.pi * 9 * t + np.sin(2 * np.pi * 1.7 * t)))
        return x * np.clip(t / 0.2, 0, 1) * np.clip((d - t) / 0.4, 0, 1) * 0.35
    if kind == "sputter":  # the tap coughing out its last water
        d = 1.0
        t = t_arr(d)
        n = rng.standard_normal(len(t))
        g = sum(np.exp(-((t - c) / 0.035) ** 2) for c in (0.05, 0.2, 0.33, 0.5, 0.62, 0.78))
        return (lp_fast(n, 5000) - lp_fast(n, 900)) * g * 0.5
    if kind == "slam":  # a door slammed shut
        d = 0.7
        t = t_arr(d)
        n = rng.standard_normal(len(t))
        return (lp_fast(n, 400) * 2.4 * np.exp(-t * 14) + osc(58, d) * np.exp(-t * 9) * 0.7 + (lp_fast(n, 6000) - lp_fast(n, 2000)) * np.exp(-t * 60) * 0.6) * 0.8
    if kind == "clang":  # a steel extinguisher hitting a skull: a dull thump with an inharmonic metal ring
        d = 1.4
        t = t_arr(d)
        n = rng.standard_normal(len(t))
        ring = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, a, k in ((523, 0.5, 4.5), (1247, 0.35, 6), (2161, 0.25, 9), (3390, 0.15, 14)))
        return (lp_fast(n, 500) * 2.0 * np.exp(-t * 30) + osc(70, d) * np.exp(-t * 16) * 0.9 + ring * 0.8) * 0.8
    if kind == "shriek":  # the infected screeching: a harsh, gliding, distorted cry
        d = 0.95
        t = t_arr(d)
        f0 = 900 + 500 * np.sin(np.pi * np.clip(t / 0.7, 0, 1)) + 60 * np.sin(2 * np.pi * 23 * t)
        ph = 2 * np.pi * np.cumsum(f0) / SR
        v = np.tanh(3 * sum(np.sin(k * ph) / k for k in range(1, 7)))
        x = (lp_fast(v, 4000) - lp_fast(v, 600)) + (lp_fast(rng.standard_normal(len(t)), 5000) - lp_fast(rng.standard_normal(len(t)), 1500)) * 0.5
        return x * np.clip(t / 0.03, 0, 1) * np.exp(-np.clip(t - 0.55, 0, None) * 7) * 0.55
    if kind == "thud":  # a body hitting the concrete
        d = 0.6
        t = t_arr(d)
        return (osc(48 + 40 * np.exp(-t * 20), d) * 1.1 + lp_fast(rng.standard_normal(len(t)), 250) * 0.8) * np.exp(-t * 10) * 0.9
    if kind == "steps":  # running feet on concrete stairs, seven quick steps
        out = np.zeros(int(1.3 * SR))
        for k in range(7):
            d = 0.09
            t = t_arr(d)
            x = (lp_fast(rng.standard_normal(len(t)), 1800) + osc(90, d) * 0.6) * np.exp(-t * 45)
            add(out, x * (0.7 + 0.3 * (k % 2)), k * 0.17)
        return out
    if kind == "marker":  # a marker squeaking across a mirror: short chirps of a bright, rough tone
        d = 0.45
        t = t_arr(d)
        n = rng.standard_normal(len(t))
        f = 2500 + 700 * np.sin(2 * np.pi * 4.5 * t) + 300 * np.sin(2 * np.pi * 13 * t)
        tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * (lp_fast(n, 60) > 0))
        chirps = np.clip(np.sin(2 * np.pi * 6.5 * t), 0, None) ** 0.5
        return (tone * 0.5 + (lp_fast(n, 6000) - lp_fast(n, 2500)) * 0.5) * chirps * np.clip(t / 0.02, 0, 1) * np.clip((d - t) / 0.05, 0, 1) * 0.35
    if kind == "latch":  # a door latch catching: click then clunk
        out = np.zeros(int(0.4 * SR))
        for off, f, g in ((0.0, 2400, 0.5), (0.06, 180, 0.9)):
            d = 0.08
            t = t_arr(d)
            add(out, (osc(f, d) * 0.6 + lp_fast(rng.standard_normal(len(t)), f * 2) * 0.6) * np.exp(-t * 60) * g, off)
        return out
    if kind == "click":  # a dead lift call button: a dry plastic click and no chime
        d = 0.08
        t = t_arr(d)
        return (osc(1700, d) * 0.4 + (rng.standard_normal(len(t)) - lp_fast(rng.standard_normal(len(t)), 1500)) * 0.6) * np.exp(-t * 110) * 0.5
    if kind == "shatter":  # a mirror bursting: a sharp crack, a noise burst, then a spray of glassy tinkles
        d = 1.2
        t = t_arr(d)
        n = rng.standard_normal(len(t))
        out = (n - lp_fast(n, 3000)) * np.exp(-t * 9) * 0.6
        add(out, lp_fast(rng.standard_normal(int(0.06 * SR)), 900) * np.exp(-t_arr(0.06) * 50) * 1.2, 0.0)
        for k in range(26):
            f, off = 2400 + rng.random() * 5200, 0.02 + rng.random() * 0.8
            dd = 0.08 + rng.random() * 0.12
            add(out, osc(f, dd) * np.exp(-t_arr(dd) * 40) * (0.25 + 0.2 * rng.random()), off)
        return out
    if kind == "powerdown":  # the mains failing: a relay clunk, then the building's hum sliding down and dying
        d = 1.3
        t = t_arr(d)
        ph = 2 * np.pi * np.cumsum(100 * np.exp(-t * 1.8) + 18) / SR
        out = lp_fast(np.sin(ph) * 0.6 + np.sin(2 * ph) * 0.3 + rng.standard_normal(len(t)) * 0.03, 700) * np.exp(-t * 2.2) * 0.45
        tc = t_arr(0.12)
        add(out, (osc(120, 0.12) * 0.8 + lp_fast(rng.standard_normal(len(tc)), 500) * 0.9) * np.exp(-tc * 45), 0.0)
        return out
    raise ValueError(kind)


def main():
    cues = json.load(open(sys.argv[1]))
    dur = cues["duration"]
    bpm = cues.get("bpm", 100)
    buf = np.zeros(int(dur * SR) + SR)
    music = np.zeros_like(buf)
    for s in cues["sections"]:
        render_section(music, s, bpm)
    # 40ms crossfades at section boundaries to avoid clicks
    for s in cues["sections"]:
        for edge in (s["start"], s["end"]):
            i = int(edge * SR)
            w = int(0.04 * SR)
            if 0 < i < len(music) - w:
                music[i - w: i + w] *= np.concatenate([np.linspace(1, 0.4, w), np.linspace(0.4, 1, w)])
    sfxbuf = np.zeros_like(buf)
    for c in cues.get("sfx", []):
        add(sfxbuf, sfx(c["type"]), c["t"], c.get("gain", 1.0))
    # duck music under sfx
    env_s = lp_fast(np.abs(sfxbuf), 8)
    duck = 1 - np.clip(env_s * 2.5, 0, 0.5)
    import os
    if os.environ.get("STEMS"):
        base = sys.argv[2].rsplit(".", 1)[0]
        for name, x in (("music", music), ("sfx", sfxbuf)):
            x = x[: int(dur * SR)].copy()
            n = int(0.8 * SR); x[-n:] *= np.linspace(1, 0, n)
            pk = np.max(np.abs(x)) or 1
            d16 = (np.stack([x / pk * 0.89] * 2, axis=1) * 32767).astype(np.int16)
            with wave.open(f"{base}_{name}.wav", "wb") as w:
                w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d16.tobytes())
        print("stems written"); return
    mix = music * duck * cues.get("music_gain", 1.0) + sfxbuf
    mix = mix[: int(dur * SR)]
    # fade out last 0.8s
    n = int(0.8 * SR)
    mix[-n:] *= np.linspace(1, 0, n)
    peak = np.max(np.abs(mix)) or 1
    mix = np.tanh(mix / peak * 1.4) * 0.89
    stereo = np.stack([mix, mix], axis=1)
    data = (stereo * 32767).astype(np.int16)
    with wave.open(sys.argv[2], "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())
    print("wrote", sys.argv[2], f"{dur}s")


if __name__ == "__main__":
    main()

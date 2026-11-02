# ---- ห้องสอบ no-hiss pass (lane C, 2 Nov 2026 · SKILL A4, owner "ลบเสียงซ่าออก"): exec'd by mix.py after samples_inc.py ----
# no noise bed of any kind: the classroom ambience and the light flicker go; long noisy recordings (shuffling feet, the crowd,
# the desk dragged, the phone buzzing) become separate events of ≤ 0.5 s; every other recorded effect is cut to ≤ 0.5 s
# (a scream / groan, which have a pitch, ≤ 1.0 s); everything recorded is rolled off above ~4.5 kHz, and so is the music bed.
DROP = {"classroom", "flicker"}
CHUNK = {"shuffle": (0.18, 0.5), "crowdwalk": (0.2, 0.6), "deskdrag": (0.45, 0.5), "phonebuzz": (0.4, 0.62), "breath": (0.45, 1.2)}
TONAL = {"scream": 1.0, "groan": 1.0}


def lp45(x, fc=4500.0):
    if len(x) < 16:
        return x
    X = np.fft.rfft(x.astype(np.float64)); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (f / fc) ** 8)
    return np.fft.irfft(X, len(x)).astype(np.float32)


def seg(name, off, ln):
    if name not in _cache:
        _cache[name] = load(os.path.join(SFXLIB, name + ".mp3"))
    x = _cache[name][int(off * SR): int((off + ln) * SR)].copy()
    if len(x) < 32:
        return np.zeros(1, np.float32)
    x = x * (0.12 / (np.sqrt(np.mean(x ** 2)) + 1e-9))
    n = len(x); fi, fo = min(n, int(0.008 * SR)), min(n, int(0.09 * SR))
    x[:fi] *= np.linspace(0, 1, fi); x[n - fo:] *= np.linspace(1, 0, fo)
    return lp45(x)


def nohiss(samples):
    out = []
    for k, t0, name, g, *mx in samples:
        if name in DROP:
            continue
        full = len(load(os.path.join(SFXLIB, name + ".mp3"))) / SR if name not in _cache else len(_cache[name]) / SR
        dur = min(mx[0], full) if mx else full
        if name in CHUNK:
            ln, step = CHUNK[name]
            i = 0
            while i * step < dur - 0.05:
                out.append((k, t0 + i * step, (name, (i * step) % max(0.1, full - ln), min(ln, dur - i * step)), g))
                i += 1
        else:
            out.append((k, t0, (name, 0.0, min(dur, TONAL.get(name, 0.5))), g))
    return out


def place_samples(sfx, samples):
    for k, t0, (name, off, ln), g in nohiss(samples):
        place(sfx, seg(name, off, ln), T(k, t0), g)


def gate(mix, floor_db=-54.0):
    """true silence between events: where the 60 ms level falls under floor_db the mix fades to zero (no hiss in the gaps)"""
    lv = np.sqrt(box(mix.astype(np.float32) ** 2, int(0.06 * SR)) + 1e-12)
    g = np.clip((20 * np.log10(lv) - floor_db) / 6.0, 0, 1)
    return mix * box(g.astype(np.float32), int(0.08 * SR))

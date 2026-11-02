# ---- A5 mix tail (lane C, 2 Nov 2026, owner: "เพลงเบาไม่ได้ยินเหมือนไม่ได้ใส่"): exec'd by mix.py once vo / mus / sfx exist ----
# the theme sits ~6 dB under the voice (duck factor 0.5, 80 ms in / 400 ms back), never gated; only the effects bus is gated;
# one linear gain takes the sum to -14 LUFS so vo_stem.wav / music_stem.wav are exactly what is in mix.wav.
def _lufs(x):
    p = os.path.join(HERE, "_lufs.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", p], input=x.astype(np.float32).tobytes(), check=True)
    o = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", p, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    os.remove(p)
    return float(o.split("Integrated loudness:")[1].split("I:")[1].split("LUFS")[0])


def _wav(name, x):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", "-c:a", "pcm_s16le", os.path.join(HERE, name)],
                   input=x.astype(np.float32).tobytes(), check=True)


def music_mix(vo, mus, sfx, mus_db=-22.0, sfx_db=-27.0, hush=None):
    mus = level(mus, mus_db)
    sfx = gate(sfx if sfx_db is None else level(sfx, sfx_db))
    env = box(np.abs(vo), int(0.03 * SR))
    act = np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1)
    hop = SR // 100
    a = act[::hop]
    g = np.empty(len(a), np.float32)
    cur, ka, kr = 1.0, 1 - np.exp(-1 / (0.08 * 100)), 1 - np.exp(-1 / (0.4 * 100))
    for i, v in enumerate(a):
        tgt = 1 - 0.5 * v
        cur += (tgt - cur) * (ka if tgt < cur else kr)
        g[i] = cur
    duck = np.interp(np.arange(len(vo)), np.arange(len(g)) * hop, g).astype(np.float32)
    mst = mus * duck
    if hush is not None:   # a planned silence beat: everything out (the stems too)
        vo, mst, sfx = vo * hush, mst * hush, sfx * hush
    mix = vo + mst + sfx
    G = 10 ** ((-14.0 - _lufs(mix)) / 20)
    vo, mst, sfx, mix = vo * G, mst * G, sfx * G, mix * G
    lim = 10 ** (-1.6 / 20)   # peak guard: a soft knee only above -1.6 dBFS (after AAC the file stays <= -1 dBTP)
    over = np.abs(mix) > lim
    if over.any():
        m = mix.copy()
        m[over] = np.sign(mix[over]) * (lim + (1 - lim) * np.tanh((np.abs(mix[over]) - lim) / (1 - lim)) * 0.5)
        mix = m
    # 16-bit TPDF dither (±1 LSB ≈ −101 dBFS) on the voice, the same samples in the mix: true silences stay measurable
    rd = np.random.default_rng(29)
    d = ((rd.random(len(vo)) - rd.random(len(vo))) / 32768.0).astype(np.float32)
    vo, mix = vo + d, mix + d
    _wav("vo_stem.wav", vo)
    _wav("music_stem.wav", mst)
    _wav("sfx_stem.wav", sfx)
    _wav("mix.wav", mix)
    return mix


def ride(mus, win=1.5, lo=0.4, hi=3.0):
    """a slow level ride on the theme (≈1.5 s): its loud and quiet passages land near one level, so the duck sets the gap"""
    e = np.sqrt(np.maximum(box(mus.astype(np.float32) ** 2, int(win * SR)), 0) + 1e-10)
    ref = np.median(e[e > 1e-4]) if (e > 1e-4).any() else 1.0
    g = np.clip(ref / e, lo, hi)
    return (mus * box(g.astype(np.float32), int(0.5 * SR))).astype(np.float32)

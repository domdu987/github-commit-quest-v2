#!/usr/bin/env python3
"""gen_tex.py : textures of the office light extension (no bpy, numpy + PIL only, deterministic).

    python3 gen_tex.py            # writes tex/sky_grey.png, tex/sky_storm.png, tex/rain_drizzle/r_0001..0096.png, tex/rain_lash/r_0001..0096.png

Sky cards: the set's own sky.png (same roofline, same layout) re-coloured to an overcast drizzle sky and to a storm sky.
Rain cards: a seamless 96-frame loop (3.2 s at 30 fps) of water on the glass, RGBA, 128 px per D over the glazing
(5.98 x 4.72 D -> 768 x 608 px).  drizzle: beads that sit, and drops that slide down in stick-slip steps leaving a wet trail.
lash: the same plus dense fast streaks driven slantwise by the wind and running sheets."""
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SET = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'set3d')
TEX = os.path.join(HERE, 'tex')
NF = 96                      # loop length in frames
W, H = 768, 608              # rain card pixels (glazing 5.98 x 4.72 D)
SS = 2                       # supersampling for the drawing


def _srgb(a): return np.clip(a, 0, 1)


def _lit_panes(mask, share, seed):
    """connected 4-neighbour components of mask (window panes); a random share of them, whole, is returned as lit."""
    h, w = mask.shape; lab = np.zeros((h, w), np.int32); n = 0
    for y0, x0 in zip(*np.nonzero(mask)):
        if lab[y0, x0]: continue
        n += 1; st = [(y0, x0)]; lab[y0, x0] = n
        while st:
            y, x = st.pop()
            for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= yy < h and 0 <= xx < w and mask[yy, xx] and not lab[yy, xx]: lab[yy, xx] = n; st.append((yy, xx))
    on = np.random.default_rng(seed).random(n + 1) < share; on[0] = False
    return on[lab]


def skies():
    src = np.asarray(Image.open(os.path.join(SET, 'tex', 'sky.png')).convert('RGB'), dtype=np.float32) / 255
    h, w, _ = src.shape
    lum = src @ np.array([0.30, 0.55, 0.15], np.float32)
    yy = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    rng = np.random.default_rng(7)
    # soft, low cloud mass: blurred noise, horizontally stretched
    c0 = w // 6; n = rng.random((h // 18 + 2, c0)).astype(np.float32)
    n3 = np.concatenate([n, n, n, n[:, :1]], 1)                # the card repeats the texture 3 times across: the clouds must tile
    big = np.asarray(Image.fromarray((n3 * 255).astype(np.uint8)).resize((3 * w + w // c0, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(14)), np.float32) / 255
    n = big[:, w:2 * w]
    n = (n - n.mean()) / (n.std() + 1e-6)
    dark = (lum < 0.62) & (yy > 0.45)                        # roofline silhouettes of the original (darker blue blocks in the lower half)
    top_row = np.where(dark.any(0), dark.argmax(0), h)        # first roof pixel of every column: everything below it is building
    roof = (np.arange(h)[:, None] >= top_row[None, :]).astype(np.float32)
    win = (roof > 0) & (lum < np.percentile(lum[roof > 0], 30)) # the original's window panes, kept as darker cells
    solid = win.sum(0) > 0.6 * np.maximum(roof.sum(0), 1)       # a whole dark building is not a window
    win &= ~solid[None, :]
    lit = _lit_panes(win, 0.45, 3)
    out = {}
    # overcast drizzle: pale blue-grey (never neutral), lighter toward the horizon, clouds barely modelled; roofs a soft slate
    top, bot = np.array([0.56, 0.60, 0.70], np.float32), np.array([0.74, 0.76, 0.82], np.float32)
    sk = top * (1 - yy[..., None]) + bot * yy[..., None]
    sk = sk * (1 + 0.025 * n[..., None])
    rf = np.array([0.40, 0.44, 0.56], np.float32) * (0.92 + 0.16 * (lum[..., None] / max(lum.max(), 1e-6)))
    rf = np.where(win[..., None], rf * 0.80, rf)
    out['sky_grey'] = sk * (1 - roof[..., None]) + rf * roof[..., None]
    # storm: deep slate-violet, a darker band of cloud, roofs near-navy silhouettes
    top, bot = np.array([0.16, 0.17, 0.27], np.float32), np.array([0.30, 0.31, 0.42], np.float32)
    sk = top * (1 - yy[..., None]) + bot * yy[..., None]
    sk = sk * (1 + 0.10 * n[..., None])
    rf = np.array([0.09, 0.10, 0.17], np.float32) * np.ones_like(sk)
    rf = np.where(win[..., None], np.array([0.13, 0.13, 0.21], np.float32), rf)
    rf = np.where(lit[..., None], np.array([0.42, 0.33, 0.16], np.float32), rf)   # about half the window panes glow a dull lamp yellow
    out['sky_storm'] = sk * (1 - roof[..., None]) + rf * roof[..., None]
    for k, v in out.items():
        Image.fromarray((_srgb(v) * 255 + 0.5).astype(np.uint8)).save(os.path.join(TEX, k + '.png'))
    return out


def _bead(dr, x, y, r, a=1.0, hi=(236, 242, 252), rim=(24, 28, 46)):
    """one water bead on glass, refracting the sky: dark rim at the bottom, bright cap with a specular dot (SS pixel units)."""
    dr.ellipse([x - r, y - r * 1.08, x + r, y + r * 1.08], fill=rim + (int(150 * a),))
    dr.ellipse([x - r * 0.82, y - r * 0.98, x + r * 0.82, y + r * 0.62], fill=hi + (int(120 * a),))
    s = max(1.0, r * 0.28)
    dr.ellipse([x - r * 0.35 - s, y - r * 0.55 - s, x - r * 0.35 + s, y - r * 0.55 + s], fill=(255, 255, 255, int(230 * a)))


def rain(kind, seed):
    """96 RGBA frames.  Positions are exact functions of the frame phase u = f / NF, so frame NF + 1 equals frame 1."""
    rnd = random.Random(seed)
    Ws, Hs = W * SS, H * SS
    beads = [(rnd.uniform(0, Ws), rnd.uniform(0, Hs), rnd.uniform(1.6, 4.2) * SS) for _ in range(260 if kind == 'drizzle' else 420)]
    sliders = []
    for i in range(26 if kind == 'drizzle' else 30):
        sliders.append(dict(x=rnd.uniform(0.02, 0.98) * Ws, s0=rnd.uniform(0, 1), k=rnd.choice((1, 1, 2)) if kind == 'drizzle' else rnd.choice((2, 3, 3, 4)),
                            r=rnd.uniform(3.6, 6.4) * SS, wig=rnd.uniform(4, 14) * SS, wf=rnd.uniform(1.5, 4.0), ph=rnd.uniform(0, 6.3),
                            m=rnd.choice((3, 4, 5)), a=rnd.uniform(0.55, 0.85), trail=rnd.uniform(0.18, 0.45)))
    streaks = []
    if kind == 'lash':                                       # wind-driven rain hitting the glass: short slanted streaks, many
        for i in range(170):
            streaks.append(dict(x=rnd.uniform(-0.2, 1.0) * Ws, y=rnd.uniform(0, 1) * Hs, k=rnd.choice((6, 8, 10, 12)), L=rnd.uniform(26, 70) * SS,
                                a=rnd.uniform(0.25, 0.6)))
    frames = []
    for f in range(NF):
        u = f / NF
        im = Image.new('RGBA', (Ws, Hs), (0, 0, 0, 0)); dr = ImageDraw.Draw(im, 'RGBA')
        # wet film: a faint cool sheen in the lower part where the water collects
        for b in beads: _bead(dr, b[0], b[1], b[2], 0.55)
        for s in sliders:
            # stick-slip: g(u) = u - sin(2 pi m u) / (2 pi m) has speed 0 at the stops and g(1) = 1, so the loop closes
            def pos(uu):
                g = uu - math.sin(2 * math.pi * s['m'] * uu) / (2 * math.pi * s['m'])
                return ((s['s0'] + s['k'] * g) % 1.0) * (Hs + 120 * SS) - 60 * SS
            y = pos(u)
            xs = lambda yy: s['x'] + s['wig'] * math.sin(yy / Hs * s['wf'] * 2 * math.pi + s['ph'])
            # trail: the path the drop has just run along, a thin wet line that fades upward
            tl = s['trail'] * Hs; n = 22
            pts = [(xs(y - tl * j / n), y - tl * j / n) for j in range(n + 1)]
            for j in range(n):
                a = (1 - j / n) * 0.75 * s['a']
                dr.line([pts[j], pts[j + 1]], fill=(30, 34, 52, int(120 * a)), width=max(1, int(s['r'] * 0.55)))
                dr.line([(pts[j][0] - s['r'] * 0.18, pts[j][1]), (pts[j + 1][0] - s['r'] * 0.18, pts[j + 1][1])], fill=(230, 236, 248, int(110 * a)), width=max(1, int(s['r'] * 0.22)))
            _bead(dr, xs(y), y, s['r'], s['a'])
        for s in streaks:
            y = (s['y'] + s['k'] * u * Hs) % (Hs + s['L']) - s['L']
            x = (s['x'] + 0.35 * s['k'] * u * Hs) % (Ws * 1.2) - 0.1 * Ws
            dr.line([(x, y), (x + 0.35 * s['L'], y + s['L'])], fill=(222, 230, 246, int(255 * s['a'])), width=int(1.4 * SS))
        im = im.resize((W, H), Image.LANCZOS)
        frames.append(im)
    d = os.path.join(TEX, 'rain_' + kind); os.makedirs(d, exist_ok=True)
    for i, im in enumerate(frames): im.save(os.path.join(d, 'r_%04d.png' % (i + 1)))
    return d


if __name__ == '__main__':
    os.makedirs(TEX, exist_ok=True)
    skies(); print('skies done')
    print(rain('drizzle', 11)); print(rain('lash', 23))

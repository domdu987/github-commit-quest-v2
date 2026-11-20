"""jimo_dress.py : ground dressing for the film-18 set (API.md, "Ground dressing (render teams: call this)").

    J.dress_ground(cam=None, density=1.0, seed=0, keep_clear=None, frames=None, actors=None)   scatter a few warm, textured, rounded ground props where the camera sees the ground, clear of the actors
    J.ground_share(png)                                                           share of "plain ground" blocks in a rendered frame (0..1)

Pure helpers (no bpy at import time) so `ground_share` also runs from a bare python: `python3 jimo_dress.py share a.png b.png`.
Everything the scatter builds is named `dg_*` (objects) / `dgm_*` (meshes) and is removed again by `clear_dressing()` or by the next `dress_ground()` call."""
import math, random, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
J = None                                                           # the jimo module (bound lazily: this file must import without bpy)
bpy = None; V = None
def _bind():
    global J, bpy, V
    if J is None:
        if HERE not in sys.path: sys.path.insert(0, HERE)
        import bpy as _b
        from mathutils import Vector
        import jimo as _j
        bpy, V, J = _b, Vector, _j

# ============================================================================= ground_share
GS_WIDTH = 360          # every frame is resized to 360 px wide first (a 720 x 1280 final and a 360 x 640 draft are then measured alike)
GS_BLOCK = 24           # block edge in px at that width
GS_SIGMA = 1.5          # Gaussian blur before the Laplacian: renders at 6 / 12 samples, OIDN blotches and h264 blocks stop counting as texture
GS_THR = 1.5            # Laplacian variance (0..255 grey) under which a block is "plain"; calibrated on the s20 take (6 frames, mean 0.40, range 0.29-0.47)
GS_FROM = 0.4           # only blocks whose top edge is below 0.4 H

def ground_share(png, thr=GS_THR, detail=False):
    """Share of "plain ground" in a rendered frame: the fraction of 24 x 24 px blocks (frame resized to 360 px wide) below y = 0.4 H whose Laplacian variance
    (after a 1.5 px Gaussian) is under `thr`. 0.38-0.42 = the bare s20 take, 0.25 or less = a well dressed frame. `png` = path, PIL image or an (H, W[, 3]) array.
    detail=True returns dict(share, blocks, plain, mask) with mask[row, col] True where plain (rows start at y = 0.4 H)."""
    from PIL import Image, ImageFilter
    if isinstance(png, np.ndarray): im = Image.fromarray(png.astype(np.uint8))
    elif isinstance(png, (str, os.PathLike)): im = Image.open(png)
    else: im = png
    im = im.convert('L'); H = int(round(GS_WIDTH * im.height / im.width)); im = im.resize((GS_WIDTH, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(GS_SIGMA))
    a = np.asarray(im, np.float32)
    lap = np.pad(-4 * a[1:-1, 1:-1] + a[:-2, 1:-1] + a[2:, 1:-1] + a[1:-1, :-2] + a[1:-1, 2:], 1)
    y0 = int(GS_FROM * H); rows = list(range(y0, H - GS_BLOCK + 1, GS_BLOCK)); cols = list(range(0, GS_WIDTH - GS_BLOCK + 1, GS_BLOCK))
    mask = np.array([[lap[y:y + GS_BLOCK, x:x + GS_BLOCK].var() < thr for x in cols] for y in rows])
    share = float(mask.mean()) if mask.size else 0.0
    return dict(share=share, blocks=int(mask.size), plain=int(mask.sum()), mask=mask) if detail else share


# ============================================================================= materials: warm earth tones, textured, shade side only slightly violet
TAU = 2 * math.pi
TEXV = 'dg2'
SHADE_TGT = (0.50, 0.40, 0.46)          # target ambient (shade side) multiplier of the art: warm brown with a touch of violet, never the navy of the set's SHADE
SHADE_WARM = (0.62, 0.42, 0.28)         # inside a fire's warm radius: ochre shade

def _tex(name):
    """Small seamless painted textures for the props (stone, straw, grass-straw, clay), made once into tex_jimo/dg2_<name>.png."""
    import jimo_tex as JX
    path = os.path.join(JX.TEX, '%s_%s.png' % (TEXV, name))
    if os.path.exists(path): return path
    os.makedirs(JX.TEX, exist_ok=True); n = 160; H = JX.hexf
    if name == 'stone':
        a, b = H('#a8865c'), H('#7a5a3a'); t = JX.fbm(n, n, 20, 3, 4); t = (t - t.min()) / (np.ptp(t) + 1e-6)
        col = JX.lerp(b, a, t[..., None]); sp = JX.fbm(n, n, 6, 9, 3); col = col * (0.88 + 0.24 * sp[..., None]); pits = JX.vn(n, n, 5, 21) > 0.82; col[pits] *= 0.78
        veins = JX.fbm(n, n, (3, 40), 5, 2); col = col * (0.94 + 0.12 * veins[..., None])
    elif name == 'straw':
        a, b = H('#c49a48'), H('#8c6a30'); t = JX.fbm(n, n, (2, 32), 4, 4); t = (t - t.min()) / (np.ptp(t) + 1e-6); col = JX.lerp(b, a, t[..., None]); col = col * (0.9 + 0.2 * JX.fbm(n, n, (8, 8), 7, 2)[..., None])
    elif name == 'grass':
        a, b = H('#9a9044'), H('#6c6a32'); t = JX.fbm(n, n, (2, 32), 14, 4); t = (t - t.min()) / (np.ptp(t) + 1e-6); col = JX.lerp(b, a, t[..., None]); col = col * (0.9 + 0.2 * JX.fbm(n, n, (8, 8), 17, 2)[..., None])
    else:   # clay
        a, b = H('#b06a42'), H('#80472c'); t = JX.fbm(n, n, 16, 6, 4); t = (t - t.min()) / (np.ptp(t) + 1e-6); col = JX.lerp(b, a, t[..., None]); col = col * (0.92 + 0.16 * JX.fbm(n, n, 5, 8, 2)[..., None])
    JX.save(col.astype('float32'), path); return path

def _pal(tone):
    """tone = (warm, dim): warm = fire-lit hue (ochre shade), dim = caption band (no bright pixel)."""
    S = J.STATE; P = S['P']; FORM = tuple(P['form']); tx = S['tx']; warm, dim = tone
    k = 0.8 if dim else 1.0; tgt = SHADE_WARM if warm else SHADE_TGT
    sm = tuple(max(0.2, t * k / max(1e-3, s)) for t, s in zip(tgt, P['shade']))
    pre = S['pre'] + TEXV + '%d%d_' % (1 if warm else 0, 1 if dim else 0)
    def mk(n, g, **kw):
        return J._untoon(J.mat_lit(pre + n, gain=g * k, shade_mul=sm, form=FORM, shade_mix=0.0, **kw))
    def C(h, g=1.0): return mk('c_%s_%g' % (h.lstrip('#'), g), g, color=h)
    def TX(n, g=1.0): return mk('t_%s_%g' % (n, g), g, image=tx[n])
    def PT(n, g=1.0): return mk('p_%s_%g' % (n, g), g, image=_tex(n))
    m = dict(straw=PT('straw', 0.85), straw_d=PT('straw', 0.62), hay=PT('straw', 0.74), grass=PT('grass', 0.8), grass_d=PT('grass', 0.6), reed=PT('grass', 0.8),
             stone=PT('stone', 0.95), stone_d=PT('stone', 0.72), wood=C('#7a5232', 1.0), wood_d=C('#56391f', 1.0), wood_l=C('#b08a58', 0.95), clay=PT('clay', 0.95), clay_d=PT('clay', 0.7),
             iron=C('#6a5a4a', 1.0), sack=TX('canvas', 0.8), sack_d=TX('canvas', 0.6), red=C('#9a3426', 1.0), leaf=C('#4c6a34', 0.95), leaf2=C('#7a7a38', 0.95), thatch=C('#8a6c34', 0.95),
             plaster=C('#b09a74', 0.9), rope=C('#8e7048', 0.95), black=C('#2a2220', 1.0), bronze=C('#9a7038', 1.0),
             earth=TX('earth', 0.8), earth_d=TX('bank', 0.7), planks=TX('planks_d', 1.2), hide=TX('hide', 0.8), grass_t=TX('grass', 0.8), grass2_t=TX('grass2', 0.8))
    return m

# ============================================================================= the mesh library (origin = foot, +z up, 1 D = one head). Soft, rounded, textured; no blades, no flat decals.
def _mb(): return J.MB()
def _tilt(mb, ax, ang, shift=(0, 0, 0)):
    from mathutils import Matrix
    R = Matrix.Rotation(ang, 3, ax); mb.v = [tuple(R @ V(v) + V(shift)) for v in mb.v]

def b_tuft(mb, m, r, kind='straw', flat=False):
    """A soft clump of straw / dry grass: 3-5 overlapping smooth rounded lumps, wider than tall, warm straw colour (no blades)."""
    mats = (m['straw'], m['hay'], m['straw_d']) if kind == 'straw' else (m['grass'], m['straw'], m['grass_d'])
    n = r.randint(3, 5)
    for i in range(n):
        a = r.uniform(0, TAU); d = r.uniform(0.0, 0.3) if i else 0.0; rr = r.uniform(0.24, 0.38) * (1.0 if i else 1.2)
        J.lumpy(mb, V((d * math.cos(a), d * math.sin(a), rr * (0.28 if flat else 0.4))), rr, mats[i % 3], r.randint(1, 99), seg=10, rings=6, rough=0.16, squash=0.38 if flat else 0.62)
    return 0.55

def b_reeds(mb, m, r):
    """A tied straw sheaf: a soft tapering bundle with a rope band (replaces the old reed blades)."""
    h = r.uniform(1.0, 1.4)
    mb.frustum(V((0, 0, 0)), V((0.0, 0.0, h)), 0.34, 0.2, m['straw'], seg=10, cap0=True, cap1=False); J.lumpy(mb, V((0, 0, h)), 0.26, m['hay'], r.randint(1, 99), seg=10, rings=5, rough=0.14, squash=0.8)
    mb.frustum(V((0, 0, h * 0.45)), V((0, 0, h * 0.45 + 0.09)), 0.31, 0.31, m['rope'], seg=10, cap0=False, cap1=False)
    return 0.5

def b_hay(mb, m, r):
    """A straw heap: a big smooth mound with two lower lobes."""
    J.lumpy(mb, V((0, 0, 0.1)), 0.85, m['hay'], r.randint(1, 99), seg=14, rings=8, rough=0.12, squash=0.62)
    for i in range(2):
        a = r.uniform(0, TAU); J.lumpy(mb, V((0.7 * math.cos(a), 0.7 * math.sin(a), 0.08)), r.uniform(0.38, 0.5), m['straw'] if i else m['hay'], r.randint(1, 99), seg=10, rings=6, rough=0.14, squash=0.6)
    return 1.1

def b_stone(mb, m, r, cluster=False):
    """Smooth rounded boulders (river-stone) in ochre / brown, with a texture."""
    if not cluster:
        rr = r.uniform(0.3, 0.5); J.lumpy(mb, V((0, 0, rr * 0.5)), rr, r.choice((m['stone'], m['stone_d'])), r.randint(1, 99), seg=14, rings=9, rough=0.09, squash=0.7)
        return rr * 1.1
    J.lumpy(mb, V((0, 0, 0.26)), 0.5, m['stone'], r.randint(1, 99), seg=14, rings=9, rough=0.1, squash=0.66)
    for q in range(2): a = r.uniform(0, TAU); d = r.uniform(0.55, 0.8); rr = r.uniform(0.2, 0.3); J.lumpy(mb, V((d * math.cos(a), d * math.sin(a), rr * 0.5)), rr, r.choice((m['stone'], m['stone_d'])), r.randint(1, 99), seg=12, rings=7, rough=0.09, squash=0.7)
    return 0.95

def b_basket(mb, m, r, tipped=False):
    mb.frustum(V((0, 0, 0)), V((0, 0, 0.72)), 0.34, 0.54, m['straw_d'], seg=12, cap0=True, cap1=False)
    J.cyl(mb, V((0, 0, 0.64)), 0.55, 0.1, m['wood_d'], seg=12, r1=0.55); J.cyl(mb, V((0, 0, 0.3)), 0.43, 0.07, m['straw'], seg=12, r1=0.43)
    if not tipped: J.lumpy(mb, V((0, 0, 0.72)), 0.46, m['hay'], r.randint(1, 99), seg=10, rings=5, rough=0.12, squash=0.5)         # heaped straw / grain
    if tipped: _tilt(mb, 'Y', 1.45, (0.0, 0.0, 0.5))
    return 0.6

def b_sack(mb, m, r, pile=False, lying=False):
    def one(c, s):
        J.lumpy(mb, c + V((0, 0, 0.36 * s)), 0.44 * s, m['sack'], r.randint(1, 99), seg=12, rings=7, rough=0.1, squash=0.82)
        mb.frustum(c + V((0, 0, 0.7 * s)), c + V((0.03, 0.02, 0.88 * s)), 0.15 * s, 0.1 * s, m['sack_d'], seg=8)
    if pile: one(V((-0.4, 0, 0)), 1.0); one(V((0.42, 0.1, 0)), 0.95); one(V((0.02, 0.05, 0.62)), 0.9)
    else: one(V((0, 0, 0)), r.uniform(0.9, 1.2))
    if lying: _tilt(mb, 'Y', 1.3, (0.3, 0, 0.42))
    return 1.0 if pile else 0.55

def b_cart(mb, m, r, loaded=False):
    Rw = 0.95; z0 = Rw * 0.95
    J.obox(mb, V((0, 0, z0)), (1, 0, 0), (0, 1, 0), (0, 0, 1), 1.3, 0.78, 0.07, m['planks'], uvk=0.5)
    for sy in (-1, 1):
        J.obox(mb, V((0, sy * 0.78, z0 + 0.3)), (1, 0, 0), (0, 1, 0), (0, 0, 1), 1.3, 0.05, 0.28, m['planks'], uvk=0.5)
        J.rod(mb, V((-1.3, sy * 0.5, z0 + 0.05)), V((-3.1, sy * 0.45, 0.28)), 0.07, m['wood'], seg=5)              # shafts, resting on the ground
        a0 = V((0, sy * 0.95, z0))
        for q in range(14):
            t0, t1 = TAU * q / 14, TAU * (q + 1) / 14
            J.rod(mb, a0 + V((Rw * math.cos(t0), 0, Rw * math.sin(t0))), a0 + V((Rw * math.cos(t1), 0, Rw * math.sin(t1))), 0.11, m['wood_d'], seg=5)
        for q in range(4):
            t0 = math.pi * q / 4; J.rod(mb, a0 + V((Rw * math.cos(t0), 0, Rw * math.sin(t0))), a0 - V((Rw * math.cos(t0), 0, Rw * math.sin(t0))), 0.07, m['wood'], seg=5)
        J.rod(mb, a0 + V((0, -0.12, 0)), a0 + V((0, 0.12, 0)), 0.15, m['wood'], seg=8)
    J.rod(mb, V((0, -1.0, z0)), V((0, 1.0, z0)), 0.07, m['wood_d'], seg=5)
    J.obox(mb, V((1.3, 0, z0 + 0.3)), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.04, 0.78, 0.28, m['planks'], uvk=0.5)
    if loaded:
        for q in range(3): J.lumpy(mb, V((-0.7 + 0.7 * q, r.uniform(-.2, .2), z0 + 0.5)), 0.5, m['sack'] if q % 2 else m['hay'], r.randint(1, 99), seg=10, rings=6, rough=0.1, squash=0.8)
    return 1.9

def b_firewood(mb, m, r):
    for lay, (ys, z) in enumerate((((-0.5, 0.0, 0.5), 0.13), ((-0.25, 0.25), 0.36), ((0.0,), 0.58))):
        for i, y in enumerate(ys):
            L = r.uniform(1.3, 1.7); x0 = -L / 2 + r.uniform(-.1, .1)
            mb.frustum(V((x0, y, z)), V((x0 + L, y + r.uniform(-.05, .05), z)), 0.13, 0.12, m['wood'] if (i + lay) % 2 else m['wood_d'], seg=8, cap_mat=m['wood_l'])
    return 1.0

def b_arrows(mb, m, r):
    for q in range(r.randint(3, 4)):
        a = r.uniform(0, TAU); d = r.uniform(0.0, 0.8); p = V((d * math.cos(a), d * math.sin(a), 0.05)); dd = V((math.cos(a + 1.2), math.sin(a + 1.2), 0.0))
        tip = p; top = p + dd * r.uniform(1.4, 2.0) + V((0, 0, 0.05)); J.rod(mb, tip, top, 0.045, m['wood_l'], seg=5)
        u = (top - tip).normalized(); J.rod(mb, tip, tip + u * 0.2, 0.07, m['iron'], seg=5, r1=0.0)
    return 1.0

def b_mat(mb, m, r, two=False):
    for k in range(2 if two else 1):
        y = 0.0 if not two else (-0.26 if k == 0 else 0.26); z = 0.24
        mb.frustum(V((-0.85, y, z)), V((0.85, y, z)), 0.24, 0.24, m['straw'], seg=10, cap_mat=m['straw_d'])
        for x in (-0.5, 0.5): mb.frustum(V((x - 0.04, y, z)), V((x + 0.04, y, z)), 0.265, 0.265, m['rope'], seg=10, cap0=False, cap1=False)
    return 1.0

def b_rope(mb, m, r):
    for i, (R, z) in enumerate(((0.5, 0.07), (0.4, 0.17), (0.3, 0.26))):
        n = 14
        for q in range(n):
            a0, a1 = TAU * q / n, TAU * (q + 1) / n; J.rod(mb, V((R * math.cos(a0), R * math.sin(a0), z)), V((R * math.cos(a1), R * math.sin(a1), z)), 0.085, m['rope'], seg=5)
    J.rod(mb, V((0.5, 0, 0.07)), V((1.1, 0.35, 0.06)), 0.07, m['rope'], seg=5)
    return 0.8

def b_helmet(mb, m, r, side=False):
    J.ellipsoid(mb, V((0, 0, 0.0)), 0.44, 0.4, 0.42, m['iron'], seg=12, rings=6, th=(math.pi / 2, math.pi))
    J.cyl(mb, V((0, 0, 0.0)), 0.47, 0.07, m['bronze'], seg=12, r1=0.47)
    mb.frustum(V((0, 0, 0.4)), V((0.05, 0, 0.62)), 0.07, 0.04, m['red'], seg=6)
    if side: _tilt(mb, 'Y', 1.2, (0.15, 0, 0.42))
    return 0.5

def b_jar(mb, m, r, tipped=False):
    """A water jar (belly + neck + rim + a band)."""
    J.ellipsoid(mb, V((0, 0, 0.55)), 0.52, 0.52, 0.58, m['clay'], seg=14, rings=8, rough=0.03, seed=r.randint(1, 50))
    J.cyl(mb, V((0, 0, 1.0)), 0.3, 0.3, m['clay_d'], seg=12, r1=0.34); J.cyl(mb, V((0, 0, 1.28)), 0.38, 0.08, m['clay'], seg=12, r1=0.38)
    J.cyl(mb, V((0, 0, 0.62)), 0.54, 0.07, m['clay_d'], seg=14, r1=0.54)
    if tipped: _tilt(mb, 'Y', 1.35, (0.35, 0, 0.55))
    return 0.6

# ---- vista (units are D but the pieces are big: they are scaled again by the distance in the placer)
def b_hedge(mb, m, r):
    n = r.randint(9, 14); y = 0.0
    for i in range(n):
        y += r.uniform(-0.25, 0.25); rr = r.uniform(1.3, 1.9)
        J.lumpy(mb, V((i * 1.9, y, rr * 0.5)), rr, m['leaf'] if i % 3 else m['leaf2'], r.randint(1, 99), seg=10, rings=5, rough=0.2, squash=0.75)
    return n * 0.95

def b_trees(mb, m, r):
    for i in range(r.randint(4, 7)):
        a = r.uniform(0, TAU); d = r.uniform(0, 3.2); p = V((d * math.cos(a), d * math.sin(a), 0)); h = r.uniform(2.6, 4.2)
        mb.frustum(p, p + V((0, 0, h)), 0.32, 0.2, m['wood_d'], seg=6)
        for q in range(2): J.lumpy(mb, p + V((0, 0, h + 0.4 + q * 1.4)), 2.0 - 0.5 * q, m['leaf'] if (i + q) % 2 else m['leaf2'], r.randint(1, 99), seg=9, rings=5, rough=0.2, squash=0.8)
    return 4.0

def b_haystack(mb, m, r):
    mb.frustum(V((0, 0, 0)), V((0, 0, 2.6)), 2.5, 1.5, m['hay'], seg=12)
    mb.frustum(V((0, 0, 2.6)), V((0, 0, 4.0)), 1.5, 0.0, m['straw'], seg=12, cap0=False)
    mb.frustum(V((0, 0, 0.9)), V((0, 0, 1.1)), 2.35, 2.35, m['straw_d'], seg=12, cap0=False, cap1=False)
    J.rod(mb, V((0, 0, 3.9)), V((0, 0, 5.0)), 0.1, m['wood_d'], seg=5, r1=0.04)
    return 2.6

def b_ridge(mb, m, r):
    n = r.randint(10, 18); y = 0.0
    for i in range(n):
        y += r.uniform(-0.3, 0.3); J.lumpy(mb, V((i * 2.2, y, 0.25)), 1.5, m['earth_d'] if i % 2 else m['grass_t'], r.randint(1, 99), seg=10, rings=5, rough=0.15, squash=0.34)
    return n * 1.1

def b_hut(mb, m, r):
    w, d, h = 3.0, 2.4, 2.6
    J.obox(mb, V((0, 0, h / 2)), (1, 0, 0), (0, 1, 0), (0, 0, 1), w, d, h / 2, m['plaster'], uvk=0.3)
    rz = h + 2.4
    e = [V((-w - 0.5, -d - 0.5, h)), V((w + 0.5, -d - 0.5, h)), V((w + 0.5, d + 0.5, h)), V((-w - 0.5, d + 0.5, h))]; rg = [V((-w * 0.5, 0, rz)), V((w * 0.5, 0, rz))]
    for pts, nrm in (([e[0], e[1], rg[1], rg[0]], (0, -1, 1)), ([e[2], e[3], rg[0], rg[1]], (0, 1, 1)), ([e[1], e[2], rg[1]], (1, 0, 1)), ([e[3], e[0], rg[0]], (-1, 0, 1))):
        mb.oface(pts, m['thatch'], [(0, 0), (1, 0), (1, 1), (0, 1)][:len(pts)], nrm)
    mb.oface([V((-0.6, -d - 0.02, 0.0)), V((0.6, -d - 0.02, 0.0)), V((0.6, -d - 0.02, 1.8)), V((-0.6, -d - 0.02, 1.8))], m['black'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
    return 3.6

# kind -> (builder, variants, kwargs per variant, [unused decal flag], base size D, height D). No ruts / puddles / shards: nothing flat, nothing dark.
LIB = dict(
    tuft_straw=(b_tuft, [dict(kind='straw'), dict(kind='straw', flat=True), dict(kind='straw')], 0, 0.55, 0.5),
    tuft_grass=(b_tuft, [dict(kind='grass'), dict(kind='grass', flat=True), dict(kind='grass')], 0, 0.55, 0.5),
    tuft_trample=(b_tuft, [dict(kind='grass', flat=True), dict(kind='straw', flat=True), dict(kind='grass', flat=True)], 0, 0.55, 0.35),
    reeds=(b_reeds, [{}, {}, {}], 0, 0.5, 1.4),
    hay=(b_hay, [{}, {}, {}], 0, 1.1, 0.8),
    stone=(b_stone, [{}, {}, dict(cluster=True)], 0, 0.5, 0.5),
    rock=(b_stone, [dict(cluster=True), {}, dict(cluster=True)], 0, 0.9, 0.6),
    basket=(b_basket, [{}, dict(tipped=True), {}], 0, 0.6, 0.75),
    sack=(b_sack, [{}, dict(pile=True), dict(lying=True)], 0, 0.8, 0.8),
    cart=(b_cart, [{}, dict(loaded=True)], 0, 1.9, 2.2),
    firewood=(b_firewood, [{}, {}], 0, 1.0, 0.8),
    arrows=(b_arrows, [{}, {}, {}], 0, 1.0, 0.3),
    mat=(b_mat, [{}, dict(two=True)], 0, 1.0, 0.5),
    rope=(b_rope, [{}, {}], 0, 0.8, 0.3),
    helmet=(b_helmet, [{}, dict(side=True), {}], 0, 0.5, 0.6),
    jar=(b_jar, [{}, dict(tipped=True), {}], 0, 0.6, 1.3),
    hedge=(b_hedge, [{}, {}, {}], 0, 11.0, 2.5),
    trees=(b_trees, [{}, {}, {}], 0, 4.5, 8.0),
    haystack=(b_haystack, [{}, {}], 0, 2.6, 5.0),
    ridge=(b_ridge, [{}, {}, {}], 1, 12.0, 0.6),
    hut=(b_hut, [{}, {}], 0, 3.8, 5.0),
)
GAIN = dict(tuft_straw=1.3, tuft_grass=1.3, tuft_trample=1.3, hay=1.15, jar=1.1, sack=1.1, basket=1.15, cart=1.1)     # larger, more recognisable pieces
NOSHADOW = ('ridge',)
SMOOTH = ('tuft_straw', 'tuft_grass', 'tuft_trample', 'reeds', 'hay', 'stone', 'rock', 'basket', 'sack', 'jar', 'helmet', 'hedge', 'trees', 'ridge', 'haystack')
DENSITY0 = 0.4                            # density 1.0 = 40 % of the old (v1) helper's candidate grid: few, larger, recognisable props
LENS_CLEAR = 3.0                          # D: nothing (prop surface) closer than this to the lens at ANY keyed pose
ACTOR_CLEAR = 2.5                         # D: default radius round every actor mark

WEIGHTS = dict(     # the recognisable ones: cart, sacks, basket, straw heap, water jar; stones and tufts are filler
    jimo_in=dict(tuft_straw=4, tuft_grass=1.5, hay=6, stone=3, basket=5, jar=5, cart=2.0, sack=6, reeds=1.5),
    jimo_out=dict(tuft_straw=3, tuft_grass=4, hay=4, stone=3, basket=4, jar=4, cart=1.8, sack=5, reeds=2),
    yan_camp=dict(tuft_trample=4, rock=3, firewood=4, arrows=1, mat=3, rope=3, helmet=2, jar=5, sack=4, basket=2, tuft_straw=2, stone=2),
    vista=dict(hedge=9, trees=7, haystack=8, ridge=8, hut=3),
)
def _zone_mult(loc, x, y):
    if loc == 'jimo_out':
        if abs(x) < 6.2 and y < -30: return dict(stone=1.0, sack=1.5, tuft_grass=0.4, reeds=0.3, basket=1.4, cart=1.5)
        return dict(tuft_grass=1.2, reeds=1.3, cart=0.6)
    if loc == 'jimo_in':
        if y < 13.0: return dict(basket=1.6, sack=1.4, jar=1.5, cart=1.4)
        return dict(hay=1.4, tuft_straw=1.2)
    return {}

# ============================================================================= templates / instances
def _template(kind, vi, tone):
    TP = J.STATE.setdefault('dg_tpl', {}); key = (kind, vi, tone)
    if key in TP: return TP[key]
    fn, variants, decal, size, height = LIB[kind]; kw = variants[vi]; m = _pal(tone)
    r = random.Random(7000 + 131 * list(LIB).index(kind) + 17 * vi); mb = _mb(); fp = fn(mb, m, r, **kw)
    name = 'dgm_%s%d_%d%d' % (kind, vi, tone[0], tone[1]); me = bpy.data.meshes.new(name)
    me.from_pydata([V(v) for v in mb.v], [], mb.f); me.update(); uvl = me.uv_layers.new(name='UVMap'); i = 0
    for fi, f in enumerate(mb.f):
        for c in mb.uv[fi]: uvl.data[i].uv = c; i += 1
    for mt in mb.mats: me.materials.append(mt)
    for fi, p in enumerate(me.polygons): p.material_index = mb.mi[fi]; p.use_smooth = kind in SMOOTH
    me.materials.append(J.T.mat_ink())                                  # the ink slot of the hull (modifier material_offset)
    TP[key] = (me, fp); _EXT[(kind, vi)] = (max(math.hypot(v[0], v[1]) for v in mb.v), max(v[2] for v in mb.v)); return TP[key]

_EXT = {}
def _ext(kind, vi):
    """(horizontal radius, height) in D of the built template mesh (true extents: cart shafts, sack tops ...)."""
    if (kind, vi) not in _EXT: _template(kind, vi, (0, 0))
    return _EXT[(kind, vi)]

def _spawn(kind, vi, tone, loc, yaw, scl, hull_w, idx):
    me, fp = _template(kind, vi, tone)
    ob = bpy.data.objects.new('dg_%s_%04d' % (kind, idx), me); J.STATE['SET'].objects.link(ob)
    ob.location = loc; ob.rotation_euler = (0.0, 0.0, yaw); ob.scale = scl
    mod = ob.modifiers.new('ink_hull', 'SOLIDIFY'); mod.thickness = hull_w / max(1e-3, sum(scl) / 3.0); mod.offset = 1.0; mod.use_flip_normals = True; mod.use_rim = False
    mod.material_offset = len(me.materials) - 1; mod.use_even_offset = True
    J.no_bounce(ob)
    if kind in NOSHADOW: ob.visible_shadow = False
    return ob

def clear_dressing():
    """Remove everything dress_ground built (objects dg_*, meshes dgm_*)."""
    _bind()
    for ob in [o for o in bpy.data.objects if o.name.startswith('dg_')]: bpy.data.objects.remove(ob, do_unlink=True)
    for me in [x for x in bpy.data.meshes if x.name.startswith('dgm_')]: bpy.data.meshes.remove(me)
    J.STATE.pop('dg_tpl', None)

# ============================================================================= camera, ground, occupancy
def _pose(cam, scene):
    mw = cam.matrix_world.copy(); vf = list(cam.data.view_frame(scene=scene))
    xs = [v.x for v in vf]; ys = [v.y for v in vf]
    return dict(mw=mw, inv=mw.inverted(), loc=mw.translation.copy(), R=mw.to_3x3(), x0=min(xs), x1=max(xs), y0=min(ys), y1=max(ys), zf=vf[0].z, clip=cam.data.clip_start)

def _ray(p, u, v):
    d = p['R'] @ V((p['x0'] + (p['x1'] - p['x0']) * u, p['y0'] + (p['y1'] - p['y0']) * v, p['zf'])); return d.normalized()

def _project(p, P):
    c = p['inv'] @ P
    if c.z > -1e-4: return None
    k = p['zf'] / c.z; return ((c.x * k - p['x0']) / (p['x1'] - p['x0']), (c.y * k - p['y0']) / (p['y1'] - p['y0']), -c.z)    # u, v (0 = bottom), depth

# ---- actor screen boxes
ACTOR_PAD = (0.035, 0.03)                  # (u, v) margin added round every actor rectangle (fraction of the frame)
def _rect(p, pts):
    """Screen rectangle (u0, v0, u1, v1) of world points; points behind the camera are ignored (None if none is in front)."""
    q = [_project(p, P) for P in pts]; q = [a for a in q if a is not None]
    if not q: return None
    return (min(a[0] for a in q), min(a[1] for a in q), max(a[0] for a in q), max(a[1] for a in q))

def _actor_objects(actors):
    """Objects whose screen box must stay free of props. actors = list of objects / names (a card, a puppet root: its mesh children count), None = auto: the ph_* placeholders and any
    object named card* / puppet* / actor* / cast* or carrying the custom property `actor`."""
    import re
    sc = bpy.context.scene; out = []
    if actors is not None: return [bpy.data.objects[a] if isinstance(a, str) else a for a in actors]
    for o in sc.objects:
        if o.name.startswith('dg_'): continue
        if o.name.startswith('ph_') or o.get('actor') or re.match(r'(card|puppet|actor|cast)', o.name, re.I):
            if o.parent is None or not (o.parent.name.startswith('ph_') or o.parent.get('actor')): out.append(o)
    return out

def _obj_points(ob):
    """World-space bounding corners of an object and all its mesh descendants (current frame)."""
    pts = []; st = [ob]
    while st:
        o = st.pop(); st += list(o.children)
        if o.hide_render: continue
        if o.type in ('MESH', 'CURVE', 'FONT', 'SURFACE', 'META') and o.bound_box:
            mw = o.matrix_world; pts += [mw @ V(c) for c in o.bound_box]
        elif o.type == 'EMPTY' and not o.children: pts.append(o.matrix_world.translation.copy())
    return pts

def _mark_boxes(preset):
    """[(x, y, half_width, height)] world boxes of the shot's stand marks (people: HEIGHT x 0.55 half width; oxen: 3.2 D half width, 3.7 D tall; herd = oxen)."""
    import jimo_shots as S
    out = []
    if preset not in S.SHOTS: return out
    for role, lst in S.marks_for(preset).items():
        if isinstance(lst, str) or role == 'road': continue
        for m in lst:
            if len(m) >= 3 and m[2] > 3.0: continue
            sc = m[4] if len(m) > 4 else 1.0
            if role == 'ox' or role.startswith('herd'): out.append((float(m[0]), float(m[1]), 3.2 * sc, 3.7 * sc))
            else: h = S.HEIGHT.get(role, 3.0); out.append((float(m[0]), float(m[1]), 0.55 * h, 1.12 * h))
    return out

def _actor_rects(p, objs, boxes):
    """All actor screen rectangles (padded) at the pose p: the objects' bounding boxes at the current frame + the marks' boxes."""
    rects = []
    for o in objs:
        r = _rect(p, _obj_points(o))
        if r: rects.append(r)
    right = p['R'] @ V((1, 0, 0)); right.z = 0.0
    right = right.normalized() if right.length > 1e-6 else V((1, 0, 0))
    for (x, y, hw, h) in boxes:
        c = V((x, y, 0.0)); r = _rect(p, [c + right * hw, c - right * hw, c + right * hw + V((0, 0, h)), c - right * hw + V((0, 0, h)), c + V((0, 0, h))])
        if r: rects.append(r)
    pu, pv = ACTOR_PAD
    return [(a - pu, b - pv, c + pu, d + pv) for (a, b, c, d) in rects]

def _poses(cam, frames, actors=None, preset=None, nmax=24):
    scene = bpy.context.scene; cam = bpy.data.objects[cam] if isinstance(cam, str) else (cam or scene.camera)
    assert cam is not None, 'dress_ground: no camera (pose one with J.shot_camera / J.make_camera first)'
    objs = _actor_objects(actors); boxes = _mark_boxes(preset)
    def one():
        bpy.context.view_layer.update(); p = _pose(cam, scene); p['rects'] = _actor_rects(p, objs, boxes); return p
    if frames is None: return [one()], cam, len(objs) + len(boxes)
    fl = [int(frames)] if isinstance(frames, (int, float)) else sorted(set(int(f) for f in frames))
    if len(fl) > nmax: fl = [fl[round(i * (len(fl) - 1) / (nmax - 1))] for i in range(nmax)]
    f0 = scene.frame_current; out = []
    for f in fl: scene.frame_set(f); out.append(one())
    scene.frame_set(f0); bpy.context.view_layer.update(); return out, cam, len(objs) + len(boxes)

def _ground_z(loc, x, y):
    return J.VS.terrain_h(x, y) if loc == 'vista' else 0.0

DRY_X = [(-46.0, -12.5), (12.5, 46.0)]
def _in_ditch(x, y): return -25.5 < y < -13.3 and any(a + 3.0 < x < b - 3.0 for a, b in DRY_X)

def _hit(loc, p, d):
    """Ray (origin p['loc'], dir d) on the ground; vista follows the terrain height by fixed-point iteration. -> (x, y, z, t) or None."""
    o = p['loc']; z = 0.0
    for _ in range(4 if loc == 'vista' else 1):
        if d.z > -1e-4: return None
        t = (z - o.z) / d.z
        if t <= 0: return None
        x, y = o.x + d.x * t, o.y + d.y * t
        if loc != 'vista':
            if loc != 'jimo_in' and -31.5 < y < -4.0:                       # the moat strip: only the dry ditch floor (z -1.2) is ground
                t2 = (-1.2 - o.z) / d.z; x, y = o.x + d.x * t2, o.y + d.y * t2
                return (x, y, -1.2, t2) if (t2 > 0 and _in_ditch(x, y)) else None
            return (x, y, 0.0, t)
        z = _ground_z(loc, x, y)
    return (x, y, z, t)

SKIP_OCC = ('sky', 'moon', 'hills', 'halos', 'cityglow', 'townglow', 'ground', 'ground2', 'campground', 'lane', 'road', 'furrows', 'streaks', 'water', 'banks', 'pools', 'terrain', 'river', 'vroad', 'straw', 'wallpools', 'rainstreaks')
VISTA_OCC = ('towns', 'townroofs', 'siegetents', 'vtrees', 'wood', 'cloth')
def _occupancy(loc, box, cell):
    """Boolean grid (cell D) over box = (x0, x1, y0, y1): True where an existing set object stands on / near the ground (any triangle between z 0.35 and 2.4 D; vista: any triangle of the town / tree meshes)."""
    x0, x1, y0, y1 = box; nx, ny = int((x1 - x0) / cell) + 2, int((y1 - y0) / cell) + 2; occ = np.zeros((nx, ny), bool)
    for ob in J.STATE['SET'].objects:
        if ob.type != 'MESH' or ob.hide_render or ob.name.startswith(('dg_', 'ph_', 'hglow', 'pen_')) or ob.name in SKIP_OCC: continue
        if loc == 'vista' and ob.name not in VISTA_OCC: continue
        me = ob.data; nv = len(me.vertices)
        if not nv: continue
        co = np.empty(nv * 3, np.float64); me.vertices.foreach_get('co', co); co = co.reshape(-1, 3); mw = np.array(ob.matrix_world); W = co @ mw[:3, :3].T + mw[:3, 3]
        me.calc_loop_triangles(); nt = len(me.loop_triangles)
        if not nt: continue
        ti = np.empty(nt * 3, np.int32); me.loop_triangles.foreach_get('vertices', ti); P = W[ti.reshape(-1, 3)]
        zmin, zmax = P[:, :, 2].min(1), P[:, :, 2].max(1)
        keep = np.ones(nt, bool) if loc == 'vista' else (zmax > 0.35) & (zmin < 2.4)
        if not keep.any(): continue
        P = P[keep]; ix0 = np.clip(((P[:, :, 0].min(1) - x0) / cell).astype(int), 0, nx - 1); ix1 = np.clip(((P[:, :, 0].max(1) - x0) / cell).astype(int), 0, nx - 1)
        iy0 = np.clip(((P[:, :, 1].min(1) - y0) / cell).astype(int), 0, ny - 1); iy1 = np.clip(((P[:, :, 1].max(1) - y0) / cell).astype(int), 0, ny - 1)
        for a, b, c, d in zip(ix0, ix1, iy0, iy1): occ[a:b + 1, c:d + 1] = True
    return occ

def default_keep_clear(preset=None, r=None):
    """[(x, y, radius)] for the shot's stand marks, herd lanes and road path (jimo_shots marks, z <= 3 only). Every mark and every herd position gets `r` = ACTOR_CLEAR = 2.5 D.
    `preset` default = the built shot."""
    _bind(); import jimo_shots as S
    r = ACTOR_CLEAR if r is None else r; preset = preset or J.STATE.get('preset'); out = []
    if preset not in S.SHOTS: return out
    for role, lst in S.marks_for(preset).items():
        if isinstance(lst, str): continue
        if role == 'road':                                               # a path: circles every r along it
            for (a, b) in zip(lst[:-1], lst[1:]):
                L = math.hypot(b[0] - a[0], b[1] - a[1]); n = max(1, int(L / r))
                out += [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n, r) for i in range(n + 1)]
            continue
        for m in lst:
            if len(m) >= 3 and m[2] > 3.0: continue                      # on the wall walk
            out.append((float(m[0]), float(m[1]), r))
    return out

def _exclude(loc, x, y):
    """Non-ground: moat / berm / bridge (outside), the wall footprint, the vista river, towns, Jimo's ring moat, the siege camp."""
    if loc in ('jimo_out', 'yan_camp') and -31.5 < y < -4.0 and not _in_ditch(x, y): return True
    if loc == 'jimo_in' and y < 4.4: return True
    if loc == 'vista':
        if abs(y - J.VS.river_y(x)) < 13.0: return True
        for t in J.STATE.get('towns', ()):
            if abs(x - t['x']) < t['s'] * 0.62 + 4 and abs(y - t['y']) < t['s'] * 0.62 + 4: return True
        jx, jy = J.VS.JIMO
        if math.hypot(x - jx, y - jy) < 52: return True
        if jx - 44 < x < jx + 70 and jy - 66 < y < jy - 36: return True
    return False



# ============================================================================= the scatter
STAT = {}
def dress_ground(cam=None, density=1.0, seed=0, keep_clear=None, frames=None, actors=None):
    """Scatter lit, inked, instanced ground dressing where the camera sees the ground (API.md). Returns dict(n, kinds, stat, poses, ...).
    cam: camera object / name (default scene camera, already posed). frames: film frames of a keyed camera; the union of the frustums (<= 24 samples) is dressed AND every sample is checked
    against the actors. density 1.0 = about 40 % of the old helper (one candidate per ~20 px square of the ground on a 360 x 640 frame), 0 = nothing. seed: deterministic.
    keep_clear: [(x, y, r)] world circles that stay empty; None = default_keep_clear() (every stand mark / herd position / road point, 2.5 D), [] = none.
    actors: the actor cards (objects / names; children count) whose SCREEN rectangle (feet included, + a margin) no prop may overlap at any sampled frame; None = auto (ph_* placeholders,
    objects named card* / puppet* / actor* / cast*, objects with the custom property `actor`) + the shot's marks as boxes; [] = marks only.
    Nothing is placed within 3 D of the lens at any sampled pose."""
    _bind(); S = J.STATE; loc = S['loc']; light = S['light']; clear_dressing()
    if density <= 0: return dict(n=0, kinds={}, poses=0)
    preset = S.get('preset'); poses, camo, nact = _poses(cam, frames, actors, preset); kc = default_keep_clear() if keep_clear is None else [tuple(float(v) for v in c) for c in keep_clear]
    far = 42.0 if loc != 'vista' else 520.0; vista = loc == 'vista'; cell = 0.5 if not vista else 2.0
    # ---- 1. candidate samples in screen space (stratified, jittered), one list per pose
    RW, RH = 360, 640; step = (13.0 if loc != 'vista' else 34.0) / math.sqrt(density * (DENSITY0 if not vista else 1.0)); nxs, nys = int(RW / step), int(RH / step); cands = []
    for pi, p in enumerate(poses):
        for gy in range(nys):
            for gx in range(nxs):
                r = random.Random(seed * 1000003 + pi * 7919 + gy * 131 + gx); u = (gx + r.random()) / nxs; v = 1.0 - (gy + r.random()) / nys
                d = _ray(p, u, v); h = _hit(loc, p, d)
                if h is None or h[3] > far or h[3] < max(LENS_CLEAR if not vista else 0.6, p['clip']): continue
                cands.append((pi, gy, gx, r.random(), h, u, v))
    if not cands: return dict(n=0, kinds={}, poses=len(poses))
    xs = [c[4][0] for c in cands]; ys = [c[4][1] for c in cands]; box = (min(xs) - 14, max(xs) + 14, min(ys) - 14, max(ys) + 14)
    if (box[1] - box[0]) / cell > 2600 or (box[3] - box[2]) / cell > 2600: cell *= 2.0
    occ = _occupancy(loc, box, cell); nx, ny = occ.shape
    def blocked(x, y, rad):
        for q in ((0, 0), (rad, 0), (-rad, 0), (0, rad), (0, -rad)):
            ix, iy = int((x + q[0] - box[0]) / cell), int((y + q[1] - box[2]) / cell)
            if 0 <= ix < nx and 0 <= iy < ny and occ[ix, iy]: return True
        return False
    def hits_actor(x, y, z, rad, hgt):
        """True when the prop's screen rectangle overlaps an actor rectangle at any sampled pose (or the prop is within LENS_CLEAR of the lens)."""
        pts = [V((x + rad * cx, y + rad * cy, z + zz)) for cx, cy in ((1, 0), (-1, 0), (0, 1), (0, -1), (0.7, 0.7), (-0.7, 0.7), (0.7, -0.7), (-0.7, -0.7)) for zz in (0.0, hgt)]
        for q in poses:
            if not vista and (q['loc'] - V((x, y, z + hgt * 0.5))).length - rad < LENS_CLEAR: return 'lens'
            if not q['rects']: continue
            behind = any(_project(q, P) is None for P in pts); pr = _rect(q, pts)
            if pr is None: continue
            if behind: return 'lens'                                       # straddles the lens plane: right beside the camera
            for (a, b, c, d) in q['rects']:
                if pr[0] < c and pr[2] > a and pr[1] < d and pr[3] > b: return 'actor'
        return None
    STAT.clear(); W = WEIGHTS[loc]; placed = []; grid = {}; counts = {}; lens = camo.data.lens
    for (pi, gy, gx, rv, (x, y, z, t), u, v) in sorted(cands, key=lambda c: (c[1], c[2], c[0])):
        r = random.Random(seed * 7000003 + pi * 104729 + gy * 977 + gx * 31 + 5)
        if _exclude(loc, x, y): continue
        zm = _zone_mult(loc, x, y); names = [k for k in W]; ws = [W[k] * zm.get(k, 1.0) for k in names]
        # screen position in every pose: caption band (y > 880 / 1280) -> dim tone
        band = False; dmin = t
        for q in poses:
            pr = _project(q, V((x, y, z + 0.4)))
            if pr and 0 <= pr[0] <= 1 and 0 <= pr[1] <= 1 and (1 - pr[1]) > 0.66: band = True
            if pr: dmin = min(dmin, pr[2])
        near = 1.0 if (vista or t > 14.0) else 0.3 + 0.7 * (t - 3.0) / 11.0          # smaller close to the lens
        if near < 1.0: ws = [0.0 if (LIB[k][4] > 1.0 or LIB[k][3] > 1.2) else w * (0.25 if k.startswith(('stone', 'rock')) else 1.0) for k, w in zip(names, ws)]   # nothing tall / wide close to a low camera, few stones
        if not any(ws): continue
        kind = r.choices(names, ws)[0]; fn, variants, decal, size, height = LIB[kind]; vi = r.randrange(len(variants))
        f_px = lens / 36.0 * RH; want = 8.0
        boost = min(1.5 if not vista else 6.5 if kind in ('hedge', 'ridge') else 4.5, max(1.0, want * t / (max(0.35, height) * f_px)))
        if vista: boost = min(boost, 2.6) if kind == 'hut' else boost
        s = r.uniform(0.85, 1.2) * boost * near * GAIN.get(kind, 1.0) * (0.8 if kind in ('stone', 'rock') else 1.0); rad = size * s; hgt = height * s
        if blocked(x, y, rad * 0.8): STAT['occ'] = STAT.get('occ', 0) + 1; continue
        if any(math.hypot(x - cx, y - cy) < cr + rad * 0.8 for (cx, cy, cr) in kc): STAT['keep'] = STAT.get('keep', 0) + 1; continue
        er, eh = _ext(kind, vi); why = hits_actor(x, y, z, max(rad, er * s * 1.05), max(hgt, eh * s * 1.05))
        if why: STAT[why] = STAT.get(why, 0) + 1; continue
        gk = (int(x // 3.0), int(y // 3.0)); hit_ = False
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for (px_, py_, pr_) in grid.get((gk[0] + dx, gk[1] + dy), ()):
                    if math.hypot(x - px_, y - py_) < (rad + pr_) * 1.15: hit_ = True
        if hit_: STAT['dup'] = STAT.get('dup', 0) + 1; continue
        grid.setdefault(gk, []).append((x, y, rad))
        wm = J.warm_at(V((x, y, 0.6))); tone = (1 if wm > 0.22 else 0, 1 if band else 0)
        yaw = r.uniform(0, TAU); scl = (s, s, s)
        STAT['ok'] = STAT.get('ok', 0) + 1
        placed.append((kind, vi, tone, (x, y, z + 0.005), yaw, scl, J.T.hull(dmin), band))
        counts[kind] = counts.get(kind, 0) + 1
    # ---- 2. build: one shared mesh per (kind, variant, tone), one object per prop
    cap = int(400 * min(2.0, density)) if not vista else int(1100 * min(2.0, density))
    if len(placed) > cap: placed = placed[:cap]
    for i, pl in enumerate(placed): _spawn(pl[0], pl[1], pl[2], pl[3], pl[4], pl[5], pl[6], i)
    return dict(n=len(placed), kinds=counts, stat=dict(STAT, cand=len(cands)), poses=len(poses), far=far, keep_clear=len(kc), actors=nact, templates=len(S.get('dg_tpl', {})))

if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'share':
        for f in sys.argv[2:]: print('%.3f  %s' % (ground_share(f), f))
    else: print(__doc__)

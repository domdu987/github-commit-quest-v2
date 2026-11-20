"""jimo_dress.py : ground dressing for the film-18 set (API.md, "Ground dressing (render teams: call this)").

    J.dress_ground(cam=None, density=1.0, seed=0, keep_clear=None, frames=None)   scatter lit, inked, instanced ground props where the camera sees the ground
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

# ============================================================================= materials (set materials, dark to mid, three tones)
TAU = 2 * math.pi
def _pal(tone):
    """tone = (warm, dim): warm = fire-lit hue (ochre shade instead of the blue ambient), dim = caption band (no bright pixel)."""
    S = J.STATE; P = S['P']; FORM = tuple(P['form']); tx = S['tx']; warm, dim = tone
    k = 0.58 if dim else 1.0; sm = ((1.55, 1.0, 0.5) if warm else (1.0, 1.0, 1.0)); sm = tuple(x * (0.8 if dim else 1.0) for x in sm)
    tint = (1.0, 0.86, 0.68) if warm else (1.0, 1.0, 1.0)
    pre = S['pre'] + 'dg%d%d_' % (1 if warm else 0, 1 if dim else 0)
    def hx(h):
        c = [int(h.lstrip('#')[i:i + 2], 16) * t for i, t in zip((0, 2, 4), tint)]; return '#%02x%02x%02x' % tuple(min(255, int(v)) for v in c)
    def C(h, g=1.0):
        h2 = hx(h); return J._untoon(J.mat_lit('%sc_%s_%g' % (pre, h2.lstrip('#'), g), h2, gain=g * k, shade_mul=sm, form=FORM))
    def TX(n, g=1.0): return J._untoon(J.mat_lit('%st_%s_%g' % (pre, n, g), image=tx[n], gain=g * k, shade_mul=sm, form=FORM))
    m = dict(straw=C('#8e7238', 0.78), straw_d=C('#6c5428', 0.78), hay=C('#7c6234', 0.7), grass=C('#5c6a30', 0.95), grass_d=C('#404a26', 0.95), reed=C('#7a6a3a', 0.95),
             stone=C('#76685a', 0.8), stone_d=C('#54483e', 0.8), wood=C('#6a4628', 1.0), wood_d=C('#46301e', 1.0), wood_l=C('#a07c4c', 0.9), clay=C('#7c4c36', 1.0), clay_d=C('#58382a', 1.0),
             iron=C('#3c3e4a', 1.0), sack=C('#8a7452', 0.95), sack_d=C('#66543c', 0.95), red=C('#842a20', 1.0), leaf=C('#34542e', 0.95), leaf2=C('#6a6a34', 0.95), thatch=C('#7a6230', 0.95),
             plaster=C('#9c8a68', 0.9), rope=C('#7e6240', 0.95), black=C('#1e1a24', 1.0), bronze=C('#8a6430', 1.0),
             earth=TX('earth', 0.62), earth_d=TX('bank', 0.5), planks=TX('planks_d', 0.95), hide=TX('hide', 0.7), grass_t=TX('grass', 0.78), grass2_t=TX('grass2', 0.74))
    # puddle: wet dark diffuse + GGX (the real lamps glint in it) + a faint sky-coloured emission standing for the sky mirror
    n = pre + 'puddle'
    if n not in bpy.data.materials:
        base = J._untoon(J.mat_lit(n, '#1c2840' if S['light'] == 'NIGHT' else '#3a3040', gain=0.7 * k, shade_mul=sm, form=FORM))
        J._glossy(base, (0.55, 0.62, 0.9), 0.5 * (0.5 if dim else 1.0), 0.06)
        sky = (0.05, 0.09, 0.2) if S['light'] == 'NIGHT' else (0.30, 0.20, 0.16)
        J.MN._append_shader(base, lambda nt: _emit(nt, sky, 0.7 * (0.5 if dim else 1.0)))
    m['puddle'] = bpy.data.materials[n]
    return m

def _emit(nt, rgb, k):
    e = nt.nodes.new('ShaderNodeEmission'); e.inputs['Color'].default_value = (*rgb, 1); e.inputs['Strength'].default_value = k; return e.outputs['Emission']

# ============================================================================= the mesh library (origin = foot, +z up, 1 D = one head)
def _mb(): return J.MB()
def _tilt(mb, ax, ang, shift=(0, 0, 0)):
    from mathutils import Matrix
    R = Matrix.Rotation(ang, 3, ax); mb.v = [tuple(R @ V(v) + V(shift)) for v in mb.v]

def _leaf(mb, p, a, ln, w, bend, mat, mat2=None):
    """One curved leaf blade: a two-segment strip from p, azimuth a, length ln, width w, bending up then over by `bend`."""
    u = V((math.cos(a), math.sin(a), 0.0)); s = V((-u.y, u.x, 0.0)); z0 = V((0, 0, 0)); mid = p + u * (ln * 0.45 * (1 - bend)) + V((0, 0, ln * 0.55)); tip = p + u * (ln * (0.5 + 0.5 * bend)) + V((0, 0, ln * (0.8 - 0.35 * bend)))
    mb.oface([p - s * w, p + s * w, mid + s * w * 0.6, mid - s * w * 0.6], mat, [(0, 0), (1, 0), (1, 0.5), (0, 0.5)], (0, 0, 1))
    mb.oface([mid - s * w * 0.6, mid + s * w * 0.6, tip], mat2 or mat, [(0, 0.5), (1, 0.5), (0.5, 1)], (0, 0, 1))
    mb.oface([p + s * w, p - s * w, mid - s * w * 0.6, mid + s * w * 0.6], mat, [(0, 0), (1, 0), (1, 0.5), (0, 0.5)], (0, 0, -1))
    mb.oface([mid + s * w * 0.6, mid - s * w * 0.6, tip], mat2 or mat, [(0, 0.5), (1, 0.5), (0.5, 1)], (0, 0, -1))

def b_tuft(mb, m, r, kind='straw', flat=False):
    """A clump of 6-9 broad leaf blades round a small soil mound (broad so that the 3 px ink hull does not swallow them)."""
    mats = (m['straw'], m['hay'], m['straw_d']) if kind == 'straw' else (m['grass'], m['leaf2'], m['grass_d'])
    J.lumpy(mb, V((0, 0, 0.04)), 0.26, m['earth_d'], r.randint(1, 99), seg=6, rings=3, rough=0.3, squash=0.4)
    n = r.randint(6, 9)
    for i in range(n):
        a = r.uniform(0, TAU); rr = r.uniform(0.0, 0.18)
        _leaf(mb, V((rr * math.cos(a), rr * math.sin(a), 0.02)), a + r.uniform(-.4, .4), r.uniform(0.55, 0.95) * (0.65 if flat else 1.0), r.uniform(0.11, 0.17), r.uniform(0.2, 0.9) if not flat else r.uniform(0.7, 1.0), r.choice(mats), mats[1])
    return 0.5

def b_reeds(mb, m, r):
    for i in range(r.randint(5, 8)):
        a = r.uniform(0, TAU); rr = r.uniform(0, 0.35); h = r.uniform(1.3, 2.1); p = V((rr * math.cos(a), rr * math.sin(a), 0))
        _leaf(mb, p, a, h, r.uniform(0.09, 0.14), r.uniform(0.05, 0.3), m['reed'] if i % 2 else m['straw'], m['straw_d'])
        if i % 3 == 0: top = p + V((0.0, 0.0, h * 0.8)); mb.frustum(top, top + V((0.03, 0.0, 0.5)), 0.13, 0.09, m['clay_d'], seg=5)
    return 0.5

def b_hay(mb, m, r):
    J.lumpy(mb, V((0, 0, 0.1)), 0.8, m['hay'], r.randint(1, 99), seg=9, rings=5, rough=0.22, squash=0.55)
    for i in range(r.randint(8, 12)):
        a = r.uniform(0, TAU); rr = r.uniform(0.15, 0.6)
        _leaf(mb, V((rr * math.cos(a), rr * math.sin(a), r.uniform(0.15, 0.35))), a + r.uniform(-.5, .5), r.uniform(0.6, 1.0), r.uniform(0.1, 0.15), r.uniform(0.8, 1.0), r.choice((m['straw'], m['hay'], m['straw_d'])))
    return 1.0

def b_stone(mb, m, r, cluster=False):
    if not cluster:
        rr = r.uniform(0.3, 0.55); J.lumpy(mb, V((0, 0, rr * 0.45)), rr, r.choice((m['stone'], m['stone_d'])), r.randint(1, 99), seg=8, rings=5, rough=0.3, squash=0.62)
        return rr * 1.1
    J.lumpy(mb, V((0, 0, 0.22)), 0.5, m['stone'], r.randint(1, 99), seg=8, rings=5, rough=0.3, squash=0.6)
    for q in range(3): a = r.uniform(0, TAU); d = r.uniform(0.5, 0.85); rr = r.uniform(0.14, 0.26); J.lumpy(mb, V((d * math.cos(a), d * math.sin(a), rr * 0.4)), rr, r.choice((m['stone'], m['stone_d'])), r.randint(1, 99), seg=6, rings=4, rough=0.3, squash=0.6)
    return 0.95

def b_basket(mb, m, r, tipped=False):
    mb.frustum(V((0, 0, 0)), V((0, 0, 0.72)), 0.34, 0.54, m['straw_d'], seg=9, cap0=True, cap1=False)
    J.cyl(mb, V((0, 0, 0.64)), 0.55, 0.1, m['wood_d'], seg=9, r1=0.55); J.cyl(mb, V((0, 0, 0.3)), 0.43, 0.07, m['straw'], seg=9, r1=0.43)
    J.cyl(mb, V((0, 0, 0.02)), 0.34, 0.03, m['hay'], seg=9, r1=0.3) if False else None
    if tipped: _tilt(mb, 'Y', 1.45, (0.0, 0.0, 0.5))
    return 0.6

def b_pot_broken(mb, m, r):
    J.ellipsoid(mb, V((0, 0, 0.4)), 0.44, 0.44, 0.4, m['clay'], seg=10, rings=5, phi=(0.0, r.uniform(3.6, 4.6)), th=(r.uniform(0.35, 0.8), math.pi))
    for q in range(r.randint(3, 5)):
        a = r.uniform(0, TAU); d = r.uniform(0.45, 0.9); p = V((d * math.cos(a), d * math.sin(a), 0.03)); u = V((math.cos(a + 1), math.sin(a + 1), 0.15)) * r.uniform(0.15, 0.3); w = V((-u.y, u.x, 0.12)) * 0.8
        mb.oface([p, p + u, p + u * 0.6 + w, p + w * 0.4], r.choice((m['clay'], m['clay_d'])), [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, 1))
    return 0.9

def b_sack(mb, m, r, pile=False, lying=False):
    def one(c, s, lie=0.0):
        J.lumpy(mb, c + V((0, 0, 0.36 * s)), 0.44 * s, m['sack'], r.randint(1, 99), seg=9, rings=5, rough=0.14, squash=0.82)
        mb.frustum(c + V((0, 0, 0.7 * s)), c + V((0.03, 0.02, 0.9 * s)), 0.13 * s, 0.07 * s, m['sack_d'], seg=5)
    if pile: one(V((-0.4, 0, 0)), 1.0); one(V((0.42, 0.1, 0)), 0.95); one(V((0.02, 0.05, 0.62)), 0.9)
    else: one(V((0, 0, 0)), r.uniform(0.9, 1.2))
    if lying: _tilt(mb, 'Y', 1.3, (0.3, 0, 0.42))
    return 1.0 if pile else 0.55

def b_cart(mb, m, r, loaded=False):
    Rw = 0.95; z0 = Rw * 0.95
    J.obox(mb, V((0, 0, z0)), (1, 0, 0), (0, 1, 0), (0, 0, 1), 1.3, 0.78, 0.07, m['planks'], uvk=0.5)
    for sy in (-1, 1):
        J.obox(mb, V((0, sy * 0.78, z0 + 0.3)), (1, 0, 0), (0, 1, 0), (0, 0, 1), 1.3, 0.05, 0.28, m['planks'], uvk=0.5)
        J.rod(mb, V((-1.3, sy * 0.5, z0 + 0.05)), V((-3.1, sy * 0.45, 0.28)), 0.07, m['wood'], seg=4)              # shafts, resting on the ground
        a0 = V((0, sy * 0.95, z0))
        for q in range(14):
            t0, t1 = TAU * q / 14, TAU * (q + 1) / 14
            J.rod(mb, a0 + V((Rw * math.cos(t0), 0, Rw * math.sin(t0))), a0 + V((Rw * math.cos(t1), 0, Rw * math.sin(t1))), 0.11, m['wood_d'], seg=4)
        for q in range(4):
            t0 = math.pi * q / 4; J.rod(mb, a0 + V((Rw * math.cos(t0), 0, Rw * math.sin(t0))), a0 - V((Rw * math.cos(t0), 0, Rw * math.sin(t0))), 0.07, m['wood'], seg=4)
        J.rod(mb, a0 + V((0, -0.12, 0)), a0 + V((0, 0.12, 0)), 0.15, m['wood'], seg=6)
    J.rod(mb, V((0, -1.0, z0)), V((0, 1.0, z0)), 0.07, m['wood_d'], seg=5)
    J.obox(mb, V((1.3, 0, z0 + 0.3)), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.04, 0.78, 0.28, m['planks'], uvk=0.5)
    if loaded:
        for q in range(3): J.lumpy(mb, V((-0.7 + 0.7 * q, r.uniform(-.2, .2), z0 + 0.5)), 0.5, m['sack'] if q % 2 else m['hay'], r.randint(1, 99), seg=8, rings=4, rough=0.15, squash=0.8)
    return 1.9

def b_rut(mb, m, r):
    L = r.uniform(2.6, 5.0); n = 4; ph = r.uniform(0, 3)
    for sy in (-0.45, 0.45):
        prev = None
        for i in range(n + 1):
            x = -L / 2 + L * i / n; y = sy + 0.12 * math.sin(ph + x * 0.9); p = (x, y)
            if prev: J.obox(mb, V(((prev[0] + p[0]) / 2, (prev[1] + p[1]) / 2, 0.035)), (1, 0, 0), (0, 1, 0), (0, 0, 1), L / n / 2 + 0.02, 0.12, 0.035, m['earth_d'], uvk=0.5)
            prev = p
    return L / 2

def b_puddle(mb, m, r):
    J.lumpy(mb, V((0, 0, 0.0)), 1.0, m['puddle'], r.randint(1, 99), seg=12, rings=6, rough=0.28, squash=0.075)
    return 1.0

def b_firewood(mb, m, r):
    for lay, (ys, z) in enumerate((((-0.5, 0.0, 0.5), 0.13), ((-0.25, 0.25), 0.36), ((0.0,), 0.58))):
        for i, y in enumerate(ys):
            L = r.uniform(1.3, 1.7); x0 = -L / 2 + r.uniform(-.1, .1)
            mb.frustum(V((x0, y, z)), V((x0 + L, y + r.uniform(-.05, .05), z)), 0.13, 0.12, m['wood'] if (i + lay) % 2 else m['wood_d'], seg=5, cap_mat=m['wood_l'])
    return 1.0

def b_arrows(mb, m, r):
    for q in range(r.randint(4, 6)):
        a = r.uniform(0, TAU); d = r.uniform(0.0, 0.8); p = V((d * math.cos(a), d * math.sin(a), 0.03)); stuck = q < 2
        if stuck: tip = p; top = p + V((r.uniform(-.5, .5), r.uniform(-.5, .5), 1.4))
        else: dd = V((math.cos(a + 1.2), math.sin(a + 1.2), 0.0)); tip = p; top = p + dd * r.uniform(1.4, 2.0) + V((0, 0, 0.05))
        J.rod(mb, tip, top, 0.032, m['wood_l'], seg=3)
        u = (top - tip).normalized(); J.rod(mb, tip, tip + u * 0.18, 0.06, m['iron'], seg=3, r1=0.0)
        s = V((-u.y, u.x, 0)).normalized() * 0.07
        for t in (0.0, 0.2): mb.oface([top - u * (0.25 + t), top - u * t, top - u * t + s * 1.3, top - u * (0.25 + t) + s * 1.3], m['red'] if t == 0.0 else m['sack'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, 1))
    return 1.0

def b_mat(mb, m, r, two=False):
    for k in range(2 if two else 1):
        y = 0.0 if not two else (-0.26 if k == 0 else 0.26); z = 0.24
        mb.frustum(V((-0.85, y, z)), V((0.85, y, z)), 0.24, 0.24, m['straw'], seg=8, cap_mat=m['straw_d'])
        for x in (-0.5, 0.5): mb.frustum(V((x - 0.04, y, z)), V((x + 0.04, y, z)), 0.265, 0.265, m['rope'], seg=8, cap0=False, cap1=False)
    if two: J.rod(mb, V((-0.7, 0, 0.55)), V((0.7, 0, 0.55)), 0.22, m['straw'], seg=8) if False else None
    return 1.0

def b_rope(mb, m, r):
    for i, (R, z) in enumerate(((0.5, 0.07), (0.4, 0.17), (0.3, 0.26))):
        n = 12
        for q in range(n):
            a0, a1 = TAU * q / n, TAU * (q + 1) / n; J.rod(mb, V((R * math.cos(a0), R * math.sin(a0), z)), V((R * math.cos(a1), R * math.sin(a1), z)), 0.085, m['rope'], seg=4)
    J.rod(mb, V((0.5, 0, 0.07)), V((1.1, 0.35, 0.06)), 0.07, m['rope'], seg=4)
    return 0.8

def b_helmet(mb, m, r, side=False):
    J.ellipsoid(mb, V((0, 0, 0.0)), 0.44, 0.4, 0.42, m['iron'], seg=10, rings=5, th=(math.pi / 2, math.pi))
    J.cyl(mb, V((0, 0, 0.0)), 0.47, 0.07, m['bronze'], seg=10, r1=0.47)
    mb.frustum(V((0, 0, 0.4)), V((0.05, 0, 0.78)), 0.08, 0.02, m['red'], seg=5)
    if side: _tilt(mb, 'Y', 1.2, (0.15, 0, 0.42))
    return 0.5

def b_jar(mb, m, r, tipped=False):
    J.ellipsoid(mb, V((0, 0, 0.55)), 0.52, 0.52, 0.58, m['clay'], seg=10, rings=6, rough=0.04, seed=r.randint(1, 50))
    J.cyl(mb, V((0, 0, 1.0)), 0.3, 0.3, m['clay_d'], seg=8, r1=0.34); J.cyl(mb, V((0, 0, 1.28)), 0.38, 0.08, m['clay'], seg=8, r1=0.38)
    J.cyl(mb, V((0, 0, 0.62)), 0.54, 0.07, m['clay_d'], seg=10, r1=0.54)
    if tipped: _tilt(mb, 'Y', 1.35, (0.35, 0, 0.55))
    return 0.6

# ---- vista (units are D but the pieces are big: they are scaled again by the distance in the placer)
def b_hedge(mb, m, r):
    n = r.randint(9, 14); y = 0.0
    for i in range(n):
        y += r.uniform(-0.25, 0.25); rr = r.uniform(1.3, 1.9)
        J.lumpy(mb, V((i * 1.9, y, rr * 0.5)), rr, m['leaf'] if i % 3 else m['leaf2'], r.randint(1, 99), seg=8, rings=4, rough=0.3, squash=0.75)
    return n * 0.95

def b_trees(mb, m, r):
    for i in range(r.randint(4, 7)):
        a = r.uniform(0, TAU); d = r.uniform(0, 3.2); p = V((d * math.cos(a), d * math.sin(a), 0)); h = r.uniform(2.6, 4.2)
        mb.frustum(p, p + V((0, 0, h)), 0.32, 0.2, m['wood_d'], seg=5)
        for q in range(2): J.lumpy(mb, p + V((0, 0, h + 0.4 + q * 1.4)), 2.0 - 0.5 * q, m['leaf'] if (i + q) % 2 else m['leaf2'], r.randint(1, 99), seg=7, rings=4, rough=0.25, squash=0.8)
    return 4.0

def b_haystack(mb, m, r):
    mb.frustum(V((0, 0, 0)), V((0, 0, 2.6)), 2.5, 1.5, m['hay'], seg=9)
    mb.frustum(V((0, 0, 2.6)), V((0, 0, 4.0)), 1.5, 0.0, m['straw'], seg=9, cap0=False)
    mb.frustum(V((0, 0, 0.9)), V((0, 0, 1.1)), 2.35, 2.35, m['straw_d'], seg=9, cap0=False, cap1=False)
    J.rod(mb, V((0, 0, 3.9)), V((0, 0, 5.0)), 0.1, m['wood_d'], seg=4, r1=0.04)
    return 2.6

def b_ridge(mb, m, r):
    n = r.randint(10, 18); y = 0.0
    for i in range(n):
        y += r.uniform(-0.3, 0.3); J.lumpy(mb, V((i * 2.2, y, 0.25)), 1.5, m['earth_d'] if i % 2 else m['grass_t'], r.randint(1, 99), seg=8, rings=4, rough=0.2, squash=0.34)
    return n * 1.1

def b_hut(mb, m, r):
    w, d, h = 3.0, 2.4, 2.6
    J.obox(mb, V((0, 0, h / 2)), (1, 0, 0), (0, 1, 0), (0, 0, 1), w, d, h / 2, m['plaster'], uvk=0.3)
    rz = h + 2.4; rd = V((0, 0, 0))
    e = [V((-w - 0.5, -d - 0.5, h)), V((w + 0.5, -d - 0.5, h)), V((w + 0.5, d + 0.5, h)), V((-w - 0.5, d + 0.5, h))]; rg = [V((-w * 0.5, 0, rz)), V((w * 0.5, 0, rz))]
    for pts, nrm in (([e[0], e[1], rg[1], rg[0]], (0, -1, 1)), ([e[2], e[3], rg[0], rg[1]], (0, 1, 1)), ([e[1], e[2], rg[1]], (1, 0, 1)), ([e[3], e[0], rg[0]], (-1, 0, 1))):
        mb.oface(pts, m['thatch'], [(0, 0), (1, 0), (1, 1), (0, 1)][:len(pts)], nrm)
    mb.oface([V((-0.6, -d - 0.02, 0.0)), V((0.6, -d - 0.02, 0.0)), V((0.6, -d - 0.02, 1.8)), V((-0.6, -d - 0.02, 1.8))], m['black'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
    return 3.6

# kind -> (builder, variants, kwargs per variant, decal?, bright_ok?, base size D, height D)
LIB = dict(
    tuft_straw=(b_tuft, [dict(kind='straw'), dict(kind='straw', flat=True), dict(kind='straw')], 0, 0.45, 0.8),
    tuft_grass=(b_tuft, [dict(kind='grass'), dict(kind='grass', flat=True), dict(kind='grass')], 0, 0.45, 0.7),
    tuft_trample=(b_tuft, [dict(kind='grass', flat=True), dict(kind='straw', flat=True), dict(kind='grass', flat=True)], 0, 0.5, 0.5),
    reeds=(b_reeds, [{}, {}, {}], 0, 0.55, 2.0),
    hay=(b_hay, [{}, {}, {}], 0, 1.0, 0.7),
    stone=(b_stone, [{}, {}, dict(cluster=True)], 0, 0.5, 0.5),
    rock=(b_stone, [dict(cluster=True), {}, dict(cluster=True)], 0, 0.9, 0.6),
    basket=(b_basket, [{}, dict(tipped=True), {}], 0, 0.6, 0.75),
    pot=(b_pot_broken, [{}, {}, {}], 0, 0.9, 0.5),
    sack=(b_sack, [{}, dict(pile=True), dict(lying=True)], 0, 0.8, 0.8),
    cart=(b_cart, [{}, dict(loaded=True)], 0, 1.9, 2.2),
    rut=(b_rut, [{}, {}, {}], 1, 2.0, 0.1),
    puddle=(b_puddle, [{}, {}, {}], 1, 1.0, 0.1),
    firewood=(b_firewood, [{}, {}], 0, 1.0, 0.8),
    arrows=(b_arrows, [{}, {}, {}], 0, 1.0, 1.4),
    mat=(b_mat, [{}, dict(two=True)], 0, 1.0, 0.5),
    rope=(b_rope, [{}, {}], 0, 0.8, 0.3),
    helmet=(b_helmet, [{}, dict(side=True), {}], 0, 0.5, 0.8),
    jar=(b_jar, [{}, dict(tipped=True), {}], 0, 0.6, 1.3),
    hedge=(b_hedge, [{}, {}, {}], 0, 11.0, 2.5),
    trees=(b_trees, [{}, {}, {}], 0, 4.5, 8.0),
    haystack=(b_haystack, [{}, {}], 0, 2.6, 5.0),
    ridge=(b_ridge, [{}, {}, {}], 1, 12.0, 0.6),
    hut=(b_hut, [{}, {}], 0, 3.8, 5.0),
)
GAIN = dict(tuft_straw=1.4, tuft_grass=1.4, tuft_trample=1.5, stone=1.2, hay=1.1, helmet=1.2)
BRIGHT = ('puddle',)                      # kinds that glint: never in the caption band
NOSHADOW = ('puddle', 'rut', 'ridge')

WEIGHTS = dict(
    jimo_in=dict(tuft_straw=14, tuft_grass=6, hay=7, stone=11, rut=5, puddle=4, basket=5, pot=5, cart=1.3, sack=5, reeds=3, rope=1),
    jimo_out=dict(tuft_straw=10, tuft_grass=14, hay=5, stone=11, rut=5, puddle=4, basket=4, pot=4, cart=1.2, sack=4, reeds=6),
    yan_camp=dict(tuft_trample=18, rock=9, firewood=4, arrows=6, mat=4, rope=4, helmet=4, jar=4, tuft_straw=6, stone=4),
    vista=dict(hedge=9, trees=7, haystack=8, ridge=8, hut=3),
)
def _zone_mult(loc, x, y):
    if loc == 'jimo_out':
        if abs(x) < 6.2 and y < -30: return dict(rut=2.4, puddle=2.0, stone=1.3, sack=1.5, tuft_grass=0.4, reeds=0.3, basket=1.4, cart=1.5)
        return dict(tuft_grass=1.2, reeds=1.3, rut=0.4, cart=0.6)
    if loc == 'jimo_in':
        if y < 13.0: return dict(basket=1.6, sack=1.4, pot=1.5, rut=1.6, cart=1.4)
        return dict(hay=1.4, tuft_straw=1.2, rut=1.4)
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
    for fi, p in enumerate(me.polygons): p.material_index = mb.mi[fi]; p.use_smooth = False
    me.materials.append(J.T.mat_ink())                                  # the ink slot of the hull (modifier material_offset)
    TP[key] = (me, fp); return TP[key]

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

def _poses(cam, frames, nmax=9):
    scene = bpy.context.scene; cam = bpy.data.objects[cam] if isinstance(cam, str) else (cam or scene.camera)
    assert cam is not None, 'dress_ground: no camera (pose one with J.shot_camera / J.make_camera first)'
    if frames is None: bpy.context.view_layer.update(); return [_pose(cam, scene)], cam
    fl = [int(frames)] if isinstance(frames, (int, float)) else sorted(set(int(f) for f in frames))
    if len(fl) > nmax: fl = [fl[round(i * (len(fl) - 1) / (nmax - 1))] for i in range(nmax)]
    f0 = scene.frame_current; out = []
    for f in fl: scene.frame_set(f); bpy.context.view_layer.update(); out.append(_pose(cam, scene))
    scene.frame_set(f0); bpy.context.view_layer.update(); return out, cam

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

def default_keep_clear(preset=None, r=1.5):
    """[(x, y, radius)] for the shot's stand marks, herd lanes and road path (jimo_shots marks, z <= 3 only). Every mark and every herd position gets `r` = 1.5 D.
    `preset` default = the built shot."""
    _bind(); import jimo_shots as S
    preset = preset or J.STATE.get('preset'); out = []
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
def dress_ground(cam=None, density=1.0, seed=0, keep_clear=None, frames=None):
    """Scatter lit, inked, instanced ground dressing where the camera sees the ground (API.md). Returns dict(n, kinds, poses, far, keep_clear, share_cap).
    cam: camera object / name (default scene camera, already posed: J.shot_camera / J.key_camera). frames: film frames of a keyed camera; the union of the frustums
    (<= 9 evenly spread samples) is dressed. density 1.0 = about one prop per 13 px square of the ground on a 360 x 640 frame, 0 = nothing. seed: deterministic. keep_clear: [(x, y, r)]
    circles that stay empty; None = default_keep_clear() of the shot, [] = none."""
    _bind(); S = J.STATE; loc = S['loc']; light = S['light']; clear_dressing()
    if density <= 0: return dict(n=0, kinds={}, poses=0)
    poses, camo = _poses(cam, frames); kc = default_keep_clear() if keep_clear is None else [tuple(float(v) for v in c) for c in keep_clear]
    far = 42.0 if loc != 'vista' else 520.0; vista = loc == 'vista'; cell = 0.5 if not vista else 2.0
    # ---- 1. candidate samples in screen space (stratified, jittered), one list per pose
    RW, RH = 360, 640; step = (13.0 if loc != 'vista' else 34.0) / math.sqrt(density); nxs, nys = int(RW / step), int(RH / step); cands = []
    for pi, p in enumerate(poses):
        for gy in range(nys):
            for gx in range(nxs):
                r = random.Random(seed * 1000003 + pi * 7919 + gy * 131 + gx); u = (gx + r.random()) / nxs; v = 1.0 - (gy + r.random()) / nys
                d = _ray(p, u, v); h = _hit(loc, p, d)
                if h is None or h[3] > far or h[3] < max(0.6, p['clip']): continue
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
    STAT.clear(); W = WEIGHTS[loc]; placed = []; grid = {}; counts = {}; lens = camo.data.lens
    for (pi, gy, gx, rv, (x, y, z, t), u, v) in sorted(cands, key=lambda c: (c[1], c[2], c[0])):
        r = random.Random(seed * 7000003 + pi * 104729 + gy * 977 + gx * 31 + 5)
        if _exclude(loc, x, y): continue
        zm = _zone_mult(loc, x, y); names = [k for k in W]; ws = [W[k] * zm.get(k, 1.0) for k in names]
        # screen position in every pose: caption band (y > 880 / 1280) -> dim tone, no glints
        band = False; dmin = t
        for q in poses:
            pr = _project(q, V((x, y, z + 0.4)))
            if pr and 0 <= pr[0] <= 1 and 0 <= pr[1] <= 1 and (1 - pr[1]) > 0.66: band = True
            if pr: dmin = min(dmin, pr[2])
        if band: ws = [0.0 if k in BRIGHT else w for k, w in zip(names, ws)]
        if t < 2.8 and not vista: continue                                    # never right on the lens
        near = 1.0 if (vista or t > 10.0) else 0.38 + 0.62 * (t - 2.8) / 7.2
        if near < 1.0: ws = [0.0 if LIB[k][4] > 1.0 else w for k, w in zip(names, ws)]   # nothing tall close to a low camera
        kind = r.choices(names, ws)[0]; fn, variants, decal, size, height = LIB[kind]; vi = r.randrange(len(variants))
        # size: natural scale x jitter x distance boost (>= ~12 px at 360 x 640)
        f_px = lens / 36.0 * RH; want = 8.0
        boost = min(1.8 if not vista else 6.5 if kind in ('hedge', 'ridge') else 4.5, max(1.0, want * t / (max(0.35, height if not decal else 0.8) * f_px)))
        if vista: boost = min(boost, 2.6) if kind == 'hut' else boost
        s = r.uniform(0.85, 1.25) * boost * near * GAIN.get(kind, 1.0); rad = size * s
        if blocked(x, y, rad * 0.8): STAT['occ'] = STAT.get('occ', 0) + 1; continue
        if any(math.hypot(x - cx, y - cy) < cr + rad * 0.8 for (cx, cy, cr) in kc): STAT['keep'] = STAT.get('keep', 0) + 1; continue
        gk = (int(x // 3.0), int(y // 3.0)); hit_ = False
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for (px_, py_, pr_) in grid.get((gk[0] + dx, gk[1] + dy), ()):
                    if math.hypot(x - px_, y - py_) < (rad + pr_) * (0.6 if decal else 1.0): hit_ = True
        if hit_: STAT['dup'] = STAT.get('dup', 0) + 1; continue
        grid.setdefault(gk, []).append((x, y, rad))
        wm = J.warm_at(V((x, y, 0.6))); tone = (1 if wm > 0.22 else 0, 1 if band else 0)
        yaw = r.uniform(0, TAU); scl = (s, s, s)
        if kind == 'puddle': scl = (s * r.uniform(0.9, 1.7), s * r.uniform(0.6, 1.0), 1.0)
        STAT['ok'] = STAT.get('ok', 0) + 1
        placed.append((kind, vi, tone, (x, y, z + 0.005), yaw, scl, J.T.hull(dmin), band))
        counts[kind] = counts.get(kind, 0) + 1
        # a small cluster around some props (lived-in): one to three satellites of a cheap kind
        if not decal and not vista and t > 10.0 and r.random() < 0.3:
            for _ in range(r.randint(1, 3)):
                a = r.uniform(0, TAU); dd = rad * r.uniform(0.9, 1.6); x2, y2 = x + dd * math.cos(a), y + dd * math.sin(a); k2 = r.choice(('tuft_straw', 'tuft_grass', 'stone') if loc != 'yan_camp' else ('tuft_trample', 'stone'))
                if _exclude(loc, x2, y2) or blocked(x2, y2, 0.5 * s) or any(math.hypot(x2 - cx, y2 - cy) < cr + 0.5 * s for (cx, cy, cr) in kc): continue
                placed.append((k2, r.randrange(len(LIB[k2][1])), tone, (x2, y2, z + 0.005), r.uniform(0, TAU), (s * 0.8,) * 3, J.T.hull(dmin), band)); counts[k2] = counts.get(k2, 0) + 1
    # ---- 2. build: one shared mesh per (kind, variant, tone), one object per prop
    cap = int(1100 * min(2.0, density));
    if len(placed) > cap: placed = placed[::1][:cap]
    for i, pl in enumerate(placed): _spawn(pl[0], pl[1], pl[2], pl[3], pl[4], pl[5], pl[6], i)
    return dict(n=len(placed), kinds=counts, stat=dict(STAT, cand=len(cands)), poses=len(poses), far=far, keep_clear=len(kc), templates=len(S.get('dg_tpl', {})))

if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'share':
        for f in sys.argv[2:]: print('%.3f  %s' % (ground_share(f), f))
    else: print(__doc__)

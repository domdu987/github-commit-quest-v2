#!/usr/bin/env python3
"""ghost_tex.py : painted textures of the film-23 set ("ไอ้กองทัพลูกโป่ง", the Ghost Army, Normandy 1944).
numpy + PIL, deterministic, cached in tex_ghost/ by a hash of the painter parameters + TEX_V (bump TEX_V after editing a painter).
Also holds the shared field layout (patchwork of fields, hedgerows, lane, river) so the ground texture and the 3D hedges agree.

    import ghost_tex as GX
    tx = GX.ensure(['sky_dawn', 'fields_dawn', ...])    # {name: png path}
World: 1 unit = 1 D (a head), Z up.  Ground image: u = (x - x0) / W, v = (y - y0) / H   (row 0 of the PNG = the top = highest y)."""
import os, sys, math, json, hashlib, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, 'tex_ghost')
TEX_V = 'g23.15'
JOBS = {}
FONT_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_N = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'

def hexf(h): h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], 'float32')
def hex8(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def fbm(H, W, base, octs=4, seed=0, tile=False):
    """fbm value noise in [0,1]; `base` = grid cells along the long side at octave 0."""
    rs = np.random.RandomState(seed); out = np.zeros((H, W), 'float32'); amp = 1.0; tot = 0.0
    for o in range(octs):
        n = base * (2 ** o); gx = max(2, int(round(n * W / max(H, W)))); gy = max(2, int(round(n * H / max(H, W))))
        g = rs.rand(gy, gx).astype('float32')
        if tile:
            g3 = np.tile(g, (3, 3)); big = np.asarray(Image.fromarray(g3, 'F').resize((3 * W, 3 * H), Image.BICUBIC)); out += amp * big[H:2 * H, W:2 * W]
        else: out += amp * np.asarray(Image.fromarray(g, 'F').resize((W, H), Image.BICUBIC))
        tot += amp; amp *= 0.5
    return out / tot

def save(arr, out, alpha=None):
    a = np.clip(arr, 0, 1)
    if alpha is not None:
        im = np.concatenate([a, np.clip(alpha, 0, 1)[..., None]], 2); Image.fromarray((im * 255 + 0.5).astype('uint8'), 'RGBA').save(out)
    else: Image.fromarray((a * 255 + 0.5).astype('uint8'), 'RGB').save(out)

def reg(name, params, fn): JOBS[name] = (params, fn)

def spline(pts, n=14):
    """Catmull-Rom through pts -> dense polyline."""
    P = [pts[0]] + list(pts) + [pts[-1]]; out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n; t2 = t * t; t3 = t2 * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in range(2)))
    out.append(tuple(pts[-1])); return out

def dist_poly(x, y, poly):
    best = 1e9
    for (ax, ay), (bx, by) in zip(poly, poly[1:]):
        dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy or 1e-9; t = max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / L2)); d = math.hypot(x - ax - t * dx, y - ay - t * dy)
        if d < best: best = d
    return best

# ============================================================================= scenes (world layout shared with ghost.py)
LANE1 = spline([(-42, -130), (-30, -70), (-18, -20), (-6, 30), (8, 72), (16, 112), (10, 152), (-6, 192), (-14, 232), (-6, 262), (12, 296), (34, 330), (44, 372)], 10)
RIVER1 = spline([(-270, 244), (-210, 262), (-150, 290), (-90, 286), (-40, 266), (10, 258), (60, 272), (120, 300), (190, 298), (270, 282)], 10)
LANE2 = spline([(-6, -40), (-4, -10), (0, 14), (8, 46), (18, 84), (30, 126), (40, 170)], 12)
LANE3 = spline([(-30, -90), (-26, -40), (-18, 0), (-10, 30), (-16, 70), (-30, 110)], 10)
SCENES = dict(
    dawn=dict(rect=(-270, 270, -130, 450), res=4096, xs=[-270 + 540 * i / 14 for i in range(15)], ys=[-130 + 580 * j / 17 for j in range(18)], jit=0.24, seed=11, lane=LANE1, lane_w=7.0, river=RIVER1, river_w=10.0, pal='day', hedge_p=0.55),
    morning=dict(rect=(-80, 80, -40, 150), res=4096, xs=[-80, -14, 16, 80], ys=[-40, 40, 150], jit=0.02, seed=5, lane=LANE2, lane_w=9.0, river=None, river_w=0, pal='day', hedge_p=1.0, warp=1.2),
    night=dict(rect=(-130, 130, -100, 160), res=4096, xs=[-130, -58, 20, 62, 130], ys=[-100, -8, 66, 160], jit=0.06, seed=7, lane=LANE3, lane_w=8.0, river=None, river_w=0, pal='night', hedge_p=1.0, warp=2.0),
)

def warp(x, y, a=3.4, seed=0):
    return (x + a * math.sin(0.045 * y + 0.021 * x + seed) + 0.6 * a * math.sin(0.11 * x - 0.07 * y + 2 * seed),
            y + a * math.cos(0.037 * x - 0.019 * y + seed * 1.7) + 0.5 * a * math.sin(0.09 * y + 0.05 * x))

_LAY = {}
def layout(sc):
    """Field patchwork of a scene: dict(cells=[dict(poly, col, kind, ang)], edges=[dict(pts, hedge)])."""
    if sc in _LAY: return _LAY[sc]
    c = SCENES[sc]; rng = random.Random(c['seed']); xs, ys = c['xs'], c['ys']; nx, ny = len(xs) - 1, len(ys) - 1; jit = c['jit']; wa = c.get('warp', 3.4)
    V = [[None] * (ny + 1) for _ in range(nx + 1)]
    for i in range(nx + 1):
        for j in range(ny + 1):
            dx = (xs[min(i + 1, nx)] - xs[max(i - 1, 0)]) / 2; dy = (ys[min(j + 1, ny)] - ys[max(j - 1, 0)]) / 2
            jx = rng.uniform(-jit, jit) * dx if 0 < i < nx else 0.0; jy = rng.uniform(-jit, jit) * dy if 0 < j < ny else 0.0
            V[i][j] = (xs[i] + jx, ys[j] + jy)
    def poly(a, b, n=None):
        L = math.hypot(b[0] - a[0], b[1] - a[1]); n = n or max(2, int(L / 5)); pts = []
        for k in range(n + 1):
            t = k / n; p = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            edge = (k == 0 or k == n)
            pts.append(warp(p[0], p[1], wa, c['seed']) if not (abs(p[0]) >= abs(xs[0]) - 1e-3 or abs(p[0]) >= abs(xs[-1]) - 1e-3 or p[1] <= ys[0] + 1e-3 or p[1] >= ys[-1] - 1e-3) else p)
        return pts
    H = {}; Vv = {}
    for i in range(nx):
        for j in range(ny + 1): H[(i, j)] = poly(V[i][j], V[i + 1][j])
    for i in range(nx + 1):
        for j in range(ny): Vv[(i, j)] = poly(V[i][j], V[i][j + 1])
    edges = []
    for k, pts in list(H.items()) + list(Vv.items()):
        border = (k in H and k[1] in (0, ny)) or (k in Vv and k[0] in (0, nx))
        edges.append(dict(pts=pts, hedge=(not border) and rng.random() < c['hedge_p'], key=k))
    pal = ['#5cb026', '#6cc22e', '#4ea01c', '#8acb34', '#46921c', '#62bf26', '#9ad036', '#52a822'] if c['pal'] == 'day' else ['#3a9a2a', '#4cae30', '#348a26', '#62b238', '#389428']
    cells = []
    for i in range(nx):
        for j in range(ny):
            pts = list(H[(i, j)]) + list(Vv[(i + 1, j)]) + list(reversed(H[(i, j + 1)])) + list(reversed(Vv[(i, j)]))
            r = rng.random(); kind = 'grass'
            if r < 0.17: kind = 'wheat'
            elif r < 0.24: kind = 'plough'
            elif r < 0.34: kind = 'clover'
            cells.append(dict(poly=pts, col=rng.choice(pal), kind=kind, ang=rng.uniform(0, math.pi), idx=len(cells), ij=(i, j)))
    _LAY[sc] = dict(cells=cells, edges=edges); return _LAY[sc]

# ============================================================================= ground
def paint_ground(p, out):
    sc = p['scene']; c = SCENES[sc]; x0, x1, y0, y1 = c['rect']; R = c['res']; rs = np.random.RandomState(c['seed']); Lay = layout(sc)
    W_, H_ = x1 - x0, y1 - y0
    def P(pt): return ((pt[0] - x0) / W_ * R, (y1 - pt[1]) / H_ * R)
    lab = Image.new('I', (R, R), 0); dr = ImageDraw.Draw(lab)
    for cell in Lay['cells']: dr.polygon([P(q) for q in cell['poly']], fill=cell['idx'] + 1)
    lab = np.asarray(lab); N = len(Lay['cells']) + 1
    base = np.zeros((N, 3), 'float32'); ang = np.zeros(N, 'float32'); per = np.ones(N, 'float32') * 4.0; kind = np.zeros(N, 'int32'); ph = np.zeros(N, 'float32')
    for cell in Lay['cells']:
        i = cell['idx'] + 1; col = hexf(cell['col']); k = cell['kind']
        if k == 'wheat': col = hexf('#d8b838') * 0.9 + 0.1 * col
        elif k == 'plough': col = hexf('#94653a')
        elif k == 'clover': col = hexf('#5ccc38')
        base[i] = col; ang[i] = cell['ang']; per[i] = rs.uniform(5.0, 9.0) if k != 'plough' else rs.uniform(2.4, 3.2); kind[i] = {'grass': 0, 'wheat': 1, 'plough': 2, 'clover': 3}[k]; ph[i] = rs.uniform(0, 6.3)
    img = base[lab]
    xw = (np.arange(R, dtype='float32') + 0.5) / R * W_ + x0; yw = y1 - (np.arange(R, dtype='float32') + 0.5) / R * H_
    ca, sa = np.cos(ang[lab]), np.sin(ang[lab]); proj = xw[None, :] * ca + yw[:, None] * sa
    st = np.sin(proj * (2 * math.pi) / per[lab] + ph[lab]); sm = (st > 0).astype('float32') * 0.5 + 0.5 * st * 0.5 + 0.5
    # r3: real field texture - mown grass in broad soft two-tone stripes (the light stripe yellower), wheat in fine crop rows with tramlines,
    # plough in strong furrows with lit ridges, clover in mid stripes; visible in sun AND in shade (luminance carries through the shade tint)
    K = kind[lab]; prow = per[lab]
    rows = np.sin(proj * (2 * math.pi) / 1.25 + ph[lab]); tram = (np.abs(np.sin(proj * math.pi / 13.0 + ph[lab])) < 0.07).astype('float32')
    fur = np.sin(proj * (2 * math.pi) / 1.7 + ph[lab]); ridge = np.clip(fur, 0, 1) ** 3
    smooth_st = np.clip(st * 2.2, -1, 1) * 0.5 + 0.5
    mow = np.where(K == 2, 0.76 + 0.24 * (fur * 0.5 + 0.5) + 0.10 * ridge,
          np.where(K == 1, (0.91 + 0.09 * rows) * (1 - 0.2 * tram), 0.89 + 0.15 * smooth_st))
    n1 = fbm(R, R, 7, 5, c['seed'] + 1); n2 = fbm(R, R, 48, 3, c['seed'] + 2)
    img = img * (mow * (0.88 + 0.24 * n1) * (0.93 + 0.14 * n2))[..., None]
    yel = ((K == 0) | (K == 3)) * smooth_st * 0.07; img = img * (1 - yel[..., None]) + yel[..., None] * hexf('#c8e040')
    wh = (kind[lab] == 1)[..., None]; img = np.where(wh, img * (0.92 + 0.2 * fbm(R, R, 160, 2, 3)[..., None]), img)
    # hedge shadow bands (dark, soft) under the 3D hedges
    m = Image.new('L', (R, R), 0); d = ImageDraw.Draw(m)
    for e in Lay['edges']:
        if e['hedge']: d.line([P(q) for q in e['pts']], fill=255, width=max(2, int(4.4 / W_ * R)), joint='curve')
    m = np.asarray(m.filter(ImageFilter.GaussianBlur(R / W_ * 1.0))).astype('float32') / 255
    img = img * (1 - 0.62 * m[..., None]) + 0.62 * m[..., None] * hexf('#22561a')
    # grass wear / flowers (white-yellow dots in some fields)
    fl = (fbm(R, R, 220, 1, 9) > 0.86).astype('float32') * (kind[lab] == 3) * 0.45
    img = img * (1 - fl[..., None]) + fl[..., None] * hexf('#ffe86a')
    # river
    glint = np.zeros((R, R), 'float32')
    if c.get('river'):
        bank = Image.new('L', (R, R), 0); db = ImageDraw.Draw(bank); riv = Image.new('L', (R, R), 0); dv = ImageDraw.Draw(riv)
        db.line([P(q) for q in c['river']], fill=255, width=int((c['river_w'] + 5) / W_ * R), joint='curve'); dv.line([P(q) for q in c['river']], fill=255, width=int(c['river_w'] / W_ * R), joint='curve')
        bank = np.asarray(bank.filter(ImageFilter.GaussianBlur(R / W_ * 0.8))).astype('float32') / 255; riv = np.asarray(riv.filter(ImageFilter.GaussianBlur(R / W_ * 0.25))).astype('float32') / 255
        img = img * (1 - 0.85 * bank[..., None]) + 0.85 * bank[..., None] * hexf('#cdbd7c')
        wcol = hexf('#2f93d0')[None, None] * (0.85 + 0.3 * fbm(R, R, 30, 3, 4)[..., None]) + 0.25 * (fbm(R, R, 90, 2, 5) > 0.7)[..., None] * hexf('#bfe8ff')
        img = img * (1 - riv[..., None]) + riv[..., None] * wcol
        gl = Image.new('L', (R, R), 0); dg = ImageDraw.Draw(gl); rr = random.Random(5)
        for _ in range(2200):
            q = c['river'][rr.randrange(len(c['river']))]; x = q[0] + rr.uniform(-4, 4); y = q[1] + rr.uniform(-4, 4); l = rr.uniform(1.2, 3.8)
            px_, py_ = P((x, y)); dg.line([(px_, py_), (px_ + l / W_ * R, py_)], fill=rr.randrange(150, 255), width=max(1, int(0.28 / W_ * R)))
        glint = np.asarray(gl.filter(ImageFilter.GaussianBlur(0.8))).astype('float32') / 255 * riv
    # lane
    ln = c['lane']; lw = c['lane_w']
    shoulder = Image.new('L', (R, R), 0); ds = ImageDraw.Draw(shoulder); ds.line([P(q) for q in ln], fill=255, width=int((lw + 3.6) / W_ * R), joint='curve')
    lane = Image.new('L', (R, R), 0); dl = ImageDraw.Draw(lane); dl.line([P(q) for q in ln], fill=255, width=int(lw / W_ * R), joint='curve')
    ruts = Image.new('L', (R, R), 0); dru = ImageDraw.Draw(ruts)
    for off in (-1.9, 1.9):
        pts = []
        for (ax, ay), (bx, by) in zip(ln, ln[1:]):
            dx, dy = bx - ax, by - ay; L = math.hypot(dx, dy) or 1; nx_, ny_ = -dy / L, dx / L; pts.append((ax + nx_ * off, ay + ny_ * off))
        dru.line([P(q) for q in pts], fill=255, width=int(1.25 / W_ * R), joint='curve')
    shoulder = np.asarray(shoulder.filter(ImageFilter.GaussianBlur(R / W_ * 0.9))).astype('float32') / 255
    lane = np.asarray(lane.filter(ImageFilter.GaussianBlur(R / W_ * 0.22))).astype('float32') / 255; ruts = np.asarray(ruts.filter(ImageFilter.GaussianBlur(R / W_ * 0.3))).astype('float32') / 255
    ctr = fbm(R, R, 300, 2, 6)
    dirt = hexf('#b3a07c')[None, None] * (0.82 + 0.3 * fbm(R, R, 40, 3, 7)[..., None]) * (0.92 + 0.14 * ctr[..., None])
    dirt = dirt * (1 - 0.32 * ruts[..., None]) + 0.32 * ruts[..., None] * hexf('#7a4a28')
    pebb = (fbm(R, R, 500, 1, 8) > 0.84).astype('float32'); dirt = dirt * (1 - 0.35 * pebb[..., None]) + 0.35 * pebb[..., None] * hexf('#efe0b8')
    tuft = (fbm(R, R, 60, 3, 12) > 0.62).astype('float32') * np.clip(1 - np.abs(lane * 2 - 1) * 0 - ruts * 3, 0, 1) * lane   # grass strip between ruts
    mid = np.clip(shoulder - lane, 0, 1)
    img = img * (1 - 0.55 * mid[..., None]) + 0.55 * mid[..., None] * (hexf('#79b83a')[None, None] * 0.9)
    img = img * (1 - lane[..., None]) + lane[..., None] * dirt
    img = img * (1 - 0.7 * tuft[..., None] * 0.5) + 0.7 * tuft[..., None] * 0.5 * hexf('#58b034')
    img = img * (0.97 + 0.06 * fbm(R, R, 700, 1, 13)[..., None])
    save(img, out); save(np.stack([glint * 1.0, glint * 0.95, glint * 0.8], -1), out.replace('.png', '_glint.png'))

for _s in SCENES: reg('fields_' + _s, dict(scene=_s, pal=SCENES[_s]['pal']), paint_ground)

def paint_detail(p, out):
    """Tileable grass micro detail (multiply, mean about 0.8): blades, specks."""
    S = 1024; rs = np.random.RandomState(4)
    a = 0.62 + 0.55 * fbm(S, S, 128, 4, 1, tile=True); b = fbm(S, S, 512, 1, 2, tile=True)
    blades = (b > 0.66).astype('float32') * 0.35 - (b < 0.28).astype('float32') * 0.22
    v = np.clip(a + blades, 0.35, 1.25) * 0.82; save(np.repeat(v[..., None], 3, 2), out)
reg('grass_detail', {}, paint_detail)

def paint_dirt(p, out):
    """Tileable lane dirt (u along the lane): warm ochre packed earth, darker damp patches, pebbles, a few straw bits; 1 tile = 4 D."""
    S = 1024; rs = random.Random(p['seed'])
    n1 = fbm(S, S, 6, 4, 21, tile=True); n2 = fbm(S, S, 40, 3, 22, tile=True); n3 = fbm(S, S, 160, 2, 23, tile=True)
    img = hexf(p['col'])[None, None] * (0.80 + 0.30 * n1[..., None]) * (0.90 + 0.16 * n2[..., None]) * (0.95 + 0.1 * n3[..., None])
    damp = np.clip((fbm(S, S, 5, 3, 24, tile=True) - 0.58) * 6, 0, 1); img = img * (1 - 0.35 * damp[..., None]) + 0.35 * damp[..., None] * hexf('#6a4424')
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(im)
    for _ in range(420):
        x, y, r = rs.uniform(0, S), rs.uniform(0, S), rs.uniform(2.5, 7); c = rs.choice(['#e8d8b0', '#cdb88c', '#9a8460', '#f0e4c8', '#7a6448'])
        for ox in (-S, 0, S):
            for oy in (-S, 0, S): d.ellipse([x + ox - r, y + oy - r * 0.75, x + ox + r, y + oy + r * 0.75], fill=hex8(c), outline=hex8('#5a4430'))
    for _ in range(70):
        x, y, a, l = rs.uniform(0, S), rs.uniform(0, S), rs.uniform(0, 6.3), rs.uniform(14, 34)
        for ox in (-S, 0, S):
            for oy in (-S, 0, S): d.line([x + ox, y + oy, x + ox + l * math.cos(a), y + oy + l * math.sin(a)], fill=hex8('#e8c860'), width=2)
    save(np.asarray(im).astype('float32') / 255, out)
reg('dirt', dict(col='#c49860', seed=3), paint_dirt)

def paint_rut(p, out):
    """Tileable rut bottom (u along the rut, v across, 1 tile = 2 D along x 1 D across): dark damp earth with tyre/track tread chevrons, wet sheen streak."""
    W, H = 1024, 512; rs = random.Random(5)
    n1 = fbm(H, W, 8, 4, 31, tile=True); img = hexf('#7a5230')[None, None] * (0.78 + 0.34 * n1[..., None])
    vv = (np.arange(H, dtype='float32') + 0.5) / H; edge = np.clip(np.abs(vv - 0.5) * 2, 0, 1) ** 2; img = img * (1 - 0.35 * edge[:, None, None]) + 0.35 * edge[:, None, None] * hexf('#b08a5a')
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(im)
    for k in range(16):                                                    # chevron tread (track pads of the trucks)
        x = k * W / 16
        for ox in (-W, 0, W):
            d.line([x + ox, H * 0.22, x + ox + 22, H * 0.5, x + ox, H * 0.78], fill=hex8('#4e321c'), width=14)
            d.line([x + ox + 9, H * 0.24, x + ox + 31, H * 0.5, x + ox + 9, H * 0.76], fill=hex8('#9a7448'), width=4)
    a = np.asarray(im).astype('float32') / 255
    wet = np.exp(-((vv - 0.42) / 0.07) ** 2)[:, None] * (0.5 + 0.5 * fbm(H, W, 6, 2, 33, tile=True)); a = a * (1 - 0.25 * wet[..., None]) + 0.25 * wet[..., None] * hexf('#a8b8c8')
    save(a, out)
reg('rut', {}, paint_rut)

# ============================================================================= sky dome (u = azimuth/360 from +x CCW, v = (elevation + 15) / 105)
SKY_W = 4096
def paint_sky(p, out):
    mode = p['mode']; sun = p['sun']; W = SKY_W; H = int(round(W * 105 / 360)); rs = np.random.RandomState({'dawn': 3, 'morning': 5, 'night': 9}[mode])
    el = 90.0 - (np.arange(H, dtype='float32') + 0.5) / H * 105.0; az = (np.arange(W, dtype='float32') + 0.5) / W * 2 * math.pi
    E = np.radians(el)[:, None] * np.ones((1, W), 'float32'); A = np.ones((H, 1), 'float32') * az[None, :]
    dx, dy, dz = np.cos(E) * np.cos(A), np.cos(E) * np.sin(A), np.sin(E)
    def grad(stops):
        e = np.clip(el, -15, 90); o = np.zeros((H, 3), 'float32')
        for ch in range(3): o[:, ch] = np.interp(e, [s[0] for s in stops], [hexf(s[1])[ch] for s in stops])
        return np.repeat(o[:, None, :], W, 1)
    sx, sy, sz = math.cos(math.radians(sun[1])) * math.cos(math.radians(sun[0])), math.cos(math.radians(sun[1])) * math.sin(math.radians(sun[0])), math.sin(math.radians(sun[1]))
    dd = np.degrees(np.arccos(np.clip(dx * sx + dy * sy + dz * sz, -1, 1)))
    ppd = W / 360.0
    def clouds(img, n, lo, hi, c_top, c_body, c_bot, wr, hr, seed, warm=None, wk=0.0):
        rr = np.random.RandomState(seed); out_ = img.copy()
        for _ in range(n):
            az0 = rr.uniform(0, 360); e0 = rr.uniform(lo, hi); wd = rr.uniform(*wr) / max(0.35, math.cos(math.radians(e0))); hd = rr.uniform(*hr); by = (90 - e0) / 105 * H; nd = rr.randint(4, 9)
            x0, x1 = int(az0 * ppd - wd * ppd * 0.7), int(az0 * ppd + wd * ppd * 0.7); y0, y1 = int(by - hd * ppd * 2.6), int(by + 2)
            if y0 < 0 or y1 >= H: continue
            xs = np.arange(x0, x1) % W; X = np.arange(x0, x1)[None, :].astype('float32'); Y = np.arange(y0, y1)[:, None].astype('float32'); cov = np.zeros((y1 - y0, x1 - x0), 'float32'); top = np.zeros_like(cov)
            for k in range(nd):
                u = (k + 0.5) / nd - 0.5; cx = az0 * ppd + u * wd * ppd * 1.05 + rr.uniform(-0.05, 0.05) * wd * ppd; rd = hd * ppd * rr.uniform(0.7, 1.25) * (1.0 - 1.8 * u * u); cy = by - rd * rr.uniform(0.15, 0.5)
                d = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2); cov = np.maximum(cov, np.clip((rd - d) / (0.5 + 0.22 * rd) + 0.5, 0, 1))
                top = np.maximum(top, np.clip(rd * 0.82 - np.sqrt((X - cx + rd * 0.12) ** 2 + (Y - cy + rd * 0.3) ** 2) + 0.5, 0, 1))
            cov = cov * np.clip((by - Y) / (0.25 * hd * ppd) + 0.5, 0, 1); bot = np.clip((Y - (by - hd * ppd * 0.9)) / (hd * ppd * 0.9), 0, 1) ** 1.3 * 0.75
            tcol = hexf(c_top)[None, None] * np.ones_like(cov)[..., None]
            if warm is not None: tcol = tcol + (np.exp(-(dd[y0:y1][:, xs] / wk) ** 2))[..., None] * hexf(warm) * 0.45
            col = hexf(c_body)[None, None] * (1 - top[..., None]) + tcol * top[..., None]; col = col * (1 - bot[..., None]) + hexf(c_bot)[None, None] * bot[..., None]
            sl = out_[y0:y1][:, xs]; out_[y0:y1, :][:, xs] = sl * (1 - cov[..., None]) + col * cov[..., None]
        return out_
    if mode == 'dawn':    # clear blue dawn: deep blue zenith, cyan-blue mid, warm gold rim only at the horizon near the sun
        img = grad([(-15, '#f4c890'), (0, '#ffe0b0'), (2.2, '#cfe0f4'), (5, '#7cc0f6'), (9, '#3c92ee'), (18, '#2878dc'), (40, '#2460cc'), (90, '#1c4cb8')])
        warm = np.exp(-(dd / 50.0) ** 2) * np.exp(-np.clip(el, -2, 90)[:, None] / 3.2)
        img = img * (1 - warm[..., None] * 0.85) + warm[..., None] * 0.85 * hexf('#ffb865')
        img += (np.exp(-(dd / 1.6) ** 2) * 1.0)[..., None] * hexf('#fff4d0'); img += (np.exp(-(dd / 7.0) ** 2) * 0.35)[..., None] * hexf('#ffd890')
        img = clouds(img, 70, 4, 32, '#fff0d0', '#f0dcd8', '#c8cfe8', (6, 18), (0.9, 2.2), 21, '#ffd890', 40.0)
    elif mode == 'morning':
        img = grad([(-15, '#f6c880'), (0, '#ffd490'), (3, '#bcd8f4'), (8, '#78b4f0'), (25, '#3e88e4'), (90, '#2257c8')])
        img += (np.exp(-(dd / 2.0) ** 2) * 1.0)[..., None] * hexf('#fff4d0'); img += (np.exp(-(dd / 10.0) ** 2) * 0.3)[..., None] * hexf('#ffe0a0')
        img = clouds(img, 44, 6, 40, '#fff6e0', '#f8e4d8', '#d0d4ea', (10, 26), (1.6, 3.4), 23, '#ffe4a8', 50.0)
    else:   # night: deep blue gradient, soft moon glow, stars, a few cool clouds
        img = grad([(-15, '#1c2c66'), (0, '#2a4690'), (6, '#2c4aa0'), (20, '#1a3080'), (50, '#101e5c'), (90, '#0a1244')])
        img += (np.exp(-(dd / 14.0) ** 2) * 0.22)[..., None] * hexf('#6a8cf0'); img += (np.exp(-(dd / 4.0) ** 2) * 0.35)[..., None] * hexf('#a0c0ff')
        img = np.where((dd < 3.1)[..., None], hexf('#f4f8ff')[None, None] * 1.0, img); img += np.where(((dd >= 3.1) & (dd < 3.5))[..., None], 0.4, 0.0)
        rs2 = np.random.RandomState(31); stars = np.zeros((H, W), 'float32')
        for _ in range(1500):
            y_ = int(rs2.beta(1.2, 1.0) * (H * 0.86)); x_ = rs2.randint(0, W); b_ = rs2.uniform(0.35, 1.0)
            stars[y_, x_] = max(stars[y_, x_], b_)
            if rs2.random() < 0.12:
                for dy_, dx_ in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                    if 0 <= y_ + dy_ < H: stars[y_ + dy_, (x_ + dx_) % W] = max(stars[y_ + dy_, (x_ + dx_) % W], b_ * 0.5)
        stars *= np.clip((el[:, None] - 3.0) / 5.0, 0, 1)
        img = img * (1 - np.clip(stars, 0, 1)[..., None]) + np.clip(stars, 0, 1)[..., None] * hexf('#fffbe8')
        img = clouds(img, 22, 6, 34, '#5a7cd0', '#3a54a6', '#22308a', (10, 26), (1.4, 3.0), 25, '#7a9cf0', 25.0)
    save(np.clip(img, 0, 1), out)
reg('sky_dawn', dict(mode='dawn', sun=(140.0, 6.0)), paint_sky)
reg('sky_morning', dict(mode='morning', sun=(172.0, 22.0)), paint_sky)
reg('sky_night', dict(mode='night', sun=(64.0, 17.0)), paint_sky)

# ============================================================================= glow images
def paint_glow(p, out):
    S = 256; y, x = np.mgrid[0:S, 0:S].astype('float32'); r = np.hypot(x - S / 2 + 0.5, y - S / 2 + 0.5) / (S / 2); a = np.clip(1 - r, 0, 1) ** 2.2
    save(np.ones((S, S, 3), 'float32'), out, alpha=a)
reg('glow', {}, paint_glow)
def paint_pool(p, out):
    S = 256; y, x = np.mgrid[0:S, 0:S].astype('float32'); r = np.hypot(x - S / 2 + 0.5, y - S / 2 + 0.5) / (S / 2); a = np.clip(1 - r, 0, 1) ** 1.5
    save(np.ones((S, S, 3), 'float32'), out, alpha=a * (a > 0.02))
reg('pool', {}, paint_pool)
def paint_mist(p, out):
    S = 512; a = fbm(S, S, 6, 4, 3) ; y, x = np.mgrid[0:S, 0:S].astype('float32'); r = np.clip(1 - np.hypot((x - S / 2) / (S / 2), (y - S / 2) / (S / 2)), 0, 1)
    save(np.ones((S, S, 3), 'float32'), out, alpha=np.clip((a - 0.35) * 2.2, 0, 1) * r ** 0.8)
reg('mist', {}, paint_mist)

# ============================================================================= materials: stone, tile, wood, hedge, leaf, canvas, net, rubber, water
def paint_hedge(p, out):
    S = 512; img = Image.new('RGB', (S, S), hex8('#2a6a1c')); d = ImageDraw.Draw(img); rr = random.Random(3)
    cols = ['#24581a', '#2e7a20', '#3a9a26', '#52b630', '#1c4814', '#64c438']
    for _ in range(900):
        x, y, r = rr.uniform(0, S), rr.uniform(0, S), rr.uniform(8, 22); c = rr.choice(cols)
        for ox in (-S, 0, S):
            for oy in (-S, 0, S): d.ellipse([x + ox - r, y + oy - r, x + ox + r, y + oy + r * 0.8], fill=hex8(c))
    for _ in range(500):
        x, y, r = rr.uniform(0, S), rr.uniform(0, S), rr.uniform(3, 7)
        for ox in (-S, 0, S):
            for oy in (-S, 0, S): d.ellipse([x + ox - r, y + oy - r * 0.6, x + ox + r, y + oy + r * 0.6], fill=hex8(rr.choice(['#7ad858', '#6ccc4c', '#8ee060'])))
    for _ in range(90):
        x, y = rr.uniform(0, S), rr.uniform(0, S); c = rr.choice(['#fff4f0', '#ffe8f0', '#ff6a5a'])
        for ox in (-S, 0, S):
            for oy in (-S, 0, S): d.ellipse([x + ox - 3, y + oy - 3, x + ox + 3, y + oy + 3], fill=hex8(c))
    arr = np.asarray(img).astype('float32') / 255; arr *= (0.9 + 0.2 * fbm(S, S, 6, 3, 2, tile=True))[..., None]; save(arr, out)
reg('hedge', {}, paint_hedge)

def paint_leaf(p, out):
    S = 512; img = Image.new('RGB', (S, S), hex8(p['base'])); d = ImageDraw.Draw(img); rr = random.Random(p['seed'])
    for _ in range(700):
        x, y, r = rr.uniform(0, S), rr.uniform(0, S), rr.uniform(6, 18); c = rr.choice(p['cols'])
        for ox in (-S, 0, S):
            for oy in (-S, 0, S): d.ellipse([x + ox - r, y + oy - r, x + ox + r, y + oy + r * 0.85], fill=hex8(c))
    for _ in range(p.get('dots', 0)):
        x, y = rr.uniform(0, S), rr.uniform(0, S)
        for ox in (-S, 0, S):
            for oy in (-S, 0, S): d.ellipse([x + ox - 4, y + oy - 4, x + ox + 4, y + oy + 4], fill=hex8(p['dotc']))
    save(np.asarray(img).astype('float32') / 255, out)
reg('leaf', dict(base='#348a22', cols=['#266a1a', '#3a9a26', '#52b832', '#66cc3c', '#1f6018'], seed=4), paint_leaf)
reg('poplar', dict(base='#46aa2c', cols=['#2f8a28', '#5cc434', '#7ad83c', '#3a9c2c', '#a0e44c'], seed=6), paint_leaf)
reg('apple', dict(base='#3a9a26', cols=['#267a1c', '#46ae2c', '#5cc436', '#348c24'], seed=8, dots=60, dotc='#e83a2a'), paint_leaf)

def paint_roof(p, out):
    S = 512; img = np.zeros((S, S, 3), 'float32'); rows = 16; rh = S // rows; rs = np.random.RandomState(2)
    base = hexf(p['col']); nt = 8
    for r in range(rows):
        for t in range(nt * 2):
            w = S // nt; x0 = (t * w - (w // 2 if r % 2 else 0)); k = rs.uniform(0.82, 1.12)
            for xo in (0, S):
                a = x0 + xo; img[r * rh:(r + 1) * rh, max(0, a):min(S, a + w)] = base * k
    yy = (np.arange(S) % rh)[:, None] / rh
    img *= (0.75 + 0.35 * (1 - yy))[..., None]; img[(np.arange(S) % rh) < 2] *= 0.55
    xx = (np.arange(S) % (S // nt))[None, :]; img[:, ((np.arange(S) % (S // nt)) < 2)] *= 0.7
    img *= (0.9 + 0.2 * fbm(S, S, 10, 3, 5, tile=True))[..., None]
    save(img, out)
reg('roof_red', dict(col='#e03a1e'), paint_roof); reg('roof_red_d', dict(col='#b02a18'), paint_roof); reg('roof_slate', dict(col='#5a6a8e'), paint_roof)

def paint_stone(p, out):
    S = 512; rs = random.Random(p['seed']); img = Image.new('RGB', (S, S), hex8(p['mortar'])); d = ImageDraw.Draw(img); y = 0
    while y < S:
        h = rs.randint(28, 46); x = -rs.randint(0, 50)
        while x < S:
            w = rs.randint(44, 90); c = rs.choice(p['cols']); sh = rs.uniform(0.9, 1.08); col = tuple(min(255, int(v * sh)) for v in hex8(c))
            for xo in (0, S):
                d.rounded_rectangle([x + xo + 2, y + 2, x + xo + w - 2, y + h - 2], radius=7, fill=col)
                d.line([x + xo + 4, y + h - 4, x + xo + w - 4, y + h - 4], fill=tuple(int(v * 0.8) for v in col), width=3)
            x += w
        y += h
    arr = np.asarray(img).astype('float32') / 255; arr *= (0.88 + 0.24 * fbm(S, S, 14, 3, 3, tile=True))[..., None]; save(arr, out)
reg('stone_farm', dict(seed=1, mortar='#a8946c', cols=['#e8cc98', '#dcbc84', '#f0d8a8', '#d0b078', '#c8a468']), paint_stone)
reg('stone_wall', dict(seed=2, mortar='#7a7264', cols=['#b8b0a0', '#a8a090', '#c8bfae', '#9c9484', '#b4a692']), paint_stone)
reg('stone_church', dict(seed=3, mortar='#8a8a96', cols=['#c8c4cc', '#b8b4c0', '#d4d0d8', '#aaa6b4']), paint_stone)

def paint_planks(p, out):
    S = 512; rs = random.Random(p['seed']); img = Image.new('RGB', (S, S), hex8(p['dark'])); d = ImageDraw.Draw(img); n = p['n']; w = S // n
    for i in range(n):
        c = rs.choice(p['cols']); d.rectangle([i * w + 2, 0, (i + 1) * w - 2, S], fill=hex8(c))
        for _ in range(8):
            y = rs.randint(0, S); d.line([i * w + 5, y, (i + 1) * w - 5, y + rs.randint(-6, 6)], fill=tuple(int(v * 0.82) for v in hex8(c)), width=2)
    arr = np.asarray(img).astype('float32') / 255; arr *= (0.9 + 0.2 * fbm(S, S, 20, 3, 2, tile=True))[..., None]; save(arr, out)
reg('barn_wood', dict(seed=5, n=8, dark='#4a2e1a', cols=['#a8703c', '#9a6232', '#b57c44', '#8e5a2c']), paint_planks)
reg('wood', dict(seed=6, n=6, dark='#6a4224', cols=['#c8935a', '#bd8650', '#d29c62', '#b47c48']), paint_planks)

def paint_canvas(p, out):
    S = 256; y, x = np.mgrid[0:S, 0:S].astype('float32'); wv = 0.5 + 0.5 * np.sin(x * 2.1) * np.sin(y * 2.1)
    col = hexf(p['col'])[None, None] * (0.88 + 0.16 * wv[..., None]) * (0.9 + 0.2 * fbm(S, S, 6, 3, 2, tile=True))[..., None]; save(col, out)
reg('canvas_khaki', dict(col='#cdb86a'), paint_canvas); reg('canvas_olive', dict(col='#8a9a44'), paint_canvas)

def paint_camonet(p, out):
    S = 512; rs = np.random.RandomState(7); cols = [hexf('#4a8a2a'), hexf('#86a23a'), hexf('#a89440'), hexf('#386a24')]
    n = fbm(S, S, 5, 3, 11); m = np.digitize(n, [0.36, 0.5, 0.64]); img = np.zeros((S, S, 3), 'float32')
    for k in range(4): img[m == k] = cols[k]
    # net holes: a coarse mesh with random torn holes
    y, x = np.mgrid[0:S, 0:S].astype('float32'); mesh = ((np.sin(x * 0.55) * np.sin(y * 0.55)) > -0.2).astype('float32')
    holes = (fbm(S, S, 12, 3, 13) > 0.58).astype('float32'); a = np.clip(0.10 + 0.62 * mesh * (1 - holes * 0.9), 0, 1)
    gar = (fbm(S, S, 40, 2, 14) > 0.7).astype('float32'); img = img * (1 - gar[..., None] * 0.6) + gar[..., None] * 0.6 * hexf('#4c7a2a'); a = np.maximum(a, gar * 0.8)
    save(img, out, alpha=a)
reg('camonet', {}, paint_camonet)

def paint_rubber(p, out):
    S = 512; y, x = np.mgrid[0:S, 0:S].astype('float32'); wv = 0.5 + 0.5 * np.sin(x * 0.9) * np.sin(y * 0.9)
    base = hexf(p['col'])[None, None] * (0.9 + 0.1 * wv[..., None]) * (0.86 + 0.28 * fbm(S, S, 7, 4, 3, tile=True))[..., None]
    mott = (fbm(S, S, 20, 3, 9, tile=True) > 0.6).astype('float32') * 0.1; base = base * (1 + mott[..., None] * np.array([0.4, 0.5, -0.4], 'float32'))
    save(base, out)
reg('rubber', dict(col='#607626'), paint_rubber); reg('rubber_d', dict(col='#3f4c22'), paint_rubber); reg('rubber_l', dict(col='#6f8236'), paint_rubber)

def paint_star(p, out):
    S = 512; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = S / 2; R = S * 0.47; r = R * 0.382
    pts = []
    for k in range(10):
        a = -math.pi / 2 + math.pi * k / 5; rr = R if k % 2 == 0 else r; pts.append((c + rr * math.cos(a), c + rr * math.sin(a)))
    d.polygon(pts, fill=(246, 244, 232, 255)); save(np.asarray(im).astype('float32')[..., :3] / 255, out, alpha=np.asarray(im).astype('float32')[..., 3] / 255)
reg('star', {}, paint_star)

def paint_water(p, out):
    S = 512; n = fbm(S, S, 8, 4, 3, tile=True); y, x = np.mgrid[0:S, 0:S].astype('float32')
    col = hexf('#2f8ed4')[None, None] * (0.8 + 0.4 * n[..., None]); g = (fbm(S, S, 60, 2, 5, tile=True) > 0.7).astype('float32'); col = col * (1 - 0.6 * g[..., None]) + 0.6 * g[..., None] * hexf('#d8f2ff')
    save(col, out)
reg('water', {}, paint_water)

def paint_cow(p, out):
    S = 512; n = fbm(S, S, 3, 3, 8, tile=True); m = (n > 0.5).astype('float32'); m = np.asarray(Image.fromarray((m * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.5))).astype('float32') / 255
    col = hexf('#f6efe2')[None, None] * (1 - m[..., None]) + m[..., None] * hexf(p['spot']); save(col, out)
reg('cow', dict(spot='#8a4a26'), paint_cow); reg('cow_b', dict(spot='#20202a'), paint_cow)

def paint_smokecard(p, out):
    S = 256; y, x = np.mgrid[0:S, 0:S].astype('float32'); r = np.hypot(x - S / 2, y - S / 2) / (S / 2); a = np.clip((1 - r) * 4, 0, 1)
    save(np.ones((S, S, 3), 'float32') * 0.95, out, alpha=a)
reg('puff', {}, paint_smokecard)

# ----------------------------------------------------------------------------- text textures
def _font(path, size): return ImageFont.truetype(path, size)

def _stencil(d, xy, text, font, fill, anchor='mm', gap=3):
    d.text(xy, text, font=font, fill=fill, anchor=anchor)

def paint_crate(p, out):
    """Crate face: planks + a stencil: lines of text centred; W x H px."""
    W, H = p['size']; base = Image.new('RGB', (W, H), hex8('#6a4224')); d = ImageDraw.Draw(base); rs = random.Random(p['seed']); n = 5; ph = H / n
    for i in range(n):
        c = rs.choice(['#c8935a', '#bd8650', '#d29c62', '#b47c48']); d.rectangle([0, i * ph + 3, W, (i + 1) * ph - 3], fill=hex8(c))
        for _ in range(6):
            x = rs.randint(0, W); d.line([x, i * ph + 8, x + rs.randint(30, 160), i * ph + 8 + rs.randint(-3, 3)], fill=hex8('#9a6a3a'), width=2)
    for x in (0, W - 78):                                              # battens
        d.rectangle([x, 0, x + 78, H], fill=hex8('#a8723e')); d.rectangle([x, 0, x + 6, H], fill=hex8('#7a4c26')); d.rectangle([x + 72, 0, x + 78, H], fill=hex8('#7a4c26'))
        for yy in (28, H - 28): d.ellipse([x + 33, yy - 7, x + 45, yy + 5], fill=hex8('#4a3a2a'))
    d.rectangle([0, 0, W - 1, H - 1], outline=hex8('#5a381c'), width=8)
    lines = p['lines']; sizes = p['sizes']; tot = sum(sizes) * 1.15; y = H / 2 - tot / 2 + sizes[0] * 0.57
    for ln, sz in zip(lines, sizes):
        f = _font(FONT_N, sz); d.text((W / 2, y), ln, font=f, fill=hex8('#1c140c'), anchor='mm'); y += sz * 1.15
    arr = np.asarray(base).astype('float32') / 255
    # stencil bridges: thin wood-coloured bars cut across the letters
    im2 = Image.fromarray((arr * 255).astype('uint8')); d2 = ImageDraw.Draw(im2); y = H / 2 - tot / 2
    for ln, sz in zip(lines, sizes):
        for k in range(1, 3): d2.line([W * 0.08, y + sz * (0.30 + 0.28 * k), W * 0.92, y + sz * (0.30 + 0.28 * k)], fill=hex8('#c08a54'), width=3)
        y += sz * 1.15
    arr = np.asarray(im2).astype('float32') / 255; arr *= (0.92 + 0.14 * fbm(H, W, 10, 3, 2))[..., None]; save(arr, out)
reg('crate_a', dict(size=(1024, 640), seed=2, lines=['23rd HQ', 'SPECIAL TROOPS'], sizes=[170, 112]), paint_crate)
reg('crate_b', dict(size=(1024, 640), seed=3, lines=['DECOY M4', 'HANDLE WITH CARE'], sizes=[170, 96]), paint_crate)
reg('crate_c', dict(size=(1024, 640), seed=4, lines=['U.S. ARMY', 'RUBBER · INFLATABLE'], sizes=[150, 96]), paint_crate)
reg('crate_plain', dict(size=(512, 640), seed=5, lines=['23', ''], sizes=[200, 10]), paint_crate)

def paint_sign(p, out):
    """Canvas sign: khaki canvas, white stencil, rope eyelets."""
    W, H = 1536, 640; im = Image.new('RGB', (W, H), hex8('#5e6a30')); d = ImageDraw.Draw(im)
    d.rectangle([10, 10, W - 11, H - 11], fill=hex8('#cfbb70')); d.rectangle([34, 34, W - 35, H - 35], outline=hex8('#4a4a22'), width=8)
    f1 = _font(FONT_N, 215); f2 = _font(FONT_N, 138); d.text((W / 2, H * 0.34), '23rd HQ', font=f1, fill=hex8('#26301a'), anchor='mm'); d.text((W / 2, H * 0.72), 'SPECIAL TROOPS', font=f2, fill=hex8('#26301a'), anchor='mm')
    for x in (60, W - 60):
        for y in (60, H - 60): d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=hex8('#7a6a30'), outline=hex8('#3a3a1a'), width=3)
    arr = np.asarray(im).astype('float32') / 255; arr *= (0.94 + 0.1 * fbm(H, W, 12, 3, 4))[..., None]
    y_, x_ = np.mgrid[0:H, 0:W].astype('float32'); arr *= (0.96 + 0.04 * np.sin(x_ * 1.7) * np.sin(y_ * 1.7))[..., None]; save(arr, out)
reg('sign', {}, paint_sign)

def paint_tankmark(p, out):
    """Hull-rear / bumper stencil 'C-23' decal on olive (RGBA)."""
    W, H = 512, 160; im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.text((W / 2, H / 2), '23 · 4', font=_font(FONT_N, 118), fill=(246, 244, 232, 255), anchor='mm')
    a = np.asarray(im).astype('float32') / 255; save(a[..., :3], out, alpha=a[..., 3])
reg('tankmark', {}, paint_tankmark)

# ============================================================================= soldier placeholder cards (flat 2D puppet look: round head, olive jacket, helmet)
def paint_soldier(p, out):
    """RGBA card, 3 D tall: ppd px per D. pose: dict(arm_l, arm_r (deg from straight down, +forward), legs, helmet, prop). tone multiplies colours (night), rim = (hex, side) warm rim line."""
    ppd = 200; Wd, Hd = 2.6, 3.2; W, Hh = int(Wd * ppd), int(Hd * ppd); SS = 3
    im = Image.new('RGBA', (W * SS, Hh * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im); k = ppd * SS
    tone = p.get('tone', (1, 1, 1)); ink = (22, 20, 26, 255)
    def C(h): r, g, b = hex8(h); return (min(255, int(r * tone[0])), min(255, int(g * tone[1])), min(255, int(b * tone[2])), 255)
    def X(x): return (Wd / 2 + x) * k
    def Y(y): return (Hd - y) * k                                   # y up from the feet
    def line(a, b, w, col): d.line([X(a[0]), Y(a[1]), X(b[0]), Y(b[1])], fill=col, width=int(w * k))
    def seg(a, b, w, col):
        line(a, b, w + 0.07, ink); line(a, b, w, col)
        for q in (a, b): d.ellipse([X(q[0]) - w * k / 2, Y(q[1]) - w * k / 2, X(q[0]) + w * k / 2, Y(q[1]) + w * k / 2], fill=col)
    pose = p['pose']; olive = C('#6a7a34'); olive_d = C('#4e5c26'); khaki = C('#b9a35a'); skin = C('#f6efe2'); boot = C('#2a2216')
    sit = pose.get('sit', False); lk = pose.get('lean', 0.0)
    hipy = 0.88 if not sit else 0.68
    # legs
    if sit:
        seg((0.1, hipy), (0.75, 0.85), 0.2, khaki); seg((0.75, 0.85), (0.8, 0.12), 0.2, khaki); seg((-0.1, hipy), (0.45, 0.8), 0.2, khaki); seg((0.45, 0.8), (0.5, 0.1), 0.2, khaki)
    else:
        sp = pose.get('stride', 0.0)
        seg((0.12, hipy), (0.16 + sp, 0.1), 0.21, khaki); seg((-0.12, hipy), (-0.16 - sp, 0.1), 0.21, khaki)
        for fx in (0.16 + sp, -0.16 - sp): d.rounded_rectangle([X(fx - 0.15), Y(0.16), X(fx + 0.3), Y(0.0)], radius=int(0.06 * k), fill=boot, outline=ink, width=int(0.04 * k))
    # torso (rounded jacket)
    tx = lk * 0.2; tb, tt = hipy - 0.05, hipy + 0.9
    d.rounded_rectangle([X(-0.52 + tx), Y(tt), X(0.52 + tx), Y(tb)], radius=int(0.25 * k), fill=olive, outline=ink, width=int(0.045 * k))
    d.rectangle([X(-0.5 + tx), Y(tb + 0.3), X(0.5 + tx), Y(tb + 0.18)], fill=khaki); d.rectangle([X(-0.08 + tx), Y(tb + 0.32), X(0.08 + tx), Y(tb + 0.15)], fill=C('#d8b848'))
    d.line([X(tx), Y(tt - 0.1), X(tx), Y(tb + 0.32)], fill=olive_d, width=int(0.03 * k))
    # arms
    def arm(sh, ang, ln=0.95, up=False):
        a = math.radians(ang); el = (sh[0] + 0.5 * ln * math.sin(a), sh[1] - 0.5 * ln * math.cos(a)); ha = a + math.radians(pose.get('bend', 25)) * (1 if ang >= 0 else -1)
        hand = (el[0] + 0.5 * ln * math.sin(ha), el[1] - 0.5 * ln * math.cos(ha)); seg(sh, el, 0.19, olive); seg(el, hand, 0.17, olive_d)
        d.ellipse([X(hand[0]) - 0.1 * k, Y(hand[1]) - 0.1 * k, X(hand[0]) + 0.1 * k, Y(hand[1]) + 0.1 * k], fill=skin, outline=ink, width=int(0.03 * k)); return hand
    shy = tt - 0.18
    hl = arm((-0.5 + tx, shy), pose.get('arm_l', 8)); hr = arm((0.5 + tx, shy), pose.get('arm_r', -8))
    prop = pose.get('prop')
    if prop == 'clip':
        d.rectangle([X(hr[0] - 0.05), Y(hr[1] + 0.32), X(hr[0] + 0.4), Y(hr[1] - 0.05)], fill=C('#d8c8a0'), outline=ink, width=int(0.03 * k))
    elif prop == 'hose':
        line(hl, (hl[0] - 0.9, hl[1] - 0.5), 0.1, ink)
    elif prop == 'phones':
        pass
    # head
    hx, hy, hr_ = tx * 1.4, tt + 0.5, 0.56
    d.ellipse([X(hx - hr_), Y(hy + hr_), X(hx + hr_), Y(hy - hr_)], fill=skin, outline=ink, width=int(0.05 * k))
    ex = 0.2 + pose.get('look', 0.0)
    for sx in (-1, 1):
        d.ellipse([X(hx + sx * 0.22 + ex * 0.3 - 0.06), Y(hy + 0.04 + 0.1), X(hx + sx * 0.22 + ex * 0.3 + 0.06), Y(hy + 0.04 - 0.1)], fill=ink)
    mouth = pose.get('mouth', 'flat')
    if mouth == 'smile': d.arc([X(hx - 0.2), Y(hy - 0.15), X(hx + 0.2), Y(hy - 0.35)], 10, 170, fill=ink, width=int(0.04 * k))
    elif mouth == 'o': d.ellipse([X(hx - 0.07), Y(hy - 0.2), X(hx + 0.07), Y(hy - 0.36)], fill=ink)
    else: d.line([X(hx - 0.14), Y(hy - 0.26), X(hx + 0.14), Y(hy - 0.26)], fill=ink, width=int(0.04 * k))
    # helmet (M1 steel pot): dome + rim + band
    d.pieslice([X(hx - 0.68), Y(hy + 0.78), X(hx + 0.68), Y(hy - 0.58)], 180, 360, fill=olive, outline=ink, width=int(0.05 * k))
    d.rounded_rectangle([X(hx - 0.8), Y(hy + 0.17), X(hx + 0.8), Y(hy + 0.05)], radius=int(0.06 * k), fill=olive_d, outline=ink, width=int(0.04 * k))
    d.line([X(hx - 0.56), Y(hy + 0.3), X(hx + 0.56), Y(hy + 0.3)], fill=C('#8fa04a'), width=int(0.05 * k))
    if prop == 'phones': d.arc([X(hx - 0.75), Y(hy + 0.9), X(hx + 0.75), Y(hy - 0.7)], 200, 340, fill=ink, width=int(0.07 * k)); [d.ellipse([X(hx + s * 0.7 - 0.14), Y(hy + 0.18), X(hx + s * 0.7 + 0.14), Y(hy - 0.18)], fill=C('#3a3a40'), outline=ink, width=int(0.03 * k)) for s in (-1, 1)]
    im = im.resize((W, Hh), Image.LANCZOS); a = np.asarray(im).astype('float32') / 255
    rim = p.get('rim')
    if rim:
        col, side, wpx, kk = hexf(rim[0]), rim[1], int(rim[2]), rim[3] if len(rim) > 3 else 0.9; al = a[..., 3] > 0.5; sh = np.roll(al, -side * wpx, axis=1); edge = al & ~sh
        for e in range(2): edge = edge | (al & ~np.roll(al, -side * (wpx - 1 - e), axis=1))
        edge &= al; a[..., :3] = np.where(edge[..., None], a[..., :3] * (1 - kk) + col * kk, a[..., :3])
    save(a[..., :3], out, alpha=a[..., 3])
POSES = dict(stand=dict(), pump=dict(arm_l=40, arm_r=30, bend=30, lean=0.8, prop=None), lift=dict(arm_l=150, arm_r=160, bend=-10, mouth='o'), carry=dict(arm_l=35, arm_r=35, bend=-20),
             clip=dict(arm_l=10, arm_r=60, bend=35, prop='clip', mouth='smile'), walk=dict(stride=0.35, arm_l=-25, arm_r=25, bend=10), point=dict(arm_l=8, arm_r=100, bend=5, mouth='smile'),
             radio=dict(sit=True, arm_l=50, arm_r=70, bend=30, prop='phones'), wave=dict(arm_l=8, arm_r=155, bend=-15, mouth='smile'), guard=dict(arm_l=20, arm_r=20, bend=15), push=dict(arm_l=75, arm_r=80, bend=-10, lean=1.0, mouth='o'),
             hold=dict(arm_l=95, arm_r=110, bend=-25, lean=0.6, mouth='o', look=0.25))
for _pn, _pose in POSES.items():
    for _tn, _tone in (('d', (1.0, 1.0, 1.0)), ('n', (0.62, 0.72, 1.1))):
        reg('sol_%s_%s' % (_pn, _tn), dict(pose=_pose, tone=_tone, rim=('#ffc060', -1, 7, 0.9) if _tn == 'd' else ('#ffb050', -1, 6, 0.85), tv=3), paint_soldier)

# ============================================================================= driver
def _key(name):
    params, fn = JOBS[name]; return hashlib.sha1((json.dumps(params, sort_keys=True, default=str) + TEX_V + name).encode()).hexdigest()[:10]

def ensure(names=None, verbose=True):
    os.makedirs(TEX, exist_ok=True); tx = {}
    for name in (names or list(JOBS)):
        params, fn = JOBS[name]; path = os.path.join(TEX, '%s_%s.png' % (name, _key(name)))
        if not os.path.exists(path):
            import time; t0 = time.time(); fn(params, path)
            if verbose: print('tex', name, '%.1fs' % (time.time() - t0), flush=True)
        tx[name] = path
        g = path.replace('.png', '_glint.png')
        if os.path.exists(g): tx[name + '_glint'] = g
    return tx

if __name__ == '__main__':
    ensure(sys.argv[1:] or None)

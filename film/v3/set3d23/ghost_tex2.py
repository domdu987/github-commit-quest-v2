#!/usr/bin/env python3
"""ghost_tex2.py : set r1 texture jobs added to ghost_tex.JOBS (same cache tex_ghost/, same hashing): the far patchwork ring of FIELDS,
the RHINE ground, the pre-dawn sky, the RHINE / division stencils, the chalk crate, sandbags, the record label, the night river and the flat
placeholder silhouettes (cards that only show the staging; the real cast is cast23).   import ghost_tex2 registers everything."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import ghost_tex as GX
from ghost_tex import reg, hexf, hex8, fbm, save, _font, FONT_N, FONT_B, spline, paint_crate, paint_ground

# ----------------------------------------------------------------------------- layouts: the far ring of FIELDS, the RHINE plain
RIVER_FAR = spline([(-1900, 330), (-1400, 300), (-900, 360), (-600, 250), (-270, 244), (-210, 262), (-150, 290), (-90, 286), (-40, 266), (10, 258), (60, 272),
                    (120, 300), (190, 298), (270, 282), (600, 320), (1000, 240), (1400, 300), (1900, 260)], 6)
LANE_FAR = spline([(-60, -1500), (-50, -700), (-42, -130), (-30, -70), (-18, -20), (-6, 30), (8, 72), (16, 112), (10, 152), (-6, 192), (-14, 232), (-6, 262),
                   (12, 296), (34, 330), (44, 372), (80, 700), (60, 1200), (120, 2300)], 6)
GX.SCENES['far'] = dict(rect=(-1900, 1900, -1500, 2300), res=4096, xs=[-1900 + 3800 * i / 52 for i in range(53)], ys=[-1500 + 3800 * j / 52 for j in range(53)],
                        jit=0.26, seed=17, lane=LANE_FAR, lane_w=9.0, river=RIVER_FAR, river_w=16.0, pal='day', hedge_p=0.8, warp=9.0)
# RHINE (local frame): the river runs north (+y) at x = 0, about 76 D wide; the US (west) bank x < -38, the German (east) bank x > 38.
RIVER_R = [(-2.0 + 6.0 * math.sin(y * 0.004), float(y)) for y in range(-700, 1301, 20)]
TRACK_R = spline([(-70, -700), (-66, -300), (-60, -100), (-62, 100), (-58, 300), (-60, 600), (-56, 1300)], 8)
GX.SCENES['rhine'] = dict(rect=(-420, 420, -700, 1300), res=4096, xs=[-420, -330, -240, -150, -60, 60, 150, 240, 330, 420], ys=[-700 + 2000 * j / 16 for j in range(17)],
                          jit=0.10, seed=29, lane=TRACK_R, lane_w=6.0, river=RIVER_R, river_w=76.0, pal='rhine', hedge_p=0.35, warp=3.0)

_old_layout = GX.layout
def _layout(sc):
    L = _old_layout(sc)
    if sc == 'rhine' and not L.get('_r'):                           # March fields: brown plough and dull winter green, no hedges in the river
        rng = random.Random(3)
        for c in L['cells']:
            c['col'] = rng.choice(['#4e7a2a', '#5a8430', '#46702a', '#6a7c34', '#5e7230'])
            if rng.random() < 0.35: c['kind'] = 'plough'
        L['_r'] = True
    return L
GX.layout = _layout
reg('fields_far', dict(scene='far', pal='day', v=2), paint_ground)
reg('fields_rhine', dict(scene='rhine', pal='rhine', v=3), paint_ground)

# ----------------------------------------------------------------------------- pre-dawn sky (S18): deep blue, cold pale band low in the east
def paint_sky_predawn(p, out):
    W = GX.SKY_W; H = int(round(W * 105 / 360)); el = 90.0 - (np.arange(H, dtype='float32') + 0.5) / H * 105.0; az = (np.arange(W, dtype='float32') + 0.5) / W * 2 * math.pi
    stops = [(-15, '#1a2c70'), (0, '#3a64b8'), (4, '#3a5cb0'), (12, '#22409a'), (35, '#142c78'), (90, '#0c1a52')]
    o = np.zeros((H, 3), 'float32'); e = np.clip(el, -15, 90)
    for ch in range(3): o[:, ch] = np.interp(e, [s[0] for s in stops], [hexf(s[1])[ch] for s in stops])
    img = np.repeat(o[:, None, :], W, 1)
    E = np.radians(el)[:, None]; A = az[None, :]; east = np.clip(np.cos(A), 0, 1) ** 2 * np.exp(-np.clip(el, -3, 90)[:, None] / 7.0)
    img = img * (1 - 0.8 * east[..., None]) + 0.8 * east[..., None] * hexf('#8ab4e8')
    rs2 = np.random.RandomState(41); stars = np.zeros((H, W), 'float32')
    for _ in range(700):
        y_ = int(rs2.beta(1.2, 1.0) * (H * 0.7)); x_ = rs2.randint(0, W); stars[y_, x_] = max(stars[y_, x_], rs2.uniform(0.3, 0.9))
    stars *= np.clip((el[:, None] - 12.0) / 10.0, 0, 1) * (1 - 0.8 * np.clip(np.cos(A), 0, 1))
    img = img * (1 - stars[..., None]) + stars[..., None] * hexf('#f0f4ff')
    save(np.clip(img, 0, 1), out)
reg('sky_predawn', dict(v=1), paint_sky_predawn)

# ----------------------------------------------------------------------------- stencils
reg('crate_30', dict(size=(1024, 640), seed=7, lines=['30th INF DIV', 'U.S. ARMY'], sizes=[150, 104]), paint_crate)
reg('crate_79', dict(size=(1024, 640), seed=8, lines=['79th INF DIV', 'U.S. ARMY'], sizes=[150, 104]), paint_crate)

def paint_chalk(p, out):
    """Crate face with 'BALLOON ARMY' scrawled in white chalk (wobbly, tilted, an underline) over a plain stencil 'DECOY M4'."""
    W, H = 1024, 640; base = np.asarray(Image.open(p['base'])).astype('float32')[..., :3] / 255 if p.get('base') else None
    paint_crate(dict(size=(W, H), seed=11, lines=['DECOY M4', ''], sizes=[120, 10]), out)
    im = Image.open(out).convert('RGB'); txt = Image.new('L', (W, H), 0); d = ImageDraw.Draw(txt); f = _font(FONT_B, 150)
    d.text((W / 2, H * 0.62), 'BALLOON', font=f, fill=255, anchor='mm'); d.text((W / 2 + 20, H * 0.86), 'ARMY', font=_font(FONT_B, 130), fill=255, anchor='mm')
    txt = txt.rotate(-5, resample=Image.BICUBIC, center=(W / 2, H / 2)); d2 = ImageDraw.Draw(txt); d2.line([W * 0.22, H * 0.97, W * 0.82, H * 0.93], fill=255, width=12)
    a = np.asarray(txt.filter(ImageFilter.GaussianBlur(1.2))).astype('float32') / 255 * (0.55 + 0.45 * (fbm(H, W, 200, 2, 3) > 0.35))
    arr = np.asarray(im).astype('float32') / 255; arr = arr * (1 - a[..., None]) + a[..., None] * hexf('#f4f2ea'); save(arr, out)
reg('crate_chalk', dict(v=2), paint_chalk)

def paint_rhine_sign(p, out):
    """Riverbank sign board: white board, black 'RHINE' (Latin capitals), red border, two bolts."""
    W, H = 1280, 480; im = Image.new('RGB', (W, H), hex8('#b8261c')); d = ImageDraw.Draw(im)
    d.rectangle([22, 22, W - 23, H - 23], fill=hex8('#f2eee2')); f = _font(FONT_B, 300); d.text((W / 2, H * 0.53), 'RHINE', font=f, fill=hex8('#18161c'), anchor='mm')
    for x in (70, W - 70): d.ellipse([x - 14, H / 2 - 14, x + 14, H / 2 + 14], fill=hex8('#6a6a70'))
    arr = np.asarray(im).astype('float32') / 255; arr *= (0.93 + 0.1 * fbm(H, W, 14, 3, 6))[..., None]; save(arr, out)
reg('sign_rhine', dict(v=1), paint_rhine_sign)

def paint_sandbag(p, out):
    S = 512; n = fbm(S, S, 10, 4, 12, tile=True); y, x = np.mgrid[0:S, 0:S].astype('float32')
    weave = 0.94 + 0.06 * np.sin(x * 1.3) * np.sin(y * 1.3); col = hexf(p['col'])[None, None] * (0.8 + 0.35 * n[..., None]) * weave[..., None]; save(col, out)
reg('sandbag', dict(col='#a89a6c'), paint_sandbag)

def paint_record(p, out):
    """Gramophone record (top view): black grooves, red centre label (spinning reads through the label's white mark)."""
    S = 512; y, x = np.mgrid[0:S, 0:S].astype('float32'); r = np.hypot(x - S / 2, y - S / 2) / (S / 2)
    col = np.ones((S, S, 3), 'float32') * hexf('#18161a'); col *= (0.85 + 0.15 * np.sin(r * 160))[..., None]
    lab = r < 0.34; col[lab] = hexf('#c8281e'); mark = lab & (np.abs(x - S / 2) < 14) & (y < S / 2) & (r > 0.08); col[mark] = hexf('#f6f0e0')
    col[r < 0.04] = hexf('#d0d0d0'); save(col, out)
reg('record', dict(v=1), paint_record)

def paint_water_night(p, out):
    """Tileable night river (u across, v along the flow; 1 tile = 24 D): dark blue-teal base, long current streaks, moon / lamp glint dashes."""
    W = H = 1024; rs = random.Random(9)
    n1 = fbm(H, W, 3, 4, 51, tile=True); n2 = fbm(H, W, 24, 3, 52, tile=True)
    col = hexf('#163a6e')[None, None] * (0.75 + 0.4 * n1[..., None]) * (0.92 + 0.16 * n2[..., None])
    im = Image.fromarray((np.clip(col, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(im)
    for _ in range(260):                                                     # current streaks (lighter teal), elongated along v
        x, y, l = rs.uniform(0, W), rs.uniform(0, H), rs.uniform(60, 220)
        for ox in (-W, 0, W):
            for oy in (-H, 0, H): d.line([x + ox, y + oy, x + ox + rs.uniform(-6, 6), y + oy + l], fill=hex8(rs.choice(['#2a5a94', '#24508a', '#3a6aa4'])), width=rs.choice([2, 3, 4]))
    save(np.asarray(im.filter(ImageFilter.GaussianBlur(1.0))).astype('float32') / 255, out)
reg('water_night', dict(v=2), paint_water_night)

def paint_glints(p, out):
    """RGBA glint dashes for the river (additive): short bright horizontal slivers in clusters, alpha soft."""
    W, H = 1024, 1024; im = Image.new('L', (W, H), 0); d = ImageDraw.Draw(im); rs = random.Random(13)
    for _ in range(700):
        x, y, l = rs.uniform(0, W), rs.uniform(0, H), rs.uniform(8, 46); w = rs.choice([2, 2, 3, 4])
        d.line([x, y, x + l, y + rs.uniform(-1, 1)], fill=int(rs.uniform(120, 255)), width=w)
    a = np.asarray(im.filter(ImageFilter.GaussianBlur(0.9))).astype('float32') / 255
    save(np.ones((H, W, 3), 'float32'), out, alpha=a)
reg('glints', dict(v=1), paint_glints)

# ----------------------------------------------------------------------------- placeholder silhouettes (flat, one colour per role)
# Not the cast: flat shapes with a lighter head disc, so the contact sheet shows who stands where and where the heads are.
PH_ROLES = dict(
    soldier=dict(body='#55662a', head='#e8e0c8', hat='helmet', hatc='#3e4c1c'),
    painter=dict(body='#55662a', head='#e8e0c8', hat='helmet', hatc='#3e4c1c', prop='brush'),
    soundman=dict(body='#55662a', head='#e8e0c8', hat='phones', hatc='#3e4c1c', prop='record'),
    radioman=dict(body='#55662a', head='#e8e0c8', hat='phones', hatc='#3e4c1c', prop='handset'),
    pumpman=dict(body='#55662a', head='#e8e0c8', hat='helmet', hatc='#3e4c1c', prop='pump'),
    clipboard=dict(body='#55662a', head='#e8e0c8', hat='helmet', hatc='#3e4c1c', prop='clip'),
    major=dict(body='#b49a58', head='#f0b8a0', hat='peaked', hatc='#6a5a30', prop='cigar', wide=1.25),
    driver=dict(body='#7a8440', head='#e8e0c8', hat='cap', hatc='#4a5424'),
    cyclist_a=dict(body='#2a4a9a', head='#ecd8c0', hat='beret', hatc='#1c1c28', bike=True, stripes=True),
    cyclist_b=dict(body='#8a5a2a', head='#ecd8c0', hat='beret', hatc='#5a1c1c', bike=True),
    german=dict(body='#6e7478', head='#e8dcc8', hat='fieldcap', hatc='#50565a', prop='binoculars'),
    dog=dict(body='#8a6a40', head='#8a6a40', hat=None, hatc=None, dog=True),
)
POSES_PH = dict(stand=dict(), wave=dict(arm_r=150), point=dict(arm_r=95), lift=dict(arm_l=170, arm_r=170), sit=dict(sit=True), pump=dict(arm_l=60, arm_r=60, lean=0.3),
                carry=dict(arm_l=60, arm_r=60), paddle=dict(arm_l=40, arm_r=120, sit=True), look=dict(arm_l=120, arm_r=120), salute=dict(arm_r=140, bend=1),
                ride=dict(), brake=dict(arm_r=100), polish=dict(arm_r=110, arm_l=40), blow=dict(sit=True, arm_l=80, arm_r=80))

def paint_ph(p, out):
    """Flat silhouette card PH_CANVAS D (feet at the bottom centre, 3.0 D tall figure), 160 px per D; role colours, simple hats; cyclists ride a bike
    (wheels touch the bottom row); `tone` scales the colours (night)."""
    R = PH_ROLES[p['role']]; po = POSES_PH[p['pose']]; ppd = 160; Wd, Hd = PH_CANVAS['bike' if R.get('bike') else ('dog' if R.get('dog') else 'man')]; W, H = int(Wd * ppd), int(Hd * ppd); SS = 2
    im = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im); k = ppd * SS; tone = p.get('tone', (1, 1, 1))
    def C(h, a=255): r, g, b = hex8(h); return (min(255, int(r * tone[0])), min(255, int(g * tone[1])), min(255, int(b * tone[2])), a)
    X = lambda x: (Wd / 2 + x) * k; Y = lambda y: (Hd - y) * k
    ink = C('#1a1822'); body = C(R['body']); head = C(R['head']); hatc = C(R['hatc']) if R['hatc'] else None; wide = R.get('wide', 1.0)
    def seg(a, b, w, col): d.line([X(a[0]), Y(a[1]), X(b[0]), Y(b[1])], fill=col, width=int(w * k)); [d.ellipse([X(q[0]) - w * k / 2, Y(q[1]) - w * k / 2, X(q[0]) + w * k / 2, Y(q[1]) + w * k / 2], fill=col) for q in (a, b)]
    if R.get('dog'):
        d.ellipse([X(-0.7), Y(1.1), X(0.5), Y(0.45)], fill=body); d.ellipse([X(0.3), Y(1.45), X(0.95), Y(0.85)], fill=body)
        for x in (-0.55, -0.35, 0.2, 0.38): seg((x, 0.6), (x, 0.0), 0.13, body)
        seg((-0.65, 0.95), (-0.95, 1.3), 0.1, body); d.ellipse([X(0.62), Y(1.62), X(0.82), Y(1.3)], fill=body)
    else:
        bike = R.get('bike'); sit = po.get('sit', False) or bike
        hip = (0.0, 1.3 if bike else (0.75 if sit else 0.95))
        if bike:
            for cx in (-1.1, 1.1):
                d.ellipse([X(cx - 0.62), Y(1.24), X(cx + 0.62), Y(0.0)], outline=C('#22222a'), width=int(0.1 * k))
            for a, b in (((-1.1, 0.62), (0.0, 0.5)), ((0.0, 0.5), (-0.2, 1.25)), ((-0.2, 1.25), (0.85, 1.3)), ((0.0, 0.5), (0.85, 1.3)), ((0.85, 1.3), (1.1, 0.62)), ((-1.1, 0.62), (-0.2, 1.25))):
                seg(a, b, 0.07, C('#3060b0'))
            seg((0.85, 1.3), (0.8, 1.7), 0.06, C('#606068')); seg((0.65, 1.75), (1.0, 1.75), 0.07, C('#606068'))
            seg(hip, (0.25, 0.75), 0.24, C('#2a2a30')); seg((0.25, 0.75), (0.05, 0.42), 0.2, C('#2a2a30'))
            d.rectangle([X(1.0), Y(1.55), X(1.4), Y(1.25)], fill=C('#c8a050')); seg((1.05, 1.5), (1.45, 1.95), 0.08, C('#e0b060'))
        elif sit:
            seg(hip, (0.55, hip[1]), 0.28 * wide, C('#3a3a2a') if p['role'] != 'major' else C('#8a7440')); seg((0.55, hip[1]), (0.6, 0.05), 0.24, C('#3a3a2a') if p['role'] != 'major' else C('#8a7440'))
        else:
            seg((0.15, hip[1]), (0.22, 0.05), 0.26, body); seg((-0.15, hip[1]), (-0.22, 0.05), 0.26, body)
            for fx in (0.22, -0.22): d.ellipse([X(fx - 0.2), Y(0.16), X(fx + 0.24), Y(0.0)], fill=C('#2a2018'))
        tw = 0.5 * wide; top = hip[1] + 0.95; lean = po.get('lean', 0.0)
        bx = 0.25 if bike else 0.0
        d.rounded_rectangle([X(-tw + lean + bx), Y(top), X(tw + lean + bx), Y(hip[1] - 0.05)], radius=int(0.22 * k), fill=body)
        if R.get('stripes'):
            for i in range(5): d.line([X(-tw + lean + bx + 0.05), Y(hip[1] + 0.12 + i * 0.17), X(tw + lean + bx - 0.05), Y(hip[1] + 0.12 + i * 0.17)], fill=C('#f0f0f0'), width=int(0.06 * k))
        sh = (lean + bx, top - 0.15)
        def arm(side, ang):
            a = math.radians(ang); bend = math.radians(30 * po.get('bend', 0.5)); s = (sh[0] + side * (tw - 0.05), sh[1]); L_ = 0.5
            e = (s[0] + side * L_ * math.sin(a) * 0.6 + L_ * math.sin(a) * 0.4, s[1] - L_ * math.cos(a)); h = (e[0] + side * 0.1 + L_ * math.sin(a + bend) * 0.5, e[1] - L_ * math.cos(a + bend))
            seg(s, e, 0.2, body); seg(e, h, 0.18, body); d.ellipse([X(h[0]) - 0.1 * k, Y(h[1]) - 0.1 * k, X(h[0]) + 0.1 * k, Y(h[1]) + 0.1 * k], fill=head); return h
        if bike: hl = arm(-1, 70); hr = arm(1, 70 if p['pose'] != 'brake' else 100)
        else: hl = arm(-1, po.get('arm_l', 12)); hr = arm(1, po.get('arm_r', 12))
        prop = R.get('prop')
        if prop == 'brush' or p['pose'] == 'polish': seg(hr, (hr[0] + 0.35, hr[1] + 0.35), 0.07, C('#c8a050'))
        if prop == 'clip': d.rectangle([X(hr[0] - 0.05), Y(hr[1] + 0.4), X(hr[0] + 0.35), Y(hr[1] - 0.05)], fill=C('#e8d8a8'))
        if prop == 'record': d.ellipse([X(hl[0] - 0.32), Y(hl[1] + 0.32), X(hl[0] + 0.32), Y(hl[1] - 0.32)], fill=C('#141418')); d.ellipse([X(hl[0] - 0.1), Y(hl[1] + 0.1), X(hl[0] + 0.1), Y(hl[1] - 0.1)], fill=C('#c8281e'))
        if prop == 'handset': seg(hr, (hr[0] - 0.1, hr[1] + 0.3), 0.12, C('#202024'))
        if prop == 'binoculars': d.rectangle([X(-0.22 + lean), Y(top + 0.78), X(0.22 + lean), Y(top + 0.56)], fill=C('#1c1c20'))
        hx, hy, hr_ = lean * 1.3 + bx, top + 0.52, 0.55
        d.ellipse([X(hx - hr_), Y(hy + hr_), X(hx + hr_), Y(hy - hr_)], fill=head, outline=ink, width=int(0.04 * k))
        if prop == 'cigar': seg((hx + 0.3, hy - 0.22), (hx + 0.72, hy - 0.16), 0.1, C('#6a3a1c')); d.ellipse([X(hx - 0.42), Y(hy - 0.06), X(hx + 0.42), Y(hy - 0.3)], fill=C('#4a3220'))
        if prop == 'binoculars': d.rectangle([X(hx - 0.34), Y(hy + 0.12), X(hx + 0.34), Y(hy - 0.12)], fill=C('#1c1c20'))
        hat = R['hat']
        if hat == 'helmet': d.pieslice([X(hx - 0.66), Y(hy + 0.74), X(hx + 0.66), Y(hy - 0.56)], 180, 360, fill=hatc); d.rectangle([X(hx - 0.76), Y(hy + 0.12), X(hx + 0.76), Y(hy + 0.02)], fill=hatc)
        elif hat == 'phones': d.pieslice([X(hx - 0.62), Y(hy + 0.7), X(hx + 0.62), Y(hy - 0.5)], 180, 360, fill=hatc); [d.ellipse([X(hx + s * 0.58 - 0.15), Y(hy + 0.15), X(hx + s * 0.58 + 0.15), Y(hy - 0.18)], fill=C('#202024')) for s in (-1, 1)]
        elif hat == 'peaked': d.rectangle([X(hx - 0.5), Y(hy + 0.78), X(hx + 0.5), Y(hy + 0.38)], fill=hatc); d.rectangle([X(hx - 0.6), Y(hy + 0.42), X(hx + 0.7), Y(hy + 0.3)], fill=C('#2a2418'))
        elif hat == 'cap': d.pieslice([X(hx - 0.55), Y(hy + 0.66), X(hx + 0.55), Y(hy - 0.3)], 180, 360, fill=hatc)
        elif hat == 'beret': d.ellipse([X(hx - 0.6), Y(hy + 0.72), X(hx + 0.5), Y(hy + 0.3)], fill=hatc)
        elif hat == 'fieldcap': d.rectangle([X(hx - 0.5), Y(hy + 0.72), X(hx + 0.5), Y(hy + 0.32)], fill=hatc); d.rectangle([X(hx - 0.5), Y(hy + 0.4), X(hx + 0.62), Y(hy + 0.3)], fill=C('#3a3e40'))
    im = im.resize((W, H), Image.LANCZOS); a = np.asarray(im).astype('float32') / 255; save(a[..., :3], out, alpha=a[..., 3])

PH_CANVAS = dict(man=(2.6, 3.6), bike=(4.2, 4.0), dog=(2.2, 1.8))     # card size in D (1 px row = feet at the bottom)
PH_TONE = dict(d=(1.0, 1.0, 1.0), n=(0.7, 0.76, 1.0))
for _r in PH_ROLES:
    for _p in POSES_PH:
        for _t, _tn in PH_TONE.items(): reg('ph_%s_%s_%s' % (_r, _p, _t), dict(role=_r, pose=_p, tone=_tn, v=4), paint_ph)

# ----------------------------------------------------------------------------- LANE r1: the lane runs on 90 D further south (jeep approach, the cyclists), the painted rect grows
GX.LANE2[:] = spline([(-8, -130), (-7.5, -80), (-6, -40), (-4, -10), (0, 14), (8, 46), (18, 84), (30, 126), (40, 170)], 12)
GX.SCENES['morning'].update(rect=(-90, 90, -130, 150), xs=[-90, -14, 16, 90], ys=[-130, -50, 40, 150])
reg('fields_morning', dict(scene='morning', pal='day', v=2), paint_ground)
reg('crate_d4', dict(size=(1024, 640), seed=11, lines=['DECOY M4', ''], sizes=[120, 10]), paint_crate)

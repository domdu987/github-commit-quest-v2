#!/usr/bin/env python3
"""room.py : Nico's tiny attic bedroom (Brescia, 1769) as a real 3D Blender set (bpy 5.3, Cycles CPU).

    import room as R
    A = R.build("DAWN")                          # collections SET and LIGHTS, world, render settings, grade -> anchors dict
    cam = R.make_camera(A["cams"]["push_rod"])
    png = R.book_page_texture()                  # the open book's two pages as one PNG (for a flat close insert)

World: 1 unit = 1 D, Z up, floor z = 0, back gable wall (with the window) = plane y = 0, the room runs toward -y
(front gable y = -6), x = 0 = ridge line, +x to the right for a viewer facing the window wall (the bed is on the right).
CLI: python3 room.py stills [preview|final] | timing | digest | book
See room_API.md."""
import os, sys, math, random
import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'small_work'))
import smallkit as K                                         # noqa: E402
make_camera = K.make_camera; setup_render = K.setup_render; placeholder_actor = K.placeholder_actor; no_bounce = K.no_bounce

# ----------------------------------------------------------------------------- dimensions (D)
XW = 2.8                        # knee walls at x = -XW and +XW
YB, YF = 0.0, -6.0              # back gable (window), front gable
ZK, ZR = 1.6, 5.2               # knee wall height, ridge height (x = 0)
SLOPE = (ZR - ZK) / XW
WALL_T = 0.3
WIN = dict(x0=-0.85, x1=0.45, z0=2.55, z1=4.0)             # the small window in the back gable
WIN_C = ((WIN['x0'] + WIN['x1']) / 2, WALL_T / 2, (WIN['z0'] + WIN['z1']) / 2)
BED = dict(x0=1.35, x1=2.62, y0=-3.5, y1=-0.9, top=0.78)    # straw bed along the right knee wall, head at the back
ROD_BASE, ROD_TOP = (1.10, -3.95, 0.0), (2.10, -4.02, 2.40)  # iron rod leaning at the foot of the bed against a rafter
STOOL = (0.55, -2.6, 1.0)                                   # stool centre and top height
CANDLE = (0.80, -2.42, 1.0)
HERO_MARK = (0.95, -1.55, 0.0)
BED_SIT = dict(feet=(1.08, -2.15, 0.0), seat_z=BED['top'])
LIGHT_TARGET = (1.07, -3.28, 1.15)                          # the sun beam is aimed here (between the book and the rod)
INK = '#2a1712'; INK_NIGHT = '#1d1449'

def roof_z(x): return ZK + (XW - abs(x)) * SLOPE

def _key_dir(elev_deg=None):
    v = Vector(LIGHT_TARGET) - Vector(WIN_C); return tuple(v.normalized())

def _elev(): v = Vector(_key_dir()); return math.degrees(math.asin(-v.z))

# ----------------------------------------------------------------------------- presets
PRESETS = {
    'DAWN': dict(key_type='SUN', key_dir=_key_dir(), key=(2.2, 1.85, 0.75), sun_angle=0.45, key_loc=(-2.0, 6.0, 8.0),
                 shade=(0.36, 0.44, 0.90), shade_desat=0.75, warm_mul=(2.4, 1.5, 0.5), warm_desat=0.0, floor_shade=1.32, lift=(0.008, 0.008, 0.014), form=(0.05, 0.0, 0.18),
                 amb_center=((0.9, -2.6, 1.0), 4.0, 0.74), amb_z=(2.4, 5.0, 0.92),
                 pools=[((1.2, -3.4, 0.8), (0.22, 0.11, 0.04), 1.8)], sky='r_sky_dawn', sky_strength=1.0, flame=0.0,
                 ink=INK, bloom_size=0.05, grade_offset=(0.002, 0.003, 0.006), grade_saturation=1.12),
    'NIGHT': dict(key_type='SUN', key_dir=_key_dir(), key=(0.62, 0.82, 1.6), key_desat=0.8, floor_shade=1.2, sun_angle=0.45, key_loc=(-2.0, 6.0, 8.0),
                  shade=(0.15, 0.21, 0.72), shade_desat=0.85, warm_mul=(1.0, 1.0, 1.0), warm_desat=0.75, lift=(0.004, 0.008, 0.022), form=(0.05, 0.0, 0.18),
                  amb_center=(CANDLE, 6.0, 0.6), amb_z=(3.0, 5.2, 0.35),
                  pools=[((CANDLE[0], CANDLE[1], CANDLE[2] + 0.3), (1.3, 0.95, 0.12), 0.75)], sky='r_sky_night', sky_strength=1.0, flame=5.0,
                  ink=INK_NIGHT, bloom_size=0.06, grade_offset=(0.002, 0.003, 0.012), grade_saturation=1.1),
}
STATE = {}

# ----------------------------------------------------------------------------- textures
def _rect(x, y, w, h, fill, extra=''): return f'<rect x="{x:.4f}" y="{y:.4f}" width="{w:.4f}" height="{h:.4f}" fill="{fill}" {extra}/>'

def _plaster(name, T=2.0, ppd=300):
    r = random.Random(21); base = '#d4a272'; o = [_rect(-0.1, -0.1, T + 0.2, T + 0.2, base)]
    for _ in range(26):
        x, y, rr = r.uniform(0, T), r.uniform(0, T), r.uniform(0.08, 0.3); c = r.choice([K.mulc(base, 1.08), K.mulc(base, 0.92), '#c89060'])
        for dx in (-T, 0, T):
            for dy in (-T, 0, T): o.append(f'<ellipse cx="{x + dx:.3f}" cy="{y + dy:.3f}" rx="{rr:.3f}" ry="{rr * 0.7:.3f}" fill="{c}" opacity="0.55"/>')
    # a patch of fallen plaster showing the brick
    bx, by = 0.3, 1.15; o.append(f'<path d="M{bx},{by} l0.5,-0.08 l0.18,0.3 l-0.1,0.32 l-0.46,0.06 l-0.16,-0.3 Z" fill="#9c4a34" stroke="#7a3a26" stroke-width="0.012"/>')
    for j in range(4):
        y = by + 0.02 + j * 0.13; o.append(f'<line x1="{bx - 0.1}" y1="{y:.3f}" x2="{bx + 0.66}" y2="{y:.3f}" stroke="#d8b08a" stroke-width="0.012" opacity="0.8"/>')
    o.append(f'<path d="M1.3,0.2 l0.06,0.2 l-0.05,0.18 l0.09,0.25" stroke="{K.mulc(base, 0.62)}" stroke-width="0.01" fill="none"/>')
    o.append(f'<path d="M1.6,1.4 l0.1,0.1 l-0.02,0.2" stroke="{K.mulc(base, 0.62)}" stroke-width="0.01" fill="none"/>')
    return name, (K.svg_doc(int(T * ppd), int(T * ppd), T, T, ''.join(o)), int(T * ppd), int(T * ppd), False)

def _planks(name, cols, W=1.8, L=3.0, pw=0.3, ppd=260, seam='#3a1c12'):
    r = random.Random(len(name)); o = []; n = int(round(W / pw))
    for i in range(n):
        x = i * pw; c = cols[i % len(cols)]; o.append(_rect(x, -0.1, pw, L + 0.2, c))
        cut = r.uniform(0.3, L - 0.3)
        o.append(f'<line x1="{x:.3f}" y1="{cut:.3f}" x2="{x + pw:.3f}" y2="{cut:.3f}" stroke="{seam}" stroke-width="0.012"/>')
        for k in range(3):
            gx = x + r.uniform(0.05, pw - 0.05); o.append(f'<path d="M{gx:.3f},0 Q{gx + 0.02:.3f},{L / 2:.3f} {gx:.3f},{L}" stroke="{K.mulc(c, 0.84)}" stroke-width="0.008" fill="none"/>')
        for yy in (cut - 0.05, cut + 0.05): o.append(f'<circle cx="{x + 0.06:.3f}" cy="{yy:.3f}" r="0.01" fill="{seam}"/><circle cx="{x + pw - 0.06:.3f}" cy="{yy:.3f}" r="0.01" fill="{seam}"/>')
        o.append(f'<line x1="{x:.3f}" y1="0" x2="{x:.3f}" y2="{L}" stroke="{seam}" stroke-width="0.014"/>')
    return name, (K.svg_doc(int(W * ppd), int(L * ppd), W, L, ''.join(o)), int(W * ppd), int(L * ppd), False)

def _beam(name, ppd=300):
    c = '#7a4426'; o = [_rect(0, 0, 1, 1, c)]; r = random.Random(9)
    for k in range(9):
        y = r.uniform(0.05, 0.95); o.append(f'<path d="M0,{y:.3f} Q0.5,{y + r.uniform(-0.04, 0.04):.3f} 1,{y:.3f}" stroke="{K.mulc(c, 0.78)}" stroke-width="0.01" fill="none"/>')
    o.append(f'<ellipse cx="0.6" cy="0.45" rx="0.05" ry="0.025" fill="none" stroke="{K.mulc(c, 0.6)}" stroke-width="0.01"/>')
    return name, (K.svg_doc(ppd, ppd, 1, 1, ''.join(o)), ppd, ppd, False)

def _straw(name, ppd=360):
    r = random.Random(4); o = [_rect(0, 0, 1, 1, '#d2a650')]
    for _ in range(260):
        x, y = r.uniform(-0.05, 1.05), r.uniform(-0.05, 1.05); a = r.uniform(-0.6, 0.6); L = r.uniform(0.04, 0.12)
        c = r.choice(['#e6c26a', '#b88a3e', '#c89a48', '#f0d482']); o.append(f'<line x1="{x:.3f}" y1="{y:.3f}" x2="{x + L * math.cos(a):.3f}" y2="{y + L * math.sin(a):.3f}" stroke="{c}" stroke-width="0.008"/>')
    o.append('<rect x="0" y="0" width="1" height="1" fill="none" stroke="#8a6a3a" stroke-width="0.02"/>')
    return name, (K.svg_doc(ppd, ppd, 1, 1, ''.join(o)), ppd, ppd, False)

def _blanket(name, ppd=400):
    """Patched wool blanket: rust red with ochre, slate blue, moss and linen patches, stitched with dashed thread."""
    o = [_rect(0, 0, 1.4, 2.0, '#a43a28')]
    for j in range(16): o.append(f'<line x1="0" y1="{j * 0.125:.3f}" x2="1.4" y2="{j * 0.125:.3f}" stroke="#8e3020" stroke-width="0.012"/>')
    patches = [(0.12, 0.2, 0.42, 0.36, '#c8883a'), (0.75, 0.55, 0.4, 0.34, '#4e6290'), (0.3, 1.05, 0.38, 0.42, '#7a8440'),
               (0.86, 1.32, 0.36, 0.3, '#d8bc8a'), (0.1, 1.6, 0.3, 0.25, '#4e6290'), (0.9, 0.08, 0.3, 0.26, '#7a8440')]
    for (x, y, w, h, c) in patches:
        o.append(_rect(x, y, w, h, c, 'transform="rotate(%d %f %f)"' % (random.Random(int(x * 100)).choice((-4, -2, 2, 3)), x + w / 2, y + h / 2)))
        o.append(f'<rect x="{x + 0.02:.3f}" y="{y + 0.02:.3f}" width="{w - 0.04:.3f}" height="{h - 0.04:.3f}" fill="none" stroke="#f0e2c0" stroke-width="0.008" stroke-dasharray="0.03 0.02" transform="rotate({random.Random(int(x * 100)).choice((-4, -2, 2, 3))} {x + w / 2} {y + h / 2})"/>')
    return name, (K.svg_doc(int(1.4 * ppd), int(2.0 * ppd), 1.4, 2.0, ''.join(o)), int(1.4 * ppd), int(2.0 * ppd), False)

def _book(name='r_book', ppd=1300):
    """Two facing pages, 1.2 x 0.84 units. Left: the hand-drawn diagram (storm cloud, lightning striking a pointed iron rod on a
    roof, the wire down the wall into the ground). Right: hand-written lines and two small sketches (the sharp point; a tower
    with no rod, split by the bolt)."""
    W, H = 1.2, 0.84; ink = '#4a2c18'; red = '#9a2c1c'
    o = [_rect(0, 0, W, H, '#eadbb4'), _rect(0.6, 0, 0.6, H, '#efe2c0')]
    o.append('<linearGradient id="gut" x1="0" x2="1"><stop offset="0" stop-color="#b89a6c" stop-opacity="0"/><stop offset="0.5" stop-color="#8a6a44" stop-opacity="0.55"/><stop offset="1" stop-color="#b89a6c" stop-opacity="0"/></linearGradient>')
    o.append(_rect(0.55, 0, 0.1, H, 'url(#gut)'))
    S = f'stroke="{ink}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    # -- left page: house, roof, rod, cloud, bolt, wire, ground stake
    o.append(f'<path d="M0.12,0.72 L0.12,0.47 L0.27,0.33 L0.42,0.47 L0.42,0.72" {S} stroke-width="0.006"/>')
    o.append(f'<path d="M0.10,0.48 L0.27,0.32 L0.44,0.48" {S} stroke-width="0.008"/>')
    for k in range(5): o.append(f'<line x1="{0.15 + k * 0.05:.3f}" y1="{0.46 - (0.06 if 1 <= k <= 3 else 0.02):.3f}" x2="{0.17 + k * 0.05:.3f}" y2="{0.47:.3f}" stroke="{ink}" stroke-width="0.002"/>')
    o.append(f'<rect x="0.24" y="0.6" width="0.06" height="0.12" {S} stroke-width="0.004"/><rect x="0.16" y="0.52" width="0.05" height="0.05" {S} stroke-width="0.004"/>')
    o.append(f'<path d="M0.27,0.32 L0.27,0.13" {S} stroke-width="0.007"/><path d="M0.262,0.14 L0.27,0.10 L0.278,0.14 Z" fill="{ink}"/>')        # the rod with its point
    o.append(f'<path d="M0.27,0.30 L0.33,0.30 L0.44,0.40 L0.44,0.76 L0.50,0.80" {S} stroke-width="0.004" stroke-dasharray="0.012 0.004"/>')      # wire down the wall
    o.append(f'<path d="M0.47,0.79 L0.53,0.79 M0.50,0.79 L0.50,0.82" {S} stroke-width="0.004"/>')
    for a in range(5): o.append(f'<line x1="0.50" y1="0.82" x2="{0.50 + 0.035 * math.cos(math.radians(20 + a * 35)):.3f}" y2="{0.82 + 0.02 * math.sin(math.radians(20 + a * 35)):.3f}" stroke="{red}" stroke-width="0.003"/>')
    o.append(f'<path d="M0.04,0.72 L0.56,0.72" {S} stroke-width="0.005"/>')
    for k in range(12): o.append(f'<line x1="{0.05 + k * 0.042:.3f}" y1="0.725" x2="{0.03 + k * 0.042:.3f}" y2="0.75" stroke="{ink}" stroke-width="0.002"/>')
    o.append(f'<path d="M0.08,0.10 q0.03,-0.05 0.08,-0.03 q0.04,-0.05 0.09,-0.01 q0.06,-0.02 0.07,0.03 q0.04,0.02 0.0,0.05 L0.09,0.14 q-0.04,-0.01 -0.01,-0.04 Z" {S} stroke-width="0.005"/>')
    o.append(f'<path d="M0.20,0.13 L0.235,0.06 L0.215,0.06 L0.26,0.0" {S} stroke-width="0.0" />')
    o.append(f'<path d="M0.18,0.135 L0.22,0.105 L0.205,0.10 L0.262,0.105" stroke="{red}" stroke-width="0.007" fill="none" stroke-linejoin="miter"/>')
    for (x1, y1, x2, y2) in ((0.36, 0.52, 0.36, 0.60), (0.38, 0.60, 0.40, 0.66)):
        o.append(f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{red}" stroke-width="0.004" marker-end="url(#ar)"/>')
    o.append(f'<defs><marker id="ar" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="{red}"/></marker></defs>')
    o.append(f'<path d="M0.47,0.36 L0.465,0.44 M0.475,0.48 L0.47,0.58 M0.475,0.62 L0.47,0.70" stroke="{red}" stroke-width="0.004" marker-end="url(#ar)"/>')
    o.append(f'<text x="0.30" y="0.06" font-family="Liberation Serif, serif" font-style="italic" font-size="0.034" fill="{ink}" text-anchor="middle">il fulmine segue il ferro</text>')
    o.append(f'<text x="0.10" y="0.81" font-family="Liberation Serif, serif" font-style="italic" font-size="0.022" fill="{ink}">terra</text>')
    o.append(f'<text x="0.035" y="0.32" font-family="Liberation Serif, serif" font-style="italic" font-size="0.026" fill="{ink}">fig. I</text>')
    # -- right page: hand-written lines, the sharp point enlarged, a tower without rod split by the bolt
    r = random.Random(8)
    for j in range(7):
        y = 0.08 + j * 0.035; x = 0.68; xe = 1.14 - r.uniform(0, 0.08); pts = []
        while x < xe: pts.append(f'{x:.3f},{y + r.uniform(-0.004, 0.004):.3f}'); x += r.uniform(0.012, 0.022)
        o.append(f'<polyline points="{" ".join(pts)}" stroke="{ink}" stroke-width="0.0035" fill="none" stroke-linejoin="round"/>')
    o.append(f'<circle cx="0.78" cy="0.48" r="0.08" {S} stroke-width="0.004"/><path d="M0.75,0.56 L0.77,0.42 L0.78,0.39 L0.79,0.42 L0.81,0.56" {S} stroke-width="0.005"/>')
    o.append(f'<path d="M0.71,0.38 L0.745,0.43 L0.732,0.435 L0.768,0.41" stroke="{red}" stroke-width="0.005" fill="none"/>')
    o.append(f'<path d="M0.97,0.74 L0.97,0.47 L1.0,0.44 L1.03,0.47 L1.03,0.74 M0.96,0.74 L1.04,0.74" {S} stroke-width="0.005"/><path d="M0.98,0.52 L1.02,0.52 L1.02,0.56 L0.98,0.56 Z" {S} stroke-width="0.003"/>')
    o.append(f'<path d="M0.93,0.37 L0.985,0.44 L0.975,0.45 L1.01,0.50 L0.995,0.60 L1.02,0.68" stroke="{red}" stroke-width="0.005" fill="none"/>')
    o.append(f'<path d="M1.06,0.40 L1.12,0.46 M1.12,0.40 L1.06,0.46" stroke="{red}" stroke-width="0.007"/>')
    o.append(f'<text x="0.78" y="0.62" font-family="Liberation Serif, serif" font-style="italic" font-size="0.024" fill="{ink}" text-anchor="middle">punta</text>')
    o.append(f'<text x="1.08" y="0.80" font-family="Liberation Serif, serif" font-size="0.022" fill="{ink}" text-anchor="end">— 47 —</text>')
    o.append(f'<path d="M0.3,0.84 L0.3,0.84" stroke="none"/>')
    return name, (K.svg_doc(int(W * ppd), int(H * ppd), W, H, ''.join(o)), int(W * ppd), int(H * ppd), False)

def _sky(name, night=False, W=16.0, H=8.0, ppd=60):
    if night: g = '<linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e2e7b"/><stop offset="0.6" stop-color="#1748ae"/><stop offset="1" stop-color="#204c8f"/></linearGradient>'
    else: g = ('<linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7d93d6"/><stop offset="0.45" stop-color="#c7a6c8"/>'
               '<stop offset="0.7" stop-color="#f2b896"/><stop offset="1" stop-color="#f7cf8e"/></linearGradient>')
    o = [g, _rect(0, 0, W, H, 'url(#s)')]
    if night: o.append('<circle cx="6.2" cy="2.4" r="0.55" fill="#f2f0e0"/><circle cx="6.2" cy="2.4" r="0.9" fill="#f2f0e0" opacity="0.18"/>')
    else: o.append('<circle cx="10.5" cy="6.6" r="1.6" fill="#fff0c0" opacity="0.5"/><ellipse cx="5" cy="3.0" rx="2.4" ry="0.35" fill="#f6d2c0" opacity="0.6"/>')
    roof = '#28306a' if night else '#8a5a6a'; r = random.Random(2); x = 0.0
    while x < W:                                                   # roofs of Brescia and one campanile
        w = r.uniform(0.8, 1.8); h = r.uniform(0.8, 1.6)
        o.append(f'<path d="M{x:.2f},{H} L{x:.2f},{H - h:.2f} L{x + w / 2:.2f},{H - h - 0.5:.2f} L{x + w:.2f},{H - h:.2f} L{x + w:.2f},{H} Z" fill="{roof}"/>')
        if night and r.random() < 0.5: o.append(_rect(x + w * 0.3, H - h * 0.6, 0.12, 0.16, '#ffc860'))
        x += w
    o.append(f'<path d="M7.6,{H} L7.6,3.2 L7.9,2.6 L8.2,3.2 L8.2,{H} Z" fill="{K.mulc(roof, 0.85)}"/><rect x="7.66" y="3.5" width="0.14" height="0.3" fill="{K.mulc(roof, 0.6)}"/><rect x="8.0" y="3.5" width="0.14" height="0.3" fill="{K.mulc(roof, 0.6)}"/>')
    return name, (K.svg_doc(int(W * ppd), int(H * ppd), W, H, ''.join(o)), int(W * ppd), int(H * ppd), False)

def textures():
    jobs = dict([_plaster('r_plaster'), _planks('r_floor', ['#9e5634', '#8e4a2c', '#a85e3a', '#94502e']),
                 _planks('r_boards', ['#7e4628', '#724024', '#86502e'], W=1.8, L=3.0, pw=0.36, seam='#2e160e'),
                 _beam('r_beam'), _straw('r_straw'), _blanket('r_blanket'), _book(), _sky('r_sky_dawn'), _sky('r_sky_night', night=True)])
    return K.raster(jobs)

def book_page_texture():
    """Path of the PNG of the open book's two pages (1560 x 1092 px, cream paper, sepia and red ink), for a flat insert."""
    return K.raster(dict([_book()]))['r_book']

# ----------------------------------------------------------------------------- geometry helpers
def _prism(mb, p0, p1, w, h, up, mat, uvlen=1.0):
    """Beam of width w (across), depth h (along -up) from p0 to p1: up = the face normal of the beam's top."""
    p0, p1 = Vector(p0), Vector(p1); a = (p1 - p0).normalized(); up = Vector(up).normalized(); s = a.cross(up).normalized()
    c = [p0 + s * (w / 2), p0 - s * (w / 2), p0 - s * (w / 2) - up * h, p0 + s * (w / 2) - up * h]
    d = p1 - p0; L = d.length; mb.pid += 1; mb._in = True
    for i in range(4):
        j = (i + 1) % 4; q = [c[i], c[j], c[j] + d, c[i] + d]
        ctr = sum(q, Vector()) / 4; mid = (c[0] + c[2]) / 2 + d / 2
        if (q[1] - q[0]).cross(q[3] - q[0]).dot(ctr - mid) < 0: q = q[::-1]
        mb.face(q, mat, [(0, 0), (1, 0), (1, L / uvlen), (0, L / uvlen)])
    for cap, sg in ((c, -1), ([x + d for x in c], 1)):
        q = list(cap)
        if (q[1] - q[0]).cross(q[2] - q[0]).dot(a * sg) < 0: q = q[::-1]
        mb.face(q, mat)
    mb._in = False

def _lathe(mb, c, prof, mat, seg=14):
    c = Vector(c); R = [[c + Vector((r * math.cos(2 * math.pi * i / seg), r * math.sin(2 * math.pi * i / seg), z)) for i in range(seg)] for (r, z) in prof]
    mb.pid += 1
    for k in range(len(prof) - 1):
        for i in range(seg):
            j = (i + 1) % seg; q = [R[k][i], R[k][j], R[k + 1][j], R[k + 1][i]]
            ctr = sum(q, Vector()) / 4; rv = ctr - Vector((c.x, c.y, ctr.z)); n = (q[1] - q[0]).cross(q[3] - q[0])
            if n.length < 1e-10: continue
            if n.dot(rv) < 0: q = q[::-1]
            mb.face(q, mat)
    if prof[0][0] > 0: mb.face(R[0][::-1], mat)
    if prof[-1][0] > 0: mb.face(R[-1], mat)

# ----------------------------------------------------------------------------- build
def build(preset='DAWN', clear=True):
    """Build the attic room into the current scene. Returns the anchors dict."""
    scene = bpy.context.scene; P = dict(PRESETS[preset]); STATE.clear(); STATE['P'] = P; STATE['preset'] = preset
    if clear: K.reset_scene(scene, 'ROOM_')
    SET = K.coll('SET', scene); LIGHTS = K.coll('LIGHTS', scene)
    for c_ in (SET, LIGHTS):
        for ob in list(c_.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for m in list(bpy.data.materials):
        if m.name.startswith(('ROOM_', 'SM_ink_')): bpy.data.materials.remove(m)
    K.setup_render(scene, 'final'); K.build_groups(P, 'ROOM_' + preset)
    tx = textures(); pre = 'ROOM_%s_' % preset; ink = P['ink']
    def C(h, gain=1.0, sm=1.0, ds=None): return K.mat_lit('%sc_%s_%g_%s_%s' % (pre, h.lstrip('#'), gain, sm, ds), h, gain=gain, shade_mul=sm, desat=ds)
    def TX(n, gain=1.0, sm=1.0, ds=None): return K.mat_lit('%st_%s_%g_%s_%s' % (pre, n, gain, sm, ds), image=tx[n], gain=gain, shade_mul=sm, desat=ds)
    def E(h, s): return K.mat_emit('%se_%s_%g' % (pre, h.lstrip('#'), s), h, strength=s)
    WM = tuple(P['warm_mul'])                                # warm surfaces keep a dusky warm shade (like the office walls); the floor goes blue-violet
    WD = P['warm_desat']
    M = dict(plaster=TX('r_plaster', 0.5, WM, WD), floor=TX('r_floor', 0.74, P.get('floor_shade', 1.0), 0.95), boards=TX('r_boards', 0.62, WM, WD), beam=TX('r_beam', 0.62, WM, WD),
             straw=TX('r_straw', 0.5, WM, max(0.2, WD)), blanket=TX('r_blanket', 0.6, 1.0, 0.3), page=TX('r_book', 0.36, 1.0, 0.3), wood=C('#7a4426', 0.62, WM, WD), dark_wood=C('#4e2a18', 0.7, WM, WD),
             iron=C('#3a3644', 0.8, 1.3, 0.9), cover=C('#6a2a1e', 0.7), wax=C('#efe0c0', 0.36, 1.0, 0.3), brass=C('#b08a40', 0.55), reveal=C('#c89a6c', 0.5),
             clay=C('#b05a34', 0.6), sky=K.mat_emit(pre + 'sky', image=tx[P['sky']], strength=P['sky_strength']))

    # ---- floor, knee walls, roof underside (boards), gables with the window opening
    mb = K.MB(); mb.quad((-XW, YF, 0), (2 * XW, 0, 0), (0, YB - YF, 0), M['floor'], (-XW / 1.8, YF / 3.0, XW / 1.8, 0)); K.obj(mb, 'floor', SET)
    mb = K.MB()
    for sx in (-1, 1):
        mb.quad((sx * XW, YF, 0), (0, YB - YF, 0), (0, 0, ZK), M['plaster'], (YF / 2, 0, 0, ZK / 2))
        p0 = Vector((sx * XW, YF, ZK)); mb.quad(p0, (0, YB - YF, 0), (-sx * XW, 0, ZR - ZK), M['boards'], (YF / 3.0, 0, 0, math.hypot(XW, ZR - ZK) / 1.8))
    K.obj(mb, 'shell', SET)
    mb = K.MB(); xs = [-XW, WIN['x0'], 0.0, WIN['x1'], XW]
    for (y, wallname) in ((YB, 'gable_back'), (YF, 'gable_front')):
        for xa, xb in zip(xs, xs[1:]):
            spans = [(0.0, None)]
            if y == YB and xa >= WIN['x0'] - 1e-6 and xb <= WIN['x1'] + 1e-6: spans = [(0.0, WIN['z0']), (WIN['z1'], None)]
            for (z0, z1) in spans:
                ta, tb = (roof_z(xa), roof_z(xb)) if z1 is None else (z1, z1)
                pts = [(xa, y, z0), (xb, y, z0), (xb, y, tb), (xa, y, ta)]
                mb.pid += 1; mb.face(pts, M['plaster'], [(xa / 2, z0 / 2), (xb / 2, z0 / 2), (xb / 2, tb / 2), (xa / 2, ta / 2)])
    # outer skin of the back gable (blocks the sun except at the window) and the window reveal
    for xa, xb in zip(xs, xs[1:]):
        spans = [(0.0, None)] if not (xa >= WIN['x0'] - 1e-6 and xb <= WIN['x1'] + 1e-6) else [(0.0, WIN['z0']), (WIN['z1'], None)]
        for (z0, z1) in spans:
            ta, tb = (roof_z(xa), roof_z(xb)) if z1 is None else (z1, z1); mb.pid += 1; mb.face([(xa, WALL_T, z0), (xb, WALL_T, z0), (xb, WALL_T, tb), (xa, WALL_T, ta)], M['reveal'])
    x0, x1, z0, z1 = WIN['x0'], WIN['x1'], WIN['z0'], WIN['z1']
    mb.quad((x0, 0, z0), (x1 - x0, 0, 0), (0, WALL_T, 0), M['reveal']); mb.quad((x0, WALL_T, z1), (x1 - x0, 0, 0), (0, -WALL_T, 0), M['reveal'])
    mb.quad((x0, WALL_T, z0), (0, -WALL_T, 0), (0, 0, z1 - z0), M['reveal']); mb.quad((x1, 0, z0), (0, WALL_T, 0), (0, 0, z1 - z0), M['reveal'])
    K.obj(mb, 'gables', SET)
    # roof outside skin above everything (keeps the sun out of the room except through the window)
    mb = K.MB()
    for sx in (-1, 1): mb.quad((sx * (XW + 0.3), YF - 0.4, ZK - 0.05), (0, YB - YF + 0.8, 0), (-sx * (XW + 0.3), 0, ZR - ZK + 0.35 + 0.05), M['dark_wood'])
    sk = K.obj(mb, 'roof_outer', SET)
    # window: frame, cross mullion, sill; shutters folded back outside; the sky card far behind
    mb = K.MB(); f = 0.06; yf0, yf1 = 0.10, 0.20
    mb.box((x0, yf0, z0), (x0 + f, yf1, z1), M['wood']); mb.box((x1 - f, yf0, z0), (x1, yf1, z1), M['wood'])
    mb.box((x0, yf0, z1 - f), (x1, yf1, z1), M['wood']); mb.box((x0, yf0, z0), (x1, yf1, z0 + f), M['wood'])
    xm, zm = (x0 + x1) / 2, (z0 + z1) / 2 + 0.08
    mb.box((xm - 0.03, yf0 + 0.01, z0), (xm + 0.03, yf1 - 0.01, z1), M['wood']); mb.box((x0, yf0 + 0.01, zm - 0.03), (x1, yf1 - 0.01, zm + 0.03), M['wood'])
    mb.box((x0 - 0.08, -0.12, z0 - 0.07), (x1 + 0.08, WALL_T, z0), M['wood'])
    K.obj(mb, 'window', SET, hull=K.hull_t(4.5), ink=ink)
    mb = K.MB(); mb.quad((-9.0, 7.0, -1.0), (18.0, 0, 0), (0, 0, 9.0), M['sky'], (0, 0, 1, 1)); K.obj(mb, 'sky', SET, shadow=False)

    # ---- rafters, collar ties, ridge beam, purlins (the slanted wooden beams)
    mb = K.MB(); up_l = Vector((-SLOPE, 0, 1)).normalized()
    for yb in (-0.55, -1.75, -2.95, -4.15, -5.35):
        for sx in (-1, 1):
            n = Vector((-sx * (ZR - ZK), 0, XW)).normalized()     # roof normal pointing into the room... the rafter hangs below the boards
            _prism(mb, (sx * XW, yb, ZK), (0.0, yb, ZR), 0.2, 0.26, (sx * (ZR - ZK), 0, XW), M['beam'])
        if yb == -1.75:
            zt = 4.3; xt = XW - (zt - ZK) / SLOPE; mb.box((-xt + 0.1, yb - 0.09, zt - 0.22), (xt - 0.1, yb + 0.09, zt), M['beam'])
    _prism(mb, (0, YF, ZR - 0.02), (0, YB, ZR - 0.02), 0.26, 0.3, (0, 0, 1), M['beam'])
    for sx in (-1, 1):
        xp = sx * 1.6; zp = roof_z(xp); _prism(mb, (xp, YF, zp - 0.24), (xp, YB, zp - 0.24), 0.18, 0.2, (sx * (ZR - ZK), 0, XW), M['beam'])
        mb.box((sx * XW - (0.14 if sx > 0 else 0), YF, ZK - 0.1), (sx * XW + (0.14 if sx < 0 else 0), YB, ZK + 0.06), M['beam'])     # wall plate
    K.obj(mb, 'beams', SET, hull=K.hull_t(4.5), ink=ink)

    # ---- straw bed: plank frame, straw mattress, patched blanket, straw bolster
    b = BED; mb = K.MB()
    mb.box((b['x0'], b['y0'], 0.18), (b['x1'], b['y1'], 0.42), M['wood'])
    for (lx, ly) in ((b['x0'], b['y0']), (b['x1'] - 0.1, b['y0']), (b['x0'], b['y1'] - 0.1), (b['x1'] - 0.1, b['y1'] - 0.1)): mb.box((lx, ly, 0), (lx + 0.1, ly + 0.1, 0.42), M['dark_wood'])
    mb.box((b['x0'] - 0.02, b['y1'] - 0.1, 0.0), (b['x1'], b['y1'], 1.25), M['wood'])                    # head board
    mb.box((b['x0'] - 0.02, b['y0'], 0.0), (b['x1'], b['y0'] + 0.08, 0.72), M['wood'])                   # foot board
    K.obj(mb, 'bed_frame', SET, hull=K.hull_t(4.0), ink=ink)
    mb = K.MB(); mb.box((b['x0'] + 0.04, b['y0'] + 0.1, 0.42), (b['x1'] - 0.03, b['y1'] - 0.12, b['top'] - 0.04), M['straw'])
    mb.box((b['x0'] + 0.12, b['y1'] - 0.62, b['top'] - 0.04), (b['x1'] - 0.1, b['y1'] - 0.14, b['top'] + 0.16), M['straw'])
    K.obj(mb, 'mattress', SET, hull=K.hull_t(4.0), ink=ink)
    mb = K.MB(); by1 = b['y1'] - 0.7
    mb.box((b['x0'] - 0.03, b['y0'] + 0.12, 0.40), (b['x1'] - 0.02, by1, b['top'] + 0.03), M['blanket'], mats=None, skip='bottom')
    mb.box((b['x0'] + 0.25, by1 - 0.02, b['top'] - 0.02), (b['x1'] - 0.1, by1 + 0.32, b['top'] + 0.09), M['blanket'])       # turned-back fold
    K.obj(mb, 'blanket', SET, hull=K.hull_t(4.0), ink=ink)

    # ---- the iron rod (thin, pointed, 2.6 D), leaning at the foot of the bed against a rafter
    mb = K.MB(); a = Vector(ROD_TOP) - Vector(ROD_BASE); L = a.length; tip0 = Vector(ROD_BASE) + a * ((L - 0.14) / L)
    mb.frustum(ROD_BASE, tip0, 0.026, 0.024, M['iron'], seg=8); mb.frustum(tip0, ROD_TOP, 0.024, 0.0, M['iron'], seg=8, cap1=False)
    mb.frustum(Vector(ROD_BASE) + a * 0.06, Vector(ROD_BASE) + a * 0.075, 0.036, 0.036, M['iron'], seg=8)       # a forged collar near the foot
    rod = K.obj(mb, 'rod', SET, hull=0.009, ink=ink); STATE['rod_len'] = L

    # ---- stool with the open book and the candle
    sx_, sy_, sz_ = STOOL; mb = K.MB()
    _lathe(mb, (sx_, sy_, sz_ - 0.08), [(0.0, 0.0), (0.4, 0.0), (0.42, 0.04), (0.4, 0.08), (0.0, 0.08)], M['wood'], seg=18)
    for k in range(3):
        ang = math.radians(90 + 120 * k); top = Vector((sx_ + 0.22 * math.cos(ang), sy_ + 0.22 * math.sin(ang), sz_ - 0.08)); bot = Vector((sx_ + 0.36 * math.cos(ang), sy_ + 0.36 * math.sin(ang), 0))
        mb.frustum(bot, top, 0.04, 0.045, M['dark_wood'], seg=8)
    K.obj(mb, 'stool', SET, hull=K.hull_t(3.5), ink=ink)
    bw, bh = 0.62, 0.43; bx, byy = sx_ - 0.04, sy_ - 0.02; zb = sz_ + 0.035; tilt = 0.035
    mb = K.MB(); mb.box((bx - bw / 2 - 0.02, byy - bh / 2 - 0.02, sz_), (bx + bw / 2 + 0.02, byy + bh / 2 + 0.02, zb - 0.005), M['cover'])
    K.obj(mb, 'book_cover', SET, hull=0.006, ink=ink)
    mb = K.MB()
    mb.face([(bx - bw / 2, byy - bh / 2, zb + tilt), (bx, byy - bh / 2, zb), (bx, byy + bh / 2, zb), (bx - bw / 2, byy + bh / 2, zb + tilt)], M['page'], [(0, 0), (0.5, 0), (0.5, 1), (0, 1)])
    mb.pid += 1
    mb.face([(bx, byy - bh / 2, zb), (bx + bw / 2, byy - bh / 2, zb + tilt), (bx + bw / 2, byy + bh / 2, zb + tilt), (bx, byy + bh / 2, zb)], M['page'], [(0.5, 0), (1, 0), (1, 1), (0.5, 1)])
    K.obj(mb, 'book_pages', SET)
    STATE['book'] = dict(centre=(bx, byy, zb + tilt / 2), size=(bw, bh), normal=(0, 0, 1), top_edge='+y', page_z=zb)
    cx, cy, cz = CANDLE; mb = K.MB()
    _lathe(mb, (cx, cy, cz), [(0.0, 0.0), (0.11, 0.0), (0.11, 0.025), (0.045, 0.03), (0.045, 0.06), (0.0, 0.06)], M['brass'], seg=14)
    _lathe(mb, (cx, cy, cz + 0.06), [(0.0, 0.0), (0.035, 0.0), (0.035, 0.22), (0.028, 0.235), (0.0, 0.235)], M['wax'], seg=12)
    K.obj(mb, 'candle', SET, hull=0.006, ink=ink)
    if P['flame'] > 0:
        mb = K.MB(); _lathe(mb, (cx, cy, cz + 0.30), [(0.0, -0.0), (0.022, 0.02), (0.026, 0.045), (0.015, 0.075), (0.0, 0.1)], E('#ffcf6a', P['flame']), seg=10)
        K.obj(mb, 'flame', SET, shadow=False)

    # ---- crucifix on the back gable (right of the window), a peg rail with a cap, a clay jug, a small chest
    mb = K.MB(); cxz = (1.25, 2.45)
    mb.box((cxz[0] - 0.03, -0.05, cxz[1] - 0.24), (cxz[0] + 0.03, -0.002, cxz[1] + 0.22), M['dark_wood']); mb.box((cxz[0] - 0.13, -0.05, cxz[1] + 0.04), (cxz[0] + 0.13, -0.002, cxz[1] + 0.1), M['dark_wood'])
    mb.box((cxz[0] - 0.012, -0.065, cxz[1] - 0.12), (cxz[0] + 0.012, -0.05, cxz[1] + 0.06), M['brass'])
    K.obj(mb, 'crucifix', SET, hull=0.006, ink=ink)
    mb = K.MB(); mb.box((-XW + 0.002, -3.6, 1.25), (-XW + 0.06, -1.6, 1.33), M['wood'])
    for py in (-3.2, -2.6, -2.0): mb.frustum((-XW + 0.06, py, 1.29), (-XW + 0.2, py, 1.33), 0.02, 0.02, M['dark_wood'], seg=6)
    mb.box((-XW + 0.06, -2.75, 0.72), (-XW + 0.12, -2.45, 1.28), C('#5e6a8a', 0.6, 1.0, 0.6))     # a hanging smock
    _lathe(mb, (-1.9, -0.6, 0.0), [(0.0, 0.0), (0.14, 0.0), (0.2, 0.12), (0.18, 0.3), (0.09, 0.38), (0.1, 0.46), (0.0, 0.46)], M['clay'], seg=14)
    mb.box((-2.65, -5.2, 0.0), (-1.75, -4.45, 0.62), M['wood'], mats=dict(top=M['dark_wood']))
    mb.box((-2.68, -5.23, 0.62), (-1.72, -4.42, 0.68), M['dark_wood'])
    K.obj(mb, 'props', SET, hull=K.hull_t(4.0), ink=ink)

    # ---- key light, grade
    K.add_key(P, LIGHTS); K.setup_grade(scene, P)
    for ob in SET.objects: no_bounce(ob)
    A = anchors(); STATE['A'] = A
    return A

def anchors():
    P = STATE['P']; bk = STATE['book']
    cams = dict(
        push_rod=dict(loc=(-1.45, -5.75, 2.1), look_at=(1.5, -3.6, 1.15), lens=22,
                      move=dict(loc=(-0.55, -4.95, 2.0), look_at=(1.55, -3.65, 1.15), note='slow push 1.2 D toward the rod and the bed foot, eye level of the boy')),
        book_insert=dict(loc=(bk['centre'][0], bk['centre'][1] - 0.02, bk['centre'][2] + 0.85), look_at=bk['centre'], up=(0, 1, 0), lens=22),
        room_wide=dict(loc=(-0.6, -4.95, 4.15), look_at=(0.7, -1.3, 1.25), lens=22),
    )
    return dict(
        room=dict(x_left=-XW, x_right=XW, y_back=YB, y_front=YF, knee=ZK, ridge=ZR, slope=round(SLOPE, 4), wall_t=WALL_T),
        window=dict(WIN, y=YB, centre=WIN_C), key_dir=tuple(round(x, 5) for x in P['key_dir']), sun_elevation_deg=round(_elev(), 1),
        light_target=LIGHT_TARGET,
        bed=dict(BED), bed_top=BED['top'],
        rod_lean=dict(base=ROD_BASE, top=ROD_TOP, tip=ROD_TOP, length=round(STATE['rod_len'], 3), radius=0.026),
        stool=STOOL, book=bk, candle=CANDLE, candle_flame=(CANDLE[0], CANDLE[1], CANDLE[2] + 0.35),
        crucifix=(1.25, -0.05, 2.45),
        hero_mark=HERO_MARK, bed_sit_mark=BED_SIT['feet'], bed_sit_seat_z=BED_SIT['seat_z'],
        cams=cams,
        cam_notes=dict(push_rod='eye level of the boy (2.0-2.15 D), slow push toward the rod and the bed foot; cams[...]["move"] = end pose',
                       book_insert='0.85 D straight above the open book (up = +y: the top of the pages points to the window)',
                       room_wide='high corner under the ridge at the front gable, the whole room, window and light patch'),
        render=dict(preset=STATE['preset'], samples=12, resolution=(720, 1280), key=P['key'], shade=P['shade']))

# ----------------------------------------------------------------------------- CLI
def stage(A, cam_name):
    K.clear_actors()
    if cam_name == 'book_insert': return
    cs = A['cams'][cam_name]; mark = A['bed_sit_mark'] if cam_name == 'push_rod' else A['hero_mark']
    placeholder_actor('hero', dict(yaw=0.35, expr='determined', arm_l='down', arm_r='down', legs='stand'), mark, face_to=cs['loc'], name='actor_boy', scale=0.8)

def cli_stills(quality='preview', outdir=None, presets=('DAWN', 'NIGHT')):
    outdir = outdir or os.path.join(HERE, 'small_work', 'stills'); os.makedirs(outdir, exist_ok=True)
    for pr in presets:
        A = build(pr); sc = bpy.context.scene; setup_render(sc, quality)
        for nm, cs in A['cams'].items():
            make_camera(cs); stage(A, nm)
            w, c = K.render(os.path.join(outdir, 'room_%s_%s.png' % (pr, nm))); print('room %s %s: %.1f s wall %.1f s cpu' % (pr, nm, w, c), flush=True)

def cli_timing(n=3, preset='DAWN', cam='push_rod'):
    A = build(preset); sc = bpy.context.scene; setup_render(sc, 'final'); cs = A['cams'][cam]; c = make_camera(cs); stage(A, cam)
    res = []
    for i in range(n):
        c.location.x += 0.03; w, cp = K.render(os.path.join(HERE, 'small_work', 'timing_room_%d.png' % i)); res.append((w, cp)); print('frame %d: %.2f s wall %.2f s cpu' % (i, w, cp), flush=True)
    print('TIMING room %s %s: cpu median %.2f s, wall median %.2f s (720x1280, %d samples, %d threads)' % (preset, cam, sorted(r[1] for r in res)[n // 2], sorted(r[0] for r in res)[n // 2], sc.cycles.samples, sc.render.threads))

if __name__ == '__main__':
    a = sys.argv[1:]; cmd = a[0] if a else 'stills'
    if cmd == 'stills': cli_stills(a[1] if len(a) > 1 else 'preview', presets=tuple(a[2].split(',')) if len(a) > 2 else ('DAWN', 'NIGHT'))
    elif cmd == 'timing': cli_timing(preset=a[1] if len(a) > 1 else 'DAWN', cam=a[2] if len(a) > 2 else 'push_rod')
    elif cmd == 'digest': build(a[1] if len(a) > 1 else 'DAWN'); print('DIGEST', K.digest())
    elif cmd == 'book': print(book_page_texture())
    else: print(__doc__)

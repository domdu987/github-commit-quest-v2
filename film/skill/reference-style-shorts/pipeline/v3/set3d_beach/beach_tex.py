#!/usr/bin/env python3
"""beach_tex.py : flat per-surface artwork for the 3D beach colony (cottage walls, shingles, boardwalk planks, the sign,
rain streaks), drawn as SVG and rasterised by headless Chromium with the office set's raster.js (imported by path, never copied).

    import beach_tex as BT
    paths = BT.ensure()          # {name: png path}; cached in v3/set3d_beach/tex/ by content hash
    BT.SIZE[name] -> (w_D, h_D)  # size of one image (or one tile) in D

Colours are what the surface shows in neutral light; the lit material turns them into shade and sun."""
import os, sys, json, random, hashlib, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
RASTER = os.path.join(PROJ, 'v3', 'set3d', 'raster.js')
TEX = os.path.join(HERE, 'tex'); TMP = os.path.join(PROJ, 'v3', 'tmp', 'beach', 'tex_svg')
JOBS = {}; SIZE = {}

def hx(c):
    c = c.lstrip('#'); return [int(c[i:i + 2], 16) for i in (0, 2, 4)]
def mul(c, k): return '#%02x%02x%02x' % tuple(max(0, min(255, int(round(v * k)))) for v in hx(c))
def mix(a, b, t): A, B = hx(a), hx(b); return '#%02x%02x%02x' % tuple(int(round(A[i] + (B[i] - A[i]) * t)) for i in range(3))

class Doc(object):
    """SVG in D units (x right, y DOWN from the top edge), ppd pixels per D."""
    def __init__(s, w, h, ppd): s.w, s.h, s.ppd = w, h, ppd; s.o = []; s.defs = []
    def rect(s, x, y, w, h, fill, stroke=None, sw=0.0, rx=0.0, extra=''):
        st = f' stroke="{stroke}" stroke-width="{sw:g}"' if stroke else ''
        s.o.append(f'<rect x="{x:.4f}" y="{y:.4f}" width="{w:.4f}" height="{h:.4f}" rx="{rx:g}" fill="{fill}"{st} {extra}/>')
    def line(s, x0, y0, x1, y1, col, sw, extra=''):
        s.o.append(f'<line x1="{x0:.4f}" y1="{y0:.4f}" x2="{x1:.4f}" y2="{y1:.4f}" stroke="{col}" stroke-width="{sw:g}" stroke-linecap="round" {extra}/>')
    def poly(s, pts, fill, stroke=None, sw=0.0, extra=''):
        st = f' stroke="{stroke}" stroke-width="{sw:g}" stroke-linejoin="round"' if stroke else ''
        s.o.append('<polygon points="%s" fill="%s"%s %s/>' % (' '.join('%.4f,%.4f' % p for p in pts), fill, st, extra))
    def circ(s, x, y, r, fill, stroke=None, sw=0.0):
        st = f' stroke="{stroke}" stroke-width="{sw:g}"' if stroke else ''
        s.o.append(f'<circle cx="{x:.4f}" cy="{y:.4f}" r="{r:.4f}" fill="{fill}"{st}/>')
    def text(s, x, y, size, txt, fill, weight='bold', family='DejaVu Serif', spacing=0.02, anchor='middle', length=None):
        tl = f' textLength="{length:g}" lengthAdjust="spacingAndGlyphs"' if length else ''
        s.o.append(f'<text x="{x:.4f}" y="{y:.4f}" font-family="{family}" font-weight="{weight}" font-size="{size:g}" letter-spacing="{spacing:g}" '
                   f'text-anchor="{anchor}" fill="{fill}"{tl}>{txt}</text>')
    def svg(s):
        W, H = int(round(s.w * s.ppd)), int(round(s.h * s.ppd))
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {s.w:g} {s.h:g}" preserveAspectRatio="none" '
                f'style="display:block"><defs>{"".join(s.defs)}</defs>{"".join(s.o)}</svg>'), W, H

def job(name, d, transparent=False):
    svg, W, H = d.svg(); JOBS[name] = dict(svg=svg, w=W, h=H, transparent=transparent); SIZE[name] = (d.w, d.h)

# ----------------------------------------------------------------------------- cottages
# name: body, trim, roof, door, shutter.  Bodies follow LOOK_SPEC 3.3 (cream, red, blue-grey) plus cedar shingle and a pale yellow.
SCHEMES = {
    'cream':  dict(body='#ebddc8', trim='#f6efe2', roof='#5b211d', door='#6b2a22', shutter='#2f6a5a'),
    'red':    dict(body='#b84735', trim='#f3e6cf', roof='#4d3e3f', door='#3b2a35', shutter='#f3e6cf'),
    'blue':   dict(body='#7f8fbf', trim='#f6efe2', roof='#5b211d', door='#5b211d', shutter='#b84735'),
    'cedar':  dict(body='#a7745a', trim='#efe2c8', roof='#4d3e3f', door='#2f6a5a', shutter='#2f6a5a'),
    'yellow': dict(body='#e3c27a', trim='#f6efe2', roof='#5b211d', door='#2f5a8a', shutter='#2f5a8a'),
}
W_C, Z_FLOOR, Z_EAVE, Z_RIDGE, D_C = 3.2, 0.6, 2.6, 3.95, 3.2     # cottage width, floor, eaves, ridge, depth (D); shared with beach3d.py
PPD_C = 170

def _siding(d, x0, x1, y0, y1, body, pitch=0.21, shingle=False, seed=1):
    d.rect(x0, y0, x1 - x0, y1 - y0, body)
    dk, hi = mul(body, 0.66), mul(body, 1.09); y = y1; r = random.Random(seed)
    while y > y0:
        d.line(x0, y, x1, y, dk, 0.016); d.line(x0, y - 0.025, x1, y - 0.025, hi, 0.01)
        if shingle:                                         # cedar shingles: staggered butt joints
            x = x0 + r.uniform(0, 0.3)
            while x < x1:
                d.line(x, y - pitch + 0.02, x, y - 0.01, dk, 0.012); x += r.uniform(0.22, 0.42)
        y -= pitch

def _window(d, cx, ytop, w, h, S, shutters=True):
    t = S['trim']; ink = mul(S['body'], 0.45)
    if shutters:
        for sx in (cx - w / 2 - 0.30, cx + w / 2 + 0.04):
            d.rect(sx, ytop, 0.26, h, S['shutter'], ink, 0.014)
            for k in range(1, 8): d.line(sx + 0.04, ytop + k * h / 8, sx + 0.22, ytop + k * h / 8, mul(S['shutter'], 0.7), 0.012)
    d.rect(cx - w / 2 - 0.06, ytop - 0.06, w + 0.12, h + 0.12, t, ink, 0.016)
    d.rect(cx - w / 2, ytop, w, h, '#9cc0f0', ink, 0.012)
    d.poly([(cx - w / 2, ytop), (cx - w / 2 + w * 0.55, ytop), (cx - w / 2, ytop + h * 0.6)], '#c4dcf7')    # sky reflection
    d.line(cx, ytop, cx, ytop + h, t, 0.05); d.line(cx - w / 2, ytop + h / 2, cx + w / 2, ytop + h / 2, t, 0.05)
    d.rect(cx - w / 2 - 0.12, ytop + h + 0.04, w + 0.24, 0.08, t, ink, 0.014)             # sill

def _door(d, cx, ybot, w, h, S):
    ink = mul(S['body'], 0.45); D_ = S['door']
    d.rect(cx - w / 2 - 0.07, ybot - h - 0.07, w + 0.14, h + 0.07, S['trim'], ink, 0.016)
    d.rect(cx - w / 2, ybot - h, w, h, D_, ink, 0.014)
    d.rect(cx - w / 2 + 0.1, ybot - h + 0.1, w - 0.2, h * 0.36, '#9cc0f0', mul(D_, 0.5), 0.012)        # glazed upper half
    d.line(cx, ybot - h + 0.1, cx, ybot - h + 0.1 + h * 0.36, mul(D_, 1.2), 0.03)
    for k in (0.55, 0.78): d.rect(cx - w / 2 + 0.1, ybot - h + h * k, w - 0.2, h * 0.17, mul(D_, 1.15), mul(D_, 0.6), 0.012)
    d.circ(cx + w / 2 - 0.12, ybot - h * 0.46, 0.035, '#e2a630', mul(D_, 0.5), 0.01)

def cottage_tex(key, S, seed):
    """front (gable, door, two windows), back (gable, window, small door), side (one window) for one colour scheme."""
    H = Z_RIDGE - Z_FLOOR + 0.05; ze = Z_EAVE - Z_FLOOR      # texture covers floor .. ridge (gable faces); y down from the ridge
    sh = key == 'cedar'
    for face in ('front', 'back'):
        d = Doc(W_C, H, PPD_C); yb = H                       # y of the floor line
        _siding(d, 0, W_C, 0, H, S['body'], pitch=0.2 if sh else 0.21, shingle=sh, seed=seed)
        ink = mul(S['body'], 0.45)
        d.rect(0, 0, 0.12, H, S['trim'], ink, 0.012); d.rect(W_C - 0.12, 0, 0.12, H, S['trim'], ink, 0.012)    # corner boards
        d.rect(0, H - ze - 0.06, W_C, 0.1, S['trim'], ink, 0.012)                      # frieze board at the eaves line
        cxv = W_C / 2; d.poly([(cxv - 0.22, H - ze - 0.32), (cxv + 0.22, H - ze - 0.32), (cxv, H - ze - 0.72)], mul(S['body'], 0.55), S['trim'], 0.04)   # gable vent
        if face == 'front':
            _door(d, W_C * 0.5, yb - 0.02, 0.78, 1.55, S)
            _window(d, 0.62, yb - 1.6, 0.52, 0.72, S, shutters=False); _window(d, W_C - 0.62, yb - 1.6, 0.52, 0.72, S, shutters=False)
        else:
            _window(d, W_C * 0.32, yb - 1.62, 0.6, 0.76, S); _door(d, W_C * 0.76, yb - 0.02, 0.66, 1.45, S)
        job('cot_%s_%s' % (key, face), d)
    d = Doc(D_C, ze, PPD_C)
    _siding(d, 0, D_C, 0, ze, S['body'], pitch=0.2 if sh else 0.21, shingle=sh, seed=seed + 7)
    ink = mul(S['body'], 0.45)
    d.rect(0, 0, 0.12, ze, S['trim'], ink, 0.012); d.rect(D_C - 0.12, 0, 0.12, ze, S['trim'], ink, 0.012); d.rect(0, 0, D_C, 0.1, S['trim'], ink, 0.012)
    _window(d, D_C * 0.5, ze - 1.62, 0.6, 0.76, S)
    job('cot_%s_side' % key, d)

def shingles(name, base, seed):
    """one 1.2 x 1.2 D tile of roof shingles, rows of staggered tabs."""
    d = Doc(1.2, 1.2, 300); r = random.Random(seed); d.rect(0, 0, 1.2, 1.2, base); rows = 8; rh = 1.2 / rows
    for j in range(rows):
        y = j * rh; x = -r.uniform(0, 0.2) if j % 2 else -0.1
        while x < 1.2:
            w = r.uniform(0.13, 0.24); k = r.uniform(0.86, 1.14)
            for dx in (0.0, -1.2, 1.2):                    # horizontally seamless
                d.rect(x + dx, y, w - 0.012, rh - 0.006, mul(base, k))
            x += w
        d.line(0, y + rh - 0.004, 1.2, y + rh - 0.004, mul(base, 0.55), 0.016)
    job(name, d)

def planks():
    """boardwalk: 1.6 D wide (across the walk) x 2.0 D along it; planks run across the walk."""
    d = Doc(1.6, 2.0, 256); r = random.Random(11); base = '#a0583f'; n = 10; pw = 2.0 / n
    for j in range(n):
        c = mix(base, '#7e3f31', r.uniform(0, 0.6)); y = j * pw
        d.rect(0, y, 1.6, pw, c); d.line(0, y + 0.012, 1.6, y + 0.012, '#4d2c1e', 0.022)
        for k in range(2): yy = y + r.uniform(0.04, pw - 0.04); d.line(r.uniform(0, 0.6), yy, r.uniform(0.9, 1.6), yy, mul(c, 0.85), 0.008)
        for nx in (0.1, 1.5): d.circ(nx, y + pw / 2, 0.012, '#3a2418')
    job('planks', d)

def sign():
    d = Doc(2.2, 0.95, 300); ink = '#2a1712'
    d.rect(0, 0, 2.2, 0.95, '#f6efe2', ink, 0.03); d.rect(0.06, 0.06, 2.08, 0.83, 'none', '#b61d32', 0.012)
    d.text(1.1, 0.42, 0.30, 'BATHING BEACH', '#b61d32', spacing=0.01, length=1.9)
    d.line(0.3, 0.52, 1.9, 0.52, '#b61d32', 0.012)
    d.text(1.1, 0.68, 0.11, 'NO LIFEGUARD AFTER 5 P.M.', '#3d2a22', spacing=0.008, length=1.6)
    d.text(1.1, 0.83, 0.085, 'SUFFOLK COUNTY  1938', '#836d4e', weight='normal', spacing=0.01, length=1.0)
    job('sign', d)

def chair_sign():
    d = Doc(1.0, 0.3, 300); d.rect(0, 0, 1.0, 0.3, '#b61d32'); d.text(0.5, 0.215, 0.17, 'LIFEGUARD', '#f6efe2', spacing=0.01, length=0.86)
    job('chair_sign', d)

def rain():
    """transparent tile of thin slanted drizzle streaks, 4 x 4 D at 128 px per D (seamless vertically and horizontally)."""
    d = Doc(4.0, 4.0, 128); r = random.Random(23)
    for i in range(70):
        x, y = r.uniform(0, 4), r.uniform(0, 4); L = r.uniform(0.25, 0.6); a = r.uniform(0.35, 0.8)
        for dx in (-4, 0, 4):
            for dy in (-4, 0, 4):
                d.line(x + dx, y + dy, x + dx - L * 0.12, y + dy + L, '#eef0fb', r.uniform(0.010, 0.018), extra=f'opacity="{a:.2f}"')
    job('rain', d, transparent=True)

def headland():
    """far bluffs: two flat silhouettes with soft top, transparent."""
    d = Doc(16.0, 1.0, 80); r = random.Random(3); pts = [(0, 1.0)]
    x = 0.0
    while x < 16:
        pts.append((x, 1.0 - (0.25 + 0.6 * abs(__import__('math').sin(x * 0.5 + r.uniform(0, 0.3)))) * (0.6 + 0.4 * r.random()))); x += 0.6
    pts.append((16, 1.0)); d.poly(pts, '#ffffff')
    job('headland', d, transparent=True)

ALL = None
def _all():
    JOBS.clear()
    for i, (k, S) in enumerate(SCHEMES.items()): cottage_tex(k, S, 10 + i)
    shingles('roof_maroon', '#5b211d', 1); shingles('roof_slate', '#4d3e3f', 2)
    planks(); sign(); chair_sign(); rain(); headland()

def ensure(verbose=True):
    os.makedirs(TEX, exist_ok=True); os.makedirs(TMP, exist_ok=True); _all()
    mpath = os.path.join(TEX, 'manifest.json'); man = json.load(open(mpath)) if os.path.exists(mpath) else {}
    todo = []; out = {}
    for name, j in JOBS.items():
        h = hashlib.sha1((j['svg'] + str(j['transparent'])).encode()).hexdigest(); png = os.path.join(TEX, name + '.png'); out[name] = png
        if man.get(name) != h or not os.path.exists(png):
            sp = os.path.join(TMP, name + '.svg'); open(sp, 'w').write(j['svg'])
            todo.append(dict(src=sp, out=png, w=j['w'], h=j['h'], transparent=j['transparent'])); man[name] = h
    if todo:
        jp = os.path.join(TMP, 'tex_jobs.json'); json.dump(todo, open(jp, 'w'))
        r = subprocess.run(['node', RASTER, jp], env=dict(os.environ, NODE_PATH=os.environ.get('NODE_PATH', '/opt/node22/lib/node_modules')), capture_output=True, text=True)
        if r.returncode != 0: raise RuntimeError('texture raster failed: ' + r.stderr[-2000:])
        if verbose: print('beach textures rasterised:', len(todo))
        json.dump(man, open(mpath, 'w'), indent=0)
    return out

if __name__ == '__main__':
    p = ensure(); print(json.dumps({k: SIZE[k] for k in p}, indent=0))

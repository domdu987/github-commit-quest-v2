#!/usr/bin/env python3
"""kitchen_tex.py : artwork of the kitchen set (shots 15 and 26), drawn as SVG by Python, rasterised by headless
Chromium (v3/set3d/raster.js, Playwright), cached by SVG sha1 in tex/manifest.json.

    import kitchen_tex as KT
    tex = KT.ensure()            # {name: png path or [png paths] for sequences}

Static: oilcloth (red-check tile), kwall (mustard wallpaper tile), curtain (blue gingham panel), toast.
Sequences: steam (24-frame loop), drizzle (24-frame loop: grey sky, grey sea, rain, drops on the panes),
wave (92 frames, one per film frame g 1873..1964: the wall of water, lightning, rivulets), crack (6 frames, pane crack).
The window sequences are drawn for the exterior card of kitchen3d (EXT_W x EXT_H D, centre EXT_C), so a point of the
card at world (x, z) is pixel ((x - x0) * PPD, (z1 - z) * PPD)."""
import os, sys, json, math, random, hashlib, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
TEX = os.path.join(HERE, 'tex'); TMP = os.path.join(HERE, 'work', 'svg')
RASTER = os.path.join(PROJ, 'v3', 'set3d', 'raster.js')

# exterior card (world, D): the card stands at y = EXT_Y behind the window wall, x0..x1, z0..z1
EXT = dict(x0=-1.9, x1=2.3, z0=0.9, z1=4.1, y=0.9, ppd=300)
WIN = dict(x0=-0.40, x1=0.90, z0=1.98, z1=3.06)          # glass opening (world), see kitchen3d.WIN
WAVE_G0, WAVE_N = 1873, 92
LIGHTNING = {1873: 1.0, 1874: 0.75, 1875: 0.45, 1876: 0.2, 1889: 0.35, 1890: 1.0, 1891: 0.8, 1892: 0.25, 1893: 0.6, 1894: 0.15,
             1935: 0.7, 1936: 0.3}                        # film frame -> lightning strength (window and key pulse)
CRACK_G = 1923                                             # 64.00 on the narration clock: a pane cracks

def ext_px(x, z):
    return ((x - EXT['x0']) * EXT['ppd'], (EXT['z1'] - z) * EXT['ppd'])

def ext_size():
    return int(round((EXT['x1'] - EXT['x0']) * EXT['ppd'])), int(round((EXT['z1'] - EXT['z0']) * EXT['ppd']))

def svg(W, H, body, defs=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="display:block">'
            f'<defs>{defs}</defs>{body}</svg>')

ROUGH = ('<filter id="rough" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="3"/>'
         '<feDisplacementMap in="SourceGraphic" scale="5"/></filter>')

# ----------------------------------------------------------------------------- static surfaces
def oilcloth(px=600, D=0.6):
    """Seamless red-check oilcloth tile, D x D world units (check 0.075 D)."""
    s = px / D; c = 0.075 * s; o = [f'<rect width="{px}" height="{px}" fill="#efd7a8"/>']
    n = int(round(px / (2 * c)))
    for i in range(n):
        x = i * 2 * c
        o.append(f'<rect x="{x:.1f}" y="0" width="{c:.1f}" height="{px}" fill="#dc6c26" opacity="0.74"/>')
        o.append(f'<rect x="0" y="{x:.1f}" width="{px}" height="{c:.1f}" fill="#c9402a" opacity="0.74"/>')
    for i in range(n):                                    # crossings print darker
        for j in range(n):
            o.append(f'<rect x="{i * 2 * c:.1f}" y="{j * 2 * c:.1f}" width="{c:.1f}" height="{c:.1f}" fill="#7c2410" opacity="0.88"/>')
    r = random.Random(11)                                 # woven hatching inside the bands, faint wear
    for i in range(160):
        x = r.uniform(0, px); y = r.uniform(0, px); L = r.uniform(4, 12)
        o.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x + L:.1f}" y2="{y:.1f}" stroke="#7a1a12" stroke-width="1.2" opacity="0.35"/>')
    return svg(px, px, ''.join(o)), px, px

def kwall(W=400, H=600, D=(0.4, 0.6)):
    """Mustard kitchen wallpaper tile: cream pin stripes, small red-orange flower sprigs (seamless)."""
    s = W / D[0]; o = [f'<rect width="{W}" height="{H}" fill="#c4853c"/>']
    for x in (0.0, 0.2, 0.4):
        o.append(f'<rect x="{x * s - 4:.1f}" y="0" width="8" height="{H}" fill="#e6b468" opacity="0.8"/>')
        o.append(f'<line x1="{x * s + 7:.1f}" y1="0" x2="{x * s + 7:.1f}" y2="{H}" stroke="#8a4a1c" stroke-width="2"/>')
    for (cx, cy) in ((0.1, 0.15), (0.3, 0.45)):
        X, Y = cx * s, cy * s
        for a in range(5):
            t = a * 72 * math.pi / 180
            o.append(f'<ellipse cx="{X + 13 * math.cos(t):.1f}" cy="{Y + 13 * math.sin(t):.1f}" rx="9" ry="9" fill="#c8352a" stroke="#5e1a10" stroke-width="2.5"/>')
        o.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="6" fill="#f2c86a" stroke="#5e1a10" stroke-width="2"/>')
        o.append(f'<path d="M{X:.1f},{Y + 18:.1f} q -6,26 4,44 M{X - 2:.1f},{Y + 40:.1f} q -16,-6 -22,4 M{X + 2:.1f},{Y + 48:.1f} q 16,-8 22,2" '
                 f'fill="none" stroke="#4f5d2a" stroke-width="4" stroke-linecap="round"/>')
    return svg(W, H, ''.join(o)), W, H

def curtain(W=500, H=800):
    """Blue gingham curtain panel (1.0 x 1.6 D) with painted folds and a red ric-rac hem."""
    o = [f'<rect width="{W}" height="{H}" fill="#efe3c9"/>']; c = 22
    for i in range(0, W, 2 * c): o.append(f'<rect x="{i}" y="0" width="{c}" height="{H}" fill="#2f56a8" opacity="0.65"/>')
    for j in range(0, H, 2 * c): o.append(f'<rect x="0" y="{j}" width="{W}" height="{c}" fill="#2f56a8" opacity="0.65"/>')
    for k in range(7):                                     # fold shading: dark troughs, light ridges
        x = (k + 0.5) * W / 7
        o.append(f'<rect x="{x - 18:.1f}" y="0" width="36" height="{H}" fill="#1f2c55" opacity="0.28"/>')
        o.append(f'<rect x="{x + 22:.1f}" y="0" width="10" height="{H}" fill="#ffffff" opacity="0.18"/>')
    z = ' '.join(f'{x},{H - 30 + (8 if (x // 12) % 2 else -8)}' for x in range(0, W + 12, 12))
    o.append(f'<rect x="0" y="{H - 44}" width="{W}" height="44" fill="#efe3c9"/>')
    o.append(f'<polyline points="{z}" fill="none" stroke="#c4392a" stroke-width="9"/>')
    o.append(f'<rect x="3" y="3" width="{W - 6}" height="{H - 6}" fill="none" stroke="#2a1712" stroke-width="6"/>')
    return svg(W, H, ''.join(o)), W, H

def toast(W=400, H=400):
    o = [f'<rect width="{W}" height="{H}" fill="none"/>',
         '<path d="M40,370 L40,150 Q40,30 200,30 Q360,30 360,150 L360,370 Z" fill="#9a4a1c" stroke="#2a1712" stroke-width="10"/>',
         '<path d="M70,345 L70,160 Q70,62 200,62 Q330,62 330,160 L330,345 Z" fill="#e8a454"/>',
         '<path d="M110,300 Q160,250 240,280 Q290,300 300,240" fill="none" stroke="#c97a30" stroke-width="10" stroke-linecap="round"/>',
         '<rect x="150" y="120" width="90" height="60" rx="10" fill="#f6dc8a" opacity="0.8"/>']
    return svg(W, H, ''.join(o)), W, H

# ----------------------------------------------------------------------------- steam (24-frame loop, 0.4 x 0.8 D)
def steam(k, n=24, W=200, H=400):
    o = []
    for w in range(3):
        ph = 2 * math.pi * (k / n + w / 3.0); x0 = 70 + w * 30; pts = []
        for i in range(30):
            t = i / 29.0; y = H - 10 - t * (H - 40)
            x = x0 + 22 * math.sin(ph * 1 + t * 7.5 + w) * (0.3 + t)
            pts.append((x, y))
        d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        fade = 0.5 + 0.5 * math.sin(2 * math.pi * k / n + w * 2.1)
        o.append(f'<path d="{d}" fill="none" stroke="#f6f0ea" stroke-width="{11 - 2 * w}" stroke-linecap="round" opacity="{0.30 + 0.25 * fade:.2f}" '
                 f'stroke-dasharray="{60 + 20 * w} {30 + 10 * w}" stroke-dashoffset="{-k * (360 / n) * 0.6 - 40 * w:.1f}"/>')
    defs = '<filter id="b"><feGaussianBlur stdDeviation="2.2"/></filter>'
    return svg(W, H, f'<g filter="url(#b)">{"".join(o)}</g>', defs), W, H

# ----------------------------------------------------------------------------- the window views
def _rain(r, W, H, k, n, count, col, op, ang=0.18, L=(30, 70), speed=1.0):
    o = []
    for i in range(count):
        x0 = r.uniform(-200, W); y0 = r.uniform(0, H); l = r.uniform(*L)
        y = (y0 + speed * H * (k / n)) % (H + 100) - 50; x = x0 + y * ang
        o.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x + l * ang:.1f}" y2="{y + l:.1f}" stroke="{col}" stroke-width="2.2" opacity="{op}"/>')
    return ''.join(o)

def _panes_drops(r, k, n, count, tone, run=1.0):
    """Drops running down the glass: a bead with a thin trail, looping inside the glass opening."""
    o = []; (ax, ay) = ext_px(WIN['x0'], WIN['z1']); (bx, by) = ext_px(WIN['x1'], WIN['z0'])
    for i in range(count):
        x = r.uniform(ax, bx); y0 = r.uniform(ay, by); sp = r.uniform(0.4, 1.0) * run
        y = ay + ((y0 - ay) + sp * (by - ay) * k / n) % (by - ay); tl = r.uniform(20, 70)
        o.append(f'<line x1="{x:.1f}" y1="{y - tl:.1f}" x2="{x:.1f}" y2="{y:.1f}" stroke="{tone}" stroke-width="2.5" opacity="0.45"/>')
        o.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="4.5" ry="6" fill="{tone}" opacity="0.8"/><ellipse cx="{x - 1.5:.1f}" cy="{y - 2:.1f}" rx="1.6" ry="2" fill="#ffffff" opacity="0.8"/>')
    return ''.join(o)

def drizzle(k, n=24):
    """Grey drizzle morning outside the four panes: flat grey sky, grey sea, a low dune with a fence, rain, drops on the glass."""
    W, H = ext_size(); hx, hz = ext_px(0, 2.42)            # horizon at z 2.42 on the card
    defs = ('<linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8f97a8"/><stop offset="1" stop-color="#b9bcc4"/></linearGradient>'
            '<linearGradient id="se" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6c7b8f"/><stop offset="1" stop-color="#55667c"/></linearGradient>')
    o = [f'<rect width="{W}" height="{H}" fill="url(#sk)"/>']
    r = random.Random(21)
    for i in range(7):                                      # low flat cloud bands
        y = r.uniform(80, hz - 60); x = r.uniform(-100, W)
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(160, 320):.0f}" ry="{r.uniform(14, 26):.0f}" fill="#a3a8b4" opacity="0.7"/>')
    o.append(f'<rect x="0" y="{hz:.0f}" width="{W}" height="{H - hz:.0f}" fill="url(#se)"/>')
    o.append(f'<line x1="0" y1="{hz:.0f}" x2="{W}" y2="{hz:.0f}" stroke="#4a5568" stroke-width="3"/>')
    o.append(f'<path d="M{W * 0.62:.0f},{hz:.0f} q 60,-26 140,-18 q 70,8 120,18 Z" fill="#5d6574"/>')        # far headland
    for i in range(16):                                    # slow swell lines, drifting
        y = hz + 14 + i * 22 + (i % 3) * 4; x = (r.uniform(0, W) + k * 1.5) % W
        o.append(f'<path d="M{x:.0f},{y:.0f} q 25,-6 50,0" fill="none" stroke="#8a97a8" stroke-width="3" opacity="0.6"/>')
    dz = ext_px(0, 2.10)[1]                                 # wet dune and a rope fence in the foreground
    o.append(f'<path d="M0,{dz:.0f} Q {W * 0.3:.0f},{dz - 40:.0f} {W * 0.55:.0f},{dz - 10:.0f} T {W},{dz - 30:.0f} L {W},{H} L 0,{H} Z" fill="#8c7a63" stroke="#2a1712" stroke-width="5"/>')
    for i in range(30):
        x = r.uniform(0, W); y = dz - 10 + r.uniform(-20, 30)
        o.append(f'<path d="M{x:.0f},{y + 20:.0f} l -6,-28 M{x:.0f},{y + 20:.0f} l 2,-34 M{x:.0f},{y + 20:.0f} l 9,-26" stroke="#6b6a4a" stroke-width="3" fill="none"/>')
    for i in range(6):
        x = 140 + i * 210; y = dz - 50 + 10 * math.sin(i)
        o.append(f'<rect x="{x}" y="{y:.0f}" width="12" height="80" fill="#5a4636" stroke="#2a1712" stroke-width="3"/>')
        if i < 5: o.append(f'<path d="M{x + 6},{y + 12:.0f} q 105,30 210,{10 * (math.sin(i + 1) - math.sin(i)):.0f}" fill="none" stroke="#3a3028" stroke-width="3"/>')
    o.append(_rain(random.Random(5), W, H, k, n, 160, '#e6e9ef', 0.45, ang=0.12, L=(40, 90), speed=2.0))
    o.append(_panes_drops(random.Random(9), k, n, 26, '#c9d2de', run=1.0))
    return svg(W, H, ''.join(o), defs), W, H

def _crest(r, W, top, k, amp):
    pts = []
    for i in range(0, W + 40, 40):
        pts.append((i, top + amp * math.sin(i * 0.011 + k * 0.21) + r.uniform(-10, 10)))
    return pts

def wave(k, n=WAVE_N):
    """Film frame g = WAVE_G0 + k. The wall of water fills the panes: it heaves and rises, its crest of foam boils above it,
    spray drifts across, rivulets sheet down the glass; lightning (LIGHTNING) whites the sky and lights the wall."""
    W, H = ext_size(); g = WAVE_G0 + k; L = LIGHTNING.get(g, 0.0); t = k / (n - 1.0)
    sky0 = _mixc('#1c2033', '#e9e6ff', L); sky1 = _mixc('#2b3048', '#bfc2e8', L)
    w0 = _mixc('#13222e', '#5a7d92', L * 0.8); w1 = _mixc('#24414f', '#7fa3b4', L * 0.8); w2 = _mixc('#0b151d', '#344c5a', L * 0.8)
    defs = (f'<linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sky0}"/><stop offset="1" stop-color="{sky1}"/></linearGradient>'
            f'<linearGradient id="wv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{w1}"/><stop offset="0.45" stop-color="{w0}"/><stop offset="1" stop-color="{w2}"/></linearGradient>'
            '<filter id="bl"><feGaussianBlur stdDeviation="3"/></filter>')
    o = [f'<rect width="{W}" height="{H}" fill="url(#sk)"/>']
    r = random.Random(100 + k)
    for i in range(5):                                      # torn storm clouds
        x = (r.uniform(0, W) + k * 9) % (W + 300) - 150; y = r.uniform(30, 200)
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(150, 280):.0f}" ry="{r.uniform(30, 55):.0f}" fill="{_mixc("#141726", "#d0cff0", L * 0.6)}" opacity="0.75"/>')
    if L > 0.5:                                             # the bolt
        x = 260 + (g % 7) * 70; y = 0; d = f'M{x},{y}'
        rr = random.Random(g)
        while y < 330:
            x += rr.uniform(-40, 40); y += rr.uniform(30, 60); d += f' L{x:.0f},{y:.0f}'
        o.append(f'<path d="{d}" fill="none" stroke="#ffffff" stroke-width="7" opacity="{L:.2f}"/><path d="{d}" fill="none" stroke="#c9c2ff" stroke-width="18" opacity="{0.35 * L:.2f}" filter="url(#bl)"/>')
    # the wall: a towering face whose curling lip starts in the upper panes and climbs out of the top of the window;
    # the face is streaked vertically (water drawn up the wall), darkest at the bottom; foam boils along the lip
    top_z = 2.95 + 0.50 * (lambda q: q * q * (3 - 2 * q))(min(1.0, k / 30.0)) + 0.03 * math.sin(k * 0.35)
    top = ext_px(0, top_z)[1]
    crest = _crest(r, W, top, k, 14)
    d = f'M0,{H} L' + ' L'.join(f'{x:.0f},{y:.0f}' for x, y in crest) + f' L{W},{H} Z'
    o.append(f'<path d="{d}" fill="url(#wv)" stroke="#0a0f14" stroke-width="6"/>')
    lip = _mixc('#2c5566', '#a9cddb', L)                      # the curl: a darker overhang band just under the crest
    d2 = 'M0,%.0f ' % (top + 70) + ' '.join('L%.0f,%.0f' % (x, y + 55 + 18 * math.sin(x * 0.02 + k * 0.3)) for x, y in crest) + f' L{W},{top - 10:.0f} L0,{top - 10:.0f} Z'
    o.append(f'<path d="{d2}" fill="{lip}" opacity="0.55"/>')
    for i in range(26):                                     # vertical streaks running up the face
        x = (i * 97 + k * 6) % W; y0 = top + 60 + (i * 37) % 120
        o.append(f'<path d="M{x:.0f},{H:.0f} Q {x + 30:.0f},{(H + y0) / 2:.0f} {x + 8:.0f},{y0:.0f}" fill="none" stroke="{_mixc("#365d6d", "#c4dde6", L)}" stroke-width="{4 + i % 5}" opacity="0.45"/>')
    for i in range(110):                                    # foam on the crest, boiling
        x, y = crest[r.randrange(len(crest))]; x += r.uniform(-20, 20); y += r.uniform(-40, 25)
        rr_ = r.uniform(10, 30); o.append(f'<ellipse cx="{x:.0f}" cy="{y + rr_ * 0.25:.0f}" rx="{rr_ * 1.6:.0f}" ry="{rr_ * 0.8:.0f}" fill="{_mixc("#8fa6b0", "#dfe8ff", L)}" opacity="0.9"/>'
                                     f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rr_ * 1.4:.0f}" ry="{rr_ * 0.7:.0f}" fill="{_mixc("#d7e0e3", "#ffffff", L)}" opacity="{r.uniform(0.75, 0.98):.2f}"/>')
    for i in range(40):                                     # spume torn off the lip, flying up and left
        x = (r.uniform(0, W) - k * 18) % W; y = top - r.uniform(20, 160)
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(10, 30):.0f}" ry="{r.uniform(3, 8):.0f}" fill="#dfe8ec" opacity="{r.uniform(0.3, 0.7):.2f}"/>')
    for i in range(90):                                     # spray flung across the window, drifting left and up
        x = (r.uniform(0, W) - k * 14) % W; y = r.uniform(top - 120, H)
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1.5, 5):.1f}" fill="#dfe8ec" opacity="{r.uniform(0.3, 0.8):.2f}"/>')
    o.append(_rain(random.Random(7), W, H, k, 12, 140, '#cfd8e6', 0.5, ang=-0.45, L=(60, 120), speed=3.0))
    o.append(_panes_drops(random.Random(17), k, 18, 60, _mixc('#9fb2c2', '#ffffff', L), run=1.6))
    (ax, ay) = ext_px(WIN['x0'], WIN['z1']); (bx, by) = ext_px(WIN['x1'], WIN['z0'])    # water sheeting down the glass
    rr = random.Random(3)
    for i in range(16):
        x = rr.uniform(ax, bx); w = rr.uniform(10, 30); ph = (k * rr.uniform(6, 14)) % 80
        o.append(f'<path d="M{x:.0f},{ay:.0f} q {w:.0f},{(by - ay) * 0.3:.0f} 0,{(by - ay) * 0.55:.0f} t 0,{(by - ay) * 0.45:.0f}" fill="none" '
                 f'stroke="#a9bccb" stroke-width="{rr.uniform(3, 7):.1f}" stroke-dasharray="40 {20 + ph:.0f}" opacity="0.5"/>')
    return svg(W, H, ''.join(o), defs), W, H

def crack(k, W=400, H=400):
    """Crack in one pane (0.8 x 0.8 D card), growing over frames 0..3 from the impact point at the lower left."""
    rr = random.Random(77); o = []; grow = min(1.0, (k + 1) / 4.0); cx, cy = 140, 260
    for a in range(7):
        ang = a * 2 * math.pi / 7 + rr.uniform(-0.3, 0.3); L = rr.uniform(120, 260) * grow; d = f'M{cx},{cy}'; x, y = cx, cy
        for s in range(5):
            x += math.cos(ang) * L / 5 + rr.uniform(-8, 8); y += math.sin(ang) * L / 5 + rr.uniform(-8, 8); d += f' L{x:.0f},{y:.0f}'
        o.append(f'<path d="{d}" fill="none" stroke="#f4f7ff" stroke-width="3.2" opacity="0.95"/><path d="{d}" fill="none" stroke="#1a2230" stroke-width="1.4" opacity="0.8" transform="translate(2,2)"/>')
    if grow >= 0.5:
        for rad in (34, 62):
            o.append(f'<circle cx="{cx}" cy="{cy}" r="{rad * grow:.0f}" fill="none" stroke="#f4f7ff" stroke-width="2.4" stroke-dasharray="18 10" opacity="0.85"/>')
    return svg(W, H, ''.join(o)), W, H

def _mixc(a, b, t):
    a = [int(a[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(b[i:i + 2], 16) for i in (1, 3, 5)]; t = max(0.0, min(1.0, t))
    return '#%02x%02x%02x' % tuple(int(round(x + (y - x) * t)) for x, y in zip(a, b))

# ----------------------------------------------------------------------------- build
STATIC = dict(oilcloth=(oilcloth, False), kwall=(kwall, False), curtain=(curtain, False), toast=(toast, True))
SEQ = dict(steam=(steam, 24, True), drizzle=(drizzle, 24, False), wave=(wave, WAVE_N, False), crack=(crack, 6, True))

def ensure(verbose=False, only=None):
    os.makedirs(TEX, exist_ok=True); os.makedirs(TMP, exist_ok=True)
    mpath = os.path.join(TEX, 'manifest.json'); man = json.load(open(mpath)) if os.path.exists(mpath) else {}
    todo = []; out = {}
    def add(key, fn_out, png, transparent):
        s, W, H = fn_out; h = hashlib.sha1((s + str(transparent)).encode()).hexdigest()
        if man.get(key) != h or not os.path.exists(png):
            sp = os.path.join(TMP, key.replace('/', '_') + '.svg'); open(sp, 'w').write(s)
            todo.append(dict(src=sp, out=png, w=W, h=H, transparent=transparent)); man[key] = h
    for name, (fn, tr) in STATIC.items():
        if only and name not in only: continue
        png = os.path.join(TEX, name + '.png'); out[name] = png; add(name, fn(), png, tr)
    for name, (fn, n, tr) in SEQ.items():
        if only and name not in only: continue
        d = os.path.join(TEX, name); os.makedirs(d, exist_ok=True); out[name] = []
        for k in range(n):
            png = os.path.join(d, 'f_%03d.png' % k); out[name].append(png); add('%s/%03d' % (name, k), fn(k), png, tr)
    if todo:
        jp = os.path.join(TMP, 'jobs.json'); json.dump(todo, open(jp, 'w'))
        r = subprocess.run(['node', RASTER, jp], capture_output=True, text=True, env=dict(os.environ, NODE_PATH=os.environ.get('NODE_PATH', '/opt/node22/lib/node_modules')))
        if r.returncode != 0: raise RuntimeError('raster failed: ' + r.stderr[-2000:])
        json.dump(man, open(mpath, 'w'), indent=0)
        if verbose: print('rasterised %d textures' % len(todo))
    return out

if __name__ == '__main__':
    import time; t = time.time(); o = ensure(verbose=True); print('%.1f s' % (time.time() - t)); print({k: (v if isinstance(v, str) else len(v)) for k, v in o.items()})

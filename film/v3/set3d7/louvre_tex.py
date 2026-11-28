#!/usr/bin/env python3
"""louvre_tex.py : artwork of the film-7 sets (Paris, August 1911: the Louvre's Salon Carre, its closet / service stair / exit door,
the street outside, Vincenzo's attic room and the Florence dealer's shop), drawn as SVG in Python and rasterised by headless Chromium
(PROJ/v3/set3d/raster.js, one launch for all changed textures). Cached in v3/set3d7/tex_louvre/ by content hash. Same route as
v3/set3d6/bakery_tex.py (whose generic surfaces - plaster, planks, cobbles, crate, shaft - are reused by calling them with new names).

    import louvre_tex as LT
    paths = LT.ensure()        # {name: png path}
    LT.SIZE[name] -> (w_D, h_D);  LT.ATLAS -> painting atlas cells

The Mona Lisa ('mona') is a simplified flat cartoon painting of the public-domain portrait (Leonardo, c. 1503-19): the sitter turned
three-quarters, dark hair and veil, the smile, folded hands, ochre sleeves, the hazy blue-green mountain landscape with the winding
road (left) and the bridge (right). mona_svg() is reused small on the newspapers and posters.
Deterministic: every random choice comes from random.Random(fixed seed)."""
import os, sys, json, math, random, hashlib, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (os.path.join(PROJ, 'v3', 'set3d2'), os.path.join(PROJ, 'v3', 'set3d4'), os.path.join(PROJ, 'v3', 'set3d6')):
    if p not in sys.path: sys.path.insert(0, p)
import tower_tex as TT                                                     # noqa: E402
from tower_tex import rect, poly, pline, line, circ, ell, path, mul, mix, _wrap, _c   # noqa: E402,F401
import pagoda_tex as PT                                                    # noqa: E402
import bakery_tex as BT                                                    # noqa: E402

TEX = os.path.join(HERE, 'tex_louvre'); WORK = os.path.join(HERE, 'louvre_work')
RASTER = TT.RASTER; SIZE = TT.SIZE; job = TT.job
INK = '#24160e'

def _txt(x, y, s, size, fill, font='DejaVu Serif, Georgia, serif', weight=700, anchor='middle', extra=''):
    return (f'<text x="{_c(x)}" y="{_c(y)}" font-family="{font}" font-weight="{weight}" font-size="{_c(size)}" '
            f'text-anchor="{anchor}" fill="{fill}"{extra}>{s}</text>')

def _g(body, tx=0.0, ty=0.0, s=1.0, extra=''):
    return f'<g transform="translate({_c(tx)} {_c(ty)}) scale({s:.5f})"{extra}>{body}</g>'

# ============================================================================= the Mona Lisa
def mona_svg(uid='m'):
    """The painting in a 100 x 145 box (SVG units), flat cartoon style with ink lines. uid keeps gradient ids unique when embedded."""
    u = uid; o = []
    d = (f'<linearGradient id="{u}sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fa088"/><stop offset="0.5" stop-color="#b8bc8e"/>'
         f'<stop offset="1" stop-color="#c8b880"/></linearGradient>'
         f'<radialGradient id="{u}vig" cx="0.5" cy="0.45" r="0.75"><stop offset="0.55" stop-color="#1a1008" stop-opacity="0"/><stop offset="1" stop-color="#1a1008" stop-opacity="0.55"/></radialGradient>'
         f'<linearGradient id="{u}face" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f0cc8c"/><stop offset="0.6" stop-color="#e6bc7c"/><stop offset="1" stop-color="#c0904e"/></linearGradient>'
         f'<linearGradient id="{u}sl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b88a3a"/><stop offset="1" stop-color="#8a6024"/></linearGradient>')
    o.append(rect(0, 0, 100, 145, f'url(#{u}sky)'))
    # far mountains: hazy blue-green crags, left lower than right (the famous mismatched horizon)
    o.append(path('M0,58 L6,44 L11,50 L17,36 L23,46 L28,40 L33,52 L34,70 L0,70 Z', '#7e9a8c', stroke='#5a7266', sw=0.4))
    o.append(path('M66,48 L71,34 L76,42 L82,28 L88,38 L93,30 L100,40 L100,72 L66,72 Z', '#7a9888', stroke='#5a7266', sw=0.4))
    o.append(path('M0,62 Q8,56 16,60 Q24,64 33,60 L34,74 L0,74 Z', '#9ab4a4', op=0.85))
    o.append(path('M66,54 Q76,50 86,55 Q94,58 100,54 L100,74 L66,74 Z', '#9ab4a4', op=0.85))
    o.append(ell(14, 63, 10, 2.2, '#c8d4c0', op=0.9)); o.append(ell(86, 57, 9, 2.0, '#c8d4c0', op=0.9))            # lakes
    # nearer brown-green land
    o.append(path('M0,74 Q10,68 20,72 Q28,75 34,72 L34,100 L0,100 Z', '#7a6a3a', stroke='#4a3e20', sw=0.3))
    o.append(path('M66,74 Q78,70 88,73 Q95,75 100,72 L100,100 L66,100 Z', '#7a6c3c', stroke='#4a3e20', sw=0.3))
    o.append(path('M3,96 C8,88 22,90 14,82 C8,77 20,75 26,74', 'none', stroke='#c8a462', sw=1.6))                   # the winding road
    o.append(path('M3,96 C8,88 22,90 14,82 C8,77 20,75 26,74', 'none', stroke='#8a6a34', sw=0.3))
    o.append(path('M70,86 L92,86 L92,88 L70,88 Z', '#8a7448', stroke='#4a3e20', sw=0.3))                            # the bridge
    for k in range(4): o.append(path(f'M{_c(71 + k * 5.2)},{_c(91)} q2.2,-4.5 4.4,0 Z', '#3e3420'))
    o.append(path('M70,88 L92,88 L92,91 L70,91 Z', '#8a7448', op=0.6))
    o.append(path('M66,93 Q80,91 100,94 L100,100 L66,100 Z', '#a8b8a0', op=0.8))                                    # river under it
    o.append(rect(0, 96, 100, 49, '#2a2216'))                                                                    # loggia (dark) behind her
    o.append(rect(0, 95, 100, 2.4, '#5a4a2a'))                                                                   # parapet
    for x in (0, 95): o.append(rect(x, 86, 5, 12, '#4a3a22', stroke=INK, sw=0.3))                                  # column bases
    # hair falling behind the shoulders (drawn first)
    o.append(path('M31,40 C29,22 40,13 50,13 C60,13 71,22 69,40 C69,54 72,64 74,76 C68,76 62,70 59,62 L41,62 C38,70 32,76 26,76 C28,64 31,54 31,40 Z',
                  '#3a2414', stroke=INK, sw=0.6))
    # body: dark dress, shoulders sloping wide
    o.append(path('M6,145 C6,112 12,86 30,76 C38,72 44,70 50,70 C56,70 62,72 70,76 C88,86 94,112 94,145 Z', '#2c2618', stroke=INK, sw=0.6))
    # ochre pleated sleeves
    o.append(path('M6,145 C6,116 11,94 22,84 C30,96 32,122 36,145 Z', f'url(#{u}sl)', stroke=INK, sw=0.5))
    o.append(path('M94,145 C94,118 89,96 78,85 C70,98 68,122 64,145 Z', f'url(#{u}sl)', stroke=INK, sw=0.5))
    for k in range(6):
        o.append(path(f'M{_c(10 + k * 3.4)},{_c(98 + k * 2)} q2,10 1,{_c(36 - k * 4)}', 'none', stroke='#6a4818', sw=0.45))
        o.append(path(f'M{_c(90 - k * 3.4)},{_c(98 + k * 2)} q-2,10 -1,{_c(36 - k * 4)}', 'none', stroke='#6a4818', sw=0.45))
    # neck and the low curved neckline with its embroidered edge
    o.append(path('M44,58 L43.5,70 Q50,73 56.5,70 L56,58 Z', '#ddb274', stroke=INK, sw=0.5))
    o.append(path('M32,78 C38,88 62,88 68,78 C62,73 56,70 50,70 C44,70 38,73 32,78 Z', '#e6bc80', stroke=INK, sw=0.5))
    o.append(path('M44,70 Q50,74 56,70', 'none', stroke='#b88a50', sw=0.5, op=0.7))
    o.append(path('M32,78 C38,88 62,88 68,78', 'none', stroke='#a88a3c', sw=1.5))
    for k in range(15): o.append(circ(33.5 + k * 2.4, 80.2 + 4.6 * math.sin(math.pi * k / 14), 0.45, '#d8bc60'))
    o.append(path('M36,90 Q50,98 64,90', 'none', stroke='#4a4030', sw=0.8, op=0.7))
    o.append(path('M40,96 Q50,103 60,96', 'none', stroke='#4a4030', sw=0.6, op=0.5))
    # the thin dark veil over the hair, falling to the shoulders
    o.append(path('M32,42 C31,58 30,68 26,78', 'none', stroke='#1a120c', sw=0.5, op=0.6))
    o.append(path('M68,42 C69,58 70,68 74,78', 'none', stroke='#1a120c', sw=0.5, op=0.6))
    # face: oval, high forehead, rounded jaw; lit from the left
    o.append(path('M37,39 C37,26 42,20 50,20 C58,20 63,26 63,39 C63,50 58,59 50,60 C42,59 37,50 37,39 Z', f'url(#{u}face)', stroke=INK, sw=0.6))
    o.append(path('M50,20 C47,21.5 43,25 41.5,30', 'none', stroke='#3a2414', sw=1.4))
    o.append(path('M50,20 C53,21.5 57,25 58.5,30', 'none', stroke='#3a2414', sw=1.4))
    o.append(path('M38,28 Q50,23.5 62,28', 'none', stroke='#2a2016', sw=0.4, op=0.55))
    o.append(path('M57.5,24 C62,30 63,42 59.5,51 C57.5,55 55,58 52,59.4 C56.5,50 58.5,37 57.5,24 Z', '#b08048', op=0.4))
    o.append(path('M44,57.5 Q50,62.5 56,57.5 Q50,60.5 44,57.5 Z', '#a87a44', op=0.45))
    # eyes: no eyebrows, heavy lids, brown irises turned to the viewer
    for (ex, w) in ((44.6, 3.6), (55.6, 3.3)):
        o.append(path(f'M{_c(ex - w)},{_c(37.4)} Q{_c(ex)},{_c(35.2)} {_c(ex + w)},{_c(37.4)} Q{_c(ex)},{_c(39.0)} {_c(ex - w)},{_c(37.4)} Z', '#f0dcb8', stroke=INK, sw=0.4))
        o.append(circ(ex + 0.7, 37.3, 1.25, '#4a2c16')); o.append(circ(ex + 0.7, 37.3, 0.55, '#140c08')); o.append(circ(ex + 0.3, 36.8, 0.3, '#fff8e8'))
        o.append(path(f'M{_c(ex - w)},{_c(36.9)} Q{_c(ex)},{_c(34.6)} {_c(ex + w)},{_c(36.9)}', 'none', stroke=INK, sw=0.75))
        o.append(path(f'M{_c(ex - w + 0.5)},{_c(35.0)} Q{_c(ex)},{_c(33.4)} {_c(ex + w - 0.5)},{_c(35.0)}', 'none', stroke='#b88a54', sw=0.4, op=0.6))
    # nose: long straight, shadow on the right
    o.append(path('M50.4,38 Q50.0,44.5 51.6,48.4 Q50.4,49.6 48.6,49.0', 'none', stroke='#8a5a2c', sw=0.5))
    o.append(path('M51,40 Q52.2,45.5 52.8,48.2 Q51.9,49.4 51.3,48.9 Z', '#b88a50', op=0.55))
    # the smile: closed lips, corners lifted into soft shadow
    o.append(path('M46.2,53.0 Q48,53.8 50,53.5 Q52.2,53.8 54.0,52.6', 'none', stroke='#6a3a20', sw=0.6))
    o.append(path('M46.2,53.0 q-0.7,-0.3 -1.1,-1.1', 'none', stroke='#8a5430', sw=0.4, op=0.8))
    o.append(path('M54.0,52.6 q0.7,-0.4 0.9,-1.2', 'none', stroke='#8a5430', sw=0.4, op=0.8))
    o.append(path('M47.2,54.9 Q50,55.9 52.8,54.9', 'none', stroke='#c89a64', sw=0.5, op=0.8))
    o.append(ell(42.0, 46.0, 3.0, 2.0, '#e8a87a', op=0.22)); o.append(ell(58.0, 46.0, 2.4, 1.8, '#d89a6a', op=0.18))
    # hands: the left hand resting on the chair arm (viewer's right), the right hand laid over the left wrist, fingers to the right
    o.append(rect(70, 130, 30, 3.2, '#4a3820', stroke=INK, sw=0.4))
    o.append(path('M58,126 C64,124 72,124 79,126 C83,127 84,131 80,132.5 C73,133.5 64,133 58,132 Z', '#e8c08a', stroke=INK, sw=0.5))
    for k in range(3): o.append(path(f'M{_c(72 + k * 3)},{_c(126.3)} q0.6,3.5 0.2,6.6', 'none', stroke='#a87a44', sw=0.35))
    o.append(path('M24,121 C30,116 42,116 52,118.5 C60,120 67,121.5 74,123 C78,124 78.5,127.6 75,128 L64,128.6 C56,129 46,128.5 38,127.8 C31,127 25,125 24,121 Z', '#ecc690', stroke=INK, sw=0.5))
    for k in range(4): o.append(path(f'M{_c(62 + k * 3)},{_c(121.6 + k * 0.4)} q2.4,0.8 4.8,2.0', 'none', stroke='#a87a44', sw=0.35))
    o.append(path('M24,121 C26,117 30,115 34,116', 'none', stroke='#6a4818', sw=1.4))
    o.append(path('M76,125 C80,121 86,121 90,124', 'none', stroke='#6a4818', sw=1.4))
    # the sfumato veil of old varnish, a craquelure and a dark vignette
    o.append(rect(0, 0, 100, 145, '#a08a40', op=0.1))
    r = random.Random(7)
    for _ in range(40):
        x, y = r.uniform(0, 100), r.uniform(0, 145); o.append(pline([(x, y), (x + r.uniform(-3, 3), y + r.uniform(1, 4)), (x + r.uniform(-4, 4), y + r.uniform(3, 7))], '#3a2a14', 0.15, op=0.12))
    o.append(rect(0, 0, 100, 145, f'url(#{u}vig)'))
    return ''.join(o), d

def mona(name='mona', W=1.0, H=1.45, ppd=600):
    body, d = mona_svg('m')
    job(name, 0, 0, W, H, ppd, _g(body, 0, 0, W / 100.0), defs=d)

# ============================================================================= salon paintings (atlas of 4 x 4 cells, 1 x 1 D each)
ATLAS = {}                       # atlas name -> list of (kind, seed) per cell (row-major, cell 0 at top-left)
KINDS = ('landscape', 'portrait', 'madonna', 'sea', 'still', 'battle', 'ruins', 'portrait2', 'feast', 'landscape2', 'saint', 'genre')

def _painting(kind, r, u):
    """One painting in a 100 x 100 box."""
    o = []; d = ''
    def sky(c0, c1, h=100):
        nonlocal d
        d += f'<linearGradient id="{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c0}"/><stop offset="1" stop-color="{c1}"/></linearGradient>'
        o.append(rect(0, 0, 100, h, f'url(#{u})'))
    def tree(x, y, s, c):
        o.append(rect(x - s * 0.08, y - s * 0.6, s * 0.16, s * 0.6, '#3a2a1a'))
        for k in range(4): o.append(circ(x + r.uniform(-s * 0.3, s * 0.3), y - s * (0.7 + 0.25 * k), s * r.uniform(0.28, 0.4), mul(c, r.uniform(0.8, 1.15)), stroke=INK, sw=0.3))
    def figure(x, y, s, robe, head='#e8c090', halo=False, hat=None):
        o.append(path(f'M{_c(x - s * 0.35)},{_c(y)} L{_c(x - s * 0.2)},{_c(y - s * 0.75)} L{_c(x + s * 0.2)},{_c(y - s * 0.75)} L{_c(x + s * 0.35)},{_c(y)} Z', robe, stroke=INK, sw=0.4))
        if halo: o.append(circ(x, y - s * 0.88, s * 0.2, '#f0c850', stroke='#a8802a', sw=0.3))
        o.append(circ(x, y - s * 0.86, s * 0.12, head, stroke=INK, sw=0.35))
        if hat: o.append(ell(x, y - s * 0.96, s * 0.15, s * 0.06, hat))
    if kind in ('landscape', 'landscape2'):
        sunset = kind == 'landscape2'
        sky(*(('#e8a860', '#f8e4b0') if sunset else ('#6a90c0', '#e8e0c4')), 70)
        for k in range(3): o.append(ell(r.uniform(10, 90), r.uniform(10, 35), r.uniform(10, 18), r.uniform(4, 7), '#fff4e0' if not sunset else '#f8c890', op=0.8))
        o.append(path(f'M0,62 Q25,{_c(r.uniform(44, 52))} 50,58 T100,{_c(r.uniform(48, 58))} L100,100 L0,100 Z', '#8aa0a8' if not sunset else '#a88a80'))
        o.append(path(f'M0,72 Q30,{_c(r.uniform(60, 66))} 60,70 T100,66 L100,100 L0,100 Z', '#6a7a3a', stroke=INK, sw=0.3))
        o.append(path('M0,84 Q40,76 100,86 L100,100 L0,100 Z', '#4a5a28'))
        o.append(path(f'M{_c(r.uniform(30, 60))},100 Q55,82 70,74', 'none', stroke='#a8c0c8', sw=3.0))
        for _ in range(r.randint(3, 6)): tree(r.uniform(5, 95), r.uniform(76, 92), r.uniform(14, 26), '#3e5a2a')
        figure(r.uniform(30, 70), 92, 10, r.choice(('#a83a2a', '#2a4a8a')))
    elif kind in ('portrait', 'portrait2'):
        bg = r.choice(('#2a2418', '#1e2a24', '#3a2a1e')); o.append(rect(0, 0, 100, 100, bg))
        if kind == 'portrait2': o.append(rect(62, 0, 38, 60, '#4a5a6a')); o.append(rect(64, 4, 34, 50, '#8aa0b0'))
        robe = r.choice(('#1a1a1e', '#8a2a20', '#2a3a6a', '#4a2a3a'))
        o.append(path('M14,100 C16,78 30,70 50,68 C70,70 84,78 86,100 Z', robe, stroke=INK, sw=0.5))
        o.append(path('M38,70 Q50,80 62,70 Q50,74 38,70 Z', '#f0ece0', stroke=INK, sw=0.4))
        o.append(rect(44, 56, 12, 14, '#d8a878', stroke=INK, sw=0.4))
        o.append(ell(50, 44, 15, 19, '#e4b884', stroke=INK, sw=0.5))
        o.append(ell(44, 42, 2.2, 1.4, '#2a1a10')); o.append(ell(56, 42, 2.2, 1.4, '#2a1a10'))
        o.append(path('M50,44 q1,6 -1,8', 'none', stroke='#8a5a30', sw=0.6)); o.append(path('M45,55 q5,2 10,0', 'none', stroke='#7a3a20', sw=0.7))
        hair = r.choice(('#2a1a10', '#6a4a2a', '#c8c0b0'))
        o.append(path('M35,40 C34,22 66,22 65,40 C62,30 38,30 35,40 Z', hair))
        if r.random() < 0.6: o.append(path('M32,30 Q50,14 68,30 L66,24 Q50,10 34,24 Z', r.choice(('#1a1a1a', '#8a2a20', '#2a2a4a'))))
        if r.random() < 0.5: o.append(path('M42,54 Q50,64 58,54 Q50,72 42,54 Z', hair))
    elif kind in ('madonna', 'saint'):
        sky('#c8a040', '#f0d890') if kind == 'madonna' else sky('#4a6a9a', '#d8c8a0')
        if kind == 'madonna':
            o.append(rect(0, 70, 100, 30, '#6a5a3a'))
            o.append(path('M22,100 C22,70 36,48 50,46 C64,48 78,70 78,100 Z', '#2a4a9a', stroke=INK, sw=0.6))
            o.append(path('M36,100 C38,76 44,60 50,58 C56,60 62,76 64,100 Z', '#b02a22', stroke=INK, sw=0.4))
            o.append(circ(50, 34, 13, '#f0c850', stroke='#a8802a', sw=0.5)); o.append(ell(50, 36, 8, 10, '#ecc89a', stroke=INK, sw=0.5))
            o.append(path('M40,36 C40,22 60,22 60,36 L62,52 L38,52 Z', '#2a4a9a', op=0.9))
            o.append(ell(50, 36, 7, 9, '#ecc89a', stroke=INK, sw=0.4)); o.append(path('M46,42 q4,2 8,0', 'none', stroke='#8a4a30', sw=0.5))
            o.append(circ(44, 66, 7, '#f0c850', op=0.8)); o.append(circ(44, 68, 5.5, '#f4d0a8', stroke=INK, sw=0.4)); o.append(ell(46, 80, 8, 7, '#f4d0a8', stroke=INK, sw=0.4))
        else:
            o.append(path('M0,80 Q50,70 100,82 L100,100 L0,100 Z', '#5a5a32'))
            for x in (30, 52, 72):
                figure(x, 92, r.uniform(36, 46), r.choice(('#a83a2a', '#2a4a8a', '#c8a040', '#3a6a3a')), halo=True)
            for k in range(5): o.append(line(50, 0, r.uniform(0, 100), 30, '#fff4c8', 1.2, op=0.4))
    elif kind == 'sea':
        sky('#7898b8', '#e8dcc0', 60)
        o.append(rect(0, 58, 100, 42, '#3a6a7a'))
        for k in range(14): y = 62 + k * 2.8; o.append(path(f'M{_c(r.uniform(-10, 20))},{_c(y)} q10,-2 20,0 t20,0 t20,0 t20,0 t20,0', 'none', stroke='#a8c8c8', sw=0.6, op=0.7))
        x = r.uniform(30, 60); o.append(path(f'M{_c(x - 14)},64 L{_c(x + 16)},64 L{_c(x + 11)},72 L{_c(x - 10)},72 Z', '#4a3020', stroke=INK, sw=0.5))
        for k, (dx, h) in enumerate(((-6, 30), (4, 38), (12, 24))):
            o.append(line(x + dx, 64, x + dx, 64 - h, '#2a1a10', 0.8)); o.append(path(f'M{_c(x + dx - 6)},{_c(64 - h + 4)} Q{_c(x + dx)},{_c(64 - h * 0.6)} {_c(x + dx - 5)},{_c(62)} L{_c(x + dx + 6)},{_c(62)} Q{_c(x + dx + 4)},{_c(64 - h * 0.6)} {_c(x + dx + 6)},{_c(64 - h + 4)} Z', '#f0e8d4', stroke=INK, sw=0.4))
        o.append(path('M0,58 L14,46 L22,58 Z', '#6a7a6a'))
    elif kind == 'still':
        o.append(rect(0, 0, 100, 100, '#2a2014')); o.append(rect(0, 64, 100, 36, '#6a4a2a', stroke=INK, sw=0.4)); o.append(rect(0, 64, 100, 4, '#8a6a3a'))
        o.append(path('M20,64 Q22,50 40,50 Q58,50 60,64 Z', '#c8c0b0', stroke=INK, sw=0.5))
        for (x, y, c) in ((30, 50, '#c83a2a'), (38, 46, '#e8a030'), (46, 49, '#7aa040'), (52, 46, '#6a2a5a'), (42, 41, '#e8c040')): o.append(circ(x, y, 5, c, stroke=INK, sw=0.4))
        o.append(path('M70,64 L68,40 Q74,34 80,40 L78,64 Z', '#4a6a8a', stroke=INK, sw=0.5))
        for k in range(7): o.append(circ(74 + r.uniform(-10, 10), 28 + r.uniform(-12, 8), r.uniform(3, 5), r.choice(('#e8e0d0', '#d83a3a', '#f0c040', '#e88aa0')), stroke=INK, sw=0.3))
        o.append(path('M8,80 L36,76 L40,90 L10,94 Z', '#f0ece0', op=0.9))
    elif kind == 'battle':
        sky('#8a6a4a', '#d8b888', 70); o.append(rect(0, 70, 100, 30, '#5a4a2a'))
        for k in range(6): o.append(circ(r.uniform(0, 100), r.uniform(30, 66), r.uniform(8, 16), '#e8dcc8', op=0.45))
        for k in range(5):
            x = 12 + k * 18 + r.uniform(-4, 4); y = 86 + r.uniform(-4, 6); c = r.choice(('#3a2a1a', '#6a4a2a', '#e8e0d0'))
            o.append(ell(x, y - 8, 9, 5, c, stroke=INK, sw=0.4)); o.append(path(f'M{_c(x + 7)},{_c(y - 10)} l5,-6 l2,4 Z', c, stroke=INK, sw=0.3))
            for dx in (-6, -2, 3, 7): o.append(line(x + dx, y - 5, x + dx + r.uniform(-2, 2), y + 3, c, 1.2))
            figure(x, y - 11, 12, r.choice(('#2a4a9a', '#b02a22', '#e8e0d0')), hat='#1a1a1a')
        o.append(line(70, 70, 76, 30, '#3a2a1a', 0.8)); o.append(path('M76,30 l12,3 l-12,4 Z', '#b02a22'))
    elif kind == 'ruins':
        sky('#e8b070', '#f8ecc8', 75); o.append(rect(0, 75, 100, 25, '#8a7a4a'))
        for x in (12, 28, 44, 70):
            h = r.uniform(30, 60); o.append(rect(x, 80 - h, 8, h, '#d8c8a8', stroke=INK, sw=0.4)); o.append(rect(x - 2, 80 - h - 3, 12, 3, '#c8b898', stroke=INK, sw=0.3))
            for k in range(3): o.append(line(x + 2 + k * 2, 80 - h, x + 2 + k * 2, 80, '#a89878', 0.4))
        o.append(rect(10, 26, 46, 6, '#c8b898', stroke=INK, sw=0.4)); o.append(path('M62,80 Q70,50 78,80 Z', '#5a6a3a'))
        figure(55, 90, 12, '#a83a2a'); figure(62, 92, 11, '#e8e0d0')
    elif kind == 'feast':
        o.append(rect(0, 0, 100, 100, '#c8b090')); o.append(rect(0, 0, 100, 40, '#7898b8'))
        for x in (6, 30, 54, 78): o.append(rect(x, 4, 8, 50, '#e8dcc0', stroke=INK, sw=0.4))
        o.append(rect(0, 54, 100, 6, '#e8e0d0')); o.append(rect(4, 60, 92, 16, '#f0ece0', stroke=INK, sw=0.4))
        for k in range(9): figure(8 + k * 10.5, 62, r.uniform(16, 20), r.choice(('#a83a2a', '#2a4a8a', '#c8a040', '#3a6a3a', '#6a2a5a', '#e8e0d0')))
        for k in range(5): figure(14 + k * 18, 98, 24, r.choice(('#b02a22', '#2a4a9a', '#c89030')))
    else:   # genre interior
        o.append(rect(0, 0, 100, 100, '#5a4a32')); o.append(rect(0, 74, 100, 26, '#7a5a3a'))
        for k in range(6): o.append(rect(k * 18 - (k % 2) * 9, 74 + (k % 2) * 6, 18, 6, '#e8dcc0', op=0.4))
        o.append(rect(10, 16, 24, 34, '#e8e4cc', stroke=INK, sw=0.5)); o.append(line(22, 16, 22, 50, INK, 0.6)); o.append(line(10, 33, 34, 33, INK, 0.6))
        o.append(path('M10,50 L34,50 L90,96 L40,96 Z', '#fff0c0', op=0.25))
        figure(60, 88, 44, r.choice(('#2a4a9a', '#e8c040', '#a83a2a')))
        o.append(rect(30, 64, 18, 4, '#8a6a3a', stroke=INK, sw=0.3)); o.append(circ(38, 62, 3, '#e8e0d0', stroke=INK, sw=0.3))
    o.append(rect(0, 0, 100, 100, '#8a6a20', op=0.13))
    vig = f'v{u}'; d += f'<radialGradient id="{vig}" cx="0.5" cy="0.5" r="0.72"><stop offset="0.6" stop-color="#140c06" stop-opacity="0"/><stop offset="1" stop-color="#140c06" stop-opacity="0.5"/></radialGradient>'
    o.append(rect(0, 0, 100, 100, f'url(#{vig})'))
    return ''.join(o), d

def atlas(name, seed, n=4, ppd=256):
    r = random.Random(seed); body = []; defs = []; cells = []
    for i in range(n * n):
        kind = r.choice(KINDS)
        b, d = _painting(kind, random.Random(seed * 100 + i), '%s%d' % (name, i)); cells.append(kind)
        x, y = (i % n), (i // n)
        body.append(f'<svg x="{x}" y="{y}" width="1" height="1" viewBox="0 0 100 100" preserveAspectRatio="none">{b}</svg>'); defs.append(d)
    ATLAS[name] = cells
    job(name, 0, 0, n, n, ppd, ''.join(body), defs=''.join(defs))

def cana(name='cana', W=3.0, H=2.0, ppd=200):
    """A huge Venetian wedding-feast canvas (after the manner of the Salon's big Veronese): colonnade, balustrade, a long white
    table of guests in silks, musicians in front, sky with clouds, guests on the balcony."""
    r = random.Random(77); o = []
    d = '<linearGradient id="cs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a88c0"/><stop offset="1" stop-color="#e0d8c4"/></linearGradient>'
    o.append(rect(0, 0, 150, 100, 'url(#cs)'))
    for k in range(5): o.append(ell(r.uniform(10, 140), r.uniform(5, 25), r.uniform(10, 18), r.uniform(4, 6), '#fff8ec', op=0.85))
    o.append(rect(0, 38, 150, 4, '#e8dcc0', stroke=INK, sw=0.3))
    for k in range(16): o.append(rect(3 + k * 9.3, 30, 3, 8, '#e8dcc0', stroke=INK, sw=0.2))
    for x in (2, 36, 104, 138): o.append(rect(x, 0, 10, 62, '#ece0c4', stroke=INK, sw=0.4)); o.append(rect(x - 1, 0, 12, 4, '#d8c8a8'))
    for k in range(10): x = 14 + k * 12.5; o.append(circ(x, 27, 2.5, '#e8c090', stroke=INK, sw=0.2)); o.append(rect(x - 2.5, 29, 5, 6, r.choice(('#b02a22', '#2a4a8a', '#e8c040')), stroke=INK, sw=0.2))
    o.append(rect(0, 62, 150, 38, '#a89070'))
    o.append(rect(8, 52, 134, 12, '#f4f0e4', stroke=INK, sw=0.4))
    for k in range(18):
        x = 10 + k * 7.4; c = r.choice(('#b02a22', '#2a4a9a', '#e8c040', '#3a7a4a', '#d87a3a', '#6a2a6a', '#f0ece0'))
        o.append(path(f'M{_c(x - 3.4)},52 L{_c(x - 2.4)},44 L{_c(x + 2.4)},44 L{_c(x + 3.4)},52 Z', c, stroke=INK, sw=0.25)); o.append(circ(x, 41.5, 2.4, '#e8c090', stroke=INK, sw=0.25))
    for k in range(7):
        x = 12 + k * 20; c = r.choice(('#b02a22', '#2a4a9a', '#e8c040', '#3a7a4a', '#f0ece0'))
        o.append(path(f'M{_c(x - 6)},98 L{_c(x - 4)},76 L{_c(x + 4)},76 L{_c(x + 6)},98 Z', c, stroke=INK, sw=0.4)); o.append(circ(x, 72, 4, '#e8c090', stroke=INK, sw=0.4))
        if k % 2: o.append(ell(x + 6, 86, 5, 3, '#a8742a', stroke=INK, sw=0.3))
    o.append(rect(0, 0, 150, 100, '#8a6a20', op=0.12))
    job(name, 0, 0, W, H, ppd, _g(''.join(o), 0, 0, W / 150.0), defs=d)

# ============================================================================= gallery surfaces
def damask(name, base, fg, seed=1, W=1.0, H=1.4, ppd=160):
    """Silk damask 1 x 1.4 D tile: tone-on-tone pomegranate / palmette medallions in a lattice."""
    o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, base)]
    for (cx, cy) in ((0.5, 0.35), (0.0, 1.05), (1.0, 1.05), (0.5, 1.75), (0.0, -0.35), (1.0, -0.35)):
        o.append(path(f'M{_c(cx)},{_c(cy - 0.32)} C{_c(cx + 0.22)},{_c(cy - 0.2)} {_c(cx + 0.28)},{_c(cy + 0.12)} {_c(cx)},{_c(cy + 0.34)} C{_c(cx - 0.28)},{_c(cy + 0.12)} {_c(cx - 0.22)},{_c(cy - 0.2)} {_c(cx)},{_c(cy - 0.32)} Z', fg))
        o.append(path(f'M{_c(cx)},{_c(cy - 0.18)} C{_c(cx + 0.11)},{_c(cy - 0.1)} {_c(cx + 0.13)},{_c(cy + 0.08)} {_c(cx)},{_c(cy + 0.2)} C{_c(cx - 0.13)},{_c(cy + 0.08)} {_c(cx - 0.11)},{_c(cy - 0.1)} {_c(cx)},{_c(cy - 0.18)} Z', base))
        o.append(circ(cx, cy + 0.0, 0.05, fg))
        for s in (-1, 1):
            o.append(path(f'M{_c(cx + s * 0.06)},{_c(cy + 0.3)} Q{_c(cx + s * 0.3)},{_c(cy + 0.4)} {_c(cx + s * 0.42)},{_c(cy + 0.2)}', 'none', stroke=fg, sw=0.025))
            o.append(ell(cx + s * 0.42, cy + 0.16, 0.05, 0.08, fg))
    for (cx, cy) in ((0.0, 0.35), (1.0, 0.35), (0.5, 1.05)):
        o.append(path(f'M{_c(cx)},{_c(cy - 0.12)} L{_c(cx + 0.07)},{_c(cy)} L{_c(cx)},{_c(cy + 0.12)} L{_c(cx - 0.07)},{_c(cy)} Z', fg, op=0.8))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def parquet(name='parquet', seed=3, W=4.0, H=4.0, ppd=80, base='#9a6a3c'):
    """Waxed oak herringbone parquet 4 x 4 D: slats 0.9 x 0.22 at 45 deg, varied tone, a polished sheen band."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, mul(base, 0.6))]
    L, w = 0.9, 0.22; s2 = math.sqrt(0.5)
    for i in range(-12, 30):
        for j in range(-4, 12):
            for k in (0, 1):
                c = mul(r.choice((base, '#a8763e', '#8c5e34', '#b07e46', '#946436')), r.uniform(0.9, 1.08))
                ox = j * 2 * L * s2 + (L * s2 if k else 0); oy = i * w * 2 * s2 - j * 0.0
                if k == 0: pts = [(ox, oy), (ox + L * s2, oy + L * s2), (ox + L * s2 - w * s2, oy + L * s2 + w * s2), (ox - w * s2, oy + w * s2)]
                else: pts = [(ox, oy + L * s2), (ox + L * s2, oy), (ox + L * s2 + w * s2, oy + w * s2), (ox + w * s2, oy + L * s2 + w * s2)]
                if any(-1 < x < W + 1 and -1 < y < H + 1 for x, y in pts): o.append(poly(pts, c, stroke='#3a2414', sw=0.012))
    for _ in range(20):
        x, y = r.uniform(0, W), r.uniform(0, H); o.append(ell(x, y, r.uniform(0.2, 0.6), r.uniform(0.05, 0.12), '#f8e8c8', op=0.12))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def gold(name='gold', seed=5, W=2.0, H=0.5, ppd=160):
    """Gilded carved frame moulding 2 x 0.5 D (u along the frame, v 0 = the outer edge, 1 = the sight edge): bevel shading, a bead
    and reel at the outer edge, an acanthus run across the cove, egg-and-dart at the sight edge, red bole showing in the hollows."""
    r = random.Random(seed)
    d = ('<linearGradient id="gb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a5418"/><stop offset="0.12" stop-color="#e8c060"/><stop offset="0.3" stop-color="#b88a30"/>'
         '<stop offset="0.5" stop-color="#f4d478"/><stop offset="0.7" stop-color="#a87a28"/><stop offset="0.86" stop-color="#e0b850"/><stop offset="1" stop-color="#6a4410"/></linearGradient>')
    o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, 'url(#gb)')]
    n = 20
    for i in range(n + 1):
        x = i * W / n
        o.append(ell(x, 0.05, 0.035, 0.025, '#f8e090', stroke='#6a4410', sw=0.006)); o.append(rect(x + 0.045, 0.04, 0.012, 0.02, '#6a4410'))
    for i in range(10):
        x = i * W / 10
        o.append(path(f'M{_c(x)},{_c(0.3)} C{_c(x + 0.03)},{_c(0.13)} {_c(x + 0.15)},{_c(0.12)} {_c(x + 0.17)},{_c(0.22)} C{_c(x + 0.12)},{_c(0.2)} {_c(x + 0.08)},{_c(0.26)} {_c(x + 0.1)},{_c(0.32)} Z', '#f8dc80', stroke='#6a4410', sw=0.008))
        o.append(path(f'M{_c(x + 0.1)},{_c(0.32)} C{_c(x + 0.12)},{_c(0.24)} {_c(x + 0.2)},{_c(0.24)} {_c(x + 0.2)},{_c(0.3)}', 'none', stroke='#6a4410', sw=0.008))
        o.append(circ(x + 0.17, 0.22, 0.012, '#8a3a1a'))
    for i in range(16):
        x = (i + 0.5) * W / 16
        o.append(ell(x, 0.43, 0.04, 0.035, '#f0d070', stroke='#5a3a10', sw=0.008)); o.append(path(f'M{_c(x + 0.062)},{_c(0.4)} l0,0.06', 'none', stroke='#5a3a10', sw=0.012))
    for _ in range(40): o.append(circ(r.uniform(0, W), r.uniform(0, H), r.uniform(0.004, 0.012), '#5a2a10', op=0.4))
    job(name, 0, 0, W, H, ppd, ''.join(o), defs=d)

def frieze(name='frieze', W=4.0, H=1.0, ppd=96):
    """Cornice frieze 4 x 1 D (v 0 = top): gilded garlands and laurel wreath medallions with an N cipher on cream, dentils above,
    a gilded egg-and-dart below."""
    o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#e8dcc0'), rect(-0.1, 0, W + 0.2, 0.14, '#d4c4a0')]
    for i in range(int(W / 0.12) + 1): o.append(rect(i * 0.12, 0.03, 0.07, 0.09, '#fff4dc', stroke='#8a7448', sw=0.006))
    o.append(rect(-0.1, 0.16, W + 0.2, 0.03, '#c8a040'))
    for cx in (1.0, 3.0):
        o.append(circ(cx, 0.52, 0.24, 'none', stroke='#c89838', sw=0.06)); o.append(circ(cx, 0.52, 0.17, '#d8c8a0'))
        o.append(_txt(cx, 0.62, 'N', 0.26, '#c89838'))
        for s in (-1, 1):
            o.append(path(f'M{_c(cx + s * 0.26)},{_c(0.44)} Q{_c(cx + s * 0.6)},{_c(0.86)} {_c(cx + s * 1.0)},{_c(0.36)}', 'none', stroke='#c89838', sw=0.07))
            for k in range(6):
                t = (k + 0.5) / 6; x = cx + s * (0.26 + 0.74 * t); y = 0.44 + (0.86 - 0.44) * 4 * t * (1 - t) * 0.8
                o.append(ell(x, y, 0.045, 0.025, '#e0b850', stroke='#7a5418', sw=0.006))
    o.append(rect(-0.1, 0.84, W + 0.2, 0.04, '#c8a040'))
    for i in range(int(W / 0.1) + 1): o.append(ell(i * 0.1 + 0.05, 0.93, 0.035, 0.045, '#e0b850', stroke='#7a5418', sw=0.006))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def coffer(name='coffer', W=2.0, H=2.0, ppd=96):
    """Coffered cove 2 x 2 D: four sunk panels, each a gilded rosette on a grey-blue ground framed by cream mouldings."""
    o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#e8dcc0')]
    for (x, y) in ((0, 0), (1, 0), (0, 1), (1, 1)):
        o.append(rect(x + 0.08, y + 0.08, 0.84, 0.84, '#c8bc9c', stroke='#8a7a58', sw=0.012)); o.append(rect(x + 0.16, y + 0.16, 0.68, 0.68, '#7a8aa0', stroke='#c89838', sw=0.03))
        cx, cy = x + 0.5, y + 0.5
        for k in range(8):
            a = 2 * math.pi * k / 8; o.append(ell(cx + 0.12 * math.cos(a), cy + 0.12 * math.sin(a), 0.08, 0.04, '#e8c058', stroke='#7a5418', sw=0.008, extra=f' transform="rotate({_c(math.degrees(a))} {_c(cx + 0.12 * math.cos(a))} {_c(cy + 0.12 * math.sin(a))})"'))
        o.append(circ(cx, cy, 0.06, '#f4d878', stroke='#7a5418', sw=0.01))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def marble(name='marble', base='#8a4a3a', vein='#e8d0c0', seed=9, W=2.0, H=2.0, ppd=80):
    """Polished marble 2 x 2 D: cloudy ground, thin wandering veins."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, base)]
    for _ in range(30): o.append(ell(r.uniform(0, W), r.uniform(0, H), r.uniform(0.1, 0.5), r.uniform(0.05, 0.2), mul(base, r.uniform(0.8, 1.2)), op=0.5))
    for _ in range(9):
        x, y = r.uniform(0, W), r.uniform(0, H); pts = [(x, y)]
        for k in range(8): x += r.uniform(0.05, 0.3); y += r.uniform(-0.15, 0.15); pts.append((x, y))
        o.append(pline(pts, vein, r.uniform(0.008, 0.02), op=0.7))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def skyglass(name='skyglass', W=2.0, H=2.0, ppd=64):
    """Skylight glazing 2 x 2 D (emission): warm white panes with a soft cloudy brightness, iron glazing bars, a dark outline."""
    r = random.Random(13); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#fff4dc')]
    for _ in range(14): o.append(ell(r.uniform(0, W), r.uniform(0, H), r.uniform(0.2, 0.5), r.uniform(0.1, 0.25), '#ffffff', op=0.5))
    for _ in range(8): o.append(ell(r.uniform(0, W), r.uniform(0, H), r.uniform(0.2, 0.4), r.uniform(0.1, 0.2), '#e8dcc8', op=0.4))
    for k in range(5): o.append(line(k * 0.5, -0.1, k * 0.5, H + 0.1, '#3a3430', 0.035))
    for k in range(9): o.append(line(-0.1, k * 0.25, W + 0.1, k * 0.25, '#4a4440', 0.018))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def door_panel(name='door_gal', W=2.0, H=4.2, ppd=96):
    """Gallery double door 2 x 4.2 D: cream-grey painted raised panels with gilded mouldings, a brass lock plate."""
    o = [rect(0, 0, W, H, '#d8ccb0', stroke=INK, sw=0.02), line(W / 2, 0, W / 2, H, '#5a4a30', 0.03)]
    for s in (0, 1):
        x = s * W / 2
        for (y, h) in ((0.2, 1.7), (2.1, 0.5), (2.8, 1.2)):
            o.append(rect(x + 0.14, y, W / 2 - 0.28, h, '#cfc2a4', stroke='#c89838', sw=0.04, rx=0.04)); o.append(rect(x + 0.24, y + 0.1, W / 2 - 0.48, h - 0.2, 'none', stroke='#a8946a', sw=0.015))
    o.append(rect(W / 2 - 0.16, 2.15, 0.12, 0.35, '#c8a040', stroke=INK, sw=0.01)); o.append(circ(W / 2 - 0.1, 2.3, 0.04, '#7a5418'))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def plaque(name='plaque', W=0.6, H=0.2, ppd=320):
    o = [rect(0, 0, W, H, '#c8a040', stroke='#6a4410', sw=0.01, rx=0.02), _txt(W / 2, 0.09, 'L&#201;ONARD DE VINCI', 0.05, '#3a2410'), _txt(W / 2, 0.16, 'La Joconde', 0.05, '#3a2410', weight=400, extra=' font-style="italic"')]
    job(name, 0, 0, W, H, ppd, ''.join(o))

# ============================================================================= service rooms
def ashlar(name='ashlar', base='#c8b898', seed=21, W=4.0, H=4.0, ppd=80, soot=0.25):
    """Dressed limestone blocks 4 x 4 D (service stair, corridor): courses 0.8 D, pale joints, chisel marks, grime toward the floor."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#e4dccc')]
    for k in range(5):
        y = k * 0.8; off = (k % 2) * 0.7; x = -off
        while x < W:
            w = r.uniform(1.0, 1.6); c = mul(r.choice((base, '#c0b090', '#d0c0a0', '#bcae92')), r.uniform(0.94, 1.05))
            for xx in _wrap(x, W, w):
                o.append(rect(xx + 0.025, y + 0.025, w - 0.05, 0.75, c, stroke=INK, sw=0.008, rx=0.02))
                o.append(line(xx + 0.06, y + 0.06, xx + w - 0.08, y + 0.06, mul(c, 1.12), 0.02, op=0.7))
                for _ in range(3): o.append(ell(xx + r.uniform(0.2, w - 0.2), y + r.uniform(0.2, 0.6), r.uniform(0.1, 0.3), r.uniform(0.04, 0.1), mul(c, r.uniform(0.88, 1.08)), op=0.6))
            x += w
    g = f'<linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3028" stop-opacity="0"/><stop offset="1" stop-color="#3a3028" stop-opacity="{soot}"/></linearGradient>'
    o.append(rect(-0.1, H - 1.5, W + 0.2, 1.6, 'url(#s)'))
    job(name, 0, 0, W, H, ppd, ''.join(o), defs=g)

def oak_door(name='oak_door', W=2.2, H=4.4, ppd=96, studs=True):
    """Heavy service door 2.2 x 4.4 D: vertical oak boards, two iron strap hinges with fleur ends, studs, a big iron lock box with a
    keyhole; the knob is missing (the hole shows - Peruggia found it removed)."""
    r = random.Random(31); o = [rect(0, 0, W, H, '#3a2414')]
    n = 6; bw = W / n
    for i in range(n):
        c = mul('#7a5230', r.uniform(0.88, 1.08)); o.append(rect(i * bw + 0.01, 0, bw - 0.02, H, c))
        for _ in range(6): x = i * bw + r.uniform(0.03, bw - 0.03); o.append(line(x, 0, x + r.uniform(-0.02, 0.02), H, mul(c, 0.8), 0.008, op=0.8))
    for y in (0.5, H - 0.7):
        o.append(rect(0.0, y, W * 0.8, 0.14, '#2a2628', stroke='#111', sw=0.01))
        o.append(path(f'M{_c(W * 0.8)},{_c(y + 0.07)} l0.18,-0.12 l0.06,0.12 l-0.06,0.12 Z', '#2a2628'))
        if studs:
            for k in range(7): o.append(circ(0.12 + k * 0.25, y + 0.07, 0.025, '#5a5658'))
    o.append(rect(W - 0.62, H * 0.47, 0.42, 0.55, '#2a2628', stroke='#111', sw=0.015, rx=0.03))
    o.append(path(f'M{_c(W - 0.41)},{_c(H * 0.47 + 0.18)} a0.05,0.05 0 1 1 0.001,0 l0.03,0.16 l-0.06,0 Z', '#000'))
    o.append(circ(W - 0.41, H * 0.47 + 0.42, 0.045, '#0a0806'))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def label_sign(name, text, sub='', W=1.6, H=0.5, bg='#1e3a2a', fg='#f0d070', ppd=200, font='DejaVu Serif, serif'):
    o = [rect(0, 0, W, H, bg, rx=0.04), rect(0.03, 0.03, W - 0.06, H - 0.06, 'none', stroke=fg, sw=0.015, rx=0.03),
         _txt(W / 2, H * (0.62 if not sub else 0.5), text, H * (0.42 if not sub else 0.32), fg, font=font)]
    if sub: o.append(_txt(W / 2, H * 0.83, sub, H * 0.16, fg, font=font, weight=400))
    job(name, 0, 0, W, H, ppd, ''.join(o))

# ============================================================================= Paris street
def haussmann(name, seed, W=8.0, H=15.0, ppd=56, shops=('CAF&#201;', 'TABAC'), stone='#e6d6b4', lit=0.0):
    """Haussmann apartment front W x H D (v 0 = the top: the cornice; H = the pavement): rusticated ground floor with shopfronts
    and signs, an entresol, the noble floor with a continuous wrought-iron balcony, two floors with pedimented windows, a fifth-floor
    balcony, the cornice. Window glass dark blue with lace curtains; some lit warm (lit = probability)."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, stone)]
    def Y(z): return H - z
    for k in range(int(W / 0.8) + 1): o.append(line(k * 0.8, Y(4.4), k * 0.8, Y(0), mul(stone, 0.82), 0.02))
    for z in [0.45 * k for k in range(1, 11)]: o.append(line(-0.1, Y(z), W + 0.1, Y(z), mul(stone, 0.8), 0.03))
    nb = 3; bay = W / nb
    for i in range(nb):                                                                    # ground-floor shopfronts
        x = i * bay + 0.25; w = bay - 0.5; sh = shops[i % len(shops)] if shops else None
        if sh:
            o.append(rect(x, Y(3.1), w, 3.1, r.choice(('#3a2a3a', '#2a3a2e', '#5a2a1e', '#2a2e48')), stroke=INK, sw=0.03))
            o.append(rect(x + 0.12, Y(2.75), w - 0.24, 2.6, '#ffd890' if r.random() < lit + 0.3 else '#3a4a5a', stroke='#c8a040', sw=0.03))
            for k in range(1, 3): o.append(line(x + 0.12 + k * (w - 0.24) / 3, Y(2.75), x + 0.12 + k * (w - 0.24) / 3, Y(0.15), '#c8a040', 0.025))
            o.append(rect(x, Y(3.7), w, 0.55, '#1e2a3a', stroke='#c8a040', sw=0.02)); o.append(_txt(x + w / 2, Y(3.3), sh, 0.36, '#f0d070'))
        else:
            o.append(path(f'M{_c(x + 0.3)},{_c(Y(0))} L{_c(x + 0.3)},{_c(Y(2.6))} A{_c(w / 2 - 0.3)},{_c(w / 2 - 0.3)} 0 0 1 {_c(x + w - 0.3)},{_c(Y(2.6))} L{_c(x + w - 0.3)},{_c(Y(0))} Z', '#2a3a2e', stroke=INK, sw=0.03))
            for k in range(4): o.append(rect(x + 0.45, Y(0.4 + k * 0.6), w - 0.9, 0.45, '#3a4a3a', stroke='#1a2a1e', sw=0.015))
    o.append(rect(-0.1, Y(4.5), W + 0.2, 0.18, mul(stone, 0.85), stroke=INK, sw=0.015))
    def window(x, z, w, h, ped=None, balc=False):
        lit_ = r.random() < lit
        o.append(rect(x - 0.08, Y(z + h + 0.08), w + 0.16, h + 0.16, mul(stone, 0.9), stroke=INK, sw=0.015))
        o.append(rect(x, Y(z + h), w, h, '#ffc870' if lit_ else '#2e3a52', stroke=INK, sw=0.02))
        if not lit_:
            o.append(path(f'M{_c(x + 0.05)},{_c(Y(z + h - 0.05))} Q{_c(x + w * 0.3)},{_c(Y(z + h * 0.4))} {_c(x + 0.1)},{_c(Y(z + 0.05))} L{_c(x + 0.05)},{_c(Y(z + 0.05))} Z', '#e8e4d8', op=0.75))
            o.append(path(f'M{_c(x + w - 0.05)},{_c(Y(z + h - 0.05))} Q{_c(x + w * 0.7)},{_c(Y(z + h * 0.4))} {_c(x + w - 0.1)},{_c(Y(z + 0.05))} L{_c(x + w - 0.05)},{_c(Y(z + 0.05))} Z', '#e8e4d8', op=0.75))
            o.append(line(x + 0.05, Y(z + h * 0.75), x + w - 0.05, Y(z + h * 0.75), '#c8d0e0', 0.02, op=0.5))
        o.append(line(x + w / 2, Y(z + h), x + w / 2, Y(z), '#e8e0cc', 0.03))
        for k in (0.33, 0.66): o.append(line(x, Y(z + h * k), x + w, Y(z + h * k), '#e8e0cc', 0.02))
        for s in (-1, 1): o.append(rect(x + (w + 0.1 if s > 0 else -0.32), Y(z + h), 0.22, h, '#5a6a52', stroke=INK, sw=0.012))   # shutters folded
        if ped == 'tri': o.append(poly([(x - 0.2, Y(z + h + 0.12)), (x + w / 2, Y(z + h + 0.55)), (x + w + 0.2, Y(z + h + 0.12))], mul(stone, 0.92), stroke=INK, sw=0.015))
        elif ped == 'seg': o.append(path(f'M{_c(x - 0.2)},{_c(Y(z + h + 0.12))} Q{_c(x + w / 2)},{_c(Y(z + h + 0.6))} {_c(x + w + 0.2)},{_c(Y(z + h + 0.12))} Z', mul(stone, 0.92), stroke=INK, sw=0.015))
        elif ped == 'flat': o.append(rect(x - 0.18, Y(z + h + 0.3), w + 0.36, 0.18, mul(stone, 0.92), stroke=INK, sw=0.015))
        if not balc:
            o.append(rect(x - 0.05, Y(z + 0.55), w + 0.1, 0.55, 'none', stroke='#1e1c20', sw=0.02))
            for k in range(7): o.append(path(f'M{_c(x + k * w / 6)},{_c(Y(z))} q0.08,-0.28 0,-0.55', 'none', stroke='#1e1c20', sw=0.015))
    for i in range(nb):                                                                     # entresol
        window(i * bay + bay * 0.3, 4.75, bay * 0.4, 1.2)
    for (z, h, ped) in ((6.4, 2.3, 'tri'), (9.1, 2.0, 'seg'), (11.4, 1.8, 'flat')):
        for i in range(nb): window(i * bay + bay * 0.28, z, bay * 0.44, h, ped if i != 1 or ped != 'tri' else 'seg', balc=z in (6.4,))
    for zb in (6.4, 13.2):                                                                  # continuous balconies (painted rail; 3D slab in the set)
        o.append(rect(-0.1, Y(zb + 0.75), W + 0.2, 0.08, '#1e1c20'))
        for k in range(int(W / 0.3) + 1):
            x = k * 0.3; o.append(path(f'M{_c(x)},{_c(Y(zb))} q0.15,-0.4 0,-0.75 M{_c(x + 0.15)},{_c(Y(zb + 0.375))} a0.08,0.08 0 1 0 0.001,0', 'none', stroke='#1e1c20', sw=0.018))
    for i in range(nb): window(i * bay + bay * 0.3, 13.2, bay * 0.4, 1.3, None, balc=True)
    o.append(rect(-0.1, Y(6.3), W + 0.2, 0.2, mul(stone, 0.82), stroke=INK, sw=0.015))
    o.append(rect(-0.1, 0, W + 0.2, 0.55, mul(stone, 0.85), stroke=INK, sw=0.02))
    for k in range(int(W / 0.2) + 1): o.append(rect(k * 0.2, 0.42, 0.1, 0.13, mul(stone, 0.7)))
    for _ in range(12):
        x = r.uniform(0, W); o.append(rect(x, r.uniform(0.6, 4.0), r.uniform(0.05, 0.3), r.uniform(1.0, 5.0), '#6a5a48', op=0.07))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def mansard(name='mansard', W=8.0, H=4.0, ppd=56):
    """Zinc mansard roof 8 x 4 D (transparent above): blue-grey zinc seams, three dormers with oeil-de-boeuf / square windows,
    chimney stacks with terracotta pots."""
    r = random.Random(41); o = [path(f'M0,{_c(H)} L0.3,1.2 L{_c(W - 0.3)},1.2 L{_c(W)},{_c(H)} Z', '#6a7488')]
    for k in range(int(W / 0.25)): o.append(line(0.15 + k * 0.25, 1.2, 0.15 + k * 0.25 * (1 + 0.0), H, '#4e586a', 0.02))
    for i in range(3):
        x = 1.0 + i * 2.6
        o.append(rect(x, 1.9, 1.0, 1.6, '#e6d6b4', stroke=INK, sw=0.02)); o.append(path(f'M{_c(x - 0.15)},1.95 Q{_c(x + 0.5)},1.25 {_c(x + 1.15)},1.95 Z', '#5a6478', stroke=INK, sw=0.02))
        lit_ = r.random() < 0.3
        o.append(path(f'M{_c(x + 0.2)},3.35 L{_c(x + 0.2)},2.45 A0.3,0.3 0 0 1 {_c(x + 0.8)},2.45 L{_c(x + 0.8)},3.35 Z', '#ffc870' if lit_ else '#2e3a52', stroke=INK, sw=0.02))
    for x in (0.4, 3.4, 6.9):
        o.append(rect(x, 0.0, 0.8, 1.3, '#c8a888', stroke=INK, sw=0.02))
        for k in range(3): o.append(rect(x + 0.06 + k * 0.25, -0.0, 0.14, 0.3, '#c8683a', stroke=INK, sw=0.012))
    o.append(rect(0, H - 0.18, W, 0.18, '#3e4656'))
    job(name, 0, 0, W, H, ppd, ''.join(o), transparent=True)

def newspaper(name, mast, head, seed, W=0.8, H=1.1, ppd=280):
    """Front page W x H D with the masthead, a banner headline about the theft and the Mona Lisa in a framed half-tone (sepia)."""
    r = random.Random(seed); o = [rect(0, 0, W, H, '#ece4cc')]
    S = W / 100.0
    body, d = mona_svg('n' + name)
    d += f'<filter id="sep{name}"><feColorMatrix type="matrix" values="0.39 0.69 0.19 0 0  0.35 0.62 0.17 0 0  0.27 0.48 0.13 0 0  0 0 0 1 0"/></filter>'
    o.append(_txt(W / 2, 0.105, mast, 0.062 if len(mast) > 12 else 0.08, '#141010'))
    o.append(line(0.03, 0.135, W - 0.03, 0.135, '#141010', 0.006)); o.append(line(0.03, 0.15, W - 0.03, 0.15, '#141010', 0.003))
    o.append(_txt(W / 2, 0.22, head, 0.058, '#141010', font='DejaVu Sans, sans-serif', weight=800))
    pw = 0.36; ph = pw * 1.45; px = (W - pw) / 2; py = 0.26
    o.append(rect(px - 0.012, py - 0.012, pw + 0.024, ph + 0.024, '#141010'))
    o.append(f'<g filter="url(#sep{name})">' + _g(body, px, py, pw / 100.0) + '</g>')
    for col in range(4):
        x0 = 0.03 + col * (W - 0.06) / 4
        for k in range(30):
            y = 0.3 + k * 0.026
            if py - 0.02 < y < py + ph + 0.03 and px - 0.03 < x0 + 0.08 < px + pw + 0.03: continue
            if y > H - 0.03: break
            o.append(line(x0 + 0.01, y, x0 + (W - 0.06) / 4 - 0.015 - (0.04 if r.random() < 0.15 else 0), y, '#5a5248', 0.008))
    job(name, 0, 0, W, H, ppd, ''.join(o), defs=d)

def poster(name, kind, seed, W=1.0, H=1.4, ppd=200):
    """Belle Epoque poster W x H D. kind 'mona': 'LA JOCONDE' in red over her portrait, 'DISPARUE !' ; 'mona2': a postcard / advert
    with her face ('Elle sourit encore !'); 'choc', 'cirque', 'velo', 'opera': invented period adverts."""
    r = random.Random(seed); o = []; d = ''
    if kind in ('mona', 'mona2'):
        body, d = mona_svg('p' + name)
        bg = '#f0e2b8' if kind == 'mona' else '#2a3a5a'; fg = '#c02a1a' if kind == 'mona' else '#f0d070'
        o.append(rect(0, 0, W, H, bg)); o.append(rect(0.04, 0.04, W - 0.08, H - 0.08, 'none', stroke=fg, sw=0.02))
        o.append(_txt(W / 2, 0.2, 'LA JOCONDE' if kind == 'mona' else 'O&#217; EST-ELLE ?', 0.12, fg, font='DejaVu Sans, sans-serif', weight=800))
        pw = 0.56; o.append(rect((W - pw) / 2 - 0.02, 0.26, pw + 0.04, pw * 1.45 + 0.04, '#c8a040'))
        o.append(_g(body, (W - pw) / 2, 0.28, pw / 100.0))
        o.append(_txt(W / 2, H - 0.12, 'DISPARUE !' if kind == 'mona' else 'Elle sourit encore', 0.1, fg, font='DejaVu Sans, sans-serif', weight=800))
    else:
        bg, fg, t1, t2 = dict(choc=('#e8a830', '#6a2a1a', 'CHOCOLAT', 'LUNA'), cirque=('#c02a2a', '#f8e8b0', 'CIRQUE', "D'HIVER"),
                              velo=('#2a5a8a', '#f8e090', 'CYCLES', 'AIGLE'), opera=('#1e1e2a', '#e8c060', 'OP&#201;RA', 'CE SOIR'))[kind]
        o.append(rect(0, 0, W, H, bg))
        o.append(_txt(W / 2, 0.22, t1, 0.15, fg, font='DejaVu Sans, sans-serif', weight=800)); o.append(_txt(W / 2, H - 0.1, t2, 0.13, fg, font='DejaVu Sans, sans-serif', weight=800))
        cx, cy = W / 2, H * 0.55
        o.append(circ(cx, cy, 0.3, mix(bg, '#ffffff', 0.35)))
        o.append(ell(cx, cy - 0.12, 0.1, 0.12, '#f4d0a8', stroke=INK, sw=0.01)); o.append(path(f'M{_c(cx - 0.22)},{_c(cy + 0.3)} Q{_c(cx)},{_c(cy - 0.1)} {_c(cx + 0.22)},{_c(cy + 0.3)} Z', fg, stroke=INK, sw=0.01))
        o.append(path(f'M{_c(cx - 0.14)},{_c(cy - 0.18)} Q{_c(cx)},{_c(cy - 0.36)} {_c(cx + 0.14)},{_c(cy - 0.18)} Z', r.choice(('#e8c040', '#2a1a10', '#c02a2a'))))
    job(name, 0, 0, W, H, ppd, ''.join(o), defs=d)

def morris(name='morris', W=6.0, H=3.6, ppd=80):
    """Colonne Morris wrap 6 x 3.6 D (u round, v 0 = top): a collage of overlapping period posters and bills."""
    r = random.Random(51); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#3a5a3a')]
    cols = ('#e8a830', '#c02a2a', '#2a5a8a', '#f0e2b8', '#1e1e2a', '#7a3a6a', '#e8e0c8', '#3a7a4a')
    for _ in range(26):
        w = r.uniform(0.6, 1.2); h = r.uniform(0.8, 1.4); x = r.uniform(0, W); y = r.uniform(-0.2, H - 0.6); c = r.choice(cols)
        for xx in _wrap(x, W, w):
            o.append(rect(xx, y, w, h, c, stroke='#1a1a1a', sw=0.008))
            o.append(rect(xx + 0.08, y + 0.1, w - 0.16, 0.16, mix(c, '#ffffff', 0.6)))
            for k in range(3): o.append(rect(xx + 0.1, y + 0.4 + k * 0.18, w * r.uniform(0.4, 0.8), 0.07, mix(c, '#000000', 0.4)))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def kiosk_panel(name='kiosk', W=2.0, H=1.0, ppd=128):
    o = [rect(0, 0, W, H, '#2e4a34'), rect(0.04, 0.04, W - 0.08, H - 0.08, 'none', stroke='#c8a040', sw=0.02)]
    o.append(_txt(W / 2, H * 0.62, 'JOURNAUX', H * 0.36, '#f0d070'))
    job(name, 0, 0, W, H, ppd, ''.join(o))

SKYP = dict(
    day=dict(stops=[(0, '#4a7cc4'), (0.4, '#7ea6d8'), (0.66, '#bcd0e4'), (0.85, '#f0e0c0'), (1, '#f8e4b8')], cloud='#fff8ee', cloud_b='#d8c8c0', sun=('#fff4d0', 200.0, 40.0), glow='#ffe0a0'),
    dusk=dict(stops=[(0, '#3a4a8a'), (0.35, '#7a6aa8'), (0.62, '#e09a80'), (0.82, '#f8c070'), (1, '#ffd890')], cloud='#ffdcb8', cloud_b='#e0a888', sun=('#fff0c0', 250.0, 6.0), glow='#ffb860'),
)
def sky(mode):
    s = SKYP[mode]; r = random.Random(191 + len(mode)); W, H = 360.0, 105.0
    g = '<linearGradient id="g" x1="0" y1="0" x2="0" y2="1">' + ''.join(f'<stop offset="{o_}" stop-color="{c}"/>' for o_, c in s['stops']) + '</linearGradient>'
    g += '<filter id="b" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="0.18"/></filter>'
    g += f'<radialGradient id="glow"><stop offset="0" stop-color="#fffbe8" stop-opacity="1"/><stop offset="0.3" stop-color="{s["glow"]}" stop-opacity="0.6"/><stop offset="1" stop-color="{s["glow"]}" stop-opacity="0"/></radialGradient>'
    o = [rect(-1, -1, W + 2, H + 2, 'url(#g)')]
    sc, az, el = s['sun']
    for dx in (0, W, -W): o.append(ell(az + dx, 90 - el, 70, 34, 'url(#glow)')); o.append(circ(az + dx, 90 - el, 4.0, sc))
    for i in range(24):
        cx = r.uniform(0, W); el2 = r.uniform(6, 40); cy = 90 - el2; w = r.uniform(14, 36) * (1.0 if el2 > 15 else 0.7)
        for xx in _wrap(cx - w / 2, W, w):
            xc = xx + w / 2; grp = []
            for k in range(5):
                t = (k + 0.5) / 5; rk = w * r.uniform(0.11, 0.17) * (1.3 - abs(t - 0.5)); grp.append(circ(xc - w / 2 + w * (0.08 + 0.84 * t), cy - rk * 0.6, rk, s['cloud']))
            grp.append(rect(xc - w / 2, cy - w * 0.07, w, w * 0.07, s['cloud'], rx=w * 0.035)); grp.append(rect(xc - w / 2 + 0.6, cy - w * 0.035, w - 1.2, w * 0.035, s['cloud_b'], rx=w * 0.02))
            o.append('<g filter="url(#b)" opacity="0.95">' + ''.join(grp) + '</g>')
    for _ in range(14):
        x = r.uniform(0, W); y = 90 - r.uniform(12, 35); o.append(pline([(x - 0.6, y - 0.3), (x, y), (x + 0.6, y - 0.3)], '#3a3a4a', 0.12))
    job('sky_' + mode, 0, 0, W, H, 4096 / 360.0, ''.join(o), defs=g)

PANO_R = 120.0; PANO_Z0, PANO_Z1 = -1.5, 40.0
def pano_paris(mode):
    """Painted ring at R 120: Paris rooftops - rows of cream Haussmann blocks with zinc mansards, chimney pots and smoke, domes (the
    Invalides gold dome, the Pantheon), the Eiffel Tower on one side, Sacre-Coeur white on its hill on the other."""
    r = random.Random(211); W = 2 * math.pi * PANO_R; H = PANO_Z1 - PANO_Z0; o = []
    dusk = mode == 'dusk'; haze = '#f0d8c0' if dusk else '#e8e4e0'
    def Y(z): return PANO_Z1 - z
    hz = lambda c, k=1.0: mix(c, haze, min(0.9, 0.3 * k))
    o.append(poly([(W * i / 60, Y(5 + 2 * abs(math.sin(i * 0.5)))) for i in range(61)] + [(W, Y(-2)), (0, Y(-2))], hz('#a8a0b8', 1.8)))
    ex = W * 0.30; o.append(path(f'M{_c(ex - 5)},{_c(Y(4))} Q{_c(ex - 1.2)},{_c(Y(14))} {_c(ex - 0.3)},{_c(Y(30))} L{_c(ex + 0.3)},{_c(Y(30))} Q{_c(ex + 1.2)},{_c(Y(14))} {_c(ex + 5)},{_c(Y(4))} '
                                 f'L{_c(ex + 3)},{_c(Y(4))} Q{_c(ex)},{_c(Y(9))} {_c(ex - 3)},{_c(Y(4))} Z', hz('#6a5a5a', 1.2)))
    for z in (11, 19): o.append(rect(ex - (3.2 if z == 11 else 1.6), Y(z), 6.4 if z == 11 else 3.2, 0.6, hz('#6a5a5a', 1.2)))
    sx = W * 0.72; o.append(ell(sx, Y(5), 18, 6, hz('#7a8a6a', 1.4)))
    o.append(rect(sx - 6, Y(13), 12, 6, hz('#f4f0e8', 1.0))); o.append(ell(sx, Y(13), 3.5, 4.5, hz('#f4f0e8', 1.0)))
    for dx in (-4.5, 4.5): o.append(ell(sx + dx, Y(13), 1.6, 2.4, hz('#f4f0e8', 1.0)))
    o.append(rect(sx + 6, Y(17), 1.6, 8, hz('#f4f0e8', 1.0)))
    for (cx, c) in ((W * 0.12, '#d8b050'), (W * 0.52, '#a8a8b0'), (W * 0.9, '#8a9a9a')):
        o.append(rect(cx - 4, Y(9), 8, 6, hz('#e8dcc4', 1.0))); o.append(rect(cx - 3, Y(12), 6, 3, hz('#e8dcc4', 1.0)))
        o.append(path(f'M{_c(cx - 3)},{_c(Y(12))} Q{_c(cx)},{_c(Y(19))} {_c(cx + 3)},{_c(Y(12))} Z', hz(c, 0.8))); o.append(line(cx, Y(17.5), cx, Y(20), hz('#5a5a5a', 0.8), 0.25))
    for band, (zb, sc_, hk) in enumerate(((3.5, 0.8, 1.2), (1.6, 1.0, 0.7), (-0.4, 1.25, 0.3))):
        x = r.uniform(-4, 0)
        while x < W:
            w = r.uniform(5, 9) * sc_; h = r.uniform(4.5, 6.5) * sc_; z0 = zb
            c = hz(r.choice(('#ecdcbc', '#e4d0ac', '#f0e4cc', '#e0ccb0')), hk); rc = hz(r.choice(('#6a7488', '#5e687c', '#7a7a8a')), hk)
            o.append(rect(x, Y(z0 + h), w, h + 2, c, stroke=hz('#8a7a64', hk), sw=0.1))
            for fz in range(1, 5):
                for wx in range(int(w / 1.2)):
                    lw = r.random() < (0.25 if dusk else 0.03)
                    o.append(rect(x + 0.4 + wx * 1.2, Y(z0 + fz * h / 5.2 + 0.7 * sc_), 0.45 * sc_, 0.7 * sc_, '#ffc070' if lw else hz('#3a4460', hk)))
            o.append(path(f'M{_c(x)},{_c(Y(z0 + h))} L{_c(x + 0.6)},{_c(Y(z0 + h + 1.6 * sc_))} L{_c(x + w - 0.6)},{_c(Y(z0 + h + 1.6 * sc_))} L{_c(x + w)},{_c(Y(z0 + h))} Z', rc, stroke=mul(rc, 0.7), sw=0.08))
            for k in range(r.randint(1, 3)):
                cx_ = x + r.uniform(0.6, w - 1.2); ch = z0 + h + 1.6 * sc_
                o.append(rect(cx_, Y(ch + 1.0 * sc_), 0.9 * sc_, 1.0 * sc_, hz('#b89878', hk)))
                for p_ in range(3): o.append(rect(cx_ + 0.08 + p_ * 0.28 * sc_, Y(ch + 1.3 * sc_), 0.16 * sc_, 0.3 * sc_, hz('#c8683a', hk)))
                if r.random() < 0.06:
                    for s_ in range(4): o.append(circ(cx_ + 0.4 + s_ * 0.6, Y(ch + 1.8 + s_ * 0.9), 0.5 + s_ * 0.35, '#f0ece8', op=0.2 - s_ * 0.04))
            x += w + r.uniform(0.0, 0.4)
    job('pano_' + mode, 0, 0, W, H, 8.0, ''.join(o), transparent=True)

def notredame(name='notredame', W=60.0, H=50.0, ppd=14):
    """Notre-Dame's west front as a painted cut-out plate (W x H D, transparent around): the two square towers with their tall
    louvred lancets, the gallery of arches, the rose window, the gallery of kings, three portals; the spire and the nave roof behind;
    on the island's quay wall above the river."""
    o = []; st = '#d8ccb0'; sh = '#b4a88e'; ink = '#3a3428'
    def Y(z): return H - z
    o.append(rect(0, Y(4), W, 4, '#a89a80', stroke=ink, sw=0.1))
    o.append(poly([(10, Y(34)), (W / 2, Y(42)), (W - 10, Y(34))], '#6a7084'))
    o.append(rect(W / 2 + 6, Y(48), 1.0, 14, '#6a7084')); o.append(poly([(W / 2 + 5.4, Y(40)), (W / 2 + 6.5, Y(50)), (W / 2 + 7.6, Y(40))], '#5a6074'))
    x0, x1 = 14.0, W - 14.0; tw = 9.0
    o.append(rect(x0, Y(30), x1 - x0, 26, st, stroke=ink, sw=0.12))
    for (tx, s) in ((x0, 1), (x1 - tw, -1)):
        o.append(rect(tx, Y(44), tw, 40, st, stroke=ink, sw=0.12)); o.append(rect(tx - 0.3, Y(44.6), tw + 0.6, 0.6, sh, stroke=ink, sw=0.08))
        for k in range(2):
            lx = tx + 1.4 + k * 3.4
            o.append(path(f'M{_c(lx)},{_c(Y(31))} L{_c(lx)},{_c(Y(40))} Q{_c(lx + 1.1)},{_c(Y(42.4))} {_c(lx + 2.2)},{_c(Y(40))} L{_c(lx + 2.2)},{_c(Y(31))} Z', '#3a3a48', stroke=ink, sw=0.08))
            for j in range(6): o.append(line(lx + 0.1, Y(32 + j * 1.3), lx + 2.1, Y(32.5 + j * 1.3), sh, 0.12))
        for k in range(int(tw / 0.6)): o.append(rect(tx + k * 0.6, Y(44.6 + 0.6), 0.35, 0.6, sh))
    o.append(rect(x0, Y(30.5), x1 - x0, 0.6, sh))
    for k in range(int((x1 - x0) / 1.2)):
        ax = x0 + 0.3 + k * 1.2; o.append(path(f'M{_c(ax)},{_c(Y(26.5))} L{_c(ax)},{_c(Y(29.4))} Q{_c(ax + 0.45)},{_c(Y(30.2))} {_c(ax + 0.9)},{_c(Y(29.4))} L{_c(ax + 0.9)},{_c(Y(26.5))} Z', '#4a4a58'))
    o.append(rect(x0, Y(26.5), x1 - x0, 0.5, sh))
    cx = W / 2; o.append(circ(cx, Y(20.5), 5.0, sh, stroke=ink, sw=0.12)); o.append(circ(cx, Y(20.5), 4.3, '#3a3e5a'))
    for k in range(16):
        a = 2 * math.pi * k / 16; o.append(line(cx, Y(20.5), cx + 4.3 * math.cos(a), Y(20.5) - 4.3 * math.sin(a), sh, 0.18))
    o.append(circ(cx, Y(20.5), 1.4, sh)); o.append(circ(cx, Y(20.5), 2.8, 'none', stroke=sh, sw=0.15))
    for tx in (x0 + tw / 2, x1 - tw / 2):
        o.append(path(f'M{_c(tx - 1.6)},{_c(Y(15))} L{_c(tx - 1.6)},{_c(Y(22))} Q{_c(tx)},{_c(Y(24.5))} {_c(tx + 1.6)},{_c(Y(22))} L{_c(tx + 1.6)},{_c(Y(15))} Z', '#3a3a48', stroke=ink, sw=0.08))
    o.append(rect(x0, Y(14.6), x1 - x0, 1.6, sh))
    for k in range(28): o.append(rect(x0 + 0.4 + k * (x1 - x0 - 0.8) / 28, Y(14.4), 0.5, 1.2, '#8a8270'))
    for (px, pw) in ((x0 + tw / 2, 5.2), (cx, 6.0), (x1 - tw / 2, 5.2)):
        for k in range(3):
            w_ = pw - k * 1.0; o.append(path(f'M{_c(px - w_ / 2)},{_c(Y(4))} L{_c(px - w_ / 2)},{_c(Y(9))} Q{_c(px)},{_c(Y(13 - k * 0.8))} {_c(px + w_ / 2)},{_c(Y(9))} L{_c(px + w_ / 2)},{_c(Y(4))} Z', [sh, '#8a8270', '#3a3a48'][k], stroke=ink, sw=0.08))
    for (bx, bw_) in ((x0 - 0.5, 1.0), (x0 + tw - 0.5, 1.0), (x1 - tw - 0.5, 1.0), (x1 - 0.5, 1.0)):
        o.append(rect(bx, Y(30), bw_, 26, sh))
    o.append(rect(0, Y(4), W, 0.6, '#8a7c66'))
    job(name, 0, 0, W, H, ppd, ''.join(o), transparent=True)

def seine(name='seine', W=4.0, H=4.0, ppd=48):
    r = random.Random(61); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#4a6a78')]
    for _ in range(60):
        x, y = r.uniform(0, W), r.uniform(0, H); w = r.uniform(0.2, 0.7)
        for xx in _wrap(x, W, w): o.append(ell(xx + w / 2, y, w / 2, 0.025, r.choice(('#8ab0c0', '#2e4a58', '#f0d8b0')), op=0.6))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def paving(name='pave', W=4.0, H=4.0, ppd=64):
    """Pavement (sidewalk) 4 x 4 D: large grey-buff stone slabs with a granite kerb row along v 0."""
    r = random.Random(71); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#6a6458')]
    for j in range(4):
        for i in range(5):
            c = mul(r.choice(('#b8b0a0', '#aca494', '#c0b8a6')), r.uniform(0.95, 1.05)); o.append(rect(i * 0.8 + 0.02, j * 1.0 + 0.02, 0.76, 0.96, c, stroke='#4a4438', sw=0.008))
            if r.random() < 0.3: o.append(ell(i * 0.8 + 0.4, j + 0.5, 0.2, 0.08, '#8a8270', op=0.3))
    job(name, 0, 0, W, H, ppd, ''.join(o))

# ============================================================================= the attic room and the dealer's shop
def wallpaper(name='wallpaper', W=1.2, H=1.2, ppd=128, base='#e0cfa4', stripe='#c8b080', rose='#b8584a', leaf='#6a8a5a', stain=0.35, seed=81):
    """Cheap faded wallpaper 1.2 x 1.2 D: cream with narrow stripes, little rose sprigs, water stains and a torn seam."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, base)]
    for k in range(6): o.append(rect(k * 0.2 + 0.08, -0.1, 0.03, H + 0.2, stripe, op=0.7))
    for (x, y) in ((0.1, 0.15), (0.3, 0.75), (0.5, 0.15), (0.7, 0.75), (0.9, 0.15), (1.1, 0.75)):
        o.append(circ(x, y, 0.045, rose)); o.append(circ(x, y, 0.022, mul(rose, 1.3)))
        o.append(ell(x - 0.05, y + 0.05, 0.03, 0.015, leaf)); o.append(ell(x + 0.05, y + 0.05, 0.03, 0.015, leaf))
    if stain:
        for _ in range(3):
            x, y = r.uniform(0, W), r.uniform(0, H); rx = r.uniform(0.15, 0.4)
            o.append(ell(x, y, rx, rx * 1.6, '#a88a5a', op=stain * 0.3))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def quilt(name='quilt', W=2.0, H=2.0, ppd=96):
    r = random.Random(91); o = []
    cols = ('#a83a2e', '#c8a060', '#3a5a8a', '#e8dcc0', '#5a7a4a', '#8a4a6a', '#d8c090')
    for i in range(8):
        for j in range(8):
            c = r.choice(cols); o.append(rect(i * 0.25, j * 0.25, 0.25, 0.25, c, stroke='#3a2a20', sw=0.008))
            if r.random() < 0.3: o.append(circ(i * 0.25 + 0.125, j * 0.25 + 0.125, 0.06, mix(c, '#ffffff', 0.4)))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def trunk(name='trunk', W=2.0, H=1.0, ppd=128):
    """Wooden travelling trunk wrap 2 x 1 D: stained boards, iron corner caps and two bands, rivets, a lock hasp, a luggage label."""
    r = random.Random(101); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#6a4224')]
    for k in range(5): c = mul('#7a4e2a', r.uniform(0.85, 1.1)); o.append(rect(-0.1, k * 0.2 + 0.01, W + 0.2, 0.18, c))
    for x in (0.0, 0.4, 1.6, W - 0.06):
        o.append(rect(x, -0.1, 0.07, H + 0.2, '#3a3436', stroke='#1a1a1a', sw=0.006))
        for k in range(8): o.append(circ(x + 0.035, 0.06 + k * 0.12, 0.012, '#8a8890'))
    o.append(rect(0.95, 0.0, 0.12, 0.2, '#b8903a', stroke='#3a2a10', sw=0.008))
    o.append(rect(1.2, 0.45, 0.28, 0.17, '#e8dcc0', stroke='#5a4a30', sw=0.006, rx=0.01)); o.append(_txt(1.34, 0.56, 'V.P.', 0.07, '#3a2a1a'))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def florence(name='florence', W=12.0, H=6.0, ppd=40):
    """Florence through the dealer's window: terracotta roofs, Brunelleschi's dome with its white ribs and lantern, Giotto's tower,
    the Palazzo Vecchio tower, cypresses and the hills of Fiesole; warm afternoon."""
    o = [rect(0, 0, W, H, '#f0dca8')]
    d = '<linearGradient id="fs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7aa0c8"/><stop offset="1" stop-color="#f4dca8"/></linearGradient>'
    o.append(rect(0, 0, W, H * 0.7, 'url(#fs)'))
    o.append(path(f'M0,{_c(H * 0.55)} Q3,{_c(H * 0.42)} 6,{_c(H * 0.5)} T12,{_c(H * 0.46)} L12,{_c(H)} L0,{_c(H)} Z', '#9aa88a'))
    cx = W * 0.45; base = H * 0.62
    o.append(rect(cx - 1.4, base - 0.8, 2.8, 0.8, '#e8dcc4', stroke=INK, sw=0.02))
    o.append(path(f'M{_c(cx - 1.3)},{_c(base - 0.8)} Q{_c(cx - 1.25)},{_c(base - 2.6)} {_c(cx)},{_c(base - 2.9)} Q{_c(cx + 1.25)},{_c(base - 2.6)} {_c(cx + 1.3)},{_c(base - 0.8)} Z', '#c8643a', stroke=INK, sw=0.025))
    for k in (-0.8, -0.3, 0.3, 0.8): o.append(path(f'M{_c(cx + k * 1.3)},{_c(base - 0.8)} Q{_c(cx + k * 1.1)},{_c(base - 2.3)} {_c(cx)},{_c(base - 2.85)}', 'none', stroke='#f4ecdc', sw=0.06))
    o.append(rect(cx - 0.15, base - 3.4, 0.3, 0.5, '#f4ecdc', stroke=INK, sw=0.015)); o.append(poly([(cx - 0.15, base - 3.4), (cx, base - 3.7), (cx + 0.15, base - 3.4)], '#c8a040'))
    tx = cx + 1.9; o.append(rect(tx, base - 3.2, 0.45, 3.2, '#ece4d4', stroke=INK, sw=0.02))
    for k in range(4): o.append(rect(tx + 0.1, base - 2.9 + k * 0.7, 0.25, 0.35, '#c88a8a', op=0.7))
    px = W * 0.75; o.append(rect(px - 1.0, base - 1.2, 2.0, 1.2, '#c8a87a', stroke=INK, sw=0.02)); o.append(rect(px - 0.18, base - 3.4, 0.36, 2.2, '#c8a87a', stroke=INK, sw=0.02))
    for k in range(5): o.append(rect(px - 1.0 + k * 0.42, base - 1.32, 0.25, 0.14, '#c8a87a'))
    import random as _r
    r = _r.Random(111); x = -0.2
    while x < W:
        w = r.uniform(0.8, 1.6); h = r.uniform(0.6, 1.2); z = H * 0.7 + r.uniform(-0.2, 0.3)
        o.append(rect(x, z - h, w, h + 2, r.choice(('#ecd8b0', '#e8c890', '#f0e0c4', '#e0b888')), stroke=INK, sw=0.015))
        o.append(poly([(x - 0.1, z - h), (x + w / 2, z - h - 0.3), (x + w + 0.1, z - h)], r.choice(('#c8643a', '#b8583a', '#d07048')), stroke=INK, sw=0.015))
        for k in range(int(w / 0.4)): o.append(rect(x + 0.12 + k * 0.4, z - h + 0.25, 0.16, 0.25, '#5a4a3a'))
        x += w
    for k in range(5):
        x = r.uniform(0, W); o.append(ell(x, H * 0.5, 0.12, 0.6, '#3a5a2a'))
    job(name, 0, 0, W, H, ppd, ''.join(o), defs=d)

def glint(name='glint', W=1.0, H=1.0, ppd=96):
    """Glass sheen 1 x 1 D (transparent): two soft diagonal white streaks and a faint overall veil (picture glass, windows)."""
    d = '<filter id="b"><feGaussianBlur stdDeviation="0.02"/></filter>'
    o = [rect(0, 0, W, H, '#ffffff', op=0.08)]
    o.append(poly([(0.15, 1.0), (0.42, 1.0), (0.95, 0.0), (0.68, 0.0)], '#ffffff', op=0.55, extra=' filter="url(#b)"'))
    o.append(poly([(0.48, 1.0), (0.56, 1.0), (1.0, 0.18), (1.0, 0.03)], '#ffffff', op=0.4, extra=' filter="url(#b)"'))
    job(name, 0, 0, W, H, ppd, ''.join(o), transparent=True)

# ============================================================================= registry
MODES = ('day', 'dusk')
def all_jobs():
    TT.JOBS.clear(); TT.SIZE.clear(); ATLAS.clear()
    mona(); plaque(); glint()
    for k, s in enumerate((11, 23, 37)): atlas('atlas%d' % k, s)
    cana()
    damask('damask_red', '#962c1c', '#b0442a', 1); damask('damask_green', '#2e4a34', '#40624a', 2); damask('damask_gold', '#a8803a', '#c09a4c', 3)
    parquet(); gold(); frieze(); coffer(); marble(); marble('marble_w', '#e4dccc', '#a8a0a0', 10); skyglass(); door_panel()
    ashlar('ashlar', '#d4bc94'); ashlar('ashlar_d', '#b09878', 22, soot=0.45); oak_door()
    BT.plaster('plaster_s', '#d8ccb0', 23, soot=0.35); BT.planks('boards', '#8c7450', 65, n=6, flour=0.0); BT.planks('shelf_w', '#8a6a44', 66, n=3)
    BT.crate('crate', 171); BT.cloth('rag', '#e8e0cc', '#8a9aa8', 182); BT.shaft('shaft'); PT.pool()
    BT.flags('flags_s', 43, flour=0.0); BT.timber('timber', '#6a4a30', 53)
    for k, (shops, st) in enumerate(((('CAF&#201; DU LOUVRE', 'TABAC', 'LIBRAIRIE'), '#e8d8b8'), (('PARFUMS', None, 'GANTERIE'), '#e2d0ac'), (('BOULANGERIE', 'VINS', None), '#ecdcc0'))):
        haussmann('haus%d' % k, 500 + k, shops=shops, stone=st, lit=0.0)
        haussmann('haus%d_n' % k, 500 + k, shops=shops, stone=st, lit=0.35)
    mansard(); BT.cobbles('cobbles', 152); paving(); seine(); notredame(); morris(); kiosk_panel()
    BT.awning('awn_cafe', '#b8282a', '#f4ead4'); BT.awning('awn_green', '#2e6a4a', '#f0e4c4')
    label_sign('sign_cafe', 'CAF&#201; DU LOUVRE', W=3.0, H=0.5); label_sign('sign_dealer', 'ANTICHIT&#192;', 'A. GERI &#183; FIRENZE', W=2.4, H=0.6, bg='#3a1e1a')
    label_sign('sign_prive', 'SERVICE', 'D&#201;FENSE D\'ENTRER', W=0.9, H=0.36, bg='#1e2a3a', fg='#e8e0c8')
    for k, (m, h) in enumerate((('LE PETIT PARISIEN', 'LA JOCONDE VOL&#201;E !'), ('LE MATIN', 'O&#217; EST LA JOCONDE ?'), ('EXCELSIOR', 'LE VOL DU LOUVRE'), ("L'&#201;CHO DE PARIS", 'MYST&#200;RE AU LOUVRE'))):
        newspaper('news%d' % k, m, h, 600 + k)
    for k, kind in enumerate(('mona', 'mona2', 'choc', 'cirque', 'velo', 'opera')): poster('poster_%s' % kind, kind, 700 + k)
    wallpaper(rose='#c06a3a'); wallpaper('wallpaper_shop', base='#3a4a34', stripe='#4a5e44', rose='#c8a040', leaf='#c8a040', stain=0.0, seed=82)
    quilt(); trunk(); florence()
    for m in MODES: sky(m); pano_paris(m)

def ensure(verbose=True):
    """Draw every texture, rasterise the changed ones (one Chromium launch), return {name: png path}."""
    os.makedirs(TEX, exist_ok=True); os.makedirs(WORK, exist_ok=True)
    all_jobs()
    mpath = os.path.join(TEX, 'manifest.json'); man = json.load(open(mpath)) if os.path.exists(mpath) else {}
    todo = []; out = {}
    for name, j in TT.JOBS.items():
        h = hashlib.sha1((j['svg'] + str(j['transparent'])).encode()).hexdigest(); png = os.path.join(TEX, name + '.png'); out[name] = png
        if man.get(name) != h or not os.path.exists(png):
            sp = os.path.join(WORK, 'tex_' + name + '.svg'); open(sp, 'w').write(j['svg'])
            todo.append(dict(src=sp, out=png, w=j['w'], h=j['h'], transparent=j['transparent'])); man[name] = h
    if todo:
        jp = os.path.join(WORK, 'tex_jobs.json'); json.dump(todo, open(jp, 'w'))
        r = subprocess.run(['node', RASTER, jp], env=dict(os.environ, NODE_PATH=os.environ.get('NODE_PATH', '/opt/node22/lib/node_modules')), capture_output=True, text=True)
        if r.returncode != 0: raise RuntimeError('texture raster failed: ' + r.stderr[-2000:])
        if verbose: print('textures rasterised:', ', '.join(os.path.basename(t['out']) for t in todo))
        json.dump(man, open(mpath, 'w'), indent=0, sort_keys=True)
    return out

if __name__ == '__main__':
    p = ensure(); print(json.dumps({k: (os.path.basename(v), SIZE[k]) for k, v in p.items()}, indent=0))

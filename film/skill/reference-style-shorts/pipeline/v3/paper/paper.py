#!/usr/bin/env python3
"""paper.py : the shared paper and text artwork of the film (build-order step 3 of plan/shot_plan.md).

Every item is a function that returns a complete SVG document (drawn in D units with the v2 office
helpers, v2/sets/office.py, imported read-only) and is rasterised by headless Chromium (raster.js,
Playwright) into tex/. Thai only from local font files (Kanit, Loma), embedded as @font-face.

    import paper as P
    P.build()                         # rasterise every item whose SVG changed (cache: tex/manifest.json)
    P.REGISTRY['nickname_label']      # {'svg': fn, 'png': path, 'size_D': (w, h), 'px': (W, H), 'kind': ..., 'note': ...}
    P.REGISTRY['newspaper_bleed']['frames']   # 12 png paths (kind 'sequence'; svg(frame=k))

CLI:  python3 paper.py [build|sheet|crops|all] [--force]
Conventions: texture y runs down; (0, 0) is the top-left corner of the item; size_D is the size the
PNG must have in the scene (map it 1:1 onto a quad of that size). Transparent PNGs carry alpha.
"""
import os, sys, json, math, random, base64, subprocess, unicodedata, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(PROJ, 'v2', 'sets'))
import office as O                                             # noqa: E402  (v2 drawing helpers + palette, read only)

TEX = os.path.join(HERE, 'tex'); TMP = os.path.join(HERE, 'tmp')
K = O.K
rect, line, poly, pline, circ, ell, path, text, grp, rot, pd, greek, fit, mul, mix = (O.rect, O.line, O.poly, O.pline, O.circ, O.ell, O.path,
                                                                                   O.text, O.grp, O.rot, O.pd, O.greek, O.fit, O.mul, O.mix)
n = O.n

# ----------------------------------------------------------------------------- palette (LOOK_SPEC 3.4, environment_materials 3.7)
PAPER = '#fff5df'          # cream paper
PRINT = '#836d4e'          # printed ink (brown-grey, never black)
PRINT_D = O.PRINT_D        # '#574430' same ink, darker (small lettering, typed words)
INK = O.INK                # '#2a1712' object outline of the office set
RED = '#b61d32'            # print red / stamp red
RED_T = O.RED              # '#c8301c' red of the track (underline on the label)
BRUSH = '#a32413'          # red-brown brush lettering of the label
NAVY = '#081148'
CREAM = '#f3d9a8'          # cream lettering on colour
GREY = '#9a8f86'           # greeked filler on calendar paper
SLAB = O.SLAB              # DejaVu Serif Bold (slab-like capitals, the office sign's face)
OLD = "'Liberation Serif','DejaVu Serif',serif"               # mixed-case old-style masthead
MONO = "'Liberation Mono','FreeMono','DejaVu Sans Mono',monospace"   # teletype

# ----------------------------------------------------------------------------- local fonts (Thai), embedded
FONT_FILES = {
    'PKanit': os.path.join(PROJ, 'fonts', 'th', 'Kanit_800ExtraBold.ttf'),
    'PKanitBlack': os.path.join(PROJ, 'fonts', 'th', 'Kanit_900Black.ttf'),
    'PLoma': '/usr/share/fonts/opentype/tlwg/Loma-Bold.otf',
}
_USED = set(); _B64 = {}; _MET = {}

def _font_css(names):
    css = []
    for nm in sorted(names):
        p = FONT_FILES[nm]
        if not os.path.exists(p):
            raise FileNotFoundError(f'{p}: font {nm} missing (the skill ships fonts/th/Kanit_*.ttf; Loma-Bold.otf comes from the fonts-tlwg-loma-otf package). Run scripts/check_env.sh <project_dir>')
        if nm not in _B64: _B64[nm] = base64.b64encode(open(p, 'rb').read()).decode()
        fmt = 'opentype' if p.endswith('.otf') else 'truetype'
        css.append(f"@font-face{{font-family:'{nm}';src:url(data:font/{'otf' if fmt == 'opentype' else 'ttf'};base64,{_B64[nm]}) format('{fmt}');}}")
    return ''.join(css)

def adv(s, fam):
    """Advance width of s in em (cmap + hmtx; Thai marks have zero advance in both fonts)."""
    if fam not in _MET:
        from fontTools.ttLib import TTFont
        f = TTFont(FONT_FILES[fam]); _MET[fam] = (f.getBestCmap(), f['hmtx'], f['head'].unitsPerEm)
    cm, hm, upm = _MET[fam]
    return sum(hm[cm[ord(c)]][0] for c in s if ord(c) in cm) / upm

def th(x, y, s, size, fill, fam='PKanit', anchor='middle', extra=''):
    """Thai text from a local font (the browser shapes it: marks stay inside one <text>)."""
    _USED.add(fam); return text(x, y, s, size, fill, font=f"'{fam}'", weight='normal', anchor=anchor, extra=extra)

def clusters(s):
    """Thai grapheme clusters: a base letter plus its combining marks (above and below vowels, tone marks)."""
    out = []
    for c in s:
        if out and unicodedata.category(c) == 'Mn': out[-1] += c
        else: out.append(c)
    return out

# ----------------------------------------------------------------------------- documents and filters
def doc(w, h, long_px, body, defs='', bg=None):
    """Complete SVG document of a w x h D item at long_px pixels on its long side (viewBox in v2 units, 100 per D)."""
    ppd = long_px / max(w, h); W, H = int(round(w * ppd)), int(round(h * ppd))
    css = _font_css(_USED); _USED.clear()
    b = f'<rect x="0" y="0" width="{w * K:g}" height="{h * K:g}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {w * K:g} {h * K:g}" preserveAspectRatio="none" '
            f'style="display:block"><defs><style>{css}</style>{defs}</defs>{b}{body}</svg>')

def f_rough(fid, w, h, disp=0.35, freq=0.9, seed=1, speck=0.0, sfreq=1.2, st=0.62, streak=0.0, octv=2):
    """Ink roughening: wobbly edges (displacement), optional speckle voids and dry-brush streaks (alpha reduced)."""
    s = (f'<filter id="{fid}" filterUnits="userSpaceOnUse" x="{-0.1 * w * K:g}" y="{-0.1 * h * K:g}" width="{1.2 * w * K:g}" height="{1.2 * h * K:g}" '
         f'color-interpolation-filters="sRGB"><feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="{octv}" seed="{seed}" result="n"/>'
         f'<feDisplacementMap in="SourceGraphic" in2="n" scale="{disp}" xChannelSelector="R" yChannelSelector="G" result="d"/>')
    last = 'd'
    for j, (amt, bf) in enumerate(((speck, f'{sfreq}'), (streak, f'{freq * 0.05:.4f} {freq * 1.6:.4f}'))):
        if amt <= 0: continue
        k = 9.0; row = f'{k} 0 0 0 {-k * st:.3f}'
        s += (f'<feTurbulence type="fractalNoise" baseFrequency="{bf}" numOctaves="2" seed="{seed + 7 + j}" result="t{j}"/>'
              f'<feColorMatrix in="t{j}" type="matrix" values="{row} {row} {row} {row}" result="m{j}"/>'
              f'<feComposite in="{last}" in2="m{j}" operator="arithmetic" k1="{-amt}" k2="1" k3="0" k4="0" result="o{j}"/>')
        last = f'o{j}'
    return s + '</filter>'

def f_grain(fid, w, h, freq=0.55, seed=5, col=(0.35, 0.25, 0.12)):
    """Paper fibre noise (brown, alpha only where the noise is bright); lay it at low opacity over the paper."""
    r, g, b = col
    return (f'<filter id="{fid}" filterUnits="userSpaceOnUse" x="0" y="0" width="{w * K:g}" height="{h * K:g}"><feTurbulence type="fractalNoise" '
            f'baseFrequency="{freq}" numOctaves="3" seed="{seed}"/><feColorMatrix type="matrix" values="0 0 0 0 {r} 0 0 0 0 {g} 0 0 0 0 {b} 1.6 0 0 0 -0.72"/></filter>')

def grain(u, w, h, clip=None, a=0.16, a2=0.07):
    c = f' clip-path="url(#{clip})"' if clip else ''
    return (f'<g{c}><rect x="0" y="0" width="{w * K:g}" height="{h * K:g}" filter="url(#{u}gr)" opacity="{a}"/>'
            f'<rect x="0" y="0" width="{w * K:g}" height="{h * K:g}" filter="url(#{u}gr2)" opacity="{a2}"/></g>')

def grain_defs(u, w, h):
    return f_grain(u + 'gr', w, h, 0.55, 5) + f_grain(u + 'gr2', w, h, 0.035, 9, (0.45, 0.32, 0.18))

def ptsd(pts, close=True):
    return 'M ' + ' L '.join(f'{n(x)} {n(y)}' for x, y in pts) + (' Z' if close else '')

def wobbly_rect(x, y, w, h, r, amp=0.003, step=0.05, torn_bottom=0.0):
    """Hand-cut paper outline; torn_bottom > 0 gives a ragged (torn-off) bottom edge of that tooth depth."""
    pts = []
    def edge(a, b, jag=0.0, st=step):
        L = math.hypot(b[0] - a[0], b[1] - a[1]); m = max(1, int(L / st))
        nx, ny = (b[1] - a[1]) / L, -(b[0] - a[0]) / L
        for i in range(m):
            t = i / m; d = r.uniform(-amp, amp) + (r.uniform(-jag, jag * 0.4) if jag else 0)
            pts.append((a[0] + (b[0] - a[0]) * t + nx * d, a[1] + (b[1] - a[1]) * t + ny * d))
    P = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    edge(P[0], P[1]); edge(P[1], P[2])
    edge(P[2], P[3], torn_bottom, 0.014 if torn_bottom else step); edge(P[3], P[0])
    return pts

def tapered(pts, w0, w1, wm):
    """Brush stroke polygon along a polyline: width w0 at start, wm in the middle, w1 at the end."""
    L = [0.0]
    for a, b in zip(pts[:-1], pts[1:]): L.append(L[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    left, right = [], []
    for i, p in enumerate(pts):
        a, b = pts[max(0, i - 1)], pts[min(len(pts) - 1, i + 1)]; dx, dy = b[0] - a[0], b[1] - a[1]; q = math.hypot(dx, dy) or 1
        t = L[i] / L[-1]; wd = (w0 + (wm - w0) * t * 2) if t < 0.5 else (wm + (w1 - wm) * (t - 0.5) * 2)
        left.append((p[0] - dy / q * wd / 2, p[1] + dx / q * wd / 2)); right.append((p[0] + dy / q * wd / 2, p[1] - dx / q * wd / 2))
    return left + right[::-1]

def tgreek(x, y, w, col, sw, r, gap=0.45):
    """A typed line seen too small to read: short word blocks with spaces (teletype filler)."""
    return greek(x, y, w, col, sw, r, gap=gap)

# ----------------------------------------------------------------------------- the rubber stamp (Thai 'ทางการ' or English 'OFFICIAL')
def stamp_group(cx, cy, R, uid, lang='th', angle=-13, mirror=False, colour=RED):
    """Round stamp impression: double ring, tiny ring text (filler), centre word between two bars. Ink-rough."""
    pid = uid + 'ring'; rr = R * 0.86
    ring = (f'<path id="{pid}" d="M {n(cx - rr)} {n(cy)} A {n(rr)} {n(rr)} 0 1 1 {n(cx + rr)} {n(cy)} A {n(rr)} {n(rr)} 0 1 1 {n(cx - rr)} {n(cy)}" fill="none"/>')
    o = [ring, circ(cx, cy, R, 'none', stroke=colour, sw=R * 0.075), circ(cx, cy, R * 0.72, 'none', stroke=colour, sw=R * 0.03)]
    o.append(f'<text font-family="{SLAB}" font-weight="bold" font-size="{n(R * 0.15)}" fill="{colour}" letter-spacing="{n(R * 0.02)}">'
             f'<textPath href="#{pid}" startOffset="0" textLength="{2 * math.pi * rr * K * 0.985:.1f}" lengthAdjust="spacing">'
             f'U.S. WEATHER BUREAU ★ WASHINGTON D.C. ★</textPath></text>')
    o.append(line(cx - R * 0.5, cy - R * 0.33, cx + R * 0.5, cy - R * 0.33, colour, R * 0.045)); o.append(line(cx - R * 0.5, cy + R * 0.36, cx + R * 0.5, cy + R * 0.36, colour, R * 0.045))
    if lang == 'th':
        w = adv('ทางการ', 'PKanit'); s = R * 1.22 / w
        o.append(th(cx, cy + s * 0.27, 'ทางการ', s, colour))
    else:
        o.append(text(cx, cy + R * 0.11, 'OFFICIAL', R * 0.3, colour, font=SLAB, extra=fit(R * 1.18)))
    for sx in (-1, 1): o.append(text(cx + sx * R * 0.47, cy + R * 0.6, '★', R * 0.16, colour, font=SLAB))
    o.append(text(cx, cy + R * 0.62, '20 SEP 1938', R * 0.13, colour, font=SLAB, extra=fit(R * 0.62)))
    tr = f'rotate({angle} {n(cx)} {n(cy)})' + (f' translate({n(2 * cx)} 0) scale(-1 1)' if mirror else '')
    return f'<g transform="{tr}"><g filter="url(#{uid}f)" opacity="0.9">' + ''.join(o) + '</g></g>'

def stamp_defs(uid, w, h):
    return f_rough(uid + 'f', w, h, disp=0.5, freq=0.7, seed=4, speck=0.75, sfreq=0.9, st=0.6)

# ----------------------------------------------------------------------------- 1. the official forecast sheet (shot 14; teletype sheet; chief's paper)
FS_W, FS_H = 1.08, 1.4
FS_WORDS = {'th': ('ฝนตก', 'ลมกระโชก'), 'en': ('RAIN,', 'GUSTY WINDS')}
FS_WORD_Y = (0.70, 0.95)            # baselines of the two big typed lines (D from the top)
FS_STAMP = (0.855, 0.215, 0.135)    # centre x, y and radius of the stamp (on the header block, right of its text)

def _fs_word(lang, i, u):
    w = FS_WORDS[lang][i]; y = FS_WORD_Y[i]; cx = FS_W / 2
    if lang == 'th':
        s = 0.27 if i == 0 else 0.26; wd = adv(w, 'PLoma') * s; sx = min(1.0, 0.94 / wd)
        t = th(cx, y, w, s, PRINT_D, 'PLoma')
    else:
        s = 0.21 if i == 0 else 0.16; wd = 0.6 * s * len(w); sx = min(1.0, 0.94 / wd)
        t = text(cx, y, w, s, PRINT_D, font=MONO)
    return f'<g transform="translate({n(cx)} 0) scale({sx:.3f} 1) translate({n(-cx)} 0)"><g filter="url(#{u}ty)">{t}</g></g>'

def forecast_svg(lang='th', words=2, stamp=True, torn=True, paper=True, only=None, long_px=2048):
    """Teletype forecast sheet 1.08 x 1.4 D. lang 'th' (plan: typed Thai 'ฝนตก' / 'ลมกระโชก', Thai stamp 'ทางการ')
    or 'en' ('RAIN,' / 'GUSTY WINDS', stamp 'OFFICIAL'). words = how many of the two big lines are typed (0, 1, 2);
    stamp = stamp impression on the header; torn = ragged bottom edge (torn off the roll at 29.95);
    only = 'word1' | 'word2' | 'stamp' draws just that layer on a transparent sheet (pop / bloom overlays, same frame)."""
    u = 'fs'; r = random.Random(31); W, H = FS_W, FS_H; o = []
    defs = grain_defs(u, W, H) + f_rough(u + 'ty', W, H, disp=0.32, freq=0.95, seed=2, speck=0.35, sfreq=1.6, st=0.66) + stamp_defs(u + 'st', W, H)
    defs += f_rough(u + 'tl', W, H, disp=0.18, freq=1.2, seed=3, speck=0.25, sfreq=2.0, st=0.68)
    if only:
        if only == 'word1': o.append(_fs_word(lang, 0, u))
        elif only == 'word2': o.append(_fs_word(lang, 1, u))
        elif only == 'stamp': o.append(stamp_group(*FS_STAMP, u + 'st', lang))
        return doc(W, H, long_px, ''.join(o), defs)
    outline = wobbly_rect(0.012, 0.012, W - 0.024, H - 0.03, r, amp=0.0015, torn_bottom=0.016 if torn else 0.0)
    defs += f'<clipPath id="{u}clip"><path d="{ptsd(outline)}"/></clipPath>'
    o.append(path(ptsd(outline), PAPER, stroke=None, sw=0))
    if paper: o.append(grain(u, W, H, u + 'clip'))
    b = []
    # ruled frame
    b.append(rect(0.045, 0.045, W - 0.09, H - 0.11, 'none', stroke=PRINT, sw=0.005)); b.append(rect(0.058, 0.058, W - 0.116, H - 0.136, 'none', stroke=PRINT, sw=0.0022))
    # tiny corner capitals (filler) and the header
    b.append(tgreek(0.09, 0.098, 0.2, PRINT, 0.009, r, 0.6)); b.append(tgreek(W - 0.29, 0.098, 0.2, PRINT, 0.009, r, 0.6))
    b.append(text(0.09, 0.19, 'U.S. WEATHER BUREAU', 0.08, PRINT_D, font=SLAB, anchor='start', ls=0.006, extra=fit(0.6)))
    b.append(line(0.09, 0.218, W - 0.09, 0.218, PRINT, 0.007)); b.append(line(0.09, 0.231, W - 0.09, 0.231, PRINT, 0.0025))
    mono = text(0.09, 0.277, 'OFFICIAL FORECAST', 0.044, PRINT_D, font=MONO, anchor='start') + text(0.09, 0.325, 'SEPT. 20, 1938', 0.044, PRINT_D, font=MONO, anchor='start')
    b.append(f'<g filter="url(#{u}tl)">' + mono + '</g>')
    b.append(line(0.09, 0.352, W - 0.09, 0.352, PRINT, 0.0025))
    tl = [tgreek(0.1, 0.395 + j * 0.042, W - 0.2 - r.uniform(0, 0.25), PRINT, 0.011, r) for j in range(3)]
    tl += [tgreek(0.1, 1.06 + j * 0.045, W - 0.2 - r.uniform(0, 0.3), PRINT, 0.011, r) for j in range(4)]
    b.append(f'<g filter="url(#{u}tl)" opacity="0.85">' + ''.join(tl) + '</g>')
    # sign-off: a short rule and the forecaster's initials as greek
    b.append(line(W - 0.42, 1.3, W - 0.12, 1.3, PRINT, 0.003)); b.append(tgreek(W - 0.4, 1.27, 0.2, PRINT, 0.01, r))
    o.append(f'<g clip-path="url(#{u}clip)">' + ''.join(b) + '</g>')
    for i in range(words): o.append(_fs_word(lang, i, u))
    if stamp: o.append(stamp_group(*FS_STAMP, u + 'st', lang))
    o.append(path(ptsd(outline), 'none', stroke=INK, sw=0.0045))
    return doc(W, H, long_px, ''.join(o), defs)

# ----------------------------------------------------------------------------- 2. the nickname label 'ทางด่วนพายุ' (shots 13, 17, 18, 19-22, 25)
LB_W, LB_H = 1.15, 0.34
LB_TEXT = 'ทางด่วนพายุ'
LB_PIN = (0.50, 0.045)               # where the red pin goes (D from the top-left): clear of the lettering

def label_svg(long_px=2400, seed=7):
    """Cream paper strip 1.15 x 0.34 D, hand-lettered in red-brown brush (Kanit ExtraBold, per-cluster jitter,
    brush roughening), red brush underline, a small doodled road with an up arrow at the right end."""
    u = 'lb'; r = random.Random(seed); W, H = LB_W, LB_H; o = []
    defs = grain_defs(u, W, H) + f_rough(u + 'br', W, H, disp=0.55, freq=0.55, seed=11, speck=0.3, sfreq=1.1, st=0.66, streak=0.25)
    defs += f_rough(u + 'dd', W, H, disp=0.35, freq=0.8, seed=12, speck=0.2, sfreq=1.4, st=0.66)
    outline = wobbly_rect(0.012, 0.012, W - 0.024, H - 0.024, r, amp=0.0025, step=0.04)
    defs += f'<clipPath id="{u}clip"><path d="{ptsd(outline)}"/></clipPath>'
    o.append(path(ptsd(outline), PAPER, stroke=None, sw=0)); o.append(grain(u, W, H, u + 'clip', 0.2, 0.09))
    # lettering: one <text> per Thai cluster so that marks stay attached; each cluster jittered like a hand
    cl = clusters(LB_TEXT); tot = adv(LB_TEXT, 'PKanit'); x0, x1 = 0.065, 0.835; s = (x1 - x0) / tot; base = 0.232
    g = []; x = x0
    for c in cl:
        a = adv(c, 'PKanit') * s; cx = x + a / 2; dy = r.uniform(-0.007, 0.007); ang = r.uniform(-4.5, 4.5); sc = r.uniform(0.95, 1.06)
        g.append(f'<g transform="translate({n(cx)} {n(base + dy)}) rotate({ang:.2f}) scale({sc:.3f})">' + th(0, 0, c, s, BRUSH) + '</g>')
        x += a + r.uniform(-0.003, 0.004)
    o.append(f'<g filter="url(#{u}br)">' + ''.join(g) + '</g>')
    # brush underline (red, tapered, rising a little to the right)
    ul = [(0.06 + 0.78 * t, 0.278 - 0.012 * t + 0.003 * math.sin(t * 7)) for t in [i / 24 for i in range(25)]]
    o.append(f'<g filter="url(#{u}br)">' + path(ptsd(tapered(ul, 0.006, 0.004, 0.019)), RED_T, stroke=None, sw=0) + '</g>')
    # doodle: a little road running up to an arrow
    d = []; rx = 0.975
    d.append(pline([(0.895, 0.300), (rx - 0.012, 0.135)], BRUSH, 0.007)); d.append(pline([(1.06, 0.300), (rx + 0.012, 0.135)], BRUSH, 0.007))
    for k in range(4):
        ya = 0.285 - k * 0.042; yb = ya - 0.022; d.append(line(rx + (0.0 - 0.003 * k), ya, rx, yb, BRUSH, 0.0065))
    d.append(path(ptsd(tapered([(rx, 0.128), (rx, 0.06)], 0.012, 0.004, 0.011), True), BRUSH, stroke=None, sw=0))
    d.append(poly([(rx - 0.04, 0.085), (rx, 0.035), (rx + 0.04, 0.085), (rx, 0.072)], BRUSH, stroke=BRUSH, sw=0.004))
    o.append(f'<g filter="url(#{u}dd)">' + ''.join(d) + '</g>')
    o.append(path(ptsd(outline), 'none', stroke=INK, sw=0.0045))
    return doc(W, H, long_px, ''.join(o), defs)

# ----------------------------------------------------------------------------- 3. tear-off calendar (shot 4: leaf 20; shots 17, 18, 25 and the kitchen: leaf 21)
CAL_W, CAL_H = 0.66, 0.90           # whole pad = the set's calendar texture (v3/set3d textures 'calendar', calendar_rect anchor)
LEAF = (0.02, 0.02, 0.62, 0.86)     # the tear-off leaf inside the pad (x, y, w, h)
WEEKDAY = {20: 'TUESDAY', 21: 'WEDNESDAY'}   # 20 and 21 September 1938 (checked with datetime)

def _leaf(x, y, w, h, day, u):
    o = [rect(x, y, w, h, PAPER, stroke=INK, sw=0.006)]
    o.append(grain(u, CAL_W, CAL_H, u + 'lclip', 0.14, 0.06))
    hh = h * 0.25
    o.append(rect(x, y, w, hh, RED, stroke=INK, sw=0.006)); o.append(rect(x + 0.022, y + 0.022, w - 0.044, hh - 0.044, 'none', stroke=CREAM, sw=0.004))
    o.append(rect(x + 0.03, y + 0.03, w - 0.06, hh - 0.06, 'none', stroke=CREAM, sw=0.0015))
    o.append(text(x + w / 2, y + hh * 0.66, 'SEPTEMBER', 0.08, CREAM, font=SLAB, extra=fit(w - 0.13)))
    for sx in (x + w * 0.3, x + w * 0.7): o.append(circ(sx, y + 0.014, 0.013, '#3a2620', sw=0.004))
    o.append(text(x + w / 2, y + h * 0.645, str(day), 0.33, RED, font=SLAB, extra=fit(w * 0.58)))
    o.append(line(x + 0.05, y + h * 0.695, x + w - 0.05, y + h * 0.695, PRINT, 0.0035))
    o.append(text(x + w / 2, y + h * 0.795, WEEKDAY[day], 0.066, PRINT_D, font=SLAB, ls=0.004, extra=fit(w * (0.62 if day == 20 else 0.74))))
    o.append(text(x + w / 2, y + h * 0.925, '1938', 0.085, RED, font=SLAB, ls=0.006, extra=fit(w * 0.36)))
    for sx in (x + w * 0.22, x + w * 0.78): o.append(text(sx, y + h * 0.918, '★', 0.05, RED, font=SLAB))
    o.append(greek(x + 0.1, y + hh + 0.045, w - 0.2, GREY, 0.008, random.Random(day), gap=0.6))
    return ''.join(o)

def calendar_svg(day=20, part='pad', long_px=1600):
    """part 'pad': the whole tear-off pad (leaf on top, the next leaves' edges under it, dog-ear) at the set's
    calendar size 0.66 x 0.9 D; part 'leaf': the top leaf alone, 0.62 x 0.86 D (the quad that flutters)."""
    u = 'cl'; o = []
    if part == 'leaf':
        x, y, w, h = 0, 0, LEAF[2], LEAF[3]; WW, HH = w, h
    else:
        x, y, w, h = LEAF; WW, HH = CAL_W, CAL_H
        for k in (2, 1):
            o.append(rect(x + 0.006 * k, y + 0.008 * k, w, h, mul(PAPER, 1 - 0.07 * k), stroke=INK, sw=0.005))
    defs = grain_defs(u, CAL_W, CAL_H) + f'<clipPath id="{u}lclip"><rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}"/></clipPath>'
    o.append(_leaf(x, y, w, h, day, u))
    if part == 'pad':
        o.append(poly([(x + w, y + h - 0.08), (x + w, y + h), (x + w - 0.08, y + h)], mul(PAPER, 0.86), stroke=INK, sw=0.005))
    return doc(WW, HH, long_px, ''.join(o), defs)

# ----------------------------------------------------------------------------- 4. the newspaper with its weather box (shots 15, 26), plus ink-bleed frames
NP_W, NP_H = 1.5, 1.95
WB = (0.56, 1.0, 0.88, 0.84)       # weather box x, y, w, h (D)
WB_WORDS = {'th': ('พยากรณ์อากาศวันนี้', 'ฝนตก', 'ลมกระโชก'), 'en': ("TODAY'S FORECAST", 'RAIN,', 'GUSTY WINDS')}
WB_W1 = (WB[0] + WB[2] / 2, WB[1] + 0.47)     # centre x and baseline of the big word ('ฝนตก'): the ink-bleed target

def _cloud(cx, cy, s, col, sw):
    o = [path(pd('M', cx - s, cy, 'C', cx - s * 1.1, cy - s * 0.55, cx - s * 0.45, cy - s * 0.75, cx - s * 0.25, cy - s * 0.5,
                 'C', cx - s * 0.1, cy - s * 1.05, cx + s * 0.75, cy - s * 0.95, cx + s * 0.6, cy - s * 0.35,
                 'C', cx + s * 1.15, cy - s * 0.4, cx + s * 1.15, cy + s * 0.05, cx + s * 0.8, cy, 'Z'), PAPER, stroke=col, sw=sw)]
    for k in range(4): o.append(line(cx - s * 0.7 + k * s * 0.42, cy + s * 0.2, cx - s * 0.82 + k * s * 0.42, cy + s * 0.6, col, sw))
    for k in range(5): o.append(line(cx - s * 0.6 + k * s * 0.25, cy - s * 0.2, cx - s * 0.4 + k * s * 0.25, cy - s * 0.45, col, sw * 0.5))
    return ''.join(o)

def _lighthouse(x, y, w, h, col, sw, r):
    o = [rect(x, y, w, h, 'none', stroke=col, sw=sw * 1.4)]; cx = x + w * 0.58; base = y + h * 0.78
    o.append(poly([(cx - 0.05, base), (cx - 0.032, y + h * 0.25), (cx + 0.032, y + h * 0.25), (cx + 0.05, base)], 'none', stroke=col, sw=sw))
    o.append(rect(cx - 0.04, y + h * 0.18, 0.08, h * 0.07, 'none', stroke=col, sw=sw)); o.append(poly([(cx - 0.045, y + h * 0.18), (cx, y + h * 0.1), (cx + 0.045, y + h * 0.18)], 'none', stroke=col, sw=sw))
    for k in range(9): yy = y + h * 0.3 + k * h * 0.05; o.append(line(cx + 0.006, yy, cx + 0.03 + k * 0.002, yy + 0.02, col, sw * 0.5))
    for k in range(3): o.append(line(cx - 0.035 - 0.01 * k, y + h * (0.4 + 0.12 * k), cx + 0.035 + 0.01 * k, y + h * (0.4 + 0.12 * k), col, sw * 0.8))
    for a in (-1, 1): o.append(line(cx + a * 0.06, y + h * 0.21, cx + a * 0.2, y + h * (0.16 + 0.03 * a), col, sw * 0.5))
    o.append(path(pd('M', x, base, 'C', x + w * 0.3, base - h * 0.08, x + w * 0.45, base - h * 0.02, cx - 0.06, base, 'L', cx + 0.08, base, 'C', x + w * 0.8, base - h * 0.04, x + w * 0.9, base + h * 0.01, x + w, base),
                  'none', stroke=col, sw=sw))
    for k in range(7):
        yy = base + h * 0.04 + k * h * 0.028; o.append(greek(x + 0.02, yy, w - 0.04, col, sw * 0.6, r, gap=1.2))
    for k in range(6): o.append(line(x + 0.03 + k * 0.03, y + h * 0.1 + k * 0.012, x + 0.12 + k * 0.035, y + h * 0.1 + k * 0.012, col, sw * 0.4))
    return ''.join(o)

def _wb_word(lang, u, bleed=None):
    t = WB_WORDS[lang][1]; cx, by = WB_W1
    if lang == 'th': s = 0.25; inner = th(cx, by, t, s, PRINT_D, 'PLoma')
    else: s = 0.19; inner = text(cx, by, t, s, PRINT_D, font=SLAB, ls=0.01)
    return inner

def newspaper_svg(lang='th', bleed=None, long_px=2600):
    """Front page of the LONG ISLAND DAILY ('Long Island Daily', mixed-case old-style masthead), WEDNESDAY,
    SEPTEMBER 21, 1938; columns greeked; weather box (lower right, toward the lens): header 'พยากรณ์อากาศวันนี้',
    big 'ฝนตก', smaller 'ลมกระโชก' (lang 'th', the plan) or TODAY'S FORECAST / RAIN, / GUSTY WINDS (lang 'en').
    bleed = None or a frame 0..11 of the shot-26 drip: a drop lands on the big word and its ink bleeds."""
    u = 'np'; r = random.Random(44); W, H = NP_W, NP_H; o = []
    defs = grain_defs(u, W, H) + f_rough(u + 'pr', W, H, disp=0.2, freq=1.1, seed=6, speck=0.3, sfreq=1.8, st=0.67)
    defs += f_rough(u + 'ty', W, H, disp=0.25, freq=0.95, seed=8, speck=0.3, sfreq=1.6, st=0.67)
    outline = wobbly_rect(0.01, 0.01, W - 0.02, H - 0.02, r, amp=0.0012, step=0.06)
    defs += f'<clipPath id="{u}clip"><path d="{ptsd(outline)}"/></clipPath>'
    o.append(path(ptsd(outline), PAPER, stroke=None, sw=0)); o.append(grain(u, W, H, u + 'clip', 0.17, 0.08))
    b = []; M = 0.06
    b.append(tgreek(M, 0.07, 0.26, PRINT, 0.008, r, 0.6)); b.append(tgreek(W - M - 0.26, 0.07, 0.26, PRINT, 0.008, r, 0.6))
    b.append(text(W / 2, 0.245, 'Long Island Daily', 0.205, PRINT_D, font=OLD, weight='normal', extra=fit(1.30) + f' stroke="{PRINT_D}" stroke-width="{n(0.003)}"'))
    b.append(line(M, 0.29, W - M, 0.29, PRINT, 0.009)); b.append(line(M, 0.305, W - M, 0.305, PRINT, 0.003))
    b.append(text(W / 2, 0.352, 'WEDNESDAY, SEPTEMBER 21, 1938', 0.042, PRINT_D, font=SLAB, ls=0.006, extra=fit(0.86)))
    b.append(tgreek(M, 0.345, 0.2, PRINT, 0.008, r)); b.append(tgreek(W - M - 0.2, 0.345, 0.2, PRINT, 0.008, r))
    b.append(line(M, 0.375, W - M, 0.375, PRINT, 0.003)); b.append(line(M, 0.39, W - M, 0.39, PRINT, 0.009))
    # headline: two heavy lines, too broken up to read (the plan greeks every column)
    for j, yy in enumerate((0.455, 0.54)):
        x = M + 0.02 + (0.05 if j else 0); end = W - M - 0.02 - (0.05 if j else 0)
        while x < end - 0.05:
            L = min(r.uniform(0.12, 0.3), end - x); xl = x
            while xl < x + L - 0.02:                      # heavy capitals as letter blocks: reads as type, not as a bar
                lw = r.uniform(0.026, 0.04); b.append(rect(xl, yy - 0.056, lw, 0.056, PRINT, stroke=None, sw=0, extra='opacity="0.8"')); xl += lw + 0.008
            x = xl + 0.04
    b.append(line(M, 0.585, W - M, 0.585, PRINT, 0.003))
    # four columns of greeked type, an engraving in the top left, the weather box lower right
    cols = 4; gut = 0.03; cw = (W - 2 * M - gut * (cols - 1)) / cols; y0 = 0.62
    pic = (M, y0, 2 * cw + gut, 0.42); box = (WB[0] - 0.025, WB[1] - 0.025, WB[2] + 0.05, WB[3] + 0.05)
    b.append(_lighthouse(*pic, PRINT, 0.005, r))
    b.append(text(M + (2 * cw + gut) / 2, y0 + 0.47, '', 0.03, PRINT))
    b.append(tgreek(M + 0.05, y0 + 0.465, 2 * cw + gut - 0.1, PRINT, 0.0085, r))
    for c in range(cols):
        cx0 = M + c * (cw + gut)
        if c: b.append(line(cx0 - gut / 2, y0, cx0 - gut / 2, H - 0.06, PRINT, 0.0018))
        yy = y0 + 0.02
        b.append(rect(cx0 + 0.03, yy - 0.012, cw - 0.06, 0.022, PRINT, stroke=None, sw=0, extra='opacity="0.7"')); yy += 0.045
        while yy < H - 0.07:
            inpic = cx0 < pic[0] + pic[2] and yy < pic[1] + pic[3] + 0.08
            inbox = cx0 + cw > box[0] and yy > box[1] - 0.02 and yy < box[1] + box[3] + 0.02
            if not inpic and not inbox:
                ind = 0.02 if r.random() < 0.08 else 0.0
                b.append(tgreek(cx0 + ind, yy, cw - ind - (r.uniform(0.05, 0.2) if r.random() < 0.12 else 0), PRINT, 0.0075, r, 0.5))
            yy += 0.028
    o.append(f'<g clip-path="url(#{u}clip)"><g filter="url(#{u}pr)">' + ''.join(b) + '</g></g>')
    # weather box
    x, y, w, h = WB; hd, w1, w2 = WB_WORDS[lang]; wb = []
    wb.append(rect(x - 0.025, y - 0.025, w + 0.05, h + 0.05, PAPER, stroke=None, sw=0))
    wb.append(rect(x, y, w, h, 'none', stroke=PRINT_D, sw=0.009)); wb.append(rect(x + 0.016, y + 0.016, w - 0.032, h - 0.032, 'none', stroke=PRINT_D, sw=0.003))
    if lang == 'th':
        s = min(0.1, (w - 0.24) / adv(hd, 'PKanit')); wb.append(th(x + w / 2 + 0.06, y + 0.135, hd, s, PRINT_D, 'PKanit'))
    else:
        wb.append(text(x + w / 2 + 0.06, y + 0.128, hd, 0.07, PRINT_D, font=SLAB, ls=0.004, extra=fit(w - 0.26)))
    wb.append(_cloud(x + 0.1, y + 0.1, 0.055, PRINT_D, 0.005))
    wb.append(line(x + 0.04, y + 0.185, x + w - 0.04, y + 0.185, PRINT, 0.003))
    if lang == 'th':
        s2 = 0.15; t2 = th(x + w / 2, y + 0.65, w2, s2, PRINT_D, 'PLoma')
    else:
        t2 = text(x + w / 2, y + 0.64, w2, 0.11, PRINT_D, font=SLAB, ls=0.006, extra=fit(w - 0.16))
    wb.append(line(x + 0.2, y + 0.52, x + w - 0.2, y + 0.52, PRINT, 0.0025))
    for j in range(2): wb.append(tgreek(x + 0.08, y + 0.73 + j * 0.035, w - 0.16 - 0.15 * j, PRINT, 0.0085, r))
    o.append(f'<g filter="url(#{u}pr)">' + ''.join(wb) + '</g>')
    word = _wb_word(lang, u)
    o.append(f'<g filter="url(#{u}ty)">' + word + t2 + '</g>')
    if bleed is not None:
        defs_b, ov = _bleed(bleed, word, u, W, H); defs += defs_b; o.append(ov)
    o.append(path(ptsd(outline), 'none', stroke=INK, sw=0.004))
    return doc(W, H, long_px, ''.join(o), defs)

BLEED_FRAMES = 12

def _bleed(k, word, u, W, H):
    """Frame k (0..11) of the drip on the big word: the drop sits as a bead (0-4), soaks in; a wet ring spreads
    and the word's ink runs into it, darker and bluer at the centre."""
    t = k / (BLEED_FRAMES - 1); e = 1 - (1 - t) ** 2.2; cx, by = WB_W1; cy = by - 0.07; dx = 0.04
    R = 0.04 + 0.13 * e
    d = (f_rough(u + 'wet', W, H, disp=3.5 + 3 * e, freq=0.12, seed=21, octv=3) +
         f'<filter id="{u}blur" filterUnits="userSpaceOnUse" x="0" y="0" width="{W * K:g}" height="{H * K:g}"><feGaussianBlur stdDeviation="{0.2 + 1.7 * e:.3f}"/></filter>'
         f'<clipPath id="{u}wc"><circle cx="{n(cx + dx)}" cy="{n(cy)}" r="{n(R * 0.95)}"/></clipPath>'
         f'<radialGradient id="{u}bd" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#ffffff" stop-opacity="0.9"/><stop offset="0.35" stop-color="#e9eef2" stop-opacity="0.35"/>'
         f'<stop offset="1" stop-color="#6f7c8a" stop-opacity="0.45"/></radialGradient>')
    o = []
    wet = circ(cx + dx, cy, R, '#8a6f4e', stroke='#5a4632', sw=0.006, shade=False, extra=f'fill-opacity="{0.14 + 0.1 * e:.3f}" stroke-opacity="{0.2 + 0.25 * e:.3f}"')
    o.append(f'<g filter="url(#{u}wet)">' + wet + '</g>')
    soft = circ(cx + dx, cy, R, '#ede0c2', stroke=None, sw=0, shade=False, extra=f'opacity="{0.45 * e:.3f}"')      # the crisp print dissolves where wet
    run = word.replace(f'fill="{PRINT_D}"', 'fill="#3b3a4e"')
    o.append(f'<g clip-path="url(#{u}wc)"><g filter="url(#{u}wet)">' + soft + f'<g filter="url(#{u}blur)" opacity="{0.3 + 0.6 * e:.3f}">' + run + '</g></g></g>')
    if k <= 4:
        s = 1 - k / 5.0; br = 0.048 * (0.6 + 0.4 * s)
        o.append(f'<g opacity="{0.4 + 0.6 * s:.2f}">' + ell(cx + dx, cy, br, br * 0.9, f'url(#{u}bd)', stroke='#5b6370', sw=0.002, shade=False)
                 + ell(cx + dx - br * 0.35, cy - br * 0.35, br * 0.22, br * 0.14, '#ffffff', stroke=None, sw=0, shade=False, extra='opacity="0.9"') + '</g>')
    return d, ''.join(o)

# ----------------------------------------------------------------------------- 5. mechanism signs and pictograms (shots 7, 19, 20)
SS_D = 0.26

def speed_sign_svg(side='front', long_px=1600):
    """Round speed sign 0.26 D: cream disc, red ring, '100' large (Kanit Black, navy), Thai unit 'กม./ชม.' under it.
    side 'back': plain painted back with two rivets. The pin goes through the centre of the back plate (spin axis)."""
    D = SS_D; c = D / 2; R = D / 2 - 0.004; o = []; u = 'ss'
    defs = f_rough(u + 'r', D, D, disp=0.12, freq=1.5, seed=3) + grain_defs(u, D, D) + f'<clipPath id="{u}c"><circle cx="{n(c)}" cy="{n(c)}" r="{n(R)}"/></clipPath>'
    if side == 'back':
        o.append(circ(c, c, R, '#b9ad98', stroke=INK, sw=0.004)); o.append(circ(c, c, R * 0.86, 'none', stroke=mul('#b9ad98', 0.8), sw=0.003))
        o.append(grain(u, D, D, u + 'c', 0.25, 0.1))
        o.append(rect(c - 0.012, c - R * 0.7, 0.024, R * 1.4, mul('#b9ad98', 0.75), stroke=INK, sw=0.002))
        for yy in (c - R * 0.5, c + R * 0.5): o.append(circ(c, yy, 0.006, '#8a7d6a', stroke=INK, sw=0.0015))
        return doc(D, D, long_px, ''.join(o), defs)
    o.append(circ(c, c, R, RED, stroke=INK, sw=0.004)); o.append(circ(c, c, R * 0.74, PAPER, stroke=mul(RED, 0.7), sw=0.002))
    o.append(grain(u, D, D, u + 'c', 0.16, 0.06))
    w = adv('100', 'PKanitBlack'); s = R * 1.12 / w
    t = th(c, c + s * 0.22, '100', s, NAVY, 'PKanitBlack')
    w2 = adv('กม./ชม.', 'PKanit'); s2 = R * 0.62 / w2
    t2 = th(c, c + R * 0.5, 'กม./ชม.', s2, NAVY, 'PKanit')
    o.append(f'<g filter="url(#{u}r)">' + t + t2 + '</g>')
    return doc(D, D, long_px, ''.join(o), defs)

def _disc(c, R, ring=RED):
    return circ(c, c, R, ring, stroke=INK, sw=0.003) + circ(c, c, R * 0.78, PAPER, stroke=mul(ring, 0.7), sw=0.0015)

def no_turn_svg(direction='right', long_px=1500):
    """No-turn pictogram 0.22 D (no words): red ring, navy bent arrow, red slash. direction 'right' (east wall, 46.45)
    or 'left' (west wall, 46.85)."""
    D = 0.22; c = D / 2; R = c - 0.004; u = 'nt'; sg = 1 if direction == 'right' else -1
    o = [_disc(c, R)]
    a = [(c - sg * 0.025, c + 0.06), (c - sg * 0.025, c - 0.005), (c - sg * 0.01, c - 0.022), (c + sg * 0.03, c - 0.022)]
    o.append(pline(a, NAVY, 0.017, 'stroke-linejoin="round"'))
    o.append(poly([(c + sg * 0.025, c - 0.052), (c + sg * 0.068, c - 0.022), (c + sg * 0.025, c + 0.008)], NAVY, stroke=NAVY, sw=0.003))
    o.append(line(c - R * 0.55, c - R * 0.55, c + R * 0.55, c + R * 0.55, RED, 0.02))
    defs = f_rough(u + 'r', D, D, disp=0.1, freq=1.5, seed=5)
    return doc(D, D, long_px, f'<g filter="url(#{u}r)">' + ''.join(o) + '</g>', defs)

def compass_svg(long_px=1500):
    """Compass card 0.3 D: eight-point rose, north point red, Latin N above (shot 19, pings at 45.15)."""
    D = 0.3; c = D / 2; R = c - 0.005; u = 'cp'; o = []
    o.append(circ(c, c + 0.01, R * 0.8, PAPER, stroke=INK, sw=0.003)); o.append(circ(c, c + 0.01, R * 0.68, 'none', stroke=PRINT, sw=0.0015))
    cy = c + 0.01
    for k in range(16): a = math.radians(k * 22.5); o.append(line(c + R * 0.68 * math.sin(a), cy - R * 0.68 * math.cos(a), c + R * 0.76 * math.sin(a), cy - R * 0.76 * math.cos(a), PRINT, 0.002))
    for k in range(8):
        a = math.radians(k * 45); L = R * (0.62 if k % 2 == 0 else 0.36); wd = 0.018 if k % 2 == 0 else 0.012
        tip = (c + L * math.sin(a), cy - L * math.cos(a)); l_ = (c + wd * math.cos(a), cy + wd * math.sin(a)); r_ = (c - wd * math.cos(a), cy - wd * math.sin(a))
        col = RED if k == 0 else (PRINT_D if k % 2 == 0 else PRINT)
        o.append(poly([l_, tip, (c, cy)], col, stroke=INK, sw=0.0015)); o.append(poly([r_, tip, (c, cy)], mul(col, 1.35) if k else mul(RED, 0.75), stroke=INK, sw=0.0015))
    o.append(circ(c, cy, 0.01, PAPER, stroke=INK, sw=0.0015))
    o.append(text(c, 0.045, 'N', 0.05, RED, font=SLAB))
    defs = f_rough(u + 'r', D, D, disp=0.08, freq=1.6, seed=9)
    return doc(D, D, long_px, f'<g filter="url(#{u}r)">' + ''.join(o) + '</g>', defs)

def tick_stamp_svg(long_px=1500):
    """Tick-mark rubber-stamp impression 0.2 D (shot 7, lands on the chalk curve at 12.95): no words."""
    D = 0.2; c = D / 2; R = c - 0.01; u = 'tk'
    o = [circ(c, c, R, 'none', stroke=RED, sw=0.012), circ(c, c, R * 0.82, 'none', stroke=RED, sw=0.004)]
    o.append(path(ptsd(tapered([(c - 0.045, c + 0.0), (c - 0.012, c + 0.04), (c + 0.05, c - 0.045)], 0.012, 0.008, 0.02)), RED, stroke=None, sw=0))
    defs = f_rough(u + 'f', D, D, disp=0.4, freq=0.9, seed=4, speck=0.75, sfreq=1.0, st=0.6)
    return doc(D, D, long_px, f'<g transform="rotate(-8 {n(c)} {n(c)})"><g filter="url(#{u}f)" opacity="0.9">' + ''.join(o) + '</g></g>', defs)

def stamp_svg(face=False, lang='th', long_px=1500):
    """The forecast stamp alone, 0.34 D (same drawing as on the sheet). face=True: the rubber face of the stamp prop,
    mirrored, red-brown rubber with the raised design."""
    D = 0.34; c = D / 2; u = 'sp'; defs = stamp_defs(u, D, D)
    body = stamp_group(c, c, 0.155, u, lang, angle=0, mirror=face, colour=('#c9584a' if face else RED))
    if face: body = circ(c, c, 0.165, '#6b2a22', stroke=INK, sw=0.004) + body
    return doc(D, D, long_px, body, defs)

# ----------------------------------------------------------------------------- 6. smaller paper props
def spinner_svg(ghost=False, long_px=1500):
    """Storm spinner disc 0.16 D: red paper disc with a cream two-arm hurricane spiral, ink outline, pin hole at the
    centre. ghost=True: the grey-blue copy of the old storms (shot 21)."""
    D = 0.16; c = D / 2; R = c - 0.004; u = 'sp'
    base = '#8f97a8' if ghost else RED_T; arm = '#e7e9ee' if ghost else PAPER; o = [circ(c, c, R, base, stroke=INK, sw=0.003)]
    for sg in (1, -1):
        pts = [(c + sg * (0.006 + 0.0011 * k) * math.cos(math.radians(k * 14)), c + sg * (0.006 + 0.0011 * k) * math.sin(math.radians(k * 14))) for k in range(52)]
        o.append(path(ptsd(tapered(pts, 0.003, 0.002, 0.012), True), arm, stroke=None, sw=0))
    o.append(circ(c, c, R * 0.86, 'none', stroke=mul(base, 0.75), sw=0.002)); o.append(circ(c, c, 0.008, mul(base, 0.6), stroke=INK, sw=0.0015))
    defs = f_rough(u + 'r', D, D, disp=0.06, freq=2.0, seed=13)
    return doc(D, D, long_px, f'<g filter="url(#{u}r)">' + ''.join(o) + '</g>', defs)

def tape_svg(long_px=1600):
    """Narrow teletype paper tape 0.12 x 0.8 D for the chief's hand in shot 4: typed rows, torn ends."""
    W, H = 0.12, 0.8; r = random.Random(3); u = 'tp'
    ol = wobbly_rect(0.006, 0.01, W - 0.012, H - 0.02, r, 0.001, 0.02, torn_bottom=0.01)
    defs = grain_defs(u, W, H) + f'<clipPath id="{u}c"><path d="{ptsd(ol)}"/></clipPath>' + f_rough(u + 't', W, H, 0.15, 1.3, 2, 0.3, 1.8, 0.67)
    o = [path(ptsd(ol), PAPER, stroke=None, sw=0), grain(u, W, H, u + 'c')]
    rows = ''.join(tgreek(0.02, 0.05 + j * 0.032, W - 0.04 - r.uniform(0, 0.03), PRINT_D, 0.009, r, 0.6) for j in range(23))
    o.append(f'<g clip-path="url(#{u}c)" filter="url(#{u}t)">{rows}</g>'); o.append(path(ptsd(ol), 'none', stroke=INK, sw=0.003))
    return doc(W, H, long_px, ''.join(o), defs)

def typed_sheet_svg(long_px=1600):
    """Greeked typed sheet 0.5 x 0.65 D for the foreground desk of shot 12 (no readable words)."""
    W, H = 0.5, 0.65; r = random.Random(12); u = 'ts'
    ol = wobbly_rect(0.006, 0.006, W - 0.012, H - 0.012, r, 0.0008, 0.05)
    defs = grain_defs(u, W, H) + f'<clipPath id="{u}c"><path d="{ptsd(ol)}"/></clipPath>' + f_rough(u + 't', W, H, 0.15, 1.3, 2, 0.3, 1.8, 0.67)
    o = [path(ptsd(ol), PAPER, stroke=None, sw=0), grain(u, W, H, u + 'c')]
    b = [line(0.05, 0.06, 0.3, 0.06, PRINT_D, 0.016), line(0.04, 0.09, W - 0.04, 0.09, PRINT, 0.002)]
    b += [tgreek(0.05, 0.13 + j * 0.03, W - 0.1 - (r.uniform(0.05, 0.2) if j % 5 == 4 else 0), PRINT, 0.008, r) for j in range(16)]
    o.append(f'<g clip-path="url(#{u}c)" filter="url(#{u}t)">' + ''.join(b) + '</g>'); o.append(path(ptsd(ol), 'none', stroke=INK, sw=0.003))
    return doc(W, H, long_px, ''.join(o), defs)

def beach_sign_svg(long_px=2400):
    """Fence sign of the beach set reworded (shots 8, 16, 23): LONG ISLAND as the large line, 2.2 x 0.95 D (same size
    as the set's 'sign' texture). Cream board, inset dark border, red slab capitals, small dark sub-line, four nails."""
    W, H = 2.2, 0.95; u = 'bs'; r = random.Random(8)
    defs = grain_defs(u, W, H) + f'<clipPath id="{u}c"><rect width="{W * K:g}" height="{H * K:g}"/></clipPath>' + f_rough(u + 'p', W, H, 0.5, 0.5, 4, 0.3, 0.9, 0.65)
    o = [rect(0, 0, W, H, '#f6efe2', stroke=INK, sw=0.03), grain(u, W, H, u + 'c', 0.3, 0.14)]
    for k in range(5): yy = 0.1 + k * 0.19 + r.uniform(-0.02, 0.02); o.append(line(0.03, yy, W - 0.03, yy + r.uniform(-0.01, 0.01), mul('#f6efe2', 0.9), 0.006))
    o.append(rect(0.07, 0.07, W - 0.14, H - 0.14, 'none', stroke='#3d2a22', sw=0.018)); o.append(rect(0.1, 0.1, W - 0.2, H - 0.2, 'none', stroke=RED, sw=0.006))
    t = [text(W / 2, 0.5, 'LONG ISLAND', 0.33, RED, font=SLAB, ls=0.02, extra=fit(1.86)), line(0.35, 0.585, W - 0.35, 0.585, RED, 0.012),
         text(W / 2, 0.735, 'BATHING BEACH · SUFFOLK COUNTY 1938', 0.085, '#3d2a22', font=SLAB, ls=0.008, extra=fit(1.5))]
    o.append(f'<g filter="url(#{u}p)">' + ''.join(t) + '</g>')
    for x, y in ((0.13, 0.13), (W - 0.13, 0.13), (0.13, H - 0.13), (W - 0.13, H - 0.13)): o.append(circ(x, y, 0.022, '#6d6058', stroke=INK, sw=0.006))
    return doc(W, H, long_px, ''.join(o), defs)

# ----------------------------------------------------------------------------- registry
def _R(name, fn, size, kind='static', note='', frames=None, transparent=True):
    return name, dict(svg=fn, png=os.path.join(TEX, name + '.png') if frames is None else os.path.join(TEX, name, 'f_%02d.png'),
                      size_D=size, kind=kind, note=note, transparent=transparent, nframes=frames,
                      frames=[os.path.join(TEX, name, 'f_%02d.png' % k) for k in range(frames)] if frames else None)

REGISTRY = dict([
    _R('forecast_sheet', lambda: forecast_svg('th'), (FS_W, FS_H), note='shot 14 hi-res quad after the tear: typed Thai ฝนตก / ลมกระโชก, Thai stamp ทางการ, torn bottom (plan text policy)'),
    _R('forecast_sheet_teletype', lambda: forecast_svg('th', words=2, stamp=False, torn=False), (FS_W, FS_H), note='shot 14 sheet still in the teletype (before the stamp at 29.82 and the tear at 29.95)'),
    _R('forecast_sheet_base', lambda: forecast_svg('th', words=0, stamp=False, torn=True), (FS_W, FS_H), note='sheet without the two big words and the stamp: lay forecast_word_1/2 and forecast_stamp over it to pop them'),
    _R('forecast_word_1', lambda: forecast_svg('th', only='word1'), (FS_W, FS_H), kind='overlay', note='ฝนตก alone, same frame as the sheet (pops at 30.85)'),
    _R('forecast_word_2', lambda: forecast_svg('th', only='word2'), (FS_W, FS_H), kind='overlay', note='ลมกระโชก alone, same frame (pops at 31.30)'),
    _R('forecast_stamp', lambda: forecast_svg('th', only='stamp'), (FS_W, FS_H), kind='overlay', note='stamp impression alone, same frame (lands 29.82)'),
    _R('forecast_sheet_en', lambda: forecast_svg('en'), (FS_W, FS_H), note='English variant: RAIN, / GUSTY WINDS, stamp OFFICIAL (task brief wording; the plan asks for Thai)'),
    _R('nickname_label', label_svg, (LB_W, LB_H), note='Thai brush lettering ทางด่วนพายุ; pin at LB_PIN'),
    _R('calendar_pad_20', lambda: calendar_svg(20, 'pad'), (CAL_W, CAL_H), note='whole pad, SEPTEMBER / 20 / TUESDAY / 1938: replaces the set texture "calendar" (same 0.66 x 0.9 D)'),
    _R('calendar_pad_21', lambda: calendar_svg(21, 'pad'), (CAL_W, CAL_H), note='whole pad, leaf 21 WEDNESDAY (shots 17, 18, 25, kitchen); also what lies under leaf 20'),
    _R('calendar_leaf_20', lambda: calendar_svg(20, 'leaf'), LEAF[2:], note='top leaf alone (flutter quad), at offset (0.02, 0.02) inside the pad'),
    _R('calendar_leaf_21', lambda: calendar_svg(21, 'leaf'), LEAF[2:], note='leaf 21 alone'),
    _R('newspaper', lambda: newspaper_svg('th'), (NP_W, NP_H), note='shots 15, 26: Thai weather box พยากรณ์อากาศวันนี้ / ฝนตก / ลมกระโชก, English masthead and dateline'),
    _R('newspaper_en', lambda: newspaper_svg('en'), (NP_W, NP_H), note="English variant: TODAY'S FORECAST / RAIN, / GUSTY WINDS"),
    _R('newspaper_bleed', lambda frame=0: newspaper_svg('th', bleed=frame), (NP_W, NP_H), kind='sequence', frames=BLEED_FRAMES,
       note='shot 26 drip from 64.95: 12 frames, one per film frame (or hold the last); f_00 = drop lands on ฝนตก'),
    _R('speed_sign', speed_sign_svg, (SS_D, SS_D), note="shot 20: '100' and Thai unit กม./ชม."),
    _R('speed_sign_back', lambda: speed_sign_svg('back'), (SS_D, SS_D), note='back face of the speed sign'),
    _R('stamp_impression', stamp_svg, (0.34, 0.34), note='round Thai stamp ทางการ alone'),
    _R('stamp_face', lambda: stamp_svg(face=True), (0.34, 0.34), note='rubber face of the stamp prop (mirrored)'),
    _R('tick_stamp', tick_stamp_svg, (0.2, 0.2), note='shot 7 tick stamp, no words'),
    _R('no_right_turn', lambda: no_turn_svg('right'), (0.22, 0.22), note='shot 19 east wall pictogram, no words'),
    _R('no_left_turn', lambda: no_turn_svg('left'), (0.22, 0.22), note='shot 19 west wall pictogram, no words'),
    _R('compass', compass_svg, (0.3, 0.3), note='shot 19 compass with Latin N'),
    _R('spinner_disc', spinner_svg, (0.16, 0.16), note='storm spinner paper disc (pin through the centre)'),
    _R('spinner_disc_ghost', lambda: spinner_svg(True), (0.16, 0.16), note='grey ghost spinner (shot 21)'),
    _R('paper_tape', tape_svg, (0.12, 0.8), note="shot 4: teletype tape in the chief's hand (torn at 4.9)"),
    _R('desk_typed_sheet', typed_sheet_svg, (0.5, 0.65), note='shot 12 foreground desk: greeked typed sheet'),
    _R('beach_sign', beach_sign_svg, (2.2, 0.95), transparent=False, note='beach fence sign reworded: LONG ISLAND (replaces beach_tex sign, same size)'),
])

def _px(svg):
    import re
    m = re.search(r'width="(\d+)" height="(\d+)"', svg); return int(m.group(1)), int(m.group(2))

def build(names=None, force=False, verbose=True):
    """Rasterise the registry (or the named items) whose SVG changed. Returns {name: png path or list of frame paths}."""
    os.makedirs(TEX, exist_ok=True); os.makedirs(TMP, exist_ok=True)
    mp = os.path.join(TEX, 'manifest.json'); man = json.load(open(mp)) if os.path.exists(mp) else {}
    jobs = []; out = {}
    for nm, e in REGISTRY.items():
        if names and nm not in names: continue
        items = [(e['svg'](frame=k), e['frames'][k], f'{nm}#{k}') for k in range(e['nframes'])] if e['kind'] == 'sequence' else [(e['svg'](), e['png'], nm)]
        for svg, png, key in items:
            W, H = _px(svg); e['px'] = (W, H); hsh = hashlib.sha1(svg.encode()).hexdigest()
            os.makedirs(os.path.dirname(png), exist_ok=True)
            if force or man.get(key) != hsh or not os.path.exists(png):
                src = os.path.join(TMP, key.replace('#', '_') + '.svg'); open(src, 'w', encoding='utf-8').write(svg)
                jobs.append(dict(src=src, out=png, w=W, h=H, transparent=e['transparent'])); man[key] = hsh
        out[nm] = e['frames'] or e['png']
    if jobs:
        jp = os.path.join(TMP, 'jobs.json'); json.dump(jobs, open(jp, 'w'))
        r = subprocess.run(['node', os.path.join(HERE, 'raster.js'), jp], capture_output=True, text=True,
                           env=dict(os.environ, NODE_PATH=os.environ.get('NODE_PATH', '/opt/node22/lib/node_modules')))
        if r.returncode != 0: raise RuntimeError('raster failed: ' + r.stderr[-3000:])
        if verbose: print(f'rasterised {len(jobs)} images')
    json.dump(man, open(mp, 'w'), indent=0)
    meta = {nm: dict(png=e['frames'] or e['png'], size_D=e['size_D'], px=e.get('px'), kind=e['kind'], note=e['note']) for nm, e in REGISTRY.items()}
    json.dump(meta, open(os.path.join(TEX, 'registry.json'), 'w'), indent=1, ensure_ascii=False)
    return out

# ----------------------------------------------------------------------------- contact sheet and shaping crops
def sheet(out=os.path.join(HERE, 'sheet.jpg')):
    """All items on a neutral ground next to the reference text props (a/t32.0 newspaper, a/t40.0 calendar, a/t27.5)."""
    from PIL import Image, ImageDraw, ImageFont
    fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
    refs = [os.path.join(PROJ, 'ref', 'a', f) for f in ('t32.0.jpg', 't40.0.jpg', 't27.5.jpg')]
    crop = os.path.join(PROJ, 'ref', 'crops', 'env', 'A_text_props.jpg')
    Hrow = 560; tiles = []
    for p in refs + [crop]:
        im = Image.open(p).convert('RGB'); s = Hrow / im.height; tiles.append((im.resize((int(im.width * s), Hrow)), 'REF ' + os.path.relpath(p, os.path.join(PROJ, 'ref'))))
    for nm, e in REGISTRY.items():
        p = e['frames'][-1] if e['kind'] == 'sequence' else e['png']
        im = Image.open(p).convert('RGBA'); s = min(Hrow / im.height, 900 / im.width); im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))))
        bg = Image.new('RGB', im.size, (107, 93, 87)); bg.paste(im, (0, 0), im); tiles.append((bg, nm + ('  [f_11]' if e['kind'] == 'sequence' else '')))
    Wmax = 3000; rows = []; cur = []; w = 0
    for t in tiles:
        if w + t[0].width + 20 > Wmax and cur: rows.append(cur); cur = []; w = 0
        cur.append(t); w += t[0].width + 20
    rows.append(cur)
    Ht = sum(Hrow + 50 for _ in rows) + 20; S = Image.new('RGB', (Wmax, Ht), (58, 50, 48)); d = ImageDraw.Draw(S); y = 10
    for row in rows:
        x = 10
        for im, lab in row:
            S.paste(im, (x, y + 36)); d.text((x, y + 6), lab, fill=(255, 235, 200) if lab.startswith('REF') else (235, 235, 235), font=fnt); x += im.width + 20
        y += Hrow + 50
    S.save(out, quality=88); return out

def crops(outdir=TMP):
    """Full-size crops of every Thai cluster with marks (ด่ ยุ in the label; ณ์ นี้ in the newspaper header) for the shaping check."""
    from PIL import Image
    res = []
    lab = Image.open(REGISTRY['nickname_label']['png']); W, H = lab.size
    res.append(lab.crop((0, 0, W // 2 + 200, H)))
    np_ = Image.open(REGISTRY['newspaper']['png']); W, H = np_.size; s = W / NP_W
    x, y, w, h = WB; res.append(np_.crop((int(x * s), int(y * s), int((x + w) * s), int((y + h) * s))))
    ss = Image.open(REGISTRY['speed_sign']['png']); res.append(ss)
    fs = Image.open(REGISTRY['forecast_sheet']['png']); W, H = fs.size; s = W / FS_W
    res.append(fs.crop((int(0.55 * s), 0, W, int(0.42 * s))))
    paths = []
    for i, im in enumerate(res):
        p = os.path.join(outdir, f'crop_thai_{i}.png'); bg = Image.new('RGB', im.size, (107, 93, 87)); im = im.convert('RGBA'); bg.paste(im, (0, 0), im); bg.save(p); paths.append(p)
    return paths

if __name__ == '__main__':
    a = sys.argv[1:] or ['all']; force = '--force' in a
    if a[0] in ('build', 'all'): build(force=force)
    if a[0] in ('sheet', 'all'): print(sheet())
    if a[0] in ('crops', 'all'): print('\n'.join(crops()))

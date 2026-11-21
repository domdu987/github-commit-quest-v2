"""film 17 v2 set: one connected world "prefecture17" (PLAN_V2 §3). bpy 5.3, Cycles CPU. 1 unit = 1 m, Z up.
One Blender scene, one coordinate frame: the Paris street at dusk (+ rooftop plate, Seine, Notre-Dame), the Préfecture façade, the corridor,
the measuring room (v1 room moved by MO = (+9.2, +12.0, +1.2)) and the ARCHIVES hall (x 13-21, y 2-34) with the reveal drawer in the GRAND bank.
`world_build(take)` builds only what a take can see (visibility sets). Light presets BLUE_HOUR_EXT / GASLIGHT_INT / SUNSET_INT / ARCHIVE_DAY /
ARCHIVE_NIGHT live in bertillon.LIGHTS (so v1 rooms can use them too). Camera paths per take (cam_path, path_T1..path_T8), anchor size report.
Imports bertillon.py (v1 kit, unchanged behaviour). See API.md §v2."""
import os, sys, math, random, json, time
import numpy as np
import bpy
from mathutils import Vector, Matrix, Euler
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bertillon as K
import bertillon_tex as TX
from bertillon import Batch, hex_lin

FILM = os.path.normpath(os.path.join(HERE, '..', '..'))
FONTS = {'serif': os.path.join(HERE, 'fonts', 'LiberationSerif-Bold.ttf'),       # bundled serif (SIL OFL), drawn condensed for signs
         'sans': os.path.join(FILM, 'fonts', 'WorkSans-Black.ttf'), 'thai': os.path.join(FILM, 'fonts', 'Kanit_900Black.ttf')}
TEX = TX.TEX
MO = (9.2, 12.0, 1.2)            # measuring room offset (v1 local -> world)
FZ = 1.2                         # interior floor z (raised ground floor)
FACADE_X = 5.45                  # outer face of the Préfecture façade (the measure room wall is 5.7..6.0 behind it)
COBALT, AMBER, HONEY, OCHRE, KEPI, ZENITH = '#1F4FD0', '#FFA62B', '#D9822B', '#E8A33A', '#D7262E', '#1A3FB8'
GOLD = '#FFC94A'

# ================================================================ light presets (PLAN §2) -> bertillon.LIGHTS
_base = dict(K.LIGHTS['DAY_INT'])
K.LIGHTS.update({
    # street at dusk: low amber sun at 0.35, gas lamps x1.6, cobalt sky dome with a thin amber horizon, blue SHADE, 70 % windows lit
    'BLUE_HOUR_EXT': dict(_base, key=(2.2, 1.25, 0.45), sun_dir=(0.55, 0.62, -0.20), sun_angle=1.0, sun=True, sun_k=0.35, lamp_k=1.6,
                          shade=(0.13, 0.20, 0.80), tint=(0.08, 0.14, 0.52), mix=0.55, lift=(0.004, 0.014, 0.06), form=(0.0, -0.05, 0.25),
                          sky=('#1A3FB8', '#2f5be0', '#ffae4a'), sky_k=1.0, ink='#141a48', world=(0.06, 0.1, 0.42), gain=0.82, glow=1.5, win_w=0,
                          win_lit=0.7, rim='#9cc2ff', fill_w=900, fill_col=(0.45, 0.6, 1.0)),
    # façade -> corridor: no sun, wall gas brackets every 2.5 m (amber/blue bands), cobalt walls, blue transom light from the street
    'GASLIGHT_INT': dict(_base, key=(1.6, 1.0, 0.5), sun_dir=(0.6, 0.2, -0.75), sun=True, sun_k=0.0, lamp_k=2.2, shade=(0.14, 0.20, 0.80),
                         tint=(0.09, 0.14, 0.52), mix=0.5, lift=(0.004, 0.012, 0.05), form=(0.0, -0.05, 0.25), ink='#141a48', world=(0.06, 0.1, 0.42),
                         gain=0.8, glow=1.4, win_w=120, rim='#ffb85a', fill_w=60, fill_col=(0.5, 0.65, 1.0)),
    # measuring room: low amber sun through the open French window (hard shaft + dust), sky fill +30 %, 2 gasoliers
    'SUNSET_INT': dict(_base, key=(2.6, 1.45, 0.42), sun_dir=(0.86, 0.12, -0.42), sun_angle=0.8, sun=True, sun_k=1.0, lamp_k=1.1,
                       shade=(0.14, 0.18, 0.70), tint=(0.09, 0.125, 0.47), mix=0.5, lift=(0.004, 0.012, 0.05), form=(0.0, -0.05, 0.25),
                       ink='#1a1440', world=(0.08, 0.12, 0.45), gain=0.72, glow=1.25, win_w=240, beam_k=1.4, rim='#ffb85a', rim2='#8fb4ff',
                       fill_w=110, fill_col=(0.55, 0.7, 1.0)),
    # archive hall, day: 5 pale blue-white skylight shafts with dust, amber banker lamps, cobalt vault and gallery iron
    'ARCHIVE_DAY': dict(_base, key=(1.95, 2.0, 2.25), sun_dir=(0.22, 0.30, -0.93), sun_angle=0.9, sun=True, sun_k=0.62, lamp_k=1.3,
                        shade=(0.13, 0.185, 0.74), tint=(0.085, 0.13, 0.49), mix=0.5, lift=(0.004, 0.012, 0.05), form=(0.0, -0.05, 0.25),
                        ink='#141a48', world=(0.06, 0.1, 0.42), gain=0.74, glow=1.3, win_w=0, frost=('#9fbcff', 1.5), beam_k=2.4,
                        rim='#ffb85a', fill_w=300, fill_col=(1.0, 0.72, 0.4), vault_w=140, beam_col='#e4edff'),
    # archive hall, night (false payoff): ONE banker lamp + candle, gasoliers at 40 %, moonlight-blue shafts; cobalt walls lifted (luma >= 85)
    'ARCHIVE_NIGHT': dict(_base, key=(0.55, 0.8, 1.9), sun_dir=(0.22, 0.30, -0.93), sun_angle=0.9, sun=True, sun_k=0.55, lamp_k=0.75,
                          shade=(0.13, 0.20, 0.92), tint=(0.08, 0.14, 0.62), mix=0.45, lift=(0.004, 0.014, 0.07), form=(0.0, -0.05, 0.25),
                          ink='#10133c', world=(0.04, 0.06, 0.3), gain=0.75, glow=1.1, win_w=0, frost=('#4a72f0', 2.6), beam_k=2.6,
                          rim='#9cc2ff', fill_w=110, fill_col=(1.0, 0.68, 0.36), gasolier_k=0.4, vault_w=1100, beam_col='#7f9eff'),
})
PRESETS_V2 = ('BLUE_HOUR_EXT', 'GASLIGHT_INT', 'SUNSET_INT', 'ARCHIVE_DAY', 'ARCHIVE_NIGHT')
AMB_K = 0.78                      # SET-gate calibration: the painted ambient (shade, tint) of the v2 presets, x0.78 -> mean luma in the 85-110 band
for _p in PRESETS_V2: K.LIGHTS[_p]['shade'] = tuple(AMB_K * x for x in K.LIGHTS[_p]['shade']); K.LIGHTS[_p]['tint'] = tuple(AMB_K * x for x in K.LIGHTS[_p]['tint'])
RIM = {p: K.LIGHTS[p]['rim'] for p in PRESETS_V2}            # rim colour per preset (warm / cool) for stage_cast v2 (`rim_col`)

# ================================================================ textures (PIL, cached in tex/, git-ignored)
def _tp(name): return os.path.join(TEX, 'v2_%s.png' % name)
def _rgb(h): return TX._hexrgb(h)
def font(kind='serif', size=64): return ImageFont.truetype(FONTS.get(kind, kind), size)
def tex_checker(name, c1, c2, n=8, S=512, joint='#5a2a1c'):
    p = _tp(name)
    if os.path.exists(p): return p
    im = Image.new('RGB', (S, S), _rgb(joint)); d = ImageDraw.Draw(im); s = S / n
    for i in range(n):
        for j in range(n): d.rectangle([i * s + 3, j * s + 3, (i + 1) * s - 3, (j + 1) * s - 3], fill=_rgb(c1 if (i + j) % 2 == 0 else c2))
    return _save(TX._std(np.asarray(im, dtype=float), 4, 3, 64), p)
def _save(a, p): Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(p); return p
def tex_runner(name='runner', S=512):
    """cobalt runner with a red border and gold lozenges (PLAN §3c rug)."""
    p = _tp(name)
    if os.path.exists(p): return p
    cb = _rgb(COBALT); red = _rgb(KEPI); gold = _rgb('#ffbe3a'); im = Image.new('RGB', (S, S), cb); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 56, S], fill=red); d.rectangle([S - 57, 0, S, S], fill=red); d.rectangle([64, 0, 72, S], fill=gold); d.rectangle([S - 73, 0, S - 65, S], fill=gold)
    for k in range(2):
        cy = S * (0.25 + 0.5 * k); cx = S / 2
        d.polygon([(cx, cy - 120), (cx + 80, cy), (cx, cy + 120), (cx - 80, cy)], outline=gold, width=8); d.polygon([(cx, cy - 56), (cx + 38, cy), (cx, cy + 56), (cx - 38, cy)], fill=red)
    return _save(TX._std(np.asarray(im, dtype=float), 4, 9, 64), p)
def tex_facade_far(name='far_facade', lit=0.6, S=512, seed=5):
    """low-poly roofscape block skin: ochre ashlar, 4 floors x 4 windows per 12 m tile, lit amber (share `lit`) or cobalt glass."""
    p = _tp(name)
    if os.path.exists(p): return p
    r = random.Random(seed); im = Image.new('RGB', (S, S), _rgb('#d29a5c')); d = ImageDraw.Draw(im)
    for fl in range(4):
        y0 = fl * S / 4; d.rectangle([0, y0, S, y0 + 6], fill=_rgb('#a8703c'))
        for k in range(4):
            x0 = k * S / 4 + S / 16; on = r.random() < lit
            d.rectangle([x0, y0 + 24, x0 + S / 8, y0 + S / 4 - 26], fill=_rgb('#ffb648' if on else '#1d2a7a'))
            d.rectangle([x0 - 6, y0 + S / 4 - 28, x0 + S / 8 + 6, y0 + S / 4 - 20], fill=_rgb('#8a5a30'))
    return _save(np.asarray(im, dtype=float), p)
def tex_zinc2(name, base, S=512, seed=8):
    """v2 zinc / slate: standing seams every 1/6 tile (6 texels, 0.55 x base), a lighter lap line per course and soft blotches; reads at 40 m."""
    p = _tp('zinc2_' + name)
    if os.path.exists(p): return p
    b = _rgb(base); im = Image.new('RGB', (S, S), b); d = ImageDraw.Draw(im); lo = tuple(int(c * 0.55) for c in b); hi = tuple(min(255, int(c * 1.25)) for c in b)
    for i in range(6): d.rectangle([i * S / 6 - 3, 0, i * S / 6 + 3, S], fill=lo)
    for j in range(4): d.rectangle([0, j * S / 4, S, j * S / 4 + 4], fill=hi)
    return _save(TX._std(np.asarray(im, dtype=float), 6, seed, 96), p)
def tex_photowall(name='photowall', S=1024, seed=3):
    """the 'PHOTOGRAPHIES — SÛRETÉ' wall: rows of small sepia-amber police photographs (head silhouettes) on a cobalt ground. tile = 1.2 m."""
    p = _tp(name)
    if os.path.exists(p): return p
    r = random.Random(seed); im = Image.new('RGB', (S, S), _rgb('#1a3fb8')); d = ImageDraw.Draw(im); nx, ny = 10, 7; cw, ch = S / nx, S / ny
    for i in range(nx):
        for j in range(ny):
            x0, y0 = i * cw + 7 + r.uniform(-2, 2), j * ch + 8 + r.uniform(-2, 2); w, h = cw - 14, ch - 16
            tone = r.choice(['#f0b25a', '#e9a042', '#f5c272', '#e08a3a', '#f7cf86']); d.rectangle([x0, y0, x0 + w, y0 + h], fill=_rgb(tone))
            d.rectangle([x0 + 6, y0 + 6, x0 + w - 6, y0 + h * 0.72], fill=_rgb('#b85a22'))
            cx, cy = x0 + w / 2, y0 + h * 0.36; rr = w * 0.2
            d.ellipse([cx - rr, cy - rr * 1.15, cx + rr, cy + rr * 1.15], fill=_rgb('#4a2016')); d.pieslice([cx - rr * 1.9, cy + rr * 0.8, cx + rr * 1.9, cy + rr * 3.6], 180, 360, fill=_rgb('#4a2016'))
            d.rectangle([x0 + 8, y0 + h * 0.8, x0 + w * r.uniform(0.4, 0.8), y0 + h * 0.86], fill=_rgb('#7a3a1c'))
    return _save(TX._std(np.asarray(im, dtype=float), 3, 4, 64), p)
def tex_flag(name='tricolore', S=256):
    p = _tp(name)
    if os.path.exists(p): return p
    im = Image.new('RGB', (S * 3 // 2, S), (255, 255, 255)); d = ImageDraw.Draw(im); w = S // 2
    d.rectangle([0, 0, w, S], fill=_rgb('#1d3fc8')); d.rectangle([w, 0, 2 * w, S], fill=_rgb('#f4ead8')); d.rectangle([2 * w, 0, 3 * w, S], fill=_rgb(KEPI))
    im.save(p); return p

def _fit_text(text, kind, W, H, maxh_frac=0.62, condense=0.84):
    """largest font size whose (condensed) text fits W x H * maxh_frac."""
    lo, hi = 8, int(H * 1.4)
    while hi - lo > 1:
        m = (lo + hi) // 2; f = font(kind, m); bb = f.getbbox(text)
        if (bb[2] - bb[0]) * condense <= W and (bb[3] - bb[1]) <= H * maxh_frac: lo = m
        else: hi = m
    return font(kind, lo)
def tex_sign(text, w, h, fg=GOLD, bg=COBALT, kind='serif', border=True, sub=None, ppm=520, condense=0.84, name=None, frame='#7a2a10', maxh=0.62, bevel=True):
    """a sign texture: `text` (and an optional smaller `sub` line) centred on a `bg` panel with a thin `fg` border line and a dark outer frame.
    ppm = texels per metre (>= 28 px cap height on a phone at the nearest distance is a placement rule; the texture never is the limit). SS x2."""
    key = name or ('sign_%s_%dx%d_%s_%s_%s' % (''.join(c for c in text if c.isalnum())[:24], int(w * 100), int(h * 100), fg[1:], bg[1:], kind))
    p = _tp(key)
    if os.path.exists(p): return p
    W = int(min(4096, max(128, w * ppm))); H = int(min(2048, max(48, h * ppm))); SS = 2; W2, H2 = W * SS, H * SS
    im = Image.new('RGB', (W2, H2), _rgb(bg)); d = ImageDraw.Draw(im); b = max(4, int(H2 * 0.05))
    if frame: d.rectangle([0, 0, W2 - 1, H2 - 1], outline=_rgb(frame), width=b)
    if border: d.rectangle([b * 2, b * 2, W2 - 2 * b, H2 - 2 * b], outline=_rgb(fg), width=max(3, b // 2))
    lines = [(text, 1.0)] + ([(sub, 0.42)] if sub else [])
    tot = sum(s for _, s in lines); y = H2 * (0.5 - (maxh * (1 if not sub else 0.92)) / 2) if not sub else H2 * 0.14
    for t, s in lines:
        hh = H2 * (maxh if not sub else 0.72) * s / tot; f = _fit_text(t, kind, W2 - 8 * b, hh / (maxh if not sub else 0.72) * 1.0, maxh_frac=(maxh if not sub else 0.72), condense=condense)
        bb = f.getbbox(t); tw, th = bb[2] - bb[0], bb[3] - bb[1]
        lay = Image.new('L', (tw + 8, th + 8), 0); ImageDraw.Draw(lay).text((4 - bb[0], 4 - bb[1]), t, font=f, fill=255)
        lay = lay.resize((max(1, int((tw + 8) * condense)), th + 8), Image.LANCZOS)
        if bevel:                                                                                 # a dark drop line under gilt letters (reads as relief)
            sh = Image.new('RGB', lay.size, (40, 14, 10)); im.paste(sh, (int(W2 / 2 - lay.size[0] / 2) + 3, int(y + (hh - th) / 2) + 4), lay)
        col = Image.new('RGB', lay.size, _rgb(fg)); im.paste(col, (int(W2 / 2 - lay.size[0] / 2), int(y + (hh - th) / 2)), lay)
        y += hh + H2 * 0.04
    im = im.resize((W, H), Image.LANCZOS); im.save(p); return p

# ================================================================ v2 palette (repaint, PLAN §2) - replaces v1 keys inside the world only
def _pal2():
    pl = K._pal()
    def add(k, col, tex=None, tile=1.0, tint=False, sm=(0.8, 1.0, 1.12), ink=False, gain=1.0, off=(0, 0, 0), mix=0.5, afl=0.12):
        pl[k] = dict(col=col, tex=tex, tile=tile, tint=tint, sm=sm, ink=ink, gain=gain, off=off, mix=mix, afl=afl)
    c = lambda h: TX._hexrgb(h)
    # the v1 keys, repainted: ochre stone (no cream/grey), cobalt dado / ceiling / glass / iron, saturated oak, honey beams, red accent
    add('wall', OCHRE, TX.plaster('v2_wall_ochre', c(OCHRE), seed=3), tile=2.5, mix=0.45, afl=0.22, sm=(0.75, 0.95, 1.15))
    add('wall_ochre', '#d99a3a', TX.plaster('v2_wall_ochre2', c('#d99a3a'), seed=4), tile=2.5, mix=0.45, afl=0.2)
    add('wall_dk', COBALT, TX.plaster('v2_wall_cobalt_dk', c('#1d47c0'), seed=5), tile=2.5, mix=0.4, afl=0.2)
    add('wain', COBALT, TX.wain_panels('v2_wain_cobalt', c('#1e48c4')), tile=1.0, mix=0.4, afl=0.2)
    add('ceiling', COBALT, TX.boards('v2_ceil_cobalt', c('#1d46c2'), seed=13), tile=1.5, mix=0.4, afl=0.2)
    add('ceil_navy', COBALT, TX.boards('v2_ceil_cobalt2', c('#1f4fd0'), seed=19), tile=1.5, mix=0.4, afl=0.2)
    add('beam', HONEY, TX.boards('v2_beam_honey', c(HONEY), seed=14, n=3), tile=1.0, ink=True, mix=0.45)
    add('frieze', COBALT, TX.frieze('v2_frieze', bg='#1a3fb8', fg='#ffbe3a'), tile=1.0, mix=0.4, afl=0.2)
    add('floor', '#B5531F', TX.planks('v2_floor_oak2', c('#a94a1a'), n=6, seed=11), tile=1.5, mix=0.45, afl=0.18)
    add('floor_dk', '#a8461a', TX.planks('v2_floor_oak2', c('#a8461a'), n=6, seed=12), tile=1.5, mix=0.45, afl=0.15)
    add('walnut', '#8a3a16', TX.boards('v2_walnut', c('#8a3a16'), seed=15), tile=1.0, tint=True, ink=True, mix=0.45)
    add('honey', HONEY, TX.boards('v2_honey', c(HONEY), seed=16, n=3), tile=0.9, tint=True, ink=True, mix=0.45)
    add('drawer', HONEY, TX.boards('v2_drawer2', c('#cc7426'), seed=16, n=3), tile=0.9, tint=True, ink=False, mix=0.45, afl=0.15)
    add('oak', '#c8661e', TX.boards('v2_oak', c('#c8661e'), seed=17, n=2), tile=0.8, tint=True, ink=True, mix=0.45)
    add('oxblood', KEPI, tint=True, ink=True, mix=0.45)
    add('navy', '#1b3ea8', tint=True, ink=True, mix=0.45)
    add('baize', '#13804a', tint=True, ink=True, mix=0.45)
    add('leather', '#9a3a12', tint=True, ink=True, mix=0.45)
    add('cream', '#f0bf6a', tint=True, ink=False, mix=0.4)
    add('brass', '#f0a92a', tint=True, ink=True, mix=0.4)
    add('brass_nk', '#f0a92a', tint=True, ink=False, mix=0.4)
    add('steel', '#7c9cf0', tint=True, ink=True, mix=0.4)
    add('iron', '#1d2c78', ink=True, mix=0.45)
    add('cloth', '#1a1d5a', ink=True, mix=0.5)
    add('ink', '#1a1d5a', mix=0.5)
    add('glass', '#4f8ae0', mix=0.4)
    add('dark', '#16207a', mix=0.4)
    add('runner', COBALT, tex_runner(), tile=1.4, off=(0.5, 0, 0), mix=0.45)
    add('stone', '#D9B07A', TX.ashlar('v2_stone2', c('#d6994e'), seam=(0x8a, 0x52, 0x2a)), tile=2.0, mix=0.5, afl=0.15)
    add('stone_dk', '#c8904a', TX.ashlar('v2_stone_dk', c('#cf8f45'), seed=21, seam=(0x7a, 0x44, 0x22)), tile=2.0, mix=0.5, afl=0.15)
    add('cobble', '#4c58b0', TX.cobbles('v2_cobble', c('#5260c0')), tile=4.0, mix=0.45, afl=0.12)
    add('zinc', '#2d45a8', tex_zinc2('zinc', '#3049b0'), tile=3.0, ink=True, mix=0.45)
    add('terracotta', '#d0541c', ink=True, mix=0.45)
    add('wagon', '#1b2a8a', tint=True, ink=True, mix=0.45)
    add('wagon_red', KEPI, ink=True, mix=0.45)
    add('smoke', '#8f9ae8', mix=0.6)
    add('cardedge', '#f6d48a', ink=True, mix=0.4)
    add('box_ochre', '#f0a840', tint=True, ink=True, mix=0.4)
    # new v2 keys
    add('cobalt', COBALT, TX.plaster('v2_cobalt', c(COBALT), seed=31), tile=2.5, mix=0.4, afl=0.22)
    add('cobalt_paint', COBALT, TX.boards('v2_cobalt_boards', c('#2152d4'), seed=32, n=3), tile=1.0, tint=True, ink=True, mix=0.4)
    add('red', KEPI, tint=True, ink=True, mix=0.4)
    add('gold', '#ffbe3a', tint=True, ink=True, mix=0.35)
    add('amber_paint', AMBER, tint=True, ink=True, mix=0.4)
    add('tiles', '#b8481a', tex_checker('tiles2', '#c24a1a', '#d08a2c', n=8), tile=2.4, mix=0.45, afl=0.15)
    add('photowall', COBALT, tex_photowall(), tile=1.2, mix=0.4, afl=0.2)
    add('far', '#d29a5c', tex_facade_far(), tile=12.0, mix=0.55, afl=0.25)
    add('far_zinc', '#2a3f9a', tex_zinc2('far_zinc', '#2f46a8'), tile=3.0, mix=0.5, afl=0.12)
    add('far_stone', '#6a74d8', mix=0.6, afl=0.35)            # Notre-Dame silhouette in the blue haze
    add('horse', '#1c2160', ink=True, mix=0.5)
    add('green', '#1f8a3a', tint=True, ink=True, mix=0.45)
    add('chalk', '#1d5a4a', mix=0.45)
    add('carcass', '#b0561a', TX.boards('v2_carcass', c('#b0561a'), seed=33, n=3), tile=1.0, tint=True, ink=True, mix=0.45)
    add('pigeon', '#6f7ad8', ink=True, mix=0.5)
    add('geranium', '#e3262e', mix=0.4)
    add('leaf', '#2a8a3a', mix=0.45)
    return pl

# ================================================================ world state, locations (one collection each), sign / flag materials
W = {'take': None, 'locs': {}, 'doors': {}, 'marks': {}, 'light': {}, 'cutaway': [], 'cams': {}, 'life': {}, 'signs': {}, 'smoke': [], 'dust': []}
LOC_ORDER = ('roofs', 'street', 'facade', 'corridor', 'measure', 'archive')
def world_new():
    """fresh empty scene (bertillon.new_scene) with the v2 palette."""
    K.new_scene('SUNSET_INT'); K.STATE['PAL'] = _pal2(); K.STATE['ink_t'] = 0.010
    for k in ('take', 'cutaway'): W[k] = None if k == 'take' else []
    for k in ('locs', 'doors', 'marks', 'light', 'cams', 'life', 'signs'): W[k] = {}
    W['smoke'] = []; W['dust'] = []
    sc = bpy.context.scene; sc.cycles.max_bounces = 6; return sc
class Loc:
    """context: everything created inside goes to the collection 'loc_<name>', materials are made with that location's light preset, the
    location's sun and fill lights only light that collection (light linking)."""
    def __init__(self, name, light, over=None): self.name, self.light, self.over = name, light, over or {}
    def __enter__(self):
        P = dict(K.LIGHTS[self.light], **self.over)
        if 'shade_mul' in P: P['shade'] = tuple(x * P['shade_mul'] for x in P['shade']); P['tint'] = tuple(x * P['shade_mul'] for x in P['tint'])
        K.STATE['P'] = P; K.STATE['light'] = self.light; K._MATS.clear(); W['light'][self.name] = self.light
        self.before = set(o.name for o in bpy.data.objects); self.coll = bpy.data.collections.new('loc_' + self.name); bpy.context.scene.collection.children.link(self.coll)
        self.linked = []; W['locs'][self.name] = self; return self
    def link_light(self, ob): self.linked.append(ob); return ob
    def __exit__(self, *a):
        sc = bpy.context.scene
        for o in bpy.data.objects:
            if o.name in self.before: continue
            for c in list(o.users_collection): c.objects.unlink(o)
            self.coll.objects.link(o)
        for ob in self.linked: ob.light_linking.receiver_collection = self.coll
        return False
def P(): return K.STATE['P']
def face_rot(n):
    """z rotation (deg) that turns local -y (a sign's front) toward the horizontal direction n."""
    return math.degrees(math.atan2(n[0], -n[1]))
def _sign_mat(key, path, emit=0.35, two=False):
    m = bpy.data.materials.new(key); nt = K._mk_tree(m); N = nt.nodes.new; L = nt.links.new; Pp = P()
    out = N('ShaderNodeOutputMaterial'); it = N('ShaderNodeTexImage'); it.image = bpy.data.images.load(path, check_existing=True); it.interpolation = 'Linear'; it.extension = 'EXTEND'
    tc = N('ShaderNodeTexCoord'); L(tc.outputs['UV'], it.inputs[0]); dif = N('ShaderNodeBsdfDiffuse'); gk = N('ShaderNodeVectorMath'); gk.operation = 'SCALE'; gk.inputs['Scale'].default_value = Pp['gain']
    L(it.outputs['Color'], gk.inputs[0]); L(gk.outputs[0], dif.inputs['Color']); em = N('ShaderNodeEmission'); em.name = 'strength'; L(it.outputs['Color'], em.inputs[0]); em.inputs[1].default_value = emit
    ad = N('ShaderNodeAddShader'); L(dif.outputs[0], ad.inputs[0]); L(em.outputs[0], ad.inputs[1]); L(ad.outputs[0], out.inputs[0]); return m
def plane(name, c, size, rotz=0.0, mat=None, rotx=0.0, parent=None, back=None):
    """a UV-mapped rectangle whose FRONT faces local -y (text reads along +x), centre c, size (w, h) in the local xz plane. back: material key of a
    thin backing slab (None = none)."""
    w, h = size; me = bpy.data.meshes.new(name); me.from_pydata([(-w / 2, 0, -h / 2), (w / 2, 0, -h / 2), (w / 2, 0, h / 2), (-w / 2, 0, h / 2)], [], [(0, 1, 2, 3)]); me.update()
    uv = me.uv_layers.new(name='UVMap')
    for i, (u, v) in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uv.data[i].uv = (u, v)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); ob.location = c; ob.rotation_euler = (math.radians(rotx), 0, math.radians(rotz))
    if mat is not None: me.materials.append(mat)
    if parent is not None: ob.parent = parent
    return ob
def sign(B, text, w, h, c, n=(0, -1), fg=GOLD, bg=COBALT, font='serif', sub=None, emit=0.35, frame='#7a2a10', depth=0.06, two_sided=False, name=None, condense=0.84, maxh=0.62, board=True):
    """PIL text sign (PLAN §3e): a sharp text texture on a plane facing the horizontal direction n, with a painted board behind it (Batch B, 'walnut').
    w, h metres; c = centre (world). font: 'serif' (bundled Liberation Serif Bold, condensed 0.84) | 'sans' (Work Sans Black) | 'thai' (Kanit Black)
    | a .ttf path. Returns the sign object. Spell-check list: PRÉFECTURE DE POLICE, SERVICE D'IDENTIFICATION, ARCHIVES, PETIT, MOYEN, GRAND,
    MARTIN, 3 MOIS, 11 MESURES (PLAN §6.8)."""
    path = tex_sign(text, w, h, fg, bg, font, sub=sub, condense=condense, frame=frame, maxh=maxh); key = 'sign_' + os.path.basename(path)[3:-4]
    m = _sign_mat(key, path, emit); nn = np.array(n, float); nn /= np.linalg.norm(nn); rz = face_rot(nn)
    pc = np.array(c, float) + np.array([nn[0], nn[1], 0]) * (depth / 2 + 0.004)
    ob = plane(name or ('sg_' + ''.join(ch for ch in text if ch.isalnum())[:16]), tuple(pc), (w, h), rotz=rz, mat=m); ob.visible_shadow = False
    if board and B is not None: B.box('walnut', tuple(c), (w + 0.06, depth, h + 0.06), rot=(0, 0, rz))
    if two_sided:
        pb = np.array(c, float) - np.array([nn[0], nn[1], 0]) * (depth / 2 + 0.004); ob2 = plane(ob.name + '_b', tuple(pb), (w, h), rotz=rz + 180, mat=m); ob2.visible_shadow = False
    W['signs'][text] = ob; return ob

# ---------------------------------------------------------------- custom emitters / special materials (made inside the active Loc)
def _emit_mat(key, hexc, strength, camera_only=True):
    m = bpy.data.materials.new(key); nt = K._mk_tree(m); out = nt.nodes.new('ShaderNodeOutputMaterial'); e = nt.nodes.new('ShaderNodeEmission'); e.name = 'strength'
    e.inputs[0].default_value = (*hex_lin(hexc), 1); e.inputs[1].default_value = strength; nt.links.new(e.outputs[0], out.inputs[0]); K._MATS[key] = m
    K.STATE['glows'].append((m, strength)) if key in ('glow_amber', 'glow_candle', 'glow_lantern') else None
    return m
def _far_mat(key='far'):
    """roofscape skin: lit diffuse (ambient model of bertillon) + the lit windows of the texture as emission (amber texels only)."""
    m = K._lit_mat(key, K.STATE['PAL'][key]); nt = m.node_tree; N = nt.nodes.new; L = nt.links.new
    it = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeTexImage'][0]; sep = N('ShaderNodeSeparateColor'); L(it.outputs['Color'], sep.inputs[0])
    gt = N('ShaderNodeMath'); gt.operation = 'GREATER_THAN'; gt.inputs[1].default_value = 0.85; L(sep.outputs[0], gt.inputs[0])
    gt2 = N('ShaderNodeMath'); gt2.operation = 'LESS_THAN'; gt2.inputs[1].default_value = 0.2; L(sep.outputs[2], gt2.inputs[0]); mu = N('ShaderNodeMath'); mu.operation = 'MULTIPLY'; L(gt.outputs[0], mu.inputs[0]); L(gt2.outputs[0], mu.inputs[1])
    em = N('ShaderNodeEmission'); em.inputs[0].default_value = (*hex_lin('#ffae3e'), 1); L(mu.outputs[0], em.inputs[1]); em.name = 'strength'
    outn = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeOutputMaterial'][0]; prev = outn.inputs[0].links[0].from_socket; ad = N('ShaderNodeAddShader'); L(prev, ad.inputs[0]); L(em.outputs[0], ad.inputs[1]); L(ad.outputs[0], outn.inputs[0])
    sc = N('ShaderNodeMath'); sc.operation = 'MULTIPLY'; sc.inputs[1].default_value = 3.2 * P().get('glow', 1.0); L(mu.outputs[0], sc.inputs[0]); L(sc.outputs[0], em.inputs[1])
    K._MATS[key] = m; return m
def _water_mat(key='water'):
    m = bpy.data.materials.new(key); nt = K._mk_tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); gl = N('ShaderNodeBsdfGlossy'); gl.inputs['Roughness'].default_value = 0.06; gl.inputs['Color'].default_value = (0.75, 0.8, 1.0, 1)
    df = N('ShaderNodeEmission'); df.inputs[0].default_value = (*hex_lin('#1a34a8'), 1); df.inputs[1].default_value = 0.55; mx = N('ShaderNodeAddShader'); L(df.outputs[0], mx.inputs[0]); L(gl.outputs[0], mx.inputs[1]); L(mx.outputs[0], out.inputs[0])
    K._MATS[key] = m; return m
def _sky_mat2(key='sky2'):
    """v2 dusk dome: thin amber horizon -> cobalt -> zenith #1A3FB8 on the view direction's z (object coords, the dome is centred near the world)."""
    Pp = P(); m = bpy.data.materials.new(key); nt = K._mk_tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); tc = N('ShaderNodeTexCoord'); nr = N('ShaderNodeVectorMath'); nr.operation = 'NORMALIZE'; L(tc.outputs['Object'], nr.inputs[0])
    sp = N('ShaderNodeSeparateXYZ'); L(nr.outputs[0], sp.inputs[0]); cr = N('ShaderNodeValToRGB'); L(sp.outputs['Z'], cr.inputs[0]); e = N('ShaderNodeEmission')
    top, mid, bot = Pp['sky']; el = cr.color_ramp.elements; el[0].position = 0.0; el[0].color = (*hex_lin(bot), 1); el[1].position = 0.55; el[1].color = (*hex_lin(top), 1)
    e1 = el.new(0.035); e1.color = (*hex_lin('#ff8a4a'), 1); e2 = el.new(0.09); e2.color = (*hex_lin('#7a5ad8'), 1); e3 = el.new(0.2); e3.color = (*hex_lin(mid), 1)
    L(cr.outputs[0], e.inputs[0]); e.inputs[1].default_value = Pp.get('sky_k', 1.0); L(e.outputs[0], out.inputs[0]); K._MATS[key] = m; return m
def _custom_glows():
    Pp = P(); g = Pp.get('glow', 1.0)
    _emit_mat('glow_amber', '#ffa62b', 9.0 * g); _emit_mat('glow_candle', '#ffb24a', 12.0 * g); _emit_mat('glow_lantern', '#ffbe5a', 10.0 * g)
    _emit_mat('glow_blue', '#4f7ef0', 2.2); _emit_mat('glow_redsign', '#ff3a2a', 3.0); _emit_mat('glow_quay', '#ffb44a', 7.0 * g); _emit_mat('glow_reflect', '#ff9a30', 2.2)
    _emit_mat('glow_rose', '#ffb050', 4.0 * g); _emit_mat('glow_sil', '#2a1b5a', 1.0); _emit_mat('glow_fan', '#ffb050', 1.4)
    m = _emit_mat('glow_win', '#ffa640', 1.7 * min(g, 1.2)); K.STATE['glows'].append((m, 1.7 * min(g, 1.2)))          # amber, never white (v2 overrides v1 glow_win)
_LocEnter = Loc.__enter__
def _loc_enter(self):
    r = _LocEnter(self); _custom_glows(); return r
Loc.__enter__ = _loc_enter

def _finalize(B, prefix, ink=True, ink_t=None, shadow=True):
    objs = B.finalize(prefix, ink=ink, ink_t=ink_t)
    if not shadow:
        for o in objs: o.visible_shadow = False
    return objs
def lift(B, z=FZ):
    """props of bertillon.py stand on z = 0: wrap them in `with lift(B):` to stand them on the interior floor."""
    return B.xf((0, 0, z))

# ================================================================ 3a. rooftop plate, Seine, Notre-Dame (far: no ink, low-poly, shadow-less)
ND = (120.0, 135.0)          # Notre-Dame (west towers) - the Préfecture's real neighbour on the Île de la Cité. No Eiffel Tower (1887-89).
SEINE = (95.0, 118.0)
def paris_roofscape(r=220.0, seed=7):
    """the plate under BIGZOOM 1 and the crane shots: ~300 low-poly blocks (ochre skin with lit amber windows 60 %, cobalt zinc roofs) out to r,
    chimney pots (smoke sources), the Seine strip with amber quay lamps and their reflections, the Notre-Dame silhouette. Returns chimney tops."""
    B = Batch(seed); rng = random.Random(seed); tops = []
    for gx in np.arange(-r, r + 1, 25.0):
        for gy in np.arange(-r * 0.6, r + 1, 22.0):
            cx, cy = gx + rng.uniform(-3, 3), gy + rng.uniform(-3, 3)
            if math.hypot(cx, cy - 40) > r: continue
            if abs(cx) < 19 and -24 < cy < 72: continue                                  # the detailed street rows
            if -3 < cx < 30 and -8 < cy < 44: continue                                    # the Préfecture block
            if SEINE[0] - 12 < cy < SEINE[1] + 12: continue
            if abs(cx - ND[0]) < 34 and 124 < cy < 270: continue
            w, d = rng.uniform(15, 21), rng.uniform(13, 19); h = rng.uniform(13, 19); rot = rng.choice((0, 90))
            B.box('far', (cx, cy, h / 2 - 1.0), (w, d, h)); B.box('far_zinc', (cx, cy, h + 0.9 - 1.0), (w - 0.6, d - 0.6, 1.8))
            B.prism_roof('far_zinc', (cx, cy, h + 1.8 - 1.0), w - 1.2, d - 1.2, 1.6, rot_z=rot, ridge_frac=0.7)
            if math.hypot(cx, cy - 10) < 90:                                            # near blocks: dormers on all four slopes (lit 40 %)
                for sx, sy, nx, ny in ((0, -1, 0, -1), (0, 1, 0, 1), (-1, 0, -1, 0), (1, 0, 1, 0)):
                    L_ = w if sy else d; n_ = 3 if L_ > 15 else 2
                    for k in range(n_):
                        t_ = (k + 0.5) / n_ - 0.5; px = cx + (t_ * (w - 4) if sy else sx * (w / 2 - 0.9)); py = cy + (t_ * (d - 4) if sx else sy * (d / 2 - 0.9)); zz = h + 0.75
                        B.box('far', (px, py, zz), (1.3 if sy else 0.9, 0.9 if sy else 1.3, 1.5)); B.box('glow_win' if rng.random() < 0.4 else 'dark', (px + nx * (0.46), py + ny * 0.46, zz), (0.06 if sx else 0.7, 0.7 if sx else 0.06, 0.9))
            for k in range(2):
                px, py = cx + rng.uniform(-w * 0.35, w * 0.35), cy + rng.uniform(-d * 0.3, d * 0.3); B.box('terracotta', (px, py, h + 2.4), (0.9, 0.6, 2.0)); tops.append((px, py, h + 3.6))
    # the ground under the plate (setts, no void between the blocks) + street lamps at the block corners
    for (ya, yb) in ((-r * 0.6 - 30, SEINE[0] - 5.0), (SEINE[1] + 5.0, r + 60)): B.box('cobble', (0, (ya + yb) / 2, -0.25), (2 * r + 80, yb - ya, 0.3))
    for gx in np.arange(-r + 12.5, r, 25.0):
        for gy in np.arange(-r * 0.6 + 11, r, 22.0):
            if math.hypot(gx, gy - 40) > r * 0.8 or (abs(gx) < 20 and -24 < gy < 72) or (-3 < gx < 30 and -8 < gy < 44) or SEINE[0] - 8 < gy < SEINE[1] + 8: continue
            B.cyl('iron', (gx, gy, 2.0), 0.08, 4.0, seg=6); B.sphere('glow_quay', (gx, gy, 4.1), 0.32, seg=8, rings=5); B.box('glow_reflect', (gx, gy, -0.08), (2.2, 2.2, 0.02))
    # the Seine: water, quay walls, lamp line and amber reflections
    y0, y1 = SEINE; B.box('stone_dk', (0, y0 - 2.5, -1.0), (2 * r, 5.0, 2.0)); B.box('stone_dk', (0, y1 + 2.5, -1.0), (2 * r, 5.0, 2.0))
    _water_mat(); B.box('water', (0, (y0 + y1) / 2, -2.4), (2 * r, y1 - y0, 0.1))
    for x in np.arange(-r + 6, r, 14.0):
        for yy, s in ((y0 - 1.0, 1), (y1 + 1.0, -1)):
            B.cyl('iron', (x, yy, 2.0), 0.08, 4.0, seg=6); B.sphere('glow_quay', (x, yy, 4.1), 0.35, seg=8, rings=5)
            B.box('glow_reflect', (x, yy + s * 3.2, -2.33), (0.35, 5.0, 0.01))
    # a bridge (Pont Saint-Michel side) across the far end of the street axis
    for k in range(4):
        B.box('stone', (0, y0 + 2.5 + k * 5.5, -0.2), (14.0, 5.6, 0.6)); B.cyl('stone_dk', (0, y0 + 5.2 + k * 5.5, -1.6), 2.4, 14.0, axis='x', seg=12)
    for x in (-7, 7): B.box('stone', (x, (y0 + y1) / 2, 0.55), (0.4, y1 - y0 + 4, 0.9))
    # Notre-Dame: 2 west towers, the west front with the rose (amber), portals, the nave roof and the flèche (spire)
    x0, yN = ND
    for sx in (-1, 1):
        B.box('far_stone', (x0 + sx * 13.5, yN, 31.0), (12.5, 12.5, 62.0)); B.box('far_stone', (x0 + sx * 13.5, yN, 62.6), (13.6, 13.6, 1.2))
        for k in range(2): B.box('glow_sil', (x0 + sx * 13.5 + (k - 0.5) * 4.2, yN - 6.3, 52.0), (1.6, 0.1, 8.0))
    B.box('far_stone', (x0, yN + 1.0, 22.0), (16.0, 10.5, 44.0)); B.box('far_stone', (x0, yN - 0.6, 45.0), (42.0, 9.0, 2.0))
    rose = 24; a = np.linspace(0, 2 * math.pi, rose, endpoint=False); v = [(0, 0, 0)] + [(4.6 * math.cos(t), 0, 4.6 * math.sin(t)) for t in a]
    with B.xf((x0, yN - 5.0, 33.0)): B.mesh('glow_rose', v, [(0, 1 + i, 1 + (i + 1) % rose) for i in range(rose)], smooth=False)
    for k in (-1, 0, 1): B.box('glow_rose', (x0 + k * 12.0, yN - 6.4, 5.0), (4.2 if k == 0 else 3.4, 0.1, 9.0))
    B.box('far_stone', (x0, yN + 60.0, 17.0), (30.0, 100.0, 34.0)); B.prism_roof('far_zinc', (x0, yN + 60.0, 34.0), 100.0, 30.0, 13.0, rot_z=90)
    B.cyl('far_zinc', (x0, yN + 72.0, 62.0), 1.8, 34.0, r2=0.05, seg=8)
    objs = _finalize(B, 'roofs', ink=False, shadow=False)
    for o in objs: o.visible_shadow = False
    return tops

# ================================================================ 3a. the street at dusk (connected world version of v1 `street`)
def horse(B, c, rot=0, scale=1.0):
    """black low-poly cart horse standing in shafts (head toward local +y), red harness collar, brass hames, a nosebag-free head. returns the nose (world)."""
    with B.xf((c[0], c[1], c[2] if len(c) > 2 else 0), (0, 0, rot), scale):
        B.sphere('horse', (0, 0, 1.38), 1.0, scale=(0.36, 0.95, 0.42)); B.sphere('horse', (0, 0.62, 1.42), 1.0, scale=(0.34, 0.42, 0.42)); B.sphere('horse', (0, -0.62, 1.4), 1.0, scale=(0.36, 0.42, 0.42))
        B.cyl('horse', (0, 1.05, 1.82), 0.2, 0.9, r2=0.15, rot=(-38, 0, 0), seg=10); B.box('horse', (0, 1.42, 2.08), (0.2, 0.6, 0.26), rot=(28, 0, 0)); B.box('horse', (0, 1.66, 1.98), (0.18, 0.3, 0.2), rot=(40, 0, 0))
        for sx in (-1, 1): B.box('horse', (sx * 0.07, 1.3, 2.33), (0.05, 0.08, 0.16), rot=(10, 0, 0))
        B.box('dark', (0, 1.0, 2.05), (0.06, 0.55, 0.2), rot=(-38, 0, 0))                                                   # mane
        for sx in (-1, 1):
            for sy in (-0.62, 0.6):
                B.cyl('horse', (sx * 0.2, sy, 0.62), 0.08, 1.05, r2=0.06, seg=8); B.cyl('dark', (sx * 0.2, sy, 0.06), 0.08, 0.12, seg=8)
        B.cyl('dark', (0, -1.0, 1.2), 0.07, 0.8, r2=0.03, rot=(20, 0, 0), seg=6)                                             # tail
        B.cyl('red', (0, 0.9, 1.62), 0.3, 0.12, rot=(-40, 0, 0), seg=14); B.box('brass', (0, 0.9, 1.95), (0.5, 0.06, 0.06), rot=(-40, 0, 0))   # collar + hames
        B.box('leather', (0, -0.1, 1.83), (0.75, 0.25, 0.05))
        nose = B.wpt((0, 1.82, 1.9))
    return nose
def police_wagon_v2(name, c, rot=0):
    """the v1 Black Maria + its horse in the shafts, all children of one root empty (hook set_wagon(t) drives it in along local +y)."""
    root = bpy.data.objects.new(name + '_root', None); bpy.context.scene.collection.objects.link(root); root.location = c; root.rotation_euler = (0, 0, math.radians(rot))
    B = Batch(41); K.police_wagon(B, (0, 0), rot=0); nose = horse(B, (0, 3.2, 0)); _finalize(B, name, ink_t=0.012)
    for o in bpy.data.objects:
        if o.name.startswith(name + '_') and o.parent is None and o is not root: o.parent = root
    for o in bpy.context.scene.collection.objects:
        if o.type == 'LIGHT' and o.name.startswith('wagon_lamp') and o.parent is None: o.location = Vector(o.location) - Vector(c) if False else o.location; o.parent = root; o.location = Vector((-0.9, 1.9, 2.45))
    W['wagon'] = dict(root=root, home=tuple(c), rot=rot, nose_local=(0, 3.2 + 1.82, 1.9)); return root
def fiacre(B, c, rot=0):
    """a fiacre (hackney cab): yellow-red body with a black hood, two big wheels, coachman's box, a horse."""
    with B.xf((c[0], c[1], 0), (0, 0, rot)):
        B.box('amber_paint', (0, 0, 1.25), (1.35, 1.6, 0.9)); B.box('red', (0, 0, 0.78), (1.4, 1.65, 0.08)); B.box('dark', (0, 0.0, 1.4), (1.37, 0.9, 0.5))
        B.box('cloth', (0, -0.45, 1.95), (1.35, 1.0, 0.25)); B.box('cloth', (0, 0.2, 1.8), (1.3, 0.1, 0.6))
        for sx in (-1, 1):
            for yy, rr in ((-0.55, 0.62), (0.75, 0.45)):
                B.cyl('red', (sx * 0.75, yy, rr), rr, 0.07, axis='x', seg=20); B.cyl('brass', (sx * 0.8, yy, rr), 0.06, 0.06, axis='x', seg=8)
                for k in range(6): B.box('iron', (sx * 0.78, yy, rr), (0.03, 0.03, rr * 1.8), rot=(k * 30, 0, 0))
        B.box('dark', (0, 1.05, 1.5), (0.9, 0.5, 0.12)); B.box('leather', (0, 1.0, 1.65), (0.7, 0.35, 0.2))
        for sx in (-1, 1): B.box('iron', (sx * 0.35, 1.9, 0.95), (0.05, 1.6, 0.05))
        B.cyl('brass', (0.6, 0.85, 1.75), 0.05, 0.2, seg=8); B.sphere('glow_lantern', (0.6, 0.85, 1.92), 0.08)
    return horse(B, (c[0], c[1], 0), rot=rot) if False else horse(B, tuple(B.wpt((0, 0, 0)) if False else (c[0] + 2.9 * -math.sin(math.radians(rot)), c[1] + 2.9 * math.cos(math.radians(rot)), 0)), rot=rot)
def morris_column(B, c, posters=(('CIRQUE', '#D7262E', '#FFC94A'), ('THÉÂTRE', '#1F4FD0', '#FFC94A'), ('LE PETIT JOURNAL', '#FFA62B', '#1A3FB8'))):
    x, y = c; B.cyl('green', (x, y, 1.3), 0.62, 2.6, seg=20); B.cyl('green', (x, y, 2.75), 0.72, 0.18, r2=0.66, seg=20); B.cyl('green', (x, y, 3.05), 0.62, 0.45, r2=0.05, seg=20)
    B.cyl('green', (x, y, 0.12), 0.72, 0.24, seg=20); B.sphere('gold', (x, y, 3.3), 0.1)
    for k, (t, bg, fg) in enumerate(posters):
        a = math.radians(-160 + k * 62); n = (math.cos(a), math.sin(a)); sign(None, t, 0.72, 0.95, (x + 0.64 * n[0], y + 0.64 * n[1], 1.7), n=n, fg=fg, bg=bg, font='serif', emit=0.25, board=False, maxh=0.3)
def kiosk(B, c):
    """green Paris news kiosk: octagonal body, dome, a ring of posters (colour blocks) and the crown."""
    x, y = c; B.cyl('green', (x, y, 1.2), 1.0, 2.4, seg=8); B.cyl('amber_paint', (x, y, 2.0), 1.02, 0.6, seg=8); B.cyl('green', (x, y, 2.55), 1.35, 0.12, seg=8)
    B.cyl('green', (x, y, 2.95), 1.1, 0.7, r2=0.2, seg=8); B.sphere('gold', (x, y, 3.4), 0.14)
    for k in range(8): a = k * math.pi / 4; B.box(['red', 'cobalt_paint', 'amber_paint', 'cream'][k % 4], (x + 1.02 * math.cos(a), y + 1.02 * math.sin(a), 1.25), (0.08, 0.5, 0.7), rot=(0, 0, math.degrees(a)))
def cafe_terrace(B, x, y0, y1, side=-1):
    """café on the left row (façade at x = -6): red/cobalt striped awning out over the pavement, round tables, bistro chairs, a lamp."""
    fx = -6.0 + 0.02; n = int((y1 - y0) / 0.9)
    for k in range(n): B.box('red' if k % 2 == 0 else 'cobalt_paint', (fx + 1.3, y0 + (k + 0.5) * (y1 - y0) / n, 3.0), (2.6, (y1 - y0) / n, 0.06), rot=(0, 16, 0))
    B.box('red', (fx + 2.55, (y0 + y1) / 2, 2.62), (0.04, y1 - y0, 0.3))
    for k, yy in enumerate(np.arange(y0 + 0.8, y1 - 0.4, 1.6)):
        xx = fx + 1.0 + (k % 2) * 0.5; B.cyl('iron', (xx, yy, 0.37), 0.03, 0.74, seg=6); B.cyl('gold', (xx, yy, 0.75), 0.32, 0.03, seg=14); B.cyl('iron', (xx, yy, 0.03), 0.2, 0.04, seg=10)
        for a in (0, 180):
            cx, cy = xx + 0.45 * math.cos(math.radians(a + 30 * k)), yy + 0.45 * math.sin(math.radians(a + 30 * k))
            B.cyl('red', (cx, cy, 0.46), 0.18, 0.04, seg=10); B.box('iron', (cx, cy, 0.23), (0.03, 0.03, 0.46)); B.box('red', (cx - 0.17 * math.cos(math.radians(a + 30 * k)), cy - 0.17 * math.sin(math.radians(a + 30 * k)), 0.72), (0.06, 0.32, 0.5), rot=(0, 0, a + 30 * k))
        B.cyl('glass', (xx, yy, 0.82), 0.03, 0.12, seg=6)
    sign(B, 'CAFÉ DU PALAIS', 3.4, 0.5, (fx + 0.06, (y0 + y1) / 2, 3.55), n=(1, 0), fg=GOLD, bg=KEPI, emit=0.45)
def pigeons(B, pts, seed=3):
    r = random.Random(seed)
    for (x, y, z) in pts:
        a = r.uniform(0, 360); B.sphere('pigeon', (x, y, z + 0.09), 0.1, scale=(1.0, 0.65, 0.7), seg=10, rings=6); B.sphere('pigeon', (x + 0.08 * math.cos(math.radians(a)), y + 0.08 * math.sin(math.radians(a)), z + 0.17), 0.05, seg=8, rings=5)
def flag(name, root_pt, direction, length=1.6, height=1.05, pole_mat='gold', B=None):
    """a tricolour on a pole leaning out of the façade: the cloth is a subdivided plane with a WAVE modifier (moves by itself with the frame)."""
    d = np.array(direction, float); d /= np.linalg.norm(d); tip = np.array(root_pt) + d * 2.6
    if B is not None: B.cyl(pole_mat, tuple((np.array(root_pt) + tip) / 2), 0.04, 2.6, rot=K.euler_to_z(d), seg=8); B.sphere('gold', tuple(tip), 0.07)
    nx, nz = 16, 8; V = []; F = []
    for j in range(nz + 1):
        for i in range(nx + 1): V.append((i / nx * length, 0, -j / nz * height))
    for j in range(nz):
        for i in range(nx): F.append((j * (nx + 1) + i, j * (nx + 1) + i + 1, (j + 1) * (nx + 1) + i + 1, (j + 1) * (nx + 1) + i))
    me = bpy.data.meshes.new(name); me.from_pydata(V, [], F); me.update(); uv = me.uv_layers.new(name='UVMap')
    for poly in me.polygons:
        for li in poly.loop_indices: v = V[me.loops[li].vertex_index]; uv.data[li].uv = (v[0] / length, 1 + v[2] / height)
    m = _sign_mat(name + '_m', tex_flag(), emit=0.15); me.materials.append(m)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); top = np.array(root_pt) + d * 2.5; ob.location = tuple(top)
    hz = math.degrees(math.atan2(d[1], d[0])); ob.rotation_euler = (0, 0, math.radians(hz + 180))
    wv = ob.modifiers.new('wave', 'WAVE'); wv.use_x = True; wv.use_y = False; wv.height = 0.09; wv.width = 0.55; wv.narrowness = 1.2; wv.speed = 0.06; wv.time_offset = -random.Random(len(name)).uniform(0, 30)
    wv.start_position_x = 0; wv.falloff_radius = 0; wv.use_normal = False
    wv.use_normal = True; wv.use_normal_y = True; wv.use_normal_x = False; wv.use_normal_z = False
    sb = ob.modifiers.new('sub', 'SUBSURF'); sb.levels = 1; sb.render_levels = 1; ob.visible_shadow = True
    return ob
def roof_back(B, c, w, d, h_wall, h_roof, rot, seed=1):
    """dormers + a lit skylight on the BACK slope of a v1 mansard block (v1 only dresses the street side)."""
    rr = random.Random(seed + 99); nw = max(2, int(w / 2.4))
    with B.xf((c[0], c[1], c[2]), (0, 0, rot)):
        for k in range(nw):
            x = (k + 0.5) * w / nw - w / 2; on = rr.random() < 0.45; zz = h_wall + 0.2 + h_roof * 0.3
            B.box('stone_dk', (x, d / 2 - 0.05, zz), (0.8, 0.5, 1.0)); B.box('glow_win' if on else 'dark', (x, d / 2 + 0.2, zz), (0.5, 0.03, 0.7))
            B.prism_roof('zinc', (x, d / 2 - 0.1, zz + 0.5), 0.9, 0.7, 0.3, rot_z=90)
def build_street2(B, A):
    """PLAN §3a: v1 street (setts, kerbs, 2 rows of Haussmann blocks, shopfronts, 16 lamps, puddles) + café terrace, Morris column with posters,
    kiosk, fiacre, the Black Maria WITH its horse, barrels / flower cart (foreground layer), pigeons; the right row gives way to the Préfecture."""
    r = random.Random(11); L0, L1 = -24.0, 64.0; M = A['marks']; lit = P().get('win_lit', 0.7)
    B.box('cobble', (0, (L0 + L1) / 2, -0.06), (8.0, L1 - L0, 0.12))
    for sx in (-1, 1):
        B.box('stone_dk', (sx * 5.0, (L0 + L1) / 2, 0.0), (2.0, L1 - L0, 0.28)); B.box('stone', (sx * 4.05, (L0 + L1) / 2, 0.0), (0.18, L1 - L0, 0.3))
    y = L0 - 1.0; i = 0
    while y < L1 - 6:
        w = r.uniform(8, 11); hw = r.uniform(12.5, 15.5); K.mansard(B, (-11.0, y + w / 2, 0), w, 10.0, hw, h_roof=2.6, rot=90, chimneys=2, seed=30 + i, stone='stone' if i % 2 else 'stone_dk', lit=lit)
        roof_back(B, (-11.0, y + w / 2, 0), w, 10.0, hw, 2.6, 90, seed=30 + i)
        if not (16.0 < y + w / 2 < 26.0): K.shop(B, (-6.0, y + w / 2), w, rot=90, seed=i)
        y += w + 0.2; i += 1
    for (ya, yb) in ((L0 - 1.0, -2.0), (38.0, L1 - 4.0)):                       # the right row outside the Préfecture block (y -2 .. 37.5)
        y = ya; i = 0
        while y < yb - 2:
            w = min(r.uniform(8, 11), yb - y); hw = r.uniform(12.5, 15.5)
            K.mansard(B, (11.0, y + w / 2, 0), w, 10.0, hw, h_roof=2.6, rot=-90, chimneys=2, seed=50 + i + int(ya), stone='stone_dk' if i % 2 else 'stone', lit=lit)
            K.shop(B, (6.0, y + w / 2), w, rot=-90, seed=i + 7); y += w + 0.2; i += 1
    K.mansard(B, (0, L1 + 5.0, 0), 22.0, 10.0, 15.0, h_roof=2.6, rot=0, chimneys=3, seed=70, lit=lit)
    lamps = []
    for yy in (-10.0, -2.0, 6.0, 14.0, 22.0, 30.0, 38.0, 46.0, 54.0):
        K.street_lamp(B, (-4.3, yy, 0.0), h=4.2, rot=0); lamps.append((-4.3, yy))
        if not (3.0 < yy + 3.0 < 9.0): K.street_lamp(B, (4.3, yy + 3.0, 0.0), h=4.2, rot=0, watts=420); lamps.append((4.3, yy + 3.0))     # dimmer: they stand 1 m from the ochre façade
    A['lamps'] = lamps
    cafe_terrace(B, -6.0, 17.0, 25.0); morris_column(B, (-4.75, 9.5)); kiosk(B, (-4.9, 31.0))
    A['fiacre_nose'] = fiacre(B, (-1.7, 27.0), rot=180)
    for (bx, by) in ((-4.7, 2.6), (-4.75, 3.25), (4.75, -4.0), (4.6, 0.6)):
        B.cyl('walnut', (bx, by, 0.55), 0.3, 0.8, seg=12); B.cyl('iron', (bx, by, 0.35), 0.31, 0.04, seg=12); B.cyl('iron', (bx, by, 0.75), 0.31, 0.04, seg=12)
    # flower cart (foreground layer for the street travelling)
    with B.xf((-3.2, -1.0, 0), (0, 0, 20)):
        B.box('honey', (0, 0, 0.75), (1.4, 0.8, 0.12)); B.box('honey', (0, 0, 0.95), (1.4, 0.8, 0.3)) if False else None
        for sx in (-1, 1): B.cyl('red', (sx * 0.45, -0.45, 0.35), 0.35, 0.06, axis='y', seg=14)
        B.box('walnut', (0, 0.75, 0.6), (0.06, 1.2, 0.06))
        for k in range(14): B.sphere(['geranium', 'gold', 'geranium', 'cobalt_paint', 'leaf'][k % 5], (-0.55 + (k % 7) * 0.18, -0.2 + (k // 7) * 0.4, 0.9 + 0.08 * (k % 3)), 0.12, seg=8, rings=5)
    K.puddles(B, [(-1.0, 1.4, 0.7, 0.45, 20), (1.4, 5.2, 0.9, 0.5, -10), (-0.2, 11.0, 1.4, 0.9, 5), (2.2, 14.0, 1.8, 1.0, 30), (-2.0, 17.0, 1.5, 0.8, 0), (0.0, 25.0, 2.0, 1.1, 10), (-1.8, 7.5, 0.9, 0.6, 40), (1.6, -3.0, 1.3, 0.8, 15), (-2.2, 34.0, 1.6, 0.9, -5)])
    police_wagon_v2('wagon', (3.0, 8.6, 0), rot=0); A['wagon'] = (3.0, 8.6)
    B.box('stone', (0.3, 3.7, 0.07), (1.2, 2.4, 0.14)); K.street_lamp(B, (0.3, 3.7, 0.14), h=4.0, watts=500, rot=0)       # refuge island + lamp post: the 1d fg layer
    pigeons(B, [(-5.6, 3.9, 0.15), (-5.4, 4.3, 0.15), (-2.6, 12.5, 0.0), (-2.1, 12.2, 0.0), (-2.4, 12.9, 0.0)])
    # crowd anchor points (feet; x, y, z, facing deg, who)
    M.update({'flaneur_a': (-2.4, 4.0, 0.0, 20, 'clerk'), 'flaneur_b': (-4.9, 15.0, 0.14, 160, 'clerk'), 'newsboy': (-4.9, 7.6, 0.14, 60, 'prisoner'),
              'lamplighter': (-3.85, 14.0, 1.05, 200, 'clerk'), 'cafe_a': (-4.6, 19.4, 0.14, 90, 'clerk'), 'cafe_b': (-4.3, 22.6, 0.14, 120, 'prisoner'),
              'fiacre_cab': (-1.7, 27.4, 1.7, 180, 'clerk'), 'wagon_door': (3.0, 6.3, 0.0, 180, 'gendarme'), 'wagon_step': (2.2, 6.0, 0.0, 200, 'prisoner'),
              'gend_wagon': (3.9, 6.0, 0.0, 200, 'gendarme'), 'wagon_driver': (3.0, 10.2, 2.1, 0, 'gendarme')})
    with B.xf((-3.85, 14.35, 0)): K.rolling_ladder(B, (0.0, 0.25, 0.0), (0.35, -0.05, 3.75), width=0.42, rungs=11)
    return A

# ================================================================ 3b. the Préfecture façade (faces -x at x = FACADE_X), main door hook, French window
BAYS = (0.9, 3.25, 5.7, 8.2, 10.7, 13.2, 16.4, 19.6, 22.8, 26.0, 29.2, 32.4, 35.6)
def build_facade(B, A):
    """3 storeys + mansard, ochre ashlar, cobalt shutters, the arched main door (set_door('main')), the PRÉFECTURE DE POLICE band with a lantern
    each side, sentry box, steps, flags, the measuring room's open French window (no bars; set_window), other windows lit with silhouettes."""
    fx = FACADE_X; t = 0.25; Y0, Y1 = -1.6, 37.6; Hc = 14.2; r = random.Random(17); M = A['marks']; lit = 0.6
    door = (4.6, 6.8, 0.14, 4.4); mwin = (12.0, 14.4, 1.35, 4.6)                 # the French window goes to the floor (z 1.35-4.6, see API.md)
    K.wall_box(B, 'stone_dk', 'x', 5.7, Y0, Y1, 0.0, 5.6, [door, mwin], out=-1, t=t); K.wall_box(B, 'stone', 'x', 5.7, Y0, Y1, 5.6, Hc, [], out=-1, t=t)
    for (ya, yb) in ((Y0 - 0.25, Y0), (Y1, Y1 + 0.25)): B.box('stone', (fx + 4.0, (ya + yb) / 2, Hc / 2), (8.5, 0.25, Hc))       # return walls
    for z, hh, pr in ((0.45, 0.6, 0.12), (5.45, 0.3, 0.16), (9.75, 0.22, 0.12), (Hc - 0.2, 0.5, 0.35)): B.box('stone_dk', (fx - pr / 2, (Y0 + Y1) / 2, z), (pr, Y1 - Y0, hh))
    for yy in (Y0 + 0.3, 2.05, 9.45, 11.55, 14.8, 18.0, 21.2, 24.4, 27.6, 30.8, 34.0, Y1 - 0.3): B.box('stone', (fx - 0.08, yy, 7.0), (0.16, 0.55, 12.6))
    # windows: ground floor barred and lit; first floor with balconies; second floor; cobalt shutters; silhouettes in some lit windows
    for b in BAYS:
        for (z0, z1, fl) in ((2.6, 4.4, 0), (6.6, 9.0, 1), (10.4, 12.6, 2)):
            if fl == 0 and (abs(b - 5.7) < 1.5 or abs(b - 13.2) < 1.5): continue
            w = 1.3 if fl else 1.25; on = r.random() < (lit if fl else 0.25); zc = (z0 + z1) / 2
            B.box('glow_win' if on else 'dark', (fx - 0.01, b, zc), (0.02, w, z1 - z0))
            if on and r.random() < 0.45: B.box('glow_sil', (fx - 0.02, b + r.uniform(-0.25, 0.25), z0 + 0.65), (0.01, 0.42, 1.25))
            B.box('stone_dk', (fx - 0.06, b, z1 + 0.14), (0.12, w + 0.4, 0.22)); B.box('stone_dk', (fx - 0.1, b, z0 - 0.08), (0.2, w + 0.3, 0.12))
            B.box('cobalt_paint', (fx - 0.05, b, zc), (0.04, 0.06, z1 - z0)); B.box('cobalt_paint', (fx - 0.05, b, z0 + (z1 - z0) * 0.62), (0.04, w, 0.05))
            if fl:
                for s in (-1, 1): B.box('cobalt_paint', (fx - 0.06, b + s * (w / 2 + 0.36), zc), (0.06, 0.66, z1 - z0 + 0.05), tint=0.95)
            if fl == 0:
                for k in range(5): B.cyl('iron', (fx - 0.1, b - 0.5 + k * 0.25, zc), 0.022, z1 - z0, seg=6)
            if fl == 1:
                B.box('iron', (fx - 0.45, b, z0 - 0.02), (0.9, w + 0.7, 0.08)); B.box('iron', (fx - 0.88, b, z0 + 0.45), (0.04, w + 0.7, 0.04))
                for k in range(9): B.box('iron', (fx - 0.88, b - (w + 0.7) / 2 + k * (w + 0.7) / 8, z0 + 0.22), (0.03, 0.03, 0.45))
    pigeons(B, [(fx - 0.15, 16.2, 10.36), (fx - 0.15, 16.6, 10.36), (fx - 0.2, 22.6, 10.36), (fx - 0.92, 8.0, 6.62), (fx - 0.15, 29.0, 2.55)])
    # mansard roof over the whole block, dormers, chimneys; archive skylights glazing (seen from the crane / BIGZOOM 1)
    xb = fx + 8.3; dep = 16.6
    B.box('zinc', (xb, (Y0 + Y1) / 2, Hc + 1.2), (dep, Y1 - Y0 + 0.3, 2.4)); B.prism_roof('zinc', (xb, (Y0 + Y1) / 2, Hc + 2.4), Y1 - Y0 + 0.3, dep, 1.4, rot_z=90, ridge_frac=0.9)
    B.box('stone_dk', (fx + 0.2, (Y0 + Y1) / 2, Hc + 0.05), (0.5, Y1 - Y0, 0.3))
    for b in BAYS:
        on = r.random() < 0.6; B.box('stone_dk', (fx + 0.55, b, Hc + 1.25), (0.6, 1.1, 1.5)); B.box('glow_win' if on else 'dark', (fx + 0.24, b, Hc + 1.2), (0.03, 0.7, 1.0))
        B.prism_roof('zinc', (fx + 0.6, b, Hc + 2.0), 1.3, 0.8, 0.45, rot_z=0)
    for (cx, cy) in ((fx + 3.5, 1.0), (fx + 3.5, 11.0), (fx + 3.5, 21.0), (fx + 3.5, 31.0), (fx + 12.0, 6.0), (fx + 12.0, 26.0)): K.chim(B, (cx, cy, Hc + 1.6))
    for yy in (5.0, 11.0, 17.0, 23.0, 29.0): B.box('glow_frost' if False else 'glow_blue', (17.0, yy, Hc + 2.45), (2.2, 2.8, 0.05))
    # the main door: rusticated arch, voussoirs, fanlight glow, double doors on hinges (set_door('main'))
    for k in range(9):
        a = math.radians(180 - k * 22.5); B.box('stone', (fx - 0.12, 5.7 + 1.35 * math.cos(a), 4.4 + 1.35 * math.sin(a)), (0.24, 0.42, 0.55), rot=(math.degrees(a) - 90, 0, 0))
    hv = 14; a = np.linspace(0, math.pi, hv + 1); v = [(0, 0, 0)] + [(0, 1.1 * math.cos(t_), 1.1 * math.sin(t_)) for t_ in a]
    with B.xf((fx - 0.02, 5.7, 4.4)): B.mesh('glow_fan', v, [(0, i + 1, i + 2) for i in range(hv)], smooth=False)
    for s in (-1, 1): B.box('stone', (fx - 0.14, 5.7 + s * 1.3, 2.2), (0.28, 0.4, 4.4))
    door_pair('main', (5.6, 4.6, 0.14), (5.6, 6.8, 0.14), h=4.26, out=(1, 0), mat='cobalt_paint', open_=0.0)
    for k in range(3): B.box('stone', (fx - 0.2 - (2 - k) * 0.36, 5.7, 0.14 + 0.153 * (k + 1) / 2 + 0.0), (0.4 + (2 - k) * 0.36 * 0, 4.2, 0.153 * (k + 1)))
    for k in range(3): B.box('stone_dk', (fx - 0.18 - k * 0.36, 5.7, 0.14 + 0.155 * (3 - k) / 2), (0.36, 4.0 + 0.3 * k, 0.155 * (3 - k)))
    # PRÉFECTURE DE POLICE: gold letters on a cobalt band over the door, a lit lantern each side
    sign(B, 'PRÉFECTURE DE POLICE', 11.2, 1.15, (fx - 0.12, 5.7, 6.15), n=(-1, 0), fg=GOLD, bg=COBALT, emit=0.55, depth=0.14)
    for yy in (3.5, 7.9):
        B.cyl('iron', (fx - 0.3, yy, 3.7), 0.03, 0.6, axis='x', seg=6); B.cyl('iron', (fx - 0.6, yy, 3.95), 0.14, 0.12, r2=0.04, seg=8); B.cyl('glow_lantern', (fx - 0.6, yy, 3.68), 0.12, 0.42, r2=0.15, seg=8, smooth=False)
        B.cyl('iron', (fx - 0.6, yy, 3.42), 0.15, 0.05, seg=8); A['lights'].append(K.point((fx - 0.6, yy, 3.68), watts=45, radius=0.12, name='door_lantern'))
    # flags (tricolour, waving), sentry box, the measuring-room French window outside: shutters open, flower box, pigeons
    for yy, dy in ((3.6, -0.5), (7.8, 0.5)): flag('flag_%d' % int(yy), (fx - 0.1, yy, 7.2), (-0.8, dy, 0.55), B=B)
    with B.xf((fx - 0.75, 2.4, 0.14)):
        for k, m in enumerate(('cobalt_paint', 'cream', 'red', 'cobalt_paint')): B.box(m, (0, -0.42 + k * 0.28, 1.15), (0.9, 0.28, 2.3))
        B.box('dark', (-0.46, 0, 1.0), (0.04, 0.6, 1.8)); B.prism_roof('cobalt_paint', (0, 0, 2.3), 1.1, 1.2, 0.5, rot_z=0)
    for s in (-1, 1): B.box('cobalt_paint', (fx - 0.06, 13.2 + s * 1.62, 2.975), (0.06, 0.78, 3.25))                     # open shutters
    B.box('stone_dk', (fx - 0.3, 13.2, 1.29), (0.6, 2.8, 0.12)); B.box('iron', (fx - 0.58, 13.2, 2.25), (0.04, 2.6, 0.04)); B.box('iron', (fx - 0.58, 13.2, 1.8), (0.03, 2.6, 0.03))
    for k in range(14): B.box('iron', (fx - 0.58, 12.0 + k * 2.4 / 13, 1.8), (0.025, 0.025, 0.9))                              # balconnet guard rail
    B.box('walnut', (fx - 0.42, 13.2, 1.45), (0.22, 2.3, 0.2))
    for k in range(8): B.box('red' if k % 2 == 0 else 'amber_paint', (fx - 0.55, 12.0 + (k + 0.5) * 0.3, 4.85), (1.1, 0.3, 0.05), rot=(0, -18, 0))
    B.box('red', (fx - 1.08, 13.2, 4.66), (0.04, 2.4, 0.22))
    for k in range(10): B.sphere('geranium' if k % 3 else 'leaf', (fx - 0.42, 12.2 + k * 0.22, 1.62), 0.11, seg=8, rings=5)
    pigeons(B, [(fx - 0.58, 14.25, 2.27)])
    M.update({'gend_door_l': (fx - 1.2, 3.9, 0.14, 270, 'gendarme'), 'gend_door_r': (fx - 1.2, 7.6, 0.14, 270, 'gendarme'), 'sentry': (fx - 0.8, 2.4, 0.14, 270, 'gendarme'),
              'steps_low': (4.4, 5.9, 0.14, 0, 'prisoner'), 'steps_top': (fx - 0.15, 5.7, 0.6, 0, 'prisoner'), 'desk_gend': (4.6, 3.2, 0.14, 90, 'gendarme')})
    with B.xf((4.75, 3.1, 0.14)): K.table(B, (0, 0), size=(0.7, 0.5), h=0.8, rot=90, top='baize') if False else None
    K.table(B, (4.7, 2.95), size=(0.8, 0.5), h=0.95, rot=90, top='baize'); K.open_ledger(B, (4.7, 2.95, 0.96), rot=90)
    return A

# ---------------------------------------------------------------- door / window hooks
def door_pair(name, hinge_a, hinge_b, h=2.4, out=(1, 0), mat='cobalt_paint', open_=0.0, max_deg=95, panels=True):
    """two door leaves between hinge_a and hinge_b (world, at the floor) that swing toward the horizontal direction `out`. set_door(name, 0..1)."""
    a = np.array(hinge_a, float); b = np.array(hinge_b, float); span = np.linalg.norm(b[:2] - a[:2]); lw = span / 2 - 0.01; leaves = []
    for (p, q) in ((a, b), (b, a)):
        dvec = (q - p)[:2] / span; base = math.degrees(math.atan2(dvec[1], dvec[0]))
        o = np.array(out, float); cross = dvec[0] * o[1] - dvec[1] * o[0]; sgn = 1 if cross > 0 else -1
        hg = bpy.data.objects.new('%s_hinge%d' % (name, len(leaves)), None); bpy.context.scene.collection.objects.link(hg); hg.location = tuple(p); hg.rotation_euler = (0, 0, math.radians(base))
        L = Batch(len(leaves) + 3); L.box(mat, (lw / 2, 0, h / 2), (lw, 0.07, h))
        if panels:
            for pz in (0.28, 0.62):
                L.box('gold', (lw / 2, -0.04, h * pz), (lw * 0.62, 0.02, h * 0.26)); L.box(mat, (lw / 2, -0.05, h * pz), (lw * 0.54, 0.02, h * 0.22))
                L.box('gold', (lw / 2, 0.04, h * pz), (lw * 0.62, 0.02, h * 0.26)); L.box(mat, (lw / 2, 0.05, h * pz), (lw * 0.54, 0.02, h * 0.22))
        L.sphere('gold', (lw - 0.1, -0.06, h * 0.45), 0.04); L.sphere('gold', (lw - 0.1, 0.06, h * 0.45), 0.04)
        for o_ in L.finalize('%s_leaf%d' % (name, len(leaves)), ink_t=0.008): o_.parent = hg
        leaves.append(dict(hinge=hg, base=base, sgn=sgn, max=max_deg))
    W['doors'][name] = leaves; set_door(name, open_); return leaves
def door_single(name, hinge, other, h=2.3, out=(0, 1), mat='cobalt_paint', open_=0.0, max_deg=100):
    a = np.array(hinge, float); b = np.array(other, float); span = np.linalg.norm(b[:2] - a[:2]); dvec = (b - a)[:2] / span; base = math.degrees(math.atan2(dvec[1], dvec[0]))
    o = np.array(out, float); sgn = 1 if dvec[0] * o[1] - dvec[1] * o[0] > 0 else -1
    hg = bpy.data.objects.new(name + '_hinge0', None); bpy.context.scene.collection.objects.link(hg); hg.location = tuple(a); hg.rotation_euler = (0, 0, math.radians(base))
    L = Batch(9); lw = span - 0.02; L.box(mat, (lw / 2, 0, h / 2), (lw, 0.06, h))
    for pz in (0.28, 0.66):
        for s in (-1, 1): L.box('gold', (lw / 2, s * 0.035, h * pz), (lw * 0.66, 0.015, h * 0.26)); L.box(mat, (lw / 2, s * 0.045, h * pz), (lw * 0.58, 0.015, h * 0.22))
    for s in (-1, 1): L.sphere('gold', (lw - 0.09, s * 0.05, h * 0.45), 0.035)
    for o_ in L.finalize(name + '_leaf0', ink_t=0.008): o_.parent = hg
    W['doors'][name] = [dict(hinge=hg, base=base, sgn=sgn, max=max_deg)]; set_door(name, open_); return hg
def set_door(name, open=1.0, frame=None):
    """swing a named door 0 (shut) .. 1 (open ~95 deg): 'main' (façade, opens into the corridor), 'ident' (SERVICE D'IDENTIFICATION, into the
    measuring room), 'archive' (measuring room -> ARCHIVES double door), 'archives' (corridor end), 'prefet' (CABINET DU PRÉFET, stays shut)."""
    for lf in W['doors'].get(name, []):
        lf['hinge'].rotation_euler = (0, 0, math.radians(lf['base'] + lf['sgn'] * lf['max'] * open))
        if frame is not None: K._key(lf['hinge'], 'rotation_euler', frame)

# ================================================================ 3b. the corridor (x 5.7-12.7, y 4.0-7.4, floor 1.2, ceiling 5.7)
CX0, CX1, CY0, CY1, CH = 5.7, 12.7, 4.0, 7.4, 4.5
def build_corridor(B, A, with_end_wall=True):
    """cobalt walls, red/ochre tiles, 5 steps up from the door, gas brackets every 2.5 m (amber/blue bands), photo-card walls floor to ceiling
    ('PHOTOGRAPHIES — SÛRETÉ', ~2,000 cards: texture + 360 relief cards), a clerk on a rolling ladder, a bench for 3 waiting prisoners,
    a gendarme's lectern, doors SERVICE D'IDENTIFICATION (set_door 'ident', into the measuring room), CABINET DU PRÉFET, ARCHIVES (set_door 'archives')."""
    M = A['marks']; z0 = FZ; zt = FZ + CH; r = random.Random(23)
    B.box('tiles', ((6.9 + CX1 + 0.3) / 2, (CY0 + CY1) / 2, z0 - 0.1), (CX1 + 0.3 - 6.9, CY1 - CY0 + 0.6, 0.2))
    for k in range(5): B.box('stone', (CX0 + 0.12 + k * 0.24 + (1.2 - k * 0.24) / 2 * 0 + 0.12, (CY0 + CY1) / 2, 0.14 + (k + 1) * 0.212 / 2), (0.24 * (5 - k) + 0.0, CY1 - CY0, (k + 1) * 0.212)) if False else None
    for k in range(5):                                                                            # steps: from the door sill (0.6) up to 1.2 inside
        xa = CX0 + k * 0.24; B.box('stone' if k % 2 else 'stone_dk', ((xa + 6.95) / 2, (CY0 + CY1) / 2, (0.6 + (k + 1) * 0.12) / 2), (6.95 - xa, CY1 - CY0, 0.6 + (k + 1) * 0.12))
    B.ceil.box('ceiling', ((CX0 + CX1) / 2, (CY0 + CY1) / 2, zt + 0.1), (CX1 - CX0 + 0.6, CY1 - CY0 + 0.6, 0.2))
    for xx in np.arange(6.6, CX1, 1.5): B.ceil.box('beam', (xx, (CY0 + CY1) / 2, zt - 0.1), (0.2, CY1 - CY0, 0.2))
    K.wall_box(B, 'cobalt', 'y', CY0, CX0, CX1, 0.0, zt, [(9.4, 10.6, z0, z0 + 2.5)], out=-1, t=0.3)
    K.wall_box(B, 'cobalt', 'y', CY1, CX0, CX1, 0.0, zt, [(9.8, 10.8, z0, z0 + 2.4)], out=+1, t=0.1)
    if with_end_wall: K.wall_box(B, 'cobalt', 'x', CX1, CY0 - 0.3, CY1 + 0.1, 0.0, zt, [(4.8, 6.6, z0, z0 + 2.7)], out=+1, t=0.3)
    # dado, photo walls with relief cards, cornice + frieze
    for (yy, s, gaps) in ((CY0 + 0.03, 1, [(9.3, 10.7)]), (CY1 - 0.03, -1, [(9.7, 10.9)])):
        xs = [6.95] + [v for g in gaps for v in g] + [CX1 - 0.05]
        for i in range(0, len(xs), 2):
            a, b = xs[i], xs[i + 1]
            B.box('wain', ((a + b) / 2, yy, z0 + 0.45), (b - a, 0.05, 0.9)); B.box('gold', ((a + b) / 2, yy + s * 0.03, z0 + 0.92), (b - a, 0.06, 0.05))
            B.box('photowall', ((a + b) / 2, yy, z0 + 0.95 + 1.6), (b - a, 0.03, 3.2))
            for k in range(int((b - a) * 26)):
                x = r.uniform(a + 0.08, b - 0.08); z = r.uniform(z0 + 1.0, z0 + 4.05); t = r.uniform(0.9, 1.1)
                B.box(r.choice(['cream', 'amber_paint', 'cardedge']), (x, yy + s * 0.03, z), (0.09, 0.012, 0.13), rot=(0, r.uniform(-12, 12), 0), tint=t)
        B.box('frieze', ((CX0 + CX1) / 2, yy, zt - 0.35), (CX1 - CX0, 0.04, 0.3)); B.box('gold', ((CX0 + CX1) / 2, yy, zt - 0.18), (CX1 - CX0, 0.07, 0.05))
    sign(B, 'PHOTOGRAPHIES — SÛRETÉ', 3.6, 0.36, (8.3, CY0 + 0.06, zt - 0.62), n=(0, 1), fg=GOLD, bg=KEPI, emit=0.4)
    sign(B, 'IDENTIFICATION', 2.9, 0.6, (10.3, CY1 - 0.06, z0 + 3.1), n=(0, -1), fg=GOLD, bg=COBALT, emit=0.45, maxh=0.66)     # corridor side: short form (cap 0.37 m)
    sign(B, 'CABINET DU PRÉFET', 2.0, 0.32, (10.0, CY0 + 0.06, z0 + 2.8), n=(0, 1), fg=GOLD, bg=KEPI, emit=0.4)
    sign(B, 'ARCHIVES', 1.9, 0.46, (CX1 - 0.06, 5.7, z0 + 3.05), n=(-1, 0), fg=GOLD, bg=COBALT, emit=0.45)
    for (x, s) in ((9.25, 1), (10.75, 1)): B.box('walnut', (x, CY0 + 0.08, z0 + 1.25), (0.14, 0.16, 2.5))
    B.box('walnut', (10.0, CY0 + 0.08, z0 + 2.55), (1.5, 0.16, 0.14)); door_single('prefet', (9.42, CY0 - 0.05, z0), (10.58, CY0 - 0.05, z0), h=2.45, out=(0, 1), mat='oxblood', open_=0.0)
    for x in (9.72, 10.88): B.box('walnut', (x, CY1 - 0.06, z0 + 1.2), (0.12, 0.14, 2.4))
    B.box('walnut', (10.3, CY1 - 0.06, z0 + 2.46), (1.3, 0.14, 0.12))
    door_single('ident', (9.82, CY1 + 0.02, z0), (10.78, CY1 + 0.02, z0), h=2.36, out=(0, 1), mat='cobalt_paint', open_=0.0)
    door_pair('archives', (CX1 + 0.15, 4.82, z0), (CX1 + 0.15, 6.58, z0), h=2.66, out=(1, 0), mat='cobalt_paint', open_=0.0)
    # transom over the main door: blue street light; the gas brackets every 2.5 m (both walls, staggered)
    B.box('glow_blue', (CX0 + 0.02, 5.7, 4.9), (0.02, 2.2, 0.7))
    for x in (7.2, 9.0, 11.7): K.gas_bracket(B, (x, CY0 + 0.02, z0 + 2.75), rot_z=90, watts=26)
    for x in (7.9, 11.6): K.gas_bracket(B, (x, CY1 - 0.02, z0 + 2.75), rot_z=-90, watts=26)
    with lift(B):
        K.bench(B, (11.5, CY0 + 0.32), length=1.9, rot=0, h=0.46); K.umbrella_stand(B, (6.95 + 0.3, CY0 + 0.3, 0)); K.ledger_stack(B, (12.4, CY0 + 0.35, 0), n=7, rot=10)
        K.crate(B, (7.4, CY1 - 0.35, 0), size=(0.5, 0.4, 0.35), rot=8); K.ledger_stack(B, (7.4, CY1 - 0.35, 0.35), n=5, rot=-12); K.wastebin(B, (12.35, CY1 - 0.3, 0))
        with B.xf((11.95, 6.75, 0), (0, 0, 200)):                                                 # gendarme's lectern with a ledger
            B.box('oak', (0, 0, 0.55), (0.12, 0.12, 1.1)); B.box('oak', (0, 0, 0.03), (0.5, 0.4, 0.06)); B.box('oak', (0, 0, 1.15), (0.55, 0.42, 0.06), rot=(14, 0, 0)); K.open_ledger(B, (0, 0, 1.19), rot=0)
    K.rolling_ladder(B, (8.6, 6.6, z0), (8.6, CY1 - 0.08, z0 + 3.9), width=0.46, rungs=13)
    B.box('runner', (9.8, 5.7, z0 + 0.008), (5.6, 1.1, 0.016))                                          # foreground layer: runner, photo-box piles
    for k in range(4): B.box('box_ochre' if k % 2 else 'cream', (7.85, 4.45, z0 + 0.12 + k * 0.22), (0.46, 0.32, 0.22), rot=(0, 0, 8 * k))
    for k in range(2): B.box('box_ochre', (12.35, 5.0 + 0.0, z0 + 0.12 + k * 0.22), (0.4, 0.3, 0.22), rot=(0, 0, -10 * k))
    for k in range(3): B.box('cream', (8.9 + 0.06 * k, 6.95, z0 + 0.04 + 0.05 * k), (0.32, 0.24, 0.05), rot=(0, 0, 20 * k))        # dropped photo cards
    M.update({'thief_door': (4.4, 5.6, 0.14, 0, 'prisoner'), 'thief_photo': (8.3, 6.5, z0, 90, 'prisoner'), 'thief_id': (10.0, 6.2, z0, 0, 'prisoner'),
              'gend_corr': (7.6, 4.7, z0, 0, 'gendarme'), 'gend_ledger': (11.75, 6.45, z0, 200, 'gendarme'), 'clerk_ladder': (8.6, 6.95, z0 + 1.45, 90, 'clerk'),
              'pris_c0': (11.0, CY0 + 0.45, z0, 90, 'seated'), 'pris_c1': (11.55, CY0 + 0.45, z0, 90, 'seated'), 'pris_c2': (12.1, CY0 + 0.45, z0, 90, 'seated')})
    A['lights'].append(K.area((9.3, 5.7, zt - 0.3), (9.3, 5.7, z0), (6.0, 2.6), P().get('fill_w', 60), color=P().get('fill_col', (0.5, 0.65, 1.0)), name='corr_fill', long_axis=(1, 0, 0)))
    return A

# ================================================================ 3c. the measuring room "SERVICE D'IDENTIFICATION" (v1 room, repainted + upgraded)
def tex_chart11(name='chart11', W_=600, H_=760):
    """the '11 MESURES' wall chart: title + 11 drawn pictograms (head length / width, cheek, ear, middle + little finger, foot, forearm, height,
    arm span, trunk) with big numerals; readable at 3 m."""
    p = _tp(name)
    if os.path.exists(p): return p
    S = 2; im = Image.new('RGB', (W_ * S, H_ * S), _rgb('#f6dfa0')); d = ImageDraw.Draw(im); ink = _rgb('#1a2a8a'); red = _rgb(KEPI)
    d.rectangle([0, 0, W_ * S - 1, H_ * S - 1], outline=_rgb('#7a2a10'), width=18); d.rectangle([24, 24, W_ * S - 25, 170], fill=_rgb(COBALT))
    f = _fit_text('11 MESURES', 'serif', W_ * S - 90, 150, 0.8); bb = f.getbbox('11 MESURES'); d.text(((W_ * S - (bb[2] - bb[0])) / 2 - bb[0], 97 - (bb[3] + bb[1]) / 2), '11 MESURES', font=f, fill=_rgb(GOLD))
    fn = font('serif', 54); cw, ch = (W_ * S - 60) / 3, (H_ * S - 230) / 4
    for k in range(11):
        cx = 30 + (k % 3) * cw + cw / 2; cy = 210 + (k // 3) * ch + ch * 0.45; s = min(cw, ch) * 0.3; w = 9
        d.rounded_rectangle([cx - cw / 2 + 10, cy - ch * 0.45 + 6, cx + cw / 2 - 10, cy + ch * 0.55 - 6], radius=18, outline=ink, width=6)
        if k in (0, 1, 2):     # head length / head width / cheek
            d.ellipse([cx - s * 0.8, cy - s, cx + s * 0.8, cy + s], outline=ink, width=w); y_ = cy if k != 2 else cy + s * 0.3
            d.line([(cx - s * 1.1, y_ if k else cy - s), (cx + s * 1.1, y_ if k else cy - s)] if k else [(cx, cy - s * 1.15), (cx, cy + s * 1.15)], fill=red, width=w)
        elif k == 3:           # ear
            d.arc([cx - s * 0.6, cy - s, cx + s * 0.6, cy + s], 270, 120, fill=ink, width=w + 2); d.arc([cx - s * 0.3, cy - s * 0.5, cx + s * 0.3, cy + s * 0.5], 280, 100, fill=ink, width=w); d.line([(cx, cy - s * 1.1), (cx, cy + s * 1.1)], fill=red, width=w)
        elif k in (4, 5):      # middle / little finger
            fw = s * (0.32 if k == 4 else 0.24); fh = s * (1.5 if k == 4 else 1.0); d.rounded_rectangle([cx - fw, cy - fh, cx + fw, cy + s * 0.8], radius=int(fw), outline=ink, width=w); d.line([(cx + fw * 2, cy - fh), (cx + fw * 2, cy + s * 0.8)], fill=red, width=w)
        elif k == 6:           # foot
            d.ellipse([cx - s * 1.2, cy - s * 0.35, cx + s * 1.2, cy + s * 0.45], outline=ink, width=w); d.line([(cx - s * 1.2, cy + s * 0.75), (cx + s * 1.2, cy + s * 0.75)], fill=red, width=w)
        elif k == 7:           # forearm
            d.line([(cx - s * 1.1, cy + s * 0.2), (cx + s * 0.8, cy + s * 0.2)], fill=ink, width=int(s * 0.4)); d.ellipse([cx + s * 0.6, cy - s * 0.15, cx + s * 1.2, cy + s * 0.55], outline=ink, width=w); d.line([(cx - s * 1.1, cy - s * 0.4), (cx + s * 1.2, cy - s * 0.4)], fill=red, width=w)
        elif k == 8:           # height
            d.ellipse([cx - s * 0.2, cy - s * 1.2, cx + s * 0.2, cy - s * 0.8], outline=ink, width=w); d.line([(cx, cy - s * 0.8), (cx, cy + s * 0.5), (cx - s * 0.3, cy + s * 1.1)], fill=ink, width=w); d.line([(cx, cy + s * 0.5), (cx + s * 0.3, cy + s * 1.1)], fill=ink, width=w); d.line([(cx + s * 0.8, cy - s * 1.2), (cx + s * 0.8, cy + s * 1.1)], fill=red, width=w)
        elif k == 9:           # arm span
            d.ellipse([cx - s * 0.16, cy - s * 0.7, cx + s * 0.16, cy - s * 0.38], outline=ink, width=w); d.line([(cx - s * 1.25, cy - s * 0.2), (cx + s * 1.25, cy - s * 0.2)], fill=ink, width=w); d.line([(cx, cy - s * 0.38), (cx, cy + s * 0.9)], fill=ink, width=w); d.line([(cx - s * 1.25, cy + s * 1.05), (cx + s * 1.25, cy + s * 1.05)], fill=red, width=w)
        else:                  # trunk (seated height)
            d.ellipse([cx - s * 0.2, cy - s * 1.1, cx + s * 0.2, cy - s * 0.7], outline=ink, width=w); d.line([(cx, cy - s * 0.7), (cx, cy + s * 0.3), (cx + s * 0.8, cy + s * 0.3), (cx + s * 0.8, cy + s * 1.0)], fill=ink, width=w); d.line([(cx - s * 0.7, cy - s * 1.1), (cx - s * 0.7, cy + s * 0.3)], fill=red, width=w)
        d.text((cx - cw / 2 + 22, cy - ch * 0.45 + 12), str(k + 1), font=fn, fill=red)
    im.resize((W_, H_), Image.LANCZOS).save(p); return p
def tex_page(text, sub=None, name=None, W_=400, H_=520, bg='#f6e3a8', fg=KEPI):
    p = _tp(name or ('page_' + ''.join(c for c in text if c.isalnum())))
    if os.path.exists(p): return p
    im = Image.new('RGB', (W_ * 2, H_ * 2), _rgb(bg)); d = ImageDraw.Draw(im); d.rectangle([0, 0, W_ * 2 - 1, 120], fill=_rgb(KEPI)); d.rectangle([0, 0, W_ * 2 - 1, H_ * 2 - 1], outline=_rgb('#7a2a10'), width=12)
    for k in range(2): d.ellipse([W_ * (0.6 + 0.8 * k) - 20, 40, W_ * (0.6 + 0.8 * k) + 20, 80], fill=_rgb('#f6e3a8'))
    lines = [l for l in text.split('\n')]; y = 190
    for i, l in enumerate(lines):
        f = _fit_text(l, 'serif', W_ * 2 - 120, (H_ * 2 - 260) / len(lines), 0.8, 0.9); bb = f.getbbox(l)
        d.text(((W_ * 2 - (bb[2] - bb[0]) * 0.9) / 2 - bb[0], y - bb[1]), l, font=f, fill=_rgb(fg if i == 0 else COBALT)); y += (H_ * 2 - 260) / len(lines)
    im.resize((W_, H_), Image.LANCZOS).save(p); return p
def casement_pair(name, hinge_a, hinge_b, h=1.45, out=(1, 0), mat='cobalt_paint', open_=1.0, max_deg=105):
    """French casement (glazed leaves: frame bars + glazing bars, no pane) on hinges; set_window(open)."""
    a = np.array(hinge_a, float); b = np.array(hinge_b, float); span = np.linalg.norm(b[:2] - a[:2]); lw = span / 2 - 0.01; leaves = []
    for (p, q) in ((a, b), (b, a)):
        dvec = (q - p)[:2] / span; base = math.degrees(math.atan2(dvec[1], dvec[0])); o = np.array(out, float); sgn = 1 if dvec[0] * o[1] - dvec[1] * o[0] > 0 else -1
        hg = bpy.data.objects.new('%s_hinge%d' % (name, len(leaves)), None); bpy.context.scene.collection.objects.link(hg); hg.location = tuple(p); hg.rotation_euler = (0, 0, math.radians(base))
        L = Batch(len(leaves) + 11)
        for (cx, cz, sx, sz) in ((0.03, h / 2, 0.06, h), (lw - 0.03, h / 2, 0.06, h), (lw / 2, 0.03, lw, 0.06), (lw / 2, h - 0.03, lw, 0.06), (lw / 2, h * 0.36, lw, 0.035), (lw / 2, h * 0.68, lw, 0.035), (lw / 2, h / 2, 0.035, h)):
            L.box(mat, (cx, 0, cz), (sx, 0.05, sz))
        L.sphere('gold', (lw - 0.07, 0.05, h * 0.5), 0.03)
        for o_ in L.finalize('%s_leaf%d' % (name, len(leaves)), ink_t=0.007): o_.parent = hg
        leaves.append(dict(hinge=hg, base=base, sgn=sgn, max=max_deg))
    W['doors'][name] = leaves; set_door(name, open_); return leaves
def set_window(open=1.0, frame=None):
    """the measuring room's French window (BIGZOOM 1 enters through it): 0 shut .. 1 wide open (default, 105 deg into the room)."""
    set_door('window', open, frame)
def set_calendar(page=1.0, frame=None):
    """the wall calendar: 0 shows 'MARS 1882', 1 the top page is flipped up and the big page reads '3 MOIS' (in between: the flip)."""
    a = W.get('calendar')
    if a is None: return
    a.rotation_euler = (math.radians(-175 * max(0.0, min(1.0, page))), 0, 0)
    if frame is not None: K._key(a, 'rotation_euler', frame)
MPATH = {}
def build_measure2(B, A):
    """PLAN §3c, in the v1 room frame (x -3.2..3.2, y -4.2..4.2, h 4.2; world = local + MO): ochre upper walls, cobalt dado and ceiling with honey
    beams, oak floor, cobalt rug with a red border (palette); the open French casement (no bars), the SERVICE D'IDENTIFICATION door in the front
    wall (corridor), the ARCHIVES double door in the right wall with 'ARCHIVES →' over it, the '11 MESURES' chart, the '3 MOIS' calendar."""
    MX0, MX1, MY0, MY1, MH = K.MX0, K.MX1, K.MY0, K.MY1, K.MH; M = A['marks']
    win = ('L', 0.0, 2.4, 0.15, 3.4); d_arch = ('R', -3.2, -1.6, 0, 2.6); d_id = ('F', 0.6, 1.6, 0, 2.4)
    K.room_shell(B, MX0, MX1, MY0, MY1, MH, wain=1.3, windows=[win], doors=[d_arch, d_id], ceil='ceil_navy')
    # the French window: frame, sill, open casement leaves (into the room), a pigeon walking in on the sill
    B.box('cobalt_paint', (MX0 + 0.06, 1.2, 0.1), (0.24, 2.64, 0.1)); B.box('cobalt_paint', (MX0 + 0.06, 1.2, 3.45), (0.2, 2.6, 0.1))
    for yy in (-0.05, 2.45): B.box('cobalt_paint', (MX0 + 0.06, yy, 1.775), (0.2, 0.1, 3.25))
    casement_pair('window', (MX0 + 0.05, 0.0, 0.15), (MX0 + 0.05, 2.4, 0.15), h=3.25, out=(1, 0), open_=1.0)
    pigeons(B, [(MX0 + 0.12, 2.05, 0.15)])
    for (x0, x1, y_) in ((0.6, 1.6, MY0), ):
        for x in (x0 - 0.07, x1 + 0.07): B.box('walnut', (x, y_ + 0.08, 1.2), (0.14, 0.16, 2.4))
        B.box('walnut', ((x0 + x1) / 2, y_ + 0.08, 2.47), (x1 - x0 + 0.28, 0.16, 0.14))
    for y in (-3.27, -1.53): B.box('walnut', (MX1 - 0.08, y, 1.3), (0.16, 0.14, 2.6))
    B.box('walnut', (MX1 - 0.08, -2.4, 2.67), (0.16, 1.88, 0.14))
    door_pair('archive', (MX1 + 0.05, -3.18, 0), (MX1 + 0.05, -1.62, 0), h=2.56, out=(1, 0), open_=0.0)
    sign(B, "SERVICE D'IDENTIFICATION", 3.9, 0.5, (1.1, MY0 + 0.06, 3.15), n=(0, 1), fg=GOLD, bg=COBALT, emit=0.4, maxh=0.66)
    sign(B, 'ARCHIVES →', 1.7, 0.4, (MX1 - 0.06, -2.4, 3.05), n=(-1, 0), fg=GOLD, bg=KEPI, emit=0.45)
    B.box('runner', (0.75, 1.5, 0.006), (1.4, 3.6, 0.012))
    K.measuring_chair(B, (0.7, 2.4), rot=180, head_z=1.34); K.toise(B, (1.7, MY1 - 0.03), rot=180, slider=1.66); K.arm_span_scale(B, (-1.55, MY1 - 0.03), rot=180, length=2.0, z=1.42)
    K.foot_board(B, (2.2, 3.3), rot=0)
    with B.xf((MX0 + 0.05, 3.35, 2.15), (0, 0, 90)):
        B.box('walnut', (0, 0.03, 0), (1.3, 0.05, 0.6)); B.box('red', (0, 0.058, 0), (1.18, 0.012, 0.48))
        K.sliding_calipers(B, (0, 0.075, -0.1), rot=0, length=0.95, open_=0.34, tilt=(90, 0, 0), scale=1.0); K.spreading_calipers(B, (-0.2, 0.08, 0.2), rot=0, span=0.3, leg=0.36, tilt=(90, 0, 0), scale=0.9)
    K.table(B, (1.9, 1.55), size=(0.85, 0.55), h=0.8, rot=8, top='baize')
    with B.xf((1.9, 1.55, 0), (0, 0, 8)): K.sliding_calipers(B, (-0.02, -0.05, 0.808), rot=10, length=0.5, open_=0.2); K.spreading_calipers(B, (0.22, 0.12, 0.808), rot=-35, span=0.26, leg=0.3); K.inkpot(B, (-0.3, 0.15, 0.808), rot=25)
    K.camera_tripod(B, (0.95, 0.55), rot=0)
    K.table(B, (2.7, 0.55), size=(1.5, 0.72), h=0.84, rot=90)
    with B.xf((2.7, 0.55, 0), (0, 0, 90)):
        K.ledger_stack(B, (-0.5, 0.1, 0.848), n=4, rot=15); K.open_ledger(B, (0.1, -0.05, 0.848), rot=-6); K.inkpot(B, (0.55, 0.2, 0.848), rot=20); K.banker_lamp(B, (-0.1, 0.22, 0.848), rot=-20, watts=40)
    K.stool(B, (1.95, 0.55), h=0.64, rot=10); K.bench(B, (-2.88, 1.2), length=2.6, rot=-90)
    K.coat_rack(B, (2.9, -0.75), rot=20, kepis=3); K.umbrella_stand(B, (2.9, -3.75, 0))
    K.wall_clock(B, (0.2, MY1 - 0.04, 3.05), rot=180, r=0.28); K.pendulum_case(B, (0.2, MY1 - 0.04, 2.7), rot=180, h=1.1, w=0.22)
    K.ledger_shelf(B, (1.3, MY1 - 0.03, 2.75), length=1.6, rot=180, n=1)
    K.stove(B, (2.75, 3.4), rot=-90, pipe_to=MH - 0.1); A['smoke_src_local'] = (2.75, 3.4, 1.15)
    for nm, c, sz, rt, ky in (('wc0', (MX1 - 0.04, 1.75, 2.15), (0.5, 0.68), -90, 'card_notice'), ('wc2', (0.45, MY1 - 0.04, 1.0), (0.5, 0.36), 180, 'card_portrait'), ('wc3', (-0.3, MY1 - 0.04, 1.05), (0.4, 0.5), 180, 'card_portrait2')):
        B.box('walnut', c, ((sz[0] + 0.08, 0.04, sz[1] + 0.08) if abs(rt) == 180 else (0.04, sz[0] + 0.08, sz[1] + 0.08))); K.STATE.setdefault('wall_cards', []).append((nm, c, sz, rt, ky))
    # the '11 MESURES' chart beside the clock (back wall) and the calendar (right wall)
    B.box('walnut', (-1.45, MY1 - 0.03, 2.72), (1.28, 0.04, 1.58)); plane('chart11', (-1.45, MY1 - 0.06, 2.72), (1.2, 1.5), rotz=face_rot((0, -1)), mat=_sign_mat('chart11', tex_chart11(), 0.3))
    B.box('walnut', (MX1 - 0.03, 2.75, 2.3), (0.04, 0.58, 0.78)); cr = (MX1 - 0.06, 2.75, 2.66)
    plane('cal_p1', (MX1 - 0.055, 2.75, 2.3), (0.5, 0.66), rotz=face_rot((-1, 0)), mat=_sign_mat('cal_p1', tex_page('3 MOIS', name='page_3mois'), 0.3))
    hg = bpy.data.objects.new('cal_hinge', None); bpy.context.scene.collection.objects.link(hg); hg.location = cr; hg.rotation_euler = (0, 0, math.radians(face_rot((-1, 0)))); W['calendar_parent'] = hg
    pv = bpy.data.objects.new('cal_flip', None); bpy.context.scene.collection.objects.link(pv); pv.parent = hg; W['calendar'] = pv
    pg = plane('cal_p0', (0, -0.012, -0.34), (0.5, 0.66), mat=_sign_mat('cal_p0', tex_page('MARS\n1882', name='page_mars'), 0.3)); pg.parent = pv
    # gas: gasoliers, brackets, pipes; clutter
    K.gasolier(B, (-0.35, 1.0, MH - 0.05), drop=1.45, watts=260); K.gasolier(B, (1.0, -1.4, MH - 0.05), drop=1.45, watts=200)
    K.gas_bracket(B, (MX0 + 0.02, 3.35, 2.75), rot_z=0, watts=14); K.gas_bracket(B, (MX1 - 0.02, 0.9, 2.8), rot_z=180, watts=14); K.gas_bracket(B, (-2.6, MY1 - 0.02, 2.6), rot_z=-90, watts=14)
    K.gas_pipe(B, (-0.35, 1.0, MH - 0.08), (-0.35, MY1 - 0.1, MH - 0.08)); K.gas_pipe(B, (1.0, -1.4, MH - 0.08), (MX1 - 0.1, -1.4, MH - 0.08))
    K.crate(B, (-2.5, -3.3, 0), size=(0.6, 0.45, 0.4), rot=12); K.crate(B, (-2.5, -3.3, 0.4), size=(0.5, 0.4, 0.3), rot=-8); K.crate(B, (-1.85, -3.55, 0), size=(0.45, 0.4, 0.35), rot=20)
    K.bucket(B, (2.55, -3.45, 0)); K.wastebin(B, (-0.4, 3.5, 0)); K.stool(B, (-0.9, -0.6), h=0.55, rot=30); K.ledger_stack(B, (-0.9, -0.6, 0.58), n=4, rot=10)
    # foreground layer by the window and the doors (SET gate B4): ledgers, a kepi on the floor, spittoon, calipers case, a dropped card, rug, crate
    K.ledger_stack(B, (-0.6, -0.35, 0.0), n=6, rot=14); K.kepi(B, (-0.95, 0.35, 0.0), rot=35); B.cyl('brass', (-0.3, 0.95, 0.09), 0.13, 0.18, r2=0.16, seg=14); B.cyl('dark', (-0.3, 0.95, 0.185), 0.1, 0.01, seg=14)
    with B.xf((-1.05, 1.05, 0.0), (0, 0, 25)):
        B.box('walnut', (0, 0, 0.05), (0.55, 0.3, 0.1)); B.box('red', (0, 0, 0.101), (0.5, 0.25, 0.004)); B.box('walnut', (0, 0.17, 0.25), (0.55, 0.03, 0.3), rot=(-15, 0, 0)); K.sliding_calipers(B, (0, 0, 0.11), rot=5, length=0.42, open_=0.1)
    B.box('cream', (-1.35, 0.55, 0.004), (0.15, 0.1, 0.004), rot=(0, 0, 30)); B.box('cream', (-0.75, 1.55, 0.004), (0.15, 0.1, 0.004), rot=(0, 0, -20))
    B.box('runner', (0.6, -2.45, 0.006), (1.7, 1.1, 0.012)); K.crate(B, (2.0, -2.6, 0), size=(0.5, 0.4, 0.35), rot=-12); K.ledger_stack(B, (2.0, -2.6, 0.35), n=4, rot=8); K.umbrella_stand(B, (-0.4, -3.3, 0))
    A['lights'].append(K.point((-2.0, 1.2, 2.7), color=(1.0, 0.72, 0.4), watts=P().get('win_lamp', 120), radius=0.15, name='win_glow', flicker=False))
    Pp = P(); d = np.array(Pp['sun_dir']); d = d / np.linalg.norm(d)
    cs = [(MX0 + 0.02, 0.0, 3.4), (MX0 + 0.02, 2.4, 3.4), (MX0 + 0.02, 2.4, 0.15), (MX0 + 0.02, 0.0, 0.15)]; K.light_shaft(B, cs, d)
    A['dust_local'] = dict(p0=np.array([MX0 + 0.1, 1.2, 2.2]), d=d, L=4.2, w=1.5, n=42)
    A['lights'] += [K.area((MX0 + 0.12, 1.2, 1.9), (0.8, 2.2, 0.4), (2.2, 3.0), Pp['win_w'], name='win_key'),
                    K.area((MX0 + 0.3, 1.2, 3.3), (2.0, 1.0, 0.0), (2.4, 1.4), Pp.get('fill_w', 110), color=Pp.get('fill_col', (0.55, 0.7, 1.0)), name='sky_fill')]
    A['pendulum_local'] = dict(pivot=(0.2, MY1 - 0.04 - 0.14, 2.62), L=0.85)
    A['clock_local'] = (0.2, MY1 - 0.04, 3.05)
    L = {'chair': (0.7, 2.3, 0.5, 180, 'seated'), 'clerk': (1.45, 1.95, 0.0, 200, 'clerk'), 'clerk_toise': (1.7, 3.55, 0.0, 180, 'clerk'), 'prisoner_toise': (1.7, 3.1, 0.0, 180, 'prisoner'),
         'queue0': (-1.5, -1.0, 0.0, 90, 'prisoner'), 'queue1': (-0.2, -0.6, 0.0, 120, 'prisoner'), 'door_id': (1.1, -3.6, 0.0, 0, 'gendarme'), 'door_arch': (2.6, -2.4, 0.0, 270, 'clerk'),
         'table': (2.0, 0.55, 0.0, 180, 'clerk'), 'armspan': (-1.55, 3.45, 0.0, 180, 'prisoner'), 'tripod': (0.2, 0.35, 0.0, 20, 'clerk'), 'bert_bench': (-1.65, 1.5, 0.0, 270, 'clerk'),
         'insp_mid': (0.3, -1.6, 0.0, 30, 'inspector'), 'gend_rack': (2.3, -1.2, 0.0, 200, 'gendarme'), 'gend_back': (-0.7, 2.9, 0.0, 180, 'gendarme'), 'prefect_in': (1.1, -2.7, 0.0, 0, 'prefect'),
         'foot': (2.2, 3.0, 0.0, 180, 'prisoner'), 'finger': (1.9, 1.9, 0.0, 180, 'prisoner'), 'desk': (2.25, 0.2, 0.0, 90, 'clerk')}
    for i, y in enumerate((0.15, 0.85, 1.55, 2.25)): L['bench%d' % i] = (-2.4, y, 0.0, 90, 'seated')
    A['marks_local'] = L
    return A

# ================================================================ 3d. the ARCHIVES hall (x 13-21, y 2-34, floor 1.2, walls to 8.6, segmental cobalt vault to 10.2)
AX0, AX1, AY0, AY1 = 13.0, 21.0, 2.0, 34.0
WT = FZ + 7.4; VR = 5.8; VCZ = WT + 1.6 - VR          # vault: rise 1.6, radius 5.8, centre z
SKY = ((3.5, 6.5), (9.5, 12.5), (15.5, 18.5), (21.5, 24.5), (27.5, 30.5))
SECT = {'PETIT': (2.0, 12.7, (0.30, 0.20)), 'MOYEN': (12.7, 23.3, (0.45, 0.25)), 'GRAND': (23.3, 34.0, (0.90, 0.40))}
HERO = dict(y=26.25, z=FZ + 1.2, face=13.55)
def bank(B, side, y0, y1, z0, height, cell, depth=0.55, reserve=(), seed=1, labels=True):
    """a run of card cabinets against the west ('W', face x 13+depth, facing +x) or east ('E', face 21-depth) wall, y0..y1, from z0, `height` tall,
    drawer cell (w, h). Plinth, carcass, cornice, drawers (honey front, cream label, brass pull). reserve = [(col, row)] left empty. returns cell fn."""
    r = random.Random(seed); cw, ch = cell; L = y1 - y0; nc = max(1, int(L / cw)); nr = max(1, int((height - 0.25) / ch)); pad = (L - nc * cw) / 2
    org, rz = ((AX0, y1, z0), -90) if side == 'W' else ((AX1, y0, z0), 90)
    res = set(reserve)
    with B.xf(org, (0, 0, rz)):
        B.box('carcass', (L / 2, depth / 2 - 0.02, height / 2), (L, depth, height), tint=0.9); B.box('carcass', (L / 2, depth / 2 + 0.04, 0.1), (L + 0.04, depth + 0.08, 0.2), tint=0.8)
        B.box('carcass', (L / 2, depth / 2 + 0.06, height + 0.08), (L + 0.06, depth + 0.14, 0.16)); B.box('gold', (L / 2, depth + 0.13, height + 0.04), (L, 0.02, 0.03))
        for cc in range(nc):
            for rr in range(nr):
                x = pad + (cc + 0.5) * cw; z = 0.2 + (rr + 0.5) * ch
                if (cc, rr) in res: B.box('dark', (x, depth + 0.006, z), (cw - 0.012, 0.004, ch - 0.012)); continue
                t = r.uniform(0.84, 1.1); B.box('drawer', (x, depth + 0.018, z), (cw - 0.02, 0.036, ch - 0.02), tint=(t, t * r.uniform(0.94, 1.0), t * r.uniform(0.85, 1.0)))
                if labels: B.box('cream', (x, depth + 0.04, z + ch * 0.18), (min(0.12, cw * 0.4), 0.006, ch * 0.18), tint=r.uniform(0.92, 1.05))
                B.box('brass_nk', (x, depth + 0.045, z - ch * 0.2), (min(0.09, cw * 0.3), 0.016, 0.016))
    def cell_world(cc, rr):
        lx = pad + (cc + 0.5) * cw; lz = z0 + 0.2 + (rr + 0.5) * ch
        return ((AX0 + depth, y1 - lx, lz) if side == 'W' else (AX1 - depth, y0 + lx, lz))
    return dict(cell=cell_world, nc=nc, nr=nr, pad=pad, y0=y0, y1=y1)
def tex_tally(n, name='tally'):
    """chalk board 'RÉCIDIVISTES 1884' + the count n in big chalk numerals + tally strokes (groups of five). frames tally_0000 .. tally_0241."""
    d_ = os.path.join(TEX, 'tally'); os.makedirs(d_, exist_ok=True); p = os.path.join(d_, '%s_%04d.png' % (name, n))
    if os.path.exists(p): return p
    Wt, Ht = 640, 400; im = Image.new('RGB', (Wt, Ht), _rgb('#1c4a58')); d = ImageDraw.Draw(im); ch_ = _rgb('#fff0c0')
    d.rectangle([0, 0, Wt - 1, Ht - 1], outline=_rgb('#8a4a1a'), width=16); f = _fit_text('RÉCIDIVISTES 1884', 'serif', Wt - 60, 80, 0.85, 0.86); bb = f.getbbox('RÉCIDIVISTES 1884')
    d.text(((Wt - (bb[2] - bb[0])) / 2 - bb[0], 24 - bb[1]), 'RÉCIDIVISTES 1884', font=f, fill=_rgb(GOLD)); d.line([(30, 100), (Wt - 30, 100)], fill=ch_, width=4)
    f2 = font('serif', 150); s = str(n); bb = f2.getbbox(s); d.text((40 - bb[0], 250 - (bb[3] + bb[1]) / 2), s, font=f2, fill=ch_)
    for g in range(n // 5 + (1 if n % 5 else 0)):
        k = min(5, n - g * 5); gx = 330 + (g % 10) * 29; gy = 118 + (g // 10) * 54
        for j in range(min(k, 4)): d.line([(gx + j * 5, gy), (gx + j * 5, gy + 40)], fill=ch_, width=3)
        if k == 5: d.line([(gx - 3, gy + 36), (gx + 20, gy + 4)], fill=ch_, width=3)
    im.save(p); return p
def set_tally(n=241, frame=None):
    """the chalk tally board on the east gallery rail rolls 0 -> 241 (image sequence; keyed per frame through the image user's frame offset)."""
    t = W.get('tally')
    if t is None: return
    n = int(max(0, min(241, round(n)))); iu = t.image_user; iu.frame_offset = n - (int(bpy.context.scene.frame_current if frame is None else frame)) + 0
    iu.frame_start = 1; iu.frame_duration = 100000; iu.use_auto_refresh = True          # shown file number = frame + offset = n (the duration must not clamp the frame first)
    if frame is not None: iu.keyframe_insert('frame_offset', frame=frame)
def set_banner_sway(t=None, frame=None, amp=4.0):
    """the PETIT / MOYEN / GRAND banners sway (deg) about their top edge; t seconds (default: from the frame)."""
    t = K._tsec(frame) if t is None else t
    for i, hg in enumerate(W.get('banners', [])):
        hg.rotation_euler = (math.radians(amp * math.sin(2 * math.pi * t / (3.1 + 0.4 * i) + i)), 0, hg.rotation_euler[2])
        if frame is not None: K._key(hg, 'rotation_euler', frame)
def tex_hero_v2():
    """hero card v2 (PLAN §3e): the v1 Dupont card with a big MARTIN in the name panel and the empty-bottle sketch moved to the right panel.
    Stored mirrored left-right, because bertillon.card_plane shows its texture mirrored from the front side."""
    p = os.path.join(TEX, 'card_bertillon_martin_v2.png')
    if os.path.exists(p): return p
    base = Image.open(TX.card('card_bertillon', 'bertillon', 7)).convert('RGB'); d = ImageDraw.Draw(base); PL = (58, 40, 50)
    d.rectangle([22, 22, 330, 108], fill=(246, 236, 208), outline=PL, width=6); f = _fit_text('MARTIN', 'serif', 290, 84, 0.86, 0.9); bb = f.getbbox('MARTIN')
    lay = Image.new('L', (bb[2] - bb[0] + 8, bb[3] - bb[1] + 8), 0); ImageDraw.Draw(lay).text((4 - bb[0], 4 - bb[1]), 'MARTIN', font=f, fill=255); lay = lay.resize((int(lay.size[0] * 0.9), lay.size[1]), Image.LANCZOS)
    base.paste(Image.new('RGB', lay.size, (176, 30, 34)), (int(176 - lay.size[0] / 2), int(65 - lay.size[1] / 2)), lay)
    d.rectangle([346, 22, 746, 108], fill=(228, 200, 168)); TX._bottle(d, 700, 65, 74)
    base.transpose(Image.FLIP_LEFT_RIGHT).save(p); return p
def build_archive(B, A):
    """PLAN §3d: 30 m hall, two storeys of honey card cabinets (PETIT 0.30x0.20 / MOYEN 0.45x0.25 / GRAND 0.90x0.40 drawers), cast-iron gallery
    at 4.2 m with a red rail, spiral stair, 3 rolling ladders, cobalt segmental vault with honey ribs and 5 skylights (shafts + dust), 3 gasoliers,
    hanging section banners, the big ARCHIVES sign, Bertillon's desk under GRAND (banker lamp, candle, card fan), the RÉCIDIVISTES tally board
    (set_tally), trolleys, overflow piles, and the reveal assembly (drawer 'big', 'box', 'box2', hero card) built into the GRAND bank at y 26.25."""
    M = A['marks']; z0 = FZ; Pp = P(); night = Pp.get('gasolier_k', 1.0) < 0.99; r = random.Random(31)
    B.box('tiles', ((AX0 + AX1) / 2, (AY0 + AY1) / 2, z0 - 0.1), (AX1 - AX0 + 0.6, AY1 - AY0 + 0.6, 0.2)); B.box('runner', (17.0, 18.0, z0 + 0.008), (1.6, 31.0, 0.016))
    K.wall_box(B, 'cobalt', 'x', AX0, AY0 - 0.3, AY1 + 0.3, 0.0, WT, [(4.8, 6.6, z0, z0 + 2.7), (8.8, 10.4, z0, z0 + 2.6)], out=-1, t=0.3)
    K.wall_box(B, 'cobalt', 'x', AX1, AY0 - 0.3, AY1 + 0.3, 0.0, WT, [], out=+1, t=0.3)
    for (yy, s) in ((AY0, -1), (AY1, 1)): B.box('cobalt', ((AX0 + AX1) / 2, yy + s * 0.15, (WT + 10.6) / 2), (AX1 - AX0 + 0.6, 0.3, 10.6 + 0.1))
    # vault (B.ceil: cut away for top-down shots) with skylight openings, honey ribs, frosted glazing
    ys = sorted(set([AY0 - 0.3, AY1 + 0.3] + [v for g in SKY for v in g])); n = 16; th = math.asin(4.0 / VR); dth = 2 * th / n
    for ya, yb in zip(ys[:-1], ys[1:]):
        sky = any(a <= (ya + yb) / 2 <= b for a, b in SKY)
        for i in range(n):
            t0 = -th + i * dth; tc = t0 + dth / 2
            if sky and abs(tc) < math.asin(1.25 / VR): continue
            B.ceil.box('ceiling', (17.0 + (VR + 0.15) * math.sin(tc), (ya + yb) / 2, VCZ + (VR + 0.15) * math.cos(tc)), (VR * dth + 0.03, yb - ya, 0.3), rot=(0, math.degrees(tc), 0))
    for yy in np.arange(AY0 + 0.1, AY1, 3.2):
        for i in range(n):
            tc = -th + (i + 0.5) * dth; B.ceil.box('beam', (17.0 + (VR - 0.08) * math.sin(tc), yy, VCZ + (VR - 0.08) * math.cos(tc)), (VR * dth + 0.03, 0.26, 0.2), rot=(0, math.degrees(tc), 0))
    for (a, b) in SKY:
        B.ceil.box('glow_frost', (17.0, (a + b) / 2, VCZ + VR + 0.45), (2.6, b - a, 0.03))
        for k in range(4): B.ceil.box('iron', (16.0 + k * 0.66, (a + b) / 2, VCZ + VR + 0.4), (0.05, b - a, 0.06))
    for x in (AX0 + 0.1, AX1 - 0.1): B.box('frieze', (x, (AY0 + AY1) / 2, WT - 0.2), (0.05, AY1 - AY0, 0.4))
    # cabinets: lower storey (4.0 m) and upper storey above the gallery (2.9 m), per section; the hero drawer reserved in GRAND west
    hero_cc = int((AY1 - 0.1 - HERO['y']) / 0.9); A['banks'] = {}
    for name, (ya, yb, cell) in SECT.items():
        segW = [(ya + 0.1, yb)] if name != 'PETIT' else [(2.1, 4.6), (6.8, 8.6), (10.6, yb)]
        for k, (a, b) in enumerate(segW):
            res = [(hero_cc, 2)] if name == 'GRAND' else []
            A['banks'][(name, 'W', k)] = bank(B, 'W', a, b - 0.05 if name == 'GRAND' and False else b, z0, 4.0, cell, reserve=res, seed=3 + k + len(name))
        A['banks'][(name, 'E', 0)] = bank(B, 'E', ya + 0.05, yb - 0.05 if name != 'GRAND' else yb - 0.1, z0, 4.0, cell, seed=13 + len(name))
        for side in 'WE': bank(B, side, ya + 0.05, yb - 0.05 if name != 'GRAND' else yb - 0.1, z0 + 4.3, 2.9, cell, seed=23 + len(name), labels=(name != 'PETIT'))
    # gallery decks at 4.2 m with a red rail, brackets; spiral stair (NE corner); rolling ladders on rails
    for (xd, s) in ((AX0 + 0.55 + 0.55, 1), (AX1 - 0.55 - 0.55, -1)):
        B.box('oak', (xd, (AY0 + AY1) / 2, z0 + 4.14), (1.1, AY1 - AY0 - 0.2, 0.12)); B.box('cobalt_paint', (xd + s * 0.55, (AY0 + AY1) / 2, z0 + 4.0), (0.06, AY1 - AY0 - 0.2, 0.3))
        B.box('gold', (xd + s * 0.58, (AY0 + AY1) / 2, z0 + 4.08), (0.02, AY1 - AY0 - 0.2, 0.05))
        xr = xd + s * 0.52; B.box('red', (xr, (AY0 + AY1) / 2, z0 + 5.2), (0.09, AY1 - AY0 - 0.2, 0.08)); B.box('iron', (xr, (AY0 + AY1) / 2, z0 + 4.65), (0.04, AY1 - AY0 - 0.2, 0.04))
        for yy in np.arange(AY0 + 0.2, AY1 - 0.1, 0.22): B.box('iron', (xr, yy, z0 + 4.7), (0.025, 0.025, 0.95))
        for yy in np.arange(AY0 + 1.0, AY1, 2.4): B.box('iron', (xd, yy, z0 + 3.85), (1.0, 0.06, 0.06), rot=(0, -s * 28, 0)); B.box('iron', (xd + s * 0.5, yy, z0 + 3.95), (0.05, 0.05, 0.35))
    sx_, sy_ = 19.6, 32.6; B.cyl('iron', (sx_, sy_, z0 + 2.2), 0.07, 4.4, seg=10)
    for k in range(19):
        a = math.radians(k * 21 + 180); zz = z0 + 0.22 * (k + 1)
        with B.xf((sx_, sy_, zz), (0, 0, math.degrees(a))): B.box('oak', (0.5, 0, 0), (0.9, 0.36, 0.05)); B.box('iron', (0.95, 0, 0.45), (0.025, 0.025, 0.9)); B.box('red', (0.95, 0.1, 0.92), (0.06, 0.4, 0.05), rot=(-12, 0, 0))
    for (x0_, y_, xt) in ((AX0 + 0.55 + 0.8, 15.6, AX0 + 0.62), (AX1 - 0.55 - 0.8, 8.2, AX1 - 0.62), (AX1 - 0.55 - 0.8, 20.4, AX1 - 0.62)):
        K.rolling_ladder(B, (x0_, y_, z0), (xt, y_, z0 + 3.9), width=0.46, rungs=14)
    for x in (AX0 + 0.62, AX1 - 0.62): B.box('iron', (x, (AY0 + AY1) / 2, z0 + 3.92), (0.05, AY1 - AY0 - 0.4, 0.05))
    # gasoliers (3), wall brackets at the ends, banners, signs
    gk = Pp.get('gasolier_k', 1.0)
    for yy in (8.0, 17.0, 26.5): K.gasolier(B, (17.0, yy, VCZ + VR - 0.1), drop=2.6, watts=900 * gk, arms=6, r=0.62)
    for x in (15.2, 18.8):
        K.gas_bracket(B, (x, AY1 - 0.02, z0 + 3.0), rot_z=-90, watts=40); K.gas_bracket(B, (x, AY0 + 0.02, z0 + 3.0), rot_z=90, watts=40)
    sign(B, 'ARCHIVES', 6.4, 1.3, (17.0, AY1 - 0.08, z0 + 6.1), n=(0, -1), fg=GOLD, bg=COBALT, emit=0.5, depth=0.12)
    sign(B, 'ARCHIVES', 1.9, 0.52, (AX0 + 0.6, 9.6, z0 + 3.3), n=(1, 0), fg=GOLD, bg=COBALT, emit=0.5)
    sign(B, 'ARCHIVES', 1.7, 0.46, (AX0 + 0.6, 5.7, z0 + 3.3), n=(1, 0), fg=GOLD, bg=COBALT, emit=0.5)
    W['banners'] = []
    for (txt, yy, bg, fg) in (('PETIT', 9.5, '#2a6cff', GOLD), ('MOYEN', 18.0, AMBER, ZENITH), ('GRAND', 27.4, KEPI, GOLD)):
        hg = bpy.data.objects.new('banner_%s' % txt, None); bpy.context.scene.collection.objects.link(hg); hg.location = (17.0, yy, VCZ + VR - 0.3)
        Bn = Batch(5); Bn.box('gold', (0, 0, 0.02), (3.5, 0.08, 0.06)); Bn.box('red' if txt != 'GRAND' else 'gold', (0, 0, -1.36), (3.3, 0.04, 0.06))
        for o_ in Bn.finalize('banner_rod_' + txt, ink_t=0.01): o_.parent = hg
        for s in (-1, 1):
            ob = plane('banner_%s_%d' % (txt, s), (0, s * 0.012, -0.68), (3.3, 1.3), rotz=0 if s < 0 else 180, mat=_sign_mat('banner_' + txt, tex_sign(txt, 3.3, 1.3, fg, bg, 'serif', maxh=0.62), 0.45)); ob.parent = hg
        for xx in (-1.6, 1.6): B.cyl('iron', (17.0 + xx, yy, VCZ + VR - 0.15), 0.012, 0.35, seg=6)
        W['banners'].append(hg)
    # desks with banker lamps (amber pools), trolleys, overflow piles; Bertillon's desk under GRAND with candle + card fan
    for (dx, dy, rz) in ((18.4, 6.2, 0), (18.0, 14.2, 0), (16.2, 20.0, 0)):
        with lift(B): K.table(B, (dx, dy), size=(1.3, 0.7), h=0.85, rot=rz, mat='walnut', top='baize'); K.stool(B, (dx, dy - 0.75), h=0.62, rot=15)
        with B.xf((dx, dy, z0), (0, 0, rz)): K.ledger_stack(B, (0.35, 0.05, 0.862), n=5, rot=8); K.fan_cards_static(B, (-0.15, -0.05, 0.862), n=6, spread=50, r=0.2)
        K.banker_lamp(B, (dx - 0.45, dy + 0.15, z0 + 0.862), rot=0, watts=0 if night else 70)
    bx, by = 16.5, 27.7
    with lift(B): K.table(B, (bx, by), size=(1.7, 0.85), h=0.86, rot=90, mat='walnut', top='baize'); K.stool(B, (bx - 0.75, by + 0.2), h=0.64, rot=30)
    with B.xf((bx, by, z0), (0, 0, 90)):
        K.ledger_stack(B, (0.55, -0.15, 0.872), n=6, rot=-8); K.open_ledger(B, (-0.15, 0.05, 0.872), rot=4); K.inkpot(B, (0.2, 0.28, 0.872)); K.spreading_calipers(B, (-0.5, 0.2, 0.872), rot=150, span=0.22, leg=0.3)
    K.banker_lamp(B, (bx + 0.15, by + 0.6, z0 + 0.872), rot=200, watts=85)
    B.cyl('cream', (bx + 0.2, by - 0.5, z0 + 0.95), 0.025, 0.16, seg=10); B.cyl('brass', (bx + 0.2, by - 0.5, z0 + 0.875), 0.06, 0.012, seg=12); B.sphere('glow_candle', (bx + 0.2, by - 0.5, z0 + 1.06), 0.022, scale=(1, 1, 1.8))
    A['lights'].append(K.point((bx + 0.2, by - 0.5, z0 + 1.1), color=(1.0, 0.7, 0.35), watts=28, radius=0.03, name='candle'))
    K.cards_fan_objects('fan', (bx - 0.05, by - 0.2, z0 + 0.876), n=9, w=0.2, d=0.15, rot=100, spread=75)
    for (px, py, nn) in ((14.6, 29.6, 4), (14.4, 30.4, 3), (19.9, 28.6, 5), (15.0, 31.6, 2), (16.3, 10.0, 4), (16.75, 10.35, 2)):
        for k in range(nn): B.box('box_ochre' if k % 2 else 'cream', (px + r.uniform(-0.05, 0.05), py, z0 + 0.12 + k * 0.24), (0.5, 0.36, 0.24), rot=(0, 0, r.uniform(-12, 12)))
    for k, (tx, ty) in enumerate(((16.5, 5.6), (17.8, 11.6), (16.3, 17.4), (17.9, 31.2), (15.4, 10.7))):
        with B.xf((tx, ty, z0), (0, 0, 15 * k)):
            B.box('walnut', (0, 0, 0.62), (0.9, 0.5, 0.06)); B.box('walnut', (0, 0, 0.25), (0.9, 0.5, 0.04)); B.box('iron', (0.5, 0, 0.85), (0.04, 0.5, 0.04))
            for sx in (-1, 1):
                for sy in (-1, 1): B.cyl('iron', (sx * 0.4, sy * 0.22, 0.32), 0.015, 0.62, seg=6); B.cyl('dark', (sx * 0.4, sy * 0.22, 0.06), 0.06, 0.03, axis='y', seg=10)
            for j in range(3): B.box('box_ochre' if j != 1 else 'drawer', (-0.27 + j * 0.28, 0, 0.75), (0.26, 0.4, 0.2))
    # tally board on the east gallery rail (image sequence 0..241)
    for n_ in range(0, 242): tex_tally(n_)
    tb = (AX1 - 1.1 - 0.55, 27.0, z0 + 4.85); B.box('walnut', (tb[0] + 0.03, tb[1], tb[2]), (0.06, 1.7, 1.08))
    tm = _sign_mat('tally', tex_tally(0), 0.35); it = [n_ for n_ in tm.node_tree.nodes if n_.bl_idname == 'ShaderNodeTexImage'][0]
    img = bpy.data.images.load(tex_tally(0), check_existing=False); img.source = 'SEQUENCE'; it.image = img; W['tally'] = it
    plane('tally', (tb[0] - 0.01, tb[1], tb[2]), (1.6, 1.0), rotz=face_rot((-1, 0)), mat=tm); set_tally(0)
    # the reveal assembly in the GRAND bank (west, lower storey), facing +x
    cw_ = A['banks'][('GRAND', 'W', 0)]['cell'](hero_cc, 2); HERO.update(y=cw_[1], z=cw_[2]); hx, hy, hz = HERO['face'], cw_[1], cw_[2]
    K.drawer_assembly('big', (hx, hy, hz), -90, w=0.9, h=0.4, depth=0.95, travel=0.78, open_=0.0, cards=34, seed=9, cards_to=-0.52)
    slide = K.STATE['anim']['big']['slide']
    Br = Batch(2); Br.box('leather', (-0.18, -0.2, -0.175 + 0.04), (0.38, 0.28, 0.08)); Br.box('navy', (-0.17, -0.2, -0.175 + 0.075), (0.36, 0.27, 0.014)); Br.finalize('riser', parent=slide, ink_t=0.008)
    K.card_box('box', (-0.18, -0.2, -0.175 + 0.08), rot_z=-4, w=0.34, d=0.24, h=0.28, lid=0.0, cards=10, seed=5, parent=slide, mat='box_ochre', lining='walnut')
    K.card_box('box2', (0.1, -0.3, -0.175), rot_z=6, w=0.28, d=0.22, h=0.17, lid=0.0, cards=8, seed=6, parent=slide)
    Bc = Batch(2); K.sliding_calipers(Bc, (0.34, -0.14, -0.178), rot=78, length=0.42, open_=0.13); Bc.finalize('dcal', parent=slide, ink_t=0.007)
    K.STATE['cardpaths']['card_martin'] = tex_hero_v2(); K.card_plane('hero', (0, 0, 0), (0.30, 0.20), rot=(0, 0, 0), key='card_martin', parent=K.STATE['anim']['box']['root'], ink_t=0.005)
    K.STATE['hero_z0'] = 0.28 - 0.05; K.STATE['anim']['hero']['root'].location = (0.0, 0.0, K.STATE['hero_z0'])
    for k, dc in enumerate((-2, -1, 1, 2)):                                                 # readable labels on the hero row: GRAND + number ranges
        p_ = A['banks'][('GRAND', 'W', 0)]['cell'](hero_cc + dc, 2); lo = 2401 + (hero_cc + dc) * 60
        sign(None, 'GRAND', 0.34, 0.16, (p_[0] + 0.05, p_[1], p_[2] + 0.07), n=(1, 0), fg='#3a1a0a', bg='#f6dfa0', sub='%d–%d' % (lo, lo + 59), emit=0.3, board=False, frame='#7a4a1a', maxh=0.7)
    with lift(B): K.table(B, (14.75, hy - 1.25), size=(0.7, 0.5), h=0.78, rot=15, top='baize')
    with B.xf((14.75, hy - 1.25, z0), (0, 0, 15)): K.sliding_calipers(B, (-0.05, 0.0, 0.788), rot=-12, length=0.5, open_=0.17); K.inkpot(B, (-0.25, 0.14, 0.788), rot=10)
    K.banker_lamp(B, (14.95, hy - 1.4, z0 + 0.788), rot=200, watts=60); K.stool(B, (14.45, hy + 0.55, 0), h=0.62) if False else None
    with lift(B): K.stool(B, (14.5, hy + 0.65), h=0.62, rot=-10)
    A['lights'].append(K.spot((15.25, hy + 0.4, hz + 1.5), (hx + 0.55, hy + 0.15, hz), watts=P().get('box_w', 120), angle=36, blend=0.7, color=(1.0, 0.76, 0.42), name='box_lamp', radius=0.05))
    # lights: the archive sun through the skylights, skylight fill areas, warm strip fills along both galleries
    for (a, b) in SKY: A['lights'].append(K.area((17.0, (a + b) / 2, VCZ + VR - 0.3), (17.0, (a + b) / 2, z0), (2.4, b - a), 260 * (0.6 if night else 1.0), color=(0.75, 0.85, 1.0), name='sky_area'))
    for x, tx in ((AX0 + 1.6, AX1), (AX1 - 1.6, AX0)):
        A['lights'].append(K.area((x, 18.0, z0 + 3.5), (tx, 18.0, z0 + 2.0), (30.0, 1.2), Pp.get('fill_w', 380), color=Pp.get('fill_col', (1.0, 0.72, 0.4)), name='strip_fill', long_axis=(0, 1, 0)))
    for x in (AX0 + 2.2, AX1 - 2.2):                                                        # moon / sky bounce on the vault and ribs (cool, cobalt)
        A['lights'].append(K.area((x, 18.0, WT - 0.6), (17.0, 18.0, VCZ + VR + 2.0), (31.0, 1.0), Pp.get('vault_w', 140), color=(0.45, 0.6, 1.0), name='vault_fill', long_axis=(0, 1, 0)))
    d = np.array(Pp['sun_dir'], float); d /= np.linalg.norm(d); A['dust_boxes'] = []
    for (a, b) in SKY:
        cs = [(15.8, a, VCZ + VR), (18.2, a, VCZ + VR), (18.2, b, VCZ + VR), (15.8, b, VCZ + VR)]; K.light_shaft(B, cs, d, z_end=z0)
        A['dust_boxes'].append(dict(p0=np.array([17.0, (a + b) / 2, VCZ + VR - 0.4]), d=d, L=7.5, w=1.8, n=34, scale=1.6))
    M.update({'bert_bank': (14.35, hy - 0.55, z0, 90, 'clerk'), 'dupont_stool': (14.55, hy + 0.65, z0, 180, 'prisoner'), 'insp_bank': (15.75, hy - 1.0, z0, 120, 'inspector'),
              'gend_a': (15.4, hy + 1.6, z0, 200, 'gendarme'), 'gend_b': (16.1, hy - 2.2, z0, 120, 'gendarme'), 'bert_desk': (15.85, by + 0.1, z0, 90, 'clerk'),
              'insp_door': (13.6, 9.6, z0, 90, 'inspector'), 'escort_mid': (17.0, 16.0, z0, 0, 'prisoner'), 'clerk_t0': (16.9, 5.0, z0, 0, 'clerk'), 'clerk_t1': (18.2, 11.0, z0, 200, 'clerk'),
              'clerk_t2': (15.9, 17.0, z0, 30, 'clerk'), 'clerk_gal_w': (14.15, 15.0, z0 + 4.2, 90, 'clerk'), 'clerk_gal_e': (19.85, 21.0, z0 + 4.2, 270, 'clerk'), 'thief_line': (17.0, 9.0, z0, 0, 'prisoner')})
    return A

# ================================================================ life (v2): smoke (30 chimneys + stove), dust in every shaft, flicker x mix, pendulum, wagon, breath
def _smoke_sources(srcs, wind=(0.8, 0.0), rise=2.2, tag='smk'):
    for si, src in enumerate(srcs):
        puffs = []
        for i in range(8):
            B = Batch(si * 11 + i); B.sphere('smoke', (0, 0, 0), 1.0, seg=12, rings=7); o = B.finalize('%s%d_%d' % (tag, si, i), ink=False)[0]; o.location = src; o.scale = (0.001,) * 3; o.visible_shadow = False; puffs.append(o)
        W['smoke'].append(dict(src=np.array(src, float), puffs=puffs, wind=wind, rise=rise, size=1.0 if rise > 1.5 else 0.6))
def _dust_box(db, seed=7):
    r = random.Random(seed); d = db['d'] / np.linalg.norm(db['d']); a = np.cross(d, [0, 0, 1.0]); a /= np.linalg.norm(a); b = np.cross(d, a); motes = []
    for i in range(db.get('n', 30)):
        B = Batch(i); B.sphere('glow_dust', (0, 0, 0), 1.0, seg=8, rings=5); o = B.finalize('dust%d_%d' % (seed, i), ink=False)[0]; o.scale = (0.001,) * 3
        motes.append(dict(ob=o, s=r.uniform(0.0, 1.0), u=r.uniform(-0.5, 0.5), v=r.uniform(-0.5, 0.5), ph=r.uniform(0, 6.28), sz=r.uniform(0.008, 0.016) * db.get('scale', 1.0)))
    W['dust'].append(dict(p0=np.array(db['p0'], float), d=d, a=a, b=b, L=db['L'], w=db['w'], motes=motes))
def set_smoke2(level=1.0, frame=None, speed=1.0):
    """chimney smoke (up to 30 sources on the street + rooftop plate) and the stove smoke: 8 puffs per source rising, drifting, growing, fading."""
    t = K._tsec(frame)
    for sm in W['smoke']:
        for i, o in enumerate(sm['puffs']):
            p = (t * 0.22 * speed + i / len(sm['puffs'])) % 1.0; rad = (0.05 + 0.22 * p) * sm['size'] * 2.2 * level * (1 - max(0, (p - 0.72) / 0.28)); rad = max(rad, 0.0005)
            rise = (0.12 + 1.5 * p) * (0.6 + 0.6 * level) * sm['rise']
            o.location = tuple(sm['src'] + np.array([sm['wind'][0] * p * 1.6 + 0.05 * math.sin(6.28 * p * 2 + i), sm['wind'][1] * p + 0.05 * math.cos(i + p * 5), rise])); o.scale = (rad,) * 3
            if frame is not None: K._key(o, 'location', frame); K._key(o, 'scale', frame)
def set_dust2(k=1.0, frame=None):
    """dust motes drifting in every light shaft (measuring-room window, 5 archive skylights)."""
    t = K._tsec(frame)
    for g in W['dust']:
        for m in g['motes']:
            s = (m['s'] + t * 0.02) % 1.0; pos = g['p0'] + g['d'] * (g['L'] * s) + g['a'] * (g['w'] * (m['u'] * (0.4 + s))) + g['b'] * (g['w'] * (m['v'] * (0.4 + s)) * 0.8)
            pos = pos + np.array([0.06 * math.sin(t * 0.9 + m['ph']), 0.06 * math.cos(t * 0.7 + 2 * m['ph']), -0.05 * ((t * 0.12 + m['ph']) % 1.0)])
            sz = max(m['sz'] * k * (0.75 + 0.25 * math.sin(t * 2.3 + m['ph'] * 3)), 0.0003); o = m['ob']; o.location = tuple(pos); o.scale = (sz,) * 3
            if frame is not None: K._key(o, 'location', frame); K._key(o, 'scale', frame)
def set_flicker2(level=1.0, frame=None, seed=0):
    """gas flicker (bertillon.set_flicker) times the per-lamp light-mix multiplier (set_light_mix)."""
    t = K._tsec(frame); mul = W.get('lampmul', {})
    for i, (ob, base) in enumerate(K.STATE['lamps']):
        ph = i * 1.7 + seed; f = 1 + level * (0.055 * math.sin(2 * math.pi * 3.1 * t + ph) + 0.04 * math.sin(2 * math.pi * 7.7 * t + 2 * ph) + 0.025 * math.sin(2 * math.pi * 13.1 * t + 3 * ph))
        ob.data.energy = base * f * mul.get(ob.name, 1.0)
        if frame is not None: K._key(ob.data, 'energy', frame)
    f0 = 1 + level * (0.05 * math.sin(2 * math.pi * 3.1 * t) + 0.03 * math.sin(2 * math.pi * 7.7 * t))
    for (m, base) in K.STATE['glows']:
        sk = m.node_tree.nodes['strength'].inputs[1]; sk.default_value = base * f0 * W.get('glowmul', {}).get(m.name, 1.0)
        if frame is not None: sk.keyframe_insert('default_value', frame=frame)
def set_wagon(t=1.0, frame=None, dist=22.0):
    """the Black Maria + horse trot in along +y: t 0 = `dist` m back down the street, 1 = parked at the steps (3.0, 8.6). ease-out."""
    w = W.get('wagon')
    if not w: return
    e = 1 - (1 - max(0.0, min(1.0, t))) ** 2; hx, hy, hz = w['home']; w['root'].location = (hx, hy - dist * (1 - e), hz)
    if frame is not None: K._key(w['root'], 'location', frame)
def key_life2(f0, f1, flicker=1.0, smoke=1.0, dust=1.0, step=1):
    """key every life hook on every frame f0..f1 (bertillon's keys rule): flicker x mix, smoke, dust, pendulum, banner sway. Flags wave by themselves."""
    for f in range(int(f0), int(f1) + 1, step):
        set_flicker2(flicker, frame=f); set_smoke2(smoke, frame=f); set_dust2(dust, frame=f); K.set_pendulum(frame=f); set_banner_sway(frame=f)
def life_at(g):
    """set (not key) every life hook for one frame g (stills)."""
    set_flicker2(1.0, frame=None); f = g + 1
    bpy.context.scene.frame_set(f); set_smoke2(1.0); set_dust2(1.0); K.set_pendulum(t=K._tsec(f)); set_banner_sway(t=K._tsec(f))

# ---------------------------------------------------------------- light mix (T5 night -> dawn)
def set_light_mix(a, b, t, frame=None, loc='archive'):
    """blend location `loc` from light preset a to b (t 0..1): sun energy + colour, the painted ambient of every material (shade, tint, lift, gain),
    frosted skylight + beam strength and colour, area fills, and the gas lamps (lamp_k, gasolier_k) through the flicker multiplier. Key it with frame
    on every frame of the change (and call set_flicker2 / key_life2 after, which applies the lamp multiplier)."""
    A_, B_ = K.LIGHTS[a], K.LIGHTS[b]; lp = lambda x, y: tuple((1 - t) * np.array(x, float) + t * np.array(y, float)); L = W['locs'][loc]
    def kk(sock):
        if frame is not None: sock.keyframe_insert('default_value', frame=frame)
    for o in L.coll.objects:
        if o.type == 'LIGHT':
            d = o.data
            if d.type == 'SUN':
                for Pq in (A_, B_): pass
                ka, kb = np.array(A_['key']) * A_.get('sun_k', 1.0), np.array(B_['key']) * B_.get('sun_k', 1.0); kv = (1 - t) * ka + t * kb; s = float(kv.max())
                d.energy = K.SUN_STRENGTH * s; d.color = tuple(kv / max(s, 1e-6))
                if frame is not None: d.keyframe_insert('energy', frame=frame); d.keyframe_insert('color', frame=frame)
            elif d.type == 'AREA' and o.name.startswith(('strip_fill', 'sky_area')):
                if 'e0' not in o: o['e0'] = d.energy
                if o.name.startswith('strip_fill'): d.energy = (1 - t) * A_.get('fill_w', 300) + t * B_.get('fill_w', 300)
                else: d.energy = o['e0'] * ((1 - t) * 1.0 + t * (1.0 / 0.6 if a == 'ARCHIVE_NIGHT' else 1.0))
                if frame is not None: d.keyframe_insert('energy', frame=frame)
            elif d.type == 'POINT':
                gk = 1.0
                if o.name.startswith('lamp') and A_.get('gasolier_k', 1.0) != B_.get('gasolier_k', 1.0): gk = ((1 - t) * A_.get('gasolier_k', 1.0) + t * B_.get('gasolier_k', 1.0)) / A_.get('gasolier_k', 1.0)
                W.setdefault('lampmul', {})[o.name] = ((1 - t) * A_['lamp_k'] + t * B_['lamp_k']) / A_['lamp_k'] * gk
    mats = set()
    for o in L.coll.objects:
        if o.type == 'MESH':
            for m in o.data.materials:
                if m: mats.add(m)
    for m in mats:
        nt = m.node_tree; nd = nt.nodes
        if 'amb_shade' in nd and 'pal' in m:
            pal = m['pal']; sm = list(pal['sm']); smm = sum(sm) / 3.0; mix = pal['mix']
            nd['amb_shade'].inputs[7].default_value = (*[x * y for x, y in zip(lp(A_['shade'], B_['shade']), sm)], 1); kk(nd['amb_shade'].inputs[7])
            nd['amb_tint'].inputs[0].default_value = tuple(x * mix * smm for x in lp(A_['tint'], B_['tint'])); kk(nd['amb_tint'].inputs[0])
            nd['amb_lift'].inputs[1].default_value = lp(A_['lift'], B_['lift']); kk(nd['amb_lift'].inputs[1])
            nd['amb_gain'].inputs['Scale'].default_value = (1 - t) * A_['gain'] + t * B_['gain']; kk(nd['amb_gain'].inputs['Scale'])
        elif m.name.startswith('glow_frost') and 'strength' in nd:
            fa, fb = A_.get('frost', ('#fff4e8', 3.0)), B_.get('frost', ('#fff4e8', 3.0)); e = nd['strength']
            e.inputs[0].default_value = (*lp(hex_lin(fa[0]), hex_lin(fb[0])), 1); e.inputs[1].default_value = (1 - t) * fa[1] + t * fb[1]; kk(e.inputs[0]); kk(e.inputs[1])
        elif m.name.startswith('beam_fx') and 'strength' in nd:
            e = nd['strength']; e.inputs[1].default_value = 0.035 * ((1 - t) * A_.get('beam_k', 1.0) + t * B_.get('beam_k', 1.0)); kk(e.inputs[1])
            e.inputs[0].default_value = (*lp(hex_lin('#9ab8ff'), hex_lin('#ffe2b0')), 1) if a == 'ARCHIVE_NIGHT' else e.inputs[0].default_value; kk(e.inputs[0])

# ================================================================ world_build: the visibility sets per take
TAKE_PARTS = {'T1': ('roofs', 'street', 'facade', 'measure'), 'T2': ('street', 'facade', 'corridor', 'measure'), 'T3': ('measure',), 'T4': ('measure', 'archive'),
              'T5': ('archive',), 'T6': ('archive',), 'T7': ('archive',), 'T8': ('measure',), 'ALL': ('roofs', 'street', 'facade', 'corridor', 'measure', 'archive')}
TAKE_LIGHT = {'T1': {'ext': 'BLUE_HOUR_EXT', 'measure': 'SUNSET_INT'}, 'T2': {'ext': 'BLUE_HOUR_EXT', 'corridor': 'GASLIGHT_INT', 'measure': 'SUNSET_INT'},
              'T3': {'measure': 'SUNSET_INT'}, 'T4': {'measure': 'SUNSET_INT', 'archive': 'ARCHIVE_DAY'}, 'T5': {'archive': 'ARCHIVE_NIGHT'},
              'T6': {'archive': 'ARCHIVE_DAY'}, 'T7': {'archive': 'ARCHIVE_DAY'}, 'T8': {'measure': 'SUNSET_INT'}}
TAKE_OVER = {   # per take, per location overrides of the light preset (SET gate v2b): T1 window brightest pool; T6 -12 % / T7 +5 % luma
    'T1': {'measure': dict(win_w=300, win_lamp=170, shade_mul=0.88)}, 'T6': {'archive': dict(shade_mul=0.8, fill_w=220, vault_w=100, gain=0.65, beam_k=0.5, frost=('#7f9ef0', 1.1))}, 'T7': {'archive': dict(shade_mul=1.16, fill_w=400)}}
TAKE_CUTAWAY = {'T3': ('measure',), 'T7': ('archive',), 'T8': ('measure',)}
def ML(x, y, z=0.0): return (x + MO[0], y + MO[1], z + MO[2])
def world_build(take='ALL', light=None, parts=None, cutaway=None):
    """build the connected world for one take: only the locations in TAKE_PARTS[take] (or `parts`), each lit by TAKE_LIGHT[take] (or `light`, a
    dict loc -> preset, or one preset name for every location). Returns A: marks (world), lights, take. The camera 'cam' is created (22 mm)."""
    world_new(); W['take'] = take; parts = parts or TAKE_PARTS[take]; lights = dict(TAKE_LIGHT.get(take, {}))
    if isinstance(light, str): lights = {k: light for k in ('ext', 'corridor', 'measure', 'archive')}
    elif isinstance(light, dict): lights.update(light)
    A = {'marks': {}, 'lights': [], 'take': take, 'parts': parts}; t0 = time.time(); cut = cutaway if cutaway is not None else TAKE_CUTAWAY.get(take, ())
    for k, kind in (('card_notice', 'notice'), ('card_portrait', 'portrait'), ('card_portrait2', 'portrait2'), ('card_bertillon', 'bertillon')):
        K.STATE['cardpaths'][k] = TX.card(k, 'notice', 7) if kind == 'notice' else (TX.frame_art(k, 11 if kind == 'portrait' else 12) if kind.startswith('portrait') else TX.card(k, 'bertillon', 7))
    if 'street' in parts or 'facade' in parts:
        with Loc('ext', lights.get('ext', 'BLUE_HOUR_EXT'), TAKE_OVER.get(take, {}).get('ext')) as L:
            n0 = len(A['lights']); B = Batch(1); B.ceil = Batch(2); B.out = Batch(3)
            if 'street' in parts: build_street2(B, A)
            if 'facade' in parts: build_facade(B, A)
            tops = paris_roofscape() if 'roofs' in parts else []
            B.finalize('ext'); B.ceil.finalize('ext_ceil')
            _sky_mat2(); Bs = Batch(4); Bs.sphere('sky2', (0, 30, 0), 520.0, seg=48, rings=24); dome = Bs.finalize('sky', ink=False)[0]
            dome.visible_shadow = dome.visible_diffuse = dome.visible_glossy = False
            Pp = P()
            if Pp.get('sun_k', 1.0) > 0: L.link_light(K.sun())
            A['lights'].append(K.area((-6.0, 14.0, 22.0), (2.0, 14.0, 0.0), (40.0, 30.0), Pp.get('fill_w', 900), color=Pp.get('fill_col', (0.45, 0.6, 1.0)), name='sky_fill', long_axis=(0, 1, 0)))
            for o in A['lights'][n0:]:
                if o.data.type in ('AREA', 'SUN'): L.link_light(o)
            ch = [c for c in K.STATE.get('chims', []) if c[1] > -20] + list(tops); ch.sort(key=lambda c: math.hypot(c[0] - 0.0, c[1] - 12.0)); _smoke_sources(ch[:30], wind=(0.9, 0.3), rise=2.4, tag='chs')
            nose = A.get('fiacre_nose')
            if nose: _smoke_sources([nose], wind=(0.25, -0.2), rise=0.25, tag='brf')
            _smoke_sources([tuple(Vector(W['wagon']['root'].location) + Vector(W['wagon']['nose_local']))], wind=(0.2, 0.3), rise=0.25, tag='brw')
            W['breath_wagon'] = W['smoke'][-1]
    if 'corridor' in parts:
        with Loc('corridor', lights.get('corridor', 'GASLIGHT_INT'), TAKE_OVER.get(take, {}).get('corridor')) as L:
            n0 = len(A['lights']); B = Batch(5); B.ceil = Batch(6); build_corridor(B, A, with_end_wall='archive' not in parts); B.finalize('corr'); B.ceil.finalize('corr_ceil')
            for o in A['lights'][n0:]:
                if o.data.type in ('AREA', 'SUN'): L.link_light(o)
    if 'measure' in parts:
        with Loc('measure', lights.get('measure', 'SUNSET_INT'), TAKE_OVER.get(take, {}).get('measure')) as L:
            before = set(o.name for o in bpy.data.objects); A2 = {'marks': {}, 'lights': []}; B = Batch(7); B.ceil = Batch(8)
            build_measure2(B, A2); B.finalize('measure'); W['ceil_measure'] = B.ceil.finalize('measure_ceil'); K._place_wall_cards()
            pv = A2['pendulum_local']; pr = bpy.data.objects.new('pend_root', None); bpy.context.scene.collection.objects.link(pr); pr.location = pv['pivot']
            Bp = Batch(3); Bp.box('iron', (0, 0, -pv['L'] / 2), (0.012, 0.01, pv['L'])); Bp.cyl('brass', (0, 0, -pv['L'] - 0.03), 0.075, 0.025, axis='y', seg=18); Bp.finalize('pend', parent=pr, ink_t=0.005); K.STATE['life']['pendulum'] = pr
            sun = K.sun(); L.link_light(sun); L.block = [sun]
            root = bpy.data.objects.new('measure_root', None); bpy.context.scene.collection.objects.link(root); root.location = MO
            for o in bpy.data.objects:
                if o.name not in before and o.parent is None and o is not root: o.parent = root
            bpy.context.view_layer.update()
            for o in A2['lights']:
                if o.data.type in ('AREA', 'SUN'): L.link_light(o)
            A['lights'] += A2['lights']
            for k, (x, y, z, fz, who) in A2['marks_local'].items(): A['marks'][k] = (x + MO[0], y + MO[1], z + MO[2], fz, who)
            _smoke_sources([ML(*A2['smoke_src_local'])], wind=(0.25, 0.0), rise=1.0, tag='stv')
            db = dict(A2['dust_local']); db['p0'] = np.array(db['p0']) + np.array(MO); _dust_box(db, seed=7)
            A['clock'] = ML(*A2['clock_local'])
    if 'archive' in parts:
        with Loc('archive', lights.get('archive', 'ARCHIVE_DAY'), TAKE_OVER.get(take, {}).get('archive')) as L:
            n0 = len(A['lights']); B = Batch(9); B.ceil = Batch(10); build_archive(B, A); B.finalize('arch'); W['ceil_archive'] = B.ceil.finalize('arch_ceil')
            sun = K.sun(); L.link_light(sun); L.block = [sun]
            for o in A['lights'][n0:]:
                if o.data.type in ('AREA', 'SUN'): L.link_light(o)
            for i, db in enumerate(A['dust_boxes']): _dust_box(db, seed=20 + i)
            bm = K._MATS.get('beam_fx')
            if bm: bm.node_tree.nodes['strength'].inputs[0].default_value = (*hex_lin(P().get('beam_col', '#e4edff')), 1)
    W['cut'] = tuple(cut)
    W['marks'] = A['marks']; A['build_s'] = time.time() - t0
    cam = K.camera((0, -10, 2), (0, 0, 2), 22.0); cam.data.clip_end = 900; cam.data.clip_start = 0.05; cam.rotation_mode = 'QUATERNION'; A['cam'] = cam
    return A
_LocExit = Loc.__exit__
def _loc_exit(self, *a):
    r = _LocExit(self, *a)
    for ob in getattr(self, 'block', []): ob.light_linking.blocker_collection = self.coll
    return r
Loc.__exit__ = _loc_exit

# ================================================================ camera paths (PLAN §4 / §5): Hermite in time through keys, look-at path, lens path
def _lookrot(loc, look, up_hint=(0, 1, 0)):
    f = (Vector(look) - Vector(loc)).normalized(); up = Vector((0, 0, 1))
    if abs(f.dot(up)) > 0.995: up = Vector(up_hint)
    rgt = f.cross(up).normalized(); u = rgt.cross(f); M = Matrix((rgt, u, -f)).transposed(); return M.to_quaternion()
def _herm(keys, g, field):
    ts = [k['g'] for k in keys]
    if g <= ts[0]: return np.array(keys[0][field], float)
    if g >= ts[-1]: return np.array(keys[-1][field], float)
    i = max(j for j in range(len(ts) - 1) if ts[j] <= g)
    def tan(j):
        if j == 0 or j == len(keys) - 1 or keys[j].get('hold'): return np.zeros_like(np.array(keys[j][field], float))
        return (np.array(keys[j + 1][field], float) - np.array(keys[j - 1][field], float)) / (ts[j + 1] - ts[j - 1]) * keys[j].get('tension', 1.0)
    h = ts[i + 1] - ts[i]; u = (g - ts[i]) / h; p0, p1 = np.array(keys[i][field], float), np.array(keys[i + 1][field], float)
    h00, h10, h01, h11 = 2 * u ** 3 - 3 * u ** 2 + 1, u ** 3 - 2 * u ** 2 + u, -2 * u ** 3 + 3 * u ** 2, u ** 3 - u ** 2
    return h00 * p0 + h10 * h * tan(i) + h01 * p1 + h11 * h * tan(i + 1)
def cam_path(keys, g0=None, g1=None):
    """keys: [{'g', 'loc', 'look', 'lens' (default 22), 'hold' (zero velocity: ease in/out at this key), 'tension'}]. Cubic Hermite in time
    (Catmull-Rom tangents; the first and last key always hold, so every take eases in and out), roll 0 (world-up look-at; straight down uses +y as
    up). Returns [{'g', 'loc', 'look', 'rot' (quaternion wxyz), 'lens'}] for every frame g0..g1 (default: the keys' span)."""
    for k in keys: k.setdefault('lens', 22.0)
    g0 = keys[0]['g'] if g0 is None else g0; g1 = keys[-1]['g'] if g1 is None else g1; out = []; prev = None
    for g in range(int(g0), int(g1) + 1):
        loc = _herm(keys, g, 'loc'); look = _herm(keys, g, 'look'); lens = float(_herm(keys, g, 'lens')); q = _lookrot(loc, look)
        if prev is not None and q.dot(prev) < 0: q.negate()
        prev = q; out.append(dict(g=g, loc=tuple(map(float, loc)), look=tuple(map(float, look)), rot=tuple(q), lens=lens))
    return out
def set_cam(cam, fr):
    cam.location = fr['loc']; cam.rotation_mode = 'QUATERNION'; cam.rotation_quaternion = fr['rot']; cam.data.lens = fr['lens']
def key_cam(cam, frames, offset=1):
    """key the camera on every frame (Blender frame = g + offset; the render teams use g + 1 so that frame 1 = g 0)."""
    for fr in frames:
        f = fr['g'] + offset; set_cam(cam, fr); cam.keyframe_insert('location', frame=f); cam.keyframe_insert('rotation_quaternion', frame=f); cam.data.keyframe_insert('lens', frame=f)
def anchor_frac(fr, feet, H, W_=720, H_=1280):
    """height of a cast anchor (feet point, height H m) as a fraction of the frame height for camera frame fr (no Blender needed). Returns
    (fraction, in_frame, distance). in_frame: the head centre lies inside the frame."""
    q = fr['rot']; Mq = Euler((0, 0, 0)).to_quaternion(); Mq.w, Mq.x, Mq.y, Mq.z = q; R = Mq.to_matrix(); loc = Vector(fr['loc']); fpx = max(W_, H_) * fr['lens'] / 36.0
    def proj(p):
        v = R.transposed() @ (Vector(p) - loc); z = -v.z
        return (W_ / 2 + fpx * v.x / max(z, 1e-6), H_ / 2 - fpx * v.y / max(z, 1e-6), z)
    a = proj(feet); b = proj((feet[0], feet[1], feet[2] + H)); c = proj((feet[0], feet[1], feet[2] + H * 0.88))
    if a[2] <= 0.05 or b[2] <= 0.05: return 0.0, False, a[2]
    return abs(a[1] - b[1]) / H_, bool(0 <= c[0] <= W_ and 0 <= c[1] <= H_), (Vector(feet) - loc).length

# ================================================================ the takes (PLAN §4 / §5): cast anchors (placeholders) + camera keys
HCAST = {'bertillon': 1.78, 'inspector': 1.66, 'prefect': 1.74, 'dupont': 1.68, 'gendarme': 1.82, 'prisoner': 1.68, 'clerk': 1.75, 'seated': 1.32, 'seated_insp': 1.3}
CCOL = {'bertillon': ('#15142e', '#f3efe8'), 'inspector': ('#1f3fb0', KEPI), 'prefect': ('#141428', '#e8e2d0'), 'dupont': ('#6a5a1e', '#5a6a1e'), 'gendarme': ('#1a2a7a', KEPI),
        'prisoner': ('#4a5a8a', '#6a4a2a'), 'clerk': ('#2a1f4a', '#3a2a5a'), 'seated': ('#4a5a8a', '#6a4a2a'), 'seated_insp': ('#1f3fb0', KEPI)}
def _C(name, who, *path, look=None):
    """a cast anchor: path = (g, (x, y, z)) keys (feet), linear between keys."""
    return dict(name=name, who=who, path=list(path))
def cast_pos(c, g):
    P_ = c['path']
    if g <= P_[0][0]: return P_[0][1]
    if g >= P_[-1][0]: return P_[-1][1]
    for (ga, pa), (gb, pb) in zip(P_[:-1], P_[1:]):
        if ga <= g <= gb: u = (g - ga) / max(gb - ga, 1e-9); return tuple((1 - u) * np.array(pa) + u * np.array(pb))
def _k(g, loc, look, lens=22.0, hold=False, tension=1.0): return dict(g=g, loc=loc, look=look, lens=lens, hold=hold, tension=tension)
BIGZOOM = {'T1': (0, 105, 'bertillon'), 'T6': (1377, 1515, 'bertillon')}
def _takes():
    T = {}
    P1CARD = (14.29, 26.14, 2.876); _n = (0.9, -0.21, 0.37); P1CAM = tuple(P1CARD[i] + 0.44 * _n[i] for i in range(3)); P1CAM2 = tuple(P1CARD[i] + 0.42 * _n[i] for i in range(3))
    hy = HERO['y']; INSP6 = (15.2, 24.35, FZ); GA6 = (13.95, 28.2, FZ); GB6 = (16.9, 29.6, FZ)
    # ---- T1 hook + Paris (g 0-336): BIGZOOM 1 roofs -> French window -> bench; out and up; swoop to the wagon; arc on the steps
    T['T1'] = dict(g=(0, 336), render=(0, 342), cast=[
        _C('bertillon', 'bertillon', (0, ML(-1.95, 1.35)), (105, ML(-1.95, 1.35)), (140, ML(-1.95, 2.05)), (336, ML(-1.95, 2.05))),
        _C('prisoner_a', 'seated', (0, ML(-2.45, 0.85))), _C('prisoner_b', 'seated', (0, ML(-2.45, 1.55))), _C('prisoner_q', 'seated', (0, ML(-2.45, 2.25))),
        _C('gend_room', 'gendarme', (0, ML(1.3, -1.7))),
        _C('lamplighter', 'clerk', (0, (-3.85, 14.0, 1.05))), _C('flaneur_a', 'clerk', (0, (-2.6, 1.0, 0.0)), (336, (-1.4, 8.0, 0.0))), _C('flaneur_b', 'clerk', (0, (-4.9, 17.0, 0.14)), (336, (-4.9, 11.0, 0.14))),
        _C('newsboy', 'prisoner', (0, (-4.9, 7.6, 0.14))), _C('cafe_a', 'clerk', (0, (-4.6, 19.4, 0.14))), _C('gend_door_l', 'gendarme', (0, (4.25, 3.9, 0.14))), _C('gend_door_r', 'gendarme', (0, (4.25, 7.6, 0.14))),
        _C('prisoner_c', 'prisoner', (0, (3.0, 5.6, 0.0)), (250, (2.2, 6.0, 0.0)), (290, (2.9, 5.8, 0.0)), (330, (5.2, 5.7, 0.6))),
        _C('gend_wagon', 'gendarme', (0, (3.9, 6.0, 0.0))), _C('desk_gend', 'gendarme', (0, (4.6, 3.6, 0.14))), _C('flaneur_c', 'clerk', (0, (1.2, 10.4, 0.0)), (336, (0.6, 13.0, 0.0))), _C('newsboy2', 'prisoner', (0, (-1.6, 8.6, 0.0)))],
        keys=[_k(0, (-34.0, -6.0, 34.0), (5.7, 13.3, 10.5), hold=True), _k(46, (-14.0, 6.0, 17.0), ML(-2.2, 1.3, 1.6)), _k(78, (2.6, 12.9, 4.6), ML(0.2, 0.6, 0.6)),
              _k(92, (6.0, 12.75, 3.1), ML(1.2, 0.5, 0.2)), _k(105, ML(0.15, -0.55, 1.6), ML(-2.1, 1.35, 1.0), hold=True),
              _k(148, ML(0.0, 1.3, 1.55), ML(-2.2, 2.0, 1.0), hold=True),
              _k(158, ML(-0.7, 0.45, 2.9), ML(-2.0, 1.6, 1.1)), _k(168, (4.6, 12.5, 3.8), ML(-1.8, 1.4, 1.0)), _k(198, (0.0, 3.0, 12.5), (5.0, 6.5, 5.0)), _k(218, (-2.5, -3.0, 15.0), (5.0, 3.5, 6.0), hold=True),
              _k(255, (-3.0, -1.0, 7.0), (3.0, 8.0, 1.2)), _k(287, (-0.2, 2.6, 1.75), (2.8, 6.4, 1.15), hold=True),
              _k(336, (2.0, 2.4, 1.6), (4.9, 6.2, 1.3), hold=True)])
    # ---- T2 corridor + mockery (g 336-651)
    T['T2'] = dict(g=(336, 651), render=(330, 657), cast=[
        _C('thief', 'prisoner', (330, (4.4, 5.7, 0.14)), (350, (5.3, 5.7, 0.6)), (386, (7.6, 5.9, FZ)), (445, (9.4, 6.5, FZ)), (470, (11.6, 6.3, FZ)), (651, (12.2, 6.2, FZ))),
        _C('gend_corr', 'gendarme', (330, (7.45, 4.3, FZ)), (651, (7.6, 4.3, FZ))), _C('clerk_ladder', 'clerk', (330, (8.6, 6.95, FZ + 1.45))), _C('gend_ledger', 'gendarme', (330, (11.75, 6.45, FZ))),
        _C('pris_c0', 'seated', (330, (11.0, 4.45, FZ))), _C('pris_c1', 'seated', (330, (11.6, 4.45, FZ))), _C('pris_c2', 'seated', (330, (12.2, 4.45, FZ))),
        _C('bertillon', 'bertillon', (330, ML(1.45, 1.95))), _C('prisoner_chair', 'seated', (330, ML(0.7, 2.3, 0.0))), _C('inspector', 'inspector', (330, ML(-0.6, 0.2)), (493, ML(-0.6, 0.2)), (545, ML(-0.2, 1.4)), (657, ML(-0.2, 1.4))),
        _C('gend_room', 'gendarme', (330, ML(-1.4, -0.4))), _C('gend_room2', 'gendarme', (330, ML(2.6, -1.7))), _C('prisoner_b', 'seated', (330, ML(-2.45, 1.55)))],
        keys=[_k(330, (2.0, 5.2, 1.85), (8.0, 5.9, 1.9), hold=True), _k(360, (3.9, 5.5, 1.95), (9.0, 6.0, 2.0)), _k(386, (6.6, 5.2, 2.75), (10.0, 6.4, 1.7)),
              _k(445, (7.9, 4.4, 2.6), (9.9, 7.2, 3.1)), _k(470, (9.9, 5.6, 2.55), (10.3, 9.0, 2.3)), _k(493, (10.25, 8.5, 1.55), ML(-0.6, 1.6, 1.75)),
              _k(560, ML(2.3, 0.9, 1.5), ML(-0.2, 1.4, 1.35)), _k(593, ML(2.25, 1.0, 1.45), ML(-0.2, 1.4, 1.3), hold=True),
              _k(657, ML(2.15, 1.05, 1.35), ML(-0.2, 1.4, 1.4), lens=28.0, hold=True)])          # 2e: the OTS push continues on a 22 -> 28 mm push-in (the chair / tripod / table corner leaves no low path)
    # ---- T3 nickname + prefect (g 651-850): bird's-eye from the gasolier (ceiling cut away), crane to eye height, low under the table, into the clock
    T['T3'] = dict(g=(651, 850), render=(645, 856), cast=[
        _C('bertillon', 'bertillon', (645, ML(1.45, 1.95)), (780, ML(1.45, 1.95)), (802, ML(1.0, 1.3))), _C('prisoner_chair', 'seated', (645, ML(0.7, 2.3))), _C('inspector', 'inspector', (645, ML(-0.4, 0.3))),
        _C('gend_a', 'gendarme', (645, ML(-1.2, -0.3))), _C('gend_b', 'gendarme', (645, ML(1.3, -1.5))), _C('prankster', 'gendarme', (645, ML(2.0, 2.9)), (725, ML(1.9, 2.5)), (760, ML(1.6, 0.6)), (800, ML(-1.6, 1.2))),
        _C('prisoner_b', 'seated', (645, ML(-2.45, 1.55))), _C('prisoner_q', 'seated', (645, ML(-2.45, 0.85))),
        _C('prefect', 'prefect', (725, ML(1.1, -4.6)), (760, ML(1.0, -2.2)), (800, ML(0.8, -2.0)), (840, ML(1.1, -3.8)))],
        keys=[_k(645, ML(0.6, 1.3, 7.6), ML(0.75, 1.6, 0.0), hold=True), _k(700, ML(0.2, 0.6, 6.0), ML(0.7, 1.6, 0.4)), _k(745, ML(-2.0, 3.0, 3.6), ML(1.0, -2.6, 2.0)),
              _k(792, ML(0.6, 3.75, 1.8), ML(1.2, -3.0, 1.4)), _k(812, ML(2.85, 2.75, 0.5), ML(1.45, 1.95, 1.55), hold=True), _k(834, ML(2.4, 2.6, 2.1), ML(0.2, 4.2, 3.05)),
              _k(856, ML(0.05, 3.05, 2.95), ML(0.2, 4.2, 3.05), lens=22.0, hold=True)])
    # ---- T4 montage + drawers (g 850-1045): out of the clock, track the stations, low at the desk, through ARCHIVES -> into the hall
    T['T4'] = dict(g=(850, 1045), render=(844, 1051), cast=[
        _C('bertillon', 'bertillon', (844, ML(-1.0, 2.6)), (902, ML(-1.2, 2.9)), (930, ML(0.2, 2.6)), (955, ML(1.6, 2.6)), (971, ML(2.0, 0.4)), (991, ML(2.0, 0.4)), (1016, (13.6, 9.7, FZ)), (1040, (14.0, 12.4, FZ)), (1051, (14.0, 12.4, FZ))),
        _C('prisoner_s', 'prisoner', (844, ML(-1.55, 3.45)), (930, ML(-0.2, 3.3)), (955, ML(2.0, 3.0)), (1051, ML(2.1, 3.0))), _C('queue0', 'prisoner', (844, ML(-1.5, -0.6))), _C('queue1', 'prisoner', (844, ML(-0.3, -0.4))),
        _C('clerk', 'clerk', (844, ML(2.25, 0.2))), _C('clerk_arch', 'clerk', (844, (17.0, 14.0, FZ)), (1051, (17.2, 16.5, FZ)))],
        keys=[_k(844, ML(0.05, 3.05, 2.95), ML(0.2, 4.2, 3.05), hold=True), _k(902, ML(-1.6, -0.4, 2.3), ML(-0.7, 4.2, 1.2)), _k(971, ML(2.0, -0.9, 2.2), ML(1.9, 4.2, 1.0)),
              _k(991, ML(0.7, -1.4, 0.55), ML(2.0, 0.4, 1.2)), _k(1026, (12.1, 9.6, 2.45), (16.0, 11.2, 2.2)), _k(1051, (15.7, 8.5, 2.5), (14.4, 13.5, 2.0), hold=True)])
    # ---- T5 false payoff + crisis (g 1045-1377): night crane from the gallery onto the desk, OTS push down the aisle, dawn, escort, three-shot
    T['T5'] = dict(g=(1045, 1377), render=(1039, 1383), mix=(1196, 1211, 'ARCHIVE_NIGHT', 'ARCHIVE_DAY'), cast=[
        _C('bertillon', 'bertillon', (1039, (15.85, 27.75, FZ)), (1196, (15.85, 27.75, FZ)), (1274, (14.35, hy - 0.55, FZ))),
        _C('inspector', 'inspector', (1039, (15.4, 15.0, FZ)), (1196, (15.4, 15.0, FZ)), (1274, INSP6)),
        _C('dupont', 'dupont', (1196, (16.6, 12.6, FZ)), (1274, (16.6, 22.0, FZ)), (1300, (14.55, hy + 0.65, FZ))), _C('gend_a', 'gendarme', (1196, (17.3, 12.8, FZ)), (1274, (17.3, 22.2, FZ)), (1300, GA6)),
        _C('gend_b', 'gendarme', (1196, (15.9, 12.4, FZ)), (1274, (15.9, 21.8, FZ)), (1300, GB6))],
        keys=[_k(1039, (14.75, 32.3, 7.0), (15.9, 27.8, 1.6), hold=True), _k(1100, (15.0, 30.8, 3.6), (15.9, 27.6, 1.7)), _k(1125, (16.3, 28.9, 2.65), (15.6, 18.0, 2.0)),
              _k(1160, (17.9, 22.5, 2.55), (15.5, 15.0, 1.9)), _k(1196, (19.2, 16.8, 2.4), (15.6, 15.2, 1.9)), _k(1240, (19.4, 18.5, 2.2), (16.6, 19.5, 1.6)), _k(1274, (19.3, 22.0, 2.2), (16.5, 23.5, 1.6)),
              _k(1345, (17.9, 27.6, 2.2), (14.9, 26.0, 1.7), hold=True), _k(1383, (16.85, 26.7, 2.15), (14.6, 26.0, 1.9), hold=True)])
    # ---- T6 reveal (g 1377-1695): BIGZOOM 2 from the far end of the vault, P1 card, OTS, three-shot, P2 face
    T['T6'] = dict(g=(1377, 1695), render=(1371, 1701), cast=[
        _C('bertillon', 'bertillon', (1371, (14.35, hy - 0.55, FZ))), _C('dupont', 'dupont', (1371, (14.55, hy + 0.65, FZ))), _C('inspector', 'inspector', (1371, INSP6)),
        _C('gend_a', 'gendarme', (1371, GA6)), _C('gend_b', 'gendarme', (1371, GB6)), _C('clerk_gal', 'clerk', (1371, (19.85, 21.0, FZ + 4.2))), _C('clerk_t', 'clerk', (1371, (17.9, 11.6, FZ)))],
        keys=[_k(1371, (17.0, 2.9, 9.55), (15.1, 24.0, 0.4), hold=True), _k(1395, (16.95, 4.6, 9.2), (15.0, 24.5, 0.8)), _k(1440, (15.7, 9.5, 7.6), (14.9, 26.0, 1.8)), _k(1478, (15.6, 17.5, 5.4), (14.8, 26.1, 1.8)),
              _k(1515, (16.35, 24.55, 2.35), (14.55, 26.05, 1.85), hold=True), _k(1535, P1CAM, P1CARD, hold=True), _k(1545, P1CAM2, P1CARD, hold=True),
              _k(1560, (15.8, 26.85, 3.05), (14.35, 25.7, 2.0)), _k(1580, (15.6, 28.2, 2.35), (14.35, 25.7, 2.0), hold=True), _k(1640, (17.9, 27.6, 2.3), (14.9, 26.0, 1.8), hold=True), _k(1671, (17.9, 27.5, 2.3), (14.9, 26.0, 1.8), hold=True),
              _k(1695, (15.95, 25.1, 2.72), (15.2, 24.35, FZ + 1.5), hold=True), _k(1701, (15.92, 25.07, 2.72), (15.2, 24.35, FZ + 1.5), hold=True)])
    # ---- T7 aha + 200 (g 1695-1868): low hero under the GRAND drawer, crane up and out to top-down (vault cut away)
    T['T7'] = dict(g=(1695, 1868), render=(1689, 1874), cast=[
        _C('bertillon', 'bertillon', (1689, (14.35, hy - 0.55, FZ))), _C('dupont', 'dupont', (1689, (14.55, hy + 0.65, FZ))), _C('inspector', 'inspector', (1689, (15.5, 27.4, FZ))),
        _C('gend_a', 'gendarme', (1792, (17.0, 6.0, FZ)), (1874, (17.0, 16.0, FZ))), _C('thief1', 'prisoner', (1792, (17.0, 4.8, FZ)), (1874, (17.0, 14.8, FZ))), _C('thief2', 'prisoner', (1792, (17.0, 3.6, FZ)), (1874, (17.0, 13.6, FZ))),
        _C('gend_b', 'gendarme', (1689, GB6))],
        keys=[_k(1689, (16.15, 24.35, 1.45), (14.4, 25.6, 2.45), hold=True), _k(1792, (16.0, 24.1, 1.5), (14.4, 25.6, 2.5), hold=True), _k(1830, (16.9, 17.0, 11.0), (16.4, 22.0, 1.2)),
              _k(1874, (17.0, 5.0, 23.0), (17.0, 21.0, 1.2), hold=True)])
    # ---- T8 ending (g 1868-2052): bird's-eye over the measuring room, crane down past the gasolier, OTS behind the crowd, P3 on the ear
    T['T8'] = dict(g=(1868, 2052), render=(1862, 2052), cast=[
        _C('inspector', 'seated_insp', (1862, ML(0.7, 2.3))), _C('bertillon', 'bertillon', (1862, ML(1.3, 1.85))), _C('gend_a', 'gendarme', (1862, ML(1.9, 0.95))), _C('gend_b', 'gendarme', (1862, ML(-0.4, 0.9))),
        _C('crowd1', 'prisoner', (1862, ML(-0.9, 1.6))), _C('crowd2', 'gendarme', (1862, ML(0.4, 0.5))), _C('crowd3', 'prisoner', (1862, ML(2.3, 2.6))), _C('prefect', 'prefect', (1862, ML(-1.2, 2.7)))],
        keys=[_k(1862, ML(0.75, 1.6, 8.6), ML(0.75, 2.2, 0.0), hold=True), _k(1910, ML(-0.15, 0.6, 3.4), ML(0.6, 2.2, 0.6)), _k(1958, ML(2.75, -1.4, 2.3), ML(0.7, 2.1, 0.8), hold=True),
              _k(2018, ML(1.95, 0.25, 1.4), ML(0.7, 2.25, 1.0), hold=True), _k(2052, ML(1.25, 1.2, 1.3), ML(0.62, 2.28, 1.12), hold=True)])
    return T
TAKES = _takes()
def path_take(take):
    """the planned travelling path of a take: per-frame camera (location, look-at, rotation quaternion, lens) for its render range (with handles)."""
    t = TAKES[take]; return cam_path(t['keys'], *t['render'])
def path_T1(): return path_take('T1')
def path_T2(): return path_take('T2')
def path_T3(): return path_take('T3')
def path_T4(): return path_take('T4')
def path_T5(): return path_take('T5')
def path_T6(): return path_take('T6')
def path_T7(): return path_take('T7')
def path_T8(): return path_take('T8')
def cam_report(take, names=None, step=6, quiet=False):
    """stand_report-style check per frame: every cast anchor's height as % of the frame (and IN/out), camera speed (m/s). BIGZOOM takes also get
    the verdict: start < 5 %, end 35-60 % (PLAN §4 / QA §H.1). Returns {'rows': [...], 'bigzoom': {...}}."""
    t = TAKES[take]; frames = path_take(take); casts = [c for c in t['cast'] if not names or c['name'] in names]; rows = []
    for i, fr in enumerate(frames):
        if i % step and i != len(frames) - 1 and not (take in BIGZOOM and fr['g'] in BIGZOOM[take][:2]): continue
        sp = (Vector(frames[min(i + 1, len(frames) - 1)]['loc']) - Vector(frames[max(i - 1, 0)]['loc'])).length * 15.0
        row = dict(g=fr['g'], speed=sp, cast={})
        for c in casts:
            f, inn, d = anchor_frac(fr, cast_pos(c, fr['g']), HCAST[c['who']]); row['cast'][c['name']] = (f * 100, inn, d)
        rows.append(row)
        if not quiet: print('g %4d  %4.1f m/s  ' % (fr['g'], sp) + '  '.join('%s %4.1f%%%s' % (n, v[0], '' if v[1] else '(out)') for n, v in row['cast'].items() if v[1] or v[0] > 0))
    res = dict(rows=rows)
    if take in BIGZOOM:
        g0, g1, who = BIGZOOM[take]; c = [c for c in t['cast'] if c['name'] == who][0]; fa = dict((f['g'], f) for f in frames)
        s0 = anchor_frac(fa[g0], cast_pos(c, g0), HCAST[c['who']]); s1 = anchor_frac(fa[g1], cast_pos(c, g1), HCAST[c['who']])
        res['bigzoom'] = dict(start=s0[0] * 100, start_in=s0[1], end=s1[0] * 100, end_in=s1[1], ok=bool(s0[0] < 0.05 and s0[1] and 0.35 <= s1[0] <= 0.60 and s1[1]))
        if not quiet: print('BIGZOOM %s g %d -> %d: %s start %.1f %%H (%s), end %.1f %%H (%s) -> %s' % (take, g0, g1, who, s0[0] * 100, 'in' if s0[1] else 'OUT', s1[0] * 100, 'in' if s1[1] else 'OUT', 'PASS' if res['bigzoom']['ok'] else 'FAIL'))
    return res

# ================================================================ cast placeholder cards (stills / animatics): body + head + rim, turned to the camera
def _flat(key, hexc, s=1.0):
    if key in K._MATS: return K._MATS[key]
    m = bpy.data.materials.new(key); nt = K._mk_tree(m); e = nt.nodes.new('ShaderNodeEmission'); e.inputs[0].default_value = (*hex_lin(hexc), 1); e.inputs[1].default_value = s
    o = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(e.outputs[0], o.inputs[0]); K._MATS[key] = m; return m
def cast_cards(take, g, cam=None, rim=None):
    """placeholder cast cards at the take's anchors for frame g: a coloured body (coat / uniform colour of the cast member, kepi band), a near-white
    head disc with an ink ring, and a rim line in the location's rim colour (warm / cool). Rebuilt on every call (old cards are removed)."""
    for o in [o for o in bpy.data.objects if o.name.startswith('cc_')]: bpy.data.objects.remove(o, do_unlink=True)
    cam = cam or bpy.context.scene.camera; cl = cam.location; seg = 20; a = np.linspace(0, 2 * math.pi, seg, endpoint=False); out = []
    for c in TAKES[take]['cast']:
        x, y, z = cast_pos(c, g); who = c['who']; H = HCAST[who]; hd = (1.78 if not who.startswith('seated') else 1.6) * 0.17; hc = H - hd * 0.55; bw = 0.5 if who != 'inspector' and who != 'seated_insp' else 0.66
        if not who.startswith('seated') and z < FZ + 0.5: z = floor_z(x, y)                                   # feet on the surface (steps, sill, pavement)
        yc = yaw_clamp(cast_face(take, c, g), (x, y, z), cl); back = is_back(take, c['name'], g, yc)
        body, acc = CCOL[who]; rc = rim or K.LIGHTS[W['light'].get(_loc_of((x, y, z)), 'SUNSET_INT')]['rim']
        if back: body = '#15122a'
        V = []; F = []; M = []
        def poly(pts, mat):
            i0 = len(V); V.extend(pts); F.append(tuple(range(i0, i0 + len(pts)))); M.append(mat)
        poly([(-bw / 2 - 0.035, 0.004, -0.0), (bw / 2 + 0.035, 0.004, 0.0), (bw * 0.36 + 0.035, 0.004, H - hd * 0.95 + 0.03), (-bw * 0.36 - 0.035, 0.004, H - hd * 0.95 + 0.03)], 2)
        poly([(-bw / 2, 0, 0), (bw / 2, 0, 0), (bw * 0.36, 0, H - hd * 0.95), (-bw * 0.36, 0, H - hd * 0.95)], 0)
        poly([(-bw * 0.36, -0.002, H - hd * 1.25), (bw * 0.36, -0.002, H - hd * 1.25), (bw * 0.36, -0.002, H - hd * 0.95), (-bw * 0.36, -0.002, H - hd * 0.95)], 1)
        poly([(hd * 0.56 * math.cos(t_), 0.002, hc + hd * 0.56 * math.sin(t_)) for t_ in a], 3); poly([(hd * 0.5 * math.cos(t_), -0.004, hc + hd * 0.5 * math.sin(t_)) for t_ in a], 4)
        if who in ('inspector', 'gendarme', 'seated_insp'): poly([(-hd * 0.5, -0.006, hc + hd * 0.42), (hd * 0.5, -0.006, hc + hd * 0.42), (hd * 0.42, -0.006, hc + hd * 0.85), (-hd * 0.42, -0.006, hc + hd * 0.85)], 1)
        me = bpy.data.meshes.new('cc_' + c['name']); me.from_pydata(V, [], F); me.update()
        for m in (_flat('ccb_' + body, body), _flat('cca_' + who, acc), _flat('ccr_' + rc, rc, 1.2), _flat('cc_ink', '#1a1033'), _flat('cc_head' if not back else 'cc_hair', '#fef7f6' if not back else '#1c1424')): me.materials.append(m)
        me.polygons.foreach_set('material_index', M); ob = bpy.data.objects.new('cc_' + c['name'], me); bpy.context.scene.collection.objects.link(ob); ob.location = (x, y, z)
        ob.rotation_euler = (0, 0, math.radians(yc['face'] + (180.0 if back else 0.0)) + math.pi / 2); ob.visible_shadow = False; out.append(ob)        # yaw-clamped (front faces local -y)
        sh = bpy.data.meshes.new('cc_sh_' + c['name']); sh.from_pydata([(0.32 * math.cos(t_), 0.22 * math.sin(t_), 0.01) for t_ in a], [], [tuple(range(seg))]); sh.update(); sh.materials.append(_flat('cc_shadow', '#1a1440', 0.6))
        so = bpy.data.objects.new('cc_sh_' + c['name'], sh); bpy.context.scene.collection.objects.link(so); so.location = (x, y, z); so.visible_shadow = False
    return out
def _loc_of(p):
    x, y, z = p
    if 13.0 <= x <= 21.0 and 2.0 <= y <= 34.0: return 'archive'
    if 6.0 <= x <= 12.4 and 7.8 <= y <= 16.2: return 'measure'
    if 5.7 <= x <= 13.0 and 3.7 <= y <= 7.7 and z >= 0.5: return 'corridor'
    return 'ext'

# ================================================================ per-take hook states (doors, window, wagon, drawer, lid, card, calendar, tally, light mix)
def _ramp(g, a, b): return max(0.0, min(1.0, (g - a) / float(b - a)))
def _ss(u): return u * u * (3 - 2 * u)
def _light_scale(prefixes, k, frame=None):
    """scale the energy of the lights whose names start with one of `prefixes` relative to their built value (stored on first use)."""
    for o in bpy.data.objects:
        if o.type == 'LIGHT' and o.name.startswith(prefixes):
            if 'e_built' not in o: o['e_built'] = o.data.energy
            o.data.energy = o['e_built'] * k; W.setdefault('lampmul', {})[o.name] = k          # flickering lamps: set_flicker2 applies the same multiplier
            if frame is not None: o.data.keyframe_insert('energy', frame=frame)
def _glow_scale(key, k, frame=None):
    for m in bpy.data.materials:
        if m.name.startswith(key) and m.node_tree and 'strength' in m.node_tree.nodes:
            sk = m.node_tree.nodes['strength'].inputs[1]
            if 'e_built' not in m: m['e_built'] = sk.default_value
            sk.default_value = m['e_built'] * k
            if frame is not None: sk.keyframe_insert('default_value', frame=frame)
def take_state(take, g, frame=None):
    """every story hook of a take at frame g (planned timings, PLAN §4). frame=None sets; frame=N keys (render teams: frame = g + 1)."""
    if take == 'T1':
        set_window(1.0, frame); set_wagon(_ss(_ramp(g, 150, 230)), frame); set_door('main', _ss(_ramp(g, 300, 330)), frame)
        _light_scale(('win_key',), 1.0 - (1.0 - 220.0 / 300.0) * _ss(_ramp(g, 96, 110)), frame)          # QA v2b: window key 300 W (BIGZOOM start) -> 220 W inside
    elif take == 'T2':
        _light_scale(('door_lantern',), 0.8 + 0.2 * _ss(_ramp(g, 360, 372)), frame); _glow_scale('glow_fan', 0.8 + 0.2 * _ss(_ramp(g, 360, 372)), frame)   # QA v2b: -20 % g330-360
        set_door('main', 0.35 + 0.65 * _ss(_ramp(g, 330, 362)), frame); set_door('ident', _ss(_ramp(g, 440, 470)), frame); set_window(1.0, frame); set_door('archives', 0.0, frame)
    elif take in ('T3', 'T8'):
        set_window(1.0, frame); set_door('ident', 0.6 if take == 'T3' else 0.3, frame); set_calendar(_ss(_ramp(g, 758, 778)) if take == 'T3' else 1.0, frame)
    elif take == 'T4':
        set_window(1.0, frame); set_calendar(1.0, frame); set_door('archive', _ss(_ramp(g, 975, 1000)), frame); set_door('ident', 0.3, frame)
    if take in ('T5', 'T6', 'T7') and 'big' in K.STATE['anim']:
        if take == 'T5': K.set_drawer('big', 0.0, frame); set_tally(0, frame); K.set_cards_fan(1.0, frame)
        if take == 'T6':
            K.set_drawer('big', _ss(_ramp(g, 1378, 1392)), frame); K.set_box_lid('box', _ss(_ramp(g, 1484, 1500)), frame); K.set_card_lift(_ss(_ramp(g, 1490, 1520)), frame); set_tally(0, frame)
        if take == 'T7':
            K.set_drawer('big', 1.0, frame); K.set_box_lid('box', 1.0, frame); K.set_card_lift(1.0, frame); set_tally(241 * _ramp(g, 1800, 1866), frame)
    if take == 'T5':
        mx = TAKES['T5']['mix']; set_light_mix(mx[2], mx[3], _ss(_ramp(g, mx[0], mx[1])), frame)

def key_take(take, cam=None, g0=None, g1=None):
    """key a whole take for a frame-by-frame render (Blender frame = g + 1), in the right order per frame: camera path, story hooks
    (take_state: doors, window, calendar, drawer, tally, light mix, the QA v2b light schedules), ceiling cutaway, then the life hooks (flicker x
    the light-mix / schedule multipliers, smoke, dust, pendulum, banners). The cast is staged separately on every frame with stage_cast2."""
    cam = cam or bpy.context.scene.camera; fr = path_take(take); g0 = fr[0]['g'] if g0 is None else g0; g1 = fr[-1]['g'] if g1 is None else g1
    key_cam(cam, [f for f in fr if g0 <= f['g'] <= g1])
    for f in fr:
        g = f['g']
        if not g0 <= g <= g1: continue
        n = g + 1; take_state(take, g, frame=n); cutaway_at(f, frame=n); set_flicker2(1.0, frame=n); set_smoke2(1.0, frame=n); set_dust2(1.0, frame=n)
        K.set_pendulum(frame=n); set_banner_sway(frame=n)
# ================================================================ render (v2 settings + grade) and the gate stills
def setup_render2(res=(720, 1280), samples=32, threads=2, adaptive=0.03):
    """recommended v2 settings: Cycles CPU, 2 threads, 32 samples + OIDN, adaptive 0.03, 0 diffuse bounces (ambient is emission), no DOF."""
    sc = bpy.context.scene; r = sc.render; r.resolution_x, r.resolution_y = res; r.resolution_percentage = 100; r.threads_mode = 'FIXED'; r.threads = threads
    r.image_settings.file_format = 'PNG'; sc.cycles.samples = samples; sc.cycles.use_denoising = True; sc.cycles.denoiser = 'OPENIMAGEDENOISE'
    sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = adaptive; sc.cycles.diffuse_bounces = 0; sc.cycles.glossy_bounces = 2; sc.cycles.transparent_max_bounces = 12
    K.STATE['scale'] = res[0] / 720.0
def grade2(path, sat=1.20, vib=0.18, bloom=0.5):
    """v2 grade (PLAN §2): bertillon.grade's emitter bloom, saturation 1.20 (was 1.05), a vibrance lift on the 0.25-0.5 saturation band only."""
    K.grade(path, sat=1.0, bloom=bloom)
    im = np.asarray(Image.open(path).convert('RGB'), dtype=np.float32) / 255; mx = im.max(-1, keepdims=True); mn = im.min(-1, keepdims=True); s = (mx - mn) / (mx + 1e-4)
    band = np.clip(1 - np.abs(s - 0.375) / 0.2, 0, 1); k = sat * (1 + vib * band); im = np.clip(mx - (mx - im) * k, 0, 1)
    Image.fromarray((im * 255 + 0.5).astype(np.uint8)).save(path)
def render_frame(path, res=(360, 640), samples=16, threads=2, do_grade=True):
    setup_render2(res, samples, threads); sc = bpy.context.scene; sc.render.filepath = path; t = time.time(); bpy.ops.render.render(write_still=True); dt = time.time() - t
    if do_grade: grade2(path)
    return dt
CEIL_Z = {'measure': FZ + K.MH - 0.15, 'archive': VCZ + VR - 0.2}
def cutaway_at(fr, frame=None):
    """hide the cut-away ceilings of the take (TAKE_CUTAWAY) only while the camera is above them (bird's-eye / top-down frames); keyed with frame."""
    for nm in W.get('cut', ()):
        hide = fr['loc'][2] > CEIL_Z[nm]
        for o in W.get('ceil_' + nm, []):
            o.visible_camera = not hide
            if frame is not None: o.keyframe_insert('visible_camera', frame=frame)
def shot(take, g, A=None, cards=True):
    """put the world in its state for frame g of a take: camera on the path, hooks, life, cast cards."""
    t = TAKES[take]; frames = dict((f['g'], f) for f in path_take(take)); g = max(t['render'][0], min(t['render'][1], g)); cam = bpy.context.scene.camera
    bpy.context.scene.frame_set(g + 1); set_cam(cam, frames[g]); take_state(take, g); cutaway_at(frames[g]); life_at(g); bpy.context.view_layer.update()
    if cards: cast_cards(take, g, cam)
    return frames[g]
def gate_stills(take, out_dir, res=(360, 640), samples=16, which=None):
    """3 stills per take (start, middle, end of its camera path) -> out_dir/<take>_g<g>.png (+ .json with build / render seconds and the %H)."""
    os.makedirs(out_dir, exist_ok=True); t = TAKES[take]; A = world_build(take); g0, g1 = t['render']; gs = which or [g0, (g0 + g1) // 2, g1]; res_ = []
    if take in BIGZOOM: gs = which or [BIGZOOM[take][0], (g0 + g1) // 2 if take != 'T1' else 170, BIGZOOM[take][1]]
    for g in gs:
        fr = shot(take, g, A); p = os.path.join(out_dir, '%s_g%04d.png' % (take, g)); dt = render_frame(p, res, samples)
        sizes = {c['name']: round(anchor_frac(fr, cast_pos(c, g), HCAST[c['who']])[0] * 100, 1) for c in t['cast']}
        info = dict(take=take, g=g, build_s=round(A['build_s'], 1), render_s=round(dt, 1), res=res, samples=samples, tris=int(sum(len(o.data.polygons) for o in bpy.data.objects if o.type == 'MESH')), size_pct=sizes)
        json.dump(info, open(p[:-4] + '.json', 'w')); res_.append(info); print('%s g%d %.1fs (build %.1fs) %s' % (take, g, dt, A['build_s'], info['tris']), flush=True)
    return res_

# ================================================================ QA: per-frame anchor + speed check (SET gate v2b)
PLANNED_CLOSE = {   # (take, anchor) -> [(g0, g1)] where > 75 %H is planned: OTS shoulders (back-view cards) and the punctuation pushes P1-P3
    ('T2', 'bertillon'): [(530, 657)], ('T2', 'prisoner_chair'): [(600, 657)], ('T5', 'bertillon'): [(1100, 1150)], ('T6', 'bertillon'): [(1516, 1545)], ('T6', 'dupont'): [(1516, 1545), (1546, 1616)],
    ('T6', 'inspector'): [(1672, 1701)], ('T8', 'gend_a'): [(1958, 2052)], ('T8', 'bertillon'): [(2018, 2052)], ('T8', 'inspector'): [(2018, 2052)]}
WHIPS = {}          # take -> [(g0, g1)] planned whips (<= 3 frames)
def check_take(take, limit=0.75, vmax=6.0):
    """every frame of the take: anchors in frame above `limit` of the frame height (outside PLANNED_CLOSE), anchors closer than 1.0 m to the lens
    (pass-through) and camera speed above vmax m/s (outside BIGZOOM / planned whips). Returns dict(hits, near, fast, max_speed)."""
    t = TAKES[take]; fr = path_take(take); hits, near, fast = [], [], []; vm = 0.0
    bz = BIGZOOM.get(take)
    for i, f in enumerate(fr):
        g = f['g']; sp = (Vector(fr[min(i + 1, len(fr) - 1)]['loc']) - Vector(fr[max(i - 1, 0)]['loc'])).length * 15.0
        inbz = bz and bz[0] <= g <= bz[1]; vm = max(vm, sp if not inbz else 0)
        if sp > vmax and not inbz and not any(a <= g <= b for a, b in WHIPS.get(take, [])): fast.append((g, round(sp, 1)))
        for c in t['cast']:
            p = cast_pos(c, g); fH, inn, d = anchor_frac(f, p, HCAST[c['who']])
            ok = any(a <= g <= b for a, b in PLANNED_CLOSE.get((take, c['name']), []))
            if inn and fH > limit and not ok: hits.append((g, c['name'], round(fH * 100)))
            cen = Vector((p[0], p[1], p[2] + HCAST[c['who']] / 2)); dl = (cen - Vector(f['loc'])).length
            if dl < 1.0 and not ok: near.append((g, c['name'], round(dl, 2)))
    return dict(hits=hits, near=near, fast=fast, max_speed=vm)
def _runs(lst):
    """compress [(g, name, v)] into 'name g0-g1 (max v)' runs."""
    out = {}
    for g, n, v in lst: out.setdefault(n, []).append((g, v))
    s = []
    for n, gv in out.items():
        a = gv[0][0]; b = a; m = gv[0][1]
        for g, v in gv[1:]:
            if g == b + 1: b = g; m = max(m, v)
            else: s.append('%s g%d-%d (%s)' % (n, a, b, m)); a = b = g; m = v
        s.append('%s g%d-%d (%s)' % (n, a, b, m))
    return s

# ================================================================ stage_cast v2 (PLAN §3e / §6.1-2): yaw clamp, floor contact on steps, walk paths, back views
BACK_VIEW = {   # (take, anchor) -> [(g0, g1)]: the anchor is an over-the-shoulder foreground figure seen from behind (or walks away: T2 2a thief)
    ('T2', 'thief'): [(330, 386)], ('T2', 'bertillon'): [(530, 657)],
    ('T1', 'bertillon'): [(60, 96), (158, 186)], ('T1', 'prisoner_a'): [(60, 96), (158, 186)], ('T1', 'prisoner_b'): [(60, 96), (158, 186)], ('T1', 'prisoner_q'): [(60, 96), (158, 186)], ('T5', 'bertillon'): [(1100, 1150)], ('T6', 'dupont'): [(1546, 1616)], ('T8', 'gend_a'): [(1958, 2052)]}
YAW_CLAMP = 35.0
def floor_z(x, y):
    """walkable surface height at (x, y): street 0, pavements 0.14, the façade's 3 outside steps (to the 0.6 sill), the 5 corridor steps (to 1.2),
    interiors FZ. Cast feet and contact shadows use it, so nobody floats over or sinks into a step."""
    fx = FACADE_X
    if CX0 <= x <= CX1 and CY0 - 0.3 <= y <= CY1 + 0.3:
        return FZ if x >= 6.95 else 0.6 + 0.12 * min(5, int((x - CX0) / 0.24) + 1)
    if fx <= x < CX0 and abs(y - 5.7) <= 1.1: return 0.6                                              # the door sill
    if (6.0 <= x <= 12.4 and 7.8 <= y <= 16.2) or (13.0 <= x <= 21.0 and 2.0 <= y <= 34.0): return FZ
    if fx - 1.08 <= x <= fx and abs(y - 5.7) <= 2.0: return 0.14 + 0.155 * (3 - min(2, int((fx - x) / 0.36)))
    if 4.0 <= abs(x) <= 6.0: return 0.14
    return 0.0
def _wrap(a): return (a + 180.0) % 360.0 - 180.0
def yaw_clamp(face_deg, pos, cam_loc, max_dev=YAW_CLAMP, back_at=110.0):
    """card yaw for an orbiting camera: the card turns toward the camera but never more than max_dev (35 deg) from its story facing face_deg
    (azimuth, deg, of the direction the figure faces). Returns dict(face: clamped facing azimuth, dev: camera angle off the story facing,
    pose_yaw: puppet 'yaw' key (-0.6..0.6) carrying the rest of the turn, back: True when the camera is behind (|dev| > back_at -> back view),
    yaw_fixed: the value for stage.actors.Actor.yaw_fixed (card yaw 0 = parallel to the y = 0 wall, facing -y => yaw_fixed = face - (-90)))."""
    az = math.degrees(math.atan2(cam_loc[1] - pos[1], cam_loc[0] - pos[0])); dev = _wrap(az - face_deg); c = max(-max_dev, min(max_dev, dev))
    rest = dev - c; py = max(-0.6, min(0.6, rest / 90.0 * 0.6)); f = face_deg + c
    return dict(face=f, dev=dev, pose_yaw=py, back=abs(dev) > back_at, yaw_fixed=_wrap(f + 90.0))
def walk_path(keys, stride=0.72, g0=None, g1=None):
    """foot-locked walk along keys [(g, (x, y)) ...] (linear in time between keys). Per frame: pos (x, y, floor_z), heading (deg azimuth of travel),
    speed (m/s), phase = distance / (2 x stride) mod 1 (feed cast17.cycle(cast, phase, 'walk')): the gait advances with the distance actually
    walked, so the planted foot does not skate; planted = 'L' for phase < 0.5 else 'R'; idle when speed < 0.05 (phase holds)."""
    g0 = keys[0][0] if g0 is None else g0; g1 = keys[-1][0] if g1 is None else g1; out = []; dist = 0.0; prev = None; head = 0.0
    for g in range(int(g0), int(g1) + 1):
        p = cast_pos(dict(path=[(k[0], (k[1][0], k[1][1], 0.0)) for k in keys]), g); x, y = p[0], p[1]
        sp = 0.0
        if prev is not None:
            dx, dy = x - prev[0], y - prev[1]; st = math.hypot(dx, dy); dist += st; sp = st * 30.0
            if st > 1e-5: head = math.degrees(math.atan2(dy, dx))
        ph = (dist / (2 * stride)) % 1.0; out.append(dict(g=g, pos=(x, y, floor_z(x, y)), heading=head, speed=sp, phase=ph, planted='L' if ph < 0.5 else 'R', idle=sp < 0.05)); prev = (x, y)
    return out
def cast_face(take, c, g):
    """story facing of a cast anchor at g: its per-segment face keys (FACE / face_keys, B7), else an explicit constant `face`, else its walking
    direction, else toward the take's start camera."""
    fk = face_keys(take).get(c['name'])
    if fk: return _face_at(fk, g)
    if c.get('face') is not None: return c['face']
    p0 = cast_pos(c, g - 1); p1 = cast_pos(c, g + 1)
    if math.hypot(p1[0] - p0[0], p1[1] - p0[1]) > 0.01: return math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
    k0 = path_take(take)[0]['loc']; p = cast_pos(c, g); return math.degrees(math.atan2(k0[1] - p[1], k0[0] - p[0]))
def is_back(take, name, g, clamp=None):
    if any(a <= g <= b for a, b in BACK_VIEW.get((take, name), [])): return True
    return bool(clamp and clamp['back'])
# ---------------------------------------------------------------- B7: per-segment face keys + check_face
STRICT = {   # (take) -> [(g0, g1, anchor)]: the speaker / hero must read front-on (<= 35 deg, the card clamp): lip-sync, BIGZOOM ends, P1-P3, 6c MARTIN
    # T1 from g97: at g90-96 the camera is still in the window, behind him (BACK_VIEW)
    'T1': [(97, 148, 'bertillon')], 'T2': [(493, 651, 'inspector')], 'T5': [(1128, 1196, 'inspector')],
    'T6': [(1500, 1530, 'bertillon'), (1515, 1545, 'bertillon'), (1545, 1616, 'bertillon'), (1671, 1695, 'inspector')], 'T8': [(2018, 2052, 'inspector')]}
FACE_OVERRIDE = {   # (take, anchor) -> [(g, deg)]: hand keys that replace the generated ones
    # T1 hook: Bertillon and the bench prisoners face into the room (PLAN / QA B7 example); the camera flies in behind them (BACK_VIEW g60-96)
    ('T1', 'bertillon'): [(0, -25.0), (342, -25.0)], ('T1', 'prisoner_a'): [(0, -15.0), (342, -15.0)], ('T1', 'prisoner_b'): [(0, -15.0), (342, -15.0)],
    ('T1', 'prisoner_q'): [(0, -15.0), (342, -15.0)]}
_FACES = {}
def _face_at(keys, g):
    if g <= keys[0][0]: return keys[0][1]
    if g >= keys[-1][0]: return keys[-1][1]
    for (ga, a), (gb, b) in zip(keys[:-1], keys[1:]):
        if ga <= g <= gb: u = (g - ga) / float(gb - ga); return a + _wrap(b - a) * u
def face_keys(take):
    """per-segment story facings (B7) for every anchor of a take: [(g, deg azimuth)], linear between keys. Generated once from the planned camera
    path: each key is the weighted circular mean of the direction to the camera over its segment (weight 1 where the card is in frame above 15 %H,
    0.05 elsewhere), keys every 20 frames, every 8 frames for the hero inside STRICT windows. FACE_OVERRIDE replaces them by hand. Written to
    v2_gate/face_keys.json by `write_face_keys()` for the render teams."""
    if take in _FACES: return _FACES[take]
    t = TAKES[take]; fr = path_take(take); g0, g1 = fr[0]['g'], fr[-1]['g']; out = {}
    for c in t['cast']:
        if (take, c['name']) in FACE_OVERRIDE: out[c['name']] = FACE_OVERRIDE[(take, c['name'])]; continue
        az = []; w = []
        for f in fr:
            p = cast_pos(c, f['g']); a = math.atan2(f['loc'][1] - p[1], f['loc'][0] - p[0]); v, inn, d = anchor_frac(f, p, HCAST[c['who']])
            az.append(a); w.append(1.0 if (inn and v > 0.15) else 0.05)
        strict = [(a, b) for (a, b, n) in STRICT.get(take, []) if n == c['name']]
        ks = []; g = g0
        while g <= g1:
            st = 8 if any(a - 8 <= g <= b + 8 for a, b in strict) else 20
            lo, hi = max(g0, g - st // 2), min(g1, g + st // 2); i0, i1 = lo - g0, hi - g0 + 1
            sx = sum(w[i] * math.cos(az[i]) for i in range(i0, i1)); sy = sum(w[i] * math.sin(az[i]) for i in range(i0, i1))
            ks.append((g, math.degrees(math.atan2(sy, sx)))); g += st
        if ks[-1][0] != g1: ks.append((g1, ks[-1][1]))
        un = [ks[0]]
        for (g, a) in ks[1:]: un.append((g, un[-1][1] + _wrap(a - un[-1][1])))                     # unwrapped, no 360 spins
        out[c['name']] = [(g, round(a, 1)) for g, a in un]
    _FACES[take] = out; return out
def write_face_keys(path=None):
    path = path or os.path.join(HERE, 'v2_gate', 'face_keys.json'); json.dump({t: face_keys(t) for t in TAKES}, open(path, 'w'), indent=0); return path
def check_face(take):
    """B7: per anchor, the facing error |story face - direction to the camera| on every frame where the card is in frame above 15 %H and not on
    BACK_VIEW. FAIL when > 60 deg anywhere, or > 35 deg on the STRICT windows (lip-sync, BIGZOOM ends, P1-P3, 6c). Also the card yaw rate
    (deg/frame) on those frames (PLAN §6.1: <= 2). Returns dict(rows: {anchor: (max_dev, max_strict, n_fail, max_rate)}, ok)."""
    t = TAKES[take]; fr = path_take(take); rows = {}; ok = True
    for c in t['cast']:
        md = ms = rate = 0.0; nf = 0; prev = None
        strict = [(a, b) for (a, b, n) in STRICT.get(take, []) if n == c['name']]
        for f in fr:
            g = f['g']; p = cast_pos(c, g); v, inn, d = anchor_frac(f, p, HCAST[c['who']]); fc = cast_face(take, c, g)
            if not (inn and v > 0.15) or is_back(take, c['name'], g): prev = None; continue
            az = math.degrees(math.atan2(f['loc'][1] - p[1], f['loc'][0] - p[0])); dev = abs(_wrap(az - fc)); st = any(a <= g <= b for a, b in strict)
            md = max(md, dev)
            if st: ms = max(ms, dev)
            if dev > 60 or (st and dev > 35): nf += 1
            yc = yaw_clamp(fc, p, f['loc'])['face']
            if prev is not None: rate = max(rate, abs(_wrap(yc - prev)))
            prev = yc
        rows[c['name']] = (md, ms, nf, rate); ok = ok and nf == 0
    return dict(rows=rows, ok=ok)

# ---------------------------------------------------------------- stage_cast2: the real cast17 cards on a take frame
def stage_cast2(take, g, assign, cam=None, sprite_dir=None, px_per_D=256):
    """the REAL cast17 cards for frame g of a take (render teams: call it on every frame before rendering; it poses at the scene's current
    frame). assign = {anchor: (story_pose, opts)}; opts: mirror, seated ('chair' | 'bench'), H, dx/dy/dz, expr, talk (True: cast17.speak drives
    the mouth: lip-sync windows only), rim (default: the location preset's RIM). Adds to bertillon.stage_cast: feet on floor_z, the B7 face keys,
    the +-35 deg yaw clamp (Actor.yaw_fixed) with the rest of the turn in the puppet 'yaw' key, and back views on BACK_VIEW frames (cast17 has no
    back art: the pose is mirrored and a dark back-of-head disc + coat silhouette cover the card). Returns {anchor: Actor}."""
    for pth in (os.path.join(K.V3, 'cast17'), os.path.join(K.V3, 'stage')):
        if pth not in sys.path: sys.path.insert(0, pth)
    import cast17, actors, sprites
    # leak fix (found by render team T3): drop the previous frame's cast actors before building new ones
    for o in [o for o in bpy.data.objects if o.name.startswith(('c2_', 'back_hair_', 'back_coat_'))]: bpy.data.objects.remove(o, do_unlink=True)
    actors.clear_registry()
    sc = bpy.context.scene; cam = cam or sc.camera; cl = cam.location; fnum = sc.frame_current; t = TAKES[take]; out = {}
    sprite_dir = sprite_dir or os.path.join(HERE, 'contact_work', 'sprites_v2'); os.makedirs(sprite_dir, exist_ok=True); bpy.context.view_layer.update()
    for c in t['cast']:
        if c['name'] not in assign: continue
        story, opts = assign[c['name']]; opts = dict(opts or {}); cast, pose = cast17.STORY17[story]; pose = dict(pose)
        if opts.get('expr'): pose = cast17.with_expr(pose, opts['expr'])
        if opts.get('talk'): pose = cast17.speak(pose, g)
        p = cast_pos(c, g); seated = opts.get('seated') or ('chair' if pose.get('seat17') == 'chair' else 'bench' if pose.get('seat17') == 'bench' else None); pose['seat17'] = None
        yc = yaw_clamp(cast_face(take, c, g), p, cl); back = is_back(take, c['name'], g, yc)
        if back: opts['mirror'] = not opts.get('mirror', False)
        if opts.get('mirror'): pose['mirror'] = True
        pose['yaw'] = max(-0.6, min(0.6, pose.get('yaw', 0.0) + (yc['pose_yaw'] if not back else 0.0)))
        rim = opts.get('rim', RIM.get(W['light'].get(_loc_of(p), 'SUNSET_INT'), '#ffb85a'))
        if rim: pose['rim'] = rim; pose['rim_opacity'] = 0.55; pose['rim_w'] = 0.02
        a = actors.Actor('c2_' + c['name'], cast); a.build(sprites.DEFAULT_CANVAS[cast], sprite_dir, contact=True); a.head_flip = True; a.yaw_fixed = yc['yaw_fixed']
        scl = opts.get('H', K.CAST_H[cast]) / K.CAST_HD[cast]
        if seated: fx, fy = sprites.feet_of(cast, pose); zz = (p[2] - 0.0 if p[2] >= FZ - 0.01 else 0.0) + (K.HEAD_Z[seated] if p[2] < FZ - 0.01 else K.HEAD_Z[seated]) - scl * fy if False else (FZ if _loc_of(p) != 'ext' else 0.0) + K.HEAD_Z[seated] - scl * fy
        else: zz = floor_z(p[0], p[1]) if p[2] < FZ + 0.5 else p[2]
        a.place(fnum, (p[0] + opts.get('dx', 0.0), p[1] + opts.get('dy', 0.0), zz + opts.get('dz', 0.0)), scale=scl); a.pose(fnum, pose, camera=cam)
        a.render_sprites(px_per_D, frames=[fnum]); out[c['name']] = a; c['_back'] = back
    actors.sync_all(sc, cam)
    for nm, a in out.items():
        c = [c for c in t['cast'] if c['name'] == nm][0]
        if c['_back']: _back_cover(a, c, cam)
    return out
def _back_cover(a, c, cam):
    """back view on a cast17 card (no back art): a dark back-of-head disc over the head (radius 0.56 D, from the card's own head anchor) and a dark
    coat panel over the torso (0.5-2.0 D below the head centre), both on the card plane, 3 cm toward the camera."""
    import actors
    L2W = lambda xy: Vector(actors.local_to_world(a, xy, camera=cam)); o = L2W((0.0, 0.0)); ex = L2W((1.0, 0.0)) - o; ey = L2W((0.0, 1.0)) - o   # ey points down the card
    to = (Vector(cam.location) - o).normalized() * 0.03; n = 28; V = [tuple(o + to)] + [tuple(o + to + ex * 0.56 * math.cos(2 * math.pi * k / n) + ey * 0.56 * math.sin(2 * math.pi * k / n)) for k in range(n)]
    me = bpy.data.meshes.new('back_hair_' + c['name']); me.from_pydata(V, [], [(0, 1 + k, 1 + (k + 1) % n) for k in range(n)]); me.update(); me.materials.append(_flat('cc_back_hair', '#1c1424'))
    ob = bpy.data.objects.new(me.name, me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = False
    T = [tuple(o + to * 0.9 + ex * x + ey * y) for (x, y) in ((-0.64, 0.5), (0.64, 0.5), (0.7, 2.0), (-0.7, 2.0))]
    me2 = bpy.data.meshes.new('back_coat_' + c['name']); me2.from_pydata(T, [], [(0, 1, 2, 3)]); me2.update(); me2.materials.append(_flat('cc_back_coat', '#17142e'))
    ob2 = bpy.data.objects.new(me2.name, me2); bpy.context.scene.collection.objects.link(ob2); ob2.visible_shadow = False
REAL_STILLS = {   # B7.3: real-cast key stills (take, g) -> assign
    ('T1', 105): {'bertillon': ('bertillon_measuring', {'mirror': True}), 'prisoner_a': ('prisoner_sitting_a', {'seated': 'bench'}), 'prisoner_b': ('prisoner_sitting_b', {'seated': 'bench'}),
                  'prisoner_q': ('prisoner_sitting_c', {'seated': 'bench'}), 'gend_room': ('gendarme_standing_a', {})},
    ('T2', 560): {'inspector': ('inspector_pointing_mock', {'talk': True}), 'bertillon': ('bertillon_measuring', {'mirror': True}), 'prisoner_chair': ('prisoner_sitting_b', {'seated': 'chair'}),
                  'gend_room': ('gendarme_laughing_a', {}), 'gend_room2': ('gendarme_laughing_b', {}), 'prisoner_b': ('prisoner_sitting_a', {'seated': 'bench'})},
    ('T6', 1600): {'bertillon': ('bertillon_holding_card', {}), 'dupont': ('dupont_sweating', {}), 'inspector': ('inspector_arms_crossed', {}), 'gend_a': ('gendarme_standing_a', {}), 'gend_b': ('gendarme_standing_b', {})},
    ('T6', 1690): {'inspector': ('inspector_shocked', {}), 'bertillon': ('bertillon_holding_card', {}), 'dupont': ('dupont_caught', {}), 'gend_b': ('gendarme_standing_b', {})}}
def real_still(take, g, out, res=(720, 1280), samples=16):
    """full-res still with the REAL cast17 cards through stage_cast2 (B7.3)."""
    A = world_build(take); shot(take, g, A, cards=False); acts = stage_cast2(take, g, REAL_STILLS[(take, g)]); dt = render_frame(out, res, samples)
    return dt, acts

if __name__ == '__main__':
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    if a and a[0] == 'stills': gate_stills(a[1], a[2], res=(int(a[3]), int(a[4])) if len(a) > 4 else (360, 640), samples=int(a[5]) if len(a) > 5 else 16, which=[int(x) for x in a[6].split(',')] if len(a) > 6 else None)
    elif a and a[0] == 'real':       # real <take> <g> <out.png>  (B7.3)
        dt, acts = real_still(a[1], int(a[2]), a[3]); print('real %s g%s %.1fs %s' % (a[1], a[2], dt, sorted(acts)))
    elif a and a[0] == 'faces':
        for tk in (a[1:] or list(TAKES)):
            r = check_face(tk); print('%s %s ' % (tk, 'PASS' if r['ok'] else 'FAIL') + '  '.join('%s %.0f/%.0f%s r%.1f' % (n, v[0], v[1], (' FAIL%d' % v[2]) if v[2] else '', v[3]) for n, v in r['rows'].items()))
    elif a and a[0] == 'report':
        for tk in (a[1:] or list(TAKES)): print('== ' + tk); cam_report(tk, step=int(os.environ.get('STEP', 12)))
    elif a and a[0] == 'frame':      # frame <take> <g> <out.png> [W H samples threads]
        A = world_build(a[1]); shot(a[1], int(a[2]), A); W_, H_ = (int(a[4]), int(a[5])) if len(a) > 5 else (720, 1280)
        dt = render_frame(a[3], (W_, H_), int(a[6]) if len(a) > 6 else 32, int(a[7]) if len(a) > 7 else 2); print('frame %s g%s %.1fs build %.1fs tris %d' % (a[1], a[2], dt, A['build_s'], sum(len(o.data.polygons) for o in bpy.data.objects if o.type == 'MESH')))
    else: print('usage: python3 prefecture17.py stills <T1..T8> <out_dir> [W H samples g,g,g] | report [T..] | frame <take> <g> <out.png> [W H samples threads]')

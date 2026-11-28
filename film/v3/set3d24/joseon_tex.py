#!/usr/bin/env python3
"""joseon_tex.py : artwork of the film-24 set (Joseon naval yard + Hansan waters, 1592). numpy + PIL, deterministic, cached in tex_joseon/.
   tx = JX.ensure()  ->  {name: png path}.  Bump TEX_V after editing a painter.  NO text anywhere."""
import os, sys, json, math, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (os.path.join(PROJ, 'v3', 'set3d9'), os.path.join(PROJ, 'v3', 'set3d8'), os.path.join(PROJ, 'v3', 'set3d10')):
    if p not in sys.path: sys.path.insert(0, p)
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
TEX = os.path.join(HERE, 'tex_joseon'); TEX_V = 'j24.6'

def hexc(h):
    h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], 'float32') / 255
def save(a, out, alpha=None):
    a = np.clip(a, 0, 1)
    if alpha is not None: a = np.concatenate([a, np.clip(alpha, 0, 1)[..., None]], -1); mode = 'RGBA'
    else: mode = 'RGB'
    Image.fromarray((a * 255 + 0.5).astype('uint8'), mode).save(out)
def noise(rs, H, W, cx, cy):
    g = rs.rand(cy + 1, cx + 1).astype('float32'); im = Image.fromarray((g * 255).astype('uint8')).resize((W, H), Image.BICUBIC)
    return np.asarray(im, 'float32') / 255
def fbm(rs, H, W, cx, cy, o=4):
    t = 0; a = 1; s = 0
    for i in range(o): t = t + a * noise(rs, H, W, cx * 2 ** i, cy * 2 ** i); s += a; a *= 0.5
    return t / s

def hexplates(p, out):
    """Hexagonal roof plates of the turtle ship: dark green-teal plates with warm wood-tone seams; alpha-free colour + the same image is the bump."""
    W, H = 512, 443; rs = np.random.RandomState(p['seed']); yy, xx = np.mgrid[0:H, 0:W].astype('float32')
    px, py = 64.0, 110.851; cs = []
    for j in range(-1, 6):
        for i in range(-1, 10):
            cs.append((i * px, j * py)); cs.append((i * px + px / 2, j * py + py / 2))
    d1 = np.full((H, W), 1e9, 'float32'); d2 = d1.copy(); idx = np.zeros((H, W), 'int32')
    for k, (cx, cy) in enumerate(cs):
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2); m = d < d1; d2 = np.where(m, d1, np.minimum(d2, d)); idx = np.where(m, k, idx); d1 = np.where(m, d, d1)
    ids = np.array([(c[0] % 512) * 7 + (c[1] % 443) * 13 for c in cs]); cols = np.stack([hexc(c) for c in p['cols']])
    ch = (np.abs(np.sin(ids * 1.7)) * len(cols)).astype(int) % len(cols)
    base = cols[ch[idx]] * (0.9 + 0.2 * fbm(rs, H, W, 8, 8)[..., None])
    edge = np.clip((d2 - d1 - 2.0) / 5.0, 0, 1)                         # 0 at the seam
    dome = np.clip(1.0 - (d1 / 38.0) ** 3, 0, 1)                         # plate boss: lighter toward the middle
    col = base * (0.85 + 0.25 * dome[..., None]); col = col * edge[..., None] + hexc(p['seam']) * (1 - edge[..., None])
    save(col, out)

def tiles(p, out):
    """Grey Korean roof tiles: rows of overlapping curved pan tiles with dark seams (any direction)."""
    S = 512; rs = np.random.RandomState(p['seed']); yy, xx = np.mgrid[0:S, 0:S].astype('float32'); cw = 32; rh = 64
    u = (xx % cw) / cw; v = (yy % rh) / rh; ci = (xx // cw).astype(int); ri = (yy // rh).astype(int)
    ar = rs.rand(S // rh + 1, S // cw + 1).astype('float32'); tone = 0.82 + 0.3 * ar[ri, ci]
    shade = 0.75 + 0.25 * np.sin(u * math.pi) ** 0.8; ov = 0.78 + 0.22 * np.clip(v * 1.4, 0, 1)
    col = hexc(p['col']) * (tone * shade * ov)[..., None] * (0.92 + 0.16 * fbm(rs, S, S, 16, 16)[..., None])
    col = np.where(((u < 0.06) | (u > 0.94))[..., None], col * 0.55, col); col = np.where((v < 0.045)[..., None], col * 0.5, col)
    save(col, out)

def stone(p, out):
    """Ashlar blocks (varied widths per course), pale grey-brown with mortar gaps."""
    S = 512; rs = np.random.RandomState(p['seed']); col = np.zeros((S, S, 3), 'float32'); base = hexc(p['col']); n = fbm(rs, S, S, 20, 20)
    ch = p.get('ch', 48); y = 0; mort = np.ones((S, S), 'float32'); tone = np.ones((S, S), 'float32')
    while y < S:
        h = min(ch, S - y); x = 0
        while x < S:
            w = int(rs.choice([64, 96, 128, 160])); w = min(w, S - x)
            if S - x - w < 32: w = S - x
            tone[y:y + h, x:x + w] = 0.8 + 0.35 * rs.rand(); mort[y:y + h, x:x + 2] = 0.45; x += w
        mort[y:y + 2, :] = 0.45; y += h
    col = base * (tone * (0.82 + 0.3 * n) * mort)[..., None]; save(col, out)

def matting(p, out):
    """Woven rush matting for sails / baskets: warm beige weave + dark bamboo battens every 64 px."""
    S = 512; rs = np.random.RandomState(p['seed']); yy, xx = np.mgrid[0:S, 0:S].astype('float32')
    wv = 0.5 + 0.5 * np.sin(xx * 2 * math.pi / 8) * np.sin(yy * 2 * math.pi / 8); n = fbm(rs, S, S, 24, 24)
    col = hexc(p['col']) * (0.78 + 0.22 * wv[..., None]) * (0.85 + 0.3 * n[..., None]); b = (yy % 64)
    col = np.where((b < 5)[..., None], hexc(p['bat']), col); col = np.where(((b >= 5) & (b < 8))[..., None], col * 0.8, col); save(col, out)

def dancheong(p, out):
    """Dancheong beam paint (no text): red field, green + blue bands, white dot rows and lotus-like diamonds."""
    W, H = 512, 128; im = Image.new('RGB', (W, H), '#b3262a'); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 18], fill='#1f8c6a'); d.rectangle([0, 18, W, 30], fill='#f0e4c0'); d.rectangle([0, 30, W, 46], fill='#2a56a8')
    d.rectangle([0, H - 18, W, H], fill='#1f8c6a'); d.rectangle([0, H - 30, W, H - 18], fill='#f0e4c0'); d.rectangle([0, H - 46, W, H - 30], fill='#2a56a8')
    for i in range(0, W, 64):
        c = (i + 32, H // 2); d.polygon([(c[0], c[1] - 24), (c[0] + 24, c[1]), (c[0], c[1] + 24), (c[0] - 24, c[1])], fill='#2a56a8')
        d.polygon([(c[0], c[1] - 14), (c[0] + 14, c[1]), (c[0], c[1] + 14), (c[0] - 14, c[1])], fill='#f4d65a'); d.ellipse([c[0] - 5, c[1] - 5, c[0] + 5, c[1] + 5], fill='#b3262a')
        for k in (-1, 1): d.ellipse([i + 32 + k * 30 - 4, c[1] - 4, i + 32 + k * 30 + 4, c[1] + 4], fill='#f0e4c0')
    im.save(out)

def flag(p, out):
    """Plain flags / banners, no text. kind: red | black | white_r | white_k | tri_* | nob_circle / nob_diamond / nob_rcircle (cream nobori with a plain mon shape) | sail (cloth seams)."""
    k = p['kind']; W, H = (96, 320) if (k.startswith('white') or k.startswith('nob')) else (256, 160) if k != 'sail' else (256, 256)
    cols = dict(red='#c4202a', black='#1c1a1c', white_r='#f4f0e4', white_k='#f4f0e4', tri_red='#c4202a', tri_black='#201e22', tri_blue='#2850a0', tri_yellow='#e0b030', nob_circle='#efe6d0', nob_diamond='#efe6d0', nob_rcircle='#efe6d0', sail='#ebe2cc')
    im = Image.new('RGBA', (W, H), cols[k] + 'ff'); d = ImageDraw.Draw(im)
    if k == 'white_r': d.rectangle([0, 0, W, 26], fill='#c4202a'); d.rectangle([0, H - 40, W, H - 14], fill='#c4202a'); d.rectangle([0, 0, 6, H], fill='#2a2a2e')
    if k == 'white_k': d.rectangle([0, 0, W, 20], fill='#1c1a1c'); d.rectangle([0, H - 20, W, H], fill='#1c1a1c'); d.rectangle([W - 8, 0, W, H], fill='#c4202a')
    if k.startswith('nob'):
        d.rectangle([0, 0, 7, H], fill='#2a2420'); d.rectangle([W - 5, 0, W, H], fill='#2a2420'); cx, cy = W // 2, 118
        if k == 'nob_circle': d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill='#1c1a1c')
        elif k == 'nob_rcircle': d.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill='#b4222a')
        else: d.polygon([(cx, cy - 36), (cx + 30, cy), (cx, cy + 36), (cx - 30, cy)], fill='#b4222a')
    if k.startswith('tri'):
        im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.polygon([(0, 0), (W, H // 2), (0, H)], fill=cols[k]); d.rectangle([0, 0, 8, H], fill='#e8dcc0')
    if k in ('red', 'black'): d.rectangle([0, 0, 10, H], fill='#e8dcc0'); d.rectangle([0, H - 12, W, H], fill='#e8dcc0' if k == 'black' else '#f0c040')
    if k == 'sail':
        for x in range(0, W, 32): d.line([(x, 0), (x, H)], fill='#b9ad90', width=2)
        for y in (0, H // 3, 2 * H // 3): d.line([(0, y), (W, y)], fill='#a69a7e', width=3)
    im.save(out)

def foam(p, out):
    """Lace foam alpha: wake (long band), bow (crest), ring (blade splash), surf (thin lines for the beach). Hard-edged cartoon lace."""
    import harbour_tex as HX
    if p['kind'] in ('wake', 'bow'): HX.foam(dict(kind=p['kind'], w=p['w'], h=p['h'], seed=p['seed'], cx=p.get('cx', 16), cy=p.get('cy', 4)), out); return
    W, H = p['w'], p['h']; rs = np.random.RandomState(p['seed']); yy, xx = np.mgrid[0:H, 0:W].astype('float32'); u = xx / W; v = yy / H
    n = fbm(rs, H, W, 24, 6, 4)
    if p['kind'] == 'ring':
        r = np.sqrt(((u - 0.5) * 2) ** 2 + ((v - 0.5) * 2) ** 2); n2 = fbm(rs, H, W, 9, 9, 4); edge = 0.72 + 0.5 * (n2 - 0.5)
        a = np.clip((edge - r) * 5, 0, 1) * (0.3 + 0.45 * np.clip((n - 0.3) * 2.4, 0, 1)); a = np.maximum(a, np.clip((n - 0.56) * 6, 0, 1) * np.clip((0.95 - r) * 4, 0, 1) * 0.6) * np.clip((1 - r) * 5, 0, 1)      # soft partly transparent foam patch, irregular edge
    else:
        a = np.clip((0.5 + 0.5 * np.sin((v * 5 + n * 2.2) * 2 * math.pi) - 0.62) * 9, 0, 1) * np.clip(n * 1.6 - 0.25, 0, 1)
    save(np.ones((H, W, 3), 'float32') * (0.93 + 0.07 * n[..., None]), out, a)

def all_jobs():
    J = {}
    J['hex'] = (dict(seed=5, cols=['#2c5f56', '#356a5c', '#2a5650', '#3a6e5a', '#294f4e'], seam='#8a6a44'), hexplates)
    J['tile'] = (dict(seed=7, col='#6a6e76'), tiles); J['tile_d'] = (dict(seed=8, col='#4c5058'), tiles)
    J['stone'] = (dict(seed=9, col='#a49e90'), stone); J['stone_d'] = (dict(seed=10, col='#7c7a72', ch=40), stone)
    J['matting'] = (dict(seed=11, col='#cdb27c', bat='#6e5230'), matting); J['matting_d'] = (dict(seed=12, col='#b8996a', bat='#5a4228'), matting)
    J['dancheong'] = (dict(), dancheong)
    for k in ('red', 'black', 'white_r', 'white_k', 'tri_red', 'tri_black', 'tri_blue', 'tri_yellow', 'nob_circle', 'nob_diamond', 'nob_rcircle', 'sail'): J['flag_' + k] = (dict(kind=k), flag)
    J['foam_wake'] = (dict(kind='wake', w=1024, h=256, seed=41, cx=24, cy=6), foam); J['foam_bow'] = (dict(kind='bow', w=512, h=128, seed=43, cx=16, cy=4), foam)
    J['foam_ring'] = (dict(kind='ring', w=256, h=256, seed=47), foam); J['foam_surf'] = (dict(kind='surf', w=1024, h=128, seed=49), foam)
    return J

def ensure(verbose=True):
    os.makedirs(TEX, exist_ok=True); J = all_jobs(); mp = os.path.join(TEX, 'manifest.json')
    try: man = json.load(open(mp)) if os.path.exists(mp) else {}
    except ValueError: man = {}
    out = {}; m0 = dict(man)
    for name, (params, fn) in J.items():
        h = hashlib.sha1((TEX_V + fn.__name__ + json.dumps(params, sort_keys=True)).encode()).hexdigest(); png = os.path.join(TEX, name + '.png'); out[name] = png
        if man.get(name) != h or not os.path.exists(png):
            fn(params, png); man[name] = h
            if verbose: print('painted', name, flush=True)
    if man != m0:
        tmp = '%s.%d.tmp' % (mp, os.getpid()); json.dump(man, open(tmp, 'w')); os.replace(tmp, mp)
    return out
if __name__ == '__main__': print(len(ensure()), 'textures')

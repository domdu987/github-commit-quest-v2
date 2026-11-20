#!/usr/bin/env python3
"""beck_util.py (builder B): helpers shared by beck_under.py and beck_map.py. Imports builder A's beck.py (never edits it).
  - Pt / pl / spot / halo: Part and light wrappers that add the module-wide origin ORG (so a location can be built in local coordinates
    and placed anywhere in a bigger world, for example the platform hall 60 D below the street in the shaft shot).
  - painters for B's textures (cached in tex_beck/ with the prefix u_, never touching beck_tex.TEX_V).
  - actors: cast22 cards through beck.cast_card, named so the raster cache is stable, with billboard + pose swap helpers."""
import os, sys, math, random, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import beck as B
from beck import V, T, STATE, BX
import bpy

HERE = B.HERE
UTEX_V = 10
ORG = V((0.0, 0.0, 0.0))

def set_org(x, y, z):
    global ORG
    ORG = V((x, y, z))

# ----------------------------------------------------------------------------- Part / lights with the origin
class Pt(B.Part):
    """B.Part + ORG: geometry is built in local coordinates; the object is moved by ORG when finished.
    hd = ink distance: the hull is sized as if the camera were hd D from the part (shots whose camera range spans 4 .. 400 D set it by hand)."""
    def __init__(s, name, at=None, ink=True, shadow=True, camera_only=False, hd=None):
        B.Part.__init__(s, name, at, ink, shadow, camera_only); s.hd = hd
    def done(s, at=None, px=3.0):
        at = V(at or s.at or (0, 0, 0)) + ORG
        if s.hd:
            keep = STATE['cam']; STATE['cam'] = at + V((0, 0, s.hd))
            ob = B.Part.done(s, at, px); STATE['cam'] = keep
        else: ob = B.Part.done(s, at, px)
        ob.location = ob.location + ORG
        return ob

def pl(name, loc, rgb, energy, radius=0.4):
    return B.point_light(name, tuple(V(loc) + ORG), rgb, energy, radius)

def spot(name, loc, target, rgb, energy, spot_deg=60, blend=0.4, radius=0.3):
    return B.spot_light(name, tuple(V(loc) + ORG), tuple(V(target) + ORG), rgb, energy, spot_deg, blend, radius)

def view(p):
    """Representative camera position (LOCAL coords) used for the ink thickness of what is built next."""
    STATE['cam'] = V(p) + ORG

# ----------------------------------------------------------------------------- textures
def utex(name, fn):
    os.makedirs(BX.OUT, exist_ok=True)
    p = os.path.join(BX.OUT, 'u_%s_v%d.png' % (name, UTEX_V))
    if not os.path.exists(p): fn().save(p)
    STATE['tx'][name] = p
    return p

def ink_rect(d, box, fill, w=6, ink='#1a1840'):
    d.rectangle(box, fill=fill, outline=ink, width=w)

def sign_img(text, bg, fg, border=None, w=800, h=240, f=BX.FB, sub=None, radius=0.1):
    return BX.sign(text, bg, fg, border=border, w=w, h=h, f=f, radius=radius, sub=sub)

def tex_pocket_cover(W=400, H=560):
    img = Image.new('RGB', (W, H), '#f6ecd0'); d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, int(H * .22)), fill='#1f49c8'); BX.fit_text(d, (20, 14, W - 20, int(H * .2)), 'UNDERGROUND', 'white')
    r = BX.roundel('MAP', 360); img.paste(r, (20, int(H * .27)), r)
    d.rectangle((0, int(H * .74), W, H), fill='#e3262b'); BX.fit_text(d, (20, int(H * .77), W - 20, int(H * .96)), 'POCKET MAP', '#fff1c0')
    d.rectangle((3, 3, W - 4, H - 4), outline='#1a1840', width=8)
    return img

def tex_crate(W=512, H=384, word='REPRINT'):
    img = Image.new('RGB', (W, H), '#c88a46'); d = ImageDraw.Draw(img); rs = np.random.RandomState(3)
    a = np.asarray(img, 'float32') / 255 * (0.82 + BX.noise(rs, H, W, 6, 0.3))[..., None]; img = Image.fromarray((np.clip(a, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(img)
    for y in range(0, H, 96): d.line((0, y, W, y), fill='#6a3a14', width=6)
    d.rectangle((0, 0, 28, H), fill='#7a4a1a'); d.rectangle((W - 28, 0, W, H), fill='#7a4a1a')
    d.rectangle((60, 90, W - 60, H - 90), fill='#f6ecd0', outline='#1a1840', width=6); BX.fit_text(d, (74, 100, W - 74, H - 100), word, '#d4161c')
    return img

def tex_moquette(W=256, H=256):
    img = Image.new('RGB', (W, H), '#a81c2c'); d = ImageDraw.Draw(img); rs = random.Random(4)
    for y in range(0, H, 32):
        for x in range(0, W, 32):
            c = '#1f49c8' if (x // 32 + y // 32) % 2 else '#ffc81e'; d.polygon([(x + 16, y + 4), (x + 28, y + 16), (x + 16, y + 28), (x + 4, y + 16)], fill=c); d.ellipse((x + 12, y + 12, x + 20, y + 20), fill='#1a1840')
    a = np.asarray(img, 'float32') / 255 * (0.85 + BX.noise(np.random.RandomState(2), H, W, 3, 0.3))[..., None]
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype('uint8'))

def tex_streak(W=1024, H=256):
    """Tunnel rushing past a carriage window: near-black navy with horizontal lamp streaks and cable lines (tiles horizontally)."""
    rs = random.Random(7); a = np.zeros((H, W, 3), 'float32'); a[:] = (0.02, 0.04, 0.16)
    img = Image.fromarray((a * 255).astype('uint8')); d = ImageDraw.Draw(img)
    for y in (36, 70, 104, 150, 196):
        d.line((0, y, W, y), fill=(14, 24, 80), width=3 + int(rs.random() * 6))
    for k in range(7):
        x = rs.randint(0, W); y = rs.choice((52, 84, 124, 176)); L = rs.randint(160, 420)
        d.line((x, y, x + L, y), fill=(255, 196, 96), width=6); d.line((x, y, x + L * .6, y), fill=(255, 236, 190), width=2)
        if x + L > W: d.line((0, y, x + L - W, y), fill=(255, 196, 96), width=6)
    for k in range(5):
        x = rs.randint(0, W); d.rectangle((x, 0, x + 26, H), fill=(10, 16, 60))
    return img.filter(ImageFilter.GaussianBlur(1.2))

def tex_strata(W=1024, H=1024):
    rs = np.random.RandomState(11); y = np.linspace(0, 1, H)[:, None]; base = np.zeros((H, W, 3), 'float32')
    cols = [np.array(c, 'float32') * 1.5 for c in ((0.20, 0.14, 0.42), (0.10, 0.12, 0.40), (0.26, 0.16, 0.36), (0.08, 0.10, 0.34))]
    for i in range(H):
        t = (i / H * 5.0 + 0.4 * math.sin(i * 0.05)) % 4; k = int(t); f = t - k; base[i, :] = cols[k] * (1 - f) + cols[(k + 1) % 4] * f
    base *= (0.8 + BX.noise(rs, H, W, 10, 0.5))[..., None]
    img = Image.fromarray((np.clip(base, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(img)
    r2 = random.Random(5)
    for _ in range(260):
        x, yy = r2.randint(0, W), r2.randint(0, H); r = r2.randint(3, 11); c = r2.choice([(70, 60, 130), (40, 50, 120), (96, 70, 100), (20, 26, 80)])
        d.ellipse((x - r, yy - r * .7, x + r, yy + r * .7), fill=c)
    return img

def tex_hall_floor(W=512, H=512):
    img = Image.new('RGB', (W, H), '#c9b890'); d = ImageDraw.Draw(img); s = W // 4
    for i in range(4):
        for j in range(4):
            if (i + j) % 2: d.rectangle((i * s, j * s, (i + 1) * s, (j + 1) * s), fill='#3a3a8a')
            d.polygon([(i * s + s // 2, j * s + 6), (i * s + s - 6, j * s + s // 2), (i * s + s // 2, j * s + s - 6), (i * s + 6, j * s + s // 2)], outline='#e8dcb8', width=3)
    a = np.asarray(img, 'float32') / 255 * (0.9 + BX.noise(np.random.RandomState(8), H, W, 5, 0.18))[..., None]
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype('uint8'))

def tex_wood_slats(W=256, H=256):
    img = Image.new('RGB', (W, H), '#b06a2e'); d = ImageDraw.Draw(img); rs = np.random.RandomState(6)
    for y in range(0, H, 64): d.rectangle((0, y, W, y + 56), fill='#b8742f'); d.line((0, y + 58, W, y + 58), fill='#4a2410', width=6)
    a = np.asarray(img, 'float32') / 255 * (0.82 + BX.noise(rs, H, W, 4, 0.4))[..., None]
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype('uint8'))

def tex_ticket_front(W=640, H=320):
    img = Image.new('RGB', (W, H), '#2a1a12'); d = ImageDraw.Draw(img)
    d.rectangle((10, 10, W - 11, H - 11), fill='#5a2a14', outline='#d6a24a', width=8)
    d.rectangle((40, 60, W - 40, 200), fill='#ffe2a0', outline='#1a1840', width=8)
    d.rectangle((60, 220, W - 60, 280), fill='#3a1a10'); d.rectangle((W // 2 - 40, 232, W // 2 + 40, 270), fill='#1a1010')
    return img

def tex_ad(i, w=360, h=480):
    return BX.poster(i + 2, w, h)

def tex_ceiling_tile(W=512, H=512):
    img = Image.new('RGB', (W, H), '#d9c9a0'); d = ImageDraw.Draw(img)
    for i in range(0, W, 128):
        d.line((i, 0, i, H), fill='#a89870', width=6); d.line((0, i, W, i), fill='#a89870', width=6)
    for i in range(64, W, 128):
        for j in range(64, H, 128): d.ellipse((i - 18, j - 18, i + 18, j + 18), outline='#b8a880', width=5)
    return img

U_PAINTERS = dict(pocket_cover=tex_pocket_cover, crate_reprint=lambda: tex_crate(word='REPRINT'), crate_maps=lambda: tex_crate(word='MAPS'),
                  moquette=tex_moquette, streak=tex_streak, strata=tex_strata, hall_floor=tex_hall_floor, wood_slats=tex_wood_slats,
                  ticket_front=tex_ticket_front, ceiling_tile=tex_ceiling_tile,
                  sign_trial=lambda: sign_img('NEW MAP', '#12307a', '#fff1c0', border='#ffc81e', w=640, h=240, sub='TRIAL'),
                  sign_new_pocket=lambda: sign_img('NEW POCKET MAP', '#12307a', '#fff1c0', border='#ffc81e', w=900, h=240),
                  sign_to_trains=lambda: sign_img('TO TRAINS', '#12307a', 'white', border='#ffc81e', w=900, h=240),
                  sign_enquiries=lambda: sign_img('MAPS', '#12724a', '#fff1c0', border='#fff1c0', w=600, h=220),
                  sign_exit=lambda: sign_img('WAY OUT', '#12724a', 'white', border='white', w=800, h=240),
                  sign_piccadilly=lambda: sign_img('PICCADILLY', '#12307a', '#fff1c0', border='#e3262b', w=900, h=240),
                  sign_red_line=lambda: sign_img('RED LINE', '#e3262b', '#fff1c0', border='#fff1c0', w=640, h=200),
                  sign_news_kiosk=lambda: sign_img('NEWS', '#e3262b', '#fff1c0', border='#fff1c0', w=480, h=170),
                  ad0=lambda: tex_ad(0), ad1=lambda: tex_ad(1), ad2=lambda: tex_ad(2), ad3=lambda: tex_ad(3), ad4=lambda: tex_ad(4))

def ensure_u(names=None):
    for n, fn in U_PAINTERS.items():
        if names is None or n in names: utex(n, fn)

# ----------------------------------------------------------------------------- actors (cast22 cards)
BILL = []                       # (object, tilt) camera-facing cards, re-faced per frame by face_cards()
ACTORS = {}                     # name -> dict(poses={key: obj}, mark, ...)

def actor(name, story, mark, poses=None, cast=None, rim='#9fb8ff', face='cam', yaw_deg=None, mirror=False, scale=1.0, shadow=True, tilt=0.0, pose=None):
    """cast22 card `name` standing at mark (x, y, z) (+ORG). `poses` = {key: story or (cast, pose)} extra poses (all start hidden; set_pose(name, key) shows one).
    story = the default pose (key 'main'). face='cam' = camera-facing billboard (default); face=None keeps yaw_deg."""
    mk = tuple(V(mark[:3]) + ORG); d = dict(poses={}, mark=mk, rim=rim, face=face, tilt=tilt)
    allp = {'main': story}; allp.update(poses or {})
    for k, st in allp.items():
        pose_over = pose if k == 'main' else None
        ob = B.cast_card(st, mk, face_to=(STATE['cam'] if face == 'cam' else None), yaw_deg=yaw_deg, tilt=tilt, mirror=mirror, pose=pose_over, rim=rim, name='act_%s_%s' % (name, k), scale=scale,
                         cast=cast, shadow=(shadow and k == 'main'))
        d['poses'][k] = ob; ob.hide_render = (k != 'main'); ob.hide_viewport = (k != 'main')
        if face == 'cam': BILL.append((ob, tilt))
    d['cur'] = 'main'; ACTORS[name] = d
    return d

def set_pose(name, key):
    d = ACTORS[name]
    for k, ob in d['poses'].items(): ob.hide_render = (k != key); ob.hide_viewport = (k != key)
    d['cur'] = key

def move_actor(name, mark):
    d = ACTORS[name]; mk = tuple(V(mark[:3]) + ORG)
    for ob in d['poses'].values(): ob.location = mk
    d['mark'] = mk

def face_cards(cam_loc=None):
    """Re-face every camera-facing card to the camera (yaw only, plus the lean-back tilt)."""
    cam = bpy.context.scene.camera; c = V(cam_loc) if cam_loc is not None else V(cam.location)
    for ob, tilt in BILL:
        d = c - ob.location; yaw = math.atan2(d.x, -d.y); ob.rotation_euler = (math.radians(-tilt), 0, yaw)

def crowd_card(name, i, pose, mark, **kw):
    sys.path.insert(0, os.path.join(B.PROJ, 'v3', 'cast22')); sys.path.insert(0, os.path.join(B.PROJ, 'v3', 'cast'))
    import cast22
    c, p = cast22.crowd_member(i, pose)
    return actor(name, (c, p), mark, **kw)

# ----------------------------------------------------------------------------- misc geometry
def ring_poly(cx, cz, r, n=24):
    return [(cx + r * math.cos(2 * math.pi * k / n), cz + r * math.sin(2 * math.pi * k / n)) for k in range(n)]

def shadow_blob(mb, x, y, z, w, d=None):
    d = d or w * 0.7
    B.plane(mb, (x - w / 2, y - d / 2, z + 0.03), (w, 0, 0), (0, d, 0), STATE['E']('blob', 'blob', alpha=True), (0, 0, 1, 1))

def smooth(a, b, u):
    u = max(0.0, min(1.0, u)); return a + (b - a) * (u * u * (3 - 2 * u))

def lerp(a, b, u): return a + (b - a) * u

def seg_box(mb, p0, p1, w, h, mat, up=(0, 0, 1)):
    """Oriented bar from p0 to p1 with cross-section w (horizontal) x h (vertical), sits on top of the line (z up from p0)."""
    p0, p1 = V(p0), V(p1); X = (p1 - p0); L_ = X.length; X.normalize(); Z = V(up); Y = Z.cross(X)
    if Y.length < 1e-4: Y = V((0, 1, 0)).cross(X)
    Y.normalize(); Zn = X.cross(Y)
    from mine import obox
    obox(mb, (p0 + p1) / 2 + Zn * h / 2, X, Y, Zn, L_ / 2, w / 2, h / 2, mat)

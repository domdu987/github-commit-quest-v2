#!/usr/bin/env python3
"""dairy_board.py : STYLE BOARD of film 11 (Jenner, cowpox, Berkeley 1796). 3 stills: A cowshed (golden morning, key preset), B Jenner's cottage
garden (low angle), C the cowshed in late afternoon (alternative palette). bpy 5.x Cycles CPU. Helpers are imported from the earlier sets
(tower: MB, mat_lit, mat_emit, make_camera, render, placeholder_actor, setup_grade; mine: obox, beam, rod, lumpy, _untoon, _denoise; wall:
_air_comp), the geometry is new. World: 1 unit = 1 D (head), Z up. NO depth of field, NO text.
usage: python3 dairy_board.py [A|B|C ...] [--preview]"""
import os, sys, math, time, random, json
import numpy as np
import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (HERE, os.path.join(PROJ, 'v3', 'set3d9'), os.path.join(PROJ, 'v3', 'set3d8'), os.path.join(PROJ, 'v3', 'set3d2'), os.path.join(PROJ, 'v3', 'set3d4'),
          os.path.join(PROJ, 'v3', 'set3d5'), os.path.join(PROJ, 'v3', 'set3d6'), os.path.join(PROJ, 'v3', 'set3d7')):
    if p not in sys.path: sys.path.insert(0, p)
import tower as T                                       # noqa: E402
import mine as MN                                       # noqa: E402
import wall as W9                                       # noqa: E402
import dairy_board_tex as X                             # noqa: E402
from tower import MB, no_bounce, setup_grade, mat_emit  # noqa: E402
from mine import obox, beam, rod, lumpy, _untoon        # noqa: E402
STATE = T.STATE; OUT = os.path.join(HERE, 'board')
FORM = (0.0, -0.05, 0.22)

# ----------------------------------------------------------------------------- light presets
def _base(**k):
    d = dict(toon=1.0, key_desat=0.0, ink='#24160e', night=False, form=FORM, bloom_size=0.05, sun_angle=0.6, wet=0.0, lamps=1.0, grade_saturation=1.18)
    d.update(k); return d
LIGHTS = dict(
    MORNING=_base(key=(1.95, 1.50, 0.88), key_dir=W9._kdaz(205, 20), shade=(0.102, 0.136, 0.34), shade_tint=(0.087, 0.118, 0.37), shade_mix=0.62, lift=(0.010, 0.018, 0.036),
                  grade_offset=(-0.006, -0.01, -0.014), bounce=(1.0, 0.66, 0.36, 0.20), beams=0.03, air=('#f4cf94', 0.30, 14.0, 160.0), sky='day'),
    AFTERNOON=_base(key=(2.25, 1.28, 0.50), key_dir=W9._kdaz(185, 11), shade=(0.070, 0.105, 0.36), shade_tint=(0.06, 0.10, 0.41), shade_mix=0.8, lift=(0.002, 0.008, 0.026),
                    grade_offset=(-0.004, -0.010, -0.008), bounce=(1.0, 0.55, 0.30, 0.10), beams=0.03, air=('#f0a870', 0.34, 14.0, 160.0), sky='eve', sun_angle=0.5, grade_saturation=1.15),
    DAY=_base(key=(1.95, 1.46, 0.84), key_dir=W9._kdaz(228, 36), shade=(0.115, 0.10, 0.31), shade_tint=(0.11, 0.098, 0.33), shade_mix=0.55, lift=(0.010, 0.010, 0.024),
              grade_offset=(-0.006, -0.01, -0.014), bounce=(1.0, 0.66, 0.36, 0.24), beams=0.0, air=('#f2d4a0', 0.40, 60.0, 900.0), sky='day'),
)
SKY = dict(day=dict(top='#5a8ae0', mid='#8ab4ee', hor='#f6e2bc', cloud_lit='#fff2dc', cloud_sh='#b6b2e8'),
           eve=dict(top='#4c64c8', mid='#9a98dc', hor='#f8c892', cloud_lit='#ffe2b4', cloud_sh='#9a8ad0'))

# ----------------------------------------------------------------------------- scene setup / material makers
def new_scene(lkey, seed=0):
    scene = bpy.context.scene; P = dict(LIGHTS[lkey])
    for ob in list(scene.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for coll in (bpy.data.meshes, bpy.data.lights, bpy.data.cameras):
        for x in list(coll):
            if x.users == 0: coll.remove(x)
    for m in list(bpy.data.materials): bpy.data.materials.remove(m)
    STATE.clear(); STATE['P'] = P; STATE['loc'] = 'dairy'; STATE['light'] = lkey
    SET = T._coll('SET', scene); LIG = T._coll('LIGHTS', scene); T._wipe(SET); T._wipe(LIG); STATE['SET'] = SET; STATE['LIGHTS'] = LIG
    w = bpy.data.worlds.get('W_dairy') or bpy.data.worlds.new('W_dairy'); scene.world = w; nt = T._tree(w)
    bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld'); bg.inputs['Color'].default_value = (0, 0, 0, 1); bg.inputs['Strength'].default_value = 0.0
    nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
    MN.setup_render(scene, 'final'); scene.frame_start = scene.frame_end = scene.frame_current = 1
    scene.render.threads_mode = 'FIXED'; scene.render.threads = 4
    pre = 'DB_%s_' % lkey; cache = {}
    def C(hexcol, gain=1.0, sm=1.0, form=True, smix=None):
        k = ('c', hexcol, gain, sm, form, smix)
        if k not in cache: cache[k] = _untoon(T.mat_lit(pre + 'c%d' % len(cache), hexcol, gain=gain, shade_mul=sm, form=FORM if form else None, shade_mix=smix))
        return cache[k]
    def TX(name, gain=1.0, sm=1.0, form=True, smix=None):
        k = ('t', name, gain, sm, form, smix)
        if k not in cache: cache[k] = _untoon(T.mat_lit(pre + 't%d' % len(cache), image=X.get(name), gain=gain, shade_mul=sm, form=FORM if form else None, shade_mix=smix))
        return cache[k]
    def E(hexcol, k=1.0, name=None):
        key = ('e', hexcol, k)
        if key not in cache: cache[key] = mat_emit(pre + 'e%d' % len(cache), hexcol, strength=k)
        return cache[key]
    STATE.update(C=C, TX=TX, E=E)
    kd = Vector(P['key_dir']).normalized(); k = max(P['key'])
    d = bpy.data.lights.new('key_sun', 'SUN'); d.color = tuple(x / k for x in P['key']); d.energy = math.pi * k; d.angle = math.radians(P['sun_angle'])
    sun = bpy.data.objects.new('key_sun', d); LIG.objects.link(sun); sun.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler(); sun.location = (0, 0, 60); STATE['sun'] = sun
    br, bg_, bb, bk = P['bounce']; bd = Vector((-kd.x * 0.5, -kd.y * 0.5, 0.75)).normalized()
    d2 = bpy.data.lights.new('bounce_sun', 'SUN'); d2.color = (br, bg_, bb); d2.energy = math.pi * k * bk; d2.angle = math.radians(20); d2.use_shadow = False
    o2 = bpy.data.objects.new('bounce_sun', d2); LIG.objects.link(o2); o2.rotation_euler = (-bd).to_track_quat('Z', 'Y').to_euler()
    return scene, SET, P, kd

def finish(scene, SET, P):
    scene.cycles.use_light_tree = False; MN._denoise(scene); setup_grade(scene); W9._air_comp(scene, P)
    for ob in SET.objects: no_bounce(ob)

# ----------------------------------------------------------------------------- geometry helpers
def R(seed): return random.Random(seed)
def qd(mb, mat, p0, p1, p2, p3, n, uvs=((0, 0), (1, 0), (1, 1), (0, 1))): mb.oface([p0, p1, p2, p3], mat, list(uvs), n)
def ell(mb, c, rad, mat, yaw=0.0, pitch=0.0, seg=10, rings=6):
    """Ellipsoid with radii (rx, ry, rz) in its own frame (x forward), yawed about z and pitched about y."""
    c = Vector(c); cy, sy, cp, sp = math.cos(yaw), math.sin(yaw), math.cos(pitch), math.sin(pitch); mb.pid += 1; Rw = []
    for k in range(rings + 1):
        th = math.pi * k / rings; row = []
        for i in range(seg):
            ph = 2 * math.pi * i / seg; x = rad[0] * math.sin(th) * math.cos(ph); y = rad[1] * math.sin(th) * math.sin(ph); z = -rad[2] * math.cos(th)
            x, z = x * cp + z * sp, -x * sp + z * cp; row.append(c + Vector((x * cy - y * sy, x * sy + y * cy, z)))
        Rw.append(row)
    for k in range(rings):
        for i in range(seg):
            j = (i + 1) % seg; mb.face([Rw[k][i], Rw[k][j], Rw[k + 1][j], Rw[k + 1][i]], mat, [(i / seg, k / rings), ((i + 1) / seg, k / rings), ((i + 1) / seg, (k + 1) / rings), (i / seg, (k + 1) / rings)])
def bx(mb, lo, hi, mat, tile=(4, 4)): mb.box(lo, hi, mat, tile=tile)
def post(mb, x, y, z0, z1, w, mat): bx(mb, (x - w / 2, y - w / 2, z0), (x + w / 2, y + w / 2, z1), mat, (3, 3))
def cone(mb, c, r, h, mat, seg=8): rod(mb, c, (c[0], c[1], c[2] + h), r, mat, seg=seg, r1=0.0)
def disk_scatter(rg, n, x0, x1, y0, y1): return [(rg.uniform(x0, x1), rg.uniform(y0, y1)) for _ in range(n)]
def par(mb, mat, p, ex, ey, ez):
    """Parallelepiped from corner p and edge vectors (all 6 faces, used for emissive light shafts: winding irrelevant)."""
    p, ex, ey, ez = map(Vector, (p, ex, ey, ez))
    for a, b, o in ((ex, ey, Vector()), (ex, ey, ez), (ex, ez, Vector()), (ex, ez, ey), (ey, ez, Vector()), (ey, ez, ex)):
        mb.pid += 1; mb.face([p + o, p + o + a, p + o + a + b, p + o + b], mat)
def beam_shaft_mat(E, k):
    m = mat_emit('DB_shaft_%g' % k, '#ffd596', strength=k, additive=True, camera_only=True); return m

# ----- creatures and small props -------------------------------------------------------------------------------------------------------
def cow(mb, pos, yaw, M, pose=0.0):
    """Low-poly dairy cow: body 4.4 long, back 2.6 high. M: hide (texture), brown, white, pink, dark, horn."""
    c = Vector(pos); f = Vector((math.cos(yaw), math.sin(yaw), 0)); s = Vector((-f.y, f.x, 0))
    ell(mb, c + Vector((0, 0, 1.72)), (2.15, 0.95, 0.98), M['hide'], yaw, seg=14, rings=8)
    ell(mb, c + f * 1.5 + Vector((0, 0, 1.95)), (0.95, 0.75, 0.85), M['hide'], yaw, 0.0, seg=10, rings=6)                       # shoulder
    ell(mb, c + f * 2.55 + Vector((0, 0, 1.7 + pose)), (0.78, 0.46, 0.5), M['hide'], yaw, -0.45 + pose * 0.3, seg=10, rings=6)    # neck
    hp = c + f * 3.25 + Vector((0, 0, 1.25 + pose * 1.4)); ell(mb, hp, (0.62, 0.38, 0.42), M['white'], yaw, -0.65, seg=10, rings=6)   # head
    ell(mb, hp + f * 0.38 + Vector((0, 0, -0.12)), (0.26, 0.31, 0.27), M['pink'], yaw, -0.6, seg=8, rings=5)                    # muzzle
    for sg in (-1, 1):
        cone(mb, hp + s * sg * 0.28 + Vector((0, 0, 0.28)) - f * 0.1, 0.1, 0.46, M['horn'], 6)
        ell(mb, hp + s * sg * 0.5 + Vector((0, 0, 0.16)) - f * 0.05, (0.3, 0.12, 0.1), M['brown'], yaw + sg * 0.5, 0.2, seg=6, rings=4)   # ear
    for fx, sg in ((1.45, -1), (1.45, 1), (-1.55, -1), (-1.55, 1)):
        rod(mb, c + f * fx + s * sg * 0.55 + Vector((0, 0, 1.55)), c + f * fx + s * sg * 0.55 + Vector((0, 0, 0.18)), 0.26, M['brown'] if fx < 0 else M['white'], seg=6, r1=0.18)
        rod(mb, c + f * fx + s * sg * 0.55 + Vector((0, 0, 0.2)), c + f * fx + s * sg * 0.55 + Vector((0, 0, 0.0)), 0.2, M['dark'], seg=6)
    ell(mb, c - f * 1.2 + Vector((0, 0, 0.95)), (0.55, 0.5, 0.36), M['pink'], yaw, seg=8, rings=5)                               # udder
    rod(mb, c - f * 2.1 + Vector((0, 0, 2.2)), c - f * 2.4 + Vector((0, 0.1, 0.5)), 0.08, M['brown'], seg=5, r1=0.05); ell(mb, c - f * 2.4 + Vector((0, 0.1, 0.4)), (0.12, 0.12, 0.28), M['brown'], seg=6, rings=4)
def hen(mb, pos, yaw, body, comb, beak='#e3a63a', M=None):
    c = Vector(pos); f = Vector((math.cos(yaw), math.sin(yaw), 0)); ell(mb, c + Vector((0, 0, 0.45)), (0.36, 0.26, 0.3), M['hen'], yaw, 0.35, seg=8, rings=5)
    ell(mb, c + f * 0.3 + Vector((0, 0, 0.8)), (0.14, 0.11, 0.16), M['hen'], yaw, seg=6, rings=4); ell(mb, c + f * 0.3 + Vector((0, 0, 0.98)), (0.09, 0.05, 0.08), M['comb'], yaw, seg=6, rings=4)
    cone(mb, c + f * 0.43 + Vector((0, 0, 0.8)), 0.05, 0.12, M['beak'], 5); ell(mb, c - f * 0.36 + Vector((0, 0, 0.62)), (0.2, 0.08, 0.22), M['hen2'], yaw, 0.9, seg=6, rings=4)
    for sg in (-1, 1): rod(mb, c + Vector((0, 0, 0.25)) + Vector((-f.y, f.x, 0)) * sg * 0.1, c + Vector((0, 0, 0.0)) + Vector((-f.y, f.x, 0)) * sg * 0.1, 0.03, M['beak'], seg=4)
def cat(mb, pos, yaw, mat, mat2, sit=False):
    c = Vector(pos); f = Vector((math.cos(yaw), math.sin(yaw), 0)); s = Vector((-f.y, f.x, 0))
    if sit:
        ell(mb, c + Vector((0, 0, 0.42)), (0.3, 0.26, 0.42), mat, yaw, 0.2, seg=8, rings=5); ell(mb, c + f * 0.12 + Vector((0, 0, 0.98)), (0.22, 0.2, 0.2), mat, yaw, seg=8, rings=5)
        hd = c + f * 0.12 + Vector((0, 0, 0.98))
    else:
        ell(mb, c + Vector((0, 0, 0.3)), (0.55, 0.22, 0.24), mat, yaw, seg=8, rings=5); hd = c + f * 0.55 + Vector((0, 0, 0.5)); ell(mb, hd, (0.2, 0.19, 0.19), mat, yaw, seg=8, rings=5)
    for sg in (-1, 1): cone(mb, hd + s * sg * 0.12 + Vector((0, 0, 0.12)), 0.07, 0.17, mat2, 4)
    rod(mb, c - f * 0.45 + Vector((0, 0, 0.25)), c - f * 0.95 + Vector((0, 0, 0.6)), 0.06, mat, seg=5, r1=0.045)
def pail(mb, c, r, h, M, water=False):
    c = Vector(c); rod(mb, c, c + Vector((0, 0, h)), r * 0.85, M['wood'], seg=10, r1=r); rod(mb, c + Vector((0, 0, h * 0.25)), c + Vector((0, 0, h * 0.32)), r * 0.89, M['iron'], seg=10, r1=r * 0.91)
    rod(mb, c + Vector((0, 0, h * 0.72)), c + Vector((0, 0, h * 0.8)), r * 0.97, M['iron'], seg=10, r1=r * 0.99)
    if water: rod(mb, c + Vector((0, 0, h * 0.9)), c + Vector((0, 0, h * 0.93)), r * 0.97, M['milk'], seg=10)
    for sg in (-1, 1): rod(mb, c + Vector((sg * r, 0, h * 0.8)), c + Vector((0, 0, h * 1.35)), 0.025, M['iron'], seg=4)
def stool(mb, c, M, h=1.1):
    c = Vector(c); bx(mb, (c.x - 0.5, c.y - 0.5, c.z + h - 0.16), (c.x + 0.5, c.y + 0.5, c.z + h), M['wood2'], (2, 2))
    for dx, dy in ((-.36, -.36), (.36, -.36), (-.36, .36), (.36, .36)): rod(mb, c + Vector((dx * 1.2, dy * 1.2, 0)), c + Vector((dx, dy, h - 0.1)), 0.07, M['wood2'], seg=5)
def lantern(mb, gm, c, chain_to, M, name):
    c = Vector(c); rod(mb, c + Vector((0, 0, 0.7)), Vector(chain_to), 0.025, M['iron'], seg=4)
    bx(mb, (c.x - 0.3, c.y - 0.3, c.z - 0.5), (c.x + 0.3, c.y + 0.3, c.z - 0.4), M['iron'], (1, 1)); bx(mb, (c.x - 0.34, c.y - 0.34, c.z + 0.5), (c.x + 0.34, c.y + 0.34, c.z + 0.6), M['iron'], (1, 1))
    cone(mb, c + Vector((0, 0, 0.6)), 0.34, 0.25, M['iron'], 6)
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)): rod(mb, c + Vector((dx * 0.28, dy * 0.28, -0.4)), c + Vector((dx * 0.28, dy * 0.28, 0.5)), 0.025, M['iron'], seg=4)
    bx(gm, (c.x - 0.24, c.y - 0.24, c.z - 0.38), (c.x + 0.24, c.y + 0.24, c.z + 0.46), M['glow'], (1, 1))
    li = MN._light(name, (c.x, c.y, c.z), (1.0, 0.68, 0.36), 1500, 0.3); return li
def sack(mb, c, r, mat, seed): lumpy(mb, (c[0], c[1], c[2] + r * 0.85), r, mat, seed, seg=8, rings=6, rough=0.12, squash=1.25)
def bale(mb, c, M, yaw=0.0):
    c = Vector(c); X_ = Vector((math.cos(yaw), math.sin(yaw), 0)); Y_ = Vector((-X_.y, X_.x, 0)); obox(mb, c, X_, Y_, (0, 0, 1), 1.1, 0.8, 0.7, M['hay'], 0.4)
    for o in (-0.55, 0.55): obox(mb, c + X_ * o, X_, Y_, (0, 0, 1), 0.05, 0.82, 0.72, M['twine'], 0.4)
def hayheap(mb, c, M, r, seed, n=6):
    rg = R(seed)
    for i in range(n): lumpy(mb, (c[0] + rg.uniform(-r, r) * 1.2, c[1] + rg.uniform(-r, r) * 0.8, c[2] + rg.uniform(0, r * 0.7)), r * rg.uniform(0.55, 0.95), M['hayc'] if i % 3 else M['hayc2'], seed + i, seg=9, rings=6, rough=0.2, squash=0.8)
def wheel(mb, c, r, M, ax=(0, 1, 0)):
    c = Vector(c); a = Vector(ax)
    u = a.cross(Vector((0, 0, 1))); u.normalize() if u.length > 1e-3 else None; v = a.cross(u)
    for i in range(16):
        t0, t1 = 2 * math.pi * i / 16, 2 * math.pi * (i + 1) / 16
        rod(mb, c + (u * math.cos(t0) + v * math.sin(t0)) * r, c + (u * math.cos(t1) + v * math.sin(t1)) * r, 0.1, M['wood2'], seg=4)
    for i in range(6): t = math.pi * i / 6; rod(mb, c + (u * math.cos(t) + v * math.sin(t)) * r, c - (u * math.cos(t) + v * math.sin(t)) * r, 0.07, M['wood2'], seg=4)
    rod(mb, c - a * 0.25, c + a * 0.25, 0.16, M['iron'], seg=6)
def tree(mb, c, h, r, trunk, leaf_mats, seed, blossom=None):
    rg = R(seed); c = Vector(c); rod(mb, c, c + Vector((0, 0, h * 0.55)), r * 0.13, trunk, seg=7, r1=r * 0.08)
    for i in range(3): a = rg.uniform(0, 6.28); rod(mb, c + Vector((0, 0, h * 0.4)), c + Vector((math.cos(a) * r * 0.6, math.sin(a) * r * 0.6, h * 0.7)), r * 0.05, trunk, seg=5)
    for i in range(7):
        a = rg.uniform(0, 6.28); d = rg.uniform(0, r * 0.55); lumpy(mb, (c.x + math.cos(a) * d, c.y + math.sin(a) * d, c.z + h * rg.uniform(0.62, 0.95)), r * rg.uniform(0.5, 0.8), leaf_mats[i % len(leaf_mats)], seed + i, seg=9, rings=6, rough=0.2, squash=0.85)
    if blossom:
        for i in range(10):
            a = rg.uniform(0, 6.28); d = rg.uniform(r * 0.3, r * 0.85); sp = Vector((c.x + math.cos(a) * d, c.y + math.sin(a) * d, c.z + h * rg.uniform(0.6, 1.0))); mb.sphere(sp, r * 0.07, blossom, seg=5, rings=3)

def sky_dome(SET, lkey, az0):
    sk = SKY[LIGHTS[lkey]['sky']]; path = X.get_sky(LIGHTS[lkey]['sky'], az0=az0, **sk); m = mat_emit('DB_sky_' + lkey, image=path, strength=1.0)
    mb = MB(); seg, rings, Rr = 64, 20, 1800.0; mb.pid += 1
    def pt(i, k):
        az = 2 * math.pi * i / seg; el = (math.pi / 2) * k / rings
        return (Rr * math.cos(el) * math.cos(az), Rr * math.cos(el) * math.sin(az), Rr * math.sin(el) - 40)
    for k in range(rings):
        for i in range(seg):
            a0, a1 = i / seg, (i + 1) / seg
            mb.face([pt(i, k), pt(i + 1, k), pt(i + 1, k + 1), pt(i, k + 1)], m, [(a0, k / rings), (a1, k / rings), (a1, (k + 1) / rings), (a0, (k + 1) / rings)])
    ob = mb.obj('sky', SET); ob.visible_shadow = False; STATE['sky_obj'] = ob; return ob

def hill_field(SET, M, x0, x1, y0, y1, nx, ny, hf, name='hills'):
    mb = MB(); mb.pid += 1; pts = [[(x0 + (x1 - x0) * i / nx, y0 + (y1 - y0) * j / ny) for i in range(nx + 1)] for j in range(ny + 1)]
    Z = [[hf(*p) for p in row] for row in pts]
    for j in range(ny):
        for i in range(nx):
            q = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
            mb.oface([(pts[b][a][0], pts[b][a][1], Z[b][a]) for a, b in q], M['hills'], [(a / nx * 2.0, b / ny) for a, b in q], (0, 0, 1))
    ob = mb.obj(name, SET); return ob

def sm(a, b, x): t = min(1, max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t)

# ============================================================================= BARN (A and C)
BX0, BX1, BY1 = -10.0, 10.0, 34.0
DOOR = (10.0, 21.0, 5.8)                # y0, y1, lintel z on the left wall x = -10
def barn(SET, LIG, M, P, kd, lkey, cam_loc, hi=False):
    rg = R(5); mb = MB(); gm = MB(); fw = MB(); kdv = Vector(kd).normalized(); lights = []
    # ---------------- ground, floor, farmyard
    mb.quad((-500, -300, -0.05), (1000, 0, 0), (0, 800, 0), M['grass'], (-500 / 9, -300 / 9, 500 / 9, 500 / 9))
    mb.quad((BX0, -1, 0.0), (20, 0, 0), (0, BY1 + 1, 0), M['earth'], (0, 0, 3.3, 5.8))
    mb.quad((-30, 6, 0.01), (20.2, 0, 0), (0, 22, 0), M['lane'], (0, 0, 1.7, 2.4)); mb.quad((-11.6, 11.2, 0.03), (2.4, 0, 0), (0, 9.2, 0), M['stone2'], (0, 0, 1, 3))
    # ---------------- walls: planks with gaps (the left one has the open door), back and front gables
    pw, gap = 0.92, 0.16; y = -0.5; PT = (7.36, 7.0)
    while y < BY1 + 0.5:
        if DOOR[0] - 0.05 < y < DOOR[1] - 0.05: bx(mb, (BX0 - 0.6, y, DOOR[2] + 0.55), (BX0, y + pw, 5.85), M['oak'], PT)
        else: bx(mb, (BX0 - 0.6, y, 0.0), (BX0, y + pw, 5.85), M['oak'], PT)
        bx(mb, (BX1, y, 0.0), (BX1 + 0.6, y + pw, 5.85), M['oak_d'], PT); y += pw + gap
    for yy, mt, th in ((BY1, M['oak_d'], 0.6), (-0.7, M['oak'], 0.6)):
        x = BX0 - 0.6
        while x < BX1 + 0.6:
            xc = x + pw / 2; top = 5.8 + 3.8 * (1 - min(1, abs(xc) / 11.0)) - 0.3
            z0_ = 5.9 if (yy < 0 and -6.2 < x < 2.2) else 0.0
            bx(mb if yy > 0 else fw, (x, yy, z0_), (x + pw, yy + th, max(top, 5.85)), mt, PT); x += pw + 0.1
    bx(mb, (BX0 - 0.7, DOOR[0] - 0.05, DOOR[2]), (BX0 + 0.1, DOOR[1] + 0.05, DOOR[2] + 0.55), M['oak'], (3, 3))
    for yy in (DOOR[0] - 0.45, DOOR[1] + 0.45): post(mb, BX0 + 0.1, yy, 0, DOOR[2], 0.8, M['oak'])
    obox(mb, (BX0 - 1.7, DOOR[0] - 2.1, 2.9), (0.95, 0.3, 0), (-0.3, 0.95, 0), (0, 0, 1), 1.9, 0.16, 2.9, M['oak_d'], 0.4)             # leaf swung back
    # ---------------- timber frame
    for yy in np.arange(0.3, BY1, 5.7):
        for xx in (-9.55, 9.55): post(mb, xx, yy, 0, 5.7, 0.62, M['oak'])
        if yy < 1 or (hi and yy < 8): continue
        bx(mb, (-10, yy - 0.3, 5.6), (10, yy + 0.3, 6.2), M['oak'], (3, 3)); post(mb, 0, yy, 6.2, 9.4, 0.5, M['oak'])
        for sg in (-1, 1): beam(mb, (sg * 9.55, yy, 3.9), (sg * 7.0, yy, 5.8), 0.32, 0.3, M['oak']); beam(mb, (sg * 1.3, yy, 6.2), (0, yy, 8.2), 0.3, 0.26, M['oak'])
    for yy in np.arange(0.3, BY1, 1.9):
        for sg in (-1, 1): beam(mb, (sg * 10.2, yy, 5.0), (0, yy, 9.5), 0.22, 0.22, M['oak'], uvk=0.6)
    for sg in (-1, 1):
        for t in (0.35, 0.7): xx = sg * 10.2 * (1 - t); zz = 5.0 + (9.5 - 5.0) * t; bx(mb, (xx - 0.17, -0.5, zz - 0.2), (xx + 0.17, BY1 + 0.5, zz + 0.2), M['oak'], (3, 3))
        bx(mb, (sg * 9.7 - 0.25, -0.5, 5.4), (sg * 9.7 + 0.25, BY1 + 0.5, 5.9), M['oak'], (3, 3))
    bx(mb, (-0.25, -0.5, 9.2), (0.25, BY1 + 0.5, 9.8), M['oak'], (3, 3))
    for sg in (-1, 1):                                                           # roof: dark boarding below, stone slates above (blocks the key)
        a = Vector((sg * 11.8, 0, 4.7)); b = Vector((0, 0, 9.9)); dv = (b - a); L = dv.length; dv.normalize(); n = Vector((0, 1, 0)).cross(dv).normalized(); n = n if n.z > 0 else -n
        for off, hz, mt in ((0.45, 0.45, M['oak_d']), (1.15, 0.28, M['slate'])): obox(mb, (a + b) / 2 + n * off + Vector((0, BY1 / 2, 0)), dv, (0, 1, 0), n, L / 2 + 0.5, BY1 / 2 + 1.5, hz, mt, 0.2)
    # ---------------- hay loft (back) with a ladder
    LY = 22.0
    bx(mb, (BX0, LY, 4.4), (BX1, BY1, 4.8), M['oak'], (4, 4)); bx(mb, (BX0, LY - 0.3, 3.7), (BX1, LY + 0.3, 4.6), M['oak'], (3, 3))
    for xx in (-9.55, -4.8, 0, 4.8, 9.55): post(mb, xx, LY, 0, 4.6, 0.6, M['oak'])
    for xx in np.arange(-9.0, 9.1, 2.0): bx(mb, (xx - 0.2, LY, 3.8), (xx + 0.2, BY1, 4.4), M['oak'], (3, 3))
    for xx in np.arange(-9.5, 9.6, 1.6): rod(mb, (xx, LY + 0.1, 4.8), (xx, LY + 0.1, 6.0), 0.07, M['oak'], seg=4)
    bx(mb, (BX0, LY, 5.9), (BX1, LY + 0.2, 6.15), M['oak'], (3, 3))
    for i, (cx_, cy_) in enumerate(((-6, 25), (-1, 26), (5, 25), (-8, 30), (2, 31), (8, 30), (-4, 32), (6, 28))): hayheap(mb, (cx_, cy_, 4.8), M, 2.3, 40 + i * 5, 6)
    hayheap(mb, (-3.0, LY + 0.5, 4.8), M, 1.4, 99, 4)
    for i in range(14): rod(mb, (rg.uniform(-9, 9), LY + 0.15, 4.6), (rg.uniform(-9, 9), LY - 0.15, rg.uniform(2.8, 4.2)), 0.04, M['straw'], seg=3)
    lx = -7.0
    for sg in (-0.45, 0.45): rod(mb, (lx + sg, LY - 3.0, 0.0), (lx + sg, LY - 0.15, 5.3), 0.09, M['wood2'], seg=5)
    for k in range(1, 10): zz = k * 0.55; yy = LY - 3.0 + (LY - 0.15 - (LY - 3.0)) * zz / 5.3; rod(mb, (lx - 0.45, yy, zz), (lx + 0.45, yy, zz), 0.06, M['wood2'], seg=4)
    # ---------------- stalls along the right wall (cows), mangers, hay racks
    for yy in (12.6, 17.6, 22.6):
        bx(mb, (2.8, yy - 0.09, 0.0), (9.9, yy + 0.09, 3.6), M['oak'], (3, 3)); bx(mb, (2.7, yy - 0.18, 3.45), (9.9, yy + 0.18, 3.75), M['oak_d'], (3, 3)); post(mb, 2.7, yy, 0, 4.2, 0.5, M['oak'])
    for y0, y1 in ((12.6, 17.6), (17.6, 22.6)):
        bx(mb, (8.9, y0 + 0.2, 0.9), (9.95, y1 - 0.2, 1.7), M['oak_d'], (3, 3)); bx(mb, (9.05, y0 + 0.4, 1.4), (9.85, y1 - 0.4, 1.75), M['hay'], (2, 2))
        for yy in np.arange(y0 + 0.6, y1 - 0.5, 0.55): rod(mb, (9.7, yy, 3.0), (9.4, yy, 4.7), 0.05, M['wood2'], seg=4)
    bx(mb, (2.7, 12.5, 0.0), (2.85, 17.7, 0.7), M['oak_d'], (3, 3)); bx(mb, (2.7, 12.5, 0.7), (2.85, 17.7, 0.9), M['oak'], (3, 3))
    cow(mb, (5.3, 15.1, 0.0), 0.0, dict(M, hide=M['hide']), 0.0)
    cow(mb, (5.2, 20.1, 0.0), 0.0, dict(M, hide=M['brown']), -0.08)
    for yy in (13.7, 18.7): hayheap(mb, (3.4, yy, 0.0), M, 0.7, 70 + int(yy), 3)
    # ---------------- Blossom in the sun (milkmaid's cow) and the milking things
    cow(mb, (-4.2, 15.6, 0.0), math.pi, M, 0.05)
    stool(mb, (-5.2, 13.3, 0.0), M); pail(mb, (-3.3, 13.5, 0.0), 0.5, 0.95, M, True); pail(mb, (-6.9, 12.0, 0.0), 0.5, 0.95, M)
    # ---------------- foreground: bale stack, churns, pails, tools, wheel, barrels, sacks
    for (bxx, byy, bz, yw) in ((6.6, 6.6, 0.7, 0.1), (8.1, 7.6, 0.7, -0.2), (7.2, 6.9, 2.1, 0.15), (4.6, 8.8, 0.7, 0.5), (8.2, 10.2, 0.7, 0.0)): bale(mb, (bxx, byy, bz), M, yw)
    for (bxx, byy, bz, yw) in ((8.4, 25.0, 0.7, 0.0), (8.0, 27.6, 0.7, 0.1), (8.4, 26.2, 2.1, 0.0), (-8.2, 24.0, 0.7, 1.5), (-8.0, 26.5, 0.7, 1.6), (-8.2, 25.2, 2.1, 1.55), (-8.4, 28.5, 0.7, 1.6)): bale(mb, (bxx, byy, bz), M, yw)
    for i, (cx_, cy_) in enumerate(((-7.6, 7.2), (-6.3, 8.2), (-8.3, 9.0))):
        c = Vector((cx_, cy_, 0)); rod(mb, c, c + Vector((0, 0, 1.9)), 0.62, M['iron'], seg=10, r1=0.5); rod(mb, c + Vector((0, 0, 1.9)), c + Vector((0, 0, 2.4)), 0.3, M['iron'], seg=10, r1=0.34)
        rod(mb, c + Vector((0, 0, 2.4)), c + Vector((0, 0, 2.6)), 0.46, M['brass'], seg=10, r1=0.46)
    pail(mb, (-3.4, 8.6, 0.0), 0.55, 1.0, M); pail(mb, (-2.6, 9.5, 0.0), 0.5, 0.9, M, True); pail(mb, (1.6, 9.0, 0.0), 0.5, 0.95, M)
    for (cx_, cy_, r_) in ((-9.0, 9.5, 0.9), (-8.2, 11.0, 0.8)): rod(mb, (cx_, cy_, 0), (cx_, cy_, 2.1), r_ * 0.85, M['wood2'], seg=10, r1=r_ * 0.85); rod(mb, (cx_, cy_, 0.5), (cx_, cy_, 0.6), r_ * 0.9, M['iron'], seg=10); rod(mb, (cx_, cy_, 1.5), (cx_, cy_, 1.6), r_ * 0.9, M['iron'], seg=10)
    wheel(mb, (-9.1, 9.0, 2.0), 2.0, M, (1, 0, 0))
    for i, (sx_, sy_) in enumerate(((8.2, 22.2), (9.0, 20.8), (-9.0, 30.5), (-8.0, 32.2), (7.6, 32.5))): sack(mb, (sx_, sy_, 0), 0.95, M['sack'] if i % 2 else M['sack2'], 200 + i)
    for (px, py, lean) in ((9.5, 6.0, -0.35), (-9.4, 16.0, 0.0)):                               # pitchfork and rake against a post
        a0 = Vector((px, py, 0)); a1 = Vector((px + lean * 3, py, 5.6)); rod(mb, a0, a1, 0.06, M['wood2'], seg=4)
        for dy in (-0.3, 0, 0.3): rod(mb, a1, a1 + Vector((lean * 0.3, dy, 1.2)), 0.04, M['iron'], seg=3)
    # wheelbarrow
    wb = Vector((1.2, 7.0, 0)); obox(mb, wb + Vector((0, 0, 1.05)), (1, 0, 0), (0, 1, 0), (0, 0, 1), 1.2, 0.8, 0.4, M['oak'], 0.4); wheel(mb, wb + Vector((1.5, 0, 0.55)), 0.55, M, (0, 1, 0))
    for sg in (-1, 1): rod(mb, wb + Vector((1.4, sg * 0.6, 1.0)), wb + Vector((-2.2, sg * 0.7, 1.5)), 0.07, M['wood2'], seg=4)
    hayheap(mb, (wb.x, wb.y, 1.25), M, 0.8, 321, 3)
    for (bxx, byy, bz, yw) in ((7.6, 2.6, 0.7, 0.1), (8.9, 4.6, 0.7, -0.2), (8.2, 3.4, 2.1, 0.15)): bale(mb, (bxx, byy, bz), M, yw)
    for (cx_, cy_) in ((-8.4, 2.4), (-7.0, 3.8)):
        c = Vector((cx_, cy_, 0)); rod(mb, c, c + Vector((0, 0, 1.9)), 0.62, M['iron'], seg=10, r1=0.5); rod(mb, c + Vector((0, 0, 1.9)), c + Vector((0, 0, 2.4)), 0.3, M['iron'], seg=10, r1=0.34); rod(mb, c + Vector((0, 0, 2.4)), c + Vector((0, 0, 2.6)), 0.46, M['brass'], seg=10, r1=0.46)
    hayheap(mb, (-2.6, 3.2, 0.0), M, 0.9, 412, 4); hayheap(mb, (3.0, 5.4, 0.0), M, 0.8, 413, 4)
    pail(mb, (3.4, 4.2, 0.0), 0.5, 0.95, M); pail(mb, (-3.2, 4.6, 0.0), 0.55, 1.0, M, True)
    for (hx, hy, hyaw) in ((-1.6, 5.4, 0.5), (2.0, 6.4, 2.2)): hen(mb, (hx, hy, 0), hyaw, M['hen'], M['comb'], M=M)
    # ---------------- harness on pegs (back wall), bridles on the stall wall
    bx(mb, (-9.0, BY1 - 0.4, 3.6), (9.0, BY1, 3.9), M['oak'], (3, 3))
    for k, xx in enumerate(np.arange(-8.0, 8.1, 2.0)): rod(mb, (xx, BY1 - 0.4, 3.75), (xx, BY1 - 1.3, 3.75), 0.07, M['iron'], seg=4)
    for k, xx in enumerate((-7.0, -3.0, 1.0, 5.0)):
        c = Vector((xx, BY1 - 1.0, 2.6)); n = 14
        for i in range(n):
            t0, t1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n; rod(mb, c + Vector((math.cos(t0) * 0.7, 0, math.sin(t0) * 0.9)), c + Vector((math.cos(t1) * 0.7, 0, math.sin(t1) * 0.9)), 0.2, M['leather'], seg=5)
        for i in range(0, n, 3): t0 = 2 * math.pi * i / n; mb.sphere(c + Vector((math.cos(t0) * 0.78, -0.1, math.sin(t0) * 1.0)), 0.13, M['brass'], seg=5, rings=3)
    for xx in (-8.0, -6.0, -2.0, 2.0, 6.0, 8.0): rod(mb, (xx, BY1 - 1.2, 3.75), (xx + 0.15, BY1 - 1.2, 1.7), 0.07, M['leather'], seg=4); mb.sphere((xx + 0.15, BY1 - 1.2, 1.6), 0.14, M['brass'], seg=5, rings=3)
    bx(mb, (9.6, 21.0, 3.5), (9.9, 30.0, 3.7), M['oak'], (3, 3))
    for yy in (21.8, 23.5, 25.2, 27.0, 28.6): rod(mb, (9.6, yy, 3.6), (8.8, yy, 3.6), 0.07, M['iron'], seg=4); rod(mb, (8.9, yy, 3.6), (8.9, yy, 1.6 + rg.random()), 0.07, M['leather'], seg=4)
    # ---------------- lanterns on the tie beams
    L1 = lantern(mb, gm, (-0.5, 10.5, 3.9), (-0.5, 10.5, 5.7), M, 'lamp1'); L2 = lantern(mb, gm, (4.0, 17.5, 3.6), (4.0, 17.5, 5.7), M, 'lamp2'); L3 = lantern(mb, gm, (0.6, 28.0, 2.9), (0.6, 28.0, 3.8), M, 'lamp3')
    # ---------------- hens, cats, nest, swallows
    for i, (hx, hy, hyaw) in enumerate(((-4.6, 8.8, 0.6), (-3.6, 10.0, 2.4), (0.2, 11.6, -0.8), (-1.8, 12.4, 1.4), (7.0, 6.4, 2.0))): hen(mb, (hx, hy, 0 if i < 4 else 1.4), hyaw, M['hen'], M['comb'], M=M)
    cat(mb, (6.6, 6.5, 2.8), -2.0, M['cat1'], M['cat1'], sit=True); cat(mb, (-1.0, 11.0, 0.0), 0.7, M['cat2'], M['cat2']); cat(mb, (-8.4, 26.5, 2.8), 0.0, M['catw'], M['catw'], sit=True)
    c = Vector((-1.6, 8.0, 0)); rod(mb, c, c + Vector((0, 0, 0.5)), 0.7, M['straw'], seg=10, r1=0.9)
    for dx in (-0.25, 0.25): ell(mb, c + Vector((dx, 0, 0.5)), (0.17, 0.12, 0.14), M['white'], seg=6, rings=4)
    for (sx_, sy_, sz_) in ((-1.0, 14.0, 4.7), (2.6, 17.5, 6.8), (-5.6, 18.0, 4.2)):
        ell(mb, (sx_, sy_, sz_), (0.28, 0.16, 0.08), M['black'], 0.7, seg=6, rings=4)
        for sg in (-1, 1): ell(mb, (sx_ - sg * 0.06, sy_ + sg * 0.36, sz_ + 0.06), (0.22, 0.4, 0.04), M['black'], 0.7 + sg * 0.2, seg=5, rings=3)
    # ---------------- straw on the floor, dust motes, light shafts
    for (fx, fy) in disk_scatter(rg, 300, -9.6, 9.6, 1.0, 33.0):
        if abs(fx) > 3.2 or fy > 9: a = rg.uniform(0, 6.28); l = rg.uniform(0.3, 0.8); rod(mb, (fx, fy, 0.03), (fx + math.cos(a) * l, fy + math.sin(a) * l, 0.07 + rg.random() * 0.1), 0.018, M['straw'], seg=3)
    # light shafts: door slab and a few plank gaps, swept along the key direction down to the floor
    ke = Vector(kdv); sf = M['shaft']
    p0 = Vector((BX0, DOOR[0], 0.3)); t_ = (DOOR[2]) / -ke.z
    par(gm, sf, p0, Vector((0, DOOR[1] - DOOR[0], 0)), Vector((0, 0, DOOR[2] - 0.3)), ke * (t_ * 0.9))
    for yy in (21.4, 23.3, 25.2, 27.1, 29.0, 30.9):
        tt = 5.4 / -ke.z; par(gm, sf, Vector((BX0, yy, 0.2)), Vector((0, 0.16, 0)), Vector((0, 0, 5.3)), ke * (tt * 0.95))
    # motes
    for i in range(300):
        y0 = rg.uniform(DOOR[0], DOOR[1]); z0 = rg.uniform(0.6, DOOR[2]); t = rg.uniform(0.0, (z0 - 0.3) / -ke.z); pm = Vector((BX0, y0, z0)) + ke * t
        if pm.x < BX1 - 0.3 and pm.z > 0.3: gm.sphere(pm, rg.uniform(0.03, 0.06), M['mote'], seg=4, rings=3)
    for i in range(90):
        yy = rg.choice((21.4, 23.3, 25.2, 27.1, 29.0, 30.9)); z0 = rg.uniform(0.6, 5.2); t = rg.uniform(0.0, z0 / -ke.z * 0.95); pm = Vector((BX0, yy + 0.08, z0)) + ke * t
        if pm.x < BX1 - 0.3 and pm.z > 0.3: gm.sphere(pm, rg.uniform(0.03, 0.055), M['mote'], seg=4, rings=3)
    STATE['fw'] = fw
    return mb, gm, lights

def yard_out(SET, M, rg_seed=8):
    """Outside the open door (x < -10): farmyard stone wall, hay wagon, trees, the field."""
    rg = R(rg_seed); mb = MB(); lv = [M['green'], M['grass_d']]
    for yy in np.arange(-10, 70, 3.0):
        bx(mb, (-36.0, yy, 0), (-35.0, yy + 3.0, 2.2 + 0.25 * math.sin(yy)), M['stone2'], (4, 4))
    for (tx_, ty_, h, r) in ((-44, 8, 9, 5), (-50, 26, 11, 6), (-46, 44, 10, 5.5), (-60, 15, 12, 6.5), (-62, 38, 12, 6.5), (-40, 60, 9, 5)): tree(mb, (tx_, ty_, 0), h, r, M['wood2'], lv, int(ty_ * 3))
    obox(mb, (-24, 24, 1.6), (1, 0, 0), (0, 1, 0), (0, 0, 1), 3.0, 1.5, 0.5, M['oak'], 0.4); wheel(mb, (-24.0, 22.4, 2.0), 1.9, M, (0, 1, 0)); wheel(mb, (-24.0, 25.6, 2.0), 1.9, M, (0, 1, 0))
    hayheap(mb, (-24, 24, 2.1), M, 1.9, 600, 5)
    hayheap(mb, (-18, 36, 0.0), M, 3.0, 650, 6)
    mb.obj('yard', SET)
def static_barn_objs(mb, gm, SET, name='barn'):
    f = STATE['fw'].obj('frontwall', SET); f.visible_camera = False; o = mb.obj(name, SET); g = gm.obj(name + '_glow', SET); g.visible_shadow = False; return o, g

def mats(C, TX, E):
    return dict(
        oak=TX('planks', 1.0), oak_d=TX('planks_dark', 0.95), silver=TX('planks_silver', 1.0), hay=TX('hay', 0.9, 1.7, smix=0.3), hayc=C('#dcae4a', 0.95, 1.9, smix=0.22), hayc2=C('#c99a3c', 0.95, 1.9, smix=0.22), earth=TX('earth', 1.0), lane=TX('lane', 1.0), grass=TX('grass', 1.0), grass_d=TX('grass_d', 0.95),
        stone=TX('stone', 1.0), stone2=TX('stone_grey', 1.0), thatch=TX('thatch', 1.0, 1.3, smix=0.35), plaster=TX('plaster', 1.0), slate=TX('slate', 1.0), hide=TX('cow', 0.78, 1.3, smix=0.4), hills=TX('hills', 1.0),
        brown=C('#7a4526'), white=C('#f2e9d6'), pink=C('#e8a898'), dark=C('#3e2a1e'), horn=C('#efe2bc'), iron=C('#4a4a58'), wood=C('#a8743c'), wood2=C('#8a5a2e'), twine=C('#6d4a22'),
        milk=C('#fbf4e6'), glow=mat_emit('DB_glow', '#ffc46a', strength=7.0), hen=C('#c46a34'), hen2=C('#7a3c1c'), comb=C('#d8321e'), beak=C('#e3a63a'), leather=C('#6b3d1e'), brass=C('#d7a43a'),
        sack=C('#cdb48a'), sack2=C('#b89b6c'), red=C('#b6402e'), green=C('#4a7a38'), door=C('#3f6f7a'), cat1=C('#d8873a'), cat2=C('#5a5a68'), catw=C('#efe6d4'),
        tile=C('#b8553a'), glass=C('#8fb4d0', 1.1), black=C('#2c2430'), straw=C('#e0b84e', 1.0, 1.6, smix=0.3), apple=C('#a8c24a'), bloom_w=C('#f7ecec'), bloom_p=C('#f2b6c8'),
        shaft=mat_emit('DB_shaft', '#ffd596', strength=0.20, additive=True, camera_only=True), mote=mat_emit('DB_mote', '#fff0c0', strength=3.2),
        cream=C('#efe2bd'), blue=C('#3f5fb8'), violet=C('#7a62c8'), yellow=C('#f0c43a'), orange=C('#e8802a'), rose=C('#d8586a'), lav=C('#8a78d0'), leaf=C('#3f7a34'), leaf2=C('#5c9040'), smoke=C('#f2ead8'),
        gate=C('#3d6a72'), thatch_d=C('#8c6a30'), church=TX('stone', 1.0), churchr=TX('slate', 1.0), yew=C('#2f5a30'), sheep=C('#f0e8d4'))

# ============================================================================= B: the village exterior
def cottage(SET, M, P):
    rg = R(11); mb = MB(); gm = MB()
    # ground: orchard/garden grass, lane, verges
    mb.quad((-600, -60, -0.05), (1200, 0, 0), (0, 130, 0), M['grass'], (-600 / 9, -60 / 9, 600 / 9, 70 / 9))
    mb.quad((-600, -11, 0.0), (1200, 0, 0), (0, 6.5, 0), M['lane'], (0, 0, 40, 1))
    mb.quad((-60, -4.5, 0.0), (120, 0, 0), (0, 11.5, 0), M['grass_d'], (0, 0, 14, 1.5)); mb.quad((-120, 6, 0.0), (240, 0, 0), (0, 80, 0), M['grass'], (-14, 0, 14, 8))
    mb.quad((-3.8, -4.4, 0.04), (2.6, 0, 0), (0, 11.6, 0), M['stone2'], (0, 0, 1, 4))                                  # flagged path to the door
    # ---- the cottage: honey Cotswold stone, thatch roof with deep eaves, chimneys, casements
    x0, x1, y0, y1, ze = -10.0, 10.0, 8.0, 16.0, 5.6
    bx(mb, (x0, y0, 0), (x1, y1, ze), M['stone'], (7, 7)); bx(mb, (x1, y0 + 0.5, 0), (x1 + 7.0, y1 - 1.5, 4.0), M['stone'], (7, 7)); bx(mb, (x0 - 0.15, y0 - 0.12, 0), (x1 + 0.15, y0 + 0.0, 0.5), M['stone2'], (6, 6))
    def thatch_roof(xa, xb, ya, yb, z0, zr, over=1.3, th=1.5, nm='r'):
        """Gabled thatch roof along x with a rounded cross-section (bulging eaves, soft ridge); ends are closed."""
        hw = (yb - ya) / 2 + over; cy = (ya + yb) / 2; xl, xr = xa - over * 0.8, xb + over * 0.8
        prof = [(-hw, z0 - 0.3), (-hw + 0.35, z0 + 0.7), (-hw * 0.6, z0 + (zr - z0) * 0.62), (-hw * 0.2, zr - 0.1), (0, zr + 0.35), (hw * 0.2, zr - 0.1), (hw * 0.6, z0 + (zr - z0) * 0.62), (hw - 0.35, z0 + 0.7), (hw, z0 - 0.3)]
        zc = z0 + (zr - z0) * 0.4
        for (a1, c1), (a2, c2) in zip(prof, prof[1:]):
            Lq = math.hypot(a2 - a1, c2 - c1); n = Vector((0, -(c2 - c1), a2 - a1)).normalized()
            if n.dot(Vector((0, (a1 + a2) / 2, (c1 + c2) / 2 - zc))) < 0: n = -n
            mb.oface([(xl, cy + a1, c1), (xr, cy + a1, c1), (xr, cy + a2, c2), (xl, cy + a2, c2)], M['thatch'], [(0, 0), ((xr - xl) / 5, 0), ((xr - xl) / 5, Lq / 5), (0, Lq / 5)], n)
        for xe, nx_ in ((xl, -1), (xr, 1)): mb.oface([(xe, cy + a, c) for a, c in prof], M['thatch_d'], [(a / 5, c / 5) for a, c in prof], (nx_, 0, 0))
    thatch_roof(x0, x1, y0, y1, ze, 10.4)
    bx(mb, (x0 + 0.6, y0 + 0.4, ze - 0.2), (x1 - 0.6, y1 - 0.4, ze + 3.0), M['thatch_d'], (5, 5)) if False else None
    for xx in (-7.6, 3.6):                                                                                              # chimneys
        bx(mb, (xx - 0.9, y0 + 2.5, ze), (xx + 0.9, y0 + 4.3, 12.2), M['stone2'], (5, 5)); bx(mb, (xx - 1.1, y0 + 2.3, 11.6), (xx + 1.1, y0 + 4.5, 12.2), M['stone'], (5, 5))
        for dx in (-0.4, 0.4): rod(mb, (xx + dx, y0 + 3.4, 12.2), (xx + dx, y0 + 3.4, 13.0), 0.28, M['red'], seg=6)
    # front wall features (the facade faces -y at y = y0)
    yf = y0 - 0.02
    def casement(cx_, cz, w=1.9, h=2.2):
        bx(mb, (cx_ - w / 2 - 0.25, yf - 0.3, cz - h / 2 - 0.2), (cx_ + w / 2 + 0.25, yf + 0.05, cz + h / 2 + 0.25), M['cream'], (2, 2)); bx(mb, (cx_ - w / 2, yf - 0.34, cz - h / 2), (cx_ + w / 2, yf - 0.28, cz + h / 2), M['glass'], (1, 1))
        bx(mb, (cx_ - 0.05, yf - 0.4, cz - h / 2), (cx_ + 0.05, yf - 0.3, cz + h / 2), M['cream'], (1, 1)); bx(mb, (cx_ - w / 2, yf - 0.4, cz - 0.05), (cx_ + w / 2, yf - 0.3, cz + 0.05), M['cream'], (1, 1))
        bx(mb, (cx_ - w / 2 - 0.5, yf - 0.45, cz - h / 2 - 0.5), (cx_ + w / 2 + 0.5, yf - 0.05, cz - h / 2 - 0.2), M['oak'], (2, 2))
    for cx_ in (-7.0, 3.6, 7.2): casement(cx_, 2.7)
    for cx_ in (-5.2, 5.4):                                                                                       # eyebrow dormers in the thatch
        lumpy(mb, (cx_, y0 + 0.2, 8.55), 1.7, M['thatch'], 800 + int(cx_), seg=10, rings=6, rough=0.08, squash=0.62)
        bx(mb, (cx_ - 0.8, y0 - 1.0, 7.8), (cx_ + 0.8, y0 - 0.9, 8.9), M['glass'], (1, 1)); bx(mb, (cx_ - 0.95, y0 - 1.05, 7.7), (cx_ + 0.95, y0 - 0.95, 7.8), M['cream'], (1, 1)); bx(mb, (cx_ - 0.04, y0 - 1.06, 7.8), (cx_ + 0.04, y0 - 0.9, 8.9), M['cream'], (1, 1))
    for cx_ in (-5.2, 5.4):                                                                                           # eyebrow dormers in the thatch
        pass
    bx(mb, (-3.0, yf - 0.35, 0), (-1.0, yf + 0.05, 3.9), M['door'], (2, 2)); bx(mb, (-3.4, yf - 0.45, 3.9), (-0.6, yf - 0.05, 4.2), M['cream'], (2, 2)); mb.sphere((-1.4, yf - 0.45, 1.9), 0.12, M['brass'], seg=5, rings=3)
    for sx_ in (-3.3, -0.7): bx(mb, (sx_ - 0.15, yf - 0.4, 0), (sx_ + 0.15, yf - 0.05, 4.0), M['cream'], (1, 1))
    for k in range(6):  # climbing roses on the facade
        px = -4.2 + rg.uniform(-0.3, 0.3); pz = 0.8 + k * 0.7
        for j in range(6): lumpy(mb, (px + rg.uniform(-0.9, 0.9) + (j % 2) * 3.8, yf - 0.5, pz + rg.uniform(-0.3, 0.3)), 0.35, M['leaf2'], 700 + k * 9 + j, seg=7, rings=4, rough=0.25)
    for j in range(16): mb.sphere((-4.0 + rg.uniform(-1.4, 1.4) + (j % 2) * 3.5, yf - 0.85, 0.8 + rg.uniform(0, 3.8)), 0.16, M['rose'] if j % 3 else M['red'], seg=5, rings=3)
    # ---- the kitchen wing roof and the little porch
    thatch_roof(x1, x1 + 7.0, y0 + 0.5, y1 - 1.5, 4.0, 7.3, 0.9, 1.2)
    bx(mb, (-4.0, yf - 1.8, 4.1), (0.0, yf + 0.0, 4.5), M['thatch_d'], (3, 3)); post(mb, -3.8, yf - 1.6, 0, 4.1, 0.2, M['oak']); post(mb, -0.2, yf - 1.6, 0, 4.1, 0.2, M['oak'])
    # ---- picket fence, gate, stone wall, hedge
    for xx in np.arange(-22.0, 22.5, 0.62):
        if -3.7 < xx < -0.5: continue
        h = 1.4 + 0.06 * math.sin(xx * 3); bx(mb, (xx - 0.17, -4.6, 0), (xx + 0.17, -4.5, h), M['cream'], (1.2, 2)); cone(mb, (xx, -4.55, h), 0.2, 0.28, M['cream'], 4)
    for yy in (0.55, 1.5): bx(mb, (-22, -4.4, yy), (22, -4.28, yy + 0.2), M['cream'], (2, 1)) if False else None
    for zz in (0.4, 1.1): bx(mb, (-22, -4.45, zz), (-3.7, -4.3, zz + 0.2), M['cream'], (3, 3)); bx(mb, (-0.5, -4.45, zz), (22, -4.3, zz + 0.2), M['cream'], (3, 3))
    for xx in (-3.9, -0.3): post(mb, xx, -4.5, 0, 2.4, 0.4, M['cream']); mb.sphere((xx, -4.5, 2.5), 0.26, M['cream'], seg=6, rings=4)
    for xx in np.arange(-3.7, -0.5, 0.45): bx(mb, (xx - 0.1, -4.55, 0.3), (xx + 0.1, -4.5, 1.5 + 0.2 * math.sin(xx * 9)), M['gate'], (1, 2))
    for yy in np.arange(-4.5, 30, 2.2): bx(mb, (22.5, yy, 0), (23.7, yy + 2.2, 1.9 + 0.2 * math.sin(yy)), M['stone2'], (3, 3)); bx(mb, (22.3, yy + 0.4, 1.6), (23.9, yy + 1.8, 2.15), M['stone'], (3, 3))
    for xx in np.arange(10.5, 22.5, 2.2): bx(mb, (xx, 16.0, 0), (xx + 2.2, 17.2, 1.8 + 0.2 * math.sin(xx)), M['stone2'], (3, 3))
    # ---- cottage garden: beds, flower clumps, bean poles, skeps, butt, hens
    for (bx0, bx1) in ((-20.0, -4.4), (0.0, 21.0)): bx(mb, (bx0, -2.4, 0.0), (bx1, 6.6, 0.28), M['earth'], (5, 5))
    def clump(cx_, cy_, mat, hh, n=6, spike=False, mat2=None):
        for i in range(n):
            px, py = cx_ + rg.uniform(-0.55, 0.55), cy_ + rg.uniform(-0.45, 0.45); hz = hh * rg.uniform(0.75, 1.1)
            rod(mb, (px, py, 0.2), (px, py, hz), 0.045, M['leaf'], seg=4)
            if spike:
                for k in range(5): mb.sphere((px, py, hz - k * 0.2), 0.17 - k * 0.012, mat if (k % 2 == 0 or mat2 is None) else mat2, seg=5, rings=3)
            else: mb.sphere((px, py, hz), 0.24, mat, seg=6, rings=4)
        for i in range(3): lumpy(mb, (cx_ + rg.uniform(-0.5, 0.5), cy_ + rg.uniform(-0.4, 0.4), 0.35), 0.4, M['leaf2'], 900 + int(cx_ * 7) + i, seg=6, rings=4, rough=0.3)
    cols = [(M['blue'], 3.0, True), (M['rose'], 3.4, True), (M['yellow'], 1.2, False), (M['red'], 1.7, False), (M['white'], 1.4, False), (M['violet'], 2.0, True), (M['orange'], 1.0, False), (M['yellow'], 3.0, True), (M['blue'], 1.6, False), (M['bloom_p'], 1.5, False), (M['red'], 3.2, True), (M['white'], 2.6, True)]
    ci = 0
    for xx in np.arange(-19.0, -5.0, 1.9):
        for yy in (-1.3, 0.8, 3.0, 5.2): m_, h_, sp = cols[ci % len(cols)]; ci += 1; clump(xx + rg.uniform(-0.2, 0.2), yy, m_, h_, 4, sp, M['white'] if m_ is M['blue'] else None)
    for xx in np.arange(1.0, 21.0, 1.9):
        for yy in (-1.3, 0.8, 3.0, 5.2): m_, h_, sp = cols[ci % len(cols)]; ci += 1; clump(xx + rg.uniform(-0.2, 0.2), yy, m_, h_, 4, sp)
    for xx in np.arange(-22, 22, 0.55):                                                                                   # border flowers along the fence (close foreground)
        if -4 < xx < -0.5: continue
        m_ = (M['yellow'], M['white'], M['orange'], M['violet'], M['bloom_p'])[int(abs(xx) * 3) % 5]; mb.sphere((xx, -3.9 + rg.uniform(-0.3, 0.3), 0.55 + rg.random() * 0.4), 0.2, m_, seg=5, rings=3)
    for (px, py) in ((9.0, 4.0), (11.0, 2.5)):                                                                          # bean poles
        for k in range(4): a = k * 1.57; rod(mb, (px + math.cos(a) * 0.9, py + math.sin(a) * 0.9, 0), (px, py, 4.3), 0.05, M['wood2'], seg=4)
        lumpy(mb, (px, py, 2.0), 1.0, M['leaf'], int(px * 10), seg=8, rings=5, rough=0.3, squash=2.0)
    for (px, py) in ((14.5, 6.0), (16.0, 5.0), (13.2, 5.2)):
        rod(mb, (px, py, 0.0), (px, py, 1.1), 0.75, M['straw'], seg=10, r1=0.8); cone(mb, (px, py, 1.1), 0.72, 0.7, M['straw'], 10)
    rod(mb, (-22.5, 3.5, 0), (-22.5, 3.5, 2.2), 0.8, M['wood2'], seg=10); rod(mb, (-22.5, 3.5, 0.5), (-22.5, 3.5, 0.6), 0.85, M['iron'], seg=10)
    for i, (hx, hy, yw) in enumerate(((-2.0, -7.0, 0.5), (1.5, -7.6, 2.5), (-5.0, -7.2, -1.0), (4.0, -6.6, 1.0))): hen(mb, (hx, hy, 0), yw, M['hen'], M['comb'], M=M)
    cat(mb, (17.8, -4.4, 0.0), 3.0, M['cat1'], M['cat1'], sit=True) if False else cat(mb, (23.0, 5.0, 1.9), 3.5, M['cat1'], M['cat1'], sit=True)
    for i in range(520):                                                              # close foreground: grass tufts and wild flowers on the verge
        px, py = rg.uniform(-34, 14), rg.uniform(-18.0, -9.0); hh = rg.uniform(0.35, 1.1); c_ = (M['leaf2'], M['leaf'], M['grass_d'])[i % 3]
        if -9.5 < px < -2.5 and py < -10.5: continue
        for k in range(3): a = rg.uniform(0, 6.28); rod(mb, (px, py, 0), (px + math.cos(a) * 0.3, py + math.sin(a) * 0.3, hh), 0.05, c_, seg=3, r1=0.0)
        if i % 3 == 0: mb.sphere((px, py, hh + 0.1), rg.uniform(0.07, 0.13), (M['yellow'], M['white'], M['violet'], M['orange'], M['blue'], M['red'])[(i // 3) % 6], seg=5, rings=3)
    # ---- the little rustic thatched hut in the garden (round, woven walls, cone roof)
    hx, hy = -10.5, -0.5
    rod(mb, (hx, hy, 0), (hx, hy, 3.3), 2.8, M['oak'], seg=12, r1=2.8, uv=(4, 1)); rod(mb, (hx, hy, 3.3), (hx, hy, 6.9), 3.9, M['thatch'], seg=12, r1=0.35, uv=(4, 2)); rod(mb, (hx, hy, 6.8), (hx, hy, 7.7), 0.5, M['thatch_d'], seg=8, r1=0.0)
    for k in range(8): a = k * 0.785 + 0.2; post(mb, hx + math.cos(a) * 2.8, hy + math.sin(a) * 2.8, 0, 3.4, 0.3, M['wood2'])
    bx(mb, (hx - 0.8, hy - 2.95, 0), (hx + 0.8, hy - 2.6, 2.6), M['door'], (2, 2)); bx(mb, (hx - 1.0, hy - 3.0, 2.6), (hx + 1.0, hy - 2.7, 2.8), M['oak'], (2, 2)); bx(mb, (hx - 1.4, hy - 3.9, 0), (hx + 1.4, hy - 3.1, 0.18), M['stone2'], (2, 2))
    bx(mb, (hx + 1.2, hy - 4.3, 0.0), (hx + 3.2, hy - 3.8, 0.8), M['oak'], (2, 2))
    # ---- orchard (left), cow Blossom grazing, washing line, tubs
    for i, (tx_, ty_) in enumerate(((-16, 13), (-23, 3), (-24, 15), (-30, 8), (-14, 24), (-34, 20), (-40, 6), (-28, 30), (-46, 16))):
        tree(mb, (tx_, ty_, 0), 7.5 + (i % 3), 4.2 + (i % 2), M['wood2'], [M['leaf2'], M['leaf'], M['green']], 50 + i, blossom=M['bloom_p'] if i % 2 else M['bloom_w'])
    for (tx_, ty_) in ((-23, 3), (-16, 13), (-24, 15)):
        for k in range(5): mb.sphere((tx_ + rg.uniform(-3, 3), ty_ + rg.uniform(-3, 3), 0.15), 0.18, M['apple'], seg=5, rings=3)
    cow(mb, (-17.5, 5.5, 0.0), 3.0, dict(M, hide=M['hide']), -0.5)
    for yy in (-0.2, 1.0): rod(mb, (-12.5, yy + 6.5, 5.2), (-12.5, yy + 6.5, 0.0), 0.08, M['wood2'], seg=4)
    # ---- smoke from the chimneys (cartoon billows), distant church, sheep
    for k in range(5): lumpy(mb, (-7.6 + k * 0.5, y0 + 3.4, 14.0 + k * 1.3), 0.6 + k * 0.28, M['smoke'], 1200 + k, seg=8, rings=5, rough=0.15)
    mb.obj('cottage', SET)
    return mb

def church(SET, M, cx, cy, S=1.0, zb=0.0):
    mb = MB(); w = 6.5 * S; h = 38 * S
    bx(mb, (cx - w, cy - w, 0), (cx + w, cy + w, h), M['church'], (9, 9)); bx(mb, (cx - w - 0.6, cy - w - 0.6, h - 4.5 * S), (cx + w + 0.6, cy + w + 0.6, h - 3.2 * S), M['stone2'], (9, 9))
    bx(mb, (cx - w - 0.7, cy - w - 0.7, h), (cx + w + 0.7, cy + w + 0.7, h + 2.0 * S), M['church'], (9, 9)); bx(mb, (cx - w * 0.55, cy - w * 0.55, h + 2.0 * S), (cx + w * 0.55, cy + w * 0.55, h + 9.0 * S), M['church'], (9, 9)) if False else None
    for sx_, sy_ in ((-1, -1), (1, -1), (-1, 1), (1, 1)): bx(mb, (cx + sx_ * w - 1.0 * S, cy + sy_ * w - 1.0 * S, h + 2.0 * S), (cx + sx_ * w + 1.0 * S, cy + sy_ * w + 1.0 * S, h + 7.0 * S), M['church'], (9, 9)); cone(mb, (cx + sx_ * w, cy + sy_ * w, h + 7.0 * S), 1.1 * S, 3.0 * S, M['church'], 4)
    for dz in (14, 24): bx(mb, (cx - 1.2 * S, cy - w - 0.4, dz * S), (cx + 1.2 * S, cy - w, (dz + 6) * S), M['black'], (2, 2))
    bx(mb, (cx - 1.5 * S, cy - w - 0.4, h - 12 * S), (cx + 1.5 * S, cy - w, h - 4.0 * S), M['black'], (2, 2))
    bx(mb, (cx - 16 * S, cy + w * 0.4 - 7.5 * S, 0), (cx - w + 0.1, cy + w * 0.4 + 7.5 * S, 13 * S), M['church'], (9, 9))
    zr = 13 * S; hw = 7.5 * S; xa, xb = cx - 17 * S, cx - w + 0.1; cy2 = cy + w * 0.4
    for sg in (-1, 1):
        a = Vector((0, cy2 + sg * (hw + 0.8), zr - 0.2)); b = Vector((0, cy2, zr + 5.2 * S)); dv = b - a; L = dv.length; dv.normalize(); nn = Vector((1, 0, 0)).cross(dv).normalized(); nn = nn if nn.z > 0 else -nn
        obox(mb, (a + b) / 2 + Vector(((xa + xb) / 2, 0, 0)) + nn * 0.3, (1, 0, 0), dv, nn, (xb - xa) / 2 + 0.4, L / 2 + 0.2, 0.3, M['churchr'], 0.2)
    ob = mb.obj('church', SET); ob.location.z = zb - 0.6
def village_hills(SET, M, mb_unused=None, flip=False):
    def hf(x, y):
        d = max(0.0, y - 35.0); r_ = sm(0, 170, d)
        return -0.05 + (90 * r_ ** 1.2) * (0.55 + 0.45 * math.sin(x * 0.009 + 1.3) * math.cos(y * 0.007)) + 9 * r_ * math.sin(x * 0.03 + y * 0.011) * math.cos(x * 0.017)
    hill_field(SET, M, -700, 700, 20, 760, 96, 44, hf)
    mb = MB()
    for (tx_, ty_, h, r) in ((-72, 74, 9, 6), (-96, 90, 9, 6), (-60, 100, 10, 7), (95, 80, 10, 6.5), (70, 70, 9, 6), (120, 105, 10, 7)): tree(mb, (tx_, ty_, hf(tx_, ty_) - 0.2), h, r, M['wood2'], [M['leaf2'], M['leaf']], int(tx_))
    rg = R(3)
    for i in range(60): sx_, sy_ = rg.uniform(-180, 220), rg.uniform(90, 330); ell(mb, (sx_, sy_, hf(sx_, sy_) + 0.6), (1.0, 0.7, 0.7), M['sheep'], rg.uniform(0, 6), seg=6, rings=4)
    mb.obj('farfield', SET); return hf

# ============================================================================= cameras, people, runner
CAMS = dict(
    A=dict(loc=(1.8, -1.0, 2.4), look_at=(-4.0, 16.0, 2.6), lens=22),
    B=dict(loc=(2.0, -20.0, 1.3), look_at=(-5.0, 14.0, 5.0), lens=22),
    C=dict(loc=(5.4, -3.0, 7.6), look_at=(-3.4, 15.0, -0.2), lens=22),
)
def people(which, cam_loc):
    out = []
    spots = dict(A=[('extra_b', (-6.3, 12.3, 0.0)), ('extra_a', (-1.2, 14.8, 0.0)), ('boy', (1.3, 11.2, 0.0))],
                 C=[('extra_b', (-6.3, 12.3, 0.0)), ('extra_a', (-1.2, 14.8, 0.0)), ('boy', (1.3, 11.2, 0.0))],
                 B=[('extra_a', (-2.4, -6.6, 0.0)), ('boy', (-4.8, -6.2, 0.0)), ('extra_b', (1.8, -5.4, 0.0)), ('priest', (-8.2, -5.8, 0.0))])[which]
    for role, mk in spots:
        d = Vector(cam_loc) - Vector(mk); el = math.degrees(math.atan2(d.z - 1.5, math.hypot(d.x, d.y)))
        out.append(T.placeholder_actor(role, mk, face_to=cam_loc, tilt=max(0.0, el - 20) * 0.5, name='actor_' + role))
    return out

def build(which):
    lkey = dict(A='MORNING', B='DAY', C='AFTERNOON')[which]
    scene, SET, P, kd = new_scene(lkey); LIG = STATE['LIGHTS']; C, TX, E = STATE['C'], STATE['TX'], STATE['E']; M = mats(C, TX, E)
    if which in 'AC':
        sky_dome(SET, lkey, 0.5)
        mb, gm, _ = barn(SET, LIG, M, P, kd, lkey, CAMS[which]['loc'], hi=(which == 'C')); static_barn_objs(mb, gm, SET)
        yard_out(SET, M)
        def hf(x, y): d = max(0.0, -x - 50.0); r_ = sm(0, 300, d); return -0.1 + 30 * r_ ** 1.3 * (0.55 + 0.45 * math.sin(y * 0.008 + 1.3)) + 8 * r_ * math.sin(y * 0.03 + x * 0.01)
        mbh = None
        # rotated hill field: reuse hill_field with swapped roles (x is the depth here)
        def hf2(x, y): return hf(x, y)
        hill_field(SET, M, -760, -40, -300, 420, 48, 60, hf2)
        if which == 'C':
            for n_, l in STATE['objects'].items() if False else []: pass
    else:
        sky_dome(SET, lkey, 0.25)
        cottage(SET, M, P); hf = village_hills(SET, M); church(SET, M, -85, 125, 1.4, hf(-85, 125))
    finish(scene, SET, P)
    cam = T.make_camera(CAMS[which], 'cam', scene); cam.data.dof.use_dof = False; cam.data.clip_end = 4000.0
    people(which, CAMS[which]['loc'])
    return scene

def run(which, preview=False, samples=32):
    scene = build(which); os.makedirs(OUT, exist_ok=True)
    if preview: MN.setup_render(scene, "final"); scene.cycles.samples = 6; scene.render.threads = 4
    if samples and not preview: scene.cycles.samples = samples
    path = os.path.join(OUT, ('prev_' if preview else 'still_') + which + '.png'); w, c = T.render(path, scene); print(which, 'wall %.1fs cpu %.1fs' % (w, c), path, flush=True)
    return w, c, path

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]; prev = '--preview' in sys.argv
    log = {}
    for w in (args or ['A', 'B', 'C']): log[w] = run(w, prev)
    if not prev: json.dump({k: dict(wall=v[0], cpu=v[1]) for k, v in log.items()}, open(os.path.join(OUT, 'render_times_%s.json' % ''.join(sorted(log))), 'w'))

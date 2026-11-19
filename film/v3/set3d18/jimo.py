#!/usr/bin/env python3
"""jimo.py : set of film 18 ("ไอ้เสมียนวัว", Tian Dan's fire oxen at Jimo, Qi vs Yan, 279 BC) as a real 3D Blender set (bpy 5.3, Cycles CPU).
STYLE-BOARD stage: three zones, each built on its own (the zones share one world: 1 unit = 1 D = one head, Z up, +y = toward Jimo).

    import jimo as J
    A = J.build('wall')      # jimo_wall_night : outside the wall, low wide: rammed-earth wall, gate tower, moat, bridge, road, moon
    A = J.build('camp')      # yan_camp_night  : eye level inside the Yan camp looking at the far lit wall
    A = J.build('holes')     # wall_holes_oxen : inside, the wall base with the holes and ONE fire ox (placeholder)
    cam = J.make_camera(A['cam']); J.T.render(path)

World: the wall runs along x at y = 0 (outer face y -5 at the base -> -3 at the top, inner face y +4 -> +3; height 16, walk z 16); the gate in
the middle (x +-3.5); the moat y -22..-9.5 (water z -2.2); the Yan camp lies at y -130..-35. NO depth of field, NO text anywhere.
Built on the film-3..10 templates (imported, not copied): tower (materials, mesh builder, camera, render, grade), mine (boxes, rods,
lumpy, fire), bakery (Frame, glow cards, lights), desert (star sky), wall (film 9: compositor air).
CLI: python3 jimo.py board            the 3 final stills + style_board.jpg + hue numbers (board/)
     python3 jimo.py still <wall|camp|holes> [draft]"""
import os, sys, math, json, time, random, subprocess
import numpy as np
import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (HERE, ) + tuple(os.path.join(PROJ, 'v3', d) for d in ('set3d9', 'set3d8', 'set3d7', 'set3d6', 'set3d5', 'set3d4', 'set3d2')):
    if p not in sys.path: sys.path.insert(0, p)
import tower as T                                          # noqa: E402
import pagoda as G                                         # noqa: E402
import mine as MN                                          # noqa: E402
import bakery as BK                                        # noqa: E402
import desert as D                                         # noqa: E402
import wall as W9                                          # noqa: E402
import jimo_tex as JX                                      # noqa: E402
from tower import MB, no_bounce, setup_grade, mat_lit, mat_emit   # noqa: E402,F401
from mine import obox, beam, rod, lumpy, _obj, _untoon, _glossy, vnoise   # noqa: E402,F401
STATE = T.STATE
Frame = BK.Frame
OUT = os.path.join(HERE, 'board')
def _rnd(s): return random.Random(s)
V = Vector
FIRE = (1.0, 0.50, 0.18); LAMP = (1.0, 0.62, 0.30)

# ----------------------------------------------------------------------------- dimensions (D)
WH = 16.0                                                   # wall height (walk level)
def yo(z): return -5.0 + 2.0 * z / WH                       # outer face y at height z (battered)
def yi(z): return 4.0 - 1.0 * z / WH                        # inner face y
WATER_Z = -2.2; MOAT = (-30.0, -9.5)
GATE_W = 3.6; GATE_H = 9.6

# ----------------------------------------------------------------------------- light presets (shade hue 240-260 against warm fire / lantern light)
_B = dict(toon=1.0, key_desat=0.15, ink='#141a3e', night=True, form=(0.0, -0.05, 0.22), bloom_size=0.06, sun_angle=0.6, sky='NIGHT', sky_k=1.0, star_k=1.0,
          shade=(0.085, 0.105, 0.34), shade_tint=(0.085, 0.115, 0.38), shade_mix=0.72, lift=(0.010, 0.012, 0.040), grade_offset=(0.002, 0.003, 0.010), grade_saturation=1.14,
          lamps=1.0, air=('#6a5cb8', 0.30, 40.0, 420.0), beams=0.0, ground_k=1.0)
LIGHTS = dict(
    wall=dict(_B, key=(0.30, 0.44, 1.15), key_dir=G._kd((0.45, 0.89), 38)),
    camp=dict(_B, key=(0.30, 0.44, 1.15), key_dir=G._kd((0.30, 0.95), 42), air=('#6a5cb8', 0.26, 40.0, 420.0)),
    holes=dict(_B, key=(0.28, 0.42, 1.10), key_dir=G._kd((0.25, -0.97), 40), air=('#5a50a8', 0.14, 30.0, 300.0)),
)

CAMS = dict(
    wall=dict(loc=(-6.0, -56.0, 9.5), look_at=(3.0, 0.0, 17.6), lens=20),
    camp=dict(loc=(0.0, -112.0, 3.3), look_at=(0.0, 0.0, 11.0), lens=18),
    holes=dict(loc=(-4.0, 20.5, 3.7), look_at=(-1.0, 6.0, 4.0), lens=22),
)
MOON_DIR = dict(wall=(58.0, 20.0), camp=(74.0, 19.0), holes=(250.0, 36.0))

# ----------------------------------------------------------------------------- mesh banks
class Banks:
    def __init__(s): s.b = {}; s.hull = {}; s.shadow = {}
    def __call__(s, name, hull=0.0, shadow=True):
        if name not in s.b: s.b[name] = MB(); s.hull[name] = hull; s.shadow[name] = shadow
        return s.b[name]
    def flush(s, SET):
        for n, mb in s.b.items():
            if mb.f: _obj(mb, n, SET, hull=s.hull[n], shadow=s.shadow[n])

def lamp(name, loc, energy, rgb=LAMP, r=0.25, shadow=False):
    return BK._light(name, tuple(loc), rgb, energy, radius=r, shadow=shadow)

def halo(mb, c, r, mat, vertical=True):
    """Camera-only glow disc (crossed cards) around a light."""
    BK._halo(mb, c, r, {'halo': mat})

def flat(mb, o, du, dv, mat, uv=None):
    mb.quad(o, du, dv, mat, uv or (0, 0, 1, 1))

def ellipsoid(mb, c, rx, ry, rz, mat, seg=14, rings=8, uvs=(1, 1), phi=(0.0, 2 * math.pi), th=(0.0, math.pi), rough=0.0, seed=0, fn=None):
    """Ellipsoid (semi-axes rx ry rz, along x/y/z) with UV u around z, v pole to pole; theta/phi ranges for partial shells; fn(p) -> point warp."""
    c = V(c); R = []; mb.pid += 1
    for k in range(rings + 1):
        t = th[0] + (th[1] - th[0]) * k / rings; row = []
        for i in range(seg + 1):
            ph = phi[0] + (phi[1] - phi[0]) * i / seg
            n = 1 + (rough * (vnoise(2 * math.sin(t) * math.cos(ph) + 3, 2 * math.sin(t) * math.sin(ph) + 2.2 * math.cos(t), int(seed)) - 0.5) * 2 if rough else 0.0)
            p = V((rx * n * math.sin(t) * math.cos(ph), ry * n * math.sin(t) * math.sin(ph), -rz * n * math.cos(t)))
            row.append(fn(c + p) if fn else c + p)
        R.append(row)
    for k in range(rings):
        for i in range(seg):
            mb.face([R[k][i], R[k][i + 1], R[k + 1][i + 1], R[k + 1][i]], mat, [(uvs[0] * i / seg, uvs[1] * k / rings), (uvs[0] * (i + 1) / seg, uvs[1] * k / rings),
                                                                              (uvs[0] * (i + 1) / seg, uvs[1] * (k + 1) / rings), (uvs[0] * i / seg, uvs[1] * (k + 1) / rings)])

def cyl(mb, c, r, h, mat, seg=10, r1=None, cap=True):
    mb.frustum(V(c), V(c) + V((0, 0, h)), r, r if r1 is None else r1, mat, seg=seg, cap0=cap, cap1=cap)

def prism(mb, x0, x1, z0, z1, mo, mi, mt, mb_=None, ends=True, uvk=1.0 / 8):
    """Wedge wall segment between x0..x1 and heights z0..z1: outer face yo(z), inner face yi(z), top, bottom, end caps. Normals outward."""
    po = [V((x0, yo(z0), z0)), V((x1, yo(z0), z0)), V((x1, yo(z1), z1)), V((x0, yo(z1), z1))]
    pi_ = [V((x0, yi(z0), z0)), V((x1, yi(z0), z0)), V((x1, yi(z1), z1)), V((x0, yi(z1), z1))]
    L = math.hypot(z1 - z0, yo(z1) - yo(z0)); a = (x1 - x0)
    mb.oface(po, mo, [(x0 * uvk, z0 / 4.0), (x1 * uvk, z0 / 4.0), (x1 * uvk, z0 / 4.0 + L / 4.0), (x0 * uvk, z0 / 4.0 + L / 4.0)], (0, -1, 0.12))
    mb.oface(pi_, mi, [(x0 * uvk, z0 / 4.0), (x1 * uvk, z0 / 4.0), (x1 * uvk, z0 / 4.0 + L / 4.0), (x0 * uvk, z0 / 4.0 + L / 4.0)], (0, 1, 0.06))
    mb.oface([V((x0, yo(z1), z1)), V((x1, yo(z1), z1)), V((x1, yi(z1), z1)), V((x0, yi(z1), z1))], mt, [(x0 / 8, 0), (x1 / 8, 0), (x1 / 8, 0.7), (x0 / 8, 0.7)], (0, 0, 1))
    if z0 > 0: mb.oface([V((x0, yo(z0), z0)), V((x1, yo(z0), z0)), V((x1, yi(z0), z0)), V((x0, yi(z0), z0))], mi, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, -1))
    if ends:
        for xe, nx in ((x0, -1), (x1, 1)):
            mb.oface([V((xe, yo(z0), z0)), V((xe, yi(z0), z0)), V((xe, yi(z1), z1)), V((xe, yo(z1), z1))], mi, [(0, z0 / 4.0), (0.9, z0 / 4.0), (0.9, z1 / 4.0), (0, z1 / 4.0)], (nx, 0, 0))

# ----------------------------------------------------------------------------- hip roof with upturned eaves
def hip_roof(mb, o, yaw, A, Bh, r, z0, rise, M, lift=1.1, nx=28, ny=18, thick=0.4, tile=4.0, mat=None, under=None, edge=None, horns=False, wadang=True):
    """Chinese hip roof: plan half sizes A x Bh around o (yaw deg), ridge half length r along local x, eave level z0, ridge z0 + rise,
    concave slopes and corners curled up by `lift`. Tile surface, underside board and a fascia edge."""
    F = Frame(o, yaw); mat = mat or M['tiles']; under = under or M['wood_d']; edge = edge or M['red']
    def hz(x, y):
        u = max(abs(y) / Bh, max(abs(x) - r, 0.0) / max(A - r, 1e-3)); u = min(u, 1.0)
        c = (abs(x) / A) * (abs(y) / Bh); return z0 + rise * (1 - u) ** 1.7 + lift * max(0.0, (u - 0.72) / 0.28) ** 2 * c ** 1.3, u
    xs = [A * (-1 + 2 * i / nx) for i in range(nx + 1)]; ys = [Bh * (-1 + 2 * j / ny) for j in range(ny + 1)]
    Pt = [[None] * (ny + 1) for _ in range(nx + 1)]; Uu = [[0] * (ny + 1) for _ in range(nx + 1)]
    for i, x in enumerate(xs):
        for j, y in enumerate(ys): z, u = hz(x, y); Pt[i][j] = F.p(x, y, z); Uu[i][j] = u
    Ls = math.hypot(rise, Bh)
    for i in range(nx):
        for j in range(ny):
            q = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]; pts = [Pt[a][b] for a, b in q]
            uv = [(xs[a] / tile, Uu[a][b] * Ls / tile) for a, b in q]
            mb.oface(pts, mat, uv, (0, 0, 1))
            mb.oface([p - V((0, 0, thick * 0.9)) for p in pts], under, [(xs[a] / 4, ys[b] / 4) for a, b in q], (0, 0, -1))
    for (a, b), (a2, b2) in [(((i, 0), (i + 1, 0))) for i in range(nx)] + [(((i, ny), (i + 1, ny))) for i in range(nx)] + [(((0, j), (0, j + 1))) for j in range(ny)] + [(((nx, j), (nx, j + 1))) for j in range(ny)]:
        p0, p1 = Pt[a][b], Pt[a2][b2]; n = (p0 + p1) / 2 - F.p(0, 0, p0.z)
        mb.oface([p0, p1, p1 - V((0, 0, thick * 0.9)), p0 - V((0, 0, thick * 0.9))], edge, [(0, 0), (1, 0), (1, 1), (0, 1)], (n.x, n.y, 0))
    if r > 0.3:                                                                                           # plain ridge (no curled horns: Warring States)
        rz = z0 + rise
        rod(mb, F.p(-r, 0, rz + 0.1), F.p(r, 0, rz + 0.1), 0.38, M['tiles_d_c'], seg=8)
        if horns:
            for sx in (-1, 1): rod(mb, F.p(sx * r, 0, rz + 0.1), F.p(sx * (r + 0.4), 0, rz + 0.8), 0.28, M['tiles_d_c'], seg=6, r1=0.12)
    if wadang:                                                                                            # half-round eaves tiles (wadang) along the long eaves
        for jj in (0, ny):
            for ii in range(1, nx, 2):
                p0 = Pt[ii][jj]; out = F.Y * (-1 if jj == 0 else 1)
                mb.frustum(p0 - V((0, 0, 0.1)) + out * 0.02, p0 - V((0, 0, 0.1)) + out * 0.16, 0.26, 0.26, M['stone'], seg=7)
    for sx in (-1, 1): hz_ = 0                                                                            # (corner finials)
    return F

def rafters(mb, o, yaw, A, Bh, z, M, step=1.3):
    F = Frame(o, yaw)
    for s_ in (-1, 1):
        for k in range(int(2 * A / step) + 1):
            x = -A + k * step
            if abs(x) <= A: obox(mb, F.p(x, s_ * (Bh - 0.5), z), F.X, F.Y, F.Z, 0.18, 0.36, 0.2, M['white'] if k % 2 else M['red'])

# ----------------------------------------------------------------------------- materials
def materials(P, tx, pre):
    FORM = tuple(P['form'])
    def _k(v): return 'x'.join('%g' % x for x in v) if isinstance(v, (tuple, list)) else '%g' % v
    def C(hexcol, gain=1.0, sm=1.0, form=True, smix=None):
        return _untoon(mat_lit('%sc_%s_%g_%s_%d_%s' % (pre, hexcol.lstrip('#'), gain, _k(sm), form, smix), hexcol, gain=gain, shade_mul=sm, form=FORM if form else None, shade_mix=smix))
    def TX(name, gain=1.0, sm=1.0, form=True, alpha=False, smix=None, glow=None, glow_k=0.0):
        return _untoon(mat_lit('%st_%s_%g_%s_%d_%d_%s_%g' % (pre, name, gain, _k(sm), form, alpha, smix, glow_k), image=tx[name], gain=gain, shade_mul=sm, form=FORM if form else None,
                               alpha=alpha, shade_mix=smix, glow=tx[glow] if glow else None, glow_k=glow_k))
    def E(name, hexcol='#ffffff', k=1.0, image=None, alpha=False): return mat_emit(pre + 'e_' + name, hexcol, image=tx[image] if image else None, strength=k, alpha=alpha)
    def ADD(name, image, rgb, k): return BK._mat_add(pre + 'a_' + name, tx[image], rgb, k)
    M = dict(rammed=TX('rammed', 1.25), rammed_d=TX('rammed_d', 1.15), earth=TX('earth', 0.9, form=False), road=TX('road', 0.95, form=False), bank=TX('bank', 0.85, form=False),
             grass=TX('grass', 0.85, form=False), grass2=TX('grass2', 0.8, form=False), tiles=TX('tiles', 1.5), tiles_d=TX('tiles_d', 1.4), tiles_d_c=C('#3a4058', 1.3),
             canvas=TX('canvas', 1.35), canvas_red=TX('canvas_red', 1.0), hide=TX('hide', 1.3), planks=TX('planks', 1.1), planks_d=TX('planks_d', 1.1),
             water=TX('water', 1.0, form=False, glow='water', glow_k=0.30), silk=TX('silk', 1.2, glow='silk', glow_k=0.10),
             wood=C('#8a5a36', 1.1), wood_d=C('#5a3a24', 1.0), wood_l=C('#b88a56', 1.1), red=C('#b82c20', 1.15), red_d=C('#7a1c1c', 1.1), gold=_glossy(C('#e0b040', 1.3, (1.5, 1.2, 0.8)), (1.0, 0.82, 0.45), 0.35, 0.3),
             iron=_glossy(C('#3a3c48', 1.2), (0.7, 0.75, 0.9), 0.4, 0.3), steel=_glossy(C('#b8c0d0', 1.5), (0.8, 0.88, 1.0), 0.55, 0.2), bronze=_glossy(C('#b8843a', 1.3), (1.0, 0.76, 0.42), 0.4, 0.3),
             stone=C('#9a98a8', 1.1), stone_d=C('#6a6878', 1.0), black=C('#201c28', 1.0), cream=C('#eadcc0', 1.15), white=C('#f0e8d8', 1.2), straw=C('#d8b860', 1.15), straw_d=C('#b08a40', 1.0),
             clay=C('#8a5a40', 1.1), clay_d=C('#5a3a2a', 1.0), jade=C('#3a8a74', 1.2), teal=C('#2a6a7a', 1.1), indigo=C('#2a3470', 1.1), ox=C('#6a4a38', 1.15), ox_d=C('#3a2a22', 1.0), hay=C('#d0b060', 1.2),
             plaster=C('#d8c8a8', 1.1), plaster_d=C('#b0a088', 1.05), leaf=C('#4a7a4a', 1.0), hill=C('#2a2c6a', 0.9, form=False),
             lantern=E('lantern', '#ff8a30', 4.2), lantern_g=E('lantern_g', '#ffd070', 5.5), win=E('win', '#ffb040', 2.6), win_c=E('win_c', '#ffd890', 3.4), gate_glow=E('gate_glow', '#ff9a40', 2.6),
             flame=E('flame', '#e8561c', 1.0), flame_t=E('flame_t', '#b8301a', 1.0), flame_e=E('flame_e', '#e8561c', 1.0), flame_m=E('flame_m', '#ffb238', 1.0), flame_c=E('flame_c', '#fffeec', 1.6), ember=E('ember', '#ff6a20', 2.2),
             skin=C('#d8a47a', 1.15), lacq=C('#4a1a20', 1.0), tiles_g=C('#4a5068', 1.3), rain=mat_emit(pre + 'e_rain', image=tx['rain'], strength=1.0, alpha=True), moon=mat_emit(pre + 'e_moon', image=tx['moon'], strength=3.2, alpha=True),
             moon_h=BK._mat_add(pre + 'a_moonh', tx['glow'], (0.35, 0.54, 0.96), 1.0), sky=D._mat_sky(pre + 'sky', P, tx['sky_' + STATE['area'].upper()], P['sky_k']),
             halo=ADD('halo', 'glow', (1.0, 0.6, 0.28), 1.0), halo_s=ADD('halo_s', 'glow', (1.0, 0.7, 0.35), 0.8), halo_big=ADD('halo_big', 'glow', (1.0, 0.55, 0.24), 0.55),
             pool=ADD('pool', 'pool', (1.0, 0.5, 0.14), 0.9), pool_w=ADD('pool_w', 'pool', (1.0, 0.5, 0.16), 0.55), streak=ADD('streak', 'streak', (1.0, 0.62, 0.3), 1.5), streak_m=ADD('streak_m', 'streak', (1.0, 0.88, 0.6), 1.5),
             mist=BK._mat_add(pre + 'a_mist', tx['glow'], (0.5, 0.42, 0.85), 0.08))
    return M

# ----------------------------------------------------------------------------- build
def build(zone='wall', clear=True):
    scene = bpy.context.scene; P = dict(LIGHTS[zone]); lkey = zone
    STATE.clear(); STATE['P'] = P; STATE['preset'] = zone; STATE['loc'] = 'jimo'; STATE['area'] = zone
    if clear:
        for ob in list(scene.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for ac in list(bpy.data.actions): bpy.data.actions.remove(ac)
    for coll in (bpy.data.meshes, bpy.data.lights, bpy.data.curves, bpy.data.cameras):
        for x in list(coll):
            if x.users == 0: coll.remove(x)
    SET = T._coll('SET', scene); LIG = T._coll('LIGHTS', scene); T._wipe(SET); T._wipe(LIG); STATE['SET'] = SET; STATE['LIGHTS'] = LIG
    for m in list(bpy.data.materials):
        if m.name.startswith(('JM_', 'ink')): bpy.data.materials.remove(m)
    tx = JX.ensure(verbose=False); STATE['tx'] = tx
    w = bpy.data.worlds.get('W_jimo') or bpy.data.worlds.new('W_jimo'); scene.world = w; nt = T._tree(w)
    bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld'); bg.inputs['Color'].default_value = (0, 0, 0, 1); bg.inputs['Strength'].default_value = 0.0
    nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
    MN.setup_render(scene, 'final'); scene.render.threads = 4; scene.frame_start = 1; scene.frame_current = 1
    pre = 'JM_%s_' % lkey; M = materials(P, tx, pre); STATE['M'] = M; STATE['pre'] = pre
    kd = V(P['key_dir']).normalized(); k = max(P['key'])
    d = bpy.data.lights.new('key_sun', 'SUN'); d.color = tuple(x / k for x in P['key']); d.energy = math.pi * k; d.angle = math.radians(P['sun_angle'])
    sun = bpy.data.objects.new('key_sun', d); LIG.objects.link(sun); sun.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler(); sun.location = (-20, -40, 40); STATE['sun'] = sun
    STATE.update(flames=[], marks={}, torches=[])
    Bk = Banks(); STATE['B'] = Bk; cam = CAMS[zone]; STATE['cam'] = cam
    sky_and_ground(Bk, SET, P, M, zone)
    wall_outer(Bk, M, zone)
    if zone in ('wall', 'camp'): gate_tower(Bk, M, zone); city(Bk, M, zone)
    if zone == 'wall': moat_bridge_road(Bk, M); foreground(Bk, M)
    if zone == 'camp': camp(Bk, M)
    if zone == 'holes': holes_inner(Bk, M)
    Bk.flush(SET)
    scene.cycles.use_light_tree = True
    MN._denoise(scene); setup_grade(scene)
    W9._air_comp(scene, P)
    for ob in SET.objects: no_bounce(ob)
    A = dict(cam=dict(cam), zone=zone, marks=dict(STATE['marks'])); STATE['A'] = A
    return A

def make_camera(setup, name='cam'):
    ob = T.make_camera(setup, name); ob.data.clip_end = 600.0; ob.data.dof.use_dof = False; return ob

# ----------------------------------------------------------------------------- sky, hills, ground
def sky_and_ground(Bk, SET, P, M, zone):
    R = 250.0; mb = MB(); seg = 72; els = [-15 + 105 * k / 14 for k in range(15)]
    for i in range(seg):
        for k in range(14):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; e0, e1 = math.radians(els[k]), math.radians(els[k + 1])
            pts = [V((R * math.cos(e) * math.cos(a), R * math.cos(e) * math.sin(a), R * math.sin(e))) for (a, e) in ((a0, e0), (a1, e0), (a1, e1), (a0, e1))]
            mb.face(pts[::-1], M['sky'], [(i / seg, k / 14), ((i + 1) / seg, k / 14), ((i + 1) / seg, (k + 1) / 14), (i / seg, (k + 1) / 14)][::-1])
    STATE['sky_obj'] = _obj(mb, 'sky', SET, shadow=False)
    # the moon: a pale-gold disc + soft halo, facing the camera, placed on the dome
    maz, mel = MOON_DIR[zone]; cam = CAMS[zone]; c0 = V(cam['loc']); d = V((math.cos(math.radians(mel)) * math.cos(math.radians(maz)), math.cos(math.radians(mel)) * math.sin(math.radians(maz)), math.sin(math.radians(mel))))
    mc = c0 + d * 230.0; u = d.cross(V((0, 0, 1))).normalized(); v = u.cross(d).normalized(); rr = 12.5
    mb = MB(); mb.face([mc - u * rr - v * rr, mc + u * rr - v * rr, mc + u * rr + v * rr, mc - u * rr + v * rr][::-1], M['moon'], [(0, 0), (1, 0), (1, 1), (0, 1)][::-1])
    rh = 40.0; mb.face([mc * 0.999 - u * rh - v * rh, mc * 0.999 + u * rh - v * rh, mc * 0.999 + u * rh + v * rh, mc * 0.999 - u * rh + v * rh][::-1], M['moon_h'], [(0, 0), (1, 0), (1, 1), (0, 1)][::-1])
    _obj(mb, 'moon', SET, shadow=False); STATE['moon_dir'] = d
    # ground (grass) and a ring of low hills at the horizon
    g = Bk('ground'); S = 260.0
    if True:                                                              # the moat is cut out of the ground
        flat(g, V((-S, -S, 0)), V((2 * S, 0, 0)), V((0, S + MOAT[0], 0)), M['grass'], (-S / 8, -S / 8, S / 8, -MOAT[0] / 8 * 0 + (S + MOAT[0]) / 8 - S / 8))
        flat(g, V((-S, MOAT[1] + 2.3, 0)), V((2 * S, 0, 0)), V((0, S - MOAT[1] - 2.3, 0)), M['earth'], (-S / 8, 0, S / 8, (S - MOAT[1]) / 8))
    else: flat(g, V((-S, -S, 0)), V((2 * S, 0, 0)), V((0, 2 * S, 0)), M['grass'], (-S / 8, -S / 8, S / 8, S / 8))
    hb = Bk('hills', shadow=False); r = _rnd(7)
    for i in range(26):
        a = 2 * math.pi * i / 26 + r.uniform(-0.1, 0.1); Rr = r.uniform(165, 195); rad = r.uniform(34, 62)
        lumpy(hb, V((Rr * math.cos(a), Rr * math.sin(a), -rad * 0.3)), rad, M['hill'], 50 + i, seg=14, rings=6, rough=0.16, squash=0.42)

# ----------------------------------------------------------------------------- wall
# ----------------------------------------------------------------------------- real flames (layered tongues)
def flame(fb, base, h, s=1.0, lean=(0.0, 0.0), seed=0, n=4, spread=0.35, mats=None):
    """Layered flame: n outer tongues graded tip #b8301a -> edge #e8561c, mid tongues #ffb238, a small core #fffeec (the only part that clips).
    Each tongue is a bent chain of tapering cone segments leaning with `lean` (xy offset at the tip, in D) with a little S wobble. `fb` is a mesh bank
    without shadows. base = V (root centre), h = full height."""
    M = STATE['M']; base = V(base); rr = _rnd(int(abs(base.x * 13 + base.y * 7 + base.z * 3) * 10 + seed) & 0xffff)
    lx, ly = lean; seg = 5
    def tongue(c0, ht, rad, mats_by_t, wob, lx_, ly_, a0):
        pts = []
        for k in range(seg + 1):
            t = k / seg; sw = math.sin(t * 3.1 + a0) * wob * t
            pts.append(c0 + V((lx_ * t ** 1.5 + sw * math.cos(a0), ly_ * t ** 1.5 + sw * math.sin(a0), ht * t)))
        for k in range(seg):
            t0, t1 = k / seg, (k + 1) / seg
            r0 = rad * (1 - t0) ** 0.72 * min(1.0, 0.55 + t0 * 3.0) if t0 > 0 else rad * 0.55; r1 = rad * (1 - t1) ** 0.72 if t1 < 1 else 0.0
            fb.frustum(pts[k], pts[k + 1], r0, r1, mats_by_t(t0), seg=5, cap0=(k == 0), cap1=False)
    ot = lambda t: M['flame_t'] if t > 0.6 else (M['flame_e'] if t > 0.22 else M['flame_m'])
    mt = lambda t: M['flame_c'] if t < 0.01 else (M['flame_m'] if t < 0.6 else M['flame_e'])
    for k in range(n):                                                                       # outer tongues: tall, red-orange, tipped dark red
        a = 2 * math.pi * k / n + rr.uniform(0, 1); d = spread * s * 0.8
        c0 = base + V((d * math.cos(a), d * math.sin(a), 0)); ht = h * rr.uniform(0.72, 1.0)
        tongue(c0, ht, 0.46 * s * (h / (2.2 * s)) ** 0.25, ot, 0.18 * s, lx * ht / h + rr.uniform(-0.15, 0.15) * s, ly * ht / h + rr.uniform(-0.15, 0.15) * s, a)
    for k in range(max(2, n - 1)):                                                           # mid tongues: amber, inside
        a = 2 * math.pi * k / max(2, n - 1) + rr.uniform(0, 1); d = spread * s * 0.35; c0 = base + V((d * math.cos(a), d * math.sin(a), 0.03 * s)); ht = h * rr.uniform(0.55, 0.78)
        tongue(c0, ht, 0.36 * s, lambda t: M['flame_m'] if t < 0.55 else M['flame_e'], 0.12 * s, lx * ht / h * 0.9, ly * ht / h * 0.9, a)
    tongue(base + V((0, 0, 0.04 * s)), h * 0.40, 0.24 * s, lambda t: M['flame_c'] if t < 0.7 else M['flame_m'], 0.05 * s, lx * 0.3, ly * 0.3, 0.0)      # hot core
    for k in range(int(3 + 2 * s)):                                                          # embers
        fb.sphere(base + V((rr.uniform(-0.8, 0.8) * s + lx * 0.7, rr.uniform(-0.8, 0.8) * s + ly * 0.7, rr.uniform(0.9, 1.9) * h)), 0.05 * s, M['ember'], seg=4, rings=3)

def px(p, cam=None):
    """World point -> (x, y) pixel on the 720x1280 frame of the current camera (None if behind)."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; cam = cam or sc.camera; v = world_to_camera_view(sc, cam, Vector(p))
    return (round(v.x * 720), round((1 - v.y) * 1280), round(v.z, 1))

def person(Bk, M, pos, yaw=0.0, pose='stand', s=1.0, robe=None, cup=False, cd=40.0, helmet=True, seed=1):
    """Stand-in soldier / guard (low-poly, 4.6 D tall when standing): robe cone, belt, head with cap or helmet, arms, optional spear / cup.
    poses: stand, spear, cheer (cup raised), sit (on the ground / a log, cup to the mouth), sleep (lying on the side, back to camera)."""
    F = Frame((pos[0], pos[1], pos[2] if len(pos) > 2 else 0.0), yaw); b = Bk('people', hull=T.hull(cd)); robe = robe or M['black']; sk = M['skin']
    P = lambda x, y, z: F.p(x * s, y * s, z * s)
    if pose == 'sleep':
        b.frustum(P(-1.4, 0, 0.55), P(1.5, 0, 0.6), 0.55 * s, 0.5 * s, robe, seg=8)
        b.sphere(P(1.95, 0, 0.62), 0.42 * s, sk, seg=8, rings=5); b.frustum(P(1.95, 0, 0.8), P(2.1, 0, 0.86), 0.46 * s, 0.4 * s, M['black'], seg=8)
        b.frustum(P(-1.4, -0.1, 0.5), P(-2.6, -0.3, 0.35), 0.28 * s, 0.22 * s, M['red_d'], seg=6)
        b.frustum(P(0.6, 0.5, 0.45), P(1.4, 0.55, 0.9), 0.14 * s, 0.12 * s, robe, seg=5)
        return
    zs = 0.0
    if pose == 'sit':
        zs = -1.2
        b.frustum(P(-0.3, 0, 0.2), P(0.9, 0, 0.5), 0.4 * s, 0.34 * s, robe, seg=7); b.frustum(P(0.9, -0.28, 0.45), P(1.5, -0.4, 0.2), 0.2 * s, 0.17 * s, M['red_d'], seg=6)
        b.frustum(P(0.9, 0.28, 0.45), P(1.5, 0.4, 0.2), 0.2 * s, 0.17 * s, M['red_d'], seg=6)
    else:
        b.frustum(P(0, -0.22, 0.05), P(0, -0.22, 1.9), 0.26 * s, 0.2 * s, M['black'], seg=6); b.frustum(P(0, 0.22, 0.05), P(0, 0.22, 1.9), 0.26 * s, 0.2 * s, M['black'], seg=6)
    b.frustum(P(0, 0, 1.6 + zs), P(0, 0, 3.4 + zs), 0.78 * s, 0.5 * s, robe, seg=9)
    b.frustum(P(0, 0, 2.3 + zs), P(0, 0, 2.5 + zs), 0.8 * s, 0.8 * s, M['red'], seg=9, cap0=False, cap1=False)
    b.frustum(P(0, 0, 3.4 + zs), P(0, 0, 3.7 + zs), 0.2 * s, 0.2 * s, sk, seg=6)
    hz = 4.1 + zs; b.sphere(P(0, 0, hz), 0.46 * s, sk, seg=9, rings=6); b.sphere(P(0.2, -0.05, hz + 0.04), 0.1 * s, M['black'], seg=4, rings=3)
    if helmet:
        b.frustum(P(0, 0, hz + 0.16), P(0, 0, hz + 0.62), 0.5 * s, 0.22 * s, M['iron'], seg=9); b.frustum(P(0, 0, hz + 0.62), P(0, 0, hz + 1.0), 0.04 * s, 0.1 * s, M['red'], seg=5)
    else: b.frustum(P(0, 0, hz + 0.2), P(0, 0, hz + 0.55), 0.46 * s, 0.4 * s, M['black'], seg=9)
    if pose in ('cheer', 'sit') and cup:
        sh = P(0.0, -0.75, 3.1 + zs); hand = P(0.35, -1.0, 4.45 + zs) if pose == 'cheer' else P(0.5, -0.3, hz - 0.35)
        J_rod(b, sh, hand, 0.14 * s, robe); b.frustum(hand, hand + V((0, 0, 0.32 * s)), 0.13 * s, 0.22 * s, M['bronze'], seg=6)
        sh2 = P(0.0, 0.75, 3.1 + zs); J_rod(b, sh2, P(0.4, 0.45, 2.0 + zs), 0.14 * s, robe)
    elif pose == 'spear':
        J_rod(b, P(0, -0.75, 3.1), P(0.3, -0.85, 2.3), 0.14 * s, robe); J_rod(b, P(0, 0.75, 3.1), P(0.3, 0.85, 2.3), 0.14 * s, robe)
        J_rod(b, P(0.4, -0.9, 0.0), P(0.4, -0.9, 7.0), 0.07 * s, M['wood']); b.frustum(P(0.4, -0.9, 7.0), P(0.4, -0.9, 7.9), 0.12 * s, 0.0, M['steel'], seg=4)
    else:
        for sy in (-1, 1): J_rod(b, P(0, sy * 0.75, 3.1 + zs), P(0.3, sy * 0.85, 2.0 + zs), 0.14 * s, robe)

def J_rod(mb, a, b, r, mat, seg=5): rod(mb, a, b, r, mat, seg=seg)

def brazier(Bk, M, p, s=1.0, light=0.0, name='br', halo_r=3.2, shadow=False, tall=2.2, lean=(0.0, 0.0)):
    """Bronze / iron brazier on a tripod with a layered flame; point light (1.0, 0.50, 0.18)."""
    p = V(p); w = Bk('wood', hull=0.0); f = Bk('fire', shadow=False); h = Bk('halos', shadow=False)
    for k in range(3):
        a = 2 * math.pi * k / 3 + 0.5; rod(w, p + V((0.7 * s * math.cos(a), 0.7 * s * math.sin(a), 0)), p + V((0.14 * s * math.cos(a), 0.14 * s * math.sin(a), tall * s)), 0.1 * s, M['iron'], seg=5)
    rod(w, p + V((0, 0, tall * s)), p + V((0, 0, (tall + 0.55) * s)), 0.30 * s, M['bronze'], seg=9, r1=0.62 * s)
    rod(w, p + V((0, 0, (tall + 0.5) * s)), p + V((0, 0, (tall + 0.62) * s)), 0.66 * s, M['iron'], seg=9, r1=0.66 * s)
    for k in range(6):
        a = 2 * math.pi * k / 6; f.sphere(p + V((0.4 * s * math.cos(a), 0.4 * s * math.sin(a), (tall + 0.66) * s)), 0.13 * s, M['ember'], seg=4, rings=3)
    c = p + V((0, 0, (tall + 0.66) * s)); flame(f, c, 1.9 * s, 0.62 * s, lean=lean, seed=int(p.x + p.y), n=3, spread=0.3)
    halo(h, c + V((0, 0, 0.8 * s)), halo_r * s, M['halo'])
    if light > 0: lamp(name, c + V((0, 0, 0.5)), light, FIRE, r=0.3, shadow=shadow)
    STATE['torches'].append(tuple(c)); return c

def oil_lamp(Bk, M, p, s=1.0, light=0.0, name='ol', halo_r=1.6, h=3.4):
    """Bronze standing oil lamp (Warring States): three feet, a stem with discs, a shallow dish with one small flame. p = floor point."""
    p = V(p); w = Bk('wood', hull=0.0); f = Bk('lamps', shadow=False); hl = Bk('halos', shadow=False)
    for k in range(3):
        a = 2 * math.pi * k / 3; rod(w, p + V((0.5 * s * math.cos(a), 0.5 * s * math.sin(a), 0.0)), p + V((0.08 * s * math.cos(a), 0.08 * s * math.sin(a), 0.4 * s)), 0.08 * s, M['bronze'], seg=4)
    rod(w, p + V((0, 0, 0.4 * s)), p + V((0, 0, (h - 0.3) * s)), 0.09 * s, M['bronze'], seg=6)
    for z in (0.9, 1.9): rod(w, p + V((0, 0, z * s)), p + V((0, 0, (z + 0.1) * s)), 0.3 * s, M['bronze'], seg=8, r1=0.3 * s)
    rod(w, p + V((0, 0, (h - 0.3) * s)), p + V((0, 0, h * s)), 0.2 * s, M['bronze'], seg=8, r1=0.5 * s)
    c = p + V((0, 0, h * s)); flame(f, c, 0.95 * s, 0.26 * s, seed=int(p.x * 3 + p.y), n=2, spread=0.1)
    halo(hl, c + V((0, 0, 0.35 * s)), halo_r * s, M['halo_s'])
    if light > 0: lamp(name, c + V((0, 0, 0.3)), light, LAMP, r=0.3)
    return c

def lantern(Bk, M, p, s=1.0, light=0.0, name='ln', halo_r=1.8, hang=0.9, floor=None):
    """Kept for the call sites: now a bronze standing oil lamp whose FLAME is at p (stem down to `floor`, else 3 D)."""
    p = V(p); fl = floor if floor is not None else p.z - 3.4 * s
    return oil_lamp(Bk, M, V((p.x, p.y, fl)), s=s, light=light, name=name, halo_r=halo_r, h=(p.z - fl) / s)

def torch_post(Bk, M, p, s=1.0, light=900.0, name='t', halo_r=3.2, shadow=False):
    return brazier(Bk, M, p, s=s * 0.8, light=light, name=name, halo_r=halo_r, shadow=shadow)

def banner(Bk, M, base, h, cloth_w, cloth_h, col, trim, wave=0.0, yaw=0.0, sw=True):
    """Pole with a hanging banner (plain shape, no text): a long swallow-tailed cloth with a trim stripe."""
    w = Bk('wood'); cl = Bk('cloth'); base = V(base); F = Frame(base, yaw)
    rod(w, base, base + V((0, 0, h)), 0.16, M['wood_d'], seg=6); w.sphere(base + V((0, 0, h + 0.25)), 0.3, M['gold'], seg=8, rings=5)
    rod(w, base + V((0, 0, h - 0.3)), F.p(cloth_w + 0.4, 0, h - 0.3), 0.08, M['wood_d'], seg=5)
    n = 8
    for i in range(n):
        x0, x1 = cloth_w * i / n, cloth_w * (i + 1) / n; z0_, z1_ = 0.0, 0.0
        sw0 = math.sin(i * 0.9 + wave) * 0.35 * (i / n); sw1 = math.sin((i + 1) * 0.9 + wave) * 0.35 * ((i + 1) / n)
        top = h - 0.4; bot0 = top - cloth_h; bot1 = bot0
        if sw: bot0 = top - cloth_h * (1 - 0.35 * (i / n)); bot1 = top - cloth_h * (1 - 0.35 * ((i + 1) / n))
        pts = [F.p(x0, sw0, top), F.p(x1, sw1, top), F.p(x1, sw1, bot1), F.p(x0, sw0, bot0)]
        cl.oface(pts, col, [(0, 0)] * 4, F.Y * -1); cl.oface(pts[::-1], col, [(0, 0)] * 4, F.Y)
        tp = [F.p(x0, sw0, top), F.p(x1, sw1, top), F.p(x1, sw1, top - 0.45), F.p(x0, sw0, top - 0.45)]
        cl.oface(tp, trim, [(0, 0)] * 4, F.Y * -1); cl.oface(tp[::-1], trim, [(0, 0)] * 4, F.Y)

def wall_outer(Bk, M, zone):
    """The rammed-earth wall: x -90..90, with the gate passage, parapet of merlons with timber coping, torches, lanterns, banners, buttresses."""
    wl = Bk('wall', hull=T.hull(62.0 if zone != 'camp' else 100.0)); X0, X1 = -95.0, 95.0
    holes = []                                                                                                # (xc, w, h) openings through the whole thickness
    holes.append((0.0, GATE_W * 2, GATE_H))
    if zone == 'holes': holes += [(-14.0, 3.8, 4.8), (-3.0, 3.8, 4.8), (8.0, 3.8, 4.8), (19.0, 3.8, 4.8)]
    holes.sort()
    x = X0
    for (xc, wd_, hh) in holes:
        a, b = xc - wd_ / 2, xc + wd_ / 2
        prism(wl, x, a, 0.0, WH, M['rammed'], M['rammed_d'], M['bank']); prism(wl, a, b, hh, WH, M['rammed'], M['rammed_d'], M['bank']); x = b
    prism(wl, x, X1, 0.0, WH, M['rammed'], M['rammed_d'], M['bank'])
    STATE['holes'] = holes
    # tunnel floors / ceilings + timber lintels and door frames
    wd = Bk('wood', hull=T.hull(62.0))
    for (xc, wd_, hh) in holes:
        a, b = xc - wd_ / 2, xc + wd_ / 2; y0, y1 = yo(hh) - 0.1, yi(hh) + 0.1
        obox(wd, (xc, (y0 + y1) / 2, hh + 0.35), (1, 0, 0), (0, 1, 0), (0, 0, 1), wd_ / 2 + 0.7, (y1 - y0) / 2 + 0.2, 0.42, M['wood_d'], uvk=0.5)
        for sx in (a - 0.35, b + 0.35):
            for ys in (yo(hh * 0.5) - 0.12, yi(hh * 0.5) + 0.12): obox(wd, (sx, ys, hh / 2), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.35, 0.35, hh / 2, M['wood_d'], uvk=0.5)
        if hh > 5:                                                                                            # the gate: closed double doors with studs and iron straps, a glow behind the cracks
            for sgn in (-1, 1):
                obox(wd, (xc + sgn * wd_ / 4, yo(hh * 0.5) + 1.3, hh / 2), (1, 0, 0), (0, 1, 0), (0, 0, 1), wd_ / 4 - 0.04, 0.28, hh / 2 - 0.1, M['planks_d'], uvk=0.5)
                for zz in (hh * 0.22, hh * 0.52, hh * 0.8): obox(wd, (xc + sgn * wd_ / 4, yo(hh * 0.5) + 1.0, zz), (1, 0, 0), (0, 1, 0), (0, 0, 1), wd_ / 4 - 0.05, 0.1, 0.16, M['iron'])
                for ix in range(4):
                    for iz in range(5): wd.sphere((xc + sgn * (0.4 + ix * 0.8), yo(hh * 0.5) + 0.98, 1.0 + iz * 1.6), 0.1, M['bronze'], seg=6, rings=4)
            fl = Bk('fire', shadow=False); flat(fl, V((xc - 0.04, yo(hh * 0.5) + 1.6, 0.4)), V((0.08, 0, 0)), V((0, 0, hh - 0.8)), M['gate_glow'])    # light through the door crack
    # parapet (outer side): merlons of rammed earth with a timber coping, a timber rail on the inner side
    mr = Bk('merlons', hull=T.hull(62.0)); yv = yo(WH) + 0.05
    x = X0 + 1.0
    while x < X1 - 2:
        if abs(x) > GATE_W + 8 or True:
            obox(mr, (x + 1.0, yv + 0.65, WH + 1.2), (1, 0, 0), (0, 1, 0), (0, 0, 1), 1.0, 0.65, 1.2, M['rammed'], uvk=0.2)
            obox(mr, (x + 1.0, yv + 0.65, WH + 2.5), (1, 0, 0), (0, 1, 0), (0, 0, 1), 1.18, 0.82, 0.14, M['wood_d'], uvk=0.4)
        x += 3.4 if zone != 'camp' else 3.4
    for sx in (-1, 1):                                                                                        # tower / end buttresses are skipped: the wall runs off-frame
        pass
    # vertical timber buttress posts on the outer face (every 11 D), with cross-beams: a rammed wall's lacing
    for xb in np.arange(-88, 90, 11.0):
        if abs(xb) < 13: continue
        for z in (3.5, 9.5): obox(wd, (xb, yo(z) - 0.05, z), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.3, 0.14, 0.2, M['wood_d'], uvk=0.5)
    ph = Bk('putlog', shadow=False)                                                                           # putlog holes of the tamping scaffold: dark squares in rows
    for z in (3.0, 7.0, 11.0):
        for xp in np.arange(-93.0, 94.0, 4.0):
            if any(abs(xp - hc) < hw_ / 2 + 1.2 and z < hh_ + 1.6 for hc, hw_, hh_ in holes): continue
            yy = yo(z) - 0.06; flat(ph, V((xp - 0.3, yy, z - 0.3)), V((0.6, 0, 0)), V((0, 0, 0.6)), M['black'])
    for z in (5.0, 10.0):
        for xp in np.arange(-91.0, 92.0, 22.0):                                                               # horizontal timber lacing beams
            obox(wd, (xp, yo(z) - 0.1, z), (1, 0, 0), (0, 1, 0), (0, 0, 1), 6.0, 0.14, 0.16, M['wood_d'], uvk=0.5)
    # torches / lanterns along the wall walk and banners; torches stand just behind the parapet gaps and light the outer face from above
    for xt in (-72, -60, -48, -36, -26, -17, 17, 26, 36, 48, 60, 72):
        if zone == 'camp' and abs(xt) > 40: pass
        c = torch_post(Bk, M, (xt, yo(WH) + 1.4, WH), s=1.5, light=(1500.0 if abs(xt) < 50 else 800.0), name='tw%d' % xt, halo_r=3.4)
        lamp('ww%d' % xt, (xt, yo(6.0) - 5.0, 8.0), 4000.0 if abs(xt) < 50 else 2600.0, (1.0, 0.64, 0.24), r=2.0, shadow=False)                  # warm wash on the wall face
        pl = Bk('wallpools', shadow=False); zc = WH - 5.0; yy = yo(zc) - 0.12                              # warm pool of torch light painted on the wall face
        flat(pl, V((xt - 7.0, yy, zc - 6.5)), V((14.0, 0, 0)), V((0, 0, 13.0)), M['pool'])
    for xl in (-65, -54, -42, -31, 31, 42, 54, 65):
        lantern(Bk, M, (xl, yo(WH) + 0.2, WH + 0.2 + 3.2), s=0.9, light=0.0, hang=0.9)
    for i, xb in enumerate((-58, -44, -30, 30, 44, 58)):
        banner(Bk, M, (xb, yo(WH) + 2.0, WH), 8.5, 3.4, 5.0, M['red'] if i % 2 == 0 else M['teal'], M['gold'], wave=i, yaw=0.0)
    if zone != 'holes':                                                                                       # reflections of the wall torches on the moat are added in moat_bridge_road
        STATE['marks']['wall_torch_x'] = [-72, -60, -48, -36, -26, -17, 17, 26, 36, 48, 60, 72]
    # ground-level wall-base details (outside): rubble, slump stains are in the texture

def gate_tower(Bk, M, zone):
    wd = Bk('tower', hull=T.hull(62.0 if zone != 'camp' else 100.0)); z0 = WH; cz = 0.0; yc = (yo(WH) + yi(WH)) / 2
    X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    obox(wd, (cz, yc, z0 + 0.5), X, Y, Z, 10.2, 4.2, 0.5, M['stone'], uvk=0.3)                               # plinth
    for xp in np.linspace(-8.4, 8.4, 7):                                                                      # red lacquered columns, front and back
        for ys in (-3.4, 3.4): rod(wd, (xp, yc + ys, z0 + 1.0), (xp, yc + ys, z0 + 7.2), 0.42, M['red'], seg=10)
    for ys in (-3.4, 3.4):
        for xp in np.linspace(-8.4, 8.4, 6):
            xm = xp + 1.4
            obox(wd, (xm, yc + ys * 0.94, z0 + 4.1), X, Y, Z, 1.4, 0.16, 3.1, M['planks_d'], uvk=0.5)
        for xm in (-5.6, -2.8, 0.0, 2.8, 5.6):                                                                # warm lit lattice windows
            fl = Bk('tw_glow', shadow=False); flat(fl, V((xm - 0.95, yc + ys * 0.99 - (0.02 if ys < 0 else -0.02), z0 + 2.2)), V((1.9, 0, 0)), V((0, 0, 3.0)), M['win'])
            for k in range(1, 4): obox(wd, (xm - 0.95 + k * 0.475, yc + ys * 1.0 - (0.05 if ys < 0 else -0.05), z0 + 3.7), X, Y, Z, 0.05, 0.06, 1.5, M['wood_d'])
            for zz in (2.2, 3.2, 4.2, 5.2): obox(wd, (xm, yc + ys * 1.0 - (0.05 if ys < 0 else -0.05), z0 + zz), X, Y, Z, 0.95, 0.06, 0.05, M['wood_d'])
    for ys in (-3.4, 3.4): obox(wd, (cz, yc + ys, z0 + 7.4), X, Y, Z, 9.2, 0.4, 0.4, M['red'])
    for xp in np.linspace(-8.4, 8.4, 7):                                                                      # bracket sets under the eaves
        for ys in (-3.7, 3.7):
            obox(wd, (xp, yc + ys, z0 + 7.9), X, Y, Z, 0.6, 0.55, 0.3, M['wood_l']); obox(wd, (xp, yc + ys * 1.12, z0 + 8.3), X, Y, Z, 0.95, 0.5, 0.22, M['wood_l'])
    rf = Bk('roof', hull=T.hull(62.0 if zone != 'camp' else 100.0))
    hip_roof(rf, (cz, yc, z0 + 8.4), 0, 12.8, 6.9, 6.0, 0.0, 3.2, M, lift=1.3)
    rafters(wd, (cz, yc, z0 + 8.5), 0, 12.0, 6.9, 0.0, M)
    # second storey
    z1 = z0 + 11.6
    obox(wd, (cz, yc, z1 - 0.3), X, Y, Z, 8.4, 3.9, 0.35, M['wood'], uvk=0.4)
    for xp in np.linspace(-7.2, 7.2, 5):
        for ys in (-3.0, 3.0): rod(wd, (xp, yc + ys, z1), (xp, yc + ys, z1 + 5.0), 0.38, M['red'], seg=10)
    for ys in (-3.0, 3.0):
        for xm in (-5.4, -1.8, 1.8, 5.4):
            obox(wd, (xm, yc + ys * 0.95, z1 + 2.5), X, Y, Z, 1.7, 0.14, 2.4, M['planks_d'], uvk=0.5)
            fl = Bk('tw_glow', shadow=False); flat(fl, V((xm - 1.15, yc + ys * 0.99 - (0.02 if ys < 0 else -0.02), z1 + 1.1)), V((2.3, 0, 0)), V((0, 0, 2.5)), M['win_c'])
            for k in range(1, 5): obox(wd, (xm - 1.15 + k * 0.46, yc + ys * 1.0 - (0.05 if ys < 0 else -0.05), z1 + 2.35), X, Y, Z, 0.05, 0.06, 1.25, M['wood_d'])
    for sx in (-1, 1): obox(wd, (sx * 7.4, yc, z1 + 2.5), X, Y, Z, 0.2, 3.0, 2.4, M['planks_d'], uvk=0.5)
    obox(wd, (cz, yc - 3.0, z1 + 5.2), X, Y, Z, 7.6, 0.35, 0.35, M['red']); obox(wd, (cz, yc + 3.0, z1 + 5.2), X, Y, Z, 7.6, 0.35, 0.35, M['red'])
    for xp in np.linspace(-7.2, 7.2, 5):
        for ys in (-3.4, 3.4): obox(wd, (xp, yc + ys, z1 + 5.6), X, Y, Z, 0.7, 0.55, 0.3, M['wood_l'])
    hip_roof(rf, (cz, yc, z1 + 5.8), 0, 10.4, 6.0, 4.4, 0.0, 5.2, M, lift=1.5)
    rafters(wd, (cz, yc, z1 + 5.9), 0, 9.6, 6.0, 0.0, M)
    # balcony rail around the lower storey walk, lanterns at both eaves, banners and torches on the platform
    for xl in (-10.4, -5.2, 0.0, 5.2, 10.4):
        lantern(Bk, M, (xl, yc - 5.9, z0 + 7.0), s=1.1, light=(260.0 if abs(xl) < 6 else 0.0), name='tl%d' % int(xl), halo_r=2.4, hang=1.0)
    for xl in (-6.0, 0.0, 6.0): lantern(Bk, M, (xl, yc - 5.0, z1 + 4.9), s=1.0, light=0.0, halo_r=2.2, hang=0.9)
    banner(Bk, M, (-10.0, yc - 2.0, z0 + 1.0), 12.0, 4.2, 6.5, M['red'], M['gold'], wave=0.5)
    banner(Bk, M, (10.0, yc - 2.0, z0 + 1.0), 12.0, 4.2, 6.5, M['teal'], M['gold'], wave=2.0, yaw=0.0)
    for xt in (-13.5, 13.5): torch_post(Bk, M, (xt, yo(WH) + 1.6, WH), s=1.1, light=900.0, name='tt%d' % int(xt), halo_r=3.6)
    for xt in (-7.0, 7.0): torch_post(Bk, M, (xt, yc - 4.6, z0 + 1.0), s=0.9, light=500.0, name='tb%d' % int(xt), halo_r=3.0)

def city(Bk, M, zone):
    """Roofs of Jimo peeking above the wall: houses with tiled hip roofs and lit windows, a drum tower, a granary."""
    r = _rnd(31); rf = Bk('cityroof', hull=T.hull(80.0)); bd = Bk('citybody', hull=T.hull(80.0)); gl = Bk('cityglow', shadow=False)
    X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    def house(cx, cy, w, d, h, rise, yaw=0.0):
        F = Frame((cx, cy, 0), yaw)
        obox(bd, F.p(0, 0, h / 2), F.X, F.Y, F.Z, w / 2, d / 2, h / 2, M['plaster'] if r.random() < 0.6 else M['wood_l'], uvk=0.3)
        hip_roof(rf, (cx, cy, h), yaw, w / 2 + 1.3, d / 2 + 1.3, max(0.0, w / 2 - d / 2), 0.0, rise, M, lift=0.8, nx=14, ny=8)
        for k in range(int(w // 3.2)):
            xx = -w / 2 + 1.6 + k * 3.2; zz = h * 0.55
            if r.random() < 0.8: flat(gl, F.p(xx - 0.5, -d / 2 - 0.03, zz - 0.5), F.X * 1.0, F.Z * 1.2, M['win'])
        return F
    spots = [(-52, 12, 14, 9, 17, 5.5), (-34, 14, 16, 10, 20, 6.0), (-19, 11, 12, 9, 16, 5.0), (19, 12, 14, 9, 18, 5.5), (34, 11, 16, 10, 16, 5.2), (52, 14, 14, 10, 21, 6.0),
             (-70, 15, 14, 10, 18, 5.5), (68, 12, 12, 9, 15, 5.0), (-44, 30, 18, 12, 24, 6.5), (42, 32, 18, 12, 23, 6.5), (0, 40, 20, 14, 26, 7.0), (-8, 20, 12, 8, 19, 5.0), (9, 24, 14, 9, 21, 5.6),
             (-26, 28, 12, 9, 22, 5.5), (26, 26, 12, 9, 21, 5.5)]
    for (cx, cy, w, d, h, rise) in spots: house(cx, cy, w, d, h, rise)
    # the drum tower: three stacked storeys with shrinking roofs; a granary with a tall roof
    def tower(cx, cy, w, floors=3, fh=6.2):
        z = 0.0
        for f in range(floors):
            ww = w * (1.0 - 0.13 * f); obox(bd, (cx, cy, z + fh / 2), X, Y, Z, ww / 2, ww / 2 * 0.8, fh / 2, M['plaster_d'] if f else M['plaster'], uvk=0.3)
            for sx in (-1, 1):
                for sy in (-1, 1): rod(bd, (cx + sx * ww / 2, cy + sy * ww * 0.4, z), (cx + sx * ww / 2, cy + sy * ww * 0.4, z + fh), 0.35, M['red'], seg=8)
            flat(gl, V((cx - 1.2, cy - ww * 0.4 - 0.05, z + fh * 0.3)), V((2.4, 0, 0)), V((0, 0, fh * 0.45)), M['win_c'])
            hip_roof(rf, (cx, cy, z + fh), 0, ww / 2 + 1.8, ww * 0.4 + 1.8, ww / 2 - ww * 0.4, 0.0, 2.2 if f < floors - 1 else 4.4, M, lift=1.1, nx=18, ny=10)
            z += fh + 1.4
        return z
    tower(-22, 36, 13, 4, 6.8); tower(26, 46, 11, 4, 6.4)
    # warm lamp-glow of the town behind the wall
    for (gx, gy, gr) in ((-30, 20, 28), (6, 22, 24), (40, 24, 24)): halo(gl, V((gx, gy, 14)), gr, M['halo_big'])

def moat_bridge_road(Bk, M):
    wt = Bk('water', shadow=False); wz = WATER_Z; x0, x1 = -200.0, 200.0; y0, y1 = MOAT
    flat(wt, V((x0, y0, wz)), V((x1 - x0, 0, 0)), V((0, y1 - y0, 0)), M['water'], (0, 0, (x1 - x0) / 16, (y1 - y0) / 16))
    bk = Bk('banks')
    # sloped banks: outer (toward the camera) y -22 -> -19.5 down to the water, inner y -9.5 -> -7.2 up to the berm
    flat(bk, V((x0, y1 - 0.0, wz)), V((x1 - x0, 0, 0)), V((0, 2.3, 2.2)), M['bank'], (0, 0, 40, 0.6))
    flat(bk, V((x0, y0, 0.0)), V((x1 - x0, 0, 0)), V((0, 2.5, wz)), M['bank'], (0, 0, 40, 0.6))
    pass
    # approach: packed-earth road from the bridge toward the camera
    rd = Bk('road'); flat(rd, V((-5.5, y0 - 0.0, 0.03)), V((11.0, 0, 0)), V((0, -160.0, 0)), M['road'], (0, 0, 11 / 8, 20))
    rd.face([V((-5.5, y1 + 2.3, 0.03)), V((-5.5, yo(0), 0.03)), V((5.5, yo(0), 0.03)), V((5.5, y1 + 2.3, 0.03))][::-1], M['road'], [(0, 0), (0, 1), (1, 1), (1, 0)][::-1])
    # timber bridge: deck, beams, posts, rails, piles
    br = Bk('bridge', hull=T.hull(60.0)); X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    yb0, yb1 = y0 - 0.5, y1 + 2.3
    obox(br, (0, (yb0 + yb1) / 2, 0.12), X, Y, Z, 4.2, (yb1 - yb0) / 2, 0.14, M['planks'], uvk=0.5)
    for sx in (-3.8, -1.3, 1.3, 3.8): obox(br, (sx, (yb0 + yb1) / 2, -0.45), X, Y, Z, 0.28, (yb1 - yb0) / 2, 0.38, M['wood_d'], uvk=0.5)
    for yy in np.linspace(yb0 + 1.5, yb1 - 1.5, 4):
        for sx in (-3.8, 3.8): rod(br, (sx, yy, WATER_Z - 0.5), (sx, yy, 0.0), 0.34, M['wood_d'], seg=7)
        obox(br, (0, yy, -0.2), X, Y, Z, 4.2, 0.22, 0.2, M['wood_d'])
    for sx in (-4.1, 4.1):
        for yy in np.linspace(yb0 + 0.4, yb1 - 0.4, 6):
            rod(br, (sx, yy, 0.2), (sx, yy, 2.2), 0.2, M['red'], seg=7)
        obox(br, (sx, (yb0 + yb1) / 2, 1.9), X, Y, Z, 0.14, (yb1 - yb0) / 2, 0.16, M['red']); obox(br, (sx, (yb0 + yb1) / 2, 1.0), X, Y, Z, 0.1, (yb1 - yb0) / 2, 0.1, M['wood'])
    for yy in (yb0 + 0.4, yb1 - 0.4):
        for sx in (-4.1, 4.1): lantern(Bk, M, (sx, yy, 3.1), s=0.9, light=130.0, name='bl%d%d' % (int(sx), int(yy)), halo_r=1.8, hang=0.4)
    # reflections: a layered streak of every wall torch / tower lantern on the water + the moon's reflection
    st = Bk('streaks', shadow=False); wz2 = wz + 0.03
    for xt in STATE['marks'].get('wall_torch_x', []):
        cam = V(CAMS['wall']['loc']); xs = xt + (xt - cam.x) * (-0.18)                                           # shifts away from the camera axis a little (perspective of a vertical)
        wd_ = 1.2; L = 19.0
        st.face([V((xs - wd_, y1 + 0.05, wz2)), V((xs + wd_, y1 + 0.05, wz2)), V((xs + wd_, y1 - L, wz2)), V((xs - wd_, y1 - L, wz2))], M['streak'], [(0, 0), (1, 0), (1, 1), (0, 1)])
    for xl in (-10.4, -5.2, 0.0, 5.2, 10.4): st.face([V((xl - 1.0, y1 + 0.05, wz2)), V((xl + 1.0, y1 + 0.05, wz2)), V((xl + 1.0, y1 - 16, wz2)), V((xl - 1.0, y1 - 16, wz2))], M['streak'], [(0, 0), (1, 0), (1, 1), (0, 1)])
    mx_ = CAMS['wall']['loc'][0] + math.tan(math.radians(JX.MOON_AZ - 90)) * -(0) + (-0.176) * (y1 - 6 - CAMS['wall']['loc'][1]) * 0.9
    for k, (dx, ww, L) in enumerate(((0.0, 1.7, 12.4), (-2.0, 0.9, 9.0), (2.2, 0.8, 8.0))):
        st.face([V((mx_ + dx - ww, y1 - 0.2, wz2 + 0.01 * k)), V((mx_ + dx + ww, y1 - 0.2, wz2 + 0.01 * k)), V((mx_ + dx + ww, y1 - L, wz2 + 0.01 * k)), V((mx_ + dx - ww, y1 - L, wz2 + 0.01 * k))], M['streak_m'], [(0, 0), (1, 0), (1, 1), (0, 1)])
    # mist over the moat
    for k in range(6): halo(Bk('halos', shadow=False), V((-60 + k * 24, -16, 0.5)), 16.0, M['mist'])

def foreground(Bk, M):
    """Nearest 15 % of the frame: dark grass tufts, a cart wheel leaning on its cart, rocks, a stake with a rope."""
    r = _rnd(5); w = Bk('fgwood', hull=T.hull(14.0)); st = Bk('fgstone', hull=T.hull(14.0)); gr = Bk('tufts')
    def wheel(c, R, yaw_deg, lean=0.0):
        F = Frame(c, yaw_deg); n = 20
        for i in range(n):
            a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
            p0, p1 = F.p(R * math.cos(a0), 0, R * math.sin(a0) + R), F.p(R * math.cos(a1), 0, R * math.sin(a1) + R)
            beam(w, p0, p1, 0.5, 0.7, M['wood_d'], up=(F.Y.x, F.Y.y, F.Y.z))
        for i in range(5): a = math.pi * i / 5; rod(w, F.p(R * math.cos(a), 0, R * math.sin(a) + R), F.p(-R * math.cos(a), 0, -R * math.sin(a) + R), 0.2, M['wood'], seg=6)
        rod(w, F.p(0, -0.6, R), F.p(0, 0.6, R), 0.5, M['wood_d'], seg=10); rod(w, F.p(0, -0.9, R), F.p(0, 0.9, R), 0.22, M['iron'], seg=8)
        for i in range(n): a = 2 * math.pi * (i + 0.5) / n; w.sphere(F.p(R * 1.0 * math.cos(a), 0.0, R * 1.0 * math.sin(a) + R), 0.09, M['iron'], seg=5, rings=3)
    wheel((-8.5, -41.5, 0.0), 1.7, 62.0); wheel((-4.0, -38.8, 0.0), 1.35, 18.0)
    obox(w, (-6.2, -40.2, 0.5), (0.94, 0.34, 0), (-0.34, 0.94, 0), (0, 0, 1), 2.6, 0.2, 0.2, M['wood'])                      # cart shaft on the ground
    for (x, y, s_, sd) in ((6.0, -41.5, 1.4, 3), (10.0, -43.5, 1.0, 5), (-15.5, -38.0, 1.1, 7), (12.5, -37.0, 0.7, 9), (2.5, -37.5, 0.5, 11), (-1.0, -44.0, 0.8, 13)):
        lumpy(st, V((x, y, s_ * 0.3)), s_, M['stone'] if sd % 2 else M['stone_d'], sd, seg=9, rings=6, rough=0.28, squash=0.62)
    for i in range(80):                                                                                        # grass tufts: crossed leaf cards (cones)
        x, y = r.uniform(-30, 30), r.uniform(-52, -31); h_ = r.uniform(0.8, 1.8)
        for k in range(3): a = r.uniform(0, 6.28); gr.frustum(V((x, y, 0)), V((x + 0.4 * math.cos(a), y + 0.4 * math.sin(a), h_)), 0.22, 0.0, M['leaf'] if k % 2 else M['grass2'], seg=3, cap1=False)
    # signal fire basket stake at the roadside + a fallen spear
    torch_post(Bk, M, (11.5, -33.0, 0.0), s=1.3, light=260.0, name='road_torch', halo_r=3.0)
    rod(w, V((-17, -37, 0.25)), V((-9.5, -35.0, 0.45)), 0.1, M['wood'], seg=5); w.frustum(V((-9.5, -35.0, 0.45)), V((-8.4, -34.8, 0.5)), 0.2, 0.0, M['steel'], seg=4)

# --- zones camp / holes follow in jimo_camp.py / jimo_ox.py (imported at the bottom)
def camp(Bk, M): CAMP.camp(sys.modules[__name__], Bk, M)
def holes_inner(Bk, M): OX.holes_inner(sys.modules[__name__], Bk, M)

# ----------------------------------------------------------------------------- CLI
def render_still(zone, draft=False, out=None):
    A = build(zone); sc = bpy.context.scene
    if draft: MN.setup_render(sc, 'preview'); sc.cycles.samples = 6; sc.render.threads = 4
    else: MN.setup_render(sc, 'final'); sc.cycles.samples = 12; sc.render.threads = 4
    cam = make_camera(A['cam']); sc.camera = cam
    os.makedirs(OUT, exist_ok=True)
    path = out or os.path.join(OUT, ('draft_' if draft else 'board_') + {'wall': '1', 'camp': '2', 'holes': '3'}[zone] + '.png')
    w, c = T.render(path); print('RENDER %s %.1f wall s, %.1f cpu s -> %s' % (zone, w, c, path), flush=True)
    return path, w, c

try:
    import jimo_camp as CAMP
    import jimo_ox as OX
except ImportError as e:                                    # the zones are written one after another
    CAMP = OX = None; print('zone modules missing:', e)

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'still':
        render_still(a[1], draft=('draft' in a[2:]))
    elif a and a[0] == 'board':
        import board; board.run()
    else: print(__doc__)

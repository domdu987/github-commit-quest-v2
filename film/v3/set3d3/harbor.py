#!/usr/bin/env python3
"""harbor.py : set of film 3, the Boston waterfront in January 1919 with the molasses tank, as a real 3D Blender set (bpy 5.3, Cycles CPU).

    import harbor as H
    A = H.build("WINTER")              # WINTER | WARM | NOON -> anchors dict (marks, tank, cameras)
    H.set_paint(1, frame=200)          # 0 grey steel with molasses streaks at the seams, 1 painted brown (bottom-up in between)
    H.set_seep(0.8, frame=10)          # glossy seep strips running down from the seams (0 none .. 1 full length)
    H.set_bucket(fill=0.4, frame=10)   # the tin bucket under the bucket seam: fill 0..1 (1 = overflowing), pos, visible, rot
    H.set_flood(0.5, frame=300)        # the molasses wave: 0 none, 0.2 burst at the tank base, 0.5 house-high wave mid street, 1 street full
    pts = H.rivet_points()             # world points on the lower seams (rivet pops)
    cam = H.make_camera(A["cams"]["street_low"])

World: 1 unit = 1 D (head diameter), Z up, street level z = 0. The tank stands at TANK_C = (14.5, 22), radius 13, wall 18 D.
Commercial Street runs from the tank yard toward the camera along -y (cobbles x -5..5, brick sidewalks to +-7.5), the elevated
railway runs along the street over its left half (columns x -6.2 and -0.6, deck z 9) and passes 2 D beside the tank; harbour water
north (y > 42) and east (x > 34) with a moored freighter. Built on the film-2 template v3/set3d2/tower.py: its materials (one hard
key + painted blue-violet shade as emission), mesh builder, ink hulls, render settings, grade, cameras, keying and placeholder
actors are imported, not rewritten. See harbor_API.md.
CLI: python3 harbor.py stills [preset ...] | flood | timing <cam> <preset> | digest <preset> <out.png>"""
import os, sys, math, json, time, random, hashlib
import bpy
import numpy as np
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d2'))
import harbor_tex as HT                                    # noqa: E402
import tower as T                                          # noqa: E402  (template: materials, MB, hulls, render, camera, keys, actors)
from tower import MB, hull, no_bounce, setup_render, setup_grade, make_camera, render, mat_lit, mat_emit   # noqa: E402,F401
WORK = os.path.join(HERE, 'harbor_work')
T.ACT = os.path.join(WORK, 'actors')                       # placeholder sprites are cached in our folder, not the template's
STATE = T.STATE                                            # the template's materials read STATE['P']; one shared dict

# ----------------------------------------------------------------------------- dimensions (D)
TANK_C = (14.5, 22.0); TANK_R = HT.TANK_R; TANK_H = HT.TANK_H; ROOF_Z = TANK_H + 2.3
TH_B = math.atan2(-12.0 - TANK_C[1], 0.0 - TANK_C[0])      # azimuth of the bucket seam (the side facing down the street)
TH_0 = TH_B - HT.SEAM_U / TANK_R                           # azimuth of u = 0 of the tank texture
TRX = (-6.2, -0.6); TR_DECK = 9.0; TR_Y = (-146.0, 142.0); TR_BAY = 12.0     # trestle columns, deck top, extent, bay
STREET = (-5.0, 5.0); WALK = 7.5
LAND_EDGE_Y = 42.0; LAND_EDGE_X = 34.0

def OUT(th): return Vector((math.cos(th), math.sin(th), 0.0))
def TAN(th): return Vector((-math.sin(th), math.cos(th), 0.0))
def wall_pt(th, r=TANK_R, z=0.0): return Vector((TANK_C[0], TANK_C[1], z)) + OUT(th) * r

# ----------------------------------------------------------------------------- presets (same light model as tower.py)
def _kd(travel, elev):
    h = Vector((travel[0], travel[1], 0)).normalized(); e = math.radians(elev)
    return (h.x * math.cos(e), h.y * math.cos(e), -math.sin(e))

PRESETS = {
    'WINTER': dict(key=(1.28, 1.12, 0.52), shade_tint=(0.14, 0.15, 0.45), shade_mix=0.7, key_desat=0.0, key_dir=_kd((0.20, 0.98), 20), sun_elev=20, sun_angle=0.4,
                   shade=(0.08, 0.15, 0.50), lift=(0.004, 0.005, 0.018), form=(0.0, -0.05, 0.22), toon=0.55, sky='winter', pano='winter', sky_k=0.78, pano_k=0.88,
                   water_k=0.82, snow=1.0, night=False, ink='#2a1712', grade_offset=(0.003, 0.002, 0.008), grade_saturation=1.08, bloom_size=0.05),
    'WARM': dict(key=(1.36, 1.08, 0.38), shade_tint=(0.16, 0.14, 0.42), shade_mix=0.7, key_desat=0.0, key_dir=_kd((0.14, 0.99), 37), sun_elev=37, sun_angle=0.7,
                 shade=(0.10, 0.15, 0.46), lift=(0.006, 0.005, 0.016), form=(0.0, -0.05, 0.2), toon=0.55, sky='warm', pano='warm', sky_k=0.82, pano_k=0.9,
                 water_k=0.85, snow=0.45, night=False, ink='#2a1712', grade_offset=(0.004, 0.003, 0.007), grade_saturation=1.06, bloom_size=0.05),
    'NOON': dict(key=(1.48, 1.18, 0.42), shade_tint=(0.15, 0.13, 0.42), shade_mix=0.72, key_desat=0.0, key_dir=_kd((0.03, 1.0), 40), sun_elev=40, sun_angle=0.35,
                 shade=(0.085, 0.14, 0.44), lift=(0.004, 0.004, 0.014), form=(0.0, -0.05, 0.2), toon=0.5, sky='warm', pano='warm', sky_k=0.84, pano_k=0.9,
                 water_k=0.88, snow=0.4, night=False, ink='#2a1712', grade_offset=(0.004, 0.003, 0.007), grade_saturation=1.07, bloom_size=0.05),
}

# ----------------------------------------------------------------------------- materials built on tower.mat_lit
def _relink_art(m, image2, value_name='paint_z', sharp=6.0):
    """Turn a one-image mat_lit into a two-image one: art = mix(image, image2, clamp((paint_z - z_world) * sharp)).
    Value node `value_name` sets the height up to which image2 (the brown paint) covers image (the grey steel)."""
    nt = m.node_tree; N = nt.nodes.new; L = nt.links.new
    tex = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeTexImage'][0]
    targets = [lk.to_socket for lk in list(nt.links) if lk.from_socket == tex.outputs['Color']]
    t2 = N('ShaderNodeTexImage'); t2.image = T._img(image2); t2.interpolation = tex.interpolation
    uv = N('ShaderNodeUVMap'); L(uv.outputs['UV'], tex.inputs['Vector']); L(uv.outputs['UV'], t2.inputs['Vector'])
    geo = N('ShaderNodeNewGeometry'); sep = N('ShaderNodeSeparateXYZ'); L(geo.outputs['Position'], sep.inputs[0])
    val = N('ShaderNodeValue'); val.name = value_name; val.outputs[0].default_value = -1.0
    sub = N('ShaderNodeMath'); sub.operation = 'SUBTRACT'; L(val.outputs[0], sub.inputs[0]); L(sep.outputs['Z'], sub.inputs[1])
    mul_ = N('ShaderNodeMath'); mul_.operation = 'MULTIPLY'; mul_.use_clamp = True; mul_.inputs[1].default_value = sharp; L(sub.outputs[0], mul_.inputs[0])
    mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MIX'; L(mul_.outputs[0], mx.inputs[0]); L(tex.outputs['Color'], mx.inputs[6]); L(t2.outputs['Color'], mx.inputs[7])
    for s in targets: L(mx.outputs[2], s)
    STATE.setdefault('paint_nodes', []).append(val)
    return m

def _add_gloss(m, k=0.35, rough=0.22, tint=(1.0, 0.86, 0.66)):
    """Add a Glossy BSDF to a mat_lit (sun highlight only: the world is black and every set object is hidden from glossy rays)."""
    nt = m.node_tree; out = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeOutputMaterial'][0]
    src = [lk.from_socket for lk in nt.links if lk.to_socket == out.inputs['Surface']][0]
    g = nt.nodes.new('ShaderNodeBsdfGlossy'); g.inputs['Roughness'].default_value = rough; g.inputs['Color'].default_value = (tint[0] * k, tint[1] * k, tint[2] * k, 1)
    ad = nt.nodes.new('ShaderNodeAddShader'); nt.links.new(src, ad.inputs[0]); nt.links.new(g.outputs['BSDF'], ad.inputs[1]); nt.links.new(ad.outputs['Shader'], out.inputs['Surface'])
    return m

# ----------------------------------------------------------------------------- geometry helpers
def _beam(mb, p0, p1, w, mat, h=None):
    """Square-section bar (4-sided prism) between two points."""
    mb.frustum(p0, p1, w * 0.7071, w * 0.7071, mat, seg=4)

def _blob(cx, cy, rx, ry, r, n=9):
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n; k = r.uniform(0.7, 1.15); out.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    return out

def _plane_patch(mb, mat, origin, u, v, nrm, pts2):
    """Polygon given in a plane frame (origin, unit u, unit v) lifted along nrm by 0.02."""
    o = Vector(origin) + Vector(nrm).normalized() * 0.025; u = Vector(u); v = Vector(v)
    mb.oface([o + u * a + v * b for a, b in pts2], mat, [(a / 2, b / 2) for a, b in pts2], nrm)

# ----------------------------------------------------------------------------- the set
def build(preset='WINTER', clear=True):
    """Build the waterfront set into the current scene (collections SET and LIGHTS, world, render settings, grade).
    Returns the anchors dict (harbor_API.md). clear=True removes every object of the scene first."""
    scene = bpy.context.scene; P = dict(PRESETS[preset]); STATE.clear(); STATE['P'] = P; STATE['preset'] = preset
    if clear:
        for ob in list(scene.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for ac in list(bpy.data.actions):
        if ac.users == 0 or ac.name.startswith(('HBR_', 'flood', 'Key', 'bucket', 'seep', 'paint')): bpy.data.actions.remove(ac)
    for me in list(bpy.data.meshes):
        if me.users == 0: bpy.data.meshes.remove(me)
    SET = T._coll('SET', scene); LIGHTS = T._coll('LIGHTS', scene); T._wipe(SET); T._wipe(LIGHTS)
    for m in list(bpy.data.materials):
        if m.name.startswith(('HBR_', 'ink')): bpy.data.materials.remove(m)
    tx = HT.ensure(verbose=False); STATE['tx'] = tx
    w = bpy.data.worlds.get('W_harbor') or bpy.data.worlds.new('W_harbor'); scene.world = w; nt = T._tree(w)
    bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld'); bg.inputs['Color'].default_value = (0, 0, 0, 1); bg.inputs['Strength'].default_value = 0.0
    nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
    setup_render(scene, 'final'); scene.frame_start = 1; scene.frame_current = 1
    pre = 'HBR_' + preset + '_'; FORM = tuple(P['form'])
    def _k(v): return 'x'.join('%g' % x for x in v) if isinstance(v, (tuple, list)) else '%g' % v
    def C(hexcol, gain=1.0, sm=1.0, form=True): return mat_lit('%sc_%s_%g_%s_%d' % (pre, hexcol.lstrip('#'), gain, _k(sm), form), hexcol, gain=gain, shade_mul=sm, form=FORM if form else None)
    def TX(name, gain=1.0, sm=1.0, form=True): return mat_lit('%st_%s_%g_%s_%d' % (pre, name, gain, _k(sm), form), image=tx[name], gain=gain, shade_mul=sm, form=FORM if form else None)
    def E(name, image, k): return mat_emit(pre + 'e_' + name, image=tx[image], strength=k)
    def PAINTM(name, grey, brown): return _relink_art(mat_lit(pre + 'paint_' + name, image=tx[grey], form=FORM), tx[brown])
    def GL(name, hexcol, k=0.35, rough=0.22, gain=1.0): return _add_gloss(mat_lit(pre + 'g_' + name, hexcol, gain=gain, form=FORM, shade_mul=1.0), k, rough, (1.0, 0.92, 0.82))
    M = dict(tank=PAINTM('tank', 'tank_grey', 'tank_brown'), patch=PAINTM('patch', 'tank_grey_patch', 'tank_brown_patch'),
             setts=TX('setts', 1.0, form=False), pavers=TX('pavers', 1.0, form=False), yard=TX('yard', 1.0, form=False), granite=C('#cfc2a8', 0.95),
             girder=TX('girder'), column=TX('column'), green=C('#2f5d40'), tie=C('#5e3c2a', 0.95), rail=C('#4a4450', 1.0, 1.2), slate=TX('slate'), tar=TX('tarroof', 1.0, form=False),
             side_red=TX('side_red'), side_ochre=TX('side_ochre'), cornice=C('#6a4a3e'), chimney=C('#9a4430'), snow=C('#f2f4fa', 0.95, 1.15, form=False),
             iron=C('#3c3034', 1.0, 1.3), wood=C('#7a4a2a'), molasses=GL('molasses', '#601602', 0.025, 0.5, 0.5), seep=GL('seep', '#4a1806', 0.015, 0.5, 0.3), crack=C('#1c0c08', 0.3, 0.5),
             tin=_add_gloss(mat_lit(pre + 'tin', '#b4b8c4', form=FORM), 0.25, 0.3), tin_d=C('#8a8c98'), stable=TX('stable'), stable_side=C('#a63c2c'), white=C('#efe6d4'))
    STATE['M'] = M; STATE['C'] = C
    _ground(SET, M, C, TX, E, P)
    _tank(SET, M, C, TX)
    _trestle(SET, M, C)
    _streets(SET, M, C, TX)
    _yard_props(SET, M, C, TX)
    _harbour(SET, M, C, TX, E, P)
    _midtown(SET, M, C, TX)
    _snow(SET, M, P)
    _seep(SET, M); _bucket(SET, M); _flood(SET, M)
    # painted plate ring + sky dome
    mb = MB(); R = HT.PANO_R; seg = 128
    for i in range(seg):
        a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; u0, u1 = i / seg, (i + 1) / seg
        mb.face([Vector((R * math.cos(a0), R * math.sin(a0), HT.PANO_Z0)), Vector((R * math.cos(a1), R * math.sin(a1), HT.PANO_Z0)), Vector((R * math.cos(a1), R * math.sin(a1), HT.PANO_Z1)), Vector((R * math.cos(a0), R * math.sin(a0), HT.PANO_Z1))],
                mat_emit(pre + 'e_pano', image=tx['pano_' + P['pano']], strength=P['pano_k'], alpha=True), [(u0, 0), (u1, 0), (u1, 1), (u0, 1)])
    pr = mb.obj('plate', SET); pr.visible_shadow = False
    mb = MB(); R = 170.0; seg = 72; els = [-15 + 105 * k / 14 for k in range(15)]
    for i in range(seg):
        for k in range(14):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; e0, e1 = math.radians(els[k]), math.radians(els[k + 1])
            pts = [Vector((R * math.cos(e) * math.cos(a), R * math.cos(e) * math.sin(a), R * math.sin(e) + 6)) for (a, e) in ((a0, e0), (a1, e0), (a1, e1), (a0, e1))]
            uvs = [(i / seg, k / 14), ((i + 1) / seg, k / 14), ((i + 1) / seg, (k + 1) / 14), (i / seg, (k + 1) / 14)]
            mb.face(pts[::-1], E('sky', 'sky_' + P['sky'], P['sky_k']), uvs[::-1])
    sk = mb.obj('sky', SET); sk.visible_shadow = False
    # one hard key
    kd = Vector(P['key_dir']).normalized(); k = max(P['key'])
    d = bpy.data.lights.new('key_sun', 'SUN'); d.color = tuple(x / k for x in P['key']); d.energy = math.pi * k; d.angle = math.radians(P['sun_angle'])
    sun = bpy.data.objects.new('key_sun', d); LIGHTS.objects.link(sun); sun.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler(); sun.location = (20, -40, 40); STATE['sun'] = sun
    setup_grade(scene)
    for ob in SET.objects: no_bounce(ob)
    set_paint(0.0); set_seep(0.6); set_bucket(fill=0.3, visible=True); set_flood(0.0)
    A = anchors(); STATE['A'] = A
    return A

# ----------------------------------------------------------------------------- ground, water, quays
def _ground(SET, M, C, TX, E, P):
    mb = MB()
    for (x0, x1, y0, y1) in ((-150, 6, -150, 150), (6, LAND_EDGE_X, -150, LAND_EDGE_Y)):
        mb.quad((x0, y0, 0), (x1 - x0, 0, 0), (0, y1 - y0, 0), M['yard'], (x0 / 4, y0 / 4, x1 / 4, y1 / 4))
    mb.obj('ground', SET)
    mb = MB()                                                                   # granite quay walls
    mb.box((6, LAND_EDGE_Y - 0.5, -1.6), (LAND_EDGE_X + 0.5, LAND_EDGE_Y, 0.06), M['granite'], tile=(2, 2))
    mb.box((LAND_EDGE_X, -150, -1.6), (LAND_EDGE_X + 0.5, LAND_EDGE_Y, 0.06), M['granite'], tile=(2, 2))
    mb.box((5.5, LAND_EDGE_Y, -1.6), (6.0, 150, 0.06), M['granite'], tile=(2, 2))
    for i in range(14): mb.box((7 + i * 2, LAND_EDGE_Y - 0.25, 0.06), (7.35 + i * 2, LAND_EDGE_Y + 0.1, 0.5), M['iron'])     # bollards
    mb.obj('quays', SET, hull=0.04)
    mb = MB(); seg = 64; R = HT.PANO_R + 2                                       # harbour water (painted)
    for i in range(seg):
        a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg
        pts = [Vector((0, 0, -1.2)), Vector((R * math.cos(a0), R * math.sin(a0), -1.2)), Vector((R * math.cos(a1), R * math.sin(a1), -1.2))]
        mb.face(pts, E('water', 'water', P['water_k']), [(p.x / 24, p.y / 24) for p in pts])
    o = mb.obj('water', SET); o.visible_shadow = False

# ----------------------------------------------------------------------------- the tank
def _tank(SET, M, C, TX):
    cx, cy = TANK_C; R = TANK_R; seg = 120; W = HT.TILE_W
    def ring_pt(i, r, z): th = TH_0 + 2 * math.pi * i / seg; return Vector((cx + r * math.cos(th), cy + r * math.sin(th), z))
    def U(i): return (2 * math.pi * TANK_R * i / seg) / W
    mb = MB()
    zs = [0.0] + [HT.COURSE * c for c in range(1, int(TANK_H / HT.COURSE))] + [TANK_H]
    for z0, z1 in zip(zs, zs[1:]):
        for i in range(seg):
            mb.face([ring_pt(i, R, z0), ring_pt(i + 1, R, z0), ring_pt(i + 1, R, z1), ring_pt(i, R, z1)], M['tank'], [(U(i), z0 / TANK_H), (U(i + 1), z0 / TANK_H), (U(i + 1), z1 / TANK_H), (U(i), z1 / TANK_H)])
    # lap ledges at the horizontal seams, angle rings top and foot
    for zc, dz, dr in [(HT.COURSE * c, 0.07, 0.05) for c in range(1, 6)] + [(TANK_H - 0.08, 0.1, 0.1), (0.12, 0.12, 0.08)]:
        za, zb = zc - dz, zc + dz; ro = R + dr
        for i in range(seg):
            u0, u1 = U(i), U(i + 1)
            mb.face([ring_pt(i, ro, za), ring_pt(i + 1, ro, za), ring_pt(i + 1, ro, zb), ring_pt(i, ro, zb)], M['tank'], [(u0, za / TANK_H), (u1, za / TANK_H), (u1, zb / TANK_H), (u0, zb / TANK_H)])
            mb.face([ring_pt(i, R, zb), ring_pt(i, ro, zb), ring_pt(i + 1, ro, zb), ring_pt(i + 1, R, zb)], M['tank'], [(u0, zb / TANK_H)] * 2 + [(u1, zb / TANK_H)] * 2)
            mb.face([ring_pt(i, R, za), ring_pt(i + 1, R, za), ring_pt(i + 1, ro, za), ring_pt(i, ro, za)], M['tank'], [(u0, za / TANK_H)] * 2 + [(u1, za / TANK_H)] * 2)
    # roof: shallow cone to the vent
    for i in range(seg):
        a, b = ring_pt(i, R + 0.15, TANK_H), ring_pt(i + 1, R + 0.15, TANK_H); c_ = Vector((cx, cy, ROOF_Z))
        mb.face([a, b, c_], M['tank'], [(a.x / W, a.y / W), (b.x / W, b.y / W), (c_.x / W, c_.y / W)])
    mb.obj('tank_shell', SET, hull=0.06)
    # hero patch round the bucket seam (high-resolution copy of the same art, z 0..7, u PW-3..PW+3)
    mb = MB(); n = 16; u0D, u1D = HT.SEAM_U - 3.0, HT.SEAM_U + 3.0
    for i in range(n):
        for (za, zb) in ((0.0, 3.0), (3.0, 6.0), (6.0, 7.0)):
            ua, ub = u0D + (u1D - u0D) * i / n, u0D + (u1D - u0D) * (i + 1) / n; ta, tb = TH_0 + ua / R, TH_0 + ub / R
            pa, pb = wall_pt(ta, R + 0.008), wall_pt(tb, R + 0.008)
            mb.face([pa + Vector((0, 0, za)), pb + Vector((0, 0, za)), pb + Vector((0, 0, zb)), pa + Vector((0, 0, zb))], M['patch'],
                    [(i / n, za / 7), ((i + 1) / n, za / 7), ((i + 1) / n, zb / 7), (i / n, zb / 7)])
    mb.obj('tank_patch', SET)
    # concrete foot ring
    mb = MB(); mb.frustum((cx, cy, -0.05), (cx, cy, 0.35), R + 0.45, R + 0.45, C('#b8ac98', 0.95), seg=seg, cap0=False, cap1=True); mb.obj('tank_foot', SET, hull=0.03)
    # roof railing, vent, top platform; ladder on the street side
    mb = MB()
    for i in range(0, 60):
        th = 2 * math.pi * i / 60; p = Vector((cx, cy, 0)) + OUT(th) * (R - 0.25); zb = TANK_H + (ROOF_Z - TANK_H) * 0.25 / R
        mb.frustum((p.x, p.y, zb), (p.x, p.y, zb + 1.15), 0.035, 0.035, M['iron'], seg=5)
    for zr in (0.6, 1.15):
        for i in range(60):
            a, b = 2 * math.pi * i / 60, 2 * math.pi * (i + 1) / 60; zb = TANK_H + (ROOF_Z - TANK_H) * 0.25 / R + zr
            pa = Vector((cx, cy, zb)) + OUT(a) * (R - 0.25); pb = Vector((cx, cy, zb)) + OUT(b) * (R - 0.25); mb.frustum(pa, pb, 0.03, 0.03, M['iron'], seg=4, cap0=False, cap1=False)
    mb.frustum((cx, cy, ROOF_Z - 0.2), (cx, cy, ROOF_Z + 0.9), 0.8, 0.8, M['iron'], seg=12); mb.frustum((cx, cy, ROOF_Z + 0.9), (cx, cy, ROOF_Z + 1.5), 1.1, 0.1, M['iron'], seg=12)
    thL = TH_B + 0.33; base = wall_pt(thL, R + 0.42); t = TAN(thL)
    for s in (-0.32, 0.32): q = base + t * s; mb.frustum((q.x, q.y, 0.0), (q.x, q.y, TANK_H + 1.3), 0.04, 0.04, M['iron'], seg=5)
    for k in range(int((TANK_H + 1.0) / 0.32)):
        z = 0.3 + k * 0.32; a = base - t * 0.32; b = base + t * 0.32; mb.frustum((a.x, a.y, z), (b.x, b.y, z), 0.025, 0.025, M['iron'], seg=4)
    for z in (2.0, 6.0, 10.0, 14.0, 17.5):
        for s in (-0.32, 0.32): q = base + t * s; w_ = wall_pt(thL, R) + t * s; mb.frustum((q.x, q.y, z), (w_.x, w_.y, z), 0.03, 0.03, M['iron'], seg=4)
    for k in range(9):                                                           # safety cage hoops from 3 D up
        z = 3.0 + k * 1.8; cen = wall_pt(thL, R + 0.75); pts = []
        for j in range(9):
            a = math.pi * j / 8; pts.append(cen + t * (0.55 * math.cos(a)) + OUT(thL) * (0.5 * math.sin(a)) + Vector((0, 0, z)))
        for p0, p1 in zip(pts, pts[1:]): mb.frustum(p0, p1, 0.025, 0.025, M['iron'], seg=4, cap0=False, cap1=False)
    mb.obj('tank_ironwork', SET, hull=0.012)
    # filling pipe from the pier: along the yard on trestles, up the east-south-east wall, over the rim
    thP = -0.96; wp = wall_pt(thP, R + 0.6); pts = [(29.0, 47.0, 0.7), (29.0, 30.0, 0.7), (29.0, wp.y, 0.7), (wp.x, wp.y, 0.7), (wp.x, wp.y, TANK_H + 0.7)]
    wi = wall_pt(thP, R - 1.2); pts += [(wi.x, wi.y, TANK_H + 0.7 + 0.5), (wi.x, wi.y, TANK_H + 0.4)]
    mb = MB()
    for p0, p1 in zip(pts, pts[1:]):
        mb.frustum(p0, p1, 0.32, 0.32, M['iron'], seg=12)
        d = (Vector(p1) - Vector(p0)); L_ = d.length; dn = d.normalized()
        for k in range(int(L_ / 3.0) + 1):
            c_ = Vector(p0) + dn * min(L_, k * 3.0); mb.frustum(c_ - dn * 0.08, c_ + dn * 0.08, 0.42, 0.42, C('#5a4a48'), seg=12)
    for y in range(14, 47, 4):
        if y > LAND_EDGE_Y - 1 and y < 43: continue
        mb.box((28.4, y - 0.1, -1.4 if y > LAND_EDGE_Y else 0), (29.6, y + 0.1, 0.45), M['wood']); mb.box((28.4, y - 0.4, 0.3), (29.6, y + 0.4, 0.4), M['wood'])
    for k in range(6):
        z = 2.5 + k * 3.0; q = wall_pt(thP, R); mb.box((min(q.x, wp.x) - 0.1, min(q.y, wp.y) - 0.1, z - 0.08), (max(q.x, wp.x) + 0.1, max(q.y, wp.y) + 0.1, z + 0.08), M['iron'])
    mb.obj('fill_pipe', SET, hull=0.03)
    STATE['pipe_pts'] = pts

# ----------------------------------------------------------------------------- the elevated railway
def _trestle(SET, M, C):
    mb = MB(); cm = MB(); x0, x1 = TRX; zg0, zg1 = TR_DECK - 1.4, TR_DECK
    ys = [TR_Y[0] + TR_BAY * k for k in range(int((TR_Y[1] - TR_Y[0]) / TR_BAY) + 1)]
    for y in ys:
        for x in (x0, x1):
            cm.box((x - 0.45, y - 0.45, 0), (x + 0.45, y + 0.45, 0.5), M['granite'])
            # latticed column: four faces textured
            lo, hi = (x - 0.3, y - 0.35, 0.5), (x + 0.3, y + 0.35, zg0)
            cm.box(lo, hi, M['column'], tile=(0.6, 2.0))
            cm.box((x - 0.36, y - 0.42, zg0 - 0.6), (x + 0.36, y + 0.42, zg0), M['green'])
            for s in (-1, 1): _beam(mb, (x, y + 0.35 * s, zg0 - 2.2), (x, y + 1.9 * s, zg0), 0.16, M['green'])     # knee braces
        cm.box((x0 - 0.4, y - 0.3, zg0 - 0.2), (x1 + 0.4, y + 0.3, zg1), M['girder'], tile=(6.0, 1.4))          # bent cap
        _beam(mb, (x0 + 0.3, y, 3.2), (x1 - 0.3, y, zg0 - 0.7), 0.14, M['green']); _beam(mb, (x0 + 0.3, y, zg0 - 0.7), (x1 - 0.3, y, 3.2), 0.14, M['green'])
    for x in (x0, x1):                                                                                    # longitudinal plate girders
        y = TR_Y[0]
        while y < TR_Y[1]:
            yb = min(TR_Y[1], y + 6.0); mb.box((x - 0.15, y, zg0), (x + 0.15, yb, zg1), M['girder'], tile=(6.0, 1.4)); y = yb
        mb.box((x - 0.45, TR_Y[0], zg1 - 0.12), (x + 0.45, TR_Y[1], zg1), M['green'])
        mb.box((x - 0.45, TR_Y[0], zg0), (x + 0.45, TR_Y[1], zg0 + 0.12), M['green'])
    mb.obj('trestle_girders', SET, hull=0.05); cm.obj('trestle_columns', SET, hull=0.04)
    dk = MB(); y = TR_Y[0]
    while y < TR_Y[1]:
        dk.box((x0 - 0.8, y, zg1), (x1 + 0.8, y + 0.32, zg1 + 0.22), M['tie']); y += 0.75
    for xr in (-5.4, -4.0, -2.8, -1.4): dk.box((xr - 0.07, TR_Y[0], zg1 + 0.22), (xr + 0.07, TR_Y[1], zg1 + 0.42), M['rail'])
    for xs in (x0 - 0.75, x1 + 0.75):
        y = TR_Y[0]
        while y <= TR_Y[1]: dk.box((xs - 0.05, y - 0.05, zg1 + 0.22), (xs + 0.05, y + 0.05, zg1 + 1.3), M['green']); y += 3.0
        dk.box((xs - 0.06, TR_Y[0], zg1 + 1.22), (xs + 0.06, TR_Y[1], zg1 + 1.32), M['green']); dk.box((xs - 0.04, TR_Y[0], zg1 + 0.72), (xs + 0.04, TR_Y[1], zg1 + 0.8), M['green'])
    dk.obj('trestle_deck', SET, hull=0.025)
    STATE['trestle_bents'] = ys

# ----------------------------------------------------------------------------- the street: sidewalks, houses, warehouses, stable
def _building(mb, rb, M, front_x, y0, y1, depth, h, face, side, sgn, roof):
    """Block whose street front is the plane x = front_x (facing sgn * +x), y0..y1, depth away from the street, eave/parapet h.
    roof 'pitch' (slate, ridge along the street, chimneys) or 'flat' (tar with a parapet)."""
    xb = front_x - sgn * depth; xa = front_x; W = y1 - y0
    fu = (lambda y: (y - y0) / W) if sgn > 0 else (lambda y: (y1 - y) / W)
    mb.oface([(xa, y0, 0), (xa, y1, 0), (xa, y1, h), (xa, y0, h)], face, [(fu(y0), 0), (fu(y1), 0), (fu(y1), 1), (fu(y0), 1)], (sgn, 0, 0))
    for (ya, n_) in ((y0, -1), (y1, 1)):
        mb.oface([(xa, ya, 0), (xb, ya, 0), (xb, ya, h), (xa, ya, h)], side, [(0, 0), (depth / 6, 0), (depth / 6, h / 6), (0, h / 6)], (0, n_, 0))
    mb.oface([(xb, y0, 0), (xb, y1, 0), (xb, y1, h), (xb, y0, h)], side, [(0, 0), (W / 6, 0), (W / 6, h / 6), (0, h / 6)], (-sgn, 0, 0))
    # cornice along the front
    xc0, xc1 = sorted((xa - sgn * 0.3, xa + sgn * 0.45)); rb.box((xc0, y0, h - 0.55), (xc1, y1, h), M['cornice'])
    xm = (xa + xb) / 2; lo_x, hi_x = sorted((xa, xb))
    if roof == 'pitch':
        rz = h + depth * 0.32
        for (xe, n_) in ((lo_x, -1), (hi_x, 1)):
            rb.oface([(xe + 0.3 * n_, y0 - 0.2, h - 0.15), (xe + 0.3 * n_, y1 + 0.2, h - 0.15), (xm, y1 + 0.2, rz), (xm, y0 - 0.2, rz)], M['slate'],
                     [(0, 0), (W / 2, 0), (W / 2, depth / 4), (0, depth / 4)], (n_, 0, 1.6))
        for ya, n_ in ((y0, -1), (y1, 1)): mb.oface([(lo_x, ya, h), (hi_x, ya, h), (xm, ya, rz - 0.05)], side, [(0, 0), (depth / 6, 0), (depth / 12, 0.4)], (0, n_, 0))
        for yc in (y0 + 0.8, y1 - 0.8): rb.box((xm - 0.45, yc - 0.6, rz - 1.0), (xm + 0.45, yc + 0.6, rz + 1.3), M['chimney'])
        return dict(kind='pitch', x=(lo_x, hi_x), y=(y0, y1), h=h, rz=rz, xm=xm)
    rb.box((lo_x, y0, h - 0.4), (hi_x, y1, h - 0.3), M['tar'], tile=(4, 4))
    for (ya, yb_) in ((y0, y0 + 0.3), (y1 - 0.3, y1)): rb.box((lo_x, ya, h - 0.3), (hi_x, yb_, h + 0.35), M['cornice'])
    k = 0
    for yc in np.arange(y0 + 2.0, y1 - 1.0, 5.0):
        k += 1
        if k % 2: rb.box((xm - 0.5, yc - 0.5, h - 0.3), (xm + 0.5, yc + 0.5, h + 1.2), M['chimney'])
    return dict(kind='flat', x=(lo_x, hi_x), y=(y0, y1), h=h - 0.3)

def _streets(SET, M, C, TX):
    mb = MB()
    mb.quad((STREET[0], -150, 0.012), (STREET[1] - STREET[0], 0, 0), (0, 154, 0), M['setts'], (STREET[0] / 2, -75, STREET[1] / 2, 2))
    for (xa, xb, y1) in ((-WALK, -5.15, 6.0), (5.15, WALK, -6.0)):
        mb.box((xa, -150, 0), (xb, y1, 0.15), M['pavers'], tile=(2, 2))
        kx = (-5.15, -5.0) if xa < 0 else (5.0, 5.15); mb.box((kx[0], -150, 0), (kx[1], y1, 0.16), M['granite'], tile=(2, 2))
    mb.obj('street', SET)
    hb = MB(); rb = MB(); roofs = []
    lefts = ['fa_row_a', 'fa_row_b', 'fa_row_c', 'fa_row_d']; rights = ['fa_ware_a', 'fa_ware_b', 'fa_ware_c', 'fa_row_d', 'fa_ware_b']
    tx = STATE['tx']; FM = {}
    def F(nm):
        if nm not in FM: FM[nm] = TX(nm)
        return FM[nm]
    y = 40.0; i = 0
    while y > -150:                                                             # left (west) side: brick rows, pitched roofs
        nm = lefts[i % 4]; w, h = [(f[1], f[2]) for f in HT.FACADES if f[0] == nm][0]
        roofs.append(_building(hb, rb, M, -WALK, y - w, y, 11.0, h, F(nm), M['side_red'], 1, 'pitch')); y -= w; i += 1
    y = -6.0; i = 0
    while y > -150:                                                             # right (east) side: warehouses, flat roofs
        nm = rights[i % 5]; w, h = [(f[1], f[2]) for f in HT.FACADES if f[0] == nm][0]
        roofs.append(_building(hb, rb, M, WALK, y - w, y, 12.0, h, F(nm), M['side_ochre'] if 'ware' in nm else M['side_red'], -1, 'flat')); y -= w; i += 1
    hb.obj('street_houses', SET, hull=0.05); rb.obj('street_roofs', SET, hull=0.05)
    STATE['roofs'] = roofs
    # the stable in the yard (front gable faces the street, -x)
    mb = MB(); x0, x1, y0, y1, e, rz = 12.0, 21.0, -4.5, 4.5, 4.2, 6.5
    mb.oface([(x0, y1, 0), (x0, y0, 0), (x0, y0, e), (x0, 0, rz), (x0, y1, e)], M['stable'], [(0, 0), (1, 0), (1, e / 6.5), (0.5, 1), (0, e / 6.5)], (-1, 0, 0))
    mb.oface([(x1, y0, 0), (x1, y1, 0), (x1, y1, e), (x1, 0, rz), (x1, y0, e)], M['stable_side'], [(0, 0)] * 5, (1, 0, 0))
    for (ya, n_) in ((y0, -1), (y1, 1)): mb.oface([(x0, ya, 0), (x1, ya, 0), (x1, ya, e), (x0, ya, e)], M['stable_side'], [(0, 0)] * 4, (0, n_, 0))
    for (ya, n_) in ((y0 - 0.4, -1), (y1 + 0.4, 1)): mb.oface([(x0 - 0.4, ya, e - 0.25), (x1 + 0.4, ya, e - 0.25), (x1 + 0.4, 0, rz + 0.05), (x0 - 0.4, 0, rz + 0.05)], M['slate'], [(0, 0), (4.5, 0), (4.5, 2.5), (0, 2.5)], (0, n_, 1.4))
    mb.box((x0 - 0.6, -1.2, 0), (x0 - 0.45, -1.0, 1.4), M['wood']); mb.box((x0 - 0.6, 1.0, 0), (x0 - 0.45, 1.2, 1.4), M['wood']); mb.box((x0 - 0.62, -1.2, 1.2), (x0 - 0.43, 1.2, 1.3), M['wood'])   # hitching rail
    mb.obj('stable', SET, hull=0.04)
    STATE['stable'] = dict(x=(x0, x1), y=(y0, y1), eave=e, ridge=rz)

def _yard_props(SET, M, C, TX):
    """Molasses barrels at the tank foot, a dray (wagon) by the stable, crates, a coil of hose; a lamp post on each sidewalk."""
    r = random.Random(61); mb = MB(); bm = C('#8a5232'); hoop = C('#3a3036')
    STATE['barrels'] = []
    for k, (dth, dr) in enumerate(((-0.24, 1.2), (-0.27, 2.2), (-0.21, 2.15), (-0.30, 1.3), (-0.33, 2.0))):
        p = wall_pt(TH_B + dth, TANK_R + dr)
        mb.frustum((p.x, p.y, 0), (p.x, p.y, 0.55), 0.42, 0.48, bm, seg=12, cap0=False); mb.frustum((p.x, p.y, 0.55), (p.x, p.y, 1.1), 0.48, 0.42, bm, seg=12, cap0=False)
        for z in (0.12, 0.98): mb.frustum((p.x, p.y, z), (p.x, p.y, z + 0.07), 0.46, 0.46, hoop, seg=12, cap0=False, cap1=False)
        STATE['barrels'].append(tuple(p))
    p = wall_pt(TH_B - 0.27, TANK_R + 1.75); mb.frustum((p.x - 0.5, p.y, 1.55), (p.x + 0.5, p.y, 1.55), 0.42, 0.42, bm, seg=12)    # one lying on top
    for (x, y) in ((9.5, 0.5), (10.2, -1.8)):                                     # crates
        mb.box((x - 0.5, y - 0.5, 0), (x + 0.5, y + 0.5, 0.9), C('#b07a44'), tile=None)
    dx, dy = 10.2, -8.6                                                           # a dray with two wheels and shafts
    mb.box((dx - 1.0, dy - 2.2, 1.0), (dx + 1.0, dy + 2.2, 1.15), M['wood']); mb.box((dx - 1.0, dy - 2.2, 1.15), (dx - 0.9, dy + 2.2, 1.6), M['wood']); mb.box((dx + 0.9, dy - 2.2, 1.15), (dx + 1.0, dy + 2.2, 1.6), M['wood'])
    for sx in (-1.15, 1.15): mb.frustum((dx + sx - 0.07, dy + 0.4, 0.85), (dx + sx + 0.07, dy + 0.4, 0.85), 0.85, 0.85, C('#c0402c'), seg=16)
    for sx in (-0.6, 0.6): _beam(mb, (dx + sx, dy - 2.2, 1.0), (dx + sx * 0.7, dy - 4.4, 0.9), 0.1, M['wood'])
    for k in range(3): mb.frustum((dx - 0.4 + k * 0.4, dy + 1.0, 1.15), (dx - 0.4 + k * 0.4, dy + 1.0, 1.9), 0.3, 0.3, bm, seg=10)
    for (lx, ly) in ((-6.9, -12.0), (6.9, -24.0), (6.9, -48.0), (-6.9, -40.0)):     # gas lamp posts
        mb.frustum((lx, ly, 0.15), (lx, ly, 5.2), 0.09, 0.07, M['green'], seg=8); mb.box((lx - 0.25, ly - 0.25, 5.2), (lx + 0.25, ly + 0.25, 5.8), C('#e8dcb0')); mb.frustum((lx, ly, 5.8), (lx, ly, 6.15), 0.33, 0.0, M['green'], seg=8)
    mb.obj('yard_props', SET, hull=0.025)

# ----------------------------------------------------------------------------- harbour: pier, freighter
def _harbour(SET, M, C, TX, E, P):
    mb = MB()
    mb.box((24.0, LAND_EDGE_Y, 0.0), (33.0, 47.5, 0.15), C('#8a6a4a'), tile=(2, 2))
    for x in np.arange(24.3, 33.0, 2.0):
        for y in (44.0, 47.2): mb.frustum((x, y, -1.4), (x, y, 0.0), 0.2, 0.2, C('#5a3a2a'), seg=6)
    mb.obj('pier', SET, hull=0.03)
    hb = MB(); y0, y1 = 48.2, 59.0; zt = 7.0; zb = -1.4
    out = [(6.0, 50.0), (8.0, y0), (66.0, y0), (74.0, 51.5), (78.0, 53.6), (74.0, 55.7), (66.0, y1), (8.0, y1), (6.0, 57.2), (5.2, 53.6)]
    for (a, b) in zip(out, out[1:] + out[:1]):
        n_ = Vector((b[1] - a[1], -(b[0] - a[0]), 0)).normalized()
        hb.oface([(a[0], a[1], zb), (b[0], b[1], zb), (b[0], b[1], zt), (a[0], a[1], zt)], TX('hull', 1.0, 1.0), [(a[0] / 70, 0), (b[0] / 70, 0), (b[0] / 70, (zt + 2) / 9), (a[0] / 70, (zt + 2) / 9)], n_)
    hb.oface([(x, y, zt) for (x, y) in out], C('#9a7450'), [(0, 0)] * len(out), (0, 0, 1))
    hb.obj('ship_hull', SET, hull=0.06)
    sb = MB(); hs = TX('ship_house')
    sb.box((8.0, y0 + 0.3, zt), (16.0, y1 - 0.3, zt + 2.2), C('#2a2630')); sb.box((62.0, y0 + 0.6, zt), (70.0, y1 - 0.6, zt + 2.2), C('#2a2630'))
    sb.box((34.0, 50.4, zt), (45.0, 56.8, zt + 3.2), hs, tile=(6, 3)); sb.box((36.0, 51.2, zt + 3.2), (42.5, 56.0, zt + 5.4), hs, tile=(6, 3)); sb.box((35.5, 50.8, zt + 5.4), (43.0, 56.4, zt + 5.7), C('#ead9b8'))
    sb.frustum((47.5, 53.6, zt + 3.0), (47.5, 53.6, zt + 8.0), 1.3, 1.3, C('#c8862e'), seg=14); sb.frustum((47.5, 53.6, zt + 8.0), (47.5, 53.6, zt + 9.5), 1.3, 1.3, C('#262230'), seg=14)
    for (mx, mh) in ((22.0, 23.0), (58.0, 21.0)):
        sb.frustum((mx, 53.6, zt), (mx, 53.6, mh), 0.28, 0.16, C('#8a5a3a'), seg=8); sb.box((mx - 0.15, 51.0, mh - 6), (mx + 0.15, 56.2, mh - 5.8), C('#8a5a3a'))
        _beam(sb, (mx, 53.6, zt + 1.0), (mx + (7 if mx < 40 else -7), 53.6, zt + 5.5), 0.22, C('#8a5a3a'))
    for (hx0, hx1) in ((17.0, 30.0), (50.0, 61.0)): sb.box((hx0, 50.6, zt), (hx1, 56.6, zt + 0.7), C('#3a3440'))     # hatches
    for (ax, ay) in ((10.0, y0), (68.0, y0)): _beam(sb, (ax, ay, zt - 0.2), (ax - 2.0, LAND_EDGE_Y + 0.5, 0.4), 0.08, C('#d8c8a0'))   # mooring lines
    sb.obj('ship_top', SET, hull=0.05)

def _midtown(SET, M, C, TX):
    """Simplified brick blocks behind the street rows and beyond its far end (parallax between the street and the plate)."""
    r = random.Random(77); mb = MB(); rb = MB(); placed = []
    cams = [Vector(c['loc'][:2]) for c in CAMS.values()]
    tries = 0
    while len(placed) < 70 and tries < 4000:
        tries += 1
        x = r.uniform(-120, 33); y = r.uniform(-150, 120)
        if x > -20 and y > -150 and x < 22: continue                          # street rows, street and the tank yard
        if x > 6 and y > 38: continue                                          # water
        if x > 20 and y > -36: continue                                        # tank yard / pier side
        w_, d_ = r.uniform(7, 14), r.uniform(7, 14); h_ = r.uniform(8, 17)
        if any((Vector((x, y)) - c).length < 12 for c in cams): continue
        if any(abs(x - px) < (w_ + pw) / 2 + 1 and abs(y - py) < (d_ + pd) / 2 + 1 for (px, py, pw, pd) in placed): continue
        placed.append((x, y, w_, d_)); wm = M['side_red'] if r.random() < 0.6 else M['side_ochre']
        x0, x1, y0, y1 = x - w_ / 2, x + w_ / 2, y - d_ / 2, y + d_ / 2
        for (xa, ya, xb, yb, nn) in ((x0, y0, x1, y0, (0, -1, 0)), (x1, y0, x1, y1, (1, 0, 0)), (x1, y1, x0, y1, (0, 1, 0)), (x0, y1, x0, y0, (-1, 0, 0))):
            L_ = math.hypot(xb - xa, yb - ya); mb.oface([(xa, ya, 0), (xb, yb, 0), (xb, yb, h_), (xa, ya, h_)], wm, [(0, 0), (L_ / 6, 0), (L_ / 6, h_ / 6), (0, h_ / 6)], nn)
        rb.box((x0, y0, h_ - 0.05), (x1, y1, h_ + 0.4), M['tar'], tile=(4, 4))
        if r.random() < 0.6: rb.box((x - 0.5, y - 0.5, h_), (x + 0.5, y + 0.5, h_ + 1.8), M['chimney'])
    mb.obj('midtown_walls', SET, hull=0.05); rb.obj('midtown_roofs', SET, hull=0.05)
    STATE['midtown'] = placed

# ----------------------------------------------------------------------------- snow patches (roofs, kerbs, ledges)
def _snow(SET, M, P):
    r = random.Random(83); mb = MB(); keep = P['snow']; sc = 0.55 + 0.45 * keep
    for rf in STATE['roofs']:
        y0, y1 = rf['y']
        if rf['kind'] == 'pitch':
            lo_x, hi_x = rf['x']; xm = rf['xm']; h = rf['h']; rz = rf['rz']
            for (xe, n_) in ((lo_x, -1), (hi_x, 1)):
                a = Vector((xe + 0.3 * n_, y0, h - 0.15)); b = Vector((xm, y0, rz)); v = (b - a); L = v.length; v.normalize(); u = Vector((0, 1, 0)); nrm = u.cross(v) if u.cross(v).z > 0 else -u.cross(v)
                for _ in range(4):
                    if r.random() > keep + 0.25: continue
                    cu, cv = r.uniform(1.0, y1 - y0 - 1.0), r.uniform(0.6, L - 0.6)
                    _plane_patch(mb, M['snow'], a, u, v, nrm, _blob(cu, cv, r.uniform(1.0, 2.6) * sc, r.uniform(0.5, 1.4) * sc, r))
                if r.random() < keep + 0.3:                                   # snow line along the eave
                    _plane_patch(mb, M['snow'], a, u, v, nrm, [(0.3, 0.05), (y1 - y0 - 0.3, 0.05), (y1 - y0 - 0.6, 0.45 * sc), (0.6, 0.5 * sc)])
        else:
            lo_x, hi_x = rf['x']; h = rf['h']
            for _ in range(5):
                if r.random() > keep + 0.3: continue
                cx_, cy_ = r.uniform(lo_x + 1.5, hi_x - 1.5), r.uniform(y0 + 1.5, y1 - 1.5)
                _plane_patch(mb, M['snow'], (0, 0, h - 0.29), (1, 0, 0), (0, 1, 0), (0, 0, 1), _blob(cx_, cy_, r.uniform(1.2, 3.2) * sc, r.uniform(1.0, 2.6) * sc, r))
    st = STATE['stable']                                                        # stable roof
    for n_ in (-1, 1):
        a = Vector((st['x'][0] - 0.4, n_ * 4.9, st['eave'] - 0.25)); b = Vector((st['x'][0] - 0.4, 0, st['ridge'] + 0.05)); v = (b - a); L = v.length; v.normalize(); u = Vector((1, 0, 0)); nrm = u.cross(v) if u.cross(v).z > 0 else -u.cross(v)
        _plane_patch(mb, M['snow'], a, u, v, nrm, _blob(4.8, L * 0.55, 3.6 * sc, 1.6 * sc, r, 11))
    # kerb heaps (low mounds) along both kerbs and against the house fronts; patches in the yard
    hm = MB()
    for side in (-1, 1):
        y = -120.0
        while y < (5.0 if side < 0 else -7.0):
            L = r.uniform(1.5, 5.0) * sc; gap = r.uniform(1.0, 6.0) / max(0.3, keep)
            if r.random() < keep + 0.25:
                xk = side * (STREET[1] - 0.35); w_ = r.uniform(0.35, 0.7) * sc; hh = r.uniform(0.18, 0.4) * sc
                pts = [(xk - w_, y), (xk + w_, y), (xk + w_ * 0.7, y + L), (xk - w_ * 0.7, y + L)]
                hm.box((xk - w_, y, 0.0), (xk + w_, y + L, hh), M['snow'])
                hm.box((xk - w_ * 0.6, y + 0.2, hh), (xk + w_ * 0.6, y + L - 0.2, hh + 0.12 * sc), M['snow'])
            if r.random() < keep:
                xw = side * (WALK - 0.4); hm.box((xw - 0.4 * sc, y + 1.0, 0.15), (xw + 0.4 * sc, y + 1.0 + L * 0.8, 0.15 + 0.25 * sc), M['snow'])
            y += L + gap
    for _ in range(int(16 * keep) + 3):                                           # yard / street patches
        cx_, cy_ = r.uniform(-4.5, 30), r.uniform(-60, 8)
        if (Vector((cx_, cy_)) - Vector(TANK_C)).length < TANK_R + 2.5: continue
        if 11 < cx_ < 22 and -5 < cy_ < 5: continue
        if 7.5 < cx_ and cy_ < -6: continue
        _plane_patch(mb, M['snow'], (0, 0, 0.0), (1, 0, 0), (0, 1, 0), (0, 0, 1), _blob(cx_, cy_, r.uniform(0.5, 1.6) * sc, r.uniform(0.4, 1.1) * sc, r))
    # snow on the trestle deck edges and the tank roof rim
    for xs in (TRX[0] - 0.8, TRX[1] + 0.4):
        y = TR_Y[0]
        while y < TR_Y[1]:
            L = r.uniform(2, 8)
            if r.random() < keep + 0.2: mb.box((xs, y, TR_DECK + 0.22), (xs + 0.4, y + L, TR_DECK + 0.32), M['snow'])
            y += L + r.uniform(1, 6)
    for i in range(24):
        if r.random() > keep + 0.3: continue
        th = 2 * math.pi * i / 24 + r.uniform(0, 0.2); dth = r.uniform(0.06, 0.18) * sc; pts = []
        for j in range(7):
            a = th + dth * j / 6; pts.append(Vector((TANK_C[0], TANK_C[1], TANK_H + 0.12)) + OUT(a) * (TANK_R - 0.05))
        for j in range(6, -1, -1):
            a = th + dth * j / 6; rr = TANK_R - r.uniform(0.6, 1.8) * sc; pts.append(Vector((TANK_C[0], TANK_C[1], TANK_H + 0.12 + (TANK_R - rr) * (ROOF_Z - TANK_H) / TANK_R)) + OUT(a) * rr)
        mb.oface(pts, M['snow'], [(0, 0)] * len(pts), (0, 0, 1))
    o = mb.obj('snow_patches', SET); o2 = hm.obj('snow_heaps', SET)

# ----------------------------------------------------------------------------- seep strips, bucket, flood
def _seep(SET, M):
    """Thin glossy molasses strips hanging from the seams (one mesh; shape key 'seep' = full length, basis = collapsed at the seam)."""
    r = random.Random(97); strips = []
    strips.append((TH_B, HT.COURSE - 0.12, HT.COURSE - 0.12 - 0.78, 0.13))                      # the bucket seam: down to just above the bucket rim
    strips.append((TH_B + 0.11 / TANK_R, HT.COURSE * 0.62, 0.95, 0.06))
    for _ in range(46):
        c = r.choice((1, 1, 1, 2, 2, 3)); th = TH_B + r.uniform(-1.0, 1.0); z0 = HT.COURSE * c - 0.12
        strips.append((th, z0, r.uniform(0.4, 1.0 + 0.5 * (3 - c)), r.uniform(0.04, 0.1)))
    for k in (-1, 1):                                                                            # vertical seams next to the bucket seam
        for c in (0, 1):
            off = (c % 2) * HT.PW / 2; th = TH_B + (k * HT.PW + off - (0 if c == 0 else 0)) / TANK_R
            if c == 1: th = TH_B + (HT.PW / 2 * k) / TANK_R
            for _ in range(2):
                z0 = HT.COURSE * c + r.uniform(1.0, 2.6); strips.append((th + 0.12 / TANK_R * r.choice((-1, 1)), z0, r.uniform(0.4, 1.3), r.uniform(0.04, 0.08)))
    me = bpy.data.meshes.new('seep'); vs = []; fs = []; full = []; n = 6
    for (th, z0, L, w) in strips:
        rr = TANK_R + 0.014; t = TAN(th); c = Vector((TANK_C[0], TANK_C[1], 0)) + OUT(th) * rr; b0 = len(vs)
        for j in range(n + 1):
            f = j / n; ww = w * (1.0 - 0.55 * f) + (w * 0.5 if j == n else 0.0)
            for s in (-1, 1):
                pf = c + t * (s * ww / 2) + Vector((0, 0, z0 - L * f)); pb = c + t * (s * ww / 2) + Vector((0, 0, z0 - 0.02 * f))
                vs.append(pb); full.append(pf)
        for j in range(n): a = b0 + 2 * j; fs.append((a, a + 1, a + 3, a + 2))
    me.from_pydata(vs, [], fs); me.update(); me.materials.append(M['seep'])
    ob = bpy.data.objects.new('seep_strips', me); SET.objects.link(ob)
    ob.shape_key_add(name='Basis'); kb = ob.shape_key_add(name='seep')
    for i, p in enumerate(full): kb.data[i].co = p
    # one falling drop between the bucket strip and the bucket
    mb = MB(); dp = wall_pt(TH_B, TANK_R + 0.14, 0.88); mb.sphere(tuple(dp), 0.035, M['seep'], seg=8, rings=5); d = mb.obj('seep_drop', SET); d.scale = (1, 1, 1.8)
    for o in (ob, d): no_bounce(o)
    STATE['seep'] = ob; STATE['drop'] = d; STATE['seep_strips'] = strips

BUCKET_H = 0.72; BUCKET_R0, BUCKET_R1 = 0.30, 0.40
def _bucket(SET, M):
    root = bpy.data.objects.new('bucket_root', None); SET.objects.link(root)
    mb = MB(); tin = M['tin']
    mb.frustum((0, 0, 0.0), (0, 0, BUCKET_H), BUCKET_R0, BUCKET_R1, tin, seg=20, cap0=True, cap1=False)
    for z in (0.18, 0.5): k = z / BUCKET_H; rr = BUCKET_R0 + (BUCKET_R1 - BUCKET_R0) * k + 0.012; mb.frustum((0, 0, z), (0, 0, z + 0.04), rr, rr + 0.003, M['tin_d'], seg=20, cap0=False, cap1=False)
    mb.frustum((0, 0, BUCKET_H - 0.03), (0, 0, BUCKET_H + 0.01), BUCKET_R1 + 0.015, BUCKET_R1 + 0.015, M['tin_d'], seg=20, cap0=False, cap1=False)
    pts = []
    for j in range(11):
        a = math.pi * j / 10; pts.append(Vector((BUCKET_R1 * math.cos(a), 0.0, BUCKET_H + 0.02 + 0.32 * math.sin(a))))
    for p0, p1 in zip(pts, pts[1:]): mb.frustum(p0, p1, 0.012, 0.012, M['iron'], seg=4, cap0=False, cap1=False)
    body = mb.obj('bucket', SET, hull=0.006); body.parent = root
    mb = MB(); mb.frustum((0, 0, -0.01), (0, 0, 0.0), 1.0, 1.0, M['molasses'], seg=20, cap0=False, cap1=True); fill = mb.obj('bucket_fill', SET); fill.parent = root
    mb = MB()                                                                    # overflow: dribbles down the outside and a puddle
    for k in range(6):
        a = 2 * math.pi * k / 6 + 0.3; c = Vector((math.cos(a), math.sin(a), 0)); t = Vector((-math.sin(a), math.cos(a), 0))
        L = 0.3 + 0.07 * k; z1 = BUCKET_H + 0.012
        top = c * (BUCKET_R1 + 0.02); bot = c * (BUCKET_R1 - (BUCKET_R1 - BUCKET_R0) * L / BUCKET_H + 0.02)
        mb.oface([top + t * 0.07 + Vector((0, 0, z1)), top - t * 0.07 + Vector((0, 0, z1)), bot - t * 0.04 + Vector((0, 0, z1 - L)), bot + t * 0.04 + Vector((0, 0, z1 - L))], M['molasses'], [(0, 0)] * 4, c)
    pts = [(0.75 * (1 + 0.15 * math.sin(3 * i)) * math.cos(2 * math.pi * i / 14), 0.75 * (1 + 0.15 * math.sin(3 * i)) * math.sin(2 * math.pi * i / 14) + 0.25, 0.02) for i in range(14)]
    mb.oface(pts, M['molasses'], [(0, 0)] * len(pts), (0, 0, 1))
    ov = mb.obj('bucket_overflow', SET); ov.parent = root
    STATE['bucket'] = dict(root=root, body=body, fill=fill, over=ov)
    for o in (body, fill, ov): no_bounce(o)
    p = wall_pt(TH_B, TANK_R + 0.47); root.location = (p.x, p.y, 0.0); root.rotation_euler = (0, 0, TH_B + math.pi / 2)

FLOOD_X = (-8.4, 34.4); FLOOD_Y = (-62.0, 22.0); FLOOD_STEP = 0.4
def _flood_grid():
    xs = np.arange(FLOOD_X[0], FLOOD_X[1] + 1e-6, FLOOD_STEP); ys = np.arange(FLOOD_Y[0], FLOOD_Y[1] + 1e-6, FLOOD_STEP)
    X, Y = np.meshgrid(xs, ys); return X, Y

def flood_height(u, X=None, Y=None):
    """Height field of the molasses (z per grid point; -0.08 = none) for flood state u in 0..1. A flow coordinate s = distance from
    the burst at the foot of the bucket seam; the front s_f = 2.5 + 49.5 u^0.8; a steep rounded front, a crest Hc (8.1 D at u 0.2,
    7.7 at 0.5, 4.6 at 1) and a layer L (0.9 + 2.6 u) behind it; a tall mound against the tank at the burst while u is small.
    Confined to the street between the house fronts (|x| < 8.1, inside the walls) and the tank yard (y > -4.5), not in the stable."""
    if X is None: X, Y = _flood_grid()
    u = float(max(0.0, min(1.0, u)))
    if u <= 1e-4: return np.full(X.shape, -0.08)
    B = wall_pt(TH_B, TANK_R); s = np.hypot(X - B.x, Y - B.y)
    sf = 2.5 + 49.5 * u ** 0.8; d = sf - s
    Hc = 4.6 + 3.2 * (1 - u) ** 1.5 + 2.0 * math.sin(math.pi * u); Hc = Hc * (1 + 0.07 * np.sin(0.9 * X + 0.31 * Y + 5 * u))
    L = (0.9 + 2.6 * u) * (0.75 + 0.25 * np.clip(1 - s / 60, 0, 1))
    wb = 3.0 + 7.0 * u
    h = np.where(d < 2.0, Hc * np.sqrt(np.clip(d / 2.0, 0, 1)), L + (Hc - L) * np.exp(-((d - 2.0) / wb) ** 2))
    h = h + (6.0 * (1 - u) + 2.0) * min(1.0, u / 0.05) * np.exp(-(s / 5.5) ** 2) * (d > 0)
    h = h + 0.07 * np.sin(0.8 * X + 3 * u) * np.cos(0.6 * Y + 2 * u) * np.clip(h, 0, 1)
    tc = np.hypot(X - TANK_C[0], Y - TANK_C[1])
    mask = ((np.abs(X) < 8.1) | (Y > -4.5)) & (tc > TANK_R - 0.3) & ~((X > 11.6) & (X < 21.4) & (Y > -4.9) & (Y < 4.9)) & (X < LAND_EDGE_X)
    return np.where(mask & (d > 0), np.maximum(h, 0.05), -0.08)

def _flood(SET, M):
    X, Y = _flood_grid(); ny, nx = X.shape
    vs = [(float(X[j, i]), float(Y[j, i]), -0.08) for j in range(ny) for i in range(nx)]
    fs = [(j * nx + i, j * nx + i + 1, (j + 1) * nx + i + 1, (j + 1) * nx + i) for j in range(ny - 1) for i in range(nx - 1)]
    me = bpy.data.meshes.new('flood'); me.from_pydata(vs, [], fs); me.update(); me.materials.append(M['molasses'])
    ob = bpy.data.objects.new('flood', me); SET.objects.link(ob); ob.shape_key_add(name='Basis'); no_bounce(ob)
    mb = MB(); n = 9; pts = []                                                    # the rupture in the wall above the burst
    for j in range(n + 1):
        z = 11.0 * j / n; w_ = 1.3 * math.sin(math.pi * min(1, (j + 0.3) / n)) + 0.2; jag = 0.25 * (1 if j % 2 else -1)
        pts.append((z, -w_ / 2 + jag, w_ / 2 + jag * 0.6))
    for (za, a0, a1), (zb, b0, b1) in zip(pts, pts[1:]):
        quad = [wall_pt(TH_B + a0 / TANK_R, TANK_R + 0.06, za), wall_pt(TH_B + a1 / TANK_R, TANK_R + 0.06, za), wall_pt(TH_B + b1 / TANK_R, TANK_R + 0.06, zb), wall_pt(TH_B + b0 / TANK_R, TANK_R + 0.06, zb)]
        mb.oface(quad, M['crack'], [(0, 0)] * 4, OUT(TH_B))
    ru = mb.obj('tank_rupture', SET); no_bounce(ru)
    STATE['flood'] = ob; STATE['rupture'] = ru; STATE['flood_keys'] = {}; STATE['flood_grid'] = (X, Y)

# ----------------------------------------------------------------------------- animated controls
def _key_value(sock_owner, path, frame, interp='LINEAR', idblock=None):
    sock_owner.keyframe_insert(path, frame=frame)
    for fc in T._fcurves(idblock):
        for kp in fc.keyframe_points:
            if int(round(kp.co.x)) == int(frame): kp.interpolation = interp

def set_paint(state, frame=None, interp='LINEAR'):
    """0: grey steel with dark molasses streaks at the seams (tank_grey); 1: painted brown, no streaks (tank_brown). In between the
    brown climbs the wall from the foot (paint line at z = state x 21.5 - 0.5), as if painted bottom-up. Keys (linear) with frame=N."""
    s = float(state); z = s * (ROOF_Z + 1.2) - 0.5 if s > 0 else -1.0
    if s >= 1: z = 99.0
    STATE['paint'] = s
    for node in STATE.get('paint_nodes', []):
        node.outputs[0].default_value = z
        if frame is not None:
            nt = node.id_data; node.outputs[0].keyframe_insert('default_value', frame=frame)
            for fc in T._fcurves(nt):
                for kp in fc.keyframe_points:
                    if int(round(kp.co.x)) == int(frame): kp.interpolation = interp

def set_seep(amount, frame=None, interp='LINEAR'):
    """Seep strips: 0 none (hidden), 1 full length (0.4 to 2.3 D down from the seams). The drop above the bucket shows from 0.3."""
    a = max(0.0, min(1.0, float(amount))); ob = STATE['seep']; kb = ob.data.shape_keys.key_blocks['seep']; kb.value = a
    if frame is not None: _key_value(kb, 'value', frame, interp, ob.data.shape_keys)
    T._show([ob], a > 0.001, frame); T._show([STATE['drop']], a >= 0.3, frame)
    STATE['seep_a'] = a

def set_bucket(pos=None, fill=None, visible=None, frame=None, rot=None, interp='BEZIER'):
    """The tin bucket (0.72 D tall, rim radius 0.40). pos: world (x, y, z) of its base centre (default bucket_mark); rot: (rx, ry, rz)
    degrees (e.g. lying on its side after the kick: (90, 0, 30)); fill 0..1 molasses level (1 = brim full and overflowing:
    dribbles and a puddle); visible. Keys location/rotation (Bezier), fill (linear), visibility (constant) at frame N."""
    B = STATE['bucket']; root = B['root']
    if pos is not None:
        root.location = tuple(pos)
        if frame is not None: T._key(root, 'location', frame, interp)
    if rot is not None:
        root.rotation_euler = tuple(math.radians(a) for a in rot)
        if frame is not None: T._key(root, 'rotation_euler', frame, interp)
    if fill is not None:
        f = max(0.0, min(1.0, float(fill))); z = 0.035 + (BUCKET_H - 0.05) * f; rr = BUCKET_R0 + (BUCKET_R1 - BUCKET_R0) * z / BUCKET_H - 0.005
        fo = B['fill']; fo.location = (0, 0, z); fo.scale = (rr, rr, 1.0)
        if frame is not None: T._key(fo, 'location', frame, 'LINEAR'); T._key(fo, 'scale', frame, 'LINEAR')
        STATE['bucket_fill'] = f
        T._show([fo], f > 0.01 and STATE.get('bucket_vis', True), frame); T._show([B['over']], f >= 0.999 and STATE.get('bucket_vis', True), frame)
    if visible is not None:
        STATE['bucket_vis'] = bool(visible); f = STATE.get('bucket_fill', 0)
        T._show([B['body']], visible, frame); T._show([B['fill']], visible and f > 0.01, frame); T._show([B['over']], visible and f >= 0.999, frame)

def set_flood(u, frame=None):
    """The molasses flood. u 0: none; ~0.05 the wall bursts (rupture + mound at the foot of the bucket seam); 0.2 an 8 D mound
    spreading round the yard; 0.5 a wave 7.7 D high (above the ground floors) halfway down Commercial Street; 1 the street full
    (layer 2.6 to 3.5 D, crest 4.6 D at 52 D from the burst). Without frame: shows state u now. With frame=N: a shape key per
    distinct u, keyed so that the mesh blends linearly between consecutive keyed states (call in any order)."""
    u = float(max(0.0, min(1.0, u))); ob = STATE['flood']; X, Y = STATE['flood_grid']; nm = 'u%.4f' % u
    kbs = ob.data.shape_keys.key_blocks
    if nm not in kbs:
        h = flood_height(u, X, Y).ravel(); kb = ob.shape_key_add(name=nm, from_mix=False)
        co = np.empty(len(kb.data) * 3); kb.data.foreach_get('co', co); co = co.reshape(-1, 3); co[:, 2] = h; kb.data.foreach_set('co', co.ravel())
    ru = STATE['rupture']; sc = min(1.0, u / 0.08) if u > 0 else 0.0
    if frame is None:
        for kb in kbs[1:]: kb.value = 1.0 if kb.name == nm else 0.0
        ru.hide_render = sc <= 0.0; ru.scale = (1, 1, max(sc, 0.001)); return
    STATE['flood_keys'][int(frame)] = nm
    key = ob.data.shape_keys
    if key.animation_data and key.animation_data.action: bpy.data.actions.remove(key.animation_data.action)
    frames = sorted(STATE['flood_keys'])
    for kb in kbs[1:]:
        for f in frames:
            kb.value = 1.0 if STATE['flood_keys'][f] == kb.name else 0.0; kb.keyframe_insert('value', frame=f)
    for fc in T._fcurves(key):
        for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    ru.scale = (1, 1, max(sc, 0.001)); T._key(ru, 'scale', frame, 'LINEAR'); T._show([ru], sc > 0, frame)

def set_tank_ink(on=True):
    """Ink hull of the tank shell on / off. The hull costs about 5 CPU s per final frame when the wall fills the frame (every camera
    ray crosses its transparent front); seam_insert renders in 19 s without it, 24 s with it. Keep it on whenever the tank's
    silhouette is in frame."""
    for nm in ('tank_shell',):
        for md in STATE['objects'][nm].modifiers: md.show_render = bool(on)

def rivet_points(seams=(1, 2), span_deg=60.0, step=0.5):
    """World points (x, y, z) on the rivet rows of the lower horizontal seams (seam c at z = 3c; two rows 0.14 below and 0.15 above)
    within +-span_deg of the bucket seam, every `step` D along the wall, plus the two rivet columns of the bucket seam (course 0).
    Points sit 0.03 D proud of the wall; the outward normal at a point p is (p - tank axis) with z = 0."""
    pts = []; n = int(math.radians(span_deg) * TANK_R / step)
    for c in seams:
        for dz in (-0.14, 0.15):
            for i in range(-n, n + 1): pts.append(tuple(wall_pt(TH_B + i * step / TANK_R, TANK_R + 0.03, HT.COURSE * c + dz)))
    for dx in (-0.13, 0.13):
        for i in range(11): pts.append(tuple(wall_pt(TH_B + dx / TANK_R, TANK_R + 0.03, 0.3 + i * (HT.COURSE - 0.6) / 10)))
    return pts

# ----------------------------------------------------------------------------- anchors and cameras
_bm = wall_pt(TH_B, TANK_R + 0.47)
BUCKET_MARK = (round(_bm.x, 3), round(_bm.y, 3), 0.0)
def _mk(th, r, t=0.0): p = wall_pt(th, r) + TAN(th) * t; return (round(p.x, 3), round(p.y, 3), 0.0)
HERO_MARK = _mk(TH_B, TANK_R + 1.4, -1.1)
BOSS_MARK = _mk(TH_B, TANK_R + 5.0, 2.6)
WORKER_MARKS = [_mk(TH_B + 0.36, TANK_R + 2.4), _mk(TH_B - 0.42, TANK_R + 3.2), (24.5, 44.5, 0.15)]
KID_MARKS = [(-2.2, -20.0, 0.0), (2.8, -27.0, 0.0), (-3.6, -33.0, 0.0)]
STREET_MARKS = [(0.0, -8.0, 0.0), (1.5, -16.0, 0.0), (-1.0, -24.0, 0.0), (0.5, -36.0, 0.0), (-2.0, -46.0, 0.0)]
SQUARE_MARKS = dict(center=(3.5, 1.0, 0.0), by_stable=(10.5, 0.0, 0.0), street_end=(0.0, -4.0, 0.0), trestle_foot=(-3.2, 2.0, 0.0))

def _cam(loc, look):
    return dict(loc=tuple(round(v, 3) for v in loc), look_at=tuple(round(v, 3) for v in look), lens=22)
CAMS = dict(
    tank_low=_cam(wall_pt(TH_B + 0.15, TANK_R + 3.4, 1.2), wall_pt(TH_B - 0.03, TANK_R, 10.5)),
    base_eye=_cam(wall_pt(TH_B + 0.04, TANK_R + 10.5, 2.6), wall_pt(TH_B - 0.02, TANK_R + 0.6, 2.2)),
    street_low=_cam((1.6, -50.0, 1.2), (10.0, 20.0, 10.0)),
    street_wide=_cam((2.0, -60.0, 22.0), (9.0, 12.0, 6.0)),
    seam_insert=_cam(wall_pt(TH_B + 0.075, TANK_R + 2.5, 2.4), wall_pt(TH_B - 0.01, TANK_R, 2.1)),
    bucket_insert=_cam(wall_pt(TH_B - 0.1, TANK_R + 2.4, 1.05), wall_pt(TH_B, TANK_R + 0.4, 0.75)),
    high_down=_cam(wall_pt(TH_B, TANK_R - 1.0, ROOF_Z + 1.3), (0.5, -26.0, 0.0)),
)
CAM_NOTES = dict(
    tank_low='from the foot of the tank, 1.2 D high, 3.4 D out, looking up the riveted wall past the ladder to the rim (+60 deg)',
    base_eye='eye level (2.6 D) 10.5 D out: hero_mark by the bucket far, boss_mark nearer (depth two-shot), barrels, the trestle on the left',
    street_low='down Commercial Street from 50 D, 1.2 D high between the trestle columns: the deck overhead, warehouses right, row houses left, the tank at the end',
    street_wide='establishing from 24 D up over the west rows: the street, trestle, stable, the tank towering over the houses, harbour and freighter behind',
    seam_insert='close on the bucket seam (vertical seam of the lowest course meeting the first horizontal seam) with the seep strips',
    bucket_insert='close and low on the bucket under the drip at the foot of the wall',
    high_down='from the tank roof at the street side, over the rim, down onto the yard and Commercial Street (-35 deg)',
)

def anchors():
    P = STATE['P']; kd = Vector(P['key_dir']).normalized()
    return dict(
        hero_mark=HERO_MARK, boss_mark=BOSS_MARK, bucket_mark=BUCKET_MARK, worker_marks=list(WORKER_MARKS), kid_marks=list(KID_MARKS),
        street_marks=list(STREET_MARKS), square_marks=dict(SQUARE_MARKS),
        tank=dict(center=(TANK_C[0], TANK_C[1], 0.0), radius=TANK_R, wall_top=TANK_H, roof_apex=ROOF_Z, courses=[HT.COURSE * c for c in range(int(TANK_H / HT.COURSE) + 1)],
                  bucket_seam_azimuth_deg=round(math.degrees(TH_B), 3), plates_round=HT.NPL, plate_width=round(HT.PW, 3),
                  ladder_azimuth_deg=round(math.degrees(TH_B + 0.33), 3), pipe=[tuple(round(c, 3) for c in p) for p in STATE['pipe_pts']],
                  burst=tuple(round(c, 3) for c in wall_pt(TH_B, TANK_R))),
        trestle=dict(column_x=TRX, deck_top=TR_DECK, girder_bottom=TR_DECK - 1.4, bents_y=list(STATE['trestle_bents']), y=TR_Y),
        street=dict(cobbles_x=STREET, house_fronts_x=(-WALK, WALK), sidewalk_top=0.15, y_end=4.0),
        stable=dict(STATE['stable']), harbour=dict(quay_y=LAND_EDGE_Y, quay_x=LAND_EDGE_X, water_z=-1.2, ship_x=(5.2, 78.0), ship_y=(48.2, 59.0), deck_z=7.0),
        key_dir=tuple(kd), preset=STATE['preset'], sun_elevation_deg=P['sun_elev'],
        key_note='the sun is behind the street cameras at screen-left (south-south-west): the warehouse fronts (east side) and the street side of the tank are lit, the west rows face away and shade the street, shadows fall forward-right',
        cams={k: dict(v) for k, v in CAMS.items()}, cam_notes=dict(CAM_NOTES),
        render=dict(samples_final=12, resolution=(720, 1280), threads=2, sun_angle_deg=P['sun_angle'], key=P['key'], shade=P['shade'], lift=P['lift'], toon=P['toon']))

# ----------------------------------------------------------------------------- placeholder actors (stills and tests only)
T.PH.update(
    hero=('beach_kid', dict(yaw=-0.3, expr='determined', arm_r='down', arm_l='down', legs='stand'), 2.4),
    foreman=('boss', dict(yaw=0.35, head_roll=-4, expr='smug', arm_l='down', arm_r='hip', legs='stand'), 3.1),
    worker=('clerk', dict(yaw=0.25, expr='neutral', arm_l='down', arm_r='down', legs='stand'), 3.0),
    worker_b=('senior_b', dict(yaw=-0.2, expr='neutral', arm_l='down', arm_r='down', legs='stand'), 2.9),
    kid=('beach_kid', dict(yaw=0.3, expr='happy', arm_r='down', arm_l='down', legs='stand'), 2.1))
placeholder_actor = T.placeholder_actor

def stage_placeholders(A, where, cam_loc):
    """'base': hero (the boy) at hero_mark by the bucket, foreman at boss_mark, a worker; 'street': three kids at kid_marks, two
    workers on street_marks; 'none'. Cards face the camera and lean back for high cameras (template rule)."""
    T._clear_actors()
    if where == 'none': return []
    if where == 'base': spots = [('hero', A['hero_mark']), ('foreman', A['boss_mark']), ('worker', A['worker_marks'][0])]
    else: spots = [('kid', A['kid_marks'][0]), ('kid', A['kid_marks'][1]), ('kid', A['kid_marks'][2]), ('worker', A['street_marks'][1]), ('worker_b', A['street_marks'][3])]
    out = []
    for i, (role, mk) in enumerate(spots):
        d = Vector(cam_loc) - Vector(mk); el = math.degrees(math.atan2(d.z - 1.5, math.hypot(d.x, d.y)))
        out.append(placeholder_actor(role, mk, face_to=cam_loc, tilt=max(0.0, el - 35) * 0.6, name='actor_%s_%d' % (role, i)))
    return out

STAGING = dict(tank_low='base', base_eye='base', street_low='street', street_wide='street', seam_insert='none', bucket_insert='none', high_down='street')

# ----------------------------------------------------------------------------- CLI
def _load(): return ' '.join('%.2f' % v for v in os.getloadavg())

def cli_stills(presets, quality='preview', outdir=None, cams=None):
    outdir = outdir or os.path.join(WORK, 'stills'); os.makedirs(outdir, exist_ok=True)
    for pr in presets:
        A = build(pr); sc = bpy.context.scene; setup_render(sc, quality)
        set_paint(0.0 if pr == 'WINTER' else 1.0); set_seep(0.7); set_bucket(fill=0.45)
        for nm, cs in A['cams'].items():
            if cams and nm not in cams: continue
            make_camera(cs); stage_placeholders(A, STAGING[nm], cs['loc'])
            w, c = render(os.path.join(outdir, '%s_%s.png' % (pr, nm))); print('%s %s: %.1f s wall, %.1f s cpu, load %s' % (pr, nm, w, c, _load()), flush=True)

def cli_flood(preset='NOON', us=(0.2, 0.5, 1.0), cams=('street_low', 'street_wide', 'high_down'), quality='preview'):
    outdir = os.path.join(WORK, 'flood'); os.makedirs(outdir, exist_ok=True)
    A = build(preset); sc = bpy.context.scene; setup_render(sc, quality); set_paint(1.0); set_seep(1.0); set_bucket(fill=1.0)
    for u in us:
        set_flood(u)
        for nm in cams:
            cs = A['cams'][nm]; make_camera(cs); stage_placeholders(A, 'street' if nm != 'base_eye' else 'none', cs['loc'])
            w, c = render(os.path.join(outdir, 'flood_%s_u%03d.png' % (nm, int(u * 100)))); print('flood %.2f %s: %.1f s, %.1f cpu' % (u, nm, w, c), flush=True)

def cli_timing(cam='street_low', preset='WINTER', n=3):
    A = build(preset); sc = bpy.context.scene; setup_render(sc, 'final'); set_seep(0.7)
    cs = A['cams'][cam]; cobj = make_camera(cs); stage_placeholders(A, STAGING[cam], cs['loc'])
    print('final: 720x1280, %d samples, threads %d; load %s' % (sc.cycles.samples, sc.render.threads, _load()))
    res = []
    for i in range(n):
        cobj.location.x += 0.02
        w, c = render(os.path.join(WORK, 'timing_%s_%s_%d.png' % (preset, cam, i))); res.append((w, c)); print('frame %d: %.2f s wall, %.2f s cpu, load %s' % (i, w, c, _load()), flush=True)
    return res

def digest():
    """Digest of object names, transforms, vertices, UVs, materials, shape keys and anchors (determinism check)."""
    h = hashlib.sha1()
    for ob in sorted(bpy.context.scene.objects, key=lambda o: o.name):
        h.update(ob.name.encode()); h.update(repr([round(x, 5) for x in ob.matrix_world.col[0]] + [round(x, 5) for c in ob.matrix_world.col for x in c]).encode())
        if ob.type == 'MESH':
            me = ob.data; co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', co); h.update(np.round(co, 5).tobytes())
            if me.uv_layers: uv = np.empty(len(me.uv_layers[0].data) * 2); me.uv_layers[0].data.foreach_get('uv', uv); h.update(np.round(uv, 5).tobytes())
            h.update(repr([m.name if m else '' for m in me.materials]).encode())
            if me.shape_keys:
                for kb in me.shape_keys.key_blocks:
                    co = np.empty(len(kb.data) * 3); kb.data.foreach_get('co', co); h.update(np.round(co, 5).tobytes())
    h.update(json.dumps(STATE.get('A', {}), sort_keys=True, default=str).encode())
    return h.hexdigest()

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stills'; arg = sys.argv[2:]
    if cmd == 'stills': cli_stills(arg or ['WINTER', 'WARM', 'NOON'])
    elif cmd == 'flood': cli_flood(*(arg[:1] or []))
    elif cmd == 'timing': cli_timing(*(arg[:2] if arg else []))
    elif cmd == 'digest':
        A = build(arg[0] if arg else 'WINTER'); set_flood(0.5); print('digest', digest())
        if len(arg) > 1:
            sc = bpy.context.scene; setup_render(sc, 'preview'); make_camera(A['cams']['street_low']); render(arg[1])
    else: print(__doc__)

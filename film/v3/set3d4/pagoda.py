#!/usr/bin/env python3
"""pagoda.py : set of film 4 ("the drunk pagoda"), an old-Japan temple town with the five-storey wooden pagoda and the master
builder's rigid tower, as a real 3D Blender set (bpy 5.3, Cycles CPU).

    import pagoda as G
    A = G.build("DAY")                 # DAY | SUNSET | NIGHT | DAWN -> anchors dict (marks, pagoda, tower, cameras)
    G.set_sway(1.0, phase, frame=10)   # snake dance of the five storeys (amp in D at the top storey; adjacent storeys opposite)
    G.set_cutaway(True)                # hide the front walls / front roof quarters: the hanging central pillar is visible
    G.set_pillar_swing(4.0, frame=10)  # pendulum swing of the shinbashira about its chain (deg, + swings the foot toward +x)
    G.set_crack(2, frame=10); G.set_plaster(1)          # crack decal at the tower joint 0..3, plaster patches 0..2
    G.set_collapse(0.6, frame=40)      # the rigid tower snaps in the middle and its top half falls east (0..1), dust and timbers
    G.set_quake(1.0, frame=12)         # loose props: hanging lanterns and wind bells swing, loose roof tiles hop
    cam = G.make_camera(A["cams"]["two_buildings"])

World: 1 unit = 1 D (head diameter), Z up, ground z = 0. The pagoda stands at (0, 0) on a stone platform (top z 0.9), its front
(doors, the approach path, the gate) faces -y. The master's tower stands at (14, 0), 14 D east. Both are inside a walled temple
courtyard (gravel, x -16..28, y -32..18) whose gate (x 0, y -32) opens onto the town street running south (-y) between two rows of
machiya. Built on the film-2/3 template v3/set3d2/tower.py: its materials (one hard key + painted blue-violet shade as emission),
mesh builder, ink hulls, render settings, grade, cameras, keying and placeholder actors are imported, not rewritten.
See pagoda_API.md.
CLI: python3 pagoda.py stills [preset ...] | tests | timing <cam> <preset> | final [preset] | digest <preset>"""
import os, sys, math, json, time, random, hashlib
import bpy
import numpy as np
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d2'))
import pagoda_tex as PT                                    # noqa: E402
import tower as T                                          # noqa: E402  (template: materials, MB, hulls, render, camera, keys, actors)
from tower import MB, no_bounce, setup_render, setup_grade, make_camera, render, mat_lit, mat_emit   # noqa: E402,F401
WORK = os.path.join(HERE, 'pagoda_work')
T.ACT = os.path.join(WORK, 'actors')                       # placeholder sprites are cached in our folder, not the template's
STATE = T.STATE

# ----------------------------------------------------------------------------- dimensions (D)
PLAT_HW = 5.2; PLAT_Z = 0.9                                 # stone platform half width and top
#            half width, base z, wall height, eave overhang
STOREYS = [(3.0, 0.9, 3.0, 2.25), (2.7, 5.1, 2.0, 2.1), (2.4, 8.3, 1.9, 2.0), (2.1, 11.4, 1.8, 1.9), (1.8, 14.4, 1.7, 1.9)]
GAP_Z = 1.2                                                 # wall top -> base of the next storey (bracket band + roof rise)
APEX_Z = 17.9; SORIN_TOP = 23.2
SOSEKI_TOP = PLAT_Z + 0.35; GAP = 0.25; FOOT_Z = SOSEKI_TOP + GAP          # stone under the pillar, the floating gap, pillar foot
PILLAR_R = 0.42; PILLAR_TOP = 15.45; CHAIN_TOP = 16.0                      # pillar top, chain anchor (beam in the top storey)
TWX, TWY = 14.0, 0.0; T_HW = 2.6; T_PLINTH = 0.8; T_ST = 4.2; T_N = 4        # master's tower
T_WALL_TOP = T_PLINTH + T_ST * T_N; T_APEX = T_WALL_TOP + 3.2
Z_SNAP = T_PLINTH + 2 * T_ST + 2.1                                          # 11.3: the nailed joint where the tower snaps
JOINT = (TWX - 0.6, TWY - T_HW, Z_SNAP)                                       # the crack: front face (-y), iron joint plate
HINGE = (TWX, TWY - T_HW, Z_SNAP)                                             # the top half falls over its south edge (-y), into the courtyard
YARD = (-16.0, 28.0, -32.0, 18.0)                                           # courtyard walls x0, x1, y0, y1
STREET_HW = 4.5; STREET_Y0 = -34.0; STREET_Y1 = -104.0

def _kd(travel, elev):
    h = Vector((travel[0], travel[1], 0)).normalized(); e = math.radians(elev)
    return (h.x * math.cos(e), h.y * math.cos(e), -math.sin(e))

# ----------------------------------------------------------------------------- presets (tower.py light model)
PRESETS = {
    'DAY': dict(key=(1.31, 1.08, 0.30), shade_tint=(0.17, 0.16, 0.48), shade_mix=0.7, key_desat=0.0, key_dir=_kd((0.45, 0.75), 45), sun_elev=45, sun_angle=0.5,
                shade=(0.10, 0.18, 0.56), lift=(0.004, 0.004, 0.016), form=(0.0, -0.05, 0.22), toon=0.55, sky='day', pano='day', sky_k=0.8, pano_k=0.9,
                night=False, ink='#2a1712', lamp_k=0.0, win_k=0.0, pool_k=0.0, haze=None, grade_offset=(0.003, 0.002, 0.008), grade_saturation=1.08, bloom_size=0.05),
    'SUNSET': dict(key=(1.62, 0.98, 0.32), shade_tint=(0.21, 0.165, 0.56), shade_mix=0.7, key_desat=0.0, key_dir=_kd((0.94, 0.34), 11), sun_elev=11, sun_angle=0.6,
                   shade=(0.17, 0.13, 0.42), lift=(0.008, 0.004, 0.02), form=(0.0, -0.05, 0.2), toon=0.5, sky='sunset', pano='sunset', sky_k=0.92, pano_k=0.92,
                   night=False, ink='#2a1712', lamp_k=1.0, win_k=0.5, pool_k=0.0, haze=('#ffb47a', 0.10), grade_offset=(0.004, 0.002, 0.009), grade_saturation=1.06, bloom_size=0.05),
    'NIGHT': dict(key=(0.20, 0.31, 0.74), shade_tint=(0.075, 0.095, 0.36), shade_mix=0.75, key_desat=0.6, key_dir=_kd((0.55, 0.50), 40), sun_elev=40, sun_angle=0.6,
                  shade=(0.07, 0.10, 0.34), lift=(0.004, 0.006, 0.024), form=(0.0, -0.05, 0.2), toon=0.55, sky='night', pano='night', sky_k=1.0, pano_k=0.85,
                  night=True, ink='#1d1449', lamp_k=2.6, win_k=1.0, pool_k=0.9, haze=None, grade_offset=(0.002, 0.003, 0.012), grade_saturation=1.05, bloom_size=0.05),
    'DAWN': dict(key=(1.30, 1.00, 0.74), shade_tint=(0.20, 0.16, 0.50), shade_mix=0.7, key_desat=0.0, key_dir=_kd((-0.92, 0.39), 14), sun_elev=14, sun_angle=3.0,
                 shade=(0.15, 0.15, 0.46), lift=(0.01, 0.008, 0.02), form=(0.0, -0.05, 0.2), toon=0.6, sky='dawn', pano='dawn', sky_k=0.9, pano_k=0.9,
                 night=False, ink='#2a1712', lamp_k=0.0, win_k=0.0, pool_k=0.0, haze=('#ffdcb0', 0.2), grade_offset=(0.004, 0.003, 0.008), grade_saturation=1.04, bloom_size=0.05),
}

# ----------------------------------------------------------------------------- small helpers
def _pivot(name, coll, loc):
    """Empty used as a pivot; 'wrest' stores its world location at rest (pivots are never rotated at build time)."""
    e = bpy.data.objects.new(name, None); coll.objects.link(e); e.location = loc; e.empty_display_size = 0.5; e['wrest'] = tuple(loc)
    STATE.setdefault('objects', {})[name] = e
    return e

def _parent(child, parent):
    """Parent keeping the child's world placement at rest (the parent's rest matrix is a pure translation)."""
    child.parent = parent; child.matrix_parent_inverse = Matrix.Translation(-Vector(parent['wrest']))

def _beam(mb, p0, p1, w, mat):
    mb.frustum(p0, p1, w * 0.7071, w * 0.7071, mat, seg=4)

def _haze_mat(name, hexcol, k, z0=0.0, z1=26.0):
    """Camera-only additive veil: emission hexcol x k x clamp((z1 - z) / (z1 - z0)) over a transparent surface (aerial haze)."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); geo = N('ShaderNodeNewGeometry'); sep = N('ShaderNodeSeparateXYZ'); L(geo.outputs['Position'], sep.inputs[0])
    mr = N('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = z0; mr.inputs['From Max'].default_value = z1; mr.inputs['To Min'].default_value = k; mr.inputs['To Max'].default_value = 0.0; mr.clamp = True
    L(sep.outputs['Z'], mr.inputs['Value'])
    em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*T.hex_lin(hexcol), 1); L(mr.outputs['Result'], em.inputs['Strength'])
    tr = N('ShaderNodeBsdfTransparent'); ad = N('ShaderNodeAddShader'); L(tr.outputs['BSDF'], ad.inputs[0]); L(em.outputs['Emission'], ad.inputs[1])
    lp = N('ShaderNodeLightPath'); mx = N('ShaderNodeMixShader'); tr2 = N('ShaderNodeBsdfTransparent')
    L(lp.outputs['Is Camera Ray'], mx.inputs['Fac']); L(tr2.outputs['BSDF'], mx.inputs[1]); L(ad.outputs['Shader'], mx.inputs[2]); L(mx.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

# ----------------------------------------------------------------------------- the set
def build(preset='DAY', clear=True, open_base=True, dress=True):
    """Build the town set into the current scene (collections SET and LIGHTS, world, render settings, grade).
    Returns the anchors dict (pagoda_API.md). clear=True removes every object of the scene first.
    v2: open_base=True removes the ground storey's front panels (the pillar is seen from the courtyard); dress=True adds the
    ornament, the in-scene warm sources and the yard / street / gate dressing (pagoda_REVIEW2.md). The pillar foot is always dressed."""
    scene = bpy.context.scene; P = dict(PRESETS[preset]); STATE.clear(); STATE['P'] = P; STATE['preset'] = preset
    if clear:
        for ob in list(scene.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for ac in list(bpy.data.actions): bpy.data.actions.remove(ac)
    for me in list(bpy.data.meshes):
        if me.users == 0: bpy.data.meshes.remove(me)
    SET = T._coll('SET', scene); LIGHTS = T._coll('LIGHTS', scene); T._wipe(SET); T._wipe(LIGHTS)
    for m in list(bpy.data.materials):
        if m.name.startswith(('PGD_', 'ink')): bpy.data.materials.remove(m)
    tx = PT.ensure(verbose=False); STATE['tx'] = tx
    w = bpy.data.worlds.get('W_pagoda') or bpy.data.worlds.new('W_pagoda'); scene.world = w; nt = T._tree(w)
    bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld'); bg.inputs['Color'].default_value = (0, 0, 0, 1); bg.inputs['Strength'].default_value = 0.0
    nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
    setup_render(scene, 'final'); scene.frame_start = 1; scene.frame_current = 1
    pre = 'PGD_' + preset + '_'; FORM = tuple(P['form'])
    def _k(v): return 'x'.join('%g' % x for x in v) if isinstance(v, (tuple, list)) else '%g' % v
    def C(hexcol, gain=1.0, sm=1.0, form=True): return mat_lit('%sc_%s_%g_%s_%d' % (pre, hexcol.lstrip('#'), gain, _k(sm), form), hexcol, gain=gain, shade_mul=sm, form=FORM if form else None)
    def TX(name, gain=1.0, sm=1.0, form=True, alpha=False, glow=None, glow_k=0.0):
        return mat_lit('%st_%s_%g_%s_%d_%s' % (pre, name, gain, _k(sm), form, glow or ''), image=tx[name], gain=gain, shade_mul=sm, form=FORM if form else None, alpha=alpha,
                       glow=tx[glow] if glow else None, glow_k=glow_k)
    def E(name, image=None, hexcol='#ffffff', k=1.0, alpha=False): return mat_emit(pre + 'e_' + name, hexcol, image=tx[image] if image else None, strength=k, alpha=alpha)
    night = P['night']
    M = dict(red=C('#c8382a'), red_d=C('#8e2420'), gold=C('#e0b04a', 1.0, 0.9), plaster=TX('plaster'), cream=C('#efe2c4'), fascia=C('#e8b85a'), wood=C('#5a3622'), wood_l=C('#7a4a30'),
             wood_d=C('#3e2418'), kawara=TX('kawara'), kawara_d=TX('kawara_dark'), kawara_h=TX('kawara_house'), ridge=C('#3c4054'), ridge_d=C('#33364a'),
             rafters=TX('rafters', 1.0, form=False), bracket=TX('bracket'), door=TX('door_red'), renji=TX('renji'), bronze=C('#b8903e', 1.0, 0.9), bronze_d=C('#7a5a2a'),
             stone=C('#b4aa9c'), stone_d=C('#8e8478'), ishigaki=TX('ishigaki'), paving=TX('paving', form=False), gravel=TX('gravel', form=False), earth=TX('earth', form=False),
             twall=TX('tower_wall'), iron=C('#3a3438', 1.0, 1.2), pine=C('#2e5a3a', 1.0, 1.1), pine_d=C('#24482e', 1.0, 1.1), bark=C('#5a3a2c'),
             side=TX('side_wall'), dust=C('#ecc898', 1.0, 1.0), chain=C('#4a4450', 1.0, 1.2), cypress=C('#d8a868'), granite=C('#e2dccc'), rubble=C('#9a7a62'), plaster_w=TX('plaster_warm'),
             lantern=(E('lantern', 'lantern', k=P['lamp_k']) if P['lamp_k'] > 0 else TX('lantern')),
             lamp_glow=E('lampwin', None, '#ffc46a', k=max(P['lamp_k'], 0.01)))
    if P['lamp_k'] <= 0: M['lantern'] = TX('lantern', glow='lantern', glow_k=0.5)          # v2: paper lanterns glow by day too
    STATE['M'] = M; STATE['C'] = C; STATE['TX'] = TX
    MV = _v2_materials(pre, P, C, TX, E)
    _ground(SET, M, C, TX, E, P)
    _pagoda(SET, M, C, TX)
    _tower(SET, M, C, TX)
    _walls_gate(SET, M, C, TX)
    _street(SET, M, C, TX, P)
    _hall(SET, M, C, TX)
    _midtown(SET, M, C, TX, P)
    _pines(SET, M)
    _lanterns(SET, M, C, TX, E, P)
    _collapse_parts(SET, M, C, TX)
    if open_base: _open_base()
    _warm_interior(); _pillar_dress(SET, STATE['MW'])
    if dress:
        _ornament(SET, MV); _dressing(SET, MV)
        O = STATE['objects']; MW = STATE['MW']
        for i_, m_ in enumerate(O['brackets_0'].data.materials):                              # ground-storey brackets: warm like its soffit
            for k_ in ('red', 'green', 'gold'):
                if m_ == MV[k_]: O['brackets_0'].data.materials[i_] = MW[k_]
        _glow_slots([O[k] for k in ('storey_0_body', 'storey_0_front', 'orn_0', 'orn_0_front', 'drapes')], GLOW_FRONT + GLOW_IN, 0.35 * GLOW_K[preset])
    # painted plate ring + sky dome (+ haze veils)
    mb = MB(); R = PT.PANO_R; seg = 128
    for i in range(seg):
        a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; u0, u1 = i / seg, (i + 1) / seg
        mb.face([Vector((R * math.cos(a0), R * math.sin(a0), PT.PANO_Z0)), Vector((R * math.cos(a1), R * math.sin(a1), PT.PANO_Z0)), Vector((R * math.cos(a1), R * math.sin(a1), PT.PANO_Z1)), Vector((R * math.cos(a0), R * math.sin(a0), PT.PANO_Z1))],
                mat_emit(pre + 'e_pano', image=tx['pano_' + P['pano']], strength=P['pano_k'], alpha=True), [(u0, 0), (u1, 0), (u1, 1), (u0, 1)])
    pr = mb.obj('plate', SET); pr.visible_shadow = False
    mb = MB(); R = 170.0; seg = 72; els = [-15 + 105 * k / 14 for k in range(15)]
    for i in range(seg):
        for k in range(14):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; e0, e1 = math.radians(els[k]), math.radians(els[k + 1])
            pts = [Vector((R * math.cos(e) * math.cos(a), R * math.cos(e) * math.sin(a), R * math.sin(e))) for (a, e) in ((a0, e0), (a1, e0), (a1, e1), (a0, e1))]
            uvs = [(i / seg, k / 14), ((i + 1) / seg, k / 14), ((i + 1) / seg, (k + 1) / 14), (i / seg, (k + 1) / 14)]
            mb.face(pts[::-1], E('sky', 'sky_' + P['sky'], k=P['sky_k']), uvs[::-1])
    sk = mb.obj('sky', SET); sk.visible_shadow = False
    if P['haze']:
        hm = _haze_mat(pre + 'haze', P['haze'][0], P['haze'][1]); mb = MB()
        for Rh in (36.0, 70.0, 115.0):
            for i in range(64):
                a0, a1 = 2 * math.pi * i / 64, 2 * math.pi * (i + 1) / 64; c = Vector((6.0, -8.0, 0))
                mb.face([c + Vector((Rh * math.cos(a0), Rh * math.sin(a0), -1)), c + Vector((Rh * math.cos(a1), Rh * math.sin(a1), -1)),
                         c + Vector((Rh * math.cos(a1), Rh * math.sin(a1), 40)), c + Vector((Rh * math.cos(a0), Rh * math.sin(a0), 40))], hm)
        hz = mb.obj('haze', SET); hz.visible_shadow = False
    # one hard key
    kd = Vector(P['key_dir']).normalized(); k = max(P['key'])
    d = bpy.data.lights.new('key_sun', 'SUN'); d.color = tuple(x / k for x in P['key']); d.energy = math.pi * k; d.angle = math.radians(P['sun_angle'])
    sun = bpy.data.objects.new('key_sun', d); LIGHTS.objects.link(sun); sun.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler(); sun.location = (-20, -40, 40); STATE['sun'] = sun
    setup_grade(scene)
    for ob in SET.objects: no_bounce(ob)
    set_sway(0.0, 0.0); set_pillar_swing(0.0); set_cutaway(False); set_crack(0); set_plaster(0); set_collapse(0.0); set_quake(0.0)
    A = anchors(); STATE['A'] = A
    return A

# ----------------------------------------------------------------------------- ground, platform
def _ground(SET, M, C, TX, E, P):
    mb = MB(); x0, x1, y0, y1 = YARD
    mb.quad((-150, -150, 0), (300, 0, 0), (0, 300, 0), M['earth'], (-25, -25, 25, 25))
    mb.quad((x0, y0, 0.01), (x1 - x0, 0, 0), (0, y1 - y0, 0), M['gravel'], (x0 / 4, y0 / 4, x1 / 4, y1 / 4))
    mb.quad((-1.3, y0, 0.02), (2.6, 0, 0), (0, y0 * -1 - PLAT_HW, 0), M['paving'], (-1.3 / 4, y0 / 4, 1.3 / 4, -PLAT_HW / 4))
    mb.quad((TWX - 1.0, y0, 0.02), (2.0, 0, 0), (0, -y0 - T_HW - 1.2, 0), M['paving'], (0, y0 / 4, 0.5, (-T_HW - 1.2) / 4))
    mb.obj('ground', SET)
    mb = MB()                                                                    # stone platform with steps on the front
    h = PLAT_HW
    for (p0, pu, nrm) in (((-h, -h, 0), (2 * h, 0, 0), (0, -1, 0)), ((h, -h, 0), (0, 2 * h, 0), (1, 0, 0)), ((h, h, 0), (-2 * h, 0, 0), (0, 1, 0)), ((-h, h, 0), (0, -2 * h, 0), (-1, 0, 0))):
        p0 = Vector(p0); pu = Vector(pu); L_ = pu.length
        mb.oface([p0, p0 + pu, p0 + pu + Vector((0, 0, PLAT_Z)), p0 + Vector((0, 0, PLAT_Z))], M['ishigaki'], [(0, 0), (L_ / 4, 0), (L_ / 4, PLAT_Z / 2), (0, PLAT_Z / 2)], nrm)
    mb.quad((-h, -h, PLAT_Z), (2 * h, 0, 0), (0, 2 * h, 0), M['paving'], (-h / 4, -h / 4, h / 4, h / 4))
    mb.box((-h - 0.1, -h - 0.1, PLAT_Z - 0.12), (h + 0.1, h + 0.1, PLAT_Z), M['stone'], skip='bottom,top')
    for k in range(3):                                                           # steps
        z = PLAT_Z * (k + 1) / 3; dy = 0.45 * (2 - k)
        mb.box((-1.5, -h - 0.45 - dy, 0), (1.5, -h, z), M['stone'])
    mb.obj('platform', SET, hull=0.03)
    # the foundation stone (soseki) of the hanging pillar
    mb = MB(); mb.frustum((0, 0, PLAT_Z - 0.01), (0, 0, SOSEKI_TOP - 0.08), 1.05, 0.98, M['stone_d'], seg=20, cap0=False); mb.frustum((0, 0, SOSEKI_TOP - 0.08), (0, 0, SOSEKI_TOP), 0.98, 0.9, M['granite'], seg=20, cap0=False)
    mb.obj('soseki', SET, hull=0.012)

# ----------------------------------------------------------------------------- the five-storey pagoda
NRM = [Vector((0, -1, 0)), Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((-1, 0, 0))]
def TAN(n): return Vector((-n.y, n.x, 0))
LIFT = 0.55

def _roof(main, front, bells, M, hw, zw, R_o, z_e, R_i, z_top, heavy=False, piv=None):
    """Curved hip roof of one storey: four sides, each a grid between the eave line (R_o at z_e, corners swept up by LIFT) and the
    inner line (R_i at z_top); fascia, rafter soffit back to the bracket band, corner hips, a wind bell under each corner.
    The front (-y) side, its soffit and fascia go into `front` (hidden by the cutaway)."""
    ns, nv = 16, 7; dz = z_top - z_e
    def P(n, s, v):
        R = R_o + (R_i - R_o) * v; z = z_e + dz * v ** 1.5 + LIFT * abs(s) ** 3 * (1 - v) ** 2
        return n * R + TAN(n) * (s * R) + Vector((0, 0, z))
    slant = math.hypot(R_o - R_i, dz)
    tile = M['kawara_d'] if heavy else M['kawara']
    for k, n in enumerate(NRM):
        mb = front if k == 0 else main
        for i in range(ns):
            s0, s1 = -1 + 2 * i / ns, -1 + 2 * (i + 1) / ns
            for j in range(nv):
                v0, v1 = j / nv, (j + 1) / nv
                q = [P(n, s0, v0), P(n, s1, v0), P(n, s1, v1), P(n, s0, v1)]
                R0, R1 = R_o + (R_i - R_o) * v0, R_o + (R_i - R_o) * v1
                uv = [(s0 * R0 / 2, v0 * slant / 2), (s1 * R0 / 2, v0 * slant / 2), (s1 * R1 / 2, v1 * slant / 2), (s0 * R1 / 2, v1 * slant / 2)]
                mb.oface(q, tile, uv, (n.x, n.y, 1.5))
            a, b = P(n, s0, 0), P(n, s1, 0); fz = Vector((0, 0, 0.3 if not heavy else 0.45))
            mb.oface([a - fz, b - fz, b, a], M['fascia'] if not heavy else M['wood_d'], [(0, 0)] * 4, n)
            ri = hw + 0.25; zi = zw + 0.6
            ia = n * ri + TAN(n) * (s0 * ri) + Vector((0, 0, zi)); ib = n * ri + TAN(n) * (s1 * ri) + Vector((0, 0, zi))
            mb.oface([a - fz, ia, ib, b - fz], M['rafters'], [(s0 * R_o / 2, 0), (s0 * ri / 2, 1), (s1 * ri / 2, 1), (s1 * R_o / 2, 0)], (n.x * 0.3, n.y * 0.3, -1))
        c0 = P(n, 1, 0); c1 = P(n, 1, 1)                                            # hip ridge on the corner (s = +1 of this side)
        pts = [P(n, 1, v) for v in (0.0, 0.25, 0.5, 0.75, 1.0)]
        for p0, p1 in zip(pts, pts[1:]): main.frustum(p0 + Vector((0, 0, 0.12)), p1 + Vector((0, 0, 0.12)), 0.13, 0.13, M['ridge_d'] if heavy else M['ridge'], seg=6)
        main.frustum(c0 + Vector((0, 0, 0.12)), c0 + (c0 - c1).normalized() * 0.35 + Vector((0, 0, 0.35)), 0.15, 0.06, M['ridge_d'] if heavy else M['ridge'], seg=6)
        if bells is not None:
            bells.append(c0 - Vector((0, 0, 0.3)))

def _pagoda(SET, M, C, TX):
    STATE['storeys'] = []; STATE['cut_objs'] = []; STATE['bells'] = []
    for i, (hw, z0, h, ov) in enumerate(STOREYS):
        zw = z0 + h; piv = _pivot('storey_%d' % i, SET, (0, 0, z0)); piv['wrest'] = (0, 0, z0); STATE['storeys'].append(piv)
        main, front = MB(), MB(); bells = []
        # floor deck with a hole round the pillar
        r_in = 0.75; ro = hw + (0.45 if i > 0 else 0.0)
        for k, n in enumerate(NRM):
            t = TAN(n); q = [n * r_in + t * r_in, n * r_in - t * r_in, n * ro - t * ro, n * ro + t * ro]
            (front if k == 0 else main).oface([p + Vector((0, 0, z0 + 0.02)) for p in q], M['paving'] if i == 0 else M['wood_l'], [(p.x / 4, p.y / 4) for p in q], (0, 0, 1))
            if i > 0: (front if k == 0 else main).oface([p + Vector((0, 0, z0 - 0.06)) for p in q], M['wood_d'], [(0, 0)] * 4, (0, 0, -1))
        # walls: 3 bays per side; corner posts and rails in main, the front side's panels and middle posts in front
        bay = 2 * hw / 3
        for k, n in enumerate(NRM):
            t = TAN(n); mb = front if k == 0 else main
            for b in range(3):
                a = -hw + b * bay; c = n * (hw - 0.06); mat = M['door'] if b == 1 else (M['renji'] if i > 0 or k % 2 else M['door'])
                if i == 0 and b != 1 and k % 2 == 0: mat = M['renji']
                p0 = c + t * (a + 0.12) + Vector((0, 0, z0 + 0.1)); p1 = c + t * (a + bay - 0.12) + Vector((0, 0, z0 + 0.1))
                mb.oface([p0, p1, p1 + Vector((0, 0, h - 0.4)), p0 + Vector((0, 0, h - 0.4))], mat, [(0, 0), (1, 0), (1, 1), (0, 1)], n)
                qi = [p - n * 0.1 for p in (p0, p1, p1 + Vector((0, 0, h - 0.3)), p0 + Vector((0, 0, h - 0.3)))]          # dark board lining inside
                mb.oface(qi, M['wood_d'], [(0, 0)] * 4, -n)
                if b > 0:                                                         # middle posts
                    pc = n * hw + t * a; mb.box((pc.x - 0.14, pc.y - 0.14, z0), (pc.x + 0.14, pc.y + 0.14, zw), M['red'])
            pc = n * hw + t * hw; main.box((pc.x - 0.16, pc.y - 0.16, z0), (pc.x + 0.16, pc.y + 0.16, zw), M['red'])      # corner post
            for (za, zb) in ((z0, z0 + 0.12), (zw - 0.32, zw - 0.1)):                                                  # sill and head rails
                pa = n * (hw + 0.02) - t * hw; pb = n * (hw + 0.02) + t * hw
                lo = Vector((min(pa.x, pb.x) - 0.1, min(pa.y, pb.y) - 0.1, za)); hi = Vector((max(pa.x, pb.x) + 0.1, max(pa.y, pb.y) + 0.1, zb))
                mb.box(tuple(lo), tuple(hi), M['red'])
        # bracket band (kumimono) between the wall top and the eave
        rb = hw + 0.2
        for k, n in enumerate(NRM):
            t = TAN(n); p0 = n * rb - t * rb + Vector((0, 0, zw - 0.1)); p1 = n * rb + t * rb + Vector((0, 0, zw - 0.1))
            main.oface([p0, p1, p1 + Vector((0, 0, 0.72)), p0 + Vector((0, 0, 0.72))], M['bracket'], [(0, 0), (2 * rb / 3, 0), (2 * rb / 3, 1), (0, 1)], n)
        main.box((-rb, -rb, zw + 0.6), (rb, rb, zw + 0.64), M['red_d'], skip='bottom')
        # balcony railing on the upper storeys
        if i > 0:
            rr = hw + 0.45
            for k, n in enumerate(NRM):
                t = TAN(n); mb = front if k == 0 else main
                pa = n * rr - t * rr; pb = n * rr + t * rr
                mb.box((min(pa.x, pb.x) - 0.05, min(pa.y, pb.y) - 0.05, z0 + 0.5), (max(pa.x, pb.x) + 0.05, max(pa.y, pb.y) + 0.05, z0 + 0.58), M['red'])
                for j in range(int(2 * rr / 0.7) + 1):
                    p = pa + (pb - pa) * (j / int(2 * rr / 0.7)); mb.box((p.x - 0.04, p.y - 0.04, z0), (p.x + 0.04, p.y + 0.04, z0 + 0.55), M['red'])
        # roof
        if i < 4:
            hn = STOREYS[i + 1][0]; _roof(main, front, bells, M, hw, zw, hw + ov, zw + 0.55, hn + 0.06, STOREYS[i + 1][1])
        else:
            _roof(main, front, bells, M, hw, zw, hw + ov, zw + 0.55, 0.32, APEX_Z)
            _sorin(main, M)
            # the beam the pillar's chain hangs from
            main.box((-hw + 0.1, -0.2, CHAIN_TOP), (hw - 0.1, 0.2, CHAIN_TOP + 0.4), M['wood'])
            main.box((-0.2, -hw + 0.1, CHAIN_TOP + 0.4), (0.2, hw - 0.1, CHAIN_TOP + 0.8), M['wood'])
        om = main.obj('storey_%d_body' % i, SET, hull=0.035); _parent(om, piv)
        of = front.obj('storey_%d_front' % i, SET, hull=0.035); _parent(of, piv); STATE['cut_objs'].append(of)
        for j, bp in enumerate(bells):                                                 # wind bells (loose props, swing in a quake)
            bpiv = _pivot('bell_%d_%d' % (i, j), SET, tuple(bp)); bpiv['wrest'] = tuple(bp); _parent(bpiv, piv)
            mb = MB(); mb.frustum(bp, bp - Vector((0, 0, 0.2)), 0.02, 0.02, M['bronze_d'], seg=4); mb.frustum(bp - Vector((0, 0, 0.2)), bp - Vector((0, 0, 0.55)), 0.09, 0.17, M['bronze'], seg=10)
            mb.frustum(bp - Vector((0, 0, 0.55)), bp - Vector((0, 0, 0.75)), 0.02, 0.07, M['bronze_d'], seg=4)
            bo = mb.obj('bell_%d_%d_mesh' % (i, j), SET, hull=0.01); _parent(bo, bpiv)
            STATE.setdefault('loose', []).append(dict(ob=bpiv, kind='swing', amp=14.0, seed=100 + i * 4 + j))
    # the hanging central pillar (shinbashira) and its chain; it hangs from the top storey
    top = STATE['storeys'][4]
    pp = _pivot('pillar_pivot', SET, (0, 0, CHAIN_TOP)); pp['wrest'] = (0, 0, CHAIN_TOP); _parent(pp, top)
    mb = MB(); mb.frustum((0, 0, FOOT_Z), (0, 0, PILLAR_TOP), PILLAR_R, PILLAR_R * 0.92, M['cypress'], seg=16)
    mb.frustum((0, 0, FOOT_Z), (0, 0, FOOT_Z + 0.06), PILLAR_R + 0.05, PILLAR_R + 0.05, M['gold'], seg=16)
    for z in (FOOT_Z + 0.3, PILLAR_TOP - 0.2): mb.frustum((0, 0, z - 0.08), (0, 0, z + 0.08), PILLAR_R + 0.04, PILLAR_R + 0.04, M['bronze_d'], seg=16, cap0=False, cap1=False)
    mb.frustum((0, 0, PILLAR_TOP), (0, 0, PILLAR_TOP + 0.12), 0.3, 0.12, M['iron'], seg=10)                        # iron cap and eye
    zc = PILLAR_TOP + 0.12; nl = 4; L_ = (CHAIN_TOP - zc) / nl
    for j in range(nl):                                                                                          # chain links (alternating)
        za, zb = zc + j * L_, zc + (j + 1) * L_ + 0.04; w_ = 0.1
        if j % 2 == 0:
            for sx in (-w_, w_): mb.frustum((sx, 0, za), (sx, 0, zb), 0.025, 0.025, M['chain'], seg=5)
            for z_ in (za, zb): mb.frustum((-w_, 0, z_), (w_, 0, z_), 0.025, 0.025, M['chain'], seg=5)
        else:
            for sy in (-w_, w_): mb.frustum((0, sy, za), (0, sy, zb), 0.025, 0.025, M['chain'], seg=5)
            for z_ in (za, zb): mb.frustum((0, -w_, z_), (0, w_, z_), 0.025, 0.025, M['chain'], seg=5)
    po = mb.obj('pillar', SET, hull=0.03); _parent(po, pp); STATE['pillar'] = pp
    # two oil lamps on stands inside the ground storey (always lit: the warm light of the interior in the cutaway shots)
    mb = MB(); fl = MB(); pl = MB(); fm = mat_emit('PGD_%s_flame' % STATE['preset'], '#ffc46a', strength=3.0); pm = mat_emit('PGD_%s_ipool' % STATE['preset'], image=STATE['tx']['pool'], strength=0.8, alpha=True)
    for (x, y) in ((-1.7, 1.5), (1.7, 1.5)):
        mb.frustum((x, y, PLAT_Z), (x, y, PLAT_Z + 0.1), 0.3, 0.3, STATE['M']['wood_d'], seg=8); mb.frustum((x, y, PLAT_Z + 0.1), (x, y, PLAT_Z + 1.5), 0.05, 0.05, STATE['M']['wood_d'], seg=6)
        mb.frustum((x, y, PLAT_Z + 1.5), (x, y, PLAT_Z + 1.95), 0.26, 0.26, STATE['M']['bronze_d'], seg=10, cap1=False)
        fl.frustum((x, y, PLAT_Z + 1.6), (x, y, PLAT_Z + 1.98), 0.24, 0.22, fm, seg=10); fl.frustum((x, y, PLAT_Z + 1.98), (x, y, PLAT_Z + 2.35), 0.12, 0.0, fm, seg=8)
        pl.quad((x - 1.6, y - 1.6, PLAT_Z + 0.04), (3.2, 0, 0), (0, 3.2, 0), pm)
    mb.obj('oil_lamps', SET, hull=0.012); o = fl.obj('oil_lamp_glow', SET); o.visible_shadow = False; o = pl.obj('oil_lamp_pools', SET); o.visible_shadow = False

def _sorin(mb, M):
    """Bronze finial on the top roof: base box, inverted bowl, shaft with nine rings, flame panel (suien), dragon-car and jewel."""
    z = APEX_Z - 0.3
    mb.box((-0.55, -0.55, z), (0.55, 0.55, z + 0.5), M['bronze_d']); z += 0.5
    mb.frustum((0, 0, z), (0, 0, z + 0.45), 0.55, 0.3, M['bronze'], seg=14); z += 0.45
    mb.frustum((0, 0, z), (0, 0, SORIN_TOP - 0.6), 0.1, 0.08, M['bronze'], seg=8)
    for k in range(9):
        zr = z + 0.35 + k * 0.38; r = 0.5 - 0.022 * k; mb.frustum((0, 0, zr), (0, 0, zr + 0.07), r, r, M['bronze'], seg=16)
        mb.frustum((0, 0, zr + 0.07), (0, 0, zr + 0.1), r, r * 0.9, M['bronze_d'], seg=16, cap0=False)
    zf = z + 0.35 + 9 * 0.38 + 0.1
    for a in (0.0, math.pi / 2):                                                   # suien: two crossed flame panels
        d = Vector((math.cos(a), math.sin(a), 0)); nn = Vector((-d.y, d.x, 0)); pts = []
        for j in range(9):
            t = j / 8; w_ = 0.42 * math.sin(math.pi * t) + 0.05; zz = zf + 0.9 * t
            pts.append((t, w_ * (1.0 if j % 2 else 0.75), zz))
        poly = [Vector((0, 0, zf))] + [d * p[1] + Vector((0, 0, p[2])) for p in pts] + [Vector((0, 0, zf + 0.95))] + [d * (-p[1]) + Vector((0, 0, p[2])) for p in reversed(pts)]
        mb.oface(poly, M['gold'], [(0, 0)] * len(poly), nn)
    mb.sphere((0, 0, zf + 1.15), 0.18, M['gold'], seg=10, rings=6)
    mb.sphere((0, 0, SORIN_TOP - 0.2), 0.16, M['gold'], seg=10, rings=6)

# ----------------------------------------------------------------------------- the master's rigid tower
def _tower(SET, M, C, TX):
    STATE['tower'] = {}
    lo, up = MB(), MB()
    lo.box((TWX - T_HW - 0.4, TWY - T_HW - 0.4, 0), (TWX + T_HW + 0.4, TWY + T_HW + 0.4, T_PLINTH), M['stone'], mats=dict(top=M['paving']), tile=(2, 1))
    for (mb, z0, z1) in ((lo, T_PLINTH, Z_SNAP), (up, Z_SNAP, T_WALL_TOP)):
        for k, n in enumerate(NRM):
            t = TAN(n); pa = Vector((TWX, TWY, 0)) + n * T_HW - t * T_HW; pb = Vector((TWX, TWY, 0)) + n * T_HW + t * T_HW
            v = lambda z: (z - T_PLINTH) / T_ST
            mb.oface([pa + Vector((0, 0, z0)), pb + Vector((0, 0, z0)), pb + Vector((0, 0, z1)), pa + Vector((0, 0, z1))], M['twall'],
                     [(0, v(z0)), (2 * T_HW / 4, v(z0)), (2 * T_HW / 4, v(z1)), (0, v(z1))], n)
            for s in (-1, 1):                                                    # heavy corner posts
                pc = Vector((TWX, TWY, 0)) + n * T_HW + t * T_HW * s
                if k % 2 == 0: mb.box((pc.x - 0.2, pc.y - 0.2, z0), (pc.x + 0.2, pc.y + 0.2, z1), M['wood_d'])
    # skirt roofs at each storey top (heavy, straight, short eaves); the top hip roof with ridge ornaments
    for j in range(1, T_N + 1):
        zt = T_PLINTH + T_ST * j; mb = lo if zt < Z_SNAP else up
        if j < T_N:
            R_o = T_HW + 0.9; R_i = T_HW + 0.02; z_e = zt - 0.35; z_i = zt + 0.35
        else:
            R_o = T_HW + 1.5; R_i = 0.35; z_e = zt - 0.2; z_i = T_APEX
        for n in NRM:
            t = TAN(n); c = Vector((TWX, TWY, 0))
            q = [c + n * R_o - t * R_o + Vector((0, 0, z_e)), c + n * R_o + t * R_o + Vector((0, 0, z_e)), c + n * R_i + t * R_i + Vector((0, 0, z_i)), c + n * R_i - t * R_i + Vector((0, 0, z_i))]
            sl = math.hypot(R_o - R_i, z_i - z_e)
            mb.oface(q, M['kawara_d'], [(-R_o / 2, 0), (R_o / 2, 0), (R_i / 2, sl / 2), (-R_i / 2, sl / 2)], (n.x, n.y, 1.3))
            fz = Vector((0, 0, 0.4)); mb.oface([q[0] - fz, q[1] - fz, q[1], q[0]], M['wood_d'], [(0, 0)] * 4, n)
            ib = c + n * T_HW - t * T_HW + Vector((0, 0, z_e - 0.9)); ic = c + n * T_HW + t * T_HW + Vector((0, 0, z_e - 0.9))
            mb.oface([q[0] - fz, q[1] - fz, ic, ib], M['wood'], [(0, 0)] * 4, (n.x * 0.3, n.y * 0.3, -1))
            p0 = q[1] + Vector((0, 0, 0.12)); p1 = q[2] + Vector((0, 0, 0.12)); mb.frustum(p0, p1, 0.17, 0.17, M['ridge_d'], seg=6)
        if j == T_N:
            for s in (-1, 1): mb.frustum((TWX + s * 0.5, TWY, T_APEX - 0.1), (TWX + s * 0.5, TWY, T_APEX + 0.8), 0.22, 0.1, M['gold'], seg=8)   # shachi ornaments
            mb.box((TWX - 0.6, TWY - 0.2, T_APEX - 0.25), (TWX + 0.6, TWY + 0.2, T_APEX + 0.1), M['ridge_d'])
    for j in range(1, T_N):                                                       # heavy cross beams sticking out at each floor
        zt = T_PLINTH + T_ST * j - 0.9; mb = lo if zt < Z_SNAP else up
        for s in (-1.4, 0, 1.4): mb.box((TWX + s - 0.18, TWY - T_HW - 0.35, zt - 0.4), (TWX + s + 0.18, TWY + T_HW + 0.35, zt), M['wood_d'])
    # the ground-floor door
    lo.oface([(TWX - 0.8, TWY - T_HW - 0.03, T_PLINTH), (TWX + 0.8, TWY - T_HW - 0.03, T_PLINTH), (TWX + 0.8, TWY - T_HW - 0.03, T_PLINTH + 2.6), (TWX - 0.8, TWY - T_HW - 0.03, T_PLINTH + 2.6)], M['wood_d'], [(0, 0)] * 4, (0, -1, 0))
    ol = lo.obj('tower_lower', SET, hull=0.04)
    tp = _pivot('tower_top_pivot', SET, HINGE); tp['wrest'] = HINGE
    ou = up.obj('tower_upper', SET, hull=0.04); _parent(ou, tp)
    STATE['tower'] = dict(lower=ol, upper=ou, pivot=tp)
    # crack and plaster decals on the joint (front face): offsets order the layers (crack1 < patch1 < crack2 < patch2 < crack3)
    jx, jy, jz = JOINT; decs = {}
    for nm, off, img in (('crack_1', 0.01, 'crack_1'), ('patch_1', 0.02, 'patch_1'), ('crack_2', 0.03, 'crack_2'), ('patch_2', 0.04, 'patch_2'), ('crack_3', 0.05, 'crack_3')):
        mb = MB(); y = jy - off
        mb.oface([(jx - 1.5, y, jz - 0.75), (jx + 1.5, y, jz - 0.75), (jx + 1.5, y, jz + 0.75), (jx - 1.5, y, jz + 0.75)], TX(img, 1.0, alpha=True), [(0, 0.25), (1, 0.25), (1, 0.75), (0, 0.75)], (0, -1, 0))
        o = mb.obj('decal_' + nm, SET); o.visible_shadow = False; decs[nm] = o
    STATE['decals'] = decs
    # the jagged stump top and splinters (shown once the top half is gone)
    mb = MB(); r = random.Random(71)
    for k in range(18):
        a = r.uniform(0, 2 * math.pi); x = TWX + r.uniform(-T_HW + 0.2, T_HW - 0.2); y = TWY + (r.choice((-1, 1)) * (T_HW - 0.12) if k % 2 else r.uniform(-T_HW, T_HW))
        if k % 2 == 0: x = TWX + r.choice((-1, 1)) * (T_HW - 0.12)
        h = r.uniform(0.3, 1.3); _beam(mb, (x, y, Z_SNAP - 0.2), (x + r.uniform(-0.25, 0.25), y + r.uniform(-0.25, 0.25), Z_SNAP + h), r.uniform(0.1, 0.22), M['wood_l'] if k % 3 else M['plaster'])
    st = mb.obj('tower_stump', SET, hull=0.02); STATE['tower']['stump'] = st

# ----------------------------------------------------------------------------- collapse: rubble pile, flying debris, dust
PILE_C = (14.0, -8.6); PILE_R = (4.4, 6.2); PILE_H = 2.6
def pile_height(x, y):
    d = ((x - PILE_C[0]) / PILE_R[0]) ** 2 + ((y - PILE_C[1]) / PILE_R[1]) ** 2
    return PILE_H * max(0.0, 1 - d) ** 1.2

def _collapse_parts(SET, M, C, TX):
    r = random.Random(73)
    # rubble pile: a mound covered with broken timbers, plaster slabs and roof tiles
    root = _pivot('rubble_root', SET, (PILE_C[0], PILE_C[1], 0)); root['wrest'] = (PILE_C[0], PILE_C[1], 0)
    mb = MB(); n = 14
    for i in range(n):
        for j in range(n):
            pts = []
            for (a, b) in ((i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)):
                x = PILE_C[0] + PILE_R[0] * (2 * a / n - 1) * 1.05; y = PILE_C[1] + PILE_R[1] * (2 * b / n - 1) * 1.05; pts.append(Vector((x, y, pile_height(x, y) - 0.05)))
            if all(p.z < -0.04 for p in pts): continue
            mb.oface(pts, M['rubble'] if (i + j) % 3 else M['stone_d'], [(0, 0)] * 4, (0, 0, 1))
    for k in range(190):
        x = PILE_C[0] + r.uniform(-1, 1) * PILE_R[0] * 0.95; y = PILE_C[1] + r.uniform(-1, 1) * PILE_R[1] * 0.95; z = pile_height(x, y)
        if z <= 0.05 and r.random() < 0.7: continue
        kind = r.random(); a = r.uniform(0, math.pi)
        if kind < 0.45:
            L_ = r.uniform(1.5, 4.5); d = Vector((math.cos(a), math.sin(a), r.uniform(-0.4, 0.5))).normalized()
            _beam(mb, Vector((x, y, z + 0.1)) - d * L_ / 2, Vector((x, y, z + 0.1)) + d * L_ / 2, r.uniform(0.2, 0.36), M['wood_l'] if r.random() < 0.6 else M['wood_d'])
        elif kind < 0.75:
            w_, l_ = r.uniform(0.6, 1.4), r.uniform(0.5, 1.2); d = Vector((math.cos(a), math.sin(a), 0)); e = Vector((-d.y, d.x, r.uniform(-0.5, 0.5)))
            c = Vector((x, y, z + 0.08)); mb.oface([c - d * w_ - e * l_, c + d * w_ - e * l_, c + d * w_ + e * l_, c - d * w_ + e * l_], M['plaster_w'] if r.random() < 0.6 else M['twall'], [(0, 0), (0.4, 0), (0.4, 0.4), (0, 0.4)], (0, 0, 1))
        else:
            mb.box((x - 0.3, y - 0.22, z), (x + 0.3, y + 0.22, z + 0.12), M['kawara_d'], tile=(2, 2))
    for k in range(3):                                                           # the broken top roof and a skirt roof slab on the pile
        cx, cy = PILE_C[0] + (2.5, -1.0, 0.8)[k], PILE_C[1] + (0.5, 1.6, -2.0)[k]; z = pile_height(cx, cy); s = (2.2, 1.5, 1.3)[k]
        q = [Vector((cx - s, cy - s * 0.7, z + 0.2)), Vector((cx + s, cy - s * 0.8, z + 0.5)), Vector((cx + s * 0.8, cy + s * 0.7, z + 0.9)), Vector((cx - s * 0.9, cy + s * 0.6, z + 0.4))]
        mb.oface(q, M['kawara_d'], [(0, 0), (s, 0), (s, s), (0, s)], (0.1, -0.2, 1))
    mb.box((PILE_C[0] + 2.7, PILE_C[1] + 0.3, pile_height(PILE_C[0] + 2.7, PILE_C[1]) + 0.6), (PILE_C[0] + 3.2, PILE_C[1] + 0.8, pile_height(PILE_C[0] + 2.7, PILE_C[1]) + 1.6), M['gold'])
    po = mb.obj('rubble', SET, hull=0.03); _parent(po, root)
    STATE['rubble'] = dict(root=root, mesh=po)
    # flying debris: 26 pieces with a ballistic path from the break to the pile
    deb = []
    for k in range(26):
        t0 = r.uniform(0.18, 0.62); dur = r.uniform(0.25, 0.4)
        s = Vector((TWX + r.uniform(-T_HW, T_HW), TWY + r.uniform(-T_HW, T_HW), Z_SNAP + r.uniform(-0.3, 0.6)))
        ex = PILE_C[0] + r.uniform(-1, 1) * PILE_R[0] * 0.8; ey = PILE_C[1] + r.uniform(-1, 1) * PILE_R[1] * 0.8
        e = Vector((ex, ey, pile_height(ex, ey) + 0.1)); arc = r.uniform(1.5, 5.0); spin = Vector((r.uniform(-8, 8), r.uniform(-8, 8), r.uniform(-4, 4)))
        piv = _pivot('debris_%02d' % k, SET, tuple(s)); piv['wrest'] = tuple(s)
        mb = MB()
        if k % 3: _beam(mb, s - Vector((r.uniform(0.6, 1.4), 0, 0)), s + Vector((r.uniform(0.6, 1.4), 0, 0)), r.uniform(0.16, 0.3), M['wood_l'] if k % 2 else M['wood_d'])
        else: mb.box(tuple(s - Vector((0.4, 0.3, 0.06))), tuple(s + Vector((0.4, 0.3, 0.06))), M['plaster_w'])
        o = mb.obj('debris_%02d_mesh' % k, SET, hull=0.015); _parent(o, piv)
        deb.append(dict(piv=piv, s=s, e=e, t0=t0, dur=dur, arc=arc, spin=spin, ob=o))
    STATE['debris'] = deb
    # dust: puffs at the break (burst) and a column rising from the landing (u -> 1); a low lingering bank (settle)
    puffs = []; settle = []
    for k in range(46):
        if k < 8: c = Vector((TWX + r.uniform(-T_HW, T_HW) * 1.1, TWY + r.uniform(-T_HW, T_HW), Z_SNAP + r.uniform(-0.6, 0.6))); kind = 'break'; size = r.uniform(0.7, 1.4); t0 = r.uniform(0.04, 0.15)
        elif k < 22: c = Vector((PILE_C[0] + r.uniform(-1, 1) * 6, PILE_C[1] + r.uniform(-1, 1) * 4.5, r.uniform(0.5, 3.5))); kind = 'ground'; size = r.uniform(1.6, 3.2); t0 = r.uniform(0.6, 0.78)
        else:
            h = (k - 22) / 23.0; c = Vector((PILE_C[0] + r.uniform(-2.2, 2.2) + 3.0 * h, PILE_C[1] + 2.0 + r.uniform(-2.0, 2.0), 2.5 + 23.0 * h + r.uniform(-1, 1))); kind = 'column'; size = r.uniform(1.8, 3.2) * (1 + 0.5 * h); t0 = 0.66 + 0.22 * h
        mb = MB(); mb.sphere((0, 0, 0), 1.0, M['dust'], seg=22, rings=12); o = mb.obj('dust_%02d' % k, SET, hull=0.02); o.location = c
        puffs.append(dict(ob=o, c=c, kind=kind, size=size, t0=t0))
    cam = Vector(CAMS['rubble_dawn']['loc'])
    while len(settle) < 16:
        c = Vector((PILE_C[0] + r.uniform(-1, 1) * 9, PILE_C[1] + 3 + r.uniform(-1, 1) * 8, r.uniform(0.2, 1.2)))
        if (c - cam).length < 6.5: continue
        mb = MB(); mb.sphere((0, 0, 0), 1.0, M['dust'], seg=22, rings=12); o = mb.obj('settle_%02d' % len(settle), SET); o.location = c
        settle.append(dict(ob=o, c=c, size=r.uniform(1.4, 2.6)))
    STATE['dust'] = puffs; STATE['settle'] = settle

# ----------------------------------------------------------------------------- courtyard walls, the gate
def _wall_run(mb, rb, M, a, b):
    """A temple wall from a to b (2D): stone base (ishigaki) 0..1.1, white plaster with a timber rail 1.1..2.5, tiled coping."""
    a = Vector((a[0], a[1], 0)); b = Vector((b[0], b[1], 0)); d = (b - a); L_ = d.length; d.normalize(); n = Vector((-d.y, d.x, 0)); w_ = 0.45
    for s in (-1, 1):
        o = a + n * w_ * s; e = b + n * w_ * s
        mb.oface([o, e, e + Vector((0, 0, 1.1)), o + Vector((0, 0, 1.1))], M['ishigaki'], [(0, 0), (L_ / 4, 0), (L_ / 4, 0.55), (0, 0.55)], n * s)
        o2 = a + n * (w_ - 0.12) * s; e2 = b + n * (w_ - 0.12) * s
        mb.oface([o2 + Vector((0, 0, 1.1)), e2 + Vector((0, 0, 1.1)), e2 + Vector((0, 0, 2.5)), o2 + Vector((0, 0, 2.5))], M['plaster'], [(0, 0), (L_ / 2, 0), (L_ / 2, 0.7), (0, 0.7)], n * s)
        mb.oface([o2 + Vector((0, 0, 1.1)), e2 + Vector((0, 0, 1.1)), e2 + Vector((0, 0, 1.25)), o2 + Vector((0, 0, 1.25))], M['wood'], [(0, 0)] * 4, n * s)
        oe, ee = a + n * (w_ + 0.35) * s, b + n * (w_ + 0.35) * s
        rb.oface([oe + Vector((0, 0, 2.45)), ee + Vector((0, 0, 2.45)), b + Vector((0, 0, 2.95)), a + Vector((0, 0, 2.95))], M['kawara_h'], [(0, 0), (L_ / 2, 0), (L_ / 2, 0.4), (0, 0.4)], n * s + Vector((0, 0, 1.5)))
    rb.frustum(a + Vector((0, 0, 2.95)), b + Vector((0, 0, 2.95)), 0.13, 0.13, M['ridge'], seg=6)

def _walls_gate(SET, M, C, TX):
    mb, rb = MB(), MB(); x0, x1, y0, y1 = YARD
    for (a, b) in (((x0, y0), (-3.6, y0)), ((3.6, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        _wall_run(mb, rb, M, a, b)
    mb.obj('yard_walls', SET, hull=0.04); rb.obj('yard_wall_roofs', SET, hull=0.04)
    # the gate: four red posts, tie beams, a tiled gable roof with deep curved eaves
    g = MB(); gy = y0
    for x in (-2.9, 2.9):
        for y in (gy - 1.0, gy + 1.0): g.frustum((x, y, 0), (x, y, 5.0), 0.26, 0.24, M['red'], seg=10); g.frustum((x, y, 0), (x, y, 0.35), 0.4, 0.4, M['stone'], seg=10)
    for z in (4.0, 4.9):
        for y in (gy - 1.0, gy + 1.0): g.box((-3.5, y - 0.18, z - 0.25), (3.5, y + 0.18, z + 0.15), M['red'])
    g.box((-3.5, gy - 1.2, 5.0), (3.5, gy + 1.2, 5.35), M['bracket'], tile=(3, 0.8))
    for s in (-1, 1):
        pts = []
        for j in range(9):
            v = j / 8; y_ = gy + s * (2.6 * (1 - v)); z_ = 5.25 + 1.9 * v ** 1.4
            pts.append((y_, z_))
        for (ya, za), (yb, zb) in zip(pts, pts[1:]):
            g.oface([(-4.6, ya, za), (4.6, ya, za), (4.6, yb, zb), (-4.6, yb, zb)], M['kawara_h'],
                    [(0, ya / 2), (4.6, ya / 2), (4.6, yb / 2), (0, yb / 2)], (0, s, 1.5))
        g.oface([(-4.6, gy + s * 2.6, 5.25), (4.6, gy + s * 2.6, 5.25), (4.6, gy + s * 2.6, 4.95), (-4.6, gy + s * 2.6, 4.95)], M['cream'], [(0, 0)] * 4, (0, s, 0))
    g.frustum((-4.7, gy, 7.2), (4.7, gy, 7.2), 0.22, 0.22, M['ridge'], seg=8)
    for x in (-4.7, 4.7): g.frustum((x, gy, 7.1), (x * 1.04, gy, 7.9), 0.28, 0.12, M['ridge'], seg=8)
    g.obj('gate', SET, hull=0.035)
    STATE['gate'] = dict(x=0.0, y=gy, roof=7.2)

# ----------------------------------------------------------------------------- the street: two rows of machiya
def _house(mb, rb, M, F, front_x, y0, y1, sgn, depth=8.0, H=PT.MA_H, ridge=7.4):
    """Machiya whose street front is the plane x = front_x facing sgn*x, y0..y1: textured front, pent roof (hisashi) at 3.0, gable
    roof with the ridge along the street, plain side walls."""
    xa = front_x; xb = front_x - sgn * depth; W = y1 - y0
    fu = (lambda y: (y - y0) / W) if sgn > 0 else (lambda y: (y1 - y) / W)
    mb.oface([(xa, y0, 0), (xa, y1, 0), (xa, y1, H), (xa, y0, H)], F, [(fu(y0), 0), (fu(y1), 0), (fu(y1), 1), (fu(y0), 1)], (sgn, 0, 0))
    for (ya, n_) in ((y0, -1), (y1, 1)):
        mb.oface([(xa, ya, 0), (xb, ya, 0), (xb, ya, H), (xa, ya, H)], M['side'], [(0, 0), (depth / 4, 0), (depth / 4, H / 4), (0, H / 4)], (0, n_, 0))
        xm = (xa + xb) / 2; mb.oface([(xa, ya, H), (xb, ya, H), (xm, ya, ridge)], M['plaster_w'], [(0, 0), (1, 0), (0.5, 0.5)], (0, n_, 0))
    mb.oface([(xb, y0, 0), (xb, y1, 0), (xb, y1, H), (xb, y0, H)], M['side'], [(0, 0), (W / 4, 0), (W / 4, H / 4), (0, H / 4)], (-sgn, 0, 0))
    xm = (xa + xb) / 2; ov = 0.9
    for (xe, n_) in ((xa + sgn * ov, sgn), (xb - sgn * ov, -sgn)):
        zl = H - 0.35
        rb.oface([(xe, y0 - 0.4, zl), (xe, y1 + 0.4, zl), (xm, y1 + 0.4, ridge), (xm, y0 - 0.4, ridge)], M['kawara_h'], [(0, 0), (W / 2, 0), (W / 2, 2.4), (0, 2.4)], (n_, 0, 1.6))
        rb.oface([(xe, y0 - 0.4, zl - 0.2), (xe, y1 + 0.4, zl - 0.2), (xe, y1 + 0.4, zl), (xe, y0 - 0.4, zl)], M['wood_d'], [(0, 0)] * 4, (n_, 0, 0))
    rb.frustum((xm, y0 - 0.5, ridge + 0.1), (xm, y1 + 0.5, ridge + 0.1), 0.2, 0.2, M['ridge'], seg=6)
    xp = xa + sgn * 1.0                                                           # pent roof
    rb.oface([(xa, y0, 3.55), (xa, y1, 3.55), (xp, y1, 3.05), (xp, y0, 3.05)], M['kawara_h'], [(0, 0), (W / 2, 0), (W / 2, 0.5), (0, 0.5)], (sgn, 0, 2.0))
    rb.oface([(xp, y0, 3.05), (xp, y1, 3.05), (xp, y1, 2.88), (xp, y0, 2.88)], M['wood_d'], [(0, 0)] * 4, (sgn, 0, 0))
    rb.oface([(xa, y0, 3.0), (xa, y1, 3.0), (xp, y1, 2.88), (xp, y0, 2.88)], M['wood'], [(0, 0)] * 4, (0, 0, -1))
    return dict(x=(min(xa, xb), max(xa, xb)), y=(y0, y1), ridge=ridge, xm=xm, pent_x=xp)

def _street(SET, M, C, TX, P):
    mb, rb = MB(), MB(); houses = []
    FM = {}
    def F(nm):
        if nm not in FM: FM[nm] = TX(nm, glow=(nm + '_glow') if P['win_k'] > 0 else None, glow_k=P['win_k'])
        return FM[nm]
    names = [m[0] for m in PT.MACHIYA]; r = random.Random(81)
    for sgn, fx in ((1, -STREET_HW), (-1, STREET_HW)):
        y = STREET_Y0; i = 0 if sgn > 0 else 1
        while y > STREET_Y1:
            w_ = r.choice((6.0, 6.0, 7.0, 5.5)); houses.append(_house(mb, rb, M, F(names[i % 3]), fx, y - w_, y, sgn, ridge=r.choice((7.2, 7.4, 7.0)))); y -= w_ + 0.05; i += 1
    # a row facing the courtyard wall west and east of the gate (outside the yard)
    for (xa, xb) in ((-30.0, -6.0), (6.0, 40.0)):
        x = xa
        while x < xb - 4:
            w_ = 6.0; nm = names[int(x) % 3]
            # front faces +y? keep simple: these face the street plaza in front of the gate (-y side of the wall), set back to y = -40
            hb = dict(x=(x, x + w_), y=(-48.0, -40.0)); houses.append(hb)
            mb.oface([(x, -40.0, 0), (x + w_, -40.0, 0), (x + w_, -40.0, PT.MA_H), (x, -40.0, PT.MA_H)], F(nm), [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 1, 0))
            for xx, n_ in ((x, -1), (x + w_, 1)): mb.oface([(xx, -40.0, 0), (xx, -48.0, 0), (xx, -48.0, PT.MA_H), (xx, -40.0, PT.MA_H)], M['side'], [(0, 0), (2, 0), (2, 1.4), (0, 1.4)], (n_, 0, 0))
            for (ye, n_) in ((-39.1, 1), (-48.9, -1)):
                rb.oface([(x - 0.3, ye, PT.MA_H - 0.35), (x + w_ + 0.3, ye, PT.MA_H - 0.35), (x + w_ + 0.3, -44.0, 7.3), (x - 0.3, -44.0, 7.3)], M['kawara_h'], [(0, 0), (3, 0), (3, 2.4), (0, 2.4)], (0, n_, 1.6))
            for xx, n_ in ((x, -1), (x + w_, 1)): mb.oface([(xx, -40.0, PT.MA_H), (xx, -48.0, PT.MA_H), (xx, -44.0, 7.3)], M['plaster_w'], [(0, 0), (1, 0), (0.5, 0.5)], (n_, 0, 0))
            rb.frustum((x - 0.4, -44.0, 7.4), (x + w_ + 0.4, -44.0, 7.4), 0.2, 0.2, M['ridge'], seg=6)
            rb.oface([(x, -40.0, 3.55), (x + w_, -40.0, 3.55), (x + w_, -39.0, 3.05), (x, -39.0, 3.05)], M['kawara_h'], [(0, 0), (3, 0), (3, 0.5), (0, 0.5)], (0, 1, 2.0))
            x += w_ + 0.05
    mb.obj('street_houses', SET, hull=0.04); rb.obj('street_roofs', SET, hull=0.04)
    STATE['houses'] = houses
    # loose roof tiles on the two street houses nearest street_eye (they hop in a quake)
    tiles = []
    for hsel in houses[:6]:
        if 'pent_x' not in hsel: continue
        y0, y1 = hsel['y']; xp = hsel['pent_x']; sgn = 1 if xp > hsel['x'][0] + 4 else -1
        for k in range(4):
            yy = y0 + 0.8 + k * (y1 - y0 - 1.6) / 3; c = Vector((xp - sgn * 0.25, yy, 3.12 + 0.06))
            piv = _pivot('tile_%d' % len(tiles), SET, tuple(c)); piv['wrest'] = tuple(c)
            m2 = MB(); m2.box(tuple(c - Vector((0.22, 0.16, 0.05))), tuple(c + Vector((0.22, 0.16, 0.05))), M['kawara_h'], tile=(2, 2)); o = m2.obj('tile_%d_mesh' % len(tiles), SET, hull=0.008); _parent(o, piv)
            tiles.append(piv); STATE.setdefault('loose', []).append(dict(ob=piv, kind='hop', amp=1.0, seed=300 + len(tiles)))
    STATE['tiles'] = tiles

# ----------------------------------------------------------------------------- temple hall, town ring, pines
def _hip_roof(rb, mat, x0, x1, y0, y1, h, o_, rz):
    x = (x0 + x1) / 2; y = (y0 + y1) / 2; w_, d_ = x1 - x0, y1 - y0
    c_ = [(x0 - o_, y0 - o_), (x1 + o_, y0 - o_), (x1 + o_, y1 + o_), (x0 - o_, y1 + o_)]
    top = [(x0 + d_ / 2, y), (x1 - d_ / 2, y)] if w_ > d_ else [(x, y0 + w_ / 2), (x, y1 - w_ / 2)]
    cen = Vector((x, y, h))
    for i in range(4):
        a, b = Vector((*c_[i], h - 0.2)), Vector((*c_[(i + 1) % 4], h - 0.2))
        ta = min(top, key=lambda p: (p[0] - a.x) ** 2 + (p[1] - a.y) ** 2); tb = min(top, key=lambda p: (p[0] - b.x) ** 2 + (p[1] - b.y) ** 2)
        pts = [a, b, Vector((*tb, rz)), Vector((*ta, rz))] if ta != tb else [a, b, Vector((*ta, rz))]
        mid = (a + b) / 2; nrm = (mid - cen); nrm.z = 1.2
        rb.oface(pts, mat, [(p.x / 2 + p.y / 2, p.z / 2) for p in pts], nrm)

def _hall(SET, M, C, TX):
    """The temple hall (kondo) west-north-west of the pagoda: stone base, red posts, white walls, a big hip roof."""
    mb, rb = MB(), MB(); x0, x1, y0, y1 = -15.0, -7.0, 0.0, 9.0
    mb.box((x0 - 0.6, y0 - 0.6, 0), (x1 + 0.6, y1 + 0.6, 0.7), M['stone'], tile=(2, 1))
    for (p0, pu, nn) in (((x0, y0), (x1 - x0, 0), (0, -1)), ((x1, y0), (0, y1 - y0), (1, 0)), ((x1, y1), (x0 - x1, 0), (0, 1)), ((x0, y1), (0, y0 - y1), (-1, 0))):
        a = Vector((p0[0], p0[1], 0.7)); u = Vector((pu[0], pu[1], 0)); L_ = u.length
        mb.oface([a, a + u, a + u + Vector((0, 0, 3.6)), a + Vector((0, 0, 3.6))], M['plaster'], [(0, 0), (L_ / 2, 0), (L_ / 2, 1.8), (0, 1.8)], (nn[0], nn[1], 0))
        for k in range(int(L_ / 2.0) + 1):
            p = a + u * (k / int(L_ / 2.0)) + Vector((nn[0], nn[1], 0)) * 0.05; mb.box((p.x - 0.16, p.y - 0.16, 0.7), (p.x + 0.16, p.y + 0.16, 4.3), M['red'])
    mb.box((x0 - 0.1, y0 - 0.1, 3.9), (x1 + 0.1, y1 + 0.1, 4.4), M['red'])
    mb.oface([(x1 + 0.06, 3.2, 0.7), (x1 + 0.06, 5.8, 0.7), (x1 + 0.06, 5.8, 3.4), (x1 + 0.06, 3.2, 3.4)], M['door'], [(0, 0), (1, 0), (1, 1), (0, 1)], (1, 0, 0))
    _hip_roof(rb, M['kawara'], x0, x1, y0, y1, 4.6, 2.0, 8.4)
    mb.obj('hall', SET, hull=0.04); rb.obj('hall_roof', SET, hull=0.04)

def _midtown(SET, M, C, TX, P):
    """Simple town houses (white walls, hip / gable tile roofs) in a ring outside the courtyard and the street rows."""
    r = random.Random(77); mb = MB(); rb = MB(); placed = []
    cams = [Vector(c['loc'][:2]) for c in CAMS.values()]
    walls = [M['plaster'], M['plaster_w'], M['side']]
    tries = 0
    while len(placed) < 90 and tries < 5000:
        tries += 1
        x = r.uniform(-95, 95); y = r.uniform(-120, 95)
        if -21 < x < 33 and -38 < y < 23: continue                                      # courtyard
        if -14 < x < 14 and y < -36: continue                                          # the street and its rows
        if -32 < x < 42 and -50 < y < -38: continue                                    # the row in front of the walls
        w_, d_ = r.uniform(5, 9), r.uniform(5, 8); h_ = r.uniform(3.6, 5.5)
        if any((Vector((x, y)) - c).length < 14 for c in cams) or (Vector((x, y)) - Vector(CAMS['town_wide']['loc'][:2])).length < 30: continue
        if any(abs(x - px) < (w_ + pw) / 2 + 1.2 and abs(y - py) < (d_ + pd) / 2 + 1.2 for (px, py, pw, pd) in placed): continue
        placed.append((x, y, w_, d_)); wm = walls[r.randrange(3)]
        x0, x1, y0, y1 = x - w_ / 2, x + w_ / 2, y - d_ / 2, y + d_ / 2
        for (xa, ya, xb, yb, nn) in ((x0, y0, x1, y0, (0, -1, 0)), (x1, y0, x1, y1, (1, 0, 0)), (x1, y1, x0, y1, (0, 1, 0)), (x0, y1, x0, y0, (-1, 0, 0))):
            L_ = math.hypot(xb - xa, yb - ya); mb.oface([(xa, ya, 0), (xb, yb, 0), (xb, yb, h_), (xa, ya, h_)], wm, [(0, 0), (L_ / 4, 0), (L_ / 4, h_ / 4), (0, h_ / 4)], nn)
        _hip_roof(rb, M['kawara_h'], x0, x1, y0, y1, h_, 0.8, h_ + min(w_, d_) * 0.38)
    mb.obj('town_walls', SET, hull=0.05); rb.obj('town_roofs', SET, hull=0.05)
    STATE['midtown'] = placed

PINES = [(-12.5, -25.0, 1.0), (-13.0, 12.5, 1.15), (24.5, -27.0, 0.9), (24.0, 13.5, 1.1), (-7.5, -12.5, 0.8), (8.0, 11.0, 0.85),
         (-14.0, -50.0, 1.1), (14.5, -52.0, 1.0), (-26.0, -20.0, 1.2), (36.0, -8.0, 1.2), (-22.0, 26.0, 1.3), (34.0, 28.0, 1.2)]
def _pines(SET, M):
    """Japanese black pines: a leaning, kinked trunk and flat cloud-like needle pads (dark green), lit top, shaded underside."""
    r = random.Random(87); mb = MB()
    for (x, y, s) in PINES:
        h = 7.5 * s; lean = Vector((r.uniform(-1, 1), r.uniform(-1, 1), 0)).normalized() * 1.6 * s; pts = [Vector((x, y, 0))]
        for k in range(1, 6):
            t = k / 5; pts.append(Vector((x, y, 0)) + lean * math.sin(t * 2.2) + Vector((r.uniform(-0.3, 0.3), r.uniform(-0.3, 0.3), h * t)))
        for k, (p0, p1) in enumerate(zip(pts, pts[1:])): mb.frustum(p0, p1, 0.4 * s * (1 - 0.15 * k), 0.4 * s * (1 - 0.15 * (k + 1)), M['bark'], seg=8)
        for k in range(r.randint(4, 6)):
            base = pts[r.randint(2, 5)]; d = Vector((r.uniform(-1, 1), r.uniform(-1, 1), 0)).normalized(); L_ = r.uniform(1.0, 2.6) * s
            tip = base + d * L_ + Vector((0, 0, r.uniform(-0.3, 0.6)))
            mb.frustum(base, tip, 0.13 * s, 0.08 * s, M['bark'], seg=5)
            rx, ry = r.uniform(1.2, 2.0) * s, r.uniform(0.9, 1.5) * s; seg = 14
            top = [tip + Vector((rx * math.cos(2 * math.pi * i / seg) * r.uniform(0.85, 1.1), ry * math.sin(2 * math.pi * i / seg) * r.uniform(0.85, 1.1), 0)) for i in range(seg)]
            cz = tip + Vector((0, 0, 0.55 * s))
            for i in range(seg):
                a, b = top[i], top[(i + 1) % seg]
                mb.face([a, b, cz], M['pine']); mb.face([b, a, tip - Vector((0, 0, 0.25 * s))], M['pine_d'])
    mb.obj('pines', SET, hull=0.05)

# ----------------------------------------------------------------------------- lanterns
def _lanterns(SET, M, C, TX, E, P):
    """Hanging paper lanterns under the street pent roofs and on the gate (loose props: they swing in a quake), stone lanterns
    in the courtyard, warm light pools on the ground at night."""
    hooks = []
    for hs in STATE['houses']:
        if 'pent_x' not in hs: continue
        y0, y1 = hs['y']
        if y0 < -70: continue
        hooks.append(Vector((hs['pent_x'] + (0.3 if hs['pent_x'] > 0 else -0.3), (y0 + y1) / 2, 2.9)))
    hooks += [Vector((-2.0, YARD[2] - 1.3, 4.6)), Vector((2.0, YARD[2] - 1.3, 4.6))]
    STATE['lanterns'] = []
    pool = MB(); pm = mat_emit('PGD_%s_pool' % STATE['preset'], image=STATE['tx']['pool'], strength=P['pool_k'], alpha=True) if P['pool_k'] > 0 else None
    for i, hk in enumerate(hooks):
        big = i >= len(hooks) - 2; s = 1.4 if big else 1.0
        piv = _pivot('lantern_%02d' % i, SET, tuple(hk)); piv['wrest'] = tuple(hk)
        mb = MB(); c = hk - Vector((0, 0, 0.55 * s))
        mb.frustum(hk, hk - Vector((0, 0, 0.18 * s)), 0.015, 0.015, M['wood_d'], seg=4)
        mb.frustum(hk - Vector((0, 0, 0.18 * s)), hk - Vector((0, 0, 0.26 * s)), 0.2 * s, 0.22 * s, M['wood_d'], seg=12)
        prof = [(0.22, 0.26), (0.32, 0.38), (0.36, 0.55), (0.32, 0.72), (0.22, 0.84)]
        for (r0, z0), (r1, z1) in zip(prof, prof[1:]):
            mb.frustum(hk - Vector((0, 0, z0 * s)), hk - Vector((0, 0, z1 * s)), r0 * s, r1 * s, M['lantern'], seg=14, cap0=False, cap1=False, uv_wrap=(2, (z1 - z0) / 0.58))
        mb.frustum(hk - Vector((0, 0, 0.84 * s)), hk - Vector((0, 0, 0.92 * s)), 0.22 * s, 0.2 * s, M['wood_d'], seg=12)
        o = mb.obj('lantern_%02d_mesh' % i, SET, hull=0.01); _parent(o, piv)
        if P['lamp_k'] > 0: o.visible_shadow = False
        STATE['lanterns'].append(piv); STATE.setdefault('loose', []).append(dict(ob=piv, kind='swing', amp=10.0 if not big else 6.0, seed=200 + i))
        if pm is not None:
            pool.quad((hk.x - 2.2 * s, hk.y - 2.2 * s, 0.03), (4.4 * s, 0, 0), (0, 4.4 * s, 0), pm)
    # stone lanterns (toro) along the approach
    mb = MB(); win = MB()
    for (x, y) in ((-3.0, -12.0), (3.0, -12.0), (-3.0, -20.0), (3.0, -20.0)):
        mb.box((x - 0.6, y - 0.6, 0), (x + 0.6, y + 0.6, 0.3), M['stone_d']); mb.frustum((x, y, 0.3), (x, y, 1.6), 0.22, 0.2, M['stone'], seg=8)
        mb.box((x - 0.5, y - 0.5, 1.6), (x + 0.5, y + 0.5, 1.8), M['stone']); mb.box((x - 0.36, y - 0.36, 1.8), (x + 0.36, y + 0.36, 2.5), M['stone'])
        mb.frustum((x, y, 2.5), (x, y, 2.95), 0.85, 0.08, M['stone_d'], seg=6); mb.sphere((x, y, 3.0), 0.12, M['stone'], seg=8, rings=5)
        for n in NRM:
            c = Vector((x, y, 2.15)) + n * 0.37; t = TAN(n)
            win.oface([c - t * 0.17 - Vector((0, 0, 0.2)), c + t * 0.17 - Vector((0, 0, 0.2)), c + t * 0.17 + Vector((0, 0, 0.2)), c - t * 0.17 + Vector((0, 0, 0.2))], M['lamp_glow'] if P['lamp_k'] > 0 else M['wood_d'], [(0, 0)] * 4, n)
        if pm is not None: pool.quad((x - 2.0, y - 2.0, 0.03), (4.0, 0, 0), (0, 4.0, 0), pm)
    # red banners (nobori) along the approach and in the street (ref a t0040)
    bn = MB(); cloth = C('#c8302a'); white = C('#f2ead8')
    for (x, y) in ((-1.9, -21.5), (1.9, -21.5), (-1.9, -27.5), (1.9, -27.5), (-3.3, -37.0), (3.3, -42.0), (-3.3, -55.0), (3.3, -62.0)):
        sx = -1 if x < 0 else 1
        bn.frustum((x, y, 0), (x, y, 4.3), 0.05, 0.04, M['wood_d'], seg=6); bn.frustum((x, y, 4.0), (x - sx * 0.75, y, 4.0), 0.03, 0.03, M['wood_d'], seg=4)
        bn.oface([(x - sx * 0.05, y, 1.5), (x - sx * 0.75, y, 1.5), (x - sx * 0.75, y, 4.0), (x - sx * 0.05, y, 4.0)], cloth, [(0, 0)] * 4, (0, -1, 0))
        bn.oface([(x - sx * 0.12, y - 0.01, 3.0), (x - sx * 0.68, y - 0.01, 3.0), (x - sx * 0.68, y - 0.01, 3.2), (x - sx * 0.12, y - 0.01, 3.2)], white, [(0, 0)] * 4, (0, -1, 0))
    bn.obj('banners', SET, hull=0.012)
    mb.obj('toro', SET, hull=0.02); w2 = win.obj('toro_windows', SET); w2.visible_shadow = False
    if pm is not None: po = pool.obj('light_pools', SET); po.visible_shadow = False

# ----------------------------------------------------------------------------- animated controls
def _keyp(ob, path, frame, interp='BEZIER'):
    if frame is not None: T._key(ob, path, frame, interp)

def sway_offsets(amp, phase=math.pi / 2):
    """x offset (D) and tilt (rad about y) of the five storeys for sway amplitude amp at oscillation phase (rad):
    offset_i = amp x (i + 1) / 5 x (-1)^i x sin(phase): adjacent storeys opposite, the top storey moves amp."""
    s = math.sin(phase); offs = [amp * (i + 1) / 5.0 * (1 if i % 2 == 0 else -1) * s for i in range(5)]
    tilts = []; prev = 0.0
    for i, o in enumerate(offs):
        tilts.append(math.atan2(o - prev, 3.2) * 0.35); prev = o
    return offs, tilts

def set_sway(amp, phase=math.pi / 2, frame=None, pillar=True, interp='BEZIER'):
    """Snake dance of the loose storeys: storey i moves amp x (i+1)/5 x (-1)^i x sin(phase) along x (adjacent storeys opposite,
    amplitude growing upward, the top storey and its finial move amp D) and tilts with it. pillar=True also swings the hanging
    pillar the other way (its foot moves opposite to the top storey: foot x = -0.3 x top offset). Keys location and rotation of
    each storey (Bezier) with frame=N; call it on every frame of a shot with the phase of that frame."""
    offs, tilts = sway_offsets(float(amp), phase)
    for piv, o, t in zip(STATE['storeys'], offs, tilts):
        piv.location = (o, 0.0, piv['wrest'][2]); piv.rotation_euler = (0.0, t, 0.0)
        _keyp(piv, 'location', frame, interp); _keyp(piv, 'rotation_euler', frame, interp)
    STATE['sway'] = (amp, phase)
    if pillar:
        L_ = CHAIN_TOP - FOOT_Z; foot = -0.3 * offs[4] - offs[4]                    # foot offset relative to the (moving) top
        set_pillar_swing(math.degrees(tilts[4]) + math.degrees(math.atan2(foot, L_)), frame, interp)

def set_cutaway(on, frame=None):
    """True: hide the front (-y) walls, doors, railings, roof quarters, soffits and fascias of all five storeys, so the inside is
    seen: the floors with their holes, the hanging pillar, its chain under the top beam, the gap over the foundation stone."""
    T._show(STATE['cut_objs'], not on, frame); STATE['cutaway'] = bool(on)

def set_pillar_swing(angle_deg, frame=None, interp='BEZIER'):
    """Swing of the hanging pillar about its chain anchor (y axis); + moves the foot toward +x. 1 deg moves the foot 0.25 D
    (one gap height). Keys the rotation (Bezier) with frame=N."""
    pp = STATE['pillar']; pp.rotation_euler = (0.0, -math.radians(angle_deg), 0.0); _keyp(pp, 'rotation_euler', frame, interp)

def set_crack(level, frame=None):
    """Crack at the nailed joint of the tower's front face: 0 none, 1 hairline, 2 finger-wide, 3 split open. Visibility keyed
    (constant) with frame=N. Decal layers: crack 1 < patch 1 < crack 2 < patch 2 < crack 3, so a later crack runs through an
    earlier patch."""
    lv = int(level); STATE['crack'] = lv; D = STATE['decals']
    for k in (1, 2, 3): T._show([D['crack_%d' % k]], lv == k and STATE.get('collapse', 0) < 0.05, frame)

def set_plaster(level, frame=None):
    """Plaster patches over the crack: 0 none, 1 the small patch (over the hairline), 2 both (the bigger second patch)."""
    lv = int(level); STATE['plaster'] = lv; D = STATE['decals']
    for k in (1, 2): T._show([D['patch_%d' % k]], lv >= k and STATE.get('collapse', 0) < 0.05, frame)

def _ss(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a))); return t * t * (3 - 2 * t)

def collapse_pose(u):
    """Angle (deg) of the tower's top half about the hinge (east edge of the snap) and the hinge drop (D) for collapse u."""
    if u <= 0.15: ang = 5.0 * (u / 0.15) ** 2
    elif u <= 0.62: ang = 5.0 + 70.0 * ((u - 0.15) / 0.47) ** 2
    else: ang = 75.0 + 17.0 * _ss(0.62, 0.8, u)
    drop = (Z_SNAP - 2.4) * _ss(0.55, 0.8, u)
    return ang, drop

def set_collapse(u, frame=None, settle=None, dust=True):
    """The rigid tower snaps at its joint (z 11.3) like a ruler: u 0 standing; 0.05..0.15 the joint opens and the top leans east
    (puffs of plaster dust at the break); 0.15..0.62 the top half topples over its east edge; 0.62..0.8 it falls and hits the
    ground east of the tower; from 0.7 the rubble pile rises out of the dust, timbers and plaster slabs fly from the break to the
    pile (0.18..1); a dust column climbs from the landing to about z 25 at u = 1 (ref a t0104). settle (0..1): a low dust bank
    lying over the ruins (the morning after); default 0. dust=False hides the burst / column dust (the morning after). With frame=N every transform / visibility is keyed (positions Bezier,
    visibility constant), so call it on each frame of the shot."""
    u = max(0.0, min(1.0, float(u))); STATE['collapse'] = u; tw = STATE['tower']
    ang, drop = collapse_pose(u); piv = tw['pivot']
    piv.location = (HINGE[0], HINGE[1], HINGE[2] - drop); piv.rotation_euler = (math.radians(ang), 0.0, 0.0); _keyp(piv, 'location', frame); _keyp(piv, 'rotation_euler', frame)
    T._show([tw['upper']], u < 0.82, frame); T._show([tw['stump']], u >= 0.05, frame)
    set_crack(STATE.get('crack', 0), frame); set_plaster(STATE.get('plaster', 0), frame)
    rb = STATE['rubble']; g = _ss(0.68, 0.95, u); rb['root'].scale = (1.0, 1.0, max(0.02, g)); _keyp(rb['root'], 'scale', frame); T._show([rb['mesh']], u >= 0.68, frame)
    for d in STATE['debris']:
        t = (u - d['t0']) / d['dur']; vis = 0.0 < t < 1.0; t = max(0.0, min(1.0, t))
        p = d['s'].lerp(d['e'], t) + Vector((0, 0, d['arc'] * 4 * t * (1 - t)))
        piv_ = d['piv']; piv_.location = p; piv_.rotation_euler = tuple(x * t for x in d['spin']); _keyp(piv_, 'location', frame); _keyp(piv_, 'rotation_euler', frame)
        T._show([d['ob']], vis, frame)
    for d in STATE['dust']:
        t = max(0.0, min(1.0, (u - d['t0']) / 0.3)); ob = d['ob']
        if d['kind'] == 'break': sc = d['size'] * (0.3 + 0.7 * t) * (1 - _ss(0.55, 0.75, u)); rise = 1.5 * t
        elif d['kind'] == 'ground': sc = d['size'] * t; rise = 0.6 * t
        else: sc = d['size'] * t; rise = -6.0 * (1 - t)
        ob.location = d['c'] + Vector((0, 0, rise)); s = max(0.001, sc); ob.scale = (s, s, s * 0.85)
        _keyp(ob, 'location', frame); _keyp(ob, 'scale', frame); T._show([ob], sc > 0.05, frame)
    if not dust:
        for d in STATE['dust']: T._show([d['ob']], False, frame)
    st = 0.0 if settle is None else max(0.0, min(1.0, float(settle)))
    for d in STATE['settle']:
        s = max(0.001, d['size'] * st); d['ob'].scale = (s * 1.6, s * 1.2, s * 0.45); _keyp(d['ob'], 'scale', frame); T._show([d['ob']], st > 0.02, frame)

def _hash01(seed, k):
    return random.Random(seed * 7919 + k).random()

def set_quake(strength, frame=None):
    """Loose props shake (camera-independent; shots add their own camera shake): hanging lanterns and the pagoda's wind bells swing
    about their hooks (up to 10..14 deg at strength 1), loose roof tiles hop and twist. Each prop has its own frequency and phase,
    so the motion is a deterministic function of the frame: call it on every frame with the strength of that frame
    (0 = rest). Without frame the scene's current frame gives the phase and nothing is keyed."""
    s = float(strength); f = bpy.context.scene.frame_current if frame is None else frame; tsec = f / 30.0; STATE['quake'] = s
    for L in STATE.get('loose', []):
        ob = L['ob']; sd = L['seed']; fr = 0.9 + 1.3 * _hash01(sd, 1); ph = 2 * math.pi * _hash01(sd, 2)
        if L['kind'] == 'swing':
            ax = math.radians(L['amp'] * s * math.sin(2 * math.pi * fr * tsec + ph)); ay = math.radians(L['amp'] * 0.6 * s * math.sin(2 * math.pi * fr * 1.37 * tsec + ph * 0.7))
            ob.rotation_euler = (ax, ay, 0.0); _keyp(ob, 'rotation_euler', frame, 'LINEAR')
        else:
            w = Vector(ob['wrest']); hop = 0.06 * s * abs(math.sin(2 * math.pi * fr * 2.1 * tsec + ph)); ob.location = (w.x, w.y, w.z + hop)
            ob.rotation_euler = (math.radians(6 * s * math.sin(2 * math.pi * 3.1 * fr * tsec + ph)), 0.0, math.radians(8 * s * math.sin(2 * math.pi * 2.3 * fr * tsec + ph * 1.3)))
            _keyp(ob, 'location', frame, 'LINEAR'); _keyp(ob, 'rotation_euler', frame, 'LINEAR')

# ----------------------------------------------------------------------------- anchors and cameras
APPRENTICE_MARK = (-1.6, -11.5, 0.0); MASTER_MARK = (9.6, -10.8, 0.0)
YARD_MARKS = [(-5.0, -16.0, 0.0), (3.6, -18.5, 0.0), (11.0, -17.0, 0.0), (-2.2, -22.5, 0.0), (7.0, -24.0, 0.0)]
STREET_MARKS = [(-1.4, -40.0, 0.0), (1.9, -44.5, 0.0), (-0.6, -49.0, 0.0), (2.4, -38.0, 0.0), (-2.4, -46.5, 0.0)]
PILE_MARK = (12.9, -9.4, round(pile_height(12.9, -9.4), 3))
PLATFORM_MARKS = [(-1.4, -4.4, PLAT_Z), (1.6, -4.6, PLAT_Z)]

def _cam(loc, look):
    return dict(loc=tuple(round(v, 3) for v in loc), look_at=tuple(round(v, 3) for v in look), lens=22)
CAMS = dict(
    pagoda_low=_cam((-0.9, -16.0, 1.0), (0.0, 0.0, 12.0)),
    two_buildings=_cam((6.9, -31.0, 3.4), (7.4, 0.0, 9.6)),
    street_eye=_cam((1.3, -58.0, 2.5), (0.6, -20.0, 6.4)),
    cutaway_insert=_cam((0.9, -3.4, 1.36), (0.0, 0.0, 1.62)),
    crack_insert=_cam((TWX - 0.4, -5.4, 11.4), (JOINT[0], JOINT[1], JOINT[2])),
    town_wide=_cam((-22.0, -58.0, 24.0), (6.0, -2.0, 6.0)),
    rubble_dawn=_cam((15.6, -13.4, 3.6), (0.0, 0.0, 9.0)),
    cutaway_full=_cam((0.6, -24.0, 9.6), (0.0, 0.0, 10.6)),
)
CAM_NOTES = dict(
    pagoda_low='from the courtyard path 9.4 D in front of the pagoda, 1 D high, up the five eaves to the bronze finial (sway reads as the eaves sliding against each other)',
    two_buildings='wide from the courtyard 30 D out: the pagoda left and the master\'s tower right, full height side by side, wall and pines behind (comparison / sway / collapse)',
    street_eye='eye level in the street 58 D south of the gate: machiya rows and hanging lanterns either side, actors at street_marks in depth, the gate, pagoda and tower beyond',
    cutaway_insert='inside the ground storey (cutaway on): the pillar foot floating one palm (0.25 D) over the foundation stone, the pillar rising into the dark',
    crack_insert='close on the tower\'s front face at the nailed joint (z 11.3): the crack / plaster decals, the joint iron plate',
    town_wide='establishing from 26 D up south-west of the town: the street, the walled courtyard, pagoda and tower, the hall, the town ring and the painted mountains',
    rubble_dawn='from the edge of the rubble pile (the fallen top half) looking west at the pagoda over broken timbers (DAWN, set_collapse(1, settle=1))',
    cutaway_full='extra: the whole pagoda in cutaway from 24 D: every storey open, the pillar from the chain under the top beam down to the gap',
)

def anchors():
    P = STATE['P']; kd = Vector(P['key_dir']).normalized()
    return dict(
        apprentice_mark=APPRENTICE_MARK, master_mark=MASTER_MARK, yard_marks=list(YARD_MARKS), street_marks=list(STREET_MARKS), pile_mark=PILE_MARK,
        platform_marks=list(PLATFORM_MARKS),
        pagoda=dict(center=(0.0, 0.0, 0.0), platform=dict(half_width=PLAT_HW, top=PLAT_Z), storeys=[dict(half_width=hw, base_z=z0, wall_top=z0 + h, eave_out=hw + ov) for (hw, z0, h, ov) in STOREYS],
                    apex=APEX_Z, sorin_top=SORIN_TOP, pillar=dict(radius=PILLAR_R, foot_z=FOOT_Z, top_z=PILLAR_TOP, chain_anchor=(0.0, 0.0, CHAIN_TOP), soseki_top=SOSEKI_TOP, gap=GAP),
                    front='-y'),
        tower=dict(center=(TWX, TWY, 0.0), half_width=T_HW, plinth=T_PLINTH, storey_h=T_ST, wall_top=T_WALL_TOP, apex=T_APEX, snap_z=Z_SNAP, joint=JOINT, hinge=HINGE,
                   falls_toward='-y', pile_center=(PILE_C[0], PILE_C[1], 0.0), pile_radii=PILE_R, pile_height=PILE_H),
        yard=dict(x=(YARD[0], YARD[1]), y=(YARD[2], YARD[3]), wall_height=2.95), gate=dict(STATE['gate']),
        street=dict(half_width=STREET_HW, y=(STREET_Y1, STREET_Y0), pent_roof_z=(2.88, 3.55)),
        lanterns=[tuple(round(c, 3) for c in L['wrest']) for L in STATE['lanterns']], pines=list(PINES),
        key_dir=tuple(kd), preset=STATE['preset'], sun_elevation_deg=P['sun_elev'],
        key_note='DAY / NIGHT key from the south-west behind the courtyard cameras (screen-left), shadows fall right and away; SUNSET from the west, 11 deg; DAWN from the east-south-east, 14 deg',
        cams={k: dict(v) for k, v in CAMS.items()}, cam_notes=dict(CAM_NOTES),
        render=dict(samples_final=12, resolution=(720, 1280), threads=2, sun_angle_deg=P['sun_angle'], key=P['key'], shade=P['shade'], lift=P['lift'], toon=P['toon']))

# ----------------------------------------------------------------------------- placeholder actors (stills and tests only)
T.PH.update(
    apprentice=('beach_kid', dict(yaw=-0.3, expr='determined', arm_r='down', arm_l='down', legs='stand'), 2.4),
    master=('boss', dict(yaw=0.35, head_roll=-4, expr='smug', arm_l='down', arm_r='hip', legs='stand'), 3.1),
    towns_a=('senior_b', dict(yaw=0.2, expr='neutral', arm_l='down', arm_r='down', legs='stand'), 2.9),
    towns_b=('beach_woman', dict(yaw=-0.25, expr='neutral', arm_l='down', arm_r='down', legs='stand'), 2.9),
    towns_c=('senior_a', dict(yaw=0.4, expr='neutral', arm_l='down', arm_r='down', legs='stand'), 3.0))
placeholder_actor = T.placeholder_actor

def stage_placeholders(A, where, cam_loc):
    """'pagoda': apprentice on the platform front, a townsman; 'yard': apprentice, master and two townspeople in the courtyard;
    'street': townspeople at street_marks and the apprentice; 'pile': the master standing on the rubble; 'none'."""
    T._clear_actors()
    if where == 'none': return []
    if where == 'pagoda': spots = [('apprentice', (0.9, -6.6, 0.0)), ('towns_a', (-2.4, -7.4, 0.0))]
    elif where == 'yard': spots = [('apprentice', (4.2, -19.5, 0.0)), ('master', (9.0, -22.0, 0.0)), ('towns_b', A['yard_marks'][1]), ('towns_c', (-1.0, -14.0, 0.0))]
    elif where == 'street': spots = [('towns_a', A['street_marks'][0]), ('towns_b', A['street_marks'][1]), ('towns_c', A['street_marks'][2]), ('apprentice', (-1.7, -50.5, 0.0)), ('towns_a', A['street_marks'][3])]
    elif where == 'pile': spots = [('master', A['pile_mark'])]
    else: spots = [('apprentice', A['apprentice_mark']), ('master', A['master_mark']), ('towns_a', A['yard_marks'][0]), ('towns_b', A['yard_marks'][2])]
    out = []
    for i, (role, mk) in enumerate(spots):
        d = Vector(cam_loc) - Vector(mk); el = math.degrees(math.atan2(d.z - 1.5, math.hypot(d.x, d.y)))
        out.append(placeholder_actor(role, mk, face_to=cam_loc, tilt=max(0.0, el - 35) * 0.6, name='actor_%s_%d' % (role, i)))
    return out

STAGING = dict(pagoda_low='pagoda', two_buildings='yard', street_eye='street', cutaway_insert='none', crack_insert='none', town_wide='wide', rubble_dawn='pile', cutaway_full='none')
CAM_STATE = dict(cutaway_insert=dict(cutaway=True), cutaway_full=dict(cutaway=True))

def apply_cam_state(nm, preset):
    """Set-state used for the contract stills of a camera: cutaway on for the cutaway cameras, crack 2 + patch 1 on the tower for
    crack_insert (story year 3), the fallen tower with settled dust for rubble_dawn (and for every camera under DAWN)."""
    set_cutaway(nm in ('cutaway_insert', 'cutaway_full'))
    set_crack(2 if nm == 'crack_insert' else 0); set_plaster(1 if nm == 'crack_insert' else 0)
    if preset == 'DAWN' or nm == 'rubble_dawn': set_collapse(1.0, settle=1.0 if preset == 'DAWN' else 0.0, dust=False)
    else: set_collapse(0.0)

# ----------------------------------------------------------------------------- CLI
def _load(): return ' '.join('%.2f' % v for v in os.getloadavg())

def cli_stills(presets, quality='preview', outdir=None, cams=None):
    outdir = outdir or os.path.join(WORK, 'stills'); os.makedirs(outdir, exist_ok=True)
    for pr in presets:
        A = build(pr); sc = bpy.context.scene; setup_render(sc, quality)
        for nm, cs in A['cams'].items():
            if cams and nm not in cams: continue
            apply_cam_state(nm, pr); make_camera(cs); apply_dof(nm); stage_placeholders(A, STAGING[nm], cs['loc'])
            w, c = render(os.path.join(outdir, '%s_%s.png' % (pr, nm))); print('%s %s: %.1f s wall, %.1f s cpu, load %s' % (pr, nm, w, c, _load()), flush=True)

def cli_tests(preset='DAY', quality='preview'):
    """Sway / pillar / crack / collapse / quake test stills into pagoda_work/tests."""
    out = os.path.join(WORK, 'tests'); os.makedirs(out, exist_ok=True)
    A = build(preset); sc = bpy.context.scene; setup_render(sc, quality); T._clear_actors()
    cs = A['cams']['two_buildings']; make_camera(cs)
    for amp in (0.0, 0.5, 1.0, 1.5):
        set_sway(amp, math.pi / 2); render(os.path.join(out, 'sway_two_buildings_a%03d.png' % int(amp * 100)))
    set_sway(1.0, -math.pi / 2); render(os.path.join(out, 'sway_two_buildings_a100_neg.png'))
    set_sway(1.0, math.pi / 2); make_camera(A['cams']['pagoda_low']); render(os.path.join(out, 'sway_pagoda_low_a100.png'))
    set_sway(0.0); set_cutaway(True)
    for ang in (0.0, 3.0, -3.0):
        set_pillar_swing(ang); make_camera(A['cams']['cutaway_insert']); render(os.path.join(out, 'pillar_insert_%+d.png' % int(ang)))
    set_sway(1.0, math.pi / 2); make_camera(A['cams']['cutaway_full']); render(os.path.join(out, 'pillar_full_sway100.png'))
    set_sway(0.0); set_cutaway(False)
    make_camera(A['cams']['crack_insert'])
    for (cr, pl) in ((1, 0), (1, 1), (2, 1), (2, 2), (3, 2)):
        set_crack(cr); set_plaster(pl); render(os.path.join(out, 'crack_%d_plaster_%d.png' % (cr, pl)))
    set_crack(0); set_plaster(0); make_camera(A['cams']['two_buildings'])
    for u in (0.1, 0.3, 0.5, 0.7, 0.85, 1.0):
        set_collapse(u); render(os.path.join(out, 'collapse_u%03d.png' % int(u * 100)))
    set_collapse(0.0); make_camera(A['cams']['street_eye'])
    for f in (1, 6): sc.frame_set(f); set_quake(1.0, frame=f); sc.frame_set(f); render(os.path.join(out, 'quake_street_f%02d.png' % f))

def cli_final(preset='DAY', cams=None):
    out = os.path.join(WORK, 'final'); os.makedirs(out, exist_ok=True)
    A = build(preset); sc = bpy.context.scene; setup_render(sc, 'final'); res = {}
    for nm, cs in A['cams'].items():
        if cams and nm not in cams: continue
        apply_cam_state(nm, preset); make_camera(cs); apply_dof(nm); stage_placeholders(A, STAGING[nm], cs['loc'])
        w, c = render(os.path.join(out, '%s_%s.png' % (preset, nm))); res[nm] = (round(w, 1), round(c, 1)); print('final %s %s: %.1f s wall, %.1f s cpu, load %s' % (preset, nm, w, c, _load()), flush=True)
    return res

def digest():
    """Digest of object names, transforms, vertices, UVs, materials and anchors (determinism check)."""
    h = hashlib.sha1()
    for ob in sorted(bpy.context.scene.objects, key=lambda o: o.name):
        h.update(ob.name.encode()); h.update(repr([round(x, 5) for c in ob.matrix_world.col for x in c]).encode())
        if ob.type == 'MESH':
            me = ob.data; co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', co); h.update(np.round(co, 5).tobytes())
            if me.uv_layers: uv = np.empty(len(me.uv_layers[0].data) * 2); me.uv_layers[0].data.foreach_get('uv', uv); h.update(np.round(uv, 5).tobytes())
            h.update(repr([m.name if m else '' for m in me.materials]).encode())
    h.update(json.dumps(STATE.get('A', {}), sort_keys=True, default=str).encode())
    return h.hexdigest()

# ============================================================================= v2 (pagoda_REVIEW2): open base, warm interior, ornament,
# dressing, in-scene warm light, the dragon-bronze pillar foot, depth of field
LAMPS_IN = [(-1.7, 1.5, PLAT_Z + 1.85), (1.7, 1.5, PLAT_Z + 1.85), (-1.55, -1.05, PLAT_Z + 1.5), (1.55, -1.05, PLAT_Z + 1.5)]   # warm flames in the ground storey
FIRE_BOWLS = [(-2.55, -4.6), (2.6, -4.7)]                     # kagaribi on the platform, in front of the outer bays
GLOW_K = dict(DAY=1.0, SUNSET=1.15, NIGHT=1.5, DAWN=1.0)      # strength of the painted lamp glow on the interior / pillar
FLAME_K = dict(DAY=4.0, SUNSET=4.0, NIGHT=4.5, DAWN=4.0)

def _out_shader(m):
    """(node, socket) feeding the material output, and the AddShader of mat_lit (key + painted shade)."""
    nt = m.node_tree; add = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeAddShader']
    return nt, (add[0] if add else None)

def _art(nt):
    for n in nt.nodes:
        if n.bl_idname == 'ShaderNodeTexImage' and n.image is not None: return n.outputs['Color']
    for n in nt.nodes:
        if n.bl_idname == 'ShaderNodeRGB': return n.outputs[0]
    return None

def _extra(m, glow=None, spec=None, glossy=None):
    """Add painted warm-light terms to a mat_lit material (noise free, no light objects):
    glow  = (points, rgb, k, radius): art x rgb x k x sum_i wrap(N.L_i) x r^2 / (r^2 + d_i^2)  (warm lamp bounce / rim)
    spec  = (points, rgb, k, power):  rgb x k x sum_i max(N.H_i, 0)^power x falloff_i      (glossy highlight of the lamps)
    glossy = (rgb, k, roughness): a real GGX lobe for the one key (shadowed sun / moon glints on gold and bronze)."""
    nt, add = _out_shader(m)
    if add is None: return m
    N = nt.nodes.new; L = nt.links.new; geo = N('ShaderNodeNewGeometry'); terms = []
    def falloff(p, r):
        d = N('ShaderNodeVectorMath'); d.operation = 'SUBTRACT'; d.inputs[0].default_value = tuple(p); L(geo.outputs['Position'], d.inputs[1])
        ln = N('ShaderNodeVectorMath'); ln.operation = 'LENGTH'; L(d.outputs['Vector'], ln.inputs[0])
        sq = N('ShaderNodeMath'); sq.operation = 'MULTIPLY'; L(ln.outputs['Value'], sq.inputs[0]); L(ln.outputs['Value'], sq.inputs[1])
        de = N('ShaderNodeMath'); de.operation = 'ADD'; de.inputs[1].default_value = r * r; L(sq.outputs[0], de.inputs[0])
        f = N('ShaderNodeMath'); f.operation = 'DIVIDE'; f.inputs[0].default_value = r * r; L(de.outputs[0], f.inputs[1])
        nd = N('ShaderNodeVectorMath'); nd.operation = 'NORMALIZE'; L(d.outputs['Vector'], nd.inputs[0])
        return f.outputs[0], nd.outputs['Vector']
    def chain_sum(vals):
        s = vals[0]
        for v in vals[1:]:
            a = N('ShaderNodeMath'); a.operation = 'ADD'; L(s, a.inputs[0]); L(v, a.inputs[1]); s = a.outputs[0]
        return s
    if glow:
        pts, rgb, k, r = glow; vals = []
        for p in pts:
            f, nd = falloff(p, r)
            dt = N('ShaderNodeVectorMath'); dt.operation = 'DOT_PRODUCT'; L(geo.outputs['Normal'], dt.inputs[0]); L(nd, dt.inputs[1])
            wr = N('ShaderNodeMath'); wr.operation = 'MULTIPLY_ADD'; wr.use_clamp = True; wr.inputs[1].default_value = 0.65; wr.inputs[2].default_value = 0.35; L(dt.outputs['Value'], wr.inputs[0])
            mu = N('ShaderNodeMath'); mu.operation = 'MULTIPLY'; L(wr.outputs[0], mu.inputs[0]); L(f, mu.inputs[1]); vals.append(mu.outputs[0])
        s = chain_sum(vals); art = _art(nt)
        sc = N('ShaderNodeVectorMath'); sc.operation = 'SCALE'; L(s, sc.inputs['Scale'])
        if art is not None: L(art, sc.inputs[0])
        else: sc.inputs[0].default_value = (1, 1, 1)
        cm = N('ShaderNodeVectorMath'); cm.operation = 'MULTIPLY'; cm.inputs[1].default_value = tuple(c * k for c in rgb); L(sc.outputs['Vector'], cm.inputs[0])
        terms.append(cm.outputs['Vector'])
    if spec:
        pts, rgb, k, pw = spec; vals = []
        for p in pts:
            f, nd = falloff(p, 2.2)
            h = N('ShaderNodeVectorMath'); h.operation = 'ADD'; L(nd, h.inputs[0]); L(geo.outputs['Incoming'], h.inputs[1])
            hn = N('ShaderNodeVectorMath'); hn.operation = 'NORMALIZE'; L(h.outputs['Vector'], hn.inputs[0])
            dt = N('ShaderNodeVectorMath'); dt.operation = 'DOT_PRODUCT'; L(geo.outputs['Normal'], dt.inputs[0]); L(hn.outputs['Vector'], dt.inputs[1])
            mx = N('ShaderNodeMath'); mx.operation = 'MAXIMUM'; mx.inputs[1].default_value = 0.0; L(dt.outputs['Value'], mx.inputs[0])
            pwn = N('ShaderNodeMath'); pwn.operation = 'POWER'; pwn.inputs[1].default_value = pw; L(mx.outputs[0], pwn.inputs[0])
            mu = N('ShaderNodeMath'); mu.operation = 'MULTIPLY'; L(pwn.outputs[0], mu.inputs[0]); L(f, mu.inputs[1]); vals.append(mu.outputs[0])
        s = chain_sum(vals)
        sc = N('ShaderNodeVectorMath'); sc.operation = 'SCALE'; sc.inputs[0].default_value = tuple(c * k for c in rgb); L(s, sc.inputs['Scale'])
        terms.append(sc.outputs['Vector'])
    last = add.outputs['Shader']; users = [l.to_socket for l in list(nt.links) if l.from_socket == last]
    if terms:
        col = terms[0]
        for t in terms[1:]:
            a = N('ShaderNodeVectorMath'); a.operation = 'ADD'; L(col, a.inputs[0]); L(t, a.inputs[1]); col = a.outputs['Vector']
        em = N('ShaderNodeEmission'); L(col, em.inputs['Color']); em.inputs['Strength'].default_value = 1.0
        a2 = N('ShaderNodeAddShader'); L(last, a2.inputs[0]); L(em.outputs['Emission'], a2.inputs[1]); last = a2.outputs['Shader']
    if glossy:
        rgb, k, rough = glossy
        gl = N('ShaderNodeBsdfGlossy'); gl.distribution = 'GGX'; gl.inputs['Roughness'].default_value = rough; gl.inputs['Color'].default_value = (*[c * k for c in rgb], 1)
        a3 = N('ShaderNodeAddShader'); L(last, a3.inputs[0]); L(gl.outputs['BSDF'], a3.inputs[1]); last = a3.outputs['Shader']
    for s_ in users: L(last, s_)
    return m

LAMPS_FRONT = [(FIRE_BOWLS[0][0], FIRE_BOWLS[0][1], PLAT_Z + 1.9), (FIRE_BOWLS[1][0], FIRE_BOWLS[1][1], PLAT_Z + 1.9), (-1.95, -3.95, 3.7), (1.95, -3.95, 3.7)]
# painted-light emitters used by the shaders: each side's flames merged into one point (half the shader cost of one point per flame)
GLOW_IN = [(-1.62, 0.2, PLAT_Z + 1.7), (1.62, 0.2, PLAT_Z + 1.7)]
GLOW_FRONT = [(-2.25, -4.3, PLAT_Z + 2.3), (2.3, -4.35, PLAT_Z + 2.3)]

def _v2_materials(pre, P, C, TX, E):
    """Materials of the v2 dressing (all named PGD_<preset>_*, rebuilt with the preset). MV: exterior (the set's blue-violet shade;
    gold and bronze keep a dark-gold shade); MW: the same for the inside of the ground storey, with the warm painted shade of the
    interior and the lamp glow."""
    tx = STATE['tx']; preset = STATE['preset']; gk = GLOW_K[preset]; warm = (1.0, 0.62, 0.3)
    P2 = dict(P, shade=tuple(s * (0.85 if P['night'] else 1.0) for s in (0.6, 0.46, 0.33)), shade_mix=0.0, lift=(0.012, 0.006, 0.002))
    def make(Pd, tag, lamps, glow_k):
        STATE['P'] = Pd
        try:
            def lit(name, hexcol='#808080', image=None, alpha=False, form=True, sm=1.0, smix=None, glow=None, gain=1.0):
                m = mat_lit(pre + tag + name, hexcol, image=tx[image] if image else None, alpha=alpha, form=tuple(Pd['form']) if form else None, shade_mul=sm, shade_mix=smix, gain=gain)
                if glow and not alpha: _extra(m, glow=(lamps, warm, glow * glow_k, 1.5))
                return m
            def metal(name, base, ks=1.0, image=None):
                sm_ = (2.4, 1.6, 0.55) if tag == 'v2_' else (1.0, 1.05, 1.1)
                m = mat_lit(pre + tag + name, base, image=tx[image] if image else None, form=tuple(Pd['form']), shade_mul=sm_, shade_mix=0.15)
                return _extra(m, glow=(lamps, (1.0, 0.78, 0.5), 0.3 * glow_k, 1.4), spec=(lamps, (1.0, 0.88, 0.6), 1.3 * ks, 24.0),
                              glossy=((1.0, 0.78, 0.4), 0.8 * ks, 0.28) if tag == 'v2_' else None)          # no sun reaches the interior: no GGX lobe there
            D = dict(gold=metal('gold', '#e4c060', 1.0), bronze=metal('bronze', '#a87a34', 0.9), bronze_d=metal('bronze_d', '#5a3c1a', 0.7),
                     dragon=metal('dragon', '#e0c878', 1.1, image='scales'), cloud=metal('cloudband', '#a87a34', 1.0, image='cloud_band'),
                     curtain=lit('curtain', image='curtain', glow=0.6), valance=lit('valance', image='valance', alpha=True), ban=lit('ban', image='ban', alpha=True),
                     nobori=lit('nobori', image='nobori2'), maku=lit('maku', image='maku'), carpet=lit('carpet', image='carpet', form=False, glow=0.5), carpet_r=lit('carpet_r', image='carpet', form=False, glow=0.5, sm=0.8, gain=0.78),
                     mural=lit('mural', image='mural', glow=0.7), iron=lit('iron', '#2e2a30', sm=1.1), candle=lit('candle', '#f4ead6', glow=0.6),
                     red=lit('red', '#c8382a', glow=0.5), red_d=lit('red_d', '#8e2420', glow=0.5), green=lit('green', '#3f8a64'), white=lit('white', '#f2ead8'),
                     rope=lit('rope', '#c8a66a'), rope_d=lit('rope_d', '#9a7a48'), tool=lit('tool', '#8a8a96', sm=1.1), straw=lit('straw', '#d8bc78'), straw_d=lit('straw_d', '#b0904e'),
                     plank=lit('plank', '#e2b884'), plank_e=lit('plank_e', '#c89a64'), wood=lit('wood', '#a0683c'), wood_d=lit('wood_d', '#6a4026'), pot=lit('pot', '#5a4a62'),
                     cloth=lit('cloth', '#2e3a6a'), cloth2=lit('cloth2', '#7a2a26'), shadow=lit('shadow', '#1e1210', form=False, sm=0.4), shadow_m=lit('shadow_m', '#7a5a44', form=False, sm=0.7))
        finally:
            STATE['P'] = P
        return D
    MV = make(P, 'v2_', GLOW_IN + GLOW_FRONT, 0.6 * gk); MW = make(P2, 'v2w_', GLOW_IN, gk)
    em = dict(maru=mat_emit(pre + 'e_v2_maru', image=tx['maru'], strength=1.0 if not P['night'] else 1.4, alpha=True),
              flame=mat_emit(pre + 'e_v2_flame', '#ffa040', strength=FLAME_K[preset]), flame_c=mat_emit(pre + 'e_v2_flamec', '#fff0c0', strength=FLAME_K[preset] * 1.4),
              lantern=mat_emit(pre + 'e_v2_lantern', image=tx['lantern'], strength=1.25 if not P['night'] else 2.6))
    MV.update(em); MW.update(em); STATE['MV'] = MV; STATE['MW'] = MW
    return MV

def _glow_slots(objs, lamps, k, r=1.8):
    """Swap every lit material of objs for a copy with the warm glow of lamps added (warm bounce of the fire bowls and lanterns on the
    ground storey's front, under its eave)."""
    cache = STATE.setdefault('glow_copies', {}); warm = (1.0, 0.6, 0.28)
    for ob in objs:
        for i, m in enumerate(ob.data.materials):
            if m is None or m.name.startswith(('ink', 'PGD_%s_e_' % STATE['preset'])) or 'v2w_' in m.name or '_w_' in m.name or 'v2_' in m.name or not any(n.bl_idname == 'ShaderNodeAddShader' for n in m.node_tree.nodes): continue
            if any(n.bl_idname == 'ShaderNodeBsdfTransparent' for n in m.node_tree.nodes): continue
            if any(w in m.name for w in ('rafters', 'kawara', 'bracket', 'ridge')): continue          # red-brown in violet shade + orange would read magenta
            if m.name not in cache:
                c = m.copy(); c.name = m.name + '_g0'; _extra(c, glow=(lamps, warm, k, r)); cache[m.name] = c
            ob.data.materials[i] = cache[m.name]

def _warm_interior():
    """(was the s01 runtime fix) warm painted shade for the inside of the pagoda: shade = art x (0.66, 0.44, 0.25), no blue tint, plus the
    lamp glow; slots of the interior objects are swapped from the cold set materials to these."""
    M = STATE['M']; O = STATE['objects']; P = STATE['P']; pre = 'PGD_%s_' % STATE['preset']; tx = STATE['tx']; gk = GLOW_K[STATE['preset']]
    P2 = dict(P, shade=tuple(s * (0.85 if P['night'] else 1.0) for s in (0.6, 0.46, 0.33)), shade_mix=0.0, lift=(0.012, 0.006, 0.002)); STATE['P'] = P2
    warm = (1.0, 0.6, 0.28)
    try:
        def W(name, hexcol=None, image=None, form=(0.0, -0.1, 0.2), gl=0.8, lamps=GLOW_IN, sm=1.0):
            m = mat_lit(pre + 'w_' + name, hexcol or '#808080', image=tx[image] if image else None, form=form, shade_mul=sm)
            return _extra(m, glow=(lamps, warm, 1.4 * gl * gk, 1.8))
        WM = dict(cypress=_extra(mat_lit(pre + 'w_cypress', '#c49a72', form=(0.0, -0.25, 0.2)), glow=(GLOW_IN, warm, 1.3 * gk, 1.6),
                                 spec=(GLOW_IN, (1.0, 0.8, 0.55), 0.5, 10.0)),
                  wood_d=W('wood_d', '#8a5634'), wood=W('wood', '#7a4a2c'), wood_l=W('wood_l', '#9a6438'), paving=W('paving', image='paving', form=None),
                  granite=W('granite', '#e2d4bc', form=(0.0, -0.1, 0.25), gl=0.6), stone_d=W('stone_d', '#9a8a78', form=(0.0, -0.1, 0.25), gl=0.6),
                  red=W('red', '#c8382a', gl=0.6), rafters=W('rafters', image='rafters', form=None, gl=0.25, lamps=GLOW_FRONT + GLOW_IN, sm=(0.5, 0.5, 0.62)), bracket=W('bracket', image='bracket', gl=0.3, lamps=GLOW_FRONT + GLOW_IN, sm=(0.6, 0.6, 0.72)))
    finally:
        STATE['P'] = P
    def swap(ob, table):
        for i, m in enumerate(ob.data.materials):
            for old, new in table:
                if m == old: ob.data.materials[i] = new
    swap(O['pillar'], [(M['cypress'], WM['cypress'])])
    swap(O['storey_0_body'], [(M['wood_d'], WM['wood_d']), (M['paving'], WM['paving'])])
    swap(O['storey_0_front'], [(M['paving'], WM['paving'])])
    for k in ('storey_0_body', 'storey_0_front'):                    # the ground storey's bracket band: warm, lit by its lanterns / fires (soffit stays cool)
        swap(O[k], [(M['bracket'], WM['bracket'])])
    swap(O['storey_4_body'], [(M['wood'], WM['wood'])])
    swap(O['soseki'], [(M['granite'], WM['granite']), (M['stone_d'], WM['stone_d'])])
    swap(O['oil_lamps'], [(M['wood_d'], WM['wood_d'])])
    for i in (1, 2, 3): swap(O['storey_%d_body' % i], [(M['wood_d'], WM['wood_d']), (M['wood_l'], WM['wood_l'])])
    STATE['WM'] = WM
    return WM

def _open_base():
    """(was the s01 runtime fix) the ground storey's front wall panels and their dark linings are removed (open base: the hanging pillar is
    seen from the courtyard without the cutaway); its two middle back posts go too (seen through the floating gap they read as a prop)."""
    import bmesh
    M = STATE['M']; ob = STATE['objects']['storey_0_front']; hw, z0, h, ov = STOREYS[0]
    kill = {i for i, m in enumerate(ob.data.materials) if m in (M['door'], M['renji'], M['wood_d'])}
    bm = bmesh.new(); bm.from_mesh(ob.data)
    dead = [f for f in bm.faces if f.material_index in kill and (lambda c: c.y < -(hw - 0.4) and z0 < c.z < z0 + h and abs(c.x) < hw)(f.calc_center_median())]
    bmesh.ops.delete(bm, geom=dead, context='FACES'); bm.to_mesh(ob.data); bm.free(); ob.data.update()
    ob2 = STATE['objects']['storey_0_body']; red = {i for i, m in enumerate(ob2.data.materials) if m == M['red']}
    bm = bmesh.new(); bm.from_mesh(ob2.data)
    d2 = [f for f in bm.faces if f.material_index in red and (lambda c: c.y > hw - 0.3 and abs(abs(c.x) - hw / 3) < 0.25 and z0 < c.z < z0 + h)(f.calc_center_median())]
    bmesh.ops.delete(bm, geom=d2, context='FACES'); bm.to_mesh(ob2.data); bm.free(); ob2.data.update()
    STATE['open_base'] = True
    return len(dead) + len(d2)

def _tube(mb, pts, radii, mat, seg=10, uvk=1.0, cap_end=True):
    """Swept tube along pts (parallel-transport frames), radius per point; uv u round, v along (uvk per D)."""
    mb.pid += 1; rings = []; u_prev = None; acc = [0.0]
    for i in range(1, len(pts)): acc.append(acc[-1] + (pts[i] - pts[i - 1]).length)
    for i, p in enumerate(pts):
        t = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        if u_prev is None:
            u = t.cross(Vector((0, 0, 1)))
            if u.length < 1e-4: u = Vector((1, 0, 0))
        else: u = u_prev - t * u_prev.dot(t)
        u.normalize(); v = t.cross(u); u_prev = u
        rings.append([p + radii[i] * (math.cos(2 * math.pi * k / seg) * u + math.sin(2 * math.pi * k / seg) * v) for k in range(seg)])
    for i in range(len(pts) - 1):
        for k in range(seg):
            j = (k + 1) % seg
            mb.face([rings[i][k], rings[i][j], rings[i + 1][j], rings[i + 1][k]], mat,
                    [(k / seg, acc[i] * uvk), ((k + 1) / seg, acc[i] * uvk), ((k + 1) / seg, acc[i + 1] * uvk), (k / seg, acc[i + 1] * uvk)])
    if cap_end: mb.face(rings[-1], mat)
    return rings

def _pillar_dress(SET, MV):
    """The hanging pillar's foot as the film's golden insert (ref a t0003): a polished bronze shoe with beaded gold rims, a cloud-scroll
    sleeve, gold bands, and a gold dragon coiling down the pillar with its head over the gap; a dark contact shade on the foundation
    stone under the foot keeps the one-palm gap reading as a dark slot. Parented to the pillar pivot (swings / sways with it)."""
    pp = STATE['pillar']; mb = MB(); dr = MB(); F = FOOT_Z; R = PILLAR_R
    mb.frustum((0, 0, F), (0, 0, F + 0.34), R + 0.09, R + 0.07, MV['bronze'], seg=32, cap_mat=MV['bronze_d'])
    for (za, zb, rr, m) in ((F - 0.01, F + 0.07, R + 0.12, MV['gold']), (F + 0.33, F + 0.41, R + 0.11, MV['gold']), (F + 0.41, F + 0.95, R + 0.05, MV['cloud']),
                            (F + 0.95, F + 1.04, R + 0.1, MV['gold']), (F + 1.75, F + 1.83, R + 0.07, MV['bronze']), (F + 1.83, F + 1.88, R + 0.09, MV['gold'])):
        mb.frustum((0, 0, za), (0, 0, zb), rr, rr, m, seg=32, cap0=(za < F), uv_wrap=(1, 1) if m is MV['cloud'] else None)
    o = mb.obj('pillar_foot', SET, hull=0.008, smooth=True); _parent(o, pp); mb = MB()
    for k in range(24):                                                                    # bead ring on the lower rim (no hull)
        a = 2 * math.pi * k / 24; mb.sphere((math.cos(a) * (R + 0.125), math.sin(a) * (R + 0.125), F + 0.03), 0.035, MV['gold'], seg=6, rings=4)
    ob_ = mb.obj('pillar_beads', SET, smooth=True); _parent(ob_, pp)
    # the dragon: head over the gap facing the insert cameras (azimuth -72 deg), body spiralling up 1.3 turns, tail at F + 2.2
    a_h = math.radians(-72.0); n = 70; pts = []; rad = []
    for i in range(n):
        t = i / (n - 1); a = a_h + t * 2 * math.pi * 1.3; rr = R + 0.17 + 0.025 * math.sin(t * 9 * math.pi)
        pts.append(Vector((rr * math.cos(a), rr * math.sin(a), F + 0.4 + t * 1.95 + 0.05 * math.sin(t * 7 * math.pi)))); rad.append(0.115 * (1 - t) ** 0.7 + 0.022)
    _tube(dr, pts, rad, MV['dragon'], seg=12, uvk=2.0)
    for i in range(3, n - 3, 3):                                                           # dorsal spikes (outward and up)
        p = pts[i]; out = Vector((p.x, p.y, 0)).normalized(); up = (out * 0.6 + Vector((0, 0, 0.8))).normalized()
        dr.frustum(p + up * rad[i] * 0.7, p + up * (rad[i] + 0.11 * (1 - i / n) + 0.04), 0.03 * (1 - i / n) + 0.012, 0.0, MV['gold'], seg=5)
    for i in (8, 30):                                                                      # two clawed legs gripping the sleeve
        p = pts[i]; inw = -Vector((p.x, p.y, 0)).normalized()
        for s_ in (-1, 1):
            tg = (pts[i + 1] - pts[i - 1]).normalized(); q = p + tg * 0.06 * s_ + Vector((0, 0, -0.06))
            dr.frustum(q, q + inw * 0.09 + Vector((0, 0, -0.09)), 0.035, 0.018, MV['dragon'], seg=6)
            for c in (-1, 0, 1): e = q + inw * 0.09 + Vector((0, 0, -0.09)); dr.frustum(e, e + inw * 0.05 + tg * 0.03 * c + Vector((0, 0, -0.03)), 0.012, 0.0, MV['gold'], seg=4)
    od = dr.obj('pillar_dragon', SET, hull=0.006, smooth=True); _parent(od, pp); dr = MB()
    hp = pts[0]; tg = (pts[0] - pts[1]).normalized(); out = Vector((hp.x, hp.y, 0)).normalized()
    fw = (tg * 0.45 + out * 0.9 + Vector((0, 0, -0.12))).normalized(); side = fw.cross(Vector((0, 0, 1))).normalized(); up = side.cross(fw).normalized()
    dr.sphere(hp + fw * 0.03, 0.125, MV['dragon'], seg=12, rings=8)                         # skull
    dr.frustum(hp + fw * 0.06 + up * 0.03, hp + fw * 0.3 + up * 0.01, 0.1, 0.065, MV['dragon'], seg=10)        # upper snout
    dr.frustum(hp + fw * 0.06 - up * 0.06, hp + fw * 0.26 - up * 0.13, 0.07, 0.045, MV['dragon'], seg=8)      # open lower jaw
    dr.sphere(hp + fw * 0.17 - up * 0.04, 0.06, MV['red_d'], seg=8, rings=5)                                    # mouth
    dr.sphere(hp + fw * 0.31 + up * 0.03, 0.05, MV['gold'], seg=8, rings=5)                                    # nose
    for s_ in (-1, 1):
        dr.sphere(hp + fw * 0.1 + up * 0.09 + side * 0.075 * s_, 0.028, MV['red'], seg=8, rings=5)             # eyes
        dr.frustum(hp + up * 0.08 + side * 0.06 * s_, hp - fw * 0.28 + up * 0.26 + side * 0.13 * s_, 0.028, 0.004, MV['gold'], seg=6)   # horns
        for k in range(4): dr.frustum(hp - fw * 0.05 + side * 0.09 * s_ + up * (0.02 * k), hp - fw * (0.2 + 0.05 * k) + side * 0.17 * s_ + up * (0.05 + 0.03 * k), 0.025, 0.0, MV['gold'], seg=4)   # mane
        for k in range(3): dr.frustum(hp + fw * (0.2 + 0.03 * k) - up * 0.02 + side * 0.04 * s_, hp + fw * (0.2 + 0.03 * k) - up * 0.08 + side * 0.04 * s_, 0.012, 0.0, MV['white'], seg=4)  # fangs
    hs = 1.15; dr.v = [tuple(hp + (Vector(v) - hp) * hs) for v in dr.v]                                   # the head 1.15x
    oh = dr.obj('pillar_dragon_head', SET, hull=0.006, smooth=True); _parent(oh, pp)
    # dark contact shade on the foundation stone under the foot (fixed to the stone)
    sh = MB(); seg = 28
    for ring, (r0, r1, m, dz) in enumerate(((0.0, 0.46, MV['shadow_m'], 0.003), (0.0, 0.3, MV['shadow'], 0.005))):
        for i in range(seg):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg
            sh.face([Vector((0, 0, SOSEKI_TOP + dz)), Vector((r1 * math.cos(a0), r1 * math.sin(a0), SOSEKI_TOP + dz)), Vector((r1 * math.cos(a1), r1 * math.sin(a1), SOSEKI_TOP + dz))], m)
    so = sh.obj('soseki_shade', SET); so.visible_shadow = False
    STATE['objects']['pillar_foot'] = o; STATE['objects']['pillar_dragon'] = od

def _lantern_mesh(mb, hk, s, mat, frame_mat):
    mb.frustum(hk, hk - Vector((0, 0, 0.18 * s)), 0.015, 0.015, frame_mat, seg=4)
    mb.frustum(hk - Vector((0, 0, 0.18 * s)), hk - Vector((0, 0, 0.26 * s)), 0.2 * s, 0.22 * s, frame_mat, seg=12)
    prof = [(0.22, 0.26), (0.32, 0.38), (0.36, 0.55), (0.32, 0.72), (0.22, 0.84)]
    for (r0, z0), (r1, z1) in zip(prof, prof[1:]):
        mb.frustum(hk - Vector((0, 0, z0 * s)), hk - Vector((0, 0, z1 * s)), r0 * s, r1 * s, mat, seg=14, cap0=False, cap1=False, uv_wrap=(2, (z1 - z0) / 0.58))
    mb.frustum(hk - Vector((0, 0, 0.84 * s)), hk - Vector((0, 0, 0.92 * s)), 0.22 * s, 0.2 * s, frame_mat, seg=12)
    mb.frustum(hk - Vector((0, 0, 0.92 * s)), hk - Vector((0, 0, 1.25 * s)), 0.03 * s, 0.07 * s, STATE['MV']['red'], seg=6)      # tassel

def _candelabrum(mb, fl, x, y, z, MV, h=1.35):
    """Gold three-armed candle stand (ref a t0005) with lit candles."""
    mb.frustum((x, y, z), (x, y, z + 0.08), 0.24, 0.2, MV['gold'], seg=12); mb.frustum((x, y, z + 0.08), (x, y, z + h), 0.035, 0.03, MV['gold'], seg=8)
    for zk in (0.35, 0.8): mb.sphere((x, y, z + h * zk), 0.06, MV['gold'], seg=8, rings=5)
    for dx in (-0.26, 0.0, 0.26):
        top = Vector((x + dx, y, z + h + (0.12 if dx == 0 else 0.0)))
        if dx: mb.frustum((x, y, z + h - 0.1), top - Vector((0, 0, 0.02)), 0.022, 0.022, MV['gold'], seg=6)
        mb.frustum(top - Vector((0, 0, 0.03)), top, 0.08, 0.08, MV['gold'], seg=10)
        mb.frustum(top, top + Vector((0, 0, 0.2)), 0.035, 0.035, MV['candle'], seg=8)
        f0 = top + Vector((0, 0, 0.22)); fl.frustum(f0, f0 + Vector((0, 0, 0.05)), 0.0, 0.032, MV['flame'], seg=8, cap0=False); fl.frustum(f0 + Vector((0, 0, 0.05)), f0 + Vector((0, 0, 0.16)), 0.032, 0.0, MV['flame'], seg=8, cap0=False)
        fl.sphere(f0 + Vector((0, 0, 0.05)), 0.016, MV['flame_c'], seg=6, rings=4)

def _fire_bowl(mb, fl, x, y, z, MV):
    """Kagaribi: iron basket on three legs with a log fire (ref a t0001 fire bowls)."""
    for k in range(3):
        a = 2 * math.pi * k / 3 + 0.4; mb.frustum((x + 0.45 * math.cos(a), y + 0.45 * math.sin(a), z), (x + 0.12 * math.cos(a), y + 0.12 * math.sin(a), z + 1.3), 0.03, 0.03, MV['iron'], seg=5)
    mb.frustum((x, y, z + 1.2), (x, y, z + 1.55), 0.2, 0.36, MV['iron'], seg=12, cap1=False)
    for k in range(8):
        a = 2 * math.pi * k / 8; mb.frustum((x + 0.2 * math.cos(a), y + 0.2 * math.sin(a), z + 1.2), (x + 0.38 * math.cos(a), y + 0.38 * math.sin(a), z + 1.6), 0.02, 0.02, MV['gold'], seg=4)
    r = random.Random(int(abs(x) * 10 + abs(y) * 100))
    for k in range(7):
        a = r.uniform(0, 2 * math.pi); d = r.uniform(0.0, 0.18); hgt = r.uniform(0.35, 0.7); c = Vector((x + d * math.cos(a), y + d * math.sin(a), z + 1.45))
        fl.frustum(c, c + Vector((r.uniform(-0.05, 0.05), r.uniform(-0.05, 0.05), hgt)), r.uniform(0.09, 0.15), 0.0, MV['flame'], seg=7)
    fl.sphere((x, y, z + 1.55), 0.16, MV['flame_c'], seg=8, rings=5)

def _ornament(SET, MV):
    """Gold fittings on the posts, 3D bracket blocks with painted / gold ends and beam ends on every storey; on the ground storey red
    velvet drapes tied back in the three front bays under a swagged gold-fringed pelmet, ban banners from the front eave corners, two
    lit paper lanterns, an interior of painted dragon murals and glowing round lattice windows, a runner carpet, a gilded canopy hung
    with chains of gold beads (yoraku) round the pillar, candelabra, and fire bowls on the platform. Everything on storey i is parented
    to storey_i (sways with it); the front (-y) parts join the cutaway list."""
    gold = MV['gold']
    for i, (hw, z0, h, ov) in enumerate(STOREYS):
        zw = z0 + h; piv = STATE['storeys'][i]; om, of_, bk = MB(), MB(), MB(); bay = 2 * hw / 3
        for k, n in enumerate(NRM):
            t = TAN(n); mb = of_ if k == 0 else om
            for a in (-hw, -hw / 3, hw / 3):                                               # posts at a (corner at -hw of this side)
                if i == 0 and k == 2 and a != -hw: continue                                 # open-base back middle posts are gone
                pc = n * hw + t * a; rr = 0.2 if a == -hw else 0.18
                for (za, zb) in ((z0 + 0.12, z0 + 0.3), (zw - 0.52, zw - 0.36)):
                    mb.box((pc.x - rr, pc.y - rr, za), (pc.x + rr, pc.y + rr, zb), gold)
            # bracket blocks on the band: lower bearing block + projecting arm with a gold cap
            rb = hw + 0.2
            for j in range(7):
                s_ = -rb + 0.25 + j * (2 * rb - 0.5) / 6; p = n * rb + t * s_
                lo = p + n * 0.02; hi = p + n * 0.3
                bk.box((min(lo.x, hi.x) - 0.11, min(lo.y, hi.y) - 0.11, zw + 0.02), (max(lo.x, hi.x) + 0.11, max(lo.y, hi.y) + 0.11, zw + 0.2), MV['red'])
                hi2 = p + n * 0.55
                bk.box((min(lo.x, hi2.x) - 0.07, min(lo.y, hi2.y) - 0.07, zw + 0.22), (max(lo.x, hi2.x) + 0.07, max(lo.y, hi2.y) + 0.07, zw + 0.36), MV['green'] if j % 2 else MV['red'])
                cap = p + n * 0.57
                bk.box((cap.x - 0.08, cap.y - 0.08, zw + 0.21), (cap.x + 0.08, cap.y + 0.08, zw + 0.37), gold)
                t0, t1 = p + n * 0.25, p + n * 0.5
                bk.box((min(t0.x, t1.x) - 0.1, min(t0.y, t1.y) - 0.1, zw + 0.36), (max(t0.x, t1.x) + 0.1, max(t0.y, t1.y) + 0.1, zw + 0.64), MV['red'])
            # beam ends past the corner (kibana) with white / gold tips
            c = n * (hw + 0.02) + t * hw
            for d in (t, n):
                e0 = c; e1 = c + d * 0.45
                mb.box((min(e0.x, e1.x) - 0.09, min(e0.y, e1.y) - 0.09, zw - 0.33), (max(e0.x, e1.x) + 0.09, max(e0.y, e1.y) + 0.09, zw - 0.09), MV['red'])
                mb.box((e1.x - 0.1, e1.y - 0.1, zw - 0.34), (e1.x + 0.1, e1.y + 0.1, zw - 0.08), gold)
        oo = om.obj('orn_%d' % i, SET, hull=0.02); _parent(oo, piv); no_bounce(oo)
        of = of_.obj('orn_%d_front' % i, SET, hull=0.02); _parent(of, piv); STATE['cut_objs'].append(of); no_bounce(of)
        ob_ = bk.obj('brackets_%d' % i, SET); _parent(ob_, piv); no_bounce(ob_); ob_.visible_shadow = False     # no ink hull: 560 small blocks (render cost)
    # ---- festival lanterns: two small lit paper lanterns under each side of every eave (shot-3 / pagoda_low / two_buildings read)
    for i, (hw_, z0_, h_, ov_) in enumerate(STOREYS):
        zw_ = z0_ + h_; piv = STATE['storeys'][i]; R_o = hw_ + ov_; z_e = zw_ + 0.55; s_l = 0.8 if i else 1.0
        for k, n in enumerate(NRM):
            for sv in (-0.5, 0.5):
                if i == 0 and k == 0: continue                                          # the two big front lanterns hang there
                hk = n * (R_o - 0.35) + TAN(n) * (sv * (R_o - 0.35)) + Vector((0, 0, z_e - 0.3 + LIFT * abs(sv) ** 3 * 0.8))
                nm = 'lantern_e%d_%d_%d' % (i, k, 0 if sv < 0 else 1); lp = _pivot(nm, SET, tuple(hk)); lp['wrest'] = tuple(hk); _parent(lp, piv)
                m2 = MB(); _lantern_mesh(m2, hk, s_l, MV['lantern'], STATE['M']['wood_d']); lo = m2.obj(nm + '_mesh', SET, hull=0.008); _parent(lo, lp); lo.visible_shadow = False; no_bounce(lo)
                if k == 0: STATE['cut_objs'].append(lo)
                STATE.setdefault('loose', []).append(dict(ob=lp, kind='swing', amp=11.0, seed=600 + i * 8 + k * 2 + (sv > 0)))
    # ---- festival bunting (red-gold swags) on the balcony railings of storeys 1..4
    for i in range(1, 5):
        hw_, z0_, h_, ov_ = STOREYS[i]; rr = hw_ + 0.51; piv = STATE['storeys'][i]; bm_, bf_ = MB(), MB()
        for k, n in enumerate(NRM):
            t = TAN(n); mb = bf_ if k == 0 else bm_; a_ = n * rr - t * rr; b_ = n * rr + t * rr; L_ = 2 * rr
            mb.oface([a_ + Vector((0, 0, z0_ + 0.02)), b_ + Vector((0, 0, z0_ + 0.02)), b_ + Vector((0, 0, z0_ + 0.6)), a_ + Vector((0, 0, z0_ + 0.6))], MV['valance'],
                     [(0, 0), (L_ / 1.6, 0), (L_ / 1.6, 1), (0, 1)], n)
        o1 = bm_.obj('bunting_%d' % i, SET); _parent(o1, piv); no_bounce(o1); o2 = bf_.obj('bunting_%d_front' % i, SET); _parent(o2, piv); no_bounce(o2); STATE['cut_objs'].append(o2)
        o1.visible_shadow = False; o2.visible_shadow = False
    # ---- ground storey: drapes, pelmet, ban banners, lanterns (front parts in the cutaway list)
    hw, z0, h, ov = STOREYS[0]; zw = z0 + h; piv0 = STATE['storeys'][0]; bay = 2 * hw / 3
    fr = MB(); al = MB(); al_in = MB(); y = -hw - 0.2
    for b in range(3):
        xa = -hw + b * bay + 0.16; xb = xa + bay - 0.32; zt = zw - 0.4
        for s_ in (0, 1):                                                       # a drape gathered to each side of the bay, tied at 1.3
            x_out = xa if s_ == 0 else xb; sg = 1 if s_ == 0 else -1
            prof = [(zt, 0.42), (z0 + 1.6, 0.16), (z0 + 1.35, 0.13), (z0 + 0.6, 0.28), (z0 + 0.12, 0.34)]
            for (za, wa), (zb_, wb) in zip(prof, prof[1:]):
                for f in range(3):                                              # three folds per drape
                    u0, u1 = f / 3.0, (f + 1) / 3.0; dz = 0.06 * (1 if f % 2 else -1)
                    pa = [Vector((x_out + sg * wa * u0, y + dz, za)), Vector((x_out + sg * wa * u1, y - dz, za)), Vector((x_out + sg * wb * u1, y - dz, zb_)), Vector((x_out + sg * wb * u0, y + dz, zb_))]
                    fr.oface(pa, MV['curtain'], [(u0 * 0.45, (za - z0) / 3.0), (u1 * 0.45, (za - z0) / 3.0), (u1 * 0.45, (zb_ - z0) / 3.0), (u0 * 0.45, (zb_ - z0) / 3.0)], (0, -1, 0))
            fr.frustum((x_out + sg * 0.0, y - 0.05, z0 + 1.42), (x_out + sg * 0.18, y - 0.05, z0 + 1.42), 0.045, 0.045, gold, seg=6)
            fr.frustum((x_out + sg * 0.16, y - 0.07, z0 + 1.42), (x_out + sg * 0.16, y - 0.07, z0 + 0.9), 0.03, 0.07, gold, seg=6)       # tassel
        al.oface([(xa - 0.12, y - 0.04, zt - 0.62), (xb + 0.12, y - 0.04, zt - 0.62), (xb + 0.12, y - 0.04, zw - 0.32), (xa - 0.12, y - 0.04, zw - 0.32)], MV['valance'],
                 [(0, 0), (0.667, 0), (0.667, 1), (0, 1)], (0, -1, 0))
    fo = fr.obj('drapes', SET, hull=0.01); _parent(fo, piv0); STATE['cut_objs'].append(fo); no_bounce(fo)
    fa = al.obj('pelmets', SET); _parent(fa, piv0); STATE['cut_objs'].append(fa); no_bounce(fa); fa.visible_shadow = False
    bn = MB(); lm = MB(); STATE['v2_lanterns'] = []
    for sx in (-1, 1):
        x0_ = sx * 4.3; yb = -4.3; z1 = 4.22
        bn.frustum((x0_ - 0.4, yb, z1), (x0_ + 0.4, yb, z1), 0.025, 0.025, gold, seg=5)
        bn.oface([(x0_ - 0.35, yb, z1 - 3.1), (x0_ + 0.35, yb, z1 - 3.1), (x0_ + 0.35, yb, z1), (x0_ - 0.35, yb, z1)], MV['ban'], [(0, 0.03), (1, 0.03), (1, 1), (0, 1)], (0, -1, 0))
        bn.oface([(x0_ - 0.35, yb + 0.01, z1 - 3.1), (x0_ + 0.35, yb + 0.01, z1 - 3.1), (x0_ + 0.35, yb + 0.01, z1), (x0_ - 0.35, yb + 0.01, z1)], MV['ban'], [(1, 0.03), (0, 0.03), (0, 1), (1, 1)], (0, 1, 0))
    for sx in (-1, 1):
        hk = Vector((sx * 1.95, -3.95, 4.38)); lp = _pivot('lantern_v2_%d' % (0 if sx < 0 else 1), SET, tuple(hk)); lp['wrest'] = tuple(hk); _parent(lp, piv0)
        m2 = MB(); _lantern_mesh(m2, hk, 1.25, MV['lantern'], STATE['M']['wood_d']); lo = m2.obj('lantern_v2_%d_mesh' % (0 if sx < 0 else 1), SET, hull=0.01); _parent(lo, lp); lo.visible_shadow = False
        STATE['v2_lanterns'].append(lp); STATE.setdefault('loose', []).append(dict(ob=lp, kind='swing', amp=9.0, seed=500 + sx))
    bo = bn.obj('ban_banners', SET); _parent(bo, piv0); no_bounce(bo); bo.visible_shadow = False
    hw1, z01, h1, ov1 = STOREYS[1]; zh = z01 + h1 + 0.55 - 0.32; b1 = MB()                     # ban from the four eave corners of storey 1
    for sx in (-1, 1):
        for sy in (-1, 1):
            c = Vector((sx * 4.15, sy * 4.15, zh + LIFT * 0.6)); nn = Vector((sx, sy, 0)).normalized(); tt = Vector((-nn.y, nn.x, 0))
            b1.frustum(c - tt * 0.38, c + tt * 0.38, 0.025, 0.025, MV['gold'], seg=5)
            for sgn in (1, -1):
                q = [c - tt * 0.32 - Vector((0, 0, 2.3)), c + tt * 0.32 - Vector((0, 0, 2.3)), c + tt * 0.32, c - tt * 0.32]
                b1.oface([p + nn * 0.01 * sgn for p in q], MV['ban'], [(0, 0.03), (1, 0.03), (1, 1), (0, 1)] if sgn > 0 else [(1, 0.03), (0, 0.03), (0, 1), (1, 1)], nn * sgn)
    ob1 = b1.obj('ban_storey1', SET); _parent(ob1, STATE['storeys'][1]); no_bounce(ob1); ob1.visible_shadow = False
    # ---- interior of the ground storey (warm interior materials MW)
    MVo = MV; MV = STATE['MW']; gold = MV['gold']
    it = MB(); win = MB(); fl = MB(); ext = MB(); beads = MB(); zi = z0 + 0.12; wi = hw - 0.19
    for k, n in enumerate(NRM):
        if k == 0: continue
        t = TAN(n)
        for b in range(3):
            a = -hw + b * bay; c = n * wi + Vector((0, 0, 0))
            if b == 1:                                                           # round window, red-gold frame round it
                cc = n * (wi - 0.02) + t * (a + bay / 2) + Vector((0, 0, z0 + 1.65)); rr = 0.78
                win.oface([cc - t * rr - Vector((0, 0, rr)), cc + t * rr - Vector((0, 0, rr)), cc + t * rr + Vector((0, 0, rr)), cc - t * rr + Vector((0, 0, rr))], MV['maru'], [(0, 0), (1, 0), (1, 1), (0, 1)], -n)
                ring = [cc - n * 0.01 + (t * math.cos(2 * math.pi * q / 28) + Vector((0, 0, math.sin(2 * math.pi * q / 28)))) * (rr - 0.02) for q in range(29)]
                _tube(it, ring, [0.06] * 29, gold, seg=6, cap_end=False)
                pa = n * (wi + 0.01) + t * (a + 0.1); pb = n * (wi + 0.01) + t * (a + bay - 0.1)
                it.oface([pa + Vector((0, 0, zi)), pb + Vector((0, 0, zi)), pb + Vector((0, 0, z0 + 0.7)), pa + Vector((0, 0, z0 + 0.7))], MV['red_d'], [(0, 0)] * 4, -n)
            else:
                pa = n * (wi - 0.01) + t * (a + 0.12); pb = n * (wi - 0.01) + t * (a + bay - 0.12)
                it.oface([pa + Vector((0, 0, zi)), pb + Vector((0, 0, zi)), pb + Vector((0, 0, zw - 0.38)), pa + Vector((0, 0, zw - 0.38))], MV['mural'],
                         [(0, 0), (1, 0), (1, 1), (0, 1)] if True else None, -n)
    # the runner's last stretch inside the storey (it sways with the floor), then a square carpet ring round the stone: four strips,
    # each with its gold borders along its own length
    zc_ = PLAT_Z + 0.025
    it.quad((-RUNNER_HW, -hw, zc_), (2 * RUNNER_HW, 0, 0), (0, hw - 1.95, 0), MV['carpet'], (0, -hw / 4.0, 1, -1.95 / 4.0))
    for (xa, xb, ya, yb) in ((-1.95, 1.95, -1.95, -1.25), (-1.95, 1.95, 1.25, 1.95)):                         # along x: u across y, v along x
        it.oface([(xa, ya, zc_ + 0.002), (xb, ya, zc_ + 0.002), (xb, yb, zc_ + 0.002), (xa, yb, zc_ + 0.002)], MV['carpet'], [(0, xa / 4.0), (0, xb / 4.0), (1, xb / 4.0), (1, xa / 4.0)], (0, 0, 1))
    for (xa, xb, ya, yb) in ((-1.95, -1.25, -1.25, 1.25), (1.25, 1.95, -1.25, 1.25)):                         # along y
        it.quad((xa, ya, zc_), (xb - xa, 0, 0), (0, yb - ya, 0), MV['carpet'], (0, ya / 4.0, 1, yb / 4.0))
    # gilded canopy (tengai) round the pillar with hanging bead chains
    zc = zw - 0.55; ri, ro = 1.05, 1.45
    for k, n in enumerate(NRM):
        t = TAN(n); q = [n * ri + t * ri, n * ri - t * ri, n * ro - t * ro, n * ro + t * ro]
        it.oface([p + Vector((0, 0, zc)) for p in q], MV['red_d'], [(0, 0)] * 4, (0, 0, -1))
        a_ = n * ro - t * ro; b_ = n * ro + t * ro
        it.oface([a_ + Vector((0, 0, zc - 0.22)), b_ + Vector((0, 0, zc - 0.22)), b_ + Vector((0, 0, zc + 0.02)), a_ + Vector((0, 0, zc + 0.02))], gold, [(0, 0)] * 4, n)
        al_in.oface([a_ + n * 0.01 + Vector((0, 0, zc - 0.62)), b_ + n * 0.01 + Vector((0, 0, zc - 0.62)), b_ + n * 0.01 + Vector((0, 0, zc - 0.2)), a_ + n * 0.01 + Vector((0, 0, zc - 0.2))], MV['valance'], [(0, 0), (1, 0), (1, 1), (0, 1)], n)
        for j in range(5):
            p = n * (ro + 0.02) + t * (-ro + 0.1 + j * (2 * ro - 0.2) / 4); L_ = 0.55 + 0.3 * (j % 2)
            for q_ in range(int(L_ / 0.07)): beads.sphere(p + Vector((0, 0, zc - 0.25 - q_ * 0.07)), 0.026, gold, seg=6, rings=4)
            beads.frustum(p + Vector((0, 0, zc - 0.25 - L_)), p + Vector((0, 0, zc - 0.38 - L_)), 0.025, 0.06, MV['red'], seg=6)
    for (x, y) in ((-1.55, -1.05), (1.55, -1.05)): _candelabrum(it, fl, x, y, PLAT_Z, MV)
    for (x, y) in FIRE_BOWLS: _fire_bowl(ext, fl, x, y, PLAT_Z, MVo)
    io = it.obj('interior_v2', SET); _parent(io, piv0); no_bounce(io)          # no ink hull: seen soft through the door / behind the insert (2 CPU s)
    eo = ext.obj('fire_bowls', SET, hull=0.01); no_bounce(eo)
    ai = al_in.obj('canopy_pelmet', SET); _parent(ai, piv0); no_bounce(ai); ai.visible_shadow = False
    bo2 = beads.obj('yoraku_chains', SET); _parent(bo2, piv0); no_bounce(bo2); bo2.visible_shadow = False
    wo = win.obj('round_windows', SET); _parent(wo, piv0); wo.visible_shadow = False
    flo = fl.obj('flames_v2', SET); flo.visible_shadow = False; _parent(flo, piv0)

RUNNER_HW = 0.975                    # half width of the red runner: 65 % of the 3 D stair, equal 0.525 D stone margins
STAIR = [(-PLAT_HW - 1.35, PLAT_Z / 3), (-PLAT_HW - 0.9, 2 * PLAT_Z / 3), (-PLAT_HW - 0.45, PLAT_Z)]   # (nosing y, tread z) of the 3 steps

def runner_profile(y_start=-70.0, y_end=-PLAT_HW + 2.2, th=0.015, lip=0.03):
    """(y, z, kind) polyline of the runner in the y-z plane, centred on x = 0: flat on the street / courtyard (z 0.03), then over each
    step riser -> rounded nosing lip -> tread, flat across the platform to the storey's front (y -3). kind: 'flat', 'riser', 'lip'."""
    P = [(y_start, 0.03, 'flat')]; zb = 0.03
    for (yn, zt) in STAIR:
        P.append((yn - th, zb, 'flat'))                                        # foot of the riser
        P.append((yn - th, zt - lip, 'riser'))
        P.append((yn - th - 0.012, zt - lip * 0.35, 'lip')); P.append((yn - th, zt + th * 0.6, 'lip')); P.append((yn + lip, zt + th, 'lip'))
        zb = zt + th
    P.append((-STOREYS[0][0], PLAT_Z + 0.025, 'flat'))
    return P

def _runner(SET, MV):
    """The red runner from the street (y -70) through the gate and the courtyard, up the three platform steps (draped over every riser and
    tread, with a slight lip at each nosing) and across the platform to the open base; 1.95 D wide, centred; the pattern runs on along it.
    Risers in a slightly darker carpet so the steps read. The last stretch inside the storey is part of interior_v2."""
    P = runner_profile(); mb = MB(); acc = 0.0; w = RUNNER_HW
    rz = MV.get('carpet_r') or MV['carpet']
    for (y0, z0, _), (y1, z1, k) in zip(P, P[1:]):
        L_ = math.hypot(y1 - y0, z1 - z0)
        if L_ < 1e-6: continue
        nrm = Vector((0, -(z1 - z0), (y1 - y0))).normalized()                    # left-hand normal of the profile: up on treads, -y on risers
        mb.oface([(-w, y0, z0), (w, y0, z0), (w, y1, z1), (-w, y1, z1)], rz if k == 'riser' else MV['carpet'],
                 [(0, acc / 4.0), (1, acc / 4.0), (1, (acc + L_) / 4.0), (0, (acc + L_) / 4.0)], nrm)
        if abs(z1 - z0) > 1e-4 or k != 'flat':                                    # side edges of the stair part (carpet thickness)
            for sx in (-1, 1):
                mb.oface([(sx * w, y0, z0), (sx * w, y1, z1), (sx * w, y1, z1 - 0.015), (sx * w, y0, z0 - 0.015)], rz, [(0, 0)] * 4, (sx, 0, 0))
        acc += L_
    o = mb.obj('runner', SET, hull=0.008); no_bounce(o)
    STATE['runner'] = o
    return o

def _dressing(SET, MV):
    """(was the s01 runtime dressing, extended) the carpenter's yard by the pagoda: plank stacks, sawhorses, beams, a tool rack with saws
    and adzes, rope coils, a log pile, barrels, rice bales, handcarts; material for the master's tower east; extra stone lanterns; street
    barrels, bales, carts, potted pines, noren awnings; a red runner up the approach; richer approach banners; the gate curtain (maku)
    and banners."""
    M = STATE['M']; mb = MB()
    wood, wood_d, plank, plank_e, hoop = MV['wood'], MV['wood_d'], MV['plank'], MV['plank_e'], M['iron']
    straw, straw_d, stone, stone_d, pine, pot = MV['straw'], MV['straw_d'], M['stone'], M['stone_d'], M['pine'], MV['pot']
    def barrel(x, y, r=0.42, h=0.95):
        mb.frustum((x, y, 0), (x, y, h * 0.5), r * 0.86, r, wood, seg=12, cap0=False, cap1=False); mb.frustum((x, y, h * 0.5), (x, y, h), r, r * 0.86, wood, seg=12, cap0=False)
        for z in (0.12 * h, 0.5 * h, 0.88 * h):
            rr = r * (0.88 if z != 0.5 * h else 1.0) + 0.02; mb.frustum((x, y, z - 0.035), (x, y, z + 0.035), rr, rr, hoop, seg=12, cap0=False, cap1=False)
    def planks(x, y, ang, n=6, L=3.6, w=0.42, t=0.09):
        ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        for k in range(n):
            layer = k // 3; j = k % 3; ox = (j - 1) * (w + 0.04); z = 0.12 + layer * t; cx, cy = x + ox * ca, y + ox * sa; hx, hy = L / 2 * -sa, L / 2 * ca
            mb.frustum(Vector((cx - hx, cy - hy, z)), Vector((cx + hx, cy + hy, z)), w * 0.5 * 1.41, w * 0.5 * 1.41, plank if k % 2 == 0 else plank_e, seg=4)
        for s in (-1, 1):
            bx, by = x + s * -sa * L * 0.35, y + s * ca * L * 0.35; mb.box((bx - 0.75, by - 0.08, 0), (bx + 0.75, by + 0.08, 0.1), wood_d)
    def sawhorse(x, y, log=False):
        mb.box((x - 0.8, y - 0.08, 0.95), (x + 0.8, y + 0.08, 1.08), wood)
        for sx in (-0.65, 0.65):
            for sy in (-0.35, 0.35): mb.frustum((x + sx, y + sy, 0), (x + sx * 0.95, y, 0.96), 0.05, 0.05, wood_d, seg=4)
        if log: mb.frustum((x - 1.4, y, 1.3), (x + 1.4, y, 1.3), 0.22, 0.22, plank_e, seg=8, cap_mat=plank)
    def beam(x0, y0, x1, y1, z=0.18, r=0.2): mb.frustum((x0, y0, z), (x1, y1, z), r, r, wood_d, seg=4)
    def bale(x, y, ang=0.0, z=0.0):
        ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang)); d = Vector((ca, sa, 0)) * 0.45; c = Vector((x, y, z + 0.34))
        mb.frustum(c - d, c + d, 0.34, 0.34, straw, seg=10, cap_mat=straw_d)
        for s in (-0.25, 0.25): mb.frustum(c + d * s * 2 - d * 0.05, c + d * s * 2 + d * 0.05, 0.355, 0.355, straw_d, seg=10, cap0=False, cap1=False)
    def cart(x, y, ang, load=None):
        ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang)); f = Vector((ca, sa, 0)); r = Vector((-sa, ca, 0)); c = Vector((x, y, 0))
        bed = [c - f * 1.2 - r * 0.7, c + f * 1.2 - r * 0.7, c + f * 1.2 + r * 0.7, c - f * 1.2 + r * 0.7]; z0, z1 = 0.62, 0.72
        mb.oface([p + Vector((0, 0, z1)) for p in bed], plank_e, [(0, 0)] * 4, (0, 0, 1)); mb.oface([p + Vector((0, 0, z0)) for p in bed], wood_d, [(0, 0)] * 4, (0, 0, -1))
        for a, b in zip(bed, bed[1:] + bed[:1]):
            nn = (a + b) / 2 - c; nn.z = 0
            mb.oface([a + Vector((0, 0, z0)), b + Vector((0, 0, z0)), b + Vector((0, 0, z1 + 0.18)), a + Vector((0, 0, z1 + 0.18))], wood, [(0, 0)] * 4, nn)
        for s in (-1, 1):
            wc = c + r * (0.82 * s) + Vector((0, 0, 0.62)); mb.frustum(wc - r * 0.06, wc + r * 0.06, 0.62, 0.62, wood_d, seg=16); mb.frustum(wc - r * 0.1, wc + r * 0.1, 0.14, 0.14, hoop, seg=8)
        for s in (-1, 1):
            mb.frustum(c + f * 1.1 + r * 0.55 * s + Vector((0, 0, 0.66)), c + f * 2.6 + r * 0.45 * s + Vector((0, 0, 0.2)), 0.05, 0.05, wood_d, seg=4)
        if load == 'bales': bale(x - ca * 0.5, y - sa * 0.5, ang + 90, z=0.72); bale(x + ca * 0.5, y + sa * 0.5, ang + 90, z=0.72)
        elif load == 'barrels':
            for k in (-0.55, 0.55):
                pc = c + f * k; mb.frustum(pc + Vector((0, 0, 0.72)), pc + Vector((0, 0, 1.5)), 0.32, 0.32, wood, seg=10); mb.frustum(pc + Vector((0, 0, 1.3)), pc + Vector((0, 0, 1.36)), 0.34, 0.34, hoop, seg=10, cap0=False, cap1=False)
    def toro(x, y):
        mb.box((x - 0.6, y - 0.6, 0), (x + 0.6, y + 0.6, 0.3), stone_d); mb.frustum((x, y, 0.3), (x, y, 1.6), 0.22, 0.2, stone, seg=8)
        mb.box((x - 0.5, y - 0.5, 1.6), (x + 0.5, y + 0.5, 1.8), stone); mb.box((x - 0.36, y - 0.36, 1.8), (x + 0.36, y + 0.36, 2.5), stone)
        mb.frustum((x, y, 2.5), (x, y, 2.95), 0.85, 0.08, stone_d, seg=6); mb.sphere((x, y, 3.0), 0.12, stone, seg=8, rings=5)
    def potted_pine(x, y, s=1.0):
        mb.frustum((x, y, 0), (x, y, 0.55 * s), 0.38 * s, 0.48 * s, pot, seg=10); mb.frustum((x, y, 0.5 * s), (x + 0.1, y, 1.3 * s), 0.08 * s, 0.06 * s, M['bark'], seg=5)
        for (dx, dz, rr) in ((-0.35, 1.25, 0.45), (0.35, 1.5, 0.4), (0.0, 1.85, 0.32)):
            mb.frustum((x + dx * s, y, (dz - 0.1) * s), (x + dx * s, y, (dz + 0.12) * s), rr * s, rr * 0.7 * s, pine, seg=10)
    def rope(x, y, r=0.42, turns=4):
        for k in range(turns): mb.frustum((x, y, 0.06 + k * 0.09), (x, y, 0.13 + k * 0.09), r - 0.02 * k, r - 0.02 * k, MV['rope'] if k % 2 else MV['rope_d'], seg=14, cap0=False, cap1=(k == turns - 1), cap_mat=MV['rope_d'])
    def rack(x, y, ang):
        ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang)); f = Vector((ca, sa, 0)); n_ = Vector((-sa, ca, 0)); c = Vector((x, y, 0))
        for s in (-1, 1):
            for d in (-1, 1): mb.frustum(c + f * 1.1 * s + n_ * 0.35 * d, c + f * 1.1 * s + Vector((0, 0, 2.0)), 0.05, 0.05, wood_d, seg=4)
        mb.frustum(c - f * 1.25 + Vector((0, 0, 1.95)), c + f * 1.25 + Vector((0, 0, 1.95)), 0.06, 0.06, wood, seg=6)
        for k, kind in enumerate(('saw', 'adze', 'saw', 'mallet', 'saw', 'adze')):
            p = c + f * (-0.9 + k * 0.36) + Vector((0, 0, 1.9)) + n_ * 0.05
            if kind == 'saw':
                mb.oface([p + n_ * 0.0 + Vector((0, 0, -0.1)), p + f * 0.02 + Vector((0, 0, -0.1)), p + f * 0.12 + Vector((0, 0, -0.95)), p - f * 0.12 + Vector((0, 0, -0.95))], MV['tool'], [(0, 0)] * 4, n_)
                mb.frustum(p, p + Vector((0, 0, -0.12)), 0.03, 0.03, wood_d, seg=4)
            elif kind == 'adze':
                mb.frustum(p, p + Vector((0, 0, -0.7)), 0.03, 0.03, wood, seg=5); mb.box(tuple(p + Vector((-0.1, -0.04, -0.78))), tuple(p + Vector((0.1, 0.04, -0.68))), MV['tool'])
            else:
                mb.frustum(p, p + Vector((0, 0, -0.55)), 0.03, 0.03, wood, seg=5); mb.frustum(p + Vector((0, 0, -0.55)) - f * 0.16, p + Vector((0, 0, -0.55)) + f * 0.16, 0.1, 0.1, wood_d, seg=8)
    def logs(x, y, ang, n=6):
        ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang)); f = Vector((ca, sa, 0)); n_ = Vector((-sa, ca, 0))
        k = 0
        for row, cnt in enumerate((3, 2, 1)):
            for j in range(cnt):
                c = Vector((x, y, 0.24 + row * 0.4)) + n_ * ((j - (cnt - 1) / 2) * 0.48)
                mb.frustum(c - f * 1.8, c + f * 1.8, 0.24, 0.23, MV['wood'], seg=10, cap_mat=plank); k += 1
    # carpenter's yard west of the path (s01 shots 1 / 4 / 5, two_buildings, town_wide)
    planks(-7.0, -8.6, 90, n=6); planks(-7.2, -10.6, 90, n=3); planks(-9.4, -8.2, 90, n=9)
    sawhorse(-4.9, -11.4); sawhorse(-8.6, -12.6, log=True); beam(-9.2, -13.6, -5.4, -14.4); beam(-9.0, -14.2, -5.6, -15.0)
    barrel(-9.6, -6.0); barrel(-10.3, -6.6, 0.38, 0.85); barrel(-6.4, -3.6, 0.4, 0.9)
    bale(-11.0, -9.0, 20); bale(-11.0, -10.0, 20); bale(-11.0, -9.5, 20, z=0.62); cart(-12.5, -15.5, 60, load='bales')
    rack(-10.8, -4.6, 0); rope(-8.4, -4.2); rope(-7.6, -4.8, 0.34, 3); logs(-12.6, -11.5, 90); rope(-5.9, -13.2, 0.36, 3)
    # east: material for the master's tower
    planks(8.4, -6.8, 90, n=6); planks(10.4, -5.2, 0, n=6); barrel(6.4, -4.2); barrel(7.0, -3.4, 0.36, 0.8); cart(10.5, -15.0, 120, load='barrels')
    bale(5.6, -14.6, -10); bale(6.4, -15.2, -10); logs(17.6, -6.2, 90); sawhorse(11.6, -8.0, log=True); rope(12.6, -6.4)
    for (x, y) in ((-3.0, -28.0), (3.0, -28.0), (-6.4, -6.8), (6.4, -7.2)): toro(x, y)
    for (x, y) in ((-3.6, -37.2), (3.7, -39.5), (-3.8, -51.0), (3.6, -56.5), (-3.7, -63.0), (3.8, -70.0)): barrel(x, y, 0.36, 0.85)
    for (x, y) in ((-3.5, -44.0), (3.4, -48.0), (3.5, -62.5)): bale(x, y, 90); bale(x, y + 0.5, 90, z=0.62)
    cart(2.9, -61.5, 95, load='bales'); cart(-2.8, -66.0, 80, load='barrels')
    for (x, y) in ((-3.9, -35.6), (3.9, -35.6), (-3.9, -58.0), (3.9, -66.5)): potted_pine(x, y)
    for (x, y) in ((-4.6, -6.0), (4.6, -6.0)): potted_pine(x, y, 0.8)
    ob = mb.obj('yard_dressing', SET, hull=0.03); no_bounce(ob)
    # noren awnings, red runner up the approach, the gate curtain and banners
    cl = MB(); ca = MB()
    for (x, y0, y1, m, s) in ((-4.45, -46.0, -41.5, MV['cloth'], 1), (4.45, -60.0, -55.0, MV['cloth2'], -1), (-4.45, -60.5, -57.0, MV['cloth2'], 1), (4.45, -43.5, -40.5, MV['cloth'], -1)):
        cl.oface([(x + 0.05 * s, y0, 1.6), (x + 0.05 * s, y1, 1.6), (x + 0.05 * s, y1, 2.6), (x + 0.05 * s, y0, 2.6)], m, [(0, 0)] * 4, (s, 0, 0))
    gy = YARD[2]
    _runner(SET, MV)
    for s in (-1, 1):                                                                            # gate curtain both faces
        yy = gy + s * 1.24
        cl.oface([(-2.65, yy, 2.85), (2.65, yy, 2.85), (2.65, yy, 3.78), (-2.65, yy, 3.78)], MV['maku'], [(0.08, 0), (0.92, 0), (0.92, 1), (0.08, 1)] if s < 0 else [(0.92, 0), (0.08, 0), (0.08, 1), (0.92, 1)], (0, s, 0))
        for x in (-3.3, 3.3):
            ca.oface([(x - 0.33, yy + s * 0.05, 1.2), (x + 0.33, yy + s * 0.05, 1.2), (x + 0.33, yy + s * 0.05, 4.2), (x - 0.33, yy + s * 0.05, 4.2)], MV['ban'], [(0, 0.03), (1, 0.03), (1, 1), (0, 1)], (0, s, 0))
    for (x, y) in ((-1.9, -21.5), (1.9, -21.5), (-1.9, -27.5), (1.9, -27.5), (-3.3, -37.0), (3.3, -42.0), (-3.3, -55.0), (3.3, -62.0), (-1.9, -24.5), (1.9, -24.5),
                   (-1.9, -30.5), (1.9, -30.5), (-3.3, -41.5), (3.3, -45.8), (-3.3, -47.5), (3.3, -50.6), (-3.3, -53.0), (3.3, -66.0), (-3.3, -68.5)):
        sx = -1 if x < 0 else 1                                                                  # richer approach banners (over v1 cloth)
        cl.frustum((x, y, 0), (x, y, 4.4), 0.05, 0.04, MV['wood_d'], seg=6); cl.frustum((x, y, 4.05), (x - sx * 0.85, y, 4.05), 0.03, 0.03, MV['wood_d'], seg=4)
        cl.sphere((x, y, 4.45), 0.08, MV['gold'], seg=8, rings=5)
        cl.oface([(x - sx * 0.05, y - 0.02, 1.45), (x - sx * 0.85, y - 0.02, 1.45), (x - sx * 0.85, y - 0.02, 4.05), (x - sx * 0.05, y - 0.02, 4.05)], MV['nobori'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
        cl.oface([(x - sx * 0.05, y + 0.02, 1.45), (x - sx * 0.85, y + 0.02, 1.45), (x - sx * 0.85, y + 0.02, 4.05), (x - sx * 0.05, y + 0.02, 4.05)], MV['nobori'], [(1, 0), (0, 0), (0, 1), (1, 1)], (0, 1, 0))
    for side in (-1, 1):                                                                         # hangings on the south wall, both faces
        yw = YARD[2] + side * 0.47
        for x in (-14.5, -11.5, -8.5, -5.5, 5.5, 8.5, 11.5, 14.5, 17.5, 20.5, 23.5, 26.5):
            cl.oface([(x - 0.4, yw, 0.75), (x + 0.4, yw, 0.75), (x + 0.4, yw, 2.4), (x - 0.4, yw, 2.4)], MV['nobori'], [(0, 0), (1, 0), (1, 1), (0, 1)] if side < 0 else [(1, 0), (0, 0), (0, 1), (1, 1)], (0, side, 0))
            cl.frustum((x - 0.5, yw + side * 0.02, 2.42), (x + 0.5, yw + side * 0.02, 2.42), 0.03, 0.03, MV['gold'], seg=5)
    o2 = cl.obj('cloth_v2', SET, hull=0.012); no_bounce(o2); o3 = ca.obj('gate_ban', SET); no_bounce(o3); o3.visible_shadow = False
    old = STATE['objects'].pop('banners', None)                                                  # v1 banners, replaced
    if old is not None: bpy.data.objects.remove(old, do_unlink=True)
    STATE['dressing'] = [ob, o2, o3]

# ----------------------------------------------------------------------------- depth of field (compositor Defocus on the Cycles Z pass)
# fstop: smaller = more blur; CoC (px at 720 x 1280) = 12 f^2 / (fstop (s - f)) / sensor x 1280 x |1 - s / Z|, capped at DOF_BLUR_MAX.
# Useful: 0.5..1 for street / courtyard medium shots focused at 10..20 D, 1.5..2.5 at 3..5 D, 2..6 for inserts at 1..3 D. Defaults per set camera: on for the close / medium cameras, off (None) for the wides.
DOF = dict(cutaway_insert=dict(focus=(0.2, -0.62, FOOT_Z + 0.45), fstop=3.0), crack_insert=dict(focus=JOINT, fstop=2.5),
           street_eye=dict(focus=(0.0, -44.0, 1.5), fstop=2.0), pagoda_low=dict(focus=(0.9, -6.6, 1.6), fstop=4.0),
           rubble_dawn=dict(focus=PILE_MARK, fstop=6.0), two_buildings=None, town_wide=None, cutaway_full=None)
DOF_BLUR_MAX = 28                                                       # px at 720 x 1280 (scaled with the resolution percentage)
DOF_CAL = 12.0                                                          # calibration of the f-stop (look, not optics)

def _dof_nodes(ng):
    """Layered depth of field in the compositor (cheap, about 0.5 CPU s at 720 x 1280; the Defocus node cost 4..8 s): CoC (px) =
    min(K x |1 - s / Z|, R) from the Cycles Z pass; a Fast Gaussian blur (radius R) of the image with the in-focus pixels masked out
    (normalised convolution: blur(img x m) / blur(m), so a sharp actor never smears a halo into the blurred background); mixed
    sharp -> blurred by CoC / (0.6 R) (one level: a second level cost 0.5 CPU s for little gain). Returns the dict of nodes whose values setup_dof / update_dof set."""
    N = ng.nodes.new; L = ng.links.new
    rl = [n for n in ng.nodes if n.bl_idname == 'CompositorNodeRLayers'][0]
    users = [l.to_socket for l in list(ng.links) if l.from_socket == rl.outputs['Image']]
    def M(op, a=None, b=None, clamp=False, name=None):
        n = N('ShaderNodeMath'); n.operation = op; n.use_clamp = clamp
        if name: n.name = name
        for i, v in enumerate((a, b)):
            if v is None: continue
            if isinstance(v, (int, float)): n.inputs[i].default_value = v
            else: L(v, n.inputs[i])
        return n
    def mix(blend, a, b, fac=1.0):
        n = N('ShaderNodeMix'); n.data_type = 'RGBA'; n.blend_type = blend
        if isinstance(fac, (int, float)): n.inputs[0].default_value = fac
        else: L(fac, n.inputs[0])
        L(a, n.inputs[6]); L(b, n.inputs[7]); return n
    img, z = rl.outputs['Image'], rl.outputs['Depth']
    inv = M('DIVIDE', 10.0, z, name='PGD_dof_s'); d = M('SUBTRACT', 1.0, inv.outputs[0]); ab = M('ABSOLUTE', d.outputs[0])
    cpx = M('MULTIPLY', ab.outputs[0], 1.0, name='PGD_dof_k'); cm = M('MINIMUM', cpx.outputs[0], 28.0, name='PGD_dof_r')
    mask = M('DIVIDE', cm.outputs[0], 5.0, clamp=True, name='PGD_dof_m')
    w1 = M('DIVIDE', cm.outputs[0], 14.0, clamp=True, name='PGD_dof_w1')
    w2a = M('SUBTRACT', cm.outputs[0], 14.0, name='PGD_dof_w2a'); w2 = M('DIVIDE', w2a.outputs[0], 14.0, clamp=True, name='PGD_dof_w2')
    im_m = mix('MULTIPLY', img, mask.outputs[0]); lv = []
    for k in (1,):
        b1 = N('CompositorNodeBlur'); b1.name = 'PGD_dof_b%d' % k; b1.inputs['Type'].default_value = 'Fast Gaussian'; L(im_m.outputs[2], b1.inputs['Image'])
        b2 = N('CompositorNodeBlur'); b2.name = 'PGD_dof_bm%d' % k; b2.inputs['Type'].default_value = 'Fast Gaussian'; L(mask.outputs[0], b2.inputs['Image'])
        mx = M('MAXIMUM', None, 1e-3); 
        L(b2.outputs['Image'], mx.inputs[0])
        lv.append(mix('DIVIDE', b1.outputs['Image'], mx.outputs[0]))
    o2 = mix('MIX', img, lv[0].outputs[2], w1.outputs[0]); o2.name = 'PGD_dof_out'
    sw = mix('MIX', img, o2.outputs[2], 1.0); sw.name = 'PGD_dof'                                # factor 0 = DOF off
    for s_ in users: L(sw.outputs[2], s_)
    return sw

def _dof_values(scene):
    D = STATE.get('dof') or {}; ng = scene.compositing_node_group
    if not ng or 'PGD_dof' not in ng.nodes: return
    sw = ng.nodes['PGD_dof']
    if not D.get('on'): sw.inputs[0].default_value = 0.0; return
    cam = D.get('cam') or scene.camera; foc = D['focus']
    if isinstance(foc, bpy.types.Object): fp = foc.matrix_world.translation
    elif isinstance(foc, (int, float)): fp = None
    else: fp = Vector(foc)
    if fp is not None:
        mw = cam.matrix_world; fwd = -(mw.to_3x3() @ Vector((0, 0, 1))).normalized(); s_ = max(0.05, (fp - mw.translation).dot(fwd))
    else: s_ = float(foc)
    pct = scene.render.resolution_percentage / 100.0; res = max(scene.render.resolution_x, scene.render.resolution_y) * pct
    f = cam.data.lens / 1000.0; sens = cam.data.sensor_width / 1000.0
    K = DOF_CAL * f * f / (D['fstop'] * max(1e-3, s_ - f)) / sens * res; R = D['blur_max'] * pct
    n = ng.nodes; n['PGD_dof_s'].inputs[0].default_value = s_; n['PGD_dof_k'].inputs[1].default_value = K; n['PGD_dof_r'].inputs[1].default_value = R
    n['PGD_dof_m'].inputs[1].default_value = max(0.5, 0.18 * R); n['PGD_dof_w1'].inputs[1].default_value = R / 2; n['PGD_dof_w2a'].inputs[1].default_value = R / 2; n['PGD_dof_w2'].inputs[1].default_value = R / 2
    n['PGD_dof_w1'].inputs[1].default_value = R * 0.6
    for k, r in ((1, R),):
        n['PGD_dof_b%d' % k].inputs['Size'].default_value = (r, r); n['PGD_dof_bm%d' % k].inputs['Size'].default_value = (r, r)
    sw.inputs[0].default_value = 1.0; STATE['dof']['s'] = s_; STATE['dof']['K'] = K

def update_dof(scene=None, *args):
    """Recompute the focus distance (camera / focus object moved) and the CoC scale; runs on every frame change and before every render."""
    _dof_values(scene if isinstance(scene, bpy.types.Scene) else bpy.context.scene)

def _dof_handlers():
    for hl in (bpy.app.handlers.frame_change_post, bpy.app.handlers.render_pre):
        for h in list(hl):
            if getattr(h, '__name__', '') == 'update_dof': hl.remove(h)
        hl.append(update_dof)

def setup_dof(scene=None, focus=None, fstop=0.4, cam=None, blur_max=None):
    """Depth of field for the next renders: the Cycles Z pass drives a layered blur in the compositor, inserted before the bloom
    (see _dof_nodes). focus: an object (the focus follows it per frame, e.g. an actor's card), an (x, y, z) world point, or a float
    distance from the camera. fstop: smaller = more blur (0.3..0.6 for medium shots focused at 10..20 D, 1..2 at 3..5 D, 1..4 for
    inserts at 1..2 D); None / 0 / False switches DOF off. cam: camera object (default: scene.camera at render time).
    blur_max: largest blur radius in px at 720 x 1280 (default DOF_BLUR_MAX). Headless-safe (bpy module, CPU compositor); the
    focus distance is recomputed on every frame change and render (handlers). Returns the switch node."""
    scene = scene or bpy.context.scene; ng = scene.compositing_node_group
    for vl in scene.view_layers: vl.use_pass_z = True
    sw = ng.nodes.get('PGD_dof') or _dof_nodes(ng)
    on = bool(fstop) and focus is not None
    STATE['dof'] = dict(on=on, focus=focus, fstop=float(fstop) if on else None, cam=cam, blur_max=float(blur_max or DOF_BLUR_MAX))
    _dof_handlers(); _dof_values(scene)
    return sw

def apply_dof(cam_name, scene=None, cam=None, preset=None):
    """The default depth of field of a set camera (DOF table): on for the close / medium ones, off for the wides."""
    d = DOF.get(cam_name)
    return setup_dof(scene, d['focus'] if d else None, d['fstop'] if d else None, cam=cam)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stills'; arg = sys.argv[2:]
    if cmd == 'stills': cli_stills(arg or ['DAY', 'SUNSET', 'NIGHT', 'DAWN'])
    elif cmd == 'tests': cli_tests(*(arg[:1] or []))
    elif cmd == 'final': cli_final(arg[0] if arg else 'DAY', arg[1:] or None)
    elif cmd == 'digest':
        A = build(arg[0] if arg else 'DAY'); set_sway(0.7, 1.0); set_collapse(0.5); bpy.context.view_layer.update(); print('digest', digest())
        if len(arg) > 1:
            sc = bpy.context.scene; setup_render(sc, 'preview'); make_camera(A['cams']['two_buildings']); render(arg[1])
    else: print(__doc__)

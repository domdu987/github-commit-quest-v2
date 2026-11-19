#!/usr/bin/env python3
"""mine.py : set of film 5 ("the bird boy"), a British coal mine about 1905, as a real 3D Blender set (bpy 5.3, Cycles CPU).
Two locations in one module:

    import mine as M
    A = M.build('tunnel', 'LAMP')        # the roadway underground: timber sets, coal walls, rails and tubs, side heading, pit bottom
    A = M.build('pithead', 'DUSK')       # the surface: headframe, engine house + chimney, cage gate, heaps, first-aid hut  (DUSK | DAWN)
    M.lamp_light((x, y, z), 1.0, frame=10)   # a miner's lamp: warm point light, keyed per frame (actors carry the lamp props)
    M.set_gas(0.5, frame=10)             # faint layered firedamp haze (very subtle), tunnel
    M.set_blast(0.4, frame=10)           # the fireball racing down the tunnel from the face toward the pit bottom, debris, dust, flash
    M.set_flame(1.0, frame=10)           # flame of the foreman's lamp on its hook (lamp_insert); 0 out .. 1 normal .. 2 tall gas cap
    M.set_cage((x, y, z), frame=10)      # move the canary cage (its hook point) - the boy carries it; set_cage(None) hangs it back
    M.set_drips(frame)                   # falling water drops (deterministic in the frame)
    cam = M.make_camera(A['cams']['tunnel_eye']); M.apply_dof('tunnel_eye')

World: 1 unit = 1 D (head diameter), Z up, floor z = 0. Tunnel: the pit bottom (shaft, cage, whitewash, bright lamps) at y -13..0,
the roadway from y 0 to the coal face at y 40, centre line x = 1.8 sin(pi y / 40) (a gentle bend), 5.2 D wide, 5 D high; the side
heading opens off the left wall at y 19.5..23. Pithead: the shaft at (0, 12) with the headframe over it, its wheels turning in x-z
planes, ropes to the engine house to the west (-x), the camera side is south (-y). Built on the film-4 template
v3/set3d4/pagoda.py v2 (itself on v3/set3d2/tower.py): materials, mesh builder, render, grade, cameras, keys, actors, the painted
light helper _extra and setup_dof are imported, not rewritten. See mine_API.md.
CLI: python3 mine.py stills | tests | final [loc preset cams..] | digest <loc> <preset>"""
import os, sys, math, json, time, random, hashlib
import bpy
import numpy as np
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d2')); sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d4'))
import tower as T                                          # noqa: E402  (template: materials, MB, hulls, render, camera, keys, actors)
import pagoda as G                                         # noqa: E402  (template v2: _extra painted light, setup_dof, haze, pivots)
import mine_tex as MT                                      # noqa: E402
from tower import MB, no_bounce, setup_grade, make_camera, render, mat_lit, mat_emit   # noqa: E402,F401
WORK = os.path.join(HERE, 'mine_work')
T.ACT = os.path.join(WORK, 'actors')                       # placeholder sprites cached in our folder
STATE = T.STATE
setup_dof = G.setup_dof; update_dof = G.update_dof; digest = G.digest

# ----------------------------------------------------------------------------- dimensions (D)
TUN_L = 40.0; BEND = 1.8; WALL_HW = 2.6; WALL_Z = 4.0; ROOF_Z = 5.0
SET_Y = [1.25 + 2.5 * k for k in range(16)]                 # timber sets (pit props + cap beam) every 2.5 D
LEG_S = 2.28; CAP_Z = 4.05; CAP_T = 0.34                    # leg position, cap beam underside, thickness
TRACK_S = 0.8; GAUGE = 1.1                                  # rail track centre (right of the axis) and gauge
HEAD_Y = (19.5, 23.0); HEAD_LEN = 10.0; HEAD_H = 3.5        # side heading (left wall)
PB_Y0 = -10.0; PB_HW = 3.6; PB_H = 5.6                      # pit bottom chamber y -10..0
SHAFT_Y = (-13.5, -10.0)                                    # shaft behind the pit bottom (cage in it)
WARM = (1.0, 0.8, 0.5); LAMP_E = 150.0                      # miner's lamp colour, energy of strength 1 (about 1.0 at 2 D)
BULB = (1.0, 0.82, 0.58)

def cx(y): return BEND * math.sin(math.pi * y / TUN_L) if 0.0 <= y <= TUN_L else 0.0
def tangent(y):
    d = BEND * math.pi / TUN_L * math.cos(math.pi * y / TUN_L) if 0.0 <= y <= TUN_L else 0.0
    return Vector((d, 1.0, 0.0)).normalized()
def right(y): t = tangent(y); return Vector((t.y, -t.x, 0.0))
def TP(y, s=0.0, z=0.0):
    """World point at tunnel station y (along the roadway), s across (+ right looking toward the face), height z."""
    return Vector((cx(y), y, 0.0)) + right(y) * s + Vector((0.0, 0.0, z))

def _rnd(seed): return random.Random(seed)
def _h(i, j, seed):
    n = (i * 374761393 + j * 668265263 + seed * 2147483647) & 0xffffffff; n = ((n ^ (n >> 13)) * 1274126177) & 0xffffffff
    return ((n ^ (n >> 16)) & 0xffff) / 65535.0
def vnoise(x, y, seed=0):
    """Smooth value noise in [0, 1] (deterministic)."""
    i, j = math.floor(x), math.floor(y); fx, fy = x - i, y - j; ux, uy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a, b, c, d = _h(i, j, seed), _h(i + 1, j, seed), _h(i, j + 1, seed), _h(i + 1, j + 1, seed)
    return a + (b - a) * ux + (c - a) * uy + (a - b - c + d) * ux * uy

# ----------------------------------------------------------------------------- presets
# tunnel: no sun; lamps are point lights (light tree on), the painted shade is a cool blue-violet; toon term off (_untoon).
PRESETS = {
    'LAMP': dict(loc='tunnel', key=None, key_dir=(0.3, 0.5, -1.0), sun_elev=90, sun_angle=1.0, shade=(0.13, 0.28, 0.85), shade_tint=(0.16, 0.34, 1.1), shade_mix=0.8,
                 lift=(0.006, 0.006, 0.020), form=(0.0, -0.08, 0.30), toon=1.0, key_desat=0.0, ink='#140f1e', night=True,
                 grade_offset=(0.002, 0.002, 0.008), grade_saturation=1.2, bloom_size=0.05, lamp_k=1.0),
    'DUSK': dict(loc='pithead', key=(1.7, 0.92, 0.32), key_dir=G._kd((0.97, 0.26), 9), sun_elev=9, sun_angle=0.6, shade=(0.13, 0.15, 0.44), shade_tint=(0.17, 0.18, 0.58), shade_mix=0.7,
                 lift=(0.008, 0.004, 0.02), form=(0.0, -0.05, 0.2), toon=0.5, key_desat=0.0, ink='#2a1712', night=False, sky='dusk', pano='dusk', sky_k=0.95, pano_k=0.92,
                 haze=('#ffa868', 0.12), grade_offset=(0.004, 0.002, 0.009), grade_saturation=1.1, bloom_size=0.05, lamp_k=1.0),
    'DAWN': dict(loc='pithead', key=(1.22, 1.08, 0.86), key_dir=G._kd((-0.97, 0.26), 11), sun_elev=11, sun_angle=2.0, shade=(0.17, 0.21, 0.50), shade_tint=(0.21, 0.24, 0.56), shade_mix=0.7,
                 lift=(0.01, 0.008, 0.02), form=(0.0, -0.05, 0.2), toon=0.6, key_desat=0.0, ink='#2a1712', night=False, sky='dawn', pano='dawn', sky_k=0.9, pano_k=0.9,
                 haze=('#e8e4f0', 0.30), grade_offset=(0.006, 0.006, 0.010), grade_saturation=1.0, bloom_size=0.05, lamp_k=0.35),
}
LOC_PRESETS = dict(tunnel=['LAMP'], pithead=['DUSK', 'DAWN'])

# ----------------------------------------------------------------------------- material helpers
def _untoon(m):
    """Tunnel: the template's toon term divides by the sun's N.L; with point lamps the diffuse alone is the key (plain Lambert)."""
    for n in m.node_tree.nodes:
        if n.bl_idname == 'ShaderNodeMath' and n.operation == 'DIVIDE' and n.inputs[1].is_linked:
            m.node_tree.links.remove(n.inputs[1].links[0]); n.inputs[1].default_value = 1.0
    return m

def _append_shader(m, make):
    """Add a shader after the material's last shader: make(nt) -> output socket."""
    nt = m.node_tree; out = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeOutputMaterial'][0]
    last = out.inputs['Surface'].links[0].from_socket; new = make(nt)
    ad = nt.nodes.new('ShaderNodeAddShader'); nt.links.new(last, ad.inputs[0]); nt.links.new(new, ad.inputs[1]); nt.links.new(ad.outputs['Shader'], out.inputs['Surface'])
    return m

def _glossy(m, rgb, k, rough, mask=None, bump=0.0, bump_scale=40.0):
    """GGX lobe for the real lamps (glints on brass, rails, wet coal); mask: an image whose value scales it (the glitter of the seams);
    bump: high-frequency noise bump (facets that sparkle as a lamp passes)."""
    def make(nt):
        N = nt.nodes.new; L = nt.links.new
        gl = N('ShaderNodeBsdfGlossy'); gl.distribution = 'GGX'; gl.inputs['Roughness'].default_value = rough
        col = tuple(c * k for c in rgb)
        if mask is not None:
            uvt = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeTexImage']
            tx = N('ShaderNodeTexImage'); tx.image = T._img(mask); mm = N('ShaderNodeMix'); mm.data_type = 'RGBA'; mm.blend_type = 'MULTIPLY'; mm.inputs[0].default_value = 1.0
            L(tx.outputs['Color'], mm.inputs[6]); mm.inputs[7].default_value = (*col, 1); L(mm.outputs[2], gl.inputs['Color'])
        else: gl.inputs['Color'].default_value = (*col, 1)
        if bump > 0:
            tc = N('ShaderNodeTexCoord'); nz = N('ShaderNodeTexVoronoi'); nz.inputs['Scale'].default_value = bump_scale; L(tc.outputs['Object'], nz.inputs['Vector'])
            bp = N('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; L(nz.outputs['Distance'], bp.inputs['Height']); L(bp.outputs['Normal'], gl.inputs['Normal'])
        return gl.outputs['BSDF']
    return _append_shader(m, make)

def _metal(name, hexcol):
    """Brass / gold: the pagoda v2 metal rule - a dark-gold shade (shade_mul (2.4, 1.6, 0.55), shade_mix 0.15) instead of the set's blue,
    so brass reads golden in shade too."""
    P = STATE['P']; m = mat_lit(STATE['pre'] + 'm_' + name, hexcol, form=tuple(P['form']), shade_mul=(2.4, 1.6, 0.55), shade_mix=0.15)
    return _untoon(m) if STATE['loc'] == 'tunnel' else m

def _mat_glass(name, tint=(0.9, 0.95, 1.0), refl=0.12):
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); tr = N('ShaderNodeBsdfTransparent'); tr.inputs['Color'].default_value = (*tint, 1)
    gl = N('ShaderNodeBsdfGlossy'); gl.inputs['Roughness'].default_value = 0.04; gl.inputs['Color'].default_value = (1, 1, 1, 1)
    lw = N('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.3
    mp = N('ShaderNodeMath'); mp.operation = 'MULTIPLY_ADD'; mp.inputs[1].default_value = 0.6; mp.inputs[2].default_value = refl; L(lw.outputs['Facing'], mp.inputs[0])
    mx = N('ShaderNodeMixShader'); L(mp.outputs[0], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(gl.outputs['BSDF'], mx.inputs[2]); L(mx.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def _mat_fire(name, core=(1.0, 0.86, 0.52), edge=(1.0, 0.32, 0.06), k_core=9.0, k_edge=2.2):
    """Fireball: emission graded by facing (bright yellow-white core, orange-red rim), broken by noise (licks)."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); lw = N('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.62
    tc = N('ShaderNodeTexCoord'); nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 2.2; nz.inputs['Detail'].default_value = 3.0; L(tc.outputs['Object'], nz.inputs['Vector'])
    f = N('ShaderNodeMath'); f.operation = 'MULTIPLY_ADD'; f.inputs[2].default_value = -0.25; L(lw.outputs['Facing'], f.inputs[0]); L(nz.outputs['Fac'], f.inputs[1])
    f2 = N('ShaderNodeMath'); f2.operation = 'ADD'; f2.use_clamp = True; L(lw.outputs['Facing'], f2.inputs[0]); L(f.outputs[0], f2.inputs[1])
    cm = N('ShaderNodeMix'); cm.data_type = 'RGBA'; L(f2.outputs[0], cm.inputs[0]); cm.inputs[6].default_value = (*core, 1); cm.inputs[7].default_value = (*edge, 1)
    km = N('ShaderNodeMapRange'); km.inputs['To Min'].default_value = k_core; km.inputs['To Max'].default_value = k_edge; L(f2.outputs[0], km.inputs['Value'])
    em = N('ShaderNodeEmission'); em.name = 'fire'; L(cm.outputs[2], em.inputs['Color']); L(km.outputs['Result'], em.inputs['Strength'])
    L(em.outputs['Emission'], out.inputs['Surface']); m.cycles.emission_sampling = 'NONE'
    return m

def _mat_puff(name, image, rgb, k, opacity):
    """Dust / smoke sprite: tint x k emission, alpha = image alpha x opacity (node 'op')."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); tx = N('ShaderNodeTexImage'); tx.image = T._img(image)
    em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*rgb, 1); em.inputs['Strength'].default_value = k
    op = N('ShaderNodeMath'); op.name = 'op'; op.operation = 'MULTIPLY'; op.inputs[1].default_value = opacity; L(tx.outputs['Alpha'], op.inputs[0])
    tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); L(op.outputs[0], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(em.outputs['Emission'], mx.inputs[2])
    lp = N('ShaderNodeLightPath'); tr2 = N('ShaderNodeBsdfTransparent'); mx2 = N('ShaderNodeMixShader')
    L(lp.outputs['Is Camera Ray'], mx2.inputs['Fac']); L(tr2.outputs['BSDF'], mx2.inputs[1]); L(mx.outputs['Shader'], mx2.inputs[2]); L(mx2.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def _mat_gas(name, rgb):
    """Firedamp haze: camera-only additive emission rgb x k(node 'gas_k') x layered profile of z (collects under the roof, in thin
    wavering layers). Very faint: it is the invisible gas."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); geo = N('ShaderNodeNewGeometry'); sep = N('ShaderNodeSeparateXYZ'); L(geo.outputs['Position'], sep.inputs[0])
    up = N('ShaderNodeMapRange'); up.inputs['From Min'].default_value = 0.8; up.inputs['From Max'].default_value = 4.8; L(sep.outputs['Z'], up.inputs['Value'])
    w1 = N('ShaderNodeMath'); w1.operation = 'MULTIPLY'; w1.inputs[1].default_value = 5.5; L(sep.outputs['Z'], w1.inputs[0])
    w2 = N('ShaderNodeMath'); w2.operation = 'MULTIPLY'; w2.inputs[1].default_value = 0.45; L(sep.outputs['Y'], w2.inputs[0])
    w2s = N('ShaderNodeMath'); w2s.operation = 'SINE'; L(w2.outputs[0], w2s.inputs[0])
    w3 = N('ShaderNodeMath'); w3.operation = 'MULTIPLY_ADD'; w3.inputs[1].default_value = 1.4; L(w2s.outputs[0], w3.inputs[0]); L(w1.outputs[0], w3.inputs[2])
    sn = N('ShaderNodeMath'); sn.operation = 'SINE'; L(w3.outputs[0], sn.inputs[0])
    lay = N('ShaderNodeMath'); lay.operation = 'MULTIPLY_ADD'; lay.inputs[1].default_value = 0.4; lay.inputs[2].default_value = 0.6; L(sn.outputs[0], lay.inputs[0])
    pr = N('ShaderNodeMath'); pr.operation = 'MULTIPLY'; L(up.outputs['Result'], pr.inputs[0]); L(lay.outputs[0], pr.inputs[1])
    kk = N('ShaderNodeValue'); kk.name = 'gas_k'; kk.outputs[0].default_value = 0.0
    st = N('ShaderNodeMath'); st.operation = 'MULTIPLY'; L(pr.outputs[0], st.inputs[0]); L(kk.outputs[0], st.inputs[1])
    em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*rgb, 1); L(st.outputs[0], em.inputs['Strength'])
    tr = N('ShaderNodeBsdfTransparent'); ad = N('ShaderNodeAddShader'); L(tr.outputs['BSDF'], ad.inputs[0]); L(em.outputs['Emission'], ad.inputs[1])
    lp = N('ShaderNodeLightPath'); tr2 = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    L(lp.outputs['Is Camera Ray'], mx.inputs['Fac']); L(tr2.outputs['BSDF'], mx.inputs[1]); L(ad.outputs['Shader'], mx.inputs[2]); L(mx.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

# ----------------------------------------------------------------------------- geometry helpers
def obox(mb, c, X, Y, Z, hx, hy, hz, mat, uvk=1.0):
    """Oriented box: centre c, unit axes X, Y, Z, half sizes."""
    c = Vector(c); X, Y, Z = Vector(X), Vector(Y), Vector(Z); mb.pid += 1
    for (n, a, b, ha, hb, hn) in ((X, Y, Z, hy, hz, hx), (-X, Y, Z, hy, hz, hx), (Y, X, Z, hx, hz, hy), (-Y, X, Z, hx, hz, hy), (Z, X, Y, hx, hy, hz), (-Z, X, Y, hx, hy, hz)):
        o = c + n * hn; pts = [o - a * ha - b * hb, o + a * ha - b * hb, o + a * ha + b * hb, o - a * ha + b * hb]
        mb.oface(pts, mat, [(0, 0), (2 * ha * uvk, 0), (2 * ha * uvk, 2 * hb * uvk), (0, 2 * hb * uvk)], n)

def beam(mb, p0, p1, w, h, mat, up=(0, 0, 1), uvk=1.0):
    p0, p1 = Vector(p0), Vector(p1); X = (p1 - p0); L_ = X.length; X.normalize(); U = Vector(up)
    Y = U.cross(X)
    if Y.length < 1e-4: Y = Vector((0, 1, 0)).cross(X)
    Y.normalize(); Z = X.cross(Y)
    obox(mb, (p0 + p1) / 2, X, Y, Z, L_ / 2, w / 2, h / 2, mat, uvk)

def rod(mb, p0, p1, r, mat, seg=6, r1=None, uv=None):
    mb.frustum(p0, p1, r, r if r1 is None else r1, mat, seg=seg, uv_wrap=uv)

def lumpy(mb, c, r, mat, seed, seg=12, rings=7, rough=0.22, squash=1.0):
    """Irregular sphere (blob, boulder, lump) built deterministically."""
    c = Vector(c); R = []; mb.pid += 1
    for k in range(rings + 1):
        th = math.pi * k / rings; row = []
        for i in range(seg):
            ph = 2 * math.pi * i / seg; d = Vector((math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), -math.cos(th)))
            rr = r * (1 + rough * (vnoise(2.2 * d.x + 3, 2.2 * d.y + 2.2 * d.z, seed) - 0.5) * 2)
            row.append(c + Vector((d.x * rr, d.y * rr, d.z * rr * squash)))
        R.append(row)
    for k in range(rings):
        for i in range(seg):
            j = (i + 1) % seg; mb.face([R[k][i], R[k][j], R[k + 1][j], R[k + 1][i]], mat, [(i / seg, k / rings), ((i + 1) / seg, k / rings), ((i + 1) / seg, (k + 1) / rings), (i / seg, (k + 1) / rings)])

def catenary(p0, p1, sag, n=8):
    p0, p1 = Vector(p0), Vector(p1)
    return [p0.lerp(p1, i / n) - Vector((0, 0, sag * 4 * (i / n) * (1 - i / n))) for i in range(n + 1)]

def chain_rod(mb, pts, r, mat, seg=5):
    for a, b in zip(pts, pts[1:]): mb.frustum(a, b, r, r, mat, seg=seg, cap0=False, cap1=False)

def _light(name, loc, rgb, energy, radius=0.05, coll=None):
    d = bpy.data.lights.get(name) or bpy.data.lights.new(name, 'POINT'); d.color = rgb; d.energy = energy; d.shadow_soft_size = radius
    ob = bpy.data.objects.get(name)
    if ob is None: ob = bpy.data.objects.new(name, d); (coll or STATE['LIGHTS']).objects.link(ob)
    ob.location = loc; ob.visible_camera = False; STATE.setdefault('objects', {})[name] = ob
    return ob

def _obj(mb, name, coll, hull=0.0, shadow=True, nobounce=True):
    o = mb.obj(name, coll, hull=hull)
    if not shadow: o.visible_shadow = False
    if nobounce: no_bounce(o)
    return o

# ----------------------------------------------------------------------------- build
def build(location='tunnel', preset=None, clear=True, dress=True):
    """Build one location ('tunnel' | 'pithead') with a preset (tunnel: LAMP; pithead: DUSK | DAWN) into the current scene
    (collections SET and LIGHTS, world, render settings, grade). Returns the anchors dict (mine_API.md)."""
    preset = preset or LOC_PRESETS[location][0]
    assert preset in LOC_PRESETS[location], 'preset %s is not one of %s' % (preset, LOC_PRESETS[location])
    scene = bpy.context.scene; P = dict(PRESETS[preset]); STATE.clear(); STATE['P'] = P; STATE['preset'] = preset; STATE['loc'] = location
    if clear:
        for ob in list(scene.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for ac in list(bpy.data.actions): bpy.data.actions.remove(ac)
    for me in list(bpy.data.meshes):
        if me.users == 0: bpy.data.meshes.remove(me)
    for li in list(bpy.data.lights):
        if li.users == 0: bpy.data.lights.remove(li)
    SET = T._coll('SET', scene); LIGHTS = T._coll('LIGHTS', scene); T._wipe(SET); T._wipe(LIGHTS); STATE['SET'] = SET; STATE['LIGHTS'] = LIGHTS
    for m in list(bpy.data.materials):
        if m.name.startswith(('MIN_', 'ink')): bpy.data.materials.remove(m)
    tx = MT.ensure(verbose=False); STATE['tx'] = tx
    w = bpy.data.worlds.get('W_mine') or bpy.data.worlds.new('W_mine'); scene.world = w; nt = T._tree(w)
    bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld'); bg.inputs['Color'].default_value = (0, 0, 0, 1); bg.inputs['Strength'].default_value = 0.0
    nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
    setup_render(scene, 'final'); scene.frame_start = 1; scene.frame_current = 1
    pre = 'MIN_%s_' % preset; FORM = tuple(P['form']); tun = location == 'tunnel'
    def _k(v): return 'x'.join('%g' % x for x in v) if isinstance(v, (tuple, list)) else '%g' % v
    def fin(m): return _untoon(m) if tun else m
    def C(hexcol, gain=1.0, sm=1.0, form=True):
        return fin(mat_lit('%sc_%s_%g_%s_%d' % (pre, hexcol.lstrip('#'), gain, _k(sm), form), hexcol, gain=gain, shade_mul=sm, form=FORM if form else None))
    def TX(name, gain=1.0, sm=1.0, form=True, alpha=False):
        return fin(mat_lit('%st_%s_%g_%s_%d' % (pre, name, gain, _k(sm), form), image=tx[name], gain=gain, shade_mul=sm, form=FORM if form else None, alpha=alpha))
    def E(name, image=None, hexcol='#ffffff', k=1.0, alpha=False): return mat_emit(pre + 'e_' + name, hexcol, image=tx[image] if image else None, strength=k, alpha=alpha)
    STATE.update(C=C, TX=TX, E=E, pre=pre)
    if tun:
        _tunnel(SET, P, C, TX, E, dress)
    else:
        _pithead(SET, P, C, TX, E, dress)
        kd = Vector(P['key_dir']).normalized(); k = max(P['key'])
        d = bpy.data.lights.new('key_sun', 'SUN'); d.color = tuple(x / k for x in P['key']); d.energy = math.pi * k; d.angle = math.radians(P['sun_angle'])
        sun = bpy.data.objects.new('key_sun', d); LIGHTS.objects.link(sun); sun.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler(); sun.location = (-20, -40, 40); STATE['sun'] = sun
        scene.cycles.use_light_tree = True
    scene.cycles.use_light_tree = False
    _denoise(scene)
    setup_grade(scene)
    for ob in SET.objects:
        no_bounce(ob)
        if ob.get('glossy_vis'): ob.visible_glossy = True
    if tun:
        set_gas(0.0); set_blast(0.0); set_flame(1.0); set_cage(None); set_drips(None)
    A = anchors(); STATE['A'] = A
    return A

def _denoise(scene):
    """Lamp-lit set: a dozen point lamps at 12 samples leave light-selection grain that the painted-light template never had;
    OpenImageDenoise (albedo + normal guides, fast prefilter, CPU, deterministic) cleans it for about 2.5 CPU s at 720 x 1280."""
    c = scene.cycles; c.use_denoising = True; c.denoiser = 'OPENIMAGEDENOISE'; c.denoising_input_passes = 'RGB_ALBEDO_NORMAL'; c.denoising_prefilter = 'FAST'
    try: c.denoising_use_gpu = False
    except Exception: pass

def setup_render(scene, quality='final'):
    """tower.setup_render (final 720x1280 12 samples / preview 360x640 6, 2 threads, direct light only) + the denoiser, light tree off."""
    T.setup_render(scene, quality); scene.cycles.use_light_tree = False; _denoise(scene)

def _mat_pool(name, rgb, k):
    """Additive warm light pool decal (painted, noise free): emission rgb x k x the pool image's alpha over the floor."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); tx = N('ShaderNodeTexImage'); tx.image = T._img(STATE['tx']['pool'])
    em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*rgb, 1); L(tx.outputs['Alpha'], em.inputs['Strength'])
    em.name = 'pool'; mu = N('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = k; L(tx.outputs['Alpha'], mu.inputs[0]); L(mu.outputs[0], em.inputs['Strength'])
    tr = N('ShaderNodeBsdfTransparent'); ad = N('ShaderNodeAddShader'); L(tr.outputs['BSDF'], ad.inputs[0]); L(em.outputs['Emission'], ad.inputs[1])
    lp = N('ShaderNodeLightPath'); tr2 = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    L(lp.outputs['Is Camera Ray'], mx.inputs['Fac']); L(tr2.outputs['BSDF'], mx.inputs[1]); L(ad.outputs['Shader'], mx.inputs[2]); L(mx.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

# ============================================================================= TUNNEL
def _wall_profile():
    """Section of the roadway (s, z, outward normal s, z): left wall up, roof arch, right wall down."""
    pts = []
    for k in range(9):
        z = WALL_Z * k / 8; pts.append((-(WALL_HW + 0.06 - 0.04 * z), z, -1.0, 0.0))
    for k in range(1, 12):
        a = math.pi - math.pi * k / 12; hw = WALL_HW - 0.1
        pts.append((hw * math.cos(a), WALL_Z + (ROOF_Z - WALL_Z) * math.sin(a), math.cos(a), math.sin(a) * 1.6))
    for k in range(8, -1, -1):
        z = WALL_Z * k / 8; pts.append(((WALL_HW + 0.06 - 0.04 * z), z, 1.0, 0.0))
    return pts

def _tunnel(SET, P, C, TX, E, dress):
    tx = STATE['tx']; pre = STATE['pre']
    M = dict(coal=_untoon(mat_lit(pre + 't_coal_glint', image=tx['coal'], form=tuple(P['form']), glow=tx['glint'], glow_k=0.07)),   # glitter specks: painted (a GGX lobe here cost 1.3 CPU s)
             coal_face=_glossy(TX('coal_face', 1.0), (0.85, 0.9, 1.0), 1.1, 0.3, mask=tx['glint']),
             floor=TX('floor', form=False), timber=TX('timber'), timber_d=TX('timber_d'), lag=TX('lagging'), planks=TX('planks'), canvas=TX('canvas'),
             white=TX('whitewash', 1.0), tub=TX('tub', 1.0, (0.8, 0.9, 1.0)), lumps=_glossy(TX('lumps'), (0.8, 0.85, 1.0), 0.6, 0.25),
             rail=_glossy(C('#5e5c6a', 1.0, 1.1), (1.0, 0.95, 0.9), 0.45, 0.22), iron=_glossy(C('#3c3a44', 1.0, 1.1), (1.0, 0.95, 0.9), 0.35, 0.3),
             steel=_glossy(C('#5a5e6e', 1.0, 1.1), (1.0, 0.95, 0.9), 0.4, 0.3), brass=_glossy(_metal('brass', '#d8a848'), (1.0, 0.8, 0.45), 1.0, 0.22),
             brass_d=_glossy(_metal('brass_d', '#8a6428'), (1.0, 0.8, 0.45), 0.6, 0.3), red=C('#c03a2a'), red_d=C('#8a2a22'), cable=C('#24222a', 1.0, 1.2),
             rope=C('#b89a6a'), sack=C('#a89070'), sack_d=C('#7a6a52'), cloth=C('#3e4a6a'), cloth2=C('#6a4a3a'), tin=_glossy(C('#8a8a96'), (1, 1, 1), 0.5, 0.25),
             wood=C('#a07a46'), wood_d=C('#6e5232'), green=C('#3a6a4e'), cream=C('#e8dcc0'), stone=C('#8a8698'), dust=C('#9a929e'),
             puddle=_glossy(C('#1c2230', 1.0, 0.7, form=False), (0.85, 0.9, 1.0), 0.14, 0.3),
             wet=_glossy(C('#cfd8f0', 1.0, 0.6), (1, 1, 1), 1.0, 0.03),
             sign_pit=TX('sign_pit'), sign_danger=TX('sign_danger'), sign_heading=TX('sign_heading'),
             glass=_mat_glass(pre + 'glass'), gauze=TX('gauze', alpha=True),
             flame=mat_emit(pre + 'e_flame', '#ffa848', strength=7.0), flame_c=mat_emit(pre + 'e_flamec', '#fff2c4', strength=11.0),
             bulb=mat_emit(pre + 'e_bulb', '#fff0d0', strength=7.0), bulb_glow=mat_emit(pre + 'e_bulbg', '#ffdca0', strength=2.2))
    STATE['M'] = M
    _roadway(SET, M); _timber_sets(SET, M); _heading(SET, M); _pit_bottom(SET, M); _track(SET, M); _tubs(SET, M)
    _services(SET, M); _lamps(SET, M); _cage(SET, M)
    if dress: _tunnel_dressing(SET, M)
    _drips(SET, M); _gas_build(SET, M); _blast_build(SET, M)

def _roadway(SET, M):
    prof = _wall_profile(); per = [0.0]
    for a, b in zip(prof, prof[1:]): per.append(per[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    ys = [k * 0.5 for k in range(int(TUN_L / 0.5) + 1)]
    def disp(y, i):
        s, z, ns, nz = prof[i]; p = per[i]
        d = 0.26 * (vnoise(y * 0.7, p * 0.7, 3) - 0.5) + 0.12 * (vnoise(y * 2.3, p * 2.3, 4) - 0.5) + 0.05 * math.sin(z * 9.0 + vnoise(y, p, 5) * 3)
        if y < 0.6: d *= y / 0.6                                                 # the mouth meets the pit-bottom wall cleanly
        if z < 0.05: d *= 0.2
        return d
    V = {}
    for y in ys:
        for i, (s, z, ns, nz) in enumerate(prof):
            d = disp(y, i); n = Vector((ns, nz)); n.normalize()
            V[(y, i)] = TP(y, s + n.x * d, z + n.y * d)
    mb = MB(); wet = MB()
    for y0, y1 in zip(ys, ys[1:]):
        for i in range(len(prof) - 1):
            s, z = prof[i][0], prof[i][1]; z2 = prof[i + 1][1]
            if s < 0 and max(z, z2) <= HEAD_H + 0.01 and HEAD_Y[0] <= y0 and y1 <= HEAD_Y[1]: continue       # the heading's mouth
            mat = M['coal']
            mb.face([V[(y0, i)], V[(y1, i)], V[(y1, i + 1)], V[(y0, i + 1)]], mat, [(y0 / 4, per[i] / 4), (y1 / 4, per[i] / 4), (y1 / 4, per[i + 1] / 4), (y0 / 4, per[i + 1] / 4)])
    # the coal face at the inbye end
    n = len(prof); cface = TP(TUN_L + 0.2, 0, 2.2)
    for i in range(n - 1):
        a, b = V[(TUN_L, i)], V[(TUN_L, i + 1)]
        mb.face([a, b, cface], M['coal_face'], [(prof[i][0] / 4, prof[i][1] / 4), (prof[i + 1][0] / 4, prof[i + 1][1] / 4), (0, 0.55)])
    mb.face([V[(TUN_L, n - 1)], V[(TUN_L, 0)], cface], M['coal_face'], [(0.65, 0), (-0.65, 0), (0, 0.55)])
    o = _obj(mb, 'roadway', SET)
    # floor (dust, centred on the curve) with wet streaks along the walls
    fb = MB()
    for y0, y1 in zip(ys, ys[1:]):
        for s0, s1 in ((-WALL_HW - 0.1, -1.0), (-1.0, 1.0), (1.0, WALL_HW + 0.1)):
            fb.face([TP(y0, s0, 0.0), TP(y0, s1, 0.0), TP(y1, s1, 0.0), TP(y1, s0, 0.0)], M['floor'], [(s0 / 4, y0 / 4), (s1 / 4, y0 / 4), (s1 / 4, y1 / 4), (s0 / 4, y1 / 4)])
    _obj(fb, 'roadway_floor', SET)
    STATE['V'] = V; STATE['prof'] = prof

def _timber_sets(SET, M):
    """Pit props (legs) and cap beams (bars) every 2.5 D, lid wedges, lagging boards over the bars and behind the legs."""
    mb = MB(); lag = MB(); r = _rnd(7)
    for k, y in enumerate(SET_Y):
        t = tangent(y); rr = right(y); Z = Vector((0, 0, 1))
        for side in (-1, 1):
            if side < 0 and HEAD_Y[0] - 0.4 < y < HEAD_Y[1] + 0.4: continue     # the heading has its own frame
            foot = TP(y, side * (LEG_S + 0.1), 0.0); top = TP(y, side * (LEG_S - 0.08), CAP_Z)
            rod(mb, foot, top, 0.17 + 0.015 * r.random(), M['timber'], seg=8, uv=(1.0, (top - foot).length / 2))
            lid = TP(y, side * (LEG_S - 0.08), CAP_Z - 0.02)
            obox(mb, lid - Z * 0.12, t, rr, Z, 0.2, 0.06, 0.12, M['timber_d'])
        a = TP(y, -LEG_S - 0.32, CAP_Z + CAP_T / 2); b = TP(y, LEG_S + 0.32, CAP_Z + CAP_T / 2)
        beam(mb, a + t * 0.0, b, 0.36, CAP_T, M['timber'], uvk=0.5)
        for s in (-1.4, 0.15, 1.5):                                                  # wedges between bar and roof
            obox(mb, TP(y, s + r.uniform(-0.2, 0.2), CAP_Z + CAP_T + 0.09), t, rr, Z, 0.2, 0.09, 0.09, M['timber_d'])
    for k in range(len(SET_Y) - 1):                                                  # lagging boards over the bars
        ya, yb = SET_Y[k], SET_Y[k + 1]
        for s in (-1.9, -1.15, -0.4, 0.4, 1.15, 1.9):
            if r.random() < 0.15: continue
            ds = r.uniform(-0.1, 0.1); zt = CAP_Z + CAP_T + 0.03
            pa = TP(ya - 0.25, s + ds, zt); pb = TP(yb + 0.25, s + ds + r.uniform(-0.15, 0.15), zt)
            beam(lag, pa, pb, 0.5, 0.06, M['lag'], uvk=0.5)
        for side in (-1, 1):                                                         # boards behind the legs
            if side < 0 and HEAD_Y[0] - 2.5 < ya < HEAD_Y[1] + 0.5: continue
            if r.random() < 0.35: continue
            for z in (0.9, 1.8, 2.7, 3.5):
                if r.random() < 0.25: continue
                s0 = side * (LEG_S + 0.26 - 0.01 * z)
                beam(lag, TP(ya - 0.2, s0, z), TP(yb + 0.2, s0, z + r.uniform(-0.12, 0.12)), 0.08, 0.42, M['lag'], uvk=0.5)
    _obj(mb, 'timber_sets', SET, hull=0.025); _obj(lag, 'lagging', SET)

def _heading(SET, M):
    """Side heading off the left wall (y 19.5..23): a straight drift running -x for 10 D to a coal face, own timber sets, the
    ventilation door frame with its canvas sheet just inside the mouth."""
    yc = sum(HEAD_Y) / 2; o = TP(yc, -WALL_HW + 0.3, 0.0); ax = -right(yc); tg = tangent(yc)        # ax: into the heading
    hw = (HEAD_Y[1] - HEAD_Y[0]) / 2; mb = MB(); r = _rnd(19)
    def HP(u, v, z): return o + ax * u + tg * v + Vector((0, 0, z))
    us = [k * 0.5 for k in range(int(HEAD_LEN / 0.5) + 1)]
    prof = [(-hw, z) for z in (0, 0.9, 1.8, 2.7, HEAD_H)] + [(-hw * 0.5, HEAD_H + 0.25), (0, HEAD_H + 0.32), (hw * 0.5, HEAD_H + 0.25)] + [(hw, z) for z in (HEAD_H, 2.7, 1.8, 0.9, 0)]
    per = [0.0]
    for a, b in zip(prof, prof[1:]): per.append(per[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    def V(u, i):
        v, z = prof[i]; d = 0.0 if u < 0.6 else 0.2 * (vnoise(u * 0.8, per[i] * 0.8, 9) - 0.5)
        nv = (-1 if v < -0.01 else (1 if v > 0.01 else 0)); nz = 1 if z > HEAD_H - 0.01 else 0
        return HP(u, v + nv * d, z + nz * d)
    for u0, u1 in zip(us, us[1:]):
        for i in range(len(prof) - 1):
            mb.face([V(u0, i), V(u1, i), V(u1, i + 1), V(u0, i + 1)], M['coal'], [(u0 / 4, per[i] / 4), (u1 / 4, per[i] / 4), (u1 / 4, per[i + 1] / 4), (u0 / 4, per[i + 1] / 4)])
        mb.face([HP(u0, -hw, 0.002), HP(u1, -hw, 0.002), HP(u1, hw, 0.002), HP(u0, hw, 0.002)], M['floor'], [(u0 / 4, -hw / 4), (u1 / 4, -hw / 4), (u1 / 4, hw / 4), (u0 / 4, hw / 4)])
    endc = HP(HEAD_LEN + 0.1, 0, 1.8)
    for i in range(len(prof) - 1): mb.face([V(HEAD_LEN, i), V(HEAD_LEN, i + 1), endc], M['coal_face'], [(prof[i][0] / 4, prof[i][1] / 4), (prof[i + 1][0] / 4, prof[i + 1][1] / 4), (0, 0.45)])
    _obj(mb, 'heading', SET)
    tb = MB(); Z = Vector((0, 0, 1))
    for u in (0.35, 2.8, 5.3, 7.8):                                                   # heading sets
        for sv in (-1, 1): rod(tb, HP(u, sv * (hw - 0.15), 0), HP(u, sv * (hw - 0.25), HEAD_H - 0.05), 0.16, M['timber'], seg=8, uv=(1.0, 1.7))
        beam(tb, HP(u, -hw - 0.1, HEAD_H + 0.1), HP(u, hw + 0.1, HEAD_H + 0.1), 0.34, 0.3, M['timber'], up=(0, 0, 1), uvk=0.5)
    for k in range(3):
        for sv in (-1.0, 0.0, 1.0):
            beam(tb, HP(0.35 + 2.5 * k - 0.2, sv, HEAD_H + 0.28), HP(2.8 + 2.5 * k + 0.2, sv + r.uniform(-0.1, 0.1), HEAD_H + 0.28), 0.45, 0.06, M['lag'], uvk=0.5)
    # ventilation door frame at u 1.5: posts, head, sill board, the canvas sheet (left half hanging, right half hooked back)
    ud = 1.6
    for sv in (-1, 1): beam(tb, HP(ud, sv * (hw - 0.3), 0), HP(ud, sv * (hw - 0.3), HEAD_H - 0.2), 0.28, 0.28, M['timber_d'], up=tuple(ax), uvk=0.5)
    beam(tb, HP(ud, -hw + 0.05, HEAD_H - 0.25), HP(ud, hw - 0.05, HEAD_H - 0.25), 0.3, 0.3, M['timber_d'], up=(0, 0, 1), uvk=0.5)
    beam(tb, HP(ud, -hw + 0.3, 0.05), HP(ud, hw - 0.3, 0.05), 0.3, 0.1, M['timber_d'], uvk=0.5)
    _obj(tb, 'heading_timber', SET, hull=0.025)
    cv = MB(); z0, z1 = 0.12, HEAD_H - 0.42; nseg = 10
    for (va, vb, bunch) in ((-hw + 0.45, 0.1, 0.0), (0.3, hw - 0.45, 1.0)):
        for k in range(nseg):
            for j in range(6):
                t0, t1 = k / nseg, (k + 1) / nseg; za, zb = z0 + (z1 - z0) * j / 6, z0 + (z1 - z0) * (j + 1) / 6
                def CP(t, z):
                    hb = (z - z0) / (z1 - z0)
                    if bunch: v = vb - (vb - va) * t * (0.35 + 0.65 * (1 - hb) ** 2) * 0.55 - 0.05; fold = 0.18 * math.sin(t * 9 + z)
                    else: v = va + (vb - va) * t; fold = 0.07 * math.sin(t * 13 + 1.0) * (0.4 + 0.6 * (1 - hb))
                    return HP(ud + 0.2 + fold + (0.15 * (1 - hb) if bunch else 0.0), v, z)
                cv.face([CP(t0, za), CP(t1, za), CP(t1, zb), CP(t0, zb)], M['canvas'], [((va + (vb - va) * t0 + hw) / 3, za / 4), ((va + (vb - va) * t1 + hw) / 3, za / 4), ((va + (vb - va) * t1 + hw) / 3, zb / 4), ((va + (vb - va) * t0 + hw) / 3, zb / 4)])
    rod(cv, HP(ud + 0.18, -hw + 0.3, z1 + 0.04), HP(ud + 0.18, hw - 0.3, z1 + 0.04), 0.035, M['iron'], seg=6)
    o2 = _obj(cv, 'vent_door', SET, hull=0.012)
    STATE['heading'] = dict(mouth=tuple(round(c, 3) for c in HP(0, 0, 0)), axis=tuple(round(c, 4) for c in ax), end=tuple(round(c, 3) for c in HP(HEAD_LEN, 0, 0)), door=tuple(round(c, 3) for c in HP(ud, 0, 0)),
                            half_width=hw, height=HEAD_H)
    STATE['HP'] = HP

def _pit_bottom(SET, M):
    """Pit bottom y -10..0: whitewashed chamber with steel joists and electric lamps, the end wall round the roadway mouth, the shaft
    behind (y -13.5..-10, brick lined, rising out of frame) with the cage, its gates and guides."""
    mb = MB(); st = MB(); hw = PB_HW; H = PB_H; y0 = PB_Y0
    mb.quad((-hw, y0, 0), (2 * hw, 0, 0), (0, -y0, 0), M['floor'], (-hw / 4, y0 / 4, hw / 4, 0))
    mb.quad((-hw, 0, H), (2 * hw, 0, 0), (0, y0, 0), M['planks'], (0, 0, 2 * hw / 2, -y0 / 2))
    for sx in (-1, 1): mb.oface([(sx * hw, y0, 0), (sx * hw, 0, 0), (sx * hw, 0, H), (sx * hw, y0, H)], M['white'], [(y0 / 4, 0), (0, 0), (0, H / 4), (y0 / 4, H / 4)], (-sx, 0, 0))
    prof = STATE['prof']; V = STATE['V']; c = Vector((0, 0, 2.6))                     # end wall round the roadway mouth
    def box_pt(p):
        d = Vector((p.x, 0, p.z)) - c; k = min(hw / max(abs(d.x), 1e-6), (H - c.z) / max(d.z, 1e-6) if d.z > 0 else 1e9, c.z / max(-d.z, 1e-6) if d.z < 0 else 1e9)
        return c + d * k
    for i in range(len(prof) - 1):
        a = V[(0.0, i)]; b = V[(0.0, i + 1)]; A_, B_ = box_pt(a), box_pt(b)
        mb.oface([Vector((a.x, -0.01, a.z)), Vector((b.x, -0.01, b.z)), Vector((B_.x, -0.01, B_.z)), Vector((A_.x, -0.01, A_.z))], M['white'], [(a.x / 4, a.z / 4), (b.x / 4, b.z / 4), (B_.x / 4, B_.z / 4), (A_.x / 4, A_.z / 4)], (0, -1, 0))
    mb.oface([Vector((-hw, -0.01, H)), Vector((-hw, -0.01, 0)), box_pt(V[(0.0, 0)])], M['white'], [(0, 0)] * 3, (0, -1, 0))
    # far wall with the shaft opening (x -2.2..2.2, z 0..4.4)
    for (xa, xb, za, zb) in ((-hw, -2.2, 0, H), (2.2, hw, 0, H), (-2.2, 2.2, 4.4, H)):
        mb.oface([(xa, y0, za), (xb, y0, za), (xb, y0, zb), (xa, y0, zb)], M['white'], [(xa / 4, za / 4), (xb / 4, za / 4), (xb / 4, zb / 4), (xa / 4, zb / 4)], (0, 1, 0))
    # shaft: brick-lined box rising 40 D, floor (sump cover)
    sy0, sy1 = SHAFT_Y
    for (p0, pu, nrm) in (((-2.4, sy0, 0), (0, sy1 - sy0, 0), (1, 0, 0)), ((2.4, sy1, 0), (0, sy0 - sy1, 0), (-1, 0, 0)), ((2.4, sy0, 0), (-4.8, 0, 0), (0, 1, 0))):
        p0 = Vector(p0); pu = Vector(pu)
        mb.oface([p0, p0 + pu, p0 + pu + Vector((0, 0, 40)), p0 + Vector((0, 0, 40))], M['white'], [(0, 0), (pu.length / 4, 0), (pu.length / 4, 10), (0, 10)], nrm)
    mb.oface([(-2.4, y0, 4.4), (2.4, y0, 4.4), (2.4, y0, 40), (-2.4, y0, 40)], M['white'], [(0, 0), (1.2, 0), (1.2, 9), (0, 9)], (0, -1, 0))
    mb.quad((-2.4, sy0, -0.01), (4.8, 0, 0), (0, sy1 - sy0, 0), M['planks'], (0, 0, 2.4, 1.75))
    _obj(mb, 'pit_bottom', SET)
    for k in range(7):                                                              # steel joists (I-beams) across the roof
        y = -0.7 - 1.45 * k
        st.box((-hw, y - 0.16, H - 0.36), (hw, y + 0.16, H - 0.3), M['steel']); st.box((-hw, y - 0.04, H - 0.3), (hw, y + 0.04, H), M['steel']); st.box((-hw, y - 0.16, H - 0.06), (hw, y + 0.16, H), M['steel'])
    for sx in (-1, 1):                                                               # wall plates and posts at the mouth
        st.box((sx * hw - 0.2 if sx > 0 else -hw, -9.9, H - 0.6), (hw if sx > 0 else -hw + 0.2, -0.1, H - 0.36), M['steel'])
    st.box((-2.5, y0 + 0.02, 4.3), (2.5, y0 + 0.35, 4.6), M['steel'])
    for sx in (-2.35, 2.35): st.box((sx - 0.15, y0 + 0.02, 0), (sx + 0.15, y0 + 0.3, 4.4), M['steel'])
    for gx in (-1.9, 1.9):                                                           # wooden cage guides up the shaft
        st.box((gx - 0.1, -11.85, -0.2), (gx + 0.1, -11.65, 40), M['timber_d'])
    _obj(st, 'pit_bottom_steel', SET, hull=0.02)
    # the cage: steel frame with two decks, roof bow, rope cappel, gates (lattice) at the pit bottom
    cg = MB(); cy = -11.75; w2, d2, h = 1.65, 1.35, 3.5
    for sx in (-1, 1):
        for sy in (-1, 1): cg.box((sx * w2 - 0.07, cy + sy * d2 - 0.07, 0.05), (sx * w2 + 0.07, cy + sy * d2 + 0.07, h * 2 + 0.3), M['iron'])
    for z in (0.05, h, 2 * h):
        cg.box((-w2, cy - d2, z), (w2, cy + d2, z + 0.12), M['steel'])
    for sx in (-1, 1):
        for k in range(9): cg.box((sx * w2 - 0.025, cy - d2 + k * 0.33, 0.17), (sx * w2 + 0.025, cy - d2 + k * 0.33 + 0.04, h), M['iron'])
    cg.box((-w2, cy + d2 - 0.04, 0.17), (w2, cy + d2, h), M['planks'])
    rod(cg, (0, cy, 2 * h + 0.3), (0, cy, 2 * h + 1.6), 0.1, M['iron'], seg=8); rod(cg, (0, cy, 2 * h + 1.6), (0, cy, 40), 0.07, M['cable'], seg=6)
    for k in range(4): rod(cg, (-w2 + 0.1, cy - d2 + 0.1 + k * 0.85 * (k % 2), 2 * h + 0.3), (0, cy, 2 * h + 1.2), 0.03, M['iron'], seg=4)
    _obj(cg, 'cage_lift', SET, hull=0.015)
    gt = MB(); gy = y0 + 0.45                                                        # the pit-bottom gates, half drawn back
    for (xa, xb) in ((-2.2, -1.25), (1.1, 2.2)):
        gt.box((xa, gy - 0.04, 0.0), (xb, gy + 0.04, 0.08), M['iron']); gt.box((xa, gy - 0.04, 2.6), (xb, gy + 0.04, 2.68), M['iron'])
        n = int((xb - xa) / 0.18)
        for k in range(n + 1):
            x = xa + k * (xb - xa) / n; gt.box((x - 0.02, gy - 0.02, 0.0), (x + 0.02, gy + 0.02, 2.68), M['iron'])
        for k in range(n):
            xa_ = xa + k * (xb - xa) / n; xb_ = xa + (k + 1) * (xb - xa) / n
            beam(gt, (xa_, gy, 0.15), (xb_, gy, 2.5), 0.03, 0.03, M['iron']); beam(gt, (xb_, gy, 0.15), (xa_, gy, 2.5), 0.03, 0.03, M['iron'])
    _obj(gt, 'cage_gates', SET, hull=0.01)

def _track(SET, M):
    """Rails (with the curve), sleepers, haulage rope rollers between the rails, from the cage to the face."""
    mb = MB(); sl = MB(); r = _rnd(23)
    ys = [-11.5 + 0.5 * k for k in range(int((38.5 + 11.5) / 0.5) + 1)]
    for rs in (TRACK_S - GAUGE / 2, TRACK_S + GAUGE / 2):
        for y0, y1 in zip(ys, ys[1:]):
            p = lambda y, ds, z: TP(y, rs + ds, z)
            mb.face([p(y0, -0.05, 0.19), p(y0, 0.05, 0.19), p(y1, 0.05, 0.19), p(y1, -0.05, 0.19)], M['rail'])
            for ds in (-0.05, 0.05): mb.face([p(y0, ds, 0.07), p(y1, ds, 0.07), p(y1, ds, 0.19), p(y0, ds, 0.19)], M['rail'])
            for ds in (-0.1, 0.1): mb.face([p(y0, ds, 0.07), p(y1, ds, 0.07), p(y1, ds * 0.5, 0.1), p(y0, ds * 0.5, 0.1)], M['iron'])
    y = -11.4
    while y < 38.6:
        t = tangent(y); rr = right(y); Z = Vector((0, 0, 1))
        obox(sl, TP(y, TRACK_S + r.uniform(-0.05, 0.05), 0.04), t, rr, Z, 0.13, 0.85, 0.04, M['timber_d'], uvk=0.5); y += 0.72
    for k in range(13):                                                              # rope rollers
        y = 1.0 + k * 3.0; t = tangent(y); rr = right(y)
        rod(sl, TP(y, TRACK_S - 0.18, 0.13), TP(y, TRACK_S + 0.18, 0.13), 0.07, M['iron'], seg=8)
        obox(sl, TP(y, TRACK_S, 0.06), t, rr, Vector((0, 0, 1)), 0.1, 0.25, 0.04, M['timber'])
    pts = [TP(-11.0 + 0.5 * k, TRACK_S, 0.215) for k in range(100)]
    chain_rod(sl, pts, 0.025, M['cable'], seg=4)
    _obj(mb, 'rails', SET); _obj(sl, 'sleepers', SET)

TUBS = [(-11.75, 0.0, True), (-4.5, 0.0, True), (12.8, 0.0, True), (14.95, 0.0, True), (17.1, 0.0, False), (34.5, 0.0, True)]
def _tub(mb, y, M, loaded=True, seed=0, ds=0.0):
    t = tangent(y); rr = right(y); Z = Vector((0, 0, 1)); c = TP(y, TRACK_S + ds, 0.0)
    L2, W2, z0, z1 = 0.95, 0.68, 0.32, 1.3
    for (n, a, ha) in ((rr, t, L2), (-rr, t, L2), (t, rr, W2), (-t, rr, W2)):           # sides (tub texture), flared slightly
        hn = W2 if (n - rr).length < 1e-6 or (n + rr).length < 1e-6 else L2
        p = [c + n * hn - a * ha + Z * z0, c + n * hn + a * ha + Z * z0, c + n * (hn + 0.06) + a * (ha + 0.04) + Z * z1, c + n * (hn + 0.06) - a * (ha + 0.04) + Z * z1]
        mb.oface(p, M['tub'], [(0, 0), (2, 0), (2, 1.4), (0, 1.4)], n)
        pi_ = [c + n * (hn - 0.06) - a * (ha - 0.06) + Z * (z0 + 0.06), c + n * (hn - 0.06) + a * (ha - 0.06) + Z * (z0 + 0.06), c + n * (hn) + a * (ha - 0.02) + Z * z1, c + n * (hn) - a * (ha - 0.02) + Z * z1]
        mb.oface(pi_, M['wood_d'], [(0, 0)] * 4, -n)
    mb.oface([c - t * L2 - rr * W2 + Z * z0, c + t * L2 - rr * W2 + Z * z0, c + t * L2 + rr * W2 + Z * z0, c - t * L2 + rr * W2 + Z * z0], M['iron'], [(0, 0)] * 4, (0, 0, -1))
    for sa in (-1, 1):                                                                      # rim bands
        beam(mb, c + t * sa * (L2 + 0.05) - rr * (W2 + 0.07) + Z * z1, c + t * sa * (L2 + 0.05) + rr * (W2 + 0.07) + Z * z1, 0.06, 0.06, M['iron'])
        beam(mb, c - t * (L2 + 0.05) + rr * sa * (W2 + 0.07) + Z * z1, c + t * (L2 + 0.05) + rr * sa * (W2 + 0.07) + Z * z1, 0.06, 0.06, M['iron'])
    for sa in (-1, 1):                                                                      # wheels on axles
        for sb in (-1, 1):
            hub = c + t * sa * 0.55 + rr * sb * (GAUGE / 2) + Z * 0.27 - rr * (TRACK_S - TRACK_S)
            mb.frustum(hub - rr * 0.06, hub + rr * 0.06, 0.25, 0.25, M['iron'], seg=12)
        rod(mb, c + t * sa * 0.55 - rr * 0.65 + Z * 0.27, c + t * sa * 0.55 + rr * 0.65 + Z * 0.27, 0.05, M['iron'], seg=6)
    for sa in (-1, 1): rod(mb, c + t * sa * (L2 + 0.02) + Z * 0.45, c + t * sa * (L2 + 0.3) + Z * 0.45, 0.04, M['iron'], seg=4)
    if loaded:
        lumpy(mb, c + Z * (z1 - 0.05), 1.0, M['lumps'], seed, seg=12, rings=6, rough=0.25, squash=0.42)

def _tubs(SET, M):
    mb = MB()
    for i, (y, ds, ld) in enumerate(TUBS):
        if y < -10: continue
        _tub(mb, y, M, ld, seed=40 + i, ds=ds)
    _obj(mb, 'tubs', SET, hull=0.02)
    cb = MB()                                                                          # couplings of the train
    for ya, yb in ((12.8, 14.95), (14.95, 17.1)):
        chain_rod(cb, catenary(TP(ya + 1.25, TRACK_S, 0.45), TP(yb - 1.25, TRACK_S, 0.45), 0.08, 4), 0.03, M['iron'], seg=4)
    tc = MB(); _tub(tc, -11.75, M, True, seed=47); _obj(tc, 'tub_in_cage', SET, hull=0.02); _obj(cb, 'couplings', SET)

def _services(SET, M):
    """Two power / signal cables catenaried along the left wall on hooks at every set, the compressed-air pipe on brackets along the
    right wall, the bell wire under the roof."""
    mb = MB(); pp = MB(); r = _rnd(29)
    ys = [y for y in SET_Y]
    for (sz, sg) in ((3.65, 0.28), (3.35, 0.22)):
        for ya, yb in zip(ys, ys[1:]):
            if HEAD_Y[0] - 0.5 < ya < HEAD_Y[1]:                                  # across the heading mouth: span on the bars
                a = TP(ya, -2.05, CAP_Z - 0.06); b = TP(yb, -2.05, CAP_Z - 0.06); chain_rod(mb, catenary(a, b, sg * 0.6, 10), 0.035, M['cable']); continue
            a = TP(ya, -LEG_S + 0.08, sz); b = TP(yb, -LEG_S + 0.08, sz); chain_rod(mb, catenary(a, b, sg, 10), 0.035, M['cable'])
    for y in ys:
        for sz in (3.65, 3.35): rod(mb, TP(y, -LEG_S + 0.1, sz + 0.12), TP(y, -LEG_S + 0.1, sz - 0.02), 0.025, M['iron'], seg=4)
    pts = [TP(0.3 + 0.5 * k, 0.0, 4.9 - 0.02 * math.sin(k)) for k in range(78)]; chain_rod(mb, pts, 0.012, M['cable'], seg=4)
    for k in range(39):                                                              # air pipe
        y0, y1 = 0.2 + k * 1.0, 1.2 + k * 1.0
        pp.frustum(TP(y0, LEG_S + 0.05, 0.55), TP(y1, LEG_S + 0.05, 0.55), 0.11, 0.11, M['iron'], seg=8, cap0=False, cap1=False)
        if k % 3 == 0:
            pp.frustum(TP(y0 - 0.04, LEG_S + 0.05, 0.55), TP(y0 + 0.04, LEG_S + 0.05, 0.55), 0.16, 0.16, M['iron'], seg=8)
    for y in SET_Y: obox(pp, TP(y + 0.25, LEG_S + 0.05, 0.38), tangent(y), right(y), Vector((0, 0, 1)), 0.06, 0.14, 0.06, M['timber_d'])
    _obj(mb, 'cables', SET); _obj(pp, 'air_pipe', SET)

# ----------------------------------------------------------------------------- lamps
def _safety_lamp(mb, gm, fl, top, M, s=1.0, ring=True):
    """Flame safety lamp hanging from `top` (the hook point): ring, bonnet, gauze, glass with the flame inside, pillars, oil vessel.
    Height 0.55 x s D. Returns the flame centre."""
    Z = Vector((0, 0, 1)); t = Vector(top)
    if ring:
        pts = [t + Vector((0.05 * s * math.sin(a), 0, -0.05 * s - 0.05 * s * math.cos(a))) for a in [2 * math.pi * k / 10 for k in range(11)]]
        chain_rod(mb, pts, 0.012 * s, M['brass'], seg=4)
    z = t.z - 0.1 * s
    mb.frustum(t - Z * (0.1 * s), t - Z * (0.16 * s), 0.03 * s, 0.075 * s, M['brass'], seg=12)                  # bonnet
    mb.frustum(t - Z * (0.16 * s), t - Z * (0.19 * s), 0.08 * s, 0.08 * s, M['brass_d'], seg=12)
    gm.frustum(t - Z * (0.19 * s), t - Z * (0.3 * s), 0.065 * s, 0.07 * s, M['gauze'], seg=12, cap0=False, cap1=False, uv_wrap=(0.45 * s, 0.11 * s))
    mb.frustum(t - Z * (0.3 * s), t - Z * (0.32 * s), 0.09 * s, 0.09 * s, M['brass'], seg=12)
    gm.frustum(t - Z * (0.32 * s), t - Z * (0.44 * s), 0.075 * s, 0.075 * s, M['glass'], seg=12, cap0=False, cap1=False)
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2; d = Vector((math.cos(a), math.sin(a), 0)) * 0.088 * s
        rod(mb, t - Z * (0.18 * s) + d, t - Z * (0.46 * s) + d, 0.008 * s, M['brass'], seg=4)
    mb.frustum(t - Z * (0.44 * s), t - Z * (0.47 * s), 0.095 * s, 0.095 * s, M['brass'], seg=12)
    mb.frustum(t - Z * (0.47 * s), t - Z * (0.56 * s), 0.09 * s, 0.1 * s, M['brass_d'], seg=12)
    mb.frustum(t - Z * (0.56 * s), t - Z * (0.58 * s), 0.1 * s, 0.085 * s, M['brass'], seg=12)
    fc = t - Z * (0.395 * s)
    fl.frustum(fc - Z * 0.035 * s, fc + Z * 0.01 * s, 0.012 * s, 0.022 * s, M['flame'], seg=8, cap0=True, cap1=False)
    fl.frustum(fc + Z * 0.01 * s, fc + Z * 0.05 * s, 0.022 * s, 0.0, M['flame'], seg=8, cap0=False)
    fl.frustum(fc - Z * 0.02 * s, fc + Z * 0.02 * s, 0.008 * s, 0.0, M['flame_c'], seg=6)
    return fc

def _lamp_bulb(mb, fl, top, M, s=1.0):
    """Electric pit-bottom lamp: conduit drop, enamel reflector shade, bulb (emitter)."""
    Z = Vector((0, 0, 1)); t = Vector(top)
    rod(mb, t, t - Z * 0.5 * s, 0.025, M['iron'], seg=4)
    mb.frustum(t - Z * 0.5 * s, t - Z * 0.75 * s, 0.08 * s, 0.42 * s, M['green'], seg=14, cap0=True, cap1=False)
    mb.frustum(t - Z * 0.75 * s, t - Z * 0.5 * s, 0.4 * s, 0.07 * s, M['cream'], seg=14, cap0=False, cap1=False)
    fl.sphere(t - Z * 0.74 * s, 0.13 * s, M['bulb'], seg=10, rings=6)
    return t - Z * 0.78 * s

# fixed hanging lamps: (station y, s, hook z); index 2 hangs behind the canary cage from the cage_insert camera
FIXED_LAMPS = [(6.25, -1.45, CAP_Z), (13.75, 1.55, CAP_Z), (18.75, -1.35, CAP_Z), (26.25, -1.5, CAP_Z), (33.75, 1.45, CAP_Z), (38.75, -0.9, CAP_Z)]
INSERT_LAMP = (8.75, 1.25, CAP_Z)                               # the foreman's lamp: S-hook and chain under the bar of set 3 (lamp_insert)
CAGE_HOOK = (16.25, -LEG_S + 0.42, 3.3)                        # nail on the left leg of set 6 that the canary cage hangs from
PB_LAMPS = [(0.0, -2.0, PB_H - 0.3), (0.0, -5.6, PB_H - 0.3), (0.0, -9.0, PB_H - 0.3)]

def _lamps(SET, M):
    P = STATE['P']; mb = MB(); gm = MB(); fl = MB(); STATE['fixed_lamps'] = []; pool = MB(); pm = _mat_pool(STATE['pre'] + 'pool', (1.0, 0.74, 0.4), 0.3)
    pre = STATE['pre']; tx = STATE['tx']                                            # lamp bodies: own brass / gauze, glowing with their flames (painted)
    lb = _glossy(_metal('lamp_brass', '#d8a848'), (1.0, 0.8, 0.45), 1.0, 0.22); lbd = _glossy(_metal('lamp_brass_d', '#8a6428'), (1.0, 0.8, 0.45), 0.6, 0.3)
    lg = _untoon(mat_lit(pre + 'lamp_gauze', image=tx['gauze'], alpha=True, form=tuple(P['form']), shade_mul=(2.4, 1.6, 0.55), shade_mix=0.15))
    M = dict(M, brass=lb, brass_d=lbd, gauze=lg); flames = []
    halo = MB(); hm = _mat_pool(pre + 'halo', (1.0, 0.72, 0.36), 0.55)
    for i, (y, s, z) in enumerate(FIXED_LAMPS):
        hook = TP(y, s, z); rod(mb, hook + Vector((0, 0, 0.02)), hook - Vector((0, 0, 0.32)), 0.012, M['iron'], seg=4)   # S-hook / chain
        fc = _safety_lamp(mb, gm, fl, hook - Vector((0, 0, 0.32)), M, s=1.0)
        L = _light('fixed_lamp_%d' % i, fc, WARM, LAMP_E * 1.1 * P['lamp_k'], radius=0.04); STATE['fixed_lamps'].append(L)
        flames.append(tuple(fc)); L.data.use_shadow = False                      # fixed lamps: shadowless (-1.7 CPU s, no visible change)
        for ax_ in (tangent(y), right(y)):                                          # halo: two crossed camera-only glow cards round the flame
            u_ = ax_.cross(Vector((0, 0, 1))).normalized(); w_ = Vector((0, 0, 1))
            halo.face([fc - u_ * 0.55 - w_ * 0.55, fc + u_ * 0.55 - w_ * 0.55, fc + u_ * 0.55 + w_ * 0.55, fc - u_ * 0.55 + w_ * 0.55], hm, [(0, 0), (1, 0), (1, 1), (0, 1)])
        pc = TP(y, s * 0.6, 0.015); t_ = tangent(y); r_ = right(y)
        pool.face([pc - t_ * 2.4 - r_ * 2.4, pc + t_ * 2.4 - r_ * 2.4, pc + t_ * 2.4 + r_ * 2.4, pc - t_ * 2.4 + r_ * 2.4], pm, [(0, 0), (1, 0), (1, 1), (0, 1)])
    hk = TP(*INSERT_LAMP); t = tangent(INSERT_LAMP[0]); rr = right(INSERT_LAMP[0])
    zc = Vector((0, 0, 1)); links = 6; top = hk
    for k in range(links):                                                          # short chain of oval links from the bar
        a = top - zc * (0.07 * k); b = a - zc * 0.075; ax = t if k % 2 else rr
        chain_rod(mb, [a + ax * 0.0, a + ax * 0.025 - zc * 0.012, b + ax * 0.025 + zc * 0.012, b, b - ax * 0.025 + zc * 0.012, a - ax * 0.025 - zc * 0.012, a], 0.007, M['iron'], seg=4)
    hk = top - zc * (0.07 * links + 0.02)
    im = MB(); ig = MB(); ifl = MB()
    M2 = dict(M, flame=mat_emit(STATE['pre'] + 'e_flame_ins', '#ffa848', strength=7.0), flame_c=mat_emit(STATE['pre'] + 'e_flamec_ins', '#fff2c4', strength=11.0))
    fc = _safety_lamp(im, ig, ifl, hk, M2, s=1.0)
    STATE['insert_flame_pos'] = fc
    flames.append(tuple(fc))
    for mat_, k_ in ((lb, 2.2), (lbd, 2.2), (lg, 3.0)): G._extra(mat_, glow=(flames, (1.0, 0.78, 0.45), k_, 0.16))
    io = _obj(im, 'insert_lamp', SET, shadow=False); io2 = _obj(ig, 'insert_lamp_glass', SET, shadow=False)
    ifo = _obj(ifl, 'insert_flame', SET, shadow=False); ifo['glossy_vis'] = 1; STATE['insert_flame'] = ifo
    # flame pivot: scale the insert flame about its base
    piv = G._pivot('insert_flame_pivot', SET, tuple(fc - Vector((0, 0, 0.035)))); G._parent(ifo, piv); STATE['flame_pivot'] = piv
    STATE['insert_light'] = _light('insert_lamp_light', fc, WARM, LAMP_E * 0.9 * P['lamp_k'], radius=0.03)
    for i, top in enumerate(PB_LAMPS):
        b = _lamp_bulb(mb, fl, top, M, 1.0)
        if i != 1: _light('pb_lamp_%d' % i, b, BULB, 700.0 if i == 2 else 520.0, radius=0.1).data.use_shadow = False
    _light('pb_fill', (0, -0.8, 3.4), BULB, 220.0, radius=0.7).data.use_shadow = False                        # the mouth: light spilling into the roadway
    po = _obj(pool, 'lamp_pools', SET, shadow=False); STATE['pool_mat'] = pm; _obj(halo, 'lamp_halos', SET, shadow=False)
    o = _obj(mb, 'lamps', SET, shadow=False); o2 = _obj(gm, 'lamp_glass', SET, shadow=False); f = _obj(fl, 'lamp_flames', SET, shadow=False); f['glossy_vis'] = 1
    STATE['lamp_flames'] = f
    # light linking: a lamp's own light does not light its own brass / glass (else the whole lamp blows out into one glow)
    ex = bpy.data.collections.get('MIN_lamp_bodies') or bpy.data.collections.new('MIN_lamp_bodies')
    for ob_ in list(ex.objects): ex.objects.unlink(ob_)
    for ob_ in (o, o2, io, io2): ex.objects.link(ob_)
    for ob_ in ex.collection_objects: ob_.light_linking.link_state = 'EXCLUDE'
    for L_ in STATE['fixed_lamps'] + [STATE['insert_light']] + [STATE['objects'][n] for n in ('pb_lamp_0', 'pb_lamp_2')]:
        L_.light_linking.receiver_collection = ex

def _cage(SET, M):
    """The canary's brass cage (bird = cast sprite): round tray, 16 wires to a domed top, hanging ring, perch, door, seed and water
    cups; hangs from CAGE_HOOK (the nail). Pivot 'cage_pivot' at the hook point (set_cage moves / swings it)."""
    hook = TP(*CAGE_HOOK); y = CAGE_HOOK[0]; rr = right(y); t = tangent(y)
    nb = MB(); rod(nb, hook - rr * 0.32 + Vector((0, 0, -0.02)), hook + Vector((0, 0, -0.02)), 0.02, M['iron'], seg=4); rod(nb, hook, hook + Vector((0, 0, 0.08)), 0.02, M['iron'], seg=4)
    _obj(nb, 'cage_nail', SET)
    piv = G._pivot('cage_pivot', SET, tuple(hook)); STATE['cage_pivot'] = piv
    mb = MB(); B = M['brass']; R = 0.24; Hc = 0.5; top = Vector(hook); ring_r = 0.05
    c0 = top - Vector((0, 0, 2 * ring_r + 0.05 + Hc + 0.12))                          # tray bottom centre
    pts = [top + Vector((ring_r * math.sin(a), 0, -ring_r - ring_r * math.cos(a))) for a in [2 * math.pi * k / 12 for k in range(13)]]
    chain_rod(mb, pts, 0.01, B, seg=4)
    knob = top - Vector((0, 0, 2 * ring_r)); mb.sphere(knob - Vector((0, 0, 0.03)), 0.035, B, seg=8, rings=5)
    mb.frustum(c0, c0 + Vector((0, 0, 0.08)), R + 0.03, R + 0.02, M['brass_d'], seg=20)
    mb.frustum(c0 + Vector((0, 0, 0.08)), c0 + Vector((0, 0, 0.11)), R + 0.035, R + 0.035, B, seg=20)
    zr0 = c0.z + 0.11; zr1 = zr0 + Hc; dome = knob.z - 0.06
    for k in range(16):
        a = 2 * math.pi * k / 16; d = Vector((math.cos(a), math.sin(a), 0))
        wp = [c0 + d * R + Vector((0, 0, 0.11)), c0 + d * R + Vector((0, 0, Hc + 0.11))]
        for j in range(1, 6):
            u = j / 5; wp.append(Vector((knob.x, knob.y, 0)) + d * R * math.cos(u * math.pi / 2) + Vector((0, 0, zr1 + (dome - zr1) * math.sin(u * math.pi / 2))))
        chain_rod(mb, wp, 0.006, B, seg=4)
    for z in (zr0 + 0.12, zr1):                                                      # hoops
        pts = [Vector((c0.x, c0.y, z)) + Vector((math.cos(a), math.sin(a), 0)) * R for a in [2 * math.pi * k / 24 for k in range(25)]]
        chain_rod(mb, pts, 0.01, B, seg=4)
    perch_z = zr0 + 0.16
    rod(mb, Vector((c0.x, c0.y, perch_z)) - t * R, Vector((c0.x, c0.y, perch_z)) + t * R, 0.012, M['wood'], seg=6)
    rod(mb, Vector((c0.x, c0.y, zr0 + 0.32)) - rr * R * 0.95, Vector((c0.x, c0.y, zr0 + 0.32)) + rr * R * 0.95, 0.009, M['wood'], seg=6)
    for sg in (-1, 1):
        cup = Vector((c0.x, c0.y, zr0 + 0.02)) + t * sg * (R - 0.06) - rr * 0.08; mb.frustum(cup, cup + Vector((0, 0, 0.06)), 0.035, 0.045, M['cream'], seg=10, cap1=False)
    dr = Vector((c0.x, c0.y, 0)) - rr * R                                               # little door frame on the camera side
    for dz in (zr0 + 0.04, zr0 + 0.26): rod(mb, dr + t * 0.08 + Vector((0, 0, dz)), dr - t * 0.08 + Vector((0, 0, dz)), 0.008, B, seg=4)
    o = _obj(mb, 'canary_cage', SET, hull=0.004); G._parent(o, piv)
    STATE['cage'] = dict(hook=tuple(round(v, 3) for v in hook), perch=tuple(round(v, 3) for v in (c0.x, c0.y, perch_z + 0.012)), floor=tuple(round(v, 3) for v in (c0.x, c0.y, zr0)),
                         radius=R, height=round(hook.z - c0.z, 3), perch_axis=tuple(round(v, 4) for v in t))

# ----------------------------------------------------------------------------- dressing (density pass)
def _pick(mb, M, head, handle_dir, L=1.6, s=1.0):
    head = Vector(head); hd = Vector(handle_dir).normalized(); butt = head + hd * L * s
    rod(mb, head, butt, 0.045 * s, M['wood'], seg=6, r1=0.04 * s)
    side = hd.cross(Vector((0, 0, 1)))
    if side.length < 1e-3: side = Vector((1, 0, 0))
    side.normalize(); up = side.cross(hd).normalized()
    for sg in (-1, 1):
        a = head - hd * 0.02; b = head + side * sg * 0.32 * s - hd * 0.04 * s; c = head + side * sg * 0.55 * s + hd * 0.12 * s
        mb.frustum(a, b, 0.055 * s, 0.04 * s, M['iron'], seg=5); mb.frustum(b, c, 0.04 * s, 0.008 * s, M['iron'], seg=5)

def _shovel(mb, M, blade_tip, handle_dir, L=1.5, s=1.0):
    tip = Vector(blade_tip); hd = Vector(handle_dir).normalized(); side = hd.cross(Vector((0, 0, 1)))
    if side.length < 1e-3: side = Vector((1, 0, 0))
    side.normalize(); nrm = side.cross(hd).normalized()
    neck = tip + hd * 0.55 * s; w = 0.24 * s
    mb.oface([tip - side * w, tip + side * w, neck + side * w * 0.9 + nrm * 0.03, neck - side * w * 0.9 + nrm * 0.03], M['steel'], [(0, 0)] * 4, nrm)
    mb.oface([tip - side * w, tip + side * w, neck + side * w * 0.9 + nrm * 0.03, neck - side * w * 0.9 + nrm * 0.03], M['steel'], [(0, 0)] * 4, -nrm)
    rod(mb, neck, neck + hd * L * s, 0.04 * s, M['wood'], seg=6)
    gp = neck + hd * (L * s + 0.12 * s)
    rod(mb, gp - side * 0.09 * s, gp + side * 0.09 * s, 0.025 * s, M['wood'], seg=5)
    for sg in (-1, 1): rod(mb, neck + hd * L * s + side * sg * 0.02, gp + side * sg * 0.09 * s, 0.022 * s, M['wood'], seg=4)

def _tunnel_dressing(SET, M):
    """Picks and shovels, tools on the props, the timber stack, stone-dust sacks, water barrel, snap tins, jackets, the deputy's
    board, fire buckets at the pit bottom, a refuge hole, puddles, chalk marks, signs, the coal heap at the face, wedges, a sledge."""
    mb = MB(); sg = MB(); pd = MB(); r = _rnd(31); Z = Vector((0, 0, 1))
    def lean(y, s, side, tool, k=0):
        rr = right(y); t = tangent(y); foot = TP(y, s, 0.02); d = (rr * side * 0.22 + Z).normalized(); d = (d + t * r.uniform(-0.15, 0.15)).normalized()
        if tool == 'pick': _pick(mb, M, foot + Z * 0.05 + rr * side * 0.02, d, 1.55)
        else: _shovel(mb, M, foot, d, 1.4)
    lean(4.6, -2.1, -1, 'pick'); lean(5.1, -2.15, -1, 'shovel'); lean(9.9, 2.15, 1, 'shovel'); lean(23.9, 2.1, 1, 'pick'); lean(29.0, -2.15, -1, 'shovel')
    lean(36.4, 2.1, 1, 'pick'); lean(37.0, 2.1, 1, 'shovel'); lean(-1.2, -3.3, -1, 'shovel'); lean(-1.6, -3.3, -1, 'pick')
    _pick(mb, M, TP(39.6, 0.9, 1.5), (tangent(39.6) * -1 + Z * 0.15).normalized(), 1.55)        # a pick stuck in the face
    _pick(mb, M, TP(7.2, -0.6, 0.06), (tangent(7.2) * 0.9 + right(7.2) * 0.4 + Z * 0.04).normalized(), 1.5)   # one on the floor (low cam fg)
    _shovel(mb, M, TP(38.3, -0.4, 0.5), (tangent(38.3) * -0.6 + Z * 0.8).normalized(), 1.35)      # in the coal heap
    # tools hung on the leg of set 4 (y 11.25): a saw, a hand pick, a coil of rope
    y = 11.25; lg = TP(y, -LEG_S + 0.15, 2.6); rr = right(y); t = tangent(y)
    rod(mb, lg, lg + rr * 0.2, 0.015, M['iron'], seg=4); _pick(mb, M, lg + rr * 0.2 - Z * 0.05, -Z, 0.9, 0.7)
    for k in range(8):
        a = 2 * math.pi * k / 8; mb.frustum(TP(y, -LEG_S + 0.25, 1.9) + t * 0.22 * math.cos(a) + Z * 0.22 * math.sin(a), TP(y, -LEG_S + 0.25, 1.9) + t * 0.22 * math.cos(a + 0.8) + Z * 0.22 * math.sin(a + 0.8), 0.04, 0.04, M['rope'], seg=5)
    # jacket and snap tin on nails (set 2 left, set 9 right)
    for (yy, s, sd) in ((6.25, -LEG_S + 0.2, -1), (23.75, LEG_S - 0.2, 1)):
        j = TP(yy, s, 2.9); t = tangent(yy); rr = right(yy)
        mb.oface([j - t * 0.25 + rr * -sd * 0.02, j + t * 0.25, j + t * 0.38 - Z * 0.95, j - t * 0.38 - Z * 0.95], M['cloth'] if sd < 0 else M['cloth2'], [(0, 0)] * 4, -rr * sd)
        mb.oface([j - t * 0.25, j + t * 0.25, j + t * 0.38 - Z * 0.95, j - t * 0.38 - Z * 0.95], M['cloth'] if sd < 0 else M['cloth2'], [(0, 0)] * 4, rr * sd)
        tn = TP(yy + 0.5, s - sd * 0.1, 1.6); obox(mb, tn, t, rr, Z, 0.17, 0.08, 0.11, M['tin'])
        mb.frustum(TP(yy + 0.9, s - sd * 0.1, 1.45), TP(yy + 0.9, s - sd * 0.1, 1.82), 0.09, 0.09, M['tin'], seg=10); rod(mb, TP(yy + 0.9, s - sd * 0.1, 1.82), TP(yy + 0.9, s - sd * 0.1, 1.9), 0.03, M['brass'], seg=6)
    # timber stack (spare props) on the left at y 27..31
    for k in range(9):
        row = k // 4; i = k % 4; y0 = 27.0 + r.uniform(-0.2, 0.2); s0 = -1.95 + 0.0 * i + 0.0
        a = TP(27.2, -2.15 + 0.0 * row, 0.17 + 0.3 * row) + right(27.2) * (0.33 * i + 0.15 * row) * 0.0
        p0 = TP(27.2 + r.uniform(-0.2, 0.1), -2.25 + 0.34 * (i % 3 if row else i) * 0.55 + 0.1 * row, 0.17 + 0.3 * row)
        p1 = TP(30.6 + r.uniform(-0.2, 0.3), -2.2 + 0.34 * (i % 3 if row else i) * 0.55 + 0.1 * row, 0.17 + 0.3 * row)
        rod(mb, p0, p1, 0.16, M['timber'], seg=8, uv=(1.0, 1.7))
    # stone-dust sacks and the water barrel at y 9..10.5 left; the deputy's board
    for k in range(5):
        c = TP(9.3 + 0.55 * (k % 3), -1.95 + 0.0, 0.3 + 0.5 * (k // 3)); lumpy(mb, c, 0.33, M['sack'] if k % 2 else M['sack_d'], 60 + k, seg=10, rings=6, rough=0.12, squash=0.65)
    bc = TP(32.2, 1.9, 0.0); mb.frustum(bc, bc + Z * 1.2, 0.42, 0.46, M['wood_d'], seg=14, cap1=False)
    for z in (0.15, 0.6, 1.05): mb.frustum(bc + Z * z, bc + Z * (z + 0.07), 0.45, 0.47, M['iron'], seg=14, cap0=False, cap1=False)
    pd.frustum(bc + Z * 1.1, bc + Z * 1.1, 0.42, 0.0, M['wet'], seg=14)
    for (yy, s, nm, w, h) in ((2.2, -2.42, 'sign_danger', 1.6, 0.7), (18.4, -2.4, 'sign_heading', 1.6, 0.45)):
        t = tangent(yy); rr = right(yy); c = TP(yy, s, 2.75)
        mb.oface([c - t * w / 2, c + t * w / 2, c + t * w / 2 + Z * h, c - t * w / 2 + Z * h], M[nm], [(0, 0), (1, 0), (1, 1), (0, 1)], rr)
    # fire buckets on a rack and a bench at the pit bottom; sign over the shaft gates
    for k in range(4):
        c = Vector((3.2, -3.0 - 0.6 * k, 1.7)); mb.frustum(c, c + Z * 0.42, 0.16, 0.21, M['red'], seg=12, cap1=False); rod(mb, c + Z * 0.42 + Vector((0.0, -0.2, 0)), c + Z * 0.42 + Vector((0.0, 0.2, 0)), 0.012, M['iron'], seg=4)
    mb.box((3.3, -5.4, 1.62), (3.6, -2.5, 1.7), M['wood_d'])
    mb.box((-3.5, -8.6, 0.85), (-2.6, -4.6, 0.95), M['wood']); [mb.box((-3.45, y_ - 0.06, 0), (-2.65, y_ + 0.06, 0.85), M['wood_d']) for y_ in (-8.3, -4.9)]
    mb.oface([(-1.4, PB_Y0 + 0.02, 4.75), (1.4, PB_Y0 + 0.02, 4.75), (1.4, PB_Y0 + 0.02, 5.75), (-1.4, PB_Y0 + 0.02, 5.75)], M['sign_pit'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 1, 0))
    mb.box((-3.55, -1.3, 2.3), (-3.3, -0.7, 2.9), M['wood_d']); rod(mb, (-3.3, -1.0, 2.75), (-3.0, -1.0, 2.2), 0.03, M['iron'], seg=5)   # signal rapper box
    # coal heap at the face, loose lumps along the floor, wedges, a sledge hammer
    lumpy(mb, TP(38.9, -0.6, 0.0), 1.35, M['lumps'], 77, seg=14, rings=7, rough=0.3, squash=0.5)
    lumpy(mb, TP(39.0, 1.6, 0.0), 0.9, M['lumps'], 78, seg=12, rings=6, rough=0.3, squash=0.5)
    for k in range(60):
        y = r.uniform(1, 39); s = r.choice((-1, 1)) * r.uniform(1.6, 2.3) if r.random() < 0.7 else r.uniform(-1.5, -0.4)
        lumpy(mb, TP(y, s, 0.03), r.uniform(0.06, 0.16), M['lumps'], 200 + k, seg=6, rings=4, rough=0.4, squash=0.8)
    sh = TP(25.2, -0.9, 0.05); rod(mb, sh, sh + tangent(25.2) * 1.2 + right(25.2) * 0.3, 0.04, M['wood'], seg=6); obox(mb, sh, tangent(25.2), right(25.2), Z, 0.08, 0.16, 0.08, M['iron'])
    # refuge hole (manhole) in the right wall at y 24.8: whitewashed recess
    y = 24.8; t = tangent(y); rr = right(y); c = TP(y, WALL_HW - 0.05, 0.0)
    for (a, b, n) in ((c - t * 0.8, c - t * 0.8 + rr * 0.6, t), (c + t * 0.8 + rr * 0.6, c + t * 0.8, -t)):
        mb.oface([a, b, b + Z * 2.4, a + Z * 2.4], M['white'], [(0, 0), (0.15, 0), (0.15, 0.6), (0, 0.6)], n)
    mb.oface([c - t * 0.8 + rr * 0.6, c + t * 0.8 + rr * 0.6, c + t * 0.8 + rr * 0.6 + Z * 2.4, c - t * 0.8 + rr * 0.6 + Z * 2.4], M['white'], [(0, 0), (0.4, 0), (0.4, 0.6), (0, 0.6)], -rr)
    mb.oface([c - t * 0.8 + Z * 2.4, c + t * 0.8 + Z * 2.4, c + t * 0.8 + rr * 0.6 + Z * 2.4, c - t * 0.8 + rr * 0.6 + Z * 2.4], M['white'], [(0, 0)] * 4, -Z)
    beam(mb, c - t * 0.95 + Z * 2.5 - rr * 0.05, c + t * 0.95 + Z * 2.5 - rr * 0.05, 0.25, 0.25, M['timber_d'])
    _obj(mb, 'dressing', SET, hull=0.012)
    # puddles: glossy dark water (reflect the flames); wet sheen strips under the drips
    for k, (y, s, rx, ry) in enumerate(((3.4, -1.2, 0.9, 0.5), (7.6, -1.6, 0.7, 0.35), (10.8, 0.1, 0.55, 0.3), (19.2, -1.0, 1.1, 0.55), (22.3, 0.6, 0.6, 0.35),
                                       (27.8, -0.3, 0.9, 0.45), (31.4, -1.4, 0.7, 0.4), (36.0, -0.6, 0.8, 0.4), (-2.6, 2.2, 0.8, 0.5), (1.2, 0.2, 0.5, 0.3))):
        t = tangent(y); rr = right(y); c = TP(y, s, 0.012); n = 18
        pts = [c + t * rx * math.cos(2 * math.pi * i / n) * (1 + 0.18 * math.sin(3 * i + k)) + rr * ry * math.sin(2 * math.pi * i / n) * (1 + 0.15 * math.cos(2 * i + k)) for i in range(n)]
        pd.face(pts, M['puddle'])
    po = _obj(pd, 'puddles', SET)

def _drips(SET, M):
    """Hanging drops under the bars and the roof, and 8 falling drops (set_drips animates them)."""
    mb = MB(); r = _rnd(37); STATE['drops'] = []
    for k in range(26):
        y = r.uniform(1, 39); s = r.uniform(-1.8, 1.8); c = TP(y, s, CAP_Z - 0.03 if r.random() < 0.6 else CAP_Z + CAP_T + 0.45)
        mb.frustum(c, c - Vector((0, 0, 0.06)), 0.012, 0.03, M['wet'], seg=6, cap0=False); mb.sphere(c - Vector((0, 0, 0.075)), 0.03, M['wet'], seg=6, rings=4)
    _obj(mb, 'drops_hanging', SET, shadow=False)
    for k in range(8):
        y = r.uniform(2, 38); s = r.uniform(-1.6, 1.6); c = TP(y, s, CAP_Z - 0.1)
        dm = MB(); dm.sphere((0, 0, 0), 0.028, M['wet'], seg=6, rings=4); dm.frustum((0, 0, 0.0), (0, 0, 0.14), 0.026, 0.0, M['wet'], seg=6)
        o = _obj(dm, 'drop_%d' % k, SET, shadow=False); o.location = c
        STATE['drops'].append(dict(ob=o, top=tuple(c), period=r.uniform(18, 34), phase=r.uniform(0, 1)))

# ----------------------------------------------------------------------------- gas and blast
def _gas_build(SET, M):
    """13 camera-only additive slabs across the roadway (y 2..38) and 2 in the heading; strength from set_gas."""
    mat = _mat_gas(STATE['pre'] + 'gas', (0.72, 0.78, 0.92)); mb = MB()
    for k in range(7):
        y = 3.0 + k * 5.6; rr = right(y)
        mb.face([TP(y, -2.7, 0.0), TP(y, 2.7, 0.0), TP(y, 2.7, 5.1), TP(y, -2.7, 5.1)], mat)
    HP = STATE['HP']; mb.face([HP(5.0, -1.9, 0), HP(5.0, 1.9, 0), HP(5.0, 1.9, 3.9), HP(5.0, -1.9, 3.9)], mat)
    o = _obj(mb, 'gas_haze', SET, shadow=False); STATE['gas_mat'] = mat; STATE['gas_obj'] = o

N_FIRE = 40; N_SMOKE = 14; N_DEBRIS = 40; N_DUST = 10
def _blast_build(SET, M):
    pre = STATE['pre']
    smoke = _untoon(mat_lit(pre + 'smoke', '#3a3644', form=(0, 0, 0.2))); fire = _mat_fire(pre + 'fire', core=(1.0, 0.8, 0.36), edge=(0.95, 0.2, 0.03), k_core=1.7, k_edge=0.55)
    fire2 = _mat_fire(pre + 'fire2', core=(1.0, 0.5, 0.12), edge=(0.7, 0.12, 0.03), k_core=1.1, k_edge=0.35); ember = mat_emit(pre + 'e_ember', '#ffb050', strength=6.0)
    dust = _mat_puff(pre + 'dust', STATE['tx']['puff'], (0.30, 0.27, 0.30), 1.0, 0.45)
    r = _rnd(41); STATE['blast'] = []; objs = []
    for k in range(N_FIRE + N_SMOKE):
        mb = MB(); kind = 'fire' if k < N_FIRE else 'smoke'; lag = (k + 0.5) / N_FIRE if kind == 'fire' else r.uniform(0.2, 1.0)
        lumpy(mb, (0, 0, 0), 1.0, (fire if lag < 0.5 else fire2) if kind == 'fire' else smoke, 500 + k, seg=16, rings=10, rough=0.28)
        o = mb.obj('blast_%s_%02d' % (kind, k), SET, smooth=True); o.visible_shadow = False; no_bounce(o)
        STATE['blast'].append(dict(ob=o, kind=kind, s=r.uniform(-2.1, 2.1), z=r.uniform(0.8, 4.2), lag=lag, rad=r.uniform(1.0, 1.8), seed=k)); objs.append(o)
    for k in range(N_DEBRIS):
        mb = MB(); kind = r.choice(('coal', 'coal', 'timber', 'ember'))
        if kind == 'coal': lumpy(mb, (0, 0, 0), r.uniform(0.07, 0.17), M['lumps'], 700 + k, seg=6, rings=4, rough=0.5)
        elif kind == 'timber': obox(mb, (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), r.uniform(0.2, 0.45), 0.04, 0.03, M['timber'])
        else: mb.sphere((0, 0, 0), 0.03, ember, seg=6, rings=4)
        o = _obj(mb, 'blast_debris_%02d' % k, SET, shadow=False)
        STATE['blast'].append(dict(ob=o, kind='debris', s=r.uniform(-2.2, 2.2), z=r.uniform(0.3, 4.4), lag=r.uniform(0, 1), v=r.uniform(1.0, 1.8), spin=r.uniform(4, 12), seed=k, dz=r.uniform(-0.6, 0.6))); objs.append(o)
    for k in range(N_DUST):
        mb = MB(); mb.face([(-1, 0, -1), (1, 0, -1), (1, 0, 1), (-1, 0, 1)], dust, [(0, 0), (1, 0), (1, 1), (0, 1)])
        o = _obj(mb, 'blast_dust_%02d' % k, SET, shadow=False)
        STATE['blast'].append(dict(ob=o, kind='dust', s=r.uniform(-2.0, 2.0), z=r.uniform(0.4, 3.8), lag=r.uniform(0, 1), rad=r.uniform(1.0, 2.0), seed=k)); objs.append(o)
    STATE['blast_objs'] = objs
    STATE['blast_light'] = _light('blast_flash', TP(TUN_L, 0, 2.5), (1.0, 0.55, 0.25), 0.0, radius=0.8)
    STATE['blast_light2'] = _light('blast_glow', TP(TUN_L, 0, 2.5), (1.0, 0.4, 0.15), 0.0, radius=1.2)

def blast_front(u):
    """Station y of the fireball's front at u (0..1): from the face (y 40) to y 1.0 by u 1, accelerating then steady."""
    e = 1 - (1 - min(1.0, max(0.0, u))) ** 1.6
    return TUN_L - (TUN_L - 1.0) * e

def set_blast(u, frame=None):
    """Explosion control 0..1. u 0: nothing. The fireball forms at the face (y 40) and races down the roadway toward the pit bottom
    (front at blast_front(u), y 1 at u 1); the burning tail grows to 14 D, smoke rolls behind it; debris (coal lumps, splinters,
    embers) and dust fly ahead of the front; the flash light rides the front (energy keyed). With frame: everything keyed
    (location / scale / rotation linear, visibility constant); call per frame."""
    u = max(0.0, min(1.0, float(u))); on = u > 1e-4; yF = blast_front(u); tail = 2.0 + 12.0 * min(1.0, u * 1.6)
    grow = min(1.0, u / 0.12)                                                        # first 12 %: the ball blooms at the face
    for b in STATE['blast']:
        o = b['ob']; k = b['seed']
        if b['kind'] in ('fire', 'smoke'):
            back = b['lag'] * tail + (3.0 if b['kind'] == 'smoke' else 0.0); y = min(TUN_L - 0.3, yF + back)
            near = 1.0 - b['lag']                                                      # front blobs bigger
            rad = b['rad'] * (0.55 + 0.75 * near) * grow * (1.0 + 0.15 * math.sin(7 * u + k))
            sq = max(0.15, 1.0 - 0.35 * b['lag'])
            lim = 2.3 - 0.3 * rad
            s = max(-lim, min(lim, b['s'] * (0.6 + 0.5 * grow))); z = max(0.6, min(4.4, b['z'] + 0.6 * b['lag'] * (b['kind'] == 'smoke')))
            o.location = TP(y, s, z); o.scale = (rad, rad * (1.2 + 0.4 * near), rad * sq) if b['kind'] == 'fire' else (rad * 1.1, rad * 1.1, rad * 0.8)
            o.rotation_euler = (0.0, 0.0, math.atan2(tangent(y).x, tangent(y).y) + 0.6 * k + 3.0 * u)
            vis = on and (b['kind'] == 'fire' or u > 0.08)
        elif b['kind'] == 'debris':
            lead = (0.4 + 2.6 * b['lag']) * b['v'] * min(1.0, u / 0.15); y = max(-1.0, yF - lead)
            fall = max(0.0, b['z'] - 0.9 * lead * lead * 0.05); z = max(0.08, b['z'] + b['dz'] * lead * 0.25 - 0.08 * lead * lead)
            o.location = TP(y, b['s'] * (0.7 + 0.1 * lead), z); o.rotation_euler = (b['spin'] * u + k, b['spin'] * 0.7 * u, b['spin'] * 1.3 * u + k * 0.3)
            o.scale = (1, 1, 1); vis = on and u > 0.04
        else:
            lead = 0.3 + 1.2 * b['lag']; y = max(-0.5, yF - lead); rad = b['rad'] * (0.5 + 1.0 * min(1.0, u * 2.0))
            o.location = TP(y, b['s'], b['z']); t = tangent(y); o.rotation_euler = (0.0, 0.0, math.atan2(t.x, t.y) * -1.0 + 0.0); o.scale = (rad, 1, rad)
            vis = on and u > 0.06
        o.hide_render = not vis; o.hide_viewport = False
        if frame is not None:
            T._key(o, 'location', frame, 'LINEAR'); T._key(o, 'scale', frame, 'LINEAR'); T._key(o, 'rotation_euler', frame, 'LINEAR'); T._key(o, 'hide_render', frame)
    L1, L2 = STATE['blast_light'], STATE['blast_light2']
    flick = 1.0 + 0.18 * math.sin(37.0 * u) + 0.1 * math.sin(91.0 * u)
    L1.location = TP(max(0.5, yF - 0.6), 0.0, 2.4); L1.data.energy = (4500.0 * grow * flick) if on else 0.0
    L2.location = TP(min(TUN_L - 0.5, yF + tail * 0.5), 0.0, 2.6); L2.data.energy = (2500.0 * grow) if on else 0.0; L2.data.use_shadow = False
    STATE['blast_u'] = u
    if frame is not None:
        for L in (L1, L2): T._key(L, 'location', frame, 'LINEAR'); T._key(L.data, 'energy', frame, 'LINEAR')

def set_gas(density, frame=None):
    """Firedamp haze 0..1 (very faint layered veil under the roof, strongest toward the face). 1.0 = the day the bird stops."""
    m = STATE.get('gas_mat')
    if m is None: return
    v = m.node_tree.nodes['gas_k'].outputs[0]; v.default_value = 0.06 * max(0.0, float(density)); STATE['gas'] = density
    T._show([STATE['gas_obj']], density > 1e-4, frame)                              # the slabs cost transparent hits: hidden at 0
    if frame is not None:
        v.keyframe_insert('default_value', frame=frame)
        for fc in T._fcurves(m.node_tree):
            for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'

def set_flame(k, frame=None):
    """Flame of the foreman's lamp (lamp_insert): 0 out, 1 normal, up to 2 = tall flame with a pale cap (gas). Scales the flame mesh
    about its wick, its emission and its light."""
    k = max(0.0, float(k)); piv = STATE.get('flame_pivot')
    if piv is None: return
    piv.scale = (max(0.001, min(1.0, k)) * (1 + 0.15 * max(0, k - 1)), max(0.001, min(1.0, k)) * (1 + 0.15 * max(0, k - 1)), max(0.001, k))
    pre = STATE['pre']; mats = [bpy.data.materials[pre + 'e_flame_ins'], bpy.data.materials[pre + 'e_flamec_ins']]
    for m, base in zip(mats, (7.0, 11.0)):
        s = m.node_tree.nodes['strength'].inputs['Strength']; s.default_value = base * min(1.0, k) * (1 + 0.3 * max(0, k - 1))
        if frame is not None: s.keyframe_insert('default_value', frame=frame)
    L = STATE['insert_light']; L.data.energy = LAMP_E * 0.9 * STATE['P']['lamp_k'] * min(1.4, k)
    if frame is not None: T._key(piv, 'scale', frame, 'LINEAR'); T._key(L.data, 'energy', frame, 'LINEAR')

def set_cage(pos=None, frame=None, swing=0.0):
    """Move the canary cage: pos = world point of its hanging ring (the boy's hand), None = back on its nail (CAGE_HOOK).
    swing: tilt about the tunnel axis in degrees (carried at a run). Keyed with frame."""
    piv = STATE['cage_pivot']; piv.location = TP(*CAGE_HOOK) if pos is None else Vector(pos)
    piv.rotation_euler = (math.radians(swing), 0.0, 0.0)
    if frame is not None: T._key(piv, 'location', frame, 'LINEAR'); T._key(piv, 'rotation_euler', frame, 'LINEAR')

def set_drips(frame=None):
    """Falling drops: each falls from the roof to the floor on its own period (frames); frame None leaves them mid-fall."""
    for d in STATE.get('drops', []):
        top = Vector(d['top']); f = 0.5 if frame is None else ((frame / d['period']) + d['phase']) % 1.0
        z = top.z - top.z * min(1.0, (f / 0.35) ** 2) if f < 0.35 else top.z
        d['ob'].location = (top.x, top.y, max(0.02, z)); d['ob'].hide_render = not (f < 0.35)
        if frame is not None: T._key(d['ob'], 'location', frame, 'LINEAR'); T._key(d['ob'], 'hide_render', frame)

def lamp_light(position, strength=1.0, frame=None, name='miner_lamp_0', color=WARM, flicker=0.04):
    """A miner's lamp: a warm point light at `position` (the flame of the actor's lamp prop), energy strength x LAMP_E (about 1.0 x
    the lamp colour on a surface 2 D away), a soft flicker deterministic in the frame. Create once per actor (distinct names) and key
    it every frame. Returns the light object."""
    if 'LIGHTS' not in STATE: STATE['LIGHTS'] = T._coll('LIGHTS', bpy.context.scene)
    L = _light(name, position, color, 0.0, radius=0.04)
    fl = 1.0 + (flicker * (math.sin(1.7 * (frame or 0)) * 0.6 + math.sin(4.3 * (frame or 0) + 1.0) * 0.4) if frame is not None else 0.0)
    L.data.energy = LAMP_E * float(strength) * fl; L.location = position
    if frame is not None: T._key(L, 'location', frame, 'LINEAR'); T._key(L.data, 'energy', frame, 'LINEAR')
    return L

def set_lamps(k, frame=None):
    """Fixed hanging lamps (not the insert lamp, not the pit bottom): 0 out .. 1 normal (flame emission and light)."""
    for L in STATE.get('fixed_lamps', []):
        L.data.energy = LAMP_E * 1.1 * STATE['P']['lamp_k'] * k
        if frame is not None: T._key(L.data, 'energy', frame, 'LINEAR')
    m = bpy.data.materials[STATE['pre'] + 'e_flame']; s = m.node_tree.nodes['strength'].inputs['Strength']; s.default_value = 7.0 * k
    if frame is not None: s.keyframe_insert('default_value', frame=frame)

# ============================================================================= PITHEAD
SHAFT_C = (0.0, 12.0); DECK_Z = 1.4
HUT = (9.0, 14.0, -4.0, 0.0)                                   # first-aid hut x0, x1, y0 (front), y1
BENCH = (10.0, 12.8, -4.75); SEAT_Z = 0.95
OXY = (11.15, -4.75)                                            # the oxygen box sits on the bench seat
PIT_LAMPS = [(3.6, 4.2), (-3.4, -9.0), (9.2, -9.6), (-4.0, 8.4), (4.0, 8.4)]

def _pithead(SET, P, C, TX, E, dress):
    tx = STATE['tx']; pre = STATE['pre']
    M = dict(yard=TX('yard', form=False), brick=TX('brick'), brick_s=TX('brick_soot'), slate=TX('slate'), planks=TX('planks'), hut=TX('hut'), tub=TX('tub'),
             lumps=_glossy(TX('lumps_heap'), (1.0, 0.9, 0.8), 0.5, 0.25), lumps_s=TX('lumps'),
             steel=_glossy(C('#4a3a40', 1.0, 1.0), (1.0, 0.85, 0.7), 0.25, 0.35), steel_r=C('#8a3a2a'), iron=C('#3a3640', 1.0, 1.1), rail=_glossy(C('#6a6670', 1.0, 1.1), (1, 0.9, 0.8), 0.6, 0.2),
             stone=C('#c8b89a'), stone_d=C('#9a8a72'), wood=C('#8a5a36'), wood_d=C('#5a3a26'), timber=TX('timber'), white=C('#ece6d8'), cream=C('#e8dcc0'), green=C('#3a6a4e'),
             red=C('#c03a2a'), black=C('#24222a'), rope=C('#b89a6a'), cable=C('#2a2830'), sack=C('#a89070'),
             brass=_glossy(_metal('brass', '#d4a24a'), (1.0, 0.82, 0.5), 1.1, 0.2), brass_d=_glossy(_metal('brass_d', '#9a6e2c'), (1.0, 0.82, 0.5), 0.6, 0.28),
             oxy=_glossy(TX('oxy_panel'), (1.0, 0.85, 0.55), 0.7, 0.22), cyl=_glossy(C('#2e6a48'), (1, 1, 1), 0.5, 0.15), rubber=C('#3a2a2a', 1.0, 1.1),
             glass=_mat_glass(pre + 'glass'), firstaid=TX('firstaid'), label=TX('pit_label'),
             win=E('win', hexcol='#ffbe6a', k=1.6 * P['lamp_k'] + 0.2), win_d=C('#2e3046'), lamp=E('lamp', hexcol='#ffd890', k=4.5), puddle=_glossy(C('#2a2838', 1.0, 0.8, form=False), (1, 1, 1), 0.9, 0.05))
    STATE['M'] = M
    mb = MB(); mb.quad((-150, -150, 0), (300, 0, 0), (0, 300, 0), M['yard'], (-37.5, -37.5, 37.5, 37.5)); _obj(mb, 'ground', SET)
    _headframe(SET, M); _engine_house(SET, M); _pit_bank(SET, M); _hut(SET, M); _pit_props(SET, M, dress)
    # painted backdrop ring and sky dome
    mb = MB(); R = MT.PANO_R; seg = 128
    for i in range(seg):
        a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; u0, u1 = i / seg, (i + 1) / seg
        mb.face([Vector((R * math.cos(a0), R * math.sin(a0), MT.PANO_Z0)), Vector((R * math.cos(a1), R * math.sin(a1), MT.PANO_Z0)), Vector((R * math.cos(a1), R * math.sin(a1), MT.PANO_Z1)), Vector((R * math.cos(a0), R * math.sin(a0), MT.PANO_Z1))],
                mat_emit(pre + 'e_pano', image=tx['pano_' + P['pano']], strength=P['pano_k'], alpha=True), [(u0, 0), (u1, 0), (u1, 1), (u0, 1)])
    _obj(mb, 'backdrop', SET, shadow=False)
    mb = MB(); R = 140.0; seg = 72; els = [-15 + 105 * k / 14 for k in range(15)]
    for i in range(seg):
        for k in range(14):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; e0, e1 = math.radians(els[k]), math.radians(els[k + 1])
            pts = [Vector((R * math.cos(e) * math.cos(a), R * math.cos(e) * math.sin(a), R * math.sin(e))) for (a, e) in ((a0, e0), (a1, e0), (a1, e1), (a0, e1))]
            uvs = [(i / seg, k / 14), ((i + 1) / seg, k / 14), ((i + 1) / seg, (k + 1) / 14), (i / seg, (k + 1) / 14)]
            mb.face(pts[::-1], E('sky', 'sky_' + P['sky'], k=P['sky_k']), uvs[::-1])
    _obj(mb, 'sky', SET, shadow=False)
    if P.get('haze'):
        hm = G._haze_mat(pre + 'haze', P['haze'][0], P['haze'][1], 0.0, 30.0); mb = MB()
        for Rh in (40.0, 75.0, 110.0):
            for i in range(64):
                a0, a1 = 2 * math.pi * i / 64, 2 * math.pi * (i + 1) / 64; c = Vector((0.0, 0.0, 0))
                mb.face([c + Vector((Rh * math.cos(a0), Rh * math.sin(a0), -1)), c + Vector((Rh * math.cos(a1), Rh * math.sin(a1), -1)), c + Vector((Rh * math.cos(a1), Rh * math.sin(a1), 40)), c + Vector((Rh * math.cos(a0), Rh * math.sin(a0), 40))], hm)
        _obj(mb, 'haze', SET, shadow=False)

def _lattice(mb, a0, a1, b0, b1, n, w, wb, M):
    """Two legs (a0->a1, b0->b1) joined by n bays of horizontal girders and X bracing."""
    a0, a1, b0, b1 = map(Vector, (a0, a1, b0, b1))
    for k in range(n + 1):
        t = k / n; pa, pb = a0.lerp(a1, t), b0.lerp(b1, t); beam(mb, pa, pb, wb, wb * 1.3, M['steel'])
        if k < n:
            qa, qb = a0.lerp(a1, (k + 1) / n), b0.lerp(b1, (k + 1) / n)
            beam(mb, pa, qb, wb * 0.6, wb * 0.6, M['steel']); beam(mb, pb, qa, wb * 0.6, wb * 0.6, M['steel'])

def _wheel(mb, c, R, M, axis=(0, 1, 0), spokes=12):
    """Spoked headframe pulley (sheave) turning in the plane normal to `axis`: rim with a groove, spokes, hub."""
    c = Vector(c); ax = Vector(axis).normalized(); u = ax.cross(Vector((0, 0, 1))).normalized() if abs(ax.z) < 0.9 else Vector((1, 0, 0)); v = ax.cross(u)
    n = 40
    for k in range(n):
        a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
        p0 = c + (u * math.cos(a0) + v * math.sin(a0)) * R; p1 = c + (u * math.cos(a1) + v * math.sin(a1)) * R
        for (dd, rr_) in ((0.13, 0.0), (-0.13, 0.0)): mb.frustum(p0 + ax * dd, p1 + ax * dd, 0.08, 0.08, M['steel_r'], seg=5, cap0=False, cap1=False)
        mb.frustum(p0, p1, 0.06, 0.06, M['steel'], seg=5, cap0=False, cap1=False)
    for k in range(spokes):
        a = 2 * math.pi * k / spokes; d = u * math.cos(a) + v * math.sin(a)
        mb.frustum(c + d * 0.25, c + d * (R - 0.05), 0.055, 0.04, M['steel_r'], seg=5)
    mb.frustum(c - ax * 0.32, c + ax * 0.32, 0.26, 0.26, M['steel'], seg=12); mb.frustum(c - ax * 0.6, c + ax * 0.6, 0.08, 0.08, M['iron'], seg=8)

def _headframe(SET, M):
    """Steel lattice headframe over the shaft: four legs tapering to the sheave platform (z 21), two spoked wheels (R 2.3) turning in
    x-z planes at y 11.1 and 12.9, back-legs raking to the west (toward the engine house), ropes to the drum and down the shaft."""
    mb = MB(); X0, Y0 = SHAFT_C; zt = 21.0
    B = {(sx, sy): Vector((X0 + sx * 3.3, Y0 + sy * 2.5, 0)) for sx in (-1, 1) for sy in (-1, 1)}
    Tp = {(sx, sy): Vector((X0 + sx * 1.6, Y0 + sy * 1.4, zt)) for sx in (-1, 1) for sy in (-1, 1)}
    for k in B: beam(mb, B[k], Tp[k], 0.42, 0.42, M['steel'])
    for (k1, k2) in (((-1, -1), (1, -1)), ((1, -1), (1, 1)), ((1, 1), (-1, 1)), ((-1, 1), (-1, -1))):
        _lattice(mb, B[k1] + Vector((0, 0, 1.2)), Tp[k1], B[k2] + Vector((0, 0, 1.2)), Tp[k2], 6, 0.3, 0.2, M)
    for sy in (-1, 1):                                                              # back-legs
        foot = Vector((X0 - 7.6, Y0 + sy * 3.0, 0)); top = Vector((X0 - 1.5, Y0 + sy * 1.3, zt - 0.4)); beam(mb, foot, top, 0.48, 0.48, M['steel'])
        for k in range(1, 5):
            p = foot.lerp(top, k / 5); q = Vector((X0 - 1.6 + 0.0, Y0 + sy * 1.4, 0)).lerp(Tp[(-1, sy)], k / 5); beam(mb, p, q, 0.18, 0.18, M['steel'])
        mb.box((foot.x - 0.7, foot.y - 0.7, 0), (foot.x + 0.7, foot.y + 0.7, 0.5), M['stone'])
    for k in B: mb.box((B[k].x - 0.7, B[k].y - 0.7, 0), (B[k].x + 0.7, B[k].y + 0.7, 0.6), M['stone'])
    mb.box((X0 - 2.4, Y0 - 2.1, zt), (X0 + 2.4, Y0 + 2.1, zt + 0.25), M['steel'])                    # platform + railing
    for sx in (-1, 1):
        for sy in (-1, 1): rod(mb, (X0 + sx * 2.3, Y0 + sy * 2.0, zt + 0.25), (X0 + sx * 2.3, Y0 + sy * 2.0, zt + 1.3), 0.05, M['steel'], seg=4)
    for z in (zt + 0.8, zt + 1.3):
        for (a, b) in (((-2.3, -2.0), (2.3, -2.0)), ((2.3, -2.0), (2.3, 2.0)), ((2.3, 2.0), (-2.3, 2.0)), ((-2.3, 2.0), (-2.3, -2.0))):
            rod(mb, (X0 + a[0], Y0 + a[1], z), (X0 + b[0], Y0 + b[1], z), 0.04, M['steel'], seg=4)
    for sy in (-1, 1):                                                              # wheel bearings
        mb.box((X0 - 0.5, Y0 + sy * 0.9 - 0.15, zt + 0.25), (X0 + 0.5, Y0 + sy * 0.9 + 0.15, zt + 2.6), M['steel'])
    _obj(mb, 'headframe', SET, hull=0.04)
    wb = MB(); STATE['wheels'] = []
    for sy in (-1, 1):
        c = (X0, Y0 + sy * 0.9, zt + 2.6); _wheel(wb, c, 2.3, M, axis=(0, 1, 0)); STATE['wheels'].append(c)
    _obj(wb, 'sheaves', SET, hull=0.025)
    rp = MB()                                                                        # ropes: down the shaft from the wheels' east side, to the drum (west)
    for sy in (-1, 1):
        rod(rp, (X0 + 2.3, Y0 + sy * 0.9, zt + 2.6), (X0 + 2.3 - 2.3 + 0.9 * sy, Y0 + sy * 0.9 - 0.2, DECK_Z + 4.2), 0.05, M['cable'], seg=5)
        rod(rp, (X0 - 1.6, Y0 + sy * 0.9, zt + 4.4), (-11.0, Y0 + sy * 0.5, 8.6), 0.05, M['cable'], seg=5)
    _obj(rp, 'ropes', SET, shadow=False)

def _engine_house(SET, M):
    """Brick winding-engine house to the west (x -19..-9, y 5..19): tall round-arched windows (lit), stone dressings, slate roof, the
    rope holes; the tall boiler chimney (z 34) behind it at (-21, 24) with a smoke plume; a lower boiler house."""
    mb = MB(); win = MB(); x0, x1, y0, y1, H = -19.0, -9.0, 5.0, 19.0, 11.0
    for (p0, pu, nrm, L_) in (((x0, y0, 0), (x1 - x0, 0, 0), (0, -1, 0), x1 - x0), ((x1, y0, 0), (0, y1 - y0, 0), (1, 0, 0), y1 - y0), ((x1, y1, 0), (x0 - x1, 0, 0), (0, 1, 0), x1 - x0), ((x0, y1, 0), (0, y0 - y1, 0), (-1, 0, 0), y1 - y0)):
        p0 = Vector(p0); pu = Vector(pu)
        mb.oface([p0, p0 + pu, p0 + pu + Vector((0, 0, H)), p0 + Vector((0, 0, H))], M['brick'], [(0, 0), (L_ / 2, 0), (L_ / 2, H / 1.92), (0, H / 1.92)], nrm)
    for (a, b) in (((x0, y0), (x1, y0)), ((x1, y1), (x0, y1))):                         # gables (south and north ends), slate roof (ridge along x)
        pass
    rz = H + 4.0; ym = (y0 + y1) / 2
    for (ya, sgn) in ((y0, -1), (y1, 1)):
        mb.oface([(x0 - 0.4, ya + sgn * 0.5, H - 0.2), (x1 + 0.4, ya + sgn * 0.5, H - 0.2), (x1 + 0.4, ym, rz), (x0 - 0.4, ym, rz)], M['slate'], [(0, 0), (5.4, 0), (5.4, 4.3), (0, 4.3)], (0, sgn, 1))
    for xa in (x0, x1):
        mb.oface([(xa, y0, H), (xa, y1, H), (xa, ym, rz - 0.1)], M['brick'], [(0, 0), (7, 0), (3.5, 2)], (1 if xa == x1 else -1, 0, 0))
    mb.box((x0 - 0.2, y0 - 0.2, 0), (x1 + 0.2, y1 + 0.2, 0.9), M['stone_d'], skip='bottom')
    mb.box((x0 - 0.3, y0 - 0.3, H - 0.4), (x1 + 0.3, y1 + 0.3, H - 0.1), M['stone'], skip='bottom')
    rod(mb, (x0 - 0.3, ym, rz + 0.1), (x1 + 0.3, ym, rz + 0.1), 0.15, M['stone_d'], seg=6)
    # east face (toward the headframe): three tall arched windows, rope holes; south face: two windows and the door
    def arch_window(face_x=None, face_y=None, c=0.0, w=1.6, z0=2.0, z1=7.4, n=None):
        segs = 8; pts = [(c - w / 2, z0), (c + w / 2, z0)] + [(c + w / 2 * math.cos(math.pi * k / segs), z1 + w / 2 * math.sin(math.pi * k / segs)) for k in range(segs + 1)]
        if face_x is not None: P3 = [Vector((face_x + 0.03, p[0], p[1])) for p in pts]; nr = (1, 0, 0)
        else: P3 = [Vector((p[0], face_y - 0.03, p[1])) for p in pts]; nr = (0, -1, 0)
        win.oface(P3, M['win'], [(0, 0)] * len(P3), nr)
        for k in range(len(P3)):
            a, b = P3[k], P3[(k + 1) % len(P3)]; mb.frustum(a, b, 0.14, 0.14, M['stone'], seg=4)
        if face_x is not None:
            for z in (z0 + 1.8, z0 + 3.6): rod(mb, (face_x + 0.06, c - w / 2, z), (face_x + 0.06, c + w / 2, z), 0.035, M['black'], seg=4)
            rod(mb, (face_x + 0.06, c, z0), (face_x + 0.06, c, z1 + w / 2), 0.035, M['black'], seg=4)
        else:
            for z in (z0 + 1.8, z0 + 3.6): rod(mb, (c - w / 2, face_y - 0.06, z), (c + w / 2, face_y - 0.06, z), 0.035, M['black'], seg=4)
            rod(mb, (c, face_y - 0.06, z0), (c, face_y - 0.06, z1 + w / 2), 0.035, M['black'], seg=4)
    for c in (8.0, 12.0, 16.0): arch_window(face_x=x1, c=c)
    for c in (-16.5, -11.5): arch_window(face_y=y0, c=c)
    mb.oface([(-14.6, y0 - 0.04, 0.9), (-13.2, y0 - 0.04, 0.9), (-13.2, y0 - 0.04, 3.6), (-14.6, y0 - 0.04, 3.6)], M['wood_d'], [(0, 0)] * 4, (0, -1, 0))
    for sy in (-1, 1): mb.oface([(x1 + 0.04, 12 + sy * 0.5 - 0.4, 8.2), (x1 + 0.04, 12 + sy * 0.5 + 0.4, 8.2), (x1 + 0.04, 12 + sy * 0.5 + 0.4, 9.0), (x1 + 0.04, 12 + sy * 0.5 - 0.4, 9.0)], M['black'], [(0, 0)] * 4, (1, 0, 0))
    lb = (x1 + 0.05, 12.0, 9.9); mb.oface([(lb[0], lb[1] - 1.5, lb[2] - 0.35), (lb[0], lb[1] + 1.5, lb[2] - 0.35), (lb[0], lb[1] + 1.5, lb[2] + 0.35), (lb[0], lb[1] - 1.5, lb[2] + 0.35)], M['label'], [(0, 0), (1, 0), (1, 1), (0, 1)], (1, 0, 0))
    # boiler house (lower, south-west) and the chimney
    bx0, bx1, by0, by1, bh = -27.0, -19.0, 14.0, 24.0, 6.0
    for (p0, pu, nrm, L_) in (((bx0, by0, 0), (bx1 - bx0, 0, 0), (0, -1, 0), bx1 - bx0), ((bx1, by0, 0), (0, by1 - by0, 0), (1, 0, 0), by1 - by0), ((bx0, by1, 0), (0, by0 - by1, 0), (-1, 0, 0), by1 - by0)):
        p0 = Vector(p0); pu = Vector(pu); mb.oface([p0, p0 + pu, p0 + pu + Vector((0, 0, bh)), p0 + Vector((0, 0, bh))], M['brick_s'], [(0, 0), (L_ / 2, 0), (L_ / 2, bh / 1.92), (0, bh / 1.92)], nrm)
    mb.oface([(bx0 - 0.3, by0 - 0.3, bh), (bx1 + 0.3, by0 - 0.3, bh), (bx1 + 0.3, (by0 + by1) / 2, bh + 2.4), (bx0 - 0.3, (by0 + by1) / 2, bh + 2.4)], M['slate'], [(0, 0), (4, 0), (4, 3), (0, 3)], (0, -1, 1))
    for c in (-25.0, -21.0): arch_window(face_y=by0, c=c, w=1.3, z0=1.4, z1=3.8)
    ch = Vector((-23.0, 27.0, 0)); hc = 36.0; segs = 8
    for k in range(segs):                                                          # tapering square chimney, banded
        z0, z1 = hc * k / segs, hc * (k + 1) / segs; w0, w1 = 1.6 - 0.45 * k / segs, 1.6 - 0.45 * (k + 1) / segs
        for (n, a) in ((Vector((0, -1, 0)), Vector((1, 0, 0))), (Vector((1, 0, 0)), Vector((0, 1, 0))), (Vector((0, 1, 0)), Vector((-1, 0, 0))), (Vector((-1, 0, 0)), Vector((0, -1, 0)))):
            pts = [ch + n * w0 - a * w0 + Vector((0, 0, z0)), ch + n * w0 + a * w0 + Vector((0, 0, z0)), ch + n * w1 + a * w1 + Vector((0, 0, z1)), ch + n * w1 - a * w1 + Vector((0, 0, z1))]
            mb.oface(pts, M['brick_s'] if k > 4 else M['brick'], [(0, z0 / 1.92), (w0, z0 / 1.92), (w1, z1 / 1.92), (0, z1 / 1.92)], n)
    for z, w_ in ((0.0, 2.1), (hc - 1.2, 1.35), (hc - 0.2, 1.45)):
        mb.box((ch.x - w_, ch.y - w_, z), (ch.x + w_, ch.y + w_, z + (1.6 if z == 0 else 0.5)), M['stone'] if z else M['stone_d'])
    _obj(mb, 'engine_house', SET, hull=0.04); _obj(win, 'engine_windows', SET, shadow=False)
    sm = MB(); pm = _mat_puff(STATE['pre'] + 'smoke', STATE['tx']['puff'], (0.36, 0.38, 0.46) if STATE['preset'] == 'DUSK' else (0.6, 0.62, 0.7), 1.0, 0.85); r = _rnd(51)
    for k in range(14):                                                            # smoke plume drifting east-north
        t = k / 13; c = ch + Vector((t * 22.0 + r.uniform(-1, 1), t * 6.0, hc + 1.0 + t * 7.0 + r.uniform(-0.5, 0.5))); s = 1.3 + 3.2 * t
        sm.face([c + Vector((-s, -0.2 * k, -s)), c + Vector((s, -0.2 * k, -s)), c + Vector((s, -0.2 * k, s)), c + Vector((-s, -0.2 * k, s))], pm, [(0, 0), (1, 0), (1, 1), (0, 1)])
    _obj(sm, 'chimney_smoke', SET, shadow=False)

def _pit_bank(SET, M):
    """The shaft top: raised plank deck (banking, z 1.4) round the shaft, steps, railings, the cage at bank level with the lattice cage
    gate in front (the gate the boy runs out of), tubs on the deck rails, the rails down a ramp to the yard and on to the heaps."""
    mb = MB(); X0, Y0 = SHAFT_C; dz = DECK_Z
    mb.box((X0 - 4.2, Y0 - 3.4, 0), (X0 + 4.2, Y0 + 3.4, dz), M['planks'], mats=dict(front=M['wood_d'], right=M['wood_d'], left=M['wood_d'], back=M['wood_d']))
    for k in range(5): mb.box((X0 - 4.0 + k * 2.0 - 0.15, Y0 - 3.45, 0), (X0 - 4.0 + k * 2.0 + 0.15, Y0 - 3.35, dz), M['timber'])
    for k in range(4):                                                            # steps at the south-west corner
        mb.box((X0 - 3.8, Y0 - 3.4 - 0.45 * (k + 1), 0), (X0 - 2.4, Y0 - 3.4 - 0.45 * k, dz * (4 - k) / 4), M['wood'])
    mb.box((X0 - 2.2, Y0 - 1.8, dz - 0.02), (X0 + 2.2, Y0 + 1.8, dz + 0.01), M['black'])                # the shaft mouth
    for sx in (-1, 1):                                                              # guides and the cage
        for sy in (-1, 1): mb.box((X0 + sx * 1.9 - 0.1, Y0 + sy * 1.2 - 0.1, dz), (X0 + sx * 1.9 + 0.1, Y0 + sy * 1.2 + 0.1, 19.0), M['wood_d'])
    cz = dz; w2, d2, h = 1.6, 1.1, 3.4
    for sx in (-1, 1):
        for sy in (-1, 1): mb.box((X0 + sx * w2 - 0.07, Y0 + sy * d2 - 0.07, cz), (X0 + sx * w2 + 0.07, Y0 + sy * d2 + 0.07, cz + h + 0.3), M['iron'])
    for z in (cz, cz + h): mb.box((X0 - w2, Y0 - d2, z), (X0 + w2, Y0 + d2, z + 0.14), M['iron'])
    for sx in (-1, 1):
        for k in range(8): mb.box((X0 + sx * w2 - 0.02, Y0 - d2 + k * 0.3, cz + 0.14), (X0 + sx * w2 + 0.02, Y0 - d2 + k * 0.3 + 0.04, cz + h), M['iron'])
    rod(mb, (X0, Y0, cz + h + 0.3), (X0, Y0, cz + h + 1.5), 0.08, M['iron'], seg=6)
    for sx in (-1, 1): rod(mb, (X0 + sx * w2, Y0, cz + h + 0.14), (X0, Y0, cz + h + 1.3), 0.03, M['iron'], seg=4)
    gy = Y0 - 1.9                                                                  # the cage gate (lattice, closed left leaf, right leaf open)
    for (xa, xb) in ((X0 - 2.0, X0 - 0.05), (X0 + 1.2, X0 + 2.1)):
        for z in (dz, dz + 2.6): mb.box((xa, gy - 0.04, z), (xb, gy + 0.04, z + 0.09), M['iron'])
        n = max(2, int((xb - xa) / 0.2))
        for k in range(n + 1): x = xa + k * (xb - xa) / n; mb.box((x - 0.02, gy - 0.02, dz), (x + 0.02, gy + 0.02, dz + 2.69), M['iron'])
        for k in range(n):
            a_ = xa + k * (xb - xa) / n; b_ = xa + (k + 1) * (xb - xa) / n
            beam(mb, (a_, gy, dz + 0.15), (b_, gy, dz + 2.5), 0.03, 0.03, M['iron']); beam(mb, (b_, gy, dz + 0.15), (a_, gy, dz + 2.5), 0.03, 0.03, M['iron'])
    for sx in (-2.15, 2.15): mb.box((X0 + sx - 0.1, gy - 0.1, dz), (X0 + sx + 0.1, gy + 0.1, dz + 3.2), M['steel'])
    mb.box((X0 - 2.3, gy - 0.1, dz + 3.1), (X0 + 2.3, gy + 0.1, dz + 3.35), M['steel'])
    for (a, b) in (((X0 + 2.3, Y0 - 3.3), (X0 + 4.1, Y0 - 3.3)), ((X0 + 4.1, Y0 - 3.3), (X0 + 4.1, Y0 + 3.3)), ((X0 - 4.1, Y0 + 3.3), (X0 - 4.1, Y0 - 1.0)), ((X0 - 2.3, Y0 - 3.3), (X0 - 2.3, Y0 - 1.9))):
        for z in (dz + 0.6, dz + 1.2): rod(mb, (a[0], a[1], z), (b[0], b[1], z), 0.04, M['iron'], seg=4)
        for t in (0.0, 0.5, 1.0): rod(mb, (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, dz), (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, dz + 1.25), 0.04, M['iron'], seg=4)
    _obj(mb, 'pit_bank', SET, hull=0.025)
    # rails: from the gate south down a ramp to the yard (x 0.6), branch west to the heap
    rl = MB(); sl = MB(); r = _rnd(53)
    def track(pts, z_of):
        for i in range(len(pts) - 1):
            a, b = Vector(pts[i]), Vector(pts[i + 1]); d = (b - a); d.z = 0; d.normalize(); s = Vector((d.y, -d.x, 0))
            for g in (-0.55, 0.55):
                pa = a + s * g + Vector((0, 0, z_of(a) + 0.15)); pb = b + s * g + Vector((0, 0, z_of(b) + 0.15)); beam(rl, pa, pb, 0.09, 0.1, M['rail'])
            n = int((b - a).length / 0.75)
            for k in range(n):
                p = a.lerp(b, (k + 0.5) / n); obox(sl, p + Vector((0, 0, z_of(p) + 0.04)), d, s, (0, 0, 1), 0.12, 0.8, 0.04, M['wood_d'])
    ramp = lambda p: dz * max(0.0, min(1.0, (p.y - 1.0) / (Y0 - 3.4 - 1.0))) if p.y < Y0 - 3.4 else dz
    track([(0.6, Y0 + 1.0, 0), (0.6, Y0 - 3.4, 0), (0.6, 1.0, 0), (0.6, -14.0, 0)], ramp)
    track([(0.6, 3.0, 0), (-2.0, 1.0, 0), (-7.0, 0.0, 0), (-12.0, 0.4, 0)], lambda p: 0.0)
    _obj(rl, 'pit_rails', SET); _obj(sl, 'pit_sleepers', SET, hull=0.01)
    tb = MB()
    for (x, y, rot, ld, z) in ((0.6, 5.0, 0.0, True, 0.6), (0.6, 2.8, 0.0, True, 0.0), (0.6, Y0 - 1.0, 0.0, False, dz), (-8.2, -0.1, 1.55, True, 0.0), (-10.4, 0.25, 1.62, False, 0.0)):
        _yard_tub(tb, (x, y, z), rot, M, ld, seed=int(x * 10 + y))
    _obj(tb, 'pit_tubs', SET, hull=0.02)
    # coal heaps: big conical heap north-east, a long low heap west, spilled coal; a tipped tub
    hp = MB()
    for (c, R, H, sd) in (((13.0, 18.0, 0), 7.0, 6.5, 1), ((-13.5, -2.0, 0), 4.5, 2.6, 2), ((-12.0, 3.8, 0), 3.4, 2.0, 3), ((7.5, 13.5, 0), 3.0, 1.8, 4)):
        _heap(hp, Vector(c), R, H, M['lumps'], sd)
    _obj(hp, 'coal_heaps', SET)

def _heap(mb, c, R, H, mat, seed):
    nr, na = 7, 28
    def pt(i, j):
        t = i / nr; a = 2 * math.pi * j / na; rr = R * t * (1 + 0.12 * (vnoise(math.cos(a) * 2 + 4, math.sin(a) * 2 + t * 3, seed) - 0.5) * 2)
        z = H * (1 - t ** 1.25) * (1 + 0.1 * (vnoise(a * 2, t * 4, seed + 9) - 0.5)) if i < nr else 0.0
        return c + Vector((rr * math.cos(a), rr * math.sin(a), max(0.0, z)))
    for i in range(nr):
        for j in range(na):
            mb.face([pt(i + 1, j), pt(i + 1, (j + 1) % na), pt(i, (j + 1) % na), pt(i, j)], mat, [(j / na * R / 2, (i + 1) / nr * R / 2), ((j + 1) / na * R / 2, (i + 1) / nr * R / 2), ((j + 1) / na * R / 2, i / nr * R / 2), (j / na * R / 2, i / nr * R / 2)])

def _yard_tub(mb, c, rot, M, loaded, seed):
    c = Vector(c); t = Vector((math.sin(rot), math.cos(rot), 0)); rr = Vector((t.y, -t.x, 0)); Z = Vector((0, 0, 1)); L2, W2, z0, z1 = 0.95, 0.68, 0.32, 1.3
    for (n, a, ha, hn) in ((rr, t, L2, W2), (-rr, t, L2, W2), (t, rr, W2, L2), (-t, rr, W2, L2)):
        p = [c + n * hn - a * ha + Z * z0, c + n * hn + a * ha + Z * z0, c + n * (hn + 0.06) + a * (ha + 0.04) + Z * z1, c + n * (hn + 0.06) - a * (ha + 0.04) + Z * z1]
        mb.oface(p, M['tub'], [(0, 0), (2, 0), (2, 1.4), (0, 1.4)], n)
    mb.oface([c - t * L2 - rr * W2 + Z * z0, c + t * L2 - rr * W2 + Z * z0, c + t * L2 + rr * W2 + Z * z0, c - t * L2 + rr * W2 + Z * z0], M['iron'], [(0, 0)] * 4, (0, 0, -1))
    for sa in (-1, 1):
        for sb in (-1, 1): hub = c + t * sa * 0.55 + rr * sb * 0.55 + Z * 0.27; mb.frustum(hub - rr * 0.06, hub + rr * 0.06, 0.25, 0.25, M['iron'], seg=12)
    if loaded: lumpy(mb, c + Z * (z1 - 0.05), 1.0, M['lumps_s'], seed, seg=12, rings=6, rough=0.25, squash=0.42)

def _hut(SET, M):
    """First-aid hut (x 9..14, y -4..0): green weatherboard, slate roof, door, a warm-lit window, FIRST AID board, a lamp over the
    door; the bench in front with the brass oxygen resuscitation box (glass window in the lid: a green cylinder and valve inside),
    its rubber tube and small mask."""
    mb = MB(); win = MB(); x0, x1, y0, y1 = HUT; H = 3.4
    for (p0, pu, nrm, L_) in (((x0, y0, 0), (x1 - x0, 0, 0), (0, -1, 0), x1 - x0), ((x1, y0, 0), (0, y1 - y0, 0), (1, 0, 0), y1 - y0), ((x1, y1, 0), (x0 - x1, 0, 0), (0, 1, 0), x1 - x0), ((x0, y1, 0), (0, y0 - y1, 0), (-1, 0, 0), y1 - y0)):
        p0 = Vector(p0); pu = Vector(pu); mb.oface([p0, p0 + pu, p0 + pu + Vector((0, 0, H)), p0 + Vector((0, 0, H))], M['hut'], [(0, 0), (L_ / 2, 0), (L_ / 2, H / 2), (0, H / 2)], nrm)
    ym = (y0 + y1) / 2
    for xa, sg in ((x0, -1), (x1, 1)): mb.oface([(xa, y0, H), (xa, y1, H), (xa, ym, H + 1.6)], M['hut'], [(0, 0), (2, 0), (1, 0.8)], (sg, 0, 0))
    for (ya, sgn) in ((y0, -1), (y1, 1)): mb.oface([(x0 - 0.4, ya + sgn * 0.45, H - 0.25), (x1 + 0.4, ya + sgn * 0.45, H - 0.25), (x1 + 0.4, ym, H + 1.65), (x0 - 0.4, ym, H + 1.65)], M['slate'], [(0, 0), (2.9, 0), (2.9, 1.3), (0, 1.3)], (0, sgn, 1))
    for xc in (x0, x1):
        for yc in (y0, y1): mb.box((xc - 0.12, yc - 0.12, 0), (xc + 0.12, yc + 0.12, H), M['white'])
    mb.box((x0 - 0.1, y0 - 0.1, 0), (x1 + 0.1, y1 + 0.1, 0.25), M['stone_d'], skip='bottom')
    dx0, dx1 = 9.5, 10.9                                                            # door with frame, step
    mb.oface([(dx0, y0 - 0.03, 0.25), (dx1, y0 - 0.03, 0.25), (dx1, y0 - 0.03, 2.75), (dx0, y0 - 0.03, 2.75)], M['wood'], [(0, 0)] * 4, (0, -1, 0))
    for x in (dx0, dx1): mb.box((x - 0.08, y0 - 0.1, 0.25), (x + 0.08, y0, 2.85), M['white'])
    mb.box((dx0 - 0.08, y0 - 0.1, 2.75), (dx1 + 0.08, y0, 2.9), M['white']); mb.box((dx0 - 0.2, y0 - 0.5, 0), (dx1 + 0.2, y0, 0.22), M['stone'])
    rod(mb, (dx1 - 0.2, y0 - 0.08, 1.4), (dx1 - 0.2, y0 - 0.16, 1.4), 0.04, M['brass'], seg=6)
    wx0, wx1, wz0, wz1 = 11.6, 13.4, 1.25, 2.55                                     # window (lit inside), cross bars, sill
    win.oface([(wx0, y0 - 0.03, wz0), (wx1, y0 - 0.03, wz0), (wx1, y0 - 0.03, wz1), (wx0, y0 - 0.03, wz1)], M['win'], [(0, 0)] * 4, (0, -1, 0))
    for x in (wx0, (wx0 + wx1) / 2, wx1): mb.box((x - 0.05, y0 - 0.09, wz0), (x + 0.05, y0 - 0.02, wz1), M['white'])
    for z in (wz0, (wz0 + wz1) / 2, wz1): mb.box((wx0, y0 - 0.09, z - 0.05), (wx1, y0 - 0.02, z + 0.05), M['white'])
    mb.box((wx0 - 0.15, y0 - 0.25, wz0 - 0.12), (wx1 + 0.15, y0, wz0 - 0.02), M['white'])
    mb.oface([(9.6, y0 - 0.05, 2.95), (12.6, y0 - 0.05, 2.95), (12.6, y0 - 0.05, 4.07), (9.6, y0 - 0.05, 4.07)], M['firstaid'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
    lp = Vector((10.2, y0 - 0.55, 3.0)); rod(mb, (10.2, y0, 3.3), lp + Vector((0, 0, 0.3)), 0.03, M['iron'], seg=4)        # lamp over the door
    mb.frustum(lp + Vector((0, 0, 0.3)), lp + Vector((0, 0, 0.12)), 0.08, 0.2, M['iron'], seg=10)
    win.sphere(lp, 0.12, M['lamp'], seg=10, rings=6)
    _light('hut_lamp', lp - Vector((0, 0, 0.05)), (1.0, 0.68, 0.38), 90.0 * STATE['P']['lamp_k'], radius=0.1)
    # bench (seat SEAT_Z) and the oxygen box on it
    bx0, bx1, by = BENCH
    mb.box((bx0, by - 0.4, SEAT_Z - 0.1), (bx1, by + 0.4, SEAT_Z), M['wood'])
    for x in (bx0 + 0.2, bx1 - 0.2):
        for dy in (-0.3, 0.3): mb.box((x - 0.07, by + dy - 0.07, 0), (x + 0.07, by + dy + 0.07, SEAT_Z - 0.1), M['wood_d'])
    mb.box((bx0, by + 0.45, SEAT_Z + 0.35), (bx1, by + 0.55, SEAT_Z + 0.85), M['wood'])
    for x in (bx0 + 0.2, bx1 - 0.2): mb.box((x - 0.06, by + 0.45, SEAT_Z), (x + 0.06, by + 0.55, SEAT_Z + 0.9), M['wood_d'])
    _obj(mb, 'first_aid_hut', SET, hull=0.02); _obj(win, 'hut_windows', SET, shadow=False)
    ob = MB(); gl = MB(); ox, oy = OXY; z0 = SEAT_Z; W2, D2, Hh = 0.55, 0.3, 0.5
    yf = oy - D2; xs = ox + 0.08                                                     # front: engraved panel (left) | glass window (right)
    ob.box((ox - W2, oy - D2, z0), (ox + W2, oy + D2, z0 + Hh), M['brass_d'], skip='front')
    ob.oface([(ox - W2, yf, z0), (xs, yf, z0), (xs, yf, z0 + Hh), (ox - W2, yf, z0 + Hh)], M['oxy'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
    wx0, wx1, wz0, wz1 = xs + 0.05, ox + W2 - 0.05, z0 + 0.06, z0 + Hh - 0.06
    for (p, q) in (((xs, z0), (wx0, z0 + Hh)), ((wx1, z0), (ox + W2, z0 + Hh)), ((wx0, z0), (wx1, wz0)), ((wx0, wz1), (wx1, z0 + Hh))):
        ob.oface([(p[0], yf, p[1]), (q[0], yf, p[1]), (q[0], yf, q[1]), (p[0], yf, q[1])], M['brass'], [(0, 0)] * 4, (0, -1, 0))
    for (p, q) in (((wx0 - 0.02, wz0 - 0.02), (wx1 + 0.02, wz0)), ((wx0 - 0.02, wz1), (wx1 + 0.02, wz1 + 0.02)), ((wx0 - 0.02, wz0), (wx0, wz1)), ((wx1, wz0), (wx1 + 0.02, wz1))):
        ob.box((p[0], yf - 0.025, p[1]), (q[0], yf, q[1]), M['brass'])                  # raised bead round the window
    for (x, z) in ((wx0 + 0.02, wz0 + 0.02), (wx1 - 0.02, wz0 + 0.02), (wx0 + 0.02, wz1 - 0.02), (wx1 - 0.02, wz1 - 0.02)): ob.sphere((x, yf - 0.026, z), 0.012, M['brass'], seg=6, rings=4)
    gl.quad((wx0, yf + 0.012, wz0), (wx1 - wx0, 0, 0), (0, 0, wz1 - wz0), M['glass'])
    ob_out = ob; ob = MB()                                                           # inside parts: no ink hull (it would fill the cavity)
    def Wm(nm, hx, sm): return mat_lit(STATE['pre'] + 'oxin_' + nm, hx, form=(0.0, -0.1, 0.25), shade_mul=sm, shade_mix=0.1)
    M = dict(M, cream=Wm('cream', '#f2e8d0', (3.4, 2.6, 1.3)), brass_d=Wm('brass', '#c08a40', (3.2, 2.2, 0.8)), cyl=_glossy(Wm('cyl', '#3e9a64', (1.6, 2.6, 1.2)), (1, 1, 1), 0.6, 0.15))   # warm-lit inside (no sun reaches it)
    ci = (wx0, oy - D2 + 0.02, wz0, wx1, oy + D2 - 0.03, wz1)                         # the cavity behind the glass (inner faces)
    ob.oface([(ci[0], ci[4], ci[2]), (ci[3], ci[4], ci[2]), (ci[3], ci[4], ci[5]), (ci[0], ci[4], ci[5])], M['cream'], [(0, 0)] * 4, (0, -1, 0))
    for x, n in ((ci[0], 1), (ci[3], -1)): ob.oface([(x, ci[1], ci[2]), (x, ci[4], ci[2]), (x, ci[4], ci[5]), (x, ci[1], ci[5])], M['brass_d'], [(0, 0)] * 4, (n, 0, 0))
    for z, n in ((ci[2], 1), (ci[5], -1)): ob.oface([(ci[0], ci[1], z), (ci[3], ci[1], z), (ci[3], ci[4], z), (ci[0], ci[4], z)], M['brass_d'], [(0, 0)] * 4, (0, 0, n))
    cxl = (wx0 + wx1) / 2 + 0.03; cyl_y = oy - 0.12
    rod(ob, (cxl, cyl_y, wz0 + 0.005), (cxl, cyl_y, wz1 - 0.12), 0.085, M['cyl'], seg=14)          # green oxygen cylinder standing inside
    ob.sphere((cxl, cyl_y, wz1 - 0.12), 0.085, M['cyl'], seg=14, rings=6)
    rod(ob, (cxl, cyl_y, wz1 - 0.06), (cxl, cyl_y, wz1 - 0.02), 0.025, M['brass'], seg=8)
    rod(ob, (cxl - 0.06, cyl_y, wz1 - 0.04), (cxl + 0.09, cyl_y, wz1 - 0.04), 0.018, M['brass'], seg=6)
    lumpy(ob, (cxl + 0.05, cyl_y + 0.24, wz0 + 0.08), 0.07, M['rubber'], 333, seg=8, rings=5, rough=0.15, squash=0.8)      # breathing bag
    _obj(ob, 'oxygen_box_inside', SET); ob = ob_out
    ob.box((ox - W2 - 0.02, oy - D2 - 0.02, z0 + Hh), (ox + W2 + 0.02, oy + D2 + 0.02, z0 + Hh + 0.06), M['brass'])        # lid
    ob.box((ox - W2 + 0.04, oy - D2 + 0.04, z0 + Hh + 0.06), (ox + W2 - 0.04, oy + D2 - 0.04, z0 + Hh + 0.085), M['brass_d'])
    for sx in (-1, 1): rod(ob, (ox + sx * 0.18, oy, z0 + Hh + 0.085), (ox + sx * 0.18, oy, z0 + Hh + 0.17), 0.014, M['brass'], seg=6)
    rod(ob, (ox - 0.18, oy, z0 + Hh + 0.17), (ox + 0.18, oy, z0 + Hh + 0.17), 0.016, M['brass'], seg=6)
    for sx in (-1, 1):                                                              # side handles, little feet
        rod(ob, (ox + sx * (W2 + 0.02), oy - 0.12, z0 + Hh - 0.12), (ox + sx * (W2 + 0.08), oy - 0.12, z0 + Hh - 0.12), 0.012, M['brass'], seg=4)
        rod(ob, (ox + sx * (W2 + 0.08), oy - 0.12, z0 + Hh - 0.12), (ox + sx * (W2 + 0.08), oy + 0.12, z0 + Hh - 0.12), 0.012, M['brass'], seg=4)
        rod(ob, (ox + sx * (W2 + 0.02), oy + 0.12, z0 + Hh - 0.12), (ox + sx * (W2 + 0.08), oy + 0.12, z0 + Hh - 0.12), 0.012, M['brass'], seg=4)
        for sy in (-1, 1): ob.sphere((ox + sx * (W2 - 0.06), oy + sy * (D2 - 0.06), z0 + 0.01), 0.03, M['brass_d'], seg=6, rings=4)
    rod(ob, (ox + W2, oy + 0.1, z0 + 0.25), (ox + W2 + 0.08, oy + 0.1, z0 + 0.25), 0.03, M['brass'], seg=8)  # outlet valve, tube, mask
    tp = [Vector((ox + W2 + 0.08, oy + 0.1, z0 + 0.25))] + [Vector((ox + W2 + 0.2 + 0.25 * math.sin(a), oy - 0.05 - 0.2 * math.cos(a) + 0.05 * a, z0 + 0.03 + 0.01 * a)) for a in [k * 0.5 for k in range(11)]]
    chain_rod(ob, tp, 0.022, M['rubber'], seg=6)
    mk = tp[-1] + Vector((0.08, -0.05, 0.0)); ob.frustum(mk, mk + Vector((0.1, -0.04, 0.06)), 0.03, 0.09, M['rubber'], seg=10)
    o = _obj(ob, 'oxygen_box', SET, hull=0.006); _obj(gl, 'oxygen_glass', SET, shadow=False)
    STATE['oxy'] = dict(box=(ox, oy, z0), window=(round(wx0, 3), round(yf, 3), round(wz0, 3), round(wx1, 3), round(wz1, 3)), size=(2 * W2, 2 * D2, Hh + 0.09), mask=tuple(round(v, 3) for v in mk), bird_spot=(round(ox - W2 - 0.25, 3), round(oy - 0.05, 3), z0))

def _pick_s(mb, M, head, d): _pick(mb, dict(M, wood=M['wood'], iron=M['iron']), head, Vector(d).normalized(), 1.55)
def _shovel_s(mb, M, tip, d): _shovel(mb, dict(M, steel=M['iron'], wood=M['wood']), tip, Vector(d).normalized(), 1.4)

def _lamp_post(mb, win, c, M, h=4.4):
    c = Vector(c); rod(mb, c, c + Vector((0, 0, 0.6)), 0.14, M['black'], seg=8, r1=0.09); rod(mb, c + Vector((0, 0, 0.6)), c + Vector((0, 0, h)), 0.07, M['black'], seg=6)
    rod(mb, c + Vector((-0.4, 0, h - 0.5)), c + Vector((0.4, 0, h - 0.5)), 0.03, M['black'], seg=4)
    top = c + Vector((0, 0, h)); mb.frustum(top, top + Vector((0, 0, 0.12)), 0.2, 0.25, M['black'], seg=4)
    win.frustum(top + Vector((0, 0, 0.12)), top + Vector((0, 0, 0.7)), 0.24, 0.3, M['lamp'], seg=4, cap0=False, cap1=False)
    mb.frustum(top + Vector((0, 0, 0.7)), top + Vector((0, 0, 1.0)), 0.36, 0.05, M['black'], seg=4)
    return top + Vector((0, 0, 0.4))

def _pit_props(SET, M, dress):
    """Yard dressing: gas lamp posts (lit), the pit-prop stack, barrels, sacks, a wheelbarrow, two railway coal wagons on the siding,
    a telegraph line, fence, a ladder, a row of 3D terraced houses on the far side of the yard (y 52) for depth."""
    mb = MB(); win = MB(); r = _rnd(61); P = STATE['P']
    for i, (x, y) in enumerate(PIT_LAMPS):
        p = _lamp_post(mb, win, (x, y, 0 if (x, y) not in ((-4.0, 8.4), (4.0, 8.4)) else DECK_Z), M, 4.4 if y < 8 else 3.2)
        if i < 3: _light('yard_lamp_%d' % i, p, (1.0, 0.7, 0.4), 160.0 * P['lamp_k'], radius=0.15)
    if dress:
        for k in range(14):                                                        # pit-prop stack west of the track
            row = k // 5; i = k % 5; y = -8.5 + i * 0.36 + row * 0.18; z = 0.17 + row * 0.3
            rod(mb, (-7.5 + r.uniform(-0.2, 0.2), y, z), (-3.4 + r.uniform(-0.2, 0.2), y, z), 0.16, M['timber'], seg=8, uv=(1.0, 2.0))
        for k, (x, y) in enumerate(((5.6, -1.8), (6.4, -1.2), (5.9, -0.6), (15.6, -2.4))):
            mb.frustum((x, y, 0), (x, y, 1.1), 0.36, 0.4, M['wood_d'], seg=12); mb.frustum((x, y, 1.1), (x, y, 1.12), 0.4, 0.0, M['wood'], seg=12)
            for z in (0.15, 0.55, 0.95): mb.frustum((x, y, z), (x, y, z + 0.06), 0.41, 0.42, M['iron'], seg=12, cap0=False, cap1=False)
        for k in range(5): lumpy(mb, (7.0 + 0.55 * (k % 3), -2.6 + 0.4 * (k // 3), 0.3 + 0.45 * (k // 3)), 0.33, M['sack'], 90 + k, seg=10, rings=6, rough=0.12, squash=0.65)
        _yard_tub(mb, (0.6, -8.6, 0.0), 0.0, M, True, 77); _yard_tub(mb, (0.6, -11.0, 0.0), 0.0, M, True, 78)           # foreground train on the rails
        for k in range(4): lumpy(mb, (-1.4 + 0.5 * (k % 2), -12.2 + 0.45 * k, 0.12), 0.18, M['lumps_s'], 120 + k, seg=8, rings=5, rough=0.4, squash=0.7)
        for k in range(3): lumpy(mb, (3.2 + 0.6 * k, -13.6 + 0.2 * k, 0.3), 0.34, M['sack'], 130 + k, seg=10, rings=6, rough=0.12, squash=0.65)
        _pick_s(mb, M, (2.9, -14.2, 0.06), (0.3, 0.9, 0.35)); _shovel_s(mb, M, (3.9, -14.3, 0.02), (0.15, 0.25, 1.0))
        wb = Vector((4.2, -9.0, 0)); mb.box((wb.x - 0.5, wb.y - 0.7, 0.45), (wb.x + 0.5, wb.y + 0.5, 0.95), M['wood']); mb.frustum((wb.x, wb.y + 0.8, 0.25), (wb.x + 0.12, wb.y + 0.8, 0.25), 0.25, 0.25, M['iron'], seg=10)
        for sx in (-1, 1): rod(mb, (wb.x + sx * 0.35, wb.y - 0.6, 0.5), (wb.x + sx * 0.45, wb.y - 1.9, 0.75), 0.04, M['wood_d'], seg=5)
        lumpy(mb, (wb.x, wb.y - 0.1, 0.95), 0.5, M['lumps_s'], 95, seg=10, rings=5, rough=0.3, squash=0.5)
        for k in range(2):                                                         # railway coal wagons (private owner, red-brown), siding at x 18
            y = 2.0 + k * 6.0; c = Vector((19.0, y, 0))
            mb.box((c.x - 1.4, c.y - 2.6, 0.9), (c.x + 1.4, c.y + 2.6, 3.0), M['steel_r'], mats=dict(top=M['lumps_s']))
            for dy in (-1.8, 1.8):
                for dx in (-1.45, 1.45): mb.frustum((c.x + dx - 0.08, c.y + dy, 0.55), (c.x + dx + 0.08, c.y + dy, 0.55), 0.5, 0.5, M['iron'], seg=14)
            mb.box((c.x - 1.5, c.y - 2.8, 0.75), (c.x + 1.5, c.y + 2.8, 0.95), M['black'])
            lumpy(mb, (c.x, c.y, 3.0), 1.0, M['lumps_s'], 97 + k, seg=12, rings=6, rough=0.25, squash=0.3)
        for y in range(-20, 30, 2): obox(mb, (19.0, y, 0.04), (0, 1, 0), (1, 0, 0), (0, 0, 1), 0.12, 1.1, 0.04, M['wood_d'])
        for g in (-0.55, 0.55): mb.box((19.0 + g - 0.05, -20, 0.08), (19.0 + g + 0.05, 30, 0.2), M['rail'])
        for k in range(5):                                                          # telegraph poles along the siding
            y = -16 + k * 10; rod(mb, (23.0, y, 0), (23.0, y, 8.5), 0.12, M['wood_d'], seg=6); rod(mb, (22.2, y, 8.0), (23.8, y, 8.0), 0.06, M['wood_d'], seg=4)
            if k < 4:
                for x in (22.4, 23.6): chain_rod(mb, catenary((x, y, 8.08), (x, y + 10, 8.08), 0.35, 8), 0.015, M['cable'], seg=4)
        for k in range(16):                                                         # paling fence along the yard's south-west
            x = -26 + k * 1.2; mb.box((x - 0.06, -14.0, 0), (x + 0.06, -13.9, 1.6), M['wood_d'])
        for z in (0.5, 1.3): mb.box((-26.2, -14.05, z), (-7.8, -13.95, z + 0.1), M['wood_d'])
        for (a, b) in ((( -3.95, 9.0, DECK_Z), (-3.5, 9.0, 6.0)),):
            for dx in (0.0, 0.5): rod(mb, (a[0], a[1] + dx, a[2]), (b[0], b[1] + dx, b[2]), 0.04, M['wood'], seg=4)
            for k in range(9): z = DECK_Z + 0.5 * (k + 1); xq = a[0] + (b[0] - a[0]) * (z - a[2]) / (b[2] - a[2]); rod(mb, (xq, a[1], z), (xq, a[1] + 0.5, z), 0.03, M['wood'], seg=4)
        # puddles in the yard
        for (x, y, rx, ry) in ((2.2, -5.0, 1.4, 0.6), (-1.6, -9.5, 1.1, 0.5), (6.2, -11.0, 0.9, 0.45), (-5.0, 3.0, 1.0, 0.5)):
            pts = [Vector((x + rx * math.cos(2 * math.pi * i / 16) * (1 + 0.15 * math.sin(3 * i)), y + ry * math.sin(2 * math.pi * i / 16), 0.012)) for i in range(16)]
            mb.face(pts, M['puddle'])
    # terraced houses across the yard (y 52..58), facing south: brick, slate, chimney stacks, windows (some lit)
    th = MB(); tw = MB(); x = -46.0; k = 0
    while x < 46.0:
        w = 3.2; H = 5.2; y0 = 52.0 + 0.4 * math.sin(k)
        th.oface([(x, y0, 0), (x + w, y0, 0), (x + w, y0, H), (x, y0, H)], M['brick'], [(x / 2, 0), ((x + w) / 2, 0), ((x + w) / 2, H / 1.92), (x / 2, H / 1.92)], (0, -1, 0))
        th.oface([(x - 0.02, y0 - 0.4, H - 0.1), (x + w + 0.02, y0 - 0.4, H - 0.1), (x + w + 0.02, y0 + 3.0, H + 2.4), (x - 0.02, y0 + 3.0, H + 2.4)], M['slate'], [(0, 0), (1.6, 0), (1.6, 2), (0, 2)], (0, -1, 1))
        for (wx, wz) in ((0.4, 0.8), (2.0, 0.8), (0.4, 3.1), (2.0, 3.1)):
            lit = r.random() < (0.45 if P.get('sky') == 'dusk' else 0.15)
            (tw if lit else th).oface([(x + wx, y0 - 0.03, wz), (x + wx + 0.8, y0 - 0.03, wz), (x + wx + 0.8, y0 - 0.03, wz + 1.3), (x + wx, y0 - 0.03, wz + 1.3)], M['win'] if lit else M['win_d'], [(0, 0)] * 4, (0, -1, 0))
        if k % 2 == 0: th.box((x + w - 0.5, y0 + 1.2, H + 0.8), (x + w + 0.5, y0 + 1.9, H + 2.8), M['brick_s'])
        x += w; k += 1
    _obj(mb, 'yard_dressing', SET, hull=0.02); _obj(win, 'yard_lamps', SET, shadow=False); _obj(th, 'terraces', SET); _obj(tw, 'terrace_windows', SET, shadow=False)

# ============================================================================= anchors, cameras
TUNNEL_MARKS = [tuple(round(v, 3) for v in TP(y, s, 0)) for (y, s) in ((5.0, -0.9), (8.5, -1.1), (12.0, -0.7), (15.5, -1.2), (24.5, -0.6), (28.0, -1.0))]
def _tc(y, s, z): return tuple(round(v, 3) for v in TP(y, s, z))
CAMS_T = dict(
    tunnel_eye=dict(loc=_tc(1.6, -0.55, 2.35), look_at=_tc(19.0, 0.2, 1.85), lens=22),
    tunnel_low=dict(loc=_tc(4.1, -1.45, 0.55), look_at=_tc(12.0, 0.2, 2.75), lens=22),
    cage_insert=dict(loc=_tc(15.35, -1.3, 2.88), look_at=_tc(16.25, -1.86, 2.84), lens=22),
    lamp_insert=dict(loc=_tc(8.05, 0.62, 3.42), look_at=_tc(8.75, 1.25, 3.38), lens=22),
    tunnel_run=dict(loc=_tc(31.5, -0.5, 0.85), look_at=_tc(4.0, 0.3, 2.3), lens=22),
    blast_wide=dict(loc=(-0.9, -3.2, 2.6), look_at=_tc(26.0, 0.0, 2.3), lens=22),
)
CAMS_P = dict(
    pithead_wide=dict(loc=(7.5, -19.0, 2.4), look_at=(-2.0, 12.0, 11.0), lens=22),
    oxygen_insert=dict(loc=(10.35, -6.55, 1.72), look_at=(11.2, -4.95, 1.2), lens=22),
)
CAM_NOTES = dict(
    tunnel_eye='eye level (2.35 D) just inside the roadway mouth looking inbye: actors at tunnel_marks in depth on the walkway (left of the rails), the timber sets marching into the bend, hanging lamps, the tub train right, the coal face at the end',
    tunnel_low='0.55 D off the floor among the props: a pick on the floor and a puddle in the foreground, the lamp of set 2 overhead, the lagged roof and the tub train',
    cage_insert='ECU on the canary cage on its nail (set 6, left leg); the hanging lamp of set 7 behind it gives the warm back light; strong DOF',
    lamp_insert='ECU on the foreman\'s flame safety lamp hanging on the right leg of set 3: brass bonnet, gauze, glass and the flame (set_flame)',
    tunnel_run='low (0.85 D) deep in the roadway looking outbye at the bright pit bottom: miners run away from the camera toward the exit',
    blast_wide='from the pit bottom, 2.7 D high, looking inbye down the whole roadway: the fireball comes round the bend toward the camera (set_blast)',
    pithead_wide='establishing from the yard 27 D south-east of the shaft: the headframe with its two spoked wheels, the engine house and chimney left, the cage gate on the bank, heaps, lamps, the first-aid hut right, terraced rows on the backdrop',
    oxygen_insert='close on the brass oxygen box on the bench in front of the first-aid hut, dusk light from the left, the hut lamp warm above',
)
DOF = dict(cage_insert=dict(focus=CAGE_HOOK, fstop=3.0), lamp_insert=dict(focus=INSERT_LAMP, fstop=3.0), tunnel_eye=dict(focus=_tc(8.5, -1.1, 1.6), fstop=2.5),
           tunnel_low=dict(focus=_tc(10.0, 0.0, 1.6), fstop=4.0), tunnel_run=dict(focus=_tc(24.5, -0.6, 1.4), fstop=3.0), blast_wide=None,
           pithead_wide=None, oxygen_insert=dict(focus=(11.15, -5.05, 1.25), fstop=5.0))

def apply_dof(cam_name, scene=None, cam=None):
    d = DOF.get(cam_name)
    if d is None: return setup_dof(scene, None, None, cam=cam)
    f = d['focus']
    if cam_name == 'lamp_insert': f = tuple(STATE['insert_flame_pos'])
    if cam_name == 'cage_insert': c = STATE['cage']; f = (c['perch'][0], c['perch'][1], c['perch'][2] + 0.15)
    return setup_dof(scene, f, d['fstop'], cam=cam)

def anchors():
    P = STATE['P']; loc = STATE['loc']
    base = dict(location=loc, preset=STATE['preset'], render=dict(samples_final=12, resolution=(720, 1280), threads=2, shade=P['shade'], lift=P['lift'], toon=P['toon']), cam_notes={})
    if loc == 'tunnel':
        base.update(
            cams={k: dict(v) for k, v in CAMS_T.items()}, cam_notes={k: CAM_NOTES[k] for k in CAMS_T},
            tunnel=dict(length=TUN_L, centre='x = 1.8 sin(pi y / 40), 0 <= y <= 40', half_width=WALL_HW, wall_z=WALL_Z, roof_z=ROOF_Z, set_y=list(SET_Y), leg_s=LEG_S, cap_z=CAP_Z,
                        track=dict(s=TRACK_S, gauge=GAUGE), face_y=TUN_L, walkway='s -1.9 .. -0.1 (left of the rails)', pit_bottom=dict(y=(PB_Y0, 0.0), half_width=PB_HW, height=PB_H),
                        shaft=dict(y=SHAFT_Y, cage_floor=0.0, gate_y=PB_Y0 + 0.45), exit_point=(0.0, -2.0, 0.0)),
            tunnel_marks=[tuple(m) for m in TUNNEL_MARKS], boy_mark=_tc(15.0, -1.0, 0), foreman_mark=_tc(9.7, -0.6, 0),
            run_path=[_tc(y, -0.5, 0) for y in (30.0, 24.0, 18.0, 12.0, 6.0, 1.0)] + [(0.0, -3.0, 0.0), (0.0, -7.0, 0.0)],
            cage=dict(STATE['cage']), cage_hook=STATE['cage']['hook'], lamp_hook=tuple(round(v, 3) for v in TP(*INSERT_LAMP)), insert_flame=tuple(round(v, 3) for v in STATE['insert_flame_pos']),
            fixed_lamps=[tuple(round(v, 3) for v in L.location) for L in STATE['fixed_lamps']], heading=dict(STATE['heading']),
            tubs=[_tc(y, TRACK_S, 0) for (y, _, _) in TUBS], blast=dict(start_y=TUN_L, end_y=1.0, front='blast_front(u)'),
            lamp=dict(energy_per_strength=LAMP_E, colour=WARM, note='lamp_light(pos, strength, frame, name): put pos at the flame of the actor\'s lamp; 1.0 lights a surface 2 D away to about the lamp colour'),
            keep_out='props at s +-2.3 every 2.5 D (sets at y 1.25 + 2.5 k), rails s 0.25..1.35, tubs at tubs[], the timber stack y 27..31 s -2.4..-1.6, barrel (y 32.2, s 1.9), sacks y 9..10.6 s -2.3..-1.6, the heap at the face y > 37')
    else:
        base.update(
            cams={k: dict(v) for k, v in CAMS_P.items()}, cam_notes={k: CAM_NOTES[k] for k in CAMS_P}, key_dir=tuple(Vector(P['key_dir']).normalized()), sun_elevation_deg=P['sun_elev'],
            shaft=dict(centre=(SHAFT_C[0], SHAFT_C[1], DECK_Z), deck_z=DECK_Z, gate=(0.0, SHAFT_C[1] - 1.9, DECK_Z), cage_floor=DECK_Z), wheels=list(STATE['wheels']),
            headframe=dict(top_z=21.0, wheel_radius=2.3), engine_house=dict(x=(-19.0, -9.0), y=(5.0, 19.0)), chimney=(-23.0, 27.0, 36.0),
            hut=dict(x=(HUT[0], HUT[1]), y=(HUT[2], HUT[3]), door=(10.2, HUT[2], 0.25)), bench=dict(x=(BENCH[0], BENCH[1]), y=BENCH[2], seat_z=SEAT_Z), oxygen=dict(STATE['oxy']),
            boy_mark=(9.6, -5.9, 0.0), gate_mark=(0.6, SHAFT_C[1] - 2.6, DECK_Z), yard_marks=[(1.6, -3.0, 0.0), (-2.2, -6.0, 0.0), (4.6, -8.0, 0.0), (-1.0, 1.5, 0.0)],
            keep_out='headframe legs (+-3.3, 9.5/14.5) and back-legs to (-7.6, 9/15), the bank x -4.2..4.2 y 8.6..15.4 (z 1.4), heaps, hut x 9..14 y -4..0, bench, wagons x 17.5..20.5')
    return base

# ----------------------------------------------------------------------------- placeholder actors (stills and tests only)
T.PH.update(
    boy=('beach_kid', dict(yaw=-0.3, expr='determined', arm_r='down', arm_l='down', legs='stand'), 2.4),
    foreman=('boss', dict(yaw=0.35, head_roll=-4, expr='smug', arm_l='down', arm_r='hip', legs='stand'), 3.1),
    miner_a=('senior_b', dict(yaw=0.2, expr='neutral', arm_l='down', arm_r='down', legs='stand'), 2.9),
    miner_b=('senior_a', dict(yaw=0.4, expr='neutral', arm_l='down', arm_r='down', legs='stand'), 3.0))
placeholder_actor = T.placeholder_actor
STAGING = dict(tunnel_eye='eye', tunnel_low='low', cage_insert='none', lamp_insert='none', tunnel_run='run', blast_wide='none', pithead_wide='yard', oxygen_insert='none')

def stage_placeholders(A, where, cam_loc, lamps=True):
    """Placeholder actors for stills; underground each one carries a lit lamp (lamp_light at hand height)."""
    T._clear_actors()
    for o in list(bpy.data.objects):
        if o.name.startswith('miner_lamp_'): bpy.data.objects.remove(o, do_unlink=True)
    if where == 'none': return []
    if where == 'eye': spots = [('foreman', _tc(6.0, -0.9, 0)), ('miner_a', _tc(10.5, -1.2, 0)), ('boy', _tc(14.5, -0.6, 0)), ('miner_b', _tc(19.0, -1.0, 0))]
    elif where == 'low': spots = [('miner_a', _tc(9.2, -0.9, 0)), ('boy', _tc(12.2, -1.3, 0))]
    elif where == 'run': spots = [('boy', _tc(27.2, -1.45, 0)), ('miner_a', _tc(22.0, -1.6, 0)), ('foreman', _tc(16.5, -0.2, 0))]
    elif where == 'yard': spots = [('boy', A['boy_mark']), ('miner_a', A['yard_marks'][0]), ('foreman', A['yard_marks'][1])]
    else: spots = []
    out = []
    for i, (role, mk) in enumerate(spots):
        out.append(placeholder_actor(role, mk, face_to=cam_loc, tilt=0.0, name='actor_%s_%d' % (role, i)))
        if lamps and STATE['loc'] == 'tunnel':
            d = (Vector(cam_loc) - Vector(mk)); d.z = 0; d.normalize(); side = Vector((d.y, -d.x, 0))
            h = 1.15 if role != 'boy' else 0.95
            lamp_light(tuple(Vector(mk) + side * 0.55 + d * 0.15 + Vector((0, 0, h))), 1.0, None, 'miner_lamp_%d' % i)
    return out

def apply_cam_state(cam, preset):
    """Set-state of the contract stills: blast_wide shows the fireball at u 0.55; everything else at rest (gas 0)."""
    if STATE['loc'] != 'tunnel': return
    set_gas(0.0); set_flame(1.0); set_cage(None)
    set_blast(0.7 if cam == 'blast_wide' else 0.0)

# ----------------------------------------------------------------------------- CLI
def _load(): return ' '.join('%.2f' % v for v in os.getloadavg())

def cli_stills(quality='preview', outdir=None, cams=None, locs=('tunnel', 'pithead')):
    outdir = outdir or os.path.join(WORK, 'stills'); os.makedirs(outdir, exist_ok=True); res = {}
    for loc in locs:
        for pr in LOC_PRESETS[loc]:
            A = build(loc, pr); sc = bpy.context.scene; setup_render(sc, quality)
            for nm, cs in A['cams'].items():
                if cams and nm not in cams: continue
                apply_cam_state(nm, pr); make_camera(cs); apply_dof(nm); stage_placeholders(A, STAGING[nm], cs['loc'])
                w, c = render(os.path.join(outdir, '%s_%s.png' % (pr, nm))); res['%s_%s' % (pr, nm)] = (round(w, 1), round(c, 1))
                print('%s %s %s: %.1f s wall, %.1f s cpu, load %s' % (loc, pr, nm, w, c, _load()), flush=True)
    return res

def cli_tests(quality='preview'):
    """Blast u series (blast_wide, tunnel_run), gas series (tunnel_eye), flame series (lamp_insert), cage carried, drips."""
    out = os.path.join(WORK, 'tests'); os.makedirs(out, exist_ok=True)
    A = build('tunnel', 'LAMP'); sc = bpy.context.scene; setup_render(sc, quality); T._clear_actors()
    make_camera(A['cams']['blast_wide']); apply_dof('blast_wide')
    for u in (0.05, 0.2, 0.4, 0.6, 0.8, 0.95):
        set_blast(u); render(os.path.join(out, 'blast_wide_u%03d.png' % int(u * 100)))
    make_camera(A['cams']['tunnel_run']); apply_dof('tunnel_run'); stage_placeholders(A, 'run', A['cams']['tunnel_run']['loc'])
    for u in (0.1, 0.18, 0.5):
        set_blast(u); render(os.path.join(out, 'blast_run_u%03d.png' % int(u * 100)))
    set_blast(0.0); stage_placeholders(A, 'eye', A['cams']['tunnel_eye']['loc']); make_camera(A['cams']['tunnel_eye']); apply_dof('tunnel_eye')
    for g in (0.0, 0.5, 1.0, 3.0):
        set_gas(g); render(os.path.join(out, 'gas_eye_g%03d.png' % int(g * 100)))
    set_gas(0.0); T._clear_actors(); make_camera(A['cams']['lamp_insert']); apply_dof('lamp_insert')
    for k in (0.0, 1.0, 1.8):
        set_flame(k); render(os.path.join(out, 'flame_k%03d.png' % int(k * 100)))
    set_flame(1.0)

def cli_final(loc='tunnel', preset=None, cams=None):
    out = os.path.join(WORK, 'final'); os.makedirs(out, exist_ok=True)
    preset = preset or LOC_PRESETS[loc][0]
    A = build(loc, preset); sc = bpy.context.scene; setup_render(sc, 'final'); res = {}
    for nm, cs in A['cams'].items():
        if cams and nm not in cams: continue
        apply_cam_state(nm, preset); make_camera(cs); apply_dof(nm); stage_placeholders(A, STAGING[nm], cs['loc'])
        w, c = render(os.path.join(out, '%s_%s.png' % (preset, nm))); res[nm] = (round(w, 1), round(c, 1))
        print('final %s %s: %.1f s wall, %.1f s cpu, load %s' % (preset, nm, w, c, _load()), flush=True)
    return res

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stills'; arg = sys.argv[2:]
    if cmd == 'stills': cli_stills(cams=arg or None)
    elif cmd == 'tests': cli_tests()
    elif cmd == 'final': cli_final(arg[0] if arg else 'tunnel', arg[1] if len(arg) > 1 else None, arg[2:] or None)
    elif cmd == 'digest':
        A = build(arg[0] if arg else 'tunnel', arg[1] if len(arg) > 1 else None)
        if STATE['loc'] == 'tunnel': set_blast(0.5); set_gas(0.5)
        bpy.context.view_layer.update(); print('digest', digest())
    else: print(__doc__)

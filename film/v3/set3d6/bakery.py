#!/usr/bin/env python3
"""bakery.py : set of film 6 ("the 13th loaf"), a medieval English market town in the 1260s, as a real 3D Blender set (bpy 5.3, Cycles CPU).
Two locations in one module:

    import bakery as B
    A = B.build('bakery', 'MORNING')     # Henry's bakery inside: domed brick oven, tables, racks of loaves, counter onto the street
    A = B.build('market', 'AFTERNOON')   # the market square: jettied houses, bakery fronts, stalls, pillory, the big public balance
    B.set_steam(0.8, frame=10)           # white steam wisps rising off the hot loaves (0 none .. 1 full), scrolls with the frame
    B.set_oven(1.0, frame=10)            # oven fire 0 out .. 1 roaring (deterministic flicker in the frame; call per frame)
    B.set_scale(-6, frame=10)            # the small hand balance on the counter: + tips the loaf pan down
    B.set_big_scale(-8, frame=10)        # the big public balance: + tips the bread pan down (passes), - the weights pan down (short)
    B.set_loaves(13, frame=10)           # loaves on the big balance's bread pan 0..13 (12 = the dozen, 13 = + the 13th on top)
    cam = B.make_camera(A['cams']['bakery_wide'])

World: 1 unit = 1 D (head diameter), Z up, floor z = 0. Bakery: the room x -7..7, y 0..11 (front wall at y 0, the street at -y),
ceiling z 7; the oven against the back wall at x -2.5. Market: the square x -22..22, y -16..24, the camera side is south (-y);
the pillory at (-4, 9.5), the big balance at (6, 6), Henry's bakery front in the west row at x -22. NO depth of field (client rule:
images sharp): setup_dof is kept only so shot scripts can call setup_dof(scene, None, None).
Built on v3/set3d5/mine.py (itself on pagoda.py v2 and tower.py): materials, mesh builder, render, grade, cameras, keys, actors,
painted haze, denoiser are imported, not rewritten. See bakery_API.md.
CLI: python3 bakery.py stills | final <loc> [preset] [cams..] | digest <loc> <preset> | heads"""
import os, sys, math, json, time, random
import bpy
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (HERE, os.path.join(PROJ, 'v3', 'set3d2'), os.path.join(PROJ, 'v3', 'set3d4'), os.path.join(PROJ, 'v3', 'set3d5')):
    if p not in sys.path: sys.path.insert(0, p)
import tower as T                                          # noqa: E402
import pagoda as G                                         # noqa: E402
import mine as MN                                          # noqa: E402  (film-5 template: helpers, denoiser)
import bakery_tex as BT                                    # noqa: E402
from tower import MB, no_bounce, setup_grade, make_camera, render, mat_lit, mat_emit   # noqa: E402,F401
from mine import obox, beam, rod, lumpy, catenary, chain_rod, _obj, _untoon, _glossy, vnoise   # noqa: E402,F401
WORK = os.path.join(HERE, 'bakery_work')
T.ACT = os.path.join(WORK, 'actors')
STATE = T.STATE
setup_dof = G.setup_dof; digest = G.digest

# ----------------------------------------------------------------------------- dimensions (D)
ROOM = (-7.0, 7.0, 0.0, 11.0); CEIL = 7.0; WALL_T = 0.5
COUNTER_OPEN = (-1.5, 3.5, 1.25, 4.1)          # x0, x1, z0 (the counter / shutter board), z1 of the shop opening in the front wall
DOOR_OPEN = (-4.6, -2.8, 0.0, 4.3)             # the half door
WIN_OPEN = (4.7, 6.3, 2.5, 4.3)                # leaded window
COUNTER_Z = 1.25
OVEN_C = (-2.5, 9.0); OVEN_R = 2.7; OVEN_BASE = 1.4; MOUTH = (-2.5, 6.55, 2.35)      # dome centre, radius, plinth top, the fire
TABLE = (4.6, 3.0, 9.6, 1.3)                    # x centre, y0, y1, top z (table 1.7 D wide)
SMALL_SCALE = (2.4, 0.75, COUNTER_Z)            # foot of the hand balance on the counter
BIG_SCALE = (6.0, 6.0)                          # market: the big balance (pivot z 6.6, pans at x 3 (bread) / 9 (weights))
BIG_PIV_Z = 6.6; BIG_ARM = 3.0; BIG_PAN_DROP = 5.0
PILLORY = (-4.0, 9.5); PLAT_H = 1.0
WELL = (-12.0, -3.0)
FIRE = (1.0, 0.55, 0.22); CANDLE = (1.0, 0.72, 0.38); LAMP_E = 150.0

def _rnd(seed): return random.Random(seed)

# ----------------------------------------------------------------------------- presets
PRESETS = {
    'MORNING': dict(loc='bakery', key=(1.36, 1.10, 0.72), key_dir=G._kd((0.30, 0.95), 30), sun_elev=30, sun_angle=1.2,
                    shade=(0.07, 0.075, 0.21), shade_tint=(0.09, 0.10, 0.30), shade_mix=0.6, lift=(0.006, 0.005, 0.014), form=(0.0, -0.06, 0.25),
                    toon=1.0, key_desat=0.0, ink='#2a1712', night=False, sky='morning', pano='morning', sky_k=0.95, pano_k=0.95, haze=('#f4e8d8', 0.18),
                    grade_offset=(0.003, 0.002, 0.006), grade_saturation=1.15, bloom_size=0.05, fire_k=1.0, shaft_k=0.3),
    'AFTERNOON': dict(loc='bakery', key=(1.52, 0.95, 0.42), key_dir=G._kd((-0.42, 0.91), 22), sun_elev=22, sun_angle=1.0,
                      shade=(0.08, 0.075, 0.21), shade_tint=(0.10, 0.10, 0.30), shade_mix=0.6, lift=(0.007, 0.005, 0.014), form=(0.0, -0.06, 0.25),
                      toon=1.0, key_desat=0.0, ink='#2a1712', night=False, sky='afternoon', pano='afternoon', sky_k=0.95, pano_k=0.95, haze=('#ffcf9a', 0.16),
                      grade_offset=(0.004, 0.002, 0.006), grade_saturation=1.15, bloom_size=0.05, fire_k=0.8, shaft_k=0.3),
    'M_AFTERNOON': dict(loc='market', key=(1.70, 1.06, 0.46), key_dir=G._kd((0.90, 0.42), 26), sun_elev=26, sun_angle=0.6,
                        shade=(0.085, 0.10, 0.32), shade_tint=(0.12, 0.13, 0.46), shade_mix=0.7, lift=(0.008, 0.005, 0.02), form=(0.0, -0.05, 0.22),
                        toon=0.5, key_desat=0.0, ink='#2a1712', night=False, sky='afternoon', pano='afternoon', sky_k=0.95, pano_k=0.95, haze=('#ffc890', 0.06),
                        grade_offset=(0.004, 0.002, 0.008), grade_saturation=1.25, bloom_size=0.05, fire_k=1.0, shaft_k=0.0),
    'M_MORNING': dict(loc='market', key=(1.36, 1.14, 0.80), key_dir=G._kd((-0.92, 0.38), 16), sun_elev=16, sun_angle=1.5,
                      shade=(0.13, 0.16, 0.44), shade_tint=(0.16, 0.18, 0.52), shade_mix=0.7, lift=(0.01, 0.009, 0.02), form=(0.0, -0.05, 0.2),
                      toon=0.6, key_desat=0.0, ink='#2a1712', night=False, sky='morning', pano='morning', sky_k=0.92, pano_k=0.92, haze=('#ece4f0', 0.10),
                      grade_offset=(0.006, 0.005, 0.009), grade_saturation=1.3, bloom_size=0.05, fire_k=0.8, shaft_k=0.0),
}
ALIASES = dict(market=dict(AFTERNOON='M_AFTERNOON', MORNING='M_MORNING'), bakery={})
LOC_PRESETS = dict(bakery=['MORNING', 'AFTERNOON'], market=['AFTERNOON', 'MORNING'])

# ----------------------------------------------------------------------------- material helpers
def _metal(name, hexcol):
    """Copper / brass: dark-gold shade (the pagoda metal rule) so it reads metallic in shade too."""
    P = STATE['P']; m = mat_lit(STATE['pre'] + 'm_' + name, hexcol, form=tuple(P['form']), shade_mul=(2.4, 1.6, 0.55), shade_mix=0.15)
    return _untoon(m) if STATE['loc'] == 'bakery' else m

def _mat_add(name, image, rgb, k, node='k', scroll=False, fade=False):
    """Camera-only additive glow card: emission rgb x k x image alpha. Node `node` (Value) holds k. scroll: the image UV gets a
    Mapping node 'scroll' (location y keyed by set_steam); fade: alpha x sin(pi v) (the wisp thins at both ends)."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); tx = N('ShaderNodeTexImage'); tx.image = T._img(image)
    if scroll:
        uv = N('ShaderNodeUVMap'); mp = N('ShaderNodeMapping'); mp.name = 'scroll'; L(uv.outputs['UV'], mp.inputs['Vector']); L(mp.outputs['Vector'], tx.inputs['Vector'])
        tx.extension = 'REPEAT'
    a = tx.outputs['Alpha']
    if fade:
        uv2 = N('ShaderNodeUVMap'); sp = N('ShaderNodeSeparateXYZ'); L(uv2.outputs['UV'], sp.inputs[0])
        mu = N('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = math.pi; L(sp.outputs['Y'], mu.inputs[0])
        sn = N('ShaderNodeMath'); sn.operation = 'SINE'; L(mu.outputs[0], sn.inputs[0])
        pw = N('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 1.5; L(sn.outputs[0], pw.inputs[0])
        m2 = N('ShaderNodeMath'); m2.operation = 'MULTIPLY'; L(a, m2.inputs[0]); L(pw.outputs[0], m2.inputs[1]); a = m2.outputs[0]
    kv = N('ShaderNodeValue'); kv.name = node; kv.outputs[0].default_value = k
    st = N('ShaderNodeMath'); st.operation = 'MULTIPLY'; L(a, st.inputs[0]); L(kv.outputs[0], st.inputs[1])
    em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*rgb, 1); L(st.outputs[0], em.inputs['Strength'])
    tr = N('ShaderNodeBsdfTransparent'); ad = N('ShaderNodeAddShader'); L(tr.outputs['BSDF'], ad.inputs[0]); L(em.outputs['Emission'], ad.inputs[1])
    lp = N('ShaderNodeLightPath'); tr2 = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    L(lp.outputs['Is Camera Ray'], mx.inputs['Fac']); L(tr2.outputs['BSDF'], mx.inputs[1]); L(ad.outputs['Shader'], mx.inputs[2]); L(mx.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def _mat_steam(name, image):
    """Steam: camera-only soft white wisp, alpha-over (not only additive, so it reads white over the bright crust too)."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = _mat_add(name, image, (1.0, 0.98, 0.95), 0.0, node='steam_k', scroll=True, fade=True)
    nt = m.node_tree; N = nt.nodes.new; L = nt.links.new
    em = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeEmission'][0]; st = em.inputs['Strength'].links[0].from_node
    # alpha-over: mix(transparent, emission 1.6, alpha x k)
    out = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeOutputMaterial'][0]; lp = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeLightPath'][0]
    em.inputs['Strength'].default_value = 1.15; nt.links.remove(em.inputs['Strength'].links[0])
    cl = N('ShaderNodeMath'); cl.operation = 'MINIMUM'; cl.inputs[1].default_value = 1.0; L(st.outputs[0], cl.inputs[0])
    tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); L(cl.outputs[0], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(em.outputs['Emission'], mx.inputs[2])
    tr2 = N('ShaderNodeBsdfTransparent'); mx2 = N('ShaderNodeMixShader'); L(lp.outputs['Is Camera Ray'], mx2.inputs['Fac']); L(tr2.outputs['BSDF'], mx2.inputs[1]); L(mx.outputs['Shader'], mx2.inputs[2])
    L(mx2.outputs['Shader'], out.inputs['Surface'])
    return m

def _light(name, loc, rgb, energy, radius=0.08, shadow=True):
    name = 'L_' + name; ob = MN._light(name, loc, rgb, energy, radius)
    ob.data.use_shadow = shadow
    return ob

# ----------------------------------------------------------------------------- local-frame helper (houses, stalls)
class Frame:
    """Local frame: origin o, yaw (deg) - local +x along the front, local -y = the way the front faces, z up."""
    def __init__(s, o, yaw):
        s.o = Vector((o[0], o[1], o[2] if len(o) > 2 else 0.0)); a = math.radians(yaw)
        s.X = Vector((math.cos(a), math.sin(a), 0)); s.Y = Vector((-math.sin(a), math.cos(a), 0)); s.Z = Vector((0, 0, 1))
    def p(s, x, y, z): return s.o + s.X * x + s.Y * y + s.Z * z
    def box(s, mb, lo, hi, mat, uvk=1.0):
        c = s.p((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2)
        obox(mb, c, s.X, s.Y, s.Z, (hi[0] - lo[0]) / 2, (hi[1] - lo[1]) / 2, (hi[2] - lo[2]) / 2, mat, uvk)
    def quad(s, mb, pts, mat, uvs, normal):
        n = s.X * normal[0] + s.Y * normal[1] + s.Z * normal[2]
        mb.oface([s.p(*q) for q in pts], mat, uvs, n)

def _bake_loaf(mb, c, r, mat, seed, squash=0.62, long=1.0, yaw=0.0):
    """A round (long > 1: oval) loaf: squashed lumpy sphere with the crust wrap (u round, v base -> crown)."""
    c = Vector(c); rr = _rnd(seed); seg, rings = 12, 6; R = []; mb.pid += 1; ca, sa = math.cos(yaw), math.sin(yaw)
    for k in range(rings + 1):
        th = math.pi * 0.5 * k / rings                                      # 0 at the base rim .. pi/2 at the crown
        row = []
        for i in range(seg):
            ph = 2 * math.pi * i / seg; x = math.cos(th) * math.cos(ph) * long; y = math.cos(th) * math.sin(ph)
            bulge = 1 + 0.06 * (vnoise(3 * math.cos(ph) + seed, 3 * math.sin(ph) + k, seed) - 0.5)
            z = math.sin(th) * squash
            row.append(c + Vector(((x * ca - y * sa) * r * bulge, (x * sa + y * ca) * r * bulge, z * r)))
        R.append(row)
    for k in range(rings):
        for i in range(seg):
            j = (i + 1) % seg
            mb.face([R[k][i], R[k][j], R[k + 1][j], R[k + 1][i]], mat, [(2 * i / seg, k / rings), (2 * (i + 1) / seg, k / rings), (2 * (i + 1) / seg, (k + 1) / rings), (2 * i / seg, (k + 1) / rings)])
    mb.face(R[0][::-1], mat, [(0.5, 0.0)] * seg)

def _basket(mb, c, r, h, M, loaves=0, seed=0, handle=False):
    """Wicker basket (open cylinder, rim, two weave bands) with loaves heaped in it."""
    c = Vector(c); rod(mb, c, c + Vector((0, 0, h)), r, M['basket'], seg=14, r1=r * 1.15)
    rod(mb, c + Vector((0, 0, h - 0.04)), c + Vector((0, 0, h + 0.03)), r * 1.2, M['basket_d'], seg=14)
    for z in (0.3, 0.65): rod(mb, c + Vector((0, 0, h * z)), c + Vector((0, 0, h * z + 0.05)), r * (1 + 0.15 * z) + 0.01, M['basket_d'], seg=14)
    rr = _rnd(seed)
    for i in range(loaves):
        a = 2 * math.pi * i / max(1, loaves) + rr.uniform(0, 0.4); d = r * 0.5 * (i % 2 + 0.3)
        _bake_loaf(mb, c + Vector((d * math.cos(a), d * math.sin(a), h * 0.75 + 0.08 * (i % 3))), r * 0.42, rr.choice((M['loaf'], M['loaf_d'], M['loaf_p'])), seed * 10 + i)
    if handle:
        pts = [c + Vector((r * 1.1 * math.cos(t), 0, h + r * 0.9 * math.sin(t))) for t in [math.pi * k / 8 for k in range(9)]]
        chain_rod(mb, pts, 0.035, M['basket_d'])

def _candle(mb, fl, base, M, h=0.45, r=0.06, holder=True):
    """Candle on an iron pricket / dish; flame (emission) into fl; returns the flame centre."""
    b = Vector(base)
    if holder:
        rod(mb, b, b + Vector((0, 0, 0.05)), r * 2.6, M['iron'], seg=10); rod(mb, b + Vector((0, 0, 0.05)), b + Vector((0, 0, 0.09)), r * 1.4, M['iron'], seg=8)
        b = b + Vector((0, 0, 0.09))
    rod(mb, b, b + Vector((0, 0, h)), r, M['candle'], seg=8)
    lumpy(mb, b + Vector((0, 0, h * 0.85)), r * 1.1, M['candle'], 7, seg=6, rings=4, rough=0.3, squash=0.5)
    f = b + Vector((0, 0, h + 0.1))
    fl.frustum(f - Vector((0, 0, 0.08)), f + Vector((0, 0, 0.14)), 0.045, 0.0, M['flame'], seg=6, cap1=False)
    fl.sphere(f - Vector((0, 0, 0.02)), 0.032, M['flame_c'], seg=6, rings=3)
    return f

def _halo(hb, c, r, M, key='halo'):
    """Camera-only glow disc (additive radial) facing +-y and +-x (crossed), around a flame."""
    c = Vector(c)
    for (u, v) in ((Vector((1, 0, 0)), Vector((0, 0, 1))), (Vector((0, 1, 0)), Vector((0, 0, 1)))):
        hb.face([c - u * r - v * r, c + u * r - v * r, c + u * r + v * r, c - u * r + v * r], M[key], [(0, 0), (1, 0), (1, 1), (0, 1)])

# ----------------------------------------------------------------------------- build
def build(location='bakery', preset=None, clear=True, dress=True):
    """Build one location ('bakery' | 'market') with a light preset (bakery: MORNING | AFTERNOON; market: AFTERNOON | MORNING) into
    the current scene (collections SET and LIGHTS, world, render settings, grade, denoiser). Returns the anchors dict (bakery_API.md)."""
    preset = preset or LOC_PRESETS[location][0]
    assert preset in LOC_PRESETS[location], 'preset %s is not one of %s' % (preset, LOC_PRESETS[location])
    key = ALIASES[location].get(preset, preset)
    scene = bpy.context.scene; P = dict(PRESETS[key]); STATE.clear(); STATE['P'] = P; STATE['preset'] = preset; STATE['loc'] = location
    if clear:
        for ob in list(scene.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for ac in list(bpy.data.actions): bpy.data.actions.remove(ac)
    for me in list(bpy.data.meshes):
        if me.users == 0: bpy.data.meshes.remove(me)
    for li in list(bpy.data.lights):
        if li.users == 0: bpy.data.lights.remove(li)
    SET = T._coll('SET', scene); LIGHTS = T._coll('LIGHTS', scene); T._wipe(SET); T._wipe(LIGHTS); STATE['SET'] = SET; STATE['LIGHTS'] = LIGHTS
    for m in list(bpy.data.materials):
        if m.name.startswith(('BKY_', 'ink')): bpy.data.materials.remove(m)
    tx = BT.ensure(verbose=False); STATE['tx'] = tx
    w = bpy.data.worlds.get('W_bakery') or bpy.data.worlds.new('W_bakery'); scene.world = w; nt = T._tree(w)
    bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld'); bg.inputs['Color'].default_value = (0, 0, 0, 1); bg.inputs['Strength'].default_value = 0.0
    nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
    setup_render(scene, 'final'); scene.frame_start = 1; scene.frame_current = 1
    pre = 'BKY_%s_%s_' % (location[0], preset); FORM = tuple(P['form']); inside = location == 'bakery'
    def _k(v): return 'x'.join('%g' % x for x in v) if isinstance(v, (tuple, list)) else '%g' % v
    def fin(m): return _untoon(m) if inside else m
    def C(hexcol, gain=1.0, sm=1.0, form=True):
        return fin(mat_lit('%sc_%s_%g_%s_%d' % (pre, hexcol.lstrip('#'), gain, _k(sm), form), hexcol, gain=gain, shade_mul=sm, form=FORM if form else None))
    def TX(name, gain=1.0, sm=1.0, form=True, alpha=False):
        return fin(mat_lit('%st_%s_%g_%s_%d_%d' % (pre, name, gain, _k(sm), form, alpha), image=tx[name], gain=gain, shade_mul=sm, form=FORM if form else None, alpha=alpha))
    def E(name, image=None, hexcol='#ffffff', k=1.0, alpha=False): return mat_emit(pre + 'e_' + name, hexcol, image=tx[image] if image else None, strength=k, alpha=alpha)
    STATE.update(C=C, TX=TX, E=E, pre=pre)
    M = _materials(P, C, TX, E, tx, pre); STATE['M'] = M
    kd = Vector(P['key_dir']).normalized(); k = max(P['key'])
    d = bpy.data.lights.new('key_sun', 'SUN'); d.color = tuple(x / k for x in P['key']); d.energy = math.pi * k; d.angle = math.radians(P['sun_angle'])
    sun = bpy.data.objects.new('key_sun', d); LIGHTS.objects.link(sun); sun.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler(); sun.location = (-20, -40, 40); STATE['sun'] = sun
    STATE['fire_lights'] = []; STATE['fire_mats'] = []; STATE['steam'] = []
    if inside: _bakery(SET, P, M, dress)
    else: _market(SET, P, M, dress)
    _sky(SET, P, M, tx, pre, E, R_pano=BT.PANO_R)
    scene.cycles.use_light_tree = False
    MN._denoise(scene)
    setup_grade(scene)
    for ob in SET.objects:
        no_bounce(ob)
    set_steam(0.0 if not inside else 0.8); set_oven(1.0); set_scale(0.0) if inside else None
    if not inside: set_big_scale(0.0); set_loaves(12)
    A = anchors(); STATE['A'] = A
    return A

def setup_render(scene, quality='final'):
    """tower.setup_render (final 720x1280 12 samples / preview 360x640 6, 2 threads, direct light only) + OpenImageDenoise, light tree
    off (= mine.setup_render). No depth of field."""
    MN.setup_render(scene, quality)

def apply_dof(cam_name=None, scene=None, cam=None):
    """Client rule: no depth of field at all. Kept for API symmetry with mine / pagoda: always switches DOF off."""
    return None

def _materials(P, C, TX, E, tx, pre):
    inside = STATE['loc'] == 'bakery'
    M = dict(stone=TX('stone_w'), stone_x=TX('stone_ext'), plaster=TX('plaster_in'), plaster_x=TX('plaster_ext'), brick=TX('brick_oven'), brick_s=TX('brick_soot'),
             flags=TX('flags', form=False), flags_c=TX('flags_clean', form=False), timber=TX('timber_b'), timber_l=TX('timber_l'), table=TX('table'), shelf=TX('shelf'),
             counter=TX('counter'), floorb=TX('floorb'), sack=TX('sack'), sack_p=TX('sack_plain'),
             loaf=_glossy(TX('loaf'), (1.0, 0.85, 0.6), 0.18, 0.35), loaf_d=_glossy(TX('loaf_dark'), (1.0, 0.85, 0.6), 0.18, 0.35), loaf_p=TX('loaf_pale'),
             copper=_glossy(_metal('copper', '#c8703a'), (1.0, 0.7, 0.45), 0.9, 0.2), brass=_glossy(_metal('brass', '#c0923e'), (1.0, 0.82, 0.5), 0.5, 0.22),
             iron=_glossy(C('#3a3640', 1.0, 1.1), (1.0, 0.9, 0.8), 0.3, 0.3), candle=C('#f2e8cc'), dough=C('#f2dfb4'), flour=C('#f6f0e2'), basket=C('#c49450'), basket_d=C('#8a6034'),
             wood=C('#9a6a3e'), wood_d=C('#6a4a2c'), rope=C('#b89a6a'), cloth_r=TX('cloth_red'), cloth_b=TX('cloth_blue'), cloth_g=TX('cloth_green'), linen=C('#ece2cc'),
             roof=TX('roof_tile'), roof2=TX('roof_tile2'), thatch=TX('thatch'), cobbles=TX('cobbles', form=False), crate=TX('crate'), log=TX('log_end'),
             herbs=TX('herbs', alpha=True), herbs2=TX('herbs2', alpha=True), onions=TX('onions', alpha=True), wheat=TX('wheat', alpha=True), leaded=TX('leaded', alpha=True),
             notice=TX('notice', alpha=True), fascia=TX('fascia'), red=C('#b8402e'), green=C('#3a6a46'), blue=C('#34508a'), cream=C('#ece0c4'), black=C('#2a2428'), water=_glossy(C('#2a3a50', 1.0, 0.8), (1, 1, 1), 0.7, 0.05),
             cabbage=C('#7aa84e'), cabbage_d=C('#5a8a3e'), tomato=C('#d8402a'), apple=C('#c8402e'), apple_g=C('#9ab84a'), turnip=C('#e4d8e0'), carrot=C('#e8822a'), onion=C('#c8883a'),
             rotten=C('#6a7a3a'), hay=TX('thatch'), pewter=_glossy(C('#9a9aa4'), (1, 1, 1), 0.5, 0.2),
             flame=mat_emit(pre + 'e_flame', '#ffa848', strength=6.0), flame_c=mat_emit(pre + 'e_flamec', '#fff2c4', strength=10.0),
             fire=mat_emit(pre + 'e_fire', image=tx['fire'], strength=4.0, alpha=True), embers=mat_emit(pre + 'e_embers', image=tx['embers'], strength=2.6),
             halo=_mat_add(pre + 'halo', tx['pool'], (1.0, 0.62, 0.3), 0.55), halo_big=_mat_add(pre + 'halo_big', tx['pool'], (1.0, 0.5, 0.2), 1.1, node='fire_glow'),
             pool=_mat_add(pre + 'pool', tx['pool'], (1.0, 0.6, 0.3), 0.6, node='pool_k'),
             shaft=_mat_add(pre + 'shaft', tx['shaft'], tuple(c / max(P['key']) for c in P['key']), P.get('shaft_k', 0.15), node='shaft_k'),
             steam=_mat_steam(pre + 'steam', tx['steam']), steam2=_mat_steam(pre + 'steam2', tx['steam2']),
             win_lit=E('winlit', hexcol='#ffb860', k=1.4), glow_in=E('glow_in', hexcol='#ff9a48', k=1.6), dark=C('#2a1e18', 1.0, 0.6, form=False))
    for nm in ('sign_bread', 'sign_pretzel', 'sign_tankard', 'sign_boot', 'sign_fish'): M[nm] = TX(nm)
    for nm in ('ban_king', 'ban_town', 'ban_guild', 'awn_red', 'awn_green', 'awn_blue', 'awn_yellow'): M[nm] = TX(nm, alpha=True)
    for v in range(4):
        M['ht%d_g' % v] = TX('ht%d_g' % v); M['ht%d_u' % v] = TX('ht%d_u' % v); M['ht%d_gab' % v] = TX('ht%d_gab' % v, alpha=True)
    M['bk_u'] = TX('bk_u'); M['bk_gab'] = TX('bk_gab', alpha=True)
    M.update(cloth_red=M['cloth_r'], cloth_blue=M['cloth_b'], cloth_green=M['cloth_g'])
    STATE['fire_mats'] = [M['fire'], M['embers']]
    return M

def _sky(SET, P, M, tx, pre, E, R_pano=120.0):
    """Painted backdrop ring (R 120), sky dome (R 140) and warm haze rings (camera-only), as mine's pithead."""
    mb = MB(); R = R_pano; seg = 128
    for i in range(seg):
        a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; u0, u1 = i / seg, (i + 1) / seg
        mb.face([Vector((R * math.cos(a0), R * math.sin(a0), BT.PANO_Z0)), Vector((R * math.cos(a1), R * math.sin(a1), BT.PANO_Z0)), Vector((R * math.cos(a1), R * math.sin(a1), BT.PANO_Z1)), Vector((R * math.cos(a0), R * math.sin(a0), BT.PANO_Z1))],
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
        for Rh in (34.0, 60.0, 95.0):
            for i in range(64):
                a0, a1 = 2 * math.pi * i / 64, 2 * math.pi * (i + 1) / 64
                mb.face([Vector((Rh * math.cos(a0), Rh * math.sin(a0), -1)), Vector((Rh * math.cos(a1), Rh * math.sin(a1), -1)), Vector((Rh * math.cos(a1), Rh * math.sin(a1), 40)), Vector((Rh * math.cos(a0), Rh * math.sin(a0), 40))], hm)
        o = _obj(mb, 'haze', SET, shadow=False)

# ============================================================================= houses (both locations)
def house(SET, name, origin, yaw, w, v, M, d=7.0, h1=3.6, h2=3.4, jetty=0.6, gable=True, sign=None, shop_glow=False, third=False, seed=0, chimney=True):
    """A jettied timber-framed house in a local frame (origin = front-left corner at the ground, front faces local -y): ground storey
    (facade ht<v>_g), jettied upper storey (ht<v>_u) with its bressumer beam and brackets, optional third storey, a front gable
    (ht<v>_gab) or a side-gable roof, chimney, hanging sign on an iron bracket. Returns the frame."""
    F = Frame(origin, yaw); mb = MB(); rr = _rnd(seed)
    if v == 'bk': g, u, gab = M['ht0_g'], M['bk_u'], M['bk_gab']
    else: g, u, gab = M['ht%d_g' % v], M['ht%d_u' % v], M['ht%d_gab' % v]
    if not shop_glow:
        F.quad(mb, [(0, 0, 0), (w, 0, 0), (w, 0, h1), (0, 0, h1)], g, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
    for (x, n) in ((0, -1), (w, 1)):
        F.quad(mb, [(x, 0, 0), (x, d, 0), (x, d, h1), (x, 0, h1)], M['plaster_x'], [(0, 0), (d / 4, 0), (d / 4, h1 / 4), (0, h1 / 4)], (n, 0, 0))
    zs = [(h1, h1 + h2, -jetty, u)]
    if third: zs.append((h1 + h2, h1 + 2 * h2 - 0.2, -2 * jetty, u))
    for (z0, z1, y0, mat) in zs:
        F.quad(mb, [(0, y0, z0), (w, y0, z0), (w, y0, z1), (0, y0, z1)], mat, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
        F.quad(mb, [(0, y0, z0), (w, y0, z0), (w, 0, z0), (0, 0, z0)], M['timber'], [(0, 0), (w / 2, 0), (w / 2, 0.3), (0, 0.3)], (0, 0, -1))
        for (x, n) in ((0, -1), (w, 1)):
            F.quad(mb, [(x, y0, z0), (x, d, z0), (x, d, z1), (x, y0, z1)], M['plaster_x'], [(0, 0), (d / 4, 0), (d / 4, (z1 - z0) / 4), (0, (z1 - z0) / 4)], (n, 0, 0))
        F.box(mb, (-0.08, y0 - 0.12, z0 - 0.28), (w + 0.08, y0 + 0.12, z0 + 0.02), M['timber'], 0.5)            # bressumer
        for x in [0.15 + (w - 0.3) * i / 3 for i in range(4)]:                                                    # brackets
            p0 = F.p(x, y0 + 0.1, z0 - 0.25); p1 = F.p(x, 0.0, z0 - 1.0); beam(mb, p0, p1, 0.16, 0.16, M['timber'])
    ztop = zs[-1][1]; yf = zs[-1][2]
    if gable:
        rh = w * 0.62
        F.quad(mb, [(0, yf, ztop), (w, yf, ztop), (w, yf, ztop + rh), (0, yf, ztop + rh)], gab, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
        for s in (0, 1):
            xa = 0 if s == 0 else w
            pts = [(xa - (0.35 if s == 0 else -0.35), yf - 0.45, ztop - 0.22), (xa - (0.35 if s == 0 else -0.35), d + 0.3, ztop - 0.22), (w / 2, d + 0.3, ztop + rh + 0.1), (w / 2, yf - 0.45, ztop + rh + 0.1)]
            F.quad(mb, pts, M['roof'] if v != 2 else M['thatch'], [(0, 0), ((d + 0.75) / 2, 0), ((d + 0.75) / 2, 2.2), (0, 2.2)], (-1 if s == 0 else 1, 0, 1.2))
        bb = [F.p(-0.3, yf - 0.47, ztop - 0.2), F.p(w / 2, yf - 0.47, ztop + rh + 0.1), F.p(w + 0.3, yf - 0.47, ztop - 0.2)]
        beam(mb, bb[0], bb[1], 0.12, 0.2, M['timber']); beam(mb, bb[1], bb[2], 0.12, 0.2, M['timber'])
        rod(mb, F.p(w / 2, yf - 0.47, ztop + rh + 0.1), F.p(w / 2, yf - 0.47, ztop + rh + 0.8), 0.06, M['timber'], seg=6)
    else:
        rh = 2.6
        F.quad(mb, [(-0.2, yf - 0.6, ztop - 0.15), (w + 0.2, yf - 0.6, ztop - 0.15), (w + 0.2, d / 2, ztop + rh), (-0.2, d / 2, ztop + rh)], M['roof2'] if v != 1 else M['thatch'],
               [(0, 0), (w / 2, 0), (w / 2, (d / 2 + 0.6) / 2.2), (0, (d / 2 + 0.6) / 2.2)], (0, -1, 1.4))
        F.quad(mb, [(-0.2, d + 0.3, ztop - 0.15), (w + 0.2, d + 0.3, ztop - 0.15), (w + 0.2, d / 2, ztop + rh), (-0.2, d / 2, ztop + rh)], M['roof2'], [(0, 0), (w / 2, 0), (w / 2, 2), (0, 2)], (0, 1, 1.4))
        for x in (0, w):
            F.quad(mb, [(x, yf, ztop), (x, d, ztop), (x, d / 2, ztop + rh)], M['plaster_x'], [(0, 0), (1, 0), (0.5, 0.6)], (-1 if x == 0 else 1, 0, 0))
    if chimney and rr.random() < 0.8:
        cx_ = w * rr.choice((0.25, 0.75)); F.box(mb, (cx_ - 0.4, d * 0.55, ztop), (cx_ + 0.4, d * 0.55 + 0.8, ztop + rh + 1.4), M['stone_x'], 0.5)
        F.box(mb, (cx_ - 0.5, d * 0.55 - 0.1, ztop + rh + 1.3), (cx_ + 0.5, d * 0.55 + 0.9, ztop + rh + 1.5), M['stone_x'], 0.5)
    if sign:
        bx = w - 0.6 if sign[1] > 0 else 0.6; z = h1 + 1.0
        p0 = F.p(bx, yf - 0.1, z); p1 = F.p(bx, yf - 1.9, z); rod(mb, p0, p1, 0.04, M['iron'], seg=6)
        rod(mb, F.p(bx, yf - 0.1, z - 0.6), F.p(bx, yf - 1.2, z), 0.03, M['iron'], seg=6)
        for k in range(8):                                                                                   # scroll curl
            a0, a1 = k / 8 * 5.5, (k + 1) / 8 * 5.5; rr_ = 0.25 * (1 - k / 10)
            rod(mb, F.p(bx, yf - 1.6 + rr_ * math.cos(a0), z + 0.3 + rr_ * math.sin(a0)), F.p(bx, yf - 1.6 + rr_ * math.cos(a1), z + 0.3 + rr_ * math.sin(a1)), 0.025, M['iron'], seg=5)
        for yy in (-0.55, -1.7): rod(mb, F.p(bx, yf + yy, z), F.p(bx, yf + yy, z - 0.25), 0.015, M['iron'], seg=4)
        sw, sh = 1.4, 1.05; sm = M[sign[0]]
        for (off, n) in ((-0.03, -1), (0.03, 1)):
            F.quad(mb, [(bx + off, yf - 0.4, z - 0.25 - sh), (bx + off, yf - 0.4 - sw, z - 0.25 - sh), (bx + off, yf - 0.4 - sw, z - 0.25), (bx + off, yf - 0.4, z - 0.25)], sm,
                   [(0, 0), (1, 0), (1, 1), (0, 1)] if n < 0 else [(1, 0), (0, 0), (0, 1), (1, 1)], (n, 0, 0))
        F.box(mb, (bx - 0.025, yf - 0.4 - sw, z - 0.25 - sh), (bx + 0.025, yf - 0.4, z - 0.25), M['wood_d'])
    _obj(mb, name, SET, hull=0.025)
    return F

def bakery_front(SET, name, F, w, M, sign='sign_bread', open_door=True, h1=3.6, seed=0):
    """Ground storey of a bakery seen from the street (market): plaster + timber framing in 3D, the shop opening with its let-down shutter
    board (counter) heaped with loaves and baskets, the warm glowing oven room inside (emission back wall + the fire), and an open door."""
    mb = MB(); gl = MB(); rr = _rnd(seed)
    ox0, ox1, oz0, oz1 = 0.8, w - 2.2, 1.25, 3.0; dx0, dx1 = w - 1.7, w - 0.5
    def wall(a, b, z0, z1):
        F.quad(mb, [(a, 0, z0), (b, 0, z0), (b, 0, z1), (a, 0, z1)], M['plaster_x'], [(a / 4, z0 / 4), (b / 4, z0 / 4), (b / 4, z1 / 4), (a / 4, z1 / 4)], (0, -1, 0))
    wall(0, dx0, 0, oz0); wall(dx1, w, 0, oz0); wall(0, w, oz1, h1); wall(0, ox0, oz0, oz1); wall(ox1, dx0, oz0, oz1); wall(dx1, w, oz0, oz1)
    for x in (0.0, ox0 - 0.1, ox1, dx0 - 0.12, dx1, w - 0.16): F.box(mb, (x, -0.1, 0), (x + 0.16, 0.05, h1), M['timber'], 0.5)
    F.box(mb, (0, -0.12, oz1), (w, 0.05, oz1 + 0.18), M['timber'], 0.5); F.box(mb, (0, -0.12, oz0 - 0.18), (dx0 - 0.1, 0.05, oz0), M['timber'], 0.5)
    for x in (0.4, w * 0.5): beam(mb, F.p(x, -0.05, oz1 + 0.2), F.p(x + 0.5, -0.05, h1 - 0.1), 0.1, 0.12, M['timber'])
    # recess (oven room) behind the opening and the door
    for (a, b, z0, z1) in ((ox0, ox1, oz0, oz1), (dx0, dx1, 0.0, oz1)):
        F.quad(mb, [(a, 0, z0), (a, 1.6, z0), (a, 1.6, z1), (a, 0, z1)], M['dark'], [(0, 0)] * 4, (1, 0, 0))
        F.quad(mb, [(b, 0, z0), (b, 1.6, z0), (b, 1.6, z1), (b, 0, z1)], M['dark'], [(0, 0)] * 4, (-1, 0, 0))
        F.quad(mb, [(a, 0, z1), (b, 0, z1), (b, 1.6, z1), (a, 1.6, z1)], M['dark'], [(0, 0)] * 4, (0, 0, -1))
        F.quad(gl, [(a, 1.6, z0), (b, 1.6, z0), (b, 1.6, z1), (a, 1.6, z1)], M['glow_in'], [(0, 0)] * 4, (0, -1, 0))
    F.quad(mb, [(dx0, 0, 0.001), (dx1, 0, 0.001), (dx1, 1.6, 0.001), (dx0, 1.6, 0.001)], M['flags_c'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, 1))
    # fire glimpse inside (oven mouth in the back of the recess)
    fx = (ox0 + ox1) / 2
    F.quad(gl, [(fx - 0.6, 1.55, oz0 + 0.1), (fx + 0.6, 1.55, oz0 + 0.1), (fx + 0.6, 1.55, oz0 + 0.9), (fx - 0.6, 1.55, oz0 + 0.9)], M['fire'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
    # open door leaf, swung in
    F.box(mb, (dx1 - 0.08, 0.05, 0.02), (dx1 - 0.02, 1.25, oz1 - 0.05), M['wood_d'])
    # shutter board / counter on chains
    F.box(mb, (ox0 - 0.1, -1.1, oz0 - 0.08), (ox1 + 0.1, 0.0, oz0), M['counter'], 0.5)
    for x in (ox0, ox1): chain_rod(mb, [F.p(x, -1.05, oz0), F.p(x, -0.05, oz1 - 0.1)], 0.02, M['iron'])
    for x in (ox0 + 0.2, ox1 - 0.2): rod(mb, F.p(x, -0.95, 0), F.p(x, -0.95, oz0 - 0.08), 0.06, M['wood_d'], seg=6)
    n = int((ox1 - ox0) / 0.55)
    for i in range(n):
        x = ox0 + 0.35 + i * (ox1 - ox0 - 0.7) / max(1, n - 1)
        if i % 3 == 1: _basket(mb, F.p(x, -0.55, oz0), 0.28, 0.22, M, loaves=4, seed=seed + i)
        else:
            for j in range(3): _bake_loaf(mb, F.p(x + 0.12 * (j - 1), -0.55 + 0.25 * (j % 2), oz0 + 0.02 + 0.12 * (j == 1)), 0.2, rr.choice((M['loaf'], M['loaf_d'], M['loaf_p'])), seed * 31 + i * 3 + j)
    o = _obj(mb, name, SET, hull=0.02); g = _obj(gl, name + '_glow', SET, shadow=False)
    return o

# ============================================================================= BAKERY (interior)
def _bakery(SET, P, M, dress):
    x0, x1, y0, y1 = ROOM
    # ---- floor, ceiling, beams
    mb = MB()
    mb.quad((x0, y0, 0), (x1 - x0, 0, 0), (0, y1 - y0, 0), M['flags'], (x0 / 4, y0 / 4, x1 / 4, y1 / 4))
    mb.quad((x0, y1, CEIL), (x1 - x0, 0, 0), (0, -(y1 - y0), 0), M['floorb'], (0, 0, (x1 - x0) / 2, (y1 - y0) / 2))
    _obj(mb, 'floor_ceiling', SET)
    mb = MB()
    for yb in (1.6, 4.0, 6.4, 8.8):
        obox(mb, (0, yb, CEIL - 0.3), (1, 0, 0), (0, 1, 0), (0, 0, 1), (x1 - x0) / 2, 0.28, 0.3, M['timber'], 0.5)
    for xb in (-4.5, 0.0, 4.5):
        obox(mb, (xb, (y0 + y1) / 2, CEIL - 0.72), (0, 1, 0), (1, 0, 0), (0, 0, 1), (y1 - y0) / 2, 0.2, 0.12, M['timber_l'], 0.5)
    # posts along the side walls + braces
    for y in (0.6, 4.0, 7.5, 10.6):
        for x in (x0 + 0.2, x1 - 0.2):
            obox(mb, (x, y, CEIL / 2), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.2, 0.2, CEIL / 2, M['timber'], 0.5)
    for (xa, ya, yb) in ((x0 + 0.25, 4.0, 2.4), (x0 + 0.25, 7.5, 9.1), (x1 - 0.25, 4.0, 2.4), (x1 - 0.25, 7.5, 9.1)):
        beam(mb, (xa, ya, CEIL - 2.0), (xa, yb, CEIL - 0.6), 0.16, 0.16, M['timber'], up=(1, 0, 0))
    _obj(mb, 'beams', SET, hull=0.02)
    # ---- walls: side walls (stone plinth + plaster), back wall (stone), front wall with openings
    mb = MB()
    for (x, n) in ((x0, 1), (x1, -1)):
        mb.oface([(x, y0, 0), (x, y1, 0), (x, y1, 1.2), (x, y0, 1.2)], M['stone'], [(y0 / 4, 0), (y1 / 4, 0), (y1 / 4, 0.3), (y0 / 4, 0.3)], (n, 0, 0))
        mb.oface([(x, y0, 1.2), (x, y1, 1.2), (x, y1, CEIL), (x, y0, CEIL)], M['plaster'], [(y0 / 4, 1 - 0.3), (y1 / 4, 1 - 0.3), (y1 / 4, 1 - CEIL / 4 - 0.3), (y0 / 4, 1 - CEIL / 4 - 0.3)], (n, 0, 0))
    mb.oface([(x0, y1, 0), (x1, y1, 0), (x1, y1, CEIL), (x0, y1, CEIL)], M['stone'], [(x0 / 4, 0), (x1 / 4, 0), (x1 / 4, CEIL / 4), (x0 / 4, CEIL / 4)], (0, -1, 0))
    _obj(mb, 'walls', SET)
    _front_wall(SET, M)
    _oven(SET, P, M)
    _table(SET, M); _racks(SET, M); _counter(SET, M)
    if dress: _bakery_dressing(SET, M)
    _lights_inside(SET, P, M)
    _street(SET, M)
    _steam_build(SET, M)

def _front_wall(SET, M):
    """Front wall y -0.5..0 with three openings: the counter opening (shutter board let down outside), the half door, the leaded window.
    Interior face plaster, exterior face plaster + timber framing; reveals in timber. Upper jettied storey and gable roof outside."""
    x0, x1 = ROOM[0], ROOM[1]; yi, yo = 0.0, -WALL_T; mb = MB(); ex = MB()
    ops = [COUNTER_OPEN, DOOR_OPEN, WIN_OPEN]
    # x breakpoints, fill every cell of the grid that is not inside an opening
    xs = sorted(set([x0, x1] + [o[0] for o in ops] + [o[1] for o in ops])); zs = sorted(set([0.0, CEIL] + [o[2] for o in ops] + [o[3] for o in ops]))
    for i in range(len(xs) - 1):
        for j in range(len(zs) - 1):
            a, b, c, d = xs[i], xs[i + 1], zs[j], zs[j + 1]; mx, mz = (a + b) / 2, (c + d) / 2
            if any(o[0] < mx < o[1] and o[2] < mz < o[3] for o in ops): continue
            mb.oface([(a, yi, c), (b, yi, c), (b, yi, d), (a, yi, d)], M['plaster'], [(a / 4, 1 - d / 4), (b / 4, 1 - d / 4), (b / 4, 1 - c / 4), (a / 4, 1 - c / 4)], (0, 1, 0))
            ex.oface([(a, yo, c), (b, yo, c), (b, yo, d), (a, yo, d)], M['plaster_x'], [(a / 4, c / 4), (b / 4, c / 4), (b / 4, d / 4), (a / 4, d / 4)], (0, -1, 0))
    for (a, b, c, d) in ops:                                                                     # reveals
        for (pts, n) in (([(a, yo, c), (a, yi, c), (a, yi, d), (a, yo, d)], (1, 0, 0)), ([(b, yo, c), (b, yi, c), (b, yi, d), (b, yo, d)], (-1, 0, 0)),
                         ([(a, yo, d), (b, yo, d), (b, yi, d), (a, yi, d)], (0, 0, -1)), ([(a, yo, c), (b, yo, c), (b, yi, c), (a, yi, c)], (0, 0, 1))):
            mb.oface(pts, M['timber_l'], [(0, 0), (1, 0), (1, 0.3), (0, 0.3)], n)
    _obj(mb, 'front_wall_in', SET);
    # exterior framing (posts, rails, braces) proud of the outside face
    fr = MB(); yf = yo - 0.06
    for x in (x0, -4.8, DOOR_OPEN[1], COUNTER_OPEN[0] - 0.18, COUNTER_OPEN[1], WIN_OPEN[0] - 0.18, WIN_OPEN[1], x1 - 0.18):
        fr.box((x, yf - 0.08, 0), (x + 0.18, yo, CEIL), M['timber'], tile=(0.5, 0.5))
    for z in (CEIL - 0.25, 4.1, 1.07):
        segs = [(x0, x1)] if z != 1.07 else [(x0, DOOR_OPEN[0]), (DOOR_OPEN[1], x1)]
        for (a, b) in segs: fr.box((a, yf - 0.08, z), (b, yo, z + 0.2), M['timber'], tile=(0.5, 0.5))
    for (a, b) in ((x0 + 0.2, -4.8), (WIN_OPEN[1] + 0.2, x1 - 0.2)):
        beam(fr, (a, yf - 0.04, 4.3), (b, yf - 0.04, CEIL - 0.3), 0.14, 0.12, M['timber'], up=(0, 1, 0)); beam(fr, (b, yf - 0.04, 4.3), (a, yf - 0.04, CEIL - 0.3), 0.14, 0.12, M['timber'], up=(0, 1, 0))
    beam(fr, (x0 + 0.2, yf - 0.04, 1.3), (-4.8, yf - 0.04, 4.0), 0.14, 0.12, M['timber'], up=(0, 1, 0))
    # half door: lower leaf closed, upper leaf open outward against the wall
    a, b = DOOR_OPEN[0], DOOR_OPEN[1]
    fr.box((a + 0.02, -0.3, 0.02), (b - 0.02, -0.2, 2.0), M['wood_d'], tile=(0.5, 0.5))
    for z in (0.35, 1.6): fr.box((a + 0.05, -0.36, z), (b - 0.05, -0.3, z + 0.1), M['iron'])
    fr.box((a - 1.75, yf - 0.16, 2.1), (a - 0.05, yf - 0.08, 4.2), M['wood_d'], tile=(0.5, 0.5))
    # leaded window glass + mullion
    a, b, c, d = WIN_OPEN
    fr.quad((a, -0.25, c), (b - a, 0, 0), (0, 0, d - c), M['leaded'], (0, 0, 1.6, 1.8))
    fr.box(((a + b) / 2 - 0.05, -0.3, c), ((a + b) / 2 + 0.05, -0.2, d), M['timber'])
    # counter shutter board let down outside, on chains, and the inside counter-sill
    a, b, c, d = COUNTER_OPEN
    fr.box((a - 0.1, -1.55, c - 0.1), (b + 0.1, yo, c), M['counter'], tile=(2, 2))
    for x in (a, b): chain_rod(fr, catenary((x, -1.5, c), (x, yo - 0.05, d - 0.1), 0.05, 6), 0.025, M['iron'])
    for x in (a + 0.3, b - 0.3): rod(fr, (x, -1.35, 0), (x, -1.35, c - 0.1), 0.07, M['wood_d'], seg=6)
    fr.box((COUNTER_OPEN[0] - 0.15, yf - 0.16, 4.38), (COUNTER_OPEN[1] + 0.15, yf - 0.08, 5.32), M['wood_d'])
    fr.quad((COUNTER_OPEN[0] - 0.1, yf - 0.17, 4.42), (COUNTER_OPEN[1] - COUNTER_OPEN[0] + 0.2, 0, 0), (0, 0, 0.86), M['fascia'], (0, 0, 1, 1))
    _obj(ex, 'front_wall_out', SET); _obj(fr, 'front_frame', SET, hull=0.02)
    # upper jettied storey, gable roof, bread sign (outside) -- the bakery seen from the street
    F = Frame((x0, yo, 0), 0)
    up = MB(); w = x1 - x0; d = 11.5; z0 = CEIL; z1 = CEIL + 3.6; yj = -0.9
    F.quad(up, [(0, yj, z0), (w, yj, z0), (w, yj, z1), (0, yj, z1)], M['bk_u'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
    F.quad(up, [(0, yj, z0), (w, yj, z0), (w, 0, z0), (0, 0, z0)], M['timber'], [(0, 0), (w / 2, 0), (w / 2, 0.3), (0, 0.3)], (0, 0, -1))
    F.box(up, (-0.08, yj - 0.12, z0 - 0.28), (w + 0.08, yj + 0.12, z0 + 0.02), M['timber'], 0.5)
    for x in [0.2 + (w - 0.4) * i / 5 for i in range(6)]: beam(up, F.p(x, yj + 0.1, z0 - 0.25), F.p(x, 0.0, z0 - 1.1), 0.16, 0.16, M['timber'])
    rh = 5.0
    F.quad(up, [(0, yj, z1), (w, yj, z1), (w, yj, z1 + rh), (0, yj, z1 + rh)], M['bk_gab'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
    for s in (0, 1):
        xa = -0.4 if s == 0 else w + 0.4
        F.quad(up, [(xa, yj - 0.5, z1 - 0.3), (xa, d, z1 - 0.3), (w / 2, d, z1 + rh + 0.1), (w / 2, yj - 0.5, z1 + rh + 0.1)], M['roof'], [(0, 0), (d / 2, 0), (d / 2, 2.6), (0, 2.6)], (-1 if s == 0 else 1, 0, 1.2))
    _obj(up, 'bakery_upper', SET, hull=0.03)
    # the hanging bread sign on its bracket, beside the counter opening (outside)
    sg = MB(); bx = 2.25; z = 5.55; yb = yo
    rod(sg, (bx, yb, z), (bx, yb - 2.0, z), 0.045, M['iron'], seg=6); rod(sg, (bx, yb, z - 0.7), (bx, yb - 1.3, z), 0.03, M['iron'], seg=6)
    for k in range(8):
        a0, a1 = k / 8 * 5.5, (k + 1) / 8 * 5.5; rr_ = 0.25 * (1 - k / 10)
        rod(sg, (bx, yb - 1.7 + rr_ * math.cos(a0), z + 0.3 + rr_ * math.sin(a0)), (bx, yb - 1.7 + rr_ * math.cos(a1), z + 0.3 + rr_ * math.sin(a1)), 0.025, M['iron'], seg=5)
    for yy in (-0.55, -1.8): rod(sg, (bx, yb + yy, z), (bx, yb + yy, z - 0.25), 0.015, M['iron'], seg=4)
    sw, sh = 1.5, 1.12
    for (off, n) in ((-0.03, -1), (0.03, 1)):
        sg.oface([(bx + off, yb - 0.4, z - 0.25 - sh), (bx + off, yb - 0.4 - sw, z - 0.25 - sh), (bx + off, yb - 0.4 - sw, z - 0.25), (bx + off, yb - 0.4, z - 0.25)], M['sign_bread'],
                 [(0, 0), (1, 0), (1, 1), (0, 1)] if n < 0 else [(1, 0), (0, 0), (0, 1), (1, 1)], (n, 0, 0))
    obox(sg, (bx, yb - 0.4 - sw / 2, z - 0.25 - sh / 2), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.025, sw / 2, sh / 2, M['wood_d'])
    _obj(sg, 'bread_sign', SET, hull=0.015)
    # loaves and baskets on the shutter board outside + a wheat sheaf hung by the door
    lb = MB(); rr = _rnd(5); a, b, c, d = COUNTER_OPEN
    for i in range(7):
        x = a + 0.4 + i * (b - a - 0.8) / 6
        if i in (1, 4): _basket(lb, (x, -1.0, c), 0.32, 0.25, M, loaves=5, seed=50 + i)
        else:
            for j in range(3): _bake_loaf(lb, (x + 0.14 * (j - 1), -0.85 - 0.3 * (j % 2), c + 0.02 + 0.13 * (j == 1)), 0.21, rr.choice((M['loaf'], M['loaf_d'], M['loaf_p'])), 600 + i * 3 + j)
    _obj(lb, 'counter_loaves_out', SET, hull=0.012)
    hb = MB(); rod(hb, (a + 0.1, -0.62, d - 0.12), (b - 0.1, -0.62, d - 0.12), 0.03, M['iron'], seg=5)
    for k, x in enumerate([a + 0.45 + i * (b - a - 0.9) / 5 for i in range(6)]):
        mat = (M['wheat'], M['onions'], M['herbs'], M['wheat'], M['herbs2'], M['onions'])[k]; s = 0.55
        for (u, n) in ((Vector((s / 2, 0, 0)), (0, -1, 0)), (Vector((0, s / 2, 0)), (1, 0, 0))):
            c = Vector((x, -0.62, d - 0.12))
            hb.face([c - u - Vector((0, 0, 1.5 * s)), c + u - Vector((0, 0, 1.5 * s)), c + u, c - u], mat, [(0, 0), (1, 0), (1, 1), (0, 1)])
    _obj(hb, 'opening_bundles', SET, shadow=False)

def _oven(SET, P, M):
    """Domed brick oven: brick plinth (z 0..1.4), dome R 2.7 squashed, a front face with the arched mouth (fire inside, ember bed),
    an iron door leaning beside it, the brick hood and chimney breast to the ceiling, soot round the mouth; ash pit; tool rack."""
    cx, cy = OVEN_C; R = OVEN_R; zb = OVEN_BASE; mb = MB(); fl = MB()
    mb.box((cx - R - 0.3, cy - R - 0.2, 0), (cx + R + 0.3, ROOM[3], zb), M['brick'], tile=(2, 2))
    # dome: rings of brick-textured quads, front part cut by the front face plane y = cy - R*0.82
    yfront = cy - R * 0.92; rings, seg = 8, 24
    def dp(th, ph):
        return Vector((cx + R * math.cos(th) * math.cos(ph), cy + R * math.cos(th) * math.sin(ph), zb + R * 0.78 * math.sin(th)))
    for k in range(rings):
        for i in range(seg):
            th0, th1 = math.pi / 2 * k / rings, math.pi / 2 * (k + 1) / rings; ph0, ph1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg
            pts = [dp(th0, ph0), dp(th0, ph1), dp(th1, ph1), dp(th1, ph0)]
            if all(p.y < yfront for p in pts): continue
            pts = [Vector((p.x, max(p.y, yfront), p.z)) for p in pts]
            mat = M['brick_s'] if k >= 5 else M['brick']
            mb.oface(pts, mat, [(i * 0.6, k * 0.45), ((i + 1) * 0.6, k * 0.45), ((i + 1) * 0.6, (k + 1) * 0.45), (i * 0.6, (k + 1) * 0.45)], (pts[0] - Vector((cx, cy, zb))))
    # front face: a flat brick wall at y = yfront from the plinth up to the hood, with the arched mouth
    mw, mh = 1.0, 1.25; mz = zb + 0.15
    hw = R * 0.98; top = zb + 2.6
    ring = [(cx + mw * math.cos(math.pi * t / 12), mz + mh - mw * 0.6 + mw * 0.6 * math.sin(math.pi * t / 12)) for t in range(13)]
    outline = [(cx + mw, mz)] + ring + [(cx - mw, mz)]
    # face as quads between the mouth outline and the outer rectangle (fan from outline to rectangle corners)
    def F(x, z): return Vector((x, yfront, z))
    for i in range(len(ring) - 1):
        (xa, za), (xb, zb_) = ring[i], ring[i + 1]
        mb.oface([F(xa, za), F(xb, zb_), F(xb, top), F(xa, top)], M['brick_s'], [(xa / 2, za / 2), (xb / 2, zb_ / 2), (xb / 2, top / 2), (xa / 2, top / 2)], (0, -1, 0))
    for (a, b) in ((cx - hw, cx - mw), (cx + mw, cx + hw)):
        mb.oface([F(a, zb), F(b, zb), F(b, top), F(a, top)], M['brick'], [(a / 2, zb / 2), (b / 2, zb / 2), (b / 2, top / 2), (a / 2, top / 2)], (0, -1, 0))
    mb.oface([F(cx - mw, zb), F(cx + mw, zb), F(cx + mw, mz), F(cx - mw, mz)], M['brick'], [(0, 0), (1, 0), (1, 0.1), (0, 0.1)], (0, -1, 0))
    # mouth tunnel (sooty) and the inner back where the fire sits
    depth = 1.4
    for i in range(len(ring) - 1):
        (xa, za), (xb, zb_) = ring[i], ring[i + 1]
        mb.oface([F(xa, za), F(xb, zb_), Vector((xb, yfront + depth, zb_)), Vector((xa, yfront + depth, za))], M['brick_s'], [(0, 0), (1, 0), (1, 1), (0, 1)], (cx - (xa + xb) / 2, 0, mz + 0.3 - (za + zb_) / 2))
    for x in (cx - mw, cx + mw):
        mb.oface([F(x, mz), Vector((x, yfront + depth, mz)), Vector((x, yfront + depth, mz + mh - mw * 0.6)), F(x, mz + mh - mw * 0.6)], M['brick_s'], [(0, 0), (1, 0), (1, 1), (0, 1)], (cx - x, 0, 0))
    fl.quad((cx - mw, yfront + 0.02, mz + 0.003), (2 * mw, 0, 0), (0, depth, 0), M['embers'], (0, 0, 1, 1))
    for k, yy in enumerate((yfront + depth - 0.05, yfront + depth * 0.6, yfront + depth * 0.3)):
        s = 1.0 - 0.18 * k
        fl.quad((cx - mw * s, yy, mz), (2 * mw * s, 0, 0), (0, 0, mh * s * (1.0 - 0.1 * k)), M['fire'], (0, 0, 1, 1))
    mb.oface([Vector((cx - mw, yfront + depth, mz)), Vector((cx + mw, yfront + depth, mz)), Vector((cx + mw, yfront + depth, mz + mh)), Vector((cx - mw, yfront + depth, mz + mh))], M['dark'], [(0, 0)] * 4, (0, -1, 0))
    for i in range(5):                                                                             # logs in the fire
        x = cx - 0.6 + i * 0.3; rod(mb, (x, yfront + 0.3, mz + 0.08), (x + 0.1, yfront + depth - 0.1, mz + 0.12), 0.07, M['wood_d'], seg=6)
    # sill ledge in front of the mouth
    obox(mb, (cx, yfront - 0.25, zb + 0.05), (1, 0, 0), (0, 1, 0), (0, 0, 1), mw + 0.6, 0.3, 0.08, M['stone_x'])
    # hood / chimney breast rising from the face to the ceiling
    hb = [(cx - hw, yfront, top), (cx + hw, yfront, top), (cx + hw * 0.6, yfront + 0.8, CEIL), (cx - hw * 0.6, yfront + 0.8, CEIL)]
    mb.oface(hb, M['brick_s'], [(0, 0.6 * 2), (1.4 * 2, 0.6 * 2), (1.2 * 2, 0), (0.2 * 2, 0)], (0, -1, 0.4))
    for s in (-1, 1):
        mb.oface([(cx + s * hw, yfront, top), (cx + s * hw, ROOM[3], top), (cx + s * hw * 0.6, ROOM[3], CEIL), (cx + s * hw * 0.6, yfront + 0.8, CEIL)], M['brick_s'], [(0, 0), (1, 0), (1, 1), (0, 1)], (s, 0, 0.2))
    obox(mb, (cx, yfront - 0.12, top + 0.02), (1, 0, 0), (0, 1, 0), (0, 0, 1), hw + 0.15, 0.2, 0.14, M['timber'])          # mantel beam
    # ash pit arch in the plinth
    obox(mb, (cx, cy - R - 0.21, 0.55), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.7, 0.02, 0.4, M['dark'])
    _obj(mb, 'oven', SET, hull=0.02)
    fo = _obj(fl, 'oven_fire', SET, shadow=False); fo.visible_shadow = False
    STATE['mouth'] = Vector((cx, yfront, mz + 0.55)); STATE['oven_front_y'] = yfront
    # glow halo around the mouth (camera-only)
    hb_ = MB(); c = Vector((cx, yfront - 0.15, mz + 0.6)); r = 2.6
    hb_.face([c + Vector((-r, 0, -r)), c + Vector((r, 0, -r)), c + Vector((r, 0, r)), c + Vector((-r, 0, r))], M['halo_big'], [(0, 0), (1, 0), (1, 1), (0, 1)])
    _obj(hb_, 'oven_halo', SET, shadow=False)
    # warm pool of light on the floor in front of the oven
    pl = MB(); pl.quad((cx - 3.5, yfront - 5.5, 0.01), (7, 0, 0), (0, 6, 0), M['pool'], (0, 0, 1, 1)); _obj(pl, 'oven_pool', SET, shadow=False)

def _table(SET, M):
    """Long flour-dusted work table along the right wall: top, trestle legs and stretcher, dough, loaves cooling on boards and in rows,
    a trough of dough, rolling pin, knife, scraper, flour bin, a candle at each end."""
    xc, ya, yb, zt = TABLE; mb = MB(); fl = MB(); rr = _rnd(7)
    hw = 0.85
    mb.box((xc - hw, ya, zt - 0.14), (xc + hw, yb, zt), M['table'], mats=dict(top=M['table']), tile=(2, 2))
    for y in (ya + 0.4, yb - 0.4, (ya + yb) / 2):
        for s in (-1, 1): beam(mb, (xc + s * 0.75, y, 0), (xc + s * 0.6, y, zt - 0.14), 0.14, 0.14, M['timber_l'], up=(0, 1, 0))
    beam(mb, (xc, ya + 0.4, 0.35), (xc, yb - 0.4, 0.35), 0.12, 0.12, M['timber_l'])
    # boards of cooling loaves (the steam sources)
    loaves = []
    for (y, n, kind) in ((ya + 0.6, 6, 'round'), (ya + 1.9, 5, 'round'), (ya + 3.3, 4, 'long')):
        mb.box((xc - 0.7, y - 0.45, zt), (xc + 0.7, y + 0.45, zt + 0.05), M['wood'], tile=(1, 1))
        for i in range(n):
            x = xc - 0.55 + 1.1 * (i % 3) / 2; yy = y - 0.22 + 0.44 * (i // 3)
            if kind == 'long': x = xc - 0.4 + 0.8 * (i % 2); yy = y - 0.22 + 0.44 * (i // 2)
            p = (x, yy, zt + 0.05); loaves.append(p)
            _bake_loaf(mb, p, 0.24 if kind == 'round' else 0.17, rr.choice((M['loaf'], M['loaf'], M['loaf_d'])), 700 + len(loaves), long=1.0 if kind == 'round' else 2.0, yaw=0.3 * rr.uniform(-1, 1))
    # dough balls, trough, rolling pin, knife
    for i in range(5): lumpy(mb, (xc - 0.4 + 0.2 * i, yb - 1.6 + 0.1 * (i % 2), zt + 0.12), 0.16, M['dough'], 80 + i, seg=10, rings=5, rough=0.1, squash=0.6)
    obox(mb, (xc, yb - 0.7, zt + 0.22), (0, 1, 0), (1, 0, 0), (0, 0, 1), 0.55, 0.42, 0.22, M['wood_d'])
    lumpy(mb, (xc, yb - 0.7, zt + 0.42), 0.4, M['dough'], 99, seg=12, rings=5, rough=0.08, squash=0.35)
    rod(mb, (xc - 0.5, yb - 2.3, zt + 0.07), (xc + 0.3, yb - 2.2, zt + 0.07), 0.06, M['wood'], seg=8)
    rod(mb, (xc + 0.1, ya + 2.65, zt + 0.02), (xc + 0.6, ya + 2.75, zt + 0.02), 0.02, M['pewter'], seg=4)
    mb.box((xc + 0.4, yb - 2.8, zt), (xc + 0.75, yb - 2.4, zt + 0.06), M['flour'])
    lumpy(mb, (xc - 0.35, yb - 2.6, zt + 0.02), 0.25, M['flour'], 111, seg=10, rings=4, rough=0.2, squash=0.25)
    STATE['table_loaves'] = loaves
    for y in (ya + 0.15, yb - 0.15):
        f = _candle(mb, fl, (xc + 0.6, y, zt), M, h=0.5); STATE.setdefault('candles', []).append(f)
    # flour bin and a stool under / beside the table
    mb.box((xc - 0.5, yb + 0.2, 0), (xc + 0.5, yb + 1.0, 1.0), M['wood_d'], tile=(1, 1))
    rod(mb, (xc - 1.5, 5.2, 0), (xc - 1.5, 5.2, 0.9), 0.35, M['wood'], seg=10)
    _obj(mb, 'table', SET, hull=0.012); _obj(fl, 'table_flames', SET, shadow=False)

def _racks(SET, M):
    """Shelf racks of loaves on the right wall (x 6.2..7) and baker's racks on the back wall right of the oven; plus a hanging shelf
    over the counter. Loaves heaped in rows, baskets, crocks, jars."""
    mb = MB(); rr = _rnd(9)
    xw = ROOM[1] - 0.25
    for (y0_, y1_) in ((1.4, 3.6), (4.4, 7.2), (8.0, 10.6)):
        for z in (1.6, 2.7, 3.8, 4.9):
            mb.box((xw - 0.85, y0_, z - 0.06), (xw, y1_, z), M['shelf'], tile=(2, 2))
            n = int((y1_ - y0_) / 0.45)
            for i in range(n):
                y = y0_ + 0.25 + i * (y1_ - y0_ - 0.5) / max(1, n - 1)
                if rr.random() < 0.12: _basket(mb, (xw - 0.45, y, z), 0.22, 0.2, M, loaves=3, seed=900 + i)
                elif rr.random() < 0.14: rod(mb, (xw - 0.45, y, z), (xw - 0.45, y, z + 0.35), 0.15, rr.choice((M['red'], M['cream'], M['blue'], M['blue'])), seg=10, r1=0.11)
                else:
                    _bake_loaf(mb, (xw - 0.45, y, z), 0.21, rr.choice((M['loaf'], M['loaf_d'], M['loaf_p'])), 1000 + int(z * 10) * 50 + i)
                    if rr.random() < 0.5: _bake_loaf(mb, (xw - 0.55, y + 0.1, z + 0.13), 0.18, rr.choice((M['loaf'], M['loaf_d'])), 2000 + int(z * 10) * 50 + i)
        for y in (y0_, y1_):
            mb.box((xw - 0.88, y - 0.06, 0), (xw - 0.78, y + 0.06, 5.2), M['timber_l'])
    # baker's rack on the back wall right of the oven (x 1.2..4.0)
    for z in (0.6, 1.6, 2.6, 3.6):
        mb.box((1.2, ROOM[3] - 0.9, z - 0.06), (4.0, ROOM[3] - 0.05, z), M['shelf'], tile=(2, 2))
        for i in range(6):
            x = 1.45 + i * 0.45
            if z == 0.6: mb.box((x - 0.18, ROOM[3] - 0.8, z), (x + 0.18, ROOM[3] - 0.2, z + 0.5), M['sack_p'], tile=(1.2, 1.2))
            else: _bake_loaf(mb, (x, ROOM[3] - 0.45, z), 0.2, rr.choice((M['loaf'], M['loaf_d'], M['loaf_p'])), 3000 + int(z * 10) * 10 + i)
    for x in (1.2, 4.0):
        mb.box((x - 0.06, ROOM[3] - 0.95, 0), (x + 0.06, ROOM[3] - 0.85, 4.2), M['timber_l'])
    _obj(mb, 'racks', SET, hull=0.012)

def _counter(SET, M):
    """Inside counter under the shop opening (x -1.5..3.5, y 0..1.3, top z 1.25): plank top, panelled front, the small hand balance
    with its weights box, a basket of loaves, coins, a tally stick, a candle; a shelf above with jars."""
    a, b, c, d = COUNTER_OPEN; mb = MB(); fl = MB(); rr = _rnd(11)
    mb.box((a - 0.2, 0.0, c - 0.12), (b + 0.2, 1.3, c), M['counter'], tile=(2, 2))
    mb.box((a - 0.1, 1.15, 0), (b + 0.1, 1.25, c - 0.12), M['wood_d'], tile=(1, 1))
    for x in [a + (b - a) * k / 4 for k in range(5)]: mb.box((x - 0.06, 1.24, 0.1), (x + 0.06, 1.3, c - 0.2), M['timber'])
    _basket(mb, (-0.7, 0.65, c), 0.38, 0.28, M, loaves=6, seed=33, handle=True)
    for i in range(4): rod(mb, (0.35 + 0.08 * i, 0.9, c), (0.35 + 0.08 * i, 0.9, c + 0.015 * (i + 1)), 0.045, M['brass'], seg=8)  # coins
    rod(mb, (0.8, 1.0, c + 0.03), (1.3, 0.95, c + 0.03), 0.03, M['wood'], seg=5)                                             # tally stick
    f = _candle(mb, fl, (3.1, 1.0, c), M, h=0.4); STATE.setdefault('candles', []).append(f)
    mb.box((a - 0.6, 0.0, d + 0.45), (b + 0.6, 0.55, d + 0.53), M['shelf'], tile=(2, 2))
    for x in (a - 0.3, b + 0.3): beam(mb, (x, 0.02, d - 0.1), (x, 0.5, d + 0.45), 0.08, 0.08, M['timber_l'], up=(1, 0, 0))
    for i in range(12):
        x = a - 0.35 + i * (b - a + 0.7) / 11; k = i % 4
        if k == 0: rod(mb, (x, 0.28, d + 0.53), (x, 0.28, d + 0.95), 0.18, M['red'] if i % 8 else M['blue'], seg=10, r1=0.12)
        elif k == 1: rod(mb, (x, 0.28, d + 0.53), (x, 0.28, d + 0.85), 0.15, M['cream'], seg=10, r1=0.17); rod(mb, (x, 0.28, d + 0.85), (x, 0.28, d + 0.98), 0.08, M['cream'], seg=8)
        elif k == 2: _basket(mb, (x, 0.28, d + 0.53), 0.2, 0.18, M, loaves=2, seed=1200 + i)
        else: _bake_loaf(mb, (x, 0.28, d + 0.53), 0.19, M['loaf_d'], 1300 + i)
    for i in range(5):
        x = a + 0.4 + i * 0.35; rod(mb, (x, 0.5, d + 0.4), (x, 0.5, d - 0.25), 0.015, M['iron'], seg=4); rod(mb, (x, 0.5, d - 0.25), (x, 0.5, d - 0.4), 0.08, M['copper'], seg=10)
    _obj(mb, 'counter', SET, hull=0.012); _obj(fl, 'counter_flame', SET, shadow=False)
    _small_scale(SET, M)

def _small_scale(SET, M):
    """Hand balance on the counter: turned wooden base, brass post, beam pivot (set_scale), two brass pans on cords (pivots follow the
    beam ends, pans stay level), a loaf on the left pan, brass weights on the right one, a box of nested weights beside it."""
    x, y, z = SMALL_SCALE; sb = MB(); pz = z + 0.95; arm = 0.5
    rod(sb, (x, y, z), (x, y, z + 0.06), 0.22, M['wood_d'], seg=14); rod(sb, (x, y, z + 0.06), (x, y, pz), 0.03, M['brass'], seg=8)
    sb.sphere((x, y, pz + 0.05), 0.05, M['brass'], seg=8, rings=4)
    _obj(sb, 'small_scale_base', SET, hull=0.008)
    piv = G._pivot('small_beam_pivot', SET, (x, y, pz)); bm = MB()
    rod(bm, (x - arm, y, pz), (x + arm, y, pz), 0.022, M['brass'], seg=8); rod(bm, (x, y, pz - 0.08), (x, y, pz + 0.12), 0.012, M['brass'], seg=6)
    for s in (-1, 1): bm.sphere((x + s * arm, y, pz), 0.035, M['brass'], seg=8, rings=4)
    ob = _obj(bm, 'small_beam', SET, hull=0.006); G._parent(ob, piv)
    pans = []
    for s, nm in ((-1, 'small_pan_loaf'), (1, 'small_pan_weights')):
        pe = G._pivot(nm, SET, (x + s * arm, y, pz)); pb = MB(); pzz = pz - 0.62
        for k in range(3):
            a = 2 * math.pi * k / 3 + 0.3; rod(pb, (x + s * arm, y, pz), (x + s * arm + 0.16 * math.cos(a), y + 0.16 * math.sin(a), pzz + 0.05), 0.005, M['rope'], seg=4)
        rod(pb, (x + s * arm, y, pzz), (x + s * arm, y, pzz + 0.05), 0.17, M['brass'], seg=14, r1=0.19)
        if s > 0:
            for k, (dx, dy, rr_) in enumerate(((0.0, 0.0, 0.08), (0.08, 0.05, 0.05), (-0.07, 0.05, 0.04))):
                rod(pb, (x + s * arm + dx, y + dy, pzz + 0.05), (x + s * arm + dx, y + dy, pzz + 0.05 + rr_ * 1.1), rr_, M['brass'], seg=10)
        po = _obj(pb, nm + '_mesh', SET, hull=0.006); G._parent(po, pe); pans.append(pe)
    lb = MB(); _bake_loaf(lb, (x - arm, y, pz - 0.62 + 0.05), 0.15, M['loaf'], 4242)
    lo = _obj(lb, 'small_scale_loaf', SET, hull=0.006); G._parent(lo, pans[0])
    STATE['small'] = dict(pivot=piv, pans=pans, arm=arm, pz=pz, loaf=lo)
    wb = MB(); wb.box((x + 0.55, y - 0.2, z), (x + 0.95, y + 0.2, z + 0.12), M['wood_d'])
    for k in range(4): rod(wb, (x + 0.62 + 0.1 * k, y, z + 0.12), (x + 0.62 + 0.1 * k, y, z + 0.16 + 0.02 * k), 0.035 + 0.008 * k, M['brass'], seg=8)
    _obj(wb, 'weights_box', SET, hull=0.006)

def _bakery_dressing(SET, M):
    """Sacks, kneading trough, wood pile, peel, barrels, hanging herbs / onions / wheat, copper pans on a rail by the oven, a candle wheel
    under the middle beam, a wall sconce, a broom, buckets, the ASSIZE notice, baskets stacked, a cat-free floor."""
    mb = MB(); fl = MB(); cards = MB(); rr = _rnd(13); x0, x1, y0, y1 = ROOM
    # flour sacks heaped against the left wall (y 2..6)
    for i, (x, y, z, rot) in enumerate(((x0 + 0.7, 2.0, 0, 0.1), (x0 + 0.7, 2.9, 0, -0.1), (x0 + 0.7, 3.8, 0, 0.05), (x0 + 1.6, 2.4, 0, 0.3), (x0 + 0.7, 2.45, 1.05, 0.0),
                                        (x0 + 0.7, 3.35, 1.05, 0.2), (x0 + 1.6, 3.4, 0, -0.2), (x0 + 0.75, 2.9, 2.0, 0.1))):
        c = Vector((x, y, z + 0.5)); X = Vector((math.cos(rot), math.sin(rot), 0)); Y = Vector((-math.sin(rot), math.cos(rot), 0))
        obox(mb, c, X, Y, Vector((0, 0, 1)), 0.5, 0.42, 0.5, M['sack'] if i % 2 == 0 else M['sack_p'])
        lumpy(mb, c + Vector((0, 0, 0.5)), 0.32, M['sack_p'], 300 + i, seg=8, rings=4, rough=0.15, squash=0.5)
        rod(mb, c + Vector((0, 0, 0.62)), c + Vector((0, 0, 0.78)), 0.08, M['rope'], seg=6)
    lumpy(mb, (x0 + 1.9, 4.2, 0.02), 0.5, M['flour'], 333, seg=10, rings=4, rough=0.25, squash=0.18)
    # kneading trough on legs (left wall, y 5..8)
    xt = x0 + 1.4
    for (yy, s) in ((5.3, 1), (7.7, 1)):
        for dx in (-0.5, 0.5): beam(mb, (xt + dx, yy, 0), (xt + dx * 0.8, yy, 1.0), 0.12, 0.12, M['timber_l'], up=(0, 1, 0))
    mb.box((xt - 0.7, 5.0, 1.0), (xt + 0.7, 8.0, 1.6), M['wood_d'], tile=(1, 1))
    mb.box((xt - 0.6, 5.1, 1.55), (xt + 0.6, 7.9, 1.58), M['dough'])
    rod(mb, (xt - 0.75, 5.0, 1.62), (xt - 0.75, 8.0, 1.62), 0.05, M['wood'], seg=6)
    # wood pile for the oven (left of the oven, x -6.6..-5.4, y 8.5..10.8)
    for k in range(18):
        row = k // 6; i = k % 6; yy = 8.6 + i * 0.38; zz = 0.2 + row * 0.36 + (0.18 if i % 2 else 0)
        rod(mb, (x0 + 0.2, yy, zz), (x0 + 1.6, yy + rr.uniform(-0.05, 0.05), zz), 0.18, M['wood_d'], seg=8)
        cards.quad((x0 + 1.61, yy - 0.18, zz - 0.18), (0, 0.36, 0), (0, 0, 0.36), M['log'], (0, 0, 1, 1))
    # bread peel leaning by the oven, rake, broom
    beam(mb, (-5.6, 6.5, 0.05), (-5.3, 7.4, 4.6), 0.07, 0.07, M['wood'])
    obox(mb, (-5.62, 6.45, 0.4), Vector((0.07, 0.2, 0.98)).normalized(), Vector((1, -0.35, 0)).normalized(), Vector((0.07, 0.2, 0.98)).normalized().cross(Vector((1, -0.35, 0)).normalized()), 0.38, 0.32, 0.03, M['wood'])
    beam(mb, (0.6, 7.0, 0.05), (0.75, 7.6, 4.0), 0.06, 0.06, M['wood'])
    obox(mb, (0.6, 6.95, 0.25), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.35, 0.05, 0.25, M['iron'])
    beam(mb, (x0 + 0.4, 0.7, 0.05), (x0 + 0.3, 1.0, 3.0), 0.05, 0.05, M['wood'])
    lumpy(mb, (x0 + 0.42, 0.68, 0.35), 0.25, M['hay'], 77, seg=8, rings=4, rough=0.3, squash=1.6)
    # water barrels and buckets
    for (x, y) in ((x0 + 0.9, 9.4), (x1 - 2.2, 10.2)):
        rod(mb, (x, y, 0), (x, y, 1.5), 0.55, M['wood'], seg=14, r1=0.55); rod(mb, (x, y, 0.75), (x, y, 0.78), 0.6, M['iron'], seg=14)
        for z in (0.25, 1.25): rod(mb, (x, y, z), (x, y, z + 0.06), 0.57, M['iron'], seg=14)
        mb.quad((x - 0.5, y - 0.5, 1.45), (1.0, 0, 0), (0, 1.0, 0), M['water'])
    rod(mb, (-0.5, 9.5, 0), (-0.5, 9.5, 0.5), 0.25, M['wood'], seg=10, r1=0.3)
    # stacked baskets by the counter, more loaves in baskets on the floor
    for i, (x, y) in enumerate(((-2.0, 1.9), (-1.6, 2.5), (3.9, 1.8))):
        _basket(mb, (x, y, 0), 0.4, 0.4, M, loaves=6 if i != 0 else 0, seed=400 + i, handle=(i == 1))
        if i == 0: lumpy(mb, (x, y, 0.42), 0.42, M['cloth_b'], 450, seg=10, rings=4, rough=0.25, squash=0.35)
    # copper pans and utensils on an iron rail over the oven mantel side (x -6.6..-5.6) and on the right of the hood
    for (xa, xb, y) in ((0.2, 2.4, y1 - 0.15),):
        rod(mb, (xa, y - 0.05, 4.9), (xb, y - 0.05, 4.9), 0.03, M['iron'], seg=6)
        for k in range(5):
            x = xa + 0.25 + k * 0.45; r_ = 0.18 + 0.03 * (k % 3)
            rod(mb, (x, y - 0.1, 4.9), (x, y - 0.1, 4.55), 0.012, M['iron'], seg=4)
            rod(mb, (x, y - 0.12, 4.55 - r_ * 2 - 0.4), (x, y - 0.12, 4.55 - r_ * 2), 0.03, M['copper'], seg=6)
            obox(mb, (x, y - 0.14, 4.55 - r_ * 3 - 0.4), (1, 0, 0), (0, 1, 0), (0, 0, 1), r_, 0.05, r_, M['copper'])
            rod(mb, (x, y - 0.2, 4.55 - r_ * 3 - 0.4), (x, y - 0.12, 4.55 - r_ * 3 - 0.4), r_, M['copper'], seg=14)
    # hanging bundles from the beams: herbs, onions, wheat (crossed cards), and copper pots on hooks under the beam y 4.0
    for k in range(16):
        yb = (1.6, 4.0, 6.4, 8.8)[k % 4]; x = -6.0 + (k // 4) * 3.1 + rr.uniform(-0.4, 0.4)
        if abs(x - OVEN_C[0]) < 3.2 and yb > 7: continue
        mat = rr.choice((M['herbs'], M['herbs2'], M['onions'], M['wheat'], M['herbs']))
        top = CEIL - 0.6; s = rr.uniform(0.85, 1.2)
        rod(mb, (x, yb - 0.3, top), (x, yb - 0.3, top - 0.25), 0.01, M['rope'], seg=4)
        for (u, v) in ((Vector((0.5, 0, 0)), 0), (Vector((0, 0.5, 0)), 1)):
            c = Vector((x, yb - 0.3, top - 0.2))
            cards.face([c - u * s - Vector((0, 0, 1.5 * s)), c + u * s - Vector((0, 0, 1.5 * s)), c + u * s, c - u * s], mat, [(0, 0), (1, 0), (1, 1), (0, 1)])
    # candle wheel (iron hoop on chains) with 6 candles, under the middle of the room
    cw = (0.6, 5.2, 4.9); hoop = [Vector((cw[0] + 0.9 * math.cos(2 * math.pi * i / 16), cw[1] + 0.9 * math.sin(2 * math.pi * i / 16), cw[2])) for i in range(17)]
    chain_rod(mb, hoop, 0.04, M['iron'])
    for i in range(3):
        a = 2 * math.pi * i / 3; chain_rod(mb, [Vector((cw[0] + 0.9 * math.cos(a), cw[1] + 0.9 * math.sin(a), cw[2])), Vector((cw[0], cw[1], CEIL - 0.6))], 0.012, M['iron'])
    for i in range(6):
        a = 2 * math.pi * i / 6 + 0.2; f = _candle(mb, fl, (cw[0] + 0.9 * math.cos(a), cw[1] + 0.9 * math.sin(a), cw[2]), M, h=0.35, r=0.05)
        _halo(cards, f, 0.35, M)
    STATE['wheel'] = Vector((cw[0], cw[1], cw[2] + 0.45))
    # wall sconce by the door and a lantern on the post near the racks
    for (p, n) in (((-4.9, 0.25, 3.6), (0, 1, 0)), ((x1 - 0.45, 4.0, 3.4), (-1, 0, 0))):
        p = Vector(p); nn = Vector(n); rod(mb, p - nn * 0.2, p + nn * 0.1, 0.03, M['iron'], seg=5)
        f = _candle(mb, fl, p + nn * 0.1, M, h=0.32, r=0.05); STATE.setdefault('candles', []).append(f)
    # the ASSIZE OF BREAD notice nailed on the post by the counter
    cards.quad((-1.9, 0.02, 2.1), (0.9, 0, 0), (0, 0, 1.17), M['notice'], (0, 0, 1, 1))
    for f in STATE.get('candles', []): _halo(cards, f, 0.32, M)
    # spilt flour patches, crumbs, a dropped loaf on the floor, a stool
    rod(mb, (-1.0, 3.0, 0), (-1.0, 3.0, 0.8), 0.3, M['wood_d'], seg=10)
    _obj(mb, 'dressing', SET, hull=0.012); _obj(fl, 'dressing_flames', SET, shadow=False)
    o = _obj(cards, 'dressing_cards', SET, shadow=False)

def _lights_inside(SET, P, M):
    """Real point lights: the oven fire (two: in the mouth and a broad fill in front, flickering via set_oven), the candle wheel, the
    candles (one light each for the table ends and the counter), the sconces. The sun comes in through the openings (shafts)."""
    m = STATE['mouth']; fk = P.get('fire_k', 1.0)
    L1 = _light('oven_fire', (m.x, m.y - 0.4, m.z + 0.1), FIRE, 1100 * fk, radius=0.5)
    L2 = _light('oven_fill', (m.x + 0.5, m.y - 2.2, m.z + 1.4), (1.0, 0.62, 0.32), 280 * fk, radius=1.2, shadow=False)
    STATE['fire_lights'] = [(L1, 1100 * fk), (L2, 280 * fk)]
    wl = STATE['wheel']; _light('candle_wheel', tuple(wl), CANDLE, 150, radius=0.6, shadow=True)
    for i, f in enumerate(STATE.get('candles', [])):
        _light('candle_%d' % i, tuple(f + Vector((0, 0, 0.05))), CANDLE, 45, radius=0.1, shadow=False)
    # sun shafts through the openings: camera-only additive prisms along the key, from the opening to the floor
    kd = Vector(P['key_dir']).normalized(); sb = MB()
    for (a, b, c, d) in (COUNTER_OPEN, DOOR_OPEN, WIN_OPEN):
        if (a, b, c, d) == DOOR_OPEN: c = 2.0                                                 # the lower leaf is shut
        corners = [Vector((a, 0.0, c)), Vector((b, 0.0, c)), Vector((b, 0.0, d)), Vector((a, 0.0, d))]
        def ext(p):
            t = p.z / max(0.05, -kd.z); t = min(t, 12.0); return p + kd * t
        far = [ext(p) for p in corners]
        mid = lambda p, q: (p + q) / 2                # two crossed mid-sheets per opening (4 faces cost 7 CPU s more)
        sb.face([mid(corners[0], corners[3]), mid(corners[1], corners[2]), mid(far[1], far[2]), mid(far[0], far[3])], M['shaft'], [(0, 0), (1, 0), (1, 1), (0, 1)])
        sb.face([mid(corners[0], corners[1]), mid(corners[3], corners[2]), mid(far[3], far[2]), mid(far[0], far[1])], M['shaft'], [(0, 0), (1, 0), (1, 1), (0, 1)])
    _obj(sb, 'sun_shafts', SET, shadow=False)

def _street(SET, M):
    """The street outside the bakery: cobbles, the row of houses opposite (y -11, facing +y) with shops and signs, neighbours either side
    of the bakery (y -0.5, facing -y), a few market stalls, barrels and a cart; seen through the counter opening and from the counter cam."""
    mb = MB(); mb.quad((-60, -60, 0), (120, 0, 0), (0, 59.5, 0), M['cobbles'], (-15, -15, 15, -0.125)); _obj(mb, 'street', SET)
    # opposite row: front at y = -11 facing +y -> origin at the right end, yaw 180
    x = 14.0; k = 0
    for (w, v, gab, sign) in ((6.0, 1, True, ('sign_tankard', 1)), (5.5, 2, False, None), (6.5, 3, True, ('sign_boot', 1)), (6.0, 0, True, None), (5.0, 1, False, ('sign_fish', 1)), (6.0, 2, True, None)):
        o = house(SET, 'opp_%d' % k, (x, -11.0, 0), 180, w, v, M, d=7, gable=gab, sign=sign, seed=40 + k, third=(k % 3 == 1)); x -= w + 0.05; k += 1
        STATE['objects']['opp_%d' % (k - 1)].visible_shadow = False      # backdrop row: keeps the bakery front in the sun
    # neighbours beside the bakery (front at y -0.5 facing -y)
    house(SET, 'nb_r', (ROOM[1] + 0.05, -0.5, 0), 0, 6.0, 3, M, d=11, gable=False, seed=61)
    house(SET, 'nb_l', (ROOM[0] - 6.05, -0.5, 0), 0, 6.0, 2, M, d=11, gable=True, seed=62, sign=('sign_pretzel', -1))
    # street dressing: a stall with an awning against the opposite row, barrels, crates, a hand cart
    _stall(SET, 'st_opp', Frame((-4.0, -9.3, 0), 180), 3.2, M, 'awn_green', 'cloth_g', seed=71)
    d = MB()
    for (x, y) in ((6.0, -2.3), (6.9, -2.0)):
        rod(d, (x, y, 0), (x, y, 1.3), 0.45, M['wood'], seg=12, r1=0.45)
        for z in (0.2, 1.05): rod(d, (x, y, z), (x, y, z + 0.06), 0.47, M['iron'], seg=12)
    for (x, y, s) in ((-5.5, -2.0, 0.55), (-6.2, -2.4, 0.5), (-5.8, -2.2, 0.45)):
        obox(d, (x, y, s + (0.5 if s < 0.5 else 0)), (1, 0, 0), (0, 1, 0), (0, 0, 1), s, s, s, M['crate'])
    _obj(d, 'street_dressing', SET, hull=0.02)

def _steam_build(SET, M):
    """Steam wisps: crossed camera-only cards (0.7 x 2.2 D) rising off the cooling loaves on the table, the basket on the counter, the
    loaves on the shutter board, and a big plume at the oven mouth. set_steam scales their strength and scrolls them up."""
    srcs = [(p, 1.0) for p in STATE.get('table_loaves', [])[::3]]
    srcs += [((-0.7, 0.65, COUNTER_Z + 0.35), 0.9), ((0.8, -0.95, COUNTER_Z + 0.25), 0.8), ((2.4, -0.9, COUNTER_Z + 0.25), 0.8)]
    rr = _rnd(17); sb = MB(); n = 0
    for (p, s) in srcs:
        p = Vector(p) + Vector((0, 0, 0.12)); hw = 0.4 * s; h = 2.2 * s; a = math.radians(45 if n % 2 else -45) + rr.uniform(-0.2, 0.2)
        for k in range(1):                       # one card per source, turned 45 deg (reads from every preset camera); cost
            u = Vector((math.cos(a), math.sin(a), 0)) * hw
            v0 = rr.uniform(0, 1)
            sb.face([p - u, p + u, p + u + Vector((0, 0, h)), p - u + Vector((0, 0, h))], M['steam'] if (n + k) % 2 == 0 else M['steam2'], [(0, v0), (1, v0), (1, v0 + 0.75), (0, v0 + 0.75)])
        n += 1
    o = _obj(sb, 'steam', SET, shadow=False); STATE['steam'] = [o]

# ============================================================================= MARKET (exterior)
def _stall(SET, name, F, w, M, awn, cloth, seed=0, produce='veg', fire=False):
    """Market stall in a local frame (front edge at y 0, facing -y, x 0..w): four posts, a trestle table with a checked cloth, a slanted
    striped awning, produce heaped (cabbages, apples, turnips, carrots, onions) in crates and baskets, a sack, sometimes a brazier."""
    mb = MB(); cards = MB(); rr = _rnd(seed); d = 1.6; zt = 1.2
    for (x, y, h) in ((0.1, 0.1, 3.0), (w - 0.1, 0.1, 3.0), (0.1, d, 3.6), (w - 0.1, d, 3.6)):
        rod(mb, F.p(x, y, 0), F.p(x, y, h), 0.07, M['wood_d'], seg=6)
    F.box(mb, (0, 0, zt - 0.1), (w, d, zt), M['wood'], 0.5)
    F.quad(mb, [(0, -0.02, zt - 0.6), (w, -0.02, zt - 0.6), (w, -0.02, zt), (0, -0.02, zt)], M[cloth], [(0, 0), (w / 2, 0), (w / 2, 0.3), (0, 0.3)], (0, -1, 0))
    F.quad(mb, [(0, 0, zt + 0.001), (w, 0, zt + 0.001), (w, d, zt + 0.001), (0, d, zt + 0.001)], M[cloth], [(0, 0), (w / 2, 0), (w / 2, d / 2), (0, d / 2)], (0, 0, 1))
    F.quad(cards, [(-0.2, -0.6, 2.75), (w + 0.2, -0.6, 2.75), (w + 0.2, d + 0.2, 3.75), (-0.2, d + 0.2, 3.75)], M[awn], [(0, 1), (w / 2, 1), (w / 2, 0), (0, 0)], (0, -0.6, 1))
    F.quad(cards, [(-0.2, -0.6, 2.75), (w + 0.2, -0.6, 2.75), (w + 0.2, -0.6, 2.35), (-0.2, -0.6, 2.35)], M[awn], [(0, 0.2), (w / 2, 0.2), (w / 2, 0.0), (0, 0.0)], (0, -1, 0))
    n = int(w / 0.75)
    for i in range(n):
        x = 0.4 + i * (w - 0.8) / max(1, n - 1); kind = rr.choice(('cab', 'apple', 'turnip', 'carrot', 'crate', 'onion')) if produce == 'veg' else 'loaf'
        if kind == 'crate':
            F.box(mb, (x - 0.3, 0.3, zt), (x + 0.3, 0.9, zt + 0.35), M['crate'], 1.0)
            for j in range(6): lumpy(mb, F.p(x - 0.18 + 0.18 * (j % 3), 0.45 + 0.3 * (j // 3), zt + 0.38), 0.11, rr.choice((M['apple'], M['apple_g'], M['tomato'])), seed * 100 + i * 10 + j, seg=8, rings=4, rough=0.08)
        elif kind == 'loaf':
            for j in range(4): _bake_loaf(mb, F.p(x - 0.15 + 0.3 * (j % 2), 0.4 + 0.35 * (j // 2), zt), 0.18, rr.choice((M['loaf'], M['loaf_d'])), seed * 100 + i * 10 + j)
        else:
            mat, r_, cnt = dict(cab=(M['cabbage'], 0.2, 5), apple=(M['apple'], 0.1, 9), turnip=(M['turnip'], 0.12, 7), carrot=(M['carrot'], 0.07, 9), onion=(M['onion'], 0.1, 8))[kind]
            for j in range(cnt):
                lumpy(mb, F.p(x - 0.25 + 0.5 * rr.random(), 0.35 + 0.6 * rr.random(), zt + r_ * 0.8 + (r_ * 1.2 if j >= cnt - 2 else 0)), r_, mat if (kind != 'cab' or j % 2) else M['cabbage_d'], seed * 100 + i * 10 + j, seg=8, rings=5, rough=0.15)
    for j in range(3):                                                                         # produce on the ground in front
        x = rr.uniform(0.3, w - 0.3); F.box(mb, (x - 0.35, -0.9, 0), (x + 0.35, -0.3, 0.45), M['crate'], 1.0)
        for q in range(4): lumpy(mb, F.p(x - 0.15 + 0.3 * (q % 2), -0.75 + 0.3 * (q // 2), 0.6), 0.2, M['cabbage'] if q % 2 else M['cabbage_d'], seed * 7 + j * 5 + q, seg=8, rings=5, rough=0.2)
    if fire:
        c = F.p(w + 0.6, -0.4, 0); rod(mb, c, c + Vector((0, 0, 0.9)), 0.08, M['iron'], seg=6)
        for k in range(3):
            a = 2 * math.pi * k / 3; beam(mb, c + Vector((0.45 * math.cos(a), 0.45 * math.sin(a), 0)), c + Vector((0, 0, 0.9)), 0.05, 0.05, M['iron'])
        rod(mb, c + Vector((0, 0, 0.9)), c + Vector((0, 0, 1.3)), 0.35, M['iron'], seg=12, r1=0.45)
        fb = MB(); fc = c + Vector((0, 0, 1.25))
        for k in range(2):
            u = Vector((math.cos(k * math.pi / 2), math.sin(k * math.pi / 2), 0)) * 0.45
            fb.face([fc - u, fc + u, fc + u + Vector((0, 0, 0.75)), fc - u + Vector((0, 0, 0.75))], M['fire'], [(0, 0), (1, 0), (1, 1), (0, 1)])
        fb.quad(fc - Vector((0.38, 0.38, -0.02)), (0.76, 0, 0), (0, 0.76, 0), M['embers'], (0, 0, 1, 1))
        _halo(fb, fc + Vector((0, 0, 0.35)), 1.3, M)
        _obj(fb, name + '_fire', SET, shadow=False)
        L = _light(name + '_brazier', tuple(fc + Vector((0, 0, 0.5))), FIRE, 700, radius=0.4, shadow=False); STATE['fire_lights'].append((L, 700))
    _obj(mb, name, SET, hull=0.015); _obj(cards, name + '_awning', SET, hull=0.0)

def _market(SET, P, M, dress):
    mb = MB(); mb.quad((-150, -150, 0), (300, 0, 0), (0, 300, 0), M['cobbles'], (-37.5, -37.5, 37.5, 37.5)); _obj(mb, 'ground', SET)
    # north row (front y 24, facing -y): origins at the left corner, yaw 0
    x = -26.0; k = 0
    for (w, v, gab, sign, third) in ((6.0, 0, True, None, False), (6.5, 1, True, ('sign_tankard', 1), True), (5.5, 2, False, None, False), (7.0, 3, True, ('sign_pretzel', 1), True),
                                     (6.0, 0, True, None, False), (6.0, 2, False, ('sign_boot', 1), False), (6.5, 1, True, None, True), (6.0, 3, True, None, False), (5.5, 0, False, None, False)):
        house(SET, 'n_%d' % k, (x, 24.0, 0), 0, w, v, M, d=8, gable=gab, sign=sign, third=third, seed=100 + k); x += w + 0.05; k += 1
    # west row (front x -22, facing +x): yaw 90 -> local +x = world +y; origin at the south end.  Henry's bakery in the middle.
    y = -14.0; k = 0
    for (w, v, gab, sign, bake) in ((6.0, 1, True, None, None), (5.5, 3, False, ('sign_fish', 1), None), (7.0, 'bk', True, ('sign_bread', 1), 'henry'), (6.0, 2, True, None, None),
                                    (6.5, 0, False, None, None), (6.0, 3, True, None, None)):
        F = house(SET, 'w_%d' % k, (-22.0, y, 0), 90, w, v, M, d=8, gable=gab, sign=sign, shop_glow=bool(bake), seed=200 + k)
        if bake: bakery_front(SET, 'henry_front', F, w, M, seed=7); STATE['henry_front'] = (F.p(w - 1.1, -1.0, 0), F)
        y += w + 0.05; k += 1
    # east row (front x 22, facing -x): yaw -90 -> local +x = world -y; origin at the north end. The neighbour bakery (pilloried) here.
    y = 22.0; k = 0
    for (w, v, gab, sign, bake) in ((6.0, 2, True, None, None), (6.5, 0, True, ('sign_pretzel', 1), 'nb'), (5.5, 1, False, None, None), (6.0, 3, True, ('sign_tankard', 1), None),
                                    (6.5, 2, False, None, None), (6.0, 0, True, None, None)):
        F = house(SET, 'e_%d' % k, (22.0, y, 0), -90, w, v, M, d=8, gable=gab, sign=sign, shop_glow=bool(bake), seed=300 + k)
        if bake: bakery_front(SET, 'nb_front', F, w, M, seed=9)
        y -= w + 0.05; k += 1
    # south row (front y -16, facing +y; yaw 180, origin at the east end), with a gap for the lane at x -3..3
    for (x, w, v, gab) in ((24.0, 6.0, 1, True), (18.0, 6.5, 3, False), (11.4, 6.0, 0, True), (5.3, 6.0, 2, True), (-3.2, 6.0, 1, False), (-9.3, 6.5, 0, True), (-15.9, 6.0, 3, True)):
        house(SET, 's_%d' % int(x), (x, -16.0, 0), 180, w, v, M, d=8, gable=gab, seed=400 + int(x))
    _pillory(SET, M); _big_scale(SET, M); _well(SET, M)
    for (nm, o, yaw, w, awn, cl, fire) in (('stall_a', (-19.5, 12.6, 0), 90, 3.4, 'awn_red', 'cloth_red', False), ('stall_b', (-10.5, 21.3, 0), 0, 3.6, 'awn_green', 'cloth_green', True),
                                           ('stall_c', (8.0, 21.3, 0), 0, 3.4, 'awn_blue', 'cloth_blue', False), ('stall_d', (19.5, 5.6, 0), -90, 3.6, 'awn_yellow', 'cloth_red', True),
                                           ('stall_e', (19.5, 15.7, 0), -90, 3.2, 'awn_red', 'cloth_blue', False), ('stall_f', (-19.5, -9.9, 0), 90, 3.4, 'awn_blue', 'cloth_green', False),
                                           ('stall_g', (1.0, 21.3, 0), 0, 3.0, 'awn_yellow', 'cloth_red', False)):
        _stall(SET, nm, Frame(o, yaw), w, M, awn, cl, seed=sum(map(ord, nm)), fire=fire)
    if dress: _market_dressing(SET, M)

def _pillory(SET, M):
    """Wooden pillory on a platform: platform 4 x 4 D (z 0..1), steps on the south side, a post with the hinged double board
    (head hole between two hand holes, at neck height for a 3 D adult standing on the platform), a padlock, a sign board,
    rotten vegetables splattered on the platform."""
    cx, cy = PILLORY; mb = MB(); rr = _rnd(21); zp = PLAT_H
    mb.box((cx - 2.0, cy - 2.0, 0), (cx + 2.0, cy + 2.0, zp), M['timber_l'], mats=dict(top=M['floorb']), tile=(1, 1))
    for k in range(3): mb.box((cx - 0.9, cy - 2.0 - 0.45 * (k + 1), 0), (cx + 0.9, cy - 2.0 - 0.45 * k, zp * (3 - k) / 4), M['wood'], tile=(1, 1))
    for (x, y) in ((cx - 2.0, cy - 2.0), (cx + 2.0, cy - 2.0), (cx - 2.0, cy + 2.0), (cx + 2.0, cy + 2.0)):
        rod(mb, (x, y, 0), (x, y, zp + 0.9), 0.1, M['wood_d'], seg=6)
    for s in (-1, 1):
        beam(mb, (cx + s * 2.0, cy - 2.0, zp + 0.85), (cx + s * 2.0, cy + 2.0, zp + 0.85), 0.08, 0.08, M['wood_d'])
    beam(mb, (cx - 2.0, cy + 2.0, zp + 0.85), (cx + 2.0, cy + 2.0, zp + 0.85), 0.08, 0.08, M['wood_d'])
    # post and boards
    rod(mb, (cx, cy + 0.3, zp), (cx, cy + 0.3, zp + 3.6), 0.17, M['timber'], seg=8)
    nz = zp + 2.05; bw = 1.6
    for (z0, z1) in ((nz - 0.32, nz), (nz, nz + 0.3)):
        mb.box((cx - bw, cy + 0.05, z0), (cx + bw, cy + 0.2, z1 - 0.01), M['timber_l'], tile=(0.6, 0.6))
    holes = [(cx, 0.21), (cx - 0.95, 0.12), (cx + 0.95, 0.12)]
    for (hx, r_) in holes:
        rod(mb, (hx, cy + 0.03, nz), (hx, cy + 0.22, nz), r_, M['dark'], seg=12)
    mb.box((cx + bw - 0.15, cy + 0.0, nz - 0.08), (cx + bw - 0.05, cy + 0.05, nz + 0.12), M['iron'])
    rod(mb, (cx - bw, cy + 0.12, nz), (cx - bw - 0.12, cy + 0.12, nz), 0.05, M['iron'], seg=6)
    mb.box((cx - 0.6, cy + 0.18, zp + 3.0), (cx + 0.6, cy + 0.24, zp + 3.5), M['wood'])
    # splattered rotten vegetables
    for k in range(14):
        x = cx + rr.uniform(-1.8, 1.8); y = cy + rr.uniform(-1.8, 1.0)
        lumpy(mb, (x, y, zp + 0.03), rr.uniform(0.1, 0.22), rr.choice((M['rotten'], M['tomato'], M['cabbage_d'])), 500 + k, seg=8, rings=3, rough=0.4, squash=0.35)
    for k in range(8):
        x = cx + rr.uniform(-3, 3); y = cy - 2.5 + rr.uniform(-2, 0.5)
        lumpy(mb, (x, y, 0.02), rr.uniform(0.08, 0.18), rr.choice((M['rotten'], M['tomato'], M['cabbage_d'])), 600 + k, seg=8, rings=3, rough=0.4, squash=0.4)
    _obj(mb, 'pillory', SET, hull=0.02)
    # lanterns on the platform corners (warm, lit by day too)
    fl = MB(); hb = MB(); lm = MB()
    for (x, y) in ((cx - 2.0, cy + 2.0), (cx + 2.0, cy + 2.0)):
        rod(lm, (x, y, zp + 0.9), (x, y, zp + 2.6), 0.06, M['wood_d'], seg=6)
        c = Vector((x, y, zp + 2.85)); obox(lm, c, (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.16, 0.16, 0.22, M['iron'])
        fl.box(c - Vector((0.13, 0.13, 0.17)), c + Vector((0.13, 0.13, 0.17)), M['flame'])
        rod(lm, c + Vector((0, 0, 0.22)), c + Vector((0, 0, 0.42)), 0.2, M['iron'], seg=8, r1=0.02)
        _halo(hb, c, 0.8, M)
        _light('pillory_lamp_%d' % int(x), tuple(c), CANDLE, 90, radius=0.15, shadow=False)
    _obj(lm, 'pillory_lamps', SET, hull=0.012); _obj(fl, 'pillory_lamp_glass', SET, shadow=False); _obj(hb, 'pillory_halos', SET, shadow=False)
    STATE['pillory'] = dict(platform_z=zp, neck=(cx, cy + 0.12, nz), hands=[(cx - 0.95, cy + 0.12, nz), (cx + 0.95, cy + 0.12, nz)], stand=(cx, cy + 0.45, zp),
                            board=dict(x=(cx - bw, cx + bw), z=(nz - 0.32, nz + 0.3), y=(cy + 0.05, cy + 0.2)), steps=(cx, cy - 3.3, 0.0))

def _big_scale(SET, M):
    """The big public balance: an A-frame of two heavy posts with braces on a stone base, a carved crossbeam pivot (set_big_scale),
    royal banners hanging from the frame, two big pans (R 1.0) on three chains each; the bread pan (x 3) holds the loaf pile
    (set_loaves 0..13), the weights pan (x 9) a stack of iron weights stamped with the crown; a chest of weights beside it."""
    cx, cy = BIG_SCALE; mb = MB(); zp = BIG_PIV_Z
    mb.box((cx - 1.4, cy - 1.4, 0), (cx + 1.4, cy + 1.4, 0.45), M['stone_x'], tile=(4, 4))
    for s in (-1, 1):
        beam(mb, (cx, cy + s * 1.2, 0.45), (cx, cy + s * 0.25, zp + 0.6), 0.32, 0.32, M['timber'], up=(1, 0, 0))
        beam(mb, (cx - 0.9, cy + s * 0.9, 0.45), (cx, cy + s * 0.75, 2.4), 0.16, 0.16, M['timber'], up=(1, 0, 0))
        beam(mb, (cx + 0.9, cy + s * 0.9, 0.45), (cx, cy + s * 0.75, 2.4), 0.16, 0.16, M['timber'], up=(1, 0, 0))
    obox(mb, (cx, cy, zp + 0.75), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.35, 0.55, 0.16, M['timber'])
    rod(mb, (cx, cy - 0.6, zp), (cx, cy + 0.6, zp), 0.09, M['iron'], seg=8)
    mb.sphere((cx, cy, zp + 1.05), 0.2, M['brass'], seg=10, rings=6)                                        # gilt finial / crown
    for k in range(5):
        a = 2 * math.pi * k / 5; rod(mb, (cx, cy, zp + 1.15), (cx + 0.18 * math.cos(a), cy + 0.18 * math.sin(a), zp + 1.45), 0.04, M['brass'], seg=5)
    _obj(mb, 'big_scale_frame', SET, hull=0.025)
    bn = MB()                                                                                                  # banners on a rail under the pivot
    for (s, nm) in ((-1, 'ban_king'), (1, 'ban_king')):
        x = cx; y = cy + s * 0.62
        rod(bn, (cx - 0.45, y, zp - 0.6), (cx + 0.45, y, zp - 0.6), 0.03, M['iron'], seg=5)
        bn.oface([(cx - 0.45, y, zp - 0.6 - 2.3), (cx + 0.45, y, zp - 0.6 - 2.3), (cx + 0.45, y, zp - 0.6), (cx - 0.45, y, zp - 0.6)], M[nm], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, s, 0))
        bn.oface([(cx - 0.45, y + s * 0.01, zp - 0.6 - 2.3), (cx + 0.45, y + s * 0.01, zp - 0.6 - 2.3), (cx + 0.45, y + s * 0.01, zp - 0.6), (cx - 0.45, y + s * 0.01, zp - 0.6)], M[nm], [(1, 0), (0, 0), (0, 1), (1, 1)], (0, -s, 0))
    _obj(bn, 'big_scale_banners', SET, hull=0.0)
    piv = G._pivot('big_beam_pivot', SET, (cx, cy, zp)); bm = MB()
    obox(bm, (cx, cy, zp), (1, 0, 0), (0, 1, 0), (0, 0, 1), BIG_ARM + 0.25, 0.16, 0.22, M['timber'], 0.5)
    for s in (-1, 1):
        bm.sphere((cx + s * (BIG_ARM + 0.25), cy, zp), 0.2, M['brass'], seg=10, rings=5)
        rod(bm, (cx + s * BIG_ARM, cy - 0.2, zp), (cx + s * BIG_ARM, cy + 0.2, zp), 0.07, M['iron'], seg=6)
    rod(bm, (cx, cy - 0.2, zp + 0.2), (cx, cy - 0.2, zp + 0.9), 0.04, M['brass'], seg=6, r1=0.01)            # pointer
    ob = _obj(bm, 'big_beam', SET, hull=0.025); G._parent(ob, piv)
    pans = []
    for s, nm in ((-1, 'big_pan_bread'), (1, 'big_pan_weights')):
        hx = cx + s * BIG_ARM; pe = G._pivot(nm, SET, (hx, cy, zp)); pb = MB(); pzz = zp - BIG_PAN_DROP
        for k in range(3):
            a = 2 * math.pi * k / 3 + 0.5; pts = [Vector((hx, cy, zp)).lerp(Vector((hx + 1.0 * math.cos(a), cy + 1.0 * math.sin(a), pzz + 0.25)), t / 10) for t in range(11)]
            chain_rod(pb, pts, 0.025, M['iron'])
        rod(pb, (hx, cy, pzz), (hx, cy, pzz + 0.25), 0.9, M['brass'], seg=20, r1=1.08)
        rod(pb, (hx, cy, pzz + 0.22), (hx, cy, pzz + 0.27), 1.1, M['brass'], seg=20)
        if s > 0:
            for k, (dx, dy, r_, h) in enumerate(((0, 0, 0.4, 0.4), (0.45, 0.35, 0.3, 0.3), (-0.42, 0.3, 0.3, 0.3), (0.1, -0.5, 0.28, 0.28), (0.0, 0.0, 0.26, 0.26))):
                z0 = pzz + 0.25 + (0.4 if k == 4 else 0); rod(pb, (hx + dx, cy + dy, z0), (hx + dx, cy + dy, z0 + h), r_, M['iron'], seg=12, r1=r_ * 0.85)
                rod(pb, (hx + dx, cy + dy, z0 + h), (hx + dx, cy + dy, z0 + h + 0.08), 0.06, M['iron'], seg=6)
        po = _obj(pb, nm + '_mesh', SET, hull=0.02); G._parent(po, pe); pans.append(pe)
    # the loaf pile: 13 loaves (a pyramid of 12 + the 13th on top), each its own object (set_loaves shows the first n)
    hx = cx - BIG_ARM; pzz = zp - BIG_PAN_DROP + 0.25; spots = []
    for i in range(7): a = 2 * math.pi * i / 7; spots.append((hx + 0.62 * math.cos(a), cy + 0.62 * math.sin(a), pzz))
    for i in range(4): a = 2 * math.pi * i / 4 + 0.4; spots.append((hx + 0.32 * math.cos(a), cy + 0.32 * math.sin(a), pzz + 0.2))
    spots.append((hx, cy, pzz + 0.42)); spots.append((hx + 0.05, cy - 0.12, pzz + 0.62))
    loaves = []; rr = _rnd(23)
    for i, p in enumerate(spots):
        lb = MB(); _bake_loaf(lb, p, 0.3 if i < 12 else 0.28, M['loaf'] if i != 12 else M['loaf_p'], 5000 + i, yaw=rr.uniform(0, 3))
        lo = _obj(lb, 'big_loaf_%02d' % (i + 1), SET, hull=0.012); G._parent(lo, pans[0]); loaves.append(lo)
    STATE['big'] = dict(pivot=piv, pans=pans, loaves=loaves, arm=BIG_ARM, pz=zp)
    # weights chest and a basket (the inspector's) beside the scale
    d = MB(); d.box((cx + 1.8, cy - 2.4, 0), (cx + 3.0, cy - 1.6, 0.8), M['wood_d'], tile=(1, 1)); d.box((cx + 1.75, cy - 2.45, 0.8), (cx + 3.05, cy - 1.55, 0.9), M['iron'])
    for k in range(3): rod(d, (cx + 2.1 + 0.35 * k, cy - 2.0, 0.9), (cx + 2.1 + 0.35 * k, cy - 2.0, 1.1 + 0.05 * k), 0.12, M['iron'], seg=8)
    _obj(d, 'weights_chest', SET, hull=0.015)

def _well(SET, M):
    cx, cy = WELL; mb = MB()
    rod(mb, (cx, cy, 0), (cx, cy, 1.2), 1.3, M['stone_x'], seg=20, uv=(8, 1.2)); rod(mb, (cx, cy, 1.2), (cx, cy, 1.35), 1.42, M['stone_x'], seg=20)
    mb.quad((cx - 1.1, cy - 1.1, 0.9), (2.2, 0, 0), (0, 2.2, 0), M['water'])
    for s in (-1, 1): rod(mb, (cx + s * 1.25, cy, 1.2), (cx + s * 1.25, cy, 3.6), 0.1, M['timber'], seg=6)
    rod(mb, (cx - 1.4, cy, 2.6), (cx + 1.4, cy, 2.6), 0.14, M['wood'], seg=8)
    F = Frame((cx - 1.7, cy, 3.5), 0)
    for s in (-1, 1): F.quad(mb, [(0, 0, 0.6), (3.4, 0, 0.6), (3.4, s * 1.3, 0), (0, s * 1.3, 0)], M['thatch'], [(0, 0), (1.7, 0), (1.7, 0.7), (0, 0.7)], (0, s, 1))
    rod(mb, (cx + 0.3, cy, 2.55), (cx + 0.3, cy, 1.8), 0.012, M['rope'], seg=4); rod(mb, (cx + 0.3, cy, 1.8), (cx + 0.3, cy, 1.4), 0.22, M['wood'], seg=10, r1=0.25)
    _obj(mb, 'well', SET, hull=0.02)

def _market_dressing(SET, M):
    """Bunting strung across the square, banners on poles, hay bales, barrels, sacks, crates, a hand cart, baskets of rotten vegetables
    by the pillory (the crowd's ammunition), a notice post with the ASSIZE OF BREAD, hitching posts."""
    rr = _rnd(31); bt = MB(); mb = MB(); cards = MB()
    cols = [M['red'], M['cream'], M['blue'], M['green'], M['basket']]
    for (p0, p1, sag) in (((-21.5, 18, 7.6), (21.5, 14, 7.6), 1.4), ((-21.5, 8, 7.6), (21.5, 20, 7.8), 1.6), ((-21.5, 0, 7.4), (21.5, 4, 7.6), 1.5), ((-14, 23.4, 7.6), (-21.4, 10, 7.4), 1.0),
                          ((14, 23.4, 7.6), (21.4, 8, 7.6), 1.0), ((-21.5, -6, 7.4), (6, 23.4, 8.0), 2.0)):
        pts = catenary(p0, p1, sag, 40); chain_rod(bt, pts, 0.02, M['rope'])
        for i in range(len(pts) - 1):
            a, b = pts[i], pts[i + 1]; mid = (a + b) / 2 - Vector((0, 0, 0.55))
            bt.face([a, b, mid], cols[i % len(cols)], [(0, 0), (1, 0), (0.5, 1)]); bt.face([b, a, mid], cols[i % len(cols)], [(0, 0), (1, 0), (0.5, 1)])
    _obj(bt, 'bunting', SET, hull=0.0)
    for (x, y, nm) in ((-8.5, 13.5, 'ban_town'), (12.5, 12.0, 'ban_guild'), (-13.5, 4.0, 'ban_town'), (13.0, -2.0, 'ban_guild')):
        rod(mb, (x, y, 0), (x, y, 7.0), 0.08, M['wood_d'], seg=6); mb.sphere((x, y, 7.05), 0.12, M['brass'], seg=8, rings=4)
        rod(mb, (x, y, 6.6), (x + 1.1, y, 6.6), 0.035, M['iron'], seg=5)
        for s in (-1, 1): cards.oface([(x + 0.05, y + s * 0.01, 6.6 - 2.6), (x + 1.1, y + s * 0.01, 6.6 - 2.6), (x + 1.1, y + s * 0.01, 6.6), (x + 0.05, y + s * 0.01, 6.6)], M[nm], [(0, 0), (1, 0), (1, 1), (0, 1)] if s < 0 else [(1, 0), (0, 0), (0, 1), (1, 1)], (0, s, 0))
    # notice post by the scale
    rod(mb, (9.6, 2.6, 0), (9.6, 2.6, 3.2), 0.12, M['timber'], seg=8); cards.quad((9.15, 2.47, 1.8), (0.9, 0, 0), (0, 0, 1.17), M['notice'], (0, 0, 1, 1))
    # hay bales, barrels, sacks, crates around the edges
    for (x, y) in ((-17.5, 9.0), (-16.6, 9.4), (-17.0, 9.2)):
        obox(mb, (x, y, 0.45 if x != -17.0 else 1.35), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.8, 0.5, 0.45, M['thatch'])
    for (x, y) in ((15.5, 19.5), (16.4, 19.9), (-15.0, -11.0), (-14.2, -11.4), (8.5, -12.0)):
        rod(mb, (x, y, 0), (x, y, 1.4), 0.5, M['wood'], seg=12, r1=0.5)
        for z in (0.2, 1.1): rod(mb, (x, y, z), (x, y, z + 0.06), 0.52, M['iron'], seg=12)
    for (x, y, s) in ((12.0, -10.0, 0.5), (12.8, -10.4, 0.45), (-6.5, 19.5, 0.5), (16.0, 7.0, 0.5)):
        obox(mb, (x, y, s), (1, 0, 0), (0, 1, 0), (0, 0, 1), s, s, s, M['crate'])
    for i, (x, y) in enumerate(((-7.0, 6.5), (-1.0, 6.8), (-6.3, 11.5))):                             # baskets of rotten veg by the pillory
        _basket(mb, (x, y, 0), 0.45, 0.45, dict(M, loaf=M['rotten'], loaf_d=M['tomato'], loaf_p=M['cabbage_d']), loaves=7, seed=800 + i)
    # hand cart with sacks
    cx, cy = 14.0, 17.0
    mb.box((cx - 1.2, cy - 0.8, 1.0), (cx + 1.2, cy + 0.8, 1.15), M['wood'], tile=(1, 1))
    for s in (-1, 1):
        mb.box((cx - 1.2, cy + s * 0.8 - 0.05, 1.15), (cx + 1.2, cy + s * 0.8 + 0.05, 1.6), M['wood_d'])
        rod(mb, (cx, cy + s * 0.95, 0.75), (cx, cy + s * 1.05, 0.75), 0.75, M['wood_d'], seg=16)
        beam(mb, (cx - 1.2, cy + s * 0.6, 1.05), (cx - 3.0, cy + s * 0.5, 0.3), 0.1, 0.1, M['wood'])
    for k in range(3): obox(mb, (cx - 0.6 + 0.6 * k, cy, 1.55), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.3, 0.45, 0.35, M['sack'])
    # hitching posts and a water trough
    for x in (-18.0, -18.0): pass
    mb.box((-19.5, -11.0, 0), (-16.5, -10.2, 0.8), M['wood_d'], tile=(1, 1)); mb.quad((-19.4, -10.9, 0.7), (2.8, 0, 0), (0, 0.6, 0), M['water'])
    _obj(mb, 'market_dressing', SET, hull=0.015); _obj(cards, 'market_cards', SET, hull=0.0)

# ============================================================================= animatable hooks
def set_steam(level, frame=None):
    """Steam wisps 0 (none) .. 1 (full) .. 1.5 (thick). The wisps scroll upward continuously: with frame=N the scroll offset is keyed
    (linear) at N from the frame number, so sparse keys still rise smoothly; the strength is keyed linear too."""
    level = max(0.0, float(level)); STATE['steam_level'] = level
    for mn in ('steam', 'steam2'):
        m = STATE['M'].get(mn)
        if m is None: continue
        nt = m.node_tree; kv = nt.nodes.get('steam_k'); kv.outputs[0].default_value = 0.85 * level
        mp = nt.nodes.get('scroll'); f = frame if frame is not None else bpy.context.scene.frame_current
        mp.inputs['Location'].default_value[1] = -0.012 * f * (1.0 if mn == 'steam' else 0.8)
        if frame is not None:
            kv.outputs[0].keyframe_insert('default_value', frame=frame); mp.inputs['Location'].keyframe_insert('default_value', index=1, frame=frame)
            for fc in T._fcurves(nt):
                for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    for o in STATE.get('steam', []):
        o.hide_render = level <= 0.001
        if frame is not None: T._key(o, 'hide_render', frame)

def _flick(frame, seed=0):
    t = float(frame or 0)
    return 1.0 + 0.10 * math.sin(t * 0.83 + seed) + 0.07 * math.sin(t * 2.31 + 1.7 * seed) + 0.05 * math.sin(t * 5.1 + 0.3 * seed)

def set_oven(k=1.0, frame=None):
    """Oven fire (and the braziers / bakery-front fires in the market) 0 out .. 1 roaring .. 1.5 flaring. Deterministic flicker from the
    frame number (call every frame of a shot; keys linear): light energies, the fire / ember emission, the mouth halo."""
    k = max(0.0, float(k)); f = frame if frame is not None else bpy.context.scene.frame_current; fl = _flick(f)
    for i, (L, base) in enumerate(STATE.get('fire_lights', [])):
        L.data.energy = base * k * _flick(f, i + 1)
        if frame is not None: T._key(L.data, 'energy', frame, 'LINEAR')
    for m, base in ((STATE['M'].get('fire'), 4.0), (STATE['M'].get('embers'), 2.6)):
        if m is None: continue
        s = m.node_tree.nodes['strength'].inputs['Strength']; s.default_value = base * k * fl
        if frame is not None:
            s.keyframe_insert('default_value', frame=frame)
            for fc in T._fcurves(m.node_tree):
                for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    m = STATE['M'].get('halo_big')
    if m is not None:
        v = m.node_tree.nodes['fire_glow'].outputs[0]; v.default_value = 1.1 * k * fl
        if frame is not None:
            v.keyframe_insert('default_value', frame=frame)
            for fc in T._fcurves(m.node_tree):
                for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    STATE['oven_k'] = k
set_fire = set_oven

def _set_balance(info, angle_deg, frame, axis='y'):
    """Rotate a beam pivot by angle (deg, + = the FIRST pan (bread / loaf) goes down) and move the pan pivots to the beam ends (pans
    stay level). Keys rotation + locations (Bezier) with frame."""
    a = math.radians(angle_deg); piv = info['pivot']; c = Vector(piv['wrest']); L = info['arm']
    piv.rotation_euler = (0.0, -a, 0.0)                                        # -a about +y lowers the -x end
    if frame is not None: T._key(piv, 'rotation_euler', frame, 'BEZIER')
    for s, pe in zip((-1, 1), info['pans']):
        end = c + Vector((s * L * math.cos(a), 0.0, s * L * math.sin(a)))
        pe.location = end
        if frame is not None: T._key(pe, 'location', frame, 'BEZIER')

def set_scale(angle_deg, frame=None):
    """Small hand balance on the bakery counter: beam tilt in degrees, + = the loaf pan (left, -x) down, - = the weights pan down.
    Useful: +-8 (clear tilt), 0 level. Keys Bezier with frame (key the start too)."""
    if 'small' in STATE: _set_balance(STATE['small'], angle_deg, frame)

def set_scale_loaf(visible, frame=None):
    """Show / hide the loaf on the small balance's left pan (visibility keyed constant)."""
    if 'small' in STATE: T._show([STATE['small']['loaf']], bool(visible), frame)

def set_big_scale(angle_deg, frame=None):
    """Big public balance in the market: beam tilt in degrees, + = the bread pan (x 3, -x side) down = passes; - = the weights pan
    (x 9) down = the bread is short. Story: -7 (does not move), then ease to +6 when the 13th loaf goes on. Keys Bezier with frame."""
    if 'big' in STATE: _set_balance(STATE['big'], angle_deg, frame)

def set_loaves(count, frame=None, which='big'):
    """Loaves on the big balance's bread pan: count 0..13 shows the first count (7 round the rim, 4 inside, the 12th on top; the
    13th is a paler loaf on the very top). Visibility keyed constant with frame. which='small': 0 / 1 = the loaf on the hand balance."""
    if which == 'small': return set_scale_loaf(count > 0, frame)
    if 'big' not in STATE: return
    n = int(max(0, min(13, count)))
    for i, lo in enumerate(STATE['big']['loaves']): T._show([lo], i < n, frame)
    STATE['loaves'] = n

# ============================================================================= anchors, cameras
CAMS_B = dict(
    bakery_wide=dict(loc=(5.9, 0.7, 3.5), look_at=(-2.2, 9.6, 2.1), lens=22),
    counter=dict(loc=(0.55, -3.9, 2.5), look_at=(1.2, 4.0, 3.1), lens=22),
    table_insert=dict(loc=(3.1, 2.1, 2.55), look_at=(4.55, 4.0, 1.55), lens=26),
    small_scale_insert=dict(loc=(1.55, 2.15, 2.0), look_at=(2.4, 0.75, 1.75), lens=26),
    window_out=dict(loc=(0.6, 6.8, 2.7), look_at=(1.0, -6.0, 3.2), lens=22),
)
CAMS_M = dict(
    market_wide=dict(loc=(11.0, -14.5, 15.5), look_at=(-3.0, 9.0, 1.0), lens=22),
    square_eye=dict(loc=(1.2, -4.5, 2.6), look_at=(0.6, 12.0, 4.0), lens=22),
    pillory_low=dict(loc=(-1.2, 4.9, 0.9), look_at=(-4.0, 9.5, 3.4), lens=22),
    big_scale_insert=dict(loc=(2.3, 1.3, 2.5), look_at=(3.0, 6.0, 3.7), lens=24),
    run_lane=dict(loc=(3.4, 4.3, 1.3), look_at=(-21.0, 4.6, 2.8), lens=22),
)
CAM_NOTES = dict(
    bakery_wide='inside, from the front-right corner at eye level looking to the oven at the back-left: the roaring mouth, flour sacks, beams with herbs and the candle wheel, the table right, sun shafts from the counter opening and door',
    counter='from the street, over the let-down shutter board (loaves, baskets) into the shop: Henry and the boy behind the inside counter, the hand balance, shelves of loaves and the oven glow behind them; jetty and sign at the top',
    table_insert='ECU over the cooling loaves on the flour-dusted table, steam rising (set_steam), the candle at the table end, oven glow beyond',
    small_scale_insert='ECU on the hand balance on the counter (set_scale): loaf pan left, weights right, the sunny street through the opening behind',
    window_out='from deep in the shop looking out through the counter opening to the sunny street: houses opposite, a stall; actors at the counter in silhouette-ish warm light',
    market_wide='high establishing from the south-east: the square, the pillory on its platform, the big balance with royal banners, stalls, bunting, jettied houses all round, the town and castle on the backdrop',
    square_eye='eye level from the south of the square looking north: the big balance right of centre, the pillory left, bunting overhead, stalls and the north row',
    pillory_low='low among the crowd looking up at the pillory: the platform, the board with its three holes against the north row and sky; lanterns',
    big_scale_insert='close, slightly low on the big balance: the bread pan with the loaf pile (set_loaves) low centre, the beam and pivot with the crown above, banners',
    run_lane='low at the balance looking west down the lane through the crowd to Henry\'s bakery front (glowing door and shop opening, bread sign): the boy runs toward the camera',
)

def anchors():
    P = STATE['P']; loc = STATE['loc']
    base = dict(location=loc, preset=STATE['preset'], render=dict(samples_final=12, resolution=(720, 1280), threads=2, denoise='OIDN', dof=None), key_dir=tuple(Vector(P['key_dir']).normalized()),
                sun_elevation_deg=P['sun_elev'], floor_z=0.0)
    if loc == 'bakery':
        a, b, c, d = COUNTER_OPEN
        base.update(cams={k: dict(v) for k, v in CAMS_B.items()}, cam_notes={k: CAM_NOTES[k] for k in CAMS_B},
                    room=dict(x=(ROOM[0], ROOM[1]), y=(ROOM[2], ROOM[3]), ceiling=CEIL, front_wall_y=(-WALL_T, 0.0)),
                    counter=dict(x=(a, b), y=(0.0, 1.3), top_z=COUNTER_Z, opening=dict(x=(a, b), z=(c, d)), shutter_board=dict(x=(a - 0.1, b + 0.1), y=(-1.55, -0.5), z=c)),
                    door=dict(x=DOOR_OPEN[:2], z=(0.0, DOOR_OPEN[3]), lower_leaf_top=2.0), window=dict(x=WIN_OPEN[:2], z=WIN_OPEN[2:]),
                    oven=dict(centre=OVEN_C, radius=OVEN_R, plinth_z=OVEN_BASE, mouth=tuple(round(v, 3) for v in STATE['mouth']), front_y=round(STATE['oven_front_y'], 3)),
                    table=dict(x=(TABLE[0] - 0.85, TABLE[0] + 0.85), y=TABLE[1:3], top_z=TABLE[3], loaves=[tuple(round(v, 3) for v in p) for p in STATE['table_loaves']]),
                    small_scale=dict(foot=SMALL_SCALE, pivot=(SMALL_SCALE[0], SMALL_SCALE[1], round(STATE['small']['pz'], 3)), arm=STATE['small']['arm'], pan_drop=0.62, loaf_pan='-x', weights_pan='+x'),
                    marks=dict(henry_counter=(2.0, 2.0, 0.0), kit_counter=(-0.2, 1.85, 0.0), kit_table=(3.0, 5.4, 0.0), henry_oven=(-1.4, 4.6, 0.0), kit_sacks=(-4.6, 3.6, 0.0),
                               customer_street=(0.4, -2.6, 0.0), passers_street=[(-2.5, -6.0, 0.0), (3.5, -7.5, 0.0), (6.0, -5.0, 0.0)]),
                    lights=dict(oven=['L_oven_fire', 'L_oven_fill'], candles=[o.name for o in STATE['LIGHTS'].objects if o.name.startswith('L_candle')]),
                    keep_out='oven x -5.3..0.3 y > 6.3; table x 3.75..5.45 y 3..9.6; racks x > 5.9; sacks x < -5.2 y 1.5..4.6; trough x -6.3..-4.9 y 5..8; counter y 0..1.3 x -1.7..3.7; the candle wheel at (0.6, 5.2, 4.9) r 0.9')
    else:
        pl = STATE['pillory']; hf = STATE.get('henry_front')
        base.update(cams={k: dict(v) for k, v in CAMS_M.items()}, cam_notes={k: CAM_NOTES[k] for k in CAMS_M},
                    square=dict(x=(-22.0, 22.0), y=(-16.0, 24.0)), pillory=dict(pl), big_scale=dict(base=BIG_SCALE, pivot=(BIG_SCALE[0], BIG_SCALE[1], BIG_PIV_Z), arm=BIG_ARM,
                    bread_pan_top=(BIG_SCALE[0] - BIG_ARM, BIG_SCALE[1], round(BIG_PIV_Z - BIG_PAN_DROP + 0.25, 3)), weights_pan_top=(BIG_SCALE[0] + BIG_ARM, BIG_SCALE[1], round(BIG_PIV_Z - BIG_PAN_DROP + 0.25, 3)),
                    pan_radius=1.05, note='pan tops move with set_big_scale: dz = -+ arm sin(angle)'),
                    henry_front=dict(door=tuple(round(v, 3) for v in hf[0]) if hf else None, faces='+x'), well=WELL,
                    marks=dict(inspector=(4.0, 3.9, 0.0), henry=(1.3, 3.6, 0.0), kit_scale=(2.6, 4.4, 0.0), guard1=(-5.8, 6.0, 0.0), guard2=(-2.2, 6.2, 0.0),
                               baker2_in_pillory=pl['stand'], crowd=[(-8.0, 3.0, 0.0), (-6.5, 1.5, 0.0), (-10.5, 5.5, 0.0), (-1.5, 2.0, 0.0), (0.5, 0.5, 0.0), (-4.5, 3.4, 0.0), (8.5, 3.0, 0.0), (9.5, 1.0, 0.0), (-12.5, 2.2, 0.0)],
                               run_lane=[(-19.5, 4.6, 0.0), (-14.0, 4.6, 0.0), (-8.5, 4.5, 0.0), (-3.0, 4.6, 0.0), (1.5, 5.0, 0.0)],
                               lane_crowd=[(-16.0, 3.0, 0.0), (-15.0, 6.3, 0.0), (-11.0, 2.9, 0.0), (-10.0, 6.4, 0.0), (-6.0, 2.8, 0.0), (-5.5, 6.5, 0.0), (-1.0, 3.0, 0.0)]),
                    keep_out='houses (|x| > 21.5, y > 23.5, y < -15.5), stalls along the edges, the pillory platform x -6..-2 y 7.5..11.5 (+ steps to y 6.2), the big balance base x 4.6..7.4 y 4.6..7.4 and its pans (r 1.1 at x 3 / 9, y 6), the well r 1.5 at (-12, -3), hay (-17.5, 9), the cart (14, 17)')
    return base

# ----------------------------------------------------------------------------- placeholder actors (stills and tests only)
T.PH.update(
    kit=('beach_kid', dict(yaw=-0.3, expr='determined', arm_r='down', arm_l='down', legs='stand'), 2.4),
    henry=('boss', dict(yaw=0.35, head_roll=-4, expr='smug', arm_l='down', arm_r='hip', legs='stand'), 3.1),
    inspector=('senior_b', dict(yaw=0.2, expr='neutral', arm_l='down', arm_r='down', legs='stand'), 3.4),
    guard=('senior_a', dict(yaw=0.3, expr='neutral', arm_l='down', arm_r='down', legs='stand'), 3.2),
    woman=('beach_woman', dict(yaw=-0.25, expr='neutral', arm_l='down', arm_r='down', legs='stand'), 2.9),
    man=('beach_man', dict(yaw=0.25, expr='neutral', arm_l='down', arm_r='down', legs='stand'), 3.0))
placeholder_actor = T.placeholder_actor
HEIGHT = dict(kit=2.4, henry=3.1, inspector=3.4, guard=3.2, woman=2.9, man=3.0)

STAGING = dict(
    bakery_wide=[('kit', (-0.6, 5.4, 0)), ('henry', (2.3, 3.4, 0))],
    counter=[('kit', (-0.2, 1.85, 0)), ('henry', (2.0, 2.0, 0))],
    table_insert=[], small_scale_insert=[],
    window_out=[('kit', (0.2, 2.6, 0)), ('man', (-2.5, -6.0, 0)), ('woman', (3.5, -7.5, 0))],
    market_wide=[('inspector', (4.0, 3.9, 0)), ('henry', (1.3, 3.6, 0)), ('kit', (-3.0, 4.6, 0)), ('guard', (-5.8, 6.0, 0)), ('woman', (-8.0, 3.0, 0)), ('man', (-1.5, 2.0, 0)), ('woman', (8.5, 3.0, 0))],
    square_eye=[('inspector', (4.0, 3.9, 0)), ('henry', (1.3, 3.6, 0)), ('kit', (2.6, 2.4, 0)), ('guard', (-5.8, 6.0, 0)), ('woman', (-1.5, 2.0, 0)), ('man', (-3.5, 3.0, 0))],
    pillory_low=[('guard', (-7.4, 11.8, 0)), ('man', (-1.0, 8.2, 0))],
    big_scale_insert=[],
    run_lane=[('kit', (-6.5, 4.6, 0)), ('woman', (-11.0, 2.9, 0)), ('man', (-10.0, 6.4, 0)), ('woman', (-6.0, 2.8, 0)), ('man', (-5.5, 6.5, 0)), ('henry', (-1.0, 3.0, 0))],
)

def stage_placeholders(A, cam_name, cam_loc):
    """Placeholder actors for the contract stills (STAGING[cam_name]); cards face the camera. Returns the actor objects."""
    T._clear_actors()
    out = []
    for i, (role, mk) in enumerate(STAGING.get(cam_name, [])):
        d = Vector(cam_loc) - Vector(mk); el = math.degrees(math.atan2(d.z - 1.5, math.hypot(d.x, d.y)))
        out.append(placeholder_actor(role, mk, face_to=cam_loc, tilt=max(0.0, el - 35) * 0.6, name='actor_%s_%d' % (role, i)))
    return out

def head_pixels(cam_name):
    """For the staged placeholders of a camera: [(role, mark, head_centre_px_y (0 = top), head_px)] at 720x1280 (caption check)."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; cam = sc.camera; out = []
    for i, (role, mk) in enumerate(STAGING.get(cam_name, [])):
        h = HEIGHT[role]; top = Vector(mk) + Vector((0, 0, h)); hc = Vector(mk) + Vector((0, 0, h - 0.5)); bot = Vector(mk) + Vector((0, 0, h - 1.0))
        p, q, b = (world_to_camera_view(sc, cam, v) for v in (hc, top, bot))
        out.append((role, mk, round((1 - p.y) * 1280), round(abs(q.y - b.y) * 1280), round((1 - Vector(world_to_camera_view(sc, cam, Vector(mk))).y) * 1280)))
    return out

def apply_cam_state(cam, preset):
    """Set-state of the contract stills: bakery steam 0.8 (table / counter), oven 1; small_scale_insert tilted +6 (loaf down); market
    big balance -7 with 12 loaves (the short dozen) in market_wide / square_eye, +6 with 13 in big_scale_insert."""
    if STATE['loc'] == 'bakery':
        set_steam(1.0 if cam == 'table_insert' else 0.8); set_oven(1.0); set_scale(6.0 if cam == 'small_scale_insert' else 0.0)
    else:
        set_oven(1.0)
        if cam == 'big_scale_insert': set_big_scale(6.0); set_loaves(13)
        else: set_big_scale(-7.0); set_loaves(12)

# ----------------------------------------------------------------------------- CLI
def _load(): return ' '.join('%.2f' % v for v in os.getloadavg())

def cli_render(loc, preset=None, cams=None, quality='final', outdir=None, actors=True):
    outdir = outdir or os.path.join(WORK, 'final' if quality == 'final' else 'stills'); os.makedirs(outdir, exist_ok=True)
    preset = preset or LOC_PRESETS[loc][0]
    A = build(loc, preset); sc = bpy.context.scene; setup_render(sc, quality); res = {}
    for nm, cs in A['cams'].items():
        if cams and nm not in cams: continue
        apply_cam_state(nm, preset); make_camera(cs)
        if actors: stage_placeholders(A, nm, cs['loc'])
        bpy.context.view_layer.update(); hp = head_pixels(nm)
        w, c = render(os.path.join(outdir, '%s_%s_%s.png' % (loc, preset, nm))); res[nm] = (round(w, 1), round(c, 1), hp)
        print('%s %s %s %s: %.1f s wall, %.1f s cpu, load %s, heads %s' % (quality, loc, preset, nm, w, c, _load(), hp), flush=True)
    return res

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'; arg = sys.argv[2:]
    if cmd in ('final', 'stills'):
        cli_render(arg[0] if arg else 'bakery', arg[1] if len(arg) > 1 else None, arg[2:] or None, 'final' if cmd == 'final' else 'preview')
    elif cmd == 'digest':
        A = build(arg[0] if arg else 'bakery', arg[1] if len(arg) > 1 else None); bpy.context.view_layer.update(); print('digest', digest())
    else: print(__doc__)

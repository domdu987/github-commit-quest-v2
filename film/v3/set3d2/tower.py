#!/usr/bin/env python3
"""tower.py : set 1 of film 2, the bell tower (campanile) of San Nazaro, Brescia 1769, as a real 3D Blender set (bpy 5.3, Cycles CPU).

    import tower as T
    A = T.build("DAY")                 # DAY | DUSK | NIGHT_STORM | NIGHT_CALM -> anchors dict (marks, rod, bell, cameras)
    T.set_rod(1)                       # 0 no rod, 1 iron rod nailed to the finial, 2 rod + wire down the tower wall
    T.set_bell(25, frame=10)           # bell swing in degrees (keyframed when frame is given)
    T.flash(1.0, frame=40); T.set_bolt(True, frame=40, target="tower")      # NIGHT_STORM lightning
    cam = T.make_camera(A["cams"]["square_low"])

World: 1 unit = 1 D (head diameter), Z up, square level z = 0. Tower centred on x = y = 0, 4.5 D square; its front faces the
square toward -y. The church is to the right (+x) of the tower, houses to the left, the cobbled square in front (-y).
Modelled on v3/set3d/office3d.py (geometry from code, SVG artwork rasterised by Chromium, inverted-hull ink, one hard key,
ambient as emission, anchors, make_camera, setup_render, placeholder actors). See tower_API.md.
CLI: python3 tower.py stills [preset ...] | timing | measure | digest"""
import os, sys, math, json, time, random, subprocess, hashlib
import bpy
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import tower_tex as TT                                     # noqa: E402
WORK = os.path.join(HERE, 'tower_work'); ACT = os.path.join(WORK, 'actors')

# ----------------------------------------------------------------------------- dimensions (D)
TW = 2.25                    # half width of the tower (4.5 D square)
Z_CH = 15.0                  # chamber floor (stage) level
Z_CORN = 21.4                # cornice bottom (top of the chamber walls)
Z_TERR = 21.9                # terrace / cornice top
WALL_T = 0.40                # chamber wall thickness
OW = 1.3                     # half width of the arched openings
Z_SILL = Z_CH + 0.75; Z_SPRING = Z_CH + 4.0     # opening sill and spring line; arch top = Z_SPRING + OW
Z_AXLE = Z_CH + 5.6          # bell axle
BELL_D = 2.2
Z_SPIRE0, Z_SPIRE1, Z_APEX = 23.5, 23.65, 27.6
ROD_BASE = (0.10, 0.0, 27.95); ROD_TIP = (0.10, 0.0, 29.45); FINIAL_TOP = (0.0, 0.0, 28.45)
CH_MARKS = dict(hero_mark=(0.55, 0.6, Z_CH), priest_mark=(-0.75, -0.7, Z_CH), extra_marks=[(1.2, -0.45, Z_CH), (-1.15, 0.85, Z_CH)])
SQ_MARKS = dict(hero=(-0.9, -11.0, 0.0), priest=(1.3, -10.2, 0.0), extra1=(-3.4, -9.4, 0.0), extra2=(3.6, -12.2, 0.0), extra3=(-5.2, -13.0, 0.0))
WIRE_X = -(TW + 0.2); WIRE_Y = -1.75

# ----------------------------------------------------------------------------- presets
# displayed (scene-linear) = art * gain * KEY * vis * toon(cos) + (art * SHADE * shade_mul + LIFT) * (1 + dot(N, form))
# toon(cos) = (k0 + (1 - k0) cos) / max(cos, COS_MIN): a face square to the key gets the full key, a grazing face k0 of it.
PRESETS = {
    'DAY': dict(key=(1.31, 1.08, 0.28), shade_tint=(0.15, 0.14, 0.43), shade_mix=0.7, key_desat=0.0, key_dir=(0.45, 0.75, -1.0), sun_angle=0.5, shade=(0.085, 0.16, 0.50), lift=(0.004, 0.004, 0.016),
                form=(0.0, -0.05, 0.22), toon=0.55, sky='day', pano='day', sky_k=0.72, pano_k=0.85, night=False, ink='#2a1712',
                inner=0.6, win_k=0.0, lamp_k=0.0, grade_offset=(0.003, 0.002, 0.008), grade_saturation=1.08, bloom_size=0.05),
    'DUSK': dict(key=(1.55, 1.02, 0.26), shade_tint=(0.21, 0.165, 0.56), shade_mix=0.7, key_desat=0.0, key_dir=(0.60, 0.75, -0.36), sun_angle=0.6, shade=(0.17, 0.13, 0.42), lift=(0.008, 0.004, 0.02),
                 form=(0.0, -0.05, 0.2), toon=0.5, sky='dusk', pano='dusk', sky_k=0.9, pano_k=0.9, night=False, ink='#2a1712',
                 inner=0.6, win_k=0.6, lamp_k=0.8, grade_offset=(0.004, 0.002, 0.009), grade_saturation=1.06, bloom_size=0.05),
    'NIGHT_STORM': dict(key=(0.14, 0.24, 0.62), shade_tint=(0.06, 0.075, 0.30), shade_mix=0.75, key_desat=0.65, key_dir=(0.55, 0.50, -0.80), sun_angle=0.7, shade=(0.05, 0.075, 0.27), lift=(0.004, 0.006, 0.024),
                        form=(0.0, -0.05, 0.2), toon=0.55, sky='storm', pano='night', sky_k=0.9, pano_k=0.75, night=True, ink='#1d1449',
                        inner=0.8, win_k=1.6, lamp_k=2.6, flash_e=2.2, grade_offset=(0.002, 0.003, 0.012), grade_saturation=1.05, bloom_size=0.05),
    'NIGHT_CALM': dict(key=(0.20, 0.31, 0.74), shade_tint=(0.075, 0.095, 0.36), shade_mix=0.75, key_desat=0.6, key_dir=(0.55, 0.50, -0.80), sun_angle=0.6, shade=(0.07, 0.10, 0.34), lift=(0.004, 0.006, 0.024),
                       form=(0.0, -0.05, 0.2), toon=0.55, sky='night', pano='night', sky_k=1.0, pano_k=0.85, night=True, ink='#1d1449',
                       inner=0.8, win_k=1.5, lamp_k=2.4, flash_e=3.2, grade_offset=(0.002, 0.003, 0.012), grade_saturation=1.05, bloom_size=0.05),
}
STATE = {}
COS_MIN = 0.12

def hex_lin(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)

# ----------------------------------------------------------------------------- materials (as office3d, plus the toon key term and a glow mask)
def _tree(m):
    nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    return nt

def _img(path):
    im = bpy.data.images.load(path, check_existing=True)
    if path not in STATE.setdefault('images', set()): im.reload(); STATE['images'].add(path)
    return im

def mat_lit(name, color='#808080', image=None, gain=1.0, shade_mul=1.0, alpha=False, form=None, glow=None, glow_k=0.0, interp='Linear', shade_mix=None):
    """Environment surface: Diffuse(art x gain x toon) lit by the one key + Emission(art x SHADE x shade_mul + LIFT) x (1 + N.form).
    glow = PNG of a glow mask (same UVs) added as emission x glow_k (lit windows at night)."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    P = STATE['P']; m = bpy.data.materials.new(name); nt = _tree(m); L = nt.links.new; N = nt.nodes.new
    out = N('ShaderNodeOutputMaterial'); dif = N('ShaderNodeBsdfDiffuse'); dif.inputs['Roughness'].default_value = 0.0
    kd = Vector(P['key_dir']).normalized(); geo = N('ShaderNodeNewGeometry')
    dot = N('ShaderNodeVectorMath'); dot.operation = 'DOT_PRODUCT'; dot.inputs[1].default_value = (-kd.x, -kd.y, -kd.z); L(geo.outputs['True Normal'], dot.inputs[0])
    cpos = N('ShaderNodeMath'); cpos.operation = 'MAXIMUM'; cpos.inputs[1].default_value = 0.0; L(dot.outputs['Value'], cpos.inputs[0])
    k0 = float(P.get('toon', 1.0))
    num = N('ShaderNodeMath'); num.operation = 'MULTIPLY_ADD'; num.inputs[1].default_value = (1.0 - k0) * gain; num.inputs[2].default_value = k0 * gain; L(cpos.outputs[0], num.inputs[0])
    mxn = N('ShaderNodeMath'); mxn.operation = 'MAXIMUM'; mxn.inputs[1].default_value = COS_MIN; L(dot.outputs['Value'], mxn.inputs[0])
    div = N('ShaderNodeMath'); div.operation = 'DIVIDE'; L(num.outputs[0], div.inputs[0]); L(mxn.outputs[0], div.inputs[1])
    emi = N('ShaderNodeEmission'); emi.inputs['Strength'].default_value = 1.0
    add = N('ShaderNodeAddShader')
    ms = N('ShaderNodeMix'); ms.data_type = 'RGBA'; ms.blend_type = 'MULTIPLY'; ms.inputs[0].default_value = 1.0
    sm = tuple(shade_mul) if isinstance(shade_mul, (tuple, list)) else (shade_mul,) * 3
    ms.inputs[7].default_value = (*[s * k for s, k in zip(P['shade'], sm)], 1.0)
    md = N('ShaderNodeVectorMath'); md.operation = 'SCALE'; L(div.outputs[0], md.inputs['Scale'])
    tex = None
    if image is not None:
        tex = N('ShaderNodeTexImage'); tex.image = _img(image); tex.interpolation = interp; art = tex.outputs['Color']
    else:
        rgb = N('ShaderNodeRGB'); rgb.outputs[0].default_value = (*hex_lin(color), 1.0); art = rgb.outputs[0]
    L(art, ms.inputs[6])
    bw = N('ShaderNodeRGBToBW'); L(art, bw.inputs[0])
    # key colour: the art desaturated toward its own luminance by key_desat (night: moonlight takes the colour out of the brick)
    kdm = N('ShaderNodeMix'); kdm.data_type = 'RGBA'; kdm.blend_type = 'MIX'; kdm.inputs[0].default_value = float(P.get('key_desat', 0.0))
    L(art, kdm.inputs[6]); L(bw.outputs[0], kdm.inputs[7]); L(kdm.outputs[2], md.inputs[0])
    # shade: (1 - m) x art x SHADE x shade_mul + m x lum(art) x TINT x mean(shade_mul): a painted blue-violet shade that keeps the
    # texture's value pattern but not its hue (red brick in blue sky light would otherwise turn magenta)
    mmix = float(P.get('shade_mix', 0.0) if shade_mix is None else shade_mix); smm = sum(sm) / 3.0
    sa = N('ShaderNodeVectorMath'); sa.operation = 'SCALE'; sa.inputs['Scale'].default_value = 1.0 - mmix; L(ms.outputs[2], sa.inputs[0])
    tb = N('ShaderNodeVectorMath'); tb.operation = 'SCALE'; L(bw.outputs[0], tb.inputs['Scale']); tb.inputs[0].default_value = tuple(x * mmix * smm for x in P.get('shade_tint', (0, 0, 0)))
    sab = N('ShaderNodeVectorMath'); sab.operation = 'ADD'; L(sa.outputs['Vector'], sab.inputs[0]); L(tb.outputs['Vector'], sab.inputs[1])
    lf = N('ShaderNodeVectorMath'); lf.operation = 'ADD'; lf.inputs[1].default_value = tuple(P.get('lift', (0, 0, 0))); L(sab.outputs['Vector'], lf.inputs[0])
    amb = lf.outputs['Vector']
    if form and any(abs(x) > 1e-6 for x in form):
        fd = N('ShaderNodeVectorMath'); fd.operation = 'DOT_PRODUCT'; fd.inputs[1].default_value = tuple(form); L(geo.outputs['True Normal'], fd.inputs[0])
        fa = N('ShaderNodeMath'); fa.operation = 'ADD'; fa.inputs[1].default_value = 1.0; L(fd.outputs['Value'], fa.inputs[0])
        fs = N('ShaderNodeVectorMath'); fs.operation = 'SCALE'; L(amb, fs.inputs[0]); L(fa.outputs[0], fs.inputs['Scale']); amb = fs.outputs['Vector']
    if glow is not None and glow_k > 0:
        gt = N('ShaderNodeTexImage'); gt.image = _img(glow); gs = N('ShaderNodeVectorMath'); gs.operation = 'SCALE'; gs.inputs['Scale'].default_value = glow_k
        L(gt.outputs['Color'], gs.inputs[0]); ga = N('ShaderNodeVectorMath'); ga.operation = 'ADD'; L(amb, ga.inputs[0]); L(gs.outputs['Vector'], ga.inputs[1]); amb = ga.outputs['Vector']
    L(amb, emi.inputs['Color'])
    L(md.outputs['Vector'], dif.inputs['Color'])
    L(dif.outputs['BSDF'], add.inputs[0]); L(emi.outputs['Emission'], add.inputs[1])
    last = add.outputs['Shader']
    if alpha and tex is not None:
        tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
        L(tex.outputs['Alpha'], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(last, mx.inputs[2]); last = mx.outputs['Shader']
    L(last, out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def mat_emit(name, color='#ffffff', image=None, strength=1.0, alpha=False, camera_only=False, additive=False):
    """Unlit surface (sky, painted plate, windows, bolt). strength > 1 feeds the bloom. Node 'strength' is the Emission node."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = _tree(m); L = nt.links.new
    out = nt.nodes.new('ShaderNodeOutputMaterial'); emi = nt.nodes.new('ShaderNodeEmission'); emi.name = 'strength'; emi.inputs['Strength'].default_value = strength
    tex = None
    if image is not None:
        tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = _img(image); L(tex.outputs['Color'], emi.inputs['Color'])
    else: emi.inputs['Color'].default_value = (*hex_lin(color), 1.0)
    last = emi.outputs['Emission']
    if additive:                                            # glow: transparent + emission (adds light over what is behind)
        tr = nt.nodes.new('ShaderNodeBsdfTransparent'); ad = nt.nodes.new('ShaderNodeAddShader'); L(tr.outputs['BSDF'], ad.inputs[0]); L(last, ad.inputs[1]); last = ad.outputs['Shader']
    if camera_only:
        lp = nt.nodes.new('ShaderNodeLightPath'); tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
        L(lp.outputs['Is Camera Ray'], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(last, mx.inputs[2]); last = mx.outputs['Shader']
    if alpha and tex is not None:
        tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
        L(tex.outputs['Alpha'], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(last, mx.inputs[2]); last = mx.outputs['Shader']
    L(last, out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def mat_card(name, image_path):
    """Actor card: the drawing exactly (emission to camera rays only, never lit), alpha cut-out, blocks the key."""
    m = bpy.data.materials.new(name); nt = _tree(m); L = nt.links.new
    out = nt.nodes.new('ShaderNodeOutputMaterial'); tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = _img(image_path); tex.extension = 'CLIP'
    lp = nt.nodes.new('ShaderNodeLightPath'); emi = nt.nodes.new('ShaderNodeEmission')
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mix = nt.nodes.new('ShaderNodeMixShader')
    L(tex.outputs['Color'], emi.inputs['Color']); L(lp.outputs['Is Camera Ray'], emi.inputs['Strength'])
    L(tex.outputs['Alpha'], mix.inputs['Fac']); L(tr.outputs['BSDF'], mix.inputs[1]); L(emi.outputs['Emission'], mix.inputs[2])
    L(mix.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def mat_ink(name='ink'):
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = _tree(m); L = nt.links.new
    out = nt.nodes.new('ShaderNodeOutputMaterial'); geo = nt.nodes.new('ShaderNodeNewGeometry'); lp = nt.nodes.new('ShaderNodeLightPath')
    emi = nt.nodes.new('ShaderNodeEmission'); emi.inputs['Color'].default_value = (*hex_lin(STATE['P']['ink']), 1.0)
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mix = nt.nodes.new('ShaderNodeMixShader')
    notcam = nt.nodes.new('ShaderNodeMath'); notcam.operation = 'SUBTRACT'; notcam.inputs[0].default_value = 1.0
    fac = nt.nodes.new('ShaderNodeMath'); fac.operation = 'MAXIMUM'
    L(lp.outputs['Is Camera Ray'], notcam.inputs[1]); L(geo.outputs['Backfacing'], fac.inputs[0]); L(notcam.outputs[0], fac.inputs[1])
    L(fac.outputs[0], mix.inputs['Fac']); L(emi.outputs['Emission'], mix.inputs[1]); L(tr.outputs['BSDF'], mix.inputs[2]); L(mix.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

# ----------------------------------------------------------------------------- mesh builder (office3d.MB plus oriented polygons)
class MB:
    def __init__(s): s.v = []; s.vi = {}; s.f = []; s.uv = []; s.mi = []; s.mats = []; s._in = False; s.pid = 0
    def _slot(s, mat):
        if mat not in s.mats: s.mats.append(mat)
        return s.mats.index(mat)
    def _vert(s, p):
        k = (s.pid, round(p[0], 5), round(p[1], 5), round(p[2], 5))
        if k not in s.vi: s.vi[k] = len(s.v); s.v.append(k[1:])
        return s.vi[k]
    def face(s, pts, mat, uvs=None):
        idx = [s._vert(p) for p in pts]
        if len(set(idx)) < 3: return
        s.f.append(idx); s.uv.append(uvs or [(0.0, 0.0)] * len(idx)); s.mi.append(s._slot(mat))
    def oface(s, pts, mat, uvs, normal):
        """Polygon whose winding is flipped if needed so that its normal points along `normal`."""
        pts = [Vector(p) for p in pts]; n = Vector((0, 0, 0))
        for i in range(len(pts)): a, b = pts[i], pts[(i + 1) % len(pts)]; n += a.cross(b)
        if n.dot(Vector(normal)) < 0: pts = pts[::-1]; uvs = uvs[::-1]
        s.pid += 1; s.face(pts, mat, uvs)
    def quad(s, p0, pu, pv, mat, uv=(0.0, 0.0, 1.0, 1.0)):
        p0, pu, pv = Vector(p0), Vector(pu), Vector(pv); u0, v0, u1, v1 = uv
        if not s._in: s.pid += 1
        s.face([p0, p0 + pu, p0 + pu + pv, p0 + pv], mat, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)])
    def box(s, lo, hi, mat, mats=None, tile=None, skip=''):
        x0, y0, z0 = lo; x1, y1, z1 = hi; dx, dy, dz = x1 - x0, y1 - y0, z1 - z0; mats = mats or {}; s.pid += 1; s._in = True
        faces = dict(front=((x0, y0, z0), (dx, 0, 0), (0, 0, dz), (x0, z0, dx, dz)), back=((x1, y1, z0), (-dx, 0, 0), (0, 0, dz), (-x1, z0, dx, dz)),
                     right=((x1, y0, z0), (0, dy, 0), (0, 0, dz), (y0, z0, dy, dz)), left=((x0, y1, z0), (0, -dy, 0), (0, 0, dz), (-y1, z0, dy, dz)),
                     top=((x0, y0, z1), (dx, 0, 0), (0, dy, 0), (x0, y0, dx, dy)), bottom=((x0, y1, z0), (dx, 0, 0), (0, -dy, 0), (x0, -y1, dx, dy)))
        for k, (p0, pu, pv, (a, b, w, h)) in faces.items():
            if k in skip.split(','): continue
            uv = (a / tile[0], b / tile[1], (a + w) / tile[0], (b + h) / tile[1]) if tile else (0.0, 0.0, 1.0, 1.0)
            s.quad(p0, pu, pv, mats.get(k, mat), uv)
        s._in = False
    def frustum(s, p0, p1, r0, r1, mat, seg=14, cap0=True, cap1=True, cap_mat=None, uv_wrap=None):
        p0, p1 = Vector(p0), Vector(p1); a = (p1 - p0).normalized(); s.pid += 1
        u = a.cross(Vector((0, 0, 1)))
        if u.length < 1e-4: u = Vector((1, 0, 0))
        u.normalize(); v = a.cross(u)
        ring = lambda p, r: [p + r * (math.cos(2 * math.pi * i / seg) * u + math.sin(2 * math.pi * i / seg) * v) for i in range(seg)]
        A, B = ring(p0, r0), ring(p1, r1)
        for i in range(seg):
            j = (i + 1) % seg
            uvs = None
            if uv_wrap: uvs = [(uv_wrap[0] * i / seg, 0), (uv_wrap[0] * (i + 1) / seg, 0), (uv_wrap[0] * (i + 1) / seg, uv_wrap[1]), (uv_wrap[0] * i / seg, uv_wrap[1])]
            s.face([A[i], A[j], B[j], B[i]], mat, uvs)
        if cap0 and r0 > 0: s.face(A[::-1], cap_mat or mat)
        if cap1 and r1 > 0: s.face(B, cap_mat or mat)
    def sphere(s, c, r, mat, seg=14, rings=8):
        c = Vector(c); R = []; s.pid += 1
        for k in range(rings + 1):
            th = math.pi * k / rings; R.append([c + Vector((r * math.sin(th) * math.cos(2 * math.pi * i / seg), r * math.sin(th) * math.sin(2 * math.pi * i / seg), -r * math.cos(th))) for i in range(seg)])
        for k in range(rings):
            for i in range(seg):
                j = (i + 1) % seg; s.face([R[k][i], R[k][j], R[k + 1][j], R[k + 1][i]], mat)
    def obj(s, name, coll, hull=0.0, smooth=False):
        me = bpy.data.meshes.new(name); me.from_pydata([Vector(v) for v in s.v], [], s.f); me.update()
        uvl = me.uv_layers.new(name='UVMap'); i = 0
        for fi, f in enumerate(s.f):
            for c in s.uv[fi]: uvl.data[i].uv = c; i += 1
        for mt in s.mats: me.materials.append(mt)
        for fi, p in enumerate(me.polygons): p.material_index = s.mi[fi]; p.use_smooth = smooth
        ob = bpy.data.objects.new(name, me); coll.objects.link(ob)
        if hull > 0: add_hull(ob, hull)
        STATE.setdefault('objects', {})[name] = ob
        return ob

def add_hull(ob, thickness):
    """Inverted-hull ink outline (camera rays only, even offset)."""
    ob.data.materials.append(mat_ink())
    mod = ob.modifiers.new('ink_hull', 'SOLIDIFY')
    mod.thickness = thickness; mod.offset = 1.0; mod.use_flip_normals = True; mod.use_rim = False
    mod.material_offset = len(ob.data.materials) - 1; mod.use_even_offset = True
    return mod

def hull(dist): return 0.00384 * dist          # 3 px ink at camera distance `dist`

def _coll(name, scene):
    c = bpy.data.collections.get(name)
    if c is None: c = bpy.data.collections.new(name)
    if name not in [k.name for k in scene.collection.children]: scene.collection.children.link(c)
    return c

def _wipe(coll):
    for ob in list(coll.objects): bpy.data.objects.remove(ob, do_unlink=True)

def no_bounce(ob):
    """Hide an object from bounce rays (as office3d): the frame is exactly ambient + one hard key. Call it on actor cards too."""
    ob.visible_diffuse = False; ob.visible_glossy = False; ob.visible_transmission = False; ob.visible_volume_scatter = False
    return ob

# ----------------------------------------------------------------------------- render settings
def setup_render(scene, quality='final'):
    """Cycles CPU, direct light only, Standard view, max 2 threads. 'final' 720x1280 12 samples; 'hq' the same at 16 samples;
    'preview' 360x640 6 samples."""
    r = scene.render; c = scene.cycles
    r.engine = 'CYCLES'; c.device = 'CPU'
    c.use_adaptive_sampling = False; c.use_denoising = False
    c.max_bounces = 1; c.diffuse_bounces = 0; c.glossy_bounces = 0; c.transmission_bounces = 0; c.volume_bounces = 0; c.transparent_max_bounces = 8
    c.caustics_reflective = False; c.caustics_refractive = False; c.sample_clamp_indirect = 3.0
    c.use_light_tree = False
    c.use_fast_gi = True; c.fast_gi_method = 'REPLACE'; c.ao_bounces_render = 1; c.ao_bounces = 1
    if scene.world: scene.world.light_settings.distance = 0.001
    vs = scene.view_settings; vs.view_transform = 'Standard'; vs.look = 'None'; vs.exposure = 0.0; vs.gamma = 1.0
    scene.display_settings.display_device = 'sRGB'
    r.film_transparent = False; r.resolution_x = 720; r.resolution_y = 1280; r.fps = 30
    r.image_settings.file_format = 'PNG'; r.image_settings.color_mode = 'RGB'; r.use_persistent_data = False
    r.threads_mode = 'FIXED'; r.threads = 2
    if quality in ('final', 'hq'): c.samples = 12 if quality == 'final' else 16; r.resolution_percentage = 100
    else: c.samples = 6; r.resolution_percentage = 50

def setup_grade(scene, bloom=True):
    """Compositor (spec/grade_compositor.py): tight bloom above 1.0, CDL black point, saturation. No vignette."""
    sys.path.insert(0, os.path.join(PROJ, 'spec'))
    import warnings
    import grade_compositor as G
    for ng in list(bpy.data.node_groups):
        if ng.name.startswith('GradeCLP'): bpy.data.node_groups.remove(ng)
    P = STATE['P']
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        ng = G.build(scene, preset=dict(vignette_strength=0.0, bloom_strength=0.5 if bloom else 0.0, bloom_size=P.get('bloom_size', 0.05),
                                        offset=tuple(P['grade_offset']), saturation=float(P['grade_saturation'])))
    scene.render.use_compositing = True
    return ng

# ----------------------------------------------------------------------------- walls with arched openings
def _arch_wall(mb, M, n, hw, z0, z1, ow=0.0, zs=0.0, zc=0.0, thick=WALL_T, tile=2.0, seg=12, ring=None, ring_w=0.28):
    """One wall of a square box centred on the z axis: outer face at distance hw along the outward normal n (unit, horizontal),
    inner face `thick` deeper. With ow > 0 a round-arched opening of half width ow, sill zs, spring line zc goes through it,
    with reveals (sill, jambs, soffit). M = dict(out, inn, rev). ring = material of a stone archivolt strip around the arch."""
    n = Vector(n); t = Vector((0, 0, 1)).cross(n); Z = Vector((0, 0, 1))
    def P(a, z, d, h=hw): return n * (h + d) + t * a + Z * z
    def polys(h):
        if ow <= 0: return [[(-h, z0), (h, z0), (h, z1), (-h, z1)]]
        out = [[(-h, z0), (-ow, z0), (-ow, z1), (-h, z1)], [(ow, z0), (h, z0), (h, z1), (ow, z1)], [(-ow, z0), (ow, z0), (ow, zs), (-ow, zs)]]
        for i in range(seg):
            a0, a1 = math.pi - math.pi * i / seg, math.pi - math.pi * (i + 1) / seg
            p0 = (ow * math.cos(a0), zc + ow * math.sin(a0)); p1 = (ow * math.cos(a1), zc + ow * math.sin(a1))
            out.append([p0, p1, (p1[0], z1), (p0[0], z1)])
        return out
    for pl in polys(hw): mb.oface([P(a, z, 0) for a, z in pl], M['out'], [(a / tile, z / tile) for a, z in pl], n)
    hi = hw - thick
    for pl in polys(hi): mb.oface([P(a, z, 0, hi) for a, z in pl], M['inn'], [(-a / tile, z / tile) for a, z in pl], -n)
    if ow <= 0: return
    d0, d1 = -thick, 0.0
    mb.oface([P(-ow, zs, d0), P(ow, zs, d0), P(ow, zs, d1), P(-ow, zs, d1)], M['rev'], [(0, 0), (2 * ow / tile, 0), (2 * ow / tile, thick / tile), (0, thick / tile)], Z)
    for sgn in (-1, 1):
        mb.oface([P(sgn * ow, zs, d0), P(sgn * ow, zc, d0), P(sgn * ow, zc, d1), P(sgn * ow, zs, d1)], M['rev'], [(zs / tile, 0), (zc / tile, 0), (zc / tile, thick / tile), (zs / tile, thick / tile)], t * (-sgn))
    for i in range(seg):
        a0, a1 = math.pi - math.pi * i / seg, math.pi - math.pi * (i + 1) / seg
        q0 = (ow * math.cos(a0), zc + ow * math.sin(a0)); q1 = (ow * math.cos(a1), zc + ow * math.sin(a1)); am = (a0 + a1) / 2
        nm = -(t * math.cos(am) + Z * math.sin(am))
        L0 = ow * (math.pi - a0); L1 = ow * (math.pi - a1)
        mb.oface([P(q0[0], q0[1], d0), P(q1[0], q1[1], d0), P(q1[0], q1[1], d1), P(q0[0], q0[1], d1)], M['rev'], [(L0 / tile, 0), (L1 / tile, 0), (L1 / tile, thick / tile), (L0 / tile, thick / tile)], nm)
    if ring is not None:                                    # archivolt: voussoir strip 0.035 proud, and jamb strips down to the sill
        dd = 0.035; Lt = 0.0
        for i in range(seg):
            a0, a1 = math.pi - math.pi * i / seg, math.pi - math.pi * (i + 1) / seg
            pa = [(r_ * math.cos(a), zc + r_ * math.sin(a)) for r_, a in ((ow, a0), (ow, a1), (ow + ring_w, a1), (ow + ring_w, a0))]
            L0 = (ow + ring_w / 2) * (math.pi - a0); L1 = (ow + ring_w / 2) * (math.pi - a1)
            mb.oface([P(a, z, dd) for a, z in pa], ring, [(L0, 0), (L1, 0), (L1, 1), (L0, 1)], n)
        for sgn in (-1, 1):
            xa, xb = sorted((sgn * ow, sgn * (ow + ring_w)))
            mb.oface([P(xa, zs, dd), P(xb, zs, dd), P(xb, zc, dd), P(xa, zc, dd)], ring, [(0, 0), (1, 0), (1, (zc - zs) / 0.3), (0, (zc - zs) / 0.3)], n)

FACES = [(0, -1, 0), (1, 0, 0), (0, 1, 0), (-1, 0, 0)]

def _band(mb, mat, hw, z0, z1, proud, tile_u=1.0, tile_v=None, sides=FACES):
    """A thin band (texture strip) proud of the four faces of a square box, wrapping round the corners."""
    for n in sides:
        n = Vector(n); t = Vector((0, 0, 1)).cross(n); h = hw + proud
        p0 = n * h - t * h + Vector((0, 0, z0)); mb.quad(p0, t * 2 * h, Vector((0, 0, z1 - z0)), mat, (0, 0, 2 * h / tile_u, 1 if tile_v is None else (z1 - z0) / tile_v))

def _ring_box(mb, mat, hw, z0, z1, proud, tile=None):
    """Closed square ring course (string course, cornice) proud of the four faces."""
    h = hw + proud; mb.box((-h, -h, z0), (h, h, z1), mat, tile=tile)

# ----------------------------------------------------------------------------- the set
def build(preset='DAY', clear=True):
    """Build the bell-tower set into the current scene (collections SET and LIGHTS, world, render settings, grade).
    Returns the anchors dict (tower_API.md). clear=True removes every object of the scene first."""
    scene = bpy.context.scene; P = dict(PRESETS[preset]); STATE.clear(); STATE['P'] = P; STATE['preset'] = preset
    if clear:
        for ob in list(scene.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for ac in list(bpy.data.actions):
        if ac.name.startswith(('TWR_', 'bell_pivot', 'rod', 'flash', 'bolt', 'wire', 'sky', 'pano')) or ac.users == 0: bpy.data.actions.remove(ac)
    SET = _coll('SET', scene); LIGHTS = _coll('LIGHTS', scene); _wipe(SET); _wipe(LIGHTS)
    for m in list(bpy.data.materials):
        if m.name.startswith(('TWR_', 'ink')): bpy.data.materials.remove(m)
    tx = TT.ensure(verbose=False)
    w = bpy.data.worlds.get('W_tower') or bpy.data.worlds.new('W_tower'); scene.world = w; nt = _tree(w)
    bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld'); bg.inputs['Color'].default_value = (0, 0, 0, 1); bg.inputs['Strength'].default_value = 0.0
    nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
    setup_render(scene, 'final'); scene.frame_start = 1; scene.frame_current = 1
    pre = 'TWR_' + preset + '_'; FORM = tuple(P['form']); inner = P['inner']; night = P['night']
    def _k(v): return 'x'.join('%g' % x for x in v) if isinstance(v, (tuple, list)) else '%g' % v
    def C(hexcol, gain=1.0, sm=1.0, form=True): return mat_lit('%sc_%s_%g_%s_%d' % (pre, hexcol.lstrip('#'), gain, _k(sm), form), hexcol, gain=gain, shade_mul=sm, form=FORM if form else None)
    def TX(name, gain=1.0, sm=1.0, alpha=False, form=True, glow=None, glow_k=0.0):
        return mat_lit('%st_%s_%g_%s_%d_%s' % (pre, name, gain, _k(sm), form, glow or ''), image=tx[name], gain=gain, shade_mul=sm, alpha=alpha, form=FORM if form else None,
                       glow=tx[glow] if glow else None, glow_k=glow_k)
    def E(name, hexcol=None, image=None, k=1.0, alpha=False, cam=False): return mat_emit(pre + 'e_' + name, hexcol or '#ffffff', image=tx[image] if image else None, strength=k, alpha=alpha, camera_only=cam)
    M = dict(brick=TX('brick'), brick_in=TX('brick_in', 1.0, inner), stone=TX('stone', 0.9), stone_in=TX('stone', 0.9, inner), vous=TX('vous', 0.9),
             archetti=TX('archetti'), roof=TX('roof'), roof_b=TX('roof_b'), scales=TX('scales'), cobbles=TX('cobbles', 1.0, 1.0, form=False),
             planks=TX('planks', 1.0, inner, form=False), beam=TX('beam', 1.0, inner), drum=TX('drum'), bell=mat_lit(pre + 'bell', image=tx['bell'], gain=0.95, shade_mul=(2.2, 1.3, 0.55), form=FORM, shade_mix=0.15),
             bell_in=mat_lit(pre + 'bell_in', '#6a3c1c', gain=0.8, shade_mul=(1.6 * inner, 1.0 * inner, 0.5 * inner), shade_mix=0.15), iron=C('#2c2a36', 1.0, 1.4), wood=C('#6e3a22', 1.0, inner), wood_out=C('#6e3a22'),
             rope=C('#d6b47a', 0.9, inner), copper=C('#d89a48', 0.9), ground=TX('ground', 1.0, form=False), clock=TX('clock', 0.9, alpha=True),
             church=TX('church_facade', 0.95), pl_cream=TX('pl_cream'), dark=C('#1e1830', 1.0, 0.6), stone_flat=C('#e2c590', 0.9))
    STATE['M'] = M
    shell_h = hull(14.0)

    # ---- ground: square (cobbles), ground disc to the plate
    mb = MB(); mb.quad((-22, -36, 0), (44, 0, 0), (0, 40, 0), M['cobbles'], (-11, -18, 11, 2)); mb.obj('square', SET)
    mb = MB(); seg = 64; R = 76.0
    for i in range(seg):
        a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg
        pts = [(0, 0, -0.03), (R * math.cos(a0), R * math.sin(a0), -0.03), (R * math.cos(a1), R * math.sin(a1), -0.03)]
        mb.face([Vector(p) for p in pts], M['ground'], [(p[0] / 10, p[1] / 10) for p in pts])
    g = mb.obj('ground', SET)

    # ---- tower shaft (z 0 .. Z_CH): brick, Lombard corner strips, string courses with hanging arches, plinth, slits, clock
    mb = MB()
    for n in FACES: _arch_wall(mb, dict(out=M['brick'], inn=M['brick_in'], rev=M['brick']), n, TW, 0.0, Z_CH, thick=0.3, tile=2.0)
    mb.obj('tower_shaft', SET, hull=shell_h)
    mb = MB()
    _ring_box(mb, M['stone'], TW, 0.0, 0.9, 0.16, tile=(2, 2))
    for zc in (5.0, 10.0, Z_CH - 0.25): _ring_box(mb, M['stone'], TW, zc, zc + 0.26, 0.13, tile=(2, 2))
    _ring_box(mb, M['stone'], TW, Z_CORN, Z_TERR, 0.32, tile=(2, 2))                       # cornice (its top is the terrace)
    mb.obj('tower_courses', SET, hull=shell_h)
    mb = MB()                                                                            # corner strips (lesene), brick, 0.07 proud
    for sx in (-1, 1):
        for sy in (-1, 1):
            x0, x1 = sorted((sx * (TW + 0.07), sx * (TW - 0.6))); y0, y1 = sorted((sy * (TW + 0.07), sy * (TW - 0.6)))
            for (za, zb) in ((0.9, 5.0), (5.26, 10.0), (10.26, Z_CH - 0.25)):
                mb.box((x0, y0, za), (x1, y1, zb), M['brick'], tile=(2.0, 1.92))
    mb.obj('tower_lesene', SET, hull=shell_h)
    mb = MB()                                                                            # hanging-arch bands under each course and under the cornice
    for zc in (5.0, 10.0, Z_CH - 0.25): _band(mb, M['archetti'], TW, zc - 0.5, zc, 0.015, 1.0)
    _band(mb, M['archetti'], TW, Z_CORN - 0.5, Z_CORN, 0.015, 1.0)
    mb.obj('tower_archetti', SET)
    mb = MB()                                                                            # dentils under the cornice
    for n in FACES:
        n = Vector(n); t = Vector((0, 0, 1)).cross(n)
        for k in range(16):
            a = -TW + 0.15 + k * (2 * TW - 0.3) / 15; c = n * (TW + 0.12) + t * a
            mb.box((c.x - 0.07, c.y - 0.07, Z_CORN - 0.14), (c.x + 0.07, c.y + 0.07, Z_CORN), M['stone_flat'])
    mb.obj('tower_dentils', SET)
    mb = MB()                                                                            # slit windows with stone frames on each face
    for n in FACES:
        n = Vector(n); t = Vector((0, 0, 1)).cross(n)
        for zc in (2.6, 7.5, 12.3):
            if n.y < 0 and zc == 12.3: continue                                          # the clock is there on the front
            c = n * (TW + 0.005) + Vector((0, 0, zc))
            mb.quad(c - t * 0.28 - Vector((0, 0, 0.75)), t * 0.56, Vector((0, 0, 1.5)), M['stone_flat'])
            mb.quad(c + n * 0.003 - t * 0.12 - Vector((0, 0, 0.6)), t * 0.24, Vector((0, 0, 1.2)), M['dark'])
    mb.obj('tower_slits', SET)
    mb = MB(); mb.quad((-0.85, -TW - 0.012, 12.3 - 0.85), (1.7, 0, 0), (0, 0, 1.7), M['clock']); mb.obj('tower_clock', SET)
    mb = MB(); mb.frustum((0, -TW - 0.002, 12.3), (0, -TW - 0.06, 12.3), 0.86, 0.86, M['stone_flat'], seg=24, cap1=False); mb.obj('tower_clock_rim', SET, hull=0.03)

    # ---- bell chamber: four arched walls, floor (the stage), ceiling, beams
    mb = MB(); MC = dict(out=M['brick'], inn=M['brick_in'], rev=M['stone_in'])
    for n in FACES: _arch_wall(mb, MC, n, TW, Z_CH, Z_CORN, OW, Z_SILL, Z_SPRING, ring=M['vous'])
    mb.obj('chamber_walls', SET, hull=hull(6.0))
    hi = TW - WALL_T
    mb = MB(); mb.box((-hi, -hi, Z_CH - 0.2), (hi, hi, Z_CH), M['planks'], tile=(2, 2)); mb.obj('chamber_floor', SET)
    mb = MB(); mb.quad((-1.62, 0.95, Z_CH + 0.004), (0.66, 0, 0), (0, 0.66, 0), M['dark']); mb.obj('trapdoor', SET)
    mb = MB(); mb.box((-1.6, 0.97, Z_CH), (-1.0, 1.02, Z_CH + 0.75), M['wood'], mats=dict(front=M['wood']));  # trapdoor lid standing open
    for x in (-1.55, -1.07): mb.box((x - 0.04, 1.2, Z_CH - 0.2), (x + 0.04, 1.28, Z_CH + 0.85), M['wood'])     # ladder rails
    mb.box((-1.6, 1.2, Z_CH + 0.45), (-1.02, 1.28, Z_CH + 0.52), M['wood'])
    mb.obj('ladder', SET, hull=hull(5.0))
    mb = MB(); mb.box((-hi, -hi, Z_CORN - 0.12), (hi, hi, Z_CORN - 0.02), M['planks'], tile=(2, 2)); mb.obj('chamber_ceiling', SET)
    mb = MB()
    for y in (-1.1, 0.0, 1.1): mb.box((-hi, y - 0.13, Z_CORN - 0.4), (hi, y + 0.13, Z_CORN - 0.12), M['beam'], mats=dict(front=M['beam'], back=M['beam']))
    for x in (-1.5, 1.5): mb.box((x - 0.14, -hi, Z_AXLE - 0.75), (x + 0.14, hi, Z_AXLE - 0.1), M['beam'], mats=dict(right=M['beam'], left=M['beam']))     # bell frame beams
    for x in (-1.5, 1.5):
        for y in (-1.6, 1.6): mb.box((x - 0.1, y - 0.1, Z_CH), (x + 0.1, y + 0.1, Z_AXLE - 0.75), M['wood'])    # posts
        mb.box((x - 0.12, -0.18, Z_AXLE - 0.1), (x + 0.12, 0.18, Z_AXLE - 0.05), M['iron'])                    # bearings
    mb.obj('bell_frame', SET, hull=hull(4.5))
    # rope that runs from the ceiling through the trapdoor (the second bell rope), lantern on a hook
    mb = MB(); mb.frustum((-1.3, 1.12, Z_CORN - 0.4), (-1.3, 1.12, Z_CH - 0.2), 0.028, 0.028, M['rope'], seg=6); mb.obj('rope_b', SET, hull=0.008)
    lx, ly, lz = -1.45, -1.35, Z_CH + 3.6
    mb = MB(); mb.frustum((lx, ly, lz + 0.35), (lx, ly, Z_CORN - 0.4), 0.012, 0.012, M['iron'], seg=5)
    mb.box((lx - 0.15, ly - 0.15, lz - 0.25), (lx + 0.15, ly + 0.15, lz - 0.2), M['iron']); mb.box((lx - 0.12, ly - 0.12, lz + 0.2), (lx + 0.12, ly + 0.12, lz + 0.26), M['iron'])
    mb.frustum((lx, ly, lz + 0.26), (lx, ly, lz + 0.38), 0.1, 0.0, M['iron'], seg=8)
    for (sx, sy) in ((-1, -1), (1, -1), (1, 1), (-1, 1)): mb.box((lx + sx * 0.13 - 0.015, ly + sy * 0.13 - 0.015, lz - 0.2), (lx + sx * 0.13 + 0.015, ly + sy * 0.13 + 0.015, lz + 0.2), M['iron'])
    mb.obj('lantern', SET, hull=0.01)
    mb = MB(); mb.box((lx - 0.11, ly - 0.11, lz - 0.2), (lx + 0.11, ly + 0.11, lz + 0.2), E('lantern', image='lantern', k=P['lamp_k'] if P['lamp_k'] > 0 else 0.35))
    o_ = mb.obj('lantern_glass', SET); o_.visible_shadow = False
    STATE['lantern'] = (lx, ly, lz)

    # ---- chamber dressing (clear of the marks): bucket, coiled spare rope, crate, broom, pigeons on the sills, a votive plaque
    mb = MB(); W_ = C('#7a4428', 1.0, inner); Wd = C('#5a2e1a', 1.0, inner); iron_in = C('#2c2a36', 1.0, 1.4 * inner)
    mb.frustum((1.45, 1.45, Z_CH), (1.45, 1.45, Z_CH + 0.42), 0.2, 0.25, W_, seg=12, cap1=False); mb.frustum((1.45, 1.45, Z_CH + 0.3), (1.45, 1.45, Z_CH + 0.34), 0.245, 0.245, iron_in, seg=12)
    mb.frustum((1.45, 1.45, Z_CH + 0.34), (1.45, 1.45, Z_CH + 0.36), 0.22, 0.22, C('#3a6ab8', 0.5, inner), seg=12)
    for k in range(5): mb.frustum((0.85, 1.5, Z_CH + k * 0.07), (0.85, 1.5, Z_CH + k * 0.07 + 0.07), 0.33 - 0.02 * k, 0.33 - 0.02 * k, M['rope'], seg=14, cap0=False, cap1=(k == 4))
    mb.box((-1.75, -0.05, Z_CH), (-1.25, 0.5, Z_CH + 0.45), W_); mb.box((-1.77, -0.07, Z_CH + 0.38), (-1.23, 0.52, Z_CH + 0.47), Wd)
    mb.frustum((1.72, -1.72, Z_CH + 0.05), (1.62, -1.6, Z_CH + 2.1), 0.025, 0.025, Wd, seg=6); mb.frustum((1.75, -1.75, Z_CH), (1.72, -1.72, Z_CH + 0.45), 0.12, 0.05, C('#c8a050', 0.8, inner), seg=8)
    mb.obj('chamber_props', SET, hull=hull(4.0))
    mb = MB(); pg = C('#7d84a8', 0.8); pw = C('#e8e2d6', 0.6)
    for (px, py, pz, rot) in ((0.75, TW - 0.15, Z_SILL, 0.4), (-0.55, TW - 0.2, Z_SILL, -0.6), (TW - 0.2, 0.9, Z_SILL, 1.9), (-1.95, -TW - 0.12, Z_TERR + 0.82, 2.6)):
        d = Vector((math.cos(rot), math.sin(rot), 0))
        mb.sphere((px, py, pz + 0.14), 0.13, pg, seg=10, rings=6); mb.sphere((px + d.x * 0.13, py + d.y * 0.13, pz + 0.3), 0.075, pg, seg=8, rings=5)
        mb.frustum((px + d.x * 0.2, py + d.y * 0.2, pz + 0.3), (px + d.x * 0.27, py + d.y * 0.27, pz + 0.29), 0.022, 0.0, C('#e0a040', 0.8), seg=5)
        mb.frustum((px - d.x * 0.1, py - d.y * 0.1, pz + 0.14), (px - d.x * 0.32, py - d.y * 0.32, pz + 0.08), 0.07, 0.02, pw, seg=6)
    mb.obj('pigeons', SET, hull=0.01)

    # ---- the bell on its headstock (pivot at the axle; set_bell rotates it about x)
    piv = bpy.data.objects.new('bell_pivot', None); SET.objects.link(piv); piv.location = (0, 0, Z_AXLE); STATE['objects']['bell_pivot'] = piv
    prof = [(1.1, 0.0), (1.1, 0.1), (1.03, 0.24), (0.92, 0.5), (0.83, 0.9), (0.78, 1.3), (0.74, 1.62), (0.64, 1.88), (0.42, 1.99), (0.0, 2.04)]
    inner_p = [(1.0, 0.06), (0.9, 0.3), (0.76, 0.9), (0.67, 1.55), (0.42, 1.85), (0.0, 1.9)]
    rim_z = -(Z_AXLE - (Z_CH + 3.35))                                                 # rim 3.35 D above the floor
    seg = 28; mb = MB(); acc = [0.0]
    for a, b in zip(prof, prof[1:]): acc.append(acc[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    def ringp(r, h, i): a = 2 * math.pi * i / seg; return Vector((r * math.cos(a), r * math.sin(a), rim_z + h))
    mb.pid += 1
    for k in range(len(prof) - 1):
        for i in range(seg):
            v0, v1 = acc[k] / acc[-1], acc[k + 1] / acc[-1]
            mb.face([ringp(*prof[k], i), ringp(*prof[k], i + 1), ringp(*prof[k + 1], i + 1), ringp(*prof[k + 1], i)], M['bell'], [(i / seg, v0), ((i + 1) / seg, v0), ((i + 1) / seg, v1), (i / seg, v1)])
    for k in range(len(inner_p) - 1):
        for i in range(seg): mb.face([ringp(*inner_p[k], i + 1), ringp(*inner_p[k], i), ringp(*inner_p[k + 1], i), ringp(*inner_p[k + 1], i + 1)], M['bell_in'])
    for i in range(seg): mb.face([ringp(1.1, 0.0, i + 1), ringp(1.1, 0.0, i), ringp(1.0, 0.06, i), ringp(1.0, 0.06, i + 1)], M['bell_in'])
    bell = mb.obj('bell', SET, hull=hull(4.5), smooth=False); bell.parent = piv
    mb = MB(); mb.frustum((0, 0, rim_z + 1.85), (0, 0, rim_z + 0.45), 0.045, 0.045, M['iron'], seg=8); mb.sphere((0, 0, rim_z + 0.35), 0.17, M['iron'], seg=12, rings=6)
    for i in range(6):                                                                 # crown loops
        a = math.pi * i / 3; mb.box((0.25 * math.cos(a) - 0.06, 0.25 * math.sin(a) - 0.06, rim_z + 2.02), (0.25 * math.cos(a) + 0.06, 0.25 * math.sin(a) + 0.06, -0.24), M['bell'])
    cl = mb.obj('bell_clapper', SET, hull=0.01); cl.parent = piv
    mb = MB(); mb.box((-1.3, -0.28, -0.26), (1.3, 0.28, 0.3), M['beam'], mats=dict(front=M['beam'], back=M['beam']))     # headstock
    for x in (-0.55, 0.55): mb.box((x - 0.06, -0.3, -0.28), (x + 0.06, 0.3, 0.32), M['iron'])                           # straps
    mb.frustum((-1.66, 0, 0), (1.66, 0, 0), 0.07, 0.07, M['iron'], seg=10)                                               # axle
    mb.box((0.85, 0.2, -0.1), (1.0, 1.05, 0.1), M['wood'])                                                               # rope lever
    rope_x, rope_y = 0.93, 1.0
    mb.frustum((rope_x, rope_y, 0.0), (rope_x, rope_y, -(Z_AXLE - Z_CH) + 1.05), 0.03, 0.03, M['rope'], seg=6)
    sally = (Z_CH + 1.55, Z_CH + 2.15)
    for k in range(6):                                                                   # the sally: striped woollen grip
        z0_ = sally[0] + k * 0.1 - Z_AXLE; mb.frustum((rope_x, rope_y, z0_), (rope_x, rope_y, z0_ + 0.1), 0.075, 0.075, C('#c8322a', 0.8, inner) if k % 2 else C('#f0e2c0', 0.5, inner), seg=8)
    hs = mb.obj('headstock', SET, hull=hull(4.5)); hs.parent = piv
    STATE['rope'] = (rope_x, rope_y)

    # ---- terrace parapet (balustrade) and the spire with its finial
    mb = MB(); e = TW + 0.24
    for (x0, y0, x1, y1) in ((-e, -e, e, -e + 0.2), (-e, e - 0.2, e, e), (-e, -e, -e + 0.2, e), (e - 0.2, -e, e, e)):
        mb.box((x0, y0, Z_TERR), (x1, y1, Z_TERR + 0.1), M['stone_flat']); mb.box((x0 - 0.02, y0 - 0.02, Z_TERR + 0.68), (x1 + 0.02, y1 + 0.02, Z_TERR + 0.82), M['stone_flat'])
    for sx in (-1, 1):
        for sy in (-1, 1):
            mb.box((sx * e - 0.17, sy * e - 0.17, Z_TERR), (sx * e + 0.17, sy * e + 0.17, Z_TERR + 0.92), M['stone_flat'])
    mb.obj('parapet', SET, hull=0.02)
    mb = MB()
    for n in FACES:
        n = Vector(n); t = Vector((0, 0, 1)).cross(n)
        for k in range(12):
            a = -e + 0.33 + k * (2 * e - 0.66) / 11; c = n * (e - 0.1) + t * a
            mb.frustum((c.x, c.y, Z_TERR + 0.1), (c.x, c.y, Z_TERR + 0.36), 0.05, 0.085, M['stone_flat'], seg=6)
            mb.frustum((c.x, c.y, Z_TERR + 0.36), (c.x, c.y, Z_TERR + 0.68), 0.085, 0.045, M['stone_flat'], seg=6)
    for sx in (-1, 1):
        for sy in (-1, 1): mb.sphere((sx * e, sy * e, Z_TERR + 1.05), 0.13, M['stone_flat'], seg=8, rings=5)
    mb.obj('balusters', SET, hull=0.012)
    mb = MB(); mb.box((-TW - 0.1, -TW - 0.1, Z_TERR - 0.001), (TW + 0.1, TW + 0.1, Z_TERR + 0.012), M['stone'], tile=(2, 2), skip='bottom'); mb.obj('terrace', SET)
    def octo(r, z, k): a = math.radians(22.5 + 45 * k); return Vector((r * math.cos(a), r * math.sin(a), z))
    mb = MB(); rd = 1.5                                                                   # drum
    for k in range(8):
        mb.oface([octo(rd, Z_TERR, k), octo(rd, Z_TERR, k + 1), octo(rd, Z_SPIRE0, k + 1), octo(rd, Z_SPIRE0, k)], M['drum'], [(0, 0), (1, 0), (1, 1), (0, 1)], (octo(1, 0, k) + octo(1, 0, k + 1)))
    mb.obj('spire_drum', SET, hull=hull(6.0))
    mb = MB(); re_ = 1.78
    for k in range(8):
        mb.oface([octo(re_, Z_SPIRE0, k), octo(re_, Z_SPIRE0, k + 1), octo(re_, Z_SPIRE1, k + 1), octo(re_, Z_SPIRE1, k)], M['stone_flat'], [(0, 0)] * 4, (octo(1, 0, k) + octo(1, 0, k + 1)))
        mb.oface([octo(rd, Z_SPIRE0, k), octo(rd, Z_SPIRE0, k + 1), octo(re_, Z_SPIRE0, k + 1), octo(re_, Z_SPIRE0, k)], M['stone_flat'], [(0, 0)] * 4, (0, 0, -1))
    mb.obj('spire_eave', SET, hull=0.02)
    mb = MB(); rc = 1.72; sl = math.hypot(rc, Z_APEX - Z_SPIRE1)
    for k in range(8):
        a, b = octo(rc, Z_SPIRE1, k), octo(rc, Z_SPIRE1, k + 1); apex = Vector((0, 0, Z_APEX)); w_ = (a - b).length
        nrm = (b - a).cross(apex - a)
        mb.oface([a, b, apex], M['scales'], [(0, 0), (w_, 0), (w_ / 2, sl)], nrm if nrm.dot(octo(1, 0, k) + octo(1, 0, k + 1)) > 0 else -nrm)
    mb.obj('spire_cone', SET, hull=0.02)
    mb = MB(); mb.frustum((0, 0, Z_APEX - 0.25), (0, 0, Z_APEX + 0.12), 0.24, 0.14, M['stone_flat'], seg=10)
    mb.sphere((0, 0, 27.9), 0.2, M['copper'], seg=14, rings=8); mb.frustum((0, 0, 28.05), (0, 0, FINIAL_TOP[2]), 0.045, 0.0, M['copper'], seg=8)
    mb.obj('finial', SET, hull=0.012)

    # ---- church facade and nave (right of the tower), steps
    cx0, cx1, cyf = 2.45, 11.85, -2.6; eave, apex = 9.6, 13.6; cw = cx1 - cx0; cm = (cx0 + cx1) / 2
    mb = MB(); front = [(cx0, 0), (cx1, 0), (cx1, eave), (cm, apex), (cx0, eave)]
    mb.oface([(x, cyf, z) for x, z in front], M['church'], [((x - cx0) / cw, z / apex) for x, z in front], (0, -1, 0))
    for (xa, za), (xb, zb) in zip(front, front[1:] + front[:1]):
        if za == 0 and zb == 0: continue
        mb.oface([(xa, cyf, za), (xb, cyf, zb), (xb, cyf + 0.45, zb), (xa, cyf + 0.45, za)], M['pl_cream'], [(0, 0), (1, 0), (1, 0.2), (0, 0.2)], Vector((zb - za, 0, -(xb - xa))) * -1)
    mb.obj('church_front', SET, hull=hull(14))
    mb = MB()                                                                              # raking and eave cornices, pilaster bases
    mb.box((cx0 - 0.15, cyf - 0.28, eave - 0.05), (cx1 + 0.15, cyf + 0.1, eave + 0.3), M['stone_flat'])
    for (xa, xb, sgn) in ((cx0 - 0.25, cm, 1), (cm, cx1 + 0.25, -1)):
        za = eave + 0.25 if sgn > 0 else apex + 0.3; zb = apex + 0.3 if sgn > 0 else eave + 0.25
        for (yy0, yy1, dz) in ((cyf - 0.3, cyf + 0.1, 0.0),):
            pts = [(xa, za - 0.4), (xb, zb - 0.4), (xb, zb), (xa, za)]
            mb.oface([(x, yy0, z) for x, z in pts], M['stone_flat'], [(0, 0)] * 4, (0, -1, 0))
            mb.oface([(x, yy0, z) for x, z in pts[2:]] + [(x, yy1, z) for x, z in pts[2:][::-1]], M['stone_flat'], [(0, 0)] * 4, (0, 0, 1))
            mb.oface([(x, yy0, z) for x, z in pts[:2]] + [(x, yy1, z) for x, z in pts[:2][::-1]], M['stone_flat'], [(0, 0)] * 4, (0, 0, -1))
    mb.sphere((cm, cyf - 0.1, apex + 0.55), 0.22, M['stone_flat'], seg=10, rings=6)
    mb.frustum((cm, cyf - 0.1, apex + 0.7), (cm, cyf - 0.1, apex + 1.6), 0.05, 0.05, M['iron'], seg=6); mb.box((cm - 0.3, cyf - 0.13, apex + 1.25), (cm + 0.3, cyf - 0.07, apex + 1.32), M['iron'])
    for k, (sz, dy) in enumerate(((0.18, 1.2), (0.36, 0.85), (0.54, 0.5))):
        mb.box((cm - 2.0 + 0.2 * k, cyf - dy, 0), (cm + 2.0 - 0.2 * k, cyf, sz), M['stone'], tile=(2, 2))
    mb.obj('church_trim', SET, hull=hull(12))
    mb = MB(); nb = 22.0                                                                   # nave body and roof
    mb.box((cx0 + 0.2, cyf + 0.45, 0), (cx1 - 0.2, nb, eave - 0.3), M['brick'], tile=(2.0, 1.92), skip='front,bottom')
    rs = [((cx0, cyf + 0.4, eave - 0.3), (cm, cyf + 0.4, apex - 0.9)), ((cm, cyf + 0.4, apex - 0.9), (cx1, cyf + 0.4, eave - 0.3))]
    for (a, b) in rs:
        a = Vector(a); b = Vector(b); dv = Vector((0, nb - a.y + 0.3, 0)); L_ = (b - a).length
        mb.oface([a, b, b + dv, a + dv], M['roof_b'], [(0, 0), (L_ / 2, 0), (L_ / 2, dv.y / 2), (0, dv.y / 2)], (0, 0, 1))
    mb.oface([(cx0 + 0.2, nb, eave - 0.3), (cx1 - 0.2, nb, eave - 0.3), (cm, nb, apex - 0.9)], M['brick'], [(0, 0), (4.5, 0), (2.25, 2)], (0, 1, 0))
    mb.obj('church_nave', SET, hull=hull(16))
    STATE['church'] = dict(x0=cx0, x1=cx1, y=cyf, eave=eave, apex=apex)

    # ---- houses round the square (front facade textures, plaster sides, canal-tile roofs)
    houses = [('house_a', (-10.4, -1.0), '-y'), ('house_b', (-15.0, -1.0), '-y'), ('house_c', (-14.0, -9.8), '+x'), ('house_d', (-14.0, -16.0), '+x'), ('house_e', (12.25, -1.6), '-y')]
    HD = {h[0]: h for h in TT.HOUSES}; facades = []
    plaster_of = {'house_a': 'pl_terra', 'house_b': 'pl_ochre', 'house_c': 'pl_pink', 'house_d': 'pl_cream', 'house_e': 'pl_red'}
    for (nm, (px, py), facing) in houses:
        _, w_, h_, d_, col, *_r = HD[nm]; mb = MB(); side = TX(plaster_of[nm]); fac = TX(nm)
        if facing == '-y':
            x0, x1, y0, y1 = px, px + w_, py, py + d_; nrm = (0, -1, 0)
            mb.oface([(x0, y0, 0), (x1, y0, 0), (x1, y0, h_), (x0, y0, h_)], fac, [(0, 0), (1, 0), (1, 1), (0, 1)], nrm)
            for (xa, ya, xb, yb, nn) in ((x1, y0, x1, y1, (1, 0, 0)), (x0, y1, x0, y0, (-1, 0, 0)), (x1, y1, x0, y1, (0, 1, 0))):
                L_ = math.hypot(xb - xa, yb - ya); mb.oface([(xa, ya, 0), (xb, yb, 0), (xb, yb, h_), (xa, ya, h_)], side, [(0, 0), (L_ / 2, 0), (L_ / 2, h_ / 2), (0, h_ / 2)], nn)
            ridge = h_ + 2.0; o_ = 0.45
            for (ya, yb, zn) in ((y0 - o_, (y0 + y1) / 2, -1), (y1 + o_, (y0 + y1) / 2, 1)):
                pts = [(x0 - o_, ya, h_ - 0.15), (x1 + o_, ya, h_ - 0.15), (x1 + o_, yb, ridge), (x0 - o_, yb, ridge)]
                Ls = math.hypot(yb - ya, ridge - h_); mb.oface(pts, TX('roof'), [(0, 0), ((w_ + 2 * o_) / 2, 0), ((w_ + 2 * o_) / 2, Ls / 2), (0, Ls / 2)], (0, zn * 0.0 + (0.0), 1))
            for xx, nn in ((x0, (-1, 0, 0)), (x1, (1, 0, 0))):
                mb.oface([(xx, y0, h_), (xx, y1, h_), (xx, (y0 + y1) / 2, ridge - 0.1)], side, [(0, 0), (d_ / 2, 0), (d_ / 4, 1)], nn)
            facades.append((nm, (x0, y0 - 0.01), (1, 0, 0), (0, -1, 0), h_))
            mb.box((x0 - o_, y0 - o_ - 0.05, h_ - 0.35), (x1 + o_, y0 - o_ + 0.2, h_ - 0.12), M['wood_out'])               # eave board / gutter
        else:
            y0, y1, x1, x0 = py, py + w_, px, px - d_; nrm = (1, 0, 0)
            mb.oface([(x1, y1, 0), (x1, y0, 0), (x1, y0, h_), (x1, y1, h_)], fac, [(0, 0), (1, 0), (1, 1), (0, 1)], nrm)
            for (xa, ya, xb, yb, nn) in ((x1, y0, x0, y0, (0, -1, 0)), (x0, y1, x1, y1, (0, 1, 0)), (x0, y0, x0, y1, (-1, 0, 0))):
                L_ = math.hypot(xb - xa, yb - ya); mb.oface([(xa, ya, 0), (xb, yb, 0), (xb, yb, h_), (xa, ya, h_)], side, [(0, 0), (L_ / 2, 0), (L_ / 2, h_ / 2), (0, h_ / 2)], nn)
            ridge = h_ + 2.0; o_ = 0.45
            for (xa, xb) in ((x1 + o_, (x0 + x1) / 2), (x0 - o_, (x0 + x1) / 2)):
                pts = [(xa, y0 - o_, h_ - 0.15), (xa, y1 + o_, h_ - 0.15), (xb, y1 + o_, ridge), (xb, y0 - o_, ridge)]
                Ls = math.hypot(xb - xa, ridge - h_); mb.oface(pts, TX('roof'), [(0, 0), ((w_ + 2 * o_) / 2, 0), ((w_ + 2 * o_) / 2, Ls / 2), (0, Ls / 2)], (0, 0, 1))
            for yy, nn in ((y0, (0, -1, 0)), (y1, (0, 1, 0))):
                mb.oface([(x0, yy, h_), (x1, yy, h_), ((x0 + x1) / 2, yy, ridge - 0.1)], side, [(0, 0), (d_ / 2, 0), (d_ / 4, 1)], nn)
            facades.append((nm, (x1 + 0.01, y1), (0, -1, 0), (1, 0, 0), h_))
            mb.box((x1 + o_ - 0.2, y0 - o_, h_ - 0.35), (x1 + o_ + 0.05, y1 + o_, h_ - 0.12), M['wood_out'])
        mb.obj(nm, SET, hull=hull(14))
    STATE['facades'] = facades

    # ---- square dressing: fountain, bench, barrels, flower pots, wall lanterns, a cart
    mb = MB(); fx, fy = 7.2, -17.5
    mb.frustum((fx, fy, 0), (fx, fy, 0.75), 1.6, 1.6, M['stone'], seg=20, uv_wrap=(5, 0.4)); mb.frustum((fx, fy, 0.75), (fx, fy, 0.85), 1.7, 1.7, M['stone_flat'], seg=20)
    mb.frustum((fx, fy, 0.85), (fx, fy, 2.2), 0.25, 0.18, M['stone_flat'], seg=10); mb.frustum((fx, fy, 2.2), (fx, fy, 2.4), 0.7, 0.55, M['stone_flat'], seg=14)
    mb.sphere((fx, fy, 2.6), 0.22, M['copper'], seg=10, rings=6)
    mb.obj('fountain', SET, hull=hull(12))
    mb = MB(); mb.frustum((fx, fy, 0.8), (fx, fy, 0.81), 1.5, 1.5, C('#3a6ab8', 0.5, 1.6), seg=20); mb.obj('fountain_water', SET)
    mb = MB()
    for (bx, by) in ((3.2, -3.4), (4.0, -3.5), (-4.6, -1.6)):
        mb.frustum((bx, by, 0), (bx, by, 0.9), 0.36, 0.36, C('#7a4428'), seg=12); mb.frustum((bx, by, 0.25), (bx, by, 0.3), 0.38, 0.38, M['iron'], seg=12); mb.frustum((bx, by, 0.65), (bx, by, 0.7), 0.38, 0.38, M['iron'], seg=12)
    for (px_, py_) in ((-9.6, -1.4), (-5.6, -1.4), (-13.6, -8.0), (-13.6, -14.4), (12.7, -2.0)):
        mb.frustum((px_, py_, 0), (px_, py_, 0.5), 0.2, 0.28, C('#b8572f'), seg=10)
        for k in range(5): mb.sphere((px_ + 0.15 * math.cos(k * 1.3), py_ + 0.15 * math.sin(k * 1.3), 0.62 + 0.06 * (k % 2)), 0.12, C('#d8303a' if k % 2 else '#3f7a3a'), seg=8, rings=4)
    mb.box((-12.6, -7.0, 0.55), (-11.4, -3.0, 0.68), C('#7a4428')); [mb.box((-12.5, y, 0), (-12.4, y + 0.1, 0.55), C('#5a2e1a')) for y in (-6.8, -3.3)]
    mb.box((-11.5, -6.8, 0), (-11.4, -6.7, 0.55), C('#5a2e1a')); mb.box((-11.5, -3.3, 0), (-11.4, -3.2, 0.55), C('#5a2e1a'))
    mb.obj('square_props', SET, hull=hull(10))
    mb = MB(); sx_, sy_ = -12.2, -12.8                                                    # market stall with a striped awning, produce crates
    for (dx, dy) in ((0, -1.3), (0, 1.3), (1.4, -1.3), (1.4, 1.3)): mb.box((sx_ + dx - 0.06, sy_ + dy - 0.06, 0), (sx_ + dx + 0.06, sy_ + dy + 0.06, 2.9 if dx == 0 else 2.4), C('#6e3a22'))
    mb.box((sx_ - 0.1, sy_ - 1.4, 1.0), (sx_ + 1.5, sy_ + 1.4, 1.1), C('#8a5232'))
    for k in range(6):
        y0 = sy_ - 1.5 + k * 0.5; mb.oface([(sx_ - 0.2, y0, 3.0), (sx_ - 0.2, y0 + 0.5, 3.0), (sx_ + 1.9, y0 + 0.5, 2.3), (sx_ + 1.9, y0, 2.3)], C('#d83a32' if k % 2 else '#f2e6c8', 0.8), [(0, 0)] * 4, (0.3, 0, 1))
    for (cx_, cy2, col) in ((sx_ + 0.4, sy_ - 0.8, '#f08a20'), (sx_ + 0.4, sy_ + 0.0, '#d8302a'), (sx_ + 0.4, sy_ + 0.8, '#8ab030'), (sx_ + 1.05, sy_ - 0.4, '#f0c030'), (sx_ + 1.05, sy_ + 0.5, '#f08a20')):
        mb.box((cx_ - 0.28, cy2 - 0.32, 1.1), (cx_ + 0.28, cy2 + 0.32, 1.32), C('#a8783e'))
        for i in range(3):
            for j in range(3): mb.sphere((cx_ - 0.17 + 0.17 * i, cy2 - 0.2 + 0.2 * j, 1.38), 0.085, C(col), seg=7, rings=4)
    cx2, cy3 = 13.2, -7.5                                                                   # hand cart with two wheels, leaning
    mb.box((cx2 - 0.7, cy3 - 1.2, 0.75), (cx2 + 0.7, cy3 + 1.2, 0.85), C('#8a5232')); mb.box((cx2 - 0.7, cy3 - 1.2, 0.85), (cx2 - 0.62, cy3 + 1.2, 1.3), C('#8a5232')); mb.box((cx2 + 0.62, cy3 - 1.2, 0.85), (cx2 + 0.7, cy3 + 1.2, 1.3), C('#8a5232'))
    for sx2 in (-0.8, 0.8): mb.frustum((cx2 + sx2 - 0.06, cy3 + 0.2, 0.7), (cx2 + sx2 + 0.06, cy3 + 0.2, 0.7), 0.7, 0.7, C('#6e3a22'), seg=16)
    for sx2 in (-0.5, 0.5): mb.frustum((cx2 + sx2, cy3 - 1.2, 0.8), (cx2 + sx2 * 0.6, cy3 - 2.8, 0.05), 0.05, 0.05, C('#6e3a22'), seg=6)
    mb.obj('market', SET, hull=hull(11))
    mb = MB(); wl = [(-5.3, -1.0 - 0.45, 4.0), (-13.55, -12.9, 4.0), (2.3, -2.7, 4.2)]
    for (lx_, ly_, lz_) in wl:
        mb.box((lx_ - 0.12, ly_ - 0.12, lz_ - 0.25), (lx_ + 0.12, ly_ + 0.12, lz_ - 0.2), M['iron']); mb.box((lx_ - 0.1, ly_ - 0.1, lz_ + 0.2), (lx_ + 0.1, ly_ + 0.1, lz_ + 0.25), M['iron'])
        mb.frustum((lx_, ly_, lz_ + 0.25), (lx_, ly_, lz_ + 0.4), 0.09, 0.0, M['iron'], seg=6)
    mb.obj('wall_lanterns', SET, hull=0.01)
    mb = MB()
    for (lx_, ly_, lz_) in wl: mb.box((lx_ - 0.09, ly_ - 0.09, lz_ - 0.2), (lx_ + 0.09, ly_ + 0.09, lz_ + 0.2), E('wlamp', image='lantern', k=P['lamp_k'] if P['lamp_k'] > 0 else 0.4))
    o_ = mb.obj('wall_lantern_glass', SET); o_.visible_shadow = False

    # ---- mid town: simplified houses in a ring (parallax between the square and the painted plate), cypresses
    _midtown(SET, M, C, TX, night)
    # ---- painted plate ring + sky dome
    mb = MB(); R = 72.0; seg = 96; z0_, z1_ = -2.0, 53.0
    for i in range(seg):
        a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; u0, u1 = 2.0 * i / seg, 2.0 * (i + 1) / seg
        mb.face([Vector((R * math.cos(a0), R * math.sin(a0), z0_)), Vector((R * math.cos(a1), R * math.sin(a1), z0_)), Vector((R * math.cos(a1), R * math.sin(a1), z1_)), Vector((R * math.cos(a0), R * math.sin(a0), z1_))],
                E('pano', image='pano_' + P['pano'], k=P['pano_k'], alpha=True), [(u0, 0), (u1, 0), (u1, 1), (u0, 1)])
    pr = mb.obj('plate', SET); pr.visible_shadow = False
    mb = MB(); R = 110.0; seg = 72; els = [-15 + 105 * k / 14 for k in range(15)]
    for i in range(seg):
        for k in range(14):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; e0, e1 = math.radians(els[k]), math.radians(els[k + 1])
            pts = [Vector((R * math.cos(e) * math.cos(a), R * math.cos(e) * math.sin(a), R * math.sin(e) + 10)) for (a, e) in ((a0, e0), (a1, e0), (a1, e1), (a0, e1))]
            uvs = [(i / seg, k / 14), ((i + 1) / seg, k / 14), ((i + 1) / seg, (k + 1) / 14), (i / seg, (k + 1) / 14)]
            mb.face(pts[::-1], E('sky', image='sky_' + P['sky'], k=P['sky_k']), uvs[::-1])
    sk = mb.obj('sky', SET); sk.visible_shadow = False

    # ---- night: lit windows (warm emission quads on the house and church windows), glowing rose window
    if P['win_k'] > 0: _night_windows(SET, P, tx)

    # ---- the rod, the wire, the lightning bolts
    _build_rod_wire(SET, M, C)
    _build_bolts(SET, P)

    # ---- lights: one hard key (sun / moon), and the lightning flash (same direction, off)
    kd = Vector(P['key_dir']).normalized(); k = max(P['key'])
    d = bpy.data.lights.new('key_sun', 'SUN'); d.color = tuple(x / k for x in P['key']); d.energy = math.pi * k; d.angle = math.radians(P['sun_angle'])
    sun = bpy.data.objects.new('key_sun', d); LIGHTS.objects.link(sun); sun.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler(); sun.location = (-20, -30, 40); STATE['sun'] = sun
    fd = bpy.data.lights.new('flash_sun', 'SUN'); fd.color = (0.78, 0.84, 1.0); fd.energy = 0.0; fd.angle = math.radians(1.0)
    fl = bpy.data.objects.new('flash_sun', fd); LIGHTS.objects.link(fl); fl.rotation_euler = sun.rotation_euler.copy(); fl.location = (-20, -30, 42); STATE['flash'] = fl
    setup_grade(scene)
    for ob in SET.objects: no_bounce(ob)
    STATE['rod'] = 0; set_rod(0); set_bell(0.0); set_bolt(False); flash(0.0)
    A = anchors(); STATE['A'] = A
    return A

def _midtown(SET, M, C, TX, night):
    r = random.Random(77); mb = MB(); rb = MB(); cy = MB(); placed = []
    walls = ['terra', 'ochre', 'pink', 'cream', 'red']
    WM = {w: TX('tw_' + w + ('_n' if night else ''), 1.0, glow=('tw_' + w + '_n_glow') if night else None, glow_k=STATE['P']['win_k'] * 0.9) for w in walls}
    cams = [(0.6, -15.5), (-13, -34), (-7.8, -6.8)]
    tries = 0
    while len(placed) < 70 and tries < 3000:
        tries += 1
        ang = r.uniform(0, 2 * math.pi); rad = r.uniform(19, 58); x, y = rad * math.cos(ang), rad * math.sin(ang)
        if -24 < x < 24 and -40 < y < 3: continue                       # the square and the camera side
        if 1.5 < x < 14 and -4 < y < 24: continue                       # church
        if -21 < x < -2 and -20 < y < 7: continue                        # houses round the square
        if y < -20 and -50 < x < 30: continue                            # keep the south open (key light, establishing camera)
        w_, d_ = r.uniform(3.5, 6.5), r.uniform(3.5, 6.0); h_ = r.uniform(6.0, 11.0) * (0.85 if rad > 40 else 1.0)
        if any(abs(x - px) < (w_ + pw) / 2 + 0.6 and abs(y - py) < (d_ + pd) / 2 + 0.6 for (px, py, pw, pd) in placed): continue
        placed.append((x, y, w_, d_))
        wm = WM[r.choice(walls)]; x0, x1, y0, y1 = x - w_ / 2, x + w_ / 2, y - d_ / 2, y + d_ / 2
        for (xa, ya, xb, yb, nn) in ((x0, y0, x1, y0, (0, -1, 0)), (x1, y0, x1, y1, (1, 0, 0)), (x1, y1, x0, y1, (0, 1, 0)), (x0, y1, x0, y0, (-1, 0, 0))):
            L_ = math.hypot(xb - xa, yb - ya); mb.oface([(xa, ya, 0), (xb, yb, 0), (xb, yb, h_), (xa, ya, h_)], wm, [(0, 0), (L_ / 2.4, 0), (L_ / 2.4, h_ / 3.0), (0, h_ / 3.0)], nn)
        o_ = 0.35; rz = h_ + min(w_, d_) * 0.32; rm = M['roof'] if r.random() < 0.6 else M['roof_b']
        if r.random() < 0.5:                                              # hip roof
            c_ = [(x0 - o_, y0 - o_), (x1 + o_, y0 - o_), (x1 + o_, y1 + o_), (x0 - o_, y1 + o_)]
            if w_ > d_: top = [(x0 + d_ / 2, y), (x1 - d_ / 2, y)]
            else: top = [(x, y0 + w_ / 2), (x, y1 - w_ / 2)]
            cen = Vector((x, y, h_))
            for i in range(4):
                a, b = Vector((*c_[i], h_ - 0.1)), Vector((*c_[(i + 1) % 4], h_ - 0.1))
                ta = min(top, key=lambda p: (p[0] - a.x) ** 2 + (p[1] - a.y) ** 2); tb = min(top, key=lambda p: (p[0] - b.x) ** 2 + (p[1] - b.y) ** 2)
                pts = [a, b, Vector((*tb, rz)), Vector((*ta, rz))] if ta != tb else [a, b, Vector((*ta, rz))]
                mid = (a + b) / 2; nrm = (mid - cen); nrm.z = 1.2
                rb.oface(pts, rm, [(p.x / 2 + p.y / 2, p.z / 2) for p in pts], nrm)
        else:
            alongx = w_ > d_
            if alongx:
                for (ya, nz) in ((y0 - o_, -1), (y1 + o_, 1)):
                    rb.oface([(x0 - o_, ya, h_ - 0.1), (x1 + o_, ya, h_ - 0.1), (x1 + o_, y, rz), (x0 - o_, y, rz)], rm, [(0, 0), ((w_ + 2 * o_) / 2, 0), ((w_ + 2 * o_) / 2, 1.5), (0, 1.5)], (0, nz, 1.5))
                for xx, nn in ((x0, (-1, 0, 0)), (x1, (1, 0, 0))): mb.oface([(xx, y0, h_), (xx, y1, h_), (xx, y, rz - 0.05)], wm, [(0, 0), (d_ / 2.4, 0), (d_ / 4.8, 0.6)], nn)
            else:
                for (xa, nz) in ((x0 - o_, -1), (x1 + o_, 1)):
                    rb.oface([(xa, y0 - o_, h_ - 0.1), (xa, y1 + o_, h_ - 0.1), (x, y1 + o_, rz), (x, y0 - o_, rz)], rm, [(0, 0), ((d_ + 2 * o_) / 2, 0), ((d_ + 2 * o_) / 2, 1.5), (0, 1.5)], (nz, 0, 1.5))
                for yy, nn in ((y0, (0, -1, 0)), (y1, (0, 1, 0))): mb.oface([(x0, yy, h_), (x1, yy, h_), (x, yy, rz - 0.05)], wm, [(0, 0), (w_ / 2.4, 0), (w_ / 4.8, 0.6)], nn)
    # two more campaniles and a dome in the mid ring
    for (tx_, ty_, th) in ((-26, 22, 22.0), (31, 30, 18.0)):
        mb.box((tx_ - 1.6, ty_ - 1.6, 0), (tx_ + 1.6, ty_ + 1.6, th), M['brick'], tile=(2.0, 1.92))
        rb.box((tx_ - 1.85, ty_ - 1.85, th), (tx_ + 1.85, ty_ + 1.85, th + 0.4), M['stone_flat'])
        for k in range(4):
            a, b = [(tx_ - 1.85, ty_ - 1.85), (tx_ + 1.85, ty_ - 1.85), (tx_ + 1.85, ty_ + 1.85), (tx_ - 1.85, ty_ + 1.85)][k], [(tx_ + 1.85, ty_ - 1.85), (tx_ + 1.85, ty_ + 1.85), (tx_ - 1.85, ty_ + 1.85), (tx_ - 1.85, ty_ - 1.85)][k]
            pts = [Vector((*a, th + 0.4)), Vector((*b, th + 0.4)), Vector((tx_, ty_, th + 4.5))]
            rb.oface(pts, M['roof'], [(0, 0), (1.8, 0), (0.9, 2)], (((a[0] + b[0]) / 2 - tx_), ((a[1] + b[1]) / 2 - ty_), 1.0))
        for n in FACES:
            n = Vector(n); c = Vector((tx_, ty_, th - 2.0)) + n * 1.61
            t = Vector((0, 0, 1)).cross(n); mb.quad(c - t * 0.5 - Vector((0, 0, 1.0)), t * 1.0, Vector((0, 0, 2.0)), M['dark'])
    dx_, dy_ = 24.0, 44.0
    mb.frustum((dx_, dy_, 0), (dx_, dy_, 9.0), 5.0, 5.0, TX('pl_cream'), seg=16, uv_wrap=(8, 4))
    for k in range(6):
        e0, e1 = math.pi / 2 * k / 6, math.pi / 2 * (k + 1) / 6
        rb.frustum((dx_, dy_, 9.0 + 5.2 * math.sin(e0)), (dx_, dy_, 9.0 + 5.2 * math.sin(e1)), 5.2 * math.cos(e0), max(0.01, 5.2 * math.cos(e1)), M['roof_b'], seg=16, cap0=False, cap1=False, uv_wrap=(8, 1))
    mb.obj('midtown_walls', SET, hull=0.06); rb.obj('midtown_roofs', SET, hull=0.06)
    for i in range(26):                                                    # cypresses
        ang = r.uniform(0, 2 * math.pi); rad = r.uniform(16, 50); x, y = rad * math.cos(ang), rad * math.sin(ang)
        if -24 < x < 24 and -40 < y < 3: continue
        if any(abs(x - px) < pw / 2 + 0.8 and abs(y - py) < pd / 2 + 0.8 for (px, py, pw, pd) in placed): continue
        h_ = r.uniform(6, 10); cy.frustum((x, y, 0), (x, y, h_ * 0.35), 0.5, 0.95, C('#2f5a36', 1.0, 1.1), seg=8, cap0=False); cy.frustum((x, y, h_ * 0.35), (x, y, h_), 0.95, 0.0, C('#2f5a36', 1.0, 1.1), seg=8)
    cy.obj('cypresses', SET, hull=0.05)
    STATE['midtown'] = placed

def _night_windows(SET, P, tx):
    """Warm lit windows on the five houses and the church (about half lit, deterministic) and the rose window."""
    r = random.Random(91); mb = MB(); wm = mat_emit('TWR_win_' + STATE['preset'], '#ffc46a', strength=P['win_k']); rose = MB()
    for (nm, origin, uax, nrm, h_) in STATE['facades']:
        ox, oy = origin; u = Vector(uax); nv = Vector(nrm)
        for (x, y, w, h) in TT.WINDOWS.get(nm, []):
            if r.random() > 0.55: continue
            z1 = h_ - y; z0 = h_ - y - h; p0 = Vector((ox, oy, z0)) + u * x + nv * 0.012
            mb.quad(p0, u * w, Vector((0, 0, h)), wm)
    ch = STATE['church']; W, H = 9.4, 13.6
    for (x, y, w, h) in TT.WINDOWS['church_facade']:
        mb.quad((ch['x0'] + x, ch['y'] - 0.012, H - y - h), (w, 0, 0), (0, 0, h), wm)
    (x, y, w, h), = TT.WINDOWS['church_rose']; cx, cz = ch['x0'] + x + w / 2, H - y - h / 2; R = w / 2
    rm = mat_emit('TWR_rose_' + STATE['preset'], image=tx['church_facade'], strength=P['win_k'] * 1.1); seg = 24
    for i in range(seg):
        a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg
        pts = [(cx, ch['y'] - 0.014, cz), (cx + R * math.cos(a0), ch['y'] - 0.014, cz + R * math.sin(a0)), (cx + R * math.cos(a1), ch['y'] - 0.014, cz + R * math.sin(a1))]
        uvs = [((p[0] - ch['x0']) / W, p[2] / H) for p in pts]
        rose.oface(pts, rm, uvs, (0, -1, 0))
    o1 = mb.obj('night_windows', SET); o1.visible_shadow = False; o2 = rose.obj('rose_glow', SET); o2.visible_shadow = False

def _wire_points():
    """Polyline of the lightning wire from the rod base down the spire, over the parapet and the cornice, down the west (-x)
    face of the tower near its front corner, into the ground."""
    def cone_r(z): return 1.72 * math.cos(math.radians(22.5)) * (Z_APEX - z) / (Z_APEX - Z_SPIRE1)
    y = -0.22; s = 0.06
    pts = [ROD_BASE, (0.0, y, 27.8), (-0.1, y, Z_APEX - 0.25)]
    for z in (27.2, 26.0, 24.8, Z_SPIRE1 + 0.05): pts.append((-(cone_r(z) + s), y, z))
    pts += [(-(1.78 * 0.924 + 0.07), y, Z_SPIRE1 + 0.05), (-(1.78 * 0.924 + 0.07), y, Z_SPIRE0 - 0.05), (-(1.5 * 0.924 + 0.05), y, Z_SPIRE0 - 0.1),
            (-(1.5 * 0.924 + 0.05), y, Z_TERR + 0.04), (-(TW - 0.05), WIRE_Y, Z_TERR + 0.04), (-(TW + 0.1), WIRE_Y, Z_TERR + 0.86),
            (-(TW + 0.32), WIRE_Y, Z_TERR + 0.86), (-(TW + 0.38), WIRE_Y, Z_TERR + 0.1), (-(TW + 0.38), WIRE_Y, Z_CORN - 0.2), (WIRE_X, WIRE_Y, Z_CORN - 0.6),
            (WIRE_X, WIRE_Y, 0.05), (WIRE_X - 0.25, WIRE_Y, 0.02)]
    return pts

def _curve_obj(name, pts, radius, mat, coll, radii=None):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'
    sp = cu.splines.new('POLY'); sp.points.add(len(pts) - 1)
    for i, (p, q) in enumerate(zip(sp.points, pts)):
        p.co = (q[0], q[1], q[2], 1.0)
        if radii: p.radius = radii[i]
    cu.bevel_mode = 'ROUND'; cu.bevel_depth = radius; cu.bevel_resolution = 1; cu.use_fill_caps = True
    cu.materials.append(mat)
    ob = bpy.data.objects.new(name, cu); coll.objects.link(ob); STATE.setdefault('objects', {})[name] = ob
    return ob

def _build_rod_wire(SET, M, C):
    mb = MB(); bx, by, bz = ROD_BASE; tz = ROD_TIP[2]
    mb.frustum((bx, by, bz), (bx, by, tz - 0.16), 0.035, 0.035, M['iron'], seg=8); mb.frustum((bx, by, tz - 0.16), (bx, by, tz), 0.05, 0.0, M['iron'], seg=8, cap0=True)
    for z in (28.1, 28.3): mb.box((-0.08, -0.07, z - 0.03), (bx + 0.08, 0.07, z + 0.03), C('#5a5060'))      # nailed iron straps round spike and rod
    mb.box((bx - 0.05, -0.05, 27.92), (bx + 0.05, 0.05, 28.0), C('#5a5060'))
    rod = mb.obj('rod', SET, hull=0.008)
    wm = C('#3a3446', 1.0, 1.3); wp = _wire_points()
    wire = _curve_obj('wire', wp, 0.028, wm, SET)
    mb = MB()                                                                              # brackets holding the wire off the wall, ground plate
    for z in [Z_CORN - 1.6 - 2.4 * k for k in range(9)]:
        if z < 0.8: break
        mb.box((-TW - 0.01, WIRE_Y - 0.03, z - 0.03), (WIRE_X + 0.03, WIRE_Y + 0.03, z + 0.03), C('#3a3446', 1.0, 1.3))
    mb.box((WIRE_X - 0.5, WIRE_Y - 0.25, 0.0), (WIRE_X - 0.1, WIRE_Y + 0.25, 0.03), C('#5a5060'))
    br = mb.obj('wire_brackets', SET, hull=0.006)
    STATE['rod_objs'] = [rod]; STATE['wire_objs'] = [wire, br]; STATE['wire_pts'] = wp

def _bolt_path(start, end, seed, n=14, jag=1.2):
    """Jagged polyline: zig-zag offsets that shrink toward the end, so the strike point is exact and the last stretch stays jagged
    at close range (points are denser near the end)."""
    r = random.Random(seed); s, e = Vector(start), Vector(end); pts = [tuple(s)]; L = (e - s).length
    side = (e - s).cross(Vector((0.3, 1, 0))).normalized(); side2 = (e - s).cross(side).normalized()
    for i in range(1, n):
        t = 1 - (1 - i / n) ** 1.6; p = s.lerp(e, t); k = (1 - t) ** 0.7
        p += side * r.uniform(-jag, jag) * (0.15 + k) + side2 * r.uniform(-jag, jag) * 0.5 * (0.15 + k)
        pts.append(tuple(p))
    pts.append(tuple(e)); return pts

def _build_bolts(SET, P):
    """Three emissive bolts (camera rays only, strength 9: they bloom): to the rod tip, to the finial top, a forked sky bolt
    over the hills to the north (in frame for town_wide and through the north arch in chamber_eye)."""
    bm = mat_emit('TWR_bolt', '#f2f2ff', strength=9.0, camera_only=True); gm = mat_emit('TWR_bolt_glow', '#8c9cff', strength=0.45, camera_only=True, additive=True)
    start = (5.0, 12.0, 78.0); objs = {}
    for nm, end in (('bolt_tower_rod', ROD_TIP), ('bolt_tower_top', FINIAL_TOP)):
        pts = _bolt_path(start, end, 5, n=34, jag=2.4); N_ = len(pts) - 1; rad = [1.0 - 0.8 * (i / N_) ** 0.5 for i in range(N_ + 1)]
        a = _curve_obj(nm, pts, 0.14, bm, SET, rad); br = _bolt_path(pts[8], (pts[8][0] + 9, pts[8][1] + 4, pts[8][2] - 16), 8, n=10, jag=1.4)
        b = _curve_obj(nm + '_branch', br, 0.07, bm, SET, [1.0 - 0.8 * i / (len(br) - 1) for i in range(len(br))])
        g = _curve_obj(nm + '_glow', pts, 0.32, gm, SET, rad)
        mb = MB(); mb.sphere(end, 0.09, bm, seg=10, rings=6); sp = mb.obj(nm + '_spot', SET)
        objs[nm] = [a, b, g, sp]
    pts = _bolt_path((18, 64, 82), (9, 68, 6), 12, n=24, jag=3.2); rad = [1.0 - 0.5 * i / (len(pts) - 1) for i in range(len(pts))]
    a = _curve_obj('bolt_sky', pts, 0.3, bm, SET, rad); g = _curve_obj('bolt_sky_glow', pts, 1.0, gm, SET, rad)
    br = _bolt_path(pts[7], (pts[7][0] + 14, pts[7][1] + 2, pts[7][2] - 24), 14, n=12, jag=2.4); b = _curve_obj('bolt_sky_branch', br, 0.16, bm, SET, [1.0 - 0.8 * i / (len(br) - 1) for i in range(len(br))])
    objs['bolt_sky'] = [a, g, b]
    for lst in objs.values():
        for o in lst: o.visible_shadow = False
    STATE['bolts'] = objs

# ----------------------------------------------------------------------------- animated controls
def _fcurves(idblock):
    ad = idblock.animation_data; out = []
    if not ad or not ad.action: return out
    for layer in ad.action.layers:
        for strip in layer.strips:
            cb = strip.channelbag(ad.action_slot)
            if cb: out += list(cb.fcurves)
    return out

def _key(idblock, path, frame, interp='CONSTANT'):
    idblock.keyframe_insert(path, frame=frame)
    for fc in _fcurves(idblock):
        if fc.data_path == path or fc.data_path.endswith(path):
            for kp in fc.keyframe_points:
                if int(round(kp.co.x)) == int(frame): kp.interpolation = interp

def _show(objs, visible, frame=None):
    for o in objs:
        o.hide_render = not visible; o.hide_viewport = False
        if frame is not None: _key(o, 'hide_render', frame)

def set_rod(state, frame=None):
    """0: no rod. 1: the iron rod nailed to the finial (rod_base .. rod_tip). 2 (or more): rod + the thin wire running from
    rod_base down the spire, over the parapet and the cornice, down the west face of the tower into the ground.
    With frame=N the visibility is keyed (constant) at frame N."""
    s = int(state); STATE['rod'] = s
    _show(STATE['rod_objs'], s >= 1, frame); _show(STATE['wire_objs'], s >= 2, frame)

def set_bell(angle_deg, frame=None, interp='BEZIER'):
    """Swing of the bell, headstock, clapper and the bell rope about the axle (x axis), degrees; positive swings the mouth toward +y
    (away from the front). With frame=N the rotation is keyframed (Bezier by default: a smooth swing between keys)."""
    piv = STATE['objects']['bell_pivot']; piv.rotation_euler = (math.radians(angle_deg), 0.0, 0.0)
    if frame is not None: _key(piv, 'rotation_euler', frame, interp)

def flash(strength, frame=None):
    """Lightning flash: the flash light (a second sun along the key, cold white) at strength x flash_e, and the sky and the
    painted plate brightened by (1 + 1.6 x strength). strength 0 = off. With frame=N everything is keyed (constant) at N,
    so flash(1, 40); flash(0.3, 41); flash(1, 42); flash(0, 44) gives a flicker."""
    P = STATE['P']; s = max(0.0, float(strength)); fl = STATE['flash']; fl.data.energy = math.pi * P.get('flash_e', 3.0) * s
    if frame is not None: _key(fl.data, 'energy', frame)
    for nm, base in (('sky', P['sky_k']), ('pano', P['pano_k'])):
        m = bpy.data.materials.get('TWR_' + STATE['preset'] + '_e_' + nm)
        if m is None: continue
        sock = m.node_tree.nodes['strength'].inputs['Strength']; sock.default_value = base * (1.0 + 1.6 * s)
        if frame is not None:
            sock.keyframe_insert('default_value', frame=frame)
            ad = m.node_tree.animation_data
            for fc in _fcurves(m.node_tree):
                for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT'
    STATE['flash_s'] = s

def set_bolt(visible, frame=None, target='tower'):
    """Show or hide a jagged bright lightning bolt. target 'tower': from the clouds to the rod tip if the rod is up (set_rod >= 1)
    at the time of the call, else to the top of the finial; 'sky': a forked bolt in the sky over the hills to the north-west.
    Hiding (visible=False) hides all of them. With frame=N visibility is keyed (constant) at N."""
    B = STATE['bolts']
    want = set()
    if visible:
        if target == 'tower': want.add('bolt_tower_rod' if STATE.get('rod', 0) >= 1 else 'bolt_tower_top')
        else: want.add('bolt_sky')
    for nm, objs in B.items():
        _show(objs, nm in want, frame)

# ----------------------------------------------------------------------------- anchors and cameras
CAMS = dict(
    square_low=dict(loc=(0.6, -15.6, 1.2), look_at=(0.1, -2.0, 8.0), lens=22),
    chamber_eye=dict(loc=(0.35, -4.1, Z_CH + 2.4), look_at=(-0.05, 1.9, Z_CH + 2.75), lens=22),
    chamber_high_down=dict(loc=(-4.3, -0.6, Z_TERR + 2.2), look_at=(-1.2, -10.2, 0.0), lens=22),
    spire_insert=dict(loc=(-2.45, -2.25, 27.8), look_at=(0.05, 0.0, 28.55), lens=22),
    town_wide=dict(loc=(-13.0, -34.0, 9.0), look_at=(0.5, 0.0, 13.6), lens=22),
    tower_side_mid=dict(loc=(-7.8, -6.9, 9.6), look_at=(-2.3, -0.9, 12.6), lens=22),
)
CAM_NOTES = dict(
    square_low='from the square, 1.2 D high, pitched up: actors at square_marks in the lower half, the tower and spire rising behind them',
    chamber_eye='bell chamber at eye level, from just outside the south arch (the opening fills the frame): priest_mark near, hero_mark far, the bell overhead, the town through the north arch',
    chamber_high_down='from the parapet at the west side, looking down the west face (wire visible) to the square marks 24 D below',
    spire_insert='close on the finial, rod and rod tip against the sky (rod 1.5 D tall, about 330 px)',
    town_wide='establishing: square, church facade, houses, the tower full height, mid town and the painted plate',
    tower_side_mid='the west face of the tower at mid height with the wire running down it, the bell chamber above',
)

def anchors():
    P = STATE['P']; kd = Vector(P['key_dir']).normalized()
    return dict(
        chamber_floor=dict(z=Z_CH, rect=dict(x0=-(TW - WALL_T), x1=TW - WALL_T, y0=-(TW - WALL_T), y1=TW - WALL_T), hero_mark=CH_MARKS['hero_mark'], priest_mark=CH_MARKS['priest_mark'],
                           extra_marks=list(CH_MARKS['extra_marks']), note='actors stand on z = 15.0; keep them inside the rect minus 0.3 D; the bell rim is 3.35 D above the floor'),
        square_marks=dict(SQ_MARKS),
        rod_base=ROD_BASE, rod_tip=ROD_TIP, finial_top=FINIAL_TOP, rod_length=round(ROD_TIP[2] - ROD_BASE[2], 3),
        wire_points=[tuple(p) for p in STATE['wire_pts']], wire_ground=tuple(STATE['wire_pts'][-1]),
        bell=dict(pivot=(0.0, 0.0, Z_AXLE), axis='x', diameter=BELL_D, rim_z=Z_CH + 3.35, crown_z=Z_CH + 3.35 + 2.04, rope=(STATE['rope'][0], STATE['rope'][1]),
                  sally_z=(Z_CH + 1.55, Z_CH + 2.15), rope_b=(-1.3, 1.12)),
        tower=dict(half_width=TW, shaft_top=Z_CH, chamber_floor=Z_CH, cornice=(Z_CORN, Z_TERR), terrace=Z_TERR, arch=dict(half_width=OW, sill=Z_SILL, spring=Z_SPRING, top=Z_SPRING + OW),
                   spire=(Z_TERR, Z_APEX), clock=(0.0, -TW - 0.012, 12.3), lantern=STATE['lantern']),
        church=dict(STATE['church']), houses=[f[0] for f in STATE['facades']],
        bolt_ends=dict(tower_rod=ROD_TIP, tower_top=FINIAL_TOP), key_dir=tuple(kd), preset=STATE['preset'],
        key_note='DAY: sun 49 deg high from the front-left (south-south-west): for cameras in the square looking at the tower (+y) the key is behind the camera at screen-left, shadows fall to screen-right and away',
        cams={k: dict(v) for k, v in CAMS.items()}, cam_notes=dict(CAM_NOTES),
        render=dict(samples_final=12, resolution=(720, 1280), threads=2, sun_angle_deg=P['sun_angle'], key=P['key'], shade=P['shade'], lift=P['lift'], toon=P['toon']))

def make_camera(setup, name='cam', scene=None):
    """Create (or reuse) a 22 mm camera from a {loc, look_at, lens[, up, roll]} setup and make it the scene camera."""
    scene = scene or bpy.context.scene
    ob = bpy.data.objects.get(name)
    if ob is None:
        cd = bpy.data.cameras.new(name); ob = bpy.data.objects.new(name, cd); scene.collection.objects.link(ob)
    cd = ob.data; cd.lens = setup.get('lens', 22); cd.sensor_width = 36; cd.sensor_fit = 'AUTO'; cd.clip_start = 0.05; cd.clip_end = 400
    ob.location = setup['loc']; fwd = (Vector(setup['look_at']) - Vector(setup['loc'])).normalized()
    if 'up' in setup:
        right = fwd.cross(Vector(setup['up'])).normalized(); up = right.cross(fwd)
        ob.rotation_euler = Matrix((right, up, -fwd)).transposed().to_euler()
    else: ob.rotation_euler = fwd.to_track_quat('-Z', 'Y').to_euler()
    if setup.get('roll'): ob.rotation_euler.rotate_axis('Z', math.radians(setup['roll']))
    scene.camera = ob
    return ob

def render(path, scene=None):
    scene = scene or bpy.context.scene; scene.render.filepath = path
    t0 = time.time(); c0 = time.process_time(); bpy.ops.render.render(write_still=True)
    return time.time() - t0, time.process_time() - c0

# ----------------------------------------------------------------------------- placeholder actors (stills and tests only)
PH = dict(boy=('beach_kid', dict(yaw=-0.3, expr='determined', arm_r='down', arm_l='down', legs='stand'), 2.4),
          priest=('boss', dict(yaw=0.35, head_roll=-4, expr='smug', arm_l='down', arm_r='hip', legs='stand'), 3.1),
          extra_a=('senior_b', dict(yaw=0.2, expr='neutral', arm_l='down', arm_r='down', legs='stand'), 2.9),
          extra_b=('beach_woman', dict(yaw=-0.25, expr='neutral', arm_l='down', arm_r='down', legs='stand'), 2.9),
          extra_c=('senior_a', dict(yaw=0.4, expr='neutral', arm_l='down', arm_r='down', legs='stand'), 3.0))

def placeholder_actor(role, mark, face_to=None, tilt=0.0, name=None, ppd=256):
    """Stand-in card from a v2/cast_ext puppet (boy = beach_kid, priest = boss, extras), scaled to the brief's heights (boy 2.4 D,
    adults about 3 D), standing at `mark`, turned to face `face_to` (yaw only) and leaned back by `tilt` degrees for high cameras."""
    sys.path.insert(0, os.path.join(PROJ, 'v3', 'cast'))
    import cast_ext                                                    # noqa: F401  (registers the extra cast in puppet)
    import puppet
    cast, pose, height = PH[role]; name = name or ('actor_' + role)
    f = puppet.figure(cast, dict(pose), name)
    bx0, by0, bx1, by1 = f['bbox']; pad = 0.08; bx0 -= pad; by0 -= pad; bx1 += pad; by1 = max(by1, f['feet_y']) + pad
    w, h = bx1 - bx0, by1 - by0; Wp, Hp = int(round(w * ppd)), int(round(h * ppd))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wp}" height="{Hp}" viewBox="{bx0:.4f} {by0:.4f} {w:.4f} {h:.4f}" style="display:block">{f["svg"]}</svg>')
    os.makedirs(ACT, exist_ok=True); tag = name + '_' + hashlib.sha1(svg.encode()).hexdigest()[:10]
    sp = os.path.join(ACT, tag + '.svg'); pp = os.path.join(ACT, tag + '.png')
    if not os.path.exists(pp):
        open(sp, 'w').write(svg); jp = os.path.join(ACT, tag + '_job.json'); json.dump([dict(src=sp, out=pp, w=Wp, h=Hp, transparent=True)], open(jp, 'w'))
        r = subprocess.run(['node', TT.RASTER, jp], capture_output=True, env=dict(os.environ, NODE_PATH=os.environ.get('NODE_PATH', '/opt/node22/lib/node_modules')))
        if r.returncode != 0: raise RuntimeError('placeholder raster failed: ' + r.stderr.decode()[-500:])
    fx = f['anchors']['feet'][0]; fy = f['feet_y']; top = min(by0 + pad, f['bbox'][1]); k = height / max(1e-6, fy - f['bbox'][1])
    me = bpy.data.meshes.new(name); xs = ((bx0 - fx) * k, (bx1 - fx) * k); zs = ((fy - by1) * k, (fy - by0) * k)
    me.from_pydata([(xs[0], 0, zs[0]), (xs[1], 0, zs[0]), (xs[1], 0, zs[1]), (xs[0], 0, zs[1])], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    me.materials.append(mat_card(name + '_mat', pp))
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); ob.location = mark; no_bounce(ob)
    yaw = 0.0
    if face_to is not None:
        d = Vector(face_to) - Vector(mark); yaw = math.atan2(d.x, -d.y)
    ob.rotation_euler = (math.radians(-tilt), 0, yaw)
    return ob

def _clear_actors(scene=None):
    scene = scene or bpy.context.scene
    for o in list(scene.objects):
        if o.name.startswith('actor_'): bpy.data.objects.remove(o, do_unlink=True)

def stage_placeholders(A, where, cam_loc):
    """'chamber': boy at hero_mark, priest at priest_mark, one extra; 'square': boy, priest and three extras on square_marks;
    'none': nobody. Cards face the camera; for a camera far above them they lean back by half its elevation."""
    _clear_actors()
    if where == 'none': return []
    out = []
    if where == 'chamber':
        F = A['chamber_floor']; spots = [('boy', F['hero_mark']), ('priest', F['priest_mark']), ('extra_a', F['extra_marks'][0])]
    else:
        S = A['square_marks']; spots = [('boy', S['hero']), ('priest', S['priest']), ('extra_a', S['extra1']), ('extra_b', S['extra2']), ('extra_c', S['extra3'])]
    for role, mk in spots:
        d = Vector(cam_loc) - Vector(mk); el = math.degrees(math.atan2(d.z - 1.5, math.hypot(d.x, d.y)))
        out.append(placeholder_actor(role, mk, face_to=cam_loc, tilt=max(0.0, el - 35) * 0.6))
    return out

STAGING = dict(square_low='square', chamber_eye='chamber', chamber_high_down='square', spire_insert='none', town_wide='square', tower_side_mid='none')

# ----------------------------------------------------------------------------- CLI
def _load(): return ' '.join('%.2f' % v for v in os.getloadavg())

def cli_stills(presets, quality='preview', outdir=None, cams=None, rod=2):
    outdir = outdir or os.path.join(WORK, 'stills'); os.makedirs(outdir, exist_ok=True)
    for pr in presets:
        A = build(pr); sc = bpy.context.scene; setup_render(sc, quality); set_rod(rod)
        if pr == 'NIGHT_STORM': flash(0.0)
        for nm, cs in A['cams'].items():
            if cams and nm not in cams: continue
            make_camera(cs); stage_placeholders(A, STAGING[nm], cs['loc'])
            w, c = render(os.path.join(outdir, '%s_%s.png' % (pr, nm))); print('%s %s: %.1f s wall, %.1f s cpu, load %s' % (pr, nm, w, c, _load()), flush=True)

def cli_timing(cam='chamber_eye', preset='DAY', n=3):
    A = build(preset); sc = bpy.context.scene; setup_render(sc, 'final'); set_rod(2)
    cs = A['cams'][cam]; cobj = make_camera(cs); stage_placeholders(A, STAGING[cam], cs['loc'])
    print('final: 720x1280, %d samples, threads %d; load %s' % (sc.cycles.samples, sc.render.threads, _load()))
    res = []
    for i in range(n):
        cobj.location.x += 0.02
        w, c = render(os.path.join(WORK, 'timing_%s_%d.png' % (cam, i))); res.append((w, c)); print('frame %d: %.2f s wall, %.2f s cpu, load %s' % (i, w, c, _load()), flush=True)
    return res

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stills'; arg = sys.argv[2:]
    if cmd == 'stills': cli_stills(arg or ['DAY', 'DUSK', 'NIGHT_STORM'])
    elif cmd == 'timing': cli_timing(*(arg[:2] if arg else []))
    else: print(__doc__)

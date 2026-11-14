#!/usr/bin/env python3
"""office3d.py : the 1938 U.S. Weather Bureau office as a real 3D Blender set (bpy 5.3, Cycles CPU).

    import office3d
    A = office3d.build("INTERIOR_DAY")           # collections SET and LIGHTS, world, render settings -> anchors
    office3d.set_track(line=0.6, erase=0.0)      # red hurricane track on the map (real geometry)
    cam = office3d.make_camera(A["cams"]["low_medium"])

World: 1 unit = 1 D (head diameter), Z up, floor z = 0, map wall = plane y = 0, room toward -y, x = 0 = map centre.
CLI:   python3 office3d.py stills | staged | timing | spike
See API.md next to this file; REVIEW.md is the independent review (measurements against the reference, what was repaired and why)"""
import os, sys, math, json, time, subprocess
import bpy
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import textures as T                                       # noqa: E402
O = T.O                                                    # v2/sets/office.py (palette, map data, track)
TMP = os.path.join(PROJ, 'v3', 'tmp', 'set3d'); OUT = os.path.join(PROJ, 'v3', 'out')

# ----------------------------------------------------------------------------- room dimensions (D)
XW = 3.8                      # side walls at x = -XW and +XW
YD = 9.0                      # room depth: the camera-side wall is y = -YD
H = 5.3                       # ceiling
Z_BASE, Z_WAIN, Z_CHAIR, Z_PRAIL0, Z_PRAIL1 = 0.16, 1.18, 1.27, 4.72, 4.80
MAP_OUT = (-1.60, 1.32, 1.60, 3.68)       # x0, z0, x1, z1 outer frame
MAP_IN = (-1.50, 1.42, 1.50, 3.58)        # paper
MAP_Y = -0.05                              # the paper surface stands 0.05 proud of the wall
WIN = dict(y0=-7.72, y1=-1.74, z0=0.36, z1=5.08, bars=(-6.71, -5.51, -4.31, -3.12), transom=2.45, wall_t=0.25)
HERO_MARK = (-0.55, -0.42, 0.0); BOSS_MARK = (1.30, -0.42, 0.0); NEAR_MARK = (2.6, -1.95, 0.0)

# ----------------------------------------------------------------------------- light model
# displayed(scene-linear) = artwork * gain * KEY * visibility + (artwork * SHADE * shade_mul + LIFT) * F   ; artwork = the texture's linear colour
# F = (1 + dot(face normal, form)) * (1 + falloff_y * y / YD): orientation and depth term of the ambient (review pass), 1 for a neutral face at the map wall
# SHADE is the flat ambient (emission, noise-free); KEY is the one hard sun. All lit materials use the direction
# to the sun as their shading normal, so every face that sees the sun gets the full KEY (two-tone, like the reference).
PRESETS = {
    # review pass (see REVIEW.md): sun angle 0.7 -> 0.45 (far bar shadows were up to 32 px soft), deeper cast shadows on the wall surfaces
    # (map / wainscot were 0.32 to 0.36 of lit in linear luminance, now 0.28 to 0.31), lighter rose wall in shade, readable ceiling.
    # form: the ambient depends on the face orientation (1 + dot(normal, form)), so boxes and wall corners read as volumes in shade.
    # falloff_y: the ambient falls from the map wall (y = 0) to the camera-side wall by this fraction, so the foreground is the darkest layer.
    'INTERIOR_DAY': dict(shade=(0.20, 0.27, 0.54), key=(2.30, 1.65, 0.74), lift=(0.0, 0.010, 0.026), key_dir=(-1.0, 1.3, -0.30), sun_angle=0.45,
                         sky=1.0, bulb=6.0, gains=dict(wallpaper=0.85, wood=0.7, floor=1.0, rug=1.0, map=0.30, paper=0.27), map_shade=0.56, wall_shade=(2.8, 2.05, 0.7), wood_shade=(0.62, 0.95, 1.1),
                         ceil_shade=(3.8, 3.0, 1.8), floor_shade=(1.06, 1.32, 1.38), form=(0.14, -0.04, 0.26), falloff_y=0.30, bloom_size=0.05,
                         grade_offset=(0.002, 0.0045, 0.010), grade_saturation=1.06),
    'INTERIOR_LAMP': dict(shade=(0.40, 0.33, 0.52), key=(0.0, 0.0, 0.0), key_dir=(-1.0, 1.3, -0.30), sun_angle=0.7,
                          sky=0.12, bulb=9.0, gains={}, lift=(0.012, 0.008, 0.022), wall_shade=1.0, form=(0.10, -0.03, 0.2), bloom_size=0.05),
}
STATE = {}                    # filled by build(): preset, objects, anchors
COS_MIN = 0.12                # faces closer than 7 degrees to edge-on to the sun fade out instead of blowing up

def hex_lin(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)

# ----------------------------------------------------------------------------- materials
def _tree(m):
    nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    return nt

def _img(path):
    im = bpy.data.images.load(path, check_existing=True)
    if path not in STATE.setdefault('images', set()): im.reload(); STATE['images'].add(path)     # pick up a texture that was redrawn since the last build
    return im

def mat_lit(name, color='#808080', image=None, gain=1.0, shade_mul=1.0, alpha=False, interp='Linear', opacity=1.0, form=None):
    """Environment surface: Emission(art x SHADE) + Diffuse(art x gain) lit by the one key. `image` = PNG path.
    form = (fx, fy, fz) or None: the ambient is multiplied by 1 + dot(face normal, form), so in shade a top face is lighter than a
    front face and that is lighter than a face turned away from the window. Noise-free (it only scales the emission)."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    P = STATE['P']; m = bpy.data.materials.new(name); nt = _tree(m); L = nt.links.new
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    dif = nt.nodes.new('ShaderNodeBsdfDiffuse'); dif.inputs['Roughness'].default_value = 0.0
    # toon key: divide the diffuse colour by the true cosine to the sun, so every face that sees the sun gets the full key
    # (two-tone, orientation-free), while visibility (the cast shadows) stays ray traced. Faces turned away get nothing.
    kd = Vector(P['key_dir']).normalized(); geo = nt.nodes.new('ShaderNodeNewGeometry')
    dot = nt.nodes.new('ShaderNodeVectorMath'); dot.operation = 'DOT_PRODUCT'; dot.inputs[1].default_value = (-kd.x, -kd.y, -kd.z); L(geo.outputs['True Normal'], dot.inputs[0])
    mxn = nt.nodes.new('ShaderNodeMath'); mxn.operation = 'MAXIMUM'; mxn.inputs[1].default_value = COS_MIN; L(dot.outputs['Value'], mxn.inputs[0])
    div = nt.nodes.new('ShaderNodeMath'); div.operation = 'DIVIDE'; div.inputs[0].default_value = gain; L(mxn.outputs[0], div.inputs[1])
    emi = nt.nodes.new('ShaderNodeEmission'); emi.inputs['Strength'].default_value = 1.0
    add = nt.nodes.new('ShaderNodeAddShader')
    ms = nt.nodes.new('ShaderNodeMix'); ms.data_type = 'RGBA'; ms.blend_type = 'MULTIPLY'; ms.inputs[0].default_value = 1.0
    sm = tuple(shade_mul) if isinstance(shade_mul, (tuple, list)) else (shade_mul,) * 3     # colour pass: a per-channel multiplier tints one surface's ambient
    ms.inputs[7].default_value = (*[s * k for s, k in zip(P['shade'], sm)], 1.0)
    md = nt.nodes.new('ShaderNodeVectorMath'); md.operation = 'SCALE'; L(div.outputs[0], md.inputs['Scale'])
    tex = None
    if image is not None:
        tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = _img(image); tex.interpolation = interp
        L(tex.outputs['Color'], ms.inputs[6]); L(tex.outputs['Color'], md.inputs[0])
    else:
        col = (*hex_lin(color), 1.0); ms.inputs[6].default_value = col; md.inputs[0].default_value = col[:3]
    lf = nt.nodes.new('ShaderNodeVectorMath'); lf.operation = 'ADD'; lf.inputs[1].default_value = tuple(P.get('lift', (0, 0, 0)))    # flat plum lift: keeps the darks from going to saturated black
    fall = float(P.get('falloff_y', 0.0)); has_form = bool(form) and any(abs(x) > 1e-6 for x in form); fac = None
    if has_form:
        fd = nt.nodes.new('ShaderNodeVectorMath'); fd.operation = 'DOT_PRODUCT'; fd.inputs[1].default_value = tuple(form); L(geo.outputs['True Normal'], fd.inputs[0])
        fa = nt.nodes.new('ShaderNodeMath'); fa.operation = 'ADD'; fa.inputs[1].default_value = 1.0; L(fd.outputs['Value'], fa.inputs[0]); fac = fa.outputs[0]
    if abs(fall) > 1e-6:                                     # depth falloff of the ambient: full at the map wall (y = 0), 1 - falloff_y at the camera-side wall
        pd = nt.nodes.new('ShaderNodeVectorMath'); pd.operation = 'DOT_PRODUCT'; pd.inputs[1].default_value = (0.0, fall / YD, 0.0); L(geo.outputs['Position'], pd.inputs[0])
        pc = nt.nodes.new('ShaderNodeMath'); pc.operation = 'ADD'; pc.inputs[1].default_value = 1.0; pc.use_clamp = True; L(pd.outputs['Value'], pc.inputs[0])
        if fac is not None:
            pm = nt.nodes.new('ShaderNodeMath'); pm.operation = 'MULTIPLY'; L(fac, pm.inputs[0]); L(pc.outputs[0], pm.inputs[1]); fac = pm.outputs[0]
        else: fac = pc.outputs[0]
    L(ms.outputs[2], lf.inputs[0])
    if fac is not None:                                      # the factor scales the whole ambient term (shade + lift): next to the lift the shade alone is too small to show it
        fs = nt.nodes.new('ShaderNodeVectorMath'); fs.operation = 'SCALE'; L(lf.outputs['Vector'], fs.inputs[0]); L(fac, fs.inputs['Scale']); L(fs.outputs['Vector'], emi.inputs['Color'])
    else: L(lf.outputs['Vector'], emi.inputs['Color'])
    L(md.outputs['Vector'], dif.inputs['Color'])
    L(dif.outputs['BSDF'], add.inputs[0]); L(emi.outputs['Emission'], add.inputs[1])
    last = add.outputs['Shader']
    if alpha and tex is not None:
        tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
        L(tex.outputs['Alpha'], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(last, mx.inputs[2]); last = mx.outputs['Shader']
    if opacity < 1.0:
        tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader'); mx.inputs['Fac'].default_value = opacity
        L(tr.outputs['BSDF'], mx.inputs[1]); L(last, mx.inputs[2]); last = mx.outputs['Shader']
    L(last, out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def mat_emit(name, color='#ffffff', image=None, strength=1.0, alpha=False, camera_only=False):
    """Unlit surface (sky card, bulbs, glowing slits). strength > 1 feeds the bloom."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = _tree(m); L = nt.links.new
    out = nt.nodes.new('ShaderNodeOutputMaterial'); emi = nt.nodes.new('ShaderNodeEmission'); emi.inputs['Strength'].default_value = strength
    tex = None
    if image is not None:
        tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = _img(image); L(tex.outputs['Color'], emi.inputs['Color'])
    else: emi.inputs['Color'].default_value = (*hex_lin(color), 1.0)
    last = emi.outputs['Emission']
    if alpha and tex is not None:
        tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
        L(tex.outputs['Alpha'], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(last, mx.inputs[2]); last = mx.outputs['Shader']
    L(last, out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def mat_card(name, image_path):
    """Actor card: shows the drawing exactly (emission to camera rays only, never lit), alpha cut-out, blocks the sun."""
    m = bpy.data.materials.new(name); nt = _tree(m); L = nt.links.new
    out = nt.nodes.new('ShaderNodeOutputMaterial'); tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = _img(image_path); tex.extension = 'CLIP'
    lp = nt.nodes.new('ShaderNodeLightPath'); emi = nt.nodes.new('ShaderNodeEmission')
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mix = nt.nodes.new('ShaderNodeMixShader')
    L(tex.outputs['Color'], emi.inputs['Color']); L(lp.outputs['Is Camera Ray'], emi.inputs['Strength'])
    L(tex.outputs['Alpha'], mix.inputs['Fac']); L(tr.outputs['BSDF'], mix.inputs[1]); L(emi.outputs['Emission'], mix.inputs[2])
    L(mix.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def mat_ink(name='ink', ink_hex='#2a1712'):
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = _tree(m); L = nt.links.new
    out = nt.nodes.new('ShaderNodeOutputMaterial'); geo = nt.nodes.new('ShaderNodeNewGeometry'); lp = nt.nodes.new('ShaderNodeLightPath')
    emi = nt.nodes.new('ShaderNodeEmission'); emi.inputs['Color'].default_value = (*hex_lin(ink_hex), 1.0)
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mix = nt.nodes.new('ShaderNodeMixShader')
    notcam = nt.nodes.new('ShaderNodeMath'); notcam.operation = 'SUBTRACT'; notcam.inputs[0].default_value = 1.0
    fac = nt.nodes.new('ShaderNodeMath'); fac.operation = 'MAXIMUM'
    L(lp.outputs['Is Camera Ray'], notcam.inputs[1]); L(geo.outputs['Backfacing'], fac.inputs[0]); L(notcam.outputs[0], fac.inputs[1])
    L(fac.outputs[0], mix.inputs['Fac']); L(emi.outputs['Emission'], mix.inputs[1]); L(tr.outputs['BSDF'], mix.inputs[2]); L(mix.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

# ----------------------------------------------------------------------------- mesh builder
class MB:
    """Collects polygons (welded vertices, per-loop UVs, per-face material) and makes one mesh object."""
    def __init__(s): s.v = []; s.vi = {}; s.f = []; s.uv = []; s.mi = []; s.mats = []; s._in = False; s.pid = 0     # pid: vertices are welded only inside one primitive
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
    def quad(s, p0, pu, pv, mat, uv=(0.0, 0.0, 1.0, 1.0)):
        """Corner p0, edge vectors pu and pv (normal = pu x pv). uv = (u0, v0, u1, v1) over the quad."""
        p0, pu, pv = Vector(p0), Vector(pu), Vector(pv); u0, v0, u1, v1 = uv
        if not s._in: s.pid += 1
        s.face([p0, p0 + pu, p0 + pu + pv, p0 + pv], mat, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)])
    def box(s, lo, hi, mat, mats=None, tile=None, skip=''):
        """Axis-aligned box. mats = {'front'|'back'|'left'|'right'|'top'|'bottom': material} overrides; front = the -y face.
        tile = (tu, tv) in D: UVs in world units / tile (for repeating textures); otherwise each face maps 0..1."""
        x0, y0, z0 = lo; x1, y1, z1 = hi; dx, dy, dz = x1 - x0, y1 - y0, z1 - z0; mats = mats or {}; s.pid += 1; s._in = True
        faces = dict(front=((x0, y0, z0), (dx, 0, 0), (0, 0, dz), (x0, z0, dx, dz)), back=((x1, y1, z0), (-dx, 0, 0), (0, 0, dz), (-x1, z0, dx, dz)),
                     right=((x1, y0, z0), (0, dy, 0), (0, 0, dz), (y0, z0, dy, dz)), left=((x0, y1, z0), (0, -dy, 0), (0, 0, dz), (-y1, z0, dy, dz)),
                     top=((x0, y0, z1), (dx, 0, 0), (0, dy, 0), (x0, y0, dx, dy)), bottom=((x0, y1, z0), (dx, 0, 0), (0, -dy, 0), (x0, -y1, dx, dy)))
        for k, (p0, pu, pv, (a, b, w, h)) in faces.items():
            if k in skip.split(','): continue
            uv = (a / tile[0], b / tile[1], (a + w) / tile[0], (b + h) / tile[1]) if tile else (0.0, 0.0, 1.0, 1.0)
            s.quad(p0, pu, pv, mats.get(k, mat), uv)
        s._in = False
    def frustum(s, p0, p1, r0, r1, mat, seg=14, cap0=True, cap1=True, cap_mat=None):
        """Cylinder / cone from p0 (radius r0) to p1 (radius r1)."""
        p0, p1 = Vector(p0), Vector(p1); a = (p1 - p0).normalized(); s.pid += 1
        u = a.cross(Vector((0, 0, 1)));
        if u.length < 1e-4: u = Vector((1, 0, 0))
        u.normalize(); v = a.cross(u)
        ring = lambda p, r: [p + r * (math.cos(2 * math.pi * i / seg) * u + math.sin(2 * math.pi * i / seg) * v) for i in range(seg)]
        A, B = ring(p0, r0), ring(p1, r1)
        for i in range(seg):
            j = (i + 1) % seg; s.face([A[i], A[j], B[j], B[i]], mat)
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

def _coll(name, scene):
    c = bpy.data.collections.get(name)
    if c is None: c = bpy.data.collections.new(name)
    if name not in [k.name for k in scene.collection.children]: scene.collection.children.link(c)
    return c

def _wipe(coll):
    for ob in list(coll.objects): bpy.data.objects.remove(ob, do_unlink=True)

# ----------------------------------------------------------------------------- render settings
def setup_render(scene, quality='final'):
    """Cycles CPU, direct light only, Standard view. quality: 'final' (720x1280, 16 samples, 4 threads), 'fast' (same, 12 samples)
    or 'preview' (360x640, 8 samples, 2 threads)."""
    r = scene.render; c = scene.cycles
    r.engine = 'CYCLES'; c.device = 'CPU'
    c.use_adaptive_sampling = False; c.use_denoising = False
    c.max_bounces = 1; c.diffuse_bounces = 0; c.glossy_bounces = 0; c.transmission_bounces = 0; c.volume_bounces = 0; c.transparent_max_bounces = 8
    c.caustics_reflective = False; c.caustics_refractive = False; c.sample_clamp_indirect = 3.0
    c.use_light_tree = False
    # Cycles always traces one last bounce ray (it may only pick up emission). Every set object is hidden from those rays
    # (no_bounce), and the 'fast GI replace' switch below shortens that ray to 1 mm, so it costs almost nothing.
    c.use_fast_gi = True; c.fast_gi_method = 'REPLACE'; c.ao_bounces_render = 1; c.ao_bounces = 1
    if scene.world: scene.world.light_settings.distance = 0.001
    vs = scene.view_settings; vs.view_transform = 'Standard'; vs.look = 'None'; vs.exposure = 0.0; vs.gamma = 1.0
    scene.display_settings.display_device = 'sRGB'
    r.film_transparent = False; r.resolution_x = 720; r.resolution_y = 1280; r.fps = 30
    r.image_settings.file_format = 'PNG'; r.image_settings.color_mode = 'RGB'; r.use_persistent_data = True
    if quality in ('final', 'fast'):                     # fast = 12 samples: 25 percent cheaper, slightly coarser edges and penumbra
        c.samples = 16 if quality == 'final' else 12; r.resolution_percentage = 100; r.threads_mode = 'FIXED'; r.threads = 4
    else:
        c.samples = 8; r.resolution_percentage = 50; r.threads_mode = 'FIXED'; r.threads = 2

def setup_grade(scene, bloom=True):
    """Compositor: tight bloom on values above 1.0, plum black point (ASC-CDL), saturation 1.12. No vignette."""
    sys.path.insert(0, os.path.join(PROJ, 'spec'))
    import warnings
    import grade_compositor as G
    for ng in list(bpy.data.node_groups):
        if ng.name.startswith('GradeCLP'): bpy.data.node_groups.remove(ng)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        gp = dict(vignette_strength=0.0, bloom_strength=0.5 if bloom else 0.0, bloom_size=STATE.get('P', {}).get('bloom_size', 0.05))
        if 'grade_offset' in STATE.get('P', {}): gp['offset'] = tuple(STATE['P']['grade_offset'])     # colour pass: navy-plum black point instead of the spec's plum
        if 'grade_saturation' in STATE.get('P', {}): gp['saturation'] = float(STATE['P']['grade_saturation'])
        ng = G.build(scene, preset=gp)
    scene.render.use_compositing = True
    return ng

# ----------------------------------------------------------------------------- the set
def _wq(mb, wall, a0, a1, z0, z1, d, mat, uv):
    """Inward-facing quad on a wall, d = distance in front of the wall plane; a = coordinate along the wall."""
    L = a1 - a0; dz = z1 - z0
    if wall == 'map': mb.quad((a0, -d, z0), (L, 0, 0), (0, 0, dz), mat, uv)
    elif wall == 'left': mb.quad((-XW + d, a0, z0), (0, L, 0), (0, 0, dz), mat, uv)
    elif wall == 'right': mb.quad((XW - d, a1, z0), (0, -L, 0), (0, 0, dz), mat, uv)
    else: mb.quad((a1, -YD + d, z0), (-L, 0, 0), (0, 0, dz), mat, uv)

def _wb(mb, wall, a0, a1, z0, z1, d0, d1, mat, **kw):
    """Box standing d0..d1 in front of a wall."""
    if wall == 'map': mb.box((a0, -d1, z0), (a1, -d0, z1), mat, **kw)
    elif wall == 'left': mb.box((-XW + d0, a0, z0), (-XW + d1, a1, z1), mat, **kw)
    elif wall == 'right': mb.box((XW - d1, a0, z0), (XW - d0, a1, z1), mat, **kw)
    else: mb.box((a0, -YD + d0, z0), (a1, -YD + d1, z1), mat, **kw)

def _wall(mb, rl, M, wall, a0, a1, zlo=0.0, zhi=None, rails=True):
    """Paper, frieze and wainscot bands of one wall run (clipped to zlo..zhi) + relief: baseboard, stiles, chair rail, picture rail, crown."""
    zhi = H if zhi is None else zhi; flip = wall in ('right', 'back'); tw = T.SIZE['wainscot'][0]
    def uu(a): return -a if flip else a
    def band(z0, z1, mat, tu, tv, vo, d=0.0):
        z0, z1 = max(z0, zlo), min(z1, zhi)
        if z1 - z0 < 1e-6: return
        ua, ub = (uu(a1), uu(a0)) if flip else (a0, a1)
        _wq(mb, wall, a0, a1, z0, z1, d, mat, (ua / tu, (z0 - vo) / tv, ub / tu, (z1 - vo) / tv))
    band(Z_BASE, Z_WAIN, M['wainscot'], tw, Z_WAIN - Z_BASE, Z_BASE, d=0.03)
    band(Z_CHAIR, Z_PRAIL0, M['wallpaper'], 0.32, 0.76, Z_PRAIL0); band(Z_PRAIL1, H, M['frieze'], 0.4, 0.5, Z_PRAIL1)
    band(0.0, Z_BASE, M['base'], 1, 1, 0); band(Z_WAIN, Z_CHAIR, M['rail'], 1, 1, 0); band(Z_PRAIL0, Z_PRAIL1, M['prail'], 1, 1, 0)
    if not rails: return
    def rb(z0, z1, d, mat):
        z0, z1 = max(z0, zlo), min(z1, zhi)
        if z1 - z0 > 1e-6: _wb(rl, wall, a0, a1, z0, z1, 0.0, d, mat)
    rb(0.0, Z_BASE, 0.07, M['base']); rb(Z_WAIN - 0.02, Z_CHAIR, 0.085, M['rail']); rb(Z_PRAIL0, Z_PRAIL1, 0.05, M['prail']); rb(H - 0.1, H, 0.09, M['crown'])
    k0 = int(math.floor(uu(a1 if flip else a0) / tw)); k1 = int(math.ceil(uu(a0 if flip else a1) / tw))
    for k in range(k0, k1 + 1):                       # stiles on the panel joints
        a = uu(k * tw)
        if a0 + 0.07 < a < a1 - 0.07 and min(Z_WAIN, zhi) - max(Z_BASE, zlo) > 0.05: _wb(rl, wall, a - 0.06, a + 0.06, max(Z_BASE, zlo), min(Z_WAIN - 0.02, zhi), 0.03, 0.052, M['stile'])

def build(preset='INTERIOR_DAY', clear=True):
    """Build the office into the current scene (collections SET and LIGHTS, world, render settings). Returns the anchors dict."""
    scene = bpy.context.scene; P = dict(PRESETS[preset]); STATE.clear(); STATE['P'] = P; STATE['preset'] = preset
    if clear:
        for ob in list(scene.objects): bpy.data.objects.remove(ob, do_unlink=True)
    SET = _coll('SET', scene); LIGHTS = _coll('LIGHTS', scene); _wipe(SET); _wipe(LIGHTS)
    for m in list(bpy.data.materials):                      # our own materials are rebuilt (they are cached by name)
        if m.name.startswith(('INTERIOR_', 'ink')): bpy.data.materials.remove(m)
    _ALPHA.clear()
    tx = T.ensure(verbose=False)
    w = bpy.data.worlds.get('W_office') or bpy.data.worlds.new('W_office'); scene.world = w; nt = _tree(w)
    setup_render(scene, 'final')
    bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld'); bg.inputs['Color'].default_value = (0, 0, 0, 1); bg.inputs['Strength'].default_value = 0.0
    nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
    kd = Vector(P['key_dir']).normalized()
    pre = preset + '_'
    FORM = tuple(P.get('form', (0, 0, 0)))                  # orientation term of the ambient; form=False switches it off for one material
    def _sm(v): return 'x'.join('%g' % x for x in v) if isinstance(v, (tuple, list)) else '%g' % v
    def C(hexcol, gain=1.0, shade_mul=1.0, form=True): return mat_lit('%sflat_%s_%g_%s_%d' % (pre, hexcol.lstrip('#'), gain, _sm(shade_mul), bool(form)), hexcol, gain=gain, shade_mul=shade_mul, form=FORM if form else None)
    def TX(name, gain=1.0, shade_mul=1.0, alpha=False, form=True): return mat_lit('%stex_%s_%g_%s_%d' % (pre, name, gain, _sm(shade_mul), bool(form)), image=tx[name], gain=gain, shade_mul=shade_mul, alpha=alpha, form=FORM if form else None)
    def E(hexcol, strength): return mat_emit('%semit_%s_%g' % (pre, hexcol.lstrip('#'), strength), hexcol, strength=strength)
    G = P.get('gains', {})
    def _t3(v): return tuple(v) if isinstance(v, (tuple, list)) else (v,) * 3
    M = dict(
        wallpaper=TX('wallpaper', G.get('wallpaper', 1.0), P.get('wall_shade', 1.0)), frieze=TX('frieze', G.get('wallpaper', 1.0), tuple(x * 0.8 for x in _t3(P.get('wall_shade', 1.0)))),
        wainscot=TX('wainscot', G.get('wood', 1.0), P.get('wood_shade', 1.0)),
        base=C(O.BASEC), rail=C(O.RAILC, G.get('wood', 1.0), P.get('wood_shade', 1.0)), stile=C(O.WOOD, G.get('wood', 1.0), P.get('wood_shade', 1.0)), prail=C(O.PRAIL, 0.5), crown=C('#6b3a26'),
        planks=TX('planks', G.get('floor', 1.0), P.get('floor_shade', 1.0), form=False), rug=TX('rug', G.get('rug', 1.0), form=False), rug_end=TX('rug_end', G.get('rug', 1.0), alpha=True, form=False),
        ceiling=TX('ceiling', 1.0, P.get('ceil_shade', 1.0), form=False), beam=C('#4a2616', 1.0, (3.4, 2.6, 1.4)), frame=C('#3d1c12', 1.0, 1.25), gold=C(O.GOLD, 0.5),
        map=TX('map', G.get('map', 0.30), P.get('map_shade', 1.0), form=False), wood=C('#7b3b26'), winframe=C('#6f3522', 1.0, 1.15),
        sky=mat_emit(pre + 'sky', image=tx['sky'], strength=P['sky']), reveal=C('#b88a68', 0.8), paper=C('#f6efe2', G.get('paper', 0.27)), brass=C(O.BRASS, 0.5),
        green=C('#2d7a52', 1.0, 1.2), steel=C(O.STEEL), dark=C('#20263c', 1.0, 1.2), iron=C('#2f3444', 1.0, 1.2),
        bulb=E(O.BULB, P['bulb']), slit=E('#fff1c4', P['bulb'] * 0.6))
    hull = lambda dist: 0.00384 * dist                    # 3 px ink at camera distance `dist`

    # ---- floor, rug, ceiling with beams
    mb = MB(); tw, th = T.SIZE['planks']
    mb.quad((-XW, -YD, 0), (2 * XW, 0, 0), (0, YD, 0), M['planks'], (-XW / tw, -YD / th, XW / tw, 0.0)); mb.obj('floor', SET)
    mb = MB(); RX = 1.2; y_end = -0.62; tl = T.SIZE['rug'][1]; el = T.SIZE['rug_end'][1]; zr = 0.014
    mb.quad((-RX, -YD, zr), (2 * RX, 0, 0), (0, YD + y_end - el + 0.001, 0), M['rug'], (0, -(YD + y_end - el) / tl, 1, 0))
    mb.quad((-RX, y_end - el, zr), (2 * RX, 0, 0), (0, el, 0), M['rug_end'], (0, 0, 1, 1)); mb.obj('rug', SET)
    mb = MB(); tw, th = T.SIZE['ceiling']
    mb.quad((-XW, 0, H), (2 * XW, 0, 0), (0, -YD, 0), M['ceiling'], (-XW / tw, 0, XW / tw, YD / th))
    mb.obj('ceiling', SET)
    mb = MB()                                                # cross beams with a lighter chamfer strip: inked, so they read against the boards
    for yb in (-1.9, -4.4, -6.9):
        mb.box((-XW, yb - 0.17, H - 0.36), (XW, yb + 0.17, H + 0.01), M['beam'], mats=dict(front=TX('beam', 1.0, (3.4, 2.6, 1.4)), back=TX('beam', 1.0, (3.4, 2.6, 1.4))))
        mb.box((-XW, yb - 0.2, H - 0.07), (XW, yb + 0.2, H + 0.005), C('#5c3220', 1.0, (3.4, 2.6, 1.4)))
    mb.obj('beams', SET, hull=hull(5.5))

    # ---- walls with relief
    W = WIN; mb = MB(); rl = MB()
    _wall(mb, rl, M, 'map', -XW, XW); _wall(mb, rl, M, 'left', -YD, 0.0); _wall(mb, rl, M, 'back', -XW, XW, rails=False)
    _wall(mb, rl, M, 'right', W['y1'], 0.0); _wall(mb, rl, M, 'right', -YD, W['y0'])
    _wall(mb, rl, M, 'right', W['y0'], W['y1'], zhi=W['z0']); _wall(mb, rl, M, 'right', W['y0'], W['y1'], zlo=W['z1'])
    t = W['wall_t']                                          # thick outer slab: the reveal throws its own shadow edge
    for (ya, yb, za, zb) in ((W['y1'], 0.3, 0, H), (-YD - 0.3, W['y0'], 0, H), (W['y0'], W['y1'], -0.2, W['z0']), (W['y0'], W['y1'], W['z1'], H + 0.3)):
        mb.box((XW + 0.001, ya, za), (XW + t, yb, zb), M['reveal'])
    mb.obj('walls', SET); rl.obj('wall_relief', SET, hull=hull(4.5))
    # window: frame, glazing bars, transom, sill (real boxes: they throw the bar shadows), sky card outside
    mb = MB(); f = 0.09; xf0, xf1 = XW + 0.04, XW + 0.15
    mb.box((xf0, W['y0'], W['z0']), (xf1, W['y0'] + f, W['z1']), M['winframe']); mb.box((xf0, W['y1'] - f, W['z0']), (xf1, W['y1'], W['z1']), M['winframe'])
    mb.box((xf0, W['y0'], W['z1'] - f), (xf1, W['y1'], W['z1']), M['winframe']); mb.box((xf0, W['y0'], W['z0']), (xf1, W['y1'], W['z0'] + f), M['winframe'])
    for yb in W['bars']: mb.box((xf0 + 0.01, yb - 0.055, W['z0']), (xf1 - 0.01, yb + 0.055, W['z1']), M['winframe'])
    mb.box((xf0 + 0.02, W['y0'], W['transom'] - 0.05), (xf1 - 0.02, W['y1'], W['transom'] + 0.05), M['winframe'])
    mb.box((XW - 0.13, W['y0'] - 0.08, W['z0'] - 0.07), (XW + 0.02, W['y1'] + 0.08, W['z0']), M['wood'])
    mb.obj('window', SET, hull=hull(5.0))
    mb = MB(); mb.quad((XW + 7.0, 20.0, -4.0), (0, -54.0, 0), (0, 0, 15.2), M['sky'], (0, 0, 3, 1)); sk = mb.obj('sky', SET); sk.visible_shadow = False

    # ---- the wall map: paper, frame mouldings with a gold slip, chalk ledge with pencils and erasers
    X0, Z0, X1, Z1 = MAP_OUT; x0, z0, x1, z1 = MAP_IN; fy = MAP_Y - 0.06
    mb = MB(); mb.quad((x0, MAP_Y, z0), (x1 - x0, 0, 0), (0, 0, z1 - z0), M['map'], (0, 0, 1, 1)); mb.obj('map_paper', SET)
    mb = MB()
    mb.box((X0, fy, Z0), (x0, 0, Z1), M['frame']); mb.box((x1, fy, Z0), (X1, 0, Z1), M['frame'])
    mb.box((x0, fy, Z0), (x1, 0, z0), M['frame']); mb.box((x0, fy, z1), (x1, 0, Z1), M['frame'])
    mb.obj('map_frame', SET, hull=hull(4.2))
    mb = MB(); g = 0.022; gy = MAP_Y - 0.012                 # gold slip inside the frame
    for (a, b, c_, d_) in ((x0, z0, x1, z0 + g), (x0, z1 - g, x1, z1), (x0, z0, x0 + g, z1), (x1 - g, z0, x1, z1)): mb.box((a, gy, b), (c_, MAP_Y + 0.001, d_), M['gold'])
    mb.obj('map_slip', SET)
    mb = MB(); lz = Z0 - 0.005
    mb.box((X0 - 0.09, -0.19, lz - 0.1), (X1 + 0.09, 0, lz), M['wood']); mb.box((X0 - 0.09, -0.205, lz - 0.035), (X1 + 0.09, -0.19, lz + 0.02), C('#a85a38'))
    for bx in (X0 + 0.25, X1 - 0.25): mb.box((bx - 0.04, -0.15, lz - 0.24), (bx + 0.04, 0, lz - 0.1), C('#5c2c1c'))
    mb.obj('map_ledge', SET, hull=hull(4.2))
    mb = MB()
    mb.box((-1.32, -0.15, lz), (-1.08, -0.05, lz + 0.075), C('#3a3e4c')); mb.box((-1.32, -0.15, lz + 0.05), (-1.08, -0.05, lz + 0.078), C('#b08a52'))
    mb.box((0.74, -0.14, lz), (0.87, -0.06, lz + 0.052), C('#e58d86', 0.6)); mb.box((-0.86, -0.12, lz), (-0.50, -0.09, lz + 0.03), C('#c8301c', 0.6))
    mb.box((1.18, -0.13, lz), (1.48, -0.10, lz + 0.028), C('#2f5a8a')); mb.box((-0.3, -0.14, lz), (-0.2, -0.07, lz + 0.034), M['paper'])
    mb.obj('ledge_props', SET, hull=0.006)

    # ---- things on the map wall
    def card(name, tex, cx, cz, w, h, d=0.03, depth_from=0.0, wall='map', hull_t=0.0, gain=0.28, alpha=True):
        mb = MB(); m = TX(tex, gain, alpha=alpha)
        if wall == 'map': mb.quad((cx - w / 2, -(depth_from + d), cz - h / 2), (w, 0, 0), (0, 0, h), m, (0, 0, 1, 1))
        else: mb.quad((-XW + depth_from + d, cx - w / 2, cz - h / 2), (0, w, 0), (0, 0, h), m, (0, 0, 1, 1))
        return mb.obj(name, SET, hull=hull_t)
    # sign board hanging from the picture rail on two chains
    mb = MB(); sm = TX('sign', 0.5); sw_, sh_ = T.SIZE['sign']; sz = 4.12
    mb.box((-sw_ / 2 + 0.02, -0.075, sz - 0.22), (sw_ / 2 - 0.02, -0.015, sz + 0.22), C('#3d1c12', 1.0, 1.25))
    for sx in (-1.2, 1.2): mb.box((sx - 0.012, -0.05, sz + 0.22), (sx + 0.012, -0.035, Z_PRAIL0 + 0.02), M['brass'])
    mb.obj('sign', SET, hull=hull(4.5))
    mb = MB(); mb.quad((-sw_ / 2, -0.078, sz - sh_ / 2), (sw_, 0, 0), (0, 0, sh_), TX('sign', 0.5, alpha=True), (0, 0, 1, 1)); mb.obj('sign_face', SET)
    # clock (drum + face card), calendar, pin board, banjo barometer, thermometer plate
    mb = MB(); mb.frustum((2.12, -0.01, 4.05), (2.12, -0.13, 4.05), 0.40, 0.40, C('#4a2216', 1.0, 1.2), seg=20)
    mb.box((1.96, -0.10, 3.26), (2.28, -0.01, 3.78), C('#4a2216', 1.0, 1.2)); mb.obj('clock', SET, hull=hull(4.5))
    card('clock_face', 'clock', 2.12, 4.05 - 0.02, 0.952, 0.952, d=0.004, depth_from=0.13)
    mb = MB(); mb.box((-2.12, -0.045, 3.72), (-1.56, -0.005, 4.50), M['paper']); mb.obj('calendar', SET, hull=hull(4.5))
    card('calendar_face', 'calendar', -1.84, 4.12, 0.60, 0.82, d=0.003, depth_from=0.045)
    mb = MB(); mb.box((2.62, -0.06, 3.10), (3.56, -0.005, 4.32), C('#4a2216', 1.0, 1.2)); mb.obj('pinboard', SET, hull=hull(4.5))
    card('pinboard_face', 'pinboard', 3.09, 3.71, 0.94, 1.22, d=0.003, depth_from=0.06)
    card('barometer', 'barometer', -1.92, 2.78, 0.72, 1.44, d=0.04)
    mb = MB(); mb.box((1.76, -0.03, 1.66), (1.86, -0.005, 2.14), C('#f3e7c9', 0.27)); mb.box((1.795, -0.036, 1.72), (1.825, -0.03, 1.96), C('#c2311e', 0.6)); mb.obj('thermometer', SET, hull=0.01)

    mb = MB(); mb.box((1.98, -0.04, 2.36), (2.52, -0.005, 3.04), C('#4a2216', 1.0, 1.2)); mb.obj('certificate', SET, hull=hull(4.5))
    card('certificate_face', 'certificate', 2.25, 2.70, 0.50, 0.64, d=0.003, depth_from=0.04)
    # left wall: a second notice board, a radiator under it
    mb = MB(); mb.box((-XW + 0.005, -3.5, 2.35), (-XW + 0.06, -2.4, 3.75), C('#4a2216', 1.0, 1.2)); mb.obj('board_left', SET, hull=hull(5.0))
    mb = MB(); mb.quad((-XW + 0.063, -3.47, 2.38), (0, 1.04, 0), (0, 0, 1.34), TX('pinboard', 0.28, alpha=True), (0, 0, 1, 1)); mb.obj('board_left_face', SET)
    mb = MB(); mb.box((-XW + 0.06, -3.55, 0.08), (-XW + 0.26, -2.35, 0.98), C('#5d6478'), mats=dict(right=TX('radiator')))
    mb.obj('radiator_left', SET, hull=hull(5.0))

    # ---- pendant lamps at different depths (above the sun beam: they throw no shadow on the map)
    lamps = [(-2.6, -1.3, 4.30), (0.4, -2.6, 4.27), (-1.7, -4.4, 4.05), (0.2, -6.4, 4.32)]
    mb = MB(); bl = MB()
    for (lx, ly, lz_) in lamps:
        mb.frustum((lx, ly, lz_ - 0.08), (lx, ly, lz_ + 0.36), 0.47, 0.09, M['green'], seg=18, cap0=False)
        mb.frustum((lx, ly, lz_ + 0.36), (lx, ly, lz_ + 0.48), 0.05, 0.05, M['brass'], seg=8)
        mb.frustum((lx, ly, lz_ + 0.48), (lx, ly, H), 0.012, 0.012, M['iron'], seg=6, cap0=False, cap1=False)
        bl.sphere((lx, ly, lz_), 0.2, M['bulb'], seg=28, rings=14)
    mb.obj('pendants', SET, hull=hull(5.0)); b = bl.obj('pendant_bulbs', SET); b.visible_shadow = False

    # ---- furniture near the map wall
    # filing cabinets (left of the map), box file + papers on top
    mb = MB(); cf = TX('cab_front', 1.0)
    for i in range(2):
        cx0 = -3.76 + i * 0.76; mb.box((cx0, -0.95, 0), (cx0 + 0.75, -0.02, 3.0), M['steel'], mats=dict(front=cf))
        mb.box((cx0 - 0.015, -0.97, 3.0), (cx0 + 0.765, -0.02, 3.06), C(O.mul(O.STEEL, 1.3)))
    mb.obj('cabinets', SET, hull=hull(5.0))
    mb = MB(); mb.box((-3.6, -0.7, 3.06), (-3.26, -0.3, 3.38), C('#b08a52')); mb.box((-2.95, -0.8, 3.06), (-2.45, -0.3, 3.14), M['paper'], mats=dict(top=TX('paper', 0.27)))
    mb.obj('cabinet_top', SET, hull=hull(5.0))
    # waste basket with rolled charts
    mb = MB(); bx_, by_ = -2.05, -0.5
    mb.frustum((bx_, by_, 0), (bx_, by_, 0.62), 0.2, 0.27, C('#8a6a3e'), seg=14, cap1=False)
    for (dx, dy, tl_, rr) in ((-0.08, 0.03, (0.05, 0.02), 0.05), (0.07, -0.04, (-0.03, 0.05), 0.045), (0.0, 0.09, (0.02, -0.04), 0.04)):
        mb.frustum((bx_ + dx, by_ + dy, 0.1), (bx_ + dx + tl_[0] * 4, by_ + dy + tl_[1] * 4, 1.25), rr, rr, C('#f1e3c0', 0.27), seg=8)
    mb.obj('basket', SET, hull=hull(4.5))
    # radiator (right of the map) and teletype on its stand (right corner)
    mb = MB(); mb.box((1.95, -0.26, 0.08), (3.2, -0.06, 0.98), C('#5d6478'), mats=dict(front=TX('radiator')))
    for xx in (2.0, 3.09): mb.box((xx, -0.24, 0), (xx + 0.06, -0.08, 0.08), C('#3c4458'))
    mb.obj('radiator', SET, hull=hull(4.5))
    mb = MB(); tx0, tx1, ty0, ty1 = 2.72, 3.62, -1.25, -0.4
    for (lx, ly) in ((tx0 + 0.05, ty0 + 0.05), (tx1 - 0.05, ty0 + 0.05), (tx0 + 0.05, ty1 - 0.05), (tx1 - 0.05, ty1 - 0.05)): mb.box((lx - 0.03, ly - 0.03, 0), (lx + 0.03, ly + 0.03, 1.2), M['iron'])
    mb.box((tx0, ty0, 0.5), (tx1, ty1, 0.56), M['iron']); mb.box((tx0 - 0.02, ty0 - 0.02, 1.2), (tx1 + 0.02, ty1 + 0.02, 1.28), C('#3c4458'))
    mb.box((tx0 + 0.02, ty0 + 0.08, 1.28), (tx1 - 0.02, ty1 - 0.05, 1.88), M['dark'], mats=dict(front=TX('teletype')))
    mb.box((tx0 + 0.18, ty1 - 0.3, 1.88), (tx1 - 0.18, ty1 - 0.27, 2.36), M['paper'], mats=dict(front=TX('paper', 0.27)))
    mb.obj('teletype', SET, hull=hull(4.5))
    # coat stand by the left wall (pole + card with coat and hat, turned to the room)
    cw, ch = T.SIZE['coatstand']; mb = MB(); px_, py_ = -3.3, -1.75
    mb.quad((px_ - 0.3 * cw, py_ - 0.3 * cw, 0.0), (0.72 * cw, 0.72 * cw * 0.55, 0), (0, 0, ch), TX('coatstand', 1.0, alpha=True), (0, 0, 1, 1)); mb.obj('coatstand', SET)

    # ---- foreground desk (camera side, left of the runner) with banker's lamp, telephone, papers; chair
    dx0, dx1, dy0, dy1, dz = -3.45, -1.45, -5.0, -3.75, 1.45
    mb = MB(); dw = C('#5b2e1c')
    mb.box((dx0 + 0.05, dy0 + 0.06, 0), (dx1 - 0.05, dy1 - 0.06, dz - 0.1), dw, mats=dict(front=TX('desk_front')))
    mb.box((dx0 - 0.04, dy0 - 0.04, dz - 0.1), (dx1 + 0.04, dy1 + 0.04, dz), C('#a56a3c'), mats=dict(top=TX('desk_top', 1.0, 1.5)))
    mb.obj('desk', SET, hull=hull(2.6))
    mb = MB(); lx, ly = -1.95, -4.05                         # banker's lamp at the right end of the desk
    mb.box((lx - 0.2, ly - 0.12, dz), (lx + 0.2, ly + 0.12, dz + 0.06), M['brass']); mb.frustum((lx, ly, dz + 0.06), (lx, ly, dz + 0.5), 0.028, 0.028, M['brass'], seg=8)
    mb.box((lx - 0.36, ly - 0.2, dz + 0.5), (lx + 0.36, ly + 0.14, dz + 0.56), M['green']); mb.box((lx - 0.3, ly - 0.14, dz + 0.56), (lx + 0.3, ly + 0.08, dz + 0.7), M['green'])
    mb.obj('banker_lamp', SET, hull=hull(2.4))
    mb = MB(); mb.box((lx - 0.31, ly - 0.17, dz + 0.455), (lx + 0.31, ly + 0.11, dz + 0.5), M['slit']); o_ = mb.obj('banker_glow', SET); o_.visible_shadow = False
    mb = MB(); tp = C('#1c1e2c', 1.0, 1.3)                   # telephone, paper stack, ink bottle, pencil
    mb.box((-3.2, -4.25, dz), (-2.75, -3.95, dz + 0.16), tp); mb.box((-3.28, -4.16, dz + 0.2), (-2.67, -4.04, dz + 0.3), tp); mb.box((-3.02, -4.14, dz + 0.16), (-2.93, -4.06, dz + 0.2), tp)
    mb.box((-2.55, -4.75, dz), (-2.05, -4.1, dz + 0.05), M['paper'], mats=dict(top=TX('paper', 0.25, 1.3)))
    mb.frustum((-1.63, -4.22, dz), (-1.63, -4.22, dz + 0.16), 0.07, 0.055, C(O.NAVY, 1.0, 1.6), seg=12); mb.frustum((-1.63, -4.22, dz + 0.16), (-1.63, -4.22, dz + 0.22), 0.032, 0.032, C('#1c1a22', 1.0, 1.4), seg=8)
    mb.box((-2.6, -4.9, dz), (-2.1, -4.86, dz + 0.035), C('#c8301c', 0.6))
    mb.box((-1.9, -4.86, dz), (-1.58, -4.45, dz + 0.012), M['paper'], mats=dict(top=TX('paper', 0.25, 0.85)))          # typed sheet at the camera end of the desk
    mb.box((-1.8, -4.4, dz), (-1.5, -4.37, dz + 0.03), C('#2f5a8a', 1.0, 1.3))
    mb.obj('desk_props', SET, hull=hull(1.3))
    mb = MB(); cx_, cy_ = -2.45, -5.75; cc = C('#55291a'); cl = C(O.mul('#55291a', 1.3))       # chair, back to the camera
    mb.box((cx_ - 0.55, cy_ - 0.5, 1.1), (cx_ + 0.55, cy_ + 0.5, 1.22), cl)
    for (ax, ay) in ((-0.5, -0.45), (0.42, -0.45), (-0.5, 0.37), (0.42, 0.37)): mb.box((cx_ + ax, cy_ + ay, 0), (cx_ + ax + 0.08, cy_ + ay + 0.08, 1.1), cc)
    for ax in (-0.55, 0.45): mb.box((cx_ + ax, cy_ - 0.5, 1.22), (cx_ + ax + 0.1, cy_ - 0.4, 2.45), cc)
    mb.box((cx_ - 0.6, cy_ - 0.52, 2.3), (cx_ + 0.6, cy_ - 0.38, 2.62), cl)
    for j in range(4): mb.box((cx_ - 0.33 + j * 0.2, cy_ - 0.48, 1.22), (cx_ - 0.27 + j * 0.2, cy_ - 0.42, 2.3), cl)
    mb.obj('chair', SET, hull=hull(2.6))

    # ---- red track on the map (real geometry) + key light
    _build_track(SET, C)
    if max(P['key']) > 0:
        k = max(P['key']); d = bpy.data.lights.new('key_sun', 'SUN'); d.color = tuple(x / k for x in P['key']); d.energy = math.pi * k
        d.angle = math.radians(P['sun_angle'])
        sun = bpy.data.objects.new('key_sun', d); LIGHTS.objects.link(sun)
        sun.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler()      # a sun shines along its local -Z
        sun.location = (XW + 3, -5, 6); STATE['sun'] = sun
    setup_grade(scene)
    set_track(0.0, 0.0)
    for ob in SET.objects: no_bounce(ob)
    A = anchors(); A['lamps'] = lamps; STATE['A'] = A
    return A

def no_bounce(ob):
    """Hide an object from diffuse / glossy / transmission bounce rays. Cycles always traces one last bounce ray that can only
    pick up emission (the ambient of every surface here is emission), which adds grain, fireflies from the bulbs and an
    uncontrolled fill. With every object hidden from those rays the frame is exactly ambient + one hard key. Call it on actor cards too."""
    ob.visible_diffuse = False; ob.visible_glossy = False; ob.visible_transmission = False; ob.visible_volume_scatter = False
    return ob

# ----------------------------------------------------------------------------- the red track
# Straightened (shot plan, build step 0): the script says the line is ruler-straight ("ตรงเป๊ะ"), so the track is ONE ruled
# segment from the storm symbol off Florida to the N.Y. dot.  The two ends are the v2 ends (O.TRACK[0], O.TRACK[-1]), which the
# printed map texture draws the storm symbol and the N.Y. dot at, so the texture is unchanged.  This point list is THE track of
# v3: track_point(u), map_track, map_storm, map_ny and the geometry all come from it (v2's curved O.TRACK is no longer used here).
TRACK_N = 85                                               # points in map_track (as before; evenly spaced, collinear)
TRACK_ENDS = (tuple(O.TRACK[0]), tuple(O.TRACK[-1]))       # map-plane (x, y-down) of the storm symbol and of N.Y.
TRACK = [(round(TRACK_ENDS[0][0] + (TRACK_ENDS[1][0] - TRACK_ENDS[0][0]) * i / (TRACK_N - 1), 6),
          round(TRACK_ENDS[0][1] + (TRACK_ENDS[1][1] - TRACK_ENDS[0][1]) * i / (TRACK_N - 1), 6)) for i in range(TRACK_N)]
TRACK_HEADING = math.degrees(math.atan2(TRACK_ENDS[1][1] - TRACK_ENDS[0][1], TRACK_ENDS[1][0] - TRACK_ENDS[0][0]))   # map-plane degrees
TRACK_R = 0.012            # half width of the ruled pencil line: 0.024 D wide (was 0.038 D, which read as a marker stroke in the insert)
SMUDGE_R = 0.040           # half width of the eraser smudge (an eraser is wider than the line it rubs out; was 0.049)
ARROW_L, ARROW_DEG = 0.115, 152.0      # arrow-head barbs at N.Y.: length (D) and angle from the heading (clear of the printed N.Y. label)

def _track_uv(u):
    """map-plane (x, y-down, heading_deg) at fraction u of the straight track."""
    u = max(0.0, min(1.0, float(u))); (x0, y0), (x1, y1) = TRACK_ENDS
    return (x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, TRACK_HEADING)
def _poly_curve(name, splines, radius, mat, coll, y):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'
    for pts in splines:
        sp = cu.splines.new('POLY'); sp.points.add(len(pts) - 1)
        for p, (x, z) in zip(sp.points, pts): p.co = (x, 0.0, z, 1.0)
    cu.bevel_mode = 'ROUND'; cu.bevel_depth = radius; cu.bevel_resolution = 1; cu.use_fill_caps = False     # no caps: a zero-length piece renders nothing
    cu.bevel_factor_mapping_start = 'SPLINE'; cu.bevel_factor_mapping_end = 'SPLINE'
    cu.materials.append(mat)
    ob = bpy.data.objects.new(name, cu); coll.objects.link(ob); ob.location = (0, y, 0); ob.scale = (1, 0.0015 / radius, 1)   # flattened: 1.5 mm proud
    ob.visible_shadow = False; STATE.setdefault('objects', {})[name] = ob
    return ob

def _build_track(coll, C):
    pts = [(x, -y) for (x, y) in TRACK_ENDS]                # one ruled segment: two points, dead straight
    P = STATE['P']; pre = STATE['preset'] + '_'
    red = C(O.RED, 0.55); pink = mat_lit(pre + 'smudge', '#f0a694', gain=0.4, opacity=0.26); ghost = mat_lit(pre + 'ghost', '#e58d7c', gain=0.4, opacity=0.3)
    _poly_curve('track_red', [pts], TRACK_R, red, coll, MAP_Y - 0.0006)
    _poly_curve('track_smudge', [pts], SMUDGE_R, pink, coll, MAP_Y - 0.0003)
    x, y, h = _track_uv(1.0); L = ARROW_L; arr = []
    for da in (ARROW_DEG, -ARROW_DEG):
        a = math.radians(h + da); arr.append([(x, -y), (x + L * math.cos(a), -(y + L * math.sin(a)))])
    _poly_curve('track_arrow', arr, TRACK_R, red, coll, MAP_Y - 0.0008)
    _poly_curve('track_arrow_ghost', arr, TRACK_R * 1.8, ghost, coll, MAP_Y - 0.0004)
    _track_drivers(coll)

TRACK_EXPR = dict(                       # simple driver expressions (no Python needed at render time) of the two controls
    track_red=('0', 'line*(1-erase)'),
    track_smudge=('line*(1-erase)', 'line*(1-erase) + line*erase*min(1, erase*1000000)'),
    track_arrow=('0', 'clamp((line-0.97)/0.03) * max(0, 1-erase/0.06)'),
    track_arrow_ghost=('0', 'clamp((line-0.97)/0.03) * min(1, erase*1000000)'))

def _track_drivers(coll):
    """One control object 'track_ctl' with custom properties line and erase; the four curves follow it through drivers."""
    ctl = bpy.data.objects.new('track_ctl', None); coll.objects.link(ctl); ctl['line'] = 0.0; ctl['erase'] = 0.0; ctl.hide_render = True
    STATE['objects']['track_ctl'] = ctl
    for name, (e0, e1) in TRACK_EXPR.items():
        cu = STATE['objects'][name].data
        for path, expr in (('bevel_factor_start', e0), ('bevel_factor_end', e1)):
            fc = cu.driver_add(path); d = fc.driver; d.type = 'SCRIPTED'
            for vn in ('line', 'erase'):
                v = d.variables.new(); v.name = vn; v.type = 'SINGLE_PROP'; v.targets[0].id = ctl; v.targets[0].data_path = '["%s"]' % vn
            d.expression = expr
    return ctl

def set_track(line, erase, frame=None):
    """Red hurricane track: line 0..1 grows it from the storm symbol to New York (the arrow head grows over the last 3 percent);
    erase 0..1 rubs it out from the New York end and leaves a faint pink smudge (the arrow head goes first, a pink ghost stays).
    With frame=N both controls are keyframed at frame N (linear between keys), so two or three keys animate a whole stroke."""
    ln = max(0.0, min(1.0, float(line))); er = max(0.0, min(1.0, float(erase))); ctl = STATE['objects']['track_ctl']
    ctl['line'] = ln; ctl['erase'] = er
    if frame is not None:
        ctl.keyframe_insert('["line"]', frame=frame); ctl.keyframe_insert('["erase"]', frame=frame)
        for fc in _fcurves(ctl):
            for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    keep = ln * (1.0 - er); ah = max(0.0, min(1.0, (ln - 0.97) / 0.03))       # also write the values directly, so the state is right before the next depsgraph update
    vals = dict(track_red=(0.0, keep), track_smudge=(keep, ln) if er > 0 else (keep, keep), track_arrow=(0.0, ah * max(0.0, 1.0 - er / 0.06)), track_arrow_ghost=(0.0, ah if er > 0 else 0.0))
    for name, (a, b) in vals.items():
        cu = STATE['objects'][name].data; cu.bevel_factor_start = a; cu.bevel_factor_end = max(a, b)
    ctl.update_tag(); STATE['track'] = (ln, er)

def get_track():
    """(line, erase) as last set."""
    return STATE.get('track', (0.0, 0.0))

def _fcurves(idblock):
    ad = idblock.animation_data; out = []
    if not ad or not ad.action: return out
    for layer in ad.action.layers:
        for strip in layer.strips:
            cb = strip.channelbag(ad.action_slot)
            if cb: out += list(cb.fcurves)
    return out

_ALPHA = {}
def _card_alpha(ob, loc, face_index, dg):
    """Alpha of a textured card at a world hit point (first Image Texture of its first material); 1.0 if it has none."""
    import numpy as np
    mats = [sl.material for sl in ob.material_slots if sl.material]
    img = None
    for m in mats:
        for n in (m.node_tree.nodes if m.node_tree else []):
            if n.bl_idname == 'ShaderNodeTexImage' and n.image and n.outputs['Alpha'].is_linked: img = n.image; break
        if img: break
    if img is None: return 1.0
    key = img.filepath or img.name
    if key not in _ALPHA:
        w, h = img.size; a = np.empty(w * h * 4, dtype=np.float32); img.pixels.foreach_get(a); _ALPHA[key] = a.reshape(h, w, 4)[:, :, 3].copy()
    A = _ALPHA[key]; me = ob.evaluated_get(dg).data; poly = me.polygons[face_index]; uvl = me.uv_layers.active.data
    from mathutils.interpolate import poly_3d_calc
    co = [ob.matrix_world @ me.vertices[v].co for v in poly.vertices]; wts = poly_3d_calc(co, loc)
    u = sum(w_ * uvl[li].uv.x for w_, li in zip(wts, poly.loop_indices)); v = sum(w_ * uvl[li].uv.y for w_, li in zip(wts, poly.loop_indices))
    if not (0.0 <= u <= 1.0 and 0.0 <= v <= 1.0): return 0.0
    return float(A[min(A.shape[0] - 1, int(v * A.shape[0])), min(A.shape[1] - 1, int(u * A.shape[1]))])

def sun_blocker(point, offset=0.004):
    """Name of the object that shadows a world point from the key light, or None if the key reaches it
    (ray cast toward the sun; alpha cut-outs of cards are respected; the 0.7 degree penumbra is ignored)."""
    scene = bpy.context.scene; dg = bpy.context.evaluated_depsgraph_get(); kd = Vector(STATE['P']['key_dir']).normalized(); d = -kd
    o = Vector(point) + d * offset
    for _ in range(24):
        hit, loc, nrm, fi, ob, mw = scene.ray_cast(dg, o, d, distance=60.0)
        if not hit: return None
        src = ob.original
        if src.name == 'sky' or src.name.startswith('track_') or not src.visible_shadow or src.hide_render: o = loc + d * 1e-4; continue
        if _card_alpha(src, loc, fi, dg) < 0.5: o = loc + d * 1e-4; continue
        return src.name
    return None

def sun_visible(point): return sun_blocker(point) is None

def track_shadow_report(n=41):
    """Which parts of the red track and of the N.Y. label are in cast shadow with the actors currently in the scene.
    Returns dict(track_shadowed=[(u, blocker), ...], label_shadowed=fraction, label_blockers=[...], ok=bool)."""
    bad = []
    for i in range(n):
        u = i / (n - 1); b = sun_blocker(track_point(u))
        if b: bad.append((round(u, 3), b))
    R = STATE['A']['ny_label_rect']; pts = [(R['x0'] + (R['x1'] - R['x0']) * i / 6, MAP_Y - 0.001, R['z0'] + (R['z1'] - R['z0']) * j / 2) for i in range(7) for j in range(3)]
    lb = [sun_blocker(p) for p in pts]; lab = sum(1 for x in lb if x) / len(pts)
    return dict(track_shadowed=bad, label_shadowed=round(lab, 3), label_blockers=sorted(set(x for x in lb if x)), ok=(not bad and lab == 0))

def line_up(target, cam_loc, plane_y):
    """Where the sight line from a camera to a world point crosses the vertical plane y = plane_y.
    Use it to put a hand or pencil tip (which lives on the actor card, 0.37 D in front of the map) exactly over a map point
    as seen from that camera: tip = line_up(track_point(u), cam.location, card_y)."""
    c = Vector(cam_loc); t = Vector(target); k = (plane_y - c.y) / (t.y - c.y); return tuple(c + (t - c) * k)

def track_point(u):
    """World point on the map surface at fraction u of the track (0 = storm symbol, 1 = New York)."""
    x, y, h = _track_uv(u); return (x, MAP_Y - 0.0015, -y)

def anchors():
    P = STATE['P']; kd = Vector(P['key_dir']).normalized()
    y_track = MAP_Y - 0.0015
    track = [(x, y_track, -y) for (x, y) in TRACK]
    cams = dict(
        insert_rake=dict(loc=(-1.05, -0.62, 2.05), look_at=(0.55, -0.05, 2.28), lens=22),
        low_medium=dict(loc=(-0.95, -3.45, 1.2), look_at=(-0.45, -0.3, 2.02), lens=22),
        eye_two_shot=dict(loc=(1.45, -6.2, 2.55), look_at=(1.3, -0.5, 2.3), lens=22),
        high_two_shot=dict(loc=(1.8, -5.9, 3.7), look_at=(1.35, -0.6, 1.55), lens=22),
        wide_high=dict(loc=(-1.9, -8.6, 4.4), look_at=(0.7, -1.2, 0.7), lens=22),
        desk_fg=dict(loc=(-1.6, -5.8, 2.25), look_at=(-0.55, -0.3, 2.15), lens=22),
        top_down=dict(loc=(0.9, -1.45, 4.8), look_at=(0.9, -0.95, 0.0), up=(0, 1, 0), lens=22),
        window_side=dict(loc=(-3.2, -2.6, 2.1), look_at=(1.2, -0.9, 2.0), lens=22),
        low_rake=dict(loc=(2.35, -2.5, 0.9), look_at=(-0.25, -0.15, 2.2), lens=22),
        high_steep=dict(loc=(2.1, -4.6, 4.75), look_at=(1.3, -0.9, 1.2), lens=22),
    )
    return dict(
        map_center=(0.0, MAP_Y, 2.5), map_normal=(0.0, -1.0, 0.0), map_size=(MAP_IN[2] - MAP_IN[0], MAP_IN[3] - MAP_IN[1]),
        map_rect=dict(x0=MAP_IN[0], z0=MAP_IN[1], x1=MAP_IN[2], z1=MAP_IN[3], y=MAP_Y), map_frame_rect=dict(x0=MAP_OUT[0], z0=MAP_OUT[1], x1=MAP_OUT[2], z1=MAP_OUT[3], y=MAP_Y - 0.06),
        map_track=track, map_ny=track[-1], map_storm=track[0], ny_label_rect=dict(x0=0.147, x1=0.40, z0=2.50, z1=2.60),
        track_heading_deg=round(math.degrees(math.atan2(track[0][0] - track[-1][0], track[-1][2] - track[0][2])), 3),   # degrees the line leans west (toward -x) of straight up on the wall
        track_width=2 * TRACK_R, track_length=round(math.dist(track[0], track[-1]), 5),
        # re-exported for the plan's props (build step 0): rectangles in world units, each lying in a plane of constant y facing -y
        calendar_rect=dict(x0=-2.14, x1=-1.54, z0=3.71, z1=4.53, y=-0.048, wall='map', note='printed calendar leaf (card calendar_face) on its block x -2.12..-1.56, z 3.72..4.50, block front y -0.045'),
        label_rect=dict(x0=-0.45, x1=0.70, z0=3.10, z1=3.44, y=MAP_Y - 0.004, pin=(0.125, MAP_Y - 0.012, 3.40), wall='map',
                        note='nickname label (cream strip 1.15 x 0.34 D), pinned on the map above the arrow head; not built yet (build step 4)'),
        teletype_sheet=dict(x0=2.90, x1=3.44, z0=1.88, z1=2.36, y=-0.70, normal=(0.0, -1.0, 0.0), feed_top=(3.17, -0.685, 2.36),
                            note='front face of the paper sheet standing in the teletype (object teletype), normal -y'),
        hero_mark=HERO_MARK, boss_mark=BOSS_MARK, near_mark=NEAR_MARK, wall_gap=round(MAP_Y - HERO_MARK[1], 4),
        ledge=dict(z=MAP_OUT[1] - 0.005, y0=-0.19, y1=0.0, x0=MAP_OUT[0] - 0.09, x1=MAP_OUT[2] + 0.09), eraser_on_ledge=(0.805, -0.10, MAP_OUT[1] + 0.05), red_pencil_on_ledge=(-0.68, -0.105, MAP_OUT[1] + 0.03),
        desk_top=dict(x0=-3.49, x1=-1.41, y0=-5.04, y1=-3.71, z=1.45), banker_lamp=(-1.95, -4.05, 1.93),
        key_dir=tuple(kd), key_screen_side='right',
        key_note='the sun is at screen-right, low and behind the camera for cameras that face the map wall: cast shadows fall to screen-LEFT and away, onto the floor and up the map wall',
        room=dict(x_left=-XW, x_right=XW, y_map_wall=0.0, y_back=-YD, ceiling=H, floor=0.0,
                  window=dict(wall='right', x=XW, y0=WIN['y0'], y1=WIN['y1'], z0=WIN['z0'], z1=WIN['z1'], bars_y=WIN['bars'], transom_z=WIN['transom']),
                  wainscot_top=Z_CHAIR, picture_rail=Z_PRAIL0, rug=dict(x0=-1.2, x1=1.2, y0=-YD, y1=-0.62)),
        cams=cams, cam_notes=dict(
            insert_rake='0.7 D from the map, raking 20 degrees to its surface: the sheet recedes to a vanishing point, track in the middle',
            low_medium='1.2 D above the floor, pitched up 14 degrees at the hero mark (head about 250 px)',
            eye_two_shot='eye level 2.55 D; hero at the wall, near_mark actor 1.36 x larger at screen right',
            high_two_shot='3.7 D high, pitched down 22 degrees; floor patch and long shadows, almost no ceiling in frame',
            wide_high='4.4 D high in the back-left corner, pitched down 25 degrees; whole room, window wall at right, desk in the foreground',
            low_rake='0.9 D above the floor by the window side, pitched up 20 degrees, raking along the map wall: boss_mark near, hero_mark far, the track stays visible',
            high_steep='4.75 D high, pitched down 43 degrees: the floor fills the frame, a pendant lamp hangs into the top left',
            desk_fg='over the foreground desk past the banker lamp toward the map',
            top_down='4.8 D above the marks looking straight down (6 degrees toward the wall); uses the up key',
            window_side='from the left wall across the marks toward the window wall and the sky'),
        render=dict(samples=16, resolution=(720, 1280), sun_angle_deg=P['sun_angle'], shade=P['shade'], key=P['key'], lift=P.get('lift', (0, 0, 0)),
                    form=P.get('form', (0, 0, 0)), falloff_y=P.get('falloff_y', 0.0), bloom_size=P.get('bloom_size', 0.05)))

# ----------------------------------------------------------------------------- cameras
def make_camera(setup, name='cam', scene=None):
    """Create (or reuse) a 22 mm camera from a {loc, look_at, lens} setup and make it the scene camera."""
    scene = scene or bpy.context.scene
    ob = bpy.data.objects.get(name)
    if ob is None:
        cd = bpy.data.cameras.new(name); ob = bpy.data.objects.new(name, cd); scene.collection.objects.link(ob)
    cd = ob.data; cd.lens = setup.get('lens', 22); cd.sensor_width = 36; cd.sensor_fit = 'AUTO'; cd.clip_start = 0.05; cd.clip_end = 200
    ob.location = setup['loc']; fwd = (Vector(setup['look_at']) - Vector(setup['loc'])).normalized()
    if 'up' in setup:                                      # explicit up vector (needed for top-down views)
        right = fwd.cross(Vector(setup['up'])).normalized(); up = right.cross(fwd)
        ob.rotation_euler = Matrix((right, up, -fwd)).transposed().to_euler()
    else: ob.rotation_euler = fwd.to_track_quat('-Z', 'Y').to_euler()
    if setup.get('roll'): ob.rotation_euler.rotate_axis('Z', math.radians(setup['roll']))
    scene.camera = ob
    return ob

# ----------------------------------------------------------------------------- placeholder actors (for stills, timing and the spike only)
def placeholder_actor(cast, story_key, mark, face_to=None, name=None, ppd=300, pose=None):
    """Rasterise a v2 puppet pose to a transparent PNG and stand it on a card at `mark`. Not part of the set API."""
    sys.path.insert(0, os.path.join(PROJ, 'v2', 'puppet'))
    import puppet
    name = name or ('actor_' + cast); pose = dict(pose) if pose else dict(puppet.STORY[story_key][1]); f = puppet.figure(cast, pose, name)
    bx0, by0, bx1, by1 = f['bbox']; pad = 0.08; bx0 -= pad; by0 -= pad; bx1 += pad; by1 = max(by1, f['feet_y']) + pad
    w, h = bx1 - bx0, by1 - by0; Wp, Hp = int(round(w * ppd)), int(round(h * ppd))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wp}" height="{Hp}" viewBox="{bx0:.4f} {by0:.4f} {w:.4f} {h:.4f}" style="display:block">{f["svg"]}</svg>')
    import hashlib
    os.makedirs(TMP, exist_ok=True); tag = name + '_' + story_key + '_' + hashlib.sha1(svg.encode()).hexdigest()[:8]
    sp = os.path.join(TMP, tag + '.svg'); pp = os.path.join(TMP, tag + '.png')
    if not os.path.exists(pp):                              # cached: Chromium is only started for a new drawing
        open(sp, 'w').write(svg); jp = os.path.join(TMP, tag + '_job.json'); json.dump([dict(src=sp, out=pp, w=Wp, h=Hp, transparent=True)], open(jp, 'w'))
        for attempt in range(3):
            r = subprocess.run(['node', os.path.join(HERE, 'raster.js'), jp], capture_output=True, env=dict(os.environ, NODE_PATH=os.environ.get('NODE_PATH', '/opt/node22/lib/node_modules')))
            if r.returncode == 0 and os.path.exists(pp): break
            time.sleep(1.0)
        else: raise RuntimeError('placeholder raster failed: ' + r.stderr.decode()[-500:])
    fx = f['anchors']['feet'][0]; fy = f['feet_y']
    me = bpy.data.meshes.new(name); xs = (bx0 - fx, bx1 - fx); zs = (fy - by1, fy - by0)
    me.from_pydata([(xs[0], 0, zs[0]), (xs[1], 0, zs[0]), (xs[1], 0, zs[1]), (xs[0], 0, zs[1])], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    me.materials.append(mat_card(name + '_mat', pp))
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); ob.location = mark; no_bounce(ob)
    if face_to is not None:
        d = Vector(face_to) - Vector(mark); ob.rotation_euler = (0, 0, math.atan2(d.x, -d.y))
    return ob

def render(path, scene=None):
    scene = scene or bpy.context.scene; scene.render.filepath = path
    t0 = time.time(); c0 = time.process_time(); bpy.ops.render.render(write_still=True)
    return time.time() - t0, time.process_time() - c0

def _load():
    return ' '.join('%.2f' % v for v in os.getloadavg())

# ----------------------------------------------------------------------------- CLI
def _clear_actors(scene):
    for o in list(scene.objects):
        if o.name.startswith('actor_'): bpy.data.objects.remove(o, do_unlink=True)

def stage_placeholders(A, staging='two_shot', cam_loc=None):
    """Two placeholder cards. 'wall': hero and boss at their wall marks. 'two_shot': hero at the wall, boss at near_mark."""
    _clear_actors(bpy.context.scene)
    h = placeholder_actor('hero', 'hero_draw', A['hero_mark'])
    if staging == 'hero': return h, None
    if staging == 'wall': b = placeholder_actor('boss', 'boss_rub', A['boss_mark'])
    else: b = placeholder_actor('boss', 'boss_near', A['near_mark'], face_to=cam_loc, pose=dict(yaw=-0.45, head_roll=-4, expr='smug', arm_l='down', arm_r='hip', legs='stand'))
    return h, b

def cli_spike(quality='final'):
    A = build(); scene = bpy.context.scene; setup_render(scene, quality); os.makedirs(OUT, exist_ok=True); set_track(1.0, 0.0)
    shots = dict(spike_low=('wall', A['cams']['low_medium']), spike_eye=('two_shot', A['cams']['eye_two_shot']), spike_high=('two_shot', A['cams']['high_two_shot']))
    for nm, (stg, cs) in shots.items():
        make_camera(cs); stage_placeholders(A, stg, cs['loc'])
        w, c = render(os.path.join(OUT, nm + '.png')); print('%s: %.1f s wall, %.1f s cpu, load %s' % (nm, w, c, _load()))

def cli_stills(quality='final', actors=False, only=None, outdir=None):
    A = build(); scene = bpy.context.scene; setup_render(scene, quality); set_track(1.0, 0.0); outdir = outdir or HERE
    for nm, cs in A['cams'].items():
        if only and nm not in only: continue
        make_camera(cs)
        if actors: stage_placeholders(A, 'wall' if nm in ('low_medium', 'insert_rake', 'top_down', 'window_side', 'low_rake') else 'two_shot', cs['loc'])
        if nm == 'insert_rake': _clear_actors(scene)
        w, c = render(os.path.join(outdir, ('staged_' if actors else 'still_') + nm + '.png')); print('%s: %.1f s wall, %.1f s cpu, load %s' % (nm, w, c, _load()))

def cli_timing(n=4):
    A = build(); scene = bpy.context.scene; setup_render(scene, 'final'); set_track(1.0, 0.0)
    cs = A['cams']['eye_two_shot']; cam = make_camera(cs); stage_placeholders(A, 'two_shot', cs['loc'])
    print('final quality: 720x1280, %d samples, threads %d, denoise %s, adaptive %s; load before: %s' % (scene.cycles.samples, scene.render.threads, scene.cycles.use_denoising, scene.cycles.use_adaptive_sampling, _load()))
    res = []
    for i in range(n):
        cam.location.x += 0.02                             # a moving camera, as in a real shot
        w, c = render(os.path.join(TMP, 'timing_%d.png' % i)); res.append((w, c)); print('frame %d: %.2f s wall, %.2f s cpu, load %s' % (i, w, c, _load()))
    ws = sorted(r[0] for r in res[1:]); cs_ = sorted(r[1] for r in res[1:])
    print('TIMING first frame %.2f s wall; following frames median %.2f s wall, %.2f s cpu' % (res[0][0], ws[len(ws) // 2], cs_[len(cs_) // 2]))

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stills'; arg = sys.argv[2:]
    if cmd == 'spike': cli_spike(arg[0] if arg else 'final')
    elif cmd == 'stills': cli_stills(arg[0] if arg else 'final')
    elif cmd == 'staged': cli_stills(arg[0] if arg else 'final', actors=True, outdir=arg[1] if len(arg) > 1 else TMP)
    elif cmd == 'timing': cli_timing()
    else: print(__doc__)

#!/usr/bin/env python3
"""joseon.py : set of film 24 ("ไอ้เรือเต่า": Admiral Yi Sun-sin's turtle ship, Joseon Korea 1592) as a real 3D Blender set, PATH-TRACED
(bpy 5.x, Cycles CPU, GI, Principled materials, thin volumetric haze, DOF allowed), after the client's R9 look (qtest/r9_scene.py).
Characters are 2D puppet cards (emission to camera, unlit, they cast shadows); everything else is lit by one soft warm sun + a gradient sky.

    import joseon as J
    A = J.build('yard', 'roof_low')      # yard: roof_low | bow | yard_wide | roof_top | macro_spikes | macro_dragon
    A = J.build('sea', 'fleet_wide')     # sea : fleet_wide flag_deck flag_deck_b flag_deck_crew hansan_high flag_bow chase board reveal_top aftermath shore macro_oar
    cam = J.make_camera(A['cam']); J.set_spikes(2, frame=10); J.set_ports(1); J.set_fleet_chase(s); J.set_korean_turn(k) ...
World: 1 unit = 1 D (head), Z up. See API.md.   CLI: python3 joseon.py final|stills [spec ...]   (render 75 % + post upscale)"""
import os, sys, math, json, time, random, subprocess
import numpy as np
import bpy
from mathutils import Vector, Matrix, Quaternion

HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (HERE, os.path.join(PROJ, 'v3', 'set3d9'), os.path.join(PROJ, 'v3', 'set3d8'), os.path.join(PROJ, 'v3', 'set3d2'), os.path.join(PROJ, 'v3', 'set3d4'),
          os.path.join(PROJ, 'v3', 'set3d5'), os.path.join(PROJ, 'v3', 'set3d6'), os.path.join(PROJ, 'v3', 'set3d7'), os.path.join(PROJ, 'v3', 'set3d10')):
    if p not in sys.path: sys.path.insert(0, p)
import tower as T                                          # noqa: E402  (MB mesh builder, placeholder_actor cards, keys)
import joseon_tex as JX                                    # noqa: E402
MB = T.MB; hexl = T.hex_lin
WORK = os.path.join(HERE, 'joseon_work')
S = {}                                                      # scene state (reset by build)
FPS = 30
CHASE_V = 3.0                                               # Japanese fleet speed, D / s (hook set_fleet_chase(s) moves them +x by CHASE_V * s)
def rnd(seed): return random.Random(seed)
def V(*a): return Vector(a)

# ============================================================================= node helpers
class NB:
    def __init__(s, m):
        s.m = m; m.use_nodes = True; s.nt = m.node_tree
        for n in list(s.nt.nodes):
            if n.type != 'OUTPUT_MATERIAL': s.nt.nodes.remove(n)
        s.out = [n for n in s.nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]
    def n(s, kind, **kw):
        nd = s.nt.nodes.new(kind)
        for k, v in kw.items(): setattr(nd, k, v)
        return nd
    def l(s, a, b): s.nt.links.new(a, b)
    def put(s, sock, v):
        if isinstance(v, bpy.types.NodeSocket): s.l(v, sock)
        else: sock.default_value = (*v, 1.0) if isinstance(v, (tuple, list)) and len(v) == 3 and sock.type == 'RGBA' else v
    def math(s, op, a, b=0.0, clamp=False):
        n = s.n('ShaderNodeMath', operation=op, use_clamp=clamp); s.put(n.inputs[0], a); s.put(n.inputs[1], b); return n.outputs[0]
    def rng(s, v, a, b, c=0.0, d=1.0, clamp=True, smooth=False):
        n = s.n('ShaderNodeMapRange', interpolation_type='SMOOTHSTEP' if smooth else 'LINEAR', clamp=clamp); s.put(n.inputs['Value'], v)
        for k, x in (('From Min', a), ('From Max', b), ('To Min', c), ('To Max', d)): n.inputs[k].default_value = x
        return n.outputs['Result']
    def mix(s, fac, a, b):
        n = s.n('ShaderNodeMix', data_type='RGBA'); s.put(n.inputs[0], fac); s.put(n.inputs[6], a); s.put(n.inputs[7], b); return n.outputs[2]
    def mul(s, a, b):
        n = s.n('ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); n.inputs[0].default_value = 1.0; s.put(n.inputs[6], a); s.put(n.inputs[7], b); return n.outputs[2]
    def coord(s, k='Object'): return s.n('ShaderNodeTexCoord').outputs[k]
    def noise(s, scale, detail=3.0, rough=0.55, vec=None, mapscale=None):
        n = s.n('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = scale; n.inputs['Detail'].default_value = detail; n.inputs['Roughness'].default_value = rough
        v = vec if vec is not None else s.coord()
        if mapscale: mp = s.n('ShaderNodeMapping'); mp.inputs['Scale'].default_value = mapscale; s.l(v, mp.inputs['Vector']); v = mp.outputs[0]
        s.l(v, n.inputs['Vector']); return n.outputs['Fac']
    def bump(s, h, strength, dist=0.1):
        b = s.n('ShaderNodeBump'); s.put(b.inputs['Strength'], strength); b.inputs['Distance'].default_value = dist; s.l(h, b.inputs['Height']); return b.outputs['Normal']
    def princ(s, col, rough=0.6, metal=0.0, normal=None, **kw):
        p = s.n('ShaderNodeBsdfPrincipled'); s.put(p.inputs['Base Color'], col if isinstance(col, bpy.types.NodeSocket) else (*col, 1.0)); s.put(p.inputs['Roughness'], rough)
        p.inputs['Metallic'].default_value = metal
        if normal is not None: s.l(normal, p.inputs['Normal'])
        for k, v in kw.items(): s.put(p.inputs[k], v)
        s.l(p.outputs[0], s.out.inputs['Surface']); return p
    def img(s, key, scale=1.0, proj='BOX', vec=None, cs='sRGB', ext='REPEAT'):
        t = s.n('ShaderNodeTexImage'); t.image = bpy.data.images.load(S['tx'][key], check_existing=True); t.image.colorspace_settings.name = cs
        t.projection = proj; t.extension = ext
        if proj == 'BOX': t.projection_blend = 0.25
        v = vec if vec is not None else s.coord()
        mp = s.n('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (scale, scale, scale); s.l(v, mp.inputs['Vector']); s.l(mp.outputs[0], t.inputs['Vector']); return t

def mat(name, build=None):
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); b = NB(m)
    if build: build(b)
    return m

def flat(name, hexcol, rough=0.7, metal=0.0, **kw):
    """Plain principled colour (hex sRGB)."""
    def f(b): b.princ(hexl(hexcol), rough, metal, **kw)
    return mat('J_' + name, f)

def tint(h, k): c = hexl(h); return tuple(min(1.0, x * k) for x in c)

def wood(name, base='#976c4d', dark='#6a4630', scale=1.25, axis='Z', rough=0.72, waterline=False, bumpk=0.35):
    """Plank wood by object-space nodes: seams between boards (wave bands along `axis`), stretched grain noise, bump, optional dark wet waterline."""
    def f(b):
        c = b.coord(); w = b.n('ShaderNodeTexWave', wave_type='BANDS', bands_direction=axis, wave_profile='SAW'); w.inputs['Scale'].default_value = scale
        w.inputs['Distortion'].default_value = 0.5; w.inputs['Detail'].default_value = 1.0; b.l(c, w.inputs['Vector'])
        ms = (0.4, 9.0, 9.0) if axis == 'Z' else (9.0, 0.4, 9.0) if axis == 'Y' else (9.0, 9.0, 0.4)
        gr = b.noise(2.5, 3.0, 0.6, c, ms); seam = b.rng(w.outputs['Fac'], 0.0, 0.07, 0.0, 1.0)
        col = b.mix(b.rng(gr, 0.3, 0.7), hexl(base), hexl(dark)); col = b.mix(seam, tint(dark, 0.45) + (1.0,), col)
        if waterline:
            z = b.n('ShaderNodeSeparateXYZ'); b.l(c, z.inputs[0]); wl = b.rng(z.outputs['Z'], 0.05, 0.45); col = b.mix(wl, hexl('#4a2a20'), col)
        nrm = b.bump(b.math('ADD', gr, b.math('MULTIPLY', seam, 0.8)), bumpk, 0.08)
        b.princ(col, rough, 0.0, nrm)
    return mat('J_w_%s' % name, f)

def imgmat(name, key, scale=0.25, proj='BOX', rough=0.8, metal=0.0, bumpk=0.25, tintc=None, uv=False):
    def f(b):
        t = b.img(key, scale, 'FLAT' if uv else proj, vec=None if not uv else b.n('ShaderNodeUVMap').outputs[0])
        if uv:                                              # UV mapped: undo the mapping node scale so UV 0..1 is the tile
            pass
        col = t.outputs['Color']
        if tintc: col = b.mul(col, (*hexl(tintc), 1))
        h = b.n('ShaderNodeRGBToBW'); b.l(t.outputs['Color'], h.inputs[0])
        b.princ(col, rough, metal, b.bump(h.outputs[0], bumpk, 0.05) if bumpk else None)
    return mat('J_i_%s' % name, f)

def emit(name, hexcol, k=8.0):
    def f(b):
        e = b.n('ShaderNodeEmission'); e.inputs['Color'].default_value = (*hexl(hexcol), 1); e.inputs['Strength'].default_value = k; b.l(e.outputs[0], b.out.inputs['Surface'])
    return mat('J_e_' + name, f)

def flagmat(key):
    def f(b):
        t = b.img(key, 1.0, 'FLAT', vec=b.n('ShaderNodeUVMap').outputs[0], ext='CLIP'); mp = [n for n in b.nt.nodes if n.type == 'MAPPING'][0]
        d = b.n('ShaderNodeBsdfDiffuse'); b.l(t.outputs['Color'], d.inputs['Color']); tr = b.n('ShaderNodeBsdfTranslucent'); b.l(t.outputs['Color'], tr.inputs['Color'])
        mx = b.n('ShaderNodeMixShader'); mx.inputs[0].default_value = 0.35; b.l(d.outputs[0], mx.inputs[1]); b.l(tr.outputs[0], mx.inputs[2])
        tp = b.n('ShaderNodeBsdfTransparent'); m2 = b.n('ShaderNodeMixShader'); b.l(t.outputs['Alpha'], m2.inputs[0]); b.l(tp.outputs[0], m2.inputs[1]); b.l(mx.outputs[0], m2.inputs[2])
        b.l(m2.outputs[0], b.out.inputs['Surface'])
    return mat('J_f_' + key, f)

def smoke_mat(name, hexcol, k=1.0):
    """Cartoon smoke billow: matte, slightly translucent-looking soft white-grey with a warm lit side (principled, rough 1)."""
    def f(b): b.princ(hexl(hexcol), 1.0, 0.0, None, **{'Subsurface Weight': 0.15})
    return mat('J_s_' + name, f)

def tx_sync(): S['tx'] = JX.ensure(verbose=False)

# ============================================================================= mesh helpers
def mk(mb, name, parent=None, coll=None, smooth=False, shadow=True, loc=None):
    o = mb.obj(name, coll or S['coll'], smooth=smooth)
    if parent is not None: o.parent = parent
    if loc is not None: o.location = loc
    if not shadow: o.visible_shadow = False
    return o

def empty(name, parent=None, loc=(0, 0, 0), rot=None):
    o = bpy.data.objects.new(name, None); S['coll'].objects.link(o); o.location = loc
    if rot is not None: o.rotation_euler = rot
    if parent is not None: o.parent = parent
    return o

def obox(mb, c, X, Y, Z, hx, hy, hz, m):
    c = Vector(c); X, Y, Z = Vector(X), Vector(Y), Vector(Z); mb.pid += 1
    for (n, a, b, ha, hb, hn) in ((X, Y, Z, hy, hz, hx), (-X, Y, Z, hy, hz, hx), (Y, X, Z, hx, hz, hy), (-Y, X, Z, hx, hz, hy), (Z, X, Y, hx, hy, hz), (-Z, X, Y, hx, hy, hz)):
        o = c + n * hn; pts = [o - a * ha - b * hb, o + a * ha - b * hb, o + a * ha + b * hb, o - a * ha + b * hb]
        mb.oface(pts, m, [(0, 0), (1, 0), (1, 1), (0, 1)], n)

def bx(mb, lo, hi, m): mb.box(lo, hi, m)
def cbox(mb, c, hx, hy, hz, m): mb.box((c[0] - hx, c[1] - hy, c[2] - hz), (c[0] + hx, c[1] + hy, c[2] + hz), m)
def beam(mb, p0, p1, w, h, m, up=(0, 0, 1)):
    p0, p1 = Vector(p0), Vector(p1); X = p1 - p0; Ln = X.length; X.normalize(); Y = Vector(up).cross(X)
    if Y.length < 1e-4: Y = Vector((0, 1, 0)).cross(X)
    Y.normalize(); Z = X.cross(Y); obox(mb, (p0 + p1) / 2, X, Y, Z, Ln / 2, w / 2, h / 2, m)
def rod(mb, p0, p1, r, m, seg=8, r1=None): mb.frustum(p0, p1, r, r if r1 is None else r1, m, seg=seg)
def cone(mb, base, tip, r, m, seg=6): mb.frustum(base, tip, r, 0.0, m, seg=seg, cap1=False)

def ell(mb, c, rx, ry, rz, m, seg=12, rings=8, axes=None):
    """Ellipsoid (optionally rotated: axes = (X, Y, Z) unit vectors)."""
    c = Vector(c); X, Y, Z = axes or (Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))); R = []; mb.pid += 1
    for k in range(rings + 1):
        th = math.pi * k / rings; R.append([c + X * (rx * math.sin(th) * math.cos(2 * math.pi * i / seg)) + Y * (ry * math.sin(th) * math.sin(2 * math.pi * i / seg)) - Z * (rz * math.cos(th)) for i in range(seg)])
    for k in range(rings):
        for i in range(seg):
            j = (i + 1) % seg; mb.face([R[k][i], R[k][j], R[k + 1][j], R[k + 1][i]], m)

def lump(mb, c, r, m, seed, seg=10, rings=6, rough=0.2, squash=1.0):
    rs = rnd(seed); c = Vector(c); R = []; mb.pid += 1
    for k in range(rings + 1):
        th = math.pi * k / rings; row = []
        for i in range(seg):
            ph = 2 * math.pi * i / seg; d = Vector((math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), -math.cos(th) * squash))
            row.append(c + d * r * (1 + rs.uniform(-rough, rough)) if 0 < k < rings else c + d * r)
        if k in (0, rings): row = [row[0]] * seg
        R.append(row)
    for k in range(rings):
        for i in range(seg):
            j = (i + 1) % seg; mb.face([R[k][i], R[k][j], R[k + 1][j], R[k + 1][i]], m)

def torus(mb, c, R, r, m, segs=18, sides=6, tilt=0.0):
    c = Vector(c); pts = []
    for i in range(segs):
        a = 2 * math.pi * i / segs; ctr = Vector((R * math.cos(a), R * math.sin(a), 0)); rad = Vector((math.cos(a), math.sin(a), 0)); ring = []
        for j in range(sides):
            b = 2 * math.pi * j / sides; ring.append(c + ctr + rad * (r * math.cos(b)) + Vector((0, 0, r * math.sin(b))))
        pts.append(ring)
    mb.pid += 1
    for i in range(segs):
        for j in range(sides):
            i2, j2 = (i + 1) % segs, (j + 1) % sides; mb.face([pts[i][j], pts[i2][j], pts[i2][j2], pts[i][j2]], m)

def quad_grid(mb, f, nu, nv, m, uvs=None, orient=None):
    """f(i, j) -> Vector on an (nu+1) x (nv+1) lattice; faces with uv (i/nu, j/nv) unless uvs(i, j) given; orient(centre) -> wanted normal."""
    P = [[f(i, j) for j in range(nv + 1)] for i in range(nu + 1)]; mb.pid += 1
    for i in range(nu):
        for j in range(nv):
            idx = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
            if orient is not None:
                q = [P[a][b] for a, b in idx]; nrm = (q[2] - q[0]).cross(q[3] - q[1]); c = (q[0] + q[1] + q[2] + q[3]) / 4
                if nrm.dot(orient(c)) < 0: idx = idx[::-1]
            mb.face([P[a][b] for a, b in idx], m, [uvs(a, b) if uvs else (a / nu, b / nv) for a, b in idx])
    return P

def key_attr(ob, path, frame, interp='LINEAR', idx=-1):
    ob.keyframe_insert(path, index=idx, frame=frame)
    for fc in T._fcurves(ob):
        if fc.data_path == path and (idx < 0 or fc.array_index == idx):
            for kp in fc.keyframe_points:
                if int(round(kp.co.x)) == int(frame): kp.interpolation = interp

def show(ob, vis, frame=None):
    ob.hide_render = not vis
    if frame is not None: ob.keyframe_insert('hide_render', frame=frame)

def smooth_round(ob, levels=2):
    md = ob.modifiers.new('ss', 'SUBSURF'); md.levels = levels; md.render_levels = levels
    for pg in ob.data.polygons: pg.use_smooth = True

# ============================================================================= scene: world, sun, haze, render settings
SKY = [(0.0, '#f6dcbc'), (0.07, '#cfd2e2'), (0.25, '#86b0ec'), (0.62, '#3a6ccc')]       # peach horizon -> blue zenith (COLOUR_SPEC daytime sky)

def setup_world(sc, sky_k=1.0):
    w = bpy.data.worlds.new('joseon_sky'); sc.world = w; b = NB.__new__(NB); w.use_nodes = True; nt = w.node_tree
    for n in list(nt.nodes):
        if n.type != 'OUTPUT_WORLD': nt.nodes.remove(n)
    def N(kind, **kw):
        nd = nt.nodes.new(kind)
        for k_, v_ in kw.items(): setattr(nd, k_, v_)
        return nd
    L = nt.links.new; o = [n for n in nt.nodes if n.type == 'OUTPUT_WORLD'][0]
    tc = N('ShaderNodeTexCoord'); sep = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Generated'], sep.inputs[0]); ramp = N('ShaderNodeValToRGB'); cr = ramp.color_ramp
    cr.elements[0].position = SKY[0][0]; cr.elements[0].color = (*hexl(SKY[0][1]), 1); cr.elements[1].position = SKY[-1][0]; cr.elements[1].color = (*hexl(SKY[-1][1]), 1)
    for pos, col in SKY[1:-1]: e = cr.elements.new(pos); e.color = (*hexl(col), 1)
    L(sep.outputs['Z'], ramp.inputs[0])
    glow = N('ShaderNodeVectorMath', operation='DOT_PRODUCT'); L(tc.outputs['Generated'], glow.inputs[0]); S['sun_glow'] = glow
    pw = N('ShaderNodeMath', operation='POWER'); pw.inputs[1].default_value = 18.0; mx = N('ShaderNodeMath', operation='MAXIMUM'); mx.inputs[1].default_value = 0.0
    L(glow.outputs['Value'], mx.inputs[0]); L(mx.outputs[0], pw.inputs[0]); sc_ = N('ShaderNodeMath', operation='MULTIPLY'); sc_.inputs[1].default_value = 1.4; L(pw.outputs[0], sc_.inputs[0])
    col = N('ShaderNodeMix', data_type='RGBA'); col.inputs[6].default_value = (0, 0, 0, 1); col.inputs[7].default_value = (3.0, 1.7, 0.8, 1); L(sc_.outputs[0], col.inputs[0])
    ad = N('ShaderNodeMix', data_type='RGBA', blend_type='ADD'); ad.inputs[0].default_value = 1.0; L(ramp.outputs[0], ad.inputs[6]); L(col.outputs[2], ad.inputs[7])
    bg = N('ShaderNodeBackground'); bg.inputs['Strength'].default_value = sky_k; L(ad.outputs[2], bg.inputs['Color']); L(bg.outputs[0], o.inputs['Surface'])

def set_sun(az_deg, elev, energy=None):
    """Sun by azimuth (direction TO the sun, degrees from +x CCW) and elevation. Warm key (1.0, 0.66, 0.40), 1.5 deg disc."""
    sun = S['sun']; e = math.radians(elev); a = math.radians(az_deg); to_sun = Vector((math.cos(a) * math.cos(e), math.sin(a) * math.cos(e), math.sin(e)))
    sun.rotation_euler = (-to_sun).to_track_quat('-Z', 'Y').to_euler(); S['to_sun'] = to_sun; S['sun_glow'].inputs[1].default_value = to_sun
    if energy: sun.data.energy = energy

def sun_for_camera(setup, elev=16.0, left=1.0, behind=0.38):
    """The key comes from the camera's left (and a little behind it)."""
    f = Vector(setup['look_at']) - Vector(setup['loc']); f.z = 0; f.normalize(); lf = Vector((-f.y, f.x, 0)); h = (lf * left - f * behind).normalized()
    return math.degrees(math.atan2(h.y, h.x)), elev

def make_haze(density, center, size):
    m = mat('J_haze', lambda b: None); b = NB(m); v = b.n('ShaderNodeVolumePrincipled'); v.inputs['Density'].default_value = density; v.inputs['Anisotropy'].default_value = 0.5
    v.inputs['Color'].default_value = (*hexl('#e8eef6'), 1); b.l(v.outputs[0], b.out.inputs['Volume']); S['haze_mat'] = m; S['haze_node'] = v
    vs = [(center[0] + sx * size[0], center[1] + sy * size[1], center[2] + sz * size[2]) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
    fs = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    me = bpy.data.meshes.new('haze'); me.from_pydata(vs, [], fs); me.update(); me.materials.append(m); ob = bpy.data.objects.new('haze', me); S['coll'].objects.link(ob)
    ob.visible_shadow = False; ob.visible_glossy = True; return ob

def setup_render(sc, quality='final'):
    """Cycles CPU, path tracing with GI, 24 samples adaptive + OIDN, 75 % resolution (540x960) upscaled to 720x1280 by post(); preview 40 %."""
    r = sc.render; r.engine = 'CYCLES'; r.resolution_x, r.resolution_y = 720, 1280; r.resolution_percentage = 75 if quality == 'final' else 40
    r.image_settings.file_format = 'PNG'; r.use_motion_blur = False; r.fps = FPS
    cy = sc.cycles; cy.device = 'CPU'; cy.samples = int(S.get('samples', 24)) if quality == 'final' else 10; cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.05; cy.adaptive_min_samples = 6
    cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'; cy.max_bounces = 4; cy.diffuse_bounces = 2; cy.glossy_bounces = 2; cy.transmission_bounces = 1
    cy.volume_bounces = 0; cy.transparent_max_bounces = 6; cy.caustics_reflective = False; cy.caustics_refractive = False; cy.blur_glossy = 1.0; cy.volume_step_rate = 3.0
    cy.use_light_tree = True; r.threads_mode = 'FIXED'; r.threads = 2; r.use_persistent_data = True
    sc.view_settings.view_transform = 'AgX'
    try: sc.view_settings.look = 'AgX - Medium High Contrast'
    except TypeError: pass
    sc.view_settings.exposure = float(S.get('exposure', 0.0))

def make_camera(setup, name='cam', scene=None):
    """Camera from {loc, look_at, lens[, fstop, focus (distance or point), up, roll]}. Lens on a 36 mm sensor (film-10 convention). DOF only when fstop is given
    (macro presets); wide shots are sharp. Nothing is ever parented to the camera."""
    scene = scene or bpy.context.scene; ob = bpy.data.objects.get(name)
    if ob is None: cd = bpy.data.cameras.new(name); ob = bpy.data.objects.new(name, cd); scene.collection.objects.link(ob)
    cd = ob.data; cd.lens = setup.get('lens', 22); cd.sensor_width = 36; cd.sensor_fit = 'AUTO'; cd.clip_start = 0.05; cd.clip_end = 9000
    ob.location = setup['loc']; fwd = (Vector(setup['look_at']) - Vector(setup['loc'])).normalized()
    if 'up' in setup:
        right = fwd.cross(Vector(setup['up'])).normalized(); up = right.cross(fwd); ob.rotation_euler = Matrix((right, up, -fwd)).transposed().to_euler()
    else: ob.rotation_euler = fwd.to_track_quat('-Z', 'Y').to_euler()
    if setup.get('roll'): ob.rotation_euler.rotate_axis('Z', math.radians(setup['roll']))
    if setup.get('fstop'):
        cd.dof.use_dof = True; cd.dof.aperture_fstop = setup['fstop']; fp = setup.get('focus', setup['look_at'])
        cd.dof.focus_distance = float(fp) if isinstance(fp, (int, float)) else (Vector(fp) - Vector(setup['loc'])).length; cd.dof.aperture_blades = 7
    else: cd.dof.use_dof = False
    scene.camera = ob; return ob

# ============================================================================= swell (shared by the ocean mesh and the ship / plank drivers)
SWELL = [(0.34, 34.0, 20.0, 0.9), (0.20, 21.0, 75.0, 1.2), (0.11, 13.0, -35.0, 1.6)]       # A, wavelength, direction deg, angular speed
CHOP = [(0.03, 7.3, 52.0, 2.2), (0.02, 4.9, -67.0, 2.8)]
def swell_z(x, y, t):
    z = 0.0
    for A, lam, ang, spd in SWELL: k = 2 * math.pi / lam; z += A * math.sin(k * (x * math.cos(math.radians(ang)) + y * math.sin(math.radians(ang))) - spd * t)
    return z
def swell_expr(xs='x', ys='y', amp=1.0):
    parts = []
    for A, lam, ang, spd in SWELL:
        k = 2 * math.pi / lam; parts.append('%.4f*sin(%.5f*%s+%.5f*%s-%.4f*frame/%d)' % (A * amp, k * math.cos(math.radians(ang)), xs, k * math.sin(math.radians(ang)), ys, spd, FPS))
    return '+'.join(parts)

def drive(ob, path, idx, expr, vars_):
    fc = ob.driver_add(path, idx); d = fc.driver; d.type = 'SCRIPTED'; d.expression = expr
    for nm, (idb, dp) in vars_.items():
        v = d.variables.new(); v.name = nm; v.type = 'SINGLE_PROP'; v.targets[0].id = idb; v.targets[0].data_path = dp

def drive_at(ob, root, c, base=0.0, amp=1.0):
    """Swell-driven height for an object that sits at root-local point c (flat foam / splash on the surface): the swell is evaluated at the WORLD x, y of an empty at c (child of the root)."""
    an = empty('an_' + ob.name, root, tuple(c)); fc = ob.driver_add('location', 2); d = fc.driver; d.type = 'SCRIPTED'; sc_ = root.scale[0]; d.expression = '%.3f+%s' % (base / sc_, swell_expr('x', 'y', amp / sc_))
    for nm, tt in (('x', 'LOC_X'), ('y', 'LOC_Y')):
        v = d.variables.new(); v.name = nm; v.type = 'TRANSFORMS'; t = v.targets[0]; t.id = an; t.transform_type = tt; t.transform_space = 'WORLD_SPACE'

def ride_swell(ob, root, base_z=0.0, amp=1.0, roll=0.0, pitch=0.0, seed=0, extra=''):
    """Heave of `ob` (child of root) from the SAME swell as the ocean mesh at the root's x, y (ships sit in the water at every frame)."""
    drive(ob, 'location', 2, '%.3f+%s%s' % (base_z, swell_expr('x', 'y', amp), extra), dict(x=(root, 'location[0]'), y=(root, 'location[1]')))
    r = rnd(seed); a, b = r.uniform(0, 6.28), r.uniform(0, 6.28)
    if roll: drive(ob, 'rotation_euler', 0, '%.4f*sin(frame*0.11+%.3f)' % (roll, a), {})
    if pitch: drive(ob, 'rotation_euler', 1, '%.4f*sin(frame*0.09+%.3f)' % (pitch, b), {})

# ============================================================================= ships: common
def new_ship(name, kind, L, B, loc, yaw_deg, scale=1.0, sea=True, hscale=1.0):
    root = empty('ship_' + name, None, tuple(loc), (0, 0, math.radians(yaw_deg))); root.rotation_mode = 'XYZ'; root.scale = (scale,) * 3
    ride = empty('ride_' + name, root); sh = dict(name=name, kind=kind, L=L, B=B, root=root, ride=ride, base=Vector(loc), yaw=yaw_deg, scale=scale, guns=[], oars=[], masts=[], parts=[], sea=sea)
    if sea: ride_swell(ride, root, 0.0, 1.0 / scale, roll=0.014, pitch=0.007, seed=sum(ord(c) for c in name) % 97)
    S['ships'][name] = sh; return sh

def wake_foam(sh, big=True, bowspray=True):
    """Flat foam on the water, children of the root: bow-wave crests, side wash, stern wake (swell-driven so it sits on the surface)."""
    L, B = sh['L'], sh['B']; fb = MB(); mb_, mw_ = S['M']['foam_bow'], S['M']['foam_wake']; z = 0.0; n = Vector((0, 0, 1))
    for sg in (-1, 1):
        a = Vector((L / 2 - 0.8, 0, z)); b = Vector((L / 2 - 0.42 * L, sg * (B / 2 + 0.28 * B + 3.0), z)); side = (b - a).normalized().cross(n) * (0.13 * B + 1.3 * (1 if big else 0.6) * sg)
        fb.oface([a - side * 0.25, b - side, b + side, a + side * 0.5], mb_, [(0, 0), (1, 0), (1, 1), (0, 1)], n)
        a2 = Vector((L / 2 - 4.0, sg * (B / 2 - 0.3), z)); b2 = Vector((-L / 2, sg * (B / 2 + 0.2), z))
        fb.oface([a2, b2, b2 + Vector((0, sg * 1.4, 0)), a2 + Vector((0, sg * 1.0, 0))], mb_, [(0, 0.3), (1, 0.3), (1, 0.85), (0, 0.85)], n)
    s0 = Vector((-L / 2 + 0.8, 0, z)); s1 = Vector((-L / 2 - 2.4 * L, 0, z))
    fb.oface([s0 + Vector((0, -B * 0.42, 0)), s1 + Vector((0, -B * 1.4, 0)), s1 + Vector((0, B * 1.4, 0)), s0 + Vector((0, B * 0.42, 0))], mw_, [(0, 0), (1, 0), (1, 1), (0, 1)], n)
    o = mk(fb, 'foam_' + sh['name'], sh['root'], shadow=False); o.visible_glossy = False
    drive(o, 'location', 2, '%.3f+' % (0.17 / sh['scale']) + swell_expr('x', 'y', 1.0 / sh['scale']), dict(x=(sh['root'], 'location[0]'), y=(sh['root'], 'location[1]')))
    sh['foam'] = o
    if False and bowspray:
        mb = MB()
        for sg in (-1, 1):
            for k in range(6):
                t = k / 5.0; lump(mb, Vector((L / 2 - 1.0 - t * 0.3 * L, sg * (B * 0.22 + t * (B / 2 + 2.2)), 0.12 - 0.05 * t)), (0.55 - 0.3 * t) * min(1.3, B / 8), S['M']['spray'], 11 + k + (3 if sg > 0 else 0), seg=7, rings=4, rough=0.4, squash=0.35)
        for k in range(6): lump(mb, Vector((-L / 2 - 1.2 - k * 1.3, ((k * 37) % 7 - 3) * 0.4, 0.1)), 0.7 - 0.07 * k, S['M']['spray'], 40 + k, seg=7, rings=4, rough=0.4, squash=0.3)
        o2 = mk(mb, 'spray_' + sh['name'], sh['root'], shadow=False); smooth_round(o2, 1)
        drive(o2, 'location', 2, '0.1+' + swell_expr('x', 'y', 1.0), dict(x=(sh['root'], 'location[0]'), y=(sh['root'], 'location[1]'))); sh['spray'] = o2

def flag_obj(sh, key, base, h, w, wave=0.0, pole=True, parent=None, name='flag', pole_r=0.07, pole_mat=None, vertical=False, ph=0.0):
    """A flag on a pole: pole rod from base up h; cloth (plain colour or white banner) hung from the top, streaming aft (-x local), slight S wave."""
    mb = MB(); base = Vector(base); M_ = S['M']
    if pole: rod(mb, base, base + Vector((0, 0, h)), pole_r, pole_mat or M_['wood_d'], seg=6)
    top = base + Vector((0, 0, h)); fm = flagmat(key); mb2 = MB(); nu, nv = 6, 1
    if vertical:                                           # nobori: tall narrow banner on a cross-bar, hanging
        bar = w * 1.15; beam(mb, top - Vector((0, bar / 2, 0.08)), top + Vector((0, bar / 2, -0.08)), 0.07, 0.07, M_['wood_d'])
        quad_grid(mb2, lambda i, j: top + Vector((0.03 * math.sin(i * 0.9 + ph), -w / 2 + w * j, -0.15 - (w * 3.3) * i / nu)), nu, nv, fm, uvs=lambda i, j: (j, 1 - i / nu))
    else:
        quad_grid(mb2, lambda i, j: top + Vector((-w * i / nu, wave * math.sin(i * 1.1 + ph) * (i / nu), -(w * 0.62) * j - 0.1)), nu, nv, fm, uvs=lambda i, j: (i / nu, 1 - j))
    o = mk(mb, name + '_pole', parent or sh['ride']); o2 = mk(mb2, name + '_cloth', parent or sh['ride'], shadow=True); o2.data.materials[0] = fm
    for pg in o2.data.polygons: pg.use_smooth = True
    return o

def oar_set(sh, xs, ys, zp, length_out=6.4, length_in=1.4, dip=True, tilt_deg=None, stroke=True, blade=True, stow=False):
    """Oars through the hull side: pivot (x, +-y, zp); tilted so the blade dips into the water (dip) or raised (rest). Stroke = driver on the yaw."""
    M_ = S['M']; r = rnd(sum(ord(c) for c in sh['name']))
    for i, (x, yh) in enumerate(zip(xs, ys)):
        for sg in (1, -1):
            mb = MB(); rod(mb, (0, -length_in, 0), (0, length_out - 1.0, 0), 0.085, M_['wood_l'], seg=6, r1=0.07)
            beam(mb, (0, length_out - 1.3, 0), (0, length_out + 0.1, 0), 0.07, 0.8, M_['wood_l'])
            o = mk(mb, 'oar_%s_%d_%s' % (sh['name'], i, 'p' if sg > 0 else 's'), sh['ride']); o.location = (x, sg * yh, zp)
            a = math.asin(max(-0.9, min(0.9, (zp + 0.36) / (length_out - 0.5)))) if dip else math.radians(tilt_deg if tilt_deg is not None else 35)
            o.rotation_mode = 'XYZ'; o.rotation_euler = (-a if dip else a, 0, 0 if sg > 0 else math.pi)
            if stow:                                       # stowed: lashed along the hull side, blade aft, a little apart so they do not overlap
                o.location = (x, sg * (yh + 0.16 + 0.17 * (i % 3)), zp - 0.12 + 0.2 * ((i + 1) % 3)); o.rotation_euler = (math.radians(-2), 0, math.pi / 2 if True else 0)
            elif stroke and not (sh['name'] == 'turtle' and i == 5 and sg > 0): drive(o, 'rotation_euler', 2, '%.4f+0.2*sin(frame*0.33+%.3f)' % (0 if sg > 0 else math.pi, i * 0.5 + (0 if sg > 0 else 0.7) + r.uniform(0, 0.4)), {})
            sh['oars'].append(o)

# ============================================================================= THE TURTLE SHIP (hero prop)
TLEN = 34.0; THALF = 17.0; TBM = 4.6; Z_EAVE = 2.7
def t_b(x):
    p = 3.2 if x > 0 else 2.6
    return TBM * math.sqrt(max(0.0, 1.0 - (abs(x) / THALF) ** p))
def t_ye(x): return t_b(x) + 0.42
def t_H(x): return 2.7 * math.sqrt(max(0.0, 1.0 - (abs(x) / THALF) ** 2.4))
def roof_z(x, y):
    ye = max(0.05, t_ye(x)); v = min(1.0, abs(y) / ye); return Z_EAVE + t_H(x) * (1.0 - v ** 2.2)
def roof_n(x, y):
    e = 0.05; dx = (roof_z(x + e, y) - roof_z(x - e, y)) / (2 * e); dy = (roof_z(x, y + e) - roof_z(x, y - e)) / (2 * e); return Vector((-dx, -dy, 1.0)).normalized()

SPIKE_V = [(0.17, 0.29, 0.41), (0.53, 0.65, 0.77), (0.74, 0.81, 0.88)]     # spike lines (fraction of the half-width), ridge -> eave: stage 1, 2, 3

def build_turtle(name='turtle', loc=(0, 0, 0), yaw=0.0, sea=False, sail=False, oars_dip=None, scale=1.0, pitch=0.0, oar_tilt=35):
    M_ = S['M']; sh = new_ship(name, 'turtle', TLEN, 2 * TBM, loc, yaw, scale, sea=sea); ride = sh['ride']
    if pitch: ride.rotation_mode = 'XYZ'; ride.rotation_euler = (0, math.radians(pitch), 0)
    N = 36; xs = [-THALF + TLEN * (1 - math.cos(math.pi * i / N)) / 2 for i in range(N + 1)]
    prof = [(0.0, -1.55), (0.42, -1.5), (0.8, -1.05), (0.965, -0.4), (1.0, 0.0), (1.012, 1.0), (1.005, 2.0), (0.99, 2.52)]
    def hp(i, j):                                      # j runs over the full section: starboard keel->eave then port eave->keel
        x = xs[i]; b = t_b(x); k = j if j < len(prof) else 2 * len(prof) - 1 - j; f, z = prof[k]; return Vector((x, (f * b) * (1 if j < len(prof) else -1), z))
    mb = MB(); quad_grid(mb, hp, N, 2 * len(prof) - 1, M_['hull'], orient=lambda c: Vector((0, c.y, c.z * 0.2 + 0.001)).normalized() if abs(c.y) > 0.05 else Vector((0, 0, -1)))
    sh['hull'] = mk(mb, name + '_hull', ride, smooth=True)
    # --- roof (hexagonal plates) : the dome
    nv = 28; mb = MB()
    def rp(i, j):
        x = xs[i]; v = -1 + 2 * j / nv; y = v * t_ye(x); return Vector((x, y, roof_z(x, y)))
    quad_grid(mb, rp, N, nv, M_['hexroof'], uvs=lambda i, j: (xs[i] / 11.2, (-1 + 2 * j / nv) * t_ye(xs[i]) / 9.7), orient=lambda c: Vector((0, 0, 1)))
    sh['roof'] = mk(mb, name + '_roof', ride, smooth=True)
    # --- eave trim (dark wood lip) + soffit
    mb = MB()
    for sg in (-1, 1):
        for i in range(N):
            x0, x1 = xs[i], xs[i + 1]; a, b = Vector((x0, sg * t_ye(x0), Z_EAVE)), Vector((x1, sg * t_ye(x1), Z_EAVE)); a2, b2 = a - Vector((0, 0, 0.34)), b - Vector((0, 0, 0.34))
            mb.oface([a, b, b2, a2], M_['wood_d'], [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((0, sg, 0)))
            c0, c1 = Vector((x0, sg * t_b(x0), 2.52)), Vector((x1, sg * t_b(x1), 2.52)); mb.oface([a2, b2, c1, c0], M_['wood_d'], [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((0, 0, -1)))
    mk(mb, name + '_eave', ride)
    # --- cross-shaped walkway on the ridge
    mb = MB(); wy = 0.62
    def strip(f, n_, hw, lo, hi):
        quad_grid(mb, lambda i, j: f(lo + (hi - lo) * i / n_, -hw + 2 * hw * j) + Vector((0, 0, 0.1)), n_, 1, M_['walk'], orient=lambda c: Vector((0, 0, 1)))
    P_ = lambda t, d: Vector((t, d, roof_z(t, d)))                            # along the ridge
    strip(lambda t, d: P_(t, d), 30, wy, -10.5, 10.5)
    strip(lambda t, d: Vector((d, t, roof_z(d, t))), 14, wy, -3.3, 3.3)
    for sgn in (-1, 1):                                                         # low side rails of the long walkway
        for t0 in range(-10, 10):
            a = P_(t0, sgn * wy) + Vector((0, 0, 0.24)); b = P_(t0 + 1.0, sgn * wy) + Vector((0, 0, 0.24)); beam(mb, a, b, 0.07, 0.2, M_['wood_d'])
    mk(mb, name + '_walk', ride, smooth=False)
    # --- iron spikes in 3 stages (ridge -> eave); each stage is one object popped in by set_spikes
    sh['spikes'] = []
    for st, vs in enumerate(SPIKE_V):
        mb = MB()
        for li, vv in enumerate(vs):
            for sg in (-1, 1):
                x = -14.0 + (0.6 if (li + (sg > 0)) % 2 else 0.0)
                while x < 14.2:
                    ye = t_ye(x); y = sg * vv * ye
                    if abs(x) > 0.95 and ye * 0.12 > 0.30:
                        n = roof_n(x, y); base = Vector((x, y, roof_z(x, y))) - n * 0.04; dirv = (n * 0.35 + Vector((0, 0, 0.65))).normalized() if vv > 0.7 else (n + Vector((0, sg * 0.16, 0))).normalized(); tip = base + dirv * 0.82
                        mb.frustum(base, tip, 0.2, 0.0, M_['iron'], seg=5, cap1=False)
                    x += 1.22
        sh['spikes'].append(mk(mb, '%s_spikes_%d' % (name, st + 1), ride, smooth=False))
    # --- gun ports (6 per side), lids on hinges, cannon muzzles
    sh['lids'] = []; sh['muzzles'] = []; mbs = MB(); gx = [-10.0 + 4.0 * i for i in range(6)]
    for i, x in enumerate(gx):
        b = t_b(x) * 1.004
        for sg in (-1, 1):
            cy_ = sg * b; mbs.oface([Vector((x - 0.55, cy_ + sg * 0.015, 1.3)), Vector((x + 0.55, cy_ + sg * 0.015, 1.3)), Vector((x + 0.55, cy_ + sg * 0.015, 2.2)), Vector((x - 0.55, cy_ + sg * 0.015, 2.2))], M_['port_dark'], [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((0, sg, 0)))
            for (dx, dz, w_, h_) in ((-0.62, 1.75, 0.08, 1.0), (0.62, 1.75, 0.08, 1.0), (0, 2.27, 1.3, 0.09), (0, 1.27, 1.3, 0.09)):
                cbox(mbs, (x + dx, cy_ + sg * 0.03, dz), w_ / 2 + 0.02, 0.07, h_ / 2, M_['red_d'])
            mbl = MB(); mbl.box((-0.56, 0.0, -0.9), (0.56, 0.07, 0.0), M_['red']); cbox(mbl, (0, 0.075, -0.45), 0.13, 0.02, 0.13, M_['gold'])
            lid = mk(mbl, '%s_lid_%d_%s' % (name, i, 'p' if sg > 0 else 's'), ride); lid.location = (x, cy_ + sg * 0.05, 2.2); lid.rotation_mode = 'XYZ'
            if sg < 0: lid.rotation_euler = (0, 0, math.pi)
            sh['lids'].append((lid, sg))
            mbm = MB(); rod(mbm, (0, -1.1, 0), (0, 0.55, 0), 0.3, M_['cannon'], seg=10); rod(mbm, (0, 0.5, 0), (0, 0.75, 0), 0.37, M_['cannon'], seg=10); rod(mbm, (0, -0.2, 0), (0, 0.2, 0), 0.36, M_['cannon'], seg=10)
            mz = mk(mbm, '%s_muzzle_%d_%s' % (name, i, 'p' if sg > 0 else 's'), ride); mz.location = (x, cy_, 1.75)
            if sg < 0: mz.rotation_mode = 'XYZ'; mz.rotation_euler = (0, 0, math.pi)
            mz.hide_render = True; sh['muzzles'].append(mz); sh['guns'].append(dict(local=Vector((x, cy_ + sg * 0.9, 1.75)), dir=Vector((0, sg, 0.15)).normalized(), name='%s_g%d%s' % (name, i, 'p' if sg > 0 else 's')))
    mk(mbs, name + '_ports', ride)
    # --- carved dragon head at the bow
    dragon(sh)
    # --- turtle tail, rudder, stem post
    mb = MB(); rod(mb, (-16.2, 0, 0.3), (-19.4, 0, 2.2), 0.62, M_['wood_d'], seg=8, r1=0.3); beam(mb, (-17.3, 0, -1.4), (-17.3, 0, 2.0), 0.18, 0.9, M_['wood_d'], up=(1, 0, 0)); rod(mb, (16.3, 0, -0.8), (17.4, 0, 2.3), 0.55, M_['wood_d'], seg=8, r1=0.4)
    cbox(mb, (-18.9, 0, 2.5), 0.5, 0.2, 0.12, M_['gold']); mk(mb, name + '_tail', ride)
    # --- oars
    ox = [-11.5 + 2.55 * i for i in range(10)]; oy = [t_b(x) + 0.04 for x in ox]
    oar_set(sh, ox, oy, 1.0, dip=(sea if oars_dip is None else oars_dip), stroke=sea, tilt_deg=oar_tilt, stow=not sea)
    # --- two masts (kept up), stays, flags; matting sails at sea
    for mi, mx in enumerate((5.0, -6.0)):
        zb = roof_z(mx, 0) + 0.1; H_ = 8.2 if mi == 0 else 6.6; mb = MB(); rod(mb, (mx, 0, zb), (mx, 0, zb + H_), 0.17, M_['wood_l'], seg=8, r1=0.11)
        beam(mb, (mx - 0.1, -2.6, zb + H_ * 0.82), (mx - 0.1, 2.6, zb + H_ * 0.82), 0.1, 0.1, M_['wood_l'])
        for (yy, ex) in ((3.2, 0), (-3.2, 0)): rod(mb, (mx, 0, zb + H_ * 0.9), (mx + 0.3 * (1 if mi else -1), yy * 1.45, roof_z(mx, yy * 1.45) + 0.05), 0.025, M_['rope'], seg=4)
        mk(mb, '%s_mast%d' % (name, mi), ride); sh['masts'].append((mx, zb, H_))
        flag_obj(sh, 'flag_tri_red' if mi == 0 else 'flag_tri_blue', (mx, 0, zb + H_), 0.5, 1.9, 0.12, pole=False, name='%s_pen%d' % (name, mi), ph=mi)
        if sail and mi == 0:
            mb = MB(); sw, shh = 5.6, 4.6
            quad_grid(mb, lambda i, j: Vector((mx - 0.25 - 0.9 * math.sin(math.pi * j / 6) * math.sin(math.pi * i / 8) , -sw / 2 + sw * j / 6, zb + H_ * 0.82 - shh * i / 8)), 8, 6, M_['sail_k'], uvs=lambda i, j: (j / 6 * 1.4, i / 8 * 1.2), orient=lambda c: Vector((-1, 0, 0)))
            s_ = mk(mb, name + '_sail', ride, smooth=True)
    flag_obj(sh, 'flag_red', (-17.0, 0, 2.6), 4.2, 2.6, 0.25, name=name + '_stern', ph=1.5)
    if sea: wake_foam(sh, True, True); oar_rings(sh, ox, oy); build_splash(sh, ox, oy)
    return sh

def dragon(sh):
    """Carved dragon head: red + gold + teal, open mouth with teeth, horns, eyes, mane. Mouth centre = sh['mouth'] (ride-local)."""
    M_ = S['M']; ride = sh['ride']; mb = MB(); X, Y, Z = Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))
    rod(mb, (15.6, 0, 2.4), (17.5, 0, 3.7), 1.18, M_['teal'], seg=12, r1=0.95)
    ell(mb, (18.5, 0, 3.75), 1.3, 1.02, 0.98, M_['dragon_red'], 14, 9)
    a = math.radians(7); ax = (Vector((math.cos(a), 0, -math.sin(a))), Y, Vector((math.sin(a), 0, math.cos(a))))
    obox(mb, Vector((20.2, 0, 3.52)), *ax, 1.1, 0.64, 0.42, M_['dragon_red']); ell(mb, (21.25, 0, 3.4), 0.72, 0.64, 0.44, M_['dragon_red'], 12, 8)
    a2 = math.radians(24); ax2 = (Vector((math.cos(a2), 0, -math.sin(a2))), Y, Vector((math.sin(a2), 0, math.cos(a2)))); H = Vector((19.0, 0, 2.95))
    obox(mb, H + ax2[0] * 1.15 + ax2[2] * -0.15, *ax2, 1.15, 0.52, 0.2, M_['gold']); ell(mb, H + ax2[0] * 2.3 + ax2[2] * -0.15, 0.35, 0.5, 0.2, M_['gold'], 10, 6)
    obox(mb, Vector((19.9, 0, 3.12)), X, Y, Z, 0.95, 0.5, 0.3, M_['mouth']); ell(mb, (19.9, 0, 2.95), 0.75, 0.3, 0.14, M_['tongue'], 10, 6)
    for i in range(6):
        xx = 19.3 + 0.38 * i
        for sg in (-1, 1):
            cone(mb, (xx, sg * 0.5, 3.18), (xx + 0.03, sg * 0.5, 2.78), 0.085, M_['tooth'], 5)
            cone(mb, H + ax2[0] * (0.4 + 0.42 * i) + Vector((0, sg * 0.46, 0.0)) + ax2[2] * 0.0, H + ax2[0] * (0.4 + 0.42 * i) + Vector((0, sg * 0.46, 0.0)) + ax2[2] * 0.4, 0.07, M_['tooth'], 5)
    for sg in (-1, 1):
        ell(mb, (18.9, sg * 0.84, 4.12), 0.34, 0.2, 0.34, M_['eye_w'], 10, 6); ell(mb, (19.05, sg * 0.97, 4.13), 0.18, 0.1, 0.18, M_['eye_k'], 8, 5)
        beam(mb, (18.4, sg * 0.8, 4.55), (19.5, sg * 0.82, 4.4), 0.2, 0.12, M_['teal']); ell(mb, (21.45, sg * 0.25, 3.78), 0.1, 0.1, 0.08, M_['eye_k'], 6, 4)
        pts = [(18.1, sg * 0.5, 4.5), (17.3, sg * 0.75, 5.2), (16.4, sg * 1.0, 5.6), (15.6, sg * 1.2, 5.45)]
        for k in range(3): rod(mb, pts[k], pts[k + 1], 0.27 - 0.08 * k, M_['gold'], seg=6, r1=0.27 - 0.08 * (k + 1))
        ell(mb, (17.4, sg * 1.2, 3.5), 0.15, 0.55, 0.45, M_['teal'], 8, 5)
    for k in range(6):
        xx = 18.0 - 0.45 * k; cone(mb, (xx, 0, 4.55 - 0.05 * k), (xx - 0.9, 0, 5.2 + 0.08 * k - 0.1 * k), 0.3 - 0.02 * k, M_['dragon_red'] if k % 2 == 0 else M_['gold'], 5)
    sh['dragon'] = mk(mb, sh['name'] + '_dragon', ride); sh['mouth'] = Vector((20.4, 0, 3.15))

def oar_rings(sh, ox, oy, length_out=6.4):
    """Foam ring + a few spray lumps where each oar blade meets the water (flat on the surface, swell-driven; children of the root)."""
    M_ = S['M']; mbs = {}
    for i, (x, yh) in enumerate(zip(ox, oy)):
        for sg in (1, -1):
            c = Vector((x - 0.2, sg * (yh + length_out - 0.6), 0.0)); mb = MB(); rr = 0.8
            mb.oface([Vector((-rr, -rr, 0)), Vector((rr, -rr, 0)), Vector((rr, rr, 0)), Vector((-rr, rr, 0))], M_['ring_f'], [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((0, 0, 1)))
            o = mk(mb, 'ring_%s_%d_%d' % (sh['name'], i, sg), sh['root'], shadow=False); o.location = (c.x, c.y, 0.2); drive_at(o, sh['root'], c, 0.2)

def build_splash(sh, ox, oy, length_out=6.4):
    """Hero oar splash (starboard oar 5 of the turtle ship, sea): 18 small droplets on ballistic arcs + two foam rings that grow and fade. Driven by set_oar_splash(t)."""
    M_ = S['M']; i = 5; c = Vector((ox[i], oy[i] + length_out - 0.75, 0.0)); r = rnd(77); S['splash'] = dict(c=c, drops=[], rings=[], root=sh['root'])
    for k in range(2):
        def f(b, k=k):
            t = b.img('foam_ring', 1.0, 'FLAT', vec=b.n('ShaderNodeUVMap').outputs[0], ext='EXTEND'); op = b.n('ShaderNodeValue'); op.name = 'op'; op.outputs[0].default_value = 1.0
            m = b.math('MULTIPLY', t.outputs['Alpha'], op.outputs[0]); d = b.n('ShaderNodeBsdfDiffuse'); d.inputs['Color'].default_value = (0.9, 0.95, 0.95, 1); em = b.n('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.85, 0.92, 0.92, 1); em.inputs['Strength'].default_value = 0.35
            ad = b.n('ShaderNodeAddShader'); b.l(d.outputs[0], ad.inputs[0]); b.l(em.outputs[0], ad.inputs[1]); tr = b.n('ShaderNodeBsdfTransparent'); mx = b.n('ShaderNodeMixShader'); b.l(m, mx.inputs[0]); b.l(tr.outputs[0], mx.inputs[1]); b.l(ad.outputs[0], mx.inputs[2]); b.l(mx.outputs[0], b.out.inputs['Surface'])
        mt = mat('J_splash_ring%d' % k, f); mb = MB(); rr = 1.0
        mb.oface([Vector((-rr, -rr, 0)), Vector((rr, -rr, 0)), Vector((rr, rr, 0)), Vector((-rr, rr, 0))], mt, [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((0, 0, 1)))
        o = mk(mb, 'splash_ring_%d' % k, sh['root'], shadow=False); o.location = (c.x, c.y, 0.2); o.hide_render = True
        drive_at(o, sh['root'], c, 0.26); S['splash']['rings'].append(dict(ob=o, mat=mt, delay=0.0 if k == 0 else 0.28))
    for k in range(70):
        mb = MB(); lump(mb, (0, 0, 0), 1.0, M_['drop'], 3000 + k, seg=8, rings=5, rough=0.05); o = mk(mb, 'drop_%d' % k, sh['root'], shadow=False); smooth_round(o, 1); o.hide_render = True
        a = r.uniform(0, 6.283); sp = r.uniform(0.15, 1.0); S['splash']['drops'].append(dict(ob=o, v=Vector((math.cos(a) * sp, math.sin(a) * sp, r.uniform(2.2, 3.7))), r=r.uniform(0.014, 0.042)))

def set_oar_splash(t, frame=None):
    """Splash at the dipping blade of the hero oar (macro_oar): t 0 = nothing .. 0..1 = the splash growing and fading (map t = (frame - f0) / 15 for a 15-frame splash). Droplets fly on arcs and shrink, two foam rings
    expand and fade. Frame-keyable (keys linear, visibility constant). Needs the sea location."""
    K = S.get('splash')
    if not K: return
    t = float(t); c = K['c']; vis = 0.0 < t < 1.0
    for d in K['drops']:
        u = max(0.0, min(1.0, t)); p = Vector((c.x + d['v'].x * u * 3.0, c.y + d['v'].y * u * 3.0, 0.2 + d['v'].z * u * 1.15 - 4.6 * u * u)); sc = d['r'] * (1.0 - u) ** 0.4
        d['ob'].location = p; d['ob'].scale = (sc, sc, sc); show(d['ob'], vis and p.z > 0.0, frame)
        if frame is not None: key_attr(d['ob'], 'location', frame, 'LINEAR'); key_attr(d['ob'], 'scale', frame, 'LINEAR')
    for rg in K['rings']:
        u = max(0.0, min(1.0, (t - rg['delay']) / (1.0 - rg['delay']))); sc = 0.3 + 1.05 * u; rg['ob'].scale = (sc, sc, 1.0); op = (1.0 - u) ** 1.1 if 0.0 < u < 1.0 else 0.0
        nd = rg['mat'].node_tree.nodes['op']; nd.outputs[0].default_value = op; show(rg['ob'], op > 0.001, frame)
        if frame is not None:
            key_attr(rg['ob'], 'scale', frame, 'LINEAR'); nd.outputs[0].keyframe_insert('default_value', frame=frame)
            for fc in T._fcurves(rg['mat'].node_tree):
                for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    S['splash_t'] = t

# ============================================================================= materials
def make_materials():
    tx = S['tx']; M_ = {}
    M_['hull'] = wood('hull', '#976c4d', '#6a4630', 1.1, 'Z', 0.7, waterline=True)
    M_['hull_a'] = wood('hull_a', '#8c5e40', '#5a3828', 1.0, 'Z', 0.7, waterline=True); M_['wall_w'] = wood('wall_w', '#6e4932', '#46301f', 1.3, 'Z', 0.75)
    M_['hull_k'] = wood('hull_k', '#9c5a3a', '#6c3826', 1.1, 'Z', 0.68, waterline=True); M_['hull_k2'] = wood('hull_k2', '#8a4c34', '#5e3022', 1.1, 'Z', 0.68, waterline=True); M_['plank_k'] = wood('plank_k', '#a35e3e', '#6c3826', 1.4, 'Z', 0.72)
    M_['sail_c'] = imgmat('sail_c', 'flag_sail', 1.0, rough=0.9, bumpk=0.3, uv=True)
    M_['hull_dk'] = wood('hull_dk', '#7c563c', '#553726', 1.1, 'Z', 0.7, waterline=True)
    M_['hexroof'] = imgmat('hex', 'hex', 1.0, rough=0.62, bumpk=0.9, uv=True)
    M_['walk'] = wood('walk', '#c8a46c', '#8d6a40', 1.8, 'Y', 0.65)
    M_['wood_d'] = wood('wood_d', '#5e3f2a', '#3c271b', 1.5, 'Y', 0.75); M_['wood_l'] = wood('wood_l', '#b88f5c', '#8a6a42', 1.6, 'Y', 0.7)
    M_['plank'] = wood('plank', '#a87c4e', '#6e4c30', 1.4, 'Z', 0.75); M_['deck'] = wood('deck', '#b98d58', '#7a5634', 1.6, 'Y', 0.7)
    M_['iron'] = flat('iron', '#3d4047', 0.34, 0.85); M_['cannon'] = flat('cannon', '#26282c', 0.4, 0.75)
    M_['port_dark'] = flat('port_dark', '#120d0c', 0.95); M_['red'] = flat('red', '#b3262a', 0.38); M_['red_d'] = flat('red_d', '#7e1c1e', 0.42)
    M_['gold'] = flat('gold', '#cb9f48', 0.3, 0.9); M_['teal'] = flat('teal', '#2c8a7a', 0.38); M_['dragon_red'] = flat('dragon_red', '#b8282c', 0.32)
    M_['mouth'] = flat('mouth', '#4d1018', 0.8); M_['tongue'] = flat('tongue', '#c85060', 0.5); M_['tooth'] = flat('tooth', '#f4eddc', 0.3)
    M_['eye_w'] = flat('eye_w', '#f6f2e6', 0.2); M_['eye_k'] = flat('eye_k', '#101010', 0.15); M_['rope'] = flat('rope', '#b79a62', 0.95)
    M_['sail_k'] = imgmat('matting', 'matting', 0.18, rough=0.9, bumpk=0.4); M_['sail_d'] = imgmat('matting_d', 'matting_d', 0.18, rough=0.9, bumpk=0.4)
    M_['cloth_w'] = flat('cloth_w', '#eee6d2', 0.95); M_['cloth_s'] = imgmat('cloth_s', 'flag_white_k', 1.0, uv=True, rough=0.95, bumpk=0.0)
    M_['black_l'] = flat('black_l', '#151316', 0.22); M_['red_l'] = flat('red_l', '#a8201f', 0.28); M_['white_p'] = flat('white_p', '#e9e2d0', 0.8)
    M_['tile'] = imgmat('tile', 'tile', 0.09, rough=0.6, bumpk=0.6); M_['tile_d'] = imgmat('tile_d', 'tile_d', 0.09, rough=0.6, bumpk=0.6)
    M_['stone'] = imgmat('stone', 'stone', 0.12, rough=0.92, bumpk=0.7); M_['stone_d'] = imgmat('stone_d', 'stone_d', 0.12, rough=0.92, bumpk=0.7)
    M_['dancheong'] = imgmat('dancheong', 'dancheong', 0.45, rough=0.55, bumpk=0.1)
    M_['plaster'] = flat('plaster', '#d9ceb4', 0.9); M_['basket'] = imgmat('basket', 'matting_d', 0.5, rough=0.95, bumpk=0.5)
    M_['drop'] = flat('drop', '#eef6f6', 0.25, 0.0, **{'Emission Color': (0.9, 0.95, 0.97, 1.0), 'Emission Strength': 0.9}); M_['earth'] = flat('earth', '#8a7456', 0.95); M_['spray'] = flat('spray', '#f3f7f6', 0.9)
    M_['smoke_g'] = smoke_mat('g', '#a8a499'); M_['smoke_d'] = smoke_mat('d', '#74716f'); M_['smoke_y'] = smoke_mat('y', '#b6ab80')
    M_['flash'] = emit('flash', '#ffcf6a', 40.0); M_['green_p'] = flat('green_p', '#2a7a58', 0.5); M_['blue_p'] = flat('blue_p', '#2a56a8', 0.5)
    for nm, k in (('wake', 'foam_wake'), ('bow', 'foam_bow'), ('ring', 'foam_ring'), ('surf', 'foam_surf')):
        def f(b, k=k):
            t = b.img(k, 1.0, 'FLAT', vec=b.n('ShaderNodeUVMap').outputs[0], ext='EXTEND'); d = b.n('ShaderNodeBsdfDiffuse'); d.inputs['Color'].default_value = (0.9, 0.95, 0.95, 1)
            em = b.n('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.85, 0.92, 0.92, 1); em.inputs['Strength'].default_value = 0.35; ad = b.n('ShaderNodeAddShader'); b.l(d.outputs[0], ad.inputs[0]); b.l(em.outputs[0], ad.inputs[1])
            tr = b.n('ShaderNodeBsdfTransparent'); mx = b.n('ShaderNodeMixShader'); b.l(t.outputs['Alpha'], mx.inputs[0]); b.l(tr.outputs[0], mx.inputs[1]); b.l(ad.outputs[0], mx.inputs[2]); b.l(mx.outputs[0], b.out.inputs['Surface'])
        M_['foam_' + nm if nm in ('wake', 'bow') else nm + '_f'] = mat('J_foam_' + nm, f)
    M_['foam_wake'] = M_['foam_wake']; M_['foam_bow'] = M_['foam_bow']
    for k in ('red', 'black', 'white_r', 'white_k', 'tri_red', 'tri_black', 'tri_blue', 'tri_yellow', 'nob_circle', 'nob_diamond', 'nob_rcircle'): flagmat('flag_' + k)
    S['M'] = M_; return M_

def water_mat(name, calm=False):
    def f(b):
        c = b.coord(); gp = b.n('ShaderNodeNewGeometry'); z = b.n('ShaderNodeSeparateXYZ'); b.l(gp.outputs['Position'], z.inputs[0])
        patch = b.noise(0.035 if not calm else 0.06, 2.0, 0.5, c, None)
        deep, mid, shl = ('#053a52', '#0b5a6e', '#22888a') if not calm else ('#0c3f4a', '#165a62', '#26746e')
        col = b.mix(b.rng(patch, 0.35, 0.65), hexl(deep), hexl(mid))
        crest = b.rng(z.outputs['Z'], 0.12 if not calm else 9, 0.45, 0, 1); col = b.mix(b.math('MULTIPLY', crest, b.rng(b.noise(0.5, 1.0, 0.5, c), 0.35, 0.7), clamp=True), col, hexl(shl))
        if not calm:
            bignz = b.rng(b.noise(0.011, 2.0, 0.5, c), 0.3, 0.7, 0.45, 1.0); col = b.mix(b.math('MULTIPLY', b.rng(z.outputs['Z'], 0.0, -0.42, 0.0, 0.85), bignz), col, hexl('#021d33'))
            col = b.mix(b.rng(b.noise(0.0035, 2.0, 0.5, c), 0.35, 0.65, 0.0, 0.35), col, hexl('#0d6c74'))
        if not calm:
            sp = b.rng(b.noise(0.6, 0.0, 0.5, c), 0.68, 0.76); wc = b.math('MULTIPLY', b.rng(z.outputs['Z'], 0.34, 0.50), sp, clamp=True); col = b.mix(wc, col, (0.93, 0.97, 0.96, 1))
        n1 = b.noise(1.3 if not calm else 0.9, 2.0, 0.5, c); n2 = b.noise(5.0, 1.0, 0.5, c); h = b.math('ADD', n1, b.math('MULTIPLY', n2, 0.35))
        st = 0.42 if not calm else 0.06
        if not calm:
            cd = b.n('ShaderNodeCameraData'); st = b.rng(cd.outputs['View Distance'], 70.0, 230.0, 0.42, 0.16, smooth=True)
        nrm = b.bump(h, st, 0.08)
        b.princ(col, 0.05 if not calm else 0.03, 0.0, nrm, IOR=1.333)
    return mat('J_' + name, f)

def land_mat(name, sand=False, rock=True, grass='#4f7d3c', rockc='#85796a', sandc='#dcc690'):
    def f(b):
        c = b.coord(); gp = b.n('ShaderNodeNewGeometry'); z = b.n('ShaderNodeSeparateXYZ'); b.l(gp.outputs['Position'], z.inputs[0])
        nz = b.n('ShaderNodeSeparateXYZ'); b.l(gp.outputs['True Normal'], nz.inputs[0]); n1 = b.noise(0.4, 4.0, 0.6, c); n2 = b.noise(3.0, 3.0, 0.5, c)
        gcol = b.mix(b.rng(n1, 0.35, 0.65), hexl(grass), hexl('#3a6a30'))
        rcol = b.mix(b.rng(n2, 0.3, 0.7), hexl(rockc), tint(rockc, 0.62) + (1.0,))
        slope = b.rng(nz.outputs['Z'], 0.55, 0.78, 0.0, 1.0) if rock else 1.0
        col = b.mix(slope, rcol, gcol)
        if sand:
            sd = b.rng(z.outputs['Z'], 0.9, 1.5, 1.0, 0.0); col = b.mix(sd, col, hexl(sandc))
        nrm = b.bump(b.math('ADD', n1, n2), 0.5, 0.2); b.princ(col, 0.92, 0.0, nrm)
    return mat('J_' + name, f)

def foliage_mat(name='pine'):
    def f(b):
        oi = b.n('ShaderNodeObjectInfo'); c = b.coord(); n = b.noise(2.0, 2.0, 0.5, c)
        col = b.mix(b.math('ADD', b.math('MULTIPLY', oi.outputs['Random'], 0.6), b.math('MULTIPLY', n, 0.4), clamp=True), hexl('#2a5532'), hexl('#47773e'))
        b.princ(col, 0.85, 0.0, b.bump(n, 0.35, 0.1))
    return mat('J_' + name, f)

# ============================================================================= terrain, pines, islands, mountains
def hfield(x, y, seed=0):
    return (math.sin(0.21 * x + seed) * math.cos(0.17 * y - seed) + 0.6 * math.sin(0.53 * x + 1.3 * seed + 0.7 * y) + 0.35 * math.sin(1.1 * x - 0.9 * y + seed)) / 1.95

def pine_kit(n=5):
    """n distinct pine meshes (shared mesh data, instanced as linked objects): trunk + 4-6 drooping tiers."""
    kit = []; fm = foliage_mat(); tm = flat('bark', '#5a3e2a', 0.95)
    for v in range(n):
        r = rnd(100 + v); mb = MB(); h = r.uniform(9.5, 13.0); nt_ = r.randint(4, 6)
        rod(mb, (0, 0, -0.4), (0, 0, h * 0.8), 0.28, tm, seg=5, r1=0.1)
        for t in range(nt_):
            f = t / nt_; zb = h * (0.16 + 0.62 * f); rr = (2.9 - 2.1 * f) * r.uniform(0.9, 1.1); hh = h * 0.30 * (1.0 - 0.3 * f)
            mb.frustum((0, 0, zb), (r.uniform(-0.1, 0.1), r.uniform(-0.1, 0.1), zb + hh), rr, 0.0, fm, seg=7, cap1=False)
        mb.frustum((0, 0, h * 0.78), (0, 0, h), 0.8, 0.0, fm, seg=6, cap1=False)
        me = bpy.data.meshes.new('pine%d' % v); me.from_pydata([Vector(a) for a in mb.v], [], mb.f); me.update()
        for m in mb.mats: me.materials.append(m)
        for fi, p in enumerate(me.polygons): p.material_index = mb.mi[fi]
        kit.append(me)
    S['pines'] = kit

def plant(x, y, z, h=None, seed=0, coll=None, rot=None):
    r = rnd(seed); me = S['pines'][r.randrange(len(S['pines']))]; o = bpy.data.objects.new('pine', me); (coll or S['coll']).objects.link(o)
    k = (h or r.uniform(0.8, 1.15)); o.location = (x, y, z); o.scale = (k * r.uniform(0.85, 1.1), k * r.uniform(0.85, 1.1), k); o.rotation_euler = (0, 0, r.uniform(0, 6.28)); return o

def polar_mesh(name, cx, cy, hfun, rmax, nr=28, nt=72, growth=1.06):
    """Radial height-field mesh around (cx, cy): rings spacing grows outward (fine near the shore). hfun(x, y) -> z."""
    rs = [0.0]; d = rmax / nr * 0.55
    while rs[-1] < rmax: d *= growth; rs.append(min(rmax, rs[-1] + d))
    rs = [r * rmax / rs[-1] for r in rs]; vs = []; fs = []
    for ri, r in enumerate(rs):
        for ti in range(nt):
            a = 2 * math.pi * ti / nt; x, y = cx + r * math.cos(a), cy + r * math.sin(a); vs.append((x, y, hfun(x, y)))
    for ri in range(len(rs) - 1):
        for ti in range(nt):
            t2 = (ti + 1) % nt; fs.append((ri * nt + ti, ri * nt + t2, (ri + 1) * nt + t2, (ri + 1) * nt + ti))
    me = bpy.data.meshes.new(name); me.from_pydata(vs, [], fs); me.update(); [setattr(p, 'use_smooth', True) for p in me.polygons]
    ob = bpy.data.objects.new(name, me); S['coll'].objects.link(ob); return ob, me

def make_island(name, cx, cy, R, H, seed, kind='rock', npine=60, sand=False, dirn=None):
    """Green rocky island (or the beach island): height field cut by the sea level; pines and boulders placed ON the surface."""
    r = rnd(seed)
    def h(x, y):
        dx, dy = x - cx, y - cy; rr = math.hypot(dx, dy); a = math.atan2(dy, dx)
        Rn = R * (1 + 0.28 * math.sin(3 * a + seed) + 0.14 * math.sin(5 * a + 2 * seed) + 0.08 * math.sin(9 * a))
        u = rr / Rn
        if u >= 1: return -(u - 1) * (6 if kind == 'rock' else 3.0) - 0.05
        f = (1 - u * u) ** (1.15 if kind == 'rock' else 1.0)
        z = H * f * (1 + 0.28 * hfield(x * 0.6, y * 0.6, seed)) + (0.9 * H * 0.12 * math.sin(2.1 * a + 5 * u) * (1 - u) if kind == 'rock' else 0)
        if dirn is not None: z *= 0.55 + 0.45 * (0.5 + 0.5 * math.cos(a - dirn)) ** 0.7 if kind == 'beach' else 1.0
        return z - 0.15
    ob, me = polar_mesh(name, cx, cy, h, R * 1.5, 30, 80); me.materials.append(land_mat(name + '_m', sand=sand, rock=(kind == 'rock'), grass='#5a8240' if kind == 'beach' else '#4f7d3c'))
    S['islands'][name] = dict(c=(cx, cy), R=R, h=h)
    placed = 0; tries = 0
    while placed < npine and tries < npine * 12:
        tries += 1; a = r.uniform(0, 6.283); u = math.sqrt(r.uniform(0.0, 0.8)); x, y = cx + R * u * math.cos(a), cy + R * u * math.sin(a); z = h(x, y)
        if z < (1.8 if sand else 0.9): continue
        e = 0.5; sl = max(abs(h(x + e, y) - z), abs(h(x, y + e) - z)) / e
        if sl > 1.5: continue
        plant(x, y, z, r.uniform(0.7, 1.15) * (1.0 if kind == 'rock' else 0.8), seed * 100 + placed); placed += 1
    bm = MB(); mrock = flat('boulder', '#7e7466', 0.95)
    for k in range(int(R * 0.35)):
        a = r.uniform(0, 6.283); u = r.uniform(0.62, 1.0); x, y = cx + R * u * math.cos(a), cy + R * u * math.sin(a); z = h(x, y)
        if -0.4 < z < 2.2: lump(bm, (x, y, z + 0.1), r.uniform(0.5, 1.6), mrock, seed + k, seg=8, rings=5, rough=0.28, squash=0.7)
    if bm.f: mk(bm, name + '_rocks', smooth=True)
    return ob

def make_mountains(cx, cy, R0, R1, hmax, seed, az0=0, az1=360, col='#5b8a62', col2='#7c8f78', nt=180):
    """Backdrop mountain ring (green-blue, faded by the haze) between radii R0..R1 over azimuths az0..az1."""
    r = rnd(seed); vs = []; fs = []; nr = 7; ph = [r.uniform(0, 6.28) for _ in range(5)]
    def hz(a): return hmax * (0.35 + 0.65 * abs(math.sin(2.3 * a + ph[0]) * 0.6 + math.sin(5.1 * a + ph[1]) * 0.3 + math.sin(11.0 * a + ph[2]) * 0.18)) 
    n_az = int((az1 - az0) / 360 * nt) + 1
    for ri in range(nr):
        u = ri / (nr - 1); rr = R0 + (R1 - R0) * u
        for ti in range(n_az):
            a = math.radians(az0 + (az1 - az0) * ti / (n_az - 1)); z = hz(a) * (1 - u) ** 1.4 * (1 + 0.18 * math.sin(a * 37 + ri) ) - 4 + (2 if ri == 0 else 0)
            vs.append((cx + rr * math.cos(a), cy + rr * math.sin(a), z))
    for ri in range(nr - 1):
        for ti in range(n_az - 1): fs.append((ri * n_az + ti, ri * n_az + ti + 1, (ri + 1) * n_az + ti + 1, (ri + 1) * n_az + ti))
    me = bpy.data.meshes.new('mountains'); me.from_pydata(vs, [], fs); me.update(); [setattr(p, 'use_smooth', True) for p in me.polygons]
    def f(b):
        gp = b.n('ShaderNodeNewGeometry'); z = b.n('ShaderNodeSeparateXYZ'); b.l(gp.outputs['Position'], z.inputs[0]); n = b.noise(0.05, 3.0, 0.6, b.coord())
        c1 = b.mix(b.rng(z.outputs['Z'], 5, hmax * 0.8), hexl(col), hexl(col2)); c1 = b.mix(b.rng(n, 0.3, 0.7), c1, tint(col, 0.75) + (1.0,)); b.princ(c1, 0.95)
    me.materials.append(mat('J_mount_%d' % seed, f)); ob = bpy.data.objects.new('mountains', me); S['coll'].objects.link(ob); return ob

# ============================================================================= the ocean (film-10 swell geometry, physically shaded)
def swell_group():
    ng = bpy.data.node_groups.new('JO_swell', 'GeometryNodeTree')
    ng.interface.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry'); ng.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    N = ng.nodes.new; L = ng.links.new; gi = N('NodeGroupInput'); go = N('NodeGroupOutput'); pos = N('GeometryNodeInputPosition'); sp = N('ShaderNodeSeparateXYZ'); L(pos.outputs[0], sp.inputs[0]); tm = N('GeometryNodeInputSceneTime')
    def wave(A, lam, ang, spd):
        k = 2 * math.pi / lam; ca, sa = math.cos(math.radians(ang)) * k, math.sin(math.radians(ang)) * k
        m1 = N('ShaderNodeMath'); m1.operation = 'MULTIPLY'; m1.inputs[1].default_value = ca; L(sp.outputs['X'], m1.inputs[0])
        m2 = N('ShaderNodeMath'); m2.operation = 'MULTIPLY_ADD'; m2.inputs[1].default_value = sa; L(sp.outputs['Y'], m2.inputs[0]); L(m1.outputs[0], m2.inputs[2])
        m3 = N('ShaderNodeMath'); m3.operation = 'MULTIPLY_ADD'; m3.inputs[1].default_value = -spd; L(tm.outputs['Seconds'], m3.inputs[0]); L(m2.outputs[0], m3.inputs[2])
        s_ = N('ShaderNodeMath'); s_.operation = 'SINE'; L(m3.outputs[0], s_.inputs[0]); a_ = N('ShaderNodeMath'); a_.operation = 'MULTIPLY'; a_.inputs[1].default_value = A; L(s_.outputs[0], a_.inputs[0]); return a_
    def add(a, b): ad = N('ShaderNodeMath'); ad.operation = 'ADD'; L(a.outputs[0], ad.inputs[0]); L(b.outputs[0], ad.inputs[1]); return ad
    tot = None
    for w in SWELL: tot = wave(*w) if tot is None else add(tot, wave(*w))      # long swell only: the short chop aliased against the 2.4 D mesh cells (grid of blobs from far above); fine chop is the bump
    cb = N('ShaderNodeCombineXYZ'); L(tot.outputs[0], cb.inputs['Z']); setp = N('GeometryNodeSetPosition'); L(gi.outputs[0], setp.inputs['Geometry']); L(cb.outputs[0], setp.inputs['Offset'])
    sm = N('GeometryNodeSetShadeSmooth'); L(setp.outputs[0], sm.inputs['Geometry']); L(sm.outputs[0], go.inputs[0]); return ng

def graded(a, b, c0, c1, h, grow=1.1):
    xs = list(np.arange(c0, c1 + 1e-6, h)); d = h
    while xs[0] > a: d *= grow; xs.insert(0, max(a, xs[0] - d))
    d = h
    while xs[-1] < b: d *= grow; xs.append(min(b, xs[-1] + d))
    return np.array(xs, 'float64')

def make_ocean(fine=(-260.0, 360.0, -200.0, 220.0), h=2.0, extent=(-1500.0, 1500.0, -1500.0, 1500.0)):
    X = graded(extent[0], extent[1], fine[0], fine[1], h); Y = graded(extent[2], extent[3], fine[2], fine[3], h); nx, ny = len(X), len(Y)
    gx, gy = np.meshgrid(X, Y); vs = np.stack([gx.ravel(), gy.ravel(), np.zeros(nx * ny)], 1); j, i = np.mgrid[0:ny - 1, 0:nx - 1]; a = (j * nx + i).ravel(); b = a + 1; c = a + nx + 1; d = a + nx
    alt = ((i + j) % 2).ravel().astype(bool); t1 = np.where(alt[:, None], np.stack([a, b, c], 1), np.stack([a, b, d], 1)); t2 = np.where(alt[:, None], np.stack([a, c, d], 1), np.stack([b, c, d], 1)); tris = np.concatenate([t1, t2])
    me = bpy.data.meshes.new('ocean'); me.vertices.add(len(vs)); me.vertices.foreach_set('co', vs.astype('float32').ravel()); me.loops.add(len(tris) * 3); me.loops.foreach_set('vertex_index', tris.astype('int32').ravel())
    me.polygons.add(len(tris)); me.polygons.foreach_set('loop_start', np.arange(0, len(tris) * 3, 3, dtype='int32')); me.polygons.foreach_set('loop_total', np.full(len(tris), 3, 'int32')); me.update(); me.validate()
    me.materials.append(water_mat('sea')); ob = bpy.data.objects.new('ocean', me); S['coll'].objects.link(ob); md = ob.modifiers.new('swell', 'NODES'); md.node_group = swell_group(); S['ocean'] = ob
    mb = MB(); R0, R1 = 1100.0, 6000.0; seg = 48                       # flat far disc under the horizon
    for k in range(seg):
        a0, a1 = 2 * math.pi * k / seg, 2 * math.pi * (k + 1) / seg
        mb.face([Vector((R0 * math.cos(a0), R0 * math.sin(a0), -0.6)), Vector((R1 * math.cos(a0), R1 * math.sin(a0), -0.6)), Vector((R1 * math.cos(a1), R1 * math.sin(a1), -0.6)), Vector((R0 * math.cos(a1), R0 * math.sin(a1), -0.6))][::-1], water_mat('sea'), [(0, 0)] * 4)
    mk(mb, 'ocean_far', shadow=False)

# ============================================================================= shared architecture: curved tile roofs, railings, drums, racks
def hip_roof(mb, cx, cy, z0, hx, hy, H, mat, mat_d, lift=0.55, over=0.9, nx=16, ny=10, tilt=0.0):
    """Korean hip roof with concave slopes and up-turned corners (grey tiles). Returns ridge half length."""
    ax, ay = hx + over, hy + over; rl = max(0.0, hx - hy)
    def f(i, j):
        x = -ax + 2 * ax * i / nx; y = -ay + 2 * ay * j / ny; d = min(ax - abs(x), ay - abs(y)); t = max(0.0, min(1.0, d / ay)); cx_ = (abs(x) / ax) ** 5 * (abs(y) / ay) ** 3
        return Vector((cx + x, cy + y, z0 + H * t ** 1.3 + lift * cx_ + 0.25 * (1 - t) ** 3 * 0.0))
    P = quad_grid(mb, f, nx, ny, mat, uvs=lambda i, j: (i / nx * ax * 2 / 3.0, j / ny * ay * 2 / 3.0), orient=lambda c: Vector((0, 0, 1)))
    for (a, b) in [((i, 0), (i + 1, 0)) for i in range(nx)] + [((i, ny), (i + 1, ny)) for i in range(nx)] + [((0, j), (0, j + 1)) for j in range(ny)] + [((nx, j), (nx, j + 1)) for j in range(ny)]:
        p, q = P[a[0]][a[1]], P[b[0]][b[1]]; mb.oface([p, q, q - Vector((0, 0, 0.32)), p - Vector((0, 0, 0.32))], mat_d, [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((p.x - cx, p.y - cy, 0.0)))
    if rl > 0.01: beam(mb, (cx - rl, cy, z0 + H + 0.12), (cx + rl, cy, z0 + H + 0.12), 0.34, 0.3, mat_d)
    for sx in (-1, 1):
        for sy in (-1, 1):
            beam(mb, (cx + sx * rl, cy, z0 + H + 0.1), (cx + sx * (ax - 0.15), cy + sy * (ay - 0.15), z0 + lift * 0.9), 0.24, 0.2, mat_d)
    return rl

def railing(mb, p0, p1, h, mpost, mrail, step=1.5, rail_w=0.09):
    p0, p1 = Vector(p0), Vector(p1); n = max(1, int(round((p1 - p0).length / step)))
    for i in range(n + 1):
        p = p0 + (p1 - p0) * i / n; rod(mb, p, p + Vector((0, 0, h)), 0.075, mpost, seg=5)
    for hh in (h, h * 0.55): beam(mb, p0 + Vector((0, 0, hh)), p1 + Vector((0, 0, hh)), rail_w, rail_w, mrail)

def taiko(mb, c, M_, r=0.95, L=1.5):
    c = Vector(c); beam(mb, c + Vector((-0.9, -0.9, 0)), c + Vector((-0.9, 0.9, 0)), 0.22, 0.22, M_['wood_d']); beam(mb, c + Vector((0.9, -0.9, 0)), c + Vector((0.9, 0.9, 0)), 0.22, 0.22, M_['wood_d'])
    cb = c + Vector((0, 0, 1.25)); mb.frustum(cb + Vector((0, -L / 2, 0)), cb + Vector((0, L / 2, 0)), r * 0.93, r * 0.93, M_['red_l'], seg=14, cap0=False, cap1=False)
    for sg in (-1, 1): mb.frustum(cb + Vector((0, sg * L / 2, 0)), cb + Vector((0, sg * (L / 2 + 0.07), 0)), r * 0.98, r * 0.98, M_['cloth_w'], seg=14)
    for k in (-1, 1): rod(mb, c + Vector((0.9 * k, -0.7, 0)), cb + Vector((0.0, -0.4, 0.1)) , 0.08, M_['wood_d'], seg=5); rod(mb, c + Vector((0.9 * k, 0.7, 0)), cb + Vector((0.0, 0.4, 0.1)), 0.08, M_['wood_d'], seg=5)
    beam(mb, c + Vector((1.5, 0.3, 0.9)), c + Vector((1.9, 0.5, 1.6)), 0.06, 0.06, M_['wood_l']); beam(mb, c + Vector((1.6, -0.3, 0.9)), c + Vector((2.0, -0.5, 1.6)), 0.06, 0.06, M_['wood_l'])

def weapon_rack(mb, c, M_, n=6):
    c = Vector(c); beam(mb, c + Vector((0, -1.6, 0.9)), c + Vector((0, 1.6, 0.9)), 0.12, 0.12, M_['wood_d']); beam(mb, c + Vector((0, -1.6, 1.9)), c + Vector((0, 1.6, 1.9)), 0.12, 0.12, M_['wood_d'])
    for sg in (-1, 1): rod(mb, c + Vector((0, sg * 1.6, 0)), c + Vector((0, sg * 1.6, 2.6)), 0.1, M_['wood_d'], seg=5)
    for i in range(n):
        y = -1.3 + 2.6 * i / (n - 1); p = c + Vector((0, y, 0.0)); top = p + Vector((0.05 * (i % 2), 0, 3.4 if i % 3 else 3.0))
        rod(mb, p + Vector((0, 0, 0.05)), top, 0.055, M_['wood_l'], seg=5); cone(mb, top, top + Vector((0, 0, 0.7)), 0.09, M_['iron'], 4)

def loft(sh, name, L, bfun, zdeck, prof, mat, N=30, mat_deck=None, deck_inset=0.97):
    """Hull loft: stations along x (denser at the ends), section = prof [(frac_of_half_beam, z or ('d', dz))] keel -> gunwale mirrored. Also a deck surface."""
    xs = [-L / 2 + L * (1 - math.cos(math.pi * i / N)) / 2 for i in range(N + 1)]; K = len(prof)
    def zv(z, x): return zdeck(x) + z[1] if isinstance(z, tuple) else z
    def hp(i, j):
        x = xs[i]; k = j if j < K else 2 * K - 1 - j; f, z = prof[k]; return Vector((x, f * bfun(x) * (1 if j < K else -1), zv(z, x)))
    mb = MB(); quad_grid(mb, hp, N, 2 * K - 1, mat, orient=lambda c: Vector((0, c.y, c.z * 0.15 + 0.001)).normalized() if abs(c.y) > 0.05 else Vector((0, 0, -1)))
    ho = mk(mb, name + '_hull', sh['ride'], smooth=True); sh['hull'] = ho
    if mat_deck:
        mb = MB(); quad_grid(mb, lambda i, j: Vector((xs[i], (-1 + 2 * j / 6) * bfun(xs[i]) * deck_inset, zdeck(xs[i]) - 0.02)), N, 6, mat_deck, orient=lambda c: Vector((0, 0, 1))); mk(mb, name + '_deck', sh['ride'])
    return xs

def sail_cloth(mb, top, w, h, bulge, mat, n=8, m=6, normal=(-1, 0, 0), sag=0.0, uvk=1.0):
    top = Vector(top)
    quad_grid(mb, lambda i, j: Vector((top.x - bulge * math.sin(math.pi * j / m) * math.sin(math.pi * min(1.0, (i + 1) / (n + 1))), top.y - w / 2 + w * j / m, top.z - h * i / n)), n, m, mat,
              uvs=lambda i, j: (j / m * uvk, i / n * uvk), orient=lambda c: Vector(normal))

# ============================================================================= Korean PANOKSEON
PL = 30.0
def p_b(x): return 4.5 * math.sqrt(max(0.0, 1 - (abs(x) / (PL / 2)) ** (3.4 if x > 0 else 3.0)))
def p_zd(x): return 2.9 + 1.3 * (abs(x) / (PL / 2)) ** 3.0

def build_panokseon(name, loc, yaw, scale=1.0, sea=True, seed=1, sail_up=True, flag='flag_tri_red', hullc=0, oar_tilt=30):
    M_ = S['M']; r = rnd(seed); sh = new_ship(name, 'panok', PL, 9.0, loc, yaw, scale, sea=sea); sh['seed'] = seed; ride = sh['ride']
    hm = M_['hull_k'] if hullc == 0 else M_['hull_k2']
    loft(sh, name, PL, p_b, p_zd, [(0.0, -1.3), (0.5, -1.25), (0.88, -0.7), (1.0, 0.1), (1.0, 1.5), (1.04, ('d', 0.0))], hm, 28, M_['deck'])
    mb = MB(); X0, X1 = -11.5, 9.5; zc0, zc1 = 2.95, 4.75; zroof = zc1
    for sg in (-1, 1):                                                          # casemate walls: side planks with gun ports
        pts = [(X0 + (X1 - X0) * i / 24) for i in range(25)]
        for i in range(24):
            xa, xb = pts[i], pts[i + 1]; ya, yb = sg * (p_b(xa) * 1.0 + 0.0), sg * (p_b(xb) * 1.0)
            mb.oface([Vector((xa, ya, zc0)), Vector((xb, yb, zc0)), Vector((xb, yb, zc1)), Vector((xa, ya, zc1))], M_['plank_k'], [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((0, sg, 0)))
        for gi in range(5):
            gx = -8.0 + 4.0 * gi; b = p_b(gx) + 0.02
            mb.oface([Vector((gx - 0.55, sg * b, 3.45)), Vector((gx + 0.55, sg * b, 3.45)), Vector((gx + 0.55, sg * b, 4.3)), Vector((gx - 0.55, sg * b, 4.3))], M_['port_dark'], [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((0, sg, 0)))
            for (dx, dz, w_, h_) in ((-0.6, 3.87, 0.1, 0.95), (0.6, 3.87, 0.1, 0.95), (0, 4.33, 1.3, 0.1), (0, 3.42, 1.3, 0.1)): cbox(mb, (gx + dx, sg * (b + 0.04), dz), w_ / 2 + 0.02, 0.06, h_ / 2, M_['red_d'])
            sh['guns'].append(dict(local=Vector((gx, sg * (b + 0.7), 3.9)), dir=Vector((0, sg, 0.1)).normalized(), name='%s_g%d%s' % (name, gi, 'p' if sg > 0 else 's')))
    for (xe, sg_) in ((X0, -1), (X1, 1)): mb.oface([Vector((xe, -p_b(xe), zc0)), Vector((xe, p_b(xe), zc0)), Vector((xe, p_b(xe), zc1)), Vector((xe, -p_b(xe), zc1))], M_['plank_k'], [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((sg_, 0, 0)))
    for sg in (-1, 1):
        for i in range(24):
            xa, xb = X0 + (X1 - X0) * i / 24, X0 + (X1 - X0) * (i + 1) / 24; beam(mb, (xa, sg * (p_b(xa) + 0.12), zc1 + 0.12), (xb, sg * (p_b(xb) + 0.12), zc1 + 0.12), 0.34, 0.34, M_['dancheong'])
    mk(mb, name + '_case', ride)
    mb = MB(); quad_grid(mb, lambda i, j: Vector((X0 - 0.3 + (X1 - X0 + 0.6) * i / 10, (-1 + 2 * j / 4) * (p_b(X0 - 0.3 + (X1 - X0 + 0.6) * i / 10) + 0.18), zroof + 0.05)), 10, 4, M_['deck'], orient=lambda c: Vector((0, 0, 1)))   # flat top deck
    for sg in (-1, 1): railing(mb, (X0, sg * (p_b(X0) + 0.1), zroof), (X1, sg * (p_b(X1) + 0.1), zroof), 1.0, M_['green_p'], M_['red_d'], 1.6)
    railing(mb, (X0, -p_b(X0) - 0.1, zroof), (X0, p_b(X0) + 0.1, zroof), 1.0, M_['green_p'], M_['red_d'], 1.6); railing(mb, (X1, -p_b(X1) - 0.1, zroof), (X1, p_b(X1) + 0.1, zroof), 1.0, M_['green_p'], M_['red_d'], 1.6)
    mk(mb, name + '_top', ride)
    for sg in (-1, 1):                                                          # bulwark on the bow deck + stern platform
        mb = MB(); xs = [X1 + 0.2 + i * (PL / 2 - X1 - 0.5) / 6 for i in range(7)]
        for i in range(6):
            a, b = xs[i], xs[i + 1]; mb.oface([Vector((a, sg * p_b(a) * 1.02, p_zd(a))), Vector((b, sg * p_b(b) * 1.02, p_zd(b))), Vector((b, sg * p_b(b) * 1.02, p_zd(b) + 0.9)), Vector((a, sg * p_b(a) * 1.02, p_zd(a) + 0.9))], M_['green_p'], [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((0, sg, 0)))
        mk(mb, '%s_bul%d' % (name, sg), ride)
    # deck pavilion (hip-roofed): red pillars, green + red dancheong beams, railing, tiled roof
    mb = MB(); hx_, hy_ = 3.8, 2.6; cxh = -1.0; zb = zroof + 0.05
    for px in (-hx_, 0.0, hx_):
        for py in (-hy_, hy_): rod(mb, (cxh + px, py, zb), (cxh + px, py, zb + 2.7), 0.17, M_['red'], seg=6); cbox(mb, (cxh + px, py, zb + 2.78), 0.3, 0.3, 0.1, M_['green_p'])
    for py in (-hy_, hy_): beam(mb, (cxh - hx_ - 0.3, py, zb + 2.55), (cxh + hx_ + 0.3, py, zb + 2.55), 0.5, 0.45, M_['dancheong']); railing(mb, (cxh - hx_, py, zb), (cxh + hx_, py, zb), 0.85, M_['red'], M_['wood_d'], 2.0)
    for px in (-hx_, hx_): beam(mb, (cxh + px, -hy_ - 0.3, zb + 2.55), (cxh + px, hy_ + 0.3, zb + 2.55), 0.5, 0.45, M_['dancheong']); railing(mb, (cxh + px, -hy_, zb), (cxh + px, hy_, zb), 0.85, M_['red'], M_['wood_d'], 2.0)
    cbox(mb, (cxh, 0, zb + 0.02), hx_, hy_, 0.04, M_['deck'])
    hip_roof(mb, cxh, 0, zb + 2.6, hx_, hy_, 1.9, M_['tile'], M_['tile_d'], 0.4, 0.8, 12, 8); mk(mb, name + '_house', ride, smooth=False)
    sh['house_top'] = (cxh, 0, zb + 2.6 + 1.9)
    # oars
    ox = [-9.0 + 2.25 * i for i in range(9)]; oar_set(sh, ox, [p_b(x) + 0.05 for x in ox], 1.5, length_out=6.8, dip=sea, stroke=sea, tilt_deg=oar_tilt, stow=not sea)
    # masts, matting sails, flags
    for mi, (mx, zbm, Hm, sw_, sh_) in enumerate(((4.5, zroof, 14.0, 8.4, 7.2), (11.0, p_zd(11.0), 10.5, 5.4, 4.6))):
        mb = MB(); rod(mb, (mx, 0, zbm), (mx, 0, zbm + Hm), 0.26, M_['wood_l'], seg=8, r1=0.15); ytop = zbm + Hm - 0.7
        beam(mb, (mx - 0.35, -sw_ / 2 - 0.5, ytop), (mx - 0.35, sw_ / 2 + 0.5, ytop), 0.16, 0.16, M_['wood_l'])
        for sg in (-1, 1): rod(mb, (mx, 0, zbm + Hm - 0.3), (mx + 2.5 * (1 if mi == 0 else -1), sg * 4.0, zbm + 0.6), 0.03, M_['rope'], seg=4)
        mk(mb, '%s_mast%d' % (name, mi), ride); sh['masts'].append((mx, zbm, Hm))
        if sail_up:
            mb = MB(); sail_cloth(mb, (mx - 0.45, 0, ytop - 0.1), sw_, sh_ * (0.95 if r.random() > 0.5 else 1.0), 1.1, M_['sail_k'], 8, 8, uvk=1.2); mk(mb, '%s_sail%d' % (name, mi), ride, smooth=True)
        flag_obj(sh, flag if mi == 0 else 'flag_tri_black', (mx, 0, zbm + Hm), 0.6, 2.4, 0.15, pole=False, name='%s_pen%d' % (name, mi), ph=mi + seed)
    flag_obj(sh, 'flag_red' if seed % 2 else 'flag_black', (-PL / 2 + 1.0, 0, p_zd(-PL / 2 + 1.0)), 5.2, 3.0, 0.3, name=name + '_stern', ph=seed)
    flag_obj(sh, 'flag_black' if seed % 2 else 'flag_red', (PL / 2 - 0.8, 0, p_zd(PL / 2 - 0.8)), 3.8, 2.2, 0.2, name=name + '_bow', ph=seed + 2)
    mk(MB(), name + '_x', ride) if False else None
    if sea: wake_foam(sh, True, True)
    return sh

# ============================================================================= Japanese ATAKEBUNE (castle ship) and SEKIBUNE (rowed)
def a_b(L, Bh):
    return lambda x: Bh * math.sqrt(max(0.0, 1 - (abs(x) / (L / 2)) ** (2.5 if x > 0 else 3.4)))

def build_atakebune(name, loc, yaw, scale=1.0, sea=True, seed=1, flagship=False, sail=False, towerh=1.0, banners=4, band='#a8201f', hull_hex='#1b181a', roof_dark=False, oar_tilt=28):
    """Atakebune: brown plank hull, tall boxy wooden fighting wall with a few black / red lacquer panels, castle (yagura) of dark wood with small plaster panels, curved tiled roofs, gold ridge ends, mon nobori."""
    M_ = S['M']; r = rnd(seed); L = 26.0 + r.uniform(-2.5, 3.0); Bh = 5.0 + r.uniform(-0.4, 0.6); sh = new_ship(name, 'atake', L, 2 * Bh, loc, yaw, scale, sea=sea); ride = sh['ride']; sh['seed'] = seed
    bf = a_b(L, Bh); lac = M_['black_l'] if seed % 3 else M_['red_l']; wallm = M_['wall_w']
    loft(sh, name, L, bf, lambda x: 2.4, [(0.0, -1.2), (0.55, -1.15), (0.9, -0.5), (1.0, 0.1), (1.0, 1.0), (1.02, 2.4)], M_['hull_a'] if seed % 2 else M_['hull_dk'], 26, M_['deck'])
    mb = MB(); z0, z1 = 2.4, 5.4; zt = z1; ins = 0.55; wx0, wx1 = -L / 2 + 1.8, L / 2 - 2.2
    def wb(x): return bf(x) - ins
    UV = [(0, 0), (1, 0), (1, 1), (0, 1)]
    for sg in (-1, 1):                                                              # fighting wall: brown planks, lacquer panels now and then, loopholes
        xs = [wx0 + (wx1 - wx0) * i / 14 for i in range(15)]
        for i in range(14):
            a, b = xs[i], xs[i + 1]; ya, yb = sg * wb(a), sg * wb(b); n = Vector((0, sg, 0))
            mb.oface([Vector((a, ya, z0)), Vector((b, yb, z0)), Vector((b, yb, z1)), Vector((a, ya, z1))], wallm, UV, n)
            if i % 3 == 1:
                ya2, yb2 = sg * (wb(a) + 0.03), sg * (wb(b) + 0.03); mb.oface([Vector((a + 0.12, ya2, z0 + 0.5)), Vector((b - 0.12, yb2, z0 + 0.5)), Vector((b - 0.12, yb2, z1 - 0.45)), Vector((a + 0.12, ya2, z1 - 0.45))], lac, UV, n)
            xm = (a + b) / 2; ym = sg * (wb(xm) + 0.04); cbox(mb, (xm, ym, z0 + 1.85), 0.24, 0.03, 0.22, M_['port_dark'])
        beam(mb, Vector((wx0, sg * wb(wx0), z1 - 0.1)), Vector((wx1, sg * wb(wx1), z1 - 0.1)), 0.22, 0.28, M_['wood_d'])
    for sx_ in (wx0, wx1):
        sgx = -1 if sx_ == wx0 else 1; yy_ = wb(sx_); mb.oface([Vector((sx_, -yy_, z0)), Vector((sx_, yy_, z0)), Vector((sx_, yy_, z1)), Vector((sx_, -yy_, z1))], wallm, UV, Vector((sgx, 0, 0)))
    mk(mb, name + '_wall', ride)
    mb = MB(); quad_grid(mb, lambda i, j: Vector((wx0 + (wx1 - wx0) * i / 8, (-1 + 2 * j / 4) * wb(wx0 + (wx1 - wx0) * i / 8), zt + 0.04)), 8, 4, M_['deck'], orient=lambda c: Vector((0, 0, 1)))   # upper deck
    for sg in (-1, 1): railing(mb, (wx0, sg * wb(wx0), zt), (wx1, sg * wb(wx1), zt), 0.95, M_['wood_d'], M_['wood_d'], 1.5)
    railing(mb, (wx1, -wb(wx1), zt), (wx1, wb(wx1), zt), 0.95, M_['wood_d'], M_['wood_d'], 1.5)
    # castle (yagura): two boxy dark-wood storeys, a tiled skirt roof, a tiled hip roof, gold ridge ends
    tx0 = wx0 + 0.6; tw = 6.4; td = 2 * (wb(tx0 + 3)) * 0.78; tz0 = zt; tz1 = zt + 3.2 * towerh; tcx = tx0 + tw / 2; tdk = M_['tile_d'] if roof_dark else M_['tile']
    cbox(mb, (tcx, 0, (tz0 + tz1) / 2), tw / 2, td / 2, (tz1 - tz0) / 2, wallm)
    for px in (-tw / 2, tw / 2):
        for py in (-td / 2, td / 2): rod(mb, (tcx + px, py, tz0), (tcx + px, py, tz1), 0.15, M_['wood_d'], seg=5)
    for sg in (-1, 1):
        for k in range(3):
            xk = tcx - 2.0 + 2.0 * k; cbox(mb, (xk, sg * (td / 2 + 0.03), (tz0 + tz1) / 2 + 0.3), 0.42, 0.04, 0.38, M_['port_dark'])
            if (k + seed) % 2 == 0: cbox(mb, (xk, sg * (td / 2 + 0.03), tz0 + 0.75), 0.5, 0.03, 0.22, M_['plaster'])          # small plaster panel under the window
    cbox(mb, (tcx + tw / 2 + 0.03, 0, (tz0 + tz1) / 2), 0.04, 0.9, 1.1, M_['port_dark'])
    hip_roof(mb, tcx, 0, tz1, tw / 2 + 0.1, td / 2 + 0.05, 1.0, tdk, M_['tile_d'], 0.45, 0.8, 12, 8)
    zb2 = tz1 + 0.75; z2 = zb2 + 1.9 * towerh; tw2, td2 = tw * 0.66, td * 0.68
    cbox(mb, (tcx, 0, (zb2 + z2) / 2), tw2 / 2, td2 / 2, (z2 - zb2) / 2, wallm)
    for px in (-tw2 / 2, tw2 / 2):
        for py in (-td2 / 2, td2 / 2): rod(mb, (tcx + px, py, zb2), (tcx + px, py, z2), 0.13, M_['wood_d'], seg=5)
    for sg in (-1, 1):
        for k in range(2): cbox(mb, (tcx - 0.9 + 1.8 * k, sg * (td2 / 2 + 0.03), (zb2 + z2) / 2), 0.4, 0.04, 0.4, M_['port_dark'])
    cbox(mb, (tcx + tw2 / 2 + 0.03, 0, (zb2 + z2) / 2), 0.04, 0.7, 0.45, M_['port_dark'])
    rl = hip_roof(mb, tcx, 0, z2, tw2 / 2, td2 / 2, 1.9, tdk, M_['tile_d'], 0.65, 0.8, 12, 8)
    for sx in (-1, 1): cone(mb, (tcx + sx * (rl + 0.1), 0, z2 + 1.95), (tcx + sx * (rl + 0.55), 0, z2 + 2.75), 0.22, M_['gold'], 5)
    sh['tower_top'] = Vector((tcx, 0, z2 + 1.9)); sh['deck_z'] = zt + 0.04; sh['deck_x'] = (tx0 + tw + 0.5, wx1 - 0.5)
    if flagship: taiko(mb, (wx1 - 2.0, -3.0, zt + 0.04), M_); weapon_rack(mb, (wx1 - 1.5, 3.2, zt + 0.04), M_, 6)
    mk(mb, name + '_upper', ride)
    if name == 'j_board':                                                              # boarding ladder hooked over the rail, hanging out toward the turtle ship
        xl = sh['deck_x'][0] + 6.4; mb = MB(); yr = wb(xl); zr = zt + 0.95
        for sgx in (-0.38, 0.38):
            rod(mb, (xl + sgx, yr - 0.15, zr + 0.25), (xl + sgx, yr + 0.15, zr), 0.06, M_['wood_l'], seg=5); rod(mb, (xl + sgx, yr + 0.15, zr), (xl + sgx, yr + 1.5, zr - 4.2), 0.06, M_['wood_l'], seg=5)
        for k in range(1, 9):
            t = k / 9.0; p = Vector((xl, yr + 0.15 + 1.35 * t, zr - 4.2 * t)); rod(mb, p + Vector((-0.4, 0, 0)), p + Vector((0.4, 0, 0)), 0.045, M_['wood_d'], seg=5)
        mk(mb, name + '_ladder', ride)
    bpos = [(wx1 - 0.3, -wb(wx1) + 0.5), (wx1 - 0.3, wb(wx1) - 0.5), (tx0 + 0.1, -wb(tx0) + 0.5), (tx0 + 0.1, wb(tx0) - 0.5), (wx1 - 5.0, -wb(wx1 - 5.0) + 0.4), (wx1 - 5.0, wb(wx1 - 5.0) - 0.4)][:banners]
    mons = ['flag_nob_circle', 'flag_nob_diamond', 'flag_nob_rcircle']
    for bi, (bx_, by_) in enumerate(bpos): flag_obj(sh, 'flag_nob_circle' if flagship else mons[(bi + seed) % 3], (bx_, by_, zt), 6.0 + r.uniform(0, 1.4), 1.0, name='%s_nobori%d' % (name, bi), vertical=True, ph=bi + seed)
    flag_obj(sh, 'flag_tri_black', (tcx, 0, z2 + 2.75), 1.6, 2.2, 0.15, name=name + '_topflag', ph=seed)
    mx = L / 2 - 4.0
    if not flagship: mb = MB(); rod(mb, (mx, 0, zt), (mx, 0, zt + 10.0), 0.22, M_['wood_l'], seg=8, r1=0.14); beam(mb, (mx, -3.6, zt + 8.8), (mx, 3.6, zt + 8.8), 0.14, 0.14, M_['wood_l']); mk(mb, name + '_mast', ride); sh['masts'].append((mx, zt, 10.0))
    if sail and not flagship:
        mb = MB(); sail_cloth(mb, (mx - 0.3, 0, zt + 8.7), 7.2, 6.8, 1.0, M_['sail_c'], 8, 8); mk(mb, name + '_sail', ride, smooth=True)
    ox = [-5.0 + 2.5 * i for i in range(7)]; oar_set(sh, ox, [bf(x) + 0.05 for x in ox], 1.3, length_out=6.2, dip=sea, stroke=sea, tilt_deg=oar_tilt, stow=not sea)
    if sea: wake_foam(sh, True, True)
    return sh

def build_sekibune(name, loc, yaw, scale=1.0, sea=True, seed=1, sail=False, shield=0, banner='flag_nob_circle', oar_tilt=25):
    """Sekibune: slender brown plank hull, shield boards (tate) of planks and lacquer, a small dark-wood cabin with a tiled roof, mon nobori, optional square cloth sail."""
    M_ = S['M']; r = rnd(seed); L = 15.0 + r.uniform(-1.5, 2.0); Bh = 1.9 + r.uniform(-0.15, 0.25); sh = new_ship(name, 'seki', L, 2 * Bh, loc, yaw, scale, sea=sea); ride = sh['ride']; sh['seed'] = seed
    bf = lambda x: Bh * math.sqrt(max(0.0, 1 - (abs(x) / (L / 2)) ** 2.6)); zd = lambda x: 1.5 + 0.7 * (abs(x) / (L / 2)) ** 3
    loft(sh, name, L, bf, zd, [(0.0, -0.9), (0.5, -0.85), (0.9, -0.3), (1.0, 0.1), (1.0, ('d', -0.2)), (1.04, ('d', 0.0))], M_['hull_a'] if seed % 2 else M_['hull_dk'], 20, M_['deck'])
    mb = MB(); lacs = [M_['black_l'], M_['red_l'], M_['plank']][shield % 3]
    for sg in (-1, 1):
        n = 9
        for i in range(n):
            a, b = -L / 2 + 2.2 + (L - 4.4) * i / n, -L / 2 + 2.2 + (L - 4.4) * (i + 0.9) / n; ya, yb = sg * (bf(a) * 1.0), sg * (bf(b) * 1.0)
            mb.oface([Vector((a, ya, zd(a))), Vector((b, yb, zd(b))), Vector((b, yb, zd(b) + 1.2)), Vector((a, ya, zd(a) + 1.2))], lacs if i % 3 == 1 else M_['wall_w'], [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((0, sg, 0)))
    cx_ = L / 2 - 4.2; cbox(mb, (cx_, 0, zd(cx_) + 1.0), 2.0, Bh * 0.78, 1.0, M_['wall_w']); cbox(mb, (cx_ + 2.02, 0, zd(cx_) + 1.0), 0.03, 0.5, 0.35, M_['port_dark'])
    hip_roof(mb, cx_, 0, zd(cx_) + 2.0, 2.0, Bh * 0.78, 0.9, M_['tile_d'], M_['tile_d'], 0.3, 0.5, 8, 6)
    mk(mb, name + '_fit', ride)
    ox = [-4.8 + 2.0 * i for i in range(6)]; oar_set(sh, ox, [bf(x) + 0.04 for x in ox], 1.2, length_out=5.2, dip=sea, stroke=sea, tilt_deg=oar_tilt, stow=not sea)
    flag_obj(sh, banner, (-L / 2 + 1.4, 0, zd(-L / 2 + 1.4)), 5.0 + r.uniform(0, 1.2), 0.9, name=name + '_nobori', vertical=True, ph=seed)
    if sail:
        mx = 1.0; mb = MB(); rod(mb, (mx, 0, zd(mx)), (mx, 0, zd(mx) + 7.5), 0.16, M_['wood_l'], seg=6, r1=0.1); beam(mb, (mx, -2.6, zd(mx) + 6.8), (mx, 2.6, zd(mx) + 6.8), 0.1, 0.1, M_['wood_l']); mk(mb, name + '_mast', ride)
        mb = MB(); sail_cloth(mb, (mx - 0.2, 0, zd(mx) + 6.7), 5.0, 4.6, 0.8, M_['sail_c'], 6, 6); mk(mb, name + '_sail', ride, smooth=True)
    flag_obj(sh, 'flag_tri_black' if seed % 3 else 'flag_tri_yellow', (L / 2 - 0.7, 0, zd(L / 2 - 0.7)), 2.2, 1.4, 0.1, name=name + '_bow', ph=seed)
    if sea: wake_foam(sh, False, False)
    return sh


# ============================================================================= YARD (Joseon naval yard, Yeosu): constants and ship-to-world map
Z_LAND = 2.2; Z_Q = 2.25; Y_SH = -3.5; THETA = math.radians(7.0); WY0 = -1.5; WZ0 = 2.56; CELL = 3.5
TRENCH = (-7.0, 7.0, -17.5, Y_SH)                     # x0, x1, y0, y1 : the slipway cut in the land
def yw(l):
    """Ship-local point (x fwd, y starboard, z up) of the turtle ship on the slipway -> world (the root yaws 90 deg: ship +x = world +y, ship +y = world -x)."""
    x, y, z = l; sx = x * math.cos(THETA) + z * math.sin(THETA); sz = -x * math.sin(THETA) + z * math.cos(THETA); return Vector((-y, WY0 + sx, WZ0 + sz))
def ramp_z(Y): s = Y - WY0; return WZ0 - s * math.tan(THETA) - 1.55 / math.cos(THETA) - 0.85

FORT = (-70.0, -135.0); FORT_H = 36.0
def LH(x, y):
    """Land height: the yard is flat at Z_LAND; hills rise behind (y < -70); the fortress hill (flat plateau r < 32) at FORT; side ridges."""
    def ss(a, b, v): t = max(0.0, min(1.0, (v - a) / (b - a))); return t * t * (3 - 2 * t)
    up = 40 * ss(-80, -280, y) * (0.65 + 0.35 * (0.5 + 0.5 * math.sin(0.021 * x + 1.0))) + 24 * ss(110, 300, abs(x)) * ss(-20, -140, y)
    d = math.hypot(x - FORT[0], y - FORT[1]); fort = FORT_H * (1.0 if d < 32 else math.exp(-((d - 32) / 24.0) ** 2))
    if d < 32: up = 40 * ss(-80, -280, FORT[1]) * 0.8
    return Z_LAND + up + fort + 3.0 * hfield(x * 0.35, y * 0.35, 3) * ss(-60, -150, y) * (0 if d < 32 else 1) + 0.8 * hfield(x * 0.9, y * 0.9, 1) * ss(-50, -90, y) * (0 if d < 32 else 1)
LH2 = LH

def terrain_mat():
    def f(b):
        gp = b.n('ShaderNodeNewGeometry'); xyz = b.n('ShaderNodeSeparateXYZ'); b.l(gp.outputs['Position'], xyz.inputs[0]); nz = b.n('ShaderNodeSeparateXYZ'); b.l(gp.outputs['True Normal'], nz.inputs[0])
        n1 = b.noise(0.12, 4.0, 0.6); n2 = b.noise(1.2, 3.0, 0.5)
        dist = b.math('SQRT', b.math('ADD', b.math('MULTIPLY', b.math('SUBTRACT', xyz.outputs['X'], 0.0), b.math('SUBTRACT', xyz.outputs['X'], 0.0)), b.math('MULTIPLY', b.math('SUBTRACT', xyz.outputs['Y'], -30.0), b.math('SUBTRACT', xyz.outputs['Y'], -30.0))))
        earth = b.mix(b.rng(n2, 0.3, 0.7), hexl('#8c7656'), hexl('#6f5d44')); grass = b.mix(b.rng(n1, 0.3, 0.7), hexl('#6f9246'), hexl('#4f7a38')); rock = b.mix(b.rng(n2, 0.3, 0.7), hexl('#85796a'), hexl('#5c5448'))
        col = b.mix(b.rng(dist, 60, 100), earth, grass); col = b.mix(b.rng(nz.outputs['Z'], 0.6, 0.8), rock, col)
        b.princ(col, 0.93, 0.0, b.bump(b.math('ADD', n1, n2), 0.5, 0.2))
    return mat('J_terrain', f)

def build_terrain():
    xs = np.arange(-350.0, 350.0 + 1e-6, CELL); ys = np.arange(-420.0, Y_SH + 1e-6, CELL); vs = []; idx = {}
    for j, y in enumerate(ys):
        for i, x in enumerate(xs): idx[(i, j)] = len(vs); vs.append((x, y, LH2(x, y)))
    fs = []
    for j in range(len(ys) - 1):
        for i in range(len(xs) - 1):
            cx_, cy_ = (xs[i] + xs[i + 1]) / 2, (ys[j] + ys[j + 1]) / 2
            if TRENCH[0] < cx_ < TRENCH[1] and TRENCH[2] < cy_ < TRENCH[3]: continue
            fs.append((idx[(i, j)], idx[(i + 1, j)], idx[(i + 1, j + 1)], idx[(i, j + 1)]))
    me = bpy.data.meshes.new('terrain'); me.from_pydata(vs, [], fs); me.update(); [setattr(p, 'use_smooth', True) for p in me.polygons]; me.materials.append(terrain_mat())
    ob = bpy.data.objects.new('terrain', me); S['coll'].objects.link(ob); S['terrain_h'] = LH2; return ob

def build_slipway(M_):
    """Stone-walled trench, ramp slab running down into the water, guide piles, west embankment wall, east wharf over the water, piles."""
    mb = MB(); x0, x1, y0, y1 = TRENCH; Ye = 9.0
    quad_grid(mb, lambda i, j: Vector((x0 + (x1 - x0) * i / 4, y0 + (Ye - y0) * j / 20, ramp_z(y0 + (Ye - y0) * j / 20))), 4, 20, M_['stone_d'], orient=lambda c: Vector((0, 0, 1)))
    for sx in (x0, x1):                                                  # trench walls (stone) from the ramp up to the land
        for j in range(20):
            ya, yb = y0 + (Ye - y0) * j / 20, y0 + (Ye - y0) * (j + 1) / 20
            if yb > y1 + 0.01: break
            mb.oface([Vector((sx, ya, ramp_z(ya))), Vector((sx, yb, ramp_z(yb))), Vector((sx, yb, Z_LAND)), Vector((sx, ya, Z_LAND))], M_['stone'], [(ya / 3, 0), (yb / 3, 0), (yb / 3, 1), (ya / 3, 1)], Vector((-1 if sx == x1 else 1, 0, 0)))
    mb.oface([Vector((x0, y0, ramp_z(y0))), Vector((x1, y0, ramp_z(y0))), Vector((x1, y0, Z_LAND)), Vector((x0, y0, Z_LAND))], M_['stone'], [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((0, 1, 0)))
    mb.oface([Vector((-9, Y_SH, -1.8)), Vector((x0, Y_SH, -1.8)), Vector((x0, Y_SH, Z_LAND)), Vector((-9, Y_SH, Z_LAND))], M_['stone'], [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((0, 1, 0)))
    mk(mb, 'slipway', smooth=False)
    mb = MB()                                                            # west embankment wall + coping, quay wall left of the slip
    mb.oface([Vector((-352, Y_SH, -1.8)), Vector((x0, Y_SH, -1.8)), Vector((x0, Y_SH, Z_LAND)), Vector((-352, Y_SH, Z_LAND))], M_['stone'], [(0, 0), (60, 0), (60, 1), (0, 1)], Vector((0, 1, 0)))
    cbox(mb, (-180, Y_SH - 0.1, Z_LAND + 0.1), 172, 0.5, 0.12, M_['stone_d'])
    mb.oface([Vector((7.0, Y_SH, -1.8)), Vector((352, Y_SH, -1.8)), Vector((352, Y_SH, Z_LAND)), Vector((7.0, Y_SH, Z_LAND))], M_['stone'], [(0, 0), (60, 0), (60, 1), (0, 1)], Vector((0, 1, 0)))
    mk(mb, 'embankment', smooth=False)
    # east wharf: L-shaped timber quay (deck + fascia + piles) ; west landing stage
    mb = MB(); WX0, WX1, WY1 = 7.4, 17.0, 21.0
    cbox(mb, ((WX0 + WX1) / 2, (-16 + WY1) / 2, Z_Q - 0.12), (WX1 - WX0) / 2, (WY1 + 16) / 2, 0.12, M_['deck'])
    for yy in range(-14, int(WY1) + 1, 3):
        for xx in (WX0 + 0.4, WX1 - 0.4):
            if yy >= Y_SH - 0.1: rod(mb, (xx, yy, -2.2), (xx, yy, Z_Q + 0.25), 0.2, M_['wood_d'], seg=6)
    beam(mb, (WX1, Y_SH, Z_Q + 0.2), (WX1, WY1, Z_Q + 0.2), 0.3, 0.3, M_['wood_d']); beam(mb, (WX0, WY1, Z_Q + 0.2), (WX1, WY1, Z_Q + 0.2), 0.3, 0.3, M_['wood_d'])
    for yy in range(0, int(WY1), 4): rod(mb, (WX1 - 0.15, yy, Z_Q), (WX1 - 0.15, yy, Z_Q + 0.55), 0.22, M_['wood_d'], seg=6)          # bollards
    cbox(mb, (-12.0, 2.0, Z_Q - 0.12), 5.0, 5.8, 0.12, M_['deck'])
    for yy in (-3, 1, 5, 7.5):
        for xx in (-16.6, -7.4): rod(mb, (xx, yy, -2.2), (xx, yy, Z_Q + 0.2), 0.2, M_['wood_d'], seg=6)
    mk(mb, 'wharf', smooth=False); S['wharf'] = (WX0, WX1, WY1)
    mb = MB()                                                            # guide piles along the ramp, in the water
    for yy in (0.0, 4.0, 8.0): 
        for sx in (-7.6, 7.6): rod(mb, (sx, yy, -2.5), (sx, yy, 1.4), 0.24, M_['wood_d'], seg=6)
    mk(mb, 'guide_piles', smooth=False)

def build_cradles(M_, sh):
    """Cradle timbers under the keel (world-fixed), sliding rails on the ramp, and slanted shores to both sides of the hull."""
    mb = MB()
    for sx in (-1.7, 1.7):                                               # sliding ways along the ramp (world, parallel to the keel line)
        for ya in range(-26, 6, 2):
            Y0, Y1 = float(ya), float(ya + 2); g0 = min(Z_LAND, ramp_z(Y0)) if Y0 > Y_SH - 14 else Z_LAND; g1 = min(Z_LAND, ramp_z(Y1)) if Y1 > Y_SH - 14 else Z_LAND
            beam(mb, (sx, Y0, g0 + 0.2), (sx, Y1, g1 + 0.2), 0.5, 0.4, M_['wood_d'])
    for k in range(-16, 17, 4):
        kp = yw((k, 0, -1.55)); Y = kp.y; g = (min(Z_LAND, ramp_z(Y)) if Y > -17.5 else Z_LAND); h = kp.z - g
        if h < 0.2: continue
        for sx in (-1.7, 1.7): cbox(mb, (sx, Y, g + 0.4 + (h - 0.4) / 2), 0.5, 0.7, (h - 0.4) / 2 + 0.02, M_['wood_l'])
        cbox(mb, (0, Y, kp.z - 0.3), 2.3, 0.65, 0.3, M_['wood_d']); beam(mb, (-2.6, Y, g + 0.8), (2.6, Y, g + 0.8), 0.45, 0.35, M_['wood_d'])
    for x in (-12.0, -6.0, 0.0, 6.0, 12.0):                              # shores: slanted timbers hull -> ground on both sides
        for sg in (-1, 1):
            hp = yw((x, sg * (t_b(x) * 0.99), 0.4)); Y = hp.y; gx = (7.0 if sg < 0 else -7.0) if (TRENCH[2] < Y < TRENCH[3]) else (-1 if sg < 0 else 1) * 0 + (8.5 if sg < 0 else -8.5); gz = Z_LAND
            if Y > TRENCH[3]: continue
            beam(mb, hp, Vector((gx, Y, gz + 0.05)), 0.42, 0.42, M_['wood_l'])
    mk(mb, 'cradles', smooth=False)

# ============================================================================= buildings
def hanok(name, cx, cy, W, D, yaw, wallh=3.2, roofH=2.6, z0=Z_LAND, M_=None, dark_roof=False, open_front=False, seed=1):
    """Workshop shed: stone plinth, dark posts, plaster + lattice walls, big door, grey tiled hip roof with up-turned eaves."""
    M_ = M_ or S['M']; r = rnd(seed); mb = MB(); hx, hy = W / 2, D / 2
    cbox(mb, (0, 0, z0 + 0.25 - z0), hx + 0.4, hy + 0.4, 0.25, M_['stone_d']); zb = 0.5
    for px in np.linspace(-hx, hx, int(W / 2.6) + 2):
        for py in (-hy, hy): rod(mb, (px, py, zb), (px, py, zb + wallh), 0.17, M_['wood_d'], seg=6)
    for py in np.linspace(-hy, hy, int(D / 2.6) + 2):
        for px in (-hx, hx): rod(mb, (px, py, zb), (px, py, zb + wallh), 0.17, M_['wood_d'], seg=6)
    for sg in (-1, 1):
        mb.oface([Vector((-hx, sg * hy, zb)), Vector((hx, sg * hy, zb)), Vector((hx, sg * hy, zb + wallh)), Vector((-hx, sg * hy, zb + wallh))], M_['plaster'], [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((0, sg, 0)))
        mb.oface([Vector((sg * hx, -hy, zb)), Vector((sg * hx, hy, zb)), Vector((sg * hx, hy, zb + wallh)), Vector((sg * hx, -hy, zb + wallh))], M_['plaster'], [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((sg, 0, 0)))
        beam(mb, (-hx, sg * (hy + 0.02), zb + wallh - 0.1), (hx, sg * (hy + 0.02), zb + wallh - 0.1), 0.3, 0.26, M_['red']); beam(mb, (-hx, sg * (hy + 0.02), zb + 0.9), (hx, sg * (hy + 0.02), zb + 0.9), 0.14, 0.12, M_['wood_d'])
    nwin = max(2, int(W / 4.0))
    for k in range(nwin):
        px = -hx + (k + 0.5) * W / nwin
        if k == nwin // 2 and not open_front: cbox(mb, (px, -hy - 0.05, zb + 1.35), 1.2, 0.06, 1.35, M_['wood_l']); cbox(mb, (px, -hy - 0.1, zb + 1.35), 0.04, 0.04, 1.3, M_['wood_d'])
        else:
            cbox(mb, (px, -hy - 0.05, zb + 1.9), 0.75, 0.05, 0.65, M_['wood_d']); cbox(mb, (px, -hy - 0.08, zb + 1.9), 0.62, 0.03, 0.52, M_['plaster'])
            for q in (-0.31, 0.0, 0.31): cbox(mb, (px + q, -hy - 0.1, zb + 1.9), 0.025, 0.02, 0.52, M_['wood_d'])
    hip_roof(mb, 0, 0, zb + wallh, hx, hy, roofH, M_['tile_d'] if dark_roof else M_['tile'], M_['tile_d'], 0.6, 1.1, 18, 10)
    ob = mk(mb, name, smooth=False); ob.location = (cx, cy, z0 - 0.0); ob.rotation_euler = (0, 0, math.radians(yaw)); return ob

def pavilion(name, cx, cy, yaw, W=11.0, D=8.0, M_=None):
    """Open pavilion with red pillars, dancheong-painted beams (red / blue / green) and a curved tiled roof, on a stone platform with steps."""
    M_ = M_ or S['M']; mb = MB(); hx, hy = W / 2, D / 2; zp = 0.9
    cbox(mb, (0, 0, 0.45), hx + 1.0, hy + 1.0, 0.45, M_['stone']); cbox(mb, (0, -hy - 1.8, 0.3), 2.2, 0.9, 0.3, M_['stone']); cbox(mb, (0, -hy - 1.2, 0.6), 2.2, 0.6, 0.3, M_['stone'])
    cbox(mb, (0, 0, zp + 0.05), hx + 0.6, hy + 0.6, 0.05, M_['deck'])
    for px in np.linspace(-hx, hx, 4):
        for py in (-hy, hy):
            rod(mb, (px, py, zp), (px, py, zp + 4.2), 0.36, M_['red'], seg=10); cbox(mb, (px, py, zp + 4.3), 0.55, 0.55, 0.12, M_['green_p'])
            cbox(mb, (px, py, zp + 4.55), 0.8, 0.8, 0.12, M_['blue_p']); cbox(mb, (px, py, zp + 4.8), 1.05, 1.05, 0.12, M_['red'])
    for py in (-hy, hy): beam(mb, (-hx - 0.7, py, zp + 4.1), (hx + 0.7, py, zp + 4.1), 0.7, 0.7, M_['dancheong']); beam(mb, (-hx - 0.7, py, zp + 5.0), (hx + 0.7, py, zp + 5.0), 0.55, 0.55, M_['dancheong'])
    for px in (-hx, hx): beam(mb, (px, -hy - 0.7, zp + 4.1), (px, hy + 0.7, zp + 4.1), 0.7, 0.7, M_['dancheong'])
    for px in np.linspace(-hx, hx, 4):
        beam(mb, (px, -hy, zp + 3.9), (px, hy, zp + 3.9), 0.4, 0.4, M_['dancheong'])
    for sg in (-1, 1): railing(mb, (-hx, sg * hy, zp + 0.1), (hx, sg * hy, zp + 0.1), 1.0, M_['red'], M_['red_d'], 2.0) if sg > 0 else None
    hip_roof(mb, 0, 0, zp + 5.3, hx, hy, 3.4, M_['tile'], M_['tile_d'], 1.0, 1.7, 22, 12)
    ob = mk(mb, name, smooth=False); ob.location = (cx, cy, Z_LAND); ob.rotation_euler = (0, 0, math.radians(yaw)); return ob

def fortress(M_):
    """Fortress wall ring on the plateau with merlons, a two-storey gate pavilion facing the yard, a corner watch tower."""
    cx, cy, R = -70.0, -135.0, 34.0; mb = MB(); n = 56; hts = []
    def pt(i, r_): a = 2 * math.pi * i / n; x, y = cx + r_ * math.cos(a), cy + r_ * math.sin(a); return Vector((x, y, LH2(x, y)))
    for i in range(n):
        a0, a1 = pt(i, R), pt((i + 1) % n, R); b0, b1 = pt(i, R - 2.2), pt((i + 1) % n, R - 2.2); ht = 6.0
        o0, o1 = a0 + Vector((0, 0, ht)), a1 + Vector((0, 0, ht)); i0, i1 = b0 + Vector((0, 0, ht)), b1 + Vector((0, 0, ht))
        out_n = Vector((a0.x - cx, a0.y - cy, 0)); mb.oface([a0 - Vector((0, 0, 2.0)), a1 - Vector((0, 0, 2.0)), o1, o0], M_['stone'], [(i * 2, 0), (i * 2 + 2, 0), (i * 2 + 2, 1), (i * 2, 1)], out_n)
        mb.oface([o0, o1, i1, i0], M_['stone_d'], [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((0, 0, 1))); mb.oface([b0 - Vector((0, 0, 2.0)), b1 - Vector((0, 0, 2.0)), i1, i0], M_['stone_d'], [(0, 0), (1, 0), (1, 1), (0, 1)], -out_n)
        if i % 2 == 0 and not (n // 4 * 3 - 3 <= i <= n // 4 * 3 + 3):
            m = (o0 + o1) / 2; d = (o1 - o0).normalized(); mb.pid += 1; obox(mb, m + Vector((0, 0, 0.55)) - out_n.normalized() * 0.1, d, out_n.normalized().cross(Vector((0, 0, 1))) * -1 if False else Vector((-d.y, d.x, 0)), Vector((0, 0, 1)), 0.7, 0.55, 0.55, M_['stone'])
    # gate pavilion facing +y (the yard): arch base + two-storey wooden pavilion with red pillars
    g = pt(n // 4 * 3, R - 1.0); g.z = LH2(g.x, g.y)
    mb2 = MB(); cbox(mb2, (0, 0, 3.2), 6.5, 3.4, 3.2, M_['stone']); cbox(mb2, (0, -3.45, 2.3), 1.9, 0.1, 2.3, M_['port_dark']); ell(mb2, (0, -3.45, 4.6), 1.9, 0.12, 1.3, M_['port_dark'], 14, 6)
    cbox(mb2, (0, 0, 6.5), 7.0, 3.9, 0.3, M_['stone_d'])
    for px in (-5.5, -2.0, 2.0, 5.5):
        for py in (-2.9, 2.9): rod(mb2, (px, py, 6.8), (px, py, 10.4), 0.32, M_['red'], seg=8)
    for py in (-2.9, 2.9): beam(mb2, (-6.2, py, 10.3), (6.2, py, 10.3), 0.6, 0.6, M_['dancheong'])
    for sx in (-6.2, 6.2): beam(mb2, (sx, -3.2, 10.3), (sx, 3.2, 10.3), 0.6, 0.6, M_['dancheong'])
    for sg in (-1, 1): cbox(mb2, (0, sg * 2.95, 8.6), 5.8, 0.1, 1.5, M_['plaster'])
    hip_roof(mb2, 0, 0, 10.7, 6.2, 3.4, 3.2, M_['tile'], M_['tile_d'], 1.0, 1.7, 22, 12)
    go = mk(mb2, 'gate_pavilion'); go.location = (g.x, g.y, g.z - 0.5); go.rotation_euler = (0, 0, math.pi)       # arch faces +y: local -y -> world +y after the 180 deg yaw
    t = pt(n // 8 * 7 + 1, R - 1.5); mb3 = MB(); cbox(mb3, (0, 0, 3.0), 3.0, 3.0, 3.0, M_['stone']); cbox(mb3, (0, 0, 7.0), 2.6, 2.6, 1.0, M_['plaster']); hip_roof(mb3, 0, 0, 8.0, 2.8, 2.8, 2.0, M_['tile'], M_['tile_d'], 0.7, 1.2, 12, 8)
    to = mk(mb3, 'watch_tower'); to.location = (t.x, t.y, t.z - 0.5)
    mk(mb, 'fortress_wall', smooth=False)
    for (fx, fy) in ((cx + 30 * math.cos(0.5), cy + 30 * math.sin(0.5)),): flag_obj_world('flag_tri_red', (g.x + 7, g.y + 1, g.z + 6), 9.0, 3.2)
    S['fort'] = (g.x, g.y, g.z)

def flag_obj_world(key, base, h, w, vertical=False, ph=0.0, name='yflag', wave=0.3):
    sh = dict(ride=None); mb = MB(); base = Vector(base); M_ = S['M']; rod(mb, base, base + Vector((0, 0, h)), 0.09, M_['wood_d'], seg=6); top = base + Vector((0, 0, h)); mb2 = MB(); fm = flagmat(key)
    quad_grid(mb2, lambda i, j: top + Vector((0.0 + wave * math.sin(i * 1.1 + ph) * (i / 6), -w * i / 6, -(w * 0.62) * j - 0.1)), 6, 1, fm, uvs=lambda i, j: (i / 6, 1 - j))
    mk(mb, name + '_pole'); o2 = mk(mb2, name + '_cloth'); [setattr(p, 'use_smooth', True) for p in o2.data.polygons]

# ============================================================================= quay props
def timber_stack(M_, cx, cy, yaw=0.0, n=4, L=5.5, z=Z_Q):
    mb = MB(); r = 0.34; mat_ = M_['wood_l']
    for row in range(n):
        for k in range(n - row):
            x = (k - (n - row - 1) / 2) * 0.74; zz = z + r + row * 0.62
            mb.frustum((-L / 2, x, zz), (L / 2, x, zz), r, r, mat_, seg=8, cap0=True, cap1=True, cap_mat=M_['wood_d'])
    ob = mk(mb, 'logs', smooth=False); ob.location = (cx, cy, 0); ob.rotation_euler = (0, 0, math.radians(yaw)); return ob

def plank_pile(M_, cx, cy, yaw, z=Z_Q, n=7):
    mb = MB()
    for i in range(n): cbox(mb, (0, 0, z + 0.07 + i * 0.16 + (0.0)), 2.6 - 0.05 * (i % 3), 0.55 + 0.02 * (i % 2), 0.07, M_['plank'])
    for sx in (-1.6, 1.6): cbox(mb, (sx, 0, z + 0.04), 0.1, 0.7, 0.04, M_['wood_d'])
    ob = mk(mb, 'planks', smooth=False); ob.location = (cx, cy, 0); ob.rotation_euler = (0, 0, math.radians(yaw)); return ob

def rope_coil(M_, c, R=0.95, layers=3):
    mb = MB()
    for k in range(layers): torus(mb, (c[0], c[1], c[2] + 0.15 + 0.2 * k), R - 0.05 * k, 0.11, M_['rope'], 16, 5)
    for k in range(layers): torus(mb, (c[0], c[1], c[2] + 0.15 + 0.2 * k), R - 0.35 - 0.05 * k, 0.11, M_['rope'], 14, 5)
    mk(mb, 'rope_coil')

def basket(M_, c, r=0.62, h=0.9):
    mb = MB(); c = Vector(c); mb.frustum(c, c + Vector((0, 0, h)), r, r * 1.25, M_['basket'], seg=12, cap0=True, cap1=False); torus(mb, c + Vector((0, 0, h)), r * 1.25, 0.05, M_['wood_d'], 14, 4)
    for sg in (-1, 1): rod(mb, c + Vector((sg * r * 1.2, 0, h)), c + Vector((0, 0, h + 0.9)), 0.04, M_['wood_d'], 4)
    mk(mb, 'basket')

def cannon_cart(M_, cx, cy, yaw, z=Z_Q, seed=1):
    """Chongtong cannon barrel lying on a low wooden cart (barrel muzzle up-slope), two spoked wheels."""
    mb = MB(); bz = z + 0.9
    cbox(mb, (0, 0, bz - 0.1), 1.9, 0.62, 0.14, M_['wood_l']); cbox(mb, (0, 0, bz - 0.28), 1.5, 0.78, 0.06, M_['wood_d'])
    for sx in (-1.0, 1.0):
        c = Vector((sx * 0.7, 0, z + 0.55)); mb.frustum(c + Vector((0, -0.95, 0)), c + Vector((0, -0.62, 0)), 0.55, 0.55, M_['wood_d'], seg=12); mb.frustum(c + Vector((0, 0.62, 0)), c + Vector((0, 0.95, 0)), 0.55, 0.55, M_['wood_d'], seg=12)
        rod(mb, c + Vector((0, -0.95, 0)), c + Vector((0, 0.95, 0)), 0.09, M_['iron'], seg=6)
    a = math.radians(8); X = Vector((math.cos(a), 0, math.sin(a))); p0 = Vector((-1.9, 0, bz + 0.45)); p1 = p0 + X * 3.7
    mb.frustum(p0, p1, 0.4, 0.27, M_['cannon'], seg=14); mb.frustum(p1 - X * 0.2, p1 + X * 0.12, 0.34, 0.34, M_['cannon'], seg=14); ell(mb, p0 - X * 0.2, 0.5, 0.45, 0.45, M_['cannon'], 12, 6)
    for k in (0.9, 1.9, 2.8): mb.frustum(p0 + X * (k - 0.07), p0 + X * (k + 0.07), 0.42 - 0.03 * k / 1, 0.42 - 0.03 * k, M_['iron'], seg=14)
    ob = mk(mb, 'cannon_cart', smooth=False); ob.location = (cx, cy, 0); ob.rotation_euler = (0, 0, math.radians(yaw)); return ob

def shear_legs(M_, cx, cy, yaw, z=Z_Q, h=12.5):
    mb = MB(); top = Vector((0, 1.4, z + h))
    for sx in (-1.5, 1.5): rod(mb, (sx, -2.2, z), top, 0.24, M_['wood_l'], seg=7, r1=0.2); cbox(mb, (sx, -2.2, z + 0.15), 0.6, 0.6, 0.15, M_['stone_d'])
    rod(mb, (0, -6.5, z), top - Vector((0, 0.1, 0.4)), 0.2, M_['wood_d'], seg=7, r1=0.16); beam(mb, (-1.4, -2.2, z + 3.2), (1.4, -2.2, z + 3.2), 0.15, 0.15, M_['rope'])
    cbox(mb, (0, 1.4, z + h - 0.15), 0.5, 0.35, 0.35, M_['iron']); rod(mb, top - Vector((0, 0.3, 0.1)), (0, 3.4, z + 6.2), 0.04, M_['rope'], 4); rod(mb, (0, 3.4, z + 6.2), (0, 3.4, z + 2.4), 0.05, M_['rope'], 4)
    cbox(mb, (0, 3.4, z + 1.6), 0.9, 0.7, 0.8, M_['plank']); beam(mb, (0, 3.4, z + 2.4), (0, 3.4, z + 2.9), 0.2, 0.2, M_['iron'])
    ob = mk(mb, 'shear_legs', smooth=False); ob.location = (cx, cy, 0); ob.rotation_euler = (0, 0, math.radians(yaw)); return ob

def barrel_group(M_, c, n=3):
    mb = MB()
    for k in range(n):
        p = Vector((c[0] + 0.95 * (k % 2) - 0.5, c[1] + 0.9 * (k // 2) * (1 if k else 0), c[2])); mb.frustum(p, p + Vector((0, 0, 1.3)), 0.52, 0.52, M_['plank'], seg=10)
        for hz in (0.25, 0.65, 1.05): mb.frustum(p + Vector((0, 0, hz - 0.04)), p + Vector((0, 0, hz + 0.04)), 0.55, 0.55, M_['iron'], seg=10, cap0=False, cap1=False)
    mk(mb, 'barrels')

# ============================================================================= YARD assembly
def calm_water():
    mb = MB(); R = 1600.0; mb.face([Vector((-R, -R, 0)), Vector((R, -R, 0)), Vector((R, R, 0)), Vector((-R, R, 0))][::-1], water_mat('yard_water', calm=True), [(0, 0)] * 4); ob = mk(mb, 'harbour_water', shadow=False); S['ocean'] = ob

def build_yard(preset):
    M_ = S['M']; rs = rnd(24)
    build_terrain(); build_slipway(M_); calm_water()
    sh = build_turtle('turtle', (0.0, WY0, WZ0), 90.0, sea=False, sail=False, oars_dip=False, pitch=math.degrees(THETA), oar_tilt=58); S['turtle'] = sh
    build_cradles(M_, sh)
    # workshop sheds (grey tiled roofs), dancheong pavilion, fortress
    hanok('shed_a', -26, -14, 15, 10, 8, seed=1); hanok('shed_b', -47, -26, 13, 9, -14, seed=2, dark_roof=True); hanok('shed_c', 40, -24, 13, 9, 172, seed=3)
    hanok('shed_d', -22, -40, 16, 9, 2, seed=4, open_front=True); pavilion('pavilion', 24, -42, 188)
    fortress(M_)
    # quay dressing (east wharf + land beside the slip)
    timber_stack(M_, 12.4, -9.5, 90, 4, 5.5, Z_Q); timber_stack(M_, 14.6, -14.0, 80, 3, 5.0, Z_Q); plank_pile(M_, 14.5, -3.0, 92, Z_Q); plank_pile(M_, 11.5, -14.0, 88, Z_Q + 0.0, 5)
    cannon_cart(M_, 12.0, -7.0, 92, Z_Q, 1); cannon_cart(M_, 14.2, -11.5, 87, Z_Q, 2); cannon_cart(M_, 13.0, 15.5, 95, Z_Q, 3)
    rope_coil(M_, (9.6, 5.8, Z_Q), 0.9, 3); rope_coil(M_, (15.0, 3.0, Z_Q), 0.8, 2); rope_coil(M_, (15.8, -9.0, Z_Q), 0.7, 2)
    for c in ((9.0, -5.8), (9.8, -6.6), (15.6, -5.0), (15.0, 17.5), (8.8, 17.6), (16.3, 14.2)): basket(M_, (c[0], c[1], Z_Q), 0.55 + 0.08 * ((int(c[0] * 7) % 3)), 0.8 + 0.1 * (int(c[1]) % 3))
    barrel_group(M_, (16.0, 1.0, Z_Q), 3); barrel_group(M_, (15.4, 12.0, Z_Q), 2); shear_legs(M_, 12.5, -19.0, 90.0, Z_Q, 12.0)
    for (fx, fy, key, hh) in ((16.2, -12.5, 'flag_tri_red', 9.5), (16.4, 20.0, 'flag_tri_blue', 8.5), (8.0, -14.5, 'flag_tri_yellow', 8.0), (-15.0, -4.5, 'flag_tri_red', 8.5)): flag_obj_world(key, (fx, fy, Z_Q if fx > 0 else Z_LAND), hh, 3.0)
    flag_obj_world('flag_red', (-12.5, 2.0, Z_Q), 9.0, 3.4, name='wflag'); flag_obj_world('flag_black', (14.5, -18, Z_LAND), 8.0, 3.0, name='bflag')
    # west landing: a pile of logs and baskets
    timber_stack(M_, -12.5, 3.5, 5, 3, 4.5, Z_Q); basket(M_, (-9.5, -1.0, Z_Q), 0.6, 0.9); basket(M_, (-15.0, 6.0, Z_Q), 0.7, 0.9); rope_coil(M_, (-10.0, 6.0, Z_Q), 0.9, 3)
    timber_stack(M_, -26, -4.5, 0, 3, 5.0, Z_LAND); plank_pile(M_, -33.0, -6.0, 5, Z_LAND, 8); cannon_cart(M_, -20.5, -6.5, 12, Z_LAND, 4); cannon_cart(M_, -16.5, -8.2, 5, Z_LAND, 5)
    # moored panokseon along the wharf and in the bay
    for (nm, x, y, yaw, sd, hc) in (('pk1', 21.9, 7.0, 90, 11, 0), ('pk2', 21.9, 36.0, 92, 12, 1), ('pk3', -34, 28, 125, 13, 0), ('pk4', 80, 52, 24, 14, 1), ('pk5', -95, 70, 160, 15, 0)):
        sh_ = build_panokseon(nm, (x, y, 0.0), yaw, scale=1.0 if nm != 'pk5' else 1.12, sea=False, seed=sd, sail_up=(nm in ('pk4', 'pk5')), hullc=hc, oar_tilt=55)
    mb = MB()
    for (yy, ya) in ((3.0, 4.4), (10.0, 11.4)): rod(mb, (17.0 - 0.15, yy, Z_Q + 0.55), (21.9 - 4.6, ya, 3.2), 0.05, M_['rope'], seg=4)
    mk(mb, 'mooring_lines')
    # bay: rocky green islands + far mountains
    make_island('bay_a', -150, 140, 42, 15, 5, npine=70); make_island('bay_b', 170, 200, 55, 20, 7, npine=90); make_island('bay_c', 20, 330, 38, 12, 9, npine=50)
    make_mountains(0, 80, 620, 1050, 85, 3, 15, 165, '#58865e', '#7a947e', 120); make_mountains(0, 80, 700, 1100, 70, 4, 165, 375, '#5a8260', '#7c9580', 120)
    # pines on the hills and round the yard
    n = 0; tries = 0
    while n < 300 and tries < 6000:
        tries += 1; x = rs.uniform(-330, 330); y = rs.uniform(-410, -8)
        if -90 < x < 95 and y > -78: continue
        if math.hypot(x - FORT[0], y - FORT[1]) < 40 and rs.random() < 0.5: continue
        z = LH2(x, y)
        if y > -40 and z < Z_LAND + 0.5 and abs(x) < 130: continue
        if math.hypot(x - FORT[0], y - FORT[1]) < 36: continue
        plant(x, y, z - 0.1, rs.uniform(0.9, 1.5) if y > -150 else rs.uniform(1.4, 2.6), 5000 + n); n += 1
    S['marks'] = {}; _yard_marks()

def _yard_marks():
    """Stand points (world, feet). Roof workers kneel ON the roof edge (parent: ship root 'turtle', local coordinates in S['parented'])."""
    mk_ = S['marks']; par = S['parented'] = {}
    mk_['yi_quay'] = (9.5, 1.2, Z_Q); mk_['yi_bow'] = (8.6, 18.5, Z_Q); mk_['yi_front'] = (8.6, -2.3, Z_Q)
    mk_['worker_quay_a'] = (9.4, -11.0, Z_Q); mk_['worker_quay_b'] = (9.3, -4.6, Z_Q); mk_['worker_quay_c'] = (13.5, 10.8, Z_Q); mk_['worker_land_a'] = (-18.0, -11.0, Z_LAND)
    for i, x in enumerate((-8.0, -3.0, 2.5, 7.5)):
        for sg, tag in ((-1, 'p'), (1, 's')):                                    # roof edge: v = 0.84 of the half width (inside the eave lip)
            ye = t_ye(x); y = sg * 0.99 * ye; lp = (x, y, roof_z(x, y)); nm = 'worker_roof_%s%d' % (tag, i + 1); par[nm] = ('turtle', lp); mk_[nm] = tuple(yw(lp))

def anchors_yard(): return dict(marks=dict(S['marks']), parented={k: dict(ship=v[0], local=tuple(v[1])) for k, v in S['parented'].items()})

# ============================================================================= SEA assembly: Hansan waters
JAP_ATAKE = ['jflag', 'j_near', 'j_board', 'j4', 'j5', 'j6', 'j7', 'j8']
KOR = ['turtle'] + ['k%d' % i for i in range(1, 8)]
U_C = (15.0, 0.0); U_R = 78.0; U_ARM = 150.0

def u_slots(n, spacing=62.0):
    """Positions along the U (crane-wing) round the Japanese fleet: the front centre first (the turtle ship), then alternating up / down the arms. [(x, y, yaw_deg)], facing inward."""
    arc = math.pi * U_R; out = []
    for i in range(n):
        d = 0.0 if i == 0 else ((i + 1) // 2) * spacing * (1 if i % 2 else -1); ad = abs(d); sg = 1 if d >= 0 else -1
        if ad <= arc / 2: a = ad / U_R; x, y = U_C[0] + U_R * math.cos(a), sg * U_R * math.sin(a); yaw = math.degrees(math.atan2(-y, -(x - U_C[0]))) if i else 180.0
        else: x, y = U_C[0] - (ad - arc / 2), sg * U_R; yaw = -sg * 90.0
        yaw = (yaw + 180.0) % 360.0 - 180.0 if i else 180.0; out.append((x, y, yaw))
    return out

def fleet_slots(rs):
    """Non-overlapping positions for the Japanese ships (ellipse test), atakebune first."""
    placed = []
    def ok(x, y, L, B): return all(not (abs(x - px) < (L + pl) / 2 + 3.0 and abs(y - py) < (B + pb) / 2 + 3.5) for (px, py, pl, pb) in placed)
    out = {}
    specs = [('jflag', 28, 11, (0, 0)), ('j_near', 27, 11, (-6, -26)), ('j_board', 27, 11, (-42, 24))]
    for nm, L, B, fixed in specs: placed.append((fixed[0], fixed[1], L, B)); out[nm] = fixed
    names = [(n, 27, 11) for n in JAP_ATAKE[3:]] + [('s%02d' % i, 17, 4.5) for i in range(1, 19)]
    for nm, L, B in names:
        for _ in range(400):
            x = rs.uniform(-130, 22); y = rs.uniform(-50, 50)
            if ok(x, y, L, B): placed.append((x, y, L, B)); out[nm] = (x, y); break
    return out

def build_sea(preset):
    M_ = S['M']; rs = rnd(924)
    make_ocean(fine=(-260.0, 360.0, -200.0, 220.0), h=2.4, extent=(-1500.0, 1500.0, -1500.0, 1500.0))
    make_island('isl_a', 300, -170, 46, 17, 3, npine=70); make_island('isl_b', -250, 190, 55, 19, 4, npine=80); make_island('isl_c', 120, 215, 36, 13, 6, npine=45)
    make_island('isl_d', -120, -215, 42, 15, 8, npine=60); make_island('isl_e', 330, 60, 30, 10, 12, npine=30)
    bh = make_island('beach', -150, 150, 62, 9, 21, kind='beach', npine=40, sand=True, dirn=-math.pi / 2); beach_extras()
    make_mountains(0, 0, 760, 1180, 90, 5, 0, 360, '#58865e', '#7b957f', 200)
    slots = fleet_slots(rs); S['jap'] = []
    seeds = rnd(77)
    for i, nm in enumerate(JAP_ATAKE):
        x, y = slots[nm]; sh = build_atakebune(nm, (x, y, 0.0), 0.0 + rs.uniform(-3, 3), scale=rs.uniform(0.92, 1.1) if i else 1.08, sea=True, seed=10 + i, flagship=(nm == 'jflag'), sail=(i % 2 == 1), towerh=rs.uniform(0.85, 1.25) if i else 1.15,
                                            banners=4 if i == 0 else rs.choice([2, 3, 4, 6]), band=['#a8201f', '#a8201f', '#7a1a1a', '#b03a1c'][i % 4], roof_dark=(i % 2 == 1)); S['jap'].append(sh)
    for i in range(1, 19):
        nm = 's%02d' % i; x, y = slots[nm]; sh = build_sekibune(nm, (x, y, 0.0), rs.uniform(-6, 6), scale=rs.uniform(0.9, 1.12), sea=True, seed=40 + i, sail=(i % 2 == 0), shield=i, banner=['flag_nob_circle', 'flag_nob_diamond', 'flag_nob_rcircle'][i % 3]); S['jap'].append(sh)
    # Korean ships: fleeing line ahead of the Japanese (k = 0) and the U slots (k = 1)
    flee = [(120.0, 8.0), (150.0, -32.0), (172.0, 40.0), (200.0, -6.0), (96.0, -58.0), (136.0, 68.0), (226.0, 30.0), (214.0, -50.0)]; us = u_slots(8)
    sh = build_turtle('turtle', (flee[0][0], flee[0][1], 0.0), 0.0, sea=True, sail=False); sh['p0'] = (flee[0][0], flee[0][1], 0.0); sh['p1'] = (us[0][0], us[0][1], 180.0); S['kor'] = [sh]; S['turtle'] = sh
    for i in range(1, 8):
        sh = build_panokseon('k%d' % i, (flee[i][0], flee[i][1], 0.0), 0.0, scale=rs.uniform(0.95, 1.1), sea=True, seed=60 + i, sail_up=True, flag=['flag_tri_red', 'flag_tri_black'][i % 2], hullc=i % 2)
        sh['p0'] = (flee[i][0], flee[i][1], 0.0); sh['p1'] = (us[i][0], us[i][1], us[i][2]); S['kor'].append(sh)
    for sh in S['jap']: sh['p0'] = (sh['base'].x, sh['base'].y, sh['yaw'])
    build_damage_kit(); build_cannon_kit(); build_plank(); S['marks'] = {}; _sea_marks()

def beach_extras():
    """Gentle surf foam lines on the beach island (swell-driven segments) and a few rocks."""
    isl = S['islands']['beach']; h = isl['h']; cx, cy = isl['c']; M_ = S['M']; n = 22; a0 = math.radians(215); a1 = math.radians(325)
    def shore(a):
        r = isl['R'] * 1.5
        while r > 0 and h(cx + r * math.cos(a), cy + r * math.sin(a)) < 0.04: r -= 0.3
        return r
    S['shore_r'] = {}
    for i in range(n):
        aa, bb = a0 + (a1 - a0) * i / n, a0 + (a1 - a0) * (i + 1) / n; mb = MB(); pts = []
        mid = Vector((cx + shore((aa + bb) / 2) * math.cos((aa + bb) / 2), cy + shore((aa + bb) / 2) * math.sin((aa + bb) / 2), 0.0))
        for row, (d0, d1) in enumerate(((0.6, 2.2), (3.6, 4.6), (6.2, 6.9))):
            q = []
            for a in (aa, bb):
                r = shore(a); q.append(Vector((cx + (r + d0) * math.cos(a), cy + (r + d0) * math.sin(a), 0.0)) - mid); q.append(Vector((cx + (r + d1) * math.cos(a), cy + (r + d1) * math.sin(a), 0.0)) - mid)
            mb.oface([q[0], q[2], q[3], q[1]], M_['surf_f'], [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((0, 0, 1)))
        o = mk(mb, 'surf_%d' % i, shadow=False); o.location = (mid.x, mid.y, 0.12)
        drive(o, 'location', 2, '0.12+' + swell_expr('(%f)' % mid.x, '(%f)' % mid.y, 0.8), {})
    S['shore_a'] = -math.pi / 2

def build_plank():
    """A wooden plank half-beached at the surf line: it lies on the wet sand in very shallow water (resting on the terrain, tilted with the slope), surf foam washing round it (foam ring driven by the swell)."""
    M_ = S['M']; mb = MB(); cbox(mb, (0, 0, 0), 2.7, 0.62, 0.11, M_['plank']); cbox(mb, (0.2, 0, 0.0), 0.08, 0.64, 0.115, M_['wood_d']); cbox(mb, (-1.3, 0, 0.0), 0.08, 0.64, 0.115, M_['wood_d'])
    isl = S['islands']['beach']; cx, cy = isl['c']; h = isl['h']; a = -math.pi / 2; rr = isl['R'] * 1.5
    while rr > 0 and h(cx + rr * math.cos(a), cy + rr * math.sin(a)) < 0.04: rr -= 0.3
    S['shore_pt'] = Vector((cx + rr * math.cos(a), cy + rr * math.sin(a), 0.0))
    px, py = cx + (rr + 0.7) * math.cos(a) + 1.0, cy + (rr + 0.7) * math.sin(a); z0 = h(px, py)
    sl = (h(px, py - 1.0) - h(px, py + 1.0)) / 2.0                       # terrain slope along y (toward the sea it falls)
    o = mk(mb, 'plank', shadow=True); o.location = (px, py, z0 + 0.12); o.rotation_euler = (math.atan(sl) * -1.0, 0, math.radians(8)); S['plank'] = o; S['plank_z'] = z0 + 0.12 + 0.11
    mb2 = MB(); mb2.oface([Vector((-4.6, -2.4, 0)), Vector((4.6, -2.4, 0)), Vector((4.6, 2.4, 0)), Vector((-4.6, 2.4, 0))], M_['ring_f'], [(0, 0), (1, 0), (1, 1), (0, 1)], Vector((0, 0, 1)))
    ro = mk(mb2, 'plank_ring', shadow=False); ro.location = (px, py, 0.12); drive(ro, 'location', 2, '0.14+' + swell_expr('(%f)' % px, '(%f)' % py, 0.8), {})

def _sea_marks():
    mk_ = S['marks']; par = S['parented'] = {}; shs = S['ships']
    fl = shs['jflag']; z = fl['deck_z']; xa, xb = fl['deck_x']; xc = xb - 5.0
    for nm, lp in (('commander_deck', (xc, 0.0, z)), ('soldier_deck_a', (xc - 3.0, 2.2, z)), ('soldier_deck_b', (xc - 3.4, -2.0, z)), ('soldier_deck_c', (xc - 1.2, 3.2, z)), ('soldier_deck_d', (xc - 1.6, -3.3, z)), ('commander_bow', (xb - 0.8, 0.0, z))): par[nm] = ('jflag', lp)
    jn = shs['j_near']; z = jn['deck_z']; xb2 = jn['deck_x'][1]
    for nm, lp in (('soldier_chase_a', (xb2 - 0.6, 0.0, z)), ('soldier_chase_b', (xb2 - 1.9, 2.4, z)), ('soldier_chase_c', (xb2 - 1.9, -2.4, z))): par[nm] = ('j_near', lp)
    jb = shs['j_board']; z = jb['deck_z']; xb3 = jb['deck_x'][1]
    for nm, lp in (('soldier_board_a', (jb['deck_x'][0] + 5.4, 3.55, z)), ('soldier_board_b', (jb['deck_x'][0] + 7.4, 3.75, z)), ('soldier_board_c', (jb['deck_x'][0] + 3.6, 3.4, z))): par[nm] = ('j_board', lp)
    for nm, (sn, lp) in par.items(): mk_[nm] = tuple(round(c, 3) for c in L2W(sn, lp))
    sp = S['shore_pt']; mk_['commander_plank'] = (S['plank'].location.x, S['plank'].location.y, S['plank_z']); mk_['commander_sand'] = tuple(round(c, 3) for c in (sp.x - 0.5, sp.y + 4.5, S['islands']['beach']['h'](sp.x - 0.5, sp.y + 4.5)))
    mk_['commander_crawl_a'] = tuple(round(c, 3) for c in (sp.x + 1.0, sp.y + 7.5, S['islands']['beach']['h'](sp.x + 1.0, sp.y + 7.5)))
    for k in ('turtle',): par['turtle_deck'] = ('turtle', (0.0, 0.0, roof_z(0, 0) + 0.1))

def anchors_sea(): return dict(marks=dict(S['marks']), parented={k: dict(ship=v[0], local=tuple(v[1])) for k, v in S['parented'].items()})

# ============================================================================= damage + cannon smoke kits
def build_damage_kit():
    """Per Japanese ship: a stump + a splintered fallen mast top (shown when its mast breaks) and a grey smoke column (billows); the mast / sail objects are hidden then."""
    M_ = S['M']; order = list(S['jap']); rs = rnd(5); rs.shuffle(order); n = len(order); S['dmg'] = []
    for i, sh in enumerate(order):
        thr = 0.03 + 0.62 * i / max(1, n - 1) if i < int(n * 0.72) else 9.0          # about 72 % of the Japanese fleet gets hit
        ride = sh['ride']; mx = sh['masts'][0][0] if sh['masts'] else (sh['L'] * 0.12); zb = sh['masts'][0][1] if sh['masts'] else sh.get('deck_z', 2.4)
        mb = MB(); rod(mb, (mx, 0, zb), (mx, 0, zb + 2.6), 0.3, M_['wood_d'], seg=6, r1=0.22); cone(mb, (mx, 0, zb + 2.5), (mx + 0.1, 0.05, zb + 3.5), 0.22, M_['wood_l'], 5); cone(mb, (mx, 0.05, zb + 2.4), (mx - 0.3, 0.2, zb + 3.2), 0.14, M_['wood_l'], 4)
        a = math.radians(70); d = Vector((math.cos(a) * (1 if i % 2 else -1), 0.22, math.sin(a) * 0.0 + 0.05)); p0 = Vector((mx + (1.0 if i % 2 else -1.0), 0.3, zb + 0.3)); p1 = p0 + Vector((2.7 * (1 if i % 2 else -1), 1.6, 0.45))
        rod(mb, p0, p1, 0.2, M_['wood_l'], seg=6, r1=0.16)
        stump = mk(mb, '%s_stump' % sh['name'], ride); stump.hide_render = True
        mbs = MB(); ph = rs.uniform(0, 6); cx_ = mx - 1.5
        for k, (zz, rr_) in enumerate(((zb + 3.0, 1.1), (zb + 5.8, 1.6), (zb + 9.0, 2.1), (zb + 12.4, 2.5), (zb + 16.0, 2.7))): lump(mbs, (cx_ - 1.4 * k + 0.6 * math.sin(ph + k), 0.5 * math.sin(ph + 2 * k), zz), rr_, M_['smoke_d'], 300 + i * 9 + k, seg=10, rings=6, rough=0.18)
        smk = mk(mbs, '%s_dsmoke' % sh['name'], ride, shadow=True); smooth_round(smk, 1); smk.hide_render = True
        hide = [o for o in (bpy.data.objects.get(sh['name'] + '_mast'), bpy.data.objects.get(sh['name'] + '_sail')) if o]
        S['dmg'].append(dict(sh=sh, thr=thr, deg=(3.0 + 5.5 * rs.random()) * (1 if i % 2 else -1), stump=stump, smoke=smk, hide=hide))

def build_cannon_kit():
    """Smoke puffs (2 per gun) + a muzzle flash at every Korean gun port (turtle ship 12, panokseon 10 each), recycled by set_cannon_smoke(level, frame)."""
    M_ = S['M']; S['guns'] = []; rs = rnd(11)
    for sh in S['kor']:
        for gi, g in enumerate(sh['guns']):
            puffs = []
            for k in range(2):
                mb = MB(); lump(mb, (0, 0, 0), 1.0, M_['smoke_g'] if (gi + k) % 3 else M_['smoke_y'], 900 + gi * 3 + k, seg=9, rings=6, rough=0.2); o = mk(mb, 'puff_%s_%d_%d' % (sh['name'], gi, k), sh['ride'], shadow=True); smooth_round(o, 1); o.hide_render = True; puffs.append(o)
            mb = MB(); lump(mb, (0, 0, 0), 0.7, M_['flash'], 1200 + gi, seg=7, rings=5, rough=0.35); fl = mk(mb, 'flash_%s_%d' % (sh['name'], gi), sh['ride'], shadow=False); fl.hide_render = True
            S['guns'].append(dict(sh=sh, g=g, puffs=puffs, flash=fl, off=rs.uniform(0, 1), per=rs.uniform(1.15, 1.7), size=rs.uniform(0.9, 1.25)))

# ============================================================================= HOOKS (keyable per frame: pass frame=n; keys win over un-keyed calls until clear_keys())
def ship_root(name):
    """The node to PARENT deck / roof cards to: the ship's `ride` empty (it carries the heave / roll / pitch and the slipway pitch), so a card keeps its spot on the deck."""
    return S['ships'][name]['ride']
def ship_motion_root(name): return S['ships'][name]['root']

def set_spikes(rows_k, frame=None):
    """Turtle roof spikes: stage j (1..3, three lines each side, ridge -> eave) is shown when rows_k >= j. 0 none, 3 the full roof. Keys constant (pop-in on the hammer beat)."""
    k = float(rows_k); sh = S['turtle']
    for j, o in enumerate(sh['spikes']): show(o, k >= j + 1 - 1e-6, frame)
    S['spike_k'] = k

def set_ports(k, frame=None):
    """Turtle gun ports: 0 lids closed, 1 lids hinged open (70 deg) and the cannon muzzles poking out. Fractions open the lids part way (muzzles show from 0.5). Keys linear."""
    k = max(0.0, min(1.0, float(k))); sh = S['turtle']
    for lid, sg in sh['lids']:
        a = math.radians(72.0) * k; lid.rotation_euler = (a, 0, 0 if sg > 0 else math.pi)
        if frame is not None: key_attr(lid, 'rotation_euler', frame, 'LINEAR')
    for mz in sh['muzzles']: show(mz, k >= 0.5, frame)
    S['ports_k'] = k

def _billow(o, base, drift, H, size, ph, vis, frame):
    s = max(0.001, size * (0.35 + 1.35 * ph) * math.sin(math.pi * min(1.0, ph * 1.12)) ** 0.5)
    o.location = base + drift * ph + Vector((0, 0, H * ph)); o.scale = (s, s, s * 0.85)
    if frame is not None: key_attr(o, 'location', frame, 'LINEAR'); key_attr(o, 'scale', frame, 'LINEAR')
    show(o, vis, frame)

def set_dragon_smoke(level, frame=None, speed=1.0):
    """Grey-yellow cartoon smoke puffs from the dragon's mouth (turtle ship): 0 none .. 1 normal .. 1.5 thick. CALL EVERY FRAME (puffs cycle with the frame number)."""
    sh = S['turtle']; f = frame if frame is not None else bpy.context.scene.frame_current
    if 'dsmoke' not in sh:
        M_ = S['M']; sh['dsmoke'] = []; r = rnd(31)
        for k in range(10):
            mb = MB(); lump(mb, (0, 0, 0), 1.0, M_['smoke_y'] if k % 2 else M_['smoke_g'], 1500 + k, seg=10, rings=6, rough=0.2); o = mk(mb, 'dsmoke_%d' % k, sh['ride'], shadow=True); smooth_round(o, 1); o.hide_render = True
            sh['dsmoke'].append(dict(ob=o, ph=k / 10 + r.uniform(0, 0.03), size=0.62 + 0.25 * r.random(), drift=Vector((5.0 + r.uniform(-1, 1), r.uniform(-1.4, 1.4), 0.0)), H=4.6 + r.uniform(0, 1.4)))
    m = sh['mouth']
    for b in sh['dsmoke']:
        ph = (b['ph'] + 0.012 * speed * f) % 1.0; _billow(b['ob'], m + Vector((0.4, 0, 0)), b['drift'], b['H'], b['size'] * (0.7 + 0.5 * min(1.5, level)), ph, level > 0.001, frame)

def set_cannon_smoke(level, frame=None):
    """Cartoon smoke puffs + short bright muzzle flashes at the Korean gun ports (turtle ship 12, panokseon 10 each): the fraction `level` (0..1) of the guns fires, each on its own
    cycle (1.2-1.7 s); the flash lasts about 3 frames at the start of each cycle. CALL EVERY FRAME. Needs the sea location."""
    f = frame if frame is not None else bpy.context.scene.frame_current; n = len(S['guns'])
    for i, G in enumerate(S['guns']):
        act = level > 0.001 and ((i * 0.618) % 1.0) < level; g = G['g']; ph0 = ((f / FPS) / G['per'] + G['off']) % 1.0
        for k, o in enumerate(G['puffs']):
            ph = (ph0 + k * 0.5) % 1.0; b = g['local'] + g['dir'] * 0.5
            _billow(o, b, g['dir'] * 9.0 + Vector((0, 0, 1.6)), 5.5, G['size'] * 2.0, ph, act, frame)
        fl = G['flash']; vis = act and ph0 < 0.075; fl.location = g['local'] + g['dir'] * 0.7; fl.scale = (1 + 0.5 * ph0 * 10,) * 3
        if frame is not None: key_attr(fl, 'location', frame, 'LINEAR'); key_attr(fl, 'scale', frame, 'LINEAR')
        show(fl, vis, frame)

def set_damage(k, frame=None):
    """Japanese ships hit: ship i is hit once k > thr_i (about 72 % of the fleet, spread over 0.03..0.65): it lists 3-8.5 deg, its mast breaks (stump + splintered top lies on the deck,
    sail gone) from amount 0.5, and a grey smoke column rises. NO fire, NO people, NO debris of bodies. Keys: listing linear, visibility constant."""
    S['vals']['d'] = float(k); S['last_hook'] = 'd'; _place(frame)

def set_fleet_chase(s, frame=None):
    """Seconds of chase: the whole Japanese fleet sails +x by CHASE_V (3 D/s) x s (the Korean ships keep their offsets, so the relative picture holds). Keys linear."""
    S['vals']['s'] = float(s); S['last_hook'] = 's'; _place(frame)

def set_korean_turn(k, frame=None):
    """0 = the Korean ships (turtle + 7 panokseon) flee ahead of the Japanese (heading +x, away from the pursuers); 1 = turned into the U (crane wing) round the Japanese fleet, facing it.
    Positions and headings are interpolated linearly. Keys linear."""
    S['vals']['k'] = max(0.0, min(1.0, float(k))); S['last_hook'] = 'k'; _place(frame)

def set_special(name, frame=None):
    """None | 'board' (turtle ship + the Japanese ship j_board lie alongside at BOARD_AT) | 'solo' (the turtle ship alone at SOLO_AT, for macro_oar). Keys constant."""
    S['vals']['sp'] = name or ''; S['last_hook'] = 'sp'; _place(frame)

BOARD_AT = (130.0, -150.0); SOLO_AT = (40.0, -120.0, 0.0)
def _interp(lst, f, default):
    if not lst: return default
    lst = sorted(lst, key=lambda a: a[0])
    if f <= lst[0][0]: return lst[0][1]
    for (f0, v0), (f1, v1) in zip(lst, lst[1:]):
        if f0 <= f <= f1: return v0 + (v1 - v0) * (f - f0) / max(1e-9, f1 - f0)
    return lst[-1][1]
def _step(lst, f, default):
    v = default
    for fr, x in sorted(lst, key=lambda a: a[0]):
        if fr <= f: v = x
    return v

def _place(frame):
    """Position every ship from the hook values (s, k, damage, special). With a frame, key at the union of all hook key frames so the keys of different hooks stay consistent."""
    V_ = S['vals']
    if frame is not None:
        S['fk'][S['last_hook']].append((frame, V_[S['last_hook']]))
        frames = sorted(set(f for l in S['fk'].values() for f, _ in l))
        for f in frames: _place_at(f, dict(s=_interp(S['fk']['s'], f, V_['s']), k=_interp(S['fk']['k'], f, V_['k']), d=_interp(S['fk']['d'], f, V_['d']), sp=_step(S['fk']['sp'], f, V_['sp'])), f)
    else: _place_at(None, V_, None)

def _place_at(f, v, frame):
    s, k, d, sp = v['s'], v['k'], v['d'], v['sp']
    for sh in S['jap']:
        p = sh['p0']; sh['root'].location = (p[0] + CHASE_V * s, p[1], 0.0); sh['root'].rotation_euler = (0, 0, math.radians(p[2]))
    for sh in S['kor']:
        a, b = sh['p0'], sh['p1']; x = a[0] + (b[0] - a[0]) * k + CHASE_V * s; y = a[1] + (b[1] - a[1]) * k + 12.0 * math.sin(math.pi * k) * (1 if b[1] > 0 else -1) * (0.4 if sh['name'] != 'turtle' else 0.0)
        sh['root'].location = (x, y, 0.0); sh['root'].rotation_euler = (0, 0, math.radians(a[2] + (b[2] - a[2]) * k))
    if sp == 'board':
        t = S['ships']['turtle']; t['root'].location = (BOARD_AT[0] + CHASE_V * s, BOARD_AT[1], 0.0); t['root'].rotation_euler = (0, 0, 0)
        jb = S['ships']['j_board']; jb['root'].location = (BOARD_AT[0] + CHASE_V * s - 3.0, BOARD_AT[1] - 10.3, 0.0); jb['root'].rotation_euler = (0, 0, 0)
    elif sp == 'solo':
        t = S['ships']['turtle']; t['root'].location = (SOLO_AT[0] + CHASE_V * s, SOLO_AT[1], 0.0); t['root'].rotation_euler = (0, 0, math.radians(SOLO_AT[2]))
    for D_ in S['dmg']:
        sh = D_['sh']; amt = max(0.0, min(1.0, (d - D_['thr']) / 0.2)); sh['root'].rotation_euler[0] = math.radians(D_['deg']) * amt
        show(D_['stump'], amt > 0.5, frame); show(D_['smoke'], amt > 0.03, frame)
        for o in D_['hide']: show(o, amt <= 0.5, frame)
    if frame is not None:
        for sh in list(S['jap']) + list(S['kor']):
            key_attr(sh['root'], 'location', frame, 'LINEAR'); key_attr(sh['root'], 'rotation_euler', frame, 'LINEAR')
    S['s'] = s; S['k'] = k; S['d'] = d

def clear_keys():
    """Drop every key the hooks inserted (objects, lamps, materials), so plain set_* calls hold again. The drivers (ship heave, oar strokes, foam, plank) stay."""
    for idb in list(bpy.data.objects) + list(bpy.data.lights):
        ad = idb.animation_data
        if ad and ad.action: ad.action = None
    for m in bpy.data.materials:
        if m.node_tree and m.node_tree.animation_data: m.node_tree.animation_data_clear()
    S['fk'] = dict(s=[], k=[], d=[], sp=[])

def sea_state(): return dict(s=S['vals']['s'], k=S['vals']['k'], d=S['vals']['d'], sp=S['vals']['sp'])

# ============================================================================= cameras, presets, anchors, cards
def _fl(name): return S['ships'][name]
def L2W(ship, lp):
    sh = S['ships'][ship]; r = sh['root']; return Vector(r.location) + Matrix.Rotation(r.rotation_euler.z, 3, 'Z') @ (Vector(lp) * sh['scale'])

def yard_cams():
    return dict(
        roof_low=dict(loc=(15.8, 9.0, 3.6), look_at=(-0.5, -3.5, 5.9), lens=22),
        bow=dict(loc=(5.6, 37.0, 4.8), look_at=(3.8, 15.0, 4.4), lens=24),
        yard_wide=dict(loc=(16.0, 24.5, 7.6), look_at=(-3.0, -10.0, 5.0), lens=21),
        roof_top=dict(loc=(-9.5, -29.0, 15.0), look_at=(0.8, -4.0, 5.2), lens=24),
        macro_spikes=dict(loc=tuple(yw((14.8, -9.0, 4.4))), look_at=tuple(yw((10.4, -3.4, roof_z(10.4, -3.4) + 0.5))), lens=60, fstop=2.8),
        macro_dragon=dict(loc=(-5.2, 25.4, 4.4), look_at=tuple(yw((20.4, 0, 3.15))), lens=55, fstop=2.8))

def sea_cams():
    fl = _fl('jflag'); z = fl['deck_z']; xa, xb = fl['deck_x']; xc = xb - 5.0
    W = lambda lp: tuple(L2W('jflag', lp))
    jn = _fl('j_near'); xn = jn['deck_x'][1]; jb = _fl('j_board')
    sp = S['shore_pt']
    return dict(
        fleet_wide=dict(loc=(-48.0, -82.0, 10.0), look_at=(-62.0, 0.0, 8.5), lens=24),
        flag_deck=dict(loc=W((xc + 3.7, 0.55, z + 2.0)), look_at=W((xc - 3.0, 0.0, z + 2.0)), lens=24),
        flag_deck_b=dict(loc=W((xc - 1.8, 3.9, z + 2.3)), look_at=W((xc, -0.3, z + 2.5)), lens=24),
        flag_deck_crew=dict(loc=W((xc + 4.3, 0.0, z + 2.4)), look_at=W((xc - 2.5, 0.0, z + 2.1)), lens=22),
        hansan_high=dict(loc=(60.0, -330.0, 150.0), look_at=(50.0, 0.0, 0.0), lens=22),
        flag_bow=dict(loc=W((xb + 7.0, -5.8, z + 2.6)), look_at=W((xb - 2.5, 0.8, z + 3.2)), lens=24),
        chase=dict(loc=tuple(L2W('j_near', (xn + 14.0, -11.0, 4.2))), look_at=tuple(L2W('j_near', (xn - 1.5, 0.0, 6.6))), lens=24),
        board=dict(loc=tuple(L2W('turtle', (jb['deck_x'][0] + 7.0 - 1.5, 0.8, 8.3))), look_at=tuple(L2W('j_board', (jb['deck_x'][0] + 6.0, 4.4, jb['deck_z'] + 0.3))), lens=26),
        board_end=dict(loc=tuple(L2W('turtle', (jb['deck_x'][0] + 6.0, 0.4, 5.6))), look_at=tuple(L2W('turtle', (jb['deck_x'][0] + 6.8, -3.2, 4.2))), lens=28),
        reveal_top=dict(loc=(-22.0, -250.0, 185.0), look_at=(-22.0, 2.0, -5.0), lens=22),
        aftermath=dict(loc=(150.0, -16.0, 6.5), look_at=(55.0, 0.0, 7.0), lens=24),
        shore=dict(loc=(sp.x + 14.0, sp.y - 34.0, 7.5), look_at=(sp.x + 2.0, sp.y + 3.0, 2.0), lens=24),
        macro_oar=dict(loc=(SOLO_AT[0] + 1.25 + 3.4, SOLO_AT[1] + 10.3 + 3.0, 1.3), look_at=(SOLO_AT[0] + 1.05, SOLO_AT[1] + 10.3 - 1.0, -0.35), lens=40, fstop=2.8))

PRESETS = dict(
    roof_low=dict(loc='yard', cam='roof_low', state='sp2'), bow=dict(loc='yard', cam='bow', state='sp3,ds1'), yard_wide=dict(loc='yard', cam='yard_wide', state='sp3'), roof_top=dict(loc='yard', cam='roof_top', state='sp1'),
    macro_spikes=dict(loc='yard', cam='macro_spikes', state='sp2'), macro_dragon=dict(loc='yard', cam='macro_dragon', state='sp3,ds1'),
    fleet_wide=dict(loc='sea', cam='fleet_wide', state=''), flag_deck=dict(loc='sea', cam='flag_deck', state=''), flag_deck_b=dict(loc='sea', cam='flag_deck_b', state=''), flag_deck_crew=dict(loc='sea', cam='flag_deck_crew', state=''),
    hansan_high=dict(loc='sea', cam='hansan_high', state=''), flag_bow=dict(loc='sea', cam='flag_bow', state=''), chase=dict(loc='sea', cam='chase', state='s0'),
    board=dict(loc='sea', cam='board', state='sp3,special:board'), reveal_top=dict(loc='sea', cam='reveal_top', state='k1,cs1,dm0.35,sp3,pt1,ds1'),
    aftermath=dict(loc='sea', cam='aftermath', state='k1,dm1,cs0.35,sp3,pt1'), shore=dict(loc='sea', cam='shore', state=''), macro_oar=dict(loc='sea', cam='macro_oar', state='special:solo,os0.4', samples=14))
LOC_PRESETS = dict(yard=[k for k, v in PRESETS.items() if v['loc'] == 'yard'], sea=[k for k, v in PRESETS.items() if v['loc'] == 'sea'])
CAM_NOTES = dict(
    roof_low='yard: low 3/4 from the east quay at the stern quarter: the turtle ship on its cradles, roof edge workers, Yi in the foreground on the quay (push in)',
    bow='yard: the dragon head at the bow seen from the front over the water, Yi beside the bow on the wharf (pull back and rise)', yard_wide='yard: wide from the wharf by the bow: ship, sheds, pavilion, fortress hill, bay (push in)',
    roof_top='yard: high 3/4 over the roof from the stern-west (crane down); spike rows 1-3 and the ports via the hooks', macro_spikes='yard: 60 mm f/2.8 on the iron spikes of the roof edge, yard in bokeh',
    macro_dragon='yard: 55 mm f/2.8 on the dragon mouth puffing smoke, bay in bokeh', fleet_wide='sea: the Japanese fleet (26 ships) seen from the side, sailing +x (slide with the fleet)',
    flag_deck='sea: commander stand on the flagship upper deck (tower, banners, drum, weapon rack), from the bow side', flag_deck_b='sea: the same stage from the port side', flag_deck_crew='sea: the stage wider with the crew spots',
    hansan_high='sea: very high wide over the strait, Japanese fleet left, the Korean ships fleeing ahead (+x), islands', flag_bow='sea: the flagship bow seen from ahead, the commander at the bow, the fleet behind',
    chase='sea: the near atakebune j_near charging, three soldier spots on its bow deck', board='sea: from the deck of j_board over the rail onto the spiked roof of the turtle ship alongside',
    reveal_top='sea: very high aerial: the U round the Japanese fleet, cannon smoke from every side, turtle ship front centre', aftermath='sea: low behind the turtle ship, drifting smoke, Japanese ships listing with broken masts and smoke columns',
    shore='sea: the beach island: the floating plank near the surf, the sand above it', macro_oar='sea: 55 mm f/2.8 low at the water on one oar blade dipping with foam and spray')

T.PH.update(yi=('boss', dict(yaw=0.3, head_roll=-3, expr='smug', arm_l='hip', arm_r='hip', legs='stand'), 3.3), worker=('beach_man', dict(yaw=0.25, expr='happy', arm_l='down', arm_r='down', legs='stand'), 2.9),
            commander=('boss', dict(yaw=0.2, head_roll=-5, expr='smug', arm_l='hip', arm_r='hip', legs='stand'), 3.3), soldier=('senior_a', dict(yaw=0.3, expr='happy', arm_l='down', arm_r='down', legs='stand'), 2.9),
            soldier_b=('senior_b', dict(yaw=-0.3, expr='neutral', arm_l='down', arm_r='down', legs='stand'), 3.1))
HEIGHT = dict(yi=3.3, worker=2.9, commander=3.3, soldier=2.9, soldier_b=3.1)
STAGING = dict(
    roof_low=[('yi', 'yi_quay'), ('worker', 'worker_roof_p2'), ('worker', 'worker_roof_p3')], bow=[('yi', 'yi_bow')], yard_wide=[('yi', 'yi_front'), ('worker', 'worker_quay_a'), ('worker', 'worker_roof_p2'), ('worker', 'worker_roof_p4')],
    roof_top=[('worker', 'worker_roof_p1'), ('worker', 'worker_roof_p2'), ('worker', 'worker_roof_p3'), ('worker', 'worker_roof_p4')], macro_spikes=[], macro_dragon=[],
    fleet_wide=[], flag_deck=[('commander', 'commander_deck'), ('soldier', 'soldier_deck_a'), ('soldier_b', 'soldier_deck_b')], flag_deck_b=[('commander', 'commander_deck')],
    flag_deck_crew=[('soldier', 'soldier_deck_a'), ('soldier_b', 'soldier_deck_b'), ('soldier', 'soldier_deck_c'), ('soldier_b', 'soldier_deck_d')], hansan_high=[], flag_bow=[('commander', 'commander_bow')],
    chase=[('soldier', 'soldier_chase_a'), ('soldier_b', 'soldier_chase_b'), ('soldier', 'soldier_chase_c')], board=[('soldier', 'soldier_board_a'), ('soldier_b', 'soldier_board_b'), ('soldier', 'soldier_board_c')],
    reveal_top=[], aftermath=[], shore=[('commander', 'commander_sand')], macro_oar=[])
def _staging(cam): return [(role, tuple(S['marks'][mk_])) for role, mk_ in STAGING.get(cam, []) if mk_ in S['marks']]

def stage_placeholders(A, cam_name, cam_loc):
    T._clear_actors(); out = []
    for i, (role, mk_) in enumerate(_staging(cam_name)):
        d = Vector(cam_loc) - Vector(mk_); el = math.degrees(math.atan2(d.z - 1.5, math.hypot(d.x, d.y)))
        out.append(T.placeholder_actor(role, mk_, face_to=cam_loc, tilt=max(0.0, el - 35) * 0.6, name='actor_%s_%d' % (role, i)))
    return out

def head_pixels(cam_name):
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; cam = sc.camera; out = []
    for i, (role, mk_) in enumerate(_staging(cam_name)):
        h = HEIGHT[role]; m = Vector(mk_); top, hc, bot = m + Vector((0, 0, h)), m + Vector((0, 0, h - 0.5)), m + Vector((0, 0, h - 1.0))
        p, q, b = (world_to_camera_view(sc, cam, v) for v in (hc, top, bot)); f = world_to_camera_view(sc, cam, m)
        out.append((role, tuple(round(v, 2) for v in mk_), round((1 - p.y) * 1280), round(abs(q.y - b.y) * 1280), round((1 - b.y) * 1280), round((1 - f.y) * 1280)))
    return out

def anchors():
    A = dict(location=S['loc'], preset=S['preset'], cams={k: dict(v) for k, v in S['cams'].items()}, cam=dict(S['cams'][PRESETS[S['preset']]['cam']]), cam_name=PRESETS[S['preset']]['cam'], cam_notes=CAM_NOTES,
             heights=dict(HEIGHT), render=dict(samples=24, adaptive=True, res_pct=75, final=(720, 1280), threads=2, denoise='OIDN', gi=True), staging={k: _staging(k) for k in S['cams']},
             key_dir=tuple(-S['to_sun']), sun_elevation_deg=S['sun_elev'], ships={k: dict(root=v['root'].name, ride=v['ride'].name, L=v['L'], base=tuple(round(c, 2) for c in v['base'])) for k, v in S['ships'].items()})
    A.update(anchors_yard() if S['loc'] == 'yard' else anchors_sea()); return A

# ============================================================================= build()
def build(location=None, preset=None, light=None):
    """Build a location for a preset (LOC_PRESETS) into a fresh scene: path-traced light, world, haze, render settings, the set and the preset's state. Returns anchors()."""
    preset = preset or ('roof_low' if location in (None, 'yard') else 'fleet_wide'); assert preset in PRESETS, preset; loc = PRESETS[preset]['loc']
    bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
    for h in (bpy.app.handlers.render_pre, bpy.app.handlers.frame_change_post):
        for f_ in list(h):
            if getattr(f_, '__name__', '') in ('_cards_face',): h.remove(f_)
    S.clear(); S.update(coll=sc.collection, ships={}, islands={}, loc=loc, preset=preset, vals=dict(s=0.0, k=0.0, d=0.0, sp=''), fk=dict(s=[], k=[], d=[], sp=[]), last_hook='s', jap=[], kor=[], dmg=[], guns=[], parented={}, marks={}); tx_sync()
    setup_world(sc, 1.0); sun = bpy.data.lights.new('key_sun', 'SUN'); sun.color = (1.0, 0.66, 0.40); sun.energy = 7.5; sun.angle = math.radians(1.5)
    so = bpy.data.objects.new('key_sun', sun); sc.collection.objects.link(so); S['sun'] = so; make_materials(); pine_kit()
    make_haze(0.0007 if loc == 'yard' else 0.0009, (0, 0, 60), (1500, 1500, 260))
    if loc == 'yard': build_yard(preset)
    else: build_sea(preset)
    S['exposure'] = 0.55; S['samples'] = PRESETS[preset].get('samples', 24); setup_render(sc, 'final'); apply_state(PRESETS[preset].get('state', ''))
    if loc == 'yard': _yard_marks(); S['cams'] = yard_cams()
    else: _sea_marks(); S['cams'] = sea_cams()
    cam = S['cams'][PRESETS[preset]['cam']]; elev = 15.0 if loc == 'sea' else 17.0; az, el = sun_for_camera(cam, elev); set_sun(az, el); S['sun_elev'] = el
    return anchors()

def apply_state(state):
    """CLI / preset state tokens (comma separated): sp<k> spikes rows, pt<k> ports, ds<level> dragon smoke, s<sec> fleet chase, k<turn> korean turn, cs<level> cannon smoke, dm<k> damage, special:board|solo."""
    sc = bpy.context.scene; f0 = 40; sc.frame_set(f0)
    for tok in [t for t in (state or '').split(',') if t]:
        if tok.startswith('special'): set_special(tok[8:])
        elif tok.startswith('os'): set_oar_splash(float(tok[2:]))
        elif tok.startswith('sp'): set_spikes(float(tok[2:]))
        elif tok.startswith('pt'): set_ports(float(tok[2:]))
        elif tok.startswith('ds'): set_dragon_smoke(float(tok[2:]))
        elif tok.startswith('cs'): set_cannon_smoke(float(tok[2:]))
        elif tok.startswith('dm'): set_damage(float(tok[2:]))
        elif tok.startswith('k'): set_korean_turn(float(tok[1:]))
        elif tok.startswith('s') and S['loc'] == 'sea': set_fleet_chase(float(tok[1:]))
    if S['loc'] == 'sea' and not S['vals']['sp'] and not state: _place(None)
    if S['loc'] == 'sea' and 'k' not in state and 'special' not in state: _place(None)
    if S['loc'] == 'yard' and 'sp' not in state: set_spikes(3)

# ============================================================================= render + post
def post(src, dst, W=720, H=1280):
    """Upscale to 720x1280 (Lanczos) + the R9 grade: bloom on hot spots only (threshold 0.80, tint 1/0.94/0.84), saturation x1.15, mild S-curve, vignette <= 5 %, ceiling 0.985."""
    from PIL import Image, ImageFilter
    im = Image.open(src).convert('RGB')
    if im.size != (W, H): im = im.resize((W, H), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255; yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 1.414; vig = (1 - 0.05 * r ** 2)[..., None]
    lum = a @ np.array([0.2126, 0.7152, 0.0722]); hot = np.clip((lum - 0.80) / 0.2, 0, 1)[..., None] * a; hi = Image.fromarray((hot * 255).astype(np.uint8))
    bloom = sum(np.asarray(hi.filter(ImageFilter.GaussianBlur(rad))).astype(np.float32) / 255 * w for rad, w in ((6, 0.35), (18, 0.30), (48, 0.25)))
    a = a + bloom * np.array([1.0, 0.94, 0.84]) * 0.55; g = a.mean(2, keepdims=True); a = g + (a - g) * 1.15; a = a + 0.06 * (a - a ** 2) * (2 * a - 1) * -1; a = np.clip(a * vig, 0, 0.985)
    Image.fromarray((a * 255 + 0.5).astype(np.uint8)).save(dst)

def render_still(path, quality='final'):
    sc = bpy.context.scene; setup_render(sc, quality); raw = path[:-4] + '_raw.png'; w, c = T.render(raw); post(raw, path); os.remove(raw); return w, c

def _load(): return ' '.join('%.2f' % v for v in os.getloadavg())
def cli_render(specs=None, quality='final', outdir=None, actors=True):
    """spec = preset[:state[:cam]] ; state tokens in apply_state."""
    outdir = outdir or os.path.join(WORK, 'final' if quality == 'final' else 'stills'); os.makedirs(outdir, exist_ok=True); res = {}
    for spec in (specs or list(PRESETS)):
        parts = spec.split(':'); pr = parts[0]; st = parts[1] if len(parts) > 1 and parts[1] else PRESETS[pr].get('state', ''); keep = PRESETS[pr]['state']
        if len(parts) > 1 and parts[1]: PRESETS[pr]['state'] = st
        A = build(None, pr); sc = bpy.context.scene; PRESETS[pr]['state'] = keep
        nm = parts[2] if len(parts) > 2 and parts[2] else A['cam_name']; cs = A['cams'][nm]; make_camera(cs)
        el = S['sun_elev']; az, _ = sun_for_camera(cs, el); set_sun(az, el)
        if actors: stage_placeholders(A, nm, cs['loc'])
        bpy.context.view_layer.update(); hp = head_pixels(nm); tag = (pr if nm == A['cam_name'] else nm) + (('_' + st.replace(',', '_').replace(':', '-')) if len(parts) > 1 and parts[1] else '')
        w, c = render_still(os.path.join(outdir, tag + '.png'), quality); res[tag] = (round(w, 1), round(c, 1), hp)
        print('%s %s: %.1f s wall, %.1f s cpu, load %s, heads %s' % (quality, tag, w, c, _load(), hp), flush=True)
    return res

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'; arg = sys.argv[2:]
    if cmd in ('final', 'stills'): cli_render(arg or None, 'final' if cmd == 'final' else 'preview', actors=os.environ.get('ACTORS', '1') == '1')
    else: print(__doc__)

"""h19_kit.py : shared kit of set3d19 (film 19, Harrison / longitude): painterly two-tone materials, geometry builder (MB), scene helpers,
keying helpers, render setup, grade, camera, placeholder actors, hue measure. Grown from styleboard/machinery.py + part_common.py.

STABLE API (h19_ship.py imports this):
  K.SC = 1.85 (D per metre)      K.W((x,y,z)) metres -> world D tuple      K.STATE (shared dict, reset by h19.build)
  K.hexc, K.lin, K.MATS, K.mat(name, A, B=None, scale=, aniso=, rough=, emit=, emit_k=, zgrad=, wave=, sheen=, contrast=)
  K.mat_emit(name, hex, k), K.metal_mat(name, A, B, rough=, scale=, spec=, metallic=)
  K.MB(name): .box .ell .rod .cyl .cone .quad .tri .push/.pop .finish(coll=None, shadow=True) -> objects (parented to K.ROOT when set)
  K.new_root(name='root') -> empty scaled SC (metres authoring: build children in METRES under it), sets K.ROOT
  K.rnd(seed), K.R, K.gear, K.ring_xy, K.ring_xz, K.curl, K.sphere_brass
  K.area_light(name, loc_m, rot, size_m, col, energy), K.point_light(name, loc_m, col, energy, r_m)  (metres in, energy scaled by SC**2 so a W value reads as in the board)
  K.sun(name, key_rgb, energy, dir_vec, angle_deg)       K.kdir(az, el)
  K.flat_world(col, k, env=...)   K.sky_world(ramp, k, amb)    (interior / outdoor world)
  K._key/_keysock/_setv/_show/_keyxf/clear_keys()    hook keying helpers (frame=None sets now; frame=n keys LINEAR, visibility CONSTANT)
  K.setup_render(scene, quality, samples=None)  K.setup_grade(scene, sat)  K.make_camera(setup)  K.render(path) -> (wall, cpu)
  K.project(pt)  K.head_pixels(staging)  K.placeholder_actor(role, mark, face_to)  K.HEIGHT   K.measure_hue(png)
No depth of field. No text anywhere."""
import os, sys, math, random, time, hashlib
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix, Euler
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))           # film/
SC = 1.85
STATE = {}
ROOT = None

def W(p): return tuple(float(v) * SC for v in p)

def lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def hexc(h):
    h = h.lstrip('#'); return tuple(lin(int(h[i:i + 2], 16)) for i in (0, 2, 4)) + (1.0,)

def new_root(name='root'):
    """empty scaled SC: everything built under it is authored in metres (D = 1.85 x metres)"""
    global ROOT
    ob = bpy.data.objects.new(name, None); ob.scale = (SC, SC, SC); bpy.context.scene.collection.objects.link(ob); ROOT = ob; STATE['root'] = ob; return ob

# ------------------------------------------------------------------ materials
MATS = {}
def mat(name, A, B=None, scale=3.0, aniso=(1, 1, 1), rough=1.0, emit=None, emit_k=0.0, zgrad=None, wave=None, sheen=0.0, contrast=1.0):
    """Principled diffuse with a two-tone object-space noise mix (painterly variation). zgrad=(z0,z1,hexLow): hexLow at z<=z0 to A/B at z>=z1."""
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); bs.name = 'bsdf'
    bs.inputs['Roughness'].default_value = rough
    if 'Specular IOR Level' in bs.inputs: bs.inputs['Specular IOR Level'].default_value = 0.0 if sheen == 0 else sheen
    tc = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (scale * aniso[0], scale * aniso[1], scale * aniso[2])
    L(tc.outputs['Object'], mp.inputs['Vector'])
    if B is not None:
        nz = N('ShaderNodeTexNoise'); nz.inputs['Detail'].default_value = 4; nz.inputs['Roughness'].default_value = 0.6; L(mp.outputs[0], nz.inputs['Vector'])
        cr = N('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.5 - 0.2 / contrast; cr.color_ramp.elements[1].position = 0.5 + 0.2 / contrast
        L(nz.outputs['Fac'], cr.inputs['Fac'])
        mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.inputs[6].default_value = hexc(A); mx.inputs[7].default_value = hexc(B); L(cr.outputs[0], mx.inputs[0]); col = mx.outputs[2]
    else:
        rg = N('ShaderNodeRGB'); rg.outputs[0].default_value = hexc(A); col = rg.outputs[0]
    if wave:
        wv = N('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'X'; wv.inputs['Scale'].default_value = wave[0]; wv.inputs['Distortion'].default_value = 1.5
        wv.inputs['Detail'].default_value = 1; L(tc.outputs['Object'], wv.inputs['Vector'])
        cr2 = N('ShaderNodeValToRGB'); L(wv.outputs['Fac'], cr2.inputs['Fac']); cr2.color_ramp.elements[0].position = 0.35; cr2.color_ramp.elements[1].position = 0.65
        mx2 = N('ShaderNodeMix'); mx2.data_type = 'RGBA'; L(col, mx2.inputs[6]); mx2.inputs[7].default_value = hexc(wave[1]); L(cr2.outputs[0], mx2.inputs[0]); col = mx2.outputs[2]
    if zgrad:
        sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Object'], sp.inputs[0])
        mr = N('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = zgrad[0]; mr.inputs['From Max'].default_value = zgrad[1]; L(sp.outputs['Z'], mr.inputs['Value'])
        mx3 = N('ShaderNodeMix'); mx3.data_type = 'RGBA'; mx3.inputs[6].default_value = hexc(zgrad[2]); L(col, mx3.inputs[7]); L(mr.outputs['Result'], mx3.inputs[0]); col = mx3.outputs[2]
    L(col, bs.inputs['Base Color'])
    if emit:
        bs.inputs['Emission Color'].default_value = hexc(emit); bs.inputs['Emission Strength'].default_value = emit_k
    L(bs.outputs[0], out.inputs['Surface'])
    MATS[name] = m; return m

def mat_emit(name, hexcol, k):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission'); em.name = 'Emission'
    em.inputs['Color'].default_value = hexc(hexcol); em.inputs['Strength'].default_value = k
    nt.links.new(em.outputs[0], out.inputs['Surface']); MATS[name] = m; return m

def metal_mat(name, A, B, rough=0.3, scale=6.0, spec=0.6, metallic=0.0):
    m = mat(name, A, B, scale=scale, rough=rough, sheen=spec)
    bs = m.node_tree.nodes.get('bsdf')
    if bs: bs.inputs['Metallic'].default_value = metallic
    return m

def mat_image(name, path, rough=0.9, emit_k=0.0, spec=0.0, interp='Linear'):
    """textured material from a PNG (painted carpet / pictures); emit_k adds self-light so a picture stays readable"""
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); bs.name = 'bsdf'; tx = N('ShaderNodeTexImage'); tx.image = bpy.data.images.load(path, check_existing=True); tx.interpolation = interp
    bs.inputs['Roughness'].default_value = rough; bs.inputs['Specular IOR Level'].default_value = spec
    L(tx.outputs['Color'], bs.inputs['Base Color'])
    if emit_k > 0: L(tx.outputs['Color'], bs.inputs['Emission Color']); bs.inputs['Emission Strength'].default_value = emit_k
    L(bs.outputs[0], out.inputs['Surface']); MATS[name] = m; return m

# ------------------------------------------------------------------ geometry builder (one object per material)
class MB:
    def __init__(self, name): self.name = name; self.bm = {}; self.T = Matrix.Identity(4); self.stack = []
    def push(self, M): self.stack.append(self.T); self.T = self.T @ M
    def pop(self): self.T = self.stack.pop()
    def _b(self, m):
        if m not in self.bm: self.bm[m] = bmesh.new()
        return self.bm[m]
    def _smooth(self, r):
        for v in r['verts']:
            for f in v.link_faces: f.smooth = True
    def box(self, m, c, s, rz=0.0, rx=0.0, ry=0.0):
        M = self.T @ Matrix.Translation(c) @ Euler((rx, ry, rz)).to_matrix().to_4x4() @ Matrix.Diagonal((s[0], s[1], s[2], 1))
        bmesh.ops.create_cube(self._b(m), size=1.0, matrix=M)
    def ell(self, m, c, r, seg=(12, 8), rot=(0, 0, 0)):
        M = self.T @ Matrix.Translation(c) @ Euler(rot).to_matrix().to_4x4() @ Matrix.Diagonal((r[0], r[1], r[2], 1))
        res = bmesh.ops.create_uvsphere(self._b(m), u_segments=seg[0], v_segments=seg[1], radius=1.0, matrix=M); self._smooth(res)
    def rod(self, m, p0, p1, r0, r1=None, seg=8, caps=True, smooth=False):
        p0 = Vector(p0); p1 = Vector(p1); d = p1 - p0; ln = d.length
        if ln < 1e-6: return
        up = 'X' if abs(d.y) > 0.95 * ln else 'Y'
        M = self.T @ Matrix.Translation((p0 + p1) / 2) @ d.to_track_quat('Z', up).to_matrix().to_4x4()
        res = bmesh.ops.create_cone(self._b(m), cap_ends=caps, cap_tris=False, segments=seg, radius1=r0, radius2=r0 if r1 is None else r1, depth=ln, matrix=M)
        if smooth: self._smooth(res)
    def cyl(self, m, c, r, ln, axis='z', seg=16, smooth=False, r2=None):
        rot = {'z': (0, 0, 0), 'x': (0, math.pi / 2, 0), 'y': (math.pi / 2, 0, 0)}[axis]
        M = self.T @ Matrix.Translation(c) @ Euler(rot).to_matrix().to_4x4()
        res = bmesh.ops.create_cone(self._b(m), cap_ends=True, cap_tris=False, segments=seg, radius1=r, radius2=r if r2 is None else r2, depth=ln, matrix=M)
        if smooth: self._smooth(res)
    def cone(self, m, c, r0, r1, h, seg=16): self.rod(m, (c[0], c[1], c[2]), (c[0], c[1], c[2] + h), r0, r1, seg)
    def quad(self, m, v):
        bm = self._b(m); vs = [bm.verts.new(self.T @ Vector(p)) for p in v]
        try: bm.faces.new(vs)
        except ValueError: pass
    def tri(self, m, v): self.quad(m, v)
    def finish(self, coll=None, shadow=True, parent=None):
        objs = []; par = parent if parent is not None else ROOT
        for m, bm in self.bm.items():
            me = bpy.data.meshes.new('%s_%s' % (self.name, m.name)); bm.to_mesh(me); bm.free()
            ob = bpy.data.objects.new('%s_%s' % (self.name, m.name), me); ob.data.materials.append(m)
            (coll or bpy.context.scene.collection).objects.link(ob); ob.visible_shadow = shadow
            if par is not None: ob.parent = par
            objs.append(ob)
        self.bm = {}; return objs

def rnd(s): return random.Random(s)
def R(a, b, rr): return a + (b - a) * rr.random()

def mesh_from(name, mat_, verts, faces, parent=None, shadow=True, smooth=False, uvs=None):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    if uvs:
        uv = me.uv_layers.new(name='UVMap')
        for poly in me.polygons:
            for li, vi in zip(poly.loop_indices, poly.vertices): uv.data[li].uv = uvs[vi]
    if smooth:
        for p in me.polygons: p.use_smooth = True
    me.materials.append(mat_); ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = shadow
    par = parent if parent is not None else ROOT
    if par is not None: ob.parent = par
    return ob

# ------------------------------------------------------------------ props shared by all locations
def ring(mb, m, ri, ro, th, seg=48):
    """closed annulus in the XZ plane (axis y), thickness th: front/back faces, outer and inner walls, outward normals"""
    bm = mb._b(m); T = mb.T; V = []
    for i in range(seg):
        a = 2 * math.pi * i / seg; c_, s_ = math.cos(a), math.sin(a)
        V.append([bm.verts.new(T @ Vector((rr * c_, yy, rr * s_))) for rr, yy in ((ro, -th / 2), (ri, -th / 2), (ri, th / 2), (ro, th / 2))])
    for i in range(seg):
        A, B = V[i], V[(i + 1) % seg]
        for k in range(4):
            k2 = (k + 1) % 4
            try: bm.faces.new((A[k], B[k], B[k2], A[k2]))
            except ValueError: pass
    bmesh.ops.recalc_face_normals(bm, faces=[f for f in bm.faces if all(v in sum(V, []) for v in f.verts)])

def gear(mb, m, c, r, nt=12, th=0.04, rim=0.03, spokes=4, tooth=0.035, rot=(0, 0, 0), hub=0.05, n=16, hubm=None):
    """gear wheel from boxes: rim ring, teeth, spokes, hub. Built in the XZ plane (axis y); rot orients it. Teeth sit just OUTSIDE the rim (no coplanar faces)"""
    mb.push(Matrix.Translation(c) @ Euler(rot).to_matrix().to_4x4())
    ring(mb, m, r - rim / 2, r + rim / 2, th, max(32, 3 * n))   # director r4: one closed annulus instead of box segments (box joints showed black wedges)
    for i in range(nt):
        a = 2 * math.pi * i / nt; rr_ = r + tooth * .45 + rim / 2
        mb.box(m, (rr_ * math.cos(a), 0, rr_ * math.sin(a)), (tooth, th * 0.96, tooth * 1.1), ry=-a)
    for i in range(spokes):
        a = math.pi * i / spokes
        mb.box(m, (0, 0, 0), (2 * r, th * .8, rim * .8), ry=-a)
    mb.cyl(m, (0, 0, 0), hub, th * 1.7, axis='y', seg=12)
    mb.pop()

def ring_xy(mb, m, c, r, w, h, n=14):
    for i in range(n):
        a = 2 * math.pi * (i + .5) / n; seg = 2 * math.pi * r / n * 1.12
        mb.box(m, (c[0] + r * math.cos(a), c[1] + r * math.sin(a), c[2]), (seg, w, h), rz=a + math.pi / 2)
def ring_xz(mb, m, c, r, w, h, n=14):
    for i in range(n):
        a = 2 * math.pi * (i + .5) / n; seg = 2 * math.pi * r / n * 1.12
        mb.box(m, (c[0] + r * math.cos(a), c[1], c[2] + r * math.sin(a)), (seg, h, w), ry=-(a + math.pi / 2))

def curl(mb, m, p, rr, s=1.0):
    """wood shaving: a thin curled ribbon (chain of thin flat boxes along a loose spiral)"""
    a0 = rr.uniform(0, 6.28); r0 = rr.uniform(0.05, 0.08) * s; n = 8; turn = rr.uniform(0.7, 1.3); yaw = rr.uniform(0, 6.28)
    pts = [Vector((r0 * (1 - 0.35 * i / n) * math.cos(a0 + i / n * turn * 2 * math.pi), 0.012 * i * s, r0 * (1 - 0.35 * i / n) * math.sin(a0 + i / n * turn * 2 * math.pi) + r0 * 1.15)) for i in range(n + 1)]
    mb.push(Matrix.Translation(p) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    for i in range(n):
        a = pts[i]; b = pts[i + 1]; d = b - a
        mb.push(Matrix.Translation((a + b) / 2) @ d.to_track_quat('Z', 'Y').to_matrix().to_4x4()); mb.box(m, (0, 0, 0), (0.026 * s, 0.004, d.length * 1.15)); mb.pop()
    mb.pop()

def sphere_brass(mb, m, c, r): mb.ell(m, c, (r, r, r), (14, 10))

def hang_saw(mb, M, c, ln=0.62, rz=0.0):
    mb.push(Matrix.Translation(c) @ Euler((0, rz, 0)).to_matrix().to_4x4())
    mb.box(M['steel'], (0, 0, 0), (ln, 0.012, 0.075)); mb.box(M['iron'], (0, -0.008, -0.04), (ln, 0.01, 0.014)); mb.box(M['oakd'], (ln / 2 + 0.06, -0.01, 0.0), (0.12, 0.035, 0.11))
    mb.pop()

# ------------------------------------------------------------------ lights (authoring in metres; energies scaled for the SC world)
E2 = SC * SC
def area_light(name, loc, rot, size, col, en, cam=False):
    l = bpy.data.lights.new(name, 'AREA'); l.shape = 'RECTANGLE'; l.size = size[0] * SC; l.size_y = size[1] * SC; l.color = col; l.energy = en * E2
    ob = bpy.data.objects.new(name, l); ob.location = W(loc); ob.rotation_euler = rot; bpy.context.scene.collection.objects.link(ob); ob.visible_camera = cam; STATE.setdefault('lights', {})[name] = (ob, en); return ob
def point_light(name, loc, col, en, r=0.1):
    l = bpy.data.lights.new(name, 'POINT'); l.color = col; l.energy = en * E2; l.shadow_soft_size = r * SC
    ob = bpy.data.objects.new(name, l); ob.location = W(loc); bpy.context.scene.collection.objects.link(ob); STATE.setdefault('lights', {})[name] = (ob, en); return ob
def spot_light(name, loc, target, col, en, r=0.1, blend=0.5, angle=60):
    l = bpy.data.lights.new(name, 'SPOT'); l.color = col; l.energy = en * E2; l.shadow_soft_size = r * SC; l.spot_size = math.radians(angle); l.spot_blend = blend
    ob = bpy.data.objects.new(name, l); ob.location = W(loc); ob.rotation_euler = (Vector(W(target)) - Vector(W(loc))).to_track_quat('-Z', 'Y').to_euler(); bpy.context.scene.collection.objects.link(ob)
    STATE.setdefault('lights', {})[name] = (ob, en); return ob
def sun(name, key, en, direction, angle=1.0):
    d = bpy.data.lights.new(name, 'SUN'); d.color = key[:3]; d.energy = en; d.angle = math.radians(angle)
    o = bpy.data.objects.new(name, d); bpy.context.scene.collection.objects.link(o); o.rotation_euler = (-Vector(direction).normalized()).to_track_quat('Z', 'Y').to_euler(); STATE['sun'] = o; return o
def kdir(az, el):
    a = math.radians(az); e = math.radians(el)
    return (-math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), -math.sin(e))

def flat_world(col, k, env=('#ffd6a0', 2.2)):
    """interior world: camera/diffuse rays see a flat colour (strength k); glossy rays see a warm room-like environment so brass reads as metal"""
    w = bpy.data.worlds.new('sky'); bpy.context.scene.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputWorld'); b1 = N('ShaderNodeBackground'); b1.name = 'skybg'; b1.inputs['Color'].default_value = hexc(col); b1.inputs['Strength'].default_value = k
    b2 = N('ShaderNodeBackground'); b2.name = 'envbg'; b2.inputs['Color'].default_value = hexc(env[0]); b2.inputs['Strength'].default_value = env[1]
    lp = N('ShaderNodeLightPath'); mx = N('ShaderNodeMixShader'); L(lp.outputs['Is Glossy Ray'], mx.inputs[0]); L(b1.outputs[0], mx.inputs[1]); L(b2.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    STATE['world'] = w

def sky_world(stops, k, amb=None):
    """outdoor world: camera rays see the vertical gradient `stops` [(pos, hex)...] (named node 'skyramp'), other rays see a flat blue-violet ambient amb=(hex, strength)"""
    w = bpy.data.worlds.new('sky'); bpy.context.scene.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputWorld'); bg = N('ShaderNodeBackground'); bg.name = 'skybg'; tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Generated'], sp.inputs[0])
    cr = N('ShaderNodeValToRGB'); cr.name = 'skyramp'; L(sp.outputs['Z'], cr.inputs[0])
    cr.color_ramp.elements[0].position = stops[0][0]; cr.color_ramp.elements[0].color = hexc(stops[0][1])
    for pos, col in stops[1:-1]:
        e = cr.color_ramp.elements.new(pos); e.color = hexc(col)
    cr.color_ramp.elements[-1].position = stops[-1][0]; cr.color_ramp.elements[-1].color = hexc(stops[-1][1])
    bg.inputs['Strength'].default_value = k; L(cr.outputs[0], bg.inputs['Color'])
    if amb:
        lp = N('ShaderNodeLightPath'); b2 = N('ShaderNodeBackground'); b2.name = 'ambbg'; b2.inputs['Color'].default_value = hexc(amb[0]); b2.inputs['Strength'].default_value = amb[1]
        mx = N('ShaderNodeMixShader'); L(lp.outputs['Is Camera Ray'], mx.inputs[0]); L(b2.outputs[0], mx.inputs[1]); L(bg.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    else: L(bg.outputs[0], out.inputs['Surface'])
    STATE['world'] = w

# ------------------------------------------------------------------ keying helpers (as film 16: LINEAR numbers, CONSTANT visibility)
def _fcurves(idb):
    ad = idb.animation_data; out = []
    if not ad or not ad.action: return out
    act = ad.action
    try:
        for layer in act.layers:
            for strip in layer.strips:
                for cb in strip.channelbags: out += list(cb.fcurves)
    except Exception: pass
    if not out and hasattr(act, 'fcurves'): out = list(act.fcurves)
    return out
def _key(idb, path, frame, interp='LINEAR', index=-1):
    idb.keyframe_insert(path, frame=frame, index=index)
    for fc in _fcurves(idb):
        if fc.data_path == path or fc.data_path.startswith(path):
            for kp in fc.keyframe_points:
                if abs(kp.co[0] - frame) < 1e-3: kp.interpolation = interp
def _keysock(sock, value, frame, interp='LINEAR'):
    sock.default_value = value
    if frame is not None:
        sock.keyframe_insert('default_value', frame=frame)
        for fc in _fcurves(sock.id_data):
            if 'default_value' in fc.data_path:
                for kp in fc.keyframe_points:
                    if abs(kp.co[0] - frame) < 1e-3: kp.interpolation = interp
def _setv(ob, vis, frame=None):
    ob.hide_render = not vis
    if frame is not None: _key(ob, 'hide_render', frame, 'CONSTANT')
def _show(objs, vis, frame=None):
    for o in (objs if isinstance(objs, (list, tuple)) else [objs]): _setv(o, vis, frame)
def _keyxf(ob, frame, loc=True, rot=False, scl=False, interp='LINEAR'):
    if frame is None: return
    if loc: _key(ob, 'location', frame, interp)
    if rot: _key(ob, 'rotation_euler', frame, interp)
    if scl: _key(ob, 'scale', frame, interp)
def _keylight(ob, value_m, frame):
    """light energy (value in authoring W) keyed/set; ob is a light object"""
    ob.data.energy = value_m * E2
    if frame is not None: _key(ob.data, 'energy', frame, 'LINEAR')

def clear_keys():
    """Drop every key the hooks inserted (objects, lights, materials, node trees, world, scene) so plain set_* calls hold again."""
    for idb in list(bpy.data.objects) + list(bpy.data.lights) + list(bpy.data.cameras):
        ad = idb.animation_data
        if ad and ad.action: ad.action = None
    for coll in (bpy.data.materials, bpy.data.node_groups, bpy.data.worlds):
        for m in coll:
            nt = getattr(m, 'node_tree', None) if coll is not bpy.data.node_groups else m
            if nt is not None and nt.animation_data: nt.animation_data_clear()
    sc = bpy.context.scene
    for idb in (sc, sc.view_settings):
        if getattr(idb, 'animation_data', None): idb.animation_data_clear()

# ------------------------------------------------------------------ render, grade, camera
FINAL_SAMPLES = 10
def setup_render(scene, quality='final', samples=None):
    """final 720x1280 (preview 360x640), Cycles CPU, few samples + OpenImageDenoise, direct light only (no diffuse bounce), 2 threads"""
    r = scene.render; c = scene.cycles; r.engine = 'CYCLES'; c.device = 'CPU'
    r.resolution_x, r.resolution_y = 720, 1280; r.resolution_percentage = 100 if quality in ('final', 'hq') else 50
    c.samples = samples or {'final': STATE.get('samples', FINAL_SAMPLES), 'hq': 24}.get(quality, 6)
    c.use_denoising = True; c.denoiser = 'OPENIMAGEDENOISE'; c.denoising_input_passes = 'RGB_ALBEDO_NORMAL'; c.denoising_prefilter = 'FAST'
    c.use_adaptive_sampling = False
    c.max_bounces = 2; c.diffuse_bounces = STATE.get('dbounce', 0); c.glossy_bounces = 1; c.transmission_bounces = 0; c.transparent_max_bounces = 8
    c.use_light_tree = False; c.filter_width = 1.2; r.threads_mode = 'FIXED'; r.threads = 2
    scene.view_settings.view_transform = 'Standard'; scene.view_settings.look = 'None'
    r.image_settings.file_format = 'PNG'; r.image_settings.color_mode = 'RGB'; r.film_transparent = False

def setup_grade(scene, sat=1.08):
    """film-wide mild saturation grade (compositor from spec/grade_compositor): no recolour"""
    sys.path.insert(0, os.path.join(PROJ, 'spec'))
    import warnings, grade_compositor as G
    for ng in list(bpy.data.node_groups):
        if ng.name.startswith('GradeCLP'): bpy.data.node_groups.remove(ng)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        G.build(scene, preset=dict(vignette_strength=0.0, bloom_strength=0.0, offset=(0.0, 0.0, 0.0), saturation=float(sat)))
    scene.render.use_compositing = True

def make_camera(setup, name='cam', scene=None):
    """22 mm / 36 mm sensor camera from {loc, look_at, lens[, roll]} (world D): DOF OFF, clip 0.05..2000"""
    scene = scene or bpy.context.scene
    ob = bpy.data.objects.get(name)
    if ob is None:
        cd = bpy.data.cameras.new(name); ob = bpy.data.objects.new(name, cd); scene.collection.objects.link(ob)
    cd = ob.data; cd.lens = setup.get('lens', 22); cd.sensor_width = 36; cd.sensor_fit = 'AUTO'; cd.clip_start = 0.05; cd.clip_end = 2000; cd.dof.use_dof = False
    ob.location = setup['loc']; ob.rotation_euler = (Vector(setup['look_at']) - Vector(setup['loc'])).to_track_quat('-Z', 'Y').to_euler()
    if setup.get('roll'): ob.rotation_euler.rotate_axis('Z', math.radians(setup['roll']))
    scene.camera = ob; STATE['cam'] = ob
    if STATE.get('caption_shade'): caption_shade(ob, **STATE['caption_shade'])
    return ob

def caption_shade(cam, y0=770, y1=900, a1=0.50, a2=0.62, col='#120c0c', name='caption_shade'):
    """foreground shadow for the caption band: a camera-attached card (camera rays only: no light / shadow / glossy effect) that blends the frame toward a dark warm brown from pixel row y0 (0 %)
    through y1 (a1) to the bottom edge (a2). It reads as a soft foreground shadow / vignette, keeps y 880-950 calm and dim. Opt-in per location: STATE['caption_shade'] = dict(...) before make_camera."""
    old = bpy.data.objects.get(name)
    if old is not None: bpy.data.objects.remove(old, do_unlink=True)
    d = 0.4; H_ = 2 * d * 18.0 / cam.data.lens; W_ = H_ * 720 / 1280.0
    me = bpy.data.meshes.new(name); me.from_pydata([(-W_ / 2 * 1.02, -H_ / 2 * 1.02, 0), (W_ / 2 * 1.02, -H_ / 2 * 1.02, 0), (W_ / 2 * 1.02, H_ / 2 * 1.02, 0), (-W_ / 2 * 1.02, H_ / 2 * 1.02, 0)], [], [(0, 1, 2, 3)]); me.update()
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); ob.parent = cam; ob.location = (0, 0, -d)
    for a in ('visible_diffuse', 'visible_glossy', 'visible_transmission', 'visible_volume_scatter', 'visible_shadow'): setattr(ob, a, False)
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); cr = N('ShaderNodeMapRange')
    em.inputs['Color'].default_value = hexc(col); em.inputs['Strength'].default_value = 1.0
    # object-space y of the card: -H/2 (bottom row 1280) .. +H/2 (top row 0); row = (0.5 - y / H) * 1280
    L(tc.outputs['Object'], sp.inputs[0]); rowm = N('ShaderNodeMath'); rowm.operation = 'MULTIPLY_ADD'; rowm.inputs[1].default_value = -1280.0 / (H_ * 1.0); rowm.inputs[2].default_value = 640.0; L(sp.outputs['Y'], rowm.inputs[0])
    cr.data_type = 'FLOAT'; cr.interpolation_type = 'SMOOTHERSTEP'; cr.inputs['From Min'].default_value = y0; cr.inputs['From Max'].default_value = y1; cr.inputs['To Min'].default_value = 0.0; cr.inputs['To Max'].default_value = a1; cr.clamp = True
    L(rowm.outputs[0], cr.inputs['Value'])
    cr2 = N('ShaderNodeMapRange'); cr2.interpolation_type = 'LINEAR'; cr2.inputs['From Min'].default_value = y1; cr2.inputs['From Max'].default_value = 1280; cr2.inputs['To Min'].default_value = a1; cr2.inputs['To Max'].default_value = a2; cr2.clamp = True; L(rowm.outputs[0], cr2.inputs['Value'])
    add = N('ShaderNodeMath'); add.operation = 'MAXIMUM'; L(cr.outputs[0], add.inputs[0]); L(cr2.outputs[0], add.inputs[1])
    gate = N('ShaderNodeMath'); gate.operation = 'GREATER_THAN'; gate.inputs[1].default_value = y1; L(rowm.outputs[0], gate.inputs[0])
    sel = N('ShaderNodeMix'); sel.data_type = 'FLOAT'; L(gate.outputs[0], sel.inputs[0]); L(cr.outputs[0], sel.inputs[2]); L(cr2.outputs[0], sel.inputs[3])
    L(sel.outputs[0], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    ob.data.materials.append(m); return ob

def render(path, scene=None):
    scene = scene or bpy.context.scene; scene.render.filepath = path
    t0 = time.time(); c0 = os.times(); bpy.ops.render.render(write_still=True); c1 = os.times()
    return time.time() - t0, (c1.user - c0.user) + (c1.system - c0.system)

def project(world_pt):
    """(x_px, y_px) of a world point in the scene camera (720x1280, y from the top)"""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; p = world_to_camera_view(sc, sc.camera, Vector(world_pt)); return round(p.x * 720), round((1 - p.y) * 1280)

# ------------------------------------------------------------------ placeholder actors (tower.placeholder_actor, cast roles)
HEIGHT = dict(harrison=3.2, william=3.0, mocker=3.1, astro=3.1, king=3.2, captain=3.2, sailor=3.0, visitor=3.1, clerk=3.0, boy=2.4)
_PH_DONE = []
def _import_tower():
    p = os.path.join(PROJ, 'v3', 'set3d2')
    if p not in sys.path: sys.path.insert(0, p)
    import tower as T
    if not _PH_DONE:
        T.PH.update(
            harrison=('senior_a', dict(yaw=0.25, expr='determined', arm_l='down', arm_r='down', legs='stand'), HEIGHT['harrison']),
            william=('beach_man', dict(yaw=-0.25, expr='happy', arm_l='down', arm_r='down', legs='stand'), HEIGHT['william']),
            mocker=('boss', dict(yaw=0.3, head_roll=-4, expr='smug', arm_l='hip', arm_r='hip', legs='stand'), HEIGHT['mocker']),
            astro=('senior_b', dict(yaw=0.2, expr='neutral', arm_l='down', arm_r='down', legs='stand'), HEIGHT['astro']),
            king=('boss', dict(yaw=-0.2, expr='neutral', arm_l='down', arm_r='down', legs='stand'), HEIGHT['king']),
            captain=('senior_a', dict(yaw=0.2, expr='neutral', arm_l='down', arm_r='down', legs='stand'), HEIGHT['captain']),
            sailor=('beach_man', dict(yaw=0.2, expr='neutral', arm_l='down', arm_r='down', legs='stand'), HEIGHT['sailor']),
            visitor=('beach_woman', dict(yaw=-0.2, expr='neutral', arm_l='down', arm_r='down', legs='stand'), HEIGHT['visitor']),
            clerk=('senior_b', dict(yaw=0.2, expr='neutral', arm_l='down', arm_r='down', legs='stand'), HEIGHT['clerk']))
        _PH_DONE.append(1)
    return T
def placeholder_actor(role, mark, face_to=None, tilt=0.0, name=None, ppd=256):
    T = _import_tower(); return T.placeholder_actor(role, tuple(mark), face_to=face_to, tilt=tilt, name=name, ppd=ppd)
def clear_actors():
    for o in list(bpy.context.scene.objects):
        if o.name.startswith('actor_'): bpy.data.objects.remove(o, do_unlink=True)
def stage_placeholders(staging, cam_loc, parent=None):
    """staging: [(role, (x, y, z) world D mark)]"""
    clear_actors(); out = []
    for i, (role, mk) in enumerate(staging):
        d = Vector(cam_loc) - Vector(mk); el = math.degrees(math.atan2(d.z - 1.5, math.hypot(d.x, d.y)))
        a = placeholder_actor(role, tuple(mk), face_to=cam_loc, tilt=max(0.0, el - 35) * 0.6, name='actor_%s_%d' % (role, i))
        if parent is not None: a.parent = parent; a.matrix_parent_inverse = parent.matrix_world.inverted()
        out.append(a)
    return out
def head_pixels(staging):
    """[(role, mark, head_centre_y_px, head_px, chin_y_px, feet_y_px, head_x_px)] at 720x1280 (caption rule: chin < 880)"""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; cam = sc.camera; out = []
    for role, mk in staging:
        h = HEIGHT[role]; m = Vector(mk); top, hc, bot = m + Vector((0, 0, h)), m + Vector((0, 0, h - 0.5)), m + Vector((0, 0, h - 1.0))
        p, q, b = (world_to_camera_view(sc, cam, v) for v in (hc, top, bot)); f = world_to_camera_view(sc, cam, m)
        out.append((role, tuple(round(v, 2) for v in mk), round((1 - p.y) * 1280), round(abs(q.y - b.y) * 1280), round((1 - b.y) * 1280), round((1 - f.y) * 1280), round(p.x * 720)))
    return out

# ------------------------------------------------------------------ hue measure (method of styleboard/hue_check.py: cast-shadow pixels from a sun-only render)
def _rd(sc, path, samples, transp):
    cy = sc.cycles; cy.samples = samples; cy.use_denoising = False; sc.render.film_transparent = transp; sc.render.filepath = path
    bpy.ops.render.render(write_still=True); a = np.asarray(Image.open(path).convert('RGBA'), dtype=np.float32) / 255.0; os.remove(path); return a

def measure_hue(png, tmp=None, hide_prefix=('clouds', 'shafts', 'rain', 'actor_', 'sun_', 'foam', 'spray', 'glass', 'caption_shade')):
    sc = bpy.context.scene; cy = sc.cycles; tmp = tmp or png[:-4]
    saved = dict(samples=cy.samples, den=cy.use_denoising, mb=cy.max_bounces, db=cy.diffuse_bounces, gb=cy.glossy_bounces, comp=sc.render.use_compositing, tr=sc.render.film_transparent,
                 cm=sc.render.image_settings.color_mode, exp=sc.view_settings.exposure)
    sc.render.image_settings.color_mode = 'RGBA'; sc.render.use_compositing = False; sc.view_settings.exposure = 0.0
    lights = [(l, l.data.energy) for l in bpy.data.objects if l.type == 'LIGHT' and l.data.type != 'SUN']
    for l, e in lights: l.data.energy = 0.0
    wnt = bpy.context.scene.world.node_tree; wb = [n for n in wnt.nodes if n.bl_idname == 'ShaderNodeBackground']; wv = [n.inputs['Strength'].default_value for n in wb]
    for n in wb: n.inputs['Strength'].default_value = 0.0
    hid = [o for o in bpy.data.objects if o.name.startswith(hide_prefix)]; hv = [o.hide_render for o in hid]
    for o in hid: o.hide_render = True
    wm = bpy.data.materials.new('ovr'); wm.use_nodes = True; bs = wm.node_tree.nodes['Principled BSDF']; bs.inputs['Base Color'].default_value = (1, 1, 1, 1); bs.inputs['Roughness'].default_value = 1.0; bs.inputs['Specular IOR Level'].default_value = 0.0
    cy.max_bounces = 0; cy.diffuse_bounces = 0; cy.glossy_bounces = 0; bpy.context.view_layer.material_override = wm
    D = _rd(sc, tmp + '_D.png', 16, True); lD = 0.3 * D[..., 0] + 0.59 * D[..., 1] + 0.11 * D[..., 2]
    vs = [(o, o.visible_shadow) for o in bpy.data.objects if o.type == 'MESH']
    for o, _ in vs: o.visible_shadow = False
    D2 = _rd(sc, tmp + '_D2.png', 6, True); bpy.context.view_layer.material_override = None
    for o, v in vs: o.visible_shadow = v
    lD2 = 0.3 * D2[..., 0] + 0.59 * D2[..., 1] + 0.11 * D2[..., 2]
    for l, e in lights: l.data.energy = e
    for n, v in zip(wb, wv): n.inputs['Strength'].default_value = v
    for o, v in zip(hid, hv): o.hide_render = v
    bpy.data.materials.remove(wm)
    cy.samples = saved['samples']; cy.use_denoising = saved['den']; cy.max_bounces = saved['mb']; cy.diffuse_bounces = saved['db']; cy.glossy_bounces = saved['gb']
    sc.render.use_compositing = saved['comp']; sc.render.film_transparent = saved['tr']; sc.render.image_settings.color_mode = saved['cm']; sc.view_settings.exposure = saved['exp']
    cast = (D[..., 3] > 0.99) & (lD < 0.02) & (lD2 > 0.08)
    mask = np.asarray(Image.fromarray((cast * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)), dtype=np.float32) > 127
    im = Image.open(png).convert('RGB'); hsv = np.asarray(im.convert('HSV'), dtype=np.float32).reshape(-1, 3)
    h = hsv[:, 0] * 360 / 255; s = hsv[:, 1] / 255; v = hsv[:, 2] / 255
    m = mask.reshape(-1); sel = m & (s > 0.1) & (v > 0.06)
    mag = float(((h >= 290) & (h <= 340) & (s > 0.25)).mean() * 100)
    if sel.sum() < 200: return dict(shade_hue=None, median=None, cast_pct=round(float(m.mean() * 100), 1), in_band=None, magenta=round(mag, 2), ok=mag <= 10)
    ang = np.deg2rad(h[sel]); mh = float((np.rad2deg(np.arctan2(np.sin(ang).mean(), np.cos(ang).mean())) + 360) % 360)
    inb = float(((h >= 225) & (h <= 265))[sel].mean() * 100)
    return dict(shade_hue=round(mh, 1), median=round(float(np.median(h[sel])), 1), cast_pct=round(float(m.mean() * 100), 1), in_band=round(inb, 1), magenta=round(mag, 2), ok=(225 <= mh <= 265) and mag <= 10)

def shafts(kd, rect, zfloor=0.0, k=4.0, a=0.02, name='shafts', col='#ffd890'):
    """faint light-shaft volume: the window rectangle (x0, x1, z0, z1, y; metres) projected along the sun direction kd to the floor (emission / transparent mix, no shadows)"""
    kd = Vector(kd).normalized(); (x0, x1, z0, z1, y) = rect
    corners = [Vector((x0, y, z0)), Vector((x1, y, z0)), Vector((x1, y, z1)), Vector((x0, y, z1))]
    proj = [c + kd * ((zfloor - c.z) / kd.z) for c in corners]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    em.inputs['Color'].default_value = hexc(col); em.inputs['Strength'].default_value = k; mx.inputs[0].default_value = a
    L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    mb = MB(name)
    for i in range(4):
        j = (i + 1) % 4; mb.quad(m, [corners[i], corners[j], proj[j], proj[i]]); mb.quad(m, [proj[i], proj[j], corners[j], corners[i]])
    objs = mb.finish(shadow=False); STATE.setdefault('shafts', []).extend(objs); return objs

"""set3d19 style board: John Harrison / longitude (1730s-1760s). Self-contained bpy scene (procedural geometry + shaders), Cycles CPU.
usage: python3 sb.py shop|ship|hall|all [draft]   -> sb1_workshop.jpg / sb2_ship.jpg / sb3_hall.jpg (d_*.jpg = 360x640 drafts)
Machinery (painterly two-tone noise materials, MB builder, sky world, sun + blue-violet ambient, camera 22mm/36mm, compositor-free sat 1.08 grade) copied from film 16 sb.py.
World units: metres. +x right, +y away from camera, z up. 720x1280, no DOF. No text anywhere."""
import os, sys, math, random, time
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix, Euler
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 720, 1280

def lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def hexc(h):
    h = h.lstrip('#'); return tuple(lin(int(h[i:i + 2], 16)) for i in (0, 2, 4)) + (1.0,)

# ------------------------------------------------------------------ materials
MATS = {}
def mat(name, A, B=None, scale=3.0, aniso=(1, 1, 1), rough=1.0, emit=None, emit_k=0.0, zgrad=None, wave=None, sheen=0.0, contrast=1.0):
    """Principled diffuse with a two-tone object-space noise mix (painterly variation). zgrad=(z0,z1,hexLow) blends hexLow at z<=z0 to A/B at z>=z1.
    wave=(freq, hexStripe): corrugation stripes along x. emit: emission colour hex with strength emit_k."""
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled')
    bs.inputs['Roughness'].default_value = rough
    for k in ('Specular IOR Level',):
        if k in bs.inputs: bs.inputs[k].default_value = 0.0 if sheen == 0 else sheen
    tc = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (scale * aniso[0], scale * aniso[1], scale * aniso[2])
    L(tc.outputs['Object'], mp.inputs['Vector'])
    col = None
    if B is not None:
        nz = N('ShaderNodeTexNoise'); nz.inputs['Detail'].default_value = 4; nz.inputs['Roughness'].default_value = 0.6; L(mp.outputs[0], nz.inputs['Vector'])
        cr = N('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.5 - 0.2 / contrast; cr.color_ramp.elements[1].position = 0.5 + 0.2 / contrast
        L(nz.outputs['Fac'], cr.inputs['Fac'])
        mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.inputs[6].default_value = hexc(A); mx.inputs[7].default_value = hexc(B); L(cr.outputs[0], mx.inputs[0])
        col = mx.outputs[2]
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
    out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = hexc(hexcol); em.inputs['Strength'].default_value = k
    nt.links.new(em.outputs[0], out.inputs['Surface']); MATS[name] = m; return m

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
        M = self.T @ Matrix.Translation((p0 + p1) / 2) @ d.to_track_quat('Z', 'Y').to_matrix().to_4x4()
        res = bmesh.ops.create_cone(self._b(m), cap_ends=caps, cap_tris=False, segments=seg, radius1=r0, radius2=r0 if r1 is None else r1, depth=ln, matrix=M)
        if smooth: self._smooth(res)
    def cone(self, m, c, r0, r1, h, seg=16, rz=0.0):
        self.rod(m, (c[0], c[1], c[2]), (c[0], c[1], c[2] + h), r0, r1, seg)
    def quad(self, m, v):
        bm = self._b(m); vs = [bm.verts.new(self.T @ Vector(p)) for p in v]
        try: bm.faces.new(vs)
        except ValueError: pass
    def tri(self, m, v): self.quad(m, v)
    def finish(self, coll=None, shadow=True):
        objs = []
        shadow = shadow and self.name not in ('moon', 'hills')
        for m, bm in self.bm.items():
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
            me = bpy.data.meshes.new('%s_%s' % (self.name, m.name)); bm.to_mesh(me); bm.free()
            ob = bpy.data.objects.new('%s_%s' % (self.name, m.name), me); ob.data.materials.append(m)
            (coll or bpy.context.scene.collection).objects.link(ob); ob.visible_shadow = shadow; objs.append(ob)
        self.bm = {}; return objs

def rnd(s): return random.Random(s)
def R(a, b, rr): return a + (b - a) * rr.random()


# ------------------------------------------------------------------ extra builder methods
def _rod(self, m, p0, p1, r0, r1=None, seg=8, caps=True, smooth=False):
    p0 = Vector(p0); p1 = Vector(p1); d = p1 - p0; ln = d.length
    if ln < 1e-6: return
    up = 'X' if abs(d.y) > 0.95 * ln else 'Y'
    M = self.T @ Matrix.Translation((p0 + p1) / 2) @ d.to_track_quat('Z', up).to_matrix().to_4x4()
    res = bmesh.ops.create_cone(self._b(m), cap_ends=caps, cap_tris=False, segments=seg, radius1=r0, radius2=r0 if r1 is None else r1, depth=ln, matrix=M)
    if smooth: self._smooth(res)
MB.rod = _rod
def _cyl(self, m, c, r, ln, axis='z', seg=16, smooth=False, r2=None):
    rot = {'z': (0, 0, 0), 'x': (0, math.pi / 2, 0), 'y': (math.pi / 2, 0, 0)}[axis]
    M = self.T @ Matrix.Translation(c) @ Euler(rot).to_matrix().to_4x4()
    res = bmesh.ops.create_cone(self._b(m), cap_ends=True, cap_tris=False, segments=seg, radius1=r, radius2=r if r2 is None else r2, depth=ln, matrix=M)
    if smooth: self._smooth(res)
MB.cyl = _cyl

def sky_world(P):
    w = bpy.data.worlds.new('sky'); bpy.context.scene.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputWorld'); bg = N('ShaderNodeBackground'); tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Generated'], sp.inputs[0])
    cr = N('ShaderNodeValToRGB'); L(sp.outputs['Z'], cr.inputs[0]); stops = P['sky']
    cr.color_ramp.elements[0].position = stops[0][0]; cr.color_ramp.elements[0].color = hexc(stops[0][1])
    for pos, col in stops[1:-1]:
        e = cr.color_ramp.elements.new(pos); e.color = hexc(col)
    cr.color_ramp.elements[-1].position = stops[-1][0]; cr.color_ramp.elements[-1].color = hexc(stops[-1][1])
    bg.inputs['Strength'].default_value = P['sky_k']; L(cr.outputs[0], bg.inputs['Color'])
    if P.get('amb'):     # non-camera rays (lighting) see a flat blue-violet sky ambient; camera rays see the painted sky gradient
        lp = N('ShaderNodeLightPath'); b2 = N('ShaderNodeBackground'); b2.inputs['Color'].default_value = hexc(P['amb'][0]); b2.inputs['Strength'].default_value = P['amb'][1]
        mx = N('ShaderNodeMixShader'); L(lp.outputs['Is Camera Ray'], mx.inputs[0]); L(b2.outputs[0], mx.inputs[1]); L(bg.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    else: L(bg.outputs[0], out.inputs['Surface'])

def kdir(az, el):
    a = math.radians(az); e = math.radians(el)
    return (-math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), -math.sin(e))

def setup_camera(P):
    sc = bpy.context.scene; c = P['cam']
    cd = bpy.data.cameras.new('cam'); cd.lens = c['lens']; cd.sensor_width = 36; cd.sensor_fit = 'AUTO'; cd.dof.use_dof = False
    ob = bpy.data.objects.new('cam', cd); sc.collection.objects.link(ob); ob.location = c['loc']
    ob.rotation_euler = (Vector(c['look']) - Vector(c['loc'])).to_track_quat('-Z', 'Y').to_euler(); sc.camera = ob

def grade(a, P):
    g = a.mean(-1, keepdims=True); return np.clip(g + (a - g) * P.get('sat', 1.08), 0, 1)

def _rd(sc, path, samples, denoise, transp=False):
    cy = sc.cycles; cy.samples = samples; cy.use_denoising = denoise; sc.render.film_transparent = transp
    sc.render.filepath = path; bpy.ops.render.render(write_still=True)
    im = Image.open(path).convert('RGBA'); a = np.asarray(im, dtype=np.float32) / 255.0; os.remove(path); return a


# ================================================================== common helpers (set3d19)
def metal_mat(name, A, B, rough=0.3, scale=6.0, spec=0.6, metallic=0.0):
    m = mat(name, A, B, scale=scale, rough=rough, sheen=spec)
    bs = m.node_tree.nodes.get('Principled BSDF')
    if bs: bs.inputs['Metallic'].default_value = metallic
    return m

def gear(mb, m, c, r, nt=12, th=0.04, rim=0.03, spokes=4, tooth=0.035, rot=(0, 0, 0), hub=0.05, n=16):
    """wooden/brass gear wheel built from boxes: rim ring, teeth, spokes, hub. Built in the XZ plane (axis y); rot orients it."""
    mb.push(Matrix.Translation(c) @ Euler(rot).to_matrix().to_4x4())
    for i in range(n):
        a = 2 * math.pi * (i + .5) / n; seg = 2 * math.pi * r / n * 1.10
        mb.box(m, (r * math.cos(a), 0, r * math.sin(a)), (seg, th, rim), ry=-(a + math.pi / 2))
    for i in range(nt):
        a = 2 * math.pi * i / nt; rr = r + tooth * .45 + rim / 2
        mb.box(m, (rr * math.cos(a), 0, rr * math.sin(a)), (tooth, th, tooth * 1.1), ry=-a)
    for i in range(spokes):
        a = math.pi * i / spokes
        mb.box(m, (0, 0, 0), (2 * r, th * .8, rim * .8), ry=-a)
    mb.cyl(m, (0, 0, 0), hub, th * 1.7, axis='y', seg=12)
    mb.pop()

def ring_xy(mb, m, c, r, w, h, n=14):
    """flat ring (rope coil / hoop) in the XY plane, section w (radial) x h (z)"""
    for i in range(n):
        a = 2 * math.pi * (i + .5) / n; seg = 2 * math.pi * r / n * 1.12
        mb.box(m, (c[0] + r * math.cos(a), c[1] + r * math.sin(a), c[2]), (seg, w, h), rz=a + math.pi / 2)

def ring_xz(mb, m, c, r, w, h, n=14):
    for i in range(n):
        a = 2 * math.pi * (i + .5) / n; seg = 2 * math.pi * r / n * 1.12
        mb.box(m, (c[0] + r * math.cos(a), c[1], c[2] + r * math.sin(a)), (seg, h, w), ry=-(a + math.pi / 2))

def curl_old(mb, m, p, rr, s=1.0):
    """wood shaving: a short curled ribbon (chain of thin boxes along an arc)"""
    a0 = rr.uniform(0, 6.28); r = rr.uniform(0.03, 0.055) * s; n = 7; turn = rr.uniform(4.0, 6.5); yaw = rr.uniform(0, 6.28)
    pts = []
    for i in range(n + 1):
        t = i / n * turn; pts.append((r * (1 + 0.25 * i / n) * math.cos(a0 + t), 0.012 * i * s * 3, r * (1 + 0.25 * i / n) * math.sin(a0 + t) + r * 1.1))
    mb.push(Matrix.Translation(p) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    for i in range(n):
        a = Vector(pts[i]); b = Vector(pts[i + 1]); d = b - a
        mb.rod(m, a, b, 0.0075 * s, 0.0075 * s, seg=4, caps=False)
    mb.pop()

def pile(mb, m, c, s, rr):
    mb.ell(m, (c[0], c[1], c[2] + 0.02 * s), (0.16 * s, 0.12 * s, 0.045 * s), (10, 6))

def hang_saw(mb, M, c, ln=0.62, rz=0.0):
    mb.push(Matrix.Translation(c) @ Euler((0, rz, 0)).to_matrix().to_4x4())
    mb.box(M['steel'], (0, 0, 0), (ln, 0.012, 0.075))
    mb.box(M['iron'], (0, -0.008, -0.04), (ln, 0.01, 0.014))
    mb.box(M['oakd'], (ln / 2 + 0.06, -0.01, 0.0), (0.12, 0.035, 0.11))
    mb.pop()

def sphere_brass(mb, m, c, r): mb.ell(m, c, (r, r, r), (14, 10))

def area_light(name, loc, rot, size, col, en, cam=False):
    sc = bpy.context.scene
    l = bpy.data.lights.new(name, 'AREA'); l.shape = 'RECTANGLE'; l.size = size[0]; l.size_y = size[1]; l.color = col; l.energy = en
    ob = bpy.data.objects.new(name, l); ob.location = loc; ob.rotation_euler = rot; sc.collection.objects.link(ob); ob.visible_camera = cam; return ob
def point_light(name, loc, col, en, r=0.1):
    sc = bpy.context.scene
    l = bpy.data.lights.new(name, 'POINT'); l.color = col; l.energy = en; l.shadow_soft_size = r
    ob = bpy.data.objects.new(name, l); ob.location = loc; sc.collection.objects.link(ob); return ob
def sun_light(P):
    sc = bpy.context.scene; k = P['key']; kd = Vector(P['key_dir']).normalized()
    d = bpy.data.lights.new('key', 'SUN'); d.color = k[:3]; d.energy = k[3]; d.angle = math.radians(P['sun_angle'])
    o = bpy.data.objects.new('key', d); sc.collection.objects.link(o); o.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler()

def flat_world(col, k):
    w = bpy.data.worlds.new('sky'); bpy.context.scene.world = w; w.use_nodes = True; nt = w.node_tree
    bg = nt.nodes['Background']; bg.inputs['Color'].default_value = hexc(col); bg.inputs['Strength'].default_value = k

def card(mb, m, x, y, h=1.62, w=0.7, z0=0.0):
    """flat grey 2D-puppet placeholder card (3 D tall = 1.62 m)"""
    mb.box(m, (x, y, z0 + h / 2), (w, 0.02, h))
    mb.ell(m, (x, y, z0 + h * 0.9), (0.2, 0.012, 0.2), (14, 10))

def curl(mb, m, p, rr, s=1.0):
    """wood shaving: a curled flat ribbon (chain of thin flat boxes along a loose spiral)"""
    a0 = rr.uniform(0, 6.28); r0 = rr.uniform(0.05, 0.08) * s; n = 10; turn = rr.uniform(0.7, 1.3); yaw = rr.uniform(0, 6.28)
    pts = [Vector((r0 * (1 - 0.35 * i / n) * math.cos(a0 + i / n * turn * 2 * math.pi), 0.012 * i * s, r0 * (1 - 0.35 * i / n) * math.sin(a0 + i / n * turn * 2 * math.pi) + r0 * 1.15)) for i in range(n + 1)]
    mb.push(Matrix.Translation(p) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    for i in range(n):
        a = pts[i]; b = pts[i + 1]; d = b - a
        mb.push(Matrix.Translation((a + b) / 2) @ d.to_track_quat('Z', 'Y').to_matrix().to_4x4()); mb.box(m, (0, 0, 0), (0.034 * s, 0.006, d.length * 1.15)); mb.pop()
    mb.pop()

def shafts(P, rect, zfloor=0.0, n=1):
    """faint light-shaft volume: the window rectangle projected along the sun direction to the floor (emission/transparent mix, no shadows)"""
    kd = Vector(P['key_dir']).normalized(); (x0, x1, z0, z1, y) = rect
    corners = [Vector((x0, y, z0)), Vector((x1, y, z0)), Vector((x1, y, z1)), Vector((x0, y, z1))]
    proj = [c + kd * ((zfloor - c.z) / kd.z) for c in corners]
    m = bpy.data.materials.new('shaft'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    em.inputs['Color'].default_value = hexc('#ffd890'); em.inputs['Strength'].default_value = P.get('shaft_k', 4.0); mx.inputs[0].default_value = P.get('shaft_a', 0.004)
    L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    mb = MB('shafts')
    for i in range(4):
        j = (i + 1) % 4; mb.quad(m, [corners[i], corners[j], proj[j], proj[i]]); mb.quad(m, [proj[i], proj[j], corners[j], corners[i]])
    mb.finish(shadow=False)

# ---- clouds (copied from film 16)
def cloud_mat(P):
    """emission-only painted cloud: normal facing the sun -> cream/peach, facing away / down -> blue-violet (gradient across every puff)"""
    m = bpy.data.materials.new('cloudG'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); gm = N('ShaderNodeNewGeometry'); vm = N('ShaderNodeVectorMath'); vm.operation = 'DOT_PRODUCT'
    kd = Vector(P['key_dir']).normalized(); vm.inputs[1].default_value = (-kd.x, -kd.y, -kd.z); L(gm.outputs['Normal'], vm.inputs[0])
    mr = N('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = -0.35; mr.inputs['From Max'].default_value = 0.45; L(vm.outputs['Value'], mr.inputs['Value'])
    mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.inputs[6].default_value = hexc(P['cloud'][1]); mx.inputs[7].default_value = hexc(P['cloud'][0]); L(mr.outputs['Result'], mx.inputs[0])
    em.inputs['Strength'].default_value = P.get('cloud_k', 1.0); L(mx.outputs[2], em.inputs['Color']); L(em.outputs[0], out.inputs['Surface']); MATS['cloudG'] = m; return m

def clouds(P):
    mb = MB('clouds'); rr = rnd(P.get('cloud_seed', 9)); a = mat_emit('cloudA', P['cloud'][0], P.get('cloud_k', 1.0)); b = mat_emit('cloudB', P['cloud'][1], P.get('cloud_k', 1.0))
    if P.get('cloud_diffuse'):      # sun-lit clouds: warm cream tops, blue-violet undersides from the sky ambient + a faint violet self term
        a = cloud_mat(P); b = a
    for i in range(P.get('ncloud', 10)):
        cx = rr.uniform(-260, 260); cy = rr.uniform(300, 420); cz = rr.uniform(P.get('cloud_z', (60, 140))[0], P.get('cloud_z', (60, 140))[1]); sz = rr.uniform(25, 55) * (1.0 + cz / 160.0) * P.get('cloud_scale', 1.0)
        for j in range(rr.randint(4, 7)):
            ox = rr.uniform(-1.4, 1.4) * sz; oz = rr.uniform(0, 0.35) * sz
            mb.ell(b, (cx + ox, cy, cz + oz - 0.25 * sz), (sz * rr.uniform(0.6, 1.0), sz * 0.5, sz * 0.32), (18, 10))
            mb.ell(a, (cx + ox, cy - 6, cz + oz), (sz * rr.uniform(0.5, 0.9), sz * 0.45, sz * 0.27), (14, 8))
    mb.finish()


# ================================================================== STILL 1: Harrison's workshop, Lincolnshire
def shop_mats():
    M = {}
    M['plaster'] = mat('plaster', '#b4663a', '#c87a44', scale=1.6, contrast=1.2, zgrad=(0.0, 0.5, '#7c3f30'))
    M['floor'] = mat('floor', '#725030', '#8a6234', scale=2.2, aniso=(0.5, 0.12, 1))
    M['floor2'] = mat('floor2', '#5e4026', '#764c2c', scale=2.2, aniso=(0.5, 0.12, 1))
    M['gap'] = mat('gap', '#2a1a22')
    M['beam'] = mat('beam', '#4e3420', '#684224', scale=2.0, aniso=(0.1, 1, 1))
    M['honey'] = mat('honey', '#c28b3e', '#aa7430', scale=5, aniso=(0.15, 1, 1), contrast=1.3)
    M['oak'] = mat('oak', '#8a5a2c', '#9e6a34', scale=5, aniso=(0.15, 1, 1))
    M['oakd'] = mat('oakd', '#5d3a20', '#72482a', scale=5, aniso=(0.2, 1, 1))
    M['lign'] = mat('lign', '#4a3a24', '#5e4a2c', scale=6)
    M['gearw'] = mat('gearw', '#c9924a', '#b07a38', scale=8, contrast=1.3)
    M['iron'] = metal_mat('iron', '#34323e', '#4a4858', rough=0.6, spec=0.15)
    M['steel'] = metal_mat('steel', '#6a6e86', '#82869e', rough=0.45, spec=0.5)
    M['brass'] = metal_mat('brass', '#a8741c', '#cc9230', rough=0.4, spec=0.4)
    M['brassd'] = metal_mat('brassd', '#7e5520', '#a0722e', rough=0.45, spec=0.3)
    M['terra'] = mat('terra', '#b5532c', '#c9683a', scale=4)
    M['cloth'] = mat('cloth', '#a98354', '#bd9560', scale=7)
    M['cream'] = mat('cream', '#e8d6aa', '#f0e0b8', scale=5)
    M['red'] = mat('red', '#8a2630', '#a23238', scale=6)
    M['green'] = mat('green', '#5e7a3a', '#748c44', scale=6)
    M['dark'] = mat('dark', '#1c1424', '#2a1c30', scale=4)
    M['shav'] = mat('shav', '#e8c88a', '#d4aa66', scale=8)
    M['grey'] = mat('grey', '#9aa0b0')
    M['flame'] = mat_emit('flame', '#ffc860', 28.0)
    M['lampg'] = mat_emit('lampg', '#ffd890', 8.0)
    return M

def box_wall(mb, m, x0, x1, y0, y1, z0, z1): mb.box(m, ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), (x1 - x0, y1 - y0, z1 - z0))

def build_shop(P):
    M = shop_mats(); mb = MB('shop'); rr = rnd(19)
    X0, X1, Y0, Y1, ZH = -2.3, 2.3, -2.9, 3.4, 2.9
    # ---- shell
    for i in range(23):                                   # floor planks along y
        x = X0 + 0.21 * i + 0.105
        mb.box(M['floor'] if i % 2 else M['floor2'], (x, (Y0 + Y1) / 2, -0.03), (0.2, Y1 - Y0, 0.06))
    mb.box(M['gap'], ((X0 + X1) / 2, (Y0 + Y1) / 2, -0.07), (X1 - X0 + .3, Y1 - Y0 + .3, 0.05))
    wx0, wx1, wz0, wz1 = -1.55, -0.3, 0.9, 2.3            # window opening in the back wall
    box_wall(mb, M['plaster'], X0 - .2, wx0, Y1, Y1 + .32, 0, ZH); box_wall(mb, M['plaster'], wx1, X1 + .2, Y1, Y1 + .32, 0, ZH)
    box_wall(mb, M['plaster'], wx0, wx1, Y1, Y1 + .32, 0, wz0); box_wall(mb, M['plaster'], wx0, wx1, Y1, Y1 + .32, wz1, ZH)
    box_wall(mb, M['plaster'], X0 - .3, X0, Y0, Y1 + .3, 0, ZH); box_wall(mb, M['plaster'], X1, X1 + .3, Y0, Y1 + .3, 0, ZH)
    box_wall(mb, M['plaster'], X0, X1, Y0 - .3, Y0, 0, ZH); box_wall(mb, M['plaster'], X0 - .3, X1 + .3, Y0, Y1 + .3, ZH, ZH + .3)
    # timber frame on the plaster: posts, sill rail, ceiling beams
    for x in (-2.2, 2.2): mb.box(M['beam'], (x, Y1 - 0.06, ZH / 2), (0.2, 0.14, ZH))
    mb.box(M['beam'], (0, Y1 - 0.06, 0.12), (4.6, 0.14, 0.24)); mb.box(M['beam'], (0, Y1 - 0.06, ZH - 0.12), (4.6, 0.14, 0.24))
    mb.box(M['beam'], (0.85, Y1 - 0.06, 1.62), (2.8, 0.1, 0.13))
    for y in (-1.8, -0.3, 1.2, 2.7): mb.box(M['beam'], (0, y, ZH - 0.14), (4.6, 0.24, 0.28))
    for x in (-1.2, 1.2): mb.box(M['beam'], (x, 0.5, ZH - 0.05), (0.14, 6.2, 0.14))
    for x in (X0 + 0.06, X1 - 0.06): mb.box(M['beam'], (x, 1.0, ZH - 0.2), (0.14, 6.0, 0.3)); mb.box(M['beam'], (x, 1.0, 0.1), (0.14, 6.0, 0.2))
    # ---- window: reveal, mullions (small panes), sill, shutter
    gl = MB('glass'); sky_m = mat_emit('sky_pane', '#a8c8f4', 1.5); hedge_m = mat_emit('hedge_pane', '#4e7a58', 0.55); roof_m = mat_emit('roof_pane', '#b86a4a', 0.7)
    gl.quad(sky_m, [(wx0, Y1 + 0.5, wz0 + 0.5), (wx1, Y1 + 0.5, wz0 + 0.5), (wx1, Y1 + 0.5, wz1), (wx0, Y1 + 0.5, wz1)][::-1])
    gl.quad(hedge_m, [(wx0, Y1 + 0.49, wz0), (wx1, Y1 + 0.49, wz0), (wx1, Y1 + 0.49, wz0 + 0.5), (wx0, Y1 + 0.49, wz0 + 0.5)][::-1])
    gl.quad(roof_m, [(wx0 + .55, Y1 + 0.48, wz0 + 0.46), (wx1 - .05, Y1 + 0.48, wz0 + 0.46), (wx1 - .05, Y1 + 0.48, wz0 + 0.7), (wx0 + .55, Y1 + 0.48, wz0 + 0.7)][::-1])
    gl.finish(shadow=False)
    ym = Y1 + 0.12
    for k in range(5): mb.box(M['oakd'], (wx0 + k * (wx1 - wx0) / 4, ym, (wz0 + wz1) / 2), (0.03, 0.05, wz1 - wz0))
    for k in range(6): mb.box(M['oakd'], ((wx0 + wx1) / 2, ym, wz0 + k * (wz1 - wz0) / 5), (wx1 - wx0, 0.05, 0.03))
    for x in (wx0 - 0.04, wx1 + 0.04): mb.box(M['oakd'], (x, ym, (wz0 + wz1) / 2), (0.08, 0.14, wz1 - wz0 + .1))
    mb.box(M['oak'], ((wx0 + wx1) / 2, Y1 - 0.12, wz0 - 0.03), (wx1 - wx0 + .3, 0.34, 0.07))
    mb.box(M['oakd'], (wx0 - 0.28, Y1 - 0.14, (wz0 + wz1) / 2), (0.34, 0.04, wz1 - wz0 - .02), rz=0.5)   # open shutter
    # ---- longcase clock with a visible wooden movement (back-left corner)
    cx, cy = -1.95, 3.0
    mb.box(M['oakd'], (cx, cy, 0.07), (0.56, 0.34, 0.14))                      # plinth
    mb.box(M['oak'], (cx - 0.24, cy, 0.8), (0.07, 0.26, 1.5)); mb.box(M['oak'], (cx + 0.24, cy, 0.8), (0.07, 0.26, 1.5)); mb.box(M['dark'], (cx, cy + 0.1, 0.8), (0.4, 0.06, 1.5))
    mb.box(M['oakd'], (cx, cy - 0.12, 1.55), (0.5, 0.05, 0.1))
    mb.box(M['oak'], (cx - 0.28, cy, 2.05), (0.08, 0.3, 0.9)); mb.box(M['oak'], (cx + 0.28, cy, 2.05), (0.08, 0.3, 0.9)); mb.box(M['dark'], (cx, cy + 0.12, 2.05), (0.5, 0.06, 0.9))
    mb.box(M['oak'], (cx, cy, 2.55), (0.74, 0.38, 0.1)); mb.box(M['oakd'], (cx, cy, 2.66), (0.62, 0.32, 0.12)); mb.box(M['oak'], (cx, cy - 0.02, 1.58), (0.62, 0.34, 0.05))
    # open wooden movement: two plates + wheels facing the room
    mb.box(M['oak'], (cx, cy + 0.04, 2.05), (0.44, 0.03, 0.82), )
    for (dx, dz, r, nt) in [(-0.08, 2.3, 0.11, 14), (0.07, 2.12, 0.085, 12), (-0.07, 1.95, 0.065, 10), (0.08, 1.84, 0.045, 8)]:
        gear(mb, M['gearw'], (cx + dx, cy - 0.04, dz), r, nt=nt, th=0.035, rim=0.02, tooth=0.02, hub=0.02, n=12)
    mb.box(M['brassd'], (cx, cy - 0.04, 2.48), (0.2, 0.03, 0.04)); mb.box(M['brassd'], (cx + 0.12, cy - 0.04, 2.38), (0.03, 0.03, 0.2))
    mb.rod(M['iron'], (cx, cy - 0.02, 2.4), (cx, cy - 0.02, 1.1), 0.007, 0.007, 6)                  # pendulum rod
    mb.cyl(M['brass'], (cx, cy - 0.02, 1.0), 0.1, 0.03, axis='y', seg=16)                         # bob
    for dx in (-0.1, 0.1):
        mb.rod(M['iron'], (cx + dx, cy - 0.04, 1.8), (cx + dx, cy - 0.04, 0.45 if dx < 0 else 0.7), 0.004, 0.004, 4)
        mb.cyl(M['brass'], (cx + dx, cy - 0.04, 0.38 if dx < 0 else 0.62), 0.045, 0.2, seg=10)
    for dx in (-0.3, 0, 0.3): mb.ell(M['brass'], (cx + dx, cy, 2.78), (0.03, 0.03, 0.05), (8, 6))
    # ---- wall: wooden gear wheels hanging on pegs, saws, chisel rack
    for (x, z, r, nt, col) in [(0.55, 2.0, 0.31, 18, 'gearw'), (1.0, 2.3, 0.2, 14, 'honey'), (0.87, 1.74, 0.14, 10, 'gearw'), (0.3, 1.7, 0.1, 8, 'oak')]:
        gear(mb, M[col], (x, Y1 - 0.08, z), r, nt=nt, th=0.045, rim=0.045 * (r / 0.3 + 0.5), tooth=0.05 * (r / 0.3 + 0.4), hub=0.04)
        mb.rod(M['iron'], (x, Y1 - 0.08, z + r + 0.04), (x, Y1, z + r + 0.04), 0.012, 0.012, 6)
    hang_saw(mb, M, (1.6, Y1 - 0.12, 2.45), 0.7, 0.0); hang_saw(mb, M, (2.05, Y1 - 0.12, 2.0), 0.55, 1.2); hang_saw(mb, M, (1.75, Y1 - 0.12, 1.85), 0.5, -0.06)
    mb.box(M['oakd'], (1.2, Y1 - 0.1, 1.5), (1.4, 0.06, 0.06))
    for k in range(7):
        x = 0.6 + k * 0.2
        mb.box(M['steel'], (x, Y1 - 0.13, 1.58), (0.018, 0.012, 0.16)); mb.box(M['honey'], (x, Y1 - 0.14, 1.42), (0.04, 0.045, 0.1))
    # ---- workbench (against the back wall, right) -- pulled 0.55 m toward the camera
    mb.push(Matrix.Translation((0.05, -1.0, 0)))
    bx0, bx1, by0, by1, bz = 0.25, 2.15, 2.5, 3.3, 0.9
    mb.box(M['honey'], ((bx0 + bx1) / 2, (by0 + by1) / 2, bz - 0.05), (bx1 - bx0, by1 - by0, 0.1))
    mb.box(M['oak'], ((bx0 + bx1) / 2, by0 + 0.02, bz - 0.17), (bx1 - bx0, 0.05, 0.14))
    for x in (bx0 + 0.1, bx1 - 0.1):
        for y in (by0 + 0.08, by1 - 0.1): mb.box(M['oak'], (x, y, bz / 2 - 0.05), (0.12, 0.12, bz - 0.1))
    mb.box(M['oakd'], ((bx0 + bx1) / 2, (by0 + by1) / 2, 0.3), (bx1 - bx0 - .1, by1 - by0 - .1, 0.05))
    mb.box(M['oak'], (bx0 + 0.15, by0 - 0.06, bz + 0.0), (0.14, 0.1, 0.1)); mb.cyl(M['iron'], (bx0 + 0.15, by0 - 0.16, bz - 0.02), 0.025, 0.18, axis='y', seg=8)   # vise
    mb.rod(M['oakd'], (bx0 + 0.04, by0 - 0.22, bz - 0.02), (bx0 + 0.26, by0 - 0.22, bz - 0.02), 0.015, 0.015, 6)
    # lower shelf clutter: gear blanks, planks
    for k in range(4): mb.cyl(M['honey'], (bx0 + 0.35 + 0.12 * k, 2.9, 0.37 + 0.035 * k), 0.16, 0.04, seg=14)
    mb.box(M['oak'], (1.5, 2.9, 0.36), (0.5, 0.3, 0.05)); mb.box(M['oakd'], (1.7, 2.95, 0.42), (0.6, 0.12, 0.05))
    # ---- hero: H1-style brass sea clock on the bench (x centre 1.2)
    hx, hy, hz = 0.95, 2.88, bz
    mb.push(Matrix.Translation((hx, hy, hz)) @ Matrix.Diagonal((1.22, 1.22, 1.22, 1.0)) @ Matrix.Translation((-hx, -hy, -hz)))
    hw, hd, hh = 0.86, 0.5, 0.42
    for dx in (-hw / 2, hw / 2):
        for dy in (-hd / 2, hd / 2): mb.box(M['brass'], (hx + dx, hy + dy, hz + hh / 2 + 0.05), (0.04, 0.04, hh))       # four corner posts
    for z in (hz + 0.05, hz + hh + .05):
        for dy in (-hd / 2, hd / 2): mb.box(M['brass'], (hx, hy + dy, z), (hw + 0.04, 0.04, 0.04))
        for dx in (-hw / 2, hw / 2): mb.box(M['brass'], (hx + dx, hy, z), (0.04, hd, 0.04))
    mb.box(M['honey'], (hx, hy, hz + 0.02), (hw + 0.1, hd + 0.1, 0.04))                                                  # oak base
    mb.box(M['brassd'], (hx, hy, hz + hh + .08), (hw, hd, 0.02))                                                       # top plate
    # inner plates + exposed gear wheels (brass + oak)
    mb.box(M['brassd'], (hx, hy - 0.12, hz + 0.28), (hw - .08, 0.02, hh - .1)); mb.box(M['brassd'], (hx, hy + 0.12, hz + 0.28), (hw - .08, 0.02, hh - .1))
    for (dx, dz, r, nt) in [(-0.22, 0.30, 0.15, 20), (0.05, 0.25, 0.11, 16), (0.26, 0.31, 0.12, 16), (-0.02, 0.38, 0.065, 10), (0.33, 0.18, 0.06, 10), (-0.33, 0.15, 0.07, 10)]:
        gear(mb, M['brass'] if nt != 16 else M['gearw'], (hx + dx, hy - 0.19, hz + dz), r, nt=nt, th=0.035, rim=0.022, tooth=0.026, hub=0.025, n=14)
    mb.rod(M['brassd'], (hx - 0.3, hy - 0.22, hz + 0.3), (hx + 0.3, hy - 0.22, hz + 0.3), 0.007, 0.007, 6)
    # two dumbbell balance bars crossing in an X on top, four brass balls
    zt = hz + hh + 0.22
    for sgn, zz in ((1, zt), (-1, zt + 0.07)):
        a = sgn * math.radians(33); L = 0.42; tipx = L * math.cos(a); tipy = L * math.sin(a)
        mb.rod(M['brass'], (hx - tipx, hy - tipy, zz), (hx + tipx, hy + tipy, zz), 0.014, 0.014, 8)
        for e in (-1, 1): sphere_brass(mb, M['brass'], (hx + e * (tipx + 0.0), hy + e * tipy, zz), 0.095)
    mb.rod(M['brass'], (hx, hy, hz + hh + .09), (hx, hy, zt + 0.1), 0.02, 0.02, 8); mb.ell(M['brass'], (hx, hy, zt + 0.1), (0.04, 0.04, 0.04), (10, 8))
    for dx in (-0.3, 0.3): mb.rod(M['brass'], (hx + dx, hy - 0.1, hz + hh + .09), (hx + dx * .3, hy, zt - 0.02), 0.008, 0.008, 6)      # springs/stays
    mb.pop()
    # ---- bench tools
    mb.box(M['honey'], (0.55, 2.9, bz + 0.035), (0.34, 0.1, 0.07)); mb.box(M['steel'], (0.55, 2.9, bz + 0.075), (0.18, 0.05, 0.012)); mb.box(M['oakd'], (0.62, 2.9, bz + 0.1), (0.05, 0.05, 0.07))   # plane
    mb.cyl(M['oakd'], (0.72, 3.15, bz + 0.07), 0.04, 0.16, axis='x', seg=8); mb.rod(M['oak'], (0.72, 3.15, bz + 0.07), (0.72, 2.8, bz + 0.07), 0.014, 0.014, 6)   # mallet
    mb.cyl(M['oak'], (0.3, 3.05, bz + 0.05), 0.045, 0.14, axis='x', seg=8); mb.rod(M['oak'], (0.3, 3.05, bz + 0.05), (0.3, 2.78, bz + 0.05), 0.012, 0.012, 6)
    mb.box(M['steel'], (1.88, 2.7, bz + 0.012), (0.5, 0.075, 0.008)); mb.box(M['oakd'], (2.15, 2.7, bz + 0.04), (0.1, 0.04, 0.08))                               # saw on bench
    for k in range(4): mb.box(M['steel'], (1.75 + 0.05 * k, 2.58, bz + 0.012), (0.015, 0.2, 0.01)); mb.box(M['honey'], (1.75 + 0.05 * k, 2.44, bz + 0.02), (0.03, 0.08, 0.03))   # chisels
    mb.rod(M['iron'], (0.8, 2.62, bz + 0.2), (0.8, 2.62, bz + 0.02), 0.012, 0.012, 6); mb.rod(M['iron'], (0.8, 2.62, bz + 0.2), (0.95, 2.62, bz + 0.2), 0.012, 0.012, 6)
    mb.ell(M['oakd'], (0.95, 2.62, bz + 0.2), (0.04, 0.04, 0.04), (8, 6))                                                                              # brace drill
    mb.box(M['steel'], (0.45, 2.6, bz + 0.01), (0.3, 0.012, 0.01)); mb.box(M['steel'], (0.31, 2.7, bz + 0.01), (0.012, 0.2, 0.01))                        # square
    mb.cyl(M['terra'], (2.05, 3.05, bz + 0.07), 0.06, 0.14, seg=10)                                                                                   # glue pot
    for k in range(5): curl(mb, M['shav'], (0.35 + 0.28 * k, 2.6 + 0.1 * (k % 2), bz), rr, 0.9)
    # candle (brass stick + wax + flame), oil lamp
    mb.cyl(M['brass'], (0.46, 3.18, bz + 0.015), 0.05, 0.03, seg=10); mb.cyl(M['brass'], (0.46, 3.18, bz + 0.07), 0.015, 0.1, seg=8)
    mb.cyl(M['cream'], (0.46, 3.18, bz + 0.2), 0.02, 0.16, seg=8)
    gl2 = MB('flame'); gl2.ell(M['flame'], (0.46, 3.18, bz + 0.31), (0.02, 0.02, 0.05), (8, 6)); gl2.finish(shadow=False)
    mb.ell(M['terra'], (2.0, 3.2, bz + 0.07), (0.085, 0.06, 0.07), (10, 8)); mb.box(M['terra'], (2.0, 3.2, bz + 0.15), (0.03, 0.03, 0.05))
    gl3 = MB('flame'); gl3.ell(M['flame'], (2.0, 3.2, bz + 0.2), (0.02, 0.02, 0.045), (8, 6)); gl3.finish(shadow=False)
    mb.pop()
    # ---- treadle lathe (left-centre, in front of the window)
    lx, ly = -1.1, 2.15
    for x in (lx - 0.55, lx + 0.55):
        for y in (ly - 0.15, ly + 0.15): mb.box(M['oak'], (x, y, 0.45), (0.09, 0.09, 0.9))
    for y in (ly - 0.07, ly + 0.07): mb.box(M['honey'], (lx, y, 0.92), (1.3, 0.07, 0.07))
    mb.box(M['oakd'], (lx - 0.45, ly, 1.07), (0.16, 0.26, 0.24)); mb.box(M['oakd'], (lx + 0.42, ly, 1.04), (0.12, 0.22, 0.18)); mb.box(M['iron'], (lx + 0.3, ly, 1.0), (0.06, 0.03, 0.03))
    mb.cyl(M['honey'], (lx - 0.02, ly, 1.04), 0.05, 0.6, axis='x', seg=12, r2=0.035)                       # the turned workpiece
    mb.box(M['oakd'], (lx + 0.05, ly - 0.14, 0.99), (0.2, 0.04, 0.025))                                    # tool rest
    gear(mb, M['oak'], (lx - 0.78, ly - 0.35, 0.62), 0.3, nt=0, th=0.06, rim=0.05, spokes=3, tooth=0.0, rot=(0, 0, math.pi / 2), hub=0.06, n=18)  # flywheel (yz plane)
    mb.box(M['oakd'], (lx + 0.1, ly - 0.55, 0.12), (0.7, 0.16, 0.04), ry=0.12)                              # treadle board
    mb.rod(M['iron'], (lx - 0.78, ly - 0.35, 0.62), (lx - 0.35, ly - 0.52, 0.16), 0.01, 0.01, 6)
    curl(mb, M['shav'], (lx - 0.0, ly - 0.2, 0.92), rr, 0.9)
    # ---- right wall: leaning boards, chest, barrel
    for k in range(5): mb.box(M['honey'] if k % 2 else M['oak'], (2.12 - 0.01 * k, 3.15 - 0.2 * k, 1.1), (0.05, 0.2, 2.1), ry=0.09)
    mb.box(M['oakd'], (1.75, 1.4, 0.26), (0.7, 0.5, 0.52)); mb.box(M['oak'], (1.75, 1.4, 0.55), (0.74, 0.54, 0.08)); 
    for dx in (-0.25, 0.25): mb.box(M['brassd'], (1.75 + dx, 1.4, 0.3), (0.05, 0.56, 0.54))
    mb.cyl(M['oak'], (-1.85, 1.2, 0.3), 0.26, 0.6, seg=14); 
    for z in (0.12, 0.3, 0.48): mb.cyl(M['iron'], (-1.85, 1.2, z), 0.275, 0.03, seg=14)
    # ---- ceiling: hanging oil lamp + herbs + long saw
    mb.rod(M['iron'], (-0.1, 1.6, ZH - 0.28), (-0.1, 1.6, 2.35), 0.008, 0.008, 4); mb.ell(M['brassd'], (-0.1, 1.6, 2.25), (0.09, 0.09, 0.07), (10, 8))
    gl4 = MB('flame'); gl4.ell(M['flame'], (-0.1, 1.6, 2.3), (0.025, 0.025, 0.05), (8, 6)); gl4.finish(shadow=False)
    for k in range(5): mb.rod(M['green'] if k % 2 else M['cloth'], (1.0 + 0.1 * k, -0.3, ZH - 0.28), (1.0 + 0.1 * k + 0.02 * (k - 2), -0.3, 2.25), 0.02, 0.05, 5)
    pass
    # ---- foreground (dark, nearest 15 % of frame): sawhorse + plank corner left, stool right, shavings
    mb.box(M['oakd'], (-1.65, -0.55, 0.4), (1.1, 0.42, 0.07)); 
    for x in (-2.1, -1.2):
        mb.box(M['oak'], (x, -0.55, 0.2), (0.08, 0.36, 0.4)); mb.box(M['oak'], (x, -0.55, 0.2), (0.08, 0.5, 0.06), ry=0.0)
    mb.box(M['honey'], (-1.6, -0.5, 0.46), (0.5, 0.2, 0.05), rz=0.35); mb.box(M['steel'], (-1.9, -0.6, 0.45), (0.3, 0.07, 0.008), rz=-0.3)
    mb.cyl(M['oakd'], (1.5, -0.7, 0.4), 0.2, 0.06, seg=14)
    for a in (0.3, 2.4, 4.5): mb.rod(M['oak'], (1.5 + 0.16 * math.cos(a), -0.7 + 0.16 * math.sin(a), 0.38), (1.5 + 0.24 * math.cos(a), -0.7 + 0.24 * math.sin(a), 0.0), 0.025, 0.02, 6)
    for (x, y, s) in [(-1.4, 0.2, 1.4), (-0.95, 1.0, 1.0), (1.2, 0.4, 1.3), (1.9, 2.1, 1.0), (-1.9, 1.9, 1.0), (0.1, 2.3, 1.0), (-0.4, -0.1, 0.8)]:
        pile(mb, M['shav'], (x, y, 0), s, rr)
    for k in range(45):
        x = rr.uniform(-2.0, 2.0); y = rr.uniform(-1.0, 3.0)
        if abs(x) < 0.55 and 0.0 < y < 2.2 and rr.random() < 0.8: continue
        curl(mb, M['shav'], (x, y, 0.0), rr, rr.uniform(0.8, 1.2))
    mb.rod(M['oak'], (-0.9, -0.3, 0.03), (-0.5, -0.6, 0.03), 0.03, 0.03, 6)
    mb.cyl(M['oakd'], (0.45, -1.05, 0.17), 0.19, 0.34, seg=14, r2=0.23)
    for z in (0.06, 0.28): mb.cyl(M['iron'], (0.45, -1.05, z), 0.2 + 0.02 * (z > 0.2), 0.025, seg=14)
    mb.box(M['honey'], (-0.45, -0.95, 0.03), (0.9, 0.12, 0.05), rz=0.5); mb.box(M['oak'], (-0.75, -0.85, 0.08), (0.7, 0.1, 0.05), rz=-0.35)
    mb.cyl(M['oak'], (-0.1, -0.55, 0.06), 0.045, 0.35, axis='x', seg=8); mb.cyl(M['oakd'], (0.12, -0.55, 0.07), 0.07, 0.14, axis='x', seg=8)
    for k in range(4): mb.cyl(M['oakd'] if k % 2 else M['oak'], (1.45 + 0.0, 0.35 + 0.0, 0.1 + 0.2 * 0), 0.1, 0.9, axis='x', seg=10) if False else None
    for (yy, zz, k) in [(0.1, 0.1, 0), (0.32, 0.1, 1), (0.21, 0.29, 0)]: mb.cyl(M['oakd'] if k else M['oak'], (1.55, yy, zz), 0.1, 1.0, axis='x', seg=10)
    mb.box(M['oakd'], (-1.7, 0.5, 0.12), (0.7, 0.4, 0.24)); mb.box(M['iron'], (-1.7, 0.29, 0.2), (0.7, 0.02, 0.04)); mb.box(M['steel'], (-1.85, 0.5, 0.26), (0.3, 0.05, 0.01))
    mb.finish()
    if os.environ.get('NOCARDS'): return
    cm = MB('cards'); card(cm, M['grey'], -1.0, 1.0, w=0.55); card(cm, M['grey'], -0.4, 1.3, w=0.55); cm.finish()

PRESETS = {}
PRESETS['shop'] = dict(
    key=(1.0, 0.8, 0.52, 15.0), key_dir=kdir(-30, 31), sun_angle=1.0, exposure=0.4, sat=1.1, samples=96, dbounce=3,
    cam=dict(loc=(0.05, -2.3, 1.32), look=(0.0, 3.4, 0.95), lens=22), flat_amb=('#3a3cff', 0.0))

def lights_shop(P):
    sun_light(P); shafts(P, (-1.55, -0.3, 0.9, 2.3, 3.38))
    area_light('fill', (0, 0.3, 2.85), (0, 0, 0), (4.4, 5.5), (0.015, 0.07, 1.0), 700)               # blue-violet ambient from above (rotation 0 -> shines down)
    area_light('fillc', (0.0, -2.8, 1.5), (math.pi / 2, 0, 0), (4.4, 2.8), (0.08, 0.18, 1.0), 170)    # from behind the camera
    area_light('winfill', (-0.85, 3.5, 1.6), (-math.pi / 2, 0, 0), (1.1, 1.3), (0.3, 0.42, 1.0), 140)
    for (loc, en) in [((0.51, 2.2, 1.3), 20), ((2.05, 2.2, 1.2), 11), ((-0.1, 1.5, 2.3), 13)]: point_light('flamep', loc, (1.0, 0.66, 0.3), en, 0.04)
    point_light('flamep', (0.3, 1.3, 1.75), (1.0, 0.7, 0.36), 22, 0.2)        # warm lamp-light on the sea clock

# ================================================================== STILL 2 (v2): Royal Navy 50-gun ship, forecastle view forward-down over the bow
DECK = 6.0; ZF = 8.0; STEM = 46.0; YF = 27.0          # waist deck z, forecastle deck z, stem y, forecastle starts at YF
def hw(y):
    """deck half-beam at y (m): full beam to y=20, narrowing to the stem at y=46 (floats and arrays)"""
    t = np.clip((np.asarray(y, dtype=np.float64) - 20.0) / (STEM - 20.0), 0.0, 1.0)
    r = 3.7 * np.maximum(0.0, 1 - t ** 2.0) ** 0.85
    return float(r) if np.ndim(r) == 0 else r

def ship_mats():
    M = {}
    M['deck1'] = mat('deck1', '#9a7440', '#85632f', scale=3, aniso=(0.12, 1, 1), contrast=1.4)
    M['deck2'] = mat('deck2', '#876530', '#a07a40', scale=3, aniso=(0.12, 1, 1), contrast=1.4)
    M['seam'] = mat('seam', '#2c1c20')
    M['hullb'] = mat('hullb', '#262034', '#332c44', scale=2, aniso=(0.3, 0.3, 1))
    M['ochre'] = mat('ochre', '#cf9230', '#bd7f26', scale=3)
    M['bulw'] = mat('bulw', '#a24c2c', '#8f3f28', scale=3, aniso=(0.2, 1, 1))
    M['cap'] = mat('cap', '#2a2230', '#3a2e3c', scale=3)
    M['iron'] = metal_mat('iron', '#2c2a3a', '#3e3c50', rough=0.5, spec=0.35)
    M['carr'] = mat('carr', '#8c4a2a', '#a05a32', scale=4, aniso=(0.2, 1, 1))
    M['oak'] = mat('oak', '#8a5a2c', '#9e6a34', scale=5, aniso=(0.15, 1, 1))
    M['mast'] = mat('mast', '#8a5c34', '#a2703c', scale=3, aniso=(0.2, 0.2, 0.05))
    M['rope'] = mat('rope', '#b8924c', '#9a7638', scale=6)
    M['rig'] = mat('rig', '#2a2030', '#3a2e3a', scale=3)
    M['brass'] = metal_mat('brass', '#cb9f48', '#e6bb5c', rough=0.28, spec=0.8, metallic=0.9)
    M['sail'] = mat('sail', '#e8dcc0', '#dccfae', scale=2.2, contrast=1.1, emit='#ffe2a0', emit_k=0.3)
    M['sail2'] = mat('sail2', '#d8c9a6', '#cdbd98', scale=2.2, contrast=1.1, emit='#ffe2a0', emit_k=0.25)
    M['red'] = mat('red', '#b83a32', '#9c2e2c', scale=4)
    M['grey'] = mat('grey', '#a4a8b8')
    M['isle'] = mat_emit('isle', '#6f9a78', 0.9); M['isle2'] = mat_emit('isle2', '#4f7e68', 0.8); M['beach'] = mat_emit('beach', '#e8dcb8', 1.0)
    M['darksail'] = mat('darksail', '#2c2838')
    M['lamp'] = mat_emit('lamp', '#ffd890', 6.0)
    return M

def tube(mb, m, p0, p1, r0, r1=None, seg=8): mb.rod(m, p0, p1, r0, r1, seg=seg, caps=True, smooth=True)

def sail_tri(mb, M, T, C, Hd, bulge, n=8, m=8):
    """billowing triangular jib: luff T->Hd, leech C->Hd, belly sideways (+x) and forward; canvas strips alternate colour"""
    T = Vector(T); C = Vector(C); Hd = Vector(Hd)
    def P(i, j):
        v = j / n; L = T + (Hd - T) * v; Rr = C + (Hd - C) * v; u = i / m
        p = L + (Rr - L) * u
        b = bulge * math.sin(math.pi * u) * math.sin(math.pi * min(1, 0.12 + 0.88 * v)) * (1 - 0.5 * v)
        return (p.x + b, p.y + b * 0.4, p.z)
    for i in range(m):
        for j in range(n):
            q = [P(i, j), P(i + 1, j), P(i + 1, j + 1), P(i, j + 1)]
            mm = M['sail'] if i % 2 else M['sail2']
            mb.quad(mm, q); mb.quad(mm, q[::-1])

def sail_quad(mb, M, x0, x1, zb, zt, y, belly, ny=8, nx=10):
    def P(i, j):
        u = i / nx; v = j / ny
        xl = x0 + (x1 - x0) * u; zz = zb + (zt - zb) * v
        by = belly * math.sin(math.pi * u) * math.sin(math.pi * (0.15 + 0.85 * v)) ** 0.8 + 0.25 * math.sin(math.pi * u * 2.0) * 0.0
        return (xl * (1 + 0.05 * (1 - v)), y + by, zz)
    for i in range(nx):
        for j in range(ny):
            q = [P(i, j), P(i + 1, j), P(i + 1, j + 1), P(i, j + 1)]
            mm = M['sail'] if i % 2 else M['sail2']; mb.quad(mm, q); mb.quad(mm, q[::-1])

def build_ship(P):
    M = ship_mats(); mb = MB('ship'); rr = rnd(5)
    Y0 = -6.0
    # ---- waist deck planks (clipped to the outline) + hull body strips (black, ochre wale, tumblehome flare)
    def ylim_for(ax):
        if ax >= 3.699: return 20.0
        lo, hi = 20.0, STEM
        for _ in range(30):
            mid = (lo + hi) / 2
            if hw(mid) > ax: lo = mid
            else: hi = mid
        return lo
    k = 0; x = -3.7 + 0.13
    while x < 3.7:
        yl = ylim_for(abs(x)); mb.box(M['deck1'] if k % 2 else M['deck2'], (x, (Y0 + min(yl, YF + 0.2)) / 2, DECK - 0.08), (0.255, min(yl, YF + 0.2) - Y0, 0.16)); x += 0.26; k += 1
    y = Y0
    while y < STEM:
        yc = y + 0.5; b = hw(yc)
        if b > 0.05:
            for s in (-1, 1):
                for (z0, z1, mm) in ((0.0, 2.7, 'hullb'), (2.7, 3.15, 'ochre'), (3.15, 5.75, 'hullb')):
                    t = (0.55 + 0.45 * (1 - ((z0 + z1) / 2) / 5.8)) * 0.9
                    mb.box(M[mm], (s * (b + t / 2), yc, (z0 + z1) / 2), (t, 1.04, z1 - z0))
            mb.box(M['hullb'], (0, yc, 2.9), (2 * b, 1.04, 5.8))
        y += 1.0
    # ---- forecastle platform (z=ZF) with planks, black/ochre sides, stair gap at the back, low balustrade
    y = YF
    while y < STEM - 0.5:
        yc = y + 0.5; b = hw(yc)
        if b > 0.2:
            mb.box(M['hullb'], (0, yc, 7.0), (2 * b + 0.2, 1.04, 2.0)); mb.box(M['ochre'], (0, yc, 7.0), (2 * b + 0.24, 1.0, 0.3))
        y += 1.0
    k = 0; x = -3.7 + 0.13
    while x < 3.7:
        yl = ylim_for(abs(x)) if abs(x) < 3.699 else 20.0
        if yl > YF + 0.5: mb.box(M['deck1'] if k % 2 else M['deck2'], (x, (YF + yl) / 2, ZF - 0.02), (0.255, yl - YF, 0.06))
        x += 0.26; k += 1
    for xx in np.arange(-3.4, 3.5, 0.45):
        if abs(xx) < 0.75 or abs(xx) > hw(YF) - 0.2: continue
        mb.box(M['oak'], (xx, YF + 0.1, ZF + 0.45), (0.09, 0.09, 0.9))
    for (a, b_) in ((-3.7, -0.75), (0.75, 3.7)): mb.box(M['cap'], ((a + b_) / 2, YF + 0.1, ZF + 0.93), (b_ - a, 0.16, 0.1))
    for st in range(3): mb.box(M['deck1'], (0, YF - 0.3 - 0.3 * st, ZF - 0.6 - 0.6 * st), (1.3, 0.5, 0.1))
    gun_y = [40.4, 43.4]; gun_yp = [42.3]
    for s, gy in ((1, gun_y), (-1, gun_yp)):               # low bulwark with gun ports, black + ochre band
        y = YF
        while y < STEM - 0.3:
            yc = y + 0.3; b = hw(yc)
            if b > 0.15 and not any(abs(yc - g) < 0.42 for g in gy):
                dy = hw(yc + 0.3) - hw(yc - 0.3); ang = math.atan2(-dy * s, 0.6)
                mb.box(M['hullb'], (s * (b - 0.04), yc, ZF + 0.25), (0.16, 0.66, 0.5), rz=ang); mb.box(M['ochre'], (s * (b - 0.04), yc, ZF + 0.63), (0.17, 0.66, 0.3), rz=ang); mb.box(M['hullb'], (s * (b - 0.04), yc, ZF + 0.84), (0.16, 0.66, 0.1), rz=ang)
            y += 0.6
        y = YF
        while y < STEM - 0.3:
            yc = y + 0.35; b = hw(yc); dy = hw(yc + 0.35) - hw(yc - 0.35)
            if b > 0.15: mb.box(M['cap'], (s * (b - 0.02), yc, ZF + 0.92), (0.3, 0.74, 0.1), rz=math.atan2(-dy * s, 0.7))
            y += 0.7
    mb.box(M['cap'], (0, STEM - 1.3, ZF + 0.92), (1.0, 0.3, 0.1))
    # ---- cannons on carriages (forecastle)
    def cannon(side, y):
        b = hw(y); s = side; zc = ZF + 0.62
        xo = s * (b - 0.1); xi = s * (b - 1.6)
        tube(mb, M['iron'], (xi, y, zc), (xo + s * 0.3, y, zc), 0.23, 0.15, 12)
        mb.ell(M['iron'], (xi - s * 0.12, y, zc), (0.17, 0.17, 0.17), (10, 8)); mb.cyl(M['iron'], (xo + s * 0.22, y, zc), 0.19, 0.08, axis='x', seg=12)
        for yy in (-0.3, 0.3): mb.box(M['carr'], ((xi + xo) / 2 - s * 0.05, y + yy, ZF + 0.3), (1.6, 0.14, 0.5))
        mb.box(M['carr'], (xi + s * 0.45, y, ZF + 0.45), (0.14, 0.6, 0.3)); mb.box(M['oak'], (xi - s * 0.55, y, ZF + 0.46), (0.5, 0.5, 0.06))
        for dx in (-0.35, 0.5):
            for yy in (-0.36, 0.36): mb.cyl(M['oak'], (s * (b - 0.9) + s * dx * 0.8, y + yy, ZF + 0.17), 0.17, 0.1, axis='y', seg=12)
        for yy in (-0.7, 0.7): mb.rod(M['rope'], (xi - s * 0.1, y, zc - 0.1), (s * (b - 0.2), y + yy, ZF + 0.8), 0.03, 0.03, 5)
        mb.rod(M['rope'], (xo, y, zc + 0.2), (s * b, y + 0.5, ZF + 0.8), 0.03, 0.03, 5)
    for g in gun_y: cannon(1, g)
    for g in gun_yp: cannon(-1, g)
    # ---- foreground deck furniture (forecastle): binnacle (wooden pedestal + brass hood), coils, bucket, lantern, barrels, capstan
    bx, by = 0.55, 39.3
    mb.box(M['oak'], (bx, by, ZF + 0.4), (0.55, 0.5, 0.8)); mb.box(M['cap'], (bx, by, ZF + 0.83), (0.62, 0.56, 0.06))
    mb.cyl(M['brass'], (bx, by, ZF + 0.95), 0.26, 0.2, seg=16, smooth=True); mb.ell(M['brass'], (bx, by, ZF + 1.05), (0.26, 0.26, 0.24), (16, 10)); mb.cyl(M['brass'], (bx, by, ZF + 0.87), 0.29, 0.05, seg=16)
    mb.ell(M['red'], (bx, by - 0.26, ZF + 0.95), (0.05, 0.02, 0.05), (6, 4))
    for (cx, cy, r, n) in [(-0.55, 39.5, 0.3, 3), (1.05, 39.0, 0.28, 3)]:
        for l in range(n): ring_xy(mb, M['rope'], (cx, cy, ZF + 0.06 + l * 0.1), r * (1 - 0.06 * l), 0.1, 0.1, 16)
        mb.cyl(M['rope'], (cx, cy, ZF + 0.06 + (n - 1) * 0.05), r * 0.8, 0.1 * n, seg=16)
    mb.cyl(M['oak'], (1.6, 39.1, ZF + 0.17), 0.17, 0.34, seg=12, r2=0.21); mb.cyl(M['iron'], (1.6, 39.1, ZF + 0.3), 0.21, 0.03, seg=12)      # bucket
    lx, ly = -0.1, 39.0                                                                    # lantern (emitter)
    mb.box(M['iron'], (lx, ly, ZF + 0.03), (0.22, 0.22, 0.06)); mb.box(M['iron'], (lx, ly, ZF + 0.4), (0.24, 0.24, 0.04))
    for dx, dy in ((-0.1, -0.1), (0.1, -0.1), (-0.1, 0.1), (0.1, 0.1)): mb.box(M['iron'], (lx + dx, ly + dy, ZF + 0.21), (0.025, 0.025, 0.36))
    lm = MB('flame'); lm.box(M['lamp'], (lx, ly, ZF + 0.2), (0.15, 0.15, 0.28)); lm.finish(shadow=False)
    for (bx2, by2) in [(-1.35, 40.2), (-1.0, 41.1)]:
        mb.ell(M['oak'], (bx2, by2, ZF + 0.45), (0.3, 0.3, 0.44), (14, 10))
        for z in (0.2, 0.45, 0.7): mb.cyl(M['iron'], (bx2, by2, ZF + z), 0.27, 0.035, seg=14)
    mb.cyl(M['cap'], (0.9, 44.6, ZF + 0.4), 0.25, 0.8, seg=10)                             # bitts
    # ---- waist guns behind (just visible not at all) skipped. Foremast (behind the camera) with its stays and jibs ahead
    mx, my = 0.2, 22.0
    tube(mb, M['mast'], (mx, my, DECK), (mx, my, 26), 0.52, 0.28, 12); tube(mb, M['mast'], (mx, my, 20), (mx, my, 40), 0.3, 0.16, 10)
    mb.box(M['mast'], (mx, my, 19.8), (3.0, 2.2, 0.22))
    for (zy, ln, r) in [(15.0, 13.0, 0.17), (26.6, 9.4, 0.13)]: tube(mb, M['mast'], (mx - ln / 2, my, zy), (mx + ln / 2, my, zy), r, r * 0.6, 8)
    sail_quad(mb, M, mx - 6.0, mx + 6.0, 8.8, 14.8, my + 0.6, 1.5)
    tube(mb, M['mast'], (0, 44.0, 9.4), (0, 62.0, 14.5), 0.2, 0.1, 10)                    # bowsprit
    mb.box(M['mast'], (0, 46.3, 9.9), (0.9, 0.5, 0.3))
    tube(mb, M['rig'], (mx, my, 40), (0, 61.0, 14.2), 0.045, 0.045, 4)                    # fore-topmast stay
    tube(mb, M['rig'], (mx, my, 33), (0, 56.0, 13.4), 0.045, 0.045, 4)
    tube(mb, M['rig'], (mx, my, 27), (0, 50.0, 12.0), 0.045, 0.045, 4)
    sail_tri(mb, M, (0, 60.5, 13.6), (0, 51.0, 11.8), (0, 55.5, 18.5), 1.1)                # outer jib
    sail_tri(mb, M, (0, 55.0, 12.8), (0, 48.6, 11.0), (0, 51.0, 17.5), 1.0)                # fore-topmast staysail
    sail_tri(mb, M, (0, 50.0, 11.8), (0, 46.6, 10.6), (0, 46.5, 16.5), 0.8)
    tube(mb, M['mast'], (-1.2, 52.0, 10.2), (1.2, 52.0, 10.2), 0.07, 0.07, 6)               # spritsail yard + sail
    sail_quad(mb, M, -1.7, 1.7, 7.0, 10.0, 52.3, 0.45, 6, 8)
    for s in (-1, 1):                                                                      # shrouds visible on the sides far away: skipped (behind camera); extra rigging overhead
        tube(mb, M['rig'], (s * 0.1, 62.0, 14.5), (s * 3.3, 44.0, ZF + 0.9), 0.04, 0.04, 4)   # bobstays/stay lines to the bow
    tube(mb, M['rig'], (0, 62.0, 14.3), (0, 45.5, 7.5), 0.04, 0.04, 4)
    mb.quad(M['red'], [(0, 61.9, 14.9), (0, 61.9, 14.3), (0, 59.0, 14.2), (0, 59.0, 14.9)])
    mb.finish()
    # ---- far dressing: green-headed headland with a pale beach and haze, tiny dark sail
    ib = MB('isle'); n = 48; X0i = 780
    for i in range(n):
        x0 = X0i + i * 7.0; x1 = x0 + 7.0
        f = lambda x: 70 * max(0, math.sin(math.pi * (x - X0i) / (n * 7.0))) ** 0.6 * (0.8 + 0.2 * math.sin((x - X0i) / 11.0)) + 6
        ib.quad(M['isle'] if i % 3 else M['isle2'], [(x0, 1800, 0), (x1, 1800, 0), (x1, 1800, f(x1)), (x0, 1800, f(x0))])
        ib.quad(M['beach'], [(x0, 1799, -0.5), (x1, 1799, -0.5), (x1, 1799, 3.5), (x0, 1799, 3.5)])
    ib.finish(shadow=False)
    sb_ = MB('farsail'); sb_.quad(M['darksail'], [(430, 1500, 0.5), (456, 1500, 0.5), (448, 1500, 24), (434, 1500, 28)]); sb_.quad(M['darksail'], [(425, 1500, 0.5), (455, 1500, 0.5), (455, 1500, 3), (425, 1500, 3)]); sb_.finish(shadow=False)
    cm = MB('cards')
    if not os.environ.get('NOCARDS'): card(cm, M['grey'], 0.35, 41.3, w=0.55, z0=ZF); card(cm, M['grey'], 1.05, 42.0, w=0.55, z0=ZF); cm.finish()
    if not os.environ.get('NOSEA'): build_sea(P)
    clouds(P)

# ---------------------------------------------------------------- the sea (v2): long smooth swells built per camera pixel, layered colour, contour foam streaks, bow wave + V-wake, one narrow glitter path
def build_sea(P):
    c = P['cam']; loc = np.array(c['loc'], dtype=np.float64); look = np.array(c['look'], dtype=np.float64)
    f = look - loc; f /= np.linalg.norm(f); r = np.cross(f, [0, 0, 1.0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    hx, hy = 0.4602 * 1.12, 0.8182
    zfar = loc[2] / 7000.0
    vmax = (-zfar - f[2]) / (u[2] * hy); vmin = -1.18
    NU, NV = 440, 800
    uu = np.linspace(-1.12, 1.12, NU); vv = vmin + (vmax - vmin) * np.linspace(0, 1, NV)
    UU, VV = np.meshgrid(uu, vv)
    ray = f[None, None, :] + r[None, None, :] * (UU * hx)[..., None] + u[None, None, :] * (VV * hy)[..., None]
    t = -loc[2] / ray[..., 2]; px = loc[0] + ray[..., 0] * t; py = loc[1] + ray[..., 1] * t
    sdep = np.abs(ray[..., 2]) / np.linalg.norm(ray, axis=-1)
    rng = np.random.RandomState(7)
    th0 = math.radians(95); waves = []
    # (wavelength, amplitude): long rolling swells; steepness 2*pi*A/L about 0.07-0.1
    spec = [(70, 1.0), (42, .62), (26, .4), (16, .22), (10.5, .13), (6.5, .075), (4.2, .04)]
    for (L, A) in spec:
        a = th0 + rng.uniform(-0.55, 0.55); waves.append((L, A, a, rng.uniform(0, 6.28)))
    rip = [(0.9, 0.012), (0.6, 0.008), (0.4, 0.006), (0.27, 0.004)]
    rip = [(L, A, th0 + rng.uniform(-1.2, 1.2), rng.uniform(0, 6.28)) for (L, A) in rip]
    fpx = t * (2 * hx / 720.0) * 1.1
    h = np.zeros_like(px); gx = np.zeros_like(px); gy = np.zeros_like(px)
    wm = np.zeros_like(px); wgx = np.zeros_like(px); wgy = np.zeros_like(px); norm_m = 0.0
    gsx = np.zeros_like(px); gsy = np.zeros_like(px)
    WARP = 3.2 * np.sin(0.021 * px + 1.3 * np.sin(0.03 * py)) + 2.4 * np.sin(0.027 * py + 1.1 * np.sin(0.02 * px)) + 1.6 * np.sin(0.06 * px + 0.04 * py)
    wpx = np.maximum(fpx / np.maximum(sdep, 0.05), 0.02) * 1.6
    brk = 0.5 + 0.5 * np.sin(px * 0.11 + 1.7 * np.sin(py * 0.06)) * np.sin(py * 0.09 + 0.9 * np.sin(px * 0.05))
    lines = np.zeros_like(px)
    for (L, A, a, ph) in waves:
        k = 2 * math.pi / L; kx = k * math.cos(a); ky = k * math.sin(a)
        fade = np.clip((L / np.maximum(fpx, 1e-6) - 5.0) / 9.0, 0, 1)
        th = kx * px + ky * py + ph + WARP; s = np.sin(th); cs = np.cos(th)
        if 9 <= L <= 30:
            lines = np.maximum(lines, np.clip(1 - (1 - s) / np.maximum((k * wpx) ** 2 / 2, 1e-5), 0, 1) ** 1.2 * (0.9 if L < 20 else 0.7))
        q = 0.5 + 0.5 * s; hh = A * (2 * q ** 1.6 - 1.0); dh = A * 2 * 1.6 * q ** 0.6 * 0.5 * cs * k
        h += hh * fade; gx += dh * math.cos(a) * fade; gy += dh * math.sin(a) * fade
        if 6 <= L <= 30:
            wm += hh / A * fade; wgx += dh / A * math.cos(a) * fade; wgy += dh / A * math.sin(a) * fade; norm_m += 1
    for (L, A, a, ph) in rip:
        k = 2 * math.pi / L; th = k * (math.cos(a) * px + math.sin(a) * py) + ph; dh = A * k * np.cos(th)
        gsx += dh * math.cos(a) * 1.5; gsy += dh * math.sin(a) * 1.5
    far = np.clip(1 - t / 3500.0, 0, 1) ** 0.5
    h *= far
    # bow wave: a raised foamy mound ahead of the stem
    sx, sy = 0.0, STEM + 3.0
    h += 0.55 * np.exp(-(((px - sx) / 2.2) ** 2 + ((py - sy) / 3.2) ** 2))
    wmn = wm / max(norm_m, 1); gm = np.sqrt(wgx ** 2 + wgy ** 2) / max(norm_m, 1) + 1e-4
    # smooth contour foam streaks: constant ~2.5 px wide, broken up by long noise, fading with distance
    lines *= np.clip((brk - 0.45) / 0.2, 0, 1) * np.clip(1 - t / 900, 0, 1)
    crest = np.clip((wmn - 0.1) / 0.7, 0, 1) * 0.55
    # hull wash, V-wake arms and bow foam
    hh_ = hw(np.clip(py, -6, STEM)); d_hull = np.abs(px) - (hh_ + 0.9); d_hull = np.where((py > -6) & (py < STEM + 1), d_hull, 9)
    wash = np.exp(-np.maximum(d_hull, 0) / 1.1) * (d_hull < 3) * (0.6 + 0.4 * np.sin(py * 0.22 + px * 0.3)) * 0.6
    dback = np.maximum(STEM - py, 0.0)
    arm = np.zeros_like(px)
    for off in (2.2, 4.8, 7.6):                    # V arms flaring back from the bow, thin broken streaks
        dd = np.abs(np.abs(px) - (hh_ + 0.9 + off * (0.35 + 0.5 * np.clip(dback / 30.0, 0, 1)))); arm = np.maximum(arm, np.clip(1 - dd / (0.4 + 0.08 * off), 0, 1) ** 1.0 * np.clip(1 - dback / (22.0 + 8 * off), 0, 1) * (py < STEM + 4))
    arm *= (0.6 + 0.4 * np.sin(py * 0.25 + np.abs(px) * 0.3) ** 2)
    bow = np.exp(-(((px - sx) / 4.6) ** 2 + ((py - sy) / 6.5) ** 2)) * (0.65 + 0.35 * np.sin(px * 0.6) * np.sin(py * 0.5 + 1.0))
    foam = np.clip(np.maximum.reduce([lines * 0.9, wash * 0.85, arm * 1.0, bow * 1.3]), 0, 1)
    # colour distance bands
    d_mid = np.clip((t - 14.0) / 120.0, 0, 1); haze = np.clip((t - 250.0) / 2400.0, 0, 1) ** 0.8
    # glitter: one narrow path under the (virtual) sun azimuth
    nx_ = -(gx + gsx); ny_ = -(gy + gsy); nz_ = np.ones_like(px); nl = np.sqrt(nx_ ** 2 + ny_ ** 2 + nz_ ** 2); nx_ /= nl; ny_ /= nl; nz_ /= nl
    vx = px - loc[0]; vy = py - loc[1]; vz = h - loc[2]; vl = np.sqrt(vx ** 2 + vy ** 2 + vz ** 2); vx /= vl; vy /= vl; vz /= vl
    dn = vx * nx_ + vy * ny_ + vz * nz_
    Rx = vx - 2 * dn * nx_; Ry = vy - 2 * dn * ny_; Rz = vz - 2 * dn * nz_
    se = math.radians(P['glit_el']); sa = math.radians(P['glit_az'])
    S = np.array([math.sin(sa) * math.cos(se), math.cos(sa) * math.cos(se), math.sin(se)])
    dd = Rx * S[0] + Ry * S[1] + Rz * S[2]
    glit = np.clip((dd - P['glit_lo']) / (P['glit_hi'] - P['glit_lo']), 0, 1) ** 1.5
    az = np.arctan2(px - loc[0], py - loc[1]); daz = az - sa
    glit *= np.exp(-(daz / (0.045 + 0.00004 * t)) ** 2) * np.clip(1 - t / 2200, 0.2, 1) * (1 - 0.6 * foam)
    verts = np.stack([px, py, h], -1).reshape(-1, 3).astype(np.float32)
    idx = np.arange(NU * NV).reshape(NV, NU)
    quads = np.stack([idx[:-1, :-1], idx[:-1, 1:], idx[1:, 1:], idx[1:, :-1]], -1).reshape(-1, 4)
    me = bpy.data.meshes.new('sea'); me.vertices.add(len(verts)); me.vertices.foreach_set('co', verts.ravel())
    nl_ = len(quads); me.loops.add(nl_ * 4); me.polygons.add(nl_)
    me.loops.foreach_set('vertex_index', quads.ravel().astype(np.int32)); me.polygons.foreach_set('loop_start', (np.arange(nl_) * 4).astype(np.int32)); me.polygons.foreach_set('loop_total', np.full(nl_, 4, dtype=np.int32))
    me.update(calc_edges=True); me.polygons.foreach_set('use_smooth', np.ones(nl_, dtype=bool))
    for name, arr in (('foam', foam), ('crest', crest), ('haze', haze), ('dmid', d_mid), ('glit', glit)):
        at = me.attributes.new(name, 'FLOAT', 'POINT'); at.data.foreach_set('value', arr.reshape(-1).astype(np.float32))
    ob = bpy.data.objects.new('sea', me); bpy.context.scene.collection.objects.link(ob)
    m = bpy.data.materials.new('sea'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); bs.inputs['Roughness'].default_value = 0.6; bs.inputs['Specular IOR Level'].default_value = 0.0
    def attr(n):
        a = N('ShaderNodeAttribute'); a.attribute_type = 'GEOMETRY'; a.attribute_name = n; return a.outputs['Fac']
    def mix(a, b, fac):
        mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'
        if hasattr(a, 'node'): L(a, mx.inputs[6])
        else: mx.inputs[6].default_value = a
        if hasattr(b, 'node'): L(b, mx.inputs[7])
        else: mx.inputs[7].default_value = b
        L(fac, mx.inputs[0]); return mx.outputs[2]
    col = mix(hexc(P['sea_deep']), hexc(P['sea_mid']), attr('dmid'))
    col = mix(col, hexc(P['sea_crest']), attr('crest'))
    col = mix(col, hexc(P['sea_haze']), attr('haze'))
    col = mix(col, hexc('#f4f8f4'), attr('foam'))
    L(col, bs.inputs['Base Color'])
    gm_ = N('ShaderNodeMath'); gm_.operation = 'MULTIPLY'; gm_.inputs[1].default_value = P.get('glit_k', 5.0); L(attr('glit'), gm_.inputs[0])
    bs.inputs['Emission Color'].default_value = hexc('#fff2cc'); L(gm_.outputs[0], bs.inputs['Emission Strength'])
    L(bs.outputs[0], out.inputs['Surface']); ob.data.materials.append(m)

PRESETS['ship'] = dict(
    sky=[(0.0, '#6c9ce0'), (0.46, '#a9c6e6'), (0.5, '#9dbfe6'), (0.58, '#7ea8e2'), (0.78, '#5b88d6'), (1.0, '#4a78cd')], sky_k=1.0,
    key=(1.0, 0.88, 0.7, 7.5), key_dir=kdir(22, 46), sun_angle=0.9, exposure=0.1, sat=1.08, amb=('#3050FF', 1.9), samples=80, dbounce=1,
    cloud=('#fffaf0', '#8c9ce8'), cloud_diffuse=True, cloud_z=(70, 170), ncloud=8, cloud_seed=4, cloud_scale=0.8,
    sea_deep='#0a4452', sea_mid='#2a8a8c', sea_crest='#48aaa0', sea_haze='#9cbccb',
    glit_az=20, glit_el=18, glit_lo=0.9975, glit_hi=0.9996, glit_k=4.0,
    cam=dict(loc=(1.2, 37.0, 12.4), look=(0.5, 61.5, -0.5), lens=22))

def lights_ship(P):
    sun_light(P); w = sky_world(P)

# ================================================================== STILL 3: the astronomers' hall (Board of Longitude)
def hall_mats():
    M = {}
    M['wall'] = mat('hwall', '#7e3028', '#92392c', scale=1.4, contrast=1.1, zgrad=(0.0, 1.0, '#5c2228'))
    M['wall2'] = mat('hwall2', '#7a2c26', '#8c3a2c', scale=1.8)
    M['ceil'] = mat('hceil', '#94503a', '#a65e44', scale=1.2)
    M['wain'] = mat('hwain', '#4c2616', '#5e3220', scale=4, aniso=(0.3, 1, 1))
    M['wood'] = mat('hwood', '#976c4d', '#82583c', scale=5, aniso=(0.15, 1, 1), contrast=1.2)
    M['woodd'] = mat('hwoodd', '#5a3220', '#70402a', scale=5, aniso=(0.15, 1, 1))
    M['floor1'] = mat('hfl1', '#8a5e40', '#a07048', scale=2.2, aniso=(0.5, 0.12, 1))
    M['floor2'] = mat('hfl2', '#744c34', '#8a5e40', scale=2.2, aniso=(0.5, 0.12, 1))
    M['rug'] = mat('hrug', '#0a1432', '#101c44', scale=6, contrast=1.1)
    M['rugb'] = mat('hrugb', '#5a1e2a', '#6c2432', scale=6)
    M['gold'] = metal_mat('hgold', '#cb9f48', '#e2b85a', rough=0.35, spec=0.5)
    M['brass'] = metal_mat('hbrass', '#b8862c', '#d4a43e', rough=0.35, spec=0.5)
    M['brassd'] = metal_mat('hbrassd', '#7e5520', '#a0722e', rough=0.45, spec=0.3)
    M['curt'] = mat('hcurt', '#9a2430', '#b43434', scale=9, aniso=(3, 0.5, 0.15), contrast=1.3)
    M['baize'] = mat('hbaize', '#2c6a3a', '#3a7c46', scale=10)
    M['paper'] = mat('hpaper', '#e8d6a8', '#dcc592', scale=6)
    M['ink'] = mat('hink', '#2a1c30')
    M['cream'] = mat('hcream', '#e6cf9c', '#d8bd88', scale=5)
    M['navy'] = mat('hnavy', '#1a2a5c', '#26387a', scale=5)
    M['teal'] = mat('hteal', '#2a7a8a', '#3a9098', scale=3)
    M['tan'] = mat('htan', '#c89a58', '#b8864a', scale=3)
    M['redp'] = mat('hredp', '#a02a2e', '#b83c34', scale=4)
    M['gl_b'] = mat('hglb', '#1c2e66', '#2a4082', scale=4)
    M['moon'] = mat('hmoon', '#dcc896', '#c8b07a', scale=3)
    M['crater'] = mat('hcrater', '#9a8456', '#8a7448', scale=3)
    M['seat'] = mat('hseat', '#1c2c60', '#2c3c78', scale=8)
    M['grey'] = mat('hgrey', '#a4a8b8')
    M['green'] = mat('hgreen', '#4a7a40', '#5c8c4c', scale=4)
    M['flame'] = mat_emit('hflame', '#ffc860', 28.0)
    M['book1'] = mat('hbk1', '#7a2a2a', '#8e3a30'); M['book2'] = mat('hbk2', '#2a4a6a', '#3a5c7c'); M['book3'] = mat('hbk3', '#6a5a2a', '#7e6c34'); M['book4'] = mat('hbk4', '#3a5a3a', '#4a6c46')
    return M

def candles(mb, M, fl, pts, h=0.18):
    for (x, y, z) in pts:
        mb.cyl(M['cream'], (x, y, z + h / 2), 0.018, h, seg=8); fl.ell(M['flame'], (x, y, z + h + 0.04), (0.02, 0.02, 0.05), (8, 6))

def build_hall(P):
    M = hall_mats(); mb = MB('hall'); fl = MB('flame'); rr = rnd(31)
    X0, X1, Y0, Y1, ZH = -3.6, 3.6, -3.4, 5.6, 6.0
    # ---- floor: parquet planks along y, navy rug with crimson border and a gold line
    for i in range(36):
        x = X0 + 0.2 * i + 0.1; mb.box(M['floor1'] if i % 2 else M['floor2'], (x, (Y0 + Y1) / 2, -0.03), (0.195, Y1 - Y0, 0.06))
    mb.box(M['ink'], (0, (Y0 + Y1) / 2, -0.08), (8, 10, 0.05))
    rx0, rx1, ry0, ry1 = -1.9, 1.1, -2.6, 4.3
    mb.box(M['rugb'], ((rx0 + rx1) / 2, (ry0 + ry1) / 2, 0.012), (rx1 - rx0 + 0.5, ry1 - ry0 + 0.5, 0.024)); mb.box(M['gold'], ((rx0 + rx1) / 2, (ry0 + ry1) / 2, 0.026), (rx1 - rx0 + 0.3, ry1 - ry0 + 0.3, 0.012))
    mb.box(M['rug'], ((rx0 + rx1) / 2, (ry0 + ry1) / 2, 0.034), (rx1 - rx0 + 0.18, ry1 - ry0 + 0.18, 0.02))
    for k in range(4): mb.box(M['rugb'], ((rx0 + rx1) / 2, ry0 + 1.0 + 1.5 * k, 0.046), (1.5, 0.5, 0.012))
    # ---- shell: walls, ceiling, cornice, wainscot, pilasters
    wx0, wx1, wz0, wz1, rad = -1.0, 1.0, 1.2, 3.6, 1.0
    mb.box(M['wall'], (X0 - 0.15, (Y0 + Y1) / 2, ZH / 2), (0.3, Y1 - Y0 + 0.6, ZH)); mb.box(M['wall'], (X1 + 0.15, (Y0 + Y1) / 2, ZH / 2), (0.3, Y1 - Y0 + 0.6, ZH))
    mb.box(M['wall'], (0, Y0 - 0.15, ZH / 2), (8, 0.3, ZH)); mb.box(M['ceil'], (0, (Y0 + Y1) / 2, ZH + 0.15), (8, Y1 - Y0 + 0.6, 0.3))
    ty = Y1 + 0.15
    mb.box(M['wall'], ((X0 + wx0) / 2 - 0.15, ty, ZH / 2), (wx0 - X0 + 0.3, 0.3, ZH)); mb.box(M['wall'], ((X1 + wx1) / 2 + 0.15, ty, ZH / 2), (X1 - wx1 + 0.3, 0.3, ZH))
    mb.box(M['wall'], (0, ty, wz0 / 2), (2.0, 0.3, wz0)); mb.box(M['wall'], (0, ty, (wz1 + rad + ZH) / 2 + 0.0), (2.0, 0.3, ZH - wz1 - rad))
    n = 18
    for i in range(n):                                          # stepped arch
        za = wz1 + rad * i / n; zb = wz1 + rad * (i + 1) / n; zm = (za + zb) / 2; w = math.sqrt(max(0, rad ** 2 - (zm - wz1) ** 2))
        for s in (-1, 1): mb.box(M['wall'], (s * (w + 1.0) / 2, ty, (za + zb) / 2), (1.0 - w + 0.02, 0.3, zb - za + 0.005))
    mb.box(M['wall'], (0, ty, (wz1 + 0.0) / 1.0 + 0.0), (0.001, 0.001, 0.001))
    gl = MB('glass'); sk = mat_emit('hsky', '#a8c8f4', 1.5); hd = mat_emit('hhedge', '#4e7a58', 0.55); rf = mat_emit('hroof', '#b86a4a', 0.7)
    gl.quad(sk, [(-1.0, Y1 + 0.4, wz0 + 0.8), (1.0, Y1 + 0.4, wz0 + 0.8), (1.0, Y1 + 0.4, wz1), (-1.0, Y1 + 0.4, wz1)][::-1])
    for i in range(n):
        za = wz1 + rad * i / n; zb = wz1 + rad * (i + 1) / n; w = math.sqrt(max(0, rad ** 2 - ((za + zb) / 2 - wz1) ** 2)); gl.quad(sk, [(-w, Y1 + 0.4, za), (w, Y1 + 0.4, za), (w, Y1 + 0.4, zb), (-w, Y1 + 0.4, zb)])
    gl.quad(hd, [(-1.0, Y1 + 0.39, wz0), (1.0, Y1 + 0.39, wz0), (1.0, Y1 + 0.39, wz0 + 0.8), (-1.0, Y1 + 0.39, wz0 + 0.8)][::-1])
    gl.quad(rf, [(-0.3, Y1 + 0.38, wz0 + 0.7), (0.9, Y1 + 0.38, wz0 + 0.7), (0.9, Y1 + 0.38, wz0 + 1.0), (-0.3, Y1 + 0.38, wz0 + 1.0)][::-1]); gl.finish(shadow=False)
    yw = Y1 + 0.02                                                # sash bars + arch ring + frame
    for x in (-0.5, 0.0, 0.5): mb.box(M['woodd'], (x, yw, (wz0 + wz1 + 0.8) / 2), (0.04, 0.05, wz1 - wz0 + 0.8))
    for k in range(1, 7): mb.box(M['woodd'], (0, yw, wz0 + k * (wz1 - wz0) / 7), (2.0, 0.05, 0.035))
    for i in range(n):
        a = math.pi * (i + 0.5) / n; sg = math.pi * rad / n * 1.1
        mb.box(M['woodd'], (rad * math.cos(a), yw, wz1 + rad * math.sin(a)), (sg, 0.07, 0.08), ry=-(a + math.pi / 2))
    for a in (math.pi * 0.25, math.pi * 0.5, math.pi * 0.75): mb.box(M['woodd'], (0, yw, wz1), (2 * rad, 0.05, 0.03), ry=-a)
    for x in (-1.0, 1.0): mb.box(M['woodd'], (x, yw, (wz0 + wz1) / 2), (0.1, 0.12, wz1 - wz0))
    mb.box(M['woodd'], (0, yw - 0.1, wz0 - 0.03), (2.3, 0.4, 0.07))
    mb.box(M['gold'], (0, Y1 - 0.1, ZH - 0.12), (8, 0.3, 0.22)); mb.box(M['gold'], (X0 + 0.1, 1.0, ZH - 0.12), (0.3, 9, 0.22)); mb.box(M['gold'], (X1 - 0.1, 1.0, ZH - 0.12), (0.3, 9, 0.22))   # cornice
    mb.box(M['wain'], (0, Y1 - 0.06, 0.55), (7.2, 0.14, 1.1)); mb.box(M['wood'], (0, Y1 - 0.1, 1.12), (7.2, 0.2, 0.07))
    for x in (-3.2, -2.55, 2.55, 3.2, -1.9, 1.9): mb.box(M['woodd'], (x, Y1 - 0.12, 0.55), (0.4, 0.04, 0.8))
    mb.box(M['wain'], (X0 + 0.06, 1.0, 0.55), (0.14, 9.0, 1.1)); mb.box(M['wain'], (X1 - 0.06, 1.0, 0.55), (0.14, 9.0, 1.1)); mb.box(M['wood'], (X0 + 0.1, 1.0, 1.12), (0.2, 9, 0.07)); mb.box(M['wood'], (X1 - 0.1, 1.0, 1.12), (0.2, 9, 0.07))
    for x in (-3.55, -2.1, 2.1, 3.55): mb.box(M['cream'], (x, Y1 - 0.12, 3.0), (0.32, 0.22, 3.6)); mb.box(M['gold'], (x, Y1 - 0.14, 4.9), (0.4, 0.26, 0.14)); mb.box(M['gold'], (x, Y1 - 0.14, 1.2), (0.4, 0.26, 0.1))
    # ---- crimson curtains + gilt pelmet + tie-backs
    for s in (-1, 1):
        for k in range(6):
            xx = s * (1.28 + 0.11 * k); mb.box(M['curt'], (xx, Y1 - 0.2 - 0.04 * (k % 2), 2.7), (0.14, 0.16 + 0.05 * (k % 3), 4.4))
        mb.box(M['gold'], (s * 1.55, Y1 - 0.2, 1.8), (0.6, 0.1, 0.07), rz=0.0)
    mb.box(M['gold'], (0, Y1 - 0.2, 5.0), (3.2, 0.2, 0.22)); mb.box(M['curt'], (0, Y1 - 0.25, 4.82), (3.0, 0.14, 0.2))
    # ---- big painted Moon disc (left) in a gilt ring, portrait frames (right), bookcase
    mx, mz = -2.8, 3.5
    mb.cyl(M['moon'], (mx, Y1 - 0.12, mz), 0.95, 0.07, axis='y', seg=28)
    for (dx, dz, r) in [(-0.3, 0.3, 0.2), (0.25, 0.1, 0.14), (0.1, -0.35, 0.24), (-0.4, -0.2, 0.1), (0.45, 0.45, 0.09), (-0.05, 0.55, 0.11)]: mb.cyl(M['crater'], (mx + dx, Y1 - 0.17, mz + dz), r, 0.03, axis='y', seg=14)
    ring_xz(mb, M['gold'], (mx, Y1 - 0.14, mz), 0.99, 0.08, 0.1, n=28)
    for (fx, fz, fw, fh, col) in [(2.9, 3.4, 0.85, 1.15, 'navy'), (2.9, 2.0, 0.6, 0.7, 'teal')]:
        mb.box(M['gold'], (fx, Y1 - 0.12, fz), (fw + 0.16, 0.06, fh + 0.16)); mb.box(M[col], (fx, Y1 - 0.16, fz), (fw, 0.04, fh)); mb.ell(M['tan'], (fx, Y1 - 0.2, fz + fh * 0.15), (fw * 0.18, 0.02, fh * 0.16), (12, 8)); mb.box(M['ink'], (fx, Y1 - 0.2, fz - fh * 0.15), (fw * 0.5, 0.02, fh * 0.3))
    # ---- long table with green baize + charts (dots and lines only), brass instruments
    tx0, tx1, ty0, ty1, tz = 1.35, 2.75, -0.7, 3.7, 0.8
    mb.box(M['woodd'], ((tx0 + tx1) / 2, (ty0 + ty1) / 2, tz - 0.05), (tx1 - tx0, ty1 - ty0, 0.1)); mb.box(M['baize'], ((tx0 + tx1) / 2, (ty0 + ty1) / 2, tz + 0.006), (tx1 - tx0 - 0.14, ty1 - ty0 - 0.14, 0.014))
    for x in (tx0 + 0.12, tx1 - 0.12):
        for y in (ty0 + 0.12, ty1 - 0.12): mb.box(M['wood'], (x, y, tz / 2 - 0.05), (0.13, 0.13, tz - 0.1)); mb.ell(M['wood'], (x, y, tz * 0.45), (0.1, 0.1, 0.12), (8, 6))
    mb.box(M['woodd'], ((tx0 + tx1) / 2, (ty0 + ty1) / 2, 0.3), (0.06, ty1 - ty0 - 0.3, 0.06))
    charts = [(2.0, 0.1, 0.7, 0.55, 0.2), (2.15, 1.05, 0.75, 0.6, -0.15), (1.8, 1.95, 0.65, 0.5, 0.1), (2.25, 2.8, 0.7, 0.55, -0.25), (1.65, 3.2, 0.5, 0.45, 0.3)]
    for (cx, cy, cw, ch, rz) in charts:
        mb.box(M['paper'], (cx, cy, tz + 0.02), (cw, ch, 0.008), rz=rz)
        mb.push(Matrix.Translation((cx, cy, tz + 0.025)) @ Euler((0, 0, rz)).to_matrix().to_4x4())
        for k in range(9): mb.ell(M['ink'], (rr.uniform(-cw / 2.4, cw / 2.4), rr.uniform(-ch / 2.4, ch / 2.4), 0), (0.012, 0.012, 0.004), (6, 4))
        for k in range(3): mb.box(M['ink'], (rr.uniform(-cw / 4, cw / 4), rr.uniform(-ch / 4, ch / 4), 0), (cw * rr.uniform(0.3, 0.6), 0.006, 0.004), rz=rr.uniform(0, 3.14))
        mb.pop()
    mb.cyl(M['paper'], (1.55, 0.7, tz + 0.06), 0.05, 0.5, axis='y', seg=10); mb.cyl(M['paper'], (1.62, 2.4, tz + 0.06), 0.045, 0.45, axis='y', seg=10)       # rolled charts
    mb.box(M['brass'], (2.5, 1.7, tz + 0.03), (0.3, 0.3, 0.04)); ring_xy(mb, M['brass'], (2.5, 1.7, tz + 0.07), 0.12, 0.02, 0.025, 14)                         # octant/sextant stand-in
    mb.cyl(M['ink'], (2.5, 0.35, tz + 0.05), 0.04, 0.08, seg=8); mb.rod(M['cream'], (2.5, 0.35, tz + 0.1), (2.58, 0.28, tz + 0.35), 0.008, 0.012, 5)        # inkwell + quill
    # candelabra on the table (5 branches)
    cxb, cyb = 2.0, 2.2
    mb.cyl(M['gold'], (cxb, cyb, tz + 0.03), 0.09, 0.05, seg=12); mb.rod(M['gold'], (cxb, cyb, tz + 0.04), (cxb, cyb, tz + 0.46), 0.022, 0.016, 8)
    pts = []
    for a in range(5):
        ang = a * 1.2566; ex = cxb + 0.2 * math.cos(ang); ey = cyb + 0.2 * math.sin(ang)
        mb.rod(M['gold'], (cxb, cyb, tz + 0.3), (ex, ey, tz + 0.4), 0.012, 0.012, 6); mb.cyl(M['gold'], (ex, ey, tz + 0.405), 0.03, 0.03, seg=8); pts.append((ex, ey, tz + 0.42))
    candles(mb, M, fl, pts, 0.17)
    # chairs along the table (Georgian: navy seat, tall backs)
    for (cx, cy, yaw) in [(0.85, 0.5, -1.5708), (0.85, 1.7, -1.5708), (0.9, 2.9, -1.5708 + 0.2)]:
        mb.push(Matrix.Translation((cx, cy, 0)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
        mb.box(M['seat'], (0, 0, 0.46), (0.46, 0.46, 0.08)); mb.box(M['woodd'], (0, 0, 0.4), (0.5, 0.5, 0.05))
        for dx in (-0.2, 0.2):
            for dy in (-0.2, 0.2): mb.box(M['wood'], (dx, dy, 0.2), (0.05, 0.05, 0.4))
        mb.box(M['wood'], (0, 0.22, 0.85), (0.46, 0.05, 0.7)); mb.box(M['seat'], (0, 0.19, 0.88), (0.34, 0.03, 0.4)); mb.pop()
    # ---- telescope on a tripod, pointed at the window
    ex, ey, ez = -2.2, 2.0, 1.35; ox, oy, oz = -0.95, 4.35, 3.05
    d = Vector((ox - ex, oy - ey, oz - ez)); L = d.length; u = d / L
    def at(t): return (ex + u.x * L * t, ey + u.y * L * t, ez + u.z * L * t)
    mb.rod(M['gold'], at(0.0), at(0.35), 0.07, 0.11, 18, True, True); mb.rod(M['brass'], at(0.35), at(0.7), 0.11, 0.15, 18, True, True); mb.rod(M['gold'], at(0.7), at(1.0), 0.15, 0.19, 18, True, True)
    for t in (0.35, 0.7, 0.98): mb.rod(M['gold'], at(t - 0.015), at(t + 0.015), 0.2 * (0.6 + 0.4 * t) + 0.02, 0.2 * (0.6 + 0.4 * t) + 0.02, 18, True, True)
    mb.rod(M['gold'], at(1.0), at(1.03), 0.21, 0.19, 18, True, True)
    mb.rod(M['brassd'], at(-0.0), at(-0.05), 0.03, 0.05, 10)                                                             # eyepiece
    mb.rod(M['brassd'], at(0.2), at(0.75), 0.03, 0.045, 10); mb.rod(M['brassd'], at(0.25), (at(0.25)[0] + 0.0, at(0.25)[1], at(0.25)[2] + 0.17), 0.012, 0.012, 5)   # finder
    pv = at(0.5)
    for (lx, ly) in [(-0.7, -0.55), (0.65, -0.5), (0.0, 0.75)]:
        mb.rod(M['woodd'], (pv[0], pv[1], pv[2] - 0.15), (pv[0] + lx, pv[1] + ly, 0.0), 0.05, 0.035, 8, True, True)
    mb.ell(M['brass'], (pv[0], pv[1], pv[2] - 0.15), (0.1, 0.1, 0.09), (12, 8)); mb.cyl(M['brass'], (pv[0], pv[1], pv[2] - 0.2), 0.07, 0.12, seg=10)
    # ---- globes: celestial (navy with gold dots) and terrestrial (teal/tan), on stands
    for (gx, gy, gr, kind) in [(1.9, 4.05, 0.42, 'cel'), (2.85, 4.4, 0.3, 'ter')]:
        mb.ell(M['gl_b'] if kind == 'cel' else M['teal'], (gx, gy, 1.05 + gr), (gr, gr, gr), (24, 16))
        if kind == 'ter':
            for (a, b, r) in [(0.4, 0.6, 0.14), (-0.5, 0.5, 0.1), (0.1, -0.7, 0.12)]: mb.ell(M['tan'], (gx + gr * 0.9 * math.cos(b) * math.sin(a), gy - gr * 0.9 * math.cos(a) * math.cos(b), 1.05 + gr + gr * 0.9 * math.sin(b)), (r, 0.03, r), (8, 6), rot=(a, 0, 0))
        else:
            for k in range(22):
                a = rr.uniform(0, 6.28); b = rr.uniform(-0.2, 1.2); mb.ell(M['gold'], (gx + gr * 1.0 * math.cos(b) * math.sin(a) * 0.98, gy - gr * 0.98 * math.cos(b) * math.cos(a), 1.05 + gr + gr * math.sin(b) * 0.98), (0.02, 0.02, 0.02), (6, 4))
        ring_xz(mb, M['gold'], (gx, gy, 1.05 + gr), gr * 1.12, 0.03, 0.03, 24); ring_xy(mb, M['gold'], (gx, gy, 1.05 + gr * 0.7), gr * 1.2, 0.03, 0.04, 20)
        mb.rod(M['woodd'], (gx, gy, 1.05), (gx, gy, 0.55), 0.05, 0.07, 8)
        for a in range(3): mb.rod(M['woodd'], (gx, gy, 0.6), (gx + 0.35 * math.cos(a * 2.094 + 0.5), gy + 0.35 * math.sin(a * 2.094 + 0.5), 0.0), 0.04, 0.03, 6)
    # ---- orrery on a round table (left)
    ox_, oy_ = -2.85, 0.9
    mb.cyl(M['woodd'], (ox_, oy_, 0.82), 0.5, 0.06, seg=20); mb.rod(M['wood'], (ox_, oy_, 0.0), (ox_, oy_, 0.8), 0.08, 0.12, 10)
    for a in range(3): mb.rod(M['wood'], (ox_, oy_, 0.2), (ox_ + 0.4 * math.cos(a * 2.094), oy_ + 0.4 * math.sin(a * 2.094), 0.0), 0.04, 0.03, 6)
    mb.ell(M['gold'], (ox_, oy_, 1.2), (0.13, 0.13, 0.13), (14, 10)); mb.rod(M['brass'], (ox_, oy_, 0.84), (ox_, oy_, 1.2), 0.02, 0.02, 6)
    for (r, col, pr, a) in [(0.18, 'redp', 0.04, 0.5), (0.28, 'teal', 0.05, 2.2), (0.38, 'tan', 0.06, 4.0), (0.46, 'navy', 0.05, 5.4)]:
        ring_xy(mb, M['brass'], (ox_, oy_, 1.2), r, 0.012, 0.012, 24); mb.ell(M[col], (ox_ + r * math.cos(a), oy_ + r * math.sin(a), 1.2), (pr, pr, pr), (10, 8))
        mb.rod(M['brass'], (ox_, oy_, 1.2), (ox_ + r * math.cos(a), oy_ + r * math.sin(a), 1.2), 0.006, 0.006, 4)
    # ---- floor candelabra (left-back) and hanging chandelier
    fx, fy = -3.0, 3.7
    mb.cyl(M['gold'], (fx, fy, 0.05), 0.2, 0.1, seg=14); mb.rod(M['gold'], (fx, fy, 0.1), (fx, fy, 1.7), 0.04, 0.025, 8)
    pts = []
    for a in range(7):
        ang = a * 0.898; ex_ = fx + 0.28 * math.cos(ang); ey_ = fy + 0.28 * math.sin(ang) * 0.6
        mb.rod(M['gold'], (fx, fy, 1.55), (ex_, ey_, 1.85), 0.015, 0.015, 6); mb.cyl(M['gold'], (ex_, ey_, 1.86), 0.035, 0.03, seg=8); pts.append((ex_, ey_, 1.875))
    candles(mb, M, fl, pts, 0.2)
    ccx, ccy, ccz = 0.0, 2.4, 4.7
    mb.rod(M['gold'], (ccx, ccy, ZH), (ccx, ccy, ccz + 0.3), 0.015, 0.015, 6); mb.ell(M['gold'], (ccx, ccy, ccz + 0.2), (0.14, 0.14, 0.18), (12, 8))
    ring_xy(mb, M['gold'], (ccx, ccy, ccz), 0.7, 0.05, 0.05, 28); ring_xy(mb, M['gold'], (ccx, ccy, ccz - 0.35), 0.4, 0.04, 0.04, 22)
    pts = []
    for a in range(10):
        ang = a * 0.628; ex_ = ccx + 0.7 * math.cos(ang); ey_ = ccy + 0.7 * math.sin(ang)
        mb.cyl(M['gold'], (ex_, ey_, ccz + 0.04), 0.035, 0.06, seg=8); pts.append((ex_, ey_, ccz + 0.07)); mb.rod(M['gold'], (ccx, ccy, ccz - 0.35), (ex_, ey_, ccz), 0.01, 0.01, 4)
    candles(mb, M, fl, pts, 0.16)
    # ---- bookcase (back-right corner) and a stool-height foreground chair back at the near-right
    for k in range(5):
        mb.box(M['woodd'], (3.28, Y1 - 0.3, 1.2 + 0.45 * k), (0.62, 0.34, 0.04))
    mb.box(M['woodd'], (3.0, Y1 - 0.3, 2.3), (0.04, 0.34, 2.4)); mb.box(M['woodd'], (3.55, Y1 - 0.3, 2.3), (0.04, 0.34, 2.4))
    for k in range(4):
        x = 3.0 + 0.05
        for j in range(8): mb.box(M['book%d' % (1 + (j + k) % 4)], (3.06 + 0.07 * j, Y1 - 0.3, 1.2 + 0.45 * k + 0.2), (0.055, 0.22, 0.3 + 0.05 * ((j * 7 + k) % 3)))
    mb.box(M['seat'], (2.1, -2.15, 0.46), (0.62, 0.6, 0.1)); mb.box(M['wood'], (2.1, -1.88, 0.95), (0.62, 0.07, 0.95)); mb.box(M['seat'], (2.1, -1.92, 1.0), (0.46, 0.04, 0.5))
    for dx in (-0.27, 0.27):
        mb.box(M['wood'], (2.1 + dx, -2.4, 0.22), (0.06, 0.06, 0.44)); mb.box(M['wood'], (2.1 + dx, -1.9, 0.22), (0.06, 0.06, 0.44))
    mb.cyl(M['woodd'], (-2.2, -2.2, 0.35), 0.28, 0.7, seg=14); mb.ell(M['teal'], (-2.2, -2.2, 0.82), (0.26, 0.26, 0.2), (12, 8))     # urn on a plinth (foreground, shade)
    mb.finish(); fl.finish(shadow=False)
    cm = MB('cards')
    if not os.environ.get('NOCARDS'): card(cm, M['grey'], -0.45, 1.5, w=0.55); card(cm, M['grey'], 0.35, 2.0, w=0.55); cm.finish()

PRESETS['hall'] = dict(
    key=(1.0, 0.82, 0.55, 30.0), key_dir=kdir(-22, 38), sun_angle=1.0, exposure=0.1, sat=1.08, samples=100, dbounce=3,
    shaft_k=4.0, shaft_a=0.007,
    cam=dict(loc=(0.0, -3.0, 1.7), look=(0.0, 5.6, 1.9), lens=22))

def lights_hall(P):
    sun_light(P); shafts(P, (-1.0, 1.0, 1.2, 4.0, 5.55))
    area_light('fill', (0, 1.0, 5.9), (0, 0, 0), (6.5, 8.0), (0.26, 0.36, 1.0), 600)
    area_light('fillc', (0.0, -3.3, 2.0), (math.pi / 2, 0, 0), (6.5, 4.0), (0.26, 0.36, 1.0), 260)
    area_light('winfill', (0, 5.5, 2.6), (-math.pi / 2, 0, 0), (2.0, 3.4), (0.3, 0.42, 1.0), 160)
    for (loc, en) in [((0.0, 2.4, 4.8), 120), ((2.0, 2.2, 1.3), 25), ((-3.0, 3.7, 1.95), 40)]: point_light('flamep', loc, (1.0, 0.66, 0.3), en, 0.05)

# ================================================================== render + run
def render(mode, out, samples, draft):
    sc = bpy.context.scene; P = PRESETS[mode]
    sc.render.engine = 'CYCLES'; cy = sc.cycles; cy.device = 'CPU'; cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'
    cy.denoising_input_passes = 'RGB_ALBEDO_NORMAL'; cy.max_bounces = 4; cy.diffuse_bounces = P.get('dbounce', 1); cy.glossy_bounces = P.get('gloss', 1); cy.transmission_bounces = 0; cy.transparent_max_bounces = 6
    cy.use_light_tree = True; cy.filter_width = 1.2; sc.render.threads = 4
    sc.render.resolution_x = W // (2 if draft else 1); sc.render.resolution_y = H // (2 if draft else 1); sc.render.resolution_percentage = 100
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = P.get('exposure', 0.0)
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
    A = _rd(sc, out + '_A.png', samples, True)[..., :3]
    # shade mask for the hue check (not used for grading): sun-only render with a white override, no bounces, sky hidden; cast shadow = sun blocked
    for l in bpy.data.lights:
        if l.name != 'key': l.energy = 0.0
    wbgs = [n for n in bpy.data.worlds['sky'].node_tree.nodes if n.bl_idname == 'ShaderNodeBackground']
    for n in wbgs: n.inputs['Strength'].default_value = 0.0
    for o in bpy.data.objects:
        if o.name.startswith(('clouds', 'glass', 'sun_', 'shafts', 'flame', 'skyobj')): o.hide_render = True
    wm = bpy.data.materials.new('ovr'); wm.use_nodes = True; bs = wm.node_tree.nodes['Principled BSDF']; bs.inputs['Base Color'].default_value = (1, 1, 1, 1)
    bs.inputs['Roughness'].default_value = 1.0; bs.inputs['Specular IOR Level'].default_value = 0.0
    cy.max_bounces = 0; cy.diffuse_bounces = 0; cy.glossy_bounces = 0; bpy.context.view_layer.material_override = wm
    D = _rd(sc, out + '_D.png', 24, False, True)
    bpy.context.view_layer.material_override = None
    lD = 0.3 * D[..., 0] + 0.59 * D[..., 1] + 0.11 * D[..., 2]
    vs = [(o, o.visible_shadow) for o in bpy.data.objects if o.type == 'MESH']
    for o, _ in vs: o.visible_shadow = False
    D2 = _rd(sc, out + '_D2.png', 8, False, True)
    for o, v in vs: o.visible_shadow = v
    lD2 = 0.3 * D2[..., 0] + 0.59 * D2[..., 1] + 0.11 * D2[..., 2]
    cast = (D[..., 3] > 0.99) & (lD < 0.02) & (lD2 > 0.08)
    Image.fromarray((cast * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).save(out + '_shade.png')
    a = grade(A, P)
    Image.fromarray((a * 255 + 0.5).astype(np.uint8)).save(out + '.jpg', quality=93)

NAMES = {'shop': 'sb1_workshop', 'ship': 'sb2_ship', 'hall': 'sb3_hall'}
def run(mode, draft=False):
    t = time.time(); bpy.ops.wm.read_factory_settings(use_empty=True); MATS.clear(); P = PRESETS[mode]
    if mode == 'shop':
        flat_world('#7a82ff', 0.0); build_shop(P); lights_shop(P)
    elif mode == 'ship':
        build_ship(P); lights_ship(P)
    else:
        flat_world('#7a82ff', 0.0); build_hall(P); lights_hall(P)
    setup_camera(P)
    out = os.path.join(HERE, ('d_' if draft else '') + NAMES[mode])
    render(mode, out, 24 if draft else P.get('samples', 100), draft)
    for f in os.listdir(HERE):
        if f.startswith(os.path.basename(out)) and f.endswith(('_A.png', '_D.png', '_D2.png')): os.remove(os.path.join(HERE, f))
    print(mode, 'done %.0fs' % (time.time() - t)); return time.time() - t

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != 'draft']; draft = 'draft' in sys.argv
    for m in (['shop', 'ship', 'hall'] if (not args or args[0] == 'all') else args): run(m, draft)

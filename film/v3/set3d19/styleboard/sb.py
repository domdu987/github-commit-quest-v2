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
            pass   # primitives come out with outward normals; recalc flips faces of intersecting solids (black gear-tooth slivers)
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

def flat_world(col, k, env=('#ffd6a0', 2.2)):
    """interior world: camera/diffuse rays see a flat colour (strength k, 0 = none); glossy rays see a warm room-like environment so brass reads as metal"""
    w = bpy.data.worlds.new('sky'); bpy.context.scene.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputWorld'); b1 = N('ShaderNodeBackground'); b1.inputs['Color'].default_value = hexc(col); b1.inputs['Strength'].default_value = k
    b2 = N('ShaderNodeBackground'); b2.inputs['Color'].default_value = hexc(env[0]); b2.inputs['Strength'].default_value = env[1]
    lp = N('ShaderNodeLightPath'); mx = N('ShaderNodeMixShader'); L(lp.outputs['Is Glossy Ray'], mx.inputs[0]); L(b1.outputs[0], mx.inputs[1]); L(b2.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])

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
    em.inputs['Color'].default_value = hexc('#ffd890'); em.inputs['Strength'].default_value = P.get('shaft_k', 4.0); mx.inputs[0].default_value = P.get('shaft_a', 0.02)
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
    M['floor'] = mat('floor', '#9a7040', '#86602f', scale=2.2, aniso=(0.5, 0.12, 1))
    M['floor2'] = mat('floor2', '#7a5530', '#8a6636', scale=2.2, aniso=(0.5, 0.12, 1))
    M['gap'] = mat('gap', '#2a1a22')
    M['beam'] = mat('beam', '#4e3420', '#684224', scale=2.0, aniso=(0.1, 1, 1))
    M['honey'] = mat('honey', '#c28b3e', '#aa7430', scale=5, aniso=(0.15, 1, 1), contrast=1.3)
    M['oak'] = mat('oak', '#8a5a2c', '#9e6a34', scale=5, aniso=(0.15, 1, 1))
    M['oakd'] = mat('oakd', '#5d3a20', '#72482a', scale=5, aniso=(0.2, 1, 1))
    M['lign'] = mat('lign', '#4a3a24', '#5e4a2c', scale=6)
    M['gearw'] = mat('gearw', '#c9924a', '#b07a38', scale=8, contrast=1.3)
    M['iron'] = metal_mat('iron', '#34323e', '#4a4858', rough=0.6, spec=0.15)
    M['steel'] = mat('steel', '#6a625c', '#7c746c', scale=8)
    M['brass'] = metal_mat('brass', '#cb9f48', '#e6bb5c', rough=0.28, spec=0.9, metallic=0.9)
    M['brassd'] = metal_mat('brassd', '#8a5e20', '#b0802e', rough=0.32, spec=0.8, metallic=0.9)
    M['terra'] = mat('terra', '#b5532c', '#c9683a', scale=4)
    M['cloth'] = mat('cloth', '#a98354', '#bd9560', scale=7)
    M['cream'] = mat('cream', '#e8d6aa', '#f0e0b8', scale=5)
    M['red'] = mat('red', '#8a2630', '#a23238', scale=6)
    M['green'] = mat('green', '#5e7a3a', '#748c44', scale=6)
    M['dark'] = mat('dark', '#1c1424', '#2a1c30', scale=4)
    M['shav'] = mat('shav', '#d9a85a', '#c8924a', scale=8)
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
        gear(mb, M['brass'] if nt != 14 else M['brassd'], (hx + dx, hy - 0.19, hz + dz), r, nt=nt, th=0.035, rim=0.022, tooth=0.026, hub=0.025, n=14)
    mb.rod(M['brassd'], (hx - 0.3, hy - 0.22, hz + 0.3), (hx + 0.3, hy - 0.22, hz + 0.3), 0.007, 0.007, 6)
    # two dumbbell balance bars crossing in an X on top, four brass balls
    zt = hz + hh + 0.22
    for sgn, zz in ((1, zt), (-1, zt + 0.07)):
        a = sgn * math.radians(33); L = 0.42; tipx = L * math.cos(a); tipy = L * math.sin(a)
        mb.rod(M['brassd'], (hx - tipx, hy - tipy, zz), (hx + tipx, hy + tipy, zz), 0.016, 0.016, 8, True, True)
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
    # ---- foreground at the frame edges (dark layer): tool chest with open drawers (left), basket of offcuts (right), sawhorse + plank, stool, leaning clock-case frame
    mb.push(Matrix.Translation((1.05, 0.35, 0)))
    mb.push(Matrix.Translation((-1.85 - 0.25, -0.85, 0)) @ Matrix.Diagonal((0.65, 0.65, 0.65, 1.0)) @ Matrix.Translation((1.85, 0.85, 0)))
    mb.box(M['oakd'], (-1.85, -0.85, 0.3), (0.9, 0.5, 0.6)); mb.box(M['oak'], (-1.85, -0.85, 0.62), (0.94, 0.54, 0.05))
    for k in range(3):
        dz = 0.14 + 0.17 * k; ext = 0.0 if k == 1 else 0.22
        mb.box(M['honey'], (-1.85, -1.12 - ext, dz), (0.78, 0.04 + 0.0, 0.13)); mb.box(M['brass'], (-1.85, -1.14 - ext, dz), (0.12, 0.02, 0.03))
        if ext: mb.box(M['dark'], (-1.85, -1.0 - ext / 2, dz - 0.02), (0.72, ext, 0.05)); mb.box(M['steel'], (-1.95, -1.0 - ext / 2, dz + 0.03), (0.3, 0.04, 0.01), rz=0.4); mb.box(M['honey'], (-1.7, -1.05 - ext / 2, dz + 0.05), (0.1, 0.1, 0.1))
    mb.pop(); mb.pop()
    mb.push(Matrix.Translation((-0.95, 0.45, 0)))
    mb.cyl(M['oakd'], (1.8, -0.9, 0.2), 0.3, 0.4, seg=14, r2=0.34)
    for a in range(9): mb.rod(M['honey'] if a % 2 else M['oak'], (1.8 + 0.18 * math.cos(a * 0.7), -0.9 + 0.18 * math.sin(a * 0.7), 0.35), (1.8 + 0.3 * math.cos(a * 0.7 + 0.4), -0.9 + 0.3 * math.sin(a * 0.7 + 0.4), 0.75 + 0.05 * (a % 3)), 0.03, 0.03, 6)
    mb.pop()
    mb.cyl(M['oakd'], (1.1, -0.45, 0.4), 0.2, 0.06, seg=14)
    for a in (0.3, 2.4, 4.5): mb.rod(M['oak'], (1.1 + 0.16 * math.cos(a), -0.45 + 0.16 * math.sin(a), 0.38), (1.1 + 0.24 * math.cos(a), -0.45 + 0.24 * math.sin(a), 0.0), 0.025, 0.02, 6)
    mb.box(M['honey'], (-1.0, -1.1, 0.03), (0.9, 0.12, 0.05), rz=0.5); mb.box(M['oak'], (-1.35, -0.55, 0.08), (0.7, 0.1, 0.05), rz=-0.35)
    cx_, cy_ = -1.55, 0.6                                                          # leaning half-built clock case (frame of rails and stiles)
    for dx in (-0.2, 0.2): mb.box(M['honey'], (cx_ + dx, cy_, 0.95), (0.07, 0.07, 1.9), ry=0.05)
    for z in (0.15, 0.7, 1.25, 1.8): mb.box(M['honey'], (cx_, cy_, z), (0.46, 0.06, 0.07))
    mb.box(M['oak'], (cx_, cy_ + 0.05, 0.95), (0.4, 0.02, 0.5))
    # shavings: ~200 thin honey ribbons clustered under the bench, lathe and chest
    for k in range(200):
        c = rr.random()
        if c < 0.4: x, y = rr.gauss(1.1, 0.45), rr.gauss(1.8, 0.35)
        elif c < 0.7: x, y = rr.gauss(-1.2, 0.4), rr.gauss(1.7, 0.3)
        elif c < 0.85: x, y = rr.gauss(-1.7, 0.4), rr.gauss(-0.6, 0.25)
        else: x, y = rr.gauss(0.2, 0.9), rr.gauss(0.2, 0.9)
        if abs(x) < 0.5 and 0.2 < y < 2.0: continue
        curl(mb, M['shav'], (x, y, 0.0), rr, rr.uniform(0.35, 0.55))
    # wall shelf of jars, tins and clock parts, hung from the beam above the lathe/window
    for dx in (-0.62, 0.62): mb.rod(M['rope'] if 'rope' in M else M['cloth'], (-1.1 + dx, 2.3, ZH - 0.26), (-1.1 + dx, 2.3, 2.06), 0.012, 0.012, 5)
    mb.box(M['oak'], (-1.1, 2.3, 2.04), (1.4, 0.3, 0.05))
    for (dx, r, h, col) in [(-0.55, 0.06, 0.2, 'terra'), (-0.4, 0.05, 0.14, 'cream'), (-0.22, 0.07, 0.24, 'terra'), (-0.05, 0.05, 0.1, 'green')]:
        mb.cyl(M[col], (-1.1 + dx, 2.3, 2.065 + h / 2), r, h, seg=10)
    mb.box(M['iron'], (-1.1 + 0.18, 2.3, 2.12), (0.14, 0.1, 0.1)); mb.box(M['brass'], (-1.1 + 0.36, 2.3, 2.09), (0.12, 0.12, 0.04)); gear(mb, M['brass'], (-1.1 + 0.52, 2.18, 2.13), 0.07, nt=10, th=0.02, rim=0.015, tooth=0.015, hub=0.015, n=10, rot=(math.pi / 2, 0, 0))
    mb.cyl(M['cream'], (-1.1 + 0.6, 2.3, 2.2), 0.018, 0.14, seg=8)
    fl5 = MB('flame'); fl5.ell(M['flame'], (-1.1 + 0.6, 2.3, 2.3), (0.02, 0.02, 0.045), (8, 6)); fl5.finish(shadow=False)
    # wall lantern on the chest (emitter)
    mb.box(M['iron'], (1.75, 1.4, 0.6), (0.2, 0.2, 0.04)); mb.box(M['iron'], (1.75, 1.4, 0.95), (0.2, 0.2, 0.04))
    for dx, dy in ((-0.08, -0.08), (0.08, -0.08), (-0.08, 0.08), (0.08, 0.08)): mb.box(M['iron'], (1.75 + dx, 1.4 + dy, 0.78), (0.02, 0.02, 0.32))
    fl6 = MB('flame'); fl6.box(M['lampg'], (1.75, 1.4, 0.78), (0.13, 0.13, 0.28)); fl6.finish(shadow=False)
    mb.finish()
    if os.environ.get('NOCARDS'): return
    cm = MB('cards'); card(cm, M['grey'], -1.0, 1.0, w=0.55); card(cm, M['grey'], -0.4, 1.3, w=0.55); cm.finish()

PRESETS = {}
PRESETS['shop'] = dict(
    key=(1.0, 0.8, 0.52, 42.0), key_dir=kdir(-46, 19), sun_angle=1.0, exposure=0.2, sat=1.1, samples=96, dbounce=2,
    cam=dict(loc=(0.05, -2.3, 1.32), look=(0.0, 3.4, 0.95), lens=22), flat_amb=('#3a3cff', 0.0))

def lights_shop(P):
    sun_light(P); shafts(P, (-1.55, -0.3, 0.9, 2.3, 3.38))
    area_light('fill', (0, 0.3, 2.85), (0, 0, 0), (4.4, 5.5), (0.12, 0.22, 1.0), 420)               # blue-violet ambient from above
    area_light('fillc', (0.0, -2.8, 1.5), (math.pi / 2, 0, 0), (4.4, 2.8), (0.2, 0.3, 1.0), 150)    # from behind the camera
    area_light('winfill', (-0.85, 3.5, 1.6), (-math.pi / 2, 0, 0), (1.1, 1.3), (0.3, 0.42, 1.0), 140)
    area_light('roomwarm', (0.3, 1.0, 2.8), (0, 0, 0), (3.5, 4.5), (1.0, 0.7, 0.4), 170)           # warm room light (candle/lamp bounce): shade stays warm
    pts = []
    for (loc, en) in [((0.51, 2.2, 1.3), 30), ((2.05, 2.2, 1.2), 16), ((-0.1, 1.5, 2.3), 20), ((1.75, 1.2, 0.95), 18), ((-1.1 + 0.6, 2.2, 2.35), 12), ((0.3, 1.3, 1.75), 30)]:
        pts.append(point_light('flamep', loc, (1.0, 0.62, 0.26), en, 0.05))

# ================================================================== STILL 2 (v2): Royal Navy 50-gun ship, forecastle view forward-down over the bow
DECK = 6.0; STEM = 46.0          # waist deck z, forecastle deck z, stem y, forecastle starts at YF
def hw(y):
    """deck half-beam at y (m): full beam to y=20, narrowing to the stem at y=46 (floats and arrays)"""
    t = np.clip((np.asarray(y, dtype=np.float64) - 20.0) / (STEM - 20.0), 0.0, 1.0)
    r = 3.7 * np.maximum(0.0, 1 - t ** 2.0) ** 0.85
    return float(r) if np.ndim(r) == 0 else r

def ship_mats():
    M = {}
    M['deck1'] = mat('deck1', '#b48a50', '#a07a40', scale=3, aniso=(0.12, 1, 1), contrast=1.4)
    M['deck2'] = mat('deck2', '#a67c44', '#bc9255', scale=3, aniso=(0.12, 1, 1), contrast=1.4)
    M['seam'] = mat('seam', '#2c1c20')
    M['hullb'] = mat('hullb', '#2a2622', '#36302a', scale=2, aniso=(0.3, 0.3, 1))
    M['ochre'] = mat('ochre', '#cf9230', '#bd7f26', scale=3)
    M['bulw'] = mat('bulw', '#a24c2c', '#8f3f28', scale=3, aniso=(0.2, 1, 1))
    M['cap'] = mat('cap', '#2a2622', '#3a342c', scale=3)
    M['iron'] = mat('iron', '#2a2622', '#38322c', scale=6, rough=0.6)
    M['carr'] = mat('carr', '#8a3e28', '#9c4a30', scale=4, aniso=(0.2, 1, 1))
    M['oak'] = mat('oak', '#8a5a2c', '#9e6a34', scale=5, aniso=(0.15, 1, 1))
    M['mast'] = mat('mast', '#8a5c34', '#a2703c', scale=3, aniso=(0.2, 0.2, 0.05))
    M['rope'] = mat('rope', '#b8924c', '#9a7638', scale=6)
    M['rig'] = mat('rig', '#2a2030', '#3a2e3a', scale=3)
    M['brass'] = metal_mat('brass', '#cb9f48', '#e6bb5c', rough=0.28, spec=0.8, metallic=0.9)
    M['sail'] = mat('sail', '#e6d4a0', '#d8c48c', scale=2.2, contrast=1.1, emit='#ffe2a0', emit_k=0.08)
    M['sail2'] = mat('sail2', '#dac690', '#cbb77c', scale=2.2, contrast=1.1, emit='#ffe2a0', emit_k=0.06)
    M['red'] = mat('red', '#b83a32', '#9c2e2c', scale=4)
    M['grey'] = mat('grey', '#a4a8b8')
    M['isle'] = mat_emit('isle', '#6f9a78', 0.9); M['isle2'] = mat_emit('isle2', '#4f7e68', 0.8); M['beach'] = mat_emit('beach', '#e8dcb8', 1.0)
    M['darksail'] = mat('darksail', '#2c2838')
    M['lamp'] = mat_emit('lamp', '#ffd890', 6.0); M['spray'] = mat('spray', '#eef4f0', '#dbe8e6', scale=2); M['lid'] = mat('lid', '#a07a48', '#8e6a3c', scale=6); M['port'] = mat('port', '#7a2c22', '#8e3828', scale=4)
    return M

def tube(mb, m, p0, p1, r0, r1=None, seg=8): mb.rod(m, p0, p1, r0, r1, seg=seg, caps=True, smooth=True)

def sail_obj(M, name, PF, nx, ny, thick=0.03):
    """smooth, two-sided (solidified) sail mesh from a (i,j)->xyz function; canvas strips alternate between two materials"""
    verts = [PF(i, j) for j in range(ny + 1) for i in range(nx + 1)]
    faces = []; midx = []
    for j in range(ny):
        for i in range(nx):
            a = j * (nx + 1) + i; faces.append((a, a + 1, a + nx + 2, a + nx + 1)); midx.append(i % 2)
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    me.materials.append(M['sail']); me.materials.append(M['sail2'])
    for p, mi in zip(me.polygons, midx): p.use_smooth = True; p.material_index = mi
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    md = ob.modifiers.new('thick', 'SOLIDIFY'); md.thickness = thick; md.offset = 0.0
    return ob

def sail_tri(mb, M, T, C, Hd, bulge, n=8, m=8):
    T = Vector(T); C = Vector(C); Hd = Vector(Hd)
    def PF(i, j):
        v = j / n; L = T + (Hd - T) * v; Rr = C + (Hd - C) * v; u = i / m
        p = L + (Rr - L) * u
        b = bulge * math.sin(math.pi * u) * math.sin(math.pi * min(1, 0.12 + 0.88 * v)) * (1 - 0.5 * v)
        return (p.x + b, p.y + b * 0.4, p.z)
    sail_obj(M, 'sail_jib%d' % int(T.y), PF, m, n)

def sail_quad(mb, M, x0, x1, zb, zt, y, belly, ny=8, nx=12):
    def PF(i, j):
        u = i / nx; v = j / ny
        xl = x0 + (x1 - x0) * u; zz = zb + (zt - zb) * v
        by = belly * math.sin(math.pi * u) * math.sin(math.pi * (0.15 + 0.85 * v)) ** 0.8
        return (xl * (1 + 0.05 * (1 - v)), y + by, zz)
    sail_obj(M, 'sail_%d_%d' % (int(y), int(zb)), PF, nx, ny)

def sky_world2(P):
    """exterior world: camera AND glossy rays see the painted sky gradient (so the sea mirrors a sky, not a flat colour); diffuse rays see the flat blue-violet ambient"""
    w = bpy.data.worlds.new('sky'); bpy.context.scene.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputWorld'); bg = N('ShaderNodeBackground'); tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Generated'], sp.inputs[0])
    cr = N('ShaderNodeValToRGB'); L(sp.outputs['Z'], cr.inputs[0]); stops = P['sky']
    cr.color_ramp.elements[0].position = stops[0][0]; cr.color_ramp.elements[0].color = hexc(stops[0][1])
    for pos, col in stops[1:-1]:
        e = cr.color_ramp.elements.new(pos); e.color = hexc(col)
    cr.color_ramp.elements[-1].position = stops[-1][0]; cr.color_ramp.elements[-1].color = hexc(stops[-1][1])
    bg.inputs['Strength'].default_value = P['sky_k']; L(cr.outputs[0], bg.inputs['Color'])
    lp = N('ShaderNodeLightPath'); b2 = N('ShaderNodeBackground'); b2.inputs['Color'].default_value = hexc(P['amb'][0]); b2.inputs['Strength'].default_value = P['amb'][1]
    ad = N('ShaderNodeMath'); ad.operation = 'ADD'; ad.use_clamp = True; L(lp.outputs['Is Camera Ray'], ad.inputs[0]); L(lp.outputs['Is Glossy Ray'], ad.inputs[1])
    mx = N('ShaderNodeMixShader'); L(ad.outputs[0], mx.inputs[0]); L(b2.outputs[0], mx.inputs[1]); L(bg.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])

def build_ship(P):
    M = ship_mats(); mb = MB('ship'); rr = rnd(5)
    Y0 = -12.0
    def ylim_for(ax):
        if ax >= 3.699: return 20.0
        lo, hi = 20.0, STEM
        for _ in range(30):
            mid = (lo + hi) / 2
            if hw(mid) > ax: lo = mid
            else: hi = mid
        return lo
    # ---- deck planks, hull body (black, ochre wale, flare), gun ports on the hull side, bulwarks with ports, cap rail
    k = 0; x = -3.7 + 0.13
    while x < 3.7:
        yl = ylim_for(abs(x)); mb.box(M['deck1'] if k % 2 else M['deck2'], (x, (Y0 + yl) / 2, DECK - 0.08), (0.255, yl - Y0, 0.16)); x += 0.26; k += 1
    gun_y = [2.0, 6.0, 10.0, 14.0, 18.0, 31.0, 34.5, 38.0]; gun_yp = [3.0, 7.0, 11.0, 15.0, 32.5, 36.0]
    y = Y0
    while y < STEM:
        yc = y + 0.5; b = hw(yc)
        if b > 0.05:
            for s in (-1, 1):
                for (z0, z1, mm) in ((0.0, 2.9, 'hullb'), (2.9, 3.6, 'ochre'), (3.6, 5.75, 'hullb')):
                    t = (0.5 + 0.5 * (1 - ((z0 + z1) / 2) / 5.8)) * 0.9
                    mb.box(M[mm], (s * (b + t / 2), yc, (z0 + z1) / 2), (t, 1.04, z1 - z0))
            mb.box(M['hullb'], (0, yc, 2.9), (2 * b, 1.04, 5.8))
        y += 1.0
    for s, gy in ((1, gun_y), (-1, gun_yp)):
        for g in gy:
            b = hw(g); tt = 0.5 + 0.5 * (1 - 4.5 / 5.8)
            mb.box(M['ochre'], (s * (b + tt + 0.04), g, 4.55), (0.06, 0.78, 0.7)); mb.box(M['port'], (s * (b + tt + 0.08), g, 4.55), (0.06, 0.62, 0.54))
    for s, gy in ((1, gun_y), (-1, gun_yp)):
        y = Y0
        while y < 43.0:
            yc = y + 0.3; b = hw(yc)
            if b > 0.3 and not any(abs(yc - g) < 0.42 for g in gy):
                dy = hw(yc + 0.3) - hw(yc - 0.3); ang = math.atan2(-dy * s, 0.6)
                mb.box(M['hullb'], (s * (b - 0.04), yc, DECK + 0.3), (0.16, 0.66, 0.6), rz=ang); mb.box(M['ochre'], (s * (b - 0.04), yc, DECK + 0.78), (0.17, 0.66, 0.36), rz=ang); mb.box(M['hullb'], (s * (b - 0.04), yc, DECK + 1.02), (0.16, 0.66, 0.12), rz=ang)
            y += 0.6
        y = Y0
        while y < 43.5:
            yc = y + 0.35; b = hw(yc); dy = hw(yc + 0.35) - hw(yc - 0.35)
            if b > 0.2:
                mb.box(M['cap'], (s * (b - 0.02), yc, DECK + 1.14), (0.3, 0.74, 0.1), rz=math.atan2(-dy * s, 0.7)); mb.box(M['cap'], (s * (b + 0.1), yc, DECK + 1.2), (0.06, 0.74, 0.06), rz=math.atan2(-dy * s, 0.7))
                mb.box(M['seam'], (s * (b - 0.02), yc + 0.36, DECK + 1.195), (0.31, 0.02, 0.012), rz=math.atan2(-dy * s, 0.7))
            y += 0.7
    # ---- cannons (black iron on red-brown carriages), muzzles through the ports
    def cannon(side, y):
        b = hw(y); s = side; zc = DECK + 0.62
        xo = s * (b - 0.1); xi = s * (b - 2.0)
        tube(mb, M['iron'], (xi, y, zc), (xo + s * 0.45, y, zc), 0.23, 0.15, 12)
        mb.ell(M['iron'], (xi - s * 0.12, y, zc), (0.17, 0.17, 0.17), (10, 8)); mb.cyl(M['iron'], (xo + s * 0.42, y, zc), 0.19, 0.08, axis='x', seg=12)
        for yy in (-0.3, 0.3): mb.box(M['carr'], ((xi + xo) / 2 - s * 0.05, y + yy, DECK + 0.3), (1.6, 0.14, 0.5))
        mb.box(M['carr'], (xi + s * 0.45, y, DECK + 0.45), (0.14, 0.6, 0.3)); mb.box(M['oak'], (xi - s * 0.55, y, DECK + 0.46), (0.5, 0.5, 0.06))
        for dx in (-0.35, 0.5):
            for yy in (-0.36, 0.36): mb.cyl(M['carr'], (s * (b - 1.0) + s * dx, y + yy, DECK + 0.17), 0.17, 0.1, axis='y', seg=12)
        for yy in (-0.7, 0.7): mb.rod(M['rope'], (xi - s * 0.1, y, zc - 0.1), (s * (b - 0.2), y + yy, DECK + 0.9), 0.03, 0.03, 5)
    for g in gun_y: cannon(1, g)
    for g in gun_yp: cannon(-1, g)
    # ---- deck furniture: barrels with plain lids, coils, capstan, hatch grating, bucket, binnacle at the stern
    for (bx2, by2) in [(-2.4, 0.2), (-2.0, 1.0), (2.2, 4.5)]:
        mb.ell(M['oak'], (bx2, by2, DECK + 0.45), (0.33, 0.33, 0.47), (14, 10)); mb.cyl(M['lid'], (bx2, by2, DECK + 0.9), 0.24, 0.03, seg=14)
        for z in (0.2, 0.7): mb.cyl(M['iron'], (bx2, by2, DECK + z), 0.3, 0.03, seg=14)
    for (cx, cy, r, n) in [(1.6, -0.5, 0.3, 3), (-0.4, 5.0, 0.3, 3), (1.4, 8.6, 0.28, 3)]:
        for l in range(n): ring_xy(mb, M['rope'], (cx, cy, DECK + 0.06 + l * 0.1), r * (1 - 0.06 * l), 0.1, 0.1, 16)
        mb.cyl(M['rope'], (cx, cy, DECK + 0.06 + (n - 1) * 0.05), r * 0.8, 0.1 * n, seg=16)
    mb.cyl(M['oak'], (-1.2, 12.5, DECK + 0.55), 0.42, 1.1, seg=14); mb.cyl(M['cap'], (-1.2, 12.5, DECK + 1.15), 0.5, 0.1, seg=14)
    for a in range(4): mb.rod(M['oak'], (-1.2, 12.5, DECK + 0.9), (-1.2 + 1.0 * math.cos(a * 1.571 + 0.5), 12.5 + 1.0 * math.sin(a * 1.571 + 0.5), DECK + 0.9), 0.05, 0.05, 6)
    for i in range(5): mb.box(M['oak'], (1.0, 15.0 + 0.3 * i, DECK + 0.05), (1.5, 0.07, 0.09)); mb.box(M['oak'], (0.3 + 0.3 * i, 15.6, DECK + 0.06), (0.07, 1.4, 0.09))
    bx, by = 0.9, -2.2
    mb.box(M['oak'], (bx, by, DECK + 0.4), (0.55, 0.5, 0.8)); mb.box(M['cap'], (bx, by, DECK + 0.83), (0.62, 0.56, 0.06))
    mb.cyl(M['brass'], (bx, by, DECK + 0.95), 0.26, 0.2, seg=16, smooth=True); mb.ell(M['brass'], (bx, by, DECK + 1.05), (0.26, 0.26, 0.24), (16, 10)); mb.cyl(M['brass'], (bx, by, DECK + 0.87), 0.29, 0.05, seg=16)
    mb.cyl(M['oak'], (-0.9, 0.8, DECK + 0.17), 0.18, 0.34, seg=12, r2=0.22)
    # ---- masts: main (y=8) and fore (y=28), with courses, topsails, topgallants, shrouds + ratlines, stays; bowsprit + jib
    def mast(my, ht, spans, sails, pins=True):
        mx = 0.0
        tube(mb, M['mast'], (mx, my, DECK), (mx, my, 0.62 * ht), 0.55, 0.3, 12); tube(mb, M['mast'], (mx, my, 0.5 * ht), (mx, my, ht), 0.32, 0.14, 10)
        top = 0.5 * ht - 0.5; mb.box(M['mast'], (mx, my, top), (3.0, 2.2, 0.22))
        mb.cyl(M['oakd'] if 'oakd' in M else M['oak'], (mx, my, DECK + 0.5), 0.8, 0.12, seg=14)
        for a in range(12): mb.rod(M['iron'], (mx + 0.8 * math.cos(a * .5236), my + 0.8 * math.sin(a * .5236), DECK + 0.5), (mx + 0.8 * math.cos(a * .5236), my + 0.8 * math.sin(a * .5236), DECK + 1.3), 0.035, 0.035, 5)
        for (zy, ln, r) in spans: tube(mb, M['mast'], (mx - ln / 2, my, zy), (mx + ln / 2, my, zy), r, r * 0.6, 8)
        for (x0, x1, zb, zt, yy, bl) in sails: sail_quad(mb, M, x0, x1, zb, zt, my + yy, bl)
        for s in (-1, 1):                                                                # shrouds + ratlines
            for kk in range(5):
                yy = my - 1.5 + 0.75 * kk; bx_ = hw(yy) - 0.1
                mb.rod(M['rig'], (mx + s * 0.4, my - 0.6 + 0.28 * kk - 0.6, top), (s * bx_, yy, DECK + 1.15), 0.045, 0.045, 4)
            for j in range(14):
                t = (j + 0.5) / 14
                a = Vector((s * (hw(my - 1.5) - 0.1) * (1 - t) + (mx + s * 0.4) * t, my - 1.5 - 0.6 * t, DECK + 1.15 + (top - DECK - 1.15) * t))
                b = Vector((s * (hw(my + 1.5) - 0.1) * (1 - t) + (mx + s * 0.4) * t, my + 1.5 - 0.6 * t, DECK + 1.15 + (top - DECK - 1.15) * t))
                mb.rod(M['rig'], a, b, 0.028, 0.028, 4)
    mast(8.0, 40.0, [(14.4, 14.0, 0.17), (24.6, 10.4, 0.14), (31.4, 7.2, 0.1)],
         [(-6.5, 6.5, 8.6, 14.2, 0.7, 2.5), (-4.7, 4.7, 15.0, 24.2, 0.8, 2.0), (-3.3, 3.3, 25.0, 31.0, 0.9, 1.5)])
    mast(28.0, 34.0, [(13.6, 12.0, 0.15), (21.4, 9.0, 0.12), (27.0, 6.2, 0.09)],
         [(-5.6, 5.6, 8.6, 13.4, 0.7, 2.2), (-4.1, 4.1, 14.2, 21.0, 0.8, 1.8), (-2.9, 2.9, 21.8, 26.6, 0.9, 1.3)])
    tube(mb, M['rig'], (0, 8.0, 40.0), (0, 28.0, 34.0), 0.05, 0.05, 4); tube(mb, M['rig'], (0, 28.0, 34.0), (0, 60.0, 14.2), 0.05, 0.05, 4); tube(mb, M['rig'], (0, 8.0, 31.0), (0, 28.0, 27.0), 0.04, 0.04, 4)
    tube(mb, M['rig'], (0.2, 7.5, 28.0), (0.2, -4.0, DECK + 1.3), 0.05, 0.05, 4)
    tube(mb, M['mast'], (0, 44.0, 9.4), (0, 62.0, 14.5), 0.2, 0.1, 10)
    sail_tri(mb, M, (0, 60.5, 13.6), (0, 51.0, 11.8), (0, 55.5, 22.0), 1.1); sail_tri(mb, M, (0, 55.0, 12.8), (0, 48.6, 11.0), (0, 50.0, 22.0), 1.0)
    mb.quad(M['red'], [(0.0, 8.0, 40.1), (0.0, 8.0, 39.3), (-0.2, 3.5, 39.2), (-0.2, 3.5, 40.0)]); mb.quad(M['red'], [(-0.2, 3.5, 40.0), (-0.2, 3.5, 39.2), (0.0, 8.0, 39.3), (0.0, 8.0, 40.1)])
    mb.finish()
    # ---- bow wave: a curling white roll pushed away from the stem with a turquoise underside, long thin rolls peeling back along the hull
    sp = MB('spray'); rr2 = rnd(8)
    tq = mat('turq', '#2fa9a4', '#46bdb0', scale=2)
    for side in (-1, 1):
        for k in range(22):
            yy = STEM - 0.3 - k * 0.75; b = hw(yy) + 2.6 + 0.25 * k ** 0.6
            hgt = max(0.22, 2.1 - 0.08 * k); yaw = -side * math.atan2(hw(yy + 0.4) - hw(yy - 0.4), 0.8) * -1.0
            sp.ell(tq, (side * (b + 0.35 + 0.02 * k), yy, 0.15 + hgt * 0.22), (0.5 + 0.02 * k, 0.8, hgt * 0.42), (12, 6), rot=(0, 0, yaw))           # turquoise underside / face
            sp.ell(M['spray'], (side * (b - 0.05), yy, 0.2 + hgt * 0.62), (0.42 + 0.015 * k, 0.78, hgt * 0.4), (12, 6), rot=(0, 0, yaw))                # white curling roll on top
            if k % 2 == 0: sp.ell(M['spray'], (side * (b - 0.35), yy + 0.2, 0.25 + hgt * 0.95), (0.3, 0.5, hgt * 0.22), (10, 6), rot=(0, 0, yaw))       # the lip
    for k in range(9):                                                                  # crescent of white across the stem
        a = math.pi * (k / 8.0); sp.ell(M['spray'], (1.7 * math.cos(a), STEM + 0.6 + 1.2 * math.sin(a), 0.5 + 0.5 * math.sin(a)), (0.6, 0.6, 0.55 + 0.35 * math.sin(a)), (10, 6))
    for k in range(30): sp.ell(M['spray'], (rr2.uniform(-1.6, 1.6), STEM + 0.8 + rr2.uniform(0, 2.0), rr2.uniform(0.7, 2.4)), (0.12, 0.12, 0.14), (6, 4))
    sp.finish(shadow=False)
    # ---- far dressing
    ib = MB('isle'); n = 48; X0i = 780
    for i in range(n):
        x0 = X0i + i * 7.0; x1 = x0 + 7.0
        f = lambda x: 70 * max(0, math.sin(math.pi * (x - X0i) / (n * 7.0))) ** 0.6 * (0.8 + 0.2 * math.sin((x - X0i) / 11.0)) + 6
        ib.quad(M['isle'] if i % 3 else M['isle2'], [(x0, 1800, 0), (x1, 1800, 0), (x1, 1800, f(x1)), (x0, 1800, f(x0))]); ib.quad(M['beach'], [(x0, 1799, -0.5), (x1, 1799, -0.5), (x1, 1799, 3.5), (x0, 1799, 3.5)])
    ib.finish(shadow=False)
    sb_ = MB('farsail'); sb_.quad(M['darksail'], [(-330, 1500, 0.5), (-304, 1500, 0.5), (-312, 1500, 24), (-326, 1500, 28)]); sb_.quad(M['darksail'], [(-335, 1500, 0.5), (-305, 1500, 0.5), (-305, 1500, 3), (-335, 1500, 3)]); sb_.finish(shadow=False)
    cm = MB('cards')
    if not os.environ.get('NOCARDS'): card(cm, M['grey'], 1.0, 34.0, w=0.55, z0=DECK); card(cm, M['grey'], 1.8, 35.4, w=0.55, z0=DECK); cm.finish()
    if not os.environ.get('NOSEA'): build_sea(P)
    clouds(P)

# ---------------------------------------------------------------- the sea (v3): film-10 technique. Graded smooth grid (one vertex per ~3 px), 3 long swells + short chop fading with distance,
# whitecap flecks on crests, teal near / deep navy far (view distance), Fresnel sky lift, sharp glitter lobe from a glossy-only virtual sun, wake/bow foam as vertex attribute.
def build_sea(P):
    c = P['cam']; loc = np.array(c['loc'], dtype=np.float64); look = np.array(c['look'], dtype=np.float64)
    f = look - loc; f /= np.linalg.norm(f); r = np.cross(f, [0, 0, 1.0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    hx, hy = 0.4602 * 1.15, 0.8182
    zfar = loc[2] / 7000.0
    vmax = (-zfar - f[2]) / (u[2] * hy); vmin = -1.3
    NU, NV = 420, 760
    uu = np.linspace(-1.15, 1.15, NU); vv = vmin + (vmax - vmin) * np.linspace(0, 1, NV)
    UU, VV = np.meshgrid(uu, vv)
    ray = f[None, None, :] + r[None, None, :] * (UU * hx)[..., None] + u[None, None, :] * (VV * hy)[..., None]
    t = -loc[2] / ray[..., 2]; px = loc[0] + ray[..., 0] * t; py = loc[1] + ray[..., 1] * t
    rng = np.random.RandomState(3)
    fpx = t * (2 * hx / 720.0) * 1.1
    h = np.zeros_like(px)
    swells = [(52, 0.85, 80), (31, 0.55, 112), (19, 0.34, 70)]
    chop = [(7.4, .10), (4.8, .06), (3.1, .04), (2.0, .026), (1.3, .016)]
    for (L, A, deg) in swells:
        a = math.radians(deg + rng.uniform(-8, 8)); k = 2 * math.pi / L; th = k * (math.cos(a) * px + math.sin(a) * py) + rng.uniform(0, 6.28)
        q = 0.5 + 0.5 * np.sin(th); h += A * (2 * q ** 1.5 - 1.0)
    for (L, A) in chop:
        a = math.radians(80 + rng.uniform(-50, 50)); k = 2 * math.pi / L; th = k * (math.cos(a) * px + math.sin(a) * py) + rng.uniform(0, 6.28)
        fade = np.clip((L / np.maximum(fpx, 1e-6) - 4.0) / 7.0, 0, 1) * np.clip(1 - t / 260.0, 0, 1)
        h += A * np.sin(th) * fade
    h *= np.clip(1 - t / 3500.0, 0, 1) ** 0.5
    # foam attribute: wash along the outboard hull, bow foam (broken up by the shader noise)
    hh_ = hw(np.clip(py, -12, STEM)); d_hull = np.abs(px) - (hh_ + 0.95); d_hull = np.where((py > -12) & (py < STEM + 1), d_hull, 9)
    dh = np.maximum(d_hull, 0.0); dback = np.maximum(STEM - py, 0.0)
    inhull = (py > -12) & (py < STEM + 1.0)
    uu_ = py / 2.4; vv_ = dh / 0.8                                   # patch coordinates: 3 m along the hull per 1 m across -> ~3:1 patches
    nzp = 0.5 + 0.22 * np.sin(1.7 * uu_ + 0.9 * np.sin(1.3 * vv_ + 0.4 * uu_)) + 0.2 * np.sin(2.3 * vv_ + 1.2 * np.sin(0.8 * uu_ + 1.7)) + 0.12 * np.sin(3.1 * uu_ - 2.2 * vv_ + 0.7)
    bands = np.zeros_like(px)
    for (off, w, amp, flen) in ((3.2, 1.6, 1.0, 90.0), (7.6, 2.2, 0.9, 90.0), (12.6, 2.8, 0.8, 90.0)):
        env = np.clip(1 - np.abs(dh - off - 0.3 * dback * (0.4 + off / 12.0) - 0.5 * np.sin(py * 0.17 + off)) / w, 0, 1); env = env * env * (3 - 2 * env)
        thr = 0.5 - 0.3 * env                                            # centre of the band is the most foamy
        patch = np.clip((nzp - thr) / 0.12, 0, 1)
        bands = np.maximum(bands, patch * env * amp * np.clip(1.05 - dback / flen, 0, 1))
    bands *= inhull * np.clip((STEM + 1.0 - py) / 7.0, 0, 1)
    bow = np.exp(-(((px - 0.0) / 3.2) ** 2 + ((py - (STEM + 2.0)) / 4.2) ** 2)) * 0.9
    foam = np.nan_to_num(np.clip(np.maximum(bands * 0.95, bow), 0, 1))
    verts = np.stack([px, py, h], -1).reshape(-1, 3).astype(np.float32)
    idx = np.arange(NU * NV).reshape(NV, NU)
    a_ = idx[:-1, :-1]; b_ = idx[:-1, 1:]; c_ = idx[1:, 1:]; d_ = idx[1:, :-1]
    alt = ((np.arange(NU - 1)[None, :] + np.arange(NV - 1)[:, None]) % 2).astype(bool)
    t1 = np.where(alt[..., None], np.stack([a_, b_, c_], -1), np.stack([a_, b_, d_], -1)); t2 = np.where(alt[..., None], np.stack([a_, c_, d_], -1), np.stack([b_, c_, d_], -1))
    tris = np.concatenate([t1.reshape(-1, 3), t2.reshape(-1, 3)])
    me = bpy.data.meshes.new('sea'); me.vertices.add(len(verts)); me.vertices.foreach_set('co', verts.ravel())
    nt_ = len(tris); me.loops.add(nt_ * 3); me.polygons.add(nt_)
    me.loops.foreach_set('vertex_index', tris.ravel().astype(np.int32)); me.polygons.foreach_set('loop_start', (np.arange(nt_) * 3).astype(np.int32)); me.polygons.foreach_set('loop_total', np.full(nt_, 3, dtype=np.int32))
    me.update(calc_edges=True); me.polygons.foreach_set('use_smooth', np.ones(nt_, dtype=bool))
    at = me.attributes.new('foam', 'FLOAT', 'POINT'); at.data.foreach_set('value', foam.reshape(-1).astype(np.float32))
    ob = bpy.data.objects.new('sea', me); bpy.context.scene.collection.objects.link(ob)
    m = bpy.data.materials.new('sea'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled')
    bs.inputs['Roughness'].default_value = 0.1; bs.inputs['IOR'].default_value = 1.33; bs.inputs['Specular IOR Level'].default_value = 0.5
    cdv = N('ShaderNodeCameraData'); msp = N('ShaderNodeMapRange'); msp.inputs['From Min'].default_value = 20.0; msp.inputs['From Max'].default_value = 120.0; msp.inputs['To Min'].default_value = 0.22; msp.inputs['To Max'].default_value = 0.5; L(cdv.outputs['View Distance'], msp.inputs['Value']); L(msp.outputs['Result'], bs.inputs['Specular IOR Level'])
    def mixc(a, b, fac):
        mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'
        if hasattr(a, 'node'): L(a, mx.inputs[6])
        else: mx.inputs[6].default_value = a
        if hasattr(b, 'node'): L(b, mx.inputs[7])
        else: mx.inputs[7].default_value = b
        L(fac, mx.inputs[0]); return mx.outputs[2]
    cd = N('ShaderNodeCameraData'); mr = N('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = 22.0; mr.inputs['From Max'].default_value = 220.0; L(cd.outputs['View Distance'], mr.inputs['Value'])
    col = mixc(hexc(P['sea_near']), hexc(P['sea_far']), mr.outputs['Result'])
    gp = N('ShaderNodeNewGeometry'); spz = N('ShaderNodeSeparateXYZ'); L(gp.outputs['Position'], spz.inputs[0])
    cr = N('ShaderNodeMapRange'); cr.inputs['From Min'].default_value = 0.55; cr.inputs['From Max'].default_value = 0.9; L(spz.outputs['Z'], cr.inputs['Value'])
    tcw = N('ShaderNodeTexCoord'); mpw = N('ShaderNodeMapping'); mpw.inputs['Scale'].default_value = (1.1, 0.7, 1.0); L(tcw.outputs['Object'], mpw.inputs['Vector'])
    nzw = N('ShaderNodeTexNoise'); nzw.inputs['Scale'].default_value = 1.0; nzw.inputs['Detail'].default_value = 2.0; L(mpw.outputs[0], nzw.inputs['Vector'])
    sp2 = N('ShaderNodeMapRange'); sp2.inputs['From Min'].default_value = 0.52; sp2.inputs['From Max'].default_value = 0.64; L(nzw.outputs['Fac'], sp2.inputs['Value'])
    wc = N('ShaderNodeMath'); wc.operation = 'MULTIPLY'; wc.use_clamp = True; L(cr.outputs['Result'], wc.inputs[0]); L(sp2.outputs['Result'], wc.inputs[1])
    col = mixc(col, hexc('#e4eeec'), wc.outputs[0])
    fa = N('ShaderNodeAttribute'); fa.attribute_type = 'GEOMETRY'; fa.attribute_name = 'foam'
    nz2 = N('ShaderNodeTexNoise'); nz2.inputs['Scale'].default_value = 1.6; nz2.inputs['Detail'].default_value = 1.0; mp2 = N('ShaderNodeMapping'); mp2.inputs['Scale'].default_value = (2.4, 2.4, 1.0); L(tcw.outputs['Object'], mp2.inputs['Vector']); L(mp2.outputs[0], nz2.inputs['Vector'])
    br = N('ShaderNodeMapRange'); br.inputs['From Min'].default_value = -2.0; br.inputs['From Max'].default_value = -1.0; L(nz2.outputs['Fac'], br.inputs['Value'])
    fm = N('ShaderNodeMath'); fm.operation = 'MULTIPLY'; fm.use_clamp = True; L(fa.outputs['Fac'], fm.inputs[0]); L(br.outputs['Result'], fm.inputs[1])
    fm2 = N('ShaderNodeMath'); fm2.operation = 'MULTIPLY'; fm2.use_clamp = True; fm2.inputs[1].default_value = 1.25; L(fm.outputs[0], fm2.inputs[0])
    col = mixc(col, hexc('#f0f6f2'), fm2.outputs[0])
    L(col, bs.inputs['Base Color'])
    lw = N('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.3
    mrn = N('ShaderNodeMapRange'); mrn.inputs['From Min'].default_value = 20.0; mrn.inputs['From Max'].default_value = 120.0; mrn.inputs['To Min'].default_value = 0.12; mrn.inputs['To Max'].default_value = 1.0; L(cd.outputs['View Distance'], mrn.inputs['Value'])
    fk = N('ShaderNodeMath'); fk.operation = 'MULTIPLY'; fk.inputs[1].default_value = P.get('fresnel_k', 0.7); L(mrn.outputs['Result'], fk.inputs[0])
    em = N('ShaderNodeMath'); em.operation = 'MULTIPLY'; L(lw.outputs['Fresnel'], em.inputs[0]); L(fk.outputs[0], em.inputs[1])
    bs.inputs['Emission Color'].default_value = hexc('#9fc2d8'); L(em.outputs[0], bs.inputs['Emission Strength'])
    nzb = N('ShaderNodeTexNoise'); nzb.inputs['Scale'].default_value = 1.8; nzb.inputs['Detail'].default_value = 0.0; L(tcw.outputs['Object'], nzb.inputs['Vector'])
    bp = N('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.2; bp.inputs['Distance'].default_value = 0.2; L(nzb.outputs['Fac'], bp.inputs['Height']); L(bp.outputs['Normal'], bs.inputs['Normal'])
    L(bs.outputs[0], out.inputs['Surface']); ob.data.materials.append(m)
    # glossy-only virtual sun (light-linked to the sea): the sharp glitter lobe lands under it, ahead-left of the camera
    coll = bpy.data.collections.new('seacoll'); bpy.context.scene.collection.children.link(coll); coll.objects.link(ob)
    kd = Vector(kdir(P['glit_az'], P['glit_el'])).normalized(); d = bpy.data.lights.new('glint', 'SUN'); d.color = (1.0, 0.86, 0.62); d.energy = P.get('glit_k', 14.0); d.angle = math.radians(0.6)
    o = bpy.data.objects.new('glint', d); bpy.context.scene.collection.objects.link(o); o.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler()
    o.visible_diffuse = False; o.light_linking.receiver_collection = coll

PRESETS['ship'] = dict(
    sky=[(0.0, '#6c9ce0'), (0.46, '#a9c6e6'), (0.5, '#a4c4e6'), (0.58, '#7ea8e2'), (0.78, '#4f7ed0'), (1.0, '#3a64be')], sky_k=1.0,
    key=(1.0, 0.92, 0.78, 6.5), key_dir=kdir(140, 48), sun_angle=0.9, exposure=0.1, sat=1.08, amb=('#3050FF', 1.7), samples=80, dbounce=1, gloss=2,
    cloud=('#ffffff', '#8c9ce8'), cloud_diffuse=True, cloud_z=(70, 170), ncloud=8, cloud_seed=4, cloud_scale=0.8,
    sea_near='#0a4a58', sea_far='#0a2c4c', fresnel_k=0.7,
    glit_az=6, glit_el=11, glit_k=30.0,
    cam=dict(loc=(2.4, 33.5, 8.9), look=(2.4 + 9.7, 33.5 + 38.8, 8.9 - 6.3), lens=22))

def lights_ship(P):
    sun_light(P); w = sky_world2(P)
# ================================================================== v6: HERO SHIP seen from the sea (low camera, three-quarter view, bow wave sheet, lacy wake, smooth cumulus)
import numpy as _np
YS, YB = -21.0, 21.0; BH = 5.6                       # stern / bow at the waterline (local y), max half beam
def ss(a, b, x):
    t = np.clip((np.asarray(x, dtype=np.float64) - a) / (b - a), 0.0, 1.0); return t * t * (3 - 2 * t)
def w_wl(t):
    t = np.asarray(t, dtype=np.float64)
    bow = BH * np.maximum(0.0, 1 - np.maximum(0.0, (t - 0.5) / 0.5) ** 2.3) ** 0.9
    ster = BH * (1 - 0.42 * np.maximum(0.0, (0.5 - t) / 0.5) ** 2)
    return np.where(t > 0.5, bow, ster)
def ztop(t):
    t = np.asarray(t, dtype=np.float64)
    return 6.2 + 2.3 * ss(0.30, 0.20, t) + 0.9 * ss(0.82, 0.92, t) + 0.5 * (2 * t - 1) ** 2
def hull_y(t, z):
    zc = np.clip(z, 0, None) / 7.0; a = YS - 1.6 * zc; b = YB + 3.2 * zc; return a + np.asarray(t) * (b - a)
def hull_t(y, z):
    zc = np.clip(z, 0, None) / 7.0; a = YS - 1.6 * zc; b = YB + 3.2 * zc; return (np.asarray(y) - a) / (b - a)
def hull_x(t, z):
    t = np.asarray(t, dtype=np.float64); z = np.asarray(z, dtype=np.float64); zp = np.clip(z, 0, None)
    flare = 0.32 * ss(0.5, 1.0, t); tumble = 0.16 * (1 - ss(0.5, 1.0, t)) + 0.06
    up = 1 + flare * zp / 6.0 - tumble * (zp / 7.0) ** 2
    dn = np.sqrt(np.clip(1 - (np.clip(-z, 0, None) / 2.45) ** 2, 0.0, 1.0))
    return w_wl(t) * np.where(z >= 0, up, dn)
def deck_z(y): return float(ztop(np.clip((y - YS) / (YB - YS), 0, 1))) - 0.95

def vnoise2(x, y, seed=1):
    G = np.random.RandomState(seed).rand(64, 64).astype(np.float32)
    x = np.asarray(x, dtype=np.float32); y = np.asarray(y, dtype=np.float32)
    xi = np.floor(x).astype(np.int32); yi = np.floor(y).astype(np.int32); fx = x - xi; fy = y - yi
    fx = fx * fx * (3 - 2 * fx); fy = fy * fy * (3 - 2 * fy)
    a = G[xi & 63, yi & 63]; b = G[(xi + 1) & 63, yi & 63]; c = G[xi & 63, (yi + 1) & 63]; d = G[(xi + 1) & 63, (yi + 1) & 63]
    return a * (1 - fx) * (1 - fy) + b * fx * (1 - fy) + c * (1 - fx) * fy + d * fx * fy
def fbm2(x, y, seed=1, octs=3):
    s = 0.0; a = 1.0; tot = 0.0; f = 1.0
    for i in range(octs):
        s = s + a * vnoise2(x * f + 17.0 * i, y * f + 31.0 * i, seed + i); tot += a; a *= 0.5; f *= 2.03
    return s / tot

def mesh_obj(name, verts, faces, mats, midx=None, smooth=True):
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in verts], [], [tuple(f) for f in faces]); me.update()
    for m in mats: me.materials.append(m)
    for i, p in enumerate(me.polygons):
        p.use_smooth = smooth
        if midx is not None: p.material_index = int(midx[i])
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); return ob

def S6(): return SHIP6
def loc2w(p):
    s = SHIP6; ph = math.radians(180.0 - s['theta']); x, y, z = p
    return Vector((s['cx'] + x * math.cos(ph) - y * math.sin(ph), s['cy'] + x * math.sin(ph) + y * math.cos(ph), z))
SHIP6 = dict(cx=4.5, cy=67.0, theta=36.0)

def ship6_mats():
    M = ship_mats()
    M['hull6'] = mat('hull6', '#2c2824', '#3a342d', scale=2.5, aniso=(0.25, 0.25, 4.5), contrast=1.2)
    M['ochre6'] = mat('ochre6', '#d89a34', '#c4832a', scale=3, aniso=(0.3, 0.3, 2.0))
    M['cap6'] = mat('cap6', '#2e2824', '#403830', scale=3)
    M['port6'] = mat('port6', '#241410', '#3a1c16', scale=3)
    M['deck6'] = mat('deck6', '#b48a50', '#a07a40', scale=3, aniso=(0.12, 1, 1), contrast=1.4)
    M['canv'] = mat('canv', '#e8dcc0', '#dccfae', scale=2.2, aniso=(1.3, 1, 0.8), contrast=0.8, emit='#ffe2a0', emit_k=0.10)
    M['canv2'] = mat('canv2', '#e2d5b4', '#d6c8a4', scale=2.2, aniso=(1.3, 1, 0.8), contrast=0.8, emit='#ffe2a0', emit_k=0.08)
    M['gold'] = mat('gold', '#d8a840', '#c08c30', scale=4, sheen=0.3)
    M['pen'] = mat('pen', '#c0392f', '#a8302a', scale=4)
    M['rig6'] = mat('rig6', '#2c2430', '#40343e', scale=3)
    return M

def build_hull6(M):
    nt = 130; T = np.linspace(0.0, 1.0, nt)
    base = [-2.35, -1.6, -0.9, -0.35, 0.0, 0.5, 1.2, 2.0, 3.1, 3.6, 4.4, 5.3, 5.7]
    zt = ztop(T)
    Z = np.zeros((nt, len(base) + 3))
    Z[:, :len(base)] = np.array(base)[None, :]; Z[:, len(base)] = 5.7 + (zt - 5.7) * 0.5; Z[:, len(base) + 1] = zt; Z[:, len(base) + 2] = zt + 0.16
    Kc = Z.shape[1]; Tm = T[:, None] * np.ones((1, Kc))
    X = hull_x(Tm, Z); Y = hull_y(Tm, Z)
    X[:, -1] = hull_x(T, zt) + 0.12; Y[:, -1] = hull_y(T, zt) + 0.0; Y[:, -2] = hull_y(T, zt)
    verts = []; faces = []; midx = []
    for s in (-1, 1):
        for i in range(nt):
            for j in range(Kc): verts.append((s * X[i, j], Y[i, j], Z[i, j]))
    ctr = np.array([0, 0, 2.5])
    for si, s in enumerate((-1, 1)):
        off = si * nt * Kc
        for i in range(nt - 1):
            for j in range(Kc - 1):
                a = off + i * Kc + j; b = off + (i + 1) * Kc + j; c = off + (i + 1) * Kc + j + 1; d = off + i * Kc + j + 1
                zm = 0.5 * (Z[i, j] + Z[i, j + 1])
                if j == Kc - 2: mi = 2
                elif (3.1 <= zm <= 3.6) or (5.3 <= zm <= 5.7): mi = 1
                else: mi = 0
                if s == 1: faces.append((a, b, c, d))
                else: faces.append((d, c, b, a))
                midx.append(mi)
    # transom (stern) and flat keel closure
    off0 = 0; off1 = nt * Kc
    for j in range(Kc - 1):
        faces.append((off0 + j, off1 + j, off1 + j + 1, off0 + j + 1)); midx.append(1 if j == Kc - 2 else 0)
    ob = mesh_obj('ship6_hull', verts, faces, [M['hull6'], M['ochre6'], M['cap6']], midx, True)
    # deck fill (barely visible from the low camera, closes the hull for shadows)
    dv = []; df = []
    for i in range(nt):
        zd = zt[i] - 0.95; bd = hull_x(T[i], zd) * 0.97; yd = hull_y(T[i], zd)
        for xx in (-1.0, -0.33, 0.33, 1.0): dv.append((xx * bd, yd, zd))
    for i in range(nt - 1):
        for c in range(3): a = i * 4 + c; df.append((a, a + 1, a + 5, a + 4))
    mesh_obj('ship6_deck', dv, df, [M['deck6']], None, False)
    # gun ports (two rows) as flat frames on the hull side, ochre frame + dark port
    mb = MB('ship6_ports')
    def pquad(m, y0, y1, z0, z1, s, off):
        pts = []
        for (yy, zz) in ((y0, z0), (y1, z0), (y1, z1), (y0, z1)):
            t = float(hull_t(yy, zz)); pts.append((s * (float(hull_x(t, zz)) + off), yy, zz))
        mb.quad(m, pts)
    for zc in (2.55, 4.45):
        y = -15.2
        while y < 16.0:
            for s in (-1, 1):
                pquad(M['ochre6'], y - 0.58, y + 0.58, zc - 0.50, zc + 0.46, s, 0.03)
                pquad(M['port6'], y - 0.44, y + 0.44, zc - 0.38, zc + 0.34, s, 0.06)
            y += 2.4
    mb.finish()
    return ob

def sq_sail(M, name, my, zb, zt_, hw_top, hw_foot, belly, nx=22, ny=16, yoff=0.55):
    def PF(i, j):
        u = 2.0 * i / nx - 1.0; v = j / ny
        hwv = hw_foot + (hw_top - hw_foot) * v
        by = belly * (1 - abs(u) ** 2.3) ** 0.8 * math.sin(math.pi * (0.07 + 0.86 * v)) ** 0.85 * (1 + 0.05 * math.sin(u * 8.0 + v * 3.0))
        z = zb + (zt_ - zb) * v + 0.05 * (zt_ - zb) * (1 - u * u) * (1 - v) ** 2
        return (u * hwv, my + yoff + by, z)
    return sail_obj(M, name, PF, nx, ny, 0.04)

def spanker(M, name, my, z0, H):
    A = Vector((0, my - 0.7, z0 + 0.52 * H)); B = Vector((0, my - 8.6, z0 + 0.60 * H)); C = Vector((0, my - 11.8, z0 + 0.09 * H)); D = Vector((0, my - 0.7, z0 + 0.09 * H))
    nx, ny = 14, 12
    def PF(i, j):
        u = i / nx; v = j / ny
        P = (D * (1 - u) + C * u) * (1 - v) + (A * (1 - u) + B * u) * v
        b = -1.6 * math.sin(math.pi * u) ** 0.8 * math.sin(math.pi * (0.1 + 0.8 * v))
        return (P.x + b, P.y, P.z)
    return sail_obj(M, name, PF, nx, ny, 0.04)

def jib(M, name, T, C, Hd, bulge, n=10, m=10):
    T = Vector(T); C = Vector(C); Hd = Vector(Hd)
    def PF(i, j):
        v = j / n; L = T + (Hd - T) * v; Rr = C + (Hd - C) * v; u = i / m; p = L + (Rr - L) * u
        b = -bulge * math.sin(math.pi * u) * math.sin(math.pi * min(1, 0.1 + 0.9 * v)) * (1 - 0.4 * v)
        return (p.x + b, p.y, p.z)
    return sail_obj(M, name, PF, m, n, 0.04)

def rigging6(mb, M, my, z0, H, s_sides=(-1, 1), nshr=5):
    top = z0 + 0.41 * H
    for s in s_sides:
        for k in range(nshr):
            yy = my - 1.8 + 0.9 * k; tt = float(hull_t(yy, 4.4)); bx = s * (float(hull_x(tt, 4.4)) + 0.35)
            a = Vector((bx, yy, deck_z(yy) - 0.7)); b = Vector((s * 1.0, my - 0.7 + 0.35 * k, top))
            mb.rod(M['rig6'], a, b, 0.05, 0.04, 4)
        for q in np.linspace(0.08, 0.92, 15):
            for k in range(nshr - 1):
                def pt(kk):
                    yy = my - 1.8 + 0.9 * kk; tt = float(hull_t(yy, 4.4)); bx = s * (float(hull_x(tt, 4.4)) + 0.35)
                    a = Vector((bx, yy, deck_z(yy) - 0.7)); b = Vector((s * 1.0, my - 0.7 + 0.35 * kk, top)); return a + (b - a) * q
                mb.rod(M['rig6'], pt(k), pt(k + 1), 0.026, 0.026, 4)
        for k in range(3):           # topmast shrouds
            mb.rod(M['rig6'], Vector((s * 0.9, my - 0.6 + 0.4 * k, top + 0.2)), Vector((s * 0.12, my - 0.3, z0 + 0.77 * H)), 0.035, 0.03, 4)
        mb.rod(M['rig6'], Vector((s * 0.2, my - 0.4, z0 + 0.77 * H)), Vector((s * (float(hull_x(float(hull_t(my - 7.0, 4.4)), 4.4)) + 0.4), my - 7.0, deck_z(my - 7.0) - 0.6)), 0.04, 0.035, 4)    # backstay

def mast6(mb, M, my, H, yards):
    z0 = deck_z(my)
    tube(mb, M['mast'], (0, my, z0 - 0.5), (0, my, z0 + 0.52 * H), 0.58, 0.36, 12)
    tube(mb, M['mast'], (0, my, z0 + 0.40 * H), (0, my, z0 + 0.80 * H), 0.30, 0.19, 10)
    tube(mb, M['mast'], (0, my, z0 + 0.76 * H), (0, my, z0 + H), 0.17, 0.08, 8)
    mb.box(M['mast'], (0, my - 0.2, z0 + 0.41 * H), (3.2, 2.6, 0.22)); mb.box(M['rig6'], (0, my - 0.2, z0 + 0.41 * H - 0.13), (3.3, 2.7, 0.04))
    for (fz, ln, r) in yards:
        zy = z0 + fz * H; tube(mb, M['mast'], (-ln / 2, my, zy), (ln / 2, my, zy), r, r * 0.55, 8)
        for s in (-1, 1): mb.rod(M['rig6'], (s * ln / 2, my, zy), (s * 0.4, my, zy + 0.18 * H * (0.8 if fz < 0.6 else 0.55)), 0.025, 0.025, 4)
    # pennant at the truck
    mb.quad(M['pen'], [(0, my, z0 + H), (0.0, my - 5.5, z0 + H - 0.2), (0.0, my - 5.2, z0 + H - 0.75), (0, my, z0 + H - 0.5)])
    mb.quad(M['pen'], [(0, my, z0 + H - 0.5), (0.0, my - 5.2, z0 + H - 0.75), (0.0, my - 5.5, z0 + H - 0.2), (0, my, z0 + H)])
    rigging6(mb, M, my, z0, H)

def build_ship6(P):
    before = set(bpy.data.objects)
    M = ship6_mats(); mb = MB('ship6'); sc = bpy.context.scene
    build_hull6(M)
    # quarter gallery + stern lantern + beakhead + figurehead
    for s in (-1, 1):
        mb.box(M['ochre6'], (s * 4.3, -16.6, 7.9), (1.4, 4.0, 3.2)); mb.box(M['hull6'], (s * 4.3, -16.6, 9.62), (1.5, 4.1, 0.2))
        for k in range(3): mb.box(M['port6'], (s * 5.04, -18.0 + 1.4 * k, 8.0), (0.06, 0.8, 1.2))
    mb.box(M['gold'], (0, -21.2, 10.2), (1.2, 1.2, 1.8)); mb.cyl(M['gold'], (0, -21.2, 11.3), 0.5, 0.5, seg=10)
    tube(mb, M['gold'], (0, YB + 2.2, 4.6), (0, YB + 4.8, 5.8), 0.36, 0.22, 8); mb.ell(M['gold'], (0, YB + 5.0, 5.9), (0.3, 0.55, 0.38), (10, 6))
    for s in (-1, 1): tube(mb, M['ochre6'], (s * 0.15, YB + 1.0, 4.9), (s * 0.5, YB + 4.8, 5.4), 0.1, 0.07, 6)
    # three masts: fore, main, mizzen
    mast6(mb, M, 11.5, 36.0, [(0.27, 15.5, 0.20), (0.55, 12.2, 0.16), (0.77, 8.8, 0.12), (0.91, 5.8, 0.09)])
    mast6(mb, M, -0.5, 40.0, [(0.27, 17.8, 0.22), (0.55, 13.6, 0.17), (0.77, 9.8, 0.13), (0.91, 6.4, 0.09)])
    mast6(mb, M, -12.5, 29.0, [(0.27, 12.5, 0.17), (0.52, 10.0, 0.13), (0.74, 7.2, 0.10)])
    # square sails (head on the yard, foot above the deck), billowing forward
    for (nm, my, H, spec) in (('fore', 11.5, 36.0, [(0.27, 0.07, 7.2, 8.0, 2.0), (0.55, 0.31, 5.6, 6.4, 1.7), (0.77, 0.58, 4.0, 4.5, 1.2), (0.91, 0.80, 2.6, 3.0, 0.7)]),
                              ('main', -0.5, 40.0, [(0.27, 0.07, 8.0, 8.9, 2.3), (0.55, 0.31, 6.2, 7.0, 1.9), (0.77, 0.58, 4.4, 4.9, 1.3), (0.91, 0.80, 2.8, 3.2, 0.8)]),
                              ('miz', -12.5, 29.0, [(0.52, 0.30, 4.8, 5.4, 1.4), (0.74, 0.55, 3.4, 3.8, 1.0)])):
        z0 = deck_z(my)
        for k, (fy, ff, hwt, hwf, bel) in enumerate(spec): sq_sail(M, 'ship6_sail_%s%d' % (nm, k), my, z0 + ff * H, z0 + fy * H, hwt, hwf, bel)
    spanker(M, 'ship6_spanker', -12.5, deck_z(-12.5), 29.0)
    # bowsprit, jib boom, spritsail yard, stays, jibs
    tube(mb, M['mast'], (0, YB - 4.0, 5.2), (0, YB + 12.5, 11.6), 0.42, 0.20, 10); tube(mb, M['mast'], (0, YB + 12.0, 11.4), (0, YB + 18.5, 13.6), 0.16, 0.08, 8)
    z0f = deck_z(11.5); z0m = deck_z(-0.5)
    fore_top = Vector((0, 11.5, z0f + 0.80 * 36.0)); fore_t2 = Vector((0, 11.5, z0f + 0.45 * 36.0)); main_top = Vector((0, -0.5, z0m + 0.80 * 40.0)); miz_top = Vector((0, -12.5, deck_z(-12.5) + 0.78 * 29.0))
    for (a, b) in ((Vector((0, YB + 18.5, 13.6)), fore_top), (Vector((0, YB + 12.3, 11.6)), fore_t2), (fore_top, main_top), (fore_t2, Vector((0, -0.5, z0m + 0.45 * 40.0))), (main_top, miz_top), (Vector((0, -0.5, z0m + 0.45 * 40.0)), Vector((0, -12.5, deck_z(-12.5) + 0.42 * 29.0)))):
        mb.rod(M['rig6'], a, b, 0.05, 0.05, 4)
    jib(M, 'ship6_jib1', (0, YB + 18.0, 13.5), (0, YB + 11.0, 9.2), (0, 31.2, z0f + 0.78 * 36.0), 1.5)
    jib(M, 'ship6_jib2', (0, YB + 11.6, 11.4), (0, YB + 4.6, 7.8), (0, 28.6, z0f + 0.52 * 36.0), 1.3)
    jib(M, 'ship6_jib3', (0, YB + 4.0, 7.4), (0, YB - 3.0, 6.9), (0, 24.0, z0f + 0.40 * 36.0), 1.0)
    # square spritsail under the bowsprit
    tube(mb, M['mast'], (-3.4, YB + 4.6, 8.0), (3.4, YB + 4.6, 8.0), 0.12, 0.08, 6)
    sq_sail(M, 'ship6_sprit', YB + 4.6, 5.0, 8.0, 3.0, 3.3, 0.9, 10, 8, 0.2)
    mb.finish()
    for o in set(bpy.data.objects) - before: o.parent = None
    return M, before

def sea_swell_params():
    rng = np.random.RandomState(3); sw = []; ch = []
    for (L, A, deg) in [(52, 0.85, 80), (31, 0.55, 112), (19, 0.34, 70)]:
        a = math.radians(deg + rng.uniform(-8, 8)); k = 2 * math.pi / L; ph = rng.uniform(0, 6.28); sw.append((k, math.cos(a), math.sin(a), ph, A))
    for (L, A) in [(7.4, .10), (4.8, .06), (3.1, .04), (2.0, .026), (1.3, .016)]:
        a = math.radians(80 + rng.uniform(-50, 50)); k = 2 * math.pi / L; ph = rng.uniform(0, 6.28); ch.append((k, math.cos(a), math.sin(a), ph, A, L))
    return sw, ch
def swell_h(px, py):
    sw, _ = sea_swell_params(); h = np.zeros_like(np.asarray(px, dtype=np.float64))
    for (k, ca, sa, ph, A) in sw:
        q = 0.5 + 0.5 * np.sin(k * (ca * px + sa * py) + ph); h = h + A * (2 * q ** 1.5 - 1.0)
    return h

def catmull(Pc, n):
    Pc = np.asarray(Pc, dtype=np.float64); Pp = np.vstack([Pc[0] * 2 - Pc[1], Pc, Pc[-1] * 2 - Pc[-2]]); m = len(Pp) - 3; out = []
    for k in range(n):
        u = k / (n - 1) * m; i = min(int(u), m - 1); f = u - i; p0, p1, p2, p3 = Pp[i:i + 4]
        out.append(0.5 * ((2 * p1) + (-p0 + p2) * f + (2 * p0 - 5 * p1 + 4 * p2 - p3) * f * f + (-p0 + 3 * p1 - 3 * p2 + p3) * f ** 3))
    return np.array(out)

def foam_sheet_mat(name, lacy=1.0, alpha_k=0.97):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    geo = N('ShaderNodeNewGeometry'); sp = N('ShaderNodeAttribute'); sp.attribute_type = 'GEOMETRY'; sp.attribute_name = 'sp'
    hz = N('ShaderNodeAttribute'); hz.attribute_type = 'GEOMETRY'; hz.attribute_name = 'hz'
    ln = N('ShaderNodeAttribute'); ln.attribute_type = 'GEOMETRY'; ln.attribute_name = 'lp'
    tc = N('ShaderNodeTexCoord'); nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 2.2; nz.inputs['Detail'].default_value = 7.0; nz.inputs['Roughness'].default_value = 0.62; L(tc.outputs['Object'], nz.inputs['Vector'])
    nz2 = N('ShaderNodeTexNoise'); nz2.inputs['Scale'].default_value = 7.0; nz2.inputs['Detail'].default_value = 3.0; L(tc.outputs['Object'], nz2.inputs['Vector'])
    # lacy outer edge: s + (noise-.5)*k - c  -> 0..1
    a1 = N('ShaderNodeMath'); a1.operation = 'SUBTRACT'; a1.inputs[1].default_value = 0.5; L(nz.outputs['Fac'], a1.inputs[0])
    a2 = N('ShaderNodeMath'); a2.operation = 'MULTIPLY'; a2.inputs[1].default_value = 0.62 * lacy; L(a1.outputs[0], a2.inputs[0])
    a3 = N('ShaderNodeMath'); a3.operation = 'ADD'; L(sp.outputs['Fac'], a3.inputs[0]); L(a2.outputs[0], a3.inputs[1])
    a4 = N('ShaderNodeMath'); a4.operation = 'SUBTRACT'; a4.inputs[1].default_value = 0.10; L(a3.outputs[0], a4.inputs[0])
    am = N('ShaderNodeMapRange'); am.inputs['From Min'].default_value = 0.0; am.inputs['From Max'].default_value = 0.16; L(a4.outputs[0], am.inputs['Value'])
    # fine speckle holes in the thin parts
    sk = N('ShaderNodeMapRange'); sk.inputs['From Min'].default_value = 0.30; sk.inputs['From Max'].default_value = 0.46; L(nz2.outputs['Fac'], sk.inputs['Value'])
    sk2 = N('ShaderNodeMath'); sk2.operation = 'MAXIMUM'; L(sk.outputs['Result'], sk2.inputs[0]); L(sp.outputs['Fac'], sk2.inputs[1])
    # lip end / tail fade
    le = N('ShaderNodeMath'); le.operation = 'SUBTRACT'; le.inputs[0].default_value = 1.0; L(sp.outputs['Fac'], le.inputs[1])
    le2 = N('ShaderNodeMapRange'); le2.inputs['From Min'].default_value = 0.0; le2.inputs['From Max'].default_value = 0.05; L(le.outputs[0], le2.inputs['Value'])
    tf = N('ShaderNodeMapRange'); tf.inputs['From Min'].default_value = 1.0; tf.inputs['From Max'].default_value = 0.82; L(ln.outputs['Fac'], tf.inputs['Value'])
    al = N('ShaderNodeMath'); al.operation = 'MULTIPLY'; L(am.outputs['Result'], al.inputs[0]); L(le2.outputs['Result'], al.inputs[1])
    al2 = N('ShaderNodeMath'); al2.operation = 'MULTIPLY'; L(al.outputs[0], al2.inputs[0]); L(tf.outputs['Result'], al2.inputs[1])
    al3 = N('ShaderNodeMath'); al3.operation = 'MULTIPLY'; L(al2.outputs[0], al3.inputs[0]); L(sk2.outputs[0], al3.inputs[1])
    al4 = N('ShaderNodeMath'); al4.operation = 'MULTIPLY'; al4.inputs[1].default_value = alpha_k; al4.use_clamp = True; L(al3.outputs[0], al4.inputs[0])
    # colour: white top, aqua toward the water; underside turquoise
    cm = N('ShaderNodeMix'); cm.data_type = 'RGBA'; cm.inputs[6].default_value = hexc('#9fe0da'); cm.inputs[7].default_value = hexc('#fbfefc'); L(hz.outputs['Fac'], cm.inputs[0])
    cb = N('ShaderNodeMix'); cb.data_type = 'RGBA'; cb.inputs[7].default_value = hexc('#22b5ad'); L(cm.outputs[2], cb.inputs[6]); L(geo.outputs['Backfacing'], cb.inputs[0])
    es = N('ShaderNodeMath'); es.operation = 'MULTIPLY_ADD'; es.inputs[1].default_value = 0.55; es.inputs[2].default_value = 0.16; L(geo.outputs['Backfacing'], es.inputs[0])
    bs.inputs['Roughness'].default_value = 0.55; bs.inputs['Specular IOR Level'].default_value = 0.2
    L(cb.outputs[2], bs.inputs['Base Color']); L(cb.outputs[2], bs.inputs['Emission Color']); L(es.outputs[0], bs.inputs['Emission Strength'])
    L(al4.outputs[0], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(bs.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface']); return m

def bow_wave6(P):
    rr = np.random.RandomState(11)
    ts = np.linspace(0.58, 1.0, 100); xs = w_wl(ts); ys = YS + ts * (YB - YS)
    port = np.stack([-xs, ys], 1); d = np.diff(port, axis=0); d = np.vstack([d, d[-1]]); d /= np.linalg.norm(d, axis=1, keepdims=True); npt = np.stack([-d[:, 1], d[:, 0]], 1)
    stb = np.stack([xs[::-1], ys[::-1]], 1); d2 = np.diff(stb, axis=0); d2 = np.vstack([d2, d2[-1]]); d2 /= np.linalg.norm(d2, axis=1, keepdims=True); nst = np.stack([-d2[:, 1], d2[:, 0]], 1)
    seg = np.linalg.norm(np.diff(port, axis=0), axis=1); lp = -np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])      # arclength from the tip, negative on the port side
    a0 = math.atan2(npt[-1, 1], npt[-1, 0]); a1 = math.atan2(nst[0, 1], nst[0, 0])
    fan = [(YB * 0 + 0.0, YB) for _ in range(14)]; fan_n = [(math.cos(a0 + (a1 - a0) * k / 13.0), math.sin(a0 + (a1 - a0) * k / 13.0)) for k in range(14)]
    Pp = np.vstack([port, np.array(fan), stb]); Nn = np.vstack([npt, np.array(fan_n), nst]); Ll = np.concatenate([lp, np.linspace(-0.2, 0.2, 14), -lp[::-1]])
    prof = [(3.0, -0.28), (2.35, -0.05), (1.85, 0.38), (1.4, 0.95), (1.0, 1.55), (0.6, 2.0), (0.2, 2.25), (-0.2, 2.2), (-0.52, 1.92), (-0.7, 1.55), (-0.66, 1.22)]
    nK = 26; pr = catmull(prof, nK); sp_ = np.linspace(0, 1, nK)
    verts = []; sp = []; hz = []; lp_ = []
    al = np.abs(Ll)
    E = np.exp(-(np.maximum(al - 2.4, 0) / 6.2) ** 2) * (0.74 + 0.26 * ss(0.0, 2.4, al))
    nzh = 1 + 0.26 * (vnoise2(Ll * 0.8 + 40, np.zeros_like(Ll) + 3.0, 5) - 0.5) * 2; nzd = 0.22 * (vnoise2(Ll * 1.3 + 90, np.zeros_like(Ll) + 8.0, 6) - 0.5) * 2
    for j in range(len(Pp)):
        D = 1.15 + 0.11 * al[j] + nzd[j]; Hs = 1.18 * E[j] * nzh[j]; Wsc = 0.55 + 0.45 * E[j] + 0.25 * ss(6, 14, al[j])
        for k in range(nK):
            dn, zz = pr[k]; pxl = Pp[j, 0] + Nn[j, 0] * (D + dn * Wsc); pyl = Pp[j, 1] + Nn[j, 1] * (D + dn * Wsc)
            wp = loc2w((pxl, pyl, 0)); zb = float(swell_h(wp.x, wp.y)) * 0.92
            verts.append((pxl, pyl, zb + zz * Hs + (0.03 if E[j] < 0.05 else 0.0)))
            sp.append(sp_[k]); hz.append(float(np.clip(zz / 2.25, 0, 1))); lp_.append(float(al[j] / 16.0))
    faces = []; nJ = len(Pp)
    for j in range(nJ - 1):
        for k in range(nK - 1):
            a = j * nK + k; b = (j + 1) * nK + k; c = (j + 1) * nK + k + 1; dd = j * nK + k + 1; faces.append((a, b, c, dd))
    # orientation: the middle of the rising slope must face outward+up
    jm = 20; k = 8; a, b, c, dd = faces[jm * (nK - 1) + k]
    va = Vector(verts[a]); n = (Vector(verts[b]) - va).cross(Vector(verts[dd]) - va); want = Vector((Nn[jm, 0], Nn[jm, 1], 1.0))
    if n.dot(want) < 0: faces = [(f[3], f[2], f[1], f[0]) for f in faces]
    me = bpy.data.meshes.new('wave6'); me.from_pydata(verts, [], faces); me.update()
    for p in me.polygons: p.use_smooth = True
    for nm, arr in (('sp', sp), ('hz', hz), ('lp', lp_)):
        at = me.attributes.new(nm, 'FLOAT', 'POINT'); at.data.foreach_set('value', np.array(arr, dtype=np.float32))
    ob = bpy.data.objects.new('ship6_wave', me); bpy.context.scene.collection.objects.link(ob); me.materials.append(foam_sheet_mat('wave6')); ob.visible_shadow = False
    return Pp, Nn, E, Ll

def spray6(P, M, Pp, Nn, E, Ll):
    rr = random.Random(21); sp = MB('ship6_fleck'); tq = M['spray']
    for _ in range(420):
        j = rr.randrange(len(Pp)); al = abs(Ll[j]); 
        if E[j] < 0.15: continue
        D = 1.0 + 0.11 * al; r = rr.uniform(-0.6, 3.2); hgt = rr.uniform(0.0, 1.0) ** 1.6 * 3.6 * E[j] + 1.2 * E[j]
        px_ = Pp[j, 0] + Nn[j, 0] * (D + r); py_ = Pp[j, 1] + Nn[j, 1] * (D + r)
        wp = loc2w((px_, py_, 0)); zb = float(swell_h(wp.x, wp.y))
        rad = rr.uniform(0.05, 0.14) * (1.0 if hgt < 2.4 else 0.75); sp.ell(tq, (px_, py_, zb + 1.2 + hgt), (rad, rad, rad * 0.9), (6, 4))
    sp.finish(shadow=False)
    # soft mist billboards above the crest, facing the camera
    cam = Vector(P['cam']['loc']); mm = bpy.data.materials.new('mist'); mm.use_nodes = True; nt = mm.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); tc = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (2, 2, 2); mp.inputs['Location'].default_value = (-1, -1, 0); L(tc.outputs['Generated'], mp.inputs['Vector'])
    gr = N('ShaderNodeTexGradient'); gr.gradient_type = 'SPHERICAL'; L(mp.outputs[0], gr.inputs['Vector'])
    pw = N('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 1.6; L(gr.outputs['Fac'], pw.inputs[0])
    sc_ = N('ShaderNodeMath'); sc_.operation = 'MULTIPLY'; sc_.inputs[1].default_value = P.get('mist_a', 0.30); L(pw.outputs[0], sc_.inputs[0])
    em.inputs['Color'].default_value = hexc('#f4fafa'); em.inputs['Strength'].default_value = 1.1
    L(sc_.outputs[0], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    rr = random.Random(33)
    for _ in range(26):
        j = rr.randrange(8, len(Pp) - 8)
        if E[j] < 0.25: continue
        D = 1.0 + 0.11 * abs(Ll[j]); p = loc2w((Pp[j, 0] + Nn[j, 0] * (D + rr.uniform(-0.2, 1.4)), Pp[j, 1] + Nn[j, 1] * (D + 0.5), 0)); p.z = float(swell_h(p.x, p.y)) + rr.uniform(1.8, 4.2) * E[j] + 0.6
        tcam = (cam - p).normalized(); rgt = Vector((0, 0, 1)).cross(tcam).normalized(); up = tcam.cross(rgt).normalized(); sz = rr.uniform(1.2, 2.6)
        vs = [p + rgt * (-sz) + up * (-sz * 0.7), p + rgt * sz + up * (-sz * 0.7), p + rgt * sz + up * (sz * 0.7), p + rgt * (-sz) + up * (sz * 0.7)]
        me = bpy.data.meshes.new('mist'); me.from_pydata([tuple(v) for v in vs], [], [(0, 1, 2, 3)]); me.update(); me.materials.append(mm)
        ob = bpy.data.objects.new('skyobj_mist', me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = False

# ---- smooth cumulus: metaball union (one smooth surface), flat soft bottom, emission gradient material
def cumulus6(P, name, c, size, seed, nballs=70, squash=0.9):
    rr = random.Random(seed); mbd = bpy.data.metaballs.new(name); mbd.resolution = 0.07; mbd.render_resolution = 0.07; mbd.threshold = 0.55
    balls = []
    nb = int(nballs * 0.35)
    for i in range(nb):                       # wide base row
        x = rr.uniform(-2.6, 2.6); balls.append((x, rr.uniform(-0.5, 0.5), rr.uniform(0.0, 0.5), rr.uniform(0.75, 1.1)))
    for i in range(int(nballs * 0.4)):        # body
        x = rr.uniform(-2.0, 2.0); balls.append((x, rr.uniform(-0.5, 0.5), rr.uniform(0.6, 1.5), rr.uniform(0.7, 1.05) * (1.1 - abs(x) * 0.12)))
    for i in range(int(nballs * 0.3)):        # towers
        x = rr.uniform(-1.3, 1.5); balls.append((x, rr.uniform(-0.4, 0.4), rr.uniform(1.4, 2.5) * (1.1 - abs(x) * 0.18), rr.uniform(0.5, 0.85)))
    for (x, y, z, r) in balls:
        e = mbd.elements.new(type='BALL'); e.co = (x, y, z); e.radius = r; e.stiffness = 2.2
    ob = bpy.data.objects.new(name, mbd); bpy.context.scene.collection.objects.link(ob)
    dg = bpy.context.evaluated_depsgraph_get(); me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg)); bpy.data.objects.remove(ob)
    co = np.empty(len(me.vertices) * 3, dtype=np.float32); me.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
    zmin = 0.35; co[:, 2] = np.where(co[:, 2] < zmin, zmin + (co[:, 2] - zmin) * 0.18, co[:, 2]); co[:, 1] *= squash
    me.vertices.foreach_set('co', co.ravel()); me.update()
    for p in me.polygons: p.use_smooth = True
    ob2 = bpy.data.objects.new('clouds_' + name, me); bpy.context.scene.collection.objects.link(ob2); ob2.data.materials.append(cloud_mat(P) if 'cloudG' not in MATS else MATS['cloudG'])
    ob2.location = c; ob2.scale = (size, size, size * 0.85); ob2.visible_shadow = False
    return ob2

def clouds6(P):
    cm = cloud_mat(P)
    for (nm, c, sz, sd) in P['clouds6']: cumulus6(P, nm, c, sz, sd)

def gull6(mb, m, mt, c, yaw, s, flap):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Diagonal((s, s, s, 1)))
    mb.ell(m, (0, 0, 0), (0.12, 0.42, 0.11), (10, 6)); mb.ell(m, (0, 0.40, 0.03), (0.075, 0.12, 0.07), (8, 5)); mb.ell(m, (0, -0.42, 0.0), (0.06, 0.2, 0.03), (8, 4))
    for sd in (-1, 1):
        pts = [(0.08, 0.15, 0.02), (0.75, 0.22 - 0.12 * flap, 0.12 + 0.34 * flap), (1.45, 0.02 - 0.2 * flap, 0.14 + 0.62 * flap), (1.95, -0.30 - 0.3 * flap, 0.0 + 0.6 * flap)]
        pb = [(0.08, -0.22, 0.0), (0.72, -0.12 - 0.1 * flap, 0.10 + 0.3 * flap), (1.35, -0.38 - 0.2 * flap, 0.1 + 0.55 * flap), (1.95, -0.58 - 0.3 * flap, 0.0 + 0.55 * flap)]
        for i in range(3):
            q = [(sd * pb[i][0], pb[i][1], pb[i][2]), (sd * pb[i + 1][0], pb[i + 1][1], pb[i + 1][2]), (sd * pts[i + 1][0], pts[i + 1][1], pts[i + 1][2]), (sd * pts[i][0], pts[i][1], pts[i][2])]
            mb.quad(mt if i == 2 else m, q); mb.quad(mt if i == 2 else m, q[::-1])
    mb.pop()

def far_dressing6(P, M):
    ib = MB('isle'); n = 56; X0i = 524.0; stp = 8.6
    for i in range(n):
        x0 = X0i + i * stp; x1 = x0 + stp
        f = lambda x: 66 * max(0, math.sin(math.pi * (x - X0i) / (n * stp))) ** 0.6 * (0.8 + 0.2 * math.sin((x - X0i) / 13.0)) + 6
        ib.quad(M['isle'] if i % 3 else M['isle2'], [(x0, 1800, 0), (x1, 1800, 0), (x1, 1800, f(x1)), (x0, 1800, f(x0))]); ib.quad(M['beach'], [(x0, 1799, -0.5), (x1, 1799, -0.5), (x1, 1799, 3.5), (x0, 1799, 3.5)])
    ib.finish(shadow=False)
    fs = MB('farsail'); x0, y0 = 205.0, 720.0
    fs.box(M['darksail'], (x0, y0, 1.2), (14.0, 3.0, 2.4))
    for k, (dx, hh, w) in enumerate(((-3.2, 17.0, 5.4), (2.4, 20.0, 5.8))):
        fs.quad(M['canv'], [(x0 + dx - w / 2, y0 - 0.4, 2.8), (x0 + dx + w / 2, y0 - 0.4, 2.8), (x0 + dx + w * 0.4, y0 - 0.4, hh), (x0 + dx - w * 0.4, y0 - 0.4, hh)])
    fs.finish(shadow=False)
    gm = MB('gulls'); gm.finish()
    gb = MB('gulls'); mw = mat('gullw', '#f6f5f0', '#e8ecee', scale=6); mt = mat('gullt', '#2e3038')
    for (c, yaw, s, fl) in P['gulls']: gull6(gb, mw, mt, c, yaw, s, fl)
    gb.finish(shadow=True)

def build_ship6_all(P):
    M, before = build_ship6(P)
    s = SHIP6; root = bpy.data.objects.new('shiproot', None); bpy.context.scene.collection.objects.link(root)
    root.location = (s['cx'], s['cy'], 0.0); root.rotation_euler = (0, 0, math.radians(180.0 - s['theta']))
    Pp, Nn, E, Ll = bow_wave6(P); spray6(P, M, Pp, Nn, E, Ll)
    for o in bpy.data.objects:
        if o.type == 'MESH' and o.parent is None and (o.name.startswith('ship6') or o.name.startswith('shiproot')) : o.parent = root
    far_dressing6(P, M)
    if not os.environ.get('NOSEA'): build_sea6(P)
    clouds6(P)

# ---------------------------------------------------------------- the v6 sea: SAME swells, material and glitter as v5 (kept exactly); only the grid density, the ship-local foam field and a small bow hump are new
def build_sea6(P):
    c = P['cam']; loc = np.array(c['loc'], dtype=np.float64); look = np.array(c['look'], dtype=np.float64)
    f = look - loc; f /= np.linalg.norm(f); r = np.cross(f, [0, 0, 1.0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    hx, hy = 0.4602 * 1.15, 0.8182
    zfar = loc[2] / 7000.0
    vmax = (-zfar - f[2]) / (u[2] * hy); vmin = -1.3
    NU, NV = P.get('sea_nu', 800), P.get('sea_nv', 1100)
    uu = np.linspace(-1.0, 1.0, NU); vv = vmin + (vmax - vmin) * np.linspace(0, 1, NV)
    UU, VV = np.meshgrid(uu, vv)
    ray = f[None, None, :] + r[None, None, :] * (UU * hx)[..., None] + u[None, None, :] * (VV * hy)[..., None]
    t = -loc[2] / ray[..., 2]; px = loc[0] + ray[..., 0] * t; py = loc[1] + ray[..., 1] * t
    fpx = t * (2 * hx / 720.0) * 1.1
    sw, ch = sea_swell_params()
    h = np.zeros_like(px)
    for (k, ca, sa, ph, A) in sw:
        q = 0.5 + 0.5 * np.sin(k * (ca * px + sa * py) + ph); h += A * (2 * q ** 1.5 - 1.0)
    for (k, ca, sa, ph, A, L) in ch:
        fade = np.clip((L / np.maximum(fpx, 1e-6) - 4.0) / 7.0, 0, 1) * np.clip(1 - t / 260.0, 0, 1)
        h += A * np.sin(k * (ca * px + sa * py) + ph) * fade
    h *= np.clip(1 - t / 3500.0, 0, 1) ** 0.5
    # ---- ship-local frame
    s = SHIP6; ph_ = math.radians(180.0 - s['theta']); dx = px - s['cx']; dy = py - s['cy']
    lx = dx * math.cos(ph_) + dy * math.sin(ph_); ly = -dx * math.sin(ph_) + dy * math.cos(ph_)
    tt = np.clip((ly - YS) / (YB - YS), 0, 1); bw = w_wl(tt)
    ax = np.abs(lx)
    dh = np.where(ly >= YB, np.hypot(lx, ly - YB), ax - bw)           # distance from the hull waterline (negative = under the hull)
    dback = np.maximum(YS - ly, 0.0)
    ahead = ss(YB + 6.0, YB - 2.0, ly)
    # small bow hump + hull-side swell pushed up
    hump = 0.38 * np.exp(-((np.maximum(dh, 0) - 1.6) / 2.4) ** 2) * ss(YB - 16.0, YB - 2.0, ly) * ss(YB + 5.0, YB, ly) * (dh > -1.0)
    h += hump
    # ---- foam field: three lacy bands along the hull (3:1 patches, noise-thresholded), V wake from the stern with a turbulent core, bow ring under the wave
    def patches(n, thr, soft=0.11): return np.clip((n - thr) / soft, 0, 1)
    sideok = (ly > YS - 3.0) & (ly < YB + 8.0)
    n1 = 0.80 * fbm2(ly / 10.0, ax / 3.2, 4, 3) + 0.20 * vnoise2(ly * 0.9, ax * 1.1, 9)
    band = np.zeros_like(px)
    for (off, wd, amp, sd) in ((1.9, 1.7, 1.0, 4), (6.2, 2.4, 0.9, 14), (11.0, 3.0, 0.8, 24)):
        env = np.clip(1 - np.abs(dh - off) / wd, 0, 1); env = env * env * (3 - 2 * env)
        n = 0.78 * fbm2(ly / 9.0 + sd, ax / 2.9, 4 + sd, 3) + 0.22 * vnoise2(ly * 1.0 + sd, ax * 1.2, 9 + sd)
        band = np.maximum(band, patches(n, 0.58 - 0.26 * env) * env * amp)
    band *= sideok * ss(YB + 4.0, YB - 8.0, ly) * np.clip(1 - dback / 9.0, 0, 1) ** 0.5 * ss(-0.6, 0.5, dh)
    # wake behind the stern: widening V (arms ~ 3:1 patches along the track) + turbulent core
    wake = np.zeros_like(px); bws = float(w_wl(0.0))
    for (slope, wd0, wd1, amp, sd) in ((0.30, 1.5, 0.16, 1.0, 40), (0.13, 1.3, 0.10, 0.85, 50), (0.52, 1.9, 0.20, 0.7, 60)):
        xarm = bws * 0.9 + slope * dback; wd = wd0 + wd1 * dback
        env = np.clip(1 - np.abs(ax - xarm) / wd, 0, 1); env = env * env * (3 - 2 * env)
        n = 0.78 * fbm2(dback / 9.0 + sd, (ax - xarm) / 2.6, 4 + sd, 3) + 0.22 * vnoise2(dback * 0.8, ax * 1.2, 20 + sd)
        wake = np.maximum(wake, patches(n, 0.58 - 0.25 * env) * env * amp * np.exp(-dback / 78.0))
    core = np.exp(-(lx / (bws * 0.95 + 0.07 * dback)) ** 2) * np.exp(-dback / 34.0)
    nc = 0.78 * fbm2(dback / 6.0 + 70, lx / 1.7, 3, 3) + 0.22 * vnoise2(dback * 1.1, lx * 1.3, 8)
    wake = np.maximum(wake, patches(nc, 0.60 - 0.22 * core) * core)
    wake *= (ly < YS + 3.0) * ss(YS + 3.0, YS - 1.0, ly)
    # bow ring: foam where the wave sheet falls back, strongest at the stem
    ringenv = ss(0.0, 1.4, dh) * (1 - ss(3.2, 6.0, dh)) * ss(YB - 15.0, YB - 2.0, ly) * ss(YB + 7.0, YB + 1.0, ly)
    nb = 0.75 * fbm2(ly / 3.6 + 90, ax / 2.0 + 10, 7, 3) + 0.25 * vnoise2(ly * 1.5, ax * 1.5, 12)
    bow = patches(nb, 0.50 - 0.2 * ringenv) * ringenv
    foam = np.nan_to_num(np.clip(np.maximum(np.maximum(band, wake), bow), 0, 1))
    verts = np.stack([px, py, h], -1).reshape(-1, 3).astype(np.float32)
    idx = np.arange(NU * NV).reshape(NV, NU)
    a_ = idx[:-1, :-1]; b_ = idx[:-1, 1:]; c_ = idx[1:, 1:]; d_ = idx[1:, :-1]
    alt = ((np.arange(NU - 1)[None, :] + np.arange(NV - 1)[:, None]) % 2).astype(bool)
    t1 = np.where(alt[..., None], np.stack([a_, b_, c_], -1), np.stack([a_, b_, d_], -1)); t2 = np.where(alt[..., None], np.stack([a_, c_, d_], -1), np.stack([b_, c_, d_], -1))
    tris = np.concatenate([t1.reshape(-1, 3), t2.reshape(-1, 3)])
    me = bpy.data.meshes.new('sea'); me.vertices.add(len(verts)); me.vertices.foreach_set('co', verts.ravel())
    nt_ = len(tris); me.loops.add(nt_ * 3); me.polygons.add(nt_)
    me.loops.foreach_set('vertex_index', tris.ravel().astype(np.int32)); me.polygons.foreach_set('loop_start', (np.arange(nt_) * 3).astype(np.int32)); me.polygons.foreach_set('loop_total', np.full(nt_, 3, dtype=np.int32))
    me.update(calc_edges=True); me.polygons.foreach_set('use_smooth', np.ones(nt_, dtype=bool))
    at = me.attributes.new('foam', 'FLOAT', 'POINT'); at.data.foreach_set('value', foam.reshape(-1).astype(np.float32))
    ob = bpy.data.objects.new('sea', me); bpy.context.scene.collection.objects.link(ob)
    m = bpy.data.materials.new('sea'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled')
    bs.inputs['Roughness'].default_value = 0.1; bs.inputs['IOR'].default_value = 1.33; bs.inputs['Specular IOR Level'].default_value = 0.5
    cdv = N('ShaderNodeCameraData'); msp = N('ShaderNodeMapRange'); msp.inputs['From Min'].default_value = 20.0; msp.inputs['From Max'].default_value = 120.0; msp.inputs['To Min'].default_value = 0.22; msp.inputs['To Max'].default_value = 0.5; L(cdv.outputs['View Distance'], msp.inputs['Value']); L(msp.outputs['Result'], bs.inputs['Specular IOR Level'])
    def mixc(a, b, fac):
        mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'
        if hasattr(a, 'node'): L(a, mx.inputs[6])
        else: mx.inputs[6].default_value = a
        if hasattr(b, 'node'): L(b, mx.inputs[7])
        else: mx.inputs[7].default_value = b
        L(fac, mx.inputs[0]); return mx.outputs[2]
    cd = N('ShaderNodeCameraData'); mr = N('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = 22.0; mr.inputs['From Max'].default_value = 220.0; L(cd.outputs['View Distance'], mr.inputs['Value'])
    col = mixc(hexc(P['sea_near']), hexc(P['sea_far']), mr.outputs['Result'])
    gp = N('ShaderNodeNewGeometry'); spz = N('ShaderNodeSeparateXYZ'); L(gp.outputs['Position'], spz.inputs[0])
    cr = N('ShaderNodeMapRange'); cr.inputs['From Min'].default_value = 0.55; cr.inputs['From Max'].default_value = 0.9; L(spz.outputs['Z'], cr.inputs['Value'])
    tcw = N('ShaderNodeTexCoord'); mpw = N('ShaderNodeMapping'); mpw.inputs['Scale'].default_value = (1.1, 0.7, 1.0); L(tcw.outputs['Object'], mpw.inputs['Vector'])
    nzw = N('ShaderNodeTexNoise'); nzw.inputs['Scale'].default_value = 1.0; nzw.inputs['Detail'].default_value = 2.0; L(mpw.outputs[0], nzw.inputs['Vector'])
    sp2 = N('ShaderNodeMapRange'); sp2.inputs['From Min'].default_value = 0.52; sp2.inputs['From Max'].default_value = 0.64; L(nzw.outputs['Fac'], sp2.inputs['Value'])
    wc = N('ShaderNodeMath'); wc.operation = 'MULTIPLY'; wc.use_clamp = True; L(cr.outputs['Result'], wc.inputs[0]); L(sp2.outputs['Result'], wc.inputs[1])
    col = mixc(col, hexc('#e4eeec'), wc.outputs[0])
    fa = N('ShaderNodeAttribute'); fa.attribute_type = 'GEOMETRY'; fa.attribute_name = 'foam'
    nz2 = N('ShaderNodeTexNoise'); nz2.inputs['Scale'].default_value = 1.6; nz2.inputs['Detail'].default_value = 1.0; mp2 = N('ShaderNodeMapping'); mp2.inputs['Scale'].default_value = (2.4, 2.4, 1.0); L(tcw.outputs['Object'], mp2.inputs['Vector']); L(mp2.outputs[0], nz2.inputs['Vector'])
    br = N('ShaderNodeMapRange'); br.inputs['From Min'].default_value = -2.0; br.inputs['From Max'].default_value = -1.0; L(nz2.outputs['Fac'], br.inputs['Value'])
    fm = N('ShaderNodeMath'); fm.operation = 'MULTIPLY'; fm.use_clamp = True; L(fa.outputs['Fac'], fm.inputs[0]); L(br.outputs['Result'], fm.inputs[1])
    fm2 = N('ShaderNodeMath'); fm2.operation = 'MULTIPLY'; fm2.use_clamp = True; fm2.inputs[1].default_value = 1.25; L(fm.outputs[0], fm2.inputs[0])
    col = mixc(col, hexc('#f0f6f2'), fm2.outputs[0])
    L(col, bs.inputs['Base Color'])
    lw = N('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.3
    mrn = N('ShaderNodeMapRange'); mrn.inputs['From Min'].default_value = 20.0; mrn.inputs['From Max'].default_value = 120.0; mrn.inputs['To Min'].default_value = 0.12; mrn.inputs['To Max'].default_value = 1.0; L(cd.outputs['View Distance'], mrn.inputs['Value'])
    fk = N('ShaderNodeMath'); fk.operation = 'MULTIPLY'; fk.inputs[1].default_value = P.get('fresnel_k', 0.7); L(mrn.outputs['Result'], fk.inputs[0])
    em = N('ShaderNodeMath'); em.operation = 'MULTIPLY'; L(lw.outputs['Fresnel'], em.inputs[0]); L(fk.outputs[0], em.inputs[1])
    bs.inputs['Emission Color'].default_value = hexc('#9fc2d8'); L(em.outputs[0], bs.inputs['Emission Strength'])
    nzb = N('ShaderNodeTexNoise'); nzb.inputs['Scale'].default_value = 1.8; nzb.inputs['Detail'].default_value = 0.0; L(tcw.outputs['Object'], nzb.inputs['Vector'])
    bp = N('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.2; bp.inputs['Distance'].default_value = 0.2; L(nzb.outputs['Fac'], bp.inputs['Height']); L(bp.outputs['Normal'], bs.inputs['Normal'])
    L(bs.outputs[0], out.inputs['Surface']); ob.data.materials.append(m)
    # glossy-only virtual sun (light-linked to the sea): the sharp glitter lobe lands under it, ahead-left of the camera
    coll = bpy.data.collections.new('seacoll'); bpy.context.scene.collection.children.link(coll); coll.objects.link(ob)
    kd = Vector(kdir(P['glit_az'], P['glit_el'])).normalized(); d = bpy.data.lights.new('glint', 'SUN'); d.color = (1.0, 0.86, 0.62); d.energy = P.get('glit_k', 14.0); d.angle = math.radians(0.6)
    o = bpy.data.objects.new('glint', d); bpy.context.scene.collection.objects.link(o); o.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler()
    o.visible_diffuse = False; o.light_linking.receiver_collection = coll


build_ship = build_ship6_all
PRESETS['ship'] = dict(
    sky=[(0.0, '#6c9ce0'), (0.46, '#b6cfe8'), (0.5, '#b0cbe8'), (0.56, '#8db3e6'), (0.66, '#6a98e0'), (0.78, '#4a7bd6'), (0.88, '#3a67cb'), (1.0, '#2c54b6')], sky_k=1.0,
    key=(1.0, 0.92, 0.78, 7.2), key_dir=kdir(160, 42), sun_angle=0.9, exposure=0.1, sat=1.08, amb=('#3050FF', 1.7), samples=80, dbounce=1, gloss=2,
    cloud=('#ffffff', '#8c9ce8'), cloud_diffuse=True,
    clouds6=[('cF', (-40, 620, 330), 46, 17), ('cA', (-250, 430, 130), 36, 3), ('cB', (150, 520, 215), 44, 7), ('cC', (-330, 700, 90), 40, 5), ('cD', (380, 560, 70), 30, 11), ('cE', (20, 900, 120), 60, 13)],
    gulls=[((9.2, 30.0, 14.0), 2.2, 0.6, 0.4), ((8.2, 40.0, 28.0), 0.8, 0.55, -0.3), ((-18.5, 50.0, 39.0), 3.4, 0.6, 0.1), ((13.4, 35.0, 9.3), 1.0, 0.45, 0.6), ((11.0, 46.0, 22.0), 2.9, 0.5, 0.0)],
    sea_near='#0a4a58', sea_far='#0a2c4c', fresnel_k=0.7,
    glit_az=12, glit_el=9, glit_k=30.0,
    cam=dict(loc=(0.0, 0.0, 5.0), look=(0.0, 100.0, 5.0 + 100.0 * math.tan(math.radians(3.0))), lens=22))

def lights_ship(P):
    sun_light(P); w = sky_world2(P)

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
    M['rug'] = mat('hrug', '#4c5268', '#586078', scale=6, contrast=1.1)
    M['rugb'] = mat('hrugb', '#5a1e2a', '#6c2432', scale=6)
    M['gold'] = metal_mat('hgold', '#cb9f48', '#e6bb5c', rough=0.3, spec=0.9, metallic=0.9)
    M['brass'] = metal_mat('hbrass', '#cb9f48', '#e6bb5c', rough=0.28, spec=0.9, metallic=0.9)
    M['brassd'] = metal_mat('hbrassd', '#8a5e20', '#b0802e', rough=0.32, spec=0.8, metallic=0.9)
    M['lacq'] = mat('hlacq', '#2a1a18', '#3a2420', scale=6)
    M['map'] = mat('hmap', '#d8c490', '#c8b078', scale=5)
    M['dome'] = mat_emit('hdome', '#e8d8b0', 0.9); M['domer'] = mat_emit('hdomer', '#c8854a', 0.8); M['tree'] = mat_emit('htree', '#4a7a48', 0.55); M['tree2'] = mat_emit('htree2', '#5e8c4e', 0.6); M['trunk'] = mat_emit('htrunk', '#5a3a28', 0.5)
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
    rx0, rx1, ry0, ry1 = -1.9, 1.1, -2.2, 4.3
    rcx, rcy = (rx0 + rx1) / 2, (ry0 + ry1) / 2; rw, rl = rx1 - rx0, ry1 - ry0
    mb.box(M['rugb'], (rcx, rcy, 0.012), (rw + 0.6, rl + 0.6, 0.024)); mb.box(M['gold'], (rcx, rcy, 0.026), (rw + 0.36, rl + 0.36, 0.012))
    mb.box(M['rugb'], (rcx, rcy, 0.032), (rw + 0.3, rl + 0.3, 0.012)); mb.box(M['gold'], (rcx, rcy, 0.04), (rw + 0.1, rl + 0.1, 0.012))
    mb.box(M['rug'], (rcx, rcy, 0.046), (rw, rl, 0.02))
    for k in range(int(rl / 0.32)):                                    # border diamonds
        yy = ry0 + 0.16 + 0.32 * k
        for xx in (rx0 - 0.1, rx1 + 0.1): mb.box(M['gold'], (xx, yy, 0.044), (0.11, 0.11, 0.012), rz=0.785)
    for k in range(int(rw / 0.32)):
        xx = rx0 + 0.16 + 0.32 * k
        for yy in (ry0 - 0.1, ry1 + 0.1): mb.box(M['gold'], (xx, yy, 0.044), (0.11, 0.11, 0.012), rz=0.785)
    for (cxm, cym, rmx, rmy) in [(rcx, rcy, 0.95, 1.5), (rcx, ry0 + 0.9, 0.5, 0.4), (rcx, ry1 - 0.9, 0.5, 0.4)]:   # medallions
        mb.ell(M['rugb'], (cxm, cym, 0.058), (rmx, rmy, 0.004), (24, 8)); mb.ell(M['gold'], (cxm, cym, 0.062), (rmx * 0.82, rmy * 0.82, 0.004), (24, 8)); mb.ell(M['rug'], (cxm, cym, 0.066), (rmx * 0.74, rmy * 0.74, 0.004), (24, 8))
        mb.ell(M['rugb'], (cxm, cym, 0.07), (rmx * 0.34, rmy * 0.34, 0.004), (20, 8))
    for sx in (-1, 1):
        for sy in (-1, 1): mb.box(M['gold'], (rcx + sx * (rw / 2 - 0.3), rcy + sy * (rl / 2 - 0.3), 0.058), (0.3, 0.3, 0.008), rz=0.785); mb.box(M['rugb'], (rcx + sx * (rw / 2 - 0.3), rcy + sy * (rl / 2 - 0.3), 0.064), (0.18, 0.18, 0.008), rz=0.785)
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
    gl = MB('glass'); sk = mat_emit('hsky', '#a8c8f4', 1.5); hd = mat_emit('hhedge', '#4e7a58', 0.55)
    gl.quad(sk, [(-1.0, Y1 + 0.4, wz0 + 0.8), (1.0, Y1 + 0.4, wz0 + 0.8), (1.0, Y1 + 0.4, wz1), (-1.0, Y1 + 0.4, wz1)][::-1])
    for i in range(n):
        za = wz1 + rad * i / n; zb = wz1 + rad * (i + 1) / n; w = math.sqrt(max(0, rad ** 2 - ((za + zb) / 2 - wz1) ** 2)); gl.quad(sk, [(-w, Y1 + 0.4, za), (w, Y1 + 0.4, za), (w, Y1 + 0.4, zb), (-w, Y1 + 0.4, zb)])
    gl.quad(hd, [(-1.0, Y1 + 0.39, wz0), (1.0, Y1 + 0.39, wz0), (1.0, Y1 + 0.39, wz0 + 0.8), (-1.0, Y1 + 0.39, wz0 + 0.8)][::-1])
    for (tx_, tz_, tr, tm) in [(-0.75, wz0 + 0.8, 0.28, 'tree'), (-0.4, wz0 + 0.75, 0.22, 'tree2'), (0.75, wz0 + 0.85, 0.3, 'tree2'), (0.45, wz0 + 0.7, 0.2, 'tree')]:
        gl.ell(M[tm], (tx_, Y1 + 0.37, tz_), (tr, 0.02, tr * 1.1), (12, 8))
    gl.ell(M['dome'], (0.1, Y1 + 0.36, wz0 + 0.8), (0.3, 0.02, 0.2), (14, 8)); gl.quad(M['dome'], [(-0.2, Y1 + 0.35, wz0 + 0.6), (0.4, Y1 + 0.35, wz0 + 0.6), (0.4, Y1 + 0.35, wz0 + 0.85), (-0.2, Y1 + 0.35, wz0 + 0.85)][::-1])
    gl.ell(M['domer'], (0.1, Y1 + 0.34, wz0 + 0.95), (0.19, 0.02, 0.2), (14, 8)); gl.quad(M['domer'], [(0.08, Y1 + 0.33, wz0 + 1.15), (0.12, Y1 + 0.33, wz0 + 1.15), (0.12, Y1 + 0.33, wz0 + 1.3), (0.08, Y1 + 0.33, wz0 + 1.3)][::-1])
    gl.finish(shadow=False)
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
    mx, mz = -2.8, 3.4
    for k in range(28):                                                   # gilt oval frame
        a = 2 * math.pi * (k + 0.5) / 28; ex, ez = 0.62 * math.cos(a), 0.9 * math.sin(a)
        mb.box(M['gold'], (mx + ex, Y1 - 0.13, mz + ez), (0.17, 0.08, 0.1), ry=-(math.atan2(0.9 * math.cos(a), -0.62 * math.sin(a))))
    mb.ell(M['navy'], (mx, Y1 - 0.14, mz), (0.56, 0.02, 0.84), (24, 12)); mb.ell(M['moon'], (mx, Y1 - 0.16, mz + 0.05), (0.42, 0.02, 0.42), (24, 12))
    for (dx, dz, r) in [(-0.14, 0.15, 0.09), (0.12, 0.05, 0.065), (0.04, -0.17, 0.1), (-0.2, -0.08, 0.05), (0.2, 0.22, 0.045)]: mb.ell(M['crater'], (mx + dx, Y1 - 0.175, mz + 0.05 + dz), (r, 0.01, r), (12, 8))
    for k in range(9): mb.ell(M['gold'], (mx + rr.uniform(-0.45, 0.45), Y1 - 0.17, mz + rr.uniform(-0.75, 0.75)), (0.015, 0.01, 0.015), (6, 4))
    for (fx, fz, fw, fh, col) in [(2.9, 3.6, 0.8, 1.0, 'navy')]:
        mb.box(M['gold'], (fx, Y1 - 0.12, fz), (fw + 0.16, 0.06, fh + 0.16)); mb.box(M[col], (fx, Y1 - 0.16, fz), (fw, 0.04, fh)); mb.ell(M['tan'], (fx, Y1 - 0.2, fz + fh * 0.15), (fw * 0.18, 0.02, fh * 0.16), (12, 8)); mb.box(M['ink'], (fx, Y1 - 0.2, fz - fh * 0.15), (fw * 0.5, 0.02, fh * 0.3))
    mb.box(M['gold'], (2.85, Y1 - 0.12, 2.0), (1.1, 0.06, 1.45)); mb.box(M['map'], (2.85, Y1 - 0.16, 2.0), (0.98, 0.04, 1.33))                              # wall map (lines and dots only)
    for k in range(12): mb.box(M['ink'], (2.85 + rr.uniform(-0.3, 0.3), Y1 - 0.19, 2.0 + rr.uniform(-0.5, 0.5)), (rr.uniform(0.25, 0.6), 0.01, 0.012), ry=rr.uniform(0, 3.1))
    for k in range(26): mb.ell(M['ink'], (2.85 + rr.uniform(-0.42, 0.42), Y1 - 0.19, 2.0 + rr.uniform(-0.58, 0.58)), (0.02, 0.008, 0.02), (6, 4))
    mb.ell(M['teal'], (2.7, Y1 - 0.185, 2.3), (0.26, 0.01, 0.22), (10, 6)); mb.ell(M['tan'], (3.0, Y1 - 0.185, 1.7), (0.22, 0.01, 0.3), (10, 6)); mb.ell(M['tan'], (2.7, Y1 - 0.185, 1.55), (0.15, 0.01, 0.12), (10, 6))
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
    for (cx, cy, yaw) in [(0.85, 0.5, -1.5708), (0.85, 1.7, -1.5708), (0.9, 2.9, -1.5708 + 0.2), (3.25, 0.7, 1.5708), (3.25, 1.9, 1.5708 - 0.15), (3.25, 3.0, 1.5708)]:
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
    for t in (0.18, 0.52, 0.86): mb.rod(M['lacq'], at(t - 0.02), at(t + 0.02), 0.2 * (0.6 + 0.4 * t) + 0.012, 0.2 * (0.6 + 0.4 * t) + 0.012, 18, True, True)
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
    # ---- orrery on a round table (left) and a small one on the Board table; quadrant on a stand
    def orrery(ox_, oy_, oz0, sc):
        mb.ell(M['gold'], (ox_, oy_, oz0 + 0.38 * sc), (0.13 * sc, 0.13 * sc, 0.13 * sc), (14, 10)); mb.rod(M['brass'], (ox_, oy_, oz0), (ox_, oy_, oz0 + 0.38 * sc), 0.02 * sc, 0.02 * sc, 6)
        for (r, col, pr, a) in [(0.18, 'redp', 0.04, 0.5), (0.28, 'teal', 0.05, 2.2), (0.38, 'tan', 0.06, 4.0), (0.46, 'navy', 0.05, 5.4)]:
            ring_xy(mb, M['brass'], (ox_, oy_, oz0 + 0.38 * sc), r * sc, 0.012 * sc, 0.012 * sc, 24); mb.ell(M[col], (ox_ + r * sc * math.cos(a), oy_ + r * sc * math.sin(a), oz0 + 0.38 * sc), (pr * sc, pr * sc, pr * sc), (10, 8))
            mb.rod(M['brass'], (ox_, oy_, oz0 + 0.38 * sc), (ox_ + r * sc * math.cos(a), oy_ + r * sc * math.sin(a), oz0 + 0.38 * sc), 0.006 * sc, 0.006 * sc, 4)
    ox_, oy_ = -2.85, 0.9
    mb.cyl(M['woodd'], (ox_, oy_, 0.82), 0.5, 0.06, seg=20); mb.rod(M['wood'], (ox_, oy_, 0.0), (ox_, oy_, 0.8), 0.08, 0.12, 10)
    for a in range(3): mb.rod(M['wood'], (ox_, oy_, 0.2), (ox_ + 0.4 * math.cos(a * 2.094), oy_ + 0.4 * math.sin(a * 2.094), 0.0), 0.04, 0.03, 6)
    orrery(ox_, oy_, 0.84, 1.0); orrery(2.35, 0.25, tz + 0.03, 0.55)
    qx, qy = -2.9, 2.5                                                                   # quadrant on a stand
    for a in range(3): mb.rod(M['woodd'], (qx, qy, 1.0), (qx + 0.4 * math.cos(a * 2.094 + 0.3), qy + 0.4 * math.sin(a * 2.094 + 0.3), 0.0), 0.035, 0.025, 6)
    mb.rod(M['brass'], (qx, qy, 0.9), (qx, qy, 1.25), 0.03, 0.03, 8)
    for k in range(14):
        a = math.radians(5 + k * 6.5); mb.box(M['brass'], (qx + 0.5 * math.cos(a) * 1.0 - 0.25, qy, 1.25 + 0.5 * math.sin(a)), (0.12, 0.02, 0.04), ry=-(a + math.pi / 2))
    mb.rod(M['brass'], (qx - 0.25, qy, 1.25), (qx + 0.25, qy, 1.25), 0.015, 0.015, 6); mb.rod(M['brass'], (qx - 0.25, qy, 1.25), (qx - 0.25, qy, 1.75), 0.015, 0.015, 6)
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
    for a in range(6):
        ang = a * 1.047 + 0.3; ex_ = ccx + 0.4 * math.cos(ang); ey_ = ccy + 0.4 * math.sin(ang)
        mb.cyl(M['gold'], (ex_, ey_, ccz - 0.31), 0.03, 0.05, seg=8); pts.append((ex_, ey_, ccz - 0.285))
    candles(mb, M, fl, pts, 0.16)
    # wall sconces on the pilasters
    sp = []
    for sx_ in (-2.1, 2.1):
        mb.rod(M['gold'], (sx_, Y1 - 0.2, 2.2), (sx_, Y1 - 0.45, 2.35), 0.02, 0.02, 6); mb.cyl(M['gold'], (sx_, Y1 - 0.45, 2.37), 0.05, 0.03, seg=8); sp.append((sx_, Y1 - 0.45, 2.385))
    candles(mb, M, fl, sp, 0.18)
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
    cam=dict(loc=(0.0, -2.6, 1.3), look=(0.0, 5.6, 1.85), lens=22))

def lights_hall(P):
    sun_light(P); shafts(P, (-1.0, 1.0, 1.2, 4.0, 5.55))
    area_light('fill', (0, 1.0, 5.9), (0, 0, 0), (6.5, 8.0), (0.26, 0.36, 1.0), 600)
    area_light('fillc', (0.0, -3.3, 2.0), (math.pi / 2, 0, 0), (6.5, 4.0), (0.26, 0.36, 1.0), 260)
    area_light('winfill', (0, 5.5, 2.6), (-math.pi / 2, 0, 0), (2.0, 3.4), (0.3, 0.42, 1.0), 160)
    for (loc, en) in [((0.0, 2.4, 4.8), 150), ((2.0, 2.2, 1.3), 35), ((-3.0, 3.7, 1.95), 45), ((-2.1, 5.15, 2.45), 30), ((2.1, 5.15, 2.45), 30), ((2.35, 0.25, 1.1), 20)]: point_light('flamep', loc, (1.0, 0.66, 0.3), en, 0.05)

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

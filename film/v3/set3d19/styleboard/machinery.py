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


"""set3d16 style board: Morse telegraph line 1843-44 (Maryland / Washington). Self-contained bpy scene (procedural geometry + shaders), Cycles CPU.
usage: python3 sb.py line|chamber|close|all [draft]   -> sb1_line_wide.jpg / sb2_chamber.jpg / sb3_bottle_close.jpg (d_*.jpg for draft)
World units: metres. +x right, +y away from camera, z up. Camera 22 mm / 36 mm sensor (AUTO fit), 720x1280, no DOF.
Look: one hard key (sun) with real cast shadows, blue-violet sky ambient, painterly two-tone noise materials. No text anywhere."""
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
def prism_roof(mb, m, x0, x1, y0, y1, z0, zr, ov=0.0, ridge='x'):
    """gable roof from eave z0 to ridge zr, ridge along x (or y). thickness via extra underside quad."""
    if ridge == 'x':
        ym = (y0 + y1) / 2
        mb.quad(m, [(x0 - ov, y0 - ov, z0 - 0.15), (x1 + ov, y0 - ov, z0 - 0.15), (x1 + ov, ym, zr), (x0 - ov, ym, zr)])
        mb.quad(m, [(x0 - ov, ym, zr), (x1 + ov, ym, zr), (x1 + ov, y1 + ov, z0 - 0.15), (x0 - ov, y1 + ov, z0 - 0.15)])
        mb.quad(m, [(x0 - ov, y0 - ov, z0 - 0.15), (x0 - ov, ym, zr), (x0 - ov, y1 + ov, z0 - 0.15)][:3] + [(x0 - ov, ym, zr - 0.02)]) if False else None
    else:
        xm = (x0 + x1) / 2
        mb.quad(m, [(x0 - ov, y0 - ov, z0 - 0.15), (xm, y0 - ov, zr), (xm, y1 + ov, zr), (x0 - ov, y1 + ov, z0 - 0.15)][::-1])
        mb.quad(m, [(xm, y0 - ov, zr), (x1 + ov, y0 - ov, z0 - 0.15), (x1 + ov, y1 + ov, z0 - 0.15), (xm, y1 + ov, zr)][::-1])

# ------------------------------------------------------------------ materials
def palette(mode):
    d = {}
    wet = mode == 'close'
    d['pole'] = mat('pole', '#c98a46', '#e8ac66', 7, aniso=(1, 1, 0.12), contrast=1.3) if not wet else \
        mat('pole_wet', '#b07440', '#d09050', 7, aniso=(1, 1, 0.12), contrast=1.4, rough=0.45, sheen=0.35, zgrad=(0.5, 3.4, '#7a4a28'))
    d['polecut'] = mat('polecut', '#efd49a', '#e0b878', 3)
    d['wood'] = mat('wood', '#78461f', '#9a6230', 6, aniso=(1, 1, 0.3), contrast=1.5)
    d['woodpale'] = mat('woodpale', '#c8883c', '#e0a856', 8, aniso=(0.4, 1, 1), contrast=1.4)
    d['walnut'] = mat('walnut', '#6a3a1c', '#8e5430', 7, aniso=(1, 0.3, 0.3), contrast=1.6, rough=0.45, sheen=0.4)
    d['glass'] = mat('glass', '#2a9a68', '#5fd09e', 4, rough=0.1, sheen=1.0, emit='#35b880', emit_k=0.5)
    d['glassjar'] = mat('glassjar', '#7ac4a8', '#a6e0c8', 4, rough=0.1, sheen=1.0, emit='#6ad0a8', emit_k=0.3)
    d['wiremat'] = mat('wiremat', '#2a221e', '#4a3c32', 3, rough=0.35, sheen=0.6)
    d['drop'] = mat('drop', '#e0f0ff', '#ffffff', 2, rough=0.05, sheen=1.0, emit='#d8ecff', emit_k=1.2)
    d['road'] = mat('road', '#bc7e3e', '#d49a58', 3.0, aniso=(1.2, 0.35, 1.0), contrast=1.4) if not wet else mat('road_w', '#7e4a2c', '#9c6038', 3.0, aniso=(1.2, 0.35, 1.0), rough=0.25, sheen=0.7)
    d['rut'] = mat('rut', '#966030', '#b27a40', 4.0, aniso=(2, 0.3, 1))
    d['verge'] = mat('verge', '#7fa63a', '#c4b042', 4.0, aniso=(1.4, 0.4, 1))
    d['earth'] = mat('earth', '#8c5233', '#b06c44', 6, contrast=1.3)
    d['ballast'] = mat('ballast', '#9a8e86', '#c0aea0', 14, contrast=1.8)
    d['sleeper'] = mat('sleeper', '#4a3426', '#6a4a34', 5)
    d['rail'] = mat('rail', '#7a6058', '#a88c80', 3, rough=0.4, sheen=0.6)
    d['lead'] = mat('lead', '#8c929c', '#b6bcc6', 3, rough=0.35, sheen=0.7)
    d['straw'] = mat('straw', '#d6b25a', '#eccb78', 7, contrast=1.3)
    d['strawdk'] = mat('strawdk', '#b08a3c', '#d0a850', 7)
    d['wheat'] = mat('wheat', '#d6a838', '#f4cc58', 6, zgrad=(0.0, 0.5, '#9a9a34'), contrast=1.4)
    d['hay'] = mat('hay', '#c8a248', '#e8c46c', 8, aniso=(1, 1, 0.3))
    d['leafA'] = mat('leafA', '#4f8a3a', '#8aa83e', 2.2, contrast=1.6)
    d['leafB'] = mat('leafB', '#8a9a2c', '#d0a838', 2.2, contrast=1.6)
    d['trunk'] = mat('trunk', '#4a3228', '#6d4a36', 5, aniso=(1, 1, 0.3))
    d['brick'] = mat('brick', '#a2402e', '#bf5a3e', 9, aniso=(1, 1, 0.5), contrast=1.4)
    d['plaster'] = mat('plaster', '#f0e2c2', '#e0cca0', 2.5)
    d['barnred'] = mat('barnred', '#8e3224', '#a84632', 5, aniso=(0.3, 1, 1))
    d['shingle'] = mat('shingle', '#5a4a48', '#7a6a66', 8, aniso=(1, 1, 0.6))
    d['roofred'] = mat('roofred', '#9a3a2c', '#b8523a', 9, aniso=(1, 1, 0.6))
    d['dark'] = mat('dark', '#241a1e', '#3a2a2a', 3)
    d['cream'] = mat('cream', '#f4ead0', '#e6d8b4', 3)
    d['green'] = mat('green', '#2f6a45', '#3f8a58', 4, rough=0.6, sheen=0.3)
    d['black'] = mat('black', '#222024', '#3a363c', 4, rough=0.6, sheen=0.3)
    d['brass'] = mat('brass', '#d7a23a', '#f2cf70', 4, rough=0.3, sheen=0.9)
    d['copper'] = mat('copper', '#b4602c', '#d88848', 4, rough=0.35, sheen=0.8, wave=(60, '#7a3c1c'))
    d['red'] = mat('red', '#a8332a', '#c8483a', 4, rough=0.6)
    d['carriage'] = mat('carriage', '#9a3a2e', '#b94c3a', 4, aniso=(0.4, 1, 1))
    d['carriage2'] = mat('carriage2', '#d9a642', '#ecc060', 4, aniso=(0.4, 1, 1))
    d['smoke'] = mat('smoke', '#f6ebe0', '#d8cce0', 2, emit='#fff0e0', emit_k=0.25)
    d['metal'] = mat('metal', '#9aa4b0', '#c0c8d0', 3, rough=0.4, sheen=0.5)
    d['rope'] = mat('rope', '#cfae74', '#a88650', 12)
    d['spool'] = mat('spool', '#a8602c', '#cc8040', 3, rough=0.35, sheen=0.8, wave=(90, '#5e3218'))
    d['bird'] = mat('bird', '#2a2428', '#3a3238', 2)
    # chamber
    d['floor'] = mat('floor', '#94592a', '#bf8040', 8, aniso=(1, 0.2, 1), contrast=1.6, rough=0.4, sheen=0.4)
    d['carpet'] = mat('carpet', '#78301e', '#8e3c28', 10, contrast=1.2)
    d['baize'] = mat('baize', '#2c8040', '#40a05a', 12)
    d['wall'] = mat('wall', '#f2e4c0', '#e4d0a0', 2.0, contrast=0.8)
    d['marble'] = mat('marble', '#f6ecd6', '#e8dcc0', 2.5, contrast=0.8)
    d['drape'] = mat('drape', '#a02a2a', '#c64440', 3, aniso=(0.4, 0.4, 3.0), contrast=1.5)
    d['gold'] = mat('gold', '#d4a840', '#f0cc68', 4, rough=0.3, sheen=0.8)
    d['leather'] = mat('leather', '#8a2a2a', '#a8403a', 6)
    d['paper'] = mat('paper', '#f6ecd2', '#e8dcc0', 6)
    d['ink'] = mat('ink', '#1c1a22', '#2c2a34', 3, rough=0.2, sheen=0.8)
    d['flame'] = mat_emit('flame', '#ffb84a', 22.0)
    d['hat'] = mat('hat', '#26201c', '#3a302a', 3, rough=0.5, sheen=0.5)
    d['globe'] = mat('globe', '#3c74b0', '#4f9a58', 3, contrast=2.0, rough=0.4, sheen=0.5)
    d['frame'] = mat('frame', '#c8962c', '#f0c858', 5, rough=0.3, sheen=0.8)
    d['paintsky'] = mat('paintsky', '#7aa8dc', '#e6b890', 1.2)
    d['paintgrn'] = mat('paintgrn', '#4a7a34', '#8a8a38', 2.0, contrast=1.6)
    d['paintdk'] = mat('paintdk', '#3a3a28', '#5a4a30', 2.0)
    d['shaft'] = shaft_mat()
    return d

def shaft_mat():
    m = bpy.data.materials.new('shaft'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    em.inputs['Color'].default_value = hexc('#ffe0a0'); em.inputs['Strength'].default_value = 5.0; mx.inputs[0].default_value = 0.05
    L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface']); MATS['shaft'] = m; return m

# ------------------------------------------------------------------ ground / sky extras
def ground_plane(P, z=0.0):
    me = bpy.data.meshes.new('ground'); bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=2, y_segments=2, size=P.get('gsize', 400)); bm.to_mesh(me)
    ob = bpy.data.objects.new('ground', me); ob.location = (0, 100, z); bpy.context.scene.collection.objects.link(ob)
    m = bpy.data.materials.new('ground'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); bs.inputs['Roughness'].default_value = P.get('grough', 1.0); bs.inputs['Specular IOR Level'].default_value = P.get('gspec', 0.0)
    tc = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping'); L(tc.outputs['Object'], mp.inputs[0])
    def noise(sc_, det, x=1, y=1):
        n = N('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = sc_; n.inputs['Detail'].default_value = det
        mm = N('ShaderNodeMapping'); mm.inputs['Scale'].default_value = (x, y, 1); L(tc.outputs['Object'], mm.inputs[0]); L(mm.outputs[0], n.inputs[0]); return n
    n1 = noise(0.06, 5); n2 = noise(0.5, 6); n3 = noise(5.0, 6, 1, 1)
    def ramp(n, a, b):
        r = N('ShaderNodeValToRGB'); L(n.outputs['Fac'], r.inputs[0]); r.color_ramp.elements[0].position = a; r.color_ramp.elements[1].position = b; return r
    c1 = N('ShaderNodeMix'); c1.data_type = 'RGBA'; c1.inputs[6].default_value = hexc(P['g1']); c1.inputs[7].default_value = hexc(P['g2']); L(ramp(n1, 0.4, 0.6).outputs[0], c1.inputs[0])
    c2 = N('ShaderNodeMix'); c2.data_type = 'RGBA'; L(c1.outputs[2], c2.inputs[6]); c2.inputs[7].default_value = hexc(P['g3']); L(ramp(n2, 0.45, 0.62).outputs[0], c2.inputs[0]); c2.inputs[0].default_value = 0.5
    c3 = N('ShaderNodeMix'); c3.data_type = 'RGBA'; c3.blend_type = 'MULTIPLY'; c3.inputs[0].default_value = 0.8; L(c2.outputs[2], c3.inputs[6])
    r3 = ramp(n3, 0.35, 0.65); r3.color_ramp.elements[0].color = (0.75, 0.75, 0.75, 1); r3.color_ramp.elements[1].color = (1.12, 1.12, 1.12, 1); L(r3.outputs[0], c3.inputs[7])
    L(c3.outputs[2], bs.inputs['Base Color']); L(bs.outputs[0], out.inputs['Surface']); ob.data.materials.append(m)

def hills(P):
    mb = MB('hills'); rr = rnd(3)
    for li, (yy, bh, amp, col) in enumerate(P['hills']):
        m = mat_emit('hill%d' % li, col, P['hill_k']); n = 100; xs = np.linspace(-500, 500, n); ph = [rr.uniform(0, 6) for _ in range(4)]
        hs = [bh + amp * (0.5 * math.sin(x / 60 + ph[0]) + 0.3 * math.sin(x / 25 + ph[1]) + 0.15 * math.sin(x / 10 + ph[2])) for x in xs]
        for i in range(n - 1): mb.quad(m, [(xs[i], yy, -5), (xs[i + 1], yy, -5), (xs[i + 1], yy, hs[i + 1]), (xs[i], yy, hs[i])])
    mb.finish()

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

def ribbon(mb, m, f, ys, w, z=0.02, off=0.0):
    """strip along +y following x=f(y); w = width (const or fn)"""
    prev = None
    for y in ys:
        ww = w(y) if callable(w) else w; x = f(y) + off
        cur = ((x - ww / 2, y, z), (x + ww / 2, y, z))
        if prev: mb.quad(m, [prev[0], prev[1], cur[1], cur[0]][::-1])
        prev = cur

def xc(y): return 0.8 + 0.012 * y          # road centre line

# ------------------------------------------------------------------ props: outdoors
def pole(mb, M, x, y, h=6.5, bs=2.2):
    mb.rod(M['pole'], (x, y, -0.2), (x + 0.03, y, h), 0.14, 0.085, 10, smooth=True)
    mb.cyl(M['polecut'], (x + 0.03, y, h + 0.02), 0.085, 0.04, 'z', 10)
    mb.rod(M['wood'], (x + 0.03, y, h), (x + 0.03, y, h + 0.14 * bs), 0.03 * bs / 2, 0.026 * bs / 2, 6)              # peg
    bottle(mb, M, (x + 0.03, y, h + 0.01), bs)
    return (x + 0.03, y, h + 0.235 * bs * 0.5 + 0.12 * bs * 0.5 + 0.1 * bs)

def bottle(mb, M, c, s=1.0):
    """inverted green bottle neck, mouth down; c = base (mouth) centre"""
    x, y, z = c; G = M['glass']
    prof = [(0.075, 0.0), (0.07, 0.05), (0.05, 0.10), (0.034, 0.16), (0.034, 0.2), (0.046, 0.205), (0.046, 0.24), (0.03, 0.25)]
    for (r0, z0), (r1, z1) in zip(prof[:-1], prof[1:]): mb.rod(G, (x, y, z + z0 * s), (x, y, z + z1 * s), r0 * s, r1 * s, 14, caps=False, smooth=True)
    mb.cyl(G, (x, y, z + 0.25 * s), 0.03 * s, 0.01 * s, 'z', 14)

def bottle_top(c, h, s): return (c[0], c[1], h + 0.255 * s + 0.012)

def wires(mb, M, tops, sag=0.45, r=0.022, birds=None):
    for a, b in zip(tops[:-1], tops[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1]); n = max(6, int(L / 0.6)); prev = None
        for i in range(n + 1):
            u = i / n; p = (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u - sag * 4 * u * (1 - u) * (L / 9.0))
            if prev: mb.rod(M['wiremat'], prev, p, r, r, 5, caps=False)
            prev = p

def wire_pt(a, b, u, sag):
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u - sag * 4 * u * (1 - u) * (L / 9.0))

def worm_fence(mb, M, pts, seg=3.0, rails=5):
    for (a, b) in zip(pts[:-1], pts[1:]):
        d = Vector((b[0] - a[0], b[1] - a[1], 0)); L = d.length; d.normalize(); nrm = Vector((-d.y, d.x, 0)); n = max(1, int(L / seg))
        P_ = [Vector((a[0], a[1], 0)) + d * (L * i / n) + nrm * (0.5 if i % 2 else -0.5) for i in range(n + 1)]
        for i in range(n):
            for k in range(rails):
                z0 = 0.14 + 0.27 * k + (0.04 if i % 2 else 0.0)
                mb.rod(M['wood'], P_[i] + Vector((0, 0, z0)), P_[i + 1] + Vector((0, 0, z0 + 0.03)), 0.05, 0.05, 6)
        for i in range(n + 1):
            for sgn in (-1, 1):
                q = P_[i] + nrm * sgn * 0.12; mb.rod(M['wood'], q + Vector((0, 0, 0.0)), q + Vector((d.x * sgn * 0.0, 0, 1.5)), 0.045, 0.04, 6)

def oak(mb, M, c, s=1.0, seed=0, A='leafA', B='leafB'):
    rr = rnd(seed); x, y, z = c
    mb.rod(M['trunk'], (x, y, z - 0.1), (x + rr.uniform(-.3, .3) * s, y, z + 3.0 * s), 0.35 * s, 0.22 * s, 8, smooth=True)
    for i in range(3):
        a = i * 2.1 + rr.random(); tp = (x + math.cos(a) * 1.3 * s, y + math.sin(a) * 1.3 * s, z + rr.uniform(4.0, 5.0) * s)
        mb.rod(M['trunk'], (x, y, z + 2.6 * s), tp, 0.2 * s, 0.1 * s, 7, smooth=True)
    for j in range(rr.randint(6, 9)):
        o = Vector((rr.uniform(-2.2, 2.2), rr.uniform(-2.2, 2.2), rr.uniform(3.7, 6.2))) * s
        mb.ell(M[A if rr.random() < 0.6 else B], (x + o.x, y + o.y, z + o.z), (rr.uniform(1.4, 2.2) * s, rr.uniform(1.4, 2.2) * s, rr.uniform(1.0, 1.5) * s), (12, 8), (0, 0, rr.random() * 6))

def stook(mb, M, c, rr, s=1.0):
    x, y, z = c
    mb.cyl(M['straw'], (x, y, z + 0.5 * s), 0.55 * s, 1.0 * s, 'z', 10, r2=0.45 * s)
    mb.cyl(M['strawdk'], (x, y, z + 1.3 * s), 0.46 * s, 0.6 * s, 'z', 10, r2=0.1 * s)
    mb.rod(M['rope'], (x, y, z + 1.0 * s), (x, y, z + 1.04 * s), 0.5 * s, 0.5 * s, 10, caps=False)
    for i in range(5):
        a = rr.random() * 6.28; mb.rod(M['straw'], (x + math.cos(a) * 0.3 * s, y + math.sin(a) * 0.3 * s, z + 1.5 * s), (x + math.cos(a) * 0.5 * s, y + math.sin(a) * 0.5 * s, z + 1.85 * s), 0.02 * s, 0.01 * s, 4)

def wheat_clump(mb, M, c, rr, h=0.9):
    x, y, z = c
    for i in range(6):
        a = rr.random() * 6.283; L = h * rr.uniform(0.8, 1.15); bend = rr.uniform(0.05, 0.25)
        d = Vector((math.cos(a), math.sin(a), 0)); sd = Vector((-d.y, d.x, 0)) * 0.02
        p0 = Vector((x + rr.uniform(-.08, .08), y + rr.uniform(-.08, .08), z)); p1 = p0 + d * bend * 0.4 + Vector((0, 0, L * 0.6)); p2 = p0 + d * bend + Vector((0, 0, L))
        mb.quad(M['wheat'], [p0 - sd * 1.2, p0 + sd * 1.2, p1 + sd * 0.8, p1 - sd * 0.8]); mb.tri(M['wheat'], [p1 - sd * 0.8, p1 + sd * 0.8, p2])

def grass_clump(mb, M, c, rr, h=0.9):
    x, y, z = c
    for i in range(6):
        a = rr.random() * 6.283; L = h * rr.uniform(0.6, 1.2); bend = rr.uniform(0.15, 0.5)
        d = Vector((math.cos(a), math.sin(a), 0)); sd = Vector((-d.y, d.x, 0)) * 0.025
        p0 = Vector((x, y, z)); p1 = p0 + d * bend * 0.4 + Vector((0, 0, L * 0.6)); p2 = p0 + d * bend + Vector((0, 0, L))
        mb.quad(M['verge'], [p0 - sd * 1.4, p0 + sd * 1.4, p1 + sd * 0.8, p1 - sd * 0.8]); mb.tri(M['verge'], [p1 - sd * 0.8, p1 + sd * 0.8, p2])

def farmhouse(mb, M, c, yaw=0.0):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    sx, sy, h = 9.0, 6.0, 5.0
    mb.box(M['plaster'], (0, 0, h / 2), (sx, sy, h)); mb.box(M['brick'], (0, 0, 0.3), (sx + 0.2, sy + 0.2, 0.6))
    prism_roof(mb, M['roofred'], -sx / 2, sx / 2, -sy / 2, sy / 2, h, h + 2.4, ov=0.6)
    for ex in (-sx / 2, sx / 2): mb.tri(M['plaster'], [(ex, -sy / 2, h), (ex, sy / 2, h), (ex, 0, h + 2.4)] if ex > 0 else [(ex, sy / 2, h), (ex, -sy / 2, h), (ex, 0, h + 2.4)])
    mb.box(M['brick'], (3.2, 0, h + 2.6), (1.0, 1.0, 3.0))
    for wx in (-3.0, -1.0, 1.2, 3.2):
        for wz in (1.4, 3.6):
            mb.box(M['cream'], (wx, -sy / 2 - 0.03, wz), (1.0, 0.1, 1.4)); mb.box(M['dark'], (wx, -sy / 2 - 0.08, wz), (0.8, 0.05, 1.2))
    mb.box(M['barnred'], (0.1, -sy / 2 - 0.06, 1.0), (1.2, 0.12, 2.0))
    mb.box(M['woodpale'], (0, -sy / 2 - 1.2, 0.2), (3.5, 2.0, 0.4)); mb.pop()

def barn(mb, M, c, yaw=0.0):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    sx, sy, h = 13.0, 9.0, 5.5
    mb.box(M['barnred'], (0, 0, h / 2), (sx, sy, h))
    prism_roof(mb, M['shingle'], -sx / 2, sx / 2, -sy / 2, sy / 2, h, h + 3.6, ov=0.5)
    for ex in (-sx / 2, sx / 2): mb.tri(M['barnred'], [(ex, -sy / 2, h), (ex, sy / 2, h), (ex, 0, h + 3.6)] if ex > 0 else [(ex, sy / 2, h), (ex, -sy / 2, h), (ex, 0, h + 3.6)])
    mb.box(M['dark'], (0, -sy / 2 - 0.05, 2.0), (3.6, 0.1, 4.0)); mb.box(M['cream'], (-1.9, -sy / 2 - 0.07, 2.0), (0.2, 0.12, 4.2)); mb.box(M['cream'], (1.9, -sy / 2 - 0.07, 2.0), (0.2, 0.12, 4.2)); mb.box(M['cream'], (0, -sy / 2 - 0.07, 4.05), (4.0, 0.12, 0.2))
    mb.box(M['dark'], (0, -sy / 2 - 0.05, h + 1.6), (1.0, 0.1, 1.0))
    mb.pop()

def crate(mb, M, c, s=(0.8, 0.6, 0.55), yaw=0.0):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M['woodpale'], (0, 0, s[2] / 2), s)
    for sx in (-1, 1): mb.box(M['wood'], (sx * (s[0] / 2 - 0.04), 0, s[2] / 2), (0.08, s[1] + 0.04, s[2] + 0.04))
    mb.box(M['wood'], (0, 0, s[2]), (s[0] + 0.02, 0.07, 0.04)); mb.box(M['wood'], (0, s[1] / 2, s[2] / 2), (s[0] + 0.02, 0.04, 0.07))
    mb.pop()

def barrel(mb, M, c, h=0.9, r=0.38):
    x, y, z = c
    mb.cyl(M['woodpale'], (x, y, z + h / 2), r, h, 'z', 14, True, r2=r)
    mb.cyl(M['woodpale'], (x, y, z + h / 2), r * 1.12, h * 0.5, 'z', 14, True, r2=r * 1.12)
    for k in (0.15, 0.85): mb.cyl(M['metal'], (x, y, z + h * k), r * 1.07 if 0.2 < k < 0.8 else r * 1.0, 0.05, 'z', 14)

def wheel(mb, M, c, r, thick=0.06, spokes=8):
    x, y, z = c
    mb.cyl(M['wood'], (x, y, z), r * 0.12, thick * 2.6, 'y', 10)
    for i in range(spokes):
        a = i * math.pi * 2 / spokes
        mb.rod(M['wood'], (x, y, z), (x + math.cos(a) * r * 0.94, y, z + math.sin(a) * r * 0.94), thick * 0.45, thick * 0.35, 5)
    for i in range(16):
        a = i * math.pi * 2 / 16; b = (i + 1) * math.pi * 2 / 16
        mb.rod(M['wood'], (x + math.cos(a) * r, y, z + math.sin(a) * r), (x + math.cos(b) * r, y, z + math.sin(b) * r), thick * 0.75, thick * 0.75, 5)
        mb.rod(M['metal'], (x + math.cos(a) * (r + 0.02), y, z + math.sin(a) * (r + 0.02)), (x + math.cos(b) * (r + 0.02), y, z + math.sin(b) * (r + 0.02)), thick * 0.5, thick * 0.5, 4)

def wagon(mb, M, c, yaw=0.0):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    # long axis = local x; bed
    mb.box(M['woodpale'], (0, 0, 0.95), (3.6, 1.6, 0.12))
    for sy in (-1, 1): mb.box(M['wood'], (0, sy * 0.8, 1.25), (3.6, 0.07, 0.5))
    for sx in (-1, 1): mb.box(M['wood'], (sx * 1.8, 0, 1.25), (0.07, 1.6, 0.5))
    for sx in (-1.2, 1.2):
        mb.box(M['wood'], (sx, 0, 0.8), (0.12, 1.9, 0.12))
        for sy in (-1, 1): wheel(mb, M, (sx, sy * 0.95, 0.62 if sx < 0 else 0.5), 0.62 if sx < 0 else 0.5)
    mb.rod(M['wood'], (1.8, 0, 0.85), (4.6, 0, 0.45), 0.06, 0.05, 6)                                    # tongue
    # big wire spool lying on its side along x: two flanges + core + wrapped wire
    z0 = 1.95
    mb.cyl(M['woodpale'], (-0.2, 0, z0), 0.78, 0.08, 'y', 22) if False else None
    for sy in (-0.52, 0.52): mb.cyl(M['woodpale'], (-0.2, sy, z0 - 0.1), 0.85, 0.1, 'y', 24)
    mb.cyl(M['spool'], (-0.2, 0, z0 - 0.1), 0.66, 0.96, 'y', 24, True)
    mb.cyl(M['wood'], (-0.2, 0, z0 - 0.1), 0.15, 1.3, 'y', 10)
    mb.cyl(M['woodpale'], (-0.2, 0, z0 - 0.1), 0.2, 0.0 + 1.14, 'y', 10) if False else None
    # loose wire end hanging off the spool
    mb.rod(M['wiremat'], (-0.2, -0.3, z0 - 0.1 + 0.66), (0.5, -0.3, 1.2), 0.02, 0.02, 4)
    # crates on bed
    crate(mb, M, (1.2, 0.35, 1.0), (0.7, 0.6, 0.5), 0.2); crate(mb, M, (1.25, -0.35, 1.0), (0.6, 0.5, 0.45), -0.1); crate(mb, M, (1.2, 0.2, 1.5), (0.5, 0.45, 0.4), 0.5)
    # ladders lying along the side
    for sy in (-1.2, 1.2) if False else ():
        pass
    mb.pop()

def ladder(mb, M, p0, p1, w=0.45, n=9):
    p0 = Vector(p0); p1 = Vector(p1); d = (p1 - p0); side = Vector((-d.y, d.x, 0)).normalized() * w / 2 if abs(d.x) + abs(d.y) > 1e-3 else Vector((w / 2, 0, 0))
    for sg in (-1, 1): mb.rod(M['wood'], p0 + side * sg, p1 + side * sg, 0.032, 0.03, 6)
    for i in range(n):
        u = (i + 0.5) / n; q = p0 + d * u; mb.rod(M['woodpale'], q - side, q + side, 0.02, 0.02, 5)

def pick(mb, M, c, yaw=0.0):
    x, y, z = c
    dx, dy = math.cos(yaw), math.sin(yaw)
    mb.rod(M['woodpale'], (x, y, z + 0.04), (x + dx * 1.0, y + dy * 1.0, z + 0.09), 0.03, 0.025, 6)
    ex, ey = x + dx * 1.0, y + dy * 1.0
    mb.rod(M['metal'], (ex - dy * 0.22, ey + dx * 0.22, z + 0.09), (ex + dy * 0.22, ey - dx * 0.22, z + 0.09), 0.03, 0.012, 5)

def shovel(mb, M, c, yaw=0.0):
    x, y, z = c; dx, dy = math.cos(yaw), math.sin(yaw)
    mb.rod(M['woodpale'], (x, y, z + 0.05), (x + dx * 1.1, y + dy * 1.1, z + 0.25), 0.03, 0.025, 6)
    mb.box(M['metal'], (x + dx * 1.25, y + dy * 1.25, z + 0.28), (0.3, 0.22, 0.03), rz=yaw)

def loco(mb, M, c, yaw=0.0, s=1.0):
    """1840s tank loco facing +x local; track gauge along y"""
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Diagonal((s, s, s, 1)))
    mb.box(M['black'], (0.4, 0, 0.95), (4.4, 1.5, 0.3))                                                    # frame
    mb.cyl(M['green'], (0.8, 0, 1.75), 0.72, 3.2, 'x', 20, True)                                           # boiler
    mb.cyl(M['brass'], (0.8, 0, 1.75), 0.76, 0.1, 'x', 20)                                                  # bands
    for bx in (-0.4, 0.6, 1.6): mb.cyl(M['brass'], (bx, 0, 1.75), 0.74, 0.08, 'x', 20)
    mb.cyl(M['black'], (2.5, 0, 1.75), 0.7, 0.6, 'x', 20, True)                                             # smokebox
    mb.cyl(M['black'], (2.82, 0, 1.75), 0.52, 0.06, 'x', 20)
    mb.cyl(M['brass'], (2.86, 0, 1.75), 0.26, 0.05, 'x', 14)
    mb.cyl(M['black'], (2.45, 0, 3.1), 0.2, 1.7, 'z', 14, True, r2=0.34)                                    # tall funnel stack
    mb.cyl(M['brass'], (2.45, 0, 3.98), 0.37, 0.08, 'z', 14)
    mb.ell(M['brass'], (1.0, 0, 2.55), (0.32, 0.32, 0.4), (14, 10)); mb.cyl(M['brass'], (1.0, 0, 2.2), 0.14, 0.4, 'z', 10)           # dome
    mb.cyl(M['brass'], (1.8, 0, 2.58), 0.13, 0.5, 'z', 10); mb.ell(M['brass'], (1.8, 0, 2.86), (0.15, 0.15, 0.1), (8, 6))             # whistle/valve
    mb.box(M['red'], (-1.35, 0, 1.9), (1.4, 1.5, 1.6)); mb.box(M['red'], (-1.35, 0, 2.7), (1.7, 1.8, 0.14))                          # cab
    mb.box(M['dark'], (-1.35, 0.76, 2.0), (0.8, 0.04, 0.6)); mb.box(M['dark'], (-1.35, -0.76, 2.0), (0.8, 0.04, 0.6))
    for sy in (-0.7, 0.7):
        for wx in (-1.5, 0.1):
            mb.cyl(M['red'], (wx, sy * 1.07, 0.7), 0.7, 0.1, 'y', 20); mb.cyl(M['black'], (wx, sy * 1.07, 0.7), 0.5, 0.12, 'y', 16); mb.cyl(M['brass'], (wx, sy * 1.07, 0.7), 0.1, 0.16, 'y', 8)
        for wx in (1.5, 2.3):
            mb.cyl(M['red'], (wx, sy * 1.07, 0.45), 0.45, 0.1, 'y', 16); mb.cyl(M['black'], (wx, sy * 1.07, 0.45), 0.3, 0.12, 'y', 12)
        mb.rod(M['metal'], (-1.5, sy * 1.2, 0.7), (1.0, sy * 1.2, 0.95), 0.04, 0.04, 5)                                                # rods
        mb.cyl(M['black'], (1.5, sy * 0.85, 1.05), 0.14, 1.0, 'x', 10)                                                                # cylinders
    mb.box(M['black'], (3.1, 0, 0.7), (0.3, 1.9, 0.3))                                                      # buffer beam
    mb.cyl(M['brass'], (3.25, 0, 2.15), 0.18, 0.2, 'x', 10); mb.cyl(M['gold'], (3.37, 0, 2.15), 0.14, 0.04, 'x', 10)  # lamp
    # cowcatcher: wedge of slats
    for i in range(7):
        yy = -0.85 + i * 0.283; mb.rod(M['black'], (3.1, yy * 0.8, 0.65), (4.1, yy * 1.05, 0.2), 0.045, 0.04, 5)
    mb.rod(M['black'], (3.1, -0.8, 0.62), (4.1, -0.9, 0.2), 0.05, 0.05, 5); mb.rod(M['black'], (3.1, 0.8, 0.62), (4.1, 0.9, 0.2), 0.05, 0.05, 5)
    mb.rod(M['black'], (4.1, -0.9, 0.2), (4.1, 0.9, 0.2), 0.05, 0.05, 5)
    mb.pop()

def carriage(mb, M, c, yaw=0.0, body='carriage', L=5.4, s=1.0):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Diagonal((s, s, s, 1)))
    mb.box(M['black'], (0, 0, 0.8), (L, 1.7, 0.25)); mb.box(M[body], (0, 0, 1.95), (L, 2.2, 2.0)); mb.box(M['cream'], (0, 0, 1.2), (L + 0.04, 2.24, 0.12)); mb.box(M['cream'], (0, 0, 2.95), (L + 0.04, 2.24, 0.1))
    prism_roof(mb, M['dark'], -L / 2, L / 2, -1.1, 1.1, 3.0, 3.5, ov=0.15)
    for i in range(5):
        wx = -L / 2 + 0.7 + i * (L - 1.4) / 4
        for sy in (-1, 1): mb.box(M['dark'], (wx, sy * 1.11, 2.1), (0.7, 0.04, 0.8)); mb.box(M['cream'], (wx, sy * 1.12, 2.1), (0.82, 0.03, 0.92))
    for sy in (-1, 1):
        for wx in (-1.8, 1.8): mb.cyl(M['red'], (wx, sy * 0.95, 0.5), 0.5, 0.08, 'y', 16); mb.cyl(M['black'], (wx, sy * 0.95, 0.5), 0.32, 0.1, 'y', 12)
    mb.pop()

def puff(mb, M, p, r):
    mb.ell(M['smoke'], p, (r, r, r * 0.9), (14, 10))

def build_line(mode, P):
    sc = bpy.context.scene; M = palette(mode); MB_ = MB
    sky_world(P); hills(P); clouds(P); ground_plane(P, 0.0)
    ys = [float(i) for i in np.arange(-14, 130, 1.0)]
    mb = MB('roads')
    ribbon(mb, M['verge'], xc, ys, 6.5, 0.01); ribbon(mb, M['road'], xc, ys, 3.0, 0.03)
    ribbon(mb, M['rut'], xc, ys, 0.3, 0.04, -0.6); ribbon(mb, M['rut'], xc, ys, 0.3, 0.04, 0.6); ribbon(mb, M['verge'], xc, ys, 0.35, 0.045, 0.0)
    tx = P['tx']                                              # railway x
    ribbon(mb, M['ballast'], lambda y: tx, ys, 3.4, 0.04)
    for y in np.arange(-14, 130, 0.85): mb.box(M['sleeper'], (tx, y, 0.12), (2.2, 0.26, 0.14))
    for sx in (-0.72, 0.72):
        for y in np.arange(-14, 130, 4.0): mb.rod(M['rail'], (tx + sx, y, 0.26), (tx + sx, y + 4.0, 0.26), 0.05, 0.05, 6) if False else mb.box(M['rail'], (tx + sx, y + 2.0, 0.24), (0.1, 4.02, 0.16))
    # trench with lead pipe (right of road) + spoil heap
    for y0 in range(-2, 62, 4):
        xt = xc(y0 + 2) + 2.3
        mb.box(M['dark'], (xt, y0 + 2, 0.03), (0.75, 4.0, 0.04)); mb.box(M['earth'], (xt + 0.65, y0 + 2, 0.12), (0.5, 4.0, 0.22)); mb.box(M['earth'], (xt - 0.55, y0 + 2, 0.08), (0.3, 4.0, 0.14))
        mb.rod(M['lead'], (xt, y0 - 0.05, 0.14), (xt, y0 + 3.9, 0.14), 0.09, 0.09, 10, smooth=True)
    for y0 in (-1.0, 14.0, 30.0):
        for i in range(5): mb.ell(M['earth'], (xc(y0) + 3.4 + i * 0.4, y0 + i * 0.2, 0.15), (0.55, 0.45, 0.28), (8, 6))
    # rolled lead-pipe coil on the verge
    for k in range(4): mb.cyl(M['lead'], (xc(2.0) + 1.7, 1.0, 0.1 + k * 0.17), 0.55, 0.15, 'z', 18, True) if False else None
    mb.finish()
    # --- telegraph poles
    mb = MB('poles'); tops = []; pyy = [4.0 + 9.0 * k for k in range(9)]; bs = P['bottle_s']
    for y in pyy:
        x = xc(y) + 3.4; h = P.get('pole_h', 6.5)
        pole(mb, M, x, y, h, bs); tops.append((x + 0.03, y, h + 0.255 * bs + 0.012))
    wires(mb, M, tops, sag=P.get('sag', 0.5), r=P.get('wire_r', 0.024))
    # birds on wire
    rb = rnd(4)
    for (i, u) in [(1, 0.35), (1, 0.5), (2, 0.6), (3, 0.3), (3, 0.38), (4, 0.5)]:
        p = wire_pt(tops[i], tops[i + 1], u, P.get('sag', 0.5)); mb.ell(M['bird'], (p[0], p[1], p[2] + 0.12), (0.1, 0.18, 0.1), (8, 5)); mb.ell(M['bird'], (p[0], p[1] - 0.15, p[2] + 0.2), (0.06, 0.06, 0.06), (6, 4))
    mb.finish()
    # --- droplets (wet look)
    if P.get('drops'):
        mb = MB('drops'); rd = rnd(12)
        for i in range(0, 3):
            for k in range(8):
                u = rd.uniform(0.05, 0.95); p = wire_pt(tops[i], tops[i + 1], u, P.get('sag', 0.5)); r_ = rd.uniform(0.022, 0.04) * P['drops']
                mb.ell(M['drop'], (p[0], p[1] + rd.uniform(-0.03, 0.03), p[2] - r_ * 1.1), (r_, r_, r_ * 1.25), (8, 6))
        t0 = tops[0]
        for k in range(10):
            a = rd.random() * 6.28; hh = rd.uniform(0.02, 0.2) * bs; rr_ = 0.06 * bs * (1 - hh / (0.25 * bs) * 0.4)
            mb.ell(M['drop'], (t0[0] + math.cos(a) * rr_, t0[1] + math.sin(a) * rr_, t0[2] - 0.255 * bs + hh), (0.018 * P['drops'],) * 3, (8, 6))
        mb.finish()
    # --- wagon + props
    mb = MB('work')
    P_ = P.get('wagon', (-2.6, 9.5)); wagon(mb, M, (P_[0], P_[1], 0.0), 1.45)
    ladder(mb, M, (xc(8) + 4.3, 6.3, 0.0), (xc(8) + 3.6, 6.1, P.get('pole_h', 6.5) - 0.3), 0.5, 14)                           # ladder leaning on pole 1
    ladder(mb, M, (-3.0, 1.0, 0.08), (-3.2, 5.2, 0.1), 0.5, 10)                                          # ladder on the ground
    for (x, y, yw) in [(xc(3) + 3.0, 1.0, 0.2), (xc(3) + 3.8, 3.0, 0.9), (xc(7) + 4.0, 8.0, -0.4)]: pick(mb, M, (x, y, 0.15), yw)
    for (x, y, yw) in [(xc(5) + 4.4, 5.0, 1.3), (xc(12) + 3.6, 12.0, 0.3)]: shovel(mb, M, (x, y, 0.05), yw)
    crate(mb, M, (xc(10) + 1.9, 7.2, 0.0), (0.8, 0.6, 0.55), 0.3); crate(mb, M, (xc(10) + 2.1, 8.0, 0.0), (0.7, 0.55, 0.5), -0.2)
    crate(mb, M, (xc(10) + 2.0, 7.6, 0.55), (0.6, 0.5, 0.45), 0.6)
    barrel(mb, M, (xc(12) + 1.9, 11.0, 0.0)); barrel(mb, M, (xc(12) + 2.5, 11.4, 0.0))
    # spare spool on end + wire coil, near the first pole
    mb.cyl(M['woodpale'], (xc(2) + 2.0, -0.2, 0.05), 0.55, 0.1, 'z', 20); mb.cyl(M['woodpale'], (xc(2) + 2.0, -0.2, 0.62), 0.55, 0.1, 'z', 20); mb.cyl(M['spool'], (xc(2) + 2.0, -0.2, 0.33), 0.42, 0.5, 'z', 20, True)
    for (x, y) in [(-1.0, 12.6), (-0.4, 13.3)]: crate(mb, M, (x, y, 0.0), (0.7, 0.55, 0.5), 0.4)
    P_f = P.get('fgprop')
    if P_f: crate(mb, M, P_f, (1.0, 0.8, 0.7), 0.35); crate(mb, M, (P_f[0] + 1.0, P_f[1] + 0.2, 0.0), (0.7, 0.6, 0.5), -0.3)
    mb.finish()
    # --- fences (split-rail)
    mb = MB('fences')
    worm_fence(mb, M, [(xc(y) - 2.6, y) for y in (6, 20, 40, 62, 85)] if P.get('lfence') else [(xc(y) - 3.0, y) for y in (12, 40, 62, 85)], seg=3.2)
    worm_fence(mb, M, [(xc(y) + 7.5, y) for y in (6, 24, 46, 70, 100)], seg=3.2)
    worm_fence(mb, M, [(-6.0, 40), (-6.0, 80)], seg=3.2) if False else None
    mb.finish()
    # --- fields: wheat (right) + stooks, grass/verge
    mb = MB('wheat'); rw = rnd(21)
    for i in range(P.get('nwheat', 3200)):
        y = rw.uniform(4, 75); x = rw.uniform(xc(y) + 8.4, xc(y) + 34)
        wheat_clump(mb, M, (x, y, 0.0), rw, rw.uniform(0.75, 1.05))
    mb.finish()
    mb = MB('stooks'); rs = rnd(22)
    for row in range(5):
        for i in range(9):
            y = 8 + i * 6.5 + row * 1.3 + rs.uniform(-.5, .5); x = xc(y) + 11 + row * 4.2 + rs.uniform(-.4, .4)
            stook(mb, M, (x, y, 0.0), rs, rs.uniform(0.9, 1.2) * (1 + y * 0.004))
    for i in range(7):
        y = 12 + i * 8 + rs.uniform(-2, 2); x = xc(y) - 7.5 + rs.uniform(-1, 1)
        stook(mb, M, (x, y, 0.0), rs, 1.1)
    # round hay ricks near farm
    for (x, y) in [(10.0, 70.0), (26.0, 64.0)]:
        mb.cyl(M['hay'], (x, y, 1.0), 2.0, 2.0, 'z', 16, True); mb.cyl(M['strawdk'], (x, y, 2.4), 1.8, 1.0, 'z', 16, True, r2=0.2)
    mb.finish()
    mb = MB('verge'); rg = rnd(23)
    for i in range(P.get('ngrass', 1100)):
        y = rg.uniform(-10, 100); side = rg.choice((-1, 1)); x = xc(y) + side * rg.uniform(2.4, 5.0)
        if side > 0 and x < xc(y) + 5.0 and rg.random() < 0.5: continue
        if abs(x - tx) < 2.2: continue
        grass_clump(mb, M, (x, y, 0.0), rg, rg.uniform(0.5, 1.1))
    for i in range(500):
        y = rg.uniform(-10, 70); x = rg.uniform(-9, -2.5) if rg.random() < 0.6 else rg.uniform(-30, -13)
        if abs(x - tx) < 2.4 or abs(x - (xc(y) - 2.6)) < 0.8: continue
        wheat_clump(mb, M, (x, y, 0.0), rg, rg.uniform(0.5, 0.9))
    mb.finish()
    # --- trees + farm
    mb = MB('trees'); rt = rnd(24)
    for (x, y, s_) in [(-30, 44, 1.6), (-34, 58, 1.8), (-24, 76, 1.6), (22, 40, 1.5), (30, 28, 1.3), (36, 60, 1.8), (-34, 30, 1.6), (4, 92, 1.8), (-8, 100, 1.9), (46, 76, 2.0), (-44, 70, 2.1), (16, 110, 2.0), (-24, 100, 2.2), (30, 104, 2.2)]:
        oak(mb, M, (x, y, 0.0), s_, int(x * 7 + y)); 
    for (yy, ss) in [(13, 1.5), (23, 1.7), (33, 1.6), (46, 1.8)]: oak(mb, M, (xc(yy) + 9.6, yy, 0.0), ss, int(yy * 3))
    mb.finish()
    mb = MB('farm'); farmhouse(mb, M, (20.0, 86.0, 0.0), 0.08); barn(mb, M, (-12.0, 96.0, 0.0), -0.05)
    mb.rod(M['trunk'], (4.0, 92, 0), (4.0, 92, 0.1), 0.01, 0.01, 4)
    mb.finish()
    # --- railway scene: loco + 2 carriages (loco facing -y toward camera side)
    mb = MB('train')
    ly = P.get('loco_y', 30.0); yaw = -math.pi / 2; LS = 1.6          # local +x -> world -y
    loco(mb, M, (tx, ly, 0.2), yaw, LS)
    carriage(mb, M, (tx, ly + 7.2 * LS, 0.2), yaw, 'carriage', 5.4, LS); carriage(mb, M, (tx, ly + 13.4 * LS, 0.2), yaw, 'carriage2', 5.4, LS)
    mb.rod(M['black'], (tx, ly + 3.6 * LS, 0.95), (tx, ly + 4.6 * LS, 0.95), 0.06, 0.06, 5); mb.rod(M['black'], (tx, ly + 9.9 * LS, 0.95), (tx, ly + 10.7 * LS, 0.95), 0.06, 0.06, 5)
    sy_ = ly - 2.45 * LS                                              # funnel position
    for i, (dx, dy, dz, r) in enumerate([(0.0, 0.0, 5.3, 0.6), (0.6, 0.6, 6.4, 0.9), (1.6, 1.6, 7.8, 1.2), (3.0, 3.0, 9.3, 1.55), (4.8, 4.6, 10.9, 1.9), (7.0, 6.4, 12.6, 2.3), (9.6, 8.2, 14.4, 2.6)]):
        puff(mb, M, (tx + 0.4 + dx * 1.3, sy_ + dy * 1.4, dz), r)
    mb.finish()
    # --- dense foreground near the lens: tall grass tufts, spool, wire coil, tools
    mb = MB('fg'); rf = rnd(31)
    for i in range(420 if mode == 'line' else 0):
        x = rf.choice((-1, 1)) * rf.uniform(1.6, 5.5) + xc(0); y = rf.uniform(-5.2, 4.5)
        if abs(x - xc(y)) < 1.6: continue
        grass_clump(mb, M, (x, y, 0.0), rf, rf.uniform(0.9, 1.7)) if rf.random() < 0.6 else wheat_clump(mb, M, (x, y, 0.0), rf, rf.uniform(0.9, 1.4))
    for i in range(70 if mode == 'line' else 0):
        x = rf.uniform(0.2, 2.2) + (rf.random() < 0.5) * 0; y = rf.uniform(-5.0, -1.0)
        if rf.random() < 0.5: grass_clump(mb, M, (x + 2.0 * (rf.random() < 0.5), y, 0.0), rf, rf.uniform(0.5, 0.9))
    sp = P.get('fgspool', (-2.3, -4.0))
    mb.cyl(M['woodpale'], (sp[0], sp[1], 0.05), 0.62, 0.1, 'z', 22); mb.cyl(M['woodpale'], (sp[0], sp[1], 0.7), 0.62, 0.1, 'z', 22); mb.cyl(M['spool'], (sp[0], sp[1], 0.38), 0.46, 0.6, 'z', 22, True)
    mb.rod(M['wiremat'], (sp[0] + 0.45, sp[1], 0.5), (sp[0] + 1.3, sp[1] + 0.3, 0.02), 0.02, 0.02, 5)
    cp = P.get('fgcoil', (1.8, -3.6))
    for k in range(3): mb.cyl(M['wiremat'], (cp[0], cp[1], 0.08 + k * 0.12), 0.6, 0.1, 'z', 22, True); mb.cyl(M['dark'], (cp[0], cp[1], 0.08 + k * 0.12), 0.26, 0.12, 'z', 14)
    pick(mb, M, (0.5, -3.9, 0.15), 0.5); shovel(mb, M, (1.0, -4.8, 0.05), 2.4); pick(mb, M, (-1.0, -2.5, 0.15), -0.4)
    mb.finish()

# ------------------------------------------------------------------ chamber
def telegraph(mb, M, c, s=1.7, yaw=0.0):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Diagonal((s, s, s, 1)))
    mb.box(M['walnut'], (0, 0, 0.03), (0.95, 0.42, 0.06)); mb.box(M['walnut'], (0, 0, 0.075), (0.9, 0.38, 0.03))
    # electromagnet: base plate, two coils, yoke, armature lever
    mb.box(M['brass'], (-0.22, 0.0, 0.1), (0.3, 0.2, 0.025))
    for sy in (-0.06, 0.06):
        mb.cyl(M['copper'], (-0.22, sy, 0.2), 0.045, 0.16, 'z', 16, True); mb.cyl(M['brass'], (-0.22, sy, 0.285), 0.05, 0.015, 'z', 16); mb.cyl(M['brass'], (-0.22, sy, 0.118), 0.05, 0.015, 'z', 16)
    mb.box(M['metal'], (-0.22, 0, 0.31), (0.08, 0.2, 0.02))
    mb.rod(M['brass'], (-0.35, 0, 0.335), (0.0, 0, 0.36), 0.01, 0.01, 6)                                         # armature lever
    mb.box(M['brass'], (-0.35, 0, 0.32), (0.025, 0.08, 0.06)); mb.ell(M['brass'], (-0.35, 0, 0.345), (0.018, 0.018, 0.018), (8, 6))
    # lever key on its own block, front right
    mb.box(M['walnut'], (0.18, -0.12, 0.1), (0.22, 0.1, 0.03)); mb.box(M['brass'], (0.2, -0.12, 0.125), (0.14, 0.03, 0.02))
    mb.rod(M['brass'], (0.12, -0.12, 0.14), (0.3, -0.12, 0.16), 0.01, 0.01, 6); mb.ell(M['black'], (0.3, -0.12, 0.17), (0.028, 0.028, 0.025), (10, 6)) if False else mb.ell(M['dark'], (0.31, -0.12, 0.172), (0.03, 0.03, 0.026), (10, 6))
    # paper-tape register: housing + spool + tape
    mb.box(M['wood'], (0.18, 0.1, 0.12), (0.32, 0.2, 0.1)); mb.cyl(M['paper'], (0.1, 0.1, 0.24), 0.08, 0.1, 'y', 20)
    mb.cyl(M['brass'], (0.1, 0.1, 0.24), 0.02, 0.16, 'y', 10); mb.cyl(M['brass'], (0.26, 0.1, 0.2), 0.03, 0.12, 'y', 12)
    mb.box(M['paper'], (0.3, 0.1, 0.178), (0.18, 0.06, 0.004), ry=-0.18); mb.box(M['paper'], (0.42, 0.1, 0.15), (0.15, 0.06, 0.004), ry=-0.5)
    for i in range(6): mb.box(M['ink'], (0.28 + i * 0.045, 0.1, 0.181 - i * 0.012), (0.018 if i % 2 else 0.01, 0.01, 0.006), ry=-0.3)
    # battery jars (green glass with copper) at the back
    for k, bx in enumerate((-0.34, -0.12)):
        mb.cyl(M['glassjar'], (bx, 0.27 + 0.0, 0.14), 0.07, 0.17, 'z', 16, True); mb.cyl(M['copper'], (bx, 0.27, 0.15), 0.035, 0.14, 'z', 10); mb.cyl(M['gold'], (bx, 0.27, 0.235), 0.075, 0.015, 'z', 16)
    mb.pop()

def window_wall(mb, M, y, win_x, ww=2.8, z0=2.5, z1=8.0, H=12.5, xa=-22.0, xb=22.0):
    mb.box(M['wall'], ((xa + xb) / 2, y, z0 / 2), (xb - xa, 1.0, z0)); mb.box(M['wall'], ((xa + xb) / 2, y, (z1 + H) / 2), (xb - xa, 1.0, H - z1))
    edges = [xa] + [v for c in win_x for v in (c - ww / 2, c + ww / 2)] + [xb]
    for i in range(0, len(edges), 2):
        a, b = edges[i], edges[i + 1]
        if b > a + 0.01: mb.box(M['wall'], ((a + b) / 2, y, (z0 + z1) / 2), (b - a, 1.0, z1 - z0))
    for c in win_x:
        mb.box(M['cream'], (c, y - 0.45, (z0 + z1) / 2), (0.1, 0.1, z1 - z0)); mb.box(M['cream'], (c, y - 0.45, z0 + 0.5 * (z1 - z0) * 0.62), (ww, 0.1, 0.08))
        mb.box(M['cream'], (c - ww / 2, y - 0.45, (z0 + z1) / 2), (0.1, 0.12, z1 - z0)); mb.box(M['cream'], (c + ww / 2, y - 0.45, (z0 + z1) / 2), (0.1, 0.12, z1 - z0))
        mb.box(M['cream'], (c, y - 0.5, z0), (ww + 0.3, 0.3, 0.1)); mb.box(M['cream'], (c, y - 0.5, z1), (ww + 0.3, 0.3, 0.1))

def desk(mb, M, c, rz, zt, rr, ink=True):
    mb.push(Matrix.Translation((c[0], c[1], zt)) @ Euler((0, 0, rz)).to_matrix().to_4x4())
    mb.box(M['walnut'], (0, 0, 0.8), (1.5, 0.76, 0.07)); mb.box(M['baize'], (0, 0, 0.84), (1.34, 0.6, 0.012))
    mb.box(M['walnut'], (0, -0.36, 0.42), (1.5, 0.05, 0.75)); 
    for sx in (-1, 1): mb.box(M['walnut'], (sx * 0.72, 0, 0.4), (0.05, 0.76, 0.8))
    mb.box(M['walnut'], (0, 0.3, 0.88), (1.5, 0.16, 0.1), rx=-0.35) if False else None
    mb.box(M['dark'], (0, 0.18, 0.43), (1.4, 0.04, 0.7))
    # items
    xi = rr.uniform(-0.4, 0.4)
    mb.cyl(M['ink'], (xi, 0.05, 0.87), 0.04, 0.05, 'z', 10); mb.cyl(M['brass'], (xi, 0.05, 0.9), 0.045, 0.012, 'z', 10)
    mb.rod(M['paper'], (xi, 0.05, 0.9), (xi + 0.08, 0.12, 1.08), 0.006, 0.003, 4)
    for k in range(rr.randint(1, 3)):
        mb.box(M['paper'], (rr.uniform(-0.55, 0.55) if k else -xi * 0.6 - 0.25, rr.uniform(-0.1, 0.1), 0.86 + k * 0.025), (0.3, 0.4, 0.04 + 0.03 * k), rz=rr.uniform(-0.3, 0.3))
    if rr.random() < 0.5: mb.box(M['leather'], (0.45, -0.1, 0.87), (0.25, 0.18, 0.05), rz=0.3)
    if rr.random() < 0.3:                                   # top hat on the desk (or on the chair back)
        hx = rr.uniform(-0.5, 0.5); mb.cyl(M['hat'], (hx, 0.1, 0.99), 0.1, 0.22, 'z', 14, True, r2=0.095); mb.cyl(M['hat'], (hx, 0.1, 0.88), 0.18, 0.02, 'z', 14); mb.cyl(M['red'], (hx, 0.1, 0.92), 0.102, 0.03, 'z', 14)
    elif rr.random() < 0.12: mb.cyl(M['hat'], (0.0, 1.2, 1.2), 0.1, 0.2, 'z', 14); mb.cyl(M['hat'], (0.0, 1.2, 1.1), 0.17, 0.02, 'z', 14)
    # chair behind
    mb.box(M['leather'], (0, 0.95, 0.5), (0.55, 0.5, 0.07)); mb.box(M['walnut'], (0, 1.2, 0.85), (0.55, 0.06, 0.6))
    for dx in (-0.25, 0.25):
        for dy in (0.75, 1.15): mb.rod(M['walnut'], (dx, dy, 0.0), (dx, dy, 0.46), 0.03, 0.025, 5)
    mb.pop()

def chandelier(mb, M, c):
    x, y, z = c
    mb.rod(M['brass'], (x, y, 12.5), (x, y, z + 0.9), 0.04, 0.04, 6)
    mb.ell(M['brass'], (x, y, z + 0.6), (0.4, 0.4, 0.5), (14, 10)); mb.ell(M['brass'], (x, y, z - 0.1), (0.25, 0.25, 0.3), (12, 8))
    for ri, (R_, zz, n) in enumerate([(1.8, z + 0.0, 12), (1.1, z + 0.5, 8)]):
        for i in range(n):
            a = i * 2 * math.pi / n; b = (i + 1) * 2 * math.pi / n
            mb.rod(M['brass'], (x + math.cos(a) * R_, y + math.sin(a) * R_, zz), (x + math.cos(b) * R_, y + math.sin(b) * R_, zz), 0.035, 0.035, 6)
            px, py = x + math.cos(a) * R_, y + math.sin(a) * R_
            mb.cyl(M['brass'], (px, py, zz + 0.08), 0.05, 0.14, 'z', 8); mb.cyl(M['cream'], (px, py, zz + 0.25), 0.032, 0.22, 'z', 8)
            mb.ell(M['flame'], (px, py, zz + 0.42), (0.03, 0.03, 0.07), (6, 4))
            mb.rod(M['brass'], (x, y, z + 0.4), (px, py, zz - 0.03), 0.02, 0.02, 5)
            if ri == 0: mb.ell(M['glassjar'], (px, py, zz - 0.25), (0.05, 0.05, 0.12), (8, 6))

def build_chamber(P):
    sc = bpy.context.scene; M = palette('chamber'); sky_world(P); hills(P); clouds(P)
    ground_plane(P, -0.4)
    mb = MB('room'); rr = rnd(5)
    mb.box(M['floor'], (0, 13, -0.15), (46, 44, 0.3)); mb.box(M['carpet'], (0, 14, -0.12), (3.0, 40, 0.3))
    mb.box(M['wall'], (-22.5, 13, 7), (1, 44, 14)); mb.box(M['wall'], (22.5, 13, 7), (1, 44, 14)); mb.box(M['wall'], (0, -9, 7), (46, 1, 14))
    mb.box(M['wall'], (0, 13, 12.8), (46, 44, 0.6))
    for i in range(-5, 6):
        mb.box(M['cream'], (i * 4.0, 13, 12.3), (0.6, 44, 0.4))
    for j in range(0, 5): mb.box(M['cream'], (0, j * 9.0 - 5, 12.25), (46, 0.6, 0.5))
    win_x = [-18, -12, -6, 0, 6, 12, 18]; BY = 34.0
    window_wall(mb, M, BY, win_x)
    for sx in (-1, 1):                                          # side wall windows (dark panes) + pilasters
        for yy in (8, 16, 24):
            mb.box(M['cream'], (sx * 21.9, yy, 5.0), (0.2, 2.4, 6.0)); mb.box(M['dark'], (sx * 21.8, yy, 5.0), (0.1, 2.0, 5.6))
    mb.box(M['walnut'], (0, BY - 0.45, 0.2), (44, 0.2, 0.4))
    # columns + drapes
    for cx in (-15, -9, -3, 3, 9, 15):
        mb.cyl(M['marble'], (cx, BY - 1.2, 5.0), 0.62, 10.0, 'z', 20, True); mb.box(M['marble'], (cx, BY - 1.2, 0.2), (1.6, 1.6, 0.4)); mb.box(M['marble'], (cx, BY - 1.2, 10.2), (1.7, 1.7, 0.4))
        mb.cyl(M['gold'], (cx, BY - 1.2, 9.8), 0.8, 0.3, 'z', 20)
    for c in win_x:
        for sg in (-1, 1):
            mb.rod(M['drape'], (c + sg * 1.85, BY - 0.9, 8.7), (c + sg * 1.85, BY - 0.9, 1.0), 0.3, 0.38, 10, smooth=True)
            mb.rod(M['drape'], (c + sg * 1.55, BY - 0.9, 8.4), (c + sg * 1.62, BY - 0.9, 3.0), 0.16, 0.18, 8, smooth=True)
            mb.cyl(M['gold'], (c + sg * 1.85, BY - 0.9, 3.0), 0.34, 0.05, 'z', 10)
        mb.box(M['drape'], (c, BY - 0.9, 8.7), (4.0, 0.5, 0.55)); mb.cyl(M['gold'], (c, BY - 1.17, 8.4), 0.05, 4.0, 'x', 6)
        for k in range(7): mb.ell(M['drape'], (c - 1.8 + k * 0.6, BY - 1.1, 8.45), (0.35, 0.2, 0.3), (10, 6))
    # speaker's dais + rostrum
    mb.box(M['floor'], (0, 10.5, 0.2), (7.0, 3.6, 0.4)); mb.box(M['carpet'], (0, 10.0, 0.42), (5.0, 2.4, 0.04))
    mb.box(M['walnut'], (0, 11.2, 1.0), (2.4, 0.9, 1.2)); mb.box(M['walnut'], (0, 11.2, 1.65), (2.7, 1.1, 0.1)); mb.box(M['leather'], (0, 11.0, 1.72), (2.4, 0.8, 0.04))
    mb.box(M['leather'], (0, 12.6, 0.95), (0.8, 0.7, 0.1)); mb.box(M['walnut'], (0, 13.0, 1.9), (0.8, 0.1, 2.2)); mb.box(M['leather'], (0, 12.95, 2.0), (0.6, 0.03, 1.7))
    mb.box(M['gold'], (0.8, 11.2, 1.8), (0.1, 0.1, 0.3)); mb.cyl(M['gold'], (-0.8, 11.2, 1.85), 0.1, 0.3, 'z', 10)
    # life: brass spittoons beside the aisle, a floor globe on the dais, framed paintings over the windows
    for (sx_, sy_) in [(-1.8, 3.0), (1.9, 9.0), (-2.1, 15.0), (2.2, 19.0)]:
        mb.ell(M['brass'], (sx_, sy_, 0.16), (0.24, 0.24, 0.16), (14, 8)); mb.cyl(M['brass'], (sx_, sy_, 0.3), 0.15, 0.12, 'z', 14, True, r2=0.2)
    gx, gy = -2.8, 10.4
    mb.cyl(M['walnut'], (gx, gy, 0.55), 0.22, 0.03, 'z', 12); mb.rod(M['walnut'], (gx, gy, 0.42), (gx, gy, 1.05), 0.04, 0.03, 8)
    for k in (-1, 1): mb.rod(M['walnut'], (gx, gy, 0.42), (gx + k * 0.4, gy, 0.42), 0.03, 0.03, 6); mb.rod(M['walnut'], (gx, gy, 0.42), (gx, gy + k * 0.4, 0.42), 0.03, 0.03, 6)
    mb.ell(M['globe'], (gx, gy, 1.5), (0.5, 0.5, 0.5), (24, 16)); mb.cyl(M['brass'], (gx, gy, 1.5), 0.53, 0.03, 'x', 24); mb.cyl(M['brass'], (gx, gy, 1.5), 0.53, 0.03, 'y', 24)
    rp = rnd(77)
    for k, c in enumerate(win_x):
        mb.box(M['frame'], (c, BY - 0.62, 10.4), (3.1, 0.14, 2.1)); mb.box(M['paintsky'], (c, BY - 0.72, 10.65), (2.8, 0.06, 1.3)); mb.box(M['paintgrn'], (c, BY - 0.72, 9.75), (2.8, 0.06, 0.6))
        for j in range(3): mb.ell(M['paintdk'], (c - 0.9 + j * 0.9 + rp.uniform(-0.2, 0.2), BY - 0.76, 10.0), (0.22, 0.03, 0.34 + 0.1 * j), (8, 6))
        mb.ell(M['paintgrn'], (c + rp.uniform(-0.6, 0.6), BY - 0.76, 9.8), (0.9, 0.03, 0.3), (10, 6))
    # tiers of desks (semicircle around C, opening toward camera)
    C = (0.0, 7.0)
    for ti, r in enumerate([6.5, 9.0, 11.5, 14.0, 16.5]):
        zt = 0.0 + 0.38 * ti
        a0, a1 = math.radians(14), math.radians(166); n = int((a1 - a0) * r / 1.75)
        for i in range(n):
            a = a0 + (i + 0.5) * (a1 - a0) / n
            if abs(a - math.pi / 2) < math.radians(5.5) or abs(a - math.pi / 2) - math.radians(38) < 0 and abs(abs(a - math.pi / 2) - math.radians(38)) < math.radians(2.0): continue
            px, py = C[0] + r * math.cos(a), C[1] + r * math.sin(a)
            if ti:
                mb.box(M['floor'], (C[0] + (r + 0.3) * math.cos(a), C[1] + (r + 0.3) * math.sin(a), zt / 2 - 0.04), (2.65, 2.55, zt + 0.0), rz=a - math.pi / 2)
            desk(mb, M, (px, py), a - math.pi / 2, zt, rr)
    mb.finish()
    # --- front table with telegraph
    mb = MB('table')
    tx, ty = 0.0, 4.2
    TW = 4.8
    mb.box(M['walnut'], (tx, ty, 0.9), (TW, 1.7, 0.1)); mb.box(M['baize'], (tx, ty, 0.955), (TW - 0.2, 1.5, 0.012)); mb.box(M['gold'], (tx, ty - 0.86, 0.9), (TW, 0.03, 0.07))
    for sx in (-TW / 2 + 0.2, TW / 2 - 0.2):
        for sy in (-0.7, 0.7): mb.rod(M['walnut'], (tx + sx, ty + sy, 0.0), (tx + sx, ty + sy, 0.86), 0.09, 0.06, 8, smooth=True)
    mb.box(M['walnut'], (tx, ty, 0.35), (TW - 0.4, 0.08, 0.1))
    telegraph(mb, M, (tx - 0.35, ty + 0.1, 0.96), 3.5)
    mb.box(M['paper'], (tx + 2.0, ty - 0.2, 0.99), (0.5, 0.65, 0.06), rz=0.2); mb.box(M['paper'], (tx + 1.95, ty - 0.18, 1.04), (0.46, 0.6, 0.05), rz=0.35)
    mb.cyl(M['ink'], (tx + 1.8, ty + 0.5, 0.99), 0.06, 0.1, 'z', 10); mb.cyl(M['brass'], (tx + 1.8, ty + 0.5, 1.05), 0.065, 0.02, 'z', 10); mb.rod(M['paper'], (tx + 1.8, ty + 0.5, 1.05), (tx + 1.95, ty + 0.62, 1.4), 0.008, 0.003, 4)
    mb.cyl(M['gold'], (tx - 2.0, ty - 0.2, 1.05), 0.1, 0.22, 'z', 10); mb.cyl(M['cream'], (tx - 2.0, ty - 0.2, 1.25), 0.03, 0.2, 'z', 8); mb.ell(M['flame'], (tx - 2.0, ty - 0.2, 1.38), (0.025, 0.025, 0.06), (6, 4))   # candlestick
    # coiled wire entering table from the floor
    for k in range(7): mb.cyl(M['wiremat'], (tx - 1.9, ty + 0.2, 0.05 + k * 0.045), 0.3, 0.03, 'z', 16) if False else None
    mb.rod(M['wiremat'], (tx - 0.7, ty + 0.5, 0.97), (tx - 1.4, ty + 0.8, 0.5), 0.015, 0.015, 5); mb.rod(M['wiremat'], (tx - 1.4, ty + 0.8, 0.5), (tx - 2.2, ty + 1.3, 0.02), 0.015, 0.015, 5)
    # two lone chairs flanking the table
    for sx in (-3.4, 3.4):
        mb.box(M['leather'], (tx + sx, ty - 0.2, 0.5), (0.55, 0.5, 0.07)); mb.box(M['walnut'], (tx + sx, ty + 0.05, 0.9), (0.55, 0.06, 0.8))
        for dx in (-0.25, 0.25):
            for dy in (-0.4, 0.0): mb.rod(M['walnut'], (tx + sx + dx, ty + dy, 0.0), (tx + sx + dx, ty + dy, 0.46), 0.03, 0.025, 5)
    mb.finish()
    mb = MB('chand'); chandelier(mb, M, (0.0, 17.0, 8.4)); mb.finish()
    # sun shafts through the back windows
    kd = Vector(P['key_dir']).normalized(); mb = MB('shafts')
    for c in win_x:
        z0, z1 = 2.5, 8.0; hw = 1.4; yy = BY - 0.4
        cor = [(c - hw, yy, z0), (c + hw, yy, z0), (c + hw, yy, z1), (c - hw, yy, z1)]
        def flo(p): t = p[2] / -kd.z; return (p[0] + kd.x * t, p[1] + kd.y * t, 0.02)
        fl = [flo(p) for p in cor]
        for i in range(4):
            j = (i + 1) % 4; mb.quad(M['shaft'], [cor[i], cor[j], fl[j], fl[i]])
    for o in mb.finish(): o.visible_shadow = False
    mb = MB('shafts2'); mb.finish()
    return M

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

# ------------------------------------------------------------------ presets
def kdir(az, el):
    a = math.radians(az); e = math.radians(el)
    return (-math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), -math.sin(e))

PRESETS = {
 'line': dict(
    sky=[(0.0, '#7a86d6'), (0.45, '#f0bc88'), (0.5, '#f8d9a2'), (0.56, '#e8d8c0'), (0.66, '#9cbcec'), (0.82, '#4a7adc'), (1.0, '#2f52c4')], sky_k=0.85,
    key=(1.0, 0.85, 0.63, 14.0), key_dir=kdir(150, 24), sun_angle=1.0, exposure=0.0, sat=1.08, bottle_s=2.2, sag=0.55, wire_r=0.03,
    amb=('#4454FF', 2.2),
    hills=[(250, 8, 16, '#9a9ad2'), (310, 20, 28, '#8aa0d8'), (380, 34, 30, '#7ea4d6')], hill_k=1.0,
    cloud=('#ffeacc', '#7c84d8'), cloud_diffuse=True, cloud_z=(40, 130), ncloud=14, cloud_scale=0.5,
    g1='#c4a244', g2='#8aa83a', g3='#b07a38', gsize=500, wagon=(1.9, 6.5), lfence=True, fgprop=(-2.0, -3.3, 0.0), loco_y=22.0, tx=-9.5,
    cam=dict(loc=(-0.2, -6.0, 1.9), look=(1.6, 30.0, 2.9), lens=22), samples=96),
 'chamber': dict(
    sky=[(0.0, '#7a86d6'), (0.45, '#f4c890'), (0.5, '#fbe0aa'), (0.56, '#f4e4c4'), (0.66, '#a8c6f0'), (0.82, '#5a86e4'), (1.0, '#3a5acc')], sky_k=1.0,
    key=(1.0, 0.85, 0.63, 9.0), key_dir=kdir(-22, 15), sun_angle=1.0, exposure=0.0, sat=1.08,
    hills=[(250, 8, 16, '#9a9ad2'), (310, 20, 28, '#8aa0d8')], hill_k=1.0, cloud=('#fff0dc', '#a8a4dc'), cloud_z=(40, 80), ncloud=6, cloud_diffuse=True,
    g1='#a8a050', g2='#c8a858', g3='#a08048', gsize=500, fill=(0.02, 0.21, 1.0, 17000), dbounce=1, cam=dict(loc=(0.0, -2.6, 2.6), look=(0.0, 15.0, 1.5), lens=22), samples=110),
 'close': dict(
    sky=[(0.0, '#4a62c0'), (0.45, '#f0b080'), (0.5, '#f8d098'), (0.58, '#8a98d0'), (0.74, '#4a64c0'), (1.0, '#2a3fa8')], sky_k=1.0,
    key=(1.0, 0.85, 0.63, 9.0), key_dir=kdir(-125, 24), sun_angle=0.8, exposure=0.0, sat=1.08, amb=('#6064FF', 2.2), bottle_s=2.3, pole_h=4.8, sag=0.45, wire_r=0.03, drops=0.9,
    hills=[(250, 8, 16, '#8a8ac8'), (310, 20, 28, '#7a96d2'), (380, 34, 30, '#7aa0d4')], hill_k=0.95,
    cloud=('#ffe2bc', '#6c78d4'), cloud_diffuse=True, cloud_z=(60, 460), ncloud=17, cloud_seed=3, cloud_scale=0.8,
    g1='#a89640', g2='#7a9a3c', g3='#9a7a44', gsize=500, grough=0.35, gspec=0.45, wagon=(-3.2, 14.0), loco_y=40.0, lfence=True, tx=-12.0,
    cam=dict(loc=(2.9, 1.9, 1.0), look=(4.1, 4.0, 2.7), lens=22), samples=120),
}

def lights(P, mode):
    sc = bpy.context.scene; k = P['key']; kd = Vector(P['key_dir']).normalized()
    d = bpy.data.lights.new('key', 'SUN'); d.color = k[:3]; d.energy = k[3]; d.angle = math.radians(P['sun_angle'])
    o = bpy.data.objects.new('key', d); sc.collection.objects.link(o); o.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler()
    if mode == 'chamber':
        l = bpy.data.lights.new('fill', 'AREA'); l.shape = 'RECTANGLE'; l.size = 36; l.size_y = 36; l.color = P['fill'][:3]; l.energy = P['fill'][3]
        ob = bpy.data.objects.new('fill', l); ob.location = (0, 13, 12.2); sc.collection.objects.link(ob); ob.visible_camera = False       # points down (-Z) by default
        l4 = bpy.data.lights.new('fillup', 'AREA'); l4.shape = 'RECTANGLE'; l4.size = 36; l4.size_y = 36; l4.color = P['fill'][:3]; l4.energy = P['fill'][3] * 0.16
        ob4 = bpy.data.objects.new('fillup', l4); ob4.location = (0, 13, 1.2); ob4.rotation_euler = (math.pi, 0, 0); sc.collection.objects.link(ob4); ob4.visible_camera = False
    if mode != 'chamber' and P.get('dome'):
        dm = P['dome']; l = bpy.data.lights.new('dome', 'AREA'); l.shape = 'SQUARE'; l.size = dm[4]; l.color = dm[:3]; l.energy = dm[3]
        ob = bpy.data.objects.new('dome', l); ob.location = (0, 100, 200); sc.collection.objects.link(ob); ob.visible_camera = False
    if P.get('sunDisc'):
        mm = mat_emit('sundisc', '#fff0cc', 40.0); mb = MB('sun'); cp = Vector(P['cam']['loc']) - kd * 330; mb.ell(mm, cp, (P['sunDisc'],) * 3, (24, 16)); mb.ell(mat_emit('sunhalo', '#ffcf90', 3.0), cp + kd * -8.0, (P['sunDisc'] * 2.2,) * 3, (24, 16)); mb.finish()

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

def render(mode, out, samples, draft):
    sc = bpy.context.scene; P = PRESETS[mode]
    sc.render.engine = 'CYCLES'; cy = sc.cycles; cy.device = 'CPU'; cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'
    cy.denoising_input_passes = 'RGB_ALBEDO_NORMAL'; cy.max_bounces = 3; cy.diffuse_bounces = P.get('dbounce', 0); cy.glossy_bounces = 1; cy.transmission_bounces = 0; cy.transparent_max_bounces = 6
    cy.use_light_tree = True; cy.filter_width = 1.2; sc.render.threads = 4
    sc.render.resolution_x = W // (2 if draft else 1); sc.render.resolution_y = H // (2 if draft else 1); sc.render.resolution_percentage = 100
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = P.get('exposure', 0.0)
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
    A = _rd(sc, out + '_A.png', samples, True)[..., :3]
    # shade mask (for the hue check only, NOT used for grading): direct-sun-only render with a white override material, no bounces,
    # sky / clouds / hills / sun disc / shafts hidden (alpha 0). Shade = not sky and sun contribution ~ 0.
    others = [(l, l.energy) for l in bpy.data.lights if l.name != 'key']
    for l, e in others: l.energy = 0.0
    wbgs = [n for n in bpy.data.worlds['sky'].node_tree.nodes if n.bl_idname == 'ShaderNodeBackground']; wvs = [n.inputs['Strength'].default_value for n in wbgs]
    for n in wbgs: n.inputs['Strength'].default_value = 0.0
    hid = [o for o in bpy.data.objects if o.name.startswith(('hills', 'clouds', 'sun_', 'shafts'))]
    for o in hid: o.hide_render = True
    wm = bpy.data.materials.new('ovr'); wm.use_nodes = True; bs = wm.node_tree.nodes['Principled BSDF']; bs.inputs['Base Color'].default_value = (1, 1, 1, 1)
    bs.inputs['Roughness'].default_value = 1.0; bs.inputs['Specular IOR Level'].default_value = 0.0
    cy.max_bounces = 0; cy.diffuse_bounces = 0; cy.glossy_bounces = 0; bpy.context.view_layer.material_override = wm
    D = _rd(sc, out + '_D.png', 24, False, True)
    bpy.context.view_layer.material_override = None
    lD = 0.3 * D[..., 0] + 0.59 * D[..., 1] + 0.11 * D[..., 2]
    # D2: same but nothing casts shadows -> where D2 is lit but D is dark, the sun is truly blocked (a real cast shadow, not just a surface turned away)
    vs = [(o, o.visible_shadow) for o in bpy.data.objects if o.type == 'MESH']
    for o, _ in vs: o.visible_shadow = False
    D2 = _rd(sc, out + '_D2.png', 8, False, True)
    for o, v in vs: o.visible_shadow = v
    lD2 = 0.3 * D2[..., 0] + 0.59 * D2[..., 1] + 0.11 * D2[..., 2]
    cast = (D[..., 3] > 0.99) & (lD < 0.02) & (lD2 > 0.08)
    Image.fromarray((cast * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).save(out + '_shade.png')
    a = grade(A, P)
    Image.fromarray((a * 255 + 0.5).astype(np.uint8)).save(out + '.jpg', quality=93)

NAMES = {'line': 'sb1_line_wide', 'chamber': 'sb2_chamber', 'close': 'sb3_bottle_close'}
def run(mode, draft=False):
    t = time.time(); bpy.ops.wm.read_factory_settings(use_empty=True); MATS.clear(); P = PRESETS[mode]
    if mode == 'chamber': build_chamber(P)
    else: build_line(mode, P)
    lights(P, mode); setup_camera(P)
    out = os.path.join(HERE, ('d_' if draft else '') + NAMES[mode])
    render(mode, out, 20 if draft else P.get('samples', 100), draft); print(mode, 'done %.0fs' % (time.time() - t))

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != 'draft']; draft = 'draft' in sys.argv
    for m in (['line', 'chamber', 'close'] if (not args or args[0] == 'all') else args): run(m, draft)

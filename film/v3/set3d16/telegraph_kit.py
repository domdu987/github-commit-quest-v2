"""telegraph_kit.py : shared kit of set3d16 (film 16): scaled/rotated geometry builder, painterly two-tone noise materials with a global
WET node group, and the props grown from the client-approved style board (styleboard/sb.py).
Authoring frame = sb.py frame (metres: +x right, +y along the line / away from the camera, z up). Everything that reaches Blender goes through
frame_mat(): D = SC * Rz(FR['rot']) * metres, so the world is 1 unit = 1 D (head) with adults ~3.2 D (SC = 1.85 D per metre)."""
import os, sys, math, random, time
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix, Euler
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SC = 1.85
FR = dict(rot=0.0)
def frame_mat(): return Matrix.Rotation(FR['rot'], 4, 'Z') @ Matrix.Scale(SC, 4)
def W(p): return frame_mat() @ Vector(p)                 # sb-frame metres -> world D
def Wd(d): return Matrix.Rotation(FR['rot'], 3, 'Z') @ Vector(d)

def lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def hexc(h):
    h = h.lstrip('#'); return tuple(lin(int(h[i:i + 2], 16)) for i in (0, 2, 4)) + (1.0,)

# ------------------------------------------------------------------ materials
MATS = {}
def mat(name, A, B=None, scale=3.0, aniso=(1, 1, 1), rough=1.0, emit=None, emit_k=0.0, zgrad=None, wave=None, sheen=0.0, contrast=1.0, wet=False, clip=None):
    """Principled diffuse with a two-tone object-space noise mix (painterly variation). zgrad=(z0,z1,hexLow) blends hexLow at z<=z0 to A/B at z>=z1.
    wave=(freq, hexStripe): corrugation stripes along x. emit: emission colour hex with strength emit_k."""
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled')
    bs.inputs['Roughness'].default_value = rough
    for k in ('Specular IOR Level',):
        if k in bs.inputs: bs.inputs[k].default_value = 0.0 if sheen == 0 else sheen
    tc = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (scale / SC * aniso[0], scale / SC * aniso[1], scale / SC * aniso[2])
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
        wv = N('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'X'; wv.inputs['Scale'].default_value = wave[0] / SC; wv.inputs['Distortion'].default_value = 1.5
        wv.inputs['Detail'].default_value = 1; L(tc.outputs['Object'], wv.inputs['Vector'])
        cr2 = N('ShaderNodeValToRGB'); L(wv.outputs['Fac'], cr2.inputs['Fac']); cr2.color_ramp.elements[0].position = 0.35; cr2.color_ramp.elements[1].position = 0.65
        mx2 = N('ShaderNodeMix'); mx2.data_type = 'RGBA'; L(col, mx2.inputs[6]); mx2.inputs[7].default_value = hexc(wave[1]); L(cr2.outputs[0], mx2.inputs[0]); col = mx2.outputs[2]
    if zgrad:
        sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Object'], sp.inputs[0])
        mr = N('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = zgrad[0] * SC; mr.inputs['From Max'].default_value = zgrad[1] * SC; L(sp.outputs['Z'], mr.inputs['Value'])
        mx3 = N('ShaderNodeMix'); mx3.data_type = 'RGBA'; mx3.inputs[6].default_value = hexc(zgrad[2]); L(col, mx3.inputs[7]); L(mr.outputs['Result'], mx3.inputs[0]); col = mx3.outputs[2]
    if wet:
        wn = wet_out(nt); dk = N('ShaderNodeMix'); dk.data_type = 'RGBA'; dk.blend_type = 'MULTIPLY'; dk.inputs[7].default_value = (0.5, 0.36, 0.34, 1.0)
        L(wn, dk.inputs[0]); L(col, dk.inputs[6]); col = dk.outputs[2]
        rm = N('ShaderNodeMath'); rm.operation = 'MULTIPLY_ADD'; rm.inputs[1].default_value = -0.6 * rough; rm.inputs[2].default_value = rough; L(wn, rm.inputs[0]); L(rm.outputs[0], bs.inputs['Roughness'])
        sm = N('ShaderNodeMath'); sm.operation = 'MULTIPLY_ADD'; sm.inputs[1].default_value = 0.5; sm.inputs[2].default_value = 0.0 if sheen == 0 else sheen; L(wn, sm.inputs[0]); L(sm.outputs[0], bs.inputs['Specular IOR Level'])
    L(col, bs.inputs['Base Color'])
    if emit:
        bs.inputs['Emission Color'].default_value = hexc(emit); bs.inputs['Emission Strength'].default_value = emit_k
    if clip:      # clip=(group name, axis idx): transparent where object-space coordinate > value of the node group (metres along the line)
        cv = clip_out(nt, clip); sp2 = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Object'], sp2.inputs[0])
        cmp_ = N('ShaderNodeMath'); cmp_.operation = 'GREATER_THAN'; L(sp2.outputs['X'], cmp_.inputs[0]); L(cv, cmp_.inputs[1])
        tr = N('ShaderNodeBsdfTransparent'); mxs = N('ShaderNodeMixShader'); L(cmp_.outputs[0], mxs.inputs[0]); L(bs.outputs[0], mxs.inputs[1]); L(tr.outputs[0], mxs.inputs[2]); L(mxs.outputs[0], out.inputs['Surface'])
    else: L(bs.outputs[0], out.inputs['Surface'])
    MATS[name] = m; return m

def _group(name, vname):
    g = bpy.data.node_groups.get(name)
    if g is None:
        g = bpy.data.node_groups.new(name, 'ShaderNodeTree'); g.interface.new_socket('V', in_out='OUTPUT', socket_type='NodeSocketFloat')
        v = g.nodes.new('ShaderNodeValue'); v.name = vname; go = g.nodes.new('NodeGroupOutput'); g.links.new(v.outputs[0], go.inputs[0])
    return g
def wet_out(nt):
    n = nt.nodes.new('ShaderNodeGroup'); n.node_tree = _group('TG_WET', 'wet'); return n.outputs[0]
def clip_out(nt, which):
    n = nt.nodes.new('ShaderNodeGroup'); n.node_tree = _group('TG_CLIP_' + which, 'clip'); return n.outputs[0]

def mat_emit(name, hexcol, k):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = hexc(hexcol); em.inputs['Strength'].default_value = k
    nt.links.new(em.outputs[0], out.inputs['Surface']); MATS[name] = m; return m

# ------------------------------------------------------------------ geometry builder (one object per material)
class MB:
    def __init__(self, name): self.name = name; self.bm = {}; self.T = frame_mat(); self.stack = []
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
def palette():
    d = {}
    d['pole'] = mat('pole', '#c98a46', '#e8ac66', 7, aniso=(1, 1, 0.12), contrast=1.3, wet=True, sheen=0.1)
    d['polecut'] = mat('polecut', '#efd49a', '#e0b878', 3)
    d['wood'] = mat('wood', '#78461f', '#9a6230', 6, aniso=(1, 1, 0.3), contrast=1.5, wet=True)
    d['woodpale'] = mat('woodpale', '#c8883c', '#e0a856', 8, aniso=(0.4, 1, 1), contrast=1.4, wet=True)
    d['walnut'] = mat('walnut', '#6a3a1c', '#8e5430', 7, aniso=(1, 0.3, 0.3), contrast=1.6, rough=0.45, sheen=0.4)
    d['glass'] = mat('glass', '#2a9a68', '#5fd09e', 4, rough=0.1, sheen=1.0, emit='#35b880', emit_k=0.5)
    d['glassjar'] = mat('glassjar', '#7ac4a8', '#a6e0c8', 4, rough=0.1, sheen=1.0, emit='#6ad0a8', emit_k=0.3)
    d['wiremat'] = mat('wiremat', '#2a221e', '#4a3c32', 3, rough=0.35, sheen=0.6)
    d['drop'] = mat('drop', '#e0f0ff', '#ffffff', 2, rough=0.05, sheen=1.0, emit='#d8ecff', emit_k=1.2)
    d['road'] = mat('road', '#bc7e3e', '#d49a58', 3.0, aniso=(1.2, 0.35, 1.0), contrast=1.4, wet=True)
    d['rut'] = mat('rut', '#966030', '#b27a40', 4.0, aniso=(2, 0.3, 1), wet=True)
    d['verge'] = mat('verge', '#7fa63a', '#c4b042', 4.0, aniso=(1.4, 0.4, 1), wet=True)
    d['earth'] = mat('earth', '#8c5233', '#b06c44', 6, contrast=1.3, wet=True)
    d['ballast'] = mat('ballast', '#9a8e86', '#c0aea0', 14, contrast=1.8, wet=True)
    d['sleeper'] = mat('sleeper', '#4a3426', '#6a4a34', 5, wet=True)
    d['rail'] = mat('rail', '#7a6058', '#a88c80', 3, rough=0.4, sheen=0.6)
    d['lead'] = mat('lead', '#8c929c', '#b6bcc6', 3, rough=0.35, sheen=0.7)
    d['straw'] = mat('straw', '#d6b25a', '#eccb78', 7, contrast=1.3, wet=True)
    d['strawdk'] = mat('strawdk', '#b08a3c', '#d0a850', 7, wet=True)
    d['wheat'] = mat('wheat', '#d6a838', '#f4cc58', 6, zgrad=(0.0, 0.5, '#9a9a34'), contrast=1.4, wet=True)
    d['hay'] = mat('hay', '#c8a248', '#e8c46c', 8, aniso=(1, 1, 0.3), wet=True)
    d['leafA'] = mat('leafA', '#4f8a3a', '#8aa83e', 2.2, contrast=1.6)
    d['leafB'] = mat('leafB', '#8a9a2c', '#d0a838', 2.2, contrast=1.6)
    d['trunk'] = mat('trunk', '#4a3228', '#6d4a36', 5, aniso=(1, 1, 0.3), wet=True)
    d['brick'] = mat('brick', '#a2402e', '#bf5a3e', 9, aniso=(1, 1, 0.5), contrast=1.4)
    d['plaster'] = mat('plaster', '#f0e2c2', '#e0cca0', 2.5, wet=True)
    d['barnred'] = mat('barnred', '#8e3224', '#a84632', 5, aniso=(0.3, 1, 1), wet=True)
    d['shingle'] = mat('shingle', '#5a4a48', '#7a6a66', 8, aniso=(1, 1, 0.6), wet=True)
    d['roofred'] = mat('roofred', '#9a3a2c', '#b8523a', 9, aniso=(1, 1, 0.6), wet=True)
    d['dark'] = mat('dark', '#241a1e', '#3a2a2a', 3)
    d['cream'] = mat('cream', '#f4ead0', '#e6d8b4', 3)
    d['green'] = mat('green', '#2f6a45', '#3f8a58', 4, rough=0.6, sheen=0.3)
    d['black'] = mat('black', '#222024', '#3a363c', 4, rough=0.6, sheen=0.3)
    d['brass'] = mat('brass', '#d7a23a', '#f2cf70', 4, rough=0.3, sheen=0.9)
    d['copper'] = mat('copper', '#b4602c', '#d88848', 4, rough=0.35, sheen=0.8, wave=(60, '#7a3c1c'))
    d['red'] = mat('red', '#a8332a', '#c8483a', 4, rough=0.6)
    d['carriage'] = mat('carriage', '#9a3a2e', '#b94c3a', 4, aniso=(0.4, 1, 1), wet=True)
    d['carriage2'] = mat('carriage2', '#d9a642', '#ecc060', 4, aniso=(0.4, 1, 1), wet=True)
    d['smoke'] = mat('smoke', '#f6ebe0', '#d8cce0', 2, emit='#fff0e0', emit_k=0.25)
    d['metal'] = mat('metal', '#9aa4b0', '#c0c8d0', 3, rough=0.4, sheen=0.5)
    d['rope'] = mat('rope', '#cfae74', '#a88650', 12, wet=True)
    d['spool'] = mat('spool', '#a8602c', '#cc8040', 3, rough=0.35, sheen=0.8, wave=(90, '#5e3218'))
    d['bird'] = mat('bird', '#2a2428', '#3a3238', 2)
    # chamber
    d['floor'] = mat('floor', '#a8702c', '#d4964a', 8, aniso=(1, 0.2, 1), contrast=1.6, rough=0.4, sheen=0.4)
    d['carpet'] = mat('carpet', '#8c1a24', '#a82a32', 10, contrast=1.2)
    d['baize'] = mat('baize', '#2c8040', '#40a05a', 12)
    d['wall'] = mat('wall', '#f2e4c0', '#e4d0a0', 2.0, contrast=0.8)
    d['marble'] = mat('marble', '#f6ecd6', '#e8dcc0', 2.5, contrast=0.8)
    d['drape'] = mat('drape', '#a02a2a', '#c64440', 3, aniso=(0.4, 0.4, 3.0), contrast=1.5)
    d['gold'] = mat('gold', '#d4a840', '#f0cc68', 4, rough=0.3, sheen=0.8)
    d['leather'] = mat('leather', '#8a2a2a', '#a8403a', 6)
    d['paper'] = mat('paper', '#f6ecd2', '#e8dcc0', 6)
    d['ink'] = mat('ink', '#1c1a22', '#2c2a34', 3, rough=0.2, sheen=0.8)
    d['flame'] = mat_emit('flame', '#ffb84a', 22.0)
    d['carpetdk'] = mat('carpetdk', '#4a0e16', '#5a1620', 10)
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


"""core20.py : shared helpers of the film-20 set (set3d20): materials, mesh builder, sky / sun / lamps, render setup, camera, keying helpers,
placeholder actors, project / head_pixels.  Used by set3d20.py (public API), site20.py, tower20.py and int20.py (CAFE / RESTO).
See API.md ("core20 contract").  bpy 5.3, Cycles CPU, NO depth of field, NO text anywhere.

SCALE: 1 world unit = 1 D (head).  Adult puppets 3.2 D tall = 1.7 m  =>  1 metre = SC = 1.88 D.
Authoring: geometry may be built in METRES under the scaled empty `root()` (scale SC; textures keep metre object coordinates) with MB(name, parent=root()),
or directly in D (MB(name) without parent).  Marks / cameras / actors are always in world D.  `W(p_metres)` converts a metre point to D.
Point lights: lamp(name, p_world_D, colour, energy_at_metre_scale) multiplies the power by SC^2 so a lamp authored for a metre scene looks the same.
"""
import os, sys, math, json, time, random, hashlib, subprocess
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))          # film/
SC = 1.88                                               # D per metre
STATE = {}                                              # live dict (loc, preset, light, marks, cam, staging, ...)
def W(p): return (p[0] * SC, p[1] * SC, p[2] * SC)
def Wv(p): return Vector(W(p))

def lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def hexc(h):
    h = h.lstrip('#'); return tuple(lin(int(h[i:i + 2], 16)) for i in (0, 2, 4)) + (1.0,)

# ------------------------------------------------------------------ materials
MATS = {}
def mat(name, A, B=None, scale=3.0, aniso=(1, 1, 1), rough=1.0, emit=None, emit_k=0.0, zgrad=None, wave=None, sheen=0.0, contrast=1.0):
    """Principled diffuse with a two-tone object-space noise mix. zgrad=(z0,z1,hexLow): hexLow below z0 -> A/B above z1. wave=(freq,hex): stripes along x."""
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); bs.inputs['Roughness'].default_value = rough
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
        L(tc.outputs['Object'], wv.inputs['Vector'])
        cr2 = N('ShaderNodeValToRGB'); L(wv.outputs['Fac'], cr2.inputs['Fac']); cr2.color_ramp.elements[0].position = 0.35; cr2.color_ramp.elements[1].position = 0.65
        mx2 = N('ShaderNodeMix'); mx2.data_type = 'RGBA'; L(col, mx2.inputs[6]); mx2.inputs[7].default_value = hexc(wave[1]); L(cr2.outputs[0], mx2.inputs[0]); col = mx2.outputs[2]
    if zgrad:
        sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Object'], sp.inputs[0])
        mr = N('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = zgrad[0]; mr.inputs['From Max'].default_value = zgrad[1]; L(sp.outputs['Z'], mr.inputs['Value'])
        mx3 = N('ShaderNodeMix'); mx3.data_type = 'RGBA'; mx3.inputs[6].default_value = hexc(zgrad[2]); L(col, mx3.inputs[7]); L(mr.outputs['Result'], mx3.inputs[0]); col = mx3.outputs[2]
    L(col, bs.inputs['Base Color'])
    if emit:
        bs.inputs['Emission Color'].default_value = hexc(emit); bs.inputs['Emission Strength'].default_value = emit_k
    L(bs.outputs[0], out.inputs['Surface']); MATS[name] = m; return m

def mat_emit(name, hexcol, k):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = hexc(hexcol); em.inputs['Strength'].default_value = k
    nt.links.new(em.outputs[0], out.inputs['Surface']); MATS[name] = m; return m

def mat_glow(name, hexcol, k, alpha):
    """see-through emissive halo (mix of transparent and emission)"""
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    em.inputs['Color'].default_value = hexc(hexcol); em.inputs['Strength'].default_value = k; mx.inputs[0].default_value = alpha
    L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface']); MATS[name] = m; return m

def mat_windows(name, wall, wall2, glass, lit, litk=6.0, prob=0.4, period=(3.4, 3.4), wf=(0.4, 0.55), z0=1.8, rough=1.0):
    """facade shader: cream wall with a procedural grid of windows (period in x+y and z); a hash picks lit warm windows (emission) vs dark glass."""
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); bs.inputs['Roughness'].default_value = rough; bs.inputs['Specular IOR Level'].default_value = 0.0
    tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Object'], sp.inputs[0])
    def M_(op, a=None, b=None, ca=None, cb=None):
        n = N('ShaderNodeMath'); n.operation = op
        if a is not None: L(a, n.inputs[0])
        elif ca is not None: n.inputs[0].default_value = ca
        if b is not None: L(b, n.inputs[1])
        elif cb is not None: n.inputs[1].default_value = cb
        return n.outputs[0]
    u = M_('MULTIPLY', M_('ADD', sp.outputs['X'], sp.outputs['Y']), cb=1.0 / period[0]); v = M_('MULTIPLY', sp.outputs['Z'], cb=1.0 / period[1])
    fu = M_('FRACT', u); fv = M_('FRACT', v)
    mu = M_('LESS_THAN', M_('ABSOLUTE', M_('SUBTRACT', fu, cb=0.5)), cb=wf[0] * 0.5)
    mv = M_('LESS_THAN', M_('ABSOLUTE', M_('SUBTRACT', fv, cb=0.5)), cb=wf[1] * 0.5)
    mz = M_('GREATER_THAN', sp.outputs['Z'], cb=z0)
    win = M_('MULTIPLY', M_('MULTIPLY', mu, mv), mz)
    vec = N('ShaderNodeCombineXYZ'); L(M_('FLOOR', u), vec.inputs[0]); L(M_('FLOOR', v), vec.inputs[1])
    wn = N('ShaderNodeTexWhiteNoise'); wn.noise_dimensions = '3D'; L(vec.outputs[0], wn.inputs['Vector'])
    lit_m = M_('MULTIPLY', M_('LESS_THAN', wn.outputs['Value'], cb=prob), win)
    nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.35; nz.inputs['Detail'].default_value = 4; L(tc.outputs['Object'], nz.inputs['Vector'])
    cr = N('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.35; cr.color_ramp.elements[1].position = 0.65; L(nz.outputs['Fac'], cr.inputs[0])
    w1 = N('ShaderNodeMix'); w1.data_type = 'RGBA'; w1.inputs[6].default_value = hexc(wall); w1.inputs[7].default_value = hexc(wall2); L(cr.outputs[0], w1.inputs[0])
    w2 = N('ShaderNodeMix'); w2.data_type = 'RGBA'; L(w1.outputs[2], w2.inputs[6]); w2.inputs[7].default_value = hexc(glass); L(win, w2.inputs[0])
    L(w2.outputs[2], bs.inputs['Base Color'])
    e = N('ShaderNodeMix'); e.data_type = 'RGBA'; e.inputs[6].default_value = (0, 0, 0, 1); e.inputs[7].default_value = hexc(lit); L(lit_m, e.inputs[0])
    L(e.outputs[2], bs.inputs['Emission Color']); bs.inputs['Emission Strength'].default_value = litk
    L(bs.outputs[0], out.inputs['Surface']); MATS[name] = m; return m

# ------------------------------------------------------------------ geometry builder (one object per material)
class MB:
    def __init__(self, name, parent=None): self.name = name; self.bm = {}; self.T = Matrix.Identity(4); self.stack = []; self.parent = parent
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
    def quad(self, m, v):
        bm = self._b(m); vs = [bm.verts.new(self.T @ Vector(p)) for p in v]
        try: bm.faces.new(vs)
        except ValueError: pass
    def finish(self, shadow=True, hull=None, group=None):
        """-> list of objects (one per material). parent: the MB's parent (root() for metre authoring). hull: ink hull thickness in the PARENT's units
        (metres under root): the whole group gets an inverted-hull outline (camera rays only). group: collection name."""
        objs = []
        for m, bm in self.bm.items():
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
            me = bpy.data.meshes.new('%s_%s' % (self.name, m.name)); bm.to_mesh(me); bm.free()
            ob = bpy.data.objects.new('%s_%s' % (self.name, m.name), me); ob.data.materials.append(m)
            bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = shadow; objs.append(ob)
            if self.parent is not None: ob.parent = self.parent
            if hull: add_hull(ob, hull)
        self.bm = {}; return objs

def rnd(s): return random.Random(s)

def palette():
    d = {}
    d['iron'] = mat('iron', '#b05a38', '#d27c4c', 5, contrast=1.2)                           # Eiffel red-brown paint
    d['ironlt'] = mat('ironlt', '#c46a40', '#e48c58', 5, contrast=1.2)
    d['redlead'] = mat('redlead', '#c8502a', '#ec7840', 6, aniso=(0.3, 1, 1), contrast=1.4)  # red-lead primed girders (orange-red)
    d['stone'] = mat('stone', '#cdbd9c', '#e2d4b4', 3.0, contrast=1.2)
    d['stonedk'] = mat('stonedk', '#a89878', '#c4b490', 4.0, contrast=1.4)
    d['timber'] = mat('timber', '#a87444', '#c89a64', 5, aniso=(1, 1, 0.25), contrast=1.4)
    d['timberdk'] = mat('timberdk', '#6e4220', '#946034', 5, aniso=(1, 1, 0.25), contrast=1.4)
    d['plank'] = mat('plank', '#b98448', '#dcaa6c', 6, aniso=(0.2, 1, 1), contrast=1.4)
    d['plankh'] = mat('plankh', '#b98448', '#dcaa6c', 6, aniso=(1, 0.2, 1), contrast=1.4)
    d['tarroof'] = mat('tarroof', '#4a3c3c', '#665454', 6)
    d['brick'] = mat('brick', '#a2402e', '#c25c3e', 9, aniso=(1, 1, 0.5), contrast=1.4)
    d['soot'] = mat('soot', '#2c2428', '#483a3a', 4)
    d['coal'] = mat_emit('coal', '#ff7a22', 22.0)
    d['rivet'] = mat_emit('rivet', '#ff9a40', 60.0)
    d['metal'] = mat('metal', '#6a707c', '#9096a2', 3, rough=0.4, sheen=0.5)
    d['dark'] = mat('dark', '#2a2024', '#40302e', 3)
    d['earth'] = mat('earth', '#c9895a', '#a86a44', 6, contrast=1.3)
    d['gravdk'] = mat('gravdk', '#8a5a3c', '#6e4630', 8, contrast=1.4)
    d['earthdk'] = mat('earthdk', '#8a5a3c', '#a86a44', 4, aniso=(1, 0.4, 1), contrast=1.3)
    d['grass'] = mat('grass', '#6f9440', '#a4ac48', 4, aniso=(1.2, 0.6, 1), contrast=1.5)
    d['grassdk'] = mat('grassdk', '#2e5446', '#46685a', 4, aniso=(1.2, 0.6, 1), contrast=1.5)
    d['gravel'] = mat('gravel', '#b09a7e', '#cdb898', 14, contrast=1.8)
    d['zinc'] = mat('zinc', '#5e6a7c', '#8a94a4', 4, rough=0.6, wave=(1.8, '#4e5a70'))
    d['zincf'] = mat('zincf', '#8c8e9c', '#a8aab6', 4, rough=0.6)
    d['zincdk'] = mat('zincdk', '#424e66', '#5c6a82', 4, rough=0.6, wave=(1.8, '#34405a'))
    d['hwallf'] = mat('hwallf', '#e4d0a8', '#d0b890', 0.05, contrast=1.0)
    d['hstone'] = mat('hstone', '#e8d8b4', '#f4e8c8', 3)
    d['chim'] = mat('chim', '#a6523a', '#c46e4c', 6)
    d['water'] = mat('water', '#4f7ea8', '#8cb0cc', 0.12, rough=0.15, sheen=0.8, contrast=0.8)
    d['leafA'] = mat('leafA', '#5a8a38', '#aab040', 2.2, contrast=1.6)
    d['leafB'] = mat('leafB', '#8a9a2c', '#e0a838', 2.2, contrast=1.6)
    d['leafN'] = mat('leafN', '#2e5a50', '#46786a', 2.2, contrast=1.6)
    d['trunk'] = mat('trunk', '#5a4030', '#7d5a44', 5, aniso=(1, 1, 0.3))
    d['horse'] = mat('horse', '#7a4020', '#a05c30', 4, contrast=1.3)
    d['horsedk'] = mat('horsedk', '#2c1e1a', '#3c2c26', 4)
    d['wk1'] = mat('wk1', '#4a5a7a', None, 1); d['wk2'] = mat('wk2', '#8a4a3a', None, 1); d['wk3'] = mat('wk3', '#5a6a4a', None, 1)
    d['canvas'] = mat('canvas', '#cdb27c', '#dcc490', 5)
    d['smoke'] = mat('smoke', '#d8cce0', '#a89cc0', 2, rough=1.0, emit='#b8a8d0', emit_k=0.25)
    d['forgeglow'] = mat_glow('forgeglow', '#ff7a2c', 3.0, 0.07)
    d['rope'] = mat('rope', '#9a7a48', '#7a5c34', 12)
    d['cream'] = mat('cream', '#f4ead0', '#e6d8b4', 3)
    d['sand'] = mat('sand', '#e6d3a8', '#f2e6c6', 3, contrast=0.8)
    d['dome'] = mat('dome', '#7a8aa8', '#9aaac6', 5, rough=0.5, sheen=0.3)
    d['gold'] = mat('gold', '#d4a840', '#f0cc68', 4, rough=0.3, sheen=0.8)
    d['brass'] = mat('brass', '#d7a23a', '#f2cf70', 4, rough=0.3, sheen=0.9)
    d['white'] = mat('white', '#f6efe0', '#e6dcc6', 4, contrast=0.7)
    d['cloth'] = mat('cloth', '#f0e6cc', '#dccfb2', 3, contrast=0.6)
    d['crimson'] = mat('crimson', '#a41f2c', '#c63a40', 5, contrast=1.2)
    d['crimdk'] = mat('crimdk', '#6a1220', '#8a2230', 6)
    d['floor'] = mat('floor', '#74401e', '#a06430', 7, aniso=(1, 0.2, 1), contrast=1.6, rough=0.4, sheen=0.4, wave=(7, '#5a2e16'))
    d['bent'] = mat('bent', '#5a2e18', '#7e4a28', 5, rough=0.4, sheen=0.5)
    d['glasswine'] = mat('glasswine', '#b8d8e8', '#e0f0f8', 3, rough=0.1, sheen=1.0)
    d['wineg'] = mat('wineg', '#2a6a44', '#3a8a5a', 3, rough=0.1, sheen=1.0)
    d['wineamb'] = mat('wineamb', '#a05a1c', '#c8802c', 3, rough=0.1, sheen=1.0)
    d['lamp'] = mat_emit('lamp', '#ffc468', 16.0)
    d['lampsm'] = mat_emit('lampsm', '#ffcf80', 11.0)
    d['wallres'] = mat('wallres', '#c8a878', '#d4b88a', 2.5, contrast=0.8)
    d['wallpan'] = mat('wallpan', '#491309', '#6b3723', 3, aniso=(1, 1, 0.5))
    d['navy'] = mat('navy', '#26395e', '#2f4670', 8, contrast=1.1)
    d['cardg'] = mat('cardg', '#6a6874', None, 1)
    d['mirror'] = mat('mirror', '#b6c8d8', '#dce8f2', 2, rough=0.08, sheen=1.0)
    d['grey'] = mat('grey', '#8c8a92', '#a8a6ae', 3)
    d['sparkc'] = mat_emit('sparkc', '#d8ecff', 90.0)
    d['sparkhalo'] = mat_glow('sparkhalo', '#9ac0ff', 6.0, 0.16)
    d['wirem'] = mat('wirem', '#f0e4d4', '#d8ccc0', 3, emit='#d8c8b8', emit_k=0.5)
    return d


# =============================================================================================== additions (film 20)
def lerp(a, b, k): return a + (b - a) * k
def mixhex(a, b, k):
    A = hexc(a) if isinstance(a, str) else a; B = hexc(b) if isinstance(b, str) else b
    return tuple(lerp(A[i], B[i], k) for i in range(4))
def col(c): return hexc(c) if isinstance(c, str) else tuple(c)

def palette_ext(d):
    """film-20 additions to the board palette (idempotent)"""
    d['earth2'] = mat('earth2', '#c98a54', '#b07444', 5, contrast=1.3)                    # lit trampled earth (QA SITE fix 1)
    d['earthpatch'] = mat('earthpatch', '#8a5a3a', '#a06a44', 7, contrast=1.5)
    d['ink'] = mat_ink_flat('inkflat', '#2a1712')
    d['hess'] = mat('hess', '#a88458', '#c4a070', 5, contrast=1.3)                         # tied hessian sacks
    d['redleadlt'] = mat('redleadlt', '#d05a30', '#f08a50', 6, aniso=(0.3, 1, 1), contrast=1.4)
    d['wk4'] = mat('wk4', '#7a5a8a', None, 1); d['wk5'] = mat('wk5', '#3a6a6a', None, 1)
    d['flag_r'] = mat('flag_r', '#c4303a', '#dc4a48', 3); d['flag_b'] = mat('flag_b', '#2c4aa8', '#3c5cc0', 3); d['flag_w'] = mat('flag_w', '#f2ead8', '#e4dcc6', 3)
    d['canvasw'] = mat('canvasw', '#e4d6b4', '#f0e4c4', 4)
    d['awn_r'] = mat('awn_r', '#b8302c', '#d4503c', 5, aniso=(0.25, 1, 1), contrast=1.6)
    d['awn_c'] = mat('awn_c', '#f0e4c8', '#e0d2b0', 5, aniso=(0.25, 1, 1), contrast=1.6)
    d['gravelp'] = mat('gravelp', '#cdb898', '#b09a7e', 14, contrast=1.8)
    d['pathg'] = mat('pathg', '#6a7a6c', '#869484', 5)
    d['brassb'] = mat('brassb', '#cba048', '#e8c068', 2, rough=0.25, sheen=0.9)
    d['vase'] = mat('vase', '#5a6a8a', '#7a8aaa', 3, rough=0.4, sheen=0.4)
    d['rubber'] = mat('rubber', '#2e3038', '#42444e', 3)
    d['wirep'] = mat('wirep', '#b4a99e', '#a89d92', 3, emit='#d8ccc0', emit_k=0.2)         # antenna wire, pale line (QA TOWER fix 1)
    return d

def mat_ink_flat(name, hexcol):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); bs = nt.nodes.new('ShaderNodeBsdfPrincipled'); bs.inputs['Base Color'].default_value = hexc(hexcol); bs.inputs['Roughness'].default_value = 0.8
    if 'Specular IOR Level' in bs.inputs: bs.inputs['Specular IOR Level'].default_value = 0.0
    nt.links.new(bs.outputs[0], out.inputs['Surface']); MATS[name] = m; return m

# ---- ink hull (inverted hull, camera rays only; hull(d) = 0.00384 x distance gives 3 px at 720 wide)
def mat_ink(name='ink_hull', ink_hex='#2a1712'):
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); geo = N('ShaderNodeNewGeometry'); lp = N('ShaderNodeLightPath')
    emi = N('ShaderNodeEmission'); emi.inputs['Color'].default_value = hexc(ink_hex)
    tr = N('ShaderNodeBsdfTransparent'); mix = N('ShaderNodeMixShader')
    notcam = N('ShaderNodeMath'); notcam.operation = 'SUBTRACT'; notcam.inputs[0].default_value = 1.0
    fac = N('ShaderNodeMath'); fac.operation = 'MAXIMUM'
    L(lp.outputs['Is Camera Ray'], notcam.inputs[1]); L(geo.outputs['Backfacing'], fac.inputs[0]); L(notcam.outputs[0], fac.inputs[1])
    L(fac.outputs[0], mix.inputs['Fac']); L(emi.outputs['Emission'], mix.inputs[1]); L(tr.outputs['BSDF'], mix.inputs[2]); L(mix.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m
def add_hull(ob, thickness):
    ob.data.materials.append(mat_ink())
    mod = ob.modifiers.new('ink_hull', 'SOLIDIFY'); mod.thickness = thickness; mod.offset = 1.0; mod.use_flip_normals = True; mod.use_rim = False
    mod.material_offset = len(ob.data.materials) - 1; mod.use_even_offset = True
    return mod
def hull_d(dist_D): return 0.00384 * dist_D

# ---- scaled root empty (metre authoring)
def root():
    r = STATE.get('root')
    if r is None or r.name not in bpy.data.objects:
        r = bpy.data.objects.new('root', None); r.scale = (SC, SC, SC); bpy.context.scene.collection.objects.link(r); STATE['root'] = r
    return r

# ---- keying helpers (as set3d16): every hook keys when frame=n is given (LINEAR; visibility CONSTANT)
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
def key(idb, path, frame, interp='LINEAR', index=-1):
    idb.keyframe_insert(path, frame=frame, index=index)
    for fc in _fcurves(idb):
        if fc.data_path == path:
            for kp in fc.keyframe_points:
                if abs(kp.co[0] - frame) < 1e-3: kp.interpolation = interp
def keysock(sock, value, frame, interp='LINEAR'):
    sock.default_value = value
    if frame is not None:
        sock.keyframe_insert('default_value', frame=frame)
        for fc in _fcurves(sock.id_data):
            if 'default_value' in fc.data_path:
                for kp in fc.keyframe_points:
                    if abs(kp.co[0] - frame) < 1e-3: kp.interpolation = interp
def setv(ob, vis, frame=None):
    ob.hide_render = not vis
    if frame is not None: key(ob, 'hide_render', frame, 'CONSTANT')
def show(objs, vis, frame=None):
    for o in (objs if isinstance(objs, (list, tuple)) else [objs]): setv(o, vis, frame)
def keyxf(ob, frame, loc=True, rot=False, scl=False, interp='LINEAR'):
    if loc: key(ob, 'location', frame, interp)
    if rot: key(ob, 'rotation_euler', frame, interp)
    if scl: key(ob, 'scale', frame, interp)
def clear_keys():
    """Drop every key the hooks inserted (objects, lights, cameras, node trees, world, scene) so plain calls hold again; keeps drivers."""
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

# ---- sky world, sun, lamps.  Light dict P: sky = 7 hex colours at SKYPOS (horizon at 0.5), sky_k, amb=(hex, k), key=(r,g,b,energy), key_dir (travel dir, world), sun_angle, exposure, sat
SKYPOS = [0.0, 0.05, 0.14, 0.30, 0.52, 0.76, 1.0]     # ramp position = sin(elevation) (the world's Generated z = direction z); everything below the horizon takes stop 0
def sky_world():
    w = bpy.data.worlds.new('sky'); bpy.context.scene.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputWorld'); bg = N('ShaderNodeBackground'); tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Generated'], sp.inputs[0])
    cr = N('ShaderNodeValToRGB'); cr.name = 'skyramp'; L(sp.outputs['Z'], cr.inputs[0]); bg.name = 'skybg'
    cr.color_ramp.elements[0].position = SKYPOS[0]
    for pos in SKYPOS[1:-1]: cr.color_ramp.elements.new(pos)
    cr.color_ramp.elements[-1].position = SKYPOS[-1]
    L(cr.outputs[0], bg.inputs['Color'])
    lp = N('ShaderNodeLightPath'); b2 = N('ShaderNodeBackground'); b2.name = 'ambbg'; mx = N('ShaderNodeMixShader')
    L(lp.outputs['Is Camera Ray'], mx.inputs[0]); L(b2.outputs[0], mx.inputs[1]); L(bg.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    STATE['world'] = w; return w
def make_sun():
    d = bpy.data.lights.new('key', 'SUN'); o = bpy.data.objects.new('key', d); bpy.context.scene.collection.objects.link(o); STATE['sun'] = o; return o
def apply_P(P, frame=None):
    """sun, sky ramp, ambient, exposure (and any STATE['lamps'] groups: {name: [(light_obj, base_energy)]} scaled by P[name]). Keyed when frame is given."""
    sc = bpy.context.scene; ks = STATE['sun']; d = ks.data; k = P['key']
    d.color = k[:3]; d.energy = k[3]; d.angle = math.radians(P.get('sun_angle', 1.0))
    ks.rotation_euler = (-Vector(P['key_dir']).normalized()).to_track_quat('Z', 'Y').to_euler()
    nt = STATE['world'].node_tree; cr = nt.nodes['skyramp']
    for el, c in zip(cr.color_ramp.elements, P['sky']): el.color = col(c)
    nt.nodes['skybg'].inputs['Strength'].default_value = P['sky_k']
    nt.nodes['ambbg'].inputs['Color'].default_value = col(P['amb'][0]); nt.nodes['ambbg'].inputs['Strength'].default_value = P['amb'][1]
    sc.view_settings.exposure = P.get('exposure', 0.0)
    for grp, base in STATE.get('lamps', {}).items():
        kk = P.get(grp, 1.0)
        for l, e in base: l.data.energy = e * kk
    if frame is not None:
        ks.keyframe_insert('rotation_euler', frame=frame); d.keyframe_insert('color', frame=frame); d.keyframe_insert('energy', frame=frame); d.keyframe_insert('angle', frame=frame)
        for i in range(len(SKYPOS)): nt.keyframe_insert('nodes["skyramp"].color_ramp.elements[%d].color' % i, frame=frame)
        for nm, sk in (('skybg', 'Strength'), ('ambbg', 'Strength'), ('ambbg', 'Color')): nt.nodes[nm].inputs[sk].keyframe_insert('default_value', frame=frame)
        sc.view_settings.keyframe_insert('exposure', frame=frame)
        for grp, base in STATE.get('lamps', {}).items():
            for l, e in base: l.data.keyframe_insert('energy', frame=frame)
    STATE['P'] = P
def lerpP(a, b, k):
    o = {}
    for key_ in a:
        va, vb = a[key_], b.get(key_, a[key_])
        if key_ == 'sky': o[key_] = [mixhex(x, y, k) for x, y in zip(va, vb)]
        elif key_ == 'amb': o[key_] = (mixhex(va[0], vb[0], k), lerp(va[1], vb[1], k))
        elif key_ == 'key': o[key_] = tuple(lerp(x, y, k) for x, y in zip(va, vb))
        elif key_ == 'key_dir': o[key_] = tuple(lerp(x, y, k) for x, y in zip(va, vb))
        elif isinstance(va, (int, float)): o[key_] = lerp(va, vb, k)
        else: o[key_] = va
    return o
def lamp(name, p_world, colour, energy, size=0.25, kind='POINT', rot=None, area=None, vis_cam=False, group=None):
    """point / area light at a world-D point. energy is authored for a metre-scale scene (power x SC^2 so it matches). group: STATE['lamps'] group for apply_P scaling."""
    sc = bpy.context.scene; l = bpy.data.lights.new(name, kind); l.color = colour[:3]; e = energy * SC * SC; l.energy = e
    if kind == 'POINT': l.shadow_soft_size = size * SC
    if kind == 'AREA' and area: l.shape = 'RECTANGLE'; l.size = area[0] * SC; l.size_y = area[1] * SC
    ob = bpy.data.objects.new(name, l); ob.location = p_world; sc.collection.objects.link(ob)
    if rot is not None: ob.rotation_euler = rot
    ob.visible_camera = vis_cam
    if group: STATE.setdefault('lamps', {}).setdefault(group, []).append((ob, e))
    return ob

# ---- render setup / grade / camera
FINAL_SPP = 8
def setup_render(scene, quality='final'):
    """final 720x1280, preview 360x640. Cycles CPU, ~8 spp + OpenImageDenoise (FAST prefilter), direct light + sky ambient only (no diffuse bounce), 2 threads, no DOF ever."""
    r = scene.render; c = scene.cycles; r.engine = 'CYCLES'; c.device = 'CPU'
    r.resolution_x, r.resolution_y = 720, 1280; r.resolution_percentage = 100 if quality in ('final', 'hq') else 50
    c.samples = {'final': STATE.get('spp', FINAL_SPP), 'hq': 24}.get(quality, 6)
    c.use_denoising = True; c.denoiser = 'OPENIMAGEDENOISE'; c.denoising_input_passes = 'RGB_ALBEDO_NORMAL'; c.denoising_prefilter = 'FAST'
    c.use_adaptive_sampling = False; c.max_bounces = 2; c.diffuse_bounces = STATE.get('dbounce', 0); c.glossy_bounces = 1; c.transmission_bounces = 0; c.transparent_max_bounces = 8
    c.use_light_tree = False; c.filter_width = 1.2; r.threads_mode = 'FIXED'; r.threads = 2
    scene.view_settings.view_transform = 'Standard'; scene.view_settings.look = 'None'
    r.image_settings.file_format = 'PNG'; r.image_settings.color_mode = 'RGB'; r.film_transparent = False
    setup_grade(scene, STATE.get('P', {}))
def setup_grade(scene, P):
    """film-wide mild saturation (the board's grade sat 1.08), no recolour: compositor from spec/grade_compositor."""
    sys.path.insert(0, os.path.join(PROJ, 'spec'))
    import warnings, grade_compositor as G
    for ng in list(bpy.data.node_groups):
        if ng.name.startswith('GradeCLP'): bpy.data.node_groups.remove(ng)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        G.build(scene, preset=dict(vignette_strength=0.0, bloom_strength=0.0, offset=(0.0, 0.0, 0.0), saturation=float(P.get('sat', 1.08))))
    scene.render.use_compositing = True
def apply_dof(*a, **k): return None          # client rule: no depth of field at all (API symmetry)
def make_camera(setup, name='cam', scene=None):
    """22 mm / 36 mm sensor camera from {loc, look_at, lens[, roll, shift]} (world D): DOF OFF, clip 0.05..6000; becomes the scene camera."""
    scene = scene or bpy.context.scene
    ob = bpy.data.objects.get(name)
    if ob is None:
        cd = bpy.data.cameras.new(name); ob = bpy.data.objects.new(name, cd); scene.collection.objects.link(ob)
    cd = ob.data; cd.lens = setup.get('lens', 22); cd.sensor_width = 36; cd.sensor_fit = 'AUTO'; cd.clip_start = 0.05; cd.clip_end = 6000; cd.dof.use_dof = False
    cd.shift_y = setup.get('shift', 0.0)
    ob.location = setup['loc']; ob.rotation_euler = (Vector(setup['look_at']) - Vector(setup['loc'])).to_track_quat('-Z', 'Y').to_euler()
    if setup.get('roll'): ob.rotation_euler.rotate_axis('Z', math.radians(setup['roll']))
    scene.camera = ob; STATE['cam'] = ob; return ob
def render(path, scene=None):
    scene = scene or bpy.context.scene; scene.render.filepath = path
    t0 = time.time(); c0 = os.times(); bpy.ops.render.render(write_still=True); c1 = os.times()
    return time.time() - t0, (c1.user - c0.user) + (c1.system - c0.system)
def project(world_pt):
    """(x_px, y_px) of a world point (D) in the scene camera (720x1280, y from the top)"""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; p = world_to_camera_view(sc, sc.camera, Vector(world_pt)); return round(p.x * 720), round((1 - p.y) * 1280)

# ---- placeholder actors (cast20 puppets as cards). roles = cast20 names; HEIGHT in D
HEIGHT = dict(eiffel=3.2, eiffel_old=3.1, maupassant=3.1, painter20=3.1, composer20=3.2, architect20=3.3, poet20=3.2, riveter_tongs=3.2, riveter_hammer=3.2, riveter_forge=3.2,
              telegraphist=3.2, officer=3.3, official=3.2, waiter=3.3, lady20=3.1, gent20=3.3, child20=2.4)
POSE = dict(yaw=0.2, expr='neutral', arm_l='down', arm_r='down', legs='stand')
def _import_tower():
    for p in (os.path.join(PROJ, 'v3', 'set3d2'), os.path.join(PROJ, 'v3', 'cast20'), os.path.join(PROJ, 'v3', 'cast')):
        if p not in sys.path: sys.path.insert(0, p)
    import tower as T, cast20                                        # noqa: F401  (cast20 registers its characters in puppet)
    for role, h in HEIGHT.items():
        if role not in T.PH: T.PH[role] = (role, dict(POSE), h)
    return T
def placeholder_actor(role, mark, face_to=None, tilt=0.0, name=None, ppd=256, pose=None, height=None):
    """Stand-in card (cast20 puppet as a lit-free card, alpha cut-out, blocks the key) scaled to HEIGHT[role] D, standing at `mark` (x, y, ground z D), facing `face_to`.
    pose: dict of puppet pose keys merged over the default (e.g. dict(expr='proud', arm_r='up')); height overrides HEIGHT."""
    T = _import_tower(); old = T.PH[role]
    T.PH[role] = (old[0], dict(old[1], **(pose or {})), height or old[2])
    try: ob = T.placeholder_actor(role, tuple(mark), face_to=face_to, tilt=tilt, name=name, ppd=ppd)
    finally: T.PH[role] = old
    return ob
def clear_actors():
    for o in list(bpy.context.scene.objects):
        if o.name.startswith('actor_'): bpy.data.objects.remove(o, do_unlink=True)
def staging_list(cam_name):
    """[(role, mark_xyz, opts)] for a camera: STATE['staging'][cam] = [(role, markname | xyz [, opts dict])]"""
    out = []
    for it in STATE.get('staging', {}).get(cam_name, []):
        role, mk = it[0], it[1]; opts = it[2] if len(it) > 2 else {}
        out.append((role, tuple(STATE['marks'][mk]) if isinstance(mk, str) else tuple(mk), opts))
    return out
def stage_placeholders(A, cam_name, cam_loc=None):
    """cards for every staged role of cam_name, facing the camera (lean back for high cameras)"""
    clear_actors(); out = []; cam_loc = cam_loc or A['cams'][cam_name]['loc']
    for i, (role, mk, opts) in enumerate(staging_list(cam_name)):
        d = Vector(cam_loc) - Vector(mk); el = math.degrees(math.atan2(d.z - 1.5, math.hypot(d.x, d.y)))
        ft = opts.get('face_to', cam_loc)
        out.append(placeholder_actor(role, mk, face_to=ft, tilt=opts.get('tilt', max(0.0, el - 35) * 0.6), name='actor_%s_%d' % (role, i), pose=opts.get('pose'), height=opts.get('height')))
    return out
def head_pixels(cam_name):
    """[(role, mark, head_centre_y_px, head_px, chin_y_px, feet_y_px, head_x_px)] at 720x1280 (caption rule: chin < 880)"""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; cam = sc.camera; out = []
    for role, mk, opts in staging_list(cam_name):
        h = opts.get('height') or HEIGHT[role]; m = Vector(mk); top, hc, bot = m + Vector((0, 0, h)), m + Vector((0, 0, h - 0.5)), m + Vector((0, 0, h - 1.0))
        p, q, b = (world_to_camera_view(sc, cam, v) for v in (hc, top, bot)); f = world_to_camera_view(sc, cam, m)
        out.append((role, tuple(round(v, 2) for v in mk), round((1 - p.y) * 1280), round(abs(q.y - b.y) * 1280), round((1 - b.y) * 1280), round((1 - f.y) * 1280), round(p.x * 720)))
    return out

def reset(loc, preset, light, spp=None, dbounce=0):
    """wipe the scene, clear MATS / STATE, create world + sun, and return the palette. Both builders call this first."""
    bpy.ops.wm.read_factory_settings(use_empty=True); MATS.clear(); STATE.clear(); STATE.update(loc=loc, preset=preset, light=light, marks={}, staging={}, lamps={}, dbounce=dbounce)
    if spp: STATE['spp'] = spp
    sky_world(); make_sun()
    M = palette(); palette_ext(M); STATE['M'] = M
    M['hwall'] = mat_windows('hwall', '#efdfba', '#e0cb9e', '#4a5882', '#ffc070', 0.0, 0.0)
    M['hwalld'] = mat_windows('hwalld', '#efdfba', '#e0cb9e', '#2c3460', '#ffc070', 5.0, 0.42)
    M['hwallt'] = mat_windows('hwallt', '#e8d4a6', '#d8c08e', '#4a5882', '#ffc070', 0.0, 0.3, (6.0, 8.0), (0.3, 0.6), 2.0)
    M['hwalltd'] = mat_windows('hwalltd', '#e8d4a6', '#d8c08e', '#2c3460', '#ffc070', 5.0, 0.3, (6.0, 8.0), (0.3, 0.6), 2.0)
    M['galwall'] = mat_windows('galwall', '#d0aa80', '#b8906a', '#5a3a30', '#ffc468', 4.0, 0.8, (4.0, 4.0), (0.55, 0.6), 0.5)
    return M

# ---- "in shade" material variants for foreground dressing (so the lens-side props read as shaded without any shadow caster)
def shade_variant(m, tint=(0.30, 0.38, 0.64)):
    name = m.name + '_sh'
    if name in bpy.data.materials: return bpy.data.materials[name]
    n2 = m.copy(); n2.name = name; nt = n2.node_tree; bs = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeBsdfPrincipled']
    if not bs: return m
    bs = bs[0]; inp = bs.inputs['Base Color']; mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs[0].default_value = 1.0
    mx.inputs[7].default_value = (tint[0], tint[1], tint[2], 1.0)
    if inp.is_linked:
        src = inp.links[0].from_socket; nt.links.new(src, mx.inputs[6])
    else: mx.inputs[6].default_value = inp.default_value
    nt.links.new(mx.outputs[2], inp); return n2
class ShadeMats(dict):
    """dict view of a palette whose entries are returned as shade variants (emissive 'lamp*' / 'coal' / 'rivet' / glow stay as they are)"""
    def __init__(self, M): super().__init__(); self.M = M
    def __missing__(self, k):
        m = self.M[k]
        if k.startswith(('lamp', 'coal', 'rivet', 'spark', 'glow', 'smoke')): v = m
        else: v = shade_variant(m)
        self[k] = v; return v

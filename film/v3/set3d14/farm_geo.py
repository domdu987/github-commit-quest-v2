"""set3d14 geometry kit: materials, mesh builder (MB) and every prop of the Kenyan smallholding. No scene logic here; farm.py uses it.
World units: metres. Look: flat-ish painterly two-tone noise materials, real geometry, one hard key (see farm.py)."""
import os, sys, math, random
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix, Euler

def lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def hexc(h):
    h = h.lstrip('#'); return tuple(lin(int(h[i:i + 2], 16)) for i in (0, 2, 4)) + (1.0,)
def rnd(s): return random.Random(s)
def R(a, b, rr): return a + (b - a) * rr.random()

# ------------------------------------------------------------------ materials
MATS = {}
def mat(name, A, B=None, scale=3.0, aniso=(1, 1, 1), rough=1.0, emit=None, emit_k=0.0, zgrad=None, wave=None, sheen=0.0, contrast=1.0, alpha=None):
    """Principled diffuse with a two-tone object-space noise mix. zgrad=(z0,z1,hexLow): hexLow below z0 -> A/B above z1 (object z).
    wave=(freq, hexStripe): stripes along x. emit: emission hex with strength emit_k."""
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled')
    bs.inputs['Roughness'].default_value = rough
    if 'Specular IOR Level' in bs.inputs: bs.inputs['Specular IOR Level'].default_value = 0.0 if sheen == 0 else sheen
    tc = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (scale * aniso[0], scale * aniso[1], scale * aniso[2])
    L(tc.outputs['Object'], mp.inputs['Vector'])
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
    surf = bs.outputs[0]
    if alpha is not None:
        tr = N('ShaderNodeBsdfTransparent'); mxs = N('ShaderNodeMixShader'); mxs.inputs[0].default_value = alpha; L(tr.outputs[0], mxs.inputs[1]); L(bs.outputs[0], mxs.inputs[2]); surf = mxs.outputs[0]
    L(surf, out.inputs['Surface'])
    MATS[name] = m; return m

def mat_emit(name, hexcol, k):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = hexc(hexcol); em.inputs['Strength'].default_value = k
    nt.links.new(em.outputs[0], out.inputs['Surface']); MATS[name] = m; return m

def mat_glow(name, hexcol, k, alpha=0.5):
    """translucent emissive (wing blur, halos): Emission mixed with Transparent."""
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    em.inputs['Color'].default_value = hexc(hexcol); em.inputs['Strength'].default_value = k; mx.inputs[0].default_value = alpha
    L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface']); MATS[name] = m; return m

def mat_card(name, png, k=1.0):
    """emission-only card (stage convention): the PNG colours + alpha, never lit; shadow-casting through alpha."""
    if name in MATS: return MATS[name]
    img = bpy.data.images.load(png); img.alpha_mode = 'STRAIGHT'
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); ti = N('ShaderNodeTexImage'); ti.image = img; ti.interpolation = 'Linear'; ti.extension = 'CLIP'
    em = N('ShaderNodeEmission'); em.inputs['Strength'].default_value = k; tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    L(ti.outputs['Color'], em.inputs['Color']); L(ti.outputs['Alpha'], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    m['card_em'] = em.name; MATS[name] = m; return m

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
    def cone(self, m, c, r0, r1, h, seg=16):
        self.rod(m, (c[0], c[1], c[2]), (c[0], c[1], c[2] + h), r0, r1, seg)
    def quad(self, m, v):
        bm = self._b(m); vs = [bm.verts.new(self.T @ Vector(p)) for p in v]
        try: bm.faces.new(vs)
        except ValueError: pass
    def tri(self, m, v): self.quad(m, v)
    def poly(self, m, pts, r0, r1=None, seg=6, smooth=True):
        n = len(pts) - 1
        for i in range(n):
            a = r0 + ((r1 if r1 is not None else r0) - r0) * i / max(1, n); b = r0 + ((r1 if r1 is not None else r0) - r0) * (i + 1) / max(1, n)
            self.rod(m, pts[i], pts[i + 1], a, b, seg, caps=(i == 0 or i == n - 1), smooth=smooth)
    def lathe(self, m, c, prof, seg=16, smooth=True):
        """surface of revolution about z through c; prof = [(r, z), ...] bottom to top (a r of 0 closes the end)."""
        bm = self._b(m); rings = []
        for (r, z) in prof:
            ring = [bm.verts.new(self.T @ Vector((c[0] + r * math.cos(2 * math.pi * i / seg), c[1] + r * math.sin(2 * math.pi * i / seg), c[2] + z))) for i in range(seg)]
            rings.append(ring)
        for a, b in zip(rings[:-1], rings[1:]):
            for i in range(seg):
                j = (i + 1) % seg
                try:
                    f = bm.faces.new([a[i], a[j], b[j], b[i]]); f.smooth = smooth
                except ValueError: pass
    def corrugated(self, m, o, dv, av, nv, length, width, rib=0.075, amp=0.018, lsteps=1):
        """corrugated panel: origin o, direction down the ribs dv (unit), across av (unit), outward normal nv; real sine ribs."""
        o = Vector(o); dv = Vector(dv); av = Vector(av); nv = Vector(nv); k = 4; n = max(2, int(width / rib * k)); bm = self._b(m)
        cols = []
        for i in range(n + 1):
            u = i * width / n; off = amp * math.sin(2 * math.pi * u / rib)
            col = [bm.verts.new(self.T @ (o + av * u + dv * (length * j / lsteps) + nv * off)) for j in range(lsteps + 1)]; cols.append(col)
        for a, b in zip(cols[:-1], cols[1:]):
            for j in range(lsteps):
                try:
                    f = bm.faces.new([a[j], b[j], b[j + 1], a[j + 1]]); f.smooth = True
                except ValueError: pass
    def finish(self, coll=None, shadow=True, join=False):
        objs = []
        shadow = shadow and self.name not in ('moon', 'hills')
        for m, bm in self.bm.items():
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
            me = bpy.data.meshes.new('%s_%s' % (self.name, m.name)); bm.to_mesh(me); bm.free()
            ob = bpy.data.objects.new('%s_%s' % (self.name, m.name), me); ob.data.materials.append(m)
            (coll or bpy.context.scene.collection).objects.link(ob); ob.visible_shadow = shadow; objs.append(ob)
        self.bm = {}
        if join and len(objs) > 1: objs = [join_objs(objs)]
        return objs

def join_objs(objs):
    for o in bpy.context.selected_objects: o.select_set(False)
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join(); o = objs[0]; o.select_set(False); return o

# ------------------------------------------------------------------ palette
def palette(mode):
    d = {}
    night = mode == 'NIGHT'
    d['maize'] = mat('maize', '#6c9a2c', '#c2b13a', 5, contrast=1.4, zgrad=(0.0, 1.3, '#3d6a22'))
    d['maize2'] = mat('maize2', '#85a935', '#d3c248', 5, contrast=1.3, zgrad=(0.0, 1.2, '#4a7a28'))
    d['maizedry'] = mat('maizedry', '#b09a42', '#d4bd62', 5, contrast=1.3)
    d['stalk'] = mat('stalk', '#8f9a45', '#b8a850', 6)
    d['cob'] = mat('cob', '#e0c24a', '#9bb04a', 8)
    d['husk'] = mat('husk', '#9fb24a', '#c7c070', 8)
    d['tassel'] = mat('tassel', '#d9b45a', '#e8d27a', 8)
    d['wood'] = mat('wood', '#6b3f22', '#8a5530', 6, aniso=(1, 1, 0.25), contrast=1.5)
    d['woodpale'] = mat('woodpale', '#b0763e', '#d09a58', 8, aniso=(0.3, 1, 1))
    d['woodgrey'] = mat('woodgrey', '#8a7a68', '#b0a088', 8, aniso=(1, 1, 0.3))
    d['hive'] = mat('hive', '#b5763a', '#d7a05a', 7, aniso=(0.4, 1, 1))
    d['hivetop'] = mat('hivetop', '#cf9650', '#e6bb78', 9, aniso=(0.3, 1, 1))
    # tin: pale galvanised with warm rust freckles (soft, no dark blotches); underside is warm planks lit by ground bounce
    d['tin'] = mat('tin', '#b9c2c8', '#c79a72', 1.3, rough=0.55, sheen=0.35, contrast=0.8)
    d['tinunder'] = mat('tinunder', '#d9a46c', '#e2b47c', 1.6, contrast=0.5, emit='#c98f58', emit_k=0.55)
    d['tin2'] = mat('tin2', '#6f93b3', '#9ab0c0', 1.3, rough=0.55, sheen=0.3, contrast=0.8)
    d['tinred'] = mat('tinred', '#b8553a', '#cf7a54', 1.3, rough=0.55, sheen=0.3, contrast=0.9)
    d['thatch'] = mat('thatch', '#b08a40', '#dfbf68', 8, aniso=(1.6, 1.6, 0.25), contrast=1.8, zgrad=(1.8, 3.6, '#7a5a2c'))
    d['thatchold'] = mat('thatchold', '#917040', '#c0a060', 8, aniso=(1.6, 1.6, 0.25), contrast=1.8)
    d['thatchlow'] = mat('thatchlow', '#6f5428', '#8f7038', 9, contrast=1.5)
    d['mud'] = mat('mud', '#b2552f', '#cf7c4c', 3.5, contrast=1.3, zgrad=(0.0, 0.9, '#8c3f26'))
    d['mudpale'] = mat('mudpale', '#d9a273', '#c98b5e', 3.0)
    d['ochre'] = mat('ochre', '#e0b25c', '#cf9a48', 3.0)
    d['plaster'] = mat('plaster', '#4aa3a0', '#6cbdb4', 2.5, zgrad=(0.0, 0.6, '#3a7f80'))
    d['plaster2'] = mat('plaster2', '#e6c88a', '#d8b070', 2.5, zgrad=(0.0, 0.6, '#b08a58'))
    d['plaster3'] = mat('plaster3', '#e8dcc0', '#d6c8a8', 2.5, zgrad=(0.0, 0.6, '#a8906a'))
    d['dark'] = mat('dark', '#3a2830', '#4c3438', 3)
    d['door'] = mat('door', '#2e5aa0', '#4474b8', 5, aniso=(0.3, 1, 1))
    d['doorred'] = mat('doorred', '#b04830', '#c86040', 5, aniso=(0.3, 1, 1))
    d['jerry'] = mat('jerry', '#f2c21c', '#e4a512', 4, rough=0.45, sheen=0.3)
    d['jcap'] = mat('jcap', '#2f5a9a', '#2f5a9a')
    d['metal'] = mat('metal', '#b9c4d0', '#8e9cae', 3, rough=0.4, sheen=0.4)
    d['bluetank'] = mat('bluetank', '#2f6fb8', '#4a8ad0', 2, rough=0.5, sheen=0.3)
    d['wire'] = mat('wire', '#f4ecdc', '#d0c8b4', 2, rough=0.3, sheen=0.5, emit='#ffe0b0', emit_k=0.3)
    d['rope'] = mat('rope', '#cfae74', '#a88650', 12)
    d['stone'] = mat('stone', '#8c8296', '#b0a6aa', 3)
    d['stonewarm'] = mat('stonewarm', '#a8967e', '#c8b498', 3)
    d['leafgreen'] = mat('acacia', '#6b8a2a', '#a8a83c', 2.4, contrast=1.6)
    d['acacia2'] = mat('acacia2', '#5c8030', '#94a038', 2.4, contrast=1.6)
    d['trunk'] = mat('trunk', '#4a3228', '#6d4a36', 5, aniso=(1, 1, 0.3))
    d['banana'] = mat('banana', '#4fa03a', '#9cc24a', 3, contrast=1.4)
    d['bananadry'] = mat('bananadry', '#9a8a3a', '#c4b060', 3, contrast=1.4)
    d['grass'] = mat('grassblade', '#b39c3a', '#d4be5a', 6, zgrad=(0.0, 0.7, '#6a8a30'))
    d['grassgreen'] = mat('grassgreen', '#7aa032', '#a8c04a', 6, zgrad=(0.0, 0.5, '#4a7a28'))
    d['goat'] = mat('goat', '#ece2cc', '#d6c8a8', 1.5, contrast=1.2)
    d['goatbrown'] = mat('goatbrown', '#8a5430', '#a8683a', 2.5, contrast=1.3)
    d['goatblack'] = mat('goatblack', '#3a2c2a', '#52403a', 2.5)
    d['hen'] = mat('hen', '#a8582e', '#d8b078', 4, contrast=0.9)
    d['henwhite'] = mat('henwhite', '#eee4d0', '#d8c8a8', 4, contrast=0.8)
    d['henblack'] = mat('henblack', '#3a3434', '#2c4a44', 4, contrast=0.8, sheen=0.4)
    d['comb'] = mat('comb', '#d8382c', '#d8382c')
    d['beak'] = mat('beak', '#e0a030', '#e0a030')
    d['eye'] = mat('eye', '#1c1418', '#1c1418')
    d['bee'] = mat('bee', '#4a3414', '#b8841c', 40, contrast=2)
    d['beegold'] = mat('beegold', '#f0b82a', '#f0b82a', emit='#e8a020', emit_k=0.35)
    d['beeblack'] = mat('beeblack', '#3c2a1a', '#3c2a1a')
    d['beewing'] = mat_glow('beewing', '#e8f0ff', 1.3, 0.38)
    d['tusk'] = mat('tusk', '#cfc8b8', '#cfc8b8')
    d['ember'] = mat_emit('ember', '#ff7a2a', 9.0)
    d['basket'] = mat('basket', '#b88a4a', '#8a5f30', 14)
    d['char'] = mat('char', '#3a2a26', '#4a3630', 4)
    d['flame'] = mat_emit('flame', '#ff9a30', 14.0)
    d['flame2'] = mat_emit('flame2', '#ffd060', 22.0)
    d['lamp'] = mat_emit('lamp', '#ffc070', 30.0 if night else 3.0)
    d['winlit'] = mat_emit('winlit', '#ffb860', 14.0) if mode in ('NIGHT', 'DUSK') else mat('winday', '#3a4a6e', '#52668a', 3)
    d['clay'] = mat('clay', '#b45a32', '#d08050', 5, contrast=1.2)
    d['claydark'] = mat('claydark', '#6a3a28', '#8a4c30', 5)
    d['cloth_red'] = mat('cloth_red', '#d6402a', '#e8603a', 4)
    d['cloth_blue'] = mat('cloth_blue', '#2f5fb0', '#4a7ad0', 4)
    d['cloth_yel'] = mat('cloth_yel', '#f0c030', '#f8d860', 4)
    d['cloth_grn'] = mat('cloth_grn', '#3f9a50', '#60b868', 4)
    d['cloth_wht'] = mat('cloth_wht', '#f2ead8', '#e0d6c0', 4)
    d['cloth_org'] = mat('cloth_org', '#e8802a', '#f09a48', 4)
    d['sack'] = mat('sack', '#c8b080', '#a89060', 9, contrast=1.3)
    d['pumpkin'] = mat('pumpkin', '#e08a28', '#f0a840', 3, contrast=1.2)
    d['vine'] = mat('vine', '#4a7a2c', '#78a040', 5)
    d['sunflower'] = mat('sunflower', '#f4c424', '#f8d850', 8)
    d['sfcenter'] = mat('sfcenter', '#5a3a1c', '#7a5028', 20)
    d['kale'] = mat('kale', '#3c8a44', '#78b050', 5, contrast=1.4, zgrad=(0.0, 0.3, '#2a6a38'))
    d['bean'] = mat('bean', '#5a9a38', '#98c050', 5)
    d['flowerA'] = mat('flowerA', '#f4d848', '#f4d848')
    d['flowerB'] = mat('flowerB', '#f08030', '#f08030')
    d['flowerC'] = mat('flowerC', '#f4f0e0', '#f4f0e0')
    d['flowerD'] = mat('flowerD', '#e04830', '#e04830')
    d['thorn'] = mat('thorn', '#6a5a48', '#8a7860', 10, contrast=1.4)
    d['thornleaf'] = mat('thornleaf', '#7a8a3a', '#a8a050', 6)
    d['tincan'] = mat('tincan', '#c8d0d8', '#9aa6b4', 3, rough=0.4, sheen=0.5)
    d['dust'] = mat('dust', '#c88a58', '#b87848', 3)
    d['foot'] = mat('foot', '#6a3a28', '#7a4630', 3)
    d['smoke'] = mat('smoke', '#d8d4dc', '#b8b8cc', 1.5, alpha=0.7)
    d['cloud'] = mat('cloud', '#fff0dc' if not night else '#8c9acc', '#ffe0c0' if not night else '#6c7cb8', 0.5, contrast=1.0)
    d['bird'] = mat('bird', '#f6f0e4', '#f6f0e4')
    d['birddark'] = mat('birddark', '#4a3a4a', '#4a3a4a')
    d['giraffe'] = mat('giraffe', '#d8a050', '#a8683a', 4, contrast=2.5)
    d['torch'] = mat('torch', '#6a4630', '#8a5a38', 6)
    d['pot'] = mat('pot', '#8a96a4', '#b0bac6', 3, rough=0.4, sheen=0.5)
    d['glass'] = mat('glass', '#aac8d8', '#c8e0ec', 3, rough=0.2, sheen=0.5)
    d['bike'] = mat('bike', '#c43c2c', '#d85a3c', 3, rough=0.4, sheen=0.4)
    d['rubber'] = mat('rubber', '#2e2628', '#3a3032', 3)
    d['bark2'] = mat('bark2', '#7a6048', '#a08868', 5, aniso=(1, 1, 0.3))
    d['rock'] = mat('rock', '#8a8298', '#b4aab0', 2.2, contrast=1.6)
    d['rockwarm'] = mat('rockwarm', '#a08a78', '#c8b098', 2.2, contrast=1.6)
    return d

# ------------------------------------------------------------------ props
def hut_round(mb, M, c, r=1.75, h=2.0, rt=2.45, ht=2.0, door_yaw=0.0, thatch='thatch', walls='mud', band='ochre', seed=0):
    x, y, z = c; rr = rnd(seed + 5)
    mb.lathe(M[walls], (x, y, z), [(r + 0.12, -0.05), (r + 0.1, 0.35), (r + 0.02, 0.4), (r, h)], 28)
    mb.lathe(M[band], (x, y, z), [(r + 0.125, 0.0), (r + 0.125, 0.3)], 28)                       # painted base band
    for i in range(14):                                                                          # base stones
        a = i / 14 * 6.283 + rr.uniform(-.1, .1); mb.ell(M['stone'], (x + math.cos(a) * (r + 0.1), y + math.sin(a) * (r + 0.1), z + 0.1), (0.22, 0.14, 0.12), (8, 5), (0, 0, a))
    # thatch: 3 layered shaggy cones + fringe of grass bundles
    mb.cone(M[thatch], (x, y, z + h - 0.05), rt, 0.05, ht, 32)
    mb.cone(M[thatch], (x, y, z + h - 0.12), rt + 0.08, rt * 0.62, 0.28, 32)
    mb.cone(M['thatchlow'], (x, y, z + h - 0.4), rt + 0.05, rt + 0.0, 0.35, 32)
    for i in range(40):
        a = i / 40 * 6.283 + rr.uniform(-.08, .08)
        p0 = Vector((x + math.cos(a) * (rt + 0.05), y + math.sin(a) * (rt + 0.05), z + h - 0.25)); p1 = p0 + Vector((math.cos(a) * 0.06, math.sin(a) * 0.06, -rr.uniform(0.2, 0.42)))
        mb.rod(M['thatchlow'], p0, p1, 0.035, 0.012, 4, caps=False)
    for k in range(3):
        zz = z + h + 0.35 + k * (ht - 0.8) / 3; rad = rt * (1 - (0.35 + k * (ht - 0.8) / 3) / ht) + 0.04
        mb.lathe(M['thatchold'], (x, y, z), [(rad + 0.05, zz - z - 0.06), (rad + 0.04, zz - z + 0.08)], 28)
    mb.rod(M['wood'], (x, y, z + h + ht - 0.1), (x, y, z + h + ht + 0.4), 0.05, 0.02, 6)
    mb.ell(M['clay'], (x, y, z + h + ht + 0.42), (0.1, 0.1, 0.12), (8, 6))
    # door + window + lintel on door_yaw side (local -y)
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, door_yaw)).to_matrix().to_4x4())
    mb.box(M['dark'], (0, -r + 0.02, 0.82), (0.78, 0.14, 1.62))
    mb.box(M['door'], (0.2, -r - 0.04, 0.82), (0.4, 0.05, 1.5), rz=0.0)                           # door leaf ajar
    mb.box(M['wood'], (0, -r - 0.06, 1.7), (1.0, 0.13, 0.12)); mb.box(M['wood'], (-0.46, -r - 0.06, 0.85), (0.1, 0.13, 1.7)); mb.box(M['wood'], (0.46, -r - 0.06, 0.85), (0.1, 0.13, 1.7))
    mb.box(M['stonewarm'], (0, -r - 0.35, 0.06), (1.3, 0.55, 0.12))
    for sgn in (1, -1):                                                                          # small window with shutter
        a = sgn * 1.05; mb.box(M['dark'], (math.sin(a) * (r - 0.02), -math.cos(a) * (r - 0.02), 1.15), (0.34, 0.1, 0.34), rz=a)
    mb.pop()

def house_tin(mb, M, c, sx=7.0, sy=4.0, h=2.7, yaw=0.0, roof='tin', walls='plaster', seed=0, door='door'):
    x, y, z = c; rr = rnd(seed + 9)
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M[walls], (0, 0, h / 2), (sx, sy, h)); mb.box(M['stone'], (0, 0, 0.17), (sx + 0.14, sy + 0.14, 0.34))
    ov = 0.75; rh = 1.35; hw = sy / 2 + ov; x0 = -sx / 2 - ov; x1 = sx / 2 + ov
    slope = math.hypot(hw, rh + 0.25)
    for sgn in (-1, 1):                                                                          # corrugated roof panels with real ribs
        o = (x0, sgn * hw, h - 0.25); dv = Vector((0, -sgn * hw, rh + 0.25)).normalized(); nv = Vector((0, sgn * (rh + 0.25), hw)).normalized()
        mb.corrugated(M[roof], o, dv, (1, 0, 0), nv, slope, x1 - x0, 0.1, 0.026)
        o2 = Vector(o) - nv * 0.03; mb.corrugated(M['tinunder'], o2, dv, (1, 0, 0), -nv, slope, x1 - x0, 0.1, 0.02)
        mb.box(M['woodpale'], (0, sgn * (hw - 0.02), h - 0.34), (x1 - x0, 0.1, 0.1))               # fascia
    for ex in (-sx / 2, sx / 2): mb.tri(M[walls], [(ex, -sy / 2, h), (ex, sy / 2, h), (ex, 0, h + rh - 0.25)])
    mb.box(M['metal'], (0, 0, h + rh), (sx + 1.6, 0.16, 0.1))
    mb.rod(M['metal'], (x1 - 0.3, -hw + 0.1, h - 0.4), (x1 - 0.3, -hw + 0.1, 0.5), 0.05, 0.05, 6)  # downpipe
    mb.box(M[door], (-1.3, -sy / 2 - 0.03, 1.1), (1.0, 0.1, 2.1)); mb.box(M['dark'], (-1.3, -sy / 2 - 0.08, 1.1), (0.8, 0.04, 1.9))
    mb.box(M['wood'], (-1.3, -sy / 2 - 0.06, 2.2), (1.2, 0.12, 0.1))
    for wx in (0.7, 2.3):
        mb.box(M['wood'], (wx, -sy / 2 - 0.04, 1.5), (1.0, 0.1, 1.0)); mb.box(M['winlit'], (wx, -sy / 2 - 0.09, 1.5), (0.8, 0.04, 0.8))
        mb.box(M['wood'], (wx, -sy / 2 - 0.1, 1.5), (0.06, 0.04, 0.8)); mb.box(M['wood'], (wx, -sy / 2 - 0.1, 1.5), (0.8, 0.04, 0.06))
    mb.box(M['stone'], (-1.3, -sy / 2 - 0.7, 0.1), (1.5, 0.9, 0.2))
    for dx in (-2.8, -0.2, 2.8):                                                                 # veranda poles
        mb.rod(M['wood'], (dx, -sy / 2 - 1.1, 0), (dx, -sy / 2 - 1.1, h - 0.1), 0.07, 0.06, 6)
    mb.box(M['woodpale'], (0, -sy / 2 - 1.1, h - 0.08), (6.0, 0.12, 0.14))
    mb.pop()

def granary(mb, M, c):
    x, y, z = c
    for dx in (-0.7, 0.7):
        for dy in (-0.7, 0.7): mb.rod(M['wood'], (x + dx, y + dy, z), (x + dx, y + dy, z + 0.9), 0.09, 0.08, 6); mb.cone(M['stone'], (x + dx, y + dy, z + 0.6), 0.2, 0.2, 0.05, 8)
    mb.cone(M['thatchold'], (x, y, z + 0.9), 1.15, 1.0, 0.25, 20)
    mb.lathe(M['basket'], (x, y, z), [(1.0, 1.05), (1.1, 1.8), (1.0, 2.5)], 22)
    mb.cone(M['thatch'], (x, y, z + 2.4), 1.5, 0.05, 1.3, 24); mb.cone(M['thatchlow'], (x, y, z + 2.3), 1.55, 1.45, 0.15, 24)
    mb.box(M['dark'], (x, y - 1.05, z + 1.6), (0.4, 0.1, 0.45))
    for i in range(10):
        a = i / 10 * 6.283; mb.rod(M['woodpale'], (x + math.cos(a) * 1.02, y + math.sin(a) * 1.02, z + 1.0), (x + math.cos(a) * 1.08, y + math.sin(a) * 1.08, z + 2.4), 0.03, 0.03, 4)

def acacia(mb, M, c, s=1.0, seed=0, yaw=0.0, mat2='leafgreen'):
    rr = rnd(seed); x, y, z = c
    top = Vector((x, y, z + 5.2 * s)); lean = Vector((rr.uniform(-0.6, 0.6), rr.uniform(-0.6, 0.6), 0)) * s
    mid = Vector((x, y, z + 2.4 * s)) + lean * 0.4
    mb.rod(M['trunk'], (x, y, z - 0.1), mid, 0.34 * s, 0.24 * s, 8, smooth=True)
    for i in range(5): a = i * 1.26; mb.rod(M['trunk'], (x, y, z), (x + math.cos(a) * 0.5 * s, y + math.sin(a) * 0.5 * s, z - 0.05), 0.12 * s, 0.05 * s, 5)   # root flare
    tops = []
    for i in range(3):
        a = yaw + i * 2.1 + rr.uniform(-.3, .3); tp = top + Vector((math.cos(a) * 1.6 * s, math.sin(a) * 1.6 * s, rr.uniform(-.5, .3) * s)) + lean
        mb.rod(M['trunk'], mid, tp, 0.2 * s, 0.1 * s, 7, smooth=True); tops.append(tp)
    for tp in tops + [top + lean]:
        for j in range(4):
            o = Vector((rr.uniform(-1.8, 1.8), rr.uniform(-1.8, 1.8), rr.uniform(0.0, 0.35))) * s
            mb.ell(M[mat2], tp + o + Vector((0, 0, 0.35 * s)), (rr.uniform(1.4, 2.4) * s, rr.uniform(1.4, 2.4) * s, 0.4 * s), (14, 8), (0, 0, rr.random() * 6))

def bush(mb, M, c, s=1.0, seed=0, mt='acacia2'):
    rr = rnd(seed); x, y, z = c
    for i in range(5):
        mb.ell(M[mt], (x + rr.uniform(-.6, .6) * s, y + rr.uniform(-.6, .6) * s, z + rr.uniform(0.3, 0.9) * s), (rr.uniform(.5, .9) * s, rr.uniform(.5, .9) * s, rr.uniform(.4, .7) * s), (10, 7), (0, 0, rr.random() * 6))

def banana(mb, M, c, seed=0, s=1.0):
    rr = rnd(seed); x, y, z = c
    for k in range(rr.randint(3, 5)):
        px = x + rr.uniform(-0.7, 0.7); py = y + rr.uniform(-0.7, 0.7); hh = rr.uniform(2.0, 3.2) * s
        mb.rod(M['banana'], (px, py, z), (px, py, z + hh), 0.17 * s, 0.1 * s, 8, smooth=True)
        for i in range(8):
            a = rr.random() * 6.283; Lf = rr.uniform(1.7, 2.4) * s; wd = 0.36 * s; mt = M['banana'] if rr.random() > 0.15 else M['bananadry']
            dirv = Vector((math.cos(a), math.sin(a), 0)); side = Vector((-dirv.y, dirv.x, 0)); pts = []
            for t in range(6):
                u = t / 5.0; p = Vector((px, py, z + hh)) + dirv * (u * Lf) + Vector((0, 0, 0.55 * s * math.sin(u * 2.2) - 0.95 * s * u * u))
                pts.append((p, wd * math.sin(math.pi * min(1, u * 1.1 + 0.08))))
            for t in range(5):
                (p0, w0), (p1, w1) = pts[t], pts[t + 1]; mb.quad(mt, [p0 - side * w0, p0 + side * w0, p1 + side * w1, p1 - side * w1])
        mb.ell(M['stalk'], (px + 0.3, py, z + hh - 0.5), (0.1, 0.1, 0.22), (6, 4))
        if k == 0:
            for q in range(5): mb.ell(M['stalk'], (px + 0.3, py + 0.05 * q, z + hh - 0.7 - 0.06 * q), (0.06, 0.2, 0.05), (6, 4))

def papaya(mb, M, c, s=1.0, seed=0):
    rr = rnd(seed); x, y, z = c; h = 3.0 * s
    mb.rod(M['bark2'], (x, y, z), (x, y, z + h), 0.13 * s, 0.09 * s, 8, smooth=True)
    for i in range(8):
        a = i * 0.785 + rr.random() * 0.3; p0 = Vector((x, y, z + h)); p1 = p0 + Vector((math.cos(a) * 1.1 * s, math.sin(a) * 1.1 * s, 0.5 * s)); mb.rod(M['banana'], p0, p1, 0.03, 0.02, 4)
        mb.ell(M['banana'], p1 + Vector((math.cos(a) * 0.3 * s, math.sin(a) * 0.3 * s, 0.05)), (0.42 * s, 0.42 * s, 0.07 * s), (10, 5), (0, 0, a))
    for i in range(4): a = i * 1.6; mb.ell(M['pumpkin'], (x + math.cos(a) * 0.16, y + math.sin(a) * 0.16, z + h - 0.25), (0.1, 0.1, 0.17), (8, 6))

def jerrycan(mb, M, c, yaw=0.0):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M['jerry'], (0, 0, 0.26), (0.34, 0.18, 0.5)); mb.box(M['jerry'], (-0.06, 0, 0.56), (0.18, 0.12, 0.1)); mb.box(M['jcap'], (0.1, 0, 0.55), (0.07, 0.07, 0.07))
    mb.box(M['dark'], (-0.06, 0, 0.56), (0.08, 0.14, 0.04)); mb.box(M['jerry'], (0, 0.095, 0.3), (0.28, 0.02, 0.36))
    mb.pop()

def hoe(mb, M, c, yaw=0.0, lean=1.3):
    x, y, z = c
    ex, ey = x + math.cos(yaw) * 1.0, y + math.sin(yaw) * 1.0
    mb.rod(M['woodpale'], (x, y, z + 0.05), (ex, ey, z + lean), 0.025, 0.022, 6)
    mb.box(M['metal'], (ex, ey, z + lean), (0.22, 0.08, 0.15), rz=yaw + 0.3, ry=0.3)

def stool(mb, M, c, yaw=0.0):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M['woodpale'], (0, 0, 0.42), (0.42, 0.42, 0.07))
    for dx, dy in ((-0.15, -0.15), (0.15, -0.15), (-0.15, 0.15), (0.15, 0.15)): mb.rod(M['wood'], (dx, dy, 0.0), (dx * 1.1, dy * 1.1, 0.4), 0.035, 0.03, 6)
    mb.pop()

def bench(mb, M, c, yaw=0.0, L=1.6):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M['woodpale'], (0, 0, 0.42), (L, 0.34, 0.07))
    for dx in (-L / 2 + 0.15, L / 2 - 0.15):
        for dy in (-0.12, 0.12): mb.rod(M['wood'], (dx, dy, 0), (dx, dy, 0.4), 0.035, 0.03, 6)
    mb.pop()

def basket(mb, M, c, full=True, seed=4):
    x, y, z = c
    mb.lathe(M['basket'], (x, y, z), [(0.25, 0.0), (0.3, 0.2), (0.37, 0.42)], 14); mb.lathe(M['woodpale'], (x, y, z), [(0.37, 0.4), (0.39, 0.44)], 14)
    rr = rnd(seed)
    if full:
        for i in range(22):
            a = rr.random() * 6.283; r = rr.random() * 0.27
            mb.ell(M['cob'], (x + math.cos(a) * r, y + math.sin(a) * r, z + 0.5 + rr.random() * 0.12), (0.13, 0.05, 0.05), (8, 5), (0, rr.random() * 0.5, rr.random() * 6.28))
            if i % 3 == 0: mb.ell(M['husk'], (x + math.cos(a) * r, y + math.sin(a) * r, z + 0.5 + rr.random() * 0.12), (0.12, 0.06, 0.04), (8, 5), (0, rr.random() * 0.5, rr.random() * 6.28))

def pot_clay(mb, M, c, s=1.0):
    x, y, z = c
    mb.lathe(M['clay'], (x, y, z), [(0.0, 0.0), (0.16 * s, 0.01 * s), (0.27 * s, 0.14 * s), (0.31 * s, 0.3 * s), (0.22 * s, 0.46 * s), (0.17 * s, 0.52 * s), (0.2 * s, 0.56 * s)], 16)
    mb.lathe(M['claydark'], (x, y, z), [(0.19 * s, 0.55 * s), (0.0, 0.5 * s)], 16)

def metal_pot(mb, M, c, s=1.0):
    x, y, z = c
    mb.lathe(M['pot'], (x, y, z), [(0.0, 0.0), (0.2 * s, 0.0), (0.24 * s, 0.25 * s), (0.25 * s, 0.3 * s)], 16)
    mb.lathe(M['dark'], (x, y, z), [(0.24 * s, 0.29 * s), (0.0, 0.26 * s)], 16)
    mb.box(M['pot'], (x + 0.3 * s, y, z + 0.27 * s), (0.18 * s, 0.05 * s, 0.03 * s))

def bucket(mb, M, c, mt='jerry'):
    x, y, z = c
    mb.lathe(M[mt], (x, y, z), [(0.0, 0.0), (0.16, 0.0), (0.21, 0.3)], 14); mb.lathe(M['dark'], (x, y, z), [(0.2, 0.29), (0.0, 0.27)], 14)

def sack(mb, M, c, yaw=0.0, s=1.0, full=True):
    x, y, z = c
    mb.ell(M['sack'], (x, y, z + 0.28 * s), (0.28 * s, 0.2 * s, 0.3 * s), (12, 8), (0, 0, yaw)); mb.ell(M['sack'], (x, y, z + 0.55 * s), (0.17 * s, 0.14 * s, 0.1 * s), (8, 6), (0, 0, yaw))
    mb.rod(M['rope'], (x - 0.1 * s, y, z + 0.52 * s), (x + 0.1 * s, y, z + 0.52 * s), 0.02, 0.02, 4)

def wheelbarrow(mb, M, c, yaw=0.0, mt='bike'):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    for sx in (-1, 1): mb.quad(M[mt], [(-0.45, sx * 0.3, 0.45), (0.25, sx * 0.3, 0.45), (0.3, sx * 0.17, 0.25), (-0.4, sx * 0.17, 0.25)]) if False else None
    mb.box(M[mt], (-0.1, 0, 0.42), (0.7, 0.55, 0.05)); mb.box(M[mt], (-0.1, 0.27, 0.58), (0.7, 0.04, 0.3), rx=0.1); mb.box(M[mt], (-0.1, -0.27, 0.58), (0.7, 0.04, 0.3), rx=-0.1)
    mb.box(M[mt], (0.28, 0, 0.58), (0.04, 0.5, 0.28)); mb.box(M[mt], (-0.45, 0, 0.58), (0.04, 0.5, 0.28))
    for sy in (-0.18, 0.18): mb.rod(M['wood'], (-0.35, sy, 0.45), (-1.0, sy, 0.7), 0.03, 0.025, 6)
    for sy in (-0.18, 0.18): mb.rod(M['wood'], (-0.6, sy, 0.0), (-0.55, sy, 0.45), 0.02, 0.02, 5)
    mb.rod(M['rubber'], (0.45, -0.07, 0.2), (0.45, 0.07, 0.2), 0.2, 0.2, 14); mb.rod(M['metal'], (0.45, -0.1, 0.2), (0.45, 0.1, 0.2), 0.03, 0.03, 6)
    for sy in (-0.1, 0.1): mb.rod(M['metal'], (0.45, sy, 0.2), (0.15, sy * 1.5, 0.45), 0.015, 0.015, 4)
    mb.pop()

def firewood(mb, M, c, yaw=0.0, n=3, L=1.0):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4()); rr = rnd(int(x * 3 + y))
    for row in range(n):
        for i in range(n - row + 1):
            mb.rod(M['woodgrey'], (-L / 2, (i - (n - row) / 2) * 0.15, 0.07 + row * 0.13), (L / 2, (i - (n - row) / 2) * 0.15 + rr.uniform(-.02, .02), 0.07 + row * 0.13), 0.065, 0.06, 7)
    mb.pop()

def water_tank(mb, M, c):
    x, y, z = c
    for dx in (-0.5, 0.5):
        for dy in (-0.5, 0.5): mb.rod(M['wood'], (x + dx, y + dy, z), (x + dx, y + dy, z + 1.2), 0.07, 0.07, 6)
    mb.box(M['woodpale'], (x, y, z + 1.2), (1.3, 1.3, 0.1))
    mb.lathe(M['bluetank'], (x, y, z + 1.25), [(0.0, 0.0), (0.62, 0.0), (0.68, 0.2), (0.68, 1.1), (0.55, 1.35), (0.3, 1.45), (0.0, 1.45)], 22)
    mb.lathe(M['bluetank'], (x, y, z + 1.25), [(0.685, 0.5), (0.685, 0.55)], 22)
    mb.rod(M['metal'], (x + 0.55, y, z + 1.3), (x + 0.55, y, z + 0.85), 0.03, 0.03, 6); mb.rod(M['metal'], (x + 0.55, y, z + 0.85), (x + 0.75, y, z + 0.85), 0.03, 0.03, 6)

def washing_line(mb, M, c, yaw=0.0, L=4.0, seed=0):
    x, y, z = c; rr = rnd(seed + 3)
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    for sx in (-L / 2, L / 2): mb.rod(M['wood'], (sx, 0, 0), (sx, 0, 2.0), 0.05, 0.04, 6)
    mb.poly(M['rope'], [(-L / 2, 0, 1.95), (0, 0, 1.86), (L / 2, 0, 1.95)], 0.012, 0.012, 4)
    cols = ['cloth_red', 'cloth_blue', 'cloth_yel', 'cloth_wht', 'cloth_grn', 'cloth_org']
    nc = 5
    for i in range(nc):
        cx = -L / 2 + 0.5 + i * (L - 1.0) / (nc - 1); w = rr.uniform(0.45, 0.8); hh = rr.uniform(0.7, 1.15); zt = 1.88 - 0.09 * math.sin(math.pi * (cx + L / 2) / L) * 0
        mt = M[cols[(i + seed) % len(cols)]]
        mb.quad(mt, [(cx - w / 2, 0.02, zt), (cx + w / 2, 0.02, zt), (cx + w / 2 + 0.05, 0.05, zt - hh), (cx - w / 2, 0.03, zt - hh)]); mb.quad(mt, [(cx - w / 2, 0.02, zt), (cx - w / 2, 0.03, zt - hh), (cx + w / 2 + 0.05, 0.05, zt - hh), (cx + w / 2, 0.02, zt)])
    mb.pop()

def bicycle(mb, M, c, yaw=0.0):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    def wheel(cx):
        for i in range(18):
            a0 = i / 18 * 6.283; a1 = (i + 1) / 18 * 6.283
            mb.rod(M['rubber'], (cx + 0.34 * math.cos(a0), 0, 0.34 + 0.34 * math.sin(a0)), (cx + 0.34 * math.cos(a1), 0, 0.34 + 0.34 * math.sin(a1)), 0.022, 0.022, 5, caps=False)
        for i in range(6): a = i / 6 * 3.1416; mb.rod(M['metal'], (cx + 0.33 * math.cos(a), 0, 0.34 + 0.33 * math.sin(a)), (cx - 0.33 * math.cos(a), 0, 0.34 - 0.33 * math.sin(a)), 0.006, 0.006, 3)
    wheel(-0.55); wheel(0.55)
    for p0, p1 in [((-0.55, 0, 0.34), (-0.1, 0, 0.36)), ((-0.1, 0, 0.36), (0.38, 0, 0.7)), ((-0.55, 0, 0.34), (-0.18, 0, 0.7)), ((-0.18, 0, 0.7), (0.38, 0, 0.7)), ((-0.1, 0, 0.36), (-0.18, 0, 0.7)), ((0.38, 0, 0.7), (0.55, 0, 0.34))]:
        mb.rod(M['bike'], p0, p1, 0.02, 0.02, 6)
    mb.rod(M['metal'], (0.38, 0, 0.7), (0.34, 0, 0.88), 0.018, 0.018, 5); mb.rod(M['metal'], (0.34, -0.25, 0.9), (0.34, 0.25, 0.9), 0.015, 0.015, 5)
    mb.box(M['rubber'], (-0.2, 0, 0.76), (0.2, 0.08, 0.04))
    mb.pop()

def tripod_pot_fire(mb, M, c, lit=True):
    x, y, z = c
    for i in range(3):
        a = i * 2.094 + 0.3; mb.ell(M['stone'], (x + math.cos(a) * 0.3, y + math.sin(a) * 0.3, z + 0.12), (0.2, 0.15, 0.13), (8, 5), (0, 0, a))
    for i in range(5):
        a = i * 1.26; mb.rod(M['char'], (x + math.cos(a) * 0.4, y + math.sin(a) * 0.4, z + 0.12), (x, y, z + 0.14), 0.045, 0.04, 5)
    metal_pot(mb, M, (x, y, z + 0.28), 1.3)
    if lit: mb.cone(M['flame'], (x, y, z + 0.1), 0.2, 0.02, 0.5, 8); mb.cone(M['flame2'], (x, y, z + 0.1), 0.1, 0.01, 0.3, 8)

def chicken(mb, M, c, yaw=0.0, s=1.0, kind=0, peck=0.0):
    """hen / rooster, 0.42 m tall: body + breast + neck + head with comb and wattle, beak, eye, folded wing, tail fan, legs with toes."""
    body = [M['hen'], M['henwhite'], M['henblack'], M['hen']][kind % 4]; wing = [M['claydark'], M['hen'], M['henblack'], M['henblack']][kind % 4]; rooster = (kind % 4 == 3) or kind == 2
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Diagonal((s, s, s, 1)))
    mb.ell(body, (0, 0, 0.27), (0.21, 0.13, 0.14), (14, 9), (0, -0.15, 0)); mb.ell(body, (0.14, 0, 0.3), (0.11, 0.11, 0.12), (10, 7))          # body + breast
    nx = 0.2 + 0.07 * peck; nz = 0.48 - 0.2 * peck; hx = 0.25 + 0.15 * peck; hz = 0.52 - 0.34 * peck
    mb.poly(body, [(0.14, 0, 0.34), (nx, 0, nz)], 0.06, 0.04, 8)
    mb.ell(body, (hx, 0, hz), (0.065, 0.05, 0.06), (10, 7)); mb.tri(M['beak'], [(hx + 0.05, 0.02, hz + 0.0), (hx + 0.05, -0.02, hz + 0.0), (hx + 0.12, 0, hz - 0.015 - 0.03 * peck)])
    mb.tri(M['beak'], [(hx + 0.05, 0.02, hz - 0.01), (hx + 0.05, -0.02, hz - 0.01), (hx + 0.11, 0, hz - 0.035)])
    for sy in (-1, 1): mb.ell(M['eye'], (hx + 0.035, sy * 0.042, hz + 0.015), (0.01, 0.01, 0.012), (5, 4))
    for i, dz in enumerate((0.0, 0.035, 0.065)): mb.ell(M['comb'], (hx - 0.01 + 0.0 * i, 0, hz + 0.055 + dz * 0.4 - 0.01 * i * i), (0.018, 0.01, 0.03 + (0.01 if rooster else 0)), (6, 4))
    mb.ell(M['comb'], (hx + 0.04, 0, hz - 0.055), (0.012, 0.01, 0.028), (6, 4))                                                               # wattle
    for sy in (-1, 1): mb.ell(wing, (-0.02, sy * 0.105, 0.29), (0.13, 0.03, 0.09), (10, 6), (0, 0.15, sy * 0.1))                              # wings
    tm = M['henblack'] if rooster else body; n = 7 if rooster else 4
    for i in range(n):                                                                                                                       # tail feathers
        a = (i - (n - 1) / 2) * 0.22; L = 0.3 if rooster else 0.17; sd = a
        p0 = Vector((-0.18, 0, 0.31)); p1 = Vector((-0.18 - L * 0.7, sd * L * 0.55, 0.31 + L * (0.85 if rooster else 0.55))); p2 = Vector((-0.18 - L * 1.05, sd * L * 0.9, 0.31 + L * (0.72 if rooster else 0.5)))
        mb.quad(tm, [p0 + Vector((0, -0.02, 0)), p0 + Vector((0, 0.02, 0)), p1 + Vector((0, 0.02, 0)), p1 + Vector((0, -0.02, 0))]); mb.quad(tm, [p1 + Vector((0, -0.03, 0)), p1 + Vector((0, 0.03, 0)), p2, p2])
    for sy in (-0.045, 0.045):                                                                                                               # legs
        mb.rod(M['beak'], (0.0, sy, 0.17), (0.02, sy, 0.02), 0.012, 0.009, 5)
        for ty in (-0.035, 0.0, 0.035): mb.rod(M['beak'], (0.02, sy, 0.02), (0.075, sy + ty, 0.008), 0.007, 0.005, 4)
    mb.pop()

def goat(mb, M, c, yaw=0.0, s=1.0, coat=0):
    """goat, 0.85 m at the withers: barrel body with chest and rump, neck, head with snout, ears, horns, beard, 2-segment legs with hooves, patch markings."""
    base = [M['goat'], M['goatbrown'], M['goatblack']][coat % 3]; patch = [M['goatbrown'], M['goat'], M['goat']][coat % 3]
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Diagonal((s, s, s, 1)))
    sg = (16, 11)
    mb.ell(base, (0, 0, 0.64), (0.46, 0.2, 0.23), sg); mb.ell(base, (0.3, 0, 0.68), (0.25, 0.19, 0.24), sg); mb.ell(base, (-0.3, 0, 0.64), (0.26, 0.19, 0.22), sg)
    mb.poly(base, [(0.38, 0, 0.72), (0.52, 0, 0.9), (0.6, 0, 1.0)], 0.12, 0.075, 10)
    mb.ell(base, (0.7, 0, 1.0), (0.14, 0.085, 0.1), (12, 8), (0, 0.3, 0)); mb.ell(base, (0.8, 0, 0.96), (0.075, 0.065, 0.065), (10, 7))
    mb.ell(M['dark'], (0.86, 0, 0.97), (0.025, 0.04, 0.025), (6, 4))
    for sy in (-1, 1):
        mb.ell(base, (0.64, sy * 0.1, 1.03), (0.1, 0.035, 0.05), (8, 5), (0.0, 0.0, sy * 0.7)); mb.ell(M['eye'], (0.74, sy * 0.062, 1.04), (0.022, 0.016, 0.022), (6, 4))
        mb.poly(M['woodgrey'], [(0.66, sy * 0.045, 1.07), (0.62, sy * 0.06, 1.2), (0.52, sy * 0.07, 1.27), (0.44, sy * 0.07, 1.25)], 0.03, 0.01, 6)    # horns
    mb.cone(M['goat'], (0.8, 0, 0.84), 0.03, 0.008, 0.1, 6)                                                                                       # beard
    for lx, dr in ((0.36, 0.0), (-0.34, 0.0)):
        for sy in (-0.1, 0.1):
            mb.poly(base, [(lx, sy, 0.5), (lx + 0.02, sy, 0.27), (lx, sy, 0.05)], 0.055, 0.028, 7); mb.rod(M['dark'], (lx, sy, 0.05), (lx, sy, 0.0), 0.03, 0.026, 6)
    mb.rod(base, (-0.5, 0, 0.7), (-0.58, 0, 0.84), 0.03, 0.012, 5)
    for (px, py, pz, rx, ry, rz) in ((0.1, 0.17, 0.68, 0.17, 0.05, 0.13), (-0.2, -0.17, 0.7, 0.14, 0.05, 0.12), (0.36, -0.14, 0.78, 0.1, 0.05, 0.1)): mb.ell(patch, (px, py, pz), (rx, ry, rz), (8, 6))
    mb.pop()

def firepit(mb, M, c, lit=True):
    x, y, z = c
    for i in range(10):
        a = i / 10 * 6.283; mb.ell(M['stone'], (x + math.cos(a) * 0.6, y + math.sin(a) * 0.6, z + 0.1), (0.2, 0.16, 0.14), (8, 5), (0, 0, a))
    for i in range(5):
        a = i * 1.26 + 0.4; mb.rod(M['char'], (x + math.cos(a) * 0.5, y + math.sin(a) * 0.5, z + 0.18), (x, y, z + 0.3), 0.06, 0.05, 6)
    mb.ell(M['ember'], (x, y, z + 0.14), (0.3, 0.3, 0.06), (10, 5))
    if lit:
        mb.cone(M['flame'], (x, y, z + 0.15), 0.28, 0.02, 0.8, 8); mb.cone(M['flame2'], (x, y, z + 0.15), 0.15, 0.01, 0.5, 8)
        for sdx in (-0.18, 0.18): mb.cone(M['flame'], (x + sdx, y + 0.1, z + 0.15), 0.14, 0.01, 0.45, 6)

def torch(mb, M, c, h=1.3, lit=True, s=1.0):
    x, y, z = c
    mb.rod(M['torch'], (x, y, z), (x, y, z + h), 0.025 * s, 0.03 * s, 6); mb.ell(M['char'], (x, y, z + h + 0.03), (0.05 * s, 0.05 * s, 0.07 * s), (6, 4))
    if lit:
        mb.cone(M['flame'], (x, y, z + h), 0.09 * s, 0.01, 0.34 * s, 8); mb.cone(M['flame2'], (x, y, z + h), 0.05 * s, 0.005, 0.2 * s, 8)

def grass_clump(mb, M, c, rr, h=0.9, mt='grass', n=9):
    x, y, z = c
    for i in range(n):
        a = rr.random() * 6.283; L = h * rr.uniform(0.6, 1.2); bend = rr.uniform(0.15, 0.5)
        d = Vector((math.cos(a), math.sin(a), 0)); sd = Vector((-d.y, d.x, 0)) * 0.026
        p0 = Vector((x + rr.uniform(-.1, .1), y + rr.uniform(-.1, .1), z)); p1 = p0 + d * bend * 0.4 + Vector((0, 0, L * 0.6)); p2 = p0 + d * bend + Vector((0, 0, L))
        mb.quad(M[mt], [p0 - sd * 1.4, p0 + sd * 1.4, p1 + sd * 0.8, p1 - sd * 0.8]); mb.tri(M[mt], [p1 - sd * 0.8, p1 + sd * 0.8, p2])

def flower_tuft(mb, M, c, rr, n=4, mt=None):
    x, y, z = c; mt = mt or rr.choice(['flowerA', 'flowerB', 'flowerC', 'flowerA', 'flowerD'])
    for i in range(n):
        px = x + rr.uniform(-0.2, 0.2); py = y + rr.uniform(-0.2, 0.2); h = rr.uniform(0.2, 0.45)
        mb.rod(M['grassgreen'], (px, py, z), (px, py, z + h), 0.006, 0.005, 3, caps=False); mb.ell(M[mt], (px, py, z + h), (0.03, 0.03, 0.015), (6, 4))

def rock(mb, M, c, s=1.0, seed=0, mt='rock'):
    rr = rnd(seed); x, y, z = c
    mb.ell(M[mt], (x, y, z + 0.3 * s), (rr.uniform(.5, .8) * s, rr.uniform(.4, .7) * s, rr.uniform(.3, .5) * s), (9, 6), (rr.random() * .4, rr.random() * .4, rr.random() * 6))

def sunflower(mb, M, c, rr, h=None):
    x, y, z = c; h = h or rr.uniform(1.4, 2.1); a = rr.uniform(0, 6.28); lean = rr.uniform(0.05, 0.25)
    tp = Vector((x + math.cos(a) * lean, y + math.sin(a) * lean, z + h)); mb.rod(M['vine'], (x, y, z), tp, 0.022, 0.016, 5)
    d = Vector((math.cos(a + 1.57), math.sin(a + 1.57), 0.0)).normalized(); nrm = Vector((math.cos(a), math.sin(a), 0.5)).normalized()
    mb.ell(M['sfcenter'], tp, (0.1, 0.1, 0.035), (10, 5), (0.5, 0, a))
    for i in range(12):
        t = i / 12 * 6.283; ax = Vector((math.cos(t), math.sin(t), 0))
        mb.ell(M['sunflower'], tp + ax * 0.17 + Vector((0, 0, 0.0)), (0.09, 0.03, 0.01), (6, 4), (0, 0, t))
    for i in range(2): mb.ell(M['vine'], (x, y, z + h * 0.5 + i * 0.25), (0.15, 0.06, 0.02), (6, 4), (0, 0, a + i * 3))

def pumpkin_patch(mb, M, c, rr, n=4):
    x, y, z = c
    for i in range(n):
        px = x + rr.uniform(-0.9, 0.9); py = y + rr.uniform(-0.9, 0.9); s = rr.uniform(0.7, 1.2)
        mb.ell(M['pumpkin'], (px, py, z + 0.14 * s), (0.2 * s, 0.2 * s, 0.14 * s), (10, 7)); mb.rod(M['vine'], (px, py, z + 0.27 * s), (px + 0.03, py, z + 0.34 * s), 0.02, 0.015, 4)
        a = rr.random() * 6.28; mb.poly(M['vine'], [(px, py, z + 0.05), (px + math.cos(a) * 0.4, py + math.sin(a) * 0.4, z + 0.04), (px + math.cos(a + .5) * 0.8, py + math.sin(a + .5) * 0.8, z + 0.04)], 0.01, 0.006, 4)
        mb.ell(M['vine'], (px + math.cos(a) * 0.3, py + math.sin(a) * 0.3, z + 0.1), (0.14, 0.12, 0.01), (6, 4), (0, 0, a))

def kale_row(mb, M, p0, p1, rr, step=0.55):
    d = Vector(p1) - Vector(p0); L = d.length; n = int(L / step); d.normalize()
    for i in range(n + 1):
        p = Vector(p0) + d * (i * step); h = rr.uniform(0.35, 0.6)
        mb.rod(M['stalk'], p, p + Vector((0, 0, h)), 0.02, 0.014, 4)
        for k in range(7):
            a = k * 0.9 + rr.random(); q = p + Vector((0, 0, 0.12 + 0.05 * k)); e = q + Vector((math.cos(a) * 0.28, math.sin(a) * 0.28, 0.06 - 0.05 * k * 0.6)); sd = Vector((-math.sin(a), math.cos(a), 0)) * 0.09
            mb.quad(M['kale'], [q, e - sd, e + sd * 0.0 + Vector((math.cos(a), math.sin(a), 0)) * 0.08, e + sd])

def thorn_pile(mb, M, c, yaw, L=3.0, h=1.1, seed=0):
    """a heap of thorn branches (dark twigs, little leaf puffs) running along yaw, 3 m long."""
    rr = rnd(seed); x, y, z = c; d = Vector((math.cos(yaw), math.sin(yaw), 0)); nrm = Vector((-d.y, d.x, 0))
    for i in range(34):
        u = rr.uniform(-0.5, 0.5) * L; base = Vector((x, y, z)) + d * u + nrm * rr.uniform(-0.25, 0.25); tip = base + d * rr.uniform(-0.6, 0.6) + nrm * rr.uniform(-0.3, 0.3) + Vector((0, 0, rr.uniform(0.3, h)))
        mb.rod(M['thorn'], base, tip, 0.022, 0.008, 4)
        for k in range(3):
            q = base.lerp(tip, rr.uniform(0.4, 1.0)); q2 = q + Vector((rr.uniform(-.2, .2), rr.uniform(-.2, .2), rr.uniform(0.0, 0.2))); mb.rod(M['thorn'], q, q2, 0.01, 0.004, 3, caps=False)
            if rr.random() < 0.5: mb.ell(M['thornleaf'], q2, (0.07, 0.05, 0.03), (5, 3))
    for k in (-0.5, 0.0, 0.5): mb.rod(M['wood'], Vector((x, y, z)) + d * (k * L), Vector((x, y, z + 1.0)) + d * (k * L), 0.04, 0.035, 5)

def tin_can_line(mb, M, p0, p1, n=5, seed=0):
    rr = rnd(seed); p0 = Vector(p0); p1 = Vector(p1)
    mb.rod(M['rope'], p0, p1, 0.008, 0.008, 3, caps=False)
    for i in range(n):
        u = (i + 0.5) / n + rr.uniform(-0.04, 0.04); p = p0.lerp(p1, u); L = rr.uniform(0.25, 0.5)
        mb.rod(M['rope'], p, p - Vector((0, 0, L)), 0.006, 0.006, 3, caps=False); mb.lathe(M['tincan'], p - Vector((0, 0, L + 0.12)), [(0.0, 0.0), (0.045, 0.0), (0.05, 0.02), (0.05, 0.11), (0.0, 0.11)], 10)

def termite_mound(mb, M, c, s=1.0):
    x, y, z = c
    mb.lathe(M['mudpale'], (x, y, z), [(0.9 * s, -0.05), (0.7 * s, 0.4 * s), (0.45 * s, 1.0 * s), (0.3 * s, 1.5 * s), (0.1 * s, 1.9 * s), (0.0, 1.95 * s)], 14)

def giraffe(mb, M, c, yaw=0.0, s=1.0):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Diagonal((s, s, s, 1))); g = M['giraffe']
    mb.ell(g, (0, 0, 2.3), (0.9, 0.38, 0.55), (10, 8)); mb.poly(g, [(0.7, 0, 2.6), (1.1, 0, 3.8), (1.35, 0, 4.9)], 0.22, 0.12, 8)
    mb.ell(g, (1.55, 0, 5.0), (0.3, 0.14, 0.17), (8, 6), (0, 0.3, 0))
    for lx in (-0.55, 0.6):
        for sy in (-0.22, 0.22): mb.poly(g, [(lx, sy, 2.0), (lx, sy, 1.0), (lx, sy, 0.0)], 0.12, 0.07, 6)
    mb.pop()

def bird(mb, M, c, yaw, flap, s=0.5, mt='bird'):
    x, y, z = c; d = Vector((math.cos(yaw), math.sin(yaw), 0)); sd = Vector((-d.y, d.x, 0)); p = Vector((x, y, z))
    mb.quad(M[mt], [p + d * 0.3 * s, p - d * 0.3 * s, p - d * 0.1 * s + sd * 1.1 * s + Vector((0, 0, flap * s)), p + d * 0.2 * s + sd * 1.0 * s + Vector((0, 0, flap * s))])
    mb.quad(M[mt], [p - d * 0.3 * s, p + d * 0.3 * s, p + d * 0.2 * s - sd * 1.0 * s + Vector((0, 0, flap * s)), p - d * 0.1 * s - sd * 1.1 * s + Vector((0, 0, flap * s))])
    mb.ell(M[mt], p, (0.28 * s, 0.1 * s, 0.1 * s), (6, 4), (0, 0, yaw))

def cloud_puff(mb, M, c, s, seed):
    rr = rnd(seed); x, y, z = c
    for i in range(int(9 + 5 * rr.random())):
        a = rr.uniform(-1, 1); mb.ell(M['cloud'], (x + a * s * 1.6, y + rr.uniform(-.3, .3) * s, z + (1 - abs(a)) * s * rr.uniform(0.2, 0.7)), (s * rr.uniform(.45, .8), s * rr.uniform(.4, .6), s * rr.uniform(.32, .5)), (14, 9))
    mb.box(M['cloud'], (x, y, z - s * 0.1), (s * 3.4, s * 1.0, s * 0.01)) if False else None

def maize_variant(M, seed, mats=('maize', 'cob', 'stalk', 'tassel', 'husk')):
    rr = rnd(seed); mb = MB('mz%d' % seed); hgt = R(2.1, 2.55, rr); lm = M[mats[0]]
    mb.rod(M['stalk'], (0, 0, 0), (0, 0, hgt), 0.035, 0.02, 6)
    for i in range(3): a = i * 2.1; mb.rod(M['stalk'], (0, 0, 0.0), (math.cos(a) * 0.12, math.sin(a) * 0.12, -0.03), 0.02, 0.01, 4)     # brace roots
    nl = 10
    for i in range(nl):
        zb = 0.3 + (hgt - 0.65) * i / (nl - 1); a = i * 2.4 + rr.random() * 0.8; Lf = R(0.95, 1.3, rr) * (1.0 - 0.25 * i / nl); wd = 0.09
        d = Vector((math.cos(a), math.sin(a), 0)); sd = Vector((-d.y, d.x, 0)); pts = []
        for t in range(7):
            u = t / 6.0; p = Vector((0, 0, zb)) + d * (u * Lf * 0.85) + Vector((0, 0, 0.45 * math.sin(u * 2.0) - 0.7 * u * u * Lf * 0.7))
            wv = wd * (0.5 + math.sin(math.pi * min(1, u * 0.95 + 0.05))); pts.append((p, wv, sd * wv * 0.35 * (1 if t % 2 else -1) * 0))
        for t in range(6):
            (p0, w0, _), (p1, w1, _) = pts[t], pts[t + 1]; mb.quad(lm, [p0 - sd * w0, p0 + sd * w0, p1 + sd * w1, p1 - sd * w1])
    for k in range(2):                                                                                     # cobs wrapped in husk, silk tuft
        a = k * 3.1 + rr.random(); cx, cy = math.cos(a) * 0.1, math.sin(a) * 0.1; zc = 1.2 + 0.22 * k
        mb.ell(M[mats[4]], (cx, cy, zc), (0.05, 0.05, 0.19), (7, 5)); mb.ell(M[mats[1]], (cx, cy, zc + 0.14), (0.035, 0.035, 0.06), (6, 4)); mb.rod(M['tassel'], (cx, cy, zc + 0.19), (cx + 0.02, cy, zc + 0.3), 0.01, 0.004, 3)
    for i in range(7):
        a = i * 0.9; mb.rod(M[mats[3]], (0, 0, hgt - 0.05), (math.cos(a) * 0.24, math.sin(a) * 0.24, hgt + 0.32), 0.012, 0.004, 4)
    return mb.finish(join=True)

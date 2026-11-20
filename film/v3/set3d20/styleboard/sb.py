"""set3d20 style board: Eiffel Tower 1887-1909 (SITE under construction / TOWER finished at dusk with radio hut / RESTO first-floor restaurant).
Self-contained bpy scene (procedural geometry + shaders), Cycles CPU.  usage: python3 sb.py site|dusk|resto|all [draft]
-> sb1_site.jpg / sb2_tower_dusk.jpg / sb3_resto.jpg (+ *_shade.png masks for hue_check.py; d_*.jpg for draft)
World units: metres. +x right, +y away from camera, z up. Camera 22 mm / 36 mm sensor (AUTO fit => 36 mm on the long side), 720x1280, no DOF.
Reusable for the set builder: `tower(...)` (lattice Eiffel Tower, any height/stage/scale), `haus(...)`, `city_ring(...)`, `mat(...)`, `MB`.
Look: one hard key (sun) with real cast shadows, blue-violet sky ambient, painterly two-tone noise materials. No text anywhere."""
import os, sys, math, random, time
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix, Euler
from PIL import Image, ImageFilter

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
    def quad(self, m, v):
        bm = self._b(m); vs = [bm.verts.new(self.T @ Vector(p)) for p in v]
        try: bm.faces.new(vs)
        except ValueError: pass
    def finish(self, shadow=True):
        objs = []
        for m, bm in self.bm.items():
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
            me = bpy.data.meshes.new('%s_%s' % (self.name, m.name)); bm.to_mesh(me); bm.free()
            ob = bpy.data.objects.new('%s_%s' % (self.name, m.name), me); ob.data.materials.append(m)
            bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = shadow; objs.append(ob)
        self.bm = {}; return objs

def rnd(s): return random.Random(s)

# ------------------------------------------------------------------ palette (period colours, painterly pairs)
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

# ------------------------------------------------------------------ the tower (reusable)
_zz = [0, 57, 115, 190, 276, 300]; _ww = [56, 32, 18, 8, 2.5, 1.0]
_wfit = np.polyfit(_zz, np.log(_ww), 3)
def tw(z): return float(max(0.9, math.exp(np.polyval(_wfit, min(z, 300)))))          # half distance between leg centre-lines at height z (m)
def th(z): return 6.5 * math.exp(-z / 90.0) + 0.8                                      # half section of one leg (m)
Z1, Z2, Z3 = 57.0, 115.0, 276.0

def _zs(z0, z1, k=0.03, d0=3.6):
    zs = [z0]
    while zs[-1] < z1 - 0.01: zs.append(min(z1, zs[-1] + d0 + zs[-1] * k))
    return zs

def lattice_face(mb, m, pa, pb, zs, rd, rh, seg=4):
    """two vertical edges pa(z), pb(z) (callables -> Vector) with X-bracing + belts at each z in zs"""
    for i in range(len(zs) - 1):
        a0, a1, b0, b1 = pa(zs[i]), pa(zs[i + 1]), pb(zs[i]), pb(zs[i + 1])
        mb.rod(m, a0, b1, rd, rd, seg); mb.rod(m, b0, a1, rd, rd, seg)
    for z in zs: mb.rod(m, pa(z), pb(z), rh, rh, seg)

def tower(mb, M, zmax=300.0, stage='full', thick=1.0, mat_main=None, mat_light=None, lamps=True, gal=None):
    """Eiffel lattice. stage 'legs': 4 legs up to Z1 + girder ring (site). 'full': everything up to zmax (platforms, galleries, lantern, spire).
    Built in tower-local metres (base 125 m square, platforms 57/115/276). thick scales member radii (use ~1.5-2 for far views)."""
    I = mat_main or M['iron']; IL = mat_light or M['ironlt']
    k = thick; zs_leg = _zs(0, Z1) if stage == 'legs' else _zs(0, min(zmax, 300))
    legs = [(sx, sy) for sx in (-1, 1) for sy in (-1, 1)]
    def post(sx, sy, ox, oy): return lambda z: Vector((sx * tw(z) + ox * th(z), sy * tw(z) + oy * th(z), z))
    top = Z1 + 40.0 if stage == 'legs' else zmax
    zs_all = _zs(0, top)
    for (sx, sy) in legs:
        P = {(ox, oy): post(sx, sy, ox, oy) for ox in (-1, 1) for oy in (-1, 1)}
        for key, f in P.items():
            for z0, z1 in zip(zs_all[:-1], zs_all[1:]): mb.rod(I, f(z0), f(z1), 0.52 * k * (1.15 - z0 / 600.0), 0.5 * k * (1.15 - z1 / 600.0), 4)
        for a, b in (((-1, -1), (1, -1)), ((1, -1), (1, 1)), ((1, 1), (-1, 1)), ((-1, 1), (-1, -1))): lattice_face(mb, IL, P[a], P[b], zs_all, 0.22 * k, 0.26 * k)
        # stone pier
        mb.box(M['stone'], (sx * tw(0), sy * tw(0), 1.4), (2 * th(0) + 5.0, 2 * th(0) + 5.0, 5.2)); mb.box(M['stonedk'], (sx * tw(0), sy * tw(0), 4.2), (2 * th(0) + 3.2, 2 * th(0) + 3.2, 0.7))
    # inter-leg lattice between adjacent legs above the arches (outer face + inner face)
    z_in = Z1 if stage == 'full' else None
    if stage == 'full':
        zs_u = _zs(Z1, top, 0.02, 3.2)
        # simpler explicit faces
        for sgn in (-1, 1):
            for off in (-1, 1):
                fa = (lambda z, s=sgn, o=off: Vector((-(tw(z) - th(z)), s * (tw(z) + o * th(z)), z))); fb = (lambda z, s=sgn, o=off: Vector(((tw(z) - th(z)), s * (tw(z) + o * th(z)), z)))
                ga = (lambda z, s=sgn, o=off: Vector((s * (tw(z) + o * th(z)), -(tw(z) - th(z)), z))); gb = (lambda z, s=sgn, o=off: Vector((s * (tw(z) + o * th(z)), (tw(z) - th(z)), z)))
                if off == 1 or True:
                    lattice_face(mb, IL, fa, fb, zs_u, 0.2 * k, 0.24 * k); lattice_face(mb, IL, ga, gb, zs_u, 0.2 * k, 0.24 * k)
    if True:
        # arches under the first platform (one per face)
        zs0, za = 6.0, 46.0
        for face in range(4):
            ang = face * math.pi / 2; R_ = Matrix.Rotation(ang, 4, 'Z'); mb.push(R_)
            for (zz_a, rr_, mm_) in ((za, 0.9 * k, I), (za - 4.5, 0.7 * k, I)):
                prev = None
                for i in range(25):
                    u = -1 + 2 * i / 24.0; z = zs0 + (zz_a - zs0) * math.sqrt(max(0.0, 1 - u * u)); xi = (tw(z) - th(z)) * u * 0.985
                    p = Vector((xi, -(tw(z) + th(z)), z))
                    if prev is not None: mb.rod(mm_, prev, p, rr_, rr_, 4)
                    prev = p
            for i in range(0, 25, 2):                       # ladder rungs / spandrel verticals
                u = -1 + 2 * i / 24.0; z = zs0 + (za - zs0) * math.sqrt(max(0.0, 1 - u * u)); xi = (tw(z) - th(z)) * u * 0.985
                zb = zs0 + (za - 4.5 - zs0) * math.sqrt(max(0.0, 1 - u * u)); yy = -(tw(z) + th(z))
                mb.rod(IL, (xi, yy, zb), (xi, yy, z), 0.2 * k, 0.2 * k, 4)
                if abs(u) < 0.95: mb.rod(IL, (xi, yy, z), (xi, yy, Z1 - 7.0), 0.22 * k, 0.22 * k, 4)
            mb.pop()
    # girder ring at the first platform (legs stage: open ring of lattice girders; full: deck + gallery)
    a1 = tw(Z1) + th(Z1)
    def ring(zb, zt, a, mmat, rd):
        for face in range(4):
            mb.push(Matrix.Rotation(face * math.pi / 2, 4, 'Z'))
            zs = [zb, zt]; ns = 8
            for i in range(ns):
                x0 = -a + 2 * a * i / ns; x1 = -a + 2 * a * (i + 1) / ns
                mb.rod(mmat, (x0, -a, zb), (x1, -a, zt), rd, rd, 4); mb.rod(mmat, (x0, -a, zt), (x1, -a, zb), rd, rd, 4)
                mb.rod(mmat, (x0, -a, zt), (x1, -a, zt), rd * 1.4, rd * 1.4, 4); mb.rod(mmat, (x0, -a, zb), (x1, -a, zb), rd * 1.4, rd * 1.4, 4)
            mb.pop()
    ring(Z1 - 7.0, Z1, a1 + 0.3, IL, 0.3 * k)
    for face in range(4):
        mb.push(Matrix.Rotation(face * math.pi / 2, 4, 'Z')); mb.box(I, (0, -(a1 + 0.3), Z1 + 0.3), (2 * a1 + 1.0, 0.9, 0.6)); mb.box(I, (0, -(a1 + 0.3), Z1 - 7.0), (2 * a1 + 1.0, 0.9, 0.5)); mb.pop()
    if stage == 'legs':
        return
    # ---- full tower: decks, galleries, second / third platform, lantern, spire
    ah = a1 + 2.0
    mb.box(I, (0, 0, Z1 - 0.2), (2 * ah, 2 * ah, 1.4)); mb.box(M['ironlt'], (0, 0, Z1 + 0.6), (2 * ah + 0.8, 2 * ah + 0.8, 0.5))
    if gal is None: gal = M['galwall']
    ag = ah - 1.6; gt = 3.4                                              # gallery ring (restaurants), cream facades with window grid
    for (cx, cy, sx_, sy_) in ((0, -(ag - gt / 2), 2 * ag, gt), (0, (ag - gt / 2), 2 * ag, gt), (-(ag - gt / 2), 0, gt, 2 * ag - 2 * gt), ((ag - gt / 2), 0, gt, 2 * ag - 2 * gt)):
        mb.box(gal, (cx, cy, Z1 + 3.6), (sx_, sy_, 6.2))
    mb.box(I, (0, 0, Z1 + 7.0), (2 * ag + 1.6, 2 * ag + 1.6, 0.7))       # gallery roof
    for i in range(20):                                                   # arcade of lamps on the gallery roof edge
        t = i / 20.0 * 4; e = int(t); f = (t - e)
        pts = [(-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)]; p = (pts[e][0] * (1 - f) + pts[e + 1][0] * f, pts[e][1] * (1 - f) + pts[e + 1][1] * f)
        if lamps: mb.ell(M['lampsm'], (p[0] * (ag + 0.7), p[1] * (ag + 0.7), Z1 + 8.0), (0.7 * k, 0.7 * k, 0.7 * k), (8, 6))
    # second platform
    a2 = tw(Z2) + th(Z2) + 1.2
    ring(Z2 - 3.6, Z2, a2 - 1.2, IL, 0.26 * k)
    mb.box(I, (0, 0, Z2 - 0.2), (2 * a2, 2 * a2, 1.2)); mb.box(gal, (0, 0, Z2 + 2.2), (2 * a2 - 4, 2 * a2 - 4, 4.2)); mb.box(I, (0, 0, Z2 + 4.5), (2 * a2 - 2.6, 2 * a2 - 2.6, 0.6))
    for z in (Z2 + 0.9,):
        for i in range(16):
            t = i / 16.0 * 4; e = int(t); f = t - e; pts = [(-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)]; p = (pts[e][0] * (1 - f) + pts[e + 1][0] * f, pts[e][1] * (1 - f) + pts[e + 1][1] * f)
            if lamps: mb.ell(M['lampsm'], (p[0] * (a2 - 0.3), p[1] * (a2 - 0.3), z + 0.4), (0.55 * k, 0.55 * k, 0.55 * k), (8, 6))
    # belts of the upper lattice every ~55 m
    for z in (165.0, 220.0): mb.box(I, (0, 0, z), (2 * (tw(z) + th(z)) + 0.8, 2 * (tw(z) + th(z)) + 0.8, 0.9))
    # third platform + lantern + spire
    a3 = tw(Z3) + th(Z3) + 1.2
    mb.box(I, (0, 0, Z3), (2 * a3 + 1.5, 2 * a3 + 1.5, 1.0)); mb.box(gal, (0, 0, Z3 + 3.2), (2 * a3, 2 * a3, 5.4)); mb.box(I, (0, 0, Z3 + 6.3), (2 * a3 + 1.0, 2 * a3 + 1.0, 0.8))
    mb.rod(I, (0, 0, Z3 + 6.6), (0, 0, 300.0), 0.9 * k * 0.8, 0.12 * k, 6)
    mb.cyl(I, (0, 0, Z3 + 8.5), 1.2 * k, 1.6, 'z', 8)
    mb.ell(M['lampsm'], (0, 0, Z3 + 9.5), (1.4 * k, 1.4 * k, 1.4 * k), (10, 8))                   # beacon
    for (sx, sy) in legs:
        for z in (Z1, Z2): mb.ell(M['lampsm'], (sx * (tw(z) + th(z)) * 1.02, sy * (tw(z) + th(z)) * 1.02, z + 3.0), (1.0 * k, 1.0 * k, 1.0 * k), (8, 6))

# ------------------------------------------------------------------ props
def girder_pile(mb, M, c, yaw, L=6.0, nx=6, nz=5, rr=None):
    """stack of I-beams (red-lead) separated by timber dunnage, local x = beam axis"""
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4()); rr = rr or rnd(1)
    for k in range(nz):
        z = 0.38 + k * 0.34
        for i in range(nx - (k // 2)):
            y = (i - (nx - (k // 2) - 1) / 2.0) * 0.36 + rr.uniform(-0.02, 0.02); l = L * rr.uniform(0.9, 1.0); x0 = rr.uniform(-0.2, 0.2)
            mb.box(M['redlead'], (x0, y, z), (l, 0.22, 0.03)); mb.box(M['redlead'], (x0, y, z + 0.14), (l, 0.04, 0.26)); mb.box(M['redlead'], (x0, y, z + 0.27), (l, 0.22, 0.03))
        if k < nz - 1:
            for xx in (-L * 0.36, 0, L * 0.36): mb.box(M['timberdk'], (xx, 0, z + 0.28), (0.14, nx * 0.4, 0.07))
    for xx in (-L * 0.36, 0, L * 0.36): mb.box(M['timberdk'], (xx, 0, 0.08), (0.2, nx * 0.4, 0.16))
    mb.pop()

def barrel(mb, M, c, h=0.9, r=0.36, mt='timber'):
    x, y, z = c
    mb.cyl(M[mt], (x, y, z + h / 2), r, h, 'z', 14, True); mb.cyl(M[mt], (x, y, z + h / 2), r * 1.13, h * 0.5, 'z', 14, True)
    for k in (0.12, 0.88): mb.cyl(M['metal'], (x, y, z + h * k), r * 1.0, 0.05, 'z', 14)
    mb.cyl(M['metal'], (x, y, z + h * 0.5), r * 1.14, 0.05, 'z', 14)

def crate(mb, M, c, s=(0.8, 0.6, 0.55), yaw=0.0, m='plank'): mb.box(M[m], (c[0], c[1], c[2] + s[2] / 2), s, rz=yaw)

def forge(mb, M, c, yaw=0.0, lights=None, sc=1.0):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Scale(sc, 4))
    mb.box(M['brick'], (0, 0, 0.5), (1.4, 1.0, 1.0)); mb.box(M['stonedk'], (0, 0, 1.03), (1.5, 1.1, 0.08))
    mb.box(M['soot'], (0, 0, 1.1), (1.1, 0.8, 0.08)); mb.box(M['coal'], (0, 0, 1.14), (1.0, 0.7, 0.05))
    pass
    mb.rod(M['soot'], (0, 0.3, 1.6), (0, 0.5, 2.6), 0.75, 0.16, 12); mb.rod(M['soot'], (0, 0.5, 2.6), (0, 0.5, 3.6), 0.16, 0.14, 8)
    for sx_ in (-1, 1): mb.rod(M['soot'], (sx_ * 0.55, -0.3, 1.0), (sx_ * 0.55, 0.3, 1.6), 0.05, 0.05, 5)
    mb.rod(M['dark'], (-0.3, -0.5, 1.25), (0.3, -0.4, 1.15), 0.02, 0.02, 4); mb.ell(M['rivet'], (0.35, -0.4, 1.13), (0.05, 0.05, 0.05), (6, 4))
    pass
    mb.box(M['plank'], (1.0, 0.0, 0.55), (0.7, 0.45, 0.35), rz=0.2); mb.rod(M['dark'], (1.3, 0.0, 0.65), (1.9, 0.0, 0.5), 0.1, 0.03, 6)      # bellows
    mb.box(M['dark'], (-1.2, 0.1, 0.55), (0.5, 0.3, 0.14)); mb.box(M['dark'], (-1.2, 0.1, 0.35), (0.22, 0.16, 0.5)); mb.box(M['dark'], (-1.45, 0.1, 0.66), (0.3, 0.12, 0.1))    # anvil
    for i in range(5): mb.ell(M['rivet'], (-0.5 + i * 0.12, -0.75, 0.97), (0.05, 0.05, 0.05), (6, 4))
    mb.box(M['timberdk'], (-0.3, -0.75, 0.45), (0.9, 0.34, 0.9)); mb.cyl(M['metal'], (0.9, -0.7, 0.2), 0.2, 0.4, 'z', 10)
    mb.pop()
    if lights is not None: lights.append((Vector(c) + Vector((0, -0.6, 1.5)), (1.0, 0.45, 0.16), 500))

def wheel(mb, M, c, r, thick=0.05, spokes=10, axis_y=True):
    x, y, z = c
    mb.cyl(M['timberdk'], (x, y, z), r * 0.12, thick * 3, 'y', 10)
    for i in range(spokes):
        a = i * math.pi * 2 / spokes; mb.rod(M['timber'], (x, y, z), (x + math.cos(a) * r * 0.94, y, z + math.sin(a) * r * 0.94), thick * 0.45, thick * 0.35, 5)
    for i in range(18):
        a = i * math.pi * 2 / 18; b = (i + 1) * math.pi * 2 / 18
        mb.rod(M['metal'], (x + math.cos(a) * r, y, z + math.sin(a) * r), (x + math.cos(b) * r, y, z + math.sin(b) * r), thick * 0.9, thick * 0.9, 5)

def horse(mb, M, c, yaw=0.0):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4()); h = M['horse']
    mb.ell(h, (0, 0, 1.25), (1.0, 0.34, 0.42), (14, 10)); mb.ell(h, (0.85, 0, 1.38), (0.45, 0.3, 0.38), (12, 8)); mb.ell(h, (-0.85, 0, 1.3), (0.4, 0.32, 0.4), (12, 8))
    mb.rod(h, (0.95, 0, 1.4), (1.4, 0, 2.0), 0.3, 0.2, 10, smooth=True); mb.ell(h, (1.58, 0, 2.02), (0.34, 0.17, 0.2), (10, 8), (0, -0.55, 0)); mb.rod(M['horsedk'], (1.3, 0, 2.15), (1.15, 0, 1.6), 0.05, 0.03, 5); mb.rod(M['horsedk'], (1.22, 0, 1.78), (1.0, 0, 1.55), 0.05, 0.03, 5)
    for (lx, ly) in ((0.7, 0.18), (0.7, -0.18), (-0.75, 0.18), (-0.75, -0.18)):
        mb.rod(h, (lx, ly, 1.0), (lx, ly, 0.1), 0.13, 0.07, 6); mb.box(M['horsedk'], (lx, ly, 0.05), (0.14, 0.12, 0.1))
    mb.rod(M['horsedk'], (-1.2, 0, 1.4), (-1.35, 0, 0.7), 0.06, 0.04, 5)
    mb.ell(M['horsedk'], (0.55, 0.0, 1.55), (0.1, 0.06, 0.1), (6, 4)); mb.box(M['crimson'], (0.45, 0, 1.55), (0.5, 0.5, 0.08))
    mb.pop()

def cart(mb, M, c, yaw=0.0, load='barrels', lights=None):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M['timber'], (0, 0, 1.0), (3.4, 1.5, 0.12)); 
    for s_ in (-1, 1): mb.box(M['timber'], (0, s_ * 0.74, 1.3), (3.4, 0.08, 0.5))
    mb.box(M['timber'], (-1.7, 0, 1.3), (0.08, 1.5, 0.5))
    mb.rod(M['timberdk'], (1.7, 0.5, 1.0), (4.2, 0.5, 0.95), 0.05, 0.04, 6); mb.rod(M['timberdk'], (1.7, -0.5, 1.0), (4.2, -0.5, 0.95), 0.05, 0.04, 6)
    wheel(mb, M, (0.2, 0.9, 0.7), 0.7); wheel(mb, M, (0.2, -0.9, 0.7), 0.7); mb.rod(M['timberdk'], (0.2, 0.9, 0.7), (0.2, -0.9, 0.7), 0.05, 0.05, 6)
    if load == 'barrels':
        for (x, y) in ((-1.0, 0.35), (-1.0, -0.35), (-0.2, 0.35), (-0.2, -0.35), (0.6, 0.0)): barrel(mb, M, (x, y, 1.06), 0.9, 0.3)
    else:
        for k in range(3): mb.box(M['redlead'], (0, (k - 1) * 0.3, 1.2), (3.2, 0.2, 0.06)); mb.box(M['redlead'], (0, (k - 1) * 0.3, 1.33), (3.2, 0.04, 0.26))
    mb.pop(); horse(mb, M, Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Vector((5.0, 0, 0)) if False else (c[0] + math.cos(yaw) * 5.2, c[1] + math.sin(yaw) * 5.2, c[2]), yaw)

def shed(mb, M, c, w=5.0, d=3.6, h=2.6, yaw=0.0, door=True, mw='plank'):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M[mw], (0, 0, h / 2), (w, d, h))
    for i in range(int(w / 0.6)): mb.box(M['timberdk'], (-w / 2 + 0.3 + i * 0.6, -d / 2 - 0.02, h / 2), (0.07, 0.03, h))            # battens
    hh = h + 0.9
    mb.quad(M['tarroof'], [(-w / 2 - 0.4, -d / 2 - 0.4, h), (w / 2 + 0.4, -d / 2 - 0.4, h), (w / 2 + 0.4, 0, hh), (-w / 2 - 0.4, 0, hh)][::-1])
    mb.quad(M['tarroof'], [(-w / 2 - 0.4, 0, hh), (w / 2 + 0.4, 0, hh), (w / 2 + 0.4, d / 2 + 0.4, h), (-w / 2 - 0.4, d / 2 + 0.4, h)][::-1])
    mb.box(M['tarroof'], (0, 0, h + 0.05), (w + 0.4, d + 0.4, 0.08))
    for sgn in (-1, 1):
        mb.quad(M['plank'], [(sgn * w / 2, -d / 2, h), (sgn * w / 2, 0, hh), (sgn * w / 2, d / 2, h)])
    if door: mb.box(M['dark'], (-w * 0.25, -d / 2 - 0.03, 1.0), (0.9, 0.05, 2.0)); mb.box(M['timberdk'], (w * 0.22, -d / 2 - 0.03, 1.5), (1.0, 0.05, 0.8))
    mb.rod(M['metal'], (w * 0.3, d * 0.2, h + 0.3), (w * 0.3, d * 0.2, h + 1.5), 0.14, 0.14, 8)
    mb.pop()

def scaffold(mb, M, c, sx, sy, hgt, lvl=6.0, post=0.14):
    """timber scaffold tower: 4 corner posts, platforms every lvl m with planks, X braces on faces, a ladder"""
    x, y, z = c
    xs = (-sx / 2, sx / 2); ys = (-sy / 2, sy / 2)
    for px in xs:
        for py in ys: mb.rod(M['timber'], (x + px, y + py, z), (x + px, y + py, z + hgt), post * 1.3, post, 5)
    n = int(hgt / lvl)
    for k in range(1, n + 1):
        zz = z + k * lvl
        for px in xs: mb.rod(M['timberdk'], (x + px, y + ys[0], zz), (x + px, y + ys[1], zz), post * 0.8, post * 0.8, 4)
        for py in ys: mb.rod(M['timberdk'], (x + xs[0], y + py, zz), (x + xs[1], y + py, zz), post * 0.8, post * 0.8, 4)
        mb.box(M['plank'], (x, y, zz + 0.1), (sx + 0.4, sy + 0.4, 0.08))
        z0 = zz - lvl
        for py in ys:
            mb.rod(M['timberdk'], (x + xs[0], y + py, z0), (x + xs[1], y + py, zz), post * 0.7, post * 0.7, 4); mb.rod(M['timberdk'], (x + xs[1], y + py, z0), (x + xs[0], y + py, zz), post * 0.7, post * 0.7, 4)
        for px in xs:
            mb.rod(M['timberdk'], (x + px, y + ys[0], z0), (x + px, y + ys[1], zz), post * 0.7, post * 0.7, 4); mb.rod(M['timberdk'], (x + px, y + ys[1], z0), (x + px, y + ys[0], zz), post * 0.7, post * 0.7, 4)

def plane_tree(mb, M, c, s=1.0, seed=0, A='leafA', B='leafB'):
    rr = rnd(seed); x, y, z = c
    mb.rod(M['trunk'], (x, y, z), (x + rr.uniform(-.2, .2) * s, y, z + 4.5 * s), 0.3 * s, 0.2 * s, 8, smooth=True)
    for j in range(rr.randint(6, 8)):
        o = Vector((rr.uniform(-2.0, 2.0), rr.uniform(-2.0, 2.0), rr.uniform(4.2, 7.6))) * s
        mb.ell(M[A if rr.random() < 0.6 else B], (x + o.x, y + o.y, z + o.z), (rr.uniform(1.5, 2.2) * s, rr.uniform(1.5, 2.2) * s, rr.uniform(1.1, 1.6) * s), (12, 8), (0, 0, rr.random() * 6))

def lamppost(mb, M, c, h=3.6):
    x, y, z = c
    mb.rod(M['dark'], (x, y, z), (x, y, z + h), 0.09, 0.06, 6); mb.cyl(M['dark'], (x, y, z + 0.2), 0.14, 0.4, 'z', 8)
    mb.box(M['dark'], (x, y, z + h + 0.05), (0.34, 0.34, 0.08)); mb.ell(M['lamp'], (x, y, z + h + 0.3), (0.2, 0.2, 0.26), (10, 8)); mb.rod(M['dark'], (x, y, z + h + 0.52), (x, y, z + h + 0.7), 0.1, 0.01, 6)

# ------------------------------------------------------------------ Paris: Haussmann blocks, Trocadero, Seine, bridge
def haus(mb, M, x, y, w, d, h, rr, detail=True, yaw=0.0, wall='hwall'):
    mb.push(Matrix.Translation((x, y, 0)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M[wall if detail else 'hwallf'], (0, 0, h / 2), (w, d, h))
    if detail:
        mb.box(M['hstone'], (0, 0, h * 0.30), (w + 0.5, d + 0.5, 0.3)); mb.box(M['hstone'], (0, 0, h * 0.72), (w + 0.5, d + 0.5, 0.3))
    mb.box(M['hstone'], (0, 0, h - 0.3), (w + 1.0, d + 1.0, 0.7))
    z0 = h; rh = 4.6; ins = 2.6; a = w / 2; b = d / 2
    c = [(-a, -b), (a, -b), (a, b), (-a, b)]; t = [(-a + ins, -b + ins), (a - ins, -b + ins), (a - ins, b - ins), (-a + ins, b - ins)]
    mz = M['zinc'] if detail else M['zincf']
    for i in range(4):
        j = (i + 1) % 4
        mb.quad(mz, [(c[i][0], c[i][1], z0), (c[j][0], c[j][1], z0), (t[j][0], t[j][1], z0 + rh), (t[i][0], t[i][1], z0 + rh)][::-1])
    mb.quad(M['zincdk'], [(t[0][0], t[0][1], z0 + rh), (t[1][0], t[1][1], z0 + rh), (t[2][0], t[2][1], z0 + rh), (t[3][0], t[3][1], z0 + rh)])
    if detail:
        nd = max(2, int(w / 6.0))
        for i in range(nd):
            xx = -a + (i + 0.5) * w / nd; mb.box(M['hstone'], (xx, -b + ins * 0.55, z0 + rh * 0.45), (1.2, 0.9, 1.5)); mb.box(M['zincdk'], (xx, -b + ins * 0.5, z0 + rh * 0.45 + 0.95), (1.4, 1.1, 0.35))
        for i in range(rr.randint(2, 3)): mb.box(M['chim'], (rr.uniform(-a * 0.6, a * 0.6), rr.uniform(-b * 0.3, b * 0.3), z0 + rh + 1.0), (0.9, 0.9, 2.4)); 
    mb.pop()

def city_ring(mb, M, rr, zb, rmin, rmax, excl, cell=34.0, detail_r=260.0, wall='hwall', trees=False):
    """jittered grid of Haussmann blocks between radii rmin..rmax (m, around origin), skipping rectangles in excl [(x0,x1,y0,y1)]"""
    n = int(rmax / cell) + 1
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            cx = i * cell + rr.uniform(-3, 3); cy = j * cell + rr.uniform(-3, 3); r = math.hypot(cx, cy)
            if r < rmin or r > rmax: continue
            if any(x0 <= cx <= x1 and y0 <= cy <= y1 for (x0, x1, y0, y1) in excl): continue
            if rr.random() < 0.12: continue
            w = rr.uniform(20, 27); d = rr.uniform(20, 27); h = rr.choice([15.0, 18.0, 21.0, 24.0]) + rr.uniform(-1, 1)
            mb.push(Matrix.Translation((0, 0, zb))); haus(mb, M, cx, cy, w, d, h, rr, detail=(r < detail_r), wall=wall); mb.pop()

def trocadero(mb, M, c, yaw=0.0, k=1.0):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Scale(k, 4))
    mb.box(M['stonedk'], (0, 0, 3), (150, 50, 6))                                                  # terrace base
    ang = np.linspace(-0.95, 0.95, 20)
    for i in range(19):                                                                           # curved wings (arc facing -y)
        a0, a1 = ang[i], ang[i + 1]; R_ = 70.0
        p0 = (R_ * math.sin(a0), -R_ * math.cos(a0) + 66, 0); p1 = (R_ * math.sin(a1), -R_ * math.cos(a1) + 66, 0)
        mx = (p0[0] + p1[0]) / 2; my = (p0[1] + p1[1]) / 2; ln = math.hypot(p1[0] - p0[0], p1[1] - p0[1]) + 0.3; rz = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
        mb.box(M['hwallt'], (mx, my, 14), (ln, 9, 16), rz=rz); mb.box(M['hstone'], (mx, my, 22.5), (ln, 10.5, 1.2), rz=rz); mb.box(M['zinc'], (mx, my, 24.2), (ln, 8, 2.4), rz=rz)
    mb.cyl(M['hwallt'], (0, 14, 20), 20, 40, 'z', 24); mb.cyl(M['hstone'], (0, 14, 40.5), 21.5, 1.4, 'z', 24)
    mb.ell(M['dome'], (0, 14, 41), (19, 19, 15), (24, 12))
    for sx in (-1, 1):                                                                           # the two towers
        mb.box(M['hwallt'], (sx * 68, -4, 36), (9, 9, 72)); mb.box(M['hstone'], (sx * 68, -4, 72.5), (11, 11, 1.4)); mb.box(M['hwallt'], (sx * 68, -4, 78), (7, 7, 10))
        mb.rod(M['zinc'], (sx * 68, -4, 83), (sx * 68, -4, 98), 4.2, 0.2, 8)
    mb.pop()

def seine(mb, M, zb, y0, y1, bend, x0=-1400, x1=1400, n=60):
    xs = np.linspace(x0, x1, n)
    for i in range(n - 1):
        ya0 = y0 + bend * math.sin(xs[i] / 380.0); ya1 = y0 + bend * math.sin(xs[i + 1] / 380.0); yb0 = y1 + bend * math.sin(xs[i] / 380.0); yb1 = y1 + bend * math.sin(xs[i + 1] / 380.0)
        mb.quad(M['water'], [(xs[i], ya0, zb - 0.6), (xs[i + 1], ya1, zb - 0.6), (xs[i + 1], yb1, zb - 0.6), (xs[i], yb0, zb - 0.6)][::-1])

def bridge(mb, M, zb, x, y0, y1, w=22.0):
    mb.box(M['stone'], (x, (y0 + y1) / 2, zb + 1.2), (w, y1 - y0 + 24, 1.4)); 
    for s_ in (-1, 1): mb.box(M['hstone'], (x + s_ * (w / 2 - 0.4), (y0 + y1) / 2, zb + 2.3), (0.8, y1 - y0 + 24, 1.0))
    n = 4
    for i in range(n + 1):
        yy = y0 - 6 + (y1 - y0 + 12) * i / n; mb.box(M['stonedk'], (x, yy, zb - 0.2), (w - 1.0, 5.0, 3.4))
    for i in range(n):
        yy = y0 - 6 + (y1 - y0 + 12) * (i + 0.5) / n; mb.box(M['stone'], (x, yy, zb + 0.55), (w - 1.0, (y1 - y0 + 12) / n - 5.0, 0.7))

def ground_plane(zb, cols, size=2400, rough=1.0, ctr=(0, 300)):
    me = bpy.data.meshes.new('ground'); bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=2, y_segments=2, size=size); bm.to_mesh(me)
    ob = bpy.data.objects.new('ground', me); ob.location = (ctr[0], ctr[1], zb); bpy.context.scene.collection.objects.link(ob)
    m = bpy.data.materials.new('ground'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); bs.inputs['Roughness'].default_value = rough; bs.inputs['Specular IOR Level'].default_value = 0.0
    tc = N('ShaderNodeTexCoord'); L(tc.outputs['Object'], N('ShaderNodeMapping').inputs[0]) if False else None
    def noise(sc_, det):
        n = N('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = sc_; n.inputs['Detail'].default_value = det; L(tc.outputs['Object'], n.inputs[0]); return n
    def ramp(n, a, b):
        r = N('ShaderNodeValToRGB'); L(n.outputs['Fac'], r.inputs[0]); r.color_ramp.elements[0].position = a; r.color_ramp.elements[1].position = b; return r
    c1 = N('ShaderNodeMix'); c1.data_type = 'RGBA'; c1.inputs[6].default_value = hexc(cols[0]); c1.inputs[7].default_value = hexc(cols[1]); L(ramp(noise(0.05, 5), 0.4, 0.6).outputs[0], c1.inputs[0])
    c2 = N('ShaderNodeMix'); c2.data_type = 'RGBA'; L(c1.outputs[2], c2.inputs[6]); c2.inputs[7].default_value = hexc(cols[2]); L(ramp(noise(0.4, 6), 0.45, 0.62).outputs[0], c2.inputs[0])
    c3 = N('ShaderNodeMix'); c3.data_type = 'RGBA'; c3.blend_type = 'MULTIPLY'; c3.inputs[0].default_value = 0.8; L(c2.outputs[2], c3.inputs[6])
    r3 = ramp(noise(4.0, 6), 0.35, 0.65); r3.color_ramp.elements[0].color = (0.75, 0.75, 0.75, 1); r3.color_ramp.elements[1].color = (1.12, 1.12, 1.12, 1); L(r3.outputs[0], c3.inputs[7])
    L(c3.outputs[2], bs.inputs['Base Color']); L(bs.outputs[0], out.inputs['Surface']); ob.data.materials.append(m)

def clouds(P):
    """stacked cumulus: flat dark-warm belly + bumpy lit tops, 2-3 depth layers; emission-only, camera-only"""
    mb = MB('clouds'); rr = rnd(P.get('cloud_seed', 9)); a = mat_emit('cloudA', P['cloud'][0], P.get('cloud_k', 1.0)); b = mat_emit('cloudB', P['cloud'][1], P.get('cloud_k', 1.0)); c = mat_emit('cloudC', P['cloud'][2] if len(P['cloud']) > 2 else P['cloud'][1], P.get('cloud_k', 1.0))
    for i in range(P.get('ncloud', 8)):
        cx = rr.uniform(-700, 700); cy = rr.uniform(700, 1000); cz = rr.uniform(*P.get('cloud_z', (120, 320))); sz = rr.uniform(60, 110) * P.get('cloud_scale', 1.0)
        mb.ell(b, (cx, cy, cz - 0.1 * sz), (sz * 1.5, sz * 0.5, sz * 0.2), (20, 10))
        mb.ell(c, (cx, cy - 8, cz), (sz * 1.3, sz * 0.45, sz * 0.22), (20, 10))
        for j in range(rr.randint(6, 9)):
            ox = rr.uniform(-1.1, 1.1) * sz; r_ = sz * rr.uniform(0.25, 0.5) * (1.2 - abs(ox) / (2.0 * sz))
            mb.ell(a, (cx + ox, cy - 14, cz + 0.12 * sz + r_ * 0.5), (r_, r_ * 0.6, r_ * 0.8), (14, 10))
    for o in mb.finish(shadow=False): o.visible_diffuse = False; o.visible_glossy = False          # painted clouds are camera-only (no warm light on the shade)

# ------------------------------------------------------------------ scenes
def cam_frame(P):
    c = P['cam']; f = Vector(c['look']) - Vector(c['loc']); f.z = 0; f.normalize(); r = Vector((f.y, -f.x, 0)); return Vector(c['loc']), f, r
def at(P, u, f, z=0.0):
    o, F, R_ = cam_frame(P); p = o + F * f + R_ * u; return (p.x, p.y, z)

def horse_card(mb, M, c, yaw=0.0, sc=1.0):
    """flat cut-out draught horse (profile card, 6 cm thick): arched neck, head, mane, four thin legs, hooves, harness"""
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Scale(sc, 4)); h = M['horse']; t = 0.03
    mb.ell(h, (0, 0, 1.3), (1.0, t, 0.5), (16, 8)); mb.ell(h, (0.95, 0, 1.75), (0.38, t, 0.16), (12, 6), (0, -0.9, 0)); mb.ell(h, (1.28, 0, 2.05), (0.3, t, 0.15), (12, 6), (0, -0.35, 0))
    mb.ell(M['horsedk'], (0.85, 0, 1.95), (0.34, t * 1.2, 0.1), (10, 5), (0, -0.9, 0)); mb.ell(M['horsedk'], (-1.0, 0, 1.15), (0.1, t, 0.45), (8, 5), (0, 0.15, 0))
    mb.ell(h, (1.5, 0, 1.98), (0.08, t, 0.07), (6, 4))
    for (lx, k_) in ((0.62, 0), (0.45, 1), (-0.6, 0), (-0.78, 1)):
        mb.box(h, (lx, 0, 0.62), (0.12, t * 1.2, 1.0), ry=0.08 * (1 if k_ else -1)); mb.box(M['horsedk'], (lx + (0.03 if k_ else -0.03), 0, 0.06), (0.15, t * 1.4, 0.12))
    mb.box(M['crimson'], (0.45, 0, 1.52), (0.5, t * 1.6, 0.12)); mb.box(M['dark'], (-0.1, 0, 1.75), (1.6, t * 1.4, 0.04))
    mb.pop()

def worker_card(mb, M, c, yaw, col, h=1.7):
    x, y, z = c; mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(col, (0, 0, h * 0.42), (0.5, 0.04, h * 0.84)); mb.ell(M['canvas'], (0, 0, h - 0.13), (0.13, 0.03, 0.16), (10, 6)); mb.ell(M['dark'], (0, 0, h - 0.04), (0.17, 0.035, 0.07), (8, 4)); mb.pop()

def derrick(mb, M, c, h=34.0, rr=None):
    x, y, z = c
    mb.rod(M['timber'], (x, y, z), (x, y, z + h), 0.28, 0.2, 6); mb.rod(M['timber'], (x, y, z + h * 0.7), (x + h * 0.45, y + 3, z + h * 0.8), 0.18, 0.12, 6)
    mb.rod(M['dark'], (x + h * 0.45, y + 3, z + h * 0.8), (x + h * 0.45, y + 3, z + h * 0.2), 0.03, 0.03, 4); mb.box(M['redlead'], (x + h * 0.45, y + 3, z + h * 0.18), (3.0, 0.3, 0.3))
    for a in (0.6, 2.2, 3.8, 5.4): mb.rod(M['rope'], (x, y, z + h * 0.95), (x + math.cos(a) * h * 0.7, y + math.sin(a) * h * 0.7, z), 0.04, 0.04, 4)
    mb.box(M['timberdk'], (x, y, z + 0.4), (1.6, 1.6, 0.8))

def build_site(P, M):
    rr = rnd(5); lights = []; mb = MB('site'); ts = P['ts']
    mb.push(Matrix.Scale(ts, 4)); tower(mb, M, stage='legs', thick=P['thick']); mb.pop()
    mb.push(Matrix.Scale(ts, 4))
    for (sx, sy) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):                                   # timber scaffold towers propping each leg
        cx_, cy_ = sx * (tw(24) - 3.0), sy * (tw(24) - 3.0)
        scaffold(mb, M, (cx_, cy_, 4.0), 9.0, 9.0, 42.0 if sy < 0 else 30.0, 8.0, 0.8)
        scaffold(mb, M, (sx * (tw(24) + 11.0), sy * (tw(24) - 3.0), 0.0), 7.0, 7.0, 30.0, 8.0, 0.7)
        zc = Z1 + 22.0                                                                   # creeper crane on the inclined top of each leg stub
        px, py = sx * (tw(zc) - th(zc) - 0.6), sy * (tw(zc) - th(zc) - 0.6)
        mb.box(M['redlead'], (px, py, zc + 4.5), (2.0, 2.0, 9.0)); mb.rod(M['redlead'], (px, py, zc + 8.5), (px - sx * 11.0, py, zc + 11.0), 0.7, 0.5, 6)
        mb.rod(M['redlead'], (px, py, zc + 8.5), (px - sx * 3.0, py, zc + 14.0), 0.45, 0.45, 5); mb.rod(M['redlead'], (px - sx * 3.0, py, zc + 14.0), (px - sx * 11.0, py, zc + 11.0), 0.3, 0.3, 5)
        mb.rod(M['dark'], (px - sx * 11.0, py, zc + 11.0), (px - sx * 11.0, py, zc + 3.0), 0.15, 0.15, 4); mb.box(M['redlead'], (px - sx * 11.0, py, zc + 2.6), (0.9, 3.4, 0.9))
    mb.pop(); mb.finish()
    mb = MB('derricks')
    derrick(mb, M, (-0.55 * 63 * ts, 0.0, 0.0), 34.0 * ts, rr); derrick(mb, M, (0.45 * 63 * ts, 12.0, 0.0), 30.0 * ts, rr)
    mb.finish()
    mb = MB('props'); ex = P['props']
    for (u, f, yaw, L_, nx, nz) in ex['girders']: girder_pile(mb, M, at(P, u, f), yaw, L_, nx, nz, rr)
    for (u, f, yaw) in ex['forges']: forge(mb, M, at(P, u, f), yaw, lights, 1.7)
    for (u, f, n) in ex['kegs']:
        for i in range(n): barrel(mb, M, at(P, u + (i % 3) * 0.85 - 0.4, f + (i // 3) * 0.85), 0.95, 0.36, 'timberdk' if i % 2 else 'timber'); 
    for (u, f, yaw, w, d, h) in ex['sheds']: shed(mb, M, at(P, u, f), w, d, h, yaw)
    for (u, f, yaw, load) in ex['carts']:
        cp = Vector(at(P, u, f)); mb.push(Matrix.Translation(cp) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
        mb.box(M['timber'], (0, 0, 1.0), (3.4, 1.5, 0.12))
        for s_ in (-1, 1): mb.box(M['timber'], (0, s_ * 0.74, 1.3), (3.4, 0.08, 0.5))
        wheel(mb, M, (0.2, 0.9, 0.7), 0.7); wheel(mb, M, (0.2, -0.9, 0.7), 0.7); mb.rod(M['timberdk'], (0.2, 0.9, 0.7), (0.2, -0.9, 0.7), 0.05, 0.05, 6)
        for k in range(3): mb.box(M['redlead'], (0, (k - 1) * 0.3, 1.2), (3.2, 0.2, 0.06)); mb.box(M['redlead'], (0, (k - 1) * 0.3, 1.33), (3.2, 0.04, 0.26))
        mb.rod(M['timberdk'], (1.7, 0.4, 1.0), (4.4, 0.4, 0.9), 0.05, 0.04, 6); mb.rod(M['timberdk'], (1.7, -0.4, 1.0), (4.4, -0.4, 0.9), 0.05, 0.04, 6)
        mb.pop(); horse_card(mb, M, (cp.x + math.cos(yaw) * 5.6, cp.y + math.sin(yaw) * 5.6, 0.0), yaw)
    for (u, f, yaw, col) in ex['workers']: worker_card(mb, M, at(P, u, f), yaw, M[col])
    for (u, f) in ex['ladders']:
        p = at(P, u, f)
        for sd in (-0.25, 0.25): mb.rod(M['timber'], (p[0] + sd, p[1], 0), (p[0] + sd, p[1] + 1.0, 4.0), 0.04, 0.04, 5)
        for k in range(10): mb.rod(M['timber'], (p[0] - 0.25, p[1] + 0.25 * k / 2.5 * 0.25, 0.35 + 0.37 * k), (p[0] + 0.25, p[1] + 0.25 * k / 2.5 * 0.25, 0.35 + 0.37 * k), 0.025, 0.025, 4)
    for i in range(70):                                                  # clutter: stones, offcuts, rivet kegs, earth heaps
        u = rr.uniform(-40, 40); f = rr.uniform(14, 120); k = rr.random(); p = at(P, u, f)
        if k < 0.35: mb.ell(M['stonedk'], (p[0], p[1], 0.15), (rr.uniform(.2, .6),) * 2 + (0.22,), (8, 6))
        elif k < 0.7: mb.box(M['timber'], (p[0], p[1], 0.07), (rr.uniform(1.0, 3.0), 0.16, 0.14), rz=rr.uniform(0, 3.1))
        elif k < 0.85: barrel(mb, M, (p[0], p[1], 0), 0.6, 0.22, 'metal'); mb.ell(M['rivet'], (p[0], p[1], 0.62), (0.18, 0.18, 0.04), (8, 4))
        else: mb.ell(M['earthdk'], (p[0], p[1], 0.0), (rr.uniform(1.2, 2.4), rr.uniform(1.0, 1.8), rr.uniform(0.4, 0.8)), (12, 6))
    mb.finish()
    mb = MB('patches')
    for i in range(40):                                                  # trampled dark gravel, ruts, plank walkways
        u = rr.uniform(-60, 60); f = rr.uniform(12, 200); p = at(P, u, f); a = rr.uniform(0, 3.1); w = rr.uniform(4, 16); d_ = rr.uniform(2, 6)
        mb.box(M['gravdk'], (p[0], p[1], 0.012), (w, d_, 0.02), rz=a)
    cp, F_, R_ = cam_frame(P)
    for sd in (-0.9, 0.9):
        for i in range(60):
            p = cp + F_ * (18.0 + i * 3.4) + R_ * (6.0 + sd); mb.box(M['gravdk'], (p.x, p.y, 0.015), (0.35, 3.6, 0.02), rz=math.atan2(F_.y, F_.x) - math.pi / 2)
    for i in range(14): p = cp + F_ * (22.0 + i * 0.5) + R_ * 3.0; mb.box(M['plank'], (p.x, p.y, 0.06), (2.4, 0.4, 0.06), rz=math.atan2(F_.y, F_.x) - math.pi / 2 + 0.2)
    mb.finish()
    mb = MB('city'); Sy = P['seine']
    seine(mb, M, 0.0, Sy[0], Sy[1], 22.0); bridge(mb, M, 0.0, Sy[2], Sy[0], Sy[1] + 10)
    trocadero(mb, M, (Sy[2] + 20, Sy[1] + 120, 0.0), 0.0, 1.4)
    mb.box(M['stone'], (0, Sy[0] - 12, 0.0), (3000, 3, 2.0))
    city_ring(mb, M, rnd(7), 0.0, 230.0, 900.0, [(-1000, 1000, Sy[0] - 30, Sy[1] + 400)], 36.0, 300.0)
    for i in range(-3, 4):
        for sgn in (-1, 1): haus(mb, M, sgn * (P['sidex'] + 18 * (i % 2)), -60 + 33 * (i + 3), rr.uniform(22, 28), 26, rr.choice([18.0, 21.0, 24.0]), rr, True)
    mb.finish()
    return lights

def build_dusk(P, M):
    rr = rnd(11); lights = []; mb = MB('tower'); mb.push(Matrix.Scale(1.0, 4))
    tower(mb, M, stage='full', thick=P['thick'], gal=M['galwall']); mb.pop(); mb.finish()
    mb = MB('antenna'); hx0, hy0, _ = P['hut']; post_top = Vector((hx0 + 3.6, hy0 + 1.6, 6.2)); n = 40
    mb.rod(M['timber'], (post_top.x, post_top.y, 0), (post_top.x, post_top.y, 6.2), 0.16, 0.12, 6); mb.box(M['timber'], (post_top.x, post_top.y, 6.0), (1.6, 0.14, 0.14))
    for wi, (ox, ex_) in enumerate(((-0.5, -0.7), (-0.15, -0.25), (0.2, 0.25), (0.55, 0.7))):
        top = Vector((ox, 0.0, 301.0)); end = post_top + Vector((ex_, 0, -0.1)); mb.cyl(M['white'], end + Vector((0, 0, 0.1)), 0.09, 0.2, 'z', 6)
        for i in range(n):
            u0, u1 = i / n, (i + 1) / n; p0 = top.lerp(end, u0); p1 = top.lerp(end, u1); p0.z -= 2.0 * 4 * u0 * (1 - u0); p1.z -= 2.0 * 4 * u1 * (1 - u1)
            mb.rod(M['wirem'], p0, p1, P['wire_r'] * (1.0 - 0.72 * u0), P['wire_r'] * (1.0 - 0.72 * u1), 4)
    hut = Vector((hx0 + 1.6, hy0 + 0.5, 5.6))
    for i in range(12): mb.rod(M['wirem'], post_top.lerp(hut, i / 12.0) + Vector((0, 0, -0.3 * math.sin(i / 12.0 * 3.14))), post_top.lerp(hut, (i + 1) / 12.0) + Vector((0, 0, -0.3 * math.sin((i + 1) / 12.0 * 3.14))), 0.05, 0.05, 4)
    mb.finish(shadow=False)
    # radio hut + spark gap (emitter)
    mb = MB('hut'); hx, hy, hz = P['hut']
    shed(mb, M, (hx, hy, 0), 5.2, 4.0, 3.2, 0.0, True)
    mb.box(M['lampsm'], (hx - 1.3, hy - 2.06, 1.55), (0.7, 0.05, 0.9)); mb.box(M['dark'], (hx - 1.3, hy - 2.1, 1.55), (0.05, 0.04, 0.9)); mb.box(M['dark'], (hx - 1.3, hy - 2.1, 1.55), (0.7, 0.04, 0.05))
    mb.box(M['plank'], (hx + 3.2, hy - 0.5, 1.0), (1.6, 2.8, 2.0)); mb.box(M['tarroof'], (hx + 3.2, hy - 0.5, 2.1), (1.9, 3.1, 0.12))
    for i in range(4): mb.cyl(M['glasswine'], (hx + 2.7 + i * 0.35, hy - 2.1, 0.45), 0.12, 0.35, 'z', 8)
    mb.box(M['timberdk'], (hx - 0.6, hy - 2.25, 0.12), (1.4, 0.7, 0.24))
    mb.rod(M['dark'], (hx + 1.6, hy + 0.5, 3.2), (hx + 1.6, hy + 0.5, 5.6), 0.12, 0.10, 6); mb.cyl(M['white'], (hx + 1.6, hy + 0.5, 5.3), 0.2, 0.3, 'z', 8)      # lead-in insulator
    sgx, sgy, sgz = hx - 3.6, hy - 2.6, 1.15                                                               # spark gap on a table in front
    mb.box(M['timber'], (sgx, sgy, 0.6), (1.4, 0.9, 1.0)); mb.rod(M['brass'], (sgx - 0.5, sgy, sgz + 0.05), (sgx - 0.12, sgy, sgz + 0.05), 0.07, 0.05, 8); mb.rod(M['brass'], (sgx + 0.5, sgy, sgz + 0.05), (sgx + 0.12, sgy, sgz + 0.05), 0.07, 0.05, 8)
    mb.cyl(M['dark'], (sgx - 0.6, sgy, sgz + 0.18), 0.22, 0.42, 'z', 10); mb.box(M['dark'], (sgx + 0.55, sgy + 0.2, sgz + 0.15), (0.5, 0.4, 0.3))
    mb.finish()
    mb = MB('spark'); s0 = Vector((sgx, sgy, sgz + 0.08)); bb = mat('brassb', '#cba048', '#e8c068', 2, rough=0.25, sheen=0.9)
    mb.ell(bb, s0 + Vector((-0.2, 0, 0)), (0.11, 0.11, 0.11), (12, 8)); mb.ell(bb, s0 + Vector((0.2, 0, 0)), (0.11, 0.11, 0.11), (12, 8))
    p = s0 + Vector((-0.1, 0, 0))
    for k in range(6):                                                                                       # jagged arc between the two balls
        q = Vector((s0.x - 0.1 + 0.2 * (k + 1) / 6.0, s0.y, s0.z + rr.uniform(-0.09, 0.09))); mb.rod(M['sparkc'], p, q, 0.028, 0.024, 4); p = q
    mb.ell(M['sparkhalo'], s0, (0.5, 0.5, 0.5), (14, 10)); mb.ell(M['sparkhalo'], s0, (0.22, 0.22, 0.22), (10, 8))
    for i in range(4):
        a = i * 1.6 + 0.4; p = s0; L_ = 0.5
        for k in range(2): q = p + Vector((math.cos(a) * L_ / 2 + rr.uniform(-.08, .08), rr.uniform(-.1, .1), math.sin(a) * L_ / 2 + rr.uniform(-.05, .1))); mb.rod(M['sparkc'], p, q, 0.02, 0.016, 4); p = q
    mb.finish(shadow=False)
    lights.append((s0 + Vector((0, -0.8, 0.5)), (0.55, 0.72, 1.0), 1500)); lights.append((s0 + Vector((0, 0.6, 1.2)), (0.45, 0.6, 1.0), 700))
    lights.append((Vector((hx - 1.3, hy - 3.0, 1.6)), (1.0, 0.62, 0.26), 160))
    # foreground / mid dressing: lamp posts along the central avenue, fence, trees, benches, gravel paths
    mb = MB('props')
    for yy in np.arange(-210.0, -60.0, 30.0):
        for sx in (-14.0, 16.0): lamppost(mb, M, (sx, yy, 0), 3.8)
    for sx, yy, s_, sd in ((-26, -205, 1.4, 1), (30, -212, 1.5, 2), (-24, -165, 1.5, 3), (28, -170, 1.4, 4), (-30, -130, 1.5, 5), (33, -125, 1.5, 6), (-36, -190, 1.7, 7), (40, -190, 1.6, 8)): plane_tree(mb, M, (sx, yy, 0), s_, sd, 'leafN', 'leafN')
    for k in range(14):
        x = -20 + k * 3.2; mb.rod(M['dark'], (x, -194, 0.0), (x, -194, 1.1), 0.05, 0.05, 5); mb.rod(M['dark'], (x, -194, 0.95), (x + 3.2, -194, 0.95), 0.03, 0.03, 4)
    for (x, y) in ((-3.0, -216), (-4.0, -217), (-13.5, -214), (9.0, -218)): barrel(mb, M, (x, y, 0), 0.95, 0.4, 'timber')
    lamppost(mb, M, (-11.0, -227.0, 0), 4.6)
    cp_ = (-15.0, -210.0)
    mb.push(Matrix.Translation((cp_[0], cp_[1], 0)) @ Euler((0, 0, 0.35)).to_matrix().to_4x4())
    mb.box(M['timberdk'], (0, 0, 1.0), (3.6, 1.6, 0.12))
    for s_ in (-1, 1): mb.box(M['timberdk'], (0, s_ * 0.78, 1.3), (3.6, 0.08, 0.5))
    wheel(mb, M, (0.2, 0.95, 0.7), 0.7); wheel(mb, M, (0.2, -0.95, 0.7), 0.7)
    for i in range(7): mb.box(M['stonedk'] if i % 2 else M['dark'], (-1.2 + (i % 4) * 0.7, (i % 3 - 1) * 0.4, 1.3 + 0.12 * (i // 4)), (0.6, 0.45, 0.35), rz=i)
    for i in range(3): mb.rod(M['metal'], (-1.4 + i * 0.4, -0.7, 1.4), (-0.6 + i * 0.4, 0.5, 2.0 + 0.1 * i), 0.03, 0.03, 4)
    mb.rod(M['timberdk'], (1.8, 0.5, 1.0), (4.6, 0.5, 0.9), 0.05, 0.04, 6); mb.rod(M['timberdk'], (1.8, -0.5, 1.0), (4.6, -0.5, 0.9), 0.05, 0.04, 6)
    mb.pop(); horse_card(mb, M, (cp_[0] + math.cos(0.35) * 5.8, cp_[1] + math.sin(0.35) * 5.8, 0.0), 0.35)
    mb.box(mat('pathg', '#6a7a6c', '#869484', 5), (0.0, -120.0, 0.02), (26.0, 200.0, 0.04))
    for k in range(10):
        a_ = k * 0.62; mb.box(M['gravel'], (math.cos(a_) * 6, -60.0 + k * -1.0, 0.025), (2.0, 120.0, 0.04), rz=0.0) if False else None
    for sx in (-1, 1):
        for yy in np.arange(-205.0, -60.0, 12.0): mb.ell(M['leafN'], (sx * 17.5, yy, 0.5), (0.9, 0.9, 0.55), (8, 6))      # clipped hedge along the avenue
    mb.finish()
    for (x, y, z) in [(-14, -150, 4.2), (16, -150, 4.2), (-14, -90, 4.2), (16, -90, 4.2), (-14, -180, 4.2), (16, -180, 4.2)]: lights.append((Vector((x, y, z)), (1.0, 0.66, 0.32), 350))
    # gas lamps in the tower: a few strong points near the gallery and the lantern (visible glow comes from emissives)
    for z, a in ((Z1 + 8, 38.0), (Z2 + 1.5, 22.0)):
        for (sx, sy) in ((-1, -1), (1, -1)): lights.append((Vector((sx * a, sy * a, z)), (1.0, 0.66, 0.3), 90000 if z < 100 else 40000))
    mb = MB('city'); Sy = P['seine']
    seine(mb, M, 0.0, Sy[0], Sy[1], 30.0); mb.box(M['stone'], (0, Sy[0] - 12, 0.0), (3000, 3, 2.0)); bridge(mb, M, 0.0, Sy[0], Sy[1] + 10, 24.0)
    trocadero(mb, M, (24, Sy[1] + 150, 0.0), 0.0, 1.5)
    city_ring(mb, M, rnd(21), 0.0, 105.0, 900.0, [(-52, 52, -300, Sy[0] - 30)], 36.0, 520.0, wall='hwall')
    mb.finish()
    return lights

def window_cut_wall(mb, m, axis, pos, lo, hi, z0, z1, wins, zlo=0.0, zhi=5.6):
    """wall plane at y=pos (axis 'y', spans x lo..hi) or x=pos (axis 'x', spans y lo..hi) with rectangular openings (wins=[(a,b,za,zb)]) as boxes around them"""
    def box(a, b, za, zb):
        if b - a < 0.01 or zb - za < 0.01: return
        if axis == 'y': mb.box(m, ((a + b) / 2, pos, (za + zb) / 2), (b - a, 0.3, zb - za))
        else: mb.box(m, (pos, (a + b) / 2, (za + zb) / 2), (0.3, b - a, zb - za))
    cur = lo
    for (a, b, za, zb) in sorted(wins):
        box(cur, a, zlo, zhi); box(a, b, zlo, za); box(a, b, zb, zhi); cur = b
    box(cur, hi, zlo, zhi)

def chair(mb, M, c, yaw):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4()); bm = M['bent']
    mb.cyl(M['crimson'], (0, 0, 0.46), 0.22, 0.05, 'z', 14); mb.cyl(bm, (0, 0, 0.43), 0.21, 0.04, 'z', 14)
    for (x, y) in ((0.15, 0.15), (-0.15, 0.15), (0.15, -0.15), (-0.15, -0.15)): mb.rod(bm, (x, y, 0.0), (x * 1.1, y * 1.1, 0.44), 0.016, 0.02, 5)
    for sx in (-1, 1): mb.rod(bm, (sx * 0.15, 0.2, 0.46), (sx * 0.14, 0.24, 0.95), 0.017, 0.014, 5)
    n = 12
    for i in range(n):                                                                        # hoop back
        a0 = -1.2 + 2.4 * i / n; a1 = -1.2 + 2.4 * (i + 1) / n
        mb.rod(bm, (0.15 * math.sin(a0) * 1.15, 0.24, 0.92 - 0.1 * (1 - math.cos(a0))), (0.15 * math.sin(a1) * 1.15, 0.24, 0.92 - 0.1 * (1 - math.cos(a1))), 0.014, 0.014, 4)
    mb.rod(bm, (-0.14, 0.24, 0.66), (0.14, 0.24, 0.66), 0.012, 0.012, 4); mb.rod(bm, (0, 0.24, 0.66), (0, 0.24, 0.9), 0.012, 0.012, 4)
    mb.pop()

def table(mb, M, c, rr, lit=True, lights=None, rect=False):
    x, y, z = c
    mb.cyl(M['cloth'], (x, y, 0.745), 0.7, 0.03, 'z', 24); mb.cyl(M['cloth'], (x, y, 0.38), 0.68, 0.72, 'z', 24, r2=0.68, smooth=True)
    for k in range(8): a_ = k * math.pi / 4; mb.box(M['cloth'], (x + math.cos(a_) * 0.7, y + math.sin(a_) * 0.7, 0.38), (0.04, 0.04, 0.7), rz=a_)
    mb.rod(M['gold'], (x, y, 0.76), (x, y, 1.0), 0.02, 0.02, 6)
    mb.ell(M['lamp'], (x, y, 1.05), (0.07, 0.07, 0.1), (8, 6)); mb.cyl(M['gold'], (x, y, 0.98), 0.05, 0.04, 'z', 8)
    if lights is not None and lit: lights.append((Vector((x, y, 1.1)), (1.0, 0.68, 0.34), 14))
    for k in range(4):
        a = k * math.pi / 2 + 0.4; px = x + math.cos(a) * 0.36; py = y + math.sin(a) * 0.36
        mb.cyl(M['white'], (px, py, 0.765), 0.13, 0.015, 'z', 14); mb.cyl(M['gold'], (px, py, 0.775), 0.09, 0.006, 'z', 12)
        gx = x + math.cos(a + 0.55) * 0.34; gy = y + math.sin(a + 0.55) * 0.34; mb.cyl(M['glasswine'], (gx, gy, 0.83), 0.03, 0.14, 'z', 8, r2=0.04)
        mb.ell(M['white'], (x + math.cos(a - 0.5) * 0.3, y + math.sin(a - 0.5) * 0.3, 0.79), (0.045, 0.03, 0.03), (6, 4))
    mb.cyl(M['wineg' if rr.random() < 0.6 else 'wineamb'], (x + 0.1, y - 0.08, 0.89), 0.04, 0.24, 'z', 8, r2=0.025)
    mb.cyl(M['crimson'], (x - 0.12, y + 0.05, 0.76), 0.08, 0.02, 'z', 8)

def palm(mb, M, c, s=1.0, seed=0):
    rr = rnd(seed); x, y, z = c
    mb.cyl(M['gold'], (x, y, z + 0.25 * s), 0.3 * s, 0.5 * s, 'z', 14, r2=0.26 * s); mb.cyl(M['earth'], (x, y, z + 0.52 * s), 0.25 * s, 0.04, 'z', 14)
    for i in range(9):
        a = i * 0.7 + rr.random() * 0.3; up = rr.uniform(0.7, 1.3); L_ = rr.uniform(0.9, 1.3) * s
        p0 = Vector((x, y, z + 0.55 * s)); p1 = p0 + Vector((math.cos(a) * 0.35 * L_, math.sin(a) * 0.35 * L_, up * 0.6 * s)); p2 = p1 + Vector((math.cos(a) * 0.7 * L_, math.sin(a) * 0.7 * L_, -0.15 * s))
        mb.rod(M['leafA'], p0, p1, 0.02 * s, 0.015 * s, 5); mb.rod(M['leafA'], p1, p2, 0.015 * s, 0.01 * s, 5)
        for k in range(8):
            q = p1.lerp(p2, k / 8.0); mb.ell(M['leafA'], q + Vector((0, 0, -0.04 * s)), (0.07 * s, 0.07 * s, 0.01 * s) if False else (0.16 * s, 0.05 * s, 0.012 * s), (6, 4), (0, 0, a + 1.57))

def build_resto(P, M):
    rr = rnd(3); lights = []; mb = MB('room')
    X0, X1, Y0, Y1, ZH = -4.8, 4.8, -9.0, 17.0, 4.5
    mb.box(M['floor'], (0, (Y0 + Y1) / 2, -0.05), (X1 - X0, Y1 - Y0, 0.1))
    mb.box(M['gold'], (0.0, (Y0 + Y1) / 2, 0.005), (2.0, Y1 - Y0 - 0.5, 0.01)); mb.box(M['crimson'], (0.0, (Y0 + Y1) / 2, 0.008), (1.8, Y1 - Y0 - 0.6, 0.012))
    mb.box(M['navy'], (0.0, (Y0 + Y1) / 2, 0.012), (1.35, Y1 - Y0 - 0.9, 0.012))
    pass
    mb.box(mat("ceil", "#8a4e28", "#a46434", 3), (0, (Y0 + Y1) / 2, ZH + 0.1), (X1 - X0 + 0.6, Y1 - Y0 + 0.6, 0.3))
    # far wall (windows onto Paris) and left wall (windows with sun), right wall (mirrors + crimson panels)
    fw = [(-4.3 + i * 3.2, -4.3 + i * 3.2 + 2.6, 0.0, 3.8) for i in range(3)]
    window_cut_wall(mb, M['wallres'], 'y', Y1, X0, X1, 0, ZH, fw, 0, ZH)
    lw = [(-3.6, -0.1, 0.0, 3.8), (1.1, 4.6, 0.0, 3.8), (5.8, 9.3, 0.0, 3.8), (10.5, 14.0, 0.0, 3.8)]
    window_cut_wall(mb, M['wallres'], 'x', X0, Y0, Y1, 0, ZH, [w for w in lw if w[1] < Y1 - 0.5], 0, ZH)
    mb.box(M['wallpan'], (X1, (Y0 + Y1) / 2, 1.2), (0.3, Y1 - Y0, 2.4)); mb.box(M['wallres'], (X1, (Y0 + Y1) / 2, 4.1), (0.3, Y1 - Y0, 3.4)); mb.box(M['gold'], (X1 - 0.2, (Y0 + Y1) / 2, 2.45), (0.1, Y1 - Y0, 0.12))
    mb.box(M['wallres'], (0, Y0 - 0.2, ZH / 2), (X1 - X0, 0.3, ZH))
    for i in range(7):                                                                         # right wall: gilt framed mirrors + crimson drape strips
        yy = Y0 + 2.0 + i * 3.5
        mb.box(M['gold'], (X1 - 0.2, yy, 3.4), (0.08, 1.7, 2.6)); mb.box(M['mirror'], (X1 - 0.26, yy, 3.4), (0.05, 1.4, 2.3))
        mb.box(M['crimson'], (X1 - 0.2, yy + 1.75, 3.0), (0.08, 0.55, 3.8))
    for yy in np.arange(Y0 + 0.5, Y1, 1.7): mb.box(M['gold'], (X1 - 0.17, yy, 0.95), (0.05, 0.12, 1.0))
    mb.box(M['crimson'], (X1 - 0.6, (Y0 + Y1) / 2, 0.45), (0.8, Y1 - Y0 - 0.4, 0.9)); mb.box(M['crimdk'], (X1 - 0.3, (Y0 + Y1) / 2, 1.1), (0.2, Y1 - Y0 - 0.4, 0.5))      # banquette
    mb.box(M['gold'], (0, Y1 - 0.2, ZH - 0.3), (X1 - X0, 0.12, 0.5))
    for yy in np.arange(Y0 + 1.0, Y1, 2.6): mb.box(M['gold'], (0, yy, ZH - 0.02), (X1 - X0, 0.09, 0.05))           # ceiling coffers: gilt strips
    for xx in (-3.6, -1.2, 1.2, 3.6): mb.box(M['gold'], (xx, (Y0 + Y1) / 2, ZH - 0.02), (0.09, Y1 - Y0, 0.05))
    cf = mat('coffer', '#7a4624', '#92582c', 3)
    for yy in np.arange(Y0 + 2.3, Y1 - 1, 2.6):
        for xx in (-2.4, 0.0, 2.4): mb.box(cf, (xx, yy, ZH - 0.1), (2.0, 2.2, 0.14))
    mb.box(M['gold'], (X0 + 0.12, (Y0 + Y1) / 2, ZH - 0.3), (0.12, Y1 - Y0, 0.45)); mb.box(M['gold'], (X1 - 0.12, (Y0 + Y1) / 2, ZH - 0.3), (0.12, Y1 - Y0, 0.45))
    # window dressing: gilt frames, crimson curtains pulled to sides
    for (a, b, za, zb) in fw:
        mb.box(M['gold'], ((a + b) / 2, Y1 - 0.2, zb + 0.14), (b - a + 0.5, 0.12, 0.26)); mb.box(M['crimson'], (a - 0.35, Y1 - 0.4, 2.4), (0.5, 0.35, 4.8)); mb.box(M['crimson'], (b + 0.35, Y1 - 0.4, 2.4), (0.5, 0.35, 4.8))
        mb.box(M['crimdk'], ((a + b) / 2, Y1 - 0.4, zb + 0.5), (b - a + 1.4, 0.35, 0.5))
        for t in np.linspace(a + 0.6, b - 0.6, 3): mb.box(M['iron'], (t, Y1 - 0.1, 2.5), (0.07, 0.05, 5.0))
        mb.box(M['iron'], ((a + b) / 2, Y1 - 0.1, 2.5), (b - a, 0.05, 0.07))
    for (a, b, za, zb) in lw:
        if b > Y1 - 0.5: continue
        mb.box(M['gold'], (X0 + 0.2, (a + b) / 2, zb + 0.14), (0.12, b - a + 0.5, 0.26)); mb.box(M['crimson'], (X0 + 0.45, a - 0.3, 2.3), (0.35, 0.45, 4.6)); mb.box(M['crimson'], (X0 + 0.45, b + 0.3, 2.3), (0.35, 0.45, 4.6))
        mb.box(M['iron'], (X0 + 0.12, (a + b) / 2, 2.35), (0.05, 0.06, 4.7)); mb.box(M['iron'], (X0 + 0.12, (a + b) / 2, 3.2), (0.05, b - a, 0.06))
    mb.finish()
    # ---- the tower's own riveted iron: columns, ceiling girders (Warren trusses), diagonal leg strut, outside lattice
    mb = MB('iron'); I = mat('irondk', '#7a3626', '#9a4a34', 5, contrast=1.2); IL = mat('irondk2', '#8a4230', '#aa5c40', 5, contrast=1.2)
    def rivets(p0, p1, n, off, z):
        for i in range(n):
            t = (i + 0.5) / n; mb.ell(M['rivet'] if False else IL, (p0[0] + (p1[0] - p0[0]) * t + off[0], p0[1] + (p1[1] - p0[1]) * t + off[1], z), (0.025, 0.025, 0.025), (5, 4))
    for (x, y) in ((-4.3, 0.8), (-4.3, 6.2), (-4.3, 11.0), (-4.3, 16.0), (4.3, 0.8), (4.3, 6.2), (4.3, 11.0), (4.3, 16.0)):
        mb.box(I, (x, y, ZH / 2), (0.55, 0.55, ZH)); mb.box(IL, (x, y, 0.25), (0.8, 0.8, 0.5)); mb.box(M['gold'], (x, y, ZH - 0.35), (0.75, 0.75, 0.3)); mb.box(I, (x, y, ZH - 0.1), (0.9, 0.9, 0.3))
        for k in range(10): mb.ell(IL, (x + 0.29, y, 0.5 + k * 0.5), (0.03, 0.03, 0.03), (5, 4)); mb.ell(IL, (x, y - 0.29, 0.5 + k * 0.5), (0.03, 0.03, 0.03), (5, 4))
    for yy in (3.0, 9.0, 14.5):                                                                      # Warren truss across the ceiling
        zt, zb_ = ZH - 0.05, ZH - 1.3
        mb.box(I, (0, yy, zt), (X1 - X0, 0.5, 0.25)); mb.box(I, (0, yy, zb_), (X1 - X0, 0.5, 0.25))
        n = 13
        for i in range(n):
            x0 = X0 + (X1 - X0) * i / n; x1 = X0 + (X1 - X0) * (i + 1) / n
            mb.rod(IL, (x0, yy, zb_ if i % 2 == 0 else zt), (x1, yy, zt if i % 2 == 0 else zb_), 0.07, 0.07, 4); mb.rod(IL, (x0, yy, zb_), (x0, yy, zt), 0.055, 0.055, 4)
        for i in range(30): mb.ell(IL, (X0 + 0.3 + i * 0.43, yy - 0.26, zb_), (0.03, 0.03, 0.03), (5, 4))
    pass          # longitudinal beams
    # inclined leg member crossing the room near the right wall (passes through floor and ceiling), lattice-braced
    a_ = Vector((3.4, 8.6, -0.2)); b_ = Vector((3.0, 10.4, ZH + 0.2))
    for (ox, oy) in ((-0.28, -0.28), (0.28, -0.28), (0.28, 0.28), (-0.28, 0.28)): mb.rod(I, a_ + Vector((ox, oy, 0)), b_ + Vector((ox, oy, 0)), 0.1, 0.1, 4)
    for k in range(9):
        p0 = a_.lerp(b_, k / 9.0); p1 = a_.lerp(b_, (k + 1) / 9.0)
        mb.rod(IL, p0 + Vector((-0.28, -0.28, 0)), p1 + Vector((0.28, -0.28, 0)), 0.04, 0.04, 4); mb.rod(IL, p0 + Vector((0.28, -0.28, 0)), p1 + Vector((-0.28, -0.28, 0)), 0.04, 0.04, 4)
        mb.rod(IL, p0 + Vector((0.28, -0.28, 0)), p1 + Vector((0.28, 0.28, 0)), 0.04, 0.04, 4)
    for (a_, b_, za_, zb_) in lw:                                                                # riveted lattice girders crossing the glass from outside (left windows)
        xo = X0 - 0.5
        for rr_ in (0.1,): 
            mb.rod(I, (xo, a_ - 0.1, 0.0), (xo, b_ + 0.1, zb_ + 0.3), 0.11, 0.11, 4); mb.rod(I, (xo, b_ + 0.1, 0.0), (xo, a_ - 0.1, zb_ + 0.3), 0.11, 0.11, 4)
            mb.rod(IL, (xo, a_ - 0.1, 1.9), (xo, b_ + 0.1, 1.9), 0.08, 0.08, 4); mb.rod(I, (xo, (a_ + b_) / 2, 0.0), (xo, (a_ + b_) / 2, zb_ + 0.3), 0.07, 0.07, 4)
    for (a_, b_, za_, zb_) in fw:
        yo = Y1 + 0.55
        mb.rod(I, (a_ - 0.1, yo, 0.0), (b_ + 0.1, yo, zb_ + 0.3), 0.11, 0.11, 4); mb.rod(I, (b_ + 0.1, yo, 0.0), (a_ - 0.1, yo, zb_ + 0.3), 0.11, 0.11, 4); mb.rod(IL, (a_ - 0.1, yo, 1.9), (b_ + 0.1, yo, 1.9), 0.08, 0.08, 4)
    # outside the far windows: the tower's lattice screen + stanchions and railing, a leg descending
    for i in range(14):
        x = X0 + 0.3 + i * (X1 - X0) / 13.0; mb.box(I, (x, Y1 + 0.9, 0.7), (0.06, 0.06, 1.4))
    mb.box(I, (0, Y1 + 0.9, 1.4), (X1 - X0, 0.08, 0.08)); mb.box(IL, (0, Y1 + 1.0, 0.0), (X1 - X0, 2.0, 0.08))
    for sx in (-1, 1):
        ax = Vector((sx * 2.4, Y1 + 3.5, 4.8)); bx = Vector((sx * 5.2, Y1 + 8.0, -30.0))
        for (ox, oy) in ((-0.5, 0), (0.5, 0)): mb.rod(I, ax + Vector((ox, oy, 0)), bx + Vector((ox * 1.6, oy, 0)), 0.2, 0.28, 4)
        for k in range(24):
            p0 = ax.lerp(bx, k / 24.0); p1 = ax.lerp(bx, (k + 1) / 24.0); w0 = 0.5 + 0.1 * k / 24.0
            mb.rod(IL, p0 + Vector((-w0, 0, 0)), p1 + Vector((w0, 0, 0)), 0.07, 0.07, 4); mb.rod(IL, p0 + Vector((w0, 0, 0)), p1 + Vector((-w0, 0, 0)), 0.07, 0.07, 4)
    mb.box(I, (0, Y1 + 5.0, 3.5), (X1 - X0 + 14.0, 0.5, 0.5)); mb.box(IL, (0, Y1 + 5.0, 2.5), (X1 - X0 + 14.0, 0.3, 0.3))
    for k in range(8): mb.rod(IL, (-9 + k * 2.4, Y1 + 5.0, 3.1), (-9 + (k + 1) * 2.4, Y1 + 5.0, 2.7), 0.06, 0.06, 4)
    mb.finish()
    # ---- furniture: tables (rows), chairs, gas lamps, chandeliers
    mb = MB('furn'); tabs = [(0.0, -3.4), (-2.9, 2.6), (-2.9, 6.6), (-2.9, 10.6), (-2.9, 14.2), (2.6, 6.0), (0.2, 14.4), (-0.4, 4.6)]
    lamps = []
    for i, (x, y) in enumerate(tabs):
        if (x, y) == (-0.3, 6.5): continue
        table(mb, M, (x, y, 0), rr, True, lights if i % 2 == 0 else None)
        for k in range(4):
            a = k * math.pi / 2 + 0.3 + rr.uniform(-0.2, 0.2); chair(mb, M, (x + math.cos(a) * 0.9, y + math.sin(a) * 0.9, 0), a - math.pi / 2)
    # hero table (the puppet's): table + 2 chairs, grey placeholder card behind it
    hx, hy = P['hero']
    table(mb, M, (hx, hy, 0), rr, True, lights); chair(mb, M, (hx + 0.95, hy - 0.1, 0), -math.pi / 2 + 0.2); chair(mb, M, (hx, hy + 0.95, 0), 0.0); chair(mb, M, (hx - 0.9, hy - 0.1, 0), math.pi / 2 - 0.3)
    bx, by = 3.5, 10.0                                                                                    # buffet / sideboard with a gilt mirror screen
    mb.box(M['wallpan'], (bx, by, 0.5), (0.8, 2.8, 1.0)); mb.box(M['cloth'], (bx, by, 1.03), (0.9, 2.9, 0.06)); mb.box(M['gold'], (bx + 0.55, by, 2.4), (0.1, 2.2, 2.6)); mb.box(M['mirror'], (bx + 0.48, by, 2.4), (0.05, 1.9, 2.3))
    for i in range(4): mb.ell(M['metal'], (bx, by - 1.1 + i * 0.7, 1.2), (0.2, 0.2, 0.16), (12, 8)); mb.cyl(M['metal'], (bx, by - 1.1 + i * 0.7, 1.07), 0.22, 0.03, 'z', 12)
    for i in range(3): mb.cyl(M['wineg'], (bx - 0.1, by - 0.9 + i * 0.9 + 0.3, 1.2), 0.04, 0.3, 'z', 8, r2=0.025)
    mb.ell(M['crimson'], (bx, by + 1.2, 1.13), (0.15, 0.15, 0.1), (8, 6)); mb.ell(M['gold'], (bx - 0.1, by + 1.0, 1.12), (0.12, 0.12, 0.09), (8, 6))
    for (x, y) in ((3.9, 7.2), (3.9, 12.8)): mb.box(M['gold'], (x, y, 1.0), (0.1, 0.6, 2.0)); mb.box(M['mirror'], (x - 0.06, y, 1.2), (0.05, 0.45, 1.5))
    for (tx, ty) in ((-2.9, 6.6), (-2.9, 10.6), (2.6, 6.0), (0.2, 14.4), (-2.9, 14.2)):                      # seated diner stand-ins
        mb.box(M['cardg'], (tx, ty + 0.92, 0.45 + 0.62), (0.5, 0.04, 1.25)); mb.ell(M['cardg'], (tx, ty + 0.92, 1.8), (0.13, 0.03, 0.16), (10, 6))
    for (a, b, za, zb) in lw + fw:
        pass
    palm(mb, M, (-4.2, 15.8, 0.0), 1.5, 2); palm(mb, M, (4.1, 15.5, 0.0), 1.4, 3)
    mb.finish()
    mb = MB('card'); g = mat('card', '#6a6874', None, 1, rough=1.0)
    mb.box(g, (hx - 0.05, hy + 0.98, 0.45 + 0.625), (0.55, 0.03, 1.25)); mb.ell(g, (hx - 0.05, hy + 0.98, 1.78), (0.14, 0.03, 0.16), (10, 8)); mb.finish()
    mb = MB('lampsx')
    for (x, y) in ((X1 - 0.5, 1.5), (X1 - 0.5, 8.5), (X1 - 0.5, 14.5), (X0 + 0.55, 3.0), (X0 + 0.55, 12.4)):
        mb.rod(M['gold'], (x, y, 2.6), (x, y, 3.0), 0.04, 0.04, 6); mb.ell(M['lamp'], (x - (0.0 if x > 0 else -0.0), y, 3.15), (0.14, 0.14, 0.2), (10, 8)); lights.append((Vector((x - 0.1 * (1 if x > 0 else -1), y, 3.1)), (1.0, 0.66, 0.3), 20))
    for (x, y) in ((0, 1.0), (0, 6.0), (0, 11.0), (0, 15.5)):                                                  # hanging gasoliers from the girders
        mb.rod(M['gold'], (x, y, ZH - 1.3), (x, y, 4.0), 0.02, 0.02, 5); mb.cyl(M['gold'], (x, y, 3.95), 0.45, 0.05, 'z', 16)
        for k in range(6):
            a = k * math.pi / 3; mb.ell(M['lamp'], (x + math.cos(a) * 0.42, y + math.sin(a) * 0.42, 4.1), (0.12, 0.12, 0.16), (8, 6))
        lights.append((Vector((x, y, 2.7)), (1.0, 0.68, 0.34), 18))
    mb.finish()
    # ---- outside: Paris far below (stylised nearer), Seine, Trocadero beyond
    mb = MB('city'); zb = P['zbase']; mb.push(Matrix.Rotation(0.62, 4, 'Z'))
    seine(mb, M, zb, 330.0, 375.0, 30.0, -2000, 2000, 80)
    bridge(mb, M, zb, 40.0, 330.0, 375.0, 24.0)
    trocadero(mb, M, (30, 520.0, zb), 0.0, 1.5)
    city_ring(mb, M, rnd(31), zb, 70.0, 1100.0, [(-2000, 2000, 310, 390), (-300, 300, 390, 700)], 38.0, 150.0)
    mb.pop(); mb.finish()
    return lights

# ------------------------------------------------------------------ world, lights, camera, render
def sky_world(P):
    w = bpy.data.worlds.new('sky'); bpy.context.scene.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputWorld'); bg = N('ShaderNodeBackground'); tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Generated'], sp.inputs[0])
    cr = N('ShaderNodeValToRGB'); L(sp.outputs['Z'], cr.inputs[0]); stops = P['sky']
    cr.color_ramp.elements[0].position = stops[0][0]; cr.color_ramp.elements[0].color = hexc(stops[0][1])
    for pos, col in stops[1:-1]: e = cr.color_ramp.elements.new(pos); e.color = hexc(col)
    cr.color_ramp.elements[-1].position = stops[-1][0]; cr.color_ramp.elements[-1].color = hexc(stops[-1][1])
    bg.inputs['Strength'].default_value = P['sky_k']; L(cr.outputs[0], bg.inputs['Color'])
    lp = N('ShaderNodeLightPath'); b2 = N('ShaderNodeBackground'); b2.inputs['Color'].default_value = hexc(P['amb'][0]); b2.inputs['Strength'].default_value = P['amb'][1]
    mx = N('ShaderNodeMixShader'); L(lp.outputs['Is Camera Ray'], mx.inputs[0]); L(b2.outputs[0], mx.inputs[1]); L(bg.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])

def lights_setup(P, extra):
    sc = bpy.context.scene; k = P['key']; kd = Vector(P['key_dir']).normalized()
    d = bpy.data.lights.new('key', 'SUN'); d.color = k[:3]; d.energy = k[3]; d.angle = math.radians(P['sun_angle'])
    o = bpy.data.objects.new('key', d); sc.collection.objects.link(o); o.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler()
    for i, (p, col, en) in enumerate(extra):
        if en <= 0: continue
        l = bpy.data.lights.new('pt%d' % i, 'POINT'); l.color = col; l.energy = en; l.shadow_soft_size = 0.25 if en < 1000 else 0.6
        ob = bpy.data.objects.new('pt%d' % i, l); ob.location = p; sc.collection.objects.link(ob)
    if P.get('winfill'):
        wc, we = P['winfill']
        for (y0_, y1_) in ((-3.6, -0.1), (1.1, 4.6), (5.8, 9.3), (10.5, 14.0)):
            l = bpy.data.lights.new('wf', 'AREA'); l.shape = 'RECTANGLE'; l.size = 3.0; l.size_y = 3.4; l.color = wc; l.energy = we
            ob = bpy.data.objects.new('wf', l); ob.location = (-5.9, (y0_ + y1_) / 2, 2.0); ob.rotation_euler = (0, -math.pi / 2, 0); sc.collection.objects.link(ob); ob.visible_camera = False
        for x_ in (-3.2, 0.0, 3.2):
            l = bpy.data.lights.new('wf2', 'AREA'); l.shape = 'RECTANGLE'; l.size = 2.4; l.size_y = 3.4; l.color = wc; l.energy = we * 0.6
            ob = bpy.data.objects.new('wf2', l); ob.location = (x_, 18.2, 2.0); ob.rotation_euler = (-math.pi / 2, 0, 0); sc.collection.objects.link(ob); ob.visible_camera = False
    if P.get('fill'):
        f = P['fill']; l = bpy.data.lights.new('fill', 'AREA'); l.shape = 'RECTANGLE'; l.size = f[4]; l.size_y = f[5]; l.color = f[:3]; l.energy = f[3]
        ob = bpy.data.objects.new('fill', l); ob.location = f[6]; sc.collection.objects.link(ob); ob.visible_camera = False

def setup_camera(P):
    sc = bpy.context.scene; c = P['cam']
    cd = bpy.data.cameras.new('cam'); cd.lens = c['lens']; cd.sensor_width = 36; cd.sensor_fit = 'AUTO'; cd.dof.use_dof = False; cd.shift_y = c.get('shift', 0.0); cd.clip_end = 6000
    ob = bpy.data.objects.new('cam', cd); sc.collection.objects.link(ob); ob.location = c['loc']
    ob.rotation_euler = (Vector(c['look']) - Vector(c['loc'])).to_track_quat('-Z', 'Y').to_euler(); sc.camera = ob

def grade(a, P):
    g = a.mean(-1, keepdims=True); return np.clip(g + (a - g) * P.get('sat', 1.08), 0, 1)

def _rd(sc, path, samples, denoise, transp=False):
    cy = sc.cycles; cy.samples = samples; cy.use_denoising = denoise; sc.render.film_transparent = transp
    sc.render.filepath = path; bpy.ops.render.render(write_still=True)
    im = Image.open(path).convert('RGBA'); a = np.asarray(im, dtype=np.float32) / 255.0; os.remove(path); return a

def render(mode, out, samples, draft, P):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; cy = sc.cycles; cy.device = 'CPU'; cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'
    cy.denoising_input_passes = 'RGB_ALBEDO_NORMAL'; cy.max_bounces = 4; cy.diffuse_bounces = P.get('dbounce', 1); cy.glossy_bounces = 1; cy.transmission_bounces = 0; cy.transparent_max_bounces = 8
    cy.use_light_tree = True; cy.filter_width = 1.2; sc.render.threads = 4
    sc.render.resolution_x = W // (2 if draft else 1); sc.render.resolution_y = H // (2 if draft else 1); sc.render.resolution_percentage = 100
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = P.get('exposure', 0.0)
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
    A = _rd(sc, out + '_A.png', samples, True)[..., :3]
    # shade mask for the hue check only: sun-only render, white override, no bounces, sky hidden; shade = geometry where a nearer object blocks the sun
    for l in bpy.data.lights:
        if l.name != 'key': l.energy = 0.0
    wbgs = [n for n in bpy.data.worlds['sky'].node_tree.nodes if n.bl_idname == 'ShaderNodeBackground']
    for n in wbgs: n.inputs['Strength'].default_value = 0.0
    for o in bpy.data.objects:
        if o.name.startswith(('clouds', 'spark')): o.hide_render = True
    wm = bpy.data.materials.new('ovr'); wm.use_nodes = True; bs = wm.node_tree.nodes['Principled BSDF']; bs.inputs['Base Color'].default_value = (1, 1, 1, 1)
    bs.inputs['Roughness'].default_value = 1.0; bs.inputs['Specular IOR Level'].default_value = 0.0
    cy.max_bounces = 0; cy.diffuse_bounces = 0; cy.glossy_bounces = 0; bpy.context.view_layer.material_override = wm
    D = _rd(sc, out + '_D.png', 16, False, True); bpy.context.view_layer.material_override = None
    lD = 0.3 * D[..., 0] + 0.59 * D[..., 1] + 0.11 * D[..., 2]
    vs = [(o, o.visible_shadow) for o in bpy.data.objects if o.type == 'MESH']
    for o, _ in vs: o.visible_shadow = False
    D2 = _rd(sc, out + '_D2.png', 6, False, True)
    lD2 = 0.3 * D2[..., 0] + 0.59 * D2[..., 1] + 0.11 * D2[..., 2]
    cast = (D[..., 3] > 0.99) & (lD < 0.02) & (lD2 > 0.08)
    Image.fromarray((cast * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5)).save(out + '_shade.png')
    a = grade(A, P); Image.fromarray((a * 255 + 0.5).astype(np.uint8)).save(out + '.jpg', quality=93)

def kd_from(travel): return tuple(travel)

PRESETS = {
 'site': dict(
    sky=[(0.0, '#f8c48c'), (0.1, '#f6c89c'), (0.26, '#e0c4c4'), (0.46, '#a4b8ec'), (0.72, '#6e8cdc'), (1.0, '#4260cc')], sky_k=0.8, amb=('#5e84FF', 2.4),
    key=(1.0, 0.82, 0.58, 9.0), dbounce=0, key_dir=(0.50, 0.42, -0.42), sun_angle=1.0, exposure=-0.8, sat=1.08, ts=1.0, thick=2.0, seine=(205.0, 245.0, 40.0), sidex=130.0,
    cam=dict(loc=(-30.0, -178.0, 6.0), look=(0.0, 0.0, 44.0), lens=22, shift=-0.02), samples=22,
    props=dict(
        girders=[(-6.0, 15.0, 1.4, 7.0, 6, 4), (9.0, 26.0, 0.1, 6.5, 6, 4), (-22.0, 62.0, 1.5, 7.0, 5, 4)],
        forges=[(3.5, 19.0, 0.15), (-5.0, 38.0, 0.1), (16.0, 56.0, 0.05)],
        kegs=[(-1.5, 12.0, 4), (14.0, 24.0, 5), (-14.0, 36.0, 6)],
        sheds=[(-13.0, 14.0, 0.15, 8.0, 5.0, 5.2), (-30.0, 72.0, 0.1, 9.0, 5.0, 3.4), (30.0, 80.0, -0.3, 10.0, 5.0, 3.6)],
        carts=[(8.0, 58.0, 3.0, 'girders'), (-12.0, 90.0, 0.2, 'girders')],
        workers=[(1.5, 22.0, 0.3, 'wk1'), (-4.0, 28.0, 0.5, 'wk2'), (11.0, 34.0, -0.4, 'wk3'), (2.0, 48.0, 0.2, 'wk2'), (-6.0, 70.0, 0.0, 'wk1'), (18.0, 78.0, 0.4, 'wk3'), (-1.0, 110.0, 0.0, 'wk2')],
        ladders=[(7.0, 40.0), (-18.0, 52.0)])),
 'dusk': dict(
    sky=[(0.0, '#f6a878'), (0.07, '#f0a07e'), (0.18, '#c890b4'), (0.32, '#8a78cc'), (0.52, '#5a52b8'), (0.78, '#3a3ca8'), (1.0, '#262c98')], sky_k=1.0, amb=('#2c32F0', 0.95),
    key=(1.0, 0.66, 0.4, 3.6), dbounce=0, key_dir=(0.6, 0.55, -0.1), sun_angle=1.5, exposure=0.25, sat=1.1, thick=2.2, seine=(135.0, 175.0), wire_r=0.32, hut=(-0.5, -203.0, 0.0),
    cam=dict(loc=(-8.0, -232.0, 4.5), look=(0.0, 0.0, 4.5), lens=22, shift=0.345), samples=22),
 'resto': dict(
    sky=[(0.0, '#f8dcb4'), (0.06, '#e8d8c4'), (0.2, '#b4c8f0'), (0.5, '#7a9ae6'), (1.0, '#4a68d0')], sky_k=1.0, amb=('#4a64FF', 3.0),
    key=(1.0, 0.84, 0.6, 18.0), key_dir=(0.80, 0.26, -0.42), sun_angle=1.0, exposure=0.5, sat=1.06, dbounce=2, zbase=-38.0, hero=(1.9, 0.3),
    fill=(0.92, 0.84, 0.74, 15.0, 22.0, 24.0, (0, 5, 4.9)), winfill=((0.14, 0.30, 0.78), 600.0),
    cam=dict(loc=(3.7, -5.0, 1.5), look=(-4.8, 9.0, 1.1), lens=22, shift=-0.10), samples=24),
}
NAMES = {'site': 'sb1_site', 'dusk': 'sb2_tower_dusk', 'resto': 'sb3_resto'}

def run(mode, draft=False):
    t = time.time(); bpy.ops.wm.read_factory_settings(use_empty=True); MATS.clear(); P = PRESETS[mode]; random.seed(1)
    M = palette()
    M['hwall'] = mat_windows('hwall', '#efdfba', '#e0cb9e', '#4a5882' if mode == 'site' else '#2c3460', '#ffc070', 5.0 if mode != 'site' else 0.0, 0.42 if mode == 'dusk' else 0.0)
    M['hwallt'] = mat_windows('hwallt', '#e8d4a6', '#d8c08e', '#4a5882' if mode == 'site' else '#2c3460', '#ffc070', 5.0 if mode == 'dusk' else 0.0, 0.3, (6.0, 8.0), (0.3, 0.6), 2.0)
    M['galwall'] = mat_windows('galwall', '#d0aa80', '#b8906a', '#5a3a30', '#ffc468', 4.0, 0.8, (4.0, 4.0), (0.55, 0.6), 0.5)
    bpy.context.scene.world = None
    if mode == 'site': lights = build_site(P, M)
    elif mode == 'dusk': lights = build_dusk(P, M)
    else: lights = build_resto(P, M)
    if mode == 'site': ground_plane(0.0, ('#c9895a', '#a86a44', '#8a5a3c'), 3000, 1.0, (0, 600))
    elif mode == 'dusk': ground_plane(0.0, ('#3a5a4e', '#4a6a58', '#6a6a5c'), 3000, 1.0, (0, 600))
    else: ground_plane(P['zbase'], ('#8a8a7a', '#a89a82', '#7a7a74'), 6000, 1.0, (0, 600))
    if mode != 'resto': clouds(dict(cloud=('#fff0dc', '#c8a8c8', '#e8c8d0') if mode == 'site' else ('#fcd5b1', '#8a78cc', '#ca6a9c'), cloud_k=1.0, ncloud=7 if mode == 'site' else 5, cloud_z=(160, 320) if mode == 'site' else (200, 330), cloud_scale=1.0, cloud_seed=4))
    sky_world(P); lights_setup(P, lights); setup_camera(P)
    out = os.path.join(HERE, ('d_' if draft else '') + NAMES[mode])
    render(mode, out, 14 if draft else P.get('samples', 22), draft, P); print(mode, 'done %.0fs' % (time.time() - t))

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != 'draft']; draft = 'draft' in sys.argv
    for m in (['site', 'dusk', 'resto'] if (not args or args[0] == 'all') else args): run(m, draft)

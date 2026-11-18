"""set3d14 style board: Kenyan beehive-fence smallholding. Self-contained bpy scene (procedural geometry + shaders), Cycles CPU.
usage: python3 sb.py day|night|close|all [draft]      -> sb1_day_wide.jpg / sb2_night_fence.jpg / sb3_hive_close.jpg (or d_*.jpg for draft)
World units: metres. +x right, +y away from the camera rig, z up. Camera 22 mm / 36 mm sensor (AUTO fit), 720x1280, no DOF.
Look: one hard key (sun / moon), blue-violet sky ambient (shade), flat-ish painterly materials (noise-varied two-tone), warm lamps at night."""
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

# ------------------------------------------------------------------ materials palette
def palette(mode):
    d = {}
    d['maize'] = mat('maize', '#6f9a2e', '#c2b13a', 5, contrast=1.4, zgrad=(0.0, 1.3, '#3d6a22'))
    d['stalk'] = mat('stalk', '#8f9a45', '#b8a850', 6)
    d['cob'] = mat('cob', '#e0c24a', '#9bb04a', 8)
    d['tassel'] = mat('tassel', '#d9b45a', '#e8d27a', 8)
    d['wood'] = mat('wood', '#6b3f22', '#8a5530', 6, aniso=(1, 1, 0.25), contrast=1.5)
    d['woodpale'] = mat('woodpale', '#b0763e', '#d09a58', 8, aniso=(0.3, 1, 1))
    d['hive'] = mat('hive', '#b5763a', '#d7a05a', 7, aniso=(0.4, 1, 1))
    d['tin'] = mat('tin', '#a9b3bb', '#a45f3a', 1.1, wave=(40, '#e6ecf0'), rough=0.55, sheen=0.35, contrast=1.3)
    d['tinunder'] = mat('tinunder', '#c9915f', '#d6a070', 0.8, contrast=0.4)
    d['tin2'] = mat('tin2', '#5f7e9a', '#8396a8', 1.2, wave=(30, '#b9c6cf'), rough=0.6, sheen=0.3, contrast=1.2)
    d['thatch'] = mat('thatch', '#a8803a', '#d9b660', 7, aniso=(1.6, 1.6, 0.25), contrast=1.8, zgrad=(1.8, 3.6, '#6e5026'))
    d['thatchold'] = mat('thatchold', '#8a6a3a', '#b89a58', 7, aniso=(1.6, 1.6, 0.25), contrast=1.8)
    d['mud'] = mat('mud', '#b2552f', '#c9774a', 3.5, contrast=1.3, zgrad=(0.0, 0.9, '#8c3f26'))
    d['mudpale'] = mat('mudpale', '#d9a273', '#c98b5e', 3.0)
    d['plaster'] = mat('plaster', '#4aa3a0', '#6cbdb4', 2.5)
    d['plaster2'] = mat('plaster2', '#e6c88a', '#d8b070', 2.5)
    d['dark'] = mat('dark', '#2a1c20', '#40292a', 3)
    d['door'] = mat('door', '#2e5aa0', '#3e70b8', 5, aniso=(0.3, 1, 1))
    d['jerry'] = mat('jerry', '#f2c21c', '#e4a512', 4, rough=0.45, sheen=0.3)
    d['jcap'] = mat('jcap', '#2f5a9a', '#2f5a9a')
    d['metal'] = mat('metal', '#b9c4d0', '#8e9cae', 3, rough=0.4, sheen=0.4)
    d['wire'] = mat('wire', '#f0e8d8', '#c8c0b0', 2, rough=0.3, sheen=0.5, emit='#ffd8a0', emit_k=0.25)
    d['rope'] = mat('rope', '#cfae74', '#a88650', 12)
    d['stone'] = mat('stone', '#8c8296', '#aaa0a8', 3)
    d['leafgreen'] = mat('acacia', '#6b8a2a', '#a3a43a', 2.4, contrast=1.6)
    d['trunk'] = mat('trunk', '#4a3228', '#6d4a36', 5, aniso=(1, 1, 0.3))
    d['banana'] = mat('banana', '#4fa03a', '#9cc24a', 3, contrast=1.4)
    d['grass'] = mat('grassblade', '#b39c3a', '#d4be5a', 6, zgrad=(0.0, 0.7, '#6a8a30'))
    d['goat'] = mat('goat', '#e6dcc8', '#8a5a3a', 1.5, contrast=2)
    d['hen'] = mat('hen', '#a8582e', '#e0c8a0', 4, contrast=0.8)
    d['comb'] = mat('comb', '#d8322a', '#d8322a')
    d['beak'] = mat('beak', '#e0a030', '#e0a030')
    d['bee'] = mat('bee', '#4a3414', '#b8841c', 40, contrast=2)
    d['wing'] = mat('wing', '#e8f0ff', '#e8f0ff', emit='#cfe0ff', emit_k=0.6)
    d['elephant'] = mat('elephant', '#4a5578', '#7886a8', 11, aniso=(1, 1, 2.2), contrast=2.2, rough=0.85, sheen=0.15)
    d['tusk'] = mat('tusk', '#cfc8b8', '#cfc8b8')
    d['ember'] = mat_emit('ember', '#ff7a2a', 9.0)
    d['basket'] = mat('basket', '#b88a4a', '#8a5f30', 14)
    d['char'] = mat('char', '#2a2020', '#3a2c28', 4)
    d['flame'] = mat_emit('flame', '#ff9a30', 14.0)
    d['flame2'] = mat_emit('flame2', '#ffd060', 22.0)
    d['lamp'] = mat_emit('lamp', '#ffc070', 30.0 if mode != 'day' else 2.0)
    d['winlit'] = mat_emit('winlit', '#ffb860', 14.0 if mode != 'day' else 0.0)
    if mode == 'day':
        d['winlit'] = mat('winday', '#27324a', '#3a4a66', 3)
    return d

# ------------------------------------------------------------------ props
def hut_round(mb, M, c, r=1.75, h=2.0, rt=2.45, ht=2.0, rr=None, door_yaw=0.0, thatch='thatch'):
    x, y, z = c
    mb.cone(M['mud'], (x, y, z), r, r, h, 24)
    mb.cone(M[thatch], (x, y, z + h - 0.05), rt, 0.06, ht, 28)
    mb.cone(M[thatch], (x, y, z + h - 0.12), rt + 0.05, rt - 0.15, 0.18, 28)       # shaggy eave
    mb.rod(M['wood'], (x, y, z + h + ht - 0.1), (x, y, z + h + ht + 0.35), 0.04, 0.02, 6)
    # door + low window on the yaw side
    dx, dy = -math.sin(door_yaw), math.cos(door_yaw)
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, door_yaw)).to_matrix().to_4x4())
    mb.box(M['dark'], (0, -r + 0.02, 0.85), (0.8, 0.14, 1.7))
    mb.box(M['door'], (0, -r - 0.02, 0.85), (0.04 + 0.1, 0.05, 1.5)) if False else None
    mb.box(M['wood'], (0, -r - 0.05, 1.75), (1.0, 0.12, 0.12)); mb.box(M['wood'], (-0.46, -r - 0.05, 0.85), (0.1, 0.12, 1.7)); mb.box(M['wood'], (0.46, -r - 0.05, 0.85), (0.1, 0.12, 1.7))
    mb.pop()

def house_tin(mb, M, c, sx=7.0, sy=4.0, h=2.7, yaw=0.0, roof='tin', walls='plaster'):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M[walls], (0, 0, h / 2), (sx, sy, h))
    mb.box(M['stone'], (0, 0, 0.15), (sx + 0.1, sy + 0.1, 0.3))
    # gable roof: ridge along x
    ov = 0.7; rh = 1.35
    hw = sy / 2 + ov; x0 = -sx / 2 - ov; x1 = sx / 2 + ov
    for sgn in (-1, 1):
        mb.quad(M[roof], [(x0, sgn * hw, h - 0.25), (x1, sgn * hw, h - 0.25), (x1, 0, h + rh), (x0, 0, h + rh)] if sgn > 0 else
                [(x0, 0, h + rh), (x1, 0, h + rh), (x1, sgn * hw, h - 0.25), (x0, sgn * hw, h - 0.25)])
        # thickness lip
        mb.quad(M[roof], [(x0, sgn * hw, h - 0.25), (x1, sgn * hw, h - 0.25), (x1, sgn * hw, h - 0.33), (x0, sgn * hw, h - 0.33)])
    # gable ends
    for ex in (-sx / 2, sx / 2):
        mb.tri(M[walls], [(ex, -sy / 2, h), (ex, sy / 2, h), (ex, 0, h + rh - 0.25)])
    mb.box(M['wood'], (0, 0, h + rh), (sx + 1.5, 0.12, 0.1))
    # front (-y) door and windows
    mb.box(M['door'], (-1.3, -sy / 2 - 0.03, 1.1), (1.0, 0.08, 2.1)); mb.box(M['dark'], (-1.3, -sy / 2 - 0.08, 1.1), (0.8, 0.04, 1.9))
    for wx in (0.6, 2.2):
        mb.box(M['door'], (wx, -sy / 2 - 0.03, 1.5), (0.9, 0.08, 0.9)); mb.box(M['winlit'], (wx, -sy / 2 - 0.08, 1.5), (0.74, 0.04, 0.74))
    mb.box(M['stone'], (-1.3, -sy / 2 - 0.7, 0.1), (1.4, 0.8, 0.2))
    mb.pop()

def granary(mb, M, c):
    x, y, z = c
    for dx in (-0.7, 0.7):
        for dy in (-0.7, 0.7): mb.rod(M['wood'], (x + dx, y + dy, z), (x + dx, y + dy, z + 0.9), 0.09, 0.08, 6)
    mb.cone(M['thatchold'], (x, y, z + 0.9), 1.15, 1.0, 0.25, 16)
    mb.cone(M['mud'], (x, y, z + 1.1), 1.1, 1.0, 1.4, 20)
    mb.cone(M['thatch'], (x, y, z + 2.45), 1.5, 0.05, 1.3, 20)
    mb.box(M['dark'], (x, y - 1.0, z + 1.6), (0.4, 0.1, 0.45))

def acacia(mb, M, c, s=1.0, seed=0, yaw=0.0):
    rr = rnd(seed); x, y, z = c
    top = Vector((x, y, z + 5.2 * s))
    lean = Vector((rr.uniform(-0.6, 0.6), rr.uniform(-0.6, 0.6), 0)) * s
    mid = Vector((x, y, z + 2.4 * s)) + lean * 0.4
    mb.rod(M['trunk'], (x, y, z - 0.1), mid, 0.34 * s, 0.24 * s, 8, smooth=True)
    tops = []
    for i in range(3):
        a = yaw + i * 2.1 + rr.uniform(-.3, .3); tp = top + Vector((math.cos(a) * 1.6 * s, math.sin(a) * 1.6 * s, rr.uniform(-.5, .3) * s)) + lean
        mb.rod(M['trunk'], mid, tp, 0.2 * s, 0.1 * s, 7, smooth=True); tops.append(tp)
    for tp in tops + [top + lean]:
        for j in range(3):
            o = Vector((rr.uniform(-1.6, 1.6), rr.uniform(-1.6, 1.6), rr.uniform(0.0, 0.35))) * s
            mb.ell(M['leafgreen'], tp + o + Vector((0, 0, 0.35 * s)), (rr.uniform(1.7, 2.6) * s, rr.uniform(1.7, 2.6) * s, 0.42 * s), (14, 8), (0, 0, rr.random() * 6))

def banana(mb, M, c, seed=0, s=1.0):
    rr = rnd(seed); x, y, z = c
    for k in range(rr.randint(2, 4)):
        px = x + rr.uniform(-0.6, 0.6); py = y + rr.uniform(-0.6, 0.6); hh = rr.uniform(2.0, 3.0) * s
        mb.rod(M['banana'], (px, py, z), (px, py, z + hh), 0.17 * s, 0.1 * s, 8, smooth=True)
        for i in range(7):
            a = rr.random() * 6.283; Lf = rr.uniform(1.6, 2.3) * s; wd = 0.34 * s
            dirv = Vector((math.cos(a), math.sin(a), 0)); side = Vector((-dirv.y, dirv.x, 0))
            pts = []
            for t in range(6):
                u = t / 5.0; p = Vector((px, py, z + hh)) + dirv * (u * Lf) + Vector((0, 0, 0.55 * s * math.sin(u * 2.2) - 0.95 * s * u * u))
                pts.append((p, wd * math.sin(math.pi * min(1, u * 1.1 + 0.08))))
            for t in range(5):
                (p0, w0), (p1, w1) = pts[t], pts[t + 1]
                mb.quad(M['banana'], [p0 - side * w0, p0 + side * w0, p1 + side * w1, p1 - side * w1])
        mb.ell(M['stalk'], (px + 0.3, py, z + hh - 0.5), (0.1, 0.1, 0.22), (6, 4))

def jerrycan(mb, M, c, yaw=0.0):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M['jerry'], (0, 0, 0.26), (0.34, 0.18, 0.5)); mb.box(M['jerry'], (-0.06, 0, 0.56), (0.18, 0.12, 0.1)); mb.box(M['jcap'], (0.1, 0, 0.55), (0.07, 0.07, 0.07))
    mb.box(M['dark'], (-0.06, 0, 0.56), (0.08, 0.14, 0.04))
    mb.pop()

def hoe(mb, M, c, yaw=0.0):
    x, y, z = c
    mb.rod(M['woodpale'], (x, y, z + 0.05), (x + math.cos(yaw) * 1.0, y + math.sin(yaw) * 1.0, z + 1.3), 0.025, 0.022, 6)
    ex, ey = x + math.cos(yaw) * 1.0, y + math.sin(yaw) * 1.0
    mb.box(M['metal'], (ex, ey, z + 1.3), (0.2, 0.07, 0.14), rz=yaw + 0.3, ry=0.3)

def chicken(mb, M, c, yaw=0.0, s=1.0):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Diagonal((s, s, s, 1)))
    mb.ell(M['hen'], (0, 0, 0.26), (0.2, 0.13, 0.14), (10, 6)); mb.ell(M['hen'], (0.17, 0, 0.42), (0.07, 0.06, 0.1), (8, 5))
    mb.ell(M['comb'], (0.19, 0, 0.53), (0.03, 0.015, 0.04), (6, 4)); mb.tri(M['beak'], [(0.24, 0.02, 0.42), (0.24, -0.02, 0.42), (0.31, 0, 0.4)])
    mb.quad(M['hen'], [(-0.18, -0.05, 0.3), (-0.18, 0.05, 0.3), (-0.34, 0, 0.5), (-0.3, 0, 0.36)])
    for sy in (-0.05, 0.05): mb.rod(M['beak'], (0, sy, 0.15), (0.02, sy, 0.0), 0.012, 0.012, 4)
    mb.pop()

def stool(mb, M, c, yaw=0.0):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M['woodpale'], (0, 0, 0.42), (0.42, 0.42, 0.07))
    for dx, dy in ((-0.15, -0.15), (0.15, -0.15), (-0.15, 0.15), (0.15, 0.15)): mb.rod(M['wood'], (dx, dy, 0.0), (dx * 1.1, dy * 1.1, 0.4), 0.035, 0.03, 6)
    mb.pop()

def basket(mb, M, c):
    x, y, z = c
    mb.rod(M['basket'], (x, y, z), (x, y, z + 0.42), 0.26, 0.36, 14)
    mb.ell(M['basket'], (x, y, z + 0.42), (0.37, 0.37, 0.05), (14, 4))
    rr = rnd(4)
    for i in range(16):
        a = rr.random() * 6.283; r = rr.random() * 0.24
        mb.ell(M['cob'], (x + math.cos(a) * r, y + math.sin(a) * r, z + 0.5 + rr.random() * 0.1), (0.13, 0.05, 0.05), (8, 5), (0, rr.random() * 0.5, rr.random() * 6.28))

def goat(mb, M, c, yaw=0.0, s=1.0):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Diagonal((s, s, s, 1)))
    mb.ell(M['goat'], (0, 0, 0.62), (0.5, 0.2, 0.22), (12, 8)); mb.ell(M['goat'], (0.55, 0, 0.85), (0.14, 0.1, 0.12), (8, 6)); mb.rod(M['goat'], (0.4, 0, 0.7), (0.52, 0, 0.82), 0.09, 0.07, 6)
    for sx in (-0.34, 0.34):
        for sy in (-0.1, 0.1): mb.rod(M['goat'], (sx, sy, 0.5), (sx, sy, 0.02), 0.04, 0.025, 6)
    for sy in (-0.05, 0.05): mb.rod(M['dark'], (0.58, sy, 0.94), (0.5, sy * 2.4, 1.1), 0.02, 0.008, 5)
    mb.rod(M['goat'], (-0.48, 0, 0.7), (-0.58, 0, 0.82), 0.03, 0.02, 5)
    mb.pop()

def firepit(mb, M, c, night):
    x, y, z = c
    for i in range(9):
        a = i / 9 * 6.283; mb.ell(M['stone'], (x + math.cos(a) * 0.6, y + math.sin(a) * 0.6, z + 0.1), (0.2, 0.16, 0.14), (8, 5), (0, 0, a))
    for i in range(4):
        a = i * 1.57 + 0.4; mb.rod(M['char'], (x + math.cos(a) * 0.5, y + math.sin(a) * 0.5, z + 0.18), (x, y, z + 0.3), 0.06, 0.05, 6)
    mb.cone(M['flame'], (x, y, z + 0.15), 0.28, 0.02, 0.8, 8); mb.cone(M['flame2'], (x, y, z + 0.15), 0.15, 0.01, 0.5, 8)

def grass_clump(mb, M, c, rr, h=0.9):
    x, y, z = c
    for i in range(7):
        a = rr.random() * 6.283; L = h * rr.uniform(0.6, 1.2); bend = rr.uniform(0.15, 0.5)
        d = Vector((math.cos(a), math.sin(a), 0)); sd = Vector((-d.y, d.x, 0)) * 0.025
        p0 = Vector((x + rr.uniform(-.08, .08), y + rr.uniform(-.08, .08), z)); p1 = p0 + d * bend * 0.4 + Vector((0, 0, L * 0.6)); p2 = p0 + d * bend + Vector((0, 0, L))
        mb.quad(M['grass'], [p0 - sd * 1.4, p0 + sd * 1.4, p1 + sd * 0.8, p1 - sd * 0.8]); mb.tri(M['grass'], [p1 - sd * 0.8, p1 + sd * 0.8, p2])

# ------------------------------------------------------------------ maize
def maize_variant(M, seed):
    rr = rnd(seed); mb = MB('mz%d' % seed); hgt = R(2.1, 2.5, rr)
    mb.rod(M['stalk'], (0, 0, 0), (0, 0, hgt), 0.035, 0.02, 6)
    nl = 9
    for i in range(nl):
        zb = 0.35 + (hgt - 0.7) * i / (nl - 1); a = i * 2.4 + rr.random() * 0.8; Lf = R(0.95, 1.25, rr) * (1.0 - 0.25 * i / nl); wd = 0.085
        d = Vector((math.cos(a), math.sin(a), 0)); sd = Vector((-d.y, d.x, 0))
        pts = []
        for t in range(7):
            u = t / 6.0; p = Vector((0, 0, zb)) + d * (u * Lf * 0.85) + Vector((0, 0, 0.45 * math.sin(u * 2.0) - 0.7 * u * u * Lf * 0.7))
            wv = wd * (0.5 + math.sin(math.pi * min(1, u * 0.95 + 0.05)))
            pts.append((p, wv))
        for t in range(6):
            (p0, w0), (p1, w1) = pts[t], pts[t + 1]
            mb.quad(M['maize'], [p0 - sd * w0, p0 + sd * w0, p1 + sd * w1, p1 - sd * w1])
    for k in range(2):
        a = k * 3.1 + rr.random(); mb.ell(M['cob'], (math.cos(a) * 0.09, math.sin(a) * 0.09, 1.25 + 0.2 * k), (0.045, 0.045, 0.17), (6, 4))
    for i in range(6):
        a = i * 1.05; mb.rod(M['tassel'], (0, 0, hgt - 0.05), (math.cos(a) * 0.22, math.sin(a) * 0.22, hgt + 0.3), 0.012, 0.004, 4)
    return mb.finish()

# ------------------------------------------------------------------ hives + fence
HIVE_X = [-10.0, -4.0, 2.0, 8.0]
WIRE_Z = 2.0
def post(mb, M, x, y, h=2.5, seed=0):
    rr = rnd(int(x * 31 + y * 17 + seed)); lean = rr.uniform(-0.04, 0.04)
    mb.rod(M['wood'], (x, y, -0.1), (x + lean * h, y, h), 0.07, 0.06, 6, smooth=True)

def hive_unit(mb, M, x, y, swing=0.0, along='x'):
    """Two posts 2.0 apart, crossbeam, pitched tin roof, hive hanging by two ropes from the wire (top-bar hive: trapezoid long box, thatch edge)."""
    for dx in (-1.0, 1.0): post(mb, M, x + dx, y, 2.55)
    mb.box(M['wood'], (x, y, 2.42), (2.3, 0.1, 0.1))
    # little pitched tin roof (ridge along x), overhang
    rw = 0.95; rh = 0.34; x0, x1 = x - 1.35, x + 1.35
    for sgn in (-1, 1):
        q = [(x0, y + sgn * rw, 2.48), (x1, y + sgn * rw, 2.48), (x1, y, 2.48 + rh), (x0, y, 2.48 + rh)]
        mb.quad(M['tin'], q if sgn > 0 else q[::-1])
        qu = [(a, b, c - 0.025) for (a, b, c) in q]; mb.quad(M['tinunder'], qu[::-1] if sgn > 0 else qu)
        mb.quad(M['tin'], [(x0, y + sgn * rw, 2.48), (x1, y + sgn * rw, 2.48), (x1, y + sgn * rw, 2.43), (x0, y + sgn * rw, 2.43)])
    for ex in (x0, x1): mb.tri(M['tin'], [(ex, y - rw, 2.48), (ex, y + rw, 2.48), (ex, y, 2.48 + rh)])
    mb.box(M['thatchold'], (x, y, 2.5 + rh), (2.8, 0.12, 0.07))
    # hive
    hz = 1.35 + swing * 0.0
    mb.push(Matrix.Translation((x, y, hz)))
    L, Wd, Hh = 1.25, 0.42, 0.34
    vt = [(-L / 2, -Wd / 2, Hh / 2), (L / 2, -Wd / 2, Hh / 2), (L / 2, Wd / 2, Hh / 2), (-L / 2, Wd / 2, Hh / 2)]
    vb = [(-L / 2 + 0.03, -Wd * 0.18, -Hh / 2), (L / 2 - 0.03, -Wd * 0.18, -Hh / 2), (L / 2 - 0.03, Wd * 0.18, -Hh / 2), (-L / 2 + 0.03, Wd * 0.18, -Hh / 2)]
    mb.quad(M['hive'], vt[::-1]); mb.quad(M['hive'], vb)
    for i in range(4):
        j = (i + 1) % 4; mb.quad(M['hive'], [vb[i], vb[j], vt[j], vt[i]])
    # top bars + gap line
    for i in range(10): mb.box(M['woodpale'], (-L / 2 + 0.07 + i * 0.12, 0, Hh / 2 + 0.012), (0.115, Wd + 0.04, 0.025))
    # entrance slots on the +x end (dark) + landing board
    for dz in (0.03, -0.05):
        mb.box(M['dark'], (L / 2 + 0.003, 0.0, dz), (0.012, 0.15, 0.03))
    mb.box(M['woodpale'], (L / 2 + 0.05, 0, -0.1), (0.1, 0.3, 0.025))
    for dz in (0.03, -0.05): mb.box(M['dark'], (-L / 2 - 0.003, 0.0, dz), (0.012, 0.15, 0.03))
    mb.box(M['woodpale'], (-L / 2 - 0.05, 0, -0.1), (0.1, 0.3, 0.025))
    mb.pop()
    # ropes up to the wire
    for sx in (-0.45, 0.45):
        mb.rod(M['rope'], (x + sx, y, hz + 0.17), (x + sx * 0.4, y, WIRE_Z), 0.016, 0.016, 5)
    mb.box(M['metal'], (x, y, WIRE_Z), (0.1, 0.07, 0.07))

def wire_line(mb, M, pts, sag=0.12, step=0.6, r=0.02):
    """pts: list of (x,y) posts; wire at WIRE_Z with a catenary-ish sag between each pair."""
    for (a, b) in zip(pts[:-1], pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1]); n = max(2, int(L / step)); prev = None
        for i in range(n + 1):
            u = i / n; p = (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, WIRE_Z - sag * 4 * u * (1 - u) * (L / 6.0))
            if prev: mb.rod(M['wire'], prev, p, r, r, 4, caps=False)
            prev = p

# ------------------------------------------------------------------ ground / sky / hills
def ground(mode, extent=130):
    # mask: R=path, G=field soil; covers x -60..60, y -40..80  (1024 x 1024)
    S = 1024; x0, x1, y0, y1 = -60.0, 60.0, -40.0, 80.0
    im = Image.new('RGB', (S, S), (0, 0, 0)); d = ImageDraw.Draw(im)
    def px(x, y): return ((x - x0) / (x1 - x0) * S, (1 - (y - y0) / (y1 - y0)) * S)
    def line(pts, w, col=(255, 0, 0)): d.line([px(*p) for p in pts], fill=col, width=int(w / (x1 - x0) * S), joint='curve')
    def disc(c, r, col=(255, 0, 0)): a = px(c[0] - r, c[1] + r); b = px(c[0] + r, c[1] - r); d.ellipse([a, b], fill=col)
    line([(-60, -3), (-30, -2.5), (0, -3.2), (30, -2.2), (60, -3)], 4.0)
    line([(-14, 2.6), (14, 2.6)], 2.0)
    line([(3.6, -9), (3.4, -4), (2.2, 1), (0.6, 5)], 2.6)
    line([(2.95, -9), (2.75, -4), (1.6, 1), (0.0, 5)], 0.28, (255, 0, 255)); line([(4.25, -9), (4.05, -4), (2.8, 1), (1.2, 5)], 0.28, (255, 0, 255))
    line([(15, -3), (15.5, 5), (17, 12), (19, 18)], 2.2)
    line([(15.5, 6), (30, 8), (40, 6)], 1.6)
    line([(10.8, 3), (10.8, 24)], 1.4); line([(-14.8, 3), (-14.8, 24)], 1.2)
    disc((20, 14), 7.5); disc((29, 10), 4); disc((22, 21), 4)
    d.rectangle([px(-13.2, 25.5), px(10.2, 4.5)], fill=(0, 255, 0))
    im = im.filter(ImageFilter.GaussianBlur(2)); p = os.path.join(HERE, 'mask_ground.png'); im.save(p)
    img = bpy.data.images.load(p); img.colorspace_settings.name = 'Non-Color'
    me = bpy.data.meshes.new('ground'); bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=2, y_segments=2, size=extent); bm.to_mesh(me)
    ob = bpy.data.objects.new('ground', me); ob.location = (0, 60, 0); bpy.context.scene.collection.objects.link(ob)
    m = bpy.data.materials.new('ground'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); bs.inputs['Roughness'].default_value = 1.0; bs.inputs['Specular IOR Level'].default_value = 0.0
    tc = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping'); L(tc.outputs['Object'], mp.inputs[0])
    nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.1; nz.inputs['Detail'].default_value = 6; L(mp.outputs[0], nz.inputs[0])
    nz2 = N('ShaderNodeTexNoise'); nz2.inputs['Scale'].default_value = 7; nz2.inputs['Detail'].default_value = 5; L(mp.outputs[0], nz2.inputs[0])
    # mask uv from world xy
    ow = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); L(ow.outputs['Object'], sp.inputs[0])
    # object coords are relative to (0,60,0): world = obj + (0,60,0)
    mx_ = N('ShaderNodeMath'); mx_.operation = 'MULTIPLY_ADD'; L(sp.outputs['X'], mx_.inputs[0]); mx_.inputs[1].default_value = 1 / (x1 - x0); mx_.inputs[2].default_value = (0 - x0) / (x1 - x0)
    my_ = N('ShaderNodeMath'); my_.operation = 'MULTIPLY_ADD'; L(sp.outputs['Y'], my_.inputs[0]); my_.inputs[1].default_value = 1 / (y1 - y0); my_.inputs[2].default_value = (60 - y0) / (y1 - y0)
    cu = N('ShaderNodeCombineXYZ'); L(mx_.outputs[0], cu.inputs['X']); L(my_.outputs[0], cu.inputs['Y'])
    # warp the mask coordinates with noise for ragged edges
    wp = N('ShaderNodeVectorMath'); wp.operation = 'ADD'; L(cu.outputs[0], wp.inputs[0])
    wn = N('ShaderNodeTexNoise'); wn.inputs['Scale'].default_value = 25; wn.inputs['Detail'].default_value = 3; L(mp.outputs[0], wn.inputs[0])
    sc = N('ShaderNodeVectorMath'); sc.operation = 'SCALE'; sc.inputs['Scale'].default_value = 0.012; L(wn.outputs['Color'], sc.inputs[0]); L(sc.outputs[0], wp.inputs[1])
    ti = N('ShaderNodeTexImage'); ti.image = img; ti.extension = 'EXTEND'; ti.interpolation = 'Linear'; L(wp.outputs[0], ti.inputs['Vector'])
    sm = N('ShaderNodeSeparateColor'); L(ti.outputs['Color'], sm.inputs[0])
    def mixc(a, b, fac, A, B):
        x = N('ShaderNodeMix'); x.data_type = 'RGBA'
        if A is not None: x.inputs[6].default_value = hexc(A)
        if B is not None: x.inputs[7].default_value = hexc(B)
        if fac is not None: L(fac, x.inputs[0])
        return x
    ramp = N('ShaderNodeValToRGB'); L(nz.outputs['Fac'], ramp.inputs[0]); ramp.color_ramp.elements[0].position = 0.35; ramp.color_ramp.elements[1].position = 0.65
    grass = mixc(None, None, ramp.outputs[0], '#8a9436', '#c9ad52')
    ramp2 = N('ShaderNodeValToRGB'); L(nz2.outputs['Fac'], ramp2.inputs[0]); ramp2.color_ramp.elements[0].position = 0.4; ramp2.color_ramp.elements[1].position = 0.6
    redd = mixc(None, None, ramp2.outputs[0], '#b0583a', '#c97a4a')
    soil = mixc(None, None, ramp2.outputs[0], '#8f4a2c', '#a85a34')
    m1 = N('ShaderNodeMix'); m1.data_type = 'RGBA'; L(grass.outputs[2], m1.inputs[6]); L(soil.outputs[2], m1.inputs[7]); L(sm.outputs['Green'], m1.inputs[0])
    m2 = N('ShaderNodeMix'); m2.data_type = 'RGBA'; L(m1.outputs[2], m2.inputs[6]); L(redd.outputs[2], m2.inputs[7]); L(sm.outputs['Red'], m2.inputs[0])
    rb = N('ShaderNodeMath'); rb.operation = 'MULTIPLY'; rb.inputs[1].default_value = 0.75; L(sm.outputs['Blue'], rb.inputs[0])
    m3 = N('ShaderNodeMix'); m3.data_type = 'RGBA'; m3.blend_type = 'MULTIPLY'; L(m2.outputs[2], m3.inputs[6]); m3.inputs[7].default_value = (0.3, 0.25, 0.24, 1); L(rb.outputs[0], m3.inputs[0])
    nz3 = N('ShaderNodeTexNoise'); nz3.inputs['Scale'].default_value = 55; nz3.inputs['Detail'].default_value = 8; L(mp.outputs[0], nz3.inputs[0])
    r3 = N('ShaderNodeValToRGB'); L(nz3.outputs['Fac'], r3.inputs[0]); r3.color_ramp.elements[0].position = 0.35; r3.color_ramp.elements[0].color = (0.72, 0.72, 0.72, 1); r3.color_ramp.elements[1].position = 0.65; r3.color_ramp.elements[1].color = (1.12, 1.12, 1.12, 1)
    m4 = N('ShaderNodeMix'); m4.data_type = 'RGBA'; m4.blend_type = 'MULTIPLY'; m4.inputs[0].default_value = 0.8; L(m3.outputs[2], m4.inputs[6]); L(r3.outputs[0], m4.inputs[7])
    L(m4.outputs[2], bs.inputs['Base Color']); L(bs.outputs[0], out.inputs['Surface']); ob.data.materials.append(m)

def sky(mode, P):
    w = bpy.data.worlds.new('sky'); bpy.context.scene.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputWorld'); bg = N('ShaderNodeBackground'); tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Generated'], sp.inputs[0])
    cr = N('ShaderNodeValToRGB'); L(sp.outputs['Z'], cr.inputs[0])
    # Generated for worlds is the direction mapped to 0..1 (z = 0.5 + dir.z/2)
    stops = P['sky']
    cr.color_ramp.elements[0].position = stops[0][0]; cr.color_ramp.elements[0].color = hexc(stops[0][1])
    for pos, col in stops[1:-1]:
        e = cr.color_ramp.elements.new(pos); e.color = hexc(col)
    cr.color_ramp.elements[-1].position = stops[-1][0]; cr.color_ramp.elements[-1].color = hexc(stops[-1][1])
    bg.inputs['Strength'].default_value = P['sky_k']; L(cr.outputs[0], bg.inputs['Color'])
    if P.get('stars'):
        vo = N('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = 260; vo.feature = 'F1'; L(tc.outputs['Generated'], vo.inputs[0])
        sr = N('ShaderNodeValToRGB'); sr.color_ramp.elements[0].position = 0.0; sr.color_ramp.elements[1].position = 0.035; sr.color_ramp.elements[0].color = (1, 1, 1, 1); sr.color_ramp.elements[1].color = (0, 0, 0, 1)
        L(vo.outputs['Distance'], sr.inputs[0])
        zm = N('ShaderNodeMapRange'); L(sp.outputs['Z'], zm.inputs['Value']); zm.inputs['From Min'].default_value = 0.6; zm.inputs['From Max'].default_value = 0.8
        mu = N('ShaderNodeMath'); mu.operation = 'MULTIPLY'; L(sr.outputs[0], mu.inputs[0]); L(zm.outputs['Result'], mu.inputs[1])
        ma = N('ShaderNodeMath'); ma.operation = 'MULTIPLY'; ma.inputs[1].default_value = 9.0; L(mu.outputs[0], ma.inputs[0])
        ad = N('ShaderNodeMix'); ad.data_type = 'RGBA'; ad.blend_type = 'ADD'; L(cr.outputs[0], ad.inputs[6]); ad.inputs[7].default_value = (0.8, 0.9, 1.0, 1); L(ma.outputs[0], ad.inputs[0])
        L(ad.outputs[2], bg.inputs['Color'])
    L(bg.outputs[0], out.inputs['Surface'])

def hills(mode, P):
    """Far ridges + one big blue mountain, emission-only flat colours (atmospheric perspective) so they never get shadows."""
    mb = MB('hills')
    rr = rnd(3)
    layers = P['hills']      # (y, base_h, amp, colour hex)
    for li, (yy, bh, amp, col) in enumerate(layers):
        m = mat_emit('hill%d_%s' % (li, mode), col, P['hill_k'])
        n = 120; xs = np.linspace(-420, 420, n); ph = [rr.uniform(0, 6) for _ in range(4)]
        hs = [bh + amp * (0.5 * math.sin(x / 55 + ph[0]) + 0.3 * math.sin(x / 23 + ph[1]) + 0.15 * math.sin(x / 9 + ph[2])) for x in xs]
        for i in range(n - 1):
            mb.quad(m, [(xs[i], yy, -5), (xs[i + 1], yy, -5), (xs[i + 1], yy, hs[i + 1]), (xs[i], yy, hs[i])])
    # mountain (Mt Kenya-like) behind the ridges
    m = mat_emit('mount_%s' % mode, P['mount'], P['hill_k'])
    cx = P.get('mount_x', 60); base = 230; hp = 90
    prof = [(-190, 0), (-110, 22), (-60, 52), (-26, 78), (-10, 92), (0, 98), (10, 90), (28, 74), (62, 50), (110, 24), (190, 0)]
    for (a, b) in zip(prof[:-1], prof[1:]):
        mb.quad(m, [(cx + a[0], base, -5), (cx + b[0], base, -5), (cx + b[0], base, b[1]), (cx + a[0], base, a[1])])
    # snow-ish cap, warm lit (emission)
    ms = mat_emit('cap_%s' % mode, P['cap'], P['hill_k'])
    mb.quad(ms, [(cx - 11, base - 1, 86), (cx + 11, base - 1, 84), (cx + 2, base - 1, 97.5), (cx - 3, base - 1, 97)])
    mb.finish()

# ------------------------------------------------------------------ elephant stand-in (rough low-poly, dark silhouette)
def elephant(mb, M, c, yaw, s=1.0):
    """Stand-in: smooth overlapping ellipsoids, tapered legs, curved trunk, tusks, big ears. Local +x is forward."""
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Diagonal((s, s, s, 1)))
    E = M['elephant']; sg = (24, 16)
    mb.ell(E, (0.0, 0, 2.25), (1.95, 1.1, 1.2), sg); mb.ell(E, (-1.1, 0, 2.4), (1.0, 1.0, 1.12), sg); mb.ell(E, (1.05, 0, 2.45), (1.0, 0.95, 1.1), sg)
    mb.ell(E, (1.7, 0, 2.5), (0.5, 0.6, 0.85), sg)                                                              # neck / shoulders
    mb.ell(E, (2.25, 0, 2.62), (0.72, 0.64, 0.78), sg)                                                          # head
    mb.ell(E, (2.7, 0, 2.95), (0.35, 0.4, 0.3), (14, 10))                                                       # forehead dome
    for sy in (-1, 1):
        mb.ell(E, (1.85, sy * 0.78, 2.78), (0.12, 0.62, 0.78), (16, 12), (0.0, 0.0, sy * 0.5))                  # ears (spread, flat)
        mb.ell(E, (1.55, sy * 1.12, 2.62), (0.1, 0.46, 0.62), (14, 10), (0.0, 0.0, sy * 0.7))
    pts = [(2.75, 0, 2.45), (3.15, 0, 1.95), (3.4, 0, 1.3), (3.45, 0, 0.7), (3.3, 0, 0.35), (3.1, 0, 0.3)]
    for i in range(len(pts) - 1): mb.rod(E, pts[i], pts[i + 1], 0.27 - 0.035 * i, 0.27 - 0.035 * (i + 1), 12, smooth=True)   # trunk
    for p in pts[1:4]: mb.ell(E, p, (0.28, 0.28, 0.28), (10, 8))
    for sy in (-1, 1): mb.rod(M['tusk'], (2.7, sy * 0.38, 2.15), (3.65, sy * 0.5, 1.7), 0.11, 0.015, 10, smooth=True)   # tusks
    for lx in (-1.15, 1.25):
        for sy in (-0.58, 0.58):
            mb.rod(E, (lx, sy, 2.1), (lx, sy, 0.15), 0.46, 0.36, 14, smooth=True); mb.ell(E, (lx, sy, 0.12), (0.4, 0.4, 0.14), (12, 8))
    mb.rod(E, (-2.0, 0, 2.7), (-2.3, 0, 1.3), 0.11, 0.05, 8, smooth=True); mb.ell(E, (-2.3, 0, 1.25), (0.08, 0.08, 0.16), (6, 4))
    mb.pop()

# ------------------------------------------------------------------ the whole set
def build(mode):
    sc = bpy.context.scene; mode_ = mode
    for o in list(bpy.data.objects): bpy.data.objects.remove(o)
    MATS.clear()
    P = PRESETS[mode]; M = palette('night' if mode == 'night' else 'day')
    sky(mode, P); hills(mode, P); ground(mode)
    # --- maize field: 25 rows (x) x 45 plants (y), 4 shared variants
    vars_ = [maize_variant(M, 100 + i) for i in range(4)]
    rr = rnd(7); n = 0
    for ix in range(-12, 9):
        for iy in range(0, 42):
            x = -12.2 + (ix + 12) * 0.95 + rr.uniform(-0.1, 0.1); y = 5.9 + iy * 0.44 + rr.uniform(-0.08, 0.08)
            if y > 24.4: continue
            v = vars_[rr.randrange(4)]
            for src in v:
                ob = bpy.data.objects.new('mz', src.data); ob.location = (x, y, 0); ob.rotation_euler = (0, 0, rr.random() * 6.283); s = rr.uniform(0.85, 1.15); ob.scale = (s, s, s * rr.uniform(0.92, 1.1))
                sc.collection.objects.link(ob)
            n += 1
    # --- fence
    mb = MB('fence')
    front = [(-14.0, 5.0)]
    for x in HIVE_X: front += [(x - 1, 5.0), (x + 1, 5.0)]
    front += [(10.8, 5.0)]
    # intermediate posts between units
    for x in (-13.0, -7.0, -1.0, 5.0, 10.8): post(mb, M, x, 5.0, 2.5)
    for y in (11.0, 17.0, 24.0): post(mb, M, 10.8, y, 2.5)
    for y in (11.0, 17.0, 24.0): post(mb, M, -14.0, y, 2.5)
    pts = [(-14.0, 5.0), (-13.0, 5.0)]
    for x in HIVE_X: pts += [(x - 1, 5.0), (x + 1, 5.0)]
    pts += [(10.8, 5.0)]
    ps = sorted(set(pts) | {(-7.0, 5.0), (-1.0, 5.0), (5.0, 5.0)})
    # wire points: one polyline; sag only on long spans
    wire_line(mb, M, ps, sag=0.07)
    wire_line(mb, M, [(10.8, 5.0), (10.8, 11.0), (10.8, 17.0), (10.8, 24.0)], sag=0.1)
    wire_line(mb, M, [(-14.0, 5.0), (-14.0, 11.0), (-14.0, 17.0), (-14.0, 24.0)], sag=0.1)
    for x in HIVE_X: hive_unit(mb, M, x, 5.0)
    hive_unit(mb, M, 10.8, 14.0); hive_unit(mb, M, -14.0, 14.0)
    # --- farmstead (right side, x 14..32): huts, house, granary, fire pit, props
    hut_round(mb, M, (20.0, 14.0, 0.0), door_yaw=0.35)
    hut_round(mb, M, (28.5, 11.5, 0.0), r=1.5, rt=2.15, ht=1.8, door_yaw=-0.4)
    hut_round(mb, M, (22.5, 22.0, 0.0), r=1.6, rt=2.3, ht=1.9, door_yaw=0.2, thatch='thatchold')
    house_tin(mb, M, (31.0, 21.0, 0.0), 7.0, 4.2, 2.7, yaw=-0.12)
    granary(mb, M, (15.5, 19.5, 0.0))
    firepit(mb, M, (24.0, 8.5, 0.0), mode == 'night')
    for dx in (-1.0, 1.0): mb.rod(M['wood'], (24.0 + dx, 8.9, 0.0), (24.0 + dx, 8.9, 1.2), 0.04, 0.04, 5)
    mb.ell(M['metal'], (24.0, 8.9, 1.15), (0.28, 0.2, 0.2), (10, 6))
    for (x, y, yw) in [(17.0, 8.0, 0.2), (17.35, 8.1, 1.0), (16.8, 8.45, 2.0)]: jerrycan(mb, M, (x, y, 0.0), yw)
    if mode == 'day':
        for (x, y, yw) in [(-6.6, 0.4, 0.7), (-6.2, 0.75, 1.3), (-6.55, 0.05, 2.2), (-6.3, 0.2, 0.2)]: jerrycan(mb, M, (x, y, 0.0), yw)
        hoe(mb, M, (-7.4, 1.9, 0.0), 0.6)
        stool(mb, M, (-5.0, 1.4, 0.0)); stool(mb, M, (-4.4, 0.9, 0.0), 0.5)
        basket(mb, M, (-7.9, 0.8, 0.0))
        for i, (x, y) in enumerate([(-4.2, 0.1), (-8.3, 1.2), (-3.4, 1.6), (-5.6, -0.6), (-7.3, -0.4)]): chicken(mb, M, (x, y, 0.0), i * 1.9, 1.15)
        goat(mb, M, (-2.0, 0.6, 0.0), 0.5, 1.3)
    mb.box(M['woodpale'], (18.5, 10.4, 0.2), (0.9, 0.35, 0.4)); mb.box(M['woodpale'], (21.5, 9.4, 0.2), (0.35, 0.8, 0.4))   # stools / bench
    for i, (x, y) in enumerate([(14.3, 4.5), (23.0, 5.0)]): chicken(mb, M, (x, y, 0.0), i * 1.7, 1.15)
    goat(mb, M, (28.0, 5.5, 0.0), 2.4, 0.9)
    mb.finish()
    mb = MB('trees')
    acacia(mb, M, (-20.0, 20.0, 0.0), 1.5, 1, 0.3); acacia(mb, M, (35.0, 5.0, 0.0), 1.3, 2, 1.1); acacia(mb, M, (-33.0, 6.0, 0.0), 1.1, 3, 2.1); acacia(mb, M, (0.0, 44.0, 0.0), 1.7, 4, 0.5)
    acacia(mb, M, (-6.0, 60.0, 0.0), 1.4, 5, 1.5); acacia(mb, M, (26.0, 34.0, 0.0), 1.2, 6, 0.9)
    for (x, y) in [(13.0, 11.0), (14.0, 15.0), (33.0, 14.5), (26.0, 16.0), (35.0, 24.0), (12.5, 22.5)]: banana(mb, M, (x, y, 0.0), int(x * 7 + y), 1.0)
    mb.finish()
    # tall grass clumps (verge, around huts, fence line)
    mb = MB('grass'); rg = rnd(11)
    for i in range(1300 + (520 if mode == 'night' else 0)):
        t = rg.random()
        if i >= 1300:
            y = rg.uniform(-8, 2.2); x = rg.uniform(-7.5, 8.0); px_ = 3.4 - (y + 4) * 0.3 if y > -4 else 3.5
            if abs(x - px_) < 1.5: continue
            grass_clump(mb, M, (x, y, 0.0), rg, rg.uniform(0.45, 0.95)); continue
        if t < 0.35: x, y = rg.uniform(-30, 14), rg.uniform(-1.8, 3.6)
        elif t < 0.55: x, y = rg.uniform(-30, -15.5), rg.uniform(4, 30)
        elif t < 0.8: x, y = rg.uniform(11.8, 40), rg.uniform(-1, 30)
        else: x, y = rg.uniform(-30, 40), rg.uniform(26, 50)
        if 10.0 < x < 18.0 and -3 < y < 3: continue
        if -13.3 < x < 10.4 and 4.4 < y < 25.6: continue
        if math.hypot(x - 20, y - 14) < 4.6 or math.hypot(x - 29, y - 10) < 3 or math.hypot(x - 22, y - 21) < 3 or (28 < x < 36 and 18 < y < 24): continue
        if -4.5 < y < -1.5 and mode_ != 'night': continue
        grass_clump(mb, M, (x, y, 0.0), rg, rg.uniform(0.6, 1.3))
    mb.finish()
    # --- elephant stand-in (night shot)
    if mode == 'night':
        mb = MB('elephant_STANDIN'); elephant(mb, M, P['ele'][0], P['ele'][1], P['ele'][2]); mb.finish()
    if mode == 'night':
        mb = MB('nightprops')
        firepit(mb, M, (1.3, 0.5, 0.0), True)
        for i in range(14):
            a = rg.random() * 6.283; r = rg.uniform(0.2, 0.9); mb.ell(M['ember'], (1.3 + math.cos(a) * r, 0.5 + math.sin(a) * r, rg.uniform(0.02, 0.12)), (0.025, 0.025, 0.015), (6, 4))
        for (x, y, yw) in [(3.4, -2.6, 0.5), (3.78, -2.4, 1.4), (3.5, -2.1, 2.6)]: jerrycan(mb, M, (x, y, 0.0), yw)
        basket(mb, M, (2.5, -3.3, 0.0)); hoe(mb, M, (4.1, -1.4, 0.0), 2.2)
        mb.finish()
        mz = rnd(21)
        for (x, y) in [(-1.3, -1.2), (-1.9, -1.5), (-2.4, -0.7), (-2.9, -1.4), (-2.0, -2.4)]:
            for src in vars_[mz.randrange(4)]:
                ob = bpy.data.objects.new('mzf', src.data); ob.location = (x, y, 0); ob.rotation_euler = (0, 0, mz.random() * 6.28); ob.scale = (1.0, 1.0, 1.05); sc.collection.objects.link(ob)
    if mode == 'night':
        mb = MB('lantern'); mb.rod(M['wood'], (1.9, 2.8, 0), (1.9, 2.8, 2.5), 0.06, 0.05, 6); mb.rod(M['wood'], (1.9, 2.8, 2.45), (1.9, 3.5, 2.45), 0.04, 0.04, 5); mb.rod(M['rope'], (1.9, 2.8, 2.4), (1.9, 2.8, 2.2), 0.01, 0.01, 4); mb.ell(M['lamp'], (1.9, 2.8, 2.1), (0.1, 0.1, 0.14), (8, 6)); mb.finish()
    if mode == 'night':
        kd0 = Vector(P['key_dir']).normalized(); mb = MB('moon'); mm = mat_emit('moon', '#c4d4ff', 1.15); cp = Vector(P['cam']['loc']) - kd0 * 330
        mb.ell(mm, cp, (4.2, 4.2, 4.2), (24, 16)); mb.finish()
    # --- lights
    k = P['key']; kd = Vector(P['key_dir']).normalized()
    d = bpy.data.lights.new('key', 'SUN'); d.color = k[:3]; d.energy = k[3]; d.angle = math.radians(P['sun_angle'])
    o = bpy.data.objects.new('key', d); sc.collection.objects.link(o); o.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler()
    for (pos, col, watt, rad) in P.get('lamps', []):
        l = bpy.data.lights.new('lamp', 'POINT'); l.color = col; l.energy = watt; l.shadow_soft_size = rad
        ob = bpy.data.objects.new('lamp', l); ob.location = pos; sc.collection.objects.link(ob)
    return M

def bees(M, c, n=14, seed=5, spread=0.35):
    mb = MB('bees'); rr = rnd(seed)
    for i in range(n):
        p = Vector(c) + Vector((-rr.uniform(0.0, spread * 1.6), rr.uniform(-spread * 0.8, spread * 0.8), rr.uniform(-spread, spread * 0.8)))
        a = rr.random() * 6.28
        mb.ell(M['bee'], p, (0.032, 0.017, 0.017), (8, 5), (0, 0, a))
        for sy in (-1, 1): mb.ell(M['wing'], p + Vector((0, sy * 0.012, 0.012)), (0.019, 0.03, 0.004), (6, 4), (0.4 * sy, 0, a))
    mb.finish()

# ------------------------------------------------------------------ presets / cameras
def kdir(az, el):
    """direction the light TRAVELS (from sun toward the ground), az = compass azimuth the sun sits at (deg, 0 = +y, 90 = +x), el = elevation"""
    a = math.radians(az); e = math.radians(el)
    return (-math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), -math.sin(e))

PRESETS = {
 'day': dict(
    sky=[(0.0, '#8aa3d8'), (0.42, '#e9b98c'), (0.5, '#f7d49c'), (0.56, '#f0d8b4'), (0.64, '#a9c6ec'), (0.8, '#5a8ee0'), (1.0, '#3a68c8')], sky_k=1.0,
    key=(1.0, 0.78, 0.5, 4.2), key_dir=kdir(-60, 27), sun_angle=1.0, exposure=-0.12, mount_x=250,
    hills=[(120, 6, 14, '#9a8fc0'), (170, 18, 26, '#8d9cca'), (205, 30, 30, '#7f9ed0')], hill_k=1.0, mount='#6f8fd4', cap='#f7e6dc',
    cam=dict(loc=(-8.4, -0.8, 2.8), look=(3.5, 7.0, -0.2), lens=22)),
 'night': dict(
    sky=[(0.0, '#1a2250'), (0.46, '#2d3b78'), (0.52, '#4a5a98'), (0.6, '#25316e'), (1.0, '#0d1445')], sky_k=2.0, stars=True,
    key=(0.46, 0.62, 1.0, 3.0), key_dir=kdir(-12, 33), sun_angle=1.2,
    hills=[(120, 6, 14, '#232c66'), (170, 18, 26, '#1f2a63'), (205, 30, 30, '#1c2760')], hill_k=0.9, mount_x=-100, mount='#222e70', cap='#7f93d0',
    lamps=[((1.3, 0.5, 0.55), (1.0, 0.5, 0.18), 650, 0.25), ((1.9, 2.8, 2.1), (1.0, 0.6, 0.26), 700, 0.12), ((18.2, 11.5, 1.6), (1.0, 0.62, 0.28), 900, 0.15), ((24.0, 8.6, 1.0), (1.0, 0.5, 0.2), 700, 0.3), ((30.5, 18.3, 1.8), (1.0, 0.65, 0.3), 700, 0.15), ((21.5, 20.0, 1.5), (1.0, 0.6, 0.3), 450, 0.15)],
    ele=((1.2, 2.4, 0.0), math.radians(12), 0.8),
    cam=dict(loc=(3.6, -6.5, 1.3), look=(-1.0, 6.0, 1.35), lens=22)),
 'close': dict(
    sky=[(0.0, '#2c3a82'), (0.44, '#d9806e'), (0.5, '#f4a868'), (0.58, '#6a74c0'), (1.0, '#1d2d78')], sky_k=0.85,
    key=(1.0, 0.55, 0.3, 3.3), key_dir=kdir(-115, 7), sun_angle=1.0,
    hills=[(120, 6, 14, '#6a5a98'), (170, 18, 26, '#5f6aa8'), (205, 30, 30, '#5470b0')], hill_k=0.8, mount='#4a62a8', cap='#e8b8b0',
    lamps=[((21.0, 8.8, 0.9), (1.0, 0.55, 0.22), 300, 0.3)],
    cam=dict(loc=(-6.4, 3.0, 1.05), look=(-3.7, 5.0, 1.65), lens=22)),
}

def setup_camera(P):
    sc = bpy.context.scene; c = P['cam']
    cd = bpy.data.cameras.new('cam'); cd.lens = c['lens']; cd.sensor_width = 36; cd.sensor_fit = 'AUTO'; cd.dof.use_dof = False
    ob = bpy.data.objects.new('cam', cd); sc.collection.objects.link(ob); ob.location = c['loc']
    ob.rotation_euler = (Vector(c['look']) - Vector(c['loc'])).to_track_quat('-Z', 'Y').to_euler(); sc.camera = ob

def render(mode, out, samples, draft):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; cy = sc.cycles; cy.device = 'CPU'; cy.samples = samples; cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'
    cy.denoising_input_passes = 'RGB_ALBEDO_NORMAL'; cy.max_bounces = 3; cy.diffuse_bounces = 2; cy.glossy_bounces = 1; cy.transmission_bounces = 0; cy.transparent_max_bounces = 4
    cy.use_light_tree = True; cy.filter_width = 1.2
    sc.render.threads = 4
    sc.render.resolution_x = W // (2 if draft else 1); sc.render.resolution_y = H // (2 if draft else 1); sc.render.resolution_percentage = 100
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = PRESETS[mode].get('exposure', 0.0)
    sc.render.image_settings.file_format = 'PNG'; sc.render.filepath = out + '.png'
    bpy.ops.render.render(write_still=True)
    im = Image.open(out + '.png').convert('RGB')
    # light grade: gentle saturation + contrast (no vignette)
    a = np.asarray(im, dtype=np.float32) / 255.0; g = a.mean(-1, keepdims=True); a = np.clip(g + (a - g) * PRESETS[mode].get('sat', 1.12), 0, 1)
    Image.fromarray((a * 255 + 0.5).astype(np.uint8)).save(out + '.jpg', quality=93); os.remove(out + '.png')

NAMES = {'day': 'sb1_day_wide', 'night': 'sb2_night_fence', 'close': 'sb3_hive_close'}
def run(mode, draft=False):
    t = time.time(); bpy.ops.wm.read_factory_settings(use_empty=True)
    M = build(mode); P = PRESETS[mode]
    if mode == 'close':
        bees(M, (-4.0 - 0.7, 5.0, 1.38), 18, 5, 0.3)
    if mode == 'night':
        pass
    setup_camera(P)
    out = os.path.join(HERE, ('d_' if draft else '') + NAMES[mode])
    render(mode, out, 24 if draft else P.get('samples', 112), draft); print(mode, 'done %.0fs' % (time.time() - t))

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != 'draft']; draft = 'draft' in sys.argv
    for m in (['day', 'night', 'close'] if (not args or args[0] == 'all') else args): run(m, draft)

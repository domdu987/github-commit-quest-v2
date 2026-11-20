"""set3d15 style board: Fosbury Flop. A = Oregon high-school track 1963 (golden afternoon), B = Mexico City Olympic stadium 1968 (evening).
usage: python3 sb.py a|b|c|all [draft]   -> sb1_track_golden.jpg / sb2_stadium_evening.jpg / sb3_bar_low.jpg (d_*.jpg when draft)
World units: metres, +x right, +y away from camera rig, z up. Camera 22 mm / 36 mm sensor (AUTO fit), 720x1280, no DOF. Helpers (mat, MB, lights, camera, render) come from ref_sb14.py."""
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


# ---- fast O(1) instancing overrides (bmesh.ops.create_* get quadratic on big meshes)
_TPL = {}
def _tpl(key):
    if key in _TPL: return _TPL[key]
    kind = key[0]
    if kind == 'cube':
        v = [(-.5, -.5, -.5), (.5, -.5, -.5), (.5, .5, -.5), (-.5, .5, -.5), (-.5, -.5, .5), (.5, -.5, .5), (.5, .5, .5), (-.5, .5, .5)]
        f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    elif kind == 'sph':
        us, vs = key[1], key[2]; v = [(0, 0, -1)]
        for j in range(1, vs):
            th = math.pi * j / vs
            for i in range(us): ph = 2 * math.pi * i / us; v.append((math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), -math.cos(th)))
        v.append((0, 0, 1)); f = []
        for i in range(us): f.append((0, 1 + (i + 1) % us, 1 + i))
        for j in range(vs - 2):
            for i in range(us):
                a = 1 + j * us + i; b = 1 + j * us + (i + 1) % us; c = 1 + (j + 1) * us + (i + 1) % us; d = 1 + (j + 1) * us + i; f.append((a, b, c, d))
        top = len(v) - 1; base = 1 + (vs - 2) * us
        for i in range(us): f.append((top, base + i, base + (i + 1) % us))
    elif kind == 'cyl':
        sg = key[1]; caps = key[2]; r1 = key[3]; v = []
        for i in range(sg): a = 2 * math.pi * i / sg; v.append((math.cos(a), math.sin(a), -.5))
        for i in range(sg): a = 2 * math.pi * i / sg; v.append((math.cos(a) * r1, math.sin(a) * r1, .5))
        f = [(i, (i + 1) % sg, sg + (i + 1) % sg, sg + i) for i in range(sg)]
        if caps: f.append(tuple(reversed(range(sg)))); f.append(tuple(range(sg, 2 * sg)))
    _TPL[key] = (v, f); return v, f
def _inst(self, m, key, M, smooth=False, scale3=None):
    v, f = _tpl(key); bm = self._b(m); vs = [bm.verts.new(M @ Vector(p)) for p in v]
    for fc in f:
        try:
            fa = bm.faces.new([vs[i] for i in fc]); fa.smooth = smooth
        except ValueError: pass
def _box(self, m, c, s, rz=0.0, rx=0.0, ry=0.0):
    M = self.T @ Matrix.Translation(c) @ Euler((rx, ry, rz)).to_matrix().to_4x4() @ Matrix.Diagonal((s[0], s[1], s[2], 1)); _inst(self, m, ('cube',), M)
def _ell(self, m, c, r, seg=(12, 8), rot=(0, 0, 0)):
    M = self.T @ Matrix.Translation(c) @ Euler(rot).to_matrix().to_4x4() @ Matrix.Diagonal((r[0], r[1], r[2], 1)); _inst(self, m, ('sph', seg[0], seg[1]), M, True)
def _rod(self, m, p0, p1, r0, r1=None, seg=8, caps=True, smooth=False):
    p0 = Vector(p0); p1 = Vector(p1); d = p1 - p0; ln = d.length
    if ln < 1e-6: return
    r1 = r0 if r1 is None else r1; rr_ = r1 / r0 if r0 > 0 else 0.01
    M = self.T @ Matrix.Translation((p0 + p1) / 2) @ d.to_track_quat('Z', 'Y').to_matrix().to_4x4() @ Matrix.Diagonal((r0, r0, ln, 1)); _inst(self, m, ('cyl', seg, caps, rr_), M, smooth)
MB.box = _box; MB.ell = _ell; MB.rod = _rod

# ------------------------------------------------------------------ palette
HEX = {}   # palette record for README
def pal():
    d = {}
    d['grass'] = mat('grass', '#8d9c3c', '#bcb458', 0.5, contrast=1.1)
    d['lawn'] = mat('lawn', '#7f9a3e', '#a3a84a', 0.9, contrast=1.0)
    d['dirt'] = mat('dirt', '#9c7a4a', '#bd9a66', 1.2)
    d['cinder'] = mat('cinder', '#7e3a2a', '#a65a3a', 2.5, contrast=1.3)
    d['tartan'] = mat('tartan', '#b4452e', '#cc643f', 1.8, contrast=0.8)
    d['chalk'] = mat('chalk', '#f0e4c8', '#e2d2ae', 3)
    d['concrete'] = mat('concrete', '#c4b2a8', '#dccabc', 0.8, contrast=0.9)
    d['concrete2'] = mat('concrete2', '#a49aa8', '#b8aeb4', 0.8)
    d['wood'] = mat('wood', '#6e4224', '#8f5a32', 6, aniso=(1, 1, 0.3), contrast=1.4)
    d['woodpale'] = mat('woodpale', '#b87c42', '#d8a463', 7, aniso=(0.3, 1, 1))
    d['woodgrey'] = mat('woodgrey', '#9a8268', '#b8a283', 6, aniso=(0.4, 1, 1))
    d['saw'] = mat('saw', '#d9a858', '#ecc880', 9, contrast=1.5)
    d['chip'] = mat('chip', '#a8743a', '#c8944e', 10)
    d['brick'] = mat('brick', '#9c4c36', '#bd6e4a', 3.2, aniso=(1, 1, 2.2), contrast=1.3)
    d['trim'] = mat('trim', '#eadfc6', '#d8c8a8', 2.5)
    d['glass'] = mat('glass', '#27324e', '#3e5078', 3)
    d['glasslit'] = mat('glasslit', '#c6803a', '#e8a456', 3, emit='#ffb458', emit_k=1.2)
    d['roofd'] = mat('roofd', '#5a4f60', '#72657a', 2)
    d['pine'] = mat('pine', '#2f5a3a', '#4f7a3e', 1.4, contrast=1.5, zgrad=(0, 6, '#22402e'))
    d['pine2'] = mat('pine2', '#3f6a3a', '#6e8a3a', 1.3, contrast=1.5)
    d['trunk'] = mat('trunk', '#4a3228', '#6d4a36', 5, aniso=(1, 1, 0.3))
    d['metal'] = mat('metal', '#aeb8c6', '#8896aa', 3, rough=0.45, sheen=0.4)
    d['steel'] = mat('steel', '#56637c', '#7584a0', 3, rough=0.5, sheen=0.3)
    d['wire'] = mat('wire', '#d8dce0', '#b8bec6', 2, rough=0.35, sheen=0.5)
    d['bar'] = mat('bar', '#f2e2ac', '#f2e2ac', rough=0.6)
    d['barr'] = mat('barr', '#d9552e', '#d9552e', rough=0.6)
    d['rust'] = mat('rust', '#b0562e', '#d07a40', 3)
    d['dark'] = mat('dark', '#2e2024', '#40292a', 3)
    d['cream'] = mat('cream', '#f0e2c0', '#e0cfa6', 3)
    d['red'] = mat('red', '#cf3c2a', '#e0583a', 4)
    d['orange'] = mat('orange', '#ec8a2c', '#f4a444', 4)
    d['yellow'] = mat('yellow', '#f0c43a', '#f8d860', 4)
    d['blue'] = mat('blue', '#2f5ea8', '#4a7cc4', 4)
    d['teal'] = mat('teal', '#2f8a86', '#4fa89c', 4)
    d['green'] = mat('green', '#4a8a3a', '#78a84a', 4)
    d['navy'] = mat('navy', '#26356a', '#364a88', 4)
    d['foam'] = mat('foam', '#7e9ccc', '#9ab4d8', 4, contrast=0.7)
    d['foamtop'] = mat('foamtop', '#a2b8dc', '#bccce2', 5, contrast=0.6)
    d['foamdk'] = mat('foamdk', '#5e74a2', '#7088b2', 4)
    d['cloth'] = mat('cloth', '#d8c08a', '#e8d4a0', 6)
    d['ember'] = mat_emit('ember', '#ff8a2a', 6.0)
    d['flame'] = mat_emit('flame', '#ff9a30', 14.0)
    d['flame2'] = mat_emit('flame2', '#ffd870', 24.0)
    d['lamp'] = mat_emit('lamp', '#fff0cc', 16.0)
    d['lampwarm'] = mat_emit('lampwarm', '#ffd890', 10.0)
    d['skin1'] = mat('skin1', '#d9a070', '#c8895a', 6)
    d['skin2'] = mat('skin2', '#8a5a3a', '#6a4430', 6)
    d['hair'] = mat('hair', '#2a2020', '#4a3428', 6)
    return d

CROWD_HEX = ['#e8c84a', '#d9532f', '#f0e4c8', '#3a6fb8', '#4aa086', '#e88a2e', '#a8c8e8', '#c8d24a', '#2d4a7a', '#cf3c2a', '#f4d8a8', '#5a8ad0', '#e87a4a', '#78a84a']
def crowd_mats():
    return [mat('cw%d' % i, h, h, 1.0, rough=1.0) for i, h in enumerate(CROWD_HEX)]

# ------------------------------------------------------------------ sky (z gradient + sun glow lobe)
def sky2(P):
    w = bpy.data.worlds.new('sky'); bpy.context.scene.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputWorld'); bg = N('ShaderNodeBackground'); tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Generated'], sp.inputs[0])
    cr = N('ShaderNodeValToRGB'); L(sp.outputs['Z'], cr.inputs[0])
    st = P['sky']
    cr.color_ramp.elements[0].position = st[0][0]; cr.color_ramp.elements[0].color = hexc(st[0][1])
    for pos, col in st[1:-1]:
        e = cr.color_ramp.elements.new(pos); e.color = hexc(col)
    cr.color_ramp.elements[-1].position = st[-1][0]; cr.color_ramp.elements[-1].color = hexc(st[-1][1])
    # glow lobe toward the sun
    kd = Vector(P['key_dir']).normalized(); sd = -kd
    ma = N('ShaderNodeVectorMath'); ma.operation = 'MULTIPLY_ADD'; L(tc.outputs['Generated'], ma.inputs[0]); ma.inputs[1].default_value = (2, 2, 2); ma.inputs[2].default_value = (-1, -1, -1)
    dt = N('ShaderNodeVectorMath'); dt.operation = 'DOT_PRODUCT'; L(ma.outputs[0], dt.inputs[0]); dt.inputs[1].default_value = tuple(sd)
    mr = N('ShaderNodeMapRange'); L(dt.outputs['Value'], mr.inputs['Value']); mr.inputs['From Min'].default_value = P['glow'][1]; mr.inputs['From Max'].default_value = 1.0; mr.interpolation_type = 'SMOOTHSTEP'
    # fade glow with height so it hugs the horizon
    zf = N('ShaderNodeMapRange'); L(sp.outputs['Z'], zf.inputs['Value']); zf.inputs['From Min'].default_value = 0.72; zf.inputs['From Max'].default_value = 0.5
    mu = N('ShaderNodeMath'); mu.operation = 'MULTIPLY'; L(mr.outputs['Result'], mu.inputs[0]); L(zf.outputs['Result'], mu.inputs[1])
    mu2 = N('ShaderNodeMath'); mu2.operation = 'MULTIPLY'; mu2.inputs[1].default_value = P['glow'][2]; L(mu.outputs[0], mu2.inputs[0])
    ad = N('ShaderNodeMix'); ad.data_type = 'RGBA'; ad.blend_type = 'MIX'; L(cr.outputs[0], ad.inputs[6]); ad.inputs[7].default_value = hexc(P['glow'][0]); L(mu2.outputs[0], ad.inputs[0])
    bg.inputs['Strength'].default_value = P['sky_k']; L(ad.outputs[2], bg.inputs['Color']); L(bg.outputs[0], out.inputs['Surface'])

def ridges(P):
    """Far ridge ring around the whole scene (emission flat colours -> atmospheric perspective)."""
    mb = MB('hills'); rr = rnd(9)
    for li, (rad, bh, amp, col) in enumerate(P['hills']):
        m = mat_emit('hill%d_%s' % (li, P['name']), col, P['hill_k']); n = 240; ph = [rr.uniform(0, 6) for _ in range(4)]
        pts = []
        for i in range(n + 1):
            t = i / n * 2 * math.pi
            h = bh + amp * (0.5 * math.sin(t * 7 + ph[0]) + 0.3 * math.sin(t * 17 + ph[1]) + 0.2 * math.sin(t * 41 + ph[2]))
            pts.append((P['cx'] + rad * math.cos(t), P['cy'] + rad * math.sin(t), h))
        for i in range(n):
            a, b = pts[i], pts[i + 1]
            mb.quad(m, [(a[0], a[1], -5), (b[0], b[1], -5), (b[0], b[1], b[2]), (a[0], a[1], a[2])])
    mb.finish()

def plane(m, size, z=0.0, c=(0, 0)):
    me = bpy.data.meshes.new('pl'); bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=size); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new('pl', me); ob.location = (c[0], c[1], z); ob.data.materials.append(m); bpy.context.scene.collection.objects.link(ob)

# ------------------------------------------------------------------ helpers / props
def ring(mb, m, cx, cy, a0, b0, a1, b1, t0, t1, z, step=2.0):
    n = max(2, int(abs(t1 - t0) / step))
    for i in range(n):
        u0 = math.radians(t0 + (t1 - t0) * i / n); u1 = math.radians(t0 + (t1 - t0) * (i + 1) / n)
        P = lambda a, b, u: (cx + a * math.cos(u), cy + b * math.sin(u), z)
        mb.quad(m, [P(a0, b0, u0), P(a1, b1, u0), P(a1, b1, u1), P(a0, b0, u1)])

def disc(mb, m, c, r, z, seg=40, rx=None):
    rx = r if rx is None else rx
    for i in range(seg):
        u0 = i / seg * 6.2832; u1 = (i + 1) / seg * 6.2832
        mb.tri(m, [(c[0], c[1], z), (c[0] + rx * math.cos(u0), c[1] + r * math.sin(u0), z), (c[0] + rx * math.cos(u1), c[1] + r * math.sin(u1), z)])

def pine(mb, M, x, y, h, seed):
    rr = rnd(seed); mb.rod(M['trunk'], (x, y, -0.2), (x, y, h * 0.5), 0.22 * h / 10, 0.1 * h / 10, 7, smooth=True)
    n = 6; mt = M['pine'] if seed % 2 else M['pine2']
    for k in range(n):
        u = k / n; z0 = h * (0.16 + 0.78 * u * 0.95); r0 = h * 0.2 * (1 - u * 0.8) + 0.4
        mb.cone(mt, (x + rr.uniform(-.2, .2), y + rr.uniform(-.2, .2), z0), r0, 0.05, h * 0.26, 11)

def hurdle(mb, M, c, yaw=0.0, tip=0.0):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Euler((tip, 0, 0)).to_matrix().to_4x4())
    for sx in (-0.55, 0.55):
        mb.rod(M['metal'], (sx, 0, 0.0), (sx, 0, 0.9), 0.016, 0.016, 6)
        mb.box(M['metal'], (sx, 0.0, 0.01), (0.04, 0.5, 0.02))
    mb.box(M['cream'], (0, 0, 0.84), (1.2, 0.03, 0.14)); mb.box(M['rust'], (-0.4, 0.0, 0.84), (0.2, 0.035, 0.14)); mb.box(M['rust'], (0.4, 0.0, 0.84), (0.2, 0.035, 0.14))
    mb.pop()

def bench(mb, M, c, yaw=0.0, L=2.4):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M['woodpale'], (0, 0, 0.45), (L, 0.36, 0.06)); mb.box(M['woodpale'], (0, -0.22, 0.52), (L, 0.05, 0.28)); 
    for sx in (-L / 2 + 0.2, L / 2 - 0.2):
        mb.box(M['wood'], (sx, 0, 0.22), (0.07, 0.34, 0.44)); mb.box(M['wood'], (sx, -0.2, 0.5), (0.07, 0.06, 0.5))
    mb.pop()

def cooler(mb, M, c):
    x, y, z = c
    mb.rod(M['orange'], (x, y, z), (x, y, z + 0.42), 0.2, 0.2, 14); mb.rod(M['cream'], (x, y, z + 0.42), (x, y, z + 0.5), 0.21, 0.21, 14)
    mb.box(M['metal'], (x + 0.2, y, z + 0.28), (0.1, 0.06, 0.05)); mb.rod(M['cream'], (x, y, z + 0.5), (x, y, z + 0.56), 0.1, 0.08, 10)

def bag(mb, M, c, yaw, mt='blue', L=0.7):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M[mt], (0, 0, 0.16), (L, 0.28, 0.3)); mb.ell(M[mt], (-L / 2, 0, 0.16), (0.04, 0.14, 0.15), (8, 6)); mb.ell(M[mt], (L / 2, 0, 0.16), (0.04, 0.14, 0.15), (8, 6))
    mb.box(M['cream'], (0, 0, 0.16), (0.12, 0.29, 0.31)); mb.rod(M['dark'], (-0.2, 0, 0.32), (0.2, 0, 0.32), 0.02, 0.02, 5)
    mb.pop()

def cone_t(mb, M, c):
    x, y, z = c
    mb.cone(M['orange'], (x, y, z), 0.14, 0.03, 0.4, 10); mb.box(M['orange'], (x, y, z + 0.01), (0.34, 0.34, 0.02)); mb.cone(M['cream'], (x, y, z + 0.18), 0.09, 0.07, 0.07, 10)

def bottle(mb, M, c, mt='blue'):
    x, y, z = c; mb.rod(M[mt], (x, y, z), (x, y, z + 0.22), 0.04, 0.04, 8); mb.rod(M['cream'], (x, y, z + 0.22), (x, y, z + 0.27), 0.015, 0.015, 6)

def jacket(mb, M, c, yaw, mt='red', s=1.0):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Diagonal((s, s, s, 1)))
    mb.box(M[mt], (0, 0, 0.04), (0.6, 0.45, 0.08)); mb.box(M[mt], (-0.32, 0.1, 0.05), (0.3, 0.14, 0.09), rz=0.5); mb.box(M[mt], (0.3, 0.12, 0.05), (0.3, 0.14, 0.09), rz=-0.5)
    mb.box(M['cream'], (0, 0, 0.085), (0.6, 0.06, 0.012))
    mb.pop()

def shoe(mb, M, c, yaw):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M['cream'], (0, 0, 0.02), (0.27, 0.1, 0.04)); mb.ell(M['dark'], (0.0, 0, 0.07), (0.13, 0.05, 0.05), (8, 5)); mb.ell(M['red'], (-0.06, 0, 0.1), (0.05, 0.045, 0.05), (6, 4))
    mb.pop()

def rake(mb, M, c, to):
    p0 = Vector(c); p1 = Vector(to)
    mb.rod(M['woodpale'], p0, p1, 0.016, 0.016, 6); d = (p1 - p0).normalized()
    mb.box(M['metal'], p0 + Vector((0, 0, 0.02)), (0.5, 0.05, 0.03), rz=math.atan2(d.y, d.x) + 1.5708)
    for i in range(6):
        mb.rod(M['metal'], p0 + Vector((0, 0, 0.02)) + Vector((-d.y, d.x, 0)) * (-0.22 + i * 0.088), p0 + Vector((0, 0, -0.0)) + Vector((-d.y, d.x, 0)) * (-0.22 + i * 0.088) - d * 0.0, 0.006, 0.004, 4)

def tape_reel(mb, M, c, yaw):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.rod(M['rust'], (0, 0, 0.0), (0, 0, 0.09), 0.2, 0.2, 18); mb.rod(M['cream'], (0, 0, 0.09), (0, 0, 0.11), 0.16, 0.16, 18); mb.rod(M['dark'], (0, 0, 0.11), (0, 0, 0.12), 0.04, 0.04, 8)
    mb.box(M['dark'], (0.26, 0, 0.05), (0.18, 0.025, 0.02)); mb.box(M['yellow'], (0.7, 0.0, 0.003), (0.9, 0.04, 0.004))
    mb.pop()

def wheelbarrow(mb, M, c, yaw):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M['green'], (0, 0, 0.42), (0.9, 0.62, 0.28)); mb.box(M['saw'], (0, 0, 0.58), (0.8, 0.52, 0.06))
    mb.rod(M['dark'], (0.55, 0, 0.2), (0.55, 0, 0.2), 0.0, 0.0, 3) if False else None
    mb.rod(M['dark'], (0.6, -0.04, 0.22), (0.6, 0.04, 0.22), 0.22, 0.22, 16, caps=True)
    for sy in (-0.28, 0.28):
        mb.rod(M['woodpale'], (0.55, sy, 0.4), (-1.0, sy * 1.3, 0.75), 0.022, 0.022, 6); mb.rod(M['metal'], (-0.35, sy, 0.3), (-0.35, sy, 0.0), 0.02, 0.02, 5)
    mb.pop()

def bucket(mb, M, c, mt='metal'):
    x, y, z = c; mb.rod(M[mt], (x, y, z), (x, y, z + 0.3), 0.14, 0.17, 12); mb.rod(M['saw'], (x, y, z + 0.28), (x, y, z + 0.31), 0.15, 0.15, 12)

def chair(mb, M, c, yaw):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M['blue'], (0, 0, 0.45), (0.42, 0.4, 0.04)); mb.box(M['blue'], (0, -0.2, 0.7), (0.42, 0.04, 0.4))
    for dx in (-0.18, 0.18):
        mb.rod(M['metal'], (dx, -0.17, 0.0), (dx, 0.17, 0.45), 0.014, 0.014, 5); mb.rod(M['metal'], (dx, 0.17, 0.0), (dx, -0.17, 0.45), 0.014, 0.014, 5)
    mb.pop()

def pennant_line(mb, M, p0, p1, n, mats, sag=0.4, size=0.32):
    p0 = Vector(p0); p1 = Vector(p1); prev = None; d = (p1 - p0)
    side = Vector((-d.y, d.x, 0)).normalized()
    for i in range(n + 1):
        u = i / n; p = p0 + d * u - Vector((0, 0, sag * 4 * u * (1 - u)))
        if prev is not None: mb.rod(M['cream'], prev, p, 0.006, 0.006, 4, caps=False)
        prev = p
    for i in range(n):
        u = (i + 0.5) / n; p = p0 + d * u - Vector((0, 0, sag * 4 * u * (1 - u))); e = d.normalized() * size * 0.5
        m = M[mats[i % len(mats)]]
        mb.tri(m, [p - e, p + e, p + Vector((0, 0, -size * 1.2))]) 

def flagpole(mb, M, x, y, z, h, cols, yaw=0.0, wave=0.0):
    mb.rod(M['metal'], (x, y, z), (x, y, z + h), 0.04, 0.025, 6); mb.ell(M['yellow'], (x, y, z + h + 0.05), (0.06, 0.06, 0.06), (6, 4))
    d = Vector((math.cos(yaw), math.sin(yaw), 0)); L = 1.8; Hh = 1.1
    for k, cm in enumerate(cols):
        zt = z + h - 0.12 - Hh * k / len(cols); zb = z + h - 0.12 - Hh * (k + 1) / len(cols)
        pts = []
        for t in range(4):
            u = t / 3; w = math.sin(u * 3.2 + wave) * 0.12 * u
            pts.append(d * (u * L) + Vector((0, 0, 0)) + Vector((-d.y, d.x, 0)) * w)
        for t in range(3):
            a, b = pts[t], pts[t + 1]; P0 = Vector((x, y, 0)) + a; P1 = Vector((x, y, 0)) + b
            mb.quad(M[cm], [P0 + Vector((0, 0, zt)), P1 + Vector((0, 0, zt)), P1 + Vector((0, 0, zb)), P0 + Vector((0, 0, zb))])

def standards(mb, M, xc, y, half, bar_z, kind='wood', top=2.7):
    mt = M['wood'] if kind == 'wood' else M['steel']
    for sx in (-half, half):
        x = xc + sx
        if kind == 'wood':
            mb.box(mt, (x, y, top / 2), (0.08, 0.08, top)); mb.box(M['woodpale'], (x, y, 0.04), (0.5, 1.0, 0.08)); mb.box(M['woodpale'], (x, y - 0.1, 0.12), (0.12, 0.8, 0.1))
        else:
            mb.rod(mt, (x, y, 0.0), (x, y, top), 0.035, 0.03, 8, smooth=True); mb.box(M['steel'], (x, y, 0.05), (0.55, 0.75, 0.1)); mb.box(M['metal'], (x, y, 0.12), (0.1, 0.1, 0.1))
        k = 1 if sx < 0 else -1
        for i in range(14):
            pz = 1.05 + i * 0.1
            mb.box(M['metal'] if kind != 'wood' else M['rust'], (x + k * 0.05, y, pz), (0.1, 0.035, 0.03))
        mb.box(M['yellow'], (x, y - 0.045, top - 0.03), (0.09, 0.02, 0.3)) if kind == 'wood' else None
    # crossbar: alternating cream / rust segments, slight sag
    x0, x1 = xc - half + 0.06, xc + half - 0.06; n = 12
    for i in range(n):
        u0 = i / n; u1 = (i + 1) / n
        s0 = 0.012 * 4 * u0 * (1 - u0); s1 = 0.012 * 4 * u1 * (1 - u1)
        mb.rod(M['bar'] if i % 2 == 0 else M['barr'], (x0 + (x1 - x0) * u0, y, bar_z - s0), (x0 + (x1 - x0) * u1, y, bar_z - s1), 0.04, 0.04, 6)
    mb.box(M['dark'], (x0, y, bar_z - 0.03), (0.05, 0.05, 0.03)); mb.box(M['dark'], (x1, y, bar_z - 0.03), (0.05, 0.05, 0.03))

def chainlink(mb, M, a, b, h=1.9, panel=3.0):
    a = Vector(a); b = Vector(b); d = b - a; L = d.length; n = max(1, int(L / panel)); dn = d.normalized()
    for i in range(n + 1):
        p = a + d * (i / n); mb.rod(M['metal'], (p.x, p.y, 0), (p.x, p.y, h + 0.1), 0.04, 0.035, 6)
    mb.rod(M['metal'], (a.x, a.y, h), (b.x, b.y, h), 0.025, 0.025, 6); mb.rod(M['metal'], (a.x, a.y, 0.15), (b.x, b.y, 0.15), 0.018, 0.018, 5)
    m = int(L / 0.45)
    for i in range(m):
        p = a + dn * (i * 0.45); q = a + dn * min(L, i * 0.45 + 0.9)
        r0 = (p.x, p.y, 0.15); r1 = (q.x, q.y, 0.15 + (h - 0.15) * ((q - p).length / 0.9))
        # one diagonal each way, cheap lattice
        mb.rod(M['wire'], (p.x, p.y, 0.15), (q.x, q.y, 0.15 + 0.9), 0.006, 0.006, 3, caps=False)
        mb.rod(M['wire'], (p.x, p.y, 1.05), (q.x, q.y, 0.15), 0.006, 0.006, 3, caps=False)

def bleacher(mb, M, c, yaw, L=11.0, rows=6, items=None):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    for i in range(rows):
        zr = 0.45 * (i + 1); yr = i * 0.85
        mb.box(M['woodgrey'], (0, yr, zr), (L, 0.32, 0.06)); mb.box(M['woodgrey'], (0, yr - 0.3, zr), (L, 0.26, 0.06))
        mb.box(M['woodpale'], (0, yr - 0.45, zr - 0.2), (L, 0.04, 0.34)); mb.box(M['woodgrey'], (0, yr + 0.05, zr - 0.38), (L, 0.28, 0.05))
    k = int(L / 2.5)
    for j in range(k + 1):
        sx = -L / 2 + 0.2 + j * (L - 0.4) / k
        mb.rod(M['steel'], (sx, 0.0, 0), (sx, 0.0, 0.45 * rows), 0.04, 0.04, 6); mb.rod(M['steel'], (sx, (rows - 1) * 0.85, 0), (sx, (rows - 1) * 0.85, 0.45 * rows), 0.04, 0.04, 6)
        mb.rod(M['steel'], (sx, 0.0, 0.0), (sx, (rows - 1) * 0.85 + 0.2, 0.45 * rows - 0.1), 0.03, 0.03, 6); mb.rod(M['steel'], (sx, (rows - 1) * 0.85 + 0.9, 0), (sx, (rows - 1) * 0.85, 0.45 * rows), 0.03, 0.03, 6)
    zt = 0.45 * rows + 0.9
    mb.rod(M['steel'], (-L / 2, (rows - 1) * 0.85 + 0.25, zt), (L / 2, (rows - 1) * 0.85 + 0.25, zt), 0.025, 0.025, 6)
    for j in range(k + 1):
        sx = -L / 2 + 0.2 + j * (L - 0.4) / k; mb.rod(M['steel'], (sx, (rows - 1) * 0.85 + 0.25, 0.45 * rows), (sx, (rows - 1) * 0.85 + 0.25, zt), 0.025, 0.025, 6)
    mb.pop()

def ground_pt(P, u, v, z=0.0):
    c = P['cam']; loc = Vector(c['loc']); q = (Vector(c['look']) - loc).to_track_quat('-Z', 'Y').to_matrix()
    d = q @ Vector((u * 0.46, v * 0.818, -1.0)); t = (z - loc.z) / d.z; p = loc + d * t
    return (p.x, p.y, z)

# ------------------------------------------------------------------ SCENE A: 1963 Oregon high-school track
def build_a(P):
    sc = bpy.context.scene; M = pal(); rr = rnd(15)
    sky2(P); ridges(P)
    plane(M['grass'], 600, -0.02)
    mb = MB('ground')
    cx, cy = 0.0, -34.0
    ring(mb, M['cinder'], cx, cy, 47, 47, 53, 53, 8, 172, 0.012, 1.0)
    for r in (47.0, 53.0 - 0.15):
        ring(mb, M['chalk'], cx, cy, r, r, r + 0.15, r + 0.15, 8, 172, 0.02, 1.0)
    for r in (49.0, 50.9): ring(mb, M['chalk'], cx, cy, r, r, r + 0.07, r + 0.07, 8, 172, 0.018, 1.0)
    disc(mb, M['dirt'], (0.4, 1.0), 3.6, 0.008, 40, 5.2)          # worn run-up
    
    # run-up chalk marks (two short marks, no text)
    for (x0, y0, x1, y1) in [(-0.4, -1.0, 0.4, -0.6), (-0.5, 1.8, 0.3, 2.3)]: mb.box(M['chalk'], ((x0 + x1) / 2, (y0 + y1) / 2, 0.015), (0.9, 0.06, 0.006), rz=0.5)
    mb.finish()
    mb = MB('setA')
    # --- landing pit: low wooden frame + sawdust/wood-chip fill
    px, py, pw, pd = 0.0, 7.6, 4.8, 4.0
    for sy, hh in ((py - pd / 2, 0.42), (py + pd / 2, 0.42)): mb.box(M['wood'], (px, sy, hh / 2), (pw, 0.12, hh)); mb.box(M['woodpale'], (px, sy, hh + 0.02), (pw + 0.1, 0.2, 0.04))
    for sx in (px - pw / 2, px + pw / 2): mb.box(M['wood'], (sx, py, 0.21), (0.12, pd, 0.42)); mb.box(M['woodpale'], (sx, py, 0.44), (0.2, pd + 0.1, 0.04))
    mb.box(M['saw'], (px, py, 0.26), (pw - 0.1, pd - 0.1, 0.34))
    mb.ell(M['saw'], (px, py, 0.34), (pw / 2 - 0.2, pd / 2 - 0.2, 0.36), (24, 10))
    mb.ell(M['saw'], (px - 1.2, py + 0.3, 0.52), (0.9, 0.7, 0.14), (12, 6)); mb.ell(M['saw'], (px + 0.9, py - 0.4, 0.55), (0.7, 0.6, 0.12), (12, 6))
    for i in range(150):
        x = px + rr.uniform(-2.2, 2.2); y = py + rr.uniform(-1.8, 1.8)
        if ((x - px) / 2.3) ** 2 + ((y - py) / 1.9) ** 2 < 1:
            mb.box(M['chip'], (x, y, 0.56 + rr.uniform(-0.15, 0.0)), (rr.uniform(0.05, 0.13), rr.uniform(0.02, 0.05), 0.012), rz=rr.random() * 6)
    # spill of sawdust around the frame
    for i in range(14):
        x = px + rr.uniform(-3.4, 3.4); y = py + rr.uniform(-3.0, 3.0)
        if abs(x - px) > 2.55 or abs(y - py) > 2.15: mb.ell(M['saw'], (x, y, 0.01), (rr.uniform(.15, .4), rr.uniform(.12, .3), 0.015), (8, 4))
    # --- standards + bar (front of pit, run-up side)
    standards(mb, M, 0.0, 5.3, 2.0, 1.72, 'wood')
    rake(mb, M, (px + pw / 2 + 0.35, py + 0.7, 0.0), (px + pw / 2 - 0.05, py + 0.4, 0.95))
    fx, fy, _ = ground_pt(P, -0.62, -0.5); hurdle(mb, M, (fx, fy, 0.0), 0.9, 0.0)
    fx, fy, _ = ground_pt(P, 0.5, -0.62); bag(mb, M, (fx, fy, 0.0), 0.6, 'red', 0.8)
    def G(u, v): return ground_pt(P, u, 0.2 + (v - 0.2) * 0.5)
    # --- team bench, cooler, bags (right of the pit)
    bx, by, _ = G(0.86, -0.02); bench(mb, M, (bx, by, 0.0), 1.2, 3.0)
    bx2, by2, _ = G(0.5, 0.0); bench(mb, M, (bx2 + 0.5, by2 + 2.4, 0.0), 1.3, 2.4)
    cx_, cy_, _ = G(0.66, -0.03); cooler(mb, M, (cx_, cy_, 0.0))
    jacket(mb, M, (bx + 0.2, by - 0.6, 0.48), 1.2, 'red'); jacket(mb, M, (bx + 0.1, by + 0.5, 0.48), 1.0, 'navy'); jacket(mb, M, (bx2 + 0.5, by2 + 2.3, 0.48), 0.4, 'yellow')
    for (u, v, yw, mt, L_) in [(0.95, -0.1, 0.5, 'blue', 0.7), (0.78, -0.12, 1.3, 'red', 0.6), (0.4, -0.27, 2.0, 'red', 0.8), (0.55, -0.33, 0.2, 'teal', 0.6), (-0.8, -0.18, 1.1, 'green', 0.7)]:
        x_, y_, _ = G(u, v); bag(mb, M, (x_, y_, 0.0), yw, mt, L_)
    for (u, v, m_) in [(0.6, -0.08, 'blue'), (0.7, -0.06, 'yellow'), (0.74, -0.09, 'cream')]:
        x_, y_, _ = G(u, v); bottle(mb, M, (x_, y_, 0.0), m_)
    # --- hurdles stacked + scattered
    x_, y_, _ = G(0.2, -0.16)
    for k in range(4): hurdle(mb, M, (x_, y_ + k * 0.3, 0.0), 0.35, 0.0)
    for (u, v, yw, tp) in [(0.9, -0.18, 1.1, 0.0), (-0.38, -0.12, 0.8, 1.45), (-0.2, -0.05, 1.6, 0.0)]:
        x_, y_, _ = G(u, v); hurdle(mb, M, (x_, y_, 0.0), yw, tp)
    # --- warm-up gear
    for (u, v) in [(-0.3, -0.36), (0.05, -0.4)]:
        x_, y_, _ = G(u, v); tape_reel(mb, M, (x_, y_, 0.0), 0.6) if u < 0 else bag(mb, M, (x_, y_, 0.0), 2.0, 'orange', 0.8)
    x_, y_, _ = G(-0.45, -0.3); jacket(mb, M, (x_, y_, 0.0), 0.8, 'orange'); x_, y_, _ = G(0.3, -0.12); jacket(mb, M, (x_, y_, 0.0), 2.5, 'cream')
    for (u, v, yw) in [(-0.1, -0.45, 0.4), (-0.02, -0.46, 0.9), (0.62, -0.47, 2.2), (0.68, -0.48, 2.6), (-0.4, -0.2, 1.0)]:
        x_, y_, _ = G(u, v); shoe(mb, M, (x_, y_, 0.0), yw)
    for (u, v) in [(-0.7, -0.08), (0.75, -0.3), (-0.25, -0.24), (0.15, -0.6)]:
        x_, y_, _ = G(u, v); cone_t(mb, M, (x_, y_, 0.0))
    x_, y_, _ = G(0.9, -0.2); bucket(mb, M, (x_, y_, 0.0)); x_, y_, _ = G(-0.55, -0.1); wheelbarrow(mb, M, (x_, y_, 0.0), 2.2)
    # second team bench and cooler at left, line of hurdles, extra gear
    bx, by, _ = G(-0.82, -0.02); bench(mb, M, (bx, by, 0.0), 1.9, 2.8); cooler(mb, M, (bx + 0.5, by - 0.6, 0.0)); jacket(mb, M, (bx, by, 0.48), 1.8, 'orange'); jacket(mb, M, (bx - 0.2, by + 0.9, 0.48), 1.5, 'teal')
    for k in range(5):
        x_, y_, _ = G(-0.55 + k * 0.1, -0.09 - k * 0.02); hurdle(mb, M, (x_, y_, 0.0), 0.2 + k * 0.1, 0.0)
    for (u, v, yw, mt) in [(-0.9, -0.12, 0.4, 'navy'), (-0.7, 0.0, 1.0, 'yellow'), (0.1, -0.02, 2.0, 'teal')]:
        x_, y_, _ = G(u, v); bag(mb, M, (x_, y_, 0.0), yw, mt, 0.7)
    for (u, v) in [(-0.3, 0.02), (0.2, 0.0), (0.45, 0.02)]:
        x_, y_, _ = G(u, v); cone_t(mb, M, (x_, y_, 0.0)); chair(mb, M, (x_ + 0.6, y_ + 0.5, 0.0), 0.5) if u > 0.3 else None
    # sack of sawdust + a ball
    mb.ell(M['woodgrey'], (-3.0, 8.6, 0.25), (0.35, 0.25, 0.3), (10, 8)); mb.ell(M['dark'], (2.0, 3.0, 0.14), (0.14, 0.14, 0.14), (10, 8))
    mb.finish()
    # --- bleachers (right), with coats and bags
    mb = MB('bleach')
    bleacher(mb, M, (15.5, 24.0, 0.0), -1.5708, 11.0, 6)
    # items on bleachers: world positions computed in local frame (yaw -90: local x -> world -y, local y -> world +x)
    def bw(lx, ly, lz): return (15.5 + ly, 24.0 - lx, lz)
    for (lx, row, mt, yw) in [(-3.5, 2, 'red', 0.3), (-1.0, 1, 'blue', 1.6), (2.0, 3, 'yellow', 0.1), (3.6, 1, 'navy', 2.0), (-4.6, 4, 'orange', 0.6), (0.6, 4, 'teal', 1.0)]:
        jacket(mb, M, bw(lx, row * 0.85, 0.45 * (row + 1) + 0.03), yw, mt, 1.1)
    for (lx, row, mt) in [(-2.0, 3, 'red'), (4.4, 2, 'blue'), (0.2, 2, 'green')]: bag(mb, M, bw(lx, row * 0.85, 0.45 * (row + 1) + 0.03), 1.5708, mt, 0.7)
    for (lx, row) in [(-5.0, 0), (1.4, 0), (4.8, 3)]: bottle(mb, M, bw(lx, row * 0.85, 0.45 * (row + 1) + 0.03), 'cream')
    mb.finish()
    # second small bleacher further out, shadowed
    mb = MB('bleach2'); bleacher(mb, M, (-26.0, 33.0, 0.0), 0.9, 9.0, 4); mb.finish()
    # --- chain-link fence along the outside of the track
    mb = MB('fence'); ro = 56.5
    ts = [math.radians(t) for t in np.linspace(48, 140, 30)]
    pts = [(cx + ro * math.cos(t), cy + ro * math.sin(t)) for t in ts]
    for a, b in zip(pts[:-1], pts[1:]): chainlink(mb, M, a, b, 1.9, 3.0)
    # pennant strings from fence to flagpole
    pennant_line(mb, M, (pts[3][0], pts[3][1], 3.6), (pts[26][0], pts[26][1], 3.6), 40, ['red', 'yellow', 'blue', 'cream', 'orange', 'teal'], 3.0, 0.5) if False else None
    mb.finish()
    # --- pole+pennants, tall poles
    mb = MB('poles')
    for (x, y) in [(-14.0, 21.0), (22.0, 20.2)]:
        mb.rod(M['wood'], (x, y, 0), (x, y, 6.5), 0.1, 0.07, 7)
    pennant_line(mb, M, (-14.0, 21.0, 6.2), (22.0, 20.2, 6.2), 46, ['red', 'yellow', 'blue', 'cream', 'orange', 'teal'], 2.5, 0.65)
    flagpole(mb, M, 30.0, 18.5, 0.0, 9.0, ['red', 'cream', 'blue'], 0.2, 0.6)
    mb.finish()
    # --- gym: low brick building
    mb = MB('gym'); gx, gy = 22.0, 62.0
    mb.box(M['brick'], (gx, gy, 3.6), (46, 12, 7.2)); mb.box(M['trim'], (gx, gy - 6.05, 7.3), (46.4, 0.5, 0.5)); mb.box(M['roofd'], (gx, gy, 7.55), (46.2, 12.2, 0.4))
    mb.box(M['brick'], (gx - 28, gy - 4, 2.4), (14, 8, 4.8)); mb.box(M['roofd'], (gx - 28, gy - 4, 4.95), (14.4, 8.4, 0.3))
    for i in range(14):
        wx = gx - 20 + i * 3.1; mb.box(M['trim'], (wx, gy - 6.06, 4.6), (1.5, 0.12, 1.9)); mb.box(M['glass'] if i % 3 else M['glasslit'], (wx, gy - 6.12, 4.6), (1.3, 0.1, 1.7))
    mb.box(M['dark'], (gx - 4, gy - 6.08, 1.4), (3.0, 0.12, 2.8)); mb.box(M['trim'], (gx - 4, gy - 6.12, 2.9), (3.6, 0.2, 0.3))
    for i in range(3): mb.box(M['glass'], (gx - 32 + i * 4, gy - 8.07, 2.6), (1.7, 0.1, 1.5)); mb.box(M['trim'], (gx - 32 + i * 4, gy - 8.04, 3.5), (2.0, 0.1, 0.2))
    mb.finish()
    # --- pines
    mb = MB('pines')
    for i in range(9): pine(mb, M, rr.uniform(-20, -6), rr.uniform(24, 40), rr.uniform(12, 18), 400 + i)
    for i in range(5): pine(mb, M, rr.uniform(-3, 8), rr.uniform(38, 48), rr.uniform(12, 17), 500 + i)
    for i in range(70):
        x = rr.uniform(-60, 70); y = rr.uniform(44, 100)
        if gx - 24 < x < gx + 24 and y < 72: continue
        pine(mb, M, x, y, rr.uniform(10, 18), i)
    for i in range(14): pine(mb, M, rr.uniform(-60, -14), rr.uniform(26, 46), rr.uniform(14, 22), 100 + i)
    for i in range(10): pine(mb, M, rr.uniform(32, 60), rr.uniform(28, 40), rr.uniform(16, 24), 300 + i)
    for i in range(8): pine(mb, M, rr.uniform(40, 70), rr.uniform(30, 55), rr.uniform(10, 15), 200 + i)
    mb.finish()
    # grass tufts (warm dry) for density
    mb = MB('tufts'); gm = mat('tuft', '#a8a040', '#c8b85a', 6, zgrad=(0, 0.4, '#6a8a30'))
    for i in range(420):
        x, y = rr.uniform(-14, 22), rr.uniform(-5, 22)
        if rr.random() < 0.5: x, y = rr.uniform(-9, 0), rr.uniform(-3, 5)
        if abs(x) < 6 and -2 < y < 12: continue
        if y > 16 - 0.0 and (x * x + (y + 30) ** 2) > 46 ** 2: continue
        if (x * x + (y + 30) ** 2) > 46 ** 2 and (x * x + (y + 30) ** 2) < 54 ** 2: continue
        for k in range(5):
            a = rr.random() * 6.28; Lh = rr.uniform(0.2, 0.5); d = Vector((math.cos(a), math.sin(a), 0)); sd = Vector((-d.y, d.x, 0)) * 0.012
            p0 = Vector((x + rr.uniform(-.06, .06), y + rr.uniform(-.06, .06), 0)); p2 = p0 + d * 0.12 + Vector((0, 0, Lh))
            mb.tri(gm, [p0 - sd, p0 + sd, p2])
    mb.finish()
    return M

# ------------------------------------------------------------------ SCENE B: Mexico City 1968
SX, SY = 0.0, 8.0        # bowl centre
def ell_pt(a, b, t): return (SX + a * math.cos(t), SY + b * math.sin(t))
NROW = 28; RW = 0.9; RISE = 0.72; A0 = 64.0; B0 = 36.0
def build_b(P):
    sc = bpy.context.scene; M = pal(); rr = rnd(68)
    sky2(P); ridges(P)
    plane(M['lawn'], 700, -0.02)
    mb = MB('apron')
    ring(mb, M['tartan'], SX, SY, 50, 22, 62, 34, 0, 360, 0.012, 2.0)
    for k in range(9):
        o = 50 + k * 12 / 8.0 if False else 50 + (k + 0.0) * 1.5
        ring(mb, M['chalk'], SX, SY, o, o - 28, o + 0.07, o - 28 + 0.07, 0, 360, 0.02, 2.0)
    ring(mb, M['chalk'], SX, SY, 61.85, 33.85, 62.0, 34.0, 0, 360, 0.022, 2.0)
    ring(mb, M['concrete2'], SX, SY, 62, 34, 64, 36, 0, 360, 0.01, 2.0)
    # tartan run-up fan + landing area in the infield
    disc(mb, M['tartan'], (0.0, 8.0), 9.0, 0.011, 48, 10.5); ring(mb, M['chalk'], 0.0, 8.0, 8.9, 8.9 * 0.857, 9.05, 9.05 * 0.857, 0, 360, 0.02, 3.0) if False else None
    mb.finish()
    # --- stand: treads, risers, rim wall
    mb = MB('stands'); steps = 2.0
    for i in range(NROW):
        a = A0 + i * RW; b = B0 + i * RW; z = 1.0 + i * RISE
        ring(mb, M['concrete'] if i % 2 == 0 else M['concrete2'], SX, SY, a, b, a + RW, b + RW, 0, 360, z, steps)
        n = int(360 / steps)
        for j in range(n):
            u0 = math.radians(j * steps); u1 = math.radians((j + 1) * steps)
            p0 = ell_pt(a, b, u0); p1 = ell_pt(a, b, u1)
            mb.quad(M['concrete2'] if i % 2 == 0 else M['concrete'], [(p0[0], p0[1], z - RISE), (p1[0], p1[1], z - RISE), (p1[0], p1[1], z), (p0[0], p0[1], z)])
    ao = A0 + NROW * RW; bo = B0 + NROW * RW; zt = 1.0 + NROW * RISE
    for j in range(180):
        u0 = math.radians(j * 2); u1 = math.radians(j * 2 + 2); p0 = ell_pt(ao, bo, u0); p1 = ell_pt(ao, bo, u1)
        mb.quad(M['concrete'], [(p0[0], p0[1], -1), (p1[0], p1[1], -1), (p1[0], p1[1], zt + 1.0), (p0[0], p0[1], zt + 1.0)])
        p0 = ell_pt(A0 - 0.5, B0 - 0.5, u0); p1 = ell_pt(A0 - 0.5, B0 - 0.5, u1)
        mb.quad(M['wood'] if False else M['rust'], [(p0[0], p0[1], 0), (p1[0], p1[1], 0), (p1[0], p1[1], 1.0), (p0[0], p0[1], 1.0)])
    for j in range(180):
        u0 = math.radians(j * 2 + 180); u1 = math.radians(j * 2 + 182); p0 = ell_pt(ao, bo, u0); p1 = ell_pt(ao, bo, u1)
        mb.quad(M['concrete'], [(p0[0], p0[1], -1), (p1[0], p1[1], -1), (p1[0], p1[1], zt + 1.0), (p0[0], p0[1], zt + 1.0)])
        p0 = ell_pt(A0 - 0.5, B0 - 0.5, u0); p1 = ell_pt(A0 - 0.5, B0 - 0.5, u1)
        mb.quad(M['rust'], [(p0[0], p0[1], 0), (p1[0], p1[1], 0), (p1[0], p1[1], 1.0), (p0[0], p0[1], 1.0)])
    mb.finish()
    # --- crowd: dense coloured blocks + heads
    cm = crowd_mats(); skins = [M['skin1'], M['skin2'], M['hair'], M['skin1']]
    mbs = [MB('crowd%d' % k) for k in range(len(cm))]; mh = MB('heads')
    cnt = 0
    for i in range(NROW):
        a = A0 + i * RW + 0.55; b = B0 + i * RW + 0.55; z = 1.0 + i * RISE
        t = math.radians(8.0)
        while t < math.radians(172.0):
            s = math.sqrt((a * math.sin(t)) ** 2 + (b * math.cos(t)) ** 2); t += 0.52 / s
            if rr.random() > 0.9: continue
            if (int(math.degrees(t) / 0.9) % 14) == 0: continue    # aisle gaps
            x, y = ell_pt(a, b, t); yaw = math.atan2(-math.sin(t) / b, -math.cos(t) / a) + math.pi
            ci = rr.randrange(len(cm)); h = rr.uniform(0.5, 0.66)
            mbs[ci].box(cm[ci], (x, y, z + h / 2), (0.3, 0.46, h), rz=yaw + math.pi)
            mh.ell(skins[rr.randrange(4)], (x - math.cos(yaw) * 0.0, y, z + h + 0.1), (0.1, 0.1, 0.11), (6, 4)); cnt += 1
    for m_ in mbs: m_.finish()
    mh.finish(); print('crowd', cnt)
    # --- flags on poles along the rim
    mb = MB('rimflags'); fc = [['red', 'cream', 'green'], ['blue', 'cream', 'red'], ['yellow', 'red', 'navy'], ['cream', 'blue', 'cream'], ['orange', 'cream', 'teal'], ['green', 'yellow', 'red'], ['navy', 'cream', 'orange'], ['red', 'yellow', 'green']]
    k = 0
    for d in range(14, 167, 5):
        u = math.radians(d); x, y = ell_pt(ao - 0.6, bo - 0.6, u)
        flagpole(mb, M, x, y, zt + 1.0, 4.6, fc[k % len(fc)], u + 1.5708 + 0.3 * math.sin(k), k * 0.8); k += 1
    mb.finish()
    # --- cauldron tower on the rim (+ glow)
    cu = math.radians(P['cauldron_t']); cxp, cyp = ell_pt(ao - 2.5, bo - 2.5, cu)
    mb = MB('cauldron')
    mb.box(M['concrete'], (cxp, cyp, zt / 2 + 3.5), (5.0, 5.0, zt + 7)); mb.box(M['concrete2'], (cxp, cyp, zt + 7.3), (5.8, 5.8, 0.6))
    mb.rod(M['steel'], (cxp, cyp, zt + 7.6), (cxp, cyp, zt + 9.0), 1.0, 0.8, 14); mb.cone(M['steel'], (cxp, cyp, zt + 9.0), 1.0, 2.6, 1.5, 18); mb.rod(M['rust'], (cxp, cyp, zt + 10.45), (cxp, cyp, zt + 10.6), 2.7, 2.7, 18)
    mb.cone(M['flame'], (cxp, cyp, zt + 10.5), 2.0, 0.1, 4.5, 12); mb.cone(M['flame2'], (cxp, cyp, zt + 10.5), 1.2, 0.05, 3.2, 12); mb.cone(M['flame'], (cxp + 0.8, cyp, zt + 10.5), 0.9, 0.05, 3.7, 8)
    for i in range(14):
        a = i / 14 * 6.283; mb.ell(M['ember'], (cxp + math.cos(a) * 1.9, cyp + math.sin(a) * 1.9, zt + 10.6), (0.12, 0.12, 0.08), (6, 4))
    mb.finish()
    # --- floodlight towers
    mb = MB('flood')
    for tdeg in P['towers']:
        u = math.radians(tdeg); x, y = ell_pt(ao + 9, bo + 9, u); H_ = 38.0
        n_ = (math.cos(u) / (ao), math.sin(u) / (bo)); nn = math.hypot(*n_); nx, ny = n_[0] / nn, n_[1] / nn
        for sx, sy in ((-0.7, -0.7), (0.7, -0.7), (-0.7, 0.7), (0.7, 0.7)):
            mb.rod(M['steel'], (x + sx * 1.3, y + sy * 1.3, 0), (x + sx * 0.5, y + sy * 0.5, H_), 0.16, 0.1, 6)
        for hz in range(3, 38, 6): mb.rod(M['steel'], (x - 0.9, y - 0.9, hz), (x + 0.8, y + 0.8, hz), 0.05, 0.05, 4)
        # lamp panel facing the pitch
        yaw = math.atan2(-ny, -nx)
        mb.push(Matrix.Translation((x, y, H_ + 2.0)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
        mb.box(M['dark'], (0, 0, 0), (0.5, 9.0, 5.6))
        for iy in range(7):
            for iz in range(4): mb.box(M['lamp'], (0.3, -3.9 + iy * 1.3, -2.1 + iz * 1.4), (0.12, 1.0, 1.0))
        mb.pop()
    mb.finish()
    # --- jump set: foam pit, standards, bar
    mb = MB('jump'); px, py = 0.0, 15.0
    for L_, (z0, z1) in enumerate([(0.0, 0.35), (0.35, 0.7)]):
        ox = 0.0 if L_ == 0 else 0.0
        for gx_ in range(4):
            for gy_ in range(3):
                x0 = px - 3.2 + gx_ * 1.6 + 0.01; y0 = py - 2.7 + gy_ * 1.8 + 0.01
                mb.box(M['foam'] if (gx_ + gy_ + L_) % 2 == 0 else M['foamdk'], (x0 + 0.79, y0 + 0.89, (z0 + z1) / 2), (1.58, 1.78, z1 - z0 - 0.01))
    mb.box(M['foamtop'], (px, py, 0.82), (6.3, 5.3, 0.2)); mb.box(M['foam'], (px, py - 2.65, 0.78), (6.4, 0.12, 0.28)); mb.box(M['foam'], (px, py + 2.65, 0.78), (6.4, 0.12, 0.28))
    for sx in (-3.15, 3.15): mb.box(M['foam'], (px + sx, py, 0.78), (0.12, 5.4, 0.28))
    for sx in (-1.5, 0.0, 1.5): mb.box(M['foamdk'], (px + sx, py, 0.935), (0.05, 5.3, 0.012))
    standards(mb, M, 0.0, 11.6, 2.1, 2.24, 'steel', 2.9)
    mb.finish()
    mb = MB('fgprops')
    fx, fy, _ = ground_pt(P, -0.62, -0.52); hurdle(mb, M, (fx, fy, 0.0), 0.7, 0.0)
    fx, fy, _ = ground_pt(P, 0.55, -0.6); bag(mb, M, (fx, fy, 0.0), 0.6, 'orange', 0.9)
    fx, fy, _ = ground_pt(P, 0.0, -0.45); cone_t(mb, M, (fx, fy, 0.0))
    for (u, v, yw, mt) in [(-0.2, -0.62, 1.0, 'red'), (0.25, -0.5, 2.3, 'blue'), (-0.75, -0.3, 0.4, 'teal'), (0.8, -0.4, 1.7, 'cream')]:
        fx, fy, _ = ground_pt(P, u, v); bag(mb, M, (fx, fy, 0.0), yw, mt, 0.7)
    for (u, v, yw) in [(-0.45, -0.38, 0.2), (0.62, -0.28, 2.6)]:
        fx, fy, _ = ground_pt(P, u, v); jacket(mb, M, (fx, fy, 0.0), yw, 'orange', 1.4)
    mb.finish(); mb = MB('officials')
    # --- officials' table + props
    tx, ty = 9.0, 5.0
    mb.push(Matrix.Translation((tx, ty, 0)) @ Euler((0, 0, 0.5)).to_matrix().to_4x4())
    mb.box(M['woodpale'], (0, 0, 0.74), (2.4, 0.9, 0.06)); mb.box(M['cloth'], (0, -0.3, 0.55), (2.45, 0.02, 0.45)); mb.box(M['cloth'], (0, 0.0, 0.78), (2.2, 0.8, 0.012))
    for sx in (-1.1, 1.1):
        for sy in (-0.38, 0.38): mb.rod(M['wood'], (sx, sy, 0), (sx, sy, 0.72), 0.03, 0.03, 6)
    mb.rod(M['metal'], (0.6, 0.1, 0.78), (0.6, 0.1, 1.25), 0.01, 0.01, 5); mb.tri(M['red'], [(0.6, 0.1, 1.25), (0.6, 0.1, 1.08), (0.95, 0.1, 1.16)])
    mb.box(M['wood'], (-0.3, 0.1, 0.81), (0.3, 0.22, 0.012)); mb.box(M['cream'], (-0.3, 0.1, 0.82), (0.26, 0.19, 0.004))
    mb.box(M['dark'], (-0.9, 0.0, 0.8), (0.12, 0.12, 0.05)); mb.rod(M['yellow'], (0.1, 0.2, 0.8), (0.3, 0.2, 0.8), 0.01, 0.01, 4)
    mb.pop()
    for (dx, dy, yw) in [(-0.9, 1.0, 3.6), (0.0, 1.2, 3.7), (0.9, 1.1, 3.55)]:
        c = Vector((tx, ty)) + Vector((dx * math.cos(0.5) - dy * math.sin(0.5), dx * math.sin(0.5) + dy * math.cos(0.5))); chair(mb, M, (c.x, c.y, 0), yw)
    # measuring stick & bar-carrier, bags, tripod + camera
    mb.rod(M['wood'], (5.5, 9.5, 0), (5.5, 9.5, 2.6), 0.02, 0.02, 5); mb.box(M['yellow'], (5.5, 9.5, 2.3), (0.04, 0.04, 0.5))
    bag(mb, M, (-5.5, 7.0, 0.0), 0.8, 'red', 0.9); bag(mb, M, (-4.8, 7.8, 0.0), 0.3, 'navy', 0.7); bag(mb, M, (6.0, 12.5, 0.0), 1.3, 'teal', 0.8)
    for (x, y, yw, mt) in [(-5.0, 6.2, 0.4, 'orange'), (6.8, 7.6, 2.0, 'cream'), (-6.2, 9.3, 1.1, 'blue')]: jacket(mb, M, (x, y, 0.0), yw, mt, 1.3)
    for (x, y) in [(-7.3, 3.0), (-6.3, 2.6), (7.6, 9.0), (-3.4, 11.5)]: bottle(mb, M, (x, y, 0.0), 'yellow')
    for k in range(4): hurdle(mb, M, (-9.4, 6.0 + k * 0.28, 0.0), 0.2) if False else None
    for (x, y) in [(-3.6, 9.4), (3.8, 9.6), (-4.2, 21.5), (4.6, 20.8)]: cone_t(mb, M, (x, y, 0.0))
    # tripods with camera boxes along the track edge
    for (x, y) in [(-14.0, 20.0), (17.0, 24.0), (-22.0, 24.0), (28.0, 26.0)]:
        for a in (0, 2.1, 4.2): mb.rod(M['metal'], (x, y, 1.4), (x + math.cos(a) * 0.5, y + math.sin(a) * 0.5, 0), 0.015, 0.015, 4)
        mb.box(M['dark'], (x, y, 1.5), (0.35, 0.2, 0.2)); mb.rod(M['steel'], (x + 0.2, y + 0.0, 1.5), (x + 0.55, y, 1.5), 0.06, 0.08, 8)
    # blank hoarding boards (no lettering) around the apron and a bunch of towels/stools
    mb2 = MB('hoard')
    hc = ['orange', 'cream', 'blue', 'red', 'yellow', 'teal']
    k = 0
    for d in range(20, 162, 3):
        u = math.radians(d); x, y = ell_pt(61.4, 33.4, u); nn = math.atan2(math.sin(u) / 33.4, math.cos(u) / 61.4)
        mb2.box(M[hc[k % 6]], (x, y, 0.55), (0.12, 3.0, 1.1), rz=nn) if False else mb2.box(M[hc[k % 6]], (x, y, 0.55), (0.14, 3.0, 1.1), rz=nn); k += 1
    mb2.finish(); mb.finish()
    # photographers / bags along the track inner kerb
    mb = MB('kit')
    for i in range(22):
        u = math.radians(rr.uniform(35, 150)); x, y = ell_pt(49.2, 21.2, u)
        mt = rr.choice(['blue', 'red', 'orange', 'cream', 'green', 'yellow', 'navy']); bag(mb, M, (x, y, 0), rr.random() * 6, mt, rr.uniform(0.5, 0.9)) if rr.random() < 0.6 else chair(mb, M, (x, y, 0), rr.random() * 6)
    mb.finish()
    # a few hurdles/kit near the pit for life
    mb = MB('kit2'); wheelbarrow(mb, M, (-7.5, 14.0, 0.0), 0.4); tape_reel(mb, M, (-1.8, 9.2, 0.0), 0.3); rake(mb, M, (3.6, 18.3, 0.0), (3.2, 18.0, 0.95))
    mb.finish()
    return M

# ------------------------------------------------------------------ lights + camera + presets
def kdir(az, el):
    a = math.radians(az); e = math.radians(el)
    return (-math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), -math.sin(e))

PRESETS = {
 'a': dict(name='a', scene='a', cx=0, cy=0,
    sky=[(0.0, '#7a70e0'), (0.40, '#f2b47a'), (0.5, '#f8cf96'), (0.56, '#d8d0c8'), (0.64, '#8aa0ec'), (0.8, '#5c6ee6'), (1.0, '#4a58d8')], sky_k=1.25, glow=('#ffa860', 0.35, 0.45),
    key=(1.0, 0.72, 0.42, 4.6), key_dir=kdir(-52, 22), sun_angle=0.9, exposure=-0.1,
    hills=[(300, 6, 14, '#a08ac8'), (340, 20, 28, '#8f90d0')], hill_k=0.95,
    cam=dict(loc=(-4.4, -0.8, 1.45), look=(1.6, 10.0, 0.0), lens=22), file='sb1_track_golden'),
 'b': dict(name='b', scene='b', cx=0, cy=8, towers=[20, 62, 118, 160], cauldron_t=104,
    sky=[(0.0, '#2a3494'), (0.4, '#5a68c4'), (0.5, '#f2a068'), (0.53, '#e6c0a0'), (0.58, '#a4b8e4'), (0.68, '#4a62c0'), (0.82, '#2a3a9c'), (1.0, '#212a82')], sky_k=1.15, glow=('#ffb050', 0.6, 0.7),
    key=(1.0, 0.64, 0.34, 4.4), key_dir=kdir(-48, 19), sun_angle=1.0, exposure=-0.05,
    hills=[(420, 20, 30, '#6a60b8'), (480, 40, 40, '#5a58b0')], hill_k=0.9,
    cam=dict(loc=(4.2, 3.2, 1.2), look=(-0.8, 15.0, 3.4), lens=22), file='sb2_stadium_evening'),
 'c': dict(name='c', scene='b', cx=0, cy=8, towers=[20, 62, 118, 160], cauldron_t=104,
    sky=[(0.0, '#2a3494'), (0.4, '#5a68c4'), (0.5, '#f2a068'), (0.53, '#e6c0a0'), (0.58, '#a4b8e4'), (0.68, '#4a62c0'), (0.82, '#2a3a9c'), (1.0, '#212a82')], sky_k=1.15, glow=('#ffb050', 0.6, 0.7),
    key=(1.0, 0.62, 0.32, 4.4), key_dir=kdir(-62, 15), sun_angle=1.0, exposure=-0.05,
    hills=[(420, 20, 30, '#6a60b8'), (480, 40, 40, '#5a58b0')], hill_k=0.9,
    cam=dict(loc=(-3.4, 9.6, 0.5), look=(0.6, 13.0, 3.6), lens=22), file='sb3_bar_low'),
}

def add_key(P):
    sc = bpy.context.scene; k = P['key']; kd = Vector(P['key_dir']).normalized()
    d = bpy.data.lights.new('key', 'SUN'); d.color = k[:3]; d.energy = k[3]; d.angle = math.radians(P['sun_angle'])
    o = bpy.data.objects.new('key', d); sc.collection.objects.link(o); o.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler()

def setup_camera(P):
    sc = bpy.context.scene; c = P['cam']
    cd = bpy.data.cameras.new('cam'); cd.lens = c['lens']; cd.sensor_width = 36; cd.sensor_fit = 'AUTO'; cd.dof.use_dof = False
    ob = bpy.data.objects.new('cam', cd); sc.collection.objects.link(ob); ob.location = c['loc']
    ob.rotation_euler = (Vector(c['look']) - Vector(c['loc'])).to_track_quat('-Z', 'Y').to_euler(); sc.camera = ob

def render(P, out, samples, draft):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; cy = sc.cycles; cy.device = 'CPU'; cy.samples = samples; cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'
    cy.denoising_input_passes = 'RGB_ALBEDO_NORMAL'; cy.max_bounces = 3; cy.diffuse_bounces = 2; cy.glossy_bounces = 1; cy.transmission_bounces = 0; cy.transparent_max_bounces = 4
    cy.use_light_tree = True; cy.filter_width = 1.2
    sc.render.threads = 4
    sc.render.resolution_x = W // (2 if draft else 1); sc.render.resolution_y = H // (2 if draft else 1); sc.render.resolution_percentage = 100
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = P.get('exposure', 0.0)
    sc.render.image_settings.file_format = 'PNG'; sc.render.filepath = out + '.png'
    bpy.ops.render.render(write_still=True)
    im = Image.open(out + '.png').convert('RGB')
    a = np.asarray(im, dtype=np.float32) / 255.0; g = a.mean(-1, keepdims=True); a = np.clip(g + (a - g) * P.get('sat', 1.12), 0, 1)
    Image.fromarray((a * 255 + 0.5).astype(np.uint8)).save(out + '.jpg', quality=93); os.remove(out + '.png')

def run(mode, draft=False):
    t = time.time(); bpy.ops.wm.read_factory_settings(use_empty=True)
    for o in list(bpy.data.objects): bpy.data.objects.remove(o)
    MATS.clear(); P = PRESETS[mode]
    (build_a if P['scene'] == 'a' else build_b)(P)
    add_key(P); setup_camera(P)
    out = os.path.join(HERE, ('d_' if draft else '') + P['file'])
    render(P, out, 16 if draft else P.get('samples', 24), draft); print(mode, 'done %.0fs' % (time.time() - t))

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != 'draft']; draft = 'draft' in sys.argv
    for m in (['a', 'b', 'c'] if (not args or args[0] == 'all') else args): run(m, draft)

"""R9 quality test: Cycles scene for the 10 s snowy-forest clip.

Usage: python r9_scene.py SHOT START END OUTDIR [RES_PCT] [SAMPLES]
  SHOT in {a, b, c}.  Global timeline: a = 1-90, b = 91-210, c = 211-300.
Run with the bpy wheel (pip install bpy==5.2.5).
"""
import sys, os, math, random
import numpy as np
import bpy
from mathutils import Vector, Quaternion, Matrix, Euler

SHOT, F0, F1, OUT = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
RES = int(sys.argv[5]) if len(sys.argv) > 5 else 100
SPP = int(sys.argv[6]) if len(sys.argv) > 6 else 96
FPS = 30
rng = random.Random(7)

bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene
COL = scn.collection


# ---------------------------------------------------------------- terrain
def H(x, y):
    """Snow height field (numpy or scalar)."""
    x = np.asarray(x, dtype=float); y = np.asarray(y, dtype=float)
    h = (0.16 * np.sin(0.55 * x + 0.3 * y) * np.cos(0.42 * y - 0.25 * x)
         + 0.07 * np.sin(1.6 * x + 1.1 * y + 1.0)
         + 0.35 * np.sin(0.11 * x + 0.5) * np.cos(0.09 * y))
    def ss(a, b, v):
        t = np.clip((v - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)
    h = h - 22 * ss(26, 120, x) + 48 * ss(190, 390, x) + 6 * ss(60, 200, np.abs(y)) * ss(30, 90, x)
    return h


def mk_obj(name, verts, faces, mats=None, smooth=True, mat_idx=None, parent=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], [], [tuple(f) for f in faces])
    me.update()
    if smooth:
        me.polygons.foreach_set('use_smooth', [True] * len(me.polygons))
    for m in (mats or []):
        me.materials.append(m)
    if mat_idx is not None:
        me.polygons.foreach_set('material_index', mat_idx)
    ob = bpy.data.objects.new(name, me)
    COL.objects.link(ob)
    if parent:
        ob.parent = parent
    return ob


def grid(x0, x1, y0, y1, step, zfun):
    xs = np.arange(x0, x1 + 1e-6, step); ys = np.arange(y0, y1 + 1e-6, step)
    X, Y = np.meshgrid(xs, ys)
    Z = zfun(X, Y)
    verts = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1)
    nx, ny = len(xs), len(ys)
    i = np.arange(nx - 1); j = np.arange(ny - 1)
    I, J = np.meshgrid(i, j)
    a = (J * nx + I).ravel()
    faces = np.stack([a, a + 1, a + nx + 1, a + nx], 1)
    return verts, faces, xs, ys


# ---------------------------------------------------------------- node helpers
def mat(name):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != 'OUTPUT_MATERIAL':
            nt.nodes.remove(n)
    return m, nt


def N(nt, kind, **kw):
    n = nt.nodes.new(kind)
    for k, v in kw.items():
        setattr(n, k, v)
    return n


def L(nt, a, b):
    nt.links.new(a, b)


def sock(node, name, typ=None, out=False):
    for s in (node.outputs if out else node.inputs):
        if s.name == name and (typ is None or s.type == typ):
            return s
    raise KeyError(name)


def mixcol(nt, fac, a, b):
    m = N(nt, 'ShaderNodeMix', data_type='RGBA')
    for s, v in ((sock(m, 'Factor', 'VALUE'), fac), (sock(m, 'A', 'RGBA'), a), (sock(m, 'B', 'RGBA'), b)):
        if isinstance(v, bpy.types.NodeSocket):
            L(nt, v, s)
        else:
            s.default_value = v
    return sock(m, 'Result', 'RGBA', out=True)


def mth(nt, op, a, b=0.0):
    m = N(nt, 'ShaderNodeMath', operation=op)
    for s, v in ((m.inputs[0], a), (m.inputs[1], b)):
        if isinstance(v, bpy.types.NodeSocket):
            L(nt, v, s)
        else:
            s.default_value = v
    return m.outputs[0]


def principled(nt, color, rough=0.5, metal=0.0, **kw):
    p = N(nt, 'ShaderNodeBsdfPrincipled')
    if isinstance(color, bpy.types.NodeSocket):
        L(nt, color, p.inputs['Base Color'])
    else:
        p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    for k, v in kw.items():
        p.inputs[k].default_value = v
    return p


def out(nt, shader):
    o = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]
    L(nt, shader if isinstance(shader, bpy.types.NodeSocket) else shader.outputs[0], o.inputs['Surface'])


def bump(nt, height, strength, dist=0.02):
    b = N(nt, 'ShaderNodeBump')
    b.inputs['Strength'].default_value = strength
    b.inputs['Distance'].default_value = dist
    L(nt, height, b.inputs['Height'])
    return b.outputs['Normal']


def noise(nt, scale, detail=4, coords='Object', rough=0.55):
    tc = N(nt, 'ShaderNodeTexCoord')
    n = N(nt, 'ShaderNodeTexNoise')
    n.inputs['Scale'].default_value = scale
    n.inputs['Detail'].default_value = detail
    n.inputs['Roughness'].default_value = rough
    L(nt, tc.outputs[coords], n.inputs['Vector'])
    return n.outputs['Fac']


def srgb(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c)


# ---------------------------------------------------------------- materials
def snow_mat(name, sparkle=True, scale=1.0, sss=0.0):
    m, nt = mat(name)
    tc = N(nt, 'ShaderNodeTexCoord')
    n1 = noise(nt, 3.0 * scale, 6, 'Object')
    n2 = noise(nt, 35.0 * scale, 3, 'Object')
    h = mth(nt, 'ADD', mth(nt, 'MULTIPLY', n1, 0.6), mth(nt, 'MULTIPLY', n2, 0.25))
    nrm = bump(nt, h, 0.2, 0.02)
    tint = mixcol(nt, n1, (*srgb('#eef3fb'), 1), (*srgb('#f8f6f4'), 1))
    p = principled(nt, tint, 0.55)
    p.inputs['Subsurface Weight'].default_value = sss
    p.inputs['Subsurface Radius'].default_value = (0.35, 0.6, 1.0)
    p.inputs['Subsurface Scale'].default_value = 0.04
    L(nt, nrm, p.inputs['Normal'])
    shader = p.outputs[0]
    if sparkle:  # tiny mirror facets -> glints that catch the sun and bloom
        v = N(nt, 'ShaderNodeTexVoronoi')
        v.inputs['Scale'].default_value = 900 * scale
        L(nt, tc.outputs['Object'], v.inputs['Vector'])
        mask = mth(nt, 'LESS_THAN', v.outputs['Distance'], 0.07)
        vn = N(nt, 'ShaderNodeVectorMath', operation='MULTIPLY_ADD')
        L(nt, v.outputs['Color'], vn.inputs[0]); vn.inputs[1].default_value = (2, 2, 2); vn.inputs[2].default_value = (-1, -1, 0.2)
        vnn = N(nt, 'ShaderNodeVectorMath', operation='NORMALIZE'); L(nt, vn.outputs[0], vnn.inputs[0])
        g = N(nt, 'ShaderNodeBsdfGlossy'); g.inputs['Roughness'].default_value = 0.04
        L(nt, vnn.outputs[0], g.inputs['Normal'])
        mx = N(nt, 'ShaderNodeMixShader')
        L(nt, mth(nt, 'MULTIPLY', mask, 0.9), mx.inputs[0]); L(nt, shader, mx.inputs[1]); L(nt, g.outputs[0], mx.inputs[2])
        shader = mx.outputs[0]
    out(nt, shader)
    return m


SNOW = snow_mat('snow')
SNOW_TREE = snow_mat('snow_tree', sparkle=False, scale=1.5)
SNOW_SSS = snow_mat('snow_sss', sparkle=False, scale=8.0, sss=0.4)


def simple(name, hexcol, rough=0.6, metal=0.0, bumpscale=0.0, bumpstr=0.2, **kw):
    m, nt = mat(name)
    p = principled(nt, srgb(hexcol), rough, metal, **kw)
    if bumpscale:
        L(nt, bump(nt, noise(nt, bumpscale, 5), bumpstr, 0.01), p.inputs['Normal'])
    out(nt, p)
    return m


NEEDLE = None
m, nt = mat('needles')
nf = noise(nt, 6, 5)
col = mixcol(nt, nf, (*srgb('#173d36'), 1), (*srgb('#2b5e4f'), 1))
p = principled(nt, col, 0.75)
L(nt, bump(nt, noise(nt, 60, 3), 0.6, 0.03), p.inputs['Normal'])
out(nt, p)
NEEDLE = m
BARK = simple('bark', '#6a3424', 0.85, bumpscale=25, bumpstr=0.6)
COAT = simple('coat', '#6a5232', 0.8, bumpscale=180, bumpstr=0.25, **{'Sheen Weight': 0.4})
LEATHER = simple('leather', '#3b2618', 0.45)
INK = simple('limb', '#2a2024', 0.5)
BRASS = simple('brass', '#d9a64e', 0.22, 1.0, bumpscale=300, bumpstr=0.03)
STEEL = simple('steel', '#2e3238', 0.32, 1.0)
WOOD = None
m, nt = mat('wood')
tc = N(nt, 'ShaderNodeTexCoord')
w = N(nt, 'ShaderNodeTexWave'); w.inputs['Scale'].default_value = 6; w.inputs['Distortion'].default_value = 6
w.wave_type = 'BANDS'; w.bands_direction = 'X'
L(nt, tc.outputs['Object'], w.inputs['Vector'])
col = mixcol(nt, w.outputs['Fac'], (*srgb('#8c4a22'), 1), (*srgb('#a65f2c'), 1))
p = principled(nt, col, 0.32, **{'Coat Weight': 0.3})
out(nt, p)
WOOD = m
FUR = None
m, nt = mat('fur')
fn = noise(nt, 140, 8, rough=0.75)
col = mixcol(nt, fn, (*srgb('#a6845a'), 1), (*srgb('#d8bf94'), 1))
p = principled(nt, col, 0.9, **{'Sheen Weight': 1.0})
L(nt, bump(nt, fn, 1.0, 0.012), p.inputs['Normal'])
out(nt, p)
FUR = m


def face_texture(path):
    from PIL import Image, ImageDraw
    S = 512
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ink = (58, 40, 50, 255)
    for cx in (S * 0.37, S * 0.63):                 # half-lidded, steady eyes
        d.ellipse([cx - 20, S * 0.47 - 15, cx + 20, S * 0.47 + 15], fill=ink)
        d.rectangle([cx - 24, S * 0.47 - 20, cx + 24, S * 0.47 - 3], fill=(0, 0, 0, 0))
        d.line([cx - 24, S * 0.47 - 3, cx + 24, S * 0.47 - 3], fill=ink, width=7)
    d.line([S * 0.30, S * 0.36, S * 0.42, S * 0.385], fill=ink, width=7)   # brows
    d.line([S * 0.58, S * 0.385, S * 0.70, S * 0.36], fill=ink, width=7)
    d.arc([S * 0.46, S * 0.56, S * 0.62, S * 0.66], 15, 150, fill=ink, width=7)  # small smirk
    im.save(path)


def head_mat(tex_path, r):
    m, nt = mat('head')
    tc = N(nt, 'ShaderNodeTexCoord')
    sep = N(nt, 'ShaderNodeSeparateXYZ'); L(nt, tc.outputs['Object'], sep.inputs[0])
    u = mth(nt, 'MULTIPLY_ADD', sep.outputs['X'], 0.5 / r); u.node.inputs[2].default_value = 0.5
    v = mth(nt, 'MULTIPLY_ADD', sep.outputs['Z'], 0.5 / r); v.node.inputs[2].default_value = 0.5
    cmb = N(nt, 'ShaderNodeCombineXYZ'); L(nt, u, cmb.inputs[0]); L(nt, v, cmb.inputs[1])
    img = N(nt, 'ShaderNodeTexImage'); img.image = bpy.data.images.load(tex_path); img.extension = 'CLIP'
    L(nt, cmb.outputs[0], img.inputs['Vector'])
    front = mth(nt, 'LESS_THAN', sep.outputs['Y'], 0.0)
    fac = mth(nt, 'MULTIPLY', img.outputs['Alpha'], front)
    col = mixcol(nt, fac, (*srgb('#fef7f6'), 1), (*srgb('#3a2832'), 1))
    p = principled(nt, col, 0.45)
    p.inputs['Subsurface Weight'].default_value = 0.15
    p.inputs['Subsurface Radius'].default_value = (1.0, 0.6, 0.5)
    p.inputs['Subsurface Scale'].default_value = 0.02
    out(nt, p)
    return m


# ---------------------------------------------------------------- geometry helpers
def lathe(name, prof, segs=48, mats=None, parent=None, cap=True):
    """prof: list of (r, z) from bottom to top."""
    verts, faces = [], []
    for r, z in prof:
        for k in range(segs):
            a = 2 * math_pi * k / segs
            verts.append((r * math.cos(a), r * math.sin(a), z))
    for i in range(len(prof) - 1):
        for k in range(segs):
            a = i * segs + k; b = i * segs + (k + 1) % segs
            faces.append((a, b, b + segs, a + segs))
    if cap:
        nb = len(verts); verts.append((0, 0, prof[0][1]))
        nt_ = len(verts); verts.append((0, 0, prof[-1][1]))
        for k in range(segs):
            faces.append((nb, (k + 1) % segs, k))
            o = (len(prof) - 1) * segs
            faces.append((nt_, o + k, o + (k + 1) % segs))
    return mk_obj(name, verts, faces, mats, parent=parent)


math_pi = math.pi


def capsule_prof(r, z0, z1, n=10):
    p = []
    for i in range(n + 1):
        a = -math.pi / 2 + (math.pi / 2) * i / n
        p.append((max(r * math.cos(a), 1e-4), z0 + r + r * math.sin(a)))
    for i in range(n + 1):
        a = (math.pi / 2) * i / n
        p.append((max(r * math.cos(a), 1e-4), z1 - r + r * math.sin(a)))
    return p


def sphere(name, r, mats, parent=None, segs=48, rings=24):
    prof = [(max(r * math.sin(math.pi * i / rings), 1e-5), -r * math.cos(math.pi * i / rings)) for i in range(rings + 1)]
    return lathe(name, prof, segs, mats, parent)


def box(name, x0, x1, hy, hz, mats, z0=0.0, taper=1.0, parent=None):
    """Box along +X; cross-section +-hy, z0 +- hz, end scaled by taper."""
    v = []
    for x, s in ((x0, 1.0), (x1, taper)):
        for yy, zz in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            v.append((x, yy * hy * s, z0 + zz * hz * s))
    f = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    ob = mk_obj(name, v, f, mats, smooth=False, parent=parent)
    bv = ob.modifiers.new('bev', 'BEVEL'); bv.width = min(hy, hz) * 0.35; bv.segments = 3
    return ob


def cyl_x(name, x0, x1, r, mats, y=0.0, z=0.0, segs=24, parent=None):
    ob = lathe(name, [(r, 0.0), (r, x1 - x0)], segs, mats, parent)
    for vtx in ob.data.vertices:
        X, Y, Z = vtx.co
        vtx.co = (Z + x0, Y + y, -X + z)
    return ob


# ---------------------------------------------------------------- pines
def pine_mesh(seed, height, far=False):
    r_ = random.Random(seed)
    verts, faces, mi = [], [], []
    def add(vs, fs, m):
        o = len(verts); verts.extend(vs); faces.extend([tuple(i + o for i in f) for f in fs]); mi.extend([m] * len(fs))
    # trunk
    seg = 10; tr = height * 0.035
    tv = []
    for z, r in ((-0.3, tr * 1.2), (height * 0.5, tr * 0.8), (height * 0.9, tr * 0.3)):
        for k in range(seg):
            a = 2 * math.pi * k / seg; tv.append((r * math.cos(a), r * math.sin(a), z))
    tf = [(i * seg + k, i * seg + (k + 1) % seg, (i + 1) * seg + (k + 1) % seg, (i + 1) * seg + k) for i in range(2) for k in range(seg)]
    add(tv, tf, 2)
    tiers = r_.randint(5, 7)
    base = height * r_.uniform(0.18, 0.28)
    S = 96
    for t in range(tiers):
        f = t / tiers
        zb = base + (height - base) * f * 0.92
        th = (height - base) / tiers * 1.55
        R = height * 0.36 * (1 - f) ** 0.9 + 0.25
        pts = r_.choice([13, 15, 17]); ph = r_.uniform(0, 6.3)
        rim, mid, top, under = [], [], [], []
        for k in range(S):
            a = 2 * math.pi * k / S
            star = 0.70 + 0.30 * abs(math.cos(pts * a / 2 + ph)) ** 2.5 + r_.uniform(-0.05, 0.05)
            rr = R * star
            droop = -0.16 * th * star + r_.uniform(-0.03, 0.03) * th
            rim.append((rr * math.cos(a), rr * math.sin(a), zb + droop))
            mid.append((0.80 * rr * math.cos(a), 0.80 * rr * math.sin(a), zb + 0.18 * th + 0.05 * th * math.sin(5 * a + ph) + r_.uniform(-0.02, 0.05) * th))
            under.append((0.55 * rr * math.cos(a), 0.55 * rr * math.sin(a), zb + 0.12 * th))
        apex = [(0, 0, zb + th)]
        under_c = [(0, 0, zb + 0.35 * th)]
        vs = rim + mid + under + apex + under_c
        A = 3 * S; U = 3 * S + 1
        fs_snow = [(S + k, S + (k + 1) % S, A) for k in range(S)]
        fs_band = [(k, (k + 1) % S, S + (k + 1) % S, S + k) for k in range(S)]
        fs_under = [((k + 1) % S, k, 2 * S + k, 2 * S + (k + 1) % S) for k in range(S)]
        fs_uc = [(2 * S + (k + 1) % S, 2 * S + k, U) for k in range(S)]
        o = len(verts); verts.extend(vs)
        for fs, m in ((fs_snow, 1), (fs_band, 3), (fs_under, 0), (fs_uc, 0)):
            faces.extend([tuple(i + o for i in f) for f in fs]); mi.extend([m] * len(fs))
    me = bpy.data.meshes.new(f'pine{seed}{far}')
    me.from_pydata(verts, [], faces); me.update()
    me.polygons.foreach_set('use_smooth', [True] * len(me.polygons))
    for mm in (NEEDLE, FAR_TOP if far else SNOW_TREE, BARK, FAR_TOP if far else PINE_BAND):
        me.materials.append(mm)
    me.polygons.foreach_set('material_index', mi)
    return me


# snow pad edge: snow with needles peeking through
m, nt = mat('pine_band')
fac = mth(nt, 'LESS_THAN', noise(nt, 18, 6, rough=0.65), 0.40)
mx = N(nt, 'ShaderNodeMixShader')
p1 = principled(nt, srgb('#f2f5fa'), 0.6)
p1.inputs['Subsurface Radius'].default_value = (0.35, 0.6, 1.0); p1.inputs['Subsurface Scale'].default_value = 0.05
p2 = principled(nt, srgb('#1d4a44'), 0.8)
L(nt, fac, mx.inputs[0]); L(nt, p1.outputs[0], mx.inputs[1]); L(nt, p2.outputs[0], mx.inputs[2])
out(nt, mx)
PINE_BAND = m
m, nt = mat('far_top')
fac = mth(nt, 'GREATER_THAN', noise(nt, 25, 5, rough=0.7), 0.56)
mx = N(nt, 'ShaderNodeMixShader')
p1 = principled(nt, srgb('#173f3a'), 0.85); p2 = principled(nt, srgb('#e9eef6'), 0.6)
L(nt, fac, mx.inputs[0]); L(nt, p1.outputs[0], mx.inputs[1]); L(nt, p2.outputs[0], mx.inputs[2])
out(nt, mx)
FAR_TOP = m

PINES = [pine_mesh(s, 1.0) for s in range(6)]  # unit height, scaled per instance
FAR_PINES = [pine_mesh(s + 10, 1.0, far=True) for s in range(4)]
TREES = []


def place_tree(x, y, h, sink=0.05, far=False):
    lib = FAR_PINES if far else PINES
    ob = bpy.data.objects.new('tree', lib[rng.randrange(len(lib))])
    ob.location = (x, y, float(H(x, y)) - sink * h)
    ob.scale = (h * rng.uniform(0.85, 1.15), h * rng.uniform(0.85, 1.15), h)
    ob.rotation_euler = (rng.uniform(-0.03, 0.03), rng.uniform(-0.03, 0.03), rng.uniform(0, 6.3))
    COL.objects.link(ob); TREES.append(ob)
    return ob


# ---------------------------------------------------------------- world, light, haze
world = bpy.data.worlds.new('sky'); scn.world = world
world.use_nodes = True
wn = world.node_tree
for n in list(wn.nodes):
    if n.type != 'OUTPUT_WORLD':
        wn.nodes.remove(n)
tc = N(wn, 'ShaderNodeTexCoord')
sep = N(wn, 'ShaderNodeSeparateXYZ'); L(wn, tc.outputs['Generated'], sep.inputs[0])
ramp = N(wn, 'ShaderNodeValToRGB')
cr = ramp.color_ramp
cr.elements[0].position = 0.0; cr.elements[0].color = (*srgb('#e9a77f'), 1)
cr.elements[1].position = 0.55; cr.elements[1].color = (*srgb('#2f5bb5'), 1)
e = cr.elements.new(0.08); e.color = (*srgb('#d9a3a6'), 1)
e = cr.elements.new(0.22); e.color = (*srgb('#7d8fd0'), 1)
L(wn, sep.outputs['Z'], ramp.inputs[0])
SUN_GLOW = N(wn, 'ShaderNodeVectorMath', operation='DOT_PRODUCT')
L(wn, tc.outputs['Generated'], SUN_GLOW.inputs[0])
gl = mth(wn, 'POWER', mth(wn, 'MAXIMUM', SUN_GLOW.outputs['Value'], 0.0), 24.0)
glc = mixcol(wn, gl, (0, 0, 0, 1), (4.0, 2.0, 0.8, 1))
add = N(wn, 'ShaderNodeMix', data_type='RGBA', blend_type='ADD')
sock(add, 'Factor', 'VALUE').default_value = 1.0
L(wn, ramp.outputs[0], sock(add, 'A', 'RGBA')); L(wn, glc, sock(add, 'B', 'RGBA'))
bg = N(wn, 'ShaderNodeBackground'); bg.inputs['Strength'].default_value = 0.75
L(wn, sock(add, 'Result', 'RGBA', out=True), bg.inputs['Color'])
L(wn, bg.outputs[0], [n for n in wn.nodes if n.type == 'OUTPUT_WORLD'][0].inputs['Surface'])

sun_d = bpy.data.lights.new('sun', 'SUN')
sun_d.energy = 6.5; sun_d.color = (1.0, 0.60, 0.33); sun_d.angle = math.radians(1.6)
SUN = bpy.data.objects.new('sun', sun_d); COL.objects.link(SUN)


def set_sun(az_vec, elev_deg):
    d = Vector((az_vec[0], az_vec[1], 0)).normalized()
    e = math.radians(elev_deg)
    to_sun = Vector((d.x * math.cos(e), d.y * math.cos(e), math.sin(e)))
    SUN.rotation_euler = (-to_sun).to_track_quat('-Z', 'Y').to_euler()
    SUN_GLOW.inputs[1].default_value = to_sun


def haze(density, center, size):
    if os.environ.get('NOHAZE'): return None
    m, nt = mat('haze')
    o = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]
    v = N(nt, 'ShaderNodeVolumePrincipled')
    v.inputs['Density'].default_value = density
    v.inputs['Anisotropy'].default_value = 0.55
    v.inputs['Color'].default_value = (*srgb('#f1e4e0'), 1)
    L(nt, v.outputs[0], o.inputs['Volume'])
    s = size
    vs = [(center[0] + sx * s[0], center[1] + sy * s[1], center[2] + sz * s[2]) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
    fs = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    ob = mk_obj('haze', vs, fs, [m], smooth=False)
    ob.visible_shadow = False
    return ob


# ---------------------------------------------------------------- terrain meshes
FINE = (-30.0, 30.0, -30.0, 30.0)
STRIP = (-4.0, 3.0, -0.6, 0.6)   # footprint strip (walk path), aligned to the 0.1 m fine grid
v, f, xs, ys = grid(*FINE, 0.1, H)
cx = v[f, 0].mean(1); cy = v[f, 1].mean(1)
keep = ~((cx > STRIP[0]) & (cx < STRIP[1]) & (cy > STRIP[2]) & (cy < STRIP[3]))
mk_obj('ground_fine', v, f[keep], [SNOW])


def coarse_z(X, Y):
    inside = np.clip(np.minimum(29.5 - np.abs(X), 29.5 - np.abs(Y)), 0, 1)
    return H(X, Y) - 0.25 * inside


v, f, _, _ = grid(-300, 900, -700, 700, 4.0, coarse_z)
mk_obj('ground_far', v, f, [SNOW])

# ---------------------------------------------------------------- character walk (shot b)
T_B0 = 91                       # first frame of shot b
V = 0.55                        # m/s walk speed
PER = 1.0                       # gait period (s)
DUTY = 0.6                      # stance fraction
X0 = 0.0                        # root x at shot-b start; walks toward -X
FWD = Vector((-1, 0, 0))
LEFT = Vector((0, -1, 0))       # character's left points at the camera
FOOT_Y = {'L': -0.07, 'R': 0.07}
PHASE = {'L': 0.0, 'R': 0.5}
SINK = 0.028                    # boot sinks into the snow


def root_x(t):
    return X0 - V * t


def foot_state(side, t):
    """returns (x, lift, planted, plant_index) for the foot at time t."""
    c = t / PER - PHASE[side]
    k = math.floor(c); ph = c - k
    def plant_x(kk):
        return root_x((kk + PHASE[side] + DUTY / 2) * PER)
    if ph < DUTY:
        return plant_x(k), 0.0, True, k
    s = (ph - DUTY) / (1 - DUTY)
    e = s * s * (3 - 2 * s)
    x = plant_x(k) + (plant_x(k + 1) - plant_x(k)) * e
    return x, math.sin(math.pi * s), False, k


def plants(side, t_from, t_to):
    out_ = []
    k = math.floor(t_from / PER - PHASE[side]) - 1
    while True:
        ts = (k + PHASE[side]) * PER
        if ts > t_to:
            break
        x = root_x((k + PHASE[side] + DUTY / 2) * PER)
        out_.append((ts, x, FOOT_Y[side]))
        k += 1
    return out_


def dent(X, Y, px, py):
    u = np.sqrt(((X - px) / 0.075) ** 2 + ((Y - py) / 0.045) ** 2)
    return np.where(u < 1, -0.032 * (1 - u * u) ** 1.5, 0) + 0.009 * np.exp(-((u - 1.15) / 0.2) ** 2)


T_END = (210 - T_B0) / FPS
all_plants = [p + (s,) for s in 'LR' for p in plants(s, -6.0, T_END + 0.1)]
old = [p for p in all_plants if p[0] < 0 and p[1] < STRIP[1] - 0.15]
new = [p for p in all_plants if p[0] >= 0]


def strip_z(X, Y):
    Z = H(X, Y)
    # match the 0.1 m grid of the surrounding mesh on the border (no cracks)
    border = (np.isclose(X, STRIP[0]) | np.isclose(X, STRIP[1]) | np.isclose(Y, STRIP[2]) | np.isclose(Y, STRIP[3]))
    gx0 = np.floor(X * 10 + 1e-6) / 10; gy0 = np.floor(Y * 10 + 1e-6) / 10
    fx = (X - gx0) * 10; fy = (Y - gy0) * 10
    lin = ((1 - fx) * (1 - fy) * H(gx0, gy0) + fx * (1 - fy) * H(gx0 + .1, gy0)
           + (1 - fx) * fy * H(gx0, gy0 + .1) + fx * fy * H(gx0 + .1, gy0 + .1))
    Z = np.where(border, lin, Z)
    for (_, px, py, _s) in old:
        Z = Z + np.where(border, 0, dent(X, Y, px, py))
    return Z


v, f, _, _ = grid(*STRIP, 0.02, strip_z)
strip = mk_obj('ground_strip', v, f, [SNOW])
strip.shape_key_add(name='Basis')
for i, (ts, px, py, s) in enumerate(new):
    kb = strip.shape_key_add(name=f'print{i}', from_mix=False)
    X = v[:, 0]; Y = v[:, 1]
    d = dent(X, Y, px, py)
    co = v.copy(); co[:, 2] += d
    kb.data.foreach_set('co', co.ravel())
    fr = T_B0 + ts * FPS
    kb.value = 0.0; kb.keyframe_insert('value', frame=max(1, int(math.floor(fr))))
    kb.value = 1.0; kb.keyframe_insert('value', frame=int(math.floor(fr)) + 1)

# ---------------------------------------------------------------- character
import os, tempfile
face_png = os.path.join(OUT, '_face.png'); os.makedirs(OUT, exist_ok=True)
face_texture(face_png)
HEAD_R = 0.165
ROOT = bpy.data.objects.new('char_root', None); COL.objects.link(ROOT)
ROOT.rotation_mode = 'XYZ'
body = lathe('body', capsule_prof(0.165, -0.07, 0.52), 48, [COAT], ROOT)
lathe('belt', [(0.170, 0.10), (0.172, 0.115), (0.172, 0.135), (0.170, 0.15)], 48, [LEATHER], ROOT)
for z in (0.21, 0.31, 0.41):
    b = sphere('button', 0.012, [BRASS], ROOT, 12, 6); b.location = (0, -0.164, z); b.scale = (1, 0.5, 1)
buck = box('buckle', -0.02, 0.02, 0.008, 0.02, [BRASS], parent=ROOT); buck.location = (0, -0.168, 0.125 - 0.0)
HEADG = bpy.data.objects.new('head_grp', None); COL.objects.link(HEADG); HEADG.parent = ROOT
HEADG.location = (0, 0, 0.64); HEADG.rotation_euler = (0.05, 0, math.radians(42))
head = sphere('head', HEAD_R, [head_mat(face_png, HEAD_R)], HEADG)
hat = lathe('hat', [(0.172, 0.0), (0.18, 0.02), (0.182, 0.09), (0.17, 0.13), (0.12, 0.155), (0.0, 0.16)], 48, [FUR], HEADG)
hat.location = (0, 0, 0.03)
fold = lathe('hat_fold', [(0.178, 0.0), (0.193, 0.015), (0.196, 0.06), (0.184, 0.075)], 48, [FUR], HEADG)
fold.location = (0, 0, 0.025)
for sx in (-1, 1):
    ear = sphere('earflap', 0.07, [FUR], HEADG, 24, 12); ear.location = (sx * 0.165, 0.01, -0.02); ear.scale = (0.45, 1.0, 1.3)
badge = sphere('badge', 0.018, [BRASS], HEADG, 16, 8); badge.location = (0, -0.194, 0.065); badge.scale = (1, 0.35, 1)


def make_rifle(name, parent=None, detail=False):
    grp = bpy.data.objects.new(name, None); COL.objects.link(grp)
    if parent:
        grp.parent = parent
    box(name + '_butt', 0.0, 0.34, 0.022, 0.055, [WOOD], z0=-0.03, taper=0.6, parent=grp)
    box(name + '_wrist', 0.30, 0.42, 0.02, 0.028, [WOOD], z0=-0.01, parent=grp)
    box(name + '_fore', 0.42, 0.98, 0.022, 0.022, [WOOD], z0=-0.004, taper=0.85, parent=grp)
    cyl_x(name + '_recv', 0.38, 0.58, 0.017, [STEEL], z=0.016, parent=grp)
    cyl_x(name + '_barrel', 0.55, 1.24, 0.011, [STEEL], z=0.014, parent=grp)
    for bx in (0.72, 0.93):
        cyl_x(name + '_band', bx, bx + 0.02, 0.027, [STEEL], z=0.0, parent=grp)
    bolt = cyl_x(name + '_bolt', 0.0, 0.07, 0.005, [STEEL], parent=grp)
    bolt.rotation_euler = (0, 0, math.radians(-90)); bolt.location = (0.47, 0.0, 0.02)
    sphere(name + '_knob', 0.011, [STEEL], grp, 16, 8).location = (0.47, -0.07, 0.02)
    # rear sight: block with a notch
    box(name + '_rs_base', 0.56, 0.62, 0.014, 0.010, [STEEL], z0=0.032, parent=grp)
    for sy in (-1, 1):
        box(name + '_rs_ear', 0.60, 0.615, 0.006, 0.012, [STEEL], z0=0.05, parent=grp).location = (0, sy * 0.009, 0)
    # front sight: hooded post with two ears
    box(name + '_fs_base', 1.18, 1.23, 0.012, 0.008, [STEEL], z0=0.03, parent=grp)
    box(name + '_fs_post', 1.205, 1.215, 0.0018, 0.013, [STEEL], z0=0.046, parent=grp)
    for sy in (-1, 1):
        ear = box(name + '_fs_ear', 1.19, 1.225, 0.0035, 0.02, [STEEL], z0=0.05, parent=grp)
        ear.location = (0, sy * 0.014, 0); ear.rotation_euler = (sy * 0.18, 0, 0)
    return grp


RIFLE = make_rifle('rifle', ROOT)
RS = 0.78                                    # rifle scale for the small character
shoulder_L = Vector((0.15, 0.0, 0.37))       # local (x = character's left)
mdir = Vector((0.10, 0.72, 0.62)).normalized()  # muzzle up and back
rq = mdir.to_track_quat('X', 'Z')
RIFLE.rotation_mode = 'QUATERNION'; RIFLE.rotation_quaternion = rq; RIFLE.scale = (RS,) * 3
rest = shoulder_L + Vector((0.055, 0.0, 0.05))
RIFLE.location = rest - mdir * (0.50 * RS)
GRIP_LOCAL = RIFLE.location + mdir * (0.12 * RS) + (rq @ Vector((0, 0, -0.04))) * RS

LIMB_R = 0.017


def limb(name):
    ob = lathe(name, [(LIMB_R, -1.0), (LIMB_R, 0.0)], 12, [INK])
    ob.rotation_mode = 'QUATERNION'
    return ob


def joint(name, r=LIMB_R * 1.05):
    ob = sphere(name, r, [INK], None, 12, 6)
    return ob


boot_me = None
legs = {}
for s in 'LR':
    legs[s] = dict(th=limb('thigh' + s), sh=limb('shin' + s), kn=joint('knee' + s))
    b = sphere('boot' + s, 0.05, [INK], None, 24, 12)
    for vtx in b.data.vertices:
        X, Y, Z = vtx.co
        vtx.co = (X * 1.0, Y * 0.62, max(Z, -0.0) * 0.7 + 0.0)
        vtx.co.x += 0.025
    b.rotation_mode = 'QUATERNION'
    legs[s]['boot'] = b
arms = {}
for s in 'LR':
    arms[s] = dict(up=limb('uarm' + s), lo=limb('farm' + s), el=joint('elbow' + s), hand=joint('hand' + s, 0.028))


def place_seg(ob, a, b, fr):
    d = b - a
    ob.location = a
    ob.rotation_quaternion = Vector((0, 0, -1)).rotation_difference(d.normalized())
    ob.scale = (1, 1, d.length)
    ob.keyframe_insert('location', frame=fr); ob.keyframe_insert('rotation_quaternion', frame=fr)
    ob.keyframe_insert('scale', frame=fr)


def ik(a, b, l1, l2, pole):
    d = b - a; dist = min(d.length, (l1 + l2) * 0.999); u = d.normalized()
    x = (l1 * l1 - l2 * l2 + dist * dist) / (2 * dist)
    h = math.sqrt(max(l1 * l1 - x * x, 0))
    n = (pole - u * pole.dot(u)).normalized()
    return a + u * x + n * h, a + u * dist


def key(ob, fr, loc=True, rot=True):
    if loc: ob.keyframe_insert('location', frame=fr)
    if rot: ob.keyframe_insert('rotation_quaternion' if ob.rotation_mode == 'QUATERNION' else 'rotation_euler', frame=fr)


L1 = L2 = 0.215
AL = 0.16
for fr in range(T_B0 - 2, 213):
    for sub in (0.0, 0.5):     # half-frame keys keep motion blur accurate
        ff = fr + sub
        t = (ff - T_B0) / FPS
        feet = {}
        for s in 'LR':
            x, lift, planted, _ = foot_state(s, t)
            y = FOOT_Y[s]
            z = float(H(x, y)) - SINK + 0.07 * lift
            feet[s] = (Vector((x, y, z)), lift)
        rx = root_x(t)
        gz = (float(H(rx, -0.07)) + float(H(rx, 0.07))) / 2
        bob = -0.012 * math.cos(4 * math.pi * t / PER)
        hipz = gz - SINK + 0.40 + bob
        sway = 0.035 * math.sin(2 * math.pi * t / PER)
        ROOT.location = (rx, 0.0, hipz)
        ROOT.rotation_euler = (sway * 0.5, 0.04 + 0.02 * math.sin(4 * math.pi * t / PER), math.radians(-90) + sway * 0.6)
        key(ROOT, ff)
        M = Matrix.Translation(ROOT.location) @ ROOT.rotation_euler.to_matrix().to_4x4()
        for s in 'LR':
            hip = M @ Vector((0.065 if s == 'L' else -0.065, 0, 0.0))
            ankle = feet[s][0] + Vector((0, 0, 0.03))
            knee, ank = ik(hip, ankle, L1, L2, FWD + Vector((0, 0, 0.2)))
            g = legs[s]
            place_seg(g['th'], hip, knee, ff); place_seg(g['sh'], knee, ank, ff)
            g['kn'].location = knee; key(g['kn'], ff, rot=False)
            lift = feet[s][1]
            g['boot'].location = ank - Vector((0, 0, 0.03))
            g['boot'].rotation_quaternion = Quaternion((0, 0, 1), math.pi) @ Quaternion((0, 1, 0), -0.35 * lift)
            key(g['boot'], ff)
        # left arm: holds the rifle on the shoulder
        shL = M @ shoulder_L
        hand = M @ GRIP_LOCAL
        el, hd = ik(shL, hand, AL, AL, Vector((0, 0, -1)) + FWD * 0.6)
        a = arms['L']; place_seg(a['up'], shL, el, ff); place_seg(a['lo'], el, hd, ff)
        a['el'].location = el; key(a['el'], ff, rot=False); a['hand'].location = hd; key(a['hand'], ff, rot=False)
        # right arm swings opposite to the right leg
        shR = M @ Vector((-0.15, 0.0, 0.37))
        sw = math.sin(2 * math.pi * (t / PER - 0.0))
        hand = shR + FWD * (0.10 * sw) + Vector((0, 0.05, -0.29))
        el, hd = ik(shR, hand, AL, AL, -FWD + Vector((0, 0, -0.3)))
        a = arms['R']; place_seg(a['up'], shR, el, ff); place_seg(a['lo'], el, hd, ff)
        a['el'].location = el; key(a['el'], ff, rot=False); a['hand'].location = hd; key(a['hand'], ff, rot=False)

# ---------------------------------------------------------------- forest layout
SUNS = {'a': ((-0.35, 1.0), 12.0), 'b': ((-1.0, -0.55), 13.0), 'c': ((0.45, 1.0), 10.0)}
P_CASE = Vector((2.0, -9.0, 0.0)); P_CASE.z = float(H(P_CASE.x, P_CASE.y))
POV = Vector((24.0, 3.0, 0.0)); POV.z = float(H(POV.x, POV.y))


def rect_d(x, y, x0, x1, y0, y1):
    dx = max(x0 - x, 0, x - x1); dy = max(y0 - y, 0, y - y1)
    return math.hypot(dx, dy)


def clear(x, y, h):
    R = 0.4 * h + 0.3                                         # widest skirt of a pine of height h
    if rect_d(x, y, -4.5, 3.5, -0.8, 0.8) < R * 0.8: return False     # walk path
    if rect_d(x, y, -3.8, -1.0, -3.9, -0.8) < R + 0.3: return False   # shot-b camera + view corridor
    if math.hypot(x - P_CASE.x, y - P_CASE.y) < R + 1.0: return False  # macro set
    if x > 17 and abs(y - POV.y) < R + 2: return False             # POV position
    # keep the low sun reaching each set: no tree inside the shadow corridor toward the sun
    for (sx, sy), (cx_, cy_, w) in ((SUNS['b'][0], (-1.5, 0.0, 3.5)), (SUNS['a'][0], (P_CASE.x, P_CASE.y, 1.5)),
                                    (SUNS['c'][0], (POV.x, POV.y, 2.0))):
        d = Vector((sx, sy)).normalized(); rel = Vector((x - cx_, y - cy_))
        along = rel.dot(d); perp = abs(rel.x * d.y - rel.y * d.x)
        if -1.0 < along < 6.0 * h and perp < w + R: return False
    return True


pts = []
tries = 0
while len(pts) < 330 and tries < 30000:
    tries += 1
    x, y, h = rng.uniform(-30, 30), rng.uniform(-30, 30), rng.uniform(4.5, 10.0)
    if x > 22 or not clear(x, y, h): continue
    if any((x - a) ** 2 + (y - b) ** 2 < (0.3 * (h + c)) ** 2 for a, b, c in pts): continue
    pts.append((x, y, h))
for x, y, h in pts:
    place_tree(x, y, h)
# young pines that pass out of focus in front of the shot-b camera (reveal at the start, wipe at the end)
place_tree(-0.05, -2.2, 1.3); place_tree(-3.9, -2.2, 1.25)
# forest outside the fine patch, valley trees and the far treeline across the valley
for _ in range(900):
    x, y = rng.uniform(-200, 22), rng.uniform(-250, 250)
    if abs(x) < 31 and abs(y) < 31: continue
    place_tree(x, y, rng.uniform(6, 11))
for _ in range(260):
    x, y = rng.uniform(40, 220), rng.uniform(-200, 200)
    if abs(y - POV.y) < 25 and x < 90: continue
    if abs(y - (3 + (x - 24) * 12 / 226)) < 12: continue
    place_tree(x, y, rng.uniform(6, 12), far=True)
for _ in range(2600):
    x, y = rng.uniform(215, 520), rng.uniform(-330, 330)
    if (x - 250) ** 2 + (y - 15) ** 2 < 14 ** 2 or (x < 250 and abs(y - (3 + (x - 24) * 12 / 226)) < 10): continue
    place_tree(x, y, rng.uniform(9, 15), far=True)
# a small cabin across the valley gives the POV shot a subject
cab = Vector((250, 15, 0)); cab.z = float(H(cab.x, cab.y))
c = box('cabin', -3, 3, 2.2, 1.4, [simple('logs', '#6b3a22', 0.8)], z0=1.2); c.location = cab; c.scale = (1.5, 1.5, 1.5)
roof = box('roof', -3.5, 3.5, 2.8, 0.25, [SNOW], z0=2.95); roof.location = cab; roof.scale = (1.5, 1.5, 1.5)
win = box('window', -3.05, -2.95, 0.5, 0.35, [simple('glow', '#ffb060', 0.5, **{'Emission Color': (1, 0.5, 0.15, 1), 'Emission Strength': 8})], z0=1.3)
win.location = cab; win.scale = (1.5, 1.5, 1.5)

# snow-covered logs near the path for foreground interest
for (lx, ly, ln, rot) in ((-4.5, 1.6, 2.2, 0.3), (2.6, -2.2, 1.6, -0.6)):
    lg = cyl_x('log', -ln / 2, ln / 2, 0.11, [BARK]); lg.location = (lx, ly, float(H(lx, ly)) + 0.05); lg.rotation_euler = (0, 0, rot)
    cap = cyl_x('logsnow', -ln / 2 - 0.02, ln / 2 + 0.02, 0.10, [SNOW]); cap.scale = (1, 1.15, 0.7)
    cap.location = (lx, ly, float(H(lx, ly)) + 0.13); cap.rotation_euler = (0, 0, rot)

# ---------------------------------------------------------------- casing (shot a)
case_prof = [(0.0001, 0.0), (0.0058, 0.0), (0.0062, 0.0006), (0.0062, 0.0016), (0.0053, 0.0021), (0.0053, 0.0030),
             (0.0060, 0.0036), (0.0058, 0.040), (0.0050, 0.0435), (0.0043, 0.0448), (0.0042, 0.0535), (0.0036, 0.0537), (0.0036, 0.050)]
CASE = lathe('casing', case_prof, 48, [BRASS], cap=False)
for vtx in CASE.data.vertices:
    vtx.co.z -= 0.027      # origin at centre
CASE.rotation_mode = 'QUATERNION'
CR = 0.006
rest_q = Quaternion((0, 1, 0), math.pi / 2) @ Quaternion((0, 0, 1), 0.3)
rest_q = Quaternion((0, 0, 1), 0.25) @ Quaternion((0, 1, 0), math.pi / 2 + 0.12)
T_IMP = 48
spin_axis = Vector((0.3, 1.0, 0.2)).normalized()
for fr in range(1, 92):
    for sub in (0.0, 0.5):
        ff = fr + sub
        if ff < T_IMP:
            tt = (T_IMP - ff) / FPS
            z = min(0.5 * 9.8 * 0.08 * tt * tt, 0.30)   # slow-motion gravity
            q = rest_q @ Quaternion(spin_axis, -9.0 * tt)
            pos = P_CASE + Vector((0.02 * tt, 0, CR * 0.55 + z))
        else:
            tt = (ff - T_IMP) / FPS
            bz = 0.012 * abs(math.sin(min(tt, 0.9) * math.pi / 0.45)) * math.exp(-3.5 * tt) if tt < 0.9 else 0.0
            pos = P_CASE + Vector((-0.012 * (1 - math.exp(-4 * tt)), 0, CR * 0.3 + bz))
            q = rest_q @ Quaternion(spin_axis, 0.5 * math.sin(8 * tt) * math.exp(-4 * tt))
        CASE.location = pos; CASE.rotation_quaternion = q; key(CASE, ff)
# snow puff: small clumps thrown out on impact that land and stay
clump = None
for i in range(22):
    cl = sphere('clump', rng.uniform(0.0015, 0.0035), [SNOW_SSS], None, 10, 5)
    ang = rng.uniform(0, 2 * math.pi); sp = rng.uniform(0.15, 0.5); up = rng.uniform(0.5, 1.2)
    vel = Vector((math.cos(ang) * sp * 0.25, math.sin(ang) * sp * 0.25, up * 0.25))
    for fr in range(1, 92):
        if fr <= T_IMP:
            cl.location = P_CASE + Vector((0, 0, -0.01)); cl.scale = (0.01,) * 3
        else:
            tt = (fr - T_IMP) / FPS
            p = P_CASE + vel * tt + Vector((0, 0, -0.5 * 0.9 * tt * tt - 0.003))
            gz = P_CASE.z + 0.0005
            if p.z < gz:
                p.z = gz
            cl.location = p; cl.scale = (1, 1, 1 if p.z > gz else 0.6)
        cl.keyframe_insert('location', frame=fr); cl.keyframe_insert('scale', frame=fr)
for i in range(14):  # loose snow grains around the impact spot
    gr = sphere('grain', rng.uniform(0.002, 0.006), [SNOW_SSS], None, 10, 5)
    a = rng.uniform(0, 6.28); r = rng.uniform(0.02, 0.25)
    gr.location = P_CASE + Vector((math.cos(a) * r, math.sin(a) * r, -0.001)); gr.scale = (1.3, 1, 0.35)

# ---------------------------------------------------------------- POV rifle (shot c only)
CAM_C = bpy.data.objects.new('cam_c', bpy.data.cameras.new('cam_c')); COL.objects.link(CAM_C)
POVR = make_rifle('povrifle', CAM_C)
POVR.rotation_mode = 'QUATERNION'
_a = math.radians(6.0)
_R = Matrix(((0, -1, 0), (0, 0, 1), (-1, 0, 0)))                # model X->-Z, Y->-X, Z->+Y
_q = Quaternion((1, 0, 0), -_a) @ _R.to_quaternion()
POVR.rotation_quaternion = _q
_rear = Vector((0.612, 0.0, 0.062))
_want = Vector((0.0, -0.30 * math.tan(_a), -0.30))
POVR.location = _want - _q @ _rear
for o in [o for o in bpy.data.objects if o.name.startswith('povrifle')]:
    o.hide_render = (SHOT != 'c')
# ---------------------------------------------------------------- cameras
def cam(name, lens, fstop, focus):
    c = bpy.data.objects.new(name, bpy.data.cameras.new(name)); COL.objects.link(c)
    c.data.lens = lens; c.data.sensor_fit = 'VERTICAL'; c.data.sensor_height = 24
    c.data.dof.use_dof = True; c.data.dof.aperture_fstop = fstop; c.data.dof.focus_object = focus
    c.data.dof.aperture_blades = 7
    c.data.clip_start = 0.01; c.data.clip_end = 3000
    return c


def look(c, eye, target, roll=0.0):
    c.location = eye
    q = (target - eye).to_track_quat('-Z', 'Y')
    c.rotation_euler = (q @ Quaternion((0, 0, 1), roll)).to_euler()


# a) macro on the casing
fa = bpy.data.objects.new('focus_a', None); COL.objects.link(fa); fa.location = P_CASE + Vector((0, 0, 0.006))
CA = cam('cam_a', 60, 3.2, fa)
for fr in (1, 91):
    k = (fr - 1) / 90
    look(CA, P_CASE + Vector((-0.012, -0.46 + 0.07 * k, 0.05 - 0.008 * k)), P_CASE + Vector((-0.012, 0, 0.026)))
    CA.keyframe_insert('location', frame=fr); CA.keyframe_insert('rotation_euler', frame=fr)

# b) medium-wide tracking shot
fb = bpy.data.objects.new('focus_b', None); COL.objects.link(fb)
CB = cam('cam_b', 32, 1.4, fb)
for fr in range(T_B0 - 1, 212, 3):
    t = (fr - T_B0) / FPS
    rx = root_x(t)
    tgt = Vector((rx - 0.3, 0, float(H(rx, 0)) + 0.58))
    eye = Vector((rx - 1.5 + 0.1 * t, -3.5 + 0.1 * t, float(H(rx, 0)) + 0.95))
    look(CB, eye, tgt)
    CB.keyframe_insert('location', frame=fr); CB.keyframe_insert('rotation_euler', frame=fr)
    fb.location = Vector((rx, -0.05, float(H(rx, 0)) + 0.6)); fb.keyframe_insert('location', frame=fr)

# c) POV down the iron sights; slight push-in
fc = bpy.data.objects.new('focus_c', None); COL.objects.link(fc)
fc.parent = CAM_C; fc.location = (0, 0, -1.05)  # front-sight distance (POV rifle is the only camera child)
CAM_C.data.lens = 30; CAM_C.data.sensor_fit = 'VERTICAL'; CAM_C.data.sensor_height = 24
CAM_C.data.dof.use_dof = True; CAM_C.data.dof.aperture_fstop = 5.6; CAM_C.data.dof.focus_object = fc
CAM_C.data.clip_start = 0.01; CAM_C.data.clip_end = 3000
for fr, lens, dx in ((211, 32, 0.0), (235, 32, 0.0), (300, 42, 0.25)):
    eye = POV + Vector((dx, 0, 1.05))
    look(CAM_C, eye, eye + (Vector((250, 15, float(H(250, 15)) + 9.0)) - eye).normalized())
    CAM_C.data.lens = lens
    CAM_C.keyframe_insert('location', frame=fr); CAM_C.keyframe_insert('rotation_euler', frame=fr)
    CAM_C.data.keyframe_insert('lens', frame=fr)

# ---------------------------------------------------------------- per-shot light + haze
if SHOT == 'a':
    set_sun(*SUNS['a']); scn.camera = CA
    haze(0.010, (2, -2, 5), (40, 40, 12))
elif SHOT == 'b':
    set_sun(*SUNS['b']); scn.camera = CB
    haze(0.028, (0, 0, 6), (45, 45, 14))
else:
    set_sun(*SUNS['c']); scn.camera = CAM_C
    haze(0.0022, (250, 0, 40), (300, 400, 80))
    sun_d.energy = 4.2

# ---------------------------------------------------------------- render settings
r = scn.render
r.engine = 'CYCLES'
r.resolution_x, r.resolution_y, r.resolution_percentage = 720, 1280, RES
r.fps = FPS
r.use_motion_blur = not os.environ.get('NOMB'); r.motion_blur_shutter = 0.5
r.image_settings.file_format = 'PNG'
r.use_persistent_data = True
cy = scn.cycles
cy.device = 'CPU'; cy.samples = SPP; cy.use_adaptive_sampling = True; cy.adaptive_threshold = float(os.environ.get('AT', 0.04))
cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'
cy.max_bounces = 4; cy.diffuse_bounces = int(os.environ.get('DB', 2)); cy.glossy_bounces = 1; cy.transmission_bounces = 1
cy.volume_bounces = 0; cy.transparent_max_bounces = 4
cy.caustics_reflective = False; cy.caustics_refractive = False
cy.blur_glossy = 1.0
cy.volume_step_rate = 4.0
scn.view_settings.view_transform = 'AgX'
for lk in ('AgX - Medium High Contrast',):
    try:
        scn.view_settings.look = lk; break
    except TypeError:
        pass
scn.view_settings.exposure = 0.0
scn.frame_start, scn.frame_end = F0, F1
r.filepath = os.path.join(OUT, f'{SHOT}_')
import time
_t = [time.time()]
def _tick(*a):
    print("FRAMETIME %.1f" % (time.time() - _t[0]), flush=True); _t[0] = time.time()
bpy.app.handlers.render_post.append(_tick)
print("BUILD done", flush=True)
if not os.environ.get("NORENDER"): bpy.ops.render.render(animation=True)

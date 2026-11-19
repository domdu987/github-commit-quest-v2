"""film 17 set kit ("Bertillon", Paris police 1882-83). bpy 5.x, Cycles CPU. 1 unit = 1 metre. Z up.
Everything is built from code: batched meshes (one object per material, per-box tint attribute), numpy/PIL textures box-projected in
object space (no UVs needed), a blue-violet ambient term injected as emission (so warm woods shade blue-violet, not pink),
one hard warm sun, gas lamps = emissive glass (no shadow) + point light. No depth of field, no text anywhere.
Texture detail is kept >= 6 texels per screen pixel footprint avoided: coarse grain only (Cycles has no mip-mapping).
Reusable: Batch, M (materials), room/window/prop functions, cameras, render_still."""
import os, math, random, contextlib
import numpy as np
import bpy, bmesh
from PIL import Image, ImageDraw
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__)); TEX = os.path.join(HERE, 'tex'); os.makedirs(TEX, exist_ok=True)
TEX_V = 1
LAMP_K = 0.9
AMB = (0.10, 0.24, 1.0)           # blue-violet ambient (hue ~248)
def lin(c): return tuple((x / 255.0) ** 2.2 for x in c) if max(c) > 1.0 else tuple(x ** 2.2 for x in c)
def hexc(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

# ---------------------------------------------------------------- textures
def _fnoise(w, h, sx, sy, seed):
    r = np.random.RandomState(seed); n = r.randn(h, w)
    fy = np.fft.fftfreq(h)[:, None]; fx = np.fft.rfftfreq(w)[None, :]
    g = np.exp(-((fx * sx) ** 2 + (fy * sy) ** 2) * 2 * math.pi ** 2)
    o = np.fft.irfft2(np.fft.rfft2(n) * g, s=(h, w)); o -= o.mean(); return o / (o.std() + 1e-9)
def _sm(x, a, b): t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)
def _save(name, arr):
    p = os.path.join(TEX, '%s_v%d.png' % (name, TEX_V))
    if not os.path.exists(p): Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8)).save(p)
    return p
def tex_wood(name, base, dark, planks=0, seed=1, S=1024, grain=7):
    p = os.path.join(TEX, '%s_v%d.png' % (name, TEX_V))
    if os.path.exists(p): return p
    y = np.arange(S)[:, None] / S * np.ones((1, S)); lo = _fnoise(S, S, 60, 6, seed); hi = _fnoise(S, S, 120, 3, seed + 1)
    rings = np.sin((y * grain + 0.55 * lo / 3) * 2 * math.pi); t = 0.5 + 0.22 * rings + 0.12 * hi / 3 + 0.1 * lo / 3
    t = np.clip(t, 0, 1)[..., None]; col = np.array(dark) / 255 * (1 - t) + np.array(base) / 255 * t
    if planks:
        pw = S // planks; idx = (np.arange(S) // pw)[:, None]; r = np.random.RandomState(seed + 5); tone = 0.86 + 0.28 * r.rand(planks + 1)
        col = col * tone[idx][..., None]; edge = (np.arange(S) % pw)[:, None]
        line = 1 - _sm(np.minimum(edge, pw - edge), 0, 5); col = col * (1 - 0.65 * line[..., None] * np.ones((1, S, 1)))
        for k in range(planks):                                             # one butt joint per plank
            xj = int(r.rand() * S); band = slice(k * pw, (k + 1) * pw)
            col[band, max(0, xj - 3):xj + 3] *= 0.45
    return _save(name, col)
def tex_plaster(name, base, seed=3, S=1024):
    p = os.path.join(TEX, '%s_v%d.png' % (name, TEX_V))
    if os.path.exists(p): return p
    a = _fnoise(S, S, 90, 90, seed); b = _fnoise(S, S, 25, 25, seed + 1)
    t = 1 + 0.07 * a / 3 + 0.03 * b / 3; return _save(name, np.clip(np.array(base) / 255 * t[..., None], 0, 1))
def tex_carpet(name, base, line, seed=4, S=1024):
    p = os.path.join(TEX, '%s_v%d.png' % (name, TEX_V))
    if os.path.exists(p): return p
    u, v = np.meshgrid(np.arange(S) / S, np.arange(S) / S); d = np.abs(((u + v) % 0.5) - 0.25) * 2; d2 = np.abs(((u - v) % 0.5) - 0.25) * 2
    lat = np.maximum(1 - _sm(d, 0.06, 0.12), 1 - _sm(d2, 0.06, 0.12))
    dot = 1 - _sm(np.hypot(((u * 2) % 1) - 0.5, ((v * 2) % 1) - 0.5), 0.1, 0.16)
    m = np.maximum(lat * 0.8, dot)[..., None]; n = 1 + 0.06 * _fnoise(S, S, 50, 50, seed)[..., None] / 3
    return _save(name, np.clip((np.array(base) / 255 * (1 - m) + np.array(line) / 255 * m) * n, 0, 1))
def _squig(d, x0, y0, x1, y1, rng, w=4, col=(70, 55, 60)):
    x = x0
    pts = []
    while x < x1:
        pts.append((x, y0 + (y1 - y0) / 2 + rng.uniform(-1, 1) * (y1 - y0) * 0.45)); x += rng.uniform(6, 14)
    if len(pts) > 1: d.line(pts, fill=col, width=w, joint='curve')
def tex_card(name, kind='card', seed=7):
    p = os.path.join(TEX, '%s_v%d.png' % (name, TEX_V))
    if os.path.exists(p): return p
    rng = random.Random(seed)
    if kind == 'card':        # filing card, landscape 3:2: two photo boxes + squiggle rows + ear-diagram oval. NO readable text.
        W, H = 768, 512; im = Image.new('RGB', (W, H), (240, 228, 196)); d = ImageDraw.Draw(im)
        d.rectangle([10, 10, W - 10, H - 10], outline=(150, 70, 60), width=6)
        d.rectangle([36, 36, 236, 276], fill=(130, 135, 160)); d.ellipse([86, 80, 186, 216], fill=(205, 175, 150))
        d.rectangle([256, 36, 456, 276], fill=(130, 135, 160)); d.ellipse([320, 80, 400, 216], fill=(205, 175, 150))
        d.ellipse([500, 50, 700, 250], outline=(90, 60, 60), width=7); d.arc([530, 80, 670, 220], 40, 300, fill=(90, 60, 60), width=7)
        for i in range(7): _squig(d, 40, 300 + i * 28, rng.randint(480, 724), 322 + i * 28, rng, 5)
        d.line([(36, 290), (730, 290)], fill=(150, 70, 60), width=5)
    else:                     # wanted notice, portrait
        W, H = 512, 700; im = Image.new('RGB', (W, H), (232, 216, 178)); d = ImageDraw.Draw(im)
        d.rectangle([14, 14, W - 14, H - 14], outline=(90, 60, 55), width=8); _squig(d, 50, 40, 460, 110, rng, 14, (60, 45, 50))
        d.rectangle([140, 140, 372, 380], fill=(135, 130, 150)); d.ellipse([200, 175, 312, 330], fill=(200, 170, 145))
        for i in range(9): _squig(d, 50, 410 + i * 28, rng.randint(300, 462), 432 + i * 28, rng, 7)
    im.save(p); return p

# ---------------------------------------------------------------- materials
_MATS = {}
def M(name, col=(200, 200, 200), tex=None, tile=1.0, rough=0.6, metal=0.0, tint=False, amb=0.14, emit=None, estr=0.0, spec=0.4,
      uv=False, bump=0.0, coat=0.0, tex_ref=None):
    """Principled + injected ambient emission (amb*luma(albedo)*AMB colour). tex: png path, box-projected in object space at `tile` metres.
    tint=True multiplies by the per-box 'tint' colour attribute. emit=(r,g,b), estr: pure emission material (lamp glass)."""
    if name in _MATS: return _MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes; L = nt.links
    out = N.new('ShaderNodeOutputMaterial')
    if emit is not None:
        e = N.new('ShaderNodeEmission'); e.inputs[0].default_value = (*lin(emit), 1); e.inputs[1].default_value = estr; L.new(e.outputs[0], out.inputs[0])
        _MATS[name] = m; return m
    c = lin(col); src = N.new('ShaderNodeRGB'); src.outputs[0].default_value = (*c, 1); colout = src.outputs[0]
    if tex:
        it = N.new('ShaderNodeTexImage'); it.image = bpy.data.images.load(tex, check_existing=True); it.interpolation = 'Linear'
        if uv: L.new(N.new('ShaderNodeTexCoord').outputs['UV'], it.inputs[0])
        else:
            it.projection = 'BOX'; it.projection_blend = 0.25
            tc = N.new('ShaderNodeTexCoord'); mp = N.new('ShaderNodeMapping'); s = 1.0 / tile; mp.inputs['Scale'].default_value = (s, s, s)
            L.new(tc.outputs['Object'], mp.inputs[0]); L.new(mp.outputs[0], it.inputs[0])
        mx = N.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs[0].default_value = 1
        L.new(it.outputs[0], mx.inputs[6])
        if tex_ref: r_ = lin(tex_ref); mx.inputs[7].default_value = (c[0] / r_[0], c[1] / r_[1], c[2] / r_[2], 1)    # recolour a neutral/other texture
        else: mx.inputs[7].default_value = (1, 1, 1, 1)                                                              # the texture carries the colour
        colout = mx.outputs[2]
    if tint:
        at = N.new('ShaderNodeAttribute'); at.attribute_name = 'tint'; at.attribute_type = 'GEOMETRY'
        mt = N.new('ShaderNodeMix'); mt.data_type = 'RGBA'; mt.blend_type = 'MULTIPLY'; mt.inputs[0].default_value = 1
        L.new(colout, mt.inputs[6]); L.new(at.outputs['Color'], mt.inputs[7]); colout = mt.outputs[2]
    pb = N.new('ShaderNodeBsdfPrincipled'); L.new(colout, pb.inputs['Base Color'])
    pb.inputs['Roughness'].default_value = rough; pb.inputs['Metallic'].default_value = metal
    for k in ('Specular IOR Level',):
        if k in pb.inputs: pb.inputs[k].default_value = spec
    if coat and 'Coat Weight' in pb.inputs: pb.inputs['Coat Weight'].default_value = coat; pb.inputs['Coat Roughness'].default_value = 0.15
    if bump:
        ns = N.new('ShaderNodeTexNoise'); ns.inputs['Scale'].default_value = 60; bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump
        L.new(ns.outputs['Fac'], bp.inputs['Height']); L.new(bp.outputs[0], pb.inputs['Normal'])
    if amb and not metal:
        bw = N.new('ShaderNodeRGBToBW'); L.new(colout, bw.inputs[0]); mu = N.new('ShaderNodeMath'); mu.operation = 'MULTIPLY_ADD'; mu.inputs[1].default_value = amb * 0.65; mu.inputs[2].default_value = amb * 0.35
        L.new(bw.outputs[0], mu.inputs[0]); em = N.new('ShaderNodeEmission'); em.inputs[0].default_value = (*AMB, 1); L.new(mu.outputs[0], em.inputs[1])
        ad = N.new('ShaderNodeAddShader'); L.new(pb.outputs[0], ad.inputs[0]); L.new(em.outputs[0], ad.inputs[1]); L.new(ad.outputs[0], out.inputs[0])
    else: L.new(pb.outputs[0], out.inputs[0])
    _MATS[name] = m; return m

def std_mats():
    """the period palette: honey wood, brass, deep green, oxblood, cream plaster."""
    T = {}
    T['floor'] = M('floor', (170, 125, 90), tex=tex_wood('floor', (205, 150, 100), (110, 68, 42), planks=5, seed=11), tile=1.2, rough=0.55, spec=0.5, amb=0.02)
    T['floor_dk'] = M('floor_dk', (175, 120, 70), tex=tex_wood('floor_dk', (190, 125, 70), (95, 55, 32), planks=5, seed=12), tile=1.2, rough=0.5, amb=0.02)
    T['honey'] = M('honey', (215, 150, 80), tex=tex_wood('honey', (225, 160, 90), (150, 90, 45), seed=21), tile=0.9, rough=0.42, tint=True, coat=0.25, amb=0.02)
    T['walnut'] = M('walnut', (160, 100, 58), tex=tex_wood('walnut', (170, 105, 60), (80, 45, 28), seed=22), tile=0.9, rough=0.45, tint=True, coat=0.2, amb=0.02)
    T['plaster'] = M('plaster', (236, 215, 170), tex=tex_plaster('plaster', (238, 214, 160)), tile=2.0, rough=0.9, spec=0.15)
    T['plaster_hi'] = M('plaster_hi', (238, 216, 168), tex=tex_plaster('plaster', (242, 224, 184)), tile=2.0, rough=0.9, spec=0.15, amb=0.36)
    T['green'] = M('green', (40, 96, 70), tex=tex_plaster('plaster', (242, 224, 184)), tile=1.5, rough=0.7, tint=True, tex_ref=(242, 224, 184))
    T['oxblood'] = M('oxblood', (120, 28, 34), rough=0.5, tint=True, coat=0.2)
    T['navy'] = M('navy', (36, 48, 92), rough=0.6, tint=True)
    T['leather'] = M('leather', (110, 62, 36), rough=0.5, tint=True)
    T['cream'] = M('cream', (240, 228, 196), rough=0.85, tint=True)
    T['brass'] = M('brass', (235, 170, 70), rough=0.28, metal=1.0, tint=True)
    T['steel'] = M('steel', (190, 196, 214), rough=0.22, metal=1.0)
    T['iron'] = M('iron', (55, 60, 75), rough=0.45, metal=0.8)
    T['cloth'] = M('cloth', (28, 28, 46), rough=0.95, spec=0.1)
    T['ink'] = M('ink', (22, 20, 40), rough=0.2, spec=0.6)
    T['glass'] = M('glass', (150, 200, 190), rough=0.05, tint=False)
    T['carpet'] = M('carpet', (135, 40, 44), tex=tex_carpet('carpet', (105, 34, 40), (150, 118, 78)), tile=0.5, rough=0.95, spec=0.1, amb=0.02)
    T['dark'] = M('dark', (40, 30, 34), rough=0.6)
    T['flat_card'] = M('flat_card', (95, 120, 150), rough=1.0, amb=0.6)
    T['glow_gas'] = M('glow_gas', emit=(255, 196, 105), estr=14.0)
    T['glow_green'] = M('glow_green', emit=(120, 235, 150), estr=3.0)
    T['glow_sky'] = M('glow_sky', emit=(185, 205, 245), estr=2.6)
    T['glow_win'] = M('glow_win', emit=(255, 214, 140), estr=6.0)
    return T

# ---------------------------------------------------------------- batched geometry
def rotm(rx=0, ry=0, rz=0):
    a, b, c = map(math.radians, (rx, ry, rz)); ca, sa, cb, sb, cc, sc = math.cos(a), math.sin(a), math.cos(b), math.sin(b), math.cos(c), math.sin(c)
    Rx = np.array([[1, 0, 0], [0, ca, -sa], [0, sa, ca]]); Ry = np.array([[cb, 0, sb], [0, 1, 0], [-sb, 0, cb]]); Rz = np.array([[cc, -sc, 0], [sc, cc, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx
def _m4(loc=(0, 0, 0), rot=(0, 0, 0), scale=1.0):
    m = np.eye(4); m[:3, :3] = rotm(*rot) * scale; m[:3, 3] = loc; return m
_CUBE_F = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
class Batch:
    """accumulates boxes/cylinders/spheres per material; finalize() makes one Blender object per material."""
    def __init__(self, T): self.T = T; self.d = {}; self.stack = [np.eye(4)]; self.rng = random.Random(5)
    @contextlib.contextmanager
    def xf(self, loc=(0, 0, 0), rot=(0, 0, 0), scale=1.0):
        self.stack.append(self.stack[-1] @ _m4(loc, rot, scale))
        try: yield
        finally: self.stack.pop()
    def _put(self, mat, v, faces, smooth, tint):
        v = np.asarray(v, float); v = (self.stack[-1][:3, :3] @ v.T).T + self.stack[-1][:3, 3]
        key = mat if isinstance(mat, str) else mat.name; D = self.d.setdefault(key, dict(v=[], f=[], s=[], t=[], n=0))
        D['f'] += [tuple(i + D['n'] for i in f) for f in faces]; D['s'] += [smooth] * len(faces); D['v'].append(v); D['n'] += len(v)
        t = tint if isinstance(tint, (tuple, list)) else (tint, tint, tint); D['t'].append(np.tile(np.array([*t, 1.0]), (len(v), 1)))
    def box(self, mat, c, s, rot=(0, 0, 0), tint=1.0):
        h = np.array(s, float) / 2; u = np.array([[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]], float) * h
        self._put(mat, (rotm(*rot) @ u.T).T + np.array(c), _CUBE_F, False, tint)
    def cyl(self, mat, c, r, h, axis='z', r2=None, seg=16, rot=(0, 0, 0), tint=1.0, smooth=True, caps=True):
        r2 = r if r2 is None else r2; a = np.linspace(0, 2 * math.pi, seg, endpoint=False); R = {'z': (0, 0, 0), 'x': (0, 90, 0), 'y': (90, 0, 0)}[axis]
        lo = np.stack([r * np.cos(a), r * np.sin(a), -h / 2 * np.ones(seg)], 1); hi = np.stack([r2 * np.cos(a), r2 * np.sin(a), h / 2 * np.ones(seg)], 1)
        v = np.concatenate([lo, hi]); f = [(i, (i + 1) % seg, seg + (i + 1) % seg, seg + i) for i in range(seg)]
        Rm = rotm(*rot) @ rotm(*R)
        self._put(mat, (Rm @ v.T).T + np.array(c), f, smooth, tint)
        if caps:
            for z, rr, rev in ((-h / 2, r, True), (h / 2, r2, False)):
                if rr <= 0: continue
                cv = np.concatenate([np.stack([rr * np.cos(a), rr * np.sin(a), z * np.ones(seg)], 1), [[0, 0, z]]]); ff = [(i, (i + 1) % seg, seg) for i in range(seg)]
                if not rev: ff = [(b, a_, c_) for a_, b, c_ in ff]
                else: ff = [(a_, b, c_) for a_, b, c_ in ff]
                self._put(mat, (Rm @ cv.T).T + np.array(c), [(f_[1], f_[0], f_[2]) if rev else f_ for f_ in ff], False, tint)
    def sphere(self, mat, c, r, seg=20, rings=12, scale=(1, 1, 1), tint=1.0):
        v = [(0, 0, -1)]; 
        for j in range(1, rings):
            p = -math.pi / 2 + math.pi * j / rings
            for i in range(seg): a = 2 * math.pi * i / seg; v.append((math.cos(p) * math.cos(a), math.cos(p) * math.sin(a), math.sin(p)))
        v.append((0, 0, 1)); f = []
        for i in range(seg): f.append((0, 1 + (i + 1) % seg, 1 + i))
        for j in range(rings - 2):
            for i in range(seg): a = 1 + j * seg + i; b = 1 + j * seg + (i + 1) % seg; f.append((a, b, b + seg, a + seg)[::-1][::-1])
        top = len(v) - 1
        for i in range(seg): f.append((top, 1 + (rings - 2) * seg + i, 1 + (rings - 2) * seg + (i + 1) % seg))
        v = np.array(v) * np.array(scale) * r + np.array(c)
        self._put(mat, v, [tuple(x) for x in f], True, tint)
    def mesh(self, mat, v, faces, smooth=True, tint=1.0): self._put(mat, v, faces, smooth, tint)
    def finalize(self, bevel=0.004):
        objs = []
        for key, D in self.d.items():
            V = np.concatenate(D['v']); me = bpy.data.meshes.new(key); me.from_pydata(V.tolist(), [], D['f']); me.update()
            me.polygons.foreach_set('use_smooth', D['s'])
            if key != 'cloth':
                bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
            ca = me.color_attributes.new('tint', 'FLOAT_COLOR', 'POINT'); ca.data.foreach_set('color', np.concatenate(D['t']).ravel())
            ob = bpy.data.objects.new(key, me); bpy.context.scene.collection.objects.link(ob); ob.data.materials.append(self.T_get(key))
            if key.startswith('glow'): ob.visible_shadow = False
            elif bevel and key not in ('floor', 'floor_dk') and len(D['f']) < 80000:
                bv = ob.modifiers.new('bv', 'BEVEL'); bv.width = bevel; bv.segments = 1; bv.limit_method = 'ANGLE'; bv.angle_limit = math.radians(40)
            objs.append(ob)
        self.d = {}; return objs
    def T_get(self, key): return _MATS[key]

# ---------------------------------------------------------------- scene, lights, camera
def new_scene(world=(0.0, 0.22, 1.0), wstr=0.80):
    bpy.ops.wm.read_factory_settings(use_empty=True); _MATS.clear()
    for im in list(bpy.data.images): bpy.data.images.remove(im)
    sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes['Background']; bg.inputs[0].default_value = (*world, 1); bg.inputs[1].default_value = wstr
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = -0.5; sc.render.film_transparent = False
    sc.cycles.max_bounces = 5; sc.cycles.diffuse_bounces = 0; sc.cycles.glossy_bounces = 3; sc.cycles.transmission_bounces = 2
    sc.cycles.sample_clamp_indirect = 8.0; sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.02
    return sc
def sun(direction, color=(1.0, 0.80, 0.55), strength=5.0, angle=0.9):
    d = bpy.data.lights.new('key', 'SUN'); d.energy = strength; d.color = color; d.angle = math.radians(angle)
    ob = bpy.data.objects.new('key', d); bpy.context.scene.collection.objects.link(ob)
    ob.rotation_euler = Vector(direction).normalized().to_track_quat('-Z', 'Y').to_euler(); return ob
def point(loc, color=(1.0, 0.68, 0.34), watts=120, radius=0.07, name='lamp'):
    d = bpy.data.lights.new(name, 'POINT'); d.energy = watts * LAMP_K; d.color = color; d.shadow_soft_size = radius
    ob = bpy.data.objects.new(name, d); ob.location = loc; bpy.context.scene.collection.objects.link(ob); return ob
def area(loc, target, size, color, watts, name='area'):
    d = bpy.data.lights.new(name, 'AREA'); d.energy = watts; d.color = color; d.size = size[0]; d.size_y = size[1]; d.shape = 'RECTANGLE'
    ob = bpy.data.objects.new(name, d); ob.location = loc; bpy.context.scene.collection.objects.link(ob)
    ob.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); return ob
def camera(loc, target, lens=22.0, roll=0.0):
    c = bpy.data.cameras.new('cam'); c.lens = lens; c.sensor_width = 36; c.sensor_fit = 'AUTO'; c.dof.use_dof = False
    ob = bpy.data.objects.new('cam', c); bpy.context.scene.collection.objects.link(ob); ob.location = loc
    ob.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); bpy.context.scene.camera = ob; return ob
def render_still(path, w=720, h=1280, samples=80):
    import time; sc = bpy.context.scene; r = sc.render; r.resolution_x, r.resolution_y, r.resolution_percentage = w, h, 100; r.image_settings.file_format = 'PNG'
    sc.cycles.samples = samples; sc.cycles.use_denoising = True; sc.cycles.denoiser = 'OPENIMAGEDENOISE'; sc.cycles.preview_samples = 8
    r.filepath = path; r.threads_mode = 'FIXED'; r.threads = 4; t = time.time(); bpy.ops.render.render(write_still=True); dt = time.time() - t; grade(path); return dt
def grade(path, sat=1.18):
    """light final grade: saturation boost (HSV), nothing else."""
    im = np.asarray(Image.open(path).convert('RGB'), dtype=float) / 255; mx = im.max(-1, keepdims=True); mn = im.min(-1, keepdims=True)
    out = np.clip(mx - (mx - im) * sat, 0, 1); Image.fromarray((out * 255 + 0.5).astype(np.uint8)).save(path)

# ---------------------------------------------------------------- room pieces
def room_shell(B, x0, x1, y0, y1, h, window=None, wain=1.15, floor='floor', wall='plaster'):
    """floor, ceiling, 4 walls (inside faces), green wainscot to `wain`, skirting, picture rail. window=(wall 'L', y_a, y_b, z_a, z_b) cuts left wall."""
    t = 0.2; W = x1 - x0; D = y1 - y0; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    B.box(floor, (cx, cy, -0.05), (W + 2 * t, D + 2 * t, 0.1))
    B.box(wall, (cx, cy, h + 0.05), (W + 2 * t, D + 2 * t, 0.1))
    B.box(wall, (cx, y1 + t / 2, h / 2), (W + 2 * t, t, h)); B.box(wall, (cx, y0 - t / 2, h / 2), (W + 2 * t, t, h))
    B.box(wall, (x1 + t / 2, cy, h / 2), (t, D, h))
    if window is None: B.box(wall, (x0 - t / 2, cy, h / 2), (t, D, h))
    else:
        _, ya, yb, za, zb = window
        B.box(wall, (x0 - t / 2, (y0 + ya) / 2, h / 2), (t, ya - y0, h)); B.box(wall, (x0 - t / 2, (yb + y1) / 2, h / 2), (t, y1 - yb, h))
        B.box(wall, (x0 - t / 2, (ya + yb) / 2, za / 2), (t, yb - ya, za)); B.box(wall, (x0 - t / 2, (ya + yb) / 2, (zb + h) / 2), (t, yb - ya, h - zb))
    # green wainscot + brass-less cap rail + skirting
    for (px, py, sx, sy) in ((cx, y1 - 0.02, W, 0.04), (cx, y0 + 0.02, W, 0.04), (x1 - 0.02, cy, 0.04, D)):
        B.box('green', (px, py, wain / 2), (sx, sy, wain)); B.box('walnut', (px, py, wain + 0.025), (sx + (0.04 if sx > 0.05 else 0.03), sy + (0.04 if sy > 0.05 else 0.03), 0.05))
        B.box('walnut', (px, py, 0.08), (sx + (0.03 if sx > 0.05 else 0.02), sy + (0.03 if sy > 0.05 else 0.02), 0.16))
    # left wall
    if window is None: segs = [(y0, y1)]
    else: segs = [(y0, window[1]), (window[2], y1)]
    for a, b in segs:
        B.box('green', (x0 + 0.02, (a + b) / 2, wain / 2), (0.04, b - a, wain)); B.box('walnut', (x0 + 0.03, (a + b) / 2, wain + 0.025), (0.07, b - a, 0.05))
        B.box('walnut', (x0 + 0.025, (a + b) / 2, 0.08), (0.05, b - a, 0.16))
    # cornice + picture rail
    for (px, py, sx, sy) in ((cx, y1, W, 0.1), (cx, y0, W, 0.1), (x1, cy, 0.1, D), (x0, cy, 0.1, D)):
        B.box('walnut', (px + (-0.03 if px == x1 else 0.03 if px == x0 else 0), py + (-0.03 if py == y1 else 0.03 if py == y0 else 0), h - 0.08), (sx, sy, 0.16))
def barred_window(B, x, ya, yb, za, zb, sky_depth=7.0, bars=5):
    """frame, iron bars, glass-less sky plane outside (no shadow) with distant Paris roofs."""
    B.box('walnut', (x + 0.06, (ya + yb) / 2, za - 0.04), (0.28, yb - ya + 0.2, 0.08)); B.box('walnut', (x + 0.06, (ya + yb) / 2, zb + 0.04), (0.2, yb - ya + 0.2, 0.08))
    B.box('walnut', (x + 0.04, ya - 0.04, (za + zb) / 2), (0.16, 0.08, zb - za)); B.box('walnut', (x + 0.04, yb + 0.04, (za + zb) / 2), (0.16, 0.08, zb - za))
    for i in range(bars):
        yy = ya + (yb - ya) * (i + 0.5) / bars; B.cyl('iron', (x + 0.07, yy, (za + zb) / 2), 0.018, zb - za, seg=8)
    for zz in (za + (zb - za) * 0.35, za + (zb - za) * 0.7): B.box('iron', (x + 0.07, (ya + yb) / 2, zz), (0.03, yb - ya, 0.03))
    B.box('walnut', (x + 0.05, (ya + yb) / 2, (za + zb) / 2), (0.05, 0.05, zb - za))                       # mullion
    for a in (-1, 1): B.box('walnut', (x + 0.15, (ya + yb) / 2, za + 0.01), (0.2, yb - ya + 0.2, 0.04))
    # outside: sky card + a few roof blocks (they sit under the sun line and do not cast shadows via visible_shadow=False on 'glow_sky')
    B.box('glow_sky', (x - sky_depth, (ya + yb) / 2, (za + zb) / 2 + 3), (0.1, 30, 22))
    r = random.Random(3)
    for i in range(9):
        yy = (ya + yb) / 2 + (i - 4) * 2.6; hh = r.uniform(3.0, 5.2); B.box('plaster', (x - 5.5 - r.uniform(0, 3), yy, hh / 2 - 0.2), (r.uniform(2.0, 3.0), r.uniform(2.0, 2.5), hh), tint=(0.95, 0.9, 1.0))
        B.box('navy', (x - 5.5 - r.uniform(0, 1.5), yy, hh + 0.35), (2.4, 2.4, 0.7), tint=(1, 1, 1.2))
def gas_bracket(B, loc, rot_z=0, glow=True, watts=40):
    """wall gas lamp: brass arm + tap + frosted globe + point light. loc = wall contact, +x local = out of the wall."""
    with B.xf(loc, (0, 0, rot_z)):
        B.box('brass', (0.03, 0, 0), (0.06, 0.12, 0.18)); B.cyl('brass', (0.16, 0, 0), 0.016, 0.3, axis='x', seg=8)
        B.cyl('brass', (0.3, 0, -0.04), 0.02, 0.1, seg=8); B.cyl('brass', (0.3, 0, -0.1), 0.05, 0.04, r2=0.034, seg=14)
        B.cyl('brass', (0.3, 0, -0.14), 0.05, 0.03, r2=0.07, seg=14); B.sphere('glow_gas', (0.3, 0, -0.24), 0.085, scale=(1, 1, 1.2))
        B.cyl('brass', (0.3, 0, -0.36), 0.04, 0.03, r2=0.02, seg=12)
        p = np.array([0.3, 0, -0.24]); wp = B.stack[-1][:3, :3] @ p + B.stack[-1][:3, 3]
    point(tuple(wp), watts=watts, radius=0.09)
def gas_stand(B, loc, h=1.9, watts=160):
    """foreground standing gas lamp: iron base, fluted post, brass collar, lantern with glow globe."""
    x, y, z = loc
    B.cyl('iron', (x, y, z + 0.06), 0.2, 0.12, r2=0.14, seg=20); B.cyl('iron', (x, y, z + 0.22), 0.1, 0.22, r2=0.06, seg=16)
    B.cyl('iron', (x, y, z + h * 0.5), 0.045, h * 0.72, seg=14); B.cyl('brass', (x, y, z + h * 0.35), 0.07, 0.05, seg=16); B.cyl('brass', (x, y, z + h * 0.62), 0.065, 0.05, seg=16)
    B.cyl('brass', (x, y, z + h - 0.28), 0.12, 0.06, r2=0.14, seg=20); B.sphere('glow_gas', (x, y, z + h - 0.12), 0.15, scale=(1, 1, 1.25))
    for k in range(4): a = k * math.pi / 2 + math.pi / 4; B.cyl('brass', (x + 0.15 * math.cos(a), y + 0.15 * math.sin(a), z + h - 0.12), 0.009, 0.36, seg=6)
    B.cyl('brass', (x, y, z + h + 0.1), 0.17, 0.05, r2=0.05, seg=20); B.sphere('brass', (x, y, z + h + 0.16), 0.045)
    point((x, y, z + h - 0.12), watts=watts, radius=0.12)
def pendant_gas(B, loc, drop=1.2, watts=220, glow='glow_gas'):
    x, y, z = loc; B.cyl('iron', (x, y, z - drop / 2), 0.012, drop, seg=6); B.cyl('brass', (x, y, z - drop - 0.04), 0.09, 0.08, r2=0.2, seg=18)
    B.sphere(glow, (x, y, z - drop - 0.24), 0.17, scale=(1, 1, 1.15)); B.cyl('brass', (x, y, z - drop - 0.44), 0.05, 0.05, r2=0.02, seg=10)
    for k in range(6): a = k * math.pi / 3; B.cyl('brass', (x + 0.18 * math.cos(a), y + 0.18 * math.sin(a), z - drop - 0.24), 0.007, 0.34, seg=5)
    point((x, y, z - drop - 0.24), watts=watts, radius=0.14)

# ---------------------------------------------------------------- furniture & props
def table(B, c, size=(1.6, 0.8), h=0.85, mat='honey', rot=0):
    with B.xf((c[0], c[1], 0), (0, 0, rot)):
        B.box(mat, (0, 0, h - 0.03), (size[0], size[1], 0.06)); B.box('walnut', (0, 0, h - 0.1), (size[0] - 0.12, size[1] - 0.12, 0.08))
        for sx in (-1, 1):
            for sy in (-1, 1):
                px, py = sx * (size[0] / 2 - 0.1), sy * (size[1] / 2 - 0.1); B.box('walnut', (px, py, (h - 0.06) / 2), (0.07, 0.07, h - 0.06)); B.cyl('walnut', (px, py, 0.18), 0.045, 0.1, seg=10)
        B.box('walnut', (0, 0, 0.2), (size[0] - 0.2, 0.04, 0.05))
def stool(B, c, h=0.62, rot=0):
    with B.xf((c[0], c[1], 0), (0, 0, rot)):
        B.cyl('leather', (0, 0, h), 0.2, 0.06, seg=18); B.cyl('walnut', (0, 0, h - 0.06), 0.18, 0.05, seg=18)
        for k in range(3): a = k * 2 * math.pi / 3; B.cyl('walnut', (0.12 * math.cos(a), 0.12 * math.sin(a), h / 2 - 0.04), 0.022, h - 0.08, seg=8, rot=(8 * math.sin(a), -8 * math.cos(a), 0))
def measuring_chair(B, c, rot=0, head_z=1.30):
    """oak measuring chair on a low dais: seat, high back, arms, tall rear post with adjustable head rest (brass clamp + screw), foot rail."""
    with B.xf((c[0], c[1], 0), (0, 0, rot)):
        B.box('walnut', (0, 0.05, 0.05), (1.0, 1.0, 0.1), tint=0.9)                            # low dais
        B.box('honey', (0, 0, 0.48), (0.56, 0.5, 0.07)); B.box('leather', (0, 0, 0.53), (0.5, 0.44, 0.05), tint=(1.0, 0.9, 0.9))
        for sx in (-1, 1):
            for sy in (-1, 1): B.box('honey', (sx * 0.24, sy * 0.2, 0.26), (0.06, 0.06, 0.4)); B.cyl('walnut', (sx * 0.24, sy * 0.2, 0.18), 0.04, 0.08, seg=10)
        B.box('honey', (0, -0.04, 0.12 + 0.08), (0.5, 0.04, 0.05)); B.box('honey', (0, 0.3, 0.2), (0.6, 0.1, 0.04))   # rails, foot rest
        B.box('honey', (0, -0.22, 0.95), (0.54, 0.05, 0.9)); B.box('honey', (0, -0.22, 1.42), (0.62, 0.06, 0.06))    # back + crest
        for sx in (-1, 1):
            B.box('honey', (sx * 0.3, -0.02, 0.72), (0.05, 0.48, 0.05)); B.box('honey', (sx * 0.3, 0.2, 0.62), (0.05, 0.05, 0.2)); B.box('brass', (sx * 0.3, 0.22, 0.73), (0.07, 0.07, 0.03))
        for k in range(5): B.cyl('honey', (-0.2 + 0.1 * k, -0.22, 0.62), 0.016, 0.4, seg=8) if False else None
        B.box('honey', (0, -0.3, 1.0), (0.12, 0.08, 1.9))                                      # tall post
        B.box('brass', (0, -0.3, 1.0), (0.13, 0.085, 0.02))
        for z in np.arange(0.2, 1.9, 0.1): B.box('brass', (0, -0.255, z), (0.05 if round(z * 10) % 5 else 0.09, 0.006, 0.006))      # ticks on the post
        B.box('brass', (0, -0.3, head_z), (0.2, 0.14, 0.07)); B.cyl('brass', (0.12, -0.3, head_z), 0.03, 0.06, axis='x', seg=12)   # clamp + screw knob
        B.box('honey', (0, -0.13, head_z), (0.05, 0.3, 0.05)); B.box('leather', (0, 0.03, head_z + 0.04), (0.22, 0.05, 0.3), tint=(1.1, 0.9, 0.9)); B.box('brass', (0, 0.03, head_z + 0.2), (0.24, 0.06, 0.02))
def height_scale(B, c, z0=0.4, z1=2.2, rot=0, slider=1.58):
    """tall wall height scale: oak board, brass tick strips (no numbers), sliding brass marker block."""
    with B.xf((c[0], c[1], 0), (0, 0, rot)):
        B.box('honey', (0, 0, (z0 + z1) / 2), (0.22, 0.04, z1 - z0 + 0.1)); B.box('walnut', (0, 0.012, (z0 + z1) / 2), (0.03, 0.02, z1 - z0 + 0.06))
        for k, z in enumerate(np.arange(z0, z1, 0.05)):
            big = k % 10 == 0; mid = k % 5 == 0; B.box('brass', (-0.05 if not big else -0.045, 0.026, z), (0.07 if big else 0.05 if mid else 0.03, 0.006, 0.006))
        B.box('brass', (0.035, 0.03, slider), (0.15, 0.04, 0.045)); B.box('walnut', (0.1, 0.06, slider), (0.14, 0.09, 0.025)); B.cyl('brass', (0.0, 0.06, slider), 0.02, 0.05, axis='y', seg=10)
        B.box('walnut', (0, 0.02, z1 + 0.08), (0.28, 0.05, 0.05)); B.box('walnut', (0, 0.02, z0 - 0.08), (0.28, 0.05, 0.05))
def sliding_calipers(B, c, rot=0, length=0.5, z=0.0, open_=0.18, tilt=(0, 0, 0)):
    """big steel sliding (head) calipers: long graduated beam, fixed jaw, sliding jaw, brass lock screw."""
    with B.xf((c[0], c[1], c[2] + z), (tilt[0], tilt[1], rot)):
        B.box('steel', (0, 0, 0.012), (length, 0.022, 0.024)); B.box('brass', (0, 0, 0.026), (length * 0.96, 0.006, 0.004))
        for k in range(int(length / 0.025)): B.box('iron', (-length / 2 + 0.02 + k * 0.025, -0.01, 0.026), (0.003, 0.008, 0.008 if k % 4 else 0.014))
        B.box('steel', (-length / 2 + 0.01, -0.04, 0.03), (0.02, 0.1, 0.07)); B.box('steel', (-length / 2 + 0.02, -0.1, 0.012), (0.03, 0.05, 0.03), rot=(0, 0, 25))
        sx = -length / 2 + 0.02 + open_; B.box('steel', (sx, -0.02, 0.012), (0.04, 0.05, 0.045)); B.box('steel', (sx, -0.1, 0.03), (0.02, 0.11, 0.07)); B.box('steel', (sx - 0.005, -0.15, 0.012), (0.03, 0.05, 0.03), rot=(0, 0, -25))
        B.cyl('brass', (sx, 0.015, 0.04), 0.014, 0.025, seg=10); B.cyl('brass', (sx, 0.015, 0.06), 0.018, 0.012, seg=10)
def spreading_calipers(B, c, rot=0, span=0.28, leg=0.4, tilt=(0, 0, 0)):
    """compass-style spreading calipers lying flat: pivot ring + two curved legs (box segments), steel."""
    with B.xf(c, (tilt[0], tilt[1], rot)):
        B.cyl('brass', (0, 0, 0.018), 0.022, 0.016, seg=14); B.cyl('steel', (0, 0, 0.03), 0.012, 0.012, seg=10)
        for s in (-1, 1):
            a = math.atan2(span / 2, leg)
            for j, (f0, f1) in enumerate(((0.0, 0.55), (0.55, 1.0))):
                r_ = leg * (0.5 * (f0 + f1)); ang = s * a * (1 if j == 0 else 0.6 + 0.0)
                B.box('steel', (s * math.sin(ang) * r_ * (0.9 if j else 1.0) + (s * 0.02 if j else 0), math.cos(ang) * r_ * 0.9 + (0.03 if j else 0), 0.012), (0.016, leg * (f1 - f0) * 1.05, 0.012), rot=(0, 0, -math.degrees(ang) * (1.0 if j == 0 else 0.35)))
            B.sphere('steel', (s * span / 2, leg * 0.9, 0.014), 0.012)
def ledger_stack(B, c, n=5, rot=0, w=0.34, d=0.24, mats=('oxblood', 'green', 'leather', 'navy', 'oxblood')):
    z = c[2]
    with B.xf((c[0], c[1], 0), (0, 0, rot)):
        for i in range(n):
            t = 0.045 + 0.02 * (i % 3); m = mats[i % len(mats)]; jx = B.rng.uniform(-0.02, 0.02); jr = B.rng.uniform(-6, 6)
            B.box(m, (jx, 0, z + t / 2), (w, d, t), rot=(0, 0, jr), tint=B.rng.uniform(0.85, 1.1)); B.box('cream', (jx, 0.0, z + t / 2), (w - 0.03, d + 0.008, t - 0.014), rot=(0, 0, jr))
            B.box('brass', (jx - w / 2 + 0.01, 0, z + t / 2), (0.014, d * 0.95, t + 0.004), rot=(0, 0, jr)); z += t
        B.box('brass', (0, 0, z + 0.004), (0.06, 0.04, 0.004))
def open_ledger(B, c, rot=0, w=0.34, d=0.25):
    with B.xf(c, (0, 0, rot)):
        B.box('oxblood', (0, 0, 0.012), (w * 2 + 0.03, d + 0.02, 0.024)); B.box('cream', (-w / 2, 0, 0.04), (w - 0.01, d - 0.01, 0.036), rot=(0, 3, 0)); B.box('cream', (w / 2, 0, 0.04), (w - 0.01, d - 0.01, 0.036), rot=(0, -3, 0))
        for k in range(8): B.box('dark', (-w / 2 + 0.0, d / 2 - 0.03 - k * 0.026, 0.06), (w * 0.8 * (1 - 0.3 * (k % 3) / 3), 0.004, 0.002), rot=(0, 3, 0)); B.box('dark', (w / 2, d / 2 - 0.03 - k * 0.026, 0.06), (w * 0.7, 0.004, 0.002), rot=(0, -3, 0))
def inkpot(B, c, quill=True, rot=0):
    x, y, z = c; B.cyl('glass', (x, y, z + 0.03), 0.04, 0.06, seg=16); B.cyl('ink', (x, y, z + 0.032), 0.034, 0.058, seg=14); B.cyl('brass', (x, y, z + 0.07), 0.03, 0.02, seg=14)
    B.cyl('ink', (x, y, z + 0.082), 0.012, 0.01, seg=10)
    if quill:
        with B.xf((x + 0.0, y, z + 0.09), (0, 0, rot)):
            B.cyl('cream', (0.1, 0, 0.13), 0.004, 0.3, rot=(0, 70, 0), seg=6); B.box('cream', (0.17, 0, 0.17), (0.16, 0.026, 0.002), rot=(0, 70, 0))
def kepi(B, c, rot=0, tilt=(0, 0, 0)):
    with B.xf(c, (tilt[0], tilt[1], rot)):
        B.cyl('oxblood', (0, 0, 0.06), 0.085, 0.12, r2=0.1, seg=18); B.cyl('navy', (0, 0, 0.022), 0.088, 0.045, seg=18); B.cyl('oxblood', (0, 0, 0.125), 0.11, 0.012, seg=18)
        B.box('leather', (0.1, 0, 0.012), (0.09, 0.15, 0.008), rot=(0, 10, 0)); B.cyl('brass', (0.092, 0, 0.065), 0.018, 0.008, axis='x', seg=10)
def coat_rack(B, c, rot=0, h=1.9, kepis=3):
    x, y = c[0], c[1]
    with B.xf((x, y, 0), (0, 0, rot)):
        B.cyl('walnut', (0, 0, 0.05), 0.24, 0.1, r2=0.18, seg=18); B.cyl('walnut', (0, 0, h / 2), 0.04, h, seg=12); B.sphere('brass', (0, 0, h + 0.04), 0.06)
        for k in range(4):
            a = k * 90 + 45; ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            B.cyl('brass', (0.13 * ca, 0.13 * sa, h - 0.16), 0.012, 0.28, rot=(0, 0, a), axis='x', seg=6) if False else None
            B.cyl('brass', (0.12 * ca, 0.12 * sa, h - 0.18), 0.013, 0.26, axis='x', rot=(0, 0, a), seg=6); B.sphere('brass', (0.24 * ca, 0.24 * sa, h - 0.18), 0.022)
        for k in range(kepis):
            a = k * 90 + 45 + 180 * (k == 2); ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            kepi(B, (0.24 * ca, 0.24 * sa, h - 0.27 - 0.0), rot=a + 90, tilt=(0, 0, 0))
        B.cyl('navy', (0.0, 0.2, h - 0.5), 0.14, 0.85, r2=0.2, seg=14, rot=(10, 0, 0))                                  # a hanging coat
def bench(B, c, length=3.2, rot=0, h=0.46):
    with B.xf((c[0], c[1], 0), (0, 0, rot)):
        B.box('walnut', (0, 0, h), (length, 0.4, 0.06)); B.box('walnut', (0, -0.17, h + 0.12), (length, 0.04, 0.2), tint=0.95)
        for sx in (-1, 1):
            for dx in (0.1, 0.8, 1.5):
                px = sx * (length / 2 - 0.1) if dx == 0.1 else sx * (length / 2 - dx - 0.1)
                if sx == 1 and dx != 0.1: continue
                B.box('walnut', (px, 0, h / 2), (0.06, 0.34, h)); 
        B.box('walnut', (0, 0, 0.18), (length - 0.2, 0.04, 0.04))
def flat_person(B, c, rot=0, h=1.7, col='flat_card', seat=False):
    """placeholder silhouette card (thin box body + disc head), flat colour; stands where a 2D puppet card will go."""
    with B.xf(c, (0, 0, rot)):
        B.box(col, (0, 0, h * 0.35 + (0 if not seat else 0)), (0.5, 0.02, h * 0.7)); B.cyl(col, (0, 0, h * 0.84), 0.15, 0.02, axis='y', seg=18)
def camera_on_tripod(B, c, rot=0, h=1.45):
    """period studio camera: wooden box + brass lens + bellows on a 3-leg tripod + black hood cloth draped over the back."""
    x, y = c[0], c[1]
    with B.xf((x, y, 0), (0, 0, rot)):
        for k in range(3):
            a = k * 120 + 90; ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            top = np.array([0, 0, h - 0.05]); bot = np.array([0.45 * ca, 0.45 * sa, 0.0]); mid = (top + bot) / 2; v = top - bot; L = np.linalg.norm(v)
            ang_y = math.degrees(math.acos(v[2] / L)); ang_z = math.degrees(math.atan2(v[1], v[0]))
            B.box('walnut', tuple(mid), (0.045, 0.03, L), rot=(0, ang_y, ang_z) if False else (0, 0, 0)) if False else None
            B.cyl('walnut', tuple(mid), 0.022, L, r2=0.016, seg=8, rot=(0, 0, 0)) if False else None
            B.cyl('walnut', tuple(mid), 0.02, L, seg=8, rot=(math.degrees(math.atan2(-sa * 0.45, (h - 0.05))) * 1.0 * 0 + 0, 0, 0)) if False else None
            # tilt about the horizontal axis perpendicular to leg direction
            t = math.degrees(math.atan2(0.45, h - 0.05)); B.cyl('walnut', tuple(mid), 0.02, L, seg=8, rot=(0, 0, 0), smooth=True) if False else None
            Rm = rotm(0, 0, a) @ rotm(0, -t, 0)
            eul = (math.degrees(math.atan2(Rm[2, 1], Rm[2, 2])), math.degrees(-math.asin(Rm[2, 0])), math.degrees(math.atan2(Rm[1, 0], Rm[0, 0])))
            B.cyl('walnut', tuple(mid), 0.022, L, seg=8, rot=eul)
        B.cyl('brass', (0, 0, h - 0.04), 0.1, 0.06, seg=16); B.box('walnut', (0, 0, h), (0.3, 0.3, 0.04))
        B.box('walnut', (0, -0.16, h + 0.22), (0.34, 0.26, 0.38)); B.box('iron', (0, -0.3, h + 0.22), (0.24, 0.1, 0.3))           # back box (+ focusing glass frame)
        B.box('cloth', (0, 0.0, h + 0.22), (0.26, 0.34, 0.26)); B.box('walnut', (0, 0.17, h + 0.22), (0.28, 0.04, 0.3))               # bellows, front standard
        B.cyl('brass', (0, 0.25, h + 0.22), 0.07, 0.14, axis='y', r2=0.06, seg=18); B.cyl('glass', (0, 0.325, h + 0.22), 0.05, 0.01, axis='y', seg=18); B.cyl('brass', (0, 0.34, h + 0.22), 0.075, 0.02, axis='y', seg=18)
        # black cloth: rings loft hanging over the back
        rows = 9; cols = 14; V = []; F = []
        for i in range(rows):
            u = i / (rows - 1)
            for j in range(cols):
                a = math.pi * (j / (cols - 1)) * 2 - math.pi; z = h + 0.44 - 0.9 * u ** 1.3; r_ = 0.2 + 0.35 * u ** 1.2 + 0.03 * math.sin(j * 2.4 + i)
                V.append((-0.26 - 0.05 * u + 0.0, r_ * math.sin(a) * 1.05, z)) if False else V.append((-0.28 - 0.18 * u * 0.4 + r_ * math.cos(a) * 0.35, r_ * math.sin(a), z))
        for i in range(rows - 1):
            for j in range(cols - 1): F.append((i * cols + j, i * cols + j + 1, (i + 1) * cols + j + 1, (i + 1) * cols + j))
        B.mesh('cloth', V, F, smooth=True)
def card_cube(B, name, c, size, rot, tex_path, mat_name):
    """one thin cube with UVs showing a card texture (separate object)."""
    bpy.ops.mesh.primitive_cube_add(size=1); ob = bpy.context.active_object; ob.name = name; ob.scale = size; ob.location = c; ob.rotation_euler = [math.radians(a) for a in rot]
    bpy.ops.object.transform_apply(scale=True)
    m = M(mat_name, (240, 232, 214), tex=tex_path, rough=0.8, uv=True, amb=0.3); ob.data.materials.append(m); return ob
def drawer_card_row(B, c, n=22, w=0.16, h=0.1, spacing=0.0125, tilt=-3, rot=0):
    """standing index cards (thin boxes) with coloured tab tops, in a row along local x."""
    with B.xf(c, (0, 0, rot)):
        for i in range(n):
            t = B.rng.uniform(0.9, 1.05); tilt_ = tilt + B.rng.uniform(-4, 4); x = i * spacing
            B.box('cream', (x, 0, h / 2), (0.003, w, h), rot=(0, tilt_, 0), tint=(t, t * 0.97, t * 0.9))
            if i % 4 == 0: B.box(['oxblood', 'green', 'navy'][(i // 4) % 3], (x, -w / 2 + 0.03 * (i % 8 == 0), h + 0.005), (0.004, 0.035, 0.02), rot=(0, tilt_, 0))
def cabinet_wall(B, origin, along, length, height, depth=0.55, cell=(0.30, 0.20), rot_z=0, pull=True, seed=9):
    """wall of wooden card cabinets. local frame: x along wall, y toward the aisle, z up. Each drawer: front, brass handle, brass label frame with blank cream card.
    pulled-out drawers (a few) show stacked cards."""
    r = random.Random(seed); cw, ch = cell; nc = int(length / cw); nr = int(height / ch)
    with B.xf(origin, (0, 0, rot_z)):
        B.box('walnut', (length / 2, depth / 2 - 0.02, height / 2), (length, depth, height), tint=0.9)
        B.box('walnut', (length / 2, depth / 2 + 0.02, height + 0.07), (length + 0.1, depth + 0.1, 0.14)); B.box('walnut', (length / 2, depth / 2 + 0.06, 0.07), (length + 0.06, depth + 0.1, 0.14))
        for i in range(nc // 5 + 1):                                                                             # pilasters every 5 columns
            B.box('walnut', (i * 5 * cw, depth + 0.012, height / 2), (0.05, 0.05, height), tint=0.85)
        for rr in range(nr // 6 + 1): B.box('walnut', (length / 2, depth + 0.012, rr * 6 * ch), (length, 0.045, 0.035), tint=0.85)
        for cc in range(nc):
            for rr in range(nr):
                if rr % 6 == 0 and rr > 0 and False: continue
                x = (cc + 0.5) * cw; z = (rr + 0.5) * ch + 0.15; t = r.uniform(0.78, 1.12); tint = (t, t * r.uniform(0.94, 1.0), t * r.uniform(0.86, 1.0))
                o = 0.0; d = 'fl'
                if pull and r.random() < 0.025: o = r.uniform(0.04, 0.16)
                y = depth + 0.01 + o
                B.box('honey', (x, y, z), (cw - 0.022, 0.035, ch - 0.02), tint=tint)
                B.box('walnut', (x, y + 0.019, z), (cw - 0.07, 0.004, ch - 0.07), tint=tint)                      # raised panel
                B.box('brass', (x, y + 0.028, z + ch * 0.12), (0.115, 0.006, 0.05), tint=r.uniform(0.9, 1.1)); B.box(['cream', 'cream', 'cream'][0], (x, y + 0.032, z + ch * 0.12), (0.094, 0.006, 0.036), tint=(r.uniform(0.9, 1.05), r.uniform(0.9, 1.0), r.uniform(0.85, 1.0)))
                B.cyl('brass', (x, y + 0.04, z - ch * 0.2), 0.012, 0.03, axis='y', seg=8); B.box('brass', (x, y + 0.052, z - ch * 0.2), (0.07, 0.01, 0.012), tint=r.uniform(0.9, 1.1))
                if o > 0.08: B.box('walnut', (x, y - o / 2, z - 0.02), (cw - 0.04, o, ch - 0.06)); B.box('dark', (x, y - o / 2, z + 0.02), (cw - 0.07, o - 0.01, 0.06))
def rolling_ladder(B, base, top, width=0.5, rot_z=0, rungs=14):
    """ladder leaning from floor point `base` to a rail point `top` (world coordinates), brass rail wheel at top."""
    b = np.array(base, float); t = np.array(top, float); v = t - b; L = np.linalg.norm(v); d = v / L
    ax = np.array([-d[1], d[0], 0]); ax = ax / (np.linalg.norm(ax) + 1e-9) if np.linalg.norm(ax) > 1e-6 else np.array([1, 0, 0])
    ang_y = math.degrees(math.atan2(math.hypot(d[0], d[1]), d[2])); ang_z = math.degrees(math.atan2(d[1], d[0]))
    Rm = rotm(0, ang_y, ang_z); eul = (math.degrees(math.atan2(Rm[2, 1], Rm[2, 2])), math.degrees(-math.asin(Rm[2, 0])), math.degrees(math.atan2(Rm[1, 0], Rm[0, 0])))
    ax = np.cross(d, [0, 0, 1]); ax = ax / np.linalg.norm(ax)
    for s in (-1, 1):
        B.box('honey', tuple((b + t) / 2 + ax * s * width / 2), (0.045, 0.03, L), rot=_euler_to_z(d), tint=0.9)
    for k in range(rungs):
        p = b + d * (0.25 + k * (L - 0.4) / (rungs - 1)); B.cyl('walnut', tuple(p), 0.016, width, axis='x', rot=(0, 0, math.degrees(math.atan2(ax[1], ax[0]))), seg=8)
    for s in (-1, 1): B.cyl('brass', tuple(t + ax * s * width / 2 + np.array([0, 0, 0.02])), 0.04, 0.03, axis='x', rot=(0, 0, math.degrees(math.atan2(ax[1], ax[0]))), seg=14)
def _euler_to_z(d):
    """euler (deg) that rotates local +z onto direction d."""
    d = np.array(d, float); d /= np.linalg.norm(d); ang_y = math.degrees(math.acos(max(-1, min(1, d[2])))); ang_z = math.degrees(math.atan2(d[1], d[0]))
    Rm = rotm(0, ang_y, ang_z); return (math.degrees(math.atan2(Rm[2, 1], Rm[2, 2])), math.degrees(-math.asin(max(-1, min(1, Rm[2, 0])))), math.degrees(math.atan2(Rm[1, 0], Rm[0, 0])))
def fan_cards(B, c, n=9, spread=70, r=0.12, rot=0, w=0.15, d=0.1):
    """cards fanned out like a hand of playing cards on a desk, pivot at the lower end."""
    with B.xf(c, (0, 0, rot)):
        for i in range(n):
            a = -spread / 2 + spread * i / (n - 1); ca, sa = math.cos(math.radians(a + 90)), math.sin(math.radians(a + 90))
            B.box('cream', (r * ca * 0.4, r * sa * 0.4, 0.002 + 0.0035 * i), (d, w, 0.002), rot=(0, 0, a), tint=B.rng.uniform(0.93, 1.04))
            if i % 3 == 0: B.box(['oxblood', 'green', 'navy'][i // 3 % 3], (r * ca * 0.4 + 0.07 * math.cos(math.radians(a)) * 0.0, r * sa * 0.4, 0.0035 * i + 0.004), (d * 0.9, 0.018, 0.0016), rot=(0, 0, a))
def banker_lamp(B, c, rot=0, watts=70):
    """brass banker's lamp, deep green glass shade; emissive inner + warm point light."""
    x, y, z = c
    with B.xf((x, y, z), (0, 0, rot)):
        B.cyl('brass', (0, 0, 0.015), 0.09, 0.03, r2=0.07, seg=18); B.cyl('brass', (0, 0, 0.17), 0.016, 0.28, seg=10); B.sphere('brass', (0, 0, 0.31), 0.03)
        B.box('green', (0.04, 0, 0.36), (0.3, 0.17, 0.09), tint=1.0, rot=(0, -12, 0)) if False else None
        B.cyl('brass', (0.04, 0, 0.34), 0.02, 0.06, seg=8)
        B.cyl('green', (0.06, 0, 0.375), 0.095, 0.17, axis='y', seg=20, caps=True, rot=(0, 0, 0), smooth=True)                          # half-cylinder-ish shade
        B.box('glow_green', (0.06, 0, 0.35), (0.2, 0.15, 0.015))
        wp = B.stack[-1][:3, :3] @ np.array([0.06, 0, 0.335]) + B.stack[-1][:3, 3]
    point(tuple(wp), color=(1.0, 0.78, 0.45), watts=watts, radius=0.08, name='banker')

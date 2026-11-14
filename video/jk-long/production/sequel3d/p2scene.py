"""สกิลจอมโกหก ภาค 2 · 3D look test after the owner's reference: a faceted rock cave at sunset, a three-headed green dragon with glowing
rims, a pile of gold, crystals, a torch, and the barrel-headed salesman holding up his insurance paper. Everything is Blender geometry
(no AI images). World: 1 unit = 1 m, Z up, ground z = 0; the cave faces -x; the hero stands at x ~ -4 facing +x.
usage: python3 p2scene.py still <shot> <t> [out.png] | render <shot> [--every N] [--draft] | plan"""
import os, sys, math, random, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
FPS = 30; DUR = 13.5; N = int(round(DUR * FPS)); RAW = os.path.join(HERE, 'raw')
import p2tex
TX = p2tex.build_all()

def ease(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)
def lerp(a, b, u): return a + (b - a) * u
def keyed(keys, t):
    """keys = [(t, value-tuple-or-float), ...] -> smoothly interpolated value."""
    if t <= keys[0][0]: return keys[0][1]
    for (a, va), (b, vb) in zip(keys[:-1], keys[1:]):
        if a <= t < b:
            u = ease((t - a) / (b - a))
            return tuple(lerp(x, y, u) for x, y in zip(va, vb)) if isinstance(va, tuple) else lerp(va, vb, u)
    return keys[-1][1]

# ============================================================================= shots
HERO = (-4.2, 0.6, 0.0)
SHOTS = [
    dict(n='S1', t0=0.0, t1=2.9, dof=None, keys=[(0.0, (-10.5, -5.8, 2.4), (-0.4, 1.2, 2.6), 22), (2.9, (-9.6, -5.0, 2.2), (-0.4, 1.2, 2.6), 24)]),
    dict(n='S2', t0=2.9, t1=5.6, dof=2.2, keys=[(2.9, (-3.2, -2.6, 0.9), (0.2, 0.9, 3.0), 22), (5.6, (-2.8, -2.2, 0.85), (0.2, 0.9, 3.1), 25)]),
    dict(n='S3', t0=5.6, t1=9.2, dof=2.0, keys=[(5.6, (-2.4, -1.6, 1.6), (-4.1, 0.6, 1.45), 32), (9.2, (-2.6, -1.3, 1.55), (-4.1, 0.6, 1.5), 38)]),
    dict(n='S4', t0=9.2, t1=DUR, dof=5.6, keys=[(9.2, (-7.2, -3.7, 1.15), (-1.6, 1.3, 2.05), 21), (DUR, (-6.8, -3.3, 1.12), (-1.6, 1.3, 2.15), 23)]),
]
# ---------------- performance (shared by all shots)
HEADS = [  # (base in the cave, rest head position, tilt) top / middle / bottom like the reference
    dict(base=(2.2, 1.4, 4.2), head=(-0.6, 0.4, 4.6), seed=1),
    dict(base=(2.4, 1.0, 2.8), head=(-1.3, 0.2, 2.75), seed=2),
    dict(base=(2.3, 0.8, 1.6), head=(-0.7, 0.0, 1.15), seed=3)]
def head_state(i, t):
    """Head position offset (emerging, sway, lunge toward the paper) + jaw opening."""
    em = ease((t - 0.4 - 0.25 * i) / 1.6)                                 # rising out of the cave in S1
    sway = (0.12 * math.sin(t * 1.7 + i * 2.1), 0.1 * math.sin(t * 1.3 + i), 0.14 * math.sin(t * 2.0 + i * 1.3))
    lunge = 0.55 * ease((t - 10.2) / 1.8) - 0.25 * ease((t - 12.4) / 0.8)  # lean in to sniff the paper
    roar = ease((t - 2.95) / 0.25) - ease((t - 4.6) / 0.6)
    jaw = 0.22 + 0.5 * roar + 0.1 * math.sin(t * 3 + i) * (1 - roar) - 0.12 * ease((t - 10.2) / 1.0)
    back = (1 - em) * 2.4
    return (sway[0] + back - lunge, sway[1], sway[2] - (1 - em) * 0.6 - 0.15 * lunge), max(0.05, jaw)
HERO_KEYS = [  # (t, pose name, face)
    (0.0, 'brace', 'scared'), (5.9, 'brace', 'scared'), (6.6, 'reach', 'scared'), (7.6, 'pull', 'scared'), (8.4, 'hold_up', 'determined'), (DUR, 'hold_up', 'determined')]
POSES = {   # segment directions in the hero's frame (forward = toward the dragon, lat = his left, up)
    'brace':   dict(lean=-0.12, thigh_f=(0.55, -0.1, -0.83), shin_f=(0.1, 0.0, -1.0), thigh_b=(-0.5, 0.1, -0.86), shin_b=(-0.35, 0.0, -0.94),
                    up_r=(0.25, -0.5, -0.8), lo_r=(0.6, -0.3, 0.2), up_l=(0.3, 0.55, -0.6), lo_l=(0.75, 0.2, 0.3), head_tilt=-0.15, paper=0.0),
    'reach':   dict(lean=-0.05, thigh_f=(0.5, -0.1, -0.86), shin_f=(0.1, 0.0, -1.0), thigh_b=(-0.45, 0.1, -0.89), shin_b=(-0.3, 0.0, -0.95),
                    up_r=(0.25, -0.5, -0.8), lo_r=(0.5, -0.3, 0.3), up_l=(0.25, 0.3, -0.9), lo_l=(0.25, -0.75, 0.5), head_tilt=0.15, paper=0.0),
    'pull':    dict(lean=0.0, thigh_f=(0.5, -0.1, -0.86), shin_f=(0.1, 0.0, -1.0), thigh_b=(-0.45, 0.1, -0.89), shin_b=(-0.3, 0.0, -0.95),
                    up_r=(0.25, -0.5, -0.8), lo_r=(0.5, -0.3, 0.3), up_l=(0.35, 0.55, -0.2), lo_l=(0.5, 0.3, 0.75), head_tilt=0.05, paper=1.0),
    'hold_up': dict(lean=0.06, thigh_f=(0.6, -0.1, -0.79), shin_f=(0.15, 0.0, -0.99), thigh_b=(-0.55, 0.1, -0.83), shin_b=(-0.4, 0.0, -0.92),
                    up_r=(0.45, -0.45, -0.55), lo_r=(0.9, -0.1, 0.1), up_l=(0.6, 0.25, 0.5), lo_l=(0.55, 0.0, 0.83), head_tilt=-0.08, paper=1.0),
}
def hero_pose(t):
    cur = HERO_KEYS[0]
    for k in HERO_KEYS:
        if t >= k[0]: cur = k
    i = HERO_KEYS.index(cur); nxt = HERO_KEYS[min(i + 1, len(HERO_KEYS) - 1)]
    u = 0.0 if nxt is cur else ease((t - cur[0]) / max(1e-3, nxt[0] - cur[0]))
    a, b = POSES[cur[1]], POSES[nxt[1]]; p = {}
    for k in a:
        p[k] = tuple(lerp(x, y, u) for x, y in zip(a[k], b[k])) if isinstance(a[k], tuple) else lerp(a[k], b[k], u)
    face = cur[2] if u < 0.5 else nxt[2]
    if (t % 3.1) < 0.12 and face != 'shout': face = 'blink'
    p['bob'] = 0.012 * math.sin(t * 2 * math.pi / 2.2) + (0.02 * math.sin(t * 40) if 3.0 < t < 3.8 else 0.0)    # breathing + a shiver at the roar
    return p, face

# ============================================================================= Blender
def blender_build():
    import bpy, bmesh
    from mathutils import Vector, Matrix, Euler, noise
    G = dict(bpy=bpy, Vector=Vector)
    bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.render.threads_mode = 'FIXED'; sc.render.threads = 4
    sc.cycles.samples = 14; sc.cycles.use_denoising = True
    try: sc.cycles.denoiser = 'OPENIMAGEDENOISE'
    except Exception: pass
    sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 1; sc.cycles.transparent_max_bounces = 8
    sc.view_settings.view_transform = 'Standard'
    sc.view_settings.exposure = -0.15
    sc.render.resolution_x, sc.render.resolution_y = 1280, 720
    sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 94
    col = bpy.data.collections.new('SET'); sc.collection.children.link(col); G['col'] = col

    def hexc(h, a=1.0):
        h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (a,)
    G['hexc'] = hexc
    MATS = {}
    def mat(name, color='#808080', rough=0.6, metal=0.0, emit=None, estr=0.0, rim=None, rim_str=0.0, img=None, alpha=False, vcol=False, spec=0.3):
        if name in MATS: return MATS[name]
        m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; L = nt.links.new
        bs = nt.nodes['Principled BSDF']; out = nt.nodes['Material Output']
        bs.inputs['Roughness'].default_value = rough; bs.inputs['Metallic'].default_value = metal
        try: bs.inputs['Specular IOR Level'].default_value = spec
        except Exception: pass
        if img:
            tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = bpy.data.images.load(img, check_existing=True); L(tx.outputs['Color'], bs.inputs['Base Color'])
            if alpha: L(tx.outputs['Alpha'], bs.inputs['Alpha'])
        elif vcol:
            at = nt.nodes.new('ShaderNodeVertexColor'); at.layer_name = 'Col'; L(at.outputs['Color'], bs.inputs['Base Color'])
        else: bs.inputs['Base Color'].default_value = hexc(color)
        if emit:
            bs.inputs['Emission Color'].default_value = hexc(emit); bs.inputs['Emission Strength'].default_value = estr
        if rim:
            lw = nt.nodes.new('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.14
            pw = nt.nodes.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 3.0; L(lw.outputs['Facing'], pw.inputs[0])
            em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = hexc(rim); em.inputs['Strength'].default_value = rim_str
            mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = rim_str; L(pw.outputs[0], mul.inputs[0]); L(mul.outputs[0], em.inputs['Strength'])
            ad = nt.nodes.new('ShaderNodeAddShader'); L(bs.outputs['BSDF'], ad.inputs[0]); L(em.outputs['Emission'], ad.inputs[1]); L(ad.outputs['Shader'], out.inputs['Surface'])
        MATS[name] = m; return m
    G['mat'] = mat

    def mesh_obj(name, verts, faces, mats, mi=None, uvs=None, smooth=False, coll=None):
        me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
        for m in mats: me.materials.append(m)
        if mi is not None:
            for p, k in zip(me.polygons, mi): p.material_index = k
        if uvs is not None:
            uvl = me.uv_layers.new(name='UVMap'); i = 0
            for f, fu in zip(faces, uvs):
                for c in fu: uvl.data[i].uv = c; i += 1
        for p in me.polygons: p.use_smooth = smooth
        ob = bpy.data.objects.new(name, me); (coll or col).objects.link(ob); return ob
    G['mesh_obj'] = mesh_obj

    class MB:
        def __init__(s): s.v = []; s.f = []; s.mi = []; s.uv = []; s.mats = []
        def slot(s, m):
            if m not in s.mats: s.mats.append(m)
            return s.mats.index(m)
        def face(s, pts, m, uv=None):
            b = len(s.v); s.v += [tuple(p) for p in pts]; s.f.append(list(range(b, b + len(pts)))); s.mi.append(s.slot(m)); s.uv.append(uv or [(0, 0)] * len(pts))
        def quad(s, p0, pu, pv, m, uv=(0, 0, 1, 1)):
            p0, pu, pv = Vector(p0), Vector(pu), Vector(pv); a, b, c, d = uv
            s.face([p0, p0 + pu, p0 + pu + pv, p0 + pv], m, [(a, b), (c, b), (c, d), (a, d)])
        def tube(s, pts, radii, m, seg=10, cap=True):
            pts = [Vector(p) for p in pts]; rings = []
            for i, p in enumerate(pts):
                t_ = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized(); a = t_.cross(Vector((0, 0, 1)))
                if a.length < 1e-3: a = Vector((1, 0, 0))
                a.normalize(); bb = t_.cross(a); r = radii[i] if isinstance(radii, (list, tuple)) else radii
                rings.append([p + r * (math.cos(2 * math.pi * k / seg) * a + math.sin(2 * math.pi * k / seg) * bb) for k in range(seg)])
            b0 = len(s.v)
            for rg in rings: s.v += [tuple(q) for q in rg]
            for i in range(len(rings) - 1):
                for k in range(seg):
                    j = (k + 1) % seg; s.f.append([b0 + i * seg + k, b0 + i * seg + j, b0 + (i + 1) * seg + j, b0 + (i + 1) * seg + k]); s.mi.append(s.slot(m)); s.uv.append([(0, 0)] * 4)
            if cap:
                s.f.append([b0 + k for k in range(seg)][::-1]); s.mi.append(s.slot(m)); s.uv.append([(0, 0)] * seg)
                e = b0 + (len(rings) - 1) * seg; s.f.append([e + k for k in range(seg)]); s.mi.append(s.slot(m)); s.uv.append([(0, 0)] * seg)
        def cone(s, base, tip, r, m, seg=8):
            base, tip = Vector(base), Vector(tip); t_ = (tip - base).normalized(); a = t_.cross(Vector((0, 0, 1)))
            if a.length < 1e-3: a = Vector((1, 0, 0))
            a.normalize(); bb = t_.cross(a); rg = [base + r * (math.cos(2 * math.pi * k / seg) * a + math.sin(2 * math.pi * k / seg) * bb) for k in range(seg)]
            for k in range(seg): s.face([rg[k], rg[(k + 1) % seg], tip], m)
            s.face(rg[::-1], m)
        def sphere(s, c, r, m, seg=12, rings=8, sx=1, sy=1, sz=1):
            c = Vector(c); R = []
            for k in range(rings + 1):
                th = math.pi * k / rings; R.append([c + Vector((r * sx * math.sin(th) * math.cos(2 * math.pi * i / seg), r * sy * math.sin(th) * math.sin(2 * math.pi * i / seg), -r * sz * math.cos(th))) for i in range(seg)])
            for k in range(rings):
                for i in range(seg): j = (i + 1) % seg; s.face([R[k][i], R[k][j], R[k + 1][j], R[k + 1][i]], m)
        def box(s, lo, hi, m, mats=None):
            (x0, y0, z0), (x1, y1, z1) = lo, hi; mats = mats or {}
            s.quad((x0, y0, z0), (x1 - x0, 0, 0), (0, 0, z1 - z0), mats.get('front', m)); s.quad((x1, y1, z0), (x0 - x1, 0, 0), (0, 0, z1 - z0), mats.get('back', m))
            s.quad((x1, y0, z0), (0, y1 - y0, 0), (0, 0, z1 - z0), mats.get('right', m)); s.quad((x0, y1, z0), (0, y0 - y1, 0), (0, 0, z1 - z0), mats.get('left', m))
            s.quad((x0, y0, z1), (x1 - x0, 0, 0), (0, y1 - y0, 0), mats.get('top', m)); s.quad((x0, y1, z0), (x1 - x0, 0, 0), (0, y0 - y1, 0), mats.get('bottom', m))
        def obj(s, name, smooth=False, coll=None):
            return mesh_obj(name, s.v, s.f, s.mats, s.mi, s.uv, smooth, coll)
    G['MB'] = MB
    build_world(G, sc); build_set(G)
    return G

def build_world(G, sc):
    bpy = G['bpy']; hexc = G['hexc']
    w = bpy.data.worlds.new('sky'); sc.world = w; w.use_nodes = True; nt = w.node_tree; L = nt.links.new
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputWorld'); tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ'); L(tc.outputs['Generated'], sep.inputs[0])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); L(sep.outputs['Z'], ramp.inputs[0]); cr = ramp.color_ramp
    cr.elements[0].position = 0.0; cr.elements[0].color = hexc('#ffc58a'); cr.elements[1].position = 0.36; cr.elements[1].color = hexc('#3f74de')
    e = cr.elements.new(0.1); e.color = hexc('#f7b98e'); e2 = cr.elements.new(0.2); e2.color = hexc('#9aa6ec')
    bgc = nt.nodes.new('ShaderNodeBackground'); L(ramp.outputs['Color'], bgc.inputs['Color']); bgc.inputs['Strength'].default_value = 1.0
    amb = nt.nodes.new('ShaderNodeBackground'); amb.inputs['Color'].default_value = hexc('#8aa4e8'); amb.inputs['Strength'].default_value = 0.4
    lp = nt.nodes.new('ShaderNodeLightPath'); mx = nt.nodes.new('ShaderNodeMixShader'); L(lp.outputs['Is Camera Ray'], mx.inputs['Fac'])
    L(amb.outputs['Background'], mx.inputs[1]); L(bgc.outputs['Background'], mx.inputs[2]); L(mx.outputs['Shader'], out.inputs['Surface'])
    def sun(name, rot, color, energy, angle):
        ld = bpy.data.lights.new(name, 'SUN'); ld.energy = energy; ld.color = hexc(color)[:3]; ld.angle = math.radians(angle)
        ob = bpy.data.objects.new(name, ld); ob.rotation_euler = rot; sc.collection.objects.link(ob); return ob
    sun('key', (math.radians(52), 0, math.radians(-118)), '#ffd8a8', 2.5, 6)        # warm low sun from the front-left
    sun('rim', (math.radians(68), 0, math.radians(72)), '#ffe2a8', 1.8, 3)          # back light: bright edges
    G['sun'] = True
    ld = bpy.data.lights.new('fill', 'AREA'); ld.energy = 420; ld.size = 3.0; ld.color = hexc('#ffe0c0')[:3]
    ob = bpy.data.objects.new('fill', ld); ob.location = (-7.0, -3.5, 3.2); sc.collection.objects.link(ob)
    from mathutils import Vector as _V
    ob.rotation_euler = (_V((-4.2, 0.6, 1.2)) - _V(ob.location)).to_track_quat('-Z', 'Y').to_euler()

def faceted_rock(G, name, center, size, seed, subdiv=2, amp=0.22, color=('#8f6748', '#7a563c', '#a27757')):
    bpy = G['bpy']; Vector = G['Vector']
    import bmesh
    from mathutils import noise
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=1.0); r = random.Random(seed)
    for v in bm.verts:
        p = v.co.copy(); n = noise.noise(p * 1.7 + Vector((seed, 0, 0))); v.co = Vector((p.x * size[0], p.y * size[1], p.z * size[2])) * (1 + amp * n)
    bm.verts.ensure_lookup_table()
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    cl = me.color_attributes.new('Col', 'BYTE_COLOR', 'CORNER')
    cols = [G['hexc'](c) for c in color]
    for p in me.polygons:
        c = cols[r.randrange(len(cols))]; k = r.uniform(0.85, 1.12) * (1.08 if p.normal.z > 0.5 else 1.0)
        for li in p.loop_indices: cl.data[li].color = (c[0] * k, c[1] * k, c[2] * k, 1)
    me.materials.append(G['mat']('rock', rough=0.85, vcol=True))
    ob = bpy.data.objects.new(name, me); ob.location = center; G['col'].objects.link(ob); return ob

def build_set(G):
    bpy, Vector, MB, mat = G['bpy'], G['Vector'], G['MB'], G['mat']; r = random.Random(7)
    # ground: big warm sand plane with gentle noise
    mb = MB(); sand = mat('sand', '#cf9258', rough=0.9)
    N_ = 30; S_ = 80.0
    def gz(x, y): return 0.0 if (-8 < x < 6 and -6 < y < 8) else 0.15 * math.sin(x * 0.3) * math.cos(y * 0.25)
    for i in range(N_):
        for j in range(N_):
            x0 = -S_ / 2 + S_ * i / N_; y0 = -S_ / 2 + S_ * j / N_; d = S_ / N_
            mb.face([(x0, y0, gz(x0, y0)), (x0 + d, y0, gz(x0 + d, y0)), (x0 + d, y0 + d, gz(x0 + d, y0 + d)), (x0, y0 + d, gz(x0, y0 + d))], sand)
    mb.obj('ground')
    # the cliff with the cave: a big faceted mound, plus boulders framing the mouth
    cl = faceted_rock(G, 'cliff', (6.5, 2.0, 2.0), (6.0, 6.5, 6.8), 3, subdiv=4, amp=0.13)
    import bmesh
    bm = bmesh.new(); bm.from_mesh(cl.data); kill = []
    for f_ in bm.faces:
        c_ = cl.matrix_world @ f_.calc_center_median()
        if c_.x < 3.2 and ((c_.y - 1.0) / 2.5) ** 2 + (max(0.0, c_.z) / 4.5) ** 2 < 1.0: kill.append(f_)
    bmesh.ops.delete(bm, geom=kill, context='FACES'); bm.to_mesh(cl.data); bm.free()
    for k, (c, s) in enumerate((((1.6, -2.6, 0.2), (1.2, 1.0, 1.4)), ((2.0, 4.6, 0.5), (1.8, 1.4, 2.4)), ((-1.4, 7.5, 0.0), (2.4, 2.0, 1.6)),
                                ((-6.5, 6.0, -0.2), (1.6, 1.3, 1.0)), ((-11, -1.0, -0.3), (2.2, 1.8, 1.4)), ((5.0, -5.5, 0.0), (2.0, 1.6, 1.8)))):
        faceted_rock(G, 'boulder%d' % k, c, s, 10 + k, subdiv=2, amp=0.25)
    # cave mouth: a dark arch sunk into the cliff face, rim stones, inner warm gradient
    mouth = bpy.data.materials.new('mouth'); mouth.use_nodes = True; nt = mouth.node_tree; Ln = nt.links.new
    for n_ in list(nt.nodes): nt.nodes.remove(n_)
    o_ = nt.nodes.new('ShaderNodeOutputMaterial'); tc = nt.nodes.new('ShaderNodeTexCoord'); sz = nt.nodes.new('ShaderNodeSeparateXYZ'); Ln(tc.outputs['Object'], sz.inputs[0])
    rp = nt.nodes.new('ShaderNodeValToRGB'); Ln(sz.outputs['Z'], rp.inputs[0]); mp = nt.nodes.new('ShaderNodeMapRange'); mp.inputs['From Min'].default_value = 0.0; mp.inputs['From Max'].default_value = 4.5
    Ln(sz.outputs['Z'], mp.inputs['Value']); Ln(mp.outputs['Result'], rp.inputs[0])
    rp.color_ramp.elements[0].color = G['hexc']('#ff9a3a'); rp.color_ramp.elements[1].position = 0.6; rp.color_ramp.elements[1].color = G['hexc']('#0c0503')
    e_ = rp.color_ramp.elements.new(0.25); e_.color = G['hexc']('#5a1c08')
    em_ = nt.nodes.new('ShaderNodeEmission'); em_.inputs['Strength'].default_value = 1.0; Ln(rp.outputs['Color'], em_.inputs['Color']); Ln(em_.outputs['Emission'], o_.inputs['Surface'])
    mb = MB(); cx, cy = 3.3, 1.0
    arch = [(cy + 2.6 * math.cos(math.pi * k / 20), 0.0 + 4.6 * math.sin(math.pi * k / 20)) for k in range(21)]
    pts = [Vector((cx, y, z)) for y, z in arch]; mb.face(pts[::-1], mouth)
    for k in range(20):                                                          # tunnel walls from the arch back to the dark plane
        (y0, z0), (y1, z1) = arch[k], arch[k + 1]
        mb.face([Vector((0.0, y0 * 1.0, z0)), Vector((0.0, y1, z1)), Vector((cx, y1, z1)), Vector((cx, y0, z0))], mat('tunnel', '#3a2418', rough=1.0))
    inner = mat('inner', '#2a1208', rough=1.0, emit='#ff7a20', estr=0.0)
    mb.obj('mouth')
    for k in range(17):                                                          # rim stones along the arch
        a = math.pi * (k + 0.5) / 17; y = cy + 2.75 * math.cos(a); z = 4.75 * math.sin(a)
        faceted_rock(G, 'rim%d' % k, (0.15, y, z), (0.6, 0.6, 0.65), 40 + k, subdiv=1, amp=0.2)
    # gold: a glowing mound of coins inside the mouth
    gold = mat('gold', '#ffb92e', rough=0.28, metal=1.0, emit='#ff9a1a', estr=1.4); mb = MB(); rg = random.Random(3)
    for k in range(700):
        u, v = rg.random(), rg.random(); a = 2 * math.pi * v; rr = 1.9 * math.sqrt(u); x = 1.7 + rr * math.cos(a) * 0.55; y = cy + rr * math.sin(a)
        z = 0.75 * max(0, 1 - (rr / 1.9) ** 2) + 0.02; n = Vector((rg.uniform(-0.6, 0.6), rg.uniform(-0.6, 0.6), 1)).normalized()
        mb.tube([Vector((x, y, z)), Vector((x, y, z)) + n * 0.02], 0.07, gold, seg=8)
    for k in range(40):                                                          # stray coins on the sand
        x, y = rg.uniform(-5.5, 0.6), rg.uniform(-2.5, 3.5); n = Vector((rg.uniform(-0.3, 0.3), rg.uniform(-0.3, 0.3), 1)).normalized()
        mb.tube([Vector((x, y, 0.01)), Vector((x, y, 0.01)) + n * 0.022], 0.075, gold, seg=10)
    mb.obj('gold', smooth=True)
    ld = bpy.data.lights.new('goldglow', 'POINT'); ld.energy = 900; ld.color = (1.0, 0.62, 0.22); ld.shadow_soft_size = 1.2
    ob = bpy.data.objects.new('goldglow', ld); ob.location = (1.0, cy, 1.3); G['col'].objects.link(ob)
    # crystals
    mb = MB(); cb = mat('crys_b', '#7ad8ff', rough=0.15, emit='#5ac8ff', estr=1.6); cp = mat('crys_p', '#b98cff', rough=0.15, emit='#a070ff', estr=1.6)
    for (x, y, m_) in ((0.2, -1.8, cb), (0.5, 3.9, cp), (-0.3, -2.4, cb)):
        for k in range(5):
            h = rg.uniform(0.35, 0.8); a = rg.uniform(-0.5, 0.5); b = rg.uniform(-0.5, 0.5); base = Vector((x + rg.uniform(-0.2, 0.2), y + rg.uniform(-0.2, 0.2), 0))
            tip = base + Vector((a * h * 0.5, b * h * 0.5, h)); mb.tube([base, base + (tip - base) * 0.75], 0.07, m_, seg=6, cap=True); mb.cone(base + (tip - base) * 0.75, tip, 0.07, m_, seg=6)
    mb.obj('crystals')
    # torch
    mb = MB(); wood = mat('wood', '#6b4426', rough=0.8)
    TX = (-0.9, -1.0); mb.tube([(TX[0], TX[1], 0), (TX[0], TX[1], 1.6)], 0.045, wood, seg=8); mb.tube([(TX[0], TX[1], 1.55), (TX[0], TX[1], 1.72)], [0.06, 0.09], mat('iron', '#3a3a40', rough=0.5, metal=0.6), seg=10)
    mb.obj('torch')
    G['torch'] = (TX[0], TX[1], 1.8)
    ld = bpy.data.lights.new('torchlight', 'POINT'); ld.energy = 120; ld.color = (1.0, 0.6, 0.25); ld.shadow_soft_size = 0.2
    ob = bpy.data.objects.new('torchlight', ld); ob.location = (TX[0] - 0.1, TX[1], 1.95); G['col'].objects.link(ob)
    # far mountains + clouds (camera only feel: big, hazy)
    hz = mat('haze', '#d9a98e', rough=1.0, emit='#e8b494', estr=0.5)
    for k in range(7):
        ob = faceted_rock(G, 'mtn%d' % k, (-60 + k * 18 + r.uniform(-4, 4), 55 + r.uniform(-6, 6), -4), (12 + r.uniform(0, 6), 8, 7 + r.uniform(0, 7)), 70 + k, subdiv=1, amp=0.2)
        ob.data.materials[0] = hz
    for k, (img, c, s) in enumerate((('cloud_a', (-18, 70, 26), 30), ('cloud_b', (-34, 72, 30), 26), ('cloud_a', (10, 75, 34), 34))):
        mb = MB(); cm = mat('cloud%d' % k, img=TX[img] if False else p2tex.os.path.join(HERE, 'tex', img + '.png'), alpha=True, rough=1.0, emit='#fff0e0', estr=0.0)
        mb.quad((c[0] - s / 2, c[1], c[2] - s * 0.19), (s, 0, 0), (0, 0, s * 0.375), cm); o = mb.obj('cloud%d' % k)
    # dragon body + wings (static), behind the heads, inside / above the cave
    D = mat('dragon', '#2c9a2e', rough=0.4, rim='#eaff5a', rim_str=3.2, spec=0.45); Dd = mat('dragon_dk', '#1a6324', rough=0.5, rim='#d4f45a', rim_str=2.0)
    mb = MB(); mb.sphere((3.6, 1.0, 2.4), 1.7, D, seg=20, rings=12, sx=1.0, sy=1.2, sz=1.15); mb.obj('dragon_body', smooth=True)
    mb = MB(); wroot = Vector((3.4, 2.3, 4.6))
    tips = [Vector((2.6, 6.5, 9.0)), Vector((3.6, 8.2, 7.2)), Vector((4.2, 8.8, 5.0)), Vector((4.6, 7.8, 3.4))]
    for a, b in zip(tips[:-1], tips[1:]): mb.face([wroot, a, b], Dd)
    for t_ in tips: mb.tube([wroot, t_], [0.12, 0.05], D, seg=8)
    mb.obj('wing', smooth=False)
    G['D'] = D; G['Dd'] = Dd

# ----------------------------------------------------------------------------- the dragon heads (rebuilt per frame)
def loft(G, mb, frame, secs, m_in, m_out, length, inward_up):
    """secs: (u, half width, top, bottom) along the local forward axis; faces whose normal points 'inward_up' (+1: up, -1: down) get m_in."""
    Vector = G['Vector']; o, f, l, up = frame; seg = 14; rings = []
    for (u, w, top, bot) in secs:
        c = o + f * (u * length); rg = []
        for k in range(seg):
            a = 2 * math.pi * k / seg; ca, sa = math.cos(a), math.sin(a)
            z = (top if sa >= 0 else -bot) * (abs(sa) ** 0.8) * (1 if sa >= 0 else 1); z = top * abs(sa) ** 0.8 if sa >= 0 else bot * abs(sa) ** 0.9
            rg.append(c + l * (w * (abs(ca) ** 0.7) * (1 if ca >= 0 else -1)) + up * z)
        rings.append(rg)
    for i in range(len(rings) - 1):
        for k in range(seg):
            j = (k + 1) % seg; quad = [rings[i][k], rings[i][j], rings[i + 1][j], rings[i + 1][k]]
            n = (quad[1] - quad[0]).cross(quad[3] - quad[0]); n = n.normalized() if n.length > 1e-9 else n
            mb.face(quad, m_in if (n.dot(up) * inward_up) > 0.55 else m_out)
    mb.face(rings[0][::-1], m_out); mb.face(rings[-1], m_out)

def build_heads(G, t, objs):
    bpy, Vector, MB, mat = G['bpy'], G['Vector'], G['MB'], G['mat']
    for o in objs: bpy.data.objects.remove(o, do_unlink=True)
    objs.clear(); D, Dd = G['D'], G['Dd']
    mouth = mat('maw', '#6a1418', rough=0.6); tooth = mat('tooth', '#f6f1e4', rough=0.35, spec=0.6); eye = mat('eye', '#ffe23a', rough=0.2, emit='#ffd21a', estr=5.0)
    pupil = mat('pupil', '#120a06', rough=0.4); horn = mat('horn', '#e8e0c0', rough=0.5)
    target = Vector(HERO) + Vector((0.6, -0.3, 1.6))
    for i, h in enumerate(HEADS):
        off, jaw = head_state(i, t); hp = Vector(h['head']) + Vector(off); base = Vector(h['base'])
        f = (target - hp); f.z *= 0.35; f.normalize(); l = Vector((0, 0, 1)).cross(f).normalized(); up = f.cross(l).normalized()
        L_ = 1.4 - 0.1 * i
        mb = MB()
        # neck: S-curve from the body to the back of the skull
        ctrl = [base, base + Vector((-0.6, 0.0, 0.7)), hp - f * 1.4 + Vector((0, 0, 0.5)), hp - f * 0.35]
        pts = []
        for k in range(17):
            s = k / 16; a = ctrl[0].lerp(ctrl[1], s); b = ctrl[1].lerp(ctrl[2], s); c = ctrl[2].lerp(ctrl[3], s); pts.append(a.lerp(b, s).lerp(b.lerp(c, s), s))
        mb.tube(pts, [0.66 - 0.24 * (k / 16) for k in range(17)], D, seg=18, cap=False)
        for k in range(3, 16, 2):                                               # dorsal spikes along the neck
            p = pts[k]; tng = (pts[min(k + 1, 16)] - pts[k - 1]).normalized(); upn = Vector((0, 0, 1)) - tng * tng.z; upn.normalize()
            rad = 0.62 - 0.3 * (k / 16); mb.cone(p + upn * rad * 0.8, p + upn * (rad + 0.32) - tng * 0.2, 0.09, horn if False else D, seg=6)
        # skull
        o = hp; frame = (o, f, l, up)
        loft(G, mb, frame, [(0.0, 0.44, 0.50, 0.06), (0.22, 0.50, 0.60, 0.0), (0.5, 0.40, 0.40, 0.0), (0.8, 0.29, 0.25, 0.0), (1.0, 0.17, 0.14, 0.0)], mouth, D, L_, -1)
        # lower jaw, hinged near the back
        ang = jaw * 0.85; hinge = o + f * (0.12 * L_) - up * 0.02
        fj = (f * math.cos(ang) - up * math.sin(ang)).normalized(); upj = fj.cross(l).normalized() * -1 if False else l.cross(fj).normalized() * -1
        upj = fj.cross(l) * -1; upj.normalize()
        loft(G, mb, (hinge, fj, l, upj), [(0.0, 0.38, 0.0, -0.30), (0.35, 0.34, 0.0, -0.25), (0.75, 0.23, 0.0, -0.15), (1.0, 0.13, 0.0, -0.08)], mouth, D, L_ * 0.86, 1)
        for side in (-1, 1):                                                    # teeth
            for k, u in enumerate((0.42, 0.55, 0.68, 0.8, 0.9)):
                w = 0.40 - 0.23 * (u - 0.4) / 0.6; big = 1.9 if k == 3 else 1.15
                p = o + f * (u * L_) + l * (side * w * 0.9); mb.cone(p + up * 0.02, p - up * 0.13 * big, 0.035 * big, tooth, seg=6)
                q = hinge + fj * (u * L_ * 0.86) + l * (side * w * 0.8); mb.cone(q - upj * 0.02, q + upj * 0.11 * big, 0.032 * big, tooth, seg=6)
            # eye + slit + angry brow
            e = o + f * (0.3 * L_) + l * (side * 0.42) + up * 0.42
            mb.sphere(e, 0.13, eye, seg=12, rings=8, sx=1.0, sy=1.0, sz=0.85)
            mb.box(tuple(e + l * side * 0.085 - up * 0.07 - f * 0.012), tuple(e + l * side * 0.105 + up * 0.07 + f * 0.012), pupil) if False else None
            sl = MB if False else None
            mb.tube([e + l * side * 0.12 - up * 0.085, e + l * side * 0.12 + up * 0.085], 0.022, pupil, seg=6)
            b0 = e + up * 0.15 - f * 0.16 + l * side * 0.02; b1 = e + up * 0.05 + f * 0.2 + l * side * 0.08
            mb.tube([b0, b1], [0.09, 0.05], Dd, seg=8)
            # horns + cheek spikes
            hb = o + f * (0.05 * L_) + l * side * 0.28 + up * 0.48; mb.cone(hb, hb - f * 0.7 + up * 0.35 + l * side * 0.15, 0.08, horn, seg=8)
            cb = o + f * (0.12 * L_) + l * side * 0.46 + up * 0.05; mb.cone(cb, cb - f * 0.45 + l * side * 0.18, 0.06, D, seg=6)
            n_ = o + f * (0.97 * L_) + l * side * 0.06 + up * 0.1; mb.sphere(n_, 0.025, pupil, seg=6, rings=4)
        objs.append(mb.obj('head%d' % i, smooth=True))

# ----------------------------------------------------------------------------- the hero (rebuilt per frame)
def build_hero(G, t, objs, cam_loc):
    bpy, Vector, MB, mat = G['bpy'], G['Vector'], G['MB'], G['mat']
    for o in objs: bpy.data.objects.remove(o, do_unlink=True)
    objs.clear(); p, face = hero_pose(t)
    suit = mat('suit', '#22346e', rough=0.55, rim='#ffd9a0', rim_str=0.6); skin = mat('skin', '#f1c49c', rough=0.6); shoe = mat('shoe', '#141418', rough=0.35)
    plank = mat('plank', img=TX['planks'], rough=0.7, rim='#ffd9a0', rim_str=0.5); lid = mat('lid', img=TX['lid'], rough=0.7); band = mat('band', '#5a5c66', rough=0.35, metal=0.8)
    front = mat('suitfront', img=TX['suit'], rough=0.55); fdec = mat('face_' + face, img=TX['face_' + face], alpha=True, rough=0.6)
    fwd = Vector((1, -0.55, 0)).normalized(); lat = Vector((0, 0, 1)).cross(fwd).normalized(); up = Vector((0, 0, 1))
    def W(v): return fwd * v[0] + lat * v[1] + up * v[2]
    root = Vector(HERO) + up * p['bob']; mb = MB()
    pelvis = root + up * 0.86; lean = p['lean']; tor_up = (up + fwd * lean).normalized(); neck = pelvis + tor_up * 0.52
    # legs: front (right, toward the dragon) and back
    for nm, side in (('f', -1), ('b', 1)):
        hip = pelvis + lat * side * 0.1; knee = hip + W(p['thigh_' + nm]) * 0.45; ank = knee + W(p['shin_' + nm]) * 0.45
        mb.tube([hip, knee, ank], 0.065, suit, seg=10); fd = fwd if nm == 'f' else (fwd * 0.6 - lat * 0.2).normalized()
        mb.box(tuple(Vector((min(ank.x, (ank + fd * 0.2).x) - 0.03, min(ank.y, (ank + fd * 0.2).y) - 0.05, 0.0))), tuple(Vector((max(ank.x, (ank + fd * 0.2).x) + 0.03, max(ank.y, (ank + fd * 0.2).y) + 0.05, 0.09))), shoe)
    # torso: a tapered box (jacket) with the shirt/tie front
    hw0, hw1, dp = 0.19, 0.25, 0.13
    c = [pelvis - lat * hw0 - fwd * dp, pelvis + lat * hw0 - fwd * dp, pelvis + lat * hw0 + fwd * dp, pelvis - lat * hw0 + fwd * dp]
    d = [neck - lat * hw1 - fwd * dp, neck + lat * hw1 - fwd * dp, neck + lat * hw1 + fwd * dp, neck - lat * hw1 + fwd * dp]
    mb.face([c[3], c[2], d[2], d[3]], front, [(1, 0), (0, 0), (0, 1), (1, 1)])
    for a, b in ((0, 1), (1, 2), (3, 0)): mb.face([c[a], c[b], d[b], d[a]], suit)
    mb.face(d, suit); mb.face(c[::-1], suit)
    # arms
    for nm, side in (('r', -1), ('l', 1)):
        sh = neck - up * 0.06 + lat * side * 0.24; el = sh + W(p['up_' + nm]) * 0.3; wr = el + W(p['lo_' + nm]) * 0.28
        mb.tube([sh, el, wr], 0.055, suit, seg=10); mb.sphere(wr + W(p['lo_' + nm]) * 0.05, 0.055, skin, seg=10, rings=6)
        if nm == 'l': G['hand_l'] = wr + W(p['lo_' + nm]) * 0.07
    mb.tube([neck, neck + up * 0.06], 0.05, skin, seg=8, cap=False)
    # barrel head
    hc = neck + up * 0.3; tilt = p['head_tilt']; hf = (fwd + up * tilt * 0.3).normalized(); hl = lat; hu = hf.cross(hl) * -1; hu = hl.cross(hf); hu.normalize()
    bw, bh, bd = 0.25, 0.27, 0.23
    def B(x, y, z): return hc + hf * x + hl * y + hu * z
    sides = [((bd, -bw), (bd, bw)), ((bd, bw), (-bd, bw)), ((-bd, bw), (-bd, -bw)), ((-bd, -bw), (bd, -bw))]
    for k, ((x0, y0), (x1, y1)) in enumerate(sides):
        mb.face([B(x0, y0, -bh), B(x1, y1, -bh), B(x1, y1, bh), B(x0, y0, bh)], plank, [(0, 0), (1, 0), (1, 1), (0, 1)])
    mb.face([B(bd, -bw, bh), B(bd, bw, bh), B(-bd, bw, bh), B(-bd, -bw, bh)], lid, [(0, 0), (1, 0), (1, 1), (0, 1)])
    mb.face([B(bd, bw, -bh), B(bd, -bw, -bh), B(-bd, -bw, -bh), B(-bd, bw, -bh)], plank)
    for z in (-bh * 0.68, bh * 0.68):                                                  # metal bands
        for (x0, y0), (x1, y1) in sides:
            mb.face([B(x0 * 1.03, y0 * 1.03, z - 0.025), B(x1 * 1.03, y1 * 1.03, z - 0.025), B(x1 * 1.03, y1 * 1.03, z + 0.025), B(x0 * 1.03, y0 * 1.03, z + 0.025)], band)
    # the face decal: on the barrel side that faces the camera most (front or the near side)
    to_cam = (Vector(cam_loc) - hc); to_cam.z = 0; to_cam.normalize()
    if to_cam.dot(-hl) > to_cam.dot(hf):                                             # near side (his right)
        mb.face([B(bd * 1.0, -bw * 1.035, -bh * 0.95), B(-bd * 1.0, -bw * 1.035, -bh * 0.95), B(-bd * 1.0, -bw * 1.035, bh * 0.95), B(bd * 1.0, -bw * 1.035, bh * 0.95)], fdec, [(1, 0), (0, 0), (0, 1), (1, 1)])
    else:
        mb.face([B(bd * 1.035, bw * 1.0, -bh * 0.95), B(bd * 1.035, -bw * 1.0, -bh * 0.95), B(bd * 1.035, -bw * 1.0, bh * 0.95), B(bd * 1.035, bw * 1.0, bh * 0.95)], fdec, [(0, 0), (1, 0), (1, 1), (0, 1)])
    objs.append(mb.obj('hero', smooth=False))
    # the insurance paper in his raised left hand, facing between the camera and the dragon
    if p['paper'] > 0.5:
        pm = mat('paper', img=TX['paper'], alpha=True, rough=0.8, emit='#ffd27a', estr=0.0); h = G['hand_l']
        glow = max(0.0, min(1.0, (t - 11.0) / 0.6)); pm.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value = 1.6 * glow
        if glow > 0: pm.node_tree.nodes['Principled BSDF'].inputs['Emission Color'].default_value = G['hexc']('#ffd27a')
        nrm = ((Vector(cam_loc) - h).normalized() * 2 + Vector((1, 0, 0))).normalized(); pl = Vector((0, 0, 1)).cross(nrm).normalized(); pu = nrm.cross(pl) * -1; pu = pl.cross(nrm) * -1
        pu = nrm.cross(pl).normalized() * -1 if False else Vector((0, 0, 1)) - nrm * nrm.z; pu.normalize()
        w_, h_ = 0.46, 0.58; c0 = h + pu * 0.05 - pl * w_ * 0.15
        mb2 = MB(); mb2.face([c0 - pl * w_ / 2, c0 + pl * w_ / 2, c0 + pl * w_ / 2 + pu * h_, c0 - pl * w_ / 2 + pu * h_], pm, [(1, 0), (0, 0), (0, 1), (1, 1)])
        mb2.face([c0 - pl * w_ / 2 + pu * h_, c0 + pl * w_ / 2 + pu * h_, c0 + pl * w_ / 2, c0 - pl * w_ / 2], mat('paperback', '#efe0bc', rough=0.9))
        objs.append(mb2.obj('paper'))
        G['paper_c'] = c0 + pu * h_ / 2

def torch_flame(G, t, objs):
    bpy, Vector, MB, mat = G['bpy'], G['Vector'], G['MB'], G['mat']
    for o in objs: bpy.data.objects.remove(o, do_unlink=True)
    objs.clear(); c = Vector(G['torch']); mb = MB(); f1 = mat('flame1', '#ffcc40', emit='#ffb020', estr=14.0); f2 = mat('flame2', '#ffffff', emit='#fff2c0', estr=24.0)
    s = 1 + 0.12 * math.sin(t * 23) + 0.08 * math.sin(t * 37)
    mb.sphere(c, 0.1, f1, seg=10, rings=7, sx=1, sy=1, sz=1.0); mb.cone(c + Vector((0, 0, 0.05)), c + Vector((0.03 * math.sin(t * 9), 0, 0.42 * s)), 0.1, f1, seg=10)
    mb.sphere(c + Vector((0, 0, 0.02)), 0.05, f2, seg=8, rings=5); objs.append(mb.obj('flame'))
    sp = mat('sparkle', '#ffffff', emit='#fff6d0', estr=20.0); mb = MB(); r = random.Random(int(t * FPS) // 3)
    for k in range(18):                                                              # gold glints
        p = Vector((1.5 + r.uniform(-0.6, 0.4), 1.0 + r.uniform(-1.6, 1.6), r.uniform(0.2, 1.1))); s_ = r.uniform(0.02, 0.05)
        mb.face([p + Vector((0, -s_ * 3, 0)), p + Vector((0, 0, s_ * 0.4)), p + Vector((0, s_ * 3, 0)), p + Vector((0, 0, -s_ * 0.4))], sp)
        mb.face([p + Vector((0, -s_ * 0.4, 0)), p + Vector((0, 0, s_ * 3)), p + Vector((0, s_ * 0.4, 0)), p + Vector((0, 0, -s_ * 3))], sp)
    objs.append(mb.obj('glints'))

def cam_at(keys, t):
    if t <= keys[0][0]: return keys[0][1], keys[0][2], keys[0][3]
    a, b = keys[0], keys[-1]; u = ease((t - a[0]) / (b[0] - a[0]))
    L = lambda x, y: tuple(x[i] + (y[i] - x[i]) * u for i in range(3))
    return L(a[1], b[1]), L(a[2], b[2]), a[3] + (b[3] - a[3]) * u

def render(shot_name, frames, out_dir, draft=False, single=None):
    import bpy
    from mathutils import Vector
    G = blender_build(); sc = bpy.context.scene
    if draft: sc.render.resolution_percentage = 50; sc.cycles.samples = 8
    sh = [s for s in SHOTS if s['n'] == shot_name][0]
    cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd); sc.collection.objects.link(cam); sc.camera = cam
    cd.sensor_fit = 'HORIZONTAL'; cd.sensor_width = 36; cd.clip_end = 500
    H_, Hh, F_ = [], [], []
    os.makedirs(out_dir, exist_ok=True)
    for g in frames:
        t = g / FPS; loc, look, lens = cam_at(sh['keys'], t)
        if shot_name == 'S2' and 2.95 < t < 3.6: r = random.Random(g); amp = 0.05 * (1 - (t - 2.95) / 0.65); loc = tuple(v + r.uniform(-amp, amp) for v in loc)
        cam.location = loc; fwd = (Vector(look) - Vector(loc)).normalized(); cam.rotation_euler = fwd.to_track_quat('-Z', 'Y').to_euler(); cd.lens = lens
        build_heads(G, t, H_); build_hero(G, t, Hh, loc); torch_flame(G, t, F_)
        if sh['dof']:
            cd.dof.use_dof = True; cd.dof.aperture_fstop = sh['dof']
            foc = Vector(HERO) + Vector((0, 0, 1.4)) if shot_name in ('S3', 'S4') else Vector(HEADS[1]['head'])
            cd.dof.focus_distance = max(0.5, (foc - Vector(loc)).dot(fwd))
        else: cd.dof.use_dof = False
        sc.render.filepath = single or os.path.join(out_dir, 'f_%04d.jpg' % g); bpy.ops.render.render(write_still=True); print('frame', g, shot_name, flush=True)

def frames_of(sh): return [g for g in range(N) if sh['t0'] <= g / FPS < sh['t1']]

if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'still':
        sh, t = sys.argv[2], float(sys.argv[3]); out = sys.argv[4] if len(sys.argv) > 4 and not sys.argv[4].startswith('--') else os.path.join(HERE, 'still_%s_%.1f.png' % (sh, t))
        render(sh, [int(round(t * FPS))], HERE, draft='--draft' in sys.argv, single=out)
    elif c == 'render':
        sh = [s for s in SHOTS if s['n'] == sys.argv[2]][0]; ev = int(sys.argv[sys.argv.index('--every') + 1]) if '--every' in sys.argv else 1
        fr = [g for g in frames_of(sh)[::ev] if not os.path.exists(os.path.join(RAW, 'f_%04d.jpg' % g))]
        render(sh['n'], fr, RAW, draft='--draft' in sys.argv)
    elif c == 'plan':
        for s in SHOTS: print(s['n'], s['t0'], s['t1'], len(frames_of(s)))

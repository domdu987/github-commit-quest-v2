#!/usr/bin/env python3
"""kit.py : reusable, cheap, grounded set-piece library for the path-traced looks (bpy 5.x, Cycles).  Usable from any set module:

    import sys; sys.path.insert(0, '.../v3/kit'); import kit as K
    K.use(collection)                                   # where new objects go (default: the scene collection)
    K.planks_ground((x0, y0, x1, y1), z, seed=1)        # individual planks with gaps, worn tones
    K.stones_ground(...), K.wet_patches(...), K.mud_patches(...), K.grass_cracks(...)
    K.rope_coil(c), K.crate(c), K.barrel(c), K.net_pile(c), K.net_hang(p0, p1), K.lantern(c), K.brazier(c)   # props + warm light pools
    K.gobo_rigging(c, yaw), K.gobo_canopy(c)            # off-screen shadow casters (invisible to the camera, cast shadows and block sun shafts)
    K.pine_cluster(c, n, radius, zfun), K.rock_cluster(c, n, radius, zfun)
    rig = K.cannon(c, yaw) / K.muzzle_rig(pos, dir);  K.fire_muzzle(rig, t, frame=f)         # flash light + flash + smoke ring + recoil puff
    ex = K.explosion_rig(pos, water_z=0.0);  K.set_explosion(ex, t, frame=f)                   # fireball, debris arcs, water column, shockwave, embers, smoke
    fr = K.fire_patch(points);  K.set_fire(fr, level, frame=f)                                 # flames on rigging / sails + embers
Every animated function takes t (seconds since the event, < 0 = not yet) or a level and an optional frame= (keys it).  Positions are world
(or parent-local when parent= is given).  Nothing is parented to a camera.  Debris lands on the ground plane or splashes into the water.
1 unit = 1 D (head) as in the film sets; z up."""
import math, random
import bpy
from mathutils import Vector, Matrix

COLL = None
G = 9.8 * 1.9              # gravity in D / s^2 (1 D ~ 0.53 m)
def use(coll): global COLL; COLL = coll
def _coll(): return COLL or bpy.context.scene.collection
def rnd(seed): return random.Random(seed)
def hexl(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]; return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)

# ----------------------------------------------------------------------------- materials (Principled; names start with K_)
def _tree(m):
    m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != 'OUTPUT_MATERIAL': nt.nodes.remove(n)
    return nt, [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]

def kmat(name, hexcol, rough=0.7, metal=0.0, var=0.0, bump=0.0, emit=None, emit_k=0.0):
    """Principled colour; var = per-object random tone (Object Info) so repeated props never look cloned; bump = noise bump strength."""
    nm = 'K_' + name
    if nm in bpy.data.materials: return bpy.data.materials[nm]
    m = bpy.data.materials.new(nm); nt, out = _tree(m); N = nt.nodes.new; L = nt.links.new
    p = N('ShaderNodeBsdfPrincipled'); p.inputs['Roughness'].default_value = rough; p.inputs['Metallic'].default_value = metal
    col = (*hexl(hexcol), 1.0)
    if var > 0:
        oi = N('ShaderNodeObjectInfo'); tc = N('ShaderNodeTexCoord'); nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.7; L(tc.outputs['Object'], nz.inputs['Vector'])
        ad = N('ShaderNodeMath'); ad.operation = 'MULTIPLY_ADD'; ad.inputs[1].default_value = 0.6; L(oi.outputs['Random'], ad.inputs[0]); L(nz.outputs['Fac'], ad.inputs[2])
        rm = N('ShaderNodeMapRange'); rm.inputs['From Min'].default_value = 0.2; rm.inputs['From Max'].default_value = 1.4; rm.inputs['To Min'].default_value = 1 - var; rm.inputs['To Max'].default_value = 1 + var * 0.6; L(ad.outputs[0], rm.inputs['Value'])
        mx = N('ShaderNodeVectorMath'); mx.operation = 'SCALE'; mx.inputs[0].default_value = col[:3]; L(rm.outputs['Result'], mx.inputs['Scale']); L(mx.outputs[0], p.inputs['Base Color'])
    else: p.inputs['Base Color'].default_value = col
    if bump > 0:
        tc = N('ShaderNodeTexCoord'); nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 6.0; nz.inputs['Detail'].default_value = 3.0; L(tc.outputs['Object'], nz.inputs['Vector'])
        bp = N('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; bp.inputs['Distance'].default_value = 0.05; L(nz.outputs['Fac'], bp.inputs['Height']); L(bp.outputs['Normal'], p.inputs['Normal'])
    if emit is not None:
        p.inputs['Emission Color'].default_value = (*hexl(emit), 1.0); p.inputs['Emission Strength'].default_value = emit_k
    L(p.outputs[0], out.inputs['Surface']); return m

def kglow(name, hexcol, k=6.0):
    """pure emission (flames, lamp glass, flash, embers); a Value node 'k' scales the strength (keyable)."""
    nm = 'K_e_' + name
    if nm in bpy.data.materials: return bpy.data.materials[nm]
    m = bpy.data.materials.new(nm); nt, out = _tree(m); N = nt.nodes.new; L = nt.links.new
    v = N('ShaderNodeValue'); v.name = 'k'; v.outputs[0].default_value = k; e = N('ShaderNodeEmission'); e.inputs['Color'].default_value = (*hexl(hexcol), 1.0); L(v.outputs[0], e.inputs['Strength'])
    L(e.outputs[0], out.inputs['Surface']); m.cycles.emission_sampling = 'NONE'; return m

def ksoft(name, hexcol, opacity=0.62, emit_k=0.0, emit_col=None):
    """soft billow: Principled with a facing-ratio alpha falloff (overlapping lumps merge into one soft cloud); optional glow (fireball)."""
    nm = 'K_s_' + name
    if nm in bpy.data.materials: return bpy.data.materials[nm]
    m = bpy.data.materials.new(nm); nt, out = _tree(m); N = nt.nodes.new; L = nt.links.new
    lw = N('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.5; s1 = N('ShaderNodeMath'); s1.operation = 'SUBTRACT'; s1.inputs[0].default_value = 1.0; L(lw.outputs['Facing'], s1.inputs[1])
    pw = N('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 1.4; L(s1.outputs[0], pw.inputs[0])
    op = N('ShaderNodeValue'); op.name = 'op'; op.outputs[0].default_value = opacity; al = N('ShaderNodeMath'); al.operation = 'MULTIPLY'; al.use_clamp = True; L(pw.outputs[0], al.inputs[0]); L(op.outputs[0], al.inputs[1])
    p = N('ShaderNodeBsdfPrincipled'); p.inputs['Base Color'].default_value = (*hexl(hexcol), 1.0); p.inputs['Roughness'].default_value = 1.0; L(al.outputs[0], p.inputs['Alpha'])
    p.inputs['Emission Color'].default_value = (*hexl(emit_col or hexcol), 1.0); p.inputs['Emission Strength'].default_value = emit_k if emit_k else 0.15
    L(p.outputs[0], out.inputs['Surface']); return m

def kline(name, hexcol):
    return kmat(name, hexcol, 0.9)

# ----------------------------------------------------------------------------- mesh builder
class MB:
    def __init__(s): s.v = []; s.f = []; s.m = []; s.mats = []
    def _mi(s, mat):
        if mat not in s.mats: s.mats.append(mat)
        return s.mats.index(mat)
    def face(s, pts, mat):
        i0 = len(s.v); s.v += [tuple(p) for p in pts]; s.f.append(tuple(range(i0, i0 + len(pts)))); s.m.append(s._mi(mat))
    def obox(s, c, X, Y, Z, hx, hy, hz, mat):
        c = Vector(c); X, Y, Z = Vector(X), Vector(Y), Vector(Z); P = lambda a, b, d: c + X * (a * hx) + Y * (b * hy) + Z * (d * hz)
        for q in (((-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1)), ((-1, -1, 1), (-1, 1, 1), (1, 1, 1), (1, -1, 1)), ((-1, -1, -1), (-1, -1, 1), (1, -1, 1), (1, -1, -1)),
                  ((1, 1, -1), (1, 1, 1), (-1, 1, 1), (-1, 1, -1)), ((-1, 1, -1), (-1, 1, 1), (-1, -1, 1), (-1, -1, -1)), ((1, -1, -1), (1, -1, 1), (1, 1, 1), (1, 1, -1))):
            s.face([P(*a) for a in q], mat)
    def box(s, c, hx, hy, hz, mat, yaw=0.0):
        a = math.radians(yaw); s.obox(c, (math.cos(a), math.sin(a), 0), (-math.sin(a), math.cos(a), 0), (0, 0, 1), hx, hy, hz, mat)
    def beam(s, p0, p1, w, h, mat):
        p0, p1 = Vector(p0), Vector(p1); X = (p1 - p0); Ln = X.length; X.normalize(); Y = Vector((0, 0, 1)).cross(X)
        if Y.length < 1e-4: Y = Vector((0, 1, 0)).cross(X)
        Y.normalize(); Z = X.cross(Y); s.obox((p0 + p1) / 2, X, Y, Z, Ln / 2, w / 2, h / 2, mat)
    def cyl(s, p0, p1, r0, r1, mat, seg=8, cap=True):
        p0, p1 = Vector(p0), Vector(p1); a = (p1 - p0).normalized(); u = a.cross(Vector((0, 0, 1)))
        if u.length < 1e-4: u = Vector((1, 0, 0))
        u.normalize(); w = a.cross(u); R = lambda p, r: [p + (u * math.cos(2 * math.pi * i / seg) + w * math.sin(2 * math.pi * i / seg)) * r for i in range(seg)]
        A, B = R(p0, r0), R(p1, r1)
        for i in range(seg): j = (i + 1) % seg; s.face([A[i], A[j], B[j], B[i]], mat)
        if cap and r0 > 0: s.face(A[::-1], mat)
        if cap and r1 > 0: s.face(B, mat)
    def lump(s, c, r, mat, seed, seg=8, rings=5, rough=0.2, squash=1.0, sx=1.0):
        rs = rnd(seed); c = Vector(c); R = []
        for k in range(rings + 1):
            th = math.pi * k / rings; row = []
            for i in range(seg):
                ph = 2 * math.pi * i / seg; d = Vector((math.sin(th) * math.cos(ph) * sx, math.sin(th) * math.sin(ph), -math.cos(th) * squash))
                row.append(c + d * r * (1 + rs.uniform(-rough, rough) if 0 < k < rings else 1.0))
            R.append(row)
        for k in range(rings):
            for i in range(seg): j = (i + 1) % seg; s.face([R[k][i], R[k][j], R[k + 1][j], R[k + 1][i]], mat)
    def torus(s, c, R, r, mat, segs=16, sides=5):
        c = Vector(c); P = [[c + Vector((math.cos(2 * math.pi * i / segs) * (R + r * math.cos(2 * math.pi * j / sides)), math.sin(2 * math.pi * i / segs) * (R + r * math.cos(2 * math.pi * j / sides)), r * math.sin(2 * math.pi * j / sides))) for j in range(sides)] for i in range(segs)]
        for i in range(segs):
            for j in range(sides): i2, j2 = (i + 1) % segs, (j + 1) % sides; s.face([P[i][j], P[i2][j], P[i2][j2], P[i][j2]], mat)
    def disc(s, c, r, mat, seg=16, z=0.0, irregular=0.0, seed=0):
        rs = rnd(seed); c = Vector(c); pts = [c + Vector((math.cos(2 * math.pi * i / seg) * r * (1 + rs.uniform(-irregular, irregular)), math.sin(2 * math.pi * i / seg) * r * (1 + rs.uniform(-irregular, irregular)), z)) for i in range(seg)]
        s.face(pts, mat)

def obj(mb, name, parent=None, loc=None, rot=None, shadow=True, camera=True, smooth=False, sub=0):
    me = bpy.data.meshes.new(name); me.from_pydata(mb.v, [], mb.f); me.update()
    for mt in mb.mats: me.materials.append(mt)
    for i, p in enumerate(me.polygons): p.material_index = mb.m[i]; p.use_smooth = smooth
    ob = bpy.data.objects.new(name, me); _coll().objects.link(ob)
    if parent is not None: ob.parent = parent
    if loc is not None: ob.location = loc
    if rot is not None: ob.rotation_euler = rot
    ob.visible_shadow = shadow; ob.visible_camera = camera
    if sub: md = ob.modifiers.new('ss', 'SUBSURF'); md.levels = md.render_levels = sub
    return ob

def _key(ob, path, frame, interp='LINEAR'):
    if frame is None: return
    ob.keyframe_insert(path, frame=frame)
    ad = ob.animation_data
    if ad and ad.action:
        for layer in ad.action.layers:
            for strip in layer.strips:
                cb = strip.channelbag(ad.action_slot)
                for fc in (cb.fcurves if cb else []):
                    if fc.data_path == path:
                        for kp in fc.keyframe_points:
                            if int(round(kp.co.x)) == int(frame): kp.interpolation = interp

def _show(ob, vis, frame):
    ob.hide_render = not vis
    if frame is not None: ob.keyframe_insert('hide_render', frame=frame)

def _setv(m, node, v, frame):
    s = m.node_tree.nodes[node].outputs[0]; s.default_value = v
    if frame is not None: s.keyframe_insert('default_value', frame=frame)

def _light(name, kind, color, energy, loc, radius=0.25, parent=None):
    d = bpy.data.lights.new(name, kind); d.color = color; d.energy = energy; d.shadow_soft_size = radius
    o = bpy.data.objects.new(name, d); _coll().objects.link(o); o.location = loc
    if parent is not None: o.parent = parent
    return o

# ============================================================================= lived-in ground
def planks_ground(rect, z, seed=1, along='x', w=0.55, gap=0.05, th=0.12, tones=('#9a7149', '#86603d', '#a8805a', '#7a5537'), name='k_planks', parent=None):
    """Deck / quay of individual planks (random lengths, butt joints, slight height and tilt jitter, 4 worn tones)."""
    x0, y0, x1, y1 = rect; rs = rnd(seed); mats = [kmat('plank%d' % i, t, 0.78, var=0.08, bump=0.25) for i, t in enumerate(tones)]; mb = MB()
    a0, a1, b0, b1 = (x0, x1, y0, y1) if along == 'x' else (y0, y1, x0, x1); b = b0
    while b < b1 - 0.05:
        a = a0
        while a < a1 - 0.05:
            Ln = min(a1 - a, rs.uniform(2.2, 5.5)); zz = z - th / 2 + rs.uniform(-0.012, 0.012); c = ((a + Ln / 2, b + w / 2, zz) if along == 'x' else (b + w / 2, a + Ln / 2, zz))
            mb.box(c, (Ln / 2 - gap / 2) if along == 'x' else (w / 2 - gap / 2), (w / 2 - gap / 2) if along == 'x' else (Ln / 2 - gap / 2), th / 2, mats[rs.randrange(len(mats))])
            a += Ln
        b += w
    return obj(mb, name, parent)

def stones_ground(rect, z, size=0.75, seed=2, tones=('#9b9388', '#857e74', '#a99f90', '#6f6a62'), mud='#5d4a36', name='k_stones', parent=None):
    """Cobbles: flattened lumps on a jittered grid with a mud bed between them."""
    x0, y0, x1, y1 = rect; rs = rnd(seed); mats = [kmat('stone%d' % i, t, 0.9, var=0.1, bump=0.4) for i, t in enumerate(tones)]; mb = MB()
    mb.face([(x0, y0, z - 0.05), (x1, y0, z - 0.05), (x1, y1, z - 0.05), (x0, y1, z - 0.05)], kmat('mudbed', mud, 0.95, bump=0.3))
    y = y0 + size / 2; row = 0
    while y < y1:
        x = x0 + size / 2 + (size / 2 if row % 2 else 0)
        while x < x1:
            r = size * rs.uniform(0.42, 0.52); mb.lump((x + rs.uniform(-0.08, 0.08) * size, y + rs.uniform(-0.08, 0.08) * size, z - 0.05 + r * 0.25), r, mats[rs.randrange(len(mats))], rs.randrange(9999), seg=7, rings=4, rough=0.15, squash=0.32)
            x += size
        y += size * 0.92; row += 1
    return obj(mb, name, parent, smooth=True)

def _patches(rect_or_pts, z, n, r, mat, seed, name, parent, zfun=None):
    rs = rnd(seed); mb = MB()
    pts = rect_or_pts if isinstance(rect_or_pts, list) else [(rs.uniform(rect_or_pts[0], rect_or_pts[2]), rs.uniform(rect_or_pts[1], rect_or_pts[3])) for _ in range(n)]
    for i, (x, y) in enumerate(pts):
        zz = zfun(x, y) if zfun else z; mb.disc((x, y, zz + 0.014), r * rs.uniform(0.6, 1.4), mat, seg=14, irregular=0.35, seed=seed * 31 + i)
    return obj(mb, name, parent, shadow=False)

def wet_patches(rect, z, n=8, r=1.2, seed=3, name='k_wet', parent=None, zfun=None):
    """dark glossy puddles / wet planks (they mirror the low sun: amber streaks in look C)."""
    m = kmat('wet', '#2b2622', 0.06); return _patches(rect, z, n, r, m, seed, name, parent, zfun)

def mud_patches(rect, z, n=6, r=1.4, seed=4, name='k_mud', parent=None, zfun=None):
    m = kmat('mud', '#4e3b29', 0.55, bump=0.6); return _patches(rect, z, n, r, m, seed, name, parent, zfun)

def grass_cracks(rect, z, n=40, seed=5, name='k_grass', parent=None, zfun=None):
    """small grass tufts (5 thin blades each) in cracks and along edges."""
    rs = rnd(seed); mb = MB(); ms = [kmat('grass0', '#6b8a3a', 0.8), kmat('grass1', '#8a9a44', 0.8)]
    for i in range(n):
        x, y = rs.uniform(rect[0], rect[2]), rs.uniform(rect[1], rect[3]); zz = zfun(x, y) if zfun else z
        for k in range(5):
            a = rs.uniform(0, 6.283); h = rs.uniform(0.22, 0.5); mb.cyl((x, y, zz - 0.02), (x + math.cos(a) * 0.12, y + math.sin(a) * 0.12, zz + h), 0.035, 0.0, ms[k % 2], seg=3, cap=False)
    return obj(mb, name, parent, shadow=True)

# ============================================================================= props
def rope_coil(c, r=0.8, layers=3, name='k_rope', parent=None):
    mb = MB(); m = kmat('rope', '#b39461', 0.95, var=0.1)
    for k in range(layers): mb.torus((c[0], c[1], c[2] + 0.12 + 0.19 * k), r - 0.06 * k, 0.1, m); mb.torus((c[0], c[1], c[2] + 0.12 + 0.19 * k), r * 0.6 - 0.05 * k, 0.1, m)
    return obj(mb, name, parent, smooth=True)

def crate(c, s=1.0, yaw=0.0, name='k_crate', parent=None):
    mb = MB(); m = kmat('crate', '#a37a4a', 0.8, var=0.15, bump=0.3); d = kmat('crate_d', '#6b4b2c', 0.8)
    mb.box((c[0], c[1], c[2] + 0.5 * s), 0.5 * s, 0.5 * s, 0.5 * s, m, yaw)
    for dz in (0.12, 0.88): mb.box((c[0], c[1], c[2] + dz * s), 0.53 * s, 0.53 * s, 0.05 * s, d, yaw)
    return obj(mb, name, parent)

def barrel(c, r=0.5, h=1.25, lying=False, yaw=0.0, name='k_barrel', parent=None):
    mb = MB(); m = kmat('barrel', '#8c6239', 0.75, var=0.12, bump=0.3); hoop = kmat('hoop', '#33302c', 0.4, metal=0.6)
    if lying:
        a = math.radians(yaw); d = Vector((math.cos(a), math.sin(a), 0)); c0 = Vector(c) + Vector((0, 0, r)); p0, p1 = c0 - d * h / 2, c0 + d * h / 2
        mb.cyl(p0, (p0 + p1) / 2, r * 0.88, r, m, 12); mb.cyl((p0 + p1) / 2, p1, r, r * 0.88, m, 12)
        for t in (0.12, 0.88): q = p0 + (p1 - p0) * t; mb.cyl(q - d * 0.04, q + d * 0.04, r * 0.95, r * 0.95, hoop, 12)
    else:
        c0 = Vector(c); mb.cyl(c0, c0 + Vector((0, 0, h / 2)), r * 0.88, r, m, 12); mb.cyl(c0 + Vector((0, 0, h / 2)), c0 + Vector((0, 0, h)), r, r * 0.88, m, 12)
        for t in (0.12, 0.88): q = c0 + Vector((0, 0, h * t)); mb.cyl(q - Vector((0, 0, 0.04)), q + Vector((0, 0, 0.04)), r * 0.95, r * 0.95, hoop, 12)
    return obj(mb, name, parent, smooth=True)

def net_pile(c, r=1.0, seed=6, name='k_net', parent=None):
    mb = MB(); m = kmat('net', '#7a6a4c', 0.95, var=0.1); f = kmat('float', '#c9a35b', 0.6)
    mb.lump((c[0], c[1], c[2] + 0.18), r, m, seed, seg=10, rings=4, rough=0.3, squash=0.3)
    rs = rnd(seed)
    for k in range(5): a = rs.uniform(0, 6.28); mb.lump((c[0] + math.cos(a) * r * 0.8, c[1] + math.sin(a) * r * 0.8, c[2] + 0.12), 0.12, f, seed + k, 6, 4, 0.1)
    return obj(mb, name, parent, smooth=True)

def net_hang(p0, p1, drop=1.4, n=10, m_=6, name='k_nethang', parent=None):
    """a fishing net hung between two posts: a sagging grid of thin strands."""
    mb = MB(); m = kmat('net', '#7a6a4c', 0.95); p0, p1 = Vector(p0), Vector(p1)
    for i in range(n + 1):
        u = i / n; top = p0 + (p1 - p0) * u - Vector((0, 0, 0.35 * math.sin(math.pi * u))); mb.beam(top, top - Vector((0, 0, drop * (0.8 + 0.2 * math.sin(3 * u)))), 0.025, 0.025, m)
    for j in range(1, m_ + 1):
        v = j / m_; pts = [p0 + (p1 - p0) * (i / n) - Vector((0, 0, 0.35 * math.sin(math.pi * i / n) + drop * v * (0.8 + 0.2 * math.sin(3 * i / n)))) for i in range(n + 1)]
        for a, b in zip(pts, pts[1:]): mb.beam(a, b, 0.025, 0.025, m)
    for p in (p0, p1): mb.cyl(p - Vector((0, 0, p.z - (p.z - 3.2))), p + Vector((0, 0, 0.2)), 0.08, 0.08, kmat('post', '#5e432c', 0.8), 6)
    return obj(mb, name, parent)

def _flicker(light, base, seed):
    fc = light.data.driver_add('energy'); d = fc.driver; d.type = 'SCRIPTED'
    d.expression = '%.1f*(1+0.12*sin(frame*0.9+%d)+0.08*sin(frame*2.3+%d))' % (base, seed, seed * 3)

def lantern(c, h=2.6, power=70.0, color=(1.0, 0.62, 0.3), post=True, name='k_lantern', parent=None, seed=1):
    """paper / iron lantern on a post: warm glass + a point light (flickering driver) -> a warm pool with falloff."""
    mb = MB(); wood = kmat('post', '#5e432c', 0.8); glass = kglow('lantern', '#ffb45e', 5.0); c = Vector(c)
    if post: mb.cyl(c, c + Vector((0, 0, h)), 0.08, 0.07, wood, 6); mb.beam(c + Vector((0, 0, h)), c + Vector((0.6, 0, h)), 0.08, 0.08, wood)
    lp = c + (Vector((0.6, 0, h - 0.55)) if post else Vector((0, 0, 0.35)))
    mb.cyl(lp - Vector((0, 0, 0.3)), lp + Vector((0, 0, 0.3)), 0.24, 0.24, glass, 10); mb.cyl(lp + Vector((0, 0, 0.3)), lp + Vector((0, 0, 0.42)), 0.28, 0.1, kmat('iron', '#2d2b2a', 0.5, 0.6), 10)
    o = obj(mb, name, parent); L = _light(name + '_L', 'POINT', color, power, lp, 0.2, parent); _flicker(L, power, seed); return dict(ob=o, light=L, pos=lp)

def brazier(c, power=260.0, name='k_brazier', parent=None, seed=2):
    """iron brazier on legs with glowing coals and flame tongues + a warm flickering point light (a big pool)."""
    mb = MB(); iron = kmat('iron', '#2d2b2a', 0.5, 0.6); coal = kglow('coal', '#ff6a1e', 3.0); flame = kglow('flame', '#ffb04a', 8.0); c = Vector(c)
    for k in range(3): a = 2 * math.pi * k / 3; mb.cyl(c + Vector((math.cos(a) * 0.55, math.sin(a) * 0.55, 0)), c + Vector((math.cos(a) * 0.35, math.sin(a) * 0.35, 1.0)), 0.05, 0.05, iron, 5)
    mb.cyl(c + Vector((0, 0, 0.95)), c + Vector((0, 0, 1.35)), 0.35, 0.62, iron, 12); mb.disc(c + Vector((0, 0, 1.3)), 0.56, coal, 12)
    rs = rnd(seed)
    for k in range(5):
        a = rs.uniform(0, 6.28); p = c + Vector((math.cos(a) * 0.25, math.sin(a) * 0.25, 1.3)); mb.cyl(p, p + Vector((rs.uniform(-0.1, 0.1), rs.uniform(-0.1, 0.1), rs.uniform(0.5, 1.0))), 0.15, 0.0, flame, 5, cap=False)
    o = obj(mb, name, parent, shadow=False); L = _light(name + '_L', 'POINT', (1.0, 0.55, 0.25), power, c + Vector((0, 0, 1.9)), 0.35, parent); _flicker(L, power, seed); return dict(ob=o, light=L)

# ============================================================================= off-screen shadow casters (gobos)
def gobo_rigging(c, yaw=0.0, scale=1.0, seed=7, masts=2, name='k_gobo_rig', parent=None):
    """masts, yards, shrouds and ratlines (invisible to the camera, cast shadows and cut the sun shafts in the haze)."""
    rs = rnd(seed); mb = MB(); m = kmat('gobo', '#202020', 1.0); a = math.radians(yaw); X = Vector((math.cos(a), math.sin(a), 0)); Y = Vector((-math.sin(a), math.cos(a), 0)); c = Vector(c)
    for i in range(masts):
        b = c + X * ((i - (masts - 1) / 2) * 9 * scale); H = rs.uniform(13, 17) * scale; mb.cyl(b, b + Vector((0, 0, H)), 0.25 * scale, 0.15 * scale, m, 6)
        for hy in (0.55, 0.85): mb.beam(b + Vector((0, 0, H * hy)) - Y * 4 * scale, b + Vector((0, 0, H * hy)) + Y * 4 * scale, 0.14 * scale, 0.14 * scale, m)
        for sg in (-1, 1):
            foot = b + Y * (sg * 4.5 * scale)
            for k in range(4):
                mb.beam(foot + X * ((k - 1.5) * 0.6 * scale), b + Vector((0, 0, H * 0.9)), 0.04 * scale, 0.04 * scale, m)
            for k in range(1, 9):
                u = k / 9.0; p0 = foot + X * (-0.9 * scale) + (b + Vector((0, 0, H * 0.9)) - foot) * u; p1 = foot + X * (0.9 * scale) + (b + Vector((0, 0, H * 0.9)) - foot) * u; mb.beam(p0, p1, 0.03 * scale, 0.03 * scale, m)
        mb.beam(b + Vector((0, 0, H)), b + X * (9 * scale) + Vector((0, 0, H * 0.7)), 0.04 * scale, 0.04 * scale, m)
    return obj(mb, name, parent, shadow=True, camera=False)

def gobo_canopy(c, n=6, radius=6.0, seed=8, name='k_gobo_tree', parent=None):
    """off-screen tree canopies (blobby leaf clusters with holes) casting dappled shadows."""
    rs = rnd(seed); mb = MB(); m = kmat('gobo', '#202020', 1.0); c = Vector(c)
    for i in range(n * 6):
        a = rs.uniform(0, 6.28); r = rs.uniform(0, radius); mb.lump(c + Vector((math.cos(a) * r, math.sin(a) * r, rs.uniform(-1.5, 1.5))), rs.uniform(0.5, 1.4), m, seed * 50 + i, 6, 4, 0.35, 0.6)
    return obj(mb, name, parent, shadow=True, camera=False)

# ============================================================================= pines and rocks
_PINES = []
def _pine_meshes():
    if _PINES and all(p.name in bpy.data.meshes for p in _PINES): return _PINES
    _PINES.clear(); fol = kmat('pine', '#2f5a36', 0.85, var=0.18); bark = kmat('bark', '#5a3e2a', 0.95)
    for v in range(4):
        rs = rnd(900 + v); mb = MB(); h = rs.uniform(9.5, 13.0); mb.cyl((0, 0, -0.4), (0, 0, h * 0.8), 0.28, 0.1, bark, 5)
        nt = rs.randint(4, 6)
        for t in range(nt):
            f = t / nt; zb = h * (0.16 + 0.62 * f); rr = (2.9 - 2.1 * f) * rs.uniform(0.9, 1.1); mb.cyl((0, 0, zb), (rs.uniform(-0.1, 0.1), rs.uniform(-0.1, 0.1), zb + h * 0.3 * (1 - 0.3 * f)), rr, 0.0, fol, 7, cap=False)
        me = bpy.data.meshes.new('k_pine%d' % v); me.from_pydata(mb.v, [], mb.f); me.update()
        for mt in mb.mats: me.materials.append(mt)
        for i, p in enumerate(me.polygons): p.material_index = mb.m[i]
        _PINES.append(me)
    return _PINES

def pine_cluster(c, n=8, radius=8.0, zfun=None, seed=9, scale=1.0, name='k_pine'):
    rs = rnd(seed); out = []; ms = _pine_meshes()
    for i in range(n):
        a = rs.uniform(0, 6.28); r = radius * math.sqrt(rs.random()); x, y = c[0] + math.cos(a) * r, c[1] + math.sin(a) * r; z = zfun(x, y) if zfun else c[2]
        o = bpy.data.objects.new(name, ms[rs.randrange(len(ms))]); _coll().objects.link(o); k = scale * rs.uniform(0.7, 1.2); o.location = (x, y, z - 0.15); o.scale = (k, k, k * rs.uniform(0.9, 1.15)); o.rotation_euler = (0, 0, rs.uniform(0, 6.28)); out.append(o)
    return out

def rock_cluster(c, n=6, radius=3.0, zfun=None, seed=10, size=1.2, name='k_rocks', parent=None):
    rs = rnd(seed); mb = MB(); ms = [kmat('rock0', '#7e7466', 0.92, var=0.15, bump=0.6), kmat('rock1', '#62594e', 0.92, var=0.15, bump=0.6)]
    for i in range(n):
        a = rs.uniform(0, 6.28); r = radius * math.sqrt(rs.random()); x, y = c[0] + math.cos(a) * r, c[1] + math.sin(a) * r; z = zfun(x, y) if zfun else c[2]; s = size * rs.uniform(0.5, 1.4)
        mb.lump((x, y, z + s * 0.25), s, ms[i % 2], seed * 13 + i, 9, 6, 0.3, 0.6, rs.uniform(0.8, 1.4))
    return obj(mb, name, parent, smooth=True)

# ============================================================================= cannon + muzzle rig
def cannon(c, yaw=0.0, pitch=6.0, name='k_cannon', parent=None):
    """chongtong-style iron barrel on a low wooden cart; returns dict(ob, muzzle, dir) for muzzle_rig."""
    mb = MB(); iron = kmat('cannon', '#26282c', 0.35, 0.8); wood = kmat('cart', '#6b4b2c', 0.8, var=0.1); c = Vector(c); a = math.radians(yaw); p = math.radians(pitch)
    d = Vector((math.cos(a) * math.cos(p), math.sin(a) * math.cos(p), math.sin(p))); side = Vector((-math.sin(a), math.cos(a), 0))
    mb.box(c + Vector((0, 0, 0.55)), 1.6, 0.55, 0.12, wood, yaw)
    for s_ in (-1, 1):
        w = c + side * (s_ * 0.7) + Vector((0, 0, 0.45)); mb.cyl(w - side * 0.12, w + side * 0.12, 0.45, 0.45, wood, 12)
    b0 = c + Vector((0, 0, 1.0)) - d * 1.5; b1 = b0 + d * 3.4; mb.cyl(b0, b1, 0.38, 0.27, iron, 12); mb.cyl(b1 - d * 0.2, b1 + d * 0.1, 0.33, 0.33, iron, 12); mb.lump(b0 - d * 0.15, 0.42, iron, 3, 10, 6, 0.0)
    o = obj(mb, name, parent, smooth=False); return dict(ob=o, muzzle=b1 + d * 0.12, dir=d, parent=parent)

def muzzle_rig(pos, dirv, parent=None, name='k_muzzle', scale=1.0, seed=11):
    """flash (emission star) + flash point light + smoke ring (torus) + recoil puff (soft cluster).  Animate with fire_muzzle(rig, t)."""
    pos = Vector(pos); dirv = Vector(dirv).normalized(); rs = rnd(seed)
    mb = MB(); fl = kglow('flash', '#ffd07a', 30.0)
    for k in range(7):
        a = rs.uniform(0, 6.28); e = rs.uniform(-0.6, 0.6); d2 = (dirv + Vector((math.cos(a) * 0.5, math.sin(a) * 0.5, e * 0.5))).normalized(); mb.cyl((0, 0, 0), d2 * rs.uniform(0.9, 1.6) * scale, 0.22 * scale, 0.0, fl, 5)
    mb.lump((0, 0, 0), 0.45 * scale, fl, seed, 8, 5, 0.3)
    flash = obj(mb, name + '_flash', parent, loc=pos, shadow=False); flash.hide_render = True
    mb = MB(); ring_m = ksoft('smokering', '#cfcac0', 0.7); mb.torus((0, 0, 0), 0.6, 0.28, ring_m, 16, 7)
    ring = obj(mb, name + '_ring', parent, loc=pos, shadow=False, smooth=True); ring.rotation_mode = 'QUATERNION'; ring.rotation_quaternion = dirv.to_track_quat('Z', 'Y'); ring.hide_render = True
    mb = MB(); pm = ksoft('puff', '#c4bfb4', 0.62)
    for k in range(5): mb.lump(Vector((rs.uniform(-0.5, 0.5), rs.uniform(-0.5, 0.5), rs.uniform(-0.4, 0.5))), rs.uniform(0.55, 0.85), pm, seed * 7 + k, 8, 5, 0.18)
    puff = obj(mb, name + '_puff', parent, loc=pos, shadow=False, smooth=True, sub=1); puff.hide_render = True
    L = _light(name + '_L', 'POINT', (1.0, 0.7, 0.35), 0.0, pos + dirv * 0.8, 0.3, parent)
    return dict(pos=pos, dir=dirv, flash=flash, ring=ring, puff=puff, light=L, scale=scale, power=4000.0 * scale * scale)

def fire_muzzle(rig, t, frame=None):
    """t = seconds since the shot (< 0: idle).  Flash + light for ~0.1 s, smoke ring flying out and growing over ~1.5 s, recoil puff swelling and drifting up."""
    p, d, s = rig['pos'], rig['dir'], rig['scale']
    fv = 0.0 <= t < 0.1; rig['flash'].scale = (1.0 + 4 * max(0, t),) * 3; _show(rig['flash'], fv, frame); _key(rig['flash'], 'scale', frame)
    rig['light'].data.energy = rig['power'] * math.exp(-max(0.0, t) / 0.05) if t >= 0 and t < 0.25 else 0.0
    if frame is not None: rig['light'].data.keyframe_insert('energy', frame=frame)
    u = max(0.0, min(1.0, t / 1.6)); rv = 0.02 < t < 1.6
    rig['ring'].location = p + d * (0.6 + 7.0 * s * (1 - (1 - u) ** 2)) + Vector((0, 0, 1.2 * u * s)); k = s * (0.6 + 2.6 * u); rig['ring'].scale = (k, k, k * (1 - 0.4 * u)); _show(rig['ring'], rv, frame)
    _key(rig['ring'], 'location', frame); _key(rig['ring'], 'scale', frame)
    v = max(0.0, min(1.0, t / 2.5)); pv = 0.0 <= t < 2.5; rig['puff'].location = p + d * (0.6 + 2.5 * s * v) + Vector((0, 0, 2.2 * s * v)); k = s * (0.35 + 1.4 * math.sqrt(v)) * (1.0 if v < 0.8 else (1 - v) / 0.2 * 0.6 + 0.4)
    rig['puff'].scale = (k, k, k); _show(rig['puff'], pv, frame); _key(rig['puff'], 'location', frame); _key(rig['puff'], 'scale', frame)

# ============================================================================= explosion kit
def explosion_rig(pos, water_z=0.0, ground=None, scale=1.0, seed=12, n_debris=22, parent=None, name='k_ex', column=True):
    """Builds a hidden explosion at world pos: 3 fireball layers + a fire light, debris planks and splinters (ballistic, they land / splash), a water column, a
    shockwave ring on the water, embers, a smoke column.  ground(x, y) -> z of a solid floor (debris lands) else they splash at water_z.  set_explosion(ex, t)."""
    rs = rnd(seed); pos = Vector(pos); s = scale; ex = dict(pos=pos, water_z=water_z, ground=ground, scale=s, debris=[], embers=[], fire=[], smoke=[])
    for k, (col, ek, r) in enumerate((('#ffc04a', 4.0, 1.0), ('#ff7a18', 2.0, 1.3), ('#d84a12', 0.9, 1.6))):
        mb = MB(); m = ksoft('fire%d' % k, col, 0.85, emit_k=ek, emit_col=col)
        for j in range(6): mb.lump(Vector((rs.uniform(-0.6, 0.6), rs.uniform(-0.6, 0.6), rs.uniform(-0.3, 0.8))) * r, r * rs.uniform(0.6, 0.9), m, seed * 3 + k * 10 + j, 8, 5, 0.25)
        o = obj(mb, '%s_fire%d' % (name, k), parent, loc=pos, shadow=False, smooth=True, sub=1); o.hide_render = True; ex['fire'].append(o)
    ex['light'] = _light(name + '_L', 'POINT', (1.0, 0.55, 0.22), 0.0, pos + Vector((0, 0, 1.5 * s)), 1.0, parent); ex['power'] = 25000.0 * s * s
    wood = kmat('debris', '#7a5434', 0.8, var=0.2); dark = kmat('debris_c', '#2d221b', 0.9)
    for i in range(n_debris):
        mb = MB(); plank = i % 3 != 2; L_ = rs.uniform(0.8, 2.2) if plank else rs.uniform(0.3, 0.7)
        mb.box((0, 0, 0), L_ / 2, (0.18 if plank else 0.05), (0.05 if plank else 0.04), wood if i % 4 else dark)
        o = obj(mb, '%s_deb%d' % (name, i), parent, loc=pos, shadow=True); o.hide_render = True
        a = rs.uniform(0, 6.28); up = rs.uniform(0.55, 1.0); sp = rs.uniform(7, 16) * s
        v = Vector((math.cos(a) * math.sqrt(1 - up * up) + 0.3 * math.cos(a), math.sin(a) * math.sqrt(1 - up * up), up)).normalized() * sp
        ex['debris'].append(dict(ob=o, v=v, w=Vector((rs.uniform(-8, 8), rs.uniform(-8, 8), rs.uniform(-6, 6))), splash=None))
    spm = kmat('splash', '#eef3f2', 0.6)
    for d in ex['debris']:
        mb = MB(); mb.torus((0, 0, 0), 0.5, 0.12, spm, 12, 5); [mb.lump((math.cos(k) * 0.4, math.sin(k) * 0.4, 0.2), 0.12, spm, k, 6, 4, 0.2) for k in range(4)]
        o = obj(mb, d['ob'].name + '_spl', parent, shadow=False, smooth=True); o.hide_render = True; d['splash'] = o
    if column:
        mb = MB(); wc = ksoft('watercol', '#e8efee', 0.8)
        for k in range(9): mb.lump(Vector((rs.uniform(-0.6, 0.6), rs.uniform(-0.6, 0.6), 0.6 * k)), 0.9 - 0.06 * k, wc, seed * 5 + k, 8, 5, 0.25, 1.2)
        ex['column'] = obj(mb, name + '_col', parent, loc=(pos.x, pos.y, water_z), shadow=True, smooth=True, sub=1); ex['column'].hide_render = True
        mb = MB(); rm = ksoft('shock', '#f4f8f8', 0.35); mb.torus((0, 0, 0), 1.0, 0.09, rm, 32, 4)
        ex['shock'] = obj(mb, name + '_shock', parent, loc=(pos.x, pos.y, water_z + 0.15), shadow=False, smooth=True); ex['shock'].hide_render = True
    em = kglow('ember', '#ffb24a', 18.0)
    for i in range(36):
        mb = MB(); mb.lump((0, 0, 0), 0.06, em, i, 5, 3, 0.0); o = obj(mb, '%s_emb%d' % (name, i), parent, loc=pos, shadow=False); o.hide_render = True
        ex['embers'].append(dict(ob=o, v=Vector((rs.uniform(-3, 3), rs.uniform(-3, 3), rs.uniform(4, 9))) * s, ph=rs.uniform(0, 6.28)))
    sm = ksoft('exsmoke', '#55504b', 0.6)
    for k in range(6):
        mb = MB(); [mb.lump(Vector((rs.uniform(-0.7, 0.7), rs.uniform(-0.7, 0.7), rs.uniform(-0.5, 0.5))), rs.uniform(0.7, 1.0), sm, seed * 9 + k * 7 + j, 8, 5, 0.2) for j in range(4)]
        o = obj(mb, '%s_smk%d' % (name, k), parent, loc=pos, shadow=False, smooth=True, sub=1); o.hide_render = True; ex['smoke'].append(dict(ob=o, h=2.5 + 2.2 * k, dr=Vector((rs.uniform(-1.5, 0.5), rs.uniform(-1, 1), 0)), k=k))
    return ex

def _floor(ex, x, y):
    if ex['ground']:
        g = ex['ground'](x, y)
        if g is not None: return g, True
    return ex['water_z'], False

def set_explosion(ex, t, frame=None):
    """t = seconds since detonation (< 0: nothing).  0-0.25 s fireball swells (flash light), 0.25-1.2 s it rolls up and darkens into smoke; debris fly on ballistic arcs and
    land (or splash and sink); the water column rises (0-0.5 s) and collapses (0.5-1.6 s); the shockwave ring runs out over the water (0-0.8 s); embers rise and fade; the
    smoke column builds from 0.4 s and stays."""
    p, s = ex['pos'], ex['scale']; on = t >= 0
    for k, o in enumerate(ex['fire']):
        u = max(0.0, t); g = min(1.0, u / 0.25); r = s * (0.4 + 1.7 * g) * (1 + 0.35 * max(0.0, u - 0.25)) * (1.0 + 0.25 * k); vis = on and u < 1.3 - 0.25 * k
        o.scale = (r, r, r * (1 + 0.6 * max(0.0, u - 0.25))); o.location = p + Vector((0, 0, s * (1.2 * g + 3.0 * max(0.0, u - 0.25))))
        _show(o, vis, frame); _key(o, 'scale', frame); _key(o, 'location', frame)
    ex['light'].data.energy = ex['power'] * (min(1.0, max(0.0, t) / 0.06) * math.exp(-max(0.0, t - 0.06) / 0.35)) if on else 0.0
    if frame is not None: ex['light'].data.keyframe_insert('energy', frame=frame)
    for d in ex['debris']:
        o = d['ob']; tt = max(0.0, t); pp = p + d['v'] * tt + Vector((0, 0, -0.5 * G * tt * tt)); fz, solid = _floor(ex, pp.x, pp.y)
        if pp.z <= fz and tt > 0.05:                                   # landed: find the touchdown time and freeze there (planks lie flat) / splash and sink
            a_, b_, c_ = -0.5 * G, d['v'].z, p.z - fz; disc = max(0.0, b_ * b_ - 4 * a_ * c_); tl = (-b_ - math.sqrt(disc)) / (2 * a_)
            pl = p + d['v'] * tl + Vector((0, 0, -0.5 * G * tl * tl)); pl.z = fz + 0.06
            if solid: o.location = pl; o.rotation_euler = (0, 0, d['w'].z * tl); _show(o, on, frame)
            else: o.location = pl - Vector((0, 0, min(0.5, (tt - tl) * 0.8))); o.rotation_euler = (0, 0, d['w'].z * tl); _show(o, on and tt - tl < 0.6, frame)
            sp = d['splash']; sp.location = (pl.x, pl.y, fz + 0.02); k = 0.4 + 2.0 * min(1.0, (tt - tl) / 0.6); sp.scale = (k, k, k); _show(sp, (not solid) and on and tt - tl < 0.7, frame)
        else:
            o.location = pp; o.rotation_euler = tuple(d['w'] * tt); _show(o, on, frame); _show(d['splash'], False, frame)
        _key(o, 'location', frame); _key(o, 'rotation_euler', frame); _key(d['splash'], 'location', frame); _key(d['splash'], 'scale', frame)
    if 'column' in ex:
        c = ex['column']; u = max(0.0, t); h = s * (1.6 * min(1.0, u / 0.5) if u < 0.5 else 1.6 * max(0.0, 1 - (u - 0.5) / 1.1)); vis = on and u < 1.6
        c.scale = (s * (1 + 0.6 * u), s * (1 + 0.6 * u), max(0.05, h * 1.6)); _show(c, vis, frame); _key(c, 'scale', frame)
        sh = ex['shock']; k = s * (1.0 + 14.0 * min(1.0, u / 0.8)); sh.scale = (k, k, 1.0); _show(sh, on and u < 0.8, frame); _key(sh, 'scale', frame)
    for e in ex['embers']:
        tt = max(0.0, t); pp = p + e['v'] * (1 - math.exp(-tt / 1.2)) * 1.4 + Vector((0.6 * math.sin(tt * 3 + e['ph']), 0.6 * math.cos(tt * 2.3 + e['ph']), 0)); e['ob'].location = pp
        _show(e['ob'], on and tt < 3.5, frame); _key(e['ob'], 'location', frame)
    for sm in ex['smoke']:
        u = max(0.0, t - 0.3 - 0.12 * sm['k']); g = min(1.0, u / 1.2); o = sm['ob']; o.location = p + Vector((0, 0, s * sm['h'] * (0.5 + 0.5 * g))) + sm['dr'] * s * u * 0.3
        k = s * (0.5 + 1.6 * g) * (1 + 0.15 * sm['k']); o.scale = (k, k, k); _show(o, on and u > 0, frame); _key(o, 'location', frame); _key(o, 'scale', frame)

def splash_rig(pos, water_z=0.0, scale=1.0, seed=13, name='k_splash', parent=None):
    """a person-size splash (comic jump into the sea): a small column + a ring + droplets.  set_splash(rig, t)."""
    return explosion_rig(pos, water_z, None, scale * 0.45, seed, 0, parent, name, True) | dict(nofire=True)

def set_splash(rig, t, frame=None):
    u = max(0.0, t); on = t >= 0; s = rig['scale']
    for o in rig['fire']: _show(o, False, frame)
    rig['light'].data.energy = 0.0
    c = rig['column']; h = s * (1.6 * min(1.0, u / 0.3) if u < 0.3 else 1.6 * max(0.0, 1 - (u - 0.3) / 0.7)); c.scale = (s * (1 + u), s * (1 + u), max(0.05, h * 1.6)); _show(c, on and u < 1.0, frame); _key(c, 'scale', frame)
    sh = rig['shock']; k = s * (1.0 + 8.0 * min(1.0, u / 0.9)); sh.scale = (k, k, 1.0); _show(sh, on and u < 0.9, frame); _key(sh, 'scale', frame)
    for e in rig['embers']: _show(e['ob'], False, frame)
    for sm in rig['smoke']: _show(sm['ob'], False, frame)

# ============================================================================= fire on rigging and sails
def fire_patch(points, size=1.0, seed=14, name='k_fire', parent=None, light=True):
    """flame tongues at the given points (on a sail, a yard, rigging) + embers + one warm light; set_fire(fr, level)."""
    rs = rnd(seed); fr = dict(fl=[], embers=[], light=None, pts=[Vector(p) for p in points], size=size)
    fm = [kglow('flame', '#ffb04a', 8.0), kglow('flame2', '#ff6a1e', 6.0)]
    for i, p in enumerate(fr['pts']):
        mb = MB()
        for k in range(4): mb.cyl(Vector((rs.uniform(-0.3, 0.3), rs.uniform(-0.3, 0.3), 0)) * size, Vector((rs.uniform(-0.3, 0.3), rs.uniform(-0.3, 0.3), rs.uniform(1.0, 2.0))) * size, 0.35 * size, 0.0, fm[k % 2], 6, cap=False)
        o = obj(mb, '%s_%d' % (name, i), parent, loc=p, shadow=False); o.hide_render = True; fr['fl'].append(o)
        fc = o.driver_add('scale', 2); fc.driver.type = 'SCRIPTED'; fc.driver.expression = '1+0.25*sin(frame*1.3+%d)+0.12*sin(frame*3.1+%d)' % (i, i * 2)
    em = kglow('ember', '#ffb24a', 18.0)
    for j in range(18):
        mb = MB(); mb.lump((0, 0, 0), 0.05 * size, em, j, 5, 3, 0.0); o = obj(mb, '%s_emb%d' % (name, j), parent, loc=fr['pts'][j % len(fr['pts'])], shadow=False); o.hide_render = True
        fr['embers'].append(dict(ob=o, base=fr['pts'][j % len(fr['pts'])], ph=rs.uniform(0, 1), dr=Vector((rs.uniform(-2, 2), rs.uniform(-2, 2), 0))))
    if light and fr['pts']:
        c = sum(fr['pts'], Vector()) / len(fr['pts']); fr['light'] = _light(name + '_L', 'POINT', (1.0, 0.5, 0.2), 0.0, c + Vector((0, 0, 1.0 * size)), 0.8 * size, parent)
        fr['power'] = 900.0 * size * size * len(fr['pts']) ** 0.5
    return fr

def set_fire(fr, level, frame=None):
    """level 0 = out .. 1 = burning (flames + flickering light + rising embers; embers cycle with the frame: call every frame)."""
    f = frame if frame is not None else bpy.context.scene.frame_current; on = level > 0.01
    for o in fr['fl']:
        k = max(0.01, level); o.scale[0] = o.scale[1] = k; _show(o, on, frame); _key(o, 'scale', frame)
    for e in fr['embers']:
        u = (e['ph'] + f / 60.0) % 1.0; e['ob'].location = e['base'] + Vector((0, 0, 6.0 * fr['size'] * u)) + e['dr'] * u * fr['size']; _show(e['ob'], on and u < 0.9, frame); _key(e['ob'], 'location', frame)
    if fr['light'] is not None:
        fr['light'].data.energy = fr['power'] * level * (1 + 0.15 * math.sin(f * 0.9)); _key(fr['light'].data, 'energy', frame) if False else (fr['light'].data.keyframe_insert('energy', frame=frame) if frame is not None else None)

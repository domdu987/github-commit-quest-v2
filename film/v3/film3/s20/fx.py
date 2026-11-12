"""fx.py -- runtime additions to the harbor set for film 3 takes s16 / s18 / s20 (the set module itself is never edited).

    import fx
    fx.init()                          # after harbor.build(...): materials, bulge patch, 3D rivets, glossy drip, streak pool
    fx.set_bulge(amp, ridge)           # the seam plate swells outward (D), the horizontal seam ridge pulls out
    fx.rivets_at(g, fn)                # fn(i, rivet) -> (offset_vector, rot_euler, visible); per-frame rivet state
    fx.drip(t_cycle, ...)              # elongated glossy drop forming on the bucket seam strip and falling into the bucket
    fx.streak(i, p0, p1, r, k)         # bright tapered tracer between two world points (k = opacity 0..1), hide with k = 0

Everything is per-frame state written directly into meshes / objects before each render (no keys), so a frame is a pure
function of g.  Copies of this file live in s16, s18 and s20 (each take folder is self-contained)."""
import math, os, sys, random
import bpy
import numpy as np
from mathutils import Vector, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(V3, "set3d3"))
import harbor as H                 # noqa: E402
import harbor_tex as HT            # noqa: E402
import tower as T                  # noqa: E402

R = H.TANK_R
TH_B = H.TH_B
TH_0 = H.TH_0
CX, CY = H.TANK_C
S = {}


def th_u(u):
    return TH_0 + u / R


def wall(u, z, r=R):
    return H.wall_pt(th_u(u), r, z)


# ----------------------------------------------------------------------------- materials
def _hexlin(h):
    return T.hex_lin(h)


def mat_glossy(name, hexcol, gloss=0.6, rough=0.12, spec_tint=(1.0, 0.9, 0.78), gain=1.0, rim=0.0):
    """Molasses: mat_lit (toon key + painted shade) + a real Glossy BSDF lit by the sun (highlights) + an optional fresnel rim
    (camera-facing gloss without a world to reflect)."""
    m = H.mat_lit(name, hexcol, gain=gain, shade_mul=1.0, form=(0.0, -0.05, 0.2))
    nt = m.node_tree
    out = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeOutputMaterial'][0]
    src = [lk.from_socket for lk in nt.links if lk.to_socket == out.inputs['Surface']][0]
    g = nt.nodes.new('ShaderNodeBsdfGlossy'); g.inputs['Roughness'].default_value = rough
    g.inputs['Color'].default_value = (spec_tint[0] * gloss, spec_tint[1] * gloss, spec_tint[2] * gloss, 1)
    ad = nt.nodes.new('ShaderNodeAddShader'); nt.links.new(src, ad.inputs[0]); nt.links.new(g.outputs['BSDF'], ad.inputs[1])
    last = ad.outputs['Shader']
    if rim > 0:
        lw = nt.nodes.new('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.35
        pw = nt.nodes.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 2.0
        nt.links.new(lw.outputs['Facing'], pw.inputs[0])
        e = nt.nodes.new('ShaderNodeEmission'); e.inputs['Color'].default_value = (0.95 * rim, 0.62 * rim, 0.34 * rim, 1)
        sc = nt.nodes.new('ShaderNodeMath'); sc.operation = 'MULTIPLY'; sc.inputs[1].default_value = 1.0
        nt.links.new(pw.outputs[0], sc.inputs[0]); nt.links.new(sc.outputs[0], e.inputs['Strength'])
        a2 = nt.nodes.new('ShaderNodeAddShader'); nt.links.new(last, a2.inputs[0]); nt.links.new(e.outputs['Emission'], a2.inputs[1])
        last = a2.outputs['Shader']
    nt.links.new(last, out.inputs['Surface'])
    return m


def mat_tracer(name, col=(1.0, 0.86, 0.55), strength=3.0):
    """Unlit tracer: emission x along-UV fade (u 0 = tail, 1 = head) mixed with transparency; object colour alpha = overall k."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*col, 1); em.inputs['Strength'].default_value = strength
    tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    uv = N('ShaderNodeUVMap'); sep = N('ShaderNodeSeparateXYZ'); L(uv.outputs['UV'], sep.inputs[0])
    pw = N('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 1.6; L(sep.outputs['X'], pw.inputs[0])
    oi = N('ShaderNodeObjectInfo'); mul = N('ShaderNodeMath'); mul.operation = 'MULTIPLY'; L(pw.outputs[0], mul.inputs[0]); L(oi.outputs['Alpha'], mul.inputs[1])
    L(mul.outputs[0], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(em.outputs['Emission'], mx.inputs[2]); L(mx.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m


def mat_haze(name, col=(1.0, 0.93, 0.85), k=0.5):
    """Soft additive haze card: emission x radial falloff x object alpha, transparent elsewhere (steam / heat over the seam)."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*col, 1); em.inputs['Strength'].default_value = k
    tr = N('ShaderNodeBsdfTransparent'); ad = N('ShaderNodeAddShader'); mx = N('ShaderNodeMixShader')
    uv = N('ShaderNodeUVMap'); vm = N('ShaderNodeVectorMath'); vm.operation = 'SUBTRACT'; vm.inputs[1].default_value = (0.5, 0.5, 0)
    L(uv.outputs['UV'], vm.inputs[0]); ln = N('ShaderNodeVectorMath'); ln.operation = 'LENGTH'; L(vm.outputs['Vector'], ln.inputs[0])
    noi = N('ShaderNodeTexNoise'); noi.inputs['Scale'].default_value = 3.0; L(uv.outputs['UV'], noi.inputs['Vector'])
    f1 = N('ShaderNodeMath'); f1.operation = 'MULTIPLY_ADD'; f1.inputs[1].default_value = -2.0; f1.inputs[2].default_value = 1.0; L(ln.outputs['Value'], f1.inputs[0])
    f1.use_clamp = True
    f2 = N('ShaderNodeMath'); f2.operation = 'MULTIPLY'; L(f1.outputs[0], f2.inputs[0]); L(noi.outputs['Fac'], f2.inputs[1])
    f3 = N('ShaderNodeMath'); f3.operation = 'MULTIPLY'; L(f2.outputs[0], f3.inputs[0])
    oi = N('ShaderNodeObjectInfo'); L(oi.outputs['Alpha'], f3.inputs[1])
    L(tr.outputs['BSDF'], ad.inputs[0]); L(em.outputs['Emission'], ad.inputs[1])
    L(f3.outputs[0], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(ad.outputs['Shader'], mx.inputs[2]); L(mx.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m


def _coll():
    c = bpy.data.collections.get('FX3')
    if c is None:
        c = bpy.data.collections.new('FX3'); bpy.context.scene.collection.children.link(c)
    return c


def _mesh_obj(name, verts, faces, uvs, mat, smooth=True):
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in verts], [], faces); me.update()
    if uvs is not None:
        ul = me.uv_layers.new(name='UVMap')
        for poly in me.polygons:
            for li in poly.loop_indices:
                ul.data[li].uv = uvs[me.loops[li].vertex_index]
    me.materials.append(mat)
    for p in me.polygons: p.use_smooth = smooth
    ob = bpy.data.objects.new(name, me); _coll().objects.link(ob); T.no_bounce(ob)
    return ob


# ----------------------------------------------------------------------------- bulge
U0, U1, Z0, Z1 = HT.SEAM_U - 3.0, HT.SEAM_U + 3.0, 0.0, 7.0


def bulge_disp(u, z, amp, ridge):
    """Outward displacement (D) of the wall at texture u (D along the wall) and height z: a broad swell centred on the bucket
    seam crossing (u = SEAM_U, z = 3) plus a sharp ridge along the horizontal seam (the lap pulling apart)."""
    du = np.asarray(u) - HT.SEAM_U; z = np.asarray(z)
    wu = np.where(np.abs(du) < 3.0, np.cos(np.pi * du / 6.0) ** 2, 0.0)
    wz = np.where((z > 0) & (z < 7), np.sin(np.pi * np.clip(z, 0, 7) / 7.0) ** 0.6, 0.0)
    swell = np.exp(-((z - 3.0) / 1.9) ** 2)
    rid = np.exp(-((z - 3.0) / 0.22) ** 2) * np.cos(np.pi * du / 6.0) ** 4
    return wu * wz * (amp * swell + ridge * rid)


def _build_bulge(M):
    nu, nz = 90, 105
    us = np.linspace(U0, U1, nu + 1); zs = np.linspace(Z0, Z1, nz + 1)
    verts, uvs = [], []
    for z in zs:
        for u in us:
            verts.append(wall(u, z, R + 0.008)); uvs.append(((u - U0) / 6.0, z / 7.0))
    faces = [(j * (nu + 1) + i, j * (nu + 1) + i + 1, (j + 1) * (nu + 1) + i + 1, (j + 1) * (nu + 1) + i) for j in range(nz) for i in range(nu)]
    ob = _mesh_obj('fx_bulge_patch', verts, faces, uvs, M['patch'], smooth=True)
    UU, ZZ = np.meshgrid(us, zs)
    S['bulge'] = dict(ob=ob, u=UU.ravel(), z=ZZ.ravel(), base=np.array([tuple(v) for v in verts]),
                      nrm=np.array([tuple(H.OUT(th_u(u))) for u in UU.ravel()]))
    H.STATE['objects']['tank_patch'].hide_render = True
    H.STATE['seep'].visible_shadow = False                              # thin film on the wall: no offset shadow
    # seep strips: an extra relative shape key that follows the bulge
    sp = H.STATE['seep']; kb_full = sp.data.shape_keys.key_blocks['seep']
    co = np.empty(len(kb_full.data) * 3); kb_full.data.foreach_get('co', co); co = co.reshape(-1, 3)
    bco = np.empty(len(sp.data.vertices) * 3); sp.data.vertices.foreach_get('co', bco); bco = bco.reshape(-1, 3)
    th = np.arctan2(co[:, 1] - CY, co[:, 0] - CX); u = (th - TH_0) * R
    u = (u + math.pi * R) % (2 * math.pi * R) - math.pi * R
    kb = sp.shape_key_add(name='fx_bulge', from_mix=False); kb.value = 1.0
    S['seep_b'] = dict(kb=kb, base=bco, u=u, zf=co[:, 2], nrm=np.stack([np.cos(th), np.sin(th), np.zeros_like(th)], 1))


def set_bulge(amp, ridge=0.0):
    b = S['bulge']; d = bulge_disp(b['u'], b['z'], amp, ridge)
    co = b['base'] + b['nrm'] * d[:, None]
    b['ob'].data.vertices.foreach_set('co', co.ravel()); b['ob'].data.update()
    s = S['seep_b']; ds = bulge_disp(s['u'], s['zf'], amp, ridge)
    ds = ds + 0.014 * np.clip(ds / 0.04, 0, 1)                         # stay proud of the curved patch between strip vertices
    s['kb'].data.foreach_set('co', (s['base'] + s['nrm'] * ds[:, None]).ravel())
    sp = H.STATE['seep']; sp.data.update()
    S['amp'] = (amp, ridge)


def wall_bulged(u, z, r_off=0.0):
    amp, ridge = S.get('amp', (0.0, 0.0))
    d = float(bulge_disp(u, z, amp, ridge))
    return wall(u, z, R + r_off + d)


# ----------------------------------------------------------------------------- 3D rivets (heads over the painted ones)
def rivet_uz(span=3.0):
    """(u, z) of the painted rivets near the bucket seam: the two rows of seams 1 and 2, the two columns of the bucket seam."""
    W = HT.TILE_W; n = int(W / 0.25); out = []
    for c in (1, 2):
        for dz in (0.14, -0.15):
            for i in range(n):
                u = (i + 0.5) * W / n
                if abs(u - HT.SEAM_U) <= span: out.append((u, c * 3.0 + dz, 'row%d' % c))
    for dx in (-0.13, 0.13):
        for i in range(11): out.append((HT.SEAM_U + dx, 3.0 - (0.3 + i * (HT.COURSE - 0.6) / 10), 'col'))
    return out


def _build_rivets(M, span):
    me = bpy.data.meshes.new('fx_rivet'); rr = 0.052; seg, rings = 10, 4; vs = [(0, 0, 0)]; fs = []
    for k in range(1, rings + 1):
        a = (math.pi / 2) * k / rings
        for i in range(seg):
            b = 2 * math.pi * i / seg; vs.append((rr * math.sin(a) * math.cos(b), rr * math.sin(a) * math.sin(b), 0.03 + 0.03 * math.cos(a)))
    vs[0] = (0, 0, 0.06)
    for i in range(seg): fs.append((0, 1 + i, 1 + (i + 1) % seg))
    for k in range(rings - 1):
        for i in range(seg):
            a0 = 1 + k * seg; a1 = a0 + seg; j = (i + 1) % seg; fs.append((a0 + i, a1 + i, a1 + j, a0 + j))
    base = len(vs)                                                     # shank (seen when the rivet flies)
    for z in (0.03, -0.12):
        for i in range(seg): b = 2 * math.pi * i / seg; vs.append((0.024 * math.cos(b), 0.024 * math.sin(b), z))
    for i in range(seg):
        j = (i + 1) % seg; fs.append((base + i, base + j, base + seg + j, base + seg + i))
    me.from_pydata(vs, [], fs); me.update(); me.materials.append(M['rivet'])
    for p in me.polygons: p.use_smooth = True
    S['rivets'] = []
    for i, (u, z, kind) in enumerate(rivet_uz(span)):
        ob = bpy.data.objects.new('fx_rivet_%03d' % i, me); _coll().objects.link(ob); T.no_bounce(ob)
        n = H.OUT(th_u(u)); ob.rotation_mode = 'QUATERNION'
        S['rivets'].append(dict(ob=ob, u=u, z=z, kind=kind, n=n))
    place_rivets(lambda i, rv: (Vector((0, 0, 0)), None, True))


def place_rivets(fn):
    """fn(i, rivet) -> (world offset Vector, extra rotation Quaternion or None, visible)."""
    for i, rv in enumerate(S['rivets']):
        off, rot, vis = fn(i, rv)
        p = wall_bulged(rv['u'], rv['z'], 0.0) + off
        q = rv['n'].to_track_quat('Z', 'Y')
        if rot is not None: q = rot @ q
        rv['ob'].location = p; rv['ob'].rotation_quaternion = q; rv['ob'].hide_render = not vis


# ----------------------------------------------------------------------------- drip (glossy elongated drop)
def _teardrop(name, mat):
    vs, fs = [], []; seg, rings = 12, 10
    for k in range(rings + 1):
        t = k / rings                                   # 0 = top (tail tip), 1 = bottom
        z = -t
        r = math.sin(math.pi * t) ** 0.9 * (0.25 + 0.75 * t ** 1.5)
        for i in range(seg):
            b = 2 * math.pi * i / seg; vs.append((r * math.cos(b), r * math.sin(b), z))
    for k in range(rings):
        for i in range(seg):
            j = (i + 1) % seg; fs.append((k * seg + i, k * seg + j, (k + 1) * seg + j, (k + 1) * seg + i))
    me = bpy.data.meshes.new(name); me.from_pydata(vs, [], fs); me.update(); me.materials.append(mat)
    for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new(name, me); _coll().objects.link(ob); T.no_bounce(ob)
    return ob


DRIP_U = HT.SEAM_U
DRIP_Z0 = HT.COURSE - 0.12 - 0.78 + 0.02        # bottom of the bucket-seam strip


def _build_drip(M):
    S['drip'] = [_teardrop('fx_drip_%d' % k, M['drip']) for k in range(2)]
    me = bpy.data.meshes.new('fx_ring'); seg = 24; vs, fs = [], []
    for k, rr in enumerate((0.8, 1.0)):
        for i in range(seg): b = 2 * math.pi * i / seg; vs.append((rr * math.cos(b), rr * math.sin(b), 0))
    for i in range(seg): j = (i + 1) % seg; fs.append((i, j, seg + j, seg + i))
    me.from_pydata(vs, [], fs); me.update(); me.materials.append(M['ring'])
    S['ring'] = bpy.data.objects.new('fx_ring', me); _coll().objects.link(S['ring']); T.no_bounce(S['ring'])
    H.STATE['drop'].hide_render = True


def drip(phase, k=0, land_z=0.70, r_off=0.16, size=1.0, bulge=True, ring_obj=True):
    """One drip cycle, phase 0..1: 0-0.62 the drop swells and stretches at the strip end, 0.62-0.86 it falls (accelerating),
    0.86-1 hidden (a ring spreads on the bucket's fill).  Returns the world position of the drop's bottom."""
    ob = S['drip'][k]; u = DRIP_U
    top = wall_bulged(u, DRIP_Z0, r_off) if bulge else wall(u, DRIP_Z0, R + r_off)
    ring = S['ring']
    if phase < 0.62:
        a = phase / 0.62; L = 0.07 + 0.16 * a ** 1.6; w = 0.035 + 0.035 * a
        ob.location = top + Vector((0, 0, 0.02)); ob.scale = (w * size, w * size, L * size); ob.hide_render = False
        ring.hide_render = True
        return top - Vector((0, 0, L))
    if phase < 0.86:
        a = (phase - 0.62) / 0.24; zf = DRIP_Z0 - 0.23 - (DRIP_Z0 - 0.23 - land_z) * a * a
        L = 0.23 + 0.25 * a; w = 0.07 - 0.02 * a
        ob.location = Vector((top.x, top.y, zf + L * size)); ob.scale = (w * size, w * size, L * size); ob.hide_render = False
        ring.hide_render = True
        return ob.location - Vector((0, 0, L))
    ob.hide_render = True
    if ring_obj:
        a = (phase - 0.86) / 0.14
        ring.location = Vector((top.x, top.y, land_z + 0.004)); s = 0.03 + 0.17 * a; ring.scale = (s, s, 1); ring.hide_render = False
        ring.color = (1, 1, 1, 1.0 - a)
    return None


# ----------------------------------------------------------------------------- tracers and haze cards
def _build_tracers(n, M):
    seg = 6; vs, fs, uvs = [], [], []
    for k, (z, r) in enumerate(((0.0, 0.0), (1.0, 1.0))):
        for i in range(seg):
            b = 2 * math.pi * i / seg; vs.append((r * math.cos(b), r * math.sin(b), z)); uvs.append((z, i / seg))
    for i in range(seg): j = (i + 1) % seg; fs.append((i, j, seg + j, seg + i))
    me = bpy.data.meshes.new('fx_tracer'); me.from_pydata(vs, [], fs); me.update()
    ul = me.uv_layers.new(name='UVMap')
    for poly in me.polygons:
        for li in poly.loop_indices: ul.data[li].uv = uvs[me.loops[li].vertex_index]
    me.materials.append(M['tracer'])
    S['tracers'] = []
    for i in range(n):
        ob = bpy.data.objects.new('fx_tracer_%02d' % i, me); _coll().objects.link(ob); T.no_bounce(ob); ob.visible_shadow = False
        ob.rotation_mode = 'QUATERNION'; ob.hide_render = True; S['tracers'].append(ob)


def streak(i, p0, p1, r, k):
    """Tracer i from tail p0 to head p1 (world), radius r at the head, opacity k (0 hides)."""
    ob = S['tracers'][i]
    if k <= 0.01 or (Vector(p1) - Vector(p0)).length < 1e-3:
        ob.hide_render = True; return
    d = Vector(p1) - Vector(p0)
    ob.location = Vector(p0); ob.rotation_quaternion = d.to_track_quat('Z', 'Y'); ob.scale = (r, r, d.length)
    ob.color = (1, 1, 1, min(1.0, k)); ob.hide_render = False


def build_haze(n, M):
    S['haze'] = []
    me = bpy.data.meshes.new('fx_haze'); me.from_pydata([(-0.5, 0, -0.5), (0.5, 0, -0.5), (0.5, 0, 0.5), (-0.5, 0, 0.5)], [], [(0, 1, 2, 3)]); me.update()
    ul = me.uv_layers.new(name='UVMap')
    for li, uv in zip(range(4), ((0, 0), (1, 0), (1, 1), (0, 1))): ul.data[li].uv = uv
    me.materials.append(M['haze'])
    for i in range(n):
        ob = bpy.data.objects.new('fx_haze_%02d' % i, me); _coll().objects.link(ob); T.no_bounce(ob); ob.visible_shadow = False
        ob.hide_render = True; S['haze'].append(ob)


def init(rivets=True, span=3.0, tracers=0, haze=0, drip_on=True, bulge=True):
    M = H.STATE['M']
    M['rivet'] = H.mat_lit('FX_rivet', '#7a4c2a', gain=1.0, shade_mul=1.0, form=(0.0, -0.05, 0.2))
    M['drip'] = mat_glossy('FX_drip', '#3a1206', gloss=0.9, rough=0.08, rim=0.35)
    M['ring'] = mat_glossy('FX_ring', '#5a2208', gloss=0.6, rough=0.1)
    M['tracer'] = mat_tracer('FX_tracer')
    M['haze'] = mat_haze('FX_haze')
    if bulge: _build_bulge(M)
    if rivets: _build_rivets(M, span)
    if drip_on: _build_drip(M)
    if tracers: _build_tracers(tracers, M)
    if haze: build_haze(haze, M)
    return M

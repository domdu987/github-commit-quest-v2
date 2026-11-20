"""jimo_vista3.py : "Vista round 3" for the Qi plain (shots s03, s04, s25). See API.md, section "Vista round 3".

What it does (all of it is applied by J.build('vista'...) itself; `J.vista_r3()` is the idempotent finisher / sweeper the take scripts may call again):
  1. warm, soft field shade: the fields no longer fall to the set's navy SHADE in cast shadows (art x (0.50 0.40 0.46), a light violet-brown) + furrow stripes + 4 crop tints;
     the long spiky cone shadows (old 'vtrees') and the flat slab shadows of the 62 x 2 pennants are gone (shadow flag off), sun disc softer;
     the Jimo ring moat / river are a dusk-teal water with warm glints (not navy).
  2. living farmland, all GEOMETRY-NODES INSTANCES (one tiny prototype mesh per kind, one points object per kind): hedgerows, tree lines (+ willows on the river), haystacks, farm huts
     (some with a warm window), carts and tiny figures on the roads, river glints (one merged quad mesh).
  3. Ju: a big walled town far on the plain with a watch tower, lit windows, wall lamps, gate fires, a glow dome and a warm ground pool; no Yan pennant; ordinary towns kept 100 D away.
  4. no loose flame: the pole of the holdout pennants carries no separate flame object any more (Ju fires are static meshes inside the town); `vista_r3()` also removes
     any flame card that hangs free in the sky.
  5. siege tents: rounded, SMOOTH-shaded canvas domes (canvas texture), warm shade, GN instances.
Env VISTA_R3=0 switches everything off (the round-2 look, for before / after)."""
import math, os
import numpy as np

J = None; VS = None; bpy = None; V = None
def bind(j, vs):
    global J, VS, bpy, V
    from mathutils import Vector
    J = j; VS = vs; bpy = j.bpy; V = Vector

def enabled(): return os.environ.get('VISTA_R3', '1') != '0'

T_SHADE = (0.58, 0.46, 0.50)         # shade side of the fields / props: warm brown with only a touch of violet
_C = {}                              # per build caches

def _h(*a):
    h = 2166136261
    for v in a: h = ((h ^ (int(v) & 0xffffffff)) * 16777619) & 0xffffffff
    return h

def wmat(hexcol, gain=1.0, T=T_SHADE, image=None, tag=''):
    P = J.STATE['P']; pre = J.STATE['pre']; sm = tuple(t / s for t, s in zip(T, P['shade']))
    name = '%sr3_%s_%s_%g_%s' % (pre, hexcol.lstrip('#') if image is None else image, tag, gain, '_'.join('%.2f' % t for t in T))
    if name in _C: return _C[name]
    kw = dict(image=J.STATE['tx'][image]) if image else dict(color=hexcol)
    m = J._untoon(J.mat_lit(name, gain=gain, shade_mul=sm, form=None, shade_mix=0.0, **kw)); _C[name] = m; return m

def _furrow(m, axis, freq, depth, tint):
    """Multiply the image of mat_lit material m by a furrow stripe pattern (stripes vary along UV axis `axis`) and a crop tint."""
    nt = m.node_tree; N = nt.nodes.new; L = nt.links.new
    tex = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeTexImage'][0]; old = [(l.to_socket) for l in tex.outputs['Color'].links]
    for l in list(tex.outputs['Color'].links): nt.links.remove(l)
    tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['UV'], sp.inputs[0])
    mu = N('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = freq * 2 * math.pi; L(sp.outputs[axis], mu.inputs[0])
    si = N('ShaderNodeMath'); si.operation = 'SINE'; L(mu.outputs[0], si.inputs[0])
    ma = N('ShaderNodeMath'); ma.operation = 'MULTIPLY_ADD'; ma.inputs[1].default_value = -0.5 * depth; ma.inputs[2].default_value = 1.0 - 0.5 * depth; L(si.outputs[0], ma.inputs[0])
    t1 = N('ShaderNodeMix'); t1.data_type = 'RGBA'; t1.blend_type = 'MULTIPLY'; t1.inputs[0].default_value = 1.0; t1.inputs[6].default_value = (*tint, 1.0); L(ma.outputs[0], t1.inputs[7])
    t2 = N('ShaderNodeMix'); t2.data_type = 'RGBA'; t2.blend_type = 'MULTIPLY'; t2.inputs[0].default_value = 1.0; L(tex.outputs['Color'], t2.inputs[6]); L(t1.outputs[2], t2.inputs[7])
    for s in old: L(t2.outputs[2], s)

def water_mat():
    """Round 4: dusk / dawn water: dark teal body, a Fresnel-weighted glossy lobe that reflects the sky dome (orange horizon), ripple bump (glints)."""
    name = J.STATE['pre'] + 'r4_water'
    if name in _C: return _C[name]
    base = wmat('#2c5058', 1.0, T=(0.52, 0.48, 0.52), tag='waterbase')
    m = base.copy(); m.name = name; nt = m.node_tree; N = nt.nodes.new; L = nt.links.new
    out = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeOutputMaterial'][0]; src = out.inputs['Surface'].links[0].from_socket
    sky = {'DUSK': (1.0, 0.50, 0.20), 'DAWN': (1.0, 0.66, 0.50)}.get(J.STATE.get('light'), (1.0, 0.5, 0.2))
    gl = N('ShaderNodeEmission'); gl.inputs['Color'].default_value = (*sky, 1.0); gl.inputs['Strength'].default_value = 1.1               # the sky seen in the water (the dome is not visible to reflection rays)
    tc = N('ShaderNodeTexCoord'); nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.55; nz.inputs['Detail'].default_value = 4.0; L(tc.outputs['Object'], nz.inputs['Vector'])
    rp = N('ShaderNodeMapRange'); rp.inputs[1].default_value = 0.40; rp.inputs[2].default_value = 0.62; rp.inputs[3].default_value = 0.30; rp.inputs[4].default_value = 1.0; rp.clamp = True; L(nz.outputs['Fac'], rp.inputs[0])   # ripples: bright / dark streaks
    gs = N('ShaderNodeMapRange'); gs.inputs[1].default_value = 0.66; gs.inputs[2].default_value = 0.70; gs.inputs[3].default_value = 0.0; gs.inputs[4].default_value = 1.0; gs.clamp = True; L(nz.outputs['Fac'], gs.inputs[0])  # glints
    fr = N('ShaderNodeLayerWeight'); fr.inputs['Blend'].default_value = 0.5
    cl = N('ShaderNodeMath'); cl.operation = 'MULTIPLY_ADD'; cl.use_clamp = True; cl.inputs[1].default_value = 1.2; cl.inputs[2].default_value = 0.30; L(fr.outputs['Facing'], cl.inputs[0])
    mu = N('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.use_clamp = True; L(cl.outputs[0], mu.inputs[0]); L(rp.outputs[0], mu.inputs[1])
    mx = N('ShaderNodeMixShader'); L(mu.outputs[0], mx.inputs[0]); L(src, mx.inputs[1]); L(gl.outputs['Emission'], mx.inputs[2])
    gg = N('ShaderNodeEmission'); gg.inputs['Color'].default_value = (1.0, 0.92, 0.75, 1.0); gg.inputs['Strength'].default_value = 2.2
    mg = N('ShaderNodeMixShader'); L(gs.outputs[0], mg.inputs[0]); L(mx.outputs['Shader'], mg.inputs[1]); L(gg.outputs['Emission'], mg.inputs[2]); L(mg.outputs['Shader'], out.inputs['Surface'])
    _C[name] = m; return m

def cloth(Bk, M, name, top, fw, fh, kind, seed):
    """Round 4: one silk pennant cloth, own object, hanging from the point `top` (pole top): swallow-tail, a travelling fold and a slight curve, red / gold border cells
    (no coplanar trim faces: no speckle). Origin is set to `top` by the vista post step, so scaling grows the cloth from the pole top."""
    b = Bk(name, hull=0.0, shadow=False); nx, ny = 12, 7
    body, edge = (M['silk_blk'], M['silk_red']) if kind == 'yan' else (M['silk_qi'], M['silk_gold'])
    ph = seed * 1.7; amp = fh * 0.16
    def P(u, v):
        x = fw * u; z = -fh * v * (1.0 - 0.38 * u)
        y = amp * u ** 0.9 * math.sin(u * 7.0 + v * 1.4 + ph) + fh * 0.07 * u * (v - 0.5) ** 2 * 2.0 + 0.12 * fh * u * u
        return top + V((x, y, z))
    for i in range(nx):
        for j in range(ny):
            pts = [P(i / nx, j / ny), P((i + 1) / nx, j / ny), P((i + 1) / nx, (j + 1) / ny), P(i / nx, (j + 1) / ny)]
            mat = edge if (j == 0 or j == ny - 1 or i == nx - 1) else body
            b.oface(pts, mat, [(0, 0)] * 4, (0, -1, 0)); b.oface(pts[::-1], mat, [(0, 0)] * 4, (0, 1, 0))

def materials(M):
    """Round-3 materials: returns a copy of M with warm fields (8 variants: 2 textures x 4 crop tints, furrows), dusk water, and the r3 prop materials."""
    _C.clear(); M = dict(M); tx = J.STATE['tx']
    M['vwater'] = water_mat()
    M['r3_gate'] = wmat(None, 0.95, image='planks', tag='gate', T=(0.66, 0.48, 0.40))                  # round 4: warm timber gate leaves (was the navy `black`)
    M['silk_blk'] = J._glossy(wmat('#3c2c30', 1.25, T=(0.66, 0.50, 0.50), tag='silkb'), (1.0, 0.70, 0.46), 0.55, 0.26)    # round 4: lit black silk (sheen picks up the dusk rim)
    M['silk_red'] = J._glossy(wmat('#c03022', 1.2, T=(0.66, 0.46, 0.44), tag='silkr'), (1.0, 0.62, 0.40), 0.35, 0.3)
    M['silk_qi'] = J._glossy(wmat('#c8142c', 1.2, T=(0.64, 0.42, 0.46), tag='silkq'), (1.0, 0.6, 0.45), 0.45, 0.26)        # Qi crimson
    M['silk_gold'] = J._glossy(wmat('#d8a848', 1.2, T=(0.66, 0.52, 0.40), tag='silkg'), (1.0, 0.8, 0.5), 0.35, 0.3)
    M['r3_glint'] = J.mat_emit(J.STATE['pre'] + 'r3_glint', '#ffe2a8', strength=2.6)
    M['r3_lampg'] = J.mat_emit(J.STATE['pre'] + 'r3_lampg', '#ffc060', strength=6.0)
    M['r3_win'] = J.mat_emit(J.STATE['pre'] + 'r3_win', '#ffb048', strength=3.2)
    M['r3_door'] = wmat('#3a2418', 1.0, tag='door')
    for nm, g in (('rammed', 0.78), ('rammed_d', 0.72), ('tiles', 1.0), ('tiles_d', 0.95)):                       # town walls and roofs: the same warm shade (no navy faces)
        M[nm] = wmat(None, g, image=nm, tag='tw', T=(0.60, 0.46, 0.50))
    M['plaster'] = wmat('#d8c8a8', 1.1, tag='tw'); M['plaster_d'] = wmat('#b0a088', 1.05, tag='tw')
    tints = [(1.0, 1.0, 1.0), (1.18, 1.04, 0.78), (0.86, 1.10, 0.84), (1.08, 0.86, 0.72)]
    for a, img in enumerate(('fields', 'fields_b')):
        for k, tn in enumerate(tints):
            m = J._untoon(J.mat_lit('%sr3_field_%d_%d' % (J.STATE['pre'], a, k), image=tx[img], gain=0.95, shade_mul=tuple(t / s for t, s in zip(T_SHADE, J.STATE['P']['shade'])), form=None, shade_mix=0.0))
            _furrow(m, 'Y' if a == 0 else 'X', 21.0, 0.34, tn); M['r3_field_%d_%d' % (a, k)] = m
    return M

def field_mat(M, xa, ya):
    px, py = int((xa + 900) / 70), int((ya + 900) / 70); h = _h(px, py, 5)
    return M['r3_field_%d_%d' % ((h >> 3) & 1, h % 4)]

# ---------------------------------------------------------------- instancing (geometry nodes: one points object + one hidden prototype per kind)
def proto(name, mb, smooth=True):
    o = mb.obj('r3p_' + name, J.STATE['SET'], hull=0.0, smooth=smooth); o.hide_render = True; o.hide_viewport = True; J.no_bounce(o); return o

def scatter(name, pr, pts, rots, scls, coll=None):
    """Instance prototype object `pr` at pts (x, y, z) with yaw (rad) and uniform scale: ONE object (a point cloud + a Geometry Nodes 'Instance on Points')."""
    if not pts: return None
    coll = coll or J.STATE['SET']
    me = bpy.data.meshes.new('r3pts_' + name); me.from_pydata([tuple(p) for p in pts], [], [])
    ra = me.attributes.new('rot', 'FLOAT_VECTOR', 'POINT'); ra.data.foreach_set('vector', np.array([(0, 0, r) for r in rots], np.float32).ravel())
    sa = me.attributes.new('scl', 'FLOAT_VECTOR', 'POINT'); sa.data.foreach_set('vector', np.array([(s, s, s) for s in scls], np.float32).ravel())
    ob = bpy.data.objects.new('r3_' + name, me); coll.objects.link(ob)
    ng = bpy.data.node_groups.new('r3gn_' + name, 'GeometryNodeTree')
    ng.interface.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry'); ng.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    N = ng.nodes; L = ng.links; gi = N.new('NodeGroupInput'); go = N.new('NodeGroupOutput'); ip = N.new('GeometryNodeInstanceOnPoints'); oi = N.new('GeometryNodeObjectInfo')
    oi.transform_space = 'RELATIVE'; oi.inputs['As Instance'].default_value = True; oi.inputs['Object'].default_value = pr
    na = N.new('GeometryNodeInputNamedAttribute'); na.data_type = 'FLOAT_VECTOR'; na.inputs['Name'].default_value = 'rot'
    nb = N.new('GeometryNodeInputNamedAttribute'); nb.data_type = 'FLOAT_VECTOR'; nb.inputs['Name'].default_value = 'scl'
    L.new(gi.outputs[0], ip.inputs['Points']); L.new(oi.outputs['Geometry'], ip.inputs['Instance']); L.new(na.outputs['Attribute'], ip.inputs['Rotation']); L.new(nb.outputs['Attribute'], ip.inputs['Scale']); L.new(ip.outputs['Instances'], go.inputs[0])
    md = ob.modifiers.new('gn', 'NODES'); md.node_group = ng; J.no_bounce(ob)
    J.STATE['objects'][ob.name] = ob; return ob

# ---------------------------------------------------------------- prototypes
def _blob(mb, c, rx, ry, rz, mat, seg=8, rings=4): J.ellipsoid(mb, c, rx, ry, rz, mat, seg=seg, rings=rings)

def make_protos(M):
    PR = {}; MB = J.MB
    hg = [wmat('#46703a', 1.0, tag='hg'), wmat('#6a8040', 1.0, tag='hg'), wmat('#3a5e38', 1.0, tag='hg')]
    for i, mt in enumerate(hg):
        mb = MB(); _blob(mb, (0, 0, 1.0), 2.8, 1.8, 1.7, mt, 8, 4); _blob(mb, (2.2, 0.3, 0.8), 2.0, 1.5, 1.3, mt, 7, 4); PR['hedge%d' % i] = proto('hedge%d' % i, mb)
    trunk = wmat('#5a3a24', 1.0, tag='tr')
    for i, col in enumerate(('#4a7a46', '#7a8a3a', '#9a7634')):
        mt = wmat(col, 1.05, tag='tree'); mb = MB()
        mb.frustum(V((0, 0, 0)), V((0, 0, 2.6)), 0.45, 0.3, trunk, seg=5, cap0=False)
        _blob(mb, (0, 0, 4.3), 2.3, 2.3, 2.3, mt, 8, 5); _blob(mb, (0.5, 0.3, 6.0), 1.6, 1.6, 1.6, mt, 7, 4)
        PR['tree%d' % i] = proto('tree%d' % i, mb)
    hay = wmat('#c4a45a', 0.9, tag='hay'); haydk = wmat('#b08a3c', 0.95, tag='hay')
    mb = MB(); mb.frustum(V((0, 0, 0)), V((0, 0, 2.4)), 2.3, 1.7, hay, seg=9, cap0=False, cap1=False); mb.frustum(V((0, 0, 2.4)), V((0, 0, 3.7)), 1.7, 0.0, haydk, seg=9, cap0=False); PR['hay'] = proto('hay', mb)
    mb = MB(); _blob(mb, (0, 0, 1.0), 3.3, 1.7, 1.9, hay, 9, 5); PR['rick'] = proto('rick', mb)
    wall = wmat('#d2b88c', 1.1, tag='hut'); roof = wmat('#a88444', 1.0, tag='roof'); door = M['r3_door']
    mb = MB(); J.obox(mb, V((0, 0, 1.4)), V((1, 0, 0)), V((0, 1, 0)), V((0, 0, 1)), 2.6, 2.0, 1.4, wall, 0.1)
    mb.frustum(V((0, 0, 2.7)), V((0, 0, 5.0)), 3.9, 0.0, roof, seg=4, cap0=False)
    mb.oface([V((-0.7, -2.02, 0)), V((0.7, -2.02, 0)), V((0.7, -2.02, 1.8)), V((-0.7, -2.02, 1.8))], door, [(0, 0)] * 4, (0, -1, 0)); PR['hut'] = proto('hut', mb, smooth=False)
    mb2 = MB(); J.obox(mb2, V((0, 0, 1.4)), V((1, 0, 0)), V((0, 1, 0)), V((0, 0, 1)), 2.6, 2.0, 1.4, wall, 0.1)
    mb2.frustum(V((0, 0, 2.7)), V((0, 0, 5.0)), 3.9, 0.0, roof, seg=4, cap0=False)
    mb2.oface([V((-0.7, -2.02, 0)), V((0.7, -2.02, 0)), V((0.7, -2.02, 1.8)), V((-0.7, -2.02, 1.8))], door, [(0, 0)] * 4, (0, -1, 0))
    mb2.oface([V((1.3, -2.03, 1.0)), V((2.1, -2.03, 1.0)), V((2.1, -2.03, 1.9)), V((1.3, -2.03, 1.9))], M['r3_win'], [(0, 0)] * 4, (0, -1, 0)); PR['hut_lit'] = proto('hut_lit', mb2, smooth=False)
    # cart: box bed, two wheels, a hay load, a pole and an ox
    wood = wmat('#7a5230', 1.0, tag='cart'); ox = wmat('#7a5640', 1.1, tag='ox')
    mb = MB(); J.obox(mb, V((0, 0, 1.15)), V((1, 0, 0)), V((0, 1, 0)), V((0, 0, 1)), 2.3, 1.4, 0.35, wood, 0.1)
    for sy in (-1, 1): mb.frustum(V((0, sy * 1.5, 0.9)), V((0, sy * 1.7, 0.9)), 0.95, 0.95, wood, seg=8)
    _blob(mb, (0, 0, 2.2), 2.0, 1.2, 0.9, hay, 7, 4); mb.frustum(V((2.2, 0, 1.2)), V((4.6, 0, 1.3)), 0.12, 0.12, wood, seg=4); _blob(mb, (5.8, 0, 1.4), 1.6, 0.8, 0.9, ox, 7, 4); PR['cart'] = proto('cart', mb, smooth=False)
    cols = ('#b8472e', '#e3d3a8', '#3b6f7a', '#c89030')
    for i, c in enumerate(cols):
        mt = wmat(c, 1.1, tag='fig'); mb = MB(); mb.frustum(V((0, 0, 0)), V((0, 0, 2.4)), 0.8, 0.45, mt, seg=6, cap0=False); mb.sphere(V((0, 0, 2.95)), 0.42, wmat('#d8a47a', 1.1, tag='skin'), seg=6, rings=4)
        mb.frustum(V((0, 0, 3.15)), V((0, 0, 3.7)), 0.95, 0.0, wmat('#c8a050', 1.0, tag='hat'), seg=6, cap0=False); PR['fig%d' % i] = proto('fig%d' % i, mb, smooth=False)
    # siege tent: smooth canvas dome with a dark doorway, rounded
    def barrel(p):                                                    # rounded barrel tent: elliptic section, long ridge, domed ends
        return V((p.x, 4.6 * math.copysign(abs(p.y / 4.2) ** 0.45, p.y), p.z))
    for key, tex, tg in (('tent', 'canvas', 'tent'), ('tent_b', 'hide', 'tentb')):
        cv = wmat(None, 0.5 if tex == 'canvas' else 0.8, image=tex, tag=tg, T=(0.56, 0.44, 0.46)); mb = MB()
        J.ellipsoid(mb, (0, 0, 0), 2.6, 4.2, 2.9, cv, seg=14, rings=8, uvs=(3, 2), th=(math.pi / 2, math.pi), fn=barrel)
        mb.oface([V((-0.8, -4.62, 0.05)), V((0.8, -4.62, 0.05)), V((0.55, -4.45, 2.0)), V((-0.55, -4.45, 2.0))], door, [(0, 0)] * 4, (0, -1, 0))
        mb.frustum(V((0, -5.6, 3.0)), V((0, 5.6, 3.0)), 0.14, 0.14, wmat('#5a3a24', 1.0, tag='tr'), seg=5); PR[key] = proto(key, mb, smooth=True)
    return PR

# ---------------------------------------------------------------- placement
def _seg_dist(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2)); return math.hypot(px - ax - t * dx, py - ay - t * dy)

def _dk(p):
    """Props far from the shot cameras (about (0, -190)) grow a little so they still read at phone size."""
    return min(2.3, max(1.0, 0.65 + math.hypot(p[0], p[1] + 190.0) / 190.0))

def make_blocked(towns, road_pts):
    jx, jy = VS.JIMO; ju = VS.JU
    def blocked(x, y, pad=0.0, road=0.0):
        if abs(y - VS.river_y(x)) < 15 + pad: return True
        if math.hypot(x - jx, y - jy) < 54 + pad: return True
        if jx - 44 - pad < x < jx + 62 + pad and jy - 96 - pad < y < jy - 36 + pad: return True                  # the Yan siege camp
        if math.hypot(x - ju[0], y - ju[1]) < 62 + pad: return True
        for t in towns:
            if math.hypot(x - t['x'], y - t['y']) < t['s'] * 0.78 + 3 + pad: return True
        if road > 0:
            for a, b in zip(road_pts[:-1], road_pts[1:]):
                if _seg_dist(x, y, a[0], a[1], b[0], b[1]) < road + pad: return True
        return False
    return blocked

def dress(Bk, M, towns, road_pts, tents):
    """Instanced farmland + river glints + tents; returns counts."""
    r = J._rnd(31); th = VS.terrain_h; PR = make_protos(M); blocked = make_blocked(towns, road_pts); S = J.STATE; cnt = {}
    X0, X1, Y0, Y1 = -330.0, 330.0, -230.0, 470.0
    # --- hedgerows and tree lines along patch edges (patch = 70 D, edges at 10 + 70 k)
    hedge = [[], [], []]; tree = [[], [], []]; hay = []; rick = []; hut = [[], []]
    def edge(a, b, kind, key):
        L = math.hypot(b[0] - a[0], b[1] - a[1]); ang = math.atan2(b[1] - a[1], b[0] - a[0]); step = 3.4 if kind == 'hedge' else 8.0; n = int(L / step)
        for q in range(n):
            t = (q + 0.5) / n; x = a[0] + (b[0] - a[0]) * t + r.uniform(-0.6, 0.6); y = a[1] + (b[1] - a[1]) * t + r.uniform(-0.6, 0.6)
            if blocked(x, y, 1.0, road=2.5): continue
            if kind == 'hedge':
                if r.random() < 0.08: continue
                hedge[(key + q // 6) % 3].append(((x, y, th(x, y) - 0.2), ang, r.uniform(0.85, 1.25)))
            else:
                tree[(key + q) % 3].append(((x, y, th(x, y) - 0.1), r.uniform(0, 6.28), r.uniform(0.85, 1.35)))
    xs = [10 + 70 * k for k in range(-5, 6)]; ys = [10 + 70 * k for k in range(-4, 8)]
    for xi in xs:
        for yj0, yj1 in zip(ys[:-1], ys[1:]):
            h = _h(int(xi), int(yj0), 11) % 100
            if h < 68: edge((xi, yj0), (xi, yj1), 'hedge' if h % 5 else 'tree', h)
            elif h < 80: edge((xi, yj0), (xi, yj1), 'tree', h)
    for yj in ys:
        for xi0, xi1 in zip(xs[:-1], xs[1:]):
            h = _h(int(xi0), int(yj), 13) % 100
            if h < 68: edge((xi0, yj), (xi1, yj), 'hedge' if h % 5 else 'tree', h)
            elif h < 80: edge((xi0, yj), (xi1, yj), 'tree', h)
    # willows on the river banks
    for k in range(70):
        x = X0 + 4 + k * 9.4 + r.uniform(-2, 2); side = -1 if k % 2 else 1; y = VS.river_y(x) + side * r.uniform(11.5, 13.5)
        if blocked(x, y, 0.0): continue
        tree[k % 3].append(((x, y, th(x, y)), r.uniform(0, 6.28), r.uniform(0.9, 1.3)))
    # haystacks (clusters), farm huts (near patch corners, some lit)
    for k in range(420):
        cx, cy = r.uniform(X0, X1), r.uniform(Y0, Y1)
        if blocked(cx, cy, 3.0, road=3.0): continue
        for q in range(r.randint(2, 5)):
            x, y = cx + r.uniform(-9, 9), cy + r.uniform(-9, 9)
            if blocked(x, y, 1.0): continue
            (hay if q % 3 else rick).append(((x, y, th(x, y) - 0.1), r.uniform(0, 6.28), r.uniform(0.8, 1.3)))
    for k in range(200):
        px, py = r.choice(xs), r.choice(ys); x, y = px + r.uniform(-10, 10), py + r.uniform(-10, 10)
        if blocked(x, y, 4.0, road=2.0): continue
        hut[1 if r.random() < 0.45 else 0].append(((x, y, th(x, y) - 0.1), math.radians(r.choice((0, 90, 180, 270)) + r.uniform(-12, 12)), r.uniform(0.9, 1.3)))
        if len(hut[0]) + len(hut[1]) >= 78: break
    for nm, lst, key in [('hedge%d' % i, hedge[i], 'hedge%d' % i) for i in range(3)] + [('tree%d' % i, tree[i], 'tree%d' % i) for i in range(3)] + [('hay', hay, 'hay'), ('rick', rick, 'rick'), ('hut', hut[0], 'hut'), ('hut_lit', hut[1], 'hut_lit')]:
        ob = scatter(nm, PR[key], [p for p, a, s in lst], [a for p, a, s in lst], [s * _dk(p) for p, a, s in lst]); cnt[nm] = len(lst)
    # --- roads: carts and tiny figures
    carts = []; figs = [[], [], [], []]
    segs = [(a, b) for a, b in zip(road_pts[:-1], road_pts[1:])]
    for si, (a, b) in enumerate(segs):
        L = math.hypot(b[0] - a[0], b[1] - a[1]); ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for q in range(int(L / 28)):
            t = r.uniform(0.08, 0.92); x = a[0] + (b[0] - a[0]) * t; y = a[1] + (b[1] - a[1]) * t
            if blocked(x, y, 0.0) and math.hypot(x - VS.JIMO[0], y - VS.JIMO[1]) < 70: continue
            if abs(y - VS.river_y(x)) < 12: continue
            if r.random() < 0.28: carts.append(((x, y, th(x, y) + 0.2), ang + (math.pi if r.random() < 0.5 else 0.0), r.uniform(0.9, 1.15) * 1.1))
            else:
                for g in range(r.randint(1, 3)):
                    xx, yy = x + g * 2.2 * math.cos(ang) + r.uniform(-0.6, 0.6), y + g * 2.2 * math.sin(ang) + r.uniform(-0.6, 0.6)
                    figs[(si + g) % 4].append(((xx, yy, th(xx, yy) + 0.2), ang, 1.25))
    scatter('cart', PR['cart'], [p for p, a, s in carts], [a for p, a, s in carts], [s for p, a, s in carts]); cnt['cart'] = len(carts)
    for i in range(4): scatter('fig%d' % i, PR['fig%d' % i], [p for p, a, s in figs[i]], [a for p, a, s in figs[i]], [s for p, a, s in figs[i]]); cnt['fig%d' % i] = len(figs[i])
    # --- siege tents (smooth canvas domes)
    for key, sel in (('tent', [q for i, q in enumerate(tents) if i % 3]), ('tent_b', [q for i, q in enumerate(tents) if not i % 3])):
        scatter(key, PR[key], [(x, y, th(x, y) - 0.05) for x, y, h, yaw in sel], [math.radians(yaw + 90) for x, y, h, yaw in sel], [1.0 + 0.1 * (i % 3 - 1) for i in range(len(sel))])
    cnt['tent'] = len(tents)
    # --- river / moat glints: bright flecks on the water, thicker towards the sun side
    gl = Bk('r3glints', shadow=False)
    for k in range(420):
        x = X0 + r.uniform(0, X1 - X0); yc = VS.river_y(x) + r.uniform(-7.5, 7.5); w = r.uniform(2.0, 4.4); d = r.uniform(0.35, 0.8)
        gl.oface([V((x - w / 2, yc - d / 2, -0.42)), V((x + w / 2, yc - d / 2, -0.42)), V((x + w / 2, yc + d / 2, -0.42)), V((x - w / 2, yc + d / 2, -0.42))], M['r3_glint'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, 1))
    jx, jy = VS.JIMO; z = th(jx, jy)
    for k in range(22):
        a = r.uniform(0, 6.283); R = r.uniform(39.5, 42.5); x, y = jx + R * math.cos(a), jy + R * math.sin(a); w = r.uniform(2.2, 4.0)
        gl.oface([V((x - w / 2, y - 0.3, z + 0.16)), V((x + w / 2, y - 0.3, z + 0.16)), V((x + w / 2, y + 0.3, z + 0.16)), V((x - w / 2, y + 0.3, z + 0.16))], M['r3_glint'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, 1))
    S['r3_counts'] = cnt; return cnt

# ---------------------------------------------------------------- Ju
def ju_extras(Bk, M, t, z0, yaw):
    """Ju: dense lit houses, a watch tower with a fire basket, wall lamps, gate fires (static flame meshes), glow dome and a warm ground pool."""
    cx, cy, s = t['x'], t['y'], t['s']; F = J.Frame((cx, cy, z0), yaw); wh = s * 0.17; r = J._rnd(77)
    bd = Bk('towns', hull=0.0); rf = Bk('townroofs', hull=0.0); gl = Bk('townglow', shadow=False); hl = Bk('halos', shadow=False); lm = Bk('julamps', shadow=False)
    for q in range(16):
        hx, hy = r.uniform(-s * 0.4, s * 0.4), r.uniform(-s * 0.38, s * 0.38); hw, hd = r.uniform(s * 0.08, s * 0.13), r.uniform(s * 0.07, s * 0.1); hh = r.uniform(s * 0.06, s * 0.1)
        J.obox(bd, F.p(hx, hy, hh / 2), F.X, F.Y, F.Z, hw / 2, hd / 2, hh / 2, M['plaster'] if q % 2 else M['plaster_d'], uvk=0.1)
        J.hip_roof(rf, F.p(hx, hy, hh), yaw, hw / 2 + s * 0.015, hd / 2 + s * 0.015, max(0.01, hw / 2 - hd / 2), 0.0, s * 0.045, M, lift=0.0, nx=3, ny=2, mat=M['tiles'], wadang=False)
        J.flat(gl, F.p(hx - hw * 0.3, hy - hd / 2 - 0.08, hh * 0.22), F.X * (hw * 0.6), F.Z * (hh * 0.5), M['r3_win'])
    # watch tower in the middle, taller than the walls, a fire basket on top
    tw = s * 0.07; th_ = wh * 2.4
    J.obox(bd, F.p(0, s * 0.05, th_ / 2), F.X, F.Y, F.Z, tw, tw, th_ / 2, M['rammed_d'], uvk=0.1)
    J.hip_roof(rf, F.p(0, s * 0.05, th_), yaw, tw * 1.5, tw * 1.5, 0.0, 0.0, s * 0.07, M, lift=0.0, nx=3, ny=3, mat=M['tiles'], wadang=False)
    J.flat(gl, F.p(-tw * 0.5, s * 0.05 - tw - 0.1, th_ * 0.7), F.X * (tw * 1.0), F.Z * (tw * 1.3), M['r3_win'])
    for sx in (-1, 1): J.flat(gl, F.p(sx * tw * 0.3 - tw * 0.18, s * 0.05 - tw - 0.1, th_ * 0.45), F.X * (tw * 0.36), F.Z * (tw * 0.8), M['r3_win'])
    top = F.p(0, s * 0.05, th_ + s * 0.07 + 1.0); J.flame(gl, top, s * 0.14, s * 0.05, seed=5, n=3); J.halo(hl, top + V((0, 0, 2)), s * 0.55, M['halo']); J.halo(hl, top + V((0, 0, 2)), s * 0.9, M['halo_big'])
    # wall lamps: an emissive lantern every s/8 on top of the four curtain walls, each with a small halo
    for sgn in (-1, 1):
        for q in range(-3, 4):
            for (px, py) in ((q * s / 7.0, sgn * s / 2), (sgn * s / 2, q * s / 7.0)):
                p = F.p(px, py, wh + 0.9); lm.sphere(p, s * 0.014, M['r3_lampg'], seg=6, rings=4); J.halo(hl, p, s * 0.06, M['halo_s'])
    # gate: two fire stakes (static flames) and a glowing gate arch
    gp = F.p(0, -s / 2 - 0.3, 0)
    for sx in (-1, 1):
        b = F.p(sx * s * 0.09, -s / 2 - 1.6, 0); J.rod(bd, b, b + V((0, 0, 4.5)), 0.22, M['wood_d'], seg=5); J.flame(gl, b + V((0, 0, 4.5)), 3.4, 1.0, seed=sx + 9, n=3); J.halo(hl, b + V((0, 0, 6)), 9.0, M['halo'])
    J.flat(gl, F.p(-s * 0.06, -s / 2 - 0.35, 0.1), F.X * (s * 0.12), F.Z * (wh * 0.8), M['gate_glow'])
    # the glow: a dome of additive cards over the town and a warm pool on the ground around it
    c = V((cx, cy, z0 + wh + 3)); J.halo(hl, c, s * 1.45, M['halo_big']); J.halo(hl, c, s * 0.85, M['halo_big'])
    pl = Bk('r3pool', shadow=False); R = s * 1.7
    pl.oface([V((cx - R, cy - R, z0 + 0.35)), V((cx + R, cy - R, z0 + 0.35)), V((cx + R, cy + R, z0 + 0.35)), V((cx - R, cy + R, z0 + 0.35))], M['pool_w'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, 1))

# ---------------------------------------------------------------- post-build finisher (also J.vista_r3())
def finish(sweep=True):
    """Idempotent. Pennants / trees / tents: no cast shadow slabs; soft sun; tents smooth; stray flame cards in the sky removed. Returns a dict of what was done."""
    S = J.STATE; out = dict(shadow_off=0, swept=[])
    if S.get('loc') != 'vista': return out
    for p in S.get('pennants', ()):
        o = p.get('ob')
        if o is not None and o.visible_shadow: o.visible_shadow = False; out['shadow_off'] += 1
    for n in ('wood', 'cloth', 'vtrees'):
        o = S['objects'].get(n)
        if o is not None and o.visible_shadow: o.visible_shadow = False; out['shadow_off'] += 1
    try: S['sun'].data.angle = math.radians(3.5)
    except Exception: pass
    if sweep:
        for fc in list(S.get('flame_cards', ())):
            root = fc['root']
            if root.parent is None and root.matrix_world.translation.z > VS.terrain_h(root.matrix_world.translation.x, root.matrix_world.translation.y) + 6.0:
                nm = root.name
                for ch in list(root.children_recursive): bpy.data.objects.remove(ch, do_unlink=True)
                bpy.data.objects.remove(root, do_unlink=True); S['flame_cards'].remove(fc); out['swept'].append(nm)
        for fi in list(S.get('fires', ())):                                                  # a mesh flame whose origin was moved off its base would float: put it back
            ob = fi['ob']
            if (ob.location - fi['base']).length > 0.05: ob.location = fi['base']
    S['r3_done'] = True; return out

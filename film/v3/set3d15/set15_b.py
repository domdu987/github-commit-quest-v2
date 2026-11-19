"""Location B: Olympic stadium 1968 (metres in the builders). Bowl centre (0, 8); jump set at (0, 11.6); foam pit centre (0, 15)."""
import math
import numpy as np
import bpy
from mathutils import Vector, Matrix, Euler
import set15_lib as L
from set15_lib import S, mat, mat_emit, rnd, fin, adopt, root, plane_at, STATE
import set15_props as PR
import set15_a as LA

SX, SY = 0.0, 8.0
NROW = 28; RW = 0.9; RISE = 0.72; A0 = 64.0; B0 = 36.0
BAR_Y_B = 11.6; PIT_B = (0.0, 15.0); FOAM_TOP = 1.0
MARKS_B = {}
def ell_pt(a, b, t): return (SX + a * math.cos(t), SY + b * math.sin(t))

# ------------------------------------------------------------------ geometry-node animation groups (crowd bob, flag wave)
def _gn_new(name):
    ng = bpy.data.node_groups.new(name, 'GeometryNodeTree')
    ng.interface.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry'); ng.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    return ng

def crowd_group(ctl):
    """z offset of every vertex of a figure: hop = amp x w x (0.5 + 0.5 sin(2 pi f t + phase)); cheer: stand up + arms raised (arm weight aw).
    amp, f, cheer = the location x, y, z of the control empty CROWD_CTL (keyed by the crowd hooks)."""
    ng = _gn_new('S15_crowd'); N = ng.nodes.new; Lk = ng.links.new; gi = N('NodeGroupInput'); go = N('NodeGroupOutput')
    def attr(nm):
        a = N('GeometryNodeInputNamedAttribute'); a.data_type = 'FLOAT'; a.inputs['Name'].default_value = nm; return a.outputs['Attribute']
    oi = N('GeometryNodeObjectInfo'); oi.inputs['Object'].default_value = ctl; oi.transform_space = 'ORIGINAL'
    sp = N('ShaderNodeSeparateXYZ'); Lk(oi.outputs['Location'], sp.inputs[0])
    tm = N('GeometryNodeInputSceneTime')
    def M_(op, a=None, b=None, c=None):
        n = N('ShaderNodeMath'); n.operation = op
        for i, v in enumerate((a, b, c)):
            if v is None: continue
            if isinstance(v, (int, float)): n.inputs[i].default_value = v
            else: Lk(v, n.inputs[i])
        return n.outputs[0]
    # phase arg = 2 pi * (f * t) + phase
    ft = M_('MULTIPLY', sp.outputs['Y'], tm.outputs['Seconds']); arg = M_('ADD', M_('MULTIPLY', ft, 6.2831853), attr('ph'))
    hop = M_('MULTIPLY', M_('MULTIPLY_ADD', M_('SINE', arg), 0.5, 0.5), M_('MULTIPLY', sp.outputs['X'], attr('wt')))
    cheer = sp.outputs['Z']
    stand = M_('MULTIPLY', M_('MULTIPLY', cheer, attr('wt')), 0.14)
    arms = M_('MULTIPLY', M_('MULTIPLY', cheer, attr('aw')), 0.42)
    tot = M_('ADD', M_('ADD', hop, stand), arms)
    cb = N('ShaderNodeCombineXYZ'); Lk(tot, cb.inputs['Z'])
    setp = N('GeometryNodeSetPosition'); Lk(gi.outputs[0], setp.inputs['Geometry']); Lk(cb.outputs[0], setp.inputs['Offset']); Lk(setp.outputs[0], go.inputs[0])
    return ng

def wave_group(ctl):
    """Flag / cloth wave: offset = dir x amp x u x sin(2 pi (f t - u x 0.9)) (+ a small droop). amp = x of FLAG_CTL, f = y; per-vertex attributes u (0 at the pole), dir (vector)."""
    ng = _gn_new('S15_wave'); N = ng.nodes.new; Lk = ng.links.new; gi = N('NodeGroupInput'); go = N('NodeGroupOutput')
    a_u = N('GeometryNodeInputNamedAttribute'); a_u.data_type = 'FLOAT'; a_u.inputs['Name'].default_value = 'u'
    a_d = N('GeometryNodeInputNamedAttribute'); a_d.data_type = 'FLOAT_VECTOR'; a_d.inputs['Name'].default_value = 'dir'
    a_p = N('GeometryNodeInputNamedAttribute'); a_p.data_type = 'FLOAT'; a_p.inputs['Name'].default_value = 'ph'
    oi = N('GeometryNodeObjectInfo'); oi.inputs['Object'].default_value = ctl; oi.transform_space = 'ORIGINAL'
    sp = N('ShaderNodeSeparateXYZ'); Lk(oi.outputs['Location'], sp.inputs[0]); tm = N('GeometryNodeInputSceneTime')
    def M_(op, a=None, b=None, c=None):
        n = N('ShaderNodeMath'); n.operation = op
        for i, v in enumerate((a, b, c)):
            if v is None: continue
            if isinstance(v, (int, float)): n.inputs[i].default_value = v
            else: Lk(v, n.inputs[i])
        return n.outputs[0]
    ft = M_('MULTIPLY', sp.outputs['Y'], tm.outputs['Seconds']); arg = M_('MULTIPLY', M_('SUBTRACT', M_('ADD', ft, a_p.outputs['Attribute']), M_('MULTIPLY', a_u.outputs['Attribute'], 0.9)), 6.2831853)
    amp = M_('MULTIPLY', M_('MULTIPLY', sp.outputs['X'], a_u.outputs['Attribute']), M_('SINE', arg))
    vs = N('ShaderNodeVectorMath'); vs.operation = 'SCALE'; Lk(a_d.outputs['Attribute'], vs.inputs[0]); Lk(amp, vs.inputs['Scale'])
    sw = N('ShaderNodeSeparateXYZ'); Lk(vs.outputs['Vector'], sw.inputs[0])
    dz = M_('MULTIPLY', M_('MULTIPLY', a_u.outputs['Attribute'], M_('SINE', M_('MULTIPLY', M_('ADD', arg, 1.5), 1.0))), M_('MULTIPLY', sp.outputs['X'], 0.15))
    cb = N('ShaderNodeCombineXYZ'); Lk(sw.outputs['X'], cb.inputs['X']); Lk(sw.outputs['Y'], cb.inputs['Y']); Lk(dz, cb.inputs['Z'])
    setp = N('GeometryNodeSetPosition'); Lk(gi.outputs[0], setp.inputs['Geometry']); Lk(cb.outputs[0], setp.inputs['Offset']); Lk(setp.outputs[0], go.inputs[0])
    return ng

def ctl_empty(name, loc):
    e = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(e); e.location = loc; e.empty_display_size = 0.5
    STATE['SET'].objects.link(e); bpy.context.scene.collection.objects.unlink(e); return e

def mesh_from_arrays(name, V, F, mat_, attrs, grp=None):
    me = bpy.data.meshes.new(name); me.from_pydata(V.tolist() if hasattr(V, 'tolist') else V, [], F.tolist() if hasattr(F, 'tolist') else F); me.update()
    for k, (typ, arr) in attrs.items():
        a = me.attributes.new(k, typ, 'POINT')
        if typ == 'FLOAT': a.data.foreach_set('value', arr.astype(np.float32))
        else: a.data.foreach_set('vector', arr.astype(np.float32).reshape(-1))
    me.materials.append(mat_)
    ob = bpy.data.objects.new(name, me); STATE['SET'].objects.link(ob); ob.parent = root(); L.T.no_bounce(ob)
    return ob

CUBE_V = np.array([(-.5, -.5, -.5), (.5, -.5, -.5), (.5, .5, -.5), (-.5, .5, -.5), (-.5, -.5, .5), (.5, -.5, .5), (.5, .5, .5), (-.5, .5, .5)], dtype=np.float64)
CUBE_F = np.array([(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)])

def boxes(centres, sizes, yaws):
    """n boxes -> (V (8n x 3), F (6n x 4)) numpy; sizes (n,3), yaws (n,)."""
    n = len(centres); c = np.cos(yaws)[:, None]; s = np.sin(yaws)[:, None]
    v = CUBE_V[None, :, :] * sizes[:, None, :]
    x = v[..., 0] * c - v[..., 1] * s; y = v[..., 0] * s + v[..., 1] * c
    V = np.stack([x, y, v[..., 2]], -1) + centres[:, None, :]
    F = (CUBE_F[None, :, :] + (np.arange(n) * 8)[:, None, None]).reshape(-1, 4)
    return V.reshape(-1, 3), F

# ------------------------------------------------------------------ crowd
SKINS = ['#d9a070', '#c8895a', '#8a5a3a', '#f0c8a0', '#6a4430', '#e8b488']
def build_crowd(P, M, rr):
    ctl = ctl_empty('CROWD_CTL', (0.012, 0.45, 0.0)); STATE['crowd_ctl'] = ctl
    ng = crowd_group(ctl); k = P.get('crowd_k', 1.0)
    cm = [mat('cw%d' % i, h, h, 1.0, rough=1.0, crowd=True) for i, h in enumerate(S.CROWD_HEX)]
    sk = [mat('sk%d' % i, h, h, 1.0, crowd=True) for i, h in enumerate(SKINS)]
    groups = {}                                            # material -> lists
    def add(mi, c, sz, yaw, ph, wt, aw):
        g = groups.setdefault(mi, dict(c=[], s=[], y=[], ph=[], wt=[], aw=[])); g['c'].append(c); g['s'].append(sz); g['y'].append(yaw); g['ph'].append(ph); g['wt'].append(wt); g['aw'].append(aw)
    cnt = 0
    for i in range(NROW):
        a = A0 + i * RW + 0.55; b = B0 + i * RW + 0.55; z = 1.0 + i * RISE
        t = math.radians(2.0)
        while t < math.radians(358.0):
            s = math.sqrt((a * math.sin(t)) ** 2 + (b * math.cos(t)) ** 2); t += 0.52 / s
            deg = math.degrees(t)
            if rr.random() > 0.93: continue
            if (int(deg / 0.9) % 14) == 0: continue                                   # radial aisles
            x, y = ell_pt(a, b, t); yaw = math.atan2(-math.sin(t) / b, -math.cos(t) / a) + math.pi
            ci = rr.randrange(len(cm)); h = rr.uniform(0.5, 0.64); ph = rr.uniform(0, 6.28); wt = rr.uniform(0.45, 1.0)
            add(('b', ci), (x, y, z + h / 2), (0.3, 0.46, h), yaw + math.pi, ph, wt, 0.0)
            si = rr.randrange(len(sk)); add(('h', si), (x, y, z + h + 0.1), (0.2, 0.2, 0.22), yaw, ph, wt, 0.0)
            for sg in (-1, 1):
                dx = -math.sin(yaw + math.pi) * 0.0; ox = math.cos(yaw + math.pi + 1.5708) * 0.2 * sg; oy = math.sin(yaw + math.pi + 1.5708) * 0.2 * sg
                add(('a', ci), (x + ox, y + oy, z + h * 0.45), (0.08, 0.08, 0.3), yaw, ph, wt, 1.0)
            cnt += 1
    objs = []
    for (kind, mi), g in groups.items():
        V, F = boxes(np.array(g['c']), np.array(g['s']), np.array(g['y'])); n = len(g['c'])
        rep = lambda a_: np.repeat(np.array(a_), 8)
        mt = cm[mi] if kind in ('b', 'a') else sk[mi]
        ob = mesh_from_arrays('crowd_%s%d' % (kind, mi), V, F, mt, dict(ph=('FLOAT', rep(g['ph'])), wt=('FLOAT', rep(g['wt'])), aw=('FLOAT', rep(g['aw']))))
        md = ob.modifiers.new('bob', 'NODES'); md.node_group = ng; objs.append(ob)
    STATE['crowd_n'] = cnt; STATE['crowd_objs'] = objs
    return cnt

def build_flags(P, M, rr):
    """Rim flags: plain stripe cloths on poles, waving through the S15_wave geometry nodes (FLAG_CTL x = amplitude m, y = Hz)."""
    ctl = ctl_empty('FLAG_CTL', (0.32, 0.55, 0.0)); STATE['flag_ctl'] = ctl; ng = wave_group(ctl)
    fc = [['red', 'cream', 'green'], ['blue', 'cream', 'red'], ['yellow', 'red', 'navy'], ['cream', 'blue', 'cream'], ['orange', 'cream', 'teal'], ['green', 'yellow', 'red'], ['navy', 'cream', 'orange'], ['red', 'yellow', 'green']]
    ao = A0 + NROW * RW; bo = B0 + NROW * RW; zt = 1.0 + NROW * RISE
    mb = S.MB('rimpoles'); cloth = {}
    def cloth_add(cmat, V, F, uu, dirv, ph):
        g = cloth.setdefault(cmat, dict(V=[], F=[], u=[], d=[], ph=[])); o = len(g['V']); g['V'] += V; g['F'] += [[o + i for i in f] for f in F]; g['u'] += uu; g['d'] += [dirv] * len(V); g['ph'] += [ph] * len(V)
    def flag(x, y, z, h, cols, yaw, ph, Lf=2.2, Hf=1.4, seg=6):
        mb.rod(M['metal'], (x, y, z), (x, y, z + h), 0.05, 0.03, 6); mb.ell(M['yellow'], (x, y, z + h + 0.06), (0.07, 0.07, 0.07), (6, 4))
        d = Vector((math.cos(yaw), math.sin(yaw), 0)); lat = (-d.y, d.x, 0.0)
        for k_, cn in enumerate(cols):
            zt_ = z + h - 0.1 - Hf * k_ / len(cols); zb_ = z + h - 0.1 - Hf * (k_ + 1) / len(cols); V = []; F = []; uu = []
            for sI in range(seg + 1):
                u = sI / seg; p = (x + d.x * u * Lf, y + d.y * u * Lf)
                V += [(p[0], p[1], zt_), (p[0], p[1], zb_)]; uu += [u, u]
            for sI in range(seg): F.append([2 * sI, 2 * sI + 1, 2 * sI + 3, 2 * sI + 2]); F.append([2 * sI + 2, 2 * sI + 3, 2 * sI + 1, 2 * sI])
            cloth_add(M[cn], V, F, uu, lat, ph)
    k = 0
    for d_ in range(8, 354, 4):
        u = math.radians(d_); x, y = ell_pt(ao - 0.6, bo - 0.6, u)
        flag(x, y, zt + 1.0, 4.6, fc[k % len(fc)], u + 1.5708 + 0.3 * math.sin(k), (k * 0.37) % 1.0); k += 1
    # a few big ones: tall poles at the corners of the far stand
    for d_ in (30, 80, 130, 150):
        u = math.radians(d_); x, y = ell_pt(ao + 1.5, bo + 1.5, u); flag(x, y, 0.0, 14.0, fc[(d_ // 10) % len(fc)], u + 1.5708, 0.3, 3.4, 2.1, 8)
    fin(mb)
    for cmat, g in cloth.items():
        ob = mesh_from_arrays('flagcloth_' + cmat.name.split('|')[-1], np.array(g['V']), np.array(g['F'], dtype=object).tolist() if False else g['F'], cmat,
                              dict(u=('FLOAT', np.array(g['u'])), dir=('FLOAT_VECTOR', np.array(g['d'])), ph=('FLOAT', np.array(g['ph']))))
        md = ob.modifiers.new('wave', 'NODES'); md.node_group = ng
    return k

# ------------------------------------------------------------------ the set
def build_b(P, M, dress=True):
    rr = rnd(1968); sc = bpy.context.scene
    PR.extra_mats(M, P)
    M['tartan2'] = mat('tartan2', '#d0663f', '#e07a50', 1.8, contrast=0.8)
    M['tartan3'] = mat('tartan3', '#9c3a28', '#b44a32', 1.8, contrast=0.8)
    M['podium'] = mat('podium', '#c8c0d8', '#dad2ea', 2); M['podium2'] = mat('podium2', '#8c9ccc', '#a0b0dc', 2)
    M['board'] = mat('board', '#2a2e52', '#3c4270', 2); M['boardlit'] = mat('boardlit', '#34406e', '#4a5a90', 2, emit='#7080c0', emit_k=0.15)
    M['roofm'] = mat('roofm', '#d8d0dc', '#e8e0ea', 1.4); M['pressglass'] = mat('pressglass', '#34426e', '#4a5c90', 3, emit='#ffd890', emit_k=0.35 if P['floods'] > 0 else 0.0)
    L.sky_world(P); L.ridges(P)
    plane_at(M['lawn'], 900, -0.02, (0, 0), 'lawn')
    mb = S.MB('apron')
    S.ring(mb, M['tartan'], SX, SY, 50, 22, 62, 34, 0, 360, 0.012, 2.0)
    for k in range(9): o = 50 + k * 1.5; S.ring(mb, M['chalk'], SX, SY, o, o - 28, o + 0.07, o - 28 + 0.07, 0, 360, 0.02, 2.0)
    S.ring(mb, M['chalk'], SX, SY, 61.85, 33.85, 62.0, 34.0, 0, 360, 0.022, 2.0)
    S.ring(mb, M['concrete2'], SX, SY, 62, 34, 64, 36, 0, 360, 0.01, 2.0)
    S.disc(mb, M['tartan2'], (0.0, 8.0), 9.0, 0.011, 48, 10.5)                      # infield tartan fan
    # the high-jump FAN: a half disc of lighter tartan on the approach side of the bar, chalk arc, darker apron around the foam pit
    cx_, cy_ = 0.0, BAR_Y_B
    for i in range(36):
        a0 = math.pi * (1.02 + 0.96 * i / 36); a1 = math.pi * (1.02 + 0.96 * (i + 1) / 36)
        mb.tri(M['tartan2'], [(cx_, cy_, 0.016), (cx_ + 12.5 * math.cos(a0) * 1.0, cy_ + 12.5 * math.sin(a0), 0.016), (cx_ + 12.5 * math.cos(a1), cy_ + 12.5 * math.sin(a1), 0.016)])
        mb.quad(M['chalk'], [(cx_ + 12.5 * math.cos(a0), cy_ + 12.5 * math.sin(a0), 0.02), (cx_ + 12.7 * math.cos(a0), cy_ + 12.7 * math.sin(a0), 0.02), (cx_ + 12.7 * math.cos(a1), cy_ + 12.7 * math.sin(a1), 0.02), (cx_ + 12.5 * math.cos(a1), cy_ + 12.5 * math.sin(a1), 0.02)])
    mb.box(M['tartan3'], (0.0, 15.0, 0.014), (9.2, 8.4, 0.006)); mb.box(M['chalk'], (0.0, BAR_Y_B, 0.021), (5.0, 0.07, 0.004))
    for sx in (-1, 1): mb.box(M['chalk'], (sx * 3.7, 8.6, 0.021), (0.07, 5.6, 0.004))
    fin(mb, cast=False)
    # --- stands: treads, risers, rim wall, aisle steps, handrails, vomitories
    mb = S.MB('stands'); steps = 2.0
    for i in range(NROW):
        a = A0 + i * RW; b = B0 + i * RW; z = 1.0 + i * RISE
        S.ring(mb, M['concrete'] if i % 2 == 0 else M['concrete2'], SX, SY, a, b, a + RW, b + RW, 0, 360, z, steps)
        for j in range(int(360 / steps)):
            u0 = math.radians(j * steps); u1 = math.radians((j + 1) * steps); p0 = ell_pt(a, b, u0); p1 = ell_pt(a, b, u1)
            mb.quad(M['concrete2'] if i % 2 == 0 else M['concrete'], [(p0[0], p0[1], z - RISE), (p1[0], p1[1], z - RISE), (p1[0], p1[1], z), (p0[0], p0[1], z)])
    ao = A0 + NROW * RW; bo = B0 + NROW * RW; zt = 1.0 + NROW * RISE
    for j in range(360 // 2):
        u0 = math.radians(j * 2); u1 = math.radians(j * 2 + 2); p0 = ell_pt(ao, bo, u0); p1 = ell_pt(ao, bo, u1)
        mb.quad(M['concrete'], [(p0[0], p0[1], -1), (p1[0], p1[1], -1), (p1[0], p1[1], zt + 1.0), (p0[0], p0[1], zt + 1.0)])
        p0 = ell_pt(A0 - 0.5, B0 - 0.5, u0); p1 = ell_pt(A0 - 0.5, B0 - 0.5, u1)
        mb.quad(M['rust'], [(p0[0], p0[1], 0), (p1[0], p1[1], 0), (p1[0], p1[1], 1.0), (p0[0], p0[1], 1.0)])
    # aisle stairs (light strips) every ~14 deg and a rail along them; barrier hoardings coloured blocks in front of row 0
    for d_ in range(7, 360, 14):
        u = math.radians(d_)
        for i in range(NROW):
            a = A0 + i * RW + 0.2; b = B0 + i * RW + 0.2; z = 1.0 + i * RISE; p0 = ell_pt(a, b, u); p1 = ell_pt(a + RW - 0.4, b + RW - 0.4, u)
            mb.box(M['trim'], ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, z + 0.02), (0.85, 0.7, 0.04), rz=math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
        for sgn in (-1, 1):
            q0 = ell_pt(A0 + 0.1, B0 + 0.1, u + sgn * 0.008); q1 = ell_pt(ao - 0.2, bo - 0.2, u + sgn * 0.008)
            mb.rod(M['metal'], (q0[0], q0[1], 1.9), (q1[0], q1[1], zt + 0.9), 0.025, 0.025, 4)
    hc = ['orange', 'cream', 'blue', 'red', 'yellow', 'teal']
    for k, d_ in enumerate(range(1, 360, 3)):
        u = math.radians(d_); x, y = ell_pt(A0 - 1.2, B0 - 1.2, u); nn = math.atan2(math.sin(u) / (B0 - 1.2), math.cos(u) / (A0 - 1.2))
        mb.box(M[hc[k % 6]], (x, y, 0.55), (0.14, 3.0, 1.1), rz=nn)
    fin(mb)
    # --- press box + roof section on the far side (the camera side faces +y): roof slab with columns, glass band, TV platform
    mb = S.MB('press')
    for d_ in (74, 106):
        pass
    for (dd0, dd1) in [(58, 122)]:
        zr = 1.0 + 20 * RISE
        for d_ in range(dd0, dd1, 4):
            u0 = math.radians(d_); u1 = math.radians(d_ + 4); a0 = A0 + 19 * RW; b0 = B0 + 19 * RW; aE = ao + 3.0; bE = bo + 3.0
            p0 = ell_pt(a0, b0, u0); p1 = ell_pt(a0, b0, u1); q0 = ell_pt(aE, bE, u0); q1 = ell_pt(aE, bE, u1)
            mb.quad(M['roofm'], [(p0[0], p0[1], zr + 6.2), (p1[0], p1[1], zr + 6.2), (q1[0], q1[1], zr + 6.7), (q0[0], q0[1], zr + 6.7)])
            mb.quad(M['concrete2'], [(q0[0], q0[1], zr + 6.7), (q1[0], q1[1], zr + 6.7), (p1[0], p1[1], zr + 6.2), (p0[0], p0[1], zr + 6.2)])
            mb.box(M['dark'], ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, zr + 6.0), (math.hypot(p1[0] - p0[0], p1[1] - p0[1]) + 0.1, 0.25, 0.35), rz=math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
        for d_ in range(dd0, dd1 + 1, 8):
            u = math.radians(d_); p = ell_pt(A0 + 19 * RW + 0.4, B0 + 19 * RW + 0.4, u); mb.rod(M['steel'], (p[0], p[1], 1.0 + 19 * RISE), (p[0], p[1], zr + 6.0), 0.18, 0.18, 8)
        # press box: glazed band along rows 16-19, below the roof
        for d_ in range(dd0 + 4, dd1 - 4, 3):
            u0 = math.radians(d_); u1 = math.radians(d_ + 3); a_ = A0 + 20 * RW; b_ = B0 + 20 * RW; p0 = ell_pt(a_, b_, u0); p1 = ell_pt(a_, b_, u1)
            zc = 1.0 + 20 * RISE + 1.4; nn = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
            mb.box(M['pressglass'], ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, zc), (math.hypot(p1[0] - p0[0], p1[1] - p0[1]) + 0.05, 0.2, 1.6), rz=nn)
            mb.box(M['trim'], ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, zc + 0.9), (math.hypot(p1[0] - p0[0], p1[1] - p0[1]) + 0.05, 0.26, 0.12), rz=nn)
    # blank scoreboard (no digits) on legs above the far rim
    u = math.radians(78); bx, by = ell_pt(ao + 1.0, bo + 1.0, u)
    mb.push(Matrix.Translation((bx, by, zt + 5.0)) @ Euler((0, 0, math.atan2(-math.sin(u) / bo, -math.cos(u) / ao) + math.pi / 2)).to_matrix().to_4x4())
    mb.box(M['steel'], (0, 0, 0), (16.5, 0.6, 7.0)); mb.box(M['board'], (0, -0.35, 0.0), (15.8, 0.15, 6.3))
    for ix in range(3): mb.box(M['boardlit'], (-5.0 + ix * 5.0, -0.45, 0.4), (4.4, 0.08, 3.4))
    mb.box(M['boardlit'], (0, -0.45, -2.4), (14.0, 0.08, 0.8)); mb.rod(M['steel'], (-7.5, 0, -3.5), (-7.5, 0, -zt - 4.0), 0.25, 0.25, 8); mb.rod(M['steel'], (7.5, 0, -3.5), (7.5, 0, -zt - 4.0), 0.25, 0.25, 8)
    mb.pop()
    fin(mb)
    # --- crowd + flags
    nc = build_crowd(P, M, rr); nf = build_flags(P, M, rr); print('crowd figures', nc, 'flags', nf)
    # --- cauldron tower with an animated flame
    cu = math.radians(P['cauldron_t']); cxp, cyp = ell_pt(ao - 2.5, bo - 2.5, cu)
    mb = S.MB('cauldron')
    mb.box(M['concrete'], (cxp, cyp, zt / 2 + 3.5), (5.0, 5.0, zt + 7)); mb.box(M['concrete2'], (cxp, cyp, zt + 7.3), (5.8, 5.8, 0.6))
    mb.rod(M['steel'], (cxp, cyp, zt + 7.6), (cxp, cyp, zt + 9.0), 1.0, 0.8, 14); mb.cone(M['steel'], (cxp, cyp, zt + 9.0), 1.0, 2.6, 1.5, 18); mb.rod(M['rust'], (cxp, cyp, zt + 10.45), (cxp, cyp, zt + 10.6), 2.7, 2.7, 18)
    for i in range(14):
        a = i / 14 * 6.283; mb.ell(M['ember'], (cxp + math.cos(a) * 1.9, cyp + math.sin(a) * 1.9, zt + 10.6), (0.12, 0.12, 0.08), (6, 4))
    fin(mb)
    fctl = ctl_empty('FLAME_CTL', (1.0, 0.0, 0.0)); STATE['flame_ctl'] = fctl; flames = []
    for nm, mt, r0, hh, dx, ph in (('flameA', M['flame'], 2.0, 4.5, 0.0, 0.0), ('flameB', M['flame2'], 1.2, 3.2, 0.0, 1.3), ('flameC', M['flame'], 0.9, 3.7, 0.8, 2.6), ('flameD', M['flame'], 0.9, 3.2, -0.7, 4.0)):
        mb = S.MB(nm); mb.cone(mt, (0, 0, 0), r0, 0.1, hh, 12)
        for o in mb.finish():
            adopt([o]); o.location = (cxp + dx, cyp, zt + 10.5); o.visible_shadow = False; flames.append((o, ph))
    STATE['flames'] = flames; STATE['torch_pos'] = (cxp, cyp, zt + 12.0)
    for o, ph in flames:
        for ch, (f1, f2, a1, a2) in zip((0, 1, 2), ((1.9, 3.7, 0.07, 0.04), (2.3, 4.1, 0.07, 0.04), (1.7, 4.9, 0.20, 0.10))):
            fcv = o.driver_add('scale', ch).driver; fcv.type = 'SCRIPTED'
            v = fcv.variables.new(); v.name = 'a'; v.type = 'TRANSFORMS'; v.targets[0].id = fctl; v.targets[0].transform_type = 'LOC_X'; v.targets[0].transform_space = 'WORLD_SPACE'
            fcv.expression = '1 + a*(%g*sin(frame*%g+%g) + %g*sin(frame*%g+%g))' % (a1, f1, ph, a2, f2, ph * 1.7 + 0.5)
        fcv = o.driver_add('rotation_euler', 2).driver; fcv.type = 'SCRIPTED'
        v = fcv.variables.new(); v.name = 'a'; v.type = 'TRANSFORMS'; v.targets[0].id = fctl; v.targets[0].transform_type = 'LOC_X'; v.targets[0].transform_space = 'WORLD_SPACE'
        fcv.expression = 'a*0.12*sin(frame*1.3+%g)' % ph
    tl = bpy.data.lights.new('torch', 'POINT'); tl.color = (1.0, 0.62, 0.3); tl.energy = 60000.0; tl.shadow_soft_size = 1.5; tl.use_shadow = False
    to = bpy.data.objects.new('torch', tl); STATE['LIGHTS'].objects.link(to); to.location = (cxp * L.U * 0 + cxp, cyp, zt + 12.0); to.parent = root(); STATE['torch_light'] = to
    fcv = tl.driver_add('energy').driver; fcv.type = 'SCRIPTED'
    v = fcv.variables.new(); v.name = 'a'; v.type = 'TRANSFORMS'; v.targets[0].id = fctl; v.targets[0].transform_type = 'LOC_X'; v.targets[0].transform_space = 'WORLD_SPACE'
    fcv.expression = '60000*a*(1 + 0.12*sin(frame*1.9) + 0.07*sin(frame*4.3))'
    # --- floodlight towers (lit lamp panels) + shadow-less pool spots aimed at the jump area
    mb = S.MB('flood')
    for tdeg in P['towers']:
        u = math.radians(tdeg); x, y = ell_pt(ao + 9, bo + 9, u); H_ = 38.0
        n_ = (math.cos(u) / ao, math.sin(u) / bo); nn = math.hypot(*n_); nx, ny = n_[0] / nn, n_[1] / nn
        for sx, sy in ((-0.7, -0.7), (0.7, -0.7), (-0.7, 0.7), (0.7, 0.7)): mb.rod(M['steel'], (x + sx * 1.3, y + sy * 1.3, 0), (x + sx * 0.5, y + sy * 0.5, H_), 0.16, 0.1, 6)
        for hz in range(3, 38, 6): mb.rod(M['steel'], (x - 0.9, y - 0.9, hz), (x + 0.8, y + 0.8, hz), 0.05, 0.05, 4)
        yaw = math.atan2(-ny, -nx)
        mb.push(Matrix.Translation((x, y, H_ + 2.0)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
        mb.box(M['dark'], (0, 0, 0), (0.5, 9.0, 5.6))
        for iy in range(7):
            for iz in range(4): mb.box(M['lamp'], (0.3, -3.9 + iy * 1.3, -2.1 + iz * 1.4), (0.12, 1.0, 1.0))
        mb.pop()
        if P['floods'] > 0:
            sp = bpy.data.lights.new('flood%d' % tdeg, 'SPOT'); sp.color = (1.0, 0.9, 0.72); sp.energy = 3.2e6 * P['floods'] / 4.0; sp.spot_size = math.radians(34); sp.spot_blend = 0.35; sp.use_shadow = False; sp.shadow_soft_size = 1.0
            so = bpy.data.objects.new('flood%d' % tdeg, sp); STATE['LIGHTS'].objects.link(so); so.parent = root(); so.location = (x, y, H_ + 2.0)
            tgt = Vector((0.0 + 3 * math.cos(u), 12.0, 0.0)); so.rotation_euler = (tgt - Vector((x, y, H_ + 2.0))).to_track_quat('-Z', 'Y').to_euler(); STATE.setdefault('flood_lights', []).append(so)
    fin(mb)
    # --- jump set: foam pit (stacked blue-grey blocks) + steel standards + striped bar; NO hurdles in the jump area
    mb = S.MB('foam'); px, py = PIT_B
    for lay, (z0, z1) in enumerate([(0.0, 0.32), (0.32, 0.64), (0.64, 0.92)]):
        ox = (0.0, 0.4, -0.3)[lay]
        for gx_ in range(4):
            for gy_ in range(3):
                x0 = px - 3.2 + gx_ * 1.6 + 0.01; y0 = py - 2.7 + gy_ * 1.8 + 0.01
                mb.box(M['foam'] if (gx_ + gy_ + lay) % 2 == 0 else M['foamdk'], (x0 + 0.79, y0 + 0.89, (z0 + z1) / 2), (1.58, 1.78, z1 - z0 - 0.01))
    mb.box(M['foamtop'], (px, py, FOAM_TOP - 0.04), (6.3, 5.3, 0.16)); mb.box(M['foam'], (px, py - 2.65, FOAM_TOP - 0.1), (6.4, 0.12, 0.3)); mb.box(M['foam'], (px, py + 2.65, FOAM_TOP - 0.1), (6.4, 0.12, 0.3))
    for sx in (-3.15, 3.15): mb.box(M['foam'], (px + sx, py, FOAM_TOP - 0.1), (0.12, 5.4, 0.3))
    for sx in (-1.5, 0.0, 1.5): mb.box(M['foamdk'], (px + sx, py, FOAM_TOP + 0.045), (0.05, 5.3, 0.012))
    mb.box(M['foamdk'], (px, py - 1.5, FOAM_TOP + 0.045), (6.3, 0.05, 0.012)); mb.box(M['foamdk'], (px, py + 1.0, FOAM_TOP + 0.045), (6.3, 0.05, 0.012))
    fin(mb)
    J = LA.jump_set(M, 0.0, BAR_Y_B, 2.1, 'steel', 2.95, FOAM_TOP, 'B', 2.24); STATE['J'] = J
    # --- officials' table (clipboard, small flag), chairs, measuring stick, kit
    mb = S.MB('officials'); tx, ty = 9.0, 5.0
    mb.push(Matrix.Translation((tx, ty, 0)) @ Euler((0, 0, 0.5)).to_matrix().to_4x4())
    mb.box(M['woodpale'], (0, 0, 0.74), (2.4, 0.9, 0.06)); mb.box(M['cloth'], (0, -0.3, 0.55), (2.45, 0.02, 0.45)); mb.box(M['cloth'], (0, 0.0, 0.78), (2.2, 0.8, 0.012))
    for sx in (-1.1, 1.1):
        for sy in (-0.38, 0.38): mb.rod(M['wood'], (sx, sy, 0), (sx, sy, 0.72), 0.03, 0.03, 6)
    mb.rod(M['metal'], (0.6, 0.1, 0.78), (0.6, 0.1, 1.3), 0.012, 0.012, 5); mb.tri(M['red'], [(0.6, 0.1, 1.3), (0.6, 0.1, 1.1), (1.0, 0.1, 1.2)]); mb.tri(M['cream'], [(0.6, 0.1, 1.2), (0.6, 0.1, 1.1), (1.0, 0.1, 1.2)])
    mb.box(M['wood'], (-0.3, 0.1, 0.81), (0.3, 0.22, 0.012)); mb.box(M['paper'], (-0.3, 0.1, 0.82), (0.26, 0.19, 0.004)); mb.box(M['metal'], (-0.3, 0.2, 0.825), (0.1, 0.03, 0.01))
    mb.box(M['dark'], (-0.9, 0.0, 0.8), (0.12, 0.12, 0.05)); mb.rod(M['yellow'], (0.1, 0.2, 0.8), (0.3, 0.2, 0.8), 0.01, 0.01, 4); mb.box(M['yellow'], (0.9, -0.15, 0.82), (0.25, 0.08, 0.04))
    mb.pop()
    for (dx, dy, yw) in [(-0.9, 1.0, 3.6), (0.0, 1.2, 3.7), (0.9, 1.1, 3.55)]:
        c = Vector((tx, ty)) + Vector((dx * math.cos(0.5) - dy * math.sin(0.5), dx * math.sin(0.5) + dy * math.cos(0.5))); S.chair(mb, M, (c.x, c.y, 0), yw)
    mb.rod(M['wood'], (5.5, 9.5, 0), (5.5, 9.5, 2.6), 0.02, 0.02, 5); mb.box(M['yellow'], (5.5, 9.5, 2.3), (0.04, 0.04, 0.5))
    S.bag(mb, M, (-5.5, 7.0, 0.0), 0.8, 'red', 0.9); S.bag(mb, M, (-4.8, 7.8, 0.0), 0.3, 'navy', 0.7); S.bag(mb, M, (6.0, 12.5, 0.0), 1.3, 'teal', 0.8)
    for (x, y, yw, mt) in [(-5.0, 6.2, 0.4, 'orange'), (6.8, 7.6, 2.0, 'cream'), (-6.2, 9.3, 1.1, 'blue')]: S.jacket(mb, M, (x, y, 0.0), yw, mt, 1.3)
    for (x, y) in [(-7.3, 3.0), (-6.3, 2.6), (7.6, 9.0), (-3.4, 11.5)]: S.bottle(mb, M, (x, y, 0.0), 'yellow')
    for (x, y) in [(-3.6, 9.4), (3.8, 9.6), (-4.2, 21.5), (4.6, 20.8)]: S.cone_t(mb, M, (x, y, 0.0))
    S.tape_reel(mb, M, (-1.8, 9.2, 0.0), 0.3); S.rake(mb, M, (3.6, 18.3, 0.0), (3.2, 18.0, 0.95)); S.wheelbarrow(mb, M, (-7.5, 14.0, 0.0), 0.4)
    # bar-carrier rack: two spare bars leaning, coaches' benches, a second table for the scorers
    mb.box(M['woodpale'], (-8.2, 9.8, 0.4), (0.5, 1.6, 0.04)); PR.clipboard(mb, M, (-8.2, 9.6, 0.5), 0.2, -1.3)
    fin(mb)
    # --- podium (3 steps, plain, no numbers): shot 31, left of the pit, facing the camera side (-y)
    mb = S.MB('podium'); pxp, pyp = -9.0, 10.0
    for (dx, hh, wd, mt) in [(-0.95, 0.55, 0.9, 'podium'), (0.0, 0.85, 1.0, 'podium'), (0.95, 0.35, 0.9, 'podium')]:
        mb.box(M[mt], (pxp + dx, pyp, hh / 2), (wd, 0.9, hh)); mb.box(M['podium2'], (pxp + dx, pyp - 0.455, hh / 2), (wd, 0.02, hh - 0.04)); mb.box(M['cream'], (pxp + dx, pyp, hh + 0.01), (wd, 0.9, 0.025))
    fin(mb)
    # --- photographers' area: low platform with tripods and cameras along the inner kerb, plus bags
    mb = S.MB('photo')
    mb.box(M['woodgrey'], (-12.0, 20.0, 0.1), (6.0, 2.2, 0.2)); mb.box(M['woodgrey'], (13.0, 23.0, 0.1), (5.0, 2.2, 0.2))
    for (x, y) in [(-14.0, 20.0), (-12.0, 20.3), (-10.0, 19.8), (11.0, 23.0), (13.2, 23.3), (15.0, 22.8), (-22.0, 24.0), (28.0, 26.0), (6.0, 8.2)]:
        z0 = 0.2 if abs(x) < 16 and y > 19 else 0.0
        for a in (0, 2.1, 4.2): mb.rod(M['metal'], (x, y, z0 + 1.4), (x + math.cos(a) * 0.5, y + math.sin(a) * 0.5, z0), 0.015, 0.015, 4)
        mb.box(M['dark'], (x, y, z0 + 1.5), (0.35, 0.2, 0.2)); mb.rod(M['steel'], (x + 0.2, y, z0 + 1.5), (x + 0.55, y, z0 + 1.5), 0.06, 0.08, 8)
        PR.photographer_bag(mb, M, (x + 0.7, y - 0.4, z0), rr.random() * 6)
    fin(mb)
    mb = S.MB('kit')
    for i in range(26):
        u = math.radians(rr.uniform(10, 170)); x, y = ell_pt(49.2, 21.2, u)
        mt = rr.choice(['blue', 'red', 'orange', 'cream', 'green', 'yellow', 'navy'])
        if rr.random() < 0.6: S.bag(mb, M, (x, y, 0), rr.random() * 6, mt, rr.uniform(0.5, 0.9))
        else: S.chair(mb, M, (x, y, 0), rr.random() * 6)
    fin(mb)
    # --- stadium flash bulbs in the stands (hidden until flashed)
    mb = S.MB('bulbs'); fm = mat_emit('bulb', '#fffbe8', 80.0); bulbs = []
    for i in range(60):
        i_ = rr.randrange(6, NROW - 2); a = A0 + i_ * RW + 0.5; b = B0 + i_ * RW + 0.5; t = math.radians(rr.uniform(15, 165)); x, y = ell_pt(a, b, t); z = 1.0 + i_ * RISE + 0.95
        o = S.MB('bulb%d' % i); o.ell(fm, (0, 0, 0), (0.17, 0.17, 0.17), (6, 4)); ob = adopt(o.finish(), cast=False)[0]; ob.location = (x, y, z); ob.hide_render = True; bulbs.append(ob)
    STATE['stand_bulbs'] = bulbs
    # --- jump-area stand points (metres)
    cs = ell_pt(A0 + 7 * RW + 0.55 + 0.4, B0 + 7 * RW + 0.55 + 0.4, math.radians(97)); COACH_SEAT = (cs[0], cs[1], 1.0 + 7 * RISE)
    path = [(8.0, 2.0), (7.4, 5.0), (6.0, 7.6), (4.2, 9.4), (2.5, 10.3)]
    MARKS_B.update(runup_path=[(x, y, 0.0) for x, y in path], runup_start=(8.0, 2.0, 0.0), takeoff=(1.15, 10.6, 0.0), bar_centre=(0.0, BAR_Y_B, 2.24), landing=(0.0, 14.5, FOAM_TOP), dick_mark=(5.8, 8.2, 0.0),
                   coach_stands=COACH_SEAT, podium_top=(-9.0, 10.0, 0.85), podium_2=(-9.95, 10.0, 0.55), podium_3=(-8.05, 10.0, 0.35),
                   photographer=(-12.0, 20.0, 0.2), photographer_b=(13.0, 23.0, 0.2), official_a=(8.0, 6.2, 0.0), official_b=(10.0, 6.4, 0.0), official_bar_l=(-2.9, 10.6, 0.0), official_bar_r=(2.9, 10.6, 0.0),
                   dick_b2=(-2.7, 9.3, 0.0), rival_a=(4.9, 7.2, 0.0), rival_b=(2.2, 9.6, 0.0), rival_land=(0.5, 13.8, FOAM_TOP), table=(9.0, 5.0, 0.0), torch=STATE['torch_pos'], foam_edge=(0.0, 12.3, FOAM_TOP))
    STATE['marks_m'] = dict(MARKS_B)

#!/usr/bin/env python3
"""shot.py -- film 21 segment J2 (ending splash), g 1709..1848, ONE travelling camera (cam_path), no handles, hard cut at 1848.
whip in (6 frames), the English look at the bridge / water / each other (nose pinch), jump 59.0-59.8 (g 1773-1792), crowns, swimmers, helmets,
the camera drops to river_low and pushes in for three big crowns at the words 1821 / 1830 / 1839.
    python3 shot.py <draft|final> a:b[:step] [out_dir] [samples]
"""
import sys, os, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c21
from c21 import *

G0, G1 = 1709, 1848
CUT29, CUT30 = 1709, 1769
HT = K.HEIGHT
# head-top-to-soles in head diameters (cast21 API) -> world scale of a card
HD = dict(cressingham=3.23, surrey=3.20, knight_a=3.26, knight_a_open=3.26, knight_b=3.38, knight_b_great=3.38, footman_a=3.04, footman_b=3.24)
HK = dict(cressingham="cressingham", surrey="surrey", knight_a="knight", knight_a_open="knight", knight_b="knight", knight_b_great="knight", footman_a="foot", footman_b="foot")
S = cast21.STORY21


def wscale(cast):
    base = cast.split("_v")[0]
    if base not in HD: base = "footman_a"
    return HT[HK[base]] / HD[base]


def pose_of(name, **kw):
    cast, p = S[name]
    p = dict(p); p.update(kw)
    return p


def aim_pitch(loc, look, dpitch=0.0):
    """look point after changing the pitch of the loc->look ray by dpitch degrees"""
    v = Vector(look) - Vector(loc); h = math.hypot(v.x, v.y); pit = math.atan2(v.z, h) + math.radians(dpitch)
    n = Vector((v.x, v.y, 0)).normalized()
    return Vector((loc[0] + n.x * 30 * math.cos(pit), loc[1] + n.y * 30 * math.cos(pit), loc[2] + 30 * math.sin(pit)))


def right_vec(loc, look):
    az = math.atan2(look[1] - loc[1], look[0] - loc[0]); return Vector((math.sin(az), -math.cos(az), 0))


def fwd_vec(loc, look):
    v = Vector(look) - Vector(loc); v.z = 0; return v.normalized()


class Rig(object):
    """one staged English actor: a timeline of (position, pose) over g"""
    def __init__(self, T, name, cast, xy, **kw):
        self.T, self.name, self.cast, self.xy = T, name, cast, Vector(xy)
        self.scale = wscale(cast)
        self.a = T.add(name, cast)
        self.kw = kw


def ground_z(x, y):
    return float(K.ground(x, y))


def entry_point(x, y, rvec, depth=1.6):
    """march from (x, y) along rvec (toward the water) to where sd < -depth"""
    e = 0.5
    gx = (K.sd_at(x + e, y) - K.sd_at(x - e, y)); gy = (K.sd_at(x, y + e) - K.sd_at(x, y - e))
    n = math.hypot(gx, gy) or 1.0
    rvec = Vector((-gx / n, -gy / n, 0.0)) * 0.8 + rvec * 0.2
    for i in range(0, 200):
        t = i * 0.1
        px, py = x + rvec.x * t, y + rvec.y * t
        if K.sd_at(px, py) < -depth:
            return px, py
    return x + rvec.x * 6, y + rvec.y * 6



# ----------------------------------------------------------------------------- camera
def smoothstep(u): return sine(u)


def quint(u):
    u = clamp(u); return u * u * u * (u * (6 * u - 15) + 10)


class CamPath(object):
    """waypoints [(g, loc, look)] with per-segment easing kind 'sine' | 'lin' | 'snap'"""
    def __init__(self, pts): self.pts = pts

    def at(self, g):
        p = self.pts
        if g <= p[0][0]: return Vector(p[0][1]), Vector(p[0][2])
        for (g0, l0, k0, *kind0), (g1, l1, k1, *kind1) in zip(p[:-1], p[1:]):
            if g <= g1:
                u = (g - g0) / float(g1 - g0); kind = kind1[0] if kind1 else 'sine'
                e = {'sine': 0.35 * sine(u) + 0.65 * u, 'lin': u, 'snap': quint(u)}[kind]
                return Vector(l0).lerp(Vector(l1), e), Vector(k0).lerp(Vector(k1), e)
        return Vector(p[-1][1]), Vector(p[-1][2])


# ----------------------------------------------------------------------------- the actors
class Rig(object):
    def __init__(self, T, name, cast, tl):
        """tl(g) -> dict(pos=(x,y,z), pose=dict, flip=bool, hide=bool, contact=bool)"""
        self.T, self.name, self.cast, self.tl = T, name, cast.split('|')[0], tl
        self.a = T.add(name, self.cast)
        self.scale = wscale(self.cast)
        self.state = {}

    def pose_frames(self, gs):
        T = self.T
        for g in gs:
            f = bf(g); st = self.tl(g); self.state[g] = st
            if st.get('hide'): continue
            self.a.place(f, st['pos'], scale=st.get('scale', self.scale), flip=st.get('flip', False))
            T.scene.frame_set(f)
            self.a.pose(f, K.with_rim(st['pose']), camera=T.cam)

    def hook(self, g):
        st = self.state.get(g)
        hide = (st is None) or st.get('hide')
        for ob in (self.a.card, self.a.proxy):
            if ob is not None: ob.hide_render = bool(hide)
        if self.a.contact is not None: self.a.contact.hide_render = bool(hide or not st.get('contact', True))



def variant(p, v):
    if v: p = dict(p, variant21=v)
    return p


def idle(p, g, k):
    p = dict(p); p['lean'] = p.get('lean', 0) + 1.3 * math.sin(g * 0.11 + k); p['head_roll'] = p.get('head_roll', 0) + 1.8 * math.sin(g * 0.17 + 2 * k)
    p['blink'] = blink(g, 83 + 7 * int(k), int(k * 11)); return p


# ============================================================================= J2 v2 (director fixes)
Y0 = 46.0                                  # centre of the group along the shore (y)
G_WHIP = 1713                              # the whip has landed on the group
G_PH = (1713, 1731, 1747)                  # head turns: bridge -> water -> each other (each >= 0.55 s)
G_PINCH = 1756
JUMPS = dict(B=(1773, "jump_pinch_nose", 0.95, 1.0), A=(1777, "jump_arms_up", 1.1, 1.0), C=(1781, "jump_bomb", 0.85, 1.0),
             D=(1784, "jump_arms_up", 1.0, 0.9), E=(1788, "jump_bomb", 0.9, 0.9), F=(1792, "jump_pinch_nose", 0.8, 0.8))
T_AIR = 14
CROWD = [dict(n="A", cast="footman_a", dy=-3.1, back=0.3, var=0, base="footman_a_stand"),
         dict(n="B", cast="footman_b", dy=-1.7, back=0.9, var=0, base="footman_b_stand"),
         dict(n="C", cast="knight_a_open", dy=-0.3, back=0.2, var=0, base="knight_a_open_stand"),
         dict(n="D", cast="footman_a", dy=1.2, back=0.8, var=2, base="footman_a_stand"),
         dict(n="E", cast="knight_b", dy=2.6, back=0.2, var=0, base="knight_b_stand"),
         dict(n="F", cast="footman_b", dy=4.0, back=0.9, var=1, base="footman_b_stand")]


def shore_x(y):
    """x of the waterline (sd = 0) at y, scanning from the water (west) to the land (east)"""
    x = -45.0
    while x < -5.0:
        if K.sd_at(x, y) > 0: return x
        x += 0.1
    return -25.0


def splash2(x, y, age, size=1.0, name="a", seed=0, z=0.0):
    """thin crown: ~9 petal sheets (tapered quads) + 5 streak rods + 12 small droplets + a thin ring; separate columns that fall back"""
    K._del_prefix('splash_' + name + '_')
    if age < 0 or age > 1.2: return 0
    rs = np.random.RandomState(seed); B = K.Batch(91); k = size
    tau = min(age / 0.7, 1.0); H = k * 1.5 * math.sin(math.pi * tau) ** 0.7 if age < 0.7 else 0.0
    R0 = k * (0.18 + 0.35 * tau); M = 'glow_spray'; M2 = 'glow_spray2'
    if H > 0.08:
        n = 9
        for i in range(n):
            a = 2 * math.pi * (i + rs.uniform(-0.2, 0.2)) / n; hh = H * rs.uniform(0.65, 1.1); fl = math.radians(rs.uniform(25, 40)); w = 0.34 * k
            tx, ty = -math.sin(a), math.cos(a); rx, ry = math.cos(a), math.sin(a)
            b = (x + R0 * rx, y + R0 * ry, z); tp = (x + (R0 + hh * math.tan(fl)) * rx, y + (R0 + hh * math.tan(fl)) * ry, z + hh)
            B.mesh(M, [(b[0] - tx * w, b[1] - ty * w, b[2]), (b[0] + tx * w, b[1] + ty * w, b[2]), (tp[0] + tx * 0.02, tp[1] + ty * 0.02, tp[2]), (tp[0] - tx * 0.02, tp[1] - ty * 0.02, tp[2])], [(0, 1, 2, 3)], False)
        for i in range(5):
            a = rs.uniform(0, 6.28); hh = H * rs.uniform(0.9, 1.4)
            B.rod(M, (x + 0.1 * math.cos(a) * k, y + 0.1 * math.sin(a) * k, z), (x + 0.25 * math.cos(a) * k, y + 0.25 * math.sin(a) * k, z + hh), 0.035 * k, seg=4, r2=0.006 * k)
    ro = R0 * 1.5 + k * 0.5 * tau; wd = max(0.02, 0.12 * k * (1 - age / 1.2)); n = 24; th = [2 * math.pi * i / n for i in range(n)]
    B.mesh(M2, [(x + (ro - wd) * math.cos(t_), y + (ro - wd) * math.sin(t_), z + 0.05) for t_ in th] + [(x + ro * math.cos(t_), y + ro * math.sin(t_), z + 0.05) for t_ in th],
           [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)], False)
    for i in range(12):
        a = rs.uniform(0, 2 * math.pi); vh = rs.uniform(0.8, 2.2) * math.sqrt(k); vz = rs.uniform(2.4, 4.6) * math.sqrt(k)
        px, py, pz = x + vh * math.cos(a) * age, y + vh * math.sin(a) * age, z + 0.15 + vz * age - 4.9 * age * age
        if pz > z + 0.03 and age > 0.02: B.sphere(M, (px, py, pz), rs.uniform(0.035, 0.06) * k, seg=4, rings=3)
    return len(B.finalize('splash_' + name + '_', ink=False, shadow=False))


def snap_to_shore(x, y, target=0.9):
    for _ in range(60):
        sd = K.sd_at(x, y)
        if abs(sd - target) < 0.15: break
        e = 0.5
        gx = K.sd_at(x + e, y) - K.sd_at(x - e, y); gy = K.sd_at(x, y + e) - K.sd_at(x, y - e); n = math.hypot(gx, gy) or 1.0
        st = (sd - target) * 0.7
        x -= gx / n * st; y -= gy / n * st
    return x, y


CL = {}
SPOTS = [(3.6, 400), (4.7, 540), (5.8, 330), (7.2, 570), (8.6, 440), (10.2, 640)]


def build_state(T, gs):
    pr = K.PRESETS['riverbank']
    for p_ in ('riverbank', 'river_low'):
        for i in range(3): K.splash(0, 0, -1, name='%s%d' % (p_, i))
    c21.hide_prefix('fg_generic_g'); c21.hide_prefix('veg_reed'); c21.hide_prefix('smoke_col')
    K.spear_wall(14, 2, np.random.RandomState(4))
    c21.hide_prefix('meadow_trees'); c21.hide_prefix('farms_leaf'); c21.hide_prefix('farms_bark')                                  # the dark tree that stood in front of the wall
    rs_ = np.random.RandomState(5); Bq = K.Batch(88)
    for sx in (-11.0, 11.0): K.banner(Bq, (sx, 26.8, float(K.ground(sx, 26.8))), 9.0, 190, 't_saltire', 't_white', 'saltire', rs_, size=(4.2, 2.9))
    Bq.finalize('wall_banners_big')
    ld = bpy.data.lights.new('wall_fill', 'POINT'); ld.energy = 30000.0; ld.shadow_soft_size = 3.0; ld.color = (1.0, 0.9, 0.7)
    lo = bpy.data.objects.new('wall_fill', ld); bpy.context.scene.collection.objects.link(lo); lo.location = (-8.0, 40.0, 9.0)   # lights the wall's north face                   # the blue Scots spear wall + saltire banners at the bridge neck
    C0 = Vector((-27.0, 54.0, float(K.ground(-27.0, 54.0)) + 1.8)); L0 = aim_pitch(C0, Vector(pr['look']), -4.5)
    base = L0 - C0
    def yawed(d, deg, up=0.0):
        c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
        return Vector((d.x * c + d.y * s, -d.x * s + d.y * c, d.z + up * d.length))
    Fv, Rv = fwd_vec(C0, L0), right_vec(C0, L0)
    dirA = yawed(base, -27.0)                       # looks toward the bridge neck: wall + saltires at the left, group right of centre
    dirB = yawed(base, 0.0)
    # stand points relative to camera direction A
    lookA = C0 + dirA
    rigs = {}; ents = {}
    for k, c in enumerate(CROWD):
        d, xp = SPOTS[k]
        x, y = K.rel_xy(C0, lookA, d, (xp - 360.0) / 440.0 * d)
        x, y = snap_to_shore(x, y, 0.8 + 0.3 * (k % 2))
        p0 = Vector((x, y, ground_z(x, y)))
        ent = Vector(entry_point(x, y, Rv, 1.7 + 0.15 * k)).to_3d(); ent.z = 0.0; ents[c['n']] = ent
        bs = variant(pose_of(c['base']), c['var'])
        def tl(g, n=c['n'], k=k, p0=p0, ent=ent, bs=bs, c=c):
            return state_of(g, n, k, p0, ent, bs, c)
        rigs[c['n']] = Rig(T, c['n'], c['cast'], tl); rigs[c['n']].ent = ent
    # swimmers cluster centre (for the end framing)
    cen = sum((ents[w] for w in ("B", "D", "E")), Vector((0, 0, 0))) / 3.0
    uu = Vector((C0.x - cen.x, C0.y - cen.y, 0)).normalized()
    e_ = 0.5; gx_ = K.sd_at(cen.x + e_, cen.y) - K.sd_at(cen.x - e_, cen.y); gy_ = K.sd_at(cen.x, cen.y + e_) - K.sd_at(cen.x, cen.y - e_); gn_ = math.hypot(gx_, gy_) or 1.0
    w_ = Vector((-gx_ / gn_, -gy_ / gn_, 0))                          # toward open water
    cen = cen + w_ * 2.4; cen.z = 0.0                               # the cluster floats well out in open water (no bank between lens and swimmers)
    t_ = Vector((-w_.y, w_.x, 0))
    if t_.y > 0: t_ = -t_                                             # camera stands south of the swimmers, along the shore, over the water
    loc3 = Vector((cen.x, cen.y, 0.6)) + t_ * 3.0 + w_ * 1.0
    for _i in range(10):
        if K.sd_at(loc3.x, loc3.y) < -0.4: break
        loc3 = loc3 + w_ * 0.4
    print('DBG cen', tuple(round(v,1) for v in cen), 'uu', tuple(round(v,2) for v in uu), 'loc3', tuple(round(v,1) for v in loc3), 'sd', round(K.sd_at(loc3.x, loc3.y),2), 'sdcen', round(K.sd_at(cen.x,cen.y),2), flush=True)
    Fw = Vector((cen.x - loc3.x, cen.y - loc3.y, 0)).normalized(); Lat = Vector((Fw.y, -Fw.x, 0))   # camera forward / right at the end framing
    for w_, o_ in (("B", -0.8), ("D", 0.1), ("E", 0.95)):
        CL[w_] = cen + Lat * o_ + Fw * (0.3 if w_ == "D" else 0.0); CL[w_].z = 0.0
    loc1 = C0 + Rv * 0.5 + Fv * 0.5
    loc2 = C0.lerp(loc3, 0.55) + Vector((0, 0, -0.3))
    def aimc(loc, dz=0.0):
        lk = Vector((cen.x, cen.y, 1.55 + dz)); return lk
    keys = [(1709, tuple(C0), tuple(C0 + dirA), 22.0), (1735, tuple(C0 + Rv * 0.2 + Fv * 0.3), tuple(C0 + Rv * 0.2 + Fv * 0.3 + yawed(base, -8.0)), 22.0),
            (1772, tuple(loc1), tuple(loc1 + dirB), 22.0),
            (1800, tuple(loc2), tuple(aimc(loc2, 0.2)), 22.0), (1821, tuple(loc3), tuple(aimc(loc3, 0.1)), 22.0),
            (1847, tuple(loc3 + Fw * 0.3), tuple(aimc(loc3, 0.0)), 22.0)]
    def cam_g(g):
        r = K.cam_path(None, keys, g, clearance=0.4)
        loc, look = Vector(r['loc']), Vector(r['look'])
        if g < G_WHIP:           # whip in from the wall side: the pan settles on the group by G_WHIP
            u = (g - 1709) / float(G_WHIP - 1709); th = 28.0 * (1.0 - u) ** 2
            d = look - loc; look = loc + yawed(d, th)
        return loc, look, r['lens']
    T.cam_g = lambda g: cam_g(g)[:2]
    for g in gs:
        loc, look, ln = cam_g(g); T.key_cam(bf(g), loc, look, lens=ln)
    for j, off in enumerate((0.6, -2.0)):
        def tlh(g, j=j, off=off):
            if g < 1805 + 4 * j: return dict(hide=True)
            u = g - (1805 + 4 * j)
            q = cen + Lat * off + Fw * (0.5 + 0.3 * j)
            return dict(pos=(q.x + 0.1 * math.sin(u * 0.13), q.y + 0.1 * math.cos(u * 0.1), 0.0),
                        pose=dict(helm21=("kettle", "great")[j], t=(g / 40.0 + 0.3 * j) % 1.0, tilt=12 * math.sin(u * 0.2 + j)), contact=False, scale=wscale("footman_a") * 0.5)
        rigs["H%d" % j] = Rig(T, "H%d" % j, "helmet_float", tlh)
    for r in rigs.values(): r.pose_frames(gs)
    T.sprites_for(128 if T.quality == 'draft' else 256); T.rigs = rigs
    IMP = (1813, 1822, 1836)
    lat = Lat; fw = Fw
    CP = [cen + lat * 1.9 + fw * 0.9, cen - lat * 1.9 + fw * 0.7, cen + lat * 0.2 + fw * 2.2]
    for p in CP: p.z = 0.0

    def on_g(g):
        t = g / 30.0
        K.set_flutter(t); K.set_smoke(t); K.set_flow(t)
        cl = T.cam_g(g)[0]
        for r in rigs.values():
            r.hook(g)
            st = r.state.get(g)
            if st and not st.get('hide') and g >= 1800:
                p_ = st['pos']
                if math.hypot(p_[0] - cl.x, p_[1] - cl.y) < 1.5:
                    for ob in (r.a.card, r.a.proxy): ob.hide_render = True
        for who, (t0, kind, h, sz) in JUMPS.items():
            age = (g - (t0 + T_AIR)) / 30.0 + 0.02
            e = ents[who]; near = math.hypot(e.x - cl.x, e.y - cl.y) < (4.8 if g >= 1790 else 3.0)
            splash2(e.x, e.y, age if (age > 0 and not near) else -1, size=sz, name=who, seed=ord(who))
        for j in range(3):
            a_ = (g - IMP[j]) / 30.0
            splash2(CP[j].x, CP[j].y, a_ if (a_ >= 0 and math.hypot(CP[j].x - cl.x, CP[j].y - cl.y) > 2.2) else -1, size=1.5, name='L%d' % j, seed=j + 3)
    return on_g


def state_of(g, n, k, p0, ent, base, c):
    jt = JUMPS[n]; t0, kind, h, sz = jt; t1 = t0 + T_AIR
    pos = Vector(p0); p = dict(base); flip = bool(k % 2)
    if g < t0 - 4:
        # three clear head turns: bridge (south-east = camera right), water (camera left / lens), each other
        ph = 0 if g < G_PH[1] else (1 if g < G_PH[2] else 2)
        if ph == 0: yaw, gz, fl = -0.9, (-0.9, 0.1), True
        elif ph == 1: yaw, gz, fl = 0.8, (0.9, 0.3), False
        else: yaw, gz, fl = (0.8 if k % 2 == 0 else -0.8), ((0.9 if k % 2 == 0 else -0.9), 0.0), (k % 2 == 1)
        p['yaw'] = yaw; p['gaze'] = gz; p['head_roll'] = (6 if ph == 0 else -5 if ph == 1 else 4) * (1 if k % 2 else -1)
        p['expr'] = 'neutral' if ph == 0 else 'worried'
        if ph > 0: p['mouth'] = 'wavy'; p['fx'] = ['sweat'] if (k + g // 12) % 2 == 0 else []
        p['pitch'] = 0.15 if ph == 1 else 0.0
        if n == "B" and g >= G_PINCH:
            pj = pose_of("footman_b_jump_pinch_nose"); pp = dict(base, **{kk: pj[kk] for kk in ("arm_r", "expr", "mouth", "head_roll")}); pp.pop('prop_r', None); pp['legs'] = 'stand'; p = pp
        return dict(pos=pos, pose=idle(p, g, k), flip=fl, contact=True)
    if g < t0:
        u = (g - (t0 - 4)) / 4.0; p['squash'] = (1.0 + 0.05 * u, 1.0 - 0.1 * u); p['expr'] = 'shouting'
        return dict(pos=pos, pose=p, flip=flip, contact=True)
    if g < t1:
        u = (g - t0) / float(T_AIR)
        x = lerp(p0.x, ent.x, u); y = lerp(p0.y, ent.y, u); z = p0.z * (1 - u) + h * 4 * u * (1 - u) + 0.05 * u
        pj = variant(pose_of(c['cast'] + '_' + kind), c['var']); pj['yaw'] = 0.5
        return dict(pos=(x, y, z), pose=pj, flip=flip, contact=False)
    w = g - t1
    if w < 2: return dict(hide=True)
    s = w - 2
    sw = 1.0 + 0.08 * math.sin(s * 0.5 + k) - 0.35 * max(0, 1 - s / 6.0)
    pn = "swim_splutter" if s < 11 else (("swim_arms_up" if k % 2 == 0 else "swim_bob") if s < 22 else "swim_paddle")
    pp = variant(pose_of(c['cast'] + '_' + pn), c['var']); pp['swim21'] = max(0.45, sw); pp['t'] = (s * 0.07 + k * 0.2) % 1.0
    if s > 6: pp['yaw'] = 0.9; pp['head_roll'] = pp.get('head_roll', 0) + 6
    if n in CL:
        e_ = ez(s / 28.0); tg = CL[n]
        px = lerp(ent.x, tg.x, e_) + 0.05 * math.sin(s * 0.3 + k); py = lerp(ent.y, tg.y, e_) + 0.05 * math.cos(s * 0.4 + k)
    else:
        px = ent.x - 0.25 * s / 30.0 + 0.06 * math.sin(s * 0.3 + k); py = ent.y
    return dict(pos=(px, py, 0.0), pose=pp, flip=False, contact=False)


def make_bank(T, gs): return build_state(T, gs)


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]; out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else: out.append(int(part))
    return out


def main():
    quality, spec = sys.argv[1], sys.argv[2]
    out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "raw")
    samples = int(sys.argv[4]) if len(sys.argv) > 4 else (12 if quality == "draft" else 32)
    gs = [g for g in parse(spec) if G0 <= g <= G1]
    os.makedirs(out, exist_ok=True)
    todo = [g for g in gs if not (quality == "final" and os.path.exists(os.path.join(out, "g_%04d.png" % g)))]
    if not todo: print("nothing to do"); return
    T = c21.Take(["riverbank", "river_low"], quality=quality)
    T.workdir = os.path.join(HERE, "work"); os.makedirs(T.workdir, exist_ok=True)
    on_g = make_bank(T, todo)
    T.render(todo, out, on_g, samples=samples, draft=(quality == "draft"))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""shot.py -- film 21 take s11 (the ENDING), shots 28-31, g 1633 (7 handle frames) .. 1848 (hard cut: no handle after).
    28 camp_table  g 1633..1708  Cressingham's EMPTY money table: the scale tips on "เร็วดี" (g 1677), the chest lid slams on "ประหยัดดี" (g 1690)
    29 riverbank   g 1709..1768  the English look at the bridge, at the water, at each other; one pinches his nose
    30 riverbank   g 1769..1820  they jump into the Forth (card lift, splash crowns), come up spluttering, swim, helmets float
    31 river_low   g 1821..1848  "ตูม ตูม ตูม": three big crowns on 1821 / 1830 / 1839; quick push; the take ends on the last splash
One process per preset:   python3 shot.py <camp|bank|low> <draft|final> a:b[:step] [out_dir] [samples]
"""
import sys, os, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c21
from c21 import *

G0, G1 = 1633, 1848
CUT29, CUT30, CUT31 = 1709, 1769, 1821
RANGES = {"camp": (1633, 1708), "bank": (1709, 1820), "low": (1821, 1848)}
PRESET = {"camp": "camp_table", "bank": "riverbank", "low": "river_low"}
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
            self.a.pose(f, st['pose'], camera=T.cam)

    def hook(self, g):
        st = self.state.get(g)
        hide = (st is None) or st.get('hide')
        for ob in (self.a.card, self.a.proxy):
            if ob is not None: ob.hide_render = bool(hide)
        if self.a.contact is not None: self.a.contact.hide_render = bool(hide or not st.get('contact', True))


# ============================================================================= BANK (shots 29 + 30)
def stage_xy(pr, d, xp):
    x, y = K.at_px(pr, d, xp); return Vector((float(x), float(y), ground_z(x, y)))


CROWD = [  # name, cast, (d, px) stand point seen from the preset camera, variant, role
    dict(n="A", cast="footman_a", d=3.3, xp=120, base="footman_a_stand", var=0),
    dict(n="B", cast="footman_b", d=4.3, xp=330, base="footman_b_stand", var=0),       # the nose-pincher
    dict(n="C", cast="knight_a_open", d=5.6, xp=510, base="knight_a_open_stand", var=0),
    dict(n="D", cast="footman_a", d=6.9, xp=190, base="footman_a_stand", var=2),
    dict(n="E", cast="knight_b", d=8.4, xp=640, base="knight_b_stand", var=0),
    dict(n="F", cast="footman_b", d=9.8, xp=95, base="footman_b_stand", var=1),
]
# jumps in shot 30: takeoff frame, jump kind, peak lift (m), splash size
JUMPS = dict(B=(1771, "jump_pinch_nose", 0.95, 1.25), A=(1776, "jump_arms_up", 1.1, 1.35), C=(1780, "jump_bomb", 0.85, 1.4),
             D=(1783, "jump_arms_up", 1.0, 1.2), E=(1788, "jump_bomb", 0.9, 1.3), F=(1792, "jump_pinch_nose", 0.8, 1.1))
T_AIR = 14                      # frames in the air
G_PINCH = (1731, 1756)           # shot 29: B pinches his nose
G_LOOK = (1709, 1725, 1745)      # shot 29: bridge -> water -> each other


def variant(p, v):
    if v: p = dict(p, variant21=v)
    return p


def idle(p, g, k):
    p = dict(p); p['lean'] = p.get('lean', 0) + 1.3 * math.sin(g * 0.11 + k); p['head_roll'] = p.get('head_roll', 0) + 1.8 * math.sin(g * 0.17 + 2 * k)
    p['blink'] = blink(g, 83 + 7 * int(k), int(k * 11)); return p


def make_bank(T, gs):
    pr = T.pr
    K.set_flow(0)
    for i in range(3): K.splash(0, 0, -1, name=str(i))          # the preset's default splashes
    c21.hide_prefix('fg_generic_g'); c21.hide_prefix('veg_reed')                              # QA-art: the dark near reed / gorse clump reads as black shards
    C0 = Vector((-27.0, 54.0, 2.5975866)); L0 = aim_pitch(C0, Vector(pr['look']), -4.5)
    Fv, Rv = fwd_vec(C0, L0), right_vec(C0, L0)
    cams = {}
    # shot 29: slide 40 px/s (about 0.35 m/s at 6 m) + push 8 %/s;  shot 30: continue, then pull-out 8 %/s and a yaw to the water
    def cam29(g):
        u = (g - 1709) / 60.0
        loc = C0 + Rv * (0.5 * u) + Fv * (0.6 * u) + Vector((0, 0, -0.05 * u))
        return loc, aim_pitch(loc, loc + Fv * 30 + Vector((0, 0, -5)), 0)  # placeholder, replaced below
    base_dir = (L0 - C0)
    def cam_g(g):
        if g < CUT30:
            u = (g - CUT29) / 60.0
            loc = C0 + Rv * (0.55 * u) + Fv * (0.7 * u)
            look = loc + base_dir
        else:
            u = (g - CUT30) / 52.0
            # snap yaw toward the water (+9 deg) then pull out 8 %/s with a slide
            yaw = math.radians(12.0) * (0.4 + 0.6 * quint(clamp((g - CUT30) / 40.0)))
            d = base_dir.copy(); c, s = math.cos(yaw), math.sin(yaw)
            # rotate about z toward the right vector (clockwise seen from above when looking along -y)
            dd = Vector((d.x * c + d.y * s, -d.x * s + d.y * c, d.z + 0.03 * d.length))
            loc = C0 + Rv * (1.0 + 0.8 * u) + Fv * (0.3 - 1.4 * u) + Vector((0, 0, -0.4 + 0.1 * u))
            look = loc + dd
        return loc, look
    T.cam_g = cam_g
    for g in gs:
        loc, look = cam_g(g); T.key_cam(bf(g), loc, look)
    P = {c['n']: c for c in CROWD}
    rigs = {}
    for k, c in enumerate(CROWD):
        n = c['n']; p0 = stage_xy(pr, c['d'], c['xp'])
        rvec = Rv
        ent = Vector(entry_point(p0.x, p0.y, rvec, 1.7 + 0.15 * k)).to_3d()
        ent.z = 0.0
        # stand point close to the edge so the jump is short
        base = pose_of(c['base']); base = variant(base, c['var'])
        flipbase = (k % 2 == 1)

        def tl(g, n=n, k=k, p0=p0, ent=ent, base=base, c=c, flipbase=flipbase):
            return actor_state(g, n, k, p0, ent, base, c, flipbase)
        rigs[n] = Rig(T, n, c['cast'], tl)
        rigs[n].ent = ent
    # helmets (drift, bob)
    for j, who in enumerate(("B", "D", "E")):
        t1 = JUMPS[who][0] + T_AIR
        ent = rigs[who].ent
        def tlh(g, j=j, t1=t1, ent=ent, who=who):
            if g < t1 + 5: return dict(hide=True)
            u = g - (t1 + 5)
            kind = ("kettle", "bascinet", "great")[j]
            x = ent.x + Rv.x * (0.25 * u / 30 + 0.4 * j) + 0.3 * math.sin(u * 0.15 + j); y = ent.y + Rv.y * (0.25 * u / 30 + 0.4 * j)
            return dict(pos=(x, y, 0.0), pose=dict(helm21=kind, t=(g / 40.0 + 0.3 * j) % 1.0, tilt=14 * math.sin(u * 0.2 + j)), contact=False, scale=wscale("footman_a"))
        rigs["H%d" % j] = Rig(T, "H%d" % j, "helmet_float", tlh)
    for r in rigs.values(): r.pose_frames(gs)
    T.sprites_for(128 if T.quality == 'draft' else 256)
    T.rigs = rigs
    T.Rv = Rv

    def on_g(g):
        t = g / 30.0
        K.set_flutter(t); K.set_smoke(t); K.set_flow(t)
        for r in rigs.values(): r.hook(g)
        # splashes
        for who, (t0, kind, h, sz) in JUMPS.items():
            age = (g - (t0 + T_AIR)) / 30.0 + 0.02
            e = rigs[who].ent
            K.splash(e.x, e.y, age if (age > 0 and g >= CUT30) else -1, size=sz * 0.5, name=who, seed=ord(who))
    return on_g


def actor_state(g, n, k, p0, ent, base, c, flipbase):
    """position / pose of crowd member n at film frame g (shots 29 and 30)"""
    jt = JUMPS.get(n)
    flip = flipbase
    pos = Vector(p0)
    p = dict(base)
    if g < CUT30:   # shot 29: looks at the bridge, the water, each other
        ph = 0 if g < G_LOOK[1] else (1 if g < G_LOOK[2] else 2)
        look_l = -1 if ph == 0 else (1 if ph == 1 else (-1 if k % 2 == 0 else 1))
        p['yaw'] = 0.9 * look_l; p['gaze'] = (0.9 * look_l, 0.0)
        p['expr'] = 'worried' if ph > 0 else 'neutral'
        if ph > 0: p['mouth'] = 'wavy'; p['fx'] = ['sweat'] if (k + g // 20) % 3 == 0 else []
        p['pitch'] = 0.1 if ph == 1 else 0.0
        if n == "B" and G_PINCH[0] <= g:
            u = ez((g - G_PINCH[0]) / 8.0)
            pp = pose_of("footman_b_jump_pinch_nose"); pp = dict(base, **{kk: pp[kk] for kk in ("arm_r", "expr", "mouth", "head_roll")}); pp.pop('prop_r', None)
            pp['legs'] = 'stand'; pp['expr'] = 'sweat' if 'sweat' in cast21.EXPR21 else 'worried'; p = pp
        return dict(pos=pos, pose=idle(p, g, k), flip=flip, contact=True)
    if jt is None: return dict(hide=True)
    t0, kind, h, sz = jt; t1 = t0 + T_AIR
    if g < t0 - 4:
        p['expr'] = 'worried'; p['mouth'] = 'wavy'; p['yaw'] = 0.6; p['gaze'] = (0.8, 0.0)
        return dict(pos=pos, pose=idle(p, g, k), flip=flip, contact=True)
    if g < t0:    # crouch before the jump: squash, arms back
        u = (g - (t0 - 4)) / 4.0
        p['squash'] = (1.0 + 0.05 * u, 1.0 - 0.1 * u); p['expr'] = 'shouting'
        return dict(pos=pos, pose=p, flip=flip, contact=True)
    if g < t1:    # airborne: parabolic lift, horizontal travel to the entry point
        u = (g - t0) / float(T_AIR)
        x = lerp(p0.x, ent.x, u); y = lerp(p0.y, ent.y, u)
        z = max(ground_z(p0.x, p0.y), 0.0) * (1 - u) + h * 4 * u * (1 - u) + 0.05 * u
        pj = pose_of(c['base'].rsplit('_', 1)[0] + '_' + kind) if False else pose_of(c['cast'] + '_' + kind)
        pj = variant(pj, c['var']); pj['yaw'] = 0.5
        return dict(pos=(x, y, z), pose=pj, flip=flip, contact=False)
    # in the water
    w = g - t1
    if w < 2: return dict(hide=True)
    s = w - 2
    drift = Vector((ent.x, ent.y, 0.0)) + T_RV * 0.0
    sw = 1.0 + 0.08 * math.sin(s * 0.5 + k) - 0.35 * max(0, 1 - s / 6.0)   # rises up out of the water
    if s < 11: pn = "swim_splutter"
    elif s < 22: pn = "swim_arms_up" if (k % 2 == 0) else "swim_bob"
    else: pn = "swim_paddle"
    pp = pose_of(c['cast'] + '_' + pn); pp = variant(pp, c['var'])
    pp['swim21'] = max(0.45, sw); pp['t'] = (s * 0.07 + k * 0.2) % 1.0
    mv = Vector((T_RVEC.x, T_RVEC.y, 0)) * (0.35 * s / 30.0 + (0.5 if pn == 'swim_paddle' else 0) * 0)
    px = ent.x + mv.x + 0.06 * math.sin(s * 0.3 + k); py = ent.y + mv.y
    return dict(pos=(px, py, 0.0), pose=pp, flip=False, contact=False)


T_RVEC = Vector((-1.0, 0.03, 0.0))
T_RV = Vector((0, 0, 0))



# ============================================================================= LOW (shot 31)
IMPACT = (1821, 1830, 1839)


def make_low(T, gs):
    pr = T.pr
    for i in range(3): K.splash(0, 0, -1, name=str(i))
    C0 = Vector(pr['cam']); L0 = Vector(pr['look']); C0.z = float(K.ground(C0.x, C0.y)) + 0.9
    base = L0 - C0; Fv = fwd_vec(C0, L0); Rv = right_vec(C0, L0)
    def cam_g(g):
        u = (g - 1821) / 27.0
        e = 0.3 * u + 0.7 * u * u            # quick accelerating push
        loc = C0 + Fv * (2.2 * e) + Rv * (0.5 * u) + Vector((0, 0, 0.1 * u))
        return loc, aim_pitch(loc, loc + base, -4.0)
    for g in gs:
        loc, look = cam_g(g); T.key_cam(bf(g), loc, look)
    pts = [Vector(p) for p in pr['splashes']]
    rigs = {}
    casts = ("footman_a", "footman_b", "knight_a_open")
    for j in range(3):
        def tl(g, j=j):
            s = g - IMPACT[j] - 5
            if s < 0 or j == 2: return dict(hide=True)
            x = pts[j].x + 0.9 * (1 if j % 2 else -1) + (-0.3 * s / 30.0)
            y = pts[j].y + 0.5
            pn = ("swim_splutter", "swim_arms_up")[j % 2]
            pp = pose_of(casts[j] + "_" + pn); pp['swim21'] = 1.0 + 0.1 * math.sin(s * 0.5); pp['t'] = (s * 0.08) % 1
            return dict(pos=(x, y, 0.0), pose=pp, contact=False)
        rigs["S%d" % j] = Rig(T, "S%d" % j, casts[j], tl)
    def tlh(g):
        if g < IMPACT[0] + 6: return dict(hide=True)
        u = g - IMPACT[0] - 6
        return dict(pos=(pts[0].x + 1.8 - 0.01 * u, pts[0].y - 0.4, 0.0), pose=dict(helm21="kettle", t=(g / 40.0) % 1, tilt=10 * math.sin(u * 0.3)), contact=False, scale=wscale("footman_a"))
    rigs["H0"] = Rig(T, "H0", "helmet_float", tlh)
    for r in rigs.values(): r.pose_frames(gs)
    T.sprites_for(128 if T.quality == 'draft' else 256); T.rigs = rigs

    def on_g(g):
        t = g / 30.0
        K.set_flutter(t); K.set_smoke(t); K.set_flow(t)
        for r in rigs.values(): r.hook(g)
        for j in range(3):
            age = (g - IMPACT[j]) / 30.0
            K.splash(pts[j].x, pts[j].y, age if age >= 0 else -1, size=pr.get('splash_size', 1.8), name="L%d" % j, seed=j)
    return on_g


# ============================================================================= driver
def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]; out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else: out.append(int(part))
    return out


def main():
    mode, quality, spec = sys.argv[1], sys.argv[2], sys.argv[3]
    out = sys.argv[4] if len(sys.argv) > 4 else os.path.join(HERE, "raw", mode)
    samples = int(sys.argv[5]) if len(sys.argv) > 5 else (12 if quality == "draft" else 24)
    lo, hi = RANGES[mode]
    gs = [g for g in parse(spec) if lo <= g <= hi]
    os.makedirs(out, exist_ok=True)
    skip_done = quality == "final"
    todo = [g for g in gs if not (skip_done and os.path.exists(os.path.join(out, "g_%04d.png" % g)))]
    if not todo: print("nothing to do"); return
    T = c21.Take(PRESET[mode], quality=quality)
    T.workdir = os.path.join(HERE, "work_" + mode); os.makedirs(T.workdir, exist_ok=True)
    on_g = {"bank": make_bank, "camp": (lambda T, gs: make_camp(T, gs)), "low": make_low}[mode](T, todo)
    T.render(todo, out, on_g, samples=samples, draft=(quality == "draft"))
    if os.environ.get("REPORT"):
        rep = {}
        for g in todo:
            f = bf(g); T.scene.frame_set(f); rep[g] = {n: T.head_px(r.a, f) for n, r in getattr(T, "rigs", {}).items() if g in r.state and not r.state[g].get("hide") and not n.startswith("H")}
        json.dump(rep, open(os.path.join(out, "heads.json"), "w"))




if __name__ == "__main__":
    main()

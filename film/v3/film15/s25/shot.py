#!/usr/bin/env python3
"""shot.py -- film 15 reveal (shots 25-31). One script, three takes (folder = first shot):
   s25 = shots 25-27 (B TENSE, g 1329..1509), s28 = shot 28 (B EVE, g 1510..1585, dissolve in + out), s29 = shots 29-31 (B TENSE -> EVE, g 1586..1803, dissolve in).
   python3 shot.py still <shot> g1,g2,.. [out] [scale] [samples]      draft stills
   python3 shot.py final <shot> a:b [part k n]                          frames to frames/g_%04d.png (resumable)
Placement: cast_test.py s27 / s28 (flop anchored on the crossbar, card 0.3 D toward the camera; straddle by the head anchor)."""
import sys, os, math, json, time
from c15 import *

BAR_X = 0.0; BAR_Y = F.STATE['J']['y'] * U if False else None
def gb(t): return int(round(t * 30))
B25, B26, B27, B28, B29, B30, B31, BEND = gb(44.30), gb(46.40), gb(49.00), gb(50.35), gb(52.85), gb(55.08), gb(58.20), gb(60.15)
SHOTS = {25: (B25, B26 - 1), 26: (B26, B27 - 1), 27: (B27, B28 - 1), 28: (B28, B29 - 1), 29: (B29, B30 - 1), 30: (B30, B31 - 1), 31: (B31, BEND - 1)}
LIGHT = {25: 'TENSE', 26: 'TENSE', 27: 'TENSE', 28: 'EVE', 29: 'TENSE', 30: 'TENSE', 31: 'EVE'}
G_SW = gb(56.6)                  # TENSE -> EVE pop (shot 30)
G_CHEER = gb(59.1)
DICK = 'dick_olympic'
PF = lambda n, c=DICK, **kw: cast15.pose_for(n, c, **kw)

# --------------------------------------------------------------------------------------------- Dick timeline (global g)
G_PLANT, G_TO, G_TO2, G_RISE, G_HEAD, G_BACK, G_FLOP = 1358, 1363, 1368, 1376, B26, 1416, 1434
G_FLICK0, G_FLICK1, G_LAND, G_LIE, G_SIT0, G_SIT1 = B29, B29 + 17, B29 + 40, B29 + 54, B30 + 14, B30 + 44
KEYS = [(G_PLANT, 'plant'), (G_TO, 'plant'), (G_TO2, 'takeoff'), (G_TO2 + 3, 'takeoff'), (G_RISE, 'flop_rise'), (G_HEAD, 'flop_head'), (G_BACK, 'flop_back'), (G_FLOP, 'flop'),
        (G_FLICK0, 'flop'), (G_FLICK1, 'flop_flick'), (G_LAND, 'land_back'), (G_LIE, 'lie_back'), (G_SIT0, 'lie_back'), (G_SIT1, 'sit_up')]
_PC = {}
def pc(n):
    if n not in _PC: _PC[n] = PF(n)
    return _PC[n]

def dick_pose(g):
    if g < G_PLANT: return cast15.run_curved(DICK, g / 16.0, 1)
    for (g0, n0), (g1, n1) in zip(KEYS, KEYS[1:]):
        if g0 <= g < g1:
            p = tween(pc(n0), pc(n1), sm(seg(g, g0, g1))) if n0 != n1 else dict(pc(n0))
            break
    else: p = dict(pc(KEYS[-1][1]))
    if G_FLOP <= g < G_FLICK0:                                  # hanging in the arch: breathing between flop and flop_back
        k = 0.2 * (0.5 + 0.5 * math.sin(2 * math.pi * g / 31.0)); p = tween(tween(pc('flop'), pc('flop_back'), k), pc('flop_flick'), 0.10 * (0.5 + 0.5 * math.sin(2 * math.pi * g / 53.0 + 1.0)))
    if G_FLOP - 6 <= g < G_FLICK0 + 4: p['roll2'] = p.get('roll2', 20) + 2.0 * math.sin(g * 0.21)
    if G_SIT1 <= g: p['gaze'] = (-0.3, -1.0); p['yaw'] = 0.1; p['pitch'] = -0.6 + 0.08 * math.sin(g * 0.13)
    if G_LIE <= g < G_SIT0: p['expr'] = 'neutral'
    p.pop('sawdust', None); p.pop('fx', None)
    return p

# --------------------------------------------------------------------------------------------- geometry (D)
def J(): return F.STATE['J']
def bar_c(): return Vector((0.0, J()['y'] * U, F.bar_height_m() * U))
def foam_z(): return J()['ground'] * U

def toward(cam, p, d):
    t = Vector(cam) - p; t.z = 0; return t.normalized() * d

RUN = dict(x0=-9.6, x1=-3.2, y0=18.4, y1=19.9)       # feet marks of the run (D), g = G_PLANT-35 .. G_PLANT+5
def run_xy(g):
    u = clamp((g - (G_PLANT - 35)) / 40.0)
    return RUN['x0'] + (RUN['x1'] - RUN['x0']) * u, RUN['y0'] + (RUN['y1'] - RUN['y0']) * u * u

BT = [(B26, -1.6, -0.35), (1417, -0.7, 0.0), (1435, 0.1, 0.12), (1452, 0.4, 0.0), (B28, 1.3, 0.05), (G_FLICK0, 1.6, 0.0)]
def bar_target(g):
    """world point of the 'bar' anchor: the card TRAVELS along the bar (head first, then back, then legs cross), z a little up at the thigh beat"""
    b = bar_c(); k = BT
    if g <= k[0][0]: x, z = k[0][1], k[0][2]
    elif g >= k[-1][0]: x, z = k[-1][1], k[-1][2]
    else:
        for (g0, x0, z0), (g1, x1, z1) in zip(k, k[1:]):
            if g0 <= g < g1: u = sm(seg(g, g0, g1)) * 0.6 + 0.4 * seg(g, g0, g1); x = lerp(x0, x1, u); z = lerp(z0, z1, u); break
    if g >= G_FLOP: x += 0.12 * math.sin(g * 0.11); z += 0.07 * math.sin(g * 0.23)
    return Vector((x, b.y, b.z + z))
FRONT = Vector((0.0, -0.3, 0.0))              # the card plane stays parallel to the bar, 0.3 D in front of it (no bar through the body)

def conv(r, a_from, a_to, cam, at):
    """world position of sprite anchor a_to when anchor a_from sits at world `at` (same card, yaw from the camera)"""
    d = Vector(cam) - at; yaw = math.atan2(d.x, -d.y); ax = Vector((math.cos(yaw), math.sin(yaw), 0)); a, b = r['anchors'][a_from], r['anchors'][a_to]
    return at + ax * (b[0] - a[0]) + Vector((0, 0, -(b[1] - a[1])))

LAND = None
def land_hip():
    return Vector((2.2, 24.0, foam_z() + 0.55))

_ref = {}
def ref_sprite(tag, cast, pose, ppd, canvas=None):
    if tag not in _ref: _ref[tag] = render_batch([dict(tag='ref_' + tag, cast=cast, pose=pose, ppd=ppd, canvas=canvas or WIDE)])[0]
    return _ref[tag]

def dick_spec(g, cam):
    pose = dick_pose(g); ppd = 192 if g >= G_RISE else 160
    def place(r, cam):
        kw = dict(scale=1.0, shadow=None, yaw_fixed=0.0 if g >= G_TO else None)
        if g < G_TO:                                           # run / plant: feet on the tartan
            x, y = run_xy(g); kw.update(mark=(x, y, 0.0), shadow=(1.5, 0.5)); return kw
        rb = ref_sprite('to', DICK, pc('takeoff'), 192)
        xt, yt = run_xy(G_TO)
        A = conv(rb, 'feet', 'bar', cam, Vector((xt, yt, 0.0)))        # bar anchor of the take-off pose standing at the take-off mark
        T0 = bar_target(G_HEAD); T = T0 + FRONT
        if g < G_HEAD:                                         # rise: the bar anchor flies from the take-off to the crossbar
            u = seg(g, G_TO, G_HEAD); p = Vector((lerp(A.x, T.x, sm(u)), lerp(A.y, T.y, sm(u)), lerp(A.z, T.z, 1 - (1 - u) ** 2)))
            kw.update(anchor=('bar', tuple(p))); hp = Vector((p.x, p.y, foam_z())); kw.update(shadow_at=(hp.x, hp.y, hp.z, 2.0, 0.7), shadow_a=0.35 * u)
        elif g < G_FLICK0:
            t = bar_target(g); p = t + FRONT; kw.update(anchor=('bar', tuple(p))); hp = Vector((p.x - 0.4, p.y, foam_z())); kw.update(shadow_at=(hp.x, hp.y, hp.z, 2.6, 0.9), shadow_a=0.55)
        else:                                                  # flick + fall + lie + sit: placed by the hip anchor
            t = bar_target(G_FLICK0); p0 = t + FRONT; rf = ref_sprite('flop', DICK, pc('flop'), 192)
            H0 = conv(rf, 'bar', 'hip', cam, p0); HL = land_hip()
            if g < G_FLICK1: u = seg(g, G_FLICK0, G_FLICK1); H = H0 + Vector((0.5 * sm(u), 0, 0.45 * math.sin(u * math.pi * 0.5)))
            elif g < G_LAND:
                u = seg(g, G_FLICK1, G_LAND); Ht = H0 + Vector((0.5, 0, 0.45)); e = u * u
                z = lerp(Ht.z, HL.z, e); w = clamp((bar_c().z - 0.9 - z) / max(0.1, bar_c().z - 0.9 - HL.z))
                H = Vector((lerp(Ht.x, HL.x, sm(u)), lerp(Ht.y, HL.y, sm(w)), z))
            else:
                u = seg(g, G_LAND, G_LAND + 10); bounce = 0.18 * math.exp(-u * 4) * abs(math.sin(u * 9.0)) if g < G_LAND + 10 else 0.0
                H = Vector((HL.x, HL.y, HL.z + bounce))
                if g >= G_SIT0: H.z = HL.z + 0.10 * sm(seg(g, G_SIT0, G_SIT1))
            kw.update(anchor=('hip', tuple(H))); kw.update(shadow_at=(H.x, HL.y if g >= G_FLICK1 else H.y, foam_z(), 2.8, 0.9), shadow_a=0.55)
        return kw
    return dict(tag='dick_%04d' % g, cast=DICK, pose=pose, ppd=ppd, canvas=WIDE, place=place, name='dick')

def rival_x(g): return lerp(-3.0, 2.6, clamp((g - 1500) / 94.0))
def rival_h(g):
    h = -1.7 + 2.4 * sm(seg(g, 1500, 1540)); h -= 2.0 * sm(seg(g, 1558, 1594)); return h      # lowest body part relative to the bar centre (D): rise, flat apex, come down
def rival_spec(g):
    """shot 28: a real straddle jump, belly down and FLAT: approach, rise, roll over (apex ~0.7 D above the bar at g1540-1558), come down"""
    st = lambda n: PF(n, 'rival1')
    if g < 1514: pose = st('takeoff')
    elif g < 1534: pose = tween(st('takeoff'), st('straddle_a'), sm(seg(g, 1514, 1534)))
    elif g < 1545: pose = st('straddle_a')
    elif g < 1557: pose = tween(st('straddle_a'), st('straddle_b'), sm(seg(g, 1545, 1557)))       # the pop: the other leg kicks up
    elif g < 1572: pose = st('straddle_b')
    else: pose = tween(st('straddle_b'), st('land_back'), sm(seg(g, 1572, 1592)))
    pose = dict(pose); pose['pitch'] = 0.3 + 0.05 * math.sin(g * 0.2)
    if 1530 <= g < 1575: pose['body_lean'] = 91; pose['roll2'] = 94      # flat, belly down
    def place(r, cam):
        b = bar_c(); an = r['anchors']; names = [n for n in ('hand_r', 'hand_l', 'foot_r', 'foot_l', 'knee_r', 'knee_l', 'head') if n in an]
        low = max(an[n][1] for n in names); hy = an['head'][1]
        zl = b.z + rival_h(g); p = Vector((rival_x(g), b.y, zl + (low - hy))) + FRONT
        return dict(scale=1.0, shadow=None, anchor=('head', tuple(p)), shadow_at=(p.x - 0.8, p.y, foam_z(), 3.2, 1.0), shadow_a=0.4, yaw_fixed=0.0)
    return dict(tag='rival_%04d' % g, cast='rival1', pose=pose, ppd=160, canvas=WIDE, place=place, name='rival')

MARKS = {}
def podium_specs(g):
    M = MARKS; k = 0.5 + 0.5 * math.sin(g * 0.5)
    cheer = seg(g, G_CHEER - 4, G_CHEER + 6)
    d = tween(PF('podium'), PF('cheer'), 0.0)
    pd = PF('podium'); pd['arm_r'] = dict(pd['arm_r']); 
    off = cast15.pose_for('official_raise', 'official1') if 'official_raise' in cast15.POSE_NAMES else PF('cheer', 'official1')
    rv = PF('cheer', 'rival2'); rv = tween(PF('stand', 'rival2'), rv, 0.5 + 0.5 * cheer)
    def mk(name, dz=0.0):
        return lambda r, cam: dict(mark=tuple(M[name]), scale=1.0, shadow=(1.5, 0.5))
    out = [dict(tag='pod2_%04d' % g, cast='official1', pose=off, ppd=128, place=mk('podium_2'), name='off'),
           dict(tag='pod3_%04d' % g, cast='rival2', pose=rv, ppd=128, place=mk('podium_3'), name='riv'),
           dict(tag='pod1_%04d' % g, cast=DICK, pose=dict(pd, bob=0.04 * math.sin(g * 0.6) * cheer), ppd=160, place=mk('podium_top'), name='dick')]
    cj = dict(PF('coach_jaw', 'coach_stands') if 'coach_jaw' in cast15.POSE_NAMES else PF('jaw_drop', 'coach_stands'))
    k = seg(g, 1774, 1782)
    cj['mouth'] = ('open', 0.30 * k, 0.22 * k) if k > 0 else 'flat'; cj['expr'] = 'shocked' if k > 0 else 'neutral'; cj['bob'] = 0.03 * math.sin(g * 0.5) * cheer
    cx, cy = [float(v) for v in os.environ.get('COACH', '-13.3,25.0').split(',')]; p = Vector((cx, cy, 0.0))
    out.append(dict(tag='coach_%04d' % g, cast='coach_stands', pose=cj, ppd=160, place=lambda r, cam: dict(mark=tuple(p), scale=1.0, shadow=(1.5, 0.5)), name='coach'))
    return out
COACH_AT = (-30.0, 108.5, 25.5); COACH_K = 3.2

# --------------------------------------------------------------------------------------------- cameras (metres): a/b per shot
CAMS = {                                           # start/end cameras (metres) used only to build the FG props (and as shot 25's path)
 25: dict(a=((-5.6, 7.2, 1.2), (-4.2, 11.6, 1.55)), b=((-1.6, 8.0, 1.4), (-0.3, 11.6, 1.9))),
}
def orbit(C, R, th, z):
    th = math.radians(th); return (C[0] + R * math.sin(th), C[1] - R * math.cos(th), z), tuple(C)
def bxm(g): return bar_target(g).x * DM
def U01(g, shot): g0, g1 = SHOTS[shot]; return (g - g0) / float(g1 - g0)
def LL(a, b, u): return tuple(lerp(x, y, u) for x, y in zip(a, b))
def cam26(g):
    u = U01(g, 26); C = (bxm(g) - 0.2, 11.6, 2.15)
    SN = lambda a: sm(seg(g, a - 2, a + 3))
    th = lerp(-26, 8, u) + 24 * (SN(1404) - SN(1416) + SN(1434) - SN(1450))
    PU = lambda a: sm(seg(g, a - 1, a + 6)) * (1 - sm(seg(g, a + 9, a + 17)))       # quick eased push-in on each beat
    R = lerp(3.0, 2.7, u) * (1 - 0.15 * (PU(1392) + PU(1416) + PU(1434)))
    return orbit(C, R, th, lerp(1.95, 2.05, u))
def cam27(g):
    u = U01(g, 27); C = (bxm(g) - 0.2, 11.6, 2.15)
    return orbit(C, lerp(3.0, 2.4, u) - 0.75 * sm(seg(g, 1470, 1476)) + 0.35 * sm(seg(g, 1486, 1500)) - 0.5 * sm(seg(g, 1490, 1496)) + 0.5 * sm(seg(g, 1500, 1505)) - 0.5 * sm(seg(g, 1507, 1513)), lerp(22, -10, u) + 6 * math.sin(g * 0.25) + 16 * (sm(seg(g, 1470, 1476)) * 0 + sm(seg(g, 1492, 1498)) - sm(seg(g, 1502, 1508))), 2.0)
def cam28(g):
    u = U01(g, 28); x = rival_x(g) * DM; zc = 2.3 + 0.7 * sm(seg(g, 1516, 1530)) - 0.7 * sm(seg(g, 1560, 1570)); C = (x - 0.35, 11.6, zc)      # tilt follows him up to the apex
    th = lerp(-24, 20, u) + 16 * (sm(seg(g, 1526, 1532)) - sm(seg(g, 1543, 1549)) + sm(seg(g, 1558, 1564)))
    R = lerp(3.4, 3.1, u) - 0.7 * sm(seg(g, 1543, 1551)) - 0.9 * sm(seg(g, 1558, 1566))                                                      # push on the pop and on the drop
    return orbit(C, R, th, 2.0)
def cam29(g):
    gw0, gw1 = G_FLICK1 - 2, G_FLICK1 + 8; Lx = land_hip().x * DM
    Cb = lambda gg: (bxm(gg) - 0.2, 11.6, 2.2)
    if g <= gw0: return orbit(Cb(g), 2.4, lerp(-12, 12, clamp((g - (B29 - 8)) / float(gw0 - B29 + 8))), 2.0)
    p0 = orbit(Cb(gw0), 2.4, 12, 2.0); p1 = orbit((Lx, 13.0, 1.25), 3.4, -8, 2.0)
    if g <= gw1: return LL(p0[0], p1[0], seg(g, gw0, gw1)), LL(p0[1], p1[1], seg(g, gw0, gw1))
    return orbit((Lx, 13.0, 1.25), lerp(3.4, 3.1, seg(g, gw1, B30)), lerp(-8, 16, seg(g, gw1, B30 + 10)), lerp(2.0, 1.9, seg(g, gw1, B30)))
def cam30(g):
    u = U01(g, 30); C = (land_hip().x * DM + 0.3, 13.0, lerp(1.5, 1.6, u)); return orbit(C, lerp(3.5, 3.1, u) - 0.7 * sm(seg(g, G_SW - 2, G_SW + 10)), lerp(-22, 32, u), lerp(1.55, 1.6, u))
def cam31(g):
    u = U01(g, 31); R = lerp(4.4, 3.9, u) * (1 - 0.14 * sm(seg(g, G_CHEER - 3, G_CHEER + 9))); return orbit((-8.3, 10.0, 2.2), R, lerp(30, 14, u) + 16 * (sm(seg(g, 1760, 1766)) - sm(seg(g, G_CHEER - 2, G_CHEER + 4))), 1.8)
CAMF = {26: cam26, 27: cam27, 28: cam28, 29: cam29, 30: cam30, 31: cam31}
def cam25(g):
    u = U01(g, 25); lo = Vector(LL(CAMS[25]['a'][0], CAMS[25]['b'][0], u)); lk = Vector(LL(CAMS[25]['a'][1], CAMS[25]['b'][1], u))
    k = 1 - 0.17 * sm(seg(g, 1361, 1368)) - 0.10 * sm(seg(g, 1380, 1388)) + 0.16 * sm(seg(g, 1323, 1331)) * (1 - sm(seg(g, 1331, 1337))) - 0.14 * sm(seg(g, 1346, 1352)) + 0.14 * sm(seg(g, 1354, 1360))
    lk = lk + Vector((0.45 * (sm(seg(g, 1343, 1350)) - sm(seg(g, 1368, 1374))), 0, 0)); return tuple(lk + (lo - lk) * k), tuple(lk)
CAMF[25] = cam25

FGS = []
def yaw_of_cam(c): return math.atan2(c[1][1] - c[0][1], c[1][0] - c[0][0])
def set_cam(sc, cam, shot, g):
    c = CAMF[shot](g); F.make_camera(F.cam_from(tuple(x * U for x in c[0]), tuple(x * U for x in c[1])))
    if FGS:                                          # FG props ride the camera (rigid, 10 % slip for parallax)
        c0, y0 = FGS[0]['c0'], FGS[0]['y0']; d = yaw_of_cam(c) - y0; cs, sn = math.cos(d), math.sin(d)
        tx = c[0][0] - (cs * c0[0][0] - sn * c0[0][1]) - 0.10 * (c[0][0] - c0[0][0]); ty = c[0][1] - (sn * c0[0][0] + cs * c0[0][1]) - 0.10 * (c[0][1] - c0[0][1])
        for f in FGS:
            f['o'].rotation_euler = (0, 0, d); f['o'].location = (tx, ty, f['z0'] + c[0][2] - c0[0][2])

def setup(shot, h_in, h_out):
    MARKS.update(F.build('B', LIGHT[shot])['marks']); sc = bpy.context.scene; F.setup_render(sc, 'final'); clear_cards()
    sd = F.SHOTS[shot]; g0, g1 = SHOTS[shot]
    a = CAMF[shot](g0 - h_in); b = CAMF[shot](g1 + h_out)
    sd['a'] = dict(loc=a[0], look=a[1]); sd['b'] = dict(loc=b[0], look=b[1]); sd['punch'] = None; sd['whip'] = False
    cam = SH.setup_shot(shot, g0 - h_in, g1 + h_out)
    cam.animation_data_clear(); FGS.clear()
    for o in bpy.data.objects:
        if o.get('fg'):
            z0 = o.location.z; o.animation_data_clear(); FGS.append(dict(o=o, z0=z0, c0=a, y0=yaw_of_cam(a)))
    if LIGHT[shot] == 'TENSE': dim_pool(0.55)
    F.crowd_mode('hush', frame=g0 - 20)
    if shot >= 30: F.crowd_mode('hush', frame=G_SW - 1); F.crowd_mode('normal', frame=G_SW + 12)
    if shot == 31:
        F.crowd_mode('normal', frame=G_CHEER - 8); F.crowd_mode('cheer', frame=G_CHEER + 6); F.torch_flicker(1.4, frame=G_CHEER); F.stand_flashes(B31 - 6, BEND + 8, density=2.2)
        for f in (B31 + 6, G_CHEER + 3, G_CHEER + 14, G_CHEER + 26): F.flash_bulb(f, energy=6e3)
    if shot >= 29: F.switch_light('EVE', G_SW, 10)
    return sc, cam

def specs_for(shot, g, cam):
    if shot == 28: return [rival_spec(g)]
    if shot in (25, 26, 27, 29, 30): return [dick_spec(g, cam)]
    return podium_specs(g)

def frame(sc, shot, g, out):
    sc.frame_set(g); set_cam(sc, sc.camera, shot, g); cam = cam_loc_now(); clear_cards()
    sp = specs_for(shot, g, cam); info = {}
    if sp:
        rs = render_batch(sp)
        for s, r in zip(sp, rs):
            kw = s['place'](r, cam); pt = put(s['tag'], r, cam, **kw)
            info[s['name']] = {n: screen(pt['world'](r['anchors'][n])) for n in ('head', 'head_top', 'hip', 'feet') if n in r['anchors']}
    wall, cpu = F.T.render(out); clear_cards(); return info, wall, cpu

def parse(spec):
    if ':' in spec: a, b = spec.split(':')[:2]; return list(range(int(a), int(b) + 1))
    return [int(x) for x in spec.split(',')]

if __name__ == '__main__':
    cmd = sys.argv[1]; shot = int(sys.argv[2]); gs = parse(sys.argv[3])
    if cmd == 'still':
        outd = sys.argv[4] if len(sys.argv) > 4 else os.path.join(WORK, 'stills'); os.makedirs(outd, exist_ok=True)
        scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5; samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
        sc, cam = setup(shot, 8, 8); r = sc.render; r.resolution_percentage = int(scale * 100); sc.cycles.samples = samples
        for g in gs:
            p = os.path.join(outd, 's%d_g%04d.png' % (shot, g)); info, wall, cpu = frame(sc, shot, g, p); print(shot, g, json.dumps(info), '%.1fs' % wall, flush=True)
    else:
        part = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (0, 1)
        outd = os.path.join(HERE, 'frames'); os.makedirs(outd, exist_ok=True)
        sc, cam = setup(shot, 8, 8); sc.cycles.samples = 12; lg = open(os.path.join(WORK, 'log_%d_%d.jsonl' % (shot, part[0])), 'a')
        for i, g in enumerate(gs):
            if i % part[1] != part[0]: continue
            own = SHOTS[shot][0] <= g <= SHOTS[shot][1]
            od = outd if own else os.path.join(HERE, 'frames_x', str(shot)); os.makedirs(od, exist_ok=True)
            p = os.path.join(od, 'g_%04d.png' % g)
            if os.path.exists(p): continue
            info, wall, cpu = frame(sc, shot, g, p); lg.write(json.dumps(dict(g=g, info=info, wall=round(wall, 1), cpu=round(cpu, 1))) + '\n'); lg.flush(); print(g, '%.1fs' % wall, flush=True)

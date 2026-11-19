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
        k = 0.16 * (0.5 + 0.5 * math.sin(2 * math.pi * g / 47.0)); p = tween(pc('flop'), pc('flop_back'), k)
    if G_FLOP - 6 <= g < G_FLICK0 + 4: p['roll2'] = p.get('roll2', 20) + 2.0 * math.sin(g * 0.21)
    if G_SIT1 <= g: p['gaze'] = (-0.4, -0.5); p['yaw'] = 0.2; p['pitch'] = 0.2 + 0.1 * math.sin(g * 0.13)
    if G_LIE <= g < G_SIT0: p['expr'] = 'neutral'
    p.pop('sawdust', None); p.pop('fx', None)
    return p

# --------------------------------------------------------------------------------------------- geometry (D)
def J(): return F.STATE['J']
def bar_c(): return Vector((0.0, J()['y'] * U, F.bar_height_m() * U))
def foam_z(): return J()['ground'] * U

def toward(cam, p, d):
    t = Vector(cam) - p; t.z = 0; return t.normalized() * d

RUN = dict(x0=-8.8, x1=-3.2, y0=20.8, y1=19.9)       # feet marks of the run (D), g = G_PLANT-35 .. G_PLANT+5
def run_xy(g):
    u = clamp((g - (G_PLANT - 35)) / 40.0)
    return RUN['x0'] + (RUN['x1'] - RUN['x0']) * u, RUN['y0'] + (RUN['y1'] - RUN['y0']) * u * u

def bar_target(g):
    """world point of the 'bar' anchor of the flop cards (on the crossbar centre line, 0.3 D toward the camera)"""
    b = bar_c(); x = b.x
    x += lerp(-1.0, 0.4, sm(seg(g, G_HEAD, B27))) if g < B27 else lerp(0.4, 1.0, seg(g, B27, G_FLICK0))
    return Vector((x, b.y, b.z + (0.05 * math.sin(g * 0.18) if g >= G_FLOP else 0.0)))

def conv(r, a_from, a_to, cam, at):
    """world position of sprite anchor a_to when anchor a_from sits at world `at` (same card, yaw from the camera)"""
    d = Vector(cam) - at; yaw = math.atan2(d.x, -d.y); ax = Vector((math.cos(yaw), math.sin(yaw), 0)); a, b = r['anchors'][a_from], r['anchors'][a_to]
    return at + ax * (b[0] - a[0]) + Vector((0, 0, -(b[1] - a[1])))

LAND = None
def land_hip():
    return Vector((1.1, 24.0, foam_z() + 0.55))

_ref = {}
def ref_sprite(tag, cast, pose, ppd, canvas=None):
    if tag not in _ref: _ref[tag] = render_batch([dict(tag='ref_' + tag, cast=cast, pose=pose, ppd=ppd, canvas=canvas or WIDE)])[0]
    return _ref[tag]

def dick_spec(g, cam):
    pose = dick_pose(g); ppd = 192 if g >= G_RISE else 160
    def place(r, cam):
        kw = dict(scale=1.0, shadow=None)
        if g < G_TO:                                           # run / plant: feet on the tartan
            x, y = run_xy(g); kw.update(mark=(x, y, 0.0), shadow=(1.5, 0.5)); return kw
        rb = ref_sprite('to', DICK, pc('takeoff'), 192)
        xt, yt = run_xy(G_TO)
        A = conv(rb, 'feet', 'bar', cam, Vector((xt, yt, 0.0)))        # bar anchor of the take-off pose standing at the take-off mark
        T0 = bar_target(G_HEAD); T = Vector((T0.x, T0.y, T0.z)) + toward(cam, T0, 0.3)
        if g < G_HEAD:                                         # rise: the bar anchor flies from the take-off to the crossbar
            u = seg(g, G_TO, G_HEAD); p = Vector((lerp(A.x, T.x, sm(u)), lerp(A.y, T.y, sm(u)), lerp(A.z, T.z, 1 - (1 - u) ** 2)))
            kw.update(anchor=('bar', tuple(p))); hp = Vector((p.x, p.y, foam_z())); kw.update(shadow_at=(hp.x, hp.y, hp.z, 2.0, 0.7), shadow_a=0.35 * u)
        elif g < G_FLICK0:
            t = bar_target(g); p = t + toward(cam, t, 0.3); kw.update(anchor=('bar', tuple(p))); hp = Vector((p.x - 0.4, p.y, foam_z())); kw.update(shadow_at=(hp.x, hp.y, hp.z, 2.6, 0.9), shadow_a=0.55)
        else:                                                  # flick + fall + lie + sit: placed by the hip anchor
            t = bar_target(G_FLICK0); p0 = t + toward(cam, t, 0.3); rf = ref_sprite('flop', DICK, pc('flop'), 192)
            H0 = conv(rf, 'bar', 'hip', cam, p0); HL = land_hip()
            if g < G_FLICK1: u = seg(g, G_FLICK0, G_FLICK1); H = H0 + Vector((0.5 * sm(u), 0, 0.45 * math.sin(u * math.pi * 0.5)))
            elif g < G_LAND:
                u = seg(g, G_FLICK1, G_LAND); Ht = H0 + Vector((0.5, 0, 0.45)); e = u * u
                H = Vector((lerp(Ht.x, HL.x, sm(u)), lerp(Ht.y, HL.y, sm(u)), lerp(Ht.z, HL.z, e)))
            else:
                u = seg(g, G_LAND, G_LAND + 10); bounce = 0.18 * math.exp(-u * 4) * abs(math.sin(u * 9.0)) if g < G_LAND + 10 else 0.0
                H = Vector((HL.x, HL.y, HL.z + bounce))
                if g >= G_SIT0: H.z = HL.z + 0.10 * sm(seg(g, G_SIT0, G_SIT1))
            kw.update(anchor=('hip', tuple(H))); kw.update(shadow_at=(H.x, H.y, foam_z(), 2.8, 0.9), shadow_a=0.55)
        return kw
    return dict(tag='dick_%04d' % g, cast=DICK, pose=pose, ppd=ppd, canvas=WIDE, place=place, name='dick')

def rival_spec(g):
    """shot 28 contrast: straddle roll, belly down, the whole body above the bar"""
    k = seg(g, B28 - 8, B29 + 8)
    pose = tween(PF('straddle_a', 'rival1'), PF('straddle_b', 'rival1'), sm(seg(g, B28 + 20, B28 + 55)))
    pose['pitch'] = 0.3 + 0.05 * math.sin(g * 0.2)
    def place(r, cam):
        b = bar_c(); x = lerp(-0.2, 1.4, k)
        hz = b.z + 1.6 + 0.12 * math.sin(math.pi * k) + 0.05 * math.sin(g * 0.3)
        p = Vector((x, b.y, hz)); p += toward(cam, p, 0.3)
        return dict(scale=1.0, shadow=None, anchor=('head', tuple(p)), shadow_at=(p.x - 0.8, p.y, foam_z(), 3.2, 1.0), shadow_a=0.4)
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
    cj = PF('coach_jaw', 'coach_stands') if 'coach_jaw' in cast15.POSE_NAMES else PF('jaw_drop', 'coach_stands')
    out.append(dict(tag='coach_%04d' % g, cast='coach_stands', pose=cj, ppd=160, place=lambda r, cam: dict(mark=COACH_AT, scale=COACH_K, shadow=(1.5, 0.5)), name='coach'))
    return out
COACH_AT = (-30.0, 108.5, 25.5); COACH_K = 3.2

# --------------------------------------------------------------------------------------------- cameras (metres): a/b per shot
CAMS = {
 25: dict(a=((-4.6, 7.2, 1.2), (-3.2, 11.6, 1.55)), b=((-2.2, 8.0, 1.4), (-0.9, 11.6, 1.9))),
 26: dict(a=((-0.85, 9.0, 1.95), (-0.85, 11.6, 2.15)), b=((-0.1, 9.2, 2.0), (-0.1, 11.6, 2.15))),
 27: dict(a=((-0.05, 9.2, 2.0), (-0.05, 11.6, 2.15)), b=((0.15, 9.7, 2.0), (0.15, 11.6, 2.15))),
 28: dict(a=((-0.45, 8.6, 2.1), (-0.15, 11.6, 2.55)), b=((0.25, 9.0, 2.1), (0.55, 11.6, 2.55))),
 29: dict(a=((0.25, 9.2, 2.0), (0.25, 11.6, 2.15)), b=((0.3, 9.6, 2.0), (0.3, 11.6, 2.15))),
 30: dict(a=((-0.9, 9.6, 1.6), (0.5, 12.8, 1.5)), b=((-0.1, 10.4, 1.6), (0.9, 12.8, 1.4))),
 31: dict(a=((-5.9, 4.8, 1.7), (-8.9, 10.0, 2.3)), b=((-6.4, 5.4, 1.7), (-9.2, 10.0, 2.3))),
}
PUNCH = {31: (59.1, 20)}

def setup(shot, h_in, h_out):
    MARKS.update(F.build('B', LIGHT[shot])['marks']); sc = bpy.context.scene; F.setup_render(sc, 'final'); clear_cards()
    sd = F.SHOTS[shot]; c = CAMS[shot]
    sd['a'] = dict(loc=c['a'][0], look=c['a'][1]); sd['b'] = dict(loc=c['b'][0], look=c['b'][1]); sd['punch'] = PUNCH.get(shot); sd['whip'] = False
    g0, g1 = SHOTS[shot]
    cam = SH.setup_shot(shot, g0 - h_in, g1 + h_out)
    if shot == 29:                                   # custom keys: hold on the arch, WHIP down to the foam with the fall
        cam.animation_data_clear(); gw0, gw1 = G_FLICK1 - 2, G_FLICK1 + 8
        def kc(f, loc, look, ip):
            c = F.make_camera(F.cam_from(tuple(x * U for x in loc), tuple(x * U for x in look))); cam.location = c.location; cam.rotation_euler = c.rotation_euler
            cam.keyframe_insert('location', frame=f); cam.keyframe_insert('rotation_euler', frame=f)
            F.T._key(cam, 'location', f, ip); F.T._key(cam, 'rotation_euler', f, ip)
        kc(g0 - 8, (0.25, 9.2, 2.0), (0.25, 11.6, 2.15), 'BEZIER'); kc(gw0, (0.4, 8.8, 2.0), (0.4, 11.6, 2.45), 'LINEAR')
        kc(gw1, (0.2, 9.6, 2.0), (0.6, 13.0, 1.25), 'BEZIER'); kc(g1 + 8, (0.45, 10.0, 1.9), (0.75, 13.0, 1.25), 'BEZIER')
        for o in bpy.data.objects:
            if o.get('fg'): o.animation_data_clear()
    if LIGHT[shot] == 'TENSE': dim_pool(0.55)
    # crowd: hush through the reveal, normal at the pop, cheer on the medal
    F.crowd_mode('hush', frame=g0 - 20)
    if shot >= 30: F.crowd_mode('hush', frame=G_SW - 1); F.crowd_mode('normal', frame=G_SW + 12)
    if shot == 31:
        F.crowd_mode('normal', frame=G_CHEER - 8); F.crowd_mode('cheer', frame=G_CHEER + 6); F.torch_flicker(1.4, frame=G_CHEER); F.stand_flashes(B31 - 6, BEND + 8, density=1.0)
        for f in (B31 + 4, B31 + 15, G_CHEER + 3, G_CHEER + 12, G_CHEER + 25): F.flash_bulb(f)
    if shot >= 29: F.switch_light('EVE', G_SW, 10)
    return sc, cam

def specs_for(shot, g, cam):
    if shot == 28: return [rival_spec(g)]
    if shot in (25, 26, 27, 29, 30): return [dick_spec(g, cam)]
    return podium_specs(g)

def frame(sc, shot, g, out):
    sc.frame_set(g); cam = cam_loc_now(); clear_cards()
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
            p = os.path.join(outd, 'g_%04d.png' % g)
            if os.path.exists(p): continue
            info, wall, cpu = frame(sc, shot, g, p); lg.write(json.dumps(dict(g=g, info=info, wall=round(wall, 1), cpu=round(cpu, 1))) + '\n'); lg.flush(); print(g, '%.1fs' % wall, flush=True)

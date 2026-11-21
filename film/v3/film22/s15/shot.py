#!/usr/bin/env python3
"""s15 (film 22): BIGZOOM 2 and the ENDING, london NIGHT. Extreme wide over the night city (match dissolve from s14), dive past roofs and the red bus to the lit PUBLICITY DEPT
window, through the opening onto the official buried in towers of pocket maps, ending MEDIUM (official 35-60 % of frame height). Film frames 1752-1889 (n 138); 10 handle
frames before (the dissolve), none after (hard end).
Run:  python3 shot.py [--draft] [--frames a:b] [--step n] [--part k/n]"""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c22 as C
B, bpy, V = C.B, C.bpy, C.V
import beck_london as L, beck_hq as H

F0, F1 = 1752, 1890; HANDLES_PRE, HANDLES_POST = 10, 0
CAM = [(0, (-14.0, -52.0, 80.0), (-3.0, 44.0, 0.0), 22), (24, (-10.0, -44.0, 70.0), (-1.0, 38.0, 2.0), 23), (44, (-3.0, -16.0, 40.0), (0.0, 26.0, 10.0), 25),
       (52, (-2.0, 2.0, 22.0), (0.0, 24.0, 11.0), 27), (62, (0.0, 12.0, 13.5), (0.0, 30.0, 10.5), 28), (68, (0.0, 20.5, 11.5), (0.0, 38.0, 10.2), 30),
       (74, (0.0, 26.5, 11.3), (0.0, 40.0, 10.3), 32), (100, (0.2, 33.0, 10.9), (0.2, 43.5, 10.5), 31), (137, (0.2, 39.0, 10.5), (0.2, 43.5, 10.5), 33)]
B.ALL_SHOTS['s15']['cam'] = CAM
_N = B.LIGHTS['NIGHT_CITY']                                              # raise the night ambient (~1.3x) so the start reaches luma 85-110
_N['key'] = tuple(x * 1.35 for x in _N['key']); _N['shade'] = tuple(min(1.0, x * 1.6) for x in _N['shade']); _N['shade_tint'] = tuple(min(1.0, x * 1.4) for x in _N['shade_tint'])
_N['lift'] = tuple(x + 0.03 for x in _N['lift'])
B.ALL_SHOTS['s15']['actors'] = lambda g: None
B.ALL_SHOTS['s15']['state'] = dict(map_towers=0.0, crate=None)         # towers and crate are built here (own placement)
BOXES = [(-70, 80, -9, 24)]
LAND = 104                                                              # local frame the crate lands (61.72 s -> film frame 1856)

rs = random.Random(15)
SPECS = []
for n in range(26):                                                      # far pavement, toward the station entrance / along the HQ front
    row = rs.choice([15.8, 17.0, 18.2, 19.4, 20.6, 21.8]); d = 1 if n % 2 else -1
    x0 = rs.uniform(-40, 60); x1 = x0 + d * rs.uniform(30, 70)
    SPECS.append(dict(i=n * 3 + 2, p0=(x0, row), p1=(x1, row), speed=rs.uniform(4.0, 5.4), t0=-rs.randint(0, 60), stride=rs.uniform(2.9, 3.4), loop=True))
for n in range(10):                                                      # near pavement
    row = rs.choice([-7.0, -6.0, -5.0, -4.0]); x0 = rs.uniform(-30, 60)
    SPECS.append(dict(i=n * 7 + 40, p0=(x0, row), p1=(x0 + 60, row), speed=rs.uniform(4.0, 5.4), t0=-rs.randint(0, 60), stride=3.1, loop=True))

LAMP_K = 0.4
W = {}
def sstep(a, b, x): u = max(0.0, min(1.0, (x - a) / float(b - a))); return u * u * (3 - 2 * u)

def build_towers(spots):
    C_, TX = B.STATE['C'], B.STATE['TX']; r = random.Random(8); tp = B.Part('my_towers', ink=True); mb = tp.mb; tm = TX('pocket_map', 0.48, 1.0); top = C_('#f0dcb0', 0.5, 1.4, smix=0.2)
    z0 = H.PZ0
    for (sx, sy, mx) in spots:
        nH = max(1, int(mx / 0.32)); z = z0
        for i in range(nH):
            yaw = r.uniform(-0.12, 0.12); ax = V((math.cos(yaw), math.sin(yaw), 0)); ay = V((-math.sin(yaw), math.cos(yaw), 0))
            B.obox(mb, V((sx + r.uniform(-0.08, 0.08), sy + r.uniform(-0.08, 0.08), z + 0.16)), ax, ay, V((0, 0, 1)), 0.62, 0.45, 0.16,
                   (tm if i % 2 == 0 else top) if i % 7 else [C_('#e3262b', 1.2, 1.6), C_('#1f49c8', 1.2, 1.6), C_('#ffc81e', 1.2, 1.6), C_('#12a15a', 1.2, 1.6)][(i // 7) % 4]); z += 0.32
    tp.done((0, 43, H.PZ0 + 3), px=2.5)

TOWER_SPOTS = [(-2.0, 45.0, 6.9), (2.1, 45.0, 6.7), (-3.5, 43.6, 6.4), (3.6, 43.6, 6.6), (-1.0, 46.1, 6.9), (1.2, 46.1, 6.9), (-5.0, 42.4, 6.8), (5.1, 42.2, 6.2), (-3.3, 45.8, 6.9), (3.4, 45.8, 6.8),
               (-6.4, 44.5, 6.9), (6.5, 44.4, 6.9), (-5.6, 40.6, 5.2), (5.8, 40.8, 5.6)]

def setup(scene):
    B.STATE['lamp_gain'] = 1.0
    build_towers(TOWER_SPOTS)
    for o in list(bpy.data.objects):
        if o.name.startswith('pubL') and o.type == 'LIGHT': o.data.energy *= LAMP_K
    for nm in ('pub_lamp_glow', 'pub_clock'): C.scale_emission(nm, 0.35)
    lamp = bpy.data.objects.get('off_lamp')
    if lamp: lamp.data.energy *= 1.6
    C.fill_foreground()
    W['wk'] = C.Walkers(SPECS, scale=1.45)
    W['off'] = None; W['crate'] = None; W['cshadow'] = None

def crate_obj(t, k=0):
    """map crate falling (t 0 high -> 1 landed on the desk beside the official, contact shadow growing)."""
    for nm in ('map_crate', 'crate_shadow'):
        o = bpy.data.objects.get(nm)
        if o: bpy.data.objects.remove(o, do_unlink=True)
    if t is None: return
    C_, TX = B.STATE['C'], B.STATE['TX']
    x0, y0 = 1.95, 42.6; zt = H.PZ0 + 1.96; z0 = zt + 0.02 + (1.0 - min(1.0, t)) ** 2 * 7.0 + (0.16 * abs(math.sin((k - LAND) * 0.8)) * max(0.0, 1 - (k - LAND) / 6.0) if k > LAND else 0.0)
    cp = B.Part('map_crate', ink=True); mb = cp.mb; hx, hy, hh = 0.55, 0.48, 0.95
    mb.box((x0 - hx, y0 - hy, z0), (x0 + hx, y0 + hy, z0 + hh), C_('#a86a32', 1.0, 1.8), mats={'front': TX('crate_maps', 1.0, 1.0)})
    mb.box((x0 - hx - 0.05, y0 - hy - 0.05, z0 + hh * 0.45), (x0 + hx + 0.05, y0 + hy + 0.05, z0 + hh * 0.58), C_('#5a2c12')); cp.done((x0, y0, z0 + 0.6), px=2.5)
    sh = B.Part('crate_shadow', ink=False, shadow=False); r_ = 1.1 * (0.6 + 0.4 * min(1.0, t))
    B.plane(sh.mb, (x0 - r_, y0 - r_ * 0.8, zt + 0.02), (2 * r_, 0, 0), (0, 1.6 * r_, 0), B.STATE['E']('blob', 'blob', alpha=True), (0, 0, 1, 1)); sh.done()

def off_card15(cam, pose):
    import cast22
    c_, p_ = cast22.STORY22['off_buried_eat']; dy = p_.get('desk_y', 1.3); zt = H.PZ0 + 1.9; x, y = H.OFF_DESK; y += 1.0; cam = V(cam)
    hz = math.hypot(cam.x - x, cam.y - y); elev = math.degrees(math.atan2(cam.z - (zt + 1.3), max(hz, 1e-3))); tilt = max(0.0, min(40.0, 0.8 * elev))
    yaw = math.degrees(math.atan2(cam.x - x, -(cam.y - y)))
    ob = B.cast_card('off_buried_eat', (x, y, 0.0), yaw_deg=yaw, tilt=tilt, pose=dict(desk=0, typewriter=0, **pose), shadow=False, rim='#a8bcff')
    hd = B.card_anchor(ob, 'head'); ob.location = (x + (x - hd.x), y + (y - hd.y), ob.location.z + (zt + dy - hd.z))
    return ob

def off_pose(k):
    ph = (k % 24) / 24.0
    roll = (1, 3, 5, 3)[int(ph * 4) % 4]; bob = (0.0, 0.05, 0.10, 0.05)[int(((k % 12) / 12.0) * 4) % 4]
    gaze = ((0.7, 0.4), (0.5, 0.5), (0.7, 0.4), (0.9, 0.3))[(k // 14) % 4]
    puff = 1.0
    if LAND + 1 <= k <= LAND + 4: puff = 0.35                   # gulp when the crate lands
    elif LAND + 5 <= k <= LAND + 8: puff = 0.7
    sweat = 1.0
    return dict(head_roll=roll, gaze=gaze, puff=puff, sweat=sweat,
                arm_r=dict(hand=(0.82, 0.80 + bob), bend=-0.2, stretch=1.2, layer='top'), prop_r=dict(type='fork', angle=-46 + (4 if bob > 0.04 else 0), scale=1.5),
                arm_l=dict(hand=(-0.80, 0.86 + (0.10 - bob)), bend=-0.2, stretch=1.2, layer='front'), prop_l=dict(type='knife', angle=-116 - (4 if bob > 0.04 else 0), scale=1.5), mouth='flat')

def frame(g, k, n):
    bpy.context.scene.camera.data.shift_y = -0.10 * (1 - sstep(30, 52, k))
    cam = B.STATE['cam']
    W['wk'].update(g, cam)
    # the official: re-faced to the camera every frame (seated card)
    if W['off'] is not None and W['off'].name in bpy.data.objects: bpy.data.objects.remove(W['off'], do_unlink=True)
    W['off'] = off_card15(cam, off_pose(k))
    t = None if k < LAND - 16 else min(1.0, (k - (LAND - 16)) / 16.0)
    crate_obj(t, k)

if __name__ == '__main__':
    unp = C.hide_static_crowd(BOXES)
    C.run('s15', 'london', 'NIGHT', F0, F1, (HANDLES_PRE, HANDLES_POST), setup, frame, segments=[(-10**6, 12), (40, 54), (68, 125)])

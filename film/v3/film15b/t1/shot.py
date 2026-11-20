#!/usr/bin/env python3
"""film 15 v2 remake, take T1 (0.00-16.30 s, g 0-489 (+6 handle), location A Medford 1963, BIGZOOM 1 0.0-4.4 s).
usage: python3 shot.py <draft|final> <g_from> <g_to> [step]    -> frames/g_%04d.png (draft: 360x640, 6 spl; final 720x1280, 12 spl)
One continuous camera path (Hermite through waypoints, ease in/out), cards rebuilt every frame (grounded, rim lit, cast shadow).
Beats (s): boy straddle 0.8-2.3 | Dick flops 4.45-6.2 | 2 boys straddle 8.0 / 9.6 | Dick straddles 12.4-13.3, bar falls 13.3 (g 399) | clean flop 15.2-16.1."""
import sys, os, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
SET = os.path.join(HERE, '..', '..', 'set3d15'); sys.path.insert(0, os.path.abspath(SET))
import numpy as np
import v2_a as V, v2_a_shots as SHT
from v2_a import F, STATE, U, DM
import bpy
from mathutils import Vector
import cast15

Q = sys.argv[1] if len(sys.argv) > 1 else 'draft'
G0 = int(sys.argv[2]) if len(sys.argv) > 2 else 0
G1 = int(sys.argv[3]) if len(sys.argv) > 3 else 495
STEP = int(sys.argv[4]) if len(sys.argv) > 4 else 1
OUT = os.path.join(HERE, 'frames_' + Q); os.makedirs(OUT, exist_ok=True)
FPS = 30.0

# ----------------------------------------------------------------------------- camera path (metres)
def hermite(pts, t):
    """pts = [(t, (x,y,z)), ...]; cubic Hermite, Catmull-Rom tangents, zero tangent at both ends (ease in/out)."""
    ts = [p[0] for p in pts]; vs = [np.array(p[1], float) for p in pts]
    t = min(max(t, ts[0]), ts[-1] - 1e-9)
    i = max(k for k in range(len(ts) - 1) if ts[k] <= t)
    def m(k):
        if k <= 0 or k >= len(ts) - 1: return np.zeros(3)
        return (vs[k + 1] - vs[k - 1]) / (ts[k + 1] - ts[k - 1])
    h = ts[i + 1] - ts[i]; u = (t - ts[i]) / h; u2 = u * u; u3 = u2 * u
    return (2 * u3 - 3 * u2 + 1) * vs[i] + (u3 - 2 * u2 + u) * h * m(i) + (-2 * u3 + 3 * u2) * vs[i + 1] + (u3 - u2) * h * m(i + 1)

# after BIGZOOM (the BZ1 path ends at rest at (4.6,-3.9,1.3)): low hero push, crane up, side track, low straddle, orbit
CAM_LOC = [(4.4, (4.6, -3.9, 1.3)), (5.2, (2.2, -2.6, 0.75)), (6.1, (-3.0, 2.0, 0.6)), (7.6, (-5.0, -2.5, 5.2)), (9.0, (0.5, -6.0, 3.0)),
           (10.4, (7.0, -5.0, 1.7)), (11.6, (8.0, -3.6, 0.95)), (12.5, (4.2, -0.6, 0.55)), (13.3, (2.5, 1.4, 0.5)), (14.4, (1.2, 1.8, 0.8)),
           (15.4, (-0.8, 2.4, 1.0)), (16.3, (-2.4, 3.0, 1.3)), (16.5, (-2.5, 3.1, 1.35))]
CAM_LOOK = [(4.4, (5.7, -0.6, 1.2)), (5.2, (3.0, 2.0, 1.1)), (6.1, (0.0, 5.3, 1.4)), (7.6, (1.5, 3.0, 0.8)), (9.0, (5.0, 0.5, 1.2)),
            (10.4, (6.2, 0.3, 1.3)), (11.6, (4.5, 1.8, 1.3)), (12.5, (0.6, 5.1, 1.3)), (13.3, (0.0, 5.3, 1.4)), (14.4, (0.5, 5.0, 1.3)),
            (15.4, (0.6, 5.0, 1.6)), (16.3, (0.3, 5.5, 1.5)), (16.5, (0.3, 5.5, 1.5))]

def cam_at(t):
    if t <= 4.4: return SHT.bigzoom1_path(t)
    return tuple(hermite(CAM_LOC, t)), tuple(hermite(CAM_LOOK, t))

# ----------------------------------------------------------------------------- world facts
M = STATE['marks_m'] if STATE.get('marks_m') else None
BARY, BARX = 5.3, 0.0; HBAR = 1.72; PIT = 0.47
RUN = [(5.6, -0.8), (4.3, 1.5), (2.9, 3.0), (1.6, 3.9), (1.15, 4.25)]
def polyline(pts):
    L = [0.0]
    for a, b in zip(pts, pts[1:]): L.append(L[-1] + math.dist(a, b))
    return L
RUNL = polyline(RUN)
def along(pts, L, s):
    s = min(max(s, 0.0), L[-1] - 1e-9)
    for k in range(len(pts) - 1):
        if L[k] <= s <= L[k + 1]:
            u = (s - L[k]) / (L[k + 1] - L[k]); return (pts[k][0] + u * (pts[k + 1][0] - pts[k][0]), pts[k][1] + u * (pts[k + 1][1] - pts[k][1]))
    return pts[-1]
def lerp(a, b, u): return a + (b - a) * u
def sm(u): u = min(max(u, 0.0), 1.0); return u * u * (3 - 2 * u)
def keyed(table, t):
    """piecewise-linear table [(t, v), ...]"""
    if t <= table[0][0]: return table[0][1]
    for (t0, v0), (t1, v1) in zip(table, table[1:]):
        if t <= t1: return lerp(v0, v1, (t - t0) / (t1 - t0))
    return table[-1][1]

class Ctx: pass
C = Ctx()   # per-frame: camera right vector, camera loc (m)

def facing_for(dx, dy):
    r = C.right; v = dx * r[0] + dy * r[1]
    return 1 if v > 0 else -1

PO = lambda name, cast, facing=1, **ov: dict(cast15.pose_for(name, cast, facing=facing), **ov)

# ----------------------------------------------------------------------------- actor timelines. Each returns None (not drawn) or a spec dict:
#   kind 'stand': xy (m), pose, z None -> surface  |  'anchor': anchor name, world (x,y,z m), zg (m) shadow plane  | canvas wide for lying/air
def spec_stand(cast, pose, xy, z=None, contact=(1.5, 0.55)): return dict(kind='stand', cast=cast, pose=pose, xy=xy, z=z, contact=contact)
def spec_anchor(cast, pose, anchor, wp, zg): return dict(kind='anchor', cast=cast, pose=pose, anchor=anchor, wp=wp, zg=zg)

def idle_rock(cast, t, xy, face_xy, ph=0.0):
    f = facing_for(face_xy[0] - xy[0], face_xy[1] - xy[1]); nm = 'rock_a' if int((t + ph) * 3.75) % 2 == 0 else 'rock_b'
    return spec_stand(cast, PO(nm, cast, f), xy)

def jumper(cast, t, ts, style, start, jog_in=1.0, side=-1):
    """one jump: runs the curve [start -> takeoff] during [ts - jog_in, ts], airborne ts .. ts+0.8 (bar crossing at ts+0.47), lands in the pit, sits up, returns nothing after ts+2.0 (caller)."""
    tc = ts + 0.47
    x0, y0 = 1.15, 4.25
    if t < ts - jog_in: return None
    if t < ts:                                    # run along the (remaining) curve
        pts = [start] + [p for p in RUN if p[1] > start[1] + 0.2][0:] if start != RUN[0] else RUN
        L = polyline(pts); u = (t - (ts - jog_in)) / jog_in; s = L[-1] * (u ** 1.25)
        xy = along(pts, L, s); dx, dy = (RUN[-1][0] - xy[0], RUN[-1][1] - xy[1]); f = facing_for(dx, dy)
        pose = cast15.run_curved(cast, s / 3.0, facing=f); return spec_stand(cast, pose, xy)
    if style == 'flop':
        # (t, y, anchor z m): the 'bar' anchor passes the bar plane (y 5.3) at height 1.70 at tc
        Y = [(ts, 4.25), (tc, 5.3), (ts + 0.80, 6.75)]
        y = keyed(Y, t); x = lerp(1.15, -0.55, sm((t - ts) / 0.8))
        stages = [(0.0, 'takeoff'), (0.10, 'flop_rise'), (0.26, 'flop_head'), (0.36, 'flop_back'), (0.46, 'flop'), (0.62, 'flop_flick'), (0.80, None)]
        w = t - ts; nm = None
        for tt, n in stages:
            if w >= tt: nm = n
        Z = [(0.0, 0.0), (0.10, 0.35), (0.26, 1.28), (0.36, 1.60), (0.47, 1.70), (0.62, 1.50), (0.78, 1.10)]
        z = keyed(Z, w)
        if nm == 'takeoff': return spec_stand(cast, PO('takeoff', cast, -1), (x, y), z=None)
        if nm == 'flop_rise': return spec_anchor(cast, PO('flop_rise', cast, -1), 'feet', (x, y, z), PIT)
        if nm is None: return None
        return spec_anchor(cast, PO(nm, cast, -1), 'bar', (x, y, z), PIT)
    else:                                         # straddle (roll face down over the bar)
        Y = [(ts, 4.25), (tc, 5.3), (ts + 0.80, 6.6)]
        y = keyed(Y, t); x = lerp(1.15, -0.1, sm((t - ts) / 0.8)); w = t - ts
        nm = 'takeoff' if w < 0.12 else ('straddle_a' if int(w * 7) % 2 == 0 or w > 0.45 else 'straddle_b') if w < 0.78 else None
        z = keyed([(0.0, 0.0), (0.12, 0.45), (0.30, 1.30), (0.47, 1.80), (0.65, 1.30), (0.78, 0.75)], w)
        if nm == 'takeoff': return spec_stand(cast, PO('takeoff', cast, -1), (x, y), z=None)
        if nm is None: return None
        return spec_anchor(cast, PO(nm, cast, -1), 'bar', (x, y, z), PIT)

def after_landing(cast, t, tl, pit_xy, then_xy=None, up=1.0):
    """t >= tl: lies in the pit (land_back), sits up, then stands (returns spec) ."""
    w = t - tl
    if w < 0.35: return spec_anchor(cast, PO('land_back', cast, -1), 'head', (pit_xy[0], pit_xy[1], PIT + 0.30), PIT)
    if w < 0.35 + 0.6 * up: return spec_stand(cast, PO('sit_up', cast, -1), pit_xy, z=PIT, contact=(2.2, 0.8))
    return spec_stand(cast, PO('stand', cast, -1), pit_xy, z=PIT)

def dick(t):
    c = 'dick'; mark = RUN[0]
    if t < 4.45: return idle_rock(c, t, mark, (BARX, BARY))
    # --- clean flop 1
    if t < 5.45: return jumper(c, t, 5.45, 'flop', RUN[0], jog_in=1.0)
    if t < 6.25: return jumper(c, t, 5.45, 'flop', RUN[0])
    if t < 7.7: return after_landing(c, t, 6.25, (-0.7, 7.05))
    # --- jog back to the mark 7.7 - 11.4 (pit -> run-up start)
    if t < 11.4:
        back = [(-0.7, 7.05), (-2.2, 5.6), (-1.3, 3.2), (1.6, 3.9), (4.3, 1.5), (5.6, -0.8)]
        Lb = polyline(back); u = (t - 7.7) / 3.7; s = Lb[-1] * sm(u) if u < 1 else Lb[-1]; xy = along(back, Lb, s)
        xy2 = along(back, Lb, min(s + 0.3, Lb[-1])); f = facing_for(xy2[0] - xy[0], xy2[1] - xy[1])
        moving = u < 1 and u > 0.0
        pose = cast15.run_curved(c, s / 1.7, facing=f) if moving and s < Lb[-1] - 0.05 else PO('stand', c, f)
        return spec_stand(c, pose, xy)
    if t < 11.55: return idle_rock(c, t, mark, (BARX, BARY))
    # --- straddle try: runs, knocks the bar at 13.3 (g 399)
    if t < 12.45: return jumper(c, t, 12.45, 'straddle', RUN[0], jog_in=0.9)
    if t < 13.2: return jumper(c, t, 12.45, 'straddle', RUN[0])
    if t < 13.62: return spec_anchor(c, PO('knock', c, -1), 'head', (-0.25, 6.7, lerp(1.3, PIT + 0.3, sm((t - 13.2) / 0.4))), PIT)
    if t < 14.05: return spec_anchor(c, PO('lie_hands_face', c, -1), 'head', (-0.5, 7.0, PIT + 0.28), PIT)
    # --- he jumps up and jogs round to the curve (turns his back, run-in 2.3 m) 14.05 - 15.1
    if t < 15.15:
        back = [(-0.5, 7.0), (-1.9, 5.0), (0.0, 3.0), (2.9, 3.0)]
        Lb = polyline(back); u = (t - 14.05) / 1.05; s = Lb[-1] * sm(u); xy = along(back, Lb, s)
        xy2 = along(back, Lb, min(s + 0.3, Lb[-1])); f = facing_for(xy2[0] - xy[0], xy2[1] - xy[1])
        return spec_stand(c, cast15.run_curved(c, s / 1.6, facing=f), xy)
    if t < 15.62: return jumper_curve_short(c, t, 15.62)
    if t < 16.45: return jumper(c, t, 15.62, 'flop', RUN[0])
    return after_landing(c, t, 16.45, (-0.7, 7.05))

def jumper_curve_short(c, t, ts):
    pts = RUN[2:]; L = polyline(pts); u = (t - 15.15) / (ts - 15.15); s = L[-1] * (u ** 1.2); xy = along(pts, L, s)
    f = facing_for(pts[-1][0] - xy[0], pts[-1][1] - xy[1]); return spec_stand(c, cast15.run_curved(c, s / 3.0, facing=f), xy)

def boy_waiter(cast, t, xy, ph=0.0, pose='rock_b'):
    f = facing_for(BARX - xy[0], BARY - xy[1])
    if pose == 'laugh': return spec_stand(cast, dict(PO('laugh', cast, f), bob=cast15.laugh_bob(int(t * 30) + int(ph * 30))), xy)
    nm = 'rock_a' if int((t + ph) * 3.75) % 2 == 0 else 'rock_b'
    return spec_stand(cast, PO(nm, cast, f), xy)

def boy3(t):
    c = 'boy3'; wait = M['boy_c'][:2]
    # 0.0 - 2.4: straddle roll seen small in the BIGZOOM (starts mid-run on the curve)
    if t < 0.75: return jumper(c, t, 0.75, 'straddle', (3.4, 2.4), jog_in=0.75) if t > 0 else jumper(c, 0.0, 0.75, 'straddle', (3.4, 2.4), jog_in=0.75)
    if t < 1.55: return jumper(c, t, 0.75, 'straddle', (3.4, 2.4))
    if t < 3.6: return after_landing(c, t, 1.55, (0.4, 7.2), up=2.0)
    if t < 5.0: return spec_stand(c, PO('laugh', c, -1, bob=cast15.laugh_bob(int(t * 30))), (0.4, 7.2), z=PIT)
    return spec_stand(c, dict(PO('point_laugh', c, -1), bob=cast15.laugh_bob(int(t * 30))), (0.4, 7.2), z=PIT) if t < 7.5 else \
           spec_stand(c, dict(PO('laugh', c, -1), bob=cast15.laugh_bob(int(t * 30))), (-1.8, 6.8), z=PIT)

def boy1(t):
    c = 'boy1'; w = M['boy_wait_a'][:2]
    if t < 7.0: return boy_waiter(c, t, w, 0.1)
    if t < 8.0: return jumper(c, t, 8.0, 'straddle', RUN[1], jog_in=0.9) if t > 7.1 else boy_waiter(c, t, w, 0.1)
    if t < 8.8: return jumper(c, t, 8.0, 'straddle', RUN[1])
    if t < 10.8: return after_landing(c, t, 8.8, (0.6, 7.3), up=1.5)
    return spec_stand(c, dict(PO('laugh', c, -1), bob=cast15.laugh_bob(int(t * 30))), (0.6, 7.3), z=PIT)

def boy2(t):
    c = 'boy2'; w = M['boy_wait_b'][:2]
    if t < 8.6: return boy_waiter(c, t, w, 0.3)
    if t < 9.6: return jumper(c, t, 9.6, 'straddle', RUN[1], jog_in=1.0) if t > 8.65 else boy_waiter(c, t, w, 0.3)
    if t < 10.4: return jumper(c, t, 9.6, 'straddle', RUN[1])
    if t < 12.6: return after_landing(c, t, 10.4, (-1.5, 7.6), up=1.5)
    return spec_stand(c, dict(PO('point_laugh', c, -1), bob=cast15.laugh_bob(int(t * 30) + 4)), (-1.5, 7.6), z=PIT)

def boy3_late(t):  # boy 3 comes back to the run-up after 7.5 s as a spectator at the curve
    return None

def coach(t):
    f = facing_for(BARX - 10.4, BARY - 2.6)
    if t < 13.3: return spec_stand('coach', dict(PO('clip', 'coach', f), bob=0.025 * math.sin(t * 5.0)), M['coach_bleacher'][:2], contact=(1.9, 0.6))
    return spec_stand('coach', dict(PO('coach_laugh', 'coach', f), bob=cast15.laugh_bob(int(t * 30))), M['coach_bleacher'][:2], contact=(1.9, 0.6))

def boy3_idle(t):
    return None

ACTORS = [('c_dick', dick), ('c_b3', boy3), ('c_b1', boy1), ('c_b2', boy2), ('c_coach', coach)]

# ----------------------------------------------------------------------------- scene build, per-frame cards
_prev = []
def clear_cards():
    global _prev
    objs = [bpy.data.objects[n] for n in _prev if n in bpy.data.objects]
    meshes = [o.data for o in objs if o.type == 'MESH']; mats = []
    for me in meshes: mats += [m for m in me.materials if m]
    imgs = []
    for m in mats:
        if m.use_nodes: imgs += [n.image for n in m.node_tree.nodes if n.bl_idname == 'ShaderNodeTexImage' and n.image]
    for o in objs: bpy.data.objects.remove(o, do_unlink=True)
    for me in meshes:
        if me.users == 0: bpy.data.meshes.remove(me)
    for m in mats:
        if m.users == 0: bpy.data.materials.remove(m)
    for im in imgs:
        if im.users == 0: bpy.data.images.remove(im)
    _prev = []

_ZC = {}
def surf(x, y):
    k = (round(x * 8), round(y * 8))
    if k not in _ZC: _ZC[k] = V.surface_z(x * U, y * U) * DM
    return _ZC[k]

def ppd_for(dist_m):
    need = 1.25 * 422.0 / max(dist_m, 0.5)
    for p in (48, 64, 96, 128, 160, 192):
        if p >= need: return p
    return 192

def place(tag, spec, cam_D, cam_m, t):
    cast = spec['cast']; pose = spec['pose']
    if spec['kind'] == 'stand':
        x, y = spec['xy']; z = spec['z'] if spec['z'] is not None else surf(x, y)
        d = math.dist((x, y, z + 1.0), cam_m); ppd = ppd_for(d)
        try: return V.ground_card(tag, cast, pose, (x * U, y * U), cam_D, z=z * U, ppd=ppd, contact=spec.get('contact', (1.5, 0.55)))
        except AssertionError: return V.ground_card(tag, cast, pose, (x * U, y * U), cam_D, z=z * U, ppd=ppd, contact=spec.get('contact', (1.5, 0.55)), canvas=cast15.CANVAS15_WIDE)
    x, y, z = spec['wp']; d = math.dist((x, y, z), cam_m); ppd = ppd_for(d)
    wp = Vector((x * U, y * U, z * U)); tc = Vector(cam_D) - wp; tc.z = 0
    if tc.length > 1e-4: wp += tc.normalized() * 0.3        # the card stands a little in front of the bar line
    return V.ground_card_anchor(tag, cast, pose, (spec['anchor'], tuple(wp)), cam_D, spec['zg'] * U, ppd=ppd, canvas=cast15.CANVAS15_WIDE)

SPOT = None
FLECKS = []
def build_scene():
    global M, SPOT
    A = V.build_a2('HERO', rays=False)
    M = STATE['marks_m']
    sc = bpy.context.scene
    F.setup_render(sc, 'final' if Q == 'final' else 'preview'); sc.cycles.samples = 12 if Q == 'final' else 6
    V.set_grade_sat(sc, 1.28); V.CT()
    loc, look = cam_at(0.0); cam = F.make_camera(F.cam_from(tuple(c * U for c in loc), tuple(c * U for c in look), lens=22.0))
    SPOT = V.spot(5.6, -0.4, r=5.0, k=0.55)
    # sawdust bursts at the landings (small flecks): Dick 6.3, boy 1.6, boys 8.9 / 10.5, Dick 13.45, Dick 16.5
    for i, (tt, xy) in enumerate(((1.6, (0.4, 7.2)), (6.3, (-0.7, 7.05)), (8.85, (0.6, 7.3)), (10.45, (-1.5, 7.6)), (13.5, (-0.5, 7.0)))):
        FLECKS.append((int(tt * 30), V.sawdust_flecks(int(tt * 30), (xy[0] * U, xy[1] * U, PIT * U), strength=0.8, seed=i, floor=PIT * U)))
    # bar: falls at g 399, then is lifted back onto the pegs 14.0-14.8
    F.bar_fall(399, side='back', bounce=True, seed=3)
    return cam, sc

def bar_lift(sc, f):
    """after the fall the bar is carried back to the pegs 14.05-14.85 (eased)"""
    J = STATE['J']; bar = J['bar']
    t = f / FPS
    if t < 14.0: return
    # rest pose from the last fall key
    if not hasattr(bar_lift, 'rest'):
        sc.frame_set(int(14.0 * 30)); bar_lift.rest = (bar.location.copy(), bar.rotation_euler.copy())
    r_loc, r_rot = bar_lift.rest
    u = sm((t - 14.05) / 0.8); tgt = Vector((J['xc'], J['y'], HBAR - 0.02)); arc = math.sin(u * math.pi) * 0.35
    bar.location = Vector(r_loc).lerp(tgt, u) + Vector((0, 0, arc)); bar.rotation_euler = tuple(lerp(a, 0.0, u) for a in r_rot)

def exposure_at(t):
    return keyed([(0, -0.8), (3.0, -0.85), (4.4, -1.0), (6.0, -1.15), (16.5, -1.15)], t)

def render_frame(g, cam, sc):
    t = g / FPS
    loc, look = cam_at(t); locD = Vector(loc) * U; lookD = Vector(look) * U
    cam.location = locD; cam.rotation_euler = (lookD - locD).to_track_quat('-Z', 'Y').to_euler()
    fwd = (lookD - locD).normalized(); right = fwd.cross(Vector((0, 0, 1))).normalized(); up = right.cross(fwd).normalized()
    C.right = (right.x, right.y); C.loc = loc
    sc.frame_set(g)
    if g >= 399 and t >= 14.0: bar_lift(sc, g)
    SPOT.hide_render = t > 2.3
    for f0, ob in FLECKS: ob.hide_render = not (f0 - 1 <= g <= f0 + 24)
    sc.view_settings.exposure = exposure_at(t)
    kd = Vector(STATE['P']['key_dir']); tl = -kd
    V.rim_on(to_light=(tl.dot(right), -tl.dot(up)), width=5, strength=0.9)
    clear_cards(); before = set(bpy.data.objects.keys()); cdD = tuple(locD)
    for tag, fn in ACTORS:
        sp = fn(t)
        if sp is None: continue
        place(tag, sp, cdD, loc, t)
    _prev.extend(set(bpy.data.objects.keys()) - before)
    out = os.path.join(OUT, 'g_%04d.png' % g)
    wall, cpu = F.T.render(out); return wall

if __name__ == '__main__':
    t0 = time.time(); cam, sc = build_scene(); print('build %.1fs' % (time.time() - t0), flush=True)
    for g in range(G0, G1 + 1, STEP):
        w = render_frame(g, cam, sc); print('g', g, '%.1fs' % w, flush=True)

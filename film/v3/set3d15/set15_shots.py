"""Shot table of film15/shot_plan.md (36 shots): location, light, start/end camera (22 mm, D units), foreground props, placeholder staging.
Authoring is in METRES (loc, look); move = push %/s (+ in, - out), slide px/s at 720 wide (+ right), rise m/s, orbit deg/s about the look point."""
import math
import numpy as np
import bpy
from mathutils import Vector, Matrix, Euler
import set15 as F
import set15_lib as L
from set15_lib import S, U, DM, STATE, mat

HFOV_T = math.tan(math.radians(24.5))      # half horizontal field of view of the 22 mm / 36 mm portrait frame

def _cam_pair(loc, look, push=0.0, slide=0.0, rise=0.0, orbit=0.0, dur=1.5, end=None, punch=None):
    """start and end camera of a shot (metres). The end is computed from the planned move unless given."""
    loc = Vector(loc); look = Vector(look); fwd = look - loc; d = fwd.length; fwd_n = fwd / d
    right = fwd_n.cross(Vector((0, 0, 1))); right = right.normalized() if right.length > 1e-6 else Vector((1, 0, 0))
    if end is not None: return dict(loc=tuple(loc), look=tuple(look)), dict(loc=tuple(end[0]), look=tuple(end[1]))
    k = max(-0.6, min(0.6, push / 100.0 * dur)); sw = slide / 720.0 * (2 * d * HFOV_T) * dur
    l2 = loc + fwd * k + right * sw + Vector((0, 0, rise * dur)); t2 = look + right * sw + Vector((0, 0, rise * dur))
    if orbit:
        a = math.radians(orbit * dur); off = l2 - look; c, s_ = math.cos(a), math.sin(a)
        l2 = look + Vector((off.x * c - off.y * s_, off.x * s_ + off.y * c, off.z)); t2 = look
    return dict(loc=tuple(loc), look=tuple(look)), dict(loc=tuple(l2), look=tuple(t2))

def shot(n, t0, t1, loc_, lt, cam, fg, actors, note, trans='cut', **mv):
    a, b = _cam_pair(cam[0], cam[1], dur=t1 - t0, **{k: v for k, v in mv.items() if k in ('push', 'slide', 'rise', 'orbit', 'end')})
    F.SHOTS[n] = dict(n=n, t0=t0, t1=t1, loc=loc_, light=lt, a=a, b=b, fg=fg, actors=actors, note=note, trans=trans, punch=mv.get('punch'), whip=mv.get('whip', False), move={k: v for k, v in mv.items() if k != 'end'})

A, B = 'A', 'B'
# ------------------------------------------------------------------ Location A (GOLDEN unless noted)
shot(1, 0.00, 2.10, A, 'GOLDEN', ((-5.6, -4.4, 1.45), (1.2, 5.2, 1.1)), [('hurdle', 1.0, -0.35, 0.5)], [('boy', (0.2, 6.6, 0.44)), ('boy', 'boy_wait_a'), ('boy', 'boy_wait_b')], 'wide 3/4 on the pit; boy straddle-rolls over the bar; two boys wait', push=8, slide=40)
shot(2, 2.10, 3.60, A, 'GOLDEN', ((3.0, -3.0, 0.75), (5.6, -0.8, 1.55)), [('cone', 1.0, 0.4, 0.0)], [('dick', 'dick_mark'), ('boy', 'boy_wait_a'), ('boy', 'boy_c')], 'low medium on Dick at his mark', push=8, slide=20, punch=(2.9, 18))
shot(3, 3.60, 4.45, A, 'GOLDEN', ((-1.2, -2.4, 1.25), (6.0, -3.0, 1.1)), [('bench_end', 1.0, 0.45, 0.4)], [('dick', 'runup_start'), ('boy', 'boy_wait_a')], 'WHIP follow pan along the curved run', end=((-1.2, -2.4, 1.25), (1.0, 4.4, 1.2)), whip=True)
shot(4, 4.45, 6.15, A, 'GOLDEN', ((-0.4, 2.1, 0.32), (0.0, 5.3, 2.1)), [('standard_base', 0.9, -0.5, 0.0)], [('dick', 'landing'), ('boy', 'boy_wait_a'), ('boy', 'boy_wait_b')], 'low at the bar, looking up; Dick flops backwards', push=10)
shot(5, 6.15, 8.20, A, 'GOLDEN', ((-6.4, -5.2, 3.0), (4.5, 13.0, 2.6)), [('pine_branch', 0.9, 0.5, 0.35)], [('coach', 'coach_bleacher'), ('boy', 'boys_bench_a'), ('boy', 'boys_bench_b')], 'high wide pull-back crane, establishing', trans='DIS', push=-8, rise=0.35)
shot(6, 8.20, 11.45, A, 'GOLDEN', ((5.6, 1.0, 1.15), (-0.2, 5.6, 1.2)), [('rake', 0.9, 0.35, 0.4)], [('boy', 'runup_start'), ('boy', 'boy_wait_b'), ('boy', 'takeoff')], 'side medium, slide left; straddle rolls', push=6, slide=-40)
shot(7, 11.45, 13.25, A, 'GOLDEN', ((-3.8, 0.0, 1.2), (0.5, 5.6, 1.3)), [('cooler', 1.0, 0.45, 0.4)], [('dick', 'takeoff'), ('boy', 'boy_wait_a')], '3/4 medium; Dick knocks the bar', push=8, punch=(13.3, 15))
shot(8, 13.25, 14.15, A, 'GOLDEN', ((-1.9, 4.0, 0.95), (-0.5, 7.4, 0.8)), [('sawdust_edge', 0.9, -0.45, 0.0)], [('dick', 'landing')], 'close-medium; bar bounces, Dick sits up sheepish', push=6, slide=40)
shot(9, 14.15, 16.30, A, 'GOLDEN', ((-4.2, 0.6, 3.7), (0.0, 5.3, 1.2)), [('bar_end', 0.9, 0.55, 0.0)], [('dick', 'takeoff'), ('boy', 'boy_wait_a')], 'high angle orbit 15 deg/s; clean flop', orbit=15)
shot(10, 16.30, 18.80, A, 'GOLDEN', ((6.3, -0.4, 1.5), (10.4, 2.6, 1.55)), [('clipboard', 0.9, -0.3, 0.2)], [('coach', 'coach_bleacher')], 'medium on the coach; belly bounce', push=8)
shot(11, 18.80, 20.70, A, 'GOLDEN', ((11.7, 3.6, 1.75), (5.0, -0.4, 1.4)), [('shoulder', 0.8, 0.5, 0.0)], [('coach', 'coach_bleacher'), ('dick', 'dick_mark'), ('boy', 'boy_wait_a'), ('boy', 'boy_wait_b')], 'over-shoulder of the coach onto Dick', slide=40)
shot(12, 20.70, 23.60, A, 'GOLDEN', ((7.0, 1.0, 1.55), (10.4, 2.6, 1.6)), [('stopwatch', 0.8, 0.25, -0.2)], [('coach', 'coach_bleacher')], 'medium-close, finger wag', push=8, punch=(23.0, 20))
shot(13, 23.60, 25.40, A, 'GOLDEN', ((-6.6, 2.2, 0.5), (-0.3, 6.4, 1.3)), [('camera_bag', 0.9, 0.4, 0.5)], [('photographer', 'photographer'), ('dick', 'landing')], 'low wide by the pit; FLASH at 24.6', slide=40, push=6)
shot(14, 25.40, 27.95, A, 'GOLDEN', ((10.7, 3.0, 1.55), (12.6, 4.4, 1.2)), [('thumb', 0.7, 0.3, -0.2)], [('reader', 'reader')], 'newspaper insert on the bleacher', push=10, slide=30)
shot(15, 27.95, 28.73, A, 'GOLDEN', ((8.8, 0.6, 1.15), (4.2, 2.6, 1.6)), [('rail', 0.9, -0.1, 0.0)], [('coach', 'coach_bleacher'), ('boy', 'boy_wait_a'), ('boy', 'boy_wait_b'), ('dick', 'takeoff')], 'PUSH! snap; everyone points and laughs', push=25)
shot(16, 28.73, 31.05, A, 'GOLDEN', ((-4.6, 2.2, 1.5), (0.4, 5.4, 1.5)), [('hurdle_stack', 1.0, -0.4, 0.4)], [('dick', 'takeoff'), ('boy', 'boy_c')], 'orbit + push; training; GOLDEN -> DAY (render both lights)', trans='DIS', orbit=10, push=6)
shot(34, 64.62, 66.25, A, 'GOLDEN', ((-0.6, -1.8, 1.3), (-4.4, 5.0, 1.45)), [('bench_end', 0.9, -0.4, 0.4)], [('coach', 'coach_end'), ('boy', 'boys_bench_a'), ('boy', 'boys_bench_b'), ('boy', 'boys_bench_c')], 'back at the school track; coach at the sawdust pit, boys on the bench', trans='DIS', push=8)
shot(35, 66.25, 68.00, A, 'GOLDEN', ((-0.8, -2.6, 1.2), (6.0, -3.0, 1.1)), [('hurdle', 0.9, 0.4, 0.8)], [('coach', 'runup_start'), ('boy', 'boys_bench_a')], 'WHIP follow; the coach runs the curve', end=((-0.8, -2.6, 1.2), (0.0, 5.0, 1.3)), whip=True)
shot(36, 68.00, 69.84, A, 'GOLDEN', ((-3.4, 3.5, 0.5), (-4.1, 6.9, 0.95)), [('sawdust_chips', 0.8, 0.0, 0.0)], [('coach', 'coach_end'), ('boy', 'boys_bench_a'), ('boy', 'boys_bench_b')], 'low at the pit; TUMP in the pile', push=8, punch=(68.6, 18))
# ------------------------------------------------------------------ Location B
shot(17, 31.05, 32.50, B, 'EVE', ((7.0, 0.5, 3.4), (-2.0, 24.0, 9.0)), [('flagpole', 1.2, -0.5, 0.0)], [('dick', 'dick_mark')], 'grand wide push-in, rise; the packed stadium', trans='DIS', push=8, rise=0.5)
shot(18, 32.50, 33.80, B, 'EVE', ((3.4, 8.4, 0.9), (0.0, 11.6, 1.7)), [('standard', 0.9, 0.4, 0.0)], [('official', 'official_bar_l'), ('official', 'official_bar_r')], 'tilt up following the bar', end=((3.4, 8.4, 0.9), (0.0, 11.6, 3.4)))
shot(19, 33.80, 35.27, B, 'EVE', ((7.6, 6.2, 1.3), (0.8, 11.4, 1.5)), [('table_corner', 0.9, -0.4, 0.0)], [('rival', 'rival_land'), ('official', 'official_a')], '3/4 medium; rival knocks the bar', slide=40)
shot(20, 35.27, 37.50, B, 'EVE', ((-3.7, 7.6, 0.5), (-2.7, 9.3, 1.85)), [('standard_peg', 0.9, 0.4, 0.0)], [('dick', 'dick_b2')], 'low tilt-up from Dick head to the bar', end=((-3.7, 7.6, 0.5), (0.0, 11.6, 3.0)))
shot(21, 37.50, 38.35, B, 'EVE', ((4.2, 8.0, 0.9), (6.0, 3.0, 1.0)), [('foam_edge', 0.9, -0.4, 0.0)], [('dick', 'runup_start')], 'WHIP; attempt 1, the bar falls', end=((4.2, 8.0, 0.9), (0.0, 12.0, 2.3)), whip=True)
shot(22, 38.35, 39.65, B, 'EVE', ((0.4, 20.2, 1.5), (-0.5, 14.0, 1.1)), [('bar_on_mat', 0.9, 0.0, 0.0)], [('dick', 'rival_land')], 'reverse angle; Dick lies on the foam', push=8)
shot(23, 39.65, 42.30, B, 'EVE', ((-6.6, 21.4, 3.9), (-9.0, 31.0, 5.9)), [('shoulder', 0.8, 0.5, 0.0)], [('coach', 'coach_stands')], 'medium in the stands; the coach jumps up and shouts', push=8, punch=(41.7, 18))
shot(24, 42.30, 44.30, B, 'TENSE', ((1.0, 5.4, 1.2), (5.8, 8.2, 1.9)), [('bar_end', 0.9, 0.5, 0.0)], [('dick', 'dick_mark')], 'slow push; the stadium hushed', push=6, slide=40)
shot(25, 44.30, 46.40, B, 'TENSE', ((-3.4, 9.6, 0.5), (0.6, 13.0, 3.6)), [('foam_edge', 0.9, 0.45, 0.0)], [('dick', 'takeoff')], 'low at the bar; run, plant and rise', push=8)
shot(26, 46.40, 49.00, B, 'TENSE', ((-5.6, 8.8, 2.0), (-0.6, 11.7, 2.3)), [('standard', 0.9, -0.4, 0.0)], [('dick', 'landing')], 'lateral track along the bar; part by part', slide=-40, push=6)
shot(27, 49.00, 50.35, B, 'TENSE', ((-5.6, 9.2, 2.3), (0.0, 11.6, 2.25)), [('crossbar_end', 0.9, 0.2, 0.0)], [('dick', 'bar_centre')], 'KEY IMAGE: side view at bar height', push=8)
shot(28, 50.35, 52.85, B, 'EVE', ((-5.8, 9.0, 2.4), (0.0, 11.6, 2.35)), [('standard', 0.9, -0.45, 0.0)], [('rival', 'bar_centre')], 'contrast: straddle rival lifted high above the bar', trans='DIS', slide=30)
shot(29, 52.85, 55.08, B, 'TENSE', ((-5.6, 9.2, 2.6), (0.0, 11.6, 2.2)), [('foam_edge', 0.9, -0.4, 0.0)], [('dick', 'bar_centre')], 'back to the side view, WHIP down', trans='DIS', end=((-5.6, 9.2, 2.6), (0.2, 13.8, 1.0)), whip=True)
shot(30, 55.08, 58.20, B, 'TENSE', ((-1.4, 10.2, 2.4), (0.2, 11.6, 2.24)), [('bar_peg', 0.9, 0.35, 0.0)], [('dick', 'rival_land')], 'close of the bar, push; light pops to EVE at 56.6', push=8)
shot(31, 58.20, 60.15, B, 'EVE', ((-3.0, -0.6, 1.5), (-8.0, 14.0, 5.0)), [('flagpole', 1.2, 0.5, 0.0)], [('dick', 'podium_top'), ('official', 'podium_2'), ('rival', 'podium_3')], 'wide; stadium erupts; Dick on the podium', push=8, punch=(59.1, 20))
shot(32, 60.15, 62.50, B, 'DAY', ((-6.2, 8.6, 1.5), (0.0, 12.2, 2.0)), [('standard', 0.9, -0.4, 0.0)], [('rival', 'takeoff'), ('rival', 'rival_a')], 'four years later; jumpers flop', trans='DIS', slide=40, push=6)
shot(33, 62.50, 64.62, B, 'DAY', ((-6.6, 13.2, 0.6), (0.0, 15.0, 1.5)), [('foam_edge', 0.9, -0.4, 0.0)], [('rival', 'rival_land'), ('rival', (-1.6, 15.8, 1.0))], 'jumpers land on the foam, sit up smiling', push=8)

# ------------------------------------------------------------------ foreground props (camera relative, 1-2 D = 0.6-1.2 m from the lens)
def fg_build(kind, p, yaw, M, cam_h):
    mb = S.MB('fg_' + kind); x, y, z = p; lensz = cam_h
    if kind == 'hurdle': S.hurdle(mb, M, (x, y, z), yaw)
    elif kind == 'cone': S.cone_t(mb, M, (x, y, z))
    elif kind == 'bench_end': S.bench(mb, M, (x, y, z), yaw, 1.8)
    elif kind == 'standard_base': mb.box(M['wood'], (x, y, 1.0), (0.1, 0.1, 2.0)); mb.box(M['woodpale'], (x, y, 0.04), (0.55, 1.0, 0.08)); mb.box(M['woodpale'], (x, y - 0.1, 0.12), (0.14, 0.8, 0.1))
    elif kind == 'pine_branch': import set15_props as PR; PR.pine_branch(mb, M, (x, y, z + 1.5), (math.cos(yaw), math.sin(yaw), 0.0), 31)
    elif kind == 'rake': S.rake(mb, M, (x, y, 0.0), (x + 0.3, y + 0.1, 1.1))
    elif kind == 'cooler': S.cooler(mb, M, (x, y, z)); S.bag(mb, M, (x + 0.5, y, z), yaw, 'blue', 0.7)
    elif kind == 'sawdust_edge':
        mb.box(M['wood'], (x, y, 0.21), (1.6, 0.12, 0.42)); mb.box(M['woodpale'], (x, y, 0.44), (1.7, 0.2, 0.04)); mb.ell(M['saw'], (x, y + 0.5, 0.4), (0.9, 0.5, 0.1), (10, 5))
    elif kind == 'bar_end':
        mb.box(M['wood'], (x, y, 1.4), (0.1, 0.1, 2.8)); mb.box(M['yellow'], (x - 0.3, y, 1.4), (0.2, 0.17, 0.035))
        for i in range(8): mb.rod(M['bar'] if i % 2 == 0 else M['barr'], (x - 0.3 - i * 0.2, y, 1.46), (x - 0.5 - i * 0.2, y, 1.46), LA_BAR, LA_BAR, 8)
    elif kind == 'clipboard': import set15_props as PR; PR.clipboard(mb, M, (x, y, z + 1.0), yaw, -1.2, 1.3); mb.box(M['wood'], (x, y, 0.55), (1.2, 0.08, 0.06)); mb.box(M['wood'], (x, y, 1.1), (1.2, 0.08, 0.06))
    elif kind == 'stopwatch':
        import set15_props as PR; PR.stopwatch(mb, M, (x, y, z + 1.0), 2.4); mb.rod(M['dark'], (x, y, z + 1.0 + 0.2), (x + 0.3, y + 0.2, z + 1.9), 0.01, 0.01, 4)
    elif kind == 'camera_bag': import set15_props as PR; PR.photographer_bag(mb, M, (x, y, 0.0), yaw)
    elif kind == 'hurdle_stack': import set15_props as PR; PR.hurdle_stack(mb, M, (x, y, 0.0), yaw, 6)
    elif kind == 'rail':
        for k in range(3): mb.rod(M['steel'], (x - 0.6, y, 0.5 + 0.3 * k), (x + 0.9, y, 0.5 + 0.3 * k), 0.025, 0.025, 6)
        for sx in (-0.5, 0.2, 0.9): mb.rod(M['steel'], (x + sx, y, 0), (x + sx, y, 1.2), 0.03, 0.03, 6)
    elif kind == 'sawdust_chips':
        import random
        rr = random.Random(3)
        for i in range(60): a = rr.random() * 6.28; rd = rr.uniform(0.0, 0.7); mb.box(M['chip'], (x + math.cos(a) * rd, y + math.sin(a) * rd * 0.5, rr.uniform(0.0, 0.12)), (rr.uniform(0.05, 0.12), rr.uniform(0.02, 0.05), 0.012), rz=rr.random() * 6)
        mb.ell(M['saw'], (x, y, 0.0), (0.6, 0.35, 0.12), (10, 5))
    elif kind == 'flagpole': mb.rod(M['metal'], (x, y, 0), (x, y, 4.0), 0.05, 0.035, 6); [mb.quad(M[c], [(x, y, 3.8 - 0.3 * i), (x + 1.4 * math.cos(yaw), y + 1.4 * math.sin(yaw), 3.8 - 0.3 * i), (x + 1.4 * math.cos(yaw), y + 1.4 * math.sin(yaw), 3.5 - 0.3 * i), (x, y, 3.5 - 0.3 * i)]) for i, c in enumerate(('red', 'cream', 'blue'))]
    elif kind == 'standard':
        mb.rod(M['steel'], (x, y, 0), (x, y, 3.2), 0.04, 0.034, 8, smooth=True); mb.box(M['steel'], (x, y, 0.05), (0.6, 0.8, 0.1))
        for i in range(15): mb.box(M['metal'], (x + 0.058, y, 1.0 + i * 0.1), (0.1, 0.04, 0.03))
    elif kind == 'standard_peg':
        mb.rod(M['steel'], (x, y, 0), (x, y, 3.2), 0.04, 0.034, 8, smooth=True); mb.box(M['yellow'], (x + 0.12, y, 2.0), (0.2, 0.16, 0.035))
        for i in range(15): mb.box(M['metal'], (x + 0.058, y, 1.0 + i * 0.1), (0.1, 0.04, 0.03))
    elif kind == 'crossbar_end' or kind == 'bar_peg':
        mb.rod(M['steel'], (x, y, 0), (x, y, 3.2), 0.04, 0.034, 8, smooth=True); mb.box(M['yellow'], (x + 0.1, y, z + 1.0), (0.2, 0.16, 0.035))
        for i in range(8): mb.rod(M['bar'] if i % 2 == 0 else M['barr'], (x + 0.2 + i * 0.2, y, z + 1.0 + 0.05), (x + 0.4 + i * 0.2, y, z + 1.0 + 0.05), LA_BAR, LA_BAR, 8)
    elif kind == 'table_corner':
        import set15_props as PR; PR.table_scorer(mb, M, (x, y, 0.0), yaw)
    elif kind == 'foam_edge':
        for gx in range(2): mb.box(M['foam'] if gx % 2 else M['foamdk'], (x + gx * 1.0, y, 0.45), (1.0, 1.6, 0.9)); mb.box(M['foamtop'], (x + gx * 1.0, y, 0.95), (1.0, 1.6, 0.12))
    elif kind == 'bar_on_mat':
        for i in range(6): mb.rod(M['bar'] if i % 2 == 0 else M['barr'], (x - 1.2 + i * 0.4, y, 0.06), (x - 0.8 + i * 0.4, y + 0.1, 0.06), LA_BAR, LA_BAR, 8)
        mb.box(M['foamtop'], (x, y + 0.2, -0.05), (3.0, 1.6, 0.12))
    elif kind in ('shoulder', 'thumb'): return []      # cast pieces (the coach's / spectator's shoulder, the reader's thumb): the stage only keeps the lens clear
    return L.fin(mb)

LA_BAR = 0.055

def cam_dicts(n, which='a'):
    s = F.SHOTS[n][which]; return F.cam_from(tuple(c * U for c in s['loc']), tuple(c * U for c in s['look']))

def _hdir(a):
    f = Vector(a['look']) - Vector(a['loc']); f.z = 0; return f.normalized()

def setup_shot(n, f0=None, f1=None, fg=True):
    """Camera keys + foreground props for shot n. f0/f1 default to round(t * 30) of the plan. Start camera at f0, end camera at f1 (Bezier ease); `punch` shots get an extra
    eased push-in of the planned % in 0.4 s at the punch time. FG props are built in the scene (parented to the set root) at the start camera, in front of the lens
    at dist x 0.6 m, and keyed to follow the camera translation (so they stay 1-2 D from the lens while the move runs)."""
    sd = F.SHOTS[n]; sc = bpy.context.scene; f0 = int(round(sd['t0'] * 30)) if f0 is None else f0; f1 = int(round(sd['t1'] * 30)) if f1 is None else f1
    a, b = sd['a'], sd['b']
    cam = F.make_camera(cam_dicts(n, 'a'))
    def put(loc, look, frame, interp='BEZIER'):
        c = F.cam_from(tuple(x * U for x in loc), tuple(x * U for x in look)); F.make_camera(c); cam.keyframe_insert('location', frame=frame); cam.keyframe_insert('rotation_euler', frame=frame)
        F.T._key(cam, 'location', frame, interp); F.T._key(cam, 'rotation_euler', frame, interp)
    pts = [(f0, a['loc'], a['look'])]
    if sd.get('punch'):
        tp, pct = sd['punch']; fp = int(round(tp * 30)); fp = max(f0 + 1, min(fp, f1 - 1)); fe = min(f1, fp + 12)
        def at(fr): u = (fr - f0) / max(1, f1 - f0); return (Vector(a['loc']).lerp(Vector(b['loc']), u), Vector(a['look']).lerp(Vector(b['look']), u))
        l1, t1 = at(fp); l2, t2 = at(fe); l2 = l2 + (t2 - l2) * (pct / 100.0)
        pts += [(fp, tuple(l1), tuple(t1)), (fe, tuple(l2), tuple(t2))]
        if fe < f1: pts += [(f1, tuple(Vector(b['loc']) + (Vector(b['look']) - Vector(b['loc'])) * (pct / 100.0)), b['look'])]
    else: pts.append((f1, b['loc'], b['look']))
    for fr, lc, lk in pts: put(lc, lk, fr, 'BEZIER' if not sd['whip'] else 'LINEAR')
    if fg and sd['fg']:
        M = STATE['M']; hd = _hdir(a); rt = Vector((hd.y, -hd.x, 0.0)); lc0 = Vector(a['loc'])
        for (kind, dist, lat, yr) in sd['fg']:
            p = lc0 + hd * dist + rt * lat; p.z = 0.0
            objs = fg_build(kind, (p.x, p.y, 0.0), math.atan2(hd.y, hd.x) + math.pi / 2 + yr, M, lc0.z)
            for o in objs:
                o['fg'] = 1
                if sd['whip'] is False:
                    # translation follow of the camera (90 %) keyed on the object
                    d1 = (Vector(b['loc']) - lc0) * 0.9; o.keyframe_insert('location', frame=f0); o.location = d1; o.keyframe_insert('location', frame=f1); o.location = (0, 0, 0)
    sc.frame_start = min(sc.frame_start, f0); sc.frame_end = max(sc.frame_end, f1); sc.frame_set(f0)
    return cam

def staging(n):
    """[(role, (x, y, z) D)] for the placeholder cards of shot n."""
    out = []; M = STATE['A']['marks']
    for role, mk in F.SHOTS[n]['actors']:
        p = tuple(M[mk]) if isinstance(mk, str) else tuple(c * U for c in mk)
        out.append((role, p))
    return out

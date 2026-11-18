#!/usr/bin/env python3
"""film 12 take s06: shots 6-8 (box_seat laugh, coach_close two-shot lip-sync, box_seat push-in lip-sync), g 315..571 + 6 handle frames each side.
usage: python3 shot.py draft|final [first last] [i n]   (frames/ or draft/ next to this file; resumable; i n = shard i of n by g % n)"""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c12 as C
S, bpy, cast12 = C.S, C.bpy, C.cast12
G0, G1 = 315, 571; HAND = 6
SHOTS = {6: (315, 377), 7: (378, 464), 8: (465, 571)}
CAMD = {6: ('box_seat', 0.0, 0.6), 7: ('coach_close', 0.0, 0.3), 8: ('box_seat', 0.30, 1.0)}
def shot_of(g):
    if g < 315: return 6
    if g > 571: return 8
    return [k for k, (a, b) in SHOTS.items() if a <= g <= b][0]
def cam_for(g):
    k = shot_of(g); a, b = SHOTS[k]; pr, u0, u1 = CAMD[k]
    p = (g - a) / float(b - a + 1)
    return _cam(pr, u0 + (u1 - u0) * C.ease(p))
def _cam(pr, u):
    c = S.CAMS[pr]; e = u                       # unclamped, linear in pose space (handles extrapolate a little); pose B only reached at u 1
    return dict(loc=C.lerp3(c['loc'], c['loc_b'], e), look_at=C.lerp3(c['look_at'], c['look_b'], e), lens=c['lens'])
QUOTE = (12.66, 19.00)
def build(quality):
    A = S.shot('box_seat', 'RAIN', u=0.5, placeholders=False, quality=quality)
    S.set_rank_busy(1.0)
    gs = list(range(G0 - HAND, G1 + HAND + 1)); camv = {}
    for g in gs:
        C.key_cam(g, cam_for(g)); camv[g] = tuple(bpy.context.scene.camera.location)
    head, han, bb, cc = C.Actor('head'), C.Actor('han'), C.Actor('cb'), C.Actor('cc')
    P = S.STAND['box_a']['pos']; PB = S.STAND['box_b']['pos']; PC = S.STAND['box_c']['pos']
    for g in gs:
        k = shot_of(g); t = g / 30.0 - 0.10
        inq = QUOTE[0] <= t <= QUOTE[1]; ph = g * 2 * math.pi / 5.0
        if k == 6:
            cast, pose = cast12.STORY12['coachman_laugh']; pos = (P[0], P[1], P[2] + 0.05 * abs(math.sin(ph / 2)))
            head.add(g, cast, pose, pos, mirror=True, roll=3.0 * math.sin(ph))
        elif k == 7:
            cast, pose = cast12.STORY12['coachman_point_mock']
            pose = dict(pose, mouth=C.mouth(g) if inq else 'flat', blink=cast12.blink_at(g, 90, 7))
            head.add(g, cast, pose, (P[0], P[1], P[2] + 0.02 * math.sin(g * 0.45)), mirror=True, roll=0.8 * math.sin(g * 0.3))
            y = 20.4 - 0.03 * (g - 378); wc, wp = C.walk('hanway_walk_umbrella', g, 56.0)
            han.add(g, wc, wp, (0.9, y, 0.0), rim='#f2b25c')
        else:
            cast, pose = cast12.STORY12['coachman_boast']
            pose = dict(pose, mouth=C.mouth(g) if inq else 'flat', blink=cast12.blink_at(g, 90, 31))
            head.add(g, cast, pose, (P[0], P[1], P[2] + 0.03 * abs(math.sin(g * 0.3))), mirror=True, roll=0.8 * math.sin(g * 0.25))
            cb, pb = cast12.STORY12['coachman_b_roar']; ccc, pc = cast12.STORY12['coachman_c_roar']
            bb.add(g, cb, pb, (PB[0], PB[1], PB[2] + 0.06 * abs(math.sin(ph / 2 + 1))), mirror=True, roll=3.0 * math.sin(ph + 1))
            cc.add(g, ccc, pc, (PC[0], PC[1], PC[2] + 0.06 * abs(math.sin(ph / 2 + 2))), mirror=True, roll=3.0 * math.sin(ph + 2))
    for a in (head, han, bb, cc): a.bake(lambda g: camv[g], gs[0], gs[-1])
    return A, gs, camv
def report(camv):
    cam = bpy.context.scene.camera; out = {}
    for g in (312, 330, 360, 380, 420, 460, 470, 520, 570):
        bpy.context.scene.frame_set(g); out[g] = {n: [round(v) for v in C.head_y(cam, p, h)[:2]] for n, p, h in
            (('head', S.STAND['box_a']['pos'], 3.19 + 0.3), ('boxb', S.STAND['box_b']['pos'], 3.48), ('boxc', S.STAND['box_c']['pos'], 2.71))}
    return out
if __name__ == '__main__':
    mode = sys.argv[1]; draft = mode != 'final'
    if mode == 'probe': pass
    a = sys.argv[2:]; os.environ.setdefault('SAMPLES', '6' if draft else '20')
    A, gs, camv = build('preview' if draft else 'final')
    sc = bpy.context.scene
    if draft: sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 720, 1280, 50
    if a and ',' in a[0]:
        for g in [int(x) for x in a[0].split(',')]: C.render_range(g, g, os.path.join(HERE, 'frames', 'draft2') if draft else os.path.join(HERE, 'frames'), draft)
        sys.exit(0)
    first, last = (int(a[0]), int(a[1])) if len(a) >= 2 else (gs[0], gs[-1])
    shard = (int(a[2]), int(a[3])) if len(a) >= 4 else None
    C.render_range(first, last, os.path.join(HERE, os.path.join('frames', 'draft2') if draft else 'frames'), draft, shard)

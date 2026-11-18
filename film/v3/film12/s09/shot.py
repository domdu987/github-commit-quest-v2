#!/usr/bin/env python3
"""film 12 take s09: shot 9 (street_wide_low, passers-by and coachmen point and laugh as Hanway passes), g 572..650 + 6 handle frames each side.
usage: python3 shot.py draft|final [first last | g,g,g] [i n]"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c12 as C
S, bpy, cast12 = C.S, C.bpy, C.cast12
G0, G1, HAND = 572, 650, 6
def cam_for(g):
    p = (g - G0) / float(G1 - G0 + 1); u = C.ease(p)
    return dict(loc=C.lerp3((0.9, -4.5, 1.45), (0.5, 0.8, 1.35), u), look_at=C.lerp3((0.3, 40.0, 5.6), (0.3, 40.0, 6.0), u), lens=22.0)
LAUGH = [  # name, pose key, feet, mirror, phase, height (head top for the check)
    ('man1', 'crowd_man_a_point_laugh', (-4.2, 12.0, 0.0), False, 0.0, 3.06),
    ('wR1', 'crowd_woman_a_point_laugh', (7.7, 7.0, 0.28), True, 1.3, 2.91),
    ('mL1', 'crowd_man_b_point_laugh', (-7.4, 5.0, 0.28), False, 2.1, 3.16),
    ('wR2', 'crowd_woman_b_point_laugh', (5.0, 15.0, 0.0), True, 3.4, 2.91),
    ('mL2', 'crowd_man_c_point_laugh', (-7.4, 14.0, 0.28), False, 0.7, 3.06),
    ('mR', 'crowd_man_d_point_laugh', (3.3, 8.5, 0.0), True, 2.8, 3.06),
    ('boxa', 'coachman_laugh', S.STAND['box_a']['pos'], True, 1.9, 3.19),
    ('boxb', 'coachman_b_point_laugh', S.STAND['box_b']['pos'], True, 0.4, 3.48),
]
def build(quality):
    A = S.shot('street_wide_low', 'RAIN', u=0.4, placeholders=False, quality=quality); S.set_rank_busy(1.0)
    gs = list(range(G0 - HAND, G1 + HAND + 1)); camv = {}
    for g in gs: C.key_cam(g, cam_for(g)); camv[g] = tuple(bpy.context.scene.camera.location)
    acts = {n: C.Actor(n) for n, *_ in LAUGH}; han = C.Actor('han')
    for g in gs:
        ph = g * 2 * math.pi / 6.0
        for (n, key, pos, mir, off, h) in LAUGH:
            cast, pose = cast12.STORY12[key]
            acts[n].add(g, cast, pose, (pos[0], pos[1], pos[2] + 0.05 * abs(math.sin(ph / 2 + off))), mirror=mir, roll=3.0 * math.sin(ph + off))
        wc, wp = C.walk('hanway_walk_umbrella', g, 40.0)
        han.add(g, wc, wp, (-0.9, 13.2 - 0.07 * (g - G0), 0.0), rim='#f2b25c')
    for a in list(acts.values()) + [han]: a.bake(lambda g: camv[g], gs[0], gs[-1])
    return A, gs, camv
if __name__ == '__main__':
    mode = sys.argv[1]; draft = mode != 'final'; a = sys.argv[2:]
    os.environ.setdefault('SAMPLES', '6' if draft else '24')
    A, gs, camv = build('preview' if draft else 'final'); sc = bpy.context.scene
    out = os.path.join(HERE, 'frames', 'draft') if draft else os.path.join(HERE, 'frames')
    if a and ',' in a[0]:
        for g in [int(x) for x in a[0].split(',')]: C.render_range(g, g, out, draft)
        sys.exit(0)
    first, last = (int(a[0]), int(a[1])) if len(a) >= 2 else (gs[0], gs[-1])
    C.render_range(first, last, out, draft, (int(a[2]), int(a[3])) if len(a) >= 4 else None)

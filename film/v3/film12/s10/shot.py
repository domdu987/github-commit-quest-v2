#!/usr/bin/env python3
"""s10: shots 10-12 (t 21.69-28.61): cabbage (market), egg (hero_track), mud splash (puddle_low). RAIN. g 645..866 (651-858 + 6 lead + 8 dissolve handle).
usage: DRAFT=1 python3 shot.py draft [A|B|C ...] [step=6]   |  python3 shot.py final [A|B|C ...]   (THREADS=2, SAMPLES from env; final default 22)"""
import os, sys
os.environ.setdefault('SAMPLES', '22')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c12 as C
S, bpy, cast12 = C.S, C.bpy, C.cast12
G0, G1 = 651, 858
FIRST, LAST = G0 - 6, G1 + 8
B0, C0 = 714, 774          # shot 11 / shot 12 starts (round(23.80*30), round(25.80*30))
HW = 'hanway'

# ------------------------------------------------------------------ A: market, cabbage (year 1)
def sub_A():
    A = C.setup('market', 'RAIN'); C.move_cam('market', FIRST, B0 + 4)
    hpos = lambda g: (-4.1 + 0.008 * (g - FIRST), 12.6 - 0.056 * (g - FIRST), 0.0)
    gi = 663                                           # cabbage thwack 22.0 s -> g
    h = hpos(gi); S.throw('cabbage', (-6.0, 11.0, 3.5), (h[0], h[1], 4.35), 655, gi, bounce=(1.6, -1.8), splat=False)
    def build(g):
        k = g - FIRST; hp = hpos(g)
        if g < gi: c, p = C.cyc('hanway_walk_umbrella', k / 30.0)
        elif g < gi + 10: c, p = C.story('hanway_cabbage_flinch')[0], dict(C.cast12.STORY12['hanway_cabbage_flinch'][1])
        else: c, p = C.cyc('hanway_walk_umbrella', k / 30.0)
        if g >= gi: p = dict(p, leaf_stick=1.0)
        C.card('hanway', c, p, hp, rim='#f2b25c')
        # thrower (coachman_b): windup, release, laugh
        if g < 655: c, p = C.story('coachman_b_throw_windup')
        elif g < 664: c, p = C.story('coachman_b_throw_release', mouth='grin')
        else: c, p = C.story('coachman_b_laugh')
        C.card('jeer_b', c, p, (-6.4, 11.0, 0.28))
        c, p = C.cyc('crowd_woman_a_walk_umbrella', k / 28.0 + 0.1); C.card('lady', c, p, (-2.4, 15.5 - 0.02 * k, 0.0))
        c, p = C.story('crowd_man_c_point_laugh'); C.card('seller', c, p, (-7.9, 12.6, 0.28))
        c, p = C.story('crowd_man_b_point_laugh'); C.card('jeer_a', c, p, (-7.4, 6.0, 0.28), mirror=False)
        return dict(h=[round(v) for v in C.head_px(hp, 3.3)[:2]])
    return build, range(FIRST, B0)

# ------------------------------------------------------------------ B: hero_track, egg (year 2)
def sub_B():
    A = C.setup('hero_track', 'RAIN'); C.move_cam('hero_track', B0, C0 - 1)
    hpos = lambda g: (-1.2, 8.0 + 9.8 * (g - B0) / 59.0, 0.0)
    ge = 732                                           # egg splat 24.2 s
    h = hpos(ge); S.throw('egg', (0.6, 12.4, 3.2), (h[0], h[1], 4.3), 725, ge, splat=False)
    def build(g):
        k = g - B0; hp = hpos(g)
        if g < ge: c, p = C.cyc('hanway_walk_umbrella', k / 30.0)
        elif g < ge + 12: c, p = C.story('hanway_egg_tilt')
        else: c, p = C.cyc('hanway_walk_umbrella', k / 30.0); p = dict(p, egg_splat=1.0)
        if g == ge: p = dict(p, egg_splat=0.5)
        C.card('hanway', c, p, hp, rim='#f2b25c')
        if g < 725: c, p = C.story('coachman_c_throw_egg_windup')
        elif g < 735: c, p = C.story('coachman_c_throw_release', mouth='grin')
        else: c, p = C.story('coachman_c_laugh')
        C.card('thrower', c, p, (1.3, 12.6, 0.0), mirror=True)
        c, p = C.story('coachman_laugh'); C.card('box_a', c, p, (3.55, 18.6, 4.22), mirror=True)
        return dict(h=[round(v) for v in C.head_px(hp, 3.3)[:2]])
    return build, range(B0, C0)

# ------------------------------------------------------------------ C: puddle_low, mud wave (year 3)
def sub_C():
    A = C.setup('puddle_low', 'RAIN'); C.move_cam('puddle_low', C0, LAST)
    fc = 786
    S.run_coach(768, 808, y0=26, y1=0)
    for g in range(fc - 2, LAST + 1): S.mud_splash(max(0.0, min(1.0, (g - (fc - 1)) / 25.0)), frame=g)
    hp = (-4.3, 11.0, 0.0)
    def build(g):
        k = g - C0
        if g < fc: c, p = C.story('hanway_stroll_smug')
        elif g < fc + 14: c, p = C.story('hanway_mud_splash'); p = dict(p, mud=min(1.0, 0.35 + 0.22 * (g - fc)))
        else: c, p = C.story('hanway_mud_deadpan'); p = dict(p, soaked=1.0, t=k * 0.04)
        C.card('hanway', c, p, hp, rim='#f2b25c')
        return dict(h=[round(v) for v in C.head_px(hp, 3.3)[:2]])
    return build, range(C0, LAST + 1)

SUBS = dict(A=sub_A, B=sub_B, C=sub_C)
if __name__ == '__main__':
    mode = sys.argv[1]; names = [a for a in sys.argv[2:] if a in SUBS] or list(SUBS)
    step = int([a for a in sys.argv[2:] if a.isdigit()][0]) if any(a.isdigit() for a in sys.argv[2:]) else 6
    for n in names:
        build, fr = SUBS[n]()
        if mode == 'draft': C.render_range(build, [g for g in fr if (g - FIRST) % step == 0], os.path.join(HERE, 'draft'), 's10' + n)
        else: C.render_range(build, list(fr), os.path.join(HERE, 'frames'), 's10' + n)

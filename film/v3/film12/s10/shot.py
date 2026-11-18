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
import art
def mouth(p, m='smirk'): return dict(p, mouth=m)
def sub_A():
    A = C.setup('market', 'RAIN'); C.move_cam('market', FIRST, B0 + 4)
    hpos = lambda g: (-4.1 + 0.008 * (g - FIRST), 12.6 - 0.056 * (g - FIRST), 0.0)
    gi, gr = 663, 654                                  # cabbage hits at 22.0 s; leaves the hand at gr (9 frames of flight)
    S.STATE['light'] = 'RAIN'; C.bpy.context.scene.frame_set(FIRST)
    c, p = C.story('coachman_b_throw_windup'); tmp = C.card('tmp', c, mouth(p, 'frown'), (-6.4, 11.0, 0.28)); p0 = C.hand_world(tmp); C.clear_cards()
    C.bpy.context.scene.frame_set(gi); c, p = C.cyc('hanway_walk_umbrella', (gi - FIRST) / 30.0); tmp = C.card('tmp', c, p, hpos(gi), rim='#f2b25c'); pa = C.apex_world(tmp, c, p, 'umb_mid_r'); C.clear_cards()
    def build(g):
        k = g - FIRST; hp = hpos(g)
        if g < gi: c, p = C.cyc('hanway_walk_umbrella', k / 30.0)
        elif g < gi + 10: c, p = C.story('hanway_cabbage_flinch')[0], dict(C.cast12.STORY12['hanway_cabbage_flinch'][1], leaf_stick=0.0)
        else: c, p = C.cyc('hanway_walk_umbrella', k / 30.0)
        hob = C.card('hanway', c, p, hp, rim='#f2b25c'); apex = C.apex_world(hob, c, p, 'umb_mid_r')
        if gr <= g < gi:                               # ONE cabbage: painted sprite flying from the thrower's hand to the dome
            u = (g - gr) / float(gi - gr); q = C.parabola(p0, (pa[0], pa[1] - 0.1, pa[2]), u, 1.6)
            C.png_card_roll('cabbage_fly', art.cabbage(), q, 0.85, 0.85, roll=u * 9.0)
        if g >= gi:                                    # big leaf stuck on the dome, rides with Hanway
            C.png_card_roll('leaf_dome', art.leaf(), (apex[0], apex[1] - 0.15, apex[2] - 0.12), 1.2, 0.82, roll=-0.12)
        if g < gr: c, p = C.story('coachman_b_throw_windup'); p = mouth(p, 'frown')
        elif g < 664: c, p = C.story('coachman_b_throw_release'); p = mouth(dict(p, expr='angry'), 'frown')
        else: c, p = C.story('coachman_b_nod'); p = mouth(p, 'smirk')
        C.card('jeer_b', c, p, (-6.4, 11.0, 0.28))
        c, p = C.cyc('crowd_woman_a_walk_umbrella', k / 28.0 + 0.1); C.card('lady', c, p, (-2.4, 15.5 - 0.02 * k, 0.0))
        c, p = C.story('crowd_man_c_point_laugh'); C.card('seller', c, mouth(p, 'smirk'), (-7.9, 12.6, 0.28))
        c, p = C.story('crowd_man_b_point_laugh'); C.card('jeer_a', c, mouth(p, 'smirk'), (-7.4, 6.0, 0.28))
        return dict(h=[round(v) for v in C.head_px(hp, 3.3)[:2]])
    return build, range(FIRST, B0)

# ------------------------------------------------------------------ B: hero_track, egg (year 2)
def sub_B():
    A = C.setup('hero_track', 'RAIN'); C.move_cam('hero_track', B0, C0 - 1)
    hpos = lambda g: (-1.2, 8.0 + 9.8 * (g - B0) / 59.0, 0.0)
    ge, gr = 732, 723                                  # egg splat 24.2 s: 9 frames of flight, splat appears on arrival
    S.STATE['light'] = 'RAIN'; C.bpy.context.scene.frame_set(B0)
    c, p = C.story('coachman_c_throw_egg_windup'); tmp = C.card('tmp', c, mouth(p, 'frown'), (1.3, 12.6, 0.0), mirror=True); p0 = C.hand_world(tmp); C.clear_cards()
    def build(g):
        k = g - B0; hp = hpos(g)
        if g < ge: c, p = C.cyc('hanway_walk_umbrella', k / 30.0)
        elif g < ge + 12: c, p = C.story('hanway_egg_tilt')
        else: c, p = C.cyc('hanway_walk_umbrella', k / 30.0); p = dict(p, egg_splat=1.0)
        C.card('hanway', c, p, hp, rim='#f2b25c')
        if gr <= g < ge:
            u = (g - gr) / float(ge - gr); C.png_card_roll('egg_fly', art.egg(), C.parabola(p0, (hpos(ge)[0], hpos(ge)[1] + 0.1, 4.3), u, 1.8), 0.5, 0.62, roll=u * 7.0)
        if g < gr: c, p = C.story('coachman_c_throw_egg_windup'); p = mouth(p, 'frown')
        elif g < 735: c, p = C.story('coachman_c_throw_release'); p = mouth(dict(p, expr='angry'), 'frown')
        else: c, p = C.story('coachman_c_nod'); p = mouth(p, 'smirk')
        C.card('thrower', c, p, (1.3, 12.6, 0.0), mirror=True)
        c, p = C.story('coachman_gloat'); C.card('box_a', c, mouth(p, 'smirk'), (3.55, 18.6, 4.22), mirror=True)
        return dict(h=[round(v) for v in C.head_px(hp, 3.3)[:2]])
    return build, range(B0, C0)

# ------------------------------------------------------------------ C: puddle_low, mud wave (year 3)
def sub_C():
    A = C.setup('puddle_low', 'RAIN'); C.move_cam('puddle_low', C0, LAST)
    fc = 786
    S.run_coach(768, 808, y0=26, y1=0)
    hp = (-3.8, 8.7, 0.0)
    a_c, a = C.story('hanway_stroll_smug'); b_c, b = C.story('hanway_mud_splash')
    def build(g):
        k = g - C0; rel = g - fc + 1
        if rel <= 2: c, p = a_c, dict(a)
        elif rel <= 7:                                           # 5-frame reaction: lerp smug -> shocked (umbrella flips over the 5 frames)
            t = (rel - 2) / 5.0; t = t * t * (3 - 2 * t); import puppet; c = a_c; p = dict(puppet.lerp_pose('hanway', a, b, t))
            for key in ('mud', 'soaked', 'fx'): p.pop(key, None)
            p['prop_r'] = dict(a['prop_r'], angle=a['prop_r']['angle'] + (b['prop_r']['angle'] - a['prop_r']['angle']) * t)
            p['expr'] = 'shocked' if t > 0.4 else a['expr']; p['mouth'] = 'o' if t > 0.4 else a['mouth']
        elif rel < 22: c, p = b_c, dict(b)
        else: c, p = C.story('hanway_mud_deadpan'); p = dict(p, soaked=1.0, t=k * 0.04)
        if rel >= 11: p['mud'] = min(1.0, (rel - 10) / 7.0)
        C.card('hanway', c, p, hp, rim='#f2b25c')
        if rel >= 0:
            C.png_card_flat('ripples', art.ripple_path(rel), (-1.7, 12.2, 0.0), art.RP_W)
            if 0 < rel < 25: C.png_card('crown', art.crown_path(rel), (-1.7 - art.BASE_DX, 12.3, 0.0), art.W_U, art.H_U)
            if 2 < rel < 25: C.png_card_flat('near_ripples', art.near_path(rel), (-3.6, 6.8, 0.0), art.NR_W, z=0.05)
            if 9 <= rel < 24: C.png_card('landing', art.landing_path(rel), (hp[0], hp[1] - 0.8, 0.0), art.LAND_W, art.LAND_W)
        return dict(h=[round(v) for v in C.head_px(hp, 3.3)[:2]], rel=rel)
    return build, range(C0, LAST + 1)

SUBS = dict(A=sub_A, B=sub_B, C=sub_C)
if __name__ == '__main__':
    mode = sys.argv[1]; names = [a for a in sys.argv[2:] if a in SUBS] or list(SUBS)
    step = int([a for a in sys.argv[2:] if a.isdigit()][0]) if any(a.isdigit() for a in sys.argv[2:]) else 6
    for n in names:
        build, fr = SUBS[n]()
        if mode == 'draft': C.render_range(build, [g for g in fr if (g - FIRST) % step == 0], os.path.join(HERE, 'draft'), 's10' + n)
        else: C.render_range(build, list(fr), os.path.join(HERE, 'frames'), 's10' + n)

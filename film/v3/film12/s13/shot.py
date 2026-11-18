#!/usr/bin/env python3
"""s13: shots 13-14 (t 28.61-34.98): ten years on, DUSK_RAIN: ONE umbrella among bare heads (street_high crane), then the head coachman's false-payoff shout (box_seat).
g 850..1055 (858-1049 + 8 handle for the 12-frame dissolve in + 6 after).
usage: DRAFT=1 python3 shot.py draft [D|E ...] [step]  |  python3 shot.py final [D|E ...]"""
import os, sys
os.environ.setdefault('SAMPLES', '22')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c12 as C
S, bpy, cast12 = C.S, C.bpy, C.cast12
G0, G1 = 858, 1049
FIRST, LAST = G0 - 8, G1 + 6
E0 = 945                    # round(31.50*30)
Q0, Q1 = C.g_of(33.00), C.g_of(34.95)       # quote window in film frames (993 .. 1052)
L = 'DUSK_RAIN'

def sub_D():
    A = C.setup('street_high', L, figures='umb'); S.set_crowd_umbrellas(0.0)
    C.move_cam('street_high', FIRST, E0, 0.35, 1.0)
    walkers = [('w1', 'crowd_man_a_walk_hat', (-7.4, 7.0, 0.28), 0.04), ('w2', 'crowd_woman_b_walk_umbrella', (7.6, 4.0, 0.28), 0.05), ('w3', 'crowd_man_d_walk_hat', (-6.8, 16.0, 0.28), -0.04),
               ('w4', 'crowd_man_c_walk_hat', (-3.6, 8.0, 0.0), 0.05), ('w5', 'crowd_man_b_walk_hat', (2.2, 7.0, 0.0), -0.05), ('w6', 'crowd_woman_a_walk_umbrella', (7.4, 14.0, 0.28), -0.04),
               ('w7', 'crowd_man_d_walk_hat', (-1.2, 12.0, 0.0), 0.04), ('w8', 'crowd_woman_b_walk_umbrella', (3.8, 13.0, 0.0), -0.04), ('w9', 'crowd_man_a_walk_hat', (-5.0, 2.0, 0.0), -0.04), ('w10', 'crowd_man_c_walk_hat', (4.4, 1.0, 0.0), 0.04)]
    def build(g):
        k = g - FIRST
        c, p = C.cyc('hanway_walk_umbrella', k / 30.0); hp = (-1.0, 11.5 + 0.0 * k, 0.0)
        C.card('hanway', c, p, hp, light=L, rim='#f2b25c', tilt=22.0)
        for nm, cy, pos, v in walkers:
            c, p = C.cyc(cy, k / 28.0 + 0.13 * len(nm) * pos[0] % 1.0)
            if 'woman' in cy: p = dict(p, prop_r=None)                 # no umbrellas: bare heads only (one umbrella among many)
            C.card(nm, c, p, (pos[0], pos[1] + v * k, pos[2]), light=L, tilt=22.0, mirror=(v < 0))
        return dict(h=[round(v) for v in C.head_px(hp, 3.3)[:2]])
    return build, range(FIRST, E0)

def sub_E():
    A = C.setup('box_seat', L); C.move_cam('box_seat', E0, LAST, 0.3, 1.0)
    pq = ['coachman_shout', 'coachman_point_mock', 'coachman_boast', 'coachman_point_mock']
    def build(g):
        if g < Q0: c, p = C.story('coachman_gloat'); p = dict(p, blink=cast12.blink_at(g, 90))
        else:
            c, p = C.story(pq[((g - Q0) // 12) % 4]); p = dict(p, mouth=cast12.talk_mouth(g, 1.0), blink=cast12.blink_at(g, 90), whip_t=(g * 0.07) % 1.0)
            if g > Q1: p = dict(p, mouth='flat')
        C.card('box_a', c, p, (3.55, 18.6, 4.22), light=L, mirror=True)
        return dict(h=[round(v) for v in C.head_px((3.55, 18.6, 4.22), 3.2)[:2]], talk=int(Q0 <= g <= Q1))
    return build, range(E0, LAST + 1)

SUBS = dict(D=sub_D, E=sub_E)
if __name__ == '__main__':
    mode = sys.argv[1]; names = [a for a in sys.argv[2:] if a in SUBS] or list(SUBS)
    step = int([a for a in sys.argv[2:] if a.isdigit()][0]) if any(a.isdigit() for a in sys.argv[2:]) else 6
    for n in names:
        build, fr = SUBS[n]()
        if mode == 'draft': C.render_range(build, [g for g in fr if (g - FIRST) % step == 0], os.path.join(HERE, 'draft'), 's13' + n)
        else: C.render_range(build, list(fr), os.path.join(HERE, 'frames'), 's13' + n)

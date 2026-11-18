#!/usr/bin/env python3
"""s13: shots 13-14 (t 28.61-34.98): ten years on, DUSK_RAIN: ONE umbrella among bare heads (street_high crane), then the head coachman's false-payoff shout (box_seat).
g 850..1055 (858-1049 + 8 handle for the 12-frame dissolve in + 6 after).
usage: DRAFT=1 python3 shot.py draft [D|E ...] [step]  |  python3 shot.py final [D|E ...]"""
import os, sys, math
os.environ.setdefault('SAMPLES', '22')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c12 as C
S, bpy, cast12 = C.S, C.bpy, C.cast12
G0, G1 = 858, 1049
FIRST, LAST = G0 - 8, G1 + 6
E0 = 945                    # round(31.50*30)
Q0, Q1 = C.g_of(33.00), C.g_of(34.95)       # quote window in film frames (993 .. 1052)
L = 'DUSK_RAIN'

import art
def solve_y(x, target, h=3.2, lo=3.0, hi=24.0):
    """world y (on the road, z 0) at which a head h above the feet projects to pixel row `target` (bisection; farther = higher on screen)."""
    for _ in range(28):
        m = (lo + hi) / 2.0
        if C.head_px((x, m, 0.0), h)[1] > target: lo = m
        else: hi = m
    return (lo + hi) / 2.0

CROWD = [  # (dx from Hanway, dy beyond Hanway, cycle, side speed)  bare heads; hunched 'soaked' walkers hold the weather off
    (-3.2, 1.6, 'crowd_man_a_walk_soaked'), (2.8, 2.2, 'crowd_man_d_walk_hat'), (-5.4, 3.0, 'crowd_woman_b_walk_umbrella'), (4.6, 3.4, 'crowd_man_c_walk_soaked'),
    (-1.9, 4.6, 'crowd_man_b_walk_hat'), (1.7, 5.4, 'crowd_man_a_walk_hat'), (-6.2, 6.0, 'crowd_woman_a_walk_umbrella'), (6.2, 6.6, 'crowd_man_d_walk_soaked'),
    (-3.6, 8.2, 'crowd_man_c_walk_hat'), (3.4, 9.0, 'crowd_man_b_walk_soaked'), (-0.4, 10.4, 'crowd_man_a_walk_hat'), (-6.4, 12.0, 'crowd_man_d_walk_hat'), (5.8, 13.0, 'crowd_woman_b_walk_umbrella')]

def sub_D():
    A = C.setup('street_high', L, figures='umb'); S.set_crowd_umbrellas(0.0)
    C.move_cam('street_high', FIRST, E0, 0.35, 1.0)
    def build(g):
        k = g - FIRST; hx = -1.0; hy = solve_y(hx, 790.0, 3.3); hp = (hx, hy, 0.0)
        c, p = C.cyc('hanway_walk_umbrella', k / 30.0)
        C.card('hanway', c, p, hp, light=L, rim='#f2b25c', tilt=22.0)
        shown = 1
        for n, (dx, dy, cy) in enumerate(CROWD):
            x = hx + dx; y = hy + dy - 0.012 * k * (1 if n % 2 else -1); z = 0.28 if abs(x) > 6.3 else 0.0
            hpx = C.head_px((x, y, z), 3.2); fpx = C.head_px((x, y, z), 0.0)
            if hpx[1] > 850 or fpx[1] > 1270 or hpx[2] <= 0: continue                    # no head below y 850, nothing cut by the bottom edge
            c, p = C.cyc(cy, k / 28.0 + 0.173 * n)
            if 'woman' in cy: p = dict(p, prop_r=None)                                   # no umbrellas: bare heads only (one umbrella among many)
            C.card('w%d' % n, c, p, (x, y, z), light=L, tilt=22.0, mirror=(n % 2 == 1)); shown += 1
        return dict(h=[round(v) for v in C.head_px(hp, 3.3)[:2]], cards=shown)
    return build, range(FIRST, E0)

def sub_E():
    A = C.setup('box_seat', L); C.move_cam('box_seat', E0, LAST, 0.3, 1.0)
    import puppet
    g_c, g_p = C.story('coachman_gloat'); s_c, s_p = C.story('coachman_shout')
    look = dict(gaze=(0.25, 0.85), pitch=0.2)                               # eyes open, looking down at the street / Hanway
    def build(g):
        base = dict(g_p, expr='neutral', mouth='grin', **look)               # closed grin, no winks, no blinks
        if g < Q0 - 8: p = base
        elif g < Q0:                                                      # ease the arms into the shout pose before the first word (no arm pop)
            t = (g - (Q0 - 8)) / 8.0; t = t * t * (3 - 2 * t); p = dict(puppet.lerp_pose('coachman', base, dict(s_p, expr='angry', mouth='grin', **look), t))
            p.update(expr='neutral' if t < 0.5 else 'angry', mouth='grin', whip_t=0.8 * t, **look); p['prop_r'] = dict(s_p['prop_r'], angle=-60 * t - 90 * (1 - t)) if t > 0 else None
        else:
            p = dict(s_p, expr='angry', mouth=C.cast12.talk_mouth(g, 1.0), whip_t=(g * 0.05) % 1.0, head_roll=6 + 2.0 * math.sin(g * 0.35), **look)
            if g > Q1: p['mouth'] = 'grin'
        C.png_card_flat('plank_shadow', art.shadow(), (3.55, 18.6, 4.22), 2.6, z=0.03)
        C.card('box_a', g_c, p, (3.55, 18.6, 4.22), light=L, mirror=True)
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

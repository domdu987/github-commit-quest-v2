#!/usr/bin/env python3
"""s13 (film 22) ticket hall: the stand empties, REPRINT crates, Beck proud in the crowd.  g 1559..1661 (+6 handles each side).
    python3 shot.py stills 1553:1667:6 <out> [scale%] [samples]      python3 shot.py final 1553:1667 <out>
"""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c22 as C
B, U, bpy, V = C.B, C.U, C.bpy, C.V
import beck_under as BU
F0, F1 = 1559, 1662
STAND = BU.STAND
BECK = (4.6, 8.2, 0.0)
CAM = [(0, (3.2, 1.2, 3.3), (0.3, 10.0, 4.4), 28), (30, (5.0, -2.5, 6.0), (0.5, 11.0, 3.8), 28), (65, (5.6, -2.8, 8.0), (2.8, 10.0, 2.6), 27), (102, (4.8, -1.8, 11.0), (4.2, 10.6, 1.6), 26)]
WALK = []

def post_build():
    random.seed(5)
    # crowd: walk across the hall, keep out of the stand's zone
    for k, nm in enumerate(BU.HALL['crowd']):
        d = U.ACTORS[nm]; x, y, z = d['mark']
        y = 5.2 + (y + 6.0) * 0.38
        if abs(y - STAND[1]) < 3.0 and abs(x - STAND[0]) < 5.0: y = 5.3 if y < STAND[1] else 13.8
        if abs(y - BECK[1]) < 2.5 and abs(x - BECK[0]) < 5.0: y += 4.0
        sp = (1.6 + 0.5 * (k % 4)) * (1 if k % 2 else -1)
        d['name'] = nm; WALK.append((d, x, y, sp, k))
    rr = random.Random(9)
    for k in range(12):
        nm = 'xc%d' % k; x, y = rr.uniform(-15, 15), rr.uniform(5.0, 7.5)
        U.crowd_card(nm, (k * 7 + 3) % 16, 'pass_walk', (x, y, 0.0), rim='#ffb878' if k % 2 else '#a8bcff', mirror=(k % 3 == 0))
        sp = (1.6 + 0.4 * (k % 3)) * (1 if k % 2 else -1); U.ACTORS[nm]['name'] = nm; WALK.append((U.ACTORS[nm], x, y, sp, 40 + k))
    U.move_actor('beck', BECK)
    # the stranger with an open map beside Beck, a porter pair wheeling the crates in
    U.actor('stranger', 'pass_read_map', (BECK[0] + 2.1, BECK[1] - 0.2, 0.0), rim='#a8bcff')
    U.actor('stranger2', 'pass_read_map', (BECK[0] - 2.4, BECK[1] + 0.6, 0.0), rim='#ffb878')
    for i in range(2):
        U.actor('pcrate%d' % i, 'porter_push_crate', (-22.0, 4.5 + i * 2.2, 0.0), rim='#ffb878', cast='porter')
    C.mount(('way_out_sign', 'stand_sign_real', 'stand_sign_trial', 'pools_h', 'lamps', 'lamp_halos'))
    C.scale_lights('hl', 1.8); C.scale_lights('hall_fill', 1.6)
    U.pl('beck_key', (BECK[0] + 0.5, BECK[1] - 3.0, 4.6), (1.0, 0.82, 0.55), 700, 0.6)

def animate(f, n):
    BU._anim_s13(f, n)
    if 'pcrate0' not in U.ACTORS: return
    t = f / 30.0
    for d, x0, y0, sp, k in WALK:
        x = x0 + sp * t
        # wrap inside the hall
        x = (x + 17.5) % 35.0 - 17.5
        C.move_card(d['name'], x, y0, 0.0)
    # porters + crates arrive from the west (REPRINT) at 54.71 s (f 85)
    for i in range(2):
        u = C.ez((f - 62 - 5 * i) / 34.0); x = -22.0 + 17.0 * u + (0.0 if i == 0 else 0.0)
        C.move_card('pcrate%d' % i, x - 2.2, 4.5 + i * 2.2, 0.0)
    crate3 = C.obj('crate_3')
    if crate3 is not None: crate3.hide_render = True            # the stacked crate would ride in the air while the others slide in
    U.face_cards()

if __name__ == '__main__':
    C.drive('s13', CAM, 'hall', 'HALL', animate, post_build, sys.argv[1:], F0, F1, state=dict(B.ALL_SHOTS['s13']['state']))

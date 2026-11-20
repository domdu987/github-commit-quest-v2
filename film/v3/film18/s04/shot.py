#!/usr/bin/env python3
"""shot.py -- film 18 take s04 (render team 2): vista at DUSK, high push-in toward the near lit town Jimo ("จี๋โม่" 11.91 s = g 360, a quick extra push),
two towns stay lit (Jimo near, Ju far), all pennants up (pn1).
Director note: opaque flag with no bloom, no blown glow stalk, caption band bright <= 1 %, Ju lit.
    python3 shot.py draft [a:b[:step]]   |   python3 shot.py final [a:b[:step]]
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18
from c18 import J, S

G0, G1 = 297, 384
H_IN, H_OUT = 2, 8                   # cut in ("same take" in the plan, but the s03 camera does not continue into this one), dissolve 11 out
FIRST, LAST = G0 - H_IN, G1 - 1 + H_OUT
G_JIMO = c18.g_of(11.91)            # 360

mode, rng = c18.parse_args(FIRST, LAST)
T = c18.Take('s04', FIRST, LAST, draft=(mode == 'draft'), cam_fn=c18.compose(lambda T, g, t: T.base_pose(t), c18.rhythm_cam(push=0.06, slide=0.0, orbit=-24.0, pulses=())))
c18.fix_vista(T); c18.vista_quiet(T); c18.vista_yard_fix()
c18.fix_sky_clean(T, 'sky_DUSK')


import jimo_vista as VS


def frame(T, g):
    T.set_camera(g)
    order = J.vista_pennant_order(T.cam)
    for r, idx in enumerate(order):
        VS.set_pennant_scale(idx, 0.4 if r < 20 else 0.55, kind='yan')
    c18.jimo_flag(0.4)


T.run(frame, gs=rng, force=(mode == 'draft'))

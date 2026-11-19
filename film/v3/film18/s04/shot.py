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
t_snap = (G_JIMO - 8 - G0) / float(G1 - G0)
T = c18.Take('s04', FIRST, LAST, draft=(mode == 'draft'), cam_fn=c18.rhythm_cam(push=0.08, slide=0.0, orbit=-9.0, pulses=(299, 312, 325, 338, G_JIMO - 6, 367, 378), width=8, amp=0.15))
c18.fix_vista(T)
c18.fix_sky(T)
print('hidden pennants near Ju:', c18.clear_sightline(T, 'ju', gs=(FIRST, 330, 360, LAST)), flush=True)


def frame(T, g):
    J.set_pennants(1.0, 'yan'); J.set_qi_return(0.0)
    c18.hold_apply(T); c18.hide_pennants(T)


T.run(frame, gs=rng, force=(mode == 'draft'))

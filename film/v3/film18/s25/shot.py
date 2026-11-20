#!/usr/bin/env python3
"""shot.py -- film 18 take s25 (render team 2): vista at DAWN, establishing high, push 6 %/s; the Qi banners return over the towns one by one
(set_qi_return 0 -> 1, keyed on every frame), warm dawn.  Opaque cloth flags without bloom, no siege halos, caption band clear.
    python3 shot.py draft [a:b[:step]]   |   python3 shot.py final [a:b[:step]]
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18
from c18 import J, S

G0, G1 = 1882, 1958
H_IN, H_OUT = 9, 8                   # dissolve 15 in / dissolve 11 out
FIRST, LAST = G0 - H_IN, G1 - 1 + H_OUT
mode, rng = c18.parse_args(FIRST, LAST)
T = c18.Take('s25', FIRST, LAST, draft=(mode == 'draft'), cam_fn=c18.compose(c18.tilt_cam(-34.0), c18.rhythm_cam(push=0.04, slide=0.0, orbit=14.0, pulses=())))
c18.fix_vista(T); c18.vista_quiet(T)
c18.fix_sky_clean(T, 'sky_DAWN')
G_Q0, G_Q1 = G0 + 4, G1 - 6


def frame(T, g):
    J.set_pennants(1.0, 'yan'); J.set_qi_return(c18.ramp(g, G_Q0, G_Q1))
    c18.hold_apply(T)


T.run(frame, gs=rng, force=(mode == 'draft'))

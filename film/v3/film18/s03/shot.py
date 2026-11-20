#!/usr/bin/env python3
"""shot.py -- film 18 take s03 (render team 2): vista at DUSK, establishing high, push 6 %/s + slide left; the black Yan pennants pop over the towns
one by one on 7.32-9.89 s (set_pennants 0 -> 1, keyed on every frame).
QA_ART_SET_R2 13 / 14: short-bar clouds, opaque Qi flags (holdouts), no siege halos, caption band clear.
    python3 shot.py draft [a:b[:step]]   |   python3 shot.py final [a:b[:step]]
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18
from c18 import J, S

G0, G1 = 156, 297                    # plan: s03 = film frames 156..296
H_IN, H_OUT = 9, 2                   # dissolve 15 in (half + 2), cut out
FIRST, LAST = G0 - H_IN, G1 - 1 + H_OUT
G_PEN0, G_PEN1 = c18.g_of(7.32), 294      # pennants pop (full count before the shot ends)

mode, rng = c18.parse_args(FIRST, LAST)
T = c18.Take('s03', FIRST, LAST, draft=(mode == 'draft'), cam_fn=c18.compose(c18.tilt_cam(-45.0), c18.rhythm_cam(push=0.0, slide=0.0, orbit=-19.0, pulses=())))
c18.fix_vista(T)
c18.fix_sky(T)


def frame(T, g):
    k = c18.ramp(g, G_PEN0, G_PEN1)
    J.set_pennants(k, 'yan'); J.set_qi_return(0.0)
    c18.hold_apply(T)


T.run(frame, gs=rng, force=(mode == 'draft'))

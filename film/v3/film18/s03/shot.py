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
def dolly(T, g, t):
    """one eased dolly + truck over the plain (TAKE gate recipe): the camera flies from the high establishing view down toward the dense western towns, look-at drifting with it."""
    e = c18.ease(t) * 0.7 + t * 0.3
    L0, L1 = (40.0, -135.0, 70.0), (-95.0, 15.0, 70.0); K0, K1 = (-12.0, 100.0, -55.0), (-125.0, 175.0, -55.0)
    return dict(loc=tuple(c18.lerp(a, b, e) for a, b in zip(L0, L1)), look_at=tuple(c18.lerp(a, b, e) for a, b in zip(K0, K1)), lens=20)


T = c18.Take('s03', FIRST, LAST, draft=(mode == 'draft'), cam_fn=dolly)
c18.fix_vista(T)
c18.fix_sky_clean(T, 'sky_DUSK')


def frame(T, g):
    k = c18.ramp(g, G_PEN0, G_PEN1)
    J.set_pennants(k, 'yan'); J.set_qi_return(0.0)
    c18.hold_apply(T)


T.run(frame, gs=rng, force=(mode == 'draft'))

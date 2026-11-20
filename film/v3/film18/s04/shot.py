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
def dolly(T, g, t):
    """one eased dolly toward Jimo with a truck: it starts high and far so Jimo (right) AND Ju (far left, beacon fire) are both in frame, then closes on Jimo; a held punch-in on "จี๋โม่"."""
    e = c18.ease(t) * 0.75 + t * 0.25
    L0, L1 = (-95.0, 15.0, 70.0), (8.0, -88.0, 50.0); K0, K1 = (-122.0, 160.0, -40.0), (29.0, -30.0, 5.0)
    k = c18.ramp(g, G_JIMO - 8, G_JIMO + 1) * 0.16                                  # the held punch-in (+16 %)
    loc = [c18.lerp(a, b, e) for a, b in zip(L0, L1)]; look = [c18.lerp(a, b, e) for a, b in zip(K0, K1)]
    loc = [l + (kk - l) * k for l, kk in zip(loc, look)]
    return dict(loc=tuple(loc), look_at=tuple(look), lens=22)


T = c18.Take('s04', FIRST, LAST, draft=(mode == 'draft'), cam_fn=dolly)
c18.fix_vista(T)
c18.fix_sky_clean(T, 'sky_DUSK')
print('hidden pennants near Ju:', c18.clear_sightline(T, 'ju', gs=(FIRST, 330, 360, LAST), radius=130), flush=True)


def frame(T, g):
    J.set_pennants(1.0, 'yan'); J.set_qi_return(0.0)
    c18.hold_apply(T); c18.hide_pennants(T)


T.run(frame, gs=rng, force=(mode == 'draft'))

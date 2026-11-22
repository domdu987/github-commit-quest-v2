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
    """one eased dolly + truck down onto the dense western towns, then from g 240 the camera eases UP and BACK so the last frame overlooks the whole pennant field."""
    e = c18.ease(t) * 0.7 + t * 0.3
    L0, L1 = (40.0, -135.0, 70.0), (-95.0, 15.0, 70.0); K0, K1 = (-12.0, 100.0, -55.0), (-125.0, 175.0, -55.0)
    loc = [c18.lerp(a, b, e) for a, b in zip(L0, L1)]; look = [c18.lerp(a, b, e) for a, b in zip(K0, K1)]
    w = c18.ramp(g, 238, 297)
    L2 = (-100.0, -125.0, 190.0); K2 = (-92.0, 110.0, -35.0)
    loc = [c18.lerp(a, b, w) for a, b in zip(loc, L2)]; look = [c18.lerp(a, b, w) for a, b in zip(look, K2)]
    return dict(loc=tuple(loc), look_at=tuple(look), lens=20)


T = c18.Take('s03', FIRST, LAST, draft=(mode == 'draft'), cam_fn=dolly)
c18.fix_vista(T); c18.vista_quiet(T); c18.vista_yard_fix()
c18.fix_sky_clean(T, 'sky_DUSK', flat_above=0.6)
import bpy
for _n in (os.environ.get('RM', 'r3_tent,r3_tent_b').split(',')):                     # V2: the siege-tent domes (white discs / brown ovals) hover over the field - removed
    _o = bpy.data.objects.get(_n)
    if _o is not None: bpy.data.objects.remove(_o, do_unlink=True)


import jimo_vista as VS
ORDER = None


def frame(T, g):
    global ORDER
    if ORDER is None:
        T.set_camera(LAST); ORDER = J.vista_pennant_order(T.cam)
    SKIP = 6                                                         # the nearest poles (bottom third, diagonal in the wide lens) stay down
    VS.set_pennant_scale(ORDER[0], 0.0, kind='yan')
    for idx in ORDER[:SKIP]:
        VS.set_pennant_scale(idx, 0.0, kind='yan')
    n = len(ORDER) - SKIP; step = (G_PEN1 - G_PEN0 - 10) / float(n)
    for r, idx in enumerate(ORDER[SKIP:]):
        cap = 0.32 if r < 12 else (0.7 if r < 26 else 1.0)
        VS.set_pennant_scale(idx, cap * c18.ramp(g, G_PEN0 + r * step, G_PEN0 + r * step + 10), kind='yan')
    J.set_qi_return(0.0) if False else None
    c18.jimo_flag(0.45)


def ground_poles():
    """V2: every pennant pole stands ON the ground (ground_check): cast down from the pole base and move the pole (and its cloth) onto the surface."""
    import importlib.util
    sp = importlib.util.spec_from_file_location('ground_check', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools', 'ground_check.py')); gc = importlib.util.module_from_spec(sp); sp.loader.exec_module(gc)
    import json
    sh = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pole_shifts.json'))); n = 0; worst = 0.0
    for nm, d in sh.items():                                          # shifts measured by ground_check at g 296 (all poles up): each pole (and its cloth) is lowered onto the terrain
        ob = bpy.data.objects.get(nm)
        if ob is None: continue
        ob.location.z -= d; n += 1; worst = max(worst, d)
        cl = bpy.data.objects.get(nm.replace('pen_', 'pcl_', 1))
        if cl is not None: cl.location.z -= d
    bpy.context.view_layer.update(); print('ground_poles: moved', n, 'poles, worst', round(worst, 3))
ground_poles()
T.run(frame, gs=rng, force=(mode == 'draft'))

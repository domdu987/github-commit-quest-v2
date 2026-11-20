"""T1a local camera-path tweaks (director's TAKE-gate fix list). Keys g0, g105 and everything from g172 on are unchanged: the modified path is
blended into the planned one (smoothstep) so the take still starts and ends exactly as planned and T1b (g191+) joins on the original path."""
import sys, os, copy
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..', 'set3d17'))
import bpy
import prefecture17 as P
ML = P.ML; _k = P._k
def _ss(x): x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)
def _w(g):        # blend weight of the modified path: 0 = planned path, 1 = modified
    w = _ss((g - 28) / 12.0)                       # roof dive fix g36-48 ... until g100
    w *= 1.0 - _ss((g - 98) / 7.0)                 # back to the planned path by g105 (hold key)
    w2 = _ss((g - 146) / 6.0) * (1.0 - _ss((g - 166) / 6.0))   # over-the-heads route g146-172
    return max(w, w2)
def new_keys():
    K0 = copy.deepcopy(P.TAKES['T1']['keys']); by = {k['g']: k for k in K0}
    head = ML(-2.15, 1.4, 1.45)
    ks = [by[0],
          _k(40, (-17.2, 4.6, 22.6), (6.0, 13.3, 12.5)), _k(46, (-13.0, 6.0, 23.0), (7.0, 13.3, 15.0)), _k(54, (-8.2, 7.8, 19.8), (7.0, 13.3, 11.5)), _k(62, (-3.5, 9.5, 15.5), ML(-2.2, 1.3, 2.0)),
          _k(78, (2.6, 12.9, 4.6), ML(0.2, 0.6, 1.0)), _k(92, ML(-3.2, 0.1, 2.1), ML(-1.0, 1.3, 1.2)), _k(97, ML(-1.7, -0.6, 1.9), ML(-1.7, 1.4, 1.3)), _k(100, ML(-0.8, -0.65, 1.7), ML(-1.9, 1.4, 1.3)), by[105], by[148],
          _k(156, ML(-0.2, 0.9, 3.2), ML(-2.1, 1.6, 1.3)), _k(163, ML(-2.2, 0.3, 3.6), ML(-2.0, 1.6, 1.2)), _k(168, (4.6, 12.5, 3.8), ML(-1.8, 1.4, 1.0))]
    ks += [by[g] for g in sorted(by) if g > 168]
    return ks
def blended_frames():
    orig = {f['g']: f for f in P.path_take('T1')}
    keys = P.TAKES['T1']['keys']; P.TAKES['T1']['keys'] = new_keys()
    try: new = {f['g']: f for f in P.path_take('T1')}
    finally: P.TAKES['T1']['keys'] = keys
    out = []; prev = None
    for g in sorted(orig):
        w = _w(g); a, b = orig[g], new[g]
        loc = tuple((1 - w) * np.array(a['loc']) + w * np.array(b['loc'])); look = tuple((1 - w) * np.array(a['look']) + w * np.array(b['look']))
        q = P._lookrot(loc, look)
        if prev is not None and q.dot(prev) < 0: q.negate()
        prev = q; out.append(dict(g=g, loc=loc, look=look, rot=tuple(q), lens=a['lens']))
    return out
def apply_path(cam, g0=36, g1=175):
    P.key_cam(cam, [f for f in blended_frames() if g0 <= f['g'] <= g1])
    for nm in ('bertillon', 'prisoner_a', 'prisoner_b', 'prisoner_q'): P.BACK_VIEW[('T1', nm)] = [(60, 96), (165, 186)]
def hide_near_smoke(cam, R=2.5):
    cp = cam.matrix_world.translation
    for sm in P.W['smoke']:
        for o in sm['puffs']: o.hide_render = (o.matrix_world.translation - cp).length < R + o.scale[0]

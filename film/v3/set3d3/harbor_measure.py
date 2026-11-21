#!/usr/bin/env python3
"""harbor_measure.py [preset] [cam] [quality] : shade / lit ratio per surface on our own render, as v3/set3d2/tower_measure.py
(whose helpers are imported): key on / key off on the same pixels, linear luminance ratio where the key reaches; pixels attributed
to objects by ray casting the camera rays. Also the hue of the lit and the shaded colour."""
import sys, os, json
import numpy as np, cv2, bpy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'set3d2'))
import harbor as H
import tower_measure as TM

def run(preset='WINTER', cam='street_low', quality='final'):
    A = H.build(preset); sc = bpy.context.scene; H.setup_render(sc, quality); sc.cycles.samples = 24
    cs = A['cams'][cam]; c = H.make_camera(cs); H.stage_placeholders(A, H.STAGING[cam], cs['loc'])
    sc.render.use_compositing = False
    d = os.path.join(H.WORK, 'measure'); os.makedirs(d, exist_ok=True); on_p = os.path.join(d, '%s_%s_on.png' % (preset, cam)); off_p = os.path.join(d, '%s_%s_off.png' % (preset, cam))
    H.render(on_p); H.STATE['sun'].hide_render = True; H.render(off_p); H.STATE['sun'].hide_render = False
    on = cv2.cvtColor(cv2.imread(on_p), cv2.COLOR_BGR2RGB).astype(np.float64); off = cv2.cvtColor(cv2.imread(off_p), cv2.COLOR_BGR2RGB).astype(np.float64)
    Hh, W = on.shape[:2]; s = 4; ids = TM.object_map(c, W // s, Hh // s)
    lon, loff = TM.Y(TM.lin(on)), TM.Y(TM.lin(off)) + 1e-5
    r = lon / loff - 1.0; rmax = cv2.dilate(r.astype(np.float32), np.ones((41, 41), np.uint8)); v = np.clip(r / np.maximum(rmax, 1e-3), 0, 1)
    lit = (r > 0.3) & (v > 0.92); sm = lambda a: a[s // 2::s, s // 2::s][:Hh // s, :W // s]
    res = {}
    for nm in sorted(set(ids.ravel()) - {'', 'water'}):
        m = (ids == nm) & sm(lit)
        if m.sum() < 30: continue
        rat = sm(loff)[m] / sm(lon)[m]
        res[nm] = dict(n=int(m.sum()), ratio_lin_median=round(float(np.median(rat)), 3), lit=TM.hsv_of(sm(on)[m].mean(0)), shade=TM.hsv_of(sm(off)[m].mean(0)))
    out = dict(preset=preset, cam=cam, surfaces=res)
    print(json.dumps(out)); json.dump(out, open(os.path.join(d, '%s_%s.json' % (preset, cam)), 'w'), indent=1)
    return out

if __name__ == '__main__':
    a = sys.argv[1:]; run(a[0] if a else 'WINTER', a[1] if len(a) > 1 else 'street_low', a[2] if len(a) > 2 else 'preview')

#!/usr/bin/env python3
"""tower_measure.py [preset] [cam] [quality] : shade / lit ratio of the set per surface, measured on our own render
(as v3/set3d/measure_light.py): the frame is rendered with the key on and with the key off; on every pixel the key reaches
ratio = linear luminance(off) / linear luminance(on) = how dark that very surface is in cast shadow. Pixels are attributed to
objects by casting the camera ray of each pixel into the scene. Also: hue of the lit and the shaded colour, frame tone."""
import sys, os, json, math
import numpy as np, cv2, bpy
from mathutils import Vector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tower as T

def lin(a): a = a / 255.0; return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
def Y(a): return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
def hsv_of(c):
    h = cv2.cvtColor(np.uint8([[np.clip(c, 0, 255)]]), cv2.COLOR_RGB2HSV)[0, 0]; return int(h[0]) * 2, round(h[1] / 255, 2), round(h[2] / 255, 2)

def object_map(cam, W, H):
    sc = bpy.context.scene; dg = bpy.context.evaluated_depsgraph_get(); fr = cam.data.view_frame(scene=sc)
    tr, br, bl, tl = [cam.matrix_world @ v for v in fr]; o = cam.matrix_world.translation; ids = np.full((H, W), '', dtype=object)
    for j in range(H):
        for i in range(W):
            u, v = (i + 0.5) / W, (j + 0.5) / H; p = tl + (tr - tl) * u + (bl - tl) * v; d = (p - o).normalized(); org = o.copy()
            for _ in range(4):
                hit, loc, n, fi, ob, mw = sc.ray_cast(dg, org, d, distance=500)
                if not hit: break
                nm = ob.original.name
                if nm.startswith('actor_') or 'glow' in nm or nm in ('plate', 'sky'): org = loc + d * 1e-3; continue
                ids[j, i] = nm; break
    return ids

def run(preset='DAY', cam='square_low', quality='final', stage=True):
    A = T.build(preset); sc = bpy.context.scene; T.setup_render(sc, quality); T.set_rod(2); sc.cycles.samples = 24
    cs = A['cams'][cam]; c = T.make_camera(cs)
    if stage: T.stage_placeholders(A, T.STAGING[cam], cs['loc'])
    sc.render.use_compositing = False                                  # measure the render itself (no bloom, no grade)
    d = os.path.join(T.WORK, 'measure'); os.makedirs(d, exist_ok=True); on_p = os.path.join(d, '%s_%s_on.png' % (preset, cam)); off_p = os.path.join(d, '%s_%s_off.png' % (preset, cam))
    T.render(on_p); T.STATE['sun'].hide_render = True; T.render(off_p); T.STATE['sun'].hide_render = False
    on = cv2.cvtColor(cv2.imread(on_p), cv2.COLOR_BGR2RGB).astype(np.float64); off = cv2.cvtColor(cv2.imread(off_p), cv2.COLOR_BGR2RGB).astype(np.float64)
    H, W = on.shape[:2]; s = 4; ids = object_map(c, W // s, H // s)
    lon, loff = Y(lin(on)), Y(lin(off)) + 1e-5
    r = lon / loff - 1.0; rmax = cv2.dilate(r.astype(np.float32), np.ones((41, 41), np.uint8)); v = np.clip(r / np.maximum(rmax, 1e-3), 0, 1)
    lit = (r > 0.3) & (v > 0.92); sm = lambda a: a[s // 2::s, s // 2::s][:H // s, :W // s]
    res = {}
    for nm in sorted(set(ids.ravel()) - {''}):
        m = (ids == nm) & sm(lit)
        if m.sum() < 30: continue
        rat = sm(loff)[m] / sm(lon)[m]
        res[nm] = dict(n=int(m.sum()), ratio_lin_median=round(float(np.median(rat)), 3), lit=hsv_of(sm(on)[m].mean(0)), shade=hsv_of(sm(off)[m].mean(0)))
    out = dict(preset=preset, cam=cam, surfaces=res)
    print(json.dumps(out, indent=0)); json.dump(out, open(os.path.join(d, '%s_%s.json' % (preset, cam)), 'w'), indent=1)
    return out

if __name__ == '__main__':
    a = sys.argv[1:]; run(a[0] if a else 'DAY', a[1] if len(a) > 1 else 'square_low', a[2] if len(a) > 2 else 'preview')

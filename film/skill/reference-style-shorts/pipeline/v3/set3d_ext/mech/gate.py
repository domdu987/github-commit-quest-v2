#!/usr/bin/env python3
"""gate.py : build-order step 2, the corridor_cam gate. One still (or a few) of the corridor view: lens h D above the wall map,
6000 px map, pressure walls at wall_height, up = wall normal, office_grey.
    python3 gate.py <out_dir> <wall_height> <lens_h> [scale] [samples] [u_lens ...]"""
import os, sys, time, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
import office_mech as M
S, X = M.S, M.X
import office_light as OL

def setup(wall_height, scale=0.5, samples=6):
    A = S.build('INTERIOR_DAY'); PA = X.build(A, hi_map=True); MA = M.build(A, PA, wall_height=wall_height); OL.apply('office_grey')
    sc = bpy.context.scene; S.setup_render(sc, 'final'); sc.cycles.samples = samples; sc.render.resolution_percentage = int(scale * 100)
    sc.render.threads = 2
    S.set_track(1, 0); X.set_chalk(1.0); [X.set_ghost(i, 1.0, 0.35) for i in range(1, 7)]; X.set_label(1.0)
    X.set_spinner(u=0.10, angle=30, wobble=2)
    for sd in 'EW': M.set_wall(sd, rise=4, slide=1, lock=1, fade=1)
    M.set_lane(1.0, glow=0.15); M.set_compass(1.0); M.set_speed_sign(1.0)
    return A, PA, MA, sc

if __name__ == '__main__':
    out = sys.argv[1]; wh = float(sys.argv[2]); h = float(sys.argv[3]); scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
    smp = int(sys.argv[5]) if len(sys.argv) > 5 else 6; us = [float(x) for x in sys.argv[6:]] or [-0.12]
    os.makedirs(out, exist_ok=True); A, PA, MA, sc = setup(wh, scale, smp); log = []
    for u in us:
        S.make_camera(M.corridor(u_lens=u, h=h))
        p = os.path.join(out, 'gate_w%.2f_h%.2f_u%.3f.png' % (wh, h, u)); t = time.time(); S.render(p); log.append((p, time.time() - t))
    print(json.dumps(log))

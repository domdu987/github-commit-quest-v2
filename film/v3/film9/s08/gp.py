#!/usr/bin/env python3
"""gp.py shot:g:px:py[:z] ... -- the world ground point under a pixel (720x1280) of the take camera (for staging)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shot as S
Tk = S.Take("preview"); sc = Tk.scene; sc.render.resolution_x, sc.render.resolution_y = 720, 1280
for a in sys.argv[1:]:
    p = a.split(':'); shot, g, px, py = int(p[0]), int(p[1]), float(p[2]), float(p[3]); z = float(p[4]) if len(p) > 4 else 0.0
    f = S.bf(shot, g); loc, look = S.cam_of(shot, g); Tk.key_cam(f, loc, look, lens=S.LENS[shot]); sc.frame_set(f)
    tr, br, bl, tl = Tk.cam.data.view_frame(scene=sc); mw = Tk.cam.matrix_world
    q = tl.lerp(tr, px / 720.0).lerp(bl.lerp(br, px / 720.0), py / 1280.0)
    o = mw.to_translation(); d = (mw @ q) - o; t = (z - o.z) / d.z
    print(a, tuple(round(c, 2) for c in (o + d * t)))

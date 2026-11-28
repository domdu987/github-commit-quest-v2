"""S056 (class A)  'วิ่งหนีสุดชีวิต'  -- M, 50 mm, tracking right at car-roof height (the camera floats along south of his
line, over the roofs).  James sprints off the SUV's far edge, takes one long step across the gap of road between the
lanes onto the lane-1 car, lands and runs on, every footfall planted on steel (drawn on ones here: the camera tracks him); terrified, eyes back over his shoulder.
No delivery box on his back (it lies on the deck where the hook left it)."""
import os, sys, importlib.util
from epbase import *


def lib():
    m = sys.modules.get("sc02c_lib")
    if m is None:
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "s050.py")
        sp = importlib.util.spec_from_file_location("sc02c_lib", p); m = importlib.util.module_from_spec(sp)
        sys.modules["sc02c_lib"] = m; sp.loader.exec_module(m)
    return m


L = lib()
LOC = "X1"
DEPS = [L.LIBF]
CLASS = "A"
CAST = ["c_james"]
PPD = {"c_james": 360}
P0, P1 = (9.00, 2.50), (14.20, -1.00)                         # corner frame: the SUV l2_b's east edge -> over the gap -> l1_a's roof


def setup(F):
    L.prep(F, alarm=True)
    L.nudge_cone(F)


def frame(F, g, t, u):
    G = F.c_geo
    L.always(F, all_extras=True)
    t0 = T0(F)
    tt = C.on_twos(t)
    tau = tt - t0
    jm = F.c_james
    a, b = L.C_(G, *P0), L.C_(G, *P1)
    tk = L.take_cached(F, "james", lambda: L.roof_take(F, jm, a, b, stride=2.20, speed=9.4))
    d = (b - a); d.z = 0.0; d.normalize()
    sw = Vector((d.y, -d.x, 0.0))                              # the side of his line away from the lens' look (south-west)
    if sw.dot(G.n) > 0: sw = -sw
    tc = t - t0
    xr, zr = tk.root(min(tc + 0.04, tk.dur))
    pos = a + d * (xr * jm.a.sc)
    mid = (a + b) * 0.5
    cam = pos + sw * 3.6 - d * 0.25
    cam.z = 3.55
    F.camera(cam, pos + Z(zr * jm.a.sc + 1.95) + d * 0.12, F.pick(50, 40), focus=pos + Z(zr * jm.a.sc + 1.6), k=7.0, kmax=20, shake=hand_cam(t, 0.10, 2.0))   # integration 11-28: tracking, not handheld (was 0.30)
    L.seq_put(F, jm, tk, min(tc, tk.dur), a, d, view="side", upd=dict(expr="terrified", blink=0, visor="down", gaze=(-1.5, -0.1)))
    F.fill("c_jfill", pos + Z(3.4) + sw * 2.2, 220.0, (0.78, 0.86, 1.0), 0.8)
    return L.rig_post()


def late(F, g, t, u):
    if once(F):
        L.no_lamp(F)
        F.shadows(L.C_(F.c_geo, 11.0, 1.0, 1.0))

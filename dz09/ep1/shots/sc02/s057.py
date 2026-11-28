"""S057 (class B)  'มันกระโจนตามไป'  -- W, 24 mm, locked, from the road south of the jam looking north.  The junior comes in
from the left at a sprint, springs onto the SUV's flank and up onto its roof (crouch, lunge, crouch on twos) and goes
after the rider, left to right; beyond, James drops off the far side of the lane-1 car and is gone behind it.  The junior
stops crouched at the SUV's far edge, head hunting on twos (rule 7: lost behind cover)."""
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
CLASS = "B"
CAST = ["c_jun", "c_james"]
JA, JB = (4.30, 0.45), (9.45, 0.05)                          # the junior: the lane-3 road -> up the SUV's flank -> its east edge
RA, RB = (14.20, -1.00), (15.70, -1.30)                       # James: l1_a's roof -> down its far (east) side, where he crouches
CAM, LOOK = (6.30, -11.80, 2.35), (10.10, 0.00, 1.90)      # 11-28 fix pass: LOOK was o 11.70 at 24 mm: the junior ran along the
# left edge (face off frame at the start, cut at k12, sweep + gate); 21 mm aimed 1.6 D further left holds his spring and run


def setup(F):
    L.prep(F, alarm=True)
    L.nudge_cone(F)


def frame(F, g, t, u):
    G = F.c_geo
    L.always(F, all_extras=True)
    t0 = T0(F)
    tt = C.on_twos(t)
    tau = tt - t0
    jm, jn = F.c_james, F.c_jun
    F.camera(L.C_(G, *CAM), L.C_(G, *LOOK), F.pick(21, 22), focus=L.C_(G, 9.0, 0.0, 2.0), k=5.0, kmax=16, shake=hand_cam(t, 0.04, 0.7))
    # ---- the junior
    a, b = L.C_(G, *JA), L.C_(G, *JB)
    tj = L.take_cached(F, "jun", lambda: L.roof_take(F, jn, a, b, stride=2.30, speed=9.6))
    d = (b - a); d.z = 0.0; d.normalize()
    run_end = tj.dur - 0.5
    if tau < run_end:
        L.seq_put(F, jn, tj, tau, a, d, view="side", upd=dict(expr="lunging", blink=0, **L.claws((0.75, 0.10), (0.55, 0.30))))
    else:                                                      # stopped at the edge, crouched, the head hunting on twos
        L.seq_put(F, jn, tj, tj.dur, a, d, view="side")
        k = int((tau - run_end) * 12)
        gx = (1.5, 1.5, -1.3, -1.3, 0.4, 0.4, 1.6)[k % 7]
        p2 = dict(jn.pose_d)
        p2.update(expr="searching", gaze=(gx, 0.2), lean=18.0, head=(0, 6 if k % 3 else -4, 0.0, 0.0), **L.claws((0.40, 0.60), (0.30, 0.70)))
        jn.set(**p2)
    # ---- James: off the lane-1 car's far side, crouched behind it
    ra, rb = L.C_(G, *RA), L.C_(G, *RB)
    tr = L.take_cached(F, "james", lambda: L.roof_take(F, jm, ra, rb, stride=1.90, speed=8.0))
    dr = (rb - ra); dr.z = 0.0; dr.normalize()
    if tau < tr.dur - 0.25:
        L.seq_put(F, jm, tr, tau, ra, dr, view="side", upd=dict(expr="terrified", blink=0, visor="down"))
    else:
        jm.hide()                                              # down behind the lane-1 car's body: out of sight (rule 7)
    F.fill("c_jfill", Vector(jn.loc) + Z(3.2) - G.n * 2.0, 300.0, (0.78, 0.86, 1.0), 0.8)
    return L.rig_post(exposure=1.95)                           # integration 11-28: the lower half was near black at 1.6


def late(F, g, t, u):
    if once(F):
        L.no_lamp(F)
        F.shadows(L.C_(F.c_geo, 9.0, 0.0, 1.0))

"""S059 (class B)  'ทั้งทางด่วน / มีแต่คนวิ่งหนี'  -- EW, 24 mm, locked, high on the east side of the jam looking west-north-
west up the expressway (north = screen-right).  Everybody runs north between the stopped cars, left to right: the nine
living bystander roles (the green rider is James) in the lane gaps, two of them going over a car side-on, and eight
back-lit repeats as dark silhouettes further up the road toward the bus.  Their feet are planted; from this height the
nearer cars cover most legs.  Beacons, hazards, the alarm taxi, sodium, the skyline."""
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
CAST = L.CAST_CROWD
CAM, LOOK = (1.5, 55.0, 10.0), (-11.0, 66.0, 0.5)              # world
#   role, lane-gap x, y at the first frame, run preset, phase, expression
RUN = [("c_x1", -6.55, 57.5, "praew", 0.10, "terrified"), ("c_x2", -12.35, 57.0, "tos", 0.55, "scared"),
       ("c_x4", -6.55, 62.0, "praew", 0.70, "terrified"), ("c_x5", -12.35, 61.5, "kong", 0.30, "terrified"),
       ("c_x6", -17.70, 58.5, "james", 0.62, "scared"), ("c_x8", -12.35, 65.5, "tos", 0.20, "terrified"),
       ("c_x9", -17.70, 64.0, "praew", 0.90, "scared")]
VAULT = [("c_x3", -15.00, 63.5, 79.0, 8.2), ("c_x7", -3.45, 57.5, 71.5, 8.6)]   # over l3_d and l1_c, side-on
SIL = [(-6.55, 82.0), (-12.35, 80.0), (-17.7, 86.0), (-9.4, 88.5), (-6.55, 92.0), (-12.35, 90.5), (-3.4, 95.0), (-17.7, 96.0)]


def setup(F):
    L.prep(F, alarm=True)
    L.nudge_cone(F)


def frame(F, g, t, u):
    G = F.c_geo
    L.always(F, all_extras=True)
    t0 = T0(F)
    tt = C.on_twos(t)
    tau = tt - t0
    F.camera(Vector(CAM), Vector(LOOK), F.pick(24, 22), focus=Vector((-11.0, 66.0, 1.2)), k=4.0, kmax=12, shake=hand_cam(t, 0.02, 0.5))
    north = Vector((0.0, 1.0, 0.0))
    for key, x, y0, who, ph, ex in RUN:
        a = getattr(F, key)
        cyc = L.take_cached(F, key, lambda a=a, who=who, ph=ph: L.gait9.Run(a.a.spec, who, phase=ph))
        L.seq_put(F, a, cyc, tau, Vector((x, y0, 0.0)), north, view="side", upd=dict(expr=ex, blink=0))
    for key, x, y0, y1, sp in VAULT:
        a = getattr(F, key)
        tk = L.take_cached(F, key, lambda a=a, x=x, y0=y0, y1=y1, sp=sp: L.roof_take(F, a, Vector((x, y0, 0)), Vector((x, y1, 0)), stride=2.1, speed=sp))
        L.seq_put(F, a, tk, min(tau + 0.15, tk.dur), Vector((x, y0, 0.0)), north, view="side", upd=dict(expr="terrified", blink=0))
    for sl, (x, y0) in zip(L.sils(F), SIL):
        sl.frame(tt, (x, y0 + sl.run.v * sl.sc * tau, 0.0), F.cam)
    return L.rig_post()


def late(F, g, t, u):
    if once(F):
        L.no_lamp(F)
        F.shadows(Vector((-10.0, 65.0, 1.0)))

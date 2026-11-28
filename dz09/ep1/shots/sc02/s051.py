"""S051 (class A)  'ก้องเอาเครื่องตัดขวาง'  -- CU, 50 mm, handheld, the camera gives ground with Kong.  The cutter held across
his chest as a bar in both gloves; the junior's teeth close on the steel arm under the jaws, his claws on Kong's forearms;
Kong's strained face behind the tool.  They rock on twos; Kong is pushed back a hand's width.  Steel only: no bite on Kong."""
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
CLASS = "A"
CAST = ["c_kong", "c_jun"]
DEPS = [L.LIBF, L.sc02_faces.FILE]
PPD = {"c_kong": 420, "c_jun": 420}


def setup(F):
    L.prep(F, alarm=True)
    L.nudge_cone(F)


def frame(F, g, t, u):
    G = F.c_geo
    L.always(F, all_extras=True)
    t0 = T0(F)
    tt = C.on_twos(t)
    tau = tt - t0
    back = 0.14 * smooth(ramp(tau, 0.15, 1.30))              # Kong gives ground
    w = math.sin(2 * math.pi * 2.6 * tau)                     # the struggle, on twos
    kloc = G.KB + G.tail * back
    mid = kloc + G.n * 0.30 + Z(2.30)
    sh = tuple(a + b for a, b in zip(hand_cam(t, 0.55, 2.4), (0.25 * w, 0.18 * w, 0.0)))
    F.camera(mid + G.out * 4.35 + G.n * 0.95 + Z(0.05), mid, F.pick(50, 40), focus=mid, k=8.0, kmax=22, shake=sh)
    bite = smooth(ramp(tau, 0.12, 0.30))                      # the teeth close on the steel
    L.block(F, t, kloc, push=w, tilt=166.0 + 3.0 * w, grip=(0.40 + 0.03 * w, 0.66), along=0.95, kexpr="angry", jexpr="z_snarl_o" if bite > 0.5 else "z_snarl",
            klean=-6.0 - 4.0 * back / 0.14, jlean=26.0 + 2.0 * w, jhead=(0, -10 + 3 * w, 0.08, 0.0))
    F.c_kong.breath = 0.010 * math.sin(t * 5.0)
    return L.rig_post()


def late(F, g, t, u):
    if once(F):
        L.work_lamp(F, [F.c_kong.head(), F.c_jun.head()], acts=(F.c_kong, F.c_jun))

"""S060 (class B)  'กับพวกที่ไล่กัด'  -- MW, 35 mm, light handheld.  At the flashing alarm taxi up the road: an infected woman
in office clothes (blouse, bun) slams a running man back against the taxi's rear door and bites at his shoulder, both
upright, his hands at her face; behind them another infected goes over the taxi's boot on hands and feet toward them.
Every head stays under a tenth of the frame (no wound is read)."""
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
CAST = L.CAST_S60
CAM, LOOK = (-9.55, 53.2, 2.00), (-6.25, 46.20, 1.50)        # world
MAN, WOMAN = (-5.80, 46.50), (-6.50, 46.72)
OVER = ((-1.55, 43.95), (-7.20, 43.95))                       # the second infected: east of the taxi -> over the boot -> west


def setup(F):
    L.prep(F, alarm=True)
    L.nudge_cone(F)


def frame(F, g, t, u):
    G = F.c_geo
    L.always(F, all_extras=True)
    t0 = T0(F)
    tt = C.on_twos(t)
    tau = tt - t0
    man, wom, inf = F.c_x7, F.c_inf13, F.c_inf9
    sh = tuple(a + b for a, b in zip(hand_cam(t, 0.30, 1.6), hand_cam(t, 1.2 * max(0.0, 1 - abs(t - t0 - 0.30) / 0.12), 9.0, 1.0)))
    F.camera(Vector(CAM), Vector(LOOK), F.pick(35, 30), focus=Vector((-6.0, 46.6, 1.5)), k=6.0, kmax=18, shake=sh)
    M, Wp = Vector((MAN[0], MAN[1], 0.0)), Vector((WOMAN[0], WOMAN[1], 0.0))
    slam = smooth(ramp(tau, 0.08, 0.30))
    w = math.sin(2 * math.pi * 2.2 * tau)
    # the man: running south along the taxi, caught and slammed back against the rear door
    mloc = M + Vector((0.0, 0.9, 0.0)) * (1 - slam) + Vector((-0.25, 0.0, 0.0)) * (1 - slam)
    if slam < 0.5:
        mp = dict(expr="terrified", blink=0, legs="step", lean=10.0, arm_n=dict(hand=(0.45, 0.45), elbow=None, hand_shape="open"),
                  arm_f=dict(hand=(-0.35, 0.55), elbow=None, hand_shape="open"))
        man.set(loc=tuple(mloc), face=facing(Vector((0.0, -1.0, 0.0))), view="side", s=None, **mp)
    else:
        mp = dict(expr="terrified", blink=0, legs="wide", lean=-12.0 - 3.0 * w, head=(0, -10 + 4 * w, -0.04, 0.0),
                  arm_n=dict(hand=(0.55, -0.15 + 0.06 * w), elbow=None, hand_shape="open"), arm_f=dict(hand=(0.40, 0.05 - 0.05 * w), elbow=None, hand_shape="open"))
        man.set(loc=tuple(mloc), face=facing(Wp - M), view="q", s=None, **mp)
    man.a.walk_lock = None
    # the infected woman: from the left into him; then her head goes at his shoulder on twos
    wloc = Wp + Vector((-0.9, 0.5, 0.0)) * (1 - slam)
    bite = 0.5 + 0.5 * w
    wp = dict(expr="bite" if bite > 0.5 else "lunging", blink=0, legs="lunge", lean=24.0 + 6.0 * bite, head=(0, -10, 0.10 * bite, 0.04 * bite),
              arm_n=dict(hand=(0.80, -0.05), elbow=None, hand_shape="claw"), arm_f=dict(hand=(0.70, 0.12), elbow=None, hand_shape="claw"))
    wom.set(loc=tuple(wloc), face=facing(M - Wp), view="side", s=None, **wp); wom.a.walk_lock = None
    # the second one, over the boot on hands and feet
    a, b = Vector((OVER[0][0], OVER[0][1], 0.0)), Vector((OVER[1][0], OVER[1][1], 0.0))
    tk = L.take_cached(F, "over", lambda: L.roof_take(F, inf, a, b, stride=1.80, speed=7.5))
    d = b - a; d.normalize()
    L.seq_put(F, inf, tk, min(tau + 0.10, tk.dur), a, d, view="side",
              upd=dict(expr="lunging", blink=0, lean=52.0, hip=(0.0, 0.35), head=(0, -30, 0.12, 0.0), arm_n=dict(hand=(0.55, 1.25), elbow=None, hand_shape="claw"),
                       arm_f=dict(hand=(0.30, 1.35), elbow=None, hand_shape="claw")))
    return L.rig_post()


def late(F, g, t, u):
    if once(F):
        L.no_lamp(F)
        F.shadows(Vector((-5.5, 47.0, 1.0)))
    F.fill("c_tfill", Vector((-8.0, 49.5, 3.2)), 260.0, (0.85, 0.90, 1.0), 0.8)

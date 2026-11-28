"""S034 (class A)  'แต่เลือด / ไหลไม่หยุด'  -- M two-shot, 35 mm, slow push 0.4 D.  The junior seated in front of the truck's rear
wheel; Kong crouched at his knees presses the gauze pad from his hip pouch on the neck with both gloves; the cutter
stands on its battery end by Kong's knee, three green LEDs lit."""
from epbase import *
import os, sys, importlib.util


def lib():
    """the range's small library lives in s025.py (see its docstring)."""
    if "ep1_sc02_s025_lib" not in sys.modules:
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "s025.py")
        sp = importlib.util.spec_from_file_location("ep1_sc02_s025_lib", p); m = importlib.util.module_from_spec(sp)
        sys.modules["ep1_sc02_s025_lib"] = m; sp.loader.exec_module(m)
    return sys.modules["ep1_sc02_s025_lib"]


L = lib()
DEPS = [L.__file__]
LOC = "X1"
CLASS = "A"
PPD = {"e1_jun_gauze0": 300, "e1_kong_clean": 300}


def setup(F):
    L.kit(F); L.junior(F, "gauze0"); L.kong(F)


def frame(F, g, t, u):
    jun = L.junior(F, "gauze0"); kg = L.kong(F)
    Wm = L.wheel(F)
    e = smooth(u)
    mid = Wm.seat + Wm.out * 0.40 + Wm.tail * 0.55
    # from the lane, 1.1 D north of side-on and low: both faces in profile with air between them (from straight across
    # Kong's lean put his head over the junior's), the big tyre behind them, the cutter standing by Kong's knee
    loc = mid + Wm.out * (4.45 - 0.40 * e) - Wm.tail * 1.10 + Z(1.15)
    F.camera(loc, mid + Z(1.08) + Wm.tail * 0.10, F.pick(33, 28), focus=mid + Z(1.2), k=6.0, kmax=20, shake=hand_cam(t, 0.08, 1.2))
    L.alarm_on(F, t)
    F.door(DOOR_OPEN)
    F.kong.hide(); F.crew.hide(); F.drv.hide(); F.drv_out.hide()
    L.press_pair(F, t, jun, kg, kview="side", lean=12, slump=0.40)
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        jun = L.junior(F, "gauze0"); kg = L.kong(F)
        L.wheel_lamp(F, [kg.head(), jun.head()])
        F.shadows(L.wheel(F).seat + Z(1.2))

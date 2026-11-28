"""S037 (class A)  'ลมหายใจน้อง / สั้นลง / ถี่ขึ้น'  -- CU 3/4, 66 mm, locked.  The junior against the wheel, one step toward grey:
the chest pumps at 3 Hz (faster from 'ถี่ขึ้น'), the shoulders shake, lids half down, the mouth a little open; the
soaked pad at his neck under Kong's gloves at the frame edge."""
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
CAMZ, KOUT, KTAIL, KHIP, KLEAN = 1.70, 1.20, 1.10, 0.90, 30      # Kong kneels low, off the left edge: his forearm comes in under the face (ep1/chk/a25/dbg37.py)

PPD = {"e1_jun_grey1": 600, "e1_kong_blood": 360}


def setup(F):
    L.kit(F); L.junior(F, "grey1"); L.kong(F, True)


def frame(F, g, t, u):
    Wm = L.wheel(F)
    jun = L.junior(F, "grey1"); kg = L.kong(F, True)
    tt = C.on_twos(t)
    hc = Wm.seat + Z(1.52) + Wm.tail * 0.10
    loc = Wm.seat + Wm.out * 3.0 - Wm.tail * 0.55 + Z(CAMZ)                # from the north side: Kong is beyond him, only his gloves reach in
    F.camera(loc, hc + Z(-0.14) + Wm.tail * 0.18, F.pick(66, 50), roll=-1.5, focus=hc, k=9.0, kmax=24, shake=hand_cam(t, 0.05, 1.1))
    L.alarm_on(F, t)
    F.door(DOOR_OPEN)
    F.kong.hide(); F.crew.hide(); F.drv.hide(); F.drv_out.hide()
    hz = 3.0 + 1.2 * smooth(ramp(t, W("ถี่ขึ้น") - 0.2, W("ถี่ขึ้น") + 0.5))
    ph = math.sin(2 * math.pi * hz * (t - T0(F)))
    L.press_pair(F, t, jun, kg, expr_j="fading", expr_k="serious", slump=0.45, shiver=1.0, view="q", blink=1, mouth=("o", 0.25 if ph > 0 else 0.5), lean=KLEAN,
                 kloc=Wm.seat + Wm.out * KOUT + Wm.tail * KTAIL, kkw=dict(hip=(0.0, KHIP)))
    jun.breath = 0.014 * ph                                   # the chest: a vertical stretch of the card on ones
    hd = jun.pose_d["head"]
    jun.pose_d["head"] = (hd[0], hd[1], hd[2], hd[3] - 0.012 * ph)
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        jun = L.junior(F, "grey1"); kg = L.kong(F, True)
        L.wheel_lamp(F, [jun.head()])
        F.shadows(L.wheel(F).seat + Z(1.2))
        jun.a.set_glow(WARM, 0.20)
    L.aim(F, L.junior(F, "grey1").head(), dz=-0.14)

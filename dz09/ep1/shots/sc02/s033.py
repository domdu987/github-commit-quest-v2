"""S033 (class A)  'น้องพยักหน้า'  -- MCU, high, 66 mm, locked.  The junior against the wheel: two small nods on twos, `scared`,
a blink; skin still paper white; the bite a torn ring where the neck meets the shoulder, blood running into the collar."""
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
PPD = {"e1_jun_bitten": 480}


def setup(F):
    L.kit(F); L.junior(F, "bitten"); L.kong(F)


def frame(F, g, t, u):
    Wm = L.wheel(F)
    jun = L.junior(F, "bitten"); kg = L.kong(F)
    tt = C.on_twos(t); t0 = T0(F)
    hc = Wm.seat + Z(1.55) + Wm.tail * 0.10
    loc = Wm.seat + Wm.out * 2.9 + Wm.tail * 0.75 + Z(2.45)
    F.camera(loc, hc + Z(-0.10), F.pick(66, 50), roll=-1.0, focus=hc, k=9.0, kmax=24, shake=hand_cam(t, 0.06, 1.2))
    L.alarm_on(F, t)
    F.door(DOOR_OPEN)
    F.kong.hide(); F.crew.hide(); F.drv.hide(); F.drv_out.hide()
    nod = sum(max(0.0, 1 - abs(tt - (t0 + a)) / 0.13) for a in (0.30, 0.66))                         # two nods
    bl = 2 if abs(tt - (t0 + 0.50)) < 0.05 else 0
    L.sit(F, jun, t, expr="scared", slump=0.2, view="q", shiver=0.5, blink=bl, mouth=("o", 0.25), dout=0.20)
    hd = jun.pose_d["head"]
    jun.pose_d["head"] = (hd[0], hd[1] + 13 * nod, hd[2] + 0.02 * nod, hd[3] + 0.035 * nod)
    kg.hide()
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        jun = L.junior(F, "bitten")
        Wm = L.wheel(F)
        F.lamp(tuple(Wm.lamp_base - Wm.tail * 3.0)[:2], tuple(Wm.lamp_aim), 2800.0, heads=[jun.head()])   # from the north-east: the default base threw a bar of shadow across his eyes
        F.shadows(L.wheel(F).seat + Z(1.2))
        jun.a.set_glow(WARM, 0.22)
    L.aim(F, L.junior(F, "bitten").head(), dz=-0.16)

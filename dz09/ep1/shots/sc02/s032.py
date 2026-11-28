"""S032 (class A)  Kong: 'มองหน้าพี่ไว้! / ได้ยินไหม!'  -- CU, 50 mm, light handheld.  Kong crouched at the junior's knees, face
to him; the line is Kong's (lip sync from the cut's mouth track), a glove on the junior's shoulder gives the second
phrase a shake; brows hard, then the mouth shuts and he watches.  The junior is a shoulder and a crest of hair at the
frame's right edge."""
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
PPD = {"e1_kong_clean": 480, "e1_jun_bitten": 300}


def setup(F):
    L.kit(F); L.junior(F, "bitten"); L.kong(F)


def frame(F, g, t, u):
    Wm = L.wheel(F)
    kg = L.kong(F); jun = L.junior(F, "bitten")
    tt = C.on_twos(t)
    hc = Wm.kong + Z(1.92) - Wm.tail * 0.22
    loc = Wm.kong + Wm.out * 2.75 - Wm.tail * 1.25 + Z(1.80 + 0.04 * u)
    look = hc - Wm.tail * 0.12 + Z(-0.12)
    F.camera(loc, look, F.pick(50, 40), roll=1.5, focus=hc, k=9.0, kmax=24, shake=hand_cam(t, 0.30, 1.9))
    L.alarm_on(F, t)
    F.door(DOOR_OPEN)
    F.kong.hide(); F.crew.hide(); F.drv.hide(); F.drv_out.hide()
    t1 = W("มองหน้าพี่ไว้!"); t2 = W("ได้ยินไหม!"); t_end = W("ได้ยินไหม!", end=True)
    shake = math.sin((tt - t2) * 2 * math.pi * 3.0) * max(0.0, 1 - abs(tt - t2 - 0.25) / 0.35)      # the hand shakes the shoulder on the second phrase
    spoke = tt > t_end + 0.08
    # 'มองหน้าพี่ไว้!' is shouted (plan: `shouting`; its squint eyes and the open-D mouth read as laughing on this face, so
    # `worried` brows with a ROUND mouth one size up); 'ได้ยินไหม!' (`serious`), searching his face
    ex = "worried" if tt < t2 - 0.04 else "serious"
    kw = dict(expr=ex, head=(0, 2 + 3 * shake - (4 if ex == "worried" else 0), 0.03 + 0.01 * shake, 0.0), lean=16 + 2 * shake + (3 if ex == "worried" else 0),
              arm_n=dict(hand=(0.80, 0.50 + 0.03 * shake), elbow=None, hand_shape="glove"), arm_f=dict(hand=(0.40, 0.55), elbow=None, hand_shape="glove"))
    m = talk("kong", g).get("mouth", 0.0)
    if m: kw["mouth"] = ("o", min(1.0, 0.25 + 1.0 * m))
    L.kong_crouch(F, kg, t, **kw)
    if not spoke: kg.pose_d["blink"] = 0
    L.sit(F, jun, t, expr="pain", slump=0.25, shiver=0.6, idx=3)      # index 3: he takes the lens blur (a soft edge at frame right)
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        kg = L.kong(F); jun = L.junior(F, "bitten")
        L.wheel_lamp(F, [kg.head(), jun.head()])
        F.shadows(L.wheel(F).kong + Z(1.4))
        kg.a.set_glow(WARM, 0.22)

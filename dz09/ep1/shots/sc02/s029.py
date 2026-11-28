"""S029 (class B)  'สัญญาณกันขโมย / ดังลั่น'  -- M, 35 mm, slow push 0.3 D.  The taxi's tail: indicators and headlamps flashing in
the alarm rhythm (10 frames), amber pulsing on the wet road and on the cars ahead.  In the foreground the driver, where S028
left him (slid down the tail, his back to the car), rises into the lower half of the frame as a DARK SHAPE against the
lamps (the flat look is turned down for this shot and he gets an amber rim that pulses with the lamps), and on 'ดังลั่น'
turns round to the lights in three drawings on twos (front, 3/4, back).  Locked off, slow push 0.3 D.""" 
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
CLASS = "B"
PPD = {"driver_out": 300}


def setup(F):
    L.kit(F)


AMBER = (1.0, 0.55, 0.12)


def frame(F, g, t, u):
    X = L.taxi(F)
    tt = C.on_twos(t); t0 = T0(F)
    e = smooth(u)
    # 11-28 fix pass (director: "a black figure covers almost half the frame in the foreground"): the camera stands 7.2 D
    # back (was 3.75) and he is at the LEFT corner of the tail (was 0.55 D left of centre): the whole tail with its four
    # lamps fills the frame and he is a dark figure in the lower-left quarter, about a third of the frame high
    p = X.mark - X.right * 1.45
    cam = X.mark - X.fwd * (7.2 - 0.30 * e) + X.right * 0.15 + Z(1.00)
    look = X.tail + X.fwd * 0.6 + X.right * 0.10 + Z(1.15)
    F.camera(cam, look, F.pick(35, 30), roll=1.5, focus=X.tail + Z(1.2), k=6.0, kmax=18, shake=hand_cam(t, 0.08, 1.2))
    F.door(DOOR_OPEN)
    L.alarm_on(F, t)
    L.rock(F, 0.0)
    for e_ in F.extras:
        if e_.name in ("extra9",): e_.visible = False
    F.kong.hide(); F.crew.hide(); F.drv.hide()
    rise = smooth(ramp(tt, t0 + 0.10, t0 + 1.10))
    tw = W("ดังลั่น")
    w = math.sin(tt * 2 * math.pi * 1.3)
    turn = tt - tw                                           # front -> 3/4 -> back, on twos
    if turn < 0:
        view, s, face = "front", 1, facing(-X.fwd)
    elif turn < 4 / 24.0:
        view, s, face = "q", 1, facing(X.right)
    else:
        view, s, face = "back", 1, facing(X.fwd)
    hip = 0.85 * (1 - rise)
    pose = dict(expr="still" if turn < 0 else "head_lift", legs="crouch" if hip > 0.25 else "stand", hip=(0.0, hip),
                lean=(14 - 10 * rise) if view != "back" else 4, head=(0, (16 - 22 * rise if turn < 0 else -6) + 2 * w, 0.0, 0.0),
                arm_r=dict(hand=(0.42, 0.70 - 0.25 * rise), elbow=None, hand_shape="claw"),
                arm_l=dict(hand=(0.45, 0.75 - 0.30 * rise), elbow=None, hand_shape="claw")) if view != "q" else dict(
                expr="head_lift", legs="stand", hip=(0.0, hip), lean=6, head=(0, -8, 0.0, 0.0), arm_n="claw", arm_f="hang")
    F.drv_out.set(loc=p, face=face, view=view, s=s, **pose)
    # backlit: the lamps are behind him, so the flat cards get almost no fill (a silhouette); the rim is his glow halo
    return {"exposure": 1.6, "sharp_idx": [2], "flat": {"AMB": 0.03, "DIR": 0.0, "BACK": 0.0}}


def late(F, g, t, u):
    if once(F):
        X = L.taxi(F)
        F.lamp(None, None, hide=True)
        F.shadows(X.mark + Z(1.4))
    on = (g % 10) < 5                                        # x1.ALARM_PERIOD: 5 frames on, 5 off
    F.drv_out.a.set_glow(AMBER, 0.95 if on else 0.30)

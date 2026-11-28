"""S028 (class B)  'ไปชนรถคันข้างๆ'  -- W low, 24 mm, locked, 4 f impact shake.  The driver comes through the air from the left
(the south, where S027 threw him) and slams back-first into the tail of the taxi in lane 1; the car rocks on its springs;
he slides down the bumper and is already twisting to get up.  The alarm's first flash is on the last frames.
(Plan: 'the flank of a white hatchback in the next lane'.  The set has no car beside the wreck: the alarm car of
ep1/sets is the taxi `l1_b`, 13 D north, and coming from the wreck he meets its tail.  No running extras: see report.)"""
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
K_HIT = 6                                                    # frames after the cut


def setup(F):
    L.kit(F)


def frame(F, g, t, u):
    X = L.taxi(F)
    t0 = T0(F); dt = t - t0 - K_HIT / 24.0
    tt = C.on_twos(t); dtt = tt - t0 - K_HIT / 24.0
    imp = max(0.0, 1 - dt / (4 / 24.0)) if dt >= 0 else 0.0
    cam = X.tail - X.fwd * 4.6 + X.right * 1.55 + Z(0.55)
    look = X.tail + X.fwd * 0.6 - X.right * 0.25 + Z(1.30)
    F.camera(cam, look, F.pick(24, 20), roll=2.0, focus=X.tail + Z(1.2), k=4.0, kmax=14, shake=hand_cam(t, 3.0 * imp, 11.0, 2.0) if imp > 0 else None)
    F.door(DOOR_OPEN)
    L.alarm_on(F, t)
    for e in F.extras:
        if e.name in ("extra9",): e.visible = False          # the man who stood at this taxi has run
    F.kong.hide(); F.crew.hide(); F.drv.hide()
    # the car on its springs: a kick, then a damped rock
    if dt >= 0:
        L.rock(F, 2.6 * math.exp(-3.2 * dt) * math.cos(2 * math.pi * 2.4 * dt), dip=0.05 * math.exp(-5.0 * dt))
    else:
        L.rock(F, 0.0)
    d = F.drv_out
    face = facing(-X.fwd)                                    # his back to the car
    if dt < 0:                                               # in the air, back first
        k = 1 + dt / (K_HIT / 24.0)                          # 0..1: past the lens from the left, receding into the car
        p = X.mark - X.fwd * (2.3 * (1 - k)) - X.right * (1.5 * (1 - k)) + Z(0.25 + 0.55 * math.sin(k * math.pi * 0.85))
        d.set(loc=p, face=face, view="front", s=1, expr="lunge", legs="step", lean=-10, head=(0, -14, 0, 0),
              arm_r=dict(hand=(0.75, -0.35), elbow=None, hand_shape="claw"), arm_l=dict(hand=(0.80, -0.10), elbow=None, hand_shape="claw"))
    else:
        slide = smooth(ramp(dtt, 0.10, 0.62))                # down the bumper
        up = smooth(ramp(dtt, 0.95, 1.55))                   # twisting to get up
        hip = 0.85 * slide * (1 - 0.55 * up)
        fl = 1 - smooth(ramp(dtt, 0.0, 0.35))                # arms flung wide on the impact, then dropping
        # 3/4 drawing all the way down (the front drawing's crouch splays the knees like a frog): back on the bumper, the
        # knees folding toward the lens, then one claw down on the road and the trunk coming forward to get up
        pose = dict(expr="still" if dtt > 0.25 else "lunge", legs="crouch" if slide > 0.05 else "step", hip=(0.0, hip),
                    lean=-6 * fl + 30 * up, head=(0, -16 * fl + 10 * slide - 14 * up, 0.0, 0.03 * slide),
                    arm_n=dict(hand=(0.30 + 0.45 * fl + 0.25 * up, 0.70 - 1.0 * fl + 0.20 * up), elbow=None, hand_shape="claw"),
                    arm_f=dict(hand=(0.35 + 0.40 * fl, 0.65 - 0.95 * fl - 0.20 * up), elbow=None, hand_shape="claw"))
        d.set(loc=X.mark, face=face, view="q", s=-1, **pose)
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        X = L.taxi(F)
        F.lamp(tuple((X.tail - X.fwd * 5.5 - X.right * 4.0))[:2], tuple(X.mark + Z(1.3)), 7000.0, heads=[F.drv_out.head()])
        F.shadows(X.mark + Z(1.4))

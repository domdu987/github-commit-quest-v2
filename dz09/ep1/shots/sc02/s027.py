"""S027 (class A)  'ก้องเอาเครื่องตัด / กระแทกมันกระเด็น'  -- M side, 28 mm.  Kong (screen-left, feet wide, planted) draws the
cutter back and rams it two-handed past the junior into the driver's chest on 'กระแทก'; the driver is torn off the junior
and flies north (screen-right); the camera whips 10 frames with him, loses him and comes back to the junior folding
over his neck and Kong looking after the thing.  (Plan: driver flies screen-left; mirrored, see s025.py.)"""
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
PPD = {"e1_jun_bitten": 300, "driver_out": 300, "e1_kong_clean": 300}


ROLL_SIGN = 1.0


def T_HIT():
    return W("กระแทกมันกระเด็น") + 3 / 24.0                  # the ram lands on the second syllable of 'กระแทก'


def setup(F):
    L.kit(F); L.junior(F, "bitten"); L.kong(F)


def frame(F, g, t, u):
    M = L.fight(F)
    jun = L.junior(F, "bitten"); kg = L.kong(F)
    th = T_HIT(); dt = t - th
    tt = C.on_twos(t); dtt = tt - th
    # ---- camera: side-on from the lane, 28 mm at 3.9 D (heads 12-17 % of the frame height); for 10 frames from the hit
    #      the look point whips after the flying driver (one frame behind him), then swings back over 12 frames
    FLY = 0.42                                             # seconds the driver takes to leave: 10 frames, 6 D north on a low arc
    fly_c = clamp((dt - 0.5 / 24.0) / FLY, 0.0, 1.15) if dt > 0 else 0.0
    follow = smooth(ramp(dt, 0.0, 1.5 / 24.0)) * (1 - smooth(ramp(dt, 12 / 24.0, 24 / 24.0))) if dt > 0 else 0.0
    whip = follow * clamp(fly_c / 0.5)
    imp = max(0.0, 1 - abs(dt) / (4 / 24.0)) if dt >= 0 else 0.0
    sh = hand_cam(t, 0.10, 2.4)                              # integration 11-28: the plan has no handheld here (whip pan only): no impact shake
    mid = M.jun - F.fwd * 0.80                                # integration 11-28: lens 28 -> 24 mm (Kong's face was half off the left edge, the driver's off the right)
    loc = mid + F.right * 3.9 + F.fwd * 0.20 + Z(1.40)                 # the median barrier is 5 D out: no further
    dpos = M.drv + F.fwd * (0.4 + 6.2 * fly_c)
    look = mid + Z(1.60) + (dpos - mid) * follow
    look.z = mid.z + 1.60 + 0.25 * whip
    F.camera(loc, look, F.pick(24, 24), roll=-3.0 - 6.0 * whip, focus=M.jun + Z(1.8), k=5.0, kmax=18, shake=sh)
    F.door(DOOR_OPEN)
    L.alarm_on(F, t)
    F.kong.hide(); F.crew.hide(); F.drv.hide()
    # ---- Kong: draw back (12 f before the hit), drive (4 f), hold, then lower the tool and look after the driver
    back = smooth(ramp(dt, -16 / 24.0, -6 / 24.0))
    drive = ease_out(ramp(dt, -4 / 24.0, 0.0), 2.0)
    rest = smooth(ramp(dtt, 0.40, 0.90))
    thrust = -0.35 * back * (1 - drive) + drive * (1 - 0.85 * rest)
    # the ram goes PAST the junior (between him and the lens) into the driver behind his shoulder: Kong lunges 0.4 D in and
    # the jaws lift 10 degrees, so the tool lands on the white shirt, not on the junior's chest
    lunge = 0.40 * drive * (1 - 0.6 * rest)
    L.kong_ram(F, t, g, kg, thrust=max(thrust, -0.3) if drive <= 0 else thrust, expr="resolve" if dt < 0.5 else "alarmed",
               tilt=86.0 + 10.0 * drive * (1 - rest) - 50.0 * rest, loc=M.kong + F.fwd * lunge,
               **({"mouth": ("a", 1.0)} if -0.2 < dt < 0.4 else {}))
    # ---- the pair until the hit; then the driver in the air and the junior folding
    if dt < 0:
        L.bite_pair(F, t, jun)
    else:
        fly = dt / FLY
        p = M.drv + F.fwd * (0.4 + 6.2 * min(fly, 1.15)) + Z(0.35 * math.sin(min(fly, 1.0) * math.pi) + 0.10 * min(fly, 1.0))
        # 11-28 fix pass ("the driver's legs look broken in the throw"): was legs="step" + lean -24 on a 38-degree tipped card:
        # the scissored legs crossed at the knees and the arms pointed straight up.  Now the legs trail together, knees bent,
        # the body jackknifes a little forward and the claws still reach for Kong (drawn in 2D first: chk/integ/view)
        F.drv_out.set(loc=p, face=facing(M.south), view="side", s=-1, expr="snap_open", legs=dict(foot_n=(-0.34, -0.18), foot_f=(-0.16, -0.06)),
                      lean=4, arm_n=dict(hand=(0.85, 0.15), elbow=None, hand_shape="claw"), arm_f=dict(hand=(0.70, 0.35), elbow=None, hand_shape="claw"),
                      head=(0, -14, 0, 0))
        if fly > 1.15: F.drv_out.hide()
        fold = smooth(ramp(dtt, 0.0, 0.5))
        w = math.sin(tt * 2 * math.pi * 2.2)
        pose = dict(expr="pain" if dtt > 0.12 else "scared", lean=14 + 22 * fold + 1.5 * w, legs="step", hip=(0.0, 0.10 * fold),
                    arm_n=dict(hand=(0.30, 0.55), elbow=None, hand_shape="open"), head=(0, 8 + 12 * fold, 0.03 * fold, 0.04 * fold))
        if dtt <= 0.12: pose["mouth"] = ("o", 1.0)
        pose.update(F._e1kit.D9.press_wound("q", -1))
        jun.set(loc=M.jun - F.fwd * (0.10 * fold), face=facing(M.south), view="q", s=-1, **pose)
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    dt = t - T_HIT()
    if dt >= 0 and F.drv_out.visible:                        # thrown back first: the card tips over in its own plane (feet trail)
        F.drv_out.a.pivot.rotation_euler[1] = math.radians(ROLL_SIGN * 34.0 * smooth(clamp(dt / 0.30)))
        F.drv_out.a.pivot.location = (0, 0, 0.55)
    if once(F):
        M = L.fight(F)
        jun = L.junior(F, "bitten"); kg = L.kong(F)
        F.lamp(F.P(M.b, 6.5, 7.5), M.jun + Z(1.3), 9000.0, heads=[jun.head(), kg.head()])
        F.shadows(M.jun + Z(1.5))
        jun.a.set_glow(WARM, 0.25); kg.a.set_glow(WARM, 0.22)

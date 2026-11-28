"""S030 (class A)  'มันทิ้งเหยื่อ / หันไปหาเสียง'  -- CU 3/4, 66 mm, locked, then a 5 f whip on his exit.  From over the taxi's
boot: the driver's face in the amber blink, red pin pupils; the head snaps up to the lamp; on 'หันไปหาเสียง' he throws
himself at the car and goes out past the lens along its flank toward the bonnet (screen-right).  Far behind him, small
and soft, the two men he has forgotten."""
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
PPD = {"driver_out": 480}


def CAM_Z(F, p):
    """just over the taxi's rear glass, wherever its roof line is."""
    if not hasattr(F, "_s030_z"):
        F._s030_z = max(2.45, F.top(p.x, p.y) + 0.22)
    return F._s030_z


def setup(F):
    L.kit(F); L.junior(F, "bitten"); L.kong(F)


def frame(F, g, t, u):
    X = L.taxi(F); M = L.fight(F)
    tt = C.on_twos(t); t0 = T0(F)
    tg = W("หันไปหาเสียง") + 6 / 24.0                           # the lunge, on 'หา'
    go = ease_in(ramp(t, tg, tg + 9 / 24.0), 2.0)
    whip = smooth(ramp(t, tg + 3 / 24.0, tg + 8 / 24.0))
    hd = X.mark + Z(2.30)
    cxy = X.tail + X.fwd * 2.2 - X.right * 0.60
    cam = Vector((cxy.x, cxy.y, CAM_Z(F, cxy)))
    look = hd + Z(-0.22) - X.right * (1.3 * whip) + X.fwd * (0.5 * whip)
    F.camera(cam, look, F.pick(66, 50), roll=-3.0 - 6 * whip, focus=hd, k=9.0, kmax=24, shake=hand_cam(t, 0.06, 1.6))   # integration 11-28: locked per the plan (was 0.12)
    F.door(DOOR_OPEN)
    L.alarm_on(F, t)
    L.rock(F, 0.0)
    for e_ in F.extras:
        if e_.name in ("extra9",): e_.visible = False
    F.kong.hide(); F.crew.hide(); F.drv.hide()
    snap = tt >= t0 + 8 / 24.0                                # head snaps to the lamp
    tw = math.sin(tt * 2 * math.pi * 3.1)
    p = X.mark - X.right * (1.9 * go) + X.fwd * (2.6 * go)
    if go <= 0:
        F.drv_out.set(loc=p, face=facing(X.fwd), view="q", s=-1 if not snap else 1, expr="still" if not snap else "head_lift", legs="stand", lean=0,
                      head=(0, (10 if not snap else -8) + 1.5 * tw, 0, 0), arm_n="hang" if not snap else "claw", arm_f="hang" if not snap else "claw_up")
    else:
        F.drv_out.set(loc=p, face=facing(X.fwd), view="q", s=1, expr="lunge", legs="lunge", lean=24 + 14 * go, head=(0, -10, 0.06, 0),
                      arm_n="claw_up", arm_f="claw_up")
    # the two he has left: at the wreck, the junior folded over his neck, Kong with him
    jun = L.junior(F, "bitten"); kg = L.kong(F)
    pose = dict(expr="pain", lean=34, legs="step", hip=(0.0, 0.10), arm_n=dict(hand=(0.30, 0.55), elbow=None, hand_shape="open"), head=(0, 18, 0.03, 0.04))
    pose.update(F._e1kit.D9.press_wound("q", -1))
    jun.set(loc=M.jun, face=facing(M.south), view="q", s=-1, idx=3, **pose)       # index 3: out of focus like the set behind him
    L.kong_ram(F, t, g, kg, thrust=0.1, expr="alarmed", idx=3)
    on = (g % 10) < 5                                         # x1.ALARM_PERIOD: 5 frames on, 5 off
    hp = Vector(F.drv_out.loc) + Z(2.2)
    F.fill("s030_alarm_amber", loc=hp + (cam - hp).normalized() * 1.3 + Z(-0.35), power=420.0 if on else 12.0, color=(1.0, 0.52, 0.12), size=0.25)
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    F.drv_out.a.set_glow((1.0, 0.55, 0.12), 0.55 if (g % 10) < 5 else 0.18)
    if once(F):
        X = L.taxi(F)
        F.lamp(None, None, hide=True)
        F.shadows(X.mark + Z(1.4))
    # frame the face on the drawing that was chosen: before the lunge the camera sits on his head; once he goes it holds
    # the last framing and whips (the 5 frames of the whip are added to it)
    tg = W("หันไปหาเสียง") + 6 / 24.0
    if t <= tg or not hasattr(F, "_s030_hd"):
        F._s030_hd = tuple(F.drv_out.head())
    whip = smooth(ramp(t, tg + 3 / 24.0, tg + 8 / 24.0))
    # 11-28 fix pass: the whip used to land 1.3 D right of his last head, on the empty wreck door, with Kong and the junior
    # cut in half at the left edge for the last 17 frames ("faces cut by the frame").  It now lands on the two men he left
    # (between their heads, a little low), so the shot ends on them, as S031 begins
    jun = L.junior(F, "bitten"); kg = L.kong(F)
    pair = (Vector(jun.head()) + Vector(kg.head())) * 0.5 + Z(-0.35)
    L.aim(F, Vector(F._s030_hd).lerp(pair, whip), dz=-0.03 * (1 - whip))

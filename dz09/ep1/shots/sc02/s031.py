"""S031 (class A)  'ก้องพยุงน้อง / ไปหลบหลังรถกู้ภัย'  -- MW track, 35 mm, eye level.  Kong walks the junior along the rescue
truck's lane side toward its rear wheel: the junior's arm over Kong's shoulders, Kong's far arm round his back, the
cutter hanging from Kong's near hand.  ep1/cast `gait9.SupportWalk`: both on planted feet, the junior's stride short
and dragging; blood down the junior's collar.  They move screen-LEFT (south): the truck is behind them as they go, and
the junior is drawn on the side that shows the bite (plan: screen-right; see s025.py)."""
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
PPD = {"e1_jun_bitten": 300, "e1_kong_clean": 300}
G = None
PHASE = 0.20
TRAIL = 0.30                                               # the junior half a step behind Kong (BU along the walk): his hair covered Kong's right eye


def setup(F):
    L.kit(F); L.junior(F, "bitten"); L.kong(F)


def roots(F, t):
    global G
    kg = L.kong(F); jun = L.junior(F, "bitten")
    if G is None:
        G = F._e1kit.gait9.SupportWalk(kg.a.spec, jun.a.spec, kg.a.sc, jun.a.sc)
    Wm = L.wheel(F)
    d = Wm.tail
    start = Wm.seat + Wm.out * 0.80 - d * 1.45                 # Kong ends at his mark beyond the wheel, the junior at the seat
    tw = max(t - T0(F), 0.0) + PHASE
    rk = start + d * (G.root(tw)[0] * kg.a.sc)
    rj = start + Wm.out * 0.42 + d * (G.root_b(tw)[0] * jun.a.sc - TRAIL)    # integration 11-28: TRAIL, his head cleared Kong's face only half
    return kg, jun, Wm, d, tw, rk, rj


def cam(F, g, t, u):
    kg, jun, Wm, d, tw, rk, rj = roots(F, t)
    mid = rk - d * 0.36
    loc = mid + Wm.out * 4.15 + d * 1.05 + Z(1.55)          # 14 degrees ahead of side-on: the near (junior's) head clears Kong's face
    look = mid + Z(1.58)
    return F.camera(loc, look, F.pick(35, 30), focus=mid + Z(1.8), k=6.0, kmax=20, shake=hand_cam(t, 0.08, 1.3))   # integration 11-28: tracking, not handheld (was 0.14)


def frame(F, g, t, u):
    cam(F, g, t, u)
    L.alarm_on(F, t)
    F.door(DOOR_OPEN)
    kg, jun, Wm, d, tw, rk, rj = roots(F, t)
    F.kong.hide(); F.crew.hide(); F.drv.hide(); F.drv_out.hide()
    s = None
    for a_, r in ((kg, rk), (jun, rj)):
        a = a_.a
        a.root.location = r; a.facing = facing(d)
        rel = a._cam_rel(F.cam)
        a.walk_lock = 90.0 if rel >= 0 else -90.0
        if s is None: s = -1 if rel > 0 else 1
    pk, pj = G.pose(tw, s=s, view="side")
    for p in (pk, pj):
        p.pop("view", None); p.pop("s", None); p.pop("_planted", None)
    pk.update(expr="resolve", blink=C.blink("kong", t), arm_n="hold_cutter", prop_n=dict(type="cutter", bars=3, wet=True))
    pj.update(expr="pain", blink=0)
    pj["lean"] = pj.get("lean", 0) + 7                       # hurt: the trunk folds over the step, his head drops below Kong's
    hd = pj.get("head", (0, 0, 0, 0))
    pj["head"] = (hd[0], hd[1] + 10, hd[2], hd[3])
    fa = dict(pj["arm_f"]); fx, fy = fa["fig"]
    fa["fig"] = (fx + s * 0.22 + s * TRAIL / jun.a.sc, fy + 0.26)   # the arm lies across Kong's shoulders, under his chin (it covered his jaw); + the trail
    pj["arm_f"] = fa
    kg.set(loc=rk, face=facing(d), view="side", s=s, **pk)
    jun.set(loc=rj, face=facing(d), view="side", s=s, **pj)
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        cam(F, g, 0, 0.5)
        kg = L.kong(F); jun = L.junior(F, "bitten")
        Wm = L.wheel(F)
        mid = Wm.seat + Wm.out * 0.8 - Wm.tail * 0.6
        F.lamp(tuple(mid + Wm.out * 4.6 + Wm.tail * 2.9)[:2], tuple(mid + Z(1.2)), 3200.0, heads=[kg.head(), jun.head()])
        F.shadows(mid + Z(1.5))
        cam(F, g, t, u)

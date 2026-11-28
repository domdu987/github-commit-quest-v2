"""S061 (class A)  'นี่ไม่ใช่อุบัติเหตุ / อีกต่อไปแล้ว'  -- M, 50 mm, slow push from 3.2 to 2.95 D (the plan's 2.4 D is a 33 % push; the user's 11-28 rule caps a push at about 10 %).  Kong alone at the truck's
rear corner, front, soaked, the cutter hanging from his right glove, the junior's blood on both gloves, chest heaving;
his eyes go over the road and come back: 'alarmed' settles into 'serious' as he understands."""
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
CLASS = "A"
CAST = ["c_kong"]
PPD = {"c_kong": 420}
SPOT = (0.42, -0.66)                                          # where S058 left him


def setup(F):
    L.prep(F, alarm=True)
    L.nudge_cone(F)


def frame(F, g, t, u):
    G = F.c_geo
    L.always(F, all_extras=True)
    t0 = T0(F)
    tt = C.on_twos(t)
    tau = tt - t0
    tc = t - t0
    kg = F.c_kong
    loc = L.C_(G, *SPOT)
    head = loc + Z(2.50)
    dist = lerp(3.2, 2.95, smooth(ramp(tc, 0.0, 3.2)))        # 8.5 % in subject size over the shot (user rule 11-28: at most ~10 %)
    F.camera(head + G.out * dist + G.n * 0.25 + Z(-0.18), head + Z(-0.22), F.pick(50, 40), focus=head, k=8.0, kmax=22, shake=hand_cam(t, 0.08, 0.9))
    settle = smooth(ramp(tau, 1.30, 1.70))                    # on the line's turn the face settles
    expr = "alarmed" if settle < 0.5 else "serious"
    look = [(0.0, 0.0), (-1.2, 0.0), (-1.2, 0.0), (1.1, 0.1), (1.1, 0.1), (0.0, 0.0)]
    gz = look[min(int(tau / 0.32), len(look) - 1)] if tau < 1.4 else (0.0, 0.05)
    heave = 1.0 - 0.6 * smooth(ramp(tc, 0.0, 3.0))
    pose = dict(expr=expr, blink=C.blink("c_kong", t), gaze=gz, legs="stand", lean=2.0, head=(0, 4 * settle - 2, 0.0, 0.0),
                arm_l=dict(hand=(0.20, 0.82), elbow=None, hand_shape="glove"), **L.hang_cutter("front"))
    kg.set(loc=tuple(loc), face=facing(G.out), view="front", s=1, **pose); kg.a.walk_lock = None
    kg.breath = 0.020 * heave * math.sin(t * 5.6)
    return L.rig_post()


def late(F, g, t, u):
    G = F.c_geo
    if once(F):
        L.work_lamp(F, [F.c_kong.head()], aim=L.C_(G, 0.42, -0.66, 2.3), energy=1500.0, shadow_at=L.C_(G, 0.4, -0.6, 1.0), acts=())
    F.c_kong.a.set_glow((0.55, 0.62, 1.0), 0.22)

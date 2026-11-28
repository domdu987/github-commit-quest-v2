"""S053 (class A)  'ก้องถอยหลบมุมรถ'  -- M, 35 mm, locked, from behind the truck's tail.  Kong backs round the rear corner
from the lane side (right), the cutter still across his body toward where the junior is, two planted steps, and turns
into the nook between the tail door and the water barrier; back to the steel, a glove on his chest, the cutter hanging
from his right hand (held up to the chest its jaws covered his face)."""
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
T_TURN = 0.92


def setup(F):
    L.prep(F, alarm=True)
    L.nudge_cone(F)


def _back_take(F, start, end):
    """backing up along the line start -> end, facing the other way (two steps, planted)."""
    sp = F.c_kong.a.spec
    sc = F.c_kong.a.sc
    Ld = (Vector(end) - Vector(start)).length / sc
    root = L.gait9._keys([(0.0, 0.0, 0.0), (0.10, -0.08, 0.0), (0.45, -0.52 * Ld, 0.0), (0.82, -Ld, 0.0), (1.6, -Ld, 0.0)])
    feet = {"f": [(0.0, 0.18, 0.30, 0.0), (0.42, 0.62, -0.52 * Ld - 0.10, 0.0), (0.80, 1.6, -Ld + 0.30, 0.0)],
            "n": [(0.0, 0.44, -0.30, 0.0), (0.66, 1.6, -Ld - 0.30, 0.0)]}
    return L.gait9.Seq(sp, 1.6, lambda t: root(t), feet, None, lift=0.20, crouch=lambda t: 0.12)


def frame(F, g, t, u):
    G = F.c_geo
    L.always(F, all_extras=True)
    t0 = T0(F)
    tt = C.on_twos(t)
    tau = tt - t0
    kg = F.c_kong
    k0 = G.KB + G.tail * 0.99                                 # where S052 left him: south of the tail line, out in the lane
    look = L.C_(G, 0.42, -0.62, 1.62)
    F.camera(look + G.tail * 4.85 + G.out * 0.10 + Z(0.05), look, F.pick(35, 30), focus=look + Z(0.2), k=6.0, kmax=18, shake=hand_cam(t, 0.05, 0.8))
    dvec = Vector(k0) - Vector(G.HIDE); dvec.z = 0.0               # he faces back the way he came while he backs up
    if tau < T_TURN:
        h = L.hold(kg, "q", 1, grip=(0.36, 0.56), tilt=148.0)
        upd = dict(expr="alarmed", blink=0, lean=-8.0, head=(0, -2, 0.0, 0.0), gaze=(1.2, 0.0), **h)
        L.seq_put(F, kg, _back_take(F, k0, G.HIDE), tau, k0, dvec, view="q", upd=upd)
    else:
        k = smooth(ramp(tau, T_TURN, T_TURN + 0.18))
        flat = smooth(ramp(tau, T_TURN + 0.10, T_TURN + 0.30))
        loc = Vector(G.HIDE) + G.n * 0.06 * flat
        pose = dict(expr="alarmed", blink=C.blink("c_kong", t), legs="stand", lean=-3.0 * flat, head=(0, -6 * flat, 0.0, 0.0),
                    gaze=((C.hash01(int(tau * 6), 5) - 0.5) * 2.0, 0.0),
                    arm_l=dict(hand=(0.14, 0.50), elbow=None, hand_shape="glove"), **L.hang_cutter("front"))   # the tool down along his leg: its jaws stay off his face
        kg.set(loc=tuple(loc), face=facing(G.tail), view="front", s=1, **pose); kg.a.walk_lock = None
    kg.breath = 0.016 * math.sin(t * 6.5)
    return L.rig_post()


def late(F, g, t, u):
    if once(F):
        G = F.c_geo
        L.work_lamp(F, [F.c_kong.head()], aim=L.C_(G, -0.1, -0.6, 1.4), energy=2200.0, shadow_at=L.C_(G, 0.2, -0.6, 1.0), acts=(F.c_kong,))

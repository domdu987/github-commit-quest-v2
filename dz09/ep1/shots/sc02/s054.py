"""S054 (class A)  'มันมองไม่เห็นเขา'  -- M split, 35 mm, locked.  From the south-east the truck's rear corner is the vertical
edge near the middle of the frame.  Right of it, along the side panel: the junior crouched at the rear wheel, head jerking
left, right, left on twos, the red pin pupils scanning, short searching breaths.  Left of it, in the nook at the tail
door: Kong flat against the steel, a glove over his own mouth, the cutter held to his chest.  The corner is between their
lines of sight.  One red beacon sweep crosses both."""
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
CAST = ["c_kong", "c_jun"]


def setup(F):
    L.prep(F, alarm=True)
    L.nudge_cone(F)


def frame(F, g, t, u):
    G = F.c_geo
    L.always(F, all_extras=True)
    t0 = T0(F)
    tt = C.on_twos(t)
    tau = tt - t0
    kg, jn = F.c_kong, F.c_jun
    look = L.C_(G, 0.14, 0.32, 1.66)
    F.camera(L.C_(G, 2.55, -4.15, 1.40), look, F.pick(32, 28), focus=L.C_(G, 0.0, 0.0, 1.6), k=6.0, kmax=18, shake=hand_cam(t, 0.04, 0.7))
    # ---- Kong: back to the door, turned toward the corner he came round, the left glove over his mouth, the cutter in his right
    kp = dict(expr="scared", blink=C.blink("c_kong", t), legs="stand", lean=-4.0, head=(0, -4, 0.0, 0.0),
              gaze=(1.4 if (int(tau * 4) % 3) else 0.3, 0.0),
              arm_n=dict(fig_rel="mouth", hand_shape="press", elbow=-1), z={"arm_n": 2.7}, **L.hang_cutter("q", 1))
    kg.set(loc=tuple(G.HIDE + G.n * 0.06), face=facing(G.out), view="q", s=1, **kp); kg.a.walk_lock = None
    kg.breath = 0.012 * math.sin(t * 6.5)
    # ---- the junior: crouched at the wheel, the head jerks on twos (drawing and gaze), sniffing breaths
    k = int(tau * 12)                                         # 12 drawings a second
    beat = [(-1.5, 8, -0.03), (-1.5, 8, -0.03), (1.6, -6, 0.03), (1.6, -6, 0.03), (1.6, -6, 0.03), (-1.4, 4, -0.02), (-1.4, 4, -0.02),
            (0.2, 12, 0.0), (0.2, 12, 0.0), (1.5, -4, 0.03), (1.5, -4, 0.03), (-1.6, 6, -0.03)]
    gx, hd, dx = beat[k % len(beat)]
    sniff = 0.02 * (k % 2)
    jp = dict(expr="searching", blink=0, legs="crouch", hip=(0.0, 0.66), lean=16.0, gaze=(gx, 0.15), head=(0, hd, dx, sniff),
              **L.claws((0.42, 0.66), (0.30, 0.76)))
    # integration 11-28: 0.45 D further out from the side panel: at G.CROUCH his camera-facing card cut into the panel and the
    # panel hid his head (a headless body in the draft)
    jn.set(loc=tuple(G.CROUCH + G.out * 0.45), face=facing(G.tail - G.out * 0.3), view="q", s=-1, **jp); jn.a.walk_lock = None
    return L.rig_post()


def late(F, g, t, u):
    G = F.c_geo
    if once(F):
        L.work_lamp(F, [F.c_kong.head(), F.c_jun.head()], aim=L.C_(G, 0.1, 0.4, 1.3), energy=2400.0, shadow_at=L.C_(G, 0.1, 0.4, 1.0), acts=(F.c_kong, F.c_jun))
    # one red beacon sweep across both (the light bar's throw, as a moving red point above the corner)
    t0 = T0(F)
    sw = math.exp(-((t - t0 - 0.85) / 0.28) ** 2)
    F.fill("c_sweep", L.C_(G, 1.2 - 2.0 * smooth(ramp(t - t0, 0.4, 1.3)), 1.2, 3.4), 900.0 * sw, (1.0, 0.12, 0.08), 0.4)

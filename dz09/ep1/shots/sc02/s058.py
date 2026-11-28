"""S058 (class A)  (no words)  -- CU, 50 mm, the camera arcs 15 degrees with his head.  Kong steps out of the nook round the
rear corner (one planted step toward the lens), the cutter hanging from his right glove, and looks left (south, the
empty road), then right (north, where the junior went and the screams are): 'alarmed'.  The red beacon on his wet face,
then the blue one."""
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
PPD = {"c_kong": 480}
OUT = (0.42, -0.66)                                           # corner frame: one step out of the nook, past the corner


def setup(F):
    L.prep(F, alarm=True)
    L.nudge_cone(F)


def _step(F):
    sp = F.c_kong.a.spec
    sc = F.c_kong.a.sc
    Ld = (L.C_(F.c_geo, *OUT) - F.c_geo.HIDE).length / sc
    root = L.gait9._keys([(0.0, 0.0, 0.0), (0.08, 0.05, 0.0), (0.34, Ld, 0.0), (1.2, Ld, 0.0)])
    feet = {"n": [(0.0, 0.10, -0.25, 0.0), (0.30, 1.2, Ld + 0.25, 0.0)], "f": [(0.0, 0.20, 0.25, 0.0), (0.42, 1.2, Ld - 0.25, 0.0)]}
    return L.gait9.Seq(sp, 1.2, lambda t: root(t), feet, None, lift=0.22, crouch=lambda t: 0.06)


def frame(F, g, t, u):
    G = F.c_geo
    L.always(F, all_extras=True)
    t0 = T0(F)
    tt = C.on_twos(t)
    tau = tt - t0
    tc = t - t0
    kg = F.c_kong
    end = L.C_(G, *OUT)
    d = end - G.HIDE; d.z = 0.0; d.normalize()
    # head turn: left (south) -> centre -> right (north); the camera arcs with it on ones
    look_ph = smooth(ramp(tc, 0.40, 0.90))
    arc = math.radians(-7.5 + 15.0 * look_ph)
    ax = G.out * math.cos(arc) + G.n * math.sin(arc)
    # integration 11-28: the camera keeps its distance to Kong through his step out of the nook (it was set on the step's end,
    # so he grew 14 % in the first 6 frames, read as a zoom after the cut: the user's "cut like a film" rule)
    xs, _ = _step(F).root(min(max(tc, 0.0), 1.2))
    head = G.HIDE + d * (xs * kg.a.sc) + Z(2.52)
    # 11-28 fix pass (director: "Kong's face is cut by the frame edge"): 3.35 D (was 2.85): the head was 70 % of the frame
    # width and its hair touched the left edge at the start and the right edge after the turn; eyes about 0.42 down the frame
    F.camera(head + ax * 3.35 + Z(-0.10), head + Z(-0.30), F.pick(50, 40), focus=head, k=8.0, kmax=22, shake=hand_cam(t, 0.06, 1.6))   # integration 11-28: an arc, not handheld (was 0.25)
    if tau < 0.40:
        view, s, gz = "front", 1, (0.0, 0.0)
    elif tau < 0.58:
        view, s, gz = "q", -1, (-1.3, 0.0)
    elif tau < 0.70:
        view, s, gz = "front", 1, (0.2, 0.0)
    else:
        view, s, gz = "q", 1, (1.3, 0.0)
    upd = dict(expr="alarmed", blink=0 if tau < 0.6 else C.blink("c_kong", t), gaze=gz, head=(0, -3, 0.0, 0.0), lean=-2.0, **L.hang_cutter(view, s))
    if view in ("q", "side"):
        upd.update(arm_n="down") if s > 0 else upd.update(arm_f="down")
    else:
        upd.update(arm_l="down")
    loc, s_, p = L.seq_put(F, kg, _step(F), min(tau, 1.2), G.HIDE, d, view=view, upd=upd, lock=False, s=s)
    kg.set(face=facing(d) if view == "front" else facing(G.tail if s < 0 else G.n))
    kg.breath = 0.014 * math.sin(t * 6.0)
    return L.rig_post()


def late(F, g, t, u):
    G = F.c_geo
    if once(F):
        L.work_lamp(F, [F.c_kong.head()], aim=L.C_(G, 0.42, -0.66, 2.2), energy=1600.0, shadow_at=L.C_(G, 0.4, -0.6, 1.0), acts=())
    k = smooth(ramp(t - T0(F), 0.30, 0.80))                   # the red beacon, then the blue one, on the wet face
    F.c_kong.a.set_glow(lerp((1.0, 0.16, 0.12), (0.25, 0.45, 1.0), k), 0.34)

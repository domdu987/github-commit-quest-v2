"""S052 (class A)  'ผลักมันสุดแรง'  -- MW side, 24 mm, locked, impact shake 4 f.  Kong (left) straightens both arms behind the
cutter; the junior is thrown back (right) against the truck's side panel by the rear wheel, slams it, bounces and drops
to a crouch, shaking his head, then comes up searching.  Kong staggers two planted steps left, toward the rear corner."""
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

T_SHOVE, T_FLY, T_HIT, T_OFF = 0.21, 0.27, 0.45, 0.58


def setup(F):
    L.prep(F, alarm=True)
    L.nudge_cone(F)


def _kong_stagger(F):
    """after the shove: two steps back along his own facing (north), feet planted; root 0 -> -1.30 D."""
    sp = F.c_kong.a.spec
    root = L.gait9._keys([(0.0, 0.0, 0.0), (0.12, -0.10, 0.0), (0.42, -0.70, 0.0), (0.72, -1.30, 0.0), (1.6, -1.32, 0.0)])
    feet = {"f": [(0.0, 0.16, 0.30, 0.0), (0.38, 0.62, -0.85, 0.0), (0.62, 1.6, -0.85, 0.0)],
            "n": [(0.0, 0.34, -0.32, 0.0), (0.60, 1.6, -1.70, 0.0)]}
    return L.gait9.Seq(sp, 1.6, lambda t: root(t), feet, None, lift=0.20, crouch=lambda t: 0.10)


def frame(F, g, t, u):
    G = F.c_geo
    L.always(F, all_extras=True)
    t0 = T0(F)
    tt = C.on_twos(t)
    tau = tt - t0
    kg, jn = F.c_kong, F.c_jun
    k0 = G.KB + G.tail * 0.14                                 # where S051 left him
    look = L.C_(G, 1.0, 0.04, 1.35)
    hit = max(0.0, 1 - (t - t0 - T_HIT) / (4 / 24.0)) if t - t0 >= T_HIT else 0.0
    sh = tuple(a + b for a, b in zip(hand_cam(t, 0.05, 0.8), hand_cam(t, 1.6 * hit, 11.0, 4.0)))
    F.camera(look + G.out * 4.45 + G.n * 0.25 + Z(-0.05), look, F.pick(22, 20), focus=look, k=6.0, kmax=18, shake=sh)
    # ---- the block (also gives the junior's take-off point: a function of the camera position only, fixed here)
    kp, jl0, jp, T = L.block(F, t, k0, push=math.sin(2 * math.pi * 2.6 * tau) if tau < T_SHOVE else 0.0, tilt=166.0, grip=(0.40, 0.66), along=0.95,
                             kexpr="angry", klean=-10.0)
    if tau >= T_SHOVE:
        sh_ = smooth(ramp(tau, T_SHOVE, T_SHOVE + 0.17))       # arms straighten
        if tau < T_SHOVE + 0.38:
            h = L.hold(kg, "q", 1, grip=(lerp(0.40, 0.86, sh_), lerp(0.66, 0.42, sh_)), tilt=lerp(166.0, 150.0, sh_))
            kp = dict(expr="angry", blink=0, legs="lunge" if sh_ > 0.5 else "wide", lean=lerp(-10.0, 16.0, sh_), head=(0, 4, 0.04, 0.0), **h)   # integration 11-28: was `shouting` (reads as laughing)
            kg.set(loc=tuple(k0), face=facing(G.n), view="q", s=1, **kp); kg.a.walk_lock = None
        else:
            tk = tau - (T_SHOVE + 0.38)
            rec = smooth(ramp(tk, 0.0, 0.6))
            h = L.hold(kg, "q", 1, grip=(lerp(0.80, 0.34, rec), lerp(0.44, 0.62, rec)), tilt=lerp(150.0, 118.0, rec))
            upd = dict(expr="alarmed", blink=0, lean=lerp(10.0, -12.0, smooth(ramp(tk, 0.0, 0.3))) + 4.0 * smooth(ramp(tk, 0.5, 0.9)), head=(0, -4, 0.0, 0.0), **h)
            L.seq_put(F, kg, _kong_stagger(F), tk, k0, G.n, view="q", upd=upd)
        # ---- the junior: thrown, the panel, the drop
        H = L.C_(G, 0.30, 1.66)                                # his back on the panel, over the rear wheel
        if tau < T_FLY:
            jl, z, lean, legs, hip = jl0, 0.0, 22.0, "lunge", 0.10
            jp = dict(expr="snap_open", blink=0, head=(0, -14, 0.06, 0.0), **L.claws((0.80, -0.10), (0.70, 0.10)))
        elif tau < T_HIT:
            k = (tau - T_FLY) / (T_HIT - T_FLY)
            jl = jl0.lerp(H, smooth(k)); z = 0.30 * math.sin(math.pi * k)
            lean, legs, hip = lerp(5.0, -26.0, k), "step", 0.0
            jp = dict(expr="snap_open", blink=0, head=(0, 12, -0.06, 0.0), **L.claws((0.75, -0.55), (0.55, -0.35)))
        elif tau < T_OFF:
            jl, z, lean, legs, hip = H, 0.0, -8.0, "step", 0.05
            jp = dict(expr="moan", blink=1, head=(0, 16, -0.08, 0.02), **L.claws((0.50, 0.10), (0.30, 0.30)))
        else:
            k = smooth(ramp(tau, T_OFF, T_OFF + 0.30))
            jl = H.lerp(G.CROUCH, k); z = 0.0
            lean, legs, hip = lerp(-4.0, 18.0, k), "crouch", lerp(0.10, 0.60, k)
            up = smooth(ramp(tau, 1.15, 1.45))
            shake = (C.hash01(int(tau * 12), 7) - 0.5) * 14.0 * (1 - up)
            jp = dict(expr="moan" if up < 0.5 else "searching", blink=0, head=(0, 14 * (1 - up) + shake, 0.02, 0.0),
                      gaze=((C.hash01(int(tau * 6), 3) - 0.5) * 2.4, 0.2) if up > 0.5 else (0.0, 0.4), **L.claws((0.42, 0.62), (0.30, 0.72)))
        jp.update(legs=legs, lean=lean, hip=(0.0, hip))
        jn.set(loc=tuple(jl + Z(z)), face=facing(G.tail), view="side", s=-1, **jp); jn.a.walk_lock = None
    kg.breath = 0.010 * math.sin(t * 5.0)
    return L.rig_post()


def late(F, g, t, u):
    if once(F):
        L.work_lamp(F, [F.c_kong.head(), F.c_jun.head()], acts=(F.c_kong, F.c_jun))

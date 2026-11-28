"""S055 (class B)  'บนหลังคารถ / ไรเดอร์เสื้อเขียว'  -- W low, 24 mm, pans right with the rider.  Low on the road behind the
truck's rear corner, looking north-east across the jam: the turned junior crouched in the near foreground (left), hunting;
hollow bangs of boots on steel: a rider in a green jacket and white helmet climbs the green hatchback from the truck's
side, runs across its roof, jumps the gap onto the SUV and runs across that roof, left to right; the junior's head snaps
up and round after the noise.  The rider ends crouched at the SUV's far edge, looking back, about to jump again."""
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
DEPS = [L.LIBF, L.sc02_faces.FILE]
CLASS = "B"
CAST = ["c_jun", "c_james"]
JAMES_A, JAMES_B = (0.60, 6.60), (9.20, 2.60)                # corner frame: the deck west of l3_a -> over l3_a -> over l2_b to its east edge
JUN = (1.90, 0.60)
CAM = (0.60, -2.60, 2.80)                                  # 11-28 fix pass: z 2.80 (eye level).  At 0.95 the rider ran THROUGH the junior's head; at 1.75 (integration) he still ran ON it (k30: his foot on the junior's crown, the roof he ran on hidden behind the head, final-tier gate still).  From 2.80 the roofs are seen from above, mid-frame, and the junior's head sits well below them


def setup(F):
    L.prep(F, alarm=True)
    L.nudge_cone(F)
    F.nudge("cone_3", tuple(F.c_geo.tail * 1.6))           # integration 11-28: out of this low camera's pan (it filled the bottom centre at the end)


def frame(F, g, t, u):
    G = F.c_geo
    L.always(F, all_extras=True)
    t0 = T0(F)
    tt = C.on_twos(t)
    tau = tt - t0
    jm, jn = F.c_james, F.c_jun
    a, b = L.C_(G, *JAMES_A), L.C_(G, *JAMES_B)
    tk = L.take_cached(F, "james", lambda: L.roof_take(F, jm, a, b, stride=2.10, speed=8.8))
    d = (b - a); d.z = 0.0; d.normalize()
    run_end = tk.dur - 0.45
    L.seq_put(F, jm, tk, min(t - t0 + 0.05, tk.dur), a, d, view="side", upd=dict(expr="terrified", blink=0, visor="down", gaze=(-1.4, 0.0) if tau > run_end else (0.0, 0.0)))
    if tau > run_end:                                          # at the far edge: crouched to jump, looking back over his shoulder
        k = smooth(ramp(tau, run_end, run_end + 0.25))
        p2 = dict(jm.pose_d); p2["lean"] = lerp(p2.get("lean", 14.0), 24.0, k); p2["hip"] = (0.0, 0.30 * k)
        p2["arm_n"] = dict(hand=(0.55, 0.55), elbow=None, hand_shape="open"); p2["arm_f"] = dict(hand=(-0.35, 0.65), elbow=None, hand_shape="open")
        jm.set(**p2)
    # ---- camera: low, starts on the junior and the rider's first steps, then pans right with the rider (on ones)
    tc = t - t0
    xr, zr = tk.root(min(tc + 0.05, tk.dur))
    jpos = a + d * (xr * jm.a.sc)
    head_j = L.C_(G, JUN[0], JUN[1], 1.45)
    tgt = jpos + Z(zr * jm.a.sc + 1.7) + d * 0.5
    look = head_j.lerp(tgt, 0.45 + 0.55 * smooth(ramp(tc, 0.0, 0.9)))
    F.camera(L.C_(G, *CAM), look, F.pick(24, 22), focus=tgt, k=5.0, kmax=16, shake=hand_cam(t, 0.06, 1.2))   # integration 11-28: a pan, not handheld (was 0.12)
    # ---- the junior: hunting with his back to us; at the first bang his head snaps up and round to the roofs
    jl = L.C_(G, *JUN)
    if tau < 0.42:
        jp = dict(expr="searching", blink=0, legs="crouch", hip=(0.0, 0.64), lean=18.0, head=(0, 10, 0.0, 0.02 * (int(tau * 12) % 2)),
                  **L.claws((0.40, 0.62), (0.30, 0.72)))
        jn.set(loc=tuple(jl), face=facing(G.out), view="side", s=1, **jp)
    else:
        up = smooth(ramp(tau, 0.42, 0.55))
        gx = 0.6 + 0.8 * smooth(ramp(tau, 0.8, 1.9))           # the eyes follow him
        jp = dict(expr="snap_open" if tau < 0.75 else "z_snarl", blink=0,   # 11-28: was lunging (a grin)
                   legs="crouch", hip=(0.0, lerp(0.64, 0.56, up)), lean=lerp(14.0, 6.0, up),
                  head=(0, -18 * up, 0.0, 0.0), gaze=(gx, -1.3), **L.claws((0.42, 0.55), (0.32, 0.66)))
        jn.set(loc=tuple(jl), face=facing(G.n + G.out), view="q", s=1, **jp)
    jn.a.walk_lock = None
    F.fill("c_jfill", jpos + Z(3.6) - G.n * 2.4, 115.0, (0.78, 0.86, 1.0), 0.8)   # integration 11-28: was 190 (James glowed cyan)
    F.fill("c_ufill", jl + Z(2.2) - G.n * 1.0 + G.out * 0.6, 110.0, (1.0, 0.55, 0.45), 0.4)
    return L.rig_post()


def late(F, g, t, u):
    if once(F):
        L.no_lamp(F)
        F.shadows(L.C_(F.c_geo, 4.0, 3.0, 1.0))

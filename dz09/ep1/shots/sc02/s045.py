"""S045 (class A)  Kong: 'เฮ้ย! ได้ยินพี่ไหม!'  -- CU two-shot, 50 mm, handheld.  Kong takes the junior's shoulder and shakes him,
shouting; the slack body rocks with every pull, the head lagging behind it, and falls back against the tyre when the
shaking stops.  No reaction on the grey face."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sc02b_lib import *
LOC = "X1"
CAST = CAST_B
DEPS = [LIB]

CLASS = "A"
PPD = {"b_jun": 420, "b_kong": 420}


def setup(F):
    prep(F, alarm=True)


def _shake(F, t):
    """(body offset toward Kong in D, head lag) of the shaken junior: 3.2 pulls a second from 'เฮ้ย!' on, dying at the end."""
    T1 = W("เฮ้ย!")
    a, b = E.scene().range(F.shot.ID)
    t_end = b / 24.0
    env = smooth(ramp(t, T1 - 0.08, T1 + 0.10)) * (1 - smooth(ramp(t, t_end - 0.42, t_end - 0.17)))
    ph = 2 * math.pi * 3.2 * (t - T1)
    return env * math.sin(ph), env * math.sin(ph - 1.1), env


def frame(F, g, t, u):
    G = F.b_geo
    always(F)
    tt = C.on_twos(t)
    s0, s1, env = _shake(F, tt)
    a = anchors(F.b_jun._spec, jun_pose(F.b_jun._spec, "side", s=-1, slump=0.35, limp=True), "side", -1)
    sc = F.b_jun.a.sc
    jh = G.J + G.n * (a["head"][0] * sc) + Z(-a["head"][1] * sc)
    mid = jh + G.tail * 0.42 + Z(0.22)
    c0, c1, _ = _shake(F, t - 0.06)
    sh = tuple(x + y for x, y in zip(hand_cam(t, 0.45, 2.6), (0.5 * c0, 0.25 * c1, 0.0)))
    F.camera(mid + G.out * 5.0 + Z(0.05), mid, F.pick(50, 40), focus=jh, k=7.0, kmax=20, shake=sh)
    jl = G.J + G.tail * (0.035 * s0)                         # the trunk is pulled toward Kong and let go (the pelvis slides a few cm on the wet deck)
    fall = smooth(ramp(t, E.scene().range(F.shot.ID)[1] / 24.0 - 0.34, E.scene().range(F.shot.ID)[1] / 24.0 - 0.08))
    jp = jun_pose(F.b_jun._spec, "side", s=-1, slump=0.35, limp=True, expr="out", blink=2)
    jp["lean"] = jp["lean"] + 5 * s0 * 1.0
    jp["head"] = (0, 9 - 11 * s1 - 12 * fall, 0.02 + 0.03 * fall, 0.0)
    jun(F, jl, "side", -1, jp)
    a2 = anchors(F.b_jun._spec, jp, "side", -1)
    sho = fig_world(F, F.b_jun, jl, (a2["shoulder_R"][0] - 0.02, a2["shoulder_R"][1] + 0.02))
    chest = fig_world(F, F.b_jun, jl, (a2["shoulder_R"][0] - 0.20, a2["shoulder_R"][1] + 0.36))
    loud = env > 0.3
    # integration 11-28: `shouting` (squint + open-D mouth) read as LAUGHING in the draft; as S032: `worried` brows with a
    # ROUND mouth one size up while he speaks, `alarmed` between the words
    m = talk("kong", g).get("mouth", 0.0)
    mo = {"mouth": ("o", min(1.0, 0.25 + 1.0 * m))} if m else {}
    kp = kong_pose(lean=22 - 3 * s0, expr="worried" if loud else "alarmed", blink=0, head=(0, 4 - 3 * s0, 0, 0),
                   arm_n=dict(fig=reach(F, G.K, sho), hand_shape="grip"), arm_f=dict(fig=reach(F, G.K, chest), hand_shape="grip"), **mo)
    kong(F, G.K, "q", 1, kp)
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        wheel_lamp(F, [F.b_kong.head(), F.b_jun.head()])

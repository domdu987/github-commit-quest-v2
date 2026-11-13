#!/usr/bin/env python3
"""shot.py -- film 5 take s13: shot 13 (40.14-45.49 s, g 1204..1364, handles g 1196..1203 / 1365..1372), mine tunnel LAMP.

alfie grabs the cage and drags the miners toward the far exit (outbye, the bright pit bottom); miner3 mocks on the quoted line
"ไอ้เด็กเลี้ยงนก ตื่นตูมอีกแล้ว" (mouth moving g 1304..1367 only); the gaffer stays under his hanging lamp, arms crossed.
    13a g 1204..1245  medium at the nail (cage on the left leg of set 6): alfie hops, his fist closes on the cage ring (g 1208,
                      "เขาคว้ากรง") and the cage comes off the nail - from that frame it is the cast's 2D held cage (bars drawn over
                      the fallen bird, eyes closed), the set's 3D cage is hidden; he lands, turns and starts to run
    13b g 1246..1287  low, outbye looking inbye: alfie runs at the camera, cage out in front, dragging miner1 by the hand;
                      miner2 / miner3 follow at a walk; the gaffer in the right foreground under his lamp, arms crossed
    13c g 1288..1329  medium tracking back with miner3: hands cupped at his mouth, mocking (mouth from g 1304); miner2 behind
    13d g 1330..1364  high wide from outbye: alfie + miner1 run past toward the camera / exit, miner3 still mocking, the gaffer
                      stays smug under his lamp.  Handle to g 1372.
Internal sub ids 1..4 (= 13a..13d).  No depth of field anywhere.  The bird is never drawn outside the bars.
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s12"))
from base import *                                       # noqa: F401,F403
import base as B

G0, G1, H = 1204, 1365, 8
G_B, G_C, G_D = 1246, 1288, 1330
G_GRAB = 1208                                             # fist on the ring ("เขาคว้ากรง" 40.11 s -> g 1206)
G_Q = (g_of(43.38), g_of(45.46))                          # 1304..1367: the mocking quote
CAGE_Y, CAGE_S = 16.25, -1.86
GAFFER = TP(9.6, 0.85, 0)
SWING = lambda g: 14 * math.sin(g * 0.45)                 # the held cage swings at a run


DROP = 0.55                                               # the nail sits 0.55 D lower in this take, so the boy can reach the ring


def setup(T):
    """runtime set change (the set file is untouched): nail + cage 0.55 D lower on the leg of set 6"""
    for o in bpy.data.objects:
        if o.name.startswith("cage_nail"):
            o.location.z -= DROP
    T.cage_at = Vector(T.hook) - Vector((0, 0, DROP))
    T.hook = Vector(T.cage_at); T.floor = T.floor - Vector((0, 0, DROP)); T.perch = T.perch - Vector((0, 0, DROP))


B.SETUP = setup


def cam_a(g):
    return cam_keys(g, [(G0 - H, TP(12.0, -0.25, 1.85), TP(16.0, -1.45, 2.05), "sine"), (G_B, TP(12.4, -0.35, 1.80), TP(15.8, -1.35, 2.0), "hold")])


def cam_b(g):
    return cam_keys(g, [(G_B, TP(8.6, -0.20, 1.20), TP(14.0, -0.85, 2.15), "lin"), (G_C, TP(8.2, -0.20, 1.15), TP(13.6, -0.85, 2.10), "hold")])


def m3_y(g):
    return 11.6 - 0.04 * (g - G_C)


def cam_c(g):
    y = m3_y(g)
    return TP(y - 2.75, -0.15, 2.55), TP(y, -0.60, 2.55)


def cam_d(g):
    return cam_keys(g, [(G_D, TP(1.9, 0.15, 3.15), TP(9.5, -0.45, 1.55), "sine"), (G1 + H, TP(1.6, 0.15, 3.10), TP(9.2, -0.45, 1.50), "hold")])


# ----------------------------------------------------------------------------- poses
def cage_bird(g):
    return dict(state="fallen", eyes=0.0, swing=SWING(g), t=g / 30.0, breath=0.15)


def alfie_a(T, g):
    """13a: alfie (right of the cage) looks at the fallen bird, reaches and snatches the cage off the nail (g 1205..1208: from
    G_GRAB it is the cast's 2D held cage, swinging hard from the yank, bird inside), turns and starts to run toward the camera"""
    base = TP(16.05, -1.22, 0)
    u_turn = ez((g - 1219) / 8.0)
    u_run = clamp((g - 1226) / float(G_B - 1226))
    pos = lerpv(base, TP(15.0, -0.95, 0), ez(u_run, "quad_in"))
    p = dict(yaw=lerp(-0.6, 0.3, u_turn), pitch=-0.3 if g < 1214 else -0.05, expr="worried" if g < G_GRAB else "determined",
             mouth="frown", head_roll=-4, lean=lerp(0, 10, u_run), arm_l=dict(hand=(0.45, 0.85), bend=0.6), t=g / 30.0)
    p["legs"] = "stand" if g < 1212 else ("wide" if g < 1226 else run_legs(g, 10, 1.1))
    p["blink"] = blink(g, [1199, 1236])
    if g < 1214:
        p["gaze"] = (-0.8, -0.6)
    if g < G_GRAB:
        u = ez((g - 1203) / 4.0, "cubic_out") if g >= 1203 else 0.0
        p["arm_r"] = dict(hand=(lerp(-0.35, -1.0, u), lerp(0.75, -0.6, u)), bend=-0.4, stretch=1.5, shape="open" if u > 0.5 else "fist")
        return pos, p, None
    p["prop_r"] = "cage"
    b = cage_bird(g); b["swing"] = 34 * math.exp(-(g - G_GRAB) / 9.0) * math.cos((g - G_GRAB) * 0.55) + (SWING(g) if g >= 1226 else 0)
    p["bird"] = b
    if g >= 1226:
        p["fx"] = ["sweat"]
    u = ez((g - G_GRAB) / 8.0)
    p["arm_r"] = dict(hand=(lerp(-0.75, -0.55, u), lerp(-0.35, 0.25, u)), bend=-0.8, stretch=1.3)
    return pos, p, None


def miner_watch(n, g):
    off = {"miner1": 0, "miner2": 5, "miner3": 11}[n]
    p = dict(yaw={"miner1": -0.35, "miner2": -0.2, "miner3": -0.45}[n], pitch=-0.1, expr="smug", mouth="smirk", arm_l="akimbo", arm_r="akimbo",
             legs="stand", head_roll=3 * math.sin(g * 0.11 + off), t=g / 30.0)
    p["blink"] = blink(g, [1210 + off, 1240 + off])
    return p


def stage_a(T, g):
    pos, p, hands = alfie_a(T, g)
    out = {"alfie": dict(pos=pos, pose=p, hands=hands),
           "miner1": dict(pos=TP(20.2, 0.05, 0), pose=miner_watch("miner1", g)),
           "miner3": dict(pos=TP(21.6, -1.35, 0), pose=miner_watch("miner3", g))}
    if g < G_GRAB:
        out["bird"] = dict(pos=Vector(T.floor) + Vector((0, 0, 0.012)), pose=dict(state="fallen", eyes=0.0, t=g / 30.0, breath=0.15))
    else:
        out["bird"] = dict(pos=Vector(T.floor), pose=dict(state="fallen"))          # hidden from G_GRAB (it is in the 2D cage now)
    return out


def drag_pair(T, g, ya, f_cam, sa=-0.55, sm=-1.45):
    """alfie running at the camera at station ya, his free hand pulling miner1's hand; returns the two entries"""
    a_pos = TP(ya, sa, 0)
    m_pos = TP(ya + 1.05, sm, 0)
    grip = TP(ya + 0.45, (sa + sm) / 2, 1.28)
    pa = dict(yaw=0.25, pitch=-0.05, expr="determined", mouth="frown", fx=["sweat"], lean=10, head_roll=-5, legs=run_legs(g, 10, 1.15),
              prop_r="cage", bird=cage_bird(g), arm_r=dict(hand=(0.55, 0.25), bend=-0.8, stretch=1.3), t=g / 30.0)
    pa["blink"] = blink(g, [1262, 1341])
    pm = dict(yaw=-0.2, pitch=-0.05, expr="smug", mouth="smirk", lean=-6, head_roll=5, legs=walk_legs(g, 12, 0.9, 0.3), arm_l="down", t=g / 30.0)
    pm["blink"] = blink(g, [1270, 1350])
    return {"alfie": dict(pos=a_pos, pose=pa, hands={"l": {"hand": tuple(grip), "stretch": 1.35}}),
            "miner1": dict(pos=m_pos, pose=pm, hands={"r": {"hand": tuple(grip), "stretch": 1.3}})}


def gaffer_pose(g):
    p = dict(cast5.STORY5["gaffer_arms_crossed"][1])
    p.update(yaw=-0.25, expr="smug", mouth="smirk", t=g / 30.0, head_roll=4 + 2 * math.sin(g * 0.08))
    p.pop("prop_l", None); p.pop("prop_r", None)
    p["blink"] = blink(g, [1258, 1300, 1345])
    return p


def mock_pose(g, back=False):
    p = dict(cast5.STORY5["miners_mock_miner3"][1])
    p.update(t=g / 30.0, legs=walk_legs(g, 14, 0.8), mouth=talk(g, *G_Q, seed=1) or "smirk", head_roll=6 + 3 * math.sin(g * 0.3),
             yaw=-0.45 if not back else 0.45)
    p["blink"] = blink(g, [1296, 1338])
    return p


def stage_b(T, g):
    u = (g - G_B) / float(G_C - G_B)
    ya = 13.6 - 2.4 * u
    out = drag_pair(T, g, ya, None)
    m2 = dict(cast5.STORY5["miners_work_miner2"][1]); m2 = dict(yaw=0.2, pitch=-0.1, expr="smug", mouth="smirk", legs=walk_legs(g, 15, 0.7, 0.5),
                                                               arm_l="down", arm_r="down", t=g / 30.0, blink=blink(g, [1266]))
    m3 = dict(yaw=-0.3, pitch=-0.1, expr="smug", mouth="smirk", legs=walk_legs(g, 14, 0.7), arm_l="akimbo", arm_r="akimbo", t=g / 30.0,
              blink=blink(g, [1275]))
    out["miner2"] = dict(pos=TP(ya + 2.6, -1.55, 0), pose=m2)
    out["miner3"] = dict(pos=TP(ya + 3.1, -0.35, 0), pose=m3)
    return out


def stage_c(T, g):
    y = m3_y(g)
    m2 = dict(yaw=0.3, pitch=-0.1, expr="smug", mouth="smirk", legs=walk_legs(g, 15, 0.7, 0.5), arm_l="down", arm_r="akimbo", t=g / 30.0,
              blink=blink(g, [1310]))
    return {"miner3": dict(pos=TP(y, -0.60, 0), pose=mock_pose(g)),
            "miner2": dict(pos=TP(y + 1.5, -1.55, 0), pose=m2)}


def stage_d(T, g):
    u = (g - G_D) / float(G1 + H - G_D)
    ya = 8.2 - 3.0 * u
    out = drag_pair(T, g, ya, None, sa=-1.45, sm=-0.70)
    out["miner3"] = dict(pos=TP(10.3 - 1.1 * u, -0.05, 0), pose=mock_pose(g))
    out["miner2"] = dict(pos=TP(11.6 - 1.0 * u, -1.6, 0), pose=dict(yaw=-0.2, pitch=-0.1, expr="smug", mouth="smirk", legs=walk_legs(g, 15, 0.7, 0.5),
                                                                    arm_l="down", arm_r="akimbo", t=g / 30.0, blink=blink(g, [1350])))
    out["gaffer"] = dict(pos=GAFFER, pose=gaffer_pose(g))
    return out


def lamps(T, g, f):
    if "alfie" not in T.subs[T.cur].actors or ("alfie", f) not in T.anch:
        return {}
    a = T.actors["alfie"]
    hx, hy = T.anch[("alfie", f)]["hip"]
    p = actors.local_to_world(a, (hx + 0.30, hy + 0.12), f)
    loc = T.subs[T.cur].cam(g)[0]
    tc = loc - p; tc.z = 0; tc.normalize()
    return {"lamp_alfie": (p + tc * 0.12, 0.75)}


def ctl_a(T, f, g):
    pass


GAS = 1.6
SUBS = {1: Sub("13a", (G0 - H, G_B - 1), cam_a, stage_a, lamps=lamps, actors=["alfie", "bird", "miner1", "miner3"], gas=GAS,
               ppd={"alfie": 384, "bird": 1024, "miner1": 160, "miner3": 160},
               extra={"cage3d": lambda g: g < G_GRAB, "hide": lambda g: set() if g < G_GRAB else {"bird"}}),
        2: Sub("13b", (G_B, G_C - 1), cam_b, stage_b, lamps=lamps, actors=["alfie", "miner1", "miner2", "miner3"], gas=GAS,
               ppd={"alfie": 384, "miner1": 320, "miner2": 224, "miner3": 224},
               extra={"cage3d": lambda g: False}),
        3: Sub("13c", (G_C, G_D - 1), cam_c, stage_c, lamps=None, actors=["miner3", "miner2"], gas=GAS,
               ppd={"miner3": 448, "miner2": 256}, extra={"cage3d": lambda g: False}),
        4: Sub("13d", (G_D, G1 + H - 1), cam_d, stage_d, lamps=lamps, actors=["alfie", "miner1", "miner2", "miner3", "gaffer"], gas=GAS,
               ppd={"alfie": 256, "miner1": 256, "miner2": 192, "miner3": 256, "gaffer": 256}, extra={"cage3d": lambda g: False})}
for _s in SUBS.values():
    _s.lamp_names = ("lamp_alfie",)

if __name__ == "__main__":
    B.main("s13", SUBS, HERE, sys.argv)

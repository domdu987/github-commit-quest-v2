#!/usr/bin/env python3
"""Example take ex_kitchen: kitchen set (set3d_kitchen), kitchen_grey light, runner v3/set3d_kitchen/kshot.py.

The kitchen is an INSERT set: a table corner by a window, built only for what its three cameras see. Its runner has no puppet
actors; its one performer is an ink ARM card (beach_man's limb and hand, drawn per frame by kshot.arm_svg) that reaches in from
off frame. Two standing puppets would need floor space in view that the set does not have (see README, "kitchen").

36 film frames (g 30..65) plus 3 + 3 handles (rendered g 27..68).
  camera  steep (tight on the weather box, ~44 deg down) eases back and up into table (THE TABLE FRAMING) over g 32..54
  actor   the arm reaches in from screen right g 46..58 and grips the cup handle; the cup rattles on its saucer when touched
  gimmick steam loop over the cup, rings on the coffee, drizzle on the window, the newspaper corner flutters
    python3 shot.py still <g> [scale% samples] | draft [a:b:step] | render [a:b] | post | contact (v3/set3d_kitchen/kshot.py)
    python3 shot.py qa      meta.json, cues.json, contact.jpg, work/qa.json (v3/set3d_kitchen/kqa.py)
"""
import math
import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(DIR))
import common as C                                                     # noqa: E402
sys.path.insert(0, os.path.join(C.PROJ, "v3", "set3d_kitchen"))
import kshot as KS                                                     # noqa: E402
import kitchen_geom as KG                                              # noqa: E402

smooth, smoother, lerp = KS.smooth, KS.smoother, KS.lerp

TAKE, SHOTS, LIGHT, VERSION = "ex_kitchen", [4], "kitchen_grey", 1     # kitchen_grey | kitchen_storm
G0, G1, H_IN, H_OUT = 30, 66, 3, 3
R0, R1 = G0 - H_IN, G1 + H_OUT
TRANSITION_IN = dict(type="dissolve", frames=5, note="example")

STEEP = KG.CAM_STEEP                                                   # A['cams']['steep']
TABLE = KG.CAM_TABLE                                                   # A['cams']['table']
MOVE = (32, 54)
REACH = (46, 58)                                                       # the hand travels in, grips at 58

_r = math.radians(KG.CUP_ROT)                                          # the cup handle in world space (cup rig turned CUP_ROT)
HANDLE_W = (KG.CUP_REST[0] + KG.HANDLE[0] * math.cos(_r) - KG.HANDLE[1] * math.sin(_r),
            KG.CUP_REST[1] + KG.HANDLE[0] * math.sin(_r) + KG.HANDLE[1] * math.cos(_r),
            KG.TOP + 0.003 + KG.HANDLE[2])
SHOULDER = (1.55, -2.05, 2.05)                                         # off frame right, in front of the window wall
HAND_FROM = (1.05, -1.75, 1.75)


def cam(g):
    u = smoother((g - MOVE[0]) / float(MOVE[1] - MOVE[0]))
    loc, look = C.blend_cam(STEEP, TABLE, u)
    k = 0.01 * C.creep((g - R0) / float(R1 - R0))                       # 1 % creep so it never parks
    return lerp(loc, look, k), look


def arm(g):
    if g < REACH[0]:
        return None
    u = smoother((g - REACH[0]) / float(REACH[1] - REACH[0]))
    return dict(hand=lerp(HAND_FROM, HANDLE_W, u), shoulder=SHOULDER)


def cup_in_hand(g):
    return False                                                       # gripped, not lifted (a lift would need the cup in the plate/matte split)


def state(g):
    k = g - R0
    rat = 1.0 if REACH[1] <= g < REACH[1] + 6 else 0.0                 # the cup rattles for 6 frames when the hand grips it
    hop = rat * 0.006 * abs(math.sin(g * 2.1))
    return dict(cup=(0.0, 0.0, hop, KG.CUP_ROT + rat * 3.0 * math.sin(g * 1.7)), saucer=None,
                ripple=(-0.9 * k, 0.25 + 0.6 * rat), steam=k, window=("drizzle", k), flutter=(g / 30.0, 0.006),
                bleed=None, lightning=0.0, crack=None, chair=0.0, drop=None)


CUES = [
    (G0 / 30.0 - 0.1, 1.2, "bed", "drizzle on the window, kettle tick (bed)"),
    (REACH[1] / 30.0 - 0.1, 0.2, "rattle", "cup rattles on its saucer"),
]

if __name__ == "__main__":
    if sys.argv[1:2] == ["qa"]:                                        # kshot has no qa command: kqa.py does it for a take folder
        import kqa
        kqa.main(DIR)
    else:
        KS.run(sys.modules[__name__], sys.argv[1:])

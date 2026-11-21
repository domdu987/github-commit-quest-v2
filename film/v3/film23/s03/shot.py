#!/usr/bin/env python3
"""shot.py -- film 23 take s03: shot S03 (LANE morning): medium, quick push-in on the pin.  A soldier (the dry smiler) pricks the hero tank with a pin
from the patch kit: set_deflate keyed 0.25 -> 0.85 of the move, the barrel droops onto his helmet, a big sweat drop.  Cut in, dissolve out 11 (handle 8)."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import c23 as C
import c23_poses as P
import cast23

G0, G1 = 252, 357
N = math.ceil((G1 - G0) * 1.25)
G_PRICK = G0 + int(0.22 * N)        # the pin goes in (deflation starts a little after)

def state(GH, g, t, f, tk):
    GH.set_deflate(C.smooth(0.25, 0.85, t), frame=f)

def pricker(g):
    c, p = P.base("gi_pin_prick"); p = P.life(p, g, 3)
    if g < G_PRICK - 10:        # concentrating, pin jabbing at the tank
        p["arm_r"] = dict(p["arm_r"]); p["arm_r"]["hand"] = (0.8 + 0.05 * math.sin(g / 5.0), 0.42)
        p["expr"] = "determined"
    elif g < G_PRICK + 14:      # jab (arm extends), then freezes
        p["arm_r"] = dict(p["arm_r"]); p["arm_r"]["hand"] = (0.98, 0.35); p["expr"] = "neutral"
    else:                       # shock + the big sweat drop; pin pulled back
        p["expr"] = "shock"; p["bigsweat23"] = 1; p["fx"] = ["sweat"]
        p["arm_r"] = dict(p["arm_r"]); p["arm_r"]["hand"] = (0.62, 0.55)
        p["pitch"] = -0.35
    return p

def pumper(g):
    return cast23.pump_frame("gi_pump", g / 20.0, -1)

def clip(g):
    c, p = P.base("gi_designer_clipboard"); return P.life(p, g, 5)

def tweak(GH, tk):
    import ghost_shots as SH
    SH.SHOTS["S03"]["move"]["slide"] = -14           # runtime camera tweak: keeps the pricker inside the frame to the end of the tail (was -30)
    C.GH.shot_camera("S03", 0.0)

CFG = dict(shot="S03", tweak=tweak, g0=G0, g1=G1, h_in=0, h_out=8, trans_in=dict(type="cut", frames=0), state=state,
  actors=[
    dict(name="pricker", cast="gi_smile", at=("pricker", 0), pose=pricker, ppd=160, flip=True),
    dict(name="pumper", cast="gi_pump", at=("pumpman", 0), pose=pumper, ppd=96, wide=True),
    dict(name="clip", cast="gi_designer", at=("clipboard", 0), off=(1.2, 4.2, 0), pose=clip, ppd=128, flip=True),
  ])
CUES = [{'time': 9.0, 'duration': 2.0, 'frame': 270, 'end_frame': 330, 'kind': 'prop', 'label': 'a pin pricks rubber then a long comic fsssss hiss'}, {'time': 10.833, 'duration': 0.333, 'frame': 325, 'end_frame': 335, 'kind': 'prop', 'label': 'the limp barrel flops onto a helmet, hollow bonk'}, {'time': 11.167, 'duration': 0.333, 'frame': 335, 'end_frame': 345, 'kind': 'prop', 'label': 'tiny comic sweat-drop plink'}]
if __name__ == "__main__":
    C.main(CFG, HERE)

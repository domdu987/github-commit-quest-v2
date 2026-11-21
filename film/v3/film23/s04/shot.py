#!/usr/bin/env python3
"""shot.py -- film 23 take s04: shot S04 (LANE morning): high crane down over the work area: the painter paints the white star, the sound man carries a
record, the designer holds a clipboard, the pump man pumps.  QA_ART_SET note: the foreground soldier's head must stay out of y 880-950 in the last frame
(mark moved up-frame).  Dissolve in 11 (handle 8), cut out."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import c23 as C
import c23_poses as P
import cast23

def painter(g): return cast23.paint_frame("gi_painter", g / 18.0, 1)
def pumper(g): return cast23.pump_frame("gi_pump", g / 20.0, -1)
def designer(g):
    c, p = P.base("gi_designer_clipboard"); p = P.life(p, g, 5)
    if (g // 45) % 2: p["arm_r"] = dict(p["arm_r"]); p["arm_r"]["hand"] = (0.3 + 0.12 * math.sin(g / 3.0), 0.62)   # pencil scribbling
    return p
def sound(g):
    c, p = P.base("gi_sound_carry_record"); p = P.life(p, g, 7, sway=1.4)
    p["spin23"] = g * 4.0
    return p

O = (-700.0, -260.0, 0.0)
def W(x, y): return (x + O[0], y + O[1], 0.0)

def prebuild(SH):
    """Director redo: the crane still comes down from high, but ENDS medium-wide on the four crew (painter at the star tank, sound man with the record,
    designer pointing with the clipboard, pump man at a half-inflated tank), heads ~130-180 px."""
    sh = SH.SHOTS["S04"]
    sh["move"] = dict(end=SH.C((0.8, 3.0, 5.2), (0.8, 12.0, 2.3), 22))

def state(GH, g, t, f, tk):
    GH.set_inflate("tank_hero", 0.45 + 0.1 * math.sin(g / 20.0 * 2 * math.pi) * 0.5 + 0.0, frame=f)   # half-inflated, breathing with the pump

def designer_pt(g):
    c, p = P.base("gi_designer_point"); p = P.life(p, g, 5)
    k = math.sin(g / 30.0 * 2 * math.pi * 0.8)
    p["arm_r"] = dict(p["arm_r"]) if isinstance(p.get("arm_r"), dict) else p.get("arm_r")
    return p

CFG = dict(shot="S04", prebuild=prebuild, g0=357, g1=486, h_in=8, h_out=0, trans_in=dict(type="dissolve", frames=11), state=state,
  actors=[
    dict(name="painter", cast="gi_painter", at=lambda g: W(0.9, 12.8), pose=painter, ppd=192, flip=False),
    dict(name="pumper", cast="gi_pump", at=lambda g: W(-2.4, 12.6), pose=pumper, ppd=192, wide=True),
    dict(name="designer", cast="gi_designer", at=lambda g: W(-0.8, 10.0), pose=designer_pt, ppd=192, flip=True),
    dict(name="sound", cast="gi_sound", at=lambda g: W(2.4, 10.3), pose=sound, ppd=192),
  ])
CUES = [{'time': 11.633, 'duration': 5.7, 'frame': 349, 'end_frame': 520, 'kind': 'ambience', 'label': 'busy work area: a hand pump wheezing, brush strokes, a record scratch'}, {'time': 11.633, 'duration': 5.7, 'frame': 349, 'end_frame': 520, 'kind': 'prop', 'label': 'pump stroke every 0.67 s'}]
if __name__ == "__main__":
    C.main(CFG, HERE)

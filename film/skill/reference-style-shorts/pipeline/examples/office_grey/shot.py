#!/usr/bin/env python3
"""Example take ex_office_grey: office set, office_grey light (set3d_ext/light), runner v3/film/s17/otake.py.
Set EX_LIGHT=office_storm in the environment for the storm preset with one lightning pulse (same file, same commands).

36 film frames (g 30..65) plus 3 + 3 handles (rendered g 27..68).
  camera  eye_two_shot (set camera) cranes up and over into high_two_shot over g 36..60 (eased, never parked)
  actors  the hero at hero_mark, slumped (acting.hero_slumped: sad, turning the pencil stub, one blink);
          the chief walks in from the window side to near_mark (acting.boss_walk: 0.68 s step, bob, sway, `_adv` / `_lift`)
  gimmick rain runs down the window (office_light.set_rain), the pinned Thai label flutters (office_props.set_label);
          storm only: lightning pulse at g 48 (office_light.lightning)
    python3 shot.py probe|stills|draft|render|post|contact|qa [a:b[:s]]      (all commands: v3/film/s17/otake.py)
Needs the light textures: python3 v3/set3d_ext/light/gen_tex.py (after the office textures exist).
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                                     # noqa: E402
sys.path.insert(0, os.path.join(C.PROJ, "v3", "film", "s17"))          # the runner with office_grey / office_storm
import otake as O                                                      # noqa: E402
import acting as AC                                                    # noqa: E402
import office3d as S                                                   # noqa: E402
import office_props as X                                               # noqa: E402

smooth, smoother, lerp = O.smooth, O.smoother, O.lerp

LIGHT = os.environ.get("EX_LIGHT", "office_grey")                      # 'office_day' | 'office_grey' | 'office_storm'
DIR = HERE if LIGHT == "office_grey" else os.path.join(HERE, LIGHT)    # the runner writes work/, frames/, meta.json under DIR
os.makedirs(DIR, exist_ok=True)
TAKE, SHOTS, VERSION, HI_MAP = "ex_" + LIGHT, [2], 1, False
G0, G1, H_IN, H_OUT = 30, 66, 3, 3
TRANSITION_IN = dict(type="dissolve", frames=5, note="example")
R0, R1 = G0 - H_IN, G1 + H_OUT

HERO = (-0.55, -0.42, 0.0)                                             # hero_mark (set3d/API.md section 3)
NEAR = (2.6, -1.95, 0.0)                                               # near_mark
START = (3.55, -1.35, 0.0)                                             # window side, where the walk starts (not a named mark)
EYE = ((1.45, -6.2, 2.55), (1.3, -0.5, 2.3))                           # A['cams']['eye_two_shot']
HIGH = ((1.8, -5.9, 3.7), (1.35, -0.6, 1.55))                          # A['cams']['high_two_shot']
MOVE = (36, 60)
FLASH = 48

_dx, _dy = NEAR[0] - START[0], NEAR[1] - START[1]
WALK_LEN = math.hypot(_dx, _dy)
WDIR = (_dx / WALK_LEN, _dy / WALK_LEN)
STEP = 0.68
ARRIVE = 60                                                            # he plants on near_mark here
TW = 2 * STEP                                                          # two steps: lands on a contact phase
SPEED = WALK_LEN / TW
GW = ARRIVE - TW * 30.0                                                # walk clock zero (film frame)


def setup(T):
    for name, val in (("eye_two_shot", EYE), ("high_two_shot", HIGH)):
        c = T.A["cams"][name]
        assert max(abs(a - b) for a, b in zip(tuple(c["loc"]) + tuple(c["look_at"]), val[0] + val[1])) < 1e-3, name


def post_build(T):
    """called once after the set, the light preset and the actor cards exist: key what is not per-frame state."""
    T.OL.set_rain(drizzle=1.0, lash=1.0 if LIGHT == "office_storm" else 0.0)
    if LIGHT == "office_storm":
        T.OL.lightning(FLASH + 1)                                      # Blender frame = g + 1; keys f, f+1, f+2 and 0 on f+3


def cam(g):
    u = smoother((g - MOVE[0]) / float(MOVE[1] - MOVE[0]))
    k = 0.02 * C.creep((g - R0) / float(R1 - R0))                       # a 2 % creep under the move so it never parks
    loc, look = C.blend_cam(EYE, HIGH, u)
    return lerp(loc, look, k), look, None, 22.0


def props(g, f):
    S.set_track(1.0, 0.0, frame=f)
    X.set_label(1.0, flutter=0.5 + 0.5 * math.sin(g * 0.7), frame=f)
    a, w = X.spinner_angle(g / 30.0)
    X.set_spinner(u=0.0, angle=a, wobble=w, frame=f)


def _walk(g):
    t = (g - GW) / 30.0
    if t <= 0:
        p = AC.boss_walk(0.0, speed=SPEED, facing=-1, step=STEP)
    elif t < TW:
        p = AC.boss_walk(t, speed=SPEED, facing=-1, step=STEP)
    else:                                                               # planted: settle the knees and the bob over 5 frames
        p = dict(AC.boss_walk(TW, speed=SPEED, facing=-1, step=STEP))
        e = smooth(ARRIVE, ARRIVE + 5, g)
        legs = dict(p["legs"]); legs["crouch"] = legs["crouch"] * (1 - e); p["legs"] = legs
        p["_lift"] = p["_lift"] * (1 - e); p["_adv"] = SPEED * TW
    return p


def boss_place(g):
    p = _walk(g)
    a = p.get("_adv", 0.0)
    return (START[0] + WDIR[0] * a, START[1] + WDIR[1] * a, p.get("_lift", 0.0)), False


def boss_pose(g):
    return _walk(g), None


def hero_pose(g):
    return AC.hero_slumped((g - R0) / 30.0, yaw=0.5, blinks_at=(0.7,)), None


ACTORS = [
    dict(name="boss_exg", cast="boss", place=boss_place, pose=boss_pose, ppd=320),
    dict(name="hero_exg", cast="hero", place=lambda g: (HERO, False), pose=hero_pose, ppd=320),
]

CUES = [
    (G0 / 30.0 - 0.1, 1.2, "bed", "rain on the window"),
    (G0 / 30.0 - 0.1 + 0.30, 0.08, "heel", "heel click"),
]
if LIGHT == "office_storm":
    CUES.append((FLASH / 30.0 - 0.1, 0.4, "thunder", "thunder crack on the lightning pulse"))

if __name__ == "__main__":
    O.run(sys.modules[__name__], sys.argv[1:])

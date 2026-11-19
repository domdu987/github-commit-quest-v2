#!/usr/bin/env python3
"""Example take ex_office_day: office set, office_day light (INTERIOR_DAY), runner v3/film/s10/otake.py.

36 film frames (g 30..65, 1.2 s) plus 3 + 3 handle frames for dissolves (rendered g 27..68).
  camera  low_boss (props camera) creeping in, snap g 40..52 (pull back, rise, pan) into G, then an eased push (a zoom 22 -> 25 mm)
  actors  the chief at boss_mark talks (acting.boss_talk on a synthetic loudness list, finger wag as the base gesture);
          the hero at gloat_near listens (acting.hero_listener: blinks, one gaze shift, mouth never moves)
  gimmick the red line grows from u 0.55 to 1.0 (office3d.set_track) while he talks; the storm spinner turns
    python3 shot.py probe|stills|draft|render|post|contact|qa [a:b[:s]]      (all commands: v3/film/s10/otake.py)
"""
import math
import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(DIR))                               # examples/ (common.py)
import common as C                                                     # noqa: E402
sys.path.insert(0, os.path.join(C.PROJ, "v3", "film", "s10"))          # the office_day runner
import otake as O                                                      # noqa: E402  (puts acting, stage, set3d, props on sys.path)
import acting as AC                                                    # noqa: E402
import office3d as S                                                   # noqa: E402
import office_props as X                                               # noqa: E402

smooth, smoother, lerp = O.smooth, O.smoother, O.lerp

# ----------------------------------------------------------------------------- the constants the runner reads
TAKE, SHOTS, VERSION, HI_MAP = "ex_office_day", [1], 1, False          # VERSION: bump it and `render` re-renders every frame
G0, G1 = 30, 66                                                        # film frames [G0, G1) of the shot itself
H_IN, H_OUT = 3, 3                                                     # handle frames rendered before G0 and after G1 - 1
TRANSITION_IN = dict(type="dissolve", frames=5, note="example")        # goes to meta.json for the conform

# ----------------------------------------------------------------------------- named marks and framings (copied from the APIs)
BOSS = (1.30, -0.42, 0.0)            # boss_mark  (set3d/API.md section 3)
HERO = (2.40, -1.70, 0.0)            # gloat_near (set3d_ext/props/API.md section 3)
LOW_BOSS = ((1.92, -4.40, 1.2), (1.45, -0.42, 2.27))                   # PA['cams']['low_boss']
G_CAM = ((1.55, -4.95, 2.85), (1.25, -0.40, 2.62))                     # PA['cams']['G'] (THE GLOAT FRAMING)
SNAP = (40, 52)                                                        # 12-frame snap: 0.4 s
LENS_END = 25.0                                                        # push after the snap as a zoom (keeps the near/far ratio)

TALK0 = G0                                                             # first frame of the chief's line
LOUD = C.synth_loud((G1 + H_OUT - TALK0) / 30.0, seed=3)               # acting.loudness(t0, t1, path=<wav>) with a real voice


def setup(T):
    """called by the runner after the set and props are built, before the camera is keyed: check the copied framings."""
    for name, val in (("low_boss", LOW_BOSS), ("G", G_CAM)):
        c = T.PA["cams"][name]
        assert max(abs(a - b) for a, b in zip(tuple(c["loc"]) + tuple(c["look_at"]), val[0] + val[1])) < 1e-3, name


def cam(g):
    """-> (loc, look_at, up or None, lens mm).  Never parked: a creep before the snap, an eased push after it."""
    r0 = G0 - H_IN
    if g < SNAP[0]:
        k = 0.03 * C.creep((g - r0) / float(SNAP[0] - r0))              # 3 % of the way to the look-at point, accelerating
        return lerp(LOW_BOSS[0], LOW_BOSS[1], k), LOW_BOSS[1], None, 22.0
    l0 = lerp(LOW_BOSS[0], LOW_BOSS[1], 0.03)
    if g < SNAP[1]:
        u = smoother((g - SNAP[0]) / float(SNAP[1] - SNAP[0]))
        ut = smoother(max(0.0, ((g - SNAP[0]) / float(SNAP[1] - SNAP[0]) - 0.06) / 0.94))   # the pan trails the move a hair
        return lerp(l0, G_CAM[0], u), lerp(LOW_BOSS[1], G_CAM[1], ut), None, 22.0
    x = (g - SNAP[1]) / float(G1 + H_OUT - 1 - SNAP[1])
    e = 1 - (1 - x) ** 2.2                                               # fast start, easing to 0
    return G_CAM[0], G_CAM[1], None, 22.0 * (LENS_END / 22.0) ** e


def props(g, f):
    """set (and key at Blender frame f) every prop state of film frame g."""
    S.set_track(0.55 + 0.45 * smooth(G0, SNAP[1] + 6, g), 0.0, frame=f)   # the red line grows to New York
    a, w = X.spinner_angle(g / 30.0)
    X.set_spinner(u=0.0, angle=a, wobble=w, frame=f)


def boss_pose(g):
    """-> (pose dict, pinned hands or None)."""
    t = (g - TALK0) / 30.0
    base = AC.boss_finger_wag(max(0.0, t), t0=0.35, dur=0.4, yaw=0.40, wags=3)
    return AC.boss_talk(t, LOUD, base=base), None


def hero_pose(g):
    t = (g - (G0 - H_IN)) / 30.0
    return AC.hero_listener(t, yaw=0.6, expr="unimpressed", blinks_at=(0.5,), gaze_shift=(0.9, (0.9, -0.1), (0.4, 0.15))), None


ACTORS = [
    dict(name="boss_ex", cast="boss", place=lambda g: (BOSS, False), pose=boss_pose, ppd=lambda g: 256 if g < SNAP[0] else 320),
    dict(name="hero_ex", cast="hero", place=lambda g: (HERO, True), pose=hero_pose, ppd=384),
]

CUES = [   # (narration clock s, duration s, kind, label): post writes them to cues.json at film time clock + 0.1
    (G0 / 30.0 - 0.1, 1.2, "voice", "the chief's line (synthetic loudness in this example)"),
    (SNAP[0] / 30.0 - 0.1, 0.4, "whoosh", "whoosh on the snap into G"),
]

if __name__ == "__main__":
    O.run(sys.modules[__name__], sys.argv[1:])

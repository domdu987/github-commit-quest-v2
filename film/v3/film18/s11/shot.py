#!/usr/bin/env python3
"""shot.py -- film 18 take s11 (shot 11, g 853..943 + 8 out-handle frames 944..951): yan_camp DUSK.  "ทหารเยียนทั้งค่ายเลยเรียกเถียนตันว่า ไอ้เสมียนวัว" -- soldiers round the fire mock-moo
(finger horns), laughing; the general laughs behind them.  NO lip-sync (the quotes are elsewhere): constant mouths only.  Varied poses (mock_moo a/b/c, laugh_point, cheer_cup),
staggered bounce phases.  Foreground: the set's jar (left) + a coiled rope (bottom-right, QA_ART_SET_R2 13).  Cloud base bars shortened.
Camera: set camera s11 (wide, pull-out 7 %/s, push on 30.64 s) with a linear blend.   python3 shot.py draft|final a:b[:step] [outdir]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c18 as C                                                         # noqa: E402

SHOT = "s11"; G0, G1 = 853, 944; H_IN, H_OUT = 0, 8                     # dissolve 11 into s12: half + 2 = 8 handle frames
CAMLIN = 0.5
POSES = ["soldier_mock_moo_a", "soldier_laugh_point_b", "soldier_mock_moo_c", "soldier_cheer_cup_a", "soldier_mock_moo_b", "soldier_laugh_point_c"]
STATIC_MOUTH = ("open", 0.26, 0.17)


def patches(T):
    C.patch_sky()
    C.fg_rope(T, "right")
    C.R2.dress(-3.0, 9.0, -82.5, -78.0, 11, 11, kinds=("hay", "basket", "pot", "rope", "silk", "stone", "hay"))


def camera_mod(g, t, pose):
    """tilt up 0.7 D so the bare-ground bottom shrinks (the heads stay far above y 880)."""
    pose["look_at"] = (pose["look_at"][0], pose["look_at"][1], pose["look_at"][2] + 0.7)
    return pose


def stage_factory(T):
    def stage(g, cam):
        marks = C.S.marks_for(SHOT)
        sol = marks["soldier"]; gen = marks["general"][0]
        card = C.pcard("general_laugh", mouth=STATIC_MOUTH, lean=-8 if ((g // 5) % 2 == 0) else -3, blink=0)
        C.place(card, gen[:3], cam, C.J.HEIGHT["general"], g, "general", bounce_amp=0.06, ph=0.4, roll_deg=2.0 * C.sway(g, 0, 1.5))
        for i, m in enumerate(sol):
            pose = POSES[i % len(POSES)]
            over = {}
            if "cheer_cup" in pose or "mock_moo" in pose:
                over["mouth"] = STATIC_MOUTH
            over["lean"] = (-5 if ((g + 3 * i) // 5) % 2 else 0)
            card = C.pcard(pose, **over)
            C.place(card, m[:3], cam, C.J.HEIGHT["soldier"], g, "sol%d" % i, bounce_amp=0.06, ph=0.9 * i, roll_deg=2.0 * C.sway(g, i, 1.5))
    return stage


def parse(rng):
    a, b = rng.split(":")[:2]
    step = int(rng.split(":")[2]) if rng.count(":") == 2 else 1
    return list(range(int(a), int(b) + 1, step))


if __name__ == "__main__":
    mode = sys.argv[1]
    gs = parse(sys.argv[2]) if len(sys.argv) > 2 else list(range(G0 - H_IN, G1 + H_OUT))
    if mode == "draft":
        out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "work", "draft"); T = C.Take(SHOT, "preview", patches=[patches])
    else:
        out = os.path.join(HERE, "raw"); T = C.Take(SHOT, "final", patches=[patches])
    T.render_frames(gs, out, stage_factory(T), lin=CAMLIN, mod=camera_mod)

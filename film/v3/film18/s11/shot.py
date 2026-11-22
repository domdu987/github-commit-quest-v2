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
PARAMS = (0.0, 0, 0.0, 0.8, 0.0, 0.1, 0.0, 0.6, 3.6)      # c18.make_mod: push, slide px/s, sway D, Hz, wobble D, dz, dz/t
POSES = ["soldier_mock_moo_a", "soldier_laugh_point_b", "soldier_mock_moo_c", "soldier_cheer_cup_a", "soldier_mock_moo_b", "soldier_laugh_point_c"]
MARKS = [(3.4, -83.8, 0.0), (7.6, -83.4, 0.0), (1.6, -87.4, 0.0), (9.6, -87.4, 0.0), (5.4, -88.8, 0.0), (5.4, -91.4, 0.0)]   # two big mock-mooers in front of the fire
BIG = 1.25                                                             # the two (three) mock-moo soldiers are drawn 22 % taller: big on a phone
STATIC_MOUTH = ("open", 0.26, 0.17)


CAM = ((0.0, -77.6, 1.8), (5.5, -85.5, 2.9), 22.0)
if os.environ.get("CAM11"):
    a, b, c = os.environ["CAM11"].split(":")
    CAM = (tuple(float(x) for x in a.split(",")), tuple(float(x) for x in b.split(",")), float(c))
C.S.SHOTS[SHOT]["cam"] = dict(loc=CAM[0], look_at=CAM[1], lens=CAM[2])
C.S.SHOTS[SHOT]["move"] = dict(push=0.075, slide=0, moves=[dict(t=0.55, d=0.9, dur=8)])      # eased pull-out + the planned held push-in (+20 %) on "ไอ้เสมียนวัว"


def patches(T):
    C.J.STATE["sun"].data.energy *= 0.75          # the sunlit sand in the caption band (y 880-950) blew out above 10 %: a little less key, same dusk look
    C.patch_sky()
    # world-space foreground props (rope, jar, basket) 2.8 D from the lens: the truck + dolly make them slide across the frame (recipe, ALL_TEAMS)
    C.fg_world_props(T, [("jar", 1.0, 0.95, 0.55), ("rope", -0.9, 1.0, 0.5), ("basket", 0.0, 1.15, 0.45),
                           ("jar", -1.7, 1.9, 0.9, 4.6), ("basket", 0.3, 1.9, 0.9, 4.2), ("rope", 1.9, 1.9, 0.9, 4.8), ("jar", 3.2, 1.9, 0.8, 5.6), ("rope", -3.3, 1.9, 0.9, 5.2)], 0.5, CAMLIN, C.make_mod(T.sh["dur"], *PARAMS))
    # start-of-shot ground dressing (director round 6: bare ground 30-33 % at g853-880): extra lit period props 3-4 D from the lens placed for the START pose; the truck slides them away
    C.fg_world_props(T, [("jar", -1.3, 1.7, 0.8, 3.6), ("basket", 0.9, 1.7, 0.8, 3.4), ("rope", -0.1, 1.8, 0.75, 3.0), ("basket", -2.2, 1.8, 0.8, 4.0), ("jar", 2.0, 1.8, 0.7, 4.2)], 0.03, CAMLIN, C.make_mod(T.sh["dur"], *PARAMS))
    for nm in ("cloth", "shields"):
        if nm in C.J.STATE["objects"]:
            C.J.STATE["objects"][nm].hide_render = True
    if "road" in C.J.STATE["objects"]:
        C.J.STATE["objects"]["road"].hide_render = True          # the navy plank lying at lower left (g853-888) belongs to the road mesh
    # the dark post / pole at the left edge (unlit slab, QA): remove the small connected islands of the 'wood' mesh that project into the left strip at the start / end poses
    mk = None
    for gg in (853, 930, 944, 951):
        T.camera(gg, CAMLIN, C.make_mod(T.sh["dur"], *PARAMS))
        mk = C.cut_faces_in_rect("wood", (-80, 80, 90, 800), T.cam, mk)
    print("post faces cut:", C.cut_islands("wood", mk))
    mk = None
    for gg in (925, 935, 944, 951):
        T.camera(gg, CAMLIN, C.make_mod(T.sh["dur"], *PARAMS))
        mk = C.cut_faces_in_rect("tent3", (-80, 0, 130, 900), T.cam, mk)
    print("tent3 pole faces cut:", C.cut_islands("tent3", mk, 300))
    for tn in ("tent1", "tent12"):
        mk = None
        for gg in (920, 930, 940, 944, 951):
            T.camera(gg, CAMLIN, C.make_mod(T.sh["dur"], *PARAMS))
            mk = C.cut_faces_in_rect(tn, (-80, 380, 220, 720), T.cam, mk)
        print(tn, "ridge pole faces cut:", C.cut_islands(tn, mk, 120))
    for nm in ("pools", "wallpools"):
        if nm in C.J.STATE["objects"]:
            C.J.STATE["objects"][nm].hide_render = True
    for fi in C.J.STATE["fires"]:
        if fi["ob"].location.y < -60:
            fi["E0"] *= 0.5
            fi["k"] = fi.get("k", 1.0) * 0.85


def camera_mod(g, t, pose):
    """tilt up 0.7 D so the bare-ground bottom shrinks (the heads stay far above y 880)."""
    pose["look_at"] = (pose["look_at"][0], pose["look_at"][1], pose["look_at"][2] + 0.7)
    return pose


def stage_factory(T):
    def stage(g, cam):
        marks = C.S.marks_for(SHOT)
        sol = MARKS; gen = marks["general"][0]
        card = C.pcard("general_laugh", mouth=STATIC_MOUTH, lean=-8 if ((g // 5) % 2 == 0) else -3, blink=0)
        C.place(card, gen[:3], cam, C.J.HEIGHT["general"], g, "general", bounce_amp=0.06, ph=0.4, roll_deg=2.0 * C.sway(g, 0, 1.5))
        for i, m in enumerate(sol):
            pose = POSES[i % len(POSES)]
            over = {}
            if "cheer_cup" in pose or "mock_moo" in pose:
                over["mouth"] = STATIC_MOUTH
            over["lean"] = (-10 if ((g + 3 * i) // 4) % 2 else 2)
            card = C.pcard(pose, horns=("mock_moo" in pose), **over)
            C.place(card, m[:3], cam, C.J.HEIGHT["soldier"] * (BIG if "mock_moo" in pose else 1.0), g, "sol%d" % i, bounce_amp=0.06, ph=0.9 * i, roll_deg=3.5 * C.sway(g, i, 1.5))
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
    T.render_frames(gs, out, stage_factory(T), lin=CAMLIN, mod=C.make_mod(T.sh["dur"], *PARAMS))

#!/usr/bin/env python3
"""Example take ex_map_mech: the mechanism on the wall map (set3d_ext/mech), office_grey, runner v3/film/s20/mc.py.

The mechanism is a table-top world built on the office's wall map (the lens sits 0.35 to 1.8 D from the paper). Puppets are
about 4 D tall, so no actor stands in this world; the performers are the props: the storm spinner, the pressure walls, the lane.
That is how film 1 shot it (takes s19 to s22 have no characters).

36 film frames (g 30..65) plus 3 + 3 handles (rendered g 27..68).
  camera  rake_spinner (30 deg rake from below-left, tight on the spinner) snaps g 36..48 back into rake_north (35 deg rake
          looking north up the map, both walls); target / log-distance / direction blend (mc.blend) so the snap never cuts a
          corner; a 3 % creep so it never parks (film 1's shot 19 does the same pair as its beats 0 and 1)
  gimmick the east wall rises out of the paper in four terraces (g 44..56, four thuds), the west wall follows (g 48..60),
          the lane unrolls from the south (g 50..64); the spinner turns at 0.5 rev/s
    python3 shot.py probe [a:b:step] | still g,g[,..] [draft] | draft [a:b:step] | render [a:b] | motion | cues | post
"""
import json
import math
import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(DIR))
import common as C                                                     # noqa: E402
sys.path.insert(0, os.path.join(C.PROJ, "v3", "film", "s20"))
import mc                                                              # noqa: E402  (imports bpy; puts set3d_ext/mech on sys.path)
from mc import smooth, smoother                                        # noqa: E402

TAKE, SHOTS = "ex_map_mech", [5]
G0, G1, H_IN, H_OUT = 30, 66, 3, 3
R0, R1 = G0 - H_IN, G1 + H_OUT
TRANSITION_IN = dict(type="dissolve", frames=5, note="example")
SNAP = (36, 48)


def _poses():
    import office_mech as M
    return mc.pose(M.cam("rake_spinner")), mc.pose(M.cam("rake_north"))


def cam_setup(g):
    """-> setup dict {loc, look_at, lens, up, roll} for office3d.make_camera."""
    a, b = _poses()
    e = mc.snap_e(g, SNAP[0], SNAP[1])
    p = mc.blend(a, b, e)
    p["d"] *= 1.0 - 0.03 * C.creep((g - R0) / float(R1 - R0))           # 3 % creep so it never parks
    return mc.setup_of(p)


def state(g):
    import office_mech as M
    X = mc._M["X"]
    mc.base_state()                                                    # the map as shot 19 leaves it, then override
    M.set_wall("E", rise=4.0 * smooth(44, 56, g), slide=1, lock=0, fade=1.0, pulse=0.0)
    M.set_wall("W", rise=4.0 * smooth(48, 60, g), slide=1, lock=0, fade=1.0, pulse=0.0)
    M.set_lane(smooth(50, 64, g), red=0.0, fuse=0.0, alpha=1.0, glow=0.2)
    for sd in "EW":
        M.set_picto(sd, show=0.0)
    a, w = X.spinner_angle(g / 30.0)
    X.set_spinner(u=0.10, angle=a, wobble=w)


def apply(g):
    """state + camera of film frame g (mc.render_frames calls it before each render)."""
    _ = mc._M
    state(g)
    cam = _["S"].make_camera(cam_setup(g))
    _["bpy"].context.view_layer.update()
    return cam


def probe_frame(g):
    import office_mech as M
    apply(g)
    sp = mc.project(M.world(0, 0, 0.02, u=0.10))
    ny = mc.project(M.S.track_point(1.0))
    c = cam_setup(g)
    return dict(g=g, cam=[round(x, 3) for x in c["loc"]], spinner_xy=[round(sp[0]), round(sp[1])], ny_xy=[round(ny[0]), round(ny[1])])


CUES = [
    (44 / 30.0 - 0.1, 0.6, "thud", "four thuds: the east wall rises terrace by terrace"),
    (SNAP[0] / 30.0 - 0.1, 0.4, "whoosh", "whoosh on the snap back from the spinner"),
    (50 / 30.0 - 0.1, 0.6, "hum", "lane hum as it unrolls"),
]


def post():
    """meta.json, cues.json and contact.jpg (s20/post.py does the same for s20-s22 only: its take table is hard-coded)."""
    sys.path.insert(0, os.path.join(C.PROJ, "v3", "film", "s20"))
    import post as P20
    n, gs = P20.contact(DIR, G0, G1)
    meta = dict(take=TAKE, shots=SHOTS, g0=G0, g1=G1, handle_in=H_IN, handle_out=H_OUT, transition_in=TRANSITION_IN,
                set="office (wall map as terrain) + set3d_ext/props + set3d_ext/mech", light=mc.LIGHT, samples=12,
                frames_dir="frames", first_rendered=min(gs), last_rendered=max(gs), resolution=[720, 1280], fps=30)
    json.dump(meta, open(os.path.join(DIR, "meta.json"), "w"), indent=1)
    mc.write_cues(sys.modules[__name__])
    print("post: %d frames, meta.json, cues.json, contact.jpg" % n)


if __name__ == "__main__":
    os.makedirs(os.path.join(DIR, "work"), exist_ok=True)
    if sys.argv[1:2] == ["post"]:
        post()
    else:
        mc.main(sys.modules[__name__])

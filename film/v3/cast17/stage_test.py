#!/usr/bin/env python3
"""stage_test.py -- the cast17 members as v3/stage actors (unlit emission cards) in the stub room, lit by the room's sun: one Cycles frame
at 360x640 -> stage_test.png (and a second angle, stage_test2.png, key light from the other side).  Proves canvases, sprites,
cast shadows on the floor and that every card stands on the floor.
    python3 stage_test.py
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import cast17  # noqa: E402,F401  (registers before sprites is imported: the canvases reach sprites.DEFAULT_CANVAS)
sys.path.insert(0, os.path.join(PROJ, "v3", "stage"))
import bpy  # noqa: E402
import actors, camrig, render, sprites, stubroom  # noqa: E402,E401

OUT = os.path.join(HERE, "tmp_stage")
os.makedirs(OUT, exist_ok=True)

CAST = (  # name, cast, story pose, x, y (depth, room toward -y)
    ("ber", "bertillon", "bertillon_measuring", -1.95, -2.3),
    ("chi", "inspector17", "inspector_arms_crossed", -0.65, -2.45),
    ("pre", "prefect", "prefect_finger_up_three", 0.75, -2.3),
    ("dup", "dupont", "dupont_innocent", 1.95, -2.4),
    ("gdA", "gendarme_a", "gendarme_standing_a", -1.35, -1.1),
    ("gdB", "gendarme_b", "gendarme_laughing_b", 1.3, -1.1),
)


def run(az, out_name):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    render.setup(scene, "final", threads=2)
    stubroom.build(scene, az=az)
    cam = camrig.make_camera(scene)
    acts = []
    for nm, cast, story, x, y in CAST:
        a = actors.Actor(nm, cast)
        a.build(sprites.DEFAULT_CANVAS[cast], os.path.join(OUT, "sprites"), contact=True)
        a.head_flip = True
        a.place(1, (x, y, 0.0))
        acts.append((a, story))
    mid = (0.0, -1.9, 2.0)
    camrig.key_pose(1, camrig.cam_for(mid, head_px=112, height_class="eye", yaw_deg=6.0, screen_x=360))
    for a, story in acts:
        a.pose(1, dict(cast17.STORY17[story][1]), camera=cam)
    for a, _ in acts:
        a.render_sprites(256)
    res = render.render_frames([1], os.path.join(OUT, "frames_" + out_name), scale=0.5, threads=2)
    shutil.copyfile(res[0]["path"], os.path.join(HERE, out_name + ".png"))
    print("wrote", os.path.join(HERE, out_name + ".png"), res[0].get("wall"))


if __name__ == "__main__":
    run(55.0, "stage_test")
    run(-50.0, "stage_test2")

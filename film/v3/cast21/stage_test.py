#!/usr/bin/env python3
"""stage_test.py -- cast21 members as v3/stage actors (unlit emission cards) in the stub room, lit by the room's sun: one Cycles frame
at 360x640 -> stage_test.png (the south bank: Cressingham and Surrey, a knight on his horse behind) and stage_test2.png (the Scots with
Wallace, the sun from the other side).  Proves canvases, sprites (including the horse + rider card), cast shadows and that every card stands on the floor.
    python3 stage_test.py
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import cast21  # noqa: E402,F401  (registers before sprites is imported: the canvases reach sprites.DEFAULT_CANVAS)
sys.path.insert(0, os.path.join(PROJ, "v3", "stage"))
import bpy  # noqa: E402
import actors, camrig, render, sprites, stubroom  # noqa: E402,E401

OUT = os.path.join(HERE, "tmp_stage")
os.makedirs(OUT, exist_ok=True)

SOUTH = (  # name, cast, pose name, x, y (depth, room toward -y)
    ("cre", "cressingham", "cressingham_pointing", -0.9, -2.2),
    ("sur", "surrey", "surrey_listening", 0.9, -2.35),
    ("knt", "knight_a_mtd", "knight_a_mounted", 2.6, -3.9),
    ("ft", "footman_a", "footman_a_point_laugh", -2.9, -1.4),
)
NORTH = (
    ("wal", "wallace", "wallace_raise_sword", 0.0, -2.2),
    ("sca", "scot_a", "scot_a_fold_spear", -1.9, -2.4),
    ("scb", "scot_b", "scot_b_chew_grass", 1.9, -2.3),
    ("hrn", "scot_horn", "scot_horn_blow", -3.0, -1.3),
    ("mor", "moray", "moray_stand_spear", 3.0, -1.4),
)


def run(cast_list, az, out_name):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    render.setup(scene, "final", threads=2)
    stubroom.build(scene, az=az)
    cam = camrig.make_camera(scene)
    acts = []
    for nm, cast, story, x, y in cast_list:
        a = actors.Actor(nm, cast)
        a.build(sprites.DEFAULT_CANVAS[cast], os.path.join(OUT, "sprites"), contact=True)
        a.head_flip = True
        a.place(1, (x, y, 0.0))
        acts.append((a, story))
    mid = (0.0, -1.9, 2.0)
    camrig.key_pose(1, camrig.cam_for(mid, head_px=82, height_class="eye", yaw_deg=6.0, screen_x=360))
    for a, story in acts:
        a.pose(1, dict(cast21.STORY21[story][1]), camera=cam)
    for a, _ in acts:
        a.render_sprites(256)
    res = render.render_frames([1], os.path.join(OUT, "frames_" + out_name), scale=0.5, threads=2)
    shutil.copyfile(res[0]["path"], os.path.join(HERE, out_name + ".png"))
    print("wrote", os.path.join(HERE, out_name + ".png"), res[0].get("wall"))


if __name__ == "__main__":
    run(SOUTH, 55.0, "stage_test")
    run(NORTH, -50.0, "stage_test2")

#!/usr/bin/env python3
"""stage_test.py -- kenta + master as v3/stage actors on cards in the stub room, one Cycles frame at 360x640 -> stage_test.png.

The key comes from screen-right (az +55), so both actors use head_flip = True.  The master (master_pat_shoulder, screen-left, his
card 0.10 D in front of kenta's) pats the boy's shoulder: his screen-right hand is pinned to a world point 0.06 D above kenta's
screen-left shoulder anchor.  Kenta (kenta_worried, turned up to him) stands screen-right.  Proves canvases, sprites, shadows,
the pinned hand, kimono sleeves, sandals and head_flip for the new cast.
    python3 stage_test.py
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import cast4  # noqa: E402,F401  (registers before sprites is imported: the canvases reach sprites.DEFAULT_CANVAS)
sys.path.insert(0, os.path.join(PROJ, "v3", "stage"))
import bpy  # noqa: E402
import actors, camrig, render, sprites, stubroom  # noqa: E402,E401

OUT = os.path.join(PROJ, "v3", "tmp", "cast4", "stage")
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
render.setup(scene, "final", threads=2)
room = stubroom.build(scene, az=55.0)
cam = camrig.make_camera(scene)

kenta = actors.Actor("kenta", "kenta")
mast = actors.Actor("master", "master")
kenta.build(sprites.DEFAULT_CANVAS["kenta"], os.path.join(OUT, "sprites"), contact=True)
mast.build(sprites.DEFAULT_CANVAS["master"], os.path.join(OUT, "sprites"), contact=True)
kenta.head_flip = mast.head_flip = True
mast.place(1, (-0.62, -1.95, 0.0))
kenta.place(1, (0.38, -1.85, 0.0))

mid = (-0.1, -1.9, 1.9)
camrig.key_pose(1, camrig.cam_for(mid, head_px=120, height_class="eye", yaw_deg=8.0, screen_x=360))

kp = dict(cast4.STORY4["kenta_worried"][1], yaw=-0.45, pitch=-0.4, gaze=(-0.6, -0.8))
kp, _ = kenta.pose(1, kp, camera=cam)
f = sprites.puppet.figure("kenta", kp, "q")
sh = f["anchors"]["shoulder_l"]
grab = actors.local_to_world(kenta, (sh[0], sh[1] - 0.06), 1)
mp = dict(cast4.STORY4["master_pat_shoulder"][1])
mp, info = mast.pose(1, mp, hands={"r": {"hand": tuple(grab), "stretch": 1.3}}, camera=cam)
print("master pat error (D):", round(info["r"]["error"], 4), "clearance (D):", round(info["r"]["clearance"], 3))

kenta.render_sprites(256)
mast.render_sprites(256)
res = render.render_frames([1], os.path.join(OUT, "frames"), scale=0.5, threads=2)
shutil.copyfile(res[0]["path"], os.path.join(HERE, "stage_test.png"))
print("wrote", os.path.join(HERE, "stage_test.png"), res[0].get("wall"))

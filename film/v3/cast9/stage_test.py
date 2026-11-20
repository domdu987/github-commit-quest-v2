#!/usr/bin/env python3
"""stage_test.py -- lin (stirring with the paddle) + the general (mocking) + a gunner (linstock) as v3/stage
actors on cards in the stub room, one Cycles frame at 360x640 -> stage_test.png.  Key from screen-right (az +55): head_flip on.
Proves canvases, sprites, shadows, the paddle, the linstock smoke and the helmet for the new cast.
    python3 stage_test.py
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import cast9  # noqa: E402,F401  (registers before sprites is imported: the canvases reach sprites.DEFAULT_CANVAS)
sys.path.insert(0, os.path.join(PROJ, "v3", "stage"))
import bpy  # noqa: E402
import actors, camrig, render, sprites, stubroom  # noqa: E402,E401

OUT = os.path.join(HERE, "tmp_stage")
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
render.setup(scene, "final", threads=2)
room = stubroom.build(scene, az=55.0)
cam = camrig.make_camera(scene)

kit = actors.Actor("lin", "lin")
hen = actors.Actor("gen", "general")
ins = actors.Actor("gun", "gunner_a")
for a in (kit, hen, ins):
    a.build(sprites.DEFAULT_CANVAS[a.cast], os.path.join(OUT, "sprites"), contact=True)
    a.head_flip = True
hen.place(1, (-1.05, -1.95, 0.0))
kit.place(1, (0.15, -1.75, 0.0))
ins.place(1, (1.15, -2.05, 0.0))

mid = (0.0, -1.9, 1.9)
camrig.key_pose(1, camrig.cam_for(mid, head_px=95, height_class="eye", yaw_deg=8.0, screen_x=360))

kit.pose(1, dict(cast9.STORY9["lin_stir"][1]), camera=cam)
hen.pose(1, dict(cast9.STORY9["general_mock"][1]), camera=cam)
ins.pose(1, dict(cast9.STORY9["gunner_light"][1]), camera=cam)

for a in (kit, hen, ins):
    a.render_sprites(256)
res = render.render_frames([1], os.path.join(OUT, "frames"), scale=0.5, threads=2)
shutil.copyfile(res[0]["path"], os.path.join(HERE, "stage_test.png"))
print("wrote", os.path.join(HERE, "stage_test.png"), res[0].get("wall"))

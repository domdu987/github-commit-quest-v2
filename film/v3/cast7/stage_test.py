#!/usr/bin/env python3
"""stage_test.py -- vincenzo_smock (lifting the framed Mona Lisa) + the director (boasting) + the newsboy (front page) as v3/stage
actors on cards in the stub room, one Cycles frame at 360x640 -> stage_test.png.  Key from screen-right (az +55): head_flip on.
Proves canvases, sprites, shadows, the held paintings / newspaper (text stays readable under head_flip with flip_text) for the new cast.
    python3 stage_test.py
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import cast7  # noqa: E402,F401  (registers before sprites is imported: the canvases reach sprites.DEFAULT_CANVAS)
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

kit = actors.Actor("vin", "vincenzo_smock")
hen = actors.Actor("dir", "director")
ins = actors.Actor("boy", "newsboy")
for a in (kit, hen, ins):
    a.build(sprites.DEFAULT_CANVAS[a.cast], os.path.join(OUT, "sprites"), contact=True)
    a.head_flip = True
hen.place(1, (-0.85, -1.95, 0.0))
kit.place(1, (0.15, -1.75, 0.0))
ins.place(1, (0.95, -2.05, 0.0))

mid = (0.0, -1.9, 1.9)
camrig.key_pose(1, camrig.cam_for(mid, head_px=95, height_class="eye", yaw_deg=8.0, screen_x=360))

kit.pose(1, dict(cast7.STORY7["vincenzo_lift"][1], flip_text=True), camera=cam)
hen.pose(1, dict(cast7.STORY7["director_boast"][1]), camera=cam)
ins.pose(1, dict(cast7.STORY7["newsboy_shout"][1], flip_text=True), camera=cam)

for a in (kit, hen, ins):
    a.render_sprites(256)
res = render.render_frames([1], os.path.join(OUT, "frames"), scale=0.5, threads=2)
shutil.copyfile(res[0]["path"], os.path.join(HERE, "stage_test.png"))
print("wrote", os.path.join(HERE, "stage_test.png"), res[0].get("wall"))

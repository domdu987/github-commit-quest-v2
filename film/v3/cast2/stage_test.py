#!/usr/bin/env python3
"""stage_test.py -- nico + padre as v3/stage actors on cards in the stub room, one Cycles frame at 360x640 -> stage_test.png.

The key comes from screen-right (az +55), so both actors use head_flip = True (thick ink side and crescent away from the key).
Padre offers the rod (padre_smug_hand_rod), nico reaches for it (nico_determined with the right hand pinned to the rod by a
world target): proves canvases, sprites, shadows, pinned hands and head_flip for the new cast.
    python3 stage_test.py
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import cast2  # noqa: E402,F401  (registers before sprites is imported: the canvases reach sprites.DEFAULT_CANVAS)
sys.path.insert(0, os.path.join(PROJ, "v3", "stage"))
import bpy  # noqa: E402
import actors, camrig, render, sprites, stubroom  # noqa: E402,E401

OUT = os.path.join(PROJ, "v3", "tmp", "cast2", "stage")
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
render.setup(scene, "final", threads=2)
room = stubroom.build(scene, az=55.0)
cam = camrig.make_camera(scene)

nico = actors.Actor("nico", "nico")
padre = actors.Actor("padre", "padre")
nico.build(sprites.DEFAULT_CANVAS["nico"], os.path.join(OUT, "sprites"), contact=True)
padre.build(sprites.DEFAULT_CANVAS["padre"], os.path.join(OUT, "sprites"), contact=True)
nico.head_flip = padre.head_flip = True
nico.place(1, (-0.62, -1.85, 0.0))
padre.place(1, (0.75, -1.9, 0.0))

mid = (-0.05, -1.75, 2.1)
camrig.key_pose(1, camrig.cam_for(mid, head_px=120, height_class="eye", yaw_deg=8.0, screen_x=360))

pp, info = padre.pose(1, dict(cast2.STORY2["padre_smug_hand_rod"][1], yaw=-0.4, mirror=True), camera=cam)
# a point on the offered rod, 0.7 D below padre's hand, in world space: nico's right hand grabs it
f = sprites.puppet.figure("padre", pp, "q")
hl = f["anchors"]["hand_l"]
grab = actors.local_to_world(padre, (hl[0], hl[1] + 0.70), 1)
npose = dict(cast2.STORY2["nico_determined"][1], yaw=0.45)
npose, ninfo = nico.pose(1, npose, hands={"r": {"hand": tuple(grab), "stretch": 1.3}}, camera=cam)
print("nico grab error (D):", round(ninfo["r"]["error"], 4), ninfo["r"])

nico.render_sprites(256)
padre.render_sprites(256)
res = render.render_frames([1], os.path.join(OUT, "frames"), scale=0.5, threads=2)
shutil.copyfile(res[0]["path"], os.path.join(HERE, "stage_test.png"))
print("wrote", os.path.join(HERE, "stage_test.png"), res[0].get("wall"))

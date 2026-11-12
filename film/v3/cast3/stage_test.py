#!/usr/bin/env python3
"""stage_test.py -- tommy + foreman as v3/stage actors on cards in the stub room, one Cycles frame at 360x640 -> stage_test.png.

The key comes from screen-right (az +55), so both actors use head_flip = True (thick ink side and crescent away from the key).
The foreman points up-left at the tank and holds the paintbrush out (foreman_order_paint); tommy (tommy_worried, turned to
him) takes it: his screen-left hand is pinned to a world point on the brush's ferrule.  Proves canvases, sprites, shadows,
pinned hands, sleeves and head_flip for the new cast.
    python3 stage_test.py
"""
import math
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import cast3  # noqa: E402,F401  (registers before sprites is imported: the canvases reach sprites.DEFAULT_CANVAS)
sys.path.insert(0, os.path.join(PROJ, "v3", "stage"))
import bpy  # noqa: E402
import actors, camrig, render, sprites, stubroom  # noqa: E402,E401

OUT = os.path.join(PROJ, "v3", "tmp", "cast3", "stage")
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
render.setup(scene, "final", threads=2)
room = stubroom.build(scene, az=55.0)
cam = camrig.make_camera(scene)

tommy = actors.Actor("tommy", "tommy")
fore = actors.Actor("foreman", "foreman")
tommy.build(sprites.DEFAULT_CANVAS["tommy"], os.path.join(OUT, "sprites"), contact=True)
fore.build(sprites.DEFAULT_CANVAS["foreman"], os.path.join(OUT, "sprites"), contact=True)
tommy.head_flip = fore.head_flip = True
fore.place(1, (-0.75, -1.9, 0.0))
tommy.place(1, (1.05, -1.95, 0.0))

mid = (0.0, -1.75, 2.1)
camrig.key_pose(1, camrig.cam_for(mid, head_px=120, height_class="eye", yaw_deg=8.0, screen_x=360))

fp0 = dict(cast3.STORY3["foreman_order_paint"][1], arm_r=dict(hand=(0.90, 1.10), bend=0.3, stretch=1.2), prop_r=dict(type="paintbrush", angle=0))
fp, info = fore.pose(1, fp0, camera=cam)
f = sprites.puppet.figure("foreman", fp, "q")
hr = f["anchors"]["hand_r"]
ang = math.radians(fp["prop_r"]["angle"]) if isinstance(fp.get("prop_r"), dict) and fp["prop_r"].get("angle") is not None else math.radians(-10)
grab_local = (hr[0] + 0.36 * math.cos(ang), hr[1] + 0.36 * math.sin(ang))      # the brush's ferrule
grab = actors.local_to_world(fore, grab_local, 1)
tp = dict(cast3.STORY3["tommy_worried"][1], yaw=-0.45, expr="worried")
tp, tinfo = tommy.pose(1, tp, hands={"l": {"hand": tuple(grab), "stretch": 1.3}}, camera=cam)
print("tommy grab error (D):", round(tinfo["l"]["error"], 4), tinfo["l"])

tommy.render_sprites(256)
fore.render_sprites(256)
res = render.render_frames([1], os.path.join(OUT, "frames"), scale=0.5, threads=2)
shutil.copyfile(res[0]["path"], os.path.join(HERE, "stage_test.png"))
print("wrote", os.path.join(HERE, "stage_test.png"), res[0].get("wall"))

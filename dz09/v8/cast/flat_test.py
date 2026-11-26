"""flat_test.py -- flat staging mode on the neutral stage: eye-level, low (looking up 25 deg), high (looking down 35 deg) and a
flat vs round pair, key light from the side.  Checks: the drawing is not skewed (aspect of the silhouette's box in the
frame vs the drawing), the cast shadow starts at the soles, no self-shadow on the cards.  -> tmp/flat/flat_test.png, out/flat_test.json"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy, numpy as np
import neutral8 as N, stage8 as S
from mathutils import Vector
from PIL import Image
OUT = os.path.join(HERE, "tmp", "flat")
N.reset()
L = N.build(res=(450, 800), samples=16, rim=False)
L["key"].location = (-7.0, -1.0, 5.0); N.aim(L["key"], (0, 0, 1.4))       # a side key: the worst case for the proxy self-shadow
S.tune_flat(AMB=0.25, TINT=(0.8, 0.86, 1.0), DIR=0.5, BACK=0.2, EXPO=1.0)
a = S.Actor8("kong", "kong", height=2.86, mode="flat")
b = S.Actor8("kong_round", "kong", height=2.86, mode="round")
pose = dict(arm_n="hold_cutter", prop_n=dict(type="cutter", bars=3), arm_r="hold_cutter", prop_r=dict(type="cutter", bars=3), legs="wide")
res = {}; tiles = []
CAMS = [("eye", (2.0, -9.0, 1.5), 50), ("low", (1.5, -6.5, 0.25), 35), ("high", (1.5, -6.0, 5.6), 35), ("high_round", (1.5, -6.0, 5.6), 35)]
for nm, loc, lens in CAMS:
    rnd = nm.endswith("round")
    act, oth = (b, a) if rnd else (a, b)
    oth.hide(True); act.hide(False)
    act.place((0, 0, 0), 20)
    cam = N.camera(loc, (0, 0, 1.45), lens)
    act.pose(pose, camera=cam)
    S.shadow_link([act], L["key"])
    p = os.path.join(OUT, "ft_%s.png" % nm)
    bpy.context.scene.render.filepath = p; bpy.ops.render.render(write_still=True)
    # projected box of the card corners: width/height in pixels vs the drawing's own aspect
    from bpy_extras.object_utils import world_to_camera_view as w2c
    sc = bpy.context.scene; bpy.context.view_layer.update()
    cv = S.draw8.canvas_for(act.spec)
    P = [act.world_of((x, y)) for x, y in ((cv[0], cv[1]), (cv[2], cv[1]), (cv[2], cv[3]), (cv[0], cv[3]))]
    q = [w2c(sc, cam, v) for v in P]; q = [(u.x * 450, (1 - u.y) * 800) for u in q]
    top = math.dist(q[0], q[1]); bot = math.dist(q[3], q[2]); lft = math.dist(q[0], q[3]); rgt = math.dist(q[1], q[2])
    asp = ((top + bot) / 2) / ((lft + rgt) / 2); true = (cv[2] - cv[0]) / (cv[3] - cv[1])
    res[nm] = dict(pitch_deg=round(getattr(act, "pitch", 0.0), 1), keystone_top_over_bottom=round(top / bot, 4),
                   aspect_ratio_error=round(asp / true - 1, 4), view=act.last_pose["view"])
    tiles.append(Image.open(p).convert("RGB")); print(nm, res[nm], flush=True)
W = Image.new("RGB", (450 * len(tiles), 800))
for i, t in enumerate(tiles): W.paste(t, (i * 450, 0))
W.save(os.path.join(OUT, "flat_test.png"))
json.dump(res, open(os.path.join(HERE, "out", "flat_test.json"), "w"), indent=1)

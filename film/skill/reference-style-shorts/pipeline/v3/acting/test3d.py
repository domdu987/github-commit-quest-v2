#!/usr/bin/env python3
"""test3d.py -- two acting cycles through the 3D stage sprite path (v3/stage: Actor cards, Cycles), stub room.

    python3 test3d.py [n_frames=24] [scale=0.5] [samples=6]

Actor 1: the chief's whistle stroll (boss_whistle_stroll, near-profile walk, note glyphs as sprite overlay), the card
root keyed every frame by pose['_adv'] (travel) and pose['_lift'] (bob share).  Actor 2: beach_man jump_run (jump scare,
then the run cycle at double rate), root keyed by _adv / _lift.  Writes test3d/frames/, test3d/contact.jpg and
test3d/report.json (head path, foot-slide on the floor, sprite clipping, card errors)."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import acting as A                                         # noqa: E402  (registers drawings before sprites import)
sys.path.insert(0, os.path.join(A.PROJ, "v3", "stage"))
import bpy                                                 # noqa: E402
import actors, camrig, render, sprites, stubroom           # noqa: E402

N = int(sys.argv[1]) if len(sys.argv) > 1 else 24
SCALE = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
SAMPLES = int(sys.argv[3]) if len(sys.argv) > 3 else 6
OUT = os.path.join(HERE, "test3d")
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
render.setup(scene, "draft", threads=2, samples=SAMPLES)
room = stubroom.build(scene)
cam = camrig.make_camera(scene)

boss_poses = [A.boss_whistle_stroll(i / 30.0, notes_at=(0.1, 0.4, 0.7)) for i in range(N)]
man_poses = [A.jump_run(i / 30.0, t_jump=0.1, cast="beach_man", facing=1) for i in range(N)]
cv_b = sprites.canvas_for("boss", [dict(p) for p in boss_poses] + [{}], margin=0.12)
cv_b = (cv_b[0] - 0.625, cv_b[1] - 1.0, cv_b[2] + 0.6875, cv_b[3])      # room for the note glyphs
cv_m = sprites.canvas_for("beach_man", man_poses, margin=0.12)
boss = actors.Actor("boss", "boss")
man = actors.Actor("man", "beach_man")
boss.build(cv_b, os.path.join(OUT, "sprites"), contact=True)
man.build(cv_m, os.path.join(OUT, "sprites"), contact=True)
B0 = (-2.4, -1.4)
M0 = (-0.6, -3.4)
for i in range(N):
    f = i + 1
    pb, pm = boss_poses[i], man_poses[i]
    boss.place(f, (B0[0] + pb.get("_adv", 0.0), B0[1], pb.get("_lift", 0.0)))
    man.place(f, (M0[0] + pm.get("_adv", 0.0), M0[1], pm.get("_lift", 0.0)), scale=1.0)

head = (0.0, -2.2, 2.6)
pose = camrig.cam_for(head, head_px=95, height_class="eye", yaw_deg=0.0, screen_x=360)
camrig.drift(1, N, pose, camrig.dolly(pose, right=0.6), ease="sine")


def notes(frame, p):
    if not p.get("_notes"):
        return ""
    fig = A.P.figure("boss", p, "n")
    return A.note_glyphs_svg(p["_notes"], fig["anchors"]["mouth"], 1)


rep = dict(frames=N, boss=[], man=[])
for i in range(N):
    f = i + 1
    boss.pose(f, boss_poses[i], camera=cam)
    man.pose(f, man_poses[i], camera=cam)
rb = boss.render_sprites(192, overlay=notes)
rm = man.render_sprites(192)
rep["clipped"] = dict(boss=sum(1 for r in rb if r["clipped"]), man=sum(1 for r in rm if r["clipped"]))
for i in range(N):
    f = i + 1
    for name, act, res in (("boss", boss, rb[i]), ("man", man, rm[i])):
        hx, hy, _ = actors.local_to_screen(act, cam, res["anchors"]["head"], f)
        # world height of the head and world x of the planted foot (foot slide check)
        hw = actors.local_to_world(act, res["anchors"]["head"], f, camera=cam)
        fl = actors.local_to_world(act, res["anchors"]["foot_l"], f, camera=cam)
        fr_ = actors.local_to_world(act, res["anchors"]["foot_r"], f, camera=cam)
        rep[name].append(dict(f=f, head_px=(round(hx, 1), round(hy, 1)), head_z=round(hw.z, 3),
                              foot_l=(round(fl.x, 3), round(fl.z, 3)), foot_r=(round(fr_.x, 3), round(fr_.z, 3))))
stats = render.render_frames(range(1, N + 1), os.path.join(OUT, "frames"), scale=SCALE, threads=2)
rep["render_s"] = round(sum(s["wall"] for s in stats) / len(stats), 2)
rep["retried"] = [s["frame"] for s in stats if s.get("retried")]
rep["still_wrong"] = [s["frame"] for s in stats if s.get("still_wrong")]


def bob(rows):
    z = [r["head_z"] for r in rows]
    return round(max(z) - min(z), 3)


def slide(rows):
    """largest x movement of a foot on consecutive frames while it is on the floor (z < 0.08 D above the lowest)."""
    worst = 0.0
    for k in ("foot_l", "foot_r"):
        for a, b in zip(rows[:-1], rows[1:]):
            if a[k][1] < 0.10 and b[k][1] < 0.10:
                worst = max(worst, abs(b[k][0] - a[k][0]))
    return round(worst, 3)


rep["boss_head_bob_D"] = bob(rep["boss"])
rep["boss_planted_foot_slide_D_per_frame"] = slide(rep["boss"])
rep["man_run_planted_foot_slide_D_per_frame"] = slide(rep["man"][12:])
json.dump(rep, open(os.path.join(OUT, "report.json"), "w"), indent=1)

from PIL import Image, ImageDraw                          # noqa: E402
ims = [Image.open(os.path.join(OUT, "frames", "f_%04d.png" % f)).convert("RGB") for f in range(1, N + 1)]
w, h = ims[0].size
cols = 8
rows_ = (N + cols - 1) // cols
sheet = Image.new("RGB", (cols * w, rows_ * (h + 18)), "#111")
dr = ImageDraw.Draw(sheet)
for i, im in enumerate(ims):
    x, y = (i % cols) * w, (i // cols) * (h + 18)
    sheet.paste(im, (x, y + 18))
    dr.text((x + 4, y + 3), "f%d" % (i + 1), fill="#fff")
sheet.save(os.path.join(OUT, "contact.jpg"), quality=85)
print(json.dumps({k: v for k, v in rep.items() if k not in ("boss", "man")}, indent=1))

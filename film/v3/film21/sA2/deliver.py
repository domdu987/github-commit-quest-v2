#!/usr/bin/env python3
"""deliver.py -- encode take.mkv from raw/, write meta.json, cues.json, contact.jpg, phone_sheet.jpg.  usage: python3 deliver.py"""
import os, json, subprocess, shutil, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
SEG = os.path.basename(HERE)
CFG = {"sA2": dict(first=77, g0=80, g1=159, trans=dict(type="dissolve", frames=6), cam_in="P_A", cam_out="end of the grass-chewer push (see shot.py)",
                   cues=[(80, "whoosh: swoop begins from P_A"), (100, "wind and pine rustle as the camera dives past the branches"), (114, "light-shaft shimmer"),
                         (125, "quick whoosh push-in on the grass-chewer, tiny stalk-chew foley"), (145, "soft hill wind under the calm Scots")]),
       "sB2": dict(first=295, g0=298, g1=418, trans=dict(type="dissolve", frames=6), cam_in="P_CAMP", cam_out="P_HILL (hill_low raised 0.8 m)",
                   cues=[(298, "camp ambience, hooves, banners"), (310, "crane-up whoosh over the pavilions"), (350, "river glitter, water ambience as the camera crosses"),
                         (395, "wind rising as the camera climbs Abbey Craig"), (410, "spears shifting on the ground, soft wood clack")])}[SEG]
FIRST, LAST = CFG["first"], CFG["g1"]
FR = os.path.join(HERE, "frames"); os.makedirs(FR, exist_ok=True)
for g in range(FIRST, LAST + 1):
    src = os.path.join(HERE, "raw", "g_%04d.png" % g)
    assert os.path.exists(src), "missing %d" % g
    dst = os.path.join(FR, "g_%04d.png" % g)
    if not os.path.exists(dst): shutil.copyfile(src, dst)
out = os.path.join(HERE, "take.mkv")
subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(FR, "g_%04d.png"), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", out])
size = os.path.getsize(out)
if size > 45e6:
    subprocess.check_call("rm -f take.mkv.part*; split -b 40M take.mkv take.mkv.part", shell=True, cwd=HERE)
meta = dict(segment=SEG, g0=CFG["g0"], g1=CFG["g1"], first_g=FIRST, n_frames=LAST - FIRST + 1, transition_in=CFG["trans"], handle_frames_before=CFG["g0"] - FIRST, cam_in=CFG["cam_in"], cam_out=CFG["cam_out"],
            samples=32, fps=30, size=[720, 1280], take_mkv_bytes=size, split=size > 45e6)
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
json.dump([dict(g=g, kind="sfx", label=l) for g, l in CFG["cues"]], open(os.path.join(HERE, "cues.json"), "w"), indent=1)
ims = []
for g in range(FIRST, LAST + 1, 6):
    im = Image.open(os.path.join(FR, "g_%04d.png" % g)).convert("RGB").resize((180, 320)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 52, 14], fill=(0, 0, 0)); d.text((3, 2), "g%d" % g, fill=(255, 255, 255)); d.line([0, 220, 180, 220], fill=(0, 255, 255)); ims.append(im)
cols = 9; rows = (len(ims) + cols - 1) // cols; sh = Image.new("RGB", (180 * cols, 320 * rows), (20, 20, 20))
for i, im in enumerate(ims): sh.paste(im, ((i % cols) * 180, (i // cols) * 320))
sh.save(os.path.join(HERE, "contact.jpg"), quality=88)
ims = [Image.open(os.path.join(FR, "g_%04d.png" % g)).convert("RGB").resize((360, 640)) for g in range(FIRST, LAST + 1, 15)]
sh = Image.new("RGB", (360 * len(ims), 640))
for i, im in enumerate(ims): sh.paste(im, (i * 360, 0))
sh.save(os.path.join(HERE, "phone_sheet.jpg"), quality=88)
print("delivered", meta)

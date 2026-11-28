"""in_hook.py -- compose in_hook.png: for S13 / S20 / S21 the approved clip frame (captions burnt in) beside our final-tier
720x1280 renders of the same film frame with the blocky cast (shot files unchanged; 'view' ignored = true 3D facing),
and, where it differs, the same frame with BLOCK_VIEW=compat (the figure turned to the view the puppet drawing showed)."""
import os, sys, json, subprocess
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
CLIP = os.path.join(PROJ, "v10", "film", "DZ09_EP1_hook_916_v2.mp4")
FONT = os.path.join(PROJ, "fonts", "Kanit_900Black.ttf")
FR = os.path.join(HERE, "hookcopy", "out", "final_720x1280")
SHOTS = [("S13", 636, "Kong on the phone, MCU"), ("S20", 1030, "the driver lifts his head (eyes open)"), ("S21", 1049, "the lunge")]
os.makedirs(os.path.join(HERE, "ref", "clip"), exist_ok=True)
fnt = ImageFont.truetype(FONT, 30); fs = ImageFont.truetype(FONT, 22)
rows = []
for sid, g, what in SHOTS:
    ref = os.path.join(HERE, "ref", "clip", "g%d.png" % g)
    if not os.path.exists(ref):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", CLIP, "-vf", "select=eq(n\\,%d)" % g, "-vframes", "1", ref], check=True)
    cells = [(Image.open(ref).convert("RGB"), "approved clip v2, frame %d (captions burnt in)" % g)]
    for tag, lab in (("block", "blocky cast, shot file unchanged (view ignored)"), ("block_compat", "blocky cast, BLOCK_VIEW=compat")):
        p = os.path.join(FR, "stills_" + tag, "%s_f%04d.png" % (sid, g + 1))
        if os.path.exists(p): cells.append((Image.open(p).convert("RGB"), lab))
    rows.append((sid, g, what, cells))
W = max(len(c) for *_, c in rows) * (720 + 24) + 24
H = len(rows) * (1280 + 110) + 30
can = Image.new("RGB", (W, H), (24, 24, 28)); d = ImageDraw.Draw(can)
y = 20
for sid, g, what, cells in rows:
    d.text((24, y), "%s  g=%d  %s" % (sid, g, what), font=fnt, fill=(240, 240, 240)); y += 44
    x = 24
    for im, lab in cells:
        can.paste(im.resize((720, 1280), Image.LANCZOS) if im.size != (720, 1280) else im, (x, y))
        d.text((x + 4, y + 1284), lab, font=fs, fill=(210, 210, 210)); x += 720 + 24
    y += 1280 + 66
can.save(os.path.join(HERE, "in_hook.png"))
can.resize((can.width // 3, can.height // 3), Image.LANCZOS).save(os.path.join(HERE, "out", "in_hook_small.png"))
print("in_hook.png", can.size)

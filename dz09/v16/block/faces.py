"""faces.py -- every expression and the 5 lip-sync mouths for Kong and the office zombie, rendered on the 3D head in
the cream studio, beside the sheet's expression rows -> faces.png.   nice -n 5 python3 faces.py [--spp 16]"""
import sys, os, time, argparse, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy, bc_studio as ST
import blockcast as BC, bc_face as FACE
from PIL import Image, ImageDraw, ImageFont
ap = argparse.ArgumentParser(); ap.add_argument("--spp", type=int, default=16); ap.add_argument("--px", type=int, default=300); a = ap.parse_args()
SHEET = os.path.join(HERE, "..", "..", "uploads", "sheets_v3")
OUT = os.path.join(HERE, "out", "faces"); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, "..", "..", "fonts", "Kanit_900Black.ttf")
JOBS = {
    "kong": dict(wet=False, expr=[("determined", None), ("angry", None), ("surprised", None), ("worried", None), ("sad", None), ("pain", None)],
                 extra=[("neutral", None), ("guilty", None), ("serious", ("o", 0.75)), ("serious", None, 2)],
                 mouth=[("serious", lv) for lv in (0.0, 0.25, 0.5, 0.75, 1.0)]),
    "z_office": dict(wet=True, expr=[("idle", None), ("roar", None), ("attack", None), ("growl", None)],
                     extra=[("still", None), ("head_lift", None)],
                     mouth=[("idle", lv) for lv in (0.0, 0.25, 0.5, 0.75, 1.0)]),
}
res = {}; log = []
for kind, J in JOBS.items():
    ST.reset(); ST.studio(key=700.0)
    f = BC.Figure(kind, kind, wet=J["wet"], gloves=False); f.pose(dict())
    c = f.head_c
    ST.camera((1.0, -6.0, c.z + 0.10), (0, 0, c.z + 0.03), ortho=f.head_dims[0] * 1.95)
    sc = bpy.context.scene; sc.cycles.samples = a.spp; sc.render.resolution_x = sc.render.resolution_y = a.px
    out = []
    for group in ("expr", "extra", "mouth"):
        for it in J[group]:
            e, m = it[0], it[1]; bl = it[2] if len(it) > 2 else 0
            f.set_face(e, m, bl)
            nm = "%s_%s_%s_%s" % (kind, e, str(m).replace(" ", "").replace("'", ""), bl)
            p = os.path.join(OUT, nm + ".png"); sc.render.filepath = p
            t0 = time.time(); bpy.ops.render.render(write_still=True); log.append(round(time.time() - t0, 1))
            out.append((group, e if group != "mouth" else "mouth %.2f" % m, p, (e, m, bl)))
    res[kind] = out

# ---------------------------------------------------------------------------------- sheet
fnt = ImageFont.truetype(FONT, 20); fb = ImageFont.truetype(FONT, 26)
rows = []
ks = Image.open(os.path.join(SHEET, "kong.png")).convert("RGB").crop((745, 478, 1530, 628))
zs = Image.open(os.path.join(SHEET, "z_office.png")).convert("RGB").crop((392, 588, 1130, 760))
P = a.px; pad = 10
def strip(cells, labels):
    W = len(cells) * (P + pad); im = Image.new("RGB", (W, P + 34), (236, 230, 218)); d = ImageDraw.Draw(im)
    for i, (c, l) in enumerate(zip(cells, labels)):
        im.paste(Image.open(c).convert("RGB"), (i * (P + pad), 0)); d.text((i * (P + pad) + 6, P + 4), l, font=fnt, fill=(40, 40, 40))
    return im
blocks = []
for kind, sh, title in (("kong", ks, "KONG"), ("z_office", zs, "OFFICE WORKER ZOMBIE")):
    o = res[kind]
    ex = [x for x in o if x[0] == "expr"]; xt = [x for x in o if x[0] == "extra"]; mo = [x for x in o if x[0] == "mouth"]
    s1 = strip([x[2] for x in ex], [x[1] for x in ex])
    s2 = strip([x[2] for x in xt], [("%s %s%s" % (x[3][0], ("mouth %s" % (x[3][1],)) if x[3][1] else "", " blink" if x[3][2] else "")).strip() for x in xt])
    s3 = strip([x[2] for x in mo], [x[1] for x in mo])
    k = (P + 34) / float(sh.height)
    shs = sh.resize((int(sh.width * k), P + 34), Image.LANCZOS)
    blocks.append((title, shs, s1, s2, s3))
W = max(max(b[1].width, b[2].width, b[3].width + b[4].width + 40) for b in blocks) + 40
Hh = sum(4 * (P + 34) + 4 * 40 for _ in blocks) + 60
can = Image.new("RGB", (W, Hh), (236, 230, 218)); d = ImageDraw.Draw(can)
d.text((20, 12), "DZ09 blocky cast faces: sheet expression row, then ours on the 3D head (decal drawn by code), extras, 5 lip-sync mouths", font=fb, fill=(20, 20, 20))
y = 60
for title, shs, s1, s2, s3 in blocks:
    d.text((20, y), title + "  sheet", font=fb, fill=(120, 20, 20)); y += 34
    can.paste(shs, (20, y)); y += shs.height + 6
    d.text((20, y), title + "  ours: the sheet's expressions", font=fb, fill=(20, 20, 120)); y += 34
    can.paste(s1, (20, y)); y += s1.height + 6
    d.text((20, y), "hook names / blink  |  lip sync levels (shape a)", font=fb, fill=(20, 20, 120)); y += 34
    can.paste(s2, (20, y)); can.paste(s3, (20 + s2.width + 40, y)); y += s3.height + 20
can = can.crop((0, 0, W, y + 10))
can.save(os.path.join(HERE, "faces.png"))
json.dump(dict(render_s=log), open(os.path.join(OUT, "log.json"), "w"))
print("faces done", len(log), "renders, median %.1f s" % sorted(log)[len(log) // 2])

"""turnaround.py -- Kong and the office zombie, front / 45 / side / back on a cream studio, beside the sheet crops at the
same figure height -> turnaround.png.   nice -n 5 python3 turnaround.py [--spp 32] [--h 720]"""
import sys, os, time, json, argparse
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy, bc_studio as ST
import blockcast as BC
from PIL import Image, ImageDraw, ImageFont
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("--spp", type=int, default=32); ap.add_argument("--h", type=int, default=720)
ap.add_argument("--only", default=""); a = ap.parse_args()
SHEET = os.path.join(HERE, "..", "..", "uploads", "sheets_v3")
OUT = os.path.join(HERE, "out", "turn"); os.makedirs(OUT, exist_ok=True)
FONT = "/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09/fonts/Kanit_900Black.ttf"
VIEWS = [("front", 0.0), ("45", -45.0), ("side", -90.0), ("back", 180.0)]
# the sheet turnaround windows (proportions.json) and their figure top / sole rows
PJ = json.load(open(os.path.join(HERE, "out", "proportions.json")))
SHEETV = {"kong": ("kong.png", ["front", "q45", "side", "back"]), "z_office": ("z_office.png", ["front", "q45", "side", "back"])}
WIN = {"kong": dict(front=(322, 528), q45=(530, 708), side=(712, 836), back=(845, 1056)),
       "z_office": dict(front=(240, 562), q45=(565, 816), side=(820, 1010), back=(1012, 1292))}
cells = {}
t_all = time.time(); log = []
for kind, wet, gloves in (("kong", False, False), ("z_office", True, None)):
    if a.only and a.only != kind: continue
    ST.reset(); ST.studio()
    f = BC.Figure(kind, kind, wet=wet, gloves=gloves)
    f.pose(dict(expr="determined" if kind == "kong" else "idle"))
    H = f.H
    cam = ST.camera((0, -12.0, H * 0.50), (0, 0, H * 0.50), ortho=H * 1.10)
    sc = bpy.context.scene; sc.cycles.samples = a.spp
    sc.render.resolution_y = a.h; sc.render.resolution_x = int(a.h * 0.62)
    for vname, ang in VIEWS:
        f.place((0, 0, 0), ang)
        p = os.path.join(OUT, "%s_%s.png" % (kind, vname)); sc.render.filepath = p
        t0 = time.time(); bpy.ops.render.render(write_still=True); dt = time.time() - t0
        log.append(dict(kind=kind, view=vname, wall=round(dt, 1)))
        cells[(kind, vname)] = p
json.dump(log, open(os.path.join(OUT, "render_log.json"), "w"), indent=1)

# ------------------------------------------------------------------ compose with the sheet crops at the same figure height
def fig_rows(im):
    """top / bottom rows of the figure on our cream render (anything not background)."""
    a_ = np.asarray(im.convert("RGB")).astype(int)
    bg = np.median(a_[5:20, 5:20].reshape(-1, 3), 0)
    m = np.abs(a_ - bg).sum(2) > 60
    rows = np.nonzero(m.sum(1) > 2)[0]
    return rows[0], rows[-1]

TH = a.h - 40                                   # common figure height in the sheet (px)
rows = []
for kind in ("kong", "z_office"):
    if a.only and a.only != kind: continue
    src = Image.open(os.path.join(SHEET, SHEETV[kind][0])).convert("RGB")
    vw = PJ[kind]["views"]
    sheet_cells, ours = [], []
    for (vname, _), sv in zip(VIEWS, SHEETV[kind][1]):
        x0, x1 = WIN[kind][sv]
        top, bot = vw[sv]["top"], vw[sv]["bottom"]
        crop = src.crop((x0, top - 6, x1, bot + 4))
        k = TH / float(bot - top)
        sheet_cells.append(crop.resize((int(crop.width * k), int(crop.height * k)), Image.LANCZOS))
        r = Image.open(cells[(kind, vname)]).convert("RGB")
        t, b = fig_rows(r)
        k2 = TH / float(b - t)
        rr = r.crop((0, max(0, t - 6), r.width, min(r.height, b + 4)))
        ours.append(rr.resize((int(rr.width * k2), int(rr.height * k2)), Image.LANCZOS))
    rows.append((kind, sheet_cells, ours))
pad = 14
W = max(sum(c.width for c in s) + sum(c.width for c in o) + pad * 12 for _, s, o in rows)
Hh = sum(max(c.height for c in s + o) + 70 for _, s, o in rows) + 60
canvas = Image.new("RGB", (W, Hh), (236, 230, 218)); d = ImageDraw.Draw(canvas)
fnt = ImageFont.truetype(FONT, 26); fs = ImageFont.truetype(FONT, 18)
d.text((pad, 12), "DZ09 blocky cast: sheet (left, grey band) vs our Cycles model (right), same figure height", font=fnt, fill=(30, 30, 30))
y = 60
for kind, s, o in rows:
    hh = max(c.height for c in s + o)
    x = pad
    d.rectangle([x - 6, y - 6, x + sum(c.width for c in s) + pad * 3 + 6, y + hh + 34], fill=(214, 208, 198))
    for c, (vname, _) in zip(s, VIEWS):
        canvas.paste(c, (x, y + hh - c.height)); d.text((x + 4, y + hh + 6), "sheet " + vname, font=fs, fill=(60, 60, 60)); x += c.width + pad
    x += pad * 3
    for c, (vname, _) in zip(o, VIEWS):
        canvas.paste(c, (x, y + hh - c.height)); d.text((x + 4, y + hh + 6), "ours " + vname, font=fs, fill=(60, 60, 60)); x += c.width + pad
    d.text((pad, y + hh + 6 + 0), "", font=fs)
    y += hh + 70
canvas.save(os.path.join(HERE, "turnaround.png"))
print("turnaround done in %.0f s" % (time.time() - t_all), log)

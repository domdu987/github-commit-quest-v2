#!/usr/bin/env python3
"""sheets.py -- contact sheet and comparison sheets from the finished MP4s.

    python3 sheets.py <proto_v3.mp4> <out_dir>

  contact_v3.jpg   12 evenly spaced frames of the film (with captions), labelled with frame and time
  compare_v3.png   reference A | reference B | ours before (flat v2) | ours now (3D v3), 540 px wide each, label bar
  aspects_v3.png   rows LIGHT, DEPTH, CAMERA ANGLE: best matching reference frame | v2 frame of the same beat | v3 frame
"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
TMP = os.path.join(PROJ, "v3", "tmp", "shots", "sheets")
V2 = os.path.join(PROJ, "v2", "out", "proto_v2.mp4")
FONT = os.path.join(PROJ, "fonts", "WorkSans-Black.ttf")


def font(size):
    try:
        return ImageFont.truetype(FONT, size)
    except Exception:
        return ImageFont.load_default()


def grab(mp4, g, tag):
    """frame g (0-based) of an mp4 as an RGB image."""
    os.makedirs(TMP, exist_ok=True)
    p = os.path.join(TMP, "%s_%04d.png" % (tag, g))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-vf", "select=eq(n\\,%d)" % g, "-frames:v", "1", p], check=True)
    return Image.open(p).convert("RGB")


def ref(name):
    return Image.open(os.path.join(PROJ, "ref", name + ".jpg")).convert("RGB")


def fit(im, w, h):
    return im.resize((w, h), Image.LANCZOS)


def contact(mp4, out, n=12, cols=6, w=300):
    nf = int(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", mp4]).decode().strip().strip(","))
    gs = [int(round((i + 0.5) * nf / n)) for i in range(n)]
    h = int(round(w * 1280 / 720.0))
    rows = (n + cols - 1) // cols
    S = Image.new("RGB", (cols * w, rows * h), (16, 12, 20))
    d = ImageDraw.Draw(S)
    f = font(15)
    for i, g in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * h
        S.paste(fit(grab(mp4, g, "v3"), w, h), (x, y))
        d.rectangle((x, y, x + 118, y + 20), fill=(0, 0, 0))
        d.text((x + 4, y + 1), "g%d  %.2f s" % (g, g / 30.0), fill=(255, 255, 255), font=f)
    S.save(out, quality=92)
    return gs


def panel_row(cells, w, h, bar=44, pad=6, bg=(18, 14, 24)):
    """cells = [(label, image)]: images scaled to w x h with a label bar on top."""
    S = Image.new("RGB", (len(cells) * (w + pad) + pad, h + bar + 2 * pad), bg)
    d = ImageDraw.Draw(S)
    f = font(22)
    for i, (label, im) in enumerate(cells):
        x = pad + i * (w + pad)
        d.rectangle((x, pad, x + w - 1, pad + bar - 1), fill=(40, 32, 52))
        d.text((x + 10, pad + 9), label, fill=(255, 240, 220), font=f)
        S.paste(fit(im, w, h), (x, pad + bar))
    return S


def compare(mp4, out, g_v3, g_v2, ref_a="a/t16.0", ref_b="b/t07.0"):
    cells = [("reference A  (%s)" % ref_a, ref(ref_a)), ("reference B  (%s)" % ref_b, ref(ref_b)),
             ("ours before (flat v2)", grab(V2, g_v2, "v2")), ("ours now (3D v3)", grab(mp4, g_v3, "v3"))]
    panel_row(cells, 540, 960).save(out)


def aspects(mp4, out, rows):
    """rows = [(aspect, note, ref_name, g_v2, g_v3)]"""
    w, h = 405, 720
    strips = []
    for aspect, note, rn, g2, g3 in rows:
        row = panel_row([("reference  %s" % rn, ref(rn)), ("v2 (flat), same beat", grab(V2, g2, "v2")), ("v3 (3D)", grab(mp4, g3, "v3"))], w, h)
        head = Image.new("RGB", (row.size[0], 58), (255, 214, 92))
        d = ImageDraw.Draw(head)
        d.text((12, 4), aspect, fill=(20, 14, 24), font=font(30))
        d.text((12 + 26 * len(aspect) + 30, 16), note, fill=(40, 30, 40), font=font(17))
        s = Image.new("RGB", (row.size[0], row.size[1] + 58), (18, 14, 24))
        s.paste(head, (0, 0)); s.paste(row, (0, 58))
        strips.append(s)
    S = Image.new("RGB", (strips[0].size[0], sum(s.size[1] for s in strips)), (18, 14, 24))
    y = 0
    for s in strips:
        S.paste(s, (0, y)); y += s.size[1]
    S.save(out)


if __name__ == "__main__":
    mp4, out = sys.argv[1], sys.argv[2]
    gs = contact(mp4, os.path.join(out, "contact_v3.jpg"))
    compare(mp4, os.path.join(out, "compare_v3.png"), g_v3=54, g_v2=84)
    aspects(mp4, os.path.join(out, "aspects_v3.png"),
            [("LIGHT", "one hard key: crisp cast shadows on floor and wall, shade cooler and violet, lamp glow", "a/t32.0", 112, 100),
             ("DEPTH", "real perspective: lines run to a vanishing point, things close to the lens, parallax", "b/t24.5", 31, 26),
             ("CAMERA ANGLE", "low angle: camera 1.2 D above the floor, pitched up 15 degrees", "a/t16.0", 84, 56)])
    print("contact frames", gs)

#!/usr/bin/env python3
"""sheet.py -- contact sheets and side-by-side strips for review (measuring / viewing only: Pillow).
  python3 tools/sheet.py contact <mp4> <out.jpg> [n=12] [cols=6] [w=360]     n evenly spaced frames of a video
  python3 tools/sheet.py frames <frames_dir> <out.jpg> a-b[:step] [cols] [w]  frames f_%04d.png (1-based file numbers = g + 1)
"""
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw


def grid(ims, labels, out, cols, w):
    h = int(ims[0].height * w / ims[0].width)
    rows = (len(ims) + cols - 1) // cols
    S = Image.new("RGB", (w * cols, h * rows), (20, 16, 22))
    for i, (im, lb) in enumerate(zip(ims, labels)):
        im = im.convert("RGB").resize((w, h), Image.LANCZOS)
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, 8 + 7 * len(lb), 14], fill=(0, 0, 0))
        d.text((3, 1), lb, fill=(255, 255, 0))
        S.paste(im, ((i % cols) * w, (i // cols) * h))
    S.save(out, quality=90)
    print("wrote", out, S.size)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "contact":
        mp4, out = sys.argv[2], sys.argv[3]
        n = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        cols = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        w = int(sys.argv[6]) if len(sys.argv) > 6 else 360
        nf = int(subprocess.check_output(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", mp4]).decode().strip().strip(","))
        idx = [int(round((i + 0.5) * nf / n - 0.5)) for i in range(n)]
        td = tempfile.mkdtemp()
        sel = "+".join("eq(n\\,%d)" % i for i in idx)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-threads", "2", "-i", mp4, "-vf", "select='%s'" % sel, "-vsync", "0", os.path.join(td, "c_%03d.png")], check=True)
        ims = [Image.open(os.path.join(td, "c_%03d.png" % (i + 1))) for i in range(n)]
        grid(ims, ["f%d  %.2fs" % (i, i / 30.0) for i in idx], out, cols, w)
    else:
        d, out, r = sys.argv[2], sys.argv[3], sys.argv[4]
        step = 1
        if ":" in r:
            r, step = r.split(":"); step = int(step)
        a, b = [int(v) for v in r.split("-")]
        cols = int(sys.argv[5]) if len(sys.argv) > 5 else 8
        w = int(sys.argv[6]) if len(sys.argv) > 6 else 200
        gs = list(range(a, b + 1, step))
        ims = [Image.open(os.path.join(d, "f_%04d.png" % (g + 1))) for g in gs]
        grid(ims, ["g%d" % g for g in gs], out, cols, w)

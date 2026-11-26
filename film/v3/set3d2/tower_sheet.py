#!/usr/bin/env python3
"""tower_sheet.py out.jpg img... [--cols N] [--label] : contact sheet of stills (labelled with the file name)."""
import sys, os
from PIL import Image, ImageDraw
def sheet(paths, out, cols=6, cell=(360, 640), label=True):
    rows = (len(paths) + cols - 1) // cols; W, H = cell
    s = Image.new('RGB', (cols * (W + 6), rows * (H + 6 + (18 if label else 0))), (25, 25, 25)); d = ImageDraw.Draw(s)
    for i, p in enumerate(paths):
        im = Image.open(p).convert('RGB').resize(cell, Image.LANCZOS); x = (i % cols) * (W + 6); y = (i // cols) * (H + 6 + (18 if label else 0))
        s.paste(im, (x, y + (18 if label else 0)))
        if label: d.text((x + 4, y + 3), os.path.splitext(os.path.basename(p))[0], fill=(230, 230, 230))
    s.save(out, quality=88)
if __name__ == '__main__':
    a = sys.argv[1:]; cols = 6
    if '--cols' in a: i = a.index('--cols'); cols = int(a[i + 1]); del a[i:i + 2]
    sheet(a[1:], a[0], cols=cols)

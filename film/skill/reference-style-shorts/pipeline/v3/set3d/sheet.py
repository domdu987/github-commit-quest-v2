#!/usr/bin/env python3
"""sheet.py prefix outfile [names...] : contact sheet of camera stills (review tool)."""
import sys, os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
def sheet(paths, out, cols=4, cell=(360, 640)):
    rows = (len(paths) + cols - 1) // cols; W, Hh = cell
    s = Image.new('RGB', (cols * (W + 6), rows * (Hh + 6)), (25, 25, 25))
    for i, p in enumerate(paths):
        im = Image.open(p).convert('RGB').resize(cell, Image.LANCZOS); s.paste(im, ((i % cols) * (W + 6), (i // cols) * (Hh + 6)))
    s.save(out, quality=88)
if __name__ == '__main__':
    d, prefix, out = sys.argv[1], sys.argv[2], sys.argv[3]; names = sys.argv[4:]
    sheet([os.path.join(d, prefix + n + '.png') for n in names], out, cols=min(4, len(names)))

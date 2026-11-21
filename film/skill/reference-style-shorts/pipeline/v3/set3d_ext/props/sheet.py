#!/usr/bin/env python3
"""sheet.py out.jpg img1 img2 ... [--cols N] [--h H] : labelled contact sheet (label above each picture, not on it)."""
import sys, os
from PIL import Image, ImageDraw
def sheet(out, paths, cols=5, h=480, labels=None):
    ims = [Image.open(p).convert('RGB') for p in paths]; ims = [im.resize((max(1, int(im.width * h / im.height)), h)) for im in ims]
    w = max(im.width for im in ims); rows = (len(ims) + cols - 1) // cols; S = Image.new('RGB', (cols * (w + 6), rows * (h + 22)), (24, 24, 28)); d = ImageDraw.Draw(S)
    for i, im in enumerate(ims):
        x, y = (i % cols) * (w + 6), (i // cols) * (h + 22); S.paste(im, (x, y + 20)); d.text((x + 3, y + 4), (labels or [os.path.basename(p)[:-4] for p in paths])[i], fill=(255, 255, 255))
    S.save(out, quality=88); return out
if __name__ == '__main__':
    a = sys.argv[1:]; cols = int(a[a.index('--cols') + 1]) if '--cols' in a else 5; h = int(a[a.index('--h') + 1]) if '--h' in a else 480
    ps = [x for i, x in enumerate(a[1:]) if not x.startswith('--') and (a[i] not in ('--cols', '--h'))]
    print(sheet(a[0], ps, cols, h))

#!/usr/bin/env python3
"""deliver.py -- B1: raw/g_%04d.png (g 159..301) -> frames/ -> take.mkv, contact.jpg, meta.json, cues.json."""
import os, sys, json, shutil, subprocess
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
RAW, OUT = os.path.join(HERE, 'raw'), os.path.join(HERE, 'frames')
G0, G1, GL = 159, 298, 301


def frames():
    os.makedirs(OUT, exist_ok=True)
    for g in range(G0, GL + 1):
        shutil.copyfile(os.path.join(RAW, 'g_%04d.png' % g), os.path.join(OUT, 'g_%04d.png' % g))


def encode():
    out = os.path.join(HERE, 'take.mkv')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '30', '-start_number', str(G0), '-i', os.path.join(OUT, 'g_%04d.png'), '-c:v', 'libx264rgb', '-crf', '6', '-preset', 'slow', out], check=True)
    sz = os.path.getsize(out)
    print('take.mkv', sz // 1024, 'KB')
    if sz > 45 * 1024 * 1024:
        subprocess.run(['split', '-b', '40M', out, out + '.part'], check=True)


def contact():
    gs = list(range(G0, GL + 1, 6)); cols, w, h = 8, 135, 240
    rows = (len(gs) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * w, rows * h), (20, 20, 20))
    for i, g in enumerate(gs):
        im = Image.open(os.path.join(OUT, 'g_%04d.png' % g)).convert('RGB').resize((w, h), Image.LANCZOS)
        d = ImageDraw.Draw(im); d.text((3, 3), str(g), fill=(255, 255, 255)); d.line([(0, int(880 * h / 1280)), (w, int(880 * h / 1280))], fill=(0, 255, 255))
        sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    sheet.save(os.path.join(HERE, 'contact.jpg'), quality=88)


if __name__ == '__main__':
    for c in (sys.argv[1:] or ['frames', 'encode', 'contact']):
        globals()[c]()

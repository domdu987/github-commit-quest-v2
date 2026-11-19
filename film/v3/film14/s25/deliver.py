#!/usr/bin/env python3
"""compose raw/ frames into frames/g_%04d.png (hard cuts; baked dissolves 25->26 (8 f centred on g 1764) and 27->28 (6 f centred on g 1914)),
encode take.mkv, write meta.json, cues.json and contact.jpg."""
import os, sys, json, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
FIRST, LAST = 1672, 1770
SHOT_OF = lambda g: 25
DISS = {}            # boundary -> dissolve length
def raw(s, g): return Image.open('raw/s%d_g_%04d.png' % (s, g)).convert('RGB')
def frame(g):
    s = SHOT_OF(g)
    for b, n in DISS.items():
        a0 = b - n // 2
        if a0 <= g < a0 + n:
            sa, sb = SHOT_OF(b - 1), SHOT_OF(b); w = (g - a0 + 0.5) / n; w = w * w * (3 - 2 * w)
            return Image.blend(raw(sa, g), raw(sb, g), w)
    return raw(s, g)
os.makedirs('frames', exist_ok=True)
for g in range(FIRST, LAST + 1):
    frame(g).save('frames/g_%04d.png' % g)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-framerate', '30', '-start_number', str(FIRST), '-i', 'frames/g_%04d.png', '-c:v', 'libx264rgb', '-crf', '6', '-preset', 'slow', 'take.mkv'], check=True)
n = LAST - FIRST + 1
meta = dict(take='s25', film=14, shots=[25], first_g=FIRST, n_frames=n, g0=1678, g1=1763, handle_in=6, handle_out=7,
            transition_in=dict(type='cut', frames=0),
            transitions=[dict(at=1678, type='cut', frames=0, note='from s24 (hard cut, handle g 1672-1677 rendered)')],
            transition_out=dict(type='dissolve', frames=8, note='dissolve into shot 26 (take s26, team 3) centred on g 1764 (g 1760-1767); shot 25 is rendered to g 1770 so the conform can blend; NOT baked here'),
            narration='film14/audio/narration.wav at +0.10 s', size=[720, 1280], samples=24)
json.dump(meta, open('meta.json', 'w'), indent=1)
# contact sheet: 1 frame per 0.5 s + the cut +-1 frames, 360x640 tiles
gs = sorted(set(list(range(FIRST, LAST + 1, 15)) + [1677, 1678, 1763, 1764, 1770]))
tiles = []
for g in gs:
    im = Image.open('frames/g_%04d.png' % g).resize((180, 320)); d = ImageDraw.Draw(im); d.text((3, 3), str(g), fill=(255, 255, 0)); d.line([(0, 220), (180, 220)], fill=(0, 255, 255)); tiles.append(im)
cols = 12; rows = (len(tiles) + cols - 1) // cols; S = Image.new('RGB', (cols * 180, rows * 320))
for i, t in enumerate(tiles): S.paste(t, ((i % cols) * 180, (i // cols) * 320))
S.save('contact.jpg', quality=85)
print('delivered', n, 'frames')

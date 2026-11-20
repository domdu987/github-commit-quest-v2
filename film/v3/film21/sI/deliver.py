#!/usr/bin/env python3
"""deliver.py -- take.mkv (g 1519..1639, no handles), meta.json, cues.json, contact.jpg from raw/*.png"""
import json, os, subprocess, glob, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
G0, G1 = 1519, 1640
N = G1 - G0
os.chdir(HERE)
fs = [os.path.join('raw', 'g_%04d.png' % g) for g in range(G0, G1)]
miss = [f for f in fs if not os.path.exists(f)]
assert not miss, miss[:5]
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-framerate', '30', '-start_number', str(G0), '-i', 'raw/g_%04d.png', '-frames:v', str(N), '-c:v', 'libx264rgb', '-crf', '6', '-preset', 'slow', 'take.mkv'], check=True)
if os.path.getsize('take.mkv') > 45e6:
    subprocess.run('split -b 40M take.mkv take.mkv.part', shell=True, check=True)
json.dump(dict(take='sI', film=21, segment='I', shots=['I'], first_g=G0, n_frames=N, g0=G0, g1=G1, handle_in=0, handle_out=0,
               transition_in=dict(type='cut', frames=0),
               transition_out=dict(type='cut', frames=0, note='J1 (camp_table) follows by a hard cut at g 1640'),
               world=['bridge_deck', 'bridge_high'], samples=32, size=[720, 1280]), open('meta.json', 'w'), indent=1)
cues = [
 (0, 121, 'ambience', 'the jammed bridge: hooves shuffling and stamping on planks, harness jingle, nervous horse snorts, river lapping the piers far below; a worried murmur of knights'),
 (34, 60, 'foley', 'wood creaks: the packed column tries to turn on the narrow deck, rails groan, hooves scrape and clop (peaks as the riders hop round)', 52),
 (54, 62, 'foley', 'a horse nose bumps a horse rump: dull thump, a startled whinny', 58),
 (62, 18, 'prop', 'comic POP: the knight\'s great helm flies off his head (metal ping, short spring boing), spins, then clangs and bounces once on the planks', 62),
 (66, 24, 'whoosh', 'camera crane up and back: a rising airy whoosh as the view lifts off the deck to look down the whole bridge', 72),
 (80, 10, 'foley', 'everybody gives up: a collective sigh, the horses settle, hooves go quiet; only the river and a distant banner flutter', 84),
 (89, 20, 'whoosh', 'SNAP pull-out on "เหมือนกัน" (g 1608): fast whoosh with a soft thud, then the wide valley wind', 94),
]
out = []
for c in cues:
    f0, dur, kind, label = c[0], c[1], c[2], c[3]
    d = dict(time=round(f0 / 30.0, 3), duration=round(dur / 30.0, 3), frame=G0 + f0, end_frame=G0 + f0 + dur, kind=kind, label=label)
    if len(c) > 4:
        d['peak_frame'] = G0 + c[4]
    out.append(d)
json.dump(dict(take='sI', fps=30, note='time = seconds from the take start (g 1519); frame = film g', cues=out), open('cues.json', 'w'), indent=1, ensure_ascii=False)
# contact sheet: every 8th frame, 120x213
sel = list(range(0, N, 8))
cols = 8
rows = (len(sel) + cols - 1) // cols
W, H = 180, 320
sheet = Image.new('RGB', (cols * W, rows * H), (20, 20, 20))
d = ImageDraw.Draw(sheet)
for i, f in enumerate(sel):
    im = Image.open(fs[f]).convert('RGB').resize((W, H))
    sheet.paste(im, ((i % cols) * W, (i // cols) * H))
    d.text(((i % cols) * W + 4, (i // cols) * H + 4), 'g%d' % (G0 + f), fill=(255, 255, 0))
sheet.save('contact.jpg', quality=85)
print('delivered', os.path.getsize('take.mkv') / 1e6, 'MB')

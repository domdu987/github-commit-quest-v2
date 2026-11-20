#!/usr/bin/env python3
"""renders every preset (placeholder cast on the marks) and builds the review sheet: contact.jpg (5 columns, 720x1280 tiles with a label strip, cyan line at y 880 =
top of the caption band), contact_small.jpg (1/3 size) and hue.md (stirling_hue numbers per tile + render seconds).
usage: python3 make_contact.py [final|draft] [preset ...]    (default final, all presets; draft = 360x640, 20 samples, tiles upscaled x2 for the sheet)"""
import os, sys, subprocess, time, json
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import stirling_hue as H
ORDER = ['hill_over', 'hill_eye', 'hill_low', 'bridge_deck', 'bridge_high', 'bridge_end_north', 'bridge_end_south', 'valley_wide', 'valley_loop', 'valley_river', 'camp_wide', 'camp_table', 'camp_bank', 'riverbank', 'river_low']
mode = 'draft' if 'draft' in sys.argv[1:] else 'final'; only = [a for a in sys.argv[1:] if a in ORDER] or ORDER
D = os.path.join(HERE, 'contact_tiles' if mode == 'final' else 'contact_tiles_draft'); os.makedirs(D, exist_ok=True)
if '--nosrender' not in sys.argv:
    for p in only:
        t = time.time(); subprocess.run([sys.executable, os.path.join(HERE, 'stirling.py'), 'render', p, os.path.join(D, p + '.png'), mode], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); print(p, 'wall %.0fs' % (time.time() - t), flush=True)
W, Hh, LB, COLS = 720, 1280, 48, 5; F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
rows = (len(ORDER) + COLS - 1) // COLS; S = Image.new('RGB', (COLS * (W + 10), rows * (Hh + LB + 10)), (18, 18, 22)); dr = ImageDraw.Draw(S); md = ['# set3d21 hue per tile (%s)\n' % mode, '| tile | red | orange | blue | violet | magenta | sat | val | dark | shade hue | render s | build s |', '|---|---|---|---|---|---|---|---|---|---|---|---|']
for i, p in enumerate(ORDER):
    f = os.path.join(D, p + '.png')
    if not os.path.exists(f): continue
    im = Image.open(f).convert('RGB').resize((W, Hh), Image.LANCZOS); x = (i % COLS) * (W + 10); y = (i // COLS) * (Hh + LB + 10); S.paste(im, (x, y)); dr.line([(x, y + 880), (x + W, y + 880)], fill=(0, 230, 255), width=2)
    dr.text((x + 10, y + Hh + 10), '%d %s' % (i + 1, p), fill=(230, 230, 235), font=F); st = H.frame_stats(f); fm = st['fam']
    try: j = json.load(open(f + '.json')); rt, bt = j['render_s'], j['build_s']
    except Exception: rt = bt = float('nan')
    md.append('| %s | %.1f | %.1f | %.1f | %.1f | %.1f | %.2f | %.2f | %.3f | %.1f | %.0f | %.0f |' % (p, fm['red'], fm['orange'], fm['blue'], fm['violet'], fm['magenta'], st['sat'], st['val'], st['dark'], st['shade'], rt, bt))
if mode == 'final':
    S.save(os.path.join(HERE, 'contact.jpg'), quality=88); S.resize((S.width // 3, S.height // 3), Image.LANCZOS).save(os.path.join(HERE, 'contact_small.jpg'), quality=90); open(os.path.join(HERE, 'hue.md'), 'w').write('\n'.join(md) + '\n')
else: S.resize((S.width // 3, S.height // 3), Image.LANCZOS).save(os.path.join(D, 'contact_draft.jpg'), quality=88)
print('\n'.join(md))

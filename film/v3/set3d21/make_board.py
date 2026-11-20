#!/usr/bin/env python3
"""style board: renders hill_over, camp_bank, valley_loop (placeholder cast cards) to styleboard/<preset>.png, copies them to still1..3.png, builds board.jpg (3 side by side
at 720x1280, label strip, cyan lines at y 880 / 950 = the caption band) and phone.jpg (the three at 360x640). Also prints the colour table.
usage: python3 make_board.py [final|draft] [preset ...]   (no preset = all three; 'draft' renders 360x640 at 20 samples into styleboard/draft/; 'final' without presets only rebuilds the sheets if --nosrender)"""
import os, sys, shutil, subprocess, time
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, 'styleboard')
ST = [('hill_over', 'still1.png', '1 hill_over (the hook)'), ('camp_bank', 'still2.png', '2 camp_bank (across the river)'), ('valley_loop', 'still3.png', '3 valley_loop (the bottle)')]
mode = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ('final', 'draft') else 'final'
only = [a for a in sys.argv[1:] if a in [p for p, _, _ in ST]] or [p for p, _, _ in ST]
out_dir = D if mode == 'final' else os.path.join(D, 'draft'); os.makedirs(out_dir, exist_ok=True)
if '--nosrender' not in sys.argv:
    for p in only:
        t = time.time(); subprocess.run([sys.executable, os.path.join(HERE, 'stirling.py'), 'render', p, os.path.join(out_dir, p + '.png'), mode], check=True); print(p, 'wall %.0fs' % (time.time() - t), flush=True)
if mode == 'final':
    for p, out, _ in ST: shutil.copyfile(os.path.join(D, p + '.png'), os.path.join(D, out))
    W, H, LB, G = 720, 1280, 64, 14
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
    S = Image.new('RGB', (W * 3 + G * 2, H + LB), (18, 18, 22)); dr = ImageDraw.Draw(S); P = Image.new('RGB', (360 * 3 + 8 * 2, 640), (18, 18, 22))
    for i, (p, out, lab) in enumerate(ST):
        im = Image.open(os.path.join(D, out)).convert('RGB'); x = i * (W + G); S.paste(im, (x, 0)); dr.line([(x, 880), (x + W, 880)], fill=(0, 230, 255), width=2); dr.line([(x, 950), (x + W, 950)], fill=(0, 230, 255), width=2)
        dr.text((x + 12, H + 16), lab, fill=(230, 230, 235), font=F); P.paste(im.resize((360, 640), Image.LANCZOS), (i * 368, 0))
    S.save(os.path.join(D, 'board.jpg'), quality=90); P.save(os.path.join(D, 'phone.jpg'), quality=92); print('board.jpg', S.size, 'phone.jpg', P.size)
subprocess.run([sys.executable, os.path.join(HERE, 'stirling_hue.py')] + [os.path.join(out_dir, p + '.png') for p in only])

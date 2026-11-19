#!/usr/bin/env python3
"""board.py : renders the three style-board stills (one bpy process each, 720x1280, Cycles CPU, 12 samples, no DOF), assembles
board/style_board.jpg (3 tiles side by side, labelled under each image, cyan line at y 880 on each tile), measures hue / shade hue /
brightness (jimo_hue.py) and writes board/numbers.json. NOTES.md is written by hand from these numbers.   usage: python3 jimo.py board"""
import os, sys, json, subprocess, time, re
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'board')
STILLS = [('wall', 'board_1.png', 'jimo_wall_night'), ('camp', 'board_2.png', 'yan_camp_night'), ('holes', 'board_3.png', 'wall_holes_oxen')]

def run():
    os.makedirs(OUT, exist_ok=True); times = {}
    for zone, fn, label in STILLS:
        t0 = time.time(); r = subprocess.run([sys.executable, os.path.join(HERE, 'jimo.py'), 'still', zone], capture_output=True, text=True)
        m = re.search(r'RENDER (\w+) ([\d.]+) wall s, ([\d.]+) cpu s', r.stdout); assert m, r.stdout[-800:] + r.stderr[-800:]
        times[fn] = dict(zone=zone, wall_s=float(m.group(2)), cpu_s=float(m.group(3)), process_s=round(time.time() - t0, 1)); print(fn, times[fn], flush=True)
    sheet(); import jimo_hue
    rows = jimo_hue.report([os.path.join(OUT, f) for _, f, _ in STILLS])
    for r_ in rows: r_.update(times[r_['file']])
    json.dump(rows, open(os.path.join(OUT, 'numbers.json'), 'w'), indent=1)

def sheet():
    W, H, gap, cap = 720, 1280, 24, 96; C = Image.new('RGB', (3 * W + 4 * gap, H + cap + 2 * gap), (16, 16, 24)); d = ImageDraw.Draw(C)
    try: fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 40)
    except Exception: fnt = ImageFont.load_default()
    for i, (zone, fn, label) in enumerate(STILLS):
        im = Image.open(os.path.join(OUT, fn)).convert('RGB'); x = gap + i * (W + gap); C.paste(im, (x, gap))
        d.line([(x, gap + 880), (x + W - 1, gap + 880)], fill=(0, 230, 255), width=2)
        tw = d.textlength('%d  %s' % (i + 1, label), font=fnt); d.text((x + (W - tw) / 2, gap + H + 24), '%d  %s' % (i + 1, label), fill=(235, 235, 245), font=fnt)
    C.save(os.path.join(OUT, 'style_board.jpg'), quality=92)

if __name__ == '__main__': run()

#!/usr/bin/env python3
"""film 17 v2 SET gate: stills -> v2_gate/ (jpg), contact_v2.jpg, stills.mp4, qa_stats2 numbers, stats.md.
usage:  python3 v2_gate.py render <png_dir> [W H samples]   render 3 stills per take (start / middle / end of the path; BIGZOOM takes: start / mid / end of the zoom)
        python3 v2_gate.py sheet <png_dir> <qa_stats2.py>    build v2_gate/ from the pngs (+ .json), run qa_stats2 on an mp4 of the stills"""
import os, sys, json, glob, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'v2_gate'); TAKES = ['T%d' % i for i in range(1, 9)]
def stats(f):
    """the qa_stats2 per-frame numbers on one still (90x160: sat = (max-min)/max, vivid = share sat > 0.5, luma = mean of R, G, B)."""
    a = np.asarray(Image.open(f).convert('RGB').resize((90, 160), Image.BILINEAR), dtype=np.float32); mx = a.max(-1); mn = a.min(-1); s = (mx - mn) / (mx + 1e-3)
    return float(s.mean()), float((s > 0.5).mean() * 100), float(a.mean(-1).mean())
def render(src, W=360, H=640, samples=16):
    for t in TAKES: subprocess.run([sys.executable, os.path.join(HERE, 'prefecture17.py'), 'stills', t, src, str(W), str(H), str(samples)])
def sheet(src, qa=None, tag=''):
    os.makedirs(OUT, exist_ok=True); fs = sorted(glob.glob(os.path.join(src, 'T*_g*.png'))); rows = []
    F = ImageFont.truetype(os.path.join(HERE, 'fonts', 'LiberationSerif-Bold.ttf'), 22); F2 = ImageFont.truetype(os.path.join(HERE, 'fonts', 'LiberationSerif-Bold.ttf'), 16)
    by = {t: [f for f in fs if os.path.basename(f).startswith(t + '_')] for t in TAKES}; C = 6; tw, th, lb = 360, 640, 52
    tiles = [f for t in TAKES for f in by[t]]; R = (len(tiles) + C - 1) // C; S = Image.new('RGB', (C * tw, R * (th + lb)), (14, 14, 22)); d = ImageDraw.Draw(S)
    for i, f in enumerate(tiles):
        im = Image.open(f).convert('RGB').resize((tw, th)); x, y = (i % C) * tw, (i // C) * (th + lb); S.paste(im, (x, y))
        j = json.load(open(f[:-4] + '.json')) if os.path.exists(f[:-4] + '.json') else {}; s, v, l = stats(f); nm = os.path.basename(f)[:-4]
        im.save(os.path.join(OUT, nm + tag + '.jpg'), quality=90); rows.append((nm, s, v, l, j.get('render_s', 0)))
        d.text((x + 8, y + th + 4), nm.replace('_g', '  g '), fill=(240, 236, 220), font=F); d.text((x + 8, y + th + 30), 'sat %.2f  vivid %.0f%%  luma %.0f  %.0fs' % (s, v, l, j.get('render_s', 0)), fill=(170, 175, 200), font=F2)
    S.save(os.path.join(HERE, 'v2_gate', 'contact_v2%s.jpg' % tag), quality=88)
    mp4 = os.path.join(src, 'stills.mp4')            # every still held 10 frames (qa_stats2 reads 30 fps; the mean is the still mean)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '3', '-pattern_type', 'glob', '-i', os.path.join(src, 'T*_g*.png'), '-vf', 'fps=30,format=yuv420p', '-c:v', 'libx264', '-crf', '12', mp4])
    qa_line = subprocess.run([sys.executable, qa, mp4], capture_output=True, text=True).stdout.strip() if qa else ''
    a = np.array([r[1:4] for r in rows]); L = ['# film 17 v2 SET gate%s: stills (360x640, 16 samples + OIDN, placeholder cast cards)' % (' re-gate ' + tag if tag else ''), '',
        'Targets (PLAN §2, qa_stats2): mean saturation >= 0.50, vivid >= 45 %, mean luma 85-110, no take below sat 0.47.', '',
        '**qa_stats2.py on stills.mp4** (every still held 10 frames): `%s`' % qa_line, '',
        '**mean of the stills**: sat %.3f, vivid %.1f %%, luma %.1f' % tuple(a.mean(0)), '', '| still | sat | vivid % | luma | render s (360x640) |', '|---|---|---|---|---|']
    L += ['| %s | %.3f | %.1f | %.1f | %.1f |' % r for r in rows]; L += ['', '| take | sat | vivid % | luma |', '|---|---|---|---|']
    for t in TAKES:
        tr = np.array([r[1:4] for r in rows if r[0].startswith(t + '_')])
        if len(tr): L.append('| %s | %.3f | %.1f | %.1f |' % (t, *tr.mean(0)))
    open(os.path.join(OUT, 'stats%s.md' % ('_v2' + tag if tag else '')), 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
if __name__ == '__main__':
    if sys.argv[1] == 'render': render(sys.argv[2], *[int(x) for x in sys.argv[3:6]])
    else: sheet(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None, sys.argv[4] if len(sys.argv) > 4 else '')

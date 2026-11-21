#!/usr/bin/env python3
"""post.py : contact.jpg, meta.json, popcheck numbers and timing for take s19 (no Blender)."""
import os, sys, json, glob
import numpy as np
from PIL import Image, ImageDraw
DIR = os.path.dirname(os.path.abspath(__file__))
G0, G1, H_IN, H_OUT = 1189, 1419, 8, 7
R0, R1 = G0 - H_IN, G1 + H_OUT

def contact(n=16, cols=8, h=480):
    fs = sorted(glob.glob(os.path.join(DIR, 'frames', 'g_*.png'))); gs = [int(f[-8:-4]) for f in fs]
    pick = [fs[round(i * (len(fs) - 1) / (n - 1))] for i in range(n)]
    w = int(720 * h / 1280); rows = (n + cols - 1) // cols; S = Image.new('RGB', (cols * (w + 4), rows * (h + 20)), (18, 18, 22)); d = ImageDraw.Draw(S)
    for i, f in enumerate(pick):
        g = int(f[-8:-4]); x, y = (i % cols) * (w + 4), (i // cols) * (h + 20)
        d.text((x + 3, y + 4), 'g%d  t%.2fs%s' % (g, g / 30.0, '' if G0 <= g < G1 else ' (handle)'), fill=(255, 255, 255))
        S.paste(Image.open(f).convert('RGB').resize((w, h)), (x, y + 20))
    S.save(os.path.join(DIR, 'contact.jpg'), quality=88); return len(fs), gs

def pops():
    fs = sorted(glob.glob(os.path.join(DIR, 'frames', 'g_*.png'))); prev = None; out = []
    for f in fs:
        a = np.asarray(Image.open(f).convert('RGB').resize((180, 320), Image.BILINEAR), dtype=np.float32)
        if prev is not None: out.append((int(f[-8:-4]), float(np.abs(a - prev).mean())))
        prev = a
    flags = [out[i][0] for i in range(1, len(out) - 1) if out[i][1] > 1.8 * out[i - 1][1] and out[i][1] > 1.8 * out[i + 1][1] and out[i][1] > 2.0]
    near = []; run = 0
    for g, v in out:
        if v < 0.15: run += 1
        else:
            if run: near.append((g - run, run))
            run = 0
    dark = []
    for f in fs[::5]:
        a = np.asarray(Image.open(f).convert('RGB'), dtype=np.float32)
        if a.mean() < 20 or ((a[..., 0] > 230) & (a[..., 1] < 30) & (a[..., 2] > 230)).mean() > 0.01: dark.append(int(f[-8:-4]))
    return out, flags, near, dark

if __name__ == '__main__':
    n, gs = contact(); out, flags, near, dark = pops()
    metas = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(DIR, 'work', 'meta', 'g_*.json')))]
    walls = [m['wall_s'] for m in metas]; cpus = [m['cpu_s'] for m in metas]
    meta = dict(take='s19', shots=[19], g0=G0, g1=G1, handle_in=H_IN, handle_out=H_OUT,
                transition_in=dict(type='dissolve', frames=12, note='match dissolve inside the crash push (the map behind the chief becomes the frame)'),
                transition_out=dict(type='dissolve', frames=9), set='office (wall map as terrain) + set3d_ext/props + set3d_ext/mech', light='office_grey',
                samples=12, frames_dir='frames', first_rendered=min(gs), last_rendered=max(gs), resolution=[720, 1280], fps=30)
    json.dump(meta, open(os.path.join(DIR, 'meta.json'), 'w'), indent=1)
    rep = dict(frames=n, missing=[g for g in range(R0, R1) if g not in gs], pop_flags=flags, near_still_runs=near, dark_or_magenta=dark,
               diff_mean=round(float(np.mean([v for _, v in out])), 2), diff_max=max(out, key=lambda x: x[1]),
               wall_s=[round(min(walls), 1), round(float(np.median(walls)), 1), round(max(walls), 1)] if walls else None,
               cpu_s=[round(min(cpus), 1), round(float(np.median(cpus)), 1), round(max(cpus), 1)] if cpus else None)
    json.dump(dict(rep, diffs=out), open(os.path.join(DIR, 'work', 'post.json'), 'w'))
    print(json.dumps(rep))

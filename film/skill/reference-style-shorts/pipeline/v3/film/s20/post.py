#!/usr/bin/env python3
"""post.py <take dir> : contact.jpg, meta.json, popcheck numbers and timing of a take of s20/s21/s22 (no Blender).
Film 1 only: the take table TAKES is hard-coded; a new take writes its own post (examples/map_mech/shot.py)."""
import os, sys, json, glob
import numpy as np
from PIL import Image, ImageDraw
TAKES = {
    's20': dict(shots=[20], g0=1419, g1=1516, hi=7, ho=7, tin=dict(type='dissolve', frames=9), tout=dict(type='dissolve', frames=10)),
    's21': dict(shots=[21], g0=1516, g1=1571, hi=7, ho=9, tin=dict(type='dissolve', frames=10, note='with the whip pull-out'), tout=dict(type='dissolve', frames=14)),
    's22': dict(shots=[22], g0=1571, g1=1664, hi=9, ho=11, tin=dict(type='dissolve', frames=14), tout=dict(type='dissolve', frames=17, note='matched from the arrow tip on Long Island to the shore')),
}

def contact(D, G0, G1, n=16, cols=8, h=480):
    fs = sorted(glob.glob(os.path.join(D, 'frames', 'g_*.png'))); gs = [int(f[-8:-4]) for f in fs]
    pick = [fs[round(i * (len(fs) - 1) / (n - 1))] for i in range(n)]
    w = int(720 * h / 1280); rows = (n + cols - 1) // cols; S = Image.new('RGB', (cols * (w + 4), rows * (h + 20)), (18, 18, 22)); d = ImageDraw.Draw(S)
    for i, f in enumerate(pick):
        g = int(f[-8:-4]); x, y = (i % cols) * (w + 4), (i // cols) * (h + 20)
        d.text((x + 3, y + 4), 'g%d  t%.2fs%s' % (g, g / 30.0, '' if G0 <= g < G1 else ' (handle)'), fill=(255, 255, 255))
        S.paste(Image.open(f).convert('RGB').resize((w, h)), (x, y + 20))
    S.save(os.path.join(D, 'contact.jpg'), quality=88); return len(fs), gs

def pops(D):
    fs = sorted(glob.glob(os.path.join(D, 'frames', 'g_*.png'))); prev = None; out = []
    for f in fs:
        a = np.asarray(Image.open(f).convert('RGB').resize((180, 320), Image.BILINEAR), dtype=np.float32)
        if prev is not None: out.append((int(f[-8:-4]), float(np.abs(a - prev).mean())))
        prev = a
    flags = [out[i][0] for i in range(1, len(out) - 1) if out[i][1] > 1.8 * out[i - 1][1] and out[i][1] > 1.8 * out[i + 1][1] and out[i][1] > 2.0]
    dark = []
    for f in fs[::3]:
        a = np.asarray(Image.open(f).convert('RGB'), dtype=np.float32)
        if a.mean() < 20 or ((a[..., 0] > 230) & (a[..., 1] < 30) & (a[..., 2] > 230)).mean() > 0.01: dark.append(int(f[-8:-4]))
    return out, flags, dark

if __name__ == '__main__':
    D = os.path.abspath(sys.argv[1]); take = os.path.basename(D)
    if take not in TAKES:
        sys.exit(f'post.py knows only film 1\'s takes {sorted(TAKES)} (hard-coded ranges); for a new take write your own post, as examples/map_mech/shot.py does')
    T = TAKES[take]
    G0, G1, R0, R1 = T['g0'], T['g1'], T['g0'] - T['hi'], T['g1'] + T['ho']
    n, gs = contact(D, G0, G1); out, flags, dark = pops(D)
    metas = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(D, 'work', 'meta', 'g_*.json')))]
    walls = [m['wall_s'] for m in metas]; cpus = [m['cpu_s'] for m in metas]
    meta = dict(take=take, shots=T['shots'], g0=G0, g1=G1, handle_in=T['hi'], handle_out=T['ho'], transition_in=T['tin'], transition_out=T['tout'],
                set='office (wall map as terrain) + set3d_ext/props + set3d_ext/mech', light='office_grey', samples=12, frames_dir='frames',
                first_rendered=min(gs), last_rendered=max(gs), resolution=[720, 1280], fps=30)
    json.dump(meta, open(os.path.join(D, 'meta.json'), 'w'), indent=1)
    rep = dict(frames=n, expected=R1 - R0, missing=[g for g in range(R0, R1) if g not in gs], pop_flags=flags, dark_or_magenta=dark,
               diff_mean=round(float(np.mean([v for _, v in out])), 2), diff_max=max(out, key=lambda x: x[1]),
               wall_s=[round(min(walls), 1), round(float(np.median(walls)), 1), round(max(walls), 1)] if walls else None,
               cpu_s=[round(min(cpus), 1), round(float(np.median(cpus)), 1), round(max(cpus), 1)] if cpus else None)
    json.dump(dict(rep, diffs=out), open(os.path.join(D, 'work', 'post.json'), 'w'))
    print(json.dumps(rep))

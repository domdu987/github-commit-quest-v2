#!/usr/bin/env python3
"""qa.py <take dir>: numbers for QA.md from raw/meta, frames/, the camera path (otake.qa_motion), popcheck and hue_report.
Writes <take>/work/qa.json and prints a summary."""
import json, os, subprocess, sys, importlib.util
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
d = os.path.abspath(sys.argv[1])
spec = importlib.util.spec_from_file_location('shot', os.path.join(d, 'shot.py'))
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
import otake as O
R0, R1 = M.G0 - M.H_IN, M.G1 + M.H_OUT
fr = os.path.join(d, 'frames')
out = {}
# per-frame meta
metas = []
for g in range(R0, R1):
    p = os.path.join(d, 'raw', 'meta', 'g_%04d.json' % g)
    if os.path.exists(p):
        metas.append(json.load(open(p)))
out['frames_rendered'] = len(metas)
out['frames_delivered'] = len([f for f in os.listdir(fr) if f.startswith('g_')]) if os.path.isdir(fr) else 0
out['missing'] = [g for g in range(R0, R1) if not os.path.exists(os.path.join(fr, 'g_%04d.png' % g))]
if metas:
    w = [m['wall'] for m in metas]; c = [m['cpu'] for m in metas]
    out['sec_per_frame'] = dict(wall_median=round(float(np.median(w)), 2), wall_max=round(max(w), 2), cpu_median=round(float(np.median(c)), 2))
    out['retried'] = [m['g'] for m in metas if m.get('retried')]
    regs = [(m['g'], n, r['px'], r['solve_err_D']) for m in metas for n, r in m.get('reg', {}).items()]
    if regs:
        out['registration_px'] = dict(max=max(r[2] for r in regs), mean=round(float(np.mean([r[2] for r in regs])), 3), frames=len(regs),
                                      solve_err_max_D=max(r[3] for r in regs))
    heads = {}
    for m in metas:
        for n, h in m.get('heads', {}).items():
            if -100 < h['x'] < 820 and -100 < h['y'] < 1380:
                heads.setdefault(n, []).append((m['g'], h['w'], h['x'], h['y']))
    out['heads'] = {n: dict(frames='%d-%d' % (v[0][0], v[-1][0]), w_min=min(x[1] for x in v), w_max=max(x[1] for x in v),
                            y_min=min(x[3] for x in v), y_max=max(x[3] for x in v), x_range=[min(x[2] for x in v), max(x[2] for x in v)])
                    for n, v in heads.items()}
    out['meta_rows'] = {m['g']: {k: m[k] for k in m if k in ('cam', 'pitch', 'yaw', 'heads', 'reg', 'calendar', 'storm_px', 'ny_px', 'hand_px', 'grow', 'map_hi', 'rig')} for m in metas[::6]}
# motion
q = O.qa_motion(M)
out['motion'] = dict(static_over6=q['static_over6'], linear_runs=q['linear_runs'], moves=q['moves'], streaked=q['streaked'])
# popcheck on delivered frames
if out['frames_delivered']:
    fs = sorted(f for f in os.listdir(fr) if f.startswith('g_'))
    prev, ds = None, []
    for f in fs:
        a = np.asarray(Image.open(os.path.join(fr, f)).convert('RGB').resize((180, 320), Image.BILINEAR), dtype=np.float32)
        if prev is not None:
            ds.append(float(np.abs(a - prev).mean()))
        prev = a
    pops = []
    for i, v in enumerate(ds):
        a = ds[i - 1] if i > 0 else v; b = ds[i + 1] if i + 1 < len(ds) else v
        if v > 1.8 * a and v > 1.8 * b and v > 1.0:
            pops.append((int(fs[i][2:6]), int(fs[i + 1][2:6]), round(v, 2), round(a, 2), round(b, 2)))
    out['popcheck'] = dict(pops=pops, max_change=round(max(ds), 2), median_change=round(float(np.median(ds)), 2))
    # black / magenta cards: big blocks of pure black or magenta
    bad = []
    for f in fs:
        a = np.asarray(Image.open(os.path.join(fr, f)).convert('RGB').resize((90, 160)), dtype=np.int32)
        blk = ((a.max(-1) < 6)).mean(); mag = ((a[..., 0] > 200) & (a[..., 1] < 60) & (a[..., 2] > 200)).mean()
        if blk > 0.02 or mag > 0.01:
            bad.append((f, round(float(blk), 3), round(float(mag), 3)))
    out['black_or_magenta'] = bad
    h = subprocess.run([sys.executable, os.path.join(O.V3, 'tools', 'hue_report.py'), fr], capture_output=True, text=True).stdout
    out['hue_report'] = [l for l in h.splitlines() if l.startswith("frames") or "/frames" in l or l.startswith('set') or l.startswith('target')]
json.dump(out, open(os.path.join(d, 'work', 'qa.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'meta_rows'}, indent=1))

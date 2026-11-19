#!/usr/bin/env python3
"""qa_md.py <take dir>: writes <take dir>/QA.md from work/qa.json, work/raw/meta, meta.json and the take's QA_NOTES."""
import os, sys, json, importlib.util
import numpy as np

D = os.path.abspath(sys.argv[1])
sys.path.insert(0, D); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec_ = importlib.util.spec_from_file_location('shot_' + os.path.basename(D), os.path.join(D, 'shot.py'))
M = importlib.util.module_from_spec(spec_); spec_.loader.exec_module(M)
q = json.load(open(os.path.join(D, 'work', 'qa.json')))
meta = json.load(open(os.path.join(D, 'meta.json')))
md = os.path.join(D, 'work', 'raw', 'meta')
r0, r1 = M.G0 - M.H_IN, M.G1 + M.H_OUT
rows = []
for g in range(r0, r1):
    try:
        rows.append(json.load(open(os.path.join(md, 'g_%04d.json' % g))))
    except Exception:
        pass
frames = sorted(int(f[2:6]) for f in os.listdir(os.path.join(D, 'frames')) if f.startswith('g_'))
L = []
L.append('# QA %s (shots %s)\n' % (M.TAKE, ', '.join(str(s) for s in M.SHOTS)))
L.append('Film frames g %d..%d (cut range [%d, %d)), handles in %d / out %d, transition in: %s. Set office, light %s, 12 samples, 720x1280.\n'
         % (r0, r1 - 1, M.G0, M.G1, M.H_IN, M.H_OUT, M.TRANSITION_IN.get('type'), M.LIGHT))
L.append('Frames delivered: %d of %d expected (%s). Every frame rendered in 3D (no 2D handle extension).\n'
         % (len(frames), r1 - r0, 'complete' if frames == list(range(r0, r1)) else 'INCOMPLETE'))
L.append('\n## Heads (from the per-frame meta of the final render; px at 720x1280)\n')
L.append('| actor | frames | width min-max | centre y min-max (fraction of H) | lowest head bottom y |')
L.append('|---|---|---|---|---|')
for k, v in q['heads'].items():
    L.append('| %s | %d | %.0f-%.0f | %.0f-%.0f (%.2f-%.2f) | %.0f |' % (k, v['n'], v['w'][0], v['w'][1], v['y'][0], v['y'][1], v['y'][0] / 1280., v['y'][1] / 1280., v['bottom_max']))
rat = []
for r in rows:
    h = r.get('heads', {})
    ks = sorted(h)
    near = [k for k in ks if k.startswith('hero')]; far = [k for k in ks if k.startswith('boss')]
    if near and far and h[far[0]]['w'] > 1:
        rat.append((r['g'], h[near[0]]['w'] / h[far[0]]['w']))
if rat:
    a = np.array([x[1] for x in rat])
    L.append('\nNear/far head ratio (hero / chief) where both are in the render: min %.2f, median %.2f, max %.2f.\n' % (a.min(), np.median(a), a.max()))
L.append('\n## Pinned props\n')
L.append('Max registration error: %s.\n' % (', '.join('%s %.2f px' % (k, v) for k, v in q['reg_max_px'].items()) if q['reg_max_px'] else 'no pinned prop in this take'))
L.append('\n## Camera (qa_motion method: true camera, corner speed px per frame)\n')
L.append('Moves (speed > 12 px/frame): %s.\n' % ('; '.join('g %d-%d peak %.0f px at g %d (film %.2f-%.2f s)' % (m['g'][0], m['g'][1], m['peak_px'], m['peak_g'], m['film_s'][0], m['film_s'][1]) for m in q['moves']) or 'none'))
L.append('Static runs (< 0.25 px/frame): %s. Linear runs (speed change < 2 %% per frame at > 1 px/frame): %s.\n' % (q['static_runs'] or 'none', q['linear_runs'] or 'none'))
sp = [s for g, s in q['speed']]
L.append('Speed per frame: min %.2f, median %.2f, max %.1f px.\n' % (min(sp), float(np.median(sp)), max(sp)))
L.append('\n## Popcheck (final frames, mean abs difference at 180x320)\n')
L.append('Median %.2f, max %.2f; isolated pops: %s.\n' % (q['median_diff'], q['max_diff'], q['pops'] or 'none'))
L.append('\n## Colour (`v3/tools/hue_report.py frames/`)\n')
L.append('```\n' + q['hue'].strip() + '\n```\n')
L.append('\n## Cost\n')
L.append('CPU s per final frame min / median / max: %s; wall s: %s (2 threads, other agents rendering at the same time). Retried frames: %s; still wrong: %s.\n'
         % (q['cpu_s'], q['wall_s'], q['retried'] or 'none', q['still_wrong'] or 'none'))
L.append('\n## Notes, deviations\n')
for n in getattr(M, 'QA_NOTES', []):
    L.append('- ' + n)
open(os.path.join(D, 'QA.md'), 'w').write('\n'.join(L) + '\n')
print('wrote', os.path.join(D, 'QA.md'))

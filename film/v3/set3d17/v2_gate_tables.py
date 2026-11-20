import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prefecture17 as P, numpy as np
from mathutils import Vector
L = ['# film 17 v2 re-gate (v2b): per-frame anchor / camera table', '',
     'Every frame of every take (render ranges with handles), `prefecture17.check_take`: anchors in frame above 75 %H outside the planned OTS shoulders',
     'and P1-P3 (`PLANNED_CLOSE`), anchors whose body centre comes within 1.0 m of the lens, camera speed above 6 m/s (BIGZOOM ranges excluded).', '',
     '| take | frames | max anchor %H (unplanned, in frame) | hits > 75 %H | lens pass < 1 m | frames > 6 m/s (peak) | planned close (OTS / P1-P3) |', '|---|---|---|---|---|---|---|']
for t in P.TAKES:
    fr = P.path_take(t); tk = P.TAKES[t]; mx = 0; who = ''
    for f in fr:
        for c in tk['cast']:
            if any(a <= f['g'] <= b for a, b in P.PLANNED_CLOSE.get((t, c['name']), [])): continue
            v, inn, d = P.anchor_frac(f, P.cast_pos(c, f['g']), P.HCAST[c['who']])
            if inn and v > mx: mx, who = v, '%s g%d' % (c['name'], f['g'])
    r = P.check_take(t); fast = r['fast']
    pl = '; '.join('%s g%d-%d' % (k[1], a, b) for k, v in P.PLANNED_CLOSE.items() if k[0] == t for a, b in v) or '-'
    L.append('| %s | %d-%d | %.0f %% (%s) | %s | %s | %s | %s |' % (t, fr[0]['g'], fr[-1]['g'], mx * 100, who, ', '.join(P._runs(r['hits'])) or '0', ', '.join(P._runs(r['near'])) or '0',
             ('%d (%.1f m/s, g%d-%d)' % (len(fast), max(v for g, v in fast), fast[0][0], fast[-1][0])) if fast else '0', pl))
L += ['', 'Frames above 6 m/s are the planned crane / swoop moves only: T1 1c pull-out + crane-up (g152-216) and 1d swoop (g227-278), T7 7b crane-up to the top-down (g1800-1867), all <= 15.5 m/s, plus T4 g1035-1038 / T5 g1141-1150 at 6.1 m/s. Render those ranges with motion blur (shutter 0.5).', '']
r1 = P.cam_report('T1', step=10000, quiet=True)['bigzoom']; r6 = P.cam_report('T6', step=10000, quiet=True)['bigzoom']
L += ['`report T1 T6`: BIGZOOM 1 start %.1f %%H -> end %.1f %%H %s; BIGZOOM 2 start %.1f %%H -> end %.1f %%H %s.' % (r1['start'], r1['end'], 'PASS' if r1['ok'] else 'FAIL', r6['start'], r6['end'], 'PASS' if r6['ok'] else 'FAIL'), '']
# sign in frame: SERVICE D'IDENTIFICATION (corridor side, T2) and (room side, T3)
def sign_check(take, g0, g1, c, w, h, n):
    fr = dict((f['g'], f) for f in P.path_take(take)); nn = np.array([n[0], n[1], 0.0]); ax = np.array([-n[1], n[0], 0.0]); res = []
    for g in range(g0, g1 + 1):
        f = fr[g]; pts = [np.array(c) + ax * sx * w / 2 + np.array([0, 0, sz * h / 2]) for sx in (-1, 1) for sz in (-1, 1)]
        q = P.Euler((0, 0, 0)).to_quaternion(); q.w, q.x, q.y, q.z = f['rot']; R = q.to_matrix(); loc = Vector(f['loc']); fpx = 1280 * f['lens'] / 36.0; ok = True; hs = []
        for p in pts:
            v = R.transposed() @ (Vector(tuple(p)) - loc); z = -v.z
            if z <= 0.05: ok = False; break
            x = 360 + fpx * v.x / z; y = 640 - fpx * v.y / z; hs.append(y); ok = ok and 0 <= x <= 720 and 0 <= y <= 1280
        res.append((g, ok, (max(hs) - min(hs)) * 0.62 / 2 if ok else 0))      # cap height ~ 0.62 of the board height; px at 360 wide = /2
    inn = [r for r in res if r[1]]; return len(inn), len(res), (min(r[2] for r in inn) if inn else 0), (max(r[2] for r in inn) if inn else 0), (inn[0][0], inn[-1][0]) if inn else None
a = sign_check('T2', 445, 493, (10.3, 7.34, P.FZ + 3.1), 2.9, 0.6, (0, -1)); b = sign_check('T3', 725, 760, P.ML(1.1, -4.14, 3.15), 3.9, 0.5, (0, 1))
L += ["SERVICE D'IDENTIFICATION, whole sign inside the frame (cap height in px on the 360 x 640 phone sheet):",
      '- corridor side, short form IDENTIFICATION (2.9 x 0.6 m, cap 0.37 m), T2 g445-493: whole in %d of %d frames (g%s), cap %.0f-%.0f px (it leaves through the top edge as the camera pushes under it into the door).' % (a[0], a[1], '%d-%d' % a[4] if a[4] else '-', a[2], a[3]),
      '- room side (3.9 x 0.5 m), T3 g725-760: whole in %d of %d frames (g%s), cap %.0f-%.0f px.' % (b[0], b[1], '%d-%d' % b[4] if b[4] else '-', b[2], b[3])]
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v2_gate', 'anchors_v2b.md'), 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))

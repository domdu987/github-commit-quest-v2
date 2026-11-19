"""knee calibration from RENDERED PNGs: the hive sits BEHIND the posts (YOFF 0.50); sweep its offset at each cue frame, the visible end of the hive grows with the offset until it meets the post's silhouette, then stays put (hidden behind the post): the knee = first offset where the visible end stops growing = the end TOUCHES the post. Writes calib.json."""
import sys, os, json
os.environ.setdefault('THREADS', '4'); HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import measure as M
import shot as S
res = {}
for g, side in ((1390, 'R'), (1410, 'L'), (1430, 'R')):
    sgn = 1 if side == 'R' else -1; pts = []
    for k in range(0, 9):
        off = sgn * (0.12 + 0.045 * k); S.OVERRIDE[g] = off; r = M.measure_frame(M.d, g)
        end = r[2] if side == 'R' else r[1]; pts.append((off, end)); print(g, side, round(off, 3), r, flush=True)
    S.OVERRIDE.pop(g, None)
    final = pts[-1][1]; knee = None
    for off, end in pts:
        if abs(end - final) <= 3: knee = off; break
    res[g] = dict(knee=knee, sweep=pts)
print(json.dumps({k: v['knee'] for k, v in res.items()})); json.dump(res, open(os.path.join(HERE, 'calib.json'), 'w'))

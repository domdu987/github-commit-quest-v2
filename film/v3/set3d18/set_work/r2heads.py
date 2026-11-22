import sys
sys.path.insert(0, '/home/user/github-commit-quest-v2/film/v3/set3d18')
import jimo as J
names = sys.argv[1:] or list(J.S.SHOTS)
for n in names:
    J.build(None, n, None); rows = J.head_rows(n); bad = [r for r in rows if r[0] not in ('ox',) and r[4] > 880]
    tops = {}
    for r in rows: tops.setdefault(r[1], []).append((r[3], r[4]))
    print(n, 'ROWS', len(rows), 'MAXCHIN', {t: max(c for _, c in v) for t, v in tops.items()}, 'BAD' if bad else 'ok', [(r[0], r[1], r[3], r[4]) for r in bad][:4], flush=True)

#!/usr/bin/env python3
"""T8 ground check (QA_TEAM section K): per sampled g the real staging (clean + stage_cast2 + ears) is rebuilt, then every card and prop is ray-cast down
(film/v3/tools/ground_check.py). Props mounted on a wall / hung from the ceiling are not 'on the floor': they are listed separately with the surface they hang from.
usage: python3 ground.py [--every 30] [--out GROUND.md] [--frames 1862:2052] [--gap 0.02]"""
import sys, os, math, argparse
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, 'film/v3/tools'))
ap = argparse.ArgumentParser(); ap.add_argument('--every', type=int, default=30); ap.add_argument('--out', default=os.path.join(HERE, 'GROUND.md')); ap.add_argument('--frames', default='1862:2052')
ap.add_argument('--frame-list'); ap.add_argument('--gap', type=float, default=0.02); a = ap.parse_args()
import render as R, bpy, ground_check as G
from mathutils import Vector
P = R.P; A = R.setup(); sc = bpy.context.scene; opts = G.make_opts(auto_props=True, max_prop_size=4.0, skip=r'^(back_|prop_blob)')
g0, g1 = [int(x) for x in a.frames.split(':')]; fl = [int(x) for x in a.frame_list.split(',')] if a.frame_list else sorted(set(list(range(g0, g1 + 1, a.every)) + [g1]))
DIRS = [Vector(v) for v in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1))]
def mounted(ob, dg):
    """a prop that fails the floor test but touches a wall / the ceiling within 4 cm (any bbox corner / lowest vertex): -> hit name"""
    vs = G._eval_world_verts(ob, dg); n = 0
    step = max(1, len(vs) // 400)
    for v in vs[::step]:
        for d in DIRS:
            ok, loc, nrm, idx, hob, mat = sc.ray_cast(dg, v - d * 0.002, d, distance=0.04)
            if ok and hob is not None and hob.name != ob.name and not hob.name.startswith(('c2_',)): return hob.name
    return None
rows = []; mnt = {}; air = {}
for g in fl:
    sc.frame_set(g + 1); R.clean(); acts = P.stage_cast2(R.TAKE, g, R.assign_for(g), sprite_dir=os.path.join(HERE, 'sprites'))
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
    for ob in sc.objects:
        k = G.classify(ob, opts)
        if k is None: continue
        if k == 'card' and ob.parent is not None and ob.parent.type == 'EMPTY':
            r = G.check_object(sc, dg, ob, k, g, a.gap); fp = ob.parent.matrix_world.translation.copy()      # feet point = the root empty (the card's origin is the feet)
            with G._Hidden(ob) as dgh: hz, hob = G.cast_down(sc, dgh, ob, fp)
            r.update(gap=None if hz is None else fp.z - hz, hit=hob.name if hob else None, how='feet', low=fp.z); r['status'] = 'FAIL' if hz is None or fp.z - hz > a.gap else 'OK'
        else: r = G.check_object(sc, dg, ob, k, g, a.gap)
        if r['status'] == 'FAIL' and k == 'prop' and ob.name.startswith(('dust', 'pend_', 'stv')): r['status'] = 'AIRBORNE'; air.setdefault(ob.name.rsplit('_', 3)[0] if ob.name.startswith('dust') else ob.name, []).append(g); rows.append(r); continue
        if r['status'] == 'FAIL' and k == 'prop':
            m = mounted(ob, dg)
            if m: r['status'] = 'MOUNTED'; r['hit'] = m; mnt.setdefault(ob.name, []).append(g)
        rows.append(r)
    print('g%d: %d objects checked' % (g, len([r for r in rows if r['frame'] == g])), flush=True)
fails = [r for r in rows if r['status'] == 'FAIL']; objs = sorted(set(r['obj'] for r in rows)); bad = sorted(set(r['obj'] for r in fails))
L = ['# GROUND.md: T8 ground check (client rule K, nothing floats)', '',
     '- tool: `film/v3/tools/ground_check.py` (ray cast straight down from each card\'s lowest visible sprite row / each prop\'s lowest contact points); driver `film/v3/film17v2/T8/ground.py` rebuilds the real staging for every sampled frame',
     '- frames: %s' % ', '.join(str(f) for f in fl), '- tolerance: gap > %.3f m, or no surface below, FAILS; sunk-in (gap < 0) is OK' % a.gap,
     '- `back_*` pieces (hair disc, coat panel, ears) are decoration lying on a card, not props: skipped; props that fail the floor test but touch a wall or the ceiling within 4 cm are reported as MOUNTED (wall pictures, shelves, clock, gasolier rod to the ceiling plane), not as floating',
     '- checked objects: %d, rows: %d, FAIL rows: %d, MOUNTED rows: %d, **result: %s**' % (len(objs), len(rows), len(fails), len([r for r in rows if r['status'] == 'MOUNTED']), 'FAIL (%d objects)' % len(bad) if fails else 'PASS'), '']
if bad:
    L += ['## Failing objects', '', '| object | kind | frames | worst gap |', '|---|---|---|---|']
    for o in bad:
        rr = [r for r in fails if r['obj'] == o]; L.append('| %s | %s | %s | %s |' % (o, rr[0]['kind'], ', '.join(str(r['frame']) for r in rr), 'NO SURFACE' if any(r['gap'] is None for r in rr) else '%.3f' % max(r['gap'] for r in rr)))
    L.append('')
if mnt:
    L += ['## Mounted (not floor props)', '', '| object | frames | touches |', '|---|---|---|']
    for o, fs in sorted(mnt.items()): L.append('| %s | %s | %s |' % (o, ', '.join(map(str, fs)), next(r['hit'] for r in rows if r['obj'] == o and r['status'] == 'MOUNTED')))
    L.append('')
if air:
    L += ['## Allowed airborne (tagged, not floor props)', '', '- `dust*` = floating dust motes, `pend_*` = the clock pendulum bob (hangs from its rod), `stv*` = stove smoke. Each is an effect or hangs from its mount; none is a cast card or a furniture prop.', '']
L += ['## All rows', '', '| object | frame | gap (m) | status | kind/how | surface under it |', '|---|---|---|---|---|---|']
for r in sorted(rows, key=lambda r: (r['status'] != 'FAIL', r['obj'], r['frame'])):
    L.append('| %s | %d | %s | %s | %s/%s | %s |' % (r['obj'], r['frame'], 'NO SURFACE' if r['gap'] is None else '%+.3f' % r['gap'], r['status'], r['kind'], r['how'], r['hit'] or '-'))
open(a.out, 'w').write('\n'.join(L)); print('GROUND: %d objects, %d rows, %d FAIL, %d mounted -> %s' % (len(objs), len(rows), len(fails), len(mnt), a.out))

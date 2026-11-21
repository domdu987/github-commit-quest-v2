#!/usr/bin/env python3
"""ghost_ground.py : "nothing floats" sweep of the film-23 set with film/v3/tools/ground_check.py (pip bpy: build the scene, then call it).

    python3 ghost.py ground                 every shot (one process each): build(shot) with its placeholder cards, then for every 10th frame of the
                                            x1.25 take: the shot's action state at that frame (ghost_shot_table.ACTION) + the keyed camera, and
                                            ground_check.run_check on that frame; plus ground_check.run_cli on each bare location -> set_work/ground/
    python3 ghost.py ground S07 S12         only these shots
Writes set_work/ground/<shot>.json and GROUND_<LOC>.md (the tool's own report), then GROUND_SET.md (summary)."""
import os, sys, json, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'set_work', 'ground')

def one_shot(name):
    import bpy, ghost as GH, ghost_shots as SH, ghost_shot_table as TB
    GC = GH._gc(); A = GH.build(name); f0, f1 = GH.key_camera(name, 1); sc = bpy.context.scene; n = f1 - f0; rows = []; air = {}
    fn = TB.ACTION.get(name)
    for f in sorted(set(list(range(f0, f1 + 1, 10)) + [f1])):
        t = (f - f0) / float(n) * 1.25
        if fn: fn(GH, t)
        bpy.context.view_layer.update()
        with GH.dress_hidden(): res, a = GC.run_check(sc, every=10, gap=0.02, frame_list=[f])
        rows += [dict(r, obj=r['obj'], gap=(None if r['gap'] is None else round(r['gap'], 4)), point=None, low=round(r['low'], 3)) for r in res]
        for k, v in a.items(): air.setdefault(k, []).extend(v)
    fails = [r for r in rows if r['status'] != 'OK']
    json.dump(dict(shot=name, loc=A['location'], rows=len(rows), objects=len(set(r['obj'] for r in rows)), fails=fails, airborne=air), open(os.path.join(OUT, name + '.json'), 'w'), indent=1)
    print('GROUND %s rows %d objects %d FAIL %d' % (name, len(rows), len(set(r['obj'] for r in rows)), len(fails)))

def one_location(loc):
    import bpy, ghost as GH
    GC = GH._gc(); GH.build(loc); sc = bpy.context.scene; sc.frame_start = sc.frame_end = 1
    with GH.dress_hidden(): code = GC.run_cli(['--every', '10', '--gap', '0.02', '--out', os.path.join(OUT, 'GROUND_%s.md' % loc), '--fails-only'])
    print('LOCATION %s exit %s' % (loc, code))

def main(a):
    os.makedirs(OUT, exist_ok=True)
    if len(a) > 1 and a[1] == '_shot': one_shot(a[2]); return
    if len(a) > 1 and a[1] == '_loc': one_location(a[2]); return
    import ghost_shots as SH
    shots = [x for x in a[1:] if x in SH.SHOTS] or list(SH.SHOTS); locs = [x for x in a[1:] if x in ('FIELDS', 'LANE', 'CAMP', 'RHINE')] or (['FIELDS', 'LANE', 'CAMP', 'RHINE'] if len(a) == 1 else [])
    for L in locs:
        r = subprocess.run([sys.executable, os.path.join(HERE, 'ghost.py'), 'ground', '_loc', L], capture_output=True, text=True); print([l for l in r.stdout.splitlines() if l.startswith(('LOCATION', 'ground_check'))] or r.stderr[-1500:], flush=True)
    for s in shots:
        r = subprocess.run([sys.executable, os.path.join(HERE, 'ghost.py'), 'ground', '_shot', s], capture_output=True, text=True); print([l for l in r.stdout.splitlines() if l.startswith('GROUND')] or r.stderr[-1500:], flush=True)
    summary()

def summary():
    import ghost_shots as SH
    L = ['# GROUND_SET.md : "nothing floats" (film/v3/tools/ground_check.py on the film-23 set)', '',
         'Run: `python3 ghost.py ground` (ghost_ground.py).  Tolerance 0.02 D (1 D = one head).  Per shot: build(shot) with its placeholder cards, the',
         'shot\'s action state (ghost_shot_table.ACTION: deflate, jeep, lift, pile, boats, inflating rows, riding cyclists) and the keyed camera, sampled every',
         '10th frame of the x1.25 take (first and last always), `ground_check.run_check` on each sample.  Per location: `ground_check.run_cli` on the bare',
         'build (reports in set_work/ground/GROUND_<LOC>.md).  Every prop is placed by `ground_snap` (ray cast) and has a `contact_shadow`; merged scenery',
         '(terrain, lane strips, hedges, trees, houses) is tagged gc_role "ground" and is not a prop.  The fine dressing (grass tufts, flowers, pebbles,',
         'glints, light-pool decals, mist, smoke) is HIDDEN from the rays while snapping and checking, so nothing may rest on a grass blade.', '',
         '| shot | location | samples x objects checked | FAIL | airborne (flagged, skipped) |', '|---|---|---|---|---|']
    tot = 0; tf = 0
    for s in SH.SHOTS:
        p = os.path.join(OUT, s + '.json')
        if not os.path.exists(p): L.append('| %s | - | not run | - | - |' % s); continue
        d = json.load(open(p)); tot += d['rows']; tf += len(d['fails'])
        air = ', '.join(sorted(set(d['airborne']))) or '-'
        L.append('| %s | %s | %d rows, %d objects | %d | %s |' % (s, d['loc'], d['rows'], d['objects'], len(d['fails']), air[:120]))
    L += ['', '**Total: %d checks, %d FAIL.**' % (tot, tf), '']
    for loc in ('FIELDS', 'LANE', 'CAMP', 'RHINE'):
        p = os.path.join(OUT, 'GROUND_%s.md' % loc)
        if os.path.exists(p):
            head = [l for l in open(p).read().splitlines() if 'FAIL' in l and ('objects' in l.lower() or 'result' in l.lower())][:2]
            L.append('- %s bare location: %s (set_work/ground/GROUND_%s.md)' % (loc, ' / '.join(head) or 'see report', loc))
    fl = []
    for s in SH.SHOTS:
        p = os.path.join(OUT, s + '.json')
        if os.path.exists(p):
            for r in json.load(open(p))['fails'][:12]: fl.append('| %s | %s | %s | %s | %s |' % (s, r['frame'], r['obj'], r['gap'], r.get('hit')))
    if fl: L += ['', '## Remaining fails', '', '| shot | frame | object | gap | hit |', '|---|---|---|---|---|'] + fl
    L += ['', '## Allowed off the ground (flagged `airborne`)', '- `tank_lift` while lifted (S12 / S13, the ONLY airborne tank); its contact blob stays on the grass and shrinks.',
          '- `balloon_loose` (S19, the last balloon escaping).', '- Cards parented to movers (jeep seats, boats, the lead tank deck) stand on their mover: they are checked, the ray hits the mover.']
    open(os.path.join(HERE, 'GROUND_SET.md'), 'w').write('\n'.join(L) + '\n'); print('\n'.join(L[-30:]))

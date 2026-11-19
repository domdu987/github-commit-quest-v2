#!/usr/bin/env python3
"""run15.py : CLI. python3 run15.py stills [shots] | final [shots] | contact   (shots: 1,2,5-9 ...). Output in work/."""
import os, sys, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import set15 as F
import set15_shots as SH
HERE = F.HERE; WORK = F.WORK
def parse(a):
    out = []
    for tok in a.split(','):
        if '-' in tok: x, y = tok.split('-'); out += list(range(int(x), int(y) + 1))
        elif tok: out.append(int(tok))
    return out
def render_shot(n, quality='final', outdir=None, actors=True, light=None, which='a'):
    sd = F.SHOTS[n]; lt = light or sd['light']
    if (F.STATE.get('loc'), F.STATE.get('light')) != (sd['loc'], lt) or True:
        A = F.build(sd['loc'], lt)
    sc = bpy.context.scene; F.setup_render(sc, quality)
    cam = SH.setup_shot(n)
    F.crowd_mode(sd.get('crowd', 'hush' if 24 <= n <= 30 else 'normal')) if sd['loc'] == 'B' else None
    sc.frame_set(int(round(sd['t0'] * 30)) if which == 'a' else int(round(sd['t1'] * 30)))
    if actors: F.stage_placeholders(n, tuple(cam.location))
    bpy.context.view_layer.update(); hp = F.head_pixels(n)
    outdir = outdir or os.path.join(WORK, 'final' if quality == 'final' else 'stills'); os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, 'shot%02d_%s_%s.png' % (n, sd['loc'], lt)); w, c = F.T.render(path)
    return path, w, c, hp
if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'; shots = parse(sys.argv[2]) if len(sys.argv) > 2 else sorted(F.SHOTS)
    if cmd in ('stills', 'final'):
        log = []
        for n in shots:
            p, w, c, hp = render_shot(n, 'final' if cmd == 'final' else 'preview')
            print('%s shot %d: %.1f s wall, %.1f s cpu, heads %s' % (cmd, n, w, c, hp), flush=True); log.append((n, w, c, hp))
    else: print(__doc__)

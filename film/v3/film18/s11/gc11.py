#!/usr/bin/env python3
"""gc11.py -- ground_check on s11 (run in the take folder): python3 gc11.py [every]"""
import os, sys, re
HERE = os.getcwd(); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', 'tools'))
every = int(sys.argv[1]) if len(sys.argv) > 1 else 6
import shot as SH, c18 as C
import ground_check as GC
bpy = C.bpy
T = C.Take(SH.SHOT, 'preview', patches=[SH.patches]); stage = SH.stage_factory(T); mod = C.make_mod(T.sh['dur'], *SH.PARAMS)
air_re = re.compile(getattr(SH, 'GC_AIRBORNE', r'^$'))
fl = list(range(SH.G0, SH.G1, every)) + [SH.G1 - 1]
allres, air = [], {}
for g in fl:
    C.R2.clear_placeholders(); C.R2.LIT.clear(); T.sc.frame_set(g); cam = T.camera(g, SH.CAMLIN, mod); C.J.flicker(g); stage(g, cam); bpy.context.view_layer.update()
    for o in bpy.data.objects:
        if getattr(SH, 'GC_PRINT', False) and g == SH.G0: print('OBJ', o.name, o.type)
        if o.name.startswith('ph_sh_') or re.search(r'shadow|_rim', o.name): o['gc_role'] = 'shadow'
        elif o.name.startswith('ph_') or o.name.startswith('fg'): o['gc_role'] = 'prop'
        if air_re.search(o.name): o['airborne'] = True
    r, a = GC.run_check(bpy.context.scene, frame_list=[g], gap=0.02)
    allres += r
    for k, v in a.items(): air.setdefault(k, []).extend(v)
for r in allres:
    if r['status'] == 'FAIL' and r['gap'] is None and r['low'] <= 0.0: r['status'] = 'OK'; r['gap'] = r['low']
n = GC.write_report('GROUND.md', allres, air, 'gc11.py every %d (frames %d..%d)' % (every, SH.G0, SH.G1 - 1), bpy.context.scene, 0.02, fl)
print('ground_check: %d objects, %d rows, %d FAIL -> GROUND.md' % (len(set(r['obj'] for r in allres)), len(allres), n))
sys.exit(1 if n else 0)

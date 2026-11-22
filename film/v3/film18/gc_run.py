#!/usr/bin/env python3
"""gc_run.py -- run tools/ground_check.py on a film-18 take (v2).  usage (from the take folder): python3 ../gc_run.py [every]
Builds the take's scene with its shot.py make_driver('preview'), then for every sampled frame g: drive(g) (our cards are placed per frame, not keyed) and checks that frame.
Cards (c18_* quads) are tagged gc_role = "prop" (bbox contacts: the quad's bottom edge is under the soles), their contact-shadow quads gc_role = "shadow";
objects with ob['airborne'] = True or shot-level GC_AIRBORNE (regex) are skipped.  Exit code 1 on any FAIL.  Writes GROUND.md."""
import os, sys, re, runpy
HERE = os.getcwd(); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
every = int(sys.argv[1]) if len(sys.argv) > 1 else 5
import shot as SH, c18 as C
import ground_check as GC
bpy = C.bpy
drive, actors = SH.make_driver('preview')
air_re = re.compile(getattr(SH, 'GC_AIRBORNE', r'^$'))
G0, G1 = SH.G0, SH.G1
fl = list(range(G0, G1, every)) + [G1 - 1]
allres, air = [], {}
def tag():
    for o in bpy.data.objects:
        if o.name.startswith('c18_sh_') or o.name.endswith('_rim') or '_rim' in o.name: o['gc_role'] = 'shadow'
        elif o.name.startswith('c18_'): o['gc_role'] = 'prop'
        if air_re.search(o.name): o['airborne'] = True
for g in fl:
    drive(g); tag(); bpy.context.view_layer.update()
    r, a = GC.run_check(bpy.context.scene, frame_list=[g], gap=0.02)
    allres += r
    for k, v in a.items(): air.setdefault(k, []).extend(v)
n = GC.write_report('GROUND.md', allres, air, 'gc_run.py every %d (frames %d..%d)' % (every, G0, G1 - 1), bpy.context.scene, 0.02, fl)
print('ground_check: %d objects, %d rows, %d FAIL -> GROUND.md' % (len(set(r['obj'] for r in allres)), len(allres), n))
sys.exit(1 if n else 0)

#!/usr/bin/env python3
"""add a 'gcheck' mode to a take's c18.py: python3 shot.py gcheck g0 g1 [step]  -> GROUND.md (v3/tools/ground_check.py on the real per-frame scene)."""
import sys, re
p = sys.argv[1] + '/c18.py'; t = open(p).read()
if 'GCHECK' in t: sys.exit(0)
a = next(x for x in ("        if mode == 'measure':\n", "        w, c = T.render(path)") if x in t)
b = """        if mode == 'gcheck':
            import importlib.util
            if 'GCMOD' not in globals():
                sp = importlib.util.spec_from_file_location('ground_check', os.path.join(HERE, '..', '..', 'tools', 'ground_check.py')); GCMOD = importlib.util.module_from_spec(sp); sp.loader.exec_module(GCMOD); globals()['GCMOD'] = GCMOD; globals()['GCHECK'] = ([], {}, [])
            if (g - a) % int(os.environ.get('GSTEP', '5')) == 0:
                bpy.context.scene.frame_set(bpy.context.scene.frame_current)
                rs, air = GCMOD.run_check(frame_list=[bpy.context.scene.frame_current], gap=0.05, include=os.environ.get('GCINC', r'(ph_|prop|pot|jar|bowl|reed|bundle)'), skip=os.environ.get('GCSKIP', r'(spk|flame|puff|pf\d|glow|pool|shadow|tfl|spark|hole)'))
                for r in rs: r['frame'] = g
                GCHECK[0].extend(rs); GCHECK[2].append(g)
                for k_, v_ in air.items(): GCHECK[1].setdefault(k_, []).extend([g])
            continue
"""
t = t.replace(a, b + a, 1)
c = next(x for x in ("    if LEADM:\n", "    if REPORT:\n", "    if tt: print('mean s/frame") if x in t)
d = """    if mode == 'gcheck' and 'GCHECK' in globals():
        rs, air, fl = GCHECK
        GCMOD.write_report(os.path.join(HERE, 'GROUND.md'), rs, air, 'python3 shot.py gcheck %d %d' % (a, b), bpy.context.scene, 0.05, fl)
        nf = len([r for r in rs if r['status'] == 'FAIL']); print('GROUND: rows %d FAIL %d' % (len(rs), nf)); sys.exit(1 if nf else 0)
"""
assert c in t; t = t.replace(c, d + c, 1)
open(p, 'w').write(t + "\n# GCHECK patched\n")

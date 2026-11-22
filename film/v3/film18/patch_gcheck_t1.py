#!/usr/bin/env python3
"""gcheck for render team 1's c18 (run(shot, actors_fn, ...)): GCHECK=1 [GSTEP=10] python3 shot.py draft  -> GROUND.md, exit 1 on FAIL."""
import sys
p = sys.argv[1] + '/c18.py'; t = open(p).read()
if 'GCHECK1' in t: sys.exit(0)
a = "    cam = sc.camera; log = []\n"
assert a in t
b = a + """    if os.environ.get('GCHECK') == '1':                                   # GCHECK1: v3/tools/ground_check.py on the real per-frame scene
        import importlib.util
        sp_ = importlib.util.spec_from_file_location('ground_check', os.path.join(HERE, '..', '..', 'tools', 'ground_check.py')); GC = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(GC)
        res, airs, fl = [], {}, []
        for f in frames[::int(os.environ.get('GSTEP', '10'))]:
            sc.frame_set(f); bpy.context.view_layer.update(); R2.clear_placeholders(); R2.LIT.clear(); actors_fn(f, cam.matrix_world.translation.copy(), ctx); bpy.context.view_layer.update()
            rs, air = GC.run_check(sc, frame_list=[f], gap=0.05, include=os.environ.get('GCINC', r'(ph_|prop|pot|jar|bowl|reed|bundle|basket|rope|hay)'), skip=os.environ.get('GCSKIP', r'(spk|flame|puff|pf\\d|glow|pool|shadow|tfl|spark|hole|ph_sh_|_sh_)'))
            for r in rs: r['frame'] = f
            res.extend(rs); fl.append(f)
            for k_, v_ in air.items(): airs.setdefault(k_, []).append(f)
        GC.write_report(os.path.join(HERE, 'GROUND.md'), res, airs, 'GCHECK=1 python3 shot.py draft (frames %d-%d step %s)' % (frames[0], frames[-1], os.environ.get('GSTEP', '10')), sc, 0.05, fl)
        nf = len([r for r in res if r['status'] == 'FAIL']); print('GROUND: rows %d FAIL %d' % (len(res), nf)); sys.exit(1 if nf else 0)
"""
open(p, 'w').write(t.replace(a, b, 1) + "\n# GCHECK1 patched\n")

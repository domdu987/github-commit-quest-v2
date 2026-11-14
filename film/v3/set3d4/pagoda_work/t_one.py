import sys, os, time; sys.path.insert(0, sys.argv[1]); import pagoda as G, bpy
pr = sys.argv[2]; cams = sys.argv[3].split(',')
t=time.time(); A = G.build(pr); print('build %.1f s' % (time.time()-t)); sc = bpy.context.scene; G.setup_render(sc, 'preview')
out = os.path.join(G.WORK, 'dbg'); os.makedirs(out, exist_ok=True)
for nm in cams:
    G.apply_cam_state(nm, pr); cs = A['cams'][nm]; G.make_camera(cs); G.stage_placeholders(A, G.STAGING[nm], cs['loc'])
    w, c = G.render(os.path.join(out, '%s_%s.png' % (pr, nm))); print(nm, '%.1f wall %.1f cpu' % (w, c), flush=True)

import sys, time, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c21; from c21 import K, bpy, np
t0 = time.time()
P = dict(K.PRESETS['camp_bank']); P.update(farms=True, heather_n=900, gorse_n=200, crag_n=140, pine_n=60, bridge_pairs=None)
K.PRESETS['reveal'] = P
A = K.build('reveal')
print('build', time.time() - t0, flush=True)
P['fg'](A, P); P['camp_fg'](A, P)
captured = []
orig_stage = K.stage_crowd; orig_wall = K.spear_wall
K.stage_crowd = lambda items, cam=None, seg=10, shadow=True: captured.extend(items)
K.spear_wall = lambda n, ranks, rs, y0=27.0, half=9.0: orig_wall(20, 5, rs, y0=26.5, half=12.5)
K.crowd_loop(A, P)
K.stage_crowd = orig_stage
print('crowd items', len(captured), time.time() - t0, flush=True)
cam = bpy.context.scene.camera
which = sys.argv[1]
if which == 'start': c21.set_cam(cam, (-72, -133, 229), (12, 36, 0), 21.0); K.STATE['vivid'] = (1.07, 1.53)
else: c21.set_cam(cam, P['cam'], P['look'], 26.0); K.STATE['vivid'] = (1.52, 1.3)
for o in orig_stage(captured, cam=cam): o.name = 'crowdx_' + o.name
K.setup_render(bpy.context.scene, 'draft')
print('render', K.render('/tmp/claude-0/-home-user-github-commit-quest-v2/413571a1-78c2-535a-87b7-3e5a904f38f5/scratchpad/t_%s.png' % which, 'draft'), flush=True)

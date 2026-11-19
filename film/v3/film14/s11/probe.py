import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shot as S
from shot import C, F, bpy
stage = int(sys.argv[1]); light = sys.argv[2]; out = sys.argv[3]; cams = json.loads(sys.argv[4])
F.CAMS['fence_ring'] = dict(loc=cams[0][0], look=cams[0][1], lens=cams[0][2]); F.PRESETS['fence_ring'] = dict(light=light, state='fs%d' % stage, wire_r=float(os.environ.get('WR','0.085')), staging=[])
F.build('fence_ring', light, dress=False); S.sharp_ground(); S.matte_wire() if False else None; cam = F.make_camera(F.CAMS['fence_ring'])
import numpy as np
path=[(c[0][0],c[0][1]) for c in cams]
path2=[]
for c in cams:
    a=np.array(c[0][:2]);b=np.array(c[1][:2])
    for t in np.linspace(0,0.7,8): path2.append(tuple(a+(b-a)*t))
print('cut',C.cut_near(('props','grass','flowers','pebbles','edge'),path2,float(os.environ.get('CR','3.0'))))
print('huts',C.cut_region('props',[(12.6,30,-9,12,5.0)]))
F.setup_render(bpy.context.scene, 'preview'); os.makedirs(out, exist_ok=True)
for i, (loc, look, lens) in enumerate(cams):
    C.set_cam(cam, loc, look, lens); F.set_fence_stage(stage); F.set_wire_push(-1); bpy.context.view_layer.update(); F.set_bees(-1)
    if stage == 3: S.matte_wire()
    print(F.render(os.path.join(out, 'p%d.png' % i)))

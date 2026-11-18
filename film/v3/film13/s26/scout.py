import sys, os, json
import c13 as C
B = C.B; bpy = C.bpy
T = B.T
S = cast = C.cast13.STORY13
def P(k): return dict(S[k][1])
T.PH.update(
  worker=('worker13_a', dict(P('worker_stand_a')), 3.2), foreman=('foreman13', dict(P('foreman_stand')), 3.3),
  rich=('rich', dict(P('rich_look_window_smug')), 3.4), maid=('town_b', dict(P('town_stand_b')), 3.0),
  clerk=('worker13_b', dict(P('worker_stand_b')), 3.2), kid=('town_c', dict(P('town_stand_c')), 2.5),
  towns_m=('town_a', dict(P('town_stand_a')), 3.2), towns_f=('town_b', dict(P('town_stand_b')), 3.0), towns_o=('worker13_c', dict(P('worker_stand_c')), 3.1))
cams = json.loads(sys.argv[1]); out = sys.argv[2]
scene = bpy.context.scene
A = B.build('front_stair', light='MORNING', state='lift1,fill0.15')
B.setup_render(scene, 'preview')
scene.render.resolution_percentage = 100
print({k: B.stand(k) for k in ['door','stair_top','stair_foot','mud_fall','sit_mud','pay_a']})
for name, (loc, look, lens) in cams.items():
    cam = B.make_camera(dict(loc=loc, look_at=look, lens=lens), name='cam_'+name)
    scene.camera = cam
    B.T.render(os.path.join(out, name + '.png'))
    bpy.data.objects.remove(cam, do_unlink=True)

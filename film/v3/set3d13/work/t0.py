import sys,time
sys.path.insert(0,'/home/user/github-commit-quest-v2/film/v3/set3d10')
import harbour as H, bpy
t=time.time()
A=H.build('harbour','quay_low',light='DAY'); print('build',time.time()-t)
sc=bpy.context.scene; H.setup_render(sc,'preview'); cam=H.make_camera(A['cam'])
print(H.T.render('/tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/t0.png'))

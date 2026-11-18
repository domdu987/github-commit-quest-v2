import sys,os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c13 as C, dressU as U, bpy
SP='/tmp/claude-0/-home-user-github-commit-quest-v2/a9e88cf6-7078-553d-b52f-0665340a811c/scratchpad/'
T=C.Take('under_rows','preview'); U.dark_surround(True); U.close_hall()
C.S.setup_render(T.scene,'preview'); T.scene.render.resolution_percentage=50; T.scene.cycles.filter_width=2.0
for i,(n,loc,look,lens) in enumerate([(10,(6.5,-3.0,5.2),(6.5,30,2.8),22),(1000,(6.5,-3.2,7.5),(6.5,36,2.0),22),(5000,(6.5,-3.4,10.5),(6.5,44,0.8),22)]):
    cam=C.S.make_camera(dict(loc=loc,look_at=look,lens=lens)); T.scene.camera=cam
    C.S.set_jack_count(n); C.S.T.render(SP+'t15_%d.png'%i)

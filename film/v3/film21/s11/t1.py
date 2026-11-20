import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shot import *
T = c21.Take('riverbank'); T.workdir = '/tmp/claude-0/s11/w1'; os.makedirs(T.workdir, exist_ok=True)
A = T.A
cam = T.cam
loc = Vector(cam.location); look = Vector(T.pr['look'])
look2 = aim_pitch(loc, look, -4.5)
T.key_cam(1, loc, look2)
names = [('e1', 'footman_a', 'footman_a_stand'), ('e2', 'footman_b', 'footman_b_jump_pinch_nose'), ('e3', 'knight_a_open', 'knight_a_open_worried'), ('e4', 'knight_b', 'knight_b_stand')]
for (nm, (x, y, z, fz, who)), (n2, cast, pn) in zip(A['marks'].items(), names):
    a = T.add(n2, cast)
    a.place(1, (x, y, z), scale=wscale(cast))
    T.scene.frame_set(1)
    a.pose(1, pose_of(pn), camera=cam)
T.sprites_for(256)
for n2 in T.actors: print(n2, T.head_px(T.actors[n2], 1))
K.set_flow(1.0)
for i in range(3): K.splash(0,0,-1,name=str(i))
T.render([0], '/tmp/claude-0/s11/o1', lambda g: None, samples=12, draft=True)

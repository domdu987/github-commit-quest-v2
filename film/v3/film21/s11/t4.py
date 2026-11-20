import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shot import *
T = c21.Take('riverbank'); T.workdir = '/tmp/claude-0/s11/w4'; os.makedirs(T.workdir, exist_ok=True)
cam = T.cam; loc = Vector(cam.location); look2 = aim_pitch(loc, Vector(T.pr['look']), -4.5)
T.key_cam(1, loc, look2)
spec = [('a', 'footman_a', 'footman_a_stand', dict(yaw=-0.9), False, 3.4, 90), ('b', 'footman_a', 'footman_a_stand', dict(yaw=0.9), False, 3.4, 330), ('c', 'footman_a', 'footman_a_stand', dict(yaw=0.3), True, 5.4, 110), ('d', 'footman_a', 'footman_a_stand', dict(yaw=0.3), False, 5.4, 330), ('e', 'knight_a_open', 'knight_a_open_stand', dict(yaw=-0.9), False, 7.5, 560)]
for n, cast, pn, kw, flip, d, xp in spec:
    a = T.add(n, cast); x, y = K.at_px(T.pr, d, xp)
    a.place(1, (x, y, float(K.ground(x, y))), scale=wscale(cast), flip=flip); T.scene.frame_set(1)
    a.pose(1, pose_of(pn, **kw), camera=cam)
T.sprites_for(128)
K.set_flow(1.0)
for i in range(3): K.splash(0,0,-1,name=str(i))
T.render([0], '/tmp/claude-0/s11/o4', lambda g: None, samples=12, draft=True)

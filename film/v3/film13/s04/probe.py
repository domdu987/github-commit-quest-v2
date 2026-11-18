import sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c13 as C
B = C.B
t0=time.time()
T = C.Take('street_wide', light='RAIN', state='lift0,fill1,rain1')
print('build', time.time()-t0)
A = T.A
print(A['cam'])
cam=A['cam']
T.scene.camera = T.cam
T.key_cam(1, cam['loc'], cam['look_at'], lens=cam.get('lens',22))
T.render([1], 'work', scale=0.5, samples=6)
print('t', time.time()-t0)

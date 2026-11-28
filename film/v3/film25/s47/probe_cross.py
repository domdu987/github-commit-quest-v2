import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c25 as C
F = C.F
import numpy as np
F.OVR.update(haze=0.0006)
A = C.W.build('cross_hero')
import tank25 as TK
H = F.S['tank']
for u in np.linspace(0, 1, 41):
    p = TK.crossing_pose(H, u)
    print("u %.3f s %.2f z %.2f pitch %.1f phi %.1f" % (u, p['s'], p['pos'][2], p['pitch'], p['phi']))

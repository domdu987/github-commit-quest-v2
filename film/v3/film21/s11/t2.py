import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shot import *
T = c21.Take('riverbank')
cam = T.cam; loc = tuple(cam.location); look = T.pr['look']
print('cam', loc, 'look', look)
print('rows = dist 2..16 step 2 (top=far); cols = lat -8..+12 step 2 ; value sd (neg=water) / ground z')
for d in range(16, 1, -2):
    row = []
    for lat in range(-8, 14, 2):
        x, y = K.rel_xy(loc, look, d, lat); row.append('%5.1f' % K.sd_at(x, y))
    print('d%2d' % d, ' '.join(row))
for d in (3, 6, 9):
    print([round(float(K.ground(*K.rel_xy(loc, look, d, lat))),2) for lat in (-4, 0, 4, 8)])

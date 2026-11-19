import sys, os; sys.path.insert(0, '..'); import wall as W, bpy
mode = sys.argv[1]
A = W.build('wall_site', 'two_sections', light=sys.argv[2]); W.make_camera(A['cam'])
if mode == 'rain': W.set_rain(1.0)
if mode == 'norain': W.set_rain(0.0)
if mode == 'nopuddle':
    pass
w, c = W.render('/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/w9/t_%s.png' % mode)
print('COST', mode, sys.argv[2], round(w, 1), round(c, 1))

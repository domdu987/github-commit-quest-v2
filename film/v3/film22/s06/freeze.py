import sys, os; sys.argv=['x']
import shot as S, c22 as C
T = S.make('preview')
def fr(g, T_): S.actors(800, T_) if False else None
orig = S.actors
def a2(g, T_):
    # same pose as g=800 but camera of g: temporarily lie about t via g
    orig(800, T_)
T.path_orig = T.path
out = 'freeze'; os.makedirs(out, exist_ok=True)
for g in range(750, 831):
    T.clear(); T.ob = []; T.set_cam(g); orig(800, T); T.animate(800, T) if False else None
    from c22 import TW
    TW.render('%s/g_%04d.png' % (out, g), T.sc)

import sys, os, json
sys.argv=['x']; import shot as S
from shot import *
CAMS = json.loads(open(os.environ.get('CAMS','cams20.json')).read())
g = int(os.environ.get('G', 1307)); shot = int(os.environ.get('SHOT', 20))
d = Driver(shot, 'preview', 2)
os.makedirs('tst', exist_ok=True)
for name, (loc, look, lens) in CAMS.items():
    S.cam_of = lambda gg, a=(tuple(loc), tuple(look), lens): a
    d.frame(g, 'tst/%s.png' % name); print('done', name, flush=True)

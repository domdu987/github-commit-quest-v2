import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = [sys.argv[0], "x", "21"]
import shot as S
C = S.C; D = S.D
T = S.Take("preview")
# dense field workers from crowd_view
cam = T.cam
T.key_cam(1, (4, 0, 14), (8, 20, 1.0), lens=28)
T.scene.camera = T.cam; T.scene.frame_set(1)
pngs, boxes = S.worker_variants("abc")
import random
r = random.Random(3)
pts = []
for i in range(400):
    x, y = r.uniform(-8, 18), r.uniform(5, 40)
    if all((x-a)**2+(y-b)**2 > 1.3**2 for a, b in pts) and D._visible(cam, x, y, 0.0, 3.0): pts.append((x, y))
print(len(pts))
cs = []
for (x, y) in pts:
    k = r.randrange(3)
    cs.append((T.cards.add("w%d" % len(cs), [pngs[2*k], pngs[2*k+1]], boxes[2*k], (x - 1.29 * 0.0, y), 0.0), x, y))
os.makedirs("work/p", exist_ok=True)
st = C.Take.render(T, [1], "work/p", scale=0.75, samples=6)[0]
os.replace(st['path'], "work/p/dense_probe.png")

import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C, jimo_shots as S
SHOT = 's07'; G0, G1, HB, HA = 531, 597, 0, 9
SNAP_G = 551                                           # "พันกว่าตัว" 18.26 s
# upright, PLAIN oxen (no coats, no blades); the yard FILLS UP before the snap: each ox appears at its own frame (g 531 -> 549)
HERD = S.herd(150, (-30, 16.0), (30, 16.0), 22.0, 7, yaw=200.0) + S.herd(60, (-30, 36.0), (30, 36.0), 6.0, 17, yaw=200.0) + S.herd(54, (-30, 41.0), (30, 41.0), 3.5, 23, yaw=200.0) + S.herd(36, (-30, 43.5), (30, 43.5), 3.0, 29, yaw=200.0)
rr = random.Random(3); APPEAR = [G0 + int(rr.uniform(-6, 20)) if i % 3 else G0 - 1 for i in range(len(HERD))]
t0 = (SNAP_G - G0) / (G1 - 1 - G0)
# starts tight on the near yard, slow push; a real x1.6 snap pull-out over 5 frames at g 551-556, then a slow hold-pull
CAM = C.cam_path(((0.0, 37.0, 8.0), (0.0, 18.0, 1.0), 24), ((0.0, 42.0, 10.0), (0.0, 27.0, 0.9), 24), punches=[(t0, 5 / (G1 - 1 - G0), -0.375, 0.62)])
def tweak(stage, A=None):
    if stage == 'pre':
        S.SHOTS[SHOT]['sun'] = 140.0
    elif stage == 'post':
        C.hide('digtools', 'baskets', 'pens', 'props', 'hay')
def actors(f, cam, ctx):
    t = (f - G0) / 30.0
    for n, (x, y, z, yaw, sc) in enumerate(HERD):
        if f < APPEAR[n]: continue
        ph = int((f * 0.25 + n * 3) % 8)
        C.ox_card(SHOT, n, (x - 0.6 * t, y, 0), 200, sc, cam, state='plain', view='three_quarter', gait='walk', phase=ph, blades=False, theta=26, shadow=(n % 5 == 0),
                  bob=0.04 * abs(math.sin(2 * math.pi * (f * 0.25 + n) / 8)))
if __name__ == '__main__':
    C.run(SHOT, actors, G0, G1, HB, HA, quality=sys.argv[1] if len(sys.argv) > 1 else None, tweak=tweak, shk=0.004, cam_fn=CAM)

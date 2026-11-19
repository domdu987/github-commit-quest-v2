import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C, jimo_shots as S
SHOT = 's02'; G0, G1, HB, HA = 78, 156, 0, 10
HERD = S.herd(66, (-22, 7.6), (4, 7.6), 7.0, 11, yaw=180.0)
# ONE smooth pull-out while the camera rises from 1.3 D to ~2.1 D (rows stack up the frame); no pulses
CAM = C.cam_path(((-30.0, 11.4, 1.3), (8.0, 10.0, 1.5), 20), ((-35.0, 10.8, 3.6), (2.0, 8.4, 0.3), 20), punches=[(0.3, 0.08, -0.14)], slide=1.0)
def tweak(stage, A=None):
    if stage == 'pre':
        import jimo_shots as S2, jimo_r2 as R2
        S2.SHOTS[SHOT]['fg'] = None; R2.POST.pop('s02', None); R2.SKIP['s02'] = [(-34.0, 8.5, 6.5), (-27.0, 8.5, 3.0)]
    elif stage == 'post':
        C.hide('baskets', 'props', 'digtools', 'straw')
def actors(f, cam, ctx):
    t = (f - G0) / 30.0
    C.person_card('tiandan', 'tiandan_tie_blade', (-26.0, 12.5, 0), cam, 0, bob=C.hop(f, 0, 0.04, 2.0), roll=2.5 * math.sin(2 * math.pi * 1.5 * t), mods=dict(gaze=(0.8, -0.4), yaw=0.5))
    C.ox_card(SHOT, 0, (-23.6, 11.6, 0), 180, 1.0, cam, view='front_three_quarter', gait='stand', bob=C.hop(f, 1, 0.03, 0.8), roll=C.sway(f, 1, 1.6, 0.9))
    # dark, lit carriers in the lower third (cast props: baskets of earth), walking with the herd
    C.person_card('townsfolk', 'old_man_carry_basket', (-19.0, 4.8, 0), cam, 7, bob=0.05 * abs(math.sin(2 * math.pi * 1.6 * t)), roll=C.sway(f, 7, 2, 1.0))
    C.person_card('townsfolk', 'woman_carry_basket', (-22.0, 12.6, 0), cam, 8, bob=0.05 * abs(math.sin(2 * math.pi * 1.7 * t + 1)), roll=C.sway(f, 8, 2, 1.0))
    for i, m in enumerate(HERD):
        x, y, z, yaw, sc = m
        xx = x - 1.8 * t
        near = math.hypot(x + 31, y - 11.4) < 24
        ph = int((f * 0.42 + i * 3) % 8)
        C.ox_card(SHOT, i + 1, (xx, y, 0), 180, sc, cam, view='front_three_quarter' if near else 'three_quarter', gait='walk', shadow=(i % 4 == 0), phase=ph, bob=0.04 * abs(math.sin(2 * math.pi * (f * 0.42 + i) / 8)))
if __name__ == '__main__':
    C.run(SHOT, actors, G0, G1, HB, HA, quality=sys.argv[1] if len(sys.argv) > 1 else None, tweak=tweak, shk=0.011, cam_fn=CAM)

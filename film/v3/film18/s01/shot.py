import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C
from mathutils import Vector as V
SHOT = 's01'; G0, G1, HB, HA = 0, 78, 0, 0
ROW = [(x, 7.4 + 0.5 * (k % 2)) for k, x in enumerate((-15.0, -9.5, -4.0, 1.5, 7.0, 12.5))]
# eased push 4 %/s + a slow slide + TWO HELD punch-ins (g 8 and g 50, +17 %), no pulses
CAM = C.cam_path(((-9.4, 20.3, 2.3), (-2.4, 12.8, 2.7), 24), ((-8.9, 19.6, 2.3), (-2.4, 12.8, 2.7), 24), punches=[(8 / 77.0, 5 / 77.0, 0.17), (50 / 77.0, 5 / 77.0, 0.17)], slide=-0.7)
def tweak(stage, A=None):
    if stage == 'pre':
        import jimo_shots as S
        S.SHOTS[SHOT]['fg'] = None
    elif stage == 'post':
        C.hide('baskets', 'props', 'digtools')                                   # unlit navy pick / basket placeholders beside the lane
    elif stage == 'cam':
        C.warm_lantern(A)
def actors(f, cam, ctx):
    t = f / 30.0
    pull = math.sin(2 * math.pi * 1.6 * t)
    # Tian Dan beside the ox, the silk running from his fist over the ox's spine; he looks at the ox (head turned, pupils to the ox)
    C.person_card('tiandan', 'tiandan_tug_cloth', (-3.4 + 0.15 * pull, 16.0, 0), cam, 0, bob=C.hop(f, 0, 0.04, 1.6), roll=2.5 * pull, sz=1 + 0.012 * pull, mods=dict(gaze=(0.9, 0.2), yaw=0.55))
    C.ox_card(SHOT, 0, (-0.9 + 0.05 * pull, 15.4, 0), 165, 1.0, cam, gait='stand', coat=0.55 + 0.45 * min(1.0, max(0.0, (f - 4) / 62.0)), bob=C.hop(f, 1, 0.03, 0.8), roll=C.sway(f, 1, 1.6, 0.9))
    for i, (x, y) in enumerate(ROW):
        C.ox_card(SHOT, i + 1, (x, y, 0), 180, 1.0, cam, gait='stand', bob=C.hop(f, i, 0.03, 0.6), roll=C.sway(f, i + 3, 1.8, 0.55))
    for i, (x, y) in enumerate(((-8.5, 14.6), (3.5, 16.8), (6.5, 13.4))):      # more dressed oxen in the yard (hook density)
        C.ox_card(SHOT, 20 + i, (x, y, 0), 170 + 20 * i, 1.0, cam, gait='stand', bob=C.hop(f, i + 7, 0.03, 0.7), roll=C.sway(f, i + 9, 1.6, 0.6))
if __name__ == '__main__':
    C.run(SHOT, actors, G0, G1, HB, HA, quality=sys.argv[1] if len(sys.argv) > 1 else None, tweak=tweak, shk=0.004, cam_fn=CAM)

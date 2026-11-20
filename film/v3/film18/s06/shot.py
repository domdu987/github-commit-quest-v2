import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C, jimo_shots as S
SHOT = 's06'; G0, G1, HB, HA = 459, 531, 0, 0
HERD = S.herd(10, (62, 15.4), (82, 17.2), 4.5, 6, yaw=200.0)
# real eased push + a 3 D slide along the lane (follows the oxen), one held punch-in on "สิบตัว" (g 497, +15 %)
CAM = C.cam_path(((83.0, 9.5, 2.5), (71.0, 21.0, 1.6), 22), ((78.0, 13.2, 2.3), (67.5, 22.0, 1.4), 22), punches=[(38 / 71.0, 5 / 71.0, 0.15)], slide=-2.4)
def tweak(stage, A=None):
    if stage == 'pre':
        S.SHOTS[SHOT]['fg'] = None
    elif stage == 'post':
        C.hide('baskets', 'digtools', 'props')
def actors(f, cam, ctx):
    t = (f - G0) / 30.0
    # Tian Dan leads along the lane, head turned toward the oxen / the gates
    C.person_card('tiandan', 'tiandan_walk', (76.5 - 1.6 * t, 12.4 + 0.5 * t, 0), cam, 0, bob=0.05 * abs(math.sin(2 * math.pi * 2.0 * t)), roll=C.sway(f, 0, 2, 1.0), mods=dict(yaw=0.45, gaze=(0.8, 0.1)))
    # townsfolk lead the oxen out of the house gates (x 58 / 74 / 86 at y 23), ropes implied by the line of walking oxen
    for i, (x, y, pose) in enumerate(((60.5, 21.8, 'woman_stand'), (72.0, 22.0, 'old_man_stand'), (84.5, 21.6, 'woman_stand'))):
        C.person_card('townsfolk', pose, (x - 1.2 * t, y - 0.6 * t, 0), cam, i + 1, bob=C.hop(f, i, 0.03, 1.2), roll=C.sway(f, i, 2.5, 0.8))
    # dark, lit foreground carriers in the lower third
    C.person_card('townsfolk', 'woman_carry_basket', (72.0 - 0.4 * t, 14.2, 0), cam, 8, bob=0.05 * abs(math.sin(2 * math.pi * 1.6 * t)), roll=C.sway(f, 8, 2, 1.0))
    C.person_card('child', 'child_carry_basket', (73.9 - 0.4 * t, 13.6, 0), cam, 9, bob=0.06 * abs(math.sin(2 * math.pi * 2.0 * t + 1)), roll=C.sway(f, 9, 2, 1.0))
    C.person_card('child', 'child_carry_basket', (81.0, 12.6, 0), cam, 10, h=1.9, bob=0.05 * abs(math.sin(2 * math.pi * 1.8 * t)), roll=C.sway(f, 10, 2, 1.0))
    C.person_card('townsfolk', 'old_man_carry_basket', (79.6, 14.8, 0), cam, 11, bob=0.05 * abs(math.sin(2 * math.pi * 1.5 * t)), roll=C.sway(f, 11, 2, 0.9))
    for i, (x, y, z, yaw, sc) in enumerate(HERD):
        xx = x - 1.8 * t
        ph = int((f * 0.30 + i * 3) % 8)
        C.ox_card(SHOT, i, (xx, y, 0), 200, sc, cam, state='plain', view='front_three_quarter' if math.hypot(x - 80, y - 10) < 14 else 'three_quarter', gait='walk', phase=ph, blades=False, bob=0.04 * abs(math.sin(2 * math.pi * (f * 0.30 + i) / 8)))
if __name__ == '__main__':
    C.run(SHOT, actors, G0, G1, HB, HA, quality=sys.argv[1] if len(sys.argv) > 1 else None, tweak=tweak, shk=0.016, cam_fn=CAM)

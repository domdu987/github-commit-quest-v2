import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C, jimo_shots as S
C.hop = (lambda _h: (lambda f, i, amp=0.06, hz=3.0: _h(f, i, min(amp, 0.018), min(hz, 1.5))))(C.hop)      # V2: bounce <= 0.02 D at <= 1.5 Hz
C.sway = (lambda _s: (lambda f, i, amp=1.5, hz=0.7: _s(f, i, min(amp, 1.5), min(hz, 0.8))))(C.sway)
from mathutils import Vector as V
SHOT = 's06'; G0, G1, HB, HA = 459, 531, 0, 0
HERD = S.herd(10, (62, 15.4), (82, 17.2), 4.5, 6, yaw=200.0)
# real eased push + a 3 D slide along the lane (follows the oxen), one held punch-in on "สิบตัว" (g 497, +15 %)
CAM = C.cam_path(((83.0, 9.5, 2.5), (71.0, 21.0, 2.5), 22), ((77.0, 13.8, 2.3), (67.5, 22.0, 2.3), 22), punches=[(38 / 71.0, 14 / 71.0, 0.10)], slide=-7.5)
LAT = -0.55
def tweak(stage, A=None):
    if stage == 'pre':
        S.SHOTS[SHOT]['fg'] = None
    elif stage == 'post':
        C.hide('baskets', 'digtools', 'props')
        import jimo_r2 as R2
        R2.dress(69.0, 79.0, 10.4, 14.4, 12, 6, kinds=('basket', 'pot', 'rope', 'hay', 'basket', 'silk'))
def actors(f, cam, ctx):
    t = (f - G0) / 30.0
    # Tian Dan leads along the lane, head turned toward the oxen / the gates
    # keep Tian Dan locked in the camera frame (cap and body fully inside the left edge): fixed distance / lateral offset from the keyed camera, plus his walk bounce
    loc_, look_, _ = CAM((f - G0) / float(G1 - 1 - G0)); fw_ = look_ - loc_; fw_.z = 0; fw_.normalize(); rt_ = V((fw_.y, -fw_.x, 0.0))
    ptd = loc_ + fw_ * 5.2 - rt_ * LAT
    C.person_card('tiandan', 'tiandan_walk', (ptd.x, ptd.y, 0), cam, 0, bob=0.018 * abs(math.sin(2 * math.pi * 1.5 * t)), roll=C.sway(f, 0, 2, 1.0), mods=dict(yaw=0.45, gaze=(0.8, 0.1)))
    # townsfolk lead the oxen out of the house gates (x 58 / 74 / 86 at y 23), ropes implied by the line of walking oxen
    for i, (x, y, pose) in enumerate(((60.5, 21.8, 'woman_stand'), (72.0, 22.0, 'old_man_stand'), (84.5, 21.6, 'woman_stand'))):
        C.person_card('townsfolk', pose, (x - 1.2 * t, y - 0.6 * t, 0), cam, i + 1, bob=C.hop(f, i, 0.03, 1.2), roll=C.sway(f, i, 2.5, 0.8))
    # dark, lit foreground carriers in the lower third
    C.person_card('townsfolk', 'woman_carry_basket', (loc_.x + fw_.x * 8.8 - rt_.x * 2.0, loc_.y + fw_.y * 8.8 - rt_.y * 2.0, 0), cam, 8, bob=0.018 * abs(math.sin(2 * math.pi * 1.5 * t)), roll=C.sway(f, 8, 2, 1.0))
    # carrier child locked to the camera, farther back and clear of the left edge / caption band (chin well above y 850)
    pch = loc_ + fw_ * 6.9 + rt_ * -1.5
    C.person_card('child', 'child_carry_basket', (pch.x, pch.y, 0), cam, 10, h=1.9, bob=0.018 * abs(math.sin(2 * math.pi * 1.5 * t)), roll=C.sway(f, 10, 2, 1.0))
    for i, (x, y, z, yaw, sc) in enumerate(HERD):
        xx = x - 1.8 * t
        ph = int((f * 0.30 + i * 3) % 8)
        C.ox_card(SHOT, i, (xx, y, 0), 200, sc, cam, state='plain', view='front_three_quarter' if math.hypot(x - 80, y - 10) < 14 else 'three_quarter', gait='walk', phase=ph, blades=False, bob=0.04 * abs(math.sin(2 * math.pi * (f * 0.30 + i) / 8)))
if __name__ == '__main__':
    C.run(SHOT, actors, G0, G1, HB, HA, quality=sys.argv[1] if len(sys.argv) > 1 else None, tweak=tweak, shk=0.0, cam_fn=CAM)

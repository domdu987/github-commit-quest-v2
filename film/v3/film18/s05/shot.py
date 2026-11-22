import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C, jimo_shots as S
C.hop = (lambda _h: (lambda f, i, amp=0.06, hz=3.0: _h(f, i, min(amp, 0.018), min(hz, 1.5))))(C.hop)      # V2: bounce <= 0.02 D at <= 1.5 Hz
C.sway = (lambda _s: (lambda f, i, amp=1.5, hz=0.7: _s(f, i, min(amp, 1.5), min(hz, 0.8))))(C.sway)
from mathutils import Vector as V
SHOT = 's05'; G0, G1, HB, HA = 384, 459, 8, 0
HAND_G = 414                                   # the sash changes hands
# real eased push (about 8 %/s) + a 1.3 D slide + ONE held punch-in (+15 %) on the hand-over
CAM = C.cam_path(((-68.6, 17.3, 2.6), (-75.0, 21.4, 0.4), 24), ((-70.3, 18.8, 2.5), (-74.7, 21.4, 0.6), 24), punches=[(0.45, 0.18, 0.10)], slide=-1.9)
def tweak(stage, A=None):
    if stage == 'pre':
        S.SHOTS[SHOT]['fg'] = None
    elif stage == 'cam':
        C.fg_rail(A, y=-1.9, z=-1.78, w=3.6)
    elif stage == 'post':
        C.hide('baskets', 'digtools', 'props'); print('sky', C.clear_sky())
        import jimo_r2 as R2
        R2.dress(-73.0, -66.0, 15.6, 19.4, 9, 5, kinds=('basket', 'pot', 'rope', 'hay', 'basket'))
        R2.dress(-76.0, -72.0, 17.0, 19.0, 4, 6, kinds=('basket', 'pot'))
def actors(f, cam, ctx):
    _h = C.bpy.data.objects.get('dg_hay_0003') if hasattr(C, 'bpy') else None
    if _h is not None: C.bpy.data.objects.remove(_h, do_unlink=True)          # V2: a dressing haystack with no ground under it (ground_check NO SURFACE)
    t = (f - G0) / 30.0; give = f < HAND_G
    sash = dict(arm_r={'hand': (0.62, 0.52), 'bend': 0.2, 'stretch': 1.1, 'layer': 'front'}, prop_r={'type': 'sash', 'scale': 1.0})
    # giver (old man) holds the sash out across the counter; Tian Dan reaches for it, then holds it
    C.person_card('townsfolk', 'old_man_stand', (-74.9, 19.9, 0), cam, 1, bob=C.hop(f, 1, 0.03, 1.2), roll=C.sway(f, 1, 2.5, 0.9) + (2.5 if give else 0), mods=(sash if give else None))
    if give: C.person_card('tiandan', 'tiandan_accept_sash', (-74.0, 21.9, 0), cam, 0, bob=C.hop(f, 0, 0.03, 1.4), roll=2.0 * math.sin(2 * math.pi * 0.9 * t), mods=dict(prop_r=None, arm_r={'hand': (0.66, 0.5), 'bend': 0.2, 'stretch': 1.1, 'layer': 'front'}, yaw=-0.55, gaze=(-0.9, 0.1), expr='neutral'))
    else: C.person_card('tiandan', 'tiandan_accept_sash', (-74.0, 21.9, 0), cam, 0, bob=C.hop(f, 0, 0.03, 1.4), roll=2.0 * math.sin(2 * math.pi * 0.9 * t), mods=dict(yaw=-0.3, gaze=(-0.6, 0.3)))
    C.person_card('townsfolk', 'woman_stand', (-75.0, 24.2, 0), cam, 2, bob=C.hop(f, 2, 0.03, 1.1), roll=C.sway(f, 2, 2.5, 0.8))
    C.person_card('child', 'child_stand', (-72.1, 24.5, 0), cam, 4, bob=C.hop(f, 4, 0.08, 2.4), roll=C.sway(f, 4, 3.0, 1.1))
    loc, look, _ = CAM((f - G0) / float(G1 - 1 - G0)); fw = look - loc; fw.z = 0; fw.normalize(); rt = V((fw.y, -fw.x, 0.0))
    p1 = loc + fw * 3.1 - rt * 1.0; p2 = loc + fw * 3.4 + rt * 1.75
    p3 = loc + fw * 3.9 + rt * 0.3; p4 = loc + fw * 4.2 + rt * 0.9
    C.person_card('townsfolk', 'old_man_carry_basket', (p3.x, p3.y, 0), cam, 7, h=1.2, bob=0.018 * abs(math.sin(2 * math.pi * 1.4 * t + 2)), roll=C.sway(f, 7, 2, 0.8))
    C.person_card('child', 'child_carry_basket', (p4.x, p4.y, 0), cam, 8, h=1.5, bob=0.018 * abs(math.sin(2 * math.pi * 1.5 * t)), roll=C.sway(f, 8, 2, 1.0), mirror=True)
    C.person_card('child', 'child_carry_basket', (p1.x, p1.y, 0), cam, 5, h=1.5, bob=0.018 * abs(math.sin(2 * math.pi * 1.5 * t)), roll=C.sway(f, 5, 2, 0.9))
    C.person_card('townsfolk', 'woman_carry_basket', (p2.x, p2.y, 0), cam, 6, h=1.6, bob=0.018 * abs(math.sin(2 * math.pi * 1.5 * t + 1)), roll=C.sway(f, 6, 2, 0.9), mirror=True)
if __name__ == '__main__':
    C.run(SHOT, actors, G0, G1, HB, HA, quality=sys.argv[1] if len(sys.argv) > 1 else None, tweak=tweak, shk=0.0, cam_fn=CAM, dress=5)

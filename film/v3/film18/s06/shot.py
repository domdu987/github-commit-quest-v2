import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C, jimo_shots as S
SHOT = 's06'; G0, G1, HB, HA = 459, 531, 0, 0
# QA-art R2 instr. 7: plain oxen, NO blades, looser double row (>= 8 readable), old man out from behind the centre ox
HERD = S.herd(10, (63, 17.8), (84, 19.8), 5.0, 6, yaw=225.0)
def tweak(stage, A=None):
    if stage == 'pre':
        S.SHOTS[SHOT]['move'].update(push=0.02, slide=-30); c = S.SHOTS[SHOT]['cam']; c['look_at'] = (c['look_at'][0], c['look_at'][1], 0.9); c['loc'] = (c['loc'][0], c['loc'][1], 2.2)
        S.SHOTS[SHOT]['move']['moves'] = [dict(t=0.10, d=0.74, dur=4), dict(t=0.24, d=1.3, dur=5), dict(t=0.40, d=0.76, dur=4), dict(t=0.54, d=1.28, dur=5), dict(t=0.70, d=0.8, dur=4), dict(t=0.84, d=1.2, dur=5)]
def actors(f, cam, ctx):
    t = (f - G0) / 30.0
    C.person_card('tiandan', 'tiandan_walk', (75.6 + 0.4 * t, 14.8 + 0.37 * t, 0), cam, 0, bob=0.05 * abs(math.sin(2 * math.pi * 2.0 * t)), roll=C.sway(f, 0, 2, 1.0), yaw_off=0)
    for i, (x, y) in enumerate(((58, 21.0), (74, 21.0), (86, 21.0))):
        C.person_card('townsfolk', ('woman_stand', 'old_man_stand', 'woman_stand')[i], (x - 0.8 * t, y + (0 if i != 1 else 1.0), 0), cam, i + 1, bob=C.hop(f, i, 0.03, 1.2), roll=C.sway(f, i, 2.5, 0.8))
    C.person_card('townsfolk', 'old_man_stand', (68.0, 10.4, 0), cam, 5, bob=C.hop(f, 5, 0.03, 1.0), roll=C.sway(f, 5, 2.0, 0.7))   # out in front of the herd
    for i, (x, y, z, yaw, sc) in enumerate(HERD):
        xx = x - 1.6 * t
        ph = int((f * 0.30 + i * 3) % 8)
        C.ox_card(SHOT, i, (xx, y, 0), 200, sc, cam, state='plain', view='front_three_quarter' if math.hypot(x - 84, y - 9) < 15 else 'three_quarter', gait='walk', phase=ph, blades=False,
                  bob=0.04 * abs(math.sin(2 * math.pi * (f * 0.30 + i) / 8)))
if __name__ == '__main__':
    C.run(SHOT, actors, G0, G1, HB, HA, quality=sys.argv[1] if len(sys.argv) > 1 else None, tweak=tweak, shk=0.02)

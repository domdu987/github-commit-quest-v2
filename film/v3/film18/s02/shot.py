import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C, jimo_shots as S
SHOT = 's02'; G0, G1, HB, HA = 78, 156, 0, 10
# QA-art R2 instr. 5: herd spread ~10 D wide and staggered (15+ readable at t=1), no stump prop, dark props in the bottom 30 %
HERD = S.herd(44, (-17, 8.6), (0, 8.6), 7.0, 11, yaw=180.0)
def tweak(stage, A=None):
    if stage == 'pre':
        import jimo_r2 as R2
        R2.POST.pop('s02', None)                         # the set's s02 'dress' (hay + sticks) is the pale stump: dropped
        c = S.SHOTS[SHOT]['cam']; c['look_at'] = (12.0, 10.5, 1.3); S.SHOTS[SHOT]['move'].update(slide=-40, push=-0.01)
        S.SHOTS[SHOT]['move']['moves'] = [dict(t=0.2, d=1.08, dur=5), dict(t=0.4, d=0.94, dur=5), dict(t=0.6, d=1.08, dur=5), dict(t=0.8, d=0.95, dur=5)]
    else:
        import jimo_r2 as R2
        R2.dress(-17, -11, 5.0, 6.5, 4, 4, kinds=('basket', 'basket', 'silk'))   # dark props in the bottom 30 %
        R2.dress(-16, -12, 11.6, 12.4, 3, 5, kinds=('basket', 'rope'))
def actors(f, cam, ctx):
    t = (f - 78) / 30.0
    C.person_card('tiandan', 'tiandan_tie_blade', (-24.0, 11.4, 0), cam, 0, bob=C.hop(f, 0, 0.04, 2.0), roll=2.5 * math.sin(2 * math.pi * 1.5 * t))
    C.ox_card(SHOT, 0, (-21.6, 10.4, 0), 180, 1.0, cam, view='front_three_quarter', gait='stand', bob=C.hop(f, 1, 0.03, 0.8), roll=C.sway(f, 1, 1.6, 0.9))
    for i, m in enumerate(HERD):
        x, y, z, yaw, sc = m
        spd = 1.7; xx = x - spd * t
        near = math.hypot(x + 28, y - 11.5) < 20
        ph = int((f * 0.32 + i * 3) % 8)
        C.ox_card(SHOT, i + 1, (xx, y, 0), 180, sc, cam, view='front_three_quarter' if near else 'three_quarter', gait='walk', phase=ph, bob=0.04 * abs(math.sin(2 * math.pi * (f * 0.32 + i) / 8)))
if __name__ == '__main__':
    C.run(SHOT, actors, G0, G1, HB, HA, quality=sys.argv[1] if len(sys.argv) > 1 else None, tweak=tweak, shk=0.015)

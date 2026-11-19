import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C, jimo_shots as S
SHOT = 's05'; G0, G1, HB, HA = 384, 459, 8, 0
def tweak(stage, A=None):
    if stage == 'pre':
        c = S.SHOTS[SHOT]['cam']; c['look_at'] = (c['look_at'][0], c['look_at'][1], 1.4); S.SHOTS[SHOT]['move'].update(slide=25, push=0.04)
        S.SHOTS[SHOT]['move']['moves'] = [dict(t=0.16, d=0.84, dur=5), dict(t=0.34, d=1.16, dur=6), dict(t=0.55, d=0.85, dur=5), dict(t=0.74, d=1.15, dur=6)]      # tilt down ~5 deg: sky <= 30 %
def actors(f, cam, ctx):
    t = (f - G0) / 30.0
    # Tian Dan in FRONT of the counter, between the old man and the woman, receiving the sash across the counter
    C.person_card('tiandan', 'tiandan_accept_sash', (-74.2, 21.6, 0), cam, 0, bob=C.hop(f, 0, 0.03, 1.4), roll=2.0 * math.sin(2 * math.pi * 0.9 * t) + 1.0, sx=1.0)
    C.person_card('townsfolk', 'old_man_stand', (-75.6, 19.8, 0), cam, 1, bob=C.hop(f, 1, 0.03, 1.2), roll=C.sway(f, 1, 2.5, 0.9))
    C.person_card('townsfolk', 'woman_stand', (-75.2, 24.0, 0), cam, 2, bob=C.hop(f, 2, 0.03, 1.1), roll=C.sway(f, 2, 2.5, 0.8))
    C.person_card('townsfolk', 'old_man_stand', (-76.2, 26.2, 0), cam, 3, bob=C.hop(f, 3, 0.03, 1.0), roll=C.sway(f, 3, 2.0, 0.7), mirror=True)
    C.person_card('child', 'child_stand', (-74.4, 25.4, 0), cam, 4, bob=C.hop(f, 4, 0.08, 2.4), roll=C.sway(f, 4, 3.0, 1.1))
if __name__ == '__main__':
    C.run(SHOT, actors, G0, G1, HB, HA, quality=sys.argv[1] if len(sys.argv) > 1 else None, tweak=tweak, shk=0.009)

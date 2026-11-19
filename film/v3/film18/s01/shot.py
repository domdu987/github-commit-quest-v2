import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C
SHOT = 's01'; G0, G1, HB, HA = 0, 78, 0, 0
ROW = [(x, 7.4 + 0.5 * (k % 2)) for k, x in enumerate((-15.0, -9.5, -4.0, 1.5, 7.0, 12.5))]
def tweak(stage, A=None):
    if stage == 'pre':     # punch-in snaps (client rule: median >= 4, p90 >= 12): quick pushes on the tug beats
        import jimo_shots as S
        S.SHOTS[SHOT]['cam']['look_at'] = (-2.0, 12.5, 3.3); S.SHOTS[SHOT]['move'].update(push=0.09, slide=-40); S.SHOTS[SHOT]['fg'] = ('torch', 'right')
        S.SHOTS[SHOT]['move']['moves'] = [dict(t=0.28, d=0.78, dur=6), dict(t=0.58, d=0.80, dur=6), dict(t=0.82, d=0.86, dur=5), dict(t=0.44, d=1.08, dur=5), dict(t=0.7, d=1.08, dur=5)]
def actors(f, cam, ctx):
    t = f / 30.0
    # Tian Dan hauls the silk coat over the ox: rocks toward / away from the ox, arms-tug rhythm 1.6 Hz
    pull = math.sin(2 * math.pi * 1.6 * t)
    C.person_card('tiandan', 'tiandan_tug_cloth', (-4.1 + 0.18 * pull, 16.8 + 0.05 * pull, 0), cam, 0, bob=C.hop(f, 0, 0.04, 1.6), roll=3.0 * pull, sz=1 + 0.015 * pull)
    C.ox_card(SHOT, 0, (-1.2 + 0.05 * pull, 15.2, 0), 165, 1.0, cam, gait='stand', bob=C.hop(f, 1, 0.03, 0.8), roll=C.sway(f, 1, 1.6, 0.9))
    for i, (x, y) in enumerate(ROW):
        C.ox_card(SHOT, i + 1, (x, y, 0), 180, 1.0, cam, gait='stand', bob=C.hop(f, i, 0.03, 0.6), roll=C.sway(f, i + 3, 1.8, 0.55))
if __name__ == '__main__':
    C.run(SHOT, actors, G0, G1, HB, HA, quality=sys.argv[1] if len(sys.argv) > 1 else None, tweak=tweak, shk=0.015)

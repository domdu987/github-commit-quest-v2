import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C, jimo_shots as S
SHOT = 's07'; G0, G1, HB, HA = 531, 597, 0, 9
M = S.marks_for(SHOT)
def tweak(stage, A=None):
    if stage == 'pre':
        c = S.SHOTS[SHOT]['cam']; c.update(loc=(0.0, 46.0, 14.0), look_at=(0.0, 24.0, 0.5), lens=16.0)
        S.SHOTS[SHOT]['move'].update(push=-0.03); S.SHOTS[SHOT]['move']['moves'] = [dict(t=0.2, d=1.1, dur=5), dict(t=0.55, d=1.3, dur=7), dict(t=0.8, d=1.06, dur=5), dict(t=0.35, d=0.93, dur=5)]
ALL = [(r, i, m) for r in ('herd', 'herd_pen', 'herd_far') for i, m in enumerate(M[r])]
def actors(f, cam, ctx):
    t = (f - G0) / 30.0
    for n, (r, i, m) in enumerate(ALL):
        x, y, z, yaw, sc = m
        if r == 'herd_pen': yaw = -90.0
        dragon = (n % 3 == 0)
        walking = r != 'herd_pen' or n % 2 == 0
        sp = 0.0 if r == 'herd_pen' else 0.6
        dx, dy = math.cos(math.radians(yaw)) * sp * t, math.sin(math.radians(yaw)) * sp * t
        ph = int((f * 0.25 + n * 3) % 8)
        C.ox_card(SHOT + r, n, (x + dx, y + dy, 0), yaw, sc, cam, state='dragon' if dragon else 'plain', view='three_quarter', gait='walk' if walking else 'stand', phase=ph, theta=30,
                  bob=0.04 * abs(math.sin(2 * math.pi * (f * 0.25 + n) / 8)) if walking else C.hop(f, n, 0.03, 0.7), roll=0 if walking else C.sway(f, n, 1.5, 0.6))
if __name__ == '__main__':
    C.run(SHOT, actors, G0, G1, HB, HA, quality=sys.argv[1] if len(sys.argv) > 1 else None, tweak=tweak, shk=0.013)

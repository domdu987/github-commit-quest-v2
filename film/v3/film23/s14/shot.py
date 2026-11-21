#!/usr/bin/env python3
"""shot.py -- film 23 take s14: RHINE night, March 1945.  Extreme wide high over the river, slow descend; the RHINE sign on the bank; soldiers unload crates of
folded rubber from the trucks and carry them to the supply dump.  g0 1506, g1 1626 (planned), render 1506..1656 (x1.25 tail) + 10 in-handle (dissolve 17).
    python3 shot.py stills i,j,k out [scale spp] | final a:b[:step] [scale spp] | probe i,j | ground [every]
Body index i = -10..150 (g = 1506 + i)."""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import c23 as C
from c23 import GH, SH, bpy, Vector, cast23, sprites, lerp, blink
TMP = os.path.join(HERE, 'work')
SHOT = 'S14'; G0 = 1506; G1 = 1626; HANDLE = 10
G_OF = lambda i: G0 + i
C.TINT.update(tint='#c8ccf0', ink='#1e142e')
MEM = ['gi_pump', 'gi_radio', 'gi_driver', 'gi_painter', 'gi_designer', 'gi_smile', 'gi_sound']

def make_take():
    return C.Take(SHOT, handle=HANDLE)

def canvas_for(cast, fn, n=8):
    return sprites.canvas_for(cast, [fn(k / float(n)) for k in range(n)], margin=0.25)

def specs_of(Tk):
    sd = os.path.join(TMP, 'sprites'); S = []
    ox, oy, oz = GH.loc_origin(); M = GH.marks(SHOT)['unloaders']
    # (start world x, y, member, vx, vy (D/s), action)   carriers walk from the truck toward the supply dump (south-east of the trucks), stand-and-sway unloader on the tailgate
    runs = []
    for k, m in enumerate(M):
        runs.append((m[0] + (5.0 if k == 2 else 0.0), m[1] - (1.5 if k == 2 else 0.0), MEM[k], (0.5 if k == 0 else (-0.5 if k == 1 else 0.0)), -0.6 if k < 3 else 0.0, 'carry' if k < 3 else 'stand', m[2]))
    # extra carriers NORTH of the trucks (between the trucks and the tank rows): they stay far from the lens, so every head stays above y 880 to the end of the descend
    extra = [(ox - 80.0, oy - 166.0, 'gi_designer', 0.4, 0.0, 'carry'), (ox - 70.0, oy - 168.5, 'gi_painter', -0.4, 0.0, 'carry'),
             (ox - 96.0, oy - 163.0, 'gi_sound', 0.5, 0.0, 'carry'), (ox - 86.0, oy - 170.0, 'gi_smile', 0.0, 0.0, 'stand')]
    runs += extra
    for k, run in enumerate(runs):
        x, y, cast, vx, vy, act = run[:6]; zm = run[6] if len(run) > 6 else None
        fac = 1 if vx >= 0 else -1
        if act == 'carry':
            cv = canvas_for(cast, lambda ph, c=cast, fac=fac: cast23.carry_pose(c, ph, fac))
            pose = (lambda i, g, c=cast, fac=fac, k=k: cast23.carry_pose(c, ((g * 0.0 + g) / 28.0 + 0.17 * k) % 1.0, fac))
            def pos(i, f, x=x, y=y, vx=vx, vy=vy, k=k):
                t = i / 30.0; wx, wy = x + vx * t, y + vy * t
                return (wx, wy, GH.ground_z(wx, wy) - 0.03)
        else:
            cv = canvas_for(cast, lambda ph, c=cast: dict(cast23.STORY23['gi_stand_' + c.split('_')[1]][1]))
            def pose(i, g, c=cast, k=k):
                p = dict(cast23.STORY23['gi_stand_' + c.split('_')[1]][1]); p['lean'] = 3.0 * math.sin(g * 0.13 + k); p['blink'] = blink(g, [30, 90]); return p
            pos = (lambda i, f, x=x, y=y, zm=zm: (x, y, (zm if zm is not None else GH.ground_z(x, y)) - 0.03))
        a = C.make_actor('u%d' % k, cast, sd, canvas=cv)
        S.append(C.Spec(a, pos, pose, 32))
    return S

def state_of(Tk, i, f):
    GH.flicker(f)

if __name__ == '__main__':
    C.cli(make_take, specs_of, state_of, G0 - HANDLE, HANDLE, G_OF)

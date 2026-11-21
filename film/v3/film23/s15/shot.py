#!/usr/bin/env python3
"""shot.py -- film 23 take s15: RHINE night, the south field.  Crane up over the rows of rubber tanks inflating in lantern light (staggered set_inflate), pump crews
pumping, a carrier and a watcher.  g0 1629, g1 1728 (planned), render 1629..1753 (x1.25 tail) + 7 in-handle (dissolve 11).
    python3 shot.py stills i,j,k out [scale spp] | final a:b[:step] [scale spp] | probe i,j | ground [every]
Body index i = -7..124 (g = 1629 + i)."""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import c23 as C
from c23 import GH, SH, bpy, Vector, cast23, sprites, lerp, blink
import ghost_shot_table as TB
TMP = os.path.join(HERE, 'work')
SHOT = 'S15'; G0 = 1629; G1 = 1728; HANDLE = 7
G_OF = lambda i: G0 + i
C.TINT.update(tint='#c8ccf0', ink='#1e142e')

def make_take():
    return C.Take(SHOT, handle=HANDLE)

def canvas_for(cast, fn, n=8):
    return sprites.canvas_for(cast, [fn(k / float(n)) for k in range(n)], margin=0.25)

def specs_of(Tk):
    sd = os.path.join(TMP, 'sprites'); S = []
    M = [list(m) for m in GH.marks(SHOT)['pumpcrew']]
    ox, oy, oz = GH.loc_origin()
    # nearer crews (QA: the crews must read): two pump men put where the camera rays of the LAST frame land at screen y ~790 (heads then stay above y 880 through the crane up)
    for k, (sx, sy) in enumerate(((510.0, 805.0), (215.0, 775.0))):
        p = C.ground_at_screen(Tk, 124, sx, sy)
        M[k][0], M[k][1], M[k][2] = p
    pump_cast = ['gi_pump', 'gi_radio', 'gi_driver']
    for k, m in enumerate(M[:3]):
        cast = pump_cast[k]
        a = C.make_actor('pump%d' % k, cast, sd, canvas=cast23.CANVAS23_WIDE.get(cast) or canvas_for(cast, lambda ph, c=cast: cast23.pump_frame(c, ph, 1)))
        S.append(C.Spec(a, (lambda i, f, m=m: (m[0], m[1], m[2] - 0.03)), (lambda i, g, c=cast, k=k: dict(cast23.pump_frame(c, ((g / 20.0) + 0.31 * k) % 1.0, 1 if k != 1 else -1), blink=blink(g, [22 + 9 * k, 80]))), 96))
    # the watcher (stand, sway) and the carrier (walk with a crate)
    m = M[3]; cast = 'gi_designer'
    a = C.make_actor('watch', cast, sd, canvas=canvas_for(cast, lambda ph: dict(cast23.STORY23['gi_stand_designer'][1])))
    def pw(i, g):
        p = dict(cast23.STORY23['gi_stand_designer'][1]); p['lean'] = 2.5 * math.sin(g * 0.12); p['head_roll'] = 2.0 * math.sin(g * 0.07); p['blink'] = blink(g, [31, 90]); return p
    S.append(C.Spec(a, (lambda i, f, m=m: (m[0], m[1], m[2] - 0.03)), pw, 64))
    m = M[4]; cast = 'gi_smile'
    a = C.make_actor('carr', cast, sd, canvas=canvas_for(cast, lambda ph: cast23.carry_pose(cast, ph, 1)))
    def pc(i, f, m=m):
        wx, wy = m[0] + 0.5 * i / 30.0, m[1] - 0.2 * i / 30.0
        return (wx, wy, GH.ground_z(wx, wy) - 0.03)
    S.append(C.Spec(a, pc, (lambda i, g: cast23.carry_pose('gi_smile', (g / 28.0) % 1.0, 1)), 64))
    return S

def state_of(Tk, i, f):
    t = Tk.t_of(i)
    Tk.scene.frame_set(f)          # evaluate the keyed state first: GH.ground_snap inside set_inflate must see this frame's keys, not stale ones
    for k in range(42):
        GH.set_inflate('decoy%d' % k, 0.2 + 0.8 * TB._sm(0.08 * (k % 7) - 0.1 + 0.05 * (k // 7), 0.5 + 0.08 * (k % 7) + 0.05 * (k // 7), max(t, 0.0)), frame=f)
    GH.flicker(f)

if __name__ == '__main__':
    C.cli(make_take, specs_of, state_of, G0 - HANDLE, HANDLE, G_OF)

#!/usr/bin/env python3
"""shot.py -- film 23 take s01: FIELDS dawn, BIGZOOM 1.  Extreme wide high oblique down onto the rubber tank column, descend + push past two poplars,
end medium 3/4 on the lead tank (col0) with a soldier on its deck waving the column on.  g0 0, g1 120 (planned), render 0..150 (x1.25 tail), no in-handle (open).
    python3 shot.py stills i,j,k out [scale spp] | final a:b[:step] [scale spp] | probe i,j | ground [every]
Body index i = 0..150 (g = i)."""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import c23 as C
from c23 import GH, SH, bpy, Vector, cast23, sprites, lerp, blink
import ghost_shot_table as TB
TMP = os.path.join(HERE, 'work')
SHOT = 'S01'; G0 = 0; G1 = 120; HANDLE = 0
G_OF = lambda i: G0 + i

def make_take():
    return C.Take(SHOT, handle=HANDLE)

def canvas_for(cast, fn, n=8):
    return sprites.canvas_for(cast, [fn(k / float(n)) for k in range(n)], margin=0.25)

def specs_of(Tk):
    sd = os.path.join(TMP, 'sprites'); S = []
    M = GH.marks(SHOT); Tk.col0 = bpy.data.objects['col0']
    wk = M['walkers']
    # rider on col0's rear deck: waves the column on (the tank is scaled 1.2: world = col0.matrix_world @ local mark)
    loc = (-2.9, 0.4, 3.3)
    a = C.make_actor('rider', 'gi_smile', sd, canvas=canvas_for('gi_smile', lambda ph: cast23.wave_frame('gi_smile', ph, 1)))
    S.append(C.Spec(a, lambda i, f: C.world_of(Tk.col0, loc), lambda i, g: dict(cast23.wave_frame('gi_smile', (g / 12.0) % 1.0, 1), blink=blink(g, [26, 71, 118])), 128))
    a = C.make_actor('walk0', 'gi_pump', sd, canvas=canvas_for('gi_pump', lambda ph: cast23.wave_frame('gi_pump', ph, -1)))
    p0 = wk[0]
    S.append(C.Spec(a, lambda i, f: (p0[0], p0[1], p0[2]), lambda i, g: dict(cast23.wave_frame('gi_pump', (g / 12.0 + 0.4) % 1.0, -1), blink=blink(g, [40, 95])), 64))
    a = C.make_actor('walk1', 'gi_designer', sd, canvas=canvas_for('gi_designer', lambda ph: dict(cast23.STORY23['gi_stand_designer'][1])))
    p1 = wk[1]
    def stand_pose(i, g):
        p = dict(cast23.STORY23['gi_stand_designer'][1]); p['lean'] = 2.0 * math.sin(g * 0.11); p['head_roll'] = 2.0 * math.sin(g * 0.07); p['blink'] = blink(g, [33, 88]); return p
    S.append(C.Spec(a, lambda i, f: (p1[0], p1[1], p1[2]), stand_pose, 64))
    return S

def state_of(Tk, i, f):
    t = Tk.t_of(i)
    TB._a01(GH, t) if False else GH.set_column(1.0 * 4.0 * t, frame=f)
    GH.flicker(f) if False else None

if __name__ == '__main__':
    C.cli(make_take, specs_of, state_of, G0 - HANDLE, HANDLE, G_OF)

#!/usr/bin/env python3
"""shot.py -- film 23 take s18: RHINE north, PRE-DAWN. Low oblique over the water, pontoon bridge diagonal, TWO assault boats (paddlers + dog)
close, troops tiptoe on the bridge, far-bank troops busy.  g0 1905, g1 1980 (planned), render 1905..1999 (x1.25 tail) + 9 in-handle (dissolve 13).
    python3 shot.py stills i,j,k out [scale spp] | final a:b[:step] [scale spp] | probe i,j
Body index i = 0..94 (g = 1905 + i); handle i = -9..-1."""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import c23 as C
from c23 import GH, SH, bpy, Vector, cast23, sprites, lerp, blink
TMP = os.path.join(HERE, 'work')
SHOT = 'S18'; G0 = 1905; G1 = 1980; HANDLE = 9
G_OF = lambda i: G0 + i

# ---- runtime camera (QA_ART_SET note: water <= 40 % of the frame): tilt up ~11 deg, horizon at ~0.62 H; boats pushed out to 13-22 D so heads stay above y 880
SH.SHOTS[SHOT]['cam'] = dict(loc=(-33.0, 361.5, 1.35), look_at=(20.0, 386.0, 14.3), lens=22)
SH.SHOTS[SHOT]['move'] = dict(end=dict(loc=(-27.0, 360.0, 1.0), look_at=(16.0, 385.0, 10.9), lens=27.0))      # a real pan east along the boats + a lens push (rhythm: the set's own end pose moved only 0.7 D)

C.TINT.update(tint='#c0caf2', ink='#1e1a3a')
MEM = ['gi_radio', 'gi_pump', 'gi_smile', 'gi_driver', 'gi_designer', 'gi_painter', 'gi_sound']
BOAT_V = 1.6                                    # D/s drift east
BOATS = {'boat3': (-21.5, 367.0), 'boat2': (-14.0, 373.5)}   # local RHINE (x, y) at i = 0

def boat_xy(name, i):
    x0, y0 = BOATS[name]; t = i / 30.0
    return (x0 + BOAT_V * t, y0 + 0.18 * math.sin(t * 1.7 + (1.3 if name == 'boat2' else 0)))

class Take(C.Take):
    pass

def make_take():
    Tk = Take(SHOT, handle=HANDLE)
    ox, oy, oz = GH.loc_origin()
    # near-bank + far-bank poplars (silhouette height for the tall frame; the sky is no longer empty)
    C.add_poplars([((ox - 44.0, oy + 372.0), 38.0, 7001), ((ox - 6.0, oy + 392.0), 30.0, 7002), ((ox + 30.0, oy + 398.0), 34.0, 7003)])
    # warm lanterns on the bridge rail: their streaks lie on the water (pre-dawn, dimmed but warm against the blue)
    C.add_lanterns([((ox - 26.0, oy + 377.7, 2.7), 700.0, 0.9, 0.8), ((ox - 12.0, oy + 377.7, 2.7), 700.0, 0.9, 0.8), ((ox + 2.0, oy + 377.7, 2.7), 700.0, 0.9, 0.8), ((ox + 16.0, oy + 377.7, 2.7), 700.0, 0.9, 0.8)])
    return Tk

def canvas_for(cast, posefn, n=8):
    return sprites.canvas_for(cast, [posefn(k / float(n)) for k in range(n)], margin=0.25)

def specs_of(Tk):
    S = []; own = {}
    boats = {n: bpy.data.objects[n] for n in BOATS}
    Tk.boats = boats
    sd = os.path.join(TMP, 'sprites')
    # paddlers: (boat, member, local x)
    plan = [('boat3', 'gi_pump', -1.5), ('boat3', 'gi_radio', 0.0),
            ('boat2', 'gi_smile', -1.5), ('boat2', 'gi_driver', 0.0), ('boat2', 'gi_designer', 1.3)]
    for k, (bn, cast, lx) in enumerate(plan):
        a = C.make_actor('pad%d' % k, cast, sd, canvas=canvas_for(cast, lambda ph, c=cast: cast23.paddle_frame(c, ph, 1)))
        par = boats[bn]
        pos = (lambda i, f, par=par, lx=lx: C.world_of(par, (lx, 0.0, -0.76)))
        pose = (lambda i, g, c=cast, k=k: dict(cast23.paddle_frame(c, ((g - 0) / 24.0 + 0.19 * k) % 1.0, 1), blink=blink(g, [20 + 17 * k, 60 + 11 * k])))
        a.card['gc_gap'] = 1.8        # cast23: the paddle blade dips below the knees ON PURPOSE; its tip meets the river bed, the knees stand on the boat-floor mark
        S.append(C.Spec(a, pos, pose, 96 if bn == 'boat3' else 64))
    # tiptoe troops on the bridge deck (z 0.52), world = local + origin (0, 9000)
    ox, oy, oz = GH.loc_origin()
    for k, (x, y, cast) in enumerate([(-20.0, 381.0, 'gi_designer'), (-11.0, 379.4, 'gi_painter'), (-2.0, 381.2, 'gi_sound'), (8.0, 379.6, 'gi_driver')]):
        a = C.make_actor('tip%d' % k, cast, sd, canvas=canvas_for(cast, lambda ph, c=cast: cast23.tiptoe_frame(c, ph, 1), 8))
        pos = (lambda i, f, x=x, y=y: (ox + x + 0.7 * i / 30.0, oy + y, 0.50))
        pose = (lambda i, g, c=cast, k=k: dict(cast23.tiptoe_frame(c, (g / 32.0 + 0.23 * k) % 1.0, 1), blink=blink(g, [25 + 9 * k, 70])))
        S.append(C.Spec(a, pos, pose, 48))
    # far bank troops (busy: carry crates / stand / wave)
    far = [(46.0, 383.0, 'gi_pump', 'carry'), (49.5, 389.0, 'gi_radio', 'stand'), (45.0, 395.0, 'gi_smile', 'wave'), (52.0, 380.0, 'gi_driver', 'carry'), (55.0, 392.0, 'gi_painter', 'stand')]
    for k, (x, y, cast, act) in enumerate(far):
        cv = canvas_for(cast, (lambda ph, c=cast: cast23.carry_pose(c, ph, 1)) if act == 'carry' else (lambda ph, c=cast: cast23.wave_frame(c, ph, 1)))
        a = C.make_actor('far%d' % k, cast, sd, canvas=cv)
        if act == 'carry':
            pos = (lambda i, f, x=x, y=y: (lambda wx, wy: (wx, wy, GH.ground_z(wx, wy) - 0.03))(ox + x - 0.5 * i / 30.0, oy + y))
            pose = (lambda i, g, c=cast: cast23.carry_pose(c, (g / 28.0) % 1.0, -1))
        elif act == 'wave':
            pos = (lambda i, f, x=x, y=y: (ox + x, oy + y, GH.ground_z(ox + x, oy + y) - 0.03))
            pose = (lambda i, g, c=cast: cast23.wave_frame(c, (g / 12.0) % 1.0, 1))
        else:
            pos = (lambda i, f, x=x, y=y: (ox + x, oy + y, GH.ground_z(ox + x, oy + y) - 0.03))
            pose = (lambda i, g, c=cast, k=k: dict(cast23.cast23.STORY23['gi_stand_' + c.split('_')[1]][1] if False else cast23.STORY23['gi_stand_' + c.split('_')[1]][1], lean=2.0 * math.sin(g * 0.11 + k), blink=blink(g, [18 + 7 * k, 66])))
        S.append(C.Spec(a, pos, pose, 32))
    # the dog on boat3 (no cast23 card: own drawing)
    paths, size = C.dog_pngs(os.path.join(TMP, 'dog'))
    c0 = SH.pose(SHOT, 0.0)['loc']; dp = Vector(boat_xy('boat3', 0)) + Vector((ox, oy)) + Vector((1.95, 0))
    yaw = math.degrees(math.atan2(c0[0] - dp.x, -(c0[1] - dp.y)))
    Tk.dog = C.DogCard('dog', paths, size, parent=boats['boat3'], local=(1.95, 0.0, -0.76), yaw_world=yaw, sc=1.0)
    Tk.dog.root['gc_role'] = 'skip'
    Tk.specs = S
    return S

def state_of(Tk, i, f):
    t = Tk.t_of(i)
    GH.set_boats(0.19 + 0.04 * t / 1.25, frame=f)
    for n in BOATS:                                    # my two boats: own drift, yaw 0, a gentle bob
        x, y = boat_xy(n, i); GH._place(Tk.boats[n], (x, y), 0.0 + 1.5 * math.sin(i / 30.0 * 2.0 + (0.6 if n == 'boat2' else 0)), f, ground=False)
    GH.flicker(f)
    Tk.dog.wag(f, (i // 6) % 2)

def extra(Tk, i, f):
    """water share of the frame: the screen row of the far water line (a water point 2500 D away along the view direction, z = water level)"""
    Tk.scene.frame_set(f); cam = Tk.cam; mw = cam.matrix_world; loc = mw.translation; fwd = -(mw.to_3x3() @ Vector((0, 0, 1))); fwd.z = 0; fwd.normalize()
    p = Vector((loc.x + fwd.x * 2500, loc.y + fwd.y * 2500, -0.6))
    import render as R
    sx, sy = R.world_to_screen(cam, p, frame=f, scene=Tk.scene)[:2]
    return dict(horizon_y=round(sy, 1), water_frac=round(1.0 - sy / 1280.0, 3))

if __name__ == '__main__':
    C.cli(make_take, specs_of, state_of, G0 - HANDLE, HANDLE, G_OF, extra_report=extra)

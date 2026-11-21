#!/usr/bin/env python3
"""shot.py -- film 23 take s16: RHINE night, the south field.  Push along the sound truck (its record spins, the horn booms) and the radio tent; 30th / 79th INF DIV
crates in the foreground; the sound man points at the horn, the radio man chatters into his handset, a soldier carries a crate.  Exposure lifted (QA: luma >= 70).
g0 1728, g1 1827 (planned), render 1728..1852 (x1.25 tail), cut in (no in-handle).
    python3 shot.py stills i,j,k out [scale spp] | final a:b[:step] [scale spp] | probe i,j | ground [every]
Body index i = 0..124 (g = 1728 + i)."""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import c23 as C
from c23 import GH, SH, bpy, Vector, cast23, sprites, lerp, blink
TMP = os.path.join(HERE, 'work')
SHOT = 'S16'; G0 = 1728; G1 = 1827; HANDLE = 0
G_OF = lambda i: G0 + i
EXPO = float(os.environ.get('EXPO', '0.6'))          # added to the set's exposure (QA: S16 luma >= 70)
C.TINT.update(tint='#c8ccf0', ink='#1e142e')

def make_take():
    Tk = C.Take(SHOT, handle=HANDLE)
    Tk.expo_add = EXPO
    return Tk

def canvas_for(cast, fn, n=8):
    return sprites.canvas_for(cast, [fn(k / float(n)) for k in range(n)], margin=0.25)

def specs_of(Tk):
    sd = os.path.join(TMP, 'sprites'); S = []
    M = GH.marks(SHOT)
    ox, oy, oz = GH.loc_origin()
    def at(x, y):                                    # local RHINE (x, y) -> world mark on the real ground
        wx, wy = ox + x, oy + y; return (wx, wy, GH.ground_z(wx, wy), 0.0, {})
    # the radio man and the carrier hid behind the truck at 55-65 D: put their feet at chosen screen spots of the MID frame (camera ray -> ground)
    M['radioman'] = [C.ground_at_screen(Tk, 62, 560.0, 835.0) + (0.0, {})]; M['soldier'] = [C.ground_at_screen(Tk, 62, 330.0, 860.0) + (0.0, {})]
    # sound man: points at the horn, leans toward it (switch-throwing pose, a small sway)
    m = M['soundman'][0]; cast = 'gi_sound'
    base = dict(cast23.STORY23['gi_point_sound'][1])
    a = C.make_actor('sound', cast, sd, canvas=canvas_for(cast, lambda ph: dict(base)))
    S.append(C.Spec(a, (lambda i, f, m=m: (m[0], m[1], m[2] - 0.03)),
                    (lambda i, g: dict(base, lean=3.0 * math.sin(g * 0.15), head_roll=2.0 * math.sin(g * 0.09), blink=blink(g, [24, 77]), arm_r=dict(base['arm_r'], hand=(1.05, 0.05 + 0.06 * math.sin(g * 0.3))))), 128))
    # radio man: seated on a crate, handset to the ear, the chatter mouth is ONE held drawing (talk_a), no mouth movement
    m = M['radioman'][0]; cast = 'gi_radio'
    rb = cast23.sit_crate_pose(cast, expr='talking', mouth='talk_a', pitch=-0.1, arm_r={'hand': (0.5, 0.06), 'bend': 0.9, 'stretch': 1.0, 'layer': 'top'}, prop_r={'type': 'handset23', 'angle': -95},
                               arm_l={'hand': (-0.35, 0.8), 'bend': 0.6, 'shape': 'point'})
    a = C.make_actor('radio', cast, sd, canvas=canvas_for(cast, lambda ph: dict(rb)))
    S.append(C.Spec(a, (lambda i, f, m=m: (m[0], m[1], m[2] - 0.03)), (lambda i, g: dict(rb, head_roll=-3.0 + 2.5 * math.sin(g * 0.2), lean=1.5 * math.sin(g * 0.13), blink=blink(g, [38, 90]))), 128))
    # soldier carrying a crate toward the tent
    m = M['soldier'][0]; cast = 'gi_pump'
    a = C.make_actor('carry', cast, sd, canvas=canvas_for(cast, lambda ph: cast23.carry_pose(cast, ph, -1)))
    def pc(i, f, m=m):
        wx, wy = m[0] + (62 - i) / 30.0 * 0.0 - 0.15 * (i - 62) / 30.0, m[1] + 0.75 * (i - 62) / 30.0
        return (wx, wy, GH.ground_z(wx, wy) - 0.03)
    S.append(C.Spec(a, pc, (lambda i, g: cast23.carry_pose('gi_pump', (g / 28.0) % 1.0, -1)), 96))
    return S

def state_of(Tk, i, f):
    GH.flicker(f)
    GH.set_record((i / 30.0) * 78.0 / 60.0 * 360.0, frame=f)          # the sound truck's record spins at 78 rpm

if __name__ == '__main__':
    C.cli(make_take, specs_of, state_of, G0 - HANDLE, HANDLE, G_OF)

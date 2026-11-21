#!/usr/bin/env python3
"""shot.py -- film 23 take s17: RHINE far bank, night.  OTS from behind the two German observers (cast23 has no back views: 3/4 front cards) across the river to the glowing
decoy field: the tall one lowers his binoculars, nudges the other and points south; the round one drops his sausage.  Comic, no weapons.
g0 1827, g1 1905 (planned), render 1827..1925 (x1.25 tail) + 7 in-handle (dissolve 11).  Mouths still (held expression drawings only).
    python3 shot.py stills i,j,k out [scale spp] | final a:b[:step] [scale spp] | probe i,j | ground [every]
Body index i = -7..98 (g = 1827 + i)."""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import c23 as C
from c23 import GH, SH, bpy, Vector, cast23, sprites, lerp, blink, actors
TMP = os.path.join(HERE, 'work')
SHOT = 'S17'; G0 = 1827; G1 = 1905; HANDLE = 7
G_OF = lambda i: G0 + i
C.TINT.update(tint='#c8ccf0', ink='#1e142e')
I_DROP = 50                                    # body index: the sausage leaves the hand
FALL_G = 40.0                                  # D/s^2 (a 1.8 D fall takes ~0.3 s)
S = cast23.STORY23

def make_take():
    return C.Take(SHOT, handle=HANDLE)

def canvas_for(cast, poses):
    return sprites.canvas_for(cast, poses, margin=0.25)

def tall_pose(i, g):
    # i: 0..22 binoculars up (squint) -> 22..44 nudge -> 44.. point south; expression swaps sit behind blinks
    if i < 24:   base = dict(S['ger_binoc_tall'][1]); k = 'b'
    elif i < 46: base = dict(S['ger_nudge_tall'][1], mirror=False); k = 'n'
    else:        base = dict(S['ger_point_tall'][1]); k = 'p'
    base['t'] = g / 30.0
    base['lean'] = base.get('lean', 0) + 2.0 * math.sin(g * 0.17) + (4.0 * math.sin((g - 24) * 0.55) if k == 'n' else 0.0)
    base['head_roll'] = base.get('head_roll', 0) + 1.5 * math.sin(g * 0.09)
    if k == 'p': base['arm_r'] = dict(base['arm_r'], hand=(1.05, -0.05 + 0.05 * math.sin(g * 0.35)))
    base['blink'] = blink(g, [G0 + 23, G0 + 45, G0 + 80])
    return base

def round_pose(i, g):
    if i < I_DROP: base = dict(S['ger_sausage'][1]); k = 's'
    elif i < I_DROP + 22: base = dict(S['ger_drop_sausage'][1]); k = 'd'
    else: base = dict(S['ger_surprise_round'][1]); k = 'x'
    base['t'] = g / 30.0
    base['lean'] = base.get('lean', 0) + (1.5 * math.sin(g * 0.35) if k == 's' else 1.5 * math.sin(g * 0.13))      # chewing bob / shock sway
    base['head_roll'] = base.get('head_roll', 0) + 1.5 * math.sin(g * 0.11)
    base['blink'] = blink(g, [G0 + I_DROP - 2, G0 + I_DROP + 22, G0 + 85])
    return base

def specs_of(Tk):
    sd = os.path.join(TMP, 'sprites'); Sp = []
    ox, oy, oz = GH.loc_origin()
    ia = 45
    tx = C.ground_at_screen(Tk, ia, 235.0, 1060.0); rx = C.ground_at_screen(Tk, ia, 505.0, 1090.0)
    a = C.make_actor('tall', 'ger_tall', sd, canvas=canvas_for('ger_tall', [S['ger_binoc_tall'][1], S['ger_nudge_tall'][1], S['ger_point_tall'][1]]))
    Sp.append(C.Spec(a, (lambda i, f: (tx[0], tx[1], tx[2] - 0.03)), tall_pose, 128))
    b = C.make_actor('round', 'ger_round', sd, canvas=canvas_for('ger_round', [S['ger_sausage'][1], S['ger_drop_sausage'][1], S['ger_surprise_round'][1]]))
    Sp.append(C.Spec(b, (lambda i, f: (rx[0], rx[1], rx[2] - 0.03)), round_pose, 128))
    # the falling sausage (cast23.sausage_svg): 12 rotation variants, one upright card (origin at its centre), keyed per frame
    items = [(cast23.sausage_svg('s%d' % k, angle=30.0 * k, tint='#c8ccf0'), (-0.7, -0.7, 1.0, 0.7), 192) for k in range(12)]
    paths = C.svg_pngs(items, os.path.join(TMP, 'sausage'))
    Tk.saus = C.DogCard('sausage', paths, (1.7, 1.4, 192), center=True)
    Tk.saus.root['gc_role'] = 'skip'
    return Sp

def state_of(Tk, i, f):
    GH.flicker(f)

def post_fn(Tk, specs, idx):
    """the sausage: hidden until the drop; falls from the round man's hand (anchor hand_r of his drawn pose), lands on the ground and stays, rotating while it falls."""
    rnd = [s for s in specs if s.actor.name == 'round'][0].actor
    fd = Tk.bf(I_DROP); Tk.scene.frame_set(fd)
    an = Tk.anch.get(('round', fd))
    if an is None:                                   # sparse frame list: draw that one pose
        rnd.pose(fd, dict(round_pose(I_DROP, G_OF(I_DROP)), **C.TINT), camera=Tk.cam); Tk.sprites_for(rnd, [fd], 128); an = Tk.anch[('round', fd)]
    hand = actors.local_to_world(rnd, an['hand_r'], fd, camera=Tk.cam)
    gz = GH.ground_z(hand.x, hand.y); gz = gz if gz is not None else hand.z - 2.0
    cx, cy = hand.x, hand.y
    land_z = gz + 0.35 * 1.0                          # card centre: half the 0.7 D sausage height above the ground... lies flat (variant 0..), centre 0.2 above ground
    land_z = gz + 0.062
    fall_t = math.sqrt(max(2.0 * (hand.z - land_z) / FALL_G, 0.01))
    nfall = int(math.ceil(fall_t * 30.0))
    af0, af1 = fd, fd + nfall
    for k, ob in enumerate(Tk.saus.cards):
        ob['airborne_frames'] = '%d:%d' % (af0, af1 - 1)
    for i in sorted(set(list(idx) + list(range(-HANDLE, Tk.n + 1)))):
        f = Tk.bf(i); Tk.scene.frame_set(f)
        cam = Tk.cam.matrix_world.translation
        if i < I_DROP:
            Tk.saus.root.location = (cx, cy, land_z); vis = None
        else:
            t = (f - fd) / 30.0
            z = max(land_z, hand.z - 0.5 * FALL_G * t * t) if f < af1 else land_z
            Tk.saus.root.location = (cx + 0.12 * min(t, fall_t), cy, z); vis = int(((f - fd) * 1.3 + 4) % 12) if f < af1 else 0
        yaw = math.atan2(cam.x - cx, -(cam.y - cy))
        Tk.saus.root.rotation_euler = (0, 0, yaw)
        Tk.saus.root.keyframe_insert('location', frame=f); Tk.saus.root.keyframe_insert('rotation_euler', frame=f)
        for k, ob in enumerate(Tk.saus.cards):
            ob.hide_render = (vis is None) or (k != vis); ob.keyframe_insert('hide_render', frame=f)
    for fc in _fcs(Tk.saus.root): 
        for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'

def _fcs(ob):
    ad = ob.animation_data
    if not ad or not ad.action: return []
    try: return list(ad.action.fcurves)
    except AttributeError:
        out = []
        for l in ad.action.layers:
            for st in l.strips:
                for cb in st.channelbags: out += list(cb.fcurves)
        return out

if __name__ == '__main__':
    C.cli(make_take, specs_of, state_of, G0 - HANDLE, HANDLE, G_OF, post_fn=post_fn)

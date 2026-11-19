"""c18.py -- film-18 take helper (render team 1): per-frame animated cast18 cards on the set3d18 jimo set. Copy of this file lives in every take folder.
Usage in shot.py:  import c18 as C ; C.run(shot, actors_fn, g0, g1, hb, ha, ...)   (actors_fn(f, cam, ctx) puts cards for film frame f)"""
import os, sys, math, json, time, random, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.dirname(os.path.dirname(HERE)); SET = os.path.join(V3, 'set3d18')
if SET not in sys.path: sys.path.insert(0, SET)
import jimo as J, jimo_shots as S, jimo_r2 as R2, jimo_cards as CD
import bpy
from mathutils import Vector as V
T = J.T; MN = J.MN; STATE = J.STATE
HEIGHT = J.HEIGHT
_SIDE = {}

def ox_card(shot_key, i, pos, travel_deg, scale, camloc, state='dragon', view='three_quarter', gait='stand', phase=0, flame=-1, blades=True, theta=36,
            bob=0.0, roll=0.0, tint=None, k=None, reed=0):
    """An ox card at pos; yaw ~theta deg off the camera axis, mirrored so the head points along travel_deg. (sgn, mirror) chosen once per ox so it never pops."""
    p = V(pos); sc = scale * 1.08
    dvec = V((math.cos(math.radians(travel_deg)), math.sin(math.radians(travel_deg)), 0.0)); c = camloc - p; c.z = 0.0; c.normalize()
    def nu(sgn):
        a = math.radians(sgn * theta); n = V((c.x * math.cos(a) - c.y * math.sin(a), c.x * math.sin(a) + c.y * math.cos(a), 0.0)); return n, V((-n.y, n.x, 0.0))
    key = (shot_key, i)
    if key not in _SIDE:
        best = None
        for sgn in (1, -1):
            n, u = nu(sgn)
            for fac in (1, -1):
                s = (u * fac).dot(dvec)
                if best is None or s > best[0]: best = (s, sgn, fac)
        _SIDE[key] = best[1:]
    sgn, fac = _SIDE[key]; n, u = nu(sgn)
    yaw = math.degrees(math.atan2(n.x, -n.y))
    meta = card_ox(state, view, gait, phase, flame, blades, reed)
    ob = R2.put_card(meta, (p.x, p.y, p.z + bob), yaw, sc, mirror=(fac < 0), name='ox%d' % i, tint=tint, k=k, sw=2.7 * sc)
    if roll: ob.rotation_euler = (0, math.radians(roll), math.radians(yaw))
    return ob

def card_ox(state, view, gait, phase, flame, blades, reed=0):
    key = 'oxv_%s_%s_%s_%d_%d_%d_%d' % (state, view, gait, phase if gait != 'stand' else 0, flame, int(blades), reed); name = hashlib.md5(key.encode()).hexdigest()[:10] + '_oxv'
    mp = os.path.join(CD.CARDS, name + '.json')
    if os.path.exists(mp) and os.path.exists(os.path.join(CD.CARDS, name + '.png')): return json.load(open(mp))
    cast, P = CD._cast()
    f = cast.ox_figure(state=state, view=view, gait=gait, phase=(phase if gait != 'stand' else 0) / 8.0, flame=flame, blades=blades, reed=(True if reed else None), uid='c%s' % name[:6])
    m = CD._write(f['svg'], f['bbox'], 0.0, CD.PXD_O, name); m['kind'] = 'ox'; json.dump(m, open(mp, 'w')); return m

def person_card(role, pose, pos, camloc, i=0, h=None, bob=0.0, roll=0.0, sx=1.0, sz=1.0, mirror=False, tint=None, k=None, yaw_off=0.0):
    p = V(pos); meta = CD.card('person', pose=pose); h = h or HEIGHT.get(role, 3.0); sc = h / meta['height']
    d = camloc - p; yaw = math.degrees(math.atan2(d.x, -d.y)) + yaw_off
    ob = R2.put_card(meta, (p.x, p.y, p.z + bob), yaw, sc, mirror=mirror, name='%s%d' % (role, i), tint=tint, k=k, sw=0.9 * h / 3.0)
    ob.rotation_euler = (0, math.radians(roll), math.radians(yaw)); ob.scale = ((-1.0 if mirror else 1.0) * sx, 1.0, sz)
    return ob

def sway(f, i, amp=1.5, hz=0.7): return amp * math.sin(2 * math.pi * hz * f / 30.0 + i * 1.7)
def hop(f, i, amp=0.06, hz=3.0): return amp * abs(math.sin(math.pi * hz * f / 30.0 + i))

def shake(cam, amp, f0, f1):
    """Hand-held feel: small deterministic rotation noise (rad) on the keyed camera, 2.3 + 4.1 Hz sinusoids per axis."""
    for fc in T._fcurves(cam):
        if fc.data_path != 'rotation_euler': continue
        for kp in fc.keyframe_points:
            f = kp.co[0]; a = fc.array_index
            kp.co[1] += amp * (0.6 * math.sin(2 * math.pi * 2.3 * f / 30.0 + 1.9 * a) + 0.4 * math.sin(2 * math.pi * 4.1 * f / 30.0 + 0.7 + 2.3 * a)) * (1.0 if a != 1 else 0.5)
            kp.handle_left[1] = kp.handle_right[1] = kp.co[1]

def run(shot, actors_fn, g0, g1, hb=0, ha=0, quality=None, outdir=None, tweak=None, state=None, ctx=None, only=None, shk=0.0):
    quality = quality or os.environ.get('Q', 'final'); outdir = outdir or os.path.join(HERE, 'raw' if quality == 'final' else 'draft'); os.makedirs(outdir, exist_ok=True)
    if tweak: tweak('pre')
    A = J.build(None, shot); sc = bpy.context.scene; MN.setup_render(sc, quality); sc.render.threads = 2
    J.apply_state(S.SHOTS[shot]['state'] if state is None else state)
    if tweak: tweak('post', A)
    cam0 = J.key_camera(shot)
    if shk: shake(cam0, shk, g0, g1)
    first, last = g0 - hb, g1 - 1 + ha
    for f in range(first, last + 1): J.flicker(f)
    frames = list(range(first, last + 1))
    if os.environ.get('FRAMES'): only = [int(x) for x in os.environ['FRAMES'].split(',')]
    if only: frames = [f for f in frames if f in only]
    cam = sc.camera; log = []
    for f in frames:
        path = os.path.join(outdir, 'g_%04d.png' % f)
        if os.path.exists(path): continue
        sc.frame_set(f); bpy.context.view_layer.update()
        R2.clear_placeholders(); R2.LIT.clear()
        cl = cam.matrix_world.translation.copy()
        actors_fn(f, cl, ctx)
        bpy.context.view_layer.update()
        w, c = T.render(path); log.append(w); print('g%d %.1fs' % (f, w), flush=True)
    return log

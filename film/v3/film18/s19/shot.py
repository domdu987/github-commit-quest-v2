#!/usr/bin/env python3
"""s19 (frames 1427-1514): oxen burst out of the holes (dust puffs), tails lit, gallop across the field; dark Qi soldiers behind; WHIP pan at the end.  jimo_out NIGHT.
python3 shot.py draft|final [first_g last_g] [out]"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C
from c18 import J, S, R2, V, bpy
SHOT = 's19'; G0, G1 = 1427, 1514; H_IN, H_OUT = 6, 6        # cut in, whip out
c = S.SHOTS[SHOT]['cam']; c['loc'] = (14.2, -15.5, 1.5); c['look_at'] = (32.0, -6.0, 5.6); c['lens'] = 18.0
C.motion(SHOT, push=0.0, slide=-30, moves=[dict(t=0.2, d=0.9, dur=8), dict(t=0.35, d=0.9, dur=8), dict(t=0.84, pan=-85, dur=7)])
_p0 = S.pose_at
def _tilt(sh, t):                                            # the whip lands on the herd: tilt down from the sky onto the field while the pan runs
    p = _p0(sh, t); k = min(1.0, max(0.0, (t - 0.82) / 0.10)); k = k * k * (3 - 2 * k)
    la = list(p['look_at']); la[2] = la[2] + (3.0 - la[2]) * k; sw = 2.4 * math.sin(t * 21.0) * (1.0 - k)
    p['loc'] = (p['loc'][0] + sw, p['loc'][1] + 0.4 * sw, p['loc'][2]); la[0] += sw; p['look_at'] = tuple(la); return p
S.pose_at = _tilt
HIDE = tuple(os.environ.get('HIDE', 'furrows,streaks,streak,rainstreaks,tufts').split(','))
HX0 = [hx for hx in J.HOLE_X if hx > 20]
HX = [HX0[1], HX0[2], HX0[3]]
rnd = random.Random(19)
OX = []                                                      # (gs, hole x, lane jitter, scale)
for w in range(6):
    for k, hx in enumerate(HX):
        OX.append((G0 - 26 + 9 * k + 18 * w, hx + rnd.uniform(-0.5, 0.5), rnd.uniform(-0.3, 0.3), rnd.uniform(0.95, 1.05)))
OX = OX[:60]
QI = [(G0 - 10 + 5 * k, HX0[(k * 3) % 4] + rnd.uniform(-1.5, 1.5)) for k in range(6)]
V_OX, V_QI = 15.0, 11.5

def setup(ctx):
    J.set_holes(12)
    for ob in bpy.data.objects:
        if ob.type == 'MESH' and ob.name in ('wall', 'merlons', 'shields', 'patches', 'putlog', 'tower', 'wood', 'posts', 'halos', 'roof', 'citybody', 'cityroof'): ob.visible_shadow = False
    import bmesh
    for ob in [o for o in bpy.data.objects if o.type == 'MESH' and (o.name == 'halos' or o.name.startswith('breach'))]:
        bm = bmesh.new(); bm.from_mesh(ob.data); mi = [i for i, m in enumerate(ob.data.materials) if m is not None and ('mist' in m.name or 'dust' in m.name)]
        bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.material_index in mi], context='FACES'); bm.to_mesh(ob.data); bm.free()
    Mt = J.STATE['M']; tun = Mt.get('tunnel'); bank = Mt.get('bank')
    if tun is not None and bank is not None:
        for ob in bpy.data.objects:
            if ob.type == 'MESH':
                for i_, m_ in enumerate(ob.data.materials):
                    if m_ is tun and ob.name == 'furrows': ob.data.materials[i_] = bank
    gd = bpy.data.objects['ground'].data; gm = gd.materials[-1]
    me = bpy.data.meshes.new('mygap'); me.from_pydata([(-30, -60, 0.06), (90, -60, 0.06), (90, -7, 0.06), (-30, -7, 0.06)], [], [(0, 1, 2, 3), (3, 2, 1, 0)]); me.update()
    uv = me.uv_layers.new(name='UVMap')
    for i_, c_ in enumerate(((0, 0), (6, 0), (6, 3), (0, 3), (0, 3), (6, 3), (6, 0), (0, 0))): uv.data[i_].uv = c_
    me.materials.append(Mt.get('bank') or gm); go = bpy.data.objects.new('mygap', me); J.STATE['SET'].objects.link(go)

FGP = []
def frame(g, t, camloc, ctx):
    J.set_holes(12)
    if not FGP:                                   # warm foreground props (pots, a helmet) low in frame, parented to nothing: placed in the world near the camera path
        for i, (wx, wy, kind) in enumerate(((17.6, -13.2, 'pot'), (19.8, -14.8, 'jar'), (16.6, -10.6, 'pot'), (21.0, -16.6, 'pot'), (24.2, -17.4, 'jar'), (18.6, -8.4, 'bowl'), (27.5, -11.0, 'pot'), (23.6, -15.4, 'pot'))):
            FGP.append(J.prop_pot((wx, wy, 0.0), 0.6 * i, kind=kind, scale=0.85, cd=8))
        for (lx, ly) in ((19.0, -13.0), (22.5, -13.8)):
            ld = bpy.data.lights.new('potl', 'POINT'); ld.color = J.FIRE; ld.energy = 650.0; ld.shadow_soft_size = 0.6; ld.use_shadow = False
            lo = bpy.data.objects.new('potl', ld); J.STATE['LIGHTS'].objects.link(lo); lo.location = (lx, ly, 1.0); lo.visible_camera = False
        FGP.append(J.prop_helmet((23.4, -9.6, 0.0), 2.4, scale=1.0, cd=8))
    for ob in bpy.data.objects:
        if ob.name in HIDE or ob.name.startswith(('rubble', 'hglow')): ob.hide_render = True
    for ob in bpy.data.objects:
        if ob.name.startswith('hglow'): ob.hide_render = True
    for j, (gs, hx, jit, sc) in enumerate(OX):
        if g < gs: continue
        y = 4.0 - V_OX * (g - gs) / 30.0
        if y < -150: continue
        pos = (hx + jit, y, 0.0); near = (V(pos) - camloc).length < 16
        ph = int((g - gs) * 12 / 30.0 + j) % 8
        C.put_ox(j, pos, -100, sc, camloc, phase=ph, flame=C.flame_for(g, j), state='dragon', view='front_three_quarter' if (near and j % 3 == 0) else 'three_quarter', gait='gallop', theta=14 if (near and j % 3 == 0) else 30, reed=True, tfx=(1.0 if (V(pos) - camloc).length < 20 else 0.8), lean=84.0, face='rage')
    for j, (gs, x) in enumerate(QI):
        if g < gs: continue
        y = -7.0 - V_QI * (g - gs) / 30.0
        m = C.qi((g - gs) * 12 / 30.0 / 8.0 + j * 0.13, 1)
        C.put_person(m, (x, y, 0), camloc, 3.1, 'qi%d' % j, mirror=(j % 2 == 0), tint=(0.5, 0.5, 0.75), k=0.8)
    for k, hx in enumerate(HX):                              # dust puffs at the hole mouths, growing and fading after the first ox of the hole bursts out
        gs = min(o[0] for o in OX if abs(o[1] - hx) < 1.0); a = g - (gs + 8)
        for q in range(3):
            aq = a - 5 * q
            if aq < 0 or aq > 40: continue
            if os.environ.get('NOPUFF') != '1': C.put_puff((hx + (q - 1) * 1.6, -5.5 - 0.15 * aq, 0.8 + 0.07 * aq), 2.5 + 0.12 * aq, camloc, alpha=(0.55, 0.4, 0.25)[min(2, aq // 14)], name='pf%d_%d' % (k, q))

if __name__ == '__main__':
    KEEP = [(hx + dx, y, 3.2) for hx in (24.5, 30.0, 35.5, 41.0) for dx in (0,) for y in range(-6, -120, -6)]
    C.run(SHOT, G0 - H_IN, G1 + H_OUT, frame, setup, sys.argv[1:], keep=KEEP)

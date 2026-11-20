#!/usr/bin/env python3
"""s19 (frames 1427-1514): oxen burst out of the holes (dust puffs), tails lit, gallop across the field; dark Qi soldiers behind; WHIP pan at the end.  jimo_out NIGHT.
python3 shot.py draft|final [first_g last_g] [out]"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C
from c18 import J, S, R2, V, bpy
SHOT = 's19'; G0, G1 = 1427, 1514; H_IN, H_OUT = 6, 6        # cut in, whip out
c = S.SHOTS[SHOT]['cam']; c['loc'] = (30.2, -26.0, 1.7); c['look_at'] = (30.0, -2.0, 2.0); c['lens'] = 22.0
C.motion(SHOT, push=0.0, slide=-30, moves=[dict(t=0.2, d=0.9, dur=8), dict(t=0.35, d=0.9, dur=8), dict(t=0.84, pan=-85, dur=7)])
_p0 = S.pose_at
def _tilt(sh, t):                                            # the whip lands on the herd: tilt down from the sky onto the field while the pan runs
    p = _p0(sh, t); k = min(1.0, max(0.0, (t - 0.82) / 0.10)); k = k * k * (3 - 2 * k)
    la = list(p['look_at']); la[2] = la[2] + (3.0 - la[2]) * k; sw = 2.4 * math.sin(t * 21.0) * (1.0 - k)
    p['loc'] = (p['loc'][0] + sw, p['loc'][1] + 0.4 * sw, p['loc'][2]); la[0] += sw; p['look_at'] = tuple(la); return p
S.pose_at = _tilt
HIDE = tuple(os.environ.get('HIDE', 'furrows,streaks,streak,rainstreaks,tufts').split(','))
HX0 = [hx for hx in J.HOLE_X if hx > 20]
HX = [HX0[0], HX0[1], HX0[2]]
rnd = random.Random(19)
OX = []                                                      # (gs, hole x, lane jitter, scale)
for w in range(5):
    for k, hx in enumerate(HX):
        OX.append((G0 - 24 + 8 * k + 24 * w + (4 if k == 1 else 0), hx + rnd.uniform(-0.5, 0.5), rnd.uniform(-0.3, 0.3), rnd.uniform(0.95, 1.05)))
OX = OX[:60]
QI = [(G0 - 6 + 9 * k, (19.0, 41.0)[k % 2]) for k in range(8)]
V_OX, V_QI = 9.0, 7.0
FAR = [(G0 - 30 + 5 * k + 2, 64 + 3.5 * (k % 4), (-0.4, 0.4, 0.0, 0.2)[k % 4]) for k in range(18)]  # far lanes 8-14 D behind the near lane, head-on / 3/4 toward the camera

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
        for (lx, ly) in ((27.0, -20.0), (33.5, -20.0)):
            ld = bpy.data.lights.new('potl', 'POINT'); ld.color = J.FIRE; ld.energy = 650.0; ld.shadow_soft_size = 0.6; ld.use_shadow = False
            lo = bpy.data.objects.new('potl', ld); J.STATE['LIGHTS'].objects.link(lo); lo.location = (lx, ly, 1.0); lo.visible_camera = False
        rr_ = random.Random(7)
        for i in range(75):                                   # round 16: dark rubble / pots on the ground between the oxen's end of run (y -13) and the camera, low in frame
            wx, wy = rr_.uniform(22.5, 38.0), rr_.uniform(-24.5, -14.8)
            corner = abs(wx - 30.0) > 4.5
            if rr_.random() < 0.5: FGP.append(J.prop_reed_bundle((wx, wy, 0.2), (0, 0, rr_.uniform(0, 6.28)), scale=rr_.uniform(0.35, 0.55), n=30, cd=8.0))
            else: FGP.append(J.prop_pot((wx, wy, 0.0), rr_.uniform(0, 6.28), kind=rr_.choice(('pot', 'jar', 'bowl')), scale=rr_.uniform(0.35, 0.38 if not corner else 0.55), cd=8))
    for ob in bpy.data.objects:
        if ob.name in HIDE or ob.name.startswith(('rubble', 'hglow')): ob.hide_render = True
    for ob in bpy.data.objects:
        if ob.name.startswith('hglow'): ob.hide_render = True
    for j, (gs, hx, jit, sc) in enumerate(OX):
        if g < gs: continue
        y = 4.0 - V_OX * (g - gs) / 30.0
        if y < -13.0: continue
        pos = (hx + jit, y, 0.0); near = True
        ph = int((g - gs) * 12 / 30.0 + j) % 8
        C.put_ox(j, pos, -100, sc, camloc, phase=ph, flame=C.flame_for(g, j), state='dragon', view='front_three_quarter', gait='gallop', theta=(6, 12, 9)[j % 3], reed=True, tfx=0.4, lean=60.0, face='rage')
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

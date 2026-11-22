#!/usr/bin/env python3
"""V2 fixes applied to a take's c18.py (idempotent): python3 patch_v2.py sNN
 1. gcheck mode (patch_gcheck.py)   2. NOPOOL env (no warm light pool decal under the flame tip)   3. dark double contact shadow under the hooves (HOOFSHADOW)
 4. BOBCOMP: cancel part of the gallop body bounce (jitter source)."""
import sys, subprocess, os
d = sys.argv[1]; p = d + '/c18.py'
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'patch_gcheck.py'), d], check=True)
t = open(p).read()
if 'HOOFSHADOW' in t: sys.exit(0)
a = "    ob = R2.put_card(meta, tuple(p), yaw, sc, mirror=mir, name='ox%d' % i, tint=tint, k=k, sw=2.7 * sc)\n"
k = t.rindex(a)
b = """    comp = 0.0
    if gait == 'gallop' and float(os.environ.get('BOBCOMP', '0.6')) > 0:       # V2 jitter fix: cancel most of the gallop's body bounce (the head anchor's phase variation)
        _hy = [anchor_of('head', state, view, gait, q_)[1] for q_ in range(8)]; comp = float(os.environ.get('BOBCOMP', '0.6')) * (_hy[ph] - sum(_hy) / 8.0) * sc
    ob = R2.put_card(meta, (p.x, p.y, p.z + comp), yaw, sc, mirror=mir, name='ox%d' % i, tint=tint, k=k, sw=2.7 * sc)
    for o_ in bpy.data.objects:
        if o_.name == 'ph_sh_ox%d' % i: o_.location.z = p.z
    if os.environ.get('HOOFSHADOW', '1') == '1':                      # V2 fix: dark contact shadow right under the hooves (centred on the card's feet, stacked twice)
        ly_ = math.radians(yaw); rgt = V((math.cos(ly_), math.sin(ly_), 0.0)); cxm = (-1.0 if mir else 1.0) * (meta['x0'] + 0.5 * meta['w']) * sc
        for q_ in range(2):
            sm_ = R2._shadow_quad('chs_%d' % q_, 1.0, 0.5)
            if not sm_.materials: sm_.materials.append(R2._card_mat(R2._shadow_png(), (1, 1, 1), 0.0, 'shadow'))
            so_ = bpy.data.objects.new('ph_sh_hoof%d_%d' % (i, q_), sm_); STATE['SET'].objects.link(so_)
            so_.location = (p.x + rgt.x * cxm, p.y + rgt.y * cxm, p.z + 0.002 * q_); so_.rotation_euler = (0, 0, ly_)
            so_.scale = (0.46 * meta['w'] * sc, 0.46 * meta['w'] * sc * 0.45, 1.0); so_.visible_shadow = False; J.no_bounce(so_); so_['placeholder'] = 1
"""
t = t[:k] + b + t[k + len(a):]
t = t.replace("tail = p + right * lx + V((0, 0, lz)); TAILS.append((tail, sc))", "tail = p + right * lx + V((0, 0, lz + comp)); TAILS.append((tail, sc))")
t = t.replace("    for (t, sc) in TAILS:\n        sm = R2._shadow_quad('cpool', 1.0, 1.0)", "    for (t, sc) in (TAILS if os.environ.get('NOPOOL', '0') != '1' else []):\n        sm = R2._shadow_quad('cpool', 1.0, 1.0)")
open(p, 'w').write(t)

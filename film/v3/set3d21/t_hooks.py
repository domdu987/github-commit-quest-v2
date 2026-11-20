#!/usr/bin/env python3
"""hook test: builds camp_table and checks that every per-frame hook really moves values (mesh vertices, node values, rotations, object counts). Prints `ok N bad []`."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, bpy
import stirling as K
bad = []; n = 0
def chk(name, cond):
    global n; n += 1
    if not cond: bad.append(name)
def verts(ob):
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get(); e = ob.evaluated_get(dg); m = e.to_mesh(); W = np.array(ob.matrix_world); v = np.array([p.co[:] for p in m.vertices]); e.to_mesh_clear(); return v @ W[:3, :3].T + W[:3, 3]
A = K.build_for_cli('camp_table'); K.setup_render(bpy.context.scene, 'draft')
# banner flutter: the evaluated cloth vertices differ between two times
fl = K.STATE['anim']['flags']; chk('flags exist', len(fl) > 0); ob = bpy.data.objects[fl[0][0]]
K.set_flutter(0.0); v0 = verts(ob); K.set_flutter(0.37); v1 = verts(ob); chk('flutter moves cloth', float(np.abs(v0 - v1).max()) > 1e-3)
K.set_flutter(0.37, amp=0.0); v2 = verts(ob); chk('flutter amp 0 is flat', float(np.abs(v2 - verts(ob)).max()) < 1e-9 and float(np.abs(v2 - v1).max()) > 1e-3)
# smoke
sm = K.STATE['anim'].get('smoke', []); chk('smoke columns exist', len(sm) > 0)
so = bpy.data.objects[sm[0]['ob']]; K.set_smoke(0.0); a = np.array([p.co[:] for p in so.data.vertices]); K.set_smoke(2.5); b = np.array([p.co[:] for p in so.data.vertices]); chk('smoke moves', float(np.abs(a - b).max()) > 0.2)
# water flow + glitter
nt = K.get_mat('water').node_tree; K.set_flow(0.0); f0 = (nt.nodes['flow_off'].inputs['Location'].default_value[0], nt.nodes['glit_vor'].inputs['W'].default_value); K.set_flow(1.5); f1 = (nt.nodes['flow_off'].inputs['Location'].default_value[0], nt.nodes['glit_vor'].inputs['W'].default_value)
chk('flow offset moves', f0[0] != f1[0]); chk('glitter phase moves', f0[1] != f1[1])
# coin scale + chest lid
be = bpy.data.objects[A['scale_beam']]; K.set_scale_tip(A, 0.0); r0 = be.rotation_euler[1]; K.set_scale_tip(A, 12.0); chk('scale tips', abs(be.rotation_euler[1] - r0) > 0.1); bv0 = verts(be); K.set_scale_tip(A, -12.0); chk('scale beam mesh moves', float(np.abs(verts(be) - bv0).max()) > 0.01)
lid = bpy.data.objects[A['chest_lid']]; K.set_chest_lid(A, 72.0); l0 = lid.rotation_euler[0]; K.set_chest_lid(A, 0.0); chk('lid closes', abs(lid.rotation_euler[0] - l0) > 1.0); lv0 = verts(lid); K.set_chest_lid(A, 72.0); chk('lid mesh moves', float(np.abs(verts(lid) - lv0).max()) > 0.1)
# splash: grows then falls then disappears; same name replaces
c1 = K.splash(-34.0, 41.0, 0.3, name='t'); h1 = max(verts(o)[:, 2].max() for o in bpy.data.objects if o.name.startswith('splash_t_')); c2 = K.splash(-34.0, 41.0, 0.75, name='t')
h2 = max(verts(o)[:, 2].max() for o in bpy.data.objects if o.name.startswith('splash_t_')); chk('splash has parts', c1 > 0 and c2 > 0); chk('splash height changes', abs(h1 - h2) > 0.02); chk('splash replaces, not stacks', len([o for o in bpy.data.objects if o.name.startswith('splash_t_')]) == c2)
chk('splash droplets present', any('glow_spray' in o.name and len(o.data.polygons) > 100 for o in bpy.data.objects if o.name.startswith('splash_t_'))); chk('splash gone late', K.splash(-34.0, 41.0, 2.0, name='t') == 0 and not [o for o in bpy.data.objects if o.name.startswith('splash_t_')])
# troops by count
got = []; i4 = K.place_troops(A, 'bridge', 4, seed=1); i10 = K.place_troops(A, 'bridge', 10, seed=1); chk('bridge count', len(i4) == 4 and len(i10) == 10)
nb = sum(len(o.data.polygons) for o in bpy.data.objects if o.name.startswith('troops_bridge')); K.place_troops(A, 'bridge', 2, seed=1); chk('bridge horses scale with count', nb > sum(len(o.data.polygons) for o in bpy.data.objects if o.name.startswith('troops_bridge')))
chk('causeway count', len(K.place_troops(A, 'causeway', 7)) == 7 and len(K.place_troops(A, 'causeway', 15)) == 15); chk('meadow count', len(K.place_troops(A, 'meadow', 40)) == 40)
K.place_troops(A, 'meadow', 25, cb=got.extend); chk('callback gets the stand points', len(got) == 25 and len(got[0]) == 5)
print('ok', n, 'bad', bad)
sys.exit(1 if bad else 0)

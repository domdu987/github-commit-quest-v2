"""Hook test for desert.py: keys every hook, checks the evaluated values at frames, renders one 360x640 still per hook state to
hooks/ and hooks.jpg.  usage: python3 t_anim.py [norender]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import bpy, desert as D
ok = True
def check(name, got, want, tol=1e-3):
    global ok
    good = abs(got - want) <= tol; ok &= good; print('%-44s %8.4f  want %8.4f  %s' % (name, got, want, 'OK' if good else 'FAIL'))
sc = bpy.context.scene
A = D.build('desert_ice', 'channel_ecu')
D.clear_keys()
D.set_ice('water', frame=1); D.set_ice('thin', frame=20); D.set_ice('thick', frame=40); D.set_ice('mud', frame=60)
for f, (lv, ml) in ((1, (0, 0)), (20, (0.25, 0)), (40, (1, 0)), (60, (1, 1))):
    sc.frame_set(f); M = D.STATE['M']
    check('ice_k @%d' % f, M['ice'].node_tree.nodes['ice_k'].outputs[0].default_value, lv)
    check('mud_k @%d' % f, M['mud'].node_tree.nodes['mud_k'].outputs[0].default_value, ml)
sc.frame_set(30); check('ice_k eased @30 (linear)', D.STATE['M']['ice'].node_tree.nodes['ice_k'].outputs[0].default_value, 0.625)
sc.frame_set(40); check('cut-face scale z @40 (thick)', D.STATE['ice']['hole'].scale.z, 0.185)
D.set_heat_wisps(0.0, frame=1); D.set_heat_wisps(1.0, frame=30)
sc.frame_set(30); check('wisp_k @30', D.STATE['M']['wisp'].node_tree.nodes['wisp_k'].outputs[0].default_value, 0.22)
check('wisp scroll y @30', D.STATE['M']['wisp'].node_tree.nodes['scroll'].inputs['Location'].default_value[1], -0.36)
for f in (1, 2, 3): D.set_flames(1.0, frame=f); D.set_stars(1.0, 0.4, frame=f)
sc.frame_set(2); L0, b0 = D.STATE['flames'][0]; check('flame energy @2 = base x flick', L0.data.energy, b0 * D._flick(2, 1), 1e-2)
sc.frame_set(3); check('star twinkle W @3', D.STATE['M']['sky'].node_tree.nodes['twinkle'].inputs['W'].default_value, 0.33)
print('ALL OK' if ok else 'SOME FAIL')
if len(sys.argv) > 1 and sys.argv[1] == 'norender': sys.exit(0)
out = os.path.join(HERE, 'hooks'); os.makedirs(out, exist_ok=True); fs = []
for tag, st in (('water', 'water'), ('thin', 'thin'), ('half', 0.55), ('thick', 'thick'), ('melting', (1.0, 0.5)), ('mud', 'mud')):
    D.build('desert_ice', 'channel_ecu', light='NIGHT' if tag != 'mud' and tag != 'melting' else 'NOON'); D.clear_keys()
    if isinstance(st, tuple): D.set_ice(st[0], melt=st[1])
    else: D.set_ice(st)
    D.setup_render(sc, 'preview'); D.make_camera(D.CAMS['plain']['channel_ecu']); p = os.path.join(out, 'ice_%s.png' % tag); D.render(p); fs.append(p)
for lv in (0.0, 1.0, 1.5):
    D.build('desert_ice', 'sky_reveal'); D.clear_keys(); D.set_heat_wisps(lv, frame=1); sc.frame_set(1)
    D.setup_render(sc, 'preview'); D.make_camera(D.CAMS['plain']['sky_reveal']); p = os.path.join(out, 'wisps_%g.png' % lv); D.render(p); fs.append(p)
os.system('cd %s && COLS=9 python3 sheet.py hooks.jpg %s' % (HERE, ' '.join(fs)))

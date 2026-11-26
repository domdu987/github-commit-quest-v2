"""anim_test.py : keyed crack glow + flash in the vault (BURN), keyframes checked by rendering frames 1, 6, 10 at preview size."""
import sys, os, bpy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import vault as V, smallkit as K
A = V.build('BURN'); sc = bpy.context.scene; K.setup_render(sc, 'preview'); V.make_camera(A['cams']['crack_follow'])
V.set_crack_glow(0.0, frame=1); V.set_crack_glow(1.0, frame=10)
V.flash(0.0, 1); V.flash(1.2, 6); V.flash(0.0, 10)
for f in (1, 6, 10):
    sc.frame_set(f); K.render(os.path.join(HERE, 'anim_f%02d.png' % f))
    print('frame', f, 'glow', round(V.STATE['crack_ctl']['glow'], 3), 'bevel_end', round(V.STATE['glow_ob'].data.bevel_factor_end, 3), 'energy', round(K.ST['key'].data.energy, 1),
          'flash', round(K.amb_group().nodes['flash'].outputs[0].default_value, 3))

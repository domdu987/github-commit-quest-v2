"""draft.py preset[:LIGHT] [out_dir] [hooks python] : one preview (360x640) tile with placeholder actors, prints cpu seconds. usage: python3 draft.py shop_wide:DAY"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, h19 as H
spec = sys.argv[1]; preset, _, light = spec.partition(':'); out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(H.HERE, 'h19_work', 'draft')
os.makedirs(out, exist_ok=True); hooks = sys.argv[3] if len(sys.argv) > 3 else ''
t0 = time.time(); A = H.build(preset, light=light or None); sc = bpy.context.scene
H.setup_render(sc, os.environ.get('Q', 'preview')); cam = H.make_camera(A['cam']); exec(hooks, dict(H=H, bpy=bpy))
H.stage_placeholders(); bpy.context.view_layer.update(); print('build %.1fs' % (time.time() - t0), 'heads', H.head_pixels())
png = os.path.join(out, '%s_%s.png' % (preset, light or 'def')); w, c = H.render(png); print('render wall %.1f cpu %.1f -> %s' % (w, c, png))

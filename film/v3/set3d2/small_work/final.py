"""final.py set preset cam out.png : one final-quality frame (720x1280, 12 samples, 2 threads) with placeholder actors; prints digest and CPU s."""
import sys, os, bpy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import smallkit as K
setname, preset, cam, out = sys.argv[1:5]; M = __import__(setname)
A = M.build(preset); sc = bpy.context.scene; K.setup_render(sc, 'final'); M.make_camera(A['cams'][cam]); M.stage(A, cam)
w, c = K.render(out); print('FINAL %s %s %s: %.2f s wall, %.2f s cpu, digest %s' % (setname, preset, cam, w, c, K.digest()))

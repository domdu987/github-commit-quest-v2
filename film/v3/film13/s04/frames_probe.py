import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c13 as C
light, state, spec = sys.argv[1], sys.argv[2], json.load(open(sys.argv[3]))
T = C.Take("street_wide", light=light if light!="-" else None, state=state)
T.scene.camera = T.cam
os.makedirs('work/cand', exist_ok=True)
for i,(name,loc,look,lens) in enumerate(spec):
    C.camrig.key_camera(i+1, C.Vector(loc), C.Vector(look), cam=T.cam, lens=lens, interp="LINEAR", easing="AUTO")
    st = T.render([i+1], 'work/cand', scale=0.4, samples=4)[0]
    os.replace(st['path'], 'work/cand/%s.png'%name)

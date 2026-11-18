import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c13 as C
preset = sys.argv[1]; out = sys.argv[2]
T = C.Take(preset, quality="preview", lens=float(sys.argv[3]) if len(sys.argv) > 3 else 22.0)
cam = C.D.CAMS[C.D.PRESETS[preset]['cam']]
T.key_cam(1, cam['loc'], cam['look_at'], lens=cam['lens'])
T.scene.frame_set(1)
os.makedirs(out, exist_ok=True)
st = T.render([1], out, scale=0.5, samples=6)[0]
os.replace(st['path'], os.path.join(out, preset + '.png')); print(st['wall'], st['cpu'])

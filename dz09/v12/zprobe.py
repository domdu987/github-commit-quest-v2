import sys, os, numpy as np, cv2
PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in ("v4/set_expressway", "v11/set"): sys.path.insert(0, os.path.join(PROJ, p))
import render11, post11
o = PROJ + "/v10/film/out/final_720x1280/stills_before/" + sys.argv[1]
out = {k: f"{o}_{k}.exr" for k in ("rgb", "z", "idx", "env")}
rgb, alpha, env, z, idx = render11.load_passes(out, 720, 1280)
lz = np.log(np.clip(z, 0.05, 5000)).astype(np.float32)
n = (np.abs(lz - cv2.medianBlur(lz, 5)) > 0.02).astype(np.float32)
nd = cv2.GaussianBlur(n, (0, 0), 4)
print("noise frac", n.mean(), "dens>0.12:", (nd > 0.12).mean(), ">0.3", (nd > .3).mean())
v = np.dstack([np.clip(lz / 8, 0, 1), nd, idx / 5.0])
cv2.imwrite(PROJ + "/v12/zprobe_%s.png" % sys.argv[1][:3], (np.clip(v, 0, 1) * 255).astype(np.uint8)[::2, ::2])

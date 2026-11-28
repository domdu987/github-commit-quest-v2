import sys, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
import bpy, numpy as np, expressway as X, shafts as SH
from PIL import Image
A = X.build(haze_cards=False)
res = {}
for pre in sys.argv[1].split(","):
    for mode in ("cards", "post"):
        X.setup_render(quality="draft", threads=2, shafts=mode)
        cam = X.use_camera(pre, "9:16", scale=0.5); bpy.context.view_layer.update()
        o = os.path.join(HERE, "review", "out", f"sh_{pre}_{mode}")
        r = X.render_still(o, frame=7, post=False)
        rgb = X._read_exr(r["rgb"])[..., :3] + X._read_exr(r["env"])[..., :3]
        z = X._read_exr(r["z"])[..., 0]
        res[mode] = (rgb, z, r["cpu_render"])
    cones = [ob for ob in bpy.data.objects if ob.get("fx") == "cone"]
    shl = SH.collect(bpy.context.scene, cam, cones)
    S = SH.splat(np.zeros_like(res["post"][0]), res["post"][1], shl)
    D = res["cards"][0] - res["post"][0]
    m = S.sum(-1) > 1e-4
    k = float((D[m] * S[m]).sum() / max((S[m] * S[m]).sum(), 1e-9))
    print(pre, "k", round(k, 3), "cpu cards", res["cards"][2], "post", res["post"][2], "D mean", D.mean(), "S mean", S.mean(), flush=True)
    enc = lambda c: (np.clip(np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(np.clip(c,0,None), 1 / 2.4) - 0.055), 0, 1) * 255).astype(np.uint8)
    im = np.concatenate([enc(res["cards"][0]), enc(res["post"][0] + k * S)], 1)
    Image.fromarray(im).save(os.path.join(HERE, "review", f"shafts_{pre}.png"))

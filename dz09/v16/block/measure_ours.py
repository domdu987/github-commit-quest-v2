"""measure_ours.py -- the same silhouette measures as measure_sheets.py, taken on OUR turnaround renders (ortho camera,
so model heights map linearly to rows) -> out/proportions_ours.json; appended to proportions.md as a check table."""
import os, json
import numpy as np, cv2
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
import importlib.util as iu
sp = iu.spec_from_file_location("ms", os.path.join(HERE, "measure_sheets.py")); MS = iu.module_from_spec(sp); sp.loader.exec_module(MS)
SPEC = {"kong": dict(chin=0.739, sh_top=0.694, cuff=0.470, fist=(0.463, 0.316)), "z_office": dict(chin=0.722, sh_top=0.694, cuff=0.475, fist=(0.456, 0.307))}
res = {}
for kind in ("kong", "z_office"):
    out = {}
    for view in ("front", "side"):
        im = np.asarray(Image.open(os.path.join(HERE, "out", "turn", "%s_%s.png" % (kind, view))).convert("RGB"))
        Hpx = im.shape[0]
        a = im.astype(np.float32) / 255
        bg = np.median(np.concatenate([a[:, :12], a[:, -12:]], 1), 1)[:, None, :]      # per-row background from the borders
        m = (np.abs(a - bg).sum(2) > 0.12).astype(np.uint8)
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8); k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])); m = (lab == k).astype(np.uint8)
        # rows: the camera is orthographic (ortho scale 1.10 H centred on 0.5 H), so the sole row is known exactly
        bot = int(round(Hpx / 2 + 0.5 / 1.10 * Hpx))
        rows = np.nonzero(m[:bot].sum(1) > 2)[0]; top = int(rows[0]); H = bot - top
        row = lambda f: int(round(Hpx / 2 - (f - 0.5) / 1.10 * Hpx))          # model height fraction -> image row (ortho camera)
        def w(y):
            xs = np.nonzero(m[y])[0]; return int(xs[-1] - xs[0]) if len(xs) else 0
        S = SPEC[kind]
        if view == "front":
            out.update(total_px=H, total_over_model_H=round(H / (Hpx / 1.10), 4),
                       head_cube_w=round(w(row(S["chin"]) - 7) / H, 4),
                       hair_w=round(max(w(y) for y in range(top, row(S["chin"] + 0.12))) / H, 4),
                       shoulder_span=round(max(w(y) for y in range(row(S["sh_top"]) + 8, row(S["cuff"]))) / H, 4),
                       hands_span=round(max(w(y) for y in range(row(S["fist"][0]), row(S["fist"][1]))) / H, 4),
                       leg_span_at_shin=round(w(row(0.16)) / H, 4))
            # hair top to chin with the real hair top (the silhouette top) and the model's chin row
            out["hair_top_to_chin"] = round((row(S["chin"]) - top) / H, 4)
        else:
            out.update(head_depth_side=round(w(row(S["chin"]) - 7) / H, 4), foot_len_side=round(max(w(y) for y in range(bot - 10, bot - 1)) / H, 4))
    res[kind] = out
json.dump(res, open(os.path.join(HERE, "out", "proportions_ours.json"), "w"), indent=1)
P = json.load(open(os.path.join(HERE, "out", "proportions.json")))
L = ["", "## Check: the same measures on our turnaround renders (`measure_ours.py`, ortho camera, cream studio)", "",
     "| measure / H | Kong sheet | Kong ours | zombie sheet | zombie ours |", "|---|---|---|---|---|"]
for key, sk in (("hair_top_to_chin", "hair_top_to_chin"), ("head_cube_w", "head_cube_w"), ("hair_w", "hair_w"), ("shoulder_span", "shoulder_span"),
                ("hands_span", "hands_span"), ("leg_span_at_shin", "leg_span_at_shin"), ("head_depth_side", "head_cube_depth_side"), ("foot_len_side", "foot_len_side")):
    L.append("| %s | %.3f | %.3f | %.3f | %.3f |" % (key, P["kong"][sk], res["kong"][key], P["z_office"][sk], res["z_office"][key]))
md = open(os.path.join(HERE, "proportions.md")).read()
if "## Check:" in md: md = md[:md.index("\n## Check:")]
open(os.path.join(HERE, "proportions.md"), "w").write(md.rstrip() + "\n" + "\n".join(L) + "\n")
print(json.dumps(res, indent=1))

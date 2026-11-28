"""measure25.py -- numbers for the 2.5D cast (no rendering except where said).

    python3 measure25.py parallax     # relative screen shift between layers when the camera orbits (720x1280 px)
    python3 measure25.py hue <dirs>   # v3/tools/hue_report rows for our frames (reads the tool, does not edit it)
    python3 measure25.py lines        # ink width / head D: ours vs ref/c f_014
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)


def parallax():
    import bpy
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view
    import orbit_test as ot, stage25 as st
    sc, cam, L = ot.scene_new(1, 720, 1280, rain=False)
    res = {}
    for mode in ("25d", "flat"):
        a = st.Actor25("M" + mode, "kong", mode=mode)
        a.place((0, 0, 0), 0.0)
        pts = {}
        for deg in (-35, -10, 0, 10, 35):
            ot.cam_at(cam, deg)
            bpy.context.view_layer.update()
            f = a.pose(ot.KONG_POSE, camera=cam, view_lock="front")     # same drawing at every angle: pure parallax
            bpy.context.view_layer.update()
            hx, hy = f["anchors"]["head"]
            out = {}
            for slot in (("pack", "torso", "head", "hair", "arm_l", "arm_r") if mode == "25d" else ("flat",)):
                c = a.cards[slot]
                w = c.matrix_world @ Vector((hx, 0, -hy))       # the same drawing point on each card
                p = world_to_camera_view(sc, cam, w)
                out[slot] = (p.x * 720, (1 - p.y) * 1280)
            pts[deg] = out
        res[mode] = pts
        for ob in [a.root] + list(a.root.children_recursive):
            ob.hide_render = True
    # head diameter on screen at 0 deg
    r = {}
    p = res["25d"]
    for deg in (-35, -10, 10, 35):
        r["front-arm vs pack, %+d deg" % deg] = round(p[deg]["arm_l"][0] - p[deg]["pack"][0] - (p[0]["arm_l"][0] - p[0]["pack"][0]), 2)
        r["hair vs torso, %+d deg" % deg] = round(p[deg]["hair"][0] - p[deg]["torso"][0] - (p[0]["hair"][0] - p[0]["torso"][0]), 2)
    r["flat: any two points"] = 0.0
    print(json.dumps(r, indent=1))
    json.dump({"relative_shift_px_720x1280": r, "raw": {m: {str(k): v for k, v in d.items()} for m, d in res.items()}},
              open(os.path.join(HERE, "out", "parallax.json"), "w"), indent=1)


def hue(dirs):
    sys.path.insert(0, os.path.join(PROJ, "v3", "tools"))
    import hue_report as hr
    print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in hr.NAMES) + "   sat  val dark")
    for d in dirs:
        hr.row(os.path.basename(d.rstrip("/")), hr.files_of(d))
    print("target band: " + ", ".join(f"{k} {lo}-{hi}" for k, (lo, hi) in hr.TARGET.items()))


def lines():
    import draw25d
    import numpy as np
    from PIL import Image
    a = np.asarray(Image.open(os.path.join(PROJ, "ref", "c", "frames2", "f_014.png")).convert("L")).astype(int)
    def runs(v, x0):
        d = np.where(v < 80)[0]
        out, s, p = [], d[0], d[0]
        for x in d[1:]:
            if x != p + 1:
                out.append((int(s + x0), int(p - s + 1)))
                s = x
            p = x
        out.append((int(s + x0), int(p - s + 1)))
        return out
    r_right = runs(a[605, 240:400], 240)[-1]
    top = runs(a[520:700, 320], 520)
    D = r_right[0] + r_right[1] - 255
    print(json.dumps({"ref_f014_head_D_px": D, "ref_head_ink_right_D": round(r_right[1] / D, 3),
                      "ref_head_ink_top_D": round(top[1][1] / D, 3),
                      "ours_head_ink_D": draw25d.LW_HEAD, "ours_body_ink_D": draw25d.LW}, indent=1))


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "parallax":
        parallax()
    elif c == "hue":
        hue(sys.argv[2:])
    elif c == "lines":
        lines()

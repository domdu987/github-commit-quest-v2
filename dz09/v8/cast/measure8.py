"""measure8.py -- re-measure the sheet proportions on our renders.

python3 measure8.py [kong,crew,driver]   -> out/measure/<name>_front.png (beauty), <name>_id.png (layer IDs),
                                            out/measure.json, out/measure_table.md

Each character is rendered in Cycles, front drawing, orthographic camera, neutral light, twice: the beauty pass
and an ID pass (every layer card re-shaded as a flat emission colour, alpha-cut by its sprite).  From the ID render:
total height (silhouette top to sole), bare head D (mean of a circle fit on the lower head contour and the widest
head row, as the sheet measurement did), hair top / width / extent, chin, crotch (first opaque row above the gap
between the legs at the body centre), shoulder span (torso + arms) and shoulder + pack span.  Parts inside one
layer (boot top, glove width, trouser-leg width, head outline) are measured on the layer's sprite by its drawn
palette, mapped through the same card transform.
Bands: spec/sheet_proportions.md (target +/- 6 %).  Crew is compared with James, the driver with Khun Tos.
"""
import os, sys, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "out", "measure")
SHEET = json.load(open(os.path.join(PROJ, "spec", "sheet_measure", "sheet_measure.json")))
REF = {"kong": "kong", "crew": "james", "driver": "tos"}
KEYS = [("head_over_total", "bare head D / total"), ("head_with_hair_over_total", "hair top to chin / total"),
        ("heads_tall", "figure height in bare heads"), ("hair_above_skull_over_D", "hair above skull / D"),
        ("hair_extent_over_D", "hair vertical extent / D"), ("hair_w_over_D", "hair width / D"),
        ("shoulder_over_D", "shoulder width / D"), ("backpack_span_over_D", "shoulders + pack / D"),
        ("torso_over_total", "torso chin-crotch / total"), ("torso_over_D", "torso / D"),
        ("leg_over_total", "legs crotch-sole / total"), ("leg_over_D", "legs / D"), ("leg_w_over_D", "trouser leg width / D"),
        ("hand_w_over_D", "hand width / D"), ("boot_h_over_D", "boot/shoe height / D"), ("outline_over_D", "head outline median / D")]
IDCOL = {"pack": (1, 0, 0), "torso": (0, 1, 0), "head": (0, 0, 1), "face": (1, 1, 0), "hair": (1, 0, 1), "leg_R": (0, 1, 1),
         "leg_L": (0.5, 0.5, 1), "arm_R": (1, 0.5, 0), "arm_L": (0.5, 0, 1), "prop_R": (0.3, 0.3, 0.3), "prop_L": (0.6, 0.6, 0.6)}


def render_pair(name, spec, H_px=1100):
    import bpy, neutral8 as N, stage8 as S
    N.reset()
    L = N.build(res=(800, 1200), samples=32, rim=False)
    a = S.Actor8(name, spec, height=2.86, ppd=300)
    tot = 2.86
    cam = N.camera((0, -20, tot / 2), (0, 0, tot / 2), 50, ortho=tot * 1200 / H_px)
    a.place((0, 0, 0), 0)
    S.shadow_link([a], L["key"])
    # the sheet face for the side-by-side (James is joyful on the sheet); face layers do not enter the measures
    a.pose(dict({"view": "front", "s": 1}, **({"expr": "joy"} if name == "crew" else {})), camera=cam)
    sc = bpy.context.scene
    os.makedirs(OUT, exist_ok=True)
    sc.render.filepath = os.path.join(OUT, name + "_front.png")
    bpy.ops.render.render(write_still=True)
    # ID pass
    for nm, ob in a.cards.items():
        m = bpy.data.materials.new(nm + "_id"); m.use_nodes = True
        nt = m.node_tree; nt.nodes.clear(); Nn, Ln = nt.nodes, nt.links.new
        out = Nn.new("ShaderNodeOutputMaterial"); uv = Nn.new("ShaderNodeUVMap"); uv.uv_map = "UVMap"
        tx = Nn.new("ShaderNodeTexImage"); tx.image = ob.data.materials[0].node_tree.nodes["col"].image; tx.interpolation = "Closest"
        Ln(uv.outputs[0], tx.inputs[0])
        em = Nn.new("ShaderNodeEmission"); em.inputs["Color"].default_value = IDCOL.get(nm, (0.2, 0.2, 0.2)) + (1,)
        tr = Nn.new("ShaderNodeBsdfTransparent")
        gt = Nn.new("ShaderNodeMath"); gt.operation = "GREATER_THAN"; Ln(tx.outputs["Alpha"], gt.inputs[0]); gt.inputs[1].default_value = 0.5
        mx = Nn.new("ShaderNodeMixShader"); Ln(gt.outputs[0], mx.inputs[0]); Ln(tr.outputs[0], mx.inputs[1]); Ln(em.outputs[0], mx.inputs[2])
        Ln(mx.outputs[0], out.inputs[0])
        ob.data.materials[0] = m
    for o in bpy.data.objects:
        if o.name in ("floor", "backdrop") or o == a.contact:
            o.hide_render = True
    sc.render.film_transparent = True
    sc.cycles.samples = 1; sc.cycles.use_denoising = False
    sc.render.filter_size = 0.01
    sc.view_settings.view_transform = "Standard"
    sc.render.filepath = os.path.join(OUT, name + "_id.png")
    bpy.ops.render.render(write_still=True)
    # pixel <-> figure-D mapping for this camera: ortho, the figure plane at y=0 (front cards; parallax ~0 in ortho)
    W, Hh = sc.render.resolution_x, sc.render.resolution_y
    os_ = cam.data.ortho_scale
    ppbu = max(W, Hh) / os_
    info = dict(W=W, H=Hh, ppbu=ppbu, cam_z=tot / 2, sc=a.sc, layers={k: dict(v, color=v["color"]) for k, v in a.layers.items()},
                anchors=a.fig["anchors"])
    return info


def to_px(info, xD, yD):
    """figure D (y down) -> pixel (ortho camera centred at x=0, z=cam_z)."""
    xb, zb = xD * info["sc"], -yD * info["sc"]
    return info["W"] / 2 + xb * info["ppbu"], info["H"] / 2 - (zb - info["cam_z"]) * info["ppbu"]


def circle_fit(xs, ys):
    A = np.c_[2 * xs, 2 * ys, np.ones(len(xs))]
    b = xs ** 2 + ys ** 2
    c, *_ = np.linalg.lstsq(A, b, rcond=None)
    cx, cy = c[0], c[1]
    r = math.sqrt(c[2] + cx * cx + cy * cy)
    res = np.abs(np.hypot(xs - cx, ys - cy) - r).mean()
    return cx, cy, r, res


def sprite_rows(info, layer):
    from PIL import Image
    L = info["layers"][layer]
    im = np.asarray(Image.open(L["color"]).convert("RGBA")).astype(int)
    x0, y0, x1, y1 = L["box"]
    h, w = im.shape[:2]
    return im, (x0, y0, (x1 - x0) / w, (y1 - y0) / h)


def analyse(name, info, spec):
    from PIL import Image
    import draw8
    sp = draw8.get_spec(spec)
    idim = np.asarray(Image.open(os.path.join(OUT, name + "_id.png")).convert("RGBA")).astype(float) / 255.0
    rgb, al = idim[..., :3], idim[..., 3]
    masks = {}
    for k, c in IDCOL.items():
        d = np.abs(rgb - np.array(c)).sum(-1)
        masks[k] = (d < 0.25) & (al > 0.5)
    sil = al > 0.5
    ys, xs = np.nonzero(sil)
    top, sole = ys.min(), ys.max()
    total = sole - top + 1
    headm = masks["head"] | masks["face"]
    hy, hx = np.nonzero(headm)
    hcy = (hy.min() + hy.max()) / 2.0
    # lower contour: boundary pixels of the head mask below the centre row, not touching other layers
    import cv2
    hm8 = headm.astype(np.uint8)
    er = cv2.erode(hm8, np.ones((3, 3), np.uint8))
    bd = (hm8 - er) > 0
    other = sil & ~headm
    near_other = cv2.dilate(other.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    by, bx = np.nonzero(bd & ~near_other)
    sel = by > hcy
    cx, cy, r, res = circle_fit(bx[sel].astype(float), by[sel].astype(float))
    widest = max((np.ptp(np.nonzero(headm[y])[0]) + 1) for y in range(hy.min(), hy.max() + 1) if headm[y].any())
    D = (2 * r + widest) / 2.0
    chin = hy.max()
    skull_top = cy - D / 2
    hairm = masks["hair"]
    hry, hrx = np.nonzero(hairm)
    hair_top = min(hry.min(), top)
    hair_w = np.ptp(hrx) + 1
    hair_low = hry.max()
    # crotch: scanning up the body-centre column from the sole, the first opaque pixel above the gap between the legs
    a = info["anchors"]
    cxp, _ = to_px(info, a["crotch"][0], a["crotch"][1])
    col = sil[:, int(round(cxp)) - 1:int(round(cxp)) + 2].any(1)
    yy = sole - 5
    while yy > top and not col[yy]:
        yy -= 1
    # skip the ground-contact part: legs touch at the soles only if the feet overlap; find the gap
    yy = sole - 2
    while yy > top and col[yy]:
        yy -= 1                                     # through feet if they overlap the centre column
    while yy > top and not col[yy]:
        yy -= 1
    crotch = yy
    # shoulder span: torso + arms in the band chin .. chin + 0.45 D
    band = slice(int(chin + 0.05 * D), int(chin + 0.45 * D))
    sh = (masks["torso"] | masks["arm_R"] | masks["arm_L"])[band]
    shx = np.nonzero(sh.any(0))[0]
    shoulder = np.ptp(shx) + 1
    shp = (masks["torso"] | masks["arm_R"] | masks["arm_L"] | masks["pack"])[band]
    shpx = np.nonzero(shp.any(0))[0]
    shoulder_pack = np.ptp(shpx) + 1 if masks["pack"].any() else None
    # sprite measurements (palette), mapped to render px through the card scale
    pxD = info["ppbu"] * info["sc"]                 # render px per D
    out = {}
    im, (bx0, by0, sx, sy) = sprite_rows(info, "leg_R")
    boot = np.array([int(sp["col"]["boot"][i:i + 2], 16) for i in (1, 3, 5)])
    trou = np.array([int(sp["col"]["trouser"][i:i + 2], 16) for i in (1, 3, 5)])
    isb = (np.abs(im[..., :3] - boot).sum(-1) <= 6) & (im[..., 3] > 200)
    ist = (np.abs(im[..., :3] - trou).sum(-1) <= 6) & (im[..., 3] > 200)
    rows_b = np.nonzero(isb.sum(1) > 3)[0]
    rows_t = np.nonzero(ist.sum(1) > 3)[0]
    alr = im[..., 3] > 128
    sole_row = np.nonzero(alr.any(1))[0].max()
    # boot top: the first row (going down) below the last trouser row where boot colour dominates
    boot_top = rows_b[rows_b > rows_t.max() - 2].min() if len(rows_t) else rows_b.min()
    boot_top_outline = boot_top - 0.032 * (1 / sy) * 0  # outline sits on the boundary
    boot_h_D = (sole_row - boot_top + 1) * sy
    # trouser leg width at the thigh (0.25 D below the crotch): opaque width of the leg sprite row
    cr_D = a["crotch"][1]
    row = int(round((cr_D + 0.25 - by0) / sy))
    rw = np.nonzero(alr[row])[0]
    leg_w_D = (np.ptp(rw) + 1) * sx
    # glove / hand width: palette pixels of the hand in the arm sprite (bbox width)
    im2, (ax0, ay0, sx2, sy2) = sprite_rows(info, "arm_L")
    hc = sp["col"].get("glove", "#333333") if sp.get("glove") else sp["skin"]
    hcol = np.array([int(hc[i:i + 2], 16) for i in (1, 3, 5)])
    ish = (np.abs(im2[..., :3] - hcol).sum(-1) <= 10) & (im2[..., 3] > 200)
    # restrict to the lowest 0.6 D of the arm sprite (the hand)
    rows = np.nonzero(im2[..., 3].max(1) > 128)[0]
    lo = rows.max() - int(0.5 / sy2)
    ish[:lo] = False
    hxs = np.nonzero(ish.any(0))[0]
    hand_w_D = (np.ptp(hxs) + 1) * sx2 if len(hxs) else None
    # head outline: ink thickness along 72 radial lines of the head sprite (median)
    im3, (hx0, hy0, sx3, sy3) = sprite_rows(info, "head")
    ink = (im3[..., :3].sum(-1) < 120) & (im3[..., 3] > 128)
    hcD = a["head"]
    c3 = ((hcD[0] - hx0) / sx3, (hcD[1] - hy0) / sy3)
    th = []
    for k in range(72):
        ang = 2 * math.pi * k / 72
        run = 0
        for rr in np.arange(0.40 / sx3, 0.52 / sx3, 0.5):
            x = int(round(c3[0] + rr * math.cos(ang))); y = int(round(c3[1] + rr * math.sin(ang)))
            if 0 <= x < ink.shape[1] and 0 <= y < ink.shape[0] and ink[y, x]:
                run += 0.5
        th.append(run * sx3)
    outline_D = float(np.median(th))
    R = dict(total_h_px=int(total), D_px=round(D, 1), D_fit_px=round(2 * r, 1), D_widest_px=int(widest), fit_residual_px=round(res, 2),
             head_over_total=D / total, head_with_hair_over_total=(chin - hair_top) / total, heads_tall=total / D,
             hair_above_skull_over_D=(skull_top - hair_top) / D, hair_extent_over_D=(hair_low - hair_top) / D, hair_w_over_D=hair_w / D,
             shoulder_over_D=shoulder / D, backpack_span_over_D=(shoulder_pack / D) if shoulder_pack else None,
             torso_over_total=(crotch - chin) / total, torso_over_D=(crotch - chin) / D,
             leg_over_total=(sole - crotch) / total, leg_over_D=(sole - crotch) / D,
             leg_w_over_D=leg_w_D * pxD / D, hand_w_over_D=(hand_w_D * pxD / D) if hand_w_D else None, boot_h_over_D=boot_h_D * pxD / D,
             outline_over_D=outline_D * pxD / D)
    R = {k: (round(v, 3) if isinstance(v, float) else v) for k, v in R.items()}
    # annotated ID image
    vis = (np.asarray(Image.open(os.path.join(OUT, name + "_front.png")).convert("RGB"))).copy()
    from PIL import ImageDraw
    im_ = Image.fromarray(vis); d = ImageDraw.Draw(im_)
    for y, c, t in ((hair_top, (255, 0, 0), "hair top"), (skull_top, (255, 128, 0), "skull top"), (chin, (255, 0, 255), "chin"),
                    (crotch, (0, 160, 0), "crotch"), (sole, (255, 0, 0), "sole")):
        d.line([(0, y), (im_.width, y)], fill=c, width=2); d.text((4, y - 12), t, fill=c)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(0, 200, 255), width=2)
    d.line([(shx.min(), band.start), (shx.max(), band.start)], fill=(0, 200, 200), width=3)
    im_.save(os.path.join(OUT, name + "_measured.png"))
    return R


def band_check(name, R):
    ref = SHEET[REF[name]]
    rows = []
    for k, lab in KEYS:
        t = ref.get(k)
        v = R.get(k)
        if t is None or v is None:
            rows.append((lab, t, v, None, None)); continue
        lo, hi = t * 0.94, t * 1.06
        if k == "boot_h_over_D" and REF[name] == "kong":
            pass
        rows.append((lab, t, v, (lo, hi), lo <= v <= hi))
    return rows


def main(names):
    import bpy
    res = {}
    for nm in names:
        spec = {"kong": "kong", "crew": "crew", "driver": "driver"}[nm]
        info = render_pair(nm, spec)
        R = analyse(nm, info, spec)
        res[nm] = dict(measured=R, check=[dict(measure=a, sheet=b, ours=c, band=d, ok=e) for a, b, c, d, e in band_check(nm, R)])
        print(nm, json.dumps(R, default=lambda o: o.item()))
    p = os.path.join(HERE, "out", "measure.json")
    old = json.load(open(p)) if os.path.exists(p) else {}
    old.update(res)
    json.dump(old, open(p, "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    # markdown table
    lines = ["| measure | Kong sheet | Kong ours | crew vs James sheet | crew ours | driver vs Tos sheet | driver ours |", "|---|---|---|---|---|---|---|"]
    for i, (k, lab) in enumerate(KEYS):
        cells = [lab]
        for nm in ("kong", "crew", "driver"):
            if nm not in old:
                cells += ["", ""]; continue
            c = old[nm]["check"][i]
            sv = "-" if c["sheet"] is None else "%.3f" % c["sheet"]
            ov = "-" if c["ours"] is None else "%.3f" % c["ours"]
            mark = "" if c["ok"] is None else (" ok" if c["ok"] else " **OUT**")
            cells += [sv, ov + mark]
        lines.append("| " + " | ".join(cells) + " |")
    open(os.path.join(HERE, "out", "measure_table.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1].split(",") if len(sys.argv) > 1 else ["kong", "crew", "driver"])

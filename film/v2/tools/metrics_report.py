#!/usr/bin/env python3
"""metrics_report.py -- colour, set and edge statistics of our frames against the reference targets -> out/METRICS.md.
Measuring only (numpy, cv2).  Uses spec/measure_color.py and ref/crops/env/tools/metrics.py unchanged (imported), the
acceptance code of sets/office.py (measure) and tools/edge_soft.py.
usage: python3 tools/metrics_report.py [g g g ...]      (output frame numbers; default 40 70 120 147)"""
import colorsys, importlib.util, json, os, subprocess, sys, tempfile
import numpy as np, cv2
HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
PROJ = os.path.dirname(V2)
sys.path.insert(0, os.path.join(V2, "sets"))
sys.path.insert(0, HERE)


def _load(name, path):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


mc = _load("measure_color", os.path.join(PROJ, "spec", "measure_color.py"))
em = _load("envmetrics", os.path.join(PROJ, "ref", "crops", "env", "tools", "metrics.py"))
import office            # noqa: E402
import edge_soft         # noqa: E402

gs = [int(a) for a in sys.argv[1:]] or [40, 70, 120, 147]
out_dir = os.path.join(V2, "out")
mp4 = os.path.join(out_dir, "proto_v2.mp4")
qa = json.load(open(os.path.join(out_dir, "qa.json")))
man = json.load(open(os.path.join(out_dir, "manifest.json")))
by = dict(((q["shot"], q["g"]), q) for q in qa)
td = os.path.join(V2, "tmp", "metrics")
os.makedirs(td, exist_ok=True)
names = {"s01": "insert", "s02": "medium", "s03": "two-shot"}
label_of = lambda q: ("close-up end of the two-shot" if q["shot"] == "s03" and q["cam"][2] > 200 else "medium after the snap" if q["shot"] == "s02" and q["cam"][2] > 230 else names[q["shot"]])


def grab(g):
    p = os.path.join(td, "ours_g%03d.png" % g)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-threads", "2", "-i", mp4, "-vf", "select=eq(n\\,%d)" % g, "-vframes", "1", p], check=True)
    return p


def hsv_of(bgr):
    b, g_, r = [float(v) / 255.0 for v in bgr]
    h, s, v = colorsys.rgb_to_hsv(r, g_, b)
    return h * 360, s, v


def head_stats(im, heads):
    """row 16: fill colour at the head centre (brighter half of a disc of 0.25 D, so that eyes and brows drop out);
    row 17: V at the centre against V 10 px inside the outline on the lower left (the side without hat, hair or crescent)."""
    res = []
    for (hx, hy, d) in heads:
        yy, xx = np.mgrid[0:im.shape[0], 0:im.shape[1]]
        m = np.hypot(xx - hx, yy - hy) < 0.25 * d
        if not m.any():
            continue
        px = im[m].astype(np.float32)
        lum = px.mean(axis=1)
        fill = np.median(px[lum >= np.median(lum)], axis=0)
        h, s, v = hsv_of(fill)
        # 10 px inside the fill edge (fill radius 0.463 D) on the lower left, where there is no hat, hair or crescent
        dvs = []
        for ang in (115.0, 130.0, 145.0):
            a = np.radians(ang)
            ex, ey = hx + (0.463 * d - 10) * np.cos(a), hy + (0.463 * d - 10) * np.sin(a)
            if 3 <= ex < im.shape[1] - 3 and 3 <= ey < im.shape[0] - 3:
                patch = im[int(ey) - 1:int(ey) + 2, int(ex) - 1:int(ex) + 2].reshape(-1, 3).astype(np.float32)
                dvs.append(abs(v - hsv_of(np.median(patch, axis=0))[2]))
        edge_dv = float(np.median(dvs)) if dvs else float("nan")
        res.append(dict(hex=mc.hexof(fill), V=v, S=s, dV=edge_dv))
    return res


def surface_detail(im, boxes):
    """luma std after a sigma-12 high-pass, on 120 px patches clear of actors and of the caption band:
    median of the patches in the upper half (wall) and below y = 1000 (floor)."""
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
    hp = g - cv2.GaussianBlur(g, (0, 0), 12)
    wall, floor = [], []
    for y in range(0, 1280 - 120 + 1, 40):
        for x in range(0, 720 - 120 + 1, 40):
            if y + 120 > 840 and y < 965:
                continue
            if any(x < b[2] and x + 120 > b[0] and y < b[3] and y + 120 > b[1] for b in boxes):
                continue
            v = float(hp[y:y + 120, x:x + 120].std())
            if y + 120 <= 640:
                wall.append(v)
            elif y >= 965:
                floor.append(v)
    med = lambda a: float(np.median(a)) if a else float("nan")
    return med(wall), med(floor)


def measure(path, heads=(), boxes=()):
    im = mc.load(path)
    s = mc.stats(im)
    pal = mc.palette(im)
    share, hexc = pal[0]
    c = [int(hexc[i:i + 2], 16) for i in (5, 3, 1)]
    ph, ps, pv = hsv_of(c)
    e = em.stats(em.load(path))
    o = office.measure(path, heads=list(heads) if heads else None)
    es = edge_soft.edge_width(path)
    hs = head_stats(im, heads)
    wall, floor = surface_detail(im, boxes)
    mid = [int(s["mid_hex"][i:i + 2], 16) / 255.0 for i in (1, 3, 5)]
    return dict(s=s, pal=(share, hexc, ps, pv), e=e, o=o, es=es, heads=hs, wall=wall, floor=floor, mid_v=max(mid))


rows = []
for g in gs:
    src = man["timeline"][g]
    q = by[tuple(src[1] if len(src) == 3 and src[2] >= 0.5 else src[0])]
    heads, boxes = [], []
    for uid, a in q["actors"].items():
        if uid == "h1":
            continue
        hx, hy = a["head"]; d = a["D_px"]
        if -0.3 * d < hx < 720 + 0.3 * d:
            heads.append((hx, hy, d))
        boxes.append((hx - 0.75 * d, hy - 0.8 * d, hx + 0.75 * d, a["feet"][1] + 10))
    rows.append(("ours g%d %s (%.2f s)" % (g, label_of(q), g / 30.0), measure(grab(g), heads, boxes)))
refs = [("ref a/t45.0", os.path.join(PROJ, "ref", "a", "t45.0.jpg"), [(499, 474, 250), (1113 - 720 + 60, 0, 0)][:1]),
        ("ref b/t05.5", os.path.join(PROJ, "ref", "b", "t05.5.jpg"), []),
        ("ref b/t24.5", os.path.join(PROJ, "ref", "b", "t24.5.jpg"), []),
        ("v1 frame45", os.path.join(PROJ, "v1", "v1_frame45.png"), [])]
ref_rows = [(n, measure(p)) for n, p, h in refs]

L = []
P = L.append
P("# METRICS: our frames against the reference targets")
P("")
P("Frames are taken from `out/proto_v2.mp4` (after the H.264 encode, captions burned in; every tool masks the caption band).")
P("Tools, unchanged: `spec/measure_color.py` (colour rows), `ref/crops/env/tools/metrics.py` (set rows), `sets/office.py measure()`")
P("(acceptance rows of LOOK_SPEC 3.5), `tools/edge_soft.py` (edge softness). Reference and v1 columns were measured with the same code in this run.")
P("")
allc = rows + ref_rows
hdr = "| # | Quantity | Target (LOOK_SPEC 4.1) | " + " | ".join(n for n, _ in allc) + " |"
P("## 1. Colour (LOOK_SPEC 4.1)")
P("")
P(hdr)
P("|" + "---|" * (3 + len(allc)))


def line(num, name, target, fn, ok=None):
    cells = []
    for i, (n, r) in enumerate(allc):
        v = fn(r)
        txt = v if isinstance(v, str) else "%.3f" % v
        if ok is not None and i < len(rows):
            txt += "" if ok(r) else " (out)"
        cells.append(txt)
    P("| %s | %s | %s | %s |" % (num, name, target, " | ".join(cells)))


rng = lambda a, b: (lambda v: a <= v <= b)
line(1, "Saturation mean", "0.40 to 0.60", lambda r: r["s"]["S_mean"], lambda r: 0.40 <= r["s"]["S_mean"] <= 0.60)
line(2, "Saturation p90", "at least 0.62", lambda r: r["s"]["S_p90"], lambda r: r["s"]["S_p90"] >= 0.62)
line(3, "Value mean", "0.44 to 0.60", lambda r: r["s"]["V_mean"], lambda r: 0.44 <= r["s"]["V_mean"] <= 0.60)
line(4, "Luma p5", "0.09 to 0.18", lambda r: r["s"]["Y_p5"], lambda r: 0.09 <= r["s"]["Y_p5"] <= 0.18)
line(5, "Luma p50", "0.22 to 0.45", lambda r: r["s"]["Y_p50"], lambda r: 0.22 <= r["s"]["Y_p50"] <= 0.45)
line(6, "Luma p95", "0.75 to 0.92", lambda r: r["s"]["Y_p95"], lambda r: 0.75 <= r["s"]["Y_p95"] <= 0.92)
line(7, "Contrast, luma p95 - p5", "0.60 to 0.75", lambda r: r["s"]["Y_contrast"], lambda r: 0.60 <= r["s"]["Y_contrast"] <= 0.75)
line(8, "Colourfulness", "55 to 100", lambda r: "%.1f" % r["s"]["colourfulness"])
line(9, "Share S > 0.5", "at least 0.25", lambda r: r["s"]["frac_S_gt_50"], lambda r: r["s"]["frac_S_gt_50"] >= 0.25)
line(10, "Share S < 0.15", "at most 0.12", lambda r: r["s"]["frac_S_lt_15"], lambda r: r["s"]["frac_S_lt_15"] <= 0.12)
line(11, "Share V > 0.95", "0.02 to 0.09", lambda r: r["s"]["frac_V_gt_95"], lambda r: 0.02 <= r["s"]["frac_V_gt_95"] <= 0.09)
line(12, "Black point, luma p1", "0.08 to 0.12", lambda r: r["s"]["Y_p1"], lambda r: 0.08 <= r["s"]["Y_p1"] <= 0.12)
line(13, "Darkest 10 percent: colour, hue, S", "hue 250 to 345, S at least 0.35", lambda r: "%s, %.0f, %.2f" % (r["s"]["dark10_hex"], r["s"]["dark10_hue"], r["s"]["dark10_sat"]))
line(14, "40 to 60 percent band: colour, hue, V", "hue 330 to 25 or 230 to 290, V 0.40 to 0.60", lambda r: "%s, %.0f, %.2f" % (r["s"]["mid_hex"], r["s"]["mid_hue"], r["mid_v"]))
line(15, "Largest palette cluster: share, colour, S, V", "V at most 0.65, S at least 0.35", lambda r: "%.0f%% %s, %.2f, %.2f" % (r["pal"][0] * 100, r["pal"][1], r["pal"][2], r["pal"][3]))
line(16, "Head fill at the head centre: colour, V, S", "V 0.97 to 0.995, S at most 0.04", lambda r: "; ".join("%s, %.3f, %.3f" % (h["hex"], h["V"], h["S"]) for h in r["heads"]) or "-")
line(17, "Head flatness: V centre against 10 px inside the outline", "at most 0.07", lambda r: "; ".join("%.3f" % h["dV"] for h in r["heads"]) or "-")
P("")
P("Rows 16 and 17 are measured at the head positions that build.py records (qa.json); row 17 on the lower-left side of the head (median of three points 10 px inside the fill edge), away from the hat, the hair patch and the lavender crescent, which is on the lower right by design.")
P("")
P("## 2. Set and acceptance checks (LOOK_SPEC 3.5, `metrics.py`)")
P("")
P("| Check | Pass | " + " | ".join(n for n, _ in allc) + " |")
P("|" + "---|" * (2 + len(allc)))


def line2(name, target, fn):
    P("| %s | %s | %s |" % (name, target, " | ".join(fn(r) for n, r in allc)))


line2("Canny edge density (60/140), caption band masked", "at least 0.05 (set alone 0.085)", lambda r: "%.3f" % r["e"]["edge"])
line2("Featureless 40 px blocks", "at most 0.30 (office 0.25)", lambda r: "%.3f" % r["o"]["featureless"])
line2("Luminance: top eighth / two middle rows / bottom eighth", "40 to 90 / 105 to 150 / 30 to 70", lambda r: "%.0f / %.0f / %.0f" % (r["o"]["lum_top"], r["o"]["lum_mid"], r["o"]["lum_bot"]))
line2("Luminance in a ring around each head", "95 to 170", lambda r: ", ".join("%.0f" % v for v in (r["o"].get("behind_heads") or [])) or "-")
line2("Surface detail, wall patches / floor patches (luma std after sigma-12 high-pass)", "0.03 to 0.10", lambda r: "%.3f / %.3f" % (r["wall"], r["floor"]))
line2("metrics.py: S / V / Laplacian / colour bins", "reference medians A 0.48 / 0.60, B 0.41 / 0.50", lambda r: "%.2f / %.2f / %.1f / %d" % (r["e"]["S"], r["e"]["V"], r["e"]["lap"], r["e"]["bins"]))
P("")
P("The luminance bands are the wide and two-shot targets; the insert and the close framings do not show the ceiling or the camera end of the floor.")
P("")
P("## 3. Edge softness (render setting)")
P("")
P("10 to 90 percent rise width of the strongest white-against-ink edges (`tools/edge_soft.py`, median of up to 4000 edge samples).")
P("")
P("| Frame | rise 10-90 (px) | quartiles | Laplacian variance |")
P("|---|---|---|---|")
for n, r in allc:
    P("| %s | %.2f | %.2f to %.2f | %.0f |" % (n, r["es"]["w50"], r["es"]["w25"], r["es"]["w75"], r["es"]["lap"]))
soft = os.path.join(out_dir, "edge_softness.json")
if os.path.exists(soft):
    P("")
    P("Render-setting test on one still (same frame, before the encode; reference frames decoded straight from the videos):")
    P("")
    P("| Variant | rise 10-90 (px) | Laplacian variance |")
    P("|---|---|---|")
    for k, v in json.load(open(soft)):
        P("| %s | %.2f | %.0f |" % (k, v[0], v[1]))
    P("")
    d = dict(json.load(open(soft)))
    refv = sorted(v[0] for k, v in d.items() if k.startswith("reference"))
    P("Decision: supersample 2x in Chromium (deviceScaleFactor 2, JPEG q98 intermediates) and scale down with ffmpeg's bilinear filter: "
      "%.2f px against %.2f to %.2f px in the reference (median %.2f). deviceScaleFactor 1 is too crisp (%.2f px, Laplacian variance %.0f against %.0f to %.0f)."
      % (d["deviceScaleFactor 2, scaled down bilinear"][0], refv[0], refv[-1], (refv[1] + refv[2]) / 2.0, d["deviceScaleFactor 1"][0], d["deviceScaleFactor 1"][1],
         min(v[1] for k, v in d.items() if k.startswith("reference")), max(v[1] for k, v in d.items() if k.startswith("reference"))))
txt = "\n".join(L) + "\n"
open(os.path.join(out_dir, "METRICS_tables.md"), "w").write(txt)
print(txt)

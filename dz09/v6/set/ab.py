"""ab.py -- before/after stills of the 4 presets (low, eye, high, macro) in 9:16, the measurements and the sheet.

python3 ab.py before [--only eye,high] [--q final] [--scale 1.0]     v4 set + v4 post, same cameras (no fg props)
python3 ab.py after  [--only ...]   [--q final] [--scale 1.0]        v6 beauty set + post6
python3 ab.py repost [--only ...] [key=value ...]                     post6 again on kept after/ EXRs (fast)
python3 ab.py sheet                                                  before_after.png (+ measure json)
"""
import os, sys, json, time, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "out")
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
REF = {"low": 81, "eye": 76, "high": 90, "macro": 2}       # ref D frames2 ids used next to each preset

ap = argparse.ArgumentParser()
ap.add_argument("mode"); ap.add_argument("--only", default="low,eye,high,macro"); ap.add_argument("--q", default="final")
ap.add_argument("--scale", type=float, default=1.0); ap.add_argument("--threads", type=int, default=4)
ap.add_argument("--frame", type=int, default=7); ap.add_argument("kv", nargs="*")
a = ap.parse_args()
names = a.only.split(",")


def kvs():
    d = {}
    for t in a.kv:
        k, v = t.split("=")
        try: d[k] = json.loads(v)
        except Exception: d[k] = v
    return d


if a.mode in ("before", "after"):
    import beauty as B
    import bpy, standins, presets
    X = B.X
    A = B.build() if a.mode == "after" else X.build()
    (B.setup_render if a.mode == "after" else (lambda q, threads: X.setup_render(quality=q, threads=threads)))(a.q, threads=a.threads)
    acts = standins.place(A)
    times = {}
    od = os.path.join(OUT, a.mode); os.makedirs(od, exist_ok=True)
    for n in names:
        cam = presets.use(n, A, "9:16", scale=a.scale, with_fg=(a.mode == "after"))
        bpy.context.view_layer.update()
        standins.pose_all(acts, cam, hide=(("kong",) if n == "macro" else ()))
        if a.mode == "after":
            r = B.render6.render(os.path.join(od, n), frame=a.frame, post_opts=kvs())
        else:
            r = X.render_still(os.path.join(od, n), frame=a.frame)
        times[n] = {k: r.get(k) for k in ("cpu_render", "wall_render", "cpu_post", "wall_post")}
        print("TIME", a.mode, n, times[n], flush=True)
    tp = os.path.join(OUT, f"times_{a.mode}.json")
    old = json.load(open(tp)) if os.path.exists(tp) else {}
    old.update(times); json.dump(old, open(tp, "w"), indent=1)

elif a.mode == "repost":
    import bpy, pickle
    import beauty as B, render6, post6
    for n in names:
        base = os.path.join(OUT, "after", n)
        info = json.load(open(base + "_info.json")); info.update(kvs())
        info["shafts"] = pickle.load(open(base + "_shafts.pkl", "rb"))
        out = {k: f"{base}_{k}.exr" for k in ("rgb", "z", "idx", "env")}
        import numpy as np
        from PIL import Image
        H, W = 1280, 720
        rgb, alpha, env, z, idx = render6.load_passes(out, W, H)
        t0 = time.process_time()
        post6.process(rgb, z, idx, info, base + ".png", None, alpha=alpha, env=env)
        print("repost", n, round(time.process_time() - t0, 2), flush=True)

elif a.mode == "sheet":
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    sys.path.insert(0, os.path.join(PROJ, "spec", "refD_beauty_tools")); sys.path.insert(0, os.path.join(PROJ, "v3", "tools"))
    import measure, hue_report
    w, h = 360, 640
    cols = []
    rows = [("ref D", lambda n: os.path.join(PROJ, "ref", "d", "frames2", f"f_{REF[n]:03d}.png")),
            ("before (v4)", lambda n: os.path.join(OUT, "before", n + ".png")),
            ("after (v6)", lambda n: os.path.join(OUT, "after", n + ".png"))]
    sheet = Image.new("RGB", (w * len(names) + 10 * (len(names) - 1), (h + 30) * 3), (12, 12, 16))
    d = ImageDraw.Draw(sheet)
    try: f = ImageFont.truetype(os.path.join(PROJ, "fonts", "WorkSans-Black.ttf"), 18)
    except Exception: f = ImageFont.load_default()
    M = {}
    for j, (lab, fn) in enumerate(rows):
        for i, n in enumerate(names):
            p = fn(n)
            x = i * (w + 10); y = j * (h + 30)
            d.text((x + 6, y + 5), f"{lab}  {n}" if lab != "ref D" else f"ref D f2_{REF[n]:03d} (look only)", fill=(230, 230, 230), font=f)
            if os.path.exists(p):
                im = Image.open(p).convert("RGB")
                sheet.paste(im.resize((w, h), Image.LANCZOS), (x, y + 30))
                if lab != "ref D":
                    st = measure.stats(measure.load(p), cap=False)
                    hs = hue_report.stats([p])
                    st["hue_report"] = {k: round(v, 1) for k, v in hs[0].items()}; st["hr_sat"] = round(hs[1], 3)
                    M[f"{lab.split()[0]}_{n}"] = st
    sheet.save(os.path.join(HERE, "before_after.png"))
    json.dump(M, open(os.path.join(OUT, "measure.json"), "w"), indent=1)
    for k, st in M.items():
        print(k, "p1 %.3f p5 %.3f p50 %.3f p95 %.3f S %.2f blue %.2f warm %.2f edge %.3f top %.3f lc %.3f mag %.1f vio %.1f shB/R %.2f" % (
            st["L_p1"], st["L_p5"], st["L_p50"], st["L_p95"], st["S_mean"], st["hue_blue"], st["hue_orange"] + st["hue_red"],
            st["edge_all"], float(np.mean(st["edge_grid"][0])), st["local_contrast"], st["hue_report"]["magenta"], st["hue_report"]["violet"],
            st["tint_sh"][2] / max(st["tint_sh"][0], 1e-3)))

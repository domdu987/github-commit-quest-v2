"""drafts.py -- render every camera preset in both aspects, build the sheets, compare with ref C, hue report, timing.

    python3 drafts.py drafts [--no-actors] [--threads 2]     # out/drafts/<preset>_916.png and _169.png (360x640 / 640x360, 8 spp + OIDN)
    python3 drafts.py sheets                                 # out/sheet_916.jpg, out/sheet_169.jpg, out/compare_ref.jpg
    python3 drafts.py hue                                    # hue_report rows -> out/hue.txt
    python3 drafts.py timing [preset] [--threads 2]          # one final-quality 720x1280 frame, CPU seconds -> out/timing.json
"""
import os, sys, json, time, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "out")
DR = os.path.join(OUT, "drafts")
REF = os.path.join(PROJ, "ref", "c", "frames", "f_017.png")
ASPECTS = [("9:16", "916"), ("16:9", "169")]


def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def drafts():
    import bpy, expressway as X
    os.makedirs(DR, exist_ok=True)
    A = X.build(); X.setup_render(quality="draft", threads=int(arg("--threads", 2)))
    X.anchors_json(A, os.path.join(OUT, "anchors.json"))
    acts = None
    if "--no-actors" not in sys.argv:
        import standins; acts = standins.place(A)
    only = arg("--only", None)
    log = {}
    for name in X.CAMERAS:
        if only and name not in only.split(","): continue
        for asp, tag in ASPECTS:
            cam = X.use_camera(name, asp, scale=0.5); bpy.context.view_layer.update()
            if acts: standins.pose_all(acts, cam, hide=("kong",) if name == "macro_cutter" else ())
            r = X.render_still(os.path.join(DR, f"{name}_{tag}"), frame=7)
            log[f"{name}_{tag}"] = {k: r[k] for k in ("cpu_render", "wall_render", "cpu_post")}
            print(name, asp, log[f"{name}_{tag}"], flush=True)
            for k in ("rgb", "idx"):
                if r.get(k) and os.path.exists(r[k]): os.remove(r[k])     # keep z.exr (depth pass), drop the bulky rest
    json.dump(log, open(os.path.join(OUT, "draft_times.json"), "w"), indent=1)


def _label(im, text, w):
    from PIL import ImageDraw, ImageFont, Image
    bar = Image.new("RGB", (w, 26), (14, 14, 18)); d = ImageDraw.Draw(bar)
    f = ImageFont.truetype(os.path.join(PROJ, "fonts", "WorkSans-Black.ttf"), 15)
    d.text((8, 4), text, font=f, fill=(235, 235, 235))
    out = Image.new("RGB", (w, im.height + 26)); out.paste(bar, (0, 0)); out.paste(im, (0, 26)); return out


def sheets():
    from PIL import Image
    import expressway as X
    for asp, tag in ASPECTS:
        tiles = []
        for name in X.CAMERAS:
            p = os.path.join(DR, f"{name}_{tag}.png")
            if not os.path.exists(p): continue
            im = Image.open(p).convert("RGB")
            tiles.append(_label(im, f"{name}  {asp}", im.width))
        if not tiles: continue
        cols = 4 if tag == "916" else 2
        w, h = tiles[0].size
        rows = (len(tiles) + cols - 1) // cols
        sh = Image.new("RGB", (cols * w + (cols + 1) * 6, rows * h + (rows + 1) * 6), (30, 30, 34))
        for i, t in enumerate(tiles):
            sh.paste(t, (6 + (i % cols) * (w + 6), 6 + (i // cols) * (h + 6)))
        sh.save(os.path.join(OUT, f"sheet_{tag}.jpg"), quality=90)
        print(os.path.join(OUT, f"sheet_{tag}.jpg"))
    # reference f_017 beside two of ours, all 360x640
    ref = Image.open(REF).convert("RGB").resize((360, 640), Image.LANCZOS)
    picks = [("ref C f_017 (t=32 s)", ref)]
    for name in ("eye", "high"):
        p = os.path.join(DR, f"{name}_916.png")
        if os.path.exists(p): picks.append((f"ours: {name} 9:16", Image.open(p).convert("RGB")))
    tiles = [_label(im, t, 360) for t, im in picks]
    sh = Image.new("RGB", (len(tiles) * 366 + 6, tiles[0].height + 12), (30, 30, 34))
    for i, t in enumerate(tiles): sh.paste(t, (6 + i * 366, 6))
    sh.save(os.path.join(OUT, "compare_ref.jpg"), quality=92); print(os.path.join(OUT, "compare_ref.jpg"))


def hue():
    sys.path.insert(0, os.path.join(PROJ, "v3", "tools"))
    from hue_report import stats, NAMES
    rows = []
    def row(label, files):
        h, s, v, dk = stats(files)
        rows.append(f"{label:34s} " + " ".join(f"{h[n]:6.1f}" for n in NAMES) + f"  {s:.2f} {v:.2f} {dk:.2f}")
    rows.append(f"{'set':34s} " + " ".join(f"{n[:6]:>6s}" for n in NAMES) + "   sat  val dark")
    row("ref C f_017 (night rain)", [REF])
    row("ref C f_017 + f_018", [REF, REF.replace("f_017", "f_018")])
    import expressway as X
    for tag in ("916", "169"):
        fl = sorted(glob.glob(os.path.join(DR, f"*_{tag}.png")))
        fl = [f for f in fl if not f.endswith(("_raw.png", "_depth.png"))]
        row(f"ours, all presets {tag}", fl)
        for f in fl: row("  " + os.path.basename(f)[:-4], [f])
    rows.append("night band (LOOK_SPEC_C check 6): blue 50-65, orange 15-25, red 8-15, violet <= 6, magenta <= 3; S 0.30-0.40; dark (V<0.25) 0.35-0.48")
    rows.append("house band (CONVENTIONS, interiors): red 30-41, orange 22-38, blue 14-30, violet 0-5, magenta 0-10")
    txt = "\n".join(rows); print(txt)
    open(os.path.join(OUT, "hue.txt"), "w").write(txt + "\n")


def timing():
    import bpy, expressway as X, resource
    os.makedirs(os.path.join(OUT, "final"), exist_ok=True)
    name = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "eye"
    thr = int(arg("--threads", 2))
    q = arg("--quality", "final")
    t0 = time.time(); r0 = resource.getrusage(resource.RUSAGE_SELF)
    A = X.build(haze_cards="--no-haze" not in sys.argv); X.setup_render(quality=q, threads=thr)
    import standins; acts = standins.place(A)
    cam = X.use_camera(name, "9:16", scale=1.0); bpy.context.view_layer.update(); standins.pose_all(acts, cam)
    r1 = resource.getrusage(resource.RUSAGE_SELF); t1 = time.time()
    res = X.render_still(os.path.join(OUT, "final", f"{name}_916_{q}"), frame=7)
    r2 = resource.getrusage(resource.RUSAGE_SELF)
    cpu_build = (r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime)
    rep = dict(preset=name, quality=q, haze_cards="--no-haze" not in sys.argv, samples=bpy.context.scene.cycles.samples, render_pct=bpy.context.scene.render.resolution_percentage,
               output="720x1280", threads=thr, build_cpu_s=round(cpu_build, 1), build_wall_s=round(t1 - t0, 1),
               render_cpu_s=res["cpu_render"], render_wall_s=res["wall_render"], post_cpu_s=res.get("cpu_post"),
               frame_cpu_s=round(res["cpu_render"] + res.get("cpu_post", 0), 1), load_avg=os.getloadavg(), png=res.get("png"))
    print(json.dumps(rep, indent=1))
    path = os.path.join(OUT, "timing.json")
    allr = json.load(open(path)) if os.path.exists(path) else []
    allr.append(rep); json.dump(allr, open(path, "w"), indent=1)


def repost():
    """re-run post.py on kept EXRs: python3 drafts.py repost <out_noext> <preset> <aspect> <focus_z> <k>"""
    import bpy, numpy as np, cv2, post, expressway as X
    o = sys.argv[2]
    rgba = X._read_exr(o + "_rgb.exr"); z = X._read_exr(o + "_z.exr")[..., 0]; idx = X._read_exr(o + "_idx.exr")[..., 0]
    env = X._read_exr(o + "_env.exr")[..., :3]
    W, H = (720, 1280) if sys.argv[4] == "9:16" else (1280, 720)
    rgb, alpha = rgba[..., :3], rgba[..., 3]
    if rgb.shape[1] != W:
        rgb = np.maximum(cv2.resize(rgb, (W, H), interpolation=cv2.INTER_LANCZOS4), 0)
        env = np.maximum(cv2.resize(env, (W, H), interpolation=cv2.INTER_LANCZOS4), 0)
        alpha = np.clip(cv2.resize(alpha, (W, H)), 0, 1)
        z = cv2.resize(z, (W, H), interpolation=cv2.INTER_NEAREST); idx = cv2.resize(idx, (W, H), interpolation=cv2.INTER_NEAREST)
    post.process(rgb, z, idx, dict(preset=sys.argv[3], focus_z=float(sys.argv[5]), k=float(sys.argv[6]), frame=7),
                 o + ".png", o + "_depth.png", alpha=alpha, env=env, out_raw=o + "_raw.png")


if __name__ == "__main__":
    {"drafts": drafts, "sheets": sheets, "hue": hue, "timing": timing, "repost": repost}[sys.argv[1]]()

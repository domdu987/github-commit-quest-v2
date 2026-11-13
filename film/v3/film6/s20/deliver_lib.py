#!/usr/bin/env python3
"""deliver_lib.py -- shared delivery for takes s20 / s21 / s23 (copied into each take folder; each deliver.py passes its config).
raw/s<id>/g_*.png -> frames/, meta.json, cues.json, contact.jpg, compare.jpg, work/qa.txt (heads, pops, hue rows) and take.mkv."""
import os, sys, json, glob, shutil, subprocess, io, contextlib
import numpy as np
from PIL import Image, ImageDraw


def run(here, cfg):
    proj = os.path.normpath(os.path.join(here, "..", "..", ".."))
    sys.path.insert(0, os.path.join(proj, "v3", "tools"))
    import hue_report as H
    sid, (ga, gb) = cfg["id"], cfg["range"]
    raw = os.path.join(here, "raw", "s%d" % sid); out = os.path.join(here, "frames"); os.makedirs(out, exist_ok=True)
    gs = list(range(ga, gb + 1))
    for g in gs:
        shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(out, "g_%04d.png" % g))
    rows = [json.load(open(os.path.join(raw, "g_%04d.json" % g))) for g in gs]
    walls = [r["wall"] for r in rows]; cpus = [r["cpu"] for r in rows]
    meta = dict(take=cfg["take"], film=6, shots=cfg["shots"], first_g=ga, n_frames=len(gs), g0=cfg["g0"], g1=cfg["g1"],
                handle_in=cfg["g0"] - ga, handle_out=gb + 1 - cfg["g1"], transition_in=cfg["transition_in"],
                transition_out=cfg["transition_out"], cuts_inside=cfg["cuts"], shot_ranges=cfg["shot_ranges"], events=cfg["events"],
                set=cfg["set"], light=cfg["light"], cast=cfg["cast"],
                dof="none (client rule: cam.data.dof.use_dof False + B.setup_dof(scene, None, None, cam=cam) at build and before every render)",
                denoiser="OpenImageDenoise, albedo+normal, prefilter FAST",
                narration="film6/audio/narration_bankky.wav at +0.10 s; captions film6/script/captions.json",
                samples=12, resolution=[720, 1280], threads=2, fps=30,
                s_per_frame_wall_mean=round(float(np.mean(walls)), 2), s_per_frame_cpu_mean=round(float(np.mean(cpus)), 2))
    json.dump(meta, open(os.path.join(here, "meta.json"), "w"), indent=1)
    ev = []
    for g0, g1, label, kind, kw in cfg["cues"]:
        e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=g0, end_frame=g1, kind=kind, label=label)
        e.update(kw); ev.append(e)
    json.dump(dict(take=cfg["take"], fps=30, note="time = film seconds (g / 30); narration PROJ/film6/audio/narration_bankky.wav at +0.10 s, captions.json",
                   cues=ev), open(os.path.join(here, "cues.json"), "w"), indent=1)
    # contact sheet: 16 frames, label strip above each picture
    sel = [gs[int(round(i * (len(gs) - 1) / 15.0))] for i in range(16)]
    w, h, lab, cols = 270, 480, 18, 8
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
    for i, g in enumerate(sel):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(os.path.join(out, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        tag = "handle" if g < cfg["g0"] or g >= cfg["g1"] else cfg["label_of"](g)
        dr.text((x + 4, y + 3), "g %d  %.2f s  %s" % (g, g / 30.0, tag), fill=(255, 255, 255))
    S.save(os.path.join(here, "contact.jpg"), quality=88)
    pairs = cfg["compare"]
    w, h, lab = 360, 640, 20
    Cm = Image.new("RGB", (len(pairs) * 2 * w + (len(pairs) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm)
    x = 0
    for g, ref in pairs:
        Cm.paste(Image.open(os.path.join(out, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
        dr.text((x + 4, 4), "%s g %d (%.2f s)" % (cfg["take"], g, g / 30.0), fill=(255, 255, 255))
        Cm.paste(Image.open(os.path.join(proj, "ref", ref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
        dr.text((x + w + 4, 4), "ref %s" % ref, fill=(255, 220, 160))
        x += 2 * w + 12
    Cm.save(os.path.join(here, "compare.jpg"), quality=88)
    # QA numbers
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        print("%s: g %d..%d (%d frames), shots %s" % (cfg["take"], ga, gb, len(gs), cfg["shots"]))
        names = sorted({n for r in rows for n in r["heads"]})
        for n in names:
            hs = [(r["g"], r["heads"][n]) for r in rows if n in r["heads"]]
            vis = [(g, q) for g, q in hs if -q["w"] / 2 < q["x"] < 720 + q["w"] / 2 and q["y"] - q["w"] / 2 < 1280]
            if not vis:
                continue
            wv = [q["w"] for g, q in vis]; yv = [q["y"] for g, q in vis]; xv = [q["x"] for g, q in vis]
            low = [g for g, q in vis if q["y"] + q["w"] / 2 > 880]
            print("  %-9s head w %4.0f..%4.0f px, centre x %4.0f..%4.0f, y %4.0f..%4.0f (%.2f..%.2f H); bottom below 880: %s"
                  % (n, min(wv), max(wv), min(xv), max(xv), min(yv), max(yv), min(yv) / 1280, max(yv) / 1280,
                     (low[0], low[-1], len(low)) if low else "none"))
        print("  render: wall %.2f s, cpu %.2f s per frame (mean); retried: %s" % (np.mean(walls), np.mean(cpus), [r["g"] for r in rows if r.get("retried")]))
        prev = None; d = []
        for g in gs:
            a = np.asarray(Image.open(os.path.join(out, "g_%04d.png" % g)).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
            if prev is not None:
                d.append((g, float(np.abs(a - prev).mean())))
            prev = a
        cuts = set(cfg["cuts"])
        pops = []
        for i, (g, v) in enumerate(d):
            p = d[i - 1][1] if i else v; nx = d[i + 1][1] if i + 1 < len(d) else v
            if v > 1.8 * p and v > 1.8 * nx and v > 1.0 and g not in cuts:
                pops.append((g - 1, g, round(v, 1)))
        print("  popcheck (cuts %s excluded): %s" % (sorted(cuts), pops))
        st = [g for g, v in d if v < 0.35]
        print("  near-still transitions (< 0.35 levels): %s" % st)
        print("  frame change median %.2f, max %.2f levels" % (float(np.median([v for g, v in d])), max(v for g, v in d)))
        bad = []
        for g in gs:
            a = np.asarray(Image.open(os.path.join(out, "g_%04d.png" % g)).convert("RGB").resize((90, 160)), dtype=np.int16)
            if ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean() > 0.002 or (a.max(axis=2) < 6).mean() > 0.2:
                bad.append(g)
        print("  magenta / black frames: %s" % bad)
        print()
        print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
        for label, (a, b) in cfg["hue_rows"]:
            H.row(label, [os.path.join(out, "g_%04d.png" % g) for g in range(a, b + 1)])
        for label, refs in cfg.get("hue_refs", []):
            H.row(label, [os.path.join(proj, "ref", r) for r in refs])
    os.makedirs(os.path.join(here, "work"), exist_ok=True)
    open(os.path.join(here, "work", "qa.txt"), "w").write(buf.getvalue())
    print(buf.getvalue())
    mkv = os.path.join(here, "take.mkv")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(ga), "-i", os.path.join(out, "g_%04d.png"),
                    "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
    print("delivered %d frames + take.mkv; mean wall %.2f s, cpu %.2f s" % (len(gs), np.mean(walls), np.mean(cpus)))

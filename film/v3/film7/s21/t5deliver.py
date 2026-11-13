#!/usr/bin/env python3
"""t5deliver.py -- delivery + QA numbers for takes s21 / s23 / s25 (render team 5), after film7/s01/deliver.py + qa.py.
deliver(cfg): raw/s<id>/g_*.png -> frames/g_%04d.png, meta.json, cues.json, contact.jpg, compare.jpg, take.mkv, work/qa.txt.
cfg keys: here, take, shots, g0, g1, handle, setups {id: (ga, gb, label)}, transition_in, transition_out, events, cues [(g0, g1, label,
kind)], compare [(g, ref 'a'|'b', tref)], set, light, cast, extra (dict merged into meta)."""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

V3 = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
PROJ = os.path.dirname(V3)
sys.path.insert(0, os.path.join(V3, "tools"))


def deliver(cfg):
    here, H = cfg["here"], cfg["handle"]
    first, last = cfg["g0"] - H, cfg["g1"] + H - 1
    N = last - first + 1
    out = os.path.join(here, "frames"); os.makedirs(out, exist_ok=True)
    rows, src = [], {}
    for sid, (ga, gb, lab) in cfg["setups"].items():
        for g in range(ga, gb + 1):
            raw = os.path.join(here, "raw", "s%d" % sid)
            shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(out, "g_%04d.png" % g))
            rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g)))); src[g] = sid
    assert sorted(src) == list(range(first, last + 1)), "missing frames"
    walls = [r["wall"] for r in rows]; cpus = [r["cpu"] for r in rows]
    meta = {"take": cfg["take"], "film": 7, "shots": cfg["shots"], "first_g": first, "n_frames": N, "g0": cfg["g0"], "g1": cfg["g1"],
            "handle_in": H, "handle_out": H, "transition_in": cfg["transition_in"], "transition_out": cfg["transition_out"],
            "shot_ranges": cfg["shot_ranges"],
            "setups": {str(k): {"g": [v[0], v[1]], "what": v[2]} for k, v in cfg["setups"].items()},
            "events": cfg["events"], "set": cfg["set"], "light": cfg["light"], "cast": cfg["cast"],
            "dof": "none (client rule: cam.data.dof.use_dof False + L.setup_dof(scene, None, None, cam=cam) at build and before every render)",
            "denoiser": "OpenImageDenoise, albedo+normal, prefilter FAST",
            "narration": "film7/audio/narration_bankky.wav at +0.10 s; captions film7/script/captions.json",
            "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
            "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2)}
    meta.update(cfg.get("extra", {}))
    json.dump(meta, open(os.path.join(here, "meta.json"), "w"), indent=1, ensure_ascii=False)

    ev = []
    for g0, g1, lab, kind in cfg["cues"]:
        ev.append(dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=lab))
    json.dump(dict(take=cfg["take"], fps=30, note="time = film seconds (g / 30); narration film7/audio/narration_bankky.wav at +0.10 s", cues=ev),
              open(os.path.join(here, "cues.json"), "w"), indent=1, ensure_ascii=False)

    # contact sheet: 16 evenly spaced frames, label strip above, cyan y 880 line
    gs = [first + int(round(i * (N - 1) / 15.0)) for i in range(16)]
    w, h, lab, cols = 270, 480, 18, 8
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
    for i, g in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(os.path.join(out, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
        hd = " handle" if g < cfg["g0"] or g >= cfg["g1"] else ""
        dr.text((x + 4, y + 3), "g %d  %.2f s  set-up %d%s" % (g, g / 30.0, src[g], hd), fill=(255, 255, 255))
    S.save(os.path.join(here, "contact.jpg"), quality=88)

    w, h, lab = 360, 640, 20
    P = cfg["compare"]
    Cm = Image.new("RGB", (len(P) * 2 * w + (len(P) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm); x = 0
    for g, rs, tref in P:
        Cm.paste(Image.open(os.path.join(out, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
        dr.text((x + 4, 4), "%s g %d (%.2f s)" % (cfg["take"], g, g / 30.0), fill=(255, 255, 255))
        Cm.paste(Image.open(os.path.join(PROJ, "ref", rs, "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
        dr.text((x + w + 4, 4), "ref %s t%04d" % (rs, tref), fill=(255, 220, 160))
        x += 2 * w + 12
    Cm.save(os.path.join(here, "compare.jpg"), quality=88)

    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(first), "-i", os.path.join(out, "g_%04d.png"),
                    "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", os.path.join(here, "take.mkv")], check=True)
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames,width,height",
                        "-of", "csv=p=0", os.path.join(here, "take.mkv")], capture_output=True, text=True)
    qa(cfg, rows, src, out, first, last, r.stdout.strip())


def qa(cfg, rows, src, out, first, last, probe):
    import io, contextlib, hue_report as HR
    buf = io.StringIO()
    p = lambda *a: print(*a, file=buf)
    p("take %s: frames g %d..%d (%d), take.mkv %s" % (cfg["take"], first, last, last - first + 1, probe))
    for sid, (ga, gb, lab) in cfg["setups"].items():
        rs = [r for r in rows if r["shot"] == sid]
        p("set-up %d g %d..%d %s" % (sid, ga, gb, lab))
        for n in sorted({n for r in rs for n in r.get("heads", {})}):
            hs = [(r["g"], r["heads"][n]) for r in rs if n in r["heads"] and -40 < r["heads"][n]["x"] < 760]
            if not hs:
                continue
            ws = [v["w"] for g, v in hs]; ys = [v["y"] for g, v in hs]; xs = [v["x"] for g, v in hs]
            low = [g for g, v in hs if v["y"] + v["w"] / 2 > 880]
            p("  %-7s head w %4.0f..%4.0f px, x %4.0f..%4.0f, y %4.0f..%4.0f (%.2f..%.2f H); bottom below 880: %s" % (
                n, min(ws), max(ws), min(xs), max(xs), min(ys), max(ys), min(ys) / 1280, max(ys) / 1280, (low[0], low[-1], len(low)) if low else "none"))
        p("  render: wall %.2f s, cpu %.2f s per frame" % (np.mean([r["wall"] for r in rs]), np.mean([r["cpu"] for r in rs])))
    p("all: wall %.2f s, cpu %.2f s per frame; retried: %s" % (np.mean([r["wall"] for r in rows]), np.mean([r["cpu"] for r in rows]),
                                                               [r["g"] for r in rows if r.get("retried")]))
    fs = [os.path.join(out, "g_%04d.png" % g) for g in range(first, last + 1)]
    prev, d = None, []
    for f in fs:
        a = np.asarray(Image.open(f).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
        if prev is not None:
            d.append(float(np.abs(a - prev).mean()))
        prev = a
    pops = []
    for i, v in enumerate(d):
        pv = d[i - 1] if i else v; nx = d[i + 1] if i + 1 < len(d) else v
        if v > 1.8 * pv and v > 1.8 * nx and v > 1.0:
            pops.append((first + i, first + i + 1, round(v, 1)))
    cuts = [ga for sid, (ga, gb, lab) in cfg["setups"].items()][1:]
    p("popcheck (g -> g+1, change): %s   planned cuts at %s" % (pops, cuts))
    p("near-still transitions (< 0.35 levels): %s" % [first + i for i, v in enumerate(d) if v < 0.35])
    runs, r0 = [], None
    for i, v in enumerate(d + [9]):
        if v < 0.35 and r0 is None:
            r0 = i
        elif v >= 0.35 and r0 is not None:
            runs.append((first + r0, first + i, i - r0)); r0 = None
    p("still runs (start, end, frames): %s" % runs)
    p("frame change median %.2f, max %.2f levels" % (float(np.median(d)), max(d)))
    bad = []
    for f in fs:
        a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
        mag = ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean(); blk = (a.max(axis=2) < 6).mean()
        if mag > 0.002 or blk > 0.2:
            bad.append(os.path.basename(f))
    p("magenta / black frames: %s" % bad)
    p("")
    p(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in HR.NAMES) + "   sat  val dark")
    with contextlib.redirect_stdout(buf):
        for sid, (ga, gb, lab) in cfg["setups"].items():
            HR.row("%s set-up %d (g %d-%d)" % (cfg["take"], sid, ga, gb), [os.path.join(out, "g_%04d.png" % g) for g in range(ga, gb + 1)])
        HR.row("%s all" % cfg["take"], fs)
        for g, rs, tref in cfg["compare"]:
            HR.row("ref %s t%04d" % (rs, tref), [os.path.join(PROJ, "ref", rs, "t%04d.jpg" % tref)])
    os.makedirs(os.path.join(cfg["here"], "work"), exist_ok=True)
    open(os.path.join(cfg["here"], "work", "qa.txt"), "w").write(buf.getvalue())
    print(buf.getvalue())

#!/usr/bin/env python3
"""build.py -- shot file -> frame SVGs + manifest + captions JSON + QA numbers (stdlib only).

    python3 build.py [shots/s01.py] [--out out] [--only s02] [--frames 80-96]

Writes  <out>/svg/<shot>_<gggg>.svg     one SVG document per raw frame (g = output frame number, handles included)
        <out>/manifest.json            what render.js rasterises and what post.py mixes
        <out>/caps.json                the caption phrases (t0, t1, text)
        <out>/caps_burn.json           the same phrases with the libass size calibration, the file given to assemble.py
        <out>/qa.json                  per-frame staging numbers (pencil / eraser registration, heads, camera speed)
"""
import importlib.util, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import compositor                      # noqa: E402

W, H = 720, 1280
CAPTION_FS = 70            # libass font size that reproduces the reference caption size (see tools/caption_check.py)


def load_shots(path):
    sp = importlib.util.spec_from_file_location("shotfile", path)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def corner_speed(cam_prev, cam):
    """zoom rate (percent per second), pan (px per second) and corner speed (px per second), as in camera_motion.md."""
    zr = (cam[2] / cam_prev[2] - 1.0) * 30 * 100
    pan = math.hypot((cam[0] - cam_prev[0]) * cam[2], (cam[1] - cam_prev[1]) * cam[2]) * 30
    return zr, pan, abs(zr) / 100.0 * 734 + pan


def main(argv):
    shot_path = os.path.join(HERE, "shots", "s01.py")
    out = os.path.join(HERE, "out")
    only = None
    rng = None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--out":
            out = os.path.abspath(argv[i + 1]); i += 1
        elif a == "--only":
            only = set(argv[i + 1].split(",")); i += 1
        elif a == "--frames":
            lo, hi = argv[i + 1].split("-"); rng = (int(lo), int(hi)); i += 1
        else:
            shot_path = os.path.abspath(a)
        i += 1
    S = load_shots(shot_path)
    svg_dir = os.path.join(out, "svg")
    raw_dir = os.path.join(out, "raw")
    os.makedirs(svg_dir, exist_ok=True)
    os.makedirs(raw_dir, exist_ok=True)
    frames = []
    qa = []
    for shot in S.SHOTS:
        name = shot["name"]
        fn, cam_fn = S.SHOT_FN[name], S.CAM_FN[name]
        for g in S.frames_of(shot):
            rec = dict(shot=name, g=g, svg=os.path.join(svg_dir, "%s_%04d.svg" % (name, g)), out=os.path.join(raw_dir, "%s_%04d.png" % (name, g)))
            frames.append(rec)
            if (only and name not in only) or (rng and not (rng[0] <= g <= rng[1])):
                continue
            spec = fn(g)
            spec["cam_prev"] = cam_fn(g - 1)
            svg, info = compositor.scene(spec, with_info=True)
            open(rec["svg"], "w").write(svg)
            cam = info["cam"]
            zr, pan, cs = corner_speed(compositor.cam4(spec["cam_prev"]), cam)
            q = dict(shot=name, g=g, cam=[round(v, 4) for v in cam[:3]], zoom_rate=round(zr, 1), pan=round(pan, 1), corner=round(cs, 1),
                     plate_shift=round(info.get("plate_shift", 0.0), 1), blur=info["blur"], line=round(spec["state"]["line"], 4),
                     erase=round(spec["state"]["erase"], 4), actors={})
            built = compositor.build_set(spec.get("set", "office"), spec["state"])
            pt, le = built["anchors"]["pencil_tip"], built["anchors"]["line_end"]
            for uid, a in info["actors"].items():
                wd, sc = a["world"], a["screen"]
                d_px = a["scale"] * cam[2]
                aq = dict(head=[round(v, 1) for v in sc["head"]], head_world=[round(v, 4) for v in wd["head"]], D_px=round(d_px, 1),
                          head_bottom=round(sc["head"][1] + 0.51 * d_px, 1), feet=[round(v, 1) for v in sc["feet"]], scale=a["scale"])
                for side in ("r", "l"):
                    tip = wd["prop_tip_" + side]
                    aq["tip_" + side] = [round(v, 4) for v in tip]
                    aq["tip_%s_to_pencil_px" % side] = round(math.hypot(tip[0] - pt[0], tip[1] - pt[1]) * cam[2], 2)
                    aq["tip_%s_to_line_end_px" % side] = round(math.hypot(tip[0] - le[0], tip[1] - le[1]) * cam[2], 2)
                q["actors"][uid] = aq
            qa.append(q)
    man = dict(width=W, height=H, fps=S.FPS, n_frames=S.N_FRAMES, frames=frames,
               timeline=[S.source_of(g) for g in range(S.N_FRAMES)], transitions=S.TRANSITIONS,
               shots=S.SHOTS)
    json.dump(man, open(os.path.join(out, "manifest.json"), "w"))
    json.dump([dict(t0=a, t1=b, text=t) for a, b, t in S.CAPS], open(os.path.join(out, "caps.json"), "w"), indent=1)
    # the same phrases with the size calibration for the burn-in: assemble.py asks libass for "Fontsize 50", which libass
    # measures on the font's full line box, so Work Sans Black comes out at 0.71 of the reference width.  The override
    # \fs70 gives the measured reference size (phrase widths within 1 percent) without touching the tool.
    json.dump([dict(t0=a, t1=b, text="{\\fs%d}%s" % (CAPTION_FS, t)) for a, b, t in S.CAPS], open(os.path.join(out, "caps_burn.json"), "w"), indent=1)
    if not only and not rng:
        json.dump(qa, open(os.path.join(out, "qa.json"), "w"))
    print("built %d SVG frame(s) for %d output frames -> %s" % (len(qa), S.N_FRAMES, svg_dir))
    return qa


if __name__ == "__main__":
    main(sys.argv[1:])

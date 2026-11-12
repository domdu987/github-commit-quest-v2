"""deliver_common.py -- raw/g_*.png (+ json) -> frames/g_%04d.png, take.mkv, meta.json, cues.json, contact.jpg, hue rows."""
import os, sys, json, glob, shutil, subprocess
from PIL import Image, ImageDraw


def deliver(here, take, shots, g0, g1, h_in, h_out, light, extra_meta, cues, n_contact=16):
    raw = os.path.join(here, "raw"); out = os.path.join(here, "frames")
    os.makedirs(out, exist_ok=True)
    first, last = g0 - h_in, g1 + h_out - 1
    rows = []
    for g in range(first, last + 1):
        png = os.path.join(raw, "g_%04d.png" % g); js = os.path.join(raw, "g_%04d.json" % g)
        if not (os.path.exists(png) and os.path.exists(js)):
            sys.exit("missing raw frame %d" % g)
        m = json.load(open(js))
        if m.get("scale") != 1.0 or m.get("samples") != 12:
            sys.exit("frame %d is not final quality" % g)
        im = Image.open(png)
        if im.size != (720, 1280):
            sys.exit("frame %d size %s" % (g, im.size))
        shutil.copyfile(png, os.path.join(out, "g_%04d.png" % g)); rows.append(m)
    n = last - first + 1
    mkv = os.path.join(here, "take.mkv")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(first), "-i",
                    os.path.join(out, "g_%04d.png"), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
    walls = [r["wall"] for r in rows]; cpus = [r["cpu"] for r in rows]
    meta = {"take": take, "shots": shots, "g0": g0, "g1": g1, "handle_in": h_in, "handle_out": h_out,
            "first_g": first, "n_frames": n,
            "transition_in": {"type": "dissolve", "frames": 10, "note": "handle g %d..%d rendered in 3D" % (first, g0 - 1)},
            "transition_out": {"type": "dissolve", "frames": 10, "note": "handle g %d..%d rendered in 3D" % (g1, last)},
            "shot_ranges": {str(shots[0]): [g0, g1 - 1]},
            "set": "v3/set3d2/tower.py", "light": light, "samples": 12, "resolution": [720, 1280], "threads": 2,
            "s_per_frame_wall_mean": round(sum(walls) / n, 2), "s_per_frame_cpu_mean": round(sum(cpus) / n, 2),
            "file": "take.mkv (libx264rgb crf 6), frames/ not in git"}
    meta.update(extra_meta)
    json.dump(meta, open(os.path.join(here, "meta.json"), "w"), indent=1, ensure_ascii=False)
    for c in cues:
        c.setdefault("duration", 0.0)
        c["time"] = round(c["frame"] / 30.0, 3)
        c["end_frame"] = c["frame"] + int(round(c["duration"] * 30))
    json.dump({"take": take, "fps": 30, "note": "time = film seconds (g / 30); narration at +0.10 s", "cues": cues},
              open(os.path.join(here, "cues.json"), "w"), indent=1, ensure_ascii=False)
    # contact sheet: labels in a strip above each picture
    gs = [first + round(i * (n - 1) / (n_contact - 1)) for i in range(n_contact)]
    cols = 8; w = 180; hh = 320; lab = 16
    S = Image.new("RGB", (cols * w, ((n_contact + cols - 1) // cols) * (hh + lab)), (20, 16, 24)); dr = ImageDraw.Draw(S)
    for i, g in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * (hh + lab)
        S.paste(Image.open(os.path.join(out, "g_%04d.png" % g)).convert("RGB").resize((w, hh), Image.LANCZOS), (x, y + lab))
        dr.text((x + 3, y + 2), "g%d  %.2fs" % (g, g / 30.0), fill=(255, 255, 255))
    S.save(os.path.join(here, "contact.jpg"), quality=88)
    sys.path.insert(0, os.path.join(here, "..", "..", "tools"))
    import hue_report as Hr
    print(f"{'set':44s} " + " ".join(f"{k[:6]:>6s}" for k in Hr.NAMES) + "   sat  val dark")
    Hr.row("%s all (g %d-%d)" % (take, first, last), sorted(glob.glob(os.path.join(out, "*.png"))))
    print("delivered %s: %d frames g %d..%d, %.2f s wall / %.2f s cpu per frame" % (take, n, first, last, meta["s_per_frame_wall_mean"], meta["s_per_frame_cpu_mean"]))
    return meta

#!/usr/bin/env python3
"""deliver.py -- take s31 (shots 31-32): raw/s31 + raw/s32 (MORNING) + raw/s33 (AFTERNOON, dissolve) -> frames/g_%04d.png, contact.jpg, compare.jpg, take.mkv,
meta.json, cues.json, work/qa.txt (pops, heads, colour rows).  Shared shape with s31/deliver.py (CFG differs)."""
import os, sys, json, glob, subprocess, shutil
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(PROJ, "v3", "tools"))

CFG = dict(
    take="s31", shots=[31, 32], first_g=2581, last_g=2841, g0=2587, g1=2836,
    sources=[((2581, 2714), "s31"), ((2715, 2780), "s32"), ((2793, 2841), "s33")],
    dissolves=[(2781, 2792, "s32", "s33")],               # MORNING -> AFTERNOON, same lens / push
    shot_ranges={"31": [2587, 2714], "32": [2715, 2835]},
    cuts=[2630, 2673, 2715, 2751],
    contact=[2581, 2600, 2620, 2630, 2645, 2660, 2672, 2673, 2690, 2705, 2714, 2715, 2730, 2750, 2751, 2775, 2786, 2795, 2805, 2815, 2826, 2841],
    compare=[(2700, 101, "ref a t0101 (mechanism ECU)"), (2826, 106, "ref a t0106 (mechanism ECU)")],
)


def raw_of(g):
    for (a, b), d in CFG["sources"]:
        if a <= g <= b:
            return os.path.join(HERE, "raw", d, "g_%04d.png" % g)
    raise KeyError(g)


def build_frames():
    out = os.path.join(HERE, "frames")
    os.makedirs(out, exist_ok=True)
    walls, cpus, src = [], [], {}
    for g in range(CFG["first_g"], CFG["last_g"] + 1):
        dst = os.path.join(out, "g_%04d.png" % g)
        dis = [d for d in CFG["dissolves"] if d[0] <= g <= d[1]]
        if dis:
            a, b, sa, sb = dis[0]
            u = (g - a + 1) / float(b - a + 2)
            A = np.asarray(Image.open(os.path.join(HERE, "raw", sa, "g_%04d.png" % g)).convert("RGB"), dtype=np.float32)
            Bm = np.asarray(Image.open(os.path.join(HERE, "raw", sb, "g_%04d.png" % g)).convert("RGB"), dtype=np.float32)
            Image.fromarray(np.clip(A * (1 - u) + Bm * u + 0.5, 0, 255).astype(np.uint8)).save(dst)
            src[str(g)] = "%s*%.3f+%s*%.3f" % (sa, 1 - u, sb, u)
            for s_ in (sa, sb):
                m = json.load(open(os.path.join(HERE, "raw", s_, "g_%04d.json" % g)))
                walls.append(m["wall"]); cpus.append(m["cpu"])
        else:
            p = raw_of(g)
            Image.open(p).convert("RGB").save(dst)
            src[str(g)] = os.path.basename(os.path.dirname(p))
            m = json.load(open(p[:-4] + ".json"))
            walls.append(m["wall"]); cpus.append(m["cpu"])
    return out, src, float(np.mean(walls)), float(np.mean(cpus))


def popcheck(out):
    prev, rows = None, []
    for g in range(CFG["first_g"], CFG["last_g"] + 1):
        im = np.asarray(Image.open(os.path.join(out, "g_%04d.png" % g)).convert("L").resize((180, 320)), dtype=np.float32)
        if prev is not None:
            rows.append((g, float(np.abs(im - prev).mean())))
        prev = im
    return rows


def main():
    out, src, wall, cpu = build_frames()
    pops = popcheck(out)
    cuts = set(CFG["cuts"])
    inshot = [d for g, d in pops if g not in cuts]
    still = [g for g, d in pops if g not in cuts and d < 0.15]
    big = [(g, round(d, 1)) for g, d in pops if g not in cuts and d > 12]
    w, h, lab = 240, 427, 18
    cols = 6
    fr = CFG["contact"]
    rows = (len(fr) + cols - 1) // cols
    S = Image.new("RGB", (cols * w, rows * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
    for i, g in enumerate(fr):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(os.path.join(out, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        tag = " handle" if (g < CFG["g0"] or g >= CFG["g1"]) else ""
        dr.text((x + 4, y + 3), "g %d  %.2f s%s" % (g, g / 30.0, tag), fill=(255, 255, 255))
        dr.line([(x, y + lab + int(h * 880 / 1280)), (x + w, y + lab + int(h * 880 / 1280))], fill=(255, 80, 80))
    S.save(os.path.join(HERE, "contact.jpg"), quality=88)
    w, h = 360, 640
    Cm = Image.new("RGB", (len(CFG["compare"]) * 2 * w + 12 * (len(CFG["compare"]) - 1), h + 20), (16, 12, 20)); dr = ImageDraw.Draw(Cm)
    x = 0
    for g, t, label in CFG["compare"]:
        Cm.paste(Image.open(os.path.join(out, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, 20))
        dr.text((x + 4, 4), "%s g %d" % (CFG["take"], g), fill=(255, 255, 255))
        Cm.paste(Image.open(os.path.join(PROJ, "ref", "a", "t%04d.jpg" % t)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, 20))
        dr.text((x + w + 4, 4), label, fill=(255, 220, 160))
        x += 2 * w + 12
    Cm.save(os.path.join(HERE, "compare.jpg"), quality=88)
    # colour rows
    import io, contextlib, hue_report as HR
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        for k, (a, b) in CFG["shot_ranges"].items():
            HR.row("%s shot %s (g %d-%d)" % (CFG["take"], k, a, b), [os.path.join(out, "g_%04d.png" % g) for g in range(a, b + 1)])
        HR.row("reference A, whole clip", sorted(glob.glob(PROJ + "/ref/a/*.jpg")))
    hue = buf.getvalue()
    # heads from the raw json reports
    heads = {}
    for g in range(CFG["first_g"], CFG["last_g"] + 1):
        try:
            m = json.load(open(raw_of(g)[:-4] + ".json"))
        except Exception:
            continue
        for n, v in (m.get("heads") or {}).items():
            if v["x"] < -v["w"] / 2 or v["x"] > 720 + v["w"] / 2:
                continue
            e = heads.setdefault(n, dict(w=[], y=[], bottom=[]))
            e["w"].append(v["w"]); e["y"].append(v["y"]); e["bottom"].append(v["y"] + v["w"] / 2)
    hs = {n: dict(w=[min(e["w"]), max(e["w"])], y=[min(e["y"]), max(e["y"])], max_bottom=max(e["bottom"])) for n, e in heads.items()}
    qa = dict(pops=dict(median=float(np.median(inshot)), max=float(np.max(inshot)), still_pairs=still, big=big,
                        cut_diffs=[(g, round(d, 1)) for g, d in pops if g in cuts]), heads=hs, wall=wall, cpu=cpu)
    os.makedirs(os.path.join(HERE, "work"), exist_ok=True)
    open(os.path.join(HERE, "work", "qa.txt"), "w").write(json.dumps(qa, indent=1) + "\n" + hue)
    print(json.dumps(qa, indent=1)); print(hue)
    mkv = os.path.join(HERE, "take.mkv")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(CFG["first_g"]),
                    "-i", os.path.join(out, "g_%04d.png"), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
    meta = json.load(open(os.path.join(HERE, "meta_base.json")))
    meta.update(first_g=CFG["first_g"], n_frames=CFG["last_g"] - CFG["first_g"] + 1, s_per_frame_wall_mean=round(wall, 2),
                s_per_frame_cpu_mean=round(cpu, 2), frame_source=src)
    json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
    print("delivered", CFG["last_g"] - CFG["first_g"] + 1, "frames + take.mkv")


if __name__ == "__main__":
    main()

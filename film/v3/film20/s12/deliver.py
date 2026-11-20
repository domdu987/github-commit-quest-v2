#!/usr/bin/env python3
"""deliver.py -- take delivery from raw/g_%04d.png (+ .json): optional post (speed lines), frames/, take.mkv (libx264rgb crf 6, split if
> 45 MB), meta.json, cues.json, contact.jpg, framediff.json, then qa_auto.py.  No bpy.   python3 deliver.py | python3 deliver.py draft"""
import os, sys, json, glob, shutil, subprocess, math, random
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
CFG = json.load(open(os.path.join(HERE, "cfg.json")))
G0, G1, HIN, HOUT = CFG["g0"], CFG["g1"], CFG["h_in"], CFG["h_out"]
GF, GL = G0 - HIN, G1 + HOUT - 1
N = GL - GF + 1
MB_LIMIT = 45e6


def speed_lines(img, g, g0, n=6):
    """post: radial speed lines on the 6 frames after the punch-in cut (g0..g0+n-1), drawn toward the centre of Eiffel (no text)"""
    k = g - g0
    if not (0 <= k < n):
        return img
    W, H = img.size
    cx, cy = 360, 700
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    rnd = random.Random(100 + k)
    for i in range(46):
        a = rnd.uniform(0, 2 * math.pi)
        r0 = rnd.uniform(230, 330) * (1.0 + 0.15 * k)
        r1 = r0 + rnd.uniform(240, 520)
        w = rnd.uniform(0.012, 0.03)
        col = (255, 248, 228, 215) if i % 3 else (40, 24, 30, 190)
        p = [(cx + math.cos(a - w) * r0, cy + math.sin(a - w) * r0), (cx + math.cos(a) * r1, cy + math.sin(a) * r1),
             (cx + math.cos(a + w) * r0, cy + math.sin(a + w) * r0)]
        d.polygon(p, fill=col)
    out = img.convert("RGBA")
    out.alpha_composite(ov)
    return out.convert("RGB")


def post(g, png):
    img = Image.open(png).convert("RGB")
    if CFG.get("speed_g0") is not None:
        img = speed_lines(img, g, CFG["speed_g0"])
    return img


def framediff(arrs):
    return [float(np.abs(arrs[i] - arrs[i - 1]).mean()) for i in range(1, len(arrs))]


def grey(img):
    return np.asarray(img.resize((90, 160), Image.BILINEAR), dtype=np.float32).mean(-1)


def contact(pngs, out, gs, cols=8, w=270):
    h, lab = w * 16 // 9, 18
    idx = [int(round(i * (len(pngs) - 1) / 15.0)) for i in range(16)]
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20))
    dr = ImageDraw.Draw(S)
    for i, j in enumerate(idx):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(pngs[j]).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
        g = gs[j]
        dr.text((x + 4, y + 3), "g %d  %.2f s%s" % (g, g / 30.0, "  handle" if (g < G0 or g >= G1) else ""), fill=(255, 255, 255))
    S.save(out, quality=88)


draft = len(sys.argv) > 1 and sys.argv[1] == "draft"
RAW = os.path.join(HERE, "work", "draft") if draft else os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "work", "draft_frames") if draft else os.path.join(HERE, "frames")
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
gs = list(range(GF, GL + 1))
rows = []
for g in gs:
    img = post(g, os.path.join(RAW, "g_%04d.png" % g))
    img.save(os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
pngs = [os.path.join(OUT, "g_%04d.png" % g) for g in gs]
arrs = [grey(Image.open(p).convert("RGB")) for p in pngs]
d = framediff(arrs)                       # d[i] = pair (gs[i], gs[i+1])
cut_pairs = set(CFG.get("skip_pairs", []))   # pair second-frame g's that straddle a planned cut inside the shot (kept: a cut IS motion)
ins = [d[i] for i in range(len(d)) if G0 < gs[i + 1] <= G1 - 1]
nb = dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), 90x160 bilinear, 0-255; pairs (g-1,g) for g in first_g+1 ..g1-1 of the take's shots (in-shot, handles excluded)",
          median=round(float(np.median(ins)), 2), p90=round(float(np.percentile(ins, 90)), 2), min=round(float(min(ins)), 2), max=round(float(max(ins)), 2),
          target=dict(median=4.0, p90=12.0), per_pair=[round(v, 2) for v in d])
if draft:
    print("draft frame-diff median %.2f p90 %.2f min %.2f max %.2f" % (nb["median"], nb["p90"], nb["min"], nb["max"]))
    contact(pngs, os.path.join(HERE, "work", "draft_contact.jpg"), gs)
    sys.exit(0)
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
heads = [h for r in rows[HIN:len(rows) - HOUT] for h in r["heads"].values() if CFG.get("head_check", True)] or [dict(w=0, y=0, bottom=0)]
meta = dict(take=CFG["take"], film=20, shots=CFG["shots"], g0=G0, g1=G1, first_g=GF, n_frames=N, shot_ranges=CFG["shot_ranges"],
            handle_in=HIN, handle_out=HOUT, transition_in=CFG["transition_in"], transition_out=CFG["transition_out"],
            set=CFG["set"], cast=CFG["cast"], camera=CFG["camera"], events=CFG["events"], dof="none", text="none", light="DAY",
            samples=rows[0].get("samples"), resolution=[720, 1280], threads=2, fps=30,
            s_per_frame_wall_mean=round(float(np.mean(walls)), 2), s_per_frame_cpu_mean=round(float(np.mean(cpus)), 2),
            head_px=[round(min(h["w"] for h in heads)), round(max(h["w"] for h in heads))],
            head_centre_y=[round(min(h["y"] for h in heads)), round(max(h["y"] for h in heads))],
            head_bottom_max_y=round(max(h["bottom"] for h in heads)),
            framediff_in_shot=dict(median=nb["median"], p90=nb["p90"]),
            narration="film20/audio/narration.wav at +0.10 s; captions film20/script/captions.json")
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
json.dump(dict(take=CFG["take"], fps=30, note="t = film seconds (g / 30); narration film20/audio/narration.wav at +0.10 s",
               cues=[dict(kind=c[2], t=round(c[0] / 30.0, 3), dur=round(max(0, c[1] - c[0]) / 30.0, 3), frame=c[0], end_frame=c[1], note=c[3]) for c in CFG["cues"]]),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
contact(pngs, os.path.join(HERE, "contact.jpg"), gs)
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(GF), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
if os.path.getsize(mkv) > MB_LIMIT:
    subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True, cwd=HERE)
    print("take.mkv %.1f MB: split into take.mkv.part*" % (os.path.getsize(mkv) / 1e6))
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(GF), "--cuts", ",".join(map(str, CFG["cuts"]))],
                   capture_output=True, text=True)
print(r.stdout[-2500:])
print("delivered %d frames, take.mkv %.1f MB; s/frame wall %.2f cpu %.2f; frame-diff median %.2f p90 %.2f"
      % (N, os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))

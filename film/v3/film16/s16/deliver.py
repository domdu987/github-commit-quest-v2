#!/usr/bin/env python3
"""deliver.py -- generic film-16 take delivery from raw/g_%04d.png (+ .json): frames/, take.mkv (libx264rgb crf 6), meta.json, cues.json,
contact.jpg (16 frames, cyan = caption band y 880), framediff.json, qa_auto.py (-> QA_AUTO.md + phone_sheet.jpg).  No bpy.
    python3 deliver.py             final delivery           python3 deliver.py draft   look at work/draft (nothing delivered)
Take constants come from take.cfg.json (take, shots, g0, g1 exclusive, handle, events, cues, set, cast, camera, light)."""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
CFG = json.load(open(os.path.join(HERE, "take.cfg.json")))
G0, G1, H = CFG["g0"], CFG["g1"], CFG["handle"]
FIRST, LAST = G0 - H, G1 + H - 1
N = LAST - FIRST + 1


def framediff(pngs, skip=()):
    prev, d = None, []
    for i, p in enumerate(pngs):
        a = np.asarray(Image.open(p).convert("RGB").resize((90, 160), Image.BILINEAR), dtype=np.float32).mean(-1)
        if prev is not None:
            d.append(float(np.abs(a - prev).mean()))
        prev = a
    return d


def contact(pngs, out, cols=8, w=270):
    h, lab = w * 16 // 9, 18
    ins = list(range(H, H + G1 - G0))
    gs = [ins[int(round(i * (len(ins) - 1) / 15.0))] for i in range(16)]
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
    for i, k in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(pngs[k]).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
        dr.text((x + 4, y + 3), "g %d  %.2f s" % (FIRST + k, (FIRST + k) / 30.0), fill=(255, 255, 255))
    S.save(out, quality=88)


def numbers(d):
    ins = d[H:H + (G1 - G0) - 1]          # pairs inside the shot proper (frame H = first shot frame; pair (H-1,H) straddles the cut)
    return dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), 90x160 bilinear, 0-255 levels; in-shot pairs only (no handles)",
                median=round(float(np.median(ins)), 2), p90=round(float(np.percentile(ins, 90)), 2), min=round(float(min(ins)), 2),
                max=round(float(max(ins)), 2), target=dict(median=4.0, p90=12.0), per_pair=[round(v, 2) for v in d])


if len(sys.argv) > 1 and sys.argv[1] == "draft":
    src = sorted(glob.glob(os.path.join(HERE, "work", "draft", "g_*.png")))
    contact(src, os.path.join(HERE, "work", "draft_contact.jpg"))
    nb = numbers(framediff(src)); print("draft frame-diff median %.2f p90 %.2f" % (nb["median"], nb["p90"])); sys.exit(0)

RAW, OUT = os.path.join(HERE, "raw"), os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)
rows = []
for g in range(FIRST, LAST + 1):
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
pngs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(FIRST, LAST + 1)]
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
nb = numbers(framediff(pngs))
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)
heads = {}
for r in rows[H:H + G1 - G0]:
    for k, v in r.get("heads", {}).items():
        heads.setdefault(k, []).append(v)
hs = {k: dict(w=[round(min(x["w"] for x in v)), round(max(x["w"] for x in v))], y=[round(min(x["y"] for x in v)), round(max(x["y"] for x in v))],
              bottom_max=round(max(x["bottom"] for x in v))) for k, v in heads.items()}
meta = {"take": CFG["take"], "film": 16, "shots": CFG["shots"], "g0": G0, "g1": G1, "first_g": FIRST, "n_frames": N,
        "shot_ranges": {str(CFG["shots"][0]): [G0, G1 - 1]}, "handle_in": H, "handle_out": H,
        "transition_in": {"type": "cut", "frames": 0}, "transition_out": {"type": "cut", "frames": 0, "at": G1},
        "set": CFG["set"], "cast": CFG["cast"], "camera": CFG["camera"], "events": CFG["events"], "dof": "none", "text": "none",
        "light": CFG["light"], "samples": rows[0].get("samples"), "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "heads": hs, "framediff_in_shot": {"median": nb["median"], "p90": nb["p90"]},
        "narration": "film16/audio/narration.wav at +0.10 s; captions film16/script/captions.json"}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
ev = [dict(time=round(g / 30.0, 3), frame=g, kind=k, label=l) for g, k, l in CFG["cues"]]
json.dump(dict(take=CFG["take"], fps=30, note="time = film seconds (g / 30); narration film16/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
contact(pngs, os.path.join(HERE, "contact.jpg"))
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(FIRST), "--cuts", "%d,%d" % (G0, G1)], capture_output=True, text=True)
print(r.stdout, r.stderr[-500:])
sz = os.path.getsize(mkv) / 1e6
if sz > 45:
    subprocess.run("split -b 40M take.mkv take.mkv.part && rm take.mkv", shell=True, cwd=HERE)
print("delivered %d frames, take.mkv %.1f MB; s/frame wall %.2f cpu %.2f; frame-diff median %.2f p90 %.2f" % (N, sz, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))

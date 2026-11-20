#!/usr/bin/env python3
"""deliver.py -- film-19 take delivery (team9: s23 / s24 / s25 / s26) from raw/g_%04d.png (+ .json): frames/, take.mkv (libx264rgb crf 6),
meta.json, cues.json, contact.jpg (16 frames, cyan line = caption band y 880), framediff.json (in-shot frame-diff, 90x160 grey), then
qa_auto.py (-> QA_AUTO.md + phone_sheet.jpg).  No bpy except that it imports this folder's shot.py for the ranges (shot.py imports c19 -> bpy).
    python3 deliver.py            final delivery
    python3 deliver.py draft      look at a draft: work/draft -> work/draft_contact.jpg + frame-diff numbers (nothing delivered)"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
import shot as S                                         # noqa: E402  (G0, G1, G_FIRST, G_LAST, CAM, events)

TAKE = os.path.basename(HERE)
G_FIRST, G_LAST, G0, G1 = S.G_FIRST, S.G_LAST, S.G0, S.G1
N = G_LAST - G_FIRST + 1
INS = (G0 - G_FIRST, G1 - G_FIRST)                      # indices of the in-shot frames in take.mkv: [a, b)
CUTS_OUT = [] if G_LAST + 1 >= 2160 else [G1]          # planned cut g list for qa_auto
CUTS_IN = [G0] if TAKE != "s23" else []                # hard cut in (s23 dissolves in: 15 f)


def framediff(pngs):
    prev, d = None, []
    for p in pngs:
        a = np.asarray(Image.open(p).convert("RGB").resize((90, 160), Image.BILINEAR), dtype=np.float32).mean(-1)
        if prev is not None:
            d.append(float(np.abs(a - prev).mean()))
        prev = a
    return d


def contact(pngs, out, cols=8, w=270):
    h, lab = w * 16 // 9, 18
    idx = [int(round(i * (len(pngs) - 1) / 15.0)) for i in range(16)]
    Im = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20))
    dr = ImageDraw.Draw(Im)
    for i, k in enumerate(idx):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        Im.paste(Image.open(pngs[k]).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
        g = G_FIRST + k
        dr.text((x + 4, y + 3), "g %d  %.2f s%s" % (g, g / 30.0, "  handle" if (g < G0 or g >= G1) else ""), fill=(255, 255, 255))
    Im.save(out, quality=88)


def numbers(d):
    ins = d[INS[0]:INS[1] - 1]                           # pairs (g-1, g) for g in G0+1 .. G1-1: in-shot only, handles excluded
    return dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), resized to 90x160 (bilinear), 0-255 levels; pairs g-1->g for g %d..%d (in-shot, no handle)" % (G0 + 1, G1 - 1),
                median=round(float(np.median(ins)), 2), p90=round(float(np.percentile(ins, 90)), 2), min=round(float(min(ins)), 2),
                max=round(float(max(ins)), 2), target=dict(median=4.0, p90=12.0), per_pair=[round(v, 2) for v in d])


if len(sys.argv) > 1 and sys.argv[1] == "draft":
    src = sorted(glob.glob(os.path.join(HERE, "work", "draft", "g_*.png")))
    assert len(src) == N, "draft has %d of %d frames" % (len(src), N)
    contact(src, os.path.join(HERE, "work", "draft_contact.jpg"))
    nb = numbers(framediff(src))
    json.dump(nb, open(os.path.join(HERE, "work", "draft_framediff.json"), "w"), indent=1)
    print("draft frame-diff median %.2f p90 %.2f (min %.2f max %.2f)" % (nb["median"], nb["p90"], nb["min"], nb["max"]))
    sys.exit(0)

RAW, OUT = os.path.join(HERE, "raw"), os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)
rows = []
for g in range(G_FIRST, G_LAST + 1):
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
pngs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(G_FIRST, G_LAST + 1)]
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
nb = numbers(framediff(pngs))
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)
heads = {}
for r in rows[INS[0]:INS[1]]:
    for k, v in r["heads"].items():
        heads.setdefault(k, []).append(v)
hs = {k: dict(w=[round(min(h["w"] for h in v)), round(max(h["w"] for h in v))], y=[round(min(h["y"] for h in v)), round(max(h["y"] for h in v))],
              x=[round(min(h["x"] for h in v)), round(max(h["x"] for h in v))], bottom_max=round(max(h["bottom"] for h in v))) for k, v in heads.items()}

cue_cfg = json.load(open(os.path.join(HERE, "cues_cfg.json"), encoding="utf-8"))
meta = {"take": TAKE, "film": 19, "shots": [int(TAKE[1:])], "g0": G0, "g1": G1, "first_g": G_FIRST, "n_frames": N,
        "shot_ranges": {TAKE[1:]: [G0, G1 - 1]}, "handle_in": G0 - G_FIRST, "handle_out": G_LAST + 1 - G1,
        "transition_in": cue_cfg["transition_in"], "transition_out": cue_cfg["transition_out"],
        "set": cue_cfg["set"], "cast": cue_cfg["cast"], "camera": cue_cfg["camera"], "events": cue_cfg["events"],
        "dof": "none", "text": "none", "caption_shade": "none", "light": S.LIGHT, "samples": rows[0].get("samples"),
        "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "heads_in_shot_px": hs,
        "framediff_in_shot": {"median": nb["median"], "p90": nb["p90"]},
        "narration": "film19/audio/narration.wav at +0.10 s; captions film19/script/captions.json"}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration film19/audio/narration.wav at +0.10 s", cues=cue_cfg["cues"]),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)

contact(pngs, os.path.join(HERE, "contact.jpg"))
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(G_FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
if os.path.getsize(mkv) > 45e6:
    subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True)
cuts = ",".join(map(str, CUTS_IN + CUTS_OUT))
cmd = [sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(G_FIRST)] + (["--cuts", cuts] if cuts else [])
r = subprocess.run(cmd, capture_output=True, text=True)
print(r.stdout, r.stderr[-500:])
print("delivered %d frames, take.mkv %.1f MB; s/frame %.2f wall %.2f cpu; frame-diff median %.2f p90 %.2f"
      % (N, os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))

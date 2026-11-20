#!/usr/bin/env python3
"""deliver.py -- s01 delivery from raw/g_%04d.png (+ .json): frames/g_%04d.png, take.mkv (libx264rgb crf 6), meta.json, cues.json,
contact.jpg (16 frames, cyan line = caption band y 880), framediff.json (in-shot frame-diff, 90x160 grey), then qa_auto.py
(-> QA_AUTO.md + phone_sheet.jpg).  No bpy.
    python3 deliver.py            final delivery
    python3 deliver.py draft      look at a draft: work/draft -> work/draft_contact.jpg + frame-diff numbers (nothing delivered)"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
TAKE = os.path.basename(HERE)                  # "s19" / "s21"
CFG = {"s19": dict(shot=19, G0=1468, G1=1581, H_IN=9, H_OUT=9, cuts=[1581], tin=("dissolve", 13), tout=("cut", 0),
                   ev=dict(lift=[1459, 1479], snap=[1496, 1509], word_caption=1497, cheer="g 1510..1589 hats and watch up, sailors bounce ~3 Hz"),
                   set="v3/set3d19/h19.py SHIP preset ship_coast, light DAY_JAMAICA; set_sea / set_roll keyed every frame with t = (g - first_g)/30"),
       "s21": dict(shot=21, G0=1665, G1=1756, H_IN=9, H_OUT=9, cuts=[], tin=("dissolve", 13), tout=("dissolve", 11),
                   ev=dict(snap=[1698, 1711], word_caption=1699, fumble="astro19_c wobbles the quadrant through the whole shot"),
                   set="v3/set3d19/h19.py SHIP preset ship_coast, light DAY_BARBADOS; set_sea / set_roll keyed every frame with t = (g - first_g)/30")}[TAKE]
G0, G1, H_IN, H_OUT = CFG["G0"], CFG["G1"], CFG["H_IN"], CFG["H_OUT"]
FIRST = G0 - H_IN
N = G1 + H_OUT - FIRST
CUTS_OUT = CFG["cuts"]
EV = CFG["ev"]


def framediff(pngs, skip=()):
    """mean |grey(i) - grey(i-1)| at 90x160 (grey = mean of R, G, B; 0-255 levels); pairs whose second frame is in skip are left out"""
    prev, d = None, []
    for i, p in enumerate(pngs):
        a = np.asarray(Image.open(p).convert("RGB").resize((90, 160), Image.BILINEAR), dtype=np.float32).mean(-1)
        if prev is not None and i not in skip:
            d.append(float(np.abs(a - prev).mean()))
        prev = a
    return d


def contact(pngs, out, cols=8, w=270):
    h, lab = w * 16 // 9, 18
    gs = [int(round(i * (len(pngs) - 1) / 15.0)) for i in range(16)]
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20))
    dr = ImageDraw.Draw(S)
    for i, g in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(pngs[g]).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
        gg = FIRST + g
        dr.text((x + 4, y + 3), "g %d  %.2f s%s" % (gg, gg / 30.0, "  handle" if (gg < G0 or gg >= G1) else ""), fill=(255, 255, 255))
    S.save(out, quality=88)


def numbers(d):
    ins = d[H_IN:H_IN + (G1 - G0) - 1]             # pairs (g-1, g) for g G0+1..G1-1: inside the shot only (handles are not screen time)
    return dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), resized to 90x160 (bilinear), 0-255 levels; pairs g-1->g for g G0+1..G1-1 (in-shot, no handles)",
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
for g in range(FIRST, FIRST + N):
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
pngs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(FIRST, FIRST + N)]
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
heads = [h for r in rows for h in r["heads"].values()]
nb = numbers(framediff(pngs))
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)

meta = {"take": TAKE, "film": 19, "shots": [CFG["shot"]], "g0": G0, "g1": G1, "first_g": FIRST, "n_frames": N,
        "shot_ranges": {str(CFG["shot"]): [G0, G1 - 1]}, "handle_in": H_IN, "handle_out": H_OUT,
        "transition_in": {"type": CFG["tin"][0], "frames": CFG["tin"][1]},
        "transition_out": {"type": CFG["tout"][0], "frames": CFG["tout"][1], "at": G1},
        "set": CFG["set"] + "; no runtime set changes; no caption_shade",
        "bigzoom": ([1468, 1578] if TAKE == "s19" else None), "events": EV, "dof": "none", "text": "none", "caption_shade": "none", "samples": rows[0].get("samples"),
        "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "head_px": [round(min(h["w"] for h in heads)), round(max(h["w"] for h in heads))],
        "head_centre_y": [round(min(h["y"] for h in heads)), round(max(h["y"] for h in heads))],
        "framediff_in_shot": {"median": nb["median"], "p90": nb["p90"]},
        "narration": "film19/audio/narration.wav at +0.10 s; captions film19/script/captions.json"}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)

ev = [dict(time=round(G0 / 30.0, 3), duration=round((G1 - G0) / 30.0, 3), frame=G0, end_frame=G1, kind="ambience",
           label="tropical beach: surf, palm fronds rustling, gulls, a far ship's bell" if TAKE == "s19" else "Barbados beach: surf, wind in the palms, gulls")]
if TAKE == "s19":
    ev += [dict(time=round(1497 / 30.0, 3), duration=0.4, frame=1497, end_frame=1509, kind="accent", label="snap push on 'แค่ห้าวินาที': airy whoosh + cheer swell", peak_frame=1503),
           dict(time=round(1468 / 30.0, 3), duration=1.0, frame=1468, end_frame=1498, kind="foley", label="sailors' cheers and a tricorne thrown up (no words)")]
else:
    ev += [dict(time=round(1699 / 30.0, 3), duration=0.4, frame=1699, end_frame=1711, kind="accent", label="snap push on 'นาฬิกาแม่น': whoosh", peak_frame=1705),
           dict(time=round(1665 / 30.0, 3), duration=3.0, frame=1665, end_frame=1755, kind="foley", label="brass quadrant clanks and wobbles in astro19_c's hands; a stumble on the sand")]
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration film19/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)

contact(pngs, os.path.join(HERE, "contact.jpg"))
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
if os.path.getsize(mkv) > 45e6:
    subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True)
cmd = [sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(FIRST)]
if CUTS_OUT:
    cmd += ["--cuts", ",".join(map(str, CUTS_OUT))]
r = subprocess.run(cmd, capture_output=True, text=True)
print(r.stdout, r.stderr[-500:])
print("delivered %d frames, take.mkv %.1f MB; s/frame %.2f wall %.2f cpu; frame-diff median %.2f p90 %.2f"
      % (N, os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))

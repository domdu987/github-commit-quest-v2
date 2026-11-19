#!/usr/bin/env python3
"""deliver.py -- take delivery from raw/g_%04d.png (+ .json): frames/, take.mkv (libx264rgb crf 6), meta.json, cues.json, contact.jpg, framediff.json, qa_auto.
    python3 deliver.py            final delivery
    python3 deliver.py draft      work/draft -> work/draft_contact.jpg + frame-diff numbers (nothing delivered)"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
from take_cfg import *          # TAKE, SHOTS, SHOT_RANGES, FIRST, LAST, G0, G1, TRANS_IN, CUTS_QA, EV, CUES, NOTES
N = LAST - FIRST + 1


def framediff(pngs, skip=()):
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
        dr.text((x + 4, y + 3), "g %d  %.2f s%s" % (gg, gg / 30.0, "" if G0 <= gg < G1 else "  handle"), fill=(255, 255, 255))
    S.save(out, quality=88)


def numbers(d):
    ins = [d[i - 1] for i in range(1, N) if G0 <= FIRST + i < G1]      # pairs (g-1,g) with g inside the shot span (in-shot, no handle)
    return dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), 90x160 bilinear, 0-255 levels; pairs g-1->g for g in the take's shots (no handle); pairs across an internal cut/dissolve included only if CUT_SKIP empty",
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
for i in range(N):
    g = FIRST + i
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
pngs = [os.path.join(OUT, "g_%04d.png" % (FIRST + i)) for i in range(N)]
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
nb = numbers(framediff(pngs))
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)
heads = {}
for r in rows:
    if G0 <= r["g"] < G1:
        for k, h in r["heads"].items():
            if -50 < h["x"] < 770 and h["y"] > -50:        # visible heads only
                heads.setdefault(k, []).append(h)
allh = [h for v in heads.values() for h in v]
meta = dict(take=TAKE, film=16, shots=SHOTS, g0=G0, g1=G1, first_g=FIRST, n_frames=N, shot_ranges=SHOT_RANGES,
            handle_in=G0 - FIRST, handle_out=LAST - G1 + 1, transition_in=TRANS_IN,
            transition_out=dict(type="cut", frames=0, at=G1), events=EV, dof="none", text="none", light=NOTES["light"],
            set=NOTES["set"], cast=NOTES["cast"], camera=NOTES["camera"], samples=rows[0].get("samples"), resolution=[720, 1280], threads=2, fps=30,
            s_per_frame_wall_mean=round(float(np.mean(walls)), 2), s_per_frame_cpu_mean=round(float(np.mean(cpus)), 2),
            head_px=[round(min(h["w"] for h in allh)), round(max(h["w"] for h in allh))],
            head_centre_y=[round(min(h["y"] for h in allh)), round(max(h["y"] for h in allh))],
            head_bottom_max_y=round(max(h["bottom"] for h in allh)),
            framediff_in_shot=dict(median=nb["median"], p90=nb["p90"]),
            narration="film16/audio/narration.wav at +0.10 s; captions film16/script/captions.json")
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
ev = []
for (a, b, kind, label) in CUES:
    ev.append(dict(time=round(a / 30.0, 3), duration=round(max(0, b - a) / 30.0, 3), frame=a, end_frame=b, kind=kind, label=label))
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration film16/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
contact(pngs, os.path.join(HERE, "contact.jpg"))
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(FIRST), "--cuts", ",".join(map(str, CUTS_QA))],
                   capture_output=True, text=True)
print(r.stdout, r.stderr[-500:])
if os.path.getsize(mkv) > 45e6:
    subprocess.run("split -b 40M take.mkv take.mkv.part && rm take.mkv", shell=True, cwd=HERE)
print("delivered %d frames, take.mkv %.1f MB; s/frame %.2f wall %.2f cpu; frame-diff median %.2f p90 %.2f"
      % (N, os.path.getsize(mkv) / 1e6 if os.path.exists(mkv) else 0, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))

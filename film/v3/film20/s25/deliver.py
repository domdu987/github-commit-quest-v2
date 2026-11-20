#!/usr/bin/env python3
"""deliver.py -- film-20 take delivery from raw/g_%04d.png (+ .json): frames/, take.mkv (libx264rgb crf 6; split if > 45 MB), meta.json,
cues.json, contact.jpg (16 frames, cyan line = caption band y 880), framediff.json (in-shot frame-diff, 90x160 grey), qa_auto.py.  No bpy.
    python3 deliver.py          final delivery
    python3 deliver.py draft    look at work/draft: contact + frame-diff numbers (nothing delivered)"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
# ---- per-take configuration (keep in step with shot.py) -------------------------------------------------------------------------
CFG = dict(
    take="s25", shot=25, g0=1853, g1=1912, h_in=4, h_out=4,
    tin=dict(type="cut", frames=0), tout=dict(type="cut", frames=0, at=1912, to_shot=26),
    cuts=[1853, 1912],                          # hard cut in (from shot 24) and out (to shot 26)
    events=dict(word_that_one_place=1879, snap_push=[1877, 1892], fork_bite_rel=[19], wine_sip_rel=[38, 78]),
    set="v3/set3d20 RESTO preset resto_table, light DAY, year 1889 (wine glass + bread basket FG from the set)",
    cast="v3/cast20 maupassant seated (maupassant_seated_eat / _eat_chew / _toast arms blended: fork bite, chew, sip of wine, fork bite; napkin; seat_h 0.865 D; mouth a still smile); stand-in card hidden",
    camera="custom 22 mm, resto_table pose 0.6 D closer, 0.55 D to the side; c20.CamPath push 8 %/s + slide -40 px/s + arc -2.5 deg/s + tilt 4 deg, decay 0.3 + SNAP PUSH x1.6 g 1877..1892 on 'ที่เดียว' (event 1879)",
    cue_note_cut_out="hard cut to shot 26 (RESTO resto_view, over his shoulder out of the window): same room tone",
)
MB_LIMIT = 45e6
G0, G1, H_IN, H_OUT = CFG["g0"], CFG["g1"], CFG["h_in"], CFG["h_out"]
G_FIRST = G0 - H_IN
N = G1 + H_OUT - G_FIRST                         # frames in take.mkv
IN0, IN1 = G0 - G_FIRST, G1 - G_FIRST            # in-shot indices [IN0, IN1)


def framediff(pngs):
    prev, d = None, []
    for i, p in enumerate(pngs):
        a = np.asarray(Image.open(p).convert("RGB").resize((90, 160), Image.BILINEAR), dtype=np.float32).mean(-1)
        d.append(None if prev is None else float(np.abs(a - prev).mean()))
        prev = a
    return d                                      # d[i] = diff(frame i-1 -> i)


def numbers(d):
    ins = [d[i] for i in range(IN0 + 1, IN1)]     # pairs inside the shot only (no handles)
    return dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), 90x160 bilinear, 0-255 levels; pairs g-1->g for g %d..%d (in-shot, no handle)" % (G0 + 1, G1 - 1),
                median=round(float(np.median(ins)), 2), p90=round(float(np.percentile(ins, 90)), 2), min=round(float(min(ins)), 2),
                max=round(float(max(ins)), 2), target=dict(median=4.0, p90=12.0), per_pair=[None if v is None else round(v, 2) for v in d])


def contact(pngs, out, cols=8, w=270):
    h, lab = w * 16 // 9, 18
    idx = [int(round(i * (len(pngs) - 1) / 15.0)) for i in range(16)]
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20))
    dr = ImageDraw.Draw(S)
    for i, k in enumerate(idx):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(pngs[k]).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
        g = G_FIRST + k
        dr.text((x + 4, y + 3), "g %d  %.2f s%s" % (g, g / 30.0, "  handle" if (g < G0 or g >= G1) else ""), fill=(255, 255, 255))
    S.save(out, quality=88)


if len(sys.argv) > 1 and sys.argv[1] == "draft":
    src = sorted(glob.glob(os.path.join(HERE, "work", "draft", "g_*.png")))
    assert len(src) == N, "draft has %d of %d frames" % (len(src), N)
    contact(src, os.path.join(HERE, "work", "draft_contact.jpg"))
    nb = numbers(framediff(src))
    print("draft frame-diff median %.2f p90 %.2f (min %.2f max %.2f)" % (nb["median"], nb["p90"], nb["min"], nb["max"]))
    sys.exit(0)

RAW, OUT = os.path.join(HERE, "raw"), os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)
rows = []
for g in range(G_FIRST, G_FIRST + N):
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
pngs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(G_FIRST, G_FIRST + N)]
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
d = framediff(pngs)
nb = numbers(d)
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)
hs = {}
for r in rows[IN0:IN1]:
    for k, h in r["heads"].items():
        hs.setdefault(k, []).append(h)
heads = {k: dict(head_px=[round(min(h["w"] for h in v)), round(max(h["w"] for h in v))], head_centre_y=[round(min(h["y"] for h in v)), round(max(h["y"] for h in v))],
                 head_bottom_max_y=round(max(h["bottom"] for h in v))) for k, v in hs.items()}
meta = {"take": CFG["take"], "film": 20, "shots": [CFG["shot"]], "g0": G0, "g1": G1, "first_g": G_FIRST, "n_frames": N,
        "shot_ranges": {str(CFG["shot"]): [G0, G1 - 1]}, "handle_in": H_IN, "handle_out": H_OUT,
        "transition_in": CFG["tin"], "transition_out": CFG["tout"],
        "set": CFG["set"], "cast": CFG["cast"], "camera": CFG["camera"], "events": CFG["events"], "dof": "none", "text": "none", "light": "DAY",
        "year": 1889, "samples": rows[0].get("samples"), "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "heads": heads, "framediff_in_shot": {"median": nb["median"], "p90": nb["p90"]},
        "narration": "film20/audio/narration.wav at +0.10 s; captions film20/script/captions.json"}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)

ev = []


def add(g0, g1, kind, note, **kw):
    e = dict(kind=kind, t=round(g0 / 30.0, 3), dur=round(max(0, g1 - g0) / 30.0, 3), frame=g0, end_frame=g1, note=note)
    e.update(kw)
    ev.append(e)


exec(open(os.path.join(HERE, "cues_def.py")).read())          # defines CUES(add, CFG, G0, G1, H_IN, H_OUT)
CUES(add, CFG, G0, G1, H_IN, H_OUT)
json.dump(dict(take=CFG["take"], fps=30, note="t = film seconds (g / 30); narration film20/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)

contact(pngs, os.path.join(HERE, "contact.jpg"))
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(G_FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
if os.path.getsize(mkv) > MB_LIMIT:
    subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True, cwd=HERE)
    print("take.mkv is %.1f MB: split into take.mkv.part* (keep take.mkv out of git)" % (os.path.getsize(mkv) / 1e6))
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(G_FIRST), "--cuts", ",".join(map(str, CFG["cuts"]))],
                   capture_output=True, text=True)
print(r.stdout, r.stderr[-500:])
print("delivered %d frames (g %d..%d), take.mkv %.1f MB; s/frame %.2f wall %.2f cpu; frame-diff median %.2f p90 %.2f"
      % (N, G_FIRST, G_FIRST + N - 1, os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))

#!/usr/bin/env python3
"""deliver.py -- s05 delivery from raw/g_%04d.png (+ .json): frames/g_%04d.png, take.mkv (libx264rgb crf 6), meta.json, cues.json,
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
GA, G0, G1, H_OUT = 253, 262, 356, 9                       # shot 1 = g 0..56 (0.00-1.91 s), hard cut out at g 57, handle g 57..65
N = G1 + H_OUT - GA
CUTS_OUT = [356]                                # planned cut g list for qa_auto (the cut to shot 2; the handle continues in 3D)
EV = {'whip': [262, 273], 'shake': [330, 339], 'word_caption': 330, 'bail_periods': [22, 26, 24]}


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
        dr.text((x + 4, y + 3), "g %d  %.2f s%s" % (g + GA, (g + GA) / 30.0, "  handle" if g >= G1 else ""), fill=(255, 255, 255))
    S.save(out, quality=88)


def numbers(d):
    ins = d[G0 - GA:G1 - 1 - GA]                            # pairs (g-1, g) for g 1..56: inside shot 1 only (the handle is not screen time)
    return dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), resized to 90x160 (bilinear), 0-255 levels; pairs g-1->g for g 192..261 (in-shot, no handle)",
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
for g in range(GA, GA + N):
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
pngs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(GA, GA + N)]
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
heads = [h for r in rows for k, h in r["heads"].items()]
nb = numbers(framediff(pngs))
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)

meta = {"take": "s05", "film": 19, "shots": [5], "g0": G0, "g1": G1, "first_g": GA, "n_frames": N,
        "shot_ranges": {"5": [G0, G1 - 1]}, "handle_in": G0 - GA, "handle_out": H_OUT,
        "transition_in": {"type": "cut", "frames": 0, "note": "hard cut from shot 4 at g 262; in-handle g 253..261 rendered in 3D (whip continues)"},
        "transition_out": {"type": "dissolve", "frames": 13, "at": G1, "note": "dissolve to shot 6 (HALL); out-handle g 356..364 rendered"},
        "set": "v3/set3d19 SHIP ship_rocks STORM_DUSK; set_sea(g/30), ship_root roll/pitch/bob = the set's own x2.2 (bob x1.2) + 2.3 deg slow roll keyed every frame, rain on; FG lantern re-hung on a swinging pivot; no caption_shade",
        "cast": "captain19 (captain_idle, hands behind back, stagger) + sailor19_a/b/c bailing (STORY19 *_bail with an animated scoop/fling cycle, splash jet, worried faces); all ride_ship; fixed expression mouths, no lip-sync",
        "camera": "custom 22 mm riding the deck (on_ship): whip pan-in g 262..273 (24 deg, eased), drift push 7 %/s + slide 30 px/s + arc -3 deg/s, ONE shake g 330..339 (decaying, 10 f) on 'เรือจมกัน'",
        "events": EV, "dof": "none", "text": "none", "caption_shade": "none", "light": "STORM_DUSK", "samples": rows[0].get("samples"),
        "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "head_px": [round(min(h["w"] for h in heads)), round(max(h["w"] for h in heads))],
        "head_centre_y": [round(min(h["y"] for h in heads)), round(max(h["y"] for h in heads))],
        "head_bottom_max_y": round(max(h["bottom"] for h in heads)),
        "framediff_in_shot": {"median": nb["median"], "p90": nb["p90"]},
        "narration": "film19/audio/narration.wav at +0.10 s; captions film19/script/captions.json"}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)

ev = []


def add(g0, g1, kind, label, **kw):
    e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=g0, end_frame=g1, kind=kind, label=label)
    e.update(kw)
    ev.append(e)


add(GA, GA + N, "ambience", "storm at dusk: wind, heavy rain, groaning timbers, surf thundering on black rocks")
add(262, 273, "accent", "whip arrival: fast whoosh into the shot", peak_frame=265)
add(262, 356, "foley", "buckets scooped and flung, water slaps, sailors' panicked grunts (no words)", peak_frame=300)
add(330, 339, "accent", "the ONE shake on 'เรือจมกัน': a timber crash with a low rumble", peak_frame=331)
add(G1, G1, "cut", "dissolve to shot 6 (the hall): storm fades under the room tone")
json.dump(dict(take="s05", fps=30, note="time = film seconds (g / 30); narration PROJ/film19/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)

contact(pngs, os.path.join(HERE, "contact.jpg"))
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(GA), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
if os.path.getsize(mkv) > 45e6:                    # WORKER rule: split big takes for git
    subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True)
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(GA), "--cuts", ",".join(map(str, CUTS_OUT))],
                   capture_output=True, text=True)
print(r.stdout)
print("delivered %d frames, take.mkv %.1f MB; s/frame %.2f wall %.2f cpu; frame-diff median %.2f p90 %.2f"
      % (N, os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))

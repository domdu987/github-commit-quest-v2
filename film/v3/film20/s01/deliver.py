#!/usr/bin/env python3
"""deliver.py -- s01 delivery from raw/g_%04d.png (+ .json): frames/g_%04d.png, take.mkv (libx264rgb crf 6; split if > 45 MB),
meta.json, cues.json, contact.jpg (16 frames, cyan line = caption band y 880), framediff.json (in-shot frame-diff, 90x160 grey),
then qa_auto.py (-> QA_AUTO.md + phone_sheet.jpg).  No bpy.
    python3 deliver.py            final delivery
    python3 deliver.py draft      look at a draft: work/draft -> work/draft_contact.jpg + frame-diff numbers (nothing delivered)"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
G0, G1, H_OUT = 0, 80, 4                       # shot 1 = g 0..79 (0.00-2.67 s), hard cut out at g 80, handle g 80..83
N = G1 + H_OUT                                 # 84 frames, first_g 0
CUTS_OUT = [G1]                                # planned cut g list for qa_auto (the cut to shot 2; the handle continues in 3D)
# event frames (keep in step with shot.py)
EV = dict(blink_1=[11, 13], word_hate=27, snap=[25, 40], face_swap_blink=[26, 28], swap_sneer_to_disgust=27, word_one=47,
          turn_away=[45, 53], expr_avoid=48, word_most=61, hmph=[61, 66])
MB_LIMIT = 45e6


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
        dr.text((x + 4, y + 3), "g %d  %.2f s%s" % (g, g / 30.0, "  handle" if g >= G1 else ""), fill=(255, 255, 255))
    S.save(out, quality=88)


def numbers(d):
    ins = d[:G1 - 1]                            # pairs (g-1, g) for g 1..79: inside shot 1 only (the handle is not screen time)
    return dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), resized to 90x160 (bilinear), 0-255 levels; pairs g-1->g for g 1..79 (in-shot, no handle)",
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
for g in range(N):
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
pngs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(N)]
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
heads = [r["heads"]["mau"] for r in rows[:G1] if "mau" in r["heads"]]
nb = numbers(framediff(pngs))
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)

meta = {"take": "s01", "film": 20, "shots": [1], "g0": G0, "g1": G1, "first_g": G0, "n_frames": N,
        "shot_ranges": {"1": [G0, G1 - 1]}, "handle_in": 0, "handle_out": H_OUT,
        "transition_in": {"type": "cut", "frames": 0, "note": "film opens on this frame (no handle before g 0)"},
        "transition_out": {"type": "cut", "frames": 0, "at": G1, "note": "hard cut to shot 2 (RESTO resto_table) at g 80; handle g 80..83 rendered in 3D (push, tilt and his idle continue)"},
        "set": "v3/set3d20 TOWER preset tower_low, light DAY, year 1889, set_crowd(1) (keyed every frame); runtime: the preset FG (fg_* lamp-post + bench, shade casters) moved by the camera's ground offset so they stay 1-2 D from the lens",
        "cast": "v3/cast20 maupassant (stage Actor, contact decal + proxy shadow), arms folded (maupassant_turn_away arms) the whole shot: sneer g 0..26, disgust20 (runtime expression) g 27..47 (swap on the closed frame of the blink 26..28), turn away yaw +0.30 -> -0.85 g 45..53 with expr avoid from g 48, hmph chin jerk g 61..66; blinks g 11, 26; no lip-sync",
        "camera": "custom 22 mm, preset tower_low lens shift 0.08 kept, camera lowered to 0.35 m and 1.6 D closer (5.0 D from his head); c20.CamPath push 8 %/s toward his head + slide 30 px/s + arc 3 deg/s + tilt up 4.5 deg/s from pitch -2.6, decay 0.3 (moving on frame 0 and the last frame) + snap x1.35 with +6 deg tilt and 0.25 D pan g 25..40 (15 f, peak 1.7) on 'เกลียดหอคอย'; pitch -2.6 -> 13.7 deg",
        "events": EV, "dof": "none", "text": "none", "light": "DAY", "year": 1889, "samples": rows[0].get("samples"), "resolution": [720, 1280],
        "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "head_px": [round(min(h["w"] for h in heads)), round(max(h["w"] for h in heads))],
        "head_centre_y": [round(min(h["y"] for h in heads)), round(max(h["y"] for h in heads))],
        "head_bottom_max_y": round(max(h["bottom"] for h in heads)),
        "framediff_in_shot": {"median": nb["median"], "p90": nb["p90"]},
        "narration": "film20/audio/narration.wav at +0.10 s; captions film20/script/captions.json"}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)

ev = []


def add(g0, g1, kind, note, **kw):
    """one sound cue: t = film seconds (g / 30), kind, note (+ frame numbers for the mixer)."""
    e = dict(kind=kind, t=round(g0 / 30.0, 3), dur=round(max(0, g1 - g0) / 30.0, 3), frame=g0, end_frame=g1, note=note)
    e.update(kw)
    ev.append(e)


add(0, N, "ambience", "Champ de Mars, sunny day 1889: open-air crowd murmur far off, a fairground band faint in the distance, light breeze, a few pigeons")
add(0, 25, "foley", "Maupassant's coat creaks as he stands arms folded; a disdainful nasal breath out", peak_frame=8)
add(25, 40, "accent", "snap push + tilt on 'เกลียดหอคอย': short airy whoosh rising", peak_frame=31)
add(27, 29, "accent", "face swap to disgust: a tiny low pizzicato 'plonk' (comic sour note)", peak_frame=27)
add(45, 53, "foley", "he turns his nose away: sharp cloth swish of the frock coat + shoe scuff on the gravel", peak_frame=49)
add(47, 50, "voice_fx", "non-verbal 'hmph!' huff (breath only, no words, mouth stays still)", peak_frame=48)
add(61, 66, "accent", "chin jerk on 'ที่สุดในโลก': a light snooty 'tsk' / woodblock tick", peak_frame=63)
add(G1, G1, "cut", "hard cut to shot 2 (RESTO resto_table): ambience changes to the restaurant room tone")
json.dump(dict(take="s01", fps=30, note="t = film seconds (g / 30); narration PROJ/film20/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)

contact(pngs, os.path.join(HERE, "contact.jpg"))
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(G0), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
if os.path.getsize(mkv) > MB_LIMIT:                    # WORKER20 §5: split -b 40M take.mkv take.mkv.part
    subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True, cwd=HERE)
    print("take.mkv is %.1f MB: split into take.mkv.part* (keep take.mkv out of git)" % (os.path.getsize(mkv) / 1e6))
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(G0), "--cuts", ",".join(map(str, CUTS_OUT))],
                   capture_output=True, text=True)
print(r.stdout)
print("delivered %d frames, take.mkv %.1f MB; s/frame %.2f wall %.2f cpu; frame-diff median %.2f p90 %.2f"
      % (N, os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))

#!/usr/bin/env python3
"""deliver.py -- s15 / s16 delivery from raw/g_%04d.png (+ .json): frames/g_%04d.png, take.mkv (libx264rgb crf 6), meta.json, cues.json,
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
SHOT = int(os.path.basename(HERE)[1:])                      # take folder s15 / s16
_c = dict(t0=36.52, t1=42.65, h_in=10, h_out=9, tin=("dissolve", 15), snap=(1166, 1182), word="อยู่ตรงหัว", g_word=1172,
          snap2=(1208, 1228), word2="บอกเวลาที่", g_word2=1218)
G0, G1 = int(round(_c["t0"] * 30)), int(round(_c["t1"] * 30))     # shot = g G0 .. G1-1
H_IN, H_OUT = _c["h_in"], _c["h_out"]
FIRST = G0 - H_IN
N = G1 + H_OUT - FIRST
CUTS_OUT = [G1]    # planned hard cuts (g) for qa_auto; 15 comes in on a dissolve
EV = dict(snap=list(_c["snap"]), snap_word=_c["word"], snap_word_g=_c["g_word"], snap2=list(_c["snap2"]), snap2_word=_c["word2"], snap2_word_g=_c["g_word2"], sun_overhead="set_sun_overhead keyed every frame" + (" 0 -> 1 (g %d..%d), then 1" % (G0 - 10, _c["g_word"] + 4)),
          deck="set_sea(t), set_roll(t) every frame; cards parented to ship_root; camera rides the deck (c19.on_ship)")


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
        dr.text((x + 4, y + 3), "g %d  %.2f s%s" % (g, g / 30.0, "  handle" if (g < G0 or g >= G1) else ""), fill=(255, 255, 255))
    S.save(out, quality=88)


def numbers(d):
    ins = d[H_IN:H_IN + (G1 - G0) - 1]          # pairs (g-1, g) for g G0+1..G1-1: inside the shot only (the handles are not screen time)
    return dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), resized to 90x160 (bilinear), 0-255 levels; pairs g-1->g for g G0+1..G1-1 (in-shot, no handle)",
                median=round(float(np.median(ins)), 2), p90=round(float(np.percentile(ins, 90)), 2), min=round(float(min(ins)), 2),
                max=round(float(max(ins)), 2), target=dict(median=4.0, p90=12.0), per_pair=[round(v, 2) for v in d])


if len(sys.argv) > 1 and sys.argv[1] == "draft":
    src = [os.path.join(HERE, "work", "draft", "g_%04d.png" % g) for g in range(FIRST, FIRST + N)]
    assert all(os.path.exists(p) for p in src), "draft incomplete"
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
nb = numbers(framediff(pngs))
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)
hd = {}
for r in rows:
    for k, v in r["heads"].items():
        hd.setdefault(k, []).append(v)
allh = [v for l in hd.values() for v in l]
ins_rows = [r for r in rows if G0 <= r["g"] < G1]
ins_h = [v for r in ins_rows for v in r["heads"].values()]
tin = {"type": _c["tin"][0], "frames": _c["tin"][1]}
meta = {"take": "s15", "film": 19, "shots": [15, 16], "g0": G0, "g1": G1, "first_g": FIRST, "n_frames": N,
        "shot_ranges": {"15": [G0, 1189], "16": [1190, G1 - 1]}, "handle_in": H_IN, "handle_out": H_OUT,
        "transition_in": tin, "transition_out": {"type": "cut", "frames": 0, "at": G1},
        "set": "v3/set3d19/h19.py SHIP preset ship_deck, light NOON; set_sea(t), set_roll(t), set_sun_overhead(k) keyed on every frame (same t); no runtime set changes; no caption_shade",
        "cast": "v3/cast19 william19 (quadrant / H4 pose) + captain19 (idle) at the deck marks william_deck / captain_wheel (+offset), cards parented to ship_root (c19.ride_ship)",
        "camera": "custom 22 mm on the deck (c19.CamPath in the ship's rest frame, c19.on_ship each frame so the camera rides the roll / bob); see shot.py",
        "events": EV, "dof": "none", "text": "none", "caption_shade": "none", "light": "NOON", "samples": rows[0].get("samples"),
        "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "head_px_in_shot": [round(min(h["w"] for h in ins_h)), round(max(h["w"] for h in ins_h))],
        "head_centre_y_in_shot": [round(min(h["y"] for h in ins_h)), round(max(h["y"] for h in ins_h))],
        "head_bottom_max_y_in_shot": round(max(h["bottom"] for h in ins_h)),
        "framediff_in_shot": {"median": nb["median"], "p90": nb["p90"]},
        "narration": "film19/audio/narration.wav at +0.10 s; captions film19/script/captions.json"}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)

ev = []


def add(g0, g1, kind, label, **kw):
    e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=g0, end_frame=g1, kind=kind, label=label)
    e.update(kw)
    ev.append(e)


add(G0, G1, "ambience", "open sea from the quarterdeck: wind in the sails, rigging creak, hull and swell, a far gull")
add(G0, G0 + 40, "foley", "William raises the brass quadrant to the sun: wood and brass creak, a soft ratchet", peak_frame=G0 + 12)
add(_c["snap"][0], _c["snap"][1], "accent", "snap tilt up on 'อยู่ตรงหัว': airy whoosh and a bright glint chime as the sun glare blooms", peak_frame=_c["g_word"])
add(1190, 1222, "foley", "the quadrant is lowered, the H4 comes out: cloth and a small tick", peak_frame=1204)
add(_c["snap2"][0], _c["snap2"][1], "accent", "crane down and push to the watch on 'บอกเวลา': whoosh, a bright H4 tick", peak_frame=_c["g_word2"])
add(G0, G1, "foley", "two sailors haul a rope in the background: a rhythmic heave-ho every 1.2 s, rope creak")
add(G1, G1, "cut", "cut out to shot 17 (ship_aerial, the ship sails on)")
json.dump(dict(take="s15", fps=30, note="time = film seconds (g / 30); narration PROJ/film19/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)

contact(pngs, os.path.join(HERE, "contact.jpg"))
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
if os.path.getsize(mkv) > 45e6:
    subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True)
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(FIRST), "--cuts", ",".join(map(str, CUTS_OUT))],
                   capture_output=True, text=True)
print(r.stdout)
print("delivered %d frames, take.mkv %.1f MB; s/frame %.2f wall %.2f cpu; frame-diff median %.2f p90 %.2f"
      % (N, os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))

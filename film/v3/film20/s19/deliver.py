#!/usr/bin/env python3
"""deliver.py -- delivery of one film-20 take from raw/g_%04d.png (+ .json): frames/, take.mkv (libx264rgb crf 6; split if > 45 MB),
meta.json, cues.json, contact.jpg (16 frames, cyan line = caption band y 880), framediff.json (in-shot, 90x160 grey), then qa_auto.py
(-> QA_AUTO.md + phone_sheet.jpg).  No bpy.  `python3 deliver.py draft` reviews work/draft (nothing delivered).
Per-take numbers are the CFG block below (take s19 = shot 19)."""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
CFG = {'take': 's19', 'shot': 19, 'g0': 1302, 'g1': 1382, 'first_g': 1298, 'last_g': 1385, 'handle_in': 4, 'handle_out': 4, 'transition_in': {'type': 'cut', 'frames': 0, 'note': 'hard cut from shot 18; 4 handle frames g 1298..1301'}, 'transition_out': {'type': 'cut', 'frames': 0, 'at': 1382, 'note': 'hard cut to shot 20 at g 1382; handle g 1382..1385'}, 'set': 'v3/set3d20 TOWER tower_dusk_summit, DUSK 1909; camera at (-4.4,-218,0.5) m on the avenue; runtime: antenna last-segment fix, wire_glow 0.7 so the wires read against the dusk sky, preset FG moved with the camera', 'cast': 'cast20 eiffel_old (eiffel_old_point_up) at mark eiffel_old, pointing up; no mouth', 'camera': "own camera function (shot.cam_at): drift push + slide, aim pitch 16 -> 18.5 deg on the summit, then WHIP-TILT (aim lerp summit -> wire foot, 9 f, peak 1.9x) at g 1343 on 'จากยอดหอ', then push on the hut", 'events': {'whip': [1343, 1352], 'word_wire': 1343}}
N = CFG["last_g"] - CFG["first_g"] + 1
G0, G1, FIRST = CFG["g0"], CFG["g1"], CFG["first_g"]
MB_LIMIT = 45e6

CUES = [(1298, 1386, 'ambience', 'Dusk on the avenue: wind in the lattice, the antenna wires hum high above, distant city'), (1343, 1352, 'accent', 'WHIP-TILT down the wire: fast rising-then-falling whoosh with a thin wire zing'), (1346, 1352, 'accent', 'wire hum swells as the camera lands on the post and hut'), (1302, 1302, 'cut', 'hard cut from shot 18'), (1382, 1382, 'cut', 'hard cut to the hut interior: the hum becomes the spark crackle')]


def framediff(pngs):
    prev, d = None, []
    for p in pngs:
        a = np.asarray(Image.open(p).convert("RGB").resize((90, 160), Image.BILINEAR), dtype=np.float32).mean(-1)
        if prev is not None:
            d.append(float(np.abs(a - prev).mean()))
        prev = a
    return d                                    # d[i] = diff between frame i and i+1 (index relative to first_g)


def numbers(d):
    a, b = G0 - FIRST, G1 - FIRST               # pairs (g-1 -> g) for g in G0+1 .. G1-1 : d index g-1-FIRST
    ins = d[a:b - 1]
    return dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), 90x160 bilinear, 0-255; in-shot pairs g0+1..g1-1 (no handles)",
                median=round(float(np.median(ins)), 2), p90=round(float(np.percentile(ins, 90)), 2), min=round(float(min(ins)), 2),
                max=round(float(max(ins)), 2), target=dict(median=4.0, p90=12.0), per_pair=[round(v, 2) for v in d])


def contact(pngs, out, cols=8, w=270):
    h, lab = w * 16 // 9, 18
    idx = [int(round(i * (len(pngs) - 1) / 15.0)) for i in range(16)]
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20))
    dr = ImageDraw.Draw(S)
    for i, k in enumerate(idx):
        g = FIRST + k
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(pngs[k]).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
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
for g in range(FIRST, CFG["last_g"] + 1):
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
pngs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(FIRST, CFG["last_g"] + 1)]
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
nb = numbers(framediff(pngs))
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)
inshot = [r for r in rows if G0 <= r["g"] < G1]
hs = [h for r in inshot for h in r["heads"].values()]
meta = {"take": CFG["take"], "film": 20, "shots": [CFG["shot"]], "g0": G0, "g1": G1, "first_g": FIRST, "n_frames": N,
        "shot_ranges": {str(CFG["shot"]): [G0, G1 - 1]}, "handle_in": CFG["handle_in"], "handle_out": CFG["handle_out"],
        "transition_in": CFG["transition_in"], "transition_out": CFG["transition_out"],
        "set": CFG["set"], "cast": CFG["cast"], "camera": CFG["camera"], "events": CFG["events"],
        "dof": "none", "text": "none", "samples": rows[0].get("samples"), "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "head_px": [round(min(h["w"] for h in hs)), round(max(h["w"] for h in hs))] if hs else None,
        "head_centre_y": [round(min(h["y"] for h in hs)), round(max(h["y"] for h in hs))] if hs else None,
        "head_bottom_max_y": round(max(h["bottom"] for h in hs)) if hs else None,
        "framediff_in_shot": {"median": nb["median"], "p90": nb["p90"]},
        "narration": "film20/audio/narration.wav at +0.10 s; captions film20/script/captions.json"}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
ev = [dict(kind=k, t=round(a / 30.0, 3), dur=round(max(0, b - a) / 30.0, 3), frame=a, end_frame=b, note=n) for a, b, k, n in CUES]
json.dump(dict(take=CFG["take"], fps=30, note="t = film seconds (g / 30); narration film20/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
contact(pngs, os.path.join(HERE, "contact.jpg"))
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
if os.path.getsize(mkv) > MB_LIMIT:
    subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True, cwd=HERE)
    print("take.mkv is %.1f MB: split into take.mkv.part* (keep take.mkv out of git)" % (os.path.getsize(mkv) / 1e6))
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(FIRST), "--cuts", ",".join(map(str, [G0, G1]))],
                   capture_output=True, text=True)
print(r.stdout, r.stderr[-500:])
print("delivered %d frames, take.mkv %.1f MB; s/frame %.2f wall %.2f cpu; frame-diff median %.2f p90 %.2f"
      % (N, os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))

#!/usr/bin/env python3
"""deliver.py -- take delivery from raw/g_%04d.png (+ .json): frames/, take.mkv (libx264rgb crf 6; split if > 45 MB), meta.json, cues.json,
contact.jpg, framediff.json, then qa_auto.py (-> QA_AUTO.md + phone_sheet.jpg).  No bpy.   python3 deliver.py"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
TAKE, SHOT = "s06", 678
G0, G1, H_IN, H_OUT = 404, 604, 8, 4
GA = G0 - H_IN
N = (G1 + H_OUT) - GA
TRANS_IN = {"type": "dissolve", "frames": 13}
CUTS_OUT = []
EV = {'snap': [430, 446], 'word_count': 444, 'word_sign': 469, 'land_1': 471, 'handover': [483, 494], 'word_paper': 491, 'land_2': 496, 'smoke_ramp': [513, 572], 'word_chimney': 572, 'end_pose_g603': True}
CAMERA = "ONE continuous travel take (WORKER20 §8): waypoint camera (Catmull-Rom on loc + look, no stop): slide past the waving artists g 396-440, push-in snap g 430-446 on 'สี่สิบกว่าคน' (444), descend and push DOWN onto the protest sheet g 446-490 (the cafe_table_insert pose at g 490), over the sheet g 490-512, rise + swing to the window g 512-572 (smoke 1.0 at 572), sweep down-right to the banquette g 572-603; last frame g603 = (3.533, 6.506, 0.983) D looking at (1.692, 13.16, 2.944) D = team7's T09 start pose, handle g604 (3.505, 6.531, 0.994), arriving with ~0.03 D/frame velocity; 22 mm, no shift, no DOF"
CAST = "v3/cast20 painter20 / composer20 / poet20 / architect20 (outraged: wave greeked newspapers g 396-500, then jab pointing fingers at the window g 500-603, 3 Hz bounce) + waiter (idle sway, off to the right) + Maupassant SEATED on the banquette mark the whole take (maupassant_seated_toast_smug, mouth held 'smile', sips, idle breathing only after g 585); runtime meshes: quill + two sleeved hands (A cream / B plum) hand the quill over the sheet g 452-520, FONT heading 'PROTESTATION' on the sheet; signatures 14 -> 15 (g 471) -> 16 (g 496); forge smoke ramps 0 -> 1 over g 513-572"
SET = 'v3/set3d20 CAFE cafe_wide DAY, window view stub, smoke ramp keyed per frame, add_signature keyed per frame; saturation grade 1.45'
CUES = [(396, 607, 'ambience', 'Café 1887, day: angry crowd hubbub, gas-lamp hiss, chairs, cups; sun shafts through the windows; far site hammering'), (404, 440, 'foley', 'artists shake newspapers: paper rattle + cloth, indignant (wordless) murmur', {'peak_frame': 418}), (430, 446, 'accent', "push-in snap on 'สี่สิบกว่าคน': rising whoosh + fist bang on the marble table", {'peak_frame': 444}), (452, 481, 'foley', 'quill scratching as the first signature is written; sleeve rustle', {'peak_frame': 468}), (471, 473, 'accent', 'first signature lands: pen tick + ink thud', {'peak_frame': 471}), (483, 494, 'foley', 'quill handed over: cloth swish, fingers on the shaft', {'peak_frame': 488}), (496, 498, 'accent', 'second signature lands: pen tick + ink thud', {'peak_frame': 496}), (512, 534, 'accent', 'camera rises off the sheet and swings to the window: whoosh', {'peak_frame': 522}), (513, 572, 'accent', 'forge smoke builds in the window: low rumbling swell', {'peak_frame': 572}), (572, 590, 'accent', "'เหมือนปล่อง' black chimney of smoke: ominous brass sting", {'peak_frame': 576}), (590, 604, 'accent', 'sweep to the banquette: soft whoosh settling; room tone narrows', {'peak_frame': 598}), (604, 607, 'cut', 'handle: match into T09 (Maupassant at the banquette) at g 604')]
END_CAM = {"g": 603, "loc_D": [3.533, 6.506, 0.983], "look_at_D": [1.692, 13.16, 2.944], "lens_mm": 22.0, "shift": [0.0, 0.0], "handle_g604": {"loc_D": [3.505, 6.531, 0.994], "look_at_D": [1.692, 13.16, 2.942]}}
SOUND_NOTE = "t = film seconds (g / 30); narration PROJ/film20/audio/narration.wav at +0.10 s"
MB_LIMIT = 45e6
IN_SHOT = (G0 + 1, G1 - 1)                      # pairs (g-1 -> g) for g in this range


def framediff(pngs):
    prev, d = None, []
    for p in pngs:
        a = np.asarray(Image.open(p).convert("RGB").resize((90, 160), Image.BILINEAR), dtype=np.float32).mean(-1)
        if prev is not None:
            d.append(float(np.abs(a - prev).mean()))
        prev = a
    return d                                    # d[i] = pair (GA+i -> GA+i+1)


def contact(pngs, out, cols=8, w=270):
    h, lab = w * 16 // 9, 18
    gs = [int(round(i * (len(pngs) - 1) / 15.0)) for i in range(16)]
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20))
    dr = ImageDraw.Draw(S)
    for i, g in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(pngs[g]).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
        gg = GA + g
        dr.text((x + 4, y + 3), "g %d  %.2f s%s" % (gg, gg / 30.0, "  handle" if (gg < G0 or gg >= G1) else ""), fill=(255, 255, 255))
    S.save(out, quality=88)


RAW, OUT = os.path.join(HERE, "raw"), os.path.join(HERE, "frames")
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
rows = []
for i in range(N):
    g = GA + i
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
pngs = [os.path.join(OUT, "g_%04d.png" % (GA + i)) for i in range(N)]
d = framediff(pngs)
ins = [d[g - 1 - GA] for g in range(IN_SHOT[0], IN_SHOT[1] + 1)]
nb = dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), 90x160 bilinear, 0-255 levels; pairs g-1->g for g %d..%d (in shot, no handles)" % IN_SHOT,
          median=round(float(np.median(ins)), 2), p90=round(float(np.percentile(ins, 90)), 2), min=round(float(min(ins)), 2), max=round(float(max(ins)), 2),
          target=dict(median=4.0, p90=12.0), per_pair=[round(v, 2) for v in d])
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
hd = {}
for r in rows[H_IN:H_IN + (G1 - G0)]:
    for k, v in r.get("heads", {}).items():
        hd.setdefault(k, []).append(v)
heads = {k: dict(w=[round(min(x["w"] for x in v)), round(max(x["w"] for x in v))], y=[round(min(x["y"] for x in v)), round(max(x["y"] for x in v))],
                 bottom_max=round(max(x["bottom"] for x in v))) for k, v in hd.items()}
meta = {"take": TAKE, "film": 20, "shots": [6, 7, 8], "g0": G0, "g1": G1, "first_g": GA, "n_frames": N, "shot_ranges": {"6": [404, 465], "7": [466, 512], "8": [513, 603]},
        "handle_in": H_IN, "handle_out": H_OUT, "transition_in": TRANS_IN,
        "transition_out": {"type": "match", "frames": 0, "at": G1, "note": "match cut into T09 (team7) at g %d; out-handle g %d..%d continues the move" % (G1, G1, G1 + H_OUT - 1)},
        "set": SET, "cast": CAST, "camera": CAMERA, "end_cam": END_CAM, "events": EV, "dof": "none", "text": "none", "light": "DAY", "year": 1887,
        "samples": rows[0].get("samples"), "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "heads_px_in_shot": heads, "framediff_in_shot": {"median": nb["median"], "p90": nb["p90"]},
        "narration": "film20/audio/narration.wav at +0.10 s; captions film20/script/captions.json"}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
ev = []
for c in CUES:
    g0, g1, kind, note = c[:4]
    e = dict(kind=kind, t=round(g0 / 30.0, 3), dur=round(max(0, g1 - g0) / 30.0, 3), frame=g0, end_frame=g1, note=note)
    if len(c) > 4:
        e.update(c[4])
    ev.append(e)
json.dump(dict(take=TAKE, fps=30, note=SOUND_NOTE, cues=ev), open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
contact(pngs, os.path.join(HERE, "contact.jpg"))
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(GA), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
if os.path.getsize(mkv) > MB_LIMIT:
    subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True, cwd=HERE)
    print("take.mkv is %.1f MB: split into take.mkv.part*" % (os.path.getsize(mkv) / 1e6))
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(GA), "--cuts", ",".join(map(str, CUTS_OUT)) or "0"], capture_output=True, text=True, cwd=HERE)
print(r.stdout, r.stderr[-500:])
print("delivered %d frames, take.mkv %.1f MB; s/frame %.2f wall %.2f cpu; frame-diff median %.2f p90 %.2f"
      % (N, os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))

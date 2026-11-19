#!/usr/bin/env python3
"""deliver.py -- take delivery from raw/g_%04d.png (+ .json): frames/g_%04d.png, take.mkv (libx264rgb crf 6), meta.json, cues.json,
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
TAKE = os.path.basename(HERE)
# ---- take config (edited per take)
SHOTS = [9]
G0, G1 = 542, 597
H_IN, H_OUT = 9, 9
FIRST_G = G0 - H_IN
N = (G1 + H_OUT) - FIRST_G
TRANS_IN = {'type': 'cut', 'frames': 0, 'note': 'hard cut in; 9 handle frames rendered in 3D before the first frame'}
TRANS_OUT = {'type': 'cut', 'frames': 0, 'at': 597, 'note': 'hard cut to shot 10 at g 597; handle g 597..605 in 3D'}
CUTS = []
SET = 'v3/set3d16 CHAMBER (chamber_low preset build, custom low camera 1.25 D above the floor), DAY; the mocker steps out in front of his desk; runtime FG desk corner with inkwell+quill'
CAST = 'mocker: belly laugh lead-in g 533..552 then mocker_mock_point LIP-SYNC (talk_mouth) from g 553 (quote 18.32 s +0.10), tears + blush, bounce ~0.06 D at 3 Hz'
CAMERA = "custom 22 mm low angle (pitch up ~14 deg), push 9 %/s + slide -45 px/s + arc -9 deg/s, snap x1.8 (+0.4 D truck) over g 552..565 on the quote's first word"
EV = {'quote_start': 553, 'pose_swap_blink': [551, 553], 'snap': [552, 565]}
CUES = [(533, 605, 'ambience', 'chamber: congressmen laughing and thumping desks, room tone'), (533, 552, 'accent', "the mocker's big belly laugh (voice-free: the narrator speaks, add a chuckle bed)"), (553, 596, 'foley', "fabric and boots as he rises and points; desk thump on 'ลวดเนี่ยนะ'"), (597, 597, 'cut', 'hard cut to shot 10')]
LABEL = "chamber_wide_high"


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
        gg = g + FIRST_G
        dr.text((x + 4, y + 3), "g %d  %.2f s%s" % (gg, gg / 30.0, "" if G0 <= gg < G1 else "  handle"), fill=(255, 255, 255))
    S.save(out, quality=88)


def numbers(d):
    """d[i] = diff between frame i and i+1 (index relative to FIRST_G); in-shot pairs g-1 -> g for g in G0+1 .. G1-1"""
    ins = [d[g - 1 - FIRST_G] for g in range(G0 + 1, G1)]
    return dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), resized to 90x160 (bilinear), 0-255 levels; pairs g-1->g for g %d..%d (in-shot, no handles)" % (G0 + 1, G1 - 1),
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
for g in range(FIRST_G, FIRST_G + N):
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
pngs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(FIRST_G, FIRST_G + N)]
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
nb = numbers(framediff(pngs))
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)
hd = {}
for r in rows:
    for k, h in r["heads"].items():
        hd.setdefault(k, []).append(h)
main = {k: v for k, v in hd.items() if k in ("mor", "mock")}
allw = [h["w"] for v in main.values() for h in v]
ally = [h["y"] for v in main.values() for h in v]
allb = [h["bottom"] for v in hd.values() for h in v]
meta = {"take": TAKE, "film": 16, "shots": SHOTS, "g0": G0, "g1": G1, "first_g": FIRST_G, "n_frames": N,
        "shot_ranges": {str(SHOTS[0]): [G0, G1 - 1]}, "handle_in": H_IN, "handle_out": H_OUT,
        "transition_in": TRANS_IN, "transition_out": TRANS_OUT,
        "set": SET, "cast": CAST, "camera": CAMERA, "events": EV, "dof": "none", "text": "none", "light": "DAY",
        "samples": rows[0].get("samples"), "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "main_head_px": [round(min(allw)), round(max(allw))], "main_head_centre_y": [round(min(ally)), round(max(ally))],
        "head_bottom_max_y": round(max(allb)),
        "framediff_in_shot": {"median": nb["median"], "p90": nb["p90"]},
        "narration": "film16/audio/narration.wav at +0.10 s; captions film16/script/captions.json"}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)

ev = []
for (a, b, kind, label) in CUES:
    ev.append(dict(time=round(a / 30.0, 3), duration=round(max(0, b - a) / 30.0, 3), frame=a, end_frame=b, kind=kind, label=label))
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration PROJ/film16/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)

contact(pngs, os.path.join(HERE, "contact.jpg"))
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST_G), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
size = os.path.getsize(mkv)
if size > 45e6:
    subprocess.run("split -b 40M take.mkv take.mkv.part", shell=True, cwd=HERE, check=True)
    print("take.mkv is %.1f MB: split into take.mkv.part*" % (size / 1e6))
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(FIRST_G), "--cuts", ",".join(map(str, CUTS))],
                   capture_output=True, text=True)
print(r.stdout)
print("delivered %d frames (g %d..%d), take.mkv %.1f MB; s/frame %.2f wall %.2f cpu; frame-diff median %.2f p90 %.2f"
      % (N, FIRST_G, FIRST_G + N - 1, size / 1e6, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))

#!/usr/bin/env python3
"""deliver.py -- from raw/s<id>/g_%04d.png build frames/g_%04d.png, meta.json, cues.json, contact.jpg, the 6 fps review strips
(work/strip_*.jpg, work/cuts.jpg), work/qa.txt (head / feet numbers) and take.mkv (libx264rgb crf 6; split when > 45 MB).
    python3 deliver.py [--no-encode]"""
import os, sys, json, shutil, subprocess, glob
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
CFG = {'take': 's09', 'first_g': 913, 'last_g': 1007, 'g0': 919, 'g1': 1002, 'plan_shots': ['9a', '9'], 'cuts': [954], 'shots': {'9': [913, 953], '19': [954, 1007]}, 'setups': {'9': {'preset': 'macro_oar', 'camera': "preset macro_oar 40 mm f/2.8 at water level, focus empty (world-fixed) at the preset look_at, one slow lateral slide 1.1 D; special 'solo'; set_oar_splash repeating every 24 frames (first dip g 922), 12 samples", 'state': 'special solo, set_oar_splash keyed every frame'}, '19': {'preset': 'hansan_high', 'camera': 'preset hansan_high camera, pushed 8 % along its view line; DOF off', 'state': "Korean ships flee ahead (set_korean_turn 0), set_fleet_chase s=(g-954)/30 keyed every frame, set_special ''"}}, 'events': {'hard_cut': 954, 'splash_dips': [922, 946]}, 'cast': 'no people', 'mouths': 'no characters', 'dof': 'shot 9a: preset f/2.8 on the oar blade; shot 9: off', 'cues': [[922, 937, 'foley', 'oar splash: blade digs into the sea, spray and foam'], [946, 961, 'foley', 'oar splash: blade digs into the sea, spray and foam'], [913, 953, 'ambience', 'water slapping, oar creak, ship hull close'], [954, 954, 'cut', 'HARD CUT to the high wide: sea wind, distant oars and sails'], [954, 1007, 'ambience', 'oars and sails far below, wind'], [1002, 1002, 'cut', 'hard cut to shot 10 (flag_bow)']]}
TAKE, FIRST, LAST = CFG["take"], CFG["first_g"], CFG["last_g"]
SHOTS = {int(k): v for k, v in CFG["shots"].items()}          # id -> [g_a, g_b] (frames drawn from raw/s<id>)
N = LAST - FIRST + 1
OUT = os.path.join(HERE, "frames_A"); os.makedirs(OUT, exist_ok=True)
WORK = os.path.join(HERE, "work"); os.makedirs(WORK, exist_ok=True)
sid_of = lambda g: [s for s, (a, b) in SHOTS.items() if a <= g <= b][0]
rows = []
for g in range(FIRST, LAST + 1):
    raw = os.path.join(HERE, "raw", "s%d" % sid_of(g))
    shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
mean = lambda v: round(float(np.mean(v)), 1)
by = {s: [r for r in rows if r["shot"] == s] for s in SHOTS}
meta = dict(take=TAKE, film=24, shots=CFG["plan_shots"], g0=CFG["g0"], g1=CFG["g1"], first_g=FIRST, n_frames=N,
            handle_in=CFG["g0"] - FIRST, handle_out=LAST - CFG["g1"],
            transition_in=dict(type="cut", frames=0), transition_out=dict(type="cut", frames=0),
            in_take_cuts=CFG.get("cuts", []), shot_ranges={str(s): v for s, v in SHOTS.items()}, setups=CFG["setups"],
            events=CFG["events"], set="v3/set3d24/joseon.py sea; runtime dressing from common.py / shot.py only", cast=CFG["cast"], mouths=CFG["mouths"],
            dof="off (Look A)", render="LOOK A (JOSEON_LOOK=A): no haze, no DOF, full 720x1280, no post(); the v1.1 grade runs in conform",
            samples=sorted({r["samples"] for r in rows}), resolution=[720, 1280], render_resolution=[720, 1280], threads=2, fps=30,
            s_per_frame_wall_mean=mean([r["wall"] for r in rows]), s_per_frame_cpu_mean=mean([r["cpu"] for r in rows]),
            s_per_frame_by_shot={str(s): dict(wall=mean([r["wall"] for r in v]), cpu=mean([r["cpu"] for r in v])) for s, v in by.items()},
            narration="film24/audio/narration.wav at +0.10 s; captions film24/script/captions.json")
json.dump(meta, open(os.path.join(HERE, "meta_A.json"), "w"), indent=1)
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration film24/audio/narration.wav at +0.10 s", cues=[
    dict(time=round(c[0] / 30.0, 3), duration=round(max(0, c[1] - c[0]) / 30.0, 3), frame=c[0], end_frame=c[1], kind=c[2], label=c[3]) for c in CFG["cues"]]),
    open(os.devnull, "w"), indent=1)


def sheet(gs, path, w=270, cols=8, lab=18):
    h = w * 16 // 9; nrow = (len(gs) + cols - 1) // cols
    S = Image.new("RGB", (cols * w, nrow * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
    for i, g in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
        dr.text((x + 4, y + 3), "g %d  %.2f s%s" % (g, g / 30.0, " handle" if g < CFG["g0"] or g > CFG["g1"] else ""), fill=(255, 255, 255))
    S.save(path, quality=88)


sheet([FIRST + int(round(i * (N - 1) / 15.0)) for i in range(16)], os.path.join(HERE, "contact_A.jpg"))
step = 5
sheet(list(range(FIRST, LAST + 1, step)), os.path.join(WORK, "strip_all_A.jpg"), w=200, cols=10)
for c in CFG.get("cuts", []):
    sheet(list(range(c - 3, c + 4)), os.path.join(WORK, "cut_A_%d.jpg" % c), w=240, cols=7)
with open(os.path.join(WORK, "qa_A.txt"), "w") as fo:
    names = sorted({n for r in rows for n in r.get("heads", {})})
    for n in names:
        hs = [r["heads"][n] for r in rows if n in r["heads"]]
        fo.write("%-3s head w %.0f..%.0f px, centre y %.0f..%.0f, bottom max %.0f (caption band 880)\n" % (
            n, min(h["w"] for h in hs), max(h["w"] for h in hs), min(h["y"] for h in hs), max(h["y"] for h in hs), max(h["bottom"] for h in hs)))
    for n in sorted({n for r in rows for n in r.get("feet", {})}):
        fs = np.array([r["feet"][n] for r in rows if n in r["feet"]]); d = np.hypot(*np.diff(fs, axis=0).T)
        fo.write("%-3s feet screen path: start %s end %s, per-frame step max %.2f px median %.2f\n" % (n, fs[0].tolist(), fs[-1].tolist(), d.max(), np.median(d)))
    fo.write("render wall %.1f s / cpu %.1f s per frame; retried %s\n" % (meta["s_per_frame_wall_mean"], meta["s_per_frame_cpu_mean"], [r["g"] for r in rows if r.get("retried")]))
if "--no-encode" not in sys.argv:
    mkv = os.path.join(HERE, "take_A.mkv")
    for p in glob.glob(mkv + "*"):
        os.remove(p)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                    "-c:v", "libx264rgb", "-crf", "12", "-preset", "slow", mkv], check=True)
    mb = os.path.getsize(mkv) / 1e6
    print("take.mkv %.1f MB" % mb)
    if mb > 45:
        subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True, cwd=HERE)
        os.remove(mkv)
        print("split into", sorted(glob.glob(mkv + ".part*")))
print(json.dumps({k: meta[k] for k in ("n_frames", "s_per_frame_wall_mean", "s_per_frame_cpu_mean", "s_per_frame_by_shot")}))

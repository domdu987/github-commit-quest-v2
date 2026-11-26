#!/usr/bin/env python3
"""deliver.py -- from raw/s1 (shot 1, roof_low, g 0..77) + raw/s2 (shot 2, macro_dragon, g 78..156) build frames/g_%04d.png,
meta.json, cues.json, contact.jpg, take.mkv (libx264rgb crf 6, g 0..156; split into take.mkv.part* when > 45 MB), the 6 fps
review strips work/strip_s1.jpg / strip_s2.jpg / work/cut.jpg (g 75..81) and work/qa.txt (head + feet numbers).
    python3 deliver.py [--no-encode]"""
import os, sys, json, shutil, subprocess, glob
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
G_CUT, G_END, H_OUT, G_HIT0, BEAT, G_SMOKE, G_PUFF = 78, 151, 6, 1, 12, 85, 115
N = G_END + H_OUT
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
WORK = os.path.join(HERE, "work"); os.makedirs(WORK, exist_ok=True)

rows = []
for g in range(N):
    sid = 1 if g < G_CUT else 2
    raw = os.path.join(HERE, "raw", "s%d" % sid)
    shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
mean = lambda v: round(float(np.mean(v)), 1)
w = {s: [r["wall"] for r in rows if r["shot"] == s] for s in (1, 2)}
c = {s: [r["cpu"] for r in rows if r["shot"] == s] for s in (1, 2)}
hits = list(range(G_HIT0, G_CUT, BEAT))

meta = {"take": "s01", "film": 24, "shots": [1, 2], "g0": 0, "g1": G_END, "first_g": 0, "n_frames": N,
        "handle_in": 0, "handle_out": H_OUT,
        "transition_in": {"type": "cut", "frames": 0, "note": "film start (no in-handle before g 0)"},
        "transition_out": {"type": "cut", "frames": 0, "note": "shot 3 (sea fleet_wide) follows at g 151; out-handle g 151..156 rendered in 3D (smoke + push continue)"},
        "transitions": [{"at": 0, "type": "cut"}, {"at": G_CUT, "type": "cut", "note": "plan hard cut shot 1 -> shot 2 at 2.60 s (inside the take; second build)"},
                        {"at": G_END, "type": "out", "handle": [G_END, N - 1]}],
        "shot_ranges": {"1": [0, G_CUT - 1], "2": [G_CUT, G_END - 1]},
        "setups": {"1": {"g": [0, G_CUT - 1], "preset": "roof_low", "camera": "the preset camera (15.8, 9, 3.6) -> (-0.5, -3.5, 5.9), 22 mm, pushed 8 % along its view line (0.35 sine + 0.65 linear), look point rising 0.25 D; DOF off",
                         "state": "set_spikes 2, set_ports 0, set_dragon_smoke 0 keyed every frame"},
                   "2": {"g": [G_CUT, N - 1], "preset": "macro_dragon", "camera": "preset lens 55 mm f/2.8, focus empty on the dragon mouth (0, 19.13, 3.20); custom position 11 D off at -50 deg on the west side, look 1.8 D ahead / 1.4 D above the mouth, pushed 5 %; sun re-aimed for this camera",
                         "state": "set_spikes 2, set_ports 0, set_dragon_smoke 0 -> 0.85 -> 1.2 (speed 1.3) keyed every frame, puffs released one by one from g 85"}},
        "events": {"hammer_strikes": hits, "strike_on_word_tok": 49, "cut_to_macro": G_CUT, "smoke_starts": G_SMOKE, "smoke_swells": G_PUFF},
        "set": "v3/set3d24/joseon.py yard (two builds: roof_low, macro_dragon); runtime dressing from common.py / shot.py only: puff release (hide_render keys), roof contact decals on the turtle ride, custom cameras, sun re-aim",
        "cast": "v3/cast24: yi24_stand_arms_behind (quay yi_quay, idle sway, feet planted); kor_a24_kneel_hammer (port roof edge worker_roof_p3, Child-Of the turtle ride, arm_r hammer every 12 frames); kor_d24_stand_carry_spikes (port roof edge local x 5.5, Child-Of the turtle ride, mirrored, planted)",
        "mouths": "no quote: fixed expression mouths",
        "dof": "shot 1 off; shot 2 the preset's f/2.8 on the mouth (no characters in shot 2)",
        "render": "R9: Cycles CPU, 24 adaptive samples (threshold 0.05), OIDN, AgX MHC, exposure 0.55, 540x960 then J.post -> 720x1280",
        "samples": 24, "resolution": [720, 1280], "render_resolution": [540, 960], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": mean(w[1] + w[2]), "s_per_frame_cpu_mean": mean(c[1] + c[2]),
        "s_per_frame_by_shot": {"1": {"wall": mean(w[1]), "cpu": mean(c[1])}, "2": {"wall": mean(w[2]), "cpu": mean(c[2])}},
        "narration": "film24/audio/narration.wav at +0.10 s; captions film24/script/captions.json"}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)


add(0, G_CUT, "Joseon naval yard, Yeosu 1592, daytime: gulls far off, water lapping at the slipway, distant carpentry (saws, mallets) and workers' voices", "ambience")
for g in hits:
    add(g, g, "hammer clink: iron hammer on an iron spike on the roof (bright metallic 'tink', small ring)", "foley", peak_frame=g)
add(G_CUT, G_CUT, "HARD CUT to the dragon head macro: yard ambience continues, a little quieter (closer, bokeh)", "cut")
add(G_SMOKE, N, "smoke hiss: a soft steam / smoke 'pfff' from the dragon mouth, puffs leaving one by one", "foley", peak_frame=G_SMOKE + 2)
add(G_PUFF - 6, G_PUFF + 4, "the smoke swells on 'พ่นควัน': a bigger whoosh-hiss", "accent", peak_frame=G_PUFF)
add(G_END, G_END, "plan: hard cut to shot 3, the Japanese fleet at sea (sea + drums far)", "cut")
json.dump(dict(take="s01", fps=30, note="time = film seconds (g / 30); narration PROJ/film24/audio/narration.wav at +0.10 s, captions.json", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)


def sheet(gs, path, w=270, cols=8, lab=18, label=None):
    h = w * 16 // 9; nrow = (len(gs) + cols - 1) // cols
    S = Image.new("RGB", (cols * w, nrow * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
    for i, g in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
        dr.text((x + 4, y + 3), label(g) if label else "g %d" % g, fill=(255, 255, 255))
    S.save(path, quality=88)


lab = lambda g: "g %d  %.2f s  shot %d%s" % (g, g / 30.0, 1 if g < G_CUT else 2, " handle" if g >= G_END else "")
sheet([int(round(i * (N - 1) / 15.0)) for i in range(16)], os.path.join(HERE, "contact.jpg"), label=lab)
sheet(list(range(0, G_CUT, 5)), os.path.join(WORK, "strip_s1.jpg"), w=240, cols=8, label=lab)
sheet(list(range(G_CUT, N, 5)), os.path.join(WORK, "strip_s2.jpg"), w=240, cols=8, label=lab)
sheet(list(range(G_CUT - 3, G_CUT + 4)), os.path.join(WORK, "cut.jpg"), w=240, cols=7, label=lab)

# QA numbers: heads, feet drift (planted check, screen px vs the camera move), timing
with open(os.path.join(WORK, "qa.txt"), "w") as fo:
    r1 = [r for r in rows if r["shot"] == 1]
    for n in sorted({n for r in r1 for n in r["heads"]}):
        hs = [r["heads"][n] for r in r1]
        fo.write("%-3s head w %.0f..%.0f px, centre y %.0f..%.0f, bottom max %.0f (caption band 880)\n" % (
            n, min(h["w"] for h in hs), max(h["w"] for h in hs), min(h["y"] for h in hs), max(h["y"] for h in hs), max(h["bottom"] for h in hs)))
    for n in sorted({n for r in r1 for n in r["feet"]}):
        fs = np.array([r["feet"][n] for r in r1]); d = np.hypot(*np.diff(fs, axis=0).T)
        fo.write("%-3s feet/ground screen path: start %s end %s, per-frame step max %.2f px (camera push only)\n" % (n, fs[0].tolist(), fs[-1].tolist(), d.max()))
    fo.write("render wall %.1f s / cpu %.1f s per frame; shot 1 %.1f / %.1f, shot 2 %.1f / %.1f; retried %s\n" % (
        meta["s_per_frame_wall_mean"], meta["s_per_frame_cpu_mean"], mean(w[1]), mean(c[1]), mean(w[2]), mean(c[2]), [r["g"] for r in rows if r.get("retried")]))

if "--no-encode" not in sys.argv:
    mkv = os.path.join(HERE, "take.mkv")
    for p in glob.glob(mkv + "*"):
        os.remove(p)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-start_number", "0", "-i", os.path.join(OUT, "g_%04d.png"),
                    "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
    mb = os.path.getsize(mkv) / 1e6
    print("take.mkv %.1f MB" % mb)
    if mb > 45:
        subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True, cwd=HERE)
        print("split into", sorted(glob.glob(mkv + ".part*")))
print(json.dumps({k: meta[k] for k in ("n_frames", "s_per_frame_wall_mean", "s_per_frame_cpu_mean", "s_per_frame_by_shot")}))

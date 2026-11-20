#!/usr/bin/env python3
"""deliver.py -- s15 delivery from raw/: frames/, take.mkv (libx264rgb crf 6), meta.json, cues.json, contact.jpg, framediff.json, QA_AUTO.
(s23's copy differs only in the CONFIG block.)"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
# ---- CONFIG
TAKE, SHOT = "s15", 15
G0, G1 = 996, 1093                 # shot = g G0..G1-1
H_IN, H_OUT = 8, 4
TR_IN = dict(type="dissolve", frames=13, note="DIS 13 into shot 15 from shot 14 (handle 8 frames g 988..995 rendered in 3D)")
TR_OUT = dict(type="cut", frames=0, at=G1, note="hard cut to shot 16 (CAFE cafe_low) at g 1093; handle g 1093..1096 rendered in 3D")
SET = "v3/set3d20 TOWER preset tower_fair, light DAY, year 1889, set_crowd(3) keyed every frame; the 24 crowd cards get a keyed idle bob + sway; preset lamp-post/bench moved far out of frame; foreground = a gent20 BACK card (top hat, brown coat) 3 D ahead of the lens in the bottom-left corner, feet underground, camera-relative every frame"
CAST = "v3/cast20 eiffel (proud -> worried + sweat swapped on the closed frame of a blink at g 1067, arm reaches, takes the document) + official (tricolour sash, doc_seal in the left hand held out toward Eiffel g 1008..1020, then hand to hip, happy); contact decals + proxy shadows; no lip-sync"
CAMERA = "custom 22 mm, shift 0.06 kept, cam z 1.6 D, 4.3 D from Eiffel (33 % closer than v1), aim ~6 deg under his head line; CamPath push 6 %/s + slide -45 px/s + arc 11 deg/s + tilt drift 1.5 deg/s, decay 0.25, push-in x1.2 g 1003..1011 on 'ใบอนุญาต', snap x1.85 g 1064..1080 (peak 2.0, tilt -3 deg) on 'ครบแล้วต้องรื้อ'"
EV = dict(push_in=[1003, 1011], permit_word=1000, doc_reach=[1008, 1030], doc_in_eiffel_hand=1020, twenty_years=1041, drop_word=1067, face_swap_blink=[1066, 1068], snap=[1064, 1079])
YEAR, LIGHT = 1889, "DAY"
CUTS = [G1]
CUES = [
    (G0, G1, "ambience", "Champ de Mars, sunny day 1889: fair crowd murmur, distant brass band, flags snapping in the breeze"),
    (1008, 1022, "foley", "the official's arm stretches out with the sealed document; paper rustle, a ceremonial 'ta-da' flourish", dict(peak_frame=1014)),
    (1020, 1024, "foley", "Eiffel takes the document: crisp paper grab + tiny pleased 'hm' (non-verbal)", dict(peak_frame=1021)),
    (1003, 1011, "accent", "push-in on 'ใบอนุญาต': soft whoosh + a paper-flutter swish", dict(peak_frame=1007)),
    (1064, 1079, "accent", "snap push on 'ครบแล้วต้องรื้อ': short airy whoosh rising", dict(peak_frame=1070)),
    (1066, 1070, "accent", "Eiffel's smile drops: comic descending slide-whistle 'womp' + a sweat-drop 'plip'", dict(peak_frame=1067)),
    (G1, G1, "cut", "hard cut to shot 16 (CAFE): ambience changes to the cafe room tone"),
]
MB_LIMIT = 45e6
# ---- /CONFIG
FIRST, LAST = G0 - H_IN, G1 + H_OUT - 1
N = LAST - FIRST + 1


def grey(p):
    return np.asarray(Image.open(p).convert("RGB").resize((90, 160), Image.BILINEAR), dtype=np.float32).mean(-1)


def contact(pngs, gs, out, cols=8, w=270):
    h, lab = w * 16 // 9, 18
    pick = [int(round(i * (len(pngs) - 1) / 15.0)) for i in range(16)]
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20))
    dr = ImageDraw.Draw(S)
    for i, k in enumerate(pick):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(pngs[k]).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
        g = gs[k]
        dr.text((x + 4, y + 3), "g %d  %.2f s%s" % (g, g / 30.0, "  handle" if g < G0 or g >= G1 else ""), fill=(255, 255, 255))
    S.save(out, quality=88)


RAW, OUT = os.path.join(HERE, "raw"), os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)
gs = list(range(FIRST, LAST + 1))
rows = []
for g in gs:
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
pngs = [os.path.join(OUT, "g_%04d.png" % g) for g in gs]
gr = [grey(p) for p in pngs]
d_all = {g: float(np.abs(gr[i] - gr[i - 1]).mean()) for i, g in enumerate(gs) if i}
ins = [d_all[g] for g in range(G0 + 1, G1)]                    # pairs inside the shot (no handles)
nb = dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), resized to 90x160 (bilinear), 0-255 levels; pairs (g-1,g) for g %d..%d (in-shot, no handles)" % (G0 + 1, G1 - 1),
          median=round(float(np.median(ins)), 2), p90=round(float(np.percentile(ins, 90)), 2), min=round(min(ins), 2), max=round(max(ins), 2),
          target=dict(median=4.0, p90=12.0), per_pair=[round(d_all[g], 2) for g in range(G0 + 1, G1)])
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
hd = [r["heads"]["eif"] for r in rows if G0 <= r["g"] < G1]
meta = dict(take=TAKE, film=20, shots=[SHOT], g0=G0, g1=G1, first_g=FIRST, n_frames=N, shot_ranges={str(SHOT): [G0, G1 - 1]},
            handle_in=H_IN, handle_out=H_OUT, transition_in=TR_IN, transition_out=TR_OUT, set=SET, cast=CAST, camera=CAMERA, events=EV,
            dof="none", text="none", light=LIGHT, year=YEAR, samples=rows[0].get("samples"), resolution=[720, 1280], threads=2, fps=30,
            s_per_frame_wall_mean=round(float(np.mean(walls)), 2), s_per_frame_cpu_mean=round(float(np.mean(cpus)), 2),
            head_px_main=[round(min(h["w"] for h in hd)), round(max(h["w"] for h in hd))],
            head_centre_y_main=[round(min(h["y"] for h in hd)), round(max(h["y"] for h in hd))],
            head_bottom_max_y=round(max(h["bottom"] for h in hd)),
            framediff_in_shot=dict(median=nb["median"], p90=nb["p90"]),
            narration="film20/audio/narration.wav at +0.10 s; captions film20/script/captions.json")
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
ev = []
for c in CUES:
    a, b, kind, note = c[:4]
    e = dict(kind=kind, t=round(a / 30.0, 3), dur=round(max(0, b - a) / 30.0, 3), frame=a, end_frame=b, note=note)
    if len(c) > 4:
        e.update(c[4])
    ev.append(e)
json.dump(dict(take=TAKE, fps=30, note="t = film seconds (g / 30); narration film20/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
contact(pngs, gs, os.path.join(HERE, "contact.jpg"))
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
if os.path.getsize(mkv) > MB_LIMIT:
    subprocess.run(["split", "-b", "40M", "take.mkv", "take.mkv.part"], check=True, cwd=HERE)
    print("take.mkv %.1f MB: split into parts" % (os.path.getsize(mkv) / 1e6))
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(FIRST), "--cuts", ",".join(map(str, CUTS))], capture_output=True, text=True)
print(r.stdout, r.stderr[-500:])
print("delivered %d frames, take.mkv %.1f MB; s/frame %.2f wall %.2f cpu; frame-diff median %.2f p90 %.2f"
      % (N, os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))

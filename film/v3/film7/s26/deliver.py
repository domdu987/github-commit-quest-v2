#!/usr/bin/env python3
"""deliver.py -- from raw/s1..s4 build frames/g_%04d.png (g 2567..2750), meta.json, cues.json, contact.jpg, compare.jpg, take.mkv.
    python3 deliver.py"""
import os, sys, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
# (shot.py imports bpy: its frame constants are repeated here)
G0, G27, G1, H = 2573, 2658, 2745, 6
G_B, G_D = 2612, 2698
RANGES = {1: (G0 - H, G_B - 1), 2: (G_B, G27 - 1), 3: (G27, G_D - 1), 4: (G_D, G1 + H - 1)}
FIRST, LAST = G0 - H, G1 + H - 1
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
NAMES = {1: "two-shot over the desk, the unwrap", 2: "the dealer inspects the panel", 3: "the dealer's secret signal", 4: "wide: police burst in, the arrest"}

src, rows = {}, []
for g in range(FIRST, LAST + 1):
    sid = [k for k, (a, b) in RANGES.items() if a <= g <= b][0]
    raw = os.path.join(HERE, "raw", "s%d" % sid)
    shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); src[g] = str(sid)
    rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
N = LAST - FIRST + 1

meta = {"take": "s26", "film": 7, "shots": [26, 27], "first_g": FIRST, "n_frames": N, "g0": G0, "g1": G1,
        "handle_in": H, "handle_out": H, "transition_in": "dissolve",
        "transition_in_detail": {"type": "dissolve", "frames": 12, "note": "from shot 25 (the attic) to the Florence shop; in-handle g 2567..2572 rendered in 3D (set-up 1 continues backward)"},
        "transition_out": {"type": "dissolve", "frames": 12, "note": "to s28 (the Louvre, the painting back); out-handle g 2745..2750 rendered in 3D (the arrest holds, camera keeps drifting)"},
        "transitions": [{"at": G0, "type": "dissolve_in", "handle": [FIRST, G0 - 1]}, {"at": G_B, "type": "cut", "note": "inside shot 26, on 'เสนอขาย' (87.07)"},
                        {"at": G27, "type": "cut", "note": "shot 27 starts"}, {"at": G_D, "type": "cut", "note": "on 'แล้วพาตำรวจ' (90.01): police burst in"},
                        {"at": G1, "type": "out", "handle": [G1, LAST]}],
        "shot_ranges": {"26": [G0, G27 - 1], "27": [G27, G1 - 1]},
        "setups": {str(k): {"g": list(v), "what": NAMES[k]} for k, v in RANGES.items()},
        "events": {"cloth_pulled_off": [2586, 2597], "presents_panel": 2599, "dealer_leans_in": [2595, 2603], "dealer_holds_panel_up": [G_B, G_B + 8],
                   "dealer_wink_and_beckon": [2676, 2696], "police_burst_in": G_D, "vincenzo_startled": [G_D + 4, 2715], "grabbed_arrested": 2716},
        "set": "v3/set3d7/louvre.py room/dealer_shop (SHOP_DAY): set_panel keyed per frame (off while the dealer holds it, set-up 2), set_flames keyed per frame; runtime wrapping-cloth prop (s26_cloth, louvre helpers + M['rag']) keyed off the panel; custom cameras 18-24 mm",
        "dof": "none (client rule: cam.data.dof.use_dof False + L.setup_dof(scene, None, None, cam=cam) at build and before every render)",
        "denoiser": "OpenImageDenoise, albedo+normal, prefilter FAST",
        "narration": "film7/audio/narration_bankky.wav at +0.10 s; captions film7/script/captions.json",
        "light": "SHOP_DAY",
        "cast": "v3/cast7: vincenzo (normal clothes, smug -> shocked -> vincenzo_arrested), dealer (dealer_smile / dealer_inspect with mona_panel x1.35 / dealer_signal wink), police x2 (run cycle -> police_arrest / police_stand); no lip-sync, STORY 'mouth' keys dropped",
        "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)


add(FIRST, LAST + 1, "Florence antique shop, 1913: a mantel clock ticking, street murmur and a church bell far off through the window", "ambience")
add(2586, 2597, "wrapping cloth whisked off the panel (cloth swish)", "prop", peak_frame=2590)
add(2597, 2612, "a soft magical shimmer as the panel is revealed", "accent", peak_frame=2598)
add(G_B, G_B + 8, "wooden panel lifted off the desk (light wood knock)", "prop", peak_frame=G_B + 3)
add(2620, 2655, "the dealer's thoughtful 'hmmm' (no lip-sync, under the narration)", "gesture", peak_frame=2630)
add(2676, 2696, "wink 'ting' + sly pizzicato as he beckons", "accent", peak_frame=2677)
add(G_D, G_D + 4, "door bursts open, two whistles, boots running on the parquet", "foley", peak_frame=G_D)
add(G_D + 4, 2715, "comic gasp sting (vincenzo startled)", "accent", peak_frame=G_D + 5)
add(2716, 2718, "grab: cloth thump, handcuff click", "foley", peak_frame=2717)
add(2718, LAST + 1, "sad trombone 'wah-wah'", "accent", peak_frame=2720)
json.dump(dict(take="s26", fps=30, note="time = film seconds (g / 30); narration PROJ/film7/audio/narration_bankky.wav at +0.10 s, captions.json", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = [int(round(FIRST + i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
    dr.text((x + 4, y + 3), "g %d %.2fs shot %d set-up %s%s" % (g, g / 30.0, 26 if g < G27 else 27, src[g], " handle" if g < G0 or g >= G1 else ""), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

PAIRS = [(2605, 15, "14 s"), (2735, 45, "44 s")]
w, h, lab = 360, 640, 20
Cm = Image.new("RGB", (len(PAIRS) * 2 * w + (len(PAIRS) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm)
x = 0
for g, tref, sec in PAIRS:
    Cm.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "s26 g %d (%.2f s)" % (g, g / 30.0), fill=(255, 255, 255))
    Cm.paste(Image.open(os.path.join(PROJ, "ref", "a", "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), "ref a t%04d (%s)" % (tref, sec), fill=(255, 220, 160))
    x += 2 * w + 12
Cm.save(os.path.join(HERE, "compare.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
print("delivered", N, "frames + take.mkv; mean wall %.2f s, cpu %.2f s" % (np.mean(walls), np.mean(cpus)))

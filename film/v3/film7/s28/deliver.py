#!/usr/bin/env python3
"""deliver.py -- from raw/s1..s4 build frames/g_%04d.png (g 2567..2750), meta.json, cues.json, contact.jpg, compare.jpg, take.mkv.
    python3 deliver.py"""
import os, sys, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
# (shot.py imports bpy: its frame constants are repeated here)
G0, G29, G1, H = 2745, 2865, 2980, 6
G_2, G_3, DIS, G_6 = 2781, 2830, (2900, 2911), 2946
RANGES = {1: (G0 - H, G_2 - 1), 2: (G_2, G_3 - 1), 3: (G_3, G29 - 1), 4: (G29, DIS[1]), 5: (DIS[0], G_6 - 1), 6: (G_6, G1 + H - 1)}
FIRST, LAST = G0 - H, G1 + H - 1
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
NAMES = {1: "eye level at the rope: she is back, the crowd streams in", 2: "reverse from the wall: the packed crowd's faces looking up at her",
         3: "side view along the wall: the crowd presses toward her", 4: "high oblique over the queue lanes: the EMPTY wall (match-dissolve A)",
         5: "same camera path: the painting back, a bigger crowd (match-dissolve B), push in", 6: "ECU on her face behind the glass, push in to the smile"}

src, rows = {}, []
for g in range(FIRST, LAST + 1):
    out = os.path.join(OUT, "g_%04d.png" % g)
    if DIS[0] <= g <= DIS[1]:                         # the match-dissolve: id 4 (empty wall) -> id 5 (crowd at the painting), same camera
        k = (g - DIS[0] + 1) / float(DIS[1] - DIS[0] + 2)
        A = np.asarray(Image.open(os.path.join(HERE, "raw", "s4", "g_%04d.png" % g)).convert("RGB"), dtype=np.float32)
        B = np.asarray(Image.open(os.path.join(HERE, "raw", "s5", "g_%04d.png" % g)).convert("RGB"), dtype=np.float32)
        Image.fromarray(np.clip(A * (1 - k) + B * k + 0.5, 0, 255).astype(np.uint8)).save(out)
        src[g] = "4+5"
        for s_ in (4, 5):
            rows.append(json.load(open(os.path.join(HERE, "raw", "s%d" % s_, "g_%04d.json" % g))))
        continue
    sid = [k for k, (a, b) in RANGES.items() if a <= g <= b][0]
    raw = os.path.join(HERE, "raw", "s%d" % sid)
    shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), out); src[g] = str(sid)
    rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
N = LAST - FIRST + 1

meta = {"take": "s28", "film": 7, "shots": [28, 29], "first_g": FIRST, "n_frames": N, "g0": G0, "g1": G1,
        "handle_in": H, "handle_out": H, "transition_in": "dissolve",
        "transition_in_detail": {"type": "dissolve", "frames": 12, "note": "from s26 (the Florence shop, the arrest) to the Louvre; in-handle g 2739..2744 rendered in 3D (set-up 1, she hangs alone)"},
        "transition_out": {"type": "cut", "frames": 0, "note": "shot 30 (empty_wall_queue, the modern-size crowd) follows; out-handle g 2980..2985 rendered in 3D (the ECU push continues)"},
        "transitions": [{"at": G0, "type": "dissolve_in", "handle": [FIRST, G0 - 1]}, {"at": G_2, "type": "cut", "note": "on 'กลายเป็นภาพ' (92.70)"},
                        {"at": G_3, "type": "cut"}, {"at": G29, "type": "cut", "note": "shot 29 starts: the empty-wall queue"},
                        {"at": DIS[0], "type": "match_dissolve", "frames": DIS[1] - DIS[0] + 1, "note": "inside the take, done in deliver.py: id 4 (empty wall, queue) -> id 5 (the painting back, crowd), identical camera"},
                        {"at": G_6, "type": "cut", "note": "punch-in to her face on 'ทำให้มันดัง' (98.54)"}, {"at": G1, "type": "out", "handle": [G1, LAST]}],
        "shot_ranges": {"28": [G0, G29 - 1], "29": [G29, G1 - 1]},
        "setups": {str(k): {"g": list(v), "what": NAMES[k]} for k, v in RANGES.items()},
        "events": {"crowd_streams_in": [2751, 2775], "crowd_faces_reverse": G_2, "match_dissolve": list(DIS), "push_in_to_her": [DIS[1], G_6 - 1], "ecu_smile": G_6},
        "qa_refs": [15, 105, 115],
        "set": "v3/set3d7/louvre.py louvre gallery (wall_eye build; empty_wall_queue build for id 4), GALLERY_DAY; set_mona / set_queue / set_mona_lift(0) / set_flames keyed per frame; cycles transparent_max_bounces 64 (stacked crowd cards); custom cameras 18-30 mm",
        "dof": "none (client rule: cam.data.dof.use_dof False + L.setup_dof(scene, None, None, cam=cam) at build and before every render)",
        "denoiser": "OpenImageDenoise, albedo+normal, prefilter FAST",
        "narration": "film7/audio/narration_bankky.wav at +0.10 s; captions film7/script/captions.json",
        "light": "GALLERY_DAY",
        "cast": "v3/cast7 crowd: lady / gentleman / newsboy (crowd_stare*, crowd_point*, lady_gasp; walk cycles when streaming in); no lip-sync, STORY 'mouth' keys dropped",
        "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)


add(FIRST, G29, "the Salon Carre 1914: a swelling murmur of a crowd, shoes on parquet, rustling skirts", "ambience")
add(FIRST, G0 + 10, "quiet: a lone footstep echo, she hangs alone (the 'nobody looked' beat)", "accent", peak_frame=G0)
add(2751, 2776, "the crowd rushes in: many footsteps, excited 'ooh!' voices (walla, no lip-sync)", "foley", peak_frame=2758)
add(G_2, G_3, "awed gasps, a lady's 'oh!', the rope creaking as they press", "foley", peak_frame=G_2 + 3)
add(G_3, G29, "crowd pressing, shuffling, a guard's 'reculez !' off screen", "foley", peak_frame=G_3 + 5)
add(G29, DIS[0], "the reopening day: hushed queue murmur before the empty wall", "ambience")
add(DIS[0], DIS[1] + 1, "match-dissolve: a shimmering harp gliss, the murmur swells into a crowd roar", "accent", peak_frame=DIS[0] + 6)
add(DIS[1], G_6, "push in: the crowd sound fades under a rising string swell", "music", peak_frame=G_6 - 5)
add(G_6, LAST + 1, "her smile: a soft music-box / celesta motif, the room falls quiet", "music", peak_frame=G_6)
json.dump(dict(take="s28", fps=30, note="time = film seconds (g / 30); narration PROJ/film7/audio/narration_bankky.wav at +0.10 s, captions.json", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = [int(round(FIRST + i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
    dr.text((x + 4, y + 3), "g %d %.2fs shot %d set-up %s%s" % (g, g / 30.0, 28 if g < G29 else 29, src[g], " handle" if g < G0 or g >= G1 else ""), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

PAIRS = [(2800, 15, "14 s"), (2975, 105, "104 s")]
w, h, lab = 360, 640, 20
Cm = Image.new("RGB", (len(PAIRS) * 2 * w + (len(PAIRS) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm)
x = 0
for g, tref, sec in PAIRS:
    Cm.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "s28 g %d (%.2f s)" % (g, g / 30.0), fill=(255, 255, 255))
    Cm.paste(Image.open(os.path.join(PROJ, "ref", "a", "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), "ref a t%04d (%s)" % (tref, sec), fill=(255, 220, 160))
    x += 2 * w + 12
Cm.save(os.path.join(HERE, "compare.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
print("delivered", N, "frames + take.mkv; mean wall %.2f s, cpu %.2f s" % (np.mean(walls), np.mean(cpus)))

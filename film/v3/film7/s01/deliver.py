#!/usr/bin/env python3
"""deliver.py -- from raw/s1 (corridor, g 0..39) + raw/s2 (street, g 40..78) build frames/g_%04d.png, meta.json, cues.json,
contact.jpg, compare.jpg (final frames beside the closest ref a frames) and take.mkv (libx264rgb crf 6, all frames g 0..78).
    python3 deliver.py"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))

G_END, H_OUT, G_CUT = 72, 7, 40
N = G_END + H_OUT
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)

src, rows = {}, []
for g in range(N):
    sid = 1 if g < G_CUT else 2
    raw = os.path.join(HERE, "raw", "s%d" % sid)
    shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); src[g] = str(sid)
    rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
w1 = [m["wall"] for m in rows if m["shot"] == 1]; w2 = [m["wall"] for m in rows if m["shot"] == 2]
c1 = [m["cpu"] for m in rows if m["shot"] == 1]; c2 = [m["cpu"] for m in rows if m["shot"] == 2]

meta = {"take": "s01", "film": 7, "shots": [1], "first_g": 0, "n_frames": N, "g0": 0, "g1": G_END,
        "handle_in": 0, "handle_out": H_OUT,
        "transition_in": {"type": "open", "frames": 0},
        "transition_out": {"type": "cut", "frames": 0, "note": "plan: shot 2 (louvre wall_eye, the empty wall) follows at g 72 (no dissolve listed); handle g 72..78 rendered in 3D (walk + track continue) in case the conform dissolves"},
        "transitions": [{"at": 0, "type": "open"}, {"at": G_CUT, "type": "cut", "note": "inside the take: corridor -> street, on 'ออกจาก' (1.48 s)"},
                        {"at": G_END, "type": "out", "handle": [G_END, N - 1]}],
        "shot_ranges": {"1": [0, G_END - 1]},
        "setups": {"1": {"g": [0, G_CUT - 1], "set": "louvre exit_door, CORRIDOR_MORNING"},
                   "2": {"g": [G_CUT, N - 1], "set": "paris street_wide area, STREET_GOLDEN, papers 0"}},
        "events": {"door_swings_open": [0, 14], "turns_to_lens": [10, 16], "nervous_grin_hands_on_bulge": [16, 30], "gulp": [22, 26],
                   "walks_to_doorway": [30, 39], "cut_to_street": G_CUT, "eyes_dart_left": [40, 48], "eyes_dart_right": [49, 55],
                   "grin_into_lens": 57},
        "set": "v3/set3d7/louvre.py: (1) exit_door + runtime dressing from shot.py (smock rail + caps, glazier's crates + panes, lit storm lantern, notices, key board, ladder, broom, toolbox, bucket, sack), fanlight shaft sheet hidden, set_door 28 -> 92 keyed per frame, set_flames keyed per frame, custom 20 mm camera; (2) paris street area (street_wide build) with a custom tracking camera at 22 mm, set_papers(0) keyed (nobody knows yet), set_flames keyed per frame",
        "dof": "none (client rule: cam.data.dof.use_dof False + L.setup_dof(scene, None, None, cam=cam) at build and before every render)",
        "denoiser": "OpenImageDenoise, albedo+normal, prefilter FAST",
        "narration": "film7/audio/narration_bankky.wav at +0.10 s; captions film7/script/captions.json",
        "light": "CORRIDOR_MORNING | STREET_GOLDEN",
        "cast": "v3/cast7: vincenzo_smock (bulge 1, sweat 0.5-0.9, pale 0.15-0.25; worried -> grinning; walk cycle with arms='l' and the right hand kept on the bulge)",
        "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "s_per_frame_by_setup": {"corridor": {"wall": round(float(np.mean(w1)), 2), "cpu": round(float(np.mean(c1)), 2)},
                                 "street": {"wall": round(float(np.mean(w2)), 2), "cpu": round(float(np.mean(c2)), 2)}},
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)


add(0, G_CUT, "Louvre service corridor, Monday morning: stone echo, a gas jet hissing softly, distant courtyard birds and city murmur growing as the door opens", "ambience")
add(0, 14, "heavy oak service door creaks open on its iron hinges, daylight floods in (warm whoosh of outside air)", "prop", peak_frame=6)
add(16, 30, "nervous grin at us: a tiny tense string tremolo / comic 'eek' sting", "accent", peak_frame=16)
add(22, 26, "audible gulp", "gesture", peak_frame=23)
add(30, G_CUT, "two quick hobnail footsteps on flagstones toward the doorway", "foley", peak_frame=33)
add(G_CUT, G_CUT, "hard cut to the street: the sound opens up", "cut")
add(G_CUT, N, "Paris street, sunny morning 1911: horse hooves and a fiacre wheel on cobbles, cafe chatter, pigeons, a distant tram bell", "ambience")
for k, g in enumerate(range(G_CUT + 3, N, 13)):
    add(g, g + 1, "his footstep on the cobbles (hobnail boots), smock rustle", "foley", peak_frame=g)
add(40, 55, "eyes dart left and right: two tiny whoosh-ticks", "accent", peak_frame=49)
add(57, N, "the nervous grin into the lens: a cheeky pizzicato sting", "accent", peak_frame=57)
add(G_END, G_END, "plan: cut to shot 2, the empty wall spot with four hooks (louvre wall_eye)", "cut")
json.dump(dict(take="s01", fps=30, note="time = film seconds (g / 30); narration PROJ/film7/audio/narration_bankky.wav at +0.10 s, captions.json", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = [int(round(i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
    dr.text((x + 4, y + 3), "g %d  %.2f s  shot 1%s%s" % (g, g / 30.0, " corridor" if g < G_CUT else " street", " handle" if g >= G_END else ""), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

PAIRS = [(20, 55, "54 s"), (64, 85, "84 s")]      # corridor before the bright doorway | walking toward us down a lane
w, h, lab = 360, 640, 20
Cm = Image.new("RGB", (len(PAIRS) * 2 * w + (len(PAIRS) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm)
x = 0
for g, tref, sec in PAIRS:
    Cm.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "shot 1  g %d (%.2f s)" % (g, g / 30.0), fill=(255, 255, 255))
    Cm.paste(Image.open(os.path.join(PROJ, "ref", "a", "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), "ref a t%04d (%s)" % (tref, sec), fill=(255, 220, 160))
    x += 2 * w + 12
Cm.save(os.path.join(HERE, "compare.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", "0", "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
print("delivered", len(src), "frames + take.mkv; mean wall %.2f s, cpu %.2f s" % (np.mean(walls), np.mean(cpus)))

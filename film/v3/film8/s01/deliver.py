#!/usr/bin/env python3
"""deliver.py -- from raw/s1 (shot 1, channels wide, g 0..74) + raw/s2 (shot 2, medium, g 75..183) build frames/g_%04d.png, meta.json,
cues.json, contact.jpg, compare.jpg (final frames beside the closest ref a frames) and take.mkv (libx264rgb crf 6, all frames g 0..183).
    python3 deliver.py"""
import os, sys, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))

G_CUT, G_END, H_OUT = 75, 178, 6
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

meta = {"take": "s01", "film": 8, "shots": [1, 2], "first_g": 0, "n_frames": N, "g0": 0, "g1": G_END,
        "handle_in": 0, "handle_out": H_OUT,
        "transition_in": {"type": "open", "frames": 0},
        "transition_out": {"type": "cut", "frames": 0, "note": "plan: shot 3 (bazaar NOON, bazaar_wide crane down) follows at g 178; handle g 178..183 rendered in 3D (the finger hold + push continue) in case the conform dissolves"},
        "transitions": [{"at": 0, "type": "open"}, {"at": G_CUT, "type": "cut", "note": "plan cut shot 1 -> shot 2 at 2.50 s, inside the take (same location and light, new set-up)"},
                        {"at": G_END, "type": "out", "handle": [G_END, N - 1]}],
        "shot_ranges": {"1": [0, G_CUT - 1], "2": [G_CUT, G_END - 1]},
        "setups": {"1": {"g": [0, G_CUT - 1], "set": "desert_ice plain (channels_wide build), NIGHT, ice 'water'; custom camera west over channel 4 looking ENE (az 79-80), 22 mm, slow push 1.8 D"},
                   "2": {"g": [G_CUT, N - 1], "set": "desert_ice plain, NIGHT, ice 'water'; custom low camera WSW of farid looking NE and up 9 deg (az 70-71.5), 22 mm, slow push + slight orbit"}},
        "events": {"pour_tip": [0, 8], "stream_and_ripples": [3, 66], "bucket_empties": [48, 66], "stream_stops_straightens": [62, 74],
                   "cut_to_medium": G_CUT, "looks_up_at_stars": [77, 112], "eyes_to_lens": [113, 125], "finger_up": [138, 148],
                   "smug_tilt": [160, 168]},
        "set": "v3/set3d8/desert.py desert_ice plain, NIGHT (stars + Milky Way, lantern posts, dome door glow): set_ice('water') keyed per frame, set_flames + set_stars (twinkle 0.35) keyed per frame; runtime additions from shot.py: two expanding ripple rings where the stream meets channel 4's water (keyed from the drawn pour_end_r anchor), D._bucket as a 3D prop on the bank in set-up 2 only (hide_render keyed)",
        "dof": "none (client rule: cam.data.dof.use_dof False + D.setup_dof(scene, None, None, cam=cam) at build and before every render)",
        "denoiser": "OpenImageDenoise, albedo+normal, prefilter FAST",
        "narration": "film8/audio/narration.wav at +0.10 s; captions film8/script/captions.json",
        "light": "NIGHT",
        "cast": "v3/cast8: farid (shot 1: STORY8 farid_pour animated pour 0.35 -> 0.85 -> 1.0 -> 0.3, bucket_water 1 -> 0, pour_len 1.35; shot 2: hands free, excited (looking up) -> happy -> smug, right index finger up)",
        "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "s_per_frame_by_setup": {"wide": {"wall": round(float(np.mean(w1)), 2), "cpu": round(float(np.mean(c1)), 2)},
                                 "medium": {"wall": round(float(np.mean(w2)), 2), "cpu": round(float(np.mean(c2)), 2)}},
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)


add(0, N, "desert night, Persia c. 1600: deep quiet, a soft cold wind over sand, crickets far off, the faint crackle of the distant camp fire; a slow airy pad under the stars", "ambience")
add(0, 8, "wooden bucket tips, its rope bail creaks, water sloshes inside", "prop", peak_frame=4)
add(3, 66, "steady water stream pouring and splashing into the shallow channel (gentle trickle-splash, stereo centre-left)", "foley", peak_frame=10)
add(48, 66, "the bucket runs dry: the stream thins to a few drips", "foley", peak_frame=62)
add(62, 74, "last drips plop into the channel; farid straightens with a small satisfied breath", "foley", peak_frame=66)
add(G_CUT, G_CUT, "cut to the medium: ambience continues unchanged (same place, same night)", "cut")
add(77, 112, "farid looks up at the Milky Way: a soft sparkling chime / twinkle shimmer", "accent", peak_frame=84)
add(113, 125, "eyes come down to us: a light 'hm' pizzicato", "accent", peak_frame=121)
add(138, 148, "finger goes up: a bright 'ting!' idea sting (ice-crystal tone)", "accent", peak_frame=146)
add(160, 168, "smug head tilt on 'น้ำแข็ง': a tiny cold frosty shimmer", "accent", peak_frame=164)
add(G_END, G_END, "plan: cut to shot 3, the bazaar at blazing noon (bazaar_wide crane down)", "cut")
json.dump(dict(take="s01", fps=30, note="time = film seconds (g / 30); narration PROJ/film8/audio/narration.wav at +0.10 s, captions.json", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = [int(round(i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
    dr.text((x + 4, y + 3), "g %d  %.2f s  shot %d%s" % (g, g / 30.0, 1 if g < G_CUT else 2, " handle" if g >= G_END else ""), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

PAIRS = [(30, 72, "a"), (100, 83, "a")]      # night wide: figure small in the lit set under a starry sky | night medium: figure under the sky
w, h, lab = 360, 640, 20
Cm = Image.new("RGB", (len(PAIRS) * 2 * w + (len(PAIRS) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm)
x = 0
for g, tref, rs in PAIRS:
    Cm.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "shot %d  g %d (%.2f s)" % (1 if g < G_CUT else 2, g, g / 30.0), fill=(255, 255, 255))
    Cm.paste(Image.open(os.path.join(PROJ, "ref", rs, "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), "ref %s t%04d" % (rs, tref), fill=(255, 220, 160))
    x += 2 * w + 12
Cm.save(os.path.join(HERE, "compare.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", "0", "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
print("delivered", len(src), "frames + take.mkv; mean wall %.2f s, cpu %.2f s" % (np.mean(walls), np.mean(cpus)))

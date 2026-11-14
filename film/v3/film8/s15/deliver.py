#!/usr/bin/env python3
"""deliver.py -- s15: raw/s1 (shot 15a stall, g 1168..1205), raw/s2 (shot 15b well, g 1206..1274), raw/s3 (shot 16 dome, g 1258..1352)
-> frames/ (the plan's 15 -> 16 DISSOLVE blended over g 1260..1271), meta.json, cues.json, contact.jpg, take.mkv (first_g 1168).
    python3 deliver.py"""
import os, sys, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))

G_IN, G0, G_B, G_DIS, G1, H, DIS = 1168, 1174, 1206, 1266, 1347, 6, 12
D0, D1 = G_DIS - DIS // 2, G_DIS + DIS // 2 - 1          # 1260..1271 blended
N = G1 + H - G_IN
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
src, rows = {}, []


def raw(sid, g):
    return os.path.join(HERE, "raw", "s%d" % sid, "g_%04d.png" % g)


for g in range(G_IN, G1 + H):
    dst = os.path.join(OUT, "g_%04d.png" % g)
    if g < G_B:
        shutil.copyfile(raw(1, g), dst); src[g] = "1"
    elif g < D0:
        shutil.copyfile(raw(2, g), dst); src[g] = "2"
    elif g <= D1:
        a = (g - D0 + 0.5) / DIS                                  # 0.04 .. 0.96, linear
        A = np.asarray(Image.open(raw(2, g)).convert("RGB"), dtype=np.float32)
        B = np.asarray(Image.open(raw(3, g)).convert("RGB"), dtype=np.float32)
        Image.fromarray(np.clip((1 - a) * A + a * B + 0.5, 0, 255).astype(np.uint8)).save(dst); src[g] = "2+3"
    else:
        shutil.copyfile(raw(3, g), dst); src[g] = "3"
for sid, (a, b) in ((1, (G_IN, G_B - 1)), (2, (G_B, G_DIS + 8)), (3, (G_DIS - 8, G1 + H - 1))):
    for g in range(a, b + 1):
        rows.append(json.load(open(raw(sid, g)[:-4] + ".json")))
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
by = lambda s, k: round(float(np.mean([m[k] for m in rows if m["shot"] == s])), 2)

meta = {"take": "s15", "film": 8, "shots": [15, 16], "first_g": G_IN, "n_frames": N, "g0": G0, "g1": G1,
        "handle_in": G0 - G_IN, "handle_out": H,
        "transition_in": {"type": "cut", "frames": 0, "note": "plan: shot 14 (merchant laughing) cuts to shot 15 at g 1174; in-handle g 1168..1173 rendered in 3D"},
        "transition_out": {"type": "cut", "frames": 0, "note": "plan: shot 17 (NIGHT sky_reveal) follows at g 1347; handle g 1347..1352 rendered in 3D"},
        "transitions": [{"at": G0, "type": "cut", "handle": [G_IN, G0 - 1]},
                        {"at": G_B, "type": "cut", "note": "inside shot 15: merchant's stall -> the well in the square (same bazaar, same light), on 'น้ำในบ่อทั้งเมือง'"},
                        {"at": G_DIS, "type": "dissolve", "frames": DIS, "blend": [D0, D1], "note": "plan shot 15 -> 16 dissolve (bazaar -> inside the dome), blended in this take; both sides rendered 8 frames past the centre (raw/s2 to g 1274, raw/s3 from g 1258)"},
                        {"at": G1, "type": "out", "handle": [G1, G1 + H - 1]}],
        "shot_ranges": {"15": [G0, G_DIS - 1], "16": [G_DIS, G1 - 1]},
        "setups": {"1": {"g": [G_IN, G_B - 1], "set": "bazaar SUMMER, the water merchant's stall: camera from the street WSW of the takht looking NE (22 mm, z 3.7 -> 3.6), push 1.3 D + orbit; steam over the five great jars"},
                   "2": {"g": [G_B, G_DIS + 8], "set": "bazaar SUMMER, the square by the well (near the well_eye preset): camera SW looking NNE up at the iwan and minaret (22 mm, z 2.5, pitch +4), push 1.6 D; steam over the well and the poured jar"},
                   "3": {"g": [G_DIS - 8, G1 + H - 1], "set": "desert_ice dome_interior SUMMER: camera on the walkway (20 mm) cranes down 0.7 D + pushes 1.7 D + pans onto farid on the ice; runtime ice-block stacks 2-5 high round him; warm lantern light + halo keyed to the drawn lantern"}},
        "events": {"merchant_sweats_fans": [G_IN, G_B - 1], "cut_to_well": G_B, "bucket_tips_pour": [1210, 1222], "pour_and_steam": [1214, 1274],
                   "fanning": [G_B, 1274], "dissolve": [D0, D1], "farid_with_lantern": [D0, G1 + H - 1], "farid_turns_to_us_smug": [1300, 1314]},
        "lipsync": "none (no quote in shots 15-16; static mouths)",
        "set": "v3/set3d8/desert.py: bazaar SUMMER (merchant_stall build) + desert_ice dome_interior SUMMER; set_flames + set_stars keyed every frame; runtime from shot.py: scrolling camera-only steam cards (bakery._mat_add with the set's wisp texture) over the merchant's five jars, the well water and the woman's jar; four jars + two pots in the square; a jar under the pour (keyed to the drawn stream end); 13 columns of ice blocks 2-5 high on the ice top in the dome; a warm point light + halo at farid's lantern",
        "dof": "none (client rule)", "denoiser": "OpenImageDenoise, prefilter FAST",
        "narration": "film8/audio/narration.wav at +0.10 s; captions film8/script/captions.json", "light": "SUMMER",
        "cast": "v3/cast8: merchant (merchant_sweat, fan beating every 8 frames), woman (bucket pour 0.3 -> 0.86 into a jar, sweat + heat), oldman (town_fan_oldman mirrored), boy (town_fan_boy flapping hand), farid (lantern held up, happy -> smug, calm)",
        "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "s_per_frame_by_setup": {k: {"wall": by(s, "wall"), "cpu": by(s, "cpu")} for k, s in (("15a_stall", 1), ("15b_well", 2), ("16_dome", 3))},
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)


add(G_IN, D1, "bazaar in high summer: oppressive heat buzz (cicadas), murmuring crowd, flies, a slow sweltering drone", "ambience")
add(G_IN, G_B - 1, "the merchant's palm fan flapping (one beat every 8 frames), heavy panting; soft simmering hiss of steam over the jars", "foley", peak_frame=1180)
add(G_B, G_B, "cut to the well in the square (ambience continues)", "cut")
add(1210, 1222, "the woman tips the wooden bucket", "prop", peak_frame=1216)
add(1214, D1, "warm water pouring into the clay jar (hollow glugging), a faint steam hiss", "foley", peak_frame=1222)
add(G_B, D1, "fans flapping (old man), the boy flapping his hand, sighs 'phew'", "foley", peak_frame=1235)
add(D0, D1, "DISSOLVE to the inside of the dome: the bazaar noise fades out, a cool hollow room tone fades in", "transition")
add(G_DIS, G1 + H, "inside the yakhchal: cool reverberant hush, slow drips of meltwater, the lantern flame's soft flutter; a cool crystalline shimmer pad", "ambience")
add(1300, 1314, "farid turns to us with a knowing smile: a light glassy 'ting'", "accent", peak_frame=1310)
add(G1, G1, "plan: cut to shot 17 (night sky reveal)", "cut")
json.dump(dict(take="s15", fps=30, note="time = film seconds (g / 30); narration PROJ/film8/audio/narration.wav at +0.10 s, captions.json", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = [G_IN + int(round(i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
    tag = "handle" if (g < G0 or g >= G1) else ("dissolve" if D0 <= g <= D1 else "")
    dr.text((x + 4, y + 3), "g %d  %.2f s  shot %d %s" % (g, g / 30.0, 15 if g < G_DIS else 16, tag), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(G_IN), "-i", os.path.join(OUT, "g_%04d.png"),
                "-frames:v", str(N), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
print("delivered", len(src), "frames + take.mkv (%.1f MB); mean wall %.2f s, cpu %.2f s" % (os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus)))

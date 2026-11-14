#!/usr/bin/env python3
"""deliver.py -- s13: raw/s1 (shot 13, g 958..1064 incl. in-handle) + raw/s2 (shot 14, g 1065..1179 incl. out-handle) -> frames/,
meta.json, cues.json, contact.jpg, take.mkv (libx264rgb crf 6, first_g 958).   python3 deliver.py"""
import os, sys, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))

G_IN, G0, G_CUT, G1, H = 958, 964, 1065, 1174, 6
N = G1 + H - G_IN
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
src, rows = {}, []
for g in range(G_IN, G1 + H):
    sid = 1 if g < G_CUT else 2
    raw = os.path.join(HERE, "raw", "s%d" % sid)
    shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); src[g] = str(sid)
    rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
by = lambda s, k: round(float(np.mean([m[k] for m in rows if m["shot"] == s])), 2)

meta = {"take": "s13", "film": 8, "shots": [13, 14], "first_g": G_IN, "n_frames": N, "g0": G0, "g1": G1,
        "handle_in": G0 - G_IN, "handle_out": H,
        "transition_in": {"type": "cut", "frames": 0, "note": "plan: shot 12 (DAWN, farid saws and carries ice) cuts to shot 13 at g 964; in-handle g 958..963 rendered in 3D (farid asleep, crane already moving)"},
        "transition_out": {"type": "cut", "frames": 0, "note": "plan: shot 15 (bazaar SUMMER) follows at g 1174; handle g 1174..1179 rendered in 3D (laugh continues, push continues)"},
        "transitions": [{"at": G0, "type": "cut", "handle": [G_IN, G0 - 1]}, {"at": G_CUT, "type": "cut", "note": "plan cut shot 13 -> 14 at 35.50 s, inside the take (same location and light)"},
                        {"at": G1, "type": "out", "handle": [G1, G1 + H - 1]}],
        "shot_ranges": {"13": [G0, G_CUT - 1], "14": [G_CUT, G1 - 1]},
        "setups": {"1": {"g": [G_IN, G_CUT - 1], "set": "desert_ice plain, NOON (sun raised to 70 deg at runtime), set_ice('mud') keyed every frame; camera starts low NW of farid at the wall foot looking SE (az 116, 22 mm) and cranes up + back west + pans left to az 101 (z 1.6 -> 6.2): the channels of mud running to the dome"},
                   "2": {"g": [G_CUT, G1 + H - 1], "set": "desert_ice plain, NOON (sun 70), mud; medium on the merchant on the bank between channels 4 and 5 from WNW over channel 5 looking ESE (az 105 -> 107.5, 22 mm, z 2.7), slow push 1.1 D + orbit; dome + wall behind, farid small beyond channel 5"}},
        "events": {"asleep": [G_IN, 979], "jolt_awake": [980, 985], "shocked_arms_up": [985, 1000], "hands_to_head_stares_at_mud": [1000, 1064],
                   "cut_to_merchant": G_CUT, "big_laugh": [G_CUT, 1075], "bends_laughing_to_tears": [1076, 1112], "quote_lipsync": [1113, 1170],
                   "points_at_mud": [1107, 1160], "laugh_again_horok": [1162, 1179]},
        "lipsync": {"who": "merchant", "g": [1113, 1170], "text": "เห็นมั้ย ทะเลทรายไม่มีน้ำแข็งหรอก!", "method": "cast8.talk_mouth(g, level) with level = narration RMS envelope at g (2-frame holds); static 'talk_b' laughing mouth outside the quote"},
        "set": "v3/set3d8/desert.py desert_ice plain, NOON light with the sun raised 44 -> 70 deg at runtime (D.STATE['sun'] rotation; the wall's shadow ends at y ~4.7: farid sleeps in the shade, the mud of channels 2-5 and the merchant are in the blazing sun); set_ice('mud') + set_flames + set_stars keyed every frame; runtime dressing from shot.py: straw mat, buckets, jars, saw, pick, mud-brick pile, rocks at the wall foot, six palms + shrubs north of the channels",
        "dof": "none (client rule)", "denoiser": "OpenImageDenoise, prefilter FAST",
        "narration": "film8/audio/narration.wav at +0.10 s; captions film8/script/captions.json", "light": "NOON (sun 70 deg)",
        "cast": "v3/cast8: farid (farid_sleep lie 90 -> farid_wake_shocked with lie 90 -> 0 over g 980..985, pale, sweat; shot 14 background: sad, head down), merchant (merchant_laugh -> merchant_tears with cry + tears, pointing at the mud for the quote, lip-sync)",
        "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "s_per_frame_by_setup": {"13": {"wall": by(1, "wall"), "cpu": by(1, "cpu")}, "14": {"wall": by(2, "wall"), "cpu": by(2, "cpu")}},
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)


add(G_IN, G1 + H, "desert at blazing noon: hot dry wind over sand, cicada-like heat buzz, flies; distant camel bell; a lazy heat-haze drone", "ambience")
add(G_IN, 979, "farid snoring softly in the shade of the wall (slow in-out breaths, a little whistle)", "foley", peak_frame=970)
add(980, 986, "jolts awake: a sharp gasp + a comic 'boing' / spring stinger", "accent", peak_frame=983)
add(986, 1003, "panicked breaths, sandals scuffing as he springs up", "foley", peak_frame=990)
add(1004, 1064, "a slow wet squelch / bubbling mud (the ice has melted to mud); a sad descending 'wah-wah' brass", "accent", peak_frame=1010)
add(G_CUT, G_CUT, "cut to the merchant, same place (ambience continues)", "cut")
add(G_CUT, 1112, "the merchant's huge belly laugh, wheezing, slapping his knee (slaps on the right hand's down-beats)", "foley", peak_frame=1085)
add(1076, 1112, "laughing to tears: high-pitched helpless giggle, sniffles", "foley", peak_frame=1095)
add(1113, 1170, "merchant's quote (narration voice): 'เห็นมั้ย ทะเลทรายไม่มีน้ำแข็งหรอก!' -- lip-sync", "dialogue")
add(1162, G1 + H, "bursts out laughing again on 'หรอก!'", "foley", peak_frame=1168)
add(G1, G1, "plan: cut to shot 15, the bazaar in summer", "cut")
json.dump(dict(take="s13", fps=30, note="time = film seconds (g / 30); narration PROJ/film8/audio/narration.wav at +0.10 s, captions.json", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = [G_IN + int(round(i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
    tag = "handle" if (g < G0 or g >= G1) else ""
    dr.text((x + 4, y + 3), "g %d  %.2f s  shot %d %s" % (g, g / 30.0, 13 if g < G_CUT else 14, tag), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(G_IN), "-i", os.path.join(OUT, "g_%04d.png"),
                "-frames:v", str(N), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
print("delivered", len(src), "frames + take.mkv (%.1f MB); mean wall %.2f s, cpu %.2f s" % (os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus)))

#!/usr/bin/env python3
"""deliver.py -- from raw/s20 (shot 20 wide + 6 in-handle frames, g 1661..1751) + raw/s21 (shot 21 two-shot, g 1752..1838) build
frames/g_%04d.png, meta.json, cues.json, contact.jpg, compare.jpg and take.mkv (libx264rgb crf 6, all frames g 1661..1838).
    python3 deliver.py"""
import os, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))

FIRST, G0, G_CUT, LAST = 1661, 1667, 1752, 1838
SAY = (1797, 1827); SWAP = 1817
N = LAST - FIRST + 1
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)

src, rows = {}, []
for g in range(FIRST, LAST + 1):
    sid = 20 if g < G_CUT else 21
    raw = os.path.join(HERE, "raw", "s%d" % sid)
    shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); src[g] = str(sid)
    rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
by = lambda s, k: round(float(np.mean([m[k] for m in rows if m["shot"] == s])), 2)

meta = {"take": "s20", "film": 8, "shots": [20, 21], "first_g": FIRST, "n_frames": N, "g0": G0, "g1": LAST + 1,
        "handle_in": G0 - FIRST, "handle_out": 0,
        "transition_in": {"type": "cut", "frames": 0, "note": "plan: shot 19 (NIGHT channel_ecu) cuts to SUMMER day here; in-handle g 1661..1666 rendered in 3D (the walk + truck continue backward) in case the conform dissolves"},
        "transition_out": {"type": "end", "frames": 0, "note": "last film frame g 1838 (N = 1839); no out-handle"},
        "transitions": [{"at": FIRST, "type": "in_handle", "handle": [FIRST, G0 - 1]}, {"at": G0, "type": "cut"},
                        {"at": G_CUT, "type": "cut", "note": "plan cut shot 20 -> shot 21 at 58.40 s, inside the take (same location and light, new set-up)"},
                        {"at": LAST + 1, "type": "end"}],
        "shot_ranges": {"20": [G0, G_CUT - 1], "21": [G_CUT, LAST]},
        "setups": {"20": {"g": [FIRST, G_CUT - 1], "set": "desert_ice plain (dome_wide build), SUMMER, ice 'mud'; custom camera south-west over the mud channels looking NE (az 52 -> 55, pitch +5), z 2.7, 22 mm, trucks 1.85 D east with the queue"},
                   "21": {"g": [G_CUT, LAST], "set": "desert_ice plain, SUMMER, ice 'mud'; custom camera south of the pair over channel 3 looking N (az 6 -> 9, pitch +4), z 2.4, 22 mm, slow push 0.75 D + slight pan"}},
        "events": {"queue_walks_to_dome": [FIRST, G_CUT - 1], "cut_to_two_shot": G_CUT, "purse_held_out_scratching_turban": [G_CUT, SWAP - 1],
                   "lipsync_merchant": list(SAY), "farid_holds_out_ice_block": [1798, 1812], "swap_purse_for_block": SWAP,
                   "merchant_looks_at_his_one_block": [SWAP + 4, LAST], "hold_to_end": [1828, LAST]},
        "set": "v3/set3d8/desert.py desert_ice plain, SUMMER (white-hot sun, haze): set_ice('mud') + set_flames + set_stars keyed per frame; runtime dressing from shot.py dress(): a couched camel with saddle bags beyond the channels + two standing camels far north, 4 date palms, 3 water jars, a straw mat with 3 ice blocks by the porch, shrubs, rocks",
        "dof": "none (client rule: cam.data.dof.use_dof False + D.setup_dof(scene, None, None, cam=cam) at build and before every render)",
        "denoiser": "OpenImageDenoise, albedo+normal, prefilter FAST",
        "narration": "film8/audio/narration.wav at +0.10 s; captions film8/script/captions.json",
        "light": "SUMMER",
        "cast": "v3/cast8: shot 20 merchant walk cycle (worried, sweat + heat, coin purse in the right hand), queue woman (water jar on the shoulder), oldman (stick), boy, woman (fanning) walking behind in single file, farid at the porch door (farid_smile, arms folded); shot 21 merchant_pay (sheepish, blush, scratching his turban, purse out; talk_mouth 1797..1827 only), farid (mirrored) holding out one ice block; props swap at g 1817",
        "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "s_per_frame_by_setup": {"wide": {"wall": by(20, "wall"), "cpu": by(20, "cpu")}, "two_shot": {"wall": by(21, "wall"), "cpu": by(21, "cpu")}},
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)


add(FIRST, LAST, "desert summer noon: hot dry wind, cicada-like heat buzz, distant camel grunt; a warm, gently comic ending pad", "ambience")
add(G0, G0, "cut from the cold starry night to blazing summer: a bright warm swell", "cut")
add(G0, G_CUT - 1, "the queue's footsteps on hard dry earth, the merchant's heavy coin purse jingling with each step, a palm fan flapping", "foley", peak_frame=1700)
add(1700, 1712, "the merchant puffs and pants in the heat", "foley", peak_frame=1705)
add(G_CUT, G_CUT, "cut to the two-shot at the dome door", "cut")
add(G_CUT, 1795, "sheepish turban scratch (a small cloth rustle), coins clink as he holds out the purse", "foley", peak_frame=1770)
add(SAY[0], SAY[1], "merchant's line 'ข้าจะซื้อหมดเลย' (in the narration) lip-synced", "dialogue")
add(1798, 1812, "farid holds out one ice block: a cold crystal shimmer", "accent", peak_frame=1810)
add(SWAP, SWAP + 3, "the swap: a heavy coin thud into farid's hand + an ice clink", "prop", peak_frame=SWAP)
add(1828, LAST, "the merchant looks at his single block: a light comic button / sting to end the film", "accent", peak_frame=1830)
json.dump(dict(take="s20", fps=30, note="time = film seconds (g / 30); narration PROJ/film8/audio/narration.wav at +0.10 s, captions.json", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = [FIRST + int(round(i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
    dr.text((x + 4, y + 3), "g %d  %.2f s  shot %d%s" % (g, g / 30.0, 20 if g < G_CUT else 21, " handle" if g < G0 else ""), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

PAIRS = [(1720, os.path.join("a", "t0061.jpg")), (1812, os.path.join("b", "t0029.jpg"))]
w, h, lab = 360, 640, 20
Cm = Image.new("RGB", (len(PAIRS) * 2 * w + (len(PAIRS) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm)
x = 0
for g, ref in PAIRS:
    Cm.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "shot %d  g %d (%.2f s)" % (20 if g < G_CUT else 21, g, g / 30.0), fill=(255, 255, 255))
    Cm.paste(Image.open(os.path.join(PROJ, "ref", ref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), "ref " + ref, fill=(255, 220, 160))
    x += 2 * w + 12
Cm.save(os.path.join(HERE, "compare.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
print("delivered", len(src), "frames + take.mkv (%.1f MB); mean wall %.2f s, cpu %.2f s" % (os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus)))

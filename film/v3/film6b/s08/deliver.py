#!/usr/bin/env python3
"""deliver.py -- from raw/s1 build frames/g_%04d.png (g 308..627), meta.json, cues.json, contact.jpg, compare.jpg and take.mkv
(libx264rgb crf 6, first_g 308; split into 40 MB parts if > 45 MB).  python3 deliver.py"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
G0, G1, H = 314, 622, 6
GA, GB = G0 - H, G1 + H - 1
N = GB - GA + 1
RAW = os.path.join(HERE, "raw", "s1"); OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
for g in range(GA, GB + 1):
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
rows = [json.load(open(js)) for js in sorted(glob.glob(os.path.join(RAW, "g_*.json")))]
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
SH = {"8": [314, 359], "9": [360, 398], "10": [399, 465], "11": [466, 533], "12": [534, 621]}
meta = {"take": "s08", "film": "6b", "shots": [8, 9, 10, 11, 12], "g0": G0, "g1": G1, "first_g": GA, "n_frames": N,
        "handle_in": H, "handle_out": H,
        "transition_in": {"type": "cut", "frames": 0}, "transition_out": {"type": "cut", "frames": 0},
        "shot_ranges": SH,
        "framings": {"8": "low CU henry + board 'ร้านลุงเฮนรี่', push up (handle g 308..313 = same framing)",
                     "9": "ECU loaf pan + tag '500 ก.', henry's face behind the beam",
                     "10": "MCU behind the balance g 399..437; punch-in CU g 438..465 (finger wag)",
                     "11": "CU kit + basket g 466..493; snap zoom g 494..499; CU henry wide eyes g 500..533",
                     "12": "low CU yell, kit in the foreground g 534..591; punch-in ECU purple face g 592..621 (+ handle to 627)"},
        "events": {"beam_settles_level": 392, "crumb_dropped": 414, "crumb_lands_beam_dips": 418, "crumb_picked_off": 436,
                   "finger_wag": [438, 465], "loaf_13_drops": 480, "henry_spots": 486, "snap_zoom": [494, 499], "eyes_wide": 495,
                   "quote_lipsync": [536, 621], "punch_in_yell": 592},
        "set": "v3/set3d6/bakery.py bakery MORNING, steam 0.30, oven flicker keyed per frame; small balance keyed (set_scale) per frame; "
               "added at runtime: 2 cool blue area lights on the back wall / upper back wall (complementary colour), PropCards: board "
               "'ร้านลุงเฮนรี่', tag '500 ก.' riding the loaf pan, crumb, basket 12/13 (cast6.basket_svg)",
        "signs": "Kanit Black embedded in SVG, rasterised with headless Chromium after document.fonts.ready (signs.py, raster_fonts.js)",
        "dof": "none (C.Take: use_dof False + B.setup_dof(None) at build and before every render)",
        "narration": "film6b/audio/narration.wav at +0.10 s; lip-sync from the narration RMS envelope g 536..621",
        "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2)}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)

ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label)
    e.update(kw); ev.append(e)


add(GA, GB + 1, "inside the bakery, morning: oven fire crackle, low room tone", "ambience")
add(314, 314, "cut to henry: low brass 'boss' sting", "cut")
add(360, 392, "the hand balance wobbles: small metal creaks, chains tinkle", "prop", peak_frame=360)
add(392, 394, "beam stops dead level on 'เป๊ะ': crisp 'tick'", "accent", peak_frame=392)
add(414, 418, "crumb drops on the brass pan: tiny 'tink', beam dips (creak)", "prop", peak_frame=418)
add(436, 442, "crumb plucked off: tiny pop, beam levels (creak)", "prop", peak_frame=436)
add(438, 465, "finger wag 'tut tut' (two wag whooshes)", "gesture", peak_frame=449)
add(479, 481, "the 13th loaf thumps on top of the basket pile", "prop", peak_frame=480)
add(494, 499, "SNAP ZOOM to henry: fast whoosh + hit", "accent", peak_frame=499)
add(499, 534, "henry's eyes go wide: rising tension string", "accent", peak_frame=499)
add(534, 622, "henry's YELL: steam whistles from his ears, kettle boil under the line", "fx", peak_frame=596)
add(592, 593, "punch-in on 'ข้าเจ๊งเหรอ!': hit", "accent", peak_frame=592)
add(G1, G1, "plan: cut to shot 13 (market, pillories)", "cut")
json.dump(dict(take="s08", fps=30, note="time = film seconds (g / 30); narration PROJ/film6b/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)

gs = [int(round(GA + i * (N - 1) / 15.0)) for i in range(16)]
shot = lambda g: next((k for k, (a, b) in SH.items() if a <= g <= b), "handle")
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.text((x + 4, y + 3), "g %d  %.2f s  shot %s" % (g, g / 30.0, shot(g)), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

# compare: our big faces / signs beside the reference sheets' closest ideas (pink sheet: big face CU, sign insert)
PAIRS = [(340, "pink_0.jpg"), (612, "pink_0.jpg")]
w, h, lab = 360, 640, 20
Cm = Image.new("RGB", (4 * w + 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm)
for k, g in enumerate((340, 385, 515, 612)):
    Cm.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (k * w, lab))
    dr.text((k * w + 4, 4), "shot %s g %d" % (shot(g), g), fill=(255, 255, 255))
ref = Image.open(os.path.join(PROJ, "analysis", "sheets", "pink_0.jpg")).convert("RGB")
cw, ch = ref.width / 6.0, ref.height / 6.0
crop = ref.crop((int(cw * 1), int(ch * 3), int(cw * 2), int(ch * 4))).resize((w // 2, h // 2))     # big face CU (19 s)
Cm2 = Image.new("RGB", (Cm.width + w // 2 + 8, Cm.height), (16, 12, 20)); Cm2.paste(Cm, (0, 0)); Cm2.paste(crop, (Cm.width + 8, lab))
ImageDraw.Draw(Cm2).text((Cm.width + 12, 4), "ref pink 19 s", fill=(255, 220, 160))
Cm2.save(os.path.join(HERE, "compare.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(GA), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
sz = os.path.getsize(mkv)
for p in glob.glob(mkv + ".part*"):
    os.remove(p)
if sz > 45e6:
    subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True)
print("delivered %d frames, take.mkv %.1f MB; mean wall %.2f s, cpu %.2f s" % (N, sz / 1e6, np.mean(walls), np.mean(cpus)))

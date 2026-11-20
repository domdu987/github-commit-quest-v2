#!/usr/bin/env python3
"""deliver.py -- delivery of a CAFE Maupassant take (s09 / s10 / s16 / s17, chosen by folder name) from raw/g_%04d.png (+ .json):
frames/, take.mkv (libx264rgb crf 6; split if > 45 MB), meta.json, cues.json, contact.jpg, framediff.json, then qa_auto.py.  No bpy.
    python3 deliver.py"""
import os, sys, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
SHOT = int(os.path.basename(HERE)[1:])
H = 4
G0, G1 = {9: (604, 675), 10: (676, 752), 16: (1093, 1142), 17: (1143, 1220)}[SHOT]   # in-shot frames, inclusive
FIRST, LAST = G0 - H, G1 + H
N = LAST - FIRST + 1
EV = {
    9: dict(rise=[612, 634], seat_to_stand=[612, 640], cravat_tugs=[640, 658], snap=[657, 672], word_declares=659, chin_up=[654, 668], mouth="none (quote starts g 682)"),
    10: dict(quote1_window=[682, 755], turn_away=[676, 712], eyes_shut_blink=685, snap=[729, 744], word_last=732, mouth="lip-sync g 682..755 from the narration loudness"),
    16: dict(crash_pull_out=[1090, 1110], laugh_bounce_hz=3, laugh_word=1117, mouth="expression grin until g 1116, lip-sync from g 1117"),
    17: dict(quote2_window=[1117, 1223], thumb_over_shoulder=[1143, 1220], crumple_mime=[1190, 1210], snap=[1192, 1207], word_scrap=1195, mouth="lip-sync g 1117..1223 from the loudness"),
}[SHOT]
WORDS = {9: "Maupassant rises from the banquette, tugs his cravat, chin up", 10: "QUOTE 1 lip-sync; he turns his back on the window, eyes shut, arms crossed",
         16: "belly laugh at the full tower, crash pull-out", 17: "QUOTE 2 lip-sync; thumb over the shoulder at the tower, crumple mime"}[SHOT]


def framediff(pngs):
    prev, d = None, []
    for p in pngs:
        a = np.asarray(Image.open(p).convert("RGB").resize((90, 160), Image.BILINEAR), dtype=np.float32).mean(-1)
        if prev is not None:
            d.append(float(np.abs(a - prev).mean()))
        prev = a
    return d


def contact(pngs, out, cols=8, w=270):
    h, lab = w * 16 // 9, 18
    idx = [int(round(i * (len(pngs) - 1) / 15.0)) for i in range(16)]
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20))
    dr = ImageDraw.Draw(S)
    for i, k in enumerate(idx):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(pngs[k]).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
        g = FIRST + k
        dr.text((x + 4, y + 3), "g %d  %.2f s%s" % (g, g / 30.0, "  handle" if (g < G0 or g > G1) else ""), fill=(255, 255, 255))
    S.save(out, quality=88)


RAW, OUT = os.path.join(HERE, "raw"), os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)
rows = []
for g in range(FIRST, LAST + 1):
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
pngs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(FIRST, LAST + 1)]
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
inshot = rows[H:H + (G1 - G0 + 1)]
heads = [r["heads"]["mau"] for r in inshot]
d = framediff(pngs)
ins = d[H:H + (G1 - G0)]                                  # pairs (g-1, g) for g in G0+1 .. G1 (in-shot only)
nb = dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), 90x160 bilinear, 0-255; in-shot pairs only (no handles)",
          median=round(float(np.median(ins)), 2), p90=round(float(np.percentile(ins, 90)), 2), min=round(min(ins), 2), max=round(max(ins), 2),
          target=dict(median=4.0, p90=12.0), per_pair=[round(v, 2) for v in d])
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)

tin = {9: dict(type="cut", frames=0), 10: dict(type="cut", frames=0), 16: dict(type="cut", frames=0), 17: dict(type="cut", frames=0)}[SHOT]
meta = {"take": "s%02d" % SHOT, "film": 20, "shots": [SHOT], "g0": G0, "g1": G1 + 1, "first_g": FIRST, "n_frames": N,
        "shot_ranges": {str(SHOT): [G0, G1]}, "handle_in": H, "handle_out": H, "transition_in": tin,
        "transition_out": dict(type="cut", frames=0, at=G1 + 1),
        "set": "v3/set3d20 CAFE preset %s, light DAY, window view %s (hook set_window_view keyed every frame)" % ({9: "cafe_low", 10: "cafe_low_close", 16: "cafe_low", 17: "cafe_low_close"}[SHOT], "stub" if SHOT in (9, 10) else "full"),
        "cast": "v3/cast20 maupassant stage Actor on the standing mark; " + WORDS + "; lip-sync mouth from narration loudness (cast20.talk_mouth + MOUTH_SET open sizes) only inside the quote windows",
        "events": EV, "dof": "none", "text": "none", "light": "DAY", "samples": 8, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "head_px": [round(min(h["w"] for h in heads)), round(max(h["w"] for h in heads))],
        "head_centre_y": [round(min(h["y"] for h in heads)), round(max(h["y"] for h in heads))],
        "head_bottom_max_y": round(max(h["bottom"] for h in heads)),
        "framediff_in_shot": {"median": nb["median"], "p90": nb["p90"]},
        "narration": "film20/audio/narration.wav at +0.10 s"}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)

ev = []


def add(a, b, kind, note, **kw):
    e = dict(kind=kind, t=round(a / 30.0, 3), dur=round(max(0, b - a) / 30.0, 3), frame=a, end_frame=b, note=note)
    e.update(kw)
    ev.append(e)


add(FIRST, LAST + 1, "ambience", "Paris café 1887-89: low murmur of the artists, cutlery and cups, a gas lamp hiss, far street noise through the window")
if SHOT == 9:
    add(612, 634, "foley", "banquette leather creak, chair scrape and a heavy breath as he gets up; shoes on the tiles", peak_frame=624)
    add(640, 658, "foley", "two quick tugs at the cravat: cloth rustle", peak_frame=645)
    add(657, 672, "accent", "snap push: short rising whoosh", peak_frame=664)
    add(654, 668, "accent", "chin-up smug pose: a pompous low brass 'pah'", peak_frame=660)
elif SHOT == 10:
    add(676, 712, "foley", "he turns on his heel, frock coat swish, arms crossed creak", peak_frame=700)
    add(729, 744, "accent", "snap push on the last words: whoosh + a muffled gasp from the artists", peak_frame=736)
    add(700, 750, "crowd", "artists murmur and nod behind him, a chair creak", peak_frame=720)
elif SHOT == 16:
    add(1090, 1110, "accent", "crash pull-out: fast whoosh falling", peak_frame=1098)
    add(1093, 1142, "voice_fx", "belly laugh bounce (his own laugh: the narration voice carries the words; add a light 'ha ha' under it)", peak_frame=1110)
    add(1117, 1142, "accent", "tower reveal in the window: a tiny sting", peak_frame=1117)
else:
    add(1143, 1220, "voice_fx", "laughing breaths under the quote (mouth follows the narration)", peak_frame=1160)
    add(1192, 1207, "accent", "snap push on 'เศษเหล็ก': whoosh + crumpling paper / scrap-metal clang on the mime", peak_frame=1198)
    add(1195, 1203, "foley", "crumple mime: fist squeeze, cloth creak", peak_frame=1198)
add(G1 + 1, G1 + 1, "cut", "hard cut out")
json.dump(dict(take="s%02d" % SHOT, fps=30, note="t = film seconds (g / 30)", cues=ev), open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
contact(pngs, os.path.join(HERE, "contact.jpg"))
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
if os.path.getsize(mkv) > 45e6:
    subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True, cwd=HERE)
    print("take.mkv split into parts")
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(FIRST), "--cuts", "%d,%d" % (G0, G1 + 1)], capture_output=True, text=True)
print(r.stdout, r.stderr[-500:])
print("delivered %d frames, %.1f MB; s/frame wall %.2f cpu %.2f; frame-diff median %.2f p90 %.2f" % (N, os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"]))

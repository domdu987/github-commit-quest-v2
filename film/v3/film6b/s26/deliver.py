#!/usr/bin/env python3
"""deliver.py -- take s26 (film 6b shots 26-28): raw/s26 + raw/s28 -> frames/g_%04d.png (g 1452..1709), meta.json, cues.json,
contact.jpg (caption line y 880 drawn), compare.jpg (beside reference sheets), hue rows, take.mkv (libx264rgb crf 6).
    python3 deliver.py"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.normpath(os.path.join(HERE, "..", ".."))
PROJ = os.path.dirname(V3)
sys.path.insert(0, os.path.join(V3, "tools"))

TAKE, FIRST, LAST = "s26", 1452, 1709
G0, G1 = 1458, 1704                                  # plan range [g0, g1)
SRC = [(26, 1452, 1592), (28, 1593, 1709)]
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)

src, rows = {}, []
for sid, a, b in SRC:
    for g in range(a, b + 1):
        p = os.path.join(HERE, "raw", "s%d" % sid, "g_%04d.png" % g)
        if not os.path.exists(p):
            raise SystemExit("missing %s" % p)
        shutil.copyfile(p, os.path.join(OUT, "g_%04d.png" % g)); src[g] = sid
        rows.append(json.load(open(p[:-4] + ".json")))
N = LAST - FIRST + 1
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
w26 = [m["wall"] for m in rows if m["shot"] == 26]; w28 = [m["wall"] for m in rows if m["shot"] == 28]

meta = {"take": TAKE, "film": "6b", "shots": [26, 27, 28], "g0": G0, "g1": G1, "first_g": FIRST, "n_frames": N,
        "handle_in": G0 - FIRST, "handle_out": LAST - G1 + 1,
        "transition_in": {"type": "cut", "frames": 0}, "transition_out": {"type": "cut", "frames": 0},
        "shot_ranges": {"26": [1458, 1553], "27": [1554, 1592], "28": [1593, 1703]},
        "framings": {"26a": [1452, 1485], "26b": [1486, 1530], "26c": [1531, 1553], "27": [1554, 1592], "28a": [1593, 1648],
                     "28b": [1649, 1709]},
        "events": {"not_smoke_label": 1463, "water_label": 1489, "evaporate_label": 1535, "beam_rises": [1558, 1588],
                   "tag_500_to_480": 1574, "loaf13_lands": 1606, "plus1_badge": 1610, "scale_level": [1606, 1630]},
        "set": "diagram (shots 26-27): own scene, emission cards only on a cool-blue blueprint backdrop (no set); shot 28: v3/set3d6 bakery MORNING, hand balance (set_scale), steam 0.30",
        "dof": "none (client rule)", "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "narration": "film6b/audio/narration.wav at +0.10 s; captions film6b/script/captions.json",
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "s_per_frame_wall_diagram": round(float(np.mean(w26)), 2), "s_per_frame_wall_bakery": round(float(np.mean(w28)), 2),
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label)
    e.update(kw); ev.append(e)


add(FIRST, 1592, "diagram: soft airy 'science' pad, light bubbly plinks as the drops leave the crumb", "ambience")
add(1463, 1468, "red X stamped on the 'ควัน' label: rubber-stamp thunk", "accent", peak_frame=1463)
add(1489, 1494, "'น้ำ' label pops in: bubble pop", "accent", peak_frame=1489)
add(1532, 1553, "drops race out of the crust: rising string of pops / whoosh up into the steam", "fx", peak_frame=1535)
add(1554, 1592, "pull back to the balance: the beam creaks as the loaf pan rises", "prop", peak_frame=1570)
add(1574, 1578, "tag flips 500 -> 480: card flip 'flick' + low 'bwomp'", "accent", peak_frame=1574)
add(1593, 1709, "bakery morning: oven crackle, street murmur", "ambience")
add(1597, 1606, "the pale 13th loaf drops into the basket: soft crusty thump + wicker creak", "prop", peak_frame=1606)
add(1606, 1630, "the balance swings and settles level: brass ting", "prop", peak_frame=1610)
add(1610, 1615, "'+1' badge pops: bright ding", "accent", peak_frame=1610)
add(1649, 1709, "tiny drops rising off the basket: faint plinks", "fx")
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration film6b/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)

# contact sheet: 24 frames, caption line y 880
gs = [int(round(FIRST + i * (N - 1) / 23.0)) for i in range(24)]
w, h, lab, cols = 240, 427, 18, 8
S = Image.new("RGB", (cols * w, 3 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    yl = y + lab + int(h * 880 / 1280.0); dr.line([(x, yl), (x + w, yl)], fill=(255, 40, 40))
    fr = [k for k, (a, b) in meta["framings"].items() if a <= g <= b][0]
    dr.text((x + 4, y + 3), "g %d %.2fs %s%s" % (g, g / 30.0, fr, " h" if (g < G0 or g >= G1) else ""), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

# compare: diagram + insert beside the director's reference sheets (cutaway / diagram reveal look)
w, h, lab = 300, 533, 20
picks = [(1520, "26b"), (1590, "27"), (1625, "28a")]
refs = [os.path.join(PROJ, "analysis", "sheets", n) for n in ("oil_1.jpg", "rail_1.jpg")]
C = Image.new("RGB", (len(picks) * w + 2 * 360 + 24, 640 + lab), (16, 12, 20)); dr = ImageDraw.Draw(C)
x = 0
for g, fr in picks:
    C.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "%s g %d" % (fr, g), fill=(255, 255, 255)); x += w
x += 24
for r in refs:
    if os.path.exists(r):
        im = Image.open(r).convert("RGB"); im.thumbnail((360, 640))
        C.paste(im, (x, lab)); dr.text((x + 4, 4), "ref " + os.path.basename(r), fill=(255, 220, 160))
    x += 360
C.save(os.path.join(HERE, "compare.jpg"), quality=88)

# hue rows
try:
    import hue_report, io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        for lab_, a, b in (("s26 diagram 26-27", G0, 1592), ("s26 bakery 28", 1593, G1 - 1)):
            hue_report.row(lab_, [os.path.join(OUT, "g_%04d.png" % g) for g in range(a, b + 1, 3)])
    print(buf.getvalue())
    open(os.path.join(HERE, "work", "hue.txt"), "w").write(buf.getvalue())
except Exception as e:  # noqa
    print("hue report skipped:", e)

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-frames:v", str(N), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
print("delivered %d frames g %d..%d + take.mkv (%.1f MB); mean wall %.2f s, cpu %.2f s" %
      (N, FIRST, LAST, os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus)))

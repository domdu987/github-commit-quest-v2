#!/usr/bin/env python3
"""deliver.py -- take s29 (film 6b shots 29-31, the end): raw/s29 + raw/s30 + raw/s31 -> frames/g_%04d.png (g 1698..1940), meta.json, cues.json,
contact.jpg (caption line y 880 drawn), compare.jpg (beside reference sheets), hue rows, take.mkv (libx264rgb crf 6).
    python3 deliver.py"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.normpath(os.path.join(HERE, "..", ".."))
PROJ = os.path.dirname(V3)
sys.path.insert(0, os.path.join(V3, "tools"))

TAKE, FIRST, LAST = "s29", 1698, 1940
G0, G1 = 1704, 1941                                  # plan range [g0, g1)
SRC = [(29, 1698, 1790), (30, 1791, 1871), (31, 1872, 1940)]
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


meta = {"take": TAKE, "film": "6b", "shots": [29, 30, 31], "g0": G0, "g1": G1, "first_g": FIRST, "n_frames": N,
        "handle_in": G0 - FIRST, "handle_out": 0,
        "transition_in": {"type": "cut", "frames": 0}, "transition_out": {"type": "end", "frames": 0, "note": "film ends on g 1940 (hard cut, no hold, no fade)"},
        "shot_ranges": {"29": [1704, 1790], "30": [1791, 1871], "31": [1872, 1940]},
        "framings": {"29a": [1698, 1747], "29b": [1748, 1790], "30a": [1791, 1830], "30b": [1831, 1871], "31": [1872, 1940]},
        "events": {"kit_looks_up_then_lens": [1748, 1768], "loaf_hop": 1776, "henry_gulp": 1868, "tomatoes_raised": [1833, 1871],
                   "first_tomato_flies": [1877, 1882], "first_splat": 1883,
                   "hits": [1883, 1890, 1896, 1901, 1906, 1910, 1914, 1918, 1921, 1924, 1927, 1930], "counter_12": 1930, "last_frame": 1940},
        "set": "v3/set3d6 market MORNING; the set's 3D pillory board/post cut out at runtime (Henry carries the cast6 drawn pillory); hanging sign card over Henry's shop front (x -21.15)",
        "dof": "none (client rule)", "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "narration": "film6b/audio/narration.wav at +0.10 s; captions film6b/script/captions.json",
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label)
    e.update(kw); ev.append(e)


add(FIRST, 1790, "market morning: birds, distant chatter; the sign creaks on its rings", "ambience")
add(1748, 1790, "kit grins at us holding up a loaf: cheeky sting", "accent", peak_frame=1770)
add(1791, 1871, "market crowd jeering, murmur rising", "ambience")
add(1866, 1872, "henry gulps (cartoon gulp)", "accent", peak_frame=1868)
add(1877, 1883, "first tomato whoosh", "fx", peak_frame=1880)
add(1883, 1886, "SPLAT (big wet cartoon splat) on 'มะเขือเทศ'", "fx", peak_frame=1883)
for i, h_ in enumerate([1890, 1896, 1901, 1906, 1910, 1914, 1918, 1921, 1924, 1927, 1930]):
    add(h_, h_ + 2, "splat %d + counter tick" % (i + 2), "fx", peak_frame=h_)
add(1930, 1940, "'12' counter: final ding; crowd cheer; HARD CUT at g 1940 (end of film)", "accent", peak_frame=1930)
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
picks = [(1745, "29a"), (1850, "30b"), (1935, "31")]
refs = [os.path.join(PROJ, "analysis", "sheets", n) for n in ("rail_0.jpg", "pink_1.jpg")]
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
        for lab_, a, b in (("s29 shot 29", G0, 1790), ("s29 shots 30-31", 1791, 1940)):
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

#!/usr/bin/env python3
"""deliver.py -- (identical in s13 / s14 / s16; the take is chosen by the folder name) from raw/s<shot>/ build
frames/g_%04d.png, meta.json, cues.json, contact.jpg, compare.jpg, take.mkv and work/qa.txt (numbers for QA.md).
    python3 deliver.py [noenc]"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(PROJ, "v3", "tools"))
import hue_report as H
TAKE = os.path.basename(HERE)
t = lambda g: round(g / 30.0, 3)

CFG = {
    "s13": dict(shots=[13], first=1048, last=1186, g0=1055, g1=1180, ranges={13: (1048, 1186)}, light="SUNSET",
                transition_in=dict(type="dissolve", frames=10, note="handle g 1048..1054 rendered in 3D (shot 13 camera before its start)"),
                transition_out=dict(type="dissolve", frames=10, note="SUNSET -> NIGHT; handle g 1180..1186 rendered in 3D (camera keeps drifting)"),
                cast="v3/cast4: master (left, nearer; pat pinned to kenta's shoulder), kenta (worried)",
                dof={"13": "g 1048-1094 master card f 3.5; g 1095-1134 master card f 3.0; g 1135- kenta card f 3.0"},
                pairs=[(13, 1070, 55), (13, 1110, 57), (13, 1160, 59)], sway=0.0,
                cuts=[]),
    "s14": dict(shots=[14, 15], first=1173, last=1438, g0=1180, g1=1432, ranges={14: (1173, 1261), 15: (1262, 1438)}, light="NIGHT",
                transition_in=dict(type="dissolve", frames=10, note="SUNSET -> NIGHT; handle g 1173..1179 rendered in 3D (shot 14 camera before its start)"),
                transition_out=dict(type="cut", frames=0, note="handle g 1432..1438 rendered in 3D anyway (shot 15 c2 continues) in case the conform dissolves"),
                cast="v3/cast4: kenta (15 a/b), merchant (15 b background, 15 c mocking, quoted line), woman2 (15 b background, laughing)",
                dof={"14": "A off; B (g 1222-) point (-3.8, -46, 2.4) f 2.5", "15": "a/b kenta card f 3.0; c merchant head point f 3.5"},
                pairs=[(14, 1195, 67), (14, 1240, 71), (15, 1285, 75), (15, 1325, 79), (15, 1365, 83), (15, 1410, 87)], sway="0 -> 1.0 x quake (1.1 Hz)",
                cuts=[1222, 1262, 1303, 1345, 1387]),
    "s16": dict(shots=[16], first=1425, last=1528, g0=1432, g1=1522, ranges={16: (1425, 1528)}, light="NIGHT",
                transition_in=dict(type="cut", frames=0, note="handle g 1425..1431 rendered in 3D anyway (shot 16 camera before its start)"),
                transition_out=dict(type="dissolve", frames=10, note="handle g 1522..1528 rendered in 3D (dust column keeps rising)"),
                cast="none (no people)", dof={"16": "off"},
                pairs=[(16, 1455, 93), (16, 1490, 95), (16, 1515, 97)], sway=1.15,
                cuts=[]),
}[TAKE]


def raw(s, g):
    return os.path.join(HERE, "raw", "s%d" % s, "g_%04d.png" % g)


def shot_of(g):
    for s, (a, b) in CFG["ranges"].items():
        if a <= g <= b:
            return s


OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
src = {}
for g in range(CFG["first"], CFG["last"] + 1):
    s = shot_of(g)
    shutil.copyfile(raw(s, g), os.path.join(OUT, "g_%04d.png" % g)); src[g] = "s%d" % s
rows = {}
for s in CFG["shots"]:
    for js in glob.glob(os.path.join(HERE, "raw", "s%d" % s, "g_*.json")):
        m = json.load(open(js)); rows[(s, m["g"])] = m
walls = [m["wall"] for m in rows.values()]; cpus = [m["cpu"] for m in rows.values()]
n = CFG["last"] - CFG["first"] + 1
meta = {"take": TAKE, "shots": CFG["shots"], "first_g": CFG["first"], "n_frames": n, "g0": CFG["g0"], "g1": CFG["g1"],
        "handle_in": CFG["g0"] - CFG["first"], "handle_out": CFG["last"] + 1 - CFG["g1"],
        "transition_in": CFG["transition_in"], "transition_out": CFG["transition_out"],
        "shot_ranges": {str(s): [max(a, CFG["g0"]), min(b, CFG["g1"] - 1)] for s, (a, b) in CFG["ranges"].items()},
        "render_ranges": {str(s): list(r) for s, r in CFG["ranges"].items()},
        "internal_cuts": CFG["cuts"],
        "set": "v3/set3d4/pagoda.py v2 (nothing added; set controls keyed per frame from shot.py)", "light": CFG["light"],
        "cast": CFG["cast"], "dof": CFG["dof"], "sway": CFG["sway"],
        "narration": "film4/audio/narration_bankky.wav (+0.10 s), captions film4/script/captions_bankky.json",
        "samples": 12, "resolution": [720, 1280], "threads": 2,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "encode": "ffmpeg -framerate 30 -start_number %d -i frames/g_%%04d.png -c:v libx264rgb -crf 6 -preset slow take.mkv" % CFG["first"]}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)


if TAKE == "s13":
    add(1048, 1187, "sunset street in front of the gate: evening wind, distant crows, a temple bell far off, low murmur of the street", "ambience")
    add(1066, 1072, "the master's heavy coat sleeve swings as he reaches for kenta (cloth rustle)", "gesture")
    for g in (1077, 1091, 1104):
        add(g, g + 2, "pat: the master's big hand claps kenta's shoulder (soft thump)", "impact", peak_frame=g)
    add(1090, 1182, "the master speaks the quote (voice is the narration; mouth lip-synced to narration_bankky.wav)", "dialogue")
    add(1092, 1099, "snap punch-in on the master (short whoosh)", "camera_snap", peak_frame=1096)
    add(1131, 1139, "snap to the two-shot on kenta (short whoosh)", "camera_snap", peak_frame=1135)
    add(1150, 1172, "kenta's worried glance toward the pagoda (small nervous swallow)", "gesture")
elif TAKE == "s14":
    add(1173, 1222, "night town from above: crickets, wind, a dog far off", "ambience")
    add(1200, 1262, "deep rumble of the earthquake rising to a roar; wooden houses creak", "quake", peak_frame=1222)
    add(1205, 1262, "lanterns and wind bells swing and rattle, the pagoda's bells jangle", "rattle")
    add(1222, 1222, "hard cut to the street, low: rumble loud", "cut")
    add(1226, 1262, "loose roof tiles clatter and hop on the eaves", "rattle")
    add(1262, 1262, "hard cut: kenta sprinting", "cut")
    add(1262, 1438, "continuous quake rumble under everything (a little lower than the peak)", "quake")
    for g in range(1262, 1303, 5):
        add(g, g + 1, "running footsteps (straw sandals on packed earth)", "footstep")
    add(1262, 1345, "kenta shouting (his voice is the narration; his mouth is a fixed shout drawing)", "voice")
    add(1303, 1303, "hard cut: kenta stops and shouts at the doorways", "cut")
    add(1303, 1345, "woman in the street laughing (background)", "voice")
    add(1345, 1345, "hard cut: low angle on the merchant in his doorway", "cut")
    add(1374, 1381, "the merchant cups his hands to his mouth (sleeve swish)", "gesture")
    add(1383, 1435, "the merchant mock-shouts the quote (voice is the narration; mouth lip-synced)", "dialogue")
    add(1387, 1393, "snap closer, lower on the merchant (whoosh)", "camera_snap", peak_frame=1390)
else:
    add(1425, 1529, "strongest quake: deep roar, lanterns and bells rattling, the pagoda creaking as it sways", "quake")
    add(1452, 1456, "the plastered joint splits: sharp crack, plaster crumbles", "crack", peak_frame=1452)
    add(1466, 1472, "snap punch-in toward the break (whoosh)", "camera_snap", peak_frame=1469)
    add(1474, 1478, "the tower snaps in the middle like a ruler: huge timber crack", "snap", peak_frame=1476)
    add(1478, 1500, "the top half topples: groaning timber, a rising whoosh", "fall")
    add(1500, 1512, "the top half slams into the courtyard: massive crash, debris rain, camera jolt", "impact", peak_frame=1500)
    add(1498, 1506, "snap pull-back (whoosh) with the dust", "camera_snap", peak_frame=1502)
    add(1500, 1529, "dust column billowing up, small debris pattering down", "dust")
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration film4/audio/narration_bankky.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)

# contact sheet: 16 evenly spaced final frames, labels above the picture
gs = [CFG["first"] + int(round(i * (n - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.text((x + 4, y + 3), "g %d  %.2f s  shot %s" % (g, g / 30.0, src[g][1:]), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

w, h, lab = 360, 640, 20
P = CFG["pairs"]
C = Image.new("RGB", (len(P) * 2 * w + (len(P) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(C)
x = 0
for shot, g, tref in P:
    C.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "shot %d  g %d (%.2f s)" % (shot, g, g / 30.0), fill=(255, 255, 255))
    C.paste(Image.open(os.path.join(PROJ, "ref", "a", "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), "ref a t%04d (%d s)" % (tref, (tref - 1) // 2), fill=(255, 220, 160))
    x += 2 * w + 12
C.save(os.path.join(HERE, "compare.jpg"), quality=88)

# QA numbers -> work/qa.txt
os.makedirs(os.path.join(HERE, "work"), exist_ok=True)
qa = open(os.path.join(HERE, "work", "qa.txt"), "w")
_print = print


def print(*a):
    _print(*a); _print(*a, file=qa)


for s, (a, b) in CFG["ranges"].items():
    rr = sorted([m for (ss, g), m in rows.items() if ss == s], key=lambda m: m["g"])
    print("shot %d (render g %d..%d, %d frames)" % (s, a, b, len(rr)))
    for nm in sorted({k for r in rr for k in r["heads"]}):
        hs = [(r["g"], r["heads"][nm]) for r in rr if nm in r["heads"]]
        ww = [x["w"] for _, x in hs]; yy = [x["y"] for _, x in hs]; xx = [x["x"] for _, x in hs]
        low = [g for g, x in hs if x["y"] + x["w"] / 2 > 880]
        print("  %-8s g %d..%d head w %4.0f..%4.0f px, centre x %4.0f..%4.0f, y %4.0f..%4.0f (%.2f..%.2f H); bottom below 880: %s"
              % (nm, hs[0][0], hs[-1][0], min(ww), max(ww), min(xx), max(xx), min(yy), max(yy), min(yy) / 1280, max(yy) / 1280, (low[0], low[-1], len(low)) if low else "none"))
    print("  render: wall %.2f s, cpu %.2f s per frame (mean); retried %s" % (np.mean([r["wall"] for r in rr]), np.mean([r["cpu"] for r in rr]), [r["g"] for r in rr if r.get("retried")]))
fs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(CFG["first"], CFG["last"] + 1)]
prev = None; d = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
    if prev is not None:
        d.append(float(np.abs(a - prev).mean()))
    prev = a
pops = []
for i, v in enumerate(d):
    p = d[i - 1] if i else v; nx = d[i + 1] if i + 1 < len(d) else v
    if v > 1.8 * p and v > 1.8 * nx and v > 1.0:
        pops.append((CFG["first"] + i, CFG["first"] + i + 1, round(v, 1)))
print("popcheck (g -> g+1, change):", pops, " internal cuts at", CFG["cuts"])
still = [CFG["first"] + i for i, v in enumerate(d) if v < 0.35]
runs = []
for g in still:
    if runs and g == runs[-1][1] + 1:
        runs[-1][1] = g
    else:
        runs.append([g, g])
print("near-still transitions (< 0.35 levels):", len(still), "longest runs:", sorted(runs, key=lambda r: r[0] - r[1])[:5])
print("frame change median (levels):", round(float(np.median(d)), 2))
bad = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
    mag = ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean(); blk = (a.max(axis=2) < 6).mean()
    if mag > 0.002 or blk > 0.2:
        bad.append(os.path.basename(f))
print("magenta / black frames:", bad)
print()
print(f"{'set':44s} " + " ".join(f"{nn[:6]:>6s}" for nn in H.NAMES) + "   sat  val dark")
import io, contextlib
for s, (a, b) in CFG["ranges"].items():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        H.row("%s shot %d (g %d-%d)" % (TAKE, s, a, b), [os.path.join(OUT, "g_%04d.png" % g) for g in range(a, b + 1)])
    print(buf.getvalue().rstrip())
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    H.row("ref a " + " ".join("t%04d" % p[2] for p in P), [os.path.join(PROJ, "ref", "a", "t%04d.jpg" % p[2]) for p in P])
print(buf.getvalue().rstrip())
qa.close()

if "noenc" not in sys.argv:
    mkv = os.path.join(HERE, "take.mkv")
    if os.path.exists(mkv):
        os.remove(mkv)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "30", "-start_number", str(CFG["first"]), "-i", os.path.join(OUT, "g_%04d.png"),
                    "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
    nf = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames",
                         "-of", "csv=p=0", mkv], capture_output=True, text=True).stdout.strip()
    _print("take.mkv frames:", nf, "expected", n)
_print("delivered", len(src), "frames; mean wall %.2f s, cpu %.2f s" % (np.mean(walls), np.mean(cpus)))

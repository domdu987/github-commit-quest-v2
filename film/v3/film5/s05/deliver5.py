#!/usr/bin/env python3
"""deliver5.py -- from raw/s<sid>/g_*.png build frames/g_%04d.png, take.mkv, meta.json, cues.json, contact.jpg, compare.jpg and
work/qa.txt (head sizes / positions, heads below y 880, pops, black / magenta frames, hue rows, s per frame).
Uses the take's shot.py (S.RANGES, S.SUB, S.CUES, S.PAIRS, S.TRANS_IN, S.TRANS_OUT, S.SHOT).  python3 deliver5.py"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from shot import S                                       # noqa: E402
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(PROJ, "v3", "tools"))
import hue_report as H                                   # noqa: E402

RAW = os.path.join(HERE, "raw"); OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(HERE, "work"), exist_ok=True)
first = min(a for a, b in S.RANGES.values()); last = max(b for a, b in S.RANGES.values())
src = {}
for g in range(first, last + 1):
    sid = [s for s, (a, b) in S.RANGES.items() if a <= g <= b][0]
    shutil.copyfile(os.path.join(RAW, "s%d" % sid, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    src[g] = S.SUB[sid]
N = last - first + 1

mkv = os.path.join(HERE, "take.mkv")
if os.path.exists(mkv):
    os.remove(mkv)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "30", "-start_number", str(first), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)

rows = {}
for sid in S.RANGES:
    for js in glob.glob(os.path.join(RAW, "s%d" % sid, "g_*.json")):
        m = json.load(open(js))
        if S.RANGES[sid][0] <= m["g"] <= S.RANGES[sid][1]:
            rows[(sid, m["g"])] = m
walls = [m["wall"] for m in rows.values()]; cpus = [m["cpu"] for m in rows.values()]

trans = [dict(at=first, type="in", **S.TRANS_IN)]
sids = sorted(S.RANGES)
for a, b in zip(sids[:-1], sids[1:]):
    trans.append(dict(at=S.RANGES[b][0], type="cut", from_shot=S.SUB[a], to_shot=S.SUB[b]))
trans.append(dict(at=S.G1, type="out", handle=[S.G1, last], **S.TRANS_OUT))
meta = {"take": S.NAME, "film": 5, "shots": [S.SHOT], "first_g": first, "n_frames": N, "g0": S.G0, "g1": S.G1,
        "handle_in": S.G0 - first, "handle_out": last + 1 - S.G1,
        "transition_in": S.TRANS_IN, "transition_out": S.TRANS_OUT, "transitions": trans,
        "shot_ranges": dict([(str(S.SHOT), [S.G0, S.G1 - 1])] + [(S.SUB[s], [max(S.G0, a), min(S.G1 - 1, b)]) for s, (a, b) in S.RANGES.items()]),
        "set": "v3/set3d5/mine.py: tunnel LAMP; the set's 3D canary cage hidden (alfie carries the cast5 2D held cage, bird inside the bars)",
        "dof": "none (client rule: M.setup_dof(scene, None, None, cam) at build and before every render)",
        "denoiser": "OpenImageDenoise, albedo+normal, prefilter FAST (M.setup_render)",
        "narration": "film5/audio/narration_bankky.wav at +0.10 s; captions film5/script/captions.json",
        "light": "LAMP", "cast": S.CAST_NOTE, "samples": 12, "resolution": [720, 1280], "threads": 2,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []
for c in S.CUES:
    g0, g1, label, kind = c[:4]
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label)
    if len(c) > 4:
        e.update(c[4])
    ev.append(e)
json.dump(dict(take=S.NAME, fps=30, note="time = film seconds (g / 30); narration PROJ/film5/audio/narration_bankky.wav at +0.10 s, captions.json",
               cues=ev), open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = [int(round(first + i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
C = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(C)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    C.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.text((x + 4, y + 3), "g %d  %.2f s  shot %s" % (g, g / 30.0, src[g]), fill=(255, 255, 255))
C.save(os.path.join(HERE, "contact.jpg"), quality=88)

w, h, lab = 360, 640, 20
C = Image.new("RGB", (len(S.PAIRS) * 2 * w + (len(S.PAIRS) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(C)
x = 0
for name, g, tref in S.PAIRS:
    C.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "shot %s  g %d (%.2f s)" % (name, g, g / 30.0), fill=(255, 255, 255))
    C.paste(Image.open(os.path.join(PROJ, "ref", "a", "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), "ref a t%04d (%d s)" % (tref, (tref - 1) // 2), fill=(255, 220, 160))
    x += 2 * w + 12
C.save(os.path.join(HERE, "compare.jpg"), quality=88)

# ------------------------------------------------------------------ QA numbers
q = open(os.path.join(HERE, "work", "qa.txt"), "w")
P = lambda *a: (print(*a), print(*a, file=q))
for sid, (a, b) in S.RANGES.items():
    rs = sorted([m for (s, g), m in rows.items() if s == sid], key=lambda m: m["g"])
    P("shot %s (g %d..%d, %d frames): wall %.2f s, cpu %.2f s per frame; retried %s" % (S.SUB[sid], a, b, len(rs),
      np.mean([m["wall"] for m in rs]), np.mean([m["cpu"] for m in rs]), [m["g"] for m in rs if m.get("retried")]))
    for n in sorted({n for m in rs for n in m["heads"]}):
        hs = [(m["g"], m["heads"][n]) for m in rs if n in m["heads"]]
        wv = [v["w"] for _, v in hs]; yv = [v["y"] for _, v in hs]; xv = [v["x"] for _, v in hs]
        low = [g for g, v in hs if v["y"] + v["w"] / 2 > 880 and -v["w"] / 2 < v["x"] < 720 + v["w"] / 2]
        mouths = sorted({v.get("mouth") for _, v in hs})
        P("  %-7s head w %4.0f..%4.0f px, x %4.0f..%4.0f, y %4.0f..%4.0f (%.2f..%.2f H); below 880: %s; mouths %s"
          % (n, min(wv), max(wv), min(xv), max(xv), min(yv), max(yv), min(yv) / 1280, max(yv) / 1280,
             (low[0], low[-1], len(low)) if low else "none", mouths))
fs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(first, last + 1)]
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
        pops.append((first + i, first + i + 1, round(v, 1)))
P("popcheck (g -> g+1, change):", pops, " cuts at", [S.RANGES[s][0] for s in sids[1:]])
still = []; run = 0
for i, v in enumerate(d):
    run = run + 1 if v < 0.15 else 0
    if run > 6:
        still.append(first + i)
P("static runs > 6 frames (change < 0.15):", still)
bad = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
    if ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean() > 0.002 or (a.max(axis=2) < 6).mean() > 0.2:
        bad.append(os.path.basename(f))
P("magenta / black frames:", bad)
P("mean s/frame: wall %.2f, cpu %.2f" % (np.mean(walls), np.mean(cpus)))
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
    for sid, (a, b) in S.RANGES.items():
        H.row("%s shot %s (g %d-%d)" % (S.NAME, S.SUB[sid], a, b), fs[a - first:b - first + 1])
    H.row("%s all (g %d-%d)" % (S.NAME, first, last), fs)
    H.row("ref a " + " ".join("t%04d" % p[2] for p in S.PAIRS), [os.path.join(PROJ, "ref", "a", "t%04d.jpg" % p[2]) for p in S.PAIRS])
P(buf.getvalue())
q.close()
print("delivered", N, "frames g %d..%d" % (first, last))

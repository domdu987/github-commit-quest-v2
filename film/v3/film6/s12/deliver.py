#!/usr/bin/env python3
"""deliver.py -- from raw/s<sid>/ build frames/g_%04d.png, meta.json, cues.json, contact.jpg, compare.jpg, take.mkv and the QA numbers
work/qa.txt (heads, caption band, pops, black / magenta frames, hue rows, s per frame).  The per-take settings are in take_cfg.py.
    python3 deliver.py"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import take_cfg as K                     # noqa: E402
import hue_report as HR                  # noqa: E402

OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(HERE, "work"), exist_ok=True)
G_FIRST, G_LAST = K.G_FIRST, K.G_LAST
src, rows = {}, []
for g in range(G_FIRST, G_LAST + 1):
    sid = [s for s, (a, b) in K.SIDS.items() if a <= g <= b][0]
    p = os.path.join(HERE, "raw", "s%d" % sid, "g_%04d.png" % g)
    shutil.copyfile(p, os.path.join(OUT, "g_%04d.png" % g)); src[g] = "sid%d" % sid
    m = json.load(open(p[:-4] + ".json")); m["sid"] = sid; rows.append(m)
N = G_LAST - G_FIRST + 1
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]

meta = dict(take=K.TAKE, film=6, shots=K.SHOTS, first_g=G_FIRST, n_frames=N, g0=K.G0, g1=K.G1, handle_in=K.G0 - G_FIRST,
            handle_out=G_LAST + 1 - K.G1, transition_in=K.TRANSITION_IN, transition_out=K.TRANSITION_OUT,
            shot_ranges={str(k): v for k, v in K.SHOT_RANGES.items()},
            framings={"sid%d" % s: dict(g=list(r), note=K.SID_NOTES[s]) for s, r in K.SIDS.items()},
            events=K.EVENTS, set=K.SET, dof="none (client rule: cam.data.dof.use_dof False + B.setup_dof(scene, None, None, cam=cam) at build and before every render)",
            sky="the set's sky dome texture (blurred SVG clouds, 11 px/deg) is replaced at runtime by the same sky redrawn without the blur at 34 px/deg (mk.sharp_sky)",
            denoiser="OpenImageDenoise, albedo+normal, prefilter FAST",
            narration="film6/audio/narration_bankky.wav at +0.10 s; captions film6/script/captions.json",
            cast=K.CAST, samples=12, resolution=[720, 1280], threads=2, fps=30,
            s_per_frame_wall_mean=round(float(np.mean(walls)), 2), s_per_frame_cpu_mean=round(float(np.mean(cpus)), 2),
            frame_source={str(g): v for g, v in src.items()})
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

ev = []
for (g0, g1, label, kind, peak) in K.CUES:
    e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label)
    if peak is not None:
        e["peak_frame"] = peak
    ev.append(e)
json.dump(dict(take=K.TAKE, fps=30, note="time = film seconds (g / 30); narration PROJ/film6/audio/narration_bankky.wav at +0.10 s, captions.json", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)

# contact sheet: 16 frames (or 24 for long takes)
nct = 16 if N < 150 else 24
gs = [G_FIRST + int(round(i * (N - 1) / float(nct - 1))) for i in range(nct)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, (nct // cols) * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    sh = [k for k, (a, b) in K.SHOT_RANGES.items() if a <= g <= b]
    dr.text((x + 4, y + 3), "g %d %.2fs %s %s" % (g, g / 30.0, src[g], ("shot %s" % sh[0]) if sh else "handle"), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

w, h, lab = 360, 640, 20
C = Image.new("RGB", (len(K.COMPARE) * 2 * w + (len(K.COMPARE) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(C)
x = 0
for g, ref, txt in K.COMPARE:
    C.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "%s g %d (%.2f s)" % (K.TAKE, g, g / 30.0), fill=(255, 255, 255))
    C.paste(Image.open(os.path.join(PROJ, "ref", ref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), "ref %s %s" % (ref, txt), fill=(255, 220, 160))
    x += 2 * w + 12
C.save(os.path.join(HERE, "compare.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(G_FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)

# ---------------------------------------------------------------- QA numbers
q = []
q.append("%s: g %d..%d (%d frames), shots %s" % (K.TAKE, G_FIRST, G_LAST, N, K.SHOTS))
for s, (a, b) in K.SIDS.items():
    rs = [r for r in rows if r["sid"] == s]
    q.append("sid %d g %d..%d  lens %s  wall %.1f s cpu %.1f s" % (s, a, b, rs[0].get("lens"), np.mean([r["wall"] for r in rs]), np.mean([r["cpu"] for r in rs])))
    for n in sorted({n for r in rs for n in r["heads"]}):
        hs = [(r["g"], r["heads"][n]) for r in rs if n in r["heads"]]
        inf = [(g, hh) for g, hh in hs if -hh["w"] / 2 < hh["x"] < 720 + hh["w"] / 2]
        if not inf:
            continue
        ws = [hh["w"] for g, hh in inf]; ys = [hh["y"] for g, hh in inf]
        low = [g for g, hh in inf if hh["y"] + hh["w"] / 2 > 880]
        q.append("   %-8s head w %4.0f..%4.0f px  centre y %4.0f..%4.0f (%.2f..%.2f H)  head bottom below 880: %s"
                 % (n, min(ws), max(ws), min(ys), max(ys), min(ys) / 1280, max(ys) / 1280, (low[0], low[-1], len(low)) if low else "none"))
fs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(G_FIRST, G_LAST + 1)]
prev = None; d = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
    if prev is not None:
        d.append(float(np.abs(a - prev).mean()))
    prev = a
cuts = sorted(b + 1 for s, (a, b) in K.SIDS.items() if b < G_LAST)
pops = []
for i, v in enumerate(d):
    p = d[i - 1] if i else v; n = d[i + 1] if i + 1 < len(d) else v
    if v > 1.8 * p and v > 1.8 * n and v > 1.0 and (G_FIRST + i + 1) not in cuts:
        pops.append((G_FIRST + i, G_FIRST + i + 1, round(v, 1)))
q.append("cuts inside the take (framing changes) at g %s" % cuts)
q.append("popcheck (excluding the cuts): %s" % pops)
q.append("near-still transitions (< 0.35 levels): %s" % [G_FIRST + i for i, v in enumerate(d) if v < 0.35])
q.append("frame change median %.2f, max %.2f levels" % (float(np.median(d)), max(d)))
bad = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
    if ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean() > 0.002 or (a.max(axis=2) < 6).mean() > 0.2:
        bad.append(os.path.basename(f))
q.append("magenta / black frames: %s;  retried frames: %s" % (bad, [r["g"] for r in rows if r.get("retried")]))
open(os.path.join(HERE, "work", "qa.txt"), "w").write("\n".join(q) + "\n")
print("\n".join(q))
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in HR.NAMES) + "   sat  val dark")
    for lab_, a, b in K.HUE_ROWS:
        HR.row(lab_, [os.path.join(OUT, "g_%04d.png" % g) for g in range(a, b + 1)])
    for lab_, refs in K.HUE_REFS:
        HR.row(lab_, [os.path.join(PROJ, "ref", r) for r in refs])
open(os.path.join(HERE, "work", "qa.txt"), "a").write(buf.getvalue())
print(buf.getvalue())
print("delivered %d frames + take.mkv; mean wall %.2f s, cpu %.2f s" % (N, np.mean(walls), np.mean(cpus)))

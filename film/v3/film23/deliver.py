#!/usr/bin/env python3
"""deliver.py <sNN>: after `shot.py final`: take.mkv (libx264rgb crf 6), qa_auto, qa_jitter, frame-diff + hue + head numbers, contact.jpg (6 fps),
meta.json, cues.json, QA.md.  Run from anywhere:  python3 deliver.py s02"""
import os, sys, json, math, subprocess, importlib.util, glob
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(os.path.dirname(HERE))
take = sys.argv[1]; D = os.path.join(HERE, take)
spec = importlib.util.spec_from_file_location("shotmod", os.path.join(D, "shot.py")); m = importlib.util.module_from_spec(spec)
sys.path.insert(0, HERE); sys.path.insert(0, D)
spec.loader.exec_module(m); CFG = m.CFG
import c23 as C
clk = C.Clock(CFG)
fr = os.path.join(D, "frames")
gs = list(range(clk.first, clk.last + 1)); miss = [g for g in gs if not os.path.exists(os.path.join(fr, "g_%04d.png" % g))]
assert not miss, "missing frames %s" % miss[:5]
mkv = os.path.join(D, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-start_number", str(clk.first), "-i", os.path.join(fr, "g_%04d.png"), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
size = os.path.getsize(mkv) / 1e6
parts = []
if size > 45:
    subprocess.run("cd %s && split -b 40M -d take.mkv take.mkv.part && rm take.mkv" % D, shell=True, check=True); parts = sorted(glob.glob(os.path.join(D, "take.mkv.part*")))
src = mkv if not parts else None
tmp = None
if src is None:
    tmp = os.path.join("/tmp/claude-0", "take_%s.mkv" % take); subprocess.run("cat %s > %s" % (" ".join(parts), tmp), shell=True, check=True); src = tmp
# QA scripts
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), src, "--first_g", str(clk.first), "--out", D], capture_output=True, text=True)
qa_exit = r.returncode; qa_out = r.stdout[-2500:]
j = subprocess.run([sys.executable, os.path.join(PROJ, "qa_jitter.py"), src], capture_output=True, text=True).stdout.strip()
# frame diff (90x160 grey) inside the shot (g0 .. g1r)
import cv2
cap = cv2.VideoCapture(src); prev = None; diffs = []; k = 0
while True:
    ok, f = cap.read()
    if not ok: break
    g = cv2.cvtColor(cv2.resize(f, (90, 160), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).astype(np.float32)
    if prev is not None and clk.first + k >= clk.g0: diffs.append(float(np.abs(g - prev).mean()))
    prev = g; k += 1
med, p90, mn = float(np.median(diffs)), float(np.percentile(diffs, 90)), float(np.min(diffs))
# hue
sys.path.insert(0, os.path.join(PROJ, "v3", "set3d23")); import ghost_hue as H
mid = (clk.g0 + clk.g1r) // 2; hue = {}
for nm, g in (("first", clk.g0), ("mid", mid), ("last", clk.g1r - 1)):
    h, fr_ = H.shade_hue(os.path.join(fr, "g_%04d.png" % g)); hue[nm] = (g, round(h, 1), round(fr_, 3))
# per-frame reports
walls, heads = [], {}
for g in gs:
    rj = json.load(open(os.path.join(fr, "g_%04d.json" % g))); walls.append(rj["wall"])
    for n, p in rj["heads"].items(): heads.setdefault(n, []).append((g, p["x"], p["y"]))
# contact sheet: every 5th frame (6 fps)
sel = gs[::5][:24]; cols = 8; rows = int(math.ceil(len(sel) / cols)); tw, th = 180, 320
sheet = Image.new("RGB", (cols * tw, rows * th), (20, 20, 20))
for i, g in enumerate(sel):
    im = Image.open(os.path.join(fr, "g_%04d.png" % g)).convert("RGB").resize((tw, th), Image.LANCZOS); d = ImageDraw.Draw(im)
    d.line([(0, int(880 * th / 1280)), (tw, int(880 * th / 1280))], fill=(0, 255, 255), width=1); d.text((3, 3), str(g), fill=(255, 255, 0))
    sheet.paste(im, ((i % cols) * tw, (i // cols) * th))
sheet.save(os.path.join(D, "contact.jpg"), quality=88)
# meta / cues
meta = dict(take=take, film=23, shot=CFG["shot"], first_g=clk.first, n_frames=clk.nf, g0=clk.g0, g1=clk.g1, g1_render=clk.g1r, handle_in=clk.h_in, handle_out=clk.h_out,
            seconds_per_frame_wall=round(float(np.mean(walls)), 1), transition_in=CFG.get("trans_in", dict(type="cut", frames=0)),
            note="timing is an ESTIMATE (timing_EST.json); take renders g0..g0+ceil((g1-g0)*1.25) then the out-handle; camera and action continue through the tail",
            parts=[os.path.basename(p) for p in parts], mkv_mb=round(size, 1))
json.dump(meta, open(os.path.join(D, "meta.json"), "w"), indent=1)
cues = getattr(m, "CUES", [])
json.dump(dict(take=take, fps=30, note="time = film seconds (g / 30); narration timing is an estimate", cues=cues), open(os.path.join(D, "cues.json"), "w"), indent=1)
# QA.md
L = ["# QA.md: film 23 take %s (shot %s, LANE morning)" % (take, CFG["shot"]), "",
     "Frames g %d .. %d (%d frames, 720x1280, 12 samples, denoise OIDN, 2 threads, no captions): planned shot g %d .. %d, render with the x1.25 tail to g %d (exclusive), handles in %d / out %d."
     % (clk.first, clk.last, clk.nf, clk.g0, clk.g1, clk.g1r, clk.h_in, clk.h_out),
     "Transition in: %s. Wall time %.1f s per frame (2 render processes at once, 2 threads each)." % (CFG.get("trans_in"), float(np.mean(walls))), "",
     "## Automatic checks", "- ground_check: see GROUND.md (every 10th frame + first + last).",
     "- qa_auto.py: exit %d (0 = no FAIL), see QA_AUTO.md; phone_sheet.jpg." % qa_exit,
     "- qa_jitter.py output (every second must be <= 2.0 px; no line = clean):", "```", j or "(empty)", "```",
     "- Frame difference on 90x160 grey inside the shot: median %.2f (rule >= 4), p90 %.2f (rule >= 12), min %.2f." % (med, p90, mn),
     "- Shade hue (target 240-260): " + "; ".join("%s g%d %.1f (%.0f%% of px)" % (k_, v[0], v[1], v[2] * 100) for k_, v in hue.items()), "",
     "## Heads (screen px, head centre; caption band starts y 880, head radius <= ~60 px)", "| actor | y min | y max | x min | x max |", "|---|---|---|---|---|"]
for n, v in heads.items():
    ys = [p[2] for p in v]; xs = [p[1] for p in v]; L.append("| %s | %.0f | %.0f | %.0f | %.0f |" % (n, min(ys), max(ys), min(xs), max(xs)))
L += ["", "## qa_auto output", "```", qa_out, "```"]
open(os.path.join(D, "QA.md"), "w").write("\n".join(L) + "\n")
print("median diff %.2f p90 %.2f" % (med, p90)); print("jitter:", j or "clean"); print("qa_auto exit", qa_exit); print(hue); print(size, "MB", parts)

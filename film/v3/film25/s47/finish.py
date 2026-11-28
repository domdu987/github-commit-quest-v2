#!/usr/bin/env python3
"""finish.py <take_dir> <g0> <g1> [--puppet]  -- grade the raw frames (t2lib.post_take, params smoothed over the take), encode take.mkv
(libx264rgb crf 12), meta.json, contact.jpg, QA_AUTO.md + phone_sheet.jpg, qa_jitter, light_metrics, camera numbers -> QA.md,
then one status line in film/v3/film25/T2_STATUS.md.   g1 is EXCLUSIVE; frames g0-6 .. g1-1+6 are used when present."""
import os, sys, json, glob, subprocess, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import t2lib as T
from PIL import Image
PROJ = T.C.PROJ
td = os.path.abspath(sys.argv[1]); g0, g1 = int(sys.argv[2]), int(sys.argv[3]); name = os.path.basename(td)
raw = os.path.join(td, "frames", "raw"); out = os.path.join(td, "frames_post")
gs = sorted(int(os.path.basename(p)[2:6]) for p in glob.glob(raw + "/f_*.png"))
gs = [g for g in gs if os.path.exists(os.path.join(td, "frames", "g_%04d.json" % g))]
assert gs, "no frames"
first, last = gs[0], gs[-1]
assert all(b - a == 1 for a, b in zip(gs, gs[1:])), "gap in frames"
for p in glob.glob(out + "/g_*.png"): os.remove(p)
P = T.post_take(gs, raw, out)
mkv = os.path.join(td, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-start_number", str(first), "-i", out + "/g_%04d.png", "-c:v", "libx264rgb", "-crf", "12", "-preset", "slow", mkv], check=True)
meta = dict(g0=g0, g1=g1, first_g=first, n_frames=len(gs), transition_in=dict(type="cut", frames=0))
json.dump(meta, open(os.path.join(td, "meta.json"), "w"), indent=1)
# contact sheet: 6 fps over g0..g1 (+-3 around the ends), 6 columns
sel = sorted(set([g for g in range(g0, g1, 5)] + [g0, g1 - 1, max(first, g0 - 3), min(last, g1 + 2)]))
tw, th = 120, 213; cols = 12; rows = (len(sel) + cols - 1) // cols
S = Image.new("RGB", (cols * tw, rows * th), (20, 20, 20))
for i, g in enumerate(sel):
    S.paste(Image.open(os.path.join(out, "g_%04d.png" % g)).convert("RGB").resize((tw, th), Image.LANCZOS), ((i % cols) * tw, (i // cols) * th))
S.save(os.path.join(td, "contact.jpg"), quality=86)
qa = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(first), "--out", td], capture_output=True, text=True)
jit = subprocess.run([sys.executable, os.path.join(PROJ, "qa_jitter.py"), mkv], capture_output=True, text=True).stdout.strip()
lm = subprocess.run([sys.executable, os.path.join(PROJ, "film25", "tools", "light_metrics.py"), mkv], capture_output=True, text=True).stdout.strip()
J = {g: json.load(open(os.path.join(td, "frames", "g_%04d.json" % g))) for g in gs}
walls = [J[g]["wall"] for g in gs]; cpus = [J[g].get("cpu", 0) for g in gs]
cam = [J[g].get("cam") for g in gs if J[g].get("cam")]
move = ""
if cam and len(cam) == len(gs):
    in_row = [g for g in gs if g0 <= g < g1]
    c0, c1 = J[in_row[0]]["cam"], J[in_row[-1]]["cam"]; l0, l1 = J[in_row[0]]["look"], J[in_row[-1]]["look"]
    d0 = math.dist(c0, l0); d1 = math.dist(c1, l1); lens = J[in_row[0]].get("lens", 24)
    wD = 2 * d0 * 10.125 / lens
    lat = math.hypot(c1[0] - c0[0], c1[1] - c0[1] - (d1 - d0) * 0) if False else abs(c1[0] - c0[0])
    secs = (len(in_row) - 1) / 30.0
    move = "camera: first -> last frame of the row: subject distance %.1f -> %.1f D (scale %+.1f %%), lateral camera travel %.1f D = %.0f %% of the frame width per second (frame width %.1f D at the subject)" % (d0, d1, (d0 / d1 - 1) * 100, lat, lat / wD * 100 / max(secs, 1e-6), wD)
q = "## Render\n- %d frames g %d-%d (row g %d-%d + handles), %.1f s wall / frame mean (min %.1f, max %.1f), %.1f s CPU, samples %s thr %s scale %s, OIDN, 2 procs x 2 threads\n" % (
    len(gs), first, last, g0, g1 - 1, sum(walls) / len(walls), min(walls), max(walls), sum(cpus) / len(cpus), J[first].get("samples"), J[first].get("threshold"), J[first].get("scale"))
q += "- post: t2lib.post_take (set sharpen + clarity, gentle grade, exposure/WB smoothed over the take)\n\n## light_metrics\n```\n%s\n```\n\n## qa_jitter\n```\n%s\n```\n\n## qa_auto\n%s\n" % (lm, jit, "PASS" if qa.returncode == 0 else "FAIL (see QA_AUTO.md)")
if move: q += "\n## Camera\n- %s\n" % move
extra = os.path.join(td, "QA_extra.md")
if os.path.exists(extra): q += "\n" + open(extra).read()
open(os.path.join(td, "QA.md"), "w").write("# QA %s (film 25, g %d-%d)\n\n" % (name, g0, g1 - 1) + q)
sf = os.path.join(os.path.dirname(td), "T2_STATUS.md")
line = "- %s g %d-%d: %d fr, %.0f s/frame wall (2 procs x 2 thr), %s | %s\n" % (name, g0, g1 - 1, len(gs), sum(walls) / len(walls), lm.replace("\n", " "), "qa_auto " + ("PASS" if qa.returncode == 0 else "FAIL"))
open(sf, "a").write(line)
print(q); print(line)

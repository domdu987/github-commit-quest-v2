#!/usr/bin/env python3
"""finish.py <take_dir> <row_label> <g0> <g1> <first_g> <last_g> [--move "text"] [--cuts g,g] [--push]
encode take.mkv, QA_AUTO.md + phone_sheet.jpg (qa_auto), qa_jitter, light_metrics, contact.jpg, meta.json, QA.md, T1_STATUS.md line; --push commits + pushes"""
import sys, os, json, subprocess, glob, argparse, statistics
from PIL import Image
ap = argparse.ArgumentParser()
ap.add_argument("take"); ap.add_argument("label"); ap.add_argument("g0", type=int); ap.add_argument("g1", type=int)
ap.add_argument("first_g", type=int); ap.add_argument("last_g", type=int)
ap.add_argument("--move", default=""); ap.add_argument("--cuts", default=""); ap.add_argument("--push", action="store_true"); ap.add_argument("--note", default="")
a = ap.parse_args()
T = os.path.abspath(a.take); FILM = os.path.abspath(os.path.join(T, "..", "..", ".."))
n = a.last_g - a.first_g + 1
for g in range(a.first_g, a.last_g + 1):
    if not os.path.exists(os.path.join(T, "frames", "g_%04d.png" % g)):
        sys.exit("missing frame %d" % g)
mkv = os.path.join(T, "take.mkv")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-start_number", str(a.first_g), "-i", os.path.join(T, "frames", "g_%04d.png"),
                "-frames:v", str(n), "-c:v", "libx264rgb", "-crf", "12", "-preset", "slow", mkv], check=True)
meta = dict(g0=a.g0, g1=a.g1, first_g=a.first_g, n_frames=n, transition_in=dict(type="cut", frames=0))
json.dump(meta, open(os.path.join(T, "meta.json"), "w"), indent=1)
run = lambda *c: subprocess.run(list(c), capture_output=True, text=True)
qa = run("python3", os.path.join(FILM, "qa_auto.py"), mkv, "--first_g", str(a.first_g), "--cuts", a.cuts or "none", "--out", T)
jit = run("python3", os.path.join(FILM, "qa_jitter.py"), mkv)
lm = run("python3", os.path.join(FILM, "film25", "tools", "light_metrics.py"), mkv)
# contact sheet: every 5th frame (6 fps), 8 per row
fr = list(range(a.first_g, a.last_g + 1, 5)); cols = 8; tw, th = 135, 240
rows = (len(fr) + cols - 1) // cols
sheet = Image.new("RGB", (cols * tw, rows * th), (20, 20, 20))
for i, g in enumerate(fr):
    sheet.paste(Image.open(os.path.join(T, "frames", "g_%04d.png" % g)).convert("RGB").resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
sheet.save(os.path.join(T, "contact.jpg"), quality=88)
walls = []; sc = []
for f in sorted(glob.glob(os.path.join(T, "frames", "g_*.json"))):
    j = json.load(open(f)); walls.append(j["wall"]); sc.append(j.get("scale"))
spf = statistics.mean(walls) if walls else 0
lml = [l for l in lm.stdout.splitlines() if l.strip()][-1] if lm.stdout.strip() else lm.stderr[-300:]
open(os.path.join(T, "QA.md"), "w").write(f"""# QA row {a.label} (g {a.g0}-{a.g1 - 1}, first_g {a.first_g}, {n} frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** {spf:.1f} s wall (mean over {len(walls)} frames, 2 threads, 2 processes running)
- **Camera move:** {a.move}
- **light_metrics:** `{lml}`
- **qa_auto:** see QA_AUTO.md ({'exit 0' if qa.returncode == 0 else 'FAILS: ' + qa.stdout[-400:]})
- **qa_jitter:** {jit.stdout.strip() or 'no shake flagged'}
- {a.note}
""")
line = f"- row {a.label}: g {a.first_g}-{a.last_g} ({n} fr) | {spf:.0f} s/frame | {lml}\n"
st = os.path.join(FILM, "v3", "film25", "T1_STATUS.md")
open(st, "a").write(line)
print(line, qa.stdout[-300:], jit.stdout, flush=True)
if a.push:
    r = os.path.abspath(os.path.join(FILM, ".."))
    subprocess.run(["git", "-C", r, "add", "film/v3/film25"], check=True)
    subprocess.run(["git", "-C", r, "commit", "-m", f"film25 T1: row {a.label} take (g {a.first_g}-{a.last_g})\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_017iwyCuhnwG52F7wAR8phsi"], check=True)
    for k in range(4):
        if subprocess.run(["git", "-C", r, "push", "-u", "origin", "render25/t1"]).returncode == 0: break
        import time; time.sleep(2 ** (k + 1))

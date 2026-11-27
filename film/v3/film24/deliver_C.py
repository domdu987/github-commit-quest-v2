#!/usr/bin/env python3
"""deliver_C.py <take dir> -- version C delivery: raw/s<id>/g_*.png -> frames_C/, take_C.mkv (crf 12), meta_C.json (+offset), contact_C.jpg,
QA_AUTO_C.md + phone_sheet_C.jpg (qa_auto), optional build_anchors.json (s08C).  Config: s08C built-in; others read meta.json (old numbering) + offset 208."""
import os, sys, json, shutil, subprocess, glob
from PIL import Image, ImageDraw
HERE = os.path.abspath(sys.argv[1]); take = os.path.basename(HERE)
if take == "s08C":
    meta = dict(take="s08C", film=24, shots=["build-up"], g0=734, g1=1126, first_g=728, n_frames=410, handle_in=6, handle_out=6, shot_ranges={"8": [728, 1131]}, in_take_cuts=[])
    OFF = 0
else:
    meta = json.load(open(os.path.join(HERE, "meta.json"))); OFF = 208
SR = {int(k): v for k, v in meta["shot_ranges"].items()}
FIRST = meta["first_g"]; LAST = meta["first_g"] + meta["n_frames"] - 1
fr = os.path.join(HERE, "frames_C"); shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr)
rows = []
for g in range(FIRST, LAST + 1):
    sid = [s for s, (a, b) in SR.items() if a <= g <= b][0]
    src = os.path.join(HERE, "raw", "s%d" % sid, "g_%04d.png" % g)
    shutil.copyfile(src, os.path.join(fr, "g_%04d.png" % g)); rows.append(json.load(open(src[:-4] + ".json")))
mean = lambda v: round(sum(v) / len(v), 1)
mc = dict(meta); mc.update(g0=meta["g0"] + OFF, g1=meta["g1"] + OFF, first_g=FIRST + OFF, look="C", render_g_first=FIRST, g_offset=OFF,
         note="look C (JOSEON_LOOK=C): frames are numbered by their OLD g in frames_C; conform places them at first_g (+%d)" % OFF,
         samples=sorted({r["samples"] for r in rows}), resolution=[720, 1280], render_resolution=[540, 960],
         s_per_frame_wall_mean=mean([r["wall"] for r in rows]), s_per_frame_cpu_mean=mean([r["cpu"] for r in rows]))
json.dump(mc, open(os.path.join(HERE, "meta_C.json"), "w"), indent=1)
if take == "s08C":
    json.dump([r["anchor"] for r in rows], open(os.path.join(HERE, "build_anchors.json"), "w"))
mk = os.path.join(HERE, "take_C.mkv")
for p in glob.glob(mk + "*"): os.remove(p)
subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(fr, "g_%04d.png"),
                       "-c:v", "libx264rgb", "-crf", "12", "-preset", "slow", mk])
if os.path.getsize(mk) > 45 * 1024 * 1024:
    subprocess.check_call("split -b 40M take_C.mkv take_C.mkv.part && rm take_C.mkv", shell=True, cwd=HERE)
# contact sheet: every 6th frame
gs = list(range(FIRST, LAST + 1, 6)); w = 180; h = 320; cols = 12; nr = (len(gs) + cols - 1) // cols
sh = Image.new("RGB", (w * cols, (h + 14) * nr), (20, 20, 20)); d = ImageDraw.Draw(sh)
for i, g in enumerate(gs):
    im = Image.open(os.path.join(fr, "g_%04d.png" % g)).convert("RGB").resize((w, h)); x, y = (i % cols) * w, (i // cols) * (h + 14)
    sh.paste(im, (x, y + 14)); d.text((x + 2, y + 1), "g%d" % g, fill=(255, 255, 255))
sh.save(os.path.join(HERE, "contact_C.jpg"), quality=82)
cuts = ",".join(str(c) for c in meta.get("in_take_cuts", []))
src_mkv = mk if os.path.exists(mk) else None
if src_mkv is None:
    subprocess.check_call("cat take_C.mkv.part* > /tmp/_tc.mkv", shell=True, cwd=HERE); src_mkv = "/tmp/_tc.mkv"
tmp = os.path.join(HERE, "work", "qa_C"); os.makedirs(tmp, exist_ok=True)
r = subprocess.run([sys.executable, os.path.join(HERE, "..", "..", "..", "qa_auto.py"), src_mkv, "--first_g", str(FIRST), "--cuts", cuts, "--out", tmp])
shutil.copyfile(os.path.join(tmp, "QA_AUTO.md"), os.path.join(HERE, "QA_AUTO_C.md"))
shutil.copyfile(os.path.join(tmp, "phone_sheet.jpg"), os.path.join(HERE, "phone_sheet_C.jpg"))
print("delivered", take, "qa_auto exit", r.returncode)

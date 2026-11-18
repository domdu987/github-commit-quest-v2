#!/usr/bin/env python3
"""deliver.py <take> -- raw/s<id>/g_*.png -> frames/, take.mkv (libx264rgb crf 6), meta.json, cues.json, contact.jpg, QA_AUTO.md + phone_sheet.jpg.
Reads TAKES below."""
import os, sys, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
TAKE = os.path.basename(HERE)
CFG = {
 "s05": dict(shots={5: (287, 365), 6: (366, 449), 7: (450, 543)}, g0=293, g1=538, shots_l=[5, 6, 7], cuts=[366, 450],
             tin={"type": "cut", "frames": 0}, set="harbour quay_low, DAY (custom cameras on the quay)", lipsync=[343, 540],
             cast="admiral + painter10 (cast10)"),
 "s08": dict(shots={8: (532, 624)}, g0=538, g1=619, shots_l=[8], cuts=[],
             tin={"type": "cut", "frames": 0}, set="harbour DAY (custom medium camera on the quay)", lipsync=None,
             cast="sailor_a/b/c + painter10 (cast10)"),
}[TAKE]
FIRST = min(v[0] for v in CFG["shots"].values()); LAST = max(v[1] for v in CFG["shots"].values()); N = LAST - FIRST + 1
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
rows = []
for sid, (a, b) in CFG["shots"].items():
    for g in range(a, b + 1):
        raw = os.path.join(HERE, "raw", "s%d" % sid)
        shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
        rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", os.path.join(HERE, "take.mkv")], check=True)
sz = os.path.getsize(os.path.join(HERE, "take.mkv")) / 1e6
if sz > 45:
    subprocess.run("split -b 40M take.mkv take.mkv.part", shell=True, cwd=HERE, check=True)
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
meta = {"take": TAKE, "film": 10, "shots": CFG["shots_l"], "g0": CFG["g0"], "g1": CFG["g1"], "first_g": FIRST, "n_frames": N,
        "handle_in": CFG["g0"] - FIRST, "handle_out": LAST + 1 - CFG["g1"], "transition_in": CFG["tin"],
        "set": CFG["set"], "light": "DAY", "cast": CFG["cast"], "samples": 12, "resolution": [720, 1280], "fps": 30, "dof": "none",
        "cuts": CFG["cuts"], "lipsync_window_g": CFG["lipsync"], "stripes": 0.6,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "take_mkv_mb": round(sz, 1)}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
# contact sheet: 12+ evenly spaced frames, label strip above
n = 15; idx = [int(round(i * (N - 1) / (n - 1))) + FIRST for i in range(n)]
tw, th = 240, 427; cols = 5; rws = (n + cols - 1) // cols
sh = Image.new("RGB", (cols * tw, rws * (th + 16)), (20, 20, 20)); d = ImageDraw.Draw(sh)
for i, g in enumerate(idx):
    im = Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((tw, th), Image.LANCZOS)
    x, y = (i % cols) * tw, (i // cols) * (th + 16); sh.paste(im, (x, y + 16)); d.text((x + 3, y + 2), "g %d  %.2f s" % (g, g / 30.0), fill=(255, 255, 255))
sh.save(os.path.join(HERE, "contact.jpg"), quality=88)
# mouth log + cues
mouth = {r["g"]: r.get("mouth") for r in rows}
json.dump(mouth, open(os.path.join(HERE, "mouth_log.json"), "w"))
t = lambda g: round(g / 30.0, 3)
ev = []
if TAKE == "s05":
    ev = [dict(time=t(293), duration=1.0, label="admiral's boots and heavy stride on quay stones, coat creak", kind="foley"),
          dict(time=t(320), duration=0.9, label="admiral bursts out laughing (big belly laugh, wheeze)", kind="voice_fx"),
          dict(time=t(343), duration=6.6, label="harbour ambience: gulls, ropes, distant crane clank under the quote", kind="ambience")]
else:
    ev = [dict(time=t(538), duration=2.7, label="sailors' laughter and jeers across the quay, boots stamping, gulls", kind="crowd"),
          dict(time=t(538), duration=2.7, label="harbour ambience: water slap, rope creak, distant crane", kind="ambience")]
json.dump(ev, open(os.path.join(HERE, "cues.json"), "w"), indent=1)
cuts = ",".join(str(c) for c in CFG["cuts"])
r = subprocess.run([sys.executable, os.path.join(HERE, "..", "..", "..", "qa_auto.py"), os.path.join(HERE, "take.mkv"), "--first_g", str(FIRST)] + (["--cuts", cuts] if cuts else []),
                   capture_output=True, text=True)
print(r.stdout[-3000:], r.stderr[-1500:], "exit", r.returncode)

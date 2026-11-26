"""test_pop.py -- 2D overlay test: icons pop in over a night plate at 720x1280 / 30 fps, plus measurements.

    python3 test_pop.py [out_dir]   -> pop_test.mp4, pop_contact.png, pop_measure.json
"""
import json, os, subprocess, sys, time
import numpy as np
from PIL import Image

import icons as I
import overlay as OV
import raster
import sheet
from anim import Cue, pop_state

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out", "poptest")
os.makedirs(OUT, exist_ok=True)
N = 120

P = [
    OV.Placement("sound_rings", Cue(4, hold=100), x=360, y=560, px=330, kw={"mode": "circle", "period": 0.9}),
    OV.Placement("exclaim_sparks", Cue(18, hold=30), x=200, y=330, px=150),
    OV.Placement("stopwatch", Cue(30, hold=80), x=560, y=230, px=200, kw={"speed": 15.0}),
    OV.Placement("phone", Cue(46, hold=50), x=190, y=640, px=170, kw={"n": 4}),
    OV.Placement("sound_rings", Cue(52, hold=60), x=190, y=640, px=250, kw={"mode": "arcs", "period": 0.7}),
    OV.Placement("x_mark", Cue(64, hold=50, profile="snap"), x=470, y=720, px=120),
    OV.Placement("check", Cue(72, hold=40, profile="snap"), x=600, y=720, px=120),
    OV.Placement("heart", Cue(80, hold=36), x=360, y=380, px=160),
    OV.Placement("battery", Cue(86, hold=30), x=200, y=1120, px=150, kw={"level": 1}),
]

# background plate: the sheet's night background
bgp = os.path.join(OUT, "bg.png")
raster.render([{"svg": '<svg xmlns="http://www.w3.org/2000/svg" width="720" height="1280">%s</svg>' % sheet.night_bg(720, 1280),
                "w": 720, "h": 1280, "out": bgp}])
fr = os.path.join(OUT, "frames")
os.makedirs(fr, exist_ok=True)
ms = []
for g in range(N):
    t0 = time.time()
    lay = OV.render_layer(P, g, os.path.join(OUT, "ovl_%04d.png" % g))
    ms.append((time.time() - t0) * 1000)
    OV.composite(bgp, lay, os.path.join(fr, "f_%04d.png" % g))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-i", os.path.join(fr, "f_%04d.png"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", os.path.join(OUT, "pop_test.mp4")], check=True)

# contact: 12 frames
ims = [Image.open(os.path.join(fr, "f_%04d.png" % g)).resize((180, 320)) for g in range(0, N, 10)]
C = Image.new("RGB", (180 * 6, 320 * 2))
for i, im in enumerate(ims):
    C.paste(im, ((i % 6) * 180, (i // 6) * 320))
C.save(os.path.join(OUT, "pop_contact.png"))

# measure the pop on the rendered pixels: a static icon (warning) alone, width of the alpha box per frame
cue = Cue(0, hold=4)
widths = []
for g in range(cue.g_end + 1):
    lay = OV.render_layer([OV.Placement("warning", cue, 360, 640, 200, rim=False, shadow=False)], g,
                          os.path.join(OUT, "m_%02d.png" % g))
    if lay is None:
        widths.append(0)
        continue
    a = np.asarray(Image.open(lay))[..., 3] > 128
    xs = np.nonzero(a.any(0))[0]
    widths.append(int(xs.max() - xs.min() + 1) if len(xs) else 0)
    os.remove(lay)
full = widths[cue.g_hold]
res = {"layer_ms_mean": float(np.mean(ms)), "layer_ms_max": float(np.max(ms)),
       "pop_width_px": widths, "pop_width_ratio": [round(w / float(full), 3) for w in widths],
       "pop_scale_expected": [round(pop_state(cue, g).scale, 3) for g in range(cue.g_end + 1)],
       "caption_safe_issues": OV.safe_report(P), "overlap_frames": len([1 for g in range(N) if sum(pop_state(p.cue, g).visible for p in P) > 1])}
json.dump(res, open(os.path.join(OUT, "pop_measure.json"), "w"), indent=1)
print(json.dumps(res))
for f_ in os.listdir(OUT):
    if f_.startswith("ovl_"):
        os.remove(os.path.join(OUT, f_))

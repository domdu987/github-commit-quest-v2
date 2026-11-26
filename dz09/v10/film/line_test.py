"""line_test.py -- proof that the ink lines stay crisp as video: 36 consecutive final-tier frames of S13 (g 608..643,
25.33-26.83 s) at 720x1280, 100 % render scale, finished (icons, captions), looped 3 times with the Ohm mix of that span.

    for i in 0 1 2 3; do python3 run.py --frames 608:644 --tier final --size 720x1280 --threads 1 --worker $i/4 & done
    python3 line_test.py          -> line_test_720.mp4, line_test_crop.png (draft_v3 frame | new final frame, 2x face crop)
"""
import os, sys, subprocess
import cv2, numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import common as C, finish as FN
G0, G1, W, H = 608, 644, 720, 1280
base = FN.base_dir("final", W, H)
out = os.path.join(base, "line_test"); os.makedirs(out, exist_ok=True)
for g in range(G0, G1):
    FN.comp_frame(base, g, W, H).save(os.path.join(out, "f_%04d.png" % (g - G0)))
FN.icons().close()
t0 = G0 / float(C.FPS); dur = (G1 - G0) / float(C.FPS)
one = os.path.join(out, "one.mp4")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(C.FPS), "-i", os.path.join(out, "f_%04d.png"), "-ss", "%.4f" % t0, "-t", "%.4f" % dur, "-i", FN.MIX,
                "-vf", "setpts=PTS+%.4f/TB,ass=%s:fontsdir=%s,setpts=PTS-STARTPTS" % (t0, FN.ass_path(), C.FONTS), "-af", "volume=-0.4dB,afade=t=in:d=0.02,afade=t=out:st=%.3f:d=0.03" % (dur - 0.03),
                "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-tune", "animation", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "320k", "-t", "%.4f" % dur, one], check=True)
dst = os.path.join(HERE, "line_test_720.mp4")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "2", "-i", one, "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-tune", "animation", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", dst], check=True)
print("wrote", dst)
# crop sheet: the same film frame from draft_v3.mp4 and from the new video, Kong's face at 2x
g = 626
def grab(path, n):
    cap = cv2.VideoCapture(path); cap.set(cv2.CAP_PROP_POS_FRAMES, n); ok, f = cap.read(); assert ok, path
    return cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
a = grab(os.path.join(HERE, "draft_v3.mp4"), g); b = grab(dst, g - G0)
box = (150, 250, 510, 700)                                  # x0, y0, x1, y1: Kong's head in S13
crops = [Image.fromarray(x[box[1]:box[3], box[0]:box[2]]).resize(((box[2] - box[0]) * 2, (box[3] - box[1]) * 2), Image.NEAREST) for x in (a, b)]
lab = 40; S = Image.new("RGB", (crops[0].width * 2 + 12, crops[0].height + lab), (14, 14, 18)); d = ImageDraw.Draw(S); f = FN.font(C.WORKS, 22)
for i, (c, txt) in enumerate(zip(crops, ("draft_v3.mp4 f%d: 360x640 render scaled up 2x" % g, "line_test_720.mp4 f%d: final tier, 720x1280 at 100 %%" % g))):
    S.paste(c, (i * (c.width + 12), lab)); d.text((i * (c.width + 12) + 8, 8), txt, font=f, fill=(232, 232, 236))
S.save(os.path.join(HERE, "line_test_crop.png")); print("wrote line_test_crop.png", S.size)

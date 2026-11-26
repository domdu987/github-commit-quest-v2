"""demo.py -- demo.mp4: the whole film, 720x1280, cards over the clean draft frames (out/draft_360x640 through finish.py's
comp_frame with this module as the overlay), the film's captions (v10/film/captions_ohm.ass, read only), mix_ohm_v2.wav, CRF 20.
One process:  nice -n 15 python3 demo.py"""
import os, subprocess, sys, time, json
import numpy as np
import cards14 as C
sys.path.insert(0, os.path.join(C.PROJ, "v10", "film"))
import finish as FN
FN._IC["m"] = C
base = FN.base_dir("draft", 360, 640)
ass = os.path.join(C.PROJ, "v10", "film", "captions_ohm.ass")
ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "720x1280", "-r", "24", "-i", "-",
                       "-i", os.path.join(C.PROJ, "audio", "narr_ohm", "mix_ohm_v2.wav"), "-vf", "ass=%s:fontsdir=%s" % (ass, os.path.join(C.PROJ, "fonts")),
                       "-threads", "1", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                       "-t", "53.333", "-movflags", "+faststart", os.path.join(C.HERE, "demo.mp4")], stdin=subprocess.PIPE)
last, miss, t0 = None, [], time.time()
for g in range(C.NF):
    im = FN.comp_frame(base, g, 720, 1280)
    if im is None:
        miss.append(g); im = last
    last = im
    ff.stdin.write(np.asarray(im.convert("RGB")).tobytes())
ff.stdin.close(); ff.wait(); C.close()
print("demo done, missing frames:", miss, "total s: %.0f" % (time.time() - t0))

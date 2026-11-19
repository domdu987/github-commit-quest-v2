"""Version 1.1 without any background blur: the v1 conform frames (sharp) through the v1.1 grade, the same captions burned last,
the v1.1 mix. Frames are piped straight into the encoder; the graded frames in graded/ are overwritten with the sharp ones.
usage: python3 make_sharp.py   (run from this folder)"""
import os, sys, subprocess
import numpy as np
from multiprocessing import Pool
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); FILM = os.path.dirname(HERE); PROJ = os.path.normpath(os.path.join(FILM, "..", ".."))
sys.path.insert(0, HERE); os.chdir(HERE)
import grade
SRC = os.path.join(FILM, "out", "frames"); ASS = os.path.join(FILM, "out", "film_silent.ass"); FONTS = os.path.join(PROJ, "fonts")
SILENT = os.path.join(HERE, "film_silent_sharp.mp4"); MIX = os.path.join(HERE, "film_mix.wav"); OUT = os.path.join(PROJ, "deliver", "film_v1_1_sharp_thai.mp4")
N = 1965
GRADED = os.path.join(HERE, "graded")      # the graded frames without captions, rewritten here without blur
def work(g):
    im = grade.grade_frame(Image.open(os.path.join(SRC, "g_%04d.png" % g)).convert("RGB"), g).convert("RGB")
    tmp = os.path.join(GRADED, ".tmp_%04d.png" % g); im.save(tmp, compress_level=3); os.replace(tmp, os.path.join(GRADED, "g_%04d.png" % g))
    return np.asarray(im, np.uint8).tobytes()
if __name__ == "__main__":
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "720x1280", "-framerate", "30", "-i", "-",
                           "-vf", f"ass={ASS}:fontsdir={FONTS}", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", SILENT], stdin=subprocess.PIPE)
    with Pool(3) as p:
        for i, b in enumerate(p.imap(work, range(N), chunksize=6)):
            assert len(b) == 720 * 1280 * 3, (i, len(b)); ff.stdin.write(b)
            if i % 200 == 0: print("frame", i, flush=True)
    ff.stdin.close(); rc = ff.wait(); print("encode rc", rc, flush=True); assert rc == 0
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", SILENT, "-i", MIX, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT], check=True)
    print("wrote", OUT, flush=True)

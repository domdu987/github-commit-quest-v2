"""demo.py -- gauge_demo.mp4: the key gauge moments cut together from the finished 720x1280 frames
(draft picture 360x640 scaled up, gauges drawn at 720x1280, captions burned in; silent because it is a cut-down).
First:  cd PROJ/v10/film && python3 finish.py comp --tier draft --size 720x1280 --base-size 360x640
Then:   python3 demo.py"""
import os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
COMP = os.path.join(PROJ, "v10", "film", "out", "draft_from360x640_720x1280", "comp", "f_%04d.png")
ASS = os.path.join(PROJ, "audio", "narr_v1", "preview_v2.ass")
SEG = [(1.85, 3.60), (16.15, 17.75), (19.00, 20.30), (27.95, 29.30), (31.45, 32.55), (41.00, 42.35), (43.30, 44.20), (46.40, 48.55), (50.65, 51.75)]


def main(out=os.path.join(HERE, "gauge_demo.mp4")):
    sel = "+".join("between(t,%.3f,%.3f)" % s for s in SEG)
    vf = "ass=%s:fontsdir=%s,select='%s',setpts=N/24/TB" % (ASS, os.path.join(PROJ, "fonts"), sel)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i", COMP, "-vf", vf, "-r", "24", "-c:v", "libx264", "-preset", "medium",
                    "-crf", "15", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], check=True)
    print("wrote", out, "%.2f s" % sum(b - a for a, b in SEG))


if __name__ == "__main__":
    main()

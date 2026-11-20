#!/usr/bin/env python3
"""encode.py <draft|final> <out.mkv> : joins raw_<q>/s15..s17 frames g 878..1050 (in order) into one mkv (draft: 360x640 x264; final: libx264rgb crf 6)."""
import sys, os, subprocess, glob, shutil
q, out = sys.argv[1], sys.argv[2]
H = os.path.dirname(os.path.abspath(__file__)); tmp = os.path.join(H, "work", "seq_" + q)
shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
for s in (15, 16, 17):
    for f in sorted(glob.glob(os.path.join(H, "raw_" + q, "s%d" % s, "g_*.png"))):
        os.symlink(f, os.path.join(tmp, os.path.basename(f)))
codec = ["-c:v", "libx264", "-crf", "12"] if q == "draft" else ["-c:v", "libx264rgb", "-crf", "6", "-preset", "slow"]
subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-start_number", "878", "-i", os.path.join(tmp, "g_%04d.png")] + codec + ["-pix_fmt", "rgb24" if q != "draft" else "yuv420p", out])

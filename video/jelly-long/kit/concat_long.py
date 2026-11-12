"""หนวดใส ฉบับเต็ม: cut every part out of its project's 60 fps render by frame number (long-parts.json), join them in one filter graph,
encode the HQ master (x264 CRF 16) and the share copy (CRF 24) with long-mix.wav as the sound.
usage: python3 concat_long.py <render dir with L1.mp4 L2.mp4 Lbr.mp4 L3.mp4 Lfb.mp4 Lend.mp4> <long dir with long-parts.json long-mix.wav> <out dir>"""
import json
import os
import subprocess
import sys

RD, LD, OUT = sys.argv[1:4]
os.makedirs(OUT, exist_ok=True)
P = json.load(open(os.path.join(LD, "long-parts.json")))
parts, total = P["parts"], P["total"]
projs = sorted({p["proj"] for p in parts})
idx = {pr: i for i, pr in enumerate(projs)}
# one ffmpeg per part (a single trim streams; several trims of one input in one graph buffer frames and ran out of memory),
# all with the same x264 settings, then the concat demuxer joins them without re-encoding and the long mix goes on
segs = []
for k, p in enumerate(parts):
    a, b = p["frame0"], p["frame0"] + p["frames"]; sp = os.path.join(OUT, f"seg{k:02d}.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(RD, p["proj"] + ".mp4"), "-vf", f"trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS",
                    "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-r", "60", "-threads", "4", sp], check=True)
    segs.append(sp); print("seg", k, p["part"], p["frames"], flush=True)
lst = os.path.join(OUT, "segs.txt"); open(lst, "w").write("".join(f"file '{os.path.abspath(s)}'\n" for s in segs))
hq = os.path.join(OUT, "LONG-jelly-16x9-HQ.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", os.path.join(LD, "long-mix.wav"), "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-t", f"{total:.4f}", "-movflags", "+faststart", hq], check=True)
for s in segs: os.remove(s)
share = os.path.join(OUT, "LONG-jelly-16x9-share.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", hq, "-threads", "4", "-c:v", "libx264", "-preset", "slow", "-crf", "24", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", share], check=True)
for f in (hq, share):
    d = subprocess.check_output(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                                 "stream=nb_read_frames,r_frame_rate,width,height", "-of", "csv=p=0", f], text=True).strip()
    print(os.path.basename(f), d, os.path.getsize(f) // 1048576, "MB")
print("expected frames", sum(p["frames"] for p in parts), "total", total)

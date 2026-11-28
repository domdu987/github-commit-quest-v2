#!/usr/bin/env python3
"""assemble.py -- motion-test deliverables from the rendered frames.
    python3 assemble.py [frames_dir] [out_dir] [r11.mp4]
frames_dir/g_%04d.png (g 522..675, post25.py output 720x1280; default frames_post/) ->
  out_dir/motion_test.mp4     720x1280 30 fps, narration cut to the same range (17.40-22.53 s), captions burnt (Kanit Black 88, white,
                              5 px dark outline, centred at y 900: the channel's conform style)
  out_dir/motion_vs_R11.mp4   1080x960: ours (left) | R11 from its beat start 7.233 s (the admiral mock, right), each 540x960, our audio
  out_dir/motion_strip.jpg    6 fps strip, ours on top, R11 below, same beat-relative times
"""
import os, sys, json, subprocess, glob
HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.dirname(HERE)
PROJ = os.path.dirname(os.path.dirname(GATE))
G0, G1 = 522, 676                                         # g1 exclusive
FPS = 30
R11_T0 = 7.233                                            # R11 cut into the admiral's "war or the circus?" beat (frame 217)
FR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "frames_post")
OUT = sys.argv[2] if len(sys.argv) > 2 else GATE
R11 = sys.argv[3] if len(sys.argv) > 3 else os.environ.get("R11", "")
TMP = os.path.join(HERE, "work", "asm")
os.makedirs(TMP, exist_ok=True)
T0, DUR = G0 / FPS, (G1 - G0) / FPS


def run(cmd):
    subprocess.run(cmd, check=True)


# frames as a sequence 0..N-1 (symlinks)
for f in glob.glob(TMP + "/s_*.png"):
    os.remove(f)
for i, g in enumerate(range(G0, G1)):
    os.symlink(os.path.abspath(os.path.join(FR, "g_%04d.png" % g)), os.path.join(TMP, "s_%04d.png" % i))

# captions (ASS, film time -> clip time; narration is placed at 0.00 s in film 25, so no offset)
caps = json.load(open(os.path.join(PROJ, "film25", "script", "captions.json")))
ts = lambda t: "%d:%02d:%05.2f" % (int(t // 3600), int(t % 3600 // 60), t % 60)
ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 720", "PlayResY: 1280", "WrapStyle: 2", "", "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: Pop,Kanit Black,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,5,0,5,30,30,0,1", "", "[Events]",
       "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
for i, c in enumerate(caps):
    end = c.get("end") or (caps[i + 1]["t"] if i + 1 < len(caps) else c["t"] + 1.0)
    a, b = max(c["t"] - T0, 0.0), min(end - T0, DUR)
    if b - a < 0.1:
        continue
    ass.append("Dialogue: 0,%s,%s,Pop,,0,0,0,,{\\pos(360,900)}%s" % (ts(a), ts(b), c["text"]))
open(TMP + "/caps.ass", "w").write("\n".join(ass))

nar = os.path.join(PROJ, "film25", "audio", "narration.wav")
mt = os.path.join(OUT, "motion_test.mp4")
run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-i", TMP + "/s_%04d.png", "-ss", "%.4f" % T0, "-t", "%.4f" % DUR, "-i", nar,
     "-vf", "ass=%s/caps.ass:fontsdir=%s/fonts" % (TMP, PROJ), "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p",
     "-crf", "16", "-c:a", "aac", "-b:a", "192k", "-t", "%.4f" % DUR, "-movflags", "+faststart", mt])
# a caption-free copy for the metrics (light_metrics does not mask captions)
run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-i", TMP + "/s_%04d.png", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "14", TMP + "/clean.mp4"])

if R11:
    sbs = os.path.join(OUT, "motion_vs_R11.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-i", mt, "-ss", "%.3f" % R11_T0, "-t", "%.4f" % DUR, "-i", R11,
         "-filter_complex", "[0:v]scale=540:960,setsar=1,fps=30[a];[1:v]scale=540:960,setsar=1,fps=30[b];[a][b]hstack=inputs=2[v]",
         "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-c:a", "aac", "-t", "%.4f" % DUR, sbs])
    # 6 fps strip: two rows (ours / R11), same beat-relative times, tiles 160x284
    n = int(DUR * 6)
    run(["ffmpeg", "-y", "-v", "error", "-i", mt, "-vf", "fps=6,scale=160:284,tile=%dx1" % n, "-frames:v", "1", TMP + "/ours_row.png"])
    run(["ffmpeg", "-y", "-v", "error", "-ss", "%.3f" % R11_T0, "-t", "%.4f" % DUR, "-i", R11, "-vf", "fps=6,scale=160:284,tile=%dx1" % n, "-frames:v", "1", TMP + "/r11_row.png"])
    run(["ffmpeg", "-y", "-v", "error", "-i", TMP + "/ours_row.png", "-i", TMP + "/r11_row.png", "-filter_complex", "vstack=inputs=2", "-q:v", "3",
         os.path.join(OUT, "motion_strip.jpg")])
print("ok", mt)

"""Assemble rendered PNG frames + word-pop captions into a 9:16 MP4.
usage: python3 assemble.py <frames_dir> <out.mp4> <captions.json> [fps]
captions.json: [{"t0":0.0,"t1":0.9,"text":"He drew a line"}, ...]
"""
import sys, json, os, subprocess
frames, out, caps_path = sys.argv[1], sys.argv[2], sys.argv[3]
fps = int(sys.argv[4]) if len(sys.argv) > 4 else 24
caps = json.load(open(caps_path))

def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 720", "PlayResY: 1280", "WrapStyle: 2", "",
       "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: Pop,Work Sans Black,50,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,4,1.5,5,40,40,0,1",
       "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
for c in caps:
    # small pop-in: scale 80%->100% over 60 ms, like the reference clips
    fx = r"{\pos(360,900)}"
    ass.append(f"Dialogue: 0,{ts(c['t0'])},{ts(c['t1'])},Pop,,0,0,0,,{fx}{c['text']}")
ass_path = os.path.splitext(out)[0] + ".ass"
open(ass_path, "w").write("\n".join(ass))

cmd = ["ffmpeg", "-y", "-framerate", str(fps), "-i", os.path.join(frames, "f_%04d.png"),
       "-vf", f"ass={ass_path}:fontsdir={os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')}", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", out]
print(" ".join(cmd)); subprocess.run(cmd, check=True)
print("wrote", out)

"""The long YouTube cut from LANDSCAPE episode renders: join the episode bodies (no EP hooks after the first, no end cards)
into one continuous 1920×1080 story — no side panels, no outro. Parts are cached by source file so three plans that share
EP.2–4 cut them once.  usage: python3 long169L.py plan.json   (PARTS_ONLY=1 stops after cutting)"""
import json, os, subprocess, sys
plan = json.load(open(sys.argv[1])); base = os.path.dirname(os.path.abspath(sys.argv[1]))
P = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
parts, xf = plan["parts"], plan.get("xfade", 0.2)
tmp = os.path.join(base, plan.get("tmp", "longL_tmp")); os.makedirs(tmp, exist_ok=True)
segs, starts, t = [], [], 0.0
for p in parts:
    d = p["to"] - p["from"]; src = P(p["video"])
    o = os.path.join(tmp, f"{os.path.basename(src)[:-4]}_{p['from']:.2f}_{p['to']:.2f}.mp4")
    if os.path.exists(o) and os.path.getmtime(o) > os.path.getmtime(src): segs.append(o); starts.append(t); t += d; print("reuse", os.path.basename(o)); continue
    fade = f"afade=t=in:st=0:d={xf},afade=t=out:st={d - xf:.3f}:d={xf}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{p['from']:.3f}", "-i", src, "-t", f"{d:.3f}", "-af", fade, "-c:v", "libx264", "-preset", "medium", "-crf", "14",
                    "-r", "60", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-ar", "48000", o], check=True)
    segs.append(o); starts.append(t); t += d; print("cut", os.path.basename(o))
if os.environ.get("PARTS_ONLY"): print("parts only"); sys.exit(0)
lst = os.path.join(tmp, os.path.basename(plan["out"]) + ".txt"); open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-r", "60", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", P(plan["out"])], check=True)
for i, s in enumerate(starts): print(f"chapter {i + 1}: {int(s // 60)}:{int(s % 60):02d}")
print("total", round(t, 2), "→", plan["out"])

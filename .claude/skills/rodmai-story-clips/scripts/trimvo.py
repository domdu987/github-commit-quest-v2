"""Keep only the spoken line of a recording where the TTS read its style prompt first: python3 trimvo.py <ep dir> <id> <cut seconds>
The original is kept as vo/<id>.full.wav; vo/durations.json is updated."""
import json, os, subprocess, sys
ep, vid, cut = sys.argv[1], sys.argv[2], float(sys.argv[3])
src = os.path.join(ep, "vo", f"{vid}.wav"); full = os.path.join(ep, "vo", f"{vid}.full.wav")
if not os.path.exists(full): os.replace(src, full)
subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", full, "-ss", f"{cut:.3f}", "-af", "afade=t=in:d=0.04", src])
d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]))
D = json.load(open(os.path.join(ep, "vo", "durations.json"))); D[vid] = round(d, 3)
json.dump(D, open(os.path.join(ep, "vo", "durations.json"), "w"), ensure_ascii=False, indent=1); print(vid, "->", round(d, 2), "s")

#!/usr/bin/env bash
# Check a rendered episode before sending it: streams, duration against the mix, loudness and peak, and a frame strip to look at.
# usage: qa_video.sh <video.mp4> [mix.wav] [frames=16]
#   prints the numbers; writes <video>.qa.jpg (frames spread over the whole episode, with their times) — open it and look
# Pass when: 1080x1920 · 60/1 fps · video and audio durations equal the mix (±0.05 s) · integrated ≈ −14 LUFS · true peak ≤ −1 dB
set -euo pipefail
V="$1"; M="${2:-}"; N="${3:-16}"
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,duration:format=duration -of compact "$V"
[ -n "$M" ] && echo "mix duration: $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$M") s"
ffmpeg -hide_banner -nostats -i "$V" -af ebur128=peak=true -f null - 2>&1 | sed -n '/Summary:/,$p' | grep -E "I:|LRA:|Peak:" || true
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
T=$(mktemp -d)
python3 - "$V" "$D" "$N" "$T" <<'EOF'
import subprocess, sys
from PIL import Image, ImageDraw
v, d, n, tmp = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
ts = [(i + 0.5) * d / n for i in range(n)]
w, h, lb, cols = 270, 480, 28, 8
rows = (n + cols - 1) // cols
sheet = Image.new("RGB", (w * cols, (h + lb) * rows), (18, 16, 20))
dr = ImageDraw.Draw(sheet)
for i, t in enumerate(ts):
    f = f"{tmp}/f{i}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", v, "-frames:v", "1", "-vf", f"scale={w}:{h}", f], check=True)
    x, y = (i % cols) * w, (i // cols) * (h + lb)
    sheet.paste(Image.open(f).convert("RGB"), (x, y + lb))
    dr.text((x + 6, y + 8), f"{int(t // 60)}:{t % 60:05.2f}", fill=(244, 236, 216))
out = v.rsplit(".", 1)[0] + ".qa.jpg"
sheet.save(out, quality=86)
print("frame strip:", out)
EOF
rm -rf "$T"

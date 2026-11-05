#!/bin/bash
# prevmux.sh <frames dir with seg0..segN> <mix.wav> <out.mp4> <fps> <a-b> … : each segment's frames + its slice of the mix → one preview mp4
set -e
D="$1"; M="$2"; OUT="$3"; FPS="$4"; shift 4
LIST="$D/list.txt"; : > "$LIST"; k=0
for r in "$@"; do
  a="${r%-*}"; b="${r#*-}"; dur=$(python3 -c "print(round($b-$a,3))")
  ffmpeg -v error -y -framerate "$FPS" -i "$D/seg$k/f%05d.jpg" -ss "$a" -t "$dur" -i "$M" -map 0:v -map 1:a \
    -vf "scale=1280:720:flags=lanczos,format=yuv420p" -r 30 -c:v libx264 -crf 21 -preset veryfast -c:a aac -b:a 160k -ar 48000 -shortest "$D/seg$k.mp4"
  echo "file '$D/seg$k.mp4'" >> "$LIST"; k=$((k+1))
done
ffmpeg -v error -y -f concat -safe 0 -i "$LIST" -c copy "$OUT"
ffprobe -v error -show_entries format=duration,size -of default=nw=1 "$OUT"

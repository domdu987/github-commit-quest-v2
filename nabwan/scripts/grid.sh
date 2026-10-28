#!/bin/bash
# grid.sh <dir> <out.jpg> <cols> <rows> [w h] — tiles still_*.png in numeric time order, with the time stamped on each
d=$1; out=$2; c=$3; r=$4; w=${5:-360}; h=${6:-640}
tmp=$(mktemp -d)
i=0
for f in $(ls $d/still_*.png | sort -t_ -k2 -g); do
  t=$(basename $f .png | sed 's/still_//')
  ffmpeg -v error -y -i $f -vf "scale=$w:$h,drawtext=text='$t':x=8:y=8:fontsize=26:fontcolor=yellow:box=1:boxcolor=black@0.6" $tmp/$(printf %03d $i).png
  i=$((i+1))
done
ffmpeg -v error -y -framerate 1 -i $tmp/%03d.png -vf "tile=${c}x${r}" -frames:v 1 $out
rm -rf $tmp

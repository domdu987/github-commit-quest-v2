#!/bin/bash
# usage: mk.sh dir out.mkv
ffmpeg -y -v error -framerate 30 -start_number 1190 -i $1/g_%04d.png -c:v libx264rgb -crf 6 -preset fast $2

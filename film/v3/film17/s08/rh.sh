#!/bin/bash
# usage: rh.sh <mode dir suffix>  -> builds work/<m>.mkv from raw/s20_<m> + raw/s21_<m>, prints rhythm
m=$1; rm -rf work/r_$m; mkdir -p work/r_$m
for f in raw/s20_$m/g_*.png raw/s21_$m/g_*.png; do ln -s $PWD/$f work/r_$m/$(basename $f); done
ffmpeg -v error -y -framerate 30 -start_number 1039 -i work/r_$m/g_%04d.png -c:v libx264 -crf 12 work/$m.mkv
python3 ../../../film17/rhythm.py work/$m.mkv --first_g 1039 --cuts 1127

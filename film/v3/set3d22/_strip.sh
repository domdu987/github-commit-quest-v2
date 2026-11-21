#!/bin/bash
# usage: _strip.sh shot f1 f2 ...   -> _prev/strip_<shot>.png (preview renders)
sh=$1; shift
files=""
for f in "$@"; do python3 beck.py shot $sh $f preview _prev/${sh}_$f.png 2>&1 | grep -i "error\|Traceback" ; files="$files _prev/${sh}_$f.png"; done
python3 - $sh $files <<'PY'
import sys
from PIL import Image, ImageDraw
sh=sys.argv[1]; fs=sys.argv[2:]
im=Image.new('RGB',(360*len(fs),640))
for i,f in enumerate(fs):
    t=Image.open(f); im.paste(t,(360*i,0)); ImageDraw.Draw(im).text((360*i+6,4),f.split('_')[-1][:-4],fill='white')
im.save('_prev/strip_%s.png'%sh)
PY

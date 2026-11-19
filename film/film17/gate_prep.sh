#!/bin/bash
# usage: gate_prep.sh <take sNN> <branch> <first_g> <cuts comma list>   -> scratch gate dir with take.mkv, qa, rhythm, f6 frames (named by film g)
T=$1; B=$2; FG=$3; CUTS=$4
G=/tmp/claude-0/-home-user-github-commit-quest-v2/d6912f88-c4cf-5bc4-981a-4123114734fd/scratchpad/gate/$T
R=/home/user/github-commit-quest-v2
cd $R && timeout 200 git fetch -q origin $B || exit 1
rm -rf $G && mkdir -p $G/f6 && git archive origin/$B film/v3/film17/$T | tar -x -C $G
D=$G/film/v3/film17/$T; cd $D && { [ -f take.mkv ] || cat take.mkv.part* > take.mkv; }
python3 $R/film/film17/rhythm.py take.mkv --first_g $FG --cuts $CUTS | tee $G/rhythm.txt
python3 $R/film/qa_auto.py take.mkv --first_g $FG --cuts $CUTS --out $G/qa > /dev/null; head -8 $G/qa/QA_AUTO.md
SEL="not(mod(n\,5))"; for c in $(echo $CUTS | tr , ' '); do l=$((c-FG-3)); h=$((c-FG+3)); SEL="$SEL+between(n\,$l\,$h)"; done
ffmpeg -v error -i take.mkv -vf "select='$SEL'" -vsync 0 -frame_pts 1 $G/f6/t%04d.png
cd $G/f6 && python3 -c "import os,sys;fg=int(sys.argv[1]);[os.rename(f,'g%04d.png'%(int(f[1:5])+fg)) for f in sorted(os.listdir('.')) if f.startswith('t')]" $FG; ls | wc -l

#!/bin/bash
# recut.sh N : re-cut the end of EP.N (1..7) — the "next" card is replaced by a teaser: 0.35 s black, then EP.N+1's climax (its cold-open moment,
# same T0/DUR as that episode's hook, no headline) with a "ตอนต่อไป · กดติดตาม / title" paper label, a sting + glitch/whoosh, fade to black.
# Source = the finished *-HQ-hook.mp4 (keeps its own cold open); one re-encode (crf 16) → *-HQ-hook2.mp4; the caller verifies, then replaces.
W=/tmp/claude-0/-home-user-github-commit-quest-v2/49762ff1-991c-52d3-b168-9c16af55ac24/scratchpad/work
N=$1; M=$((N+1))
A=$(ls $W/hook/EP$N-*-HQ-hook.mp4 | head -1); B=$(ls $W/fence$M/EP$M-*-HQ.mp4 | head -1)
base=$(basename "$A" -HQ-hook.mp4)
declare -A OFF=([1]=1.6 [2]=1.839 [3]=2.5 [4]=2.283 [5]=1.857 [6]=1.9 [7]=1.904)      # cold-open length in front of the episode
declare -A TN=([1]=141.49 [2]=159.74 [3]=177.63 [4]=188.81 [5]=182.62 [6]=153.76 [7]=108.49)   # start of the "next" card (schedule.json)
declare -A T0=([2]=78.80 [3]=128.40 [4]=98.67 [5]=65.10 [6]=100.75 [7]=36.0 [8]=66.3)         # the next episode's climax (its hook moment)
declare -A DU=([2]=1.82 [3]=2.5 [4]=2.28 [5]=1.85 [6]=1.9 [7]=1.9 [8]=1.9)
tcut=$(python3 -c "print(round(${OFF[$N]}+${TN[$N]},3))"); t0=${T0[$M]}; d=${DU[$M]}; gap=0.35
lab=$W/hook/next$N.png; sfx=$W/hook/tease$N.wav; out=$W/hook/$base-HQ-hook2.mp4
fo=$(python3 -c "print(round($d-0.22,3))"); bfo=$(python3 -c "print(round($tcut-0.25,3))")
AF="aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo"
nice -n 10 ffmpeg -nostdin -loglevel error -y -i "$A" -ss $t0 -t $d -i "$B" -i "$lab" -i "$sfx" -f lavfi -i "color=c=black:s=1080x1920:r=60:d=$gap" -f lavfi -i "anullsrc=r=48000:cl=stereo:d=$gap" -filter_complex "[0:v]trim=0:$tcut,setpts=PTS-STARTPTS,format=yuv420p[bv];[0:a]atrim=0:$tcut,asetpts=PTS-STARTPTS,$AF,afade=t=out:st=$bfo:d=0.25[ba];[4:v]format=yuv420p[gv];[5:a]$AF[ga];[1:v]setpts=PTS-STARTPTS[tv0];[tv0][2:v]overlay=0:0,fade=t=in:st=0:d=0.12:color=black,fade=t=out:st=$fo:d=0.22:color=black,format=yuv420p[tv];[1:a]asetpts=PTS-STARTPTS,$AF[ta0];[3:a]$AF,lowpass=f=14000,volume=0.9[ts];[ta0][ts]amix=inputs=2:duration=first:normalize=0,lowpass=f=18000,alimiter=limit=0.84:attack=0.5:release=60:level=disabled:latency=1,afade=t=out:st=$fo:d=0.22,$AF[ta];[bv][ba][gv][ga][tv][ta]concat=n=3:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 16 -r 60 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 256k -movflags +faststart "$out" || { echo "recut EP$N failed"; exit 1; }
want=$(python3 -c "print(round($tcut+$gap+$d,2))")
echo "EP$N tcut $tcut teaser EP$M@$t0+$d want $want got $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out") frames $(ffprobe -v error -count_packets -select_streams v:0 -show_entries stream=nb_read_packets -of csv=p=0 "$out") size $(ls -l "$out" | awk '{print $5}')"
echo "RECUT$N DONE"

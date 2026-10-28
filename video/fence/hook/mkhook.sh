#!/bin/bash
# mkhook.sh IN.mp4 OUT.mp4 T0 DUR OVERLAY.png SFX.wav [FADEIN] : prepend a cold-open (IN[T0, T0+DUR] + headline overlay, fading to black) and re-encode the whole episode
# FADEIN (s, default 0): fade the episode's own opening in from black — use it when the episode does not open on black (EP.5), otherwise the dip ends in a hard cut to a bright frame
# the hook audio (episode audio + glitch/whoosh) is band-limited and limited to -1.5 dBFS: the glitch on top of loud dialogue went over 0 dBFS (EP.2 +0.6),
# and its sharp transients overshoot again inside AAC unless they are low-passed before the limiter
in=$1; out=$2; t0=$3; dur=$4; ov=$5; sfx=$6; fi=${7:-0}
fo=$(python3 -c "print(round($dur - 0.18, 3))")
mvf="setpts=PTS-STARTPTS"; [ "$fi" != "0" ] && mvf="$mvf,fade=t=in:st=0:d=$fi:color=black"
nice -n 15 ffmpeg -nostdin -loglevel error -y -i "$in" -ss $t0 -t $dur -i "$in" -i "$ov" -i "$sfx" -filter_complex "[1:v]setpts=PTS-STARTPTS[hv];[hv][2:v]overlay=0:0,fade=t=out:st=$fo:d=0.18:color=black,format=yuv420p[hookv];[1:a]asetpts=PTS-STARTPTS,aresample=48000[ha];[3:a]aresample=48000,aformat=channel_layouts=stereo,lowpass=f=14000,volume=0.9[gs];[ha][gs]amix=inputs=2:duration=first:normalize=0,lowpass=f=18000,alimiter=limit=0.84:attack=0.5:release=60:level=disabled:latency=1[hooka];[0:v]$mvf,format=yuv420p[mv];[0:a]asetpts=PTS-STARTPTS[ma];[hookv][hooka][mv][ma]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 16 -r 60 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 256k -movflags +faststart "$out" && ffprobe -v error -show_entries stream=nb_frames:format=duration -of compact "$out"

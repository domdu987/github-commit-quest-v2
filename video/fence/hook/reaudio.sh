#!/bin/bash
# reaudio.sh HQ-HOOK.mp4 MIX.wav T0 DUR SFX.wav OUT.mp4 : swap a new episode mix into a finished *-HQ-hook.mp4 without touching its video
# (stream copied bit for bit — no re-render, no second x264 generation). The audio is rebuilt with mkhook.sh's own chain:
# cold open = MIX[T0, T0+DUR] + SFX (lp 14k, x0.9), lp 18k, limiter 0.84 · then the whole MIX. Checked on EP.6: lag 0 samples vs mkhook.sh
hq=$1; mix=$2; t0=$3; dur=$4; sfx=$5; out=$6
ffmpeg -nostdin -loglevel error -y -i "$hq" -ss $t0 -t $dur -i "$mix" -i "$sfx" -i "$mix" -filter_complex "[1:a]asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[ha];[2:a]aresample=48000,aformat=channel_layouts=stereo,lowpass=f=14000,volume=0.9[gs];[ha][gs]amix=inputs=2:duration=first:normalize=0,lowpass=f=18000,alimiter=limit=0.84:attack=0.5:release=60:level=disabled:latency=1[hooka];[3:a]asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[ma];[hooka][ma]concat=n=2:v=0:a=1[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 256k -movflags +faststart "$out" && ffprobe -v error -show_entries stream=nb_frames:format=duration -of compact "$out"

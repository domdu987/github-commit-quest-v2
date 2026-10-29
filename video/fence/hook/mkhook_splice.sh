#!/bin/bash
# mkhook_splice.sh RAW.mp4 MIX.wav OUT.mp4 T0 DUR OVERLAY.png SFX.wav FADEIN SPLICE_DIR N0 : mkhook.sh straight from the render (raw video + mix.wav, one encode),
# with the episode's frames from N0 on replaced by the PNG frames in SPLICE_DIR (one per 1/60 s, sorted by the time in their names) — a fix to the
# last shot without rendering the whole episode again (cut inside a black frame so the two captures cannot show a seam)
raw=$1; mix=$2; out=$3; t0=$4; dur=$5; ov=$6; sfx=$7; fi=$8; sd=$9; n0=${10}
W=/tmp/claude-0/-home-user-github-commit-quest-v2/49762ff1-991c-52d3-b168-9c16af55ac24/scratchpad/work
seq=$W/hook/_splice; rm -rf $seq; mkdir -p $seq
python3 -c "import glob,re,sys,os; fs=glob.glob(sys.argv[1]+'/frame-*.png'); fs.sort(key=lambda f: float(re.search(r'at-([0-9.]+)s', f).group(1))); [os.symlink(f, '%s/%05d.png' % (sys.argv[2], i)) for i, f in enumerate(fs)]; print(len(fs), 'splice frames')" $sd $seq
fo=$(python3 -c "print(round($dur - 0.18, 3))")
fin=""; [ "$fi" != "0" ] && fin=",fade=t=in:st=0:d=$fi:color=black"
nice -n 15 ffmpeg -nostdin -loglevel error -y -i "$raw" -ss $t0 -t $dur -i "$raw" -i "$ov" -i "$sfx" -i "$mix" -ss $t0 -t $dur -i "$mix" -framerate 60 -i $seq/%05d.png -filter_complex "\
[1:v]setpts=PTS-STARTPTS[hv];[hv][2:v]overlay=0:0,fade=t=out:st=$fo:d=0.18:color=black,format=yuv420p,setsar=1[hookv];\
[5:a]asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[ha];[3:a]aresample=48000,aformat=channel_layouts=stereo,lowpass=f=14000,volume=0.9[gs];\
[ha][gs]amix=inputs=2:duration=first:normalize=0,lowpass=f=18000,alimiter=limit=0.84:attack=0.5:release=60:level=disabled:latency=1[hooka];\
[0:v]trim=end_frame=$n0,setpts=PTS-STARTPTS,format=yuv420p,setsar=1[m1];[6:v]scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,setsar=1,setpts=PTS-STARTPTS[m2];\
[m1][m2]concat=n=2:v=1:a=0$fin,format=yuv420p[mv];[4:a]asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[ma];\
[hookv][hooka][mv][ma]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 16 -r 60 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 256k -movflags +faststart "$out" && ffprobe -v error -show_entries stream=nb_frames:format=duration -of compact "$out"

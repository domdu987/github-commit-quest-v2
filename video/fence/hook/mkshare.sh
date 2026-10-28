#!/bin/bash
# mkshare.sh IN-HQ.mp4 OUT-share.mp4 : the small copy kept in the repo (2.8 Mbps video, AAC 160k)
# audio: low-pass 15 kHz + limiter -2 dBFS before AAC — without them the hook glitch decoded at +1.2 dBFS (AAC overshoot on sharp transients)
nice -n 15 ffmpeg -nostdin -loglevel error -y -i "$1" -c:v libx264 -preset medium -b:v 2800k -maxrate 3200k -bufsize 6000k -pix_fmt yuv420p -af "lowpass=f=15000,alimiter=limit=0.79:attack=0.5:release=60:level=disabled:latency=1" -c:a aac -b:a 160k -movflags +faststart "$2" && ls -l "$2" | awk '{print $5, $9}'

#!/bin/bash
# Mix the three long-version parts with one unbroken score (each part's suno1 starts where the previous part ended), join them
# sample-exact into the film's mix and stems, and run musiccheck + hisscheck on the film.
#   tools/mixall.sh [out dir]      default out: /dev/shm/phrailong/mix
set -euo pipefail
W="$(cd "$(dirname "$0")/.." && pwd)"; OUT="${1:-/dev/shm/phrailong/mix}"; Q=/home/user/github-commit-quest-v2/.claude/skills/rodmai-club-video/scripts
off=0
for e in 1 2 3; do
  (cd "$W/ep$e" && MUSOFF=$off MIXOUT="$OUT/ep$e" python3 mix.py | tail -1)
  off=$(python3 -c "import json; print($off + json.load(open('$W/ep$e/schedule.json'))['total'])")
done
for f in mix vo_stem music_stem; do
  c=pcm_s16le; [ "$f" != mix ] && c=pcm_f32le
  ffmpeg -v error -y -i "$OUT/ep1/$f.wav" -i "$OUT/ep2/$f.wav" -i "$OUT/ep3/$f.wav" -filter_complex "[0:a][1:a][2:a]concat=n=3:v=0:a=1" -c:a $c "$OUT/film_$f.wav"
done
echo "film: $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/film_mix.wav") s"
ffmpeg -nostats -i "$OUT/film_mix.wav" -af ebur128=peak=true -f null - 2>&1 | grep -A12 Summary | grep -E "I:|Peak:" || true
python3 -I "$Q/musiccheck.py" "$OUT/film_vo_stem.wav" "$OUT/film_music_stem.wav" | sed -n 1,5p || true
python3 -I "$Q/hisscheck.py" "$OUT/film_mix.wav" --vo "$OUT/film_vo_stem.wav" || true
python3 -I "$Q/hisscheck.py" "$OUT/film_mix.wav" || true

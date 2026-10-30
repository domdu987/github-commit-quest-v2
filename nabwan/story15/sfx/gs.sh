#!/bin/bash
# gs.sh "name|text|seconds": fal ElevenLabs sound effect -> sfx/name.wav (44.1k mono)
IFS='|' read -r N T D <<< "$1"; cd "$(dirname "$0")"
python3 -c "import json,sys;json.dump({'text':sys.argv[1],'duration_seconds':float(sys.argv[2]),'prompt_influence':0.55},open('req_'+sys.argv[3]+'.json','w'))" "$T" "$D" "$N"
for i in 1 2 3 4; do
  curl -sS -m 180 -X POST https://fal.run/fal-ai/elevenlabs/sound-effects/v2 -H 'Content-Type: application/json' -d @req_$N.json > res_$N.json
  U=$(python3 -c "import json;print(json.load(open('res_$N.json'))['audio']['url'])" 2>/dev/null) && curl -sS -o $N.mp3 "$U" && break
  sleep $((i*3))
done
[ -s $N.mp3 ] || { echo "FAIL $N $(head -c 200 res_$N.json)"; exit 1; }
ffmpeg -loglevel error -y -i $N.mp3 -ar 44100 -ac 1 $N.wav && echo "OK $N"

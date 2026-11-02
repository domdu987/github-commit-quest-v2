#!/bin/bash
# gen.sh KEY TEMPO : req_KEY.json -> res_KEY.json -> KEY.wav, KEY44.wav (tempo), KEY16.wav (16 kHz mono)
K=$1; T=${2:-1.2}; cd "$(dirname "$0")"
for i in 1 2 3 4; do
  curl -sS -m 180 -X POST https://fal.run/fal-ai/gemini-3.1-flash-tts -H 'Content-Type: application/json' -d @req_$K.json > res_$K.json
  U=$(python3 -c "import json;print(json.load(open('res_$K.json'))['audio']['url'])" 2>/dev/null) && [ -n "$U" ] && curl -sS -m 120 -o $K.wav "$U" && break
  sleep $((i*3))
done
[ -s $K.wav ] || { echo "FAIL $K: $(head -c 300 res_$K.json)"; exit 1; }
ffmpeg -loglevel error -y -i $K.wav -af "atempo=$T" -ar 44100 -ac 1 ${K}44.wav
ffmpeg -loglevel error -y -i ${K}44.wav -ar 16000 -ac 1 ${K}16.wav
echo "OK $K $(ffprobe -v error -show_entries format=duration -of csv=p=0 ${K}44.wav)"

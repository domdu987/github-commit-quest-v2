#!/bin/bash
# record every segment (fal Gemini TTS, cached by text+style+take) then Whisper QA each one
set -u
cd "$(dirname "$0")/.."
export WHISPER_DIR=${WHISPER_DIR:-/tmp/claude-0/-home-user-github-commit-quest-v2/dadc119d-850b-549d-82c6-f1e8a1f13306/scratchpad/whisper}
for s in ep1 ep2 ep3 bridges; do
  echo "== $s"; python3 tools/voice.py $s/lines.json $s/vo 2>&1 | grep -E "^tts|retry|recorded|total|Error" 
done
for s in ep1 ep2 ep3 bridges; do echo "== QA $s"; python3 tools/voice_qa.py $s/lines.json $s/vo 2>&1 | grep -vi warn | tail -60; done

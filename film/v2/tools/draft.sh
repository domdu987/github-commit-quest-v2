#!/bin/bash
# draft.sh -- fast review build: dsf 1, JPEG intermediates, no captions.  usage: [SHOTS=shots/s01.py] tools/draft.sh
set -e
V2="$(cd "$(dirname "$0")/.." && pwd)"
cd "$V2"
python3 build.py "${SHOTS:-shots/s01.py}" > /dev/null
node render.js out/manifest.json --dsf 1 --jpg | tail -1
python3 post.py | tail -1
python3 tools/qa_check.py

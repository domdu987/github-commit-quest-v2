#!/usr/bin/env bash
# สร้างวิดีโอทั้งเรื่องตั้งแต่ต้น (ข้ามขั้นที่มีไฟล์แคชแล้ว)
set -euo pipefail
cd "$(dirname "$0")"
node audio/tts.js        # เสียงบรรยาย (fal.ai MiniMax) → audio/clips, durations.json
node audio/timeline.js   # ไทม์ไลน์ + voice.wav
node audio/align.js      # ซับไตเติลจับเวลา (fal.ai Whisper) → cues.json, scenes/timeline.data.js
node audio/sfx.js        # SFX (fal.ai stable-audio-25) → audio/sfx
node audio/mix.js        # mix.wav
node render/render.js --workers "${WORKERS:-4}"   # เฟรม + MP4 → out/zombie-pump-ep1.mp4

#!/bin/bash
# resumable: render.py skips frames already written (> 50 kB)
cd "$(dirname "$0")/../../../.."
until [ "$(ls film/v3/film17v2/T8/frames/g_*.png 2>/dev/null | wc -l)" -ge 191 ]; do
  python3 film/v3/film17v2/T8/render.py range 1862 2052 film/v3/film17v2/T8/frames >> /tmp/t8_render.log 2>&1 || sleep 5
done

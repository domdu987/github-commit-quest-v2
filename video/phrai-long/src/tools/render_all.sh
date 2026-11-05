#!/bin/bash
# Render the three long-version parts one after another (detached: setsid nohup bash tools/render_all.sh &).
# Writes /dev/shm/phrailong/rN.mp4, renderN.log, and renderN.done holding the exit code.
mkdir -p /dev/shm/tmp
for e in 1 2 3; do
  cd /dev/shm/phrailong/build$e || exit 1
  TMPDIR=/dev/shm/tmp npx --yes hyperframes@0.8.185 render -f 60 -o /dev/shm/phrailong/r$e.mp4 > /dev/shm/phrailong/render$e.log 2>&1
  echo $? > /dev/shm/phrailong/render$e.done
done

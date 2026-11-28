#!/bin/bash
# the remaining renders, one at a time (2 threads, nice 5): walk, turnaround, faces, final hook frames (both view modes)
cd /tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09/v16/block
DZ09_CAST=block nice -n 5 python3 walk_kong.py --frames 72 > out/walk.log 2>&1; echo walk $?
nice -n 5 python3 turnaround.py --spp 28 --h 760 > out/turn.log 2>&1; echo turn $?
nice -n 5 python3 faces.py --spp 16 --px 280 > out/faces.log 2>&1; echo faces $?
cd hookcopy
DZ09_CAST=block BLOCK_VIEW=ignore nice -n 5 python3 run.py --frames 636,1030,1049 --tier final --size 720x1280 --threads 2 --tag block --force > ../out/final_block.log 2>&1; echo hook1 $?
DZ09_CAST=block BLOCK_VIEW=compat nice -n 5 python3 run.py --frames 1030,1049 --tier final --size 720x1280 --threads 2 --tag block_compat --force > ../out/final_block_compat.log 2>&1; echo hook2 $?
echo ALLDONE

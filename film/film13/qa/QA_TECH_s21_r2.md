# QA_TECH s21 round 2 - FAIL (one blocking issue)
Checked: qa_auto every frame, 6 fps sheets + cut frames + full-size crops, joins with neighbours (s26 older version, rough only). Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qa13b3/<take>/ and /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qa13b3/j/ . Take files untouched.
Auto: PASS (66 frames, no frozen/pop/blur).
Round-1 issues: 2 FIXED (enclosed timber cellar, beam ceiling, lamps, same space as s20/s22). 3 FIXED (no sky). 4 mouths FIXED (closed/hidden), thick blue bars all at one angle and swinging together at g ~1370-1382 (readable).
1. STILL BLOCKING g 1356-1380 (and again as dark slabs under pads g ~1395-1421): stray geometry bottom-left, a dark navy brick-textured slab / box lying on the mud at the frame edge (x 0-160, y 1000-1280) plus a hard-edged dark hex/wedge mesh hanging under the jack pads (g 1395+, bottom right) and small white shards (g ~1405+). Same defect as round 1 issue 1, not removed. Fix: hide the debris/shadow-box mesh, re-render g 1356-1421.
Non-blocking: g 1356-1385 bottom 35 % is bare mud with pockmark rings before the camera drops in; at g ~1376-1380 the hex bar end-cap covers a worker's face. Heads y 570-700 (<880).
Joins: s20 -> s21 cellar -> cellar OK; s21 -> s22 OK.

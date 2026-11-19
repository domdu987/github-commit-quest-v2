# QA_TECH s17 round 2 - PASS
Checked: qa_auto every frame (planned cuts passed), own frame-diff/pop scan, 6 fps sheets + cut +-3 frames, full-size key frames, joins with neighbours. Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qa13b2/s17/ (sheet_*.jpg, full/). Take files untouched. G1 cut offset: now FIXED in all re-renders (pops/cuts sit exactly on the plan g: s17 1173/1255, s26 1743/1775/1871/1909); qa_auto's 'no change' on in/out handle boundaries is expected.
Auto: PASS (no frozen/blur). My scan: pops only at g 1173 (17->18) and g 1255 (18->19), both exactly on the plan.
Round-1 notes: 1 (time-of-day) unchanged and still non-blocking: sky is the same bright blue; no morning cue. 2 FIXED in framing: rich is now a three-quarter figure at the window glass (sun/shade, painting + wallpaper at left, rug <= 30 %), cup visible at chest (still no hand on the cup; non-blocking). 3 shot 18 unchanged and good (tea disc visible, still, push-in). 4 FIXED: shot 19 now a three-figure line-up with chandelier, window and clear gaps; rich on the open left side with the cup raised on a straight arm, no overlap with the gentleman.
Q2 lip-sync (window g 1255-1300 +-4): mouth closed g 1255-1264, open/moving g 1265-1299, closed again by g 1304. OK. Mouths of guests closed (lady smiling, gentleman grim).
Non-blocking notes:
1. g 1262-1305 (shot 19): rich is pushed to the left edge, the saucer of the raised cup touches/clips the frame edge (x 0-45 px). Fix: shift 0.3 D right.
2. g 1110-1172 chair/armchair from plan not present (he stands); no continuity issue with s20 as he is absent there.
Heads < 880 (rich 560-760 in shot 19). No text. Join s16 -> s17 OK, s17 -> s20 (suite -> cellar) hard cut OK.

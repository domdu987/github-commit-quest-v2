# QA take s32 (film 15, shots 32-36, g 1804-2095, KEY take: ending)
- take.mkv.part* (cat them to rebuild take.mkv): g 1796-2101, 306 frames, 720x1280, 12 samples, OIDN, no DOF. ~8.2 s wall per frame (2 processes x 2 threads).
- Locations: B DAY (32-33), A GOLDEN (34-36), one process each. The 33->34 dissolve (g 1934-1944, 11 frames) is baked into the take; the 32 dissolve-in has 8 handle frames (1796-1803); 6 handle frames after 2095.
- qa_auto: PASS (soft frames only at the dissolve; the whip 35 no longer flagged). motion_check: median 4.6, p90 15.6 (32 3.9/5.0, 33 3.6/5.1, 34 5.0/7.5, 35 14.4/20.6, 36 6.8/23.1).
- Director fixes (round 2): shot 34 camera slides right so the pole clears the coach, plus a sigh (shoulder drop, head shake); shot 35 camera closer (coach larger) with a back turn on the plant; shot 36 camera closer and lower, coach sunk to the chin on top of the mound in front of the boys, dazed/sheepish face, raised wobbling thumbs-up from g 2056, boys laugh with the 3 Hz bounce. The raised arm is limited by the puppet arm reach (thumb ends about head height).
- Checked by eye at 6 fps (contact.jpg): heads above y 880; flops read (head and legs hang below the bar); three kits land, sit up smiling, thumbs up; coach buried to the chin with spray in the air and boys laughing; no mouth movement (no quote window in this take).
## Differences from the plan
- Cameras of 32, 33, 34, 36 are my own (closer than the plan so the flop and the buried coach read); 35 is a per-frame camera that follows the coach (whip), no hurdle FG. Shot 33 looks from the left over the foam, not from the plan camera.
- Shot 34 coach stands at the pit's left edge in front of the bench, not on the sawdust pile. Boys stand on the pit sand in 36.
- Median motion in 32-34 is just above 3.5 (camera slide + breathing); whole-take median 4.4.
- Round 3 (shot 36 only, g 2040-2101 re-rendered): coach sunk 0.3 D more (sawdust at his chin), raised thumb drawn 1.3x larger. Sneakers not added. Motion median 4.5 / p90 15.6, qa_auto PASS.

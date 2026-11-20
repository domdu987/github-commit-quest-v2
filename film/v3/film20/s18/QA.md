# s18 = T18 camera-travel take (shots 18+19+20), TOWER dusk 1909 (render team 8) -- round 3 (TAKE2_ART + TAKE2_B)
One continuous take, g 1221-1430, first_g 1210 (11 handle frames, DIS 17 in), 4 out-handle frames g 1431-1434 (hard cut out), 225 frames, 720x1280, 8 spp, no DOF.
take.mkv is 96 MB: committed as take.mkv.part{aa,ab,ac} (cat to rebuild); the full file is git-ignored. s19/s20 folders deleted.

## Travel
g 1210-1303 dusk, closer + low camera, wagon (moved 5 m toward the group) with horse + crowbars, old Eiffel worried (calm->worried on the blink g 1254), push + orbit + tilt + 2 snaps | g 1304-1342 he points up, camera CRANES (fast start so he leaves frame quickly) to 30 m tilting up | g 1343-1360 WHIP-TILT down the wires to the post | g 1361-1390 DIVE to the hut window (lit glass hidden from g 1384) | g 1390-1399 THROUGH the window between wall battens (x 1.1 m) | g 1399-1434 soldier taps, 5 taps.

## Round-4 fixes (TAKE3_B + TAKE3_ART)
- Ground g 1210-1300: the avenue is dressed (planks lying flat, rope coils, barrels/crates at the sides, a gas lamp with a warm point light), the set's jagged rope-coil ring (wagon_rope, cut the group at the waist g 1255-1300) is hidden; wagon, horse, crowbars stay. Opening is faster (push 20 %/s, slide -35 px/s, orbit -6 deg/s, tilt -5.5 deg/s).
- Window: the lit glass + muntin object are hidden from g 1372 and a warm lamp inside makes the hole glow (no blown white pane); the dive is now arc-length parametrised with ease-IN only, so the camera crosses the window plane at speed (g 1392) and brakes inside; passes between the battens (x 1.1 m).
- Inside: the aim is shifted so the telegraphist sits fully in the left third (head 166-214 px, never cut); desk less blown (exposure +0.15, lamp 7, rim 3).
- Earlier rounds: wire stay to a ground stake, own Morse key under his hand with a dipping lever, blue spark arc + cool flash.

## Numbers
- QA_AUTO: PASS (soft frames g 1390-1395 only, the 6 frames of the crossing; no pops).
- qa_stats2: sat 0.603, vivid 58.5 %, luma 99.4, motion median 4.14, p90 17.87, still 3.4 %.
- own frame-diff (in-shot g 1222-1430): median 4.04, p90 20.9. s/frame 8.67 wall, 16.69 cpu.

## Known weak
Ground is still ~35 % of the first frames (heads must stay above y 880); coils read as flat discs; no "T.S.F." sign; the soldier's key hand is small; 6 soft frames at the crossing.

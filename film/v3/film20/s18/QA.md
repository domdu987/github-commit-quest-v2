# s18 = T18 camera-travel take (shots 18+19+20), TOWER dusk 1909 (render team 8)
One continuous take, g 1221-1430 (40.70-47.71 s), first_g 1210 (11 handle frames for DIS 17 in), 4 out-handle frames g 1431-1434 (hard cut out), 225 frames, 720x1280, 8 spp, no DOF.
take.mkv is 100 MB: delivered as take.mkv.part{aa,ab,ac} (cat them to rebuild).
Old s19/s20 folders deleted (merged into this take).

## Travel
g 1210-1303 dusk, wagon, old Eiffel worried (calm->worried on the blink at g 1254), push 20 %/s + orbit + tilt + 2 snaps | g 1304-1342 he points up on "ไอเฟลเลยขึง", camera CRANES to 30 m tilting up the tower + wires | g 1343-1360 WHIP-TILT down the wires to the post on "จากยอดหอ ลงมาถึงพื้น" | g 1361-1394 DIVE to the hut's lit window | g 1390-1410 THROUGH the window (glass panel hut_lampsm hidden) | g 1410-1434 soldier taps the Morse key, 5 taps, spark gap flashes (own jagged arc between the brass balls), push.
Not done: the optional "T.S.F." sign on the hut.

## Numbers
- qa_stats2: sat 0.618, vivid 56.2 %, luma 97.9, motion median 4.94 p90 22.36, still 3.7 %.
- own frame-diff (in-shot, 90x160): median 5.79, p90 22.07 (target 4 / 12: met).
- s/frame 8.66 wall, 16.74 cpu (2 processes x 2 threads).
- QA_AUTO: PASS (see QA_AUTO.md); planned-cut note only.

## Fixes carried from the TAKE gate
antenna last-segment bug fixed at runtime (wires reach the post), warm low sun for a lit avenue with cast shadows, preset FG / shade casters hidden (no torn plank), wagon with wheels + horse + crowbars readable, hands on the key, duplicate headphones removed, exposure +0.35 inside (luma ok).
Known weak: the ground is still ~40 % of the first 90 frames (heads must stay above y 880); window crossing frames g 1388-1396 are close-ups of lit panes and wall battens (about 8 frames); plank moire faint on the hut ceiling; eiffel head 52-125 px.

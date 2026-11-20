# s18 = T18 camera-travel take (shots 18+19+20), TOWER dusk 1909 (render team 8) -- round 3 (TAKE2_ART + TAKE2_B)
One continuous take, g 1221-1430, first_g 1210 (11 handle frames, DIS 17 in), 4 out-handle frames g 1431-1434 (hard cut out), 225 frames, 720x1280, 8 spp, no DOF.
take.mkv is 96 MB: committed as take.mkv.part{aa,ab,ac} (cat to rebuild); the full file is git-ignored. s19/s20 folders deleted.

## Travel
g 1210-1303 dusk, closer + low camera, wagon (moved 5 m toward the group) with horse + crowbars, old Eiffel worried (calm->worried on the blink g 1254), push + orbit + tilt + 2 snaps | g 1304-1342 he points up, camera CRANES (fast start so he leaves frame quickly) to 30 m tilting up | g 1343-1360 WHIP-TILT down the wires to the post | g 1361-1390 DIVE to the hut window (lit glass hidden from g 1384) | g 1390-1399 THROUGH the window between wall battens (x 1.1 m) | g 1399-1434 soldier taps, 5 taps.

## Round-3 fixes
1 closer start (Eiffel head 70 -> 123 px, officer 60+), low camera 0.3 m, wagon in frame, warm low sun + cast shadows, props moved to the sides (no barrel in the lens); ground ~30 %. | 2 crane: fast ease-out start. | 3 wire: a stay wire from the anchor post top (6.2 m) to a ground stake. | 4 crossing: path x moved to 1.1 m (battens are at 0.2/0.8/1.4 m, the earlier x 0.7-0.8 hit one), muntin/dark object + glass hidden, crossing sped up. | 5 hand: card prop removed, own brass Morse key under the soldier's right hand (hand_r anchor), lever dips on each tap. | 6 spark: blue arc (hue ~210) between the brass balls, cool point flash (55 W) keyed on taps + a faint cool rim light inside.

## Numbers
- QA_AUTO: PASS (notes: soft frames g 1384-1394 = the window crossing, flat planks; pops g 1383-1384 = the glass-off + dive).
- qa_stats2: sat 0.639, vivid 61.9 %, luma 95.8. Its motion line (median 2.74 / p90 11.56) is thrown off by 17 'shots' it detects at the window pops; my own in-shot frame-diff (90x160, g 1222-1430, no handles): median 3.58, p90 25.2 (target 4 / 12).
- s/frame 8.92 wall, 17.24 cpu (2 processes x 2 threads).

## Known weak
Frame-diff median 3.6 (< 4) in the first 90 frames (small figures, smooth sky); soft frames at the window crossing (planks are low-contrast); ground still ~30 % early; soldier's hand/key is small (about 30 px); no "T.S.F." sign; the lit-window glass pops off at g 1384.

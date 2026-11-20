# QA_TECH s15

## Round 2 - FAIL
Checked: qa_auto PASS (g1190 cut not visible in range: continuous handle, expected), meta g0 1096/g1 1190 handles 10/9 DIS 15 OK, framediff 5.08 / 13.96 OK. Cards and camera ride the ship: horizon, rail and deck shadows stay locked to the cards, no sliding found. Sun overhead: the mast shadow shrinks and curls in over g1096-1180, reads OK. Mouths fixed (frown). Contact shadows under shoes present. Snap g1168-1184 on อยู่ตรงหัว (g1172) OK.
1. g1184-1190: William's hat brim and head touch/clip at the LEFT frame edge during the final hold (head x ~0). Fix: recentre the final settle ~0.15 m right.
2. g1160-1176: the captain is cut by the left edge (arm/body) during the snap. Fix: shift the captain mark right or loosen the push.
3. NOTE: William looks at the lens, not up at the sun; the quadrant is raised at the forehead tilted aside rather than aimed straight up. Not blocking at phone size.

## Round 4: PASS
Checked 6 fps (take g1086-1198), qa_auto PASS. No text, black/magenta, frozen, blur, mouths closed (frown). Frame-diff g1097-1189 median 4.54 / p90 12.27 OK. Ship ride (deck, rail, cards) consistent; sun overhead and the glare disc appear after the snap on "อยู่ตรงหัว".
Earlier issues: R2-1 (William hat at left edge at the end) FIXED, William now at right with face inside; R2-2 (captain cut by left edge) FIXED: captain fully inside until g1160; at g1176-1189 his hat brim touches the left edge (face and body inside) = NOTE; R2-3 NOTE: William now squints up with the quadrant raised, OK.
Notes: William's quadrant tip / hat brim touches the right edge g1181-1189 (face intact). Captain feet shadows present.

## Round 10 (director QA-tech): FAIL (1 blocker: William's eyes)
Take: s15 take.mkv.partaa+partab, 720x1280, 203 frames, g1086-1288 (frame = g-1086). Frames in /tmp/qa19_r10/s15/g####.png (every frame g1086-1288; 6 fps sheet and per-frame crops reviewed).

Frame-diff (mine): 90x160 grey, bilinear (ffmpeg scale flags=bilinear), mean abs diff of consecutive pairs (g-1,g). Range g1096-1279: pairs (1096,1097)..(1278,1279) = 183 pairs. Median 4.86, p90 10.10, min 1.43 (limits >=4 / >=10: OK). Other ranges: g1086-1288 (202 pairs) median 4.69, p90 9.78; g1190-1279 only (s16 half, 89 pairs) median 2.93, p90 9.03. The team/director 9.03 equals my s16-only range, so it was measured on a different span than g1096-1279 (p90 is just over the 10 limit on the full in-shot range, 10.10). Last round's 11.18 was a different range/scale than this one; not reproduced. No pair < 1.0 anywhere g1150-1288, no black frames (min mean luma 91), no frozen runs.

Round 9 blockers
1. Sun disc: FIXED. Per-frame check g1150-1288: halo rises from g1156, core disc appears g1163 (1230 px >=245) and g1164 (5796 px, i.e. pops to full size within 2 frames), steady 7000-7650 px afterwards, no blink at g1207-1229 (small 6 percent dip g1204-1206 and g1213-1215 where the glide passes behind rigging, no gap). Disc is round, soft halo, no square edge in crops g1154-1172, 1205, 1214, 1230. Note only: at g1161 the halo lights the hard-edged blue sky patch behind it as a pale rectangle (scene geometry, not the overlay).
2. William's glance: NOT FIXED. Eyes are open (round pupils) only from g1248 to g1288 (with one blink g1270-1272). From the H4 reveal (g~1204) to g1247 they are still flat half-lid slits with a frown, so g1238-1247 of the glance window g1238-1262 is still closed-looking and the "eyes open through the H4 phase" request is met for only the last 41 frames. Also at g1248 the mouth snaps from the frown to an open O and stays open to g1288 (a hard state change; no talking cycle, but it reads as a mouth open on the pop). Fix: switch William to the open-eye expression at g1238 or earlier (ideally from g1204), and blend/hold the mouth.

Polish checks
- Sun x: 565-575 at g1166-1190 (about 560 at g1190), glides left from g1194 to x 359 (top-centre) by g1228, steady after: OK.
- Diagonal sail shadow: fades out by g1172 (strong at g1164-1170, none from g1172): OK.
- Captain's hat brim distance from left edge g1218-1288: about 50-60 px (min about 50 at g1229-1232): OK.

Usual checks: no character cut by the frame edge, faces about 16-20 percent of height (under 35), heads at about y 500-700 (above 880), feet on deck with contact shadows (nothing floating), no props through faces, no pops/black/frozen frames. Sun disc fast ramp g1163-1164 is the only near-pop. Characters hold near-idle poses after g1229 but the camera keeps drifting and faces change, no still run over 1.5 s found in the frame-diff.

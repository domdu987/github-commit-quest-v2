# QA-art sH2b v3 (TAKE gate, team10 4cc1296)
Take: gate/sH2b/film/v3/film21/sH2b/take.mkv (g1389-1522, 134 frames, BIGZOOM 2 + CU3). Viewed: every 5th frame (f6/) at full size, every frame g1486-1496 (the look and the double take), full-size crops of P_TOP, the team's contact and phone sheets. Also compared H2b g1389/1392/1395 against H2a v3 (approved) at the same g, for the D6. Levels and the lemon cast are left to the conform. Rim light is ruled on at FINAL. The violet tents (g1425-1480) are known and handled separately; noted, not failed.

## Verdict: FIX-FIRST

The v2 blocker is fixed: from g1489 the trapped army, the bridge and the blue saltire wall stand as a big band behind the pair, Cressingham points, and the blink-and-swap double take with sweat drops lands right on "อยู่อีกฝั่ง". The BIGZOOM is a good §H move. But the new set state broke the P_TOP start: the armies do not match H2a inside the D6 dissolve (B1 below).

## v2 item
| v2 item | status |
|---|---|
| B1 "ได้แต่ยืนดู" sound-off | FIXED (via staging, option b). At g1499-1519 the far bank reads: blue saltire wall plus a crimson-and-blue rank row (rank row about 5 % of frame height, the whole far-bank band with banners about 15-18 %), bridge on the right. Pointing g1484-1493, blink g1492-93, shocked swap g1494-96, sweat drops. Option a (over-the-shoulder look) only partly done: see N1. |
| N1 empty field | FIXED (the approach crosses the camp; now tent-heavy instead, see N3) |
| N2 Surrey hidden | FIXED (Surrey beside Cressingham, face visible to g1519) |
| N3 Cressingham findable at P_TOP | NOT DONE (non-blocking, carried as N4) |

## qa_auto "suspected blur" ruling: FALSE POSITIVE
The 32 flagged frames (g1389-1420 and the tent pass) are not soft. At full size the tent stripes, flag poles, bridge planks and soldier cards have hard edges. The flag comes from low contrast: the take opens on the same dark, hazy exposure that H2a ends on (luma 116 at g1392, rising to 155 by g1422), and the top view has big flat areas. Edge energy divided by contrast is 0.23 at g1392-1420, the same as the approved H2a end (0.22-0.23) and the later aerial frames. There is no DOF or blur. The same false positive happened on the lawn in v2.

## Issues

**B1 (blocking), g1389-1395 (the D6 at P_TOP): the armies do not match H2a.** The camera matches H2a exactly at g1392, but the set state does not:
- The south-bank crimson block (the "other half" in front of the bridge foot among the tents, about 8 % of the frame in H2a) is GONE in H2b, and it does not appear anywhere later in the take.
- The trapped block inside the loop goes from H2a's solid crimson rectangle to sparse, thin red cones with a smudge shadow. It reads much weaker as "trapped army".
- The Scots cork changes from 2 banners plus a blue line to a 5-banner wall, the loop banners change (black and red-black flags are added), and the camp tents are re-laid out.
During a 6-frame dissolve this shows as whole regiments ghosting away. The story also loses its "other half" ("อีกครึ่ง ข้ามมาช่วยไม่ได้"), which needs the south-bank army.
Fix: render H2b on the same army and dressing state as H2a for at least g1389-1440: put back the south-bank crimson block and the solid loop block. The new 5-banner blue wall is better, so if you keep it, it must also go into H2a's tail g1386-1395 (only re-render H2a if that is cheaper). After that, H2a g1392 and H2b g1392 must be the same picture: a pixel MAD of about 1 or less, against 5.9 now. If the south-bank block cannot stay in the camp because of the swoop path, keep it at least through P_TOP and let it fall behind the camera.

**N1 (non-blocking), g1484-1493: the "look across" does not read as a look.** All faces stay frontal to the lens with half-lidded eyes, and Cressingham points to camera-right along the bank, not back across the water. The staging now carries the meaning, so this is not blocking. If cheap: a 3/4-back or profile head swap toward the far bank for about 8 frames before the blink, and point his arm up and back over his shoulder.

**N2 (non-blocking), g1499-1519: the top of the blue banner wall is cut by the top frame edge**, and a soldier is sliced at the left edge at g1514-1519. Tilt down about 3-5 % or lower the end lens target so the banner tops clear the frame. Feet stay just inside the bottom edge at g1519. Watch that through the handle.

**N3 (non-blocking, known set issue), g1464-1480: the tents dominate.** At g1470-1479 white and violet tent roofs fill the lower 40-50 % of the frame for about 0.4 s, and with the violet set shading they read as a purple mass. When the set fix is patched in, also either lift the path about 0.5 m over the plaza tents or start the arc a few frames later, so the pair and the river hold the frame.

**N4 (non-blocking), g1389-1420: Cressingham is still not findable at P_TOP.** The pair are dark specks at the south-bank waterline left of the bridge. A gold-and-crimson pennant at their spot would do it.

## Checks
- BIGZOOM: near-hold g1389-1421, descent g1422 to medium g1489, so wide to medium is about 3.2 s. PASS.
- Heads above y 880: pair heads y about 430-660 in the medium and CU3. PASS. Face size at CU3 (g1519): Cressingham's head about 14-15 % of the frame height, under the §G limit. PASS.
- Nothing floats: feet on the sand, barrel and props grounded. PASS.
- Colour story: English crimson/gold (Cressingham, Surrey's red-gold check, crimson rank), Scots blue saltire wall. PASS.
- No lip movement: the O-mouth swap holds static g1494-1519, and Cressingham does not speak. PASS.
- Bloodless. PASS.

## Scores
phone legibility 7 (trap 8, payoff 8; the P_TOP trap is weaker than in H2a) / set density 7 / light 7 / colour story 8 / acting and comedy 7 / same channel? yes / camera travel 8.

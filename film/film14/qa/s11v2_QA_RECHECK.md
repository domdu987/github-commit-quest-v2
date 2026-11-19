VERDICT: FAIL. 2 blockers:

Director note: blocker 2 (g757) is inside the lead-in handle. The conform cuts s11 in at g759, so g757 is never used; it is not a blocker. Only blocker 1 (shot 12) stands.
1. Shot 12 (g821-863), the count: the ring of hives does not read. The frame shows one straight row of roofed stands running down a road. At phone size only about 4-5 hive boxes can be told apart (about 5-6 at full res, at g863: one large front hive, then 4-5 small ones, then roofs only). Nothing shows "ten" or "round the field". Fix: finish the crane higher and wider so the arc of the ring and all 10 hives are in frame by about g850. For example, camera at about 4-5 m, tilted down 20-25 deg, lens 28-32. Or move the camera to the inside of the ring so the hives curve round the field. Turn the hive fronts (bee end) toward the lens and give each one the same bright bee cluster as a per-hive cue. Use exactly this ring and these hives for shot 14 (the s11 v1 item 3 still applies).
2. Handle pop at g757 (n4): one stray frame shows the farmer card mirrored. The veil jumps to the left of his head, the rope coil jumps to the other hand and the arm flips. Then g758 returns to normal (frame diff 6.1 against a baseline of about 2.8). It sits in the in-handle, so it is not seen at the planned hard cut at g759, but handles are delivered for trimming and must be clean. Fix: re-render g757 with the same card and pose key as g756/g758, and check that the pose-loop key does not wrap at the handle start.

Take: r23/film/v3/film14/s11/take.mkv: 117 frames g753-869, 720x1280, 30 fps, h264, 3.90 s. meta.json matches (g0 759, g1 863, first_g 753, cut in, shot ranges 11 = 759-820 and 12 = 821-863).
Review: all 117 frames extracted to scratchpad/takes/qa_s11v2/all/ (g-numbered). Checked at 6 fps (every 5th frame), plus the cuts g759, g821 and g864 at +-3 frames, at full size and as phone sheets. Also checked with full-res crops of the feet, hands and hives, a per-frame difference measure, and the neighbour frames s07 g758, s13 g864/g898 and s01 g150. Sheets: sheet_6fps_phone.jpg, cuts_phone.jpg, neighbours.jpg, feet_zoom.jpg, hands_zoom.jpg, s12_full.jpg.

## Checks
| # | Check | Result |
|---|---|---|
| 1 | Story read at phone size | Shot 11 reads: one hive box under a tin roof, the farmer on a stool beside it, his arm up on the hanger rope (3-pose loop), the coil in his other hand. Shot 12 reads as "many hive stands in a row", not "ten round the field" (blocker 1). |
| 2 | Heads above y 880 | PASS. The farmer's head is at about y 560-760 in every shot 11 frame. Shot 12 has no people. |
| 3 | Contact shadows | Shot 12 PASS: the posts and rocks cast clear shadows. Shot 11 is weak: the stool stands in the roof's blue shade, so no distinct shadow under its legs is visible, and the farmer card leaves no darkening on the lit stool top under his soles. Non-blocking. Suggested fix: a soft 20-30 % AO/blob under each sole on the stool top and under the 4 legs. |
| 4 | Props in hands | PASS with a note. The rope runs from his raised hand to the hanger bracket. The coil hangs from the other wrist in every loop pose (at g771 the hook sits about 20 px inboard of the hand). Only g757 (handle) is wrong, see blocker 2. |
| 5 | No pops, cut at g821 clean | Cut g821: PASS. One-frame change (diff 44 at g821 only), with no black, magenta or doubled frame either side. g820 is clean shot 11 and g821 is clean shot 12. Pose-loop swaps inside shot 11 do not spike. Pop at g757 (handle): blocker 2. Cut g864 to s13: g863 is clean shot 12, and the handle g864-869 continues shot 12 with no pop. |
| 6 | Camera always moves (no static run over 6 frames) | PASS. Shot 11: orbit plus push. The background (farmer masked out) changes on every frame by 1.75-2.9 against a sky noise floor of 0.09, and by 5.5-8.0 over every 6-frame window. Shot 12: dolly/crane with a lateral drift of 1-5 px per frame from g821 to g869. |
| 7 | No text | PASS. The hanger blocks and lamp boxes carry no letters, and there are no signs. |
| 8 | Mouths still | PASS. The farmer's mouth is a flat line in all of g753-820. |
| 9 | Continuity: farmer costume | PASS. Same safari hat with side veil, orange shirt with hex badge, khaki trousers and white rope coil as s07 shot 10, s01 shot 3 and s13 (frames compared side by side). Note: s07 g758 and s13 show the card with the veil on screen-left, while s11 has it on screen-right (as s01 does), so the veil and coil hand flip across both cuts. Acceptable for a flat card, but matching s13 (veil left) would make the 11 -> 13 tie-on look like one action. |

## Re-check of s11 v1 (s11_QA_TECH.md) issues and team claims
- v1-1 blurry ground patch: FIXED. The green grass-mask patch is gone. The shot 12 ground is sharp laterite with crisp post shadows, and no mip blur is visible at full res. The ground still covers about 35 % of the frame in 12, but it is sharp and sits under the caption band, so this is acceptable.
- v1-2 hives too small / not countable: PARTLY FIXED. The front hive is now about 140-180 px wide, with top bars, slot and bees. The count still fails (blocker 1).
- v1-3 the ring is not the same ring / count ambiguous: OPEN for shot 12 (no ring visible). Shot 14 is not in this take.
- v1-4 shot 11 static, plank hive, no tie action: FIXED. The camera moves, the hive reads as a box with a bee end, and the arm loop works the rope.
- v1-7 stool: soles on the stool, team claim CONFIRMED. The dark shoe strips meet the stool top on every sampled frame (g759-820, 4x crops). The feet stay fixed relative to the stool, so there is no sliding, and the stool moves with him. The sapling stem in the leg area is gone. The contact shadow is still not visible (see check 3).
- v1-8 cut 821: clean.
- v1-9 shot 12 crane weak: FIXED. The framing changes a lot (g821 -> g863 difference 27; the near roof grows from 1/3 to 2/3 of the frame width).
- Team claim "shot 12 clear of roofs": CONFIRMED. No roof fills the frame. The nearest roof reaches the top-left at g863, but the sky and the row stay open.
- Eye-line (v1 note): still OPEN. The farmer looks into the lens while tying, not at the rope or hanger. Non-blocking. Suggested fix: use a pose key with the eyes toward the hanger (screen-left/up).

## Non-blocking notes
- Caption overlap: captions at y about 900 will cover the stool top, the soles and the stool legs (y about 840-980) for all of shot 11, which hides the proof that he stands on the stool. Suggested fix: raise the shot 11 framing by about 120 px (tilt down or raise the camera 0.15 m) so the stool top sits at y about 720-760.
- Light: shot 11 has a golden yellow-orange sky and shot 12 a pink-lilac sky. Both are labelled DAY. The change works as "next day", but shot 11 looks close to the dusk of shot 10. A bluer sky top in 11 would sell "Day 1" against the shot 10 dusk.
- The 3-sphere puff clouds in shot 12 (top right) are large. They match the set's cloud style (s01), so they are acceptable.

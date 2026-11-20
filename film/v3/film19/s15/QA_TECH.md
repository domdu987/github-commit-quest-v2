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

## Round 8 (director QA-tech): FAIL
Checked: merged take s15 (203 frames, g1086-1288, in-shot g1096-1279) at 6 fps plus every frame g1160-1230 (frames in /tmp/qa19_r8/s15/, name = g-1086). No black/magenta frames, no pops, no mouth movement (William and captain frowning or smiling with closed mouths; none moving). Heads max y 835 (<880), faces about 19 % of frame height (<35 %), contact shadows under shoes present throughout.
Frame-diff (90x160 grey, bilinear, in-shot pairs g1097-1279, n=183): median 4.08, p90 10.70, min 2.76, max 13.50. Numeric target (median >=4, p90 >=10) met, but only just, and the number is made by camera and light motion, not by acting (see 1, 2).
1. g1229-1279 (last ~2 s, diff 3.5 falling to 2.8): NOT frozen at the pixel level (min 2.76; the camera drifts, the deck roll and sea move, and the mast and rigging shift), but the characters are held in the same pose: the diff over the character region is about the same as over the plain deck. William's H4 pose and the captain's idle pose do not change. It is a camera-only run, near-frozen as acting. FAIL under §I5.
2. g1096-1160 and g1189-1279: both characters hold fixed idle or pose cycles on one spot (about 2 s at the start, 3 s at the end with no body motion): "nobody still for more than 1.5 s" is broken. Only g1160-1188 (snap) and g1190-1226 (lower, turn to H4) show body motion.
3. Plan coverage g1230-1279: the captain does NOT step in and lean to look at the H4. He stays on his mark at left, upright, looking at the lens, for the whole take. The sailors are tiny in the background (g1210-1279), the right one jiggles in place and no rope is visible or hauled; at g1270-1279 the sailors are cut by the left and right frame edges. Plan beat missing. Fix: key the captain from his mark to William's side, with a lean toward the watch, g1200-1250; show rope and haul loop for the sailors, keep them inside the frame.
4. Captain "glide 0.6 D" during the pull-back (g1190-1226): on screen he drifts from the left edge toward centre (x about 60 -> 85 px of 250, while the camera moves back and he shrinks), feet in contact with the deck and the shadow, no walk cycle. Because he is parented to the ship and the camera moves, he does not slide against the deck planks or the mast shadow; he looks planted and the crane reads as a camera move. I do not rate it as floating/sliding. But the drift is not a mark move, so the team's "0.6 D glide" is camera parallax, not captain motion.
5. g1160-1178 (William quadrant up): William's quadrant tip and the captain's hat brim touch the left frame edge (g1170-1182). NOTE, not blocking (faces inside).
6. NOTE: the sun disc appears at g1176 and is a flat white disc; at g1218 it sits beside the rigging, fine.
Verdict: FAIL (issues 1, 2, 3).

## Round 9 (director QA-tech): FAIL
Take: take.mkv.partaa+partab, 203 frames 720x1280. Frames: /tmp/qa19_r9/s15/ (six/ = 6 fps, all/ = every frame, i = g-1086). Checked 6 fps plus every frame g1160-1280. No black frames (min luma 91), no frozen runs (min diff 1.64), no magenta/text, no character cut in half, nothing floating (contact shadows under all feet), no prop through a face.

Frame-diff (own run, 90x160 grey, bilinear, g1097-1279): median 4.84 (>=4 OK), p90 11.18 (>=10 OK), min 1.64, max 19.7. Caveat: p90 is carried by the camera tilt at g1166-1184 (diff 8-20). Last 2 s (g1220-1279) mean 4.04; the "2.4" belongs to g1187-1190 only.

Issues
1. g1207-1229 SUN DISC BLINKS OUT: the disc fades 255 -> 91 in 3 frames (g1207-1210), is replaced by a dull grey patch (about 165, the sail colour) until g1226 and snaps back g1227-1229. About 22 frames (0.7 s) with no sun during snap2 and the dial push-in. Unintended pop. Fix: keep the disc and halo at constant strength through g1196-1240, or fade over at least 12 frames.
2. g1238-1262 William's glance is NOT visible: eyes stay closed-smile in every frame (g1236, 1248, 1258, 1268, 1279). Fix: add open eyes with a glance up and back.
3. g1248-1279 (1.0 s): both principals hold the same pose. Only the captain's face and the watch sway change, and the crane moves slowly. Under 1.5 s so not a hard fail, but it reads static. Only the sailors move (striped sailor hauls, red-bandana sailor appears behind the captain's head from g1244).
4. g1218-1242 captain's hat brim touches or clips the LEFT frame edge during the peak push (face inside, skin x >= 25). The dial at the peak is about 170-190 px: OK. Fix: nudge the captain 40 px right or ease the push.
5. Claim 1 only partly true. The diagonal sail shadow does NOT disappear at g1171. It stays on the lower left to g1279 (g1171-1174 still a big dark diagonal). The change is smooth with no pop at g1171 (diff 19.5 vs 17.9 and 19.7 neighbours, continuous). The deck is 25-28 % of the frame (orange mask) from g1172, a hair over the claimed 25 %. The sun is top-centre at (359,124) from g1166, camera-parented.
6. Claim 2 only partly confirmed. Hands read 8:00 and the dial is about 170-190 px. I could NOT reproduce "face = 37 %": measured face-only max 188 px = 14.7 % of 1280 (g1230-1232); hat-top to chin about 330 px = 26 %. Frames over 35 %: 0 (peak margin about 9 points under). Close-ups under §I.6: 1 push (g1212-1240), within the limit of 3.
7. Note: from g1236 the captain's mouth is an open "O" (shock) held to g1279 with one blink at g1268. It reads as an expression, not talking. Mouth flapping outside the quote window: none seen.

Claim 3 (sun top, watch bottom in the last 2 s, slow crane up): CONFIRMED (sun top-centre and constant, watch at y about 800-900, deck about 25 %). Claim 4: captain shock from g1236 CONFIRMED, William glance MISSING (issue 2), sailors stay in frame CONFIRMED. Claim 5: deck dressed (lamps, rope coils, rails, sailors): OK.
Fix items 1 and 2 are blocking; 3-4 should be fixed in the same re-render.

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

## Round 11 (director QA-tech) - FAIL (one measurement issue: luma 111.1 > 110)
Checked: take.mkv cat of partaa+ab (203 f, 720x1280, first_g 1086), all g1180-1288 + every 5th frame extracted to /tmp/qa19_r11/s15/, plus a full-res frame-by-frame look at g1232-1262 (face crops). (Note: this file had no Round 10 section in the copy read; the round 10 reason came from the brief.)
Fixed since round 10 (confirmed):
- William's eyes: open ring eyes + smile from g1198 (g1196 still being swapped in); smile held to the end. PASS.
- Glance up: ring eyes centred g1232-1237; head pitch/roll visible g1238-1241 (hat brim lifts), pupils at the very top of the eye whites g1239-1245, still up-ish at g1246-1248, back to centred/low g1250-1254. Reads as a glance up to the sun and back, sun is top-left in frame. PASS.
- Captain's mouth: closed dash to g1232, opens continuously g1233-1250 (mouth px 6 -> 850, smooth, no step larger than ~85 px/frame, no snap). PASS.
- Sun disc: fades in on the snap g1161-1164 (px 39 -> 302 -> 1453 -> ~2000), then steady (area 1730-2130, no frame with a >10 % jump, centroid moves smoothly with the camera, parks at x 179.7 / y 62.3 of 360x640 from g1228 on, area drifts 1850 -> 1735 to g1288). No blink. PASS. (Disc is not on screen before g1161; the fade-in is the snap itself.)
- Drift to the last frame: camera/disc still moving at g1288 (disc area, parallax). PASS.
Usual checks:
- Frame-diff (ffmpeg bilinear, 90x160 grey, pairs g1097-1279): median 4.87 / p90 11.11 (matches the director). PASS (>= 4 / >= 10). Segments: g1097-1160 ~4.6, g1160-1230 ~7.8 (snap/pull-back), g1230-1280 ~3.0 (hold). Note: with grey = mean(R,G,B) as in framediff.json it is 4.51 / 9.86, i.e. p90 just under 10; the ffmpeg-grey figure is the one used here.
- No black/blank/magenta frames, no frozen runs (min pair diff 1.39 at g1249), one pop group g1170-1175 (diff 14-23) = the planned snap (g1172 "อยู่ตรงหัว"), no other spikes. PASS.
- Framing: both characters fully inside in every frame checked; closest edge is the captain's hat brim at g1176-1190 (~50-65 px from the left edge) - NOTE only. Faces about 20-23 % of frame height at the dial-push peak (g1225-1235) (team says 33 %, real is lower) - PASS. Heads y 450-760 (< 880) throughout. PASS.
- Nothing floating: feet with contact shadows on the deck in all frames; sailors in the background are on deck/rail; no props through faces (watch sits under William's chin, in front of the chest, face unobstructed). PASS.
- Mouths: William still (smile). Captain: after the open (g1250 peak) the mouth narrows to g1268 (217 px) and widens again to g1288 (1024 px), a slow swell with no syllable pattern - reads as a gasp then awe, not talking. NOTE (there is no quote in this shot; if the director wants a hard "no mouth movement", hold it at the g1250 size).
- Nobody still > 1.5 s: William/captain blink and sway, sailors haul, glance g1238-1254. PASS.
- Colour (qa_stats.py formula): saturation 0.511 (>= 0.47 / 0.50 OK); **luma (brightness) 111.1 whole file, 111.2 in-shot -> FAIL vs 85-110 (over by 1.1).** Breakdown: g1096-1165 ~ 95, g1176-1279 ~ 121 (post-snap sunlit deck 120-126 after the snap, so -0.2 EV is not enough on its own).
Issues:
1. LUMA g1176-1288: ~121 (whole file 111.1 > 110). Fix: lower exposure another ~0.15-0.25 EV after the snap (target post-snap ~105-110, whole file ~100-105); a darker deck/sail, not a darker sun disc.
2. NOTE g1176-1190: captain's hat brim ~50-65 px from the left edge (not cut).
3. NOTE g1250-1288: captain mouth swell (see above).
Verdict: FAIL only on item 1 (luma 111.1, limit 110); every other check, including the R10 failure (William's eyes / glance), passes.

## Round 12 (director QA-tech) - PASS
Take: s15 take.mkv.partaa+partab -> /tmp/s15q12.mkv, 203 frames 720x1280, first_g 1086. Frames: every frame g1086-1288 in /tmp/qa19_r12/s15/g####.png (6 fps sheet /tmp/qa19_r12/sheet6.png, darkening and snap sheets reviewed).
Numbers (qa_stats formula, 90x160 bilinear):
- Luma 105.25 whole file, 105.25 in-shot g1096-1279 (limit 85-110): PASS (was 111.1). Per segment: g1086-1156 96.0, g1156-1176 107.0, g1176-1196 117.4 (decaying), g1196-1280 109.1, tail 110.5. Min frame 89.9.
- Saturation 0.507 whole, 0.501 in-shot (limit 0.47 / 0.50): PASS (thin margin on the 0.50 target).
- Frame-diff, pairs g1097-1279 (183): mean-RGB grey median 4.41 / p90 10.46; ffmpeg gray median 4.72 / p90 11.66. Both >= 4 / >= 10: PASS. Min pair 1.63 (mean-RGB) / 1.74 (gray) at g1249, no pair < 1.5.
Regression checks (all PASS):
- William: open ring eyes + smile throughout from g1198, glance up at g1238-1254 reads (head tilts, pupils up, back).
- Sun: steady round disc, >=230 area 6900-7800 px (720x1280) g1185-1221, no blink or square edge in crops g1188-1221. NOTE: with a strict >=245 threshold the count fluctuates (peak is 246-247) so use a lower threshold when counting; visually steady.
- Captain mouth: continuous open g1233-1250, then frozen "O" from g1246 (crops g1244-1288 show the same O, no snap, no narrowing/widening; this removes the round-11 swell note).
- Framing: both characters fully in frame, hat brim clear of edges (about 50-65 px at g1176-1190, as in R11; checked visually, not re-measured). Faces about 20-23 % of height at the dial push, heads y about 450-760 (< 880). Feet on deck with contact shadows, nothing floating, no props through faces (watch under William's chin). No black frames, no frozen runs.
- Nobody still > 1.5 s: the captain's pose is frozen from g1246, but the camera keeps drifting and parallax moves rigging, sea, sailors and the sun; his head-box frame-diff stays 4.7-7.8 (180x320 scale) and whole-frame 3.7-4.1 to g1288; William blinks and sways. Alive enough: PASS. NOTE: captain's face itself is static for about 1.4 s (g1246-1288), right at the limit; a blink would make it safe.
Darkening g1176-1196 (-0.56 EV): the ramp is smooth, deck luma 108 -> 90 over 18 frames (about 1.3 per frame, no step) and whole-frame 126 -> 109 (about 0.85 per frame); sky fades 173 -> 158. No visible exposure pop inside g1176-1196. The only step is at the planned snap g1170-1172 (deck 90 -> 113, whole-frame +8.7 at g1172), which is the "อยู่ตรงหัว" snap and the only frame-diff spike group (14-23 over g1170-1178). It reads as snap flash then settle; PASS, NOTE only (could soften by lowering the post-snap peak 126, not required).
Verdict: PASS (luma 105.3, sat 0.501, frame-diff 4.41 / 10.46 mean-RGB, 4.72 / 11.66 ffmpeg gray).

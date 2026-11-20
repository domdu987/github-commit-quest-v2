# QA-art, TAKE gate: s15 (SHIP ship_deck NOON, "the sun is overhead"): FIX-FIRST, 6.0

Frames checked (take index): 12, 40, 70, 86, 92, 102 at full size and 360x640, plus contact.jpg and phone_sheet.jpg.
Frames: /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artkey/s15_*.png

| Criterion | Score |
|---|---|
| Set density / ornament | 8 |
| Lighting & colour | 8 |
| Composition / phone legibility | 6 |
| Acting (aims at the sun) | 4 |
| Key moment ("the sun is right overhead") | 4 |
| Match to refs / client taste | 7 |
| **Overall** | **6.0** |

## What works
- The deck is sunlit, with sails, shrouds, sea, and a cloud. It is sharp and wide at the start. The big sail shadow sweeping off the deck as set_sun_overhead runs is a real 3D cue, and it is the best thing in the shot.

## Why FIX-FIRST
1. **There is no sun in any frame.** The mechanism is "noon, sun straight overhead", but the only evidence is a shadow that leaves, and a phone viewer reads that as a lighting change. Nobody is looking at a sun.
2. **Nobody looks up.** William holds the quadrant beside his hat, but his eyes and head face the lens with a scowl, so he reads as "angry man saluting". The captain also faces the lens, and his pitch -0.35 is not visible. The gaze (0.5, -0.9) does not come across as "up" on these faces.
3. On "อยู่ตรงหัว" the snap goes to a medium of William. His head is cut by the left edge in the last in-shot frames (take index ~100-103) and the quadrant is cut at the top.

## Fixes (shot.py)
1. Put the sun in frame. After the snap (g 1172-1189), tilt up: snap shift (0.8, 0.0) to (0.4, +0.45) with k 1.5 and rise_px 15 to 40, so a sky band with a hot sun disc sits at the top of frame and William's head stays at about y 500-650. If set3d19 has no visible sun disc, add a shot.py dressing: an emissive disc (warm white, strength about 20) on the ship_root up-axis about 40 D above William, plus a soft glow card. Show it only at frame top and keep no text.
2. William's pose: pitch -0.45, head_roll 10, gaze (0.3, -1.0), expression "squint" or "determined". Arm the quadrant vertically: angle about -85 instead of -62, hand y 0.25 on the thrust, so it points UP and not sideways.
3. Captain: pitch -0.5, yaw toward William (0.0), and a hand shading his eyes (arm_l hand (-0.15, 0.95), layer front). Two faces turned up then make the beat.
4. Keep William's head inside x 40-680 through g 1189. Cut slide_px from 40 to 20, or end the arc at the snap.

---
## Round 2 (TAKE gate, key takes, re-render): PASS, 7.0

Frames checked (take index): 12, 50, 80, 90, 100, 110 at full size and 360x640, plus contact.jpg and phone_sheet.jpg.
Frames: /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artkey6/s15_*.png

| Criterion | R1 | R2 |
|---|---|---|
| Set density / ornament | 8 | 8 |
| Lighting & colour | 8 | 8 |
| Composition / phone legibility | 6 | 7 |
| Acting (aims at the sun) | 4 | 6 |
| Key moment ("the sun is right overhead") | 4 | 7 |
| Match to refs / client taste | 7 | 7 |
| **Overall** | **6.0** | **7.0** |

## Earlier fixes
1. A sun in frame after the snap: **FIXED.** The camera-parented glare disc and halo (shot.py build_sun_disc, top right at 580,150) sit over the sails after the snap and read as a hot noon sun blazing through the canvas, with soft warm rays. It is the clearest "sun" read in the film so far, and it looks good at 360x640. The tilt-up to sky and sails works.
2. William's pose and quadrant pointing up: **FIXED** for the prop. The quadrant now stands vertical on his hat brim (angle -85) and reads as "aiming up". **OPEN (minor)** for the head: pitch -0.45 and gaze (0.2, -1.0) still do not read as looking up on the flat face. He faces the lens with a squint.
3. The captain looks up and shades his eyes: **PARTLY FIXED.** The hand at the brow reads as shading the eyes, but his face is also frontal.
4. William's head inside the frame through the snap: **FIXED.** William (right) is fully in frame with the quadrant inside x 700. The captain's hat brim touches the left edge at f 100-110. That is acceptable.

## Polish notes (not blocking)
- At f 76-84 (just before the snap) the disc fades in as a hard, flat white circle with almost no halo, and because it is 12 D from the lens it sits IN FRONT of the yard and shrouds. For those few frames it looks like a paper moon stuck on the rigging. Fade the halo in first (halo fade leads the disc by about 6 f), or hold the disc at 0 until the snap peak, so the sun first appears already blooming.
- A long diagonal sail shadow remains on the lower-left deck at the end. It matches the opening of s16, so continuity holds, but a shorter shadow would support "overhead" a little better.

---
## Round 10 (director QA-art): PASS, 7.3

Take: take.mkv.partaa+partab -> /tmp/s15a10.mkv (203 f, first_g 1086). Frames at 3 fps plus key beats (idx 73-83 bloom, 86, 96, 104, 122-140 sun/mast, 146-182 glance, 190, 202), full size and 360x640.
Frames and sheets: /tmp/qa19_r10art/s15/ (sheet.jpg, bloom.jpg, sunmast.jpg, glance.jpg).
Measured on the extracted frames: sat 0.516, mean luma 121 (team figure 113.6).

| Criterion | R2 | R10 |
|---|---|---|
| Set density / ornament | 8 | 8 |
| Lighting & colour | 8 | 7 |
| Composition / phone legibility | 7 | 8 |
| Acting | 6 | 6 |
| Key moment (sun overhead + watch on home time) | 7 | 8 |
| Match to refs / client taste | 7 | 7 |
| **Overall** | **7.0** | **7.3** |

## Does the mechanism read? Yes, better than any earlier round.
- idx 86-104: the noon sun sits at x~560, right above the quadrant William aims, and the sail shadow has left the deck. Reading "sun overhead, they measure it" is immediate at phone size.
- idx 132-202: the sun is at top centre and the big white pocket watch is in the lower half of the same frame. f190 shows sun and watch in one picture, which is the whole mechanism (noon here, but the watch says 8 o'clock home time). The captain's "O" mouth against William's smug smile sells the reveal.

## Sun: is it a sun or a sticker? It reads as a sun.
- The halo blooms first (idx 75-79) with a soft radial falloff and no square edge or hard rim. The disc then firms up inside the glow. The R2 note about a paper moon is fixed.
- It is steady from the bloom to the last frame, with no blink (the R9 tech failure at g1207-1229 is not visible: idx 121-143 are continuous).
- Because it is image-space, the disc washes over the mast and topmast stays (sunmast.jpg, idx 122-140), and the spars show faintly through it. This reads as lens glare and not as a sticker, because the glow also lifts the sail and the mast edge around it. NOTE only.

## Glance: does not read (NOTE, not blocking)
- The eyes are open through idx 146-182, which fixes the R9 problem. The glance up and back at g1238-1262 is only a few-pixel pupil shift under the same half-lidded lids. At 360x640 I cannot see it at all, so William reads as smugly holding the watch to camera. The beat still works, because the sun and the watch share the frame and the viewer's eye makes the connection.
- To land it: tilt the head (pitch about -0.3, roll 8) for 6-8 frames as he glances, raise his brows, and put the pupils at the very top of the eye whites. Do not rely on the gaze value alone.

## Anything worse than R9? No.
- The sail shadows clear by idx ~88, before the snap ends at idx 96. The captain's hat has about 45 px of air from the left edge at idx 96-110, and nobody is cut by a frame edge.
- Grounding: contact shadows under every pair of feet on all tiles. Nothing floats.
- Colour: sat passes §G (>= 0.47) and §I (>= 0.50) narrowly. Mean luma 113-121 is above the §G band of 85-110, because the sail and the glare are large and bright. QA-tech/auto own that number. If it gates, pull the sail exposure down by about 0.2 EV after the snap. Do not darken the sun.

## Polish (not blocking)
1. The glance described above.
2. William and the captain still face the lens squinting during the measurement (idx 86-110). That is acceptable at this size.

---
## Round 11 (director QA-art): PASS, 7.5

Take: take.mkv.partaa+partab -> /tmp/s15a11.mkv (203 f, first_g 1086, idx = g - 1086). Frames at 3 fps (20) plus every frame g1230-1260, and every frame g1186-1246 for the captain's face, at full size and 360x640.
Frames and sheets: /tmp/qa19_r11art/s15/ (sheet3fps.jpg, glance_sheet.jpg, glance_crops.jpg, glance_phone.jpg, cap_sheet.jpg, keys.jpg).
Measured on the 3 fps frames: sat 0.524, mean luma 117.5 (before the snap 92-108, after 125-134).
Note: the round-11 pull had dropped the R9/R10 QA-art section from this file. The R10 section above is restored from 8379068.

| Criterion | R10 | R11 |
|---|---|---|
| Set density / ornament | 8 | 8 |
| Lighting & colour | 7 | 7 |
| Composition / phone legibility | 8 | 8 |
| Acting | 6 | 7 |
| Key moment (sun overhead + watch on home time) | 8 | 8 |
| Match to refs / client taste | 7 | 7 |
| **Overall** | **7.3** | **7.5** |

## Does the glance read on a phone? Yes, modestly.
- William has open ring eyes and a smile in every frame from g1219. At g1230-1234 his pupils sit low, on the watch.
- g1238-1248: the head rolls and pitches up, and the pupils go to the very top of the eye whites. At 360x640 (glance_phone.jpg, g1244) the dots at the top of the rings and the tilted head read as "looks up at the sun", and the sun is right above him in the same frame. By g1254 he is back on the watch. The look is now a beat a viewer can catch, not a pixel shift.
- It is still small: the head move is about 10 deg, and there are no brows to help. It reads, but it does not land hard. NOTE only.

## Does the mechanism still read? Yes.
- g1172 (idx 86): noon sun above the raised quadrant, both men shading or aiming up, and the sail shadow gone.
- g1222-1288: the sun is at top centre and the watch shows 8 o'clock in the lower half of the same frame. The captain's growing "O" mouth against William's smile sells the reveal.

## Dial push as punctuation: acceptable.
- At the peak (g1222), the faces are about 33 % of the frame WIDTH and about 18-20 % of the frame height including the hat. This is under the §G 35 % limit and reads as a medium punch, not an extreme close-up. Both hat brims are inside the frame, and the watch dial is large and readable. It lasts about 1 s and then eases back, which fits §I.6.
- The deeper pull-back before it (g1196-1214) shows the whole quarterdeck with rope coils and buckets in the foreground, which gives the travel some depth.

## Captain's mouth: fixed.
- It stays closed until g1236, is small at g1237, and grows to a full "O" over g1238-1246. There is no snap.

## Regressions vs R10? None blocking.
1. NOTE: the captain goes to half-lid slits for four frames (g1230-1233) between ring eyes. It reads as a blink at speed, and at 30 fps a viewer will not see it as a pose pop. If it is not meant as a blink, hold the rings through it.
2. Brightness after the snap is still 125-134 mean luma on my frames, above the §G 85-110 band, because the big lit sail plus the glare fill the top half. The -0.2 EV is barely visible. QA-tech/auto own that gate. If it blocks, darken the sail or tilt the end frame down a little; do not dim the sun.
3. The last-second drift arc is smooth and keeps both men and the sailors inside the frame. There is no new edge cut.
4. Grounding: contact shadows under all feet on every tile, and nothing floats. The background sailors' rope end is still a known minor issue.

## Polish (not blocking)
- Make the glance bigger: add a brow lift if the rig has one, or about 15 deg of head roll for the 8 held frames.

---
## Round 12 (director QA-art): PASS, 7.5

Take: take.mkv.partaa+partab -> /tmp/s15a12.mkv (203 f, 720x1280, 30 fps, first_g 1086, idx = g - 1086). I extracted every frame, then reviewed frames at 3 fps (21), every second frame from g1170 to g1200, and a captain crop strip from g1242 to g1288. Each was viewed at full size and at phone size (180x320 / 360x640).
Frames and sheets are in /tmp/qa19_r12art/s15/ (sheet3fps.jpg, dark_sheet.jpg, phone_sheet.jpg, cap_sheet.jpg, fr/).
Measured per-frame mean luma (PIL L, full frame): before the snap 108 -> 92. Snap peak 137 at g1172-1176. It ramps down to 118 by g1192 and holds at 114-119 to the end.
Note: my measure gives about 117 after the snap, not 105. That is probably a different metric or window. QA-tech owns the gate number. On my frames the shot is visibly darker than R11 (125-134 -> 114-119).

| Criterion | R11 | R12 |
|---|---|---|
| Set density / ornament | 8 | 8 |
| Lighting & colour | 7 | 7 |
| Composition / phone legibility | 8 | 8 |
| Acting | 7 | 7 |
| Key moment (sun overhead + watch on home time) | 8 | 8 |
| Match to refs / client taste | 7 | 7 |
| **Overall** | **7.5** | **7.5** |

## Darker deck: still reads as bright noon.
- The deck is still saturated amber-orange, and the plank grain is lit. Hard, short contact shadows sit under every pair of feet, so the sun still reads as overhead. The sails are warm off-white, not grey. The sun disc and halo are undimmed, and the glare still lifts the sail and the mast around it (g1186 full-size, g1260 full-size).
- The image is a little less "blown", which helps the watch dial and the faces stand out. It does not look dull or overcast at either size.

## Darkening transition g1176-1196: no pop.
- Luma falls by about 1-1.5 per frame from 136 to 118 over about 20 frames, a smooth ramp. There is no step in the per-frame series.
- It happens during the pull-back, while the eye is tracking the move, and it reads as the exposure settling after the sun bloom. I cannot see it as an event at 30 fps or on the phone sheet.

## Faster dial push: acceptable as punctuation.
- The pull-back runs g1196-1206 (whole quarterdeck, foreground rope coil and buckets kept). The push lands at about g1222 and holds, then eases out to the two-shot by about g1246.
- At the peak, the faces and the 8:00 dial are big and readable, and both hat brims are inside the frame. The faster move reads punchier, not jerky. framediff stays under 11 through the push.

## Frozen captain "O": fine.
- From g1246 to g1288 (about 1.4 s), the O pose is held while camera drift and the slow scale change keep the frame alive (cap_sheet.jpg). At this length it reads as a stunned, frozen gape, which suits the gag. It does not read as a dead rig.
- NOTE: a 1-2 px head bob or one eye-ring pulse around g1265 would make it read as alive rather than held, if a later round is touching the shot anyway.

## Mechanism: still reads.
- g1172-1186: noon sun overhead and both men sighting up with the quadrant, with the sail shadow gone.
- g1216-1288: the sun is at the top of the frame and the watch shows 8 o'clock in the lower half of the same frame. William smiles and the captain gapes. The cause and the effect read clearly at 360x640.

## Regressions vs R11? None.
- The extra drift keeps everyone inside the frame, with no new edge cuts. Grounding is intact. The R11 notes about the glance size and the captain's half-lid blink are unchanged.

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
## Round 9 (director QA-art): PASS, 7.2

Take: take.mkv.partaa+ab -> /tmp/s15r9a.mkv (203 f, first_g 1086). Frames: /tmp/qa19_r9art/s15/ (3 fps `f3_*`, key beats `k_60..k_200`, phone sheet `phone_sheet.png`, phone triptych `ph_key3.png` = idx 86/132/190, punch strip `punch.png` = idx 116-128, sun crop `crop_sun190.png`). Each frame was checked at 720x1280 and at 360x640.

| Criterion | R2 | R9 |
|---|---|---|
| Set (rich / detailed) | 8 | 8 |
| Light / colour | 8 | 7.5 |
| Composition / phone legibility | 7 | 7 |
| Acting | 6 | 7 |
| Key moment (mechanism) | 7 | 7 |
| Match to refs (R4/R5, §G-I) | 7 | 7 |
| **Overall** | 7.0 | **7.2** |

### Does the mechanism read on a phone?
**Yes, with the narration.** At idx 86 a hot white sun sits top-centre (360,125), with both men saluting or shading under it and the quadrant raised. At idx 132 the H4 dial reads clearly as **8:00** at 360x640 (a big white face with black hands). At idx 190 the sun is at the top, the 8:00 watch is at the bottom and the captain is shocked (round eyes, open mouth) in ONE frame. That frame is the thesis frame, and it works. "Sun overhead" plus "noon" in the voice, against a watch plainly at 8, is a clear contrast. Without a "LONDON"/home cue, "home time" still rests on the narration alone. That is acceptable, because the narration says it at exactly that moment.

### Punch-in on the watch
It is acceptable as punctuation, and gentler than briefed. At the peak (idx 132) the dial is about 130 px wide (not 180), and William's head is about 30 % of frame height including the hat (the face alone is about 20 %). That is under the §G 35 % rule, so there is no breach. The push lasts about 1 s and eases back. It counts as 1 of the 3 allowed close-ups (§I.6).

### Ending: alive or static?
**Alive.** In idx 175-200 the captain switches to `shocked`, William smiles at the watch and glances up, both sailors haul in the background, and a slow crane/arc moves the sails behind them. The last 2 s are the strongest image in the take.

### Still wrong (polish, not blocking)
1. **The sun card has a visible square edge.** Around the disc at (310-410, 75-175) there is a faint textured square, best seen in `crop_sun190.png` at idx 86 and 190. The halo/glow plane is a square texture whose corners do not fade to 0 alpha. Fix: give the glow card a radial alpha falloff to 0 at the edge, or use a circular card mesh.
2. **The sun pops in as a flat white disc with no bloom** (idx ~78-82, see `extra.png` panel 2). It sits IN FRONT of the mast and yard, so for a few frames it looks like a paper moon (the R2 note is still open). Fix: lead the halo fade by about 6 f before the disc, and start the disc at 50 % size/alpha.
3. **The quadrant is not under the sun.** At the snap the sun is at x 360, but William's quadrant is at x ~620 and the captain's salute at x ~390. The "tilt up" is mild: the deck still fills about 45 % of the frame at idx 86. Fix (optional): shift the sun disc screen-x to about 560 during g 1166-1190 so it is directly above the quadrant, or slide the pair left.
4. **A diagonal sail shadow is still there before the snap.** In idx 0-80 it covers half the deck, and a dark band stays on the lower left through idx 200. This works as a "before" image, but the "noon shadows" read only around the feet. Fix (optional): key `visible_shadow` off by about g 1150, or shorten the band.
5. At idx 190 the captain's hat brim touches x≈5. He is not cut, but give him 20-30 px of air (slide the pair right by 15 px).

### Verdict
**PASS (7.2).** The mechanism now reads on a phone: sun overhead (noon here) against an 8:00 watch (home), and the final frame holds both images with a shocked reaction. Fixes 1-2 are cheap and should go in if s15 is re-rendered for any other reason. They do not block conform.

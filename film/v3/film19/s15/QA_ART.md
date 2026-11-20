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
## Round 8 (director QA-art, merged take): FIX, 5.5

Take: merged s15+s16, g 1086-1288 (first_g 1086), one continuous move. Frames checked at 3 fps (20) and key frames (take index) 10, 40, 70, 80, 86, 92, 100, 110, 120, 126, 132, 138, 150, 165, 180, 193, at full size and 360x640, plus glide strip (98-130) and tail strip (140-202).
Frames: /tmp/qa19_r8art/s15/ (f3_*.png, k_*.png, keys_phone.jpg, sheet3fps_phone.jpg, glide.jpg, tail.jpg, watch_crop.png)

| Criterion | Score |
|---|---|
| Set (rich / detailed) | 7 |
| Light / colour | 6 |
| Composition / phone legibility | 5 |
| Acting | 5 |
| Key moment (the mechanism) | 4 |
| Match to refs (R5 / R4) | 6 |
| **Overall** | **5.5** |

### What works
- One continuous take with no cut, two snaps on the right words, sails, rigging, sea, brass binnacle and lamps, hauling sailors behind. The deck rides the swell. This is §I travel and is in the spirit of R5.
- The H4 reads as a pocket watch on a phone: white dial, hands, crown and bow (~45-50 px at 360x640).
- The pull-back from the sun to the pair is clean and well eased (frame-diff 13.5 peak, no pops).

### Why FIX (the mechanism does not read on a phone)
1. **"Sun straight overhead" is contradicted by the frame.** The sun disc sits at the top right, in front of the sails, at about 30-40 degrees off vertical. A huge diagonal sail shadow crosses the deck through the whole take, including the snap. A phone viewer sees "a sunny afternoon", not "noon, sun overhead". The "crane up to the sun" is only a mild tilt: at the snap (f 86) the frame still shows full bodies and 35 % empty deck, so it never feels like looking up.
2. **"The watch still shows home time" has no contrast.** The H4 shows 10:10 (the catalogue pose) and nothing on screen says "noon here" versus "a different time at home". Without the contrast the second half of the line is just "a man holds a watch".
3. **The last ~2 s hurt (f 150-202).** It is a static frontal two-shot: two cards side by side facing the lens, William smiling, the captain unchanged. The captain does not visibly lean in or look at the watch. On the payoff beat of the mechanism this reads as a pause. Frame-diff ~3.3 confirms it.
4. **Empty deck.** The lower 35-45 % of every frame is flat orange planking with nothing on it (f 10-130 especially). §G.3/§H.3 "no empty flat ground planes".
5. **Colour.** Frames measure sat 0.45-0.52 but luma 129-139 (§G.1 asks 85-110; team mean 124). The large beige sails and the bright orange deck give a washed, sunlit-paper look; the blue sky shows only in slivers. It is not hazy, but it is not R5's deep blue.

### Team caveats
- **Captain glide 0.6 D (g 1188-1214):** does NOT hurt. It happens while the camera pulls back fast and the cards shrink; at 360x640 the feet move a few px under a moving frame and read as a step-in. Keep.
- **Low-motion last ~2 s:** DOES hurt, see 3.

### Fixes (shot.py / set)
1. **Make the crane up a real look-up.** At the snap (g 1166-1182) tilt until the deck leaves the frame: frame bottom at William's hat brim, the quadrant pointing straight up the centre of the frame, and the sun disc top-centre directly above it (move the camera-parented disc from (580,150) to about (360,120)). Vertical line quadrant -> sun = "overhead".
2. **Kill the long shadow at noon.** Once set_sun_overhead reaches 1 (g 1176) the sail shadow must shrink to a pool under the feet / the mast. If the shadow is from a fixed lamp, cut its strength 70 % after g 1176 or rotate the key light to vertical. Short shadows under the feet are the second "overhead" cue.
3. **Give the watch a different time and say "home".** Set H4 hands to a clearly non-noon time (e.g. 8:00 or 3:00, hour hand far from 12). Add one short in-world label (allowed by §I.4): a brass tag on the watch chain or a card "LONDON" / "ลอนดอน", and on the sun side "12:00" / "เที่ยง". Push the snap2 to a dial of ~160-200 px at full size (face still < 35 % of frame height).
4. **End on "sun top, watch bottom".** In the last 2 s, a slow crane up / arc (no new snap) so the sun returns at the top while the H4 stays in the lower half: the mechanism in one frame, plus motion. The captain must act: yaw and pitch toward the watch, lean 0.2 D toward William, expression surprise; William glances up at the sun then back to the watch (gaze change around g 1245).
5. **Dress the deck foreground.** Coiled rope, a cannon, buckets, crates, or a hatch grating in the near foreground lower third; or drop the camera height so the deck takes < 25 % of frame.
6. **Colour.** Exposure about -0.3 EV (target luma ~105), deeper blue sky with more of it visible behind the rigging, slightly warmer/darker sail shading so the sails stop being a big beige wall. Target sat >= 0.50 (§I.3).

Re-check after the fixes: f 86 (overhead), f 132 (watch), f 190 (sun + watch in one frame), phone size.

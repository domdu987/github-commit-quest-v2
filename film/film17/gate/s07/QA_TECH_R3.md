# QA-tech film17 s07 ROUND 3 (shots 16-19, g844-1051) - VERDICT: FAIL

Checked: all 208 frames extracted (take.mkv), 6 contact strips, 15 frames viewed full size (g874, g918, g925, g926-g930 strip, g928, g936-g946 strip, g940, g954, g970, g990, g1000, g1011, g1027, g1048) plus a per-frame Laplacian/diff pass.
No black/magenta/blank frames. No head crosses y 880 (lowest chin ~y 750 in g1027, ~y 880 never reached; shot 16 chins <= y 700). No mouths moving. No see-through cards, no beam shafts. Dust: a few small white motes in shot 18 (g970, g990), under 0.5 density - OK. Cuts g900/g948/g996 are real hard cuts (frame diff 63/65/62).
Sharpness numbers (Laplacian var vs median 213): soft runs g914-927 (0.46-0.59), g996-1005 (0.51-0.58), g1026-1045 (0.54-0.60).

## R2 items - status
1 (shot 17 no finger/foot board): PARTLY FIXED - macro of gauge exists g900-927, foot board visible g928+, but both beats fail (see B1, B3).
2 (calipers touch nothing, shot 17): NOT FIXED.
3 (crate covering feet): FIXED (crate gone).
4 (thief swap blue->green, huge Bertillon): FIXED - green thief only from g900; but see B2 (pop).
5/6/7 (shot 18 arm-span, tiny chars, tripod): shot 18 now a medium two-shot (heads ~170 px), tripod gone. Arm-span/ear: ear only (g954-g984). Card+pen present g990 - FIXED partly.
9/10/11/12 (shot 19): card now ~90 px, 3 drawer sizes exist, but card never enters a drawer (B4).
14 (gendarme late): FIXED - gendarme in frame, pen on card g844-g899.
15/16 (head cropped, reading): shot 16 OK now.

## Blocking
B1. g900-927 and g925 (shot 17, finger): team claim CONFIRMED and worse. Caliper bar sits in AIR behind the gauge; jaws (g925, x 375-440, y 590-720 of 720x1280) are beside/behind the gauge slider, not around any finger. No finger exists on the gauge: thief's hands are behind his back at every frame. Bertillon's hand is not holding the bar (bar end hovers left of his coat, g918 x 250-440 y 640-660). Fix: show the thief's hand (middle finger) on the gauge slot with jaws closed on the finger, Bertillon's fingers on the grip.
B2. g927->g928 POP (qa_auto flag CONFIRMED, team's explanation WRONG): frame diff 65 equals a hard cut (planned cuts ~63). It is NOT an actor swap at a snap peak. g927 is a macro on the gauge table; g928 is a wide of the thief/Bertillon on the foot board - a full camera/framing jump, only 1-2 motion-blur frames (g920-g927 diff 28-50) lead into it, and the content is entirely different. It reads as an unplanned cut inside shot 17. Plan allows a snap (14 f); this one is an instant swap. Fix: make the snap a real whip (>= 8 frames of streak into the new framing, hide the swap at peak blur) or add it to the planned cut list (g928) and update shot_plan.
B3. g940 (and g936-g946, shot 17 foot): team claim CONFIRMED. Foot board is at the floor at y 740-870 but the caliper bar crosses at shin/knee height (y ~610-640, x 215-480), jaws are hidden behind the thief's shins; no jaw is on a heel or foot. Bertillon is crouched behind the thief, his hands are not visible (dark coat mass at x 330-520, y 620-760); the thief's feet are on the board but nothing touches them. Not readable at phone size. Fix: low insert on the bare foot, jaws on the heel, Bertillon's hand gripping, Bertillon not behind the legs.
B4. g996-1049 (shot 19): card never goes into a drawer. g1011: card held at x 370-465, y 615-750 beside the small drawer, then g1027 card has vanished and Bertillon's hand is empty (open ring hand, y 750). No slide, no fill (the dark maroon band drawers are static; one top drawer is open all through). Plan beat (slide into size-marked drawer, drawers fill) is missing. Team claim "sizes differ only modestly" CONFIRMED for g996-1030 (small ~100x70 vs large ~120x90 px); by g1048 sizes are clear (small ~110x70, large ~210x130 px) but only two drawers are special and the medium is absent.
B5. g970 (jaws on ear) - team says it reads well: PARTLY WRONG. Caliper jaws are on the gendarme's hat-brim/ear line (x 340-450, y 545-610), good. But the bar runs back to Bertillon's face/glasses temple (x 290-345) and his hand is NOT on it - his arms hang at his sides (hand at x 170-210, y 790-800). Instrument is not held by a hand. g954-g984 identical. Fix: put Bertillon's hand on the bar.
B6. Leftover geometry: floating crossed white/cream rods and a cream plank, g900-g946. g918 / g925: crossed rods at left (x 0-310, y 380-580) and a small silver cross on the table right (x 530-690, y 640-770); g929-g941: large cream plank + diagonal rod standing across Bertillon's face and the thief's legs (x 330-420, y 340-600; rod end at x 125, y 780). These are the rods seen in other takes. Remove.
B7. g996-g1005 (10 frames) soft at 0.5 of median, outside the 3-frame blur limit; also g1026-g1045 (20 frames at 0.54-0.60), g914-g927 (14 frames). Check by eye: g1000/g1027 are the actual drawer-wall frames and are visibly soft vs g990 (cause: push-in on a low-res plate / texture). Only g920-g927 is motion streak (acceptable at the snap, not 14 frames). Fix: sharper wall plate or hold the camera.

## Should-fix
S1. g990 pen/nib on card: team claim OK - card (x 340-500, y 580-740) and pen tip touch, Bertillon's hand holds both. Reads. But the "pen" has white feather/arrow fletching at the gendarme end (x 540-640, y 720-760) and looks like an arrow; swap for a plain pen.
S2. g939-g947 and g950-g969: thief and Bertillon nearly static (camera drift only); about 0.6 s, below the 1 s hold limit but reads as a tableau at phone size.
S3. g1000-g1019: Bertillon scratches his head with the hand behind it, no card visible for ~20 frames; card appears only g1009-g1019.
S4. Drawer wall (g996-g1049): hard horizontal seams of a darker maroon band at y ~510 and ~840 (two stacked plates with different perspective), visible as a slab.
S5. g1019 onward: gendarme not present in shot 19 (fine); Bertillon's eyes close at g1027 while no mouth movement - OK.
S6. g1044-g1049: left edge crop of Bertillon (x 0-20) minor.

## Checks summary
Instrument ON body part and held: shot 16 PASS (g874: rod on head, hand grips; gendarme writes), shot 17 FAIL, shot 18 FAIL (jaws on ear but hand not on bar), shot 19 FAIL.
Static tableaux: borderline (S2). See-through/beam: none. Dust: PASS. Chins: PASS. Mouths: PASS. Blur: FAIL (B7). Frozen > 1 s: PASS. Pop: FAIL (B2). Black/magenta: PASS. Leftover geometry: FAIL (B6).
Rhythm 5.24 / 14.85: acceptable.

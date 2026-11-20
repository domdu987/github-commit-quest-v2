# QA-tech film17 s07 ROUND 4 (shots 16-19, g844-1051, f745e43) - VERDICT: FAIL (2 blocking, both small fixes)

Checked: all 208 frames extracted from take.mkv (take = g-844). Viewed full size: g910, g920, g935, g940, g945, g960, g976, g985, g1005, g1015, g1030, g1038, g1045 (13), plus 5-frame cut strips at 900/924/948/972/996 (±2), and strips g1000-1051, g927-984 (all frames 940-947 viewed as strip). Numeric pass: Laplacian sharpness, frame diff, mean luma on all 208 frames.

## Auto numbers
- Hard cuts: frame diff at g900 63.6, g924 72.9, g948 77.1, g972 82.8, g996 75.9. All clean, single-frame hard cuts (QA_AUTO "no visible change" note is wrong; all 5 cuts are visible, new content on the cut frame). No pops elsewhere (diffs 20-37 at g977-993 are pen strokes, g1024-1044 the camera pull-back).
- Blur: 0 frames below 0.65 of median sharpness. No blur run, no motion streak. Soft-flagged g940-947 and g976: sharp by eye (outlines, plank grain, ruler ticks, pen nib all crisp). PASS.
- Frozen: longest run of near-identical frames = 1. PASS.
- Black/magenta: none (min mean luma > 30). Dust: a few single white motes (g1030 x 215-250 y 1180; g1045 x 427 y 1258), < 0.5. PASS. No beam shafts, no see-through cards.
- Mouths: 18a puppets (g948-971) static, no moving mouths. Chins: shot 16 and 18a chins y <= ~700 (Bertillon chin ~y 665 at g960). PASS (< 880).

## Self-check claims
- g910 (17a): PARTLY TRUE. Glove at right edge (x 560-720, y 420-600), cropped by half the frame, sits on the caliper bar end; jaw (x 480-600, y 520-720) is open, ~100 px from the fingertip. Finger = three white capsules (x 0-380, y 620-740), hand/wrist off frame. Reads as "sausages and a block".
- g920: TRUE. Sliding jaw plate (x 345-410, y 520-730) touches the end of the middle capsule at x 345; glove still on the bar. Touch is visible but the "finger" is only recognisable as a finger by context. Weak.
- g935/g945 (17b): block touches the toe cap (g945 block face x 430-490 meets boot at x 440), glove on the handle (x 400-700, y 0-300). Touch TRUE. But the boot is a plain brown oval with no ankle, no sole, no laces (reads as a loaf/potato), and the glove is cropped by the frame edge.
- g960 (18a): TRUE. Jaws (x 190-330, y 650-770) straddle prisoner_b's ear; bar runs back to Bertillon's glove (cream bubble with squiggle, x 0-100, y 650-710, blue cuff). Held. Small: glove is edge-cropped and there is an odd dark ball at x 60, y 815.
- g985 (18b): TRUE. Plain pen (no fletching), glove at top-right edge (x 620-720, y 190-380), nib on the card at x 515, y 600, three rows of marks already drawn, rows grow g972-995. Reads.
- g1005 (19): TRUE. Glove with card (x 140-400, y 570-700) enters the medium drawer; card visibly goes in over g1005-1014 (card rim visible above drawer front, then gone behind it, g1012 card edge below the drawer front is a brief clip, see S3).
- g1015: TRUE. Card gone into the drawer, glove on the drawer rim lifting away. Drawer closed by glove g1028-1032 (glove pressing the drawer front at g1030, x 305-440, y 630-760). Beat reads.
- g1045: TRUE. Large ~130x110 px, medium ~105x70 px, small ~50x35 px: clearly different. Many drawers ajar with cards (right grid, left column). PASS.

## Blocking
B1. Leftover geometry, g1024-g1046 (shot 19 pull-back): the glove's blue sleeve is a free-floating tube with a flat cut end in mid-wall. g1030: tube x 305-670, y 330-740, flat end at x 640, y 330. g1038: tube x 345-560, y 470-690, flat end at x 540, y 480. No body or shoulder attached, so it reads as a floating rod/arm. Fix: keep the arm leaving frame (arm goes off the top/right edge) or show Bertillon's coat/shoulder at the end of the sleeve; or fade the arm out when the glove releases (g1020).
B2. 17a/17b do not read at phone size (g900-947, 48 frames): the finger is three unconnected capsules with no hand/wrist, the boot (g924-947) is an unlabeled brown oval (no sole, ankle, lace, no leg), and the gloves are cropped by half at the frame edge (g910 x 560-720, g935 x 630-720). The touches exist (jaw on fingertip g920, block on toe g945), but the viewer cannot tell finger from sausage or boot from bread. Fix: put an obvious hand (palm + wrist + fingernail on the middle finger) and an obvious boot (sole line, toe cap, ankle/shin stub, laces) in frame, move the glove 100+ px inside the frame.

## Should-fix
S1. Concentric ring moire / denoise artifact on the dark back wall in all table inserts (g910 x 250-430, y 330-540; g940 x 130-330, y 220-340; g976 x 130-330, y 0-90). Visible at full size, faint at phone size. Re-render with more samples or a smooth wall texture.
S2. g976 (and g970-g984) noise speckle patch beside the nib on the table (x 380-530, y 430-490): denoise smear. Also g985 x 400-540, y 430-480.
S3. g1012-g1014: a loose white card edge sticks out below the medium drawer front (x 780-870 in the 8-frame strip, ~y 300-315 of 427) for ~3 frames while the card is meant to be inside. Trim.
S4. Dark blue stub under the lower open drawer (x 290-390, y 1095-1145 at g1030; x 320-390, y 975-1030 at g1038), visible g1000-g1051. Looks like a leftover bucket/inkwell; delete or explain.
S5. g948-971: orange foot-board frame with yellow cap in the lower left foreground (x 170-420, y 960-1280) overlaps both characters' legs; reads as a floating plank. Move it behind the characters or remove.
S6. Table inserts (g900-923, g972-995): 25-35 % of the frame is an empty flat table colour (g910 y 880-1280, g985 y 880-1280). Reframe lower or push in.
S7. g1000-g1015: wall plates have a visible softness/halo outline at glove edges only; acceptable, note only.

## Rules summary
Held by glove + touches target: 16 PASS (approved), 17a PASS-weak (B2), 17b PASS-weak (B2), 18a PASS, 18b PASS. Card enters drawer: PASS. Leftover geometry: FAIL (B1; S4, S5). Hard cuts: PASS. Blur: PASS. Frozen: PASS. See-through/beams: PASS. Dust: PASS. Mouths: PASS. Chins: PASS. Black/magenta: PASS. Phone-size reads: 16, 18a, 18b, 19 PASS; 17a/17b FAIL (B2).
Rhythm 7.88 / 23.15 acceptable.

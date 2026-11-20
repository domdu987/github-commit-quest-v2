# QA-art: SET gate, film 20 (set3d20), 2026-11-20

Reviewer: QA-art (Opus). Look approval belongs to QA-art; the director cannot override alone (QA_TEAM.md E).
Looked at: `contact.jpg` (36 tiles) and every tile in `work/final/*.png` at 720x1280, plus 360x640 phone strips (made in scratchpad: `p_site1/2`, `p_t1/2`, `p_i1/2`);
`hue_report.txt`, `int_hue.txt`, the per-tile json head positions, `API.md`, approved board `styleboard/board.jpg`, my board review `film20/qa/QA_ART_board.md` (v1 + v2 mandatory list),
BRIEF.md, shot_plan.md, QA_TEAM.md, production-lessons §2 and §10.

## Verdict: **FIX-FIRST**

The big wins are real:
- the four rise snaps and the finished tower read as the Eiffel Tower instantly at phone size;
- tower_low (the hook), tower_fair, tower_dusk and tower_window_end are beautiful;
- the café wide and resto_wide are dense, warm and in band.

Seven key images still fail at phone size, though, and none of them can be fixed by camera work in the takes:
- the antenna reveal (white tower, flat circles);
- the spark hut;
- the last image (window pull);
- the shot 16/17 gag (finished tower hidden behind Maupassant's head);
- the ending view (resto_view faces him, not the window);
- the Eiffel plan-table and leg-low shots (dark, magenta over the limit, unreadable);
- the girder slide (no girder stack in frame).

There is also a render defect: pure-black (0,0,0) rectangles on the SITE ground.

## Scores per location (1-10)

| location | density / ornament | lighting & colour | composition / phone | key moments | match board / refs | mean |
|---|---|---|---|---|---|---|
| SITE  | 6 | 5 | 4 | 6 | 6 | 5.4 |
| TOWER | 6 | 6 | 6 | 4 | 7 | 5.8 |
| CAFE  | 7 | 6 | 6 | 4 | 6 | 5.8 |
| RESTO | 7 | 7 | 6 | 5 | 7 | 6.4 |

### SITE (S01-S10)
- site_wide / site_wide_end:
  - Dense and readable. It shows four converging legs, creeper cranes, scaffolds, forges with hoods, girder stacks, kegs, sheds, workers and the Trocadéro.
  - Problems:
    - pure-black ground rectangles (pixel (190,1015) = 0,0,0);
    - the forge smoke is a chain of lilac beads;
    - the bottom 25 % is an empty flat cool-grey shadow;
    - the end-pose foreground figure is a blob.
  - The site_wide_end shade hue of 291 comes from only 6 % cast pixels (median 236). Note only.
- site_rise snap 1/2/3: **the best SITE images**. Stage states are correct, every stage converges and tapers, and each reads at phone size. Ship as is.
- site_table: **fails**.
  - The camera sits under the leg in shade. Measures: dark 0.66, top luma 25, magenta 13.5 % (over the 10 % hard limit).
  - Eiffel is a 20 px figure in a dark corner. A huge black lattice tangle fills 50 % of the frame. A black (0,0,0) hole sits on the ground.
  - The plan table and blueprint are not visible.
- site_leg_low: **fails**.
  - The leg tangle is unreadable as "a leg rising to the sky", and a floating black slab sits over it.
  - Measures: dark 0.61, magenta 12.6 %.
  - The scaffold decks and riveters do not read.
- site_fence: the lower 45 % is empty grey ground. The Parisians are 18-31 px heads lost at mid-frame, and a black shed overhang slab hangs top left. Fixable by camera (notes).
- site_girders: **fails**.
  - Shot 12 slides "along a huge stack of red-lead girders". The stack is not in frame: two floating dark boxes, a derrick pole, a black ground hole and 40 % empty ground.
- site_rivet:
  - Good idea: it shows the deck, forge, Paris beyond and the scaffold below.
  - Problems: the spark and rivet read as flat yellow ping-pong balls, and the smoke is the bead chain again.

### TOWER (T01-T13)
- tower_low (hook): strong. Maupassant is foreground, the tower fills the sky, the arch frames the Trocadéro, and the hue is in band.
  - The black lamp-post on the left edge is acceptable as foreground.
  - The planned tilt-up must reach the second platform.
- tower_fair 1889/1910: a lovely set. The crowd, though, is rows of flat colour columns (green, red, teal pegs) that read as bollards at phone size.
- tower_dusk DUSK/NIGHT: the board image, now with the hut, wagon and cumulus.
  - The four wires still read as a white light beam, but it is acceptable as a story line for shot 19.
  - Cast marks are at y 1198-1222 with 20 px heads (below the frame bottom). See the render notes.
- tower_dusk_summit / summit_end: good whip-tilt start and end. A black lamp box on a pole sits in the foreground top left (fine as parallax).
- tower_hut / hut_spark: **fails**.
  - Wall and ceiling carry a blotchy noise texture, and the light is overexposed yellow (spark tile V>0.95 55 %).
  - The spark gap is not visible: only a white bloom on the table and a huge soldier shadow.
  - The window with the tower legs beyond is nice.
- tower_night_wide / tower_night_summit: **fails** (key reveal, shot 21).
  - The whole lattice turns flat white-blue, so the tower loses its Eiffel red and its lattice read.
  - The rings are big vertical white circles facing the lens (billboards), like a target or halo, not a radio wave spreading over Paris.
  - The night_summit start is a white mast against an empty sea-like horizon.
- tower_window_pull: **fails** (LAST IMAGE, shot 27).
  - The façade is a flat orange slab with noise and no lattice. The window room is a stack of brown stripes.
  - Maupassant is about 30 px. It does not read as "a restaurant inside the Eiffel Tower".
- tower_window_end: beautiful whole-tower end pose with the fair. Ship.

### CAFE (I01-I09)
- cafe_wide / cafe_window: dense and warm: banquettes, mirrors, wall lamps, artists, waiter, foreground chairs, and the lattice through the window.
  - The checker floor is high-contrast blue/cream on 27 % of the frame and dominates the lower half.
  - The ceiling is mauve-pink with blue "porthole" roundels. The chandeliers are flat discs.
- cafe_table_insert: the sheet with quill reads well. But the "signatures" are rows of the same looped **"B"/"BBBB" letterforms**, which read as Latin text at full size (client: no text).
- cafe_low (stub): Maupassant against the window with the stub legs. The blue ceiling roundel at top left (white ovals) reads as a face/mask and the disc chandelier is cut.
- cafe_low_full / cafe_low_close_full (1889): **fails**.
  - The finished tower is a 6 px spire hidden directly behind Maupassant's head.
  - The stub version actually shows MORE tower than the finished one. The shot 16/17 gag ("the full tower now stands behind him") does not read.

### RESTO (I10-I12)
- resto_wide: dense, Warren trusses, navy carpet with crimson border, buffet, diners, chandeliers. In band: floor 24.3 %, blue 25.8, red 33.8.
- resto_table: a nice reveal set. The lattice girders cross the window over Paris, the Trocadéro and the Seine. Floor 7 %.
- resto_view: **fails** (shot 26, the ending punch).
  - The camera faces Maupassant with Paris behind him. The plan needs "over his shoulder out of the big window".
  - The view must fill the frame, and the absent tower is the joke.

## BLOCKING fixes (set must be fixed and re-tiled before any render team starts)

1. **SITE ground black holes.**
   - Where: `site20.py` ground layer, the `earthpatch` boxes at z 0.012-0.015, 0.02 thick (lines 211-218) and/or the plank walks.
   - What to fix: they render as pure (0,0,0) rectangles in site_wide, site_wide_end, site_table, site_girders and site_fence.
   - Fix the normals/material or offset them so they no longer coplanar-fight the ground.
   - Pass condition: no ground pixel with luma < 15 in any SITE tile, with the shadowed earth at about luma 50-70.
2. **site_table (shot 4): rebuild the camera.**
   - Move the camera out from under the leg to the sunlit side, 6-7 m from the table, 1.5 m high, looking back at the table with the curved leg and scaffold rising behind.
   - Frame:
     - Eiffel is at least 150 px tall with his head at y 450-750;
     - the plan table and unrolled blueprint (greeked lines, no text) are lit and readable;
     - a girder end sits in the foreground.
   - Targets: dark V<0.25 at most 0.30, magenta at most 10 % (hard), shade hue 240-260, sky 15-30 %.
3. **site_leg_low (shot 5).**
   - Put the camera at the foot of one leg on its OUTER sunlit face, looking up along the curved leg with the scaffold beside it, so the leg is one clear diagonal from bottom to top.
   - Sky at least 35 %. Remove the floating black slab.
   - At least 3 riveter cards on the scaffold decks at 40 px or more. Eiffel at the foot with his head above y 880.
   - Targets: dark at most 0.30, magenta at most 10 %.
4. **site_girders (shot 12).**
   - Bring the 3 piles of red-lead I-girders into the nearest 40 % of the frame, lit, with flanges and ends readable, plus the two carrier cards with a girder.
   - Delete or relight the two floating dark boxes.
   - Empty ground at most 20 % of the frame. Derrick and hanging girder in the upper third.
5. **Smoke and sparks (site_wide, site_rivet; same kit in tower/hut).**
   - Replace the bead-chain smoke with 3-5 overlapping soft puffs: grey-lilac `#b8aec8`, low opacity, widening upward.
   - Sparks become short emissive streaks (`#ffcf60` core, 6-12 px long) instead of spheres.
   - The tossed rivet becomes a small elongated glowing cylinder (`#ff8a2a`, strength ≥ 20), at most 14 px, not a yellow ball.
6. **tower_night_wide / night_summit (shot 21, antenna reveal).**
   - Keep the tower **Eiffel red with its gas-lamp dots**. `wire_glow` may only brighten the 4 wires and a thin blue-white rim along the lattice edges (emission strength at most 3 on the edge or wire material, base colour unchanged). The lattice must stay red-brown with dark gaps.
   - Rings:
     - make them **horizontal** (lying in the plane at summit height, so they read as flattened ellipses spreading over the city) instead of billboard circles;
     - colour `#9ac0ff`, minor radius about 2x the current, soft falloff;
     - fade alpha out with radius, 3-4 rings visible at once;
     - the largest ring must reach the horizon city lights.
   - In night_summit, put the city ring and lights under the horizon (not an empty sea).
7. **tower_hut / hut_spark (shot 20).**
   - Remove the noise texture on the walls and ceiling: use flat planks with battens `#9a6a40/#6e4a2c` as on the board.
   - Lamp key down so V>0.95 is at most 9 % with the spark on.
   - Build the spark gap on the bench in view: two brass balls `#cba048` on rods with a jagged arc `#e6f2ff` and a 12-24 px halo `#9ac0ff`.
   - Place the Morse key and headphones in the foreground. The soldier's shadow must not cover the gap.
8. **tower_window_pull (shot 27, LAST IMAGE).**
   - Façade: the riveted red-brown lattice girders (as in resto_table's window, seen from outside) frame the window, not a flat noisy orange slab.
   - Window room: a lit restaurant interior (warm chandelier glow, cream wall, white cloth, a second table), no brown stripes. The window glows warmer than the façade.
   - Maupassant at the start pose at least 90 px tall (head and table), eyes shut, glass up.
   - The pull must pass through recognisable first-platform lattice into tower_window_end.
9. **CAFE 1889 tower in the window (shots 16, 17).**
   - In cafe_low_full and cafe_low_close_full, the finished tower must be a complete Eiffel silhouette (legs, arch, platforms, spire) beside Maupassant, not behind his head. Two ways to get there:
     - move the far tower or the window-view placement so it sits in the window's right half;
     - or move the window and banquette mark so the head covers the window mullion.
   - The tower should be 45-65 % of the window height, clearly bigger in mass than the 1887 stub in cafe_low.
10. **resto_view (shot 26, ending).**
    - Over-the-shoulder camera behind Maupassant: his back, shoulder and the back of his head in the left or right third, foreground at 1-2 D, raising a glass.
    - The window takes at least 60 % of the frame: Paris roofs, a clear Seine ribbon, the Trocadéro, lattice girders crossing the glass, **no tower**.
    - Head above y 880.
11. **CAFE dressing.**
    - Checker floor: lower the contrast (`#3c4f86` / `#d9c9a4`, about half the current luma gap) and make the tiles 1.5x larger.
    - Ceiling: warm ochre-cream coffers instead of mauve-pink. Remove the blue roundels with white ovals: they read as faces.
    - Chandeliers: 3D arms with 6-8 candle emitters, not flat discs.
    - Signature sheet: replace the repeated "B" loops with varied scribble strokes (zigzags, loops, underlines at different angles and lengths) so no letter shape repeats or reads.
12. **Fair crowd (tower_fair, shots 15/23).** Replace the flat colour columns with cast20 crowd cards (head, hat, coat silhouette, parasols) at least 40 px tall in the midground, 15-25 visible.

## NOTES FOR RENDER WORKERS (camera and staging in the takes, not blocking)
- tower_dusk (shots 18 and 22):
  - the marks project at y 1198-1222 with 20 px heads;
  - raise the camera or push in so Old Eiffel, the officer and the wagon sit at y 600-850 with heads at least 35 px;
  - keep the lamp-post or bench in the foreground.
- tower_low (shot 1): the tilt-up must end with the second platform in frame. Keep Maupassant's head above 880.
- site_fence (shot 11): lower and push in so the Parisians' heads are at least 40 px and the empty ground stays at most 25 %. Frame out the black shed overhang. On the punch-in, Eiffel and the rivet fill at least 30 % of the height.
- site_wide (shot 3): the crane-down end pose has a blob foreground figure. Use a real worker card or crop it.
- site_wide_end: the shade hue of 291 comes from few cast pixels. QA-tech must check the take's hue_report; the median of 236 is acceptable.
- Wires in shot 19: follow the brightest wire on the whip-tilt so it stays continuous.
- Resto and café: keep a foreground chair, glass or bread in the nearest 15 % on every camera (§10).
- Seated Maupassant: the lowered stand-in is acceptable for the SET gate, but the cast team must deliver a seated pose (bent knees hidden by the cloth, forearms on the table) before shots 2, 25 and 26. It is not a set item.
- Sharpness: all tiles are sharp with no DOF. Keep it so.

## Re-gate
Re-tile only the cameras in the blocking list:
- site_wide, site_table, site_leg_low, site_girders, site_rivet;
- tower_night_wide, tower_night_summit, tower_hut(_spark), tower_window_pull, tower_fair;
- cafe_wide, cafe_low(_close)_full, cafe_table_insert;
- resto_view.

Send them with the hue numbers. Everything else is approved now: site_rise snaps 1-3, tower_low, tower_dusk (+ NIGHT), tower_dusk_summit(_end), tower_window_end, cafe_window, resto_wide and resto_table.

---

# Round 2 (2026-11-20, re-tiles in work/final S*/T* 08:48-09:05 and int_work/*.png 08:31-08:38)

Looked at every re-tiled camera at 720x1280 and 360x640 (the I* files in work/final are the OLD 07:38-07:46 renders; I judged the interiors on int_work/).

## Verdict: **SHIP** (render teams may start). No blocking items remain. The notes below go to the render workers and the take gate.

| # | round-1 blocking item | result | decision |
|---|---|---|---|
| 1 | SITE black ground holes | gone in S01/S02/S03/S05/S06 | PASS |
| 2 | site_table | Eiffel at a lit table with a blue unrolled plan reads at phone size; magenta 1.6 %, dark 0.33. Weak: a blank pale pier wall fills about 30 % of the background, and the bottom 35 % is empty ground | PASS, note R1 |
| 3 | site_leg_low | the leg now reads as one big lit diagonal with pale timber scaffolds, a deck and riveters; magenta 0.9 %, dark 0.23. Sky 22 % (asked 35) | PASS, note R2 (the tilt-up in the take adds the sky) |
| 4 | site_girders | the stack and the hanging girder are in frame; dark 0.42 with bare shadow ground in the lower third | PASS, note R3 |
| 5 | smoke / sparks / rivet | the bead chains are gone (soft puffs); the rivet-deck spark is still a small yellow dot at phone size, but tiny, no longer a ball | PASS, note R4 |
| 6 | night wide rings / white tower | the tower is Eiffel red with lamp dots; the rings now read as wide arcs spreading over the city. The small circle at the summit is still a flat halo. T11 is mostly empty sky over a sea-like horizon | PASS, notes R5/R6 |
| 7 | hut / spark | plank walls, exposure in band (V>.95 8.4 %), brass balls on rods with a blue-white arc and halo readable | PASS, note R7 (plank stripe shimmer) |
| 8 | tower_window_pull | an iron X lattice frames a lit restaurant window (chandelier, cloth, Maupassant at the table); reads as "eating inside the iron". I meant the head-to-table group ≥ 90 px; the head is 51 px and the head-to-cloth group is about 100 px, so it passes. The façade slabs above and below are still flat noisy orange | PASS, note R8 |
| 9 | cafe 1889 tower | cafe_low_full / close_full: the complete lit Eiffel silhouette now stands beside his head in the right half of the window, clearly different from the stub legs | PASS |
| 10 | resto_view | true over-the-shoulder shot: the back of his head and shoulder in the left third, the window over the Seine, Trocadéro, gardens and roofs, lattice crossing it, no tower | PASS |
| 11 | CAFE dressing | the ceiling is cream with plain discs (no face roundels); the chandeliers have 3D arms with candles; the signatures are varied scribbles with no letter shapes. Checker contrast barely changed | PASS, note R9 |
| 12 | fair crowd | 20+ cast cards with heads, hats and parasols | PASS |

## Builders' admitted misses: decisions (all NOTES, none blocking)
- **Shade hue S03 271, S06 290, S07 294:** the cast pixels fall on red-lead iron and red girders, which shade toward crimson (bible rule 3, the same exception granted to the resto crimson). Frame magenta stays ≤ 7.9 % everywhere. Accept, and log it in the set QA.md.
- **Bottom-eighth luma S07 93, S09 88, S10 106:** these are the high crane snaps and the rivet deck, where the yard is in sun far below. Accept, because a darker bottom would kill the key "tower rises" read.
- **site_leg_low sky 22 %:** the planned tilt-up from 13 to 35 deg ends with more sky. Accept.
- **site_girders dark 0.42 / bare lower third:** camera note R3.
- **cafe_window smoke a short dark blob, artist covering the window:** the script line is "black factory chimney", so dark smoke is right. Staging note R10.
- **resto cloth/wall shade 222:** 8 deg under the band, on cool window fill. Accept with a note.
- **T11 empty sky:** note R6.

## NOTES FOR RENDER WORKERS (round 2, adding to the round-1 notes)
- R1 site_table (shot 4):
  - lower the camera by about 0.4 m and tilt it up about 8 deg so the curved leg and scaffold, not the blank pier wall, fill the background;
  - keep a girder end in the nearest 15 %;
  - push in at 8 %/s so the empty ground leaves the frame within the first second.
- R2 site_leg_low (shot 5): the tilt must reach a look_at of z 28 m by the snap at 11.44 s, so the sky ends at 35 % or more.
- R3 site_girders (shot 12): camera at 1.0 m and 2-3 m from the nearest pile, sliding along it, so the stack fills the lower half. Frame out the bare ground and the dark box at the right.
- R4 site_rivet (shot 13): key `spark(strength=1.5)` on the hammer hits, and snap-push onto the catch so the rivet reads at least 10 px.
- R5 tower_night_wide (shot 21):
  - stagger the rings so 3-4 arcs are visible and fading;
  - hide or shrink the small summit circle once the first arc has left;
  - the whole-lattice glow comes only on "เสาอากาศยักษ์" (50.90).
- R6 tower_night_summit (whip pull-out start, shot 21): hold it at most 4 frames before the whip so the empty sky is never on screen alone; or start the pull-out from a closer T10 framing.
- R7 tower_hut (shot 20): the fine plank grooves can shimmer on a moving camera. Push at most 9 %/s and check a draft strip at 360x640 for moiré. If it shimmers, use the same preset at 1.3x the plank pitch (set tweak allowed at the take gate).
- R8 tower_window_pull (shot 27): the crash pull-out starts on the window group. The flat façade slabs are on screen only for the first few frames of the pull, so start them already moving (no static first frame on the slab).
- R9 CAFE checker: keep the camera height so floor is at most 25 % in cafe_wide/cafe_window (currently 27.4/23.5) and put a foreground chair or table over the nearest checker.
- R10 cafe_window (shot 8): move the nearest artist card about 0.5 D to the side so the tower stub and the dark smoke are fully clear in the window by "ปล่องโรงงานสีดำ" (18.96).
- Interior finals: the director/QA-tech must take the CAFE/RESTO stills from int_work/ (the work/final I* tiles and the contact sheet interiors are the old round-1 renders); rebuild contact.jpg before showing the client.

QA-art round 2: **SHIP**.

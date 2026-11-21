# QA-art (strict) — film 17 style board (Bertillon), set3d17

Reviewed: still1.png (measuring room), still2.png (records office), still3.png (drawer/card reveal), board.jpg, all at full size,
against NOTES.md, film17/BRIEF.md, QA_TEAM.md (QA-art + Stricter QA), production-lessons §2/§10, bible colour-light.md + sets.md
(38b5918), and the approved set3d9 / set3d10 contact sheets.

## Verdict: FIX-FIRST

The board has a good idea in it: the card-cabinet canyon in still2 is a striking image, and the drawer reveal in still3 is staged
inside the lit 3D world. The picture is sharp, has no DOF, and has no readable text. But the light model does not follow the series
look. Shade is brown, not blue-violet. Large pale cream walls and ceiling will swallow the white-headed cast. Skies are flat
saturated blue, and the measuring room lacks the story's key instruments. Fix these before the full build.

## Scores

| area | score | why |
|---|---|---|
| density / ornament | 6 | still2 drawer walls are dense (hundreds of fronts, brass pulls, label frames) but uniform: no cornices, pilasters, ladders or pulled drawers. still1 has about 18 distinct objects (target 20-26). Its corner is cluttered with odd blocks (blue box + spheres, blue stand at right), and the brief's hero kit is missing (wall height gauge, arm-span scale, foot board, calipers on show). |
| light & colour | 4 | One hard warm key with crisp cast shadows: good (window patches in 1, raking shafts in 2). But there is no blue ambient. In my measurement, dim pixels (V 0.12-0.40, S > 0.15) sit at hue 0-45 for 57 / 79 / 52 % and at 230-260 for only 5.6 / 1.7 / 5.2 %. Shade reads brown-black, which is the bible's "shadows brown" fault. Black point luma p1 is 0.029 / 0.059 / 0.065 (bible 0.08-0.12): crushed. Blue is 6.4 % in still1 (band 14-30). Sky / skylights / window are flat saturated blue blocks (vivid blue 4.3 % of frame in still2). The floor and wood have glossy specular and photographic grain, unlike the flat colour-block look of set3d9 / set3d10. Magenta is fine (<= 7.4). |
| composition | 6 | still2: strong one-point corridor and good depth, but it is dead-centre symmetric, with an empty floor band in the bottom third and no foreground prop near the lens. still1: the ceiling takes the top 30 % as a pale plane; the foreground lamp post is a good §10 idea but reads as a street lamp. still3: clear reveal read, good diagonal. |
| period credibility | 5 | Card-drawer wall and skylit attic are right for the 1882-83 Préfecture. Problems: an outdoor street lantern standing indoors; electric-looking globe pendants with no gas pipe or gasolier arms; modern-looking blocky modernist exterior through the still1 window. The reveal card shows zig-zag scribbles instead of a Bertillon card (two portrait frames + ruled measurement rows). The red diamond runner is generic. |
| readiness for flat 2D puppet cast | 4 | Heads are near-white (`#fef7f6`). In still1 they would stand against a cream upper wall of V > 0.8 (and in still2 against cream upper walls / back wall). The bible wants a ring luma around the head of ~120. Characters in still2 would be tiny unless the camera moves in. The stand-in "people" are blue blocks + spheres and have not been placed at real marks. Floor space at the measuring chair is free and sits above the caption band: good. |

## Most important fixes (for the full build)

1. **Light model → series look (blocking).**
   - Add the bible's flat blue ambient as emission on every lit surface: `shade` (0.20, 0.27, 0.54). Set per-surface `shade_mul`: woods (0.62, 0.95, 1.1), warm walls (2.8, 2.05, 0.7). Use a yellow-orange key, about (2.30, 1.65, 0.74).
   - Use navy lift (0.0, 0.010, 0.026).
   - Acceptance (re-measure after the change):
     - dim-pixel hue majority in 240-260, with < 25 % at hue 0-45;
     - shade hue 240-260 on all three stills (still1 and still3 now 233);
     - luma p1 0.08-0.12;
     - dark 8-15 % (still1 / 3 now 18 %);
     - blue 14-30 %;
     - magenta <= 10.
   - Do this with real geometry and material values, not a grade-only tint.
2. **Walls and ceiling: no large pale surfaces; make heads read.**
   - Upper walls and ceiling are cream, V > 0.8. Repaint them as saturated mid-darks (V 0.45-0.70), for example terracotta `#aa3e2c` or ochre-brown with a warm wood ceiling.
   - Raise the dark wainscot to about 1.3 D. In still1, swap the green wainscot for a deep crimson or brown one, and keep a single navy cool block (rug or cloth).
   - Target: background ring luma around every planned head mark of about 95-165 (median about 120), measured with stand-in head cards at the real marks.
3. **Skies and windows.**
   - Replace the flat saturated-blue skylights (still2) and window exterior (still1) with a gradient sky, `#4a78cd` top to `#92b7e7` horizon.
   - still1 window: Paris mansard roofs and chimney pots (zinc grey-blue, chimney terracotta), instead of the blue boxes.
   - still2 skylights: frosted / mullioned glazing at emission about 3 with bloom.
   - still2 back window: a rooftop beyond it rather than white.
   - Target: vivid blue (S > 0.6, H 200-245) < 1.5 % of frame.
4. **Material finish to match set3d9 / set3d10.**
   - Roughness 1.0 on floors, walls and cabinets; no specular streaks (still2 floor, still3 drawer faces).
   - Swap the photographic wood grain for drawn SVG plank / panel textures: seam `#432219`, texture std 7-8.
   - Apply the house ink-line treatment the approved sets use on man-made props: 3 px hull = 0.00384 x camera distance.
   - Only real emitters above 1.0, with a bloom halo of 12-24 px.
5. **Dress the measuring room for the story (still1) and fix the period props.**
   - Add the instruments:
     - wall height gauge (toise) with greeked tick marks beside the chair;
     - arm-span scale painted along the wall;
     - foot-measuring board / stool;
     - compas d'épaisseur and sliding calipers laid on the table, large enough to read at phone size;
     - mug-shot camera on its tripod aimed AT the head-rest chair (now it faces away at frame left);
     - ledger shelves;
     - coal stove with pipe;
     - wall clock without numerals;
     - kepis on hooks.
   - Gas lighting: replace the street lantern with a period gas standard or a gasolier with visible gas pipe and arms.
   - Remove the abstract blue blocks / spheres and the blue stand at right.
   - Target 22-26 distinct objects.
6. **Records office and reveal.**
   - Break the uniformity:
     - cornice + pilaster every about 1.5 D on the cabinets;
     - a rolling library ladder on a rail;
     - 4-6 drawers pulled out at different depths;
     - card boxes stacked on the floor;
     - a clerk's desk with a green-shade lamp;
     - a gas bracket on the cabinet faces.
   - Move the camera off-centre (about 10-15 % lateral) and put a foreground prop 1-2 D from the lens. Fill the empty bottom-third floor band.
   - Make the runner navy `#26395e` with a red border; it becomes the cool block.
   - Reveal card (still3): build the full narrowing chain (big drawer → box → card). The hero card is cream, with two small portrait frames (front + profile, drawn in the cast's flat style) and ruled, greeked measurement rows. No zig-zags, no readable text.
   - Tablecloth: lower it to V about 0.35 navy or green baize, so it stops being the strongest blue in the frame.

## What already passes
Sharp, no DOF; no readable text; magenta <= 10 on all stills; one hard warm key with crisp cast shadows; reveal staged inside the lit
3D world; still2 is a genuinely beautiful hero location once the light and skies are fixed.

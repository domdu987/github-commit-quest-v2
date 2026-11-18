# QA-art, SET gate, set3d10 + cast10 (film 10)

## VERDICT: FAIL (FIX-FIRST)
The harbour is ready to show. The sea reveal is not.

The harbour is dense, warm and sharp and matches the film 9 look. The cast sheet is on-model. The reveal (shots 17-19), which is the key moment, currently reads as a 2D diagram laid over an empty purple sea, which breaks a client hard rule. The sea colour is also off-look.

## Scores (1-10)
| area | score | note |
|---|---|---|
| Set density / ornament | 8 | harbour, hull_side and hull_plank are rich. The sea is empty by nature. |
| Light & colour | 6 | Harbour DAY: 8. Sea: 4, flat saturated violet with almost no warm light on the water. |
| Composition / phone legibility | 5 | Harbour presets: good. topdown_sea: ships fill about 15% of the width, the torpedo is invisible, and the bottom 40% is dead sea. |
| Character acting (cast10 sheet) | 8 | Poses read; the admiral's plank_sheepish and jaw_drop work. The contact sheet still shows placeholder cast. |
| Key moment (reveal) | 3 | See blocking fixes 1-4. |
| Match to refs / film 9 | 6 | Film 9's reveal was big, close, emissive and in-world. Film 10's is far away and schematic. |

## Blocking fixes
1. **topdown_sea: reframe closer.**
   - Bring the camera in to a 40-50° oblique so the dazzle ship and the ghost span about 60-70% of the frame width (each hull ≥ 300 px long at 720 wide).
   - Put the torpedo's start just off the bottom edge.
   - Crop out the empty lower 40% and the grey ships in the far row (keep at most one).
   - Aim the frame so the low sun's warm glitter path crosses the water in the frame.
2. **Remove the dashed aim lines and arrowheads (A, B).** The yellow and cyan dashes with arrow tips are exactly the "2D infographic" the client banned. Replace them with in-world objects:
   - A: the real torpedo plus its bubble wake, running at a glowing floating buoy (the lead point, keep it) ahead of the real bow.
   - B: a second buoy, pale cyan, ahead of the ghost's bow; the torpedo/wake heads to it.
   - If any guide is still needed, use a faint light streak on the water surface (no dashes, no arrowheads, no rings).
3. **Make the torpedo and wake readable at phone size.**
   - Wake: a white foam band at least 20-25 px wide at 720, with bubble specks and a brighter head. It is currently a 3-4 px pale scratch in C and invisible in A/B.
   - Torpedo: dark body with a warm glint at the nose.
   - In C, leave a clear gap of open water (≥ 1 hull-width) between the wake and the real stern.
   - Give both ships a big white bow wave and smoke streaming aft, so the heading of the real ship and of the ghost is obvious without lines.
   - Also hide the periscope feather (bottom-left white "ʎ"); it reads as a glyph or letter.
4. **periscope_pov ghost: make it read as a ship facing the other way.** Right now it looks like a cyan wash over the right half of the hull.
   - Slide the mirrored ghost so its bow sticks out about 25-30% past the real ship's stern (into clear sky and sea).
   - Drop the body alpha to about 0.4 and add an emissive pale-cyan rim or edge line on the silhouette.
   - Give the ghost its own bow wave on the opposite end.
   - Keep the reticle; it is fine (ticks only, no text).
5. **Sea colour: warm it up.** The sea is about 76% blue chroma against 29% in the references and the film 9 warmth.
   - Desaturate the water base by about 35-40%.
   - Make lit swell faces pick up the warm key (warm peach/gold sun specular and glints spread over the near water, not only the horizon band).
   - Keep the troughs and shade blue-violet (hue 240-260).
   - Target: sea frames ≤ 50% blue chroma and ≥ 20% red+orange. Re-run harbour_hue.py on convoy_wide, periscope_pov, topdown A/B/C and torpedo_chase.

## Not blocking (fix in the takes)
- The contact sheet shows the placeholder cast. Re-check heads and scale with cast10 in the first takes.
- harbour_wide DUSK and quay_low DUSK are dark in the lower half. Add one warm lamp or bucket-fire pool near the camera.
- The hull_side stage 0/1/2 difference is modest at phone size. Animate the stage changes on screen, or cut to hull_plank.
- torpedo_chase: the wake is a solid white slab. Break it into foam clumps and bubbles once fix 3 is in.
- The harbour presets and cast10 are approved as they are.

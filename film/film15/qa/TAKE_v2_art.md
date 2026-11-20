# TAKE gate v2, film 15: QA-art (independent review): T1, T2, T3, T7
Reviewer: QA-art (opus), 2026-11-20. Sources: film/v3/film15b/{t1,t2,t3,t7}/take.mkv. I looked at frames every 10 frames (3 fps), at ±3 frames around each cut, flash and dissolve, and at full-res crops where something looked wrong.
g = first_g + frame index; t = g/30. The measured numbers (motion, sat/vivid/luma) all pass and are not repeated here.
Rules applied: QA_TEAM Stricter QA + §G/§H/§I, shot_plan v2, WORKER15b, FACTS.

| take | verdict | blockers |
|---|---|---|
| T1 | **FIX** | bar through faces g156-164 and g412-418; grey bench slices Dick g330-352 |
| T2 | **FIX** | the T2→T3 seam doesn't match (see T3); the newspaper floats with no hands g744-868; the whip g710-716 strobes |
| T3 | **FIX (hard)** | **full-magenta frames g857, 859, 863, 865** and a magenta card at g912; seam framing ~1.7x off; beats at 32.5 and 33.8 can't be read |
| T7 | **FIX** | "MEXICO 68" banners in the 1972 stadium g1880-1930; the coach isn't buried (stands behind the mound) g2046-2100; the bar vanishes g2032-2036 |

---
## T1 (g0-495): FIX
Works: BIGZOOM 1 is strong. It starts as a true bird's-eye of the town (houses, water tower, MEDFORD HIGH roof, track; kids are specks, <5 %) at g0, descends through the pines, and ends medium (~45 % height) on Dick + a boy at g132. It takes ~4.4 s with easing. The colour is vivid sky blue + maroon/amber. The set is dense (bunting, cars, bleachers, HIGH JUMP / BAR board, MEDFORD HIGH sign). Beats are on time: the flop crosses the bar g168-185 (5.6-6.2 s); the straddle bar falls at g399 (13.3 s); the clean flop is g465-489. Contact shadows are present. No mouths flap (Dick's "O" at g400 is a held reaction).

Fixes:
1. **Bar through faces (§G2, blocking).**
   - g156-164: the bar runs across the green-striped boy's chin/mouth behind it (he stands just past the far standard).
   - g160-164: the bar crosses Dick's chest/neck at take-off.
   - Fix: move the green boy off the bar line (≥ 1 m to the side, or lower him into the pit), and keep Dick on the near side of the bar until his hips rise.
2. **Falling bar sweeps through Dick's face g410-418 (blocking).** At g415 the falling diagonal bar covers his face. Fix: drop the bar on the far side of his head, or have him roll out first.
3. **Grey slab slices Dick g330-352 (§G2, blocking).** A lavender-grey bench/beam in the foreground cuts him off at the knees, so he reads as floating behind it with no feet. Fix: lower or remove that bench from the camera line, or raise the camera so his feet and shadow show.
4. **Character cut by the frame edge g438-446.** A giant Dick card (head ~28 % of the frame) passes the lens. Its top and bottom are cut off and it has an orange halo edge. Fix: make it a fast blurred foreground wipe (≤ 4 frames, with motion blur), or keep it fully in frame at ≤ 25 %.
5. Mid-take readability g230-330 (8-11 s): the two boys' straddles are tiny and are lost behind the foreground boxes/cones. Fix: bring the side-tracking path closer to the run-up so the straddling boy is ≥ 20 % of frame height for at least one straddle (around g240 or g288).
6. Minor (not blocking):
   - A "MEXICO 68" poster hangs on the Medford High wall in 1963 (g158-182; it also shows in T2 g711-716). This is anachronistic. Hide it in T1/T2; it is fine from T3 g918 onward.
   - The cards have a yellow/orange edge halo (g164, g442). Tighten the alpha matte.

## T2 (g483-868): FIX
Works:
- Over-the-shoulder push on the laughing coach, g483-564.
- Side tracking along the bleachers, with the coach pointing and miming, g564-687.
- Punch CLOSE-UP 1 at g683-710 (head ≤ 34 %, ~0.9 s, inside the plan).
- The flash at g741 (24.7 s) whites out into the page. "MEDFORD MAIL TRIBUNE / FOSBURY FLOPS OVER BAR / BACKWARD LEAP WINS" is sharp and readable on a phone.
- The pull-back at g800-850 shows boys, the reader and the coach laughing.
- Mouth/expression motion stays inside g534-706. The laughing grin at g708-710 is a held laugh face, which is OK.

Fixes:
1. **Newspaper floats (§G2).** The paper at g744-868 (and the reader's paper in the background, g573-640 and g800-850) has no hands holding it. It is a sheet hovering in front of a pair of legs on a red crate. Fix: add two hands/thumbs gripping the side edges, plus the reader's hat brim above the top edge.
2. **Whip g710-716 strobes.** With no motion blur, each frame lands on a different unrelated view (coach → reader → boys → an empty lawn with a grey bin). Fix: add directional motion blur on g710-716 (or render with shutter blur), and avoid the empty lawn + bin composition at g713-715.
3. **The seam needs re-framing:** see T3 fix 2. Either T2 or T3 changes; the cheaper option is to change T3.
4. Minor: there is no photographer visible for the flash at g738. Add a press photographer with a flash gun at the pit edge in g716-740.

## T3 (g856-1064): FIX (hard)
Works:
- The photo-comes-alive push at g866-890.
- The golden training flop at g873-909.
- The MEXICO 68 poster on the MEDFORD HIGH wall at g918-927, with the match-dissolve into night.
- BIGZOOM 2 (g930-1059) is the most beautiful frame range in the film: the city grid, a mountain silhouette, the floodlit bowl, beams, MEXICO 68 banners, the HIGH JUMP board. It ends on Dick medium at ~32 % of frame height, with officials, the 2.24 m board, and the red rival walking off at g1040-1050.

Fixes:
1. **Magenta frames (blocking, must re-render).**
   - g857, g859, g863 and g865 are 100 % magenta (failed or missing renders inside the seam handle and the dissolve).
   - g912 has a magenta rectangle over the pit (a card/plane with no texture) in the middle of the season dissolve.
   - qa_auto recorded these as "blank/blur by design". They are not by design.
2. **The T2→T3 seam doesn't match (blocking).**
   - Averaging T2 and T3 at g862 and g868 gives a clear double image. T3 is ~1.7x more zoomed in and its photo sits ~170 px lower at full res (Dick's face is at y≈710 in T2 and y≈880 in T3). T3 also has a coarser halftone and no headline in frame.
   - Fix: start T3's g856-868 at T2's framing (headline "OVER BAR" top edge in frame, photo face ~110 px wide at full res, same slight tilt), then begin the push-in after g868.
3. **Dick pops out in the season dissolve g904-914.** The DAY plate has no Dick, so he fades away mid-flop. Put Dick (or the next attempt) in the DAY plate too, and show the plan's falling leaves.
4. **Beats inside BIGZOOM 2 can't be read.**
   - The bar rising at 32.5 s (g975) happens while the fan is ~40 px wide.
   - The rival's fail at 33.8 s (g1014) is tiny and buried under floodlight bloom (g1005-1020 is almost a white-out over the target).
   - Fix: reach a medium-wide of the fan by ~g1000 (the descent can ease out earlier), and cut the bloom/beam intensity over the fan for g1000-1025. Then the knocked bar bouncing at g1014 reads at ≥ 15 % height, and the 2.24 m board change can be seen.
5. Minor:
   - The end framing at g1058 is Dick ~32 % tall. Push ~10 % more so it reaches the plan's medium (35-60 %).
   - At g890 the bar crosses behind Dick's torso card at take-off; keep him on the near side.

## T7 (g1796-2100): FIX
Works:
- The 1972 day crane: the "1972" banner, the cauldron, three kits (green / gold / red) flopping at g1826-1880.
- The sky-to-sky dissolve at g1938-1965 is smooth.
- Medford at golden hour with the coach "sighing" in front of the boys at g1966.
- Low side tracking of the coach run and the clumsy airborne flop over the pit at g2026-2036.
- The film's last image (coach in the sawdust, thumbs-up, MEDFORD HIGH behind) is warm and readable.
- The coach's "O" gasps at g1990-2012 are held expressions, not lip-flap. That is OK.

Fixes:
1. **"MEXICO 68" banners in the 1972 stadium (continuity/fact, blocking).** They show at g1880-1930 ("MEXICO 68", "CO 68" boards around the fan and on the rim). Replace them with "1972" or neutral banners; the "2.24 m" board is also odd in 1972, so show a different height or hide it.
2. **The coach isn't "buried to the chin" (g2046-2100).**
   - He stands behind the mound with his chest and shoulders above it, so it reads as standing, not sitting buried.
   - His pose is near-identical from g2056 to g2094 (~1.3 s; only the camera moves).
   - Fix: sink him so the sawdust line is at his chin, scatter sawdust on his cap, pump the thumbs-up 2-3 times, and add a blink/sigh. Push in so the coach head reaches ~15-20 % (medium); it is currently ~13 % and barely grows.
3. **The bar vanishes g2032-2036.** It is visible under the coach at g2030 and gone at g2036. Knock it off instead: the bar falls into the sawdust with the coach, which is a better gag.
4. **TUMP spray is weak at g2040-2050.** Only a few flecks fly up. Make a big sawdust burst (a plume around 0.5 m, falling over ~12 frames, with shadows).
5. Minor:
   - The 1972 jumpers' "land smiling with thumbs up" isn't readable after g1856 (too small). Hold one landing at ≥ 15 % height around g1840-1860.
   - The coach is cut by the right frame edge at g2024.

---
## Summary of g-numbered fixes
- T1: g156-164 (bar across the boy's face and Dick's chest), g410-418 (bar over Dick's face), g330-352 (grey bench slicing Dick), g438-446 (giant halo card cut by the edges), g230-330 (straddles unreadable), hide the MEXICO 68 poster g150-190.
- T2: hands on the paper g744-868 (+ background reader g573-640, g800-850), motion blur on the whip g710-716, photographer for the flash g716-740.
- T3: re-render magenta g857/859/863/865 and g912; re-frame g856-868 to T2's page framing (scale ~1/1.7, up ~170 px, headline in frame); Dick in the DAY plate g904-914; make the bar rise (g975) and the rival's fail (g1014) readable, with less bloom g1000-1025.
- T7: remove MEXICO 68 from the 1972 stadium g1880-1930; bury the coach to the chin + animate the thumbs-up g2046-2100; the bar falls instead of vanishing g2032-2036; bigger sawdust spray g2040-2050.

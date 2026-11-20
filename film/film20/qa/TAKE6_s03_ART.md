# TAKE6 QA-art: T03 = s03, BIGZOOM 1 + crane (g 170-411, 5.93-13.47 s)

**Verdict: FAIL (cheap fix).** The camera, the composition and the colour are good. Four set and material defects keep it from passing. None of them needs a camera change: re-render the same move after the prop and material fixes below, then check it on a phone sheet plus a contact sheet.

## Inputs
- Frames: scratchpad conf/takes/s03/frames, all 242 (g 170-411).
  - Viewed at full size (720x1280) and at 360x640.
  - Contact rows every 8 frames, plus crops of g 198, g 300 and g 370.
- Joins: s02 g 178 and s06 g 398.
- References: board.jpg, the ref_shorts sheets, QA_TEAM §G-§I, shot_plan T03, TAKE3_ART and TAKE4_ART.
- Stats (every 10th frame): mean saturation 0.547 and mean luma 100.6, so §G-1 passes.
  - The start is lower: saturation is 0.40-0.43 over g 170-190 and dips to 0.38 around g 360.

## Scores (1-10)
| Opening wide | Eiffel find -> subject | Landing | Crane to workers | Light/colour | Set richness | Defects | Overall |
|---|---|---|---|---|---|---|---|
| 7 | 6 | 7 | 6 | 8 | 7 | 4 | 6 |

## What works
- **Opening wide (g 170-178): it reads.**
  - The sky with clouds, the Trocadéro with its dome and two towers, and the block rows of Paris are all in frame.
  - The Seine is now in frame as a saturated blue band with bridges, which fixes the round-3 and round-4 note.
  - The two rising orange legs on their piers, the yard huts, the cranes and the long shadows are also there.
- **The descent is one continuous move.** It goes from the city to the yard to the foot of the leg, and the orange-on-blue signature is clear from the first frame.
- **Landing (g 260-300):**
  - Eiffel stands full-body, smiling, with a hand raised and a contact shadow. He is about 30-33 % of the frame height.
  - Barrels and the masonry pier are on the right, and the lattice frames him from above.
  - This is a strong low-high frame on the channel. §G is clean: nothing crosses his face.
- **Light:**
  - A warm low sun gives long blue shadows and an orange key on the iron.
  - Deep blue sky behind the riveters, with warm rivet glows at the hot rivets. The warm/cool contrast is good.
  - Rim light reads on the workers' blue coats.
- **Crane end (g 380-411):** three riveters with hammers and hot rivets sit on a platform inside the lattice against deep blue. It reads "workers riveting high up".

## Defects / fixes (blocking)
1. **White blob, bottom-left, g 188-210.**
   - A white low-poly disc about 150 px wide with 4-5 black dots floating just off its rim. It is probably a sheep or tarp card seen from above, with its legs offset.
   - On a phone it reads as a hole or a blob, and the dots float, which breaks §G-2.
   - **Fix:** delete it, or replace it with a grounded prop such as a stone pile or a covered stack with a contact shadow.
2. **Black deck underside, g 362-411.**
   - The platform bottom renders as a flat, unlit black rectangle covering about 25-30 % of the frame. That frame is the payoff of "สูงที่สุดในโลก".
   - **Fix:** give the deck underside wood planks with a bounce or fill (warm rivet-glow up-light from below), or tilt so less of the underside shows.
   - **Also:** the small white bulb or teardrop hanging just above the deck (g 346-380, top centre) has no fixture. Give it a hanger and an emissive glow, or remove it.
3. **Bare white "flag pole", g 186-240.**
   - A tall white pole with no flag stands right of the table and Eiffel, then slides across the left edge at g 234.
   - It is a meaningless bright line that pulls the eye away from Eiffel.
   - **Fix:** add a tricolour flag (which tells us "France") and darken the pole to iron or wood, or remove it.
4. **Dark scatter props and outline halos.**
   - The wheelbarrow in front of Eiffel's feet (g 250-310) has a thick black card outline, so it reads as a black scribble at phone size, right under the subject.
   - **Fix:** thin or remove the outline, or swap in a 3D wheelbarrow.
   - In the opening yard (g 170-180), the near-black bits between the huts are fewer than before, but they still read as debris in the bottom third. Clear the smallest ones.

## Notes (non-blocking, do with the re-render if cheap)
- **Eiffel is not findable in the far wide (g 170-180).**
  - He becomes findable only around g 194, as a tiny figure near the white table.
  - **Fix:** add a warm lamp or a small red flag at the table so the eye lands there in the first frames.
  - The extreme wide is still a quick flash: about 16 frames to the leg. Hold it 6-8 frames longer.
- **The far bank behind the Seine is a flat grey-lavender plane with a peach sky band** (sat 0.40). Push it toward blue or green, and add a few roofs or trees.
- **The white table roof in the foreground (g 234-300)** is a large, flat, blank white wedge at bottom-right. Add the red trim stripe pattern or texture, or warm it slightly.
- **The leg reads curved/bent at g 186-200** from the wide lens and the low angle on a long diagonal member. It is acceptable, but a slightly longer lens there would straighten it.
- **Crane path (g 318-360).**
  - The camera leaves the leg, drops to ground level to look at the Trocadéro tower and the sky, and then finds the scaffold. It reads as a drift, not as "up the leg".
  - Keep the leg in frame through the whole rise if it is re-timed.
  - Eiffel is half-cut at the right edge at g 312-318. That is acceptable during the move.
- **Scaffolding:** the riveter cards overlap one another (heads stacked, g 380-411), and a scaffold post sits right beside the top worker's face. Nothing actually passes through a face, so there is no clipping. Spread the three cards about 40 px apart.
- **Joins:** the s02 to s03 and s03 to s06 dissolves are clean. Both sides are warm, with no flash.

## Re-submit
Re-render with fixes 1-4. Pass on a phone sheet (every 0.5 s) plus close crops of g 198, g 290 and g 380.

# QA-art s03 (vista: Yan pennants rise over the plain, 5.20-9.89 s), TAKE gate, Vista round 4 — FIX-FIRST
I reviewed take.mkv at 6 fps (art11/f/NNN.png, g = 147 + 5*(NNN-1)) at full size and on art11/psheet_1-4.jpg (360x640, cyan line = y 880).

## Earlier changes
1. Pennant count, scale and placement: PARTLY done. The flags now grow from the pole top and are capped in size, which is good. But the camera drifts right and down over the near town blocks, so at the end (g 292, art11/f/030.png) only about 7 flags are in frame, not the 30 or more I asked for. The "51 up by g 296" are mostly outside the frame. s04 then opens on about 35 flags.
2. Pop animation: Mostly done. No flag lies flat any more. But the nearest pole at the bottom right (g 272-282, f/026-028) leans about 30° across the lower third, and its cloth is cut by the right edge. On the phone it still reads as a falling pole.
3. Material: The pennants are DONE (dark silk, red border, lit by the dusk; they read as cloth). The moat is now a textured, glinting gravel or mud ring, which is acceptable. The navy slabs are NOT done. The flat navy ramp/plank is still inside the first town (g 147-200), and flat navy L-shaped strips lie at the pole bases of the later towns. At g 277 (f/027.png, bottom right) a navy slab carries a lump of yellow cubes, which reads as a placeholder prop (rule 2).

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 5 | 7 | 5 | n/a (no cast) | 6 |

On the phone you see a warm dusk plain with lit towns, and a handful of black flags appear near the lens over the last second. The line is "Yan took 70+ towns". The image says "a few towns" instead.

## Verdict: FIX-FIRST
1. **End framing shows the whole plain (g 255-296):** Stop the drift down into the near blocks. From about g 240, ease the camera up and back (or pull its look-at toward the horizon) so the last frame looks over the plain with 25 or more black flags visible, matching s04's opening field. Keep the eased move; no pulse.
2. **Nearest pole (g 262-292):** Keep every pole out of the bottom third and at least 40 px inside the frame edges. Either skip the nearest town's pennant in this shot or pop it before it reaches the lower-right corner.
3. **Navy slabs (set-level, also affects s04 and s25):** Give the navy ramp/plank and the L-shaped pole-base strips an earth or timber texture (or hide them), and remove the yellow-cube lump at the pole base. Check the last 10 frames for zero flat navy areas.

## Notes
- The bright Jimo "sun flare" on the horizon is pretty, but it is stronger than any town light. Less bloom would read more like a town.
- Frame-diff median 5.8 / p90 6.5, below the 9 guide. The move is visible, so this is fine for a vista.

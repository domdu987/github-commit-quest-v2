# QA-art round 13 s24: FIX-FIRST
s24: the comic rout in the Yan camp (g 1807-1882). I extracted all 87 frames (g = 1801 + n). I judged them on a 180x320 phone sheet every 5th frame (about 6 fps), on action-band crops every 3rd frame, at full size on the centre, left and bottom regions, and with two ground measures: smooth 20 px blocks and a chroma mask.

## Asked fixes
1. **Ground ≤30 %: DONE.** Plain ground is at most 17 % (median 11 %) with the block method, and at most 16 % with the chroma mask. The floor is now dressed with stones, pots, sacks, helmets and reed bundles from the first frame. The bottom reads as a ransacked camp. It is busy, but grounded.
2. **At least 2 visible falls: NOT DONE on the phone.**
   - **Fall 1: reads.** The moustached soldier at the left sits with his legs splayed at g 1855-1873 (x 0.05-0.30, y 0.66-0.78).
   - **Fall 2: does not read.** The team puts the second and third falls at x 0.6-0.72 (g about 1821 and 1843). On the render, the soldier who sits at g 1839-1851 (x 0.71-0.83, head at y about 800) is directly behind the fire-pit flame cards and the tipped cart, so only his head shows above the flames. I find no tile on the phone sheet with two soldiers visibly on the ground.
3. **Warm props no wider than about 20 % of the frame: PARTLY DONE.**
   - **Flying helmets and pots: DONE.** They now reach about 10-18 % (largest about 18 % at g 1876).
   - **Chariot: NOT DONE.** The tipped chariot is wheel plus box about 29 % of the frame width, and about 58 % with the pole, at g 1864-1882 (x 0.08-0.66). In the last second it becomes the dominant orange shape across the bottom centre, competing with the fire pit.
4. **The rout reads as a comic scatter: YES, with a note.** Terrified faces, flying helmets and pots, the tent folding and the cart tipping all read as comic and bloodless. The soldiers still clump in the centre band rather than streaming out to the edges. I accepted the scatter in round 12 and do not re-raise it.

## §G checks
- Nothing hangs still in mid-air: the flying props move on every frame.
- No character is cut in half by an edge.
- Flying helmets pass in front of bodies (g 1865) but not across a face long enough to read.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 6 | 8 | 6 | 6 | 7 |

## Verdict: FIX-FIRST (2 blockers, each measurable)
1. **Second fall in the open:**
   - Move the g 1839-1851 sit-down at least 120 px clear of the fire pit and the cart. Put it on the clear floor at front-right, x 0.75-0.92 and y 0.62-0.75 (the barrels/tent side), or front-left at x 0.30-0.45 before the cart arrives.
   - Hold it for at least 12 frames, with the whole body at least 120 px tall and unoccluded.
   - Pass check: one 0.5 s phone tile in g 1850-1870 shows both the moustached soldier and this one on the ground.
2. **Chariot scale:** Scale the chariot so that the wheel plus box is ≤ 20 % of the frame width (≤ 145 px) and the pole is ≤ 35 %, measured at g 1870, 1876 and 1882. Or let it roll farther back, beyond the fire pit.

## Notes (not blocking)
- The fire-pit flame cards are flat red wedges that sit at frame centre for the whole shot. They read, but they hide action. A bit lower or narrower would free the centre.
- Frame-diff (team): median 10.01, p90 15.51. Good.

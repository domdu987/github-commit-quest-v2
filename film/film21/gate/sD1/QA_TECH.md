# QA-tech TAKE gate: segment D1 (team 7, g542-642): FAIL
(Transcribed by the director from the QA-tech (Sonnet) hand-back; the agent did not save the file itself.)

## Blocking
1. **g542 to about 575: the sign does not read.** "KING'S TREASURY" shows only as "'S / URY", cropped at the left edge; it leaves the frame by about g562.
   Fix: re-aim the arc so the full two-line sign is centred for about 1 s.
2. **g542 to about 600: the coin counting is not visible.** His hands are hidden behind the table slab, and from g630 one hand rests on his hip. The coins read as white chalk.
   Fix: raise the camera to table height and tint the coins gold.
3. **Whole take: no rim light on the card.** Only dark ink shows at the edge. See the director note below.

## Recommended
4. **g542 to about 590:** the table slab and its underside fill about 45 % of the frame, and his head is only about 12 % of frame height.
   Fix: lift the camera, or move closer.
5. **g603-611:** there is no clear look-up beat before the laugh at g612.
   Fix: add about 0.3 s of head and eyes up.

## Passes
- **Whip:** the qa_auto blur and pop flags on g637-642 are the planned horizontal whip, which is acceptable.
- **Heads:** all within y 520-740.
- **Face size:** 12-21 % of frame height.
- **Laugh:** a fixed laugh drawing, no lip-sync, with bounce.
- **Floating:** none.
- **Colour:** sat 0.637, luma 108.
- **Pops:** none outside the whip.

## Director note (2026-11-20)
- **Re-assigned:** D1 is re-rendered by team 2, starting from team 7's scripts, with fixes 1, 2, 4 and 5.
- **Issue 3 (rim light):** this is a SET/CAST limitation, not a take defect. Emission cards cannot take a scene rim, and the puppet `rim` key only halos the limbs (set3d21/API.md §12).
  - It is NOT waived. It goes to QA-art at the FINAL gate as one film-wide question with §I 2.
  - It is listed as an open item in the client report.

# QA-tech round 11 s22: FAIL

Checked: g 1683-1742 at 6 fps plus g 1729-1742 every frame (25 frames). Sheets at 240x427 with a y=860 line. Full-size look at g 1742. Pixel measures on the frames.

## Blockers
1. **Ox head leaves the left edge, g 1731-1742 (director's must-fix NOT met).** Cream muzzle touches x=0 at g 1730-1734. At g 1735-1742 the head sits at x 0-270 and the left half of the face and the left horn are cropped (g 1742: face spans x ~0-270). The brief asks for the head at x 0.08-0.45 (x 58-324). The head is only inside that range at about g 1683-1700. Rule 4 (subject stays in frame) and the mandatory "whole head" are breached. Fix: truck or pan so the head holds x 0.08-0.45 through the +15 % hold, and shift the ox head right or slide less.
2. **Chin and mouth below 860, g 1731-1742 (hard check: no face or mouth at y > 860).** The open mouth and tongue reach y ~900-1000 from g 1731 (g 1733-1737 the mouth is at about y 900-990, g 1742 the mouth bottom and chin are at about y 935). The cream muzzle's lowest pixel passes 860 at g 1733 (862) and reaches 882 at g 1737. The meta value "max_chin_y hero 595" is wrong again. Before the punch the mouth already sits at y ~810-870 (borderline). Fix: tilt the camera down or move the ox up so the chin stays at y ≤ 860 in every frame, and re-measure the real mouth, not the head box.
3. **Tripod brazier is still in frame (director's must-fix NOT met), whole take.** At the right edge, x ~600-720, y ~430-750, a dark navy slab on a tan leg holds a tall flame. It is visible at g 1683-1742 and is an untextured placeholder (rule 2). The only flame in frame sits on it, not on a tail (rule 3). The flame is detached from any tail and about 40-60 px from the soldier's head (g 1742: flame x 600-690, helmet right edge x 520, a 80 px gap, but it is a floating brazier flame). Fix: delete the brazier and its flame. Parent a flame card to the ox's tail tip, trailing backward, behind the ox, with a warm light.
4. **Soldier staging (director's must-fix NOT met), whole take.** He stands at x ~0.50-0.72 (g 1742: helmet x 340-520, body x 340-490), overlapping the ox's body and rump, which hides the dragon silk. He faces the lens (square), not front-3/4 toward the ox. A second small ox head with a snarl sits behind his hip (g 1738-1742, x 470-590, y 570-690), which reads as a glitch. A gold bundle sticks out of his shoulder. Fix: move him to x 0.65-0.90, behind the ox, yaw toward the ox, clear of the body, tail and flame. Remove or move the stray second ox head.
5. **Glint reads as a flare, g 1732-1737, optional but visible.** A white star sits on the coat and horn root and becomes a large flare at x 0-100 at g 1735-1737. It is not on a blade tip. Optional per the director. If kept, put it on a blade tip, 60-90 px.

## Passed checks
- Sky: measured RGB about 19,81,183 (target about 25,76,165): blue, moonlit, OK.
- Plain ground: about 25-30 % bare dirt below y ~900 in the full frame (a note, not a blocker at ≤ 30 %). Please crop it with a dark fg prop.
- No text in frame, no magenta. No zoom pulsing seen: one held punch-in from g 1731.
- Mouths: soldier's mouth is still (O shape). Ox mouth stays open (rage face), no flapping.
- Frame-diff re-measure (90x160 grey, g 1683-1741): median 11.78, p90 16.85, min 5.81. The director's 11.46 and 16.34 agree within noise. Passes.

## Notes
- Hard-check summary: face at y > 860 FAIL (item 2), placeholders FAIL (item 3), flames on tails FAIL (item 3), subject in frame FAIL (item 1), ground OK, pulsing OK, mouths OK, no text OK.
- The ox's horns carry gold blades with red wraps at g 1683-1730, so the blade continuity from s21 is now OK.
- Soldier's face is not cut off, sweat drop and mouth read well.

Fix list for the next take: (1) no brazier, flame on the tail; (2) ox head x 0.08-0.45, chin ≤ 860 all frames; (3) soldier at x 0.65-0.90, front-3/4 toward the ox; (4) drop the stray ox head; (5) glint on a blade tip or omit.

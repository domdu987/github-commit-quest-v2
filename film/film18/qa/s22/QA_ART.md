# QA-art round 12 s22: FIX-FIRST
Shot: REVEAL close-medium, "หางลุกเป็นไฟ เขาติดมีดวาววับ". I reviewed take.mkv g 1677-1747. I looked at every 5th frame (about 6 fps) from g 1683 to 1742 and every frame from g 1729 to 1742. I viewed them at full size (720x1280), on 240x427 phone sheets, and with guide lines at x 0.08/0.45/0.65/0.90 and y 860. I took the pixel measures on the decoded frames.
**phone_sheet.jpg is still the same file as contact.jpg (same md5).** The script-side projection in QA.md ("mouth worst y 808, head x 0.16-0.41") does not match the render after the punch.

## Asked fixes
1. **Ox head x 0.08-0.45, mouth y ≤ 860 in every frame: NOT DONE after the punch.**
   - **g 1683-1732: OK.** The lowest pixel of the tongue is at y 804-842, so the mouth outline is at about 820-855. The muzzle sits at about x 0.12-0.55 (the face runs a little past 0.45 on the right, which is acceptable).
   - **From the g 1731 punch, the head drops and slides left.**
     - The lowest tongue pixel is at y 865 (g 1733), 879 (1734), 912 (1735), 901-905 (1736-37) and 910 (g 1742). The dark mouth outline is about 15 px lower than that.
     - At g 1742 the head spans x 0-300 and the left edge cuts the cheek and the eye.
   - This is the same failure as round 11.
2. **Soldier at x 0.65-0.90, behind the ox's rear, turned toward the ox, clear of the tail and flame: PARTLY DONE.**
   - **Depth: DONE.** He now stands behind the ox, and the caparison overlaps his lower torso. No soldier pixels are between the lens and the tail or flame.
   - **Position: NOT DONE.** For g 1683-1731 his face is at x 0.82-0.97 and his shoulder touches the right edge. He only reaches x 0.64-0.82 after the punch.
   - **Facing: NOT DONE.** He is still square to the lens with his eyes on camera, not on the ox. He is the soldier who must react to the ox, so the calibration exception to rule 7 applies to him.
3. **Tripod brazier: DONE.** For g 1736-1747 there are no tan-legged tripod or navy cone pixels at x > 0.80. The dark diagonal shape at the right edge is the wall ladder, which belongs to the set and is fine.
4. **Blue moonlit sky: DONE.** Over y < 120 the sky measures RGB 25,82,178 (g 1683) to 38,76,159 (g 1742). The moon and clouds are present.
5. **Reveal reads on a phone: NOT YET.**
   - **Blades: read.** The gold horn blades with red wraps show in every frame.
   - **Flame: does not read as this ox's.** Its tail flame is off-frame for g 1683-1732: only a 5-10 px red sliver shows at x 710-720. It enters only at g 1733-1742, cut by the right edge (x 650-720).
   - **Tail bundle reads as a prop.** The straw bundle runs diagonally across the soldier's chest and hands (g 1683: x 590-720, y 420-560). On the phone it still reads as "soldier holding a broom".
   - The flames you see are the other oxen's tails at the left, so "THIS ox's tail is ablaze" does not land until the last 10 frames.
6. **Ground: BLOCKS.**
   - **Measure:** Plain dirt is about 35-40 % of the frame (measured 33-38 % by ground colour). The full width from y about 870 down to 1280 is plain, plus the strips between the legs. After the punch it is about 32-34 %.
   - **Not dressed:** It is bare foreground road with spots and long shadows, and nothing sits on it. It is not "night ground at the base of the walls": the walls are far back, and this is the lower 1/3 of the frame in front of the ox. It is over 30 % and not dressed, so it blocks.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 5 | 8 | 4 | 6 | 5 |

## Verdict: FIX-FIRST (3 blockers, each measurable)
1. **Punch framing:**
   - Re-anchor the g 1731 punch on the ox head (centre about x 0.33, y 0.55), cap it at +10 %, or truck the camera to keep the head in place.
   - Check on rendered frames (not by projection) that from g 1683 to 1742 the mouth outline stays at y ≤ 860 and the muzzle's left edge stays at x ≥ 58 px. g 1733-1742 is where it fails now.
2. **Ground:**
   - Bring plain ground to ≤ 30 % in every frame (measure g 1683, 1712, 1742).
   - Best fix: put a dark, lit fg prop low in frame, covering at least 8-10 % of the frame in the bottom third, for example a dropped wine jar and cups, an overturned stool, a spear rack or a sack, or a dark ox-shadow band.
   - Lifting the ox so that the ground below the hooves shrinks also works, as long as item 1 holds.
3. **Reveal staging (tail and soldier):**
   - Keep the ox's own flame card at least 80 % in frame, with x ≤ 0.97, from g 1683 to 1742.
   - Route the straw bundle so that it does not cross the soldier's torso or hands. It can trail behind him or above his helmet.
   - Hold the soldier's whole figure at x 0.65-0.90 for the whole take, not 0.82-1.0.
   - Yaw him about 30-40° toward the ox, with his pupils on the ox.
   - Pass check: on the 240x427 phone sheet, the flame visibly grows out of the hero ox's tail and the soldier holds nothing.

## Notes (not blocking)
- The glint star at g 1733 sits on the coat and horn root, not on a blade tip. It is still optional.
- A small brown second ox head behind the soldier's hip (g 1738-1742, x 540-600, y 560-690) still reads as a glitch. Push it back or hide it.
- The grade and the rage face are good. Keep them.

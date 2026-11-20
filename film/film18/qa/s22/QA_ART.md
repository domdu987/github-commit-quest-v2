# QA-art s22 (REVEAL close-medium: "หางลุกเป็นไฟ เขาติดมีดวาววับ", 56.08-58.04 s), TAKE gate re-render — FIX-FIRST (reveal, strict; regressed)
I reviewed take.mkv at 6 fps (art9/gNNNN.png, g 1677-1747) at full size 720x1280 and on the 360x640 sheets art9_phone_0-1.jpg (cyan line = y 880). "วาววับ" = g 1732.

## Earlier changes
1. Punch-in keeps the full face and tail flame in frame: NOT DONE. At g 1742-1747 the hero's face is cut in half by the left edge (x 0).
2. Frozen soldier, full figure at the right, 3/4 toward the ox: DONE WRONG. He now stands IN FRONT of the ox's body at x 0.42-0.75, square to the lens, calm, looking at the camera. He hides the dragon silk. The hero's tail bundle sticks out behind his shoulder, so on the phone he seems to carry a broom, with a "torch" flame beside it.
3. Glint on the word: PARTLY done. A 4-point star appears at g 1732, but on the coat/horn root, not a blade tip. At g 1737 it becomes a tall white vertical spike at the left edge (x 70-130, y 250-620) with a white bar across the ox, which reads as a render glitch.

## Also
- **Night grade:** The sky is near-black (RGB about 17,24,62), the same as s21. The passed s14/s15 have a blue moonlit sky (about 25,76,165). Only s21 may be darker, per the director.
- **Caption band:** The hero's mouth is at y 950-1060 in most frames. The meta value of "hero chin 741" is wrong.
- **Placeholder:** A tan-legged tripod brazier with a flat navy cone sits at the right edge (g 1737-1747, x 630-720, y 500-830).

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 4 | 5 | 3 | 4 | 4 |

On the phone you see a calm soldier posing in front of an angry ox, holding a broom next to a torch. Neither "tail on fire" nor "glinting blades" reads.

## Verdict: FIX-FIRST
1. **Staging:** Move the soldier off the ox, to the right-hand ground at x 0.65-0.90, a little further back than the ox. Turn him front-3/4 TOWARD the ox (eyes on it), with a recoil pose and the sweat drop, head above y 880. Keep the ox's body, tail rope, bundle and its trailing flame unobstructed: the flame streams back from the bundle tip and nothing stands between the lens and the tail. Remove the right-edge tripod brazier.
2. **Ox framing, whole take including the punch:** Hero face at x 0.08-0.45 and chin at y 860 or above in every frame. The +8 % punch from g 1731 must keep x 0.03 or more on the face. Pan or truck with the push so it does not drift out left.
3. **Grade + glint:** Bring the sky back to the s14/s15 blue moonlit grade (same sky object/colour, moon may stay off-frame). Replace the g 1737 white spike and bar with clean 4-point stars (60-90 px) on the two blade TIPS, firing from g 1732 to 1739.

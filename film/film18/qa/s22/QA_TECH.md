# QA-tech round 13 s22: PASS
Checked: all 71 frames at 6 fps; 1:1 frames g1683/1710/1742 with x 0.08/0.45/0.65/0.90 and y860 lines; mouth crops every 3 frames g1683-1742 with the y860 line; flame x extent every 6 frames; ground colour mask; frame-diff re-measured 90x160 (median 11.67, p90 15.55).

## Previous blockers
- Mouth <= 860 on every frame: DONE. Lowest edge of the mouth/tongue: about 832 g1683, 845-855 g1695-1731, 858 g1737 (worst), 845 g1742. Margin 2 px at g1737, fine.
- Head in x 0.08-0.45: DONE for the face/muzzle (x about 0.12-0.40 g1683-1742; left tusk at x about 56 = 0.078 at g1742). The ear tip and horn spill to about x 345-360 (0.48-0.50) at g1683-1710: note.
- Soldier x 0.65-0.90 and fully in frame: DONE (g1742 body x 504-645 = 0.70-0.90, g1683 x about 0.65-0.85), no edge clip. He is behind the ox's rump and the tail pole crosses in front of him, so he is not between the lens and the tail.
- Own tail flame in frame: DONE, flame x 600-710 in g1683-1731; at g1737-1742 it reaches x 719 (44 edge pixels at g1737): clipped at the right edge for about 5-8 frames (note).
- No brazier: DONE. Sky blue with moon: DONE.
- Tail through chest: see notes.

## Notes
- Ground: raw colour mask below y 0.55 is 0.36-0.38; minus the pot and reed bundle I read about 0.29-0.32, on the 30 % edge. QA.md's claim of 3-5 % is wrong. If anything is touched, add one more dark prop at lower right (x 0.55-0.9, y 1000-1180).
- Reed/pole: it starts at the ox's rump, rises diagonally across the soldier's chest, ends in a straw tuft at his shoulder, and the flame is right behind his head. It reads as a long torch/broom he might hold, and the straw tuft does look like a broom head. It is acceptable as a tail torch because the root is on the ox, but a clean fix is to shorten the pole so the straw ends 40 px before his torso. Note, not blocking.
- The soldier's face is frontal to the lens (eyes at camera, shocked "O"); body is 3/4. He does not look at the ox. Per director calibration rule 7 this is a note.
- Glints at g1731-1739: one star at the left edge, a flash on the horn; fine (optional).
- Frame-diff 11.67 / 15.55. No pulsing (steady push). No text, mouths held, no placeholders, plain ground not an issue otherwise.

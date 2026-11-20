# QA-tech round 14 s22: FAIL
Checked: all 71 frames at 6 fps; 1:1 frames g1683/1713/1742 with y860 and x 0.08/0.45/0.80/0.92 guides; mouth tongue+outline mask on every frame g1683-1742 (confirmed by eye on g1725/1728/1731/1737 crops); flame/soldier crops g1683/1713/1742; sand mask; frame-diff 90x160 (director 10.95 / 15.05).

## Blockers
1. Flame staging, g1683-1742 (entire take): the tall tail flame stands directly against the soldier and does not come from the hero's tail.
   - Gap flame-to-soldier: about 12-15 px at g1683 (flame right edge x ~547, soldier shoulder/head x ~560-567); 0 px at g1713; overlapping the soldier's shoulder/torso edge at g1742 (flame x 480-573 vs soldier body from x 567; the flame also covers the glow outline). Required: >= 60 px, no "torch" read.
   - The flame base floats about 20-30 px above the hero's own tail tuft (the unlit straw bundle at x 330-390 / 370-460, y 460-470); it is rooted behind the neighbouring ox's neck, so the hero's tail is unlit and the flame is a free-standing column next to the soldier. It reads as a torch/brazier beside him (rule 3: flame parented to the tail tip, never free).
   - Fix: parent the flame card to the hero's tail tip (the bundle at its rump), trail it backward at the rump line; place the soldier at x >= 0.86 or move the flame/tail left so the flame's right edge is <= soldier left edge - 60 px (flame <= x ~500 at the end) on every frame; keep the whole flame <= x 700 and in frame.
2. Soldier is not turned toward the ox: body frontal, eyes and shocked "O" at the lens on every frame (director calibration: soldiers must visibly react to the oxen). Fix: yaw him 30-40 deg toward the ox with pupils on the ox (can be combined with fix 1).
3. Ground above 30 %: plain sand below the oxen y ~640-1280 minus pot and bundle = 33-34 % on a sand/low-variance mask (g1689 0.343, g1713 0.342, g1742 0.343; stable all take). Limit 30 %. Fix: a third dark prop at lower centre-right (x 0.45-0.9, y 950-1200), or tilt up ~40 px; QA.md's 3-5 % is wrong.

## Asked checks (pass)
- Mouth lowest pixel <= y 860 on every frame g1683-1742: PASS. Tongue bottom 794-844; mouth outline 816-846 (max 846 at g1707-1713, 840-862 only in my first heuristic and 832-840 on the eyeballed g1725-1737 crops). Margin >= 14 px.
- Head at x 0.08-0.45: face/muzzle x ~0.18-0.46 (horn/ear spill to ~0.50): OK, ear note.
- Soldier fully in frame at x 0.78-0.93 incl. glow, head to feet in frame: OK.
- Flame in frame: yes, x 0.67-0.78 (not clipped).
- Blue sky and moon: yes. Warm and cool in the same frame, rim on soldier (light blue) and oxen: yes.
- No mouth movement (held drawings), no placeholders, no text. Frame-diff fine, no pulse (steady push).

## Notes
- The blade glint star g1731-1739 is on the neighbour ox's head/coat, not a blade tip (optional).
- Pot (left) and reed bundle (bottom) have a soft/glowy gradient but are lit and warm: fine.

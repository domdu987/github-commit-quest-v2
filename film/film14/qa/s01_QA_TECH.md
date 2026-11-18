# s01 QA-tech (TAKE gate, strict)  VERDICT: FAIL

Checked: 187 frames, 6 fps (37 frames) plus g 63-69 and 120-126 at full size, plus numeric per-frame diff/sharpness at 360x640.

## Verified OK
- Cuts happen exactly at the planned frames: frame-diff spike (mean abs diff 45.5 and 35.7, against 5-8 elsewhere) at g66 and g123, with g65/g122 the last frames of the old shot. QA_AUTO's "no visible change" was only a threshold artefact; the cuts are real and on plan.
- No blur: Laplacian energy stable per shot (min 560 to 713, no dips). No frozen runs (min inter-frame diff 3.0), no pops outside cuts, no black or magenta frames.
- Heads: highest-low head (shot 2 youth/woman chins) is around y 700, shot 1 and shot 3 heads around y 450-720. None near y 880.
- Mouths: no talking mouths; only held laughing shapes. OK.
- Farmer on ladder (shot 1): feet on rungs, ladder fixed, no slide. Hive in his hands g0-~40, swap to the hung hive at ~g44 is clean.

## Issues
1. g66-122 (shot 2) stray grey tub / basket floating at head height between the woman and the youth. It covers the kid's face and torso (kid is the planned v_kid_laugh_point). Fix: remove or lower the tub to the ground and put the kid clear of it, or move it behind the cards.
2. g66-122 (shot 2) foreground clutter: guinea fowl, squash leaves, pumpkin and sack fill the bottom 25-35 % of the frame (g66-90 worst, g100-122 leaves/fowl wing still cover the corner). It is close to the action and the fowl/wing shape reads as a black blob. Fix: move the camera or clutter so only low grass/stones are in the lower third, or push the camera past them.
3. g66-122 (shot 2) the farmer and the hung hive are tiny (~5 % of the frame width, behind the tin roof), so "villagers laugh at THE FENCE" does not read. Fix: reframe so the hive and the farmer on the ladder sit larger behind the villagers (camera closer or lower and off-axis), or add a long lens crop on the hive.
4. g66-122 (shot 2) eye-lines: all four villagers look straight at the lens with eyes squeezed shut; the plan says they point toward the fence. The youth's arms are held out sideways like a T, not pointing, and nobody points screen-left. Fix: swap to the point poses, and turn the cards (flip x, or yaw) so faces and arms point screen-left toward the hive.
5. g66-122 (shot 2) stray stick/pole poking out under the woman's feet (about x 310, y 940 at g84), looks like a spike through the shoe. Fix: hide the stray prop or move it.
6. g66-122 (shot 2) contact: the kid and the oldman have weak contact shadows (kid's feet float slightly behind the tub, oldman has no clear shadow under the robe). Fix: raise shadow opacity and size under every card, as on the woman.
7. g0-65 (shot 1) the "hook_close" is not close: the farmer is about 15 % of the frame width, hive roughly 40 px, and from g20 the woman's head overlaps the ladder and the farmer's lower body. The hook (farmer hangs hive, village laughs) reads, but the hang itself is small and slow. Fix: tighten the camera on the ladder or shift the woman right so she does not cover the ladder; show the hive hook moment (g40-48) with the hive visibly leaving his hands.
8. g66 and g123: the cuts are on a new framing each, but the shot 3 time g123-186 is a nearly static push (frame diff 3 to 5, farmer in near-identical pose from g150) for 2 s. The plan wants a sweep toward the hills. Fix: add an arm sweep to the hills at about g150-170 and a camera that follows it.
9. g123-186 (shot 3) the ladder: farmer stands in front of the ladder with his hand on it, but the ladder top is behind the roof beam and the hive hangs under the roof far from his hand; the farmer's head sits in front of the roof and fills little of the hive story. Minor. Fix: place the farmer next to the hive so one frame holds both.
10. g123-186 (shot 3) foreground sack and basket occupy the lower corners (about 25 % of height). Acceptable as framing but close to clutter; trim if issue 2 is fixed in the same way.
11. Continuity: shot 1 and 2 show the same hive-on-rack but shot 3 shows a different rack/roof angle with the hive visible at the left edge; fine. Check against s02 first frames when s02 arrives (not available).
12. QA_AUTO.md "no visible change at cuts" note should not be accepted as a PASS: the numbers above prove the cuts, so the note can be dropped from the QA.md.

## Plan coverage
Hook in 2 s: partly. A farmer on a ladder holding a hive with the village laughing is readable in shot 1 (g0-65), but the two-second read is weak because the farmer is small and shot 2 loses him. Shots 1 and 2 cover the plan beats; shot 3 lacks the sweep toward the hills.

Blocking fixes: 1, 2, 3, 4, 5. Send back to render team 1.

# QA-tech sD1 v3 (film-13 QA, team2 5ebc0b7)

**Verdict: FAIL** (1 blocking issue: the head-cut defect has moved from the right edge to the left edge)

Checked: 6 fps frames g542-642 at full size (every 5th frame, f6/), a 101-frame contact sheet, edge crops at g622/627/632, background phase-correlation for camera motion, QA.md, meta.json, cues.json, plan row D1, WORKER21 mouth rules. Colour and exposure are not judged (normalized at the conform). Not checked: the last frame of C and the first frame of D2 were not supplied, so the cut-in/out continuity is only judged from this take's own first and last frames.

## Previous FAIL (head cut by the right edge, g562-582): FIXED
Head is fully inside the frame at g562, 572 and 582 (right of centre, clear margin to the right edge). Earlier fixes still hold: the sign is readable at g542-~565 (cropped by the glide afterwards, a transition), the coins are gold, the look-up beat at g602 reads, and the laugh drawing appears at g612.

## Issues
1. **BLOCKING, g622-632 (worst g627-632): Cressingham's head is cut by the LEFT frame edge.** After the laugh push-in the camera keeps drifting right, so the head slides left. At g622 the hat and cheek touch x=0. At g627-632 the left of the hat dome and the hair are clipped and the body is cropped, with the head only partly in frame during the laugh, which is the shot's payoff. This happens before the planned whip (g637), so it is not part of the whip.
   Fix: stop the glide or ease the aim back so the head stays at least ~40 px inside the left edge from g617 to g636. The head should be centred or slightly right at the laugh, and the whip should start from that framing. Then the head slides out left only during g637-642. Re-render g612-642 only.
2. Non-blocking, g602-636, qa_jitter 7.5 px: this is not a camera shake. Phase correlation on static background (bridge, river, pole) gives a smooth drift of at most 6 px over 30 frames with no oscillation. The vertical ±20 px in the head and hat region at g613-634 is the planned laugh bounce of the card. Nothing to fix.
3. Non-blocking, g570-590: the sign is cropped by the left edge as the camera leaves it, which the brief documents. Fine as a transition. If wanted, the camera could ease out slightly later so the second line is read to the end, but no change is required.
4. Non-blocking, g577-607: the head is small and set into the upper-left third of the frame, and the table front dominates the lower half. It reads at phone size but is a framing note for QA-art, not a tech failure.

## Checklist results
- Blur/DOF: only the planned whip g637-642 is blurred (qa_auto expected). No other frame is soft.
- Heads over y 880: none. The lowest chin is about y 860 at g627, which is under the limit.
- Clipped sprites/props: head clipped at the left edge per issue 1. Nothing else is clipped. The chest and sign crop at g570-590 is intended.
- Floating feet/scale: no feet are visible. Scale is consistent, with the head growing for the laugh push-in as planned.
- Black/magenta/blank frames: none (qa_auto magenta 0.0 %). No frozen runs (the head and coins change throughout).
- Pops/jumps: none outside the cut-in at g542. The only large step is the whip at g636-637, which is planned.
- Continuity: the costume (crimson cap, gold chain), the canopy and the lantern are constant. The coin stacks stay gold, and the pinched coin and counting hand are visible g592-602. The table state is consistent.
- Eye-lines: the look-up toward the river at g602-612 is correct, and the eyes close in the laugh.
- Mouth: it is closed g542-607 (no speech in this window; Cressingham's quote starts at narration 21.29 = g642). Open-mouth laugh drawing from g612 (narration 20.29-21.29) per the plan with no lip-sync. No mouth movement outside the allowed window.
- Plan coverage (D1): money canopy and "KING'S TREASURY" chest, counting, camera arc, look-up and laugh bounce at g612, and whip right in the last 6 frames are all present. The whip direction (camera right, subject exits left, the tent and flag appear) is consistent.
- Thai text: none in the shot.

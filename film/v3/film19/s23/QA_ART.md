# QA-art, TAKE gate: s23 (shot 23, HALL hall_door EVENING) — PASS

Frames checked (take index / g): 9/1856, 25/1872, 45/1892, 55/1902, 70/1917, 85/1932, 94/1941 (full size + 360x640).
Frames: /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artend/s23_*.jpg

| Criterion | Score |
|---|---|
| Set density / ornament | 7 |
| Lighting & colour (warm practicals, depth) | 8 |
| Composition / phone legibility | 7 |
| Acting (pose reads the beat) | 7 |
| Key moment (old Harrison arrives) | 7 |
| Match to refs / client taste | 7 |
| **Overall** | **7.2** |

## What works
- The beat reads at phone size: white hair, spectacles, stoop, brown coat, slow shuffle through a lit panelled doorway. "Old man arrives" is unmistakable.
- Warm evening practicals (sconces, lit antechamber behind the door) against the deep red walls give real depth; sharp, no DOF, no text.
- Head 121-191 px, bottom 693 < 880. The door leaf crossing the frame after the snap (f 70-94) is a good foreground wipe and leads into the cut.

## Non-blocking notes (do if re-rendering anyway)
1. Watch too small: the H4 on his palm is about 25-30 px wide and reads as a white dot at 360x640. In `pose`, lift the right hand to chest height (hand y about 0.95 instead of the walk-cycle hip height) and turn the palm toward the lens, or scale the `h4_watch` prop about 1.4x. The watch is the subject of the next shot, so the viewer should see it here.
2. Bottom third is empty floor and carpet (y > 900 has no subject in every frame). Add CAM `rise_px` toward 0 (less crane-down), or tilt the look point about 0.3 D lower, so the doorway and the cornice sit higher and the floor takes about 25 % of the frame instead of about 35 %.
3. Last frames (f 85-94): the dark door slab takes the right 30 % and Harrison is small left of centre at the cut to s24. Fine for the wipe, but keep him at x 250-450 by easing `slide_px` (-135 -> about -100) so the cut to the King's wide gets a clean left-to-right eye-trace.

## Continuity
Costume matches s26 (white hair, round spectacles, brown coat and waistcoat, white stockings). Light is EVENING warm, consistent. Note: he carries the H4 in, but it is not in his hands or on the table in s26 (see s26 note).

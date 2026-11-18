# QA_TECH s10 round 2 (film 13, TAKE gate) - PASS (with non-blocking notes)

Checked: qa_auto (first_g 585, cuts 591,650,726), 6 fps sheet + cut 645-653 at 30 fps, full-size crops, joins s07 -> s10 -> s12. Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qa13s10r2/s10/ (sheet_*.jpg), /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qa13s10r2/full/. Take untouched. 147 frames read OK.

Round-1 issues:
1. Mouth open before Q1 (g612-649): FIXED. g612-649 closed-mouth laugh (squeezed eyes, tears, belly shake); mouth first opens at g650 (cut), inside Q1 window (653 -0.15 s = g648.5). Mouth varies g650-731. OK.
2. Armchair/window staging: FIXED. Red armchair, window, cup; he looks screen-left toward the window g585-605, startled g605-611, turns and laughs g612.
3. Cup continuity: FIXED. Cup + saucer in his left hand in g585-649 and g650-731 (verified g590, g665 full size).
4. Point down at Pullman: PARTLY. Right arm points sideways/slightly down toward a tiny Pullman (head ~25 px, right of the belly, g650-700); but the eyes are half-lidded and look screen-LEFT / at camera, not toward Pullman (screen-right, below). Eye-line does not hit the target. Non-blocking (Pullman is tiny); would be better with eyes/head turned to screen-right-down.
5. Chandelier / empty foreground: chandelier no longer clipped (only a small arm at right edge, g585-645). Shot 10 still has ~50% empty dark parquet below the chair (y 700-1280) and he is small (head y ~500-620); shot 11 bottom ~40% is carpet (patterned, shadow, acceptable). Non-blocking composition note.

Other checks:
- Heads: all < 880 (shot 10 head y ~500-620; shot 11 chin ~520-560 at g650-731). No crossing.
- qa_auto "suspected blur" 48 frames (g585-632): false positive. Full-res Laplacian var ~170-185 in shot 10 vs ~320 in shot 11 (smooth purple walls/floor/sky); sprite crop at full size is crisp, no DOF. Non-blocking.
- No frozen/black/magenta frames. Cut 650 is a clear cut (qa_auto 'no visible change' for 591 and 726 = joins at neighbour set-ups, by eye OK).
- Cut convention per README (cuts at round(t*30)): accepted.
- Joins: s07 end (hotel facade, Pullman hands on hips) -> s10 (suite) clean. s10 end (suite, g731) -> s12 start (facade, g720 handle) clean. Note for conform: s07 meta g1 = 594 but s10 g0 = 591 (3-frame overlap; both have handles, conform must pick one cut frame).
- Cup/props, scale, contact shadows OK. Armchair absent in shot 11 (standing at window): acceptable new set-up.

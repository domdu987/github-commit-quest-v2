# QA_TECH s24 round 2 - FAIL
Checked: qa_auto every frame, 6 fps sheets + cut frames + full-size crops, joins with neighbours (s26 older version, rough only). Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qa13b3/<take>/ and /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qa13b3/j/ . Take files untouched.
Auto: PASS (77 frames).
Round-1 issues: heads FIXED trivially (no figures at all now), box prop FIXED.
1. BLOCKING g 1537-1602 plan coverage: shot 24 is 'hotel high on its cribbing, tiny workers beneath'. Here the stair runs straight down to the ground in front of the portico, the only cue is a thin orange sliver (~15 px) under the base, no void, no cribbing, no workers (not even the cheering one); the team's own QA.md admits 'workers are not visible inside the gap'. It reads as an ordinary grounded hotel and breaks lift continuity (s23 shows a clear gap, s26 shows a large one). Fix: lower camera / lift to 0.9+ so a dark gap with lit cribbing runs the full width, detach the stair, put 4-6 tiny workers (heads y <= 840, one cheering) inside/in front of the gap.
2. g 1537-1602: stray dark blade/wedge shapes left and right of the portico awnings (x ~0-50 and ~680-720, y ~ 470) and a dark leaning box at each side of the stair top. Fix: hide.
Non-blocking: lower 35 % bare mud, plank ramp fragment bottom-left.
Joins: s23 -> s24 OK; s24 -> s25 street -> cellar hard cut OK.

# QA_TECH s14 round 2 - PASS
Checked: qa_auto every frame (planned cuts passed), own frame-diff/pop scan, 6 fps sheets + cut +-3 frames, full-size key frames, joins with neighbours. Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qa13b2/s14/ (sheet_*.jpg, full/). Take files untouched. G1 cut offset: now FIXED in all re-renders (pops/cuts sit exactly on the plan g: s17 1173/1255, s26 1743/1775/1871/1909); qa_auto's 'no change' on in/out handle boundaries is expected.
Auto: PASS (no frozen/pop/blur/magenta). Heads: worker heads at y ~ 770-830 of 1280, all < 880.
Round-1 issues: 1 FIXED (Tremont facade fills top 60 %, trench/portal at its base). 2 FIXED (9 workers in one continuous file, each with a jack on the shoulder, walking right into the tunnel mouth; constant count). 3 PARTLY (lower ~35 % is still empty mud with puddle rings, two crates and a barrel at the edges; acceptable, non-blocking). 4 FIXED (shadows attached, feet on the plank). 5 FIXED (s15 is now the cellar under this hotel).
Non-blocking notes:
1. g 906-980 lower 35 % mud: crop 10 % tighter or add a cart/plank if a re-render happens anyway.
2. Faces are all grimace/closed, no mouth flapping. No text.
Join s14 -> s15: street/portal -> cellar interior, hard cut, location logic OK.

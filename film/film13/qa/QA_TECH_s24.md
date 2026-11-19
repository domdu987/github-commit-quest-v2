# QA_TECH s24 (shot 24, aha wide: hotel high on cribbing) - FAIL (heads in caption band)
Checked: qa_auto every frame (planned cuts passed), own frame-diff/pop scan, 6 fps sheets + cut +-3 frames, full-size key frames, joins with neighbours. Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qa13b2/s24/ (sheet_*.jpg, full/). Take files untouched. G1 cut offset: now FIXED in all re-renders (pops/cuts sit exactly on the plan g: s17 1173/1255, s26 1743/1775/1871/1909); qa_auto's 'no change' on in/out handle boundaries is expected.
Auto: PASS (76 frames, no frozen/pop/blur).
Seen: wide frontal six-storey hotel, deep blue sky, 5-6 tiny workers (one cheering with raised arms) at the base, glowing cribbing/jack stacks visible at both sides of the stair, plank ramp and barrels, slow push-in. No machine in frame. 
1. HEADS: all 5-6 workers' heads span y ~ 850-925 of 1280 (head centres 870-895) from g 1537 to 1602, i.e. they cross the caption-band line y 880 (full-size frame g 1571 confirms: left red-vest man head 850-925). Client hard rule: heads fully above 880. Fix: tilt the camera down ~8 % (figures move up in frame) or move the workers up the stair so heads sit at y <= 840.
Non-blocking notes (numbering continues):
1. g 1537-1602: a blocky brown box on four thin legs (cart/stool without wheels) glides through the lower-middle foreground, g 1580-1602 it fills 30 % of the frame and looks like a stray prop. Fix: hide it or give it wheels/shadow and keep it out of frame.
2. g 1537-1602: lower 40 % flat mud; the sky has hard-edged pastel cloud slivers at the left/right edges (cut-out look). Fix: crop or soften.
3. Rise still reads mostly through the side cribbing; the stair touches the portico base, so 'high on its cribbing' is moderate at phone size. Fix: lower the camera 10 % so the void under the facade is visible.
4. Lift h 0.9 not distinguishable from s23 (0.8). Fine.
Joins: s23 -> s24 OK; s24 -> s25 (street -> pit cut-away) hard cut OK.

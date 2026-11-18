# QA_TECH s01 (film 13, TAKE gate) - FAIL

Checked: qa_auto every frame (plan cuts passed), 6 fps + every cut +-3 frames, full-size key frames, join with neighbours. Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qa13/s01/ (sheet_*.jpg, full/<g>.jpg). Take files untouched.

Global note G1 (all takes): delivered cuts sit at round(t*30) of the plan table, i.e. 3 frames (0.10 s) EARLIER than the plan's g = round((t+0.10)*30) (e.g. shot 3 at 108 vs 111, shot 11 at 650 vs 653, shot 17 at 1107 vs 1110, s26 cuts 1740/1772/1868/1906 vs 1743/1775/1871/1909). qa_auto reports every planned cut as 'no visible change' or as a pop 3 frames off for that reason. Fix: conform must cut at the plan g (handles cover it) or the take must be re-keyed +3 frames; in-shot cues (e.g. nickname jump g895, splash g1893) are not consistently offset either.

Auto: PASS (0 frozen/black/pop, magenta 0 %). Frames 0-68, shot 1 only.
1. g 0-68 (hook, key shot): the lift is not readable. Hotel base, portico and stair look sitting on the ground the whole time; no gap, exposed cribbing or jacks under the ground floor (only a small crib pier + jack at far left foreground). The motion reads as a camera crane, not a rising building. Fix: frame the base so the foundation/crib gap grows (h 0.55->0.65 = ~1.1-1.3 m: show dark gap with jacks across the full facade width, stair treads rising off the mud), add the dust trickle visibly at the base.
2. g 0-68: bottom 25-30 % of frame (y >~ 940) is a smooth brown mud plane with smeared, low-detail texture and a blurry puddle reflection; reads as soft/DOF. Fix: lower the camera pitch/crop so the foreground is plank/crib detail, or add sharp mud/puddle detail.
3. g 0-68: all four cast cards stand in a line on the stair, stiff and identical in pose for 2.3 s; only legs tiny stilts, no cast action (no workers turning jacks), so the 'workers raise the hotel' beat has no actors. Fix: put 2-3 workers on jacks at the crib pier in the foreground.
4. G1 (cut offset): out-handle g 63-68 continues hotel_front correctly, so the plan cut at g 66 is covered. No action beyond G1.
Heads: all < y 880 (Pullman head ~y 810-850 at g 65: OK). Mouths closed. No text. Join s01->s02: hard cut hotel -> suite, no continuity break.

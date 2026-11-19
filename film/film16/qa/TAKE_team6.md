# TAKE gate QA-tech, film 16, render team 6 (s19, s20, s21)
Method: all frames decoded; 6 fps (every 5th in-shot frame) + every cut +-3 frames viewed; frame-diff recomputed (90x160 grey, mean abs diff, in-shot pairs); qa_auto.py run on each take.mkv (all three: PASS, magenta 0 %, no black/frozen; its "no visible change at planned cuts" note is expected because handles are one continuous render). Neighbours s18 (render16/team5) and s22 (render16/team7) NOT present on those branches (no take), so continuity vs neighbours is judged only from the plan (s18 DUSK buggy -> s19 DAY bare poles; s21 RAIN -> s22 AFTER_RAIN bottles).
Numbers: s19 in-shot median 5.64 / p90 15.24 (min 3.77); s20 median 9.49 / p90 12.07 (min 6.96, p90 only just over 12); s21 median 9.28 / p90 14.12 (min 4.13). No parked camera (no pair < 3.7). No text, no DOF, no black/magenta in any take.

## s19 (shot 19, g 1226-1267): FAIL
1. g 1256->1257: hard pop. The hand-held poles (Morse's and worker's) vanish and the set pole 3 appears standing in one frame, mid-snap; no rising motion. Meta/cues say pole_up 1259, the pop actually lands at 1257 (cue and frame disagree by 2). Fix: animate the pole tilting upright into the hole over ~8 frames, or hide the swap behind a foreground element; correct meta/cue frame.
2. g 1257-1267: Morse's and the worker's raised arms hold nothing (empty hands up) after the swap; pole is behind Morse with its base hidden. Fix: keep the hand props until the pole is planted, or lower the arms / pose "hands on pole" on the standing pole.
3. whole shot: plan beat "hang the wire straight on the wood" is not visible. No wire anywhere in the shot, including the standing pole top (the pole top is out of frame after the snap). Fix: show a wire spanning from pole 3 to the next pole (wide frames) and keep the pole top in frame at the end.
4. g 1226-1250: worker_b (red shirt, third man) is walked/pushed out of frame by the snap (gone by ~1251), so the "workers" raise reads as 2 people; only one person remains besides Morse. Fix: re-stage the camera so at least two workers + Morse stay in frame, or re-pan.
5. g 1226-1267: eye-lines: Morse and worker look at the camera (frown, straight ahead), not at the pole top. Fix: turn the heads up toward the pole.
6. g 1250-1267: ground artefacts in the foreground (clipped grey/green slabs with hard dark edges, dark hole squares) show at the bottom; reads as broken geometry at phone size. Fix: cover with grass FG prop or reposition the camera.
Passes: heads < 880 (head bottoms ~740), feet on ground with shadows, mouths still, no DOF/text, sun shadows consistent. Note: light is plain DAY (plan said overcast warm; accepted by the worker).

## s20 (shot 20, g 1268-1345): PASS (with notes)
Rain falls down (slight lean, consistent through the take), pole bare (no bottles), wire at top, blue sparks crawl DOWN the pole into the base glow, tilt follows them, snap at 1316-1331 present, camera moving every frame, no characters (no heads/mouths). Dissolve-in from s19 handled by hard cut: s19 end is warm DAY, s20 start is blue RAIN, acceptable as a plan CUT.
Non-blocking notes: (a) p90 12.07 is right at the threshold; (b) the wire leaves the frame after ~g 1320 so the "wet pole darkens / wire present" read weakens; (c) puddle (dark blue ellipse) sits left of the pole, sparks end in a glow at the pole foot rather than in the puddle (plan says into the puddles at the base); (d) pole top/bottom bright foot sparks sit near the caption band at g 1340+ (no head involved).

## s21 (shot 21, g 1346-1380): FAIL
1. g 1352-1358 and 1367-1373 (press1/press2): the key press is not visible. Morse stands behind a wall/crate, the key and his hand are hidden, only a small body lean; "presses: nothing" cannot be read. Fix: lower/shift the camera or move the crate so the key and the pressing hand are in frame, or add a visible lever dip.
2. g 1351-1380: the hat is held by Cornell over Cornell's own head/beside it, not over Morse; Morse's head is in the open rain (drops across his face). Plan: "a worker holds a hat over him". Fix: move Cornell next to Morse with the hat above Morse's head, or shift Morse under it.
3. g 1356-1380: Cornell is cropped by the left frame edge (half face by 1366, eye-line unreadable); the push + slide drags him out. Fix: slide the other way or re-stage Cornell nearer the centre; worker_a (red) also exits by 1356, so the "workers waiting" is lost.
4. g 1346-1380: eye-lines: Morse looks at the camera with a sad frown rather than at the key/register; Cornell looks at the camera. Fix: turn Morse's head to the key then slowly to the sky/camera.
5. g 1346-1349: foreground grass blades in the lens cover the lower third; they are dark and read as streaks. Minor (non-blocking).
Passes: heads < 880 (Morse head bottom ~ y 650 in frame at 1376), feet/contact shadows present, mouths still, rain vertical and consistent, no pop, no DOF/text, p90 passes.

Continuity: s20 bare pole in rain -> s21 trench end in rain OK; s21 -> s22 (AFTER_RAIN, bottles on a crate) cannot be checked, s22 not on render16/team7.

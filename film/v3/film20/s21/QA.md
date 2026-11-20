# QA s21 (shot 21, g1431..1559, handles 1427-1430 / 1560-1563) -- take-gate fix round 1
- qa_auto: no FAIL. Notes: soft frames g1427-1430 are the out-of-shot handle (3 on screen max), 'cuts with no visible change' = handles are 3-D continuations.
- qa_stats: `take.mkv: 4.6s ... saturation 0.748, brightness 69.9, in-shot motion median 7.18 p90 11.70`
- s/frame 7.52 wall / 14.32 cpu (2 procs x 2 threads, 720x1280, 8 spp). Frame-diff (90x160 grey, in shot): median 6.27 PASS, p90 9.16 (target 12: MISS; the previous version had 12.3 but with the camera sliding past the wire anchor, which sent the wire across the sky).
## Take-gate fixes (QA-art F1-F4, QA-tech 1-5, QA-stats)
- F1 rings: own thick glowing tori (shot.build_fx), a ring born every 18 f at the summit lamp (r 6 m, bright flash sphere), growing to 500 m (age^0.7) while fading, 3 alive, so they visibly EXPAND over Paris; the set's thin rings are hidden every frame.
- F2 glow g1530+: iron stays red-orange; the glow is an ADDED blue-white emission (0.03) on the lattice + the single wire ramps 2 -> 7 + ring flash. No tint toward pale pink.
- F3/QA-tech 4 wire: set's 4 fat wires hidden; ONE thin pale wire (r 0.22 m) from the summit to the post (same tower20.wire_path) for the whole shot; the slide is -14 px/s so the wire never swings over to the left.
- F4/QA-tech 5 trees: wide camera raised 5 -> 30 m, aim 4 deg down: lit roofs of Paris under the rings, trees small, tower base visible.
- QA-tech 1: start framing 40 m from the summit lamp with a warm summit point light and exposure +0.95 (scene view_settings): lit summit with lamp dots; 9-frame whip (g1427-1436) already running at the cut; soft frames only in the handle.
- QA-stats: exposure +0.95 lifted brightness 54 -> 69.9 (night floor 70), saturation 0.75.
## Rules
Heads: none (no cast). Tower reads as the Eiffel Tower on every frame. No DOF, no text, nothing floating. Ground (avenue lawn) <= 25 % at the wide.
## Deviations
- Wire is a runtime single wire (set object antenna_wirep hidden), the set module untouched. The wire exits the frame at the right edge during the snap-in (it runs on to the post).
- Pull 6 %/s along the ground + snap push x1.28 on the word (plan: drift 6 %).

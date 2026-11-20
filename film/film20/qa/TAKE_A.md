# TAKE gate A, QA-tech, film 20: s01 s03 s04 s05 s06 s11
Method: ffmpeg frames (g = first_g + index); qa_auto.py re-run on each take (all PASS: no black/blank/magenta/frozen/pops);
viewed every 5th frame (6 fps) plus handles, g0+-3, g1+-3 and the beat frames; frame-diff measured myself (90x160 grey, consecutive, in-shot g0<g<g1).

| take | median | p90 | verdict |
|---|---|---|---|
| s01 | 5.60 | 14.76 | PASS |
| s03 | 4.01 | 9.97 | FAIL |
| s04 | 4.55 | 5.52 | FAIL |
| s05 | 6.25 | 13.08 | FAIL |
| s06 | 5.58 | 16.99 | FAIL |
| s11 | 6.96 | 13.04 | FAIL |

## s01 PASS
Tower reads as the Eiffel Tower in every frame; heads < 880 (chin max ~830); contact shadow under both shoes g0-30; no blur/DOF; no text; swap on the closed blink g27 clean; cut +-3 (g77-83) clean; handles present (0 in, 4 out).
Notes (non-blocking): 1. g60-66 the moustache/mouth shape deforms with the hmph (reads as a mouth move outside the quote windows; mostly head roll). 2. From g55 the right tower leg is cropped by the frame edge (spire still in frame). 3. g35-83 legs/feet are out of frame, so no contact visible (acceptable, close framing). 4. Next take s02 not available, so continuity with RESTO not checked.

## s03 FAIL
1. g178-268 whole shot: the lower ~38% of the frame (y > ~790) is a flat dark-blue slab with only a sun wedge; no props or feet in the caption zone. Fix: tilt up 4-6 deg or move the camera so ground <= 25%.
2. g229-268: the high crane-down never reaches the plan's "high crane down 3.8 D -> 2.5 D" read: the four legs are cropped off at the top from g224 (only two leg stubs at the top edge), so the tower does not read as Eiffel; the building site reads as a barrel yard. Fix: keep the whole of at least 2-3 legs in frame at the end pose.
3. g178-268: the riveters are 22-30 px heads and only 2-3 are visible (six planned); the one close worker (g224-268) stands behind barrels, head ~y 800-870 touching the band at g266-268. Fix: bring workers into the mid ground, keep heads < 860.
4. In-shot frame-diff p90 9.97 < 12 (median 4.01, min 2.99). The 'ปี 1887' snap (g213-228) is too soft. Fix: stronger snap (x1.6 plus orbit) and/or slide 60 px/s.
5. g213-228 the snap does not read: no visible speed-up in the first frames of the snap (diff stays < 6). Fix as 4.
6. Handles present (9 in = 13/2+2 ok, 4 out). Dissolve side start g169 is a near-copy of g178 (ok).

## s04 FAIL
1. g261-321: NO tower or leg is visible behind Eiffel; the background is a blank beige wall (about 45% of the frame) with one orange corner at the top-left (g261-285). Director note "lower the camera, tilt up ~8 deg so leg + scaffold fill the background" is not met. The tower does not read as Eiffel. Fix: tilt up and aim at a leg/scaffold, crop the wall.
2. g261-285: huge saturated pure-blue blocks + black plank slats fill the bottom 30% (the plan table?). They read as an unlit blue box with no texture or blueprint; no rolled blueprint is visible. Fix: texture/shade the table, show the blueprint, or crop.
3. g281-286: a new blue bucket enters from the left and a crate FG pops in (g283-291) while the table FG slides out: reads as a pop-in; fix by staging the FG pieces before g261.
4. g266-321: Eiffel's arm is raised the whole shot (plan: up on 'วิศวกรไอเฟล' g266-274 only); he holds the pose to g321 with only a squash; he is small (head 112-144 px but y 720-747, figure is a stick on the wall). Fix: arm down/up cycle, push in on him.
5. Frame-diff p90 5.52 < 12 (median 4.55): no snap move is in this shot at all (plan had push + slide + arc + tilt; the snap is missing). Fix: add a snap on the strongest word.
6. g300-321 feet: contact shadow present (ok); wide gap of empty ground at bottom.

## s05 FAIL
1. g314-407: a flat grey-beige wall fills the middle 35-45% of the frame (y 330-800) for the whole shot. Fix: aim the tilt at the leg, drop the wall via a higher camera/narrower FOV start.
2. g314-340: Eiffel (the only character, head ~16 px at g314-324) is tiny at the far left behind a giant sack and leaves frame left by g335; the plan's "Eiffel small at the foot, arm raised" is gone after g335. Fix: keep him in frame or cut the sack.
3. g314-407: no riveters on the platforms are visible at all (plan: "riveters on the scaffold"). The scaffolded leg shows only timber struts. Fix: add worker cards on the platforms.
4. g314-407: the tower does not read as the Eiffel Tower (one iron section + a platform, no leg arc or lattice in context). At g404-407 sky is ~22% (plan: tilt-up must end at >= 35% sky). Fix: end the tilt higher, show the leg tapering into sky.
5. g314-345: FG sack (g314-335) and bucket (g314-340) cover 30% of the frame width; coarse, outlined 'gourd' sacks look like jars. Fix: smaller props at 1-2 D.
6. Bottom 20% shows only sacks/barrels at g364-407 (no feet, no shadows) while the diff is carried by the camera alone.
7. Frame-diff median 6.25 / p90 13.08: pass. Handles 4 in / 4 out present. Snap g344-359 present.

## s06 FAIL
1. g395-440: ceiling is ~40% and the checker floor ~35% of the frame (rule: checker <= 25%); the artists are small at the horizon (heads 60-90 px, 12-20% of height). Fix: raise the framing, crop the ceiling, lower pitch so the group sits at y 550-800.
2. g410-447: the near chair back/rail and the table column cross the artists' faces (g420-445 the chair back covers the red-beret artist and the hat of the gentleman; g445 the arched chair back covers two faces). Fix: move the FG chair out of the line of the group (1-2 D to the side).
3. g395-466: the tower stub is not readable in the window (only a few lattice pixels behind the beret at g395-415, hidden after); plan: "tall window with the tower stub on the skyline". Fix: frame the window with the stub visible.
4. g450-469: the artist at the left is cropped by the frame edge (g465-469 gentleman's head cut), only 3 of 5 cast in frame after the snap. Fix: finish the move with the whole group in frame (4 artists + waiter).
5. g395-466: feet/contact of the artists hidden by the tables; the waiter is not visible at any frame.
6. Frame-diff median 5.58 / p90 16.99: pass. Handles 9 in (13/2+2 ok) and 4 out present. Mouths held open (as stated in meta); no readable text (newspapers greeked scribble with a dot photo, acceptable).

## s11 FAIL
1. g745-801: the Parisians' heads are 37-55 px (plan/QA-art: >= 40 px) and sit as a small row at y 480-640; the lower 40% (y > 780) is empty ground for g745-780 (ground <= 25% required). Fix: lower and push in on the Parisians.
2. g776-801: barrels move into the foreground and hide the lady (gone from frame by g785) and half the child and gent; at g785-801 only 2 of the 3 Parisians are legible. Fix: keep the FG barrels left/right of the group.
3. g745-801: no clear laughing bounce (3 Hz squash) visible at 6 fps on the lady and child (g745-775 they are near static); eye-lines are to camera rather than to Eiffel (he is not in frame in framing A, so the 'point at Eiffel' beat is lost). Fix: put Eiffel (small) in frame A.
4. g802-825: the rivet in Eiffel's raised hand reads as a red mallet/wrench head, not a giant rivet. Fix: bigger rivet silhouette (round head + shank), glow.
5. g802-807: speed lines (6 frames) and 2-frame shake present; the lines are fat white and dark polygons, cut the face at g802-803 and fill 30% of the frame. Acceptable but heavy: reduce width. After g808 the pose is nearly frozen (arm bounce small); plan says push 12 %/s + slide: view g808-825 as near-static (frame-diff low).
6. g802: punch-in cut is clean (spike 36 at g802, planned). Handles 8 in (11/2+2 ok) and 4 out present. Frame-diff median 6.96 / p90 13.04: pass. Tower (leg stub) reads in framing A.

# s25b QA (render team 6): shot 25 "the herd turns and runs off", g1672-1770, 99 frames
- qa_auto: see QA_AUTO.md / phone_sheet.jpg. 16 samples, ~35 s/frame, 2 procs x 2 threads, detached resumable loop (run_s25b.sh).
- 1. Night elephants: sprite pixels graded x0.52 and tinted (0.78,0.82,1.0) (team 3's method; team 5's shader multiply never took effect). Measured mean luma of the elephant region 54 vs lit soil ~67 (g1680), i.e. not brighter than the soil. Dark contact ellipse under every elephant (team 3 sizes, offset along the moon-shadow direction, strength 0.8).
- 2. Turn: NO cross-fade. The frontal ears-flared card is shown at full opacity and swapped for the running profile card on ONE frame per elephant (g1684-1692) behind a dust crown (frame-diff spike 8.3 at g1683 is that swap + crown; no ghost frames, no double heads).
- 3. Herd leaves: the camera sits oblique to the fence (9.8,-6.8,1.7 pulling to 9.2,-6.6) looking at the yard; the herd runs 2.8x the original stride distance, crosses the frame and is out of the left edge by about g1715; g1715-1770 is an emptying field with settling dust and the hive row/mountain.
- 4. Dust: darker warm-grey streaks (teardrop droplets with long thin tails) and soft low-opacity wisps; no bright round balls piled at the feet; extra slow wisps at gs+6/14/24 so dust settles through the last 55 frames.
- 5. Sky about 30 % (look target lowered).
- Weak: the herd is on screen only for the first ~40 frames; contact ellipses near the camera in g1672-1690 are big dark blotches on the soil; the leftover dust in the last frames is faint.

## v2 (director recheck: turn pop, dead air, shadows)
- 1. Turn: dropped. The herd is already turned and running at g1672 (shot 24 ends on the trumpet): no on-screen swap, no pop (max frame diff 5.4, median 3.0).
- 2. Dead air / direction: the camera now stands INSIDE the fence (field side, in the gap between units 3 and 4, nearest hives/posts/roofs and the maize near it hidden) looking out over the yard; the herd runs away from the fence and the camera into depth (direction (-0.78,-0.62)) and keeps receding in frame (size about 1.0 -> 0.15) through g1770; dust streaks/wisps settle behind it. The herd does not leave the frame but is tiny by the end.
- 3. Shadows: the large loose dark blotches were the cards' own cast shadows: cards no longer cast (visible_shadow False); the contact ellipse is placed at each card's foot and moves with it (at 720 px it is mostly hidden by the foreground grass); the hard yellow patch of v1 is gone with the new camera.
- Also: the thick set wire passed 1 m from the lens and crossed the herd's faces, so the wire is hidden in this shot; bees reduced (0.22 burst).
- Weak: sky is about 38 % (horizon at ~38-40 % of the frame), not the 30 % asked; ground in the lower half is plain soil with footprints and grass; the herd is a tight overlapping clump of dark cards; the contact ellipses are hard to see under the grass. I could not verify luma at the final frames beyond the v1 figure (elephants 54 vs soil ~67).

## v3 (director recheck: moonwalk, patches)
- Moonwalk: the running cards are no longer mirrored (MIRROR25 = False), so the elephants face the direction the clump travels on screen (right and into depth), matching shot 24's right-facing matriarch; tails/rumps lead on the left. Max frame diff 4.3, median 2.9.
- Patches: the hard-edged flat rectangles were the edges of the dust strip cards (paint window clipped at +-7.5 m round the lead elephant, with the spray thrown AHEAD of the herd). Strips are now +-14 m wide, the spray drifts BEHIND the runners (dirx +1), both dust cards sit behind their elephant, and streak/wisp alpha is lower (95/85): no card edge in the picture and the rear elephants are no longer drawn through. A few faint streaks still cross the rear elephants' bodies (they read as dust, not as see-through).
- Drafts of g1690, 1720, 1750 checked before the final render (by me, at 540x370 crops).
- Everything else as v2 (herd already running at g1672, runs into depth, thick wire hidden, card shadows off).

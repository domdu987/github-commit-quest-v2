# s25b QA (render team 6): shot 25 "the herd turns and runs off", g1672-1770, 99 frames
- qa_auto: see QA_AUTO.md / phone_sheet.jpg. 16 samples, ~35 s/frame, 2 procs x 2 threads, detached resumable loop (run_s25b.sh).
- 1. Night elephants: sprite pixels graded x0.52 and tinted (0.78,0.82,1.0) (team 3's method; team 5's shader multiply never took effect). Measured mean luma of the elephant region 54 vs lit soil ~67 (g1680), i.e. not brighter than the soil. Dark contact ellipse under every elephant (team 3 sizes, offset along the moon-shadow direction, strength 0.8).
- 2. Turn: NO cross-fade. The frontal ears-flared card is shown at full opacity and swapped for the running profile card on ONE frame per elephant (g1684-1692) behind a dust crown (frame-diff spike 8.3 at g1683 is that swap + crown; no ghost frames, no double heads).
- 3. Herd leaves: the camera sits oblique to the fence (9.8,-6.8,1.7 pulling to 9.2,-6.6) looking at the yard; the herd runs 2.8x the original stride distance, crosses the frame and is out of the left edge by about g1715; g1715-1770 is an emptying field with settling dust and the hive row/mountain.
- 4. Dust: darker warm-grey streaks (teardrop droplets with long thin tails) and soft low-opacity wisps; no bright round balls piled at the feet; extra slow wisps at gs+6/14/24 so dust settles through the last 55 frames.
- 5. Sky about 30 % (look target lowered).
- Weak: the herd is on screen only for the first ~40 frames; contact ellipses near the camera in g1672-1690 are big dark blotches on the soil; the leftover dust in the last frames is faint.

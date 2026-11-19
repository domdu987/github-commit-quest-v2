# QA s19 (render team 5, film 18) — frames g1427-1514 (+6 handles each side: take.mkv g1421-1520, 100 frames), jimo_out NIGHT
Render: Cycles 12 samples 720x1280, 2 threads, ~25-35 s/frame with four renders sharing the 4 cores (about 11-16 s alone). Per-frame cards (c18.py). First version of this take was re-rendered (camera too far: the oxen were 60 px tall; replaced by a closer camera) and the whip landing frames re-rendered once more with a tilt-down.

## Frame-diff (90x160 grey, in-shot g1427-1514, n=87)
median **15.83**, p90 **28.27** (min 0.30, max 38.36): large charging oxen pass the lens.

## qa_auto
FAIL on one item only: "suspected blur" g1510-1520 (11 frames, 11 %). Those are the whip landing frames: after the pan the lens looks along the field at a sky + sand + distant herd, which has far less edge detail than the wall-and-oxen frames before it, so the Laplacian-variance test drops under 60 % of the median. They are not blurred: no motion blur is rendered, the herd and tail flames are sharp (see contact2.jpg). Frames g1515-1520 are handle frames after the cut. Judge by eye.

## Brief items (QA_ART_SET_R2 instructions 2 and 4)
- Tail flames: every lit ox has the cast reed-tail flame (variants 0/1/2 cycled every 2-3 frames) plus an added painted tail flame card; >= 1 flame visible in every frame from g1437 on (the first oxen leave the holes at g1430), 3-8 in the second half. Before that only the dark breaches and the wall are on screen (the oxen still inside the tunnels).
- No dark-square puffs: the set's additive `dust` flats, `mist` halo quads and the `hglow` squares were removed/hidden at runtime (they were the dark translucent squares at the breaches); replaced by light-brown puff cards (3 per hole, grow and fade over 40 frames) at the hole mouths.
- Qi silhouettes: 6 `qi_run` dark runners (cast18.qi_pose, 8-phase run cycle) pour out of the holes behind the last oxen, outside the wall (from g1449).
- Flat ground: tilted the view up (look z 9) so the moat/sand is about 25 % of the frame at the start and the herd and wall fill the rest; the camera starts closer (11, -22, 1.4).
- Oxen burst out of the holes in waves (22 oxen, 4 waves, 15 D/s), gallop at ~12 fps, front-3/4 cards for the near ones, scale varied; holes all open (12).
- Comic / bloodless: nobody near a blade; Qi soldiers only follow.
- Whip pan at the end as planned (-85 deg over 6 frames from t 0.9), now with a tilt-down so it lands on the herd.

## Deviations
- Camera position changed from the plan's (6,-32,1.5) to (11,-22,1.4) look (30,-5,9) so the oxen read at the holes.
- The blur flag above.

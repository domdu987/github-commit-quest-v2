# QA, film 9 take s15 (shots 15 + 16, the reveal), worker 4, round 2 (QA-tech round 1 fixes)
Frames g 1147..1418 (272 = 6 in-handle + shot 15 g 1153..1283 + shot 16 g 1284..1412 + 6 out-handle), 720x1280, 12 samples, 30 fps.
`take.mkv` 93.5 MB, delivered as `take.mkv.partaa` + `.partab` + `.partac` (`cat take.mkv.part* > take.mkv`). first_g 1147, n_frames 272.

## QA-tech round 1 -> fixes
1. Ring: the set's thin pulse ring (expanding to the frame edge, turning olive) is hidden every frame.  New: a thick soft-glow emissive
   gold ring hugging the ball (radial profile 1.3..2.5 x the ball radius, scale 0.82 -> 1.1) that fades to transparent with no colour
   change (g 1380..1406); a gold glow burst along the web on impact (web strengths x ~2.9 at the hit, Gaussian 6 frames).
2. Web flex: a 'bulge' shape key on the web (strands round the ball pushed outward ~0.42 D and into the joint) driven as a damped
   spring from the hit, settling at a small held stretch; the ball stays held and visible in its glowing dent to the end.
3. The calm part (g 1284..1351): longer camera push (10 -> 6.9 D) with a small orbit and a gentle gold glow pulse of the web
   (+-24 %, 46-frame period).  Near-still transitions: 0.
4. Recommended tilt: both halves now use an oblique orbit camera (24 -> 19 deg / 17 -> 23 deg yaw from the front-left, 6.5-11 deg
   down, 24 mm): the warm fire key rakes across the bricks, crystals and web; same tilt family in both halves.
Plain half: unchanged in content (star-burst flash at the hit g 1207, black cracks with orange fronts race through the joint).

## Checks (deliver.py -> work/qa.txt)
- Pops: only g 1283 -> 1284 = the planned cut (37.3). Near-still transitions: 0 (median frame change 2.15).
- No heads / mouths / text; no DOF; no black or magenta frames. Smoke billows: none in front of the impact (bf() phase offset kept).
- Hue: red 76.8 / orange 10.3 / yellow 4.7 / blue 4.5 / cyan 3.1, sat 0.42: warm fired-clay macro by the set's design, gold + cyan accents.
- s/frame: 12.6 s wall / 22.8 s CPU (two processes, 2 threads): plain 12.4 / 22.5, rice 12.7 / 23.1.

## Differences from the plan
- Rice: the ball is held in its dent (round-3 set + director), not bouncing off.
- The dark navy area at the lower left of some frames is the cool-shaded joint below the lower brick course (set geometry).

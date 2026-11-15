# QA, film 9 take s15 (shots 15 + 16, the reveal), worker 4
Frames g 1147..1418 (272 = 6 in-handle + shot 15 g 1153..1283 + shot 16 g 1284..1412 + 6 out-handle), 720x1280, 12 samples, 30 fps.
`take.mkv` is 90 MB: delivered as `take.mkv.partaa` + `take.mkv.partab` (`cat take.mkv.part* > take.mkv`). first_g 1147, n_frames 272.

## What is on screen
- Shot 15 (mortar_macro, plain, BATTLE, macro_front, slow push 2 D): calm grey joint with cyan lime crystals on
  "ปูนธรรมดา แข็งก็จริง แต่เปราะ"; the ball enters at g ~1195 and hits on "โดนกระแทก" (g 1207): star-burst flash, small camera jolt,
  black jagged cracks with orange running fronts race along the joint and into the bricks on "ทีเดียวก็ร้าวทั้งแผ่น" (g 1207..1262),
  red / grey grit spalls, the ball drops away.
- Shot 16 (mortar_macro_rice, same camera family, push from the other side): the gold starch net around the crystals on
  "ส่วนแป้งข้าวเหนียว ไปพันกับผลึกปูนเป็นตาข่ายเหนียวหนึบ"; the ball flies in and hits at g 1380 ("ลูกปืนกระแทก"): gold ring pulse,
  web flexes and holds; the ball springs back slightly and stays HELD in its glowing dent ring to the end ("แค่ไหนก็แค่บุบ"), visible (round-3 set note).

## Checks (deliver.py -> work/qa.txt)
- Pops: g 1283 -> 1284 = the planned cut (31.7); g 1182 -> 1183 (2.0) = the ball entering frame. No other pops.
- Near-still transitions (< 0.35 levels): 0 (median frame change 1.57).
- Black / magenta / blank frames: none. No DOF. No people (no heads, no mouths). No text.
- Hue: red 83.6 / orange 7.0 / yellow 4.3 / cyan 3.0, sat 0.43, val 0.59: red-heavy by the set's macro design (warm-lit fired clay;
  the set API reports macro plain ~75 % red); gold + cyan accents on the subject. No magenta (0.2).
- s/frame: 12.0 s wall / 23.5 s CPU (2 threads, two processes): plain 11.9 / 23.4, rice 12.1 / 23.7.

## Differences from the plan / notes
- Plan: rice "the ball only dents and bounces off". Round-3 set + director: the ball is held in the dent (stays visible); followed the set.
- The set's macro smoke billows take their phase from the Blender frame; shot 15's Blender frames are offset by one smoke cycle
  (bf() in shot.py) so no billow drifts across the lens (at the first offset big billows covered the impact).
- Shot 15 -> 16 is a hard cut inside the take (both macro_front, mirrored push directions).

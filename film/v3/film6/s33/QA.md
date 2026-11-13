# s33 QA: film 6, shot 33 ("aha": they never cheated), market AFTERNOON — render team 7

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps), first_g 2830, 141 frames g 2830..2970.
- g 2830..2835: 6-frame in-handle for the dissolve from shot 32.
- g 2836..2964: shot 33 (plan 94.54-98.83 s).
- g 2965..2970: 6-frame out-handle for the dissolve to shot 34.

All frames, handles included, were rendered in 3D. Also included: `meta.json` (transition_in "dissolve"), `cues.json`, `contact.jpg`
(red line = y 880), `compare.jpg`, `shot.py`, `deliver.py`, and `work/qa.txt`.

## What is on screen
Three earlier bakers are locked in a row in the pillory on the platform, sad and drooping, with slow "no" head shakes and sighs. In front
of each, on the platform boards, stands a basket of his own bread with white steam drifting off it into the afternoon sun.
- **A** g 2830..2878 (1.63 s): low and frontal; the three heads in a row behind the steaming baskets; slow push. Captions:
  "ร้านพวกนั้น ไม่ได้โกงเลย".
- **B** g 2879..2922 (1.47 s), hard framing cut: punch-in on the middle baker (baker2, with tears) as the steam rises across him; slow
  tilt up. Caption: "ขนมปังของพวกเขา".
- **C** g 2923..2970 (1.60 s), framing cut: low from the right. Steam rises past the bakers, who lift their eyes after it; the camera
  tilts up toward the sky. Captions: "แค่ลอยหายไปในอากาศ ทีละนิด".

## How
- The set pillory has one neck hole and one 3D board. Its board, post, hole rims, padlock and sign are deleted from the `pillory` mesh at
  runtime (151 verts, by bmesh in shot.py). The platform, rails, lanterns and veg splats stay.
- Each baker is a cast6 `pillory=True` pose card with his own drawn board and post.
- `baker3` (brown cap, ginger hair, blue tunic, bushy moustache) and `baker4` (bald / grey, brown tunic, stouter) are deep-copied recolours
  of cast6 `baker2`. They are registered into `puppet.CAST` / `CANVAS` at runtime; cast6 itself is not edited.
- Baskets: `cast6.basket_svg` (10 / 12 / 11 loaves) on PropCards, x1.25.
- Steam: three local camera-only cards per basket, using the set's own steam material, keyed by `B.set_steam(1.5)` every frame.
  The set's steam sources exist only in the bakery interior.

## Client rules
- **No DOF / sharp**: DOF is off at build and before every render. There is no motion blur, and the cuts are framing switches.
- **Heads above the caption band**: no head bottom below y 880 on any frame (`work/qa.txt`).
  - Main head per framing: A bk_m 0.38..0.41 H; B bk_m 0.38..0.47 H; C bk_r 0.39..0.42 H.
  - Secondary heads: bk_l reaches 0.61 H at the end of C (bottom 860 px).
- **Mouths**: no quoted line; the bakers keep static sad / worried mouths.
- **Comic, not cruel**: no injury; the platform keeps the set's cartoon veg splats.

## Numbers
- Heads: bk_l 139..305 px, bk_m 158..293 px, bk_r 164..322 px (the larger sizes are in B and C).
- Popcheck: the only jumps are the two planned framing cuts (2878->2879, 2922->2923); no near-still frame pairs.
- No black or magenta frames; no retried frames.

Hue (shot frames):
- s33: red 8.9, orange 28.9, blue 53.8, violet 3.9, magenta 3.8, sat 0.42, val 0.72, dark 0.03.
- The sky fills much of the low framings, hence the blue. The shade is blue-violet, never magenta.
- Like every market shot, it is brighter and flatter than the refs (bakery_API 7).

## Seconds per frame
18.9 s wall / 36.7 s CPU mean, with 12 samples, 720x1280, 2 threads and two render processes on 4 cores.

## Differences from the plan / known issues
- The plan says "the earlier bakers". Shots 13-15 showed 1 / 2 / 4 heads; this take shows three in a row, because the platform fits three
  boards. The extra bakers are recolours, so they may not match whatever shot 15's worker used. Check continuity in the conform.
- The steam is deliberately strong (level 1.5), the visual motif of the shot. In A and B it veils the bakers' aprons; faces stay readable.
- In B the left and right bakers are cut by the frame edges (punch-in).

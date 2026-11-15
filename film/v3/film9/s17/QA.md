# s17 QA: film 9, shot 17 (dawn after the battle): wall_site aftermath_dawn, DAWN

Delivered: `frames/g_1407.png .. g_1559.png` (153 frames, 720x1280, 12 samples, 2 threads, denoise FAST; not in git) and `take.mkv`
(libx264rgb crf 6, 30 fps, first_g 1407, 153 frames; 43.9 MB, not split). g 1407..1412 = in-handle (for the 8-frame dissolve in from shot 16), g 1413..1553 = shot 17
(plan 47.11-51.79 s), g 1554..1559 = out-handle (shot 18 cuts in at g 1554). Rendered on the client-approved set (commit 5d511aa).
Also `meta.json`, `cues.json` (5 cues), `contact.jpg` (16 frames, cyan line = y 880), `qa.txt`. Scripts: `shot.py` (stills / final),
`deliver.py` (frames, meta, cues, contact, mkv, QA numbers from `take.json`), helper `c9.py` (film8/common.py switched to cast9 + wall.py).

## Content (re-rendered after QA-tech round 1)
- **Framing:** wide view from the field, a little above eye level (16 mm). It shows the whole rice section with its crenellated top and
  blue banners, the dawn sky with clouds, the field, and the lit rubble foreground (the spent ball and a snapped stake). Lin is small
  but readable at the wall foot (head 52-59 px). Camera: slow push and drift (-8.8,-14.8,3.0) -> (-10.6,-14.0,3.2), eased 0.35 sine +
  0.65 linear. No DOF.
- **Dents:** set_impact lin 0..2 at t 1. At runtime each dent is 1.35x bigger, has a painted soot scorch, and has 9-12 jagged hairline
  cracks (up to 2.9 D long) radiating from its rim; they read at phone size. The set's crack overlay is made fully opaque (alpha x4).
  The embedded balls are subdivided.
- **Foreground ball:** smooth (a 64x32 sphere over the set's 28x16 one).
- **Lin's shadow:** no proxy shadow (the low sun threw it on the wall, detached from him); a dark contact decal sits under his feet.
- **Acting:** Lin looks up at his wall in quiet wonder (stunned eyes, dash mouth, head and gaze up). Behind the blink (closed frame
  g 1502, on "ยังตั้งอยู่") he switches to a happy smile, arms folded, turning to the lens over g 1502-1512.
- Nobody speaks, so mouths are static.

## Numbers (qa.txt)
- Lin's head: 52-59 px, centre y 751-768 (0.59-0.60 H; this is a wide), bottom <= 798 (all above 880). No clipped sprites.
- Popcheck: no pops; no near-still frames (median change 0.91 levels); no black or magenta frames.
- Render: 13.4 s wall / 25.3 s CPU per frame (two processes at once, 2 threads each).
- Hue: red 31.4 / orange 34.5 / yellow 9.3 / blue 20.9 / violet 1.8 / magenta 2.2; saturation 0.34, value 0.60, dark 0.02.
  The report flags saturation and dark fraction: this is the warm dawn look of the approved preset (not re-graded).

## Differences from the plan
- No dissolve to a weathered "today" wall: per the director's assignment, shot 17 is dawn after the battle only.
- Lin is not in the plan row; I added him for a calm payoff.

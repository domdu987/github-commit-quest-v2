# s17 QA: film 9, shot 17 (dawn after the battle): wall_site aftermath_dawn, DAWN

Delivered: `frames/g_1407.png .. g_1559.png` (153 frames, 720x1280, 12 samples, 2 threads, denoise FAST; not in git) and `take.mkv`
(libx264rgb crf 6, 30 fps, first_g 1407, 153 frames; 47.9 MB, so it is split in git as `take.mkv.partaa` + `take.mkv.partab`:
`cat take.mkv.part* > take.mkv`). g 1407..1412 = in-handle (for the 8-frame dissolve in from shot 16), g 1413..1553 = shot 17
(plan 47.11-51.79 s), g 1554..1559 = out-handle (shot 18 cuts in at g 1554). Rendered on the client-approved set (commit 5d511aa).
Also `meta.json`, `cues.json` (5 cues), `contact.jpg` (16 frames, cyan line = y 880), `qa.txt`. Scripts: `shot.py` (stills / final),
`deliver.py` (frames, meta, cues, contact, mkv, QA numbers from `take.json`), helper `c9.py` (film8/common.py switched to cast9 + wall.py).

## Content
From the field in front of Lin's rice-mortar section at dawn (preset `aftermath_dawn`: warm low sun raking the outer face, cartoon
clouds, rubble of the general's section, a spent ball in a scorched furrow and a snapped stake in the foreground). The face carries the
three dents with embedded balls (set_impact lin 0..2 at t 1) and hairlines (set_cracks lin 1.0), but stands whole. Lin stands at the
wall foot (-13.8, -3.0) looking up at his wall (lin_watch, mirrored), then turns to us with a calm, confident smile and folded arms
(lin_calm), with the expression change hidden behind the blink at g 1501 on "ยังตั้งอยู่" (49.97 s). Camera: a slow push and drift from
(-13.4,-16.4,2.2) to (-10.6,-14.6,2.3), 20 mm, eased 0.35 sine + 0.65 linear. No DOF. Nobody speaks, so mouths are static.

## Numbers (qa.txt)
- Lin's head: 54-62 px wide, centre y 756-782 (0.59-0.61 H; this is a wide), bottom <= 813 (all above 880). No clipped sprites.
- Popcheck: no pops; no near-still frames (median change 1.31 levels); no black or magenta frames.
- Render: 13.1 s wall / 25.4 s CPU per frame (two processes at once, 2 threads each).
- Hue: red 40.0 / orange 32.4 / yellow 7.1 / blue 16.2 / violet 1.9 / magenta 2.4; saturation 0.33, value 0.62, dark 0.02. The report
  flags saturation and dark fraction as out of the band: this is the warm dawn look of the approved preset, and it was not re-graded.

## Differences from the plan
- No dissolve to a weathered "today" wall: per the director's assignment, shot 17 is dawn after the battle only.
- Lin is not in the plan row; I added him for a calm payoff.

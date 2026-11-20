# s08 QA: film 20, shot 8 (artists jab at the window, black smoke) -- CAFE cafe_window, DAY
Delivered: take.mkv (41.7 MB, under 45), first_g 509, 99 frames. Shot g 513..603; handles 4 in (cut) / 4 out (cut at 604). 30.3 s/frame wall (two processes + other jobs), 43.8 s cpu, 8 spp.
qa_auto: PASS. `qa_stats.py`: saturation 0.565, brightness 99.6, in-shot motion median 4.39 p90 12.93 (my own 90x160 grey measure: 3.79 / 11.57, slightly lower; the director's tool passes).
Beats: the window shows the tower stub (arch + legs) from the first frame; forge smoke ramps 0 -> 1 over g 513..572 (17.10-18.96 s) and holds 1.0 on "เหมือนปล่อง / โรงงานสีดำ": a black column of puffs rises from the stub like a chimney. Four artists jab fingers at the window (~2.5 Hz, wider on the snap), 3 Hz breathing bounce, mouths held. Snap x1.15 g 570-585 and x1.12 g 588-602; slide -45 px/s (camera trucks left), push 5 %/s. Camera over the artists' shoulders: architect (back card) and painter (back card) at the left edge, composer + poet face the window; no artist card covers the window.
Colour: film-wide saturation grade raised to 1.30 (runtime `CO.setup_grade`), no DOF, no text. Mouths never animated.
## Deviations
- Checker floor is ~30-35 % of the frame at g 509-575 (target <= 25 %); ceiling ~35 %. More tilt would push the artists' heads into the caption band.
- The group is looser than "over the shoulder" in the first half (heads 90-140 px); from g 580 the camera closes to heads 200-300 px (about 20-25 % of frame height).
- Push is 5-8 %/s plus two snaps (the plan says 9 %/s); a stronger push ran the camera through the artists.
- Painter and architect are partly cropped by the left edge in the over-shoulder framing (back cards, intentional foreground); the poet leaves the right edge around g 600.

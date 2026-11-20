# T4 QA (g1058-1331, file g1052-1337, 286 frames, 720x1280, 12 spl)
Render: pit ~26 s/frame, coach stands ~55 s/frame (2 procs x 2 threads, shared). Script: shot.py (pit|stands), stands.py, post.py.
## Numbers
sat 0.70, vivid 75 %, luma 93, magenta 0 % (qa_stats2). Motion median 9.7, p90 25.0 (motion_check, cuts 1100,1148,1205,1273).
qa_auto: FAIL "suspected blur" on 28 frames = intended: official passing the lens (g1097-1104, 1144-1152) and the whip-pan streaks (g1203-1208, 1268-1277). No other fails.
## Angles (g)
- low hero beside the standard, bar ~30 cm over Dick's head, 2.46 m bar, 2.24 m board right: 1052-1096 (rocking)
- side tracking along the bar: attempt 1 1105-1146 (flop, bar falls g1140 = 38.0 s), attempt 2 1153-1186 (bar falls g1176 = 39.2 s); lands flat, hands on face 1187-1204
- through a foreground object: official card passes the lens 1097-1104, 1144-1152 (masks the swap Dick-under-bar -> Dick at his mark; attempt 1 -> 2, bar re-seated 2.24 m)
- WHIP up 1203-1208; coach in stands (maroon cap + windbreaker, dense crowd cards on every tread incl. parallax foreground cards) 1205-1267; coach 28-30 % of frame in the medium; mouth only 1211-1267 (40.38-42.25 s)
- punch CLOSE-UP 2: g1238-1262 (41.27-42.07 s); face ~25 % of frame
- WHIP back down 1268-1277
- hush push on Dick rocking at his mark, through a foreground frame of dark crowd heads: 1273-1337
BIGZOOM: none (not in T4).
## Round 2 (director FIX list)
1-2 low shot g1052-1096 reframed: Dick moved to x -0.5 off the standard line (pole no longer touches his head), camera 17 mm so the full 2.24 m board reads; the 2nd official moved out of the board.
3 landing g1182-1204: camera raised/closer (about 3.5 m, 28 mm), lying card 1.5x and leaned, Dick ~40 % of width / 15 % of height from g1188 (0.55 s), hands on face visible, bar rests below him (g1188 bar still crosses his torso, not the face).
4 hush g1273-1337: 4 dark crowd-head cards locked in front of the lens for the whole push (parallax drift), sparkles at 50 %.
5 whips: luma capped 125 (g1205-1207, 1269-1272) and lifted to 86-97 (g1273-1277): post2.py. 6 horizontal motion blur on the two official swaps (g1097-1104, 1144-1152); grey/discus props removed at (-1.9,9.1).
Numbers now: sat 0.71, vivid 76 %, luma 91, magenta 0 %, motion median 8.4 / p90 28.6.
## Fixes done in the take (set untouched)
coach-in-stands: closer camera, 3D crowd lifted, ~600 crowd cards on every tread, coach pool of light, press box hidden, black void filled in post.py; grey slab props near the run-up removed; hurdle "cloth" slab removed.
## Differences from plan
Dick rocks under the bar only 35.3-36.6 s; the run starts 37.1 so the bar falls on 38.0 / 39.2. Two masked swaps (official walking across the lens) instead of a continuous camera for the attempt change. Bar 2.46 m in the low shot, 2.24 m for the jumps. Faces: only the close-up exceeds 35 %? no: close-up face ~25 %.

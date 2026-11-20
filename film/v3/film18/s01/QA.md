# QA s01 (film 18, team 1) — BIGZOOM A: extreme wide -> medium on Tian Dan (replaces old s01 + s02)
Take: g 0-155 in-shot (156 frames) + 6 handle frames after (g 156-161); first_g 0, n_frames 162, g0 0, g1 156. jimo_in NIGHT, 720x1280, 12 samples, ~17 s/frame (two processes). transition_in: cut.
Move (one continuous eased path, no cut, no pulses; shot.py `camera(f)`): g 0-108 crane DOWN + push IN (smootherstep blended with a linear term so there is no dead hold; log-distance 86 D -> 7 D, lens 24 -> 32 mm) along a curved path over the wall top and tiled roofs (side arc 13 D, roofs / wall / flags pass the lens), end at MEDIUM on Tian Dan (camera (-8.6, 11, 2.0) looking at (-3.4, 16.1, 2.1)); g 108-155 push about 6 %/s plus a 7-degree orbit.
Set / action: whole ox yard, pens, lanterns, braziers and 70 dragon-dressed oxen (herd helper) at the start; Tian Dan tugs the dragon silk over the ox g 0-89 (coat grows onto its back), ties the bronze blades from g 90 ("ผูกมีด" g 97, he is already at medium); a warm point light + pool on him and the ox keeps him findable from g 0; world lantern on a stake; two basket carriers (woman, child) camera-locked in the lower third from g 60; contact shadows under him and the near oxen (far herd cards have no shadow quad: they are inside the lit yard).
## Measured on the camera / rendered frames
- Tian Dan height / frame height (3.0 D from the actual camera path): g0 2.3 % (< 5 % OK), g108 35.6 % (35-60 % OK), g155 41.7 %.
- Zoom duration g 0-108 = 3.6 s (3-6 s OK).
- Plain ground share (J.ground_share, 12-sample frames): g0 0.01, g108 0.14, g155 0.20 (<= 0.30 OK).
- Caption band y 880-950 at g155: mean 108.5, bright (>200) 0.00 % (clear).
## Frame-diff (90x160 grey, in-shot g 0-155)
median 8.09 (>= 4 OK), p90 11.26, min 2.52, max 17.61.
## Checks
qa_auto PASS. Real 360x640 phone_sheet.jpg. Heads above y 880 (his head ~y 330-470 at the end). No mouth moves, no text, no flames on tails.
Known: the carriers appear at g 60 when the camera is already low (they pop in at the lower edge); Tian Dan is hard to see at g 0-30 (he is a ~3 % figure on a lit patch); the old s02 take stays on the branch history as fallback.

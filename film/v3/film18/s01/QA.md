# QA s01 (film 18, team 1) — BIGZOOM A: extreme wide -> medium on Tian Dan (v2: rim light, 即墨 plaque, §I)
Take: g 0-155 in-shot (156 frames) + 6 handle frames after (g 156-161); first_g 0, n_frames 162, g0 0, g1 156. jimo_in NIGHT, 720x1280, 12 samples, ~17 s/frame (two processes). transition_in: cut.
Move: one continuous eased path (shot.py `camera(f)`), g 0-108 crane DOWN + push IN (86 D -> 7 D, lens 24 -> 32 mm) along a curved path over the wall top and roofs, MEDIUM on Tian Dan from g108, then g 108-155 push ~6 %/s + 7-degree orbit. No cut, no pulses.
§I additions: (1) cool moon-blue RIM light: each of Tian Dan and the hero ox has a slightly bigger, brighter blue-tinted backing copy of its card (cards are emissive, so the rim is drawn, not lit), beside the warm lantern / brazier key and the warm pool light on them; (2) saturation kept high (reds of the silk, deep blue sky); (3) sharp wooden plaque 即墨 (WenQuanYi Zen Hei, gold on lacquered board, painted texture on a world quad, two dark posts, warm light) at (-15, 17.6) in the yard; the zoom passes it: readable on the phone sheet g ~36-72 (>= 1.2 s); (4) Tian Dan never stands still: tug 2.2 Hz with bob / roll / lean until g89, then tying with a 1.4 Hz + 3.1 Hz sway.
## Measured
- Tian Dan height / frame height (3.0 D, actual camera path): g0 2.3 % (< 5 %), g108 35.6 % (35-60 %), g155 41.7 %. Zoom duration g 0-108 = 3.6 s.
- Plain ground share: g0 0.01, g108 0.15, g155 0.18 (<= 0.30). Caption band y 880-950 at g155: mean 104.9, bright 0.03 %.
- Colour (frames every 10): saturation 0.49, luma 97 (target sat >= 0.47, luma 85-110).
## Frame-diff (90x160 grey, in-shot g 0-155)
median 8.38 (>= 4 OK), p90 14.89, min 2.93, max 21.24.
## Checks
qa_auto PASS. Real 360x640 phone_sheet.jpg. Heads above y 880. No mouth moves, no flames on tails.
Known: the rim reads as a thin pale-blue edge, strongest on the hat and the ox's horn; at g 62-80 the plaque post (dark pole) crosses the frame edge as the camera passes; carriers pop in at g 60; Tian Dan is a ~3 % figure at g 0-30 (findable by the lit patch).

# QA s01 (film 18, team 1) — BIGZOOM A: extreme wide -> medium on Tian Dan (v3: gate-14 fixes)
Take: g 0-155 in-shot (156 frames) + 6 handle frames after (g 156-161); first_g 0, n_frames 162, g0 0, g1 156. jimo_in NIGHT, 720x1280, 12 samples, ~17 s/frame (two processes). transition_in: cut.
Gate-14 fixes: (1) the rim backing cards (ghost duplicates: second cap, extra legs) are DELETED; the cool moon-blue rim is now LIGHTS only (two blue spot lights behind / above the hero pair aimed at the camera side, no extra geometry); full-size stills at g110 and g150 checked: no duplicate cap, legs or hooves. (2) the basket carriers are REMOVED; a woman and an old man with baskets stand farther back in the yard (y 19, fully in frame, heads far above y 860). (3) the plaque is nudged 1.0 D back (y 17.6 -> 18.6): at g79-80 no post crosses a face.
Kept from v2: continuous eased crane-down + push over the roofs (86 D -> 7 D, lens 24 -> 32 mm, g 0-108 = 3.6 s) then 6 %/s push + 7-degree orbit; 70 dragon-dressed oxen, warm lanterns / braziers / pool on the pair; 即墨 plaque (gold on lacquer, readable g ~36-70); Tian Dan always moving (tug 2.2 Hz, then tying with 1.4 + 3.1 Hz sway); contact shadows under him and the near oxen.
## Measured
- Tian Dan height / frame height: g0 2.3 % (< 5 %), g108 35.6 % (35-60 %), g155 41.7 %.
- Plain ground share: g0 0.00, g108 0.13, g155 0.20 (<= 0.30). Caption band y 880-950 at g155: mean 124.1, bright 0.0 %.
- Colour (frames every 10): saturation 0.48, luma 100.
## Frame-diff (90x160 grey, in-shot g 0-155)
median 7.93 (>= 4 OK), p90 12.42, min 2.26, max 17.87.
## Checks
qa_auto PASS. Real 360x640 phone_sheet.jpg. Heads above y 880. No mouth moves, no flames on tails.
Known: the blue rim light mostly tints the ground and wall edges because the cards are emissive (it does not shade the drawn figures, so the rim on Tian Dan himself is faint); Tian Dan is a ~3 % figure at g 0-30; caption band mean is 124 at g155 (lit ground), above the 110 note level but with no bright pixels.

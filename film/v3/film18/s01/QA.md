# QA s01 (film 18, team 1) — BIGZOOM A: extreme wide -> medium on Tian Dan (v4: gate-15 fixes)
Take: g 0-155 in-shot (156 frames) + 6 handle frames after (g 156-161); first_g 0, n_frames 162, g0 0, g1 156. jimo_in NIGHT, 720x1280, 12 samples, ~17 s/frame (two processes). transition_in: cut.
Gate-15 fixes (patch render g 26-116, the rest of v3 untouched): the small rider (old man / woman with baskets behind the left foreground ox) is REMOVED; the herd oxen in the box x -23..-9, y 15..24.5 are removed so no ox is half-cut by the left edge at g 60-95; the plaque + posts slide 2.0 D (to (-16.5, 19.6)) and every frame g 60-95 was checked on a phone strip: no pole crosses any face, nothing is cut at the left edge. (Gate-14 fixes kept: no rim backing cards, lights-only rim, no basket carriers.)
Kept from v2: continuous eased crane-down + push over the roofs (86 D -> 7 D, lens 24 -> 32 mm, g 0-108 = 3.6 s) then 6 %/s push + 7-degree orbit; 70 dragon-dressed oxen, warm lanterns / braziers / pool on the pair; 即墨 plaque (gold on lacquer, readable g ~36-62); Tian Dan always moving (tug 2.2 Hz, then tying with 1.4 + 3.1 Hz sway); contact shadows under him and the near oxen.
## Measured
- Tian Dan height / frame height: g0 2.3 % (< 5 %), g108 35.6 % (35-60 %), g155 41.7 %.
- Plain ground share (J.ground_share): g0 0.00, g60 0.00, g108 0.15, g130 0.17, g155 0.20 (<= 0.30).
- Colour as v3 (saturation 0.48, luma 100).
## Frame-diff (90x160 grey, in-shot g 0-155)
median 7.27 (>= 4 OK), p90 11.63 (just under 12; v3 had 12.42), min 2.26, max 17.65.
## Checks
qa_auto PASS. Real 360x640 phone_sheet.jpg. Heads above y 880. No mouth moves, no flames on tails.
Known: the blue rim light mostly tints the ground and wall edges because the cards are emissive (it does not shade the drawn figures, so the rim on Tian Dan himself is faint); Tian Dan is a ~3 % figure at g 0-30; caption band mean is 124 at g155 (lit ground), above the 110 note level but with no bright pixels.

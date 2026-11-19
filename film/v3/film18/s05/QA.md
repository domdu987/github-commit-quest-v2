# QA s05 (film 18, team 1) — Tian Dan receives the general's sash at the market stall
Take: g 384-458 in-shot (75 frames) + 8 handle frames before (g 376-383) for the 11-frame dissolve; first_g 376, n_frames 83. jimo_in DUSK, 720x1280, 12 samples, ~16.5 s/frame. transition_in: dissolve 11. No handle after (s06 is a cut).
Applied (QA_ART_SET_R2 #6): Tian Dan moved in front of the counter (-74.2,21.6), face and hands clear between the woman and the old man, tiandan_accept_sash card with the sash across the counter; camera look-at lowered (tilt down ~5 deg), sky about 25 % of the frame at g 376-391; child and second old man behind the stall for density.
Camera: push 4 %/s, slide 25 px/s, 4 punch snaps (in/out pairs so the shot never closes on him), hand-held sway 0.009 rad.
## Frame-diff (90x160 grey, in-shot g 384-458)
median 4.08 (>= 4 OK), p90 10.68 (target >= 12: NOT MET), min 1.25, max 15.29.
## Checks
qa_auto PASS. Heads above y 880 (cyan line on phone sheet); no mouths move; no text.
Known: the old man is mostly at the left edge / hidden behind the shelf; the striped shelf items behind the stall were not hidden (they alias lightly); p90 short of 12.

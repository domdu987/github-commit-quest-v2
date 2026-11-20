# QA s06 (film 18, team 1) — "สิบตัว" (FINAL-gate fix)
Take: g 459-530 (72 frames), first_g 459, jimo_in DUSK, 720x1280, 12 samples, ~17 s/frame. transition_in: CUT.
Round-4 changes: the 10 plain oxen (no coats, no blades) were moved nearer the lens (y 15-17) so they and Tian Dan fill the frame, camera look-at raised, a child and an old man carrying baskets added at the right foreground from g 459, so bare ground is about 30 % at g 459-510 (was 40 %); dolly + 2.4 D truck + one held punch at g 497 as in round 3, no pulses; Tian Dan inside the frame all take.
FINAL-gate fix (Tian Dan cut by the left edge at g500-530): Tian Dan is now locked to the keyed camera (5.2 D in front of it, 0.55 D to the right of the axis, walk bounce kept), so his cap and body stay fully inside the frame (60+ px margin) for the whole take and nothing stands in front of him; the child and old man carriers stay lower left. cycles.transparent_max_bounces = 64. Everything else as before: 10 plain oxen (no coats, no blades), dolly + 2.4 D truck + one held punch at g 497.
## Frame-diff (90x160 grey, in-shot)
median 6.70 (>= 4 OK), p90 11.27 (just under 12), min 2.81, max 13.56.
## Checks
qa_auto PASS. Heads above y 880, no mouths, no flames, no blades, no text.

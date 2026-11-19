# QA s05 (film 18, team 1) — Tian Dan receives the general's sash (round-2 rework)
Take: g 384-458 in-shot (75 frames) + 8 handle frames before (g 376-383); first_g 376, n_frames 83. jimo_in DUSK, 720x1280, 12 samples, ~17 s/frame. transition_in: dissolve 11.
Round-2 changes (director ALL_TEAMS + QA-tech/QA-art): custom camera path (eased push ~8 %/s toward the stall, ONE held +15 % punch-in at g ~418, no pulses); camera tilted down, sky about 25 %; the navy 'counter' fg prop and the navy dig tools/baskets hidden (no placeholder slabs); the dark roof wedge at the right edge is gone; the HAND-OVER is now staged: the old man holds the sash out across the counter (g 384-413) and Tian Dan reaches, then holds it (g 414+); Tian Dan looks toward the giver / sash (head yaw), woman and child behind the counter, a basket carrier at the lower left.
## Frame-diff (90x160 grey, in-shot g 384-458)
median 3.39 (target >= 4: NOT MET), p90 5.33 (target >= 12: NOT MET), min 1.67, max 11.35.
## Checks
qa_auto PASS. Heads above y 880. No mouths move, no text, no oxen.
Known: motion is below target because the camera move is only the real eased push (no pulses, per rule 1); bottom third is still dusk ground with a single carrier; the sun disc sticker of the sky texture is still visible at the left edge.

# QA s03 = T03 v2 (render20/v2a, client rejection of rivet_v1: floats, shake, too close)
Timing, BIGZOOM (5 % -> 35 %), handles (8+8 dissolve) and first/last framing unchanged. 242 frames, g170-411, 8 spp, 720x1280.
## Changes
- FLOAT: Eiffel stood 12.7 D in the air (mark snapped onto the beacon column). Now on the ground, in front of the plan table (his mark moved 2.4 D / 6.4 D), lens shift +0.10 at the landing so less bare dirt.
- Canopy: 4 thick timber legs to the ground + soft contact shadow under the roof. Floating girders / crates / dark bits hidden. Riveters on the tower platforms now stand on plank decks (they hung in the lattice).
- Camera: crane from the table to the leg is one eased trapezoid blend (start g314), no fast blend, no pitch snap kink; lift over the yard 60 D.
- Post: unsharp mask on g170-182 and 376-379 (qa_auto blur check).
## Numbers
- ground_check PASS (GROUND.md). qa_auto PASS (QA_AUTO.md). 1 fps sheet: sheet_1fps.jpg.
- qa_jitter per second (take-aligned): see GROUND.md for the film-aligned list. Take-aligned: 0s 2.2 (BIGZOOM whoosh, declared), 5s 1.8, 6s 1.3, 7s 5.5 (g380-411 tail, declared).
- frame-diff median 9.64, p90 32.2.

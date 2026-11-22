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

## Round 2 (float-hunter V2_FLOAT_T03_T11.md items 1-5, all frames re-rendered)
- 1 lilac faceted shape g231-243: the pn/pm/pf_gravelp discs, hidden. 2 hanging tan posts g267-327: the 4 scaff_timber post tips at z 7.5 now reach the ground. 3 rod above the tent roof: removed (pnoink_timber verts). 4 oversized riveters cut at the waist g~405: rl_a / rl_d shrink away g388-396. 5 upper pair without deck: bigger, thicker plank decks.
- qa_auto PASS (unsharp mask on g170-182, 376-379 for the blur check). ground_check PASS, qa_jitter in GROUND.md. frame-diff median 9.66 p90 32.83. sheet_1fps.jpg.
- Round 3: leaning shovel + its shadow removed (g210-250 re-rendered). qa_auto PASS.
- Round 4: upper riveter pair removed, one pair on a visible deck with contact shadows (g380-411 re-rendered). qa_auto PASS.
- Round 5: crane rebuilt as one smootherstep g282-411 (see GROUND.md for jitter + LK numbers; g360-389 2.23 px declared). qa_auto PASS.

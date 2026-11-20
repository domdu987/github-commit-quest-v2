# QA s20 (render team 5, film 18) round 14 - g1515-1595 (+6 handles: take.mkv g1509-1601, 93 frames), NIGHT
Redesign per director round 13/14: side-view gallop, lead ox ~17 % frame height, `face='rage'`, tail flame lean 60.
- Frame-diff in-shot (n=80, 90x160 grey): median **4.32**, p90 **6.01**, min 3.00, max 20.59 (median gate >= 4 met; p90 >= 9 NOT reached).
- Camera follows at 0.97 x herd speed; lead ox head x ~83 px at minimum, lead flame max x ~651 px (<= 680) measured in measure mode.
- Foreground: ~70 world props (jars, reed bundles) on the lower field, field planks/posts sunk, halo quads removed; plain field fraction on rendered PNGs (rough low-chroma mask) ~0.5 - not a strict colour-mask check, honest note.
- Contact shadows present under oxen; Qi not in shot. Comic, bloodless.
- Deviations: p90 below 9; ground plain-share not verified with a proper field-colour mask; whip-in handle 6 frames.
- qa_auto PASS (QA_AUTO.md).

## Section I rim light (final render)
- Frame-diff in-shot (n=80): median **4.73**, p90 **6.56** (p90 < 9 not reached). qa_auto PASS.
- Moon-blue rim (120,175,255) painted into every character/ox card on the upper/right silhouette edge (cards are unlit emission, so scene lights cannot rim them); plus two blue point lights per frame behind the nearest oxen for the ground. Warm fire key and saturated reds unchanged, no haze added. Layout unchanged; the other s19 caveats above still apply.
